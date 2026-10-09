"""Tests for SPEC-012 version 17's cross-run figures (src/claude/DevForgeAI/progress/history.py), VER-51 and VER-52.

RunRules checks IF-04's run figures (BEH-27, ERR-15) on run folders built from states the evaluator wrote; OdometerRules
checks the ledger (DM-04, BEH-28, ERR-16). The output is validated against DM-06 throughout. The Under-S classes run
every test with the script under `python3 -S` (QR-05). Each spawn uses -B, so no __pycache__ lands in the plugin
folder, which deploys.

Run from the repository root:
    PYTHONDONTWRITEBYTECODE=1 python3 -B -m pytest -q -p no:cacheprovider src/tests/progress
"""
import json
import os
import sys
import tempfile
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import script_fixtures as fx  # noqa: E402

mc = fx.mc
ZERO = {"input": 0, "output": 0, "cacheRead": 0, "cacheWrite": 0, "tokens": 0, "turns": 0, "duplicates": 0,
        "malformed": 0}


def validator(name):
    return Draft202012Validator(json.loads((fx.SCHEMAS / (name + ".schema.json")).read_text(encoding="utf-8")))


class Base(unittest.TestCase):
    INTERPRETER = (sys.executable, "-B")

    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name) / "project"
        self.root.mkdir()

    def tearDown(self):
        self._tmp.cleanup()

    def history(self, root=None, *extra):
        return fx.run_script(fx.HISTORY, ["--root", root or self.root] + list(extra), self.INTERPRETER)

    def figures(self, root=None):
        """The printed figures; the run must exit 0 with nothing on stderr, and validate against DM-06."""
        proc = self.history(root)
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertEqual(proc.stderr, "")
        out = json.loads(proc.stdout)
        self.assertEqual([e.message for e in validator("history").iter_errors(out)], [])
        self.assertEqual(proc.stdout, json.dumps(out, sort_keys=True, indent=2, ensure_ascii=False) + "\n")
        return out

    def assert_refused(self, proc, word):
        self.assertEqual(proc.returncode, 2, proc.stderr)
        self.assertEqual(proc.stdout, "")
        self.assertEqual(len(proc.stderr.splitlines()), 1, proc.stderr)
        self.assertTrue(proc.stderr.startswith("history: "), proc.stderr)
        self.assertIn(word, proc.stderr)

    def state(self, log):
        return fx.evaluate_log(log, self.INTERPRETER)

    def add(self, name, log_or_text):
        text = log_or_text if isinstance(log_or_text, str) else self.state(log_or_text)
        return fx.put_run(self.root, name, text)

    def run_names(self, skill, count, start=0):
        return [fx.run_name(skill, start + i) for i in range(count)]


class RunRules(Base):
    """VER-51: the runs' figures and the median of the complete ones."""

    def test_ver51_the_states_the_fixture_uses_are_what_the_tests_say_they_are(self):
        done = json.loads(self.state(fx.brainstorm_run(600)))
        self.assertEqual((done["timing"]["activeSeconds"], done["ended"], done["timing"]["stepsCarried"]), (600, "session-end", 0))
        self.assertEqual(sorted({s["state"] for s in done["steps"]}), ["done", "not-applicable"])
        idle = json.loads(self.state(fx.architecture_run_ending_idle()))
        self.assertEqual(idle["ended"], "idle")
        self.assertEqual([s["state"] for s in idle["steps"] if s["n"] in (5, 7)], ["not-applicable"] * 2)
        self.assertEqual(sorted({s["state"] for s in idle["steps"]}), ["done", "not-applicable"])
        stopped = json.loads(self.state(mc.CASE_BUILDERS["arch-stopped"]()[0]))
        self.assertEqual((stopped["ended"], [s["state"] for s in stopped["steps"] if s["n"] >= 9]), ("stopped", ["pending"] * 3))

    def test_ver51_the_median_of_three_complete_runs(self):
        for name, active in zip(self.run_names("brainstorm", 3), (600, 1200, 900)):
            self.add(name, fx.brainstorm_run(active))
        out = self.figures()
        self.assertEqual(out["skills"], {"brainstorm": {"runs": 3, "complete": 3, "medianActiveSeconds": 900}})
        self.assertEqual(out["runs"], {"read": 3, "skipped": 0})
        self.assertEqual(out["odometer"], ZERO)

    def test_ver51_the_median_of_two_is_the_mean_rounded_down(self):
        for name, active in zip(self.run_names("brainstorm", 2), (100, 201)):
            self.add(name, fx.brainstorm_run(active))
        self.assertEqual(self.figures()["skills"]["brainstorm"], {"runs": 2, "complete": 2, "medianActiveSeconds": 150})

    def test_ver51_one_complete_run_has_no_median(self):
        self.add(self.run_names("brainstorm", 1)[0], fx.brainstorm_run(600))
        self.assertEqual(self.figures()["skills"]["brainstorm"], {"runs": 1, "complete": 1, "medianActiveSeconds": None})

    def test_ver51_an_open_stopped_carried_or_early_run_is_read_and_never_complete(self):
        names = self.run_names("brainstorm", 4)
        # A run that continued another, whose carried step then got evidence of its own: no step is in the carried
        # state, yet the run carried a step and so doesn't count (BEH-27).
        redone = mc.brn_start(mc.carrying("brainstorm", [1], follow=False)).write(mc.BRN_PATH, mc.brn(["open"] * 15))
        redone.bash(mc.VALIDATE).tick(6, 7).tick(8).end("session-end")
        state = json.loads(self.state(redone))
        self.assertEqual((state["timing"]["stepsCarried"], state["ended"]), (1, "session-end"))
        self.assertEqual({s["state"] for s in state["steps"]} & {"pending", "current", "your-turn", "carried"}, set())
        self.add(fx.run_name("brainstorm", 8), redone)
        self.add(names[0], fx.brainstorm_run(600, end=None))  # open
        self.add(names[1], mc.carrying("brainstorm", [1, 2, 3, 4, 5]).started(6).end("session-end"))  # carried steps
        log = mc.brn_start(mc.Log("brainstorm")).write(mc.BRN_PATH, mc.brn(["open"] * 15)).end("another-skill")
        self.add(names[2], log)  # ended by another skill with step 7 still to come
        self.add(fx.run_name("architecture", 9), mc.CASE_BUILDERS["arch-stopped"]()[0])  # the user stopped it
        out = self.figures()
        self.assertEqual(out["skills"]["brainstorm"], {"runs": 4, "complete": 0, "medianActiveSeconds": None})
        self.assertEqual(out["skills"]["architecture"], {"runs": 1, "complete": 0, "medianActiveSeconds": None})
        self.assertEqual(out["runs"], {"read": 5, "skipped": 0})

    def test_ver51_an_idle_end_with_a_conditional_step_that_did_not_apply_is_complete(self):
        names = self.run_names("architecture", 2)
        self.add(names[0], fx.architecture_run_ending_idle())
        self.add(names[1], fx.architecture_run_ending_idle())
        out = self.figures()
        self.assertEqual(out["skills"]["architecture"]["complete"], 2)
        active = json.loads(self.state(fx.architecture_run_ending_idle()))["timing"]["activeSeconds"]
        self.assertEqual(out["skills"]["architecture"]["medianActiveSeconds"], active)

    def test_ver51_every_skill_the_states_name_has_an_entry_built_or_not(self):
        self.add(fx.run_name("brainstorm", 1), fx.brainstorm_run(300))
        self.add(fx.run_name("prd", 2), mc.Log("prd").tick(1, 2).end("session-end"))  # no manifest: a run all the same
        self.add(fx.run_name("shipit", 3), mc.Log("shipit", checklist=mc.SHIPIT).tick(1).end("session-end"))
        self.assertEqual(sorted(self.figures()["skills"]), ["brainstorm", "prd", "shipit"])

    def test_ver51_states_that_are_not_run_states_are_skipped_and_counted(self):
        good = json.loads(self.state(fx.brainstorm_run(600)))
        no_timing = {k: v for k, v in good.items() if k != "timing"}
        wrong_format = dict(good, format="devforgeai-progress/2")
        bad_skill = dict(good, skill=7)
        no_active = dict(good, timing={"started": None})
        bool_active = dict(good, timing=dict(good["timing"], activeSeconds=True))
        float_active = dict(good, timing=dict(good["timing"], activeSeconds=1.5))
        self.add(self.run_names("brainstorm", 1)[0], json.dumps(good))
        bad = {"no-timing": json.dumps(no_timing), "not-json": "this is not json {", "empty": "", "array": "[1, 2]",
               "format": json.dumps(wrong_format), "skill": json.dumps(bad_skill), "no-active": json.dumps(no_active),
               "bool-active": json.dumps(bool_active), "float-active": json.dumps(float_active),
               "string": json.dumps("a string")}
        for name, text in bad.items():
            fx.put_run(self.root, "bad-" + name, text)
        out = self.figures()
        self.assertEqual(out["runs"], {"read": 1, "skipped": len(bad)})
        self.assertEqual(out["skills"], {"brainstorm": {"runs": 1, "complete": 1, "medianActiveSeconds": None}})

    # The review of the build (review-build-028.md, S1): a state of the right format whose skill holds a lone surrogate
    # ("\\ud800x" is legal JSON) can't be printed as UTF-8. It is skipped under ERR-15 like any state that isn't a run's,
    # so one bad state never hides the history (exit 0, never a traceback).
    def test_ver51_a_state_whose_skill_cannot_be_printed_is_skipped(self):
        good = json.loads(self.state(fx.brainstorm_run(600)))
        self.add(self.run_names("brainstorm", 1)[0], json.dumps(good))
        fx.put_run(self.root, "bad-surrogate", json.dumps(dict(good, skill="\ud800x")))  # written as the escape \ud800
        fx.put_run(self.root, "bad-surrogate-mid", json.dumps(dict(good, skill="a\udfffb")))
        out = self.figures()
        self.assertEqual(out["runs"], {"read": 1, "skipped": 2})
        self.assertEqual(sorted(out["skills"]), ["brainstorm"])

    def test_ver52_a_lone_surrogate_in_a_ledger_line_is_a_string_like_any_other(self):
        fx.ledger(self.root, "S1.jsonl", [json.dumps(fx.line("\ud800", "\udfff", "main", 1, 2, 3, 4))])  # escapes, as written
        out = self.figures()["odometer"]
        self.assertEqual((out["turns"], out["malformed"], out["tokens"]), (1, 0, 10))

    def test_ver51_what_is_ignored_and_what_is_a_link(self):
        self.add(self.run_names("brainstorm", 1)[0], fx.brainstorm_run(600))
        (self.root / "devforgeai/progress/runs/no-state-json").mkdir()  # a run folder with no state.json: uncounted
        (self.root / "devforgeai/progress/runs/stray.txt").write_text("x\n")  # a file beside the run folders: uncounted
        out = self.figures()
        self.assertEqual(out["runs"], {"read": 1, "skipped": 0})
        elsewhere = Path(self._tmp.name) / "elsewhere"
        fx.write(elsewhere, "state.json", self.state(fx.brainstorm_run(900)))
        runs = self.root / "devforgeai/progress/runs"
        os.symlink(elsewhere, runs / "linked-run")  # a run folder that is a link: skipped, its state never read
        again = self.figures()
        self.assertEqual(again["runs"], {"read": 1, "skipped": 1})
        self.assertEqual(again["skills"], out["skills"])
        os.symlink(elsewhere / "state.json", runs / "linked-state-file")  # ERR-15: any entry of runs/ that is a link
        self.assertEqual(self.figures()["runs"], {"read": 1, "skipped": 2})

    def test_ver51_a_state_json_that_is_a_link_is_skipped_and_not_followed(self):
        elsewhere = Path(self._tmp.name) / "elsewhere.json"
        elsewhere.write_text(self.state(fx.brainstorm_run(900)), encoding="utf-8")
        folder = self.root / "devforgeai/progress/runs/linked"
        folder.mkdir(parents=True)
        os.symlink(elsewhere, folder / "state.json")
        out = self.figures()
        self.assertEqual((out["runs"], out["skills"]), ({"read": 0, "skipped": 1}, {}))

    def test_ver51_the_same_figures_whatever_order_the_folders_were_made_in(self):
        states = [(fx.run_name("brainstorm", i), self.state(fx.brainstorm_run(a))) for i, a in enumerate((600, 1200, 900, 300))]
        states.append((fx.run_name("brainstorm", 9), "not json"))
        first = self.history().stdout
        self.assertIn('"skills": {}', first)
        for name, text in states:
            fx.put_run(self.root, name, text)
        forward = self.history().stdout
        other = Path(self._tmp.name) / "other"
        other.mkdir()
        for name, text in reversed(states):
            fx.put_run(other, name, text)
        self.assertEqual(self.history(other).stdout, forward)
        self.assertNotEqual(forward, first)

    def test_ver51_no_runs_folder_gives_empty_figures(self):
        out = self.figures()
        self.assertEqual(out, {"format": "devforgeai-history/1", "skills": {}, "odometer": ZERO,
                               "runs": {"read": 0, "skipped": 0}})
        (self.root / "devforgeai/progress/runs").mkdir(parents=True)
        self.assertEqual(self.figures(), out)

    def test_ver51_errors_exit_2_with_nothing_on_stdout_and_one_line_on_stderr(self):
        a_file = self.root / "a-file"
        a_file.write_text("x\n")
        for args in ([], ["--root"], ["--root", self.root / "missing"], ["--root", a_file],
                     ["--root", self.root, "--bogus"], ["--bogus"], ["--root", self.root, "extra"]):
            with self.subTest(args=[str(a) for a in args]):
                proc = fx.run_script(fx.HISTORY, args, self.INTERPRETER)
                self.assert_refused(proc, "")


class OdometerRules(Base):
    """VER-52: the ledger, one file for each session."""

    def valid(self, *lines):
        """Every generated line is a DM-04 line."""
        check = validator("odometer")
        for l in lines:
            self.assertEqual([e.message for e in check.iter_errors(l)], [], l)

    def test_ver52_main_loop_and_agents_over_turns_in_two_session_files(self):
        one = [fx.line("S1", "t1", "main", 10, 5, 100, 20), fx.line("S1", "t1", "agent-a", 1, 2, 3, 4),
               fx.line("S1", "t1", "agent-b", 5, 6, 7, 8), fx.line("S1", "t2", "main", 20, 10, 200, 40)]
        two = [fx.line("S2", "t1", "main", 7, 7, 7, 7), fx.line("S2", "t2", "agent-a", 1, 1, 1, 1)]
        self.valid(*one, *two)
        fx.ledger(self.root, "S1.jsonl", one)
        fx.ledger(self.root, "S2.jsonl", two)
        # A run with usage events beside them: the ledger's lines alone are totalled (BEH-28).
        log = mc.Log("brainstorm").usage("t1", input=1000, output=1000, cache_read=1000, cache_write=1000).tick(1)
        self.add(self.run_names("brainstorm", 1)[0], log)
        out = self.figures()
        self.assertEqual(out["odometer"], {"input": 44, "output": 31, "cacheRead": 318, "cacheWrite": 80, "tokens": 473,
                                           "turns": 6, "duplicates": 0, "malformed": 0})
        self.assertEqual(out["runs"], {"read": 1, "skipped": 0})

    def test_ver52_a_repeated_triple_counts_once_wherever_it_is(self):
        fx.ledger(self.root, "a.jsonl", [fx.line("S1", "t1", "main", 10, 10, 10, 10),
                                         fx.line("S1", "t1", "main", 99, 99, 99, 99),  # same file: the first counts
                                         fx.line("S1", "t1", "agent", 1, 1, 1, 1),  # same turn, another source: counts
                                         fx.line("S2", "t1", "main", 2, 2, 2, 2)])  # same turn ID, another session: counts
        fx.ledger(self.root, "b.jsonl", [fx.line("S1", "t1", "main", 77, 77, 77, 77),  # an earlier file had it
                                         fx.line("S1", "t2", "main", 3, 3, 3, 3)])
        out = self.figures()["odometer"]
        self.assertEqual((out["input"], out["turns"], out["duplicates"], out["malformed"]), (10 + 1 + 2 + 3, 4, 2, 0))
        self.assertEqual(out["tokens"], 4 * out["input"])

    def test_ver52_files_are_taken_in_the_byte_order_of_their_names(self):
        # B sorts before a in byte order; the line in the earlier file stands whatever order the files were made in.
        fx.ledger(self.root, "a.jsonl", [fx.line("S1", "t1", "main", 5, 5, 5, 5)])
        fx.ledger(self.root, "B.jsonl", [fx.line("S1", "t1", "main", 9, 9, 9, 9)])
        out = self.figures()["odometer"]
        self.assertEqual((out["input"], out["duplicates"]), (9, 1))

    def test_ver52_a_line_counts_by_its_own_session_whatever_file_holds_it(self):
        fx.ledger(self.root, "x.jsonl", [fx.line("S1", "t1", "main", 4, 4, 4, 4)])
        fx.ledger(self.root, "y.jsonl", [fx.line("S1", "t2", "main", 6, 6, 6, 6), fx.line("S9", "t1", "main", 1, 1, 1, 1)])
        self.assertEqual(self.figures()["odometer"]["turns"], 3)

    def test_ver52_a_link_a_folder_and_other_files_are_ignored_and_counted_nowhere(self):
        fx.ledger(self.root, "S1.jsonl", [fx.line("S1", "t1", "main", 1, 2, 3, 4)])
        elsewhere = Path(self._tmp.name) / "elsewhere"
        fx.ledger(elsewhere, "S9.jsonl", [fx.line("S9", "t1", "main", 100, 100, 100, 100)])
        folder = self.root / fx.LEDGER
        os.symlink(elsewhere / fx.LEDGER / "S9.jsonl", folder / "linked.jsonl")
        os.symlink(elsewhere / fx.LEDGER, folder / "linked-folder.jsonl")
        (folder / "folder.jsonl").mkdir()
        fx.ledger(self.root, "folder.jsonl/inner.jsonl", [fx.line("S8", "t1", "main", 100, 100, 100, 100)])
        (folder / "notes.txt").write_text('{"junk": true}\n')
        (folder / "S1.jsonl.bak").write_text(json.dumps(fx.line("S7", "t1", "main", 100, 100, 100, 100)) + "\n")
        out = self.figures()["odometer"]
        self.assertEqual(out, {"input": 1, "output": 2, "cacheRead": 3, "cacheWrite": 4, "tokens": 10, "turns": 1,
                               "duplicates": 0, "malformed": 0})

    def test_ver52_a_blank_line_is_ignored(self):
        fx.ledger(self.root, "S1.jsonl", [fx.line("S1", "t1", "main", 1, 1, 1, 1), "", "   ", "\t",
                                          fx.line("S1", "t2", "main", 1, 1, 1, 1)])
        out = self.figures()["odometer"]
        self.assertEqual((out["turns"], out["malformed"], out["duplicates"]), (2, 0, 0))

    def test_ver52_what_is_malformed(self):
        good = fx.line("S1", "t0", "main", 1, 1, 1, 1)
        base = fx.line("S1", "tx", "main", 5, 5, 5, 5)
        cut = json.dumps(fx.line("S1", "t-cut", "main", 5, 5, 5, 5), sort_keys=True)[:-8]
        variants = {
            "not json": "this is not json",
            "array": json.dumps([base]),
            "a string": json.dumps("S1"),
            "missing session": {k: v for k, v in base.items() if k != "session"},
            "missing turn": {k: v for k, v in base.items() if k != "turn"},
            "missing source": {k: v for k, v in base.items() if k != "source"},
            "missing count": {k: v for k, v in base.items() if k != "cacheWrite"},
            "empty session": dict(base, session=""),
            "empty turn": dict(base, turn=""),
            "empty source": dict(base, source=""),
            "numeric session": dict(base, session=7),
            "negative count": dict(base, input=-1),
            "string count": dict(base, output="5"),
            "true count": dict(base, cacheRead=True),
            "false count": dict(base, cacheWrite=False),
            "fractional count": dict(base, input=1.5),
            "null count": dict(base, output=None),
            "missing time": {k: v for k, v in base.items() if k != "time"},
            "numeric time": dict(base, time=5),
            "not UTF-8": b"\xff\xfe{}",
        }
        lines = [json.dumps(good, sort_keys=True)]
        for value in variants.values():
            lines.append(value if isinstance(value, (str, bytes)) else json.dumps(value, sort_keys=True))
        lines.append(json.dumps(fx.line("S1", "t9", "main", 1, 1, 1, 1), sort_keys=True))
        text = b"\n".join(l if isinstance(l, bytes) else l.encode("utf-8") for l in lines) + b"\n" + cut.encode("utf-8")
        fx.write(self.root, "%s/S1.jsonl" % fx.LEDGER, text, "wb")  # the last line is cut short, with no newline
        out = self.figures()["odometer"]
        self.assertEqual(out["malformed"], len(variants) + 1)
        self.assertEqual((out["turns"], out["duplicates"], out["input"], out["tokens"]), (2, 0, 2, 8))

    def test_ver52_a_line_with_a_key_the_reader_does_not_know_still_counts(self):
        self.valid(fx.line("S1", "t1", "main"))
        fx.ledger(self.root, "S1.jsonl", [dict(fx.line("S1", "t1", "main", 3, 3, 3, 3), model="claude-opus-5-5", extra=[1])])
        self.assertEqual(self.figures()["odometer"]["turns"], 1)

    def test_ver52_the_time_is_read_as_text_and_no_line_is_dropped_for_its_age(self):
        fx.ledger(self.root, "S1.jsonl", [fx.line("S1", "t1", "main", 2, 2, 2, 2, time="2001-01-01T00:00:00Z"),
                                          fx.line("S1", "t2", "main", 2, 2, 2, 2, time="yesterday"),
                                          fx.line("S1", "t3", "main", 2, 2, 2, 2, time="")])
        self.add(self.run_names("brainstorm", 1)[0], fx.brainstorm_run(60))  # a run that started long after the lines
        out = self.figures()["odometer"]
        self.assertEqual((out["turns"], out["malformed"], out["input"]), (3, 0, 6))

    def test_ver52_no_odometer_folder_and_an_empty_one_give_zeros(self):
        self.assertEqual(self.figures()["odometer"], ZERO)
        (self.root / fx.LEDGER).mkdir(parents=True)
        self.assertEqual(self.figures()["odometer"], ZERO)
        fx.ledger(self.root, "empty.jsonl", [])
        self.assertEqual(self.figures()["odometer"], ZERO)

    def test_ver52_an_odometer_folder_that_is_a_link_is_not_followed(self):
        elsewhere = Path(self._tmp.name) / "elsewhere"
        fx.ledger(elsewhere, "S1.jsonl", [fx.line("S1", "t1", "main", 9, 9, 9, 9)])
        (self.root / "devforgeai/progress").mkdir(parents=True)
        os.symlink(elsewhere / fx.LEDGER, self.root / fx.LEDGER)
        self.assertEqual(self.figures()["odometer"], ZERO)

    def test_ver52_a_ledger_file_that_cannot_be_read_is_an_error_naming_it(self):
        path = fx.ledger(self.root, "S1.jsonl", [fx.line("S1", "t1", "main")])
        fx.ledger(self.root, "S0.jsonl", [fx.line("S0", "t1", "main")])
        os.chmod(path, 0)
        try:
            if os.access(path, os.R_OK):
                self.skipTest("the permission doesn't bind this user")
            proc = self.history()
        finally:
            os.chmod(path, 0o644)
        self.assert_refused(proc, "S1.jsonl")

    def test_ver52_the_figures_are_the_ledgers_alone_beside_run_states_with_usage(self):
        fx.ledger(self.root, "S1.jsonl", [fx.line("S1", "t1", "main", 1, 1, 1, 1)])
        log = mc.Log("brainstorm").usage("a", input=500, output=500, cache_read=500, cache_write=500)
        log.usage("b", input=500, output=500, cache_read=500, cache_write=500).tick(1).end("session-end")
        self.add(self.run_names("brainstorm", 1)[0], log)
        out = self.figures()
        self.assertEqual(out["odometer"]["tokens"], 4)
        self.assertEqual(out["runs"]["read"], 1)


class RunRulesUnderS(RunRules):
    """Every RunRules test with the script (and the evaluator that makes the fixtures) under python3 -S (QR-05)."""
    INTERPRETER = (sys.executable, "-S", "-B")


class OdometerRulesUnderS(OdometerRules):
    INTERPRETER = (sys.executable, "-S", "-B")


if __name__ == "__main__":
    unittest.main()
