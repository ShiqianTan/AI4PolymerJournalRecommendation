# AI4PolymerJournalRecommendation

An interactive journal discovery guide for AI4Polymer and polymer informatics research.

## Project contents

- `deliverables/index.html` — responsive journal explorer with title search, subject filters, a configurable Web of Science record-count threshold (default 10), evidence labels, and a topic-oriented journal matching helper.
- `deliverables/AI4Polymer_journal_guide.xlsx` — sortable journal database, priority journal profiles, and source/method notes.
- `deliverables/assets/` — vector figures showing the top journals, inferred topic distribution, and long-tail frequency pattern.
- `deliverables/draw_figures.py` — dependency-free SVG figure generator. Run it from any directory with Python 3; it reads the data embedded in `index.html`.

## View the website

Open `deliverables/index.html` in a browser. The page and SVG charts work as static files; no server or package installation is needed.

## Data coverage and interpretation

The supplied Web of Science summary contains 61 visible journal rows and ends with “Showing 61 out of 977 entries.” The other 916 titles, query, query date, and publication-year window were not included. Counts therefore describe only the visible supplied summary and must not be interpreted as current annual output or acceptance probability.

Four journal profiles have official-source detail checked on 2026-10-11: *Polymers*, *ACS Applied Polymer Materials*, *Journal of Chemical Information and Modeling*, and *npj Computational Materials*. Other journal rows are discovery records with name-based subject hints and explicitly unverified journal policies. Journal metrics, APCs, and timelines can change; verify publisher pages before submission. First-decision time, submission-to-acceptance time, and post-acceptance publication time are kept separate where the publisher reports them.

Journal matching is a transparent first-pass heuristic, not a prediction of acceptance. It uses journal names, the supplied record counts, and the small set of verified OA/timing details. Confirm scope and recent comparable papers manually.

## Updating the figures

Edit the embedded journal records in `deliverables/index.html`, then run:

```bash
python3 deliverables/draw_figures.py
```

The charts are written to `deliverables/assets/` as scalable SVG files.
