"""Unit tests for the precompact skill's checker, scripts/check_handoff.py (SPEC-015 VER-01; IF-01, BEH-08).

Each case builds a project folder with a handoff in a temporary folder and runs the script as a subprocess twice:
with this interpreter's packages and with `-S`, which hides every site-packages directory. The output must be the
same both ways, never end in a traceback, and leave the folder as it was.

Readings this test pins where SPEC-015 leaves a choice (listed for Bryan in the end-of-workflow notes):
- a file-level problem (a missing file) is reported at line 0;
- `[[fill:` inside a code span or a fenced block is quoted text, not a leftover placeholder, so a handoff about this
  skill can name the form; the assets never put a placeholder in backticks;
- a relative link target is accepted when it exists under the root or beside the file that holds it;
- `handoff: clean` needs no problem and no warning; with warnings only, the summary line counts them and exit is 0;
- headings, shapes and references inside fenced blocks are not read;
- `#Lnn-Lmm` is stripped as `#Lnn` is.

Run from the repository root:
    python3 -B src/tests/precompact/test_check_handoff.py
"""
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
SCRIPT = ROOT / "src/claude/DevForgeAI/skills/precompact/scripts/check_handoff.py"
HANDOFF = "devforgeai/handoff/feat-export"

START_HERE = """\
# Start here: CSV export on feat/export

## 1. What this is

Adding CSV export to the reports page. Project root: `{root}`. Branch `feat/export`. Written 2026-10-05 14:00 UTC by
session abc123.

## 2. Verified state

- Branch `feat/export` is 2 commits ahead of `origin/main` [checked: git status --porcelain=v2 -b -> ahead 2]
- The last commit is `1a2b3c4` "add exporter"
  [checked: git log -n 5 --oneline -> 1a2b3c4 add exporter]
- The unit tests passed (unverified: the session's last test run, 2026-10-04)

## 3. Decisions

### Decided

- CSV only, no Excel: Dana, 2026-10-04, "CSV is enough for now".

### Open

- Which delimiter, comma or semicolon: the user hasn't chosen.

## 4. Read first

1. `docs/plan.md` - the plan and its checkpoints; read it first, it is the source of truth for the steps.
2. `src/export.py:10` - the exporter; read it before changing the format.

When something you need isn't here, search the repository and memory before asking the user.

## 5. Outstanding

1. Add the header row. Next: edit `src/export.py:10`. Waits for: nothing.

## 6. Rules, traps and learnings

- Never commit generated files.

## 7. Before acting

- `git log -n 1 --oneline` shows `1a2b3c4`.
"""

RESUME = """\
Continue the CSV export work in {root}.
Read {start} first, then TASKS.md in the same folder.
If the branch checked out isn't the one START-HERE section 1 names, stop and tell the user.
Run START-HERE section 7, then go on with the first item of section 5.
Ask the user before anything sections 3 or 5 say is theirs.
When something you need isn't in the handoff, search the repository and the memory index before asking.
"""

TASKS = """\
# Tasks: CSV export

## Done

- [x] Exporter written: commit `1a2b3c4`, 2026-10-05.

## Next

- [ ] Header row. Next: edit `src/export.py`.
"""

# The forms references take in practice (VER-01): none of them is refused.
PRACTICAL_FORMS = """\

## 8. Notes

- Commands: `git push origin feat/export`, `claude plugin test src/plugin`, `grep -n "<term>" <path>`.
- Globs and patterns: `src/**/*.test.ts`, `tmp/plans/<date>-<topic>.md`, `docs/*`.
- URLs: `https://github.com/o/r/pull/93` and [the PR](https://github.com/o/r/pull/93), [mail](mailto:a@b.example),
  [section 1](#1-what-this-is).
- Slash commands: `/compact`, `/devforgeai:precompact`, `/reload-plugins`.
- Branches and versions: `docs/precompact`, `origin/main`, `0.25.0`, `v2.1`.
- Home paths: `~/.claude/projects/x/memory/MEMORY.md`, `~/code/papercuts.md`.
- References with lines: `src/export.py:10-20`, `src/export.py#L10`, `missing/file.py:3`.
- Templates: `<noreply@example.com>`, `<main sha>`, `Array<string>`, `@scope/pkg`, `owner/repo`.
- A quote: the user said "do it today", and a link to the plan: [plan](docs/plan.md).

```text
## 1. What this is
[[fill: a quoted template line inside a fence is not a placeholder]]
```

The placeholder form is `[[fill: what]]`, written in backticks here.
"""

READ_FIRST_EXTRA = """\
3. `src/export.py#L10-L20` - the format's lines.
4. `~/notes/export.md` - the user's notes, outside the project.
5. A scratch script, valid until the session ends (session-only):
   `scratch/run.sh` - reproduces the bug.
6. `docs/` - the documents folder.
"""


def write(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


class Handoff:
    """A project folder with a complete handoff; edit() changes one file before a run."""

    def __init__(self, tmp):
        self.root = Path(tmp) / "project"
        self.home = Path(tmp) / "home"
        self.dir = self.root / HANDOFF
        write(self.root / "docs/plan.md", "# Plan\n")
        write(self.root / "src/export.py", "print('csv')\n")
        write(self.home / "notes/export.md", "notes\n")
        write(self.root / "devforgeai/handoff/.gitignore", "*\n")
        self.files = {
            "START-HERE.md": START_HERE.format(root=self.root),
            "RESUME-PROMPT.md": RESUME.format(root=self.root, start=self.dir / "START-HERE.md"),
            "TASKS.md": TASKS,
        }
        self.save()

    def save(self):
        for name, text in self.files.items():
            write(self.dir / name, text)

    def edit(self, name, old, new):
        text = self.files[name]
        assert text.count(old) == 1, (name, old)
        self.files[name] = text.replace(old, new)
        self.save()

    def run(self, *extra, handoff=HANDOFF, cwd=None):
        args = list(extra) + ["--root", str(self.root), handoff]
        return run_both(args, cwd=cwd or self.root, home=self.home)


def snapshot(folder):
    return {str(p.relative_to(folder)): p.read_bytes() for p in Path(folder).rglob("*") if p.is_file()}


def run_both(args, cwd, home):
    env = dict(os.environ, HOME=str(home), PYTHONDONTWRITEBYTECODE="1")
    before = snapshot(cwd)
    results = []
    for flags in (["-B"], ["-B", "-S"]):
        p = subprocess.run([sys.executable, *flags, str(SCRIPT), *args], cwd=cwd, env=env,
                           capture_output=True, text=True, timeout=60)
        results.append(p)
    a, b = results
    assert (a.returncode, a.stdout, a.stderr) == (b.returncode, b.stdout, b.stderr), (a, b)
    assert "Traceback" not in a.stderr, a.stderr
    assert snapshot(cwd) == before, "the script changed the folder"
    return a


class Clean(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.h = Handoff(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def test_a_complete_handoff_is_clean(self):
        p = self.h.run()
        self.assertEqual((p.returncode, p.stdout), (0, "handoff: clean\n"), p.stdout + p.stderr)

    def test_the_forms_references_take_in_practice_are_clean(self):
        self.h.edit("START-HERE.md", "When something you need", READ_FIRST_EXTRA + "\nWhen something you need")
        self.h.files["START-HERE.md"] += PRACTICAL_FORMS
        self.h.save()
        p = self.h.run()
        self.assertEqual((p.returncode, p.stdout), (0, "handoff: clean\n"), p.stdout + p.stderr)

    def test_nothing_outstanding_is_a_valid_section_5(self):
        self.h.edit("START-HERE.md", "1. Add the header row. Next: edit `src/export.py:10`. Waits for: nothing.",
                    "Nothing outstanding.")
        self.assertEqual(self.h.run().returncode, 0)

    def test_crlf_line_ends_read_the_same(self):
        for name in self.h.files:
            (self.h.dir / name).write_bytes(self.h.files[name].replace("\n", "\r\n").encode())
        p = self.h.run()
        self.assertEqual((p.returncode, p.stdout), (0, "handoff: clean\n"), p.stdout)

    def test_more_headings_after_the_last_required_one_and_level_3_anywhere(self):
        self.h.edit("START-HERE.md", "## 4. Read first\n", "## 4. Read first\n\n### Specs\n")
        self.h.edit("TASKS.md", "## Next\n", "## Next\n\n### Soon\n")
        self.h.files["TASKS.md"] += "\n## Earlier work: PDF export\n\n- [x] Spike: 2026-09-30.\n"
        self.h.save()
        self.assertEqual(self.h.run().returncode, 0)

    def test_a_relative_path_for_the_handoff_folder_and_the_default_root(self):
        p = run_both([HANDOFF], cwd=self.h.root, home=self.h.home)
        self.assertEqual((p.returncode, p.stdout), (0, "handoff: clean\n"), p.stdout)


class Problems(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.h = Handoff(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def assertProblem(self, file, line, text):
        p = self.h.run()
        self.assertEqual(p.returncode, 1, p.stdout + p.stderr)
        where = f"{HANDOFF}/{file}" if not file.startswith("devforgeai/") else file
        wanted = [l for l in p.stdout.splitlines() if l.startswith(f"{where}:{line}: ") and text in l]
        self.assertTrue(wanted, f"no '{where}:{line}: ...{text}...' in:\n{p.stdout}")
        self.assertRegex(p.stdout.splitlines()[-1], r"^handoff: [1-9]\d* problems, \d+ warnings$")
        return p

    def test_a_missing_file(self):
        for name in ("START-HERE.md", "TASKS.md", "RESUME-PROMPT.md"):
            with self.subTest(name):
                (self.h.dir / name).unlink()
                self.assertProblem(name, 0, "missing")
                self.h.save()

    def test_a_missing_heading(self):
        self.h.edit("START-HERE.md", "## 6. Rules, traps and learnings\n", "")
        self.assertProblem("START-HERE.md", 39, "## 6. Rules, traps and learnings")

    def test_a_misordered_heading(self):
        self.h.edit("START-HERE.md", "## 3. Decisions\n", "## 4. Decisions\n")
        self.assertProblem("START-HERE.md", 15, "## 3. Decisions")

    def test_a_tasks_heading_missing(self):
        self.h.edit("TASKS.md", "## Next\n", "## Later\n")
        self.assertProblem("TASKS.md", 7, "## Next")

    def test_a_heading_inside_a_fence_doesnt_count(self):
        self.h.edit("START-HERE.md", "## 7. Before acting\n", "```\n## 7. Before acting\n```\n")
        self.assertProblem("START-HERE.md", 44, "## 7. Before acting")

    def test_a_section_2_bullet_with_no_check_or_unverified(self):
        self.h.edit("START-HERE.md", "- The unit tests passed (unverified: the session's last test run, 2026-10-04)",
                    "- The unit tests passed")
        self.assertProblem("START-HERE.md", 13, "[checked:")

    def test_a_check_with_no_result(self):
        self.h.edit("START-HERE.md", "[checked: git status --porcelain=v2 -b -> ahead 2]",
                    "[checked: git status]")
        self.assertProblem("START-HERE.md", 10, "[checked:")

    def test_a_decision_with_no_date(self):
        self.h.edit("START-HERE.md", "Dana, 2026-10-04, ", "Dana, ")
        self.assertProblem("START-HERE.md", 19, "date")

    def test_a_decision_with_no_quote(self):
        self.h.edit("START-HERE.md", '"CSV is enough for now"', "CSV is enough for now")
        self.assertProblem("START-HERE.md", 19, "quote")

    def test_an_outstanding_item_with_no_next(self):
        self.h.edit("START-HERE.md", "Next: edit `src/export.py:10`. ", "")
        self.assertProblem("START-HERE.md", 34, "Next:")

    def test_an_outstanding_item_with_no_waits_for(self):
        self.h.edit("START-HERE.md", " Waits for: nothing.", "")
        self.assertProblem("START-HERE.md", 34, "Waits for:")

    def test_an_empty_section_5(self):
        self.h.edit("START-HERE.md", "1. Add the header row. Next: edit `src/export.py:10`. Waits for: nothing.\n", "")
        self.assertProblem("START-HERE.md", 32, "Nothing outstanding.")

    def test_a_resume_prompt_over_40_lines(self):
        self.h.files["RESUME-PROMPT.md"] += "".join(f"Line {i}.\n" for i in range(35))
        self.h.save()
        self.assertProblem("RESUME-PROMPT.md", 41, "40 lines")

    def test_a_resume_prompt_without_the_absolute_path(self):
        self.h.edit("RESUME-PROMPT.md", str(self.h.dir / "START-HERE.md"), f"{HANDOFF}/START-HERE.md")
        self.assertProblem("RESUME-PROMPT.md", 0, "absolute path")

    def test_a_leftover_placeholder(self):
        self.h.edit("TASKS.md", "- [ ] Header row.", "- [ ] [[fill: the next step]]")
        self.assertProblem("TASKS.md", 9, "[[fill:")

    def test_a_read_first_path_that_doesnt_exist(self):
        self.h.edit("START-HERE.md", "2. `src/export.py:10`", "2. `src/exporter.py:10`")
        self.assertProblem("START-HERE.md", 28, "src/exporter.py")

    def test_a_link_target_that_doesnt_exist(self):
        self.h.edit("START-HERE.md", "- Never commit generated files.",
                    "- Never commit generated files ([why](docs/why.md)).")
        self.assertProblem("START-HERE.md", 38, "docs/why.md")

    def test_a_missing_reference_is_kept_when_marked_not_yet_created(self):
        self.h.edit("START-HERE.md", "- Never commit generated files.",
                    "- Never commit generated files ([why](docs/why.md), not yet created).")
        self.assertEqual(self.h.run().returncode, 1)  # "not yet created" isn't the marker's form
        self.h.edit("START-HERE.md", "not yet created).", "(not yet created)).")
        self.assertEqual(self.h.run().returncode, 0)

    def test_a_missing_gitignore(self):
        (self.h.root / "devforgeai/handoff/.gitignore").unlink()
        self.assertProblem("devforgeai/handoff/.gitignore", 0, "*")

    def test_a_gitignore_without_the_star(self):
        write(self.h.root / "devforgeai/handoff/.gitignore", "*.tmp\n")
        self.assertProblem("devforgeai/handoff/.gitignore", 0, "*")


class Warnings(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.h = Handoff(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def test_start_here_over_250_lines(self):
        self.h.files["START-HERE.md"] += "".join(f"\nNote {i}.\n" for i in range(110))
        self.h.save()
        p = self.h.run()
        self.assertEqual(p.returncode, 0, p.stdout)
        self.assertIn(f"{HANDOFF}/START-HERE.md:251: warning: ", p.stdout)
        self.assertEqual(p.stdout.splitlines()[-1], "handoff: 0 problems, 1 warnings")

    def test_a_relative_date_word_outside_quotes(self):
        self.h.edit("START-HERE.md", "- Never commit generated files.",
                    '- Never commit generated files; we learned that yesterday. Dana: "ship it today".')
        p = self.h.run()
        self.assertEqual(p.returncode, 0, p.stdout)
        self.assertIn(f"{HANDOFF}/START-HERE.md:38: warning: ", p.stdout)
        self.assertIn("yesterday", p.stdout)
        self.assertNotIn("today", p.stdout.replace("yesterday", ""))
        self.assertEqual(p.stdout.splitlines()[-1], "handoff: 0 problems, 1 warnings")


class CantRun(unittest.TestCase):
    def test_a_missing_handoff_folder_exits_2(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = run_both(["--root", tmp, "devforgeai/handoff/none"], cwd=tmp, home=tmp)
            self.assertEqual(p.returncode, 2)
            self.assertIn("devforgeai/handoff/none", p.stdout + p.stderr)


if __name__ == "__main__":
    unittest.main()
