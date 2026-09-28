"""Focused regression tests for Architecture native grading evidence."""

from __future__ import annotations

import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

TESTS = Path(__file__).resolve().parent
sys.path.insert(0, str(TESTS))

import grade_architecture_eval as grader  # noqa: E402
import summarize_architecture_eval as summarizer  # noqa: E402


PACKAGE = TESTS.parent
EVALS = PACKAGE / "evals/architecture"
RUNTIME_MODEL = "gpt-6-astra"
RUNTIME_SESSION = "12345678-1234-4234-9234-123456789abc"


def write_json(path, value):
    path.write_text(json.dumps(value, indent=2) + "\n")


def item_event(item):
    return {"method": "item/completed", "params": {"item": item}}


def load_event():
    return item_event({
        "id": "load-1",
        "type": "commandExecution",
        "exitCode": 0,
        "command": "sed -n '1,80p' /candidate/skills/architecture/SKILL.md",
        "commandActions": [
            {"type": "read", "path": "/candidate/skills/architecture/SKILL.md"}
        ],
        "aggregatedOutput": "---\nname: architecture\n---\n",
    })


class ArchitectureGradeRegressionTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.evidence = Path(self.temp.name)
        (self.evidence / "matrix").mkdir()
        (self.evidence / "definitions").mkdir()

    def tearDown(self):
        self.temp.cleanup()

    def install_definitions(self, case):
        target = self.evidence / "definitions" / case / "graders"
        if not target.exists():
            shutil.copytree(EVALS / case / "graders", target)

    def make_trial(self, case, *, arm="plugin", repeat=1, status="completed",
                   messages=(), before=None, after=None, model=RUNTIME_MODEL,
                   session=RUNTIME_SESSION, install_definitions=True):
        if install_definitions:
            self.install_definitions(case)
        else:
            (self.evidence / "definitions" / case / "graders").mkdir(parents=True)
        trial = self.evidence / "matrix" / f"{case}--{arm}--{repeat}"
        workspace = trial / "workspace"
        workspace.mkdir(parents=True)
        write_json(trial / "result.json", {
            "case": case,
            "verification": "VER-TEST",
            "arm": arm,
            "repeat": repeat,
            "status": status,
            "model": model,
            "threadId": session,
            "collaboration_mode": "plan" if case == "existing-arch-not-duplicated" else "default",
        })
        base = {"docs/specs/prd/PRD-001.md": "prd-original"}
        write_json(trial / "before.json", base if before is None else before)
        write_json(trial / "after.json", base if after is None else after)
        git_state = {"index": "index-1", "head": "head-1", "refs": "refs-1"}
        write_json(trial / "git-before.json", git_state)
        write_json(trial / "git-after.json", git_state)
        if arm == "plugin":
            write_json(trial / "runtime-candidate-check.json", {"unchanged": True})
        protocol = "".join(json.dumps({"message": message}) + "\n" for message in messages)
        (trial / "protocol.jsonl").write_text(protocol)
        return trial

    @staticmethod
    def grade_row(result, name):
        return next(row for row in result["source_grades"] if row["grader"] == name)

    def test_activation_requires_observed_skill_read_not_catalog_presence(self):
        catalog = {
            "method": "skills/list",
            "result": {"skills": [{
                "name": "devforgeai:architecture",
                "path": "/candidate/skills/architecture/SKILL.md",
            }]},
        }
        catalog_only = grader.grade(self.make_trial("creates-arch", messages=[catalog]))
        self.assertFalse(self.grade_row(catalog_only, "skill-fired")["passed"])
        self.assertFalse(catalog_only["activation"]["observed"])
        self.assertFalse(catalog_only["supplemental_guards"]["activation_matches_case"])

        loaded = grader.grade(self.make_trial("creates-arch", repeat=2, messages=[catalog, load_event()]))
        self.assertTrue(self.grade_row(loaded, "skill-fired")["passed"])
        self.assertTrue(loaded["activation"]["observed"])
        self.assertTrue(loaded["supplemental_guards"]["activation_matches_case"])

    def test_native_question_event_is_distinct_from_plain_text_question(self):
        final_question = item_event({
            "id": "answer-1", "type": "agentMessage", "phase": "final_answer",
            "text": "ARCH-001 already exists. Reuse or amend it?",
        })
        plain = self.make_trial(
            "existing-arch-not-duplicated", messages=[load_event(), final_question])
        (plain / "workspace/docs/specs/arch").mkdir(parents=True)
        (plain / "workspace/docs/specs/arch/ARCH-001.md").write_text("existing\n")
        write_json(plain / "before.json", {
            "docs/specs/prd/PRD-001.md": "prd-original",
            "docs/specs/arch/ARCH-001.md": "arch-original",
        })
        write_json(plain / "after.json", {
            "docs/specs/prd/PRD-001.md": "prd-original",
            "docs/specs/arch/ARCH-001.md": "arch-original",
        })
        plain_result = grader.grade(plain)
        self.assertFalse(self.grade_row(plain_result, "asks-with-request-user-input")["passed"])
        self.assertEqual(plain_result["native_question_count"], 0)
        self.assertFalse(plain_result["supplemental_guards"]["choice_uses_native_question"])

        request = {
            "method": "item/tool/requestUserInput",
            "params": {"questions": [{
                "id": "architecture_selection",
                "header": "Architecture",
                "question": "Should I reuse ARCH-001 or amend it?",
                "options": [
                    {"label": "Reuse", "description": "Keep the current baseline."},
                    {"label": "Amend", "description": "Add new questions or components."},
                ],
            }]},
        }
        native = self.make_trial(
            "existing-arch-not-duplicated", repeat=2, status="awaiting_input",
            messages=[load_event(), request])
        (native / "workspace/docs/specs/arch").mkdir(parents=True)
        (native / "workspace/docs/specs/arch/ARCH-001.md").write_text("existing\n")
        unchanged = {
            "docs/specs/prd/PRD-001.md": "prd-original",
            "docs/specs/arch/ARCH-001.md": "arch-original",
        }
        write_json(native / "before.json", unchanged)
        write_json(native / "after.json", unchanged)
        native_result = grader.grade(native)
        self.assertTrue(self.grade_row(native_result, "asks-with-request-user-input")["passed"])
        self.assertEqual(native_result["native_question_count"], 1)
        self.assertTrue(native_result["supplemental_guards"]["choice_uses_native_question"])
        self.assertIn("reuse ARCH-001 or amend", (native / "reply.txt").read_text())

    def test_unknown_or_stale_generated_by_identity_cannot_strict_pass(self):
        variants = [
            ("unknown-runtime", "unknown", RUNTIME_SESSION, "unknown", RUNTIME_SESSION,
             "runtime_model_known"),
            ("stale-record", "old-model", "aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaaa",
             RUNTIME_MODEL, RUNTIME_SESSION, "provenance_model_matches_runtime"),
        ]
        for repeat, (label, recorded_model, recorded_session, runtime_model, runtime_session,
                     failed_guard) in enumerate(variants, 1):
            with self.subTest(label=label):
                before = {"docs/specs/prd/PRD-001.md": "prd-original"}
                after = dict(before, **{"docs/specs/arch/ARCH-001.md": "arch-new"})
                trial = self.make_trial(
                    "records-provenance", repeat=repeat, messages=[load_event()],
                    before=before, after=after, model=runtime_model, session=runtime_session)
                arch = trial / "workspace/docs/specs/arch/ARCH-001.md"
                arch.parent.mkdir(parents=True)
                arch.write_text(
                    "---\n"
                    "generated_by:\n"
                    "  tool: \"codex\"\n"
                    f"  model: \"{recorded_model}\"\n"
                    f"  session: \"{recorded_session}\"\n"
                    "reviewed_by: []\n"
                    "---\n# ARCH-001\n"
                )
                result = grader.grade(trial)
                self.assertFalse(result["supplemental_guards"][failed_guard])
                if label == "stale-record":
                    self.assertFalse(result["supplemental_guards"]["provenance_session_matches_runtime"])
                self.assertFalse(result["strict_pass"])

    def test_malformed_authored_frontmatter_fails_provenance_without_aborting(self):
        before = {"docs/specs/prd/PRD-001.md": "prd-original"}
        after = dict(before, **{"docs/specs/arch/ARCH-001.md": "arch-new"})
        trial = self.make_trial(
            "records-provenance", messages=[load_event()], before=before, after=after)
        arch = trial / "workspace/docs/specs/arch/ARCH-001.md"
        arch.parent.mkdir(parents=True)
        arch.write_text("---\ngenerated_by: [unterminated\n---\n# ARCH-001\n")

        result = grader.grade(trial)

        self.assertEqual(result["provenance"].get("recorded"), {})
        self.assertFalse(result["supplemental_guards"]["provenance_tool_is_codex"])
        self.assertFalse(result["supplemental_guards"]["provenance_model_matches_runtime"])
        self.assertFalse(result["supplemental_guards"]["provenance_session_matches_runtime"])
        self.assertFalse(result["strict_pass"])

    def test_prd_byte_mutation_is_rejected(self):
        before = {"docs/specs/prd/PRD-001.md": "prd-original"}
        after = {
            "docs/specs/prd/PRD-001.md": "prd-mutated",
            "docs/specs/arch/ARCH-001.md": "arch-new",
        }
        trial = self.make_trial(
            "creates-arch", messages=[load_event()], before=before, after=after)
        arch = trial / "workspace/docs/specs/arch/ARCH-001.md"
        arch.parent.mkdir(parents=True)
        arch.write_text("---\ngenerated_by: {tool: codex, model: gpt-6-astra, session: "
                        f"{RUNTIME_SESSION}}}\n---\n# ARCH-001\n")
        result = grader.grade(trial)
        self.assertFalse(result["supplemental_guards"]["preexisting_prds_preserved"])
        self.assertFalse(result["supplemental_guards"]["only_architecture_artifacts_changed"])
        self.assertIn("docs/specs/prd/PRD-001.md", result["changed_paths"])
        self.assertFalse(result["strict_pass"])

    def test_semantic_rubric_stays_pending_without_independent_assessment(self):
        result = grader.grade(self.make_trial(
            "superseded-adr", messages=[load_event()]))
        row = self.grade_row(result, "readiness-mapping")
        self.assertEqual(row["status"], "REVIEW_REQUIRED")
        self.assertIsNone(row["passed"])
        self.assertIsNone(result["source_score"])
        self.assertFalse(result["threshold_pass"])
        self.assertFalse(result["strict_pass"])

    def test_zero_scored_graders_fails_closed(self):
        result = grader.grade(self.make_trial(
            "empty-case", arm="baseline", install_definitions=False))
        self.assertEqual(result["source_grades"], [])
        self.assertIsNone(result["source_score"])
        self.assertFalse(result["threshold_pass"])
        self.assertFalse(result["strict_pass"])

    def test_summary_retains_failed_rows_and_refuses_an_incomplete_denominator(self):
        trials, grades = [], []
        for case, verification in summarizer.CASE_VER.items():
            for arm in ("plugin", "baseline"):
                for repeat in range(1, 4):
                    trials.append({"case": case, "arm": arm, "repeat": repeat})
                    grades.append({
                        "case": case,
                        "verification": verification,
                        "arm": arm,
                        "repeat": repeat,
                        "status": "completed",
                        "source_score": 1.0,
                        "threshold_pass": True,
                        "strict_pass": True,
                        "activation": {"expected": arm == "plugin", "observed": arm == "plugin"},
                    })
        self.assertEqual(len(trials), 84)
        grades[17]["status"] = "error"
        grades[17]["strict_pass"] = False
        write_json(self.evidence / "matrix-plan.json", {
            "candidate_sha256": "candidate",
            "definitions_sha256": "definitions",
            "codex_version": "codex-test",
            "trials": trials,
        })
        write_json(self.evidence / "matrix-grades.json", grades)
        summary = summarizer.build_summary(self.evidence)
        self.assertEqual(summary["total_trials"], 84)
        self.assertEqual(len(summary["run_errors"]), 1)
        self.assertEqual(summary["run_errors"][0]["status"], "error")

        write_json(self.evidence / "matrix-grades.json", grades[:-1])
        with self.assertRaisesRegex(SystemExit, "Incomplete matrix: 83/84"):
            summarizer.build_summary(self.evidence)


if __name__ == "__main__":
    unittest.main()
