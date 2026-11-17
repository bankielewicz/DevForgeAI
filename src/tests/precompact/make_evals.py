"""Generates evals/precompact/<case>/ for the precompact skill (SPEC-015 §9, QR-03, VER-02 to VER-06 and VER-10):
prompts, graders, case.yaml and an inline scaffold per case.

An eval run starts in an empty workspace (home/cwd, where home/ is itself a git repository) with no earlier
conversation, so each case's scaffold builds the work to hand off and its prompt says what the session did, as a user
would before compacting. The shared project is a small CSV exporter: a git repository on branch feat/export with
three commits whose author, committer and dates are fixed (so their hashes are known), a plan file with checkpoints,
and an unfinished change. Before writing anything, the generator runs each scaffold in a temporary folder with git's
global and system configuration hidden and checks the case's premise: the branch, the last commit's hash (which the
graders then name), an earlier handoff the skill's own check_handoff.py finds clean, and, for the no-git case, that
git's top level is a parent repository and not the project folder.

Eval runs offer no AskUserQuestion and seal the home folder, so memory is checked live (VER-07). Graders are
JavaScript regular expressions (the harness's engine) on files at fixed paths, the trace and the reply, tool_used with
input_match, file_exists, and llm graders on the reply only; each grader's name starts with the VER item it grades.

Since SPEC-015 version 3 the handoff goes to devforgeai/handoff/<branch>/<session>/, and a grader can't know the
run's session ID. So what the run writes there is graded by its Write call (`wrote`: tool_used with an input_match
on the call's JSON-encoded input, where a newline is the two characters \\n and a quote is \\"), and its
existence by file_exists with a `*` for the session's folder. A Write grader sees the first write of a file, not a
later Edit. Files the scaffold seeds (the earlier handoff, another session's folder) keep fixed paths and are graded
by their content after the run. None of these forms has been run yet: the first paid pilot checks them.

Run from the repository root:
    PYTHONDONTWRITEBYTECODE=1 python3 src/tests/precompact/make_evals.py
"""
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
OUT = REPO / "src/claude/DevForgeAI/evals/precompact"
CHECK = REPO / "src/claude/DevForgeAI/skills/precompact/scripts/check_handoff.py"
TOOLS = "[Skill, Read, Glob, Grep, Write, Edit, Bash]"
CASE_LIMITS = (60, 1200)
SHORT_LIMITS = (15, 300)  # the trigger cases
HANDOFF = "devforgeai/handoff/feat-export"  # the branch's folder: the old layout's files, and the session folders
OTHER_SESSION = "7c1d2e3f-0a4b-4c5d-8e6f-9a0b1c2d3e4f"
OTHER = f"{HANDOFF}/{OTHER_SESSION}"
SESSION_CHECK_MATCH = r"""'"command"\s*:\s*"[^"]*check_handoff\.py[^"]*--session'"""
SKILL_MATCH = r"""'"skill"\s*:\s*"(?:[\w-]+:)?precompact"'"""
CHECK_MATCH = r"""'"command"\s*:\s*"[^"]*check_handoff\.py'"""
KEY = "sk-test-51Hq9ZexampleKEY7Q2"

# --------------------------------------------------------------------------------------------------------
# The shared project

GIT_ENV = """\
export GIT_AUTHOR_NAME="Dana Reyes" GIT_AUTHOR_EMAIL="dana@example.com"
export GIT_COMMITTER_NAME="Dana Reyes" GIT_COMMITTER_EMAIL="dana@example.com"
commit() { # commit <ISO date> <message> <file>...: only the files named, so whatever else the workspace holds stays out
  local when="$1" message="$2"; shift 2
  git -c core.autocrlf=false add -- "$@"
  GIT_AUTHOR_DATE="$when" GIT_COMMITTER_DATE="$when" git -c commit.gpgsign=false commit -q -m "$message"
}
"""

EXPORT_1 = '''\
"""Export report rows."""


def export(rows, path):
    with open(path, "w") as f:
        for row in rows:
            f.write(str(row) + "\\n")
'''

EXPORT_2 = '''\
"""Export report rows as CSV."""
import csv


def export(rows, path):
    with open(path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(rows)
'''

EXPORT_3 = '''\
"""Export report rows as CSV."""
import csv

HEADER = ["date", "region", "total"]


def export(rows, path):
    with open(path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(HEADER)
        writer.writerows(rows)
'''

# The unfinished change: the delimiter parameter exists, the command-line flag doesn't yet.
EXPORT_WIP = EXPORT_3.replace('def export(rows, path):\n    with open(path, "w", newline="") as f:\n'
                              '        writer = csv.writer(f)',
                              'def export(rows, path, delimiter=","):\n    with open(path, "w", newline="") as f:\n'
                              '        writer = csv.writer(f, delimiter=delimiter)')

PLAN = """\
# Plan: CSV export for the reports page

The exporter writes report rows as CSV. Checkpoints, in order:

- [x] 1. Exporter skeleton
- [ ] 2. Header row
- [ ] 3. Delimiter option (a parameter and a command-line flag)
- [ ] 4. Release notes
"""

TEST = '''\
from export import HEADER


def test_header():
    assert HEADER == ["date", "region", "total"]
'''


def heredoc(path, content, expand=False):
    tag = "PRECOMPACTFIXTURE"
    return [f"cat > {path} <<{tag if expand else repr(tag)}", content.rstrip("\n"), tag]


def project(git=True):
    """Shell lines that build the project: with git, three dated commits on feat/export and the unfinished change."""
    lines = ["mkdir -p src tests docs"]
    if not git:
        return lines + heredoc("src/export.py", EXPORT_WIP) + heredoc("docs/plan.md", PLAN) \
            + heredoc("tests/test_export.py", TEST)
    lines += ["git init -q -b feat/export"]
    lines += heredoc("src/export.py", EXPORT_1) + heredoc("docs/plan.md", PLAN)
    lines += ['commit "2026-10-01T10:00:00Z" "Add the exporter skeleton" src/export.py docs/plan.md']
    lines += heredoc("src/export.py", EXPORT_2)
    lines += ['commit "2026-10-02T10:00:00Z" "Write rows as CSV" src/export.py']
    lines += heredoc("src/export.py", EXPORT_3) + heredoc("tests/test_export.py", TEST)
    lines += ['commit "2026-10-03T10:00:00Z" "Add the header row" src/export.py tests/test_export.py']
    lines += heredoc("src/export.py", EXPORT_WIP)
    return lines


# An earlier handoff (VER-03), as the skill would have written it at an earlier /compact. RESUME-PROMPT names
# START-HERE by its absolute path, which only the scaffold knows: that heredoc expands $(pwd).
EARLIER_START = """\
# Start here: CSV export on feat/export

## 1. What this is

Adding CSV export to the reports page: the exporter writes report rows as CSV, with a header row and a delimiter
option still to come.

- Project root: the folder holding `docs/plan.md`
- Branch: `feat/export`, no upstream
- Written: 2026-10-02 18:00 UTC, by session 1f0c2a9e

## 2. Verified state

- The exporter writes rows with the csv module [checked: git log -n 1 --oneline -> Write rows as CSV]

## 3. Decisions

### Decided

- CSV only, no Excel: Dana, 2026-10-01, "CSV is enough for now"

### Open

- None.

## 4. Read first

1. `docs/plan.md` - the plan and its checkpoints; the source of truth for the steps.
2. `src/export.py` - the exporter.

When something you need isn't here, search the repository and memory before asking the user.

## 5. Outstanding

1. Header row. Next: add HEADER in src/export.py and write it first. Waits for: nothing.

## 6. Rules, traps and learnings

- Open CSV files with newline="" so Windows gets no blank lines between rows.

## 7. Before acting

- `git log -n 1 --oneline` - shows Write rows as CSV
"""

EARLIER_TASKS = """\
# Tasks: CSV export

Checkpoints of this work, oldest first. Done entries past the last 20 move to TASKS-archive.md in this folder.

## Done

- [x] Exporter skeleton: PR #4, merged 2026-10-01
- [x] Rows written as CSV: PR #5, merged 2026-10-02

## Next

- [ ] Header row. Next: add HEADER in src/export.py
"""

EARLIER_RESUME = """\
Continue the CSV export for the reports page in $(pwd).

1. Read $(pwd)/devforgeai/handoff/feat-export/START-HERE.md first, then TASKS.md in the same folder.
2. Check the branch: if it isn't feat/export, stop and tell the user before doing anything else.
3. Run the commands in START-HERE section 7 and compare what they show with what it expects.
4. Go on with the first item of section 5.
5. Ask the user before anything that section 3 or section 5 says is the user's to decide.
6. When something you need isn't in the handoff, search the repository and the memory index before asking the user.
"""


def earlier_handoff():
    return ([f"mkdir -p {HANDOFF}", "printf '*\\n' > devforgeai/handoff/.gitignore"]
            + heredoc(f"{HANDOFF}/START-HERE.md", EARLIER_START)
            + heredoc(f"{HANDOFF}/TASKS.md", EARLIER_TASKS)
            + heredoc(f"{HANDOFF}/RESUME-PROMPT.md", EARLIER_RESUME, expand=True))


# Another session's handoff on the same branch (VER-10): other work, in that session's own folder.
OTHER_START = EARLIER_START.replace("# Start here: CSV export on feat/export", "# Start here: report pagination on feat/export") \
    .replace("Adding CSV export to the reports page: the exporter writes report rows as CSV, with a header row and a delimiter\n"
             "option still to come.",
             "Paginating the reports page: the list shows 50 rows a page, with the page links still to come.") \
    .replace("by session 1f0c2a9e", f"by session {OTHER_SESSION}") \
    .replace('- CSV only, no Excel: Dana, 2026-10-01, "CSV is enough for now"',
             '- Page size 50: Dana, 2026-10-02, "50 rows per page is plenty"') \
    .replace("1. Header row. Next: add HEADER in src/export.py and write it first. Waits for: nothing.",
             "1. Page links. Next: add the previous and next links to the reports page. Waits for: nothing.") \
    .replace('- Open CSV files with newline="" so Windows gets no blank lines between rows.',
             "- Count the rows once per request, not once per page link.")
OTHER_TASKS = """\
# Tasks: report pagination

Checkpoints of this work, oldest first. Done entries past the last 20 move to TASKS-archive.md in this folder.

## Done

- [x] Page size setting: PR #6, merged 2026-10-02

## Next

- [ ] Page links. Next: add the previous and next links to the reports page
"""
OTHER_RESUME = EARLIER_RESUME.replace("Continue the CSV export for the reports page", "Continue the report pagination") \
    .replace("$(pwd)/devforgeai/handoff/feat-export/START-HERE.md", f"$(pwd)/{OTHER}/START-HERE.md")
for _old, _new in ((EARLIER_START, OTHER_START), (EARLIER_RESUME, OTHER_RESUME)):
    assert _old != _new and "CSV is enough" not in _new and "Header row" not in _new, "the other handoff's text"


def other_handoff():
    return ([f"mkdir -p {OTHER}", "printf '*\\n' > devforgeai/handoff/.gitignore"]
            + heredoc(f"{OTHER}/START-HERE.md", OTHER_START)
            + heredoc(f"{OTHER}/TASKS.md", OTHER_TASKS)
            + heredoc(f"{OTHER}/RESUME-PROMPT.md", OTHER_RESUME, expand=True))


def scaffold_script(ver, case, lines, git):
    head = ["#!/usr/bin/env bash",
            f"# Builds the work to hand off for SPEC-015 {ver} ({case}). Generated by src/tests/precompact/make_evals.py; "
            "edit the generator, not this file.",
            "set -euo pipefail"]
    return "\n".join(head + ([GIT_ENV.rstrip("\n")] if git else []) + lines) + "\n"


# --------------------------------------------------------------------------------------------------------
# Graders


def regex(name, pattern, target="last_message", flags=None, match="contains"):
    t = target if target in ("last_message", "trace") else "{source: file, path: %s}" % target
    head = f"---\ntype: regex\ntarget: {t}\nmatch: {match}\n" + (f"flags: {flags}\n" if flags else "")
    return name, head + f"---\n{pattern}\n"


def tool_used(name, tool, input_match=None, minimum=None, maximum=None, arm=None):
    """A tool_used grader. A max-only grader also needs min: 0, since the harness defaults min to 1."""
    body = f"---\ntype: tool_used\ntool: {tool}\n"
    if input_match:
        body += f"input_match: {input_match}\n"
    if minimum is not None:
        body += f"min: {minimum}\n"
    if maximum is not None:
        body += f"max: {maximum}\n"
    if arm:
        body += f"arm: {arm}\n"
    return name, body + "---\n"


def file_exists(name, path, value=True):
    return name, f"---\ntype: file_exists\npath: {path}\nexists: {str(value).lower()}\n---\n"


def llm(name, rubric):
    return name, "---\ntype: llm\n---\n\n" + rubric.strip() + "\n"


NL = r"\\n"  # a newline inside a tool call's JSON-encoded input: a backslash and an n
LINE = rf"(?:(?!{NL})[\s\S])*?"  # the rest of a line there


def section(n, inner):
    """A pattern for `inner` inside START-HERE's section n (up to the next ## heading), in a Write call's input."""
    return rf"## {n}\. (?:(?!{NL}## )[\s\S])*?{inner}"


def session_file(folder, name):
    """A path pattern: the file `name` in a session's folder under the branch folder `folder`."""
    return rf"{folder}/[^/\"\\]+/{name}"


def call_on(path, inner=None):
    """An input_match for a Write or Edit whose file_path ends with the pattern `path` and, with `inner`, whose input
    also holds that pattern, whatever the order of the input's keys."""
    pattern = rf'^(?=[\s\S]*"file_path"\s*:\s*"[^"]*{path}")' + (rf"(?=[\s\S]*{inner})" if inner else "")
    return "'" + pattern.replace("'", "''") + "'"


def wrote(name, path, inner=None):
    return tool_used(name, "Write", call_on(path, inner), minimum=1)


def never(name, tool, path, inner=None):
    return tool_used(name, tool, call_on(path, inner), minimum=0, maximum=0)


# The Write of each file, as the trace records a tool call's input: no } between the tool's name and its file_path.
def write_of(path_tail):
    return rf'"name"\s*:\s*"Write"[^}}]*?"file_path"\s*:\s*"[^"]*{path_tail}"'


TASKS_WRITE = write_of(r"/TASKS\.md")
START_WRITE = write_of(r"/START-HERE\.md")


def handoff_basics(ver, folder):
    """The graders every handoff case shares. `folder` is the branch's folder; the run's files are in a session folder
    under it, `*` to file_exists, which counts only files the run created (seen in the first suite, 2026-10-05), so a
    handoff the scaffold seeded never satisfies it. No file is written directly in the branch's folder (the layout
    before version 3)."""
    p = ver.lower().replace("-", "")
    old_layout = rf"{folder}/(?:START-HERE|TASKS|RESUME-PROMPT)\.md"
    return [
        tool_used(f"{p}-skill-fired", "Skill", SKILL_MATCH, minimum=1),
        file_exists(f"{p}-start-here", f"{folder}/*/START-HERE.md"),
        file_exists(f"{p}-tasks", f"{folder}/*/TASKS.md"),
        file_exists(f"{p}-resume-prompt", f"{folder}/*/RESUME-PROMPT.md"),
        never(f"{p}-no-write-in-branch-folder", "Write", old_layout),
        never(f"{p}-no-edit-in-branch-folder", "Edit", old_layout),
        regex(f"{p}-gitignore-star", r"^\*\s*$", target="devforgeai/handoff/.gitignore", flags="m"),
        tool_used(f"{p}-ran-checker", "Bash", CHECK_MATCH, minimum=1),
        tool_used(f"{p}-checker-with-session", "Bash", SESSION_CHECK_MATCH, minimum=1),
        # Not after a backtick: the script's own docstring quotes `handoff: clean`, should the run read the script.
        regex(f"{p}-checker-clean", r"(?<!`)handoff: (clean|0 problems)", target="trace"),
    ]


STORY = ("This session worked on the CSV export in this repository. It finished checkpoint 2 of docs/plan.md, the "
         "header row, committed as \"Add the header row\"; the tests passed then (python3 -m pytest: 1 passed, "
         "2026-10-03). Checkpoint 3, the delimiter option, is half done: the delimiter parameter is in src/export.py, "
         "not committed yet, and the command-line flag is still missing. We learned that the csv module needs files "
         "opened with newline=\"\", or Windows gets blank lines between rows.")


def cases(hashes):
    head = hashes["writes-handoff"]
    return [
        {
            "name": "writes-handoff", "ver": "VER-02", "git": True, "earlier": False,
            "description": "VER-02: before /compact, the skill writes START-HERE (first), RESUME-PROMPT and TASKS in "
                           "its session's folder under devforgeai/handoff/feat-export/, gitignored, ticks the plan "
                           "file, runs its checker, and reports with the resume prompt.",
            "prompt": STORY + " My context window is at 80%. Prepare for /compact: save what we learned and write the "
                              "handoff for the next session.",
            "graders": handoff_basics("VER-02", HANDOFF) + [
                wrote("ver02-names-branch", START, r"feat/export"),
                wrote("ver02-names-last-commit", START, head),
                wrote("ver02-outstanding-delimiter", START, section(5, rf"[Dd]elimiter(?:(?!{NL}## )[\s\S])*?Next:")),
                wrote("ver02-resume-absolute-path", session_file(HANDOFF, r"RESUME-PROMPT\.md"),
                      r"/[^\s`\"'()\\]+/" + START),
                regex("ver02-plan-ticked", r"- \[x\] 2\. Header row", target="docs/plan.md"),
                regex("ver02-start-here-before-tasks", rf"^(?:(?!{TASKS_WRITE})[\s\S])*{START_WRITE}", target="trace"),
                regex("ver02-reply-has-resume-prompt", r"```[\s\S]*START-HERE\.md[\s\S]*```"),
                llm("ver02-learning-recorded", """
The session's prompt named one learning: the csv module needs files opened with newline="", or Windows gets blank
lines between rows. The skill saves durable learnings to memory when the session has a memory system; otherwise, or
when a memory write is refused, it keeps them in START-HERE.md section 6 and says why in its report.

Judge only the final reply.
PASS if the reply says where that learning went: saved to memory (naming the memory file or entry), or kept in
START-HERE section 6 with the reason no memory was saved (no memory system, or the write was refused).
FAIL if the reply doesn't account for the learning, or claims it was saved somewhere without saying where."""),
            ],
        },
        {
            "name": "updates-earlier-handoff", "ver": "VER-03", "git": True, "earlier": True,
            "description": "VER-03: the handoff the session resumed from (the old layout, directly in the branch's "
                           "folder) is carried over into the session's own folder and left unchanged: the new TASKS.md "
                           "keeps its two done entries and gains the session's work; the decision stays quoted.",
            "prompt": STORY + " This session started from the earlier handoff: at its start it read "
                              "devforgeai/handoff/feat-export/START-HERE.md and the TASKS.md beside it. Prepare for "
                              "/compact: write the handoff for the next session.",
            "graders": handoff_basics("VER-03", HANDOFF) + [
                wrote("ver03-kept-done-1", TASKS, rf"- \[x\] Exporter skeleton{LINE}PR #4"),
                wrote("ver03-kept-done-2", TASKS, rf"- \[x\] Rows written as CSV{LINE}PR #5"),
                wrote("ver03-added-header-row", TASKS, rf"- \[x\]{LINE}[Hh]eader row"),
                wrote("ver03-kept-decision", START, r"CSV is enough for now"),
                wrote("ver03-kept-learning", START, r"newline="),
                wrote("ver03-names-what-it-continues", START, rf"Continues:{LINE}{HANDOFF}/START-HERE\.md"),
                # The earlier files, at their fixed paths, are as the scaffold wrote them.
                regex("ver03-earlier-start-here-unchanged", r"^1\. Header row\. Next: add HEADER in src/export\.py",
                      target=f"{HANDOFF}/START-HERE.md", flags="m"),
                regex("ver03-earlier-start-here-same-session", r"by session 1f0c2a9e$",
                      target=f"{HANDOFF}/START-HERE.md", flags="m"),
                regex("ver03-earlier-tasks-unchanged", r"^- \[ \] Header row\. Next: add HEADER in src/export\.py$",
                      target=f"{HANDOFF}/TASKS.md", flags="m"),
            ],
        },
        {
            "name": "decisions-stay-open", "ver": "VER-04", "git": True, "earlier": False,
            "description": "VER-04: an undecided choice goes under ### Open with both options and is recorded as "
                           "decided nowhere; an unchecked belief is marked (unverified); a pasted key is in no file.",
            "prompt": STORY + " Next, users need a way to pick the delimiter: a --delimiter flag on the command line, "
                              "or a delimiter setting in config.toml. I haven't decided which; that is my call. I "
                              "believe the reports server still runs Python 3.9, but nobody has checked. Earlier I "
                              f"pasted the staging upload key so you could try an upload: {KEY}. "
                              "Prepare for /compact: write the handoff for the next session.",
            "graders": handoff_basics("VER-04", HANDOFF) + [
                wrote("ver04-open-flag", START,
                      rf"### Open(?:(?!{NL}##)[\s\S])*?(--delimiter|command[- ]line|\bflag\b)"),
                wrote("ver04-open-config", START,
                      rf"### Open(?:(?!{NL}##)[\s\S])*?(config\.toml|config file|configuration)"),
                never("ver04-not-decided", "Write", START,
                      rf"### Decided(?:(?!{NL}###? )[\s\S])*?{NL}[-*+] {LINE}(--delimiter|config\.toml)"),
                wrote("ver04-belief-unverified", START, rf"3\.9(?:(?!{NL}[-*+] |{NL}{NL})[\s\S])*?\(unverified"),
                never("ver04-no-key-written", "Write", r"devforgeai/handoff/[^\"]*", KEY),
                never("ver04-no-key-edited", "Edit", r"devforgeai/handoff/[^\"]*", KEY),
                llm("ver04-choice-left-open", """
The user said they haven't decided between a --delimiter command-line flag and a delimiter setting in config.toml,
and that the choice is theirs.

Judge only the final reply.
PASS if the reply leaves that choice to the user (it may list both options as open, or say the next session must
ask), and doesn't say or imply that either option was chosen or is the plan.
FAIL if it presents either option as decided, chosen or planned."""),
            ],
        },
        {
            "name": "no-git", "ver": "VER-05", "git": False, "earlier": False,
            "description": "VER-05: in a project folder with no repository of its own (git's top level is a parent "
                           "repository), the handoff goes to the session's folder under devforgeai/handoff/no-git/, "
                           "section 2 says git couldn't be used, and the checker finds it clean.",
            "prompt": "This session added the header row to the CSV exporter in src/export.py (checkpoint 2 of "
                      "docs/plan.md); the delimiter option, checkpoint 3, is half done: the parameter exists, the "
                      "command-line flag doesn't. Prepare for /compact: write the handoff for the next session.",
            "graders": handoff_basics("VER-05", "devforgeai/handoff/no-git") + [
                wrote("ver05-section-2-says-git", session_file("devforgeai/handoff/no-git", r"START-HERE\.md"),
                      section(2, r"\b[Gg]it\b")),
                llm("ver05-says-git-not-used", """
The workspace's project folder has no git repository of its own; git finds only a repository in a parent folder,
which isn't this project's.

Judge only the final reply.
PASS if the reply says git couldn't be used for this project (no repository of its own, or the repository git found
belongs to a parent folder) and that the handoff was written under devforgeai/handoff/no-git/.
FAIL if it reports a branch or commits of the parent repository as this project's, or doesn't mention the
no-git folder."""),
            ],
        },
        {
            "name": "leaves-other-session-handoff", "ver": "VER-10", "git": True, "earlier": False, "other": True,
            "description": "VER-10: another session's handoff of other work on the same branch stays unchanged; the "
                           "skill writes its own folder beside it, names the other under Other handoffs, takes over "
                           "none of its decisions, and passes its session to the checker.",
            "prompt": STORY + " Another session is working on this branch too, on paginating the reports page; that "
                              "is its work, and this session never touched or read it. Prepare for /compact: write "
                              "the handoff for the next session.",
            "graders": handoff_basics("VER-10", HANDOFF) + [
                never("ver10-no-write-in-other-folder", "Write", rf"{OTHER}/[^\"]*"),
                never("ver10-no-edit-in-other-folder", "Edit", rf"{OTHER}/[^\"]*"),
                regex("ver10-other-start-here-same-session", rf"by session {OTHER_SESSION}$",
                      target=f"{OTHER}/START-HERE.md", flags="m"),
                regex("ver10-other-start-here-unchanged", r"^1\. Page links\. Next: add the previous and next links",
                      target=f"{OTHER}/START-HERE.md", flags="m"),
                regex("ver10-other-start-here-holds-no-export-work", r"newline=|[Hh]eader row|[Dd]elimiter",
                      target=f"{OTHER}/START-HERE.md", match="not_contains"),
                regex("ver10-other-tasks-unchanged", r"^- \[ \] Page links\. Next: add the previous and next links",
                      target=f"{OTHER}/TASKS.md", flags="m"),
                regex("ver10-other-tasks-hold-no-export-work", r"[Hh]eader row|[Dd]elimiter|[Ee]xporter",
                      target=f"{OTHER}/TASKS.md", match="not_contains"),
                regex("ver10-other-resume-unchanged", r"^Continue the report pagination in\s",
                      target=f"{OTHER}/RESUME-PROMPT.md", flags="m"),
                wrote("ver10-names-the-other-handoff", START,
                      rf"Other handoffs on this branch:{LINE}{OTHER_SESSION}"),
                never("ver10-other-decision-not-taken", "Write", START,
                      rf"### Decided(?:(?!{NL}###? )[\s\S])*?50 rows per page"),
            ],
        },
    ]


START = session_file(HANDOFF, r"START-HERE\.md")
TASKS = session_file(HANDOFF, r"TASKS\.md")

TRIGGERS = [
    (True, "I'm at 75% context: save what we learned and write a handoff before I compact."),
    (True, "Write a start-here document and a resume prompt for the next session after /compact."),
    (True, "Prepare for /compact."),
    (False, "Summarize what we did so far in this conversation."),
    (False, "Save this to memory: I prefer tabs."),
    (False, "Create a TASKS.md listing this feature's backlog."),
    (False, "How does /compact work?"),
    (False, "Update the README with what changed."),
]


def prompt_md(description, tags, limits, prompt):
    return (f'---\ndescription: "{description}"\ntags: [{", ".join(tags)}]\nmax_turns: {limits[0]}\n'
            f"timeout_seconds: {limits[1]}\nallowed_tools: {TOOLS}\n---\n{prompt}\n")


def case_yaml(name, scaffold):
    text = f'schema_version: "1.1"\nname: {name}\n'
    return text + ("context:\n  scaffold_script: scaffold.sh\n" if scaffold else "")


def scaffold_for(c):
    lines = project(git=c["git"]) + (earlier_handoff() if c["earlier"] else []) \
        + (other_handoff() if c.get("other") else [])
    return scaffold_script(c["ver"], c["name"], lines, c["git"])


# --------------------------------------------------------------------------------------------------------
# Premise checks, then writing

CLEAN_GIT = {"GIT_CONFIG_NOSYSTEM": "1", "GIT_CONFIG_GLOBAL": os.devnull}


def run(cmd, cwd, **kw):
    env = dict(os.environ, **CLEAN_GIT, **kw.pop("env", {}))
    return subprocess.run(cmd, cwd=cwd, env=env, capture_output=True, text=True, **kw)


def build(c, folder):
    script = Path(folder) / "scaffold.sh"
    script.write_text(scaffold_for(c))
    p = run(["bash", str(script)], folder)
    script.unlink()
    if p.returncode:
        sys.exit(f"{c['name']}: scaffold failed:\n{p.stderr}")


def check_premise(c):
    """Build the case in a temporary folder and check what its prompt and graders assume. Returns the head hash."""
    with tempfile.TemporaryDirectory() as tmp:
        if not c["git"]:
            # The eval workspace is home/cwd, and home/ is a git repository: so is this parent.
            parent = Path(tmp)
            run(["git", "init", "-q"], parent, check=True)
            cwd = parent / "cwd"
            cwd.mkdir()
            build(c, cwd)
            top = run(["git", "rev-parse", "--show-toplevel"], cwd).stdout.strip()
            if Path(top).resolve() != parent.resolve():
                sys.exit(f"{c['name']}: git's top level is {top!r}, not the parent repository")
            return None
        (Path(tmp) / "STRAY.md").write_text("a file the workspace held before the scaffold ran\n")
        build(c, tmp)
        if "STRAY.md" in run(["git", "ls-files"], tmp).stdout:
            sys.exit(f"{c['name']}: a file the scaffold didn't write was committed")
        branch = run(["git", "branch", "--show-current"], tmp).stdout.strip()
        log = run(["git", "log", "--format=%s"], tmp).stdout.split("\n")
        status = run(["git", "status", "--porcelain"], tmp).stdout
        if branch != "feat/export" or log[0] != "Add the header row" or " M src/export.py" not in status:
            sys.exit(f"{c['name']}: unexpected repository: {branch!r} {log[:3]} {status!r}")
        if c["earlier"]:
            p = run([sys.executable, "-S", "-B", str(CHECK), "--root", tmp, HANDOFF], tmp)
            if p.returncode != 0 or "handoff: clean" not in p.stdout:
                sys.exit(f"{c['name']}: the earlier handoff isn't clean:\n{p.stdout}{p.stderr}")
        if c.get("other"):
            p = run([sys.executable, "-S", "-B", str(CHECK), "--root", tmp, "--session", OTHER_SESSION, OTHER], tmp)
            if p.returncode != 0 or "handoff: clean" not in p.stdout:
                sys.exit(f"{c['name']}: the other session's handoff isn't clean:\n{p.stdout}{p.stderr}")
        return run(["git", "rev-parse", "HEAD"], tmp).stdout.strip()[:7]


def all_cases():
    drafts = cases({"writes-handoff": "HEAD"})
    hashes = {c["name"]: check_premise(c) for c in drafts}
    out = []
    for c in cases(hashes):
        ver_tag = "ver-" + c["ver"].split("-")[1]
        out.append({"name": c["name"], "scaffold": scaffold_for(c),
                    "prompt.md": prompt_md(c["description"], ["precompact", ver_tag], CASE_LIMITS, c["prompt"]),
                    "graders": c["graders"]})
    for n, (positive, prompt) in enumerate(TRIGGERS, 1):
        kind = "positive" if positive else "negative"
        description = f"VER-06 ({kind}): the skill {'fires' if positive else 'does not fire'}."
        grader = (tool_used("ver06-skill-fired", "Skill", SKILL_MATCH, minimum=1, arm="both") if positive else
                  tool_used("ver06-skill-not-fired", "Skill", SKILL_MATCH, minimum=0, maximum=0, arm="both"))
        out.append({"name": f"precompact-trigger-{n:02d}", "scaffold": None,
                    "prompt.md": prompt_md(description, ["trigger", "ver-06", "precompact-trigger"], SHORT_LIMITS,
                                           prompt),
                    "graders": [grader]})
    return out, hashes


def main():
    out, hashes = all_cases()
    if OUT.exists():
        shutil.rmtree(OUT)
    for case in out:
        folder = OUT / case["name"]
        (folder / "graders").mkdir(parents=True)
        (folder / "case.yaml").write_text(case_yaml(case["name"], case["scaffold"] is not None))
        (folder / "prompt.md").write_text(case["prompt.md"])
        if case["scaffold"]:
            script = folder / "scaffold.sh"
            script.write_text(case["scaffold"])
            script.chmod(0o755)
        for name, body in case["graders"]:
            (folder / "graders" / f"{name}.md").write_text(body)
    print(f"wrote {len(out)} cases under {OUT.relative_to(REPO)}; feat/export head {hashes['writes-handoff']}")


if __name__ == "__main__":
    main()
