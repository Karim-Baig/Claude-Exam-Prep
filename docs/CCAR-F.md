# CCAR-F — Claude Certified Architect, Foundations

Methodology, coverage and verification record for
[`CCAR-F_Architect_Question_Bank.html`](../CCAR-F_Architect_Question_Bank.html).

**1,501 questions · 130 flashcards · 2.1 MB · single file, no dependencies**

---

## Exam this targets

| | |
|---|---|
| Questions | 60, single-answer multiple choice |
| Time | 120 minutes |
| Scoring | Scaled 100–1000, **720 to pass** |
| Delivery | Pearson VUE |
| Cost | USD 125 |
| Validity | 12 months |
| Guessing penalty | None — answer every question |

Roughly 4 scenarios are drawn from a pool of 8, so you cannot predict which
appear. The bank covers all 8.

> These figures come from published exam-guide summaries and community study
> material, not from an official Anthropic PDF. Reconcile against the official
> guide before relying on them.

## Domain coverage

| # | Domain | Target | Actual | Questions |
|---|---|---:|---:|---:|
| 1 | Agent Architecture & Orchestration | 27% | 28.2% | 424 |
| 2 | Tool Design & MCP Integration | 18% | 17.4% | 261 |
| 3 | Claude Code Configuration & Workflows | 20% | 18.7% | 281 |
| 4 | Prompt Engineering & Structured Output | 20% | 18.9% | 283 |
| 5 | Context Management & Reliability | 15% | 16.8% | 252 |

All **30 task statements** (1.1–1.7, 2.1–2.5, 3.1–3.6, 4.1–4.6, 5.1–5.6) are
represented, none with fewer than 30 questions.

## Scenario coverage

All 8 scenarios in the pool, plus general recall items:

| Code | Scenario |
|---|---|
| CSA | Customer Support Agent |
| CGC | Code Generation & Review |
| MAR | Multi-Agent Research |
| DPT | Data Pipeline & Transformation |
| CCI | Content Creation & Iteration |
| SDE | Software Development Environment |
| CAP | Conversational AI Patterns |
| AAT | Agentic AI Tools |
| GEN | General / direct recall |

CAP and AAT are frequently missing from other study material. They are fully
covered here.

## Question design

- **70% scenario / 30% recall**, matching the requested exam mix.
- Difficulty tuned slightly **above** the real exam, so the real thing feels
  easier than practice.
- Four options each. Distractors are plausible design choices that fail for a
  specific, stated reason — not filler.
- **Per-option rationale**: every one of the four options gets its own
  explanation of why it is right or wrong.
- **Detailed explanation** averaging 406 characters.
- **"Concept to lock in"** — a one-line takeaway that generalises beyond the item.

### Answer-key balance

Questions are authored correct-answer-first, then redistributed at build time by
a seeded shuffle (`mulberry32`, seed `20260908`):

```
A = 376   B = 375   C = 375   D = 375
```

There is no positional tell to learn, and rebuilds are deterministic.

## Study modes

| Mode | What it does |
|---|---|
| **Practice** | Filter by domain, task statement, scenario, difficulty, or set. Instant feedback with full rationale. |
| **Exam Simulator** | Timed 60-question mock under real conditions. See below. |
| **Weak Areas** | Accuracy per task statement, worst first. One click drills that task. |
| **Flashcards** | 130 concept cards on Leitner spaced repetition (1/3/7/21-day intervals). |
| **Search** | Full-text across every stem, option, explanation and card. |
| **Blueprint** | The domain/task/scenario reference, in-app. |

Bookmarks, per-question history, streaks and theme persist in browser local
storage. Nothing leaves your machine.

**Keyboard:** `A`–`D` answer · `→` next · `S` bookmark · `F` flag (exam only).

### Exam Simulator

Reproduces the real sitting: **60 questions, 120 minutes, no feedback until you
submit**, scored 100–1000 against the 720 pass mark.

The paper is seated to the blueprint by largest remainder, so it always totals
exactly 60:

| Domain | Weight | Seats |
|---|---:|---:|
| D1 Agent Architecture & Orchestration | 27% | 16 |
| D2 Tool Design & MCP Integration | 18% | 11 |
| D3 Claude Code Configuration & Workflows | 20% | 12 |
| D4 Prompt Engineering & Structured Output | 20% | 12 |
| D5 Context Management & Reliability | 15% | 9 |

Each sitting also draws **4 scenarios from the pool of 8**, matching the real
exam, and prefers questions you have not been served before so repeat attempts
stay useful.

During the exam you can flag questions, move freely via the question navigator,
and clear an answer. The clock runs on wall time and the paper is persisted, so
reloading the page restores your sitting rather than resetting it; running out of
time auto-submits.

Afterwards you get the scaled score against the pass line, a per-domain
breakdown, the scenarios that were drawn, and full explanations for all 60
questions. Results feed Weak Areas, past attempts are kept in a history, and one
click bookmarks everything you missed for targeted practice.

At 60 questions, **42 correct (70%) is the pass mark** — 42/60 scores 730, 41/60
scores 715.

`assemble.sh` fails the build if the domain weights do not total 100%, if the
seats do not resolve to exactly 60, or if any domain has fewer questions in the
bank than the exam needs to seat.

## Verification

Technical content was checked against Anthropic's official documentation:
Claude Code memory (CLAUDE.md), skills, sub-agents, hooks reference, CLI
reference, settings, MCP, and the API pages for tool use, stop reasons and
batch processing.

**Two factual errors** inherited from third-party study material were found and
corrected:

1. **`allowed-tools` in `SKILL.md` frontmatter.** The community guide describes
   it as *restricting* which tools a skill may call. The official docs say it
   **pre-approves** tools for that turn only and does **not** restrict
   availability — all tools remain callable. `disallowed-tools` is the field that
   restricts. Two questions had the wrong correct answer and were fixed; one
   flashcard was rewritten; 20 further occurrences were annotated.

2. **`PostToolUse` hooks.** Described in third-party material as able to
   normalise, trim or redact tool results. The official hooks reference is clear
   that `PostToolUse` fires *after* execution and cannot rewrite results;
   `updatedInput` is documented only for `PreToolUse` and `PermissionRequest`.
   One flashcard was rewritten and all 35 occurrences annotated.

Also corrected: the `Task` tool is now the **`Agent`** tool (renamed after
v2.1.62), and a "4–7 tools" guideline was aligned to the blueprint's "4–5".

### Documentation-check notes

41 questions carry a blue **"Documentation check"** callout. These appear where
the exam blueprint and the current official docs diverge. Each states what the
docs actually say and what the exam is likely to expect — so you can answer the
exam question correctly without internalising the wrong model.

### Automated checks

`build/ccarf/assemble.sh` fails the build on any of:

- duplicate question IDs
- an item without exactly 4 options
- a correct-answer index that is not 0 pre-shuffle
- a missing explanation, per-option rationale, or concept anchor
- an invalid task statement, scenario code, or difficulty
- a JavaScript syntax error in the assembled bundle

## Rebuilding

```bash
./build/ccarf/assemble.sh
```

Requires Node.js. Sources live in `build/ccarf/`:

| File | Contents |
|---|---|
| `part1_head.html` | Markup and CSS |
| `part2_meta.js` | Blueprint metadata (domains, tasks, scenarios) |
| `qb_head.js`, `qb_b01…b36.js` | 1,501 questions in 36 batches |
| `cards_head.js`, `cards_b01…b02.js` | 130 flashcards |
| `part5_app.js` | Application engine |
| `part6_exam.js` | Exam simulator (paper generation, timer, scoring) |
| `part9_tail.html` | Closing markup |
| `shuffle.js` | Seeded answer-key rebalance + doc-note injection |
| `assemble.sh` | Validate, shuffle, concatenate |

Question format:

```js
{i:1, d:1, t:"1.1", s:"CSA", diff:2,
 q:"scenario stem…",
 ask:"Which approach is most effective?",
 a:["correct option","distractor","distractor","distractor"],
 c:0,
 w:["Correct. …","Wrong because…","Wrong because…","Wrong because…"],
 e:"detailed explanation…",
 n:"optional documentation-check note",
 k:"concept to lock in"}
```

## Suggested study sequence

1. **Read the Blueprint tab first.** Knowing the 5 domains and 30 task
   statements makes the questions legible.
2. **One domain at a time**, heaviest first: D1 (27%) → D3/D4 (20%) → D2 (18%)
   → D5 (15%).
3. **Check Weak Areas after every ~100 questions** and drill the worst two task
   statements.
4. **Run flashcards daily.** Spaced repetition needs elapsed days to work.
5. **In the last week**, drill mixed sets across all domains rather than
   studying by domain — that is how the exam presents them.
6. **Read the Documentation-check notes deliberately.** They are the places most
   likely to trip up someone who has only read community material.

## Limitations

- Original practice questions, not real exam content.
- Exam metadata and domain weights are from third-party sources.
- Certification content changes; check the current official exam guide.
