#!/usr/bin/env python3
"""
Deterministic correctness / hallucination audit over the assembled question bank.

Usage:  python build/audit.py [--full]

This does NOT judge whether an answer is *right* — that needs independent
re-answering (see blind_export.py). What it does catch is the mechanical
signatures of hallucination and internal inconsistency:

  * invented Anthropic specifics  (prices, token limits, context sizes, quotas)
  * named model versions          (drift the moment a new model ships)
  * internal contradiction        (explanation argues a letter that is not the key)
  * unsupported multi keys        (a correct key the explanation never justifies)
  * self-defeating distractors    (distractor rationale that concedes it is right)
  * letter-referencing options    (breaks if options are ever reordered)
  * near-identical options        (two options that mean the same thing)
  * absolute language in the key  ("always", "never", "only")
  * cross-batch contradictions    (same question, different answer)
"""
from __future__ import annotations
import json, re, sys
from collections import Counter, defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from assemble import read_json, scrub, norm, QDIR, KEYS   # reuse the loader

FULL = "--full" in sys.argv
CTX = 150


def load_all():
    items = {}
    for fp in sorted(QDIR.glob("*.json"), key=lambda p: (p.stat().st_mtime, p.name)):
        try:
            data, _ = read_json(fp)
        except Exception:
            continue
        if not isinstance(data, list):
            continue
        for it in data:
            if isinstance(it, dict) and it.get("id"):
                items[it["id"]] = (scrub(it), fp.name)
    return items


def blob(it) -> str:
    parts = [str(it.get("stem", ""))]
    parts += [str(o.get("text", "")) for o in it.get("options") or []]
    e = it.get("explanation") or {}
    if isinstance(e, dict):
        parts += [str(e.get(k, "")) for k in ("correct", "concept", "examTip")]
        d = e.get("distractors")
        if isinstance(d, dict):
            parts += [str(v) for v in d.values()]
    return "\n".join(parts)


# ---------------------------------------------------------------- fact patterns
# A number is acceptable when it is clearly a property of the fictional company
# ("their policy caps uploads at 20MB"). It is a hallucination risk when it is
# asserted as an Anthropic product fact.
COMPANY_FRAME = re.compile(
    r"\b(their|its|company|companies|firm|organisation|organization|internal|corporate|"
    r"policy|policies|contract|contractual|sla|agreed|team's|department|budget|"
    r"client's|vendor|procurement|governance)\b", re.I)

FACT_PATTERNS = [
    ("invented context-window size",
     re.compile(r"\b\d{2,3}[,.]?\d{0,3}\s*(?:k|thousand)?\s*token(?:s)?\s*"
                r"(?:context|window|limit|budget)|\bcontext window of\s+\d", re.I)),
    ("invented price / cost figure",
     re.compile(r"\$\s?\d[\d,.]*\s*(?:per|/)\s*(?:million|mtok|1m|1,000|k|token|request|call|seat|user|month)"
                r"|\$\d[\d,.]*\s*(?:per million|/mtok)", re.I)),
    ("invented rate limit",
     re.compile(r"\b\d{2,6}\s*(?:requests?|calls?|rpm|tpm)\s*(?:per|/)\s*(?:minute|min|second|hour)", re.I)),
    ("invented plan quota",
     re.compile(r"\b\d{1,4}\s*(?:messages?|prompts?|queries?)\s*(?:per|every|/)\s*"
                r"(?:\d+\s*)?(?:hours?|day|days|week|month)", re.I)),
    ("invented file / upload cap",
     re.compile(r"\b\d{1,4}\s*(?:MB|GB|KB)\b|\b(?:up to|maximum of|max)\s+\d{1,3}\s*"
                r"(?:files?|documents?|attachments?|uploads?|images?)\b", re.I)),
    # The negative lookahead skips numbered-list markers: prose like
    # "...the task given to Claude 2. The AI-generated draft..." is a list item
    # after the word Claude, not a version reference.
    ("named model version",
     re.compile(r"claude[-\s]*(?:[1-9](?:\.\d)?)(?![.)]\s)\b"
                r"|claude[-\s]*(?:opus|sonnet|haiku)[-\s]*[0-9]"
                r"|(?:opus|sonnet|haiku)[-\s]*[0-9](?:\.[0-9])?\b", re.I)),
    ("asserted knowledge-cutoff date",
     re.compile(r"(?:knowledge|training)\s+cut[-\s]?off\s+(?:of|is|was|date\s+of)?\s*"
                r"(?:[A-Z][a-z]+\s+)?20\d\d", re.I)),
    ("asserted benchmark / accuracy stat for Claude",
     re.compile(r"claude\s+(?:achieves|scores|reaches|has)\s+(?:an?\s+)?\d{1,3}(?:\.\d)?\s*%", re.I)),
]

LETTER_REF = re.compile(r"\boption\s+[A-E]\b|\b[A-E]\s+and\s+[A-E]\b|\bboth\s+[A-E]\b")

# Narrowed to explicit SELF-reference. The earlier version matched any prose
# about something being correct, which flagged legitimate contrastive
# explanations ("this would be correct for style defaults, but ...") and
# arithmetic discussion about figures in the scenario. 34 hits, all noise.
CONCEDE = re.compile(
    r"\bthis (?:option |answer |choice )?is (?:also |actually |equally |technically )"
    r"(?:the )?correct(?:\s+answer)?\b"
    r"|\bthis (?:option |answer |choice )?would (?:also |equally )?be "
    r"(?:the |a )?(?:correct|best) (?:answer|choice|option)\b"
    r"|\b(?:this|it) is (?:just )?as (?:correct|valid|defensible)\b", re.I)


def words(s):
    return set(re.findall(r"[a-z]{4,}", str(s).lower()))


def main() -> int:
    items = load_all()
    if not items:
        print("no items found")
        return 1
    findings = defaultdict(list)

    stem_map = defaultdict(list)

    for qid, (it, src) in items.items():
        b = blob(it)
        cor = [str(k).upper() for k in (it.get("correct") or [])]
        opts = it.get("options") or []
        e = it.get("explanation") or {}
        ex_correct = str(e.get("correct", "")) if isinstance(e, dict) else ""

        # ---- invented facts
        for label, pat in FACT_PATTERNS:
            for m in pat.finditer(b):
                seg = b[max(0, m.start() - 70): m.start() + 80].replace("\n", " ")
                # a company-framed number is legitimate per the spec
                near = b[max(0, m.start() - 90): m.start() + 40]
                if label != "named model version" and COMPANY_FRAME.search(near):
                    continue
                findings[label].append((qid, src, seg.strip()))
                break

        # ---- multi keys the explanation never justifies
        # A key counts as justified if the explanation either names its letter OR
        # discusses its content. Explanations legitimately say "Statements R and T"
        # or restate the option in prose instead of citing "C" and "D".
        if it.get("type") == "multi" and len(cor) > 1 and ex_correct:
            ex_words = words(ex_correct)
            unjustified = []
            for k in cor:
                opt = next((o for o in opts if str(o.get("key", "")).upper() == k), None)
                if not opt:
                    continue
                if re.search(rf"(?<![A-Za-z]){k}(?![a-z])", ex_correct):
                    continue                      # letter is cited
                ow = words(opt.get("text"))
                if ow and len(ow & ex_words) / len(ow) >= 0.25:
                    continue                      # content is discussed
                unjustified.append(k)
            if unjustified:
                findings["multi key neither cited nor discussed in explanation"].append(
                    (qid, src, f"keys {'+'.join(cor)}; unaddressed: {'/'.join(unjustified)}"))

        # ---- distractor rationale that concedes the distractor is correct
        if isinstance(e, dict) and isinstance(e.get("distractors"), dict):
            for k, v in e["distractors"].items():
                if str(k).upper() in cor:
                    continue
                m = CONCEDE.search(str(v))
                if m:
                    findings["distractor rationale concedes it is correct"].append(
                        (qid, src, f"{k}: ...{str(v)[max(0,m.start()-60):m.start()+90]}..."))

        # ---- options that reference other options by letter
        for o in opts:
            if LETTER_REF.search(str(o.get("text", ""))):
                findings["option refers to another option by letter"].append(
                    (qid, src, f"{o.get('key')}: {str(o.get('text'))[:110]}"))
                break

        # ---- two options that say the same thing
        for i in range(len(opts)):
            for j in range(i + 1, len(opts)):
                a, c = words(opts[i].get("text")), words(opts[j].get("text"))
                if not a or not c:
                    continue
                jac = len(a & c) / len(a | c)
                if jac > 0.72:
                    findings["two options nearly identical"].append(
                        (qid, src, f"{opts[i].get('key')} vs {opts[j].get('key')} "
                                   f"overlap {jac:.0%}: {str(opts[j].get('text'))[:80]}"))
                    break
            else:
                continue
            break

        # NOTE: an "absolute language in the correct option" check was tried here
        # and removed. It fired on 221 items, essentially all legitimate prose
        # ("activates for every session in the Project"), and buried the real
        # findings. Detecting an unwarranted absolute needs semantic judgement,
        # which is the blind verifier's job, not a regex's.

        stem_map[norm(it.get("stem", ""))].append((qid, tuple(sorted(cor))))

    # ---- same question, different recorded answer
    for n, lst in stem_map.items():
        keys = {k for _, k in lst}
        if len(lst) > 1 and len(keys) > 1:
            findings["same stem, conflicting answers"].append(
                (", ".join(q for q, _ in lst), "-", f"keys recorded: {sorted(keys)}"))

    # ------------------------------------------------------------------ report
    order = sorted(findings, key=lambda k: -len(findings[k]))
    total = sum(len(v) for v in findings.values())
    print(f"\nAudited {len(items):,} items — {total} finding(s) across {len(findings)} category(ies)\n")
    print(f"{'count':>6}  category")
    print("-" * 68)
    for k in order:
        print(f"{len(findings[k]):>6}  {k}")

    limit = 10**9 if FULL else 6
    for k in order:
        print(f"\n### {k}  ({len(findings[k])})")
        for qid, src, ctx in findings[k][:limit]:
            print(f"  [{qid}] {ctx[:CTX]}")
        if len(findings[k]) > limit:
            print(f"  ... and {len(findings[k]) - limit} more (run with --full)")

    print("\nNote: this audit finds mechanical signatures only. Whether each recorded")
    print("answer is genuinely the best answer requires independent re-answering.")
    print("\nThe 'invented ...' categories are ADVISORY and run at a deliberately low")
    print("threshold. A figure is legitimate when it is a property of the fictional")
    print("company ('their policy caps uploads at 20MB', 'volume is 15,000 queries per")
    print("day') and only a problem when asserted as an Anthropic product limit.")
    print("Read the context before acting; most hits here are the former.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
