"""Generates evals/ui/<case>/ for the ui skill (SPEC-017 §9, QR-03, VER-01 to VER-22 and VER-30 to VER-38): prompts,
graders, case.yaml and an inline scaffold per case.

Every fixture is built once here: BRN-001 and the four boards of SPEC-017 §9's shared fixture, the DSNs, PRDs, ADRs
and neighbouring documents the cases seed. An eval run starts in an empty workspace with no earlier conversation, so
each scaffold writes everything a case reads. Before writing anything, the generator
- runs each scaffold in a temporary folder and checks that it wrote exactly the files the case declares;
- validates each seeded document against src/schemas/ with a format checker, except a document a case marks as
  expected to be invalid (`invalid`) or unreadable (`unparseable`). A document that cites a DSN fails its schema on
  exactly one error until cycle C adds DSN to the document ID pattern (SPEC-017 §9, §10); `schema_errors` ignores that
  error, the docId pattern's, at frontmatter/upstream/N/id for an instance that matches ^DSN-\\d{3}$, and no other.
  test_make_evals.py asserts that the error is present for each such fixture, so the suite fails the day the schema
  accepts DSN, and the exemption is then removed;
- runs the skill's dsn_check.py over every seeded boards folder (`boards`) and DSN (`check`, or `check
  --before-amend` for a fixture an amend run starts from), and fails on a surprise: the exact ERR a stop case is
  about, the exact `fact:` lines an amend run starts from, a current fixture that is not current.

SPEC-017 version 2: `claude -p`, which `claude plugin eval` runs, has no Artifact tool, so no case makes, adds to or imports a
canvas (those are the manual items VER-43 to VER-49). The e2e cases run the copy path (a fixture that seeds the boards
folder; the reply says the canvas was not checked), the stops (ERR-19 among them) and the drafting of the briefs (VER-39).
ToolSearch is among the allowed tools so that the skill's own check for the Artifact tool finds none, instead of being denied.
The negative trigger cases carry `runs: 10` in case.yaml (QR-04: at least 9 of 10 must not fire, --threshold 0.9).

Graders are JavaScript regular expressions (the harness's engine). SPEC-017 §9 writes whole-content anchors as ^…$ with
no m flag, which anchors at the start and end of the input, as the context suite does. Each grader's name starts with
the VER item it grades. A grader reads a reply or a file, never whether the prd skill exists (VER-02).

Run from the repository root, under the normal HOME (it imports jsonschema and referencing, from the user site):
    PYTHONDONTWRITEBYTECODE=1 python3 src/tests/ui/make_evals.py
"""
import hashlib
import os
import json
import re
import shutil
import subprocess
import sys
import tempfile
from dataclasses import dataclass, field
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator, FormatChecker
from referencing import Registry, Resource

sys.dont_write_bytecode = True

REPO = Path(__file__).resolve().parents[3]
ROOT = REPO / "src/claude/DevForgeAI/evals/ui"
SCHEMAS = REPO / "src/schemas"
SCRIPT = REPO / "src/claude/DevForgeAI/skills/ui/scripts/dsn_check.py"
EXAMPLE = REPO / "src/staging/examples/context-cli-service-rdbms/docs/specs"
# ToolSearch is how the skill checks for the Artifact tool (SKILL.md, Tools): a `claude -p` run has none (ERR-19)
TOOLS = "[Skill, Read, Glob, Grep, Write, Edit, Bash, ToolSearch]"
WRITING_LIMITS = (60, 900)   # §9: a case that writes
SHORT_LIMITS = (15, 300)     # §9: the stop cases and the trigger cases
SKILL_MATCH = r"""'"skill"\s*:\s*"(?:[\w-]+:)?ui"'"""
FIXTURE_SESSION = "00000000-0000-0000-0000-000000000000"
MODEL = "claude-opus-5-5"
DESIGN = "docs/specs/design"
BRN_PATH = "docs/specs/brainstorm/BRN-001.md"
CANVAS_URL = "https://claude.ai/artifact/EXAMPLE"
CANVAS_VERSION = "17-example"
BOARD_ORDER = ["Home.dc.html", "List.dc.html", "Add.dc.html", "Report.dc.html"]


def replace(text, old, new, count=1):
    assert text.count(old) == count, f"expected {count} of {old!r}, found {text.count(old)}"
    return text.replace(old, new)


def digest(text):
    return hashlib.sha256(text.encode()).hexdigest()


# --------------------------------------------------------------------------------------------------------
# The boards (SPEC-017 §9: four small HTML files with a <title>; List and Add are terminal screens, Home and Report
# web pages). A board's <title> differs from its file name's stem, so a title that the user did not confirm shows.

HEAD = '<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n<title>{title}</title>\n</head>\n<body>\n'
TAIL = "</body>\n</html>\n"

BOARDS = {
    "Home.dc.html": HEAD.format(title="Shiftlog home") + (
        "<h1>Shiftlog</h1>\n<p>38 hours worked this week.</p>\n"
        '<nav><a href="Report.dc.html">Weekly report</a> <a href="List.dc.html">All shifts</a></nav>\n') + TAIL,
    "List.dc.html": HEAD.format(title="shiftlog list") + (
        "<pre>\n$ shiftlog list\n  DATE        START  STOP   HOURS\n  2026-10-05  09:00  17:30  8.5\n"
        "  2026-10-06  09:00  17:00  8.0\n</pre>\n") + TAIL,
    "Add.dc.html": HEAD.format(title="shiftlog add") + (
        "<pre>\n$ shiftlog add\nStart time (HH:MM)? 09:00\nStop time (HH:MM)? 17:30\nSaved a shift of 8.5 hours.\n"
        "</pre>\n") + TAIL,
    "Report.dc.html": HEAD.format(title="Weekly report") + (
        "<h1>Weekly report</h1>\n<table>\n<tr><th>Week</th><th>Hours</th></tr>\n"
        "<tr><td>2026-W41</td><td>38</td></tr>\n</table>\n") + TAIL,
}
REPORT_CHANGED = HEAD.format(title="Weekly report") + (
    "<h1>Weekly report</h1>\n<table>\n<tr><th>Week</th><th>Hours</th><th>Overtime</th></tr>\n"
    "<tr><td>2026-W41</td><td>38</td><td>2.5</td></tr>\n</table>\n") + TAIL
SETTINGS = HEAD.format(title="Settings") + (
    "<h1>Settings</h1>\n<p>Retention period: 90 days</p>\n") + TAIL
LIST_CHANGED = HEAD.format(title="shiftlog list") + (
    "<pre>\n$ shiftlog list\n  DATE        START  STOP   HOURS\n  2026-10-05  09:00  17:30  8.5\n"
    "  2026-10-06  09:00  17:00  8.0\nSync conflict: keep the local copy? [y/N]\n</pre>\n") + TAIL
DIGESTS = {name: digest(text) for name, text in BOARDS.items()}
BOARD_CONTENT = dict(BOARDS, **{"Settings.dc.html": SETTINGS})   # every board file the DSN fixtures know, by name


# Where each board sits on the canvas (DM-04: IF-02 prints x and y, BEH-09 proposes a flow's step order from them, y then x
# ascending). The first row is the flow report-and-home, Home then Report; the second is the flow shifts, List then Add;
# Settings, when it is added, comes last in the first row. They agree with the order the shared prompt states.
POSITIONS = {"Home.dc.html": (0, 0), "List.dc.html": (0, 900), "Add.dc.html": (1100, 900), "Report.dc.html": (1100, 0),
             "Settings.dc.html": (2200, 0)}


def canvas_json(names, v=3):
    """canvas.json in canvas order (never sorted: the order of the boards member is the canvas order)."""
    boards = {n: ({"x": POSITIONS[n][0], "y": POSITIONS[n][1], "w": 1040, "h": 760} if n in POSITIONS
                  else {"expand": False, "h": 640}) for n in names}
    return json.dumps({"v": v, "attachments": {}, "boards": boards}, indent=2) + "\n"


def boards_files(dsn_id="DSN-001", contents=None, names=None, canvas=None):
    """The files of one boards folder: canvas.json and each board named in it."""
    contents = BOARDS if contents is None else contents
    names = list(contents) if names is None else names
    base = f"{DESIGN}/{dsn_id}/boards"
    files = {f"{base}/canvas.json": canvas if canvas is not None else canvas_json(names)}
    files.update({f"{base}/{n}": contents[n] for n in names if n in contents})
    return files


# --------------------------------------------------------------------------------------------------------
# BRN-001, the shared fixture (SPEC-017 §9), and the variants

IDEAS = {
    "IDEA-01": "Add a shift from the terminal", "IDEA-02": "List shifts in a table",
    "IDEA-03": "A weekly report page", "IDEA-04": "Export shifts as CSV", "IDEA-05": "Sync to a server",
    "IDEA-06": "A dark theme for the report page",
}
SHARED_DISPOSITIONS = {"IDEA-01": "promoted", "IDEA-02": "promoted", "IDEA-03": "promoted", "IDEA-04": "promoted",
                       "IDEA-05": "parked", "IDEA-06": "promoted"}


def brn(id="BRN-001", title="Shiftlog: record shifts", status="converged", version=1, ideas=None, malformed=False,
        updated="2026-10-02"):
    """A brainstorm document. ideas is a list of (IDEA-NN, text, disposition); malformed breaks the ideas block."""
    if ideas is None:
        ideas = [(i, IDEAS[i], d) for i, d in SHARED_DISPOSITIONS.items()]
    items = ""
    for i, text, disposition in ideas:
        reason = '"Decided with the owner"' if disposition in ("promoted", "parked") else "null"
        items += (f'  - id: {i}\n    status: active\n    idea: "{text}"\n    addresses: ["PRB-01"]\n'
                  f'    value: "medium"\n    effort: "low"\n    risk: "low"\n    score: null\n'
                  f'    disposition: {disposition}\n    reason: {reason}\n')
    if malformed:
        items = replace(items, '    idea: "Add a shift from the terminal"\n', '    idea: "Add a shift from the terminal\n')
    n = id[-3:]
    return f"""\
---
id: {id}
type: brainstorm
title: "{title}"
status: {status}
version: {version}
created: 2026-10-01
updated: {updated}
owner: "Example Owner"
authors: ["Example Owner", "claude-code"]
generated_by:
  tool: "claude-code"
  model: "{MODEL}"
  session: "{FIXTURE_SESSION}"
reviewed_by: []
approved_by: ""
approved_on: null
upstream: []
supersedes: []
superseded_by: null
blocked_by: []
# --- brainstorm-specific ---
participants: ["Example Owner"]
sources: ["Interview notes"]
---

# {id} — {title}

## 1. Context

Shift workers record when they start and stop work, and want to see the hours they worked each week.

## 2. Problems

```yaml items
problems:
  - id: PRB-01
    status: active
    statement: "Workers lose track of the hours they worked each week"
    who: "Shift worker"
    evidence: "Interview notes"
    severity: high
```

## 3. Target users

Shift workers.

## 4. Ideas

```yaml items
ideas:
{items}```

## 5. Evaluation method

Value, effort and risk rated high, medium or low with the owner.

## 6. Convergence

The owner decided each idea's disposition.

## 7. Assumptions and open questions

```yaml items
assumptions:
  - id: ASM-01
    status: active
    statement: "We believe that workers will record shifts every day."
    validation: "Shifts recorded each week"
    state: open
```

- None.

## 8. Candidate success signals

- The hours worked each week are right.

## Change Log

| Version | Date | Author | Change |
|---|---|---|---|
| 1 | 2026-10-02 | claude-code (session {FIXTURE_SESSION}) | Converged |
""" + (f"| {version} | {updated} | claude-code (session {FIXTURE_SESSION}) | Revised | all |\n" if version > 1 else "")


BRN = brn()
BRN_ALL_OPEN = brn(ideas=[(i, IDEAS[i], "parked" if i == "IDEA-05" else "open") for i in IDEAS])
BRN_DRAFT_OPEN = brn(status="draft", ideas=[(i, IDEAS[i], "open") for i in IDEAS])
BRN_UNCONVERGED = brn(status="draft")
BRN_MALFORMED = brn(malformed=True)
# VER-12: version 2 promotes a new IDEA-07, and IDEA-02 is parked now
BRN_MOVED = brn(version=2, updated="2026-10-07", ideas=[
    ("IDEA-01", IDEAS["IDEA-01"], "promoted"), ("IDEA-02", IDEAS["IDEA-02"], "parked"),
    ("IDEA-03", IDEAS["IDEA-03"], "promoted"), ("IDEA-04", IDEAS["IDEA-04"], "promoted"),
    ("IDEA-05", IDEAS["IDEA-05"], "parked"), ("IDEA-06", IDEAS["IDEA-06"], "promoted"),
    ("IDEA-07", "Dark theme for List", "promoted")])
BRN_2 = brn("BRN-002", "Shiftlog: remind about open shifts", ideas=[
    ("IDEA-01", "Remind the user when a shift is left running", "promoted"),
    ("IDEA-02", "Show the open shift at login", "promoted"),
    ("IDEA-03", "Send reminders by e-mail", "parked")])

# --------------------------------------------------------------------------------------------------------
# DSN documents, in the form the skill writes (assets/dsn.md, references/output-rules.md)


@dataclass
class Brd:
    id: str
    file: str
    flow: str = None
    surface: str = None
    ideas: list = None
    title: str = None
    answers: list = field(default_factory=list)
    sha: str = None
    status: str = "active"
    notes: str = None
    superseded_by: str = None

    @property
    def stem(self):
        return self.title or (self.file.split(".")[0] or self.file)


def standard_boards(report=None, contents=None):
    """The four boards of the shared prompt, every mapping confirmed (SPEC-017 §9)."""
    contents = BOARD_CONTENT if contents is None else contents
    return [
        Brd("BRD-01", "Home.dc.html", "report-and-home", "web", ["IDEA-02"], sha=digest(contents["Home.dc.html"])),
        Brd("BRD-02", "List.dc.html", "shifts", "terminal", ["IDEA-02"], sha=digest(contents["List.dc.html"])),
        Brd("BRD-03", "Add.dc.html", "shifts", "terminal", ["IDEA-01"], sha=digest(contents["Add.dc.html"])),
        Brd("BRD-04", "Report.dc.html", "report-and-home", "web", ["IDEA-03"],
            sha=digest(report if report is not None else contents["Report.dc.html"])),
    ]


def list_text(values):
    return "null" if values is None else "[" + ", ".join(f'"{v}"' for v in values) + "]"


def brd_text(b):
    nulls = [k for k, v in (("flow", b.flow), ("surface", b.surface), ("ideas", b.ideas)) if v is None]
    notes = b.notes if b.notes is not None else (
        '"[NEEDS CLARIFICATION: ' + ", ".join(nulls) + ']"' if nulls else "null")
    if notes != "null" and not notes.startswith('"'):
        notes = json.dumps(notes)
    lines = [f"  - id: {b.id}", f"    status: {b.status}"]
    if b.superseded_by:
        lines.append(f"    superseded_by: {b.superseded_by}")
    lines += [f'    file: "{b.file}"', f'    title: "{b.stem}"', f"    flow: {b.flow or 'null'}",
              f"    surface: {b.surface or 'null'}", f"    ideas: {list_text(b.ideas)}",
              f"    answers: {list_text(b.answers)}", f'    sha256: "{b.sha}"', f"    notes: {notes}"]
    return "\n".join(lines) + "\n"


def link_line(brn_id, version, item=None):
    mid = f"item: {item}, " if item else ""
    return f"  - {{id: {brn_id}, {mid}relation: derives, version: {version}, hash: null}}\n"


def dsn(boards, coverage, *, id="DSN-001", brn_id="BRN-001", brn_title="Shiftlog: record shifts", status="draft",
        version=1, links_version=1, created="2026-10-08", updated="2026-10-08", canvas=CANVAS_URL,
        canvas_version=CANVAS_VERSION, canvas_format=3, copy_date=None, considered=(), approved_by="",
        approved_on=None, markers=(), changelog=None, link_ideas=None, scope=None, superseded_by=None,
        session=FIXTURE_SESSION):
    """A design document the skill could have written. coverage is a list of (IDEA-NN, boards cell, Status)."""
    if link_ideas is None:
        link_ideas = sorted({i for b in boards if b.status == "active" for i in (b.ideas or [])})
    upstream = link_line(brn_id, links_version) + "".join(link_line(brn_id, links_version, i) for i in link_ideas)
    flows = sorted({b.flow for b in boards if b.status == "active" and b.flow})
    scope = scope or (f"{brn_title} records and reports shifts. The design covers the flows "
                      f"{' and '.join(f.replace('-', ' ') for f in flows) or 'not yet confirmed'}.")
    canvas_marker = canvas is None or canvas_version is None
    section_5 = list(markers)
    if canvas_marker:
        section_5.append("[NEEDS CLARIFICATION: canvas URL and version copied]")
    rows = "".join(f"| {i} | {cell} | {st} |\n" for i, cell, st in coverage)
    if changelog is None:
        changelog = [(1, created, f"claude-code (session {session})",
                      f"Created from {brn_id} v{links_version} and the boards; {len(section_5)} markers left", "all")]
    log = "".join(f"| {v} | {d} | {a} | {c} | {x} |\n" for v, d, a, c, x in changelog)
    return f"""\
---
id: {id}
type: design
title: "{brn_title}: release design"
status: {status}
version: {version}
created: {created}
updated: {updated}
owner: "Example Owner"
authors: ["Example Owner", "claude-code"]
generated_by:
  tool: "claude-code"
  model: "{MODEL}"
  session: "{session}"
reviewed_by: []
approved_by: "{approved_by}"
approved_on: {approved_on or 'null'}
upstream:
{upstream}supersedes: []
superseded_by: {superseded_by or 'null'}
blocked_by: []
# --- design-specific ---
canvas: {json.dumps(canvas) if canvas else 'null'}
canvas_version: {json.dumps(canvas_version) if canvas_version else 'null'}
canvas_format: {canvas_format}
boards_root: {DESIGN}/{id}/boards/
considered: {list_text(list(considered))}
---

# {id} — {brn_title}: release design

## 1. Scope

{scope}

## 2. Boards

```yaml items
boards:
{''.join(brd_text(b) for b in boards)}```

## 3. Idea coverage

| Idea | Boards | Status |
|---|---|---|
{rows}
## 4. Canvas

- Canvas: {canvas or 'null'}
- Canvas version imported: {canvas_version or 'null'}
- Date of the import: {copy_date or 'not known'}
{'[NEEDS CLARIFICATION: canvas URL and version copied]' + chr(10) if canvas_marker else ''}
The boards in boards_root were imported from this canvas by the ui skill, or placed there and recorded as they
were. A new import means a new run, which amends this document. The brief is not recorded here.

## 5. Open questions

{chr(10).join('- ' + m for m in section_5) if section_5 else 'None.'}

## Change Log

| Version | Date | Author | Change | Items affected |
|---|---|---|---|---|
{log}"""


# The coverage tables of the shared fixture: every promoted idea of BRN-001 at version 1
COVER_DESIGNED = [("IDEA-01", "BRD-03", "designed"), ("IDEA-02", "BRD-01, BRD-02", "designed"),
                  ("IDEA-03", "BRD-04", "designed")]
COVER_A = COVER_DESIGNED + [("IDEA-04", "none", "not a screen"), ("IDEA-06", "none", "no board yet")]   # one marker
COVER_B = COVER_DESIGNED + [("IDEA-04", "none", "not a screen"), ("IDEA-06", "none", "not a screen")]   # no marker
MARKER_06 = "[NEEDS CLARIFICATION: IDEA-06 has no board yet]"

# State A: what writes-dsn writes (a draft with one marker). State B: every mapping confirmed, no marker.
DSN_A = dsn(standard_boards(), COVER_A, markers=[MARKER_06])
DSN_B = dsn(standard_boards(), COVER_B)
DSN_B_APPROVED = dsn(standard_boards(), COVER_B, status="approved", approved_by="Example Owner", approved_on="2026-10-08",
                     changelog=[(1, "2026-10-08", f"claude-code (session {FIXTURE_SESSION})",
                                 "Created from BRN-001 v1 and the boards; 0 markers left", "all"),
                                (1, "2026-10-08", "Example Owner", "Approved", "status")])


def with_state(text, **kw):
    """text with the DSN's id, status and similar lines changed (a small edit of a seeded DSN)."""
    for old, new in kw.values():
        text = replace(text, old, new)
    return text


def second_dsn(text, dsn_id="DSN-002"):
    """A copy of a seeded DSN under another number (its boards_root and heading move with it)."""
    return text.replace("DSN-001", dsn_id)


# --------------------------------------------------------------------------------------------------------
# Neighbouring documents: a PRD, ADRs, an ARCH, context documents and a story


def prd(version=1, requirements=None, dsn_version=None, status="approved", updated="2026-10-08"):
    requirements = requirements or [("FR-001", "The system shall record each shift with a start time and a stop time."),
                                    ("FR-002", "The system shall total the hours worked in each week.")]
    dsn_link = f"  - {{id: DSN-001, relation: informed_by, version: {dsn_version}, hash: null}}\n" if dsn_version else ""
    related = (f"\n## 8. Related documents\n\n- DSN-001, version {dsn_version}: the release design.\n"
               if dsn_version else "")
    frs = "".join(f'  - id: {i}\n    status: active\n    statement: "{s}"\n    priority: must\n    release: current\n'
                  f'    notes: ""\n' for i, s in requirements)
    log = (f"| 1 | 2026-10-06 | claude-code (session {FIXTURE_SESSION}) | Initial draft | all |\n"
           + (f"| {version} | {updated} | claude-code (session {FIXTURE_SESSION}) | Revised | all |\n" if version > 1 else ""))
    return f"""\
---
id: PRD-001
type: prd
title: "Shiftlog: record shifts and report weekly hours"
status: {status}
version: {version}
created: 2026-10-06
updated: {updated}
owner: "Example Owner"
authors: ["Example Owner", "claude-code"]
generated_by:
  tool: "claude-code"
  model: "{MODEL}"
  session: "{FIXTURE_SESSION}"
reviewed_by: []
approved_by: "Example Owner"
approved_on: 2026-10-07
upstream:
  - {{id: BRN-001, item: PRB-01, relation: derives, version: 1, hash: null}}
{dsn_link}supersedes: []
superseded_by: null
blocked_by: []
# --- prd-specific ---
target_release: "1.0"
stage: mvp
operating_context: internal
stakeholders: ["Example Owner"]
---

# PRD-001 — Shiftlog: record shifts and report weekly hours

## 1. Summary

Shiftlog records work shifts and totals the hours worked each week.

## 2. Functional requirements

```yaml items
functional_requirements:
{frs}```

## 3. Non-functional requirements

```yaml items
non_functional_requirements:
  - id: NFR-001
    status: active
    category: privacy
    statement: "Shift records stay on the user's own machine; nothing is sent over the network."
    priority: must
    release: current
```
{related}
## Change Log

| Version | Date | Author | Change | Items affected |
|---|---|---|---|---|
{log}"""


SCREEN_FRS = [
    ("FR-024", "The system shall let an administrator set the retention period on a settings screen"),
]
CANDIDATE_FRS = [(f"FR-{n:03d}", text) for n, text in zip(range(25, 38), [
    "The system shall show the weekly total on a summary screen.",
    "The system shall let a worker correct a shift on an edit screen.",
    "The system shall show a confirmation screen before a shift is deleted.",
    "The system shall list the open shifts on a dashboard screen.",
    "The system shall show a help screen that explains each command.",
    "The system shall show the month's overtime on a monthly screen.",
    "The system shall let a worker pick the week on a calendar screen.",
    "The system shall show an error screen when a shift cannot be saved.",
    "The system shall let a worker filter shifts on a search screen.",
    "The system shall show the export progress on a progress screen.",
    "The system shall let an administrator invite a user on an invitation screen.",
    "The system shall show a welcome screen the first time a worker starts the tool.",
    "The system shall let a worker print a report from a print screen.",
])]


def adr(id="ADR-009", title="Resolve a sync conflict by asking the user", consequence=None, version=1):
    consequence = consequence or "the CLI must print a sync conflict and offer to keep the local copy"
    return f"""\
---
id: {id}
type: adr
title: "{title}"
status: accepted
version: {version}
created: 2026-10-08
updated: 2026-10-08
owner: "Example Owner"
authors: ["Example Owner", "claude-code"]
generated_by:
  tool: "claude-code"
  model: "{MODEL}"
  session: "{FIXTURE_SESSION}"
reviewed_by: []
approved_by: "Example Owner"
approved_on: 2026-10-08
upstream:
  - {{id: PRD-001, item: FR-002, relation: informed_by, version: 1, hash: null}}
supersedes: []
superseded_by: null
blocked_by: []
# --- adr-specific ---
consulted: []
informed: []
---

# {id} — {title}

## Context and problem statement

A shift that was changed on two machines has two versions.

## Decision drivers

- PRD-001#FR-002: the hours worked each week must be right

## Considered options

1. Ask the user which copy to keep
2. Keep the newest copy

## Decision outcome

**Chosen option:** Ask the user which copy to keep, because a silent choice could drop hours.

### Consequences

- Good: no shift is lost without the user knowing.
- Consequence: {consequence}.

### Confirmation

A sync of two diverged copies stops and asks.

## Pros and cons of the options

### Ask the user which copy to keep
- Good, because no hours are lost silently.

### Keep the newest copy
- Bad, because an older but correct copy is lost.

## Status history

| Date | Status | Note |
|---|---|---|
| 2026-10-08 | proposed | |
| 2026-10-08 | accepted | Accepted by Example Owner |
"""


ADR_NO_SCREEN = (EXAMPLE / "adr/ADR-001.md").read_text()   # Python 3.12 for every component: names no screen
ADR_STAGED_2 = (EXAMPLE / "adr/ADR-002.md").read_text()
ARCH = (EXAMPLE / "arch/ARCH-001.md").read_text()
CONTEXT_DOCS = {name: (EXAMPLE / f"context/{name}.md").read_text() for name in ("index", "front-end", "ui-mockups")}

STORY_1 = f"""\
---
id: STORY-001
type: story
title: "List recorded shifts"
status: ready
version: 1
created: 2026-10-08
updated: 2026-10-08
owner: "Example Owner"
authors: ["Example Owner", "claude-code"]
generated_by:
  tool: "claude-code"
  model: "{MODEL}"
  session: "{FIXTURE_SESSION}"
reviewed_by: []
approved_by: ""
approved_on: null
upstream: []
supersedes: []
superseded_by: null
blocked_by: []
# --- story-specific ---
estimate: null
spec_mode: separate
---

# STORY-001 — List recorded shifts

## 1. User story

As a **shift worker**, I want **to list recorded shifts**, so that **my hours are right**.

## 2. Context

Part of PRD-001.

## 3. Scope

**In scope**
- List recorded shifts.

**Out of scope**
- Anything else.

## 4. Acceptance criteria

```yaml items
acceptance_criteria:
  - id: AC-01
    status: active
    name: "List recorded shifts"
    given:
      - "a recorded shift"
    when:
      - "I run the command"
    then:
      - "the shift is shown"
    upstream:
      - {{id: PRD-001, item: FR-001, relation: satisfies, version: 1, hash: null}}
```

## 5. Specification

GENERATED: the SPEC that specifies this story cites it.

## 6. Definition of Done

- [ ] Every AC is verified by at least one test that cites it (`STORY-001#AC-01`)

## 7. Open questions

None.

## Change Log

| Version | Date | Author | Change | AC affected |
|---|---|---|---|---|
| 1 | 2026-10-08 | claude-code (session {FIXTURE_SESSION}) | Initial draft | all |
"""


# --------------------------------------------------------------------------------------------------------
# Regex builders (JavaScript syntax). Q is an optional YAML quote.

Q = "[\"']?"
FM_LINE = r"(?:(?!---[ \t]*\n)[^\n]*\n)"
EOL = r"[ \t]*(?:#[^\n]*)?\n"
DATE = r"\d{4}-\d{2}-\d{2}"
UUID = r"[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}"


def esc(text):
    """Escapes text for a JavaScript RegExp source, with newlines written \\n so a pattern stays one line."""
    out = []
    for ch in text:
        if ch in "\\^$.|?*+()[]{}":
            out.append("\\" + ch)
        elif ch == "\n":
            out.append("\\n")
        elif ch == "\t":
            out.append("\\t")
        else:
            out.append(ch)
    return "".join(out)


def whole(text):
    """The file's whole content, anchored at both ends (SPEC-017 §9, VER-20: ^…$ without the m flag)."""
    return "^" + esc(text) + "$"


def fm_has(*conds):
    """Frontmatter holds a line (or lines) matching each condition, in any order."""
    return r"^---[ \t]*\n" + "".join(f"(?={FM_LINE}*?{c})" for c in conds)


def fm_field(key, value):
    return key + r":[ \t]*" + Q + value + Q + EOL


def fm_null(key):
    return key + r":[ \t]*(?:null|~)" + EOL


def fm_empty_list(key):
    return key + r":[ \t]*\[[ \t]*\]" + EOL


def nested(parent, key, value):
    """A key of a block mapping such as generated_by, or the same key in its flow form."""
    return (parent + r":(?:[ \t]*\n(?:[ \t]+[^\n]*\n)*?[ \t]+|[^\n]*[{,][ \t]*)" + key + r":[ \t]*" + Q + value
            + Q + r"[ \t]*[,}\n#]")


def link(doc, item=None, relation="derives", version=None):
    """A link record to doc, in flow form ({id: …}) or block form (id: … on its own lines)."""
    keys = [(k, v) for k, v in (("item", item), ("relation", relation), ("version", version)) if v is not None]
    flow = (r"\{(?=[^}\n]*\bid:[ \t]*" + Q + doc + r"\b)"
            + "".join(r"(?=[^}\n]*\b" + k + r":[ \t]*" + Q + str(v) + r"\b)" for k, v in keys) + r"[^}\n]*\}")
    block = (r"id:[ \t]*" + Q + doc + Q + r"[ \t]*\n"
             + "".join(r"(?=(?:[ \t]+(?!- )[^\n]*\n){0,6}?[ \t]+" + k + r":[ \t]*" + Q + str(v) + r"\b)"
                       for k, v in keys))
    return r"[ \t]*-[ \t]*(?:" + flow + "|" + block + ")"


def link_without_item(doc, relation="derives", version=None):
    """A flow-form link record to doc with no item (the template's form)."""
    return (r"[ \t]*-[ \t]*\{(?![^}\n]*\bitem:)(?=[^}\n]*\bid:[ \t]*" + Q + doc + r"\b)(?=[^}\n]*\brelation:[ \t]*" + Q
            + relation + r"\b)" + (r"(?=[^}\n]*\bversion:[ \t]*" + Q + str(version) + r"\b)" if version else "")
            + r"[^}\n]*\}")


def link_at_version(doc, version):
    """Any link record to doc at the version, in flow or block form."""
    return (r"[ \t]*-[ \t]*(?:\{(?=[^}\n]*\bid:[ \t]*" + Q + doc + r"\b)[^}\n]*\bversion:[ \t]*" + Q + str(version)
            + r"\b[^}\n]*\}|id:[ \t]*" + Q + doc + Q + r"[ \t]*\n(?:[ \t]+[^\n]*\n){0,6}?[ \t]+version:[ \t]*"
            + str(version) + r"\b)")


def section(title):
    """From a level-2 heading (numbered or not) to a match inside that section."""
    return r"\n##[ \t]+(?:\d+\.[ \t]+)?" + title + r"[^\n]*\n(?:(?!\n##[ \t])[\s\S])*?"


# A board item of the boards block: the lines after `- id: BRD-NN` up to the next item or the closing fence.
ITEM_LINE = r"(?:(?![ \t]*- id:[ \t]*" + Q + r"BRD-\d|```)[^\n]*\n)"


def item(brd_id, *conds):
    head = r"(?:^|\n)[ \t]*- id:[ \t]*" + Q + brd_id + Q + r"[ \t]*\n"
    return head + "".join(f"(?={ITEM_LINE}*?{c})" for c in conds)


def field_is(key, value):
    return r"[ \t]*" + key + r":[ \t]*" + Q + value + Q + EOL


def scalar_is(key, value):
    """A scalar field: null when value is None, else the value (a plain string, escaped here)."""
    if value is None:
        return r"[ \t]*" + key + r":[ \t]*(?:null|~)" + EOL
    return field_is(key, esc(value))


def list_is(key, values):
    """A list field in flow or block form: null, [] or exactly the values in order."""
    if values is None:
        return r"[ \t]*" + key + r":[ \t]*(?:null|~)" + EOL
    if not values:
        return r"[ \t]*" + key + r":[ \t]*\[[ \t]*\]" + EOL
    flow = r"\[[ \t]*" + r"[ \t]*,[ \t]*".join(Q + esc(v) + Q for v in values) + r"[ \t]*,?[ \t]*\]" + EOL
    block = (r"[ \t]*(?:#[^\n]*)?\n" + "".join(r"[ \t]*-[ \t]*" + Q + esc(v) + Q + EOL for v in values)
             + r"(?![ \t]*-[ \t])")
    return r"[ \t]*" + key + r":[ \t]*(?:" + flow + "|" + block + ")"


def brd_conds(b, sha=True):
    conds = [field_is("status", b.status), field_is("file", esc(b.file)), scalar_is("title", b.stem),
             scalar_is("flow", b.flow), scalar_is("surface", b.surface), list_is("ideas", b.ideas),
             list_is("answers", b.answers)]
    if sha:
        conds.append(field_is("sha256", b.sha))
    return conds


def cov_row(idea, boards, status):
    """A row of section 3: the Boards cell lists the BRD items in order, or none."""
    cell = "none" if not boards else r"[ \t,;&]+(?:and[ \t]+)?".join(boards)
    return (r"\n\|[ \t]*`?" + idea + r"`?[ \t]*\|[ \t]*`?" + cell + r"`?[ \t]*\|[ \t]*`?" + esc(status) + r"`?[ \t]*\|")


def log_row(version, author=r"claude-code \(session " + UUID + r"\)", change=r"[^\n]*"):
    return (r"\n\|[ \t]*" + str(version) + r"[ \t]*\|[ \t]*" + DATE + r"[ \t]*\|[ \t]*" + author + r"[ \t]*\|[ \t]*"
            + change + r"\|")


def considered_has(entry):
    """The considered list of the frontmatter holds the entry (flow or block form)."""
    e = esc(entry)
    return (r"considered:(?:[^\n]*" + Q + e + Q + r"[ \t,\]]|[ \t]*(?:#[^\n]*)?\n(?:[ \t]+-[^\n]*\n)*?[ \t]+-[ \t]*" + Q
            + e + Q + EOL + ")")


def block_line(label, rest):
    """A line of the reply's report block (BEH-17), bold or plain, in or out of a code block."""
    return r"(?:^|\n)[ \t>*-]*(?:\*\*)?" + label + r":(?:\*\*)?[ \t]*" + rest


OPENS_WITH_BLOCK = r"^\s*(?:```[^\n]*\n\s*)?(?:\*\*)?Design document:"
PARA_START = r"(?:^|\n[ \t]*\n)[ \t]*(?:\*\*|__)?Next step\b"
PARA_REST = r"(?:(?!\n[ \t]*\n)[\s\S])*?"
NEXT_STEP_LAST = PARA_START + PARA_REST + r"\s*$"
NEXT_STEP_IN_CODE = r"Next step" + PARA_REST + r"\n[ \t]*```[ \t]*\s*$"
PRD_CMD = r"/devforgeai:prd[` \t]+BRN-001\b"


def next_step_has(*conds):
    """The reply's last paragraph starts with Next step, holds each condition, and nothing follows it."""
    return PARA_START + "".join(f"(?={PARA_REST}{c})" for c in conds) + PARA_REST + r"\s*$"


def review_by_hand(dsn_id, version):
    """BEH-18's sentence: review them against DSN-001 version N by hand until their skills do it."""
    return (r"against[` \t]+" + dsn_id + r"[`,]?[ \t]+(?:at[ \t]+)?(?:version[ \t]+|v)" + str(version)
            + r"\b" + r"(?=[^\n]*\bby hand\b)")


# --------------------------------------------------------------------------------------------------------
# Cases and graders


@dataclass
class Grader:
    name: str
    type: str
    target: str = None      # "last_message" or a workspace path
    pattern: str = None
    match: str = "contains"
    flags: str = ""
    exists: bool = None
    min: int = None
    max: int = None
    witness: str = None     # text that, appended to the target, must make a not_contains grader fail
    input_match: str = None  # tool_used: the pattern (a YAML scalar, quotes included); the trigger pattern when None


@dataclass
class Case:
    name: str
    vers: list
    description: str
    prompt: str
    files: dict
    graders: list
    limits: tuple = WRITING_LIMITS
    tags: list = None
    invalid: dict = field(default_factory=dict)      # path -> True: the document is expected to fail its schema
    unparseable: set = field(default_factory=set)    # paths whose item blocks cannot be read at all
    boards: dict = field(default_factory=dict)       # DSN-NNN -> "ok" (default) or the first ERR its boards folder gives
    checks: dict = field(default_factory=dict)       # DSN-NNN -> ("current",) default | ("amend", [facts]) | ("invalid", [text])
    dirs: tuple = ()                                 # folders the scaffold makes even when it seeds no file in them
    runs: int = None                                 # runs of the case (case.yaml); the harness's default (3) when None


def rx(name, target, pattern, match="contains", flags="", witness=None):
    return Grader(name, "regex", target=target, pattern=pattern, match=match, flags=flags, witness=witness)


def present(name, path, exists=True):
    return Grader(name, "file_exists", target=path, exists=exists)


def skill_fired(name, fired):
    return Grader(name, "tool_used", min=1 if fired else 0, max=None if fired else 0)


def llm(name, body):
    """A grader the judge model reads; the final reply is what it sees (.claude/rules/evals.md)."""
    return Grader(name, "llm", pattern=body)


def unchanged(name, path, text):
    return rx(name, path, whole(text))


DSN1 = f"{DESIGN}/DSN-001.md"
DSN2 = f"{DESIGN}/DSN-002.md"
NO_STRAY = ["prd", "arch", "adr", "context", "story", "brainstorm", "epic", "spec", "policy", "ambiguities", "sprint"]


def nothing_written(prefix, *folders):
    """file_exists false: the run created no file under each folder of docs/specs/ (a `/**` path)."""
    return [present(f"{prefix}-no-file-under-{f.replace('/', '-')}", f"docs/specs/{f}/**", exists=False)
            for f in folders]


def no_dsn_written(prefix, dsn_id="DSN-001"):
    return [present(f"{prefix}-no-dsn-written", f"{DESIGN}/{dsn_id}.md", exists=False)]


def reply(name, pattern, flags="i", match="contains", witness=None):
    return rx(name, "last_message", pattern, match=match, flags=flags, witness=witness)


def boards_unchanged(prefix, contents, names=None, canvas=None, dsn_id="DSN-001"):
    """Whole-content graders for the boards folder: canvas.json and each board file are byte-identical."""
    names = list(contents) if names is None else names
    base = f"{DESIGN}/{dsn_id}/boards"
    g = [unchanged(f"{prefix}-canvas-json-unchanged", f"{base}/canvas.json", canvas or canvas_json(names))]
    g += [unchanged(f"{prefix}-board-{n.split('.')[0].lower()}-unchanged", f"{base}/{n}", contents[n]) for n in names]
    return g


def brd_graders(prefix, boards, path=DSN1, sha=True):
    g = []
    for b in boards:
        n = b.id[-2:]
        g.append(rx(f"{prefix}-brd-{n}-mapping", path, item(b.id, *brd_conds(b, sha=False))))
        if sha:
            g.append(rx(f"{prefix}-brd-{n}-sha256", path, item(b.id, field_is("sha256", b.sha))))
    return g


def idea_links(prefix, ideas, absent=(), version=1, path=DSN1):
    g = [rx(f"{prefix}-link-brn", path, fm_has(link_without_item("BRN-001", version=version)))]
    g += [rx(f"{prefix}-link-{i.lower()}", path, fm_has(link("BRN-001", item=i, version=version))) for i in ideas]
    g += [rx(f"{prefix}-no-link-{i.lower()}", path, fm_has(link("BRN-001", item=i)), match="not_contains") for i in absent]
    return g


def cover_rows(prefix, rows, path=DSN1):
    return [rx(f"{prefix}-row-{i.lower()}", path,
               section("Idea coverage") + cov_row(i, [x.strip() for x in boards.split(",")] if boards != "none" else [], st))
            for i, boards, st in rows]


def reply_block(prefix, dsn_id, version, status, kind, boards_cell, flows, no_idea, no_board, markers):
    """The block that opens a run's reply (BEH-17), line by line."""
    ln = lambda label, rest: reply(f"{prefix}-block-{label.lower().replace(' ', '-')}", block_line(label, rest))
    return [
        rx(f"{prefix}-block-opens-reply", "last_message", OPENS_WITH_BLOCK),
        reply(f"{prefix}-block-design-document", r"Design document:(?:\*\*)?[ \t]*" + dsn_id + r" \(v" + str(version) + ", "
              + esc(status) + "; " + kind + r"\)"),
        ln("Boards", boards_cell), ln("Flows", flows), ln("Boards with no idea", no_idea),
        ln("Ideas with no board", no_board), ln("Markers left", markers),
        reply(f"{prefix}-block-ok-line", r"(?:^|\n)[ \t>*-]*OK " + esc(f"{DESIGN}/{dsn_id}.md") + r"[ \t]*(?:\n|$)", flags=""),
    ]


# --------------------------------------------------------------------------------------------------------
# Wording the stop cases' replies are graded on (flags i)

APOS = "['’]"
NO_FETCH = r"(?:\bnever\b|\bnot\b|n" + APOS + r"t)[^\n]{0,60}\bfetch|\bfetch\w*[^\n]{0,60}\b(?:never|not)\b|\bno fetch"
COPY_AGAIN = (r"\bcop(?:y|ied|ying)\b[^\n]{0,80}\bagain\b|\bre-?cop(?:y|ied|ying)\b|\bagain\b[^\n]{0,60}\bcop(?:y|ied)")
BRAINSTORM_CMD = r"/devforgeai:brainstorm"
NOT_ACCEPTED = (r"\bpaths?\b[^\n]{0,80}(?:not accepted|aren" + APOS + r"t accepted|isn" + APOS + r"t accepted|never|"
                r"not (?:taken|allowed|supported)|refus|can" + APOS + r"t|cannot)|(?:never|not|doesn" + APOS + r"t|don"
                + APOS + r"t|won" + APOS + r"t|no)[^\n]{0,60}\bpaths?\b")

# The reply says the session has no Artifact tool (ERR-19, BEH-05): it names the tool and its absence
# (a contraction has no word boundary before its n: "isn't" is matched by n't\b, never by \bn't)
NO_ARTIFACT = (r"\bno Artifact\b|\bArtifact tool\b[^\n]{0,40}(?:\bnot\b|n" + APOS + r"t\b|\bunavailable\b|\bmissing\b|\babsent\b)|"
               r"\b(?:without|lacks?|missing|has no|have no|don" + APOS + r"t have|do not have|doesn" + APOS
               + r"t have)\b[^\n]{0,30}\bArtifact\b")
# The canvas was not checked (BEH-05 routes A and D; ERR-17 v2)
CANVAS_NOT_CHECKED = (r"(?:\bnot|n" + APOS + r"t) (?:been |yet |re-?)*(?:checked|verified|looked at)\b|\bcould(?:n" + APOS
                      + r"t| not) (?:be )?(?:check|see|verify|read|reach)\w*|\bunchecked\b|\bno Artifact tool\b|"
                      r"\bwithout (?:the )?Artifact tool\b")
COPY_RECORDED_AS_IS = (r"\bas[- ]is\b|\bas it is\b|\brecorded\b[^\n]{0,60}\bcopy\b|\bcopy\b[^\n]{0,80}\b(?:recorded|record)\b")
IMPORT_OR_COPY_AGAIN = (r"\b(?:re-?)?import\w*\b[^\n]{0,80}\bagain\b|\bre-?import\b|\bcop(?:y|ied|ying)\b[^\n]{0,80}\bagain\b|"
                        r"\bre-?cop(?:y|ied|ying)\b|\bagain\b[^\n]{0,60}\b(?:import|cop(?:y|ied))")
# A drawing of a screen in a reply (VER-39, VER-41): a run of box-drawing or block characters, or a +---+ rule
NO_DRAWING = r"[\u2500-\u257f\u2580-\u259f]{3}|\+-{3,}\+"
DESIGN_MATCH = r"""'"skill"\s*:\s*"/?(?:[\w-]+:)?design"'"""
BRIEF_CLOSING = "Give me 3 distinctly different directions of the key screen first, with a one-line tradeoff under each."

UI = "ui"
SHARED_PROMPT = """\
Record the UI design for BRN-001. The canvas is https://claude.ai/artifact/EXAMPLE, version 17-example. Home and Report
are web screens in the flow report-and-home, in that order; List and Add are terminal screens in the flow shifts, in that
order. Home shows IDEA-02; List shows IDEA-02; Add shows IDEA-01; Report shows IDEA-03. IDEA-04 names no screen. IDEA-06
has no board yet. Proceed without questions."""
PROMPT_SETTINGS = """\
Record the UI design for BRN-001. The canvas is https://claude.ai/artifact/EXAMPLE, version 17-example. Home, Report and
Settings are web screens in the flow report-and-home, in that order; List and Add are terminal screens in the flow
shifts, in that order. Home shows IDEA-02; List shows IDEA-02; Add shows IDEA-01; Report shows IDEA-03; Settings shows
IDEA-06. IDEA-04 names no screen. Proceed without questions."""
PROMPT_DESIGN = "Design the UI for BRN-001. Proceed without questions."
PROMPT_UNCONFIRMED = "Record the UI design for BRN-001. Proceed without questions."
APPROVAL_WORDS = "I'm Example Owner, and I approve DSN-001."
CANVAS_NOW = "Update the UI design for BRN-001. I copied the boards again from the canvas, version {v}."

SHARED = {BRN_PATH: BRN, **boards_files()}
BOARDS_5 = dict(BOARD_CONTENT)
FIVE = BOARD_ORDER + ["Settings.dc.html"]
SETTINGS_BRD = Brd("BRD-05", "Settings.dc.html", "report-and-home", "web", ["IDEA-06"], sha=digest(SETTINGS))
DSN_5 = dsn(standard_boards() + [SETTINGS_BRD], COVER_DESIGNED + [("IDEA-04", "none", "not a screen"),
                                                                ("IDEA-06", "BRD-05", "designed")])


# --------------------------------------------------------------------------------------------------------
# VER-01 to VER-09: the create run and the boards problems


def writes_dsn():
    p = "ver01"
    b = standard_boards()
    g = [present("ver01-dsn-written", DSN1),
         rx("ver01-id-and-type", DSN1, fm_has(fm_field("id", "DSN-001"), fm_field("type", "design"))),
         rx("ver01-status-draft", DSN1, fm_has(fm_field("status", "draft"))),
         rx("ver01-version-1", DSN1, fm_has(r"version:[ \t]*1" + EOL)),
         rx("ver01-approval-empty", DSN1, fm_has(r"approved_by:[ \t]*(?:\"\"|'')" + EOL, fm_null("approved_on"))),
         rx("ver01-owner", DSN1, fm_has(fm_field("owner", "Example Owner"))),
         rx("ver01-title", DSN1, fm_has(fm_field("title", esc("Shiftlog: record shifts: release design")))),
         rx("ver01-canvas", DSN1, fm_has(fm_field("canvas", esc(CANVAS_URL)))),
         rx("ver01-canvas-version", DSN1, fm_has(fm_field("canvas_version", esc(CANVAS_VERSION)))),
         rx("ver01-canvas-format-3", DSN1, fm_has(r"canvas_format:[ \t]*3" + EOL)),
         rx("ver01-boards-root", DSN1, fm_has(fm_field("boards_root", esc(f"{DESIGN}/DSN-001/boards/")))),
         rx("ver01-generated-by", DSN1, fm_has(nested("generated_by", "tool", "claude-code"),
                                               nested("generated_by", "model", r"[A-Za-z0-9][^\"'\n,}]*"),
                                               nested("generated_by", "session", UUID))),
         rx("ver01-considered-empty", DSN1, fm_has(fm_empty_list("considered"))),
         rx("ver01-reviewed-by-empty", DSN1, fm_has(fm_empty_list("reviewed_by")))]
    g += brd_graders(p, b)
    g.append(rx("ver01-items-in-canvas-order", DSN1,
                r"\bfile:[ \t]*" + Q + r"Home\.dc\.html[\s\S]*?\bfile:[ \t]*" + Q + r"List\.dc\.html[\s\S]*?\bfile:[ \t]*" + Q
                + r"Add\.dc\.html[\s\S]*?\bfile:[ \t]*" + Q + r"Report\.dc\.html"))
    g.append(rx("ver01-no-fifth-item", DSN1, r"\bid:[ \t]*" + Q + "BRD-05", match="not_contains",
                witness="\n  - id: BRD-05\n"))
    g += idea_links(p, ["IDEA-01", "IDEA-02", "IDEA-03"], absent=["IDEA-04", "IDEA-05", "IDEA-06"])
    g += [rx("ver01-change-log-row", DSN1, log_row(1)),
          rx("ver01-one-change-log-row", DSN1, r"claude-code \(session[\s\S]*claude-code \(session", match="not_contains",
             witness="| 1 | 2026-10-10 | claude-code (session x) | Again | all |\n")]
    # the findings: the copy was recorded as it is and the canvas was not checked, because the session has no Artifact tool
    g += [reply("ver01-says-copy-recorded-as-it-is", COPY_RECORDED_AS_IS),
          reply("ver01-says-no-artifact-tool-in-this-session", NO_ARTIFACT),
          reply("ver01-says-canvas-not-checked", CANVAS_NOT_CHECKED)]
    return g


def coverage_and_report():
    p = "ver02"
    g = [present("ver02-dsn-written", DSN1)]
    g.append(rx("ver02-section-3-header-and-five-rows", DSN1,
                section("Idea coverage") + r"\n\|[ \t]*Idea[ \t]*\|[ \t]*Boards[ \t]*\|[ \t]*Status[ \t]*\|[ \t]*\n"
                r"\|[-| :\t]+\|[ \t]*(?:\n\|[^\n]*){5}(?=\n(?!\|)|$)"))
    g += cover_rows(p, [("IDEA-01", "BRD-03", "designed"), ("IDEA-02", "BRD-01, BRD-02", "designed"),
                        ("IDEA-03", "BRD-04", "designed"), ("IDEA-04", "none", "not a screen"),
                        ("IDEA-06", "none", "no board yet")])
    g.append(rx("ver02-no-idea-05-anywhere", DSN1, r"IDEA-05", match="not_contains", witness="\nIDEA-05\n"))
    g += [rx("ver02-section-5-marker-names-idea-06", DSN1,
             section("Open questions") + r"\[NEEDS CLARIFICATION:[^\]\n]*IDEA-06"),
          rx("ver02-one-marker", DSN1, r"\[NEEDS CLARIFICATION[\s\S]*\[NEEDS CLARIFICATION", match="not_contains",
             witness="\n- [NEEDS CLARIFICATION: x]\n")]
    g += reply_block(p, "DSN-001", 1, "draft", "new", esc(f"{DESIGN}/DSN-001/boards/") + r"[^\n]*?\b4\b[^\n]*?\bversion "
                     + esc(CANVAS_VERSION) + r"\b", r"report and home \(2\), shifts \(2\)", r"none\b", r"IDEA-06\b",
                     r"DSN-001: 1\b")
    g += [rx("ver02-next-step-is-last", "last_message", NEXT_STEP_LAST),
          rx("ver02-next-step-outside-code", "last_message", NEXT_STEP_IN_CODE, match="not_contains", witness="```"),
          rx("ver02-next-step-names-prd", "last_message",
             next_step_has(PRD_CMD, r"\bsection 8\b", r"\bby hand\b", r"\bDSN-001\b"), flags="i")]
    return g


def unconfirmed_stays_null():
    p = "ver03"
    g = [present("ver03-dsn-written", DSN1), rx("ver03-status-draft", DSN1, fm_has(fm_field("status", "draft")))]
    for n, f in enumerate(BOARD_ORDER, start=1):
        b = Brd(f"BRD-0{n}", f, sha=digest(BOARDS[f]))
        g.append(rx(f"ver03-brd-0{n}-null-mapping", DSN1, item(b.id, field_is("file", esc(f)), scalar_is("title", b.stem),
                                                                scalar_is("flow", None), scalar_is("surface", None),
                                                                list_is("ideas", None), list_is("answers", []),
                                                                r"[ \t]*notes:[^\n]*\[NEEDS CLARIFICATION")))
    g += [rx("ver03-canvas-null", DSN1, fm_has(fm_null("canvas"), fm_null("canvas_version"))),
          rx("ver03-section-4-marker", DSN1, section("Canvas") + r"\[NEEDS CLARIFICATION")]
    g += cover_rows(p, [(i, "none", "no board yet") for i in ("IDEA-01", "IDEA-02", "IDEA-03", "IDEA-04", "IDEA-06")])
    g += [rx("ver03-no-not-a-screen", DSN1, section("Idea coverage") + r"\|[ \t]*not a screen[ \t]*\|", match="not_contains"),
          reply("ver03-flows-unconfirmed", block_line("Flows", r"unconfirmed \(4\)")),
          reply("ver03-markers-left-not-none", block_line("Markers left", r"(?!none\b)\S"))]
    return g


def no_boards_stops():
    # ERR-19: the prompt names a canvas URL, no copy is in the folder and the session has no Artifact tool
    return no_dsn_written("ver04") + nothing_written("ver04", "design") + [
        reply("ver04-says-no-artifact-tool", NO_ARTIFACT),
        reply("ver04-names-boards-folder", esc(f"{DESIGN}/DSN-001/boards/"), flags=""),
        reply("ver04-names-canvas-json", r"canvas\.json"),
        reply("ver04-says-a-copy-placed-by-hand-is-recorded-when-run-again",
              r"\b(?:by hand|yourself|manually|place[sd]?|put|cop(?:y|ied))\b[^\n]{0,160}\b(?:run|runs|rerun|re-run|ran)\b[^\n]{0,40}\bagain\b|"
              r"\bagain\b[^\n]{0,160}\b(?:record\w*)\b|\b(?:record\w*)\b[^\n]{0,160}\b(?:run|runs|rerun|re-run)\b[^\n]{0,40}\bagain\b|"
              r"\brecord\w*\b[^\n]{0,160}\b(?:next|following|later)\s+(?:run|time|session)\b|"
              r"\b(?:next|following|later)\s+(?:run|time|session)\b[^\n]{0,160}\brecord\w*\b"),
        rx("ver04-no-drawing", "last_message", NO_DRAWING, match="not_contains", witness="\n┌──────┐\n│ Home │\n└──────┘\n")]


def boards_without_canvas_json():
    # ERR-03: the folder holds the board files and no canvas.json
    return no_dsn_written("ver04") + nothing_written("ver04", "design") + [
        reply("ver04-names-boards-folder", esc(f"{DESIGN}/DSN-001/boards/"), flags=""),
        reply("ver04-names-canvas-json", r"canvas\.json"),
        reply("ver04-says-the-folder-must-hold-canvas-json-and-the-board-files",
              r"(?=[\s\S]*\bcanvas\.json\b)(?=[\s\S]*\bboard files?\b)")]


def boards_at_wrong_number():
    return [unchanged("ver05-dsn-001-unchanged", DSN1, DSN1_OTHER_BRN),
            present("ver05-no-dsn-002", DSN2, exists=False),
            present("ver05-no-file-under-dsn-002-folder", f"{DESIGN}/DSN-002/**", exists=False),
            # the skill says the new DSN's ID is the one `next` prints (DSN-002): "next free number" or "the new DSN"
            reply("ver05-next-free-number", r"\b(?:new|next)\b[^\n]{0,80}\bDSN-002\b|\bDSN-002\b[^\n]{0,80}\b(?:new|next)\b|"
                  r"\bDSN-002\b[^\n]{0,60}\b(?:would be|will be|is)\b"),
            reply("ver05-copy-into-dsn-002-boards", esc(f"{DESIGN}/DSN-002/boards/"), flags=""),
            reply("ver05-says-no-artifact-tool", NO_ARTIFACT)]


def canvas_unreadable():
    return no_dsn_written("ver06") + nothing_written("ver06", "design") + [
        reply("ver06-cannot-read-canvas-json", r"canvas\.json[^\n]{0,160}(?:can" + APOS + r"?t|cannot|can not|unable|could(?:n"
              + APOS + r"t| not)|not (?:be )?(?:read|readable|valid|parsed|parseable)|unreadable|damaged|invalid|corrupt)"
              r"|(?:cannot|can" + APOS + r"t|unable to|could not) (?:be )?(?:read|parse)[^\n]{0,100}canvas\.json"),
        reply("ver06-asks-to-import-or-copy-again", IMPORT_OR_COPY_AGAIN)]


def unknown_canvas_format():
    return no_dsn_written("ver07") + nothing_written("ver07", "design") + [
        reply("ver07-names-version-4", r"\b(?:v|version)[ ]?4\b|\b4\b[^\n]{0,40}\b(?:version|format)\b|\b(?:version|format)\b[^\n]{0,60}\b4\b"),
        reply("ver07-names-supported-version-3", r"\b3\b[^\n]{0,60}\b(?:supported|only)\b|\b(?:supported|only)\b[^\n]{0,60}\b3\b"),
        reply("ver07-says-not-documented", r"\b(?:not|isn" + APOS + r"t|is not|un)[ -]?documented\b")]


def board_file_absent():
    return no_dsn_written("ver08") + nothing_written("ver08", "design") + [
        reply("ver08-names-gone-board", r"Gone\.dc\.html"), reply("ver08-names-outside-board", r"outside\.dc\.html")]


def too_many_boards():
    return no_dsn_written("ver09") + nothing_written("ver09", "design") + [
        reply("ver09-gives-the-count-100", r"\b100\b"), reply("ver09-gives-the-limit-99", r"\b99\b")]


# --------------------------------------------------------------------------------------------------------
# VER-10 to VER-12: the amend run

def prd_cites_dsn(version):
    """A line that names PRD-001 as citing DSN-001 at the version (the block's lines name neither)."""
    return (r"(?:^|\n)(?=[^\n]*\bPRD-001\b)(?=[^\n]*\bDSN-001\b)[^\n]*\b(?:version[ \t]*|v)" + str(version) + r"\b")


PRE_CHECK_ORDER = (r"dsn_check\.py[\"']?\s+boards\s+DSN-001[\s\S]*?dsn_check\.py[\"']?\s+check\s+--before-amend\s+DSN-001")
OLD_ROWS_B_APPROVED = [r for r in DSN_B_APPROVED.splitlines(True) if r.startswith("| 1 |")]


def amend_changed_board():
    b = standard_boards(report=REPORT_CHANGED)[:4]
    p = "ver10"
    g = [rx("ver10-version-2", DSN1, fm_has(r"version:[ \t]*2" + EOL)),
         rx("ver10-status-in-review", DSN1, fm_has(fm_field("status", "in-review"))),
         rx("ver10-approval-cleared", DSN1, fm_has(r"approved_by:[ \t]*(?:\"\"|'')" + EOL, fm_null("approved_on")))]
    g += brd_graders(p, b)
    g += [rx("ver10-brd-05-settings", DSN1, item("BRD-05", *brd_conds(SETTINGS_BRD))),
          rx("ver10-row-idea-06-designed", DSN1, section("Idea coverage") + cov_row("IDEA-06", ["BRD-05"], "designed")),
          rx("ver10-link-idea-06", DSN1, fm_has(link("BRN-001", item="IDEA-06", version=1)))]
    g += [rx("ver10-change-log-keeps-version-1-rows", DSN1, esc("".join(OLD_ROWS_B_APPROVED))),
          rx("ver10-change-log-version-2-row", DSN1, log_row(2))]
    g += [unchanged("ver10-prd-001-unchanged", "docs/specs/prd/PRD-001.md", PRD_CITING_1),
          unchanged("ver10-brn-001-unchanged", BRN_PATH, BRN)]
    g += boards_unchanged("ver10", BOARDS_AMEND_CHANGED, names=FIVE)
    g += [reply("ver10-pre-check-order", PRE_CHECK_ORDER, flags=""),
          reply("ver10-fact-report-changed", r"fact: board Report\.dc\.html: changed", flags=""),
          reply("ver10-fact-settings-new", r"fact: board Settings\.dc\.html: new", flags=""),
          reply("ver10-says-amended", r"Design document:(?:\*\*)?[ \t]*DSN-001 \(v2, in-review; amended\)", flags=""),
          reply("ver10-names-prd-citing-version-1", prd_cites_dsn(1)),
          rx("ver10-next-step", "last_message", next_step_has(PRD_CMD, review_by_hand("DSN-001", 2), r"\bPRD-001\b"),
             flags="i"),
          rx("ver10-next-step-is-last", "last_message", NEXT_STEP_LAST)]
    return g


def amend_removed_board():
    b = standard_boards()
    keep = [x for x in b if x.id != "BRD-03"]
    g = [rx("ver11-version-2", DSN1, fm_has(r"version:[ \t]*2" + EOL))]
    g += brd_graders("ver11", keep)
    g += [rx("ver11-brd-03-deprecated", DSN1, item("BRD-03", field_is("status", "deprecated"), field_is("file", "\"?Add\\.dc\\.html\"?"))),
          rx("ver11-no-item-renumbered", DSN1, r"\bid:[ \t]*" + Q + "BRD-05", match="not_contains"),
          rx("ver11-row-idea-01-no-board-yet", DSN1, section("Idea coverage") + cov_row("IDEA-01", [], "no board yet")),
          rx("ver11-marker-names-idea-01", DSN1, r"\[NEEDS CLARIFICATION:[^\]\n]*IDEA-01"),
          reply("ver11-boards-line-counts-3", block_line("Boards", r"[^\n]*(?:\b3\b)"), flags=""),
          reply("ver11-says-amended", r"Design document:(?:\*\*)?[ \t]*DSN-001 \(v2, draft; amended\)", flags="")]
    return g


def amend_brn_moved():
    b = standard_boards()
    g = [rx("ver12-version-2-once", DSN1, fm_has(r"version:[ \t]*2" + EOL)),
         rx("ver12-no-link-at-version-1", DSN1, fm_has(link_at_version("BRN-001", 1)), match="not_contains"),
         rx("ver12-link-brn-version-2", DSN1, fm_has(link_without_item("BRN-001", version=2))),
         rx("ver12-link-idea-02-kept", DSN1, fm_has(link("BRN-001", item="IDEA-02", version=2)))]
    g += brd_graders("ver12", b, sha=False)
    g += [rx("ver12-row-idea-07", DSN1, section("Idea coverage") + cov_row("IDEA-07", [], "no board yet")),
          rx("ver12-row-idea-02-withdrawn", DSN1, section("Idea coverage") + cov_row("IDEA-02", ["BRD-01", "BRD-02"], "withdrawn")),
          rx("ver12-marker-names-idea-07", DSN1, section("Open questions") + r"\[NEEDS CLARIFICATION:[^\]\n]*IDEA-07"),
          rx("ver12-no-item-deprecated", DSN1, r"status:[ \t]*" + Q + "deprecated", match="not_contains"),
          rx("ver12-change-log-says-links-moved", DSN1,
             r"\n\|[ \t]*2[ \t]*\|[^\n]*(?:\b[Ll]inks?\b[^\n]*\bmov|\bmov\w*\b[^\n]*\blinks?\b)", flags="")]
    return g


# --------------------------------------------------------------------------------------------------------
# VER-13 to VER-21: the gates, the problems with the BRN, approval in the run that writes


def unknown_brn():
    return no_dsn_written("ver13") + nothing_written("ver13", "design") + [reply("ver13-lists-brn-001", r"BRN-001")]


def path_refused():
    return no_dsn_written("ver14") + nothing_written("ver14", "design") + [
        reply("ver14-says-paths-are-not-accepted", NOT_ACCEPTED),
        # a brainstorm ID is the BRN ID; a question or a request, not the statement that the skill takes one
        reply("ver14-asks-for-the-brn-id", r"\b(?:BRN|brainstorm)\b[^\n]*\?|\bwhich\b[^\n]{0,80}\bID\b|"
              r"\b(?:give|provide|tell|name|send|pick|choose|say|supply)\b[^\n]{0,60}\b(?:BRN|brainstorm)\b")]


def unconverged_brn():
    return no_dsn_written("ver15") + nothing_written("ver15", "design") + [
        reply("ver15-warns-ideas-may-not-be-decided",
              r"\bideas?\b[^\n]{0,100}\b(?:may|might|could)\b[^\n]{0,60}\bnot\b[^\n]{0,40}\b(?:decided|settled|final|confirmed|converged)\b"
              r"|(?:\bnot|n" + APOS + r"t) (?:yet |been )?(?:converged|decided|settled|final)\b|\bundecided\b|\bnot all (?:of )?the ideas\b"
              r"|\bsome ideas?\b[^\n]{0,60}\b(?:may|might|could)\b[^\n]{0,20}\b(?:still )?(?:change|move|be open|be undecided)\b")]


def no_promoted_idea():
    return no_dsn_written("ver16") + nothing_written("ver16", "design") + [reply("ver16-points-to-brainstorm", BRAINSTORM_CMD)]


def malformed_brn():
    return no_dsn_written("ver17") + nothing_written("ver17", "design") + [
        reply("ver17-names-the-ideas-block", r"\bideas\b[^\n]{0,40}\bblock\b|\bblock\b[^\n]{0,40}\bideas\b"), reply("ver17-names-the-brn-path", esc(BRN_PATH), flags=""),
        unchanged("ver17-brn-001-unchanged", BRN_PATH, BRN_MALFORMED)]


def two_dsns_cite():
    return [unchanged("ver18-dsn-001-unchanged", DSN1, DSN_B), unchanged("ver18-dsn-002-unchanged", DSN2, DSN_B_2),
            present("ver18-no-dsn-003", f"{DESIGN}/DSN-003.md", exists=False),
            reply("ver18-lists-dsn-001", r"DSN-001"), reply("ver18-lists-dsn-002", r"DSN-002"),
            reply("ver18-asks-which-to-amend", r"\bwhich\b[^\n]{0,100}\?|\?[^\n]{0,100}\bwhich\b")]


# A line that says the marker remains or blocks the approval: not the block's own `Markers left:` line, which a run
# that says nothing about the marker prints too
MARKER_REMAINS = (r"(?:^|\n)(?![ \t>*-]*(?:\*\*)?Markers left:)(?=[^\n]*\bmarkers?\b)"
                  r"(?=[^\n]*\b(?:remains?|remaining|still|blocks?|blocked|waits?|waiting|until|unresolved|open)\b)[^\n]+")


def approve_blocked_by_marker():
    return [present("ver19-dsn-written", DSN1), rx("ver19-status-stays-draft", DSN1, fm_has(fm_field("status", "draft"))),
            rx("ver19-approved-by-empty", DSN1, fm_has(r"approved_by:[ \t]*(?:\"\"|'')" + EOL)),
            rx("ver19-approved-on-null", DSN1, fm_has(fm_null("approved_on"))),
            rx("ver19-no-approved-row", DSN1, r"\n\|[^\n]*\|[ \t]*Approved\.?[ \t]*\|", match="not_contains"),
            rx("ver19-marker-for-idea-06-remains", DSN1, r"\[NEEDS CLARIFICATION:[^\]\n]*IDEA-06"),
            reply("ver19-reply-says-the-marker-remains", MARKER_REMAINS)]


def approve_on_explicit_words():
    return [present("ver19-dsn-written", DSN1), rx("ver19-status-approved", DSN1, fm_has(fm_field("status", "approved"))),
            rx("ver19-approved-by", DSN1, fm_has(fm_field("approved_by", "Example Owner"))),
            rx("ver19-approved-on-a-date", DSN1, fm_has(fm_field("approved_on", DATE))),
            rx("ver19-version-1", DSN1, fm_has(r"version:[ \t]*1" + EOL)),
            rx("ver19-approved-row", DSN1, r"\n\|[ \t]*1[ \t]*\|[ \t]*" + DATE + r"[ \t]*\|[ \t]*Example Owner[ \t]*\|[ \t]*Approved\.?[ \t]*\|"),
            rx("ver19-no-marker-left", DSN1, r"\[NEEDS CLARIFICATION", match="not_contains")]


def no_approval_without_words():
    return [present("ver19-dsn-written", DSN1), rx("ver19-status-stays-draft", DSN1, fm_has(fm_field("status", "draft"))),
            rx("ver19-approved-by-empty", DSN1, fm_has(r"approved_by:[ \t]*(?:\"\"|'')" + EOL)),
            rx("ver19-approved-on-null", DSN1, fm_has(fm_null("approved_on"))),
            rx("ver19-no-approved-row", DSN1, r"\n\|[^\n]*\|[ \t]*Approved\.?[ \t]*\|", match="not_contains")]


NEIGHBOURS = {
    "docs/specs/prd/PRD-001.md": prd(), "docs/specs/arch/ARCH-001.md": ARCH, "docs/specs/adr/ADR-001.md": ADR_NO_SCREEN,
    "docs/specs/adr/ADR-002.md": ADR_STAGED_2, "docs/specs/story/STORY-001.md": STORY_1,
    **{f"docs/specs/context/{n}.md": t for n, t in CONTEXT_DOCS.items()}}


def neighbours_unchanged():
    g = [present("ver20-dsn-001-written", DSN1)]
    g += [unchanged(f"ver20-{Path(p).stem.lower()}-unchanged", p, t) for p, t in sorted(NEIGHBOURS.items())]
    g.append(unchanged("ver20-brn-001-unchanged", BRN_PATH, BRN))
    g += boards_unchanged("ver20", BOARDS)
    g += [present("ver20-no-dsn-002", DSN2, exists=False), present("ver20-no-file-under-dsn-001-folder", f"{DESIGN}/DSN-001/**", exists=False)]
    g += nothing_written("ver20", *NO_STRAY)
    return g


def lists_brns():
    return [unchanged("ver21-dsn-001-unchanged", DSN1, DSN_B), present("ver21-no-dsn-002", DSN2, exists=False),
            reply("ver21-lists-brn-001-with-title", r"BRN-001[^\n]*Shiftlog: record shifts|Shiftlog: record shifts[^\n]*BRN-001"),
            reply("ver21-lists-brn-002-with-title", r"BRN-002[^\n]*Shiftlog: remind about open shifts|Shiftlog: remind about open shifts[^\n]*BRN-002"),
            reply("ver21-brn-001-is-cited-by-dsn-001", r"BRN-001[^\n]*\bDSN-001\b|\bDSN-001\b[^\n]*BRN-001"),
            reply("ver21-brn-002-is-cited-by-none", r"BRN-002[^\n]*\b(?:none|no DSN|not (?:yet )?cited|uncited)\b|\b(?:none|no DSN)\b[^\n]*BRN-002"),
            reply("ver21-asks-which-to-use", r"\bwhich\b[^\n]{0,100}\?|\?[^\n]{0,100}\bwhich\b")]


def no_brainstorm_yet():
    return nothing_written("ver21", "design") + no_dsn_written("ver21") + [
        reply("ver21-says-no-brainstorm-exists", r"\bno (?:brainstorm|BRN)\b[^\n]{0,60}|\bnot? brainstorm\b|brainstorm[^\n]{0,40}\b(?:exists?|yet|found)\b"),
        reply("ver21-points-to-brainstorm", BRAINSTORM_CMD)]


def no_brn_with_promoted_idea():
    return nothing_written("ver21", "design") + no_dsn_written("ver21") + [
        reply("ver21-lists-brn-001-with-status", r"BRN-001[^\n]*\bdraft\b|\bdraft\b[^\n]*BRN-001"),
        reply("ver21-says-none-has-a-promoted-idea", r"\b(?:no|none|not)\b[^\n]{0,80}\bpromoted\b|\bpromoted\b[^\n]{0,80}\b(?:none|no|not)\b"),
        reply("ver21-points-to-brainstorm", BRAINSTORM_CMD)]


# --------------------------------------------------------------------------------------------------------
# VER-30 to VER-38: the amend triggers, approval-only runs, candidates

NOBODY_CITES = (r"\b(?:no|none of the|not any)\b[^\n.]{0,40}\b(?:documents?|PRDs?|docs)\b[^\n.]{0,60}\bcit\w+|"
                r"\bnothing\b[^\n.]{0,40}\bcit\w+|\bnot cited by (?:any|a)\b|\bno one cites\b|\bnone\b[^\n.]{0,40}\bcit\w+")
CURRENT = r"\bcurrent\b|\bup to date\b|\bnothing to (?:change|update|amend)\b"
DECLINE_PROMPT = ("I decline PRD-001 FR-025, FR-026, FR-027, FR-028, FR-029 and FR-030: none of them needs a board.")

B_REPORT = standard_boards(report=REPORT_CHANGED)
B_FINAL_30 = B_REPORT                                # VER-30: Report's digest is the only difference from the seed


def amend_draft_revision():
    b = B_REPORT
    g = [rx("ver30-version-2", DSN1, fm_has(r"version:[ \t]*2" + EOL)),
         rx("ver30-status-stays-draft", DSN1, fm_has(fm_field("status", "draft"))),
         rx("ver30-canvas-version-is-the-new-one", DSN1, fm_has(fm_field("canvas_version", "1791580000-c3d4")))]
    g += brd_graders("ver30", b)
    g += [rx("ver30-change-log-keeps-version-1-row", DSN1, esc(DSN_A.splitlines(True)[-1])),
          rx("ver30-change-log-version-2-row", DSN1, log_row(2)),
          reply("ver30-says-amended", r"Design document:(?:\*\*)?[ \t]*DSN-001 \(v2, draft; amended\)", flags=""),
          reply("ver30-boards-line-ends-with-the-new-version", block_line("Boards", r"[^\n]*\bversion 1791580000-c3d4[ \t]*(?:\n|$)"), flags=""),
          reply("ver30-says-no-document-cites-dsn-001", NOBODY_CITES),
          rx("ver30-next-step", "last_message", next_step_has(PRD_CMD), flags="i"),
          rx("ver30-next-step-is-last", "last_message", NEXT_STEP_LAST)]
    return g


def amend_without_new_version():
    return [rx("ver30-canvas-version-null", DSN1, fm_has(fm_null("canvas_version"))),
            rx("ver30-canvas-version-never-the-old-value", DSN1, fm_has(fm_field("canvas_version", esc(CANVAS_VERSION))),
               match="not_contains"),
            rx("ver30-section-4-marker", DSN1, section("Canvas") + r"\[NEEDS CLARIFICATION"),
            rx("ver30-version-2", DSN1, fm_has(r"version:[ \t]*2" + EOL)),
            reply("ver30-boards-line-ends-with-unknown", block_line("Boards", r"[^\n]*\bversion unknown[ \t]*(?:\n|$)"), flags="")]


B31_SEED_LOG = [
    (1, "2026-10-08", f"claude-code (session {FIXTURE_SESSION})", "Created from BRN-001 v1 and the boards; 0 markers left", "all"),
    (2, "2026-10-09", f"claude-code (session {FIXTURE_SESSION})",
     "Report.dc.html changed; canvas version 1791580000-c3d4; the new version has not been reviewed", "BRD-04"),
    (2, "2026-10-09", "Example Owner", "Approved", "status")]
DSN_V2_APPROVED = dsn(B_REPORT, COVER_B, version=2, status="approved", approved_by="Example Owner", approved_on="2026-10-09",
                      updated="2026-10-09", canvas_version="1791580000-c3d4", changelog=B31_SEED_LOG)
SETTINGS_FR024 = Brd("BRD-05", "Settings.dc.html", "report-and-home", "web", [], answers=["PRD-001#FR-024"], sha=digest(SETTINGS))
PRD_V2_DSN2 = prd(version=2, requirements=[("FR-001", "The system shall record each shift with a start time and a stop time."),
                                           ("FR-002", "The system shall total the hours worked in each week.")] + SCREEN_FRS,
                  dsn_version=2)
BOARDS_AMEND_CHANGED = dict(BOARD_CONTENT, **{"Report.dc.html": REPORT_CHANGED})
PRD_CITING_1 = prd(version=1, dsn_version=1)
BOARDS_31 = BOARDS_AMEND_CHANGED


def amend_prd_requirement():
    p = "ver31"
    b = B_REPORT + [SETTINGS_FR024]
    g = [rx("ver31-version-3", DSN1, fm_has(r"version:[ \t]*3" + EOL)),
         rx("ver31-status-in-review", DSN1, fm_has(fm_field("status", "in-review"))),
         rx("ver31-approval-cleared", DSN1, fm_has(r"approved_by:[ \t]*(?:\"\"|'')" + EOL, fm_null("approved_on")))]
    g += brd_graders(p, b)
    g += [rx("ver31-considered-holds-prd-001-at-2", DSN1, fm_has(considered_has("PRD-001@2"))),
          rx("ver31-upstream-holds-no-prd-link", DSN1, fm_has(link("PRD-001", relation=None)), match="not_contains"),
          rx("ver31-upstream-holds-no-adr-link", DSN1, fm_has(link(r"ADR-\d{3}", relation=None)), match="not_contains"),
          rx("ver31-change-log-names-prd-001-version-2", DSN1,
             r"\n\|[ \t]*3[ \t]*\|[^\n]*PRD-001[^\n]*(?:version[ \t]*|\bv|@)2\b"),
          unchanged("ver31-prd-001-unchanged", "docs/specs/prd/PRD-001.md", PRD_V2_DSN2),
          unchanged("ver31-brn-001-unchanged", BRN_PATH, BRN)]
    g += boards_unchanged(p, BOARDS_31, names=FIVE)
    g += [reply("ver31-says-amended", r"Design document:(?:\*\*)?[ \t]*DSN-001 \(v3, in-review; amended\)", flags=""),
          rx("ver31-settings-not-under-boards-with-no-idea", "last_message", block_line("Boards with no idea", r"[^\n]*Settings"),
             match="not_contains"),
          reply("ver31-names-prd-001-citing-version-2", prd_cites_dsn(2)),
          rx("ver31-next-step", "last_message", next_step_has(PRD_CMD, review_by_hand("DSN-001", 3), r"\bPRD-001\b"), flags="i"),
          rx("ver31-next-step-is-last", "last_message", NEXT_STEP_LAST)]
    return g


ADR_9 = adr()
B32_SEED = B_REPORT + [SETTINGS_FR024]
B32_FINAL = [Brd(b.id, b.file, b.flow, b.surface, b.ideas, title=b.title, answers=["ADR-009"] if b.id == "BRD-02" else b.answers,
                 sha=digest(LIST_CHANGED) if b.id == "BRD-02" else b.sha) for b in B32_SEED]
DSN_V3_IN_REVIEW = dsn(B32_SEED, COVER_B, version=3, status="in-review", updated="2026-10-09", canvas_version="1791670000-e5f6",
                       considered=["PRD-001@2"],
                       changelog=B31_SEED_LOG + [(3, "2026-10-09", f"claude-code (session {FIXTURE_SESSION})",
                                                  "Settings.dc.html added; answers PRD-001#FR-024; PRD-001 version 2 considered; "
                                                  "canvas version 1791670000-e5f6; the new version has not been reviewed", "BRD-05")])
PRD_V2_DSN3 = prd(version=2, requirements=[("FR-001", "The system shall record each shift with a start time and a stop time."),
                                           ("FR-002", "The system shall total the hours worked in each week.")] + SCREEN_FRS,
                  dsn_version=3)
BOARDS_32 = dict(BOARDS_AMEND_CHANGED, **{"List.dc.html": LIST_CHANGED})


def amend_adr_consequence():
    p = "ver32"
    g = [rx("ver32-version-4", DSN1, fm_has(r"version:[ \t]*4" + EOL)),
         rx("ver32-status-stays-in-review", DSN1, fm_has(fm_field("status", "in-review")))]
    g += brd_graders(p, B32_FINAL)
    g += [rx("ver32-considered-holds-adr-009-at-1", DSN1, fm_has(considered_has("ADR-009@1"))),
          rx("ver32-considered-keeps-prd-001-at-2", DSN1, fm_has(considered_has("PRD-001@2"))),
          rx("ver32-upstream-holds-no-adr-009-link", DSN1, fm_has(link("ADR-009", relation=None)), match="not_contains"),
          unchanged("ver32-adr-009-unchanged", "docs/specs/adr/ADR-009.md", ADR_9),
          unchanged("ver32-prd-001-unchanged", "docs/specs/prd/PRD-001.md", PRD_V2_DSN3),
          unchanged("ver32-brn-001-unchanged", BRN_PATH, BRN)]
    g += boards_unchanged(p, BOARDS_32, names=FIVE)
    g += [reply("ver32-says-amended", r"Design document:(?:\*\*)?[ \t]*DSN-001 \(v4, in-review; amended\)", flags=""),
          reply("ver32-names-prd-001-citing-version-3", prd_cites_dsn(3)),
          rx("ver32-next-step", "last_message", next_step_has(PRD_CMD, review_by_hand("DSN-001", 4), r"\bPRD-001\b"), flags="i"),
          rx("ver32-next-step-is-last", "last_message", NEXT_STEP_LAST),
          rx("ver32-next-step-outside-code", "last_message", NEXT_STEP_IN_CODE, match="not_contains")]
    return g


def amend_nothing(dsn_text, unasked=False):
    """ERR-17 (version 2): the DSN is current, its version and the canvas version it records, and that the canvas was not
    checked and a change on it is seen only when a run with the tool imports it (version 1 said the boards were copied
    again: not graded)."""
    g = [unchanged("ver33-dsn-001-unchanged", DSN1, dsn_text), reply("ver33-says-dsn-001-is-current", CURRENT),
         reply("ver33-gives-version-1", r"\b(?:version[ \t]*|v)1\b"),
         reply("ver33-gives-the-recorded-canvas-version", esc(CANVAS_VERSION)),
         reply("ver33-says-canvas-not-checked", CANVAS_NOT_CHECKED),
         reply("ver33-says-a-change-is-seen-by-an-import",
               r"\bimport(?:s|ed|ing)?\b[^\n]{0,100}\b(?:board|canvas|change)|\b(?:board|canvas|change)\w*[^\n]{0,100}\bimport")]
    if unasked:
        # the candidate is left unasked under "proceed without questions": nothing is written, and the reply counts it
        g += [reply("ver33-says-one-candidate-waits",
                    r"(?:\bone\b|\b1\b)[^\n]{0,80}\b(?:candidates?|requirements?|consequences?)\b|"
                    r"\b(?:candidates?|requirements?)\b[^\n]{0,80}(?:\bone\b|\b1\b)|\bFR-024\b"),
              reply("ver33-says-for-an-interactive-run", r"\binteractive (?:run|session)\b")]
    return g


DSN_CONSIDERED_PRD = dsn(standard_boards(), COVER_A, markers=[MARKER_06], considered=["PRD-001@2"])
PRD_V2_SCREEN = prd(version=2, requirements=[("FR-001", "The system shall record each shift with a start time and a stop time."),
                                             ("FR-002", "The system shall total the hours worked in each week.")] + SCREEN_FRS)
PRD_V2_PLAIN = prd(version=2)


def approval_only_run():
    p = "ver34"
    expected = replace(DSN_B, "status: draft\n", "status: @@STATUS@@\n")
    expected = replace(expected, "updated: 2026-10-08\n", "updated: @@UPDATED@@\n")
    expected = replace(expected, 'approved_by: ""\n', "approved_by: @@BY@@\n")
    expected = replace(expected, "approved_on: null\n", "approved_on: @@ON@@\n")
    # Every line but these four and the new Change Log row equals the seeded file; updated precedes approved_on, so
    # a backreference grades "both the run's date".
    pattern = (esc(expected).replace("@@STATUS@@", Q + "approved" + Q).replace("@@UPDATED@@", "(" + DATE + ")")
               .replace("@@BY@@", Q + "Example Owner" + Q).replace("@@ON@@", Q + r"\1" + Q))
    row = r"\|[ \t]*1[ \t]*\|[ \t]*\1[ \t]*\|[ \t]*Example Owner[ \t]*\|[ \t]*Approved\.?[ \t]*\|[^|\n]*\|\n"
    g = [rx("ver34-approved-and-every-other-line-unchanged", DSN1, "^" + pattern + row + "$"),
         unchanged("ver34-brn-001-unchanged", BRN_PATH, BRN)]
    g += boards_unchanged(p, BOARDS)
    g += nothing_written(p, *NO_STRAY)
    g += [present("ver34-no-dsn-002", DSN2, exists=False), present("ver34-no-file-under-dsn-001-folder", f"{DESIGN}/DSN-001/**", exists=False),
          reply("ver34-block-is-the-single-line", OPENS_WITH_BLOCK + r"[ \t]*DSN-001 \(v1, approved\)[ \t]*(?:\n|$)", flags=""),
          rx("ver34-block-has-no-other-line", "last_message",
             r"(?:^|\n)[ \t>*-]*(?:\*\*)?(?:Boards|Flows|Boards with no idea|Ideas with no board|Markers left):", match="not_contains",
             witness="\nBoards: docs/specs/design/DSN-001/boards/ · 4 · version 17-example\n"),
          rx("ver34-next-step-names-prd", "last_message", next_step_has(PRD_CMD), flags="i"),
          rx("ver34-next-step-is-last", "last_message", NEXT_STEP_LAST),
          rx("ver34-asks-nothing", "last_message", r"\?", match="not_contains", witness="\nShall I continue?\n")]
    return g


def plain_run_never_approves():
    return [unchanged("ver35-dsn-001-unchanged", DSN1, DSN_B), rx("ver35-status-draft", DSN1, fm_has(fm_field("status", "draft"))),
            rx("ver35-approved-by-empty", DSN1, fm_has(r"approved_by:[ \t]*(?:\"\"|'')" + EOL))]


def amend_never_approves():
    return [rx("ver35-status-draft", DSN1, fm_has(fm_field("status", "draft"))),
            rx("ver35-approved-by-empty", DSN1, fm_has(r"approved_by:[ \t]*(?:\"\"|'')" + EOL)),
            rx("ver35-approved-on-null", DSN1, fm_has(fm_null("approved_on"))),
            rx("ver35-version-2", DSN1, fm_has(r"version:[ \t]*2" + EOL)),
            rx("ver35-no-approved-row", DSN1, r"\n\|[^\n]*\|[ \t]*Approved\.?[ \t]*\|", match="not_contains")]


def approval_blocked_by_changed_board():
    return [unchanged("ver36-dsn-001-unchanged", DSN1, DSN_B),
            reply("ver36-says-the-check-failed", r"\b(?:check|validation)\b[^\n]{0,100}\b(?:fail\w*|INVALID|did not pass|didn" + APOS
                  + r"t pass|errors?|not valid)\b|\b(?:fail\w*|INVALID|errors?)\b[^\n]{0,100}\b(?:check|validation)\b"),
            reply("ver36-names-the-digest", r"\bsha-?256\b|\bdigests?\b|\bhash\b"), reply("ver36-names-the-board", r"Report"),
            reply("ver36-says-an-amend-run-comes-first", r"\bamend"),
            reply("ver36-block-line-not-approved", r"Design document:(?:\*\*)?[ \t]*DSN-001 \(v1, draft; not approved\)", flags="")]


def approval_already_approved():
    return [unchanged("ver37-dsn-001-unchanged", DSN1, DSN_B_APPROVED), reply("ver37-says-already-approved", r"\balready\s+approved\b"),
            reply("ver37-gives-version-approver-and-date",
                  r"(?=[\s\S]*(?:\bversion[ \t]*1\b|\bv1\b))(?=[\s\S]*Example Owner)(?=[\s\S]*2026-10-08)", flags="")] \
        + nothing_written("ver37", *NO_STRAY)


def approval_plus_change():
    return [unchanged("ver37-dsn-001-unchanged", DSN1, DSN_B),
            reply("ver37-says-an-amend-run-comes-first", r"\bamend run\b[^\n]{0,80}\bfirst\b|\bfirst\b[^\n]{0,80}\bamend\b"),
            reply("ver37-names-the-amend-command", r"/devforgeai:ui[` \t]+BRN-001\b"),
            reply("ver37-block-line-not-approved", r"Design document:(?:\*\*)?[ \t]*DSN-001 \(v1, draft; not approved\)", flags="")] \
        + boards_unchanged("ver37", BOARDS)


DSN_SUPERSEDED = dsn(standard_boards(), COVER_B, status="superseded", approved_by="Example Owner", approved_on="2026-10-08",
                     changelog=[(1, "2026-10-08", f"claude-code (session {FIXTURE_SESSION})",
                                 "Created from BRN-001 v1 and the boards; 0 markers left", "all"),
                                (1, "2026-10-08", "Example Owner", "Approved", "status")])
ONLY_DRAFT_OR_IN_REVIEW = (r"\bonly\b[^\n]{0,80}\bdraft\b[^\n]{0,60}\bin[- ]review\b|\bdraft\b[^\n]{0,30}\b(?:or|and)\b[^\n]{0,30}"
                           r"\bin[- ]review\b[^\n]{0,60}\bonly\b|\bonly\b[^\n]{0,80}\bin[- ]review\b[^\n]{0,60}\bdraft\b")


BRIEF_PARTS_IN_ORDER = (r"\bContext\b[\s\S]*\bContent\b[\s\S]*\bMust[- ]haves?\b[\s\S]*\bStyle\b[\s\S]*" + esc(BRIEF_CLOSING))
GRID_OR_SIZE = (r"\b\d{2,3}\s*(?:columns?|cols?)\s*(?:by|x|×|\*)\s*\d{2,3}\s*rows?\b|\b\d{3,4}\s*(?:px|pixels?)\b|"
                r"\b\d{3,4}\s*(?:x|×|by)\s*\d{3,4}\b")
UNCONFIRMED = (r"\bun-?confirmed\b|\bnot (?:yet )?confirmed\b|\bawaiting (?:your )?confirmation\b|\bneeds? (?:your |the user" + APOS
               + r"s )?confirmation\b|\bto confirm\b|\bhaven" + APOS + r"t confirmed\b|\bpending confirmation\b")
IDEA_TEXTS = (r"Add a shift from the terminal|List shifts in a table|A weekly report page|A dark theme for the report page")
# The harness's judge is told to answer with one word and keeps no reasons (its votes are PASS or FAIL, a reply with both words
# counts as FAIL), so the briefs are judged by six narrow rubrics, three of them for one span each of a brief, each with the facts
# it needs, not one rubric of seven parts: a failing vote then says which part failed.
BRIEF_FACTS = """\
Everything the brainstorm behind the briefs (BRN-001, "Shiftlog: record shifts") says that a brief may quote:
- The brainstorm's context section: Shift workers record when they start and stop work, and want to see the hours they worked
  each week.
- Problem PRB-01, raised by shift workers, evidence "Interview notes": "Workers lose track of the hours they worked each week".
- Target users: Shift workers.
- Promoted ideas: IDEA-01 "Add a shift from the terminal", IDEA-02 "List shifts in a table", IDEA-03 "A weekly report page" and
  IDEA-06 "A dark theme for the report page". (IDEA-04 "Export shifts as CSV" names no screen; IDEA-05 "Sync to a server" is
  parked.)
- Assumption ASM-01: "We believe that workers will record shifts every day."
- Candidate success signal: The hours worked each week are right (quoted as "The hours worked each week are right").
"""
BRIEF_SUPPORT = """\
What the ideas support, in other words (not quotes):
- Surfaces: IDEA-01 and IDEA-02 are screens of a terminal tool; IDEA-03 and IDEA-06 are a web page. A terminal flow and a web flow, and
  a product called a terminal tool or a web app, are supported.
- Jobs: add a shift (IDEA-01); see the recorded shifts in a table (IDEA-02); read the hours worked in a week on a report page
  (IDEA-03), also in a dark theme (IDEA-06).
"""


def brief_span(label, nxt, other, criteria):
    """A rubric for one span of each brief: the instruction first, then the criteria, then the facts (ui-v2-brief2: a judge that
    answers one word applied 'adds nothing unsupported' to the lead line and the Must-haves, which other graders judge)."""
    return (f"""\
The agent was asked to design the UI for a brainstorm (BRN-001, Shiftlog: record shifts) in a session with no Artifact tool, so it
could only draft briefs for Claude Design. Each brief has a lead line, then Context, Content, Must-haves, Style and a closing line;
labels may be bold, plain or followed by a colon, and a brief may sit in a code block.
Judge ONLY the text after "{label}:" in each brief, up to its "{nxt}:" label. The lead line, {other}, the Must-haves, the Style, the
closing line and the rest of the reply are judged by other graders. A pass needs all of these:
""" + criteria + "\n\n" + BRIEF_FACTS + "\n" + BRIEF_SUPPORT.rstrip("\n"))


BRIEF_JUDGES = {
    "ver39-brief-parts-in-order": """\
The agent was asked to design the UI for a brainstorm (BRN-001, Shiftlog: record shifts) in a session with no Artifact tool, so it
could only propose flows and draft briefs for Claude Design. Judge the briefs in its output. A pass needs all of these:
- It shows one brief for each flow it proposes (one flow for the whole release gives one brief, two flows give two).
- Each brief starts with a lead line that names the flow and the product, Shiftlog.
- After its lead line each brief has, in this order, a Context, a Content, Must-haves and a Style, and each ends with a line that
  asks for 3 distinctly different directions of the key screen first.
- Labels may be bold, plain or followed by a colon, and a brief may sit in a code block.
Anything else is not a pass.""",
    "ver39-brief-context": brief_span("Context", "Content", "the Content", """\
- Each Context is two or three sentences.
- Each Context says who uses the flow and the one job it does.
- A Context adds no fact about the product that the facts below do not support. It may paraphrase the context, the users and the
  problem, and its job may restate in plain words what the ideas let the user do.
Anything else is not a pass."""),
    "ver39-brief-content-shape": brief_span("Content", "Must-haves", "the Context", """\
- Each Content quotes, between quotation marks, the wording of one or more of the sources in the facts below (an idea, the problem,
  the assumption or the success signal).
- Each Content lists the flow's screens in order, with the key screen marked.
- Each Content names at least one state to show. A state is acceptable when the ideas could support it: an empty state ("no shift
  recorded yet", "a week with no shifts"), a state with data, an error, a loading or a mid-flow state. The words empty, error and
  loading need not appear.
Anything else is not a pass."""),
    "ver39-brief-content-invents-nothing": brief_span("Content", "Must-haves", "the Context", """\
- Every wording a Content puts between quotation marks is, word for word, a wording in the facts below (a full stop inside the
  closing quotation mark is fine).
- Every screen a Content lists is one that a promoted idea names (a screen may be named by one word: List, Add, Report), and every
  state it names is one that those ideas could support.
- A Content holds no figure, name, date, hour count, field, button label or feature that nothing in the facts supports.
Anything else is not a pass."""),
    "ver39-brief-must-haves-and-no-layout": """\
Judge the Must-haves and the Style of each brief in the agent's output. A pass needs all of these:
- Each Must-haves is two to four short constraints. A constraint is a clause between semicolons (or an item on its own line);
  commas inside a clause list parts of one constraint, as in "text, box-drawing and block characters". So "a terminal screen, a
  monospace cell grid of 120 columns by 40 rows; drawn only with text, box-drawing and block characters and 24-bit colour; fully
  keyboard-driven" is three constraints.
- A terminal flow's Must-haves state a monospace cell grid of columns by rows; a web flow's state the surface and a size. A
  rendering note such as "drawn only with text, box-drawing and block characters", "keyboard-driven" or "readable in a dark theme"
  is a constraint.
- No brief prescribes a solution: no positions, spacing, sizes of parts or component-by-component layout. A surface, a screen size
  or a cell grid is a constraint, not a layout.
- Each Style refers to a design system or says to propose one, and states no colour value, no token and no font size.
Anything else is not a pass.""",
    "ver39-grouping-and-status": """\
The agent ran in a session with no Artifact tool and was told to proceed without questions. The promoted ideas that name a screen
are IDEA-01, IDEA-02, IDEA-03 and IDEA-06; IDEA-04 names none. Judge the agent's output outside the briefs. A pass needs all of
these:
- It proposes how the screens group into flows (one flow for the release, or two such as a terminal flow of IDEA-01 and IDEA-02
  and a web flow of IDEA-03 and IDEA-06), with the key screen and the surface of each flow, and says the grouping is unconfirmed.
- It says the session has no Artifact tool, and that no canvas was made and nothing was sent to claude.ai (wording such as "no
  screens designed" or "nothing goes to claude.ai without confirmation" counts).
- It names docs/specs/design/DSN-001/boards/, where a copy placed by hand is recorded.
- It contains no drawing of a screen made with characters. The words "box-drawing characters" inside a brief are a constraint on
  the canvas, not a drawing.
Anything else is not a pass.""",
}


def brief_drafted():
    p = "ver39"
    g = nothing_written("ver39", "design") + no_dsn_written("ver39")
    g += [reply("ver39-lists-the-screen-ideas", r"^(?=[\s\S]*IDEA-01)(?=[\s\S]*IDEA-02)(?=[\s\S]*IDEA-03)(?=[\s\S]*IDEA-06)"),
          reply("ver39-says-idea-04-names-no-screen",
                r"IDEA-04[^\n]{0,160}\b(?:no screen|names? no|not a screen|nothing|none|doesn" + APOS + r"t|does not|no user interface|"
                r"isn" + APOS + r"t a screen)\b"),
          reply("ver39-says-the-grouping-is-unconfirmed", UNCONFIRMED),
          # the surface is named by saying terminal or web next to the flow; the word "surface" need not appear
          reply("ver39-names-key-screen-and-surface", r"^(?=[\s\S]*\bkey screen\b)(?=[\s\S]*\b(?:terminal|web)\b)"),
          reply("ver39-briefs-in-dm05-order", BRIEF_PARTS_IN_ORDER),
          reply("ver39-quotes-an-idea", IDEA_TEXTS),
          # a state may be named by what it shows (briefs.md: "no shift recorded yet", "a week with no shifts")
          reply("ver39-names-a-state", r"\b(?:empty|error|loading|loads?|mid-flow|no shifts?|nothing (?:recorded|yet)|not yet recorded|"
                r"cannot be saved|can" + APOS + r"t be saved)\b"),
          reply("ver39-must-haves-state-a-grid-or-a-size", GRID_OR_SIZE),
          reply("ver39-style-says-propose-one", r"\bpropose one\b"),
          rx("ver39-style-holds-no-hex-or-px", "last_message",
             r"(?:^|\n)[ \t>*#-]*(?:\*\*)?Style(?:\*\*)?[:.\s][^\n]*(?:#[0-9a-fA-F]{3,8}\b|\b\d+\s?px\b)", match="not_contains",
             witness="\nStyle: a dark palette #1a1b26\n"),
          rx("ver39-no-hex-value-anywhere", "last_message", r"#[0-9a-fA-F]{6}\b", match="not_contains", witness="\ntext #1a1b26\n"),
          reply("ver39-closing-line-exact", esc(BRIEF_CLOSING), flags=""),
          reply("ver39-says-no-artifact-tool", NO_ARTIFACT),
          reply("ver39-names-boards-folder", esc(f"{DESIGN}/DSN-001/boards/"), flags=""),
          rx("ver39-no-drawing", "last_message", NO_DRAWING, match="not_contains", witness="\n┌──────┐\n│ Home │\n└──────┘\n"),
          *[llm(name, body) for name, body in BRIEF_JUDGES.items()]]
    return g


def no_screen_idea():
    return nothing_written("ver40", "design") + no_dsn_written("ver40") + [
        reply("ver40-says-no-idea-names-a-screen",
              r"(?:\bno\b|\bnone\b|\bnothing\b|\bnot\b|n" + APOS + r"t)[^\n]{0,100}\b(?:screens?|user interface|UI)\b"),
        reply("ver40-says-the-step-is-optional", r"\boptional\b"),
        reply("ver40-points-to-prd", PRD_CMD)]


def no_mockup_no_design_skill():
    return nothing_written("ver41", "design") + no_dsn_written("ver41") + [
        Grader("ver41-design-skill-not-invoked", "tool_used", min=0, max=0, input_match=DESIGN_MATCH),
        rx("ver41-no-drawing", "last_message", NO_DRAWING, match="not_contains", witness="\n+------+\n| Home |\n+------+\n"),
        reply("ver41-says-no-artifact-tool", NO_ARTIFACT)]


def approval_unknown_dsn():
    return [unchanged("ver37-dsn-001-unchanged", DSN1, DSN_B), present("ver37-no-dsn-009", f"{DESIGN}/DSN-009.md", exists=False),
            reply("ver37-lists-dsn-001-with-status", r"DSN-001[^\n]*\bdraft\b"), reply("ver37-says-only-draft-or-in-review", ONLY_DRAFT_OR_IN_REVIEW)]


def approval_superseded_dsn():
    return [unchanged("ver37-dsn-001-unchanged", DSN1, DSN_SUPERSEDED),
            reply("ver37-lists-dsn-001-with-status", r"DSN-001[^\n]*\bsuperseded\b"), reply("ver37-says-only-draft-or-in-review", ONLY_DRAFT_OR_IN_REVIEW)]


def approval_without_id():
    return [unchanged("ver37-dsn-001-unchanged", DSN1, DSN_B), reply("ver37-lists-the-dsns", r"DSN-001"),
            reply("ver37-asks-for-the-dsn-id", r"\b(?:DSN|design)\b[^\n]*\?|\bwhich\b[^\n]{0,80}\b(?:DSN|design)\b|"
                  r"\b(?:give|provide|tell|name|send|pick|choose|say|supply)\b[^\n]{0,60}\b(?:DSN|design)\b")]


LATER_RUN = (r"\b(?:later|future|another|subsequent|interactive)\s+(?:run|session)\b|\bnext run\b|\bleft for later\b|"
             r"\bwait\w*\b[^\n]{0,40}\b(?:run|session)\b")


def candidates_left():
    return [rx("ver38-version-2", DSN1, fm_has(r"version:[ \t]*2" + EOL)),
            rx("ver38-considered-does-not-hold-prd-001-at-2", DSN1, fm_has(considered_has("PRD-001@2")), match="not_contains"),
            rx("ver38-considered-holds-no-declined-entry", DSN1, r"considered:[^\n]*declined:", match="not_contains"),
            # the skill says "candidates" and also "wait for an interactive run" (SKILL.md step 2): a reply may call them requirements
            reply("ver38-says-six-candidates-were-left",
                  r"(?:\bsix\b|\b6\b)[^\n]{0,80}\b(?:candidates?|requirements?)\b|\b(?:candidates?|requirements?)\b[^\n]{0,80}(?:\bsix\b|\b6\b)"),
            reply("ver38-says-for-a-later-run", LATER_RUN)]


def candidates_declined():
    g = [rx("ver38-version-2", DSN1, fm_has(r"version:[ \t]*2" + EOL)),
         rx("ver38-considered-holds-prd-001-at-2", DSN1, fm_has(considered_has("PRD-001@2")))]
    g += [rx(f"ver38-considered-declines-fr-{n:03d}", DSN1, fm_has(considered_has(f"declined:PRD-001#FR-{n:03d}")))
          for n in range(25, 31)]
    return g


def candidates_capped():
    g = [rx("ver38-version-2", DSN1, fm_has(r"version:[ \t]*2" + EOL))]
    g += [rx(f"ver38-considered-declines-fr-{n:03d}", DSN1, fm_has(considered_has(f"declined:PRD-001#FR-{n:03d}")))
          for n in range(25, 37)]
    g += [rx("ver38-considered-does-not-decline-fr-037", DSN1, fm_has(considered_has("declined:PRD-001#FR-037")), match="not_contains"),
          rx("ver38-considered-does-not-hold-prd-001-at-2", DSN1, fm_has(considered_has("PRD-001@2")), match="not_contains"),
          reply("ver38-says-one-candidate-was-left",
                r"\b(?:one|1)\b[^\n]{0,60}\bcandidate\b[^\n]{0,80}\b(?:left|later)|\bcandidate\b[^\n]{0,80}\b(?:left|later)\b[^\n]{0,60}\b(?:one|1)\b"
                r"|FR-037[^\n]{0,80}\b(?:left|later)\b|\b(?:left|later)\b[^\n]{0,80}FR-037")]
    return g


TRIGGERS = [
    (True, "Record the screen designs for BRN-001 from the boards we copied."),
    (True, "Add the UI design step for our release before the PRD."),
    (True, "Update the UI design: the PRD now names a settings screen."),
    (True, "Turn our Claude Design boards into a design document."),
    (True, "Run the UI design step for BRN-001."),
    (True, "Approve the design document DSN-001. I am Example Owner."),
    (False, "Write the PRD for BRN-001."),
    (False, "What UI framework should I use for a CLI?"),
    (False, "Draw a login screen for me."),
    (False, "Record the approved design for STORY-001."),
    (False, "Make the button on the report page blue."),
    (False, "Make me a mockup of a settings page."),
    (True, "Design the screens for BRN-001 in Claude Design."),
]
NEGATIVE_TRIGGERS = range(7, 13)   # these run 10 times each, and must not fire in 9 (QR-04, §9)


# --------------------------------------------------------------------------------------------------------
# The cases (SPEC-017 §9)

BRN2_PATH = "docs/specs/brainstorm/BRN-002.md"
STUBS = {f"Board{n:03d}.dc.html": HEAD.format(title=f"Stub {n}") + TAIL for n in range(1, 101)}
BOARDS_REPORT_CHANGED = dict(BOARDS, **{"Report.dc.html": REPORT_CHANGED})
_OTHER_BRN_BOARDS = [
    Brd("BRD-01", "Home.dc.html", "reminders", "web", ["IDEA-02"], sha=DIGESTS["Home.dc.html"]),
    Brd("BRD-02", "List.dc.html", "reminders", "terminal", ["IDEA-02"], sha=DIGESTS["List.dc.html"]),
    Brd("BRD-03", "Add.dc.html", "reminders", "terminal", ["IDEA-01"], sha=DIGESTS["Add.dc.html"]),
    Brd("BRD-04", "Report.dc.html", "reminders", "web", [], sha=DIGESTS["Report.dc.html"])]
# VER-05: the existing DSN-001 records BRN-002, from the boards in its own folder
DSN1_OTHER_BRN = dsn(_OTHER_BRN_BOARDS, [("IDEA-01", "BRD-03", "designed"), ("IDEA-02", "BRD-01, BRD-02", "designed")],
                     brn_id="BRN-002", brn_title="Shiftlog: remind about open shifts")
DSN_B_2 = second_dsn(DSN_B)
SHARED_NO_BOARDS = {BRN_PATH: BRN}
# VER-40: converged, with promoted ideas that name no screen, flow or user interface
BRN_NO_SCREEN = brn(ideas=[("IDEA-01", "Keep shifts in a local SQLite file", "promoted"),
                           ("IDEA-02", "Back up the data nightly", "promoted"), ("IDEA-03", "Sync to a server", "parked")])
AMEND_FACTS_REPORT = ["fact: board Report.dc.html: changed"]
CANDIDATE_BASE = [("FR-001", "The system shall record each shift with a start time and a stop time."),
                  ("FR-002", "The system shall total the hours worked in each week.")]
REPORT_STANDS = "Report's mapping stands."


def case(name, ver, description, prompt, files, graders, stop=False, **kw):
    limits = SHORT_LIMITS if stop else WRITING_LIMITS
    return Case(name, [ver], f"VER-{ver}: {description}", prompt, files, graders, limits=limits, **kw)


CASES = [
    case("writes-dsn", "01", "the shared fixture and prompt write DSN-001 as draft version 1 with four active board items "
         "in canvas order, each with its digest, the derives links, the provenance and one Change Log row.",
         SHARED_PROMPT, SHARED, writes_dsn()),
    case("coverage-and-report", "02", "section 3 has the five rows (IDEA-05 is parked), section 5 one marker naming IDEA-06, "
         "and the reply opens with the report block and ends with the next step to the PRD.",
         SHARED_PROMPT, SHARED, coverage_and_report()),
    case("unconfirmed-stays-null", "03", "with no canvas facts and no mapping, every flow, surface and idea list is null with a "
         "marker, the titles are the file names' first parts, and all five promoted ideas are 'no board yet'.",
         PROMPT_UNCONFIRMED, SHARED, unconfirmed_stays_null()),
    case("no-boards-stops", "04", "with no boards folder nothing is written and the reply names the folder to copy the boards into.",
         SHARED_PROMPT, SHARED_NO_BOARDS, no_boards_stops(), stop=True, boards={"DSN-001": "ERR-03"}),
    case("boards-without-canvas-json", "04", "the boards folder holds the four board files and no canvas.json: nothing is written and "
         "the reply names the folder that must hold canvas.json and the board files it names.",
         SHARED_PROMPT, {BRN_PATH: BRN, **{f"{DESIGN}/DSN-001/boards/{n}": t for n, t in BOARDS.items()}},
         boards_without_canvas_json(), stop=True, boards={"DSN-001": "ERR-03"}),
    case("boards-at-wrong-number", "05", "the boards sit in the folder of an existing DSN-001, so the new design's number is "
         "DSN-002: nothing is written and DSN-001 is unchanged.",
         SHARED_PROMPT, {BRN_PATH: BRN, BRN2_PATH: BRN_2, DSN1: DSN1_OTHER_BRN, **boards_files()}, boards_at_wrong_number(),
         stop=True, boards={"DSN-002": "ERR-03"}),
    case("canvas-unreadable", "06", "a canvas.json that is not JSON stops the run before anything is written.",
         SHARED_PROMPT, {BRN_PATH: BRN, **boards_files(canvas="not json {\n")}, canvas_unreadable(), stop=True,
         boards={"DSN-001": "ERR-04"}),
    case("unknown-canvas-format", "07", "a canvas.json with v 4 stops the run; the reply names versions 4 and 3.",
         SHARED_PROMPT, {BRN_PATH: BRN, **boards_files(canvas=canvas_json(BOARD_ORDER, v=4))}, unknown_canvas_format(),
         stop=True, boards={"DSN-001": "ERR-05"}),
    case("board-file-absent", "08", "a canvas.json that names a missing file and a path outside the folder stops the run; "
         "both boards are named.",
         SHARED_PROMPT, {BRN_PATH: BRN, **boards_files(names=BOARD_ORDER + ["Gone.dc.html", "../outside.dc.html"], contents=BOARDS)},
         board_file_absent(), stop=True, boards={"DSN-001": "ERR-06"}),
    case("too-many-boards", "09", "a canvas.json that names 100 boards stops the run; the reply gives the count and the limit 99.",
         SHARED_PROMPT, {BRN_PATH: BRN, **boards_files(contents=STUBS)}, too_many_boards(), stop=True,
         boards={"DSN-001": "ERR-12"}),
    case("amend-changed-board", "10", "an approved DSN-001, a changed Report board and a new Settings board: the amend run quotes "
         "the pre-check, writes version 2 as in-review with approval cleared, and leaves the neighbours alone.",
         CANVAS_NOW.format(v="18-example") + " Report's mapping is unchanged. Settings is a new web screen in the flow "
         "report-and-home, as its last step, and it shows IDEA-06. Proceed without questions.",
         {BRN_PATH: BRN, DSN1: DSN_B_APPROVED, "docs/specs/prd/PRD-001.md": PRD_CITING_1,
          **boards_files(contents=BOARDS_AMEND_CHANGED, names=FIVE)}, amend_changed_board(),
         checks={"DSN-001": ("amend", ["fact: board Report.dc.html: changed", "fact: board Settings.dc.html: new"])}),
    case("amend-removed-board", "11", "a board that left the canvas is deprecated, never deleted or renumbered, and its idea "
         "becomes 'no board yet' with a marker.",
         "Update the UI design for BRN-001. I removed Add.dc.html from the canvas and from the boards folder; deprecate it. "
         "The other boards and their mappings stand. IDEA-01 now has no board yet. The canvas version of the new copy is "
         "19-example. Proceed without questions.",
         {BRN_PATH: BRN, DSN1: DSN_A, **boards_files(contents={k: v for k, v in BOARDS.items() if k != "Add.dc.html"})},
         amend_removed_board(), checks={"DSN-001": ("amend", ["fact: board Add.dc.html: removed"])}),
    case("amend-brn-moved", "12", "BRN-001 is at version 2 with a new promoted IDEA-07 and IDEA-02 parked: the links move to "
         "version 2 in one version bump, IDEA-07 gets a row and IDEA-02 a withdrawn row.",
         "Update the UI design for BRN-001. No board changed. IDEA-07 has no board yet. The boards that named IDEA-02 keep it. "
         "Proceed without questions.",
         {BRN_PATH: BRN_MOVED, DSN1: DSN_B, **boards_files()}, amend_brn_moved(),
         checks={"DSN-001": ("amend", ["fact: idea IDEA-07: no row", "fact: idea IDEA-02: no longer promoted",
                                       "fact: links: BRN-001 at version 1, the BRN is at 2"])}),
    case("unknown-brn", "13", "a BRN that does not exist writes nothing and the reply lists the one that does.",
         "Record the UI design for BRN-009.", SHARED, unknown_brn(), stop=True),
    case("path-refused", "14", "a file path instead of a BRN ID writes nothing; the reply asks for the ID.",
         "Record the UI design from docs/specs/brainstorm/BRN-001.md.", SHARED, path_refused(), stop=True),
    case("unconverged-brn", "15", "a draft BRN writes nothing and the reply warns that some ideas may not be decided.",
         PROMPT_UNCONFIRMED, {BRN_PATH: BRN_UNCONVERGED, **boards_files()}, unconverged_brn(), stop=True),
    case("no-promoted-idea", "16", "a BRN whose ideas are all open or parked writes nothing; the reply points to the brainstorm.",
         PROMPT_UNCONFIRMED, {BRN_PATH: BRN_ALL_OPEN, **boards_files()}, no_promoted_idea(), stop=True),
    case("malformed-brn", "17", "a BRN whose ideas block is malformed YAML writes nothing and is left unchanged; the reply names the "
         "block and the path.",
         PROMPT_UNCONFIRMED, {BRN_PATH: BRN_MALFORMED, **boards_files()}, malformed_brn(), stop=True,
         unparseable={BRN_PATH}),
    case("two-dsns-cite", "18", "two draft DSNs cite BRN-001: nothing is written or changed and the reply lists both and asks which to amend.",
         "Update the UI design for BRN-001. Proceed without questions.",
         {BRN_PATH: BRN, DSN1: DSN_B, DSN2: DSN_B_2, **boards_files("DSN-001"), **boards_files("DSN-002")}, two_dsns_cite(),
         stop=True),
    case("approve-blocked-by-marker", "19", "approval words in a write run don't approve while the marker for IDEA-06 remains.",
         SHARED_PROMPT + "\n\nI'm Example Owner, and I approve DSN-001, with IDEA-06 left as it is.", SHARED,
         approve_blocked_by_marker()),
    case("approve-on-explicit-words", "19", "with a fifth board placing IDEA-06 and approval words naming the approver, DSN-001 "
         "is approved at version 1.",
         PROMPT_SETTINGS + "\n\n" + APPROVAL_WORDS, {BRN_PATH: BRN, **boards_files(contents=BOARDS_5, names=FIVE)},
         approve_on_explicit_words()),
    case("no-approval-without-words", "19", "the same fixture with no approval words leaves DSN-001 a draft.",
         PROMPT_SETTINGS, {BRN_PATH: BRN, **boards_files(contents=BOARDS_5, names=FIVE)}, no_approval_without_words()),
    case("neighbours-unchanged", "20", "with a PRD, an ARCH, ADRs, context documents and a story seeded, a create run writes only "
         "DSN-001: every neighbour, the BRN and every board file are byte-identical.",
         SHARED_PROMPT, {**SHARED, **NEIGHBOURS}, neighbours_unchanged()),
    case("lists-brns", "21", "with no BRN named, the reply lists both BRNs with their titles and which DSN cites each and asks "
         "which to use; nothing is written.",
         "Record the UI design.", {BRN_PATH: BRN, BRN2_PATH: BRN_2, DSN1: DSN_B, **boards_files()}, lists_brns(), stop=True),
    case("no-brainstorm-yet", "21", "with no BRN at all, the reply says no brainstorm exists and points to /devforgeai:brainstorm.",
         "Record the UI design.", {}, no_brainstorm_yet(), stop=True, dirs=("docs/specs/brainstorm",)),
    case("no-brn-with-promoted-idea", "21", "with only a draft BRN whose ideas are all open, the reply lists it with its status and "
         "points to /devforgeai:brainstorm.",
         "Record the UI design.", {BRN_PATH: BRN_DRAFT_OPEN}, no_brn_with_promoted_idea(), stop=True),
    case("brief-drafted", "39", "no boards folder and no Artifact tool: the reply lists the screens the ideas name, proposes the flows "
         "unconfirmed, shows one brief for each in DM-05's order with the exact closing line, and says the session has no "
         "Artifact tool.",
         PROMPT_DESIGN, SHARED_NO_BOARDS, brief_drafted(), stop=True),
    case("no-screen-idea", "40", "no promoted idea names a screen, a flow or a user interface: nothing is written, the step is "
         "optional and the reply points to /devforgeai:prd BRN-001.",
         PROMPT_DESIGN, {BRN_PATH: BRN_NO_SCREEN}, no_screen_idea(), stop=True),
    case("no-mockup-no-design-skill", "41", "'Design the screens for BRN-001 in Claude Design.' without an Artifact tool: the design "
         "skill is not invoked, no screen is drawn in the reply, and the reply says the session has no Artifact tool.",
         "Design the screens for BRN-001 in Claude Design.", SHARED_NO_BOARDS, no_mockup_no_design_skill(), stop=True),
] + [
    Case(f"ui-trigger-{i:02d}", ["22"], f"VER-22 ({'positive' if fires else 'negative'}): the skill "
         f"{'fires' if fires else 'does not fire'}.", prompt, SHARED_NO_BOARDS,
         [skill_fired("ver22-skill-fired" if fires else "ver22-skill-not-fired", fires)], limits=SHORT_LIMITS,
         tags=["trigger", "ver-22", "ui-trigger"], runs=10 if i in NEGATIVE_TRIGGERS else None)
    for i, (fires, prompt) in enumerate(TRIGGERS, start=1)
] + [
    case("amend-draft-revision", "30", "a redrawn Report board and a new canvas version: DSN-001 is version 2 and still draft; the "
         "Boards line ends with the new version.",
         CANVAS_NOW.format(v="1791580000-c3d4") + " " + REPORT_STANDS + " Proceed without questions.",
         {BRN_PATH: BRN, DSN1: DSN_A, **boards_files(contents=BOARDS_REPORT_CHANGED)}, amend_draft_revision(),
         checks={"DSN-001": ("amend", AMEND_FACTS_REPORT)}),
    case("amend-without-new-version", "30", "the same, with no canvas version given: canvas_version is null with a marker, never the old value.",
         "Update the UI design for BRN-001. " + REPORT_STANDS + " Proceed without questions.",
         {BRN_PATH: BRN, DSN1: DSN_A, **boards_files(contents=BOARDS_REPORT_CHANGED)}, amend_without_new_version(),
         checks={"DSN-001": ("amend", AMEND_FACTS_REPORT)}),
    case("amend-prd-requirement", "31", "a new Settings board that answers PRD-001 FR-024: version 3, in-review, answers and "
         "considered recorded, no PRD link in upstream, the PRD untouched.",
         CANVAS_NOW.format(v="1791670000-e5f6") + " Settings is a new web screen in the flow report-and-home, as its last step. "
         "It shows no idea. It answers PRD-001 FR-024. Proceed without questions.",
         {BRN_PATH: BRN, DSN1: DSN_V2_APPROVED, "docs/specs/prd/PRD-001.md": PRD_V2_DSN2,
          **boards_files(contents=BOARDS_31, names=FIVE)}, amend_prd_requirement(),
         checks={"DSN-001": ("amend", ["fact: board Settings.dc.html: new"])}),
    case("amend-adr-consequence", "32", "a redrawn List board that answers ADR-009's consequence: version 4, still in-review, "
         "considered holds ADR-009@1, no ADR link in upstream.",
         CANVAS_NOW.format(v="1791750000-a7b8") + " List answers ADR-009 and its mapping stands. Proceed without questions.",
         {BRN_PATH: BRN, DSN1: DSN_V3_IN_REVIEW, "docs/specs/prd/PRD-001.md": PRD_V2_DSN3, "docs/specs/adr/ADR-009.md": ADR_9,
          **boards_files(contents=BOARDS_32, names=FIVE)}, amend_adr_consequence(),
         checks={"DSN-001": ("amend", ["fact: board List.dc.html: changed"])}),
    case("amend-nothing-to-do", "33", "a current draft DSN-001, no PRD and no ADR: nothing is written and the reply says it is current.",
         "Update the UI design for BRN-001. Proceed without questions.", {BRN_PATH: BRN, DSN1: DSN_A, **boards_files()},
         amend_nothing(DSN_A), stop=True),
    case("amend-nothing-with-prd", "33", "a PRD whose FR-024 names a screen but is already in considered: the same result.",
         "Update the UI design for BRN-001. Proceed without questions.",
         {BRN_PATH: BRN, DSN1: DSN_CONSIDERED_PRD, "docs/specs/prd/PRD-001.md": PRD_V2_SCREEN, **boards_files()},
         amend_nothing(DSN_CONSIDERED_PRD), stop=True),
    case("amend-nothing-with-unrelated-documents", "33", "an ADR and a PRD that name no screen and an empty considered list: no "
         "bookkeeping amend, DSN-001 is byte-identical.",
         "Update the UI design for BRN-001. Proceed without questions.",
         {BRN_PATH: BRN, DSN1: DSN_A, "docs/specs/prd/PRD-001.md": PRD_V2_PLAIN, "docs/specs/adr/ADR-001.md": ADR_NO_SCREEN,
          **boards_files()}, amend_nothing(DSN_A), stop=True),
    case("amend-nothing-with-unasked-candidate", "33", "a PRD whose FR-024 names a screen and an empty considered list, under 'proceed "
         "without questions': the candidate is left unasked, nothing is written and the reply says one candidate waits for an "
         "interactive run.",
         "Update the UI design for BRN-001. Proceed without questions.",
         {BRN_PATH: BRN, DSN1: DSN_A, "docs/specs/prd/PRD-001.md": PRD_V2_SCREEN, **boards_files()},
         amend_nothing(DSN_A, unasked=True), stop=True),
    case("approval-only-run", "34", "'/devforgeai:ui approve DSN-001' approves a valid draft: four fields and one Change Log row "
         "change, nothing else is written, and the reply is the one-line block and the next step.",
         "/devforgeai:ui approve DSN-001. I'm Example Owner.", {BRN_PATH: BRN, DSN1: DSN_B, **boards_files()},
         approval_only_run()),
    case("plain-run-never-approves", "35", "a plain run for a BRN with a current draft DSN leaves DSN-001 byte-identical and a draft.",
         "Record the UI design for BRN-001.", {BRN_PATH: BRN, DSN1: DSN_B, **boards_files()}, plain_run_never_approves(),
         stop=True),
    case("amend-never-approves", "35", "an amend run with no approval words leaves the amended DSN a draft.",
         "Update the UI design for BRN-001. Proceed without questions.",
         {BRN_PATH: BRN, DSN1: DSN_A, **boards_files(contents=BOARDS_REPORT_CHANGED)}, amend_never_approves(),
         checks={"DSN-001": ("amend", AMEND_FACTS_REPORT)}),
    case("approval-blocked-by-changed-board", "36", "a board changed since the DSN was written blocks the approval: DSN-001 is "
         "unchanged and the reply says an amend run comes first.",
         "/devforgeai:ui approve DSN-001. I'm Example Owner.",
         {BRN_PATH: BRN, DSN1: DSN_B, **boards_files(contents=BOARDS_REPORT_CHANGED)}, approval_blocked_by_changed_board(),
         stop=True, checks={"DSN-001": ("invalid", ["sha256"])}),
    case("approval-unknown-dsn", "37", "approving a DSN that does not exist writes nothing; the reply lists the DSNs and their statuses.",
         "/devforgeai:ui approve DSN-009", {BRN_PATH: BRN, DSN1: DSN_B, **boards_files()}, approval_unknown_dsn(), stop=True),
    case("approval-superseded-dsn", "37", "approving a superseded DSN writes nothing; the reply says only a draft or in-review DSN is approved.",
         "/devforgeai:ui approve DSN-001", {BRN_PATH: BRN, DSN1: DSN_SUPERSEDED, **boards_files()}, approval_superseded_dsn(),
         stop=True),
    case("approval-without-id", "37", "'Approve the design.' names no DSN: nothing is written and the reply asks for the ID.",
         "Approve the design.", {BRN_PATH: BRN, DSN1: DSN_B, **boards_files()}, approval_without_id(), stop=True),
    case("approval-already-approved", "37", "'/devforgeai:ui approve DSN-001' for a DSN that is already approved writes nothing; the "
         "reply says it is already approved, with its version, approver and date.",
         "/devforgeai:ui approve DSN-001. I'm Example Owner.", {BRN_PATH: BRN, DSN1: DSN_B_APPROVED, **boards_files()},
         approval_already_approved(), stop=True),
    case("approval-plus-change", "37", "'/devforgeai:ui approve DSN-001 and also rename the Report board to Weekly.' approves nothing "
         "and changes nothing: the reply says an amend run comes first and its block line reads 'not approved'.",
         "/devforgeai:ui approve DSN-001 and also rename the Report board to Weekly.",
         {BRN_PATH: BRN, DSN1: DSN_B, **boards_files()}, approval_plus_change(), stop=True),
    case("amend-candidates-left", "38", "six PRD requirements name a screen and none is answered; under 'proceed without questions' "
         "none is put to the user, considered lacks PRD-001@2 and the reply says six candidates were left.",
         CANVAS_NOW.format(v="1791580000-c3d4") + " " + REPORT_STANDS + " Proceed without questions.",
         {BRN_PATH: BRN, DSN1: DSN_B, "docs/specs/prd/PRD-001.md": prd(version=2, requirements=CANDIDATE_BASE + CANDIDATE_FRS[:6]),
          **boards_files(contents=BOARDS_REPORT_CHANGED)}, candidates_left(),
         checks={"DSN-001": ("amend", AMEND_FACTS_REPORT)}),
    case("amend-declined-recorded", "38", "the request declines FR-025 to FR-030 by name: considered holds PRD-001@2 and the six declined entries.",
         CANVAS_NOW.format(v="1791580000-c3d4") + " " + REPORT_STANDS + " " + DECLINE_PROMPT + " Proceed without questions.",
         {BRN_PATH: BRN, DSN1: DSN_B, "docs/specs/prd/PRD-001.md": prd(version=2, requirements=CANDIDATE_BASE + CANDIDATE_FRS[:6]),
          **boards_files(contents=BOARDS_REPORT_CHANGED)}, candidates_declined(),
         checks={"DSN-001": ("amend", AMEND_FACTS_REPORT)}),
    case("amend-candidates-capped", "38", "thirteen such requirements and a request to decline every candidate put to the user: "
         "considered holds exactly twelve declined entries and the reply says one candidate was left.",
         CANVAS_NOW.format(v="1791580000-c3d4") + " " + REPORT_STANDS + " I decline every candidate you would put to me: none of "
         "them needs a board. Don't offer to approve DSN-001.",
         {BRN_PATH: BRN, DSN1: DSN_B, "docs/specs/prd/PRD-001.md": prd(version=2, requirements=CANDIDATE_BASE + CANDIDATE_FRS),
          **boards_files(contents=BOARDS_REPORT_CHANGED)}, candidates_capped(),
         checks={"DSN-001": ("amend", AMEND_FACTS_REPORT)}),
]


# --------------------------------------------------------------------------------------------------------
# Validation of the fixtures

CONTEXT_STEMS = {"index", "architecture", "tech-stack", "source-tree", "testing", "front-end", "middle-tier", "back-end",
                 "api", "rdbms", "datastore", "ui-mockups"}
SCHEMA_FOR = {"prd": "prd", "arch": "arch", "adr": "adr", "story": "story", "brainstorm": "brainstorm",
              "design": "design", "context": "context"}
_REGISTRIES = {}


def registry(schemas=SCHEMAS):
    schemas = Path(schemas)
    if schemas not in _REGISTRIES:
        reg = Registry()
        for p in sorted(schemas.glob("*.json")):
            s = json.loads(p.read_text())
            reg = reg.with_resource(s["$id"], Resource.from_contents(s)).with_resource(p.name, Resource.from_contents(s))
        _REGISTRIES[schemas] = reg
    return _REGISTRIES[schemas]


class _Loader(yaml.SafeLoader):
    pass


_Loader.yaml_implicit_resolvers = {k: [r for r in v if r[0] != "tag:yaml.org,2002:timestamp"]
                                   for k, v in yaml.SafeLoader.yaml_implicit_resolvers.items()}


def parse(text):
    """A document as the schemas see it: its frontmatter and each yaml items block. Raises on malformed YAML."""
    m = re.match(r"---\n(.*?)\n---\n", text, re.S)
    doc = {"frontmatter": yaml.load(m.group(1), Loader=_Loader)}
    for block in re.findall(r"^```yaml items\n(.*?)^```", text, re.S | re.M):
        for key, value in yaml.load(block, Loader=_Loader).items():
            doc.setdefault(key, []).extend(value)
    return doc


def schema_kind(path):
    parts = Path(path).parts
    if len(parts) != 4 or parts[:2] != ("docs", "specs") or not path.endswith(".md"):
        return None
    if parts[2] == "context" and Path(path).stem not in CONTEXT_STEMS:
        return None
    return SCHEMA_FOR.get(parts[2])


def schema_errors(path, text, schemas=None):
    """(errors, exempt) for a document: the schema errors, and the one error SPEC-017 §9 exempts until cycle C, the
    docId pattern's at frontmatter/upstream/N/id for an instance that matches ^DSN-\\d{3}$. Nothing else is exempt."""
    schemas = Path(schemas) if schemas else SCHEMAS
    kind = schema_kind(path)
    v = Draft202012Validator(json.loads((schemas / f"{kind}.schema.json").read_text()), registry=registry(schemas),
                             format_checker=FormatChecker())
    doc_id = json.loads((schemas / "common.schema.json").read_text())["$defs"]["docId"]["pattern"]
    errors, exempt = [], []
    for e in v.iter_errors(parse(text)):
        info = {"path": "/".join(str(p) for p in e.absolute_path), "validator": e.validator,
                "instance": e.instance, "message": e.message}
        if (e.validator == "pattern" and e.validator_value == doc_id and isinstance(e.instance, str)
                and re.fullmatch(r"frontmatter/upstream/\d+/id", info["path"]) and re.fullmatch(r"DSN-\d{3}", e.instance)):
            exempt.append(info)
        else:
            errors.append(info)
    return sorted(errors, key=lambda i: i["path"]), exempt


def script(ws, *args):
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1")
    p = subprocess.run([sys.executable, "-B", str(SCRIPT), *args[:-1], "--root", str(ws), args[-1]],
                       capture_output=True, text=True, env=env)
    return p.returncode, p.stdout


def check_fixtures():
    """Runs every scaffold and checks what it wrote, every document against the schemas and every boards folder and
    DSN against the skill's script. Returns the problems found (an empty list when the fixtures are sound)."""
    problems = []
    for c in CASES:
        with tempfile.TemporaryDirectory() as tmp:
            ws = Path(tmp) / "ws"
            ws.mkdir()
            (Path(tmp) / "scaffold.sh").write_text(scaffold(c))
            subprocess.run(["bash", str(Path(tmp) / "scaffold.sh")], cwd=ws, check=True, capture_output=True)
            for path, text in c.files.items():
                if (ws / path).read_text() != text:
                    problems.append(f"{c.name}: the scaffold changed {path}")
                    continue
                if path in c.unparseable:
                    try:
                        parse(text)
                        problems.append(f"{c.name}: {path} is marked unparseable but parses")
                    except yaml.YAMLError:
                        pass
                    continue
                if schema_kind(path) is None:
                    continue
                errors, exempt = schema_errors(path, text)
                if path in c.invalid:
                    if not errors:
                        problems.append(f"{c.name}: {path} is marked invalid but validates")
                elif errors:
                    problems.append(f"{c.name}: {path} is invalid: {[e['path'] + ' ' + e['message'] for e in errors]}")
            problems += check_script(c, ws)
    return problems


def check_script(c, ws):
    problems = []
    dsns = sorted(re.match(rf"{DESIGN}/(DSN-\d{{3}})\.md$", p).group(1) for p in c.files if re.match(rf"{DESIGN}/DSN-\d{{3}}\.md$", p))
    folders = sorted({m.group(1) for p in c.files if (m := re.match(rf"{DESIGN}/(DSN-\d{{3}})/boards/", p))} | set(c.boards))
    for dsn_id in folders:
        want = c.boards.get(dsn_id, "ok")
        code, out = script(ws, "boards", dsn_id)
        if want == "ok":
            if code != 0 or not out.rstrip().endswith("boards: ok"):
                problems.append(f"{c.name}: boards {dsn_id} should be ok: {out.strip()}")
        elif code != 1 or not out.startswith(want + ":"):
            problems.append(f"{c.name}: boards {dsn_id} should fail with {want}: {out.strip()}")
    for dsn_id in dsns:
        mode = c.checks.get(dsn_id, ("current",))
        facts = lambda out: [l for l in out.splitlines() if l.startswith("fact: ")]
        if mode[0] == "current":
            code, out = script(ws, "check", dsn_id)
            if code != 0 or not out.rstrip().endswith(f"OK {DESIGN}/{dsn_id}.md"):
                problems.append(f"{c.name}: check {dsn_id} should pass: {out.strip()}")
            code, out = script(ws, "check", "--before-amend", dsn_id)
            if code != 0 or facts(out):
                problems.append(f"{c.name}: check --before-amend {dsn_id} should print no fact: {out.strip()}")
        elif mode[0] == "amend":
            code, out = script(ws, "check", "--before-amend", dsn_id)
            if code != 0 or sorted(facts(out)) != sorted(mode[1]) or not out.rstrip().endswith("(before amend)"):
                problems.append(f"{c.name}: check --before-amend {dsn_id} should print exactly {mode[1]}: {out.strip()}")
            code, out = script(ws, "check", dsn_id)
            if code != 1:
                problems.append(f"{c.name}: the full check of {dsn_id} should fail before the amend: {out.strip()}")
        elif mode[0] == "invalid":
            code, out = script(ws, "check", dsn_id)
            if code != 1 or not all(t in out for t in mode[1]):
                problems.append(f"{c.name}: the full check of {dsn_id} should fail on {mode[1]}: {out.strip()}")
    return problems


# --------------------------------------------------------------------------------------------------------
# Writing the cases


def scaffold(c):
    lines = ["#!/usr/bin/env bash", f"# Seeds the fixtures for SPEC-017 {', '.join('VER-' + v for v in c.vers)} ({c.name}). "
             "Generated by src/tests/ui/make_evals.py; edit the generator, not this file.", "set -euo pipefail"]
    made = set()
    for d in list(c.dirs) + sorted({str(Path(p).parent) for p in c.files if str(Path(p).parent) != "."}):
        if d not in made:
            made.add(d)
            lines.append(f"mkdir -p {d}")
    for path, text in sorted(c.files.items()):
        assert text.endswith("\n") and "\nUIFIXTURE\n" not in text, path
        lines.append(f"cat > {path} <<'UIFIXTURE'\n{text}UIFIXTURE")
    return "\n".join(lines) + "\n"


def grader_file(g):
    if g.type == "regex":
        target = "last_message" if g.target == "last_message" else f"{{source: file, path: {g.target}}}"
        head = ["type: regex", f"target: {target}", f"match: {g.match}"] + ([f"flags: {g.flags}"] if g.flags else [])
        assert "\n" not in g.pattern, g.name
        return "---\n" + "\n".join(head) + "\n---\n" + g.pattern + "\n"
    if g.type == "file_exists":
        return f"---\ntype: file_exists\npath: {g.target}\nexists: {'true' if g.exists else 'false'}\n---\n"
    if g.type == "llm":
        return "---\ntype: llm\n---\n\n" + g.pattern + "\n"
    head = ["type: tool_used", "tool: Skill", f"input_match: {g.input_match or SKILL_MATCH}", f"min: {g.min}"]
    head += [f"max: {g.max}"] if g.max is not None else []
    return "---\n" + "\n".join(head + ["arm: both"]) + "\n---\n"


def prompt_file(c):
    tags = c.tags or (["ui"] + [f"ver-{v}" for v in c.vers])
    turns, seconds = c.limits
    return (f"---\ndescription: {json.dumps(c.description)}\ntags: [{', '.join(tags)}]\nmax_turns: {turns}\n"
            f"timeout_seconds: {seconds}\nallowed_tools: {TOOLS}\n---\n{c.prompt}\n")


def write_cases(out):
    """Writes every case's folder under out (an empty folder). Nothing here depends on the time or the machine."""
    out = Path(out)
    for c in CASES:
        d = out / c.name
        (d / "graders").mkdir(parents=True)
        (d / "prompt.md").write_text(prompt_file(c))
        runs = f"runs: {c.runs}\n" if c.runs else ""
        (d / "case.yaml").write_text(f'schema_version: "1.1"\nname: {c.name}\n{runs}context:\n  scaffold_script: scaffold.sh\n')
        (d / "scaffold.sh").write_text(scaffold(c))
        (d / "scaffold.sh").chmod(0o755)
        for g in c.graders:
            (d / "graders" / f"{g.name}.md").write_text(grader_file(g))


def structure_problems():
    problems = []
    names = [c.name for c in CASES]
    if len(names) != len(set(names)) or len(names) != 62:
        problems.append(f"expected 62 distinct cases, found {len(names)}")
    for c in CASES:
        gnames = [g.name for g in c.graders]
        if len(gnames) != len(set(gnames)):
            problems.append(f"{c.name}: duplicate grader names")
        if not all(n.startswith(tuple(f"ver{v}-" for v in c.vers)) for n in gnames):
            problems.append(f"{c.name}: a grader name lacks the ver prefix")
    return problems


def main():
    problems = structure_problems() + check_fixtures()
    for p in problems:
        print("PROBLEM", p)
    if problems:
        return 1
    if ROOT.exists():
        shutil.rmtree(ROOT)
    write_cases(ROOT)
    print(f"wrote {len(CASES)} cases ({sum(len(c.graders) for c in CASES)} graders) to {ROOT.relative_to(REPO)}; fixtures valid; "
          "dsn_check.py agrees")
    return 0


if __name__ == "__main__":
    sys.exit(main())
