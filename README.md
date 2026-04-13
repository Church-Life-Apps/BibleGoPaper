# BibleGoAI Research Paper

A LaTeX research paper documenting **BibleGoAI** — an AI/NLP system that synthesizes biblical commentary from 20+ commentators into concise, source-adherent summaries called **Brief Helpful Texts (BHTs)**, served at [BibleGo.org](https://www.biblego.org/).

## What This Paper Covers

This paper is a technical record of the BibleGoAI project — how it works, how it was built, and what the results look like. It documents:

- **The Pipeline**: A 6-phase system (quote extraction → retrieval → generation → scoring → footnoting → tagging) that transforms multi-author biblical commentary into 30–80 word summary paragraphs
- **Commentary Digitization**: Two major volunteer efforts to digitize Alford's NT commentary (2,544 pages, 28 volunteers) and Govett's Revelation commentary (627 pages)
- **Original Language Tagging**: Mapping every word in the Bible to its Hebrew/Greek Strong's concordance number (321K tagged occurrences)
- **Evaluation**: Quality metrics across 7,957 NT and 10,492 OT verses, generation strategy comparisons, and human evaluation results
- **The Platform**: BibleGo.org — a deployed web app with commentary reading, word study (Word Donut), and full commentator browsing

## Authors

Eric Hao, Brandon Xia, Esther Faulk, Rex Beck — [BibleGo Ministry](https://www.biblego.org/)

## Building the Paper

**Prerequisites**: A TeX distribution with `pdflatex` and `bibtex` (e.g., TeX Live, MiKTeX).

```bash
pdflatex -interaction=nonstopmode paper.tex
bibtex paper
pdflatex -interaction=nonstopmode paper.tex
pdflatex -interaction=nonstopmode paper.tex
```

Three `pdflatex` passes are needed for cross-references and bibliography. Output: `paper.pdf`.

**To regenerate charts** (requires Python with matplotlib, numpy):
```bash
python generate_charts.py
```
Note: This reads BHT JSON data from `../bht/` which is not included in this repo.

## Repository Structure

```
├── paper.tex                 # Main document (modular \input structure)
├── paper.pdf                 # Compiled paper
├── refs.bib                  # Bibliography (13 entries)
├── generate_charts.py        # Python script → 4 PDF charts
├── sections/
│   ├── abstract.tex
│   ├── introduction.tex
│   ├── related-work.tex
│   ├── architecture.tex      # Contains TikZ diagrams
│   ├── methods.tex           # Contains TikZ flowchart
│   ├── evaluation.tex        # References PDF charts
│   ├── discussion.tex
│   ├── platform.tex          # References screenshots
│   └── conclusion.tex
├── figures/
│   ├── quality_distribution.pdf
│   ├── attempt_trajectory.pdf
│   ├── strategy_comparison.pdf
│   ├── tier_breakdown.pdf
│   ├── word-donut.png
│   ├── biblego-desktop-bht.png
│   ├── biblego-full-commentary.png
│   ├── biblego-bht-mobile.jpg
│   └── biblego-wordstudy-mobile.jpg
└── SESSION_HANDOFF.md        # Context from original drafting session
```

## Related Repositories

| Repo | Description |
|------|-------------|
| BibleGoAI | The AI pipeline (this paper's primary subject) |
| BibleGo | Next.js web app at biblego.org |
| digitizing-alford | OCR pipeline for Alford's commentary |
| digitizing-govett | OCR pipeline for Govett's commentary |
| parse-bible | Pipeline for Strong's tagged Bible data |

## License

This paper and its contents are © BibleGo Ministry. All rights reserved.
