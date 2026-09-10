# CCAR-P — Claude Certified Architect, Professional

Practice bank for Anthropic's most senior certification. One self-contained HTML file:
download, double-click, study. No install, no server, no network, no account. Progress
lives in your browser's local storage.

> **Unofficial.** Not affiliated with, endorsed by, or connected to Anthropic. These are
> original practice questions written against the *published* exam blueprint. No real
> exam content was used and none is reproduced here.

---

## The exam

| | |
|---|---|
| Code | CCAR-P |
| Items | 63 |
| Time | 120 minutes |
| Score | 100–1000 scale, **720 to pass** |
| Delivery | Online proctored, or a Pearson VUE test centre |
| Conditions | Closed book. No AI assistance. |
| Objectives | 38 graded objectives across 7 domains |
| Audience | Solution architects, AI/ML engineers, tech leads, senior SWEs |
| Assumed | 3+ years systems architecture; 6+ months production LLM work |

Blueprint: Exam Guide **v1.0, effective July 2026**, cross-checked across four
independent published summaries.

The Professional tier differs from Foundations in what it asks of you. Foundations asks
whether you can **design** a working Claude system. Professional asks whether you can
**own one in production** — ship it, defend the decisions to stakeholders, and keep it
safe and compliant across its lifecycle. Every question in this bank is written from
inside that assumption.

### Domain weights

| Domain | Blueprint | In this bank |
|---|---:|---:|
| Integration | 19% | 17.7% |
| Solution Design & Architecture | 17% | 17.8% |
| Evaluation, Testing & Optimisation | 16% | 15.5% |
| Governance, Safety & Risk Management | 14% | 13.4% |
| Stakeholder Communication & Lifecycle Management | 14% | 13.4% |
| Claude Models, Prompting & Context Engineering | 13% | 13.4% |
| Developer Productivity & Operational Enablement | 7% | 8.9% |

7% to 19% is the flattest spread of any Claude certification. There is no domain you can
safely skip — even Developer Productivity is about four items, more than the margin most
people pass by.

---

## What is in the file

- **1,617 questions** across the 7 domains, ~25 full 63-item mock papers
- **140 flashcards**, 20 per domain
- **80 "10 Things to Know" concepts** — 8 sets of 10, in a left-hand rail
- 70% workplace scenario / 30% direct recall
- 19% easy / 50% medium / 31% hard, tuned slightly harder than the real exam
- Single-answer (1,124), multi-select *Choose TWO/THREE* (327), next-step (166)

Every question carries four things: why the key is right, **why each individual
distractor fails**, a transferable concept to lock in, and the exam-craft tip — what
made it hard and how to spot the pattern under time pressure.

### The "10 Things to Know" rail

A collapsible left-hand panel, always available while you practise. Pick a domain and
you get its ten highest-leverage concepts, each with a description and a note on how the
idea actually shows up in a question stem. There is also an **Exam Essentials** set
covering the cross-cutting rules — the workflow-vs-agent decision, reading for the
binding constraint, why you cannot write a deterministic SLA for a probabilistic system.

### Modes

- **Practice** — filter by domain, difficulty, type, or set (All / Unseen / Missed /
  Bookmarked), plus full-text search over stems.
- **Flashcards** — flip, shuffle, filter by domain.
- **Progress** — accuracy by domain, difficulty and question type, plus your weakest
  topics ranked for drilling.

Keyboard throughout: `A`–`E` to pick, `Enter` to check and advance, `←`/`→` to move,
`S` to bookmark, `Space` to flip a card.

---

## How it was verified

Three independent layers, because each catches something the others cannot.

### 1. Structural validation

Every item is rejected at build time unless it passes: exact domain string, valid
difficulty and type, option-count matching type, key count matching type, one distractor
note per non-key option and none for keys, all four explanation parts present and
non-stub, no option referencing another by letter, no two options above 80% lexical
overlap, and no authoring commentary leaked into any field.

### 2. Mechanical audit at bank scale

Checks no single authoring batch can see: invented product facts, near-duplicate stems
across batches, absolute-language tells, and the answer-length tell.

**Cross-batch duplicate stems: zero**, across 22 batches written in parallel.

### 3. Blind verification — the one that matters

Every item was exported with the answer and explanation stripped, leaving only the stem,
the options and how many to choose. Independent verifiers answered them cold and their
answers were diffed against a key held in a separate file they never read.

| | |
|---|---|
| Coverage | **1,618 / 1,618 — 100%** |
| Agreement | **1,616 / 1,618 — 99.9%** |
| Disagreements | 2 |
| Low-confidence agreements | 1 |
| Disagreements on multi-select | **0 of 327** |

Zero multi-select disagreements is the number worth dwelling on. Over-keying — writing
three genuinely true options for a two-slot question — is the defect banks of this size
fail on most often, and the one hardest to catch by reading your own work.

Both disagreements were adjudicated by hand and **both items were withheld**, with the
reasoning recorded in the build. An item with two defensible answers is worse than no
item: it teaches a candidate to distrust their own correct reasoning.

---

## The defect that nearly shipped

At 1,116 items the audit found that **in 85% of questions the correct answer was the
longest option**. Chance is 25%.

A candidate could have scored 85% on this bank by always picking the longest answer,
learning nothing — and worse, would have trained a habit that fails on the real exam,
where options are length-matched. The cause is a natural authoring bias: you know why the
right answer is right, so you write it out fully, then dash off three short wrong ones.
It affected 16 of 23 batches, worst at 98%.

Two authoring agents had reported fixing it. Measurement showed they had not.

Repairing it took a dedicated pass over every affected batch, rewriting roughly a
thousand option texts under one rule: **change the wording, never which answer is
correct**. The real hazard was the opposite of the original defect — padding a distractor
with a hedge ("in some cases", "where appropriate") makes it defensible and converts a
clean item into an ambiguous one. Several agents caught themselves mid-edit doing exactly
that and reverted.

| | before | after |
|---|---:|---:|
| Key is the longest option | 85% | **26%** |
| Average key-minus-distractor | +56 chars | **+5 chars** |
| Batches showing a tell | 16 of 23 | **0** |

Multi-selects carried a milder form of the same bias (all keys being the longest options:
22% against a 10% baseline) and were corrected separately.

The build now prints this measurement on every run, so it cannot regress unnoticed.

---

## Honest limitations

- **The blueprint comes from published exam guides and community material**, not from an
  official Anthropic document in hand. Domain weights and exam mechanics were
  cross-checked across four independent sources and agree, but if you have the official
  guide, reconcile against it.
- **99.9% agreement measures internal consistency, not external truth.** It means an
  independent reader, working blind, reaches the same answer as the author. It does not
  prove the answer matches what Anthropic's examiners would mark correct.
- **Questions were deliberately written without specific product figures** — no prices,
  rate limits, cache TTLs, context numbers beyond the well-established 200K, benchmark
  scores or dated model strings. Where a scenario needed a number it belongs to the
  fictional organisation. This keeps the bank from teaching invented facts, but it also
  means it will not drill you on any figure the real exam expects you to have memorised.
- **Verifiers flagged roughly thirty items** for a second read — arithmetic inside a
  distractor, a stem that overstates, an option closer to defensible than intended. The
  clear cases were repaired; the register is at `build/ccarp/review/DEFECTS.md`.
- Certification content changes. Check the current official exam guide before relying on
  any specific claim here.

---

## A study sequence that works

1. **Read the 10 Things for one domain.** Ten concepts, five minutes. Do not skip to
   questions — the rail is what makes the questions teach rather than just test.
2. **Practise that domain on Easy + Medium** until you are around 85%.
3. **Add Hard.** Expect a drop. The hard items are where the trade-off reasoning lives.
4. **Live in the Missed filter.** This is the highest-yield thing in the app. Re-answering
   what you got wrong beats new questions by a wide margin.
5. **Check Progress → Weakest topics** and drill the bottom five.
6. Repeat per domain, then run mixed sets of 63 with no filter to simulate the paper.

Two habits worth building deliberately, because the exam rewards both:

- **Find the binding constraint before you read the options.** A CCAR-P stem almost
  always names the thing that is actually tight — a p95 budget, a cost ceiling, a
  regulator's reproducibility requirement, a team of two who must maintain it. Options
  that optimise a dimension the stem never mentioned are distractors.
- **Prefer the simplest thing that meets the requirement.** The most sophisticated option
  is a distractor more often than it is the key. If you cannot point at the requirement
  in the stem that the extra machinery satisfies, it is not the answer.

---

## Rebuilding

```bash
python build/ccarp/assemble.py --rebalance   # validate + bundle
python build/ccarp/audit.py                  # bank-scale defect scan
python build/ccarp/verify.py export 60       # blind batches, key held back
python build/ccarp/verify.py score           # diff verifier answers vs key
```

Sources are in `build/ccarp/questions/` and `build/ccarp/flashcards/`; the app shell is
`build/ccarp/template.html`; the left-rail content is `build/ccarp/tenthings.json`.
Authoring rules are in `build/ccarp/spec/`. The HTML is a generated artefact, committed
deliberately so the repo works by download alone.
