# Batch Output Rules — READ THIS BEFORE WRITING ANYTHING

**This file overrides the item-count and file-layout rules in
`QUESTION_SPEC.md` and `RECALL_AND_FLASHCARD_SPEC.md`. Everything else in those
files still applies in full.**

## Why this exists

A single response is capped at **32,000 output tokens**. One of our items costs
roughly 850–900 tokens once its four-part explanation is written. Attempting to
emit 75 items in one `Write` call exceeds the cap, the response is truncated, and
**the entire batch is lost**. This already happened once.

So: never put more than **20 items in one `Write` call.**

## Question batches (`OEV-*`, `WIS-*`, `GRR-*`, `PTE-*`, `PMS-*`, `CKM-*`, `TOP-*`, `TAW-*`, `RCL-*`)

Write **80 items as FOUR separate files of exactly 20 items each.**

| File | Items | IDs |
|---|---|---|
| `build/questions/<BATCH>-p1.json` | 20 | `<BATCH>-001` … `<BATCH>-020` |
| `build/questions/<BATCH>-p2.json` | 20 | `<BATCH>-021` … `<BATCH>-040` |
| `build/questions/<BATCH>-p3.json` | 20 | `<BATCH>-041` … `<BATCH>-060` |
| `build/questions/<BATCH>-p4.json` | 20 | `<BATCH>-061` … `<BATCH>-080` |

Four separate `Write` calls, one per file. Each file is a **complete, standalone,
valid JSON array** — do not split a JSON array across files.

Work sequentially: write p1, then p2, then p3, then p4. If you run out of room,
a batch with three good files is fine; a batch with one truncated file is not.

### Per-file mix (20 items)

**Scenario batches** — everything except `RCL-*`:

| | Count |
|---|---|
| `single` | 15 |
| `multi` | 4 |
| `nextstep` | 1 |
| `easy` | 5 |
| `medium` | 10 |
| `hard` | 5 |

**Recall batches** — `RCL-*` only:

| | Count |
|---|---|
| `single` | 16 |
| `multi` | 4 |
| `nextstep` | 0 |
| `easy` | 3 |
| `medium` | 10 |
| `hard` | 7 |

Correct-key spread: aim for roughly 5 items keyed to each of A, B, C, D per
file — but read the "Correct-key placement" section of `QUESTION_SPEC.md` before
you act on that. **Never pre-assign a key and then bend the content to fit it.**
Write the item, see where the true answer lands, record that letter. If a file
ends up skewed, fix it by reordering options — never by changing which option is
true. An uneven spread is cosmetic; a wrong key is a bug that teaches the
candidate something false.

## Flashcard batches (`FC-*`)

Write **60 cards as TWO separate files of exactly 30 cards each.**

| File | Cards | IDs |
|---|---|---|
| `build/flashcards/<BATCH>-p1.json` | 30 | `<BATCH>-001` … `<BATCH>-030` |
| `build/flashcards/<BATCH>-p2.json` | 30 | `<BATCH>-031` … `<BATCH>-060` |

Per-file difficulty: 7 easy / 15 medium / 8 hard.

## Anti-truncation discipline

1. **Do not print any item to the conversation before writing it.** Compose
   directly into the `Write` call. Narrating items first doubles the token cost
   and is what kills batches.
2. **No preamble.** Do not explain your plan, restate the spec, or list the
   topics you intend to cover before writing. Read the specs, then write p1.
3. **Keep explanations inside the specified word budgets.** `correct` 60–140
   words, each `distractors` entry 30–70 words, `concept` 90–200 words,
   `examTip` 50–120 words. Going long is what pushed the first attempt over the
   cap.
4. **One `Write` per file.** Do not build a file with a `Write` and then extend
   it with `Edit` — that wastes tokens re-emitting content.
5. **Report only at the very end**, in under 120 words.

## Never leak your own reasoning into the file

The build validator hard-rejects any item containing authoring commentary, and
several items have already been thrown away for this. Real examples pulled from
rejected output:

- `"Wait — I need C to be correct here. But logically for this..."`
- `"Let me reconsider this scenario."`
- `"...exclusion clause. Now D is the correct answer and makes logical sense."`
- `"distractors": {"A": "placeholder", "B": "placeholder"}`

This happens when you start composing an item, notice the key does not fit, and
"think out loud" inside the JSON. **Do not.** If an item is not working, discard
it and write a different one. The file must contain only finished content.

Equally: never write a field as `placeholder`, `TBD`, `TODO`, `N/A`, or `-`
intending to fill it later. There is no later — the file is written once. Every
`distractors` entry, every `concept`, and every `examTip` must be real prose of
the specified length. An item with stub fields is discarded whole, so you lose
the work either way.

If you are running low on room, **write fewer items, fully finished.** Fifteen
complete items are worth more than twenty with stub explanations.

## Continuing to topic coverage

Your batch's four files should together cover the breadth of your assigned topic
scope, not four repetitions of the same few ideas. Before writing each file,
pick a different slice of your assigned topics:

- **p1** — the most central, frequently-tested ideas in your scope
- **p2** — the adjacent-concept discriminations (X vs. Y confusions)
- **p3** — the failure modes and edge cases
- **p4** — cross-cutting judgement calls that combine two ideas from your scope

## Self-check per file, before each Write

- [ ] Exactly 20 items (or 30 cards for `FC-*`).
- [ ] Valid JSON array, parses on first attempt, no trailing comma.
- [ ] IDs are the correct contiguous range for this file number.
- [ ] `domain` byte-identical to your assignment on every item.
- [ ] Mix matches the table above.
- [ ] Every non-correct option has a `distractors` entry.
- [ ] No item duplicates one from an earlier file in this batch.
