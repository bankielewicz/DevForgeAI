"""Tests for SPEC-013's prune script (src/claude/DevForgeAI/progress/prune.py), VER-17.

PruneRules checks IF-04 and BEH-19's confinement: only run and session folders under devforgeai/progress/, named
by their patterns, older than --days, never followed through a symbolic link. PruneRulesUnderS runs every test with
the script under `python3 -S` (QR-04). Each spawn uses -B, so no __pycache__ lands in the plugin folder, which deploys.

Run from the repository root:
    PYTHONDONTWRITEBYTECODE=1 python3 -B -m pytest -q -p no:cacheprovider src/tests/progress
"""
import os
import subprocess
import sys
import tempfile
import time
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
PRUNE = ROOT / "src/claude/DevForgeAI/progress/prune.py"
DAY = 86400
OLD_RUN = "20260901T120000Z-brainstorm-0a1b2c3d"
NEW_RUN = "20261002T120000Z-architecture-4e5f6a7b"
OLD_SESSION = "0bca858d-4aa1-4888-9112-a05bef6011c1"
NEW_SESSION = "f9d52ee2-aa0b-4908-a9c4-393328435e15"


class Base(unittest.TestCase):
    INTERPRETER = (sys.executable, "-B")

    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name) / "project"
        self.root.mkdir()
        self.progress = self.root / "devforgeai/progress"
        self.now = time.time()

    def tearDown(self):
        self._tmp.cleanup()

    def prune(self, *args):
        return subprocess.run(list(self.INTERPRETER) + [str(PRUNE), "prune"] + [str(a) for a in args], cwd=ROOT,
                              capture_output=True, text=True)

    def folder(self, path, age_days, files=("events.jsonl", "state.json")):
        """A folder holding files, every one (and the folder) last modified age_days ago."""
        path.mkdir(parents=True, exist_ok=True)
        for name in files:
            (path / name).write_text("{}\n")
        self.age(path, age_days)
        return path

    def age(self, path, age_days):
        when = self.now - age_days * DAY
        targets = [path] if not path.is_dir() else [Path(d) / n for d, ds, fs in os.walk(path) for n in ds + fs] + [path]
        for target in targets:
            os.utime(target, (when, when), follow_symlinks=False)

    def run_dir(self, name, age_days, **kw):
        return self.folder(self.progress / "runs" / name, age_days, **kw)

    def session_dir(self, name, age_days):
        return self.folder(self.progress / "sessions" / name, age_days, files=("current.json", "adapter.log"))

    def assert_pruned(self, proc, runs, sessions):
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertEqual(proc.stdout, "pruned %d runs, %d sessions\n" % (runs, sessions))
        self.assertEqual(proc.stderr, "")

    def assert_refused(self, proc):
        self.assertEqual(proc.returncode, 2)
        self.assertEqual(proc.stdout, "")
        self.assertEqual(len(proc.stderr.splitlines()), 1, proc.stderr)


class PruneRules(Base):
    """VER-17: IF-04 removes only old run and session folders, and nothing it can't vouch for."""

    def test_old_folders_go_and_newer_ones_stay(self):
        old_run, new_run = self.run_dir(OLD_RUN, 40), self.run_dir(NEW_RUN, 2)
        old_session, new_session = self.session_dir(OLD_SESSION, 40), self.session_dir(NEW_SESSION, 2)
        self.assert_pruned(self.prune("--root", self.root, "--days", 30), 1, 1)
        self.assertFalse(old_run.exists())
        self.assertFalse(old_session.exists())
        self.assertTrue((new_run / "events.jsonl").exists())
        self.assertTrue((new_session / "adapter.log").exists())

    def test_the_kept_session_and_run_stay_however_old(self):
        run, session = self.run_dir(OLD_RUN, 40), self.session_dir(OLD_SESSION, 40)
        proc = self.prune("--root", self.root, "--days", 30, "--keep-session", OLD_SESSION, "--keep-run", OLD_RUN)
        self.assert_pruned(proc, 0, 0)
        self.assertTrue(run.exists())
        self.assertTrue(session.exists())

    def test_a_folder_with_one_recent_file_stays(self):
        run = self.run_dir(OLD_RUN, 40)
        (run / "pending.json").write_text("{}\n")
        self.age(run / "pending.json", 1)
        self.assert_pruned(self.prune("--root", self.root, "--days", 30), 0, 0)
        self.assertTrue(run.exists())

    def test_names_that_match_neither_pattern_stay(self):
        odd = [self.run_dir("not-a-run", 40), self.run_dir("20260901T120000Z-Brainstorm-0a1b2c3d", 40),
               self.folder(self.progress / "sessions" / "not-a-session-id", 40),
               self.folder(self.progress / "sessions" / OLD_SESSION.upper(), 40)]
        self.assert_pruned(self.prune("--root", self.root, "--days", 30), 0, 0)
        for path in odd:
            self.assertTrue(path.exists(), path)

    def test_files_beside_the_folders_and_outside_progress_stay(self):
        self.progress.mkdir(parents=True)
        loose = [self.progress / "current.json", self.progress / "adapter.log", self.progress / ".gitignore"]
        (self.progress / "runs").mkdir()
        loose.append(self.progress / "runs" / "stray.txt")
        doc = self.root / "docs/specs/brainstorm/BRN-001.md"
        doc.parent.mkdir(parents=True)
        loose.append(doc)
        for path in loose:
            path.write_text("x\n")
            self.age(path, 400)
        manifests = self.folder(self.root / "devforgeai/manifests" / OLD_SESSION, 400)
        self.assert_pruned(self.prune("--root", self.root, "--days", 30), 0, 0)
        for path in loose + [manifests]:
            self.assertTrue(path.exists(), path)

    def test_a_link_inside_a_run_folder_leaves_the_folder_and_its_target(self):
        target = self.folder(Path(self._tmp.name) / "elsewhere", 400, files=("precious.txt",))
        run = self.run_dir(OLD_RUN, 40)
        os.symlink(target, run / "link")
        self.age(run, 40)
        self.assert_pruned(self.prune("--root", self.root, "--days", 30), 0, 0)
        self.assertTrue((run / "link").is_symlink())
        self.assertTrue((target / "precious.txt").exists())

    def test_a_run_folder_that_is_a_link_is_skipped(self):
        target = self.folder(Path(self._tmp.name) / "elsewhere", 400, files=("precious.txt",))
        (self.progress / "runs").mkdir(parents=True)
        link = self.progress / "runs" / OLD_RUN
        os.symlink(target, link)
        os.utime(link, (self.now - 400 * DAY,) * 2, follow_symlinks=False)
        self.assert_pruned(self.prune("--root", self.root, "--days", 30), 0, 0)
        self.assertTrue(link.is_symlink())
        self.assertTrue((target / "precious.txt").exists())

    def test_a_progress_folder_that_is_a_link_is_left_alone(self):
        target = Path(self._tmp.name) / "elsewhere"
        self.folder(target / "runs" / OLD_RUN, 400)
        (self.root / "devforgeai").mkdir()
        os.symlink(target, self.progress)
        self.assert_pruned(self.prune("--root", self.root, "--days", 30), 0, 0)
        self.assertTrue((target / "runs" / OLD_RUN / "events.jsonl").exists())

    def test_nothing_to_prune_without_a_progress_folder(self):
        self.assert_pruned(self.prune("--root", self.root, "--days", 30), 0, 0)
        self.assertEqual(list(self.root.iterdir()), [])

    def test_a_root_that_is_not_a_folder_exits_2(self):
        self.assert_refused(self.prune("--root", self.root / "missing", "--days", 30))

    def test_days_must_be_a_whole_number_of_at_least_1(self):
        run = self.run_dir(OLD_RUN, 40)
        for days in ("0", "-3", "1.5", "soon"):
            with self.subTest(days=days):
                self.assert_refused(self.prune("--root", self.root, "--days", days))
        self.assertTrue(run.exists())


class PruneRulesUnderS(PruneRules):
    INTERPRETER = (sys.executable, "-S", "-B")


def load_prune():
    """prune.py as a module, so a test can change the tree between its check and its deletion."""
    import importlib.util
    spec = importlib.util.spec_from_file_location("prune_under_test", PRUNE)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class PruneRaces(Base):
    """VER-17, after the plugin-validator's review: prune runs outside the sandbox, so a folder swapped for a link
    between its check and its deletion must not take prune outside devforgeai/progress/, and a folder that changes
    or vanishes meanwhile is skipped, never a crash."""

    def setUp(self):
        super().setUp()
        self.module = load_prune()
        self.victim = self.folder(Path(self._tmp.name) / "victim", 400, files=("precious.txt",))
        (self.victim / "deep").mkdir()
        (self.victim / "deep" / "keep.txt").write_text("x\n")
        self.age(self.victim, 400)

    def patched_newest(self, before):
        """newest() that runs `before(name)` first, as a racing writer would, then answers as prune's own does."""
        real = self.module.newest

        def newest(name, dir_fd):
            before(name)
            return real(name, dir_fd)
        self.module.newest = newest

    def assert_victim_intact(self):
        self.assertTrue((self.victim / "precious.txt").exists())
        self.assertTrue((self.victim / "deep" / "keep.txt").exists())

    def test_a_candidate_swapped_for_a_link_after_its_check_is_not_followed(self):
        run = self.run_dir(OLD_RUN, 40)
        real = self.module.newest

        def newest(name, dir_fd):
            latest = real(name, dir_fd)
            os.rename(run, run.with_name("moved"))
            os.symlink(self.victim, run)
            return latest
        self.module.newest = newest
        runs, sessions, failure = self.module.prune(str(self.root), 30, None, None, self.now)
        self.assert_victim_intact()
        # Opening the swapped name finds a link, not a folder: the candidate is skipped as changed, never entered.
        self.assertEqual((runs, failure), (0, None))
        self.assertTrue((run.with_name("moved") / "events.jsonl").exists())

    def test_a_subfolder_swapped_for_a_link_during_removal_is_not_followed(self):
        run = self.run_dir(OLD_RUN, 40)
        (run / "sub").mkdir()
        (run / "sub" / "a.txt").write_text("x\n")
        self.age(run, 40)
        real = self.module.newest

        def newest(name, dir_fd):
            latest = real(name, dir_fd)
            os.rename(run / "sub", self.root / "sub-moved")
            os.symlink(self.victim, run / "sub")
            return latest
        self.module.newest = newest
        self.module.prune(str(self.root), 30, None, None, self.now)
        self.assert_victim_intact()
        self.assertTrue(self.victim.is_dir())

    def test_a_parent_folder_swapped_for_a_link_is_not_followed(self):
        session = self.session_dir(OLD_SESSION, 40)
        outside = self.folder(Path(self._tmp.name) / "elsewhere" / OLD_SESSION, 400, files=("precious.txt",))
        sessions = session.parent

        def before(name):
            if sessions.is_symlink():
                return
            os.rename(sessions, sessions.with_name("sessions-moved"))
            os.symlink(outside.parent, sessions)
        self.patched_newest(before)
        self.module.prune(str(self.root), 30, None, None, self.now)
        self.assertTrue((outside / "precious.txt").exists())

    def test_a_folder_that_vanishes_before_its_check_is_skipped(self):
        run = self.run_dir(OLD_RUN, 40)
        other = self.run_dir("20260901T120000Z-architecture-0a1b2c3e", 40)

        def before(name):
            if name == OLD_RUN and run.exists():
                for child in run.iterdir():
                    child.unlink()
                run.rmdir()
        self.patched_newest(before)
        runs, sessions, failure = self.module.prune(str(self.root), 30, None, None, self.now)
        self.assertIsNone(failure)
        self.assertEqual(runs, 1)
        self.assertFalse(other.exists())

    def test_a_platform_without_descriptor_support_is_refused(self):
        self.module.supported = lambda: False
        self.run_dir(OLD_RUN, 40)
        with self.assertRaises(self.module.Fail):
            self.module.prune(str(self.root), 30, None, None, self.now)
        self.assertTrue((self.progress / "runs" / OLD_RUN).exists())


class PruneFailures(Base):
    """VER-17 and ERR-12: a failure gives exit 2 and one stderr line, after both passes have run; two prunes at
    once, as two sessions starting their first runs together would start, both finish cleanly."""

    def test_a_folder_that_cant_be_removed_gives_one_line_and_the_other_pass_still_runs(self):
        run = self.run_dir(OLD_RUN, 40)
        locked = run / "locked"
        locked.mkdir()
        (locked / "a.txt").write_text("x\n")
        self.age(run, 40)
        locked.chmod(0o555)
        session = self.session_dir(OLD_SESSION, 40)
        try:
            proc = self.prune("--root", self.root, "--days", 30)
        finally:
            locked.chmod(0o755)
        self.assertEqual(proc.returncode, 2)
        self.assertEqual(len(proc.stderr.splitlines()), 1, proc.stderr)
        self.assertNotIn("Traceback", proc.stderr)
        self.assertFalse(session.exists())

    def test_two_prunes_at_once_both_finish_cleanly(self):
        for i in range(300):
            self.run_dir("20260901T120000Z-brainstorm-%08x" % i, 40)
        cmd = [sys.executable, "-B", str(PRUNE), "prune", "--root", str(self.root), "--days", "30"]
        procs = [subprocess.Popen(cmd, cwd=ROOT, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                 for _ in range(2)]
        results = [proc.communicate(timeout=120) + (proc.returncode,) for proc in procs]
        for out, err, code in results:
            self.assertEqual((code, err), (0, ""))
        self.assertEqual(sum(int(out.split()[1]) for out, _, _ in results), 300)
        self.assertEqual(list((self.progress / "runs").iterdir()), [])


if __name__ == "__main__":
    unittest.main()
