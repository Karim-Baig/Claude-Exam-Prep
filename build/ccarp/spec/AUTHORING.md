# CCAR-P authoring spec — read this completely before writing a single item

This spec exists because a previous bank of this size was built without one. Every rule
below is here because breaking it produced a defect that had to be found and fixed later.
Treat it as binding, not advisory.

---

## 1. Output mechanics — the hard cap

You have a **32,000 token output ceiling per message**. A CCAR-P item with a scenario
stem and a four-part explanation runs 450–700 tokens. Twenty of them is comfortably
inside the cap; forty is not.

**Write exactly 4 files, 18 items each, one `Write` call per message.**

```
build/ccarp/questions/<BATCH>-p1.json    18 items
build/ccarp/questions/<BATCH>-p2.json    18 items
build/ccarp/questions/<BATCH>-p3.json    18 items
build/ccarp/questions/<BATCH>-p4.json    18 items
```

If you try to emit all 72 in one call the message is truncated mid-JSON, the file is
unparseable, and the entire batch is lost. This has happened. Do not test it.

Number ids continuously across the four files: `p1` holds 001–018, `p2` holds 019–036,
`p3` holds 037–054, `p4` holds 055–072.

Each file is a **bare JSON array**. No wrapper object, no markdown fence, no prose
before or after. UTF-8, no BOM.

---

## 2. Schema

```json
{
  "id": "INT-A-001",
  "domain": "Integration",
  "topic": "Chunk size trade-off in a long-document RAG index",
  "difficulty": "medium",
  "type": "single",
  "stem": "…",
  "options": [
    { "key": "A", "text": "…" },
    { "key": "B", "text": "…" },
    { "key": "C", "text": "…" },
    { "key": "D", "text": "…" }
  ],
  "correct": ["B"],
  "explanation": {
    "correct": "…",
    "distractors": { "A": "…", "C": "…", "D": "…" },
    "concept": "…",
    "tip": "…"
  }
}
```

Field rules, all enforced by the build:

- `id` — `<BATCH>-<NNN>`, zero-padded to 3. Unique across the whole bank.
- `domain` — one of the seven exact strings in BLUEPRINT.md. Copy-paste them.
- `topic` — 4–12 words naming the *specific* thing tested. Not the domain name again.
  Every topic in your batch must be distinct.
- `difficulty` — `easy` | `medium` | `hard`. Target **20 / 50 / 30** across your 72.
- `type` — `single` | `multi` | `next-step`. Target **70 / 20 / 10** across your 72.
- `options` — exactly 4 for `single` and `next-step`; **5 for `multi`**.
- `correct` — array of option keys. 1 for `single`/`next-step`, 2 or 3 for `multi`.
- `explanation.distractors` — **one entry per non-correct option**, keyed by letter.
  A missing entry fails the item. An entry for a correct option fails the item.

---

## 3. What a Professional-tier question sounds like

This is the difference between a CCAR-P item and a Foundations item, and it is the
thing most likely to go wrong.

Foundations asks *"which pattern is this?"* Professional asks *"you own this in
production and something is wrong / something must be decided — what do you do?"*

**Reject any stem that could be answered by someone who has read the docs but never
shipped anything.**

Good Professional stems carry:

- A **concrete production context** — scale, volume, latency budget, cost ceiling,
  regulatory setting, team constraint, existing system that cannot be replaced.
- A **real tension** — two defensible things pulling apart. Cost vs accuracy. Speed of
  delivery vs maintainability. Autonomy vs auditability. What the stakeholder asked for
  vs what the problem needs.
- A **decision that carries consequence** — the wrong choice costs money, breaks a
  regulator commitment, or wakes someone at 3am.

Sample stem opening that is right for this exam:

> A retail bank runs a Claude-based adverse-media screening step inside its onboarding
> flow. It processes 40,000 checks a day against a 200ms p95 budget for the whole
> onboarding call, and the compliance team must be able to reproduce any decision made
> in the last seven years. The team currently sends the full retrieved article set into
> a single Opus call…

Sample stem opening that is **wrong** for this exam (this is Foundations):

> Which of the following best describes the orchestrator-workers pattern?

### The 70/30 split

**70% scenario** — a named situation with an organisation, constraints, and a decision.
**30% recall** — direct knowledge, no scenario, 10–30 words. Recall items are still
Professional-tier: they test the kind of fact an architect needs at decision time, not
trivia. "What is the default TTL of a prompt cache breakpoint" is fine. "Who founded
Anthropic" is not.

### Difficulty calibration

- `easy` — one concept, clean application, an architect gets it in 15 seconds.
- `medium` — two concepts interact, or a plausible wrong answer requires eliminating.
- `hard` — three-way trade-off, or the obvious answer is a trap, or requires noticing
  something the stem states but does not emphasise.

Tune **slightly harder than the real exam**. A candidate who scores 85% here should walk
into the real thing comfortable.

---

## 4. The correct-answer rule — this is the one that broke the last bank

**Never decide which letter is correct before you write the options.**

The failure mode: an author decides "this batch needs more Cs", writes option C first
intending it to be right, then bends the other three to be wrong. The result is either
an item where the explanation argues for a different letter than the key, or an item
where the "wrong" options are obviously filler.

The correct process:

1. Write the stem and settle what the *right answer actually is*, in prose, for yourself.
2. Write the option that expresses it.
3. Write three (or four) genuinely wrong options — each wrong for a **different, real
   reason** that a competent architect might actually believe.
4. Order them however reads most naturally.
5. Record whichever letter the right one landed on.

If your batch comes out 40% keyed B, **do not fix it by changing which option is true.**
Fix it by reordering option *text* on some items so the same true statement sits at a
different letter. The build has a rebalancer that does this safely; you do not need to.

---

## 5. Multi-select — the highest-defect item type

Multi-select items fail verification at roughly **four times** the rate of single-answer
items, and the cause is almost always the same: the author wrote three or four options
that are all genuinely true, then keyed only two of them.

Before you finalise any `multi` item, run this test explicitly:

> Go through all five options one at a time. For each, ask: *is this statement true
> **and** responsive to what the stem actually asked?* Count the yeses.
>
> **The count must exactly equal the number of keys.** Not "the two best". Exactly equal.

If you count three yeses for a two-key item, you do not have a hard question — you have
a broken one. Fix it by making the surplus option **false**, or by narrowing the stem so
the surplus option becomes non-responsive. Do not fix it by arguing one is "more"
correct.

Say the count in the stem: *"(Choose TWO.)"* or *"(Choose THREE.)"*

---

## 6. Never invent facts

You do not have the Claude documentation in front of you. Anything you state as a
specific published figure will be checked, and inventions get the item deleted.

**Do not state:**

- Specific rate limits, RPM/TPM numbers, or quota figures
- Specific prices, per-token costs, or plan tiers
- Specific file size caps, upload limits, or page counts
- Context window or output token numbers as precise claims *unless* they are the
  well-established 200K context figure
- Knowledge cutoff dates for any model
- Benchmark scores, MMLU/SWE-bench percentages, or "X% better than Y"
- Named model versions with dates you are not certain of

**Instead, write the architecture around the constraint:**

- ✅ "the account's published rate limit" / "the tier's token-per-minute ceiling"
- ✅ "a document that exceeds the context window"
- ✅ "the cheaper tier" / "the higher-capability tier"
- ✅ "Haiku", "Sonnet", "Opus" as capability tiers — these are safe
- ❌ "the 400 requests-per-minute limit"
- ❌ "at $3 per million input tokens"

Where a scenario needs a number, **make it a property of the fictional organisation**,
not of Anthropic: *"the team's internal SLO is 800ms p95"* is fine and useful. *"the API
times out at 600 seconds"* is an invented product fact.

Relatedly: if a stem contains arithmetic — a cost calculation, a latency budget, a
throughput figure — **do the arithmetic**. Items have shipped where the premise did not
compute. Every number in the stem must be consistent with every other number.

---

## 7. Option-writing rules

- **Never reference another option by letter.** No "Both A and C", no "A, but only if…",
  no "None of the above". Options are reordered by the build; letter references break.
- **No near-duplicates.** If two options would be marked the same by a reasonable
  grader, the item is unanswerable. Two options that differ only by a hedge word are
  near-duplicates.
- **Match length and specificity.** The correct answer must not be systematically the
  longest or the most qualified. Test-wise candidates read length as a tell.
- **Wrong options must be wrong for a reason worth teaching.** The best distractors are
  things practitioners genuinely do: the industry-default answer that does not fit this
  context, the technically-correct-but-solves-a-different-problem answer, the answer
  that was right two years ago, the over-engineered answer.
- **No absolute-language tells.** Do not make every wrong option contain "always" or
  "never" while the right one hedges.

---

## 8. Explanations — all four parts, every item

**`correct`** (60–120 words). Why the key is right, argued from the specifics of *this*
stem. Name the constraint in the scenario that forces this answer. Do not restate the
option text. Do not open with "Option B is correct because" — the reader can see which
option is correct.

**`distractors`** (30–70 words each, one per wrong option). Why this specific option
fails *here*. The most valuable distractor notes explain what the option **would** be
right for — that is where the concept gets taught. "This is the right move when the
bottleneck is retrieval quality; here the stem tells you retrieval precision is already
at 0.9 and the failure is in synthesis."

**`concept`** (40–90 words). The transferable principle, stated so it applies beyond
this item. This is the sentence the candidate should remember in the exam room. Write it
as a rule, not as a summary of the question.

**`tip`** (20–50 words). The exam-craft observation. What made this hard, what the trap
was, how to recognise the pattern under time pressure. "When a stem gives you a
reproducibility requirement measured in years, it is telling you the answer involves
logging the inputs, not just the outputs."

### Explanation hazards

- **Never name a letter other than the key as correct** inside `explanation.correct`.
  The build scans for this and rejects the item.
- **Never write your own reasoning process into the JSON.** Real examples pulled from a
  previous build: `"Wait — I need C to be correct here"`, `"(TODO: check this)"`,
  `"Actually, let me reconsider"`. Anything like this is a hard delete of the item.
  Think before you write the field; do not think *in* the field.
- **Never leave a stub.** `"TBD"`, `"…"`, an empty string, or a one-word explanation
  fails the item.
- Use markdown sparingly — `**bold**` and backticks are rendered; headings are not.

---

## 9. Internal consistency across the bank

You are writing one batch of twenty-two. Other batches are writing simultaneously.

- Stay strictly inside your batch's scope in BLUEPRINT.md.
- Do not assert a contested rule as settled fact. If a behaviour depends on
  configuration or version, write the item so the answer does not hinge on the
  contested part.
- Every `topic` string in your batch must be distinct, and every stem must be
  substantively different — not the same scenario with the industry swapped.
- Vary the setting. Financial services, healthcare, retail, logistics, public sector,
  telco, energy, legal, manufacturing, media. Vary org size. Vary the role of the person
  in the scenario. Twenty-two batches all set at "a large bank" would be tedious.

---

## 10. Before you write each file — the self-check

For every item, in order:

1. Could this be answered by someone who has never run a Claude system in production?
   → If yes, it is a Foundations item. Rewrite it.
2. Is every number in the stem consistent with every other number?
3. For `multi`: did I count the true-and-responsive options, and does the count equal
   the number of keys exactly?
4. Does any option reference another by letter?
5. Are any two options gradeable as the same answer?
6. Does `explanation.correct` name any letter other than the key?
7. Is there an entry in `distractors` for every non-key option, and none for the key?
8. Did I state any specific Anthropic figure I am not certain of?
9. Are all four explanation parts filled with real content?
10. Is the stem's `topic` distinct from every other topic in this batch?

Then write the file.
