# Claude Certification — Exam Prep

Practice question banks for Anthropic's Claude certification exams. Three
separate banks, each a **single self-contained HTML file** — download, double-click,
study. No install, no server, no network calls, no account. Progress is saved in
your browser's local storage.

> **Unofficial.** Not affiliated with, endorsed by, or connected to Anthropic.
> These are original practice questions written against the *published* exam
> blueprints. They are not real exam questions and no exam content was used.

---

## The three banks

| Exam | File | Questions | Flashcards | Docs |
|---|---|---:|---:|---|
| **CCAO-F** — Claude Certified Associate, Foundations | [`CCAO-F_Question_Bank.html`](CCAO-F_Question_Bank.html) | 2,366 | 479 | [details](docs/CCAO-F.md) |
| **CCAR-F** — Claude Certified Architect, Foundations | [`CCAR-F_Architect_Question_Bank.html`](CCAR-F_Architect_Question_Bank.html) | 1,501 | 130 | [details](docs/CCAR-F.md) |
| **CCDV-F** — Claude Certified Developer, Foundations | [`claude-foundations-exam.html`](claude-foundations-exam.html) | 400 | — | — |

**4,267 practice questions** in total.

Each file is a few megabytes because everything is embedded — expect a moment's
pause on first open. That is normal.

---

## Which one do I need?

- **Associate (CCAO-F)** — broadest and most foundational. Start here if you are
  new to Claude or unsure which exam you are sitting.
- **Architect (CCAR-F)** — scenario-heavy, focused on design trade-offs:
  agentic architecture, tool and MCP design, Claude Code configuration, context
  reliability. Assumes you already build with Claude.
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

**Modes:** Practice (filter by domain, task, scenario, or set) · Weak Areas
(accuracy per task statement, with one-click drilling) · Flashcards (Leitner
spaced repetition, 1/3/7/21-day intervals) · Search · Blueprint reference.

Keyboard: `A`–`D` answer · `→` next · `S` bookmark.

Full details: **[docs/CCAR-F.md](docs/CCAR-F.md)**

### Documentation-check notes

41 questions carry a **"Documentation check"** callout. These mark places where
the community study material diverges from Anthropic's current official docs —
for example `allowed-tools` in `SKILL.md` frontmatter *pre-approves* tools rather
than restricting them (`disallowed-tools` is what restricts). Each note states
what the docs say and what the exam is likely to expect, so you get the mark
without learning the wrong thing.

---

## CCDV-F — Developer, Foundations

**400 questions · 8 domains · 31 subject tags**

| # | Domain | Questions |
|---|---|---:|
| D1 | Applications & Integration | 115 |
| D3 | Agents & Workflows | 60 |
| D2 | Model Selection & Optimization | 55 |
| D5 | Tools & Model Context Protocol | 50 |
| D4 | Prompt & Context Engineering | 45 |
| D6 | Security & Safety | 35 |
| D7 | Claude Code | 20 |
| D8 | Evaluation, Testing & Debugging | 20 |

Heaviest subject tags: Tool Implementation (26), Claude API Mechanics (23),
Prompt Engineering (22), Agent Patterns & Frameworks (21), Agent Architecture,
Claude Code Operation and Debugging & Error Handling (20 each).

Smaller and earlier than the other two banks; treat it as a supplement rather
than a complete course.

---

## Repository layout

```
.
├── CCAO-F_Question_Bank.html            # Associate bank  — open this
├── CCAR-F_Architect_Question_Bank.html  # Architect bank  — open this
├── claude-foundations-exam.html         # Developer bank  — open this
├── docs/
│   ├── CCAO-F.md      # Associate: methodology & verification
│   └── CCAR-F.md      # Architect: methodology & verification
├── spec/              # Authoring specs (blueprint, question spec)
└── build/
    ├── ccarf/         # Architect: question sources, shuffle.js, assemble.sh
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
`CCAR-F_Architect_Question_Bank.html`. Requires Node.js.

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
