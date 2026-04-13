# BibleGoAI Research Paper — Session Handoff Document

**Created**: April 13, 2026  
**Purpose**: Transfer full context to continue this project on another machine.  
**Original session**: Copilot CLI session `6a31959d-231b-4da2-8889-26d578847118`

---

## 1. Project Overview

We are producing a **LaTeX research paper** documenting the **BibleGoAI** project — an AI/NLP system that synthesizes biblical commentary from 20+ commentators into concise summaries called **Brief Helpful Texts (BHTs)**, served via [BibleGo.org](https://www.biblego.org/).

- **Format**: Two-column academic paper (11pt, `article` class with `times` font)
- **Audience**: General — not targeting a specific conference or journal
- **Length**: Flexible (currently 14 pages), no page constraints
- **Authors**: Eric Hao, Brandon Xia, Esther Faulk, Rex Beck (all at BibleGo Ministry)
- **Acknowledgments**: 26 named individuals + "and many more"

### What is BHT?

**Brief Helpful Text** — the name reflects the project's core value: bringing the richness of difficult-to-read commentary to the fingertips of Bible readers in an accessible way. Each BHT is a 30–80 word paragraph synthesized from up to 9 primary commentators, with automated footnotes linking every claim back to its source.

---

## 2. Paper Structure (Section Order)

1. **Abstract** (~150 words) — `sections/abstract.tex`
2. **Introduction** — `sections/introduction.tex`
   - Mission, round table meetings, collaborative community context
   - Three design principles: Fidelity, Conciseness, Traceability
   - Two public launches: New Year's Conference Dec 2023 (NT), Memorial Day Conference 2024 (full Bible)
   - Four contributions
3. **Related Work** — `sections/related-work.tex`
   - Summarization, RAG, embeddings, digital humanities
4. **System Architecture** — `sections/architecture.tex`
   - TikZ architecture diagram (Figure 1) — carefully tuned spacing
   - Data sources (NASB Bible, 20+ commentaries)
   - Commentator tiering (Tier 1/2/3) with table
   - Prompt engineering (3 prompt families, versioned)
   - Commentary digitization subsection (Alford 2,544pg/28 volunteers + Govett 627pg, TikZ pipeline)
   - Original language tagging subsection (321K occurrences, 14K Strong's codes)
5. **Methods** — `sections/methods.tex`
   - 6 phases + TikZ flowchart
   - Phase 1: Quote extraction
   - Phase 2: Retrieval (FAISS, 3 chunking strategies)
   - Phase 3: BHT Generation (constrained)
   - Phase 4: Split-BHT variant
   - Phase 5: Scoring & validation
   - Phase 6: Footnoting & tagging
   - **The OT Challenge** (Section 4.7) — versification → enhanced extraction → RAG breakthrough
6. **Evaluation** — `sections/evaluation.tex`
   - Aggregate quality metrics table (NT: 7,957 verses, OT: 10,492 verses)
   - Generation strategy comparison (Regular vs Split-A vs Split-B)
   - Generation attempt analysis
   - Commentator tier contribution
   - Quality score distribution
   - Cross-model comparison (GPT-3.5 vs Llama 3.3 vs GPT-4o-mini, 13-verse preliminary)
   - Human evaluation (8 verses, mean 67.7/100)
7. **Discussion** — `sections/discussion.tex`
   - Strengths, limitations, source adherence vs fluency
   - Prompt engineering insights
   - Project process (ESV denied → NASB, 18 demos, round table)
8. **The BibleGo.org Platform** — `sections/platform.tex`
   - Commentary reading (3-column layout + desktop screenshot + mobile mockup)
   - Word study / Word Donut (desktop screenshot + mobile mockup)
   - Full commentary browsing (screenshot)
   - User experience (dark mode, 4 usability test rounds)
   - Data flow (PostgreSQL → Next.js → users)
9. **Conclusion and Future Work** — `sections/conclusion.tex`
10. **Acknowledgments** (unnumbered section in `paper.tex`)
11. **References** — `refs.bib` (17 entries)

---

## 3. Files & Directory Structure

```
paper/
├── paper.tex                    # Main document (modular \input structure)
├── refs.bib                     # 17 bibliography entries
├── generate_charts.py           # Python script → 4 PDF charts from BHT data
├── SESSION_HANDOFF.md           # This file
├── sections/
│   ├── abstract.tex
│   ├── introduction.tex
│   ├── related-work.tex
│   ├── architecture.tex         # Contains 2 TikZ diagrams
│   ├── methods.tex              # Contains 1 TikZ flowchart
│   ├── evaluation.tex           # References 4 chart PDFs
│   ├── discussion.tex
│   ├── platform.tex             # References 5 screenshots/mockups
│   └── conclusion.tex
├── figures/
│   ├── quality_distribution.pdf # Histogram of quality scores (NT vs OT)
│   ├── attempt_trajectory.pdf   # Score improvement by attempt 1-5
│   ├── strategy_comparison.pdf  # Regular vs Split-A vs Split-B
│   ├── tier_breakdown.pdf       # Tier 1/2/3 contribution
│   ├── word-donut.png           # Desktop Word Donut screenshot (203 KB)
│   ├── biblego-desktop-bht.png  # Desktop 3-column BHT reading view (859 KB)
│   ├── biblego-full-commentary.png  # Full commentary browsing mode (845 KB)
│   ├── biblego-bht-mobile.jpg   # iPhone mockup: BHT drawer (595 KB)
│   ├── biblego-bht-mobile.png   # Original PNG (9.9 MB) — JPG used in paper
│   ├── biblego-wordstudy-mobile.jpg  # iPhone mockup: Word Donut (495 KB)
│   └── biblego-wordstudy-mobile.png  # Original PNG (9.6 MB) — JPG used in paper
```

---

## 4. How to Compile

**Prerequisites**: MiKTeX (or any TeX distribution with pdflatex + bibtex).

```bash
cd paper
pdflatex -interaction=nonstopmode paper.tex
bibtex paper
pdflatex -interaction=nonstopmode paper.tex
pdflatex -interaction=nonstopmode paper.tex
```

Three pdflatex passes are needed for cross-references and bibliography.

**MiKTeX auto-install** (if packages are missing):
```
initexmf --set-config-value=[MPM]AutoInstall=1
```

**To regenerate charts** (requires Python with matplotlib, numpy):
```bash
cd paper
python generate_charts.py
```
This reads BHT JSON data from `../bht/` and writes 4 PDFs to `figures/`.

---

## 5. Key Data Sources

| Data | Location | Records |
|------|----------|---------|
| NT BHTs | `bht/nt bht v3/` | 7,957 verses |
| OT Regular BHTs | `bht/ot bht v1/bht/regular/` | 10,492 verses |
| OT Split-A BHTs | `bht/ot bht v1/bht/split-a/` | 12,653 verses |
| OT Split-B BHTs | `bht/ot bht v1/bht/split-b/` | 12,653 verses |
| Cross-model | `groq output/poc_comparison.json` | 13 verses, 3 models |
| Commentary corpus | `commentary/` | 20+ commentators |
| Tagged Bible | `bible/bible_tagged/`, `bible/tagged_occurrences/` | 66 books, 321K occurrences |
| Strong's dictionary | `bible/bible_dictionary.json` | 14,897 entries |

---

## 6. Key Metrics (from actual data)

| Metric | NT (n=7,957) | OT Regular (n=10,492) |
|--------|-------------|----------------------|
| Quality Score | 1.912 ± 0.348 | 1.785 ± 0.282 |
| Word Count | 84.2 ± 11.1 | 62.9 ± 11.6 |
| Quote Proportion | 39.6% ± 7.4% | 31.8% ± 6.3% |
| Verse Accuracy | n/a | 0.417 ± 0.147 |

**OT Strategy Comparison**:
- Split-A: highest quality (1.935), highest verse accuracy (0.467)
- Regular: balanced (quality 1.785, 62.9 words avg)
- Split-B: shortest (30.8 words avg), lower quality (1.710)

**Human Evaluation** (BHT V2 test, 8 verses): mean 67.7/100, range 50.4–94.2

---

## 7. Important Design Decisions & User Preferences

### Terminology
- **"Brief Helpful Texts"** (NOT "Bible Highlight Texts") — the name reflects the core value
- **"Source adherence"** (NOT "faithfulness") — replaced globally in all 5 section files
- **"Project direction"** (NOT "discussion") — for contribution descriptions in acknowledgments

### Content Decisions
- **GPT-3.5 framing**: It was among the leading models *at the time of development*. The newer model comparison (Llama 3.3, GPT-4o-mini) is framed as a preliminary study only, not as the primary corpus generation.
- **OT breakthrough narrative**: No drama or individual names — factual description of the challenge and RAG solution.
- **Page length**: Flexible — "more important to include everything necessary"
- **ESV → NASB**: ESV permission was denied by the publisher; NASB 1995 was selected with permission from the Lockman Foundation.
- **Two launches**: NT at New Year's Conference (Dec 31, 2023), full Bible at Memorial Day Conference (May 2024).

### Visual Design
- **Figure 1 (architecture)**: Iteratively refined over many rounds:
  - Background group boxes have `draw=none` (borders were rendering on top of labels)
  - Node borders lightened to `!40` opacity
  - Vertical spacing: 1.4cm between rows
  - Tech labels: first 2 below boxes, last 3 above, 0.35cm offset
  - "Data Sources" label: 0.5cm above boxes
  - "BibleGoAI Pipeline" label: 0.8cm above middle row
  - "Deployment" label: 0.8cm below bottom row
- **Figure 2 (digitization pipeline)**: `figure*` (full-width) to avoid overlap with text
- **Mobile mockups**: Compressed from ~10MB PNG to ~500KB JPG (quality=85)
- **Platform figures**: Use `[!htbp]` placement, `height=0.3\textheight` for mobile mockups
- **`\raggedbottom`**: Added to prevent LaTeX from stretching vertical space between sections
- **`placeins` package**: With `[section]` option to prevent figures floating past section boundaries

### TikZ Gotchas
- **`step` is a reserved TikZ keyword** — node style was renamed to `flowstep`
- **`on background layer` + `fit` nodes with borders** render ON TOP of content — use `draw=none`
- **Hebrew Unicode** causes errors in standard pdflatex — use transliteration only

---

## 8. The Human Story (Context for the Paper)

This context is woven throughout the paper, not just in one section:

### Project Process
- Weekly round table meetings with Christian volunteers and full-time ministry leaders (Cleveland, OH area)
- Brainstormed how AI could make commentary accessible to Bible readers
- Studied existing platforms (BibleHub, BlueLetterBible, StudyLight)
- Original commentaries sourced from StudyLight.org
- Many rounds of website design discussions, user testing, brainstorming website names

### Commentary Digitization
- **Alford's NT for English Readers**: 2,544 pages, 4 volumes, 27 NT books. 28 volunteers spent hundreds of hours correcting OCR output via coordinated Google Drive spreadsheet. Three-stage pipeline: Tesseract OCR + Google Cloud Vision → human correction → automated consolidation.
- **Govett's Commentary on Revelation**: 627 pages, same pipeline, 274 verse files across 22 chapters.
- Both digitization projects are significant scholarly contributions independent of the AI pipeline.

### The OT Challenge
- After NT launch, team turned to OT
- Critical structural difference: OT commentary is rarely verse-by-verse
- Tried GPT-based verse tagging ("versification") — inconsistent
- Considered manual human tagging — prohibitively labor-intensive
- **Breakthrough**: An AI/ML engineer suggested RAG → produced satisfactory results
- This unlocked OT BHT generation and completion of the full Bible corpus

### Word Donut
- Major sub-project to build interactive word study tool
- Each word in the Bible tagged to its Hebrew/Greek Strong's number
- Taggings provided courtesy of NASB
- `parse-bible` repo (separate from BibleGoAI) prepared the tagged data
- 321,621 tagged occurrences, 14,141 Strong's codes
- Doughnut chart shows translation frequencies

### Licensing
- ESV permission denied by publisher
- Selected NASB 1995 with permission from Lockman Foundation
- NASB's literal translation style works well with the commentary corpus

### Development Timeline
- 18 demo presentations (intensive April–May 2024 period)
- 6 rounds of user testing (BHT V2 Quality, OT V1 Quality, Usability Tests 1-2, User Tests 1-2)
- Google Drive files lost: User lost access to Google Drive account; many project docs are inaccessible

---

## 9. Related Repos & External Files

| Resource | Location | Description |
|----------|----------|-------------|
| BibleGoAI | `Desktop/BibleGoAI` | The AI pipeline repo (this paper's primary subject) |
| BibleGo | `Desktop/BibleGo` | Next.js web app deployed at biblego.org |
| digitizing-alford | `Desktop/digitizing-alford` | OCR pipeline for Alford's commentary |
| digitizing-govett | `Desktop/digitizing-govett` | OCR pipeline for Govett's commentary |
| parse-bible | `Desktop/parse-bible` | Pipeline for preparing Strong's tagged Bible data |
| VBI.pdf | `D:\Eric Stuff\...\BibleGo\User Interface\VBI.pdf` | Brand identity guide (noted, not in paper) |
| BHTGen1.png | `D:\Eric Stuff\...\BibleGo\` | NT pipeline workflow diagram |
| OT BHT Gen.png | `D:\Eric Stuff\...\BibleGo\` | OT pipeline workflow showing options explored |
| User test scores | `D:\Eric Stuff\...\User Testing\BHT V2 Quality\` | Human eval scores PDF |

---

## 10. Current State & Remaining Work

### What's Done
- ✅ All 9 sections fully written with real data
- ✅ 17 bibliography entries
- ✅ 3 TikZ diagrams (architecture, digitization pipeline, BHT generation flow)
- ✅ 4 data-driven PDF charts from 43,755 BHT records
- ✅ 5 platform screenshots/mockups integrated
- ✅ Human evaluation section with scores table
- ✅ "Brief Helpful Texts" (corrected from "Bible Highlight Texts")
- ✅ "Source adherence" (replaced "faithfulness" globally)
- ✅ Paper compiles cleanly to 14 pages

### What Could Be Improved / Added
- [ ] Review whether any figures still overlap text (was an iterative issue)
- [ ] The cross-model comparison section (Section 5.6) mentions Table `\ref{tab:crossmodel}` but the table itself may not exist — verify
- [ ] Could add more desktop screenshots if the user takes them
- [ ] Dark mode screenshot was discussed but not added
- [ ] Could clean up the large PNG originals of mockups (9.6–9.9 MB each) since JPGs are used
- [ ] Full OT coverage is noted as future work (currently 24 of 39 OT books)
- [ ] A formal user study is listed as future work
- [ ] Consider adding the BHTGen1.png and OT BHT Gen.png workflow diagrams if they add value

### Known Issues
- `gunning1952fog` in refs.bib has an "empty journal" warning (it's a book, not a journal article)
- Cross-model chart was skipped because `poc_comparison.json` format didn't match expected structure
- Some `[h]` float specifiers get changed to `[ht]` by LaTeX (harmless warnings)

---

## 11. LaTeX Package Dependencies

The paper uses these packages (all available in MiKTeX/TeX Live):
```
inputenc, fontenc, times, geometry, graphicx, amsmath, amssymb,
booktabs, enumitem, hyperref, xcolor, tikz, caption, subcaption,
float, natbib, multirow, tabularx, microtype, placeins
```

TikZ libraries: `shapes.geometric, arrows.meta, positioning, fit, backgrounds, calc`

Custom colors: `tier1` (blue), `tier2` (green), `tier3` (orange), `pipeline` (dark blue-gray), `accent` (red)

---

## 12. Quick Reference — Compile & Verify

```powershell
# On Windows with MiKTeX:
$env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")
cd C:\Users\erich\Desktop\BibleGoAI\paper
pdflatex -interaction=nonstopmode paper.tex
bibtex paper
pdflatex -interaction=nonstopmode paper.tex
pdflatex -interaction=nonstopmode paper.tex
# Should produce paper.pdf (~2.6 MB, 14 pages)
```

---

*This document was generated from a Copilot CLI session spanning ~35 turns of iterative development, covering codebase exploration, full paper drafting, data-driven chart generation, visual refinements, and content additions based on the author's detailed project history.*
