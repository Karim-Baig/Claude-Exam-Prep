# CCAR-P defect register — from blind verification

Compiled from the independent verifier reports. Blind verification put 1,618 items in
front of verifiers who never saw the key; agreement with the recorded answer ran
**99.8%**. So the *keys* are sound. Almost everything below is a flaw in the surrounding
prose — a wrong number inside a distractor, a stem that overstates, an option that is
closer to defensible than intended.

Ordered by how much harm it does to a candidate.

---

## Tier 1 — teaches something false. Fix these.

These put an incorrect claim in front of a candidate who will believe it.

| id | defect |
|---|---|
| `INT-C-033` | An option proposes enabling caching on a ~250-token instruction block. Verifier reports that is below the minimum cacheable prefix, so the breakpoint would be ignored entirely — the option is not merely low-value, it is inoperable. Either raise the block size in the stem or re-point the option. |
| `INT-C-049` | An option invokes a "caller-supplied identifier" for the **batch job**. Per the verifier, the caller-supplied id is per-request; the batch id is server-assigned. The action is still the right one, but as written it teaches a capability that does not exist. |
| `INT-D-071` | The stem sends 40–80 MB manuscript bodies to a model gateway — roughly two orders of magnitude beyond any context window, so the call would be rejected long before the described symptom appeared. The keyed remedy holds; the premise does not. |
| `ETO-C-058` | Stem arithmetic does not compute. At n=300 and p=0.18 the binomial SD is 0.022, putting the 0.25 boundary ~3.1 SD out — it would fire far less than the stated "roughly twice a week". Twice-weekly implies a denominator near 10/day. |
| `SCL-B-043` | On the stem's own linear sensitivity, the pilot's measured 58% implies roughly £1.0m three-year net, not the headline £1.4m (which needs a ~62% assumption the stem never states). The break-even ≈47% in the key does check out. |
| `SCL-B-069` | Stem claims a 31% fall in **cost per thousand tokens**; the correct option restates it as **cost per request**. Those coincide only if tokens per request are flat, which the stem never says. |

## Tier 2 — a wrong number inside a distractor

The item still grades correctly, but a candidate reading the distractor learns a bad
figure. Cheap to fix.

| id | defect |
|---|---|
| `GSR-A-063` | Distractor claims "roughly a third" reduction; 0.2×3 + 0.8×1 = 1.4 of 3 is ~53%. |
| `ETO-B-017` | Option says one category "can fail outright while the aggregate still clears 95%". With even category sizes it lands at 88.9%. "Can be badly degraded" would be true. |
| `DPO-B-019` | Distractor says raising sampling 1%→10% makes a miss "ten times less likely"; a miss drops 99%→90%. Capture is 10× likelier; a miss is not 10× rarer. |
| `DPO-B-061` | Chosen option asserts two figures "can only diverge if the populations differ"; a grader-vs-human criterion mismatch also produces divergence. Soften "can only". |
| `CPE-A-009` | Option states 8.6% where 52/600 = 8.67%. Truncation, not rounding. Trivial. |
| `ETO-A-006` | Distractor's "±3-point margin at n=200" is really ±5 — believed intentional (it is a distractor), confirm. |

## Tier 3 — possible over-key or two defensible answers

Verifiers still answered these correctly, but named a second option they could defend.
Each needs one decisive fact added to the stem, or the surplus option made false.

**Multi-select, surplus true option:**
`SCL-A-013` (4 defensible for choose-3) · `GSR-C-048` · `GSR-A-051` · `INT-B-026`
(option C reads as self-contradictory) · `CPE-C-066` · `GSR-C-050` (an embedded clause
makes D true) · `SDA-A-023` · `SDA-A-040`

**Single-answer, two defensible:**
`SCL-A-021` (the 18% figure in the stem makes the rival genuinely correct) ·
`ETO-C-059` · `ETO-C-063` · `ETO-D-026` · `CPE-B-056` · `CPE-A-050` · `CPE-A-063` ·
`DPO-B-027` · `DPO-A-070` · `INT-A-050` · `INT-A-067` · `INT-D-020` · `ETO-A-072` ·
`ETO-B-066` · `ETO-C-016` · `SCL-B-003` · `GSR-B-071` · `GSR-A-027`

**Overlapping options (gradeable, but close):**
`ETO-A-036` · `INT-B-070` · `SDA-A-043` · `ETO-D-013`

## Tier 4 — stem wording

| id | defect |
|---|---|
| `CPE-C-053` | Stem says an audit "has just arrived" covering notes from 18 months ago, but every option is a going-forward control. Nothing answers the audit that arrived. Change to "an audit is expected". |
| `GSR-A-020` | Stem excludes "clinician confirmation of every extracted field"; an option proposes *intake-clerk* confirmation, which the exclusion does not literally cover. Tighten to "human confirmation". |
| `GSR-B-062` | Stem infers the **caller's** emotional state; the correct option's justification says emotion inference applied to **workers**. Reached only via the supervisor aggregates — say so. |
| `DPO-B-052` | Assistant is stated as used 08:00–18:00, yet a monitor pages at 23:50, implying synthetic probe traffic the stem never mentions. |
| `SDA-A-041` | "Eleven variables emitted nothing" only coheres if 0.3% equals eleven, i.e. ~3,700 variables total, which the stem does not give. |
| `SCL-B-048` | "Cannot be improved by shedding hard cases" is only true if escalated cost stays in the numerator. |
| `SCL-B-068` | "The rest assessed within two working days" overreaches — the two-day figure is stated only for the 22% deferred. |
| `INT-D-030` | Option says "scale by adding partitions", which is not order-safe: repartitioning remaps keys and can break per-customer ordering. |
| `ETO-D-004` | An option catches the regression only if the parts master flags superseded status. |
| `ETO-D-028` | Rationale clause "a uniform sample over responses is dominated by short sessions" is not necessarily true given the stem says sessions run for hours. |

## Tier 5 — cross-item consistency

- **`DPO-A-054` vs `DPO-A-070`** — one rewards "add a CI check against a fresh checkout"
  and the other appears to penalise the same idea in favour of staged adoption. A
  prepared candidate who learns the first will get the second wrong. Reconcile them.

## Non-defects, recorded so the next reviewer does not re-raise them

- **`GSR-A-037`** — the option's mechanic ("a prefix must match exactly for a cache hit")
  is factually correct; the option is wrong on its pooled-credential reasoning, not on
  the fact. Working as intended.
- **`INT-B-004` / `INT-B-005`** — both depend on strict tool use not enforcing
  `minimum`/`maximum`/`multipleOf`, and the verifier confirmed they are mutually
  consistent on that point.
- **`INT-D-062`** — absent from the bank. Dropped at build time for having two options
  94% identical. Correct outcome.
- **Nine `CPE-B` items** end as a bare scenario with no interrogative sentence. Verifier
  judged it consistent house style rather than truncation, and it impeded no answers.
