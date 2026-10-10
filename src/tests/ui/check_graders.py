"""Checks the ui eval graders offline, with good and bad simulated runs (SPEC-017 §9; the offline check
`.claude/rules/evals.md` describes for the other suites).

For the six cases below, after running each scaffold:
- a correct run (a DSN as the skill writes one, a reply as BEH-17 and BEH-18 give it) passes every grader, and a
  correct DSN also passes the skill's own `dsn_check.py check`, which is the strongest evidence that the graders and
  the script agree;
- the same reply with SKILL.md step 6's plain-text approval offer inserted before the Next step paragraph still passes
  every grader in the cases that end with Next step;
- each targeted wrong run fails exactly the graders it names;
- every grader fails in at least one wrong run: a run that writes nothing and says nothing, an automatic mutation
  (a changed byte for a whole-content grader, the file a file_exists-false grader forbids, the witness text of a
  not_contains grader) or a targeted wrong run.
The cases: writes-dsn (VER-01), coverage-and-report (VER-02), amend-changed-board (VER-10), approval-only-run (VER-34),
amend-nothing-to-do (VER-33) and the trigger cases ui-trigger-01 (fires) and ui-trigger-07 (does not fire), whose
tool_used graders are graded against simulated tool calls. Every other case has a correct run too, which must pass
all its graders (and its DSN the script's check), and fails in the empty run and the automatic mutations; a grader
that no wrong run of those catches is listed as a NOTE (the six cases above must have none).

Run from the repository root, under the normal HOME (it imports make_evals):
    PYTHONDONTWRITEBYTECODE=1 python3 src/tests/ui/check_graders.py
"""
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))
import make_evals as M  # noqa: E402

GRADE = Path(__file__).resolve().parent / "grade_evals.mjs"
TODAY = "2026-10-10"
RUN_SESSION = "7f3c9a1e-5b2d-4c8e-9a16-0d4e2b7f8c13"
SCRIPT_PATH = "/home/u/.claude/plugins/cache/devforgeai/skills/ui/scripts/dsn_check.py"
CASES = {c.name: c for c in M.CASES}
DSN1 = M.DSN1
PRD = "docs/specs/prd/PRD-001.md"

# --------------------------------------------------------------------------------------------------------
# The correct runs


def created_dsn():
    return M.dsn(M.standard_boards(), M.COVER_A, markers=[M.MARKER_06], created=TODAY, updated=TODAY, session=RUN_SESSION)


REPLY_CREATE = f"""\
Design document: DSN-001 (v1, draft; new)
Boards: docs/specs/design/DSN-001/boards/ · 4 · version 17-example
Flows: report and home (2), shifts (2)
Boards with no idea: none
Ideas with no board: IDEA-06 (A dark theme for the report page)
Markers left: DSN-001: 1
OK docs/specs/design/DSN-001.md

Boards come from the copy in docs/specs/design/DSN-001/boards/, recorded as it is. No Artifact tool in this session, so the canvas was not checked.
Check 1: OK docs/specs/design/DSN-001.md.
IDEA-04 is recorded as not a screen, as the request said; IDEA-06 has no board yet and holds the one open marker.

Next step: run /devforgeai:prd BRN-001 to write the PRD from this brainstorm, and link DSN-001 in the PRD's section 8 by hand, since the prd skill does not do it yet.
"""

SEED_LOG_B_APPROVED = [
    (1, "2026-10-08", f"claude-code (session {M.FIXTURE_SESSION})", "Created from BRN-001 v1 and the boards; 0 markers left", "all"),
    (1, "2026-10-08", "Example Owner", "Approved", "status")]


def amended_dsn():
    boards = M.B_REPORT + [M.SETTINGS_BRD]
    cover = M.COVER_DESIGNED + [("IDEA-04", "none", "not a screen"), ("IDEA-06", "BRD-05", "designed")]
    log = SEED_LOG_B_APPROVED + [(2, TODAY, f"claude-code (session {RUN_SESSION})",
                                  "Report.dc.html changed; Settings.dc.html added; canvas version 18-example; PRD-001 version 1 "
                                  "considered; the new version has not been reviewed", "BRD-04, BRD-05")]
    return M.dsn(boards, cover, version=2, status="in-review", updated=TODAY, canvas_version="18-example",
                 considered=["PRD-001@1"], changelog=log, session=RUN_SESSION)


REPLY_AMEND = f"""\
Design document: DSN-001 (v2, in-review; amended)
Boards: docs/specs/design/DSN-001/boards/ · 5 · version 18-example
Flows: report and home (3), shifts (2)
Boards with no idea: none
Ideas with no board: none
Markers left: none
OK docs/specs/design/DSN-001.md

Pre-check, as run:
- python3 "{SCRIPT_PATH}" boards DSN-001 -> boards: ok
- python3 "{SCRIPT_PATH}" check --before-amend DSN-001 -> fact: board Report.dc.html: changed; fact: board Settings.dc.html: new; OK docs/specs/design/DSN-001.md (before amend)
PRD-001 cites DSN-001 at version 1. The new version has not been reviewed.

Next step: PRD-001 cites DSN-001 at an older version. These documents cite DSN-001 at an older version; review them against DSN-001 version 2 by hand until their skills do it (cycle C): /devforgeai:prd BRN-001 for PRD-001.
"""


def approved_dsn():
    t = M.DSN_B
    t = M.replace(t, "status: draft\n", "status: approved\n")
    t = M.replace(t, "updated: 2026-10-08\n", f"updated: {TODAY}\n")
    t = M.replace(t, 'approved_by: ""\n', 'approved_by: "Example Owner"\n')
    t = M.replace(t, "approved_on: null\n", f"approved_on: {TODAY}\n")
    return t + f"| 1 | {TODAY} | Example Owner | Approved | status |\n"


REPLY_APPROVE = """\
Design document: DSN-001 (v1, approved)

Check: OK docs/specs/design/DSN-001.md.

Next step: run /devforgeai:prd BRN-001 to write the PRD, and link DSN-001 in the PRD's section 8 by hand, since the prd skill does not do it yet.
"""

REPLY_CURRENT = ("DSN-001 is current: it is at version 1 and records canvas version 17-example. Nothing was written. "
                 "Without the Artifact tool the canvas was not checked; a board changed on the canvas is seen only when a run "
                 "with the tool imports it.\n")

# Without AskUserQuestion, SKILL.md step 6 makes the approval offer the last finding of step 7, before the Next step
# paragraph. A case that ends with Next step must tolerate that line (it holds a question mark and the words
# "approve DSN-001"); none expects it, because every such case says to proceed without questions.
OFFER = "Approve DSN-001 now? Reply 'approve DSN-001' with your name, or 'not now'."
TOLERATE_OFFER = ("writes-dsn", "coverage-and-report", "neighbours-unchanged", "amend-changed-board", "amend-draft-revision",
                  "amend-prd-requirement", "amend-adr-consequence", "amend-removed-board", "amend-brn-moved")
SKILL = [{"tool": "Skill", "input": {"skill": "devforgeai:ui", "args": "BRN-001"}}]
OTHER_SKILL = [{"tool": "Skill", "input": {"skill": "devforgeai:prd", "args": "BRN-001"}}]
BASH = [{"tool": "Bash", "input": {"command": "python3 dsn_check.py next"}}]

GOOD = {
    "writes-dsn": ({DSN1: created_dsn()}, REPLY_CREATE, []),
    "coverage-and-report": ({DSN1: created_dsn()}, REPLY_CREATE, []),
    "amend-changed-board": ({DSN1: amended_dsn()}, REPLY_AMEND, []),
    "approval-only-run": ({DSN1: approved_dsn()}, REPLY_APPROVE, []),
    "amend-nothing-to-do": ({}, REPLY_CURRENT, []),
    "ui-trigger-01": ({}, "Done.", SKILL),
    "ui-trigger-07": ({}, "Done.", OTHER_SKILL),
}

# --------------------------------------------------------------------------------------------------------
# The correct runs of the other cases

def log_row_tuple(version, change, items):
    return (version, TODAY, f"claude-code (session {RUN_SESSION})", change, items)


def null_dsn():
    boards = [M.Brd(f"BRD-0{n}", f, sha=M.DIGESTS[f]) for n, f in enumerate(M.BOARD_ORDER, start=1)]
    ideas = ("IDEA-01", "IDEA-02", "IDEA-03", "IDEA-04", "IDEA-06")
    return M.dsn(boards, [(i, "none", "no board yet") for i in ideas], canvas=None, canvas_version=None, created=TODAY,
                 updated=TODAY, session=RUN_SESSION, markers=[f"[NEEDS CLARIFICATION: {i} has no board yet]" for i in ideas])


REPLY_NULL = """\
Design document: DSN-001 (v1, draft; new)
Boards: docs/specs/design/DSN-001/boards/ · 4 · version unknown
Flows: unconfirmed (4)
Boards with no idea: none
Ideas with no board: IDEA-01 (Add a shift from the terminal), IDEA-02 (List shifts in a table), IDEA-03 (A weekly report page), IDEA-04 (Export shifts as CSV), IDEA-06 (A dark theme for the report page)
Markers left: DSN-001: 11
OK docs/specs/design/DSN-001.md

Nothing was confirmed, so every mapping is null with a marker.

Next step: run /devforgeai:prd BRN-001 and link DSN-001 in the PRD's section 8 by hand.
"""


def amended(boards, cover, *, base_log, change, items, version=2, status="draft", **kw):
    kw.setdefault("canvas_version", "1791580000-c3d4")
    return M.dsn(boards, cover, version=version, status=status, updated=TODAY, session=RUN_SESSION,
                 changelog=base_log + [log_row_tuple(version, change, items)], **kw)


LOG_A = [(1, "2026-10-08", f"claude-code (session {M.FIXTURE_SESSION})", "Created from BRN-001 v1 and the boards; 1 markers left", "all")]
LOG_B = [(1, "2026-10-08", f"claude-code (session {M.FIXTURE_SESSION})", "Created from BRN-001 v1 and the boards; 0 markers left", "all")]


def removed_dsn():
    boards = M.standard_boards()
    boards[2].status = "deprecated"
    cover = [("IDEA-01", "none", "no board yet"), ("IDEA-02", "BRD-01, BRD-02", "designed"), ("IDEA-03", "BRD-04", "designed"),
             ("IDEA-04", "none", "not a screen"), ("IDEA-06", "none", "no board yet")]
    return amended(boards, cover, base_log=LOG_A, change="Add.dc.html removed (BRD-03 deprecated); canvas version 19-example; "
                   "the new version has not been reviewed", items="BRD-03", canvas_version="19-example",
                   markers=[M.MARKER_06, "[NEEDS CLARIFICATION: IDEA-01 has no board yet]"])


def moved_dsn():
    cover = [("IDEA-01", "BRD-03", "designed"), ("IDEA-02", "BRD-01, BRD-02", "withdrawn"), ("IDEA-03", "BRD-04", "designed"),
             ("IDEA-04", "none", "not a screen"), ("IDEA-06", "none", "not a screen"), ("IDEA-07", "none", "no board yet")]
    return amended(M.standard_boards(), cover, base_log=LOG_B, canvas_version="17-example", links_version=2,
                   change="BRN-001 moved to version 2: links moved to version 2; IDEA-07 added (no board yet); IDEA-02 withdrawn, its mapping kept; "
                   "the new version has not been reviewed", items="section 3", markers=["[NEEDS CLARIFICATION: IDEA-07 has no board yet]"])


def revision_dsn(canvas_version="1791580000-c3d4", status="draft"):
    return amended(M.B_REPORT, M.COVER_A, base_log=LOG_A, change="Report.dc.html changed; canvas version "
                   f"{canvas_version or 'unknown'}; the new version has not been reviewed", items="BRD-04",
                   canvas_version=canvas_version, markers=[M.MARKER_06], status=status)


def prd_amend_dsn():
    return amended(M.B_REPORT + [M.SETTINGS_FR024], M.COVER_B, base_log=M.B31_SEED_LOG, version=3, status="in-review",
                   canvas_version="1791670000-e5f6", considered=["PRD-001@2"],
                   change="Settings.dc.html added; answers PRD-001#FR-024; PRD-001 version 2 considered; the new version has not been reviewed",
                   items="BRD-05", created="2026-10-08")


def adr_amend_dsn():
    boards = [M.Brd(b.id, b.file, b.flow, b.surface, b.ideas, answers=["ADR-009"] if b.id == "BRD-02" else b.answers,
                    sha=M.digest(M.LIST_CHANGED) if b.id == "BRD-02" else b.sha) for b in M.B32_SEED]
    return amended(boards, M.COVER_B, base_log=M.B31_SEED_LOG + [(3, "2026-10-09", f"claude-code (session {M.FIXTURE_SESSION})",
                                                                   "Settings.dc.html added; answers PRD-001#FR-024", "BRD-05")],
                   version=4, status="in-review", canvas_version="1791750000-a7b8", considered=["PRD-001@2", "ADR-009@1"],
                   change="List.dc.html changed; answers ADR-009; ADR-009 version 1 considered; the new version has not been reviewed",
                   items="BRD-02", created="2026-10-08")


def candidates_dsn(considered):
    return amended(M.B_REPORT, M.COVER_B, base_log=LOG_B, considered=considered,
                   change="Report.dc.html changed; canvas version 1791580000-c3d4; the new version has not been reviewed", items="BRD-04")


def settings_dsn(status, approved=False):
    log = [(1, TODAY, f"claude-code (session {RUN_SESSION})", "Created from BRN-001 v1 and the boards; 0 markers left", "all")]
    if approved:
        log.append((1, TODAY, "Example Owner", "Approved", "status"))
    cover = M.COVER_DESIGNED + [("IDEA-04", "none", "not a screen"), ("IDEA-06", "BRD-05", "designed")]
    return M.dsn(M.standard_boards() + [M.SETTINGS_BRD], cover, status=status, created=TODAY, updated=TODAY, changelog=log,
                 session=RUN_SESSION, approved_by="Example Owner" if approved else "", approved_on=TODAY if approved else None)


def amend_block(version, status, boards_line, flows, extra=""):
    return (f"Design document: DSN-001 (v{version}, {status}; amended)\nBoards: docs/specs/design/DSN-001/boards/ · {boards_line}\n"
            f"Flows: {flows}\nBoards with no idea: none\nIdeas with no board: none\nMarkers left: none\nOK docs/specs/design/DSN-001.md\n\n{extra}")


NEXT_PRD = "Next step: run /devforgeai:prd BRN-001 to write the PRD."
REPLY_REVISION = (amend_block(2, "draft", "4 · version 1791580000-c3d4", "report and home (2), shifts (2)").replace("Markers left: none", "Markers left: DSN-001: 1")
                  .replace("Ideas with no board: none", "Ideas with no board: IDEA-06 (A dark theme for the report page)")
                  + "No document cites DSN-001.\n\n" + NEXT_PRD + "\n")
REPLY_UNKNOWN_VERSION = REPLY_REVISION.replace("version 1791580000-c3d4", "version unknown")
CITES = "PRD-001 cites DSN-001 at version {n}. The new version has not been reviewed.\n\n"
REPLY_PRD = (amend_block(3, "in-review", "5 · version 1791670000-e5f6", "report and home (3), shifts (2)")
             + CITES.format(n=2) + "Next step: PRD-001 cites DSN-001 at an older version; review it against DSN-001 version 3 by hand until its skill does it: /devforgeai:prd BRN-001.\n")
REPLY_ADR = (amend_block(4, "in-review", "5 · version 1791750000-a7b8", "report and home (3), shifts (2)")
             + CITES.format(n=3) + "Next step: PRD-001 cites DSN-001 at an older version; review it against DSN-001 version 4 by hand until its skill does it: /devforgeai:prd BRN-001.\n")
REPLY_REMOVED = (amend_block(2, "draft", "3 · version 19-example", "report and home (2), shifts (1)").replace("Markers left: none", "Markers left: DSN-001: 2")
                 + "No document cites DSN-001.\n\n" + NEXT_PRD + "\n")
REPLY_MOVED = (amend_block(2, "draft", "4 · version 17-example", "report and home (2), shifts (2)").replace("Markers left: none", "Markers left: DSN-001: 1")
               + "No document cites DSN-001.\n\n" + NEXT_PRD + "\n")
REPLY_CANDIDATES = (amend_block(2, "draft", "4 · version 1791580000-c3d4", "report and home (2), shifts (2)") + "{text}\n\n" + NEXT_PRD + "\n")
CONSIDERED_12 = [f"declined:PRD-001#FR-{n:03d}" for n in range(25, 37)]
CONSIDERED_6 = ["PRD-001@2"] + [f"declined:PRD-001#FR-{n:03d}" for n in range(25, 31)]


SAYS_MARKER_REMAINS = "DSN-001 stays draft: the marker for IDEA-06 remains, so I did not offer approval."


def stop(text):
    return ({}, text + "\n", [])


DESIGN_SKILL = [{"tool": "Skill", "input": {"skill": "design"}}]
CALLS_CASES = ("no-mockup-no-design-skill",)   # non-trigger cases with a tool_used grader: graded against simulated calls
BRIEF_SHIFTS = """\
**Brief 1: the flow shifts**

Shifts in the terminal: the List and Add screens of Shiftlog, a terminal tool, for people who work shifts and record each one from the command line.

Context: Shiftlog is used by people who work shifts. The one job of this flow: record a shift and see the shifts already recorded.

Content: the idea "List shifts in a table"; the idea "Add a shift from the terminal". The flow's screens, in order: 1. List (the key screen), 2. Add. States to show: no shift recorded yet (empty); an error when a shift cannot be saved.

Must-haves: a terminal screen, a monospace cell grid of 120 columns by 40 rows; keyboard-driven.

Style: propose one.

Give me 3 distinctly different directions of the key screen first, with a one-line tradeoff under each.
"""
BRIEF_REPORT = """\
**Brief 2: the flow report-and-home**

The weekly report: the Home and Report pages of Shiftlog, a web app, for people who want to see their week at a glance.

Context: Shiftlog users record shifts and then want to know how much they worked. The one job of this flow: read the week's report.

Content: the idea "A weekly report page"; the idea "A dark theme for the report page". The flow's screens, in order: 1. Home, 2. Report (the key screen). States to show: a week with no shifts (empty); the report while it loads.

Must-haves: a web page for a desktop browser, 1280 pixels wide; readable in a dark theme.

Style: propose one.

Give me 3 distinctly different directions of the key screen first, with a one-line tradeoff under each.
"""
REPLY_BRIEFS = """\
I made no canvas and wrote nothing: this session has no Artifact tool, which making the canvas needs (ERR-19). Here is what I would send, unconfirmed.

**Screens the promoted ideas name:** IDEA-01 (Add), IDEA-02 (List), IDEA-03 (Report) and IDEA-06 (the dark Report). IDEA-04, "Export shifts as CSV", names no screen.

**Proposed grouping, unconfirmed:**
1. shifts: List (the key screen) and Add, surface terminal.
2. report-and-home: Home and Report (the key screen), surface web.

@@BRIEF_SHIFTS@@
@@BRIEF_REPORT@@
Nothing was sent. The boards would go into docs/specs/design/DSN-001/boards/; run the skill in an interactive Claude Code session to make the canvas.
""".replace("@@BRIEF_SHIFTS@@", BRIEF_SHIFTS).replace("@@BRIEF_REPORT@@", BRIEF_REPORT)

GOOD2 = {
    "unconfirmed-stays-null": ({DSN1: null_dsn()}, REPLY_NULL, []),
    "no-boards-stops": stop("This session has no Artifact tool, which importing the canvas named in your request needs (ERR-19), and "
                            "docs/specs/design/DSN-001/boards/ holds no copy. A copy placed there by hand (canvas.json and the board files it "
                            "names) is recorded when the skill is run again, in an interactive session. Nothing was written."),
    "boards-without-canvas-json": stop("docs/specs/design/DSN-001/boards/ holds board files but no canvas.json. The folder must hold canvas.json and "
                                       "the board files it names: import the canvas, or place them there. Nothing was written."),
    "boards-at-wrong-number": stop("The next free number is DSN-002, so its boards would go in docs/specs/design/DSN-002/boards/; DSN-001's folder "
                                   "belongs to a DSN that cites BRN-002. This session has no Artifact tool to import the canvas, and that folder holds "
                                   "no copy. Nothing was written."),
    "canvas-unreadable": stop("canvas.json cannot be read as JSON (the copy may be damaged), so nothing was written. Import the canvas again, "
                              "or copy canvas.json again."),
    "unknown-canvas-format": stop("canvas.json has v 4, but only version 3 is supported. Claude Design's format is not documented, so I do not guess "
                                  "what version 4 means. Nothing was written."),
    "board-file-absent": stop("Two boards fail: Gone.dc.html is absent from the folder and ../outside.dc.html is not a plain file name. "
                              "Nothing was written; copy the boards again."),
    "too-many-boards": stop("canvas.json names 100 boards; the DSN's board IDs hold 99. Nothing was written."),
    "amend-removed-board": ({DSN1: removed_dsn()}, REPLY_REMOVED, []),
    "amend-brn-moved": ({DSN1: moved_dsn()}, REPLY_MOVED, []),
    "unknown-brn": stop("BRN-009 does not exist. The BRNs that exist: BRN-001 (Shiftlog: record shifts). Nothing was written."),
    "path-refused": stop("The skill takes a BRN ID or approve DSN-NNN, never a path; paths such as docs/specs/brainstorm/BRN-001.md are not accepted. "
                         "Which BRN ID should I use? BRN-001 has promoted ideas."),
    "unconverged-brn": stop("BRN-001 is a draft, so some ideas may not be decided. I stopped without writing; confirm that I should continue."),
    "no-promoted-idea": stop("BRN-001 has no promoted idea, so there is nothing to map the boards to. Go back to /devforgeai:brainstorm to converge it."),
    "malformed-brn": stop("The ideas block of docs/specs/brainstorm/BRN-001.md is malformed YAML (an unterminated quote), so I stopped. "
                          "Nothing was written and the BRN is unchanged."),
    "two-dsns-cite": stop("Two active DSNs cite BRN-001: DSN-001 (v1, draft) and DSN-002 (v1, draft). ADR-007 D4 allows one active DSN for each BRN. "
                          "Which one should I amend?"),
    "approve-blocked-by-marker": ({DSN1: created_dsn()}, REPLY_CREATE.split("\n\n")[0] + "\n\n" + SAYS_MARKER_REMAINS + "\n", []),
    "approve-on-explicit-words": ({DSN1: settings_dsn("approved", approved=True)}, "Approved DSN-001 for Example Owner.\n", []),
    "no-approval-without-words": ({DSN1: settings_dsn("draft")}, "Wrote DSN-001 as a draft.\n", []),
    "neighbours-unchanged": ({DSN1: created_dsn()}, REPLY_CREATE, []),
    "lists-brns": stop("BRN-001 Shiftlog: record shifts (converged, 5 promoted ideas), cited by DSN-001.\nBRN-002 Shiftlog: remind about open "
                       "shifts (converged, 2 promoted ideas), cited by none.\nWhich BRN should I use?"),
    "no-brainstorm-yet": stop("No brainstorm exists yet. Run /devforgeai:brainstorm first."),
    "no-brn-with-promoted-idea": stop("BRN-001 (draft) has no promoted idea; none of the BRNs has one. Run /devforgeai:brainstorm to converge it."),
    "amend-draft-revision": ({DSN1: revision_dsn()}, REPLY_REVISION, []),
    "amend-without-new-version": ({DSN1: revision_dsn(canvas_version=None)}, REPLY_UNKNOWN_VERSION, []),
    "amend-prd-requirement": ({DSN1: prd_amend_dsn()}, REPLY_PRD, []),
    "amend-adr-consequence": ({DSN1: adr_amend_dsn()}, REPLY_ADR, []),
    "amend-nothing-with-prd": ({}, REPLY_CURRENT, []),
    "amend-nothing-with-unrelated-documents": ({}, REPLY_CURRENT, []),
    "plain-run-never-approves": stop("DSN-001 is current: nothing to change, nothing was written."),
    "amend-never-approves": ({DSN1: revision_dsn()}, REPLY_REVISION, []),
    "approval-blocked-by-changed-board": stop("Design document: DSN-001 (v1, draft; not approved)\n\nThe check failed: Report.dc.html differs from the "
                                              "digest (sha256) recorded in DSN-001, so nothing was approved. An amend run comes first."),
    "approval-already-approved": stop("DSN-001 is already approved: version 1, approved by Example Owner on 2026-10-08. Nothing was written."),
    "approval-plus-change": stop("Design document: DSN-001 (v1, draft; not approved)\n\nI approved nothing and changed nothing: the request also asks "
                                 "for a change, so an amend run comes first: /devforgeai:ui BRN-001."),
    "amend-nothing-with-unasked-candidate": ({}, REPLY_CURRENT.rstrip("\n") + " One candidate (PRD-001 FR-024) waits for an interactive run.\n", []),
    "brief-drafted": ({}, REPLY_BRIEFS, []),
    "no-screen-idea": stop("No promoted idea of BRN-001 names a screen, a flow or a user interface (they keep shifts in a local SQLite file and back "
                           "up the data), so there is nothing to design here; this step is optional. Go on with /devforgeai:prd BRN-001. Nothing "
                           "was written."),
    "no-mockup-no-design-skill": ({}, "I can't make the canvas: this session has no Artifact tool, and I don't draw a screen in the terminal. "
                                      "Nothing was written. Run /devforgeai:ui BRN-001 in an interactive Claude Code session.\n", []),
    "approval-unknown-dsn": stop("DSN-009 does not exist. DSN-001 (v1, draft). Only a draft or in-review DSN is approved."),
    "approval-superseded-dsn": stop("DSN-001 (v1, superseded). Only a draft or in review DSN is approved."),
    "approval-without-id": stop("Which DSN should I approve? DSN-001 (v1, draft). Give me the DSN ID."),
    "amend-candidates-left": ({DSN1: candidates_dsn([])}, REPLY_CANDIDATES.format(text="Six candidates from PRD-001 version 2 were left for a later run."), []),
    "amend-declined-recorded": ({DSN1: candidates_dsn(CONSIDERED_6)}, REPLY_CANDIDATES.format(text="Declined FR-025 to FR-030 as asked."), []),
    "amend-candidates-capped": ({DSN1: candidates_dsn(CONSIDERED_12)},
                                REPLY_CANDIDATES.format(text="One candidate (PRD-001 FR-037) was left for a later run."), []),
}
for i, (fires, _) in enumerate(M.TRIGGERS, start=1):
    GOOD2[f"ui-trigger-{i:02d}"] = ({}, "Done.", SKILL if fires else OTHER_SKILL)

for name in ("ui-trigger-01", "ui-trigger-07"):
    GOOD2.pop(name)

# Final replies of suite run 1 (ui-suite1-20261010T020051, 2ace6b9), whose wording the graders refused: each must pass
# every grader of its case with the primary correct run's files.
OBSERVED_LEFT = """\
```
Design document: DSN-001 (v2, draft; amended)
Boards: docs/specs/design/DSN-001/boards/ · 4 · version 1791580000-c3d4
Flows: report and home (2), shifts (2)
Boards with no idea: none
Ideas with no board: none
Markers left: none
OK docs/specs/design/DSN-001.md
```

I updated DSN-001 to version 2. It is still a draft.

**Pre-check results**
- `dsn_check.py boards DSN-001` found 4 boards in the copy and ended with `boards: ok`. The other three boards (Home, List and Add) are identical to the last copy.
- `dsn_check.py check --before-amend DSN-001` printed one difference, `fact: board Report.dc.html: changed`, and ended with `OK docs/specs/design/DSN-001.md (before amend)`.
- All four boards were read in full; none was cut short.

**What changed in DSN-001**
- **Report board (BRD-04):** the file fingerprint is updated. Its mapping is unchanged, as you said: flow report and home, surface web, IDEA-03.
- **Canvas version:** now `1791580000-c3d4`, in the frontmatter and in section 4.
- **Version and log:** version 1 → 2, `updated` set to 2026-10-10, and one Change Log row added.
- **Not changed:** the links to BRN-001 v1 are still current, so none were moved.

**Check:** one check after the edits passed (`OK docs/specs/design/DSN-001.md`), and no repairs were needed.

**Screen requirements not mapped yet:** PRD-001 v2 has 6 requirements that name a screen and that no board answers yet: FR-025 (summary), FR-026 (edit), FR-027 (delete confirmation), FR-028 (dashboard), FR-029 (help) and FR-030 (monthly). You said not to ask questions, so I didn't put them to you. They wait for an interactive run, and PRD-001 is not yet added to `considered`.

**Not reviewed or approved:** nobody has reviewed version 2 yet. Since you said not to ask questions, I didn't offer approval.

Next step: no other document cites DSN-001, so nothing needs re-checking against version 2. Run `/devforgeai:prd BRN-001` and add DSN-001 to the PRD's section 8 by hand, because the prd skill doesn't link it yet. To map the 6 screen requirements to boards, run `/devforgeai:ui BRN-001` again without "proceed without questions".
"""
OBSERVED_CAPPED = """\
Design document: DSN-001 (v2, draft; amended)
Boards: docs/specs/design/DSN-001/boards/ · 4 · version 1791580000-c3d4
Flows: report and home (2), shifts (2)
Boards with no idea: none
Ideas with no board: none
Markers left: none
OK docs/specs/design/DSN-001.md

- **Board check:** `dsn_check.py boards DSN-001` passed with `boards: ok`. It found 4 boards in format v3.
- **Pre-check:** `dsn_check.py check --before-amend DSN-001` printed `OK docs/specs/design/DSN-001.md (before amend)`. Its only `fact:` line was `fact: board Report.dc.html: changed`. No board was added or removed, and the links to BRN-001 v1 are still current.
- **Report board:** As you said, Report's mapping is unchanged: flow report-and-home, surface web, IDEA-03. Only its file fingerprint (`sha256`) was updated.
- **Canvas version:** now 1791580000-c3d4. The canvas URL and "date of the copy: not given" are unchanged.
- **Boards read:** all four were read in full; none was cut short.
- **Declined requirements:** PRD-001 v2 has 13 requirements that name a screen. A run can put at most 12 to you, so your decline covers FR-025 to FR-036. They're recorded as declined in `considered`.
- **Left for a later run:** FR-037, the print screen. Because of that, `PRD-001@2` isn't recorded as fully considered yet. There's no ADR folder, so no ADRs were read.
- **Final check:** `OK docs/specs/design/DSN-001.md` on the first try, with no repairs. The read-back against the self-check list also passed.
- **Review:** version 2 hasn't been reviewed. Its status is still draft. As you asked, I didn't offer approval.

Next step: no other document cites DSN-001, so nothing needs a second look because of this change. Run `/devforgeai:prd BRN-001` when you're ready, and link DSN-001 in PRD section 8 by hand, since the prd skill doesn't do that yet.
"""
OBSERVED_PATH = """\
I didn't write anything. This skill needs a brainstorm ID like `BRN-001` (or `approve DSN-NNN`), and it doesn't accept file paths. That includes a path to a brainstorm file such as `docs/specs/brainstorm/BRN-001.md`, so I didn't pull the ID out of it.

There's one brainstorm with promoted ideas you can record a design from:

| BRN | Title | Status | Promoted ideas | Design document (DSN) that cites it |
|---|---|---|---|---|
| BRN-001 | Shiftlog: record shifts | converged | 5 | none |

Which brainstorm ID should I use? If it's BRN-001, run `/devforgeai:ui BRN-001`.
"""
ALT_REPLIES = {"amend-candidates-left": [OBSERVED_LEFT], "amend-candidates-capped": [OBSERVED_CAPPED], "path-refused": [OBSERVED_PATH]}

# --------------------------------------------------------------------------------------------------------
# The targeted wrong runs: (label, edits, the graders that must fail, and no others). An edit is
# ("file", path, old, new) or ("reply", None, old, new); "calls" replaces the tool calls.

A = created_dsn()
BOARD_04_SHA = M.DIGESTS["Report.dc.html"]
CREATE_BAD = [
    ("Report digest is stale", [("file", DSN1, f'sha256: "{BOARD_04_SHA}"', 'sha256: "' + "0" * 64 + '"')], {"ver01-brd-04-sha256"}),
    ("List's title is the proposal, not the file name", [("file", DSN1, 'title: "List"', 'title: "shiftlog list"')], {"ver01-brd-02-mapping"}),
    ("the status is approved", [("file", DSN1, "status: draft\n", "status: approved\n")], {"ver01-status-draft"}),
    ("a fifth board item", [("file", DSN1, "```\n\n## 3. Idea coverage",
                             '  - id: BRD-05\n    status: active\n    file: "Settings.dc.html"\n    title: "Settings"\n    flow: null\n'
                             '    surface: null\n    ideas: null\n    answers: []\n    sha256: "' + "0" * 64 + '"\n'
                             '    notes: "[NEEDS CLARIFICATION: flow, surface and ideas]"\n```\n\n## 3. Idea coverage')],
     {"ver01-no-fifth-item"}),
    ("a link for the parked IDEA-05", [("file", DSN1, "  - {id: BRN-001, item: IDEA-03, relation: derives, version: 1, hash: null}\n",
                                        "  - {id: BRN-001, item: IDEA-03, relation: derives, version: 1, hash: null}\n"
                                        "  - {id: BRN-001, item: IDEA-05, relation: derives, version: 1, hash: null}\n")],
     {"ver01-no-link-idea-05"}),
    ("the link for IDEA-03 is missing", [("file", DSN1, "  - {id: BRN-001, item: IDEA-03, relation: derives, version: 1, hash: null}\n", "")],
     {"ver01-link-idea-03"}),
    ("the session is the text ${CLAUDE_SESSION_ID}", [("file", DSN1, f'  session: "{RUN_SESSION}"', '  session: "${CLAUDE_SESSION_ID}"')],
     {"ver01-generated-by"}),
    ("canvas_format is 4", [("file", DSN1, "canvas_format: 3", "canvas_format: 4")], {"ver01-canvas-format-3"}),
    ("a board has an answers entry", [("file", DSN1, f'    answers: []\n    sha256: "{M.DIGESTS["Home.dc.html"]}"',
                                       f'    answers: ["PRD-001#FR-001"]\n    sha256: "{M.DIGESTS["Home.dc.html"]}"')],
     {"ver01-brd-01-mapping"}),
    ("approved_by is filled", [("file", DSN1, 'approved_by: ""', 'approved_by: "Example Owner"')], {"ver01-approval-empty"}),
    ("considered is not empty", [("file", DSN1, "considered: []", 'considered: ["PRD-001@1"]')], {"ver01-considered-empty"}),
    ("the title is another", [("file", DSN1, 'title: "Shiftlog: record shifts: release design"', 'title: "Shiftlog release design"')], {"ver01-title"}),
    ("the owner is another", [("file", DSN1, 'owner: "Example Owner"', 'owner: "Someone Else"')], {"ver01-owner"}),
    ("no Change Log row", [("file", DSN1, f"| 1 | {TODAY} | claude-code (session {RUN_SESSION}) | Created from BRN-001 v1 and the boards; 1 markers left | all |\n", "")],
     {"ver01-change-log-row"}),
    ("the type is another", [("file", DSN1, "type: design\n", "type: designs\n")], {"ver01-id-and-type"}),
    ("the version is 2", [("file", DSN1, "version: 1\n", "version: 2\n", 1)], {"ver01-version-1"}),
    ("canvas is null", [("file", DSN1, 'canvas: "https://claude.ai/artifact/EXAMPLE"', "canvas: null")], {"ver01-canvas"}),
    ("canvas_version is null", [("file", DSN1, 'canvas_version: "17-example"', "canvas_version: null")], {"ver01-canvas-version"}),
    ("boards_root is another number", [("file", DSN1, "boards_root: docs/specs/design/DSN-001/boards/", "boards_root: docs/specs/design/DSN-002/boards/")],
     {"ver01-boards-root"}),
    ("reviewed_by is filled", [("file", DSN1, "reviewed_by: []", 'reviewed_by: ["Someone"]')], {"ver01-reviewed-by-empty"}),
    ("the BRN link is missing", [("file", DSN1, "  - {id: BRN-001, relation: derives, version: 1, hash: null}\n", "")], {"ver01-link-brn"}),
    ("the IDEA-01 link is missing", [("file", DSN1, "  - {id: BRN-001, item: IDEA-01, relation: derives, version: 1, hash: null}\n", "")],
     {"ver01-link-idea-01"}),
    ("the first two items swap their files", [("file", DSN1, 'file: "Home.dc.html"', 'file: "Zed.dc.html"'), ("file", DSN1, 'file: "List.dc.html"', 'file: "Home.dc.html"'),
                                              ("file", DSN1, 'file: "Zed.dc.html"', 'file: "List.dc.html"')],
     {"ver01-items-in-canvas-order", "ver01-brd-01-mapping", "ver01-brd-02-mapping"}),
    ("the IDEA-02 link is missing", [("file", DSN1, "  - {id: BRN-001, item: IDEA-02, relation: derives, version: 1, hash: null}\n", "")],
     {"ver01-link-idea-02"}),
]
for n, f, flow, surface, ideas in (("01", "Home.dc.html", "report-and-home", "web", "IDEA-02"), ("02", "List.dc.html", "shifts", "terminal", "IDEA-02"),
                                   ("03", "Add.dc.html", "shifts", "terminal", "IDEA-01"), ("04", "Report.dc.html", "report-and-home", "web", "IDEA-03")):
    CREATE_BAD.append((f"BRD-{n} has no surface", [("file", DSN1, f'    file: "{f}"\n    title: "{f.split(".")[0]}"\n    flow: {flow}\n    surface: {surface}\n',
                                                  f'    file: "{f}"\n    title: "{f.split(".")[0]}"\n    flow: {flow}\n    surface: null\n')],
                       {f"ver01-brd-{n}-mapping"}))
    CREATE_BAD.append((f"BRD-{n}'s digest is stale", [("file", DSN1, f'sha256: "{M.DIGESTS[f]}"', 'sha256: "' + "1" * 64 + '"')], {f"ver01-brd-{n}-sha256"}))

COVERAGE_BAD = [
    ("the IDEA-04 row is missing", [("file", DSN1, "| IDEA-04 | none | not a screen |\n", "")],
     {"ver02-section-3-header-and-five-rows", "ver02-row-idea-04"}),
    ("a row for the parked IDEA-05", [("file", DSN1, "| IDEA-06 | none | no board yet |\n", "| IDEA-05 | none | no board yet |\n| IDEA-06 | none | no board yet |\n")],
     {"ver02-section-3-header-and-five-rows", "ver02-no-idea-05-anywhere"}),
    ("IDEA-06 is designed", [("file", DSN1, "| IDEA-06 | none | no board yet |", "| IDEA-06 | BRD-04 | designed |")], {"ver02-row-idea-06"}),
    ("IDEA-01 is on the wrong board", [("file", DSN1, "| IDEA-01 | BRD-03 | designed |", "| IDEA-01 | BRD-02 | designed |")], {"ver02-row-idea-01"}),
    ("IDEA-02 lists one board", [("file", DSN1, "| IDEA-02 | BRD-01, BRD-02 | designed |", "| IDEA-02 | BRD-01 | designed |")], {"ver02-row-idea-02"}),
    ("IDEA-03 is not a screen", [("file", DSN1, "| IDEA-03 | BRD-04 | designed |", "| IDEA-03 | none | not a screen |")], {"ver02-row-idea-03"}),
    ("IDEA-04 is no board yet", [("file", DSN1, "| IDEA-04 | none | not a screen |", "| IDEA-04 | none | no board yet |")], {"ver02-row-idea-04"}),
    ("a second marker", [("file", DSN1, "- [NEEDS CLARIFICATION: IDEA-06 has no board yet]\n", "- [NEEDS CLARIFICATION: IDEA-06 has no board yet]\n- [NEEDS CLARIFICATION: more]\n")],
     {"ver02-one-marker"}),
    ("the marker names another idea", [("file", DSN1, "[NEEDS CLARIFICATION: IDEA-06 has no board yet]", "[NEEDS CLARIFICATION: IDEA-04 has no board yet]")],
     {"ver02-section-5-marker-names-idea-06"}),
    ("no block", [("reply", None, REPLY_CREATE.split("\n\n")[0] + "\n\n", "")],
     {"ver02-block-opens-reply", "ver02-block-design-document", "ver02-block-boards", "ver02-block-flows", "ver02-block-boards-with-no-idea",
      "ver02-block-ideas-with-no-board", "ver02-block-markers-left", "ver02-block-ok-line"}),
    ("the flows keep their hyphens", [("reply", None, "report and home (2)", "report-and-home (2)")], {"ver02-block-flows"}),
    ("the markers line says none", [("reply", None, "Markers left: DSN-001: 1", "Markers left: none")], {"ver02-block-markers-left"}),
    ("the Boards line has another count", [("reply", None, "· 4 ·", "· 5 ·")], {"ver02-block-boards"}),
    ("the Boards line lacks the version", [("reply", None, " · version 17-example", "")], {"ver02-block-boards"}),
    ("the block says amended", [("reply", None, "(v1, draft; new)", "(v1, draft; amended)")], {"ver02-block-design-document"}),
    ("Boards with no idea lists a board", [("reply", None, "Boards with no idea: none", "Boards with no idea: Report.dc.html")], {"ver02-block-boards-with-no-idea"}),
    ("Ideas with no board says none", [("reply", None, "Ideas with no board: IDEA-06 (A dark theme for the report page)", "Ideas with no board: none")],
     {"ver02-block-ideas-with-no-board"}),
    ("no OK line in the block", [("reply", None, "OK docs/specs/design/DSN-001.md\n\nBoards come from", "\nBoards come from")], {"ver02-block-ok-line"}),
    ("a paragraph after the next step", [("reply", None, "since the prd skill does not do it yet.\n", "since the prd skill does not do it yet.\n\nAnything else?\n")],
     {"ver02-next-step-is-last", "ver02-next-step-names-prd"}),
    ("the next step does not mention section 8", [("reply", None, ", and link DSN-001 in the PRD's section 8 by hand, since the prd skill does not do it yet", "")],
     {"ver02-next-step-names-prd"}),
    ("the next step names another command", [("reply", None, "/devforgeai:prd BRN-001", "/devforgeai:epic PRD-001")], {"ver02-next-step-names-prd"}),
    ("the next step is not a Next step paragraph", [("reply", None, "Next step: run", "Then run")], {"ver02-next-step-is-last", "ver02-next-step-names-prd"}),
]

B_OLD_APPROVED_ROW = "| 1 | 2026-10-08 | Example Owner | Approved | status |\n"
AMEND_BAD = [
    ("Report's digest is the old one", [("file", DSN1, f'sha256: "{M.digest(M.REPORT_CHANGED)}"', f'sha256: "{M.DIGESTS["Report.dc.html"]}"')],
     {"ver10-brd-04-sha256"}),
    ("the status stays approved", [("file", DSN1, "status: in-review\n", "status: approved\n")], {"ver10-status-in-review"}),
    ("approved_by is not cleared", [("file", DSN1, 'approved_by: ""', 'approved_by: "Example Owner"')], {"ver10-approval-cleared"}),
    ("the version stays 1", [("file", DSN1, "version: 2\n", "version: 1\n")], {"ver10-version-2"}),
    ("the Approved row is dropped", [("file", DSN1, B_OLD_APPROVED_ROW, "")], {"ver10-change-log-keeps-version-1-rows"}),
    ("no version 2 Change Log row", [("file", DSN1, f"| 2 | {TODAY} | claude-code (session {RUN_SESSION}) | Report.dc.html changed; Settings.dc.html added; "
                                                   "canvas version 18-example; PRD-001 version 1 considered; the new version has not been reviewed | BRD-04, BRD-05 |\n", "")],
     {"ver10-change-log-version-2-row"}),
    ("Settings is missing", [("file", DSN1, "\n  - id: BRD-05", "\n  - id: BRD-06", 1), ("file", DSN1, "| IDEA-06 | BRD-05 | designed |", "| IDEA-06 | none | not a screen |"),
                             ("file", DSN1, "  - {id: BRN-001, item: IDEA-06, relation: derives, version: 1, hash: null}\n", "")],
     {"ver10-brd-05-settings", "ver10-row-idea-06-designed", "ver10-link-idea-06"}),
    ("Settings is not on a web surface", [("file", DSN1, '    title: "Settings"\n    flow: report-and-home\n    surface: web\n', '    title: "Settings"\n    flow: report-and-home\n    surface: mobile\n')],
     {"ver10-brd-05-settings"}),
    ("the PRD is edited", [("file", PRD, "shall total", "shall sum")], {"ver10-prd-001-unchanged"}),
    ("the BRN is edited", [("file", M.BRN_PATH, "Shift workers.", "Everyone.")], {"ver10-brn-001-unchanged"}),
    ("a board file is edited", [("file", f"{M.DESIGN}/DSN-001/boards/Home.dc.html", "Shiftlog home", "Shiftlog start")], {"ver10-board-home-unchanged"}),
    ("canvas.json is edited", [("file", f"{M.DESIGN}/DSN-001/boards/canvas.json", '"h": 760', '"h": 761', 5)], {"ver10-canvas-json-unchanged"}),
    ("the commands are in the other order", [("reply", None, f'- python3 "{SCRIPT_PATH}" boards DSN-001 -> boards: ok\n- python3 "{SCRIPT_PATH}" check --before-amend DSN-001 ->',
                                              f'- python3 "{SCRIPT_PATH}" check --before-amend DSN-001 -> x\n- python3 "{SCRIPT_PATH}" boards DSN-001 ->')],
     {"ver10-pre-check-order"}),
    ("the Report fact is not quoted", [("reply", None, "fact: board Report.dc.html: changed; ", "")], {"ver10-fact-report-changed"}),
    ("the Settings fact is not quoted", [("reply", None, "fact: board Settings.dc.html: new; ", "")], {"ver10-fact-settings-new"}),
    ("the block says new", [("reply", None, "(v2, in-review; amended)", "(v2, in-review; new)")], {"ver10-says-amended"}),
    ("PRD-001 is not named as citing", [("reply", None, "PRD-001 cites DSN-001 at version 1. The new version has not been reviewed.\n", "The new version has not been reviewed.\n")],
     {"ver10-names-prd-citing-version-1"}),
    ("PRD-001 is named without DSN-001 on the line", [("reply", None, "PRD-001 cites DSN-001 at version 1.", "PRD-001 cites it at version 1.")],
     {"ver10-names-prd-citing-version-1"}),
    ("the next step lacks the review sentence", [("reply", None, "review them against DSN-001 version 2 by hand until their skills do it (cycle C)", "review them")],
     {"ver10-next-step"}),
    ("the next step reviews against another version", [("reply", None, "against DSN-001 version 2 by hand", "against DSN-001 version 1 by hand")], {"ver10-next-step"}),
    ("the next step does not name the command", [("reply", None, "/devforgeai:prd BRN-001 for PRD-001.", "the prd skill for PRD-001.")], {"ver10-next-step"}),
    ("a paragraph after the next step", [("reply", None, "for PRD-001.\n", "for PRD-001.\n\nDone.\n")], {"ver10-next-step", "ver10-next-step-is-last"}),
]

for n, f, flow, surface, ideas in (("01", "Home.dc.html", "report-and-home", "web", "IDEA-02"), ("02", "List.dc.html", "shifts", "terminal", "IDEA-02"),
                                   ("03", "Add.dc.html", "shifts", "terminal", "IDEA-01"), ("04", "Report.dc.html", "report-and-home", "web", "IDEA-03")):
    AMEND_BAD.append((f"BRD-{n} has no surface", [("file", DSN1, f'    file: "{f}"\n    title: "{f.split(".")[0]}"\n    flow: {flow}\n    surface: {surface}\n',
                                                  f'    file: "{f}"\n    title: "{f.split(".")[0]}"\n    flow: {flow}\n    surface: null\n')],
                      {f"ver10-brd-{n}-mapping"}))
    if n != "04":
        AMEND_BAD.append((f"BRD-{n}'s digest is stale", [("file", DSN1, f'sha256: "{M.DIGESTS[f]}"', 'sha256: "' + "1" * 64 + '"')],
                          {f"ver10-brd-{n}-sha256"}))

APPROVE_BAD = [
    ("the version is raised", [("file", DSN1, "version: 1\n", "version: 2\n", 1)], {"ver34-approved-and-every-other-line-unchanged"}),
    ("another line is edited", [("file", DSN1, "# DSN-001 — Shiftlog: record shifts: release design", "# DSN-001 — Shiftlog release design")],
     {"ver34-approved-and-every-other-line-unchanged"}),
    ("approved_on is not the run's date", [("file", DSN1, f"approved_on: {TODAY}", "approved_on: 2026-10-09")], {"ver34-approved-and-every-other-line-unchanged"}),
    ("the status is not approved", [("file", DSN1, "status: approved", "status: in-review")], {"ver34-approved-and-every-other-line-unchanged"}),
    ("there is no Approved row", [("file", DSN1, f"| 1 | {TODAY} | Example Owner | Approved | status |\n", "")], {"ver34-approved-and-every-other-line-unchanged"}),
    ("the approver is another", [("file", DSN1, 'approved_by: "Example Owner"', 'approved_by: "Someone Else"')], {"ver34-approved-and-every-other-line-unchanged"}),
    ("the BRN is edited", [("file", M.BRN_PATH, "Shift workers.", "Everyone.")], {"ver34-brn-001-unchanged"}),
    ("a board is edited", [("file", f"{M.DESIGN}/DSN-001/boards/Report.dc.html", "2026-W41", "2026-W42")], {"ver34-board-report-unchanged"}),
    ("the block has a Boards line", [("reply", None, "Design document: DSN-001 (v1, approved)\n", "Design document: DSN-001 (v1, approved)\nBoards: docs/specs/design/DSN-001/boards/ · 4 · version 17-example\n")],
     {"ver34-block-has-no-other-line"}),
    ("the block says draft", [("reply", None, "(v1, approved)", "(v1, draft; not approved)")], {"ver34-block-is-the-single-line"}),
    ("the reply asks a question", [("reply", None, "Check: OK", "Shall I also open the PRD? Check: OK")], {"ver34-asks-nothing"}),
    ("the next step names no command", [("reply", None, "/devforgeai:prd BRN-001", "the next skill")], {"ver34-next-step-names-prd"}),
    ("a paragraph after the next step", [("reply", None, "does not do it yet.\n", "does not do it yet.\n\nDone.\n")],
     {"ver34-next-step-names-prd", "ver34-next-step-is-last"}),
]

NOTHING_BAD = [
    ("the status was changed", [("file", DSN1, "status: draft", "status: approved")], {"ver33-dsn-001-unchanged"}),
    ("the version was raised", [("file", DSN1, "version: 1\n", "version: 2\n", 1)], {"ver33-dsn-001-unchanged"}),
    ("it does not say the DSN is current", [("reply", None, "DSN-001 is current:", "DSN-001 stands:")], {"ver33-says-dsn-001-is-current"}),
    ("it does not give the version", [("reply", None, "at version 1 and", "at revision one and")], {"ver33-gives-version-1"}),
    ("it does not give the canvas version", [("reply", None, "17-example", "unknown")], {"ver33-gives-the-recorded-canvas-version"}),
    ("it does not say the canvas was not checked", [("reply", None, "Without the Artifact tool the canvas was not checked; a board changed",
                                                      "A board changed")], {"ver33-says-canvas-not-checked"}),
    ("it does not say a change is seen by an import", [("reply", None, "; a board changed on the canvas is seen only when a run with the tool imports it", "")],
     {"ver33-says-a-change-is-seen-by-an-import"}),
    ("it says the boards are copied again, as version 1 did", [("reply", None, "a board changed on the canvas is seen only when a run with the tool imports it",
                                                                "a board changed on the canvas must be copied into the boards folder again")],
     {"ver33-says-a-change-is-seen-by-an-import"}),
]

TRIGGER_BAD = {
    "ui-trigger-01": [("no Skill call", {"calls": []}, {"ver22-skill-fired"}),
                      ("the prd skill fires instead", {"calls": OTHER_SKILL}, {"ver22-skill-fired"}),
                      ("a Bash call only", {"calls": BASH}, {"ver22-skill-fired"})],
    "ui-trigger-07": [("the ui skill fires", {"calls": SKILL}, {"ver22-skill-not-fired"})],
}
for i, (fires, _) in enumerate(M.TRIGGERS, start=1):
    name = f"ui-trigger-{i:02d}"
    if name not in TRIGGER_BAD:
        TRIGGER_BAD[name] = ([("no Skill call", {"calls": []}, {"ver22-skill-fired"}), ("the prd skill fires instead", {"calls": OTHER_SKILL}, {"ver22-skill-fired"})]
                             if fires else [("the ui skill fires", {"calls": SKILL}, {"ver22-skill-not-fired"})])
TRIGGER_BAD["no-mockup-no-design-skill"] = [("the design skill is invoked", {"calls": DESIGN_SKILL}, {"ver41-design-skill-not-invoked"}),
                                           ("the ui skill is not the design skill", {"calls": SKILL}, set())]
STATUS_APPROVED = ("file", DSN1, "status: draft\n", "status: approved\n")
BAD2 = {
    "writes-dsn": [("the findings are silent about the copy and the canvas", [("reply", None, "Boards come from the copy in docs/specs/design/DSN-001/boards/, recorded as it is. No Artifact tool in this session, so the canvas was not checked.\n", "")],
                    {"ver01-says-copy-recorded-as-it-is", "ver01-says-no-artifact-tool-in-this-session", "ver01-says-canvas-not-checked"}),
                   ("the canvas is not said to be unchecked", [("reply", None, " No Artifact tool in this session, so the canvas was not checked.", "")],
                    {"ver01-says-no-artifact-tool-in-this-session", "ver01-says-canvas-not-checked"})],
    "no-boards-stops": [("no statement about the tool", [("reply", None, "This session has no Artifact tool, which importing the canvas named in your request needs (ERR-19), and ", "")],
                         {"ver04-says-no-artifact-tool"}),
                        ("a drawing of a screen", [("reply", None, "Nothing was written.", "Nothing was written.\n┌──────┐\n│ Home │\n└──────┘")],
                         {"ver04-no-drawing"}),
                        ("no copy by hand is recorded when run again", [("reply", None, "A copy placed there by hand (canvas.json and the board files it names) is recorded when the skill is run again, in an interactive session. ", "")],
                         {"ver04-says-a-copy-placed-by-hand-is-recorded-when-run-again"})],
    "boards-at-wrong-number": [("no statement about the tool", [("reply", None, "This session has no Artifact tool to import the canvas, and that folder holds no copy. ", "")],
                                {"ver05-says-no-artifact-tool"})],
    "canvas-unreadable": [("it does not ask to import or copy again", [("reply", None, " Import the canvas again, or copy canvas.json again.", "")],
                           {"ver06-asks-to-import-or-copy-again"})],
    "approval-blocked-by-changed-board": [("the block line says approved", [("reply", None, "(v1, draft; not approved)", "(v1, approved)")],
                                           {"ver36-block-line-not-approved"})],
    "approval-already-approved": [("it does not say already approved", [("reply", None, "is already approved:", "is a draft:")], {"ver37-says-already-approved"}),
                                  ("it does not give the approver", [("reply", None, "approved by Example Owner on 2026-10-08", "approved")],
                                   {"ver37-gives-version-approver-and-date"})],
    "approval-plus-change": [("it says nothing about an amend run", [("reply", None, "so an amend run comes first: /devforgeai:ui BRN-001.", "so nothing else happened.")],
                              {"ver37-says-an-amend-run-comes-first", "ver37-names-the-amend-command"}),
                             ("the block line says approved", [("reply", None, "(v1, draft; not approved)", "(v1, approved)")],
                              {"ver37-block-line-not-approved"})],
    "amend-nothing-with-unasked-candidate": [("it does not count the candidate", [("reply", None, " One candidate (PRD-001 FR-024) waits for an interactive run.", "")],
                                              {"ver33-says-one-candidate-waits", "ver33-says-for-an-interactive-run"})],
    "brief-drafted": [("the closing line is missing from the second brief", [("reply", None, "Give me 3 distinctly different directions of the key screen first, with a one-line tradeoff under each.\n\nNothing was sent.", "\nNothing was sent.")],
                       set()),
                      ("no closing line at all", [("reply", None, "Give me 3 distinctly different directions of the key screen first, with a one-line tradeoff under each.\n", "", 2)],
                       {"ver39-briefs-in-dm05-order", "ver39-closing-line-exact"}),
                      ("the Style holds a hex value", [("reply", None, "Style: propose one.\n\nGive me 3 distinctly different directions of the key screen first, with a one-line tradeoff under each.\n\n**Brief 2", "Style: propose one, dark #1a1b26.\n\nGive me 3 distinctly different directions of the key screen first, with a one-line tradeoff under each.\n\n**Brief 2")],
                       {"ver39-style-holds-no-hex-or-px", "ver39-no-hex-value-anywhere"}),
                      ("a drawing of a screen", [("reply", None, "Nothing was sent.", "Nothing was sent.\n┌────────┐\n│ Shifts │\n└────────┘")],
                       {"ver39-no-drawing"}),
                      ("no statement about the tool", [("reply", None, "this session has no Artifact tool, which making the canvas needs (ERR-19). Here", "here")],
                       {"ver39-says-no-artifact-tool"}),
                      ("the grouping is not called unconfirmed", [("reply", None, "Here is what I would send, unconfirmed.", "Here is what I would send."),
                                                                 ("reply", None, "**Proposed grouping, unconfirmed:**", "**Proposed grouping:**")],
                       {"ver39-says-the-grouping-is-unconfirmed"}),
                      ("the folder is not named", [("reply", None, "The boards would go into docs/specs/design/DSN-001/boards/; run", "Run")],
                       {"ver39-names-boards-folder"}),
                      ("IDEA-04 is not mentioned", [("reply", None, " IDEA-04, \"Export shifts as CSV\", names no screen.", "")],
                       {"ver39-says-idea-04-names-no-screen"})],
    "no-screen-idea": [("it does not point to the PRD", [("reply", None, " Go on with /devforgeai:prd BRN-001.", "")], {"ver40-points-to-prd"}),
                       ("it does not call the step optional", [("reply", None, "; this step is optional", "")], {"ver40-says-the-step-is-optional"})],
    "no-mockup-no-design-skill": [("a drawing of a screen", [("reply", None, "Nothing was written.", "Nothing was written.\n+------+\n| Home |\n+------+")],
                                   {"ver41-no-drawing"}),
                                  ("no statement about the tool", [("reply", None, "this session has no Artifact tool, and ", "")], {"ver41-says-no-artifact-tool"})],
    "approve-blocked-by-marker": [("only the Markers left line says it", [("reply", None, SAYS_MARKER_REMAINS + "\n", "")],
                                   {"ver19-reply-says-the-marker-remains"})],
    "path-refused": [("no question or request", [("reply", None, " Which BRN ID should I use? BRN-001 has promoted ideas.", "")],
                      {"ver14-asks-for-the-brn-id"})],
    "malformed-brn": [("the block is not named", [("reply", None, "The ideas block of", "The ideas of")], {"ver17-names-the-ideas-block"})],
    "approval-without-id": [("no question or request", [("reply", None, "Which DSN should I approve? ", "Only DSN-NNN can be approved. "),
                                                         ("reply", None, " Give me the DSN ID.", "")], {"ver37-asks-for-the-dsn-id"})],
    "amend-removed-board": [("BRD-04 renumbered", [("file", DSN1, "BRD-04", "BRD-05", 2)], {"ver11-no-item-renumbered"})],
    "amend-brn-moved": [("BRD-03 deprecated", [("file", DSN1, '    status: active\n    file: "Add.dc.html"', '    status: deprecated\n    file: "Add.dc.html"')],
                         {"ver12-no-item-deprecated"})],
    "amend-draft-revision": [("the status is in-review", [("file", DSN1, "status: draft\n", "status: in-review\n")], {"ver30-status-stays-draft"}),
                             ("the version 1 row is dropped", [("file", DSN1, f"| 1 | 2026-10-08 | claude-code (session {M.FIXTURE_SESSION}) | Created from BRN-001 v1 and the boards; 1 markers left | all |\n", "")],
                              {"ver30-change-log-keeps-version-1-row"})],
    "amend-prd-requirement": [
        ("a PRD link in upstream", [("file", DSN1, "  - {id: BRN-001, relation: derives, version: 1, hash: null}\n",
                                     "  - {id: BRN-001, relation: derives, version: 1, hash: null}\n  - {id: PRD-001, relation: informed_by, version: 2, hash: null}\n")],
         {"ver31-upstream-holds-no-prd-link"}),
        ("an ADR link in upstream", [("file", DSN1, "  - {id: BRN-001, relation: derives, version: 1, hash: null}\n",
                                      "  - {id: BRN-001, relation: derives, version: 1, hash: null}\n  - {id: ADR-009, relation: informed_by, version: 1, hash: null}\n")],
         {"ver31-upstream-holds-no-adr-link"}),
        ("PRD-001 is named without DSN-001 on the line", [("reply", None, "PRD-001 cites DSN-001 at version 2.", "PRD-001 cites it at version 2.")],
         {"ver31-names-prd-001-citing-version-2"}),
        ("Settings is listed as a board with no idea", [("reply", None, "Boards with no idea: none", "Boards with no idea: Settings.dc.html")],
         {"ver31-settings-not-under-boards-with-no-idea"})],
    "amend-adr-consequence": [
        ("an ADR link in upstream", [("file", DSN1, "  - {id: BRN-001, relation: derives, version: 1, hash: null}\n",
                                      "  - {id: BRN-001, relation: derives, version: 1, hash: null}\n  - {id: ADR-009, relation: informed_by, version: 1, hash: null}\n")],
         {"ver32-upstream-holds-no-adr-009-link"}),
        ("PRD-001 is named without DSN-001 on the line", [("reply", None, "PRD-001 cites DSN-001 at version 3.", "PRD-001 cites it at version 3.")],
         {"ver32-names-prd-001-citing-version-3"}),
        ("considered lost PRD-001@2", [("file", DSN1, '"PRD-001@2", ', "")], {"ver32-considered-keeps-prd-001-at-2"}),
        ("the status is approved", [("file", DSN1, "status: in-review\n", "status: approved\n")], {"ver32-status-stays-in-review"}),
        ("the next step is in a code block", [("reply", None, "/devforgeai:prd BRN-001.\n", "/devforgeai:prd BRN-001.\n```")], {"ver32-next-step-outside-code"})],
    "plain-run-never-approves": [("the status is approved", [("file", DSN1, "status: draft\n", "status: approved\n")], {"ver35-status-draft"}),
                                 ("approved_by is filled", [("file", DSN1, 'approved_by: ""', 'approved_by: "Example Owner"')], {"ver35-approved-by-empty"})],
    "amend-never-approves": [("the status is approved", [("file", DSN1, "status: draft\n", "status: approved\n")], {"ver35-status-draft"}),
                             ("approved_by is filled", [("file", DSN1, 'approved_by: ""', 'approved_by: "Example Owner"')], {"ver35-approved-by-empty"}),
                             ("approved_on is set", [("file", DSN1, "approved_on: null", "approved_on: 2026-10-10")], {"ver35-approved-on-null"}),
                             ("an Approved row", [("file", DSN1, "the new version has not been reviewed | BRD-04 |\n",
                                                   "the new version has not been reviewed | BRD-04 |\n| 2 | 2026-10-10 | Example Owner | Approved | status |\n")],
                              {"ver35-no-approved-row"})],
    "amend-candidates-left": [("considered holds PRD-001@2", [("file", DSN1, "considered: []", 'considered: ["PRD-001@2"]')],
                               {"ver38-considered-does-not-hold-prd-001-at-2"}),
                              ("considered holds a declined entry", [("file", DSN1, "considered: []", 'considered: ["declined:PRD-001#FR-025"]')],
                               {"ver38-considered-holds-no-declined-entry"})],
    "amend-candidates-capped": [("FR-037 is declined too", [("file", DSN1, "considered: [", 'considered: ["declined:PRD-001#FR-037", ')],
                                {"ver38-considered-does-not-decline-fr-037"}),
                                ("considered holds PRD-001@2", [("file", DSN1, "considered: [", 'considered: ["PRD-001@2", ')],
                                 {"ver38-considered-does-not-hold-prd-001-at-2"})],
}
BAD = {"writes-dsn": CREATE_BAD, "coverage-and-report": COVERAGE_BAD, "amend-changed-board": AMEND_BAD,
       "approval-only-run": APPROVE_BAD, "amend-nothing-to-do": NOTHING_BAD}

# --------------------------------------------------------------------------------------------------------


def workspace(case, tmp):
    ws = Path(tmp) / "ws"
    ws.mkdir()
    (Path(tmp) / "scaffold.sh").write_text(M.scaffold(case))
    subprocess.run(["bash", str(Path(tmp) / "scaffold.sh")], cwd=ws, check=True, capture_output=True)
    return ws


def grade(case, files, reply, calls=None):
    """Runs the scaffold, applies the run's files (None deletes), and grades. Returns {grader: bool | None}."""
    case_dir = (M.ROOT / case.name).resolve()
    with tempfile.TemporaryDirectory() as tmp:
        ws = workspace(case, tmp)
        for path, text in files.items():
            p = ws / path
            if text is None:
                p.unlink()
            else:
                p.parent.mkdir(parents=True, exist_ok=True)
                p.write_text(text)
        (Path(tmp) / "reply.txt").write_text(reply)
        (Path(tmp) / "seeded.json").write_text(json.dumps(sorted(case.files)))
        args = [str(case_dir), str(ws), str(Path(tmp) / "reply.txt"), str(Path(tmp) / "seeded.json")]
        if calls is not None:
            (Path(tmp) / "calls.json").write_text(json.dumps(calls))
            args.append(str(Path(tmp) / "calls.json"))
        out = subprocess.run(["node", str(GRADE), *args], capture_output=True, text=True, check=True)
    return json.loads(out.stdout)


def script_check(case, files):
    """The correct run also passes the skill's dsn_check.py check."""
    if DSN1 not in files:
        return 0, ""
    with tempfile.TemporaryDirectory() as tmp:
        ws = workspace(case, tmp)
        for path, text in files.items():
            (ws / path).write_text(text)
        return M.script(ws, "check", "DSN-001")


def failing(results):
    return {k for k, v in results.items() if v is False}


def apply(case, files, reply, calls, edits):
    files = dict(files)
    for edit in edits:
        kind, path, old, new = edit[:4]
        count = edit[4] if len(edit) > 4 else 1
        if kind == "reply":
            assert reply.count(old) == count, f"{case.name}: the reply has {reply.count(old)} of {old!r}"
            reply = reply.replace(old, new)
        else:
            text = files[path] if path in files else case.files[path]
            assert text.count(old) >= 1 and (count is None or text.count(old) == count), f"{case.name}: {path} has {text.count(old)} of {old!r}"
            files[path] = text.replace(old, new)
    return files, reply, calls


def mutations(case, files, reply):
    """Automatic wrong runs: (grader, files, reply) where the grader must fail."""
    for g in case.graders:
        if g.type == "file_exists" and g.exists is False:
            path = g.target[:-3] + "/stray.md" if g.target.endswith("/**") else g.target
            yield g.name, dict(files, **{path: "stray\n"}), reply
        elif (g.type == "regex" and g.match == "contains" and g.pattern.startswith("^") and g.pattern.endswith("$")
              and g.target != "last_message" and g.name.endswith("-unchanged")):
            text = files.get(g.target, case.files.get(g.target))
            yield g.name, dict(files, **{g.target: text.replace("\n", " \n", 1)}), reply
        elif g.type == "regex" and g.match == "not_contains" and g.witness is not None:
            if g.target == "last_message":
                yield g.name, files, reply + g.witness
            else:
                text = files.get(g.target, case.files.get(g.target))
                yield g.name, dict(files, **{g.target: text + g.witness}), reply


def item_mutations(case, files, reply):
    """A board item's mapping or digest changed, for the graders named ver*-brd-NN-mapping and -sha256."""
    text = files.get(DSN1)
    for g in case.graders:
        m = re.fullmatch(r"ver\d\d-brd-(\d\d)-(mapping|sha256)", g.name)
        if not (m and text):
            continue
        start = text.index(f"  - id: BRD-{m.group(1)}\n")
        ends = [text.find(t, start + 1) for t in ("\n  - id: BRD-", "```")]
        block = text[start:min(e for e in ends if e != -1)]
        if m.group(2) == "sha256":
            changed = re.sub(r'sha256: "[0-9a-f]{64}"', 'sha256: "' + "2" * 64 + '"', block)
        else:
            changed = re.sub(r'title: "([^"]*)"', r'title: "Other \1"', block)
        assert changed != block, g.name
        yield g.name, dict(files, **{DSN1: text.replace(block, changed)}), reply


def main():
    if not M.ROOT.is_dir():
        sys.exit("Run make_evals.py first, from the repository root.")
    problems, checked, runs = [], 0, 0
    notes = []
    for name, (files, reply, calls) in list(GOOD.items()) + list(GOOD2.items()):
        case = CASES[name]
        is_trigger = name.startswith("ui-trigger-")
        with_calls = is_trigger or name in CALLS_CASES
        good = grade(case, files, reply, calls if with_calls else None)
        runs += 1
        graded = {k for k, v in good.items() if v is not None}
        if failing(good):
            problems.append(f"{name}: the correct run fails {sorted(failing(good))}")
        if not is_trigger:
            code, out = script_check(case, files)
            if code != 0:
                problems.append(f"{name}: the correct run fails dsn_check.py check:\n{out}")
        for i, alt in enumerate(ALT_REPLIES.get(name, []), start=1):
            observed = grade(case, files, alt)
            runs += 1
            if failing(observed):
                problems.append(f"{name}: the observed reply {i} fails {sorted(failing(observed))}")
        if name in TOLERATE_OFFER:
            at = reply.rindex("Next step")
            offered = grade(case, files, reply[:at] + OFFER + "\n\n" + reply[at:])
            runs += 1
            if failing(offered):
                problems.append(f"{name}: the plain-text approval offer before Next step fails {sorted(failing(offered))}")
        caught = failing(grade(case, {}, "", [] if with_calls else None))
        runs += 1
        bad_runs = [(label, apply(case, files, reply, calls, [])[0], reply, edit["calls"], expected, True)
                    for label, edit, expected in TRIGGER_BAD.get(name, [])]
        if not is_trigger:
            for label, edits, expected in BAD.get(name, []):
                bfiles, breply, _ = apply(case, files, reply, None, edits)
                bad_runs.append((label, bfiles, breply, calls if with_calls else None, expected, True))
            for label, edits, expected in BAD2.get(name, []):
                bfiles, breply, _ = apply(case, files, reply, None, edits)
                bad_runs.append((label, bfiles, breply, calls if with_calls else None, expected, False))
            for gname, mfiles, mreply in list(mutations(case, files, reply)) + list(item_mutations(case, files, reply)):
                got = failing(grade(case, mfiles, mreply, calls if with_calls else None))
                runs += 1
                if gname not in got:
                    problems.append(f"{name}: the mutation for {gname} doesn't fail it")
                caught |= got
        for label, bfiles, breply, bcalls, expected, exact in bad_runs:
            got = failing(grade(case, bfiles, breply, bcalls))
            runs += 1
            if (got != expected) if exact else not (expected <= got):
                problems.append(f"{name}: '{label}' fails {sorted(got)}, expected {'exactly ' if exact else 'at least '}{sorted(expected)}")
            caught |= got
        targeted = set().union(*[b[4] for b in bad_runs]) if bad_runs else set()
        for gname in sorted(graded - caught):
            (problems if name in GOOD else notes).append(f"{name}: {gname} never fails in any wrong run")
        checked += len(graded)
        print(f"{name}: {len(graded)} graders, {len(bad_runs)} targeted wrong runs fail {len(targeted)} of them by name; "
              f"{len(caught & graded)} fail in some wrong run")
    for n in notes:
        print("NOTE", n)
    for p in problems:
        print("PROBLEM", p)
    print(f"{checked} graders checked over {runs} simulated runs: "
          + (f"{len(problems)} problem(s)" if problems else "every grader passes the correct run and fails a wrong one"))
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
