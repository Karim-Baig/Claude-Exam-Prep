# Blind verification brief

You are answering exam questions cold. You have not seen the recorded answer and you
must not go looking for it — the whole value of this pass is that your judgement is
independent. If you find yourself reasoning about "what the author probably intended",
stop and reason about what is actually correct instead.

## What you are given

`build/ccarp/review/blind_NN.json` — a batch of items in this shape:

```json
{ "id": "INT-A-014", "choose": 1,
  "question": "…full stem…",
  "options": { "A": "…", "B": "…", "C": "…", "D": "…" } }
```

`choose` tells you how many options to select. It is the only thing you know about the
key, and it is given because a multi-select is unanswerable without it.

**Do not read** `build/ccarp/questions/`, `build/ccarp/_key.json`, or the built HTML.
Those contain the answers. Reading them invalidates your entire batch.

## What to produce

`build/ccarp/review/answers_NN.json` — a bare JSON array, one entry per item, same order:

```json
[
  { "id": "INT-A-014", "answer": ["B"], "confidence": "high", "note": "" },
  { "id": "INT-A-015", "answer": ["A","D"], "confidence": "low",
    "note": "C is equally defensible: the stem never says the index is rebuilt nightly, so incremental staleness is as good an answer as chunk drift." }
]
```

- `answer` — array of option letters. Length must equal `choose`.
- `confidence` — `high` | `medium` | `low`.
- `note` — required whenever confidence is not `high`, and whenever you spot a defect.
  Empty string otherwise. Be specific and brief.

Write in chunks of at most ~55 answers per `Write` call to stay under the output cap.

## Use `low` confidence honestly

`low` is not an admission of ignorance — it is the most valuable signal in this pass.
Mark `low` when:

- **Two options are both defensible.** Say which, and what in the stem would have to
  change to separate them. This is the single most common real defect.
- **The stem is under-specified** — the answer depends on a fact the stem never states.
- **A multi-select looks over-keyed** — you count more true-and-responsive options than
  `choose` allows. Give the count and name them. This is the highest-frequency defect
  in banks of this size; look for it deliberately on every multi item.
- **Two options mean the same thing** by any reasonable grading.
- **The arithmetic does not work.** Several stems carry cost, latency, throughput or
  sample-size figures. Where a stem contains numbers, actually check them. A premise
  that does not compute has shipped in banks like this before.

A high-confidence answer with an empty note is a perfectly good result and should be
the majority. Do not manufacture doubt.

## Also flag, in the note

- A claim about Anthropic products you believe is **factually wrong** — an invented rate
  limit, price, cap, benchmark figure, cutoff date, or a capability attributed to the
  wrong model tier.
- An option that references another option by letter (they get reordered; this breaks).
- Anything that reads as authoring commentary that leaked into the text.

## What NOT to do

- Do not rewrite items. You are measuring, not fixing.
- Do not skip items. If you truly cannot decide, answer with your best guess, mark
  `low`, and explain in the note.
- Do not let one hard item stall the batch. Budget your time; a whole unreported batch
  is far worse than one shaky answer.

## How this is used

Your answers are diffed against a key you never saw. Where you agree with the author,
that is independent evidence the item is sound. Where you disagree, one of three things
is true — the key is wrong, the item is ambiguous, or you are wrong — and a human reads
the item to decide which. So your `note` on a disagreement is doing real work: it is
what the adjudicator reads first.
