# CCAO-F Question Authoring Spec

You are authoring items for a **Claude Certified Associate – Foundations (CCAO-F)**
practice question bank. Read this whole file before writing a single item.

The user is a senior technology consultant preparing to sit the real exam. Items
that are vague, trivially guessable, or repetitive are worse than useless — they
build false confidence. Hold the bar.

---

## 1. Output format — non-negotiable

Write **one JSON file** containing a single JSON array of question objects.
No wrapper object, no markdown fences, no trailing commas, no comments.
The file must parse with `json.load()` on the first attempt.

```json
[
  {
    "id": "OEV-A-001",
    "domain": "Output Evaluation and Validation",
    "topic": "Fabricated citations",
    "difficulty": "medium",
    "type": "single",
    "stem": "A marketing lead asks Claude to draft a competitor landscape summary. The response is fluent and well-structured, and includes the sentence: \"According to Gartner's 2024 Enterprise AI Adoption Report, 43% of mid-market firms deployed generative AI in production.\" The lead searches Gartner's site and Google and cannot find any report by that name.\n\nWhat is the MOST likely explanation?",
    "options": [
      { "key": "A", "text": "Claude's training data predates the report, so it summarised an earlier edition under the wrong title." },
      { "key": "B", "text": "Claude generated a plausible-sounding citation that does not correspond to a real source." },
      { "key": "C", "text": "The report exists but sits behind Gartner's paywall, so it is not publicly indexed." },
      { "key": "D", "text": "The prompt did not specify a citation format, so Claude invented a placeholder reference." }
    ],
    "correct": ["B"],
    "explanation": {
      "correct": "This is a textbook fabricated citation. When a model is asked for factual content without grounding material in context, it generates text that is statistically plausible rather than retrieved. Specific, verifiable-looking artifacts — a named report, a year, a precise percentage — are the highest-risk category, because their specificity is what makes them convincing. The correct read is that the citation was generated, not sourced, and the claim must be treated as unverified until a real source is found.",
      "distractors": {
        "A": "Stale training data produces outdated facts, not non-existent artifacts. If Claude had summarised a real earlier edition, the lead's search would surface that edition's title. Nothing was found at all, which points to fabrication rather than staleness.",
        "C": "A paywall restricts access to a document's contents, not the existence of its title. Gartner report names, publication years, and abstracts are indexed and discoverable even when the full text is gated. A total absence from search is inconsistent with a paywalled-but-real report.",
        "D": "Claude does not insert deliberate placeholders when a citation format is unspecified. Missing format guidance affects how a citation is styled, not whether the underlying source is real. This option misattributes a grounding failure to a formatting gap."
      },
      "concept": "**Grounding** is the property that a claim traces back to something actually present in the context window — an uploaded file, a Project knowledge document, or a live search result. Anything not grounded is produced from the model's parametric memory and must be independently verified before use.\n\nHighest-risk fabrication markers, in rough order:\n- Named reports or studies paired with a year\n- Precise statistics (43%, $2.1B, 3.7x)\n- Direct quotations attributed to a named person\n- Specific dates, version numbers, case citations, statute references\n\nThe operative principle: **fluency is not evidence of accuracy.** A model's confidence and polish are properties of its language generation, entirely independent of whether the underlying claim is true.",
      "examTip": "This item tests whether you can separate **hallucination** from **staleness** — two failure modes that both yield a wrong fact but have different causes and different fixes. Staleness is fixed by supplying current material; fabrication is fixed by grounding and verification.\n\nExpect Anthropic to build distractors that are *true statements about how Claude works* but *wrong explanations for the scenario in front of you*. Option A is a real phenomenon; it just is not what happened here. Always ask \"does this mechanism actually produce the symptom described?\" rather than \"is this sentence true?\""
    }
  }
]
```

### Field rules

| Field | Rule |
|---|---|
| `id` | Exactly your assigned batch prefix + zero-padded 3-digit counter, e.g. `OEV-A-001` … `OEV-A-075`. Sequential, no gaps. |
| `domain` | Copy your assigned domain string **verbatim**. Any deviation breaks the UI filter. |
| `topic` | 2–5 words naming the specific concept. Used for weak-area analysis. Draw from your assigned topic list. |
| `difficulty` | `"easy"` \| `"medium"` \| `"hard"`. Mix per §4. |
| `type` | `"single"` \| `"multi"` \| `"nextstep"`. Mix per §3. |
| `stem` | The scenario + question. See §2. |
| `options` | Array of 4 (single/nextstep) or 5 (multi) objects with `key` and `text`. Keys are `"A"`, `"B"`, `"C"`, `"D"`, `"E"`. |
| `correct` | Array of correct keys. One element for `single`/`nextstep`; two or three for `multi`. |
| `explanation.correct` | 60–140 words. Why the key is right, and what principle it rests on. |
| `explanation.distractors` | An entry for **every** non-correct key. 30–70 words each. |
| `explanation.concept` | 90–200 words teaching the underlying concept. Markdown allowed. |
| `explanation.examTip` | 50–120 words naming the trap or discrimination being tested. Markdown allowed. |

Markdown supported in `stem`, `concept`, `examTip`, and option text: `**bold**`,
`*italic*`, `` `code` ``, `- bullets`, and `\n\n` for paragraph breaks. The renderer
handles these. Do not use HTML tags or tables.

---

## 2. Writing the stem

**Every item is a scenario.** Not a definition quiz. The real exam presents a
workplace situation and asks for judgement.

Bad — trivia, no judgement required:
> What does PII stand for?

Bad — vague, no anchor:
> What is the best way to use Claude Projects?

Good — concrete role, concrete artifact, concrete tension:
> A compliance analyst maintains a Claude Project for reviewing vendor contracts.
> The Project knowledge contains the 2023 and 2025 versions of the company's
> procurement policy; the 2023 version was never removed. Claude's contract
> reviews have begun citing approval thresholds that the procurement team says
> were superseded two years ago.
>
> What is the FIRST action the analyst should take?

Requirements:

1. **Name a role and a business context.** Compliance analyst, HR business
   partner, bid manager, clinical operations coordinator, RevOps lead, grant
   writer, procurement specialist, internal auditor, L&D manager, actuarial
   analyst. Rotate these — do not write forty questions about "a marketing
   manager".
2. **Include a specific artifact or number** so the scenario feels real: a
   140-page RFP, 3,000 support tickets, a 12-tab workbook, a 40-slide QBR deck.
3. **Create a genuine tension.** Something has gone wrong, or two reasonable
   courses of action compete. If the answer is obvious from the stem alone, the
   item is too easy.
4. **End with a precise question** using a capitalised qualifier where it
   disambiguates: `MOST likely`, `BEST`, `FIRST`, `NEXT`, `PRIMARY`,
   `LEAST appropriate`, `MOST significant risk`.
5. **Length: 40–130 words.** Enough to establish the situation. No padding.
6. Multi-select stems must end with `(Choose TWO)` or `(Choose THREE)`.

### Scenario diversity mandate

Across your 75 items, vary the industry: financial services, healthcare
provider, pharma, insurance, retail, manufacturing, public sector, higher
education, professional services, media, logistics, energy, non-profit,
telecoms, hospitality. Vary the company size: solo consultant, 12-person
startup, 400-person mid-market, 90,000-person global enterprise. Vary the
stakes: internal draft vs. regulator-facing filing.

Repetition is the single most common failure in generated question banks.
Before writing item N, glance at what you wrote for items N-10 to N-1 and
deliberately move away from it.

---

## 3. Item type mix (per 75-item file)

| Type | Count | Shape |
|---|---|---|
| `single` | 56 | 4 options, exactly 1 correct. |
| `multi` | 15 | 5 options, exactly 2 or 3 correct. Stem ends `(Choose TWO)` / `(Choose THREE)`. |
| `nextstep` | 4 | 4 options, 1 correct. Stem describes a partially-completed troubleshooting or design sequence and asks what to do **NEXT** or **FIRST**. All four options are actions that are individually defensible; correctness turns on *ordering* — diagnose before changing, isolate one variable, verify before scaling. |

For `multi` items, write the distractor explanations for the incorrect keys and,
in `explanation.correct`, address why **each** correct key qualifies.

### Multi-select: the over-keying trap

This is the most common defect found in this bank. Blind verification showed
multi-select items disagreeing with their own recorded answer **4× more often**
than single-answer items, and almost always for the same reason: the author
wrote five options where **three or more are genuinely true**, then picked two.

An item that asks for TWO but contains three true statements is broken. There is
no defensible way for a candidate to choose, and any answer key is arbitrary.

So for every `multi` item, apply this test before you move on:

> Count the options that are **true and responsive to the question asked**.
> That count must equal the number you are asking for. Exactly.

If you ask for TWO, then exactly two options are correct and the other three
must be **actually wrong** — not "less important", not "also valid but weaker",
not "true but secondary". Wrong.

Ways to make a multi-select distractor properly wrong:

- It states something factually untrue about Claude or the situation.
- It is true in general but does not answer *this* question (e.g. a real
  governance control when the stem asks specifically about data handling).
- It describes an action that would not achieve the stated goal.
- It confuses an adjacent concept (accountability where capability was asked).

Avoid the ranking-in-disguise item — five sensible practices where the key is
just the two the author liked best. If your stem needs the words "MOST
important" to separate three true options from two others, you have written a
ranking question with no objective answer. Rewrite it so the untrue options are
untrue.

---

## 4. Difficulty mix (per 75-item file)

| Level | Count | Definition |
|---|---|---|
| `easy` | 18 | One clear principle. A prepared candidate answers in under 20 seconds. Distractors are plainly wrong to someone who studied. |
| `medium` | 39 | Requires applying a principle to an unfamiliar situation, or discriminating between two adjacent concepts. Two options survive first inspection. |
| `hard` | 18 | Two options are genuinely defensible and the key wins on a subtle basis: a qualifier in the stem, an ordering constraint, a least-privilege preference, or a detail most candidates overlook. The `examTip` must explicitly name the discriminator. |

---

## 5. Distractor craft

This is what separates a real exam item from filler.

**Every distractor must be attractive to someone who half-knows the material.**

Draw distractors from these patterns:

- **True but irrelevant.** A correct statement about Claude that does not answer
  the question asked.
- **Right action, wrong time.** A step that belongs later in the sequence.
- **Over-engineering.** Escalating to Opus, building a Project, or looping in IT
  when a prompt constraint would have solved it.
- **Under-engineering.** Accepting output without verification; shipping to a
  regulator without review.
- **Adjacent-concept swap.** Research mode where Projects is correct; RAG where
  long context is correct; hallucination where staleness is correct.
- **Plausible-sounding invented feature.** A capability that does not exist but
  sounds like it should. Use sparingly — at most 1 in 10 items.
- **Correct-but-incomplete.** Addresses one of two required conditions.

Forbidden:

- Joke or absurd options. Every option must be something a real professional
  might actually propose.
- `"All of the above"` / `"None of the above"`.
- Options that are grammatically inconsistent with the stem, or where the
  correct one is conspicuously the longest. **Keep option lengths within ~25%
  of each other** — length is the number-one accidental tell.
- Absolute language (`always`, `never`, `only`) in the correct answer unless the
  principle genuinely is absolute.
- Two options that mean the same thing in different words.

### Correct-key placement — read carefully, this has gone wrong before

**Never decide the answer letter before you write the item.** Write the
question, write the four options so that exactly one is genuinely correct, and
then record whichever letter that option happens to occupy.

Agents have destroyed real work by doing the opposite: pre-planning "item 34
will be keyed D", discovering that option B was the defensible answer, and then
either forcing a wrong key or leaving a note about it in the explanation. Both
outcomes are worse than an uneven key spread. **A mis-keyed item actively
teaches the wrong thing** — it is the single most damaging defect possible here.

If you finish a file and one letter has run away with it (say 11 of 20 keyed C),
fix it the safe way: pick a few of those items and **reorder their options**, so
the correct text moves to a different letter. Update `correct` to match the new
position and make sure no option refers to another by letter. Never fix a skew
by changing which option is true.

An uneven spread is a cosmetic blemish. A wrong key is a bug. Prefer the
blemish, every time.

---

## 6. Explanation craft

The user's stated goal: *"clear my concepts so that I can pass with flying
colours."* The explanation is the product; the question is just the hook.

- `explanation.correct` — State the principle, then tie it to the specifics of
  this scenario. Not "B is correct because it is the best practice." Explain the
  *mechanism*.
- `explanation.distractors` — For each wrong key, name the **specific
  misconception** that would lead a candidate to pick it, then dismantle it.
  Never write "this is incorrect because it is not the best option."
- `explanation.concept` — Teach the topic as if the reader has never met it.
  This is where they actually learn. Use a short bulleted structure where it
  helps. Include the rule of thumb they should carry into the exam.
- `explanation.examTip` — Name the trap. What discrimination is being tested?
  What qualifier mattered? What pattern will recur on other items?

Do not repeat the same `concept` text across items. If two items share a
concept, teach a different facet of it — a different edge case, a different
rule of thumb, a different failure mode.

---

## 7. Factual accuracy — read this twice

The bank is worthless if it teaches wrong facts. Constraints:

- **Model tiers.** Claude Haiku = fastest and cheapest, for high-volume simple
  work. Claude Sonnet = balanced default for most professional work. Claude Opus
  = deepest reasoning, highest cost and latency, for genuinely hard analysis.
  Reason about tiers by their *characteristics*, not by version numbers.
- **Do not invent** specific prices, token limits, file-size caps, message
  quotas, context-window figures, or SKU names. If an item needs a number, make
  it a property of the fictional company ("their policy caps uploads at 20MB"),
  never a claimed Anthropic product limit.
- **Do not name a specific model version** (no "Claude 3.5 Sonnet", no
  "claude-opus-4"). Write "Sonnet", "Opus", "Haiku", "the mid-tier model".
- Prefer **timeless capability statements** over anything release-dependent. If
  a fact might have changed in the last six months, build the item on the
  underlying principle instead.
- Governance items should turn on **generally-applicable practice** — data
  minimisation, least privilege, human review for high-stakes decisions,
  auditability — not on a specific clause of a specific contract or regulation.
  You may reference GDPR/HIPAA/SOX at a conceptual level, not by article number.

When in doubt, build the item on a principle that will still be true in two
years.

---

## 8. Self-check before you finish

Run this list against your file. Fix violations before writing.

- [ ] Valid JSON, single array, parses cleanly.
- [ ] Exactly 75 objects.
- [ ] IDs sequential with the assigned prefix, no gaps or duplicates.
- [ ] `domain` string is byte-identical to the assignment on every item.
- [ ] Type mix: 56 single / 15 multi / 4 nextstep.
- [ ] Difficulty mix: 18 easy / 39 medium / 18 hard.
- [ ] Correct-key distribution roughly even across A/B/C/D.
- [ ] Every `multi` stem ends with `(Choose TWO)` or `(Choose THREE)` and
      `correct` has matching length.
- [ ] Every non-correct option has a `distractors` entry.
- [ ] No two items in the file test the same point with the same scenario.
- [ ] No invented Anthropic pricing, limits, or version numbers.
- [ ] Option lengths within a comparable range; correct answer is not
      systematically longest.
- [ ] Roles and industries genuinely varied across all 75.

Write the file to the exact path given in your assignment. Then report: item
count, type counts, difficulty counts, correct-key distribution, and the list of
topics you covered.
