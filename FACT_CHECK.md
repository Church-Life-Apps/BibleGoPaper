# BibleGoPaper Fact-Check (against BibleGoAI code + BibleGo.org)

_Generated: 2026-04-22 04:05 UTC_
_Scope: full paper cross-checked against `/tmp/BibleGoAI` pipeline code, prompt archive, and https://www.biblego.org_

## Summary

- **6** factual errors found (🔴)
- **2** misleading / apples-to-oranges framings (🟡)
- **4** minor drift / wording issues (🟠)
- **3** unverifiable claims flagged for Eric (🔵)
- **Many** claims spot-checked and confirmed (✅)

Severity legend: 🔴 factual error · 🟡 misleading · 🟠 minor drift · 🔵 unverifiable · ✅ confirmed

---

## 🔴 Factual errors

### 1. "Nine primary commentators form Tier 1" (NT) — WRONG
- **Paper location:** `sections/architecture.tex:57` — *"For the New Testament, nine primary commentators form **Tier 1**: Henry Alford, Jamieson-Fausset-Brown, Albert Barnes, Marvin Vincent, John Calvin, Philip Schaff, Archibald T. Robertson, John Gill, and John Wesley."*
- **Reality:** The code tiers those nine commentators **across all three tiers**, not all into Tier 1. From `src/bht/common.py` `get_commentator_tier()` (lines ~465–475):
  - **Tier 1 (NT, 4):** Henry Alford, Jamieson-Fausset-Brown, Marvin Vincent, Archibald T. Robertson
  - **Tier 2 (NT, 2):** Albert Barnes, Philip Schaff
  - **Tier 3 (NT, 3):** John Wesley, John Gill, John Calvin
- **Evidence:** `/tmp/BibleGoAI/src/bht/common.py:464-478`
- **Proposed correction:** Rewrite the paragraph to distinguish the list of nine active NT commentators from the Tier-1 subset. Suggested replacement:
  > "For the New Testament, nine commentators form the active corpus: Henry Alford, Jamieson-Fausset-Brown, Albert Barnes, Marvin Vincent, John Calvin, Philip Schaff, Archibald T. Robertson, John Gill, and John Wesley. These are organized into three tiers: **Tier 1** (Alford, Jamieson-Fausset-Brown, Vincent, Robertson), **Tier 2** (Barnes, Schaff), and **Tier 3** (Wesley, Gill, Calvin)."
- **Impact: HIGH.** Table 1 (`tab:commentators`) is titled "Tier 1 New Testament commentators" and lists all nine, which is also wrong. Table caption + contents need fixing too.

### 2. Table 1 caption mislabels all nine as Tier 1
- **Paper location:** `sections/architecture.tex` — `\caption{Tier~1 New Testament commentators.}` with 9 rows.
- **Reality:** Same as #1 — only 4 of the 9 are actually Tier 1 in code.
- **Proposed correction:** Either (a) re-caption as "Active New Testament commentators, with tier assignment" and add a tier column, or (b) keep Table 1 but restrict to the 4 genuine Tier 1 commentators.
- **Impact: HIGH** (tied to #1).

### 3. Adam Clarke listed as part of OT corpus, but not in active OT commentator list
- **Paper location:** `sections/architecture.tex:57` — *"For the Old Testament, the corpus includes Keil & Delitzsch, Albert Barnes, **Adam Clarke**, and specialty commentators such as Arthur W. Pink and Charles H. Mackintosh."*
- **Reality:** `OT_COMMENTATORS` in `src/bht/common.py:97` has 12 entries: Jamieson-Fausset-Brown, Albert Barnes, John Gill, Keil & Delitzsch, Cyrus I. Scofield, Johann P. Lange, John Calvin, William Kelly, Charles H. Mackintosh, Charles A. Coates, Arthur W. Pink, Henri L. Rossier. **Adam Clarke is not present.** An `Adam Clarke/` directory exists under `commentary/` but there is no tier entry for him in `get_commentator_tier()` (his name would raise `"No tier defined for OT commentator"`).
- **Evidence:** `/tmp/BibleGoAI/src/bht/common.py:97-110`, `:464-500`.
- **Proposed correction:** Replace "Adam Clarke" with an actually-deployed commentator (e.g., John Gill or Johann P. Lange), or remove the named example and list the full 12-member OT roster.
- **Impact: MEDIUM.**

### 4. "10,492 OT verses across 24 books" framed as total OT coverage
- **Paper location:**
  - `sections/abstract.tex` — *"across 7,957 New Testament and 10,492 Old Testament verses"*
  - `sections/introduction.tex:15` — *"substantial portions of the Old Testament (10,492 verses across 24 books)"*
  - `sections/evaluation.tex` Table 2 (`tab:aggregate`) — OT $n=10{,}492$
- **Reality:** 10,492 verses / 24 books reflects **only the `regular` pipeline variant**. The `split-a` variant covers a disjoint-plus-overlap set of 20 books (12,653 verses). Union of regular (24 books) + split-a (20 books, 5 overlapping: 1 Kings, Esther, Habakkuk, Hosea, Micah) = **39 books — the full OT**. Split-a contributes the 15 books missing from regular: Genesis, Exodus, Leviticus, Numbers, Deuteronomy, Joshua, Judges, Ruth, 1 Samuel, 2 Samuel, 2 Kings, 1 Chronicles, 2 Chronicles, Song of Solomon, Zechariah.
- **Evidence:** Directory listings under `/tmp/BibleGoAI/bht/ot bht v1/bht/{regular,split-a,split-b}/`; `comm` of regular∩split-a yields the 5 overlap books.
- **Proposed correction:** The paper needs to reconcile two different framings (pick one and be explicit):
  - **Framing A (most honest):** "Across the full OT, we generated BHTs via two pipelines: a *regular* pipeline covering 24 books (10,492 verses) and a *split* pipeline covering the remaining 15 books plus 5 overlap (20 books, 12,653 verses). Together they provide coverage for all 39 OT books."
  - **Framing B (if only regular is 'deployed'):** Explicitly say so and note split-a/split-b are experimental arms. (Needs Eric input — see Q1.)
- **Impact: HIGH.** Touches abstract, intro, evaluation, discussion, and conclusion.

### 5. Future-work bullet: "Complete OT coverage … currently 24 are covered" — contradicts the project's own data
- **Paper location:** `sections/conclusion.tex` Future work bullet — *"Complete OT coverage: Extending BHT generation to all 39 Old Testament books (currently 24 are covered)."*
- **Reality:** BHTs exist in the repo for all 39 OT books (24 via regular + 15 additional via split-a). Also, `sections/methods.tex` §OT Challenge explicitly says the RAG approach *"ultimately enabl[ed] completion of the full Bible corpus"* — self-contradiction with the future-work bullet.
- **Evidence:** Union of `/tmp/BibleGoAI/bht/ot bht v1/bht/regular/` (24) ∪ `/tmp/BibleGoAI/bht/ot bht v1/bht/split-a/` (20) = 39 OT books; `sections/methods.tex` §7 last sentence.
- **Proposed correction:** Delete the "Complete OT coverage" bullet, or replace it with "Consolidating the regular and split-pipeline OT corpora into a single served variant per verse."
- **Impact: HIGH.** Directly contradicts methods.tex and the repo.

### 6. "Three LLM backends" (conclusion) overstates the model diversity
- **Paper location:** `sections/conclusion.tex:3` — *"The comparison of four generation strategies and **three LLM backends** provides practical guidance for similar systems."*
- **Reality:** Per `sections/discussion.tex`, *the entire deployed corpus was generated using GPT-3.5-turbo*. The cross-model comparison was an **informal 13-verse spot-check** against Llama 3.3-70B and GPT-4o-mini. Calling that "three LLM backends" in the conclusion's headline sentence overstates the evaluation.
- **Evidence:** `sections/discussion.tex:7` (limitations paragraph); `/tmp/BibleGoAI/src/bht/gpt_client.py:8` default model `gpt-3.5-turbo`.
- **Proposed correction:** Either soften to *"a preliminary cross-model comparison on 13 verses"* or drop the phrase. Suggested:
  > "The comparison of four generation strategies, together with a preliminary 13-verse cross-model check, provides practical guidance for similar systems."
- **Impact: MEDIUM.** Conclusion-level overstatement that's inconsistent with the discussion's own framing.

---

## 🟡 Misleading framings / apples-to-oranges

### 7. Table 2 (`tab:strategy`) compares Regular vs Split-A vs Split-B over different book sets
- **Paper location:** `sections/evaluation.tex` — Table 2 "Generation strategy comparison across OT verses" with n=10,492 / 12,653 / 12,653.
- **Reality:** Regular (24 books) and Split-A/Split-B (20 books) **cover largely disjoint OT book sets** (only 5 books overlap: 1 Kings, Esther, Habakkuk, Hosea, Micah). So "Split-A quality 1.935 > Regular 1.785" could reflect either strategy quality *or* inherent differences in the underlying books (e.g., Pentateuch + historical books vs. Psalms + prophets). This is an apples-to-oranges comparison.
- **Evidence:** Directory listings in `bht/ot bht v1/bht/{regular,split-a,split-b}/`.
- **Proposed correction:** Either (a) restrict Table 2 to the 5 overlap books so all three columns share the same underlying verses, or (b) keep the corpus-wide numbers but add a footnote / caveat: *"Regular and Split cover largely disjoint OT book sets; differences may partially reflect book-level commentary availability rather than strategy alone. A head-to-head comparison restricted to the 5 overlap books (1 Kings, Esther, Habakkuk, Hosea, Micah) is left to future work."*
- **Impact: HIGH** for any reader who would interpret Table 2 as a clean strategy ablation.

### 8. Architecture para calls Pink & Mackintosh "specialty commentators" — reads as low-priority
- **Paper location:** `sections/architecture.tex:57` — *"and **specialty commentators** such as Arthur W. Pink and Charles H. Mackintosh."*
- **Reality:** Both are **Tier 1 OT** in code — same tier as Keil & Delitzsch. Separately, `OT_COMMENTATORS` is split into `OT_GENERAL_COMMENTATORS = OT_COMMENTATORS[:7]` and `OT_SPECIALTY_COMMENTATORS = OT_COMMENTATORS[7:]` (`common.py:115,117`) — this is probably what "specialty" refers to, but the term in the paper reads as lesser importance when they are actually Tier 1.
- **Proposed correction:** Either use the code's own term "general vs. specialty" and explain it, or just say "Tier 1 OT commentators include Keil & Delitzsch, Arthur W. Pink, Charles H. Mackintosh, Charles A. Coates, and Henri L. Rossier."
- **Impact: MEDIUM.**

---

## 🟠 Minor drift / wording

### 9. "Over 20 commentators" — depends on counting method
- **Paper location:** `sections/introduction.tex:15`, `architecture.tex:57`, `conclusion.tex:1`.
- **Reality:** Distinct commentators *actively referenced in code* (union NT_COMMENTATORS ∪ OT_COMMENTATORS, ignoring `(parsed)` variants of same author): ~**14 unique names** (Alford, JFB, Barnes, Vincent, Calvin, Schaff, Robertson, Gill, Wesley, Keil & Delitzsch, Scofield, Lange, Kelly, Mackintosh, Coates, Pink, Rossier = 16 unique if counting Coates/Rossier). The `commentary/` directory has 14 unique non-parenthesized commentator folders. Neither count reaches "over 20". Saying "roughly 15 commentators" would be accurate; "over 20 curated sources" is only defensible if you count every digitized *source file family* (Alford, Alford (Greek), Govett, etc.).
- **Proposed correction:** Either change "over 20" → "~15 commentators" / "over a dozen commentators", or change "commentators" → "commentary sources" and define what a source is.
- **Impact: LOW-MEDIUM.**

### 10. BHT prompt version range "v0.1–v0.8"
- **Paper location:** `sections/methods.tex` Phase 3, `discussion.tex` prompt engineering para.
- **Reality:** `gpt prompts/bht/` contains BHT prompts through **v1.3** (plus split-a v0.1–v0.2 and split-b variants). v0.8 is evidently the last *deployed* NT version (matches the "50% words / 30–70 words" language the paper quotes), but v0.9–v1.3 do exist.
- **Evidence:** `ls '/tmp/BibleGoAI/gpt prompts/bht/'`
- **Proposed correction:** Either clarify — *"BHT prompts (v0.1–v0.8 deployed; v0.9–v1.3 exist as later iterations not used in the deployed corpus)"* — or leave as-is but add a footnote. Safest: keep "v0.1–v0.8" and add a single-sentence footnote.
- **Impact: LOW.**

### 11. "30–80 words" (abstract/scoring) vs "30–70 words" (BHT prompt) — self-consistent but flag-worthy
- **Paper location:** `methods.tex` Phase 3 ("30–70 words in 1–3 sentences"), §Scoring hard constraints ("30–80"), abstract ("30–80 word paragraph"), `bht prompt v0.8.txt` ("30 to 70 words").
- **Reality:** Code enforces a soft gate of `word_limits = (30, 80)` and strict gate `(20, 100)`; the *prompt* asks for 30–70 as a stylistic target. This is internally consistent as "prompt target vs. validation gate" — PR #8 already acknowledges this. Just document it in one place.
- **Proposed correction:** Add one sentence in methods §Phase 3 making the relationship explicit (something like: *"The prompt asks for 30–70 words as a stylistic target; the hard validation gate is the wider 30–80 range with a strict fallback of 20–100."*)
- **Impact: LOW.**

### 12. Evaluation section's observed mean word count (NT: 84.2) exceeds the hard gate upper bound (80)
- **Paper location:** `sections/evaluation.tex` Table 1 — *NT Word Count = 84.2 ± 11.1*.
- **Reality:** The hard gate is 30–80 soft / 20–100 strict. A mean of 84.2 implies a substantial fraction of NT BHTs are in the 80–100 "strict but not soft" band. Paper doesn't discuss why deployed corpus sits above the soft cap.
- **Proposed correction:** Add one-sentence note in evaluation: *"The NT mean (84.2) lies just above the soft word-limit upper bound (80) because validation falls back to the strict range (20–100) when no candidate lands inside the soft range; see §Scoring."* (Needs Eric confirmation — see Q2.)
- **Impact: LOW-MEDIUM.**

---

## 🔵 Unverifiable — need Eric input

### Q1. Is `split-a` (and `split-b`) deployed to production, or experimental-only?
The repo contains a full set of split-a BHTs for the 15 non-regular OT books (Genesis, Exodus, …, Zechariah). BibleGo.org's reading interface is fully JavaScript-rendered and I could not hit any public `/api/…` route (all tried endpoints returned 404 HTML), so I cannot confirm from the outside what the site serves for, e.g., Genesis 1:1 — whether it's the split-a BHT, nothing, or something else. **Paper claim #4 and future-work bullet #5 both hinge on this.** If split-a is deployed, the paper should claim 39-book OT coverage. If not, the paper should explicitly call split-a/split-b experimental and leave the "substantial portions / 24 books" framing but fix the future-work bullet.

### Q2. Are NT BHTs exceeding the 80-word soft cap intentional?
Related to finding #12 — confirm whether the 84.2 mean is by design (strict fallback) or an artefact.

### Q3. "Hundreds of monthly users" — any specific number?
Claim appears in abstract, intro, platform section, and conclusion. No analytics artefact in the repo to verify. Safe as phrased but if Eric has a tighter figure (e.g., "~300/mo", "500–800/mo") it would strengthen the paper.

---

## ✅ Spot-checked and confirmed

- NT coverage of 27 books, 7,957 verses (directory listing: 27 book folders under `bht/nt bht v3/`). ✓
- Default BHT generation settings: `proportion_limits=(0.3, 0.9)`, `target_proportion=0.7`, `strict=(0.2, 0.9)`; `word_limits=(30, 80)`, `strict=(20, 100)`, `target=50`; `attempts_limit=5`; `min_accuracy_score=2.3`. (`src/bht/bht.py:60-71`) ✓
- Tokenizer is gensim word-level, not BPE (`src/bht/bht_semantics.py:4`, `bht_analysis.py:3,130,305`). ✓
- GPT-3.5-turbo default for generation (`src/bht/gpt_client.py:8`). ✓
- Chunking strategies: `CharacterTextSplitter`, `RecursiveCharacterTextSplitter`, `SemanticChunker` — names match paper. ✓ *(not re-grepped in this round but confirmed by Eric previously.)*
- Cross-encoder footnoting via sentence-transformers. ✓
- NASB 1995 translation served, Lockman Foundation permission, ESV request denied — confirmed on https://www.biblego.org/about. ✓
- "Cleveland area group of Christians ministering to churches for years" — confirmed on /about. ✓
- Platform features exist (advertised on biblego.org homepage): Bible text with commentary, Word Donut ("language donut"), commentator browsing. ✓ *(Three-column desktop layout, dark mode, drawer mobile, font-size persistence, deep-linking — cannot directly verify due to JS-rendered DOM, but consistent with Next.js build metadata.)*
- Prompt families: `choicest/`, `choicest range/`, `bht/`, `tag commentary/` — four families exist in `gpt prompts/`. Paper references three (choicest, BHT, tag commentary); "choicest range" is not mentioned but that's a minor omission not an error.
- Choicest prompt range v0.1–v2.2 — confirmed (v0.1–v0.5, v1.0–v1.2, v2.1–v2.2).
- Each NT BHT draws from 9 commentators (verified by inspecting `Matthew 1 1 bht.json` — `choicestQuotes` has exactly the 9 NT commentators as keys). ✓
- Dec 2023 NT launch timestamp corroborated by `bestBHT.timestamp: "12-19-2023 23:42:59"` in `Matthew 1 1 bht.json`. ✓

---

## Open questions for Eric

1. **Q1 above (most important):** Is split-a deployed in production? This determines whether the paper should claim full OT coverage or continue framing as "24 books." It also determines whether Table 2's regular-vs-split-a comparison is a production-vs-production strategy ablation (still apples-to-oranges re: book sets) or a production-vs-experiment comparison (which changes framing).
2. **Q2:** Is the 84.2-word NT mean (above the 80 soft cap) intentional via strict fallback, or is there an explanation worth surfacing?
3. **Q3:** Any specific monthly-user figure to replace "hundreds"?
4. Should Table 1 be restructured to (a) show tier-by-tier, or (b) show only the 4 genuine Tier 1 NT commentators? (Current: lists all 9 under a Tier 1 caption.)
5. Should Adam Clarke be removed from the architecture narrative, or added to `OT_COMMENTATORS` if he was intended to be active?
6. Is the `choicest range` prompt family worth mentioning in methods §Prompt Engineering? (Paper lists only 3 families; 4 exist in the repo.)
