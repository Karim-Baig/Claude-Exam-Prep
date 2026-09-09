# CCAO-F Exam Prep

A self-contained practice bank for the **Claude Certified Associate – Foundations
(CCAO-F)** exam.

## The deliverable

**`Claude Certified Associate - Foundations.html`** — one file. Double-click it. No install, no
server, no network calls. Progress is saved in that browser's local storage.

Because everything is embedded in a single file, it is a few megabytes and takes
a moment to parse on first open. That is expected.

### What's inside

| | |
|---|---|
| Questions | **2,366** across 8 domains, weighted to the published blueprint |
| Style mix | **71% workplace scenarios / 29% direct recall** |
| Item types | Single-answer (1,846), multi-select *Choose TWO/THREE* (434), next-step sequencing (86) |
| Difficulty | **22% easy / 50% medium / 28% hard** — tuned slightly above the real exam |
| Distinct topics | **2,181** |
| Flashcards | **479** concept cards with a one-line memory hook each |
| Practice volume | ~39 full 60-item exams |
| Every answer carries | why the key is right · why **each** distractor fails · a concept refresher · the exam trap being tested |

Verified completeness: every item has a distractor explanation for every wrong
option, a concept refresher, and an exam tip — zero gaps.

### Verification results

| | |
|---|---|
| Blind-verified | **2,471 / 2,471 items (100%)** |
| Agreement with independent verifiers | **98.0%** |
| Items quarantined | 102, each with a written reason |
| Items re-keyed | 3, each with a visible correction notice |
| Correct-key spread | A 25.0% · B 27.4% · C 25.2% · D 22.4% |

Verifiers ran on a stronger model than the authors and never saw the recorded
answer. Disagreements went to a third-opinion adjudicator. Details of the method
are in *Correctness verification* below.

### The three tabs

- **Practice** — filter by domain, topic, difficulty, item type, or status
  (unseen / missed / correct / flagged). Answer, then read all four explanation
  panels. Flag anything you got right by luck.
- **Flashcards** — active recall, one concept per card. Cards marked *Need
  review* collect into a review pile you can drill alone.
- **Progress** — accuracy by domain, by difficulty, and a ranked list of your
  weakest topics once you have three or more attempts in them.

### Keyboard

`1`–`5` select · `Enter` check then advance · `←`/`→` navigate · `F` flag ·
`Space` flip card · `K` know it · `J` need review · `\` sidebar · `?` help

## Suggested study sequence

1. **Flashcards first, one domain at a time.** Cheap way to load the vocabulary
   before you spend questions on it.
2. **Practice that same domain** on Easy + Medium until you clear ~85%.
3. **Switch Status to "Missed"** and re-drill until the filter empties. This is
   the single highest-yield thing in the app.
4. **Filter to Hard across all domains.** This is what separates a pass from a
   comfortable pass.
5. **Check the Progress tab** for weak topics and go back to step 1 for those.
6. **The day before:** run the Flagged filter and the review pile. Nothing new.

Weight your time by blueprint share — Output Evaluation is 21% of the real exam
and Troubleshooting is 10%, so they do not deserve equal hours.

## The real exam

60 items · 120 minutes · scaled 100–1000 · **720 to pass**

| Domain | Weight |
|---|---|
| Output Evaluation and Validation | 21% |
| Workflow Integration and Solution Design | 16% |
| Governance, Risk, and Responsible Use | 15% |
| Prompting and Task Execution | 14% |
| Product and Model Selection | 12% |
| Configuration and Knowledge Management | 12% |
| Troubleshooting and Optimisation | 10% |

This bank adds a **Technical Awareness** domain that is *not* on the official
blueprint. It was requested for client-conversation fluency and to bridge toward
the developer certification. If you are optimising purely for the CCAO-F score,
filter it out.

## Rebuilding

```
python build/assemble.py
```

Reads every `build/questions/*.json` and `build/flashcards/*.json`, validates
each entry, drops anything malformed, de-duplicates, and rewrites the HTML. It
is safe to run at any point — you get a usable file from whatever batches exist.

The validator reports per-batch counts, type and difficulty mix, correct-key
spread, domain distribution, and any content warnings (uneven option lengths,
references to specific model versions, thin explanations).

## Correctness verification

A practice bank that teaches a wrong answer is worse than no bank. Three layers
guard against that, and they catch different things.

**1. Structural validation** — `build/assemble.py`, runs on every build.
Drops items that are malformed, contain leaked authoring commentary, have stub
fields, or whose explanation names a different option letter than the recorded
key. Also repairs mojibake, escapes stray control characters, salvages truncated
files, and lets a later rewrite supersede a stale one.

**2. Mechanical hallucination audit** — `python build/audit.py [--full]`.
Scans for the signatures of invented facts: fabricated context-window sizes,
prices, rate limits, plan quotas, file caps, named model versions, asserted
knowledge-cutoff dates, and Claude benchmark stats. Also finds near-duplicate
options, options that reference each other by letter, multi-select keys the
explanation never addresses, and the same question recorded with two different
answers.

**3. Blind adjudication** — the only layer that tests whether an answer is
actually *right*.

```
python build/blind_export.py 50     # export items with key + explanation stripped
#   ... independent verifier agents answer build/review/blind_NN.json
#   ... writing picks to build/review/answers_NN.json
python build/adjudicate.py          # diff picks against the held-back key
```

The verifier never sees the recorded answer, so it cannot be anchored by it.
Agreement is evidence an item is sound; disagreement means the key is wrong, the
item is ambiguous, or the verifier erred — and only a human read separates those.
`adjudicate.py` writes `build/review/DISAGREEMENTS.md` with the full item, both
answers, and the verifier's reasoning, ready for a verdict. It also reports
disagreement rates by domain, difficulty, type and batch, so systematic trouble
shows up as a cluster rather than as noise.

Verifiers run on a different, stronger model than the authors. Having a model
check its own work shares blind spots.

### Recording verdicts

Adjudicated decisions live in `build/verdicts.json` and are applied at build
time:

- `quarantine` — drop the item. Use when it is ambiguous, has two defensible
  answers, or its explanation argues for a different option than the key
  (re-keying alone would leave a contradictory rationale).
- `rekey` — change the recorded answer. Only safe when the existing explanation
  still reads correctly for the new key.

Every entry carries a reason. The build prints what it applied, so the exclusions
are never silent.

### Layout

```
spec/
  QUESTION_SPEC.md              authoring rules for scenario items
  DOMAIN_BLUEPRINT.md           domain weights + per-batch topic assignments
  RECALL_AND_FLASHCARD_SPEC.md  overrides for recall items and flashcards
build/
  questions/*.json              one file per authoring batch
  flashcards/*.json             one file per flashcard batch
  template.html                 the app: UI, CSS, quiz engine
  assemble.py                   validator + bundler
Claude Certified Associate - Foundations.html       ← the output
```

To add questions, drop another JSON file into `build/questions/` following
`spec/QUESTION_SPEC.md` and re-run the assembler.

### Option rebalancing

```
python build/assemble.py --rebalance
```

Some authoring batches drifted into keying half their items to the same letter —
one reached 68% B, which would teach you "when unsure, pick B". This rotates
option order so the correct text lands on a different letter, remapping
`correct` and the distractor explanations to match. It is content-preserving:
the same text is still the answer.

Two safety rules are built in. Items whose explanation prose names option
letters ("unlike C, this option…") are skipped, because rotating them would
invalidate those references. And the step is **opt-in**, because changing which
letter is correct would desynchronise a blind verification pass running against
the old arrangement — so it runs last, after verification is settled.

Effect: worst-batch skew fell from 68% to 32%, and no item changed which text is
correct.

## Known limitations

**Semantic redundancy.** De-duplication catches identical stems, and a handful of
same-concept-different-wording pairs were caught by verifiers and quarantined.
But some redundancy certainly remains — two items can test the same point with
only ~25% word overlap, which no lexical threshold can find. At this volume that
is closer to spaced repetition than to a defect, but do not read a high item
count as 2,366 fully distinct ideas.

**The `invented …` audit categories are advisory.** They run at a deliberately
low threshold and mostly fire on legitimate prose — a figure is fine when it is a
property of the fictional company ("volume is 15,000 queries per day") and only a
problem when asserted as an Anthropic product limit. Read the context before
acting on a hit.

**Verification artifacts predate the rebalance.** `build/_answer_key.json` and
the `answers_*.json` files record pre-rotation letters. Verification conclusions
still hold, because rotation never changes which text is correct — but re-run
`blind_export.py` before `adjudicate.py` if you verify again, or you will see
false disagreements.

**Four unresolved disagreements** remain where a verifier and the author differ
and no adjudicator ruling was recorded. They are listed in
`build/review/DISAGREEMENTS.md` with both answers and the reasoning, ready for a
verdict.

## Caveats

Practice items are modelled on the published blueprint and on how professional
certification items are typically written — they are not retired exam questions,
and no question here is claimed to appear on the live test. Content deliberately
avoids specific prices, token limits, context-window sizes, and model version
numbers, since those change; items are built on principles that should still hold
in a year. Verify anything version-specific against current Anthropic
documentation before relying on it in front of a client.
