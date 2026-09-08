# Addendum — Recall Items & Concept Flashcards

Read `QUESTION_SPEC.md` first. This file **overrides** it only where stated.
Everything not mentioned here (JSON validity, four-part explanations, distractor
craft, factual-accuracy limits, correct-key rotation) still applies in full.

---

# PART 1 — RECALL ITEMS (batch prefix `RCL-`)

The bank is being built to a **70% scenario / 30% recall** mix. The scenario
items already exist. Your batch supplies the recall 30%.

## What overrides QUESTION_SPEC.md

| Rule | QUESTION_SPEC says | For `RCL-` batches |
|---|---|---|
| Stem style | Every item is a workplace scenario | **No scenarios.** Direct knowledge questions. |
| Stem length | 40–130 words | **8–35 words.** Tight. |
| Role/industry/artifact | Mandatory in every stem | **Omit entirely.** No personas, no company. |
| Difficulty mix | 18 easy / 39 medium / 18 hard | **12 easy / 38 medium / 25 hard** |
| Type mix | 56 single / 15 multi / 4 nextstep | **60 single / 15 multi / 0 nextstep** |

Item count is still exactly **75**. Explanation structure is still all four
parts. `type` values are still `"single"` and `"multi"` only.

## What a recall item looks like

Recall items test whether the candidate **owns the vocabulary and the canonical
facts** — the layer beneath scenario judgement. They are short, direct, and
unambiguous.

Good:
> Which Claude model tier is intended for high-volume, latency-sensitive tasks
> where per-item reasoning demands are low?

> In the five-part prompt structure, which element specifies the shape the
> output should take rather than what to produce?

> What does it mean for a claim in Claude's output to be *grounded*?

> Which TWO of the following are properties of Project knowledge rather than a
> per-chat file upload? (Choose TWO)

Bad — this is a scenario, which belongs in the other 70%:
> A procurement analyst at a 400-person manufacturer notices that Claude's
> contract summaries cite superseded thresholds…

Bad — trivia with no conceptual payload:
> How many letters are in the acronym PII?

Bad — unanswerable without invented facts:
> What is the maximum file size for a Project knowledge document?

## Making recall items *hard* without making them unfair

Your 25 hard items must not be hard because they are vague. They should be hard
because they demand a **fine discrimination between adjacent concepts**. Reach
for these axes:

- **Definition boundaries.** Grounding vs. accuracy vs. calibration.
  Hallucination vs. staleness vs. omission. Bias vs. variance in output quality.
- **Category membership.** Which of these is a *governance* control rather than
  a *technical* one? Which is a property of retrieval rather than long context?
- **Purpose vs. side effect.** What a feature is *for*, versus something it
  happens to also do.
- **Correct-but-incomplete definitions.** Three options are partially right;
  one is precisely right.
- **Commonly confused pairs.** Few-shot vs. chain-of-thought. Projects vs.
  Styles. Connectors vs. uploads. Tool use vs. MCP. Evals vs. spot-checking.
  Prompt caching vs. batch processing. Custom instructions vs. system prompt.

Rule: if a candidate who genuinely understands the concept could still pick the
wrong option, the item is broken — rewrite it.

## Recall batch assignments

Draw topics from the matching domain section of `DOMAIN_BLUEPRINT.md`, but cover
the **whole domain**, not one sub-batch. You are the single recall batch for
your domain (except OEV, which has two — stay on your assigned half).

| Batch | Domain string (verbatim) | Coverage |
|---|---|---|
| `RCL-OEV-A` | `Output Evaluation and Validation` | Blueprint sections OEV-A + OEV-B |
| `RCL-OEV-B` | `Output Evaluation and Validation` | Blueprint sections OEV-C + OEV-D |
| `RCL-WIS` | `Workflow Integration and Solution Design` | All of WIS-A/B/C |
| `RCL-GRR` | `Governance, Risk, and Responsible Use` | All of GRR-A/B/C |
| `RCL-PTE` | `Prompting and Task Execution` | All of PTE-A/B/C |
| `RCL-PMS` | `Product and Model Selection` | All of PMS-A/B |
| `RCL-CKM` | `Configuration and Knowledge Management` | All of CKM-A/B |
| `RCL-TOP` | `Troubleshooting and Optimisation` | All of TOP-A/B |
| `RCL-TAW` | `Technical Awareness` | All of TAW-A/B/C |

IDs: `<BATCH>-001` … `<BATCH>-075`.
Output: `build/questions/<BATCH>.json`.

---

# PART 2 — CONCEPT FLASHCARDS (batch prefix `FC-`)

A separate deck for **active recall** — the fast, repeatable layer the candidate
drills between question sessions. One card = one idea, stated so precisely that
reading the back twice is enough to own it.

## Schema

Write a single JSON array to `build/flashcards/<BATCH>.json`.

```json
[
  {
    "id": "FC-OEV-001",
    "domain": "Output Evaluation and Validation",
    "topic": "Grounding",
    "difficulty": "medium",
    "front": "What does it mean for a claim in Claude's output to be *grounded*?",
    "back": "The claim traces back to material actually present in the context window — an uploaded file, a Project knowledge document, or a live search result. Anything else was produced from the model's parametric memory and is unverified by default.\n\nGrounding is a statement about **provenance**, not about truth. A grounded claim can still be wrong if the source is wrong; an ungrounded claim can happen to be right. What grounding buys you is that the claim is *checkable*.",
    "hook": "Grounded = traceable to something in the context, not merely correct."
  }
]
```

| Field | Rule |
|---|---|
| `id` | Batch prefix + zero-padded 3-digit counter. Sequential. |
| `domain` | Assigned domain string, verbatim. |
| `topic` | 1–4 words. The concept being carded. |
| `difficulty` | `easy` \| `medium` \| `hard`. Target 15 / 30 / 15 per 60-card batch. |
| `front` | The prompt. 5–25 words. Markdown allowed. |
| `back` | The answer. **50–130 words.** Markdown allowed, `\n\n` for paragraphs. |
| `hook` | One line the candidate can carry into the exam. **≤ 25 words.** No markdown. |

Exactly **60 cards** per batch.

## Writing good fronts

A front must be answerable *from memory* and have one defensible answer.

- Good: "What distinguishes a hallucination from a staleness error?"
- Good: "Name the five building blocks of an effective prompt."
- Good: "When does escalating the model tier *not* fix a quality problem?"
- Good: "Which lever do you reach for first: a bigger model, or a better prompt? Why?"
- Bad: "Tell me about Claude Projects." — unbounded, no single answer.
- Bad: "Is verification important?" — yes/no, no recall value.
- Bad: "What is the context window size?" — invented fact.

Vary the front *form* across your 60 cards: definitions, discriminations
("X vs. Y"), enumerations ("name the three…"), decision rules ("when would you…"),
diagnostics ("what symptom points to…"), and inversions ("what does this *not* do?").
Aim for roughly a quarter of your cards to be explicit **X vs. Y**
discriminations — those are where exam items are won and lost.

## Writing good backs

- Lead with the direct answer in the first sentence. No preamble.
- Then add the one clarification that prevents the common misunderstanding.
- Bold the load-bearing term.
- Where a card covers a discrimination, state both sides symmetrically.
- Do not write "it depends" without saying what it depends on.

## Flashcard batch assignments

| Batch | Domain string (verbatim) | Cards |
|---|---|---|
| `FC-OEV` | `Output Evaluation and Validation` | 60 |
| `FC-WIS` | `Workflow Integration and Solution Design` | 60 |
| `FC-GRR` | `Governance, Risk, and Responsible Use` | 60 |
| `FC-PTE` | `Prompting and Task Execution` | 60 |
| `FC-PMS` | `Product and Model Selection` | 60 |
| `FC-CKM` | `Configuration and Knowledge Management` | 60 |
| `FC-TOP` | `Troubleshooting and Optimisation` | 60 |
| `FC-TAW` | `Technical Awareness` | 60 |

Cover your domain's full blueprint scope. No two cards in a batch may teach the
same point.

---

## Self-check (both parts)

- [ ] Valid JSON, single array, parses on first attempt.
- [ ] Exact item count (75 recall / 60 flashcards).
- [ ] IDs sequential with the assigned prefix, no gaps.
- [ ] `domain` byte-identical to the assignment on every entry.
- [ ] Recall: no scenarios, no personas, stems 8–35 words.
- [ ] Recall: 60 single / 15 multi, and 12 / 38 / 25 difficulty.
- [ ] Recall: correct key spread roughly even across A/B/C/D.
- [ ] Flashcards: every `back` 50–130 words, every `hook` ≤ 25 words.
- [ ] No invented Anthropic pricing, limits, or model version numbers anywhere.
- [ ] Nothing duplicates another entry in your own file.

Report when done: entry count, difficulty counts, (recall: type counts and
correct-key spread), and the topics covered.
