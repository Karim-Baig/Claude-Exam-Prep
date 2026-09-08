#!/usr/bin/env python3
"""
Compare blind verifier answers against the recorded keys and report disagreements.

Usage:  python build/adjudicate.py [--detail]

Reads every build/review/answers_*.json produced by the verifier agents and diffs
them against build/_answer_key.json.

Interpreting the output
-----------------------
An independent verifier agreeing with the author is evidence the item is sound.
Disagreement means one of three things, and only a human read can separate them:

  1. the recorded key is wrong          -> fix or drop the item
  2. the item is genuinely ambiguous    -> two defensible answers, rewrite it
  3. the verifier was wrong             -> item is fine, leave it

Disagreement rate is the headline number. For well-built items a competent
verifier should agree ~90%+ of the time. A much lower rate on some domain points
at systematic trouble in that batch, not at bad luck.
"""
from __future__ import annotations
import json, sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RDIR = ROOT / "build" / "review"
KEYF = ROOT / "build" / "_answer_key.json"
BANK = ROOT / "CCAO-F_Question_Bank.html"
OUT  = ROOT / "build" / "review" / "DISAGREEMENTS.md"

DETAIL = "--detail" in sys.argv


def main() -> int:
    if not KEYF.exists():
        print("!! run build/blind_export.py first")
        return 1
    key = json.loads(KEYF.read_text(encoding="utf-8"))

    answers, dupes = {}, 0
    files = sorted(RDIR.glob("answers_*.json"))
    if not files:
        print("!! no answers_*.json found in build/review/ — verifiers have not reported yet")
        return 1
    for fp in files:
        try:
            data = json.loads(fp.read_text(encoding="utf-8-sig"))
        except Exception as ex:
            print(f"   {fp.name}: UNPARSEABLE ({ex})")
            continue
        if isinstance(data, dict):
            data = data.get("answers") or data.get("items") or []
        for r in data:
            if not isinstance(r, dict) or not r.get("id"):
                continue
            if r["id"] in answers:
                dupes += 1
            answers[r["id"]] = r

    graded = [q for q in answers if q in key]
    print(f"verifier answers: {len(answers):,}   matched to key: {len(graded):,} "
          f"of {len(key):,} shipped items ({100*len(graded)/max(1,len(key)):.0f}% covered)")
    if dupes:
        print(f"   note: {dupes} duplicate id(s) across answer files (last one used)")
    if not graded:
        return 1

    agree, disagree = [], []
    for qid in graded:
        rec = {str(k).upper() for k in key[qid]["correct"]}
        got = {str(k).upper() for k in (answers[qid].get("answer") or [])}
        (agree if rec == got else disagree).append(qid)

    rate = 100 * len(agree) / len(graded)
    print(f"\nAGREEMENT: {len(agree):,}/{len(graded):,} = {rate:.1f}%"
          f"   DISAGREEMENT: {len(disagree):,}")

    # ---- where the disagreements cluster ----
    for field, label in (("domain", "domain"), ("difficulty", "difficulty"), ("type", "type")):
        tot = Counter(key[q][field] for q in graded)
        bad = Counter(key[q][field] for q in disagree)
        print(f"\ndisagreement by {label}:")
        for k in sorted(tot, key=lambda x: -bad.get(x, 0) / max(1, tot[x])):
            n, d = tot[k], bad.get(k, 0)
            print(f"   {d:>4}/{n:<5} {100*d/max(1,n):>5.1f}%   {k}")

    batch = defaultdict(lambda: [0, 0])
    for q in graded:
        batch[q.rsplit("-", 1)[0]][0] += 1
    for q in disagree:
        batch[q.rsplit("-", 1)[0]][1] += 1
    worst = sorted(batch.items(), key=lambda kv: -kv[1][1] / max(1, kv[1][0]))[:12]
    print("\nworst batches by disagreement rate:")
    for b, (n, d) in worst:
        if d:
            print(f"   {d:>4}/{n:<5} {100*d/max(1,n):>5.1f}%   {b}")

    # ---- low-confidence agreements are also worth a look ----
    shaky = [q for q in agree if str(answers[q].get("confidence", "")).lower() == "low"]
    if shaky:
        print(f"\n{len(shaky)} item(s) the verifier answered correctly but with LOW confidence "
              f"— possible ambiguity")

    # ---- write the review file ----
    stems = {}
    if BANK.exists():
        import re
        html = BANK.read_text(encoding="utf-8")
        m = re.search(r"const QUESTIONS = (\[.*?\]);\nconst FLASHCARDS", html, re.S)
        if m:
            stems = {i["id"]: i for i in json.loads(m.group(1))}

    lines = [f"# Blind adjudication — {len(disagree)} disagreement(s)", "",
             f"Coverage {len(graded):,}/{len(key):,} shipped items. "
             f"Agreement {rate:.1f}%.", "",
             "Each entry below is an item where an independent verifier, working without",
             "sight of the recorded answer, chose differently from the author. One of the",
             "two is wrong, or the item is ambiguous. Verdicts needed.", ""]
    for qid in sorted(disagree, key=lambda q: (key[q]["domain"], q)):
        r, it = answers[qid], stems.get(qid, {})
        lines += [f"## {qid} — {key[qid]['domain']} / {key[qid]['difficulty']} / {key[qid]['type']}",
                  "",
                  f"- **recorded answer:** {'+'.join(sorted(key[qid]['correct']))}",
                  f"- **verifier answer:** {'+'.join(sorted(r.get('answer') or [])) or '(none)'}"
                  f"  (confidence: {r.get('confidence','?')})"]
        if r.get("note"):
            lines.append(f"- **verifier reasoning:** {r['note']}")
        if it:
            lines += ["", "> " + str(it.get("stem", "")).replace("\n", "\n> "), ""]
            for o in it.get("options", []):
                mark = "**(recorded)**" if o["key"] in key[qid]["correct"] else ""
                pick = "**(verifier)**" if o["key"] in (r.get("answer") or []) else ""
                lines.append(f"- `{o['key']}` {o['text']} {mark}{pick}")
            ex = it.get("explanation") or {}
            if ex.get("correct"):
                lines += ["", f"*Author's rationale:* {ex['correct']}"]
        lines.append("")
    OUT.write_text("\n".join(lines), encoding="utf-8")
    print(f"\n-> wrote {OUT.relative_to(ROOT)}  ({len(disagree)} item(s) needing a verdict)")

    if DETAIL:
        print("\n" + "\n".join(lines[:120]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
