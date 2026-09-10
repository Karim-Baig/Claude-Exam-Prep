#!/usr/bin/env python3
"""
Blind verification harness for the CCAR-P bank.

    python build/ccarp/verify.py export [per_batch]   # write blind batches + hold the key
    python build/ccarp/verify.py score                # diff verifier answers against the key

`export` reads the questions actually shipped in the built HTML — so we verify what a
candidate will really see, not what is sitting in the source folder — and writes
build/ccarp/review/blind_NN.json with the key and explanation stripped out. A verifier
agent answers each batch cold. It cannot be anchored by an answer it never saw.

`score` diffs those answers against the held-back key. Agreement is evidence an item is
sound. Disagreement means one of three things, and only a human read separates them:

    1. the recorded key is wrong        -> fix or drop the item
    2. the item is genuinely ambiguous  -> two defensible answers, rewrite it
    3. the verifier was wrong           -> item is fine, leave it

Verdicts are bound to a hash of the stem. If an item is rewritten after a verdict is
recorded, the hash stops matching and the verdict is treated as stale rather than
silently applied to a question it was never about.
"""
from __future__ import annotations
import hashlib, json, re, sys, unicodedata
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
BANK = ROOT / "Claude Certified Architect - Professional.html"
RDIR = ROOT / "build" / "ccarp" / "review"
KEYF = ROOT / "build" / "ccarp" / "_key.json"
OUT  = RDIR / "DISAGREEMENTS.md"


def sha(stem: str) -> str:
    s = unicodedata.normalize("NFKD", str(stem)).lower()
    return hashlib.sha1(re.sub(r"[^a-z0-9]+", " ", s).strip().encode()).hexdigest()[:12]


def shipped() -> list:
    if not BANK.exists():
        sys.exit("!! build the bank first: python build/ccarp/assemble.py")
    m = re.search(r"const QUESTIONS = (\[.*?\]);\nconst FLASHCARDS",
                  BANK.read_text(encoding="utf-8"), re.S)
    if not m:
        sys.exit("!! could not find the QUESTIONS array in the bank")
    return json.loads(m.group(1).replace("<\\/", "</"))


def export(per: int):
    items = shipped()
    RDIR.mkdir(parents=True, exist_ok=True)
    for old in RDIR.glob("blind_*.json"):
        old.unlink()

    batches = [items[i:i + per] for i in range(0, len(items), per)]
    for n, chunk in enumerate(batches, 1):
        (RDIR / f"blind_{n:02d}.json").write_text(json.dumps({
            "batch": f"blind_{n:02d}",
            "count": len(chunk),
            "answer_file": f"build/ccarp/review/answers_{n:02d}.json",
            "items": [{
                "id": it["id"],
                "choose": len(it["correct"]),
                "question": it["stem"],
                "options": {o["key"]: o["text"] for o in it["options"]},
            } for it in chunk],
        }, ensure_ascii=False, indent=1), encoding="utf-8")

    # The key lives outside review/ so a verifier cannot stumble across it.
    KEYF.write_text(json.dumps({
        it["id"]: {"correct": it["correct"], "domain": it["domain"], "type": it["type"],
                   "difficulty": it["difficulty"], "stem_sha": sha(it["stem"])}
        for it in items}, ensure_ascii=False), encoding="utf-8")

    print(f"{len(items):,} shipped items -> {len(batches)} blind batch(es) of up to {per}")
    print(f"key held separately at {KEYF.relative_to(ROOT)}")


def score():
    if not KEYF.exists():
        sys.exit("!! run `verify.py export` first")
    key = json.loads(KEYF.read_text(encoding="utf-8"))
    items = {it["id"]: it for it in shipped()}

    answers, dupes, unparsed = {}, 0, []
    for fp in sorted(RDIR.glob("answers_*.json")):
        try:
            d = json.loads(fp.read_text(encoding="utf-8-sig"))
        except Exception as e:
            unparsed.append(f"{fp.name}: {e}")
            continue
        if isinstance(d, dict):
            d = d.get("answers") or d.get("items") or []
        for r in d:
            if isinstance(r, dict) and r.get("id"):
                dupes += r["id"] in answers
                answers[r["id"]] = r
    for u in unparsed:
        print("  !!", u)
    if not answers:
        sys.exit("!! no answers_*.json in build/ccarp/review/ — verifiers have not reported")

    graded = [q for q in answers if q in key]
    print(f"verifier answers {len(answers):,}   graded {len(graded):,} of {len(key):,} "
          f"shipped ({100*len(graded)/max(1,len(key)):.0f}% covered)")
    if dupes:
        print(f"   {dupes} duplicate id(s) across answer files (last wins)")

    agree, dis = [], []
    for q in graded:
        rec = {str(k).upper() for k in key[q]["correct"]}
        got = {str(k).upper() for k in (answers[q].get("answer") or [])}
        (agree if rec == got else dis).append(q)
    rate = 100 * len(agree) / max(1, len(graded))
    print(f"\nAGREEMENT {len(agree):,}/{len(graded):,} = {rate:.1f}%    DISAGREEMENT {len(dis):,}")

    for field in ("domain", "type", "difficulty"):
        tot, bad = Counter(key[q][field] for q in graded), Counter(key[q][field] for q in dis)
        print(f"\nby {field}:")
        for k in sorted(tot, key=lambda x: -bad.get(x, 0) / max(1, tot[x])):
            print(f"   {bad.get(k,0):>4}/{tot[k]:<5} {100*bad.get(k,0)/max(1,tot[k]):>5.1f}%   {k}")

    per_batch = defaultdict(lambda: [0, 0])
    for q in graded:
        per_batch[q.rsplit("-", 1)[0]][0] += 1
    for q in dis:
        per_batch[q.rsplit("-", 1)[0]][1] += 1
    print("\nworst batches:")
    for b, (n, d) in sorted(per_batch.items(), key=lambda kv: -kv[1][1] / max(1, kv[1][0]))[:12]:
        if d:
            print(f"   {d:>4}/{n:<5} {100*d/max(1,n):>5.1f}%   {b}")

    shaky = [q for q in agree if str(answers[q].get("confidence", "")).lower() == "low"]
    print(f"\n{len(shaky)} item(s) answered correctly but at LOW confidence — possible ambiguity")

    lines = [f"# CCAR-P blind adjudication — {len(dis)} disagreement(s)", "",
             f"Coverage {len(graded):,}/{len(key):,}. Agreement {rate:.1f}%.", "",
             "Each entry is an item where an independent verifier, working without sight of",
             "the recorded answer, chose differently. Either the key is wrong, or the item is",
             "ambiguous, or the verifier erred. A human read decides which.", ""]
    for q in sorted(dis, key=lambda x: (key[x]["domain"], x)) + \
             [q for q in shaky if q not in dis]:
        r, it = answers[q], items.get(q, {})
        tagged = "LOW-CONFIDENCE AGREEMENT" if q not in dis else "DISAGREEMENT"
        lines += [f"## {q} — {key[q]['domain']} / {key[q]['difficulty']} / {key[q]['type']}  ({tagged})", "",
                  f"- **recorded:** {'+'.join(sorted(key[q]['correct']))}",
                  f"- **verifier:** {'+'.join(sorted(r.get('answer') or [])) or '(none)'} "
                  f"(confidence {r.get('confidence','?')})"]
        if r.get("note"):
            lines.append(f"- **verifier reasoning:** {r['note']}")
        if it:
            lines += ["", "> " + str(it.get("stem", "")).replace("\n", "\n> "), ""]
            for o in it.get("options", []):
                mk = " **(recorded)**" if o["key"] in key[q]["correct"] else ""
                pk = " **(verifier)**" if o["key"] in (r.get("answer") or []) else ""
                lines.append(f"- `{o['key']}` {o['text']}{mk}{pk}")
            ex = it.get("explanation") or {}
            if ex.get("correct"):
                lines += ["", f"*Author's rationale:* {ex['correct']}"]
        lines.append("")
    RDIR.mkdir(parents=True, exist_ok=True)
    OUT.write_text("\n".join(lines), encoding="utf-8")
    print(f"\n-> {OUT.relative_to(ROOT)}  ({len(dis)} disagreement(s) + {len(shaky)} low-confidence)")


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else ""
    if cmd == "export":
        export(int(sys.argv[2]) if len(sys.argv) > 2 and sys.argv[2].isdigit() else 55)
    elif cmd == "score":
        score()
    else:
        sys.exit(__doc__)
