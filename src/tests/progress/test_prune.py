"""Tests for SPEC-013's prune script (src/claude/DevForgeAI/progress/prune.py), VER-17.

PruneRules checks IF-04 and BEH-19's confinement: only run and session folders under devforgeai/progress/, named
by their patterns, older than --days, never followed through a symbolic link. PruneRulesUnderS runs every test with
the script under `python3 -S` (QR-04). Each spawn uses -B, so no __pycache__ lands in the plugin folder, which deploys.

Run from the repository root:
    PYTHONDONTWRITEBYTECODE=1 python3 -B -m pytest -q -p no:cacheprovider src/tests/progress
"""
import json
import os
import shutil
import subprocess
import sys
import tempfile
import time
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
PRUNE = Path(os.environ.get("PRUNE_UNDER_TEST") or ROOT / "src/claude/DevForgeAI/progress/prune.py")
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
        return self.command("prune", *args)

    def command(self, name, *args):
        return subprocess.run(list(self.INTERPRETER) + [str(PRUNE), name] + [str(a) for a in args], cwd=ROOT,
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


# ---------------------------------------------------------------------------------------------------------------
# Version 20 (SPEC-013 IF-04's age pass for work files, IF-05's remove): VER-51.

PATTERN = "devforgeai/drafts/brainstorm/*.md"
WORK = "devforgeai/drafts/brainstorm/draft.md"


class WorkBase(Base):
    """A project with a plugin manifests folder holding brainstorm.json, and helpers for work files."""

    def setUp(self):
        super().setUp()
        self.manifests = Path(self._tmp.name) / "plugin-manifests"
        self.manifests.mkdir()
        self.manifest("brainstorm.json", [PATTERN])

    def manifest(self, name, patterns, folder=None, **extra):
        data = dict(skill="x", **extra)
        if patterns is not None:
            data["workFiles"] = patterns
        (folder or self.manifests).mkdir(parents=True, exist_ok=True)
        (folder or self.manifests).joinpath(name).write_text(json.dumps(data))

    def work(self, rel=WORK, age_days=0, text="draft\n"):
        path = self.root / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text)
        self.age(path, age_days)
        return path

    def state(self, run, files, age_days=2, **kw):
        """A run folder whose state.json lists files under workFiles (SPEC-012 DM-03)."""
        folder = self.run_dir(run, age_days)
        (folder / "state.json").write_text(json.dumps({"workFiles": {"files": files, "due": True}}))
        self.age(folder, age_days)
        return folder

    def victim_file(self):
        victim = Path(self._tmp.name) / "victim"
        victim.mkdir()
        (victim / "draft.md").write_text("precious\n")
        return victim


class RemoveBase(WorkBase):
    def remove(self, *paths, root=None, manifests=None, raw=()):
        args = ["--root", root or self.root, "--manifests", manifests or self.manifests]
        args += ["--file=%s" % p for p in paths] + list(raw)
        return self.command("remove", *args)

    def assert_removed(self, proc, removed, skipped, tail=""):
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertEqual(proc.stdout, "removed %d work files, skipped %d%s\n" % (removed, skipped, tail))
        self.assertEqual(proc.stderr, "")


class RemoveRules(RemoveBase):
    """VER-51, IF-05: only a regular file of a plugin manifest's pattern, reached without a link or a dot segment."""

    def test_a_matching_regular_file_goes_and_its_folders_stay(self):
        file = self.work()
        self.assert_removed(self.remove(WORK), 1, 0)
        self.assertFalse(file.exists())
        self.assertTrue(file.parent.is_dir())

    def test_several_files_are_each_removed_once(self):
        files = [self.work("devforgeai/drafts/brainstorm/%s.md" % n) for n in "abc"]
        self.assert_removed(self.remove(*[f.relative_to(self.root) for f in files]), 3, 0)
        self.assertEqual([f.exists() for f in files], [False] * 3)

    def test_a_path_named_twice_is_removed_once_and_the_second_is_skipped(self):
        self.work()
        self.assert_removed(self.remove(WORK, WORK), 1, 1)

    def test_a_missing_file_is_skipped_and_counted(self):
        self.assert_removed(self.remove(WORK), 0, 1)

    def test_paths_outside_the_patterns_are_skipped_and_stay(self):
        paths = ["docs/specs/brainstorm/BRN-001.md", "devforgeai/drafts/.gitignore",
                 "devforgeai/drafts/other/x.md", "README.md", "devforgeai/drafts/brainstorm/x.txt"]
        files = [self.work(p) for p in paths]
        self.assert_removed(self.remove(*paths), 0, len(paths))
        self.assertTrue(all(f.exists() for f in files))

    def test_unsafe_paths_are_skipped_before_matching(self):
        outside = self.root / "README.md"
        outside.write_text("keep\n")
        real = self.work()
        absolute = str(real)
        cases = {"absolute": absolute,
                 "leading ..": "../project/" + WORK,
                 "middle ..": "devforgeai/drafts/brainstorm/../../../README.md",
                 "middle .. that stays inside": "devforgeai/drafts/brainstorm/../brainstorm/draft.md",
                 "dot segment": "devforgeai/drafts/./brainstorm/draft.md",
                 "leading dot segment": "./" + WORK,
                 "empty segment": "devforgeai/drafts//brainstorm/draft.md",
                 "trailing slash": WORK + "/",
                 "empty path": "",
                 "dot": "."}
        for label, path in cases.items():
            with self.subTest(label):
                self.assert_removed(self.remove(path), 0, 1)
                self.assertTrue(real.exists())
                self.assertTrue(outside.exists())

    def test_dash_leading_paths_are_values_and_never_options(self):
        real = self.work()
        proc = self.remove("-x", "--root", "devforgeai/drafts/brainstorm/../../../README.md", WORK)
        self.assert_removed(proc, 1, 3)
        self.assertFalse(real.exists())

    def test_a_dash_leading_file_name_that_matches_is_removed(self):
        self.manifest("brainstorm.json", ["devforgeai/drafts/*.md"])
        file = self.work("devforgeai/drafts/-x.md")
        self.assert_removed(self.remove("devforgeai/drafts/-x.md"), 1, 0)
        self.assertFalse(file.exists())

    def test_a_folder_a_link_and_a_pipe_are_skipped(self):
        folder = self.root / "devforgeai/drafts/brainstorm/dir.md"
        folder.mkdir(parents=True)
        (folder / "inner.md").write_text("x\n")
        target = self.work("devforgeai/drafts/brainstorm/target.md")
        link = self.root / "devforgeai/drafts/brainstorm/link.md"
        os.symlink(target, link)
        pipe = self.root / "devforgeai/drafts/brainstorm/pipe.md"
        os.mkfifo(pipe)
        names = ["dir.md", "link.md", "pipe.md"]
        self.assert_removed(self.remove(*["devforgeai/drafts/brainstorm/" + n for n in names]), 0, 3)
        self.assertTrue((folder / "inner.md").exists())
        self.assertTrue(link.is_symlink())
        self.assertTrue(target.exists())
        self.assertTrue(stat_is_fifo(pipe))

    def test_a_dangling_link_is_skipped_and_stays(self):
        link = self.root / WORK
        link.parent.mkdir(parents=True)
        os.symlink(self.root / "nowhere", link)
        self.assert_removed(self.remove(WORK), 0, 1)
        self.assertTrue(link.is_symlink())

    def test_a_file_whose_parent_folder_is_a_link_is_skipped(self):
        victim = self.victim_file()
        (self.root / "devforgeai/drafts").mkdir(parents=True)
        os.symlink(victim, self.root / "devforgeai/drafts/brainstorm")
        self.assert_removed(self.remove(WORK), 0, 1)
        self.assertTrue((victim / "draft.md").exists())

    def test_a_link_higher_up_in_the_path_is_skipped(self):
        victim = Path(self._tmp.name) / "elsewhere"
        self.work_in(victim)
        os.symlink(victim, self.root / "devforgeai")
        self.assert_removed(self.remove(WORK), 0, 1)
        self.assertTrue((victim / "drafts/brainstorm/draft.md").exists())

    def work_in(self, base):
        path = base / "drafts/brainstorm/draft.md"
        path.parent.mkdir(parents=True)
        path.write_text("precious\n")

    def test_a_root_without_the_folder_is_not_an_error(self):
        self.assert_removed(self.remove(WORK), 0, 1)

    def test_only_the_plugin_folders_manifests_give_patterns(self):
        project = Path(self._tmp.name) / "project-manifests"
        self.manifest("brainstorm.json", ["devforgeai/drafts/brainstorm/*", "devforgeai/drafts/extra/*"], project)
        extra = self.work("devforgeai/drafts/extra/x.md")
        self.assert_removed(self.remove("devforgeai/drafts/extra/x.md"), 0, 1)
        self.assertTrue(extra.exists())
        nested = self.manifests / "sub"
        self.manifest("extra.json", ["devforgeai/drafts/extra/*"], nested)
        self.assert_removed(self.remove("devforgeai/drafts/extra/x.md"), 0, 1)

    def test_a_manifest_that_adds_nothing_is_not_named(self):
        shutil.rmtree(self.manifests)
        self.manifests.mkdir()
        (self.manifests / "broken.json").write_text("{not json")
        (self.manifests / "list.json").write_text("[1, 2]")
        (self.manifests / "binary.json").write_bytes(b"\xff\xfe\x00")
        (self.manifests / "notes.txt").write_text(json.dumps({"workFiles": [PATTERN]}))
        self.manifest("nokey.json", None)
        file = self.work()
        self.assert_removed(self.remove(WORK), 0, 1)
        self.manifest("good.json", [PATTERN])
        self.assert_removed(self.remove(WORK), 1, 0)
        self.assertFalse(file.exists())

    def test_a_manifests_folder_that_is_not_there_adds_no_pattern(self):
        file = self.work()
        self.assert_removed(self.remove(WORK, manifests=Path(self._tmp.name) / "missing"), 0, 1)
        self.assertTrue(file.exists())

    def test_a_bad_manifest_is_ignored_alone_and_named(self):
        bad = {"outside.json": ["docs/specs/*.md"], "dotdot.json": ["devforgeai/drafts/../x"],
               "nonstring.json": [7], "mixed.json": [PATTERN, "devforgeai/drafts/ok/*", "src/*"],
               "notalist.json": PATTERN, "empty.json": []}
        for name, patterns in bad.items():
            with self.subTest(name):
                self.manifest(name, patterns)
        outside = self.work("docs/specs/a.md")
        mixed_only = self.work("devforgeai/drafts/ok/a.md")
        file = self.work()
        proc = self.remove(WORK, "docs/specs/a.md", "devforgeai/drafts/ok/a.md", "devforgeai/drafts/x")
        self.assertEqual(proc.returncode, 0, proc.stderr)
        line = proc.stdout
        self.assertTrue(line.startswith("removed 1 work files, skipped 3; ignored "), line)
        self.assertEqual(line.count("\n"), 1)
        names = [part.split(":")[0].replace("ignored ", "") for part in line.strip().split("; ")[1:]]
        self.assertEqual(names, sorted(bad))
        for part in line.strip().split("; ")[1:]:
            self.assertTrue(part.split(":", 1)[1].strip(), part)
        self.assertFalse(file.exists())
        self.assertTrue(outside.exists())
        self.assertTrue(mixed_only.exists())

    def test_a_pattern_not_beginning_devforgeai_drafts_is_a_bad_manifest(self):
        for pattern in ("devforgeai/draft/*.md", "devforgeai/drafts", "/devforgeai/drafts/*", "*", ""):
            with self.subTest(pattern):
                self.manifest("bad.json", [pattern])
                proc = self.remove(WORK)
                self.assertIn("; ignored bad.json: ", proc.stdout)

    def test_a_pattern_ending_in_a_slash_means_anything_inside(self):
        self.manifest("brainstorm.json", ["devforgeai/drafts/brainstorm/"])
        file = self.work("devforgeai/drafts/brainstorm/deep/x.txt")
        self.assert_removed(self.remove("devforgeai/drafts/brainstorm/deep/x.txt"), 1, 0)
        self.assertFalse(file.exists())

    def test_without_a_file_exit_2(self):
        self.assert_refused(self.remove())

    def test_a_root_that_is_not_a_folder_exits_2(self):
        self.assert_refused(self.remove(WORK, root=self.root / "missing"))

    def test_the_command_takes_no_manifests_folder_as_optional(self):
        proc = self.command("remove", "--root", self.root, "--file=" + WORK)
        self.assertEqual(proc.returncode, 2)
        self.assertEqual(proc.stdout, "")

    def test_a_locked_folder_exits_2_after_the_other_paths_were_tried(self):
        locked = self.work("devforgeai/drafts/brainstorm/locked/a.md")
        self.manifest("brainstorm.json", ["devforgeai/drafts/brainstorm/*"])
        other = self.work("devforgeai/drafts/brainstorm/b.md")
        locked.parent.chmod(0o555)
        try:
            proc = self.remove("devforgeai/drafts/brainstorm/locked/a.md", "devforgeai/drafts/brainstorm/b.md")
        finally:
            locked.parent.chmod(0o755)
        self.assertEqual(proc.returncode, 2)
        self.assertEqual(proc.stdout, "")
        self.assertEqual(len(proc.stderr.splitlines()), 1, proc.stderr)
        self.assertIn("locked/a.md", proc.stderr)
        self.assertNotIn("Traceback", proc.stderr)
        self.assertFalse(other.exists())
        self.assertTrue(locked.exists())


def stat_is_fifo(path):
    import stat
    return stat.S_ISFIFO(os.lstat(path).st_mode)


class RemoveRulesUnderS(RemoveRules):
    INTERPRETER = (sys.executable, "-S", "-B")


class RemoveRaces(RemoveBase):
    """VER-51, IF-05: a change between the check and the removal is skipped and counted; any other error is not."""

    def setUp(self):
        super().setUp()
        self.module = load_prune()
        self.victim = self.victim_file()

    def run_remove(self, *paths):
        return self.module.remove_work(str(self.root), str(self.manifests), list(paths))

    def hook_unlink(self, before):
        real = self.module.unlink_file

        def unlink_file(name, dir_fd):
            before(name)
            return real(name, dir_fd)
        self.module.unlink_file = unlink_file

    def test_a_file_replaced_by_a_folder_after_its_check_is_skipped(self):
        file = self.work()

        def before(name):
            file.unlink()
            file.mkdir()
            (file / "inner.md").write_text("x\n")
        self.hook_unlink(before)
        removed, skipped, ignored, failure = self.run_remove(WORK)
        self.assertEqual((removed, skipped, ignored, failure), (0, 1, [], None))
        self.assertTrue((file / "inner.md").exists())

    def test_a_file_that_vanishes_after_its_check_is_skipped(self):
        file = self.work()
        self.hook_unlink(lambda name: file.unlink())
        self.assertEqual(self.run_remove(WORK), (0, 1, [], None))

    def test_a_file_swapped_for_a_link_after_its_check_leaves_the_target(self):
        file = self.work()

        def before(name):
            file.unlink()
            os.symlink(self.victim / "draft.md", file)
        self.hook_unlink(before)
        removed, skipped, ignored, failure = self.run_remove(WORK)
        self.assertIsNone(failure)
        self.assertTrue((self.victim / "draft.md").exists())

    def test_a_folder_swapped_for_a_link_before_it_is_opened_is_not_followed(self):
        self.work()
        drafts = self.root / "devforgeai/drafts"
        real = self.module.open_folder

        def open_folder(name, dir_fd):
            if name == "brainstorm" and not (drafts / "brainstorm").is_symlink():
                os.rename(drafts / "brainstorm", drafts / "moved")
                os.symlink(self.victim, drafts / "brainstorm")
            return real(name, dir_fd)
        self.module.open_folder = open_folder
        self.assertEqual(self.run_remove(WORK), (0, 1, [], None))
        self.assertTrue((self.victim / "draft.md").exists())
        self.assertTrue((drafts / "moved/draft.md").exists())

    def test_a_folder_swapped_for_a_link_after_it_was_opened_is_not_followed(self):
        file = self.work()
        drafts = self.root / "devforgeai/drafts"

        def before(name):
            os.rename(drafts / "brainstorm", drafts / "moved")
            os.symlink(self.victim, drafts / "brainstorm")
        self.hook_unlink(before)
        self.run_remove(WORK)
        self.assertTrue((self.victim / "draft.md").exists())

    def test_any_other_error_on_the_unlink_is_a_failure_naming_the_first_after_the_rest(self):
        a, b, c = [self.work("devforgeai/drafts/brainstorm/%s.md" % n) for n in "abc"]
        real = self.module.unlink_file

        def unlink_file(name, dir_fd):
            if name == "a.md":
                raise PermissionError(13, "Permission denied")
            return real(name, dir_fd)
        self.module.unlink_file = unlink_file
        removed, skipped, ignored, failure = self.run_remove(
            "devforgeai/drafts/brainstorm/a.md", "devforgeai/drafts/brainstorm/b.md",
            "devforgeai/drafts/brainstorm/c.md")
        self.assertEqual((removed, skipped), (2, 0))
        self.assertIn("devforgeai/drafts/brainstorm/a.md", failure)
        self.assertTrue(a.exists())
        self.assertFalse(b.exists() or c.exists())

    def test_a_platform_without_descriptor_support_is_refused(self):
        file = self.work()
        self.module.supported = lambda: False
        with self.assertRaises(self.module.Fail):
            self.run_remove(WORK)
        self.assertTrue(file.exists())


class AgeBase(WorkBase):
    def age_pass(self, *args, days=30):
        return self.prune("--root", self.root, "--days", days, "--manifests", self.manifests, *args)

    def assert_aged(self, proc, runs, sessions, work, tail=""):
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertEqual(proc.stdout, "pruned %d runs, %d sessions, %d work files%s\n" % (runs, sessions, work, tail))
        self.assertEqual(proc.stderr, "")


class AgePass(AgeBase):
    """VER-51, IF-04 with --manifests: an old work file goes unless a run that survives the pass lists it."""

    def test_an_old_matching_file_goes_and_a_newer_one_stays(self):
        old = self.work("devforgeai/drafts/brainstorm/old.md", 40)
        new = self.work("devforgeai/drafts/brainstorm/new.md", 2)
        self.assert_aged(self.age_pass(), 0, 0, 1)
        self.assertFalse(old.exists())
        self.assertTrue(new.exists())

    def test_old_files_that_match_no_pattern_stay(self):
        keep = [self.work(p, 400) for p in ("devforgeai/drafts/.gitignore", "devforgeai/drafts/brainstorm/n.txt",
                                            "devforgeai/drafts/other/x.md", "docs/specs/brainstorm/BRN-001.md")]
        self.assert_aged(self.age_pass(), 0, 0, 0)
        self.assertTrue(all(p.exists() for p in keep))

    def test_no_folder_is_removed_and_none_is_descended_through_a_link(self):
        old = self.work("devforgeai/drafts/brainstorm/sub/old.md", 40)
        empty = self.root / "devforgeai/drafts/brainstorm/empty"
        empty.mkdir()
        victim = self.victim_file()
        self.age(victim / "draft.md", 400)
        os.symlink(victim, self.root / "devforgeai/drafts/brainstorm/linked")
        self.assert_aged(self.age_pass(), 0, 0, 1)
        self.assertFalse(old.exists())
        self.assertTrue(old.parent.is_dir() and empty.is_dir())
        self.assertTrue((victim / "draft.md").exists())

    def test_a_link_is_left_with_its_target_and_a_pipe_stays(self):
        target = self.work("devforgeai/drafts/brainstorm/target.md", 400)
        outside = Path(self._tmp.name) / "outside.md"
        outside.write_text("x\n")
        self.age(outside, 400)
        link = self.root / "devforgeai/drafts/brainstorm/link.md"
        os.symlink(outside, link)
        os.utime(link, (self.now - 400 * DAY,) * 2, follow_symlinks=False)
        pipe = self.root / "devforgeai/drafts/brainstorm/pipe.md"
        os.mkfifo(pipe)
        os.utime(pipe, (self.now - 400 * DAY,) * 2)
        self.assert_aged(self.age_pass(), 0, 0, 1)
        self.assertFalse(target.exists())
        self.assertTrue(link.is_symlink())
        self.assertTrue(outside.exists())
        self.assertTrue(stat_is_fifo(pipe))

    def test_a_drafts_folder_that_is_a_link_is_not_entered(self):
        victim = Path(self._tmp.name) / "elsewhere"
        self.work_in(victim)
        self.age(victim / "drafts/brainstorm/draft.md", 400)
        os.symlink(victim / "drafts", self.root / "devforgeai-drafts")
        (self.root / "devforgeai").mkdir()
        os.symlink(victim / "drafts", self.root / "devforgeai/drafts")
        self.assert_aged(self.age_pass(), 0, 0, 0)
        self.assertTrue((victim / "drafts/brainstorm/draft.md").exists())

    def work_in(self, base):
        path = base / "drafts/brainstorm/draft.md"
        path.parent.mkdir(parents=True)
        path.write_text("precious\n")

    def test_the_pass_runs_with_no_progress_folder_and_with_no_drafts_folder(self):
        old = self.work(age_days=40)
        self.assertFalse(self.progress.exists())
        self.assert_aged(self.age_pass(), 0, 0, 1)
        self.assertFalse(old.exists())
        self.assert_aged(self.age_pass(), 0, 0, 0)
        shutil.rmtree(self.root / "devforgeai")
        self.assert_aged(self.age_pass(), 0, 0, 0)

    def test_a_file_that_a_surviving_run_lists_stays_however_old(self):
        old = self.work(age_days=40)
        run = self.state(NEW_RUN, [WORK], age_days=2)
        self.assert_aged(self.age_pass(), 0, 0, 0)
        self.assertTrue(old.exists())
        self.assertTrue(run.exists())

    def test_a_file_only_a_pruned_run_lists_goes_in_the_same_pass_as_its_run(self):
        old = self.work(age_days=40)
        run = self.state(OLD_RUN, [WORK], age_days=40)
        self.assert_aged(self.age_pass(), 1, 0, 1)
        self.assertFalse(old.exists() or run.exists())

    def test_a_run_continued_and_passed_as_a_second_keep_run_keeps_its_files(self):
        old = self.work(age_days=40)
        earlier = self.state(OLD_RUN, [WORK], age_days=40)
        new = self.state(NEW_RUN, [], age_days=0)
        self.assert_aged(self.age_pass("--keep-run", NEW_RUN, "--keep-run", OLD_RUN), 0, 0, 0)
        self.assertTrue(old.exists() and earlier.exists() and new.exists())

    def test_the_file_goes_once_the_continued_run_is_no_longer_kept(self):
        old = self.work(age_days=40)
        earlier = self.state(OLD_RUN, [WORK], age_days=40)
        self.assert_aged(self.age_pass("--keep-run", NEW_RUN), 1, 0, 1)
        self.assertFalse(old.exists() or earlier.exists())

    def test_a_state_that_names_other_paths_widens_nothing(self):
        gone = self.work(age_days=40)
        other = self.work("devforgeai/drafts/other/x.md", 40)
        readme = self.root / "README.md"
        readme.write_text("x\n")
        self.age(readme, 40)
        self.state(NEW_RUN, ["README.md", "../x", "devforgeai/drafts/other/x.md", 7, None, {"a": 1}], age_days=2)
        self.assert_aged(self.age_pass(), 0, 0, 1)
        self.assertFalse(gone.exists())
        self.assertTrue(other.exists() and readme.exists())

    def test_a_state_that_isnt_json_or_has_the_wrong_shape_keeps_nothing(self):
        bodies = ["{not json", "[]", "null", '{"workFiles": 3}', '{"workFiles": {"files": "%s"}}' % WORK,
                  '{"workFiles": {"files": {"%s": 1}}}' % WORK, "\xff"]
        for body in bodies:
            with self.subTest(body):
                old = self.work(age_days=40)
                run = self.run_dir(NEW_RUN, 2)
                (run / "state.json").write_bytes(body.encode("latin-1"))
                self.assert_aged(self.age_pass(), 0, 0, 1)
                self.assertFalse(old.exists())
                shutil.rmtree(run)

    def test_a_state_that_is_a_link_or_missing_or_a_run_folder_that_is_a_link_keeps_nothing(self):
        listing = Path(self._tmp.name) / "listing.json"
        listing.write_text(json.dumps({"workFiles": {"files": [WORK]}}))
        run = self.run_dir(NEW_RUN, 2)
        (run / "state.json").unlink()
        os.symlink(listing, run / "state.json")
        other = self.progress / "runs" / "20261001T000000Z-prd-0a0a0a0a"
        os.symlink(run, other)
        old = self.work(age_days=40)
        self.assert_aged(self.age_pass(), 0, 0, 1)
        self.assertFalse(old.exists())

    def test_a_state_that_is_a_pipe_does_not_hang_the_pass(self):
        run = self.run_dir(NEW_RUN, 2)
        (run / "state.json").unlink()
        os.mkfifo(run / "state.json")
        old = self.work(age_days=40)
        self.assert_aged(self.age_pass(), 0, 0, 1)
        self.assertFalse(old.exists())

    def test_a_state_in_a_folder_of_any_name_still_keeps(self):
        old = self.work(age_days=40)
        run = self.progress / "runs" / "odd-name"
        run.mkdir(parents=True)
        (run / "state.json").write_text(json.dumps({"workFiles": {"files": [WORK]}}))
        self.assert_aged(self.age_pass(), 0, 0, 0)
        self.assertTrue(old.exists())

    def test_without_manifests_the_line_and_the_files_are_as_before(self):
        old = self.work(age_days=400)
        self.assert_pruned(self.prune("--root", self.root, "--days", 30), 0, 0)
        self.assertTrue(old.exists())

    def test_the_folder_pass_is_as_before_with_manifests(self):
        old_run, new_run = self.run_dir(OLD_RUN, 40), self.run_dir(NEW_RUN, 2)
        old_session, new_session = self.session_dir(OLD_SESSION, 40), self.session_dir(NEW_SESSION, 2)
        self.assert_aged(self.age_pass("--keep-session", NEW_SESSION), 1, 1, 0)
        self.assertFalse(old_run.exists() or old_session.exists())
        self.assertTrue(new_run.exists() and new_session.exists())

    def test_a_bad_manifest_adds_no_pattern_and_is_named_on_the_line(self):
        self.manifest("bad.json", ["devforgeai/drafts/other/*", "docs/*"])
        other = self.work("devforgeai/drafts/other/x.md", 40)
        old = self.work(age_days=40)
        proc = self.age_pass()
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertTrue(proc.stdout.startswith("pruned 0 runs, 0 sessions, 1 work files; ignored bad.json: "),
                        proc.stdout)
        self.assertEqual(proc.stdout.count("\n"), 1)
        self.assertFalse(old.exists())
        self.assertTrue(other.exists())

    def test_a_locked_folder_exits_2_naming_the_first_after_both_passes(self):
        locked = self.work("devforgeai/drafts/brainstorm/locked/a.md", 40)
        self.manifest("brainstorm.json", ["devforgeai/drafts/brainstorm/*"])
        other = self.work("devforgeai/drafts/brainstorm/b.md", 40)
        session = self.session_dir(OLD_SESSION, 40)
        locked.parent.chmod(0o555)
        try:
            proc = self.age_pass()
        finally:
            locked.parent.chmod(0o755)
        self.assertEqual(proc.returncode, 2)
        self.assertEqual(proc.stdout, "")
        self.assertEqual(len(proc.stderr.splitlines()), 1, proc.stderr)
        self.assertNotIn("Traceback", proc.stderr)
        self.assertFalse(other.exists() or session.exists())

    def test_a_missing_manifests_folder_prunes_folders_and_no_files(self):
        old = self.work(age_days=400)
        proc = self.prune("--root", self.root, "--days", 30, "--manifests", Path(self._tmp.name) / "missing")
        self.assertEqual((proc.returncode, proc.stdout), (0, "pruned 0 runs, 0 sessions, 0 work files\n"))
        self.assertTrue(old.exists())


class AgePassUnderS(AgePass):
    INTERPRETER = (sys.executable, "-S", "-B")


class AgePassRaces(AgeBase):
    def setUp(self):
        super().setUp()
        self.module = load_prune()

    def call(self, *keep_runs):
        return self.module.prune_all(str(self.root), 30, None, list(keep_runs), self.now, str(self.manifests))

    def test_a_file_replaced_by_a_folder_after_its_check_is_skipped(self):
        file = self.work(age_days=40)

        def before(name):
            file.unlink()
            file.mkdir()
        real = self.module.unlink_file
        self.module.unlink_file = lambda name, fd: (before(name), real(name, fd))[1]
        result = self.call()
        self.assertEqual((result.work, result.failure), (0, None))
        self.assertTrue(file.is_dir())

    def test_a_file_that_vanishes_after_its_check_is_skipped(self):
        file = self.work(age_days=40)
        real = self.module.unlink_file
        self.module.unlink_file = lambda name, fd: (file.unlink(), real(name, fd))[1]
        result = self.call()
        self.assertEqual((result.work, result.failure), (0, None))

    def test_a_platform_without_descriptor_support_is_refused(self):
        file = self.work(age_days=40)
        self.module.supported = lambda: False
        with self.assertRaises(self.module.Fail):
            self.call()
        self.assertTrue(file.exists())

    def test_a_run_and_a_file_it_lists_are_removed_together_never_the_file_alone(self):
        file = self.work(age_days=40)
        run = self.state(OLD_RUN, [WORK], age_days=40)
        result = self.call()
        self.assertEqual((result.runs, result.work, result.failure), (1, 1, None))
        self.assertFalse(file.exists() or run.exists())


LEDGER_LINE = ('{"session": "%s", "turn": "t1", "source": "main", "input": 1, "output": 2, "cacheRead": 3, '
               '"cacheWrite": 4, "time": "2026-01-01T00:00:00Z"}\n')


class OdometerKept(AgeBase):
    """SPEC-013 VER-65 (version 24), SPEC-012 BEH-28: prune.py never removes, truncates or rewrites the odometer folder or
    a file in it, whatever its age, by either command, and never follows a link to or from it. The pass only ever
    enters runs/, sessions/ and drafts/, so these tests could not fail first; they pin the promise against a later
    change (SPEC-012 section 9 records the same of version 13's)."""

    def ledger(self, name=NEW_SESSION + ".jsonl", age_days=400):
        folder = self.progress / "odometer"
        folder.mkdir(parents=True, exist_ok=True)
        path = folder / name
        path.write_text(LEDGER_LINE % name)
        self.age(path, age_days)
        self.age(folder, age_days)
        return folder

    @staticmethod
    def snapshot(folder):
        """Every entry under a folder, the folder included: its bytes, size and modification time."""
        seen = {}
        for dirpath, dirnames, filenames in os.walk(folder, followlinks=False):
            for name in dirnames + filenames:
                path = Path(dirpath) / name
                info = path.lstat()
                seen[str(path.relative_to(folder))] = (path.read_bytes() if path.is_file() and not path.is_symlink()
                                                       else os.readlink(path) if path.is_symlink() else None,
                                                       info.st_size, info.st_mtime_ns)
        info = Path(folder).lstat()
        seen["."] = (None, 0, info.st_mtime_ns)
        return seen

    def old_things(self):
        """An old run, an old session and an old work file: everything prune is for."""
        return [self.run_dir(OLD_RUN, 40), self.session_dir(OLD_SESSION, 40), self.work(age_days=40)]

    def test_prune_removes_the_old_things_and_leaves_the_ledger_with_its_bytes_sizes_and_times(self):
        for manifests in (False, True):
            with self.subTest(manifests=manifests):
                folder = self.ledger()
                self.ledger("S-old.jsonl", age_days=2)
                self.age(folder, 400)
                things = self.old_things()
                before = self.snapshot(folder)
                proc = self.age_pass(days=1) if manifests else self.prune("--root", self.root, "--days", 1)
                self.assertEqual(proc.returncode, 0, proc.stderr)
                self.assertEqual(proc.stdout, "pruned 1 runs, 1 sessions%s\n" % (", 1 work files" if manifests else ""))
                self.assertFalse(things[0].exists() or things[1].exists())
                self.assertEqual(things[2].exists(), not manifests)
                self.assertEqual(self.snapshot(folder), before)

    def test_a_ledger_of_any_age_is_in_no_count(self):
        folder = self.ledger(age_days=4000)
        self.assertEqual(self.prune("--root", self.root, "--days", 1).stdout, "pruned 0 runs, 0 sessions\n")
        self.assertEqual(self.age_pass(days=1).stdout, "pruned 0 runs, 0 sessions, 0 work files\n")
        self.assertEqual(self.prune("--root", self.root, "--days", 1, "--keep-session", NEW_SESSION).stdout,
                         "pruned 0 runs, 0 sessions\n")
        self.assertTrue((folder / (NEW_SESSION + ".jsonl")).exists())

    def test_a_folder_in_the_ledger_folder_named_like_a_run_or_a_session_stays(self):
        folder = self.ledger()
        for name in (OLD_RUN, OLD_SESSION):
            self.folder(folder / name, 400, files=("S.jsonl",))
        self.age(folder, 400)
        before = self.snapshot(folder)
        self.assertEqual(self.age_pass(days=1).stdout, "pruned 0 runs, 0 sessions, 0 work files\n")
        self.assertEqual(self.snapshot(folder), before)

    def test_remove_leaves_the_ledger_alone_and_skips_a_path_into_it(self):
        folder = self.ledger()
        file = self.work()
        before = self.snapshot(folder)
        ledger_path = "devforgeai/progress/odometer/%s.jsonl" % NEW_SESSION
        proc = self.command("remove", "--root", self.root, "--manifests", self.manifests, "--file=%s" % WORK,
                            "--file=%s" % ledger_path, "--file=devforgeai/progress/odometer")
        self.assertEqual((proc.returncode, proc.stdout), (0, "removed 1 work files, skipped 2\n"))
        self.assertFalse(file.exists())
        self.assertEqual(self.snapshot(folder), before)

    def test_a_ledger_file_that_is_a_link_is_untouched_with_its_target(self):
        folder = self.ledger(age_days=2)
        outside = Path(self._tmp.name) / "outside.jsonl"
        outside.write_text(LEDGER_LINE % "outside")
        self.age(outside, 400)
        link = folder / "linked.jsonl"
        os.symlink(outside, link)
        os.utime(link, (self.now - 400 * DAY,) * 2, follow_symlinks=False)
        self.old_things()
        before, target = self.snapshot(folder), (outside.read_bytes(), outside.stat().st_mtime_ns)
        for proc in (self.prune("--root", self.root, "--days", 1), self.age_pass(days=1)):
            self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertEqual(self.snapshot(folder), before)
        self.assertTrue(link.is_symlink())
        self.assertEqual((outside.read_bytes(), outside.stat().st_mtime_ns), target)

    def test_a_ledger_folder_that_is_a_link_is_untouched_with_its_target(self):
        victim = self.ledger_in(Path(self._tmp.name) / "elsewhere")
        link = self.progress / "odometer"
        self.progress.mkdir(parents=True, exist_ok=True)
        os.symlink(victim, link)
        self.old_things()
        before = self.snapshot(victim)
        for proc in (self.prune("--root", self.root, "--days", 1), self.age_pass(days=1)):
            self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertTrue(link.is_symlink())
        self.assertEqual(self.snapshot(victim), before)

    def ledger_in(self, folder):
        folder.mkdir(parents=True)
        (folder / "S.jsonl").write_text(LEDGER_LINE % "S")
        self.age(folder / "S.jsonl", 400)
        self.age(folder, 400)
        return folder


class OdometerKeptUnderS(OdometerKept):
    INTERPRETER = (sys.executable, "-S", "-B")


if __name__ == "__main__":
    unittest.main()
