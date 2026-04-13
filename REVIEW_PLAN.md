# BibleGoPaper — Review & Fix Plan

Generated: 2026-04-13

## Issues Found

### 🔴 Must Fix

1. **Missing cross-model table (Section 5.6)**
   - `evaluation.tex:105` references `\ref{tab:crossmodel}` but no such table exists
   - Compile log confirms: `Reference 'tab:crossmodel' on page 8 undefined`
   - **Fix**: Either add the table with whatever data is available, or rewrite the sentence to remove the table reference (since the next paragraph already summarizes the findings narratively)

2. **Missing space in discussion.tex (line 10)**
   - `"positions.Our constraint"` → missing space between sentences
   - **Fix**: `"positions. Our constraint"`

3. **Overfull hboxes — figures too wide for single column**
   - `platform.tex:15` (BHT mobile mockup): **28pt too wide**
   - `platform.tex:32` (word study mobile mockup): **28pt too wide**
   - `architecture.tex:64` (architecture TikZ diagram): **57pt too wide** — but this is a `figure*` so it's full-width; may be intentional overhang
   - `evaluation.tex:15` (aggregate table): **0.5pt too wide** — negligible
   - **Fix**: For the two mobile mockups, reduce `height=0.3\textheight` to something narrower, or switch to `width=\columnwidth` with a max height

4. **Duplicate data in aggregate table**
   - In `evaluation.tex`, "Quality Score" and "Commentary Accuracy" show identical values (1.912/1.785). Either they are truly the same metric (in which case remove the duplicate row) or one should be different.

5. **NT verse count inconsistency**
   - Abstract/intro/conclusion/evaluation text: **7,959**
   - Evaluation table header: **n=7,957**
   - Need to pick one and use it consistently

### 🟡 Should Fix

6. **`[h]` float specifiers changed to `[ht]`** (4 instances)
   - Harmless but indicates LaTeX couldn't place figures where requested
   - **Fix**: Change all `[h]` to `[htbp]` for better float placement

7. **Unused bibliography entries**
   - `brown2020gpt3`, `ouyang2022instructgpt`, `honnibal2020spacy`, `zhang2024survey` — defined in `refs.bib` but never cited in any `.tex` file
   - **Fix**: Either cite them where relevant or remove from `refs.bib`

8. **`gunning1952fog` bib entry type**
   - Defined as `@article` but has no `journal` field (it's a book)
   - Compile warning: "empty journal"
   - **Fix**: Change to `@book` with `publisher={McGraw-Hill}`

9. **Several underfull hbox warnings** (~10 instances)
   - Mostly in methods.tex and evaluation.tex from long technical terms
   - Low priority — cosmetic only. Could add `\sloppy` locally or adjust wording where egregious.

### 🟢 Nice to Have

10. **Build artifacts in repo**
    - `paper.aux`, `paper.bbl`, `paper.blg`, `paper.log`, `paper.out` are build artifacts
    - **Fix**: Add `.gitignore` to exclude them, keep `paper.pdf` for convenience

11. **Large original PNG mockups**
    - `biblego-bht-mobile.png` (9.9 MB) and `biblego-wordstudy-mobile.png` (9.6 MB) are not used in the paper (JPGs are used instead)
    - **Fix**: Could remove or move to a separate archive to slim the repo

12. **Abstract mentions "four generation strategies and three LLM backends"**
    - The strategies section covers Regular/Split-A/Split-B + RAG variants — arguably more than four
    - The three LLM backends (GPT-3.5, Llama 3.3, GPT-4o-mini) are only a 13-verse preliminary study
    - Consider softening: "comparing multiple generation strategies and preliminary cross-model evaluation"

---

## Proposed Fix Order

1. Fix #2 (missing space) — trivial
2. Fix #1 (crossmodel table ref) — remove dangling reference
3. Fix #5 (verse count consistency)
4. Fix #4 (duplicate table row)
5. Fix #3 (overfull mobile figures)
6. Fix #8 (bib entry type)
7. Fix #6 (float specifiers)
8. Fix #7 (unused bib entries)
9. Fix #10 (gitignore)
10. Fix #11 (large PNGs)
