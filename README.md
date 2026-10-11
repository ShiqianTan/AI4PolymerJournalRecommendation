# AI4Polymer Journal Explorer

A practical, evidence-aware journal discovery and matching tool for AI4Polymer and polymer informatics.

**Web of Science journal data updated through October 11, 2026.** The supplied file contains 977 unique journal titles and 3,267 records.

[Open the live GitHub Pages site](https://shiqiantan.github.io/AI4PolymerJournalRecommendation/) · [Download the Excel guide](deliverables/AI4Polymer_journal_guide.xlsx)

## What is included

- Search and filter 977 journals, with a configurable WoS record threshold (default: 10).
- Match journals to polymer, AI/computing, materials, chemistry, and engineering topics. Match scores explain title-based signals; they are not acceptance probabilities.
- Review 11 priority profiles with publisher-sourced scope, article types, metrics, stage-specific timing, OA options, fees, and links.
- Explore three figures and a sortable Excel database with source and method notes.

## Research landscape

![Top journals by Web of Science record count](deliverables/assets/journal-frequency-top15.svg)

![Exploratory journal subject groups](deliverables/assets/topic-landscape.svg)

![Record frequency across all journal titles](deliverables/assets/frequency-long-tail.svg)

## Priority profiles

*Polymers*, *ACS Applied Polymer Materials*, *Journal of Chemical Information and Modeling*, *npj Computational Materials*, *Macromolecules*, *Chemical Engineering Journal*, *Polymer*, *Digital Discovery*, *Nature Communications*, *Nature Computational Science*, and *Nature Machine Intelligence*. The last two are present in the supplied WoS list with one record each.

## Data notes

The source summary totals 3,267 records. Its percentages are rounded to three decimal places and sum to 100.144%. The search query and publication-year window are not included, so counts should not be interpreted as annual output, acceptance rates, or current popularity. Subject clusters are inferred from journal titles. Metrics, fees, policies, and timing change; verify publisher sources before submitting. A fast first decision can include editorial screening and is not the same as fast external review. Submission-to-acceptance includes author revision time when reported; acceptance-to-online is a separate stage.

The 11 priority profiles were checked against publisher sources on October 11, 2026. For the other titles, publisher-specific scope and policies remain unverified.

## Project files

- `deliverables/index.html` — interactive journal explorer; `index.html` at the repository root routes to it.
- `deliverables/AI4Polymer_journal_guide.xlsx` — journal database, priority profiles, and source/method notes.
- `deliverables/assets/` — SVG figures shown above and in the explorer.
- `deliverables/draw_figures.py` — regenerates the figures from data embedded in the explorer.

To regenerate figures, run `python3 deliverables/draw_figures.py`. GitHub Pages serves the interactive site at the live link above.
