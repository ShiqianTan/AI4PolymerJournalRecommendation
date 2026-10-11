"""Draw publication-frequency figures as portable, high-resolution vector SVGs."""
from pathlib import Path
import json
import re
from collections import defaultdict
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve().parent
html = (ROOT / "index.html").read_text(encoding="utf-8")
m = re.search(r"const DATA=(\{.*?\});\nconst records=", html, re.S)
if not m:
    raise SystemExit("Could not read embedded journal data from index.html")
data = json.loads(m.group(1))
rows = data["records"]
out = ROOT / "assets"
out.mkdir(exist_ok=True)
INK, MUTED, BLUE, TEAL, LINE, PAPER = "#142f43", "#607788", "#176b87", "#38a7a3", "#dbe6eb", "#f5f8fa"

def text(x, y, value, size=20, fill=INK, weight=400, anchor="start", extra=""):
    return f'<text x="{x}" y="{y}" font-family="Arial, PingFang SC, Microsoft YaHei, sans-serif" font-size="{size}" fill="{fill}" font-weight="{weight}" text-anchor="{anchor}" {extra}>{escape(str(value))}</text>'

def frame(title, subtitle, body, height=920):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="1600" height="{height}" viewBox="0 0 1600 {height}">
<defs><linearGradient id="hero" x1="0" x2="1"><stop stop-color="#102b40"/><stop offset="1" stop-color="#176b87"/></linearGradient><linearGradient id="bar" x1="0" x2="1"><stop stop-color="#176b87"/><stop offset="1" stop-color="#48b4ad"/></linearGradient><filter id="shadow" x="-10%" y="-10%" width="120%" height="130%"><feDropShadow dx="0" dy="8" stdDeviation="12" flood-color="#142f43" flood-opacity=".10"/></filter></defs>
<rect width="1600" height="{height}" fill="{PAPER}"/><rect x="48" y="38" width="1504" height="155" rx="26" fill="url(#hero)"/>
<circle cx="1445" cy="83" r="126" fill="#ffffff" opacity=".045"/><circle cx="1360" cy="192" r="78" fill="#7ce0cf" opacity=".09"/>
{text(92, 92, "AI4POLYMER  /  JOURNAL LANDSCAPE", 17, "#9ee0dd", 700, extra='letter-spacing="3"')}
{text(92, 145, title, 40, "#ffffff", 700)}{text(92, 174, subtitle, 17, "#d1e1e8")}
{body}<rect x="48" y="{height-55}" width="1504" height="1" fill="{LINE}"/>{text(58,height-25,"Source: supplied Web of Science journal-frequency summary · 61 visible titles · count window not supplied",14,MUTED)}
</svg>'''

# 1. Ranked bar chart — make every label readable and highlight the top three.
top = rows[:15]
body = ['<rect x="48" y="220" width="1504" height="610" rx="22" fill="#ffffff" filter="url(#shadow)"/>']
left, top_y, plot_w, row_h = 460, 267, 920, 34
maxv = max(r["count"] for r in top)
for i, r in enumerate(top):
    y = top_y + i * row_h
    body.append(text(left-20, y+18, r["title"], 17, INK, 600, "end"))
    w = plot_w * r["count"] / maxv
    color = "url(#bar)" if i < 3 else "#c5dce4"
    body.append(f'<rect x="{left}" y="{y}" width="{plot_w}" height="19" rx="9" fill="#edf3f6"/><rect x="{left}" y="{y}" width="{w:.1f}" height="19" rx="9" fill="{color}"/>')
    body.append(text(left+w+13, y+16, r["count"], 16, BLUE if i < 3 else MUTED, 700))
body.append(text(1460, 285, "WoS records", 14, MUTED, 600, "end"))
(out / "journal-frequency-top15.svg").write_text(frame("最常见的 15 本期刊", "频次反映这份检索结果中的发文分布，不代表期刊录用概率或当前年度发文量。", "".join(body), 920), encoding="utf-8")

# 2. Topic landscape — aggregate the provided records by the page's inferred title cluster.
groups = defaultdict(int)
for r in rows:
    groups[r["category"]] += r["count"]
palette = ["#176b87", "#38a7a3", "#77c8b4", "#f0ad68", "#8497c4", "#b7c9d1"]
total = sum(groups.values())
cx, cy, radius, thick = 515, 530, 235, 86
body = ['<rect x="48" y="220" width="1504" height="610" rx="22" fill="#ffffff" filter="url(#shadow)"/>']
angle = -90
for (label, val), color in zip(sorted(groups.items(), key=lambda kv: -kv[1]), palette):
    sweep = 360 * val / total
    end = angle + sweep
    large = 1 if sweep > 180 else 0
    import math
    x1, y1 = cx + radius*math.cos(math.radians(angle)), cy + radius*math.sin(math.radians(angle))
    x2, y2 = cx + radius*math.cos(math.radians(end)), cy + radius*math.sin(math.radians(end))
    ix1, iy1 = cx + (radius-thick)*math.cos(math.radians(angle)), cy + (radius-thick)*math.sin(math.radians(angle))
    ix2, iy2 = cx + (radius-thick)*math.cos(math.radians(end)), cy + (radius-thick)*math.sin(math.radians(end))
    d = f"M{x1:.1f},{y1:.1f} A{radius},{radius} 0 {large},1 {x2:.1f},{y2:.1f} L{ix2:.1f},{iy2:.1f} A{radius-thick},{radius-thick} 0 {large},0 {ix1:.1f},{iy1:.1f} Z"
    body.append(f'<path d="{d}" fill="{color}"/>')
    angle = end
body.append(text(cx,cy-7,total,39,INK,700,"middle")); body.append(text(cx,cy+25,"listed records",16,MUTED,400,"middle"))
legend_x, legend_y = 900, 365
for i, (label,val) in enumerate(sorted(groups.items(),key=lambda kv:-kv[1])):
    y=legend_y+i*64
    body.append(f'<rect x="{legend_x}" y="{y-17}" width="18" height="18" rx="6" fill="{palette[i]}"/>')
    body.append(text(legend_x+34,y,label,21,INK,600))
    body.append(text(1435,y,f"{val}  ·  {val/total:.1%}",18,MUTED,500,"end"))
body.append(text(900, 730, "分类依据期刊名称作初步归类，仅用于概览；期刊范围仍需逐本核验。", 16, MUTED))
(out / "topic-landscape.svg").write_text(frame("检索结果的主题分布", "将可见期刊记录数按名称启发式学科标签汇总。", "".join(body), 920), encoding="utf-8")

# 3. Long-tail curve — a clean rank/count profile for the visible titles.
ranked = sorted(rows, key=lambda r: -r["count"])
W,H=1350,550; x0,y0=150,745; x1,y1=1460,295
body=['<rect x="48" y="220" width="1504" height="610" rx="22" fill="#ffffff" filter="url(#shadow)"/>']
for tick in [0,20,40,60,80,100]:
    y=y0-(y0-y1)*tick/100
    body.append(f'<path d="M{x0} {y:.1f} H{x1}" stroke="{LINE}" stroke-width="1"/>')
    body.append(text(x0-18,y+5,tick,14,MUTED,400,"end"))
for tick in [1,10,20,30,40,50,61]:
    x=x0+(x1-x0)*(tick-1)/(len(ranked)-1)
    body.append(f'<path d="M{x:.1f} {y0} V{y0+5}" stroke="{MUTED}"/>')
    body.append(text(x,y0+28,tick,14,MUTED,400,"middle"))
coords=[]
for i,r in enumerate(ranked):
    x=x0+(x1-x0)*i/(len(ranked)-1)
    y=y0-(y0-y1)*r["count"]/100
    coords.append((x,y))
line_path = "M" + " L".join(f"{x:.1f},{y:.1f}" for x,y in coords)
body.append(f'<path d="{line_path}" fill="none" stroke="url(#bar)" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/>')
for i in [0,1,2,4,9,19,39,60]:
    x,y=coords[i]
    body.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="7" fill="{TEAL}" stroke="#ffffff" stroke-width="3"/>')
    body.append(text(x,y-15,ranked[i]["count"],14,BLUE,700,"middle"))
body.append(text((x0+x1)/2,806,"期刊排名（由 WoS 记录数从高到低）",16,MUTED,500,"middle"))
body.append(f'<text x="68" y="520" transform="rotate(-90 68 520)" font-family="Arial, sans-serif" font-size="16" fill="{MUTED}">WoS records</text>')
(out / "frequency-long-tail.svg").write_text(frame("发文频次呈长尾分布", "高频期刊之外，较多期刊只有少量命中；选择时还要结合课题相似度。", "".join(body), 920), encoding="utf-8")

print(f"Rendered 3 SVG figures for {len(rows)} visible journals.")
