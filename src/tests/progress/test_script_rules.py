"""Tests for the rules that bind chain_state.py and history.py both (SPEC-012 version 17): VER-53 (QR-05, QR-06) and
VER-54 (QR-07).

ScriptRules runs over a fixture project that holds every shape VER-50 to VER-52 name: documents (one a link), run
states (one bad), and a ledger (one line malformed). ScriptRulesUnderS runs each test with the scripts under
`python3 -S`. Performance builds a project of 500 documents, 500 run folders and a ledger of 20 files and 20,000 lines,
and times each script. Each spawn uses -B, so no __pycache__ lands in the plugin folder, which deploys.

Run from the repository root:
    PYTHONDONTWRITEBYTECODE=1 python3 -B -m pytest -q -p no:cacheprovider src/tests/progress
"""
import ast
import json
import os
import stat
import sys
import tempfile
import time
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import script_fixtures as fx  # noqa: E402

mc = fx.mc
SCRIPTS = {"chain_state": fx.CHAIN_STATE, "history": fx.HISTORY}
BANNED = {"socket", "subprocess", "urllib", "http", "ctypes"}


def strings(value):
    """Every string in a JSON value, keys included."""
    if isinstance(value, str):
        yield value
    elif isinstance(value, dict):
        for k, v in value.items():
            yield k
            yield from strings(v)
    elif isinstance(value, list):
        for v in value:
            yield from strings(v)


class Base(unittest.TestCase):
    INTERPRETER = (sys.executable, "-B")

    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.base = Path(self._tmp.name)
        self.root = self.base / "project"
        self.cwd = self.base / "cwd"
        self.root.mkdir()
        self.cwd.mkdir()

    def tearDown(self):
        make_writable(self.base)
        self._tmp.cleanup()

    def build(self):
        """The fixture project: three documents and a link, three run states and a bad one, a two-file ledger."""
        for rel, text in (("brainstorm/BRN-001.md", "---\nid: BRN-001\ntype: brainstorm\nstatus: converged\nversion: 2\n---\n"),
                          ("spec/SPEC-001.md", "---\nid: SPEC-001\ntype: spec\nstatus: approved\nversion: 17\n"
                                               "upstream:\n  - {id: BRN-001, relation: informed_by}\n---\n"),
                          ("no-id.md", "---\ntype: spec\n---\n"), ("proposal.md", "# no frontmatter\n")):
            fx.write(self.root, "docs/specs/" + rel, text)
        os.symlink(self.base / "cwd", self.root / "docs/specs/linked")
        for i, active in enumerate((600, 1200, 900)):
            fx.put_run(self.root, fx.run_name("brainstorm", i), fx.evaluate_log(fx.brainstorm_run(active)))
        fx.put_run(self.root, "bad", "not json")
        fx.ledger(self.root, "S1.jsonl", [fx.line("S1", "t1", "main", 4, 3, 2, 1), fx.line("S1", "t1", "agent", 1, 1, 1, 1),
                                          "not json"])
        fx.ledger(self.root, "S2.jsonl", [fx.line("S2", "t1", "main", 9, 9, 9, 9), fx.line("S1", "t1", "main", 5, 5, 5, 5)])

    def script(self, name, interpreter=None, env=None, root=None):
        return fx.run_script_bytes(SCRIPTS[name], ["--root", root or self.root], interpreter or self.INTERPRETER,
                                   cwd=self.cwd, env=env)


def make_writable(base):
    for dirpath, dirnames, filenames in os.walk(base, followlinks=False):
        os.chmod(dirpath, 0o755)
        for name in filenames:
            path = Path(dirpath) / name
            if not path.is_symlink():
                os.chmod(path, 0o644)


def make_read_only(base):
    for dirpath, dirnames, filenames in os.walk(base, topdown=False, followlinks=False):
        for name in filenames:
            path = Path(dirpath) / name
            if not path.is_symlink():
                os.chmod(path, 0o444)
        os.chmod(dirpath, 0o555)


class ScriptRules(Base):
    """VER-53: the scripts' rules, over every shape of fixture."""

    def test_ver53_the_output_is_the_same_with_and_without_dash_S(self):
        self.build()
        for name in SCRIPTS:
            with self.subTest(name):
                plain = self.script(name, (sys.executable, "-B"))
                bare = self.script(name, (sys.executable, "-S", "-B"))
                self.assertEqual((plain.returncode, bare.returncode), (0, 0), (plain.stderr, bare.stderr))
                self.assertEqual(plain.stdout, bare.stdout)
                self.assertTrue(plain.stdout.endswith(b"\n"))

    def test_ver53_they_import_only_the_standard_library(self):
        for name, path in SCRIPTS.items():
            with self.subTest(name):
                tree = ast.parse(path.read_text(encoding="utf-8"))
                modules = set()
                for node in ast.walk(tree):
                    if isinstance(node, ast.Import):
                        modules.update(alias.name.split(".")[0] for alias in node.names)
                    elif isinstance(node, ast.ImportFrom):
                        self.assertEqual(node.level, 0, "a relative import")
                        modules.add((node.module or "").split(".")[0])
                self.assertTrue(modules, "the script imports nothing at all?")
                self.assertEqual(modules - set(sys.stdlib_module_names), set())
                self.assertEqual(modules & BANNED, set())

    def test_ver53_different_hash_seeds_give_identical_bytes_and_no_absolute_path(self):
        self.build()
        for name in SCRIPTS:
            with self.subTest(name):
                outputs = []
                for seed in ("0", "1", "4242", "random"):
                    env = dict(os.environ, PYTHONHASHSEED=seed)
                    proc = self.script(name, env=env)
                    self.assertEqual(proc.returncode, 0, proc.stderr)
                    outputs.append(proc.stdout)
                self.assertEqual(len(set(outputs)), 1)
                out = json.loads(outputs[0])
                for text in strings(out):
                    self.assertFalse(text.startswith("/"), text)
                    self.assertNotIn(str(self.base), text)
                self.assertNotIn(str(self.root).encode(), outputs[0])
                self.assertNotIn(tempfile.gettempdir().encode(), outputs[0])

    def test_ver53_a_read_only_tree_is_left_unchanged_and_nothing_is_created(self):
        self.build()
        make_read_only(self.base)
        before = fx.snapshot(self.base)
        for name in SCRIPTS:
            with self.subTest(name):
                proc = self.script(name)
                self.assertEqual(proc.returncode, 0, proc.stderr)
                self.assertEqual(proc.stderr, b"")
                self.assertEqual(fx.snapshot(self.base), before)
        self.assertEqual(sorted(os.listdir(self.cwd)), [])  # the working directory gained no file
        self.assertEqual(stat.S_IMODE(os.stat(self.root).st_mode), 0o555)

    def test_ver53_a_missing_root_creates_nothing_either(self):
        before = fx.snapshot(self.base)
        for name in SCRIPTS:
            with self.subTest(name):
                proc = fx.run_script_bytes(SCRIPTS[name], ["--root", self.base / "missing"], self.INTERPRETER, cwd=self.cwd)
                self.assertEqual((proc.returncode, proc.stdout), (2, b""))
                self.assertEqual(fx.snapshot(self.base), before)


class ScriptRulesUnderS(ScriptRules):
    INTERPRETER = (sys.executable, "-S", "-B")


class Performance(unittest.TestCase):
    """VER-54, QR-07: 500 documents, 500 run folders and a ledger of 20 files and 20,000 lines, each script under 1 s."""

    def test_ver54_each_script_runs_in_under_a_second_on_a_large_project(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "project"
            types = ("spec", "adr", "prd", "arch", "epic", "brainstorm", "story", "policy", "context", "report")
            upstream = "".join("  - {id: %s-%03d, relation: informed_by, version: 3, hash: null, note: \"a note\"}\n" % (t.upper(), i)
                               for i, t in enumerate(types[:5]))
            body = "# Title\n\n" + "A line of body text that is never read.\n" * 12
            for i in range(500):
                kind = types[i % len(types)]
                fx.write(root, "docs/specs/%s/%s-%03d.md" % (kind, kind.upper(), i),
                         "---\nid: %s-%03d\ntype: %s\nstatus: approved\nversion: %d\nupdated: 2026-10-08\nupstream:\n%s---\n%s"
                         % (kind.upper(), i, kind, i % 20 + 1, upstream, body))
            state = json.loads(fx.evaluate_log(fx.brainstorm_run(600)))
            for i in range(500):
                state["timing"]["activeSeconds"] = 300 + i
                fx.put_run(root, "20261002T120000Z-brainstorm-%08x" % i, json.dumps(state, sort_keys=True, indent=2) + "\n")
            for f in range(20):
                fx.ledger(root, "session-%02d.jsonl" % f,
                          [fx.line("session-%02d" % f, "turn-%04d" % t, "main" if t % 3 else "agent-%d" % (t % 7),
                                   100 + t, 50 + t, 1000 + t, 300 + t, "2026-10-06T12:%02d:%02dZ" % (t // 60 % 60, t % 60))
                           for t in range(1000)])
            for name, script in SCRIPTS.items():
                with self.subTest(name):
                    started = time.perf_counter()
                    proc = fx.run_script_bytes(script, ["--root", root], (sys.executable, "-B"), cwd=tmp)
                    elapsed = time.perf_counter() - started
                    self.assertEqual(proc.returncode, 0, proc.stderr)
                    out = json.loads(proc.stdout)
                    print("\nVER-54: %s on 500 documents, 500 run folders and 20,000 ledger lines: %.0f ms"
                          % (name, elapsed * 1000))
                    self.assertLess(elapsed, 1.0)
                    if name == "chain_state":
                        self.assertEqual(len(out["documents"]), 500)
                    else:
                        self.assertEqual((out["runs"]["read"], out["odometer"]["turns"]), (500, 20000))


if __name__ == "__main__":
    unittest.main()
