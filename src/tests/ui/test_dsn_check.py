"""Unit tests for the ui skill's checker, scripts/dsn_check.py (SPEC-017 VER-23 and VER-24; IF-01 to IF-04, QR-05).

Each case builds a project folder in a temporary directory and runs the script as a subprocess three ways, which must
agree byte for byte on the exit code and standard output, and print nothing on standard error:
- `python3 -B SCRIPT`: this interpreter's packages, so PyYAML (when installed) adds its YAML syntax cross-check;
- `python3 -B -S SCRIPT`: `-S` hides every site-packages directory, as a machine without PyYAML would;
- `python3 -B -S -c GUARD SCRIPT`: the same under an audit hook (QR-05) that makes opening a socket, starting a
  process, any write, rename or delete, and opening a path in the case's forbid list fail.
After each run the whole temporary tree (modes, sizes, times, bytes, link targets) must equal what it was before.

Readings this test pins where SPEC-017 leaves a choice (listed for Bryan in the build report):
- the `head` trailer's `<n> lines cut` is the number of lines left out (lines - shown), as VER-23 says "the trailer
  says 250 lines left out"; a shortened line shows `[cut]` on the line, and `bytes shown` is the bytes of the
  file actually printed (a shortened line counts its first 500 characters). The whole output stays within 16384 bytes;
- `pending boards folders` lists every DSN-NNN folder without a DSN-NNN.md (the definition in section 4), including
  one at the next free number;
- a board name holding `..` anywhere, or equal to `.`, is refused (ERR-06's text says "holds .."), not only `..`;
- `check --before-amend` prints both the suspect-link `warning:` and the `fact: links:` line;
- `board <k>` in the `boards` output counts from 1, and "1 boards" is not pluralised (the literal section 5 text);
- exit 2 is for arguments, an unreadable root, a missing DSN file and a BRN that cannot be read; a boards folder
  that cannot be used is one `boards` error in the full check, and exit 2 in `--before-amend` and `head`;
- a symbolic link is refused (never followed) for a board file, for canvas.json, for the boards folder and for the
  DSN document itself;
- `<part>` is a frontmatter key, `BRD-NN`, `upstream`, `section 3`, `Change Log`, `canvas.json`, `marker` or
  `document`; warnings print as `warning: <file>:<line>: <part>: <message> (<rule>)`, after the errors, then the facts.

Run from the repository root:
    python3 -B src/tests/ui/test_dsn_check.py
"""
import hashlib
import json
import os
import re
import shutil
import stat
import subprocess
import sys
import tempfile
import unittest
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
SCRIPT = ROOT / "src/claude/DevForgeAI/skills/ui/scripts/dsn_check.py"
FILE = "docs/specs/design/DSN-001.md"
FOLDER = "docs/specs/design/DSN-001/boards/"
MAX_OUTPUT = 16 * 1024


def _has_yaml(flags):
    return subprocess.run([sys.executable, *flags, "-c", "import yaml"], capture_output=True).returncode == 0


# --- The guard: an audit hook that makes everything the script must never do fail (QR-05) ----------------------
GUARD = r'''
import os, runpy, sys

FORBID = {os.path.abspath(p) for p in os.environ.get("DSN_GUARD_FORBID", "").split(os.pathsep) if p}
WRITE_FLAGS = os.O_WRONLY | os.O_RDWR | os.O_CREAT | os.O_TRUNC | os.O_APPEND
# Audit events that mean a connection, a new process, or a change to the file system.
DENIED = ("socket.", "subprocess.", "urllib.", "http.client.", "shutil.", "tempfile.") + tuple(
    "os." + name for name in ("system", "exec", "posix_spawn", "spawn", "fork", "forkpty", "mkdir", "rename",
                              "replace", "remove", "rmdir", "chmod", "chown", "symlink", "link", "truncate",
                              "utime", "mkfifo", "mknod"))


class Violation(BaseException):
    """BaseException, so that a broad `except Exception` in the script cannot swallow it."""


def hook(event, args):
    if event.startswith(DENIED):
        raise Violation(event)
    if event == "open":
        path, _mode, flags = args
        if isinstance(flags, int) and flags & WRITE_FLAGS:
            raise Violation("open for writing: %r" % (path,))
        if isinstance(path, (str, bytes)) and os.path.abspath(os.fsdecode(path)) in FORBID:
            raise Violation("open of a forbidden path: %r" % (path,))


script, args = sys.argv[1], sys.argv[2:]
sys.argv = [script] + args
sys.addaudithook(hook)
try:
    runpy.run_path(script, run_name="__main__")
except SystemExit as e:
    sys.stdout.flush()
    sys.exit(e.code)
except Violation as v:
    print("GUARD: " + str(v), file=sys.stderr)
    sys.exit(97)
'''

ARMS = [("plain", ["-B", str(SCRIPT)]), ("-S", ["-B", "-S", str(SCRIPT)]),
        ("guarded", ["-B", "-S", "-c", GUARD, str(SCRIPT)])]


class Result:
    def __init__(self, code, raw):
        self.code = code
        self.raw = raw
        self.out = raw.decode("utf-8", "replace")
        self.lines = self.out.split("\n")[:-1] if self.out.endswith("\n") else self.out.split("\n")

    def __repr__(self):
        return f"exit {self.code}\n{self.out}"


def run_arms(args, cwd, forbid=()):
    """Run the script in the three ways; they must agree and print nothing on stderr (so no traceback)."""
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1", DSN_GUARD_FORBID=os.pathsep.join(str(p) for p in forbid))

    def one(arm):
        return subprocess.run([sys.executable, *arm[1], *args], cwd=cwd, env=env, capture_output=True, timeout=120)

    with ThreadPoolExecutor(len(ARMS)) as pool:
        procs = list(pool.map(one, ARMS))
    for (name, _), p in zip(ARMS, procs):
        assert p.stderr == b"", f"{name}: stderr was not empty:\n{p.stderr.decode('utf-8', 'replace')}"
    first = procs[0]
    for (name, _), p in zip(ARMS, procs):
        assert (p.returncode, p.stdout) == (first.returncode, first.stdout), (
            f"the arms disagree ({name}):\n{first.returncode}\n{first.stdout.decode('utf-8', 'replace')}\n--\n"
            f"{p.returncode}\n{p.stdout.decode('utf-8', 'replace')}")
    return Result(first.returncode, first.stdout)


def snapshot(top):
    """Every path under top, without following links: kind, mode, size, mtime, bytes (None if unreadable), target."""
    snap = {}
    for dirpath, dirnames, filenames in os.walk(top, followlinks=False):
        for name in dirnames + filenames:
            p = os.path.join(dirpath, name)
            st = os.lstat(p)
            entry = [stat.S_IFMT(st.st_mode), stat.S_IMODE(st.st_mode), st.st_size, st.st_mtime_ns]
            if stat.S_ISLNK(st.st_mode):
                entry.append(os.readlink(p))
            elif stat.S_ISREG(st.st_mode):
                try:
                    with open(p, "rb") as f:
                        entry.append(f.read())
                except OSError:
                    entry.append(None)
            snap[os.path.relpath(p, top)] = tuple(entry)
    return snap


def sha256(data):
    return hashlib.sha256(data).hexdigest()


def count_lines(data):
    return data.count(b"\n") + (1 if data and not data.endswith(b"\n") else 0)


def edit(text, old, new, count=1):
    assert text.count(old) == count, f"fixture has {text.count(old)} of {old!r}, wanted {count}"
    return text.replace(old, new)


def line_of(text, needle, nth=1):
    """The 1-based number of the nth line holding needle."""
    seen = 0
    for i, line in enumerate(text.split("\n"), 1):
        if needle in line:
            seen += 1
            if seen == nth:
                return i
    raise AssertionError(f"no line holds {needle!r}")


def _item_span(text, brd):
    start = text.index(f"  - id: {brd}\n")
    fence = text.index("\n```", start)
    nxt = text.find("\n  - id: ", start + 1)
    return start, (fence if nxt < 0 or nxt > fence else nxt)


def set_field(text, brd, field, value):
    """Replace one field of one board item in the boards block."""
    start, end = _item_span(text, brd)
    block, n = re.subn(rf"(?m)^    {field}:.*$", lambda m: f"    {field}: {value}", text[start:end])
    assert n == 1, (brd, field, n)
    return text[:start] + block + text[end:]


def drop_field(text, brd, field):
    start, end = _item_span(text, brd)
    block, n = re.subn(rf"(?m)^    {field}:.*\n?", "", text[start:end])
    assert n == 1, (brd, field, n)
    return text[:start] + block + text[end:]


def add_field(text, brd, line):
    _, end = _item_span(text, brd)
    return text[:end] + f"\n    {line}" + text[end:]


def add_item(text, item):
    """Append a board item (lines, no trailing newline) at the end of the boards block."""
    end = text.index("\n```", text.index("```yaml items"))
    return text[:end] + "\n" + item + text[end:]


# --- Fixtures: the shared fixture of SPEC-017 section 9 (Shiftlog, four boards) --------------------------------
BOARDS = {
    "Home.dc.html": "<!doctype html>\n<title>Home</title>\n<h1>Home</h1>\n<p>Today's shifts and a link to the report.</p>\n",
    "List.dc.html": "<!doctype html>\n<title>List</title>\n<pre>$ shiftlog list\n2026-10-09  08:00  12:00  4h</pre>\n",
    "Add.dc.html": "<!doctype html>\n<title>Add</title>\n<pre>$ shiftlog add\nStart? 08:00\nEnd? 12:00</pre>\n",
    "Report.dc.html": "<!doctype html>\n<title>Report</title>\n<h2>Weekly report</h2>\n<table></table>\n",
}
SETTINGS = "<!doctype html>\n<title>Settings</title>\n<h1>Settings</h1>\n<p>Retention period.</p>\n"

IDEAS = {
    "IDEA-01": ("Add a shift from the terminal", "promoted"),
    "IDEA-02": ("List shifts in a table", "promoted"),
    "IDEA-03": ("A weekly report page", "promoted"),
    "IDEA-04": ("Export shifts as CSV", "promoted"),
    "IDEA-05": ("Sync to a server", "parked"),
    "IDEA-06": ("A dark theme for the report page", "promoted"),
}


def brn_text(version=1, ideas=None, status="converged"):
    ideas = IDEAS if ideas is None else ideas
    items = []
    for iid, (text, disposition) in ideas.items():
        reason = "null" if disposition == "open" else '"Decided: it matters, a lot."'
        items.append(f'''  - id: {iid}
    status: active
    idea: "{text}"
    addresses:
      - PRB-01
    value: "high"
    effort: "low"
    risk: "low"
    score: 3
    disposition: {disposition}
    reason: {reason}
''')
    return f'''---
id: BRN-001
type: brainstorm
title: "Shiftlog: record shifts"
status: {status}
version: {version}
created: 2026-10-01
updated: 2026-10-01
owner: "Example Owner"
authors: ["Example Owner", "claude-code"]
reviewed_by: []
approved_by: ""
approved_on: null
upstream: []
supersedes: []
superseded_by: null
blocked_by: []
participants: ["Example Owner"]
sources: []
---

# BRN-001 — Shiftlog: record shifts

## 2. Problems

```yaml items
problems:
  - id: PRB-01
    status: active
    statement: "Shifts are hard to record: a paper log gets lost."
    who: "Part-time staff"
    evidence: "Interviews"
    severity: high
```

## 4. Ideas

```yaml items
ideas:
{"".join(items)}```

## Change Log

| Version | Date | Author | Change |
|---|---|---|---|
| 1 | 2026-10-01 | claude-code (session 0b6c1d2e-3f40-4a5b-8c7d-9e0f1a2b3c4d) | Initial draft |
'''


PRD = '''---
id: PRD-001
type: prd
title: "Shiftlog"
status: approved
version: 2
---

# PRD-001

## 6. Functional requirements

```yaml items
functional_requirements:
  - id: FR-023
    status: active
    statement: "The system shall record a shift."
    priority: must
    release: current
    notes: null
  - id: FR-024
    status: active
    statement: "The system shall let an administrator set the retention period on a settings screen."
    priority: should
    release: current
    notes: null
  - id: FR-025
    status: deprecated
    statement: "The system shall show a splash screen."
    priority: could
    release: later
    notes: null
```

## 7. Non-functional requirements

```yaml items
non_functional_requirements:
  - id: NFR-001
    category: usability
    status: active
    statement: "Every screen shall load within one second."
    priority: should
    release: current
```
'''


def adr_text(number, status="accepted", superseded_by="null"):
    return f'''---
id: ADR-{number:03d}
type: adr
title: "A decision"
status: {status}
version: 1
created: 2026-10-01
updated: 2026-10-01
owner: "Example Owner"
authors: ["Example Owner"]
upstream: []
supersedes: []
superseded_by: {superseded_by}
blocked_by: []
---

# ADR-{number:03d}
'''


CHANGE_ROW = ("| 1 | 2026-10-09 | claude-code (session 0b6c1d2e-3f40-4a5b-8c7d-9e0f1a2b3c4d) | "
              "Created from BRN-001 and the boards; 1 marker left | all |")
MARKER = "- [NEEDS CLARIFICATION: IDEA-06 has no board yet, so no screen shows it]"
IDEA01_LINK = "  - {id: BRN-001, item: IDEA-01, relation: derives, version: 1, hash: null}\n"

BASE = f'''---
id: DSN-001
type: design
title: "Shiftlog: record shifts: release design"
status: draft          # draft | in-review | approved | superseded | deprecated
version: 1
created: 2026-10-09
updated: 2026-10-09
owner: "Example Owner"
authors: ["Example Owner", "claude-code"]
generated_by:
  tool: "claude-code"
  model: "claude-sonnet-5-5"
  session: "0b6c1d2e-3f40-4a5b-8c7d-9e0f1a2b3c4d"
reviewed_by: []
approved_by: ""
approved_on: null
upstream:
  - {{id: BRN-001, relation: derives, version: 1, hash: null}}
{IDEA01_LINK}  - {{id: BRN-001, item: IDEA-02, relation: derives, version: 1, hash: null}}
  - {{id: BRN-001, item: IDEA-03, relation: derives, version: 1, hash: null}}
supersedes: []
superseded_by: null
blocked_by: []
# --- design-specific ---
canvas: "https://claude.ai/artifact/EXAMPLE"
canvas_version: "17-example"
canvas_format: 3
boards_root: "docs/specs/design/DSN-001/boards/"
considered: []
---

# DSN-001 — Shiftlog: record shifts: release design

## 1. Scope

Shiftlog records shifts. The design covers the report-and-home flow on the web and the shifts flow in a terminal.

## 2. Boards

```yaml items
boards:
  - id: BRD-01
    status: active
    file: "Home.dc.html"
    title: "Home"
    flow: "report-and-home"
    surface: "web"
    ideas: ["IDEA-02"]
    answers: []
    sha256: "@Home.dc.html@"
    notes: null
  - id: BRD-02
    status: active
    file: "List.dc.html"
    title: "List"
    flow: "shifts"
    surface: "terminal"
    ideas: ["IDEA-02"]
    answers: []
    sha256: "@List.dc.html@"
    notes: null
  - id: BRD-03
    status: active
    file: "Add.dc.html"
    title: "Add"
    flow: "shifts"
    surface: "terminal"
    ideas: ["IDEA-01"]
    answers: []
    sha256: "@Add.dc.html@"
    notes: null
  - id: BRD-04
    status: active
    file: "Report.dc.html"
    title: "Report"
    flow: "report-and-home"
    surface: "web"
    ideas: ["IDEA-03"]
    answers: []
    sha256: "@Report.dc.html@"
    notes: null
```

## 3. Idea coverage

| Idea | Boards | Status |
|---|---|---|
| IDEA-01 | BRD-03 | designed |
| IDEA-02 | BRD-01, BRD-02 | designed |
| IDEA-03 | BRD-04 | designed |
| IDEA-04 | none | not a screen |
| IDEA-06 | none | no board yet |

## 4. Canvas

Copied from https://claude.ai/artifact/EXAMPLE, version 17-example. A new copy of the boards means a new run, which
amends this document.

## 5. Open questions

{MARKER}

## Change Log

| Version | Date | Author | Change | Items affected |
|---|---|---|---|---|
{CHANGE_ROW}
'''

# A DSN whose mappings are all unconfirmed (VER-03): every field null with a marker, no canvas facts.
NULL_DSN = '''---
id: DSN-001
type: design
title: "Shiftlog: record shifts: release design"
status: draft
version: 1
created: 2026-10-09
updated: 2026-10-09
owner: "Example Owner"
authors: ["Example Owner", "claude-code"]
generated_by:
  tool: "claude-code"
  model: "claude-sonnet-5-5"
  session: "0b6c1d2e-3f40-4a5b-8c7d-9e0f1a2b3c4d"
reviewed_by: []
approved_by: ""
approved_on: null
upstream:
  - {id: BRN-001, relation: derives, version: 1, hash: null}
supersedes: []
superseded_by: null
blocked_by: []
# --- design-specific ---
canvas: null
canvas_version: null
canvas_format: 3
boards_root: docs/specs/design/DSN-001/boards/
considered: []
---

# DSN-001 — Shiftlog: record shifts: release design

## 1. Scope

Shiftlog records shifts.

## 2. Boards

```yaml items
boards:
@ITEMS@```

## 3. Idea coverage

| Idea | Boards | Status |
|---|---|---|
| IDEA-01 | none | no board yet |
| IDEA-02 | none | no board yet |
| IDEA-03 | none | no board yet |
| IDEA-04 | none | no board yet |
| IDEA-06 | none | no board yet |

## 4. Canvas

- [NEEDS CLARIFICATION: canvas URL and version copied]

## 5. Open questions

- [NEEDS CLARIFICATION: IDEA-01 has no board yet]
- [NEEDS CLARIFICATION: IDEA-02 has no board yet]
- [NEEDS CLARIFICATION: IDEA-03 has no board yet]
- [NEEDS CLARIFICATION: IDEA-04 has no board yet]
- [NEEDS CLARIFICATION: IDEA-06 has no board yet]

## Change Log

| Version | Date | Author | Change | Items affected |
|---|---|---|---|---|
| 1 | 2026-10-09 | claude-code (session 0b6c1d2e-3f40-4a5b-8c7d-9e0f1a2b3c4d) | Created; 6 markers left | all |
'''
NULL_ITEM = '''  - id: BRD-0{n}
    status: active
    file: "{file}"
    title: "{title}"
    flow: null
    surface: null
    ideas: null
    answers: []
    sha256: "@{file}@"
    notes: "[NEEDS CLARIFICATION: flow, surface and ideas of the {title} screen]"
'''


class Project:
    """A temporary project folder (`root`) beside an `elsewhere` folder, with helpers to seed it."""

    def __init__(self):
        self.tmp = Path(tempfile.mkdtemp(prefix="dsn-check-"))
        self.root = self.tmp / "project"
        self.root.mkdir()
        self.elsewhere = self.tmp / "elsewhere"
        self.elsewhere.mkdir()
        self.boards = dict(BOARDS)

    def cleanup(self):
        for dirpath, dirnames, filenames in os.walk(self.tmp):
            for name in dirnames:
                os.chmod(os.path.join(dirpath, name), 0o755)
        shutil.rmtree(self.tmp, ignore_errors=True)

    def path(self, rel):
        return self.root / rel

    def put(self, rel, content):
        p = self.path(rel)
        p.parent.mkdir(parents=True, exist_ok=True)
        if isinstance(content, str):
            content = content.encode("utf-8")
        p.write_bytes(content)
        return p

    def boards_dir(self, dsn="DSN-001"):
        return self.path(f"docs/specs/design/{dsn}/boards")

    def write_canvas(self, canvas=None, dsn="DSN-001"):
        if canvas is None:
            canvas = {"v": 3, "attachments": {}, "boards": {name: {"expand": False, "h": 480} for name in self.boards}}
        self.put(f"docs/specs/design/{dsn}/boards/canvas.json", json.dumps(canvas))

    def write_boards(self, dsn="DSN-001"):
        for name, content in self.boards.items():
            self.put(f"docs/specs/design/{dsn}/boards/{name}", content)
        self.write_canvas(dsn=dsn)

    def add_board(self, name, content, dsn="DSN-001"):
        """Add a board file (str or bytes) to the folder and to canvas.json, at the end."""
        self.boards[name] = content
        self.put(f"docs/specs/design/{dsn}/boards/{name}", content)
        canvas = json.loads(self.boards_dir(dsn).joinpath("canvas.json").read_text())
        canvas["boards"][name] = {"expand": False, "h": 480}
        self.write_canvas(canvas, dsn)

    def remove_board(self, name, dsn="DSN-001"):
        self.boards.pop(name, None)
        (self.boards_dir(dsn) / name).unlink()
        canvas = json.loads(self.boards_dir(dsn).joinpath("canvas.json").read_text())
        del canvas["boards"][name]
        self.write_canvas(canvas, dsn)

    def digest(self, name, dsn="DSN-001"):
        return sha256((self.boards_dir(dsn) / name).read_bytes())

    def render(self, text, dsn="DSN-001"):
        """Fill the @file@ digest placeholders of a fixture text from the files on disk."""
        for name in re.findall(r"@([\w.-]+\.html)@", text):
            text = text.replace(f"@{name}@", self.digest(name, dsn))
        return text

    def write_brn(self, **kw):
        self.put("docs/specs/brainstorm/BRN-001.md", brn_text(**kw))

    def write_dsn(self, text, dsn="DSN-001"):
        return self.put(f"docs/specs/design/{dsn}.md", self.render(text, dsn))

    def shared(self):
        """BRN-001, the four boards, the PRD and an ADR the cases read."""
        self.write_brn()
        self.write_boards()
        self.put("docs/specs/prd/PRD-001.md", PRD)
        self.put("docs/specs/adr/ADR-009.md", adr_text(9))


class Base(unittest.TestCase):
    def setUp(self):
        self.p = Project()
        self.addCleanup(self.p.cleanup)

    def cli(self, *args, root=True, forbid=(), cwd=None):
        """Run the script with --root set to the project (or not) and check that it changed nothing."""
        argv = list(args)
        if root:
            argv[1:1] = ["--root", str(self.p.root)]
        before = snapshot(self.p.tmp)
        r = run_arms(argv, cwd or self.p.elsewhere, forbid)
        self.assertEqual(snapshot(self.p.tmp), before, "the script changed the folder")
        return r


class Arms(unittest.TestCase):
    def test_the_plain_arm_has_pyyaml_and_the_s_arm_does_not(self):
        if not _has_yaml([]):
            self.skipTest("PyYAML is not installed for this interpreter: only the no-PyYAML path is exercised")
        if _has_yaml(["-S"]):
            self.skipTest("PyYAML is importable even with -S")
        self.assertTrue(_has_yaml([]))
        self.assertFalse(_has_yaml(["-S"]))


# =====================================================================================================================
# Arguments: exit 2 with `Cannot run: <reason>.` and nothing else (VER-23, section 5)
# =====================================================================================================================
class CannotRun(Base):
    def assert_cannot_run(self, r):
        self.assertEqual(r.code, 2, r)
        self.assertEqual(len(r.lines), 1, r)
        self.assertRegex(r.lines[0], r"^Cannot run: \S.*\.$")

    def test_no_arguments(self):
        self.assert_cannot_run(self.cli(root=False))

    def test_an_unknown_subcommand(self):
        self.assert_cannot_run(self.cli("frobnicate"))

    def test_an_unknown_option(self):
        for argv in (("next", "--frobnicate"), ("boards", "DSN-001", "--frobnicate"), ("check", "-x", "DSN-001")):
            with self.subTest(argv=argv):
                self.assert_cannot_run(self.cli(*argv))

    def test_a_missing_root_value(self):
        for argv in (["next", "--root"], ["boards", "DSN-001", "--root"], ["next", "--root", "--before-amend"]):
            with self.subTest(argv=argv):
                self.assert_cannot_run(self.cli(*argv, root=False))

    def test_a_root_that_does_not_exist_or_is_not_a_folder(self):
        self.p.put("a-file", "x")
        for root in (str(self.p.tmp / "no-such-folder"), str(self.p.path("a-file"))):
            with self.subTest(root=root):
                self.assert_cannot_run(self.cli("next", "--root", root, root=False))

    def test_a_repeated_root(self):
        self.assert_cannot_run(self.cli("next", "--root", str(self.p.root), "--root", str(self.p.root), root=False))

    def test_a_dsn_id_that_is_not_one(self):
        for bad in ("DSN-1", "dsn-001", "DSN-0001", "DSN-001.md", "../DSN-001", "BRN-001", ""):
            for sub in ("boards", "check"):
                with self.subTest(sub=sub, bad=bad):
                    self.assert_cannot_run(self.cli(sub, bad))

    def test_a_missing_dsn_id(self):
        for sub in ("boards", "check", "head"):
            with self.subTest(sub=sub):
                self.assert_cannot_run(self.cli(sub))

    def test_too_many_or_too_few_positionals(self):
        self.assert_cannot_run(self.cli("next", "DSN-001"))
        self.assert_cannot_run(self.cli("boards", "DSN-001", "extra"))
        self.assert_cannot_run(self.cli("check", "DSN-001", "extra"))
        self.assert_cannot_run(self.cli("head", "DSN-001"))
        self.assert_cannot_run(self.cli("head", "DSN-001", "a", "b"))

    def test_before_amend_belongs_to_check(self):
        for argv in (("next", "--before-amend"), ("boards", "--before-amend", "DSN-001"),
                     ("head", "--before-amend", "DSN-001", "Home.dc.html")):
            with self.subTest(argv=argv):
                self.assert_cannot_run(self.cli(*argv))

    def test_check_of_a_missing_dsn_file_cannot_run(self):
        self.p.shared()
        self.assert_cannot_run(self.cli("check", "DSN-001"))
        self.assert_cannot_run(self.cli("check", "--before-amend", "DSN-001"))


# =====================================================================================================================
# IF-01 next (VER-23)
# =====================================================================================================================
class Next(Base):
    def test_no_design_folder(self):
        r = self.cli("next")
        self.assertEqual((r.code, r.lines), (0, ["next: DSN-001", "pending boards folders: none"]), r)

    def test_an_empty_design_folder(self):
        self.p.path("docs/specs/design").mkdir(parents=True)
        r = self.cli("next")
        self.assertEqual((r.code, r.lines), (0, ["next: DSN-001", "pending boards folders: none"]), r)

    def test_one_more_than_the_highest(self):
        self.p.put("docs/specs/design/DSN-001.md", "x")
        self.p.put("docs/specs/design/DSN-003.md", "x")
        r = self.cli("next")
        self.assertEqual((r.code, r.lines), (0, ["next: DSN-004", "pending boards folders: none"]), r)

    def test_a_deprecated_dsn_counts(self):
        self.p.put("docs/specs/design/DSN-001.md", BASE.replace("status: draft ", "status: deprecated "))
        self.p.put("docs/specs/design/DSN-002.md", BASE.replace("status: draft ", "status: superseded "))
        r = self.cli("next")
        self.assertEqual(r.lines[0], "next: DSN-003", r)

    def test_a_boards_folder_with_no_document_is_pending(self):
        self.p.put("docs/specs/design/DSN-001.md", "x")
        self.p.put("docs/specs/design/DSN-001/boards/canvas.json", "{}")
        self.p.put("docs/specs/design/DSN-005/boards/canvas.json", "{}")
        r = self.cli("next")
        self.assertEqual((r.code, r.lines), (0, ["next: DSN-002", "pending boards folders: DSN-005"]), r)

    def test_pending_folders_are_listed_in_order_and_include_the_next_number(self):
        self.p.put("docs/specs/design/DSN-001.md", "x")
        for n in ("DSN-004", "DSN-002", "DSN-009"):
            self.p.put(f"docs/specs/design/{n}/boards/canvas.json", "{}")
        r = self.cli("next")
        self.assertEqual(r.lines, ["next: DSN-002", "pending boards folders: DSN-002, DSN-004, DSN-009"], r)

    def test_other_names_are_ignored(self):
        self.p.put("docs/specs/design/DSN-002.md", "x")
        for name in ("DSN-010-draft.md", "DSN-9.md", "DSN-0003.md", "README.md", "DSN-007.txt", "notes/x.md"):
            self.p.put(f"docs/specs/design/{name}", "x")
        self.p.path("docs/specs/design/DSN-008.md.d").mkdir()
        r = self.cli("next")
        self.assertEqual(r.lines, ["next: DSN-003", "pending boards folders: none"], r)

    def test_it_reads_names_only(self):
        self.p.put("docs/specs/design/DSN-001.md", "x")
        self.p.put("docs/specs/design/DSN-002.md", "x")
        self.p.put("docs/specs/design/DSN-002/boards/canvas.json", "{}")
        forbid = [self.p.path("docs/specs/design/DSN-001.md"), self.p.path("docs/specs/design/DSN-002.md"),
                  self.p.path("docs/specs/design/DSN-002/boards/canvas.json")]
        r = self.cli("next", forbid=forbid)
        self.assertEqual(r.lines[0], "next: DSN-003", r)

    def test_the_default_root_is_the_working_folder(self):
        self.p.put("docs/specs/design/DSN-004.md", "x")
        r = self.cli("next", root=False, cwd=self.p.root)
        self.assertEqual(r.lines[0], "next: DSN-005", r)

    def test_a_trailing_root_option_is_accepted(self):
        self.p.put("docs/specs/design/DSN-004.md", "x")
        r = self.cli("next", "--root", str(self.p.root), root=False)
        self.assertEqual(r.lines[0], "next: DSN-005", r)

    def test_the_numbers_are_used_up(self):
        self.p.put("docs/specs/design/DSN-999.md", "x")
        r = self.cli("next")
        self.assertEqual(r.code, 2, r)
        self.assertRegex(r.lines[0], r"^Cannot run: .*DSN-999.*\.$")


# =====================================================================================================================
# IF-02 boards (VER-23): DM-04, ERR-03 to ERR-06, ERR-12
# =====================================================================================================================
class Boards(Base):
    def setUp(self):
        super().setUp()
        self.p.write_boards()

    def canvas(self, content, dsn="DSN-001"):
        self.p.put(f"docs/specs/design/{dsn}/boards/canvas.json", content)

    def boards(self, dsn="DSN-001", **kw):
        return self.cli("boards", dsn, **kw)

    def assert_one_error(self, r, code, pattern):
        self.assertEqual(r.code, 1, r)
        self.assertEqual(len(r.lines), 2, r)
        self.assertRegex(r.lines[0], rf"^ERR-{code}: .*{pattern}")
        self.assertEqual(r.lines[1], "boards: 1 problem(s)")

    def test_a_valid_folder_of_four_boards(self):
        r = self.boards()
        expected = ["canvas.json: v3, 4 boards"]
        for k, name in enumerate(BOARDS, 1):
            data = (self.p.boards_dir() / name).read_bytes()
            expected.append(f"board {k} {name} {len(data)} {count_lines(data)} {hashlib.sha256(data).hexdigest()}")
        expected.append("boards: ok")
        self.assertEqual((r.code, r.lines), (0, expected), r)

    def test_the_order_is_canvas_order_not_alphabetical(self):
        self.canvas(json.dumps({"v": 3, "boards": {"Report.dc.html": {}, "Add.dc.html": {}, "Home.dc.html": {}}}))
        r = self.boards()
        self.assertEqual([l.split()[2] for l in r.lines[1:-1]], ["Report.dc.html", "Add.dc.html", "Home.dc.html"], r)
        self.assertEqual(r.lines[0], "canvas.json: v3, 3 boards")

    def test_line_counts(self):
        self.p.boards = {"A.html": "", "B.html": "x", "C.html": "x\ny", "D.html": "x\ny\n", "E.html": "x\r\ny\r\n"}
        self.p.write_boards()
        r = self.boards()
        counts = {l.split()[2]: (l.split()[3], l.split()[4]) for l in r.lines[1:-1]}
        self.assertEqual(counts, {"A.html": ("0", "0"), "B.html": ("1", "1"), "C.html": ("3", "2"),
                                  "D.html": ("4", "2"), "E.html": ("6", "2")}, r)

    def test_other_members_and_other_files_are_ignored(self):
        canvas = {"v": 3, "attachments": {"a": 1, "a2": 2}, "boards": {n: {"expand": True, "h": 1} for n in BOARDS},
                  "future": [1, 2, 3], "title": "x"}
        self.canvas(json.dumps(canvas))
        self.p.put("docs/specs/design/DSN-001/boards/README.md", "digests: not read")
        self.p.put("docs/specs/design/DSN-001/boards/notes.txt", "not named")
        forbid = [self.p.boards_dir() / "README.md", self.p.boards_dir() / "notes.txt"]
        r = self.boards(forbid=forbid)
        self.assertEqual((r.code, r.lines[0], r.lines[-1]), (0, "canvas.json: v3, 4 boards", "boards: ok"), r)

    def test_a_duplicate_key_in_an_ignored_member_is_ignored(self):
        self.canvas('{"v": 3, "attachments": {"a": 1, "a": 2}, "boards": {"Home.dc.html": {"h": 1, "h": 2}}}')
        r = self.boards()
        self.assertEqual((r.code, r.lines[0]), (0, "canvas.json: v3, 1 boards"), r)

    # --- ERR-03 ------------------------------------------------------------------------------------------------
    def test_err03_a_missing_folder(self):
        r = self.boards("DSN-002")
        self.assert_one_error(r, "03", re.escape("docs/specs/design/DSN-002/boards/"))

    def test_err03_an_empty_folder(self):
        shutil.rmtree(self.p.boards_dir())
        self.p.boards_dir().mkdir()
        self.assert_one_error(self.boards(), "03", re.escape(FOLDER))

    def test_err03_a_folder_without_canvas_json(self):
        (self.p.boards_dir() / "canvas.json").unlink()
        self.assert_one_error(self.boards(), "03", re.escape(FOLDER))

    def test_err03_an_empty_boards_object(self):
        self.canvas('{"v": 3, "boards": {}}')
        self.assert_one_error(self.boards(), "03", re.escape(FOLDER))

    def test_err03_canvas_json_that_is_not_a_regular_file(self):
        (self.p.boards_dir() / "canvas.json").unlink()
        (self.p.boards_dir() / "canvas.json").mkdir()
        self.assert_one_error(self.boards(), "03", re.escape(FOLDER))

    def test_err03_a_symbolic_link_as_canvas_json_is_not_followed(self):
        secret = self.p.elsewhere / "canvas.json"
        secret.write_text('{"v": 3, "boards": {"Home.dc.html": {}}}')
        (self.p.boards_dir() / "canvas.json").unlink()
        link = self.p.boards_dir() / "canvas.json"
        link.symlink_to(secret)
        r = self.boards(forbid=[link, secret])
        self.assert_one_error(r, "03", re.escape(FOLDER))

    def test_err03_a_boards_folder_that_is_a_symbolic_link_is_not_followed(self):
        real = self.p.elsewhere / "boards"
        shutil.copytree(self.p.boards_dir(), real)
        shutil.rmtree(self.p.boards_dir())
        self.p.boards_dir().symlink_to(real)
        r = self.boards(forbid=[real / "canvas.json", real / "Home.dc.html", self.p.boards_dir() / "canvas.json"])
        self.assert_one_error(r, "03", re.escape(FOLDER))

    # --- ERR-04 ------------------------------------------------------------------------------------------------
    def test_err04_forms_canvas_json_cannot_take(self):
        cases = {
            "invalid UTF-8": b'{"v": 3, "boards": {"Home.dc.html": {}}, "x": "\xff\xfe"}',
            "not JSON": b"not json {",
            "empty": b"",
            "an array": b'[{"v": 3}]',
            "a number": b"3",
            "a string": b'"canvas"',
            "null": b"null",
            "no boards member": b'{"v": 3}',
            "boards is a list": b'{"v": 3, "boards": ["Home.dc.html"]}',
            "boards is a string": b'{"v": 3, "boards": "Home.dc.html"}',
            "boards is null": b'{"v": 3, "boards": null}',
            "truncated": b'{"v": 3, "boards": {"Home.dc.html": {}',
            "NaN": b'{"v": NaN, "boards": {"Home.dc.html": {}}}',
        }
        for name, raw in cases.items():
            with self.subTest(name):
                self.canvas(raw)
                self.assert_one_error(self.boards(), "04", "")

    def test_err04_a_duplicate_key_in_boards(self):
        self.canvas('{"v": 3, "boards": {"Home.dc.html": {}, "List.dc.html": {}, "Home.dc.html": {}}}')
        r = self.boards()
        self.assert_one_error(r, "04", "Home.dc.html")
        self.assertRegex(r.lines[0], r"duplicate")

    def test_err04_a_duplicate_top_level_member(self):
        self.canvas('{"v": 4, "v": 3, "boards": {"Home.dc.html": {}}}')
        self.assert_one_error(self.boards(), "04", "")

    def test_err04_comes_before_err05(self):
        self.canvas('{"v": 4, "boards": []}')
        self.assert_one_error(self.boards(), "04", "")

    # --- ERR-05 ------------------------------------------------------------------------------------------------
    def test_err05_values_of_v_the_spec_does_not_support(self):
        cases = [("4", r"\b4\b"), ('"3"', r'"3"'), ("3.0", r"3\.0"), ("true", r"\btrue\b"), ("false", r"\bfalse\b"),
                 ("null", r"\bnull\b"), ("[3]", r"\[3\]"), ("2", r"\b2\b"), ("3.00", r"3\.00"), ("30", r"\b30\b")]
        for raw, shown in cases:
            with self.subTest(v=raw):
                self.canvas('{"v": %s, "boards": {"Home.dc.html": {}}}' % raw)
                r = self.boards()
                self.assert_one_error(r, "05", shown)
                self.assertRegex(r.lines[0], r"supported")

    def test_err05_a_missing_v(self):
        self.canvas('{"boards": {"Home.dc.html": {}}}')
        r = self.boards()
        self.assert_one_error(r, "05", "")
        self.assertRegex(r.lines[0], r"no v|missing")

    def test_err03_an_empty_boards_object_comes_before_err05(self):
        self.canvas('{"v": 4, "boards": {}}')
        self.assert_one_error(self.boards(), "03", re.escape(FOLDER))

    def test_err05_comes_before_err12(self):
        names = {f"b{n}.html": {} for n in range(100)}
        self.canvas(json.dumps({"v": 4, "boards": names}))
        self.assert_one_error(self.boards(), "05", r"\b4\b")

    # --- ERR-12 ------------------------------------------------------------------------------------------------
    def test_err12_one_hundred_boards(self):
        names = {f"b{n:03d}.html": {} for n in range(100)}
        self.canvas(json.dumps({"v": 3, "boards": names}))
        r = self.boards()
        self.assert_one_error(r, "12", "100")
        self.assertRegex(r.lines[0], r"99")

    def test_ninety_nine_boards_are_allowed(self):
        self.p.boards = {f"b{n:03d}.html": f"<title>{n}</title>\n" for n in range(99)}
        self.p.write_boards()
        r = self.boards()
        self.assertEqual((r.code, r.lines[0], r.lines[-1]), (0, "canvas.json: v3, 99 boards", "boards: ok"), r)

    # --- ERR-06 ------------------------------------------------------------------------------------------------
    def err06(self, r):
        """{k: (name as JSON, reason)} for the ERR-06 lines of a result, checking its closing line."""
        found = {}
        for line in r.lines[:-1]:
            m = re.match(r'^ERR-06: board (\d+) (".*"): (.+)$', line)
            self.assertIsNotNone(m, line)
            found[int(m.group(1))] = (m.group(2), m.group(3))
        self.assertEqual(r.lines[-1], f"boards: {len(found)} problem(s)", r)
        return found

    def test_err06_an_absent_file(self):
        (self.p.boards_dir() / "List.dc.html").unlink()
        r = self.boards()
        self.assertEqual(r.code, 1, r)
        found = self.err06(r)
        self.assertEqual(list(found), [2], r)
        self.assertEqual(found[2][0], '"List.dc.html"')
        self.assertRegex(found[2][1], r"absent|does not exist|missing")

    def test_err06_a_directory(self):
        (self.p.boards_dir() / "Add.dc.html").unlink()
        (self.p.boards_dir() / "Add.dc.html").mkdir()
        found = self.err06(self.boards())
        self.assertEqual(list(found), [3])
        self.assertRegex(found[3][1], r"regular file")

    def test_err06_a_symbolic_link_is_refused_and_its_target_is_never_read(self):
        target = self.p.elsewhere / "secret.html"
        target.write_text("<title>secret</title>\nSECRET-CONTENT\n")
        link = self.p.boards_dir() / "Home.dc.html"
        link.unlink()
        link.symlink_to(target)
        r = self.boards(forbid=[link, target])
        found = self.err06(r)
        self.assertEqual(list(found), [1])
        self.assertRegex(found[1][1], r"symbolic link")
        self.assertNotIn(sha256(target.read_bytes()), r.out)

    @unittest.skipIf(os.geteuid() == 0, "root can read a file with mode 000")
    def test_err06_an_unreadable_file(self):
        path = self.p.boards_dir() / "Report.dc.html"
        path.chmod(0)
        self.addCleanup(path.chmod, 0o644)
        found = self.err06(self.boards())
        self.assertEqual(list(found), [4])
        self.assertRegex(found[4][1], r"cannot be read|unreadable|permission")

    def test_err06_names_that_are_not_plain_file_names(self):
        self.p.put("docs/specs/design/outside.dc.html", "<title>outside</title>\n")
        for name in ("", ".", "..", "a/b", "a\\b", "../outside.dc.html", "x..y.html", "/etc/passwd"):
            with self.subTest(name=name):
                self.canvas(json.dumps({"v": 3, "boards": {"Home.dc.html": {}, name: {}}}))
                r = self.boards(forbid=[self.p.path("docs/specs/design/outside.dc.html")])
                found = self.err06(r)
                self.assertEqual(list(found), [2], r)
                self.assertEqual(found[2][0], json.dumps(name))
                self.assertRegex(found[2][1], r"plain file name")

    def test_err06_lists_every_failing_board(self):
        (self.p.boards_dir() / "Dir.dc.html").mkdir()
        (self.p.boards_dir() / "Link.dc.html").symlink_to(self.p.elsewhere / "nowhere")
        names = ["Home.dc.html", "Gone.dc.html", "Dir.dc.html", "Link.dc.html", "", "..", "a/b", "a\\b", "List.dc.html"]
        self.canvas(json.dumps({"v": 3, "boards": {n: {} for n in names}}))
        found = self.err06(self.boards())
        self.assertEqual(sorted(found), [2, 3, 4, 5, 6, 7, 8], found)
        self.assertEqual([found[k][0] for k in sorted(found)], [json.dumps(n) for n in names[1:8]])

    def test_a_failing_board_prints_none_of_the_good_lines(self):
        (self.p.boards_dir() / "List.dc.html").unlink()
        r = self.boards()
        self.assertFalse(any(l.startswith(("board ", "canvas.json")) for l in r.lines), r)


# =====================================================================================================================
# IF-04 head (VER-23)
# =====================================================================================================================
class Head(Base):
    def setUp(self):
        super().setUp()
        self.p.write_boards()

    def head(self, name, **kw):
        return self.cli("head", "DSN-001", name, **kw)

    def trailer(self, r):
        m = re.fullmatch(r"head: (\d+) of (\d+) lines, (\d+) of (\d+) bytes, (\d+) lines cut", r.lines[-1])
        self.assertIsNotNone(m, r.lines[-1])
        return tuple(int(x) for x in m.groups())

    def test_a_board_under_the_caps_prints_whole(self):
        lines = [f"<p>row {n:02d}: some text</p>" for n in range(1, 21)]
        data = ("\n".join(lines) + "\n").encode()
        self.p.add_board("Twenty.dc.html", data)
        r = self.head("Twenty.dc.html")
        self.assertEqual(r.code, 0, r)
        self.assertEqual(r.lines, lines + [f"head: 20 of 20 lines, {len(data)} of {len(data)} bytes, 0 lines cut"])

    def test_a_small_real_board_prints_whole(self):
        data = BOARDS["Home.dc.html"].encode()
        r = self.head("Home.dc.html")
        self.assertEqual(r.lines[:-1], BOARDS["Home.dc.html"].splitlines())
        self.assertEqual(r.lines[-1], f"head: 4 of 4 lines, {len(data)} of {len(data)} bytes, 0 lines cut")

    def test_a_board_of_400_lines_prints_150(self):
        lines = [f"line {n:03d} of the board" for n in range(1, 401)]
        data = ("\n".join(lines) + "\n").encode()
        self.p.add_board("Long.dc.html", data)
        r = self.head("Long.dc.html")
        shown = ("\n".join(lines[:150]) + "\n").encode()
        self.assertEqual(r.code, 0, r)
        self.assertEqual(r.lines[:-1], lines[:150])
        self.assertEqual(r.lines[-1], f"head: 150 of 400 lines, {len(shown)} of {len(data)} bytes, 250 lines cut")

    def test_a_two_megabyte_line_prints_500_characters_marked_cut(self):
        data = b"x" * (2 * 1024 * 1024) + b"\n"
        self.p.add_board("Minified.dc.html", data)
        r = self.head("Minified.dc.html")
        self.assertEqual(r.code, 0, r)
        self.assertEqual(len(r.lines), 2, r.out[:200])
        self.assertTrue(r.lines[0].endswith(" [cut]"), r.lines[0][-20:])
        self.assertEqual(r.lines[0][:-len(" [cut]")], "x" * 500)
        lines_shown, lines, bytes_shown, size, left_out = self.trailer(r)
        self.assertEqual((lines_shown, lines, size, left_out), (1, 1, len(data), 0))
        self.assertTrue(500 <= bytes_shown <= 501, bytes_shown)
        self.assertLess(len(r.raw), 1024)

    def test_a_long_line_in_a_short_file_is_cut_and_the_others_print_whole(self):
        lines = ["first", "second", "c" * 600, "fourth", "fifth"]
        data = ("\n".join(lines) + "\n").encode()
        self.p.add_board("Uneven.dc.html", data)
        r = self.head("Uneven.dc.html")
        self.assertEqual(r.lines[:2], ["first", "second"])
        self.assertEqual(r.lines[2], "c" * 500 + " [cut]")
        self.assertEqual(r.lines[3:5], ["fourth", "fifth"])
        shown_lines, total_lines, bytes_shown, size, left_out = self.trailer(r)
        self.assertEqual((shown_lines, total_lines, size, left_out), (5, 5, len(data), 0))
        self.assertLess(bytes_shown, size)

    def test_a_line_of_exactly_500_characters_is_not_cut(self):
        self.p.add_board("Exact.dc.html", "e" * 500 + "\n" + "f" * 501 + "\n")
        r = self.head("Exact.dc.html")
        self.assertEqual(r.lines[0], "e" * 500)
        self.assertEqual(r.lines[1], "f" * 500 + " [cut]")

    def test_the_output_never_exceeds_16_kb(self):
        lines = ["y" * 400 for _ in range(300)]
        self.p.add_board("Wide.dc.html", "\n".join(lines) + "\n")
        r = self.head("Wide.dc.html")
        self.assertLessEqual(len(r.raw), MAX_OUTPUT)
        shown_lines, total_lines, bytes_shown, size, left_out = self.trailer(r)
        self.assertEqual((total_lines, size), (300, 300 * 401))
        self.assertTrue(30 <= shown_lines < 150, shown_lines)
        self.assertEqual((bytes_shown, left_out), (shown_lines * 401, 300 - shown_lines))
        self.assertEqual(r.lines[:-1], lines[:shown_lines])

    def test_multibyte_text_is_bounded_in_bytes_and_never_split(self):
        lines = ["é" * 400 for _ in range(200)]
        self.p.add_board("Accents.dc.html", "\n".join(lines) + "\n")
        r = self.head("Accents.dc.html")
        self.assertLessEqual(len(r.raw), MAX_OUTPUT)
        r.raw.decode("utf-8")
        shown_lines = self.trailer(r)[0]
        self.assertTrue(10 <= shown_lines <= 20, shown_lines)
        self.assertEqual(r.lines[:-1], lines[:shown_lines])

    def test_a_line_of_wide_characters_is_cut_at_500_characters(self):
        self.p.add_board("Wide-chars.dc.html", "あ" * 700 + "\n")
        r = self.head("Wide-chars.dc.html")
        self.assertEqual(r.lines[0], "あ" * 500 + " [cut]")

    def test_an_empty_file(self):
        self.p.add_board("Empty.dc.html", "")
        r = self.head("Empty.dc.html")
        self.assertEqual((r.code, r.lines), (0, ["head: 0 of 0 lines, 0 of 0 bytes, 0 lines cut"]), r)

    def test_a_file_without_a_final_newline(self):
        self.p.add_board("NoEol.dc.html", "a\nb\nc")
        r = self.head("NoEol.dc.html")
        self.assertEqual(r.lines, ["a", "b", "c", "head: 3 of 3 lines, 5 of 5 bytes, 0 lines cut"])

    def test_carriage_returns_are_not_printed_but_counted(self):
        self.p.add_board("Crlf.dc.html", b"a\r\nb\r\n")
        r = self.head("Crlf.dc.html")
        self.assertEqual(r.lines, ["a", "b", "head: 2 of 2 lines, 6 of 6 bytes, 0 lines cut"])
        self.assertNotIn(b"\r", r.raw)

    def test_bytes_that_are_not_utf8_do_not_end_in_a_traceback(self):
        self.p.add_board("Binary.dc.html", b"ok \xff\xfe bytes\nsecond\n")
        r = self.head("Binary.dc.html")
        self.assertEqual(r.code, 0, r)
        self.assertEqual(r.lines[1], "second")
        self.assertEqual(self.trailer(r)[:2], (2, 2))

    def test_the_trailer_counts_match_the_boards_command(self):
        listing = self.cli("boards", "DSN-001")
        for line in listing.lines[1:-1]:
            _, _k, name, size, lines, _digest = line.split()
            r = self.head(name)
            self.assertEqual(self.trailer(r)[1], int(lines), (line, r.lines[-1]))
            self.assertEqual(self.trailer(r)[3], int(size), (line, r.lines[-1]))

    def assert_err06(self, r, name_json, reason):
        self.assertEqual(r.code, 1, r)
        self.assertEqual(len(r.lines), 1, r)
        self.assertRegex(r.lines[0], rf"^ERR-06: board {re.escape(name_json)}: {reason}")

    def test_a_symbolic_link_is_refused_and_its_target_is_never_read(self):
        target = self.p.elsewhere / "secret.html"
        target.write_text("SECRET-CONTENT\n")
        link = self.p.boards_dir() / "Home.dc.html"
        link.unlink()
        link.symlink_to(target)
        r = self.head("Home.dc.html", forbid=[link, target])
        self.assert_err06(r, '"Home.dc.html"', r"symbolic link")
        self.assertNotIn("SECRET", r.out)

    def test_a_file_canvas_json_does_not_name(self):
        self.p.put("docs/specs/design/DSN-001/boards/Other.dc.html", "<title>Other</title>\nNOT-NAMED\n")
        r = self.head("Other.dc.html", forbid=[self.p.boards_dir() / "Other.dc.html"])
        self.assert_err06(r, '"Other.dc.html"', r"not named|does not name")
        self.assertNotIn("NOT-NAMED", r.out)

    def test_an_absent_file(self):
        (self.p.boards_dir() / "Home.dc.html").unlink()
        self.assert_err06(self.head("Home.dc.html"), '"Home.dc.html"', r"absent|does not exist|missing")

    def test_a_directory(self):
        (self.p.boards_dir() / "Home.dc.html").unlink()
        (self.p.boards_dir() / "Home.dc.html").mkdir()
        self.assert_err06(self.head("Home.dc.html"), '"Home.dc.html"', r"regular file")

    def test_names_with_a_slash_or_dots_are_refused_even_when_canvas_json_names_them(self):
        self.p.put("docs/specs/design/DSN-001/outside.dc.html", "OUTSIDE-CONTENT\n")
        self.p.put("docs/specs/design/DSN-001/boards/sub/x.html", "SUB-CONTENT\n")
        forbid = [self.p.boards_dir() / "sub" / "x.html", self.p.boards_dir().parent / "outside.dc.html"]
        for name in ("a/b", "../outside.dc.html", "sub/x.html", "..", ".", "", "a\\b", "x..y.html"):
            with self.subTest(name=name, named=False):
                r = self.head(name, forbid=forbid)
                self.assert_err06(r, json.dumps(name), r"plain file name")
            with self.subTest(name=name, named=True):
                canvas = json.loads((self.p.boards_dir() / "canvas.json").read_text())
                canvas["boards"][name] = {}
                self.p.write_canvas(canvas)
                r = self.head(name, forbid=forbid)
                self.assert_err06(r, json.dumps(name), r"plain file name")
                self.assertNotIn("CONTENT", r.out)

    def test_an_unusable_canvas_json_cannot_run(self):
        self.p.put("docs/specs/design/DSN-001/boards/canvas.json", "not json {")
        r = self.head("Home.dc.html")
        self.assertEqual((r.code, len(r.lines)), (2, 1), r)
        self.assertRegex(r.lines[0], r"^Cannot run: .+\.$")

    def test_a_missing_boards_folder_cannot_run(self):
        r = self.cli("head", "DSN-009", "Home.dc.html")
        self.assertEqual((r.code, len(r.lines)), (2, 1), r)
        self.assertRegex(r.lines[0], r"^Cannot run: .+\.$")


# =====================================================================================================================
# QR-05: the guard itself bites, so that "no socket, no write, no forbidden path" above is not vacuous
# =====================================================================================================================
class GuardBites(unittest.TestCase):
    def run_guard(self, body, forbid=""):
        with tempfile.TemporaryDirectory() as d:
            script = Path(d) / "probe.py"
            script.write_text(body)
            env = dict(os.environ, DSN_GUARD_FORBID=forbid)
            return subprocess.run([sys.executable, "-B", "-S", "-c", GUARD, str(script)], capture_output=True,
                                  text=True, env=env, timeout=60)

    def test_a_socket_fails(self):
        p = self.run_guard("import socket\ntry:\n    socket.socket()\nexcept Exception:\n    pass\n")
        self.assertEqual((p.returncode, p.stderr.split(":")[0]), (97, "GUARD"), p)

    def test_a_connection_fails(self):
        p = self.run_guard("import socket\nsocket.create_connection(('127.0.0.1', 9))\n")
        self.assertEqual(p.returncode, 97, p)

    def test_a_write_fails(self):
        with tempfile.TemporaryDirectory() as d:
            target = Path(d) / "out.txt"
            p = self.run_guard(f"open({str(target)!r}, 'w').write('x')\n")
            self.assertEqual(p.returncode, 97, p)
            self.assertFalse(target.exists())

    def test_a_delete_or_rename_fails(self):
        with tempfile.TemporaryDirectory() as d:
            f = Path(d) / "x.txt"
            f.write_text("x")
            for body in (f"import os\nos.remove({str(f)!r})\n", f"import os\nos.rename({str(f)!r}, {str(f) + '2'!r})\n"):
                self.assertEqual(self.run_guard(body).returncode, 97, body)
            self.assertTrue(f.exists())

    def test_starting_a_process_fails(self):
        p = self.run_guard("import subprocess\nsubprocess.run(['true'])\n")
        self.assertEqual(p.returncode, 97, p)

    def test_a_forbidden_path_cannot_be_opened_but_other_reads_work(self):
        with tempfile.TemporaryDirectory() as d:
            a, b = Path(d) / "a.txt", Path(d) / "b.txt"
            a.write_text("a")
            b.write_text("b")
            p = self.run_guard(f"print(open({str(b)!r}).read())\nprint(open({str(a)!r}).read())\n", forbid=str(a))
            self.assertEqual((p.returncode, p.stdout), (97, "b\n"), p)


# =====================================================================================================================
# IF-03 check (VER-24)
# =====================================================================================================================
ERR_LINE = re.compile(r"^docs/specs/design/DSN-001\.md:(\d+): ([^:]+): (.+) \((frontmatter|boards|mapping|links|"
                      r"coverage|approval|changelog|placeholder)\)$")
WARN_LINE = re.compile(r"^warning: docs/specs/design/DSN-001\.md:(\d+): ([^:]+): (.+) \((links|mapping)\)$")


class CheckCase(Base):
    """The seeded project and the helpers the check cases share (no tests here)."""

    def setUp(self):
        super().setUp()
        self.p.shared()
        self.base = BASE

    def check(self, text=None, *flags):
        self.p.write_dsn(self.base if text is None else text)
        return self.cli("check", *flags, "DSN-001")

    def errors(self, r):
        return [l for l in r.lines[:-1] if not l.startswith(("warning: ", "fact: "))]

    def warnings(self, r):
        return [l for l in r.lines[:-1] if l.startswith("warning: ")]

    def facts(self, r):
        return [l for l in r.lines[:-1] if l.startswith("fact: ")]

    def assert_ok(self, text=None, *flags, warnings=0):
        r = self.check(text, *flags)
        self.assertEqual(r.code, 0, r)
        suffix = " (before amend)" if "--before-amend" in flags else ""
        self.assertEqual(r.lines[-1], f"OK {FILE}{suffix}", r)
        self.assertEqual(self.errors(r), [], r)
        self.assertEqual(len(self.warnings(r)), warnings, r)
        for w in self.warnings(r):
            self.assertRegex(w, WARN_LINE)
        return r

    def assert_invalid(self, text, *expect, n=None, flags=()):
        """Exit 1, every error line well formed, and a line for each (rule, part, message pattern[, line])."""
        r = self.check(text, *flags)
        self.assertEqual(r.code, 1, r)
        errors = self.errors(r)
        for line in errors:
            self.assertRegex(line, ERR_LINE)
        self.assertEqual(r.lines[-1], f"INVALID: {len(errors)} error(s) in {FILE}", r)
        if n is not None:
            self.assertEqual(len(errors), n, r)
        for spec in expect:
            rule, part, msg = spec[:3]
            line = spec[3] if len(spec) > 3 else None
            hits = []
            for l in errors:
                m = ERR_LINE.match(l)
                if (re.fullmatch(rule, m.group(4)) and re.search(part, m.group(2)) and re.search(msg, m.group(3))
                        and (line is None or int(m.group(1)) == line)):
                    hits.append(l)
            self.assertTrue(hits, f"no {rule} error for {part!r} / {msg!r} (line {line}) in:\n{r.out}")
        return r

    def approved(self, text=None):
        text = self.base if text is None else text
        text = edit(text, "status: draft ", "status: approved ")
        text = edit(text, 'approved_by: ""', 'approved_by: "Example Owner"')
        text = edit(text, "approved_on: null", "approved_on: 2026-10-09")
        text = edit(text, "| IDEA-06 | none | no board yet |", "| IDEA-06 | none | not a screen |")
        text = edit(text, MARKER, "None.")
        return edit(text, CHANGE_ROW, CHANGE_ROW + "\n| 1 | 2026-10-09 | Example Owner | Approved | status |")

    def withdrawn(self):
        """IDEA-02 stopped being promoted in the BRN, and the DSN kept it as a withdrawn row and mapping."""
        self.p.write_brn(version=2, ideas=dict(IDEAS, **{"IDEA-02": ("List shifts in a table", "parked")}))
        text = edit(self.base, "| IDEA-02 | BRD-01, BRD-02 | designed |", "| IDEA-02 | BRD-01, BRD-02 | withdrawn |")
        return edit(text, "version: 1, hash: null}", "version: 2, hash: null}", count=4)

    def without_add_board(self, text):
        """BRD-03 (Add) deprecated, the file gone from the canvas, and everything that follows from it."""
        text = set_field(text, "BRD-03", "status", "deprecated")
        text = set_field(text, "BRD-03", "sha256", f'"{self.p.digest("Add.dc.html")}"')  # the file is about to go
        text = edit(text, "| IDEA-01 | BRD-03 | designed |", "| IDEA-01 | none | no board yet |")
        text = edit(text, MARKER, MARKER + "\n- [NEEDS CLARIFICATION: IDEA-01 has no board yet]")
        text = edit(text, IDEA01_LINK, "")
        self.p.remove_board("Add.dc.html")
        return text

    def returned_add_board(self, text):
        """BRD-03 (Add) deprecated and a new active item BRD-05 for the same file."""
        text = set_field(text, "BRD-03", "status", "deprecated")
        text = add_item(text, '''  - id: BRD-05
    status: active
    file: "Add.dc.html"
    title: "Add"
    flow: "shifts"
    surface: "terminal"
    ideas: ["IDEA-01"]
    answers: []
    sha256: "@Add.dc.html@"
    notes: null''')
        return edit(text, "| IDEA-01 | BRD-03 | designed |", "| IDEA-01 | BRD-05 | designed |")


class Check(CheckCase):
    # --- Valid documents ---------------------------------------------------------------------------------------
    def test_a_created_dsn_passes(self):
        r = self.assert_ok()
        self.assertEqual(r.lines, [f"OK {FILE}"])

    def test_an_approved_dsn_passes(self):
        self.assert_ok(self.approved())

    def test_a_superseded_dsn_that_was_approved_passes_even_with_a_marker(self):
        text = edit(self.base, "status: draft ", "status: superseded ")
        text = edit(text, 'approved_by: ""', 'approved_by: "Example Owner"')
        text = edit(text, "approved_on: null", "approved_on: 2026-10-09")
        text = edit(text, "superseded_by: null", "superseded_by: DSN-002")
        self.assert_ok(text)

    def test_a_deprecated_dsn_passes(self):
        self.assert_ok(edit(self.base, "status: draft ", "status: deprecated "))

    def test_an_in_review_dsn_passes(self):
        self.assert_ok(edit(self.base, "status: draft ", "status: in-review "))

    def test_a_dsn_with_null_mappings_and_markers_passes(self):
        items = "".join(NULL_ITEM.format(n=n, file=f, title=f.split(".")[0]) for n, f in enumerate(BOARDS, 1))
        self.assert_ok(NULL_DSN.replace("@ITEMS@", items))

    def test_an_amended_dsn_passes(self):
        self.p.add_board("Settings.dc.html", SETTINGS)
        text = edit(self.base, "\nversion: 1\n", "\nversion: 2\n")
        text = edit(text, "status: draft ", "status: in-review ")
        text = edit(text, "updated: 2026-10-09", "updated: 2026-10-10")
        text = edit(text, 'canvas_version: "17-example"', 'canvas_version: "1791670000-e5f6"')
        text = edit(text, "considered: []", 'considered: ["PRD-001@2"]')
        text = add_item(text, '''  - id: BRD-05
    status: active
    file: "Settings.dc.html"
    title: "Settings"
    flow: "report-and-home"
    surface: "web"
    ideas: []
    answers: ["PRD-001#FR-024"]
    sha256: "@Settings.dc.html@"
    notes: null''')
        text = edit(text, CHANGE_ROW, CHANGE_ROW + "\n| 2 | 2026-10-10 | claude-code (session 0b6c1d2e-3f40-4a5b-8c7d-"
                    "9e0f1a2b3c4d) | Settings added; PRD-001 version 2 read | BRD-05 |")
        self.assert_ok(text)

    def test_a_deprecated_item_and_an_active_item_for_the_same_file_pass(self):
        self.assert_ok(self.returned_add_board(self.base))

    def test_a_deprecated_item_may_hold_stale_things(self):
        text = self.without_add_board(self.base)
        text = set_field(text, "BRD-03", "sha256", '"' + "0" * 64 + '"')
        text = set_field(text, "BRD-03", "file", '"Gone.dc.html"')
        text = set_field(text, "BRD-03", "ideas", '["IDEA-05"]')
        self.assert_ok(text)

    def test_a_kept_withdrawn_idea_passes(self):
        self.assert_ok(self.withdrawn())

    def test_a_withdrawn_row_with_no_boards_passes(self):
        text = self.withdrawn()
        for brd in ("BRD-01", "BRD-02"):
            text = set_field(text, brd, "ideas", "[]")
        text = edit(text, "| IDEA-02 | BRD-01, BRD-02 | withdrawn |", "| IDEA-02 | none | withdrawn |")
        text = edit(text, "  - {id: BRN-001, item: IDEA-02, relation: derives, version: 2, hash: null}\n", "")
        self.assert_ok(text)

    def test_plain_scalars_and_comments_pass(self):
        text = self.base
        for field, new in (("file", "Home.dc.html"), ("title", "Home"), ("flow", "report-and-home"), ("surface", "web")):
            text = set_field(text, "BRD-01", field, new)
        text = set_field(text, "BRD-02", "flow", '"shifts"        # the terminal flow')
        text = edit(text, 'owner: "Example Owner"', 'owner: "Example Owner"   # the BRN\'s owner')
        text = edit(text, 'boards_root: "docs/specs/design/DSN-001/boards/"',
                    "boards_root: docs/specs/design/DSN-001/boards/")
        text = edit(text, "canvas_format: 3", "canvas_format: 3   # read from canvas.json")
        text = edit(text, 'canvas: "https://claude.ai/artifact/EXAMPLE"', "canvas: https://claude.ai/artifact/EXAMPLE")
        self.assert_ok(text)

    def test_block_lists_in_the_frontmatter_pass(self):
        text = edit(self.base, 'authors: ["Example Owner", "claude-code"]',
                    'authors:\n  - "Example Owner"\n  - "claude-code"')
        text = edit(text, "considered: []", 'considered:\n  - "PRD-001@2"\n  - "declined:PRD-001#FR-025"')
        self.assert_ok(text)

    def test_a_document_with_windows_line_endings_passes(self):
        self.assert_ok(self.base.replace("\n", "\r\n"))

    def test_code_spans_quote_the_forms_that_would_otherwise_be_flagged(self):
        text = edit(self.base, "## 1. Scope\n\n", "## 1. Scope\n\nWrite `[[fill: x]]`, `<!-- x -->` or "
                    "`[NEEDS CLARIFICATION: x]` in a code span.\n\n")
        self.assert_ok(text)

    def test_values_with_hash_colon_quote_and_comma_pass_in_every_arm(self):
        text = edit(self.base, 'title: "Shiftlog: record shifts: release design"',
                    'title: "Shiftlog: \\"record\\" shifts, v2 # not a comment: release design"')
        text = set_field(text, "BRD-02", "title", '"List: the \\"shifts\\", a \\\\ table # one"')
        text = set_field(text, "BRD-02", "notes", '"flow, surface; ideas: confirmed # by Example Owner, 2026-10-09"')
        text = set_field(text, "BRD-03", "answers", '["PRD-001#FR-024", "PRD-001#NFR-001", "ADR-009"]')
        text = edit(text, "considered: []", 'considered: ["PRD-001@2", "ADR-009@1", "declined:PRD-001#FR-023"]')
        self.assert_ok(text)

    def test_a_plain_title_with_a_colon_is_rejected_in_every_arm(self):
        text = edit(self.base, 'title: "Shiftlog: record shifts: release design"', "title: Shiftlog: record shifts")
        self.assert_invalid(text, ("frontmatter", "title", r"quote"), n=1)

    def test_an_unclosed_quote_is_rejected_in_every_arm(self):
        text = edit(self.base, 'title: "Shiftlog: record shifts: release design"', 'title: "Shiftlog: record shifts')
        self.assert_invalid(text, ("frontmatter", "title", r"quote"), n=1)

    # --- frontmatter ----------------------------------------------------------------------------------------------
    def test_frontmatter_id_must_equal_the_file_name(self):
        text = edit(self.base, "id: DSN-001\ntype", "id: DSN-002\ntype")
        self.assert_invalid(text, ("frontmatter", "^id$", r"file name", 2), n=1)

    def test_frontmatter_boards_root_must_be_the_documents_own(self):
        for bad in ("docs/specs/design/DSN-002/boards/", "docs/specs/design/DSN-001/boards", "boards/", ""):
            with self.subTest(bad=bad):
                text = edit(self.base, 'boards_root: "docs/specs/design/DSN-001/boards/"', f'boards_root: "{bad}"')
                self.assert_invalid(text, ("frontmatter", "^boards_root$", r"docs/specs/design/DSN-001/boards/",
                                           line_of(self.base, "boards_root:")), n=1)

    def test_frontmatter_canvas_format_must_equal_canvas_json(self):
        text = edit(self.base, "canvas_format: 3", "canvas_format: 2")
        self.assert_invalid(text, ("frontmatter", "^canvas_format$", r"canvas\.json.*3|3.*canvas\.json",
                                   line_of(self.base, "canvas_format:")), n=1)

    def test_frontmatter_canvas_format_must_be_an_integer(self):
        for bad in ('"3"', "3.0", "true", "null", "0", "-1"):
            with self.subTest(bad=bad):
                self.assert_invalid(edit(self.base, "canvas_format: 3", f"canvas_format: {bad}"),
                                    ("frontmatter", "^canvas_format$", r"integer"))

    def test_frontmatter_canvas_must_be_https_or_null(self):
        for bad in ("http://claude.ai/x", "ftp://x", "claude.ai/artifact/x", "https://", "https://a b", ""):
            with self.subTest(bad=bad):
                text = edit(self.base, 'canvas: "https://claude.ai/artifact/EXAMPLE"', f'canvas: "{bad}"')
                self.assert_invalid(text, ("frontmatter", "^canvas$", r"https://"))
        self.assert_ok(edit(self.base, 'canvas: "https://claude.ai/artifact/EXAMPLE"', "canvas: null"))

    def test_frontmatter_canvas_version_is_a_non_empty_string_or_null(self):
        for bad in ('""', "17", "2026-10-09", "1.5", "true"):
            with self.subTest(bad=bad):
                self.assert_invalid(edit(self.base, 'canvas_version: "17-example"', f"canvas_version: {bad}"),
                                    ("frontmatter", "^canvas_version$", r"string|null"))
        self.assert_ok(edit(self.base, 'canvas_version: "17-example"', "canvas_version: null"))

    def test_frontmatter_a_malformed_considered_entry(self):
        for bad in ("PRD-1@2", "PRD-001", "ADR-009@", "XYZ-001@1", "declined:FR-001", "declined:PRD-001",
                    "declined:ADR-9", "PRD-001@2 ", "PRD-001@v2", "prd-001@2"):
            with self.subTest(bad=bad):
                text = edit(self.base, "considered: []", f'considered: ["{bad}"]')
                self.assert_invalid(text, ("frontmatter", "^considered$", r"considered entry",
                                           line_of(self.base, "considered:")), n=1)

    def test_frontmatter_considered_entries_may_not_repeat(self):
        text = edit(self.base, "considered: []", 'considered: ["PRD-001@2", "PRD-001@2"]')
        self.assert_invalid(text, ("frontmatter", "^considered$", r"repeat|duplicate"))

    def test_frontmatter_a_declined_entry_may_not_name_an_answered_item(self):
        text = set_field(self.base, "BRD-03", "answers", '["PRD-001#FR-024"]')
        text = edit(text, "considered: []", 'considered: ["declined:PRD-001#FR-024"]')
        self.assert_invalid(text, ("frontmatter", "^considered$", r"declined.*PRD-001#FR-024.*answers"), n=1)
        text = set_field(self.base, "BRD-03", "answers", '["ADR-009"]')
        text = edit(text, "considered: []", 'considered: ["declined:ADR-009"]')
        self.assert_invalid(text, ("frontmatter", "^considered$", r"declined.*ADR-009"), n=1)

    def test_frontmatter_a_declined_entry_for_a_deprecated_boards_answer_is_allowed(self):
        text = set_field(self.base, "BRD-03", "answers", '["PRD-001#FR-024"]')
        text = self.without_add_board(text)
        text = edit(text, "considered: []", 'considered: ["declined:PRD-001#FR-024"]')
        self.assert_ok(text)

    def test_frontmatter_a_missing_key(self):
        text = edit(self.base, 'canvas_version: "17-example"\n', "")
        self.assert_invalid(text, ("frontmatter", "canvas_version", r"missing"), n=1)

    def test_frontmatter_every_key_is_required(self):
        keys = re.findall(r"(?m)^([a-z_]+):", self.base.split("\n---\n")[0])
        self.assertEqual(len(keys), 22, keys)
        for key in keys:
            if key in ("generated_by", "upstream"):
                continue
            with self.subTest(key=key):
                text = re.sub(rf"(?m)^{key}:.*\n", "", self.base, count=1)
                self.assert_invalid(text, ("frontmatter", key, r"missing"))

    def test_frontmatter_keys_out_of_order(self):
        text = edit(self.base, "created: 2026-10-09\nupdated: 2026-10-09\n", "updated: 2026-10-09\ncreated: 2026-10-09\n")
        self.assert_invalid(text, ("frontmatter", "created|updated", r"order"))

    def test_frontmatter_an_unknown_key(self):
        text = edit(self.base, "considered: []\n", "considered: []\ntokens: []\n")
        self.assert_invalid(text, ("frontmatter", "^tokens$", r"unknown|not allowed"), n=1)

    def test_frontmatter_a_repeated_key(self):
        text = edit(self.base, "version: 1\ncreated", "version: 1\nversion: 1\ncreated")
        self.assert_invalid(text, ("frontmatter", "^version$", r"repeat|duplicate"))

    def test_frontmatter_type_status_and_version(self):
        self.assert_invalid(edit(self.base, "type: design", "type: spec"), ("frontmatter", "^type$", r"design"), n=1)
        for status in ("archived", "Draft", "accepted", ""):
            with self.subTest(status=status):
                text = edit(self.base, "status: draft ", f"status: {status} ")
                self.assert_invalid(text, ("frontmatter", "^status$",
                                           r"draft.*in-review.*approved.*superseded.*deprecated"))
        for version in ("0", "-1", '"1"', "1.0", "one", "true", "null"):
            with self.subTest(version=version):
                text = edit(self.base, "\nversion: 1\n", f"\nversion: {version}\n")
                self.assert_invalid(text, ("frontmatter", "^version$", r"integer"))

    def test_frontmatter_dates(self):
        for key in ("created", "updated"):
            for bad in ("2026-13-45", "2026-02-30", "2026-9-1", '"2026-10-09"', "yesterday", "null"):
                with self.subTest(key=key, bad=bad):
                    text = edit(self.base, f"\n{key}: 2026-10-09\n", f"\n{key}: {bad}\n")
                    self.assert_invalid(text, ("frontmatter", f"^{key}$", r"date|YYYY-MM-DD"))
        self.assert_invalid(edit(self.base, "\nupdated: 2026-10-09\n", "\nupdated: 2026-10-08\n"),
                            ("frontmatter", "^updated$", r"before"))

    def test_frontmatter_the_other_keys_have_the_shapes_of_the_schema(self):
        for old, new, part in (
                ('owner: "Example Owner"', 'owner: ""', "^owner$"),
                ('owner: "Example Owner"', "owner: 7", "^owner$"),
                ('title: "Shiftlog: record shifts: release design"', 'title: ""', "^title$"),
                ('authors: ["Example Owner", "claude-code"]', "authors: Example Owner", "^authors$"),
                ("reviewed_by: []", "reviewed_by: nobody", "^reviewed_by$"),
                ("supersedes: []", 'supersedes: ["DSN-1"]', "^supersedes$"),
                ("superseded_by: null", "superseded_by: DSN-1", "^superseded_by$"),
                ("blocked_by: []", "blocked_by: [x]", "^blocked_by$"),
                ('  tool: "claude-code"', "  tool: 5", "generated_by")):
            with self.subTest(new=new):
                self.assert_invalid(edit(self.base, old, new), ("frontmatter", part, r"."))

    def test_frontmatter_not_found(self):
        self.assert_invalid("# DSN-001\n\nno frontmatter\n", ("frontmatter", ".", r"---"), n=1)
        self.assert_invalid("---\nid: DSN-001\n", ("frontmatter", ".", r"closing"), n=1)

    # --- boards ---------------------------------------------------------------------------------------------------
    def test_boards_a_duplicate_item_id(self):
        text = edit(self.base, "  - id: BRD-03\n", "  - id: BRD-02\n")
        self.assert_invalid(text, ("boards", "BRD-02", r"duplicate"))

    def test_boards_item_ids_are_brd_and_two_digits(self):
        for bad in ("BRD-1", "BRD-001", "BOARD-01", "brd-01"):
            with self.subTest(bad=bad):
                text = edit(self.base, "  - id: BRD-04\n", f"  - id: {bad}\n")
                self.assert_invalid(text, ("boards", re.escape(bad), r"BRD-NN"))

    def test_boards_a_board_in_canvas_json_with_no_active_item(self):
        self.p.add_board("Settings.dc.html", SETTINGS)
        self.assert_invalid(self.base, ("boards", "canvas.json", r"Settings\.dc\.html.*no active"), n=1)

    def test_boards_a_board_whose_only_item_is_deprecated_has_no_active_item(self):
        text = set_field(self.base, "BRD-03", "status", "deprecated")
        text = edit(text, "| IDEA-01 | BRD-03 | designed |", "| IDEA-01 | none | no board yet |")
        text = edit(text, MARKER, MARKER + "\n- [NEEDS CLARIFICATION: IDEA-01 has no board yet]")
        text = edit(text, IDEA01_LINK, "")
        self.assert_invalid(text, ("boards", "canvas.json", r"Add\.dc\.html.*no active"), n=1)

    def test_boards_an_active_item_whose_file_canvas_json_does_not_name(self):
        text = set_field(self.base, "BRD-04", "file", '"Gone.dc.html"')
        self.assert_invalid(text, ("boards", "BRD-04", r"Gone\.dc\.html.*not named by canvas\.json"),
                            ("boards", "canvas.json", r"Report\.dc\.html.*no active"))

    def test_boards_a_stale_digest(self):
        old = self.p.digest("Report.dc.html")
        line = line_of(self.p.render(self.base), old)
        self.p.write_dsn(self.base)
        self.p.put("docs/specs/design/DSN-001/boards/Report.dc.html", BOARDS["Report.dc.html"] + "<p>changed</p>\n")
        r = self.cli("check", "DSN-001")
        self.assertEqual(r.code, 1, r)
        self.assertEqual(len(self.errors(r)), 1, r)
        m = ERR_LINE.match(self.errors(r)[0])
        self.assertEqual((m.group(2), m.group(4), int(m.group(1))), ("BRD-04", "boards", line), r)
        self.assertRegex(m.group(3), r"sha256")

    def test_boards_a_malformed_digest(self):
        for bad in ('"ABCDEF"', '"' + "g" * 64 + '"', '"' + "A" * 64 + '"', "null", "7"):
            with self.subTest(bad=bad):
                self.assert_invalid(set_field(self.base, "BRD-01", "sha256", bad), ("boards", "BRD-01", r"sha256"))

    def test_boards_an_extra_field(self):
        self.assert_invalid(add_field(self.base, "BRD-02", 'colour: "red"'),
                            ("boards", "BRD-02", r"colour.*not allowed"), n=1)

    def test_boards_a_board_level_upstream(self):
        text = add_field(self.base, "BRD-02", "upstream: []")
        self.assert_invalid(text, ("boards", "BRD-02", r"upstream.*not allowed"), n=1)

    def test_boards_a_missing_required_field(self):
        for field in ("status", "file", "title", "flow", "surface", "ideas", "answers", "sha256"):
            with self.subTest(field=field):
                self.assert_invalid(drop_field(self.base, "BRD-02", field), ("boards", "BRD-02", rf"missing.*{field}"))

    def test_boards_an_item_without_answers_fails(self):
        self.assert_invalid(drop_field(self.base, "BRD-01", "answers"), ("boards", "BRD-01", r"answers"), n=1)

    def test_boards_optional_fields_are_allowed(self):
        text = self.returned_add_board(self.base)
        text = add_field(text, "BRD-03", "superseded_by: BRD-05")
        self.assert_ok(text)

    def test_boards_status_is_active_or_deprecated(self):
        self.assert_invalid(set_field(self.base, "BRD-01", "status", "retired"),
                            ("boards", "BRD-01", r"active.*deprecated"))

    def test_boards_superseded_by_is_a_brd_id_or_null(self):
        self.assert_invalid(add_field(self.base, "BRD-01", "superseded_by: Home"),
                            ("boards", "BRD-01", r"superseded_by"))

    def test_boards_file_must_be_a_plain_name(self):
        for bad in ("a/b.html", "..", "x..y.html", "a\\\\b", ""):
            with self.subTest(bad=bad):
                self.assert_invalid(set_field(self.base, "BRD-01", "file", f'"{bad}"'),
                                    ("boards", "BRD-01", r"plain file name"))

    def test_boards_two_active_items_for_one_file(self):
        text = add_item(self.base, '''  - id: BRD-05
    status: active
    file: "Home.dc.html"
    title: "Home again"
    flow: null
    surface: null
    ideas: []
    answers: []
    sha256: "@Home.dc.html@"
    notes: "[NEEDS CLARIFICATION: flow and surface of the second Home]"''')
        self.assert_invalid(text, ("boards", "BRD-0[15]|canvas.json", r"Home\.dc\.html.*(two|both|more than one)"))

    def test_boards_a_board_file_named_by_canvas_json_that_cannot_be_read(self):
        self.p.write_dsn(self.base)
        (self.p.boards_dir() / "Report.dc.html").unlink()
        r = self.cli("check", "DSN-001")
        self.assertEqual(r.code, 1, r)
        self.assertEqual(len(self.errors(r)), 1, r)
        self.assertRegex(self.errors(r)[0], r"Report\.dc\.html.*ERR-06.*\(boards\)$")

    def test_boards_a_boards_folder_that_cannot_be_used_is_one_error(self):
        self.p.write_dsn(self.base)
        for raw in (b"not json {", b'{"v": 4, "boards": {"Home.dc.html": {}}}', b'{"v": 3, "boards": {}}'):
            with self.subTest(raw=raw):
                self.p.put("docs/specs/design/DSN-001/boards/canvas.json", raw)
                r = self.cli("check", "DSN-001")
                self.assertEqual(r.code, 1, r)
                self.assertEqual(len(self.errors(r)), 1, r)
                self.assertRegex(self.errors(r)[0], r"ERR-0[345].*\(boards\)$")

    def test_boards_no_boards_block(self):
        text = re.sub(r"(?s)```yaml items\nboards:.*?\n```\n", "", self.base)
        self.assert_invalid(text, ("boards", ".", r"boards:"))

    def test_boards_a_block_that_is_not_in_the_fixed_shape(self):
        for old, new, pattern in (
                ('    ideas: ["IDEA-02"]\n    answers: []\n    sha256: "@Home.dc.html@"',
                 '    ideas:\n      - IDEA-02\n    answers: []\n    sha256: "@Home.dc.html@"', r"ideas"),
                ('    title: "Home"\n', '    title: "Home\n', r"title"),
                ('    title: "Home"\n', '    title: Home: the page\n', r"title"),
                ('    title: "Home"\n', '    title:\n', r"title"),
                ('    title: "Home"\n', '    title: "Ho" me\n', r"title"),
                ('    notes: null\n  - id: BRD-02', '    notes: null\n      stray: line\n  - id: BRD-02',
                 r"stray|shape|indent")):
            with self.subTest(new=new):
                self.assert_invalid(edit(self.base, old, new), ("boards", ".", pattern))

    # --- mapping ---------------------------------------------------------------------------------------------------
    def test_mapping_a_bad_flow_slug(self):
        for bad in ('"Day To Day"', '"day_to_day"', '"-day"', '"day-"', '"day--to"', '""', "5", "true"):
            with self.subTest(bad=bad):
                text = set_field(self.base, "BRD-01", "flow", bad)
                self.assert_invalid(text, ("mapping", "BRD-01", r"flow.*slug", line_of(self.base, 'flow: "report-and-home"')),
                                    n=1)

    def test_mapping_surface_is_one_of_four_or_null(self):
        for bad in ('"cli"', '"Web"', '"tui"', '""', "7"):
            with self.subTest(bad=bad):
                text = set_field(self.base, "BRD-02", "surface", bad)
                self.assert_invalid(text, ("mapping", "BRD-02", r"surface.*web.*desktop.*mobile.*terminal"), n=1)
        for good in ("web", "desktop", "mobile", "terminal"):
            with self.subTest(good=good):
                self.assert_ok(set_field(self.base, "BRD-02", "surface", f'"{good}"'))

    def test_mapping_a_null_field_needs_a_marker_in_notes(self):
        for field in ("flow", "surface", "ideas"):
            with self.subTest(field=field):
                text = set_field(self.base, "BRD-01", field, "null")
                if field == "ideas":
                    text = edit(text, "| IDEA-02 | BRD-01, BRD-02 | designed |", "| IDEA-02 | BRD-02 | designed |")
                self.assert_invalid(text, ("mapping", "BRD-01", rf"{field}.*null.*\[NEEDS CLARIFICATION"), n=1)
                with_marker = set_field(text, "BRD-01", "notes", f'"[NEEDS CLARIFICATION: {field}, as yet unconfirmed]"')
                self.assert_ok(with_marker)

    def test_mapping_a_marker_in_notes_without_a_null_field_is_fine(self):
        self.assert_ok(set_field(self.base, "BRD-01", "notes", '"[NEEDS CLARIFICATION: title]"'))

    def test_mapping_ideas_is_a_list_of_idea_ids_without_repeats(self):
        for bad in ('["IDEA-1"]', '["idea-02"]', '["IDEA-02", "IDEA-02"]', '"IDEA-02"', '[2]', '["IDEA-02", null]'):
            with self.subTest(bad=bad):
                self.assert_invalid(set_field(self.base, "BRD-01", "ideas", bad), ("mapping", "BRD-01", r"ideas"))

    def test_mapping_an_idea_that_is_not_promoted_and_has_no_withdrawn_row(self):
        text = set_field(self.base, "BRD-04", "ideas", '["IDEA-03", "IDEA-05"]')
        text = edit(text, "  - {id: BRN-001, item: IDEA-03, relation: derives, version: 1, hash: null}\n",
                    "  - {id: BRN-001, item: IDEA-03, relation: derives, version: 1, hash: null}\n"
                    "  - {id: BRN-001, item: IDEA-05, relation: derives, version: 1, hash: null}\n")
        self.assert_invalid(text, ("mapping", "BRD-04", r"IDEA-05.*(not promoted|promote)"), n=1)

    def test_mapping_an_idea_the_brn_does_not_have(self):
        text = set_field(self.base, "BRD-04", "ideas", '["IDEA-03", "IDEA-99"]')
        text = edit(text, "  - {id: BRN-001, item: IDEA-03, relation: derives, version: 1, hash: null}\n",
                    "  - {id: BRN-001, item: IDEA-03, relation: derives, version: 1, hash: null}\n"
                    "  - {id: BRN-001, item: IDEA-99, relation: derives, version: 1, hash: null}\n")
        self.assert_invalid(text, ("mapping", "BRD-04", r"IDEA-99"), n=1)

    def test_mapping_answers_must_have_the_form(self):
        for bad in ("FR-006", "ADR-9", "PRD-001", "PRD-001#FR-24", "PRD-1#FR-024", "PRD-001#XR-024", "PRD-001#fr-024",
                    "ADR-0009", "prd-001#FR-024", "PRD-001#FR-024 "):
            with self.subTest(bad=bad):
                text = set_field(self.base, "BRD-01", "answers", f'["{bad}"]')
                self.assert_invalid(text, ("mapping", "BRD-01", r"answers.*PRD-NNN#FR-NNN.*ADR-NNN"), n=1)

    def test_mapping_answers_is_a_list_without_repeats(self):
        for bad in ('"ADR-009"', "null", '["ADR-009", "ADR-009"]', "[9]"):
            with self.subTest(bad=bad):
                self.assert_invalid(set_field(self.base, "BRD-01", "answers", bad),
                                    ("(mapping|boards)", "BRD-01", r"answers"))

    def test_mapping_an_answer_naming_a_prd_item_that_does_not_exist(self):
        for ref, pattern in (("PRD-001#FR-099", r"FR-099"), ("PRD-001#NFR-099", r"NFR-099"),
                             ("PRD-009#FR-001", r"PRD-009"), ("PRD-001#FR-001", r"FR-001")):
            with self.subTest(ref=ref):
                text = set_field(self.base, "BRD-01", "answers", f'["{ref}"]')
                self.assert_invalid(text, ("mapping", "BRD-01", pattern), n=1)

    def test_mapping_an_answer_naming_an_adr_that_does_not_exist(self):
        text = set_field(self.base, "BRD-01", "answers", '["ADR-042"]')
        self.assert_invalid(text, ("mapping", "BRD-01", r"ADR-042"), n=1)

    def test_mapping_answers_that_exist_pass(self):
        text = set_field(self.base, "BRD-01", "answers",
                         '["PRD-001#FR-023", "PRD-001#FR-024", "PRD-001#NFR-001", "ADR-009"]')
        self.assert_ok(text)

    def test_mapping_a_deprecated_prd_item_is_a_warning(self):
        text = set_field(self.base, "BRD-01", "answers", '["PRD-001#FR-025"]')
        r = self.assert_ok(text, warnings=1)
        self.assertRegex(self.warnings(r)[0], r"BRD-01.*FR-025.*deprecated.*\(mapping\)$")

    def test_mapping_an_adr_that_is_not_accepted_is_a_warning(self):
        for status in ("proposed", "rejected", "deprecated", "superseded"):
            with self.subTest(status=status):
                self.p.put("docs/specs/adr/ADR-010.md", adr_text(10, status=status))
                r = self.assert_ok(set_field(self.base, "BRD-01", "answers", '["ADR-010"]'), warnings=1)
                self.assertRegex(self.warnings(r)[0], rf"BRD-01.*ADR-010.*{status}.*\(mapping\)$")

    def test_mapping_an_adr_with_a_superseded_by_is_a_warning(self):
        self.p.put("docs/specs/adr/ADR-010.md", adr_text(10, superseded_by="ADR-011"))
        r = self.assert_ok(set_field(self.base, "BRD-01", "answers", '["ADR-010"]'), warnings=1)
        self.assertRegex(self.warnings(r)[0], r"BRD-01.*ADR-010.*ADR-011.*\(mapping\)$")

    def test_mapping_warnings_come_after_errors(self):
        text = set_field(self.base, "BRD-01", "answers", '["PRD-001#FR-025", "PRD-001#FR-099"]')
        r = self.assert_invalid(text, ("mapping", "BRD-01", r"FR-099"), n=1)
        self.assertEqual(len(self.warnings(r)), 1, r)
        self.assertEqual([l.startswith("warning: ") for l in r.lines[:-1]], [False, True], r)

    def test_mapping_answers_of_a_deprecated_item_are_not_checked(self):
        text = self.returned_add_board(self.base)
        text = set_field(text, "BRD-03", "answers", '["PRD-009#FR-001"]')
        self.assert_ok(text, warnings=0)

    # --- links ------------------------------------------------------------------------------------------------------
    DOC_LINK = "  - {id: BRN-001, relation: derives, version: 1, hash: null}\n"

    def test_links_no_document_level_derives_link(self):
        text = edit(self.base, self.DOC_LINK, "")
        self.assert_invalid(text, ("links", "upstream", r"derives link.*without an item"), n=1)

    def test_links_two_document_level_links(self):
        text = edit(self.base, self.DOC_LINK,
                    self.DOC_LINK + "  - {id: BRN-002, relation: derives, version: 1, hash: null}\n")
        self.assert_invalid(text, ("links", "upstream", r"exactly one|more than one|BRN-002"))

    def test_links_a_missing_item_link(self):
        text = edit(self.base, "  - {id: BRN-001, item: IDEA-03, relation: derives, version: 1, hash: null}\n", "")
        self.assert_invalid(text, ("links", "upstream", r"IDEA-03.*active board"), n=1)

    def test_links_an_extra_item_link(self):
        text = edit(self.base, self.DOC_LINK,
                    self.DOC_LINK + "  - {id: BRN-001, item: IDEA-04, relation: derives, version: 1, hash: null}\n")
        self.assert_invalid(text, ("links", "upstream", r"IDEA-04.*no active board"), n=1)

    def test_links_a_repeated_item_link(self):
        link = "  - {id: BRN-001, item: IDEA-03, relation: derives, version: 1, hash: null}\n"
        self.assert_invalid(edit(self.base, link, link + link),
                            ("links", "upstream", r"IDEA-03.*(twice|repeat|more than once|duplicate)"))

    def test_links_the_item_links_follow_the_active_boards_not_the_deprecated_ones(self):
        # the helper drops the IDEA-01 link along with the board; putting it back leaves an extra link
        text = self.without_add_board(self.base)
        text = edit(text, self.DOC_LINK, self.DOC_LINK + IDEA01_LINK)
        self.assert_invalid(text, ("links", "upstream", r"IDEA-01.*no active board"))

    def test_links_a_kept_withdrawn_ideas_item_link_is_required(self):
        text = edit(self.withdrawn(), "  - {id: BRN-001, item: IDEA-02, relation: derives, version: 2, hash: null}\n", "")
        self.assert_invalid(text, ("links", "upstream", r"IDEA-02"), n=1)

    def test_links_mixed_versions(self):
        self.p.write_brn(version=2)
        text = edit(self.base, "item: IDEA-03, relation: derives, version: 1,",
                    "item: IDEA-03, relation: derives, version: 2,")
        r = self.assert_invalid(text, ("links", "upstream", r"one version|same version|mixed"), n=1)
        self.assertGreaterEqual(len(self.warnings(r)), 1, r)

    def test_links_other_relations_and_targets(self):
        for old, new in (("relation: derives, version: 1, hash: null}\n  - {id: BRN-001, item: IDEA-01",
                          "relation: informed_by, version: 1, hash: null}\n  - {id: BRN-001, item: IDEA-01"),
                         ("item: IDEA-01, relation: derives", "item: IDEA-01, relation: informed_by"),
                         ("{id: BRN-001, item: IDEA-01,", "{id: BRN-002, item: IDEA-01,"),
                         ("{id: BRN-001, item: IDEA-01,", "{id: PRD-001, item: FR-001,"),
                         ("version: 1, hash: null}\n  - {id: BRN-001, item: IDEA-01",
                          "version: 1, hash: abc}\n  - {id: BRN-001, item: IDEA-01"),
                         ("{id: BRN-001, item: IDEA-02, relation: derives, version: 1,",
                          "{id: BRN-001, item: IDEA-02, relation: derives, version: 0,")):
            with self.subTest(new=new):
                self.assert_invalid(edit(self.base, old, new), ("links", "upstream", r"."))

    def test_links_a_version_below_the_brns_is_a_warning(self):
        self.p.write_brn(version=2)
        r = self.assert_ok(warnings=1)
        self.assertRegex(self.warnings(r)[0], r"upstream: .*BRN-001.*version 1.*version 2.*\(links\)$")
        self.assertEqual(r.lines[-1], f"OK {FILE}")

    def test_links_a_version_above_the_brns_is_an_error(self):
        text = self.base.replace("version: 1, hash: null}", "version: 3, hash: null}")
        self.assert_invalid(text, ("links", "upstream", r"version 3.*BRN.*version 1"))

    # --- coverage ---------------------------------------------------------------------------------------------------
    def test_coverage_a_missing_row(self):
        text = edit(self.base, "| IDEA-03 | BRD-04 | designed |\n", "")
        self.assert_invalid(text, ("coverage", "section 3", r"IDEA-03.*no row"), n=1)

    def test_coverage_a_repeated_row(self):
        row = "| IDEA-03 | BRD-04 | designed |\n"
        self.assert_invalid(edit(self.base, row, row + row),
                            ("coverage", "section 3", r"IDEA-03.*(twice|repeat|more than once|duplicate)"))

    def test_coverage_rows_out_of_idea_order(self):
        text = edit(self.base, "| IDEA-01 | BRD-03 | designed |\n| IDEA-02 | BRD-01, BRD-02 | designed |\n",
                    "| IDEA-02 | BRD-01, BRD-02 | designed |\n| IDEA-01 | BRD-03 | designed |\n")
        self.assert_invalid(text, ("coverage", "section 3", r"order"), n=1)

    def test_coverage_a_designed_idea_with_no_board(self):
        text = edit(self.base, "| IDEA-04 | none | not a screen |", "| IDEA-04 | none | designed |")
        self.assert_invalid(text, ("coverage", "section 3", r"IDEA-04.*designed.*no active board"), n=1)

    def test_coverage_a_board_names_the_idea_but_the_row_says_otherwise(self):
        for status in ("not a screen", "no board yet"):
            with self.subTest(status=status):
                text = edit(self.base, "| IDEA-03 | BRD-04 | designed |", f"| IDEA-03 | none | {status} |")
                self.assert_invalid(text, ("coverage", "section 3", r"IDEA-03.*designed"))

    def test_coverage_the_boards_cell_lists_the_active_items_that_name_the_idea(self):
        for cell in ("BRD-01", "BRD-01, BRD-02, BRD-03", "none", "BRD-09"):
            with self.subTest(cell=cell):
                text = edit(self.base, "| IDEA-02 | BRD-01, BRD-02 | designed |", f"| IDEA-02 | {cell} | designed |")
                self.assert_invalid(text, ("coverage", "section 3", r"IDEA-02.*Boards"))
        self.assert_ok(edit(self.base, "| IDEA-02 | BRD-01, BRD-02 | designed |", "| IDEA-02 | BRD-02,BRD-01 | designed |"))

    def test_coverage_a_withdrawn_row_for_an_idea_still_promoted(self):
        text = edit(self.base, "| IDEA-02 | BRD-01, BRD-02 | designed |", "| IDEA-02 | BRD-01, BRD-02 | withdrawn |")
        self.assert_invalid(text, ("coverage", "section 3", r"IDEA-02.*withdrawn.*still promot"), n=1)

    def test_coverage_a_row_for_an_idea_that_is_not_promoted_needs_withdrawn(self):
        text = edit(self.base, "| IDEA-06 | none | no board yet |",
                    "| IDEA-05 | none | no board yet |\n| IDEA-06 | none | no board yet |")
        self.assert_invalid(text, ("coverage", "section 3", r"IDEA-05.*not promoted"))
        text = edit(self.base, "| IDEA-06 | none | no board yet |",
                    "| IDEA-05 | none | withdrawn |\n| IDEA-06 | none | no board yet |")
        self.assert_ok(text)

    def test_coverage_no_board_yet_needs_a_marker_naming_the_idea(self):
        self.assert_invalid(edit(self.base, MARKER, "None."), ("coverage", "section 3", r"IDEA-06.*marker"), n=1)
        self.assert_invalid(edit(self.base, MARKER, "- [NEEDS CLARIFICATION: IDEA-04 has no board yet]"),
                            ("coverage", "section 3", r"IDEA-06.*marker"), n=1)
        self.assert_ok(edit(self.base, MARKER, "- [NEEDS CLARIFICATION: which screen shows\n  IDEA-06?]"))

    def test_coverage_a_marker_in_a_code_span_does_not_count(self):
        self.assert_invalid(edit(self.base, MARKER, "- `[NEEDS CLARIFICATION: IDEA-06]`"),
                            ("coverage", "section 3", r"IDEA-06.*marker"))

    def test_coverage_not_a_screen_and_no_board_yet_list_no_boards(self):
        text = edit(self.base, "| IDEA-04 | none | not a screen |", "| IDEA-04 | BRD-01 | not a screen |")
        self.assert_invalid(text, ("coverage", "section 3", r"IDEA-04.*Boards"))

    def test_coverage_a_withdrawn_row_lists_the_boards_that_still_name_the_idea(self):
        text = edit(self.withdrawn(), "| IDEA-02 | BRD-01, BRD-02 | withdrawn |", "| IDEA-02 | none | withdrawn |")
        self.assert_invalid(text, ("coverage", "section 3", r"IDEA-02.*Boards"))

    def test_coverage_the_status_is_one_of_four(self):
        for bad in ("done", "Designed", "withdrawn,", ""):
            with self.subTest(bad=bad):
                text = edit(self.base, "| IDEA-04 | none | not a screen |", f"| IDEA-04 | none | {bad} |")
                self.assert_invalid(text, ("coverage", "section 3",
                                           r"designed.*not a screen.*no board yet.*withdrawn"))

    def test_coverage_the_table_has_the_header(self):
        self.assert_invalid(edit(self.base, "| Idea | Boards | Status |", "| Idea | Boards |"),
                            ("coverage", "section 3", r"Idea.*Boards.*Status"))

    def test_coverage_the_section_is_required(self):
        text = re.sub(r"(?s)## 3\. Idea coverage.*?(?=## 4\.)", "", self.base)
        self.assert_invalid(text, ("coverage", "section 3", r"## 3\. Idea coverage"))

    def test_coverage_the_idea_cell_may_carry_the_idea_text(self):
        self.assert_ok(edit(self.base, "| IDEA-04 | none |", "| IDEA-04 Export shifts as CSV | none |"))

    # --- approval ---------------------------------------------------------------------------------------------------
    def test_approval_approved_with_a_marker(self):
        text = edit(self.base, "status: draft ", "status: approved ")
        text = edit(text, 'approved_by: ""', 'approved_by: "Example Owner"')
        text = edit(text, "approved_on: null", "approved_on: 2026-10-09")
        self.assert_invalid(text, ("approval", "marker", r"approved.*\[NEEDS CLARIFICATION",
                                   line_of(self.base, "[NEEDS CLARIFICATION")), n=1)

    def test_approval_a_marker_in_a_boards_notes_blocks_approval(self):
        text = set_field(self.approved(), "BRD-01", "notes", '"[NEEDS CLARIFICATION: title]"')
        self.assert_invalid(text, ("approval", "marker", r"\[NEEDS CLARIFICATION"), n=1)

    def test_approval_a_marker_in_a_code_span_does_not_block_approval(self):
        text = edit(self.approved(), "## 1. Scope\n\n", "## 1. Scope\n\nThe form is `[NEEDS CLARIFICATION: x]`.\n\n")
        self.assert_ok(text)

    def test_approval_approved_with_an_empty_approver(self):
        for bad in ('""', "null", "7"):
            with self.subTest(bad=bad):
                text = edit(self.approved(), 'approved_by: "Example Owner"', f"approved_by: {bad}")
                self.assert_invalid(text, ("approval", "^approved_by$", r"approved.*approved_by"), n=1)

    def test_approval_approved_without_a_date(self):
        for bad in ("null", "2026-13-01", '"2026-10-09"'):
            with self.subTest(bad=bad):
                text = edit(self.approved(), "approved_on: 2026-10-09", f"approved_on: {bad}")
                self.assert_invalid(text, ("approval", "^approved_on$", r"date"))

    def test_approval_a_draft_or_in_review_dsn_has_no_approver_or_date(self):
        for status in ("draft", "in-review"):
            with self.subTest(status=status, field="approved_by"):
                text = edit(self.base, "status: draft ", f"status: {status} ")
                text = edit(text, 'approved_by: ""', 'approved_by: "Example Owner"')
                self.assert_invalid(text, ("approval", "^approved_by$", rf"{status}.*approved_by"), n=1)
            with self.subTest(status=status, field="approved_on"):
                text = edit(self.base, "status: draft ", f"status: {status} ")
                text = edit(text, "approved_on: null", "approved_on: 2026-10-09")
                self.assert_invalid(text, ("approval", "^approved_on$", rf"{status}.*approved_on"), n=1)

    # --- changelog --------------------------------------------------------------------------------------------------
    def test_changelog_a_row_for_the_version_is_required(self):
        text = edit(self.base, "\nversion: 1\n", "\nversion: 2\n")
        self.assert_invalid(text, ("changelog", "Change Log", r"no row for version 2"), n=1)

    def test_changelog_rows_in_version_order(self):
        second = "| 2 | 2026-10-09 | claude-code (session x) | second | all |"
        text = edit(self.base, "\nversion: 1\n", "\nversion: 2\n")
        self.assert_ok(edit(text, CHANGE_ROW, CHANGE_ROW + "\n" + second))
        self.assert_invalid(edit(text, CHANGE_ROW, second + "\n" + CHANGE_ROW), ("changelog", "Change Log", r"order"))

    def test_changelog_several_rows_may_share_a_version(self):
        self.assert_ok(edit(self.base, CHANGE_ROW, CHANGE_ROW + "\n| 1 | 2026-10-09 | Example Owner | Reviewed | none |"))

    def test_changelog_a_row_dated_after_updated(self):
        text = edit(self.base, CHANGE_ROW, CHANGE_ROW + "\n| 1 | 2026-10-10 | Example Owner | Reviewed | none |")
        self.assert_invalid(text, ("changelog", "Change Log", r"2026-10-10.*after.*updated",
                                   line_of(text, "2026-10-10 | Example")), n=1)

    def test_changelog_a_bad_date_or_version(self):
        for new in ("| 1 | 2026-13-09 |", "| one | 2026-10-09 |", "| 1 | yesterday |"):
            with self.subTest(new=new):
                self.assert_invalid(edit(self.base, "| 1 | 2026-10-09 |", new), ("changelog", "Change Log", r"."))

    def test_changelog_the_section_and_header_are_required(self):
        self.assert_invalid(edit(self.base, "## Change Log", "## History"), ("changelog", "Change Log", r"## Change Log"))
        self.assert_invalid(edit(self.base, "| Version | Date | Author | Change | Items affected |",
                                 "| Version | Date | Author |"),
                            ("changelog", "Change Log", r"Version.*Date.*Author.*Change.*Items affected"))

    # --- placeholder ------------------------------------------------------------------------------------------------
    def test_placeholder_an_html_comment(self):
        text = edit(self.base, "## 1. Scope\n\n", "## 1. Scope\n\n<!-- author comment -->\n\n")
        self.assert_invalid(text, ("placeholder", "document", r"HTML comment", line_of(text, "<!--")), n=1)

    def test_placeholder_an_html_comment_in_the_boards_block_or_the_frontmatter(self):
        self.assert_invalid(edit(self.base, '    title: "Home"\n', '    title: "Home"   <!-- x -->\n'),
                            ("placeholder", "document", r"HTML comment"))
        self.assert_invalid(edit(self.base, "version: 1\ncreated", "version: 1 <!-- x -->\ncreated"),
                            ("placeholder", "document", r"HTML comment"))

    def test_placeholder_a_fill_marker(self):
        text = edit(self.base, "## 1. Scope\n\n", "## 1. Scope\n\n[[fill: two to four sentences]]\n\n")
        self.assert_invalid(text, ("placeholder", "document", r"\[\[fill:", line_of(text, "[[fill:")), n=1)

    # --- the BRN and the other files --------------------------------------------------------------------------------
    def test_a_brn_that_is_missing_cannot_run(self):
        self.p.path("docs/specs/brainstorm/BRN-001.md").unlink()
        for flags in ((), ("--before-amend",)):
            with self.subTest(flags=flags):
                r = self.check(self.base, *flags)
                self.assertEqual((r.code, len(r.lines)), (2, 1), r)
                self.assertRegex(r.lines[0], r"^Cannot run: .*BRN-001.*\.$")

    def test_a_brn_that_cannot_be_read_cannot_run(self):
        good = brn_text()
        cases = {
            "not UTF-8": good.encode().replace(b"Shiftlog", b"Shift\xfflog"),
            "no ideas block": good.replace("ideas:\n", "thoughts:\n"),
            "an empty ideas block": re.sub(r"(?s)ideas:\n.*?```", "ideas:\n```", good),
            "no frontmatter": good.split("\n---\n", 1)[1],
            "no version": good.replace("version: 1\n", "", 1),
            "a version that is not an integer": good.replace("version: 1\n", "version: one\n", 1),
            "an idea without a disposition": good.replace("    disposition: promoted\n", "", 1),
            "an unreadable item": good.replace("    status: active\n    idea: \"Add a shift",
                                               "    status active\n    idea: \"Add a shift", 1),
        }
        for name, content in cases.items():
            for flags in ((), ("--before-amend",)):
                with self.subTest(name, flags=flags):
                    self.p.put("docs/specs/brainstorm/BRN-001.md", content)
                    r = self.check(self.base, *flags)
                    self.assertEqual((r.code, len(r.lines)), (2, 1), r)
                    self.assertRegex(r.lines[0], r"^Cannot run: .*BRN-001.*\.$")

    def test_only_the_brn_the_dsn_cites_is_read(self):
        self.p.put("docs/specs/brainstorm/BRN-002.md", "not even a BRN\n")
        self.p.put("docs/specs/design/DSN-002.md", "not even a DSN\n")
        self.p.put("docs/specs/design/DSN-001/boards/README.md", "digests\n")
        forbid = [self.p.path("docs/specs/brainstorm/BRN-002.md"), self.p.path("docs/specs/design/DSN-002.md"),
                  self.p.path("docs/specs/design/DSN-001/boards/README.md"), self.p.path("docs/specs/adr/ADR-009.md"),
                  self.p.path("docs/specs/prd/PRD-001.md")]
        self.p.write_dsn(self.base)
        r = self.cli("check", "DSN-001", forbid=forbid)
        self.assertEqual((r.code, r.lines), (0, [f"OK {FILE}"]), r)

    def test_only_the_prds_and_adrs_the_answers_name_are_read(self):
        self.p.put("docs/specs/prd/PRD-002.md", "not a PRD\n")
        self.p.put("docs/specs/adr/ADR-010.md", "not an ADR\n")
        self.p.write_dsn(set_field(self.base, "BRD-01", "answers", '["PRD-001#FR-024", "ADR-009"]'))
        forbid = [self.p.path("docs/specs/prd/PRD-002.md"), self.p.path("docs/specs/adr/ADR-010.md")]
        r = self.cli("check", "DSN-001", forbid=forbid)
        self.assertEqual((r.code, r.lines), (0, [f"OK {FILE}"]), r)

    def test_a_dsn_that_is_a_symbolic_link_is_not_followed(self):
        real = self.p.elsewhere / "DSN-001.md"
        real.write_text(self.p.render(self.base))
        link = self.p.path("docs/specs/design/DSN-001.md")
        link.parent.mkdir(parents=True, exist_ok=True)
        link.symlink_to(real)
        r = self.cli("check", "DSN-001", forbid=[link, real])
        self.assertEqual((r.code, len(r.lines)), (2, 1), r)
        self.assertRegex(r.lines[0], r"^Cannot run: .+\.$")

    def test_a_dsn_that_is_not_utf8_is_invalid_not_a_traceback(self):
        raw = self.p.render(self.base).encode().replace(b"Shiftlog records", b"Shiftlog \xff records")
        self.p.put("docs/specs/design/DSN-001.md", raw)
        r = self.cli("check", "DSN-001")
        self.assertEqual(r.code, 1, r)
        self.assertRegex(r.lines[0], r"UTF-8")

    def test_the_default_root_is_the_working_folder(self):
        self.p.write_dsn(self.base)
        r = self.cli("check", "DSN-001", root=False, cwd=self.p.root)
        self.assertEqual((r.code, r.lines), (0, [f"OK {FILE}"]), r)

    def test_the_error_lines_are_sorted_by_line_and_counted(self):
        text = edit(self.base, "\nupdated: 2026-10-09\n", "\nupdated: 2026-10-08\n")
        text = edit(text, "type: design", "type: spec")
        text = set_field(text, "BRD-02", "surface", '"cli"')
        r = self.assert_invalid(text, ("frontmatter", "^type$", "."), ("frontmatter", "^updated$", "."),
                                ("mapping", "BRD-02", "surface"))
        lines = [int(ERR_LINE.match(l).group(1)) for l in self.errors(r)]
        self.assertEqual(lines, sorted(lines), r)


# =====================================================================================================================
# check --before-amend (BEH-05, section 13 ad)
# =====================================================================================================================
class BeforeAmend(CheckCase):
    def test_a_current_dsn_prints_no_fact(self):
        r = self.assert_ok(None, "--before-amend")
        self.assertEqual(r.lines, [f"OK {FILE} (before amend)"])

    def test_a_changed_board(self):
        self.p.write_dsn(self.base)
        self.p.put("docs/specs/design/DSN-001/boards/Report.dc.html", BOARDS["Report.dc.html"] + "<p>redrawn</p>\n")
        r = self.cli("check", "--before-amend", "DSN-001")
        self.assertEqual((r.code, r.lines), (0, ["fact: board Report.dc.html: changed", f"OK {FILE} (before amend)"]), r)
        full = self.cli("check", "DSN-001")
        self.assertEqual(full.code, 1, full)
        self.assertRegex(full.out, r"BRD-04: .*sha256")

    def test_a_new_board(self):
        self.p.write_dsn(self.base)
        self.p.add_board("Settings.dc.html", SETTINGS)
        r = self.cli("check", "--before-amend", "DSN-001")
        self.assertEqual((r.code, r.lines), (0, ["fact: board Settings.dc.html: new", f"OK {FILE} (before amend)"]), r)
        self.assertEqual(self.cli("check", "DSN-001").code, 1)

    def test_a_removed_board(self):
        self.p.write_dsn(self.base)
        self.p.remove_board("Add.dc.html")
        r = self.cli("check", "--before-amend", "DSN-001")
        self.assertEqual((r.code, r.lines), (0, ["fact: board Add.dc.html: removed", f"OK {FILE} (before amend)"]), r)
        self.assertEqual(self.cli("check", "DSN-001").code, 1)

    def test_a_board_that_left_and_came_back_is_new_not_changed(self):
        text = set_field(self.base, "BRD-03", "status", "deprecated")
        text = edit(text, "| IDEA-01 | BRD-03 | designed |", "| IDEA-01 | none | no board yet |")
        text = edit(text, MARKER, MARKER + "\n- [NEEDS CLARIFICATION: IDEA-01 has no board yet]")
        text = edit(text, IDEA01_LINK, "")
        r = self.check(text, "--before-amend")
        self.assertEqual((r.code, r.lines), (0, ["fact: board Add.dc.html: new", f"OK {FILE} (before amend)"]), r)

    def test_a_canvas_format_that_differs(self):
        text = edit(self.base, "canvas_format: 3", "canvas_format: 2")
        r = self.check(text, "--before-amend")
        self.assertEqual((r.code, r.lines), (0, ["fact: canvas_format: the DSN records 2, canvas.json has 3",
                                                 f"OK {FILE} (before amend)"]), r)
        self.assertEqual(self.check(text).code, 1)

    def test_an_idea_that_is_not_promoted_any_more(self):
        self.p.write_brn(ideas=dict(IDEAS, **{"IDEA-02": ("List shifts in a table", "parked")}))
        r = self.check(None, "--before-amend")
        self.assertEqual((r.code, r.lines), (0, ["fact: idea IDEA-02: no longer promoted",
                                                 f"OK {FILE} (before amend)"]), r)
        full = self.check(None)
        self.assertEqual(full.code, 1, full)
        self.assertRegex(full.out, r"IDEA-02")

    def test_a_promoted_idea_without_a_row(self):
        self.p.write_brn(ideas=dict(IDEAS, **{"IDEA-07": ("Dark theme for List", "promoted")}))
        r = self.check(None, "--before-amend")
        self.assertEqual((r.code, r.lines), (0, ["fact: idea IDEA-07: no row", f"OK {FILE} (before amend)"]), r)
        full = self.check(None)
        self.assertEqual(full.code, 1, full)
        self.assertRegex(full.out, r"IDEA-07.*no row")

    def test_an_idea_not_promoted_any_more_that_has_a_withdrawn_row_prints_no_fact(self):
        text = edit(self.base, "| IDEA-02 | BRD-01, BRD-02 | designed |", "| IDEA-02 | BRD-01, BRD-02 | withdrawn |")
        self.p.write_brn(ideas=dict(IDEAS, **{"IDEA-02": ("List shifts in a table", "parked")}))
        r = self.check(text, "--before-amend")
        self.assertEqual((r.code, r.lines), (0, [f"OK {FILE} (before amend)"]), r)
        self.assertEqual(self.check(text).code, 0)

    def test_a_brn_that_moved_on(self):
        self.p.write_brn(version=2)
        r = self.check(None, "--before-amend")
        self.assertEqual(r.code, 0, r)
        self.assertEqual(self.facts(r), ["fact: links: BRN-001 at version 1, the BRN is at 2"])
        self.assertEqual(len(self.warnings(r)), 1, r)
        self.assertRegex(self.warnings(r)[0], r"\(links\)$")
        self.assertEqual(r.lines[-1], f"OK {FILE} (before amend)")

    def test_every_fact_at_once_in_a_fixed_order(self):
        self.p.write_dsn(edit(self.base, "canvas_format: 3", "canvas_format: 2"))
        self.p.put("docs/specs/design/DSN-001/boards/Report.dc.html", BOARDS["Report.dc.html"] + "<p>redrawn</p>\n")
        self.p.add_board("Settings.dc.html", SETTINGS)
        self.p.remove_board("Add.dc.html")
        self.p.write_brn(version=2, ideas=dict(IDEAS, **{"IDEA-02": ("List shifts in a table", "parked"),
                                                         "IDEA-07": ("Dark theme for List", "promoted")}))
        r = self.cli("check", "--before-amend", "DSN-001")
        self.assertEqual(r.code, 0, r)
        self.assertEqual(self.facts(r), [
            "fact: board Report.dc.html: changed",
            "fact: board Settings.dc.html: new",
            "fact: board Add.dc.html: removed",
            "fact: canvas_format: the DSN records 2, canvas.json has 3",
            "fact: idea IDEA-02: no longer promoted",
            "fact: idea IDEA-07: no row",
            "fact: links: BRN-001 at version 1, the BRN is at 2",
        ])
        self.assertEqual(r.lines[-1], f"OK {FILE} (before amend)")

    def test_structural_errors_exit_1_under_both(self):
        cases = {
            "a duplicate item id": edit(self.base, "  - id: BRD-03\n", "  - id: BRD-02\n"),
            "a bad board status": set_field(self.base, "BRD-01", "status", "retired"),
            "a bad document status": edit(self.base, "status: draft ", "status: archived "),
            "an extra field": add_field(self.base, "BRD-02", 'colour: "red"'),
            "a missing answers": drop_field(self.base, "BRD-02", "answers"),
            "surface cli": set_field(self.base, "BRD-01", "surface", '"cli"'),
            "a bad flow slug": set_field(self.base, "BRD-01", "flow", '"Day To Day"'),
            "repeated ideas": set_field(self.base, "BRD-01", "ideas", '["IDEA-02", "IDEA-02"]'),
            "a malformed answers entry": set_field(self.base, "BRD-01", "answers", '["FR-006"]'),
            "a malformed considered entry": edit(self.base, "considered: []", 'considered: ["PRD-1@2"]'),
            "a bad coverage status": edit(self.base, "| IDEA-04 | none | not a screen |", "| IDEA-04 | none | done |"),
            "a malformed coverage row": edit(self.base, "| IDEA-04 | none | not a screen |", "| IDEA-04 |"),
            "a missing item link": edit(self.base, IDEA01_LINK, ""),
        }
        for name, text in cases.items():
            with self.subTest(name):
                self.p.write_dsn(text)
                a = self.cli("check", "--before-amend", "DSN-001")
                b = self.cli("check", "DSN-001")
                self.assertEqual((a.code, b.code), (1, 1), (a, b))
                self.assertRegex(a.lines[-1], rf"^INVALID: \d+ error\(s\) in {re.escape(FILE)}$")

    def test_approval_changelog_and_placeholder_rules_apply(self):
        cases = {
            "approved with a marker": edit(self.base, "status: draft ", "status: approved "),
            "no row for the version": edit(self.base, "\nversion: 1\n", "\nversion: 2\n"),
            "an HTML comment": edit(self.base, "## 1. Scope\n\n", "## 1. Scope\n\n<!-- x -->\n\n"),
            "a fill placeholder": edit(self.base, "## 1. Scope\n\n", "## 1. Scope\n\n[[fill: x]]\n\n"),
        }
        for name, text in cases.items():
            with self.subTest(name):
                r = self.check(text, "--before-amend")
                self.assertEqual(r.code, 1, r)

    def test_frontmatter_rules_apply_except_the_canvas_format_equality(self):
        r = self.check(edit(self.base, "canvas_format: 3", "canvas_format: 2"), "--before-amend")
        self.assertEqual(r.code, 0, r)
        r = self.check(edit(self.base, "canvas_format: 3", "canvas_format: 0"), "--before-amend")
        self.assertEqual(r.code, 1, r)

    def test_the_unenforced_rules_are_not_errors_even_together(self):
        text = edit(self.base, "canvas_format: 3", "canvas_format: 2")
        text = set_field(text, "BRD-04", "sha256", '"' + "0" * 64 + '"')
        text = set_field(text, "BRD-03", "file", '"Gone.dc.html"')
        self.p.add_board("Settings.dc.html", SETTINGS)
        self.p.write_brn(ideas=dict(IDEAS, **{"IDEA-03": ("A weekly report page", "parked")}))
        r = self.check(text, "--before-amend")
        self.assertEqual(r.code, 0, r)

    def test_a_dsn_failing_the_check_before_the_amend(self):
        r = self.check(edit(self.base, "type: design", "type: spec"), "--before-amend")
        self.assertEqual(r.code, 1, r)
        self.assertRegex(self.errors(r)[0], r"\(frontmatter\)$")

    def test_a_boards_folder_that_cannot_be_used_cannot_run(self):
        self.p.write_dsn(self.base)
        for raw in (b"not json {", b'{"v": 4, "boards": {"Home.dc.html": {}}}'):
            with self.subTest(raw=raw):
                self.p.put("docs/specs/design/DSN-001/boards/canvas.json", raw)
                r = self.cli("check", "--before-amend", "DSN-001")
                self.assertEqual((r.code, len(r.lines)), (2, 1), r)
                self.assertRegex(r.lines[0], r"^Cannot run: .+\.$")

    def test_a_board_file_that_cannot_be_read_cannot_run(self):
        self.p.write_dsn(self.base)
        (self.p.boards_dir() / "Report.dc.html").unlink()
        r = self.cli("check", "--before-amend", "DSN-001")
        self.assertEqual((r.code, len(r.lines)), (2, 1), r)
        self.assertRegex(r.lines[0], r"^Cannot run: .+\.$")

    def test_the_option_may_come_before_or_after_the_root(self):
        self.p.write_dsn(self.base)
        for argv in (["check", "--before-amend", "--root", str(self.p.root), "DSN-001"],
                     ["check", "--root", str(self.p.root), "--before-amend", "DSN-001"],
                     ["check", "--root", str(self.p.root), "DSN-001", "--before-amend"]):
            with self.subTest(argv=argv):
                r = run_arms(argv, self.p.elsewhere)
                self.assertEqual((r.code, r.lines), (0, [f"OK {FILE} (before amend)"]), r)


if __name__ == "__main__":
    unittest.main()
