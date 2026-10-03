"""Tests for SPEC-012's progress evaluator (src/claude/DevForgeAI/progress/evaluate.py).

SpecRules checks each VER item's obligation as properties of the evaluator's output. Goldens compares
each case's output with its reviewed expected.json, byte for byte, so a failure there means the output
changed rather than that a rule broke. SpecRulesUnderS runs every SpecRules test with the evaluator
under `python3 -S` (VER-18, QR-01). The test runner itself needs jsonschema (VER-02).

The evaluator runs as a separate process, as its contract is exit codes, a stderr line, a stdout
summary and a file. Every spawn uses -B, so no __pycache__ lands in the plugin folder, which deploys.

Run from the repository root:
    PYTHONDONTWRITEBYTECODE=1 python3 -B -m pytest -q -p no:cacheprovider src/tests/progress
"""
import json
import re
import shutil
import subprocess
import sys
import tempfile
import time
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import make_cases as mc  # noqa: E402

ROOT = mc.ROOT
PROGRESS = ROOT / "src/claude/DevForgeAI/progress"
SCHEMAS = PROGRESS / "schemas"
SKILLS = ROOT / "src/claude/DevForgeAI/skills"


def schema_validator(name):
    return Draft202012Validator(json.loads((SCHEMAS / (name + ".schema.json")).read_text(encoding="utf-8")))


class Base(unittest.TestCase):
    INTERPRETER = (sys.executable, "-B")

    def run_case(self, name):
        """Evaluate a case; return (state, completed process, the output's bytes, files left in the out folder)."""
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "state.json"
            proc = subprocess.run(mc.evaluate_args(name, out, self.INTERPRETER), cwd=ROOT,
                                  capture_output=True, text=True)
            self.assertEqual(proc.returncode, 0, "%s: %s" % (name, proc.stderr))
            raw = out.read_bytes()
            left = sorted(p.name for p in Path(tmp).iterdir())
        return json.loads(raw), proc, raw, left

    def run_cli(self, *args):
        return subprocess.run(list(self.INTERPRETER) + [mc.EVALUATE] + [str(a) for a in args], cwd=ROOT,
                              capture_output=True, text=True)

    @staticmethod
    def step(state, n):
        return next(s for s in state["steps"] if s["n"] == n)

    @staticmethod
    def flags(state, step=None, kind=None):
        return [f for f in state["flags"]
                if (step is None or f["step"] == step) and (kind is None or f["type"] == kind)]


class SpecRules(Base):

    # VER-01: the manifests validate, and IF-02 binds each to its skill's checklist.
    def test_ver01_manifests_validate_and_match_their_skills(self):
        validator = schema_validator("manifest")
        for skill in ("brainstorm", "architecture"):
            with self.subTest(skill):
                manifest = json.loads((PROGRESS / "manifests" / (skill + ".json")).read_text(encoding="utf-8"))
                self.assertEqual([e.message for e in validator.iter_errors(manifest)], [])
                skill_md = SKILLS / skill / "SKILL.md"
                expected = mc.checklist_hash(skill_md.read_text(encoding="utf-8"))
                self.assertEqual(manifest["checklistHash"], expected)
                proc = self.run_cli("check", "--manifests", mc.PLUGIN_MANIFESTS, "--skill", skill,
                                    "--checklist", skill_md.relative_to(ROOT))
                self.assertEqual(proc.returncode, 0, proc.stderr)
                self.assertEqual(proc.stdout.strip(), "matched " + expected)

    def test_ver01_check_reports_stale_and_none(self):
        with tempfile.TemporaryDirectory() as tmp:
            changed = Path(tmp) / "SKILL.md"
            changed.write_text(mc.checklist_block("brainstorm").replace("6. Write the BRN", "6. Write it"),
                               encoding="utf-8")
            proc = self.run_cli("check", "--manifests", mc.PLUGIN_MANIFESTS, "--skill", "brainstorm",
                                "--checklist", changed)
            self.assertEqual(proc.returncode, 1)
            self.assertTrue(proc.stdout.startswith("stale manifest sha256:"), proc.stdout)
            self.assertIn(" checklist " + mc.checklist_hash(changed.read_text(encoding="utf-8")), proc.stdout)
            proc = self.run_cli("check", "--manifests", mc.PLUGIN_MANIFESTS, "--skill", "prd",
                                "--checklist", (SKILLS / "prd/SKILL.md").relative_to(ROOT))
            self.assertEqual(proc.returncode, 1)
            self.assertTrue(proc.stdout.startswith("none sha256:"), proc.stdout)

    # VER-02: events and states validate against their schemas.
    def test_ver02_events_and_states_validate(self):
        events_v, state_v = schema_validator("events"), schema_validator("progress")
        for name in mc.CASE_BUILDERS:
            with self.subTest(name):
                if name != "messy-log":  # its malformed lines are the point of that case
                    for line in (mc.CASES / name / "events.jsonl").read_text(encoding="utf-8").splitlines():
                        self.assertEqual([e.message for e in events_v.iter_errors(json.loads(line))], [])
                state, _, _, _ = self.run_case(name)
                self.assertEqual([e.message for e in state_v.iter_errors(state)], [])
                expected = mc.CASES / name / "expected.json"
                if expected.exists():
                    doc = json.loads(expected.read_text(encoding="utf-8"))
                    self.assertEqual([e.message for e in state_v.iter_errors(doc)], [])

    # VER-03: evidence, current step, no flags while the run is open.
    def test_ver03_arch_reading(self):
        state, _, _, _ = self.run_case("arch-reading")
        s1, s2, s3 = (self.step(state, n) for n in (1, 2, 3))
        self.assertEqual((s1["state"], s1["evidence"][0]["type"], s1["evidence"][0]["strength"]),
                         ("done", "script", "strong"))
        self.assertEqual((s2["state"], s2["evidence"][0]["type"], s2["evidence"][0]["strength"]),
                         ("done", "read", "medium"))
        self.assertEqual(s3["state"], "done")
        self.assertEqual(state["current"], 4)
        self.assertEqual(state["flags"], [])
        self.assertEqual(state["gate"], {"kind": None, "seq": None, "refuse": False, "reason": None})
        self.assertIsNone(state["next"])

    # VER-04: a step seen late is noted, never flagged.
    def test_ver04_late_step(self):
        before, _, _, _ = self.run_case("arch-late-step-before")
        s4 = self.step(before, 4)
        self.assertEqual((s4["state"], s4["note"]), ("pending", "not seen yet"))
        self.assertEqual(before["current"], 7)
        self.assertEqual(before["flags"], [])
        after, _, _, _ = self.run_case("arch-late-step")
        s4 = self.step(after, 4)
        self.assertEqual((s4["state"], s4["note"]), ("done", "seen late (after step 6)"))
        self.assertEqual(after["flags"], [])

    # VER-05: your turn, then the answer.
    def test_ver05_your_turn(self):
        waiting, _, _, _ = self.run_case("arch-your-turn-waiting")
        self.assertEqual(waiting["current"], 7)
        self.assertEqual(self.step(waiting, 7)["state"], "your-turn")
        answered, _, _, _ = self.run_case("arch-your-turn")
        s7 = self.step(answered, 7)
        self.assertEqual(s7["state"], "done")
        self.assertIn(("answer", "strong"), [(e["type"], e["strength"]) for e in s7["evidence"]])

    # VER-06: an outcome written without confirmation is flagged at the write gate.
    def test_ver06_outcome_unconfirmed(self):
        state, _, _, _ = self.run_case("arch-outcome-unconfirmed")
        self.assertEqual(self.step(state, 7)["state"], "done")
        self.assertEqual(self.step(state, 8)["state"], "skipped")
        self.assertEqual([f["gate"] for f in self.flags(state, 8, "skipped")], ["write"])
        self.assertEqual(self.step(state, 9)["state"], "rule-broken")
        broken = self.flags(state, 9, "rule-broken")
        self.assertEqual(len(broken), 1)
        for word in ("ARCH-001", "outcome", "create"):
            self.assertIn(word, broken[0]["message"])
        self.assertFalse([f for f in state["flags"] if "ADR-004" in f["message"]])
        self.assertTrue(state["gate"]["refuse"])
        self.assertEqual(state["gate"]["kind"], "write")

    def test_ver06_outcome_confirmed(self):
        state, _, _, _ = self.run_case("arch-outcome-confirmed")
        s8 = self.step(state, 8)
        self.assertEqual(s8["state"], "done")
        self.assertIn(("answer", "strong"), [(e["type"], e["strength"]) for e in s8["evidence"]])
        self.assertEqual(state["flags"], [])

    # VER-07: an ADR accepted without an answer at step 7.
    def test_ver07_adr_without_answer(self):
        state, _, _, _ = self.run_case("arch-adr-accepted-unanswered")
        self.assertEqual(self.step(state, 7)["state"], "skipped")
        self.assertEqual(self.step(state, 9)["state"], "rule-broken")
        broken = self.flags(state, 9, "rule-broken")
        self.assertEqual(len(broken), 1)
        for word in ("ADR-004", "status", "accepted"):
            self.assertIn(word, broken[0]["message"])
        proposed, _, _, _ = self.run_case("arch-adr-proposed-unanswered")
        s7 = self.step(proposed, 7)
        self.assertEqual((s7["state"], s7["note"]), ("not-applicable", "no answer; left open"))
        self.assertEqual(proposed["flags"], [])

    # VER-08: SPEC-001 VER-02's allowed path raises nothing.
    def test_ver08_brn_left_open(self):
        state, _, _, _ = self.run_case("brn-left-open")
        s5 = self.step(state, 5)
        self.assertEqual((s5["state"], s5["note"]), ("not-applicable", "no answer; left open"))
        self.assertEqual((self.step(state, 6)["state"], self.step(state, 7)["state"]), ("done", "done"))
        self.assertEqual(state["flags"], [])
        self.assertEqual((state["next"]["skill"], state["next"]["available"]), ("prd", True))

    # VER-09: dispositions written without confirmation.
    def test_ver09_brn_unconfirmed(self):
        state, _, _, _ = self.run_case("brn-unconfirmed-cut")
        self.assertEqual(self.step(state, 5)["state"], "skipped")
        self.assertEqual(self.step(state, 6)["state"], "rule-broken")
        self.assertTrue(state["gate"]["refuse"])
        broken = self.flags(state, 6, "rule-broken")
        self.assertEqual(len(broken), 1)
        for word in ("BRN-002", "disposition", "promoted"):
            self.assertIn(word, broken[0]["message"])
        self.assertEqual(len(self.flags(state, 5, "skipped")), 1)
        # The full log reaches the report gate too, which finds the same steps and adds no flag:
        # one flag per step and type across gates (a build decision recorded in SPEC-012 section 9).
        full, _, _, _ = self.run_case("brn-unconfirmed")
        self.assertEqual(len(full["flags"]), 2)
        self.assertEqual(full["gate"]["kind"], "report")
        self.assertFalse(full["gate"]["refuse"])
        status, _, _, _ = self.run_case("brn-unconfirmed-status")
        broken = self.flags(status, 6, "rule-broken")
        self.assertEqual(len(broken), 1)
        for word in ("status", "converged"):
            self.assertIn(word, broken[0]["message"])
        self.assertEqual(len(self.flags(status, 5, "skipped")), 1)

    # VER-10: answer windows.
    def test_ver10_answer_windows(self):
        early, _, _, _ = self.run_case("brn-answer-early")
        self.assertEqual(self.step(early, 5)["state"], "skipped")
        self.assertEqual(self.step(early, 6)["state"], "rule-broken")
        after, _, _, _ = self.run_case("brn-answer-after")
        self.assertEqual(self.step(after, 5)["state"], "done")
        self.assertEqual(after["flags"], [])

    # BEH-09 as built (a recorded departure): ticking a step as Claude asks doesn't lose the answer.
    def test_beh09_tick_then_answer(self):
        state, _, _, _ = self.run_case("brn-ticked-then-answered")
        s5 = self.step(state, 5)
        self.assertEqual(s5["state"], "done")
        self.assertIn(("answer", "strong"), [(e["type"], e["strength"]) for e in s5["evidence"]])
        self.assertEqual(state["flags"], [])

    # VER-11: validation claimed but not run, failed, or run on another file.
    def test_ver11_validation_claimed(self):
        for name in ("brn-validation-claimed", "brn-validation-failed", "brn-validation-other-file"):
            with self.subTest(name):
                state, _, _, _ = self.run_case(name)
                self.assertEqual(self.step(state, 7)["state"], "claimed")
                flags = self.flags(state, 7, "claimed-not-evidenced")
                self.assertEqual([f["gate"] for f in flags], ["report"])

    # VER-12: a legitimate skip.
    def test_ver12_skipped_with_reason(self):
        state, _, _, _ = self.run_case("skipped-with-reason")
        s3 = self.step(state, 3)
        self.assertEqual(s3["state"], "skipped-with-reason")
        self.assertEqual(s3["claim"]["reason"], "no remote")
        self.assertEqual(state["flags"], [])

    # VER-13: stale and missing manifests track claims only.
    def test_ver13_stale_and_no_manifest(self):
        stale, _, _, _ = self.run_case("stale-manifest")
        self.assertEqual(stale["manifest"]["state"], "stale")
        self.assertEqual(self.step(stale, 6)["title"], "Write the BRN file")
        self.assertTrue(all(s["kind"] is None and s["need"] == "text-only" for s in stale["steps"]))
        self.assertEqual([self.step(stale, n)["state"] for n in (1, 2, 3)], ["done"] * 3)
        self.assertIn("out of date", self.step(stale, 1)["note"])
        self.assertEqual(stale["flags"], [])
        none, _, _, _ = self.run_case("no-manifest")
        self.assertEqual(none["manifest"]["state"], "none")
        self.assertIn("no manifest", self.step(none, 1)["note"])
        self.assertEqual(none["flags"], [])

    # VER-14: a run with no replies.
    def test_ver14_evidence_only(self):
        state, _, _, _ = self.run_case("evidence-only")
        self.assertEqual(self.step(state, 6)["state"], "unconfirmed")
        s5 = self.step(state, 5)
        self.assertEqual((s5["state"], s5["note"]), ("not-applicable", "the user named paths to inspect"))
        self.assertEqual(state["flags"], [])
        self.assertEqual(state["ended"], "another-skill")

    # VER-15: a messy log, and nothing written beside --out.
    def test_ver15_messy_log(self):
        state, _, _, left = self.run_case("messy-log")
        counts = state["counts"]
        self.assertEqual((counts["malformed"], counts["outOfOrder"], counts["duplicates"],
                          counts["unknownClaims"], counts["afterEnd"]), (3, 1, 1, 1, 2))
        self.assertEqual(self.step(state, 5)["note"], "content not available; rule not checked")
        self.assertEqual(self.flags(state, 5), [])
        self.assertEqual(left, ["state.json"])

    # VER-16: runs that can't proceed exit 2, name the file and leave no state.
    def test_ver16_exit_2(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            good = mc.CASES / "brn-left-open" / "events.jsonl"
            first_tool = tmp / "first-tool.jsonl"
            lines = good.read_text(encoding="utf-8").splitlines()
            first_tool.write_text("\n".join(lines[1:]) + "\n", encoding="utf-8")
            bad_manifests = tmp / "manifests"
            bad_manifests.mkdir()
            (bad_manifests / "brainstorm.json").write_text("{not json", encoding="utf-8")
            runs = [
                ("first event", ["--manifests", mc.PLUGIN_MANIFESTS, "--events", first_tool], first_tool.name),
                ("manifest", ["--manifests", bad_manifests, "--events", good], "brainstorm.json"),
                ("events", ["--manifests", mc.PLUGIN_MANIFESTS, "--events", tmp / "missing.jsonl"],
                 "missing.jsonl"),
            ]
            for label, args, named in runs:
                with self.subTest(label):
                    out = tmp / ("out-%s.json" % label.replace(" ", "-"))
                    proc = self.run_cli("evaluate", *args, "--out", out)
                    self.assertEqual(proc.returncode, 2)
                    self.assertEqual(len(proc.stderr.strip().splitlines()), 1, proc.stderr)
                    self.assertIn(named, proc.stderr)
                    self.assertFalse(out.exists())
            with self.subTest("out folder"):
                out = tmp / "no-such-folder" / "state.json"
                proc = self.run_cli("evaluate", "--manifests", mc.PLUGIN_MANIFESTS, "--events", good,
                                    "--out", out)
                self.assertEqual(proc.returncode, 2)
                self.assertEqual(len(proc.stderr.strip().splitlines()), 1, proc.stderr)
                self.assertIn("no-such-folder", proc.stderr)

    # VER-17: the summary line, phases, and next after epic.
    def test_ver17_summary_phases_next(self):
        _, proc, _, _ = self.run_case("brn-unconfirmed-cut")
        self.assertEqual(proc.stdout.strip(), "progress brainstorm: step 7 of 8, 2 flags, refuse")
        left_open, proc, _, _ = self.run_case("brn-left-open")
        self.assertEqual(proc.stdout.strip(), "progress brainstorm: all 8 steps reached, 0 flags")
        self.assertNotIn("phases", left_open)
        phases, _, _, _ = self.run_case("phases")
        self.assertEqual(phases["phases"],
                         json.loads((mc.CASES / "phases/phases.json").read_text(encoding="utf-8")))
        epic, proc, _, _ = self.run_case("epic-ended")
        self.assertEqual(epic["next"], {"skill": "story", "available": False,
                                        "note": "the story skill isn't built yet (SPEC-009)"})
        self.assertEqual(proc.stdout.strip(), "progress epic: ended (another-skill), 0 flags")

    # VER-18: the same inputs give the same bytes (and SpecRulesUnderS repeats everything under -S).
    def test_ver18_deterministic(self):
        for name in mc.CASE_BUILDERS:
            with self.subTest(name):
                _, _, first, _ = self.run_case(name)
                _, _, second, _ = self.run_case(name)
                self.assertEqual(first, second)

    # VER-19: a 500-event log evaluates quickly.
    def test_ver19_performance(self):
        log = mc.Log("architecture")
        mc.arch_start(log).glob("docs/specs/arch/ARCH-*.md").tick(1, 2, 3, 4, 6)
        while len(log.events) < 499:
            log.read("src/module_%03d.py" % len(log.events))
            log.reply("Reading the code.\n- [x] 6. done")
        with tempfile.TemporaryDirectory() as tmp:
            events = Path(tmp) / "events.jsonl"
            events.write_text("\n".join(log.lines()[:500]) + "\n", encoding="utf-8")
            started = time.perf_counter()
            proc = self.run_cli("evaluate", "--manifests", mc.PLUGIN_MANIFESTS, "--events", events,
                                "--out", Path(tmp) / "state.json")
            elapsed = time.perf_counter() - started
        self.assertEqual(proc.returncode, 0, proc.stderr)
        print("\nVER-19: 500 events evaluated in %.0f ms (%s)" % (elapsed * 1000, " ".join(self.INTERPRETER[1:])))
        self.assertLess(elapsed, 1.0)

    # VER-20: a project layer adds a rule; a project's own skill.
    def test_ver20_layers_add(self):
        state, _, _, _ = self.run_case("layer-adds-rule")
        self.assertEqual(self.step(state, 5)["state"], "skipped")
        broken = self.flags(state, 6, "rule-broken")
        self.assertEqual(len(broken), 1)
        for word in ("reason", "keeps-teens"):
            self.assertIn(word, broken[0]["message"])
        self.assertEqual(state["manifest"]["layers"], [
            mc.PLUGIN_MANIFESTS + "/brainstorm.json",
            "src/tests/progress/cases/layer-adds-rule/project/brainstorm.json"])
        own, _, _, _ = self.run_case("layer-own-skill")
        self.assertEqual(own["manifest"]["state"], "matched")
        self.assertEqual(own["manifest"]["layers"], ["src/tests/progress/cases/layer-own-skill/project/team-review.json"])
        self.assertEqual(own["flags"], [])

    # VER-21: a project layer that relaxes a rule stops evaluation.
    def test_ver21_layers_relax(self):
        plugin = json.loads((PROGRESS / "manifests/brainstorm.json").read_text(encoding="utf-8"))

        def need_text_only(m):
            m["steps"]["7"]["need"] = "text-only"

        def drop_gate(m):
            del m["steps"]["6"]["gate"]

        def drop_rule(m):
            m["contentRules"] = [r for r in m["contentRules"] if r["field"] != "disposition"]

        def change_kind(m):
            m["steps"]["2"]["kind"] = "read"

        def other_hash(m):
            m["checklistHash"] = "sha256:" + "0" * 64

        events = mc.CASES / "brn-left-open" / "events.jsonl"
        for mutate in (need_text_only, drop_gate, drop_rule, change_kind, other_hash):
            with self.subTest(mutate.__name__), tempfile.TemporaryDirectory() as tmp:
                project = Path(tmp) / "project"
                project.mkdir()
                manifest = json.loads(json.dumps(plugin))
                mutate(manifest)
                (project / "brainstorm.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
                out = Path(tmp) / "state.json"
                proc = self.run_cli("evaluate", "--manifests", mc.PLUGIN_MANIFESTS, "--manifests", project,
                                    "--events", events, "--out", out)
                self.assertEqual(proc.returncode, 2, proc.stdout)
                self.assertEqual(len(proc.stderr.strip().splitlines()), 1, proc.stderr)
                self.assertIn(str(project / "brainstorm.json"), proc.stderr)
                self.assertIn(mc.PLUGIN_MANIFESTS + "/brainstorm.json", proc.stderr)
                self.assertFalse(out.exists())

    # The committed cases are what the generator writes.
    def test_cases_are_current(self):
        proc = subprocess.run([sys.executable, "-B", str(HERE / "make_cases.py"), "--check"], cwd=ROOT,
                              capture_output=True, text=True)
        self.assertEqual(proc.returncode, 0, proc.stdout)


    # ---- version 2 ----

    # The schemas are DM-01 to DM-03 as the spec writes them.
    def test_schemas_equal_the_spec_blocks(self):
        text = (ROOT / "docs/specs/spec/SPEC-012.md").read_text(encoding="utf-8")
        blocks = re.findall(r"```json\n(.*?)```", text, re.S)
        for block, name in zip(blocks, ("manifest", "events", "progress")):
            with self.subTest(name):
                self.assertEqual(json.loads((SCHEMAS / (name + ".schema.json")).read_text(encoding="utf-8")),
                                 json.loads(block))

    # VER-22: a Bash command naming a read rule's path is read evidence.
    def test_ver22_bash_reads(self):
        state, _, _, _ = self.run_case("bash-reads")
        s1 = self.step(state, 1)
        self.assertEqual(s1["state"], "done")
        self.assertEqual([(e["type"], e["strength"], e["detail"]) for e in s1["evidence"]],
                         [("read", "medium", "Bash docs/specs/brainstorm/*.md")])
        self.assertEqual(self.flags(state, 1), [])
        for name in ("bash-reads-failed", "bash-reads-error"):
            with self.subTest(name):
                state, _, _, _ = self.run_case(name)
                self.assertEqual(self.step(state, 1)["evidence"], [])
                self.assertEqual([f["gate"] for f in self.flags(state, 1, "skipped")], ["write"])
        state, _, _, _ = self.run_case("bash-reads-forms")
        self.assertEqual([e["seq"] for e in self.step(state, 1)["evidence"]], [2, 3, 4])
        arch, _, _, _ = self.run_case("arch-bash-reads")
        for n in (2, 3):
            self.assertIn("Bash docs/specs/prd/PRD-001.md", [e["detail"] for e in self.step(arch, n)["evidence"]])
        s10 = self.step(arch, 10)
        self.assertEqual([e["detail"] for e in s10["evidence"]], ["Bash docs/specs/arch/ARCH-001.md"])
        self.assertEqual(s10["state"], "done")

    # VER-22: with --root, a token under the root counts; without it, an absolute token matches nothing.
    def test_ver22_bash_reads_under_an_absolute_root(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "proj"
            root.mkdir()
            log = mc.Log("brainstorm").bash("cat %s/docs/specs/brainstorm/BRN-001.md" % root)
            events = Path(tmp) / "events.jsonl"
            events.write_text("\n".join(log.lines()) + "\n", encoding="utf-8")
            out = Path(tmp) / "state.json"
            base = ["evaluate", "--manifests", mc.PLUGIN_MANIFESTS, "--events", events, "--out", out]
            proc = self.run_cli(*base, "--root", root)
            self.assertEqual(proc.returncode, 0, proc.stderr)
            self.assertEqual([e["detail"] for e in self.step(json.loads(out.read_text()), 1)["evidence"]],
                             ["Bash docs/specs/brainstorm/BRN-001.md"])
            proc = self.run_cli(*base)
            self.assertEqual(proc.returncode, 0, proc.stderr)
            self.assertEqual(self.step(json.loads(out.read_text()), 1)["evidence"], [])

    # VER-23: exclude, and architecture's step 5.
    def test_ver23_exclude_and_step_5(self):
        state, _, _, _ = self.run_case("arch-inspect")
        self.assertEqual([e["detail"] for e in self.step(state, 5)["evidence"]],
                         ["Grep .", "Read src/booking/service.py"])
        manifest = json.loads((PROGRESS / "manifests/architecture.json").read_text(encoding="utf-8"))
        self.assertEqual(manifest["steps"]["5"]["evidence"],
                         [{"type": "read", "pattern": "*", "exclude": ["docs/specs/", ".claude/", "devforgeai/"]}])
        validator = schema_validator("manifest")
        self.assertEqual([e.message for e in validator.iter_errors(manifest)], [])
        bad = json.loads(json.dumps(manifest))
        bad["steps"]["9"]["evidence"][0]["exclude"] = ["x/"]
        self.assertNotEqual(list(validator.iter_errors(bad)), [])

    # VER-24: the flag messages name the evidence expected.
    def test_ver24_flag_messages(self):
        state, _, _, _ = self.run_case("bash-reads-failed")
        self.assertEqual([f["message"] for f in self.flags(state, 1, "skipped")], [
            "step 1 (Intake: topic, existing BRNs, clarifying questions) has no evidence or tick before the "
            "write gate: expected a read of docs/specs/brainstorm/, or a tick in the reply text"])
        state, _, _, _ = self.run_case("no-rule-step")
        self.assertEqual([f["message"] for f in state["flags"]], [
            "step 2 (Decide) has no evidence or tick before the write gate: expected a tick in the reply text",
            "step 3 (Inspect) has no evidence or tick before the write gate: expected a read of * except "
            "notes/, out/, or a tick in the reply text",
            "step 4 (Check) has no evidence or tick before the write gate: expected a successful run of check.sh"])
        state, _, _, _ = self.run_case("brn-validation-claimed")
        self.assertEqual([f["message"] for f in self.flags(state, 7, "claimed-not-evidenced")], [
            "step 7 (Validate the BRN) is ticked, but a successful run of validate_brn.py on a written file "
            "wasn't seen"])


    # ---- version 3 ----

    # VER-26: work on earlier steps after the user's answer doesn't lose it.
    def test_ver26_answers_survive_later_work_on_earlier_steps(self):
        for name, owned in (("answer-then-listing", 5), ("answer-then-reticks", 5),
                            ("arch-answer-then-listing", 8), ("arch-answer-then-inspection", 8)):
            with self.subTest(name):
                state, _, _, _ = self.run_case(name)
                self.assertEqual(state["flags"], [])
                self.assertFalse(state["gate"]["refuse"])
                s = self.step(state, owned)
                self.assertEqual(s["state"], "done")
                self.assertIn("answer", [e["type"] for e in s["evidence"]])
        early, _, _, _ = self.run_case("brn-answer-early")
        self.assertEqual(sorted((f["step"], f["type"]) for f in early["flags"]), [(5, "skipped"), (6, "rule-broken")])

    # VER-27: ./ tool paths are read like the rest.
    def test_ver27_dot_paths(self):
        state, _, _, _ = self.run_case("arch-dot-paths")
        self.assertEqual([e["detail"] for e in self.step(state, 2)["evidence"]],
                         ["Glob docs/specs/prd/PRD-*.md", "Read docs/specs/prd/PRD-001.md"])
        self.assertEqual([e["detail"] for e in self.step(state, 3)["evidence"]],
                         ["Glob docs/specs/prd/PRD-*.md", "Read docs/specs/prd/PRD-001.md"])
        self.assertEqual(self.step(state, 5)["evidence"], [])


    # ---- version 4 ----

    # VER-28: an earlier step ticked only after the answer still moves the window; the re-tick limit is pinned.
    def test_ver28_a_step_finished_after_the_answer_moves_the_window(self):
        state, _, _, _ = self.run_case("intake-then-tick")
        self.assertEqual(sorted((f["step"], f["type"]) for f in state["flags"]), [(5, "skipped"), (6, "rule-broken")])
        self.assertTrue(state["gate"]["refuse"])
        limit, _, _, _ = self.run_case("arch-retick-after-answer")
        # The limit §13 names: step 7's answer goes to step 8. Pinned so a later BEH-09 change shows here.
        self.assertEqual(sorted((f["step"], f["type"]) for f in limit["flags"]), [(7, "skipped"), (9, "rule-broken")])
        self.assertEqual(self.step(limit, 8)["state"], "done")

    # VER-29: a Write's ./ path reaches the write gate.
    def test_ver29_a_dot_write_reaches_the_gate(self):
        cut, _, _, _ = self.run_case("brn-unconfirmed-cut")
        for name in ("write-dot-path", "write-double-slash"):
            with self.subTest(name):
                state, _, _, _ = self.run_case(name)
                self.assertEqual([(f["step"], f["type"]) for f in state["flags"]],
                                 [(f["step"], f["type"]) for f in cut["flags"]])
                self.assertEqual((state["gate"]["kind"], state["gate"]["refuse"]), ("write", True))

    # ---- versions 5 and 6 ----

    @staticmethod
    def events_of(name, kind=None):
        lines = (mc.CASES / name / "events.jsonl").read_text(encoding="utf-8").splitlines()
        return [e for e in map(json.loads, lines) if kind is None or e["kind"] == kind]

    def answer_seqs(self, step):
        return [e["seq"] for e in step["evidence"] if e["type"] == "answer"]

    # VER-30: step events place a brainstorm's answers: the intake answer is step 1's own, the confirmation step 5's.
    def test_ver30_steps_brainstorm(self):
        state, _, _, _ = self.run_case("steps-brainstorm")
        intake, confirmation = [e["seq"] for e in self.events_of("steps-brainstorm", "answer")]
        self.assertEqual(state["flags"], [])
        self.assertEqual((state["gate"]["kind"], state["gate"]["refuse"]), ("write", False))
        s5 = self.step(state, 5)
        self.assertEqual(s5["state"], "done")
        self.assertEqual([(e["seq"], e["strength"]) for e in s5["evidence"]], [(confirmation, "strong")])
        self.assertNotIn(intake, [e["seq"] for s in state["steps"] for e in s["evidence"]])
        self.assertEqual(state["counts"]["stepEvents"], len(self.events_of("steps-brainstorm", "step")))
        self.assertEqual(state["counts"]["unmarkedQuestions"], 0)

    # VER-31: with step events, step 7 keeps its two answers and step 8 its typed prompt, re-ticks or not.
    def test_ver31_steps_arch(self):
        state, _, _, _ = self.run_case("steps-arch")
        answers = [e["seq"] for e in self.events_of("steps-arch", "answer")]
        prompt = [e["seq"] for e in self.events_of("steps-arch", "prompt")]
        self.assertEqual(state["flags"], [])
        self.assertEqual((state["gate"]["kind"], state["gate"]["refuse"]), ("write", False))
        s7, s8 = self.step(state, 7), self.step(state, 8)
        self.assertEqual((s7["state"], self.answer_seqs(s7)), ("done", answers))
        self.assertEqual((s8["state"], self.answer_seqs(s8)), ("done", prompt))
        self.assertEqual([e["detail"] for e in s8["evidence"]], ["prompt"])

    # VER-32: a question asked while no step is in progress is a question gate; a prompt there raises nothing.
    def test_ver32_unmarked_question(self):
        message = ("a question was asked while no step was marked in progress in the task list: "
                   "mark the step it belongs to in progress, then ask")
        cut, _, _, _ = self.run_case("steps-unmarked-question-cut")
        seq = self.events_of("steps-unmarked-question-cut", "answer")[0]["seq"]
        self.assertEqual(cut["flags"], [{"gate": "question", "seq": seq, "step": 7, "type": "unmarked-question",
                                         "message": message}])
        self.assertEqual(cut["gate"], {"kind": "question", "seq": seq, "refuse": True, "reason": message})
        self.assertNotIn(seq, [e["seq"] for s in cut["steps"] for e in s["evidence"]])
        self.assertEqual(cut["counts"]["unmarkedQuestions"], 1)
        self.assertEqual(cut["counts"]["stepEvents"], len(self.events_of("steps-unmarked-question-cut", "step")))
        full, _, _, _ = self.run_case("steps-unmarked-question")
        self.assertEqual(sorted((f["step"], f["type"]) for f in full["flags"]),
                         [(7, "unmarked-question"), (8, "skipped"), (9, "rule-broken")])
        self.assertEqual((full["gate"]["kind"], full["gate"]["refuse"]), ("write", True))
        prompt, _, _, _ = self.run_case("steps-unmarked-prompt")
        self.assertEqual(prompt["flags"], [])
        self.assertEqual(prompt["gate"], {"kind": None, "seq": None, "refuse": False, "reason": None})
        self.assertEqual(prompt["counts"]["unmarkedQuestions"], 0)
        self.assertNotIn(self.events_of("steps-unmarked-prompt", "prompt")[0]["seq"],
                         [e["seq"] for s in prompt["steps"] for e in s["evidence"]])

    # VER-33: current follows step events; a conditional step done with no evidence doesn't apply; step 40 is unknown.
    def test_ver33_current_and_step_events(self):
        state, _, _, _ = self.run_case("steps-current")
        answer = self.events_of("steps-current", "answer")[0]["seq"]
        manifest = json.loads((PROGRESS / "manifests/architecture.json").read_text(encoding="utf-8"))
        self.assertEqual(state["current"], 8)
        self.assertEqual(self.answer_seqs(self.step(state, 8)), [answer])
        self.assertEqual(self.answer_seqs(self.step(state, 7)), [])
        s5 = self.step(state, 5)
        self.assertEqual((s5["state"], s5["note"]), ("not-applicable", manifest["steps"]["5"]["when"]))
        self.assertEqual(state["counts"]["unknownClaims"], 1)
        # counts.stepEvents counts the step events naming a step the checklist has: step 40's is unknownClaims'.
        self.assertEqual(state["counts"]["stepEvents"], len(self.events_of("steps-current", "step")) - 1)
        self.assertEqual(state["flags"], [])
        retick, _, _, _ = self.run_case("steps-retick")
        self.assertEqual((self.step(retick, 5)["state"], self.step(retick, 5)["note"]),
                         ("not-applicable", manifest["steps"]["5"]["when"]))

    # VER-34 and SPEC-013 VER-24: without the tag, or without a task list, nothing changes and nothing is refused;
    # step events Claude kept unasked still place answers, and an answer with no step in progress goes to the windows.
    def test_ver34_rollout(self):
        base, _, _, _ = self.run_case("arch-outcome-confirmed")
        for name in ("rollout-untagged", "tasklist-false-tagged"):
            with self.subTest(name):
                state, _, _, _ = self.run_case(name)
                self.assertEqual(state, base)
        state, _, _, _ = self.run_case("rollout-unasked-steps")
        first, second = [e["seq"] for e in self.events_of("rollout-unasked-steps", "answer")]
        self.assertEqual(state["flags"], [])
        self.assertEqual((state["gate"]["kind"], state["gate"]["refuse"]), ("write", False))
        self.assertEqual(self.answer_seqs(self.step(state, 7)), [first])
        self.assertEqual(self.answer_seqs(self.step(state, 8)), [second])
        self.assertEqual(state["counts"]["unmarkedQuestions"], 0)


class SpecRulesUnderS(SpecRules):
    """Every SpecRules test with the evaluator under python3 -S (VER-18, QR-01)."""
    INTERPRETER = (sys.executable, "-S", "-B")


class Goldens(Base):
    """Each case's output equals its reviewed expected.json, byte for byte."""

    def test_outputs_match_expected(self):
        for name in mc.CASE_BUILDERS:
            with self.subTest(name):
                expected = mc.CASES / name / "expected.json"
                self.assertTrue(expected.exists(), "no expected.json: run make_cases.py --write-expected")
                _, _, raw, _ = self.run_case(name)
                self.assertEqual(raw, expected.read_bytes())


if __name__ == "__main__":
    unittest.main()
