#!/usr/bin/env python3
"""
Assemble every build/questions/*.json batch into one standalone HTML question bank.

Usage:  python build/assemble.py
Output: CCAO-F_Question_Bank.html   (single file, no external dependencies)

Hard-invalid items are dropped and reported. Soft issues are warned about but kept.
"""
from __future__ import annotations
import hashlib, json, re, sys, unicodedata
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
QDIR = ROOT / "build" / "questions"
CDIR = ROOT / "build" / "flashcards"
TPL  = ROOT / "build" / "template.html"
OUT  = ROOT / "CCAO-F_Question_Bank.html"

DOMAINS = {
    "Output Evaluation and Validation",
    "Workflow Integration and Solution Design",
    "Governance, Risk, and Responsible Use",
    "Prompting and Task Execution",
    "Product and Model Selection",
    "Configuration and Knowledge Management",
    "Troubleshooting and Optimisation",
    "Technical Awareness",
}
DIFFS = {"easy", "medium", "hard"}
TYPES = {"single", "multi", "nextstep"}
KEYS  = ["A", "B", "C", "D", "E"]

META = {
    "built": datetime.now().strftime("%d %B %Y"),
    "examItems": 60, "examMinutes": 120,
    "passMark": 720, "scaleMin": 100, "scaleMax": 1000,
}


VERDICTS = ROOT / "build" / "verdicts.json"


def stem_fp(it) -> str:
    """Short fingerprint of an item's stem, used to bind a verdict to content."""
    return hashlib.sha1(norm(it.get("stem", "")).encode("utf-8")).hexdigest()[:12]


def load_verdicts():
    """Adjudicated decisions: items to drop, and answers to correct.

    An entry may be a bare reason string (applies to the id unconditionally) or
    an object with a `stem_sha`. The hash matters: authoring agents sometimes
    rewrite a whole batch file, so an id can come to hold a completely different
    question. Without content binding, a verdict made about the old item would
    silently delete the new one.
    """
    if not VERDICTS.exists():
        return {}, {}
    try:
        v = json.loads(VERDICTS.read_text(encoding="utf-8-sig"))
    except Exception as ex:
        print(f"!! verdicts.json is unreadable ({ex}) — proceeding without it")
        return {}, {}
    q = {}
    for k, r in (v.get("quarantine") or {}).items():
        if k.startswith("_"):
            continue
        q[k] = ({"reason": str(r), "stem_sha": None} if isinstance(r, str)
                else {"reason": str(r.get("reason", "")), "stem_sha": r.get("stem_sha")})
    rk = {k: d for k, d in (v.get("rekey") or {}).items() if not k.startswith("_")}
    return q, rk


def norm(s: str) -> str:
    """Normalise a stem for duplicate detection."""
    s = unicodedata.normalize("NFKD", str(s)).lower()
    return re.sub(r"[^a-z0-9]+", " ", s).strip()


# Telltale byte pairs left when UTF-8 text is decoded as cp1252 — an em dash
# (E2 80 94) arrives as the three characters "â€”", and so on.
MOJI_MARKERS = ("â€", "Ã¢", "Ã©", "Ã¨", "Ã¡", "Ã­", "Ã³", "Ãº", "Ã±", "Ã ",
                "Â ", "Â·", "Â«", "Â»", "Â½", "Ââ")


def demojibake(s: str) -> str:
    """Undo one or two rounds of UTF-8-as-cp1252 mis-decoding.

    Only fires when a known mojibake marker is present, and only keeps the
    result if the round-trip succeeds cleanly — so correctly-encoded text
    (including legitimate accented characters) is left untouched.
    """
    for _ in range(2):
        if not any(m in s for m in MOJI_MARKERS):
            break
        try:
            s = s.encode("cp1252", errors="strict").decode("utf-8", errors="strict")
        except (UnicodeEncodeError, UnicodeDecodeError):
            break
    return s


def clean(s):
    """Repair mojibake and strip control characters that would corrupt the HTML."""
    if not isinstance(s, str):
        return s
    s = demojibake(s)
    return "".join(c for c in s if c in "\t\n" or (ord(c) >= 32 and ord(c) != 0x7F))


# Authoring agents that lose the thread sometimes leak their own reasoning into
# the content. Any item containing this must never reach the study bank.
LEAK = re.compile(
    r"let me (rethink|redesign|reconsider|revise|rework|adjust|fix|change|try|compose|write|draft)"
    r"|let's (rethink|redesign|reconsider|try again)"
    # "Wait" used as a self-correction interjection: followed by a dash, or by a
    # pivoting word. Deliberately does NOT match "wait time", "wait-list",
    # "wait for approval", which are ordinary prose.
    r"|\bwait\b(\s*[—–]|\s+-\s|[\s,.]+(i|let|actually|no|that|the|so)\b)"
    r"|let me (recalculate|recompute|double-check|re-?check|verify that)"
    r"|\bscratch that\b|\bhold on\b|\bi mis(calculated|read|counted)\b"
    r"|\bcorrection:\s"
    r"|i need [a-e] to be"
    r"|now [a-e] (is|becomes) the correct answer"
    r"|needs? to be the correct answer"
    r"|and makes logical sense"
    r"|(actually|hmm)[\s,]+(let me|i should|i need|that)"
    r"|on second thought"
    r"|as an ai (language )?model"
    r"|\bTODO\b|\bFIXME\b|\blorem ipsum\b",
    re.I,
)

# A field left entirely unfilled. Must match the WHOLE value — words like
# "placeholder" are perfectly legitimate inside real prose ("Claude returned a
# generic one-paragraph placeholder"), so only a bare stub counts.
STUB = re.compile(
    r"^\W*(placeholder|tbd|todo|to do|n/?a|none|null|xxx+|\[insert[^\]]*\]|[-.—]+)\W*$",
    re.I,
)


def stub_fields(it):
    """Names of fields that were left as unfilled stubs or are uselessly short."""
    bad = []
    if STUB.match(str(it.get("stem", "")).strip()):
        bad.append("stem")
    for o in it.get("options") or []:
        if isinstance(o, dict) and STUB.match(str(o.get("text", "")).strip()):
            bad.append(f"option {o.get('key')}")
    e = it.get("explanation")
    if isinstance(e, dict):
        for k in ("correct", "concept", "examTip"):
            v = str(e.get(k, "")).strip()
            if v and (STUB.match(v) or len(v) < 20):
                bad.append(f"explanation.{k}")
        d = e.get("distractors")
        if isinstance(d, dict):
            for k, v in d.items():
                s = str(v).strip()
                if s and (STUB.match(s) or len(s) < 20):
                    bad.append(f"distractors.{k}")
    return bad


# An explanation that names a different option letter than the recorded key means
# the item is mis-keyed. That is the most damaging defect possible in a study
# bank, so it is caught structurally rather than trusted to the author.
# The option letter is matched case-SENSITIVELY. Without that, a lowercase "a"
# matches [A-E] under re.I and prose like "the correct answer is a specific
# value" gets misread as naming option A.
CLAIMS_KEY = re.compile(
    r"(?:correct answer(?:\s+\w+)?\s+(?:is|should be|would be)"
    r"|the answer\s+(?:is|should be)"
    r"|correct key\s+(?:is|should be))\s*\(?(?-i:([A-E]))(?![a-z])\b"
    r"|(?-i:\b([A-E]))(?![a-z])\s+is\s+(?:clearly\s+|actually\s+|definitely\s+)?"
    r"(?:the\s+)?(?:most\s+)?correct(?:\s+answer)?\b",
    re.I,
)


def miskeyed(it) -> str | None:
    """Flag items whose explanation names an option letter other than the key."""
    e = it.get("explanation") or {}
    if not isinstance(e, dict):
        return None
    cor = {str(k).upper() for k in (it.get("correct") or [])}
    if not cor:
        return None
    for m in CLAIMS_KEY.finditer(str(e.get("correct", ""))):
        letter = (m.group(1) or m.group(2) or "").upper()
        if letter and letter not in cor:
            return (f"explanation asserts {letter} is correct, "
                    f"but key is {'+'.join(sorted(cor))}")
    return None


def leaked(it) -> str | None:
    """Return the offending snippet if authoring commentary leaked into an item."""
    parts = [str(it.get("stem", ""))]
    for o in it.get("options") or []:
        if isinstance(o, dict):
            parts.append(str(o.get("text", "")))
    e = it.get("explanation")
    if isinstance(e, dict):
        parts += [str(e.get(k, "")) for k in ("correct", "concept", "examTip")]
        d = e.get("distractors")
        if isinstance(d, dict):
            parts += [str(v) for v in d.values()]
    for p in parts:
        m = LEAK.search(p)
        if m:
            return m.group(0)[:60]
    return None


def repair_json(txt: str) -> str:
    """
    Escape raw control characters that appear inside JSON string literals.

    Authoring agents occasionally emit a literal newline inside a string instead
    of \\n, which makes the whole file unparseable and would cost us the entire
    batch. Walk the text tracking string/escape state and fix only what is
    genuinely inside a string.
    """
    out, in_str, esc = [], False, False
    for ch in txt:
        if not in_str:
            out.append(ch)
            if ch == '"':
                in_str = True
            continue
        if esc:
            out.append(ch)
            esc = False
            continue
        if ch == "\\":
            out.append(ch)
            esc = True
            continue
        if ch == '"':
            out.append(ch)
            in_str = False
            continue
        if ch == "\n":
            out.append("\\n")
        elif ch == "\r":
            out.append("\\r")
        elif ch == "\t":
            out.append("\\t")
        elif ord(ch) < 0x20 or ord(ch) == 0x7F:
            pass                      # drop other control characters
        else:
            out.append(ch)
    return "".join(out)


def repair_schema_typos(txt: str) -> str:
    """Fix a recurring authoring typo that makes a whole file unparseable.

    Agents sometimes write a comma where the distractors object needs a colon:

        "distractors": { "A", "Chain-of-thought and tone do not conflict..."
        "distractors": { "A", "text": "Model tier is a product decision..."

    instead of `"A": "..."`. One occurrence kills the file, costing ~20 items.

    The length guard matters: `"A", "` is perfectly valid inside an array such as
    `"correct": ["A", "C"]`, so only rewrite when the following string is long
    enough to be an explanation rather than an option letter.

    Anchoring is equally essential. The letter must directly follow `{` or `,` —
    i.e. it sits in a key position inside an object. Without that anchor the
    pattern also matches the legitimate option shape `"key": "A", "text": "..."`
    and corrupts every option in the file.
    """
    # "A", "C": "shared explanation"   ->   "A": "shared explanation", "C": "shared explanation"
    # The agent merged two distractor keys onto one entry. The text discusses both
    # letters, so giving each key a copy is faithful and keeps distractor coverage
    # complete (validate requires an entry per non-correct option).
    txt = re.sub(r'([{,]\s*)"([A-E])",\s*"([A-E])"\s*:\s*"((?:[^"\\]|\\.)*)"',
                 r'\1"\2": "\4", "\3": "\4"', txt)
    # "A", "text": "..."   ->   "A": "..."
    txt = re.sub(r'([{,]\s*)"([A-E])",\s*"text"\s*:\s*"', r'\1"\2": "', txt)
    # "A", "long explanation ..."   ->   "A": "long explanation ..."
    # The length guard keeps arrays like ["A", "C"] out of scope.
    txt = re.sub(r'([{,]\s*)"([A-E])",\s*"(?=[^"\\]{25,})', r'\1"\2": "', txt)
    return txt


def salvage_array(txt: str):
    """Pull as many complete top-level objects out of a broken JSON array as possible.

    Used when an authoring agent truncated a file or corrupted it partway
    through — the items written before the breakage are still perfectly good.
    """
    dec = json.JSONDecoder()
    i = txt.find("[")
    if i < 0:
        return []
    i += 1
    items, n = [], len(txt)
    while i < n:
        while i < n and txt[i] in " \t\r\n,":
            i += 1
        if i >= n or txt[i] == "]":
            break
        try:
            obj, i = dec.raw_decode(txt, i)
        except json.JSONDecodeError:
            break
        items.append(obj)
    return items


def read_json(fp):
    """Parse a batch file, repairing then salvaging as needed.

    Returns (data, note) where note is None or a warning string.
    """
    txt = fp.read_text(encoding="utf-8-sig")
    try:
        return json.loads(txt), None
    except json.JSONDecodeError as first:
        fixed = repair_json(txt)
        try:
            return json.loads(fixed), (
                f"{fp.name}  had unescaped control characters — repaired ({first.msg})")
        except json.JSONDecodeError:
            pass
        typo_fixed = repair_schema_typos(fixed)
        if typo_fixed != fixed:
            try:
                return json.loads(typo_fixed), (
                    f"{fp.name}  had comma-for-colon typos in distractors — repaired "
                    f"({first.msg})")
            except json.JSONDecodeError:
                fixed = typo_fixed      # partial improvement; let salvage try it
        rescued = salvage_array(fixed)
        if rescued:
            return rescued, (f"{fp.name}  is corrupt ({first.msg}) — "
                             f"salvaged the first {len(rescued)} complete item(s)")
        raise first


LETTER_IN_PROSE = re.compile(
    r"(?<![A-Za-z])(?:option\s+)?[A-E](?![a-z])\s+(?:is|are|would|fails?|"
    r"describes?|addresses?|offers?|correctly|incorrectly)")


def has_letter_refs(item) -> bool:
    """True if the item's prose names option letters, making reordering unsafe."""
    e = item.get("explanation")
    if not isinstance(e, dict):
        return False
    prose = " ".join(str(e.get(k, "")) for k in ("correct", "concept", "examTip"))
    if isinstance(e.get("distractors"), dict):
        prose += " " + " ".join(str(v) for v in e["distractors"].values())
    for o in item.get("options") or []:
        prose += " " + str(o.get("text", ""))
    return bool(LETTER_IN_PROSE.search(prose))


def move_key(item, target: str) -> bool:
    """Swap option payloads so the correct answer sits at `target`.

    Content-preserving: the text that was correct is still correct, it just
    occupies a different letter. Only valid for single-answer items whose prose
    never names an option letter — callers must check has_letter_refs first.
    """
    opts = item.get("options") or []
    keys = [o.get("key") for o in opts]
    if keys != KEYS[:len(opts)] or len(item.get("correct") or []) != 1:
        return False
    k = item["correct"][0]
    if k == target or target not in keys:
        return False
    i, j = keys.index(k), keys.index(target)
    opts[i]["text"], opts[j]["text"] = opts[j]["text"], opts[i]["text"]
    item["correct"] = [target]
    e = item.get("explanation")
    if isinstance(e, dict) and isinstance(e.get("distractors"), dict):
        d = e["distractors"]
        moved = d.get(target)          # the distractor that used to sit at target
        d.pop(target, None)            # target is now the correct answer
        if moved is not None:
            d[k] = moved               # ...and now sits where the key used to be
        else:
            d.pop(k, None)
    return True


def rebalance(items, warns) -> int:
    """Reduce per-batch positional bias by rotating options.

    Some authoring agents drifted into keying half a batch to the same letter,
    which teaches "when unsure, pick B". Rotating is safe where no prose names a
    letter; items that do reference letters are left alone.

    Off by default: this changes which letter is correct, so it must not run
    while a blind verification pass is mid-flight against the old arrangement.
    """
    batches = defaultdict(list)
    for it in items:
        batches[it["id"].rsplit("-", 1)[0]].append(it)
    moved = 0
    for b, grp in sorted(batches.items()):
        singles = [i for i in grp
                   if i.get("type") in ("single", "nextstep") and len(i.get("correct") or []) == 1]
        if len(singles) < 12:
            continue
        for _ in range(len(singles)):
            kc = Counter(i["correct"][0] for i in singles)
            top, n = kc.most_common(1)[0]
            if n / len(singles) <= 0.32:
                break
            target = min("ABCD", key=lambda x: kc.get(x, 0))
            cand = next((i for i in sorted(singles, key=lambda x: x["id"])
                         if i["correct"][0] == top and not has_letter_refs(i)), None)
            if cand is None or not move_key(cand, target):
                warns.append(f"{b}: {100*n/len(singles):.0f}% keyed {top} but no further item "
                             f"can be rotated safely (prose names option letters)")
                break
            moved += 1
    return moved


def apply_rekey(item, verdict):
    """Change an item's recorded answer and repair the explanation to match.

    Swapping `correct` alone silently breaks the item two ways:
      * the previously-correct option becomes a distractor with no distractor
        explanation, so validate() rejects the whole item and it is dropped;
      * `explanation.correct` still argues for the old letter, which would teach
        the reader the wrong thing.

    The adjudicator's reasoning is exactly the missing material: it says why the
    new key is right and, implicitly, why the old one was not. Use it for both.
    """
    old = [str(k).upper() for k in (item.get("correct") or [])]
    new = [str(k).upper() for k in verdict["correct"]]
    why = str(verdict.get("why", "")).strip() or "Adjudicated correction."
    item["correct"] = list(new)

    e = item.setdefault("explanation", {})
    if not isinstance(e, dict):
        return item
    d = e.setdefault("distractors", {})
    if isinstance(d, dict):
        for k in new:
            d.pop(k, None)                       # now correct, needs no distractor note
        for k in old:
            if k not in new and not str(d.get(k, "")).strip():
                d[k] = (f"This was originally recorded as the answer. On review it is "
                        f"not correct: {why}")
    e["correct"] = (f"**Adjudicated correction — the answer is "
                    f"{'+'.join(new)}.** {why}\n\n"
                    f"The original rationale is kept below for context, but it was "
                    f"written for a different key and should be read critically.\n\n"
                    + str(e.get("correct", "")))
    return item


def renumber_options(item):
    """Re-letter options to match their display order.

    Agents told to fix a key skew by reordering options sometimes move the
    option text but leave the old letters attached, yielding keys like
    [A, C, B, D, E]. Array order is what the UI renders, so relabel by position
    and remap `correct` and the distractor explanations to match.
    """
    opts = item.get("options")
    if not isinstance(opts, list) or not opts:
        return item
    keys = [o.get("key") for o in opts if isinstance(o, dict)]
    want = KEYS[:len(opts)]
    if keys == want or sorted(keys) != sorted(want):
        return item                      # already fine, or too broken to fix safely

    # If the explanation prose names option letters, renumbering would silently
    # invalidate those references ("unlike C, ..."). Remapping the `correct` list
    # is not enough. Leave such an item alone and let the audit flag it instead.
    e = item.get("explanation")
    if isinstance(e, dict):
        prose = " ".join(str(e.get(k, "")) for k in ("correct", "concept", "examTip"))
        if isinstance(e.get("distractors"), dict):
            prose += " " + " ".join(str(v) for v in e["distractors"].values())
        if re.search(r"(?<![A-Za-z])(?:option\s+)?[A-E](?![a-z])\s+(?:is|are|would|fails?|"
                     r"describes?|addresses?|offers?)", prose):
            return item
    remap = dict(zip(keys, want))
    for o, new in zip(opts, want):
        o["key"] = new
    item["correct"] = [remap.get(c, c) for c in item.get("correct") or []]
    e = item.get("explanation")
    if isinstance(e, dict) and isinstance(e.get("distractors"), dict):
        e["distractors"] = {remap.get(k, k): v for k, v in e["distractors"].items()}
    return item


def scrub(item):
    for k, v in list(item.items()):
        if isinstance(v, str):
            item[k] = clean(v)
    for o in item.get("options", []) or []:
        if isinstance(o, dict):
            for k, v in list(o.items()):
                if isinstance(v, str):
                    o[k] = clean(v)
    e = item.get("explanation")
    if isinstance(e, dict):
        for k, v in list(e.items()):
            if isinstance(v, str):
                e[k] = clean(v)
        d = e.get("distractors")
        if isinstance(d, dict):
            for k, v in list(d.items()):
                if isinstance(v, str):
                    d[k] = clean(v)

    renumber_options(item)

    # Always surface the "choose N" cue on multi-select stems — the real exam
    # states it, and without it the item reads as a broken single-answer question.
    if item.get("type") == "multi" and isinstance(item.get("stem"), str):
        n = len(item.get("correct") or [])
        if n in (2, 3) and not re.search(r"\(choose (two|three)\)", item["stem"], re.I):
            item["stem"] = item["stem"].rstrip() + (" (Choose TWO)" if n == 2 else " (Choose THREE)")
    return item


def validate(it, src):
    """Return (hard_errors, soft_warnings)."""
    E, W = [], []
    tag = f"{src}:{it.get('id', '?')}"

    for f in ("id", "domain", "topic", "difficulty", "type", "stem", "options",
              "correct", "explanation"):
        if not it.get(f):
            E.append(f"{tag}  missing field '{f}'")
    if E:
        return E, W

    lk = leaked(it)
    if lk:
        E.append(f"{tag}  leaked authoring commentary: {lk!r}")
        return E, W
    st = stub_fields(it)
    if st:
        E.append(f"{tag}  unfilled/stub field(s): {', '.join(st[:5])}")
        return E, W
    mk = miskeyed(it)
    if mk:
        E.append(f"{tag}  MIS-KEYED: {mk}")
        return E, W

    if it["domain"] not in DOMAINS:
        E.append(f"{tag}  unknown domain {it['domain']!r}")
    if it["difficulty"] not in DIFFS:
        E.append(f"{tag}  bad difficulty {it['difficulty']!r}")
    if it["type"] not in TYPES:
        E.append(f"{tag}  bad type {it['type']!r}")

    opts = it["options"]
    if not isinstance(opts, list) or not (4 <= len(opts) <= 5):
        E.append(f"{tag}  needs 4-5 options, has {len(opts) if isinstance(opts, list) else '?'}")
        return E, W
    ks = [o.get("key") for o in opts]
    if ks != KEYS[:len(ks)]:
        # Correctness is preserved as long as `correct` points at real keys, so
        # this is a display-order blemish rather than a reason to bin the item.
        if sorted(ks) == sorted(KEYS[:len(ks)]):
            W.append(f"{tag}  option keys out of display order: {ks}")
        else:
            E.append(f"{tag}  option keys must be A..{KEYS[len(ks)-1]}, got {ks}")
    if any(not str(o.get("text", "")).strip() for o in opts):
        E.append(f"{tag}  has an empty option")

    cor = it["correct"]
    if not isinstance(cor, list) or not cor:
        E.append(f"{tag}  'correct' must be a non-empty list")
        return E, W
    if any(c not in ks for c in cor):
        E.append(f"{tag}  correct {cor} not a subset of {ks}")
    if len(set(cor)) != len(cor):
        E.append(f"{tag}  duplicate keys in correct {cor}")
    if it["type"] in ("single", "nextstep") and len(cor) != 1:
        E.append(f"{tag}  type {it['type']} needs exactly 1 correct, has {len(cor)}")
    if it["type"] == "multi" and len(cor) not in (2, 3):
        E.append(f"{tag}  type multi needs 2-3 correct, has {len(cor)}")

    ex = it["explanation"]
    if not isinstance(ex, dict):
        E.append(f"{tag}  explanation must be an object")
        return E, W
    if not str(ex.get("correct", "")).strip():
        E.append(f"{tag}  explanation.correct is empty")
    d = ex.get("distractors") or {}
    for k in ks:
        if k in cor:
            continue
        if not str(d.get(k, "")).strip():
            E.append(f"{tag}  no distractor explanation for option {k}")

    # ---- soft ----
    if not str(ex.get("concept", "")).strip():
        W.append(f"{tag}  no concept refresher")
    if not str(ex.get("examTip", "")).strip():
        W.append(f"{tag}  no exam tip")
    if it["type"] == "multi" and not re.search(r"\(choose (two|three)\)", it["stem"], re.I):
        W.append(f"{tag}  multi stem lacks '(Choose TWO/THREE)'")
    if len(str(it["stem"]).split()) < 18:
        W.append(f"{tag}  stem very short ({len(str(it['stem']).split())} words)")
    lens = [len(str(o['text'])) for o in opts]
    if max(lens) > 2.6 * max(1, min(lens)):
        W.append(f"{tag}  option lengths uneven {lens}")
    if re.search(r"claude\s+[0-9]", it["stem"], re.I) or \
       re.search(r"claude-(opus|sonnet|haiku)-[0-9]", json.dumps(it), re.I):
        W.append(f"{tag}  references a specific model version")
    return E, W


def validate_card(c, src):
    """Return (hard_errors, soft_warnings) for one flashcard."""
    E, W = [], []
    tag = f"{src}:{c.get('id', '?')}"
    for f in ("id", "domain", "topic", "difficulty", "front", "back"):
        if not str(c.get(f, "")).strip():
            E.append(f"{tag}  missing field '{f}'")
    if E:
        return E, W
    blob = " ".join(str(c.get(k, "")) for k in ("front", "back", "hook"))
    m = LEAK.search(blob)
    if m:
        E.append(f"{tag}  leaked authoring commentary: {m.group(0)[:60]!r}")
        return E, W

    if c["domain"] not in DOMAINS:
        E.append(f"{tag}  unknown domain {c['domain']!r}")
    if c["difficulty"] not in DIFFS:
        E.append(f"{tag}  bad difficulty {c['difficulty']!r}")

    fw, bw = len(c["front"].split()), len(c["back"].split())
    if fw > 40:
        W.append(f"{tag}  front is long ({fw} words)")
    if bw < 35:
        W.append(f"{tag}  back is thin ({bw} words)")
    if bw > 190:
        W.append(f"{tag}  back is long ({bw} words)")
    if not str(c.get("hook", "")).strip():
        W.append(f"{tag}  no hook line")
    elif len(c["hook"].split()) > 32:
        W.append(f"{tag}  hook exceeds ~25 words")
    return E, W


def load_cards():
    """Load, validate and de-duplicate the flashcard deck."""
    cards, errors, warns, per_file = [], [], [], {}
    seen_ids, seen_fronts = {}, {}
    for fp in sorted(CDIR.glob("*.json")):
        try:
            data, note = read_json(fp)
            if note:
                warns.append(note)
        except Exception as ex:
            errors.append(f"{fp.name}  UNPARSEABLE: {ex}")
            per_file[fp.stem] = 0
            continue
        if not isinstance(data, list):
            errors.append(f"{fp.name}  top level is {type(data).__name__}, expected list")
            per_file[fp.stem] = 0
            continue
        kept = 0
        for c in data:
            if not isinstance(c, dict):
                errors.append(f"{fp.name}  non-object entry")
                continue
            for k, v in list(c.items()):
                if isinstance(v, str):
                    c[k] = clean(v)
            E, W = validate_card(c, fp.stem)
            warns += W
            if E:
                errors += E
                continue
            if c["id"] in seen_ids:
                errors.append(f"{fp.stem}:{c['id']}  duplicate id")
                continue
            n = norm(c["front"])
            if n in seen_fronts:
                warns.append(f"{fp.stem}:{c['id']}  duplicate front of {seen_fronts[n]} — dropped")
                continue
            seen_ids[c["id"]] = fp.stem
            seen_fronts[n] = c["id"]
            cards.append(c)
            kept += 1
        per_file[fp.stem] = kept
    return cards, errors, warns, per_file


def main() -> int:
    # Oldest first: when an agent rewrites a truncated batch as -pN chunks, the
    # newer files share item ids with the stale original. Processing in mtime
    # order and letting later files win keeps the rewrite, not the leftover.
    files = sorted(QDIR.glob("*.json"), key=lambda p: (p.stat().st_mtime, p.name))
    if not files:
        print(f"!! no JSON batches found in {QDIR}")
        return 1

    errors, warns = [], []
    by_id, id_src, superseded = {}, {}, []
    per_file = {}
    quarantine, rekey = load_verdicts()
    dropped_by_verdict, rekeyed, stale_verdicts = [], [], []

    for fp in files:
        try:
            data, note = read_json(fp)
            if note:
                warns.append(note)
        except Exception as ex:
            errors.append(f"{fp.name}  UNPARSEABLE: {ex}")
            per_file[fp.stem] = 0
            continue
        if not isinstance(data, list):
            errors.append(f"{fp.name}  top level is {type(data).__name__}, expected list")
            per_file[fp.stem] = 0
            continue

        kept = 0
        for it in data:
            if not isinstance(it, dict):
                errors.append(f"{fp.name}  non-object entry")
                continue
            it = scrub(it)
            E, W = validate(it, fp.stem)
            warns += W
            if E:
                errors += E
                continue
            qid = it["id"]
            if qid in by_id:
                superseded.append(f"{qid} ({id_src[qid]} -> {fp.stem})")
            by_id[qid] = it
            id_src[qid] = fp.stem
            kept += 1
        per_file[fp.stem] = kept

    # Apply adjudicated verdicts only AFTER duplicate ids are resolved. An id can
    # appear in several files with different content (a late batch rewrite
    # overlapping an earlier top-up), and judging every copy would flag the
    # superseded one as stale even when the surviving copy matches the verdict
    # exactly. Verdicts are about the item that ships, so decide here.
    for qid in list(by_id):
        it = by_id[qid]
        sha = stem_fp(it)
        if qid in quarantine:
            ent = quarantine[qid]
            if ent["stem_sha"] and ent["stem_sha"] != sha:
                stale_verdicts.append((qid, sha))
            else:
                dropped_by_verdict.append(qid)
                del by_id[qid]
                continue
        if qid in rekey and rekey[qid].get("correct"):
            want = rekey[qid].get("stem_sha")
            if want and want != sha:
                # A stale rekey is more dangerous than a stale quarantine: it
                # would assert a wrong answer on rewritten content.
                stale_verdicts.append((qid, sha))
            else:
                apply_rekey(it, rekey[qid])
                E2, _ = validate(it, "rekeyed")
                if E2:
                    errors += E2
                    del by_id[qid]
                    continue
                rekeyed.append(qid)

    # De-duplicate by stem only after id resolution, so a superseded copy can
    # never shadow the version we actually kept.
    items, seen_stems = [], {}
    for qid in sorted(by_id):
        it = by_id[qid]
        n = norm(it["stem"])
        if n in seen_stems:
            warns.append(f"{qid}  near-duplicate stem of {seen_stems[n]} — dropped")
            continue
        seen_stems[n] = qid
        items.append(it)

    if superseded:
        warns.append(f"{len(superseded)} item(s) replaced by a newer file, "
                     f"e.g. {superseded[0]}")

    # Option rotation is opt-in because it changes which letter is correct, which
    # would desynchronise any blind verification pass running against the old
    # arrangement. Run it only after verification is settled.
    if "--rebalance" in sys.argv:
        n = rebalance(items, warns)
        print(f"\nRebalanced {n} item(s) by rotating options to reduce positional bias "
              f"(content preserved; the same text is still the answer)")

    # ---------------- report ----------------
    # group by the batch prefix embedded in each id, not by filename —
    # one batch is split across several -pN.json files
    batches = defaultdict(list)
    for i in items:
        batches[i["id"].rsplit("-", 1)[0]].append(i)

    print(f"\n{'batch':<12}{'kept':>6}  {'single':>7}{'multi':>7}{'next':>6}   "
          f"{'easy':>6}{'med':>6}{'hard':>6}   key spread")
    print("-" * 86)
    for b in sorted(batches):
        grp = batches[b]
        t = Counter(i["type"] for i in grp)
        d = Counter(i["difficulty"] for i in grp)
        k = Counter(c for i in grp for c in i["correct"])
        spread = " ".join(f"{x}:{k.get(x, 0)}" for x in KEYS if k.get(x))
        print(f"{b:<12}{len(grp):>6}  {t['single']:>7}{t['multi']:>7}{t['nextstep']:>6}   "
              f"{d['easy']:>6}{d['medium']:>6}{d['hard']:>6}   {spread}")

    print("-" * 86)
    print(f"{'TOTAL':<12}{len(items):>6}   from {len(per_file)} file(s), {len(batches)} batch(es)")

    dom = Counter(i["domain"] for i in items)
    print("\nDomain distribution")
    for k, v in dom.most_common():
        print(f"  {v:>5}  {100*v/max(1,len(items)):>5.1f}%   {k}")

    ty = Counter(i["type"] for i in items)
    di = Counter(i["difficulty"] for i in items)
    ky = Counter(c for i in items for c in i["correct"])
    print(f"\nTypes       {dict(ty)}")
    print(f"Difficulty  {dict(di)}")
    print(f"Correct key {dict(sorted(ky.items()))}")
    print(f"Topics      {len(set(i['topic'] for i in items))} distinct")

    scen = sum(1 for i in items if not i["id"].startswith("RCL-"))
    rcl  = len(items) - scen
    if items:
        print(f"Style mix   {scen:,} scenario ({100*scen/len(items):.0f}%) / "
              f"{rcl:,} recall ({100*rcl/len(items):.0f}%)")

    # ---------------- flashcards ----------------
    cards, cerr, cwarn, cper = load_cards()
    errors += cerr
    warns += cwarn
    if cper:
        # Group by the batch prefix in each card id, not by filename — one deck
        # is split across several -pN.json files.
        cbatch = defaultdict(list)
        for c in cards:
            cbatch[c["id"].rsplit("-", 1)[0]].append(c)
        print("\nFlashcard deck")
        for b in sorted(cbatch):
            d = Counter(c["difficulty"] for c in cbatch[b])
            print(f"  {len(cbatch[b]):>4}  {b:<10} easy {d['easy']:>3}  med {d['medium']:>3}  "
                  f"hard {d['hard']:>3}")
        print(f"  {len(cards):>4}  TOTAL    across {len(set(c['domain'] for c in cards))} domains, "
              f"{len(set(c['topic'] for c in cards))} topics")
    else:
        print("\nFlashcard deck: none found (build/flashcards/ is empty)")

    if dropped_by_verdict or rekeyed:
        print(f"\nAdjudicated verdicts applied: {len(dropped_by_verdict)} quarantined"
              f"{f', {len(rekeyed)} re-keyed' if rekeyed else ''}")
        for q in dropped_by_verdict:
            print(f"   - {q}: {quarantine[q]['reason'][:110]}")
        for q in rekeyed:
            print(f"   ~ {q} -> {'+'.join(rekey[q]['correct'])}: "
                  f"{str(rekey[q].get('why',''))[:100]}")

    if stale_verdicts:
        print(f"\n!! {len(stale_verdicts)} STALE VERDICT(S) — the item behind this id was")
        print("   rewritten after the verdict was recorded, so it was NOT dropped.")
        print("   Re-review, then update or remove the entry in build/verdicts.json:")
        for q, fp in stale_verdicts:
            print(f"   - {q}: current stem_sha is {fp}")

    # ---- batch-level quality audit ----------------------------------------
    # Individual items can each be valid while a batch as a whole is skewed.
    # A runaway correct-key letter creates a guessing bias; a missing difficulty
    # tier means the agent stopped following spec partway through.
    audit = []
    for b in sorted(batches):
        grp = batches[b]
        singles = [i for i in grp if i["type"] in ("single", "nextstep") and i.get("correct")]
        if len(singles) >= 12:
            kc = Counter(i["correct"][0] for i in singles)
            top, n = kc.most_common(1)[0]
            if n / len(singles) > 0.45:
                audit.append(f"{b}: {n}/{len(singles)} single-answer items keyed {top} "
                             f"({100 * n / len(singles):.0f}%) — positional bias")
            absent = [k for k in "ABCD" if not kc.get(k)]
            if absent:
                audit.append(f"{b}: no single-answer item keyed {'/'.join(absent)} "
                             f"across {len(singles)} items")
        if len(grp) >= 20:
            dc = Counter(i["difficulty"] for i in grp)
            for lvl in ("easy", "medium", "hard"):
                if not dc.get(lvl):
                    audit.append(f"{b}: zero '{lvl}' items across {len(grp)} items")
    if audit:
        print(f"\n!  BATCH QUALITY AUDIT — {len(audit)} issue(s) worth a top-up:")
        for a in audit:
            print("   " + a)

    if errors:
        print(f"\n!! {len(errors)} HARD ERROR(S) — those items were dropped:")
        for e in errors[:40]:
            print("   " + e)
        if len(errors) > 40:
            print(f"   ... and {len(errors)-40} more")
    if warns:
        print(f"\n~  {len(warns)} warning(s):")
        wc = Counter(re.sub(r"^\S+\s+", "", w) for w in warns)
        for w, c in wc.most_common(14):
            print(f"   x{c:<4} {w}")

    if not items:
        print("\n!! nothing to emit")
        return 1

    # ---------------- emit ----------------
    def js(obj):
        """Serialise for safe embedding inside a <script> block."""
        s = json.dumps(obj, ensure_ascii=False, separators=(",", ":"))
        return (s.replace("<", "\\u003c").replace(">", "\\u003e")
                 .replace("\u2028", "\\u2028").replace("\u2029", "\\u2029"))

    META["cards"] = len(cards)
    html = TPL.read_text(encoding="utf-8")
    for token, value in (("/*__QUESTIONS__*/[]", js(items)),
                         ("/*__FLASHCARDS__*/[]", js(cards)),
                         ("/*__META__*/{}", js(META))):
        if token not in html:
            print(f"!! template is missing the {token} placeholder")
            return 1
        html = html.replace(token, value, 1)

    OUT.write_text(html, encoding="utf-8", newline="\n")
    kb = OUT.stat().st_size / 1024
    print(f"\n-> {OUT.name}   {len(items):,} questions + {len(cards):,} flashcards   "
          f"{kb:,.0f} KB ({kb/1024:.1f} MB)   ~{len(items)//META['examItems']} full exams")
    return 0


if __name__ == "__main__":
    sys.exit(main())
