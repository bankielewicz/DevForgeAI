"""Reject semantic evidence tampering after the outer digest checks succeed."""

import json
import re
import sys
import tempfile
import unittest
from pathlib import Path

from test_streaming import advisor, jsonl, process, result_event


class PriorAttemptIntegrityTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.contract = self.root / "contract.md"
        self.contract.write_text("Synthetic read-only review.", encoding="utf-8")
        self.briefing = self.root / "briefing.md"
        self.briefing.write_text("\n\n".join(
            f"## {label}\nSynthetic evidence." for label in advisor.BRIEFING_SECTIONS),
            encoding="utf-8")
        self.request = advisor.validate_request({
            "schema": "advisor-request-v1", "ask": "Verify the synthetic candidate",
            "repo_root": str(self.root), "claude_path": sys.executable,
            "contract_path": str(self.contract),
            "contract_sha256": advisor.digest(self.contract.read_bytes()),
            "auth_mode": "subscription",
        })
        self.run_dir = self.root / "run"
        self.attempt = self.run_dir / "attempt-001"
        self.calls = []
        self.review_process = process(jsonl(result_event()))

    def probe(self, argv, cwd, timeout, env=None):
        self.calls.append(tuple(argv))
        if "--version" in argv:
            text = "synthetic-cli"
        elif "--help" in argv:
            text = " ".join(advisor.REQUIRED_FLAGS) + " --append-system-prompt-file --verbose stream-json"
        else:
            raise AssertionError("No quiet reviewer invocation is expected")
        return {"exit_code": 0, "stdout": text.encode(), "stderr": b"",
                "timed_out": False, "spawn_error": None}

    def stream(self, argv, cwd, timeout, env=None, progress=None):
        self.calls.append(tuple(argv))
        return self.review_process

    def review(self, reason="initial"):
        return advisor.run_review(
            self.request, self.run_dir, self.briefing, reason=reason,
            execute=self.probe, show_progress=True, stream_execute=self.stream)

    def pristine(self, failed=False):
        if failed:
            self.review_process = process(
                jsonl(result_event(is_error=True, result="Synthetic failure")), exit_code=1)
        receipt = self.review()
        self.assertEqual(receipt["execution_status"], "FAILED" if failed else "SUCCEEDED")
        self.assertEqual(receipt["response_status"], "NOT_EVALUATED" if failed else "VALID")
        self.request_hash = advisor.digest((self.run_dir / "request.json").read_bytes())
        # Prove the complete fixture is accepted before making any change.
        self.assertIsNone(advisor.validate_prior_attempt(
            self.attempt, 1, self.request, self.request_hash, "1.00"))
        return receipt

    def assert_rejected(self, reason):
        snapshot = {p.name: p.read_bytes() for p in self.attempt.iterdir() if p.is_file()}
        before_calls = list(self.calls)
        message = "^" + re.escape("Invalid prior attempt history: " + reason) + "$"
        with self.assertRaisesRegex(ValueError, message):
            advisor.validate_prior_attempt(self.attempt, 1, self.request, self.request_hash, "1.00")
        # Also prove that the normal follow-up path stops before preflight or invocation.
        with self.assertRaisesRegex(ValueError, message):
            self.review(reason="retry")
        self.assertEqual(self.calls, before_calls)
        self.assertFalse((self.run_dir / "attempt-002").exists())
        self.assertFalse((self.run_dir / ".lock").exists())
        self.assertEqual(snapshot, {p.name: p.read_bytes() for p in self.attempt.iterdir() if p.is_file()})

    def rewrite_fixture(self, path, value):
        # Deliberate test tampering bypasses the production writer's create-only mode.
        path.write_bytes((json.dumps(value, ensure_ascii=True, indent=2, allow_nan=False)
                          + "\n").encode("utf-8"))

    def test_receipt_cost_disagreeing_with_raw_stream_is_rejected(self):
        receipt = self.pristine()
        receipt["reported_cost_usd"] = 0.75
        self.rewrite_fixture(self.attempt / "execution.json", receipt)
        self.assert_rejected("Prior stream receipt disagrees with raw output: reported_cost_usd")

    def test_launch_version_disagreeing_with_receipt_is_rejected_after_rehash(self):
        receipt = self.pristine()
        path = self.attempt / "started.json"
        started = json.loads(path.read_text(encoding="utf-8"))
        started["claude_version"] = "tampered-version"
        self.rewrite_fixture(path, started)
        # Rebind only the dependent digest so the semantic comparison is reached.
        receipt["started_sha256"] = advisor.digest(path.read_bytes())
        self.rewrite_fixture(self.attempt / "execution.json", receipt)
        self.assert_rejected("Prior launch record disagrees with receipt")

    def test_final_envelope_disagreeing_with_raw_stream_is_rejected_after_rehash(self):
        receipt = self.pristine()
        path = self.attempt / "result.json"
        envelope = json.loads(path.read_text(encoding="utf-8"))
        envelope["total_cost_usd"] = 0.75
        self.rewrite_fixture(path, envelope)
        receipt["result_sha256"] = advisor.digest(path.read_bytes())
        self.rewrite_fixture(self.attempt / "execution.json", receipt)
        self.assert_rejected("Prior final envelope disagrees with raw output")

    def test_failed_attempt_with_stray_extracted_response_is_rejected(self):
        self.pristine(failed=True)
        path = self.attempt / "response.md"
        self.assertFalse(path.exists())
        path.write_text("Fabricated successful advice", encoding="utf-8")
        self.assert_rejected("Unexpected prior extracted response")

    def test_stream_receipt_with_extra_field_is_rejected(self):
        receipt = self.pristine()
        receipt["unexpected_field"] = "unrecognized"
        self.rewrite_fixture(self.attempt / "execution.json", receipt)
        self.assert_rejected("Invalid prior stream format")


if __name__ == "__main__":
    unittest.main()
