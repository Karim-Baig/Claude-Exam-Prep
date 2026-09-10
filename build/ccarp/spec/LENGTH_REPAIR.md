# Length-tell repair pass — surgical instructions

## What is wrong

A bank-wide audit found that in **85% of single-answer items the correct option is the
longest of the four**. Chance is 25%. The average correct option runs 56 characters
longer than the mean distractor.

This is not cosmetic. A candidate who has learned nothing can score ~85% by always
choosing the longest option. It destroys the bank's value as practice, and it teaches a
habit that will actively mislead on the real exam, where options are length-matched.

The cause is a natural authoring bias: you know why the right answer is right, so you
write it out fully, then dash off three short wrong ones.

## What you are changing

**Only the `text` of option objects.** Nothing else.

For each item, bring the option lengths into the same band so that the correct option is
not identifiable by length. Meet in the middle:

- **Expand thin distractors** by making them *more specifically wrong* — name the
  mechanism, the tool, the metric, or the circumstance the option is appealing to.
- **Trim a bloated key** where it restates the stem or over-explains. The key should
  state the answer, not argue for it — the argument belongs in `explanation.correct`.

Target: every option within roughly ±15% of the item's mean option length. Perfect
parity is not required and would look artificial; what matters is that the key is not
reliably the longest.

## What you must NOT change

- `id`, `domain`, `topic`, `difficulty`, `type`, `stem`
- `correct` — **which option is true does not change, ever**
- the `key` letter on any option
- the *meaning* of any explanation field

If you touch a distractor's text, re-read its note in `explanation.distractors` and make
sure the note still describes the option you now have. Adjust the note's wording only if
the option's specifics changed; never change what the note argues.

## The trap in this task

**An expanded distractor must stay false.** The failure mode is adding a qualifier that
makes a wrong option defensible — "in some cases", "unless the data allows", "where
appropriate". That converts a clean item into an ambiguous one, which is worse than the
length tell you were sent to fix.

Add substance in the form of **more specific wrongness**:

- Weak: *"Increase the chunk size."*
- Wrong way to expand: *"Increase the chunk size, which may help in some retrieval
  scenarios."* ← now arguably true, item is broken
- Right way to expand: *"Increase the chunk size to 4,000 tokens so each retrieved
  passage carries the full contract clause and its preamble."* ← concrete, still wrong
  here, and now it teaches something when the candidate reads why it fails

Good distractors name a real thing a real practitioner would really do. That is what
makes them the same length as the key without becoming true.

## Also fix, if you see it while you are in there

- **The inverse tell** — the key being reliably the *shortest*.
- **Absolute-language tells** — every distractor saying "always"/"never" while the key
  hedges. Redistribute so absolutes are not a marker of wrongness.
- **Near-duplicate options** — two options a reasonable grader would mark the same.
  Differentiate them or make one clearly distinct.

## Process

Work one file at a time. Read it, rewrite the option texts, write it back with the same
filename. One `Write` per message — a 32K output cap will truncate a larger message and
destroy the file.

Before writing each file back, verify:

1. Same number of items, same ids, same order.
2. Every `correct` array is byte-identical to what it was.
3. Every option still has its original `key` letter.
4. `explanation.distractors` still has exactly one entry per non-key option.
5. No distractor became true. Re-read each one against the stem and ask: *could a
   competent architect now defend this?* If yes, you broke it — make it wrong again.
6. Recount: how many items in this file have the key as the longest option? It should
   be near one in four, not three in four.
