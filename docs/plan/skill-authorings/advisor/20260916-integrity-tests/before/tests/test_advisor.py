import importlib.util
import unittest
import hashlib
import json
import sys
import tempfile
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "advisor_run.py"
SPEC = importlib.util.spec_from_file_location("advisor_run", SCRIPT)
advisor = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(advisor)


def response(verdict="PROCEED", audit="- scope -> CONFIRMED (sample.txt:1)"):
    value = (f"VERDICT: {verdict}\n\nASK RESTATED:\nCheck scope.\n\n"
             "DO THIS:\n1. Continue the selected task.\n\nDO NOT:\n- Expand scope.\n\n"
             f"CLAIM AUDIT:\n{audit}\n\nRISKS:\nnone\n\n"
             "COULD NOT VERIFY:\nnone\n\nFLIP CONDITIONS:\n- Changed evidence.\n")
    if verdict == "INSUFFICIENT_CONTEXT":
        value += "\nMISSING:\n1. Supply the failing command output.\n"
    return value


class ResponseTests(unittest.TestCase):
    def test_valid_enum_bearing_first_line(self):
        self.assertEqual(advisor.parse_response(response())["verdict"], "PROCEED")

    def test_missing_sections_never_produce_advice(self):
        with self.assertRaises(ValueError):
            advisor.parse_response("VERDICT: PROCEED\n")

    def test_missing_context_requires_missing_items(self):
        result = advisor.parse_response(response("INSUFFICIENT_CONTEXT"))
        self.assertEqual(result["verdict"], "INSUFFICIENT_CONTEXT")
        with self.assertRaises(ValueError):
            advisor.parse_response(response().replace("PROCEED", "INSUFFICIENT_CONTEXT"))

    def test_invalid_verdict_and_preamble_rejected(self):
        for text in ("Hello\n" + response(), response("APPROVED"), "", response() + "\nVERDICT: STOP_REDIRECT"):
            with self.subTest(text=text), self.assertRaises(ValueError):
                advisor.parse_response(text)

    def test_all_unverified_is_recorded_as_evidence_gap(self):
        result = advisor.parse_response(response(audit="- scope -> UNVERIFIED (read denied)"))
        self.assertTrue(result["all_unverified"])

    def test_unexpected_missing_section_rejected(self):
        with self.assertRaises(ValueError):
            advisor.parse_response(response() + "\nMISSING:\nnone\n")


class RequestTests(unittest.TestCase):
    def test_unknown_field_rejected(self):
        with self.assertRaises(ValueError):
            advisor.validate_request({"shell": True})

    def test_budget_and_timeout_are_bounded(self):
        base = {"schema": "advisor-request-v1", "ask": "Check plan", "repo_root": str(Path.cwd()),
                "contract_path": str(SCRIPT), "claude_path": str(SCRIPT), "contract_sha256": "a" * 64}
        for field, value in (("total_budget_usd", "0"), ("total_budget_usd", "NaN"),
                             ("timeout_seconds", 0), ("timeout_seconds", True), ("type", "wrong")):
            with self.subTest(field=field, value=value), self.assertRaises(ValueError):
                advisor.validate_request(dict(base, **{field: value}))


class RunnerTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.contract = self.root / "contract.md"
        self.contract.write_text("Review independently.", encoding="utf-8")
        self.briefing = self.root / "briefing.md"
        labels = ["REQUEST TYPE and ONE-LINE ASK", "REPO ROOT", "TASK AS GIVEN", "SCOPE",
                  "BINDING CONSTRAINTS", "FACTS", "INFERENCES", "STATE", "ATTEMPTS",
                  "CURRENT PLAN", "OPTIONS CONSIDERED", "ASSUMPTIONS", "OPEN QUESTIONS",
                  "WHAT WOULD CHANGE MY MIND", "EXCERPTS"]
        self.briefing.write_text("\n\n".join(f"## {x}\nTest evidence." for x in labels), encoding="utf-8")
        self.request = {"schema": "advisor-request-v1", "ask": "Check scope", "repo_root": str(self.root),
                        "contract_path": str(self.contract), "claude_path": sys.executable,
                        "contract_sha256": hashlib.sha256(self.contract.read_bytes()).hexdigest()}
        self.calls = []
        self.run_dir = self.root / "run"

    def fake(self, argv, cwd, timeout, env=None):
        self.calls.append(argv)
        if "--help" in argv:
            text = " ".join(advisor.REQUIRED_FLAGS) + " --append-system-prompt[-file]"
        elif "--version" in argv:
            text = "2.1.273 (Claude Code)"
        else:
            text = json.dumps({"type": "result", "subtype": "success", "is_error": False,
                               "result": response(), "total_cost_usd": 0.01})
        return {"exit_code": 0, "stdout": text.encode(), "stderr": b"", "timed_out": False, "spawn_error": None}

    def run_review(self, **kwargs):
        return advisor.run_review(self.request, self.run_dir, self.briefing, execute=self.fake, **kwargs)

    def test_real_evidence_and_two_attempt_limit(self):
        first = self.run_review()
        self.assertEqual(first["response_status"], "VALID")
        self.assertEqual(first["verdict"], "PROCEED")
        saved = (self.run_dir / "attempt-001" / "execution.json").read_bytes()
        self.run_review(reason="reconcile")
        with self.assertRaises(ValueError):
            self.run_review(reason="context")
        self.assertEqual(saved, (self.run_dir / "attempt-001" / "execution.json").read_bytes())
        invocations = [x for x in self.calls if "--print" in x]
        self.assertEqual(len(invocations), 2)
        self.assertTrue(all(x[x.index("--max-budget-usd") + 1] == "1.00" for x in invocations))

    def test_contract_drift_blocks_without_invocation(self):
        self.contract.write_text("changed", encoding="utf-8")
        with self.assertRaises(ValueError):
            self.run_review()
        self.assertEqual(self.calls, [])

    def test_no_permission_relaxation_or_shell(self):
        self.run_review()
        command = self.calls[-1]
        for flag in ("--restricted", "--safe-mode", "--strict-mcp-config", "--no-session-persistence"):
            self.assertIn(flag, command)
        self.assertEqual(command[command.index("--tools") + 1], "Read,Grep,Glob")
        self.assertEqual(command[command.index("--permission-mode") + 1], "dontAsk")
        self.assertNotIn("--dangerously-skip-permissions", command)

    def test_request_change_and_existing_lock_block(self):
        self.run_review()
        self.request["ask"] = "Another task"
        with self.assertRaises(ValueError):
            self.run_review(reason="context")
        (self.run_dir / ".lock").write_text("occupied")
        with self.assertRaises(FileExistsError):
            self.run_review(reason="context")

    def test_incomplete_briefing_blocks(self):
        self.briefing.write_text("## FACTS\nNothing else", encoding="utf-8")
        with self.assertRaises(ValueError):
            self.run_review()

    def test_failed_process_never_exposes_verdict(self):
        original = self.fake
        def failed(argv, cwd, timeout, env=None):
            result = original(argv, cwd, timeout)
            if "--print" in argv:
                result["exit_code"] = 1
            return result
        value = advisor.run_review(self.request, self.run_dir, self.briefing, execute=failed)
        self.assertEqual(value["execution_status"], "FAILED")
        self.assertIsNone(value["verdict"])

    def test_subprocess_bytes_and_timeout(self):
        value = advisor.execute_process([sys.executable, "-c", "import sys; sys.stdout.buffer.write(b'abc'); sys.stderr.write('problem'); sys.exit(3)"], self.root, 5)
        self.assertEqual(value["stdout"], b"abc")
        self.assertEqual(value["stderr"], b"problem")
        self.assertEqual(value["exit_code"], 3)
        value = advisor.execute_process([sys.executable, "-c", "import time; time.sleep(3)"], self.root, 0.05)
        self.assertTrue(value["timed_out"])


if __name__ == "__main__":
    unittest.main()
