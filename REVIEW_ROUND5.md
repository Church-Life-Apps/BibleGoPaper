# Round 5 — Pre-submission sweep

Final pass after Rounds 1-4. Goal: catch anything that only shows up once the paper is structurally settled. Receipts-only; no net-new prose.

## 1. Figure regeneration

**Finding:** `figures/*.pdf` had been built by a prior run of `generate_charts.py` and still carried outdated labels. Round 2 already updated the script labels (`Commentary Accuracy` instead of `Quality Score`), but the rendered PDFs had not been regenerated.

**Fix:** Installed numpy + matplotlib in an isolated venv, repointed `generate_charts.py` from its Windows-absolute `REPO` to `/tmp/BibleGoAI`, and reran. All four figures regenerated:

- `figures/attempt_trajectory.pdf`
- `figures/quality_distribution.pdf`
- `figures/strategy_comparison.pdf`
- `figures/tier_breakdown.pdf`

**Corpus cuts now correct:**

- Attempt trajectory: n=43,755 first attempts across NT + OT regular + OT split-a + OT split-b (previously the text claimed NT-only and OT-split-only cuts).
- Tier breakdown NT: 31.8 / 31.2 / 37.0 (matches prior claim).
- Tier breakdown OT: 35.1 / 29.7 / 35.1 (full regular+split corpus — **not** 56/17/26 as the prior text claimed, which came from a split-b-only sample).
- Score distribution NT: 1.32 / 1.68 / 1.93 / 2.14 / 2.46 at 5/25/50/75/95 percentiles (n=7,957; matches prior claim).
- Score distribution OT full: 1.29 / 1.58 / 1.80 / 2.02 / 2.39 at same percentiles (n=35,798; **not** the 2,761-sample cut previously claimed).

**Eval text updated** to match the regenerated figures. Tier interpretation softened: both testaments show the tier instruction is not strongly followed (previously the text claimed OT followed the instruction at 56% Tier 1; the full corpus does not bear that out).

## 2. Cross-reference audit

- 8 `\label{sec:...}` defined. 5 referenced; 3 unreferenced (`sec:introduction`, `sec:discussion`, `sec:conclusion`). Unreferenced section labels are normal (anchor-only). No action.
- 10 `\label{fig:...}` + 3 `\label{tab:...}` defined. All tables and most figures referenced. 3 figure labels are unreferenced: `fig:digitization`, `fig:wordstudy-mobile`, `fig:strategy`. These render fine (figures auto-number by placement); a future edit pass could add in-text "see Fig. X" pointers but it's stylistic, not correctness.
- 0 undefined references, 0 undefined citations in pdflatex output.

**Verdict:** Reference graph is clean.

## 3. Bibliography audit

- 14 entries in `refs.bib`, 13 cited at least once.
- **1 unused entry: `groq2024llama`.** The paper does not mention Groq or Llama anywhere. Removed from `refs.bib`.
- All remaining 13 entries are cited. All `\citep{...}` calls resolve.

**Verdict:** Bibliography is clean, 13 entries, every entry earns its place.

## 4. Build

- 15 pages (unchanged from Round 4).
- pdflatex clean: 0 errors, 0 undefined references, 0 undefined citations, 0 "multiply defined" warnings.
- bibtex clean.

## 5. Not addressed in Round 5 (deliberate)

- **Related Work expansion (Y4.3).** Left thin. Without direction on venue/framing, expanding risks padding. Recommend holding until reviewer feedback or venue target is decided.
- **Caption consistency across all figures.** Round 4 rewrote the eval-section captions; architecture/platform captions are unchanged from pre-review. Would benefit from one more sweep but not required for submission-ready.
- **Appendix / prompt dump.** Full prompt text is archived in the project repository; reproducing it in an appendix is venue-dependent (short-paper tracks wouldn't want it).
- **Cover letter / venue-specific abstract.** Not drafted in this round; can be generated on request once a venue is chosen.

## Summary of Round 5 deltas on PR #9

| File | Change |
| --- | --- |
| `figures/*.pdf` | Regenerated with current labels and full corpus cuts (4 files) |
| `sections/evaluation.tex` | Three subsections updated to match figure numbers (attempt n, OT tier distribution, OT full-corpus percentiles) |
| `refs.bib` | Removed unused `groq2024llama` entry |

Paper is now submission-ready for reviewer pass.
