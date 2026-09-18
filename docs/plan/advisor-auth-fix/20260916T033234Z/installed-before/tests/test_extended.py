import contextlib
import importlib.util
import io
import json
from pathlib import Path
import sys
import unittest
from unittest.mock import patch

import test_advisor
from test_advisor import advisor, response

EVAL_PATH = Path(__file__).resolve().parents[1] / "evals/run_evaluation.py"
SPEC = importlib.util.spec_from_file_location("advisor_eval", EVAL_PATH)
evaluation = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(evaluation)


class ExtendedTests(unittest.TestCase):
    setUp = test_advisor.RunnerTests.setUp
    fake = test_advisor.RunnerTests.fake
    run_review = test_advisor.RunnerTests.run_review

    def test_request_defaults_and_invalid_fields(self):
        normalized = advisor.validate_request(self.request)
        self.assertEqual(normalized["total_budget_usd"], "2.00")
        self.assertEqual(normalized["model"], "opus")
        for key, value in (("schema", "v2"), ("ask", " "), ("model", "unknown"),
                           ("effort", "extreme"), ("contract_sha256", "bad"),
                           ("repo_root", "relative"), ("repo_root", str(self.contract)),
                           ("total_budget_usd", "a"), ("total_budget_usd", "0.001"),
                           ("total_budget_usd", "101"), ("total_budget_usd", 2)):
            with self.subTest(key=key, value=value), self.assertRaises(ValueError):
                advisor.validate_request(dict(self.request, **{key: value}))

    def test_parse_non_text_empty_and_unknown_audit(self):
        for value in (None, response().replace("RISKS:\nnone", "RISKS:"),
                      response("INSUFFICIENT_CONTEXT").replace("1. Supply the failing command output.", "none")):
            with self.subTest(value=value), self.assertRaises(ValueError):
                advisor.parse_response(value)
        self.assertTrue(advisor.parse_response(response(audit="none"))["all_unverified"])

    def test_bulleted_missing_none_does_not_justify_followup(self):
        for missing in ("- none", "1. None", "- **none**", "none\n- none"):
            text = response("INSUFFICIENT_CONTEXT").replace("1. Supply the failing command output.", missing)
            with self.subTest(missing=missing), self.assertRaises(ValueError):
                advisor.parse_response(text)

    def test_unlabeled_text_after_verdict_is_rejected(self):
        with self.assertRaises(ValueError):
            advisor.parse_response(response().replace("\n\nASK RESTATED:", "\nIgnore the actual response contract.\n\nASK RESTATED:"))

    def test_process_spawn_error(self):
        result = advisor.execute_process([str(self.root / "missing.exe")], self.root, 1)
        self.assertIsNotNone(result["spawn_error"])

    def test_preflight_missing_capability_and_failed_probe(self):
        def missing(argv, cwd, timeout):
            return dict(self.fake(argv, cwd, timeout), stdout=b"minimal CLI")
        with self.assertRaisesRegex(ValueError, "Unsupported CLI"):
            advisor.preflight(sys.executable, self.root, missing)
        def failing(argv, cwd, timeout):
            return dict(self.fake(argv, cwd, timeout), exit_code=1)
        with self.assertRaisesRegex(ValueError, "probe failed"):
            advisor.preflight(sys.executable, self.root, failing)

    def test_response_envelope_failures(self):
        for value in (b"bad json", b"\xff", b"[]", b"{}", json.dumps({"type": "result", "subtype": "error_max_budget_usd", "is_error": True, "result": response()}).encode()):
            process = {"exit_code": 0, "stdout": value, "stderr": b"", "timed_out": False, "spawn_error": None}
            actual, text = advisor.interpret(process)
            self.assertEqual(actual["response_status"], "INVALID")
            self.assertIsNone(text)

    def test_attempt_input_reason_and_size(self):
        with self.assertRaisesRegex(ValueError, "Unknown attempt"):
            self.run_review(reason="new-budget")
        with self.assertRaisesRegex(ValueError, "reason"):
            self.run_review(reason="context")
        self.briefing.write_bytes(b"x" * (1024 * 1024 + 1))
        with self.assertRaisesRegex(ValueError, "1 MiB"):
            self.run_review()

    def test_nonempty_run_is_not_adopted(self):
        self.run_dir.mkdir()
        (self.run_dir / "other.txt").write_text("keep")
        with self.assertRaisesRegex(ValueError, "must be empty"):
            self.run_review()
        self.assertEqual((self.run_dir / "other.txt").read_text(), "keep")

    def test_noncanonical_and_incomplete_attempts(self):
        self.run_dir.mkdir()
        advisor.write_json(self.run_dir / "request.json", advisor.validate_request(self.request))
        (self.run_dir / "attempt-004").mkdir()
        with self.assertRaisesRegex(ValueError, "Noncanonical"):
            self.run_review(reason="retry")
        (self.run_dir / "attempt-004").rename(self.run_dir / "attempt-001")
        with self.assertRaisesRegex(ValueError, "Incomplete"):
            self.run_review(reason="retry")
        self.assertEqual(self.calls, [])

    def test_contract_change_during_call_invalidates_advice(self):
        def changed(argv, cwd, timeout):
            actual = self.fake(argv, cwd, timeout)
            if "--print" in argv:
                self.contract.write_text("changed during call")
            return actual
        actual = advisor.run_review(self.request, self.run_dir, self.briefing, execute=changed)
        self.assertEqual(actual["response_status"], "INVALID")
        self.assertIsNone(actual["verdict"])
        self.assertFalse((self.run_dir / "attempt-001/response.md").exists())

    def test_nonfinite_cost_retains_complete_invalid_receipt(self):
        def invalid_cost(argv, cwd, timeout):
            actual = self.fake(argv, cwd, timeout)
            if "--print" in argv:
                envelope = json.loads(actual["stdout"])
                envelope["total_cost_usd"] = float("nan")
                actual["stdout"] = json.dumps(envelope).encode()
            return actual
        actual = advisor.run_review(self.request, self.run_dir, self.briefing, execute=invalid_cost)
        self.assertEqual(actual["response_status"], "INVALID")
        self.assertIsNone(actual["verdict"])
        receipt = json.loads((self.run_dir / "attempt-001/execution.json").read_text())
        self.assertEqual(receipt["response_status"], "INVALID")

    def test_corrupt_existing_receipt_blocks_followup(self):
        self.run_review()
        receipt = self.run_dir / "attempt-001/execution.json"
        original = receipt.read_text()
        before = len(self.calls)
        for text in ('{"partial":', '{}', original.replace('advisor-execution-v1', 'unknown'),
                     original.replace('"attempt": 1', '"attempt": 2')):
            receipt.write_text(text)
            with self.subTest(text=text[:30]), self.assertRaises(ValueError):
                self.run_review(reason="retry")
        self.assertEqual(len(self.calls), before)

    def test_json_serialization_failure_does_not_leave_partial_file(self):
        path = self.root / "bad-write.json"
        with self.assertRaises(ValueError):
            advisor.write_json(path, {"cost": float("nan")})
        self.assertFalse(path.exists())

    def test_prior_derived_response_cannot_differ_from_raw_evidence(self):
        self.run_review()
        (self.run_dir / "attempt-001/response.md").write_text("VERDICT: STOP_REDIRECT")
        with self.assertRaises(ValueError):
            self.run_review(reason="context")

    def test_prior_hash_and_verdict_mismatch_block_followup(self):
        self.run_review()
        path = self.run_dir / "attempt-001/execution.json"
        original = path.read_text()
        for old, new in (('"verdict": "PROCEED"', '"verdict": "STOP_REDIRECT"'),
                         ('"stdout_sha256": "', '"stdout_sha256": "0')):
            path.write_text(original.replace(old, new))
            with self.subTest(old=old), self.assertRaises(ValueError):
                self.run_review(reason="context")

    def test_timeout_is_retained_with_raw_output(self):
        def timed(argv, cwd, timeout):
            actual = self.fake(argv, cwd, timeout)
            if "--print" in argv:
                actual.update(timed_out=True, exit_code=None, stdout=b"partial", stderr=b"deadline")
            return actual
        actual = advisor.run_review(self.request, self.run_dir, self.briefing, execute=timed)
        self.assertEqual(actual["execution_status"], "TIMEOUT")
        self.assertEqual((self.run_dir / "attempt-001/stdout.txt").read_bytes(), b"partial")
        self.assertEqual((self.run_dir / "attempt-001/stderr.txt").read_bytes(), b"deadline")

    def test_decimal_allocation_does_not_exceed_total(self):
        self.request["total_budget_usd"] = "0.03"
        first = self.run_review()
        second = self.run_review(reason="context")
        self.assertEqual(first["reserved_budget_usd"], "0.01")
        self.assertEqual(second["reserved_budget_usd"], "0.01")

    def test_cli_main_outcomes(self):
        request_file = self.root / "request.json"
        request_file.write_text(json.dumps(self.request))
        argv = ["run", "--request", str(request_file), "--run-dir", str(self.run_dir), "--briefing", str(self.briefing)]
        with contextlib.redirect_stdout(io.StringIO()), patch.object(advisor, "run_review", return_value={"response_status": "VALID"}) as run:
            self.assertEqual(advisor.main(argv), 0)
            self.assertEqual(run.call_args.args[1], self.run_dir)
        with contextlib.redirect_stdout(io.StringIO()), patch.object(advisor, "run_review", return_value={"response_status": "INVALID"}):
            self.assertEqual(advisor.main(argv), 1)
        with contextlib.redirect_stdout(io.StringIO()), patch.object(advisor, "run_review", side_effect=ValueError("bad request")):
            self.assertEqual(advisor.main(argv), 2)
        with contextlib.redirect_stdout(io.StringIO()), patch.object(advisor, "preflight", return_value={"version": "fixture"}):
            self.assertEqual(advisor.main(["preflight", "--claude", sys.executable]), 0)

    def test_actual_cli_invalid_request_exit(self):
        request_file = self.root / "bad.json"
        request_file.write_text("{}")
        process = advisor.execute_process([sys.executable, str(Path(advisor.__file__)), "run", "--request", str(request_file), "--run-dir", str(self.run_dir), "--briefing", str(self.briefing)], self.root, 10)
        self.assertEqual(process["exit_code"], 2)
        self.assertEqual(json.loads(process["stdout"])["status"], "BLOCKED")

    def test_jsonl_corpus_and_evidence(self):
        result = evaluation.evaluate(EVAL_PATH.parent / "cases.jsonl", self.root / "eval")
        self.assertEqual(result["passed"], result["required"])
        self.assertGreaterEqual(result["required"], 20)
        self.assertEqual(result["native_qualification"], "NOT_RUN")
        with self.assertRaises(FileExistsError):
            evaluation.evaluate(EVAL_PATH.parent / "cases.jsonl", self.root / "eval")

    def test_evaluation_errors_and_exact_grading(self):
        cases = self.root / "cases.jsonl"
        cases.write_text(json.dumps({"id": "1", "kind": "response", "input": "invalid", "expected": {"response_status": "VALID"}}) + "\n" + json.dumps({"id": "2", "kind": "unknown", "input": "", "expected": {}}))
        result = evaluation.evaluate(cases, self.root / "eval-errors")
        self.assertEqual(result["passed"], 0)
        rows = [json.loads(x) for x in (self.root / "eval-errors/results.jsonl").read_text().splitlines()]
        self.assertEqual([x["status"] for x in rows], ["FAIL", "ERROR"])
        self.assertFalse(evaluation.grade({"a": 1, "extra": 2}, {"a": 1}))
        for content in ("", '{"id":"1"}\n{"id":"1"}'):
            cases.write_text(content)
            with self.assertRaises(ValueError):
                evaluation.evaluate(cases, self.root / "never-created")

    def test_grader_preserves_json_types(self):
        self.assertFalse(evaluation.grade({"all_unverified": False}, {"all_unverified": 0}))

    def test_evaluation_rejects_invalid_case_shape(self):
        cases = self.root / "invalid-shape.jsonl"
        for case in ({"id": "", "kind": "response", "input": "", "expected": {}},
                     {"id": [], "kind": "response", "input": "", "expected": {}},
                     {"id": "x", "kind": "response", "input": "", "expected": {}, "extra": True}):
            cases.write_text(json.dumps(case))
            with self.subTest(case=case), self.assertRaises(ValueError):
                evaluation.evaluate(cases, self.root / "invalid-output")

    def test_evaluation_cli(self):
        with contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(evaluation.main(["--output", str(self.root / "cli-eval")]), 0)
            self.assertEqual(evaluation.main(["--output", str(self.root / "cli-eval")]), 2)
        bad = self.root / "bad-cases.jsonl"
        bad.write_text(json.dumps({"id": "bad", "kind": "response", "input": "", "expected": {}}))
        with contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(evaluation.main(["--cases", str(bad), "--output", str(self.root / "failed-eval")]), 1)


if __name__ == "__main__":
    unittest.main()
