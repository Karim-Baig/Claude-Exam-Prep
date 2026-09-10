#!/usr/bin/env python3
"""
Mechanical defect scan across the whole CCAR-P bank.

    python build/ccarp/audit.py [--show N]

Runs the checks that only make sense at bank scale — the ones no single authoring
batch can see. Several are ADVISORY: they surface candidates for a human read rather
than asserting a defect. False positives are expected and noted per section.

The one check that is not advisory is the answer-length tell. Most batches shipped
drafts where the correct option was the longest in ~90% of items, which lets a
test-wise candidate score without knowing the material. It cannot be fixed
mechanically — padding text to equalise lengths produces obvious filler — so it is
reported per batch and repaired by re-authoring the option prose. See
spec/LENGTH_REPAIR.md.
"""
from __future__ import annotations
import json, re, sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
QDIR = ROOT / "build" / "ccarp" / "questions"
SHOW = int(sys.argv[sys.argv.index("--show") + 1]) if "--show" in sys.argv else 6

items = []
for fp in sorted(QDIR.glob("*.json")):
    try:
        for it in json.loads(fp.read_text(encoding="utf-8-sig")):
            if isinstance(it, dict) and it.get("id"):
                it["_f"] = fp.name
                items.append(it)
    except Exception as e:
        print(f"  !! {fp.name}: {e}")

by_id = {}
for it in items:
    by_id[it["id"]] = it
items = list(by_id.values())
print(f"scanning {len(items):,} items from {len(set(i['_f'] for i in items))} files\n")

batch = lambda i: i["id"].rsplit("-", 1)[0]
nfails = 0


def head(t):
    print("\n" + "=" * 72)
    print(t)
    print("=" * 72)


# ---------------------------------------------------------------- 1. length tell
head("1. ANSWER-LENGTH TELL  (not advisory — this is an exam-validity defect)")
print("If the correct option is reliably the longest, a candidate can score without")
print("knowing the material. Chance is 1/n_options: 25% on a 4-option item.\n")

per = defaultdict(lambda: {"n": 0, "long": 0, "short": 0, "marg": 0.0})
for it in items:
    if len(it["correct"]) != 1:
        continue
    opts = it["options"]
    L = {o["key"]: len(o["text"]) for o in opts}
    k = it["correct"][0]
    if k not in L:
        continue
    b = per[batch(it)]
    b["n"] += 1
    if L[k] == max(L.values()):
        b["long"] += 1
    if L[k] == min(L.values()):
        b["short"] += 1
    others = [v for kk, v in L.items() if kk != k]
    b["marg"] += L[k] - (sum(others) / len(others))

print(f"{'batch':<10}{'n':>5}{'longest':>10}{'expected':>10}{'shortest':>10}{'avg margin':>12}   verdict")
bad = []
for bn in sorted(per):
    b = per[bn]
    if not b["n"]:
        continue
    pl, exp = 100 * b["long"] / b["n"], 25.0
    ps = 100 * b["short"] / b["n"]
    mg = b["marg"] / b["n"]
    v = ""
    if pl >= 55:
        v = "<-- STRONG TELL"; bad.append(bn); nfails += 1
    elif pl >= 40:
        v = "<-- leaning"
    elif ps >= 55:
        v = "<-- inverse tell"; bad.append(bn); nfails += 1
    print(f"{bn:<10}{b['n']:>5}{pl:>9.0f}%{exp:>9.0f}%{ps:>9.0f}%{mg:>+11.0f}c   {v}")

alln = sum(b["n"] for b in per.values())
alll = sum(b["long"] for b in per.values())
allm = sum(b["marg"] for b in per.values()) / max(1, alln)
print(f"\nBANK      {alln:>5}{100*alll/max(1,alln):>9.0f}%{25:>9.0f}%{'':>10}{allm:>+11.0f}c")
if bad:
    print(f"\n  batches needing a length rewrite: {', '.join(bad)}")
else:
    print("\n  no batch shows a length tell")


# ------------------------------------------------------- 2. invented product facts
head("2. POSSIBLE INVENTED PRODUCT FACTS  (advisory — many will be the org's own numbers)")
PATS = [
    ("price",        r"\$\s?\d[\d,.]*\s*(?:per|/)\s*(?:million|1M|1,000,000|token|M\b)"),
    ("rate limit",   r"\b\d[\d,]*\s*(?:requests?|calls?|tokens?)\s*per\s*(?:minute|second)"),
    ("rpm/tpm",      r"\b\d[\d,]*\s*(?:RPM|TPM|QPS)\b"),
    ("file cap",     r"\b\d+\s*(?:MB|GB)\b[^.]{0,30}\b(?:limit|cap|maximum|max)\b"),
    ("cutoff date",  r"\b(?:knowledge|training)\s+(?:cut-?off|data)[^.]{0,25}\b20\d\d\b"),
    ("benchmark",    r"\b(?:MMLU|SWE-?bench|HumanEval|GPQA|ARC-?AGI|MATH)\b[^.]{0,25}\d"),
    ("versioned model", r"\bclaude[-\s](?:3|3\.5|3\.7|4|opus|sonnet|haiku)[-\s]?\d{6,8}\b"),
    ("cache TTL",    r"\bcache[^.]{0,30}\b\d+\s*(?:minute|hour|second)s?\b"),
]
tot = 0
for name, p in PATS:
    rx = re.compile(p, re.I)
    hits = []
    for it in items:
        blob = it["stem"] + " " + " ".join(o["text"] for o in it["options"])
        m = rx.search(blob)
        if m:
            hits.append((it["id"], m.group(0)[:64]))
    tot += len(hits)
    if hits:
        print(f"\n  {name}: {len(hits)}")
        for i, s in hits[:SHOW]:
            print(f"     {i:<14} {s!r}")
print(f"\n  total flags: {tot}   (review these by hand; a figure owned by the fictional")
print("  organisation is fine, a figure attributed to Anthropic is not)")


# --------------------------------------------------------- 3. cross-batch overlap
head("3. NEAR-DUPLICATE STEMS ACROSS BATCHES  (22 batches wrote in parallel)")
def shingles(s, k=6):
    w = re.sub(r"[^a-z0-9 ]+", " ", s.lower()).split()
    return {" ".join(w[i:i + k]) for i in range(max(0, len(w) - k + 1))}

sh = {it["id"]: shingles(it["stem"]) for it in items}
dupes = []
ids = list(sh)
buckets = defaultdict(list)
for i in ids:
    for g in list(sh[i])[:24]:
        buckets[g].append(i)
seen = set()
for g, grp in buckets.items():
    if len(grp) < 2:
        continue
    for a in range(len(grp)):
        for b in range(a + 1, len(grp)):
            p = tuple(sorted((grp[a], grp[b])))
            if p in seen:
                continue
            seen.add(p)
            A, B = sh[p[0]], sh[p[1]]
            if not A or not B:
                continue
            j = len(A & B) / len(A | B)
            if j > 0.30:
                dupes.append((j, p[0], p[1]))
dupes.sort(reverse=True)
if dupes:
    print(f"  {len(dupes)} stem pair(s) above 30% shingle overlap:\n")
    for j, a, b in dupes[:SHOW * 2]:
        print(f"    {j:.0%}  {a} ({batch(by_id[a])})  <->  {b} ({batch(by_id[b])})")
        print(f"          {by_id[a]['stem'][:100]}…")
    nfails += len(dupes)
else:
    print("  none — batch scoping held")


# ------------------------------------------------------------- 4. absolute tells
head("4. ABSOLUTE-LANGUAGE TELL  (advisory)")
ABS = re.compile(r"\b(always|never|all|every|no)\b", re.I)
skew = 0
for it in items:
    if len(it["correct"]) != 1:
        continue
    ck = it["correct"][0]
    wrong_abs = sum(1 for o in it["options"] if o["key"] != ck and ABS.search(o["text"]))
    right_abs = 1 if ABS.search(next(o["text"] for o in it["options"] if o["key"] == ck)) else 0
    if wrong_abs == len(it["options"]) - 1 and not right_abs:
        skew += 1
print(f"  {skew} item(s) where EVERY distractor uses absolute language and the key does not.")
print("  On its own this is weak evidence; at scale it becomes a learnable pattern.")
if skew > len(items) * 0.06:
    print("  ^ above 6% of the bank — worth a look")


# --------------------------------------------------------------- 5. mix vs target
head("5. MIX AGAINST TARGET")
sc = sum(1 for i in items if len(i["stem"].split()) >= 45)
print(f"  scenario (stem >=45 words): {sc:,}  ({100*sc/len(items):.0f}%)   target 70%")
print(f"  recall    (stem < 45 words): {len(items)-sc:,}  ({100*(len(items)-sc)/len(items):.0f}%)   target 30%")
for lbl, key in (("difficulty", "difficulty"), ("type", "type")):
    c = Counter(i[key] for i in items)
    print(f"  {lbl}: " + "  ".join(f"{k}={v} ({100*v/len(items):.0f}%)" for k, v in c.most_common()))
kc = Counter(i["correct"][0] for i in items if len(i["correct"]) == 1)
t = sum(kc.values())
print("  key spread: " + "  ".join(f"{k}={100*kc[k]/t:.1f}%" for k in "ABCDE" if kc[k]))

per_dom = Counter(i["domain"] for i in items)
print("\n  per-domain recall share:")
for d in sorted(per_dom):
    dd = [i for i in items if i["domain"] == d]
    r = sum(1 for i in dd if len(i["stem"].split()) < 45)
    print(f"    {100*r/len(dd):>3.0f}% recall   {len(dd):>4} items   {d}")


head(f"DONE — {nfails} hard finding(s)")
sys.exit(0)
