# REVIEW_ROUND3.md — Third pass after commits 7e9de9e..a086333

Date: 2026-04-22. Focus: remaining inconsistencies and overclaims not caught in Round 2. Read every section cold with the "only claims the data supports" principle.

---

## 🔴 Must-fix (violates the principle)

### R3.1. Evaluation section-lead contradicts its own §Pipeline Comparison on the "5-book overlap" framing.

**Section lead (evaluation.tex, line 4):**
> *The two pipelines overlap on 5 books (1 Kings, Esther, Habakkuk, Hosea, Micah), **enabling a head-to-head comparison on shared texts** in addition to corpus-wide aggregates.*

**Next subsection (evaluation.tex §A note on the comparison):**
> *inspection reveals that the two pipelines covered **different chapters** of these books with no overlapping verses—the regular-pipeline outputs for these books are experimental partial runs that never reached production. As a result, **no paired per-verse head-to-head comparison is possible** from the deployed corpus*

The lead claims exactly what the subsection explicitly denies. This is a direct self-contradiction within 150 words.

**Fix:** Rewrite the lead to match what the paper actually shows. Proposal:
> *The two pipelines overlap at the book level on 5 books (1 Kings, Esther, Habakkuk, Hosea, Micah) but cover different verses within them, so the comparison reported below is corpus-wide over each pipeline's own book set rather than a paired per-verse ablation.*

---

### R3.2. Architecture §Prompt Engineering still uses the old "30–70 word" BHT constraint — contradicts methods.tex after Round 2 fix.

**architecture.tex:**
> *BHT — single-paragraph synthesis from the extracted quotes. A regular variant produces a **30–70 word, 1–3 sentence paragraph** grounded in the tiered quotes (deployed for NT and for 24 OT books).*

**methods.tex (post-round-2):**
> *The output must be a single coherent paragraph of 30–80 words in 1–3 sentences.*

**intro.tex:**
> *Each BHT is constrained to 30–80 words in 1–3 sentences*

Three sections, two different numbers. Methods is now the canonical source; architecture was missed in Round 2.

**Fix:** In `architecture.tex`, change "30–70 word" → "30–80 word". Also: the sentence says split is for "15 narrative OT books plus a 5-book overlap" — the total is 20, which matches the data, but the phrasing implies 15 unique + 5 overlap as two additive sets. Clearer: "deployed for 20 OT books (predominantly narrative), 5 of which also appear in the regular-pipeline corpus as partial experimental runs."

---

### R3.3. Related Work revives the phantom "four-strategies comparison" claim we just killed in intro/abstract.

**related-work.tex §Retrieval-augmented generation:**
> *Our system extends this paradigm by **comparing multiple retrieval and chunking strategies—character-based, recursive, and semantic splitting—and evaluating their impact on downstream generation quality**.*

This claim is identical in spirit to the one we dropped from the introduction (R1) and softened in methods (§Phase 2). The paper never reports the downstream-impact evaluation, so this sentence overstates what we actually did.

**Fix:** Replace with:
> *Our system extends this paradigm by applying RAG specifically to multi-verse biblical commentary and organizing the retrieved context into a tiered structure across multiple independent commentaries before generation.*

(Drop the downstream-impact claim; keep the "tiered structure across multiple commentaries" contribution, which is real.)

---

### R3.4. Architecture claims a "form of ablation study applied to prompt design" that the paper doesn't report.

**architecture.tex §Prompt Engineering:**
> *Prompts went through multiple iterations (recorded in the repository), with the final deployed versions used to generate the corpus served on BibleGo.org. **Prompt versioning enabled systematic comparison of prompt effectiveness across generation runs, a form of ablation study applied to prompt design.***

No prompt ablation results appear anywhere in §Evaluation or §Discussion. The only per-prompt-version observations are qualitative remarks in the discussion ("explicit negative constraints were more effective than positive-only"). Calling this an "ablation study" overstates what's been demonstrated.

**Fix:** Change the last sentence to:
> *Prompt versioning enabled iterative comparison across generation runs, informing the qualitative lessons summarized in Section~\ref{sec:discussion}.*

(Drops "systematic" and "ablation study"; replaces with what the paper actually delivers.)

---

## 🟡 Softer issues (should fix)

### Y3.1. Abstract and intro both list "readability" as part of the scoring framework, but readability is never reported in evaluation.

**abstract.tex:**
> *a composite scoring framework combining semantic accuracy, readability, and source fidelity*

**introduction.tex** (contributions bullet 2):
> *A composite quality scoring framework that integrates semantic similarity, **readability metrics**, and source fidelity checks.*

Readability is computed internally (methods.tex §Phase 5 lists FKGL, FRE, Gunning Fog, ARI, Dale-Chall), but Round 2 already removed "readability" from the evaluation section lead because no subsection reports readability numbers.

**Fix options:**
- (a) **Preferred:** Drop "readability" from abstract and intro bullet to match what we actually show. The scoring framework in deployed practice is commentary-accuracy + quote-proportion + hard constraints; readability is collected but unused as a selection signal in the reported results.
- (b) Add a §Readability subsection in evaluation reporting corpus-wide means for the five readability metrics. (More work; only worth it if Eric wants to include them.)

Recommend (a).

### Y3.2. Discussion §Limitations has odd phrasing "interpretive source adherence."

**discussion.tex:**
> *relies heavily on embedding-based similarity, which may not capture all aspects of theological accuracy or interpretive source adherence.*

"Interpretive source adherence" is awkward and slightly redundant with "theological accuracy."

**Fix:** Change to "may not capture all aspects of theological accuracy or interpretive nuance." (More natural, same meaning.)

### Y3.3. Evaluation §Pipeline Comparison final sentence slightly contradicts its own caveat.

**evaluation.tex §Pipeline Comparison last paragraph (body):**
> *these corpus-wide means should be read as per-pipeline performance characteristics on the books each was actually deployed to—not as a controlled ablation.*

Good — this is the honest framing. But the figure caption immediately below says:
> *Corpus-wide means for the Regular and Split (combined) OT pipelines across each pipeline's own book set.*

Caption is fine. But the earlier paragraph still starts with "The two pipelines produce BHTs with similar commentary-accuracy means (1.78 vs. 1.82)…". 1.82 > 1.78 by 0.04, on two different book sets, with different difficulty characteristics. Saying they are "similar" is a judgment call readers might contest.

**Fix (minor):** Soften "similar" to "comparable" or just report the numbers without the editorial. Optional polish.

### Y3.4. Architecture §Prompt Engineering's "choicest range" paragraph includes a dangling claim.

**architecture.tex:**
> *A fourth family, choicest range—designed to extract single-verse quotes from commentary covering multi-verse ranges—was developed but not ultimately used in the deployed pipeline; **verse-range handling was instead addressed through the split pipeline's retrieval strategy**.*

This sentence conflates the *split pipeline* (two-stage generation) with the *retrieval strategy* (RAG, §Phase 2). The split pipeline doesn't actually address verse-range inputs via retrieval — it addresses them via the split-a/split-b decomposition. The RAG is a separate mechanism. This is a small technical inaccuracy.

**Fix:** Change to:
> *verse-range handling was instead addressed through retrieval-augmented generation (Phase~2) combined with the split pipeline for narrative OT books.*

---

## 🟢 Nits (optional)

### N3.1. Evaluation's "NT word count" paragraph uses "soft word-limit" three times.

**evaluation.tex:**
> *The observed NT mean (84.2 words) sits just above the **soft word-limit upper bound** (80). The generation loop runs up to five attempts per verse and, if no candidate satisfies the full set of **soft constraints** (30–80 words, quote-proportion, etc.), the highest-scoring attempt is retained regardless of which constraints it misses. This best-of-five fallback prioritizes commentary quality over strict length compliance, yielding a mean that slightly overshoots the **soft cap**…*

"Soft" appears three times in different phrasings ("soft word-limit", "soft constraints", "soft cap") in one paragraph. Stylistic polish.

**Fix (optional):** Settle on one term ("soft constraint") and use it consistently.

### N3.2. `evaluation.tex` still has a stale comment at line 1:
```tex
% Evaluation section - will be populated with real metrics and chart references
% after generate-charts produces the figures
```
The section is populated. The comment is historical scaffolding.

**Fix:** Delete the two comment lines.

### N3.3. `conclusion.tex` says "strong commentary accuracy" without citing a number.

> *the pipeline produces consistent, high-quality summaries with **strong commentary accuracy** and appropriate tier distribution.*

Minor qualitative claim; the numbers are in Tables 1 and 2. Fine as is, but if we want to be maximally rigorous we'd reference the tables.

---

## ✅ Verified good on this pass

- Abstract + intro scope matches what's evaluated (Round 2 fixes held).
- Methods §Phase 3 prompt constraints match the hard-gate numbers (Round 2 held).
- Table 1 label = "Commentary Accuracy" (Round 2 held).
- Human-eval count = 2 rounds (Round 2 held).
- Discussion quote-proportion framing is honest (Round 2 held).
- Architecture commentator tables still match source code.
- Platform user-count figures consistent with abstract/intro/conclusion.

---

## Recommended commit plan

Three commits would do it:

1. **Fix architecture + related-work overclaims** (R3.2 + R3.3 + R3.4 + Y3.4): unify BHT word constraint, drop phantom RAG-strategies-comparison claim, remove "ablation study" label, fix choicest-range dangling claim.
2. **Fix evaluation self-contradiction** (R3.1 + N3.1 + N3.2 + Y3.3): rewrite the section lead's 5-book-overlap framing, consistent "soft constraint" terminology, delete stale scaffold comment.
3. **Drop readability from abstract/intro scoring framework** (Y3.1 + Y3.2): align scoring-framework claims with what we actually report; fix "interpretive source adherence."

All three are small (1–3 line edits each). Rebuild paper.pdf after.

---

**Headline:** 4 🔴 issues and 4 🟡 issues, all of which trace to one of two patterns:
- **Phantom comparisons** that we thought we killed but survived in related-work.tex and architecture.tex (Round 2 only hit intro/abstract/methods).
- **Local self-contradictions** from prior commits where the section-lead wasn't updated when the body was reframed.

Nothing structural. All fixable in ~15 minutes.
