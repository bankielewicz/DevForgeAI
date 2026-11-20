#!/usr/bin/env python3
"""Validate a DevForgeAI brainstorm (BRN) document against references/output-rules.md.

Usage: python3 validate_brn.py docs/specs/brainstorm/BRN-NNN.md

Prints one line per problem ("line N: message") and exits 1, or prints "OK: <path>" and
exits 0. Uses only the standard library; if PyYAML is installed it also checks YAML syntax.
Every other check, dates against the calendar included, gives the same verdict with or without it.
It cannot check whether the user confirmed a disposition, convergence or the first release cut: that is
the skill's job.
"""
import datetime
import os
import re
import sys

FRONTMATTER_KEYS = [
    "id", "type", "title", "status", "version", "created", "updated", "owner", "authors",
    "generated_by", "reviewed_by", "approved_by", "approved_on", "upstream", "supersedes",
    "superseded_by", "blocked_by", "participants", "sources",
]
SECTIONS = [
    "## 1. Context", "## 2. Problems", "## 3. Target users", "## 4. Ideas",
    "## 5. Evaluation method", "## 6. Convergence", "## 7. Assumptions and open questions",
    "## 8. Candidate success signals", "## Change Log",
]
COMMON = {"id", "status", "superseded_by", "upstream"}
COLLECTIONS = {
    "problems": {
        "prefix": "PRB",
        "required": ["statement", "who", "evidence", "severity"],
        "quoted": {"statement", "who", "evidence"},
        "enums": {"severity": {"high", "medium", "low"}},
    },
    "ideas": {
        "prefix": "IDEA",
        "required": ["idea", "addresses", "value", "effort", "risk", "score", "disposition", "reason"],
        "quoted": {"idea"},
        "enums": {"disposition": {"open", "promoted", "parked", "rejected"}},
    },
    "assumptions": {
        "prefix": "ASM",
        "required": ["statement", "validation", "state"],
        "quoted": {"statement", "validation"},
        "enums": {"state": {"open", "validated", "invalidated"}},
    },
}
DATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
NUMBER = re.compile(r"^-?\d+(\.\d+)?$")
PLACEHOLDER = re.compile(r"<[a-z][^<>\n]*>")
INLINE_HTML = re.compile(r"</?(br|b|i|em|strong|code|kbd|sub|sup|s|u|mark|small)\s*/?>")
GENERATED_BY_KEYS = ("tool", "model", "session")


def closing_quote(v):
    """Index of the quote that closes a double-quoted value starting at v[0], or None."""
    end = 1
    while end < len(v):
        if v[end] == "\\":
            end += 2
            continue
        if v[end] == '"':
            return end
        end += 1
    return None


def value_of(raw):
    """Strip a trailing YAML comment from a scalar value, respecting double quotes.

    Text after the closing quote that isn't a comment is kept, so quoted() rejects the value.
    """
    v = raw.strip()
    if v.startswith('"'):
        end = closing_quote(v)
        rest = v[end + 1:].strip() if end is not None else None
        if rest == "" or (rest and rest.startswith("#")):
            return v[: end + 1]
        return v
    return v.split(" #", 1)[0].strip()


def quoted(v):
    return len(v) >= 2 and v.startswith('"') and closing_quote(v) == len(v) - 1


def flow_items(v):
    """The raw items of a one-line flow list such as ["a", "b"], or None if v isn't one."""
    if not (v.startswith("[") and v.endswith("]")):
        return None
    items, cur, in_quote, escaped = [], "", False, False
    for ch in v[1:-1]:
        if in_quote:
            cur += ch
            if escaped:
                escaped = False
            elif ch == "\\":
                escaped = True
            elif ch == '"':
                in_quote = False
        elif ch == '"':
            in_quote = True
            cur += ch
        elif ch == ",":
            items.append(cur.strip())
            cur = ""
        else:
            cur += ch
    if cur.strip() or items:
        items.append(cur.strip())
    return items


KIND_PREFIX = "Project kind: "
KINDS = {
    "greenfield": "greenfield",
    "brownfield": "brownfield",
    "[NEEDS CLARIFICATION: greenfield or brownfield]": "unknown",
}
MARKER = re.compile(r"^\[NEEDS CLARIFICATION: [^\[\]]+\]$")
SOURCE = re.compile(r"^(document|data|ticket|interview|url|note): \S")
TARGET_USERS = "| Persona | Job to be done | Current workaround | Pain |"
SIGNAL = re.compile(r"^- (IDEA-\d{2}): (.+?); baseline (.+)$")
WORKED = re.compile(r"^- \[NEEDS CLARIFICATION: greenfield or brownfield; this run worked as "
                    r"(greenfield|brownfield)\]$")
SIGNAL_FORM = ("section 8 holds one bullet per first-release idea, '- IDEA-NN: outcome; baseline value', "
               "or the single line '- None.' (IV-05)")


def unquote(v):
    """The text of a double-quoted value, with \\" and \\\\ unescaped; any other value unchanged."""
    if not quoted(v):
        return v
    return v[1:-1].replace('\\"', '"').replace("\\\\", "\\")


def outside_fences(lines, fm_end):
    """(line number, text) for each line after the frontmatter that is outside every fenced block."""
    out, fence = [], False
    for i in range(fm_end + 1, len(lines)):
        if lines[i].startswith("```"):
            fence = not fence
        elif not fence:
            out.append((i + 1, lines[i]))
    return out


def kind_lines(lines, fm_end):
    """The project-kind lines. A BRN with at least one is a new-shape BRN (the gate)."""
    return [(n, t) for n, t in outside_fences(lines, fm_end)
            if " ".join(t.lower().split()).startswith("project kind:")]


def new_shape_kind(lines, fm_end):
    """None for an earlier-shape BRN; otherwise greenfield, brownfield, unknown or invalid."""
    found = kind_lines(lines, fm_end)
    if not found:
        return None
    text = found[0][1]
    if not text.startswith(KIND_PREFIX):
        return "invalid"
    return KINDS.get(text[len(KIND_PREFIX):], "invalid")


def section_body(lines, heading):
    """(the heading's line number, [(line number, text)] up to the next '## ' heading), or (0, [])."""
    if heading not in lines:
        return 0, []
    start = lines.index(heading)
    body = []
    for i in range(start + 1, len(lines)):
        if lines[i].startswith("## "):
            break
        body.append((i + 1, lines[i]))
    return start + 1, body


def subsection(body, heading):
    """(the '### ' heading's line number, its non-blank lines up to the next '### '), or (0, [])."""
    at = next((k for k, (_, t) in enumerate(body) if t == heading), None)
    if at is None:
        return 0, []
    rows = []
    for n, t in body[at + 1:]:
        if t.startswith("### "):
            break
        if t.strip():
            rows.append((n, t))
    return body[at][0], rows


def cells(text):
    """The cells of a table row, or None when the line is not a table row."""
    t = text.strip()
    if len(t) < 2 or not (t.startswith("|") and t.endswith("|")):
        return None
    return [c.strip() for c in t[1:-1].split("|")]


def ends_with_source(text, sources):
    """True when text is a statement followed by one sources entry in parentheses."""
    return any(text.endswith(" (" + s + ")") and len(text) > len(s) + 3 for s in sources)


def cited(text, sources):
    """True when text is one NEEDS CLARIFICATION marker, or ends with one sources entry in parentheses."""
    return bool(MARKER.match(text)) or ends_with_source(text, sources)


def first_release_ideas(lines):
    """The IDs whose row under '### First release cut' (section 6) says yes, in the table's order."""
    _, body = section_body(lines, "## 6. Convergence")
    _, rows = subsection(body, "### First release cut")
    out = []
    for _, t in rows:
        c = cells(t)
        if c and len(c) >= 2 and re.fullmatch(r"IDEA-\d{2}", c[0]) and c[1] == "yes":
            out.append(c[0])
    return out


def working_kind(lines):
    """The kind an undecided run worked as, from its one bullet in section 7; None without exactly one."""
    _, body = section_body(lines, "## 7. Assumptions and open questions")
    found = [m.group(1) for m in (WORKED.match(t) for _, t in body) if m]
    return found[0] if len(found) == 1 else None


def check_intake(lines, fm_end, source_items, items, err):
    """IV-01 to IV-07, for a new-shape BRN. Returns the valid sources entries, unquoted."""
    # IV-01: the project-kind line
    found = kind_lines(lines, fm_end)
    ln, text = found[0]
    for n, _ in found[1:]:
        err(n, "only one Project kind line is allowed (IV-01)")
    if not (text.startswith(KIND_PREFIX) and text[len(KIND_PREFIX):] in KINDS):
        err(ln, "the Project kind line must be exactly 'Project kind: greenfield', 'Project kind: "
            "brownfield' or 'Project kind: [NEEDS CLARIFICATION: greenfield or brownfield]' (IV-01)")
    _, body = section_body(lines, "## 1. Context")
    first = next((n for n, t in body if t.strip()), 0)
    if first != ln or ln >= len(lines) or lines[ln].strip():
        err(ln, "the Project kind line must be the first line under '## 1. Context', followed by a "
            "blank line (IV-01)")

    # IV-07: an undecided kind is recorded in section 7, with the kind the run worked as
    head, body = section_body(lines, "## 7. Assumptions and open questions")
    marks = [n for n, t in body if WORKED.match(t)]
    kind = new_shape_kind(lines, fm_end)
    if head and kind == "unknown" and len(marks) != 1:
        err(head, "while the project kind is not decided, section 7 must hold exactly one bullet '- [NEEDS "
            "CLARIFICATION: greenfield or brownfield; this run worked as greenfield]' or the same with "
            "'worked as brownfield' (IV-07)")
    if kind in ("greenfield", "brownfield"):
        for n in marks:
            err(n, "the project kind is decided: remove the bullet that says which kind the run worked as "
                "(IV-07)")

    # IV-02: sources entries
    sources = []
    for n, raw in source_items:
        s = unquote(raw)
        if not SOURCE.match(s) or s != s.strip() or "|" in s:
            err(n, f"sources entry {raw} must be \"kind: reference\" with no | in it, the kind being "
                "document, data, ticket, interview, url or note (IV-02)")
        elif s in sources:
            err(n, f"duplicate sources entry {raw} (IV-02)")
        else:
            sources.append(s)

    def active(collection):
        return [it for it in items[collection] if it["fields"].get("status", (0, ""))[1] == "active"]

    # IV-03: each active problem's evidence is cited
    for it in active("problems"):
        ev = it["fields"].get("evidence")
        if ev and quoted(ev[1]) and not cited(unquote(ev[1]), sources):
            err(ev[0], f"{it['id']}: evidence must be one [NEEDS CLARIFICATION: ...] marker or end with one "
                "sources entry in parentheses, such as \"... (data: no-show log, August 2026)\" (IV-03)")

    # IV-04: section 3 is the Target users table, one row per who value
    head, body = section_body(lines, "## 3. Target users")
    rows = [(n, t) for n, t in body if t.strip()]
    if head and (len(rows) < 2 or rows[0][1] != TARGET_USERS or rows[1][1] != "|---|---|---|---|"):
        err(rows[0][0] if rows else head, f"section 3 must start with the table header '{TARGET_USERS}' "
            "and the line '|---|---|---|---|' (IV-04)")
    elif head:
        personas = []
        for n, t in rows[2:]:
            c = cells(t)
            if c is None or len(c) != 4 or not all(c):
                err(n, "section 3 holds only the Target users table: each row has four non-empty cells (IV-04)")
            else:
                personas.append(c[0])
        who = []
        for it in active("problems"):
            w = it["fields"].get("who")
            if w and unquote(w[1]) not in who:
                who.append(unquote(w[1]))
        if personas != who:
            err(rows[0][0], "section 3's Persona cells must be the active problems' who values, each once, "
                f"in the order they first appear: expected {'; '.join(who)}, got {'; '.join(personas)} (IV-04)")

    # IV-05: section 8's bullets; IV-06: they are the first-release ideas
    head, body = section_body(lines, "## 8. Candidate success signals")
    rows = [(n, t) for n, t in body if t.strip()]
    ideas = {it["id"] for it in active("ideas")}
    bullets = []
    if head and not rows:
        err(head, SIGNAL_FORM)
    elif head and [t for _, t in rows] != ["- None."]:
        for n, t in rows:
            m = SIGNAL.match(t)
            if not m:
                err(n, SIGNAL_FORM)
                continue
            iid = m.group(1)
            if iid not in ideas:
                err(n, f"section 8: {iid} is not an active idea (IV-05)")
            if bullets and iid <= bullets[-1]:
                err(n, "section 8's bullets must be in ID order, each idea once (IV-05)")
            bullets.append(iid)
            if not cited(m.group(3), sources):
                err(n, f"{iid}: baseline must be one [NEEDS CLARIFICATION: ...] marker or end with one "
                    "sources entry in parentheses (IV-05)")
    if head:
        first = sorted(set(first_release_ideas(lines)))
        if sorted(set(bullets)) != first:
            err(head, "section 8 must hold one bullet for each idea whose First release cut row says yes "
                f"({', '.join(first) or 'none'}) and no other; with none, the single line '- None.' (IV-06)")
    return sources


DOC_FOLDERS = {"BRN": "brainstorm", "PRD": "prd", "EPIC": "epic", "ARCH": "arch"}
DOC_ID = re.compile(r"^(BRN|PRD|EPIC|ARCH)-\d{3}$")
COVERED_BY = re.compile(r"^(PRD-\d{3})#(?:FR|NFR)-\d{3}$|^(EPIC-\d{3})#DW-\d{2}$|^(ARCH-\d{3})#CMP-\d{2}$")
SKIPPED = re.compile(r"^Skipped: \S+ \((could not be read|no frontmatter|id does not match the file name|"
                     r"no version)\)$")
CONFIRMED = re.compile(r"^confirmed on (\d{4}-\d{2}-\d{2})$")
BROWNFIELD_HEADINGS = [
    ("### Existing product", "## 1. Context"),
    ("### Already covered", "## 6. Convergence"),
    ("### Previously decided", "## 6. Convergence"),
    ("### Assumption updates", "## 6. Convergence"),
]
NO_DOCUMENT = "No document was found in the project."


def table(rows, header, err, what, code):
    """The cell lists of a subsection's table, as (line number, cells), or None when it is malformed."""
    width = header.count("|") - 1
    if len(rows) < 3 or rows[0][1] != header or rows[1][1] != "|" + "---|" * width:
        err(rows[0][0], f"{what} must be the table '{header}' with at least one row, or its replacement line ({code})")
        return None
    out = []
    for n, t in rows[2:]:
        c = cells(t)
        if c is None or len(c) != width or not all(c):
            err(n, f"{what}: each row has {width} non-empty cells ({code})")
        else:
            out.append((n, c))
    return out


def link(raw):
    """(id, item, relation, version) of a flow-form link record; a missing part is None."""
    def part(key):
        m = re.search(r"[{,]\s*" + key + r":\s*([^\s,}]+)", raw)
        return m.group(1) if m else None
    return part("id"), part("item"), part("relation"), part("version")


def check_brownfield(lines, kind, own_id, upstream_items, sources, items, err):
    """BV-01 to BV-05, for a new-shape BRN. `sources` is what check_intake returned."""
    bodies = {h: section_body(lines, h) for h in ("## 1. Context", "## 6. Convergence")}
    found = {}
    for heading, section in BROWNFIELD_HEADINGS:
        found[heading] = subsection(bodies[section][1], heading)

    # BV-01: which brownfield headings are present, and their order
    present = [h for h, _ in BROWNFIELD_HEADINGS if found[h][0]]
    mode = working_kind(lines) if kind == "unknown" else None
    for heading, section in BROWNFIELD_HEADINGS:
        n = found[heading][0]
        if kind == "greenfield" and n:
            err(n, f"'{heading}' belongs to a brownfield BRN only: remove it, or correct the Project kind line (BV-01)")
        elif kind == "brownfield" and not n:
            err(bodies[section][0], f"a brownfield BRN needs '{heading}' in section {section[3]} (BV-01)")
        elif mode == "brownfield" and not n:
            err(bodies[section][0], f"this run worked as brownfield: '{heading}' is needed in section "
                f"{section[3]} (BV-01)")
        elif mode == "greenfield" and n:
            err(n, f"this run worked as greenfield: remove '{heading}' (BV-01)")
        elif kind == "unknown" and mode is None and present and not n:
            err(bodies[section][0], f"'{heading}' is missing: while the project kind is not decided, write "
                "all four brownfield headings or none of them (BV-01)")
    order = [found[h][0] for h in ("### Already covered", "### Previously decided", "### Assumption updates")
             if found[h][0]]
    cut = subsection(bodies["## 6. Convergence"][1], "### First release cut")[0]
    if order != sorted(order) or (cut and order and cut > order[0]):
        err(order[0], "section 6's subsections must come in this order: First release cut, Already covered, "
            "Previously decided, Assumption updates (BV-01)")

    # BV-02: Existing product, with an upstream record and a sources entry for each document
    docs = {}
    n, rows = found["### Existing product"]
    if n and not rows:
        err(n, f"'### Existing product' must hold its table or the line '{NO_DOCUMENT}' (BV-02)")
    elif n:
        k = next((i for i, (_, t) in enumerate(rows) if cells(t) is None), len(rows))
        for m, t in rows[k:]:
            if not (t == NO_DOCUMENT and m == rows[0][0]) and not SKIPPED.match(t):
                err(m, "under '### Existing product', after the table or its replacement line, only "
                    "'Skipped: path (reason)' lines are allowed, the reason being could not be read, no "
                    "frontmatter, id does not match the file name, or no version (BV-02)")
        if k:
            for m, c in table(rows[:k], "| Document | Version | What it already covers |", err,
                              "'### Existing product'", "BV-02") or []:
                if not DOC_ID.match(c[0]) or not re.fullmatch(r"[1-9]\d*", c[1]):
                    err(m, "Existing product: Document must be a BRN, PRD, EPIC or ARCH ID and Version a "
                        "positive integer (BV-02)")
                elif c[0] in docs or c[0] == own_id:
                    err(m, f"Existing product: {c[0]} is listed twice, or is this BRN itself (BV-02)")
                else:
                    docs[c[0]] = (m, c[1])
    links = [link(x) for _, x in upstream_items]
    for doc, (m, version) in docs.items():
        if (doc, None, "informed_by", version) not in links:
            err(m, f"{doc}: the frontmatter's upstream needs the record {{id: {doc}, relation: informed_by, "
                f"version: {version}, hash: null}} (BV-02)")
        entry = f"document: docs/specs/{DOC_FOLDERS[doc.split('-')[0]]}/{doc}.md v{version}"
        if entry not in sources:
            err(m, f"{doc}: sources needs the entry \"{entry}\" (BV-02)")

    # BV-03: Already covered
    n, rows = found["### Already covered"]
    if n and [t for _, t in rows] != ["None."]:
        for m, c in (table(rows, "| Suggestion | Covered by |", err, "'### Already covered'", "BV-03")
                     if rows else err(n, "'### Already covered' must hold its table or the line 'None.' (BV-03)")) or []:
            hit = COVERED_BY.match(c[1])
            if not hit:
                err(m, "Already covered: Covered by must be PRD-NNN#FR-NNN, PRD-NNN#NFR-NNN, EPIC-NNN#DW-NN "
                    "or ARCH-NNN#CMP-NN (BV-03)")
            elif next(g for g in hit.groups() if g) not in docs:
                err(m, f"Already covered: {c[1]} cites a document that Existing product does not list (BV-03)")

    # BV-04: Previously decided, and no idea linked to an idea it lists
    wheres = {}
    n, rows = found["### Previously decided"]
    if n and [t for _, t in rows] != ["None."]:
        for m, c in (table(rows, "| Idea | Decision | Where |", err, "'### Previously decided'", "BV-04")
                     if rows else err(n, "'### Previously decided' must hold its table or the line 'None.' (BV-04)")) or []:
            hit = re.fullmatch(r"(BRN-\d{3})#IDEA-\d{2}", c[2])
            if c[1] not in ("rejected", "parked") or not hit:
                err(m, "Previously decided: Decision must be rejected or parked, and Where BRN-NNN#IDEA-NN (BV-04)")
            elif hit.group(1) not in docs:
                err(m, f"Previously decided: {c[2]} cites a BRN that Existing product does not list (BV-04)")
            elif c[2] in wheres:
                err(m, f"Previously decided: {c[2]} is listed twice (BV-04)")
            else:
                wheres[c[2]] = m
    for it in items["ideas"]:
        for m, t in it["fields"].get("upstream", (0, "", []))[2]:
            doc, item, _, _ = link(t[1:].strip())
            if f"{doc}#{item}" in wheres:
                err(m, f"{it['id']} is linked to {doc}#{item}, which Previously decided also lists: an idea "
                    "taken up again is not listed there (BV-04)")

    # BV-05: Assumption updates
    states = {it["id"]: it["fields"].get("state", (0, ""))[1] for it in items["assumptions"]}
    seen = set()
    n, rows = found["### Assumption updates"]
    if n and [t for _, t in rows] != ["None."]:
        for m, c in (table(rows, "| Earlier assumption | Change | Evidence | Status |", err,
                           "'### Assumption updates'", "BV-05")
                     if rows else err(n, "'### Assumption updates' must hold its table or the line 'None.' (BV-05)")) or []:
            hit = re.fullmatch(r"(BRN-\d{3})#(ASM-\d{2})", c[0])
            done = CONFIRMED.match(c[3])
            if done:
                try:
                    datetime.date.fromisoformat(done.group(1))
                except ValueError:
                    done = None
            if not hit or (hit.group(1) not in docs and hit.group(1) != own_id) or c[0] in seen:
                err(m, "Assumption updates: Earlier assumption must be BRN-NNN#ASM-NN of a BRN that Existing "
                    "product lists, or of this BRN, each once (BV-05)")
                continue
            seen.add(c[0])
            if c[1] not in ("open to validated", "open to invalidated"):
                err(m, "Assumption updates: Change must be 'open to validated' or 'open to invalidated' (BV-05)")
            if not ends_with_source(c[2], sources):
                err(m, "Assumption updates: Evidence must be a fact that ends with one sources entry in "
                    "parentheses (BV-05)")
            if c[3] != "proposed, not confirmed" and not done:
                err(m, "Assumption updates: Status must be 'proposed, not confirmed' or 'confirmed on DATE', "
                    "the date a real one written as four digits, two, two (BV-05)")
            elif hit.group(1) == own_id:
                want = c[1][len("open to "):] if done else "open"
                if states.get(hit.group(2)) != want:
                    err(m, f"Assumption updates: {hit.group(2)} of this BRN must have state {want} while its "
                        f"row says '{c[3] if not done else 'confirmed'}' (BV-05)")


def check(path):
    errors = []

    def err(line, msg):
        errors.append((line, msg))

    name = os.path.basename(path)
    stem = name[:-3] if name.endswith(".md") else name
    if not re.fullmatch(r"BRN-\d{3}\.md", name):
        err(0, f"file name {name!r} must be BRN-NNN.md")
    if not os.path.dirname(os.path.abspath(path)).replace("\\", "/").endswith("docs/specs/brainstorm"):
        err(0, "file must be in docs/specs/brainstorm/")

    try:
        with open(path, encoding="utf-8") as f:
            lines = f.read().replace("\r\n", "\n").split("\n")
    except UnicodeDecodeError as e:
        err(0, f"file is not UTF-8 text (byte {e.start}: {e.reason}); save it as UTF-8")
        return errors

    # --- frontmatter -------------------------------------------------------------------
    if not lines or lines[0] != "---":
        err(1, "frontmatter must start with a '---' line")
        return errors
    try:
        fm_end = lines.index("---", 1)
    except ValueError:
        err(1, "frontmatter has no closing '---' line")
        return errors

    keys, fm, nested = [], {}, {}
    current = None
    for i in range(1, fm_end):
        line = lines[i]
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        m = re.match(r"^([A-Za-z_][\w-]*):(.*)$", line)
        if m:
            current = m.group(1)
            keys.append(current)
            fm[current] = (i + 1, value_of(m.group(2)))
            nested[current] = []
        elif current:
            nested[current].append((i + 1, line))

    for k in keys:
        if k not in FRONTMATTER_KEYS:
            err(fm[k][0], f"unknown frontmatter key {k!r}")
    for k in FRONTMATTER_KEYS:
        if k not in fm:
            err(fm_end + 1, f"missing frontmatter key {k!r}")
    known = [k for k in keys if k in FRONTMATTER_KEYS]
    if known != [k for k in FRONTMATTER_KEYS if k in known]:
        err(2, "frontmatter keys are out of order (see output-rules.md)")

    def fv(k):
        return fm.get(k, (0, None))

    ln, v = fv("id")
    if v is not None and v != stem:
        err(ln, f"id {v!r} must equal the file name {stem!r}")
    ln, v = fv("type")
    if v is not None and v != "brainstorm":
        err(ln, "type must be brainstorm")
    ln, v = fv("title")
    if v is not None and (not quoted(v) or v == '""'):
        err(ln, "title must be a non-empty quoted string")
    ln, v = fv("status")
    if v is not None and v not in {"draft", "converged", "archived"}:
        err(ln, "status must be draft, converged or archived")
    ln, v = fv("version")
    if v is not None and not re.fullmatch(r"[1-9]\d*", v):
        err(ln, "version must be a positive integer")
    bad_date = False
    for k in ("created", "updated"):
        ln, v = fv(k)
        if v is not None and not DATE.match(v):
            err(ln, f"{k} must be an unquoted YYYY-MM-DD date")
        elif v is not None:
            try:
                datetime.date.fromisoformat(v)
            except ValueError:
                bad_date = True
                err(ln, f"{k} {v} is not a real calendar date")
    ln, v = fv("owner")
    if v is not None and (not quoted(v) or v == '""'):
        err(ln, 'owner must be a quoted name, or "[NEEDS CLARIFICATION: owner]" when it is unknown')

    def list_of(k):
        """(line, raw item) pairs for a frontmatter list in flow or block form, or None."""
        ln, v = fm[k]
        if v:
            items = flow_items(v)
            return None if items is None else [(ln, x) for x in items]
        rows = [(l, s.strip()) for l, s in nested[k] if s.strip()]
        if rows and all(s.startswith("- ") for _, s in rows):
            return [(l, value_of(s[2:])) for l, s in rows]
        return None

    def strings(items):
        return items is not None and all(quoted(x) and x != '""' for _, x in items)

    authors = list_of("authors") if "authors" in fm else None
    if "authors" in fm and not (authors and strings(authors)):
        err(fm["authors"][0],
            'authors must be a non-empty list of quoted names, e.g. ["Dana", "claude-code"]')
    for k in ("participants", "sources"):
        if k in fm and not strings(list_of(k)):
            err(fm[k][0], f"{k} must be [] or a list of quoted strings")
    if "upstream" in fm:
        links = list_of("upstream")
        if links is None or not all(x.startswith("{") and x.endswith("}") and re.search(r"[{,]\s*id:", x)
                                    and re.search(r"[{,]\s*relation:", x) for _, x in links):
            err(fm["upstream"][0], "upstream must be [] or a list of link records, one per line, such as "
                "- {id: BRN-002, relation: informed_by, version: 1, hash: null}")
    for k, want in (("supersedes", "[]"), ("superseded_by", "null"), ("blocked_by", "[]")):
        ln, v = fv(k)
        if v is not None and v != want:
            err(ln, f"{k} must be {want} in a brainstorm")
    ln, v = fv("reviewed_by")
    if v is not None and v != "[]":
        err(ln, "reviewed_by must be [] (only humans who reviewed it fill this)")
    ln, v = fv("approved_by")
    if v is not None and v != '""':
        err(ln, 'approved_by must be ""')
    ln, v = fv("approved_on")
    if v is not None and v != "null":
        err(ln, "approved_on must be null")
    if "generated_by" in fm:
        sub = {}
        for ln, line in nested["generated_by"]:
            m = re.match(r"^\s+([A-Za-z_][\w-]*):(.*)$", line)
            if m:
                sub[m.group(1)] = (ln, value_of(m.group(2)))
                if m.group(1) not in GENERATED_BY_KEYS:
                    err(ln, f"generated_by.{m.group(1)} is not allowed: generated_by holds only tool, "
                        "model and session")
        for k in GENERATED_BY_KEYS:
            ln, v = sub.get(k, (fm["generated_by"][0], None))
            if v is None or not quoted(v) or v == '""' or "${" in v:
                err(ln, f"generated_by.{k} must be a non-empty quoted string")

    # --- whole-document checks ---------------------------------------------------------
    for i, line in enumerate(lines, 1):
        for m in re.finditer(r"\bhash:\s*([^\s,}]+)", line):
            if m.group(1) != "null":
                err(i, "every hash must be null")
        if "<!--" in line:
            err(i, "leftover HTML comment")
        for token, what in (("BRN-000", "the allocated ID"), ("YYYY-MM-DD", "today's date")):
            if token in line:
                err(i, f"leftover template placeholder {token}: replace it with {what}")
        if i > fm_end:
            for m in PLACEHOLDER.finditer(line):
                if not INLINE_HTML.fullmatch(m.group(0)):
                    err(i, f"leftover template placeholder {m.group(0)!r}: replace it with content or "
                        "[NEEDS CLARIFICATION: question]")

    pos = fm_end
    for heading in SECTIONS:
        try:
            pos = lines.index(heading, pos) + 1
        except ValueError:
            err(0, f"missing or out-of-order section heading {heading!r}")

    # --- Change Log: the newest row names its session ------------------------------------
    try:
        log_start = lines.index("## Change Log", fm_end)
    except ValueError:
        log_start = None
    if log_start is not None:
        rows = []
        for i in range(log_start + 1, len(lines)):
            line = lines[i].strip()
            if line.startswith("## "):
                break
            if line.startswith("|") and not re.match(r"^\|\s*(Version|-+)\s*\|", line):
                rows.append((i + 1, [c.strip() for c in line.strip("|").split("|")]))
        if not rows:
            err(log_start + 1, "Change Log has no rows")
        else:
            ln, cells = rows[-1]
            author = cells[2] if len(cells) > 2 else ""
            if not author:
                err(ln, "last Change Log row has no author: write 'claude-code (session ID)' with the ID "
                    "from generated_by.session, or the name of the person who made the change")
            elif author.startswith("claude-code"):
                m = re.fullmatch(r"claude-code \(session ([A-Za-z0-9-]+)\)", author)
                session = (fm.get("generated_by") and next(
                    (value_of(l.split(":", 1)[1]) for _, l in nested["generated_by"]
                     if l.strip().startswith("session:")), None))
                if not m:
                    err(ln, "last Change Log row: author must be 'claude-code (session <ID>)'")
                elif session and m.group(1) != session.strip('"'):
                    err(ln, "last Change Log row: session must match generated_by.session")

    # --- item blocks -------------------------------------------------------------------
    items = {c: [] for c in COLLECTIONS}  # collection -> list of (line, id, fields)
    i = fm_end
    while i < len(lines):
        if lines[i].rstrip() != "```yaml items":
            i += 1
            continue
        start = i + 1
        try:
            end = next(j for j in range(start, len(lines)) if lines[j].startswith("```"))
        except StopIteration:
            err(start, "unclosed yaml items fence")
            break
        block = lines[start:end]
        collection, item = None, None
        reported = content = unindented = False
        for off, line in enumerate(block):
            ln = start + off + 1
            if not line.strip() or line.lstrip().startswith("#"):
                continue
            if "<!--" in line:
                continue  # already reported
            content = True
            if not line[0].isspace() and not (collection and line.startswith("- ")):
                key = line.split(":", 1)[0]
                if collection is None:
                    if key not in COLLECTIONS or line.rstrip() != key + ":":
                        err(ln, f"top-level key {key!r} is not problems, ideas or assumptions")
                        reported = True
                        break
                    collection = key
                else:
                    err(ln, f"second top-level key {key!r} in one item block: put each collection in its "
                        "own yaml items fence")
                continue
            if not line[0].isspace() and not unindented:
                err(ln, f"list items must be indented under '{collection}:' (write '  - id: ...', as the "
                    "template does)")
                unindented = True
            m = re.match(r"^(\s*)- id:(.*)$", line)
            if m:
                item = {"line": ln, "id": value_of(m.group(2)), "indent": len(m.group(1)) + 2, "fields": {}}
                items.setdefault(collection, []).append(item)
                continue
            m = re.match(r"^(\s+)([A-Za-z_][\w-]*):(.*)$", line)
            if item and m and len(m.group(1)) == item["indent"]:
                item["fields"][m.group(2)] = (ln, value_of(m.group(3)), [])
                item["last"] = m.group(2)
                continue
            if item and item.get("last"):
                item["fields"][item["last"]][2].append((ln, line.strip()))
        if collection is None and not reported:
            err(start, "item block has no top-level key: start it with problems:, ideas: or assumptions:"
                if content else "empty yaml items block")
        i = end + 1

    prb_ids = {it["id"] for it in items["problems"]}
    for collection, spec in COLLECTIONS.items():
        seen = []
        for it in items[collection]:
            ln, iid, fields = it["line"], it["id"], it["fields"]
            if not re.fullmatch(spec["prefix"] + r"-\d{2}", iid):
                err(ln, f"{iid!r} does not match {spec['prefix']}-NN")
            if iid in seen:
                err(ln, f"duplicate id {iid}")
            seen.append(iid)
            allowed = COMMON | set(spec["required"])
            for f, (fln, _, _) in fields.items():
                if f not in allowed:
                    err(fln, f"field {f!r} is not allowed in {collection}")
            st = fields.get("status")
            if not st or st[1] not in {"active", "deprecated"}:
                err(ln, f"{iid}: status must be active or deprecated")
            for f in spec["required"]:
                if f not in fields:
                    err(ln, f"{iid}: missing field {f!r}")
            for f in spec["quoted"]:
                if f in fields and not quoted(fields[f][1]):
                    err(fields[f][0], f"{iid}: {f} must be a quoted string")
            for f, allowed_values in spec["enums"].items():
                if f in fields and fields[f][1] not in allowed_values:
                    err(fields[f][0], f"{iid}: {f} must be one of {sorted(allowed_values)}")
            if collection == "ideas":
                if "addresses" in fields:
                    fln, inline, sub = fields["addresses"]
                    if inline:
                        err(fln, f"{iid}: addresses must be a block list (- PRB-NN), not {inline!r}")
                    refs = [value_of(s[1][2:]) for s in sub if s[1].startswith("- ")]
                    if not refs and not inline:
                        err(fln, f"{iid}: addresses must name at least one problem")
                    for r in refs:
                        if r not in prb_ids:
                            err(fln, f"{iid}: addresses {r!r}, which is not a defined problem")
                for f in ("value", "effort", "risk"):
                    if f in fields:
                        v = fields[f][1]
                        if not (v == "null" or quoted(v) or NUMBER.match(v)):
                            err(fields[f][0], f"{iid}: {f} must be null, a quoted rating or a number")
                if "score" in fields:
                    v = fields["score"][1]
                    if not (v == "null" or NUMBER.match(v)):
                        err(fields["score"][0], f"{iid}: score must be null or a number")
                if "disposition" in fields and "reason" in fields:
                    d, r = fields["disposition"][1], fields["reason"][1]
                    if d == "open" and r != "null":
                        err(fields["reason"][0], f"{iid}: reason must be null while disposition is open")
                    if d != "open" and not quoted(r):
                        err(fields["reason"][0], f"{iid}: a decided disposition needs a quoted reason")
        nums = [int(x.split("-")[1]) for x in seen if re.fullmatch(spec["prefix"] + r"-\d{2}", x)]
        if nums != list(range(1, len(nums) + 1)):
            err(0, f"{collection} IDs must be numbered from 01 in order, got {seen}")
    if not items["problems"]:
        err(0, "no problems recorded")
    if not items["ideas"]:
        err(0, "no ideas recorded")

    # --- new-shape checks (a BRN with the project-kind line) ----------------------------
    kind = new_shape_kind(lines, fm_end)
    if kind is not None:
        sources = check_intake(lines, fm_end, (list_of("sources") or []) if "sources" in fm else [],
                               items, err)
        check_brownfield(lines, kind, stem, (list_of("upstream") or []) if "upstream" in fm else [],
                         sources, items, err)

    # --- the first release cut and the assumption risk ranking (new-shape BRNs) ----------
    sources = list_of("sources") if "sources" in fm else None
    check_mvp_path(lines, fm_end, fm, [x for _, x in sources or []], items, err)

    # --- optional YAML syntax check ----------------------------------------------------
    try:
        import yaml  # type: ignore
    except ImportError:
        yaml = None
    if yaml is not None:
        # safe_load also raises plain exceptions, such as ValueError for 2026-13-45; report them all,
        # on one line, except a date error the calendar check above already reported.
        try:
            yaml.safe_load("\n".join(lines[1:fm_end]))
        except Exception as e:
            if not (bad_date and not isinstance(e, yaml.YAMLError)):
                err(2, f"frontmatter YAML does not parse: {' '.join(str(e).split())}")
        for j, line in enumerate(lines):
            if line.rstrip() == "```yaml items":
                end = next((k for k in range(j + 1, len(lines)) if lines[k].startswith("```")), len(lines))
                try:
                    yaml.safe_load("\n".join(lines[j + 1:end]))
                except Exception as e:
                    err(j + 2, f"item block YAML does not parse: {' '.join(str(e).split())}")
    return errors


MV_RANK_HEAD = ["Rank", "Assumption", "If wrong", "Confidence", "Cheapest test"]
MV_CUT_HEAD = ["Idea", "In first release", "Why"]
MV_NO_ROWS = "No idea is promoted or proposed for promotion."
MV_FLAG = "Needs review: no rule supports this value."
MV_PROTOTYPE = (
    "prototype", "prototypes", "mock-up", "mock-ups", "mockup", "mockups", "pilot", "pilots", "trial",
    "trials", "beta", "demo", "demos", "experiment", "experiments", "a/b", "landing page", "smoke test",
    "fake door", "build", "launch",
)
MV_INTERVIEW = (
    "ask", "asks", "interview", "interviews", "survey", "surveys", "poll", "polls", "observe", "shadow",
    "talk to", "speak to", "questionnaire", "focus group", "workshop",
)
MV_IMPACT = {"Fatal": 3, "Serious": 2, "Minor": 0}
MV_DOUBT = {"low": 3, "medium": 2, "high": 1}
MV_KINDS = {"high": ("data", "document", "ticket"), "medium": ("interview", "url", "note")}
MV_IF_WRONG = re.compile(
    r"(Fatal|Serious): stops (IDEA-\d{2}(?:, IDEA-\d{2})*) \((\d+) of (\d+) in the cut table\)\."
    r"|(Minor): stops no idea in the cut table \(0 of (\d+)\)\.")
MV_STATUS = re.compile(
    r"First release cut: (?:proposed, not confirmed|confirmed on (\d{4}-\d{2}-\d{2}))")


def cheapest_test(asm_id, validation):
    """The 'Cheapest test' cell (C-07) for an assumption's quoted `validation` value."""
    text = validation[1:-1].replace('\\"', '"').replace("|", "/").strip() if quoted(validation) else ""
    if not text or text.startswith("[NEEDS CLARIFICATION:"):
        return f"[NEEDS CLARIFICATION: how to test {asm_id}]"
    m = re.search(r"[.?!](?= |$)", text)
    sentence = text[:m.end()] if m else text + "."
    low = sentence.lower()

    def has(words):
        return any(re.search(r"(?<![a-z0-9])" + re.escape(w) + r"(?![a-z0-9])", low) for w in words)

    kind = "Prototype" if has(MV_PROTOTYPE) else "Interview" if has(MV_INTERVIEW) else "Data"
    return f"{kind}: {sentence}"


def check_mvp_path(lines, fm_end, fm, sources, items, err):
    """MV-01 to MV-12: the assumption risk ranking (C-07) and the first release cut (C-05)."""
    plain, inside = [], False  # indexes of the lines after the frontmatter and outside every fence
    for i in range(fm_end + 1, len(lines)):
        if lines[i].startswith("```"):
            inside = not inside
        elif not inside:
            plain.append(i)
    if not any(" ".join(lines[i].lower().split()).startswith("project kind:") for i in plain):
        return  # an earlier-shape BRN: none of these checks applies

    def at(text):
        return [i for i in plain if lines[i].rstrip() == text]

    def block(i, stop):
        """Non-blank lines after heading line i, up to a heading, a line `stop` accepts, or the end."""
        out = []
        for j in plain:
            if j > i:
                if lines[j].startswith("#") or stop(lines[j]):
                    break
                if lines[j].strip():
                    out.append(j)
        return out

    def cells(i):
        s = lines[i].strip()
        return [c.strip() for c in s[1:-1].split("|")] if len(s) > 1 and s[0] == "|" == s[-1] else None

    def table(rows, head, what, mv):
        """The data rows [(index, cells)] of the table that starts at rows[0], or None once reported."""
        if not rows or cells(rows[0]) != head:
            err((rows[0] if rows else 0) + 1,
                f"{what}: the table must start with the header row '| {' | '.join(head)} |' ({mv})")
            return None
        if len(rows) < 3 or not re.fullmatch(r"\|(\s*:?-+:?\s*\|)+", lines[rows[1]].strip()):
            err(rows[0] + 1,
                f"{what}: a |---| row and at least one row must follow the header row ({mv})")
            return None
        out = []
        for i in rows[2:]:
            c = cells(i)
            if c is None or len(c) != len(head):
                err(i + 1, f"{what}: each row has exactly {len(head)} cells, with no '|' inside a cell, "
                    f"and nothing else follows the table ({mv})")
                return None
            out.append((i, c))
        return out

    def active(collection):
        return [it for it in items[collection] if it["fields"].get("status", (0, ""))[1] == "active"]

    def field(it, name):
        return it["fields"].get(name, (0, ""))[1]

    def score(iid):
        v = field(ideas[iid], "score")
        return float(v) if NUMBER.match(v) else float("-inf")

    sec = [(at(h) or [None])[0] for h in SECTIONS[5:]]
    if None in sec or sorted(sec) != sec:
        return  # a missing or misplaced section heading is already reported
    s6, s7, s8 = sec[:3]
    ideas = {it["id"]: it for it in active("ideas")}
    open_asm = {it["id"]: it for it in active("assumptions") if field(it, "state") == "open"}

    # --- the first release cut (section 6): MV-08, MV-09 ---------------------------------------
    cut, confirmed, status_at, cut_ok = {}, None, 0, False  # cut: idea ID -> (index, yes or no, why)
    heads = at("### First release cut")
    if len(heads) != 1 or not s6 < heads[0] < s7:
        err(s6 + 1, "section 6 must hold exactly one '### First release cut' heading, and no other "
            "section may hold one (MV-08)")
    else:
        rows = block(heads[0], lambda l: False)
        m = MV_STATUS.fullmatch(lines[rows[0]].rstrip()) if rows else None
        if not m:
            err(heads[0] + 1, "the first line under '### First release cut' must be 'First release cut: "
                "proposed, not confirmed' or 'First release cut: confirmed on YYYY-MM-DD' (MV-08)")
        else:
            confirmed, status_at = m.group(1), rows[0] + 1
            if len(rows) == 2 and lines[rows[1]].rstrip() == MV_NO_ROWS:
                data = []
            else:
                data = table(rows[1:], MV_CUT_HEAD, "first release cut", "MV-09")
            cut_ok = data is not None
            for i, (iid, value, why) in data or []:
                if iid not in ideas or field(ideas[iid], "disposition") not in ("promoted", "open"):
                    err(i + 1, f"first release cut: {iid!r} is not an active idea whose disposition is "
                        "promoted or open (MV-09)")
                    cut_ok = False
                elif cut and iid <= max(cut):
                    err(i + 1, "first release cut: rows are in idea ID order, each idea once; "
                        f"{iid} is out of place (MV-09)")
                    cut_ok = False
                if value not in ("yes", "no"):
                    err(i + 1, f"first release cut: 'In first release' for {iid} must be yes or no (MV-09)")
                    cut_ok = False
                cut[iid] = (i, value, why)
            for iid in ideas:
                if cut_ok and field(ideas[iid], "disposition") == "promoted" and iid not in cut:
                    err(heads[0] + 1, f"first release cut: the promoted idea {iid} has no row (MV-09)")
                    cut_ok = False
    yes = [iid for iid in sorted(cut) if cut[iid][1] == "yes"]
    flagged = [iid for iid in sorted(cut) if cut[iid][2] == MV_FLAG]

    # --- the assumption risk ranking (section 7): MV-01 to MV-07 -----------------------------------
    rank, rank_ok = {}, False  # assumption ID -> (rank, the ideas it stops)
    heads = at("### Assumption risk ranking")
    fences = [i for i in range(s7, s8) if lines[i].startswith("```")]
    bullets = [i for i in plain if s7 < i < s8 and lines[i].startswith("- ")]
    if (len(heads) != 1 or not s7 < heads[0] < s8 or (fences and heads[0] < fences[-1])
            or (bullets and heads[0] > bullets[0])):
        err(s7 + 1, "section 7 must hold exactly one '### Assumption risk ranking' heading, after its item "
            "block and before its bullets, and no other section may hold one (MV-01)")
    else:
        rows = block(heads[0], lambda l: l.startswith("- "))
        if len(rows) == 1 and lines[rows[0]].rstrip() == "None.":
            data = []
        else:
            data = table(rows, MV_RANK_HEAD, "assumption risk ranking", "MV-02")
        rank_ok = data is not None
        if rank_ok and sorted(c[1] for _, c in data) != sorted(open_asm):
            want = ", ".join(sorted(open_asm)) or "none, so the line 'None.' replaces the table"
            err(heads[0] + 1, "assumption risk ranking: one row for each active assumption whose state is "
                f"open, and no other row ({want}) (MV-03)")
            rank_ok = False
        kinds = {q[1:].split(": ", 1)[0] for q in sources if ": " in q}
        keys = []
        for n, (i, (r, aid, wrong, conf, test)) in enumerate(data or [], 1):
            if r != str(n):
                err(i + 1, f"assumption risk ranking: Rank counts 1, 2, 3 and so on; row {n} says {r!r} "
                    "(MV-03)")
                rank_ok = False
            m = MV_IF_WRONG.fullmatch(wrong)
            stops = m.group(2).split(", ") if m and m.group(2) else []
            cls = (m.group(1) or m.group(5)) if m else None
            if not m:
                err(i + 1, f"{aid}: 'If wrong' must read 'Fatal: stops IDEA-NN, IDEA-NN (N of M in the cut "
                    "table).', 'Serious: stops IDEA-NN (N of M in the cut table).' or 'Minor: stops no idea "
                    "in the cut table (0 of M).' (MV-04)")
                rank_ok = False
            elif cut_ok:
                want = "Minor" if not stops else "Fatal" if len(stops) == len(cut) else "Serious"
                if (stops != sorted(set(stops)) or any(s not in cut for s in stops) or cls != want
                        or int(m.group(3) or 0) != len(stops) or int(m.group(4) or m.group(6)) != len(cut)):
                    err(i + 1, f"{aid}: 'If wrong' lists rows of the cut table in ID order and counts them "
                        f"against its {len(cut)} row(s): Fatal when it lists every row, Serious when it lists "
                        "some, Minor when it lists none (MV-04)")
                    rank_ok = False
            if conf not in MV_DOUBT:
                err(i + 1, f"{aid}: Confidence must be high, medium or low (MV-05)")
                rank_ok = False
            elif conf != "low" and not kinds & set(MV_KINDS[conf]):
                need = MV_KINDS[conf]
                err(i + 1, f"{aid}: Confidence {conf} needs a sources entry of kind {need[0]}, {need[1]} or "
                    f"{need[2]} (MV-05)")
            want = cheapest_test(aid, field(open_asm[aid], "validation")) if aid in open_asm else test
            if test != want:
                err(i + 1, f"{aid}: 'Cheapest test' must be {want!r} (MV-07)")
            if m and conf in MV_DOUBT:
                rank[aid] = (n, stops)
                keys.append((-MV_IMPACT[cls] * MV_DOUBT[conf], -MV_IMPACT[cls], -MV_DOUBT[conf],
                             -len(stops), aid))
        if rank_ok and keys != sorted(keys):
            order = ", ".join(k[-1] for k in sorted(keys))
            err(heads[0] + 1, f"assumption risk ranking: rows out of order; the order is {order} (MV-06)")
            rank_ok = False

    # --- each row's reason, the top three covered, a confirmed cut: MV-10 to MV-12 -----------------
    if cut_ok and rank_ok:
        top = {a: v for a, v in rank.items() if v[0] <= 3}
        tested, by_user = [], False
        for iid in sorted(cut):
            i, value, why = cut[iid]
            mine = sorted((v[0], a) for a, v in top.items() if iid in v[1])
            ok = False
            m = re.fullmatch(r"Tests (ASM-\d{2}), ranked ([1-3])\.", why)
            if m and value == "yes":
                ok = (int(m.group(2)), m.group(1)) in mine and m.group(1) not in tested
                tested.append(m.group(1))
            m = re.fullmatch(r"Tests (ASM-\d{2}), ranked ([1-3]), which (IDEA-\d{2}) already tests\.", why)
            if m and value == "no":
                ok = (bool(mine) and mine[0] == (int(m.group(2)), m.group(1)) and m.group(3) != iid
                      and m.group(3) in yes and m.group(3) in top[m.group(1)][1])
            m = re.fullmatch(r"Needed by (IDEA-\d{2}), which is in the first release\.", why)
            if m and value == "yes":
                ok = m.group(1) != iid and m.group(1) in yes
            if why == "Highest score; no assumption ranked 1 to 3 picks an idea." and value == "yes":
                ok = iid == max(sorted(cut), key=score) and not any(v[1] for v in top.values())
            if why == "Tests no assumption ranked 1 to 3." and value == "no":
                ok = not mine
            if (why, value) in (("Included by the user.", "yes"), ("Left out by the user.", "no")):
                ok = by_user = True
            if not ok and why != MV_FLAG:
                err(i + 1, f"first release cut: the Why cell of {iid} is not one of the fixed sentences for "
                    f"'{value}', or it does not match the ranking or the other rows (MV-10)")
        for a, v in sorted(top.items()):
            if not by_user and not flagged and v[1] and not set(v[1]) & set(yes):
                err(cut[v[1][0]][0] + 1, f"first release cut: no 'yes' row tests {a}, ranked {v[0]}; one of "
                    f"{', '.join(v[1])} must be in the first release (MV-11)")
        if cut and not yes and not by_user and not flagged:
            err(status_at, "first release cut: a cut that the user did not change has a 'yes' row (MV-11)")
    if confirmed and cut_ok:
        created, updated = (fm.get(k, (0, ""))[1] for k in ("created", "updated"))
        try:
            real = bool(datetime.date.fromisoformat(confirmed))
        except ValueError:
            real = False
        if not real or not created <= confirmed <= updated:
            err(status_at, "first release cut: the date of a confirmed cut is a real date from created to "
                "updated (MV-12)")
        if flagged:
            err(cut[flagged[0]][0] + 1, "first release cut: a confirmed cut holds no row that says "
                f"'{MV_FLAG}'; flagged: {', '.join(flagged)} (MV-12)")
        loose = [iid for iid in sorted(cut) if field(ideas[iid], "disposition") != "promoted"]
        if loose or not cut:
            err(status_at, "first release cut: confirmed only when the table has a row and every row's idea "
                f"is promoted; not promoted: {', '.join(loose) or 'there is no row'} (MV-12)")


def main(argv):
    if len(argv) != 2:
        print(__doc__.strip().splitlines()[2])
        return 2
    path = argv[1]
    if not os.path.isfile(path):
        print(f"line 0: file not found: {path}")
        return 1
    errors = check(path)
    for line, msg in sorted(set(errors)):
        print(f"line {line}: {msg}")
    if errors:
        print(f"{len(set(errors))} problem(s) in {path}")
        return 1
    print(f"OK: {path}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
