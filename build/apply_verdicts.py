#!/usr/bin/env python3
"""
Merge verification findings into build/verdicts.json.

Usage:  python build/apply_verdicts.py [--write]

Sources, in increasing authority:
  1. build/review/answers_*.json      — verifier items marked confidence "low".
                                        A low-confidence answer means two or more
                                        options were genuinely defensible, which
                                        makes the item defective by definition.
  2. build/review/PROPOSED_VERDICTS.json — adjudicator rulings on disagreements
                                        (optional; overrides source 1).

Each entry is bound to a `stem_sha` computed from the stem AS IT WAS VERIFIED
(read out of the blind export, not the current source file). If an authoring
agent later rewrites that item, the hash stops matching and assemble.py refuses
to apply the verdict — so a verdict about an old question can never silently
delete a new one. That has already happened once in this project.

Without --write this only reports what it would change.
"""
from __future__ import annotations
import json, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from assemble import norm  # noqa: E402
import hashlib

ROOT = Path(__file__).resolve().parent.parent
RDIR = ROOT / "build" / "review"
VF   = ROOT / "build" / "verdicts.json"
WRITE = "--write" in sys.argv


def sha(stem: str) -> str:
    return hashlib.sha1(norm(stem).encode("utf-8")).hexdigest()[:12]


def main() -> int:
    # ---- stems exactly as the verifiers saw them ----
    verified_stems = {}
    for fp in sorted(RDIR.glob("blind_*.json")):
        d = json.loads(fp.read_text(encoding="utf-8-sig"))
        for it in d.get("items", []):
            verified_stems[it["id"]] = it["question"]
    if not verified_stems:
        print("!! no blind_*.json found — run build/blind_export.py first")
        return 1

    # A verifier often describes a structural defect while still rating its own
    # answer "medium" — it knew which subset the author probably wanted. The
    # defect is in the prose, not the confidence field, so match the prose too.
    import re as _re
    DEFECT_NOTE = _re.compile(
        r"over[-\s]?keyed"
        r"|(?:three|four|3|4)\s+(?:of\s+the\s+\w+\s+)?(?:options|statements)?\s*(?:are|is)?\s*"
        r"(?:all\s+)?(?:genuinely\s+|equally\s+)?(?:true|correct|defensible|essential)"
        r"|more\s+true\s+options?\s+than"
        r"|than\s+(?:the\s+number\s+)?requested"
        r"|for\s+(?:only\s+)?(?:two|three)\s+slots"
        r"|near[-\s]?duplicates?"
        r"|(?:assert|prescribe|describe|say|give|name)\s+(?:essentially\s+|materially\s+)?"
        r"the\s+same"
        r"|no\s+(?:option|answer)\s+is\s+(?:cleanly\s+)?correct"
        r"|arithmetic\s+is\s+wrong|does\s+not\s+compute|premise\s+is\s+broken"
        r"|equally\s+defensible|both\s+(?:are\s+)?(?:fully\s+)?(?:correct|defensible)",
        _re.I)

    # ---- source 1: low-confidence verifier flags ----
    proposals = {}
    for fp in sorted(RDIR.glob("answers_*.json")):
        try:
            d = json.loads(fp.read_text(encoding="utf-8-sig"))
        except Exception as ex:
            print(f"   skipping {fp.name}: {ex}")
            continue
        if isinstance(d, dict):
            d = d.get("answers") or d.get("items") or []
        for r in d:
            if not isinstance(r, dict) or not r.get("id"):
                continue
            conf = str(r.get("confidence", "")).lower()
            note = str(r.get("note", "")).strip()
            low = conf == "low"
            described_defect = bool(note) and bool(DEFECT_NOTE.search(note))
            if not (low or described_defect):
                continue
            label = ("LOW confidence" if low else f"{conf or 'unrated'} confidence, "
                                                  f"but described a structural defect")
            proposals[r["id"]] = {
                "action": "quarantine",
                "reason": f"Blind verifier ({label}): {note or 'no note given'}",
            }

    # ---- source 2: adjudicator rulings (authoritative) ----
    pv = RDIR / "PROPOSED_VERDICTS.json"
    adjudicated = 0
    cleared = {}
    if pv.exists():
        try:
            for r in json.loads(pv.read_text(encoding="utf-8-sig")):
                if not isinstance(r, dict) or not r.get("id"):
                    continue
                act = str(r.get("action", "")).lower()
                if act not in ("quarantine", "rekey", "keep"):
                    continue
                adjudicated += 1
                if act == "keep":
                    # The adjudicator ruled the item sound. Drop any pending
                    # proposal AND lift an existing quarantine, since a verifier's
                    # low-confidence flag is weaker evidence than a full ruling.
                    proposals.pop(r["id"], None)
                    cleared[r["id"]] = f"Adjudicated keep: {r.get('reason','')}"
                    continue
                proposals[r["id"]] = {
                    "action": act,
                    "reason": f"Adjudicated ({r.get('verdict','?')}): {r.get('reason','')}",
                    "correct": r.get("correct"),
                }
        except Exception as ex:
            print(f"!! PROPOSED_VERDICTS.json unreadable: {ex}")
    else:
        print("note: no PROPOSED_VERDICTS.json yet — using verifier flags only")

    # ---- merge into the existing verdicts file ----
    cur = json.loads(VF.read_text(encoding="utf-8-sig")) if VF.exists() else {}
    q = cur.setdefault("quarantine", {})
    rk = cur.setdefault("rekey", {})
    resolved = cur.get("_resolved", {})

    added_q, added_r, skipped, lifted, refreshed, retired = [], [], [], [], [], []
    for qid, why in sorted(cleared.items()):
        if qid in q:
            resolved = cur.setdefault("_resolved", {})
            resolved[qid] = f"Quarantine LIFTED. {why} (was: {q[qid].get('reason','')[:200]})"
            q.pop(qid)
            lifted.append(qid)

    # Reconcile verdicts whose item has since been rewritten AND re-verified.
    # Without this, a stale entry blocks its own replacement: the id is "already
    # recorded" so a fresh flag cannot update the hash, and a fresh clean pass
    # cannot retire it. Either way the item sits in limbo, neither dropped nor
    # cleared.
    for qid in sorted(list(q)):
        if qid.startswith("_"):
            continue
        recorded = q[qid].get("stem_sha")
        stem_now = verified_stems.get(qid)
        if not recorded or not stem_now:
            continue
        fresh = sha(stem_now)
        if fresh == recorded:
            continue                       # verdict still matches what was reviewed
        if qid in proposals:
            # rewritten and flagged again — carry the verdict forward
            q[qid] = {"stem_sha": fresh, "reason": proposals[qid]["reason"][:600]}
            proposals.pop(qid)
            refreshed.append(qid)
        else:
            # rewritten and the fresh pass did not flag it — the defect is gone
            cur.setdefault("_resolved", {})[qid] = (
                f"Quarantine RETIRED: item was rewritten and re-verified clean. "
                f"Original reason: {q[qid].get('reason','')[:250]}")
            q.pop(qid)
            retired.append(qid)

    for qid, p in sorted(proposals.items()):
        if qid in q or qid in rk:
            skipped.append(f"{qid} (already recorded)")
            continue
        if qid in resolved:
            skipped.append(f"{qid} (previously resolved — re-review by hand)")
            continue
        stem = verified_stems.get(qid)
        if not stem:
            skipped.append(f"{qid} (not in any blind export, cannot bind a hash)")
            continue
        entry = {"stem_sha": sha(stem), "reason": p["reason"][:600]}
        if p["action"] == "rekey" and p.get("correct"):
            rk[qid] = {"stem_sha": sha(stem), "correct": list(p["correct"]),
                       "why": p["reason"][:600]}
            added_r.append(qid)
        else:
            q[qid] = entry
            added_q.append(qid)

    print(f"verified stems available: {len(verified_stems):,}")
    print(f"adjudicator rulings read: {adjudicated}")
    print(f"proposals: {len(proposals)}  ->  quarantine +{len(added_q)}, rekey +{len(added_r)}, "
          f"skipped {len(skipped)}")
    for qid in added_q:
        print(f"   Q {qid}: {q[qid]['reason'][:105]}")
    for qid in added_r:
        print(f"   R {qid} -> {'+'.join(rk[qid]['correct'])}")
    for qid in lifted:
        print(f"   ^ {qid}: quarantine LIFTED by adjudicator ruling")
    for qid in refreshed:
        print(f"   * {qid}: rewritten and re-flagged — verdict hash refreshed")
    for qid in retired:
        print(f"   v {qid}: rewritten and re-verified clean — quarantine RETIRED")
    for s in skipped:
        print(f"   - {s}")

    if WRITE:
        VF.write_text(json.dumps(cur, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"\n-> updated {VF.relative_to(ROOT)}  "
              f"({len(q)} quarantined, {len(rk)} re-keyed in total)")
    else:
        print("\n(dry run — pass --write to apply)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
