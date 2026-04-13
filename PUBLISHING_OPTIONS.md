# Publishing Options for BibleGoAI Paper

*Compiled: April 13, 2026*

This document outlines publishing venues for the BibleGoAI research paper, organized by type and timeline. It includes deadlines, format requirements, fit assessment, and what would need to change in the paper for each venue.

---

## Table of Contents

1. [Preprint (No Peer Review)](#1-preprint-no-peer-review)
2. [Conference Demo Tracks](#2-conference-demo-tracks)
3. [Conference Main Tracks (via ACL Rolling Review)](#3-conference-main-tracks-via-acl-rolling-review)
4. [Workshops](#4-workshops)
5. [Journals](#5-journals)
6. [Comparison Matrix](#6-comparison-matrix)
7. [Recommended Strategy](#7-recommended-strategy)
8. [What Would Strengthen the Paper for Any Venue](#8-what-would-strengthen-the-paper-for-any-venue)

---

## 1. Preprint (No Peer Review)

### arXiv

| Field | Details |
|-------|---------|
| **URL** | https://arxiv.org |
| **Category** | cs.CL (Computation and Language) |
| **Deadline** | Anytime — submit whenever ready |
| **Format** | LaTeX or PDF, no page limit |
| **Review** | None (moderated for basic quality, not peer-reviewed) |
| **Cost** | Free |
| **Turnaround** | 1–3 business days to appear |
| **Indexed** | Google Scholar, Semantic Scholar, DBLP |
| **Citable** | Yes — gets a permanent arXiv ID (e.g., `arXiv:2604.xxxxx`) |

**Fit for BibleGoAI**: ★★★★★ — The paper is ready to submit as-is. No changes needed. Establishes priority and makes the work citable immediately.

**How to submit**:
1. Create an arXiv account (needs institutional endorsement or endorser for first submission to cs.CL)
2. Upload the `.tex` source files + figures as a `.tar.gz`
3. Fill in metadata (title, abstract, authors)
4. Submit — appears in 1–3 days

**Important**: Posting on arXiv does **not** prevent future peer-reviewed publication. Most venues (ACL, EMNLP, AAAI, journals) allow arXiv preprints.

---

## 2. Conference Demo Tracks

Demo tracks are specifically designed for deployed systems with real users — the best fit for BibleGoAI.

### EMNLP 2026 System Demonstrations

| Field | Details |
|-------|---------|
| **URL** | https://2026.emnlp.org/calls/demos/ |
| **Submission Deadline** | **~July 4, 2026** (announced via @emnlpmeeting; official page says TBA) |
| **Notification** | ~August 2026 (estimated) |
| **Camera Ready** | ~September 2026 (estimated) |
| **Conference** | October 24–29, 2026, Budapest, Hungary |
| **Format** | Up to **6 pages** + unlimited references/appendices, EMNLP style |
| **Requirements** | Paper + **2.5-min screencast video** + **live demo URL or installable package** |
| **Presentation** | Live demo + poster at the conference (at least one author must attend) |
| **Published in** | EMNLP 2026 Companion Proceedings (ACL Anthology) |
| **Review** | Peer-reviewed, no rebuttal stage |

**Fit for BibleGoAI**: ★★★★★ — BibleGo.org is live with real users, which is exactly what demo tracks want. The screencast requirement is easy (just record using the website). Key questions reviewers will ask:
- What is the novelty?
- How does it compare with existing systems?
- How was it evaluated? (user studies matter here)
- How is it licensed?

**What needs to change**:
- Trim from 12 → 6 pages (cut Related Work, compress Methods, keep Architecture + Platform + key Evaluation)
- Record a 2.5-min screencast showing BibleGo.org features
- Ensure biblego.org is live and accessible during review
- Submissions without evaluation may be desk rejected

### AACL-IJCNLP 2026

| Field | Details |
|-------|---------|
| **URL** | https://2026.aaclnet.org/ |
| **ARR Submission Deadline** | **May 25, 2026** (for main track long/short papers via ARR) |
| **Demo Track** | Not yet announced — check website |
| **Conference** | November 6–10, 2026, Hengqin, China |
| **Format** | ACL style, likely 6 pages for demos |

**Fit**: ★★★☆☆ — Similar to EMNLP but newer venue, smaller. Demo track not yet confirmed. Worth monitoring.

### ACL 2027 System Demonstrations (Projected)

| Field | Details |
|-------|---------|
| **Conference** | ~July 2027 (location TBA) |
| **Demo Deadline** | ~February 2027 (estimated based on ACL 2026 pattern) |
| **Format** | 6 pages + video + live demo |

**Fit**: ★★★★★ — Same as EMNLP demo track. Gives more time to strengthen evaluation.

### NAACL 2027 (Projected)

| Field | Details |
|-------|---------|
| **Conference** | ~Spring 2027 (dates/location TBA) |
| **Demo Deadline** | ~Late 2026 or early 2027 (estimated) |
| **Format** | Likely 6 pages + video + live demo |

**Fit**: ★★★★☆ — NAACL rotates with ACL in odd years. Good option if you miss EMNLP 2026.

---

## 3. Conference Main Tracks (via ACL Rolling Review)

Main conference tracks go through **ACL Rolling Review (ARR)** — a shared review system. You submit to ARR, get reviews, then "commit" your reviewed paper to a specific conference.

### How ARR Works

1. Submit paper to an ARR cycle (deadlines every ~10 weeks)
2. Receive reviews + meta-review (~10 weeks later)
3. Optionally revise and resubmit to the next ARR cycle
4. When satisfied, "commit" your paper + reviews to a specific venue

### Upcoming ARR Cycles

| Cycle | Submission Deadline | Reviews By | Can Commit To |
|-------|-------------------|------------|---------------|
| May 2026 | May 25, 2026 | ~August 2, 2026 | AACL 2026, EMNLP 2026 |
| August 2026 | August 3, 2026 | ~October 11, 2026 | EMNLP 2026 (if commitment deadline allows), future venues |
| October 2026 | October 12, 2026 | ~December 20, 2026 | ACL 2027, NAACL 2027 (projected) |
| ~January 2027 | ~January 2027 | ~March 2027 | ACL 2027 (projected) |

### EMNLP 2026 Main Conference

| Field | Details |
|-------|---------|
| **ARR Submission** | May 25 or August 3, 2026 |
| **Commitment Deadline** | ~August 2026 (TBA) |
| **Conference** | October 24–29, 2026, Budapest |
| **Format** | Long paper: 8 pages, Short: 4 pages (+ unlimited references) |

**Fit for main track**: ★★☆☆☆ — The paper would need significant strengthening for a main track: baselines, expanded human evaluation, inter-annotator agreement, ablation studies. Possible but substantial work.

---

## 4. Workshops

### NLP4DH 2026 (NLP for Digital Humanities)

| Field | Details |
|-------|---------|
| **URL** | https://www.nlp4dh.com/nlp4dh-2026 |
| **Submission Deadline** | ❌ **March 5, 2026** (PASSED) |
| **Conference** | July 6, 2026, San Diego (co-located with ACL 2026) |
| **Format** | Long (8 pages) or Short (4 pages), ACL style |
| **Published in** | ACL Anthology |

**Fit**: ★★★★★ — Perfect thematic fit (NLP applied to biblical/humanities texts). Unfortunately the 2026 deadline has passed.

### NLP4DH 2027 (Projected)

| Field | Details |
|-------|---------|
| **Conference** | ~2027 (likely co-located with a *CL conference) |
| **Deadline** | ~Early 2027 (estimated) |

**Fit**: ★★★★★ — If this workshop continues (it has run 6 years), it would be the ideal venue. The commentary digitization and Strong's concordance work are particularly relevant to this audience. Watch https://www.nlp4dh.com/ for announcements.

### Other Relevant Workshops (recurring, watch for 2027 CFPs)

- **LT4HALA** (Language Technologies for Historical and Ancient Languages) — focuses on historical/religious texts
- **NLP and CSS** (Computational Social Science) — if framing emphasizes community impact
- **Workshop on NLP for Religious Texts** — occasionally held at *CL conferences

---

## 5. Journals

Journals have no fixed deadlines — submit anytime. Review takes 2–6 months.

### Journal of Data Mining & Digital Humanities (JDMDH)

| Field | Details |
|-------|---------|
| **URL** | https://jdmdh.episciences.org/ |
| **Deadline** | Rolling (submit anytime) |
| **Format** | No strict page limit; submit via HAL, arXiv, or Zenodo first |
| **Review** | Peer-reviewed, open access |
| **Turnaround** | 3–6 months typical |
| **Cost** | Free (Diamond open access) |

**Fit**: ★★★★☆ — Good match for the digital humanities angle (commentary digitization, Strong's concordance). Less emphasis on ML baselines than *CL conferences. You'd upload to arXiv first, then submit the arXiv link to the journal.

### Digital Humanities Quarterly (DHQ)

| Field | Details |
|-------|---------|
| **URL** | https://digitalhumanities.org/dhq/ |
| **Deadlines** | Quarterly: January 15, April 15, **July 15**, **October 15** |
| **Format** | No strict page limit, flexible format |
| **Review** | Peer-reviewed, open access |
| **Cost** | Free |

**Fit**: ★★★☆☆ — More humanities-focused, less technical. Would need to reframe around the scholarly contribution (making commentary accessible) rather than the ML pipeline. The digitization efforts would be particularly valued here.

### Computational Linguistics (CL Journal)

| Field | Details |
|-------|---------|
| **URL** | https://direct.mit.edu/coli |
| **Deadline** | Rolling |
| **Format** | Long-form research articles |
| **Review** | Rigorous peer review (3–6 months) |
| **Published by** | MIT Press, ACL Anthology |

**Fit**: ★★☆☆☆ — Top-tier journal. Would need the same strengthening as a main conference track paper (baselines, formal evaluation). High bar but high prestige.

### Transactions of the ACL (TACL)

| Field | Details |
|-------|---------|
| **URL** | https://transacl.org/ |
| **Deadline** | Rolling |
| **Review** | Rigorous, can present at ACL/EMNLP/NAACL if accepted |

**Fit**: ★☆☆☆☆ — Very competitive. Not recommended without major evaluation upgrades.

---

## 6. Comparison Matrix

| Venue | Deadline | Pages | Peer Review | Fit | Effort to Prepare |
|-------|----------|-------|-------------|-----|-------------------|
| **arXiv** | Anytime | Any | No | ★★★★★ | None — submit as-is |
| **EMNLP 2026 Demo** | ~Jul 4, 2026 | 6 | Yes | ★★★★★ | Medium (trim + video) |
| **AACL 2026** | May 25, 2026 | 6–8 | Yes (ARR) | ★★★☆☆ | Medium–High |
| **NLP4DH 2026** | ~~Mar 5~~ | 4–8 | Yes | ★★★★★ | PASSED |
| **NLP4DH 2027** | ~Early 2027 | 4–8 | Yes | ★★★★★ | Low–Medium |
| **ACL 2027 Demo** | ~Feb 2027 | 6 | Yes | ★★★★★ | Medium (trim + video) |
| **NAACL 2027** | ~Late 2026 | 6 | Yes | ★★★★☆ | Medium |
| **JDMDH** | Anytime | Flexible | Yes | ★★★★☆ | Low |
| **DHQ** | Quarterly | Flexible | Yes | ★★★☆☆ | Medium (reframe) |
| **EMNLP 2026 Main** | May/Aug 2026 | 4–8 | Yes (ARR) | ★★☆☆☆ | High (baselines needed) |

---

## 7. Recommended Strategy

### Immediate (April 2026)
1. **Post to arXiv** as a technical report. The paper is ready. This makes it citable and establishes priority.

### Near-term (by July 2026)
2. **Submit to EMNLP 2026 Demo Track** (~July 4 deadline):
   - Trim to 6 pages focused on: system architecture, pipeline overview, key evaluation metrics, platform features
   - Record a 2.5-min screencast of BibleGo.org
   - Ensure the live site is stable during review
   - Optionally add a simple baseline comparison to strengthen the submission

### Medium-term (late 2026 – early 2027)
3. **Watch for NLP4DH 2027** — if announced, this is the best thematic fit
4. **Consider ACL 2027 Demo Track** as a backup if EMNLP 2026 doesn't work out
5. **Submit to JDMDH** if you want a journal publication (can do in parallel with conference submissions, as long as the versions are sufficiently different)

### If you want to go further
6. Add a zero-shot baseline, expand human evaluation, and target a **main conference track** via ARR

---

## 8. What Would Strengthen the Paper for Any Venue

Listed in order of impact per effort:

1. **Zero-shot baseline** (HIGH impact, MEDIUM effort)
   - Run GPT-3.5/4 with a simple "summarize this commentary" prompt, no pipeline
   - Score with the same metrics
   - Shows the pipeline adds value beyond raw LLM capability

2. **Expanded human evaluation** (HIGH impact, MEDIUM effort)
   - Current: 8 verses, project-team raters
   - Target: 25–30 verses, 2–3 independent raters, inter-annotator agreement (Cohen's kappa)

3. **Comparison with existing tools** (MEDIUM impact, LOW effort)
   - Show what BibleHub/StudyLight give users vs. what BibleGo BHTs provide
   - Can be qualitative (side-by-side examples) rather than quantitative

4. **User study with real users** (MEDIUM impact, HIGH effort)
   - Recruit Bible study participants outside the project team
   - Structured task: "Find insights about verse X using BibleGo vs. traditional tools"
   - Measure time-to-insight, satisfaction, accuracy

5. **Full cross-model comparison** (LOW impact, MEDIUM effort)
   - Expand from 13 verses to a meaningful sample (100+)
   - Currently too preliminary to draw conclusions

---

*This document will be updated as new deadlines are announced. Check venue websites for the latest information.*
