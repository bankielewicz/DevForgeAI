#!/usr/bin/env python3
"""Scratch prototype of the validator additions specified in mvp-and-prototype-path.md (BEH-33).
Standard library only, line and regex based. Usage: mvp_checks.py BRN.md ; prints 'line N: message' per problem."""
import datetime
import re
import sys

LEVEL = {"Fatal": 0, "Serious": 1, "Minor": 2}
CONF = {"low": 0, "medium": 1, "high": 2}


def cells(line):
    return [c.strip() for c in line.strip().strip("|").split("|")]


def section(lines, heading):
    """(index of heading line, index after last line) of a '## ' section, or None."""
    try:
        s = lines.index(heading)
    except ValueError:
        return None
    e = next((i for i in range(s + 1, len(lines)) if lines[i].startswith("## ")), len(lines))
    return s, e


def after(lines, start, end, heading):
    """Index of the first non-blank line after `heading` inside [start, end), or None when heading is missing."""
    try:
        h = next(i for i in range(start, end) if lines[i] == heading)
    except StopIteration:
        return None, None
    i = h + 1
    while i < end and not lines[i].strip():
        i += 1
    return h, i


def table(lines, i, end, header, ncols):
    """Rows (index, cells) of the table starting at line i, or None when its header or separator is wrong."""
    if i >= end or lines[i] != header:
        return None
    if i + 1 >= end or lines[i + 1] != "|" + "---|" * ncols:
        return None
    rows, j = [], i + 2
    while j < end and lines[j].startswith("|"):
        rows.append((j, cells(lines[j])))
        j += 1
    return rows


def items(lines):
    """{collection: [(id, {field: raw})]} read the way validate_brn.py reads item blocks."""
    out = {"problems": [], "ideas": [], "assumptions": []}
    i = 0
    while i < len(lines):
        if lines[i].rstrip() != "```yaml items":
            i += 1
            continue
        j = next(k for k in range(i + 1, len(lines)) if lines[k].startswith("```"))
        coll, cur = None, None
        for ln in lines[i + 1:j]:
            if not ln.strip() or ln.lstrip().startswith("#"):
                continue
            if not ln[0].isspace():
                coll = ln.split(":")[0]
                continue
            m = re.match(r"^\s*- id: (\S+)", ln)
            if m:
                cur = (m.group(1), {})
                out[coll].append(cur)
                continue
            m = re.match(r"^\s+(\w+):\s*(.*?)\s*$", ln)
            if m and cur and len(ln) - len(ln.lstrip()) == 4:
                cur[1][m.group(1)] = m.group(2)
        i = j + 1
    return out


def check(path):
    lines = open(path, encoding="utf-8").read().replace("\r\n", "\n").split("\n")
    body, in_fence, fm_end = [], False, lines.index("---", 1)
    for i, l in enumerate(lines):
        if i <= fm_end:
            continue
        if l.startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        body.append(l)
    if not any(" ".join(l.lower().split()).startswith("project kind:") for l in body):
        return []
    if "### First release cut" not in body and "### Assumption risk ranking" not in body:
        return []
    errs = []
    it = items(lines)
    ideas = {iid: f for iid, f in it["ideas"] if f.get("status") == "active"}
    asms = {iid: f for iid, f in it["assumptions"]}
    promoted = {iid for iid, f in ideas.items() if f.get("disposition") == "promoted"}

    # ---- the first release cut, section 6 ----
    sec6 = section(lines, "## 6. Convergence")
    cut_rows, cut_confirmed, cut_none, yes_rows = [], False, False, []
    cut_found = "### First release cut" in body
    if sec6:
        s, e = sec6
        h, i = after(lines, s, e, "### First release cut")
        if h is None:
            errs.append((s + 1, "a BRN with a Project kind line needs '### First release cut' in section 6"))
        else:
            m = re.fullmatch(r"First release cut: (proposed, not confirmed|confirmed by (\S.*) on (\d{4}-\d{2}-\d{2}))",
                             lines[i]) if i < e else None
            if not m:
                errs.append((i + 1 if i < e else h + 1, "the first release cut needs the status line "
                             "'First release cut: proposed, not confirmed' or "
                             "'First release cut: confirmed by NAME on YYYY-MM-DD'"))
                nxt = i + 1
            else:
                cut_confirmed = m.group(1).startswith("confirmed")
                if m.group(3):
                    try:
                        datetime.date.fromisoformat(m.group(3))
                    except ValueError:
                        errs.append((i + 1, f"the first release cut date {m.group(3)} is not a real calendar date"))
                nxt = i + 1
            while nxt < e and not lines[nxt].strip():
                nxt += 1
            if nxt < e and lines[nxt] == "No idea is promoted or proposed for promotion.":
                cut_none = True
                if promoted:
                    errs.append((nxt + 1, f"the cut says no idea is promoted, but {sorted(promoted)[0]} is promoted"))
                if cut_confirmed:
                    errs.append((i + 1, "a first release cut with no rows can't be confirmed"))
            else:
                rows = table(lines, nxt, e, "| Idea | In first release | Why |", 3)
                if rows is None:
                    errs.append((nxt + 1 if nxt < e else h + 1, "the first release cut needs the table "
                                 "'| Idea | In first release | Why |' or the line "
                                 "'No idea is promoted or proposed for promotion.'"))
                else:
                    seen = []
                    for ln, c in rows:
                        if len(c) != 3:
                            errs.append((ln + 1, f"first release cut row has {len(c)} cells, expected 3"))
                            continue
                        iid = c[0]
                        if not re.fullmatch(r"IDEA-\d{2}", iid):
                            errs.append((ln + 1, f"first release cut row must start with an idea ID, not '{iid}'"))
                            continue
                        if iid not in ideas:
                            errs.append((ln + 1, f"first release cut row {iid} is not an active idea of this document"))
                        elif ideas[iid].get("disposition") in ("parked", "rejected"):
                            errs.append((ln + 1, f"first release cut row {iid} is {ideas[iid]['disposition']}, "
                                         "so it can't be in the cut"))
                        if seen and iid <= seen[-1]:
                            errs.append((ln + 1, "first release cut rows must be unique and in ID order"))
                        seen.append(iid)
                        if c[1] not in ("yes", "no"):
                            errs.append((ln + 1, f"'In first release' must be yes or no, not '{c[1]}'"))
                        if not c[2]:
                            errs.append((ln + 1, f"first release cut row {iid} has an empty Why"))
                        cut_rows.append(iid)
                        if c[1] == "yes":
                            yes_rows.append(iid)
                    if cut_confirmed:
                        if set(cut_rows) != promoted:
                            miss = ", ".join(sorted(promoted - set(cut_rows))) or "none"
                            extra = ", ".join(sorted(set(cut_rows) - promoted)) or "none"
                            errs.append((i + 1, "a confirmed first release cut must list exactly the promoted ideas "
                                         f"(missing: {miss}; extra: {extra})"))

    # ---- the ranking, section 7 ----
    sec7 = section(lines, "## 7. Assumptions and open questions")
    if sec7:
        s, e = sec7
        h, i = after(lines, s, e, "### Assumption risk ranking")
        open_asm = sorted(a for a, f in asms.items() if f.get("status") == "active" and f.get("state") == "open")
        if h is None:
            errs.append((s + 1, "a BRN with a Project kind line needs '### Assumption risk ranking' in section 7"))
        elif i < e and lines[i] == "None.":
            if open_asm:
                errs.append((i + 1, f"the ranking says None. but {open_asm[0]} is active and open"))
        else:
            rows = table(lines, i, e, "| Rank | Assumption | If wrong | Confidence | Cheapest test |", 5)
            if rows is None:
                errs.append((i + 1 if i < e else h + 1, "the assumption risk ranking needs the table "
                             "'| Rank | Assumption | If wrong | Confidence | Cheapest test |' or the line 'None.'"))
            else:
                keys, ranked = [], []
                for pos, (ln, c) in enumerate(rows, 1):
                    if len(c) != 5:
                        errs.append((ln + 1, f"ranking row has {len(c)} cells, expected 5"))
                        continue
                    rank, aid, wrong, conf, test = c
                    if rank != str(pos):
                        errs.append((ln + 1, f"rank must be {pos}, not '{rank}'"))
                    if aid not in open_asm:
                        errs.append((ln + 1, f"ranking row {aid} is not an active assumption with state open"))
                    elif aid in ranked:
                        errs.append((ln + 1, f"{aid} is ranked twice"))
                    ranked.append(aid)
                    if conf not in CONF:
                        errs.append((ln + 1, f"Confidence must be high, medium or low, not '{conf}'"))
                    if not re.match(r"(Data|Prototype|Interview): \S", test):
                        errs.append((ln + 1, "'Cheapest test' must start with 'Data: ', 'Prototype: ' or "
                                     "'Interview: ' and then words"))
                    m = re.fullmatch(r"(Fatal|Serious|Minor)(?: \((IDEA-\d{2}(?:, IDEA-\d{2})*)\))?: (\S.*)", wrong)
                    level = None
                    if not m or "IDEA-" in m.group(3) or "|" in m.group(3):
                        errs.append((ln + 1, "'If wrong' must be a level (Fatal, Serious or Minor), an optional list "
                                     "of idea IDs in parentheses, ': ', then words with no idea ID"))
                    else:
                        level = m.group(1)
                        lst = m.group(2).split(", ") if m.group(2) else []
                        if lst != sorted(set(lst)):
                            errs.append((ln + 1, "'If wrong' must list each idea once, in ID order"))
                        for x in (lst if cut_found else []):
                            if x not in cut_rows:
                                errs.append((ln + 1, f"'If wrong' lists {x}, which is not a row of the first release cut"))
                        n_in = len(set(lst) & set(cut_rows))
                        want = "Minor" if n_in == 0 else ("Fatal" if n_in == len(cut_rows) else "Serious")
                        if cut_found and want != level:
                            errs.append((ln + 1, f"'If wrong' says {level}, but the listed ideas make it {want} "
                                         f"(the cut has {len(cut_rows)} rows, the list names {n_in} of them)"))
                        if conf not in CONF:
                            continue
                        keys.append((LEVEL[level], CONF[conf], aid))
                        if len(keys) > 1 and keys[-2] > keys[-1]:
                            errs.append((ln + 1, f"{aid} must be ranked before {keys[-2][2]} "
                                         "(level, then confidence low first, then assumption number)"))
                for a in open_asm:
                    if a not in ranked:
                        errs.append((h + 1, f"active open assumption {a} is missing from the ranking"))

    # ---- section 8 follows the cut's yes rows ----
    sec8 = section(lines, "## 8. Candidate success signals")
    if sec8 and "### First release cut" in body and (cut_rows or cut_none):
        s8, e8 = sec8
        yes = [c[0] for ln, c in (cut_table or [])] if False else yes_rows
        found = [m.group(1) for l in lines[s8 + 1:e8] for m in [re.match(r"^- (IDEA-\d{2}):", l)] if m]
        if found != yes_rows:
            errs.append((s8 + 1, "section 8 must hold one bullet for each first release idea, in ID order "
                         f"(expected: {', '.join(yes_rows) or 'none'}; found: {', '.join(found) or 'none'})"))
    return sorted(set(errs))


if __name__ == "__main__":
    errs = check(sys.argv[1])
    for ln, msg in errs:
        print(f"line {ln}: {msg}")
    print("OK" if not errs else f"{len(errs)} problem(s)")
