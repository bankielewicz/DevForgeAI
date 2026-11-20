# Brownfield iteration

**Status:** proposal, written 2026-11-18 by claude-code on the model Fable 5.2 (session
fa59a935-ed2e-4502-b6c4-93bb6d847546) for Bryan's review. It changes nothing until SPEC-001's next version is
approved and built. Read [README.md](README.md) first: this document uses its rules (R1 to R10), its shapes (C-01
to C-11), its gate and its IDs without repeating them. It is the third of the four documents built as SKL-001
version 13 (README section 8), after [intake-and-evidence.md](intake-and-evidence.md), whose project kind,
sources and citation rule it builds on.

## Workflow steps this changes

| Step (SKILL.md's line, unchanged) | Today | Added by this document |
|---|---|---|
| 1. Intake: topic, existing BRNs, clarifying questions | Topic; extend or new; up to three questions | Brownfield: extend-or-new asked only for a draft BRN; the project's documents and earlier BRNs read, read-only, and recorded (C-02, `upstream`, `sources`) |
| 3. Diverge: problems, ideas, assumptions | Problems, 5 to 15 ideas, assumptions | Brownfield: covered and previously decided candidates kept out of `ideas` (C-06); parked ideas offered once; earlier open assumptions shown |
| 5. Propose dispositions and ask the user to confirm | Two questions: dispositions, convergence | Brownfield: proposed assumption updates (C-11) and, when there is one, C-10's question 4 |
| 6. Write the BRN | Template, frontmatter, Change Log | Brownfield: C-02, C-06 and C-11 written; one `informed_by` record per document read |
| 7. Validate the BRN | `validate_brn.py`, then the read-back | Validator checks BV-01 to BV-05; the read-back also covers C-11's status cells and assumption states |

## 1. Scope

**In.** What a run does when the project kind is brownfield, decided or worked with (intake-and-evidence.md,
BEH-20):

- which documents it reads, in which order, with which cap, and what it takes from each;
- the Existing product table (C-02), the `upstream` records and the `sources` entries for them;
- the test for "already covered" and for "previously decided", what happens to such a candidate idea, and
  how the user overrides it (C-06);
- how parked ideas of earlier BRNs are offered and recorded when taken up;
- how assumptions of earlier BRNs are shown, how a change of state is proposed and confirmed (C-11, C-10's
  question 4), and where a confirmed change lives;
- extend versus new for a brownfield run, and extending a brownfield BRN;
- documents that can't be read, and a brownfield project with nothing to read;
- validator checks BV-01 to BV-05, their unit tests, the reference `references/brownfield.md` and an example.

**Out.**

- Deciding the kind, the question sets, sources and citations: intake-and-evidence.md.
- The `improve-existing` framework and its selection: [framework-catalog.md](framework-catalog.md).
- The first release cut and the risk ranking: [mvp-and-prototype-path.md](mvp-and-prototype-path.md).
- What the PRD skill does with C-02, C-06 and C-11: [prd-handoff-contract.md](prd-handoff-contract.md).
- Reading source code, ADRs, stories or specs on the skill's own account (a project file the user names as a
  source is read under intake-and-evidence.md, BEH-22); editing any document other than the BRN being written.
- A BRN without the project-kind line: nothing here applies to it, also when it is extended (the gate).

## 2. Changes by file

Each edit is exact (R7). This document is built after intake-and-evidence.md, so where it changes a passage
that document already changed, its old text is that document's new text. Every old text below was checked
against version 11 of the files with framework-catalog.md's and intake-and-evidence.md's edits applied, and on
2026-11-20 against version 12's (section 5, "What was checked").

An old or new text in a `python` block is whole lines with their indentation: the new lines replace the old
lines. In a `text` block the old text may start in the middle of a line; what stands before and after it on
its lines stays.

### 2.1 `docs/specs/spec/SPEC-001.md` (its next version)

BEH-05, BEH-06 and ERR-01 are extended. BEH-25 to BEH-29, ERR-08, ERR-09 and VER-30 to VER-34 are added
(sections 3 to 5). Section 3's tree gains `references/brownfield.md`; section 5's Tools gain nothing (Glob and
Read are already listed). SPEC-001 version 19, drafted before the build, makes these changes, edits B-P1 to
B-P3 among them; the build's third commit doesn't repeat them.

**Edit B-P1** — `docs/specs/spec/SPEC-001.md` (BEH-05's rule)

Old text:

```text
During divergence, record the user's ideas in their own words alongside generated ones.
```

New text:

```text
During divergence, record the user's ideas in their own words alongside generated ones. In a brownfield run, a suggestion that a document read already covers, or that an earlier BRN rejected, is not added to ideas, the user's own included: it is listed in section 6 and the user is told, and it is added when the user then says to add it (BEH-26).
```

**Edit B-P2** — `docs/specs/spec/SPEC-001.md` (ERR-01's condition)

Old text:

```text
condition: "A BRN on the same or a closely similar topic already exists"
```

New text:

```text
condition: "A BRN on the same or a closely similar topic already exists; when the user's words say the product exists, only one whose status is draft counts (BEH-29)"
```

**Edit B-P3** — `docs/specs/spec/SPEC-001.md` (BEH-06's rule)

Old text:

```text
Both questions are tagged step 5 (BEH-12).
```

New text:

```text
Both questions are tagged step 5 (BEH-12). In a brownfield run whose Assumption updates table has a row, the same form ends with the question 'Confirm these assumption updates?', and only its answer confirms a row (BEH-28).
```

### 2.2 `src/claude/DevForgeAI/skills/brainstorm/SKILL.md`

Ten edits. They add 20 lines to the file (348 to 368, after framework-catalog.md's and intake-and-evidence.md's
edits).

**Edit B-S1** — `src/claude/DevForgeAI/skills/brainstorm/SKILL.md` (Decisions that belong to the user)

Old text:

```text
Two decisions are the user's, never yours:

- **Each idea's disposition** (`promoted`, `parked` or `rejected`) and its `reason`.
- **Convergence**: whether the brainstorm is finished (`status: converged`).
```

New text:

```text
These decisions are the user's, never yours:

- **Each idea's disposition** (`promoted`, `parked` or `rejected`) and its `reason`.
- **Convergence**: whether the brainstorm is finished (`status: converged`).
- **Each assumption update** in a brownfield BRN: its `confirmed on` status and the changed `state`.
```

**Edit B-S2** — `src/claude/DevForgeAI/skills/brainstorm/SKILL.md` (step 1, item 2)

Old text:

```text
Never overwrite an existing BRN silently.
```

New text:

```text
Never overwrite an existing BRN silently. When the user's words
   say the product exists, only a BRN whose `status` is `draft` counts as on the same topic
   ([brownfield.md](references/brownfield.md#extend-or-new)).
```

**Edit B-S3** — `src/claude/DevForgeAI/skills/brainstorm/SKILL.md` (step 1, item 3; the old text is edit A-S2's)

Old text:

```text
When it can't be asked or isn't answered, the kind stays
   undecided and intake.md says which kind to work with.
```

New text:

```text
When it can't be asked or isn't answered, the kind stays
   undecided and intake.md says which kind to work with. When that kind is brownfield, next read the
   project's documents and earlier BRNs, read-only ([brownfield.md](references/brownfield.md)).
```

**Edit B-S4** — `src/claude/DevForgeAI/skills/brainstorm/SKILL.md` (step 3)

Old text:

```text
- Capture **assumptions** (`ASM-NN`): beliefs the ideas depend on, each with how to validate it.
```

New text:

```text
- Capture **assumptions** (`ASM-NN`): beliefs the ideas depend on, each with how to validate it.
- **Brownfield.** Keep out of `ideas` what a document read already covers or an earlier BRN rejected,
  the user's suggestions included; list it for section 6 and tell the user. Offer earlier parked ideas
  once and show earlier open assumptions ([brownfield.md](references/brownfield.md#already-covered)).
```

**Edit B-S5** — `src/claude/DevForgeAI/skills/brainstorm/SKILL.md` (step 5, the form: C-10's question 4)

Old text:

```text
2. "Has the brainstorm converged?", options `Converged` and `Not yet`.
```

New text:

```text
2. "Has the brainstorm converged?", options `Converged` and `Not yet`.
3. "Confirm these assumption updates?", only when a brownfield BRN's *Assumption updates* table has
   a row: options `Accept all as proposed` and `Leave them proposed`, each option's `preview` holding
   the table. Changes come typed under Other.
```

The item is numbered 3 here. mvp-and-prototype-path.md, built next, rewrites the list once: it inserts its
first-release-cut question as 3 and renumbers this one to 4, README C-10's final order (the lead's decision,
2026-11-18). The line of question 2 stays unchanged so that document can anchor on it.

**Edit B-S6** — `src/claude/DevForgeAI/skills/brainstorm/SKILL.md` (step 5, what the answers write)

Old text:

```text
- Set `status: converged` only on *Converged*; otherwise `draft`.
```

New text:

```text
- Set `status: converged` only on *Converged*; otherwise `draft`.
- **Brownfield.** Before the form, propose assumption updates, each from a stated fact with a source.
  A row is `confirmed on <today>` only on *Accept all as proposed* or typed text confirming it;
  else `proposed, not confirmed` ([brownfield.md](references/brownfield.md#assumption-updates)).
```

**Edit B-S7** — `src/claude/DevForgeAI/skills/brainstorm/SKILL.md` (step 6, item 2; the old text is edit A-S4's)

Old text:

```text
keep or delete the template's brownfield-only parts as its first comment says.
```

New text:

```text
keep or delete the template's brownfield-only parts as its first comment says. Fill the parts
   kept as [brownfield.md](references/brownfield.md) says.
```

**Edit B-S8** — `src/claude/DevForgeAI/skills/brainstorm/SKILL.md` (step 6, item 3; the old text is edit A-S5's)

Old text:

```text
- `upstream` and `participants`: fill from the conversation, or leave them empty.
```

New text:

```text
- `upstream`: in a brownfield run, one `informed_by` record per document read (brownfield.md);
     otherwise fill from the conversation, or leave it empty.
   - `participants`: fill from the conversation, or leave it empty.
```

**Edit B-S9** — `src/claude/DevForgeAI/skills/brainstorm/SKILL.md` (step 7, item 2)

Old text:

```text
Reset anything else to `disposition: open` with `reason: null`, or to
   `status: draft`.
```

New text:

```text
Reset anything else to `disposition: open` with `reason: null`, or to
   `status: draft`. In a brownfield BRN, check the same way every `confirmed on` cell under
   *Assumption updates* and every assumption `state` this run changed: reset an unconfirmed one to
   `proposed, not confirmed` and to the state it had.
```

**Edit B-S10** — `src/claude/DevForgeAI/skills/brainstorm/SKILL.md` (References; the old text is edit A-S8's)

Old text:

```text
the kind rules, the question sets, the form of `sources`, and sections 3 and 8.
```

New text:

```text
the kind rules, the question sets, the form of `sources`, and sections 3 and 8.
- [references/brownfield.md](references/brownfield.md): read at step 1 when the kind is brownfield:
  what to read, what is kept out of `ideas`, parked ideas and assumption updates.
```

mvp-and-prototype-path.md is built next and also changes the list of the user's decisions, step 5 and step 7's
item 2. Its edits to the decisions list, the question list, the answers' bullets and the read-back start from
lines that B-S1, B-S5, B-S6 and B-S9 keep unchanged as the first line of their new text, so each of its old
texts still occurs once; its S1 is no edit, because B-S1 already made that change.

### 2.3 `src/claude/DevForgeAI/skills/brainstorm/references/output-rules.md`

**Edit B-O1** — `src/claude/DevForgeAI/skills/brainstorm/references/output-rules.md` (Frontmatter, `upstream`)

Old text:

```text
| `upstream` | `[]`, or link records (usually `relation: informed_by`) |
```

New text:

```text
| `upstream` | `[]`, or link records (usually `relation: informed_by`); in a brownfield BRN, one per document read |
```

**Edit B-O2** — `src/claude/DevForgeAI/skills/brainstorm/references/output-rules.md` (the brownfield parts; the old text is edit A-O5's)

Old text:

```text
with none, the single line `- None.` |
```

New text:

```text
with none, the single line `- None.` |

A BRN whose kind is `brownfield` also holds the four parts below; a `greenfield` BRN holds none of
them; while the kind is not decided it holds all four when the run worked as brownfield and none
when it worked as greenfield. [brownfield.md](brownfield.md) says how to fill each.

| Part | Form |
|---|---|
| `### Existing product`, in section 1 after the context prose | The table `\| Document \| Version \| What it already covers \|`, one row per document read (a BRN, PRD, EPIC or ARCH ID, never this BRN; its version), or the line `No document was found in the project.`; then any `Skipped: <path> (<reason>)` lines. Each row's document has an `upstream` record `{id: <ID>, relation: informed_by, version: <version>, hash: null}` and the `sources` entry `"document: docs/specs/<folder>/<ID>.md v<version>"` |
| `### Already covered`, in section 6 | The table `\| Suggestion \| Covered by \|`, `Covered by` being `PRD-NNN#FR-NNN`, `PRD-NNN#NFR-NNN`, `EPIC-NNN#DW-NN` or `ARCH-NNN#CMP-NN` of a document Existing product lists; or the line `None.` |
| `### Previously decided`, in section 6 | The table `\| Idea \| Decision \| Where \|`, `Decision` being `rejected` or `parked` and `Where` `BRN-NNN#IDEA-NN` of a BRN Existing product lists, each once; or the line `None.` An idea of this BRN that carries an item-level `upstream` link to such an idea is not listed |
| `### Assumption updates`, last in section 6 | The table `\| Earlier assumption \| Change \| Evidence \| Status \|`: `BRN-NNN#ASM-NN` of a BRN Existing product lists, or of this BRN, each once; `open to validated` or `open to invalidated`; a fact ending with one `sources` entry in parentheses; `proposed, not confirmed` or `confirmed on YYYY-MM-DD`. Or the line `None.` |

Section 6's subsections stand in this order: First release cut, Already covered, Previously
decided, Assumption updates.
```

**Edit B-O3** — `src/claude/DevForgeAI/skills/brainstorm/references/output-rules.md` (Validation checklist, item 13; the old text is edit A-O6's)

Old text:

```text
section 8 has one bullet per first-release idea, or the line `- None.`
```

New text:

```text
section 8 has one bullet per first-release idea, or the line `- None.`
13. In a brownfield BRN: `### Existing product` in section 1 and `### Already covered`,
    `### Previously decided` and `### Assumption updates` in section 6, in that order, each
    holding its table or its replacement line; every document of Existing product has its
    `upstream` record and its `sources` entry; every `Covered by` and `Where` cites a listed
    document; every Evidence cell ends with a `sources` entry; and every `confirmed on` status is
    one the user confirmed. A greenfield BRN has none of the four headings.
```

### 2.4 `src/claude/DevForgeAI/skills/brainstorm/references/work-file.md`

**Edit B-W1** — `src/claude/DevForgeAI/skills/brainstorm/references/work-file.md` (Its shape; the old text is edit A-W1's)

Old text:

```text
section 7 holds the bullet that names the kind the run works as, from the first save.
```

New text:

```text
section 7 holds the bullet that names the kind the run works as, from the first save.
- In a brownfield run, from the first save: section 1's *Existing product*, the `upstream` records,
  and in section 6, after the not-reached marker, *Already covered* and *Previously decided*. At the
  step-5 save: *Assumption updates*, every row `proposed, not confirmed`
  ([brownfield.md](brownfield.md)).
```

**Edit B-W2** — `src/claude/DevForgeAI/skills/brainstorm/references/work-file.md` (Continuing a run, item 1; the old text is edit A-W2's)

Old text:

```text
and don't ask the kind
   question or the clarifying questions again.
```

New text:

```text
and don't ask the kind
   question or the clarifying questions again. A brownfield run reads the project's documents again,
   keeps the file's section 6 rows, and offers parked ideas only when the file has no
   `### Previously decided` heading.
```

### 2.5 `src/claude/DevForgeAI/skills/brainstorm/references/brownfield.md` (new)

Copied from [staged/skills/brainstorm/references/brownfield.md](staged/skills/brainstorm/references/brownfield.md).

### 2.6 `src/claude/DevForgeAI/skills/brainstorm/scripts/validate_brn.py`

Two edits add the checks of section 3.8. They use the helpers that intake-and-evidence.md's edit A-V1 added,
only the standard library, and string comparison, so the verdict is the same with and without PyYAML.

**Edit B-V1** — `src/claude/DevForgeAI/skills/brainstorm/scripts/validate_brn.py` (new functions before `check`)

Old text:

```python
def check(path):
```

New text:

```python
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
```

**Edit B-V2** — `src/claude/DevForgeAI/skills/brainstorm/scripts/validate_brn.py` (the call; the old text is edit A-V2's)

Old text:

```python
        sources = check_intake(lines, fm_end, (list_of("sources") or []) if "sources" in fm else [],
                               items, err)
```

New text:

```python
        sources = check_intake(lines, fm_end, (list_of("sources") or []) if "sources" in fm else [],
                               items, err)
        check_brownfield(lines, kind, stem, (list_of("upstream") or []) if "upstream" in fm else [],
                         sources, items, err)
```

### 2.7 `src/tests/brainstorm/test_validate_brn.py`

Written before the validator changes. The brownfield fixture is the staged example BRN-002, read from its
destination, so the example is tested with every run of the file.

**Edit B-T1** — `src/tests/brainstorm/test_validate_brn.py` (the brownfield fixtures; the old text is edit A-T2's)

Old text:

```python
NEW_UNDECIDED = edit(NEW_UNDECIDED, QUESTION, WORKED_AS % "greenfield" + "\n" + QUESTION)
```

New text:

```python
NEW_UNDECIDED = edit(NEW_UNDECIDED, QUESTION, WORKED_AS % "greenfield" + "\n" + QUESTION)

# A brownfield new-shape BRN: the staged example, checks BV-01 to BV-05 (brownfield-iteration.md).
BROWN = (ROOT / "src/staging/examples/brainstorm-brownfield/BRN-002.md").read_text(encoding="utf-8")
PRODUCT = ("| Document | Version | What it already covers |\n|---|---|---|\n"
           "| BRN-001 | 1 | Reducing appointment no-shows at the dental clinic: 6 ideas (2 promoted, 2 parked, "
           "2 rejected, 0 open) |\n"
           "| PRD-001 | 3 | Online booking for returning patients (FR-001 to FR-006) |")
COVERED = "| Suggestion | Covered by |\n|---|---|\n| Text reminders before a visit | PRD-001#FR-003 |"
DECIDED = ("| Idea | Decision | Where |\n|---|---|---|\n"
           "| Open a waitlist for freed slots. | parked | BRN-001#IDEA-05 |\n"
           "| Charge a deposit at booking. | rejected | BRN-001#IDEA-06 |")
UPDATE = ("| BRN-001#ASM-01 | open to validated | 8 of 10 reminder texts were opened within a day (data: "
          "reminder pilot export, October 2026) | confirmed on 2026-11-18 |")
UPDATES = "| Earlier assumption | Change | Evidence | Status |\n|---|---|---|---|\n" + UPDATE
# The same BRN in a project with no document to read (ERR-09).
BROWN_ALONE = edit(BROWN, "upstream:\n  - {id: BRN-001, relation: informed_by, version: 1, hash: null}\n"
                   "  - {id: PRD-001, relation: informed_by, version: 3, hash: null}\n", "upstream: []\n")
BROWN_ALONE = edit(BROWN_ALONE, '  - "document: docs/specs/brainstorm/BRN-001.md v1"\n'
                   '  - "document: docs/specs/prd/PRD-001.md v3"\n', "")
BROWN_ALONE = edit(BROWN_ALONE, PRODUCT, "No document was found in the project.")
BROWN_ALONE = edit(BROWN_ALONE, "    upstream:\n      - {id: BRN-001, item: IDEA-04, relation: informed_by, "
                   "version: 1, hash: null}\n", "")
for _table in (COVERED, DECIDED, UPDATES):
    BROWN_ALONE = edit(BROWN_ALONE, _table, "None.")
```

**Edit B-T2** — `src/tests/brainstorm/test_validate_brn.py` (the new tests; the old text is edit A-T3's)

Old text:

```python
        code, lines = self.run_text(VALID)
        self.assertEqual((code, len(lines)), (0, 1), lines)
```

New text:

```python
        code, lines = self.run_text(VALID)
        self.assertEqual((code, len(lines)), (0, 1), lines)

    # --- Brownfield BRNs: checks BV-01 to BV-05 (brownfield-iteration.md) ------------------------

    def brown_valid(self, text):
        code, lines = self.run_text(text, name="BRN-002.md")
        self.assertEqual(code, 0, "\n".join(lines))

    def brown_rejects(self, text, *patterns):
        code, lines = self.run_text(text, name="BRN-002.md")
        return self.assert_invalid(lines, code, *patterns)

    def test_brownfield_example_passes(self):
        self.brown_valid(BROWN)

    def test_brownfield_with_no_document_passes(self):
        self.brown_valid(BROWN_ALONE)

    def test_brownfield_without_assumption_updates_is_rejected(self):
        text = edit(BROWN, "### Assumption updates\n\n" + UPDATES + "\n\n", "")
        errors = self.brown_rejects(text, r"^line 165: a brownfield BRN needs '### Assumption updates' in "
                                    r"section 6 \(BV-01\)$")
        self.assertEqual(len(errors), 1, errors)

    def test_brownfield_without_existing_product_is_rejected(self):
        text = edit(BROWN_ALONE, "### Existing product\n\nNo document was found in the project.\n\n", "")
        self.brown_rejects(text, r"^line 32: a brownfield BRN needs '### Existing product' in section 1 "
                           r"\(BV-01\)$")

    def test_greenfield_with_a_brownfield_heading_is_rejected(self):
        text = edit(BROWN_ALONE, "Project kind: brownfield", "Project kind: greenfield")
        lines = self.brown_rejects(text, r"^line 40: '### Existing product' belongs to a brownfield BRN only: "
                                   r".* \(BV-01\)$")
        self.assertEqual(len(lines), 4, lines)

    def undecided(self, text, worked):
        text = edit(text, "Project kind: brownfield", "Project kind: [NEEDS CLARIFICATION: greenfield or brownfield]")
        return edit(text, "\n- [NEEDS CLARIFICATION: ", "\n" + WORKED_AS % worked + "\n- [NEEDS CLARIFICATION: ")

    def test_undecided_kind_worked_as_brownfield_passes(self):
        self.brown_valid(self.undecided(BROWN, "brownfield"))

    def test_undecided_kind_worked_as_brownfield_needs_every_heading(self):
        text = edit(self.undecided(BROWN_ALONE, "brownfield"), "### Already covered\n\nNone.\n\n", "")
        self.brown_rejects(text, r"^line 156: this run worked as brownfield: '### Already covered' is needed in "
                           r"section 6 \(BV-01\)$")

    def test_undecided_kind_worked_as_greenfield_has_no_brownfield_heading(self):
        lines = self.brown_rejects(self.undecided(BROWN_ALONE, "greenfield"),
                                   r"^line 40: this run worked as greenfield: remove '### Existing product' "
                                   r"\(BV-01\)$")
        self.assertEqual(len(lines), 4, lines)

    def test_brownfield_subsections_out_of_order_are_rejected(self):
        text = edit(BROWN_ALONE, "### Already covered\n\nNone.\n\n### Previously decided\n\nNone.\n\n",
                    "### Previously decided\n\nNone.\n\n### Already covered\n\nNone.\n\n")
        self.brown_rejects(text, r"^line \d+: section 6's subsections must come in this order: .* \(BV-01\)$")

    def test_empty_existing_product_is_rejected(self):
        text = edit(BROWN_ALONE, "No document was found in the project.\n\n", "")
        self.brown_rejects(text, r"^line 40: '### Existing product' must hold its table or the line .* "
                           r"\(BV-02\)$")

    def test_skipped_line_after_the_table_passes(self):
        self.brown_valid(edit(BROWN, PRODUCT, PRODUCT + "\n\nSkipped: docs/specs/prd/PRD-002.md (no frontmatter)"))

    def test_other_text_after_the_table_is_rejected(self):
        text = edit(BROWN, PRODUCT, PRODUCT + "\n\nPRD-002 was unreadable.")
        self.brown_rejects(text, r"^line 51: under '### Existing product', .* \(BV-02\)$")

    def test_existing_product_row_that_is_not_a_document_is_rejected(self):
        text = edit(BROWN, "| PRD-001 | 3 | Online booking", "| ADR-001 | 3 | Online booking")
        self.brown_rejects(text, r"^line 49: Existing product: Document must be a BRN, PRD, EPIC or ARCH ID "
                           r".* \(BV-02\)$")

    def test_document_without_its_upstream_record_is_rejected(self):
        text = edit(BROWN, "  - {id: PRD-001, relation: informed_by, version: 3, hash: null}\n", "")
        self.brown_rejects(text, r"^line 48: PRD-001: the frontmatter's upstream needs the record \{id: PRD-001, "
                           r"relation: informed_by, version: 3, hash: null\} \(BV-02\)$")

    def test_upstream_record_with_another_version_is_rejected(self):
        text = edit(BROWN, "  - {id: PRD-001, relation: informed_by, version: 3, hash: null}",
                    "  - {id: PRD-001, relation: informed_by, version: 2, hash: null}")
        self.brown_rejects(text, r"^line 49: PRD-001: the frontmatter's upstream needs the record .* \(BV-02\)$")

    def test_document_without_its_sources_entry_is_rejected(self):
        text = edit(BROWN, '  - "document: docs/specs/prd/PRD-001.md v3"\n', "")
        self.brown_rejects(text, r'^line 48: PRD-001: sources needs the entry "document: docs/specs/prd/'
                           r'PRD-001\.md v3" \(BV-02\)$')

    def test_document_sources_entries_may_follow_other_entries(self):
        # An extension appends its new entries: the validator checks that each is there, not where.
        entry = '  - "document: docs/specs/prd/PRD-001.md v3"\n'
        note = '  - "note: Dana, conversation of 2026-11-18"\n'
        self.brown_valid(edit(edit(BROWN, entry, ""), note, note + entry))

    def test_covered_by_without_an_item_is_rejected(self):
        text = edit(BROWN, "| PRD-001#FR-003 |", "| PRD-001 |")
        self.brown_rejects(text, r"^line 183: Already covered: Covered by must be .* \(BV-03\)$")

    def test_covered_by_an_unlisted_document_is_rejected(self):
        text = edit(BROWN, "| PRD-001#FR-003 |", "| PRD-009#FR-003 |")
        self.brown_rejects(text, r"^line 183: Already covered: PRD-009#FR-003 cites a document that Existing "
                           r"product does not list \(BV-03\)$")

    def test_already_covered_as_prose_is_rejected(self):
        text = edit(BROWN, COVERED, "Text reminders are covered by PRD-001.")
        self.brown_rejects(text, r"^line 181: '### Already covered' must be the table .* \(BV-03\)$")

    def test_unknown_decision_is_rejected(self):
        text = edit(BROWN, "| parked | BRN-001#IDEA-05 |", "| deferred | BRN-001#IDEA-05 |")
        self.brown_rejects(text, r"^line 189: Previously decided: Decision must be rejected or parked, .* "
                           r"\(BV-04\)$")

    def test_previously_decided_idea_listed_twice_is_rejected(self):
        text = edit(BROWN, "| rejected | BRN-001#IDEA-06 |", "| rejected | BRN-001#IDEA-05 |")
        self.brown_rejects(text, r"^line 190: Previously decided: BRN-001#IDEA-05 is listed twice \(BV-04\)$")

    def test_idea_taken_up_and_still_listed_is_rejected(self):
        text = edit(BROWN, "| parked | BRN-001#IDEA-05 |", "| parked | BRN-001#IDEA-04 |")
        self.brown_rejects(text, r"^line 121: IDEA-03 is linked to BRN-001#IDEA-04, which Previously decided also "
                           r"lists: .* \(BV-04\)$")

    def test_assumption_update_without_a_source_is_rejected(self):
        text = edit(BROWN, " (data: reminder pilot export, October 2026) | confirmed", " | confirmed")
        self.brown_rejects(text, r"^line 196: Assumption updates: Evidence must be a fact that ends with one "
                           r"sources entry in parentheses \(BV-05\)$")

    def test_assumption_update_with_a_marker_as_evidence_is_rejected(self):
        text = edit(BROWN, "8 of 10 reminder texts were opened within a day (data: reminder pilot export, "
                    "October 2026)", "[NEEDS CLARIFICATION: pilot result]")
        self.brown_rejects(text, r"^line 196: Assumption updates: Evidence must be .* \(BV-05\)$")

    def test_unknown_change_is_rejected(self):
        self.brown_rejects(edit(BROWN, "| open to validated |", "| validated |"),
                           r"^line 196: Assumption updates: Change must be .* \(BV-05\)$")

    def test_status_without_a_date_or_with_a_name_is_rejected(self):
        # The second sample is the form of the drafts before 2026-11-20: a cell that names someone is not valid.
        for status in ("confirmed", "confirmed by Dana on 2026-11-18"):
            with self.subTest(status=status):
                self.brown_rejects(edit(BROWN, "| confirmed on 2026-11-18 |\n\n## 7", f"| {status} |\n\n## 7"),
                                   r"^line 196: Assumption updates: Status must be .* \(BV-05\)$")

    def test_status_with_an_impossible_date_is_rejected(self):
        self.brown_rejects(edit(BROWN, "| confirmed on 2026-11-18 |\n\n## 7",
                                "| confirmed on 2026-11-31 |\n\n## 7"),
                           r"^line 196: Assumption updates: Status must be .* \(BV-05\)$")

    def test_proposed_assumption_update_passes(self):
        self.brown_valid(edit(BROWN, "| confirmed on 2026-11-18 |\n\n## 7",
                              "| proposed, not confirmed |\n\n## 7"))

    def test_update_of_an_unlisted_brn_is_rejected(self):
        self.brown_rejects(edit(BROWN, "| BRN-001#ASM-01 | open", "| BRN-007#ASM-01 | open"),
                           r"^line 196: Assumption updates: Earlier assumption must be .* \(BV-05\)$")

    def test_confirmed_update_of_this_brns_assumption_needs_the_new_state(self):
        own = edit(BROWN, UPDATE, UPDATE + "\n" + UPDATE.replace("BRN-001#ASM-01", "BRN-002#ASM-01"))
        self.brown_rejects(own, r"^line 197: Assumption updates: ASM-01 of this BRN must have state validated "
                           r"while its row says 'confirmed' \(BV-05\)$")
        code, lines = self.run_text(edit(own, "    state: open", "    state: validated"), name="BRN-002.md")
        self.assertFalse(any("(BV-05)" in line for line in lines), lines)

    def test_proposed_update_of_this_brns_assumption_keeps_it_open(self):
        own = edit(BROWN, UPDATE, UPDATE + "\n" + UPDATE.replace("BRN-001#ASM-01", "BRN-002#ASM-01").replace(
            "confirmed on 2026-11-18", "proposed, not confirmed"))
        self.brown_valid(own)
        self.brown_rejects(edit(own, "    state: open", "    state: validated"),
                           r"^line 197: Assumption updates: ASM-01 of this BRN must have state open while its row "
                           r"says 'proposed, not confirmed' \(BV-05\)$")
```

The 32 new tests run in each of the file's three classes. Their pinned line numbers are those of the staged
BRN-002: a change to that file moves them.

### 2.8 The example

`src/staging/examples/brainstorm-brownfield/` (new) is copied from
[staged/examples/brainstorm-brownfield/](staged/examples/brainstorm-brownfield/): `README.md`, `BRN-001.md`,
`PRD-001.md` and `BRN-002.md` (section 6).

### 2.9 Eval cases and the runbook

Three new hand-written case folders under `src/claude/DevForgeAI/evals/brainstorm/`:
`brownfield-reads-documents`, `brownfield-keeps-out-covered` and `brownfield-nothing-to-read` (section 5).
VER-34's steps are added to `docs/runbooks/brainstorm-manual-test.md` by a documents change, written on Fable
after the build's commits and before VER-34 is run live (README §8). The existing case `existing-brn` is
unchanged: its request does not say the product exists, so today's test applies and the draft BRN-001 it seeds
is asked about.

## 3. Behaviour

### 3.1 Items

```yaml items
behaviors:
  - id: BEH-25
    status: proposed
    rule:
      - "When the kind is brownfield, decided or worked with (BEH-20), read the project's documents right after the kind is known and before the clarifying questions. Select files by name with Glob, then read each selected file whole with the Read tool, in this order and with these caps: (1) docs/specs/brainstorm/BRN-*.md, the three highest numbers, highest first, never the BRN being extended; (2) docs/specs/prd/PRD-*.md, the two highest numbers, highest first; (3) docs/specs/epic/EPIC-*.md, the four highest numbers, highest first; (4) docs/specs/arch/ARCH-*.md, the highest number. Only a file named <PREFIX>-NNN.md is selected. Nothing else is read for this purpose: no story, no spec, no ADR and no source code is read automatically (Bryan, 2026-11-19: 'Skip automatic story and spec reads.'); a file the user names as a source is read under BEH-22 and is never an Existing product row. At most ten documents."
      - "Every document read is read-only: the skill never edits, repairs, moves or deletes it."
      - "Take from a BRN its title, version, and each active idea's id, idea, disposition and reason and each active assumption's id, statement, validation and state; from a PRD its title, version, section 1 and each active functional and non-functional requirement's id, statement and priority; from an EPIC its title, version and each active done_when item's id and criterion; from an ARCH its title, version and each active component's id, name and responsibility. Copy no disposition, priority or decision into this BRN's items."
      - "For each document read, in the order read, write one frontmatter upstream record with no item, '{id: <ID>, relation: informed_by, version: <its version>, hash: null}', and one sources entry 'document: docs/specs/<folder>/<ID>.md v<its version>', these entries standing before every other sources entry in a BRN this run creates; a run that extends a BRN appends them instead (BEH-29)."
      - "Write '### Existing product' in section 1 after the context prose (C-02): one row per document read, in the order read, with its ID, its version and the third cell of section 3.3; with no document read, the line 'No document was found in the project.' in place of the table."
      - "The context prose says what the product does today only from a PRD's section 1 or the user's words; otherwise it holds '[NEEDS CLARIFICATION: what the product does today]'."
    changes: "new"
    lands_in: "SPEC-001 §6; SKILL.md step 1 item 3 and step 6 (edits B-S3, B-S7, B-S8); references/brownfield.md, 'What to read' and 'Existing product (section 1)'"
  - id: BEH-26
    status: proposed
    rule:
      - "At step 3, test every candidate idea before it gets an ID: each suggestion of the user's and each idea the skill generates."
      - "A candidate is already covered when one item taken from a PRD, EPIC or ARCH read, as it is written, already gives the same people the same result. The items that count are active functional and non-functional requirements whose priority is not wont, active done_when items and active components. PRD items are checked first, then EPIC, then ARCH, each in ID order, and the first that covers the candidate is cited. A candidate covered only in part is not covered. Section 3.4 gives the test's examples."
      - "A candidate is previously decided when it proposes the same action for the same people as an active idea of a BRN read whose disposition is rejected. Section 3.5 gives the test's examples."
      - "A covered or previously decided candidate is not added to ideas, the user's own suggestion included. A covered one is a row of '### Already covered' (its wording, and '<document ID>#<item ID>'), in the order the candidates came up. A previously decided one is a row of '### Previously decided' (the earlier idea's text, 'rejected', 'BRN-NNN#IDEA-NN'). Each table is replaced by the line 'None.' when it has no row (C-06)."
      - "The skill reports every candidate kept out with the exact ID, and never asks about it (Bryan, 2026-11-19: 'Report covered suggestions with the exact requirement ID and let me say \"add it anyway\" without prompting.'). When step 3's work is done, the reply holds one line per candidate kept out, in the order they came up: for a covered one, 'Not added, already covered by <document ID>#<item ID>: \"<the suggestion>\"'; for a previously decided one, 'Not added, rejected in BRN-NNN#IDEA-NN: \"<the suggestion>\"'. After the lines comes, once, the sentence 'Say \"add it anyway\" to add one.' The final reply's discussion repeats the lines and the sentence for every candidate still kept out. No question, in a form or in text, is ever asked about a kept-out candidate, and the run does not wait for an answer."
      - "The user overrides by saying so, at any time after a report: a message that tells the skill to add a kept-out candidate ('add it anyway', 'add them anyway', 'add both', 'include the text reminders anyway', 'keep my deposit idea'). Which candidate: the one the message names, by its words or by the ID in its report line; 'it' when exactly one candidate is kept out; 'them', 'both' or 'all' for every candidate kept out. 'It' with several kept out and none named adds nothing: the reply says 'Several suggestions were kept out. Name the one to add, for example \"add the text reminders anyway\".' A message that asks why, or only acknowledges, adds nothing. Section 3.5 gives examples."
      - "An override writes this: the candidate becomes an idea in the user's words (the skill's wording for a candidate of its own) with the next free ID and disposition open, rated at step 4 like any other; its row is removed from its table, which becomes 'None.' when that was the last row; a previously decided idea gets the item-level link of BEH-27; and section 6's prose gains one sentence, 'IDEA-NN was added at the user's request although <document ID>#<item ID> covers it.' or 'IDEA-NN was added at the user's request although BRN-NNN#IDEA-NN rejected it.', in which 'the user's' is fixed text and never a name. Before the BRN is written this goes into the work as it stands. After the BRN is written, in the same session, the skill edits the BRN in place as SKILL.md's 'Decisions that belong to the user' describes for a later confirmation (mark step 6, edit, step 7 validate, step 8 report), without asking step 5's form again: the new idea is open. In a later session it is an extension of that BRN (BEH-11)."
      - "The framework's idea count (5 to 15, unless its Steps set their own: framework-catalog.md, BEH-17 and BEH-18) is counted among the ideas added; candidates kept out don't count. A framework that generates no idea of its own (shortlist-ranking) generates none in place of a candidate kept out: a candidate of the user's list that is covered or previously decided is kept out and listed like any other."
    changes: "BEH-05: an exception to 'record the user's ideas in their own words alongside generated ones' (edit B-P1)"
    lands_in: "SPEC-001 §6; SKILL.md step 3 (edit B-S4); references/brownfield.md, 'Already covered' and 'Previously decided'"
  - id: BEH-27
    status: proposed
    rule:
      - "A parked idea of an earlier BRN is never added to ideas by the skill alone. When the BRNs read hold at least one active idea whose disposition is parked and the skill can ask, it offers them once, at step 3, after the problems are framed and before it generates ideas: one AskUserQuestion form tagged devforgeai_step:3, one question with header 'Step 3', 'Take up parked ideas from earlier brainstorms?', options 'Take up none' and 'Take up all' in this order, each option's preview listing every parked idea as 'BRN-NNN#IDEA-NN: <idea text>', one per line. Names typed under Other take up those ideas only: a name is a qualified 'BRN-NNN#IDEA-NN', or a bare 'IDEA-NN' that matches exactly one parked idea listed. A bare ID that matches parked ideas of more than one BRN read is asked about once more, in a form tagged devforgeai_step:3 with header 'Step 3': 'Which IDEA-NN do you mean?' (with the ID), one option per matching idea labelled with its qualified form, multiSelect true. When that question can't be asked, is dismissed or is not answered, that idea is not taken up and stays a 'parked' row of Previously decided. A dismissal takes up none. Without AskUserQuestion the list and the question are plain text and the turn ends."
      - "Each idea taken up becomes a new idea of this BRN: the next free ID, its idea text copied word for word, addresses naming the problems of this BRN it bears on, value, effort, risk and score rated afresh at step 4, disposition open, and an item-level upstream record '{id: BRN-NNN, item: IDEA-NN, relation: informed_by, version: <that BRN's version>, hash: null}'."
      - "An idea taken up that bears on no problem of this BRN is not added: it stays previously decided and the reply says so. Ideas taken up don't count toward the framework's idea count."
      - "Every parked idea not taken up is a row of '### Previously decided' with the decision 'parked'. The rows of that table are ordered by Where. An idea that carries the item-level link is never also a row."
      - "When the skill can't ask (BEH-20's meaning), no parked idea is taken up."
    changes: "new"
    lands_in: "SPEC-001 §6; SKILL.md step 3 (edit B-S4); references/brownfield.md, 'Parked ideas' and 'Previously decided'"
  - id: BEH-28
    status: proposed
    rule:
      - "At step 3, after the problems, the reply shows each active assumption of the BRNs read whose state is open, as 'BRN-NNN#ASM-NN: <statement> (to validate: <validation>)'. Nothing is asked about them."
      - "At step 5, before the form, the skill proposes a change of state only from a stated fact with a source: for each assumption shown, a fact in this run's sources that reports the result the assumption's validation asks for gives 'open to validated' when it agrees with the statement and 'open to invalidated' when it contradicts it. No such fact, a fact about something else, or an opinion gives no row. Section 3.7 gives the test's examples."
      - "Each proposal is a row of '### Assumption updates', the last subsection of section 6 (C-11): 'BRN-NNN#ASM-NN', the change, the fact ending with one sources entry in parentheses, and the status 'proposed, not confirmed'. Rows are ordered by their first cell. With no row the line 'None.' replaces the table. An Evidence cell is never a marker."
      - "When the table has a row, step 5's form ends with C-10's question 4, header 'Step 5': 'Confirm these assumption updates?', options 'Accept all as proposed' and 'Leave them proposed', each option's preview holding the table with each assumption's statement; changes come typed under Other."
      - "Accept all as proposed writes 'confirmed on <today>' in every row, today as YYYY-MM-DD; a status cell names nobody. Leave them proposed, a dismissal, or no question asked leaves every row 'proposed, not confirmed'. Typed text confirms the rows it confirms, removes a row it rejects, and leaves the rest proposed."
      - "A confirmed change lives in this BRN's row and nowhere else: a new BRN never edits an earlier BRN."
      - "Step 7's read-back resets to 'proposed, not confirmed' any status cell the user did not confirm in step 5 of this run, unless the BRN being extended already held that row as confirmed."
    changes: "new; extends BEH-06's form by C-10's question 4 (edit B-P3) and BEH-09's read-back"
    lands_in: "SPEC-001 §6; SKILL.md 'Decisions that belong to the user', step 5 and step 7 (edits B-S1, B-S5, B-S6, B-S9); references/brownfield.md, 'Earlier assumptions' and 'Assumption updates'"
  - id: BEH-29
    status: proposed
    rule:
      - "When the user's words say the product exists (BEH-20's rule 2), a BRN is on the same topic for ERR-01 only when its title covers the same or a closely similar topic and its status is draft. A converged or archived BRN is not asked about: it is read as an earlier BRN (BEH-25) and the run writes a new BRN. When the user asks in words to extend a BRN by its ID, it is extended, whatever its status."
      - "When the user's words don't say the product exists, ERR-01's test is unchanged: any BRN on the same or a closely similar topic is asked about."
      - "A run that extends a BRN whose kind line says brownfield reads the documents again (BEH-25) and rebuilds Existing product from this reading; updates each upstream record's version; appends this run's new sources entries (a document read for the first time, or read at a new version) after the existing entries, in BEH-25's order among themselves, and never reorders or removes an existing entry; keeps the rows of Already covered, Previously decided and Assumption updates and adds new rows by BEH-26 to BEH-28."
      - "In such a run the BRN's own active assumptions whose state is open are candidates for an update too (BEH-28). Their row's first cell names this BRN. On confirmation the assumption's state is set to validated or invalidated in the same edit, under BEH-11's rules for extending, and the assumption risk ranking and the first release cut are then made again without it (mvp-and-prototype-path.md, BEH-32 item 3); while the row is 'proposed, not confirmed' the state stays open."
      - "When a run that extends a new-shape BRN turns its kind line to brownfield (intake-and-evidence.md, BEH-20: from 'greenfield', or from the NEEDS CLARIFICATION line of a BRN without the four headings), it reads the documents (BEH-25), adds '### Existing product' in section 1 after the context prose and '### Already covered', '### Previously decided' and '### Assumption updates' in section 6 after the first release cut, each filled by this run (BEH-25 to BEH-28) or holding its replacement line, adds the upstream records, and appends the sources entries. Nothing already in the BRN is removed, except section 7's bullet that says which kind an undecided run worked as (intake-and-evidence.md, IV-07). The result passes BV-01."
      - "Nothing of BEH-25 to BEH-29 applies to a BRN without the project-kind line, also when it is extended."
    changes: "ERR-01: narrows 'a BRN on the same or a closely similar topic' for a brownfield request (edit B-P2); extends BEH-11"
    lands_in: "SPEC-001 §6 and §7; SKILL.md step 1 item 2 (edit B-S2); references/brownfield.md, 'Extend or new' and 'Extending a brownfield BRN'"
```

### 3.2 What is read

| Order | Glob | Take | At most | Why this cap |
|---|---|---|---|---|
| 1 | `docs/specs/brainstorm/BRN-*.md` | the highest numbers, highest first; never the BRN being extended | 3 | The latest brainstorms hold the decisions still in force |
| 2 | `docs/specs/prd/PRD-*.md` | the highest numbers, highest first | 2 | The product in use, and one PRD before or after it |
| 3 | `docs/specs/epic/EPIC-*.md` | the highest numbers, highest first | 4 | The work most recently planned |
| 4 | `docs/specs/arch/ARCH-*.md` | the highest number | 1 | One description covers the system |

The folders are the ones the skills write to: `skills/prd/SKILL.md` ("`docs/specs/prd/PRD-NNN.md`"),
`skills/epic/SKILL.md` ("`docs/specs/epic/EPIC-NNN.md`") and `skills/architecture/SKILL.md`
("`docs/specs/arch/ARCH-NNN.md`"). ADRs are not read: an ADR records how something is built, has no item a
suggestion could be covered by, and a PRD run reads them later. Stories and specs are not read either (Bryan,
2026-11-19: "Skip automatic story and spec reads."): the run globs neither `docs/specs/story/` nor
`docs/specs/spec/`. A story or spec the user names as a source is read as a project file, by
intake-and-evidence.md's BEH-22: it gets a `document` entry in `sources`, and no Existing product row.

Worked example. A project holds BRN-001 to BRN-005, PRD-001 to PRD-003, no epic and ARCH-001. The run reads, in
this order: BRN-005, BRN-004, BRN-003, PRD-003, PRD-002, ARCH-001. BRN-001, BRN-002 and PRD-001 are not read.

### 3.3 Existing product (C-02)

The third cell, with any `|` in a title replaced by `/`:

| Document | Third cell | Example |
|---|---|---|
| BRN | `<title>: <n> ideas (<p> promoted, <k> parked, <r> rejected, <o> open)`, counting active ideas | `Reducing appointment no-shows at the dental clinic: 6 ideas (2 promoted, 2 parked, 2 rejected, 0 open)` |
| PRD | `<title> (<first FR ID> to <last FR ID>)`, over active functional requirements; with one, `(<its ID>)`; with none, `(no functional requirement)` | `Online booking for returning patients (FR-001 to FR-006)` |
| EPIC | `<title> (<first DW ID> to <last DW ID>)`, by the same rule; with none, `(no done-when item)` | `Self-service booking (DW-01 to DW-03)` |
| ARCH | `<title> (<first CMP ID> to <last CMP ID>)`, by the same rule; with none, `(no component)` | `Booking site architecture (CMP-01 to CMP-04)` |

After the table (or the line that replaces it) and one blank line comes one line per skipped document, in the
order met: `Skipped: <path from the project root> (<reason>)` (ERR-08).

### 3.4 Already covered: the test

Whether an item "already gives the same people the same result" can't be made mechanical (R9). The model reads
the item as written and applies these examples:

| Candidate | Item | Covered? |
|---|---|---|
| "Text reminders before a visit" | FR-003 "The system shall send a text reminder two days before each booked visit." | Yes: row `PRD-001#FR-003` |
| "Remind patients by text and by email" | the same FR-003 | No: the email half is not covered. The whole candidate becomes an idea |
| "Let new patients book online" | FR-001 "The system shall let a returning patient book a free slot online." | No: other people |

A document that discusses a suggestion in prose but has no item for it covers nothing: `Covered by` always
names an item, and the candidate becomes an idea.

### 3.5 Previously decided: the test

| Candidate | Earlier idea | Same idea? |
|---|---|---|
| "Take a deposit when a patient books" | BRN-001#IDEA-06 "Charge a deposit at booking." (rejected) | Yes: not added; a row with `rejected` |
| "Charge a fee for a missed visit" | the same IDEA-06 | No: charged after the visit, not at booking. It becomes an idea |

Only rejected ideas that came up again are listed, not every rejected idea of every BRN read: the table records
what this run kept out. Every parked idea is listed, because each was offered (or could not be) and none may be
lost between brainstorms.

**The report and the override: examples.** With the reminders and the deposit both kept out, the reply at the end
of step 3 holds:

```text
Not added, already covered by PRD-001#FR-003: "text reminders before a visit"
Not added, rejected in BRN-001#IDEA-06: "taking a deposit when a patient books"
Say "add it anyway" to add one.
```

Whether a later message is an override can't be made mechanical (R9). The test: the message tells the skill to
add a kept-out candidate.

| The user's next message | Result |
|---|---|
| "add the text reminders anyway" | The reminders become an idea in the user's words; their row is removed; section 6 gains "IDEA-07 was added at the user's request although PRD-001#FR-003 covers it." |
| "add both" | Both become ideas; the deposit's idea carries the link to BRN-001#IDEA-06 and section 6 gains "… although BRN-001#IDEA-06 rejected it." |
| "add it anyway" (two are kept out) | Nothing is added. The reply says: Several suggestions were kept out. Name the one to add, for example "add the text reminders anyway". |
| "add it anyway" (only the reminders are kept out) | The reminders become an idea |
| "why are the reminders covered?" | Nothing is added; the skill answers from FR-003's statement |
| "ok" | Nothing is added |

### 3.6 Parked ideas: worked example

BRN-001 (version 1) holds IDEA-04 "Let patients move their own appointment online." and IDEA-05 "Open a waitlist
for freed slots.", both parked. The form's previews list both. The user types "IDEA-04" under Other. The new
BRN gets:

```yaml
  - id: IDEA-03
    status: active
    idea: "Let patients move their own appointment online."
    addresses:
      - PRB-03
    value: null
    effort: null
    risk: null
    score: null
    disposition: open
    reason: null
    upstream:
      - {id: BRN-001, item: IDEA-04, relation: informed_by, version: 1, hash: null}
```

and *Previously decided* gets the row `| Open a waitlist for freed slots. | parked | BRN-001#IDEA-05 |`.
`validate_brn.py` accepts both link forms today: `upstream` is an allowed field of every item, and a
frontmatter record needs only `id` and `relation` (checked: the staged BRN-002 prints `OK`).

### 3.7 Assumption updates: the test, and where a change lives

Example. BRN-001#ASM-01: "We believe that patients read texts from the clinic within a day", validation "Send
reminder texts for one month and count how many are opened."

| Fact in this run's sources | Proposal |
|---|---|
| "8 of 10 reminder texts were opened within a day (data: reminder pilot export, October 2026)" | `open to validated`: it is the count the validation asks for, and it agrees |
| "2 of 10 reminder texts were opened within a day (data: reminder pilot export, October 2026)" | `open to invalidated`: the same count, and it contradicts |
| "Patients say they like the texts (note: Dana, conversation of 2026-11-18)" | No row: an opinion, not the count |

| Run | Where a confirmed change is written |
|---|---|
| A new BRN (BRN-002) about an assumption of BRN-001 | BRN-002's row `BRN-001#ASM-01 … confirmed on 2026-11-18`. BRN-001 is not touched: its ASM-01 still says `state: open` |
| A run that extends BRN-002, about BRN-002's own ASM-01 | BRN-002's row `BRN-002#ASM-01 … confirmed on …`, and in the same edit ASM-01's `state: validated` in BRN-002 |
| A run that extends an earlier-shape BRN | Nowhere: this document does not apply to it |

Whoever needs an assumption's current state reads the latest BRN's *Assumption updates* first, then the
assumption itself.

### 3.8 Validator checks

All five apply only to a new-shape BRN, after intake-and-evidence.md's checks, and use the kind its line gives:
`greenfield`, `brownfield`, not decided (the NEEDS CLARIFICATION line), or invalid (IV-01 failed; then BV-01
checks only the order). "The four headings" are `### Existing product` in section 1 and `### Already covered`,
`### Previously decided` and `### Assumption updates` in section 6. A heading's content is its non-blank lines
up to the next `### ` or `## ` heading. "A `sources` entry" is one that passed IV-02.

| Check | Rule | Reported at | Message |
|---|---|---|---|
| BV-01 | A greenfield BRN has none of the four headings | each such heading | `'<heading>' belongs to a brownfield BRN only: remove it, or correct the Project kind line (BV-01)` |
| BV-01 | A brownfield BRN has all four | the heading of the section (1 or 6) that lacks one | `a brownfield BRN needs '<heading>' in section <1 or 6> (BV-01)` |
| BV-01 | While the kind is not decided and section 7's bullet says the run worked as brownfield (IV-07), a BRN has all four | the heading of the section that lacks one | `this run worked as brownfield: '<heading>' is needed in section <1 or 6> (BV-01)` |
| BV-01 | While the kind is not decided and the bullet says the run worked as greenfield, a BRN has none of the four | each such heading | `this run worked as greenfield: remove '<heading>' (BV-01)` |
| BV-01 | While the kind is not decided and that bullet is missing or doubled (IV-07 reports it), a BRN has all four or none | the heading of the section that lacks one | `'<heading>' is missing: while the project kind is not decided, write all four brownfield headings or none of them (BV-01)` |
| BV-01 | In section 6 the headings present stand in the order First release cut, Already covered, Previously decided, Assumption updates | the first of the three brownfield headings present | `section 6's subsections must come in this order: First release cut, Already covered, Previously decided, Assumption updates (BV-01)` |
| BV-02 | Existing product has content | its heading | `'### Existing product' must hold its table or the line 'No document was found in the project.' (BV-02)` |
| BV-02 | Its content is the table (header `\| Document \| Version \| What it already covers \|`, the line `\|---\|---\|---\|`, at least one row) or, as the first line, `No document was found in the project.` | the first content line | `'### Existing product' must be the table '\| Document \| Version \| What it already covers \|' with at least one row, or its replacement line (BV-02)` |
| BV-02 | Each row has three non-empty cells | the row | `'### Existing product': each row has 3 non-empty cells (BV-02)` |
| BV-02 | A row's Document is `BRN-NNN`, `PRD-NNN`, `EPIC-NNN` or `ARCH-NNN` and its Version a positive integer | the row | `Existing product: Document must be a BRN, PRD, EPIC or ARCH ID and Version a positive integer (BV-02)` |
| BV-02 | No document is listed twice, and this BRN is not listed | the row | `Existing product: <ID> is listed twice, or is this BRN itself (BV-02)` |
| BV-02 | After the table or the replacement line, every line is `Skipped: <path> (<reason>)`, the reason one of ERR-08's four | the line | `under '### Existing product', after the table or its replacement line, only 'Skipped: path (reason)' lines are allowed, the reason being could not be read, no frontmatter, id does not match the file name, or no version (BV-02)` |
| BV-02 | Each listed document has a frontmatter `upstream` record with that `id`, no `item`, `relation: informed_by` and that `version` | the row | `<ID>: the frontmatter's upstream needs the record {id: <ID>, relation: informed_by, version: <version>, hash: null} (BV-02)` |
| BV-02 | Each listed document has the `sources` entry `document: docs/specs/<folder>/<ID>.md v<version>`, the folder being `brainstorm`, `prd`, `epic` or `arch` | the row | `<ID>: sources needs the entry "document: docs/specs/<folder>/<ID>.md v<version>" (BV-02)` |
| BV-03 | Already covered holds the line `None.` alone, or the table `\| Suggestion \| Covered by \|` with at least one row of two non-empty cells | its first content line (or its heading when empty; or the row) | `'### Already covered' must be the table '\| Suggestion \| Covered by \|' with at least one row, or its replacement line (BV-03)`; when empty `'### Already covered' must hold its table or the line 'None.' (BV-03)`; for a row `'### Already covered': each row has 2 non-empty cells (BV-03)` |
| BV-03 | `Covered by` is `PRD-NNN#FR-NNN`, `PRD-NNN#NFR-NNN`, `EPIC-NNN#DW-NN` or `ARCH-NNN#CMP-NN` | the row | `Already covered: Covered by must be PRD-NNN#FR-NNN, PRD-NNN#NFR-NNN, EPIC-NNN#DW-NN or ARCH-NNN#CMP-NN (BV-03)` |
| BV-03 | Its document is listed in Existing product | the row | `Already covered: <cell> cites a document that Existing product does not list (BV-03)` |
| BV-04 | Previously decided holds `None.` alone, or the table `\| Idea \| Decision \| Where \|` with at least one row of three non-empty cells | as BV-03 | The three messages of BV-03 with `'### Previously decided'`, its header, `3` and `(BV-04)` |
| BV-04 | `Decision` is `rejected` or `parked` and `Where` is `BRN-NNN#IDEA-NN` | the row | `Previously decided: Decision must be rejected or parked, and Where BRN-NNN#IDEA-NN (BV-04)` |
| BV-04 | `Where`'s BRN is listed in Existing product | the row | `Previously decided: <cell> cites a BRN that Existing product does not list (BV-04)` |
| BV-04 | No `Where` stands twice | the second row | `Previously decided: <cell> is listed twice (BV-04)` |
| BV-04 | No idea's item-level `upstream` record names a BRN and item that a `Where` cell names | the record's line | `IDEA-NN is linked to <BRN-NNN#IDEA-NN>, which Previously decided also lists: an idea taken up again is not listed there (BV-04)` |
| BV-05 | Assumption updates holds `None.` alone, or the table `\| Earlier assumption \| Change \| Evidence \| Status \|` with at least one row of four non-empty cells | as BV-03 | The three messages of BV-03 with `'### Assumption updates'`, its header, `4` and `(BV-05)` |
| BV-05 | The first cell is `BRN-NNN#ASM-NN` of a BRN listed in Existing product, or of this BRN, and stands once | the row | `Assumption updates: Earlier assumption must be BRN-NNN#ASM-NN of a BRN that Existing product lists, or of this BRN, each once (BV-05)` |
| BV-05 | `Change` is `open to validated` or `open to invalidated` | the row | `Assumption updates: Change must be 'open to validated' or 'open to invalidated' (BV-05)` |
| BV-05 | `Evidence` ends with a space and one `sources` entry in parentheses, with text before it; a marker is not accepted | the row | `Assumption updates: Evidence must be a fact that ends with one sources entry in parentheses (BV-05)` |
| BV-05 | `Status` is `proposed, not confirmed`, or `confirmed on <a real calendar date as YYYY-MM-DD>` and nothing else | the row | `Assumption updates: Status must be 'proposed, not confirmed' or 'confirmed on DATE', the date a real one written as four digits, two, two (BV-05)` |
| BV-05 | A row about this BRN's own assumption agrees with it: confirmed, and the assumption's `state` is the change's target; proposed, and the `state` is `open` | the row | `Assumption updates: ASM-NN of this BRN must have state <validated, invalidated or open> while its row says '<confirmed, or proposed, not confirmed>' (BV-05)` |

Edit B-V1's code is the reference for every detail the table leaves out. After a row fails BV-05's first rule,
its other cells are not checked. The validator can't know what the user confirmed: a `confirmed on` cell passes
it, and step 7's read-back (BEH-28) is what protects R3.

## 4. Errors and edge cases

```yaml items
errors:
  - id: ERR-08
    status: proposed
    condition: "A document selected for reading (BEH-25) can't be used: the Read tool returns no content; or it does not start with a '---' line or has no closing '---' line; or its frontmatter id differs from the file name without .md; or its frontmatter version is not a positive integer. The tests run in this order and stop at the first that fails"
    handling: "Skip the document: no Existing product row, no upstream record, no sources entry, nothing taken from it, and no other file read in its place. Never repair or edit it. Write the line 'Skipped: <path from the project root> (<reason>)' after the Existing product table and one blank line, the reason being 'could not be read', 'no frontmatter', 'id does not match the file name' or 'no version' by the test that failed"
    user_result: "The BRN and the final reply name each skipped document with its reason; the document is unchanged"
    changes: "new"
    lands_in: "SPEC-001 §7; references/brownfield.md, 'What to read' and 'Existing product (section 1)'"
  - id: ERR-09
    status: proposed
    condition: "The kind is brownfield, decided or worked with, and no document was read: the four globs match nothing, or every selected document was skipped"
    handling: "Write 'No document was found in the project.' in place of the Existing product table (then any Skipped lines), 'None.' under Already covered and Previously decided, and under Assumption updates 'None.' unless the run extends a BRN with rows of its own. Tell the user once: 'I found no DevForgeAI document in this project, so I work from what you tell me about the product.' Ask nothing more than the brownfield question set"
    user_result: "A valid brownfield BRN built from the user's words; the reply says no document was found"
    changes: "new"
    lands_in: "SPEC-001 §7; references/brownfield.md, 'Existing product (section 1)'"
```

Edge cases, each decided by the items above:

| Case | What happens | By |
|---|---|---|
| The request says the site is live, and a converged BRN-001 on the same topic exists | No extend-or-new question. BRN-001 is read; the run writes BRN-002 | BEH-29 |
| The same, and BRN-001 is a draft | Extend-or-new is asked. On *extend*, BRN-001 is extended: as a brownfield BRN when it has the kind line, in its earlier shape when it has none | BEH-29, the gate |
| The user suggests an idea a PRD requirement covers | Kept out. The reply says `Not added, already covered by PRD-001#FR-003: "text reminders before a visit"` and `Say "add it anyway" to add one.` Nothing is asked | BEH-26 |
| The user answers "add it anyway" | It becomes an idea in the user's words, its row is removed and section 6 says so | BEH-26 |
| Two candidates are kept out and the user writes "add it anyway" | Nothing is added; the reply says to name the one to add. "add both" adds both | BEH-26 |
| The user says "add it anyway" after the BRN was written, in the same session | The BRN is edited in place, validated again and reported; step 5's form is not asked again | BEH-26 |
| The user names `docs/specs/story/STORY-002.md` as a source | Read as a project file (intake-and-evidence.md, BEH-22): a `document` entry, no Existing product row, and nothing in it covers a candidate | BEH-25 |
| The skill's own candidate is covered | Listed under Already covered with the skill's wording; another idea is generated in its place while the framework's idea count asks for more | BEH-26 |
| A requirement with `priority: wont` matches the candidate | Not covered: the product does not do it. The candidate becomes an idea | BEH-26 |
| The same idea was rejected in BRN-001 and parked in BRN-003 | Both rows are listed when the rejected one came up again; the parked one is offered | BEH-26, BEH-27 |
| The waiver was answered *Proceed without questions* | Documents are read; no parked idea is taken up; every update stays proposed; kept-out candidates are still reported | BEH-27, BEH-28 |
| A source contradicts an assumption that an earlier BRN already marks `validated` | No row: only `open` assumptions are candidates | BEH-28 |
| The user rejects a proposed update in typed text | The row is removed | BEH-28 |
| A document's version changed between the first run and an extending run | Existing product and the `upstream` record show the new version; `sources` keeps the old entry and gains the new one | BEH-29 |
| An eleventh document exists | Not read, not listed, not mentioned | BEH-25 |
| The user types "IDEA-04" and both BRN-001 and BRN-003 hold a parked IDEA-04 | One more question, "Which IDEA-04 do you mean?", with `BRN-001#IDEA-04` and `BRN-003#IDEA-04`; unanswered, neither is taken up and both stay `parked` rows | BEH-27 |
| A `greenfield` BRN is extended and the user says the product is now live | The kind line becomes `brownfield`; the four headings are added, filled by this run; nothing is removed | BEH-29, intake-and-evidence.md BEH-20 |
| A run extends BRN-002 after PRD-001 moved to version 4 | `sources` keeps its entries in place and gains `"document: docs/specs/prd/PRD-001.md v4"` at the end | BEH-29 |
| The kind is not decided and the run worked as greenfield | None of the four headings is written; BV-01 accepts none | BEH-20, BV-01 |

## 5. Verification

The conventions of intake-and-evidence.md, section 5, apply: hand-written cases, the same `prompt.md`
frontmatter, graders without flags, and prompts that say to proceed without questions (R5). `file_exists` counts
only files the run created, so every seeded file is graded by a regex on its content, with an "unchanged"
grader. Each scaffold's earlier BRN is `converged` and each prompt says in words that the product exists, so no
run stops at extend-or-new.

```yaml items
verifications:
  - id: VER-30
    status: proposed
    covers:
      - BEH-25
      - BEH-27
      - BEH-29
      - ERR-08
    level: eval
    obligation: "With a converged BRN-001, PRD-001 version 3 and a PRD-002 without frontmatter seeded, a request that says the site is live writes BRN-002 with 'Project kind: brownfield', an Existing product table listing BRN-001 and PRD-001 in that order, a Skipped line for PRD-002, an informed_by record and a document sources entry for each document read, both parked ideas of BRN-001 under Previously decided, and leaves the three seeded files unchanged."
    case: brownfield-reads-documents
    prompt: |-
      Our dental clinic's online booking site has been live since March 2026 for returning patients.
      Brainstorm what we should improve next for patients who book online. Don't ask me any
      questions, just work through it and write it up.
    scaffold: "scaffold.sh writes docs/specs/brainstorm/BRN-001.md and docs/specs/prd/PRD-001.md, byte for byte staged/examples/brainstorm-brownfield/BRN-001.md and PRD-001.md, and docs/specs/prd/PRD-002.md holding exactly the three lines '# PRD-002', an empty line and 'Notes for a later release. fixture-prd2-91be'"
    graders:
      - name: skill-fired
        type: tool_used
        pattern: 'tool: Skill; input_match: "skill"\s*:\s*"(?:[\w-]+:)?brainstorm"'
      - name: brn-002-exists
        type: file_exists
        pattern: 'path: docs/specs/brainstorm/BRN-002.md; exists: true'
      - name: kind-brownfield
        type: regex
        target: docs/specs/brainstorm/BRN-002.md
        match: contains
        pattern: '\n## 1\. Context\n+Project kind: brownfield\n\n'
      - name: existing-product-table
        type: regex
        target: docs/specs/brainstorm/BRN-002.md
        match: contains
        pattern: '\n### Existing product\n+\| Document \| Version \| What it already covers \|\n\|---\|---\|---\|\n\| BRN-001 \| 1 \| [^|\n]+ \|\n\| PRD-001 \| 3 \| [^|\n]*\(FR-001 to FR-006\) \|\n'
      - name: skipped-named
        type: regex
        target: docs/specs/brainstorm/BRN-002.md
        match: contains
        pattern: '\nSkipped: docs/specs/prd/PRD-002\.md \(no frontmatter\)\n'
      - name: upstream-records
        type: regex
        target: docs/specs/brainstorm/BRN-002.md
        match: contains
        pattern: '\nupstream:\n[ \t]+- \{id: BRN-001, relation: informed_by, version: 1, hash: null\}\n[ \t]+- \{id: PRD-001, relation: informed_by, version: 3, hash: null\}\n'
      - name: sources-documents
        type: regex
        target: docs/specs/brainstorm/BRN-002.md
        match: contains
        pattern: '\nsources:[\s\S]*?"document: docs/specs/brainstorm/BRN-001\.md v1"[\s\S]*?"document: docs/specs/prd/PRD-001\.md v3"[\s\S]*?\n---\n'
      - name: parked-listed
        type: regex
        target: docs/specs/brainstorm/BRN-002.md
        match: contains
        pattern: '\n### Previously decided\n+\| Idea \| Decision \| Where \|\n\|---\|---\|---\|\n(?:\|[^\n]*\|\n)*\| [^|\n]+ \| parked \| BRN-001#IDEA-04 \|\n(?:\|[^\n]*\|\n)*\| [^|\n]+ \| parked \| BRN-001#IDEA-05 \|\n'
      - name: brn-001-unchanged
        type: regex
        target: docs/specs/brainstorm/BRN-001.md
        match: contains
        pattern: '\nversion: 1\n[\s\S]*\nupdated: 2026-03-02\n[\s\S]*\n    state: open\n[\s\S]*\| 1 \| 2026-03-02 \| claude-code \(session fixture-brn-7c1e\) \| Initial draft \|\s*$'
      - name: prd-001-unchanged
        type: regex
        target: docs/specs/prd/PRD-001.md
        match: contains
        pattern: '\nversion: 3\n[\s\S]*\nupdated: 2026-09-14\n[\s\S]*fixture-prd-4d2a[\s\S]*\| 3 \| 2026-09-14 \| Dana \| Approved \| status \|\s*$'
      - name: prd-002-unchanged
        type: regex
        target: docs/specs/prd/PRD-002.md
        match: contains
        pattern: '^# PRD-002\n\nNotes for a later release\. fixture-prd2-91be\n?$'
  - id: VER-31
    status: proposed
    covers:
      - BEH-26
      - BEH-28
    level: eval
    obligation: "With BRN-001 and PRD-001 seeded, a request that suggests text reminders (covered by PRD-001#FR-003) and a deposit at booking (rejected as BRN-001#IDEA-06), and gives the reminder pilot's result, writes BRN-002 with the reminders under Already covered, the deposit under Previously decided, neither among the ideas, and an Assumption updates row for BRN-001#ASM-01 that is proposed and not confirmed; the reply names each kept-out suggestion with its exact ID and asks nothing; BRN-001 is unchanged."
    case: brownfield-keeps-out-covered
    prompt: |-
      Our dental clinic's online booking site has been live since March 2026. Two things I'd like to
      see in it: text reminders before a visit, and taking a deposit when a patient books. Our
      reminder pilot export for October 2026 shows that 8 of 10 reminder texts were opened within a
      day. Brainstorm what we should improve next. Don't ask me any questions, just work through it
      and write it up.
    scaffold: "scaffold.sh writes docs/specs/brainstorm/BRN-001.md and docs/specs/prd/PRD-001.md, byte for byte staged/examples/brainstorm-brownfield/BRN-001.md and PRD-001.md, and nothing else"
    graders:
      - name: skill-fired
        type: tool_used
        pattern: 'tool: Skill; input_match: "skill"\s*:\s*"(?:[\w-]+:)?brainstorm"'
      - name: brn-002-exists
        type: file_exists
        pattern: 'path: docs/specs/brainstorm/BRN-002.md; exists: true'
      - name: reminders-already-covered
        type: regex
        target: docs/specs/brainstorm/BRN-002.md
        match: contains
        pattern: '\n### Already covered\n+\| Suggestion \| Covered by \|\n\|---\|---\|\n(?:\|[^\n]*\|\n)*\| [^|\n]*[Rr]eminder[^|\n]* \| PRD-001#FR-003 \|\n'
      - name: deposit-previously-decided
        type: regex
        target: docs/specs/brainstorm/BRN-002.md
        match: contains
        pattern: '\n### Previously decided\n+\| Idea \| Decision \| Where \|\n\|---\|---\|---\|\n(?:\|[^\n]*\|\n)*\| Charge a deposit at booking\. \| rejected \| BRN-001#IDEA-06 \|\n'
      - name: no-deposit-idea
        type: regex
        target: docs/specs/brainstorm/BRN-002.md
        match: not_contains
        pattern: '```yaml items[ \t]*\nideas:[ \t]*\n(?:(?!```)[\s\S])*[Dd]eposit'
      - name: kept-out-of-ideas
        type: llm
        focus: docs/specs/brainstorm/BRN-002.md
        pattern: "The file is a brainstorm document. Look only at the fenced block that starts with `ideas:`. PASS if no idea in it proposes sending patients a text reminder before a visit, and no idea in it proposes taking or charging a deposit at booking. An idea about another kind of reminder (email, phone call) or another kind of charge (a fee after a missed visit) does not cause a FAIL. FAIL otherwise, and quote the idea."
      - name: assumption-update-proposed
        type: regex
        target: docs/specs/brainstorm/BRN-002.md
        match: contains
        pattern: '\n### Assumption updates\n+\| Earlier assumption \| Change \| Evidence \| Status \|\n\|---\|---\|---\|---\|\n\| BRN-001#ASM-01 \| open to validated \| [^|\n]*8 of 10[^|\n]*\(data: [^|\n]*[Rr]eminder pilot export[^|\n]*October 2026\) \| proposed, not confirmed \|\n'
      - name: no-confirmed-update
        type: regex
        target: docs/specs/brainstorm/BRN-002.md
        match: not_contains
        pattern: '\| confirmed [^|\n]*\d{4}-\d{2}-\d{2} \|'
      - name: brn-001-unchanged
        type: regex
        target: docs/specs/brainstorm/BRN-001.md
        match: contains
        pattern: '\nversion: 1\n[\s\S]*\nupdated: 2026-03-02\n[\s\S]*\n    state: open\n[\s\S]*\| 1 \| 2026-03-02 \| claude-code \(session fixture-brn-7c1e\) \| Initial draft \|\s*$'
      - name: tells-what-was-kept-out
        type: llm
        pattern: "The user suggested two things: text reminders before a visit, and taking a deposit when a patient books. PASS if the final reply says that both were not added as ideas, names PRD-001#FR-003 for the reminders and BRN-001#IDEA-06 for the deposit, and tells the user they can say \"add it anyway\". FAIL if the reply is silent about either suggestion, gives no ID for one of them, presents either as a new idea, or asks the user a question about them."
      - name: reply-names-requirement-id
        type: regex
        target: last_message
        match: contains
        pattern: 'Not added, already covered by PRD-001#FR-003: "[^"\n]*[Rr]eminder[^"\n]*"'
      - name: reply-names-rejected-idea
        type: regex
        target: last_message
        match: contains
        pattern: 'Not added, rejected in BRN-001#IDEA-06: "[^"\n]*[Dd]eposit[^"\n]*"'
      - name: reply-offers-the-override
        type: regex
        target: last_message
        match: contains
        pattern: 'Say "add it anyway" to add one\.'
  - id: VER-32
    status: proposed
    covers:
      - BEH-20
      - ERR-09
    level: eval
    obligation: "A request that says the product is in use, in a project with no document, writes a brownfield BRN-001 whose Existing product holds 'No document was found in the project.', with 'None.' under the three section 6 headings and an empty upstream, and the reply says no document was found."
    case: brownfield-nothing-to-read
    prompt: |-
      Our internal expense-report approval tool has been in use for two years, and an approval still
      takes about nine working days. Brainstorm how we could make approvals faster. Skip any
      questions and write it up.
    scaffold: none
    graders:
      - name: skill-fired
        type: tool_used
        pattern: 'tool: Skill; input_match: "skill"\s*:\s*"(?:[\w-]+:)?brainstorm"'
      - name: brn-exists
        type: file_exists
        pattern: 'path: docs/specs/brainstorm/BRN-001.md; exists: true'
      - name: kind-brownfield
        type: regex
        target: docs/specs/brainstorm/BRN-001.md
        match: contains
        pattern: '\n## 1\. Context\n+Project kind: brownfield\n\n'
      - name: no-document-line
        type: regex
        target: docs/specs/brainstorm/BRN-001.md
        match: contains
        pattern: '\n### Existing product\n+No document was found in the project\.\n+## 2\. Problems\n'
      - name: three-none-lines
        type: regex
        target: docs/specs/brainstorm/BRN-001.md
        match: contains
        pattern: '\n### Already covered\n+None\.\n+### Previously decided\n+None\.\n+### Assumption updates\n+None\.\n+## 7\. '
      - name: upstream-empty
        type: regex
        target: docs/specs/brainstorm/BRN-001.md
        match: contains
        pattern: '\nupstream: \[\][ \t]*\n'
      - name: says-nothing-found
        type: llm
        pattern: "PASS if the final reply tells the user that no document (no earlier brainstorm, PRD or other DevForgeAI document) was found in the project, so the brainstorm rests on what the user said about the product. FAIL if the reply does not mention this, or claims to have read a document."
  - id: VER-33
    status: proposed
    covers:
      - BEH-25
      - BEH-26
      - BEH-27
      - BEH-28
      - BEH-29
      - ERR-08
      - ERR-09
    level: unit
    obligation: "src/tests/brainstorm/test_validate_brn.py, run as 'python3 -B src/tests/brainstorm/test_validate_brn.py': the 32 tests of edit B-T2 pass in each of its three classes. They show that the staged example BRN-002 passes, as does the same BRN with no document read; that each of BV-01 to BV-05 reports its message on its line; that a Skipped line, a proposed update, an undecided kind that worked as brownfield with all four headings and document sources entries that follow other entries pass; and that a row about this BRN's own assumption must agree with its state."
  - id: VER-34
    status: proposed
    covers:
      - BEH-26
      - BEH-27
      - BEH-28
      - BEH-29
    level: manual
    obligation: "Live, with AskUserQuestion, following docs/runbooks/brainstorm-manual-test.md with a copy of the plugin, in a project seeded with the example's BRN-001 and PRD-001: (a) 'Our booking site is live. Brainstorm what to improve next.': no extend-or-new question although BRN-001 exists; at step 3 one form headed 'Step 3' asks 'Take up parked ideas from earlier brainstorms?' with 'Take up none' and 'Take up all', both previews listing BRN-001#IDEA-04 and BRN-001#IDEA-05; typing 'IDEA-04' gives a new idea with that text and an item-level upstream record, and Previously decided lists only IDEA-05 as parked; (b) in the same run the reply shows BRN-001#ASM-01 and ASM-02 with their validations; (c) the user suggests text reminders: the reply holds the line 'Not added, already covered by PRD-001#FR-003: \"<the user's words>\"' and the sentence 'Say \"add it anyway\" to add one.', and no question about it is asked, in a form or in text; the user says 'add it anyway': it becomes an idea in the user's words, the row is gone and section 6 holds the sentence 'IDEA-NN was added at the user's request although PRD-001#FR-003 covers it.'; (d) the user gives the pilot result with its source: step 5's form ends with 'Confirm these assumption updates?', its previews showing the row; 'Accept all as proposed' writes 'confirmed on <today>' and BRN-001 is byte for byte unchanged; in a second run 'Leave them proposed' writes 'proposed, not confirmed'; (e) with BRN-001's status changed by hand to draft and the same request: extend-or-new is asked; (f) a run that extends the BRN-002 written in (d), with a fact for BRN-002's own ASM-01: on acceptance the row says confirmed and ASM-01's state is validated; on 'Leave them proposed' the state stays open; (g) with PRD-001's frontmatter removed by hand: the BRN names it in a Skipped line with 'no frontmatter' and PRD-001 is unchanged; (h) with a second earlier BRN that also holds a parked IDEA-04, typing 'IDEA-04' gets one more question, 'Which IDEA-04 do you mean?', with the two qualified forms as options, and dismissing it takes up neither, both staying parked rows; (i) extending a greenfield new-shape BRN after saying the product is live: the kind line becomes brownfield, the four headings are added and filled, nothing else is removed and the validator prints OK; (k) with the reminders and a deposit both kept out, 'add it anyway' adds neither and the reply says to name one, and 'add both' adds both, the deposit's idea carrying the item-level link to BRN-001#IDEA-06 and section 6 the sentence '... although BRN-001#IDEA-06 rejected it.'; (l) 'add it anyway' said after the BRN was written, in the same session: the BRN is edited in place and validated again, and step 5's form is not shown again; (m) the project holds docs/specs/story/STORY-001.md and docs/specs/spec/SPEC-001.md: the session shows no Read of either and Existing product lists neither; (j) extending the BRN-002 of (d) after PRD-001's version was raised by hand: the existing sources entries keep their order and the new document entry is the last. Recorded in SPEC-001 §9."
```

**What was checked while writing this document** (2026-11-18, in the worktree, with scratch copies only):

- Every edit of section 2 against the files as framework-catalog.md's and then intake-and-evidence.md's edits
  leave them: each old text occurs exactly once, ignoring line breaks; the ten SKILL.md edits add 20 lines
  (339 to 359), which leaves 41 lines under R2's limit of 400 for mvp-and-prototype-path.md.
- mvp-and-prototype-path.md's SKILL.md, output-rules.md and validator edits against the files as this
  document leaves them: its old texts for S2 to S13, O1, O2, W2, V1 and V2 each still occur once (its S1 is
  already done).
- The validator with both documents' edits applied to a scratch copy, and the test file with both documents'
  tests: 279 tests pass (93 in each of the three classes), 32 of them new here. With
  mvp-and-prototype-path.md's validator edits (its V1 and V2, as that document stood on 2026-11-18) added on
  top, they still pass, the staged BRN-002 included.
- `staged/examples/brainstorm-brownfield/BRN-001.md` and `BRN-002.md`: `OK` under the validator as it is today,
  with `python3` and `python3 -S`, and `OK` under the changed validator. Both, and `PRD-001.md`, validate
  against `src/schemas/brainstorm.schema.json` and `prd.schema.json` with the prd generator's `validate()`.
- `staged/examples/brainstorm-greenfield-mvp/BRN-001.md` (mvp-and-prototype-path.md) under the changed
  validator: `OK`.
- Every `regex` pattern above in node, against one good and one wrong sample.
- framework-catalog.md's `test_structure.py` (its section 5.1) on a scratch tree holding the three documents'
  edits and staged files: its 16 tests pass with `intake.md` and `brownfield.md` in place, and
  `progress/evaluate.py`'s `checklist_hash` of the edited SKILL.md equals the manifest's `checklistHash`.
- The test file with mvp-and-prototype-path.md's own tests added (its T1 and T2): 354 tests pass.
- Every `yaml items` block of this document with PyYAML, for R4's keys.

**Re-checked on 2026-11-20** against `main` at `ff78d44`, after pull request #173 (SKL-001 version 12), with the
reviewer's script, which applies every edit of the five documents in build order to scratch copies: each edit of
section 2 still applies; the ten SKILL.md edits take the file from 348 to 368 lines, which leaves 32 lines under
R2's limit of 400 (mvp-and-prototype-path.md and BEH-34 take 18); the validator's test file as this document
leaves it runs 279 tests, `OK`, with and without site-packages; `test_structure.py` runs 16 tests, `OK`.

**Re-checked again on 2026-11-20**, after Bryan's decisions of that day (section 7, decisions 23 and 24), the same
way: each edit of section 2 applies; SKILL.md still goes from 348 to 368 lines; the test file as this document
leaves it runs 279 tests, `OK`, with and without site-packages, 32 of them new here as before
(`test_status_without_a_name_and_date_is_rejected` is now `test_status_without_a_date_or_with_a_name_is_rejected`
and holds one sample of each); the staged BRN-002 prints `OK`, and with a status cell that names someone it gets
BV-05's message; `no-confirmed-update` in node passes the proposed row and fails a row confirmed in the new
form and one in the earlier form.

## 6. Staged files

| Staged file | Destination | What it is |
|---|---|---|
| [staged/skills/brainstorm/references/brownfield.md](staged/skills/brainstorm/references/brownfield.md) | `src/claude/DevForgeAI/skills/brainstorm/references/brownfield.md` (new) | The reference the skill reads at step 1 of a brownfield run: extend or new, what to read, C-02, C-06, parked ideas, earlier assumptions, C-11, extending, and what holds when nothing can be asked |
| [staged/examples/brainstorm-brownfield/README.md](staged/examples/brainstorm-brownfield/README.md) | `src/staging/examples/brainstorm-brownfield/README.md` (new) | What the three documents show |
| [staged/examples/brainstorm-brownfield/BRN-001.md](staged/examples/brainstorm-brownfield/BRN-001.md) | the same folder | The earlier brainstorm, in the earlier shape, converged: two ideas promoted, two parked, two rejected; two assumptions open |
| [staged/examples/brainstorm-brownfield/PRD-001.md](staged/examples/brainstorm-brownfield/PRD-001.md) | the same folder | A short PRD in the PRD skill's shape, version 3, approved, FR-001 to FR-006 |
| [staged/examples/brainstorm-brownfield/BRN-002.md](staged/examples/brainstorm-brownfield/BRN-002.md) | the same folder | A brownfield new-shape BRN holding every shape, with C-02, C-06 and C-11 filled and confirmed; also the unit tests' fixture |

BRN-001 and PRD-001 are also what the eval scaffolds of VER-26 (intake-and-evidence.md), VER-30 and VER-31
seed, byte for byte. BRN-002's *First release cut* and *Assumption risk ranking* rows were written by the rules
of the staged `references/mvp-path.md`: one open assumption, which stops IDEA-01 of the two cut rows.

## 7. Decisions and open questions

**Decisions made here**, each with its reason:

1. **Four kinds of document, ten at most, selected by file name.** The cap keeps the reading bounded in a
   project with many documents, and selection by name needs no reading to decide what to read. BRNs, PRDs,
   epics and the ARCH are the documents that say what the product does and what was decided about it.
2. **ADRs, stories, specs and code are not read.** None has an item that a product suggestion can be "covered
   by", and the PRD and architecture skills read ADRs at their own step.
3. **"Covered" needs an item.** C-06's `Covered by` is `<document ID>#<item ID>`. A suggestion that a document
   only discusses is not kept out, because there would be nothing exact to cite and the user could not check
   the claim.
4. **A requirement with `priority: wont` covers nothing.** The product does not do it, so the idea is new work.
5. **Only rejected ideas that came up again are listed; every parked idea is listed or taken up.** The first
   keeps the table to what this run kept out. The second makes sure a parked idea is seen at every later
   brainstorm until someone decides it.
6. **The override is a statement by the user, never a question by the skill.** A question for every kept-out
   candidate would make brownfield runs slow, and the waiver's text allows no new question. The reply always
   says what was kept out, so the user can act.
7. **Parked ideas are offered in one form with two options and the list in the previews**, the pattern BEH-06
   uses for dispositions. It works for any number of parked ideas, where one option per idea stops at four.
8. **An idea taken up is a new idea with an item-level `informed_by` link**, not a copy of the earlier item's
   ID. IDs never move between documents (output-rules.md), and the earlier BRN keeps its record.
9. **A new BRN never edits an earlier BRN.** PRD requirements cite the earlier BRN's items by version; an edit
   would need a version bump and a move of every link. The confirmed change is recorded in the new BRN's row.
10. **A run that extends a BRN edits that BRN's own assumption `state` in place**, with the row beside it, under
    BEH-11's extending rules. The validator checks that row and state agree (BV-05).
11. **An Evidence cell is never a marker.** A problem's `evidence` and a section 8 baseline may be a marker
    (README C-09). A proposal to change a state without a fact would be a guess, so no fact means no row, and
    BV-05 rejects a marker. README C-09 says so too.
12. **In a brownfield request only a draft BRN is "on the same topic".** Otherwise every later brainstorm about
    the same product would stop at extend-or-new. A converged BRN is a closed record that a PRD may cite;
    iterating on the product is a new BRN that reads it.
13. **A skipped document is not replaced by the next file.** The selection is then known from the file names
    alone, and the skipped file is named so the user can repair it.
14. **While the kind is not decided, the brownfield headings are all there or all absent.** The run worked
    with one kind (intake-and-evidence.md, BEH-20); a mix would show that it did not.
15. **Nothing here applies to an earlier-shape BRN, also when extended.** The gate says such a BRN keeps its
    earlier shape. Its assumptions' states change only as SPEC-001 allows today.

16. **An extension that turns the kind to brownfield adds the brownfield parts and removes nothing** (the
    lead's decision, 2026-11-19). The kind line moves only towards brownfield (intake-and-evidence.md,
    decision 15), so BV-01 holds on every extended BRN.
17. **A bare `IDEA-NN` that matches parked ideas of two BRNs is asked about once, then left parked** (the
    lead's decision, 2026-11-19). The offer always shows the qualified form, so the question is rare; a guess
    would take up an idea the user did not name.
18. **"Document entries first" holds for a BRN the run creates; an extension appends** (the lead's decision,
    2026-11-19). Existing `sources` entries are never reordered, because facts already cite them and a diff
    of the extension then shows only what it added. The validator checks no order of `sources`.

**Points settled with README.**

- A C-11 evidence cell is never a NEEDS CLARIFICATION marker: R3 wants a change proposed "only from a stated
  fact with a source" (decision 11). README C-09 says the same.
- README C-11 gives `Earlier assumption` as an assumption of an earlier BRN. A run that extends a brownfield BRN
  also updates that BRN's own assumptions, and their row names the BRN itself (BEH-29). The column name stays.
- README's gate says an earlier-shape BRN keeps its earlier shape when extended, and this document lets a
  run that extends a brownfield BRN edit that BRN's own assumption `state` in place. The second holds for a
  new-shape BRN only; for an earlier-shape BRN the gate wins (decision 15).

**Decided by Bryan on 2026-11-19** (pull request #172's open questions; his words are quoted).

19. **The reading caps stand.** "Keep the reading caps at 3 BRNs, 2 PRDs, 4 epics, and 1 ARCH." BEH-25 is
    unchanged.
20. **No story and no spec is read automatically.** "Skip automatic story and spec reads." BEH-25 and section
    3.2 now say it in those words. A file the user names is another matter: intake-and-evidence.md's BEH-22
    reads it as a source ("You may read a project file I name as a source."), and it is never an Existing
    product row.
21. **A covered suggestion is reported with the exact ID, and the user overrides without being asked.**
    "Report covered suggestions with the exact requirement ID and let me say "add it anyway" without
    prompting." BEH-26 fixes the report line (`Not added, already covered by PRD-001#FR-003: "…"`), the one
    sentence that names the override, the wordings that count as one, which candidate "it" means, and what is
    written. Decided here, because he left it open: an override removes the candidate's row and records the
    fact in section 6's prose, so the tables list only what is still kept out; "it" with several kept out
    adds nothing rather than guess; and an override after the BRN is written edits it in place.
22. **A confirmed update to an earlier assumption is recorded in the new BRN only.** "Record a confirmed
    update to an earlier assumption in the new BRN only." Decision 9 and BEH-28 are unchanged: the earlier
    BRN is never edited.

**Decided by Bryan on 2026-11-20** (session fa59a935-ed2e-4502-b6c4-93bb6d847546; his words are quoted).

23. **A status cell names no owner.** Asked about the skill's ask for the owner's name when a BRN's `owner` is
    a NEEDS CLARIFICATION marker: "the owner isn't necessary". Of the four readings then offered: "No owner in
    the line at all" (the option's text: "The line is always "confirmed on <date>", never naming anyone.").
    C-11's status cell is `proposed, not confirmed` or `confirmed on YYYY-MM-DD`: BEH-28, edits B-S1, B-S6,
    B-S9, B-O2, B-O3, B-V1, B-T1 and B-T2, section 3.7, BV-05, VER-31's `no-confirmed-update`, VER-34 (d), the
    staged `brownfield.md` and BRN-002 with its README. BEH-28 no longer asks for the owner's name, and section
    4's row for an `owner` that is a marker is removed. BV-05 checks the date as it did, a real calendar date,
    and now rejects a cell that names someone: nothing shipped with the earlier form, so no rule reads it. The
    frontmatter key `owner` is untouched (R1).
24. **The override sentence says "the user".** ""at the user's request" (Recommended)". Section 6's sentence is
    always `IDEA-NN was added at the user's request although …`, in both of its forms: BEH-26, section 3.5,
    VER-34 (c), the staged `brownfield.md`. It holds no name and no marker, so a BRN whose `owner` is a marker
    needs no rule of its own.

**Open, for Bryan.** None.
