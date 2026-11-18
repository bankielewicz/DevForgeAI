"""Unit tests for the precompact skill's scripts/handoff_paths.py (SPEC-015 VER-12; IF-02, BEH-02).

Each case builds a home folder and a project in a temporary folder and runs the script as a subprocess, with this
interpreter's packages and with `-S`. Every run passes --home and sets HOME to the temporary home: no test reads,
lists or deletes anything under the real home folder, where live handoffs are.

Run from the repository root:
    python3 -B src/tests/precompact/test_handoff_paths.py
"""
import hashlib
import json
import os
import re
import subprocess
import sys
import tempfile
import time
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
SCRIPT = ROOT / "src/claude/DevForgeAI/skills/precompact/scripts/handoff_paths.py"
SESSION = "aaaa1111-2222-3333-4444-555566667777"
DAY = 86400
GIT_ENV = {"GIT_CONFIG_NOSYSTEM": "1", "GIT_CONFIG_GLOBAL": os.devnull, "GIT_AUTHOR_NAME": "T", "GIT_AUTHOR_EMAIL": "t@example.com",
           "GIT_COMMITTER_NAME": "T", "GIT_COMMITTER_EMAIL": "t@example.com"}


def git(cwd, *args):
    subprocess.run(["git", *args], cwd=cwd, env=dict(os.environ, **GIT_ENV), check=True, capture_output=True)


def start_here(title="CSV export", branch="feat/export", session="s1"):
    return (f"# Start here: {title}\n\n## 1. What this is\n\nWork.\n\n- Project root: `/p`\n- Branch: `{branch}`, no upstream\n"
            f"- Written: 2026-10-05 10:00 UTC, by session {session}\n\n## 2. Verified state\n")


def handoff(folder, age_days=0, **kw):
    """A handoff folder whose files were written `age_days` ago."""
    folder.mkdir(parents=True, exist_ok=True)
    when = time.time() - age_days * DAY
    for name, text in (("START-HERE.md", start_here(**kw)), ("TASKS.md", "# Tasks\n"), ("RESUME-PROMPT.md", "Continue.\n")):
        (folder / name).write_text(text, encoding="utf-8")
        os.utime(folder / name, (when, when))
    os.utime(folder, (when, when))
    return folder


def snapshot(*folders):
    out = {}
    for folder in folders:
        for p in sorted(Path(folder).rglob("*")):
            if ".git" in p.parts:
                continue
            out[str(p)] = p.read_bytes() if p.is_file() and not p.is_symlink() else None
    return out


class Case(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.tmp = Path(self._tmp.name).resolve()
        self.home = self.tmp / "home"
        self.home.mkdir()
        self.project = self.tmp / "My Project"
        self.project.mkdir()

    def tearDown(self):
        for p in self.tmp.rglob("*"):  # a test may have made a folder unreadable
            if p.is_dir() and not p.is_symlink():
                try:
                    p.chmod(0o755)
                except OSError:
                    pass
        self._tmp.cleanup()

    def run_script(self, *extra, root=None, session=SESSION, expect=0):
        args = ["--root", str(root or self.project), "--session", session, "--home", str(self.home), *extra]
        env = dict(os.environ, HOME=str(self.home), USERPROFILE=str(self.home), PYTHONDONTWRITEBYTECODE="1", **GIT_ENV)
        results = []
        for flags in (["-B"], ["-B", "-S"]):
            results.append(subprocess.run([sys.executable, *flags, str(SCRIPT), *args], cwd=self.tmp, env=env,
                                          capture_output=True, text=True, timeout=60))
        a, b = results
        self.assertNotIn("Traceback", a.stderr + b.stderr)
        self.assertEqual((a.returncode, b.returncode), (expect, expect), a.stdout + a.stderr)
        return a, b

    def lines(self, *extra, **kw):
        a, _ = self.run_script(*extra, **kw)
        out = {}
        for line in a.stdout.splitlines():
            key, _, value = line.partition(": ")
            out.setdefault(key, []).append(value)
        return out

    def key(self, folder):
        name = re.sub(r"[^A-Za-z0-9._-]+", "-", Path(folder).name)
        return f"{name}-{hashlib.sha256(os.path.normcase(os.path.realpath(folder)).encode()).hexdigest()[:8]}"

    def store(self, folder=None):
        return self.home / ".devforgeai" / self.key(folder or self.project) / "handoff"


class Paths(Case):
    def test_project_folder_and_fallback_without_git(self):
        out = self.lines()
        self.assertEqual(out["project"], [self.key(self.project)])
        self.assertRegex(out["project"][0], r"^My-Project-[0-9a-f]{8}$")
        self.assertEqual(out["session"], [SESSION])
        self.assertEqual(out["folder"], [str(self.store() / SESSION)])
        self.assertEqual(out["fallback"], [str(self.project / "devforgeai/handoff" / SESSION)])

    def test_a_worktree_has_the_main_checkouts_key_and_a_clone_its_own(self):
        git(self.project, "init", "-q", "-b", "main")
        (self.project / "a.txt").write_text("a\n")
        git(self.project, "add", "a.txt")
        git(self.project, "commit", "-q", "-m", "a")
        tree = self.tmp / "trees" / "feature"
        git(self.project, "worktree", "add", "-q", "-b", "feature", str(tree))
        clone = self.tmp / "clone"
        git(self.tmp, "clone", "-q", str(self.project), str(clone))
        main, wt, cl = self.lines(), self.lines(root=tree), self.lines(root=clone)
        self.assertEqual(main["project"], [self.key(self.project)])
        self.assertEqual(wt["project"], main["project"])
        self.assertEqual(wt["folder"], main["folder"])
        self.assertEqual(wt["fallback"], [str(tree / "devforgeai/handoff" / SESSION)])  # the fallback stays with the checkout
        self.assertEqual(cl["project"], [self.key(clone)])
        self.assertNotEqual(cl["project"], main["project"])

    def test_a_parent_repository_isnt_the_projects(self):
        git(self.tmp, "init", "-q", "-b", "main")  # the eval workspace's shape: home/ is a repository, the project is below it
        self.assertEqual(self.lines()["project"], [self.key(self.project)])

    def test_an_unsubstituted_or_empty_session_gets_a_time_name(self):
        for value in ("", "${CLAUDE_SESSION_ID}"):
            with self.subTest(value):
                out = self.lines(session=value)
                self.assertRegex(out["session"][0], r"^session-\d{8}T\d{6}Z$")
                self.assertEqual(out["folder"], [str(self.store() / out["session"][0])])

    def test_a_session_that_isnt_one_folder_name_is_refused(self):
        for value in ("../x", "a/b", ".."):
            with self.subTest(value):
                self.run_script(session=value, expect=2)

    def test_a_missing_root_exits_2(self):
        self.run_script(root=self.tmp / "none", expect=2)

    def test_it_creates_no_folder_and_no_file(self):
        before = snapshot(self.home, self.project)
        self.lines()
        self.assertEqual(snapshot(self.home, self.project), before)
        self.assertFalse((self.home / ".devforgeai").exists())


class Listing(Case):
    def test_other_handoffs_of_the_store_and_the_project_newest_first(self):
        handoff(self.store() / SESSION, title="mine")
        a = handoff(self.store() / "other-a", age_days=3, title="Pagination", branch="feat/pages")
        b = handoff(self.project / "devforgeai/handoff/feat-export", age_days=1, title="Old layout")  # versions 1 and 2
        c = handoff(self.project / "devforgeai/handoff/feat-export/v3-session", age_days=2, title="Version 3 layout")
        handoff(self.project / "devforgeai/handoff" / SESSION, title="my fallback")
        (self.store() / "empty").mkdir()
        other = self.lines("--no-prune")["other"]
        self.assertEqual([o.split(" | ")[0] for o in other], [str(b), str(c), str(a)])
        self.assertRegex(other[2], r"^\S.* \| \d{4}-\d{2}-\d{2} \| feat/pages \| Pagination$")
        self.assertTrue(other[0].endswith(" | feat/export | Old layout"))

    def test_at_most_ten_and_a_question_mark_for_what_is_missing(self):
        for n in range(12):
            handoff(self.store() / f"s{n:02d}", age_days=n, title=f"work {n}")
        odd = self.store() / "odd"
        odd.mkdir()
        (odd / "START-HERE.md").write_text("no heading, no branch | pipe\n", encoding="utf-8")
        other = self.lines("--no-prune")["other"]
        self.assertEqual(len(other), 10)
        self.assertTrue(other[0].startswith(str(odd) + " | "))
        self.assertTrue(other[0].endswith(" | ? | ?"))
        self.assertTrue(other[1].endswith(" | work 0"))

    def test_none_listed_when_there_are_none(self):
        handoff(self.store() / SESSION)
        self.assertNotIn("other", self.lines())


class Pruning(Case):
    def config(self, text):
        (self.home / ".devforgeai").mkdir(exist_ok=True)
        (self.home / ".devforgeai/config.json").write_text(text, encoding="utf-8")

    def scene(self):
        s = self.store()
        self.old = handoff(s / "old", age_days=31)
        self.new = handoff(s / "new", age_days=29)
        self.own = handoff(s / SESSION, age_days=90)
        self.bare = s / "no-start-here"
        self.bare.mkdir()
        (self.bare / "notes.md").write_text("x\n")
        os.utime(self.bare / "notes.md", (time.time() - 90 * DAY,) * 2)
        self.target = handoff(self.tmp / "elsewhere", age_days=90)
        self.link = s / "link"
        self.link.symlink_to(self.target, target_is_directory=True)
        self.in_project = handoff(self.project / "devforgeai/handoff/feat-old", age_days=400)
        self.other_project = handoff(self.home / ".devforgeai/Other-12345678/handoff/old", age_days=400)

    def test_only_an_old_handoff_folder_of_this_projects_store_is_deleted(self):
        self.scene()
        out = self.lines()
        self.assertEqual(out["pruned"], [str(self.old)])
        self.assertFalse(self.old.exists())
        for kept in (self.new, self.own, self.bare, self.target, self.in_project, self.other_project):
            self.assertTrue(kept.exists(), kept)
        self.assertTrue(self.link.is_symlink())
        self.assertNotIn(str(self.old), " ".join(out.get("other", [])))

    def test_the_newest_file_counts(self):
        self.scene()
        (self.old / "TASKS.md").touch()
        self.assertNotIn("pruned", self.lines())
        self.assertTrue(self.old.exists())

    def test_no_prune_and_retention_zero_delete_nothing(self):
        self.scene()
        out = self.lines("--no-prune")
        self.assertEqual(out["prune"], ["skipped: --no-prune"])
        self.assertTrue(self.old.exists())
        self.config('{"handoffRetentionDays": 0}')
        self.assertNotIn("pruned", self.lines())
        self.assertTrue(self.old.exists())

    def test_the_setting(self):
        for text, gone in (('{"handoffRetentionDays": 40}', False), ('{"handoffRetentionDays": 7}', True),
                           ('{"handoffRetentionDays": "7"}', False), ("not json", False), ('{"other": 1}', False),
                           ('{"handoffRetentionDays": true}', False), ('{"handoffRetentionDays": -1}', False)):
            with self.subTest(text):
                old = handoff(self.store() / "old", age_days=29 if "7" in text or "40" in text else 20)
                handoff(self.store() / "older", age_days=35)
                self.config(text)
                self.lines()
                self.assertEqual(old.exists(), not gone, text)
                self.assertEqual((self.store() / "older").exists(), "40" in text, text)  # 30 unless a number says otherwise

    def test_a_retention_that_isnt_a_finite_number_of_days_never_deletes_what_is_new(self):
        """NaN compares false with everything, and a fraction of a day would reach live sessions' folders (the reviews
        of 4d76e83): a non-finite value means 30, and a positive one below 1 means 1."""
        for text, pruned in (('{"handoffRetentionDays": NaN}', ["old"]), ('{"handoffRetentionDays": Infinity}', ["old"]),
                             ('{"handoffRetentionDays": 0.0001}', ["old", "week"])):
            with self.subTest(text):
                s = self.store()
                handoff(s / "old", age_days=31)
                handoff(s / "week", age_days=7)
                live = handoff(s / "live", age_days=0.25)
                self.config(text)
                out = self.lines()
                self.assertEqual(sorted(Path(x).name for x in out.get("pruned", [])), pruned)
                self.assertTrue(live.exists())

    def test_a_retention_too_large_for_a_float_means_the_default(self):
        old = handoff(self.store() / "old", age_days=31)
        new = handoff(self.store() / "new", age_days=29)
        self.config('{"handoffRetentionDays": 1' + "0" * 400 + "}")
        out = self.lines()
        self.assertEqual([Path(x).name for x in out["pruned"]], ["old"])
        self.assertTrue(new.exists() and not old.exists())

    def test_a_folder_whose_age_cant_be_read_is_listed_with_a_question_mark(self):
        """A folder can vanish between the listing and the read, when two sessions prune at once (the review of b58476d)."""
        import importlib.util
        spec = importlib.util.spec_from_file_location("handoff_paths", SCRIPT)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        gone = str(self.store() / "gone")
        self.assertEqual(module.newest(gone), float("inf"))
        self.assertEqual(module.describe(gone), f"other: {gone} | ? | ? | ?")

    def test_a_store_reached_through_a_link_isnt_pruned(self):
        real = self.tmp / "elsewhere" / "handoff"
        old = handoff(real / "old", age_days=90)
        self.store().parent.mkdir(parents=True)
        self.store().symlink_to(real, target_is_directory=True)
        out = self.lines()
        self.assertTrue(old.exists())
        self.assertTrue(any(v.startswith("skipped: ") and "link" in v for v in out["prune"]), out)
        self.assertNotIn("pruned", out)

    def test_keep_spares_the_handoff_this_session_resumed_from(self):
        s = self.store()
        resumed = handoff(s / "resumed", age_days=60)
        handoff(s / "old", age_days=60)
        out = self.lines("--keep", str(resumed / "START-HERE.md"))
        self.assertEqual([Path(x).name for x in out["pruned"]], ["old"])
        self.assertTrue(resumed.exists())
        out = self.lines("--keep", str(resumed))
        self.assertNotIn("pruned", out)
        self.assertTrue(resumed.exists())

    @unittest.skipIf(hasattr(os, "geteuid") and os.geteuid() == 0, "root deletes anything")
    def test_a_folder_that_cant_be_deleted_is_named_and_the_run_goes_on(self):
        old = handoff(self.store() / "old", age_days=31)
        locked = old / "sub"
        locked.mkdir()
        (locked / "f").write_text("x")
        os.utime(locked / "f", (time.time() - 40 * DAY,) * 2)
        locked.chmod(0o500)
        out = self.lines()
        self.assertTrue(any(v.startswith(f"skipped: {old}") for v in out["prune"]), out)
        self.assertTrue(old.exists())
        self.assertEqual(out["folder"], [str(self.store() / SESSION)])


if __name__ == "__main__":
    unittest.main()
