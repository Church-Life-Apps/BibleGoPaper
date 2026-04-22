# REVIEW_ROUND2.md — Full-paper read with "only claims the data supports" principle

Date: 2026-04-22. Scope: every section as currently on branch `review/fixes` (through commit 05824a2). Ignores already-fixed items from FACT_CHECK.md.

---

## 🔴 Issues that violate the principle (must fix)

### R1. Intro promises a "systematic comparison of four generation strategies" that the paper never delivers.

**Where:** `introduction.tex`, Contributions list bullet 3:
> *A systematic comparison of four generation strategies—character-based RAG, recursive RAG, semantic RAG, and GPT-based tagging—across thousands of verses.*

**Reality:** The evaluation section does not report this 4-way comparison anywhere. Methods section (`methods.tex` §Phase 2) only mentions that these four retrieval variants "were evaluated"—no table, no numbers, no discussion in §Evaluation. The only strategy comparison in the paper is now Regular vs. Split (Table 2).

**Why this breaks the principle:** We're advertising a contribution the paper doesn't substantiate. A reviewer who flips from intro to evaluation will find the claim unsupported.

**Fix:** Replace the bullet with something we actually did. Proposal:
> *An OT-specific two-pipeline design (regular single-pass and two-stage split) that together covers all 39 books, with per-pipeline metrics reported across the deployed corpus.*

Also: **drop the "four retrieval variants" listing in `methods.tex` §Phase 2** (or demote it to one sentence saying retrieval-variant exploration informed the deployed design, without implying evaluation results exist).

---

### R2. "six rounds of structured user testing" — the two archived BHT user tests don't total six.

**Where:** `evaluation.tex` §Human Evaluation:
> *BHT quality was evaluated through six rounds of structured user testing conducted with members of the project's Bible study community:*

Only two BHT-focused tests are then described: BHT V2 Quality Test (NT) and OT BHT V1 Quality Test. Platform.tex separately mentions "four rounds of dedicated usability testing" (UI, not BHT content). Six does not match either count.

**Why this breaks the principle:** "Six rounds" is a specific number without a visible basis. Archives in `/tmp/BibleGoAI/demos/` show two BHT user-test directories, not six.

**Fix:** Either
- (a) Change "six rounds" to "two rounds" (matching the two described) and split out UI-usability mention as "four additional rounds of UI usability testing." Or
- (b) If there really were six BHT rounds (including unreported sampling/pilot passes), list them by name and date before asserting the count.

Safer default: (a).

---

### R3. Table 1 "Quality Score" label is a legacy alias; readers may assume it's different from Table 2's "Commentary Accuracy."

**Where:** `evaluation.tex` Table 1 (`tab:aggregate`) uses "Quality Score"; Table 2 (`tab:strategy`) uses "Commentary Accuracy."

**Reality (from `/tmp/BibleGoAI/src/bht/bht.py:300`):**
```python
"qualityScore": self.commentary_accuracy_score,  # included for legacy reasons
"commentaryAccuracyScore": self.commentary_accuracy_score,
```
Both fields hold the same number — the commentary-accuracy score. The "qualityScore" key is literally an alias kept for legacy JSON compatibility.

**Why this breaks the principle:** Two tables, two different column names, identical underlying metric. Reader naturally reads this as two different scores.

**Fix:** Rename Table 1's "Quality Score" row to "Commentary Accuracy" to match Table 2, and update the introductory sentence accordingly. One name, one concept.

---

### R4. Methods §Phase 3 still says "30–70 words" and "At least 50% of the words must originate from the provided quotes" — inconsistent with the rest of the paper.

**Where:** `methods.tex` §Phase 3 bullets:
- "single coherent paragraph of **30–70 words** in 1–3 sentences"
- "**At least 50%** of the words must originate from the provided quotes"

Versus:
- `methods.tex` §Phase 5 hard constraints: 30–80 words, 30–90% quote proportion (target 70%)
- `introduction.tex`: 30–80 words, 30–90% (target 70%)
- `evaluation.tex` and `discussion.tex`: 30–80 words, 30–90%

The §Phase 3 numbers describe the **natural-language prompt text**, not the enforced hard gate — which is explicitly noted two paragraphs later. But as written, the reader sees three different word ranges (30–70, 30–80, 20–100 strict) and two different quote thresholds (50%, 30–90%) without a clear reason.

**Why this breaks the principle:** These are factual claims about what the prompt says vs. what the gate enforces. A careful reader has to reconcile them; a skimmer concludes the paper is sloppy.

**Fix:** Either:
- (a) Collapse the §Phase 3 numbers to the deployed hard-gate numbers (30–80 / 30–90%), removing the prompt-vs-gate distinction entirely. Simpler and honest: what matters to the reader is what got enforced.
- (b) Keep the prompt-vs-gate distinction but flag the difference explicitly in §Phase 3 (not just §Phase 5). E.g., "The prompt asks for 30–70 words and at least 50% quote words; the hard acceptance gate at validation time is wider (30–80, 30–90%) — see §Phase 5."

Recommend (a). The prompt-text-vs-gate asymmetry is a deployment detail that doesn't help the reader.

---

### R5. Discussion's "Source adherence vs. fluency" paragraph's corpus-level quote-proportion numbers are the only place NT=39.6% appears without the caveat that quote-proportion measurement methodology is itself approximate.

**Where:** `discussion.tex`:
> *the observed corpus-level means (39.6% for NT, 31.8% for OT; see Table~\ref{tab:aggregate}) sit comfortably inside this range.*

Both numbers are far below the 70% **target** and below the 90% **upper bound** but inside the 30–90% **acceptance** range. The sentence says this "sits comfortably inside" which is technically true for the 30% floor but misleading re: the 70% target — the deployed corpus consistently **undershoots** the target by 30+ percentage points.

**Why this breaks the principle:** "Sits comfortably" implies the target is being met. It is not.

**Fix:** Replace the last clause with something like:
> *the observed corpus-level means (39.6% for NT, 31.8% for OT; see Table~\ref{tab:aggregate}) satisfy the 30% floor and stay well below the 90% ceiling, but consistently fall short of the 70% target. In practice, BHTs tend to paraphrase more than the target would suggest; we discuss this gap and its implications for source fidelity below.*

(Optional follow-up: add a sentence acknowledging this is a known gap between target and deployment.)

---

## 🟡 Issues that weaken a claim (should fix)

### Y1. Abstract's "up to nine primary commentators" — per-BHT or per-corpus?

**Where:** `abstract.tex`:
> *Each BHT distills the most striking insights from up to nine primary commentators into a single 30–80 word paragraph*

"Nine" refers to the size of the NT commentator corpus (9 commentators, Table 1). But "Each BHT distills … up to nine" reads as a per-BHT bound.

**Reality:** A single BHT's quote pool only includes commentators that actually wrote on that verse (often far fewer than 9, especially for OT). And the OT corpus has 12 commentators, not 9 — so the "nine" number is NT-specific anyway.

**Fix:** Change to "up to fourteen commentators" (the full NT ∪ OT set) or, more accurately, drop the numeric bound: "from the curated corpus of tiered commentators."

---

### Y2. Abstract says "multi-strategy retrieval" but the evaluation only reports one pipeline pair (regular vs. split).

**Where:** `abstract.tex`:
> *quote extraction, tiered synthesis, multi-strategy retrieval, iterative generation with constraint enforcement*

After R1's fix, "multi-strategy retrieval" becomes yet another unsupported claim.

**Fix:** Change to "retrieval-augmented generation" (singular). Or "quote extraction, tiered synthesis, retrieval-augmented generation for long-form commentary, iterative generation with constraint enforcement."

---

### Y3. Intro's OT figure breakdown is accurate but dense, and the "with overlap on 5 books" parenthetical is now known to be experimental partial runs, not production coverage.

**Where:** `introduction.tex`:
> *the full Old Testament (all 39 books; 10,492 verses generated via a regular single-pass pipeline and an additional 12,653 verses via a two-stage split pipeline, with overlap on 5 books)*

The "overlap on 5 books" wording is literally true but misleading — those 5 regular-pipeline books are partial experimental runs that never reached production; users on BibleGo.org for those books see split-pipeline BHTs. We say this honestly in §Evaluation but pitch it without the caveat in Intro.

**Fix:** Drop the "with overlap on 5 books" clause from intro entirely. The 24 + 20 = 44 > 39 math implies overlap without us flagging it; a reader who cares will find the detail in §Evaluation where it's properly caveated.

Proposed:
> *the full Old Testament (all 39 books, served via two pipelines: a single-pass regular pipeline for 24 books and a two-stage split pipeline for 20 books, described in §Evaluation)*

---

### Y4. Evaluation's §Aggregate Quality Metrics sentence "likely reflecting the more extensive commentary coverage for New Testament verses and the maturity of the NT prompt versions."

**Where:** `evaluation.tex`:
> *The NT corpus achieves higher average quality scores (1.912 vs. 1.785), likely reflecting the more extensive commentary coverage for New Testament verses and the maturity of the NT prompt versions.*

Both speculations are reasonable but unverified by the paper. We don't report per-verse commentator counts to substantiate "more extensive coverage," and "maturity of NT prompt versions" is subjective.

**Why this is soft:** "Likely" hedges adequately. But the principle says: if we don't have the data, say less.

**Fix:** Trim to:
> *The NT corpus achieves higher average commentary-accuracy scores (1.912 vs. 1.785), with longer BHTs (84 vs. 63 words) and higher quote proportions (39.6% vs. 31.8%). These differences are consistent with the structural contrast between NT (verse-by-verse commentary, direct per-verse extraction) and OT (multi-verse commentary, retrieval-augmented) pipelines described in §Methods.*

Grounds the explanation in the methodological difference we actually do describe, rather than speculating about corpus-size or prompt-maturity effects we don't measure.

---

### Y5. Evaluation's §Commentator Tier Contribution subsection has a figure but zero prose.

**Where:** `evaluation.tex`:
```
\subsection{Commentator Tier Contribution}
Figure~\ref{fig:tiers} shows the distribution of semantic similarity across
the three commentator tiers, illustrating how well the tiering instructions
are followed during generation.
\begin{figure}...\end{figure}
```

One sentence, one figure. No actual numbers in the text. Same pattern for §Quality Score Distribution (one sentence + figure) and §Generation Attempt Analysis.

**Why this is soft:** It's not a falsehood, but a reader can't learn what the figures show without flipping to them. For §Tier Contribution specifically, we should at least state whether the tiering was followed (Tier 1 > Tier 2 > Tier 3 by what margin?) in prose, since this is a load-bearing design choice.

**Fix:** Add one sentence per subsection reporting the headline number from the figure. E.g., for §Tier Contribution: "Across both corpora, Tier 1 contributions exceed Tier 2 by a factor of roughly X and Tier 3 by Y, consistent with the 'primarily / sparingly / minimally' prompt language." (Numbers to be pulled from the tier-breakdown chart data.)

**Alternative:** Delete these sparse subsections and just reference the figures from §Aggregate Quality Metrics.

---

### Y6. Discussion's "Over 18 demo presentations" is specific and unverified.

**Where:** `discussion.tex` §Project process:
> *Over 18 demo presentations were prepared during an intensive April--May 2024 development period, each showcasing incremental improvements*

"Over 18" is an odd number to give without citing the archive. If the archive exists (it does, in `/tmp/BibleGoAI/demos/`), the exact count is verifiable; if not, we shouldn't assert it.

**Fix:** If Eric knows the count: say the exact number. If not: "Roughly 18 demo presentations …" or drop the number: "A series of weekly demos during the April–May 2024 development period."

(The demos archive under `/tmp/BibleGoAI/demos/nt bht archive/` plus `/ot bht archive/` plus others could be counted; I didn't, to avoid over-asserting.)

---

## 🟢 Nits (optional polish)

### N1. Related Work cites `nllb2022translate` that the build reports as undefined (from `paper.log`).

The bibliography has a missing entry `nllb2022translate` in `related-work.tex` §AI in digital humanities and biblical studies. Build warning:
> *Package natbib Warning: Citation 'nllb2022translate' on page 2 undefined*

**Fix:** Add the BibTeX entry for the NLLB-200 paper (Costa-jussà et al. 2022) to `refs.bib`, or drop the citation.

### N2. `paper.log` reported undefined references to `tab:nt-commentators` and `tab:ot-commentators` on first pass — resolved on second pass (they appear later in architecture.tex). Needs two `pdflatex` runs to resolve. Mention in README build instructions if not already.

### N3. Evaluation's lead sentence says "aggregate quality metrics, generation strategy comparison, generation attempt analysis, and readability" — but "readability" has no subsection. It only appears in §Phase 5's scoring list in methods.

**Fix:** Either add a §Readability subsection reporting the five readability metrics (FKGL, FRE, Gunning Fog, ARI, Dale-Chall) as corpus means, or remove "and readability" from the lead.

### N4. `abstract.tex` still says "multi-strategy retrieval" (addressed in Y2 above — same line).

### N5. `conclusion.tex` §Future work: "Unified OT delivery" bullet is good but reads confusingly without the §Evaluation context. Consider: "Unified OT delivery: consolidating the 5 partially-overlapping regular/split OT books into a single served variant per verse, enabling a cleaner head-to-head pipeline evaluation."

---

## ✅ Verified good

- **Table 2** matches `table2_data.json` and the caveat prose is honest.
- **Commentator tables** (Tables 1 & 2 in architecture) match `common.py` `get_commentator_tier()` for both testaments.
- **14 commentators / four centuries** is derivable: earliest Calvin (1509), latest Robertson (d. 1934). ✓
- **verse accuracy = USE cosine sim** — confirmed against `bht_analysis.py:244` → `compute_semantic_similarity` → `bht_semantics.py` (tfhub universal-sentence-encoder/4). ✓
- **min_accuracy_score = 2.3** — confirmed in `bht.py:71/85/99`. ✓
- **Split pipeline concatenation + averaged score** — confirmed in `post_ot_bhts.py`. ✓
- **All OT pipeline framing updates** (regular 24 books, split 20 books, paired-comparison caveat). ✓
- **User count / traffic phrasing** — consistent across abstract / intro / platform / conclusion. ✓

---

## Recommended commit plan (if you want to execute)

1. **R1 + Y2**: Drop phantom "four generation strategies" claim from intro + "multi-strategy retrieval" in abstract; replace with what we actually report.
2. **R3**: Rename Table 1's "Quality Score" row to "Commentary Accuracy"; update surrounding prose.
3. **R4**: Collapse methods §Phase 3 prompt numbers to the hard-gate numbers (30–80 / 30–90%).
4. **R2**: Fix "six rounds" → "two rounds" (plus separately cite four UI rounds if desired).
5. **R5 + Y4**: Tighten discussion's quote-proportion claim and evaluation's NT-vs-OT speculation.
6. **Y1 + Y3 + Y6**: Abstract bound, intro overlap parenthetical, "Over 18" demo claim — small phrasing fixes.
7. **Y5**: Either add one prose sentence per sparse evaluation subsection, or delete them.
8. **N1**: Add or drop the `nllb2022translate` citation.

Items 1–5 are the high-value fixes; 6–8 are polish.
