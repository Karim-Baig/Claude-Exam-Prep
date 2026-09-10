# "10 Things to Know" — authoring spec

A left rail that sits beside the questions. Pick a domain, get its ten
highest-leverage concepts. Each one has a title, a description, and a note saying how
the idea actually shows up in an exam question.

This already exists for the CCAR-P bank. **Read `build/ccarp/tenthings.json` before
writing anything** — it is the worked exemplar and the quality bar. You are producing
the same artefact for a different exam.

---

## Schema

A single JSON object. Keys are section names; values are arrays of exactly ten objects.

```json
{
  "Exam Essentials": [
    { "title": "…", "desc": "…", "note": "…" },
    …ten total…
  ],
  "<exact domain string>": [ …ten… ],
  …
}
```

- **`title`** — 3–8 words. The name of the idea, not a sentence. "Context rot", not
  "You should be careful about long contexts".
- **`desc`** — 2–4 sentences, roughly 35–70 words. What the thing *is*, stated so
  someone who has never met the term can use it afterwards. Teach the distinction, not
  the category.
- **`note`** — 1–2 sentences, roughly 20–45 words. **The most valuable field.** How this
  shows up in a question: the phrase in a stem that signals it, the trap it defends
  against, the option shape that is always wrong. Make it specific enough to act on.

Order the ten from most foundational to most specialised. The first three should be the
ones you would tell someone who had one minute.

## The `Exam Essentials` section

Always the first key. Ten cross-cutting things: the exam's own shape (items, minutes,
pass mark, weighting), plus the reasoning habits that pay off across every domain. Look
at CCAR-P's Exam Essentials for the register — it mixes hard exam facts with judgement
rules like "find the binding constraint before reading the options".

## Quality bar

**Write for someone sitting the exam next week, not for a glossary.**

Good:
> **title:** "Hybrid search plus reranking"
> **desc:** "Dense vector search captures meaning but misses exact tokens — part
> numbers, error codes, statute references. Sparse/BM25 keyword search catches those and
> misses paraphrase. Hybrid runs both and fuses; a reranker then re-scores the shortlist
> with a model that reads query and passage together."
> **note:** "The classic stem: semantic search fails on identifiers. The answer is
> hybrid retrieval, not a better embedding model."

Bad — a definition with no teeth:
> **title:** "Retrieval"
> **desc:** "Retrieval means finding relevant documents to give the model."
> **note:** "Important for RAG questions."

## Hard rules

1. **No invented product facts.** No prices, rate limits, cache TTLs, file-size caps,
   benchmark scores, knowledge-cutoff dates, or dated model version strings. Haiku /
   Sonnet / Opus as capability tiers is safe. The 200K context figure is safe. If you
   are not certain a specific number is right, describe the mechanism instead.
2. **Exact section keys.** The domain strings are given to you verbatim. They are used
   to match the bank's own filter values — a typo silently produces an empty panel.
3. **Ten per section. Not nine, not eleven.**
4. **No overlap inside a section.** Ten angles on one idea is a failure. Cover the
   domain's spread; use the bank's own sub-topics as your coverage map.
5. **No cross-section duplication.** If a concept genuinely spans two domains, put it
   where it is most tested and give the other section a different angle on it.
6. **Markdown is limited to `**bold**` and `` `code` ``.** No headings, no lists, no
   links. Newlines are rendered as line breaks.
7. **Never write authoring commentary into a field** — no "TODO", no "note to self".

## What to base the content on

You are writing for a bank that already exists. Ground the concepts in what that bank
actually tests:

- The domain list and weights you are given.
- The bank's own sub-topic or task labels, if provided — those are the real coverage map.
- If you need to check what a domain covers, you may read the exam's question sources,
  but do **not** paste question text into a concept. The rail teaches the idea; the
  questions test it.

## Output

One JSON file, written with a single `Write` call. If the content will exceed the
output cap, write the file in two calls: first the earlier sections, then re-write the
whole file with the remaining sections appended. Never leave the file half-written —
it must always be parseable JSON.
