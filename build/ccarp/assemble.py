#!/usr/bin/env python3
"""
Build the CCAR-P question bank into a single self-contained HTML file.

    python build/ccarp/assemble.py [--rebalance] [--quiet]

Reads every JSON array in build/ccarp/questions/ and build/ccarp/flashcards/,
validates each item hard, and writes 'Claude Certified Architect - Professional.html'.

Anything that fails validation is DROPPED and reported. A bank that silently ships a
broken item is worse than a smaller bank, because the candidate learns the wrong thing
and has no way to know.
"""
from __future__ import annotations
import json, re, sys, unicodedata
from collections import Counter, defaultdict
from difflib import SequenceMatcher
from pathlib import Path

ROOT  = Path(__file__).resolve().parent.parent.parent
HERE  = ROOT / "build" / "ccarp"
QDIR  = HERE / "questions"
FDIR  = HERE / "flashcards"
TMPL  = HERE / "template.html"
TENF  = HERE / "tenthings.json"
OUT   = ROOT / "Claude Certified Architect - Professional.html"

REBALANCE = "--rebalance" in sys.argv
QUIET     = "--quiet" in sys.argv

DOMAINS = {
    "Integration": 19,
    "Solution Design & Architecture": 17,
    "Evaluation, Testing & Optimisation": 16,
    "Governance, Safety & Risk Management": 14,
    "Stakeholder Communication & Lifecycle Management": 14,
    "Claude Models, Prompting & Context Engineering": 13,
    "Developer Productivity & Operational Enablement": 7,
}
DIFFS = {"easy", "medium", "hard"}
TYPES = {"single", "multi", "next-step"}
LETTERS = "ABCDE"

# Items withheld from the bank after blind adjudication. Every entry is a decision with
# a written reason, not a guess. An item with two defensible answers is worse than no
# item: it teaches a candidate to distrust their own correct reasoning.
QUARANTINE = {
    "DPO-A-039":
        "Two defensible answers. The stem demands that modification be 'structurally "
        "impossible rather than merely discouraged', and a read-only filesystem mount "
        "meets that test more completely than the recorded answer's permission mode "
        "plus deny rules — deny rules on file-writing tools would not stop a shell "
        "redirect. An independent verifier chose the mount at high confidence.",
    "ETO-D-026":
        "Two defensible analyses. The recorded answer (cross-score the cheap model on "
        "both paths) correctly breaks the router/capability confound, but the stem asks "
        "which analysis should precede the *category-migration decision*, and comparing "
        "the cheap path against the pre-routing baseline on those same categories "
        "prices that decision directly. Nothing in the stem separates them.",
}

# Authoring commentary that leaked into a JSON field. Every alternative below was seen
# for real in a previous build. Each is anchored tightly: a loose version of this regex
# threw out three good items on "actually is", "actually informed", and the wholly
# legitimate PII phrase "replace the identifier with a generic placeholder".
LEAK = re.compile(
    r"\bwait\s*[,—-]\s*(?:i\s|let me\b|actually\b)"
    r"|\blet me (?:reconsider|think|check|revise|rewrite)\b"
    r"|\bactually,?\s+(?:i|let)\s"
    r"|\bi need (?:this|[a-e]) to be\b"
    r"|\bi'?ll (?:make|pick|change) (?:this|that|it)\b"
    r"|\bi should (?:make|pick|choose)\b"
    r"|\bon second thought\b"
    r"|\bas an ai(?:\s+language)?\s+model\b|\bas an ai,?\s+i\b"
    r"|\btodo\s*[:)\]]|\bfixme\s*[:)\]]"
    r"|\blorem ipsum\b|\[insert\b",
    re.I)
# Every alternative above is anchored to first-person authorial voice, because the
# loose forms threw out good questions: "as an AI tool" is ordinary shadow-AI
# governance prose, and "asleep inside a backoff wait, the queue is growing" is an
# ordinary description of a retry storm.

# explanation.correct asserting a letter that is not the key. Case-SENSITIVE, or the
# article "a" matches and every third item gets flagged. Tightly bound to an explicit
# "the answer is X" construction so passing mentions of another option do not trip it.
CLAIMS = re.compile(r"\b(?:the answer|correct answer|the key)\s+(?:is|would be)\s+\(?(?-i:([A-E]))\b")

# an option that points at another option by letter — breaks under rebalancing.
# A bare "A and B" is deliberately not matched: "Tier A and B" and "Class A and B
# shares" are ordinary enterprise prose.
XREF = re.compile(r"\b(?:option|choice|answer)s?\s+(?-i:[A-E])\b"
                  r"|\b(?:both|either|neither)\s+(?-i:[A-E])\s+and\s+(?-i:[A-E])\b"
                  r"|^(?-i:[A-E])\s+and\s+(?-i:[A-E])\b"
                  r"|\bnone of the above\b|\ball of the above\b", re.I)

STUBS = {"", "tbd", "todo", "n/a", "na", "...", "…", "-", "—", "?"}

warn: list[str] = []
def W(m: str):
    warn.append(m)


# ---------------------------------------------------------------- loading

def demojibake(s: str) -> str:
    """Repair UTF-8 bytes that were decoded as cp1252 ('â€"' for an em dash)."""
    if not isinstance(s, str) or "Ã" not in s and "â" not in s:
        return s
    try:
        fixed = s.encode("cp1252", "strict").decode("utf-8", "strict")
        return fixed if fixed.count("\ufffd") == 0 else s
    except (UnicodeEncodeError, UnicodeDecodeError):
        return s


def deep_fix(o):
    if isinstance(o, str):
        return demojibake(o)
    if isinstance(o, list):
        return [deep_fix(x) for x in o]
    if isinstance(o, dict):
        return {k: deep_fix(v) for k, v in o.items()}
    return o


def repair_ctrl(txt: str) -> str:
    """Escape raw control characters sitting inside JSON string literals."""
    out, instr, esc = [], False, False
    for ch in txt:
        if esc:
            out.append(ch); esc = False; continue
        if ch == "\\" and instr:
            out.append(ch); esc = True; continue
        if ch == '"':
            instr = not instr
        if instr and ch in "\n\r\t":
            out.append({"\n": "\\n", "\r": "\\r", "\t": "\\t"}[ch]); continue
        out.append(ch)
    return "".join(out)


def salvage(txt: str) -> list:
    """Pull every complete top-level object out of a truncated/corrupt array."""
    items, depth, start, instr, esc = [], 0, None, False, False
    for i, ch in enumerate(txt):
        if esc:
            esc = False; continue
        if ch == "\\" and instr:
            esc = True; continue
        if ch == '"':
            instr = not instr; continue
        if instr:
            continue
        if ch == "{":
            if depth == 0:
                start = i
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth == 0 and start is not None:
                try:
                    items.append(json.loads(txt[start:i + 1]))
                except Exception:
                    pass
                start = None
    return items


def load(fp: Path) -> list:
    raw = fp.read_text(encoding="utf-8-sig")
    raw = re.sub(r"^\s*```(?:json)?\s*|\s*```\s*$", "", raw.strip())
    for attempt in (raw, repair_ctrl(raw)):
        try:
            d = json.loads(attempt)
            return deep_fix(d if isinstance(d, list) else d.get("items") or d.get("questions") or [])
        except Exception:
            continue
    got = deep_fix(salvage(raw))
    if got:
        W(f"{fp.name}: unparseable — salvaged {len(got)} complete item(s) from the wreckage")
    else:
        W(f"{fp.name}: UNPARSEABLE and nothing salvageable — 0 items")
    return got


# ---------------------------------------------------------------- validation

def norm(s: str) -> str:
    s = unicodedata.normalize("NFKD", str(s)).lower()
    return re.sub(r"[^a-z0-9]+", " ", s).strip()


def jaccard(a: str, b: str) -> float:
    A, B = set(norm(a).split()), set(norm(b).split())
    if not A or not B:
        return 0.0
    return len(A & B) / len(A | B)


def check(it, src: str) -> str | None:
    """Return a rejection reason, or None if the item is sound."""
    if not isinstance(it, dict):
        return "not an object"
    qid = it.get("id")
    if not isinstance(qid, str) or not qid.strip():
        return "missing id"
    if qid in QUARANTINE:
        return "QUARANTINED after adjudication: " + QUARANTINE[qid]

    for f in ("domain", "difficulty", "type", "stem", "options", "correct", "explanation"):
        if f not in it:
            return f"missing field '{f}'"
    if it["domain"] not in DOMAINS:
        return f"unknown domain {it['domain']!r}"
    if it["difficulty"] not in DIFFS:
        return f"bad difficulty {it['difficulty']!r}"
    if it["type"] not in TYPES:
        return f"bad type {it['type']!r}"

    stem = it["stem"]
    if not isinstance(stem, str) or len(stem.strip()) < 15:
        return "stem too short or not a string"

    opts = it["options"]
    if not isinstance(opts, list) or not 2 <= len(opts) <= 5:
        return f"needs 2-5 options, got {len(opts) if isinstance(opts, list) else '?'}"
    keys = []
    for o in opts:
        if not isinstance(o, dict) or "key" not in o or "text" not in o:
            return "malformed option"
        k = str(o["key"]).strip().upper()
        if k not in LETTERS:
            return f"bad option key {k!r}"
        if not str(o["text"]).strip():
            return f"option {k} has empty text"
        o["key"], o["text"] = k, str(o["text"]).strip()
        keys.append(k)
    if len(set(keys)) != len(keys):
        return "duplicate option keys"

    # normalise correct[] and confirm explanation is an object BEFORE any re-lettering,
    # otherwise the remap below iterates a bare string one character at a time
    cor = it["correct"]
    if isinstance(cor, str):
        cor = [cor]
    if not isinstance(cor, list):
        return "correct[] is not a list"
    it["correct"] = [str(c).strip().upper() for c in cor]
    if not isinstance(it.get("explanation"), dict):
        return "explanation is not an object"
    if not isinstance(it["explanation"].get("distractors"), dict):
        return "explanation.distractors missing"

    if keys != sorted(keys) or keys != list(LETTERS[:len(keys)]):
        # re-letter in the order given rather than throwing the item away
        if any(re.search(r"\b(?-i:[A-E])\b", str(v)) for v in
               [stem] + [o["text"] for o in opts]):
            return "option keys out of order and prose names letters — unsafe to re-letter"
        remap = {}
        for i, o in enumerate(opts):
            remap[o["key"]] = LETTERS[i]
            o["key"] = LETTERS[i]
        it["correct"] = [remap.get(c, c) for c in it["correct"]]
        d = it["explanation"].get("distractors") or {}
        it["explanation"]["distractors"] = {remap.get(k, k): v for k, v in d.items()}
        keys = [o["key"] for o in opts]

    cor = it["correct"]
    if not cor:
        return "no correct answer"
    if len(set(cor)) != len(cor):
        return "duplicate keys in correct[]"
    bad = [c for c in cor if c not in keys]
    if bad:
        return f"correct[] names non-existent option(s) {bad}"
    it["correct"] = cor

    if it["type"] in ("single", "next-step") and len(cor) != 1:
        return f"{it['type']} item has {len(cor)} correct answers"
    if it["type"] == "multi" and not 2 <= len(cor) <= 3:
        return f"multi item has {len(cor)} correct answers (want 2 or 3)"
    if len(cor) >= len(keys):
        return "every option is keyed correct"

    ex = it["explanation"]
    if not isinstance(ex, dict):
        return "explanation is not an object"
    for f in ("correct", "concept", "tip"):
        v = ex.get(f)
        if not isinstance(v, str) or norm(v) in STUBS or len(v.strip()) < 12:
            return f"explanation.{f} is missing or a stub"
    dis = ex.get("distractors")
    if not isinstance(dis, dict):
        return "explanation.distractors missing"
    dis = {str(k).strip().upper(): v for k, v in dis.items()}
    want = [k for k in keys if k not in cor]
    for k in want:
        v = dis.get(k)
        if not isinstance(v, str) or norm(v) in STUBS or len(v.strip()) < 12:
            return f"no usable distractor note for option {k}"
    for k in list(dis):
        if k in cor:
            del dis[k]           # a note on the correct option is harmless; drop it
        elif k not in keys:
            del dis[k]
    ex["distractors"] = dis

    blob = " ".join([stem, ex["correct"], ex["concept"], ex["tip"],
                     *[o["text"] for o in opts], *dis.values()])
    m = LEAK.search(blob)
    if m:
        return f"leaked authoring commentary: {m.group(0)!r}"

    if len(cor) == 1:
        for m in CLAIMS.finditer(ex["correct"]):
            if m.group(1) != cor[0]:
                return f"explanation.correct claims {m.group(1)} but key is {cor[0]}"

    for o in opts:
        m = XREF.search(o["text"])
        if m:
            return f"option {o['key']} references another option ({m.group(0)!r})"

    # Near-duplicate options. Word-set overlap alone is not enough: converse pairs like
    # "required calls that were made" vs "calls made that were required" — i.e. recall
    # vs precision — share almost every word while being the whole point of the item.
    # Only drop when the word ORDER also matches; otherwise warn and keep.
    for i in range(len(opts)):
        for j in range(i + 1, len(opts)):
            r = jaccard(opts[i]["text"], opts[j]["text"])
            if r <= 0.80:
                continue
            seq = SequenceMatcher(None, norm(opts[i]["text"]).split(),
                                  norm(opts[j]["text"]).split()).ratio()
            if seq > 0.75:
                return (f"options {opts[i]['key']}/{opts[j]['key']} are {int(r*100)}% "
                        f"identical (word order {int(seq*100)}% too)")
            W(f"{qid}: options {opts[i]['key']}/{opts[j]['key']} share {int(r*100)}% of "
              f"their words but differ in order — kept as a likely converse pair")

    it["topic"] = str(it.get("topic") or "").strip()
    it["_src"] = src
    return None


# ---------------------------------------------------------------- rebalance

def letter_ref(it) -> bool:
    """True if any prose names an option letter, making rotation unsafe."""
    blob = " ".join([it["stem"], it["explanation"]["correct"], it["explanation"]["concept"],
                     it["explanation"]["tip"], *it["explanation"]["distractors"].values()])
    return bool(re.search(r"\b(?:option|choice)\s+(?-i:[A-E])\b", blob, re.I))


def rotate(it, k: int):
    """Rotate option text among the letter slots. Content preserving."""
    opts = it["options"]
    n = len(opts)
    k %= n
    if not k:
        return
    texts = [o["text"] for o in opts]
    texts = texts[k:] + texts[:k]
    old_at = {o["key"]: o["text"] for o in opts}
    for i, o in enumerate(opts):
        o["text"] = texts[i]
    new_at = {o["key"]: o["text"] for o in opts}
    where = {v: kk for kk, v in new_at.items()}
    it["correct"] = sorted(where[old_at[c]] for c in it["correct"])
    it["explanation"]["distractors"] = {
        where[old_at[kk]]: v for kk, v in it["explanation"]["distractors"].items()
        if old_at.get(kk) in where
    }


def rebalance(items):
    """Even out the correct-key distribution without changing which text is true."""
    moved = 0
    for dom in {i["domain"] for i in items}:
        pool = [i for i in items
                if i["domain"] == dom and len(i["correct"]) == 1 and not letter_ref(i)]
        if len(pool) < 8:
            continue
        for it in pool:
            n = len(it["options"])
            counts = Counter(i["correct"][0] for i in items
                             if i["domain"] == dom and len(i["correct"]) == 1)
            cur = it["correct"][0]
            slots = list(LETTERS[:n])
            target = min(slots, key=lambda L: (counts[L], L))
            if counts[cur] - counts[target] < 2:
                continue
            before = it["correct"][0]
            rotate(it, (slots.index(cur) - slots.index(target)) % n)
            if it["correct"][0] != before:
                moved += 1
    return moved


# ---------------------------------------------------------------- main

def main() -> int:
    if not TMPL.exists():
        print("!! missing template:", TMPL); return 1
    if not QDIR.exists():
        print("!! no questions directory:", QDIR); return 1

    files = sorted(QDIR.glob("*.json"))
    if not files:
        print("!! no question files yet in", QDIR); return 1

    raw, dropped = [], []
    for fp in files:
        got = load(fp)
        if not got:
            continue
        for it in got:
            r = check(it, fp.name)
            (dropped.append((fp.name, it.get("id", "?"), r)) if r else raw.append(it))

    # de-duplicate ids (last file wins) and identical stems (first wins)
    by_id, dup_id = {}, 0
    for it in raw:
        if it["id"] in by_id:
            dup_id += 1
        by_id[it["id"]] = it
    items, seen_stem, dup_stem = [], {}, 0
    for it in sorted(by_id.values(), key=lambda x: x["id"]):
        fp = norm(it["stem"])[:400]
        if fp in seen_stem:
            dup_stem += 1
            dropped.append((it["_src"], it["id"], f"duplicate stem of {seen_stem[fp]}"))
            continue
        seen_stem[fp] = it["id"]
        items.append(it)

    # cross-item contradiction: same stem, different key — caught above by stem dedupe,
    # but near-identical stems with different keys are worth surfacing
    stem_keys = defaultdict(set)
    for it in items:
        stem_keys[norm(it["stem"])[:180]].add("".join(it["correct"]))
    for s, ks in stem_keys.items():
        if len(ks) > 1:
            W(f"near-identical stems disagree on the key: {sorted(ks)} — {s[:70]}…")

    moved = rebalance(items) if REBALANCE else 0

    # flashcards
    cards = []
    if FDIR.exists():
        for fp in sorted(FDIR.glob("*.json")):
            for c in load(fp):
                if not isinstance(c, dict):
                    continue
                if not (str(c.get("front", "")).strip() and str(c.get("back", "")).strip()):
                    continue
                if c.get("domain") not in DOMAINS:
                    continue
                cards.append({k: c.get(k) for k in
                              ("id", "domain", "topic", "difficulty", "front", "back", "hook")})
    # Two statements, not a tuple assignment: in `a, b = set(), [... uses a ...]`
    # the right-hand side is evaluated before either name is bound, so the
    # comprehension would reference `seenc` before it exists.
    seenc: set[str] = set()
    deduped = []
    for c in cards:
        fp = norm(c["front"])
        if fp in seenc:
            continue
        seenc.add(fp)
        deduped.append(c)
    cards = deduped

    ten = json.loads(TENF.read_text(encoding="utf-8-sig")) if TENF.exists() else {}

    for it in items:
        it.pop("_src", None)

    meta = {
        "exam": "CCAR-P", "items": 63, "minutes": 120, "pass": 720,
        "weights": DOMAINS, "total": len(items), "cards": len(cards),
    }

    def emb(o):
        # never let a literal </script> or a lone surrogate break the page
        return (json.dumps(o, ensure_ascii=False, separators=(",", ":"))
                .replace("</", "<\\/").replace("\u2028", "\\u2028").replace("\u2029", "\\u2029"))

    html = TMPL.read_text(encoding="utf-8")
    for tok, val in (("@@QUESTIONS@@", items), ("@@FLASHCARDS@@", cards),
                     ("@@TENTHINGS@@", ten), ("@@META@@", meta)):
        if tok not in html:
            print("!! template is missing placeholder", tok); return 1
        html = html.replace(tok, emb(val))
    OUT.write_text(html, encoding="utf-8")

    # ------------------------------------------------------------ report
    if not QUIET:
        print(f"\nfiles read        {len(files)}")
        print(f"items accepted    {len(items):,}")
        print(f"items dropped     {len(dropped):,}")
        if dup_id:
            print(f"  (ids superseded across files: {dup_id})")
        if dropped:
            why = Counter(re.sub(r"[A-E'\"].*", "…", r) for _, _, r in dropped)
            print("\n  drop reasons:")
            for r, n in why.most_common(14):
                print(f"    {n:>4}  {r}")
            print("\n  first 12 dropped:")
            for f, i, r in dropped[:12]:
                print(f"    {i:<14} {f:<18} {r}")

        print(f"\nflashcards        {len(cards):,}")
        if moved:
            print(f"rebalanced        {moved} item(s) rotated to even out the key spread")

        print("\nby domain (target vs actual share):")
        dc = Counter(i["domain"] for i in items)
        for d, wgt in sorted(DOMAINS.items(), key=lambda kv: -kv[1]):
            n = dc.get(d, 0)
            share = 100 * n / max(1, len(items))
            flag = "  <-- thin" if share < wgt - 4 else ""
            print(f"   {n:>5}  {share:5.1f}%  (target {wgt:>2}%)  {d}{flag}")

        for label, key in (("difficulty", "difficulty"), ("type", "type")):
            c = Counter(i[key] for i in items)
            tot = sum(c.values()) or 1
            print(f"\nby {label}: " + "  ".join(
                f"{k}={v} ({100*v/tot:.0f}%)" for k, v in c.most_common()))

        kc = Counter(i["correct"][0] for i in items if len(i["correct"]) == 1)
        tot = sum(kc.values()) or 1
        print("\nkey spread (single-answer): " + "  ".join(
            f"{k}={100*kc[k]/tot:.1f}%" for k in LETTERS if kc[k]))

        # Answer-length tell. Reported on every build because it is invisible to any
        # single authoring batch and silently makes the bank scoreable without
        # knowledge: at 85% a candidate can just pick the longest option.
        sing = [i for i in items if len(i["correct"]) == 1]
        longest = sum(1 for i in sing
                      if len(next(o["text"] for o in i["options"] if o["key"] == i["correct"][0]))
                      == max(len(o["text"]) for o in i["options"]))
        pct = 100 * longest / max(1, len(sing))
        verdict = ("OK" if pct < 35 else "LEANING — worth a look" if pct < 45
                   else "*** DEFECT: the bank is scoreable by picking the longest option ***")
        print(f"answer-length tell: key is longest in {pct:.0f}% of {len(sing):,} "
              f"single-answer items (chance 25%)  -> {verdict}")

        print(f"\ntopics distinct   {len({i['topic'] for i in items if i['topic']}):,}")
        print(f"full 63-item mocks {len(items)//63}")

        if warn:
            print(f"\n{len(warn)} warning(s):")
            for w in warn[:20]:
                print("   -", w)

    size = OUT.stat().st_size
    print(f"\n-> {OUT.name}   {size/1e6:.1f} MB   {len(items):,} questions   {len(cards):,} cards")
    return 0


if __name__ == "__main__":
    sys.exit(main())
