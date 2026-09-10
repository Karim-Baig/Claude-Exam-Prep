# CCAR-P build state

Working checkpoint. Update as phases complete.

## Deliverable

`Claude Certified Architect - Professional.html` — single self-contained file.
Build with: `python build/ccarp/assemble.py --rebalance`

## Pipeline

| Script | Purpose |
|---|---|
| `build/ccarp/assemble.py` | validate + bundle into the HTML |
| `build/ccarp/audit.py` | bank-scale defect scan (length tell, invented facts, cross-batch dupes) |
| `build/ccarp/verify.py export` | write blind batches, hold the key back |
| `build/ccarp/verify.py score` | diff verifier answers against the key |

UI test (jsdom, 51 assertions), run after every build:

```
SP=<scratchpad>
NODE_PATH="$SP/node_modules" node "$SP/uitest.js" "Claude Certified Architect - Professional.html"
```

## Phase 1 — authoring (22 batches x 72 items, + ETO-D at 36)

DONE: INT-A INT-B INT-C INT-D SDA-A SDA-B SDA-C SDA-D ETO-A ETO-B
      GSR-A GSR-B SCL-A SCL-B CPE-A CPE-B
IN FLIGHT: ETO-C ETO-D GSR-C SCL-C CPE-C DPO-A DPO-B
FLASHCARDS: set 1 done (80 cards, INT/SDA/ETO/GSR). set 2 in flight (60 cards, SCL/CPE/DPO).

## Phase 2 — length-tell repair

Audit at 1,116 items found the correct option was the LONGEST in **85% of the bank**
(chance = 25%). Exam-validity defect: scoreable without knowing the material.
Repair spec: `spec/LENGTH_REPAIR.md`. Option wording only; `correct` never changes.

**COMPLETE. Bank-wide 85% -> 26%** against a 25% chance baseline, average margin +56c
-> +5c. `audit.py` reports "no batch shows a length tell". Every one of the 23 batches
now sits between 16% and 33%. The build prints this line on every run, so it cannot
regress silently.

Residual, being handled: multi-select items carried a milder version (all keys being
the longest options: 22% vs 10% chance). One agent is balancing the five worst
batches — CPE-A (71%), SCL-B (50%), GSR-B (43%), SCL-C (40%), INT-B (36%).

DONE: INT-A 48->24 · INT-B 71->26 · INT-D 97->29 · SDA-A 97->28 · SDA-B 97->28
      CPE-A 64->24 · CPE-B 94->30 · ETO-A 86->23 · SCL-A 83->21 · SCL-B 98->28
      GSR-B 93->28
SELF-FIXED by their authoring agent, verified, no repair needed:
      CPE-C 18% · ETO-C 30% · ETO-D 26% · SCL-C 18% · DPO-B 26%
STILL IN FLIGHT: **ETO-B, SDA-C, SDA-D, INT-C, GSR-A, GSR-C, DPO-A**

## Two traps this phase produced — read before dispatching another repair

**1. Never repair a batch whose authoring agent is still writing.** They collide. Worse,
the audit will give you a *misleading percentage*: it reads whatever shards exist, so a
batch that is one-quarter authored reports that quarter's numbers. DPO-B was dispatched
at "48%" measured from `-p1` alone; the finished 72-item batch was 26% and needed
nothing. **Check the batch has all 72 items before trusting any percentage for it.**

**2. Authoring agents often fix their own tell between your audit and their report.**
ETO-C, SCL-C and DPO-B were all repaired twice-over this way. Before dispatching, and
again on arrival, measure the files on disk. Two dispatched agents correctly detected
the concurrent rewrite, snapshotted, diffed and made zero edits — that is the right
outcome, not a failure.

**3. Do not drive the tell to zero.** "The key is never the longest" is exactly as
learnable as the original defect. Target ~25% longest AND ~25% shortest.

Wave-3 batches were explicitly warned about the tell in their authoring brief and most
still shipped it (ETO-C at 86% on first draft). The warning helps but does not prevent
it: this is a deep authoring bias. Budget the repair pass in; do not hope it away.

## Phase 3 — blind verification  (COMPLETE)

All 1,618 candidate items exported with key + explanation stripped and answered cold by
independent verifiers, diffed against a key held outside the review folder.

    Coverage      1,618 / 1,618   100%
    Agreement     1,616 / 1,618   99.9%
    Disagreements 2      -> both adjudicated by hand, both QUARANTINED (see assemble.py)
    Low-confidence 1     -> reviewed, item kept (the rival is the intended trap)
    Multi-select disagreements  0 of 327

Blind export was itself audited: every item exposes only id / choose / question /
options. Zero leakage, so the agreement figure is real.

~39 items were then edited to repair defects verification found, and **re-verified
blind in their repaired form: 39/39 agreement**. That second pass caught two more
defects the first could not have seen, both since fixed:

- `SDA-C-003` had a physically impossible premise — with non-overlapping spans and
  synchronised clocks, end-to-end p95 cannot fall below the largest single stage.
  Measured 1,690 ms against an 1,820 ms stage. Now 1,900 ms.
- `CPE-A-009` used 91.4% on n=600, which is not representable (548/600 = 91.3%).

## Phase 4 — final  (COMPLETE)

    1,617 questions   140 flashcards   80 "10 Things" concepts   4.99 MB
    3 items withheld: 2 quarantined after adjudication, 1 genuine duplicate-option
    54 / 54 UI assertions pass (jsdom, drives the real user path)
    length tell 26% vs 25% chance   key spread A 25.0 / B 25.1 / C 25.0 / D 24.8
    zero duplicate stems, zero incomplete explanations, zero distractor-coverage gaps
    zero mojibake, zero control chars, one </script>, no unreplaced placeholders

Docs: `docs/CCAR-P.md`. Defect register: `build/ccarp/review/DEFECTS.md`.
README updated with the CCAR-P section.

## One lesson worth carrying forward

The near-duplicate-option check originally compared word *sets*, which flagged
`ETO-B-043` — where option A is the definition of recall and B is the definition of
precision. Nearly identical words, opposite meanings, and the distinction is the entire
question. The check now requires word *order* to match too before dropping an item.
Any mechanical similarity test needs that guard, or it deletes exactly the items that
teach a converse pair.
