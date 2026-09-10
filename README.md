# Claude Certification — Exam Prep

Practice question banks for Anthropic's Claude certification exams. Four
separate banks, each a **single self-contained HTML file** — download, double-click,
study. No install, no server, no network calls, no account. Progress is saved in
your browser's local storage.

> **Unofficial.** Not affiliated with, endorsed by, or connected to Anthropic.
> These are original practice questions written against the *published* exam
> blueprints. They are not real exam questions and no exam content was used.

---

## The four banks

| Exam | File | Questions | Flashcards | Docs |
|---|---|---:|---:|---|
| **CCAO-F** — Claude Certified Associate, Foundations | [`Claude Certified Associate - Foundations.html`](<Claude Certified Associate - Foundations.html>) | 2,366 | 479 | [details](docs/CCAO-F.md) |
| **CCAR-F** — Claude Certified Architect, Foundations | [`Claude Certified Architect - Foundations.html`](<Claude Certified Architect - Foundations.html>) | 1,501 | 130 | [details](docs/CCAR-F.md) |
| **CCAR-P** — Claude Certified Architect, **Professional** | [`Claude Certified Architect - Professional.html`](<Claude Certified Architect - Professional.html>) | 1,617 | 140 | [details](docs/CCAR-P.md) |
| **CCDV-F** — Claude Certified Developer, Foundations | [`Claude Certified Developer - Foundations.html`](<Claude Certified Developer - Foundations.html>) | 1,506 | — | — |

**6,990 practice questions** in total.

All four carry a **"10 Things to Know"** study rail — a collapsible panel beside the
questions with the ten highest-leverage concepts per domain, and a note on how each
one shows up in a stem. 320 concepts in total, written per exam.

Each file is a few megabytes because everything is embedded — expect a moment's
pause on first open. That is normal.

---

## Which one do I need?

- **Associate (CCAO-F)** — broadest and most foundational. Start here if you are
  new to Claude or unsure which exam you are sitting.
- **Architect Foundations (CCAR-F)** — scenario-heavy, focused on design trade-offs:
  agentic architecture, tool and MCP design, Claude Code configuration, context
  reliability. Assumes you already build with Claude.
- **Architect Professional (CCAR-P)** — the most senior of the four. Where Foundations
  asks whether you can *design* a Claude system, Professional asks whether you can
  *own one in production* — ship it, defend the decisions to stakeholders, and keep it
  safe and compliant over its lifecycle. Adds governance, stakeholder work and lifecycle
  ownership on top of the Foundations material.
- **Developer (CCDV-F)** — hands-on implementation: API mechanics, tool
  implementation, agent construction, debugging, application security.

---

## CCAO-F — Associate, Foundations

**2,366 questions · 479 flashcards · 8 domains**

- 71% workplace scenarios / 29% direct recall
- Single-answer (1,846), multi-select *Choose TWO/THREE* (434), next-step sequencing (86)
- 22% easy / 50% medium / 28% hard
- Three tabs: Practice, Flashcards, Progress

| Domain | Questions |
|---|---:|
| Output Evaluation and Validation | 439 |
| Workflow Integration and Solution Design | 330 |
| Prompting and Task Execution | 305 |
| Technical Awareness | 304 |
| Governance, Risk, and Responsible Use | 301 |
| Product and Model Selection | 230 |
| Troubleshooting and Optimisation | 229 |
| Configuration and Knowledge Management | 228 |

All 2,366 stems are unique, across 2,181 distinct topics — roughly 39 full
60-item practice exams.


Every item carries why the key is right, why **each** distractor fails, a concept
refresher, and the exam trap being tested.


### "10 Things to Know" — the left rail

A collapsible panel beside the questions, opened from the header (or `Esc` to close).
Pick a domain and you get its ten highest-leverage concepts: what the idea is, and a
note on how it actually shows up in a question stem. Plus an **Exam Essentials** set
covering the cross-cutting rules. 90 concepts, written specifically for this exam.

Full methodology, verification results and study sequence: **[docs/CCAO-F.md](docs/CCAO-F.md)**

---

## CCAR-F — Architect, Foundations

**1,501 questions · 130 flashcards · 5 domains · all 30 blueprint task statements**

Weighted to the published blueprint:

| Domain | Blueprint weight | In this bank |
|---|---:|---:|
| Agent Architecture & Orchestration | 27% | 28.2% (424) |
| Prompt Engineering & Structured Output | 20% | 18.9% (283) |
| Claude Code Configuration & Workflows | 20% | 18.7% (281) |
| Tool Design & MCP Integration | 18% | 17.4% (261) |
| Context Management & Reliability | 15% | 16.8% (252) |

Covers all **8 exam scenarios**, including Conversational AI Patterns and Agentic
AI Tools, which most study material omits.

Every question carries the scenario stem, **per-option rationale for all four
options**, a detailed explanation (406 characters average), and a "Concept to lock
in" takeaway. The answer key is balanced A=376 / B=375 / C=375 / D=375 by a
seeded build-time shuffle, so there is no positional tell to learn.

**Modes:** Practice (filter by domain, task, scenario, or set) · **Exam Simulator**
(timed 60-question mock) · Weak Areas (accuracy per task statement, with one-click
drilling) · Flashcards (Leitner spaced repetition, 1/3/7/21-day intervals) ·
Search · Blueprint reference.

Keyboard: `A`–`D` answer · `→` next · `S` bookmark (`F` to flag during an exam).

### Exam Simulator

A full mock under real conditions — **60 questions, 120 minutes, no feedback until
you submit**. Each sitting seats the paper to the blueprint (D1:16 D2:11 D3:12
D4:12 D5:9) and draws **4 scenarios from the pool of 8**, as the real exam does.

Flag questions for review, jump around with the question navigator, and let the
clock run on wall time — reloading restores your paper rather than resetting it.
Submitting gives you a scaled 100–1000 score against the 720 pass mark, a
per-domain breakdown, and full explanations for all 60. Questions you have already
been served are de-prioritised, so repeat sittings stay useful. Results feed Weak
Areas, and one click bookmarks everything you missed for practice.


### "10 Things to Know" — the left rail

A collapsible panel beside the questions, opened from the header (or `Esc` to close).
Pick a domain and you get its ten highest-leverage concepts: what the idea is, and a
note on how it actually shows up in a question stem. Plus an **Exam Essentials** set
covering the cross-cutting rules. 60 concepts, written specifically for this exam.

Full details: **[docs/CCAR-F.md](docs/CCAR-F.md)**

### Documentation-check notes

41 questions carry a **"Documentation check"** callout. These mark places where
the community study material diverges from Anthropic's current official docs —
for example `allowed-tools` in `SKILL.md` frontmatter *pre-approves* tools rather
than restricting them (`disallowed-tools` is what restricts). Each note states
what the docs say and what the exam is likely to expect, so you get the mark
without learning the wrong thing.

---

## CCAR-P — Architect, Professional

**1,617 questions · 140 flashcards · 7 domains · 38 blueprint objectives**

The real exam is 63 items in 120 minutes, 720/1000 to pass. Weighted to the
published blueprint (v1.0, effective July 2026):

| Domain | Blueprint | In this bank |
|---|---:|---:|
| Integration | 19% | 17.8% (287) |
| Solution Design & Architecture | 17% | 17.8% (288) |
| Evaluation, Testing & Optimisation | 16% | 15.5% (250) |
| Governance, Safety & Risk Management | 14% | 13.4% (216) |
| Stakeholder Communication & Lifecycle Management | 14% | 13.4% (216) |
| Claude Models, Prompting & Context Engineering | 13% | 13.4% (216) |
| Developer Productivity & Operational Enablement | 7% | 8.8% (143) |

7% to 19% is the flattest weight spread of any Claude certification — there is no
domain you can safely skip.

- 68% workplace scenarios / 32% direct recall, tuned slightly harder than the exam
- Single-answer (1,124), multi-select *Choose TWO/THREE* (327), next-step (166)
- 19% easy / 50% medium / 31% hard · ~25 full 63-item mock papers
- Every stem unique; every item carries why the key is right, **why each individual
  distractor fails**, a concept to lock in, and the exam-craft tip

### "10 Things to Know" — the left rail

A collapsible panel beside every question. Pick a domain and you get its ten
highest-leverage concepts, each with a description and a note on how the idea
actually shows up in a stem — plus an **Exam Essentials** set covering the
cross-cutting rules. 80 concepts in total. It is what makes the bank teach rather
than just test.

**Modes:** Practice (filter by domain, difficulty, type, or set — All / Unseen /
Missed / Bookmarked — plus full-text search) · Flashcards (flip, shuffle, per
domain) · Progress (accuracy by domain, difficulty and type, with your weakest
topics ranked for drilling).

Keyboard: `A`–`E` pick · `Enter` check/advance · `←`/`→` move · `S` bookmark ·
`Space` flip a card.

### Verification

Every one of the 1,618 candidate items was exported with its answer and explanation
stripped and answered cold by independent verifiers, then diffed against a key held
in a file they never read.

**100% coverage. 99.9% agreement (1,616/1,618). Zero disagreements on any of the
327 multi-select items** — over-keying is the defect banks of this size fail on most.

The two genuinely ambiguous items were withheld with written reasons. A separate
audit caught an answer-length tell affecting 85% of the bank (a candidate could have
scored 85% by always picking the longest option); it was repaired to 26% against a
25% baseline, and the build now reports that measurement on every run.

Full methodology, the defect register and a study sequence: **[docs/CCAR-P.md](docs/CCAR-P.md)**

---

## CCDV-F — Developer, Foundations

**1,506 questions · 8 domains · 24 sub-skill tags**

The developer track: hands-on implementation rather than architecture strategy.

| # | Domain | Share | Questions |
|---|---|---:|---:|
| D1 | Applications & Integration | 33.1% | 497 |
| D2 | Model Selection & Optimization | 16.8% | 252 |
| D3 | Agents & Workflows | 14.7% | 221 |
| D4 | Prompt & Context Engineering | 11.0% | 165 |
| D5 | Tools & MCP | 10.6% | 163 |
| D6 | Security & Safety | 8.1% | 122 |
| D7 | Claude Code | 3.1% | 47 |
| D8 | Evaluation, Testing & Debugging | 2.6% | 39 |

A third of the bank is API mechanics — request and response shape, streaming,
retries, batch, deployment — so revise by weight rather than by interest.

**Fact-checked against live documentation.** Five verification passes against the
platform docs found and corrected 57 claims that had been written from model recall.
Several surfaces developers know by heart have changed: assistant prefill is rejected
on current models, `temperature`/`top_p`/`top_k` are deprecated in favour of an effort
setting, and structured output is now a first-class request feature. The bank's
authoring spec records the corrected facts, and the study rail agrees with them.

Includes the **"10 Things to Know"** rail — 90 concepts across the eight domains plus
an Exam Essentials set.

---

## Repository layout

```
.
├── Claude Certified Associate - Foundations.html    # Associate bank   — open this
├── Claude Certified Architect - Foundations.html    # Architect (F)    — open this
├── Claude Certified Architect - Professional.html   # Architect (P)    — open this
├── Claude Certified Developer - Foundations.html    # Developer bank   — open this
├── docs/
│   ├── CCAO-F.md      # Associate: methodology & verification
│   ├── CCAR-F.md      # Architect Foundations: methodology & verification
│   └── CCAR-P.md      # Architect Professional: methodology & verification
├── spec/              # Associate: authoring specs
└── build/
    ├── ccarf/         # Architect (F): question sources, exam module, assemble.sh
    ├── ccarp/         # Architect (P): the full pipeline
    │   ├── questions/    # 90 question batches (JSON)
    │   ├── flashcards/   # 7 flashcard files, 20 cards each
    │   ├── review/       # blind batches, verifier answers, defect register
    │   ├── spec/         # blueprint, authoring rules, repair + verify briefs
    │   ├── tenthings.json  # the "10 Things to Know" left-rail content
    │   ├── template.html   # page shell
    │   ├── assemble.py     # validate + bundle
    │   ├── audit.py        # bank-scale defect scan
    │   └── verify.py       # blind export + scoring
    ├── questions/     # Associate: 108 question batches (JSON)
    ├── flashcards/    # Associate: flashcard batches (JSON)
    ├── review/        # Associate: audit + adjudication artefacts
    ├── assemble.py    # Associate: build script
    └── template.html  # Associate: page shell
```

The HTML files are **generated artefacts** and are committed deliberately so the
repo works by download alone.

## Rebuilding

The Architect bank is assembled from the sources in `build/ccarf/`:

```bash
./build/ccarf/assemble.sh
```

This validates JS syntax, checks data integrity (duplicate IDs, malformed items,
missing explanations), rebalances the answer key with a fixed seed, and writes
`Claude Certified Architect - Foundations.html`. Requires Node.js.

The Architect **Professional** bank is assembled from `build/ccarp/`:

```bash
python build/ccarp/assemble.py --rebalance   # validate + bundle
python build/ccarp/audit.py                  # bank-scale defect scan
python build/ccarp/verify.py export 60       # blind batches, key held back
python build/ccarp/verify.py score           # diff verifier answers vs key
```

`assemble.py` rejects any item that fails validation rather than shipping it, and
reports the answer-length tell on every run so it cannot regress unnoticed.

## Provenance and limitations

These banks were generated with Claude Code and reviewed as described in each
bank's docs. A few things worth knowing:

- **Domain weights, scenario pools and exam metadata** come from published exam
  guides and community study material, not from an official Anthropic document.
  If you have access to the official exam guide PDF, reconcile against it.
- **The CCAR-F technical content was verified against Anthropic's official
  documentation** — Claude Code memory, skills, sub-agents, hooks, CLI reference,
  MCP, and the API tool-use, stop-reason and batch-processing pages. Two factual
  errors inherited from third-party material were found and corrected; see the
  Documentation-check notes.
- **The three banks were built independently** with different methodologies and
  different levels of verification. Do not assume the quality claims from one
  apply to another.
- Certification content changes. Check the current official exam guide before
  relying on any specific figure here.

## Licence

No licence is granted for reuse or redistribution. Provided as-is for personal
exam preparation.
