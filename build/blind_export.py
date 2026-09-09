#!/usr/bin/env python3
"""
Export every shipped question as a BLIND review batch — key and explanation removed.

Usage:  python build/blind_export.py [items_per_batch]

Reads the questions actually embedded in Claude Certified Associate - Foundations.html (so we verify
exactly what ships, not what is sitting in the source folder) and writes
build/review/blind_NN.json.

An independent verifier answers each batch without ever seeing the recorded key.
Agreement is evidence the item is sound; disagreement flags it for adjudication.
Nothing here reveals the answer, so a verifier cannot be anchored by it.
"""
from __future__ import annotations
import hashlib, json, re, sys, unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BANK = ROOT / "Claude Certified Associate - Foundations.html"
RDIR = ROOT / "build" / "review"
KEYF = ROOT / "build" / "_answer_key.json"

PER = int(sys.argv[1]) if len(sys.argv) > 1 and sys.argv[1].isdigit() else 50
# --new-only exports just the items that have never been verified, or whose stem
# changed since they were. Re-verifying 1,400 settled items to reach 800 new ones
# is wasted effort, and it would clobber answer files that are still valid.
NEW_ONLY = "--new-only" in sys.argv


def _sha(stem: str) -> str:
    s = unicodedata.normalize("NFKD", str(stem)).lower()
    s = re.sub(r"[^a-z0-9]+", " ", s).strip()
    return hashlib.sha1(s.encode("utf-8")).hexdigest()[:12]


def already_verified():
    """ids -> hash of the stem a verifier actually answered.

    The blind export files are the source of truth here, not the answer key:
    they hold the exact question text that was put in front of a verifier. If an
    authoring agent has since rewritten that item, the hash will not match the
    shipped stem and the item is correctly treated as unverified.
    """
    seen_stem = {}
    for fp in sorted(RDIR.glob("blind_*.json")):
        try:
            d = json.loads(fp.read_text(encoding="utf-8-sig"))
        except Exception:
            continue
        for it in d.get("items", []):
            if it.get("id"):
                seen_stem[it["id"]] = it.get("question", "")

    answered = set()
    for fp in RDIR.glob("answers_*.json"):
        try:
            d = json.loads(fp.read_text(encoding="utf-8-sig"))
        except Exception:
            continue
        if isinstance(d, dict):
            d = d.get("answers") or d.get("items") or []
        for r in d:
            if isinstance(r, dict) and r.get("id"):
                answered.add(r["id"])

    return {qid: _sha(stem) for qid, stem in seen_stem.items() if qid in answered}


def main() -> int:
    if not BANK.exists():
        print("!! build the bank first (python build/assemble.py)")
        return 1
    html = BANK.read_text(encoding="utf-8")
    m = re.search(r"const QUESTIONS = (\[.*?\]);\nconst FLASHCARDS", html, re.S)
    if not m:
        print("!! could not locate the QUESTIONS array in the bank")
        return 1
    items = json.loads(m.group(1))
    print(f"loaded {len(items):,} shipped questions")

    RDIR.mkdir(parents=True, exist_ok=True)
    start = 1
    if NEW_ONLY:
        done = already_verified()
        keep = [it for it in items
                if done.get(it["id"]) is None or done[it["id"]] != _sha(it["stem"])]
        changed = sum(1 for it in items
                      if it["id"] in done and done[it["id"]] != _sha(it["stem"]))
        print(f"already verified and unchanged: {len(items)-len(keep):,}")
        print(f"to verify: {len(keep):,}  ({changed} of them rewritten since last pass)")
        items = keep
        # keep existing batch files and their answers; number the new ones after
        existing = [int(p.stem.split("_")[1]) for p in RDIR.glob("blind_*.json")
                    if p.stem.split("_")[1].isdigit()]
        start = (max(existing) + 1) if existing else 1
        if not items:
            print("nothing new to verify")
            return 0
    else:
        for old in RDIR.glob("blind_*.json"):
            old.unlink()

    batches = [items[i:i + PER] for i in range(0, len(items), PER)]
    for n, chunk in enumerate(batches, start):
        out = {
            "batch": f"blind_{n:02d}",
            "count": len(chunk),
            "answer_file": f"build/review/answers_{n:02d}.json",
            "items": [
                {
                    "id": it["id"],
                    "choose": len(it["correct"]),
                    "question": it["stem"],
                    "options": {o["key"]: o["text"] for o in it["options"]},
                }
                for it in chunk
            ],
        }
        (RDIR / f"blind_{n:02d}.json").write_text(
            json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")

    # The key file stays out of the review folder so a verifier cannot stumble on
    # it. Under --new-only the previous key is merged in, not replaced, so that
    # adjudicate.py can still grade the batches verified in earlier passes.
    key = {}
    if NEW_ONLY and KEYF.exists():
        try:
            key = json.loads(KEYF.read_text(encoding="utf-8-sig"))
        except Exception:
            key = {}
    all_shipped = json.loads(m.group(1))
    for it in all_shipped:
        if NEW_ONLY and it["id"] in key and key[it["id"]].get("stem_sha") == _sha(it["stem"]):
            continue
        key[it["id"]] = {"correct": it["correct"], "domain": it["domain"],
                         "difficulty": it["difficulty"], "type": it["type"],
                         "stem_sha": _sha(it["stem"])}
    KEYF.write_text(json.dumps(key, ensure_ascii=False), encoding="utf-8")

    print(f"wrote {len(batches)} blind batch(es) of up to {PER} items "
          f"(numbered from {start:02d}) to build/review/")
    print(f"answer key held separately at build/_answer_key.json ({len(key):,} entries)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
