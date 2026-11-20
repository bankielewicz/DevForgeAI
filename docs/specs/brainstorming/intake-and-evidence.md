# Intake and evidence

**Status:** proposal, written 2026-11-18 by claude-code on the model Fable 5.2 (session
fa59a935-ed2e-4502-b6c4-93bb6d847546) for Bryan's review. It changes nothing until SPEC-001's next version is
approved and built. Read [README.md](README.md) first: this document uses its rules (R1 to R10), its shapes (C-01
to C-11), its gate and its IDs without repeating them. It is the second of the four documents built as SKL-001
version 13 (README section 8).

## Workflow steps this changes

| Step (SKILL.md's line, unchanged) | Today | Added by this document |
|---|---|---|
| 1. Intake: topic, existing BRNs, clarifying questions | Topic; extend or new; up to three questions | The project kind decided (C-01); the question set for that kind, up to four questions in one form; sources gathered (C-09) |
| 3. Diverge: problems, ideas, assumptions | Problems, 5 to 15 ideas, assumptions | Each problem's `evidence` taken from a source and cited, or a marker |
| 6. Write the BRN | Template, frontmatter, Change Log | The project-kind line (C-01), Target users (C-03), success signals (C-08) and `sources` (C-09) written in their fixed shapes, from the one template |
| 7. Validate the BRN | `validate_brn.py`, then the read-back | Validator checks IV-01 to IV-07, for a new-shape BRN only |

## 1. Scope

**In.**

- The rule that decides the project kind, the kind question, and what is written when the kind is not decided.
- The two clarifying-question sets, their limit (four), when a question is skipped, and the waiver.
- Sources: what counts, the form of each entry, and how a fact cites one.
- Section 3 (Target users) and section 8 (Candidate success signals): which step gathers, which writes, and
  the rule for each cell.
- Validator checks IV-01 to IV-07 and their unit tests.
- The one BRN template for the whole build, and the reference `references/intake.md`.

**Out.**

- What a brownfield run reads and writes beyond the kind line: [brownfield-iteration.md](brownfield-iteration.md).
  The template stages its shapes (C-02, C-06, C-11); that document owns their rules.
- The first release cut (C-05) and the assumption risk ranking (C-07):
  [mvp-and-prototype-path.md](mvp-and-prototype-path.md). The template stages both in README's form. This
  document only reads C-05's table to know which ideas get a success signal.
- Framework selection: [framework-catalog.md](framework-catalog.md). This document supplies the kind that
  README section 5's rule 4 reads.
- Any new frontmatter key, collection or field (R1), and any change to the eight checklist lines (R2).

## 2. Changes by file

Each edit below is exact (R7): the old text occurs once in the file as it stands when this document is built,
ignoring line breaks, and the new text replaces it. [framework-catalog.md](framework-catalog.md) is built first
and moves SKILL.md's steps under a new heading; no edit here depends on a heading's position. Every old text
below was checked against version 11 of the files with that document's edits applied, and on 2026-11-20 against
version 12's (section 5, "What was checked"). One edit, A-W2, starts from text that document wrote.

An old or new text in a `python` block is whole lines with their indentation: the new lines replace the old
lines. In a `text` block the old text may start in the middle of a line; what stands before and after it on
its lines stays.

### 2.1 `docs/specs/spec/SPEC-001.md` (its next version)

BEH-01 is replaced. BEH-20 to BEH-24, ERR-07 and VER-25 to VER-29 are added (sections 3 to 5). Section 3's tree
gains `references/intake.md`. SPEC-001 version 19, drafted before the build, makes these changes, edit A-P1
among them; the build's second commit doesn't repeat it.

**Edit A-P1** — `docs/specs/spec/SPEC-001.md` (BEH-01's rule)

Old text:

```text
Ask at most three clarifying questions (trigger, affected users, constraints) before diverging, and skip any question the request already answers. When the request says to proceed without questions, ask none, once the waiver question (BEH-13) has been answered Proceed without questions or couldn't be asked, except the topic question when no topic is given (BEH-13, version 15).
```

New text:

```text
Decide the project kind (BEH-20). Ask at most four clarifying questions before diverging, in one form: the question set of the kind (BEH-21), skipping any question the request already answers. When the request says to proceed without questions, ask none, and never the kind question, once the waiver question (BEH-13) has been answered Proceed without questions or couldn't be asked, except the topic question when no topic is given (BEH-13, version 15).
```

### 2.2 `docs/specs/adr/ADR-003.md`

The clarifying-question limit is an interaction default in ADR-003's table of value classes (line 94).
ADR-003 version 3, drafted with SPEC-001 version 19 and accepted by Bryan with it, before the build, changes the
number there (edit A-D1), has a new `updated` date, and adds rows to its "Status history" table naming
SPEC-001's version and Bryan's acceptance. Nothing else in the ADR changes, and the build doesn't repeat the
edit. The
limit is fixed (Bryan, 2026-11-19: "Keep the four-question limit fixed."): in ADR-003's table the row still
classes it as an interaction default, its default value becomes 4, and no setting exposes it. Configuration
contract v1's only interaction key stays `interview.max_calls`; the brainstorm skill reads no policy document
and no local preference for this number, so every run's limit is four.

**Edit A-D1** — `docs/specs/adr/ADR-003.md` (A2, the Interaction default row)

Old text:

```text
clarifying-question limit (3)
```

New text:

```text
clarifying-question limit (4)
```

### 2.3 `src/claude/DevForgeAI/skills/brainstorm/SKILL.md`

Eight edits. They add 17 lines to the file (331 to 348, after framework-catalog.md's edits).

**Edit A-S1** — `src/claude/DevForgeAI/skills/brainstorm/SKILL.md` (Inputs)

Old text:

```text
- The template: `${CLAUDE_SKILL_DIR}/assets/brainstorm.md`.
```

New text:

```text
- The template: `${CLAUDE_SKILL_DIR}/assets/brainstorm.md`.
- Sources: what the user gives or names as evidence, and their own statements, recorded in
  `sources` ([intake.md](references/intake.md)).
```

**Edit A-S2** — `src/claude/DevForgeAI/skills/brainstorm/SKILL.md` (step 1, item 3)

Old text:

```text
3. **Clarifying questions.** Ask at most three, in one message: what triggered this, who is
   affected, and what constraints apply. Skip any the request already answers. Ask none when
   the request says to proceed without questions and the waiver was answered *Proceed without
   questions* or couldn't be asked. Record anything still unknown as
   `[NEEDS CLARIFICATION: question]` in the document; never fill a gap with a guess.
```

New text:

```text
3. **Project kind.** Decide whether the product the topic is about exists (*brownfield*) or not
   (*greenfield*) by the ordered rules in [intake.md](references/intake.md): the user's words
   decide, and a PRD in the project only makes brownfield the recommended answer of the kind
   question, asked alone in its own form. When it can't be asked or isn't answered, the kind stays
   undecided and intake.md says which kind to work with.
4. **Clarifying questions.** Ask at most four, in one form: the question set intake.md gives for
   the kind, in its order and wording. Skip any the request already answers. Ask none when
   the request says to proceed without questions and the waiver was answered *Proceed without
   questions* or couldn't be asked. Record anything still unknown as
   `[NEEDS CLARIFICATION: question]` in the document; never fill a gap with a guess.
5. **Sources.** Record each input the user gives or names as a `sources` entry in intake.md's
   form. Never invent a source and never fetch one.
```

**Edit A-S3** — `src/claude/DevForgeAI/skills/brainstorm/SKILL.md` (step 3, problems)

Old text:

```text
- Frame **problems** first (`PRB-NN`), stated from the affected user's side.
```

New text:

```text
- Frame **problems** first (`PRB-NN`), stated from the affected user's side. Take each `evidence`
  from a source and cite it, or write the marker ([intake.md](references/intake.md#citing-a-source)).
```

**Edit A-S4** — `src/claude/DevForgeAI/skills/brainstorm/SKILL.md` (step 6, item 2)

Old text:

```text
Replace the example items with the real ones. Delete every HTML comment.
```

New text:

```text
Replace the example items with the real ones. Delete every HTML comment. Write the project-kind
   line, section 3's table and section 8's bullets as [intake.md](references/intake.md) says, and
   keep or delete the template's brownfield-only parts as its first comment says.
```

**Edit A-S5** — `src/claude/DevForgeAI/skills/brainstorm/SKILL.md` (step 6, item 3)

Old text:

```text
- `upstream`, `participants` and `sources`: fill from the conversation, or leave them empty.
```

New text:

```text
- `upstream` and `participants`: fill from the conversation, or leave them empty.
   - `sources`: the entries recorded since step 1, in intake.md's form; `[]` when there is none.
```

**Edit A-S6** — `src/claude/DevForgeAI/skills/brainstorm/SKILL.md` (Extending an existing BRN)

Old text:

```text
Never edit earlier Change Log rows: they keep the
sessions that wrote earlier versions.
```

New text:

```text
Never edit earlier Change Log rows: they keep the
sessions that wrote earlier versions. A BRN without the `Project kind:` line keeps its earlier shape
when extended: add none of intake.md's shapes to it.
```

**Edit A-S7** — `src/claude/DevForgeAI/skills/brainstorm/SKILL.md` (Examples, first example)

Old text:

```text
The skill asks up to three questions (trigger, who is affected, constraints)
```

New text:

```text
The skill asks whether the product exists, then up to four questions (trigger, who is affected,
   constraints, evidence),
```

**Edit A-S8** — `src/claude/DevForgeAI/skills/brainstorm/SKILL.md` (References)

Old text:

```text
- `scripts/validate_brn.py`: run at step 7; it applies the output rules mechanically.
```

New text:

```text
- [references/intake.md](references/intake.md): read at step 1, before deciding the project kind:
  the kind rules, the question sets, the form of `sources`, and sections 3 and 8.
- `scripts/validate_brn.py`: run at step 7; it applies the output rules mechanically.
```

Not edited: item 3 of the task-list rules, which stand under `## Working through the steps` after
framework-catalog.md's edits ("the waiver, topic, clarifying and extend-or-new questions belong to step 1"). The
kind question is covered by its last clause, "any other question … belongs to the step whose work
asks it", and its form is tagged step 1 (BEH-20).

### 2.4 `src/claude/DevForgeAI/skills/brainstorm/references/output-rules.md`

**Edit A-O1** — `src/claude/DevForgeAI/skills/brainstorm/references/output-rules.md` (Contents)

Old text:

```text
- Collections and fields
- Unknowns
```

New text:

```text
- Collections and fields
- Project kind, sources and sections 3 and 8
- Unknowns
```

**Edit A-O2** — `src/claude/DevForgeAI/skills/brainstorm/references/output-rules.md` (Frontmatter, `sources`)

Old text:

```text
| `sources` | List of quoted raw inputs (notes, tickets, URLs), or `[]` |
```

New text:

```text
| `sources` | `[]`, or one quoted `"<kind>: <reference>"` string per input used (*Project kind, sources and sections 3 and 8*) |
```

**Edit A-O3** — `src/claude/DevForgeAI/skills/brainstorm/references/output-rules.md` (problems, `who`)

Old text:

```text
| `who` | Quoted persona |
```

New text:

```text
| `who` | Quoted persona, with no vertical bar in it, spelled the same way in every problem |
```

**Edit A-O4** — `src/claude/DevForgeAI/skills/brainstorm/references/output-rules.md` (problems, `evidence`)

Old text:

```text
| `evidence` | Quoted source or data, or `"[NEEDS CLARIFICATION: …]"` |
```

New text:

```text
| `evidence` | Quoted fact that ends with one `sources` entry in parentheses, or `"[NEEDS CLARIFICATION: …]"`. In a BRN without the project-kind line: quoted source or data |
```

**Edit A-O5** — `src/claude/DevForgeAI/skills/brainstorm/references/output-rules.md` (a new section before Unknowns)

Old text:

```text
## Unknowns

Never guess.
```

New text:

```text
## Project kind, sources and sections 3 and 8

These rules hold for a BRN that has the project-kind line (a *new-shape* BRN): a line after the
frontmatter and outside every fenced block that starts with `Project kind:`. A BRN without it keeps
its earlier shape, also when extended, and is checked by the other rules only.
[intake.md](intake.md) says how to fill each part.

| Part | Form |
|---|---|
| Project kind | The first line under `## 1. Context`, followed by a blank line: `Project kind: greenfield`, `Project kind: brownfield` or `Project kind: [NEEDS CLARIFICATION: greenfield or brownfield]`. With the third, and only then, section 7 holds one bullet `- [NEEDS CLARIFICATION: greenfield or brownfield; this run worked as greenfield]`, or the same with `worked as brownfield` |
| `sources` | Each entry `"<kind>: <reference>"`, the kind one of `document`, `data`, `ticket`, `interview`, `url`, `note`; no vertical bar; no entry twice |
| A cited fact: an active problem's `evidence`, a section 8 baseline | One `[NEEDS CLARIFICATION: …]` marker and nothing else, or text that ends with one `sources` entry, without its quotes, in parentheses after a space |
| Section 3 | Only the table `\| Persona \| Job to be done \| Current workaround \| Pain \|`: one row per distinct `who` value of the active problems, in the order the values first appear, the Persona cell equal to the `who` value; four non-empty cells in each row |
| Section 8 | One bullet `- IDEA-NN: <outcome>; baseline <cited fact>` for each active idea whose row in section 6's *First release cut* table says `yes`, in ID order; with none, the single line `- None.` |

## Unknowns

Never guess.
```

**Edit A-O6** — `src/claude/DevForgeAI/skills/brainstorm/references/output-rules.md` (Validation checklist, item 12)

Old text:

```text
11. The last Change Log row's author is `claude-code (session <ID>)` with the ID in
    `generated_by.session`, unless a person wrote that row.
```

New text:

```text
11. The last Change Log row's author is `claude-code (session <ID>)` with the ID in
    `generated_by.session`, unless a person wrote that row.
12. In a BRN with the project-kind line: that line is exact, first under `## 1. Context` and
    followed by a blank line; while it is the NEEDS CLARIFICATION line, and only then, section 7
    holds the one bullet that says which kind the run worked as; every `sources` entry has the form `"<kind>: <reference>"` and stands
    once; every active problem's `evidence` and every section 8 baseline is one marker or ends with
    a `sources` entry in parentheses; section 3 is the Target users table with one row per `who`
    value; section 8 has one bullet per first-release idea, or the line `- None.`
```

### 2.5 `src/claude/DevForgeAI/skills/brainstorm/references/work-file.md`

The work file is built from the template, so it already carries the kind line, `sources` and section 3. These
two edits say when each is written and that a continued run keeps them.

**Edit A-W1** — `src/claude/DevForgeAI/skills/brainstorm/references/work-file.md` (Its shape)

Old text:

```text
- No HTML comments.
```

New text:

```text
- The project-kind line, the frontmatter `sources` and section 3's table from the first save, and
  section 8's bullets at the step-5 save, each as [intake.md](intake.md) gives it. While the kind
  is not decided, section 7 holds the bullet that names the kind the run works as, from the first save.
- No HTML comments.
```

**Edit A-W2** — `src/claude/DevForgeAI/skills/brainstorm/references/work-file.md` (Continuing a run, item 1; the old text is framework-catalog.md's edit W3)

Old text:

```text
select at step 2 as usual).
```

New text:

```text
select at step 2 as usual). Keep its project-kind line, its `sources` and its section 3 too, and
   don't ask the kind question or the clarifying questions again.
```

### 2.6 The template

`src/claude/DevForgeAI/skills/brainstorm/assets/brainstorm.md` is replaced by
[staged/skills/brainstorm/assets/brainstorm.md](staged/skills/brainstorm/assets/brainstorm.md), and
`src/templates/brainstorm.md` by the same bytes. It is the one template of the whole build (README section 8):
it holds every shape C-01 to C-11 in its final form. Section 6 of this document describes it.

### 2.7 `src/claude/DevForgeAI/skills/brainstorm/references/intake.md` (new)

Copied from [staged/skills/brainstorm/references/intake.md](staged/skills/brainstorm/references/intake.md).

### 2.8 `src/claude/DevForgeAI/skills/brainstorm/scripts/validate_brn.py`

Two edits add the checks of section 3.6. They use only the standard library and compare strings, so the verdict
is the same with and without PyYAML. They run only when the BRN has a project-kind line, and they never raise
on an unfilled template. `section_body`, `subsection`, `cells`, `ends_with_source` and `unquote` are also used by
the checks that brownfield-iteration.md adds (BV), and `check_intake` returns the valid `sources` entries for
them. mvp-and-prototype-path.md's checks (MV) apply the gate themselves and use none of these.

**Edit A-V1** — `src/claude/DevForgeAI/skills/brainstorm/scripts/validate_brn.py` (new functions before `check`)

Old text:

```python
def check(path):
```

New text:

```python
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


def check(path):
```

**Edit A-V2** — `src/claude/DevForgeAI/skills/brainstorm/scripts/validate_brn.py` (the call, at the end of `check`)

Old text:

```python
    # --- optional YAML syntax check ----------------------------------------------------
```

New text:

```python
    # --- new-shape checks (a BRN with the project-kind line) ----------------------------
    kind = new_shape_kind(lines, fm_end)
    if kind is not None:
        sources = check_intake(lines, fm_end, (list_of("sources") or []) if "sources" in fm else [],
                               items, err)

    # --- optional YAML syntax check ----------------------------------------------------
```

### 2.9 `src/tests/brainstorm/test_validate_brn.py`

Written before the validator changes (README section 8). `VALID` stays an earlier-shape BRN, so every existing
test also proves that an earlier-shape BRN is checked as today. The new fixture `NEW` already holds C-05's and
C-07's tables, in mvp-and-prototype-path.md's grammar, so that these tests still pass when that document's
checks arrive. Three edits.

**Edit A-T1** — `src/tests/brainstorm/test_validate_brn.py` (the unfilled template)

Old text:

```python
                            r"^line 108: last Change Log row has no author")
```

New text:

```python
                            r"^line 191: last Change Log row has no author",
                            r"^line 41: the Project kind line must be exactly .* \(IV-01\)$")
```

**Edit A-T2** — `src/tests/brainstorm/test_validate_brn.py` (a new-shape fixture, after `edit`)

Old text:

```python
    return text.replace(old, new, 1)
```

New text:

```python
    return text.replace(old, new, 1)


# A new-shape BRN (it has the project-kind line), built from VALID: intake checks IV-01 to IV-07.
USERS = (
    "| Persona | Job to be done | Current workaround | Pain |\n|---|---|---|---|\n"
    "| Returning patient | Keep a check-up booked weeks ahead | A paper card on the fridge | Forgets the date |\n"
    "| Working patient | Move a visit after work | [NEEDS CLARIFICATION: current workaround of Working patient] "
    "| Cannot call during office hours |")
CUT = ("\n\n### First release cut\n\nFirst release cut: proposed, not confirmed\n\n"
       "| Idea | In first release | Why |\n|---|---|---|\n| IDEA-01 | yes | Tests ASM-01, ranked 1. |")
RANKING = ("\n\n### Assumption risk ranking\n\n| Rank | Assumption | If wrong | Confidence | Cheapest test |\n"
           "|---|---|---|---|---|\n| 1 | ASM-01 | Fatal: stops IDEA-01 (1 of 1 in the cut table). | low "
           "| Data: Check delivery and read receipts for one month. |")
SIGNAL = ("- IDEA-01: fewer missed visits; baseline one in eight visits missed (data: front-desk no-show log, "
          "August 2026)")
NEW = edit(VALID, "## 1. Context\n\n", "## 1. Context\n\nProject kind: greenfield\n\n")
NEW = edit(NEW, "sources: []", 'sources: ["data: front-desk no-show log, August 2026", '
           '"note: Dana, conversation of 2026-09-01"]')
NEW = edit(NEW, 'evidence: "Front-desk notes"',
           'evidence: "Callers ask to move visits after hours (note: Dana, conversation of 2026-09-01)"')
NEW = edit(NEW, "| Persona | Pain |\n|---|---|\n| Returning patient | Forgets the date |", USERS)
NEW = edit(NEW, "Dana confirmed IDEA-01 as promoted.", "Dana confirmed IDEA-01 as promoted." + CUT)
NEW = edit(NEW, "    state: open\n```", "    state: open\n```" + RANKING)
NEW = edit(NEW, "- Fewer no-shows per month.", SIGNAL)
# The same BRN with no idea promoted: no first-release idea, so section 8 holds "- None."
NEW_NONE = edit(NEW, 'disposition: promoted\n    reason: "Cheap to try and addresses both problems."',
                "disposition: open\n    reason: null")
NEW_NONE = edit(NEW_NONE, "| Idea | In first release | Why |\n|---|---|---|\n| IDEA-01 | yes | Tests ASM-01, "
                "ranked 1. |", "No idea is promoted or proposed for promotion.")
NEW_NONE = edit(NEW_NONE, "Fatal: stops IDEA-01 (1 of 1 in the cut table).",
                "Minor: stops no idea in the cut table (0 of 0).")
NEW_NONE = edit(NEW_NONE, SIGNAL, "- None.")
# The same BRN with the kind not decided: section 7 says which kind the run worked as.
QUESTION = "- [NEEDS CLARIFICATION: Which booking system does the clinic use?]"
WORKED_AS = "- [NEEDS CLARIFICATION: greenfield or brownfield; this run worked as %s]"
NEW_UNDECIDED = edit(NEW, "Project kind: greenfield", "Project kind: [NEEDS CLARIFICATION: greenfield or brownfield]")
NEW_UNDECIDED = edit(NEW_UNDECIDED, QUESTION, WORKED_AS % "greenfield" + "\n" + QUESTION)
```

**Edit A-T3** — `src/tests/brainstorm/test_validate_brn.py` (the new tests, at the end of `Base`)

Old text:

```python
        self.assert_rejects(edit(VALID, "upstream: []", "upstream: [BRN-002]"),
                            r"upstream must be \[\] or a list of link records")
```

New text:

```python
        self.assert_rejects(edit(VALID, "upstream: []", "upstream: [BRN-002]"),
                            r"upstream must be \[\] or a list of link records")

    # --- New-shape BRNs: intake checks IV-01 to IV-07 (intake-and-evidence.md) -------------------

    def test_new_shape_brn_passes(self):
        self.assert_valid(NEW)

    def test_undecided_project_kind_passes(self):
        self.assert_valid(NEW_UNDECIDED)

    def test_undecided_project_kind_without_its_bullet_is_rejected(self):
        errors = self.assert_rejects(edit(NEW_UNDECIDED, WORKED_AS % "greenfield" + "\n", ""),
                                     r"^line 116: while the project kind is not decided, section 7 must hold "
                                     r"exactly one bullet .* \(IV-07\)$")
        self.assertEqual(len(errors), 1, errors)

    def test_undecided_project_kind_with_two_bullets_is_rejected(self):
        text = edit(NEW_UNDECIDED, QUESTION, WORKED_AS % "brownfield" + "\n" + QUESTION)
        self.assert_rejects(text, r"^line 116: while the project kind is not decided, .* \(IV-07\)$")

    def test_decided_project_kind_with_the_bullet_is_rejected(self):
        text = edit(NEW, QUESTION, WORKED_AS % "greenfield" + "\n" + QUESTION)
        errors = self.assert_rejects(text, r"^line 133: the project kind is decided: remove the bullet .* "
                                     r"\(IV-07\)$")
        self.assertEqual(len(errors), 1, errors)

    def test_project_kind_inside_a_fenced_block_is_not_the_gate(self):
        self.assert_valid(edit(VALID, "Dana confirmed IDEA-01 as promoted.",
                               "Dana confirmed IDEA-01 as promoted.\n\n```text\nProject kind: greenfield\n```"))

    def test_wrong_project_kind_value_is_rejected(self):
        self.assert_rejects(edit(NEW, "Project kind: greenfield", "project  kind: Brownfield"),
                            r"^line 31: the Project kind line must be exactly .* \(IV-01\)$")

    def test_project_kind_after_the_prose_is_rejected(self):
        text = edit(NEW, "Project kind: greenfield\n\nOne in eight booked appointments ends in a no-show.",
                    "One in eight booked appointments ends in a no-show.\n\nProject kind: greenfield")
        self.assert_rejects(text, r"^line 33: the Project kind line must be the first line under .* \(IV-01\)$")

    def test_project_kind_without_a_blank_line_after_is_rejected(self):
        self.assert_rejects(edit(NEW, "Project kind: greenfield\n\n", "Project kind: greenfield\n"),
                            r"^line 31: the Project kind line must be the first line under .* \(IV-01\)$")

    def test_second_project_kind_line_is_rejected(self):
        text = edit(NEW, "Dana confirmed IDEA-01 as promoted.",
                    "Dana confirmed IDEA-01 as promoted.\n\nProject kind: brownfield")
        errors = self.assert_rejects(text, r"^line 108: only one Project kind line is allowed \(IV-01\)$")
        self.assertEqual(len(errors), 1, errors)

    def test_sources_entry_without_a_known_kind_is_rejected(self):
        text = edit(NEW, '"data: front-desk no-show log, August 2026"', '"Front-desk no-show log"')
        self.assert_rejects(text, r'^line 24: sources entry "Front-desk no-show log" must be .* \(IV-02\)$')

    def test_sources_entry_with_a_vertical_bar_is_rejected(self):
        text = edit(NEW, '"data: front-desk no-show log, August 2026"', '"data: log | August"')
        self.assert_rejects(text, r"^line 24: sources entry .* \(IV-02\)$")

    def test_duplicate_sources_entry_is_rejected(self):
        text = edit(NEW, '"data: front-desk no-show log, August 2026"',
                    '"note: Dana, conversation of 2026-09-01"')
        self.assert_rejects(text, r"^line 24: duplicate sources entry .* \(IV-02\)$")

    def test_evidence_without_a_source_is_rejected(self):
        text = edit(NEW, " (note: Dana, conversation of 2026-09-01)", "")
        errors = self.assert_rejects(text, r"^line 49: PRB-02: evidence must be one .* \(IV-03\)$")
        self.assertEqual(len(errors), 1, errors)

    def test_evidence_citing_an_unlisted_source_is_rejected(self):
        text = edit(NEW, "(note: Dana, conversation of 2026-09-01)", "(data: call log, 2026)")
        self.assert_rejects(text, r"^line 49: PRB-02: evidence must be one .* \(IV-03\)$")

    def test_marker_with_text_around_it_is_not_cited_evidence(self):
        text = edit(NEW, '"[NEEDS CLARIFICATION: current no-show rate]"',
                    '"High, we think [NEEDS CLARIFICATION: current no-show rate]"')
        self.assert_rejects(text, r"^line 43: PRB-01: evidence must be one .* \(IV-03\)$")

    def test_deprecated_problem_needs_no_cited_evidence(self):
        text = edit(NEW, " (note: Dana, conversation of 2026-09-01)", "")
        text = edit(text, '  - id: PRB-02\n    status: active', '  - id: PRB-02\n    status: deprecated')
        self.assert_valid(edit(text, "\n| Working patient | Move a visit after work | [NEEDS CLARIFICATION: current "
                               "workaround of Working patient] | Cannot call during office hours |", ""))

    def test_section_3_as_prose_is_rejected(self):
        self.assert_rejects(edit(NEW, USERS, "Returning patients and working patients."),
                            r"^line 55: section 3 must start with the table header .* \(IV-04\)$")

    def test_persona_that_is_not_a_who_value_is_rejected(self):
        self.assert_rejects(edit(NEW, "| Working patient | Move", "| Working patients | Move"),
                            r"^line 55: section 3's Persona cells must be .*: expected Returning patient; "
                            r"Working patient, got Returning patient; Working patients \(IV-04\)$")

    def test_missing_persona_row_is_rejected(self):
        text = edit(NEW, "\n| Working patient | Move a visit after work | [NEEDS CLARIFICATION: current workaround "
                    "of Working patient] | Cannot call during office hours |", "")
        self.assert_rejects(text, r"^line 55: section 3's Persona cells must be .* \(IV-04\)$")

    def test_target_users_row_with_an_empty_cell_is_rejected(self):
        self.assert_rejects(edit(NEW, "| A paper card on the fridge |", "| |"),
                            r"^line 57: section 3 holds only the Target users table: .* \(IV-04\)$")

    def test_new_shape_brn_with_no_first_release_idea_passes(self):
        self.assert_valid(NEW_NONE)

    def test_free_text_success_signal_is_rejected(self):
        self.assert_rejects(edit(NEW, SIGNAL, "- Fewer no-shows per month."),
                            r"^line 137: section 8 holds one bullet per first-release idea, .* \(IV-05\)$")

    def test_success_signal_for_an_idea_outside_the_first_release_is_rejected(self):
        text = edit(NEW, "| IDEA-01 | yes | Tests ASM-01, ranked 1. |", "| IDEA-01 | no | Left out by the user. |")
        self.assert_rejects(text, r"^line 135: section 8 must hold one bullet for each idea whose First release "
                            r"cut row says yes \(none\) and no other; .* \(IV-06\)$")

    def test_none_with_a_first_release_idea_is_rejected(self):
        self.assert_rejects(edit(NEW, SIGNAL, "- None."),
                            r"^line 135: section 8 must hold one bullet .* says yes \(IDEA-01\) and no other; .* "
                            r"\(IV-06\)$")

    def test_baseline_without_a_source_is_rejected(self):
        text = edit(NEW, SIGNAL, "- IDEA-01: fewer missed visits; baseline one in eight")
        self.assert_rejects(text, r"^line 137: IDEA-01: baseline must be one .* \(IV-05\)$")

    def test_success_signal_for_an_unknown_idea_is_rejected(self):
        text = edit(NEW, SIGNAL, SIGNAL + "\n- IDEA-09: more bookings; baseline [NEEDS CLARIFICATION: bookings "
                    "a week]")
        self.assert_rejects(text, r"^line 138: section 8: IDEA-09 is not an active idea \(IV-05\)$")

    def test_success_signals_out_of_order_are_rejected(self):
        text = edit(NEW, "| IDEA-01 | yes | Tests ASM-01, ranked 1. |",
                    "| IDEA-01 | yes | Tests ASM-01, ranked 1. |\n| IDEA-03 | yes | Included by the user. |")
        text = edit(text, SIGNAL, "- IDEA-03: more visits moved online; baseline [NEEDS CLARIFICATION: visits "
                    "moved by phone a week]\n" + SIGNAL)
        self.assert_rejects(text, r"^line 139: section 8's bullets must be in ID order, each idea once \(IV-05\)$")

    def test_earlier_shape_brn_is_not_held_to_the_new_checks(self):
        # VALID has no project-kind line: prose in section 3, a free bullet in section 8, uncited evidence.
        code, lines = self.run_text(VALID)
        self.assertEqual((code, len(lines)), (0, 1), lines)
```

The 29 new tests run in each of the file's three classes (with PyYAML, without the user site, and with
`python3 -S`), which is the proof that the verdict does not depend on PyYAML.

### 2.10 `docs/runbooks/brainstorm-manual-test.md`

**Edit A-R1** — `docs/runbooks/brainstorm-manual-test.md` (the first path's expectations)

Old text:

```text
and it asks at most 3 clarifying questions.
```

New text:

```text
and it asks whether the product exists, then at most 4 clarifying questions.
```

The build also adds VER-29's steps (section 5) to this runbook.

### 2.11 Eval cases

Three new hand-written case folders under `src/claude/DevForgeAI/evals/brainstorm/`: `records-project-kind`,
`kind-not-decided` and `cites-sources` (section 5). No existing case changes: section 5, "What was checked",
shows that the ten existing cases' regex graders give the same result on a new-shape BRN.

## 3. Behaviour

### 3.1 Items

```yaml items
behaviors:
  - id: BEH-20
    status: proposed
    rule:
      - "After the topic and extend-or-new, decide the project kind by the first rule that matches: (1) the BRN being extended, or the work file of a continued run, has the line 'Project kind: greenfield' or 'Project kind: brownfield': that kind, and nothing is asked, with the one exception of the next item; (2) the user's words say the product exists: brownfield; (3) the user's words say it does not exist: greenfield; (4) the skill can ask and the run is not a continued one: the kind question, whose answer decides; (5) otherwise the kind is not decided. When rules 2 and 3 both match, neither does."
      - "When a new-shape BRN is extended, its kind line changes only in these ways. A 'greenfield' line becomes 'brownfield' when the user's words in this run say the product exists (rule 2); otherwise it stays, and nothing is asked. The NEEDS CLARIFICATION line is decided again by rules 2 to 5 and becomes 'greenfield' or 'brownfield' when one of them decides; when that BRN already holds the four brownfield headings it can become only 'brownfield'. A 'brownfield' line never changes. When the user's words say the product does not exist and the line can't follow them (a 'brownfield' line, or the NEEDS CLARIFICATION line with the four headings), the skill says 'BRN-NNN records this product as brownfield. To brainstorm it as a new product, create a new BRN.', keeps the line, and goes on with the extension unless the user asks for a new BRN. When the line becomes 'brownfield', brownfield-iteration.md BEH-29 adds the brownfield parts; nothing is ever removed from the BRN. The one thing taken out is section 7's bullet that says which kind an undecided run worked as: it goes when the kind line is decided (IV-07)."
      - "The user's words are the arguments, the user's messages in the conversation and the answer to the topic question. Only an explicit statement about the product counts, by the test and the seven examples of references/intake.md (section 3.2). A file in the project never decides the kind."
      - "The kind question is asked alone in its own AskUserQuestion form tagged devforgeai_step:1 with header 'Step 1': 'Does the product this brainstorm is about already exist?', options 'It exists' and 'It doesn't exist yet', in this order, with the descriptions of section 3.3. When docs/specs/prd/PRD-*.md matches at least one file, the first label is 'It exists (Recommended)' and its description ends with ' This project has a PRD.' Typed text is judged by rules 2 and 3; a dismissal, or text matching neither or both, leaves the kind not decided. Without AskUserQuestion the question is asked in plain text, alone, and the turn ends."
      - "The skill can ask unless the request says to proceed without questions and the waiver (BEH-13) was answered Proceed without questions or couldn't be asked. After Proceed without questions the kind question is never asked."
      - "When the kind is not decided, write the line 'Project kind: [NEEDS CLARIFICATION: greenfield or brownfield]' and work with brownfield when docs/specs/prd/PRD-*.md matches at least one file, else with greenfield. The kind worked with chooses the question set (BEH-21), the framework rule that reads the kind (README section 5, rule 4), the template's brownfield-only parts and whether brownfield-iteration.md applies. It is never written as the project kind."
      - "A BRN whose kind is not decided records it in three places (Bryan, 2026-11-19: 'Record that the kind is still undecided.'): the NEEDS CLARIFICATION kind line; one bullet among section 7's open questions, written before the others, exactly '- [NEEDS CLARIFICATION: greenfield or brownfield; this run worked as greenfield]' or the same with 'worked as brownfield'; and one sentence in the final reply's discussion, 'The project kind is not decided: I worked as <greenfield or brownfield> because this project has <a PRD or no PRD>. Tell me whether the product exists and I will update BRN-NNN.' The report block names the kind as 'not settled' (prd-handoff-contract.md, BEH-34). The bullet is written only while the kind line is the NEEDS CLARIFICATION line: when the kind is decided later, in this run or an extension, the bullet is removed in the same edit."
      - "Write the kind line as the first line under '## 1. Context', followed by a blank line and the context prose (C-01)."
      - "An explicit statement the user makes later, before the BRN is written, replaces the kind; a change to brownfield runs the brownfield reading before the next step's work."
      - "A BRN without the project-kind line that is being extended gets no kind: no line and no shape of this document is added to it, and the greenfield question set is asked."
    changes: "new; extends BEH-01's intake and BEH-11 (an extended BRN without the project-kind line keeps its earlier shape)"
    lands_in: "SPEC-001 §6; SKILL.md step 1 item 3 (edit A-S2), 'Extending an existing BRN' (edit A-S6), Examples (edit A-S7) and References (edit A-S8); references/intake.md, 'Project kind' and 'The kind question'"
  - id: BEH-21
    status: proposed
    rule:
      - "Ask at most four clarifying questions in step 1, in one AskUserQuestion form tagged devforgeai_step:1, each question with header 'Step 1' and multiSelect true: the greenfield set or the brownfield set of section 3.4, chosen by the kind decided or worked with, in the set's order, with its exact wording and options."
      - "Skip a question the user's words already answer, by the test of section 3.4 for that question. When all four are skipped, show no form."
      - "Ask no follow-up question in step 1. An option picked with nothing typed is recorded in the option's words and its missing detail as a NEEDS CLARIFICATION marker."
      - "Ask none of them when the request says to proceed without questions and the waiver was answered Proceed without questions or couldn't be asked."
      - "Without AskUserQuestion, and with no such request, ask the same questions as a numbered plain-text list without the options, in one message, and end the turn."
      - "Each answer fills what section 3.4's table names; what stays unknown is written as the marker that table gives."
    changes: "BEH-01: replaces 'at most three clarifying questions (trigger, affected users, constraints)' (edit A-P1)"
    lands_in: "SPEC-001 §6; SKILL.md step 1 item 4 (edit A-S2); references/intake.md, 'Clarifying questions'"
  - id: BEH-22
    status: proposed
    rule:
      - "A source is an input the brainstorm used: something the user gave or named, the user's own statement in the conversation, or a project document the skill read in this run. Write one frontmatter sources entry per source, as the quoted string '<kind>: <reference>', with the kind and the reference form of section 3.5's table, taking the first kind that fits."
      - "Never write an entry for anything else: what the skill knows by itself is not a source. Never fetch a source: no URL is opened and no web search is made."
      - "A project file the user names as a source is read (Bryan, 2026-11-19: 'You may read a project file I name as a source.'). A project file is a path in the user's words that, taken from the project root when relative, resolves to a regular file inside the project folder and outside its .git folder; a path that leaves the folder, a folder, and a pattern with a wildcard are not. The skill reads it whole with the Read tool, once, and nothing else because of it: it never edits, moves, deletes or runs it, and never reads a file the user did not name (the brownfield reading of brownfield-iteration.md apart). Its entry is 'document: <path from the project root>', then ' v<version>' when its frontmatter has an integer version. Facts taken from it are stated in its terms and cited with that entry. When it can't be read (it does not exist, it is not text, or the Read tool fails or is refused), ERR-07 applies."
      - "Write one note entry per run for the user's own statements. Clean each reference as section 3.5 says. Entries stand in the order the sources were first given or read, each once; when extending, existing entries are kept as they are and new ones appended."
      - "A fact written into an active problem's evidence or a section 8 baseline is either one NEEDS CLARIFICATION marker and nothing else, or a statement that ends with one sources entry, without its quotes, in parentheses after one space. When two sources state the fact, cite the one that stands first in sources."
      - "A fact from the skill's own knowledge is never written as evidence: the value is a marker naming the missing fact."
    changes: "new; replaces SKILL.md step 6's 'sources: fill from the conversation, or leave them empty'"
    lands_in: "SPEC-001 §6; SKILL.md Inputs, step 1 item 5, step 3 and step 6 (edits A-S1, A-S2, A-S3, A-S5); references/intake.md, 'Sources' and 'Citing a source'; references/output-rules.md"
  - id: BEH-23
    status: proposed
    rule:
      - "Section 3 holds exactly the table '| Persona | Job to be done | Current workaround | Pain |' and nothing else: one row per distinct who value of the active problems, in the order the values first appear, the Persona cell equal to the who value character for character (C-03)."
      - "Step 1's question 2 and step 3's framing gather the cells; step 6 writes the table, and the work file holds it from its first save."
      - "Each of the three other cells holds what the user's words or a source say about that persona, in at most 15 words, with no vertical bar and no citation. A cell nobody stated holds '[NEEDS CLARIFICATION: job to be done of <persona>]', '[NEEDS CLARIFICATION: current workaround of <persona>]' or '[NEEDS CLARIFICATION: pain of <persona>]'. It is never filled from a problem's statement or from general knowledge."
      - "A who value has no vertical bar, and one persona has one spelling in every problem."
    changes: "new; extends BEH-08 (section 3 was free prose)"
    lands_in: "SPEC-001 §6; SKILL.md step 6 item 2 (edit A-S4); references/intake.md, 'Target users (section 3)'; the template"
  - id: BEH-24
    status: proposed
    rule:
      - "Section 8 holds one bullet per first-release idea, in ID order: '- IDEA-NN: <observable outcome>; baseline <value>' (C-08). The first-release ideas are the active ideas whose row in section 6's First release cut table says yes; with no such table or no such row, section 8 holds the single line '- None.'"
      - "Step 5 gathers the bullets, once the first release cut is proposed; step 6 writes them, and the work file holds them at its step-5 save."
      - "The outcome is one clause naming what would be seen to change, for the persona of a problem the idea addresses, if the idea works. It states a direction and never a target number, and never contains '; baseline '."
      - "The baseline is today's value of that outcome as a cited fact (BEH-22), or the marker '[NEEDS CLARIFICATION: current <what is measured>]'."
    changes: "new; extends BEH-08 (section 8 was free bullets)"
    lands_in: "SPEC-001 §6; SKILL.md step 6 item 2 (edit A-S4); references/intake.md, 'Candidate success signals (section 8)'; the template"
```

### 3.2 The project kind: worked examples

The decision list is BEH-20's first rule. Whether the user's words "say the product exists" can't be made
mechanical (R9). The test the model applies: only an explicit statement counts, never an inference. *Exists*:
the words name the product and say it is built, released, live, in production or in use; or that it has users,
customers, data, issues or a version today; or they ask to improve, extend, fix, speed up, migrate or replace
it as something they have now. *Does not exist*: the words say it is new, not built yet, to be built from
scratch, an idea or a concept, or that nothing exists yet. A request that names only a goal or a symptom, and no
product, says neither. A new feature for a product that exists is brownfield.

| The user's words | Kind | Why |
|---|---|---|
| "Brainstorm improvements to our patient booking site, which went live in March." | brownfield | "went live" |
| "Our open-source CLI tool has 400 open GitHub issues. Brainstorm how to get triage under control." | brownfield | the tool has issues today |
| "Brainstorm ideas for making our internal expense-report approvals faster; right now an approval takes about nine working days." | brownfield | the process is named and in use now |
| "We want to build a new booking app for our clinic; nothing exists yet." | greenfield | "nothing exists yet" |
| "Brainstorm ideas for a feature that helps remote teams run better stand-ups in Slack." | not decided | it does not say whether the product the feature belongs to exists |
| "I run a small dental clinic. Brainstorm ways we could cut down on no-shows." | not decided | a goal, no product named |
| "We have a prototype nobody uses yet; brainstorm what the real product should be." | not decided | built, and not in use: both rules match |

What follows from "not decided", by case:

| Case | Kind question | Kind line written | Kind worked as |
|---|---|---|---|
| A user is there and the request does not waive | Asked; the answer decides | `greenfield` or `brownfield` | The same |
| The same, and the user dismisses the question | Asked once | The NEEDS CLARIFICATION line | Brownfield with a PRD in the project, else greenfield |
| The waiver was answered *Proceed without questions* | Never asked | The NEEDS CLARIFICATION line | Brownfield with a PRD in the project, else greenfield |
| No question tool and the request waives (an eval run) | Never asked | The NEEDS CLARIFICATION line | Brownfield with a PRD in the project, else greenfield |
| No question tool and the request does not waive | Asked in plain text; the turn ends | By the answer in the next turn | The same |

Example: the request "I run a small dental clinic … cut down on no-shows. Don't ask me any questions" in a
project that holds `docs/specs/prd/PRD-001.md`. Rules 1 to 3 don't match; rule 4 fails (the request waives and
there is no question tool); rule 5 writes `Project kind: [NEEDS CLARIFICATION: greenfield or brownfield]` and
the run works as brownfield: brownfield question set (none asked here), the brownfield reading, and the
template's brownfield-only parts kept. The same request in an empty project works as greenfield.

**The undecided kind is recorded** (Bryan, 2026-11-19: "Record that the kind is still undecided."). In the first
case of the example the BRN and the reply hold:

| Where | Text |
|---|---|
| Section 1, first line | `Project kind: [NEEDS CLARIFICATION: greenfield or brownfield]` |
| Section 7, first bullet | `- [NEEDS CLARIFICATION: greenfield or brownfield; this run worked as brownfield]` |
| The report block's first line (prd-handoff-contract.md) | `… (framework: diverge-converge; project kind: not settled)` |
| The final reply's discussion | "The project kind is not decided: I worked as brownfield because this project has a PRD. Tell me whether the product exists and I will update BRN-001." |

In the empty project the bullet ends `worked as greenfield` and the sentence reads "… I worked as greenfield
because this project has no PRD. …". When the user then says "it has been live since March", the skill edits
BRN-001 in place as SKILL.md's *Decisions that belong to the user* describes for a later confirmation: the kind
line becomes `Project kind: brownfield`, the bullet is removed, and a run that had worked as greenfield does
the brownfield reading and adds the brownfield parts; then it validates and reports again.

### 3.3 The kind question

| Part | Text |
|---|---|
| Form | One question, alone; `metadata: {"source": "devforgeai_step:1"}`; `header: "Step 1"`; asked after the topic and extend-or-new and before the clarifying questions |
| Question | "Does the product this brainstorm is about already exist?" |
| Option 1 | Label `It exists`; description "Brownfield: it is built or in use. I read the project's documents and earlier brainstorms before we start." |
| Option 2 | Label `It doesn't exist yet`; description "Greenfield: nothing is built or in use." |
| With a PRD in the project | Option 1's label is `It exists (Recommended)` and its description ends with " This project has a PRD." |

A PRD makes brownfield the recommended answer and nothing more: a team may keep the PRD of a product that was
never built. Without a PRD no option is recommended.

### 3.4 The clarifying questions

Four, in one form, because one AskUserQuestion form holds at most four questions (ADR-003 A2, "Platform
limit") and a fifth would need a second form. The fourth question is new: it asks for evidence, which is what
fills `sources` and `evidence`.

**Greenfield set**

| # | Question | Options (labels, in order) |
|---|---|---|
| 1 | "What triggered this brainstorm?" | `A problem we keep hitting`, `A request from users or customers`, `A new opportunity`, `A deadline or outside change` |
| 2 | "Who is affected, and what do they do today instead?" | `Customers or end users`, `Our own staff`, `Another team or partner` |
| 3 | "What constraints apply?" | `A fixed deadline`, `A fixed budget`, `Technology we must use`, `Rules or regulation` |
| 4 | "What evidence should I use?" | `Numbers or reports`, `Support tickets or complaints`, `Interviews or feedback`, `None yet` |

**Brownfield set**

| # | Question | Options (labels, in order) |
|---|---|---|
| 1 | "What triggered this brainstorm about the existing product?" | `A problem users keep hitting`, `A request from users or customers`, `A metric that moved`, `A new opportunity` |
| 2 | "Which users of the product are affected, and what do they do today instead?" | `Existing customers or end users`, `People who tried it and left`, `Our own staff` |
| 3 | "What must stay as it is?" | `Behaviour users rely on`, `Existing data and integrations`, `Commitments already made`, `Nothing is fixed` |
| 4 | "What evidence from the product in use should I use?" | `Usage data or reports`, `Support tickets or complaints`, `Interviews or feedback`, `None yet` |

Every question has `multiSelect: true`; the user types detail under Other. Options carry no description.

**When a question is skipped.** A judgment (R9), made per question on the user's words:

| # | Skip when the words | Skipped: example | Asked: example |
|---|---|---|---|
| 1 | give a reason for brainstorming now: an event, a number, a complaint, a request or a deadline | "one in eight booked appointments ends in a no-show, and it's costing us real money" | "Brainstorm ideas for a loyalty scheme." |
| 2 | name at least one group of affected people | "helps remote teams run better stand-ups" | "ways we could cut down on no-shows" |
| 3 | state at least one limit: a deadline, a budget, a technology, a rule, or something that must not change | "There are only two of us maintaining it, in our spare time." | "Brainstorm how to get issue triage under control." |
| 4 | name at least one source other than the user's own statement: a document, a dataset or report, a ticket, an interview or a URL | "the front-desk no-show log for August shows one in eight" | "about one in eight appointments is missed" |

**What each answer fills.**

| # | Fills | Unknown after the answer |
|---|---|---|
| 1 | Section 1's context prose | `[NEEDS CLARIFICATION: what triggered this brainstorm]` in the prose |
| 2 | Each problem's `who`, and section 3's cells | The cell markers of BEH-23 |
| 3 | Section 1's context prose | `[NEEDS CLARIFICATION: constraints]` in the prose |
| 4 | `sources` and each problem's `evidence` | The marker of BEH-22 |

An option picked with nothing typed is recorded as the option's words with a marker for its detail: `A fixed
deadline` gives "A fixed deadline applies: [NEEDS CLARIFICATION: the deadline's date]". `None yet` and `Nothing
is fixed` record nothing.

**Under the waiver.** After *Proceed without questions*, or when the waiver couldn't be asked and the request
waives, no clarifying question and no kind question is asked. The waiver's own text (BEH-13) does not change:
its description names the topic and extend-or-new questions as the only ones still asked, and VER-15 checks it
word for word. On *Ask me as usual*, typed text or a dismissal, both the kind question and the set are asked.

### 3.5 Sources and citations

The entry is `"<kind>: <reference>"`. Take the first kind that fits, in this order:

| Kind | What it is | Reference | Example entry |
|---|---|---|---|
| `ticket` | An issue or support ticket, given by ID or link | The tracker and ID, or the link, as the user gave it | `"ticket: GitHub issue 412"` |
| `data` | Numbers (counts, rates, measurements) from a dataset, report, log, survey or analytics tool | Its name as the user gave it, then `, ` and the period or date when given | `"data: front-desk no-show log, August 2026"` |
| `interview` | What a named person or group said in words when asked, with no count | Who, by the name or role given, then `, ` and the date or month when given | `"interview: three hygienists, October 2026"` |
| `document` | A file or a named document | A project file: its path from the project root, then ` v` and the `version` of its frontmatter when it has one. Any other document: its title as the user gave it | `"document: docs/specs/prd/PRD-001.md v3"` |
| `url` | A web address not covered above | The address exactly as given | `"url: https://example.com/no-show-study"` |
| `note` | The user's own statement in this conversation, with no other source named | The owner's name, or `user` when the owner is unknown, then `, conversation of ` and today's date | `"note: Dana, conversation of 2026-11-18"` |

A survey's counts are `data`: "in our contributor survey of October 2026, 12 of 20 contributors said they gave
up" gives `"data: contributor survey, October 2026"`. What people said, with no count, is `interview`: "three
hygienists told us in October that the reminder cards get lost" gives `"interview: three hygienists, October
2026"`. mvp-and-prototype-path.md's Confidence cell reads the kind, so the order matters.

**A project file the user names** (Bryan, 2026-11-19: "You may read a project file I name as a source."):

| The user's words | A project file? | What the skill does |
|---|---|---|
| "the survey results are in docs/contributor-survey.md" | Yes | Reads it whole with the Read tool; entry `"document: docs/contributor-survey.md"`; facts from it cite that entry |
| "see docs/specs/prd/PRD-001.md" | Yes | Reads it; entry `"document: docs/specs/prd/PRD-001.md v3"` (its frontmatter has `version: 3`) |
| "it's all in ../shared/handbook.pdf" | No: the path leaves the project folder | Does not read it; entry `"document: ../shared/handbook.pdf"`; uses only what the user said it shows |
| "look through the notes folder" | No: a folder | Reads nothing; no entry; the user's statements stay the `note` entry |
| "docs/old-survey.md" (the file does not exist) | Yes, but it can't be read | ERR-07: entry `"document: docs/old-survey.md"`, and the reply says so |

The read is read-only and happens once, when the file is named. The skill reads no other file on its own
account: not a file it thinks relevant, not a neighbour of the named one.

Cleaning a reference: one line, no leading or trailing space, runs of spaces collapsed, `"` replaced by `'`,
`|` replaced by `/`, no final period.

Worked example. The request: "Our front-desk no-show log for August 2026 shows that one in eight booked visits
was missed. Most of them are people who booked more than a month ahead." It names one dataset and adds a
statement of the user's own. With the owner unknown, on 2026-11-18:

```yaml
sources:
  - "data: front-desk no-show log, August 2026"
  - "note: user, conversation of 2026-11-18"
```

```yaml
    evidence: "One in eight booked visits was missed (data: front-desk no-show log, August 2026)"
    evidence: "Most missed visits were booked more than a month ahead (note: user, conversation of 2026-11-18)"
    evidence: "[NEEDS CLARIFICATION: how many patients say they forgot the date]"
```

The third problem is one the skill framed itself: nobody stated a fact for it, so it holds one marker.

### 3.6 Validator checks

All seven apply only to a new-shape BRN (the gate): a BRN with at least one line, after the frontmatter and outside
every fenced block, that starts with `project kind:` once lowercased and with its runs of spaces collapsed. "A
`sources` entry" below is the entry's text between its quotes, with `\"` read as `"` and `\\` as `\`; a problem's
`who` and `evidence` are read the same way. "Active" is an item whose `status` is `active`.

| Check | Rule | Reported at | Message |
|---|---|---|---|
| IV-01 | There is one project-kind line | each further such line | `only one Project kind line is allowed (IV-01)` |
| IV-01 | The line is exactly one of C-01's three lines | the first such line | `the Project kind line must be exactly 'Project kind: greenfield', 'Project kind: brownfield' or 'Project kind: [NEEDS CLARIFICATION: greenfield or brownfield]' (IV-01)` |
| IV-01 | The line is the first non-blank line after `## 1. Context`, and the line after it is blank | the first such line | `the Project kind line must be the first line under '## 1. Context', followed by a blank line (IV-01)` |
| IV-02 | Each `sources` entry starts with one of the six kinds, a colon, a space and a non-space character, has no leading or trailing space and no vertical bar | the entry's line | `sources entry <the entry as written> must be "kind: reference" with no \| in it, the kind being document, data, ticket, interview, url or note (IV-02)` |
| IV-02 | No valid entry stands twice | the second one's line | `duplicate sources entry <the entry as written> (IV-02)` |
| IV-03 | Each active problem's quoted `evidence` is one marker and nothing else, or ends with a space and one valid `sources` entry in parentheses, with text before it | the `evidence` line | `PRB-NN: evidence must be one [NEEDS CLARIFICATION: ...] marker or end with one sources entry in parentheses, such as "... (data: no-show log, August 2026)" (IV-03)` |
| IV-04 | Section 3's first two non-blank lines are the header `\| Persona \| Job to be done \| Current workaround \| Pain \|` and `\|---\|---\|---\|---\|` | the section's first non-blank line, or its heading when it is empty | `section 3 must start with the table header '\| Persona \| Job to be done \| Current workaround \| Pain \|' and the line '\|---\|---\|---\|---\|' (IV-04)` |
| IV-04 | Every further non-blank line of section 3 is a row with four non-empty cells | that line | `section 3 holds only the Target users table: each row has four non-empty cells (IV-04)` |
| IV-04 | The Persona cells of the well-formed rows, in order, equal the distinct `who` values of the active problems in the order they first appear | the header line | `section 3's Persona cells must be the active problems' who values, each once, in the order they first appear: expected <values joined by "; ">, got <cells joined by "; "> (IV-04)` |
| IV-05 | Section 8's non-blank lines are the single line `- None.`, or each matches `- IDEA-NN: <text>; baseline <text>` (split at the first `; baseline `) | each line that does not match, or the heading when the section is empty | `section 8 holds one bullet per first-release idea, '- IDEA-NN: outcome; baseline value', or the single line '- None.' (IV-05)` |
| IV-05 | A bullet's idea is an active idea of the BRN | the bullet's line | `section 8: IDEA-NN is not an active idea (IV-05)` |
| IV-05 | Each bullet's ID is greater than the one before | the bullet's line | `section 8's bullets must be in ID order, each idea once (IV-05)` |
| IV-05 | A bullet's baseline is one marker and nothing else, or ends with a space and one valid `sources` entry in parentheses, with text before it | the bullet's line | `IDEA-NN: baseline must be one [NEEDS CLARIFICATION: ...] marker or end with one sources entry in parentheses (IV-05)` |
| IV-06 | The set of the bullets' IDs equals the set of ideas whose row under `### First release cut` in section 6 has `yes` in its second cell (no such heading or row: the empty set) | section 8's heading | `section 8 must hold one bullet for each idea whose First release cut row says yes (<IDs joined by ", ", or none>) and no other; with none, the single line '- None.' (IV-06)` |

A marker is text matching `^\[NEEDS CLARIFICATION: [^\[\]]+\]$`. A table row is a line that, stripped, starts and
ends with `|`; its cells are the text between the bars, stripped. Edit A-V1's code is the reference for every
detail the table leaves out.

| IV-07 | While the kind line is the NEEDS CLARIFICATION line, section 7 holds exactly one line `- [NEEDS CLARIFICATION: greenfield or brownfield; this run worked as greenfield]` or the same with `worked as brownfield` | section 7's heading | `while the project kind is not decided, section 7 must hold exactly one bullet '- [NEEDS CLARIFICATION: greenfield or brownfield; this run worked as greenfield]' or the same with 'worked as brownfield' (IV-07)` |
| IV-07 | While the kind line says `greenfield` or `brownfield`, section 7 holds no such line | each such line | `the project kind is decided: remove the bullet that says which kind the run worked as (IV-07)` |

IV-06 reads C-05's table and nothing else of it. Until mvp-and-prototype-path.md's commit the skill writes no
such table, so section 8 is `- None.` and IV-06 passes.

Not checked by the validator, because they need judgment: that a source was really given (BEH-22), that a cell of
section 3 says what the user said (BEH-23), that an outcome is observable (BEH-24). Section 5 covers them with
`llm` graders and manual items.

## 4. Errors and edge cases

```yaml items
errors:
  - id: ERR-07
    status: proposed
    condition: "The user names a source the skill can't open: a URL, a document outside the project folder, or a project file (BEH-22) that does not exist, is not text, or that the Read tool fails or is refused to read"
    handling: "Write its sources entry by BEH-22 (a project file that can't be read: 'document: <its path from the project root>' with no version). Fetch nothing, and try no other file or tool in its place. For a project file, say in the reply 'I could not read <path>, so I used only what you said about it.' Use only what the user said the source shows, cited with that entry; a fact nobody stated is a NEEDS CLARIFICATION marker"
    user_result: "The source is listed in sources; the facts cited from it are the user's own words about it; nothing was fetched or invented"
    changes: "new"
    lands_in: "SPEC-001 §7; references/intake.md, 'Sources'"
```

Edge cases, each decided by the items above:

| Case | What happens | By |
|---|---|---|
| The request says both "our live site" and "the new product, not built yet" | Rules 2 and 3 both match, so neither does: the kind question is asked, or the kind is not decided | BEH-20 |
| The user dismisses the kind question | The NEEDS CLARIFICATION line and section 7's bullet with the kind the run worked as; the question is not asked again in this run or a continued one | BEH-20 |
| The user names `docs/contributor-survey.md` as evidence | The skill reads it with the Read tool, lists `"document: docs/contributor-survey.md"` and cites it for the facts it takes from the file | BEH-22 |
| The user names a file outside the project folder, or a folder | Not read. A file outside is listed by the path as given, and only the user's words about it are used; a folder gives no entry | BEH-22, ERR-07 |
| The user names a story or a spec of the project as a source | It is a project file: read under BEH-22 and listed as a `document` entry. It is never an Existing product row; brownfield-iteration.md reads no story and no spec on its own | BEH-22 |
| The kind was not decided and the user later writes "it's been live for a year" | Brownfield from then on; the brownfield reading runs before the next step's work; the kind line says brownfield and section 7's bullet is not written (or is removed) | BEH-20 |
| Extending BRN-001, which has no project-kind line | No kind, no new shape, the greenfield question set; `sources` and sections 3 and 8 are written as that BRN has them | BEH-20, the gate |
| Extending a new-shape BRN whose line is the NEEDS CLARIFICATION one | Rule 1 doesn't match; rules 2 to 5 run again, so the question can be asked in this run. The line becomes `greenfield` or `brownfield`; with the four brownfield headings already in the BRN, only `brownfield` | BEH-20 |
| Extending a `greenfield` BRN, and the user now says the product is live | The line becomes `brownfield`; the brownfield reading runs and the four headings are added | BEH-20, brownfield-iteration.md BEH-29 |
| Extending a `brownfield` BRN, and the user says the product does not exist | The line stays `brownfield`; the skill says the BRN records it as brownfield and that a new BRN can be created | BEH-20 |
| Every clarifying question is answered by the request | No form is shown | BEH-21 |
| The user picks `None yet` for evidence | No source besides the `note` entry; problems the user gave no fact for hold markers | BEH-21, BEH-22 |
| The user states a number and names no source | The `note` entry; the fact is cited with it | BEH-22 |
| The skill knows a typical figure (an industry no-show rate) | Not written. The evidence is a marker | BEH-22 |
| Two problems have the `who` values "Patients" and "patients" | Two personas for the validator. The skill uses one spelling, so this arises only by mistake and IV-04 reports the missing row | BEH-23 |
| No idea is promoted or proposed for promotion | Section 8 is `- None.` | BEH-24 |
| A user confirms the first release cut later with changes | Step 6 edits section 8 with the BRN, so its bullets match the `yes` rows again; IV-06 fails otherwise | BEH-24 |

## 5. Verification

Eval cases are hand-written, like brainstorm's other cases. Each new case's `prompt.md` has the frontmatter
`description` (the obligation's first sentence), `tags: [brainstorm, ver-NN]`, `max_turns: 60`, `timeout_seconds:
900` and `allowed_tools: [Skill, Read, Glob, Grep, Write, Edit, Bash]`. A `regex` grader's file has `type:
regex`, `target: {source: file, path: <path>}` (or `target: last_message`), `match: contains` or `match:
not_contains`, and the pattern as its body; an `llm` grader with `focus` reads that file, otherwise the final
reply. No grader uses a flag. For a `tool_used` or `file_exists` grader the `pattern` below lists the grader
file's frontmatter keys, separated by semicolons: `tool`, `input_match` (written in single quotes in the file, as
`writes-valid-brn/graders/ran-validator-alone.md` does), `min`, `max`; or `path`, `exists`. No eval can answer a
question (R5), so every prompt says to proceed without questions and the graders check the unconfirmed forms.

```yaml items
verifications:
  - id: VER-25
    status: proposed
    covers:
      - BEH-20
      - BEH-23
      - BEH-24
    level: eval
    obligation: "A request that says the product does not exist yet gives a BRN whose first line under section 1 is 'Project kind: greenfield', with no brownfield subsection, section 3 as the Target users table and section 8 as success-signal bullets or '- None.'"
    case: records-project-kind
    prompt: |-
      We want to build a new booking app for our dental clinic. Nothing exists yet: patients can only
      phone us during opening hours. Brainstorm what the app should do first. Don't ask me any
      questions, just work through it and write it up.
    scaffold: none
    graders:
      - name: skill-fired
        type: tool_used
        pattern: 'tool: Skill; input_match: "skill"\s*:\s*"(?:[\w-]+:)?brainstorm"'
      - name: brn-exists
        type: file_exists
        pattern: 'path: docs/specs/brainstorm/BRN-001.md; exists: true'
      - name: kind-greenfield
        type: regex
        target: docs/specs/brainstorm/BRN-001.md
        match: contains
        pattern: '\n## 1\. Context\n+Project kind: greenfield\n\n'
      - name: no-brownfield-parts
        type: regex
        target: docs/specs/brainstorm/BRN-001.md
        match: not_contains
        pattern: '\n### (?:Existing product|Already covered|Previously decided|Assumption updates)\n'
      - name: target-users-table
        type: regex
        target: docs/specs/brainstorm/BRN-001.md
        match: contains
        pattern: '\n## 3\. Target users\n+\| Persona \| Job to be done \| Current workaround \| Pain \|\n\|---\|---\|---\|---\|\n(?:\|[^|\n]+\|[^|\n]+\|[^|\n]+\|[^|\n]+\|\n)+\n*## 4\. Ideas\n'
      - name: success-signals-form
        type: regex
        target: docs/specs/brainstorm/BRN-001.md
        match: contains
        pattern: '\n## 8\. Candidate success signals\n+(?:- None\.\n|(?:- IDEA-\d{2}: [^\n]+; baseline [^\n]+\n)+)\n*## Change Log\n'
      - name: personas-match-who
        type: llm
        focus: docs/specs/brainstorm/BRN-001.md
        pattern: "The file is a brainstorm document. PASS if every Persona cell of the table in section 3 (Target users) is, character for character, the `who` value of at least one problem in the problems block, and every distinct `who` value has exactly one row. FAIL otherwise, and quote the persona or the who value that has no match."
      - name: ran-validator-alone
        type: tool_used
        pattern: 'tool: Bash; input_match: "command"\s*:\s*"(?:[^"\\;|&]|\\[^n]|&&|[0-9]?>&[0-9]?)*validate_brn\.py(?:[^"\\;|&]|\\[^n]|&&|[0-9]?>&[0-9]?)*"'
  - id: VER-26
    status: proposed
    covers:
      - BEH-20
    level: eval
    obligation: "A request that does not say whether the product exists, with nobody to ask and a PRD in the project, gives the NEEDS CLARIFICATION kind line, never 'brownfield'; section 7 holds the bullet that says the run worked as brownfield; the run works as brownfield (the Existing product table lists the PRD); the reply says the kind is not decided; and the PRD is unchanged."
    case: kind-not-decided
    prompt: |-
      I run a small dental clinic with two dentists and a hygienist. About one in eight booked
      appointments ends in a no-show, and it's costing us real money. Brainstorm ways we could
      cut down on no-shows. Don't ask me any questions, just work through it and write it up.
    scaffold: "scaffold.sh writes docs/specs/prd/PRD-001.md, byte for byte staged/examples/brainstorm-brownfield/PRD-001.md, and nothing else"
    graders:
      - name: skill-fired
        type: tool_used
        pattern: 'tool: Skill; input_match: "skill"\s*:\s*"(?:[\w-]+:)?brainstorm"'
      - name: brn-exists
        type: file_exists
        pattern: 'path: docs/specs/brainstorm/BRN-001.md; exists: true'
      - name: kind-needs-clarification
        type: regex
        target: docs/specs/brainstorm/BRN-001.md
        match: contains
        pattern: '\n## 1\. Context\n+Project kind: \[NEEDS CLARIFICATION: greenfield or brownfield\]\n\n'
      - name: undecided-recorded-in-section-7
        type: regex
        target: docs/specs/brainstorm/BRN-001.md
        match: contains
        pattern: '\n## 7\. Assumptions and open questions\n[\s\S]*\n- \[NEEDS CLARIFICATION: greenfield or brownfield; this run worked as brownfield\]\n[\s\S]*\n## 8\. '
      - name: reply-says-undecided
        type: llm
        pattern: "PASS if the final reply tells the user that the project kind (greenfield or brownfield) is not decided or not settled, says that the run worked as brownfield because the project has a PRD, and tells the user they can say whether the product exists. FAIL if the reply states as a fact that the product exists or that the project is brownfield, or does not mention that the kind is undecided."
      - name: works-as-brownfield
        type: regex
        target: docs/specs/brainstorm/BRN-001.md
        match: contains
        pattern: '\n### Existing product\n+\| Document \| Version \| What it already covers \|\n\|---\|---\|---\|\n\| PRD-001 \| 3 \| [^|\n]+ \|\n'
      - name: prd-unchanged
        type: regex
        target: docs/specs/prd/PRD-001.md
        match: contains
        pattern: '\nversion: 3\n[\s\S]*\nupdated: 2026-09-14\n[\s\S]*fixture-prd-4d2a[\s\S]*\| 3 \| 2026-09-14 \| Dana \| Approved \| status \|\s*$'
  - id: VER-27
    status: proposed
    covers:
      - BEH-22
      - ERR-07
    level: eval
    obligation: "A request that names a project file and a URL as sources: the file is read and left unchanged, sources holds a document entry for it and a url or ticket entry for the address, the fact that only the file states is in evidence and cites the file, no evidence value is neither a marker nor cited, and nothing is fetched."
    case: cites-sources
    prompt: |-
      Our open-source CLI tool has 400 open GitHub issues and most were never triaged (the list is at
      https://github.com/example/cli/issues). The results of our October contributor survey are in
      docs/contributor-survey.md. There are only two of us maintaining it, in our spare time.
      Brainstorm how we could get issue triage under control. Go ahead without asking me anything
      and write up the brainstorm.
    scaffold: "scaffold.sh writes docs/contributor-survey.md holding exactly four lines: '# Contributor survey, October 2026', an empty line, '12 of 20 contributors said they gave up on an issue because nobody answered. fixture-survey-5b0c' and '3 of 20 said the labels helped them find an issue to work on.'"
    graders:
      - name: skill-fired
        type: tool_used
        pattern: 'tool: Skill; input_match: "skill"\s*:\s*"(?:[\w-]+:)?brainstorm"'
      - name: brn-exists
        type: file_exists
        pattern: 'path: docs/specs/brainstorm/BRN-001.md; exists: true'
      - name: read-the-named-file
        type: tool_used
        pattern: 'tool: Read; input_match: "file_path"\s*:\s*"[^"]*docs/contributor-survey\.md"'
      - name: url-recorded
        type: regex
        target: docs/specs/brainstorm/BRN-001.md
        match: contains
        pattern: '\nsources:[\s\S]*?"(?:url|ticket): https://github\.com/example/cli/issues"[\s\S]*?\n---\n'
      - name: file-recorded
        type: regex
        target: docs/specs/brainstorm/BRN-001.md
        match: contains
        pattern: '\nsources:[\s\S]*?"document: docs/contributor-survey\.md"[\s\S]*?\n---\n'
      - name: evidence-cites-file
        type: regex
        target: docs/specs/brainstorm/BRN-001.md
        match: contains
        pattern: '\n[ \t]+evidence: "[^"\n]*12 of 20[^"\n]* \(document: docs/contributor-survey\.md\)"'
      - name: no-uncited-evidence
        type: regex
        target: docs/specs/brainstorm/BRN-001.md
        match: not_contains
        pattern: '\n[ \t]+evidence: (?!"\[NEEDS CLARIFICATION: [^\[\]"\n]+\]"[ \t]*\n)(?!"[^"\n]+ \((?:document|data|ticket|interview|url|note): [^"\n]+\)"[ \t]*\n)'
      - name: file-unchanged
        type: regex
        target: docs/contributor-survey.md
        match: contains
        pattern: '^# Contributor survey, October 2026\n\n12 of 20 contributors said they gave up on an issue because nobody answered\. fixture-survey-5b0c\n3 of 20 said the labels helped them find an issue to work on\.\n?$'
      - name: did-not-fetch
        type: tool_used
        pattern: 'tool: Bash; input_match: "command"\s*:\s*"(?:[^"\\]|\\.)*\b(?:curl|wget)\b; min: 0; max: 0'
      - name: facts-are-given
        type: llm
        focus: docs/specs/brainstorm/BRN-001.md
        pattern: "The file is a brainstorm document. These are all the facts its author was given. From the user: the tool has 400 open GitHub issues, most never triaged; two people maintain the tool in their spare time. From the project file docs/contributor-survey.md: 12 of 20 contributors said they gave up on an issue because nobody answered; 3 of 20 said the labels helped them find an issue to work on. PASS if no `evidence` value in the problems block states a number or a finding other than these. A value that is only a [NEEDS CLARIFICATION: ...] marker is fine. FAIL if any evidence value states another number, study or finding, and quote it."
  - id: VER-28
    status: proposed
    covers:
      - BEH-20
      - BEH-22
      - BEH-23
      - BEH-24
    level: unit
    obligation: "src/tests/brainstorm/test_validate_brn.py, run as 'python3 -B src/tests/brainstorm/test_validate_brn.py': the 29 tests of edit A-T3 pass in each of its three classes (with PyYAML, without the user site, with python3 -S). They show that a new-shape BRN passes; that each of IV-01 to IV-07 reports its message on its line; that an undecided kind passes only with its one section 7 bullet; that a deprecated problem, a kind line inside a fenced block and an earlier-shape BRN are not held to the checks; and that the unfilled template is rejected without a traceback. The file's other tests pass unchanged except the template's pinned line (edit A-T1)."
  - id: VER-29
    status: proposed
    covers:
      - BEH-20
      - BEH-21
      - BEH-22
      - ERR-07
    level: manual
    obligation: "Live, with AskUserQuestion, following docs/runbooks/brainstorm-manual-test.md with a copy of the plugin: (a) 'Brainstorm ways to cut no-shows at our dental clinic' in an empty project: the kind question comes alone, headed 'Step 1', with the labels 'It exists' and 'It doesn't exist yet' and neither recommended; (b) the same request in a project holding docs/specs/prd/PRD-001.md: the first label is 'It exists (Recommended)' and its description ends with 'This project has a PRD.'; (c) after 'It doesn't exist yet': one form with the greenfield set's questions that the request does not answer, in the set's order, wording and options, at most four, and the BRN's kind line says greenfield; (d) after 'It exists': the brownfield set; (e) a request that states the trigger, the people, a limit and a named report: no clarifying form is shown; (f) a request that says to proceed without questions, answered 'Proceed without questions': no kind question and no clarifying question, the kind line is the NEEDS CLARIFICATION one, section 7's first bullet is '- [NEEDS CLARIFICATION: greenfield or brownfield; this run worked as greenfield]' (as brownfield in the project of (b)), the report block says 'project kind: not settled' and the reply holds the sentence 'The project kind is not decided: I worked as greenfield because this project has no PRD. Tell me whether the product exists and I will update BRN-NNN.'; then the user writes 'it has been live since March': the BRN is edited in place, its kind line says brownfield, the bullet is gone and the validator prints OK; (g) the user answers question 4 with a URL: the BRN lists it as a url or ticket entry, and the session shows no fetch of it; (h) extending a BRN that has no project-kind line: the extended file has no such line and its section 3 keeps its shape; (i) extending a greenfield new-shape BRN with 'the site went live last month': the kind line becomes brownfield, the four brownfield headings are added and the validator prints OK; extending a brownfield BRN with 'nothing is built yet': the line stays brownfield and the reply says, word for word, 'BRN-NNN records this product as brownfield. To brainstorm it as a new product, create a new BRN.' (j) the user answers question 4 with 'the numbers are in docs/contributor-survey.md', a file of the project: the session shows one Read of it and no write to it, and the BRN lists 'document: docs/contributor-survey.md' and cites it; with a path that does not exist the reply says 'I could not read <path>, so I used only what you said about it.'; with '../other/notes.md' the session shows no Read of it. Recorded in SPEC-001 §9."
```

**What was checked while writing this document** (2026-11-18, in the worktree, with scratch copies only):

- Every edit of section 2 against version 11 of its file with framework-catalog.md's edits (S1 to S9, O1, W1
  to W3, R1 to R3) applied first: each old text occurs exactly once, ignoring line breaks; the eight SKILL.md
  edits add 17 lines (322 to 339).
- The validator with edits A-V1 and A-V2 applied to a scratch copy, and the test file with A-T1 to A-T3: 183
  tests pass (61 in each of the three classes), 29 of them new. The real `docs/specs/brainstorm/BRN-001.md`
  still prints `OK`.
- The same tests with mvp-and-prototype-path.md's validator edits (its V1 and V2, as that document stood on
  2026-11-18) added on top: they still pass. The fixture `NEW` holds a first release cut and a risk ranking in
  that document's grammar for this reason.
- The staged template under the changed validator: rejected, no traceback, its last line 191.
- Every `regex` pattern above, and the `input_match` of `did-not-fetch` and `read-the-named-file`, in
  node, against one good and one wrong sample.
- The regex graders of the ten existing brainstorm cases in node against a new-shape BRN: the same verdicts as on
  an earlier-shape BRN. In particular `no-decided-disposition` and `work-file-all-open` look for
  `disposition:` followed by a value, which no new shape contains.
- Every `yaml items` block of this document with PyYAML, for R4's keys.

**Re-checked on 2026-11-20** against `main` at `ff78d44`, after pull request #173 (SKL-001 version 12), with the
reviewer's script, which applies every edit of the five documents in build order to scratch copies: each edit of
section 2 still applies; the eight SKILL.md edits take the file from 331 to 348 lines; the validator's test file
as this document leaves it runs 183 tests, `OK`, with and without site-packages; the staged examples and the
project's own BRN-001 print `OK`.

## 6. Staged files

| Staged file | Destination | What it is |
|---|---|---|
| [staged/skills/brainstorm/references/intake.md](staged/skills/brainstorm/references/intake.md) | `src/claude/DevForgeAI/skills/brainstorm/references/intake.md` (new) | The reference the skill reads at step 1: the kind rules and question, both question sets, sources, citing, sections 3 and 8. Written for Claude, in the imperative, with a contents list |
| [staged/skills/brainstorm/assets/brainstorm.md](staged/skills/brainstorm/assets/brainstorm.md) | `src/claude/DevForgeAI/skills/brainstorm/assets/brainstorm.md` and `src/templates/brainstorm.md` (both replaced) | The one template of the build |

**The template.** It keeps today's frontmatter keys, the nine headings and the author-comment style, and adds:

| Shape | Where | Form in the template |
|---|---|---|
| C-01 | Section 1, first line | `Project kind: <greenfield or brownfield>`, then a comment giving the three allowed values |
| C-02 | Section 1, between brownfield markers | `### Existing product` and its table |
| C-03 | Section 3 | The table with one placeholder row |
| C-04, C-05 | Section 6 | The prose comment; `### First release cut`, its status line in the unconfirmed form, its table |
| C-06, C-11 | Section 6, between brownfield markers | `### Already covered`, `### Previously decided`, `### Assumption updates`, each with its table |
| C-07 | Section 7, after the `assumptions` block | `### Assumption risk ranking` and its table |
| C-08 | Section 8 | One placeholder bullet |
| C-09 | Frontmatter | The `sources` comment names the form and the six kinds |

The brownfield-only parts sit between the comment lines `<!-- brownfield only: start -->` and
`<!-- brownfield only: end -->`. The template's first comment gives the rule: greenfield, delete both lines and
everything between them; brownfield, keep what is between them and delete the two lines; kind not decided, do
as for the kind the run worked with. Every placeholder starts with `<` and a lower-case letter, so the
validator's leftover check reports any that remain. The comment under the kind line names the allowed values
without starting a line with `Project kind:`, so the gate reads one such line in the template.

C-05's and C-07's rows are placeholders in README's form; mvp-and-prototype-path.md owns their sentences and
rules and needs no change to the template.

## 7. Decisions and open questions

**Decisions made here**, each with its reason:

1. **The limit is four.** One AskUserQuestion form holds four questions. Evidence had no question, which is why
   `sources` and `evidence` were filled only by chance; a fourth question closes that without a second form.
2. **The kind question is a form of its own and is not one of the four.** The set depends on its answer. It is
   asked only when the user's words do not decide, so most runs see one form.
3. **A PRD never decides the kind.** A project can hold the PRD of a product that was never built. The PRD does
   two smaller things: it puts "(Recommended)" on *It exists*, and it chooses the kind the run works with when
   nobody can be asked.
4. **When the kind is not decided, the BRN says so and the run still picks a kind to work with.** Writing
   `brownfield` because a PRD exists would record a decision nobody made (R3). Working with no kind would leave
   the question set, the framework rule and the template undefined. The PRD is the only signal that exists
   without the user, so it chooses the working kind.
5. **No question is added to the waiver's exceptions.** BEH-13's description is fixed text that VER-15 checks.
   After *Proceed without questions* the kind is simply not decided.
6. **Every clarifying question has fixed options and `multiSelect: true`.** AskUserQuestion needs two to four
   options per question; leaving them to the builder would give two builds two different forms. The real
   BRN-001 records that "all four triggers apply", so more than one option must be selectable.
7. **No follow-up questions in step 1.** A picked option without detail becomes a marker. Otherwise the limit
   of four would not be a limit.
8. **`note` makes the user's own statement a source.** Without it, a fact the user states in the request could
   only be a marker or an uncited claim. One `note` entry per run keeps `sources` short.
9. **A fact cites exactly one entry, at its end, in parentheses.** The validator can check that by comparing
   strings, with or without PyYAML.
10. **Section 3's cells are never inferred.** A cell holds what was said or a marker. The PRD skill asks about
    users anyway (its interview), so a marker costs one question later; a guess would cost a wrong persona.
11. **Section 8 follows the first release cut, not the promoted ideas.** README fixes C-08 this way. The
    validator's cross-check (IV-06) reads C-05's table and lives here, so mvp-and-prototype-path.md does not
    repeat it.
12. **Validator messages end with the check's ID**, as mvp-and-prototype-path.md's do, so a failure names the
    rule to read.
13. **`who` may not hold a vertical bar** in a new-shape BRN. The Persona cell must equal it, and a bar would
    split the cell.
14. **An earlier-shape BRN is asked the greenfield set when extended.** Its three first questions are today's
    three; the fourth only adds sources, which that BRN's `sources` accepts in any form.

15. **An extended BRN's kind line moves only towards brownfield** (the lead's decision, 2026-11-19). The
    NEEDS CLARIFICATION line may be decided; `greenfield` may become `brownfield`; `brownfield` never
    changes, and nothing is removed from a BRN. A product that exists does not stop existing, and removing the
    brownfield parts would delete a record that a PRD may cite.

**Points settled with README** (each was a contradiction in an earlier draft; README now says the same).

- The gate is loose and C-01 is exact. README's gate defines a new-shape BRN by a line that *starts with*
  `project kind:` after lowercasing, and C-01 requires the line to be *exactly* one of three. Both hold: the
  gate uses the loose test, and IV-01 then rejects a line that passes the gate but is not exact
  (`project  kind: Brownfield`).
- A cited fact that is a marker is one marker and nothing else (README C-09; IV-03, IV-05): a value such as
  `High, we think [NEEDS CLARIFICATION: …]` would otherwise pass as cited.
- The user's own statements are one `note` entry (section 3.5), never an `interview` entry.
  `staged/examples/brainstorm-greenfield-mvp/BRN-001.md` (mvp-and-prototype-path.md) records its owner's
  statements that way.

**Decided by Bryan on 2026-11-19** (pull request #172's open questions; his words are quoted).

16. **The limit of four is fixed, not a setting.** The question was whether to expose it as a setting. "Keep
    the four-question limit fixed." ADR-003's row keeps it an interaction default whose value becomes 4;
    configuration contract v1 gains no key, and the skill reads no setting for it (section 2.2).
17. **Not decided and nobody to ask: brownfield with a PRD, greenfield otherwise, and the BRN says the kind is
    undecided.** "When the project kind is undecided and you can't ask, use brownfield as the working mode if
    a PRD exists and greenfield otherwise. Record that the kind is still undecided." The working rule is the
    drafted one (decision 4). The record is new: besides the NEEDS CLARIFICATION kind line, section 7 holds a
    bullet that names the kind the run worked as, the reply says so in one fixed sentence, and the report
    block says `not settled` (BEH-20; IV-07). The bullet is a NEEDS CLARIFICATION bullet in an existing
    section, so R1 holds.
18. **The skill may read a project file the user names as a source.** "You may read a project file I name as a
    source." BEH-22 and section 3.5 say which paths count (a regular file inside the project folder), that
    the read is whole, once and read-only, the entry's form, and ERR-07 what happens when it can't be read.
    VER-27 now proves the read in an eval.

**Open, for Bryan.** None.
