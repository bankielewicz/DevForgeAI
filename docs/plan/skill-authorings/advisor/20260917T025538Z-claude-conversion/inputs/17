"""Authentication policy tests use synthetic values and real local children."""
import contextlib
import io
import json
import os
import sys
import unittest
from unittest.mock import patch

import test_advisor
from test_advisor import advisor
from test_extended import evaluation


class AuthTests(unittest.TestCase):
    setUp = test_advisor.RunnerTests.setUp
    fake = test_advisor.RunnerTests.fake

    def test_subscription_request_excludes_key_from_every_child(self):
        self.request["auth_mode"] = "subscription"
        observed = []

        def capture(argv, cwd, timeout, env=None):
            observed.append(env)
            return self.fake(argv, cwd, timeout)

        with patch.dict(os.environ, {"ANTHROPIC_API_KEY": "synthetic-invalid-key"}):
            before = dict(os.environ)
            try:
                result = advisor.run_review(self.request, self.run_dir, self.briefing, execute=capture)
            except ValueError as error:
                self.fail("Subscription requests must execute with a filtered environment: " + str(error))
            self.assertEqual(dict(os.environ), before)
        self.assertEqual(len(observed), 3)
        for environment in observed:
            self.assertIsNotNone(environment)
            self.assertEqual(environment, {k: v for k, v in before.items() if k.upper() != "ANTHROPIC_API_KEY"})
        self.assertEqual(result["auth_mode"], "subscription")
        self.assertNotIn("synthetic-invalid-key", (self.run_dir / "attempt-001/execution.json").read_text())
        self.assertEqual(advisor.read_json(self.run_dir / "request.json")["auth_mode"], "subscription")

    def test_real_children_and_parent_environment(self):
        probe = "import json,os; print(json.dumps([os.environ.get('ANTHROPIC_API_KEY'), os.environ.get('ADVISOR_AUTH_TEST')]))"
        with patch.dict(os.environ, {"ANTHROPIC_API_KEY": "synthetic-key", "ADVISOR_AUTH_TEST": "preserve"}):
            before = dict(os.environ)
            for mode, expected in (("inherit", ["synthetic-key", "preserve"]), ("subscription", [None, "preserve"])):
                with self.subTest(mode=mode):
                    child_env = advisor.build_environment(mode, os.environ)
                    result = advisor.execute_process([sys.executable, "-c", probe], self.root, 10, env=child_env)
                    self.assertEqual(result["exit_code"], 0, result["stderr"])
                    self.assertEqual(json.loads(result["stdout"]), expected)
            self.assertEqual(dict(os.environ), before)

    def test_absent_key_case_variants_and_independent_copy(self):
        source = {"Path": "keep", "anthropic_api_key": "lower", "AnThRoPiC_ApI_KeY": "mixed"}
        self.assertEqual(advisor.build_environment("subscription", source), {"Path": "keep"})
        self.assertEqual(len(source), 3)
        inherited = advisor.build_environment("inherit", source)
        self.assertEqual(inherited, source)
        self.assertIsNot(inherited, source)
        self.assertEqual(advisor.build_environment("subscription", {}), {})
        with self.assertRaises(ValueError):
            advisor.build_environment("automatic", source)

    def test_request_modes_and_invalid_values(self):
        self.assertEqual(advisor.validate_request(self.request)["auth_mode"], "inherit")
        for mode in ("inherit", "subscription"):
            self.assertEqual(advisor.validate_request(dict(self.request, auth_mode=mode))["auth_mode"], mode)
        for mode in (None, "", "auto", True, [], {}):
            with self.subTest(mode=mode), self.assertRaises(ValueError):
                advisor.validate_request(dict(self.request, auth_mode=mode))

    def test_mode_change_is_immutable_and_receipt_mismatch_blocks(self):
        advisor.run_review(self.request, self.run_dir, self.briefing, execute=self.fake)
        before = len(self.calls)
        with self.assertRaisesRegex(ValueError, "immutable"):
            advisor.run_review(dict(self.request, auth_mode="subscription"), self.run_dir, self.briefing, reason="retry", execute=self.fake)
        receipt_path = self.run_dir / "attempt-001/execution.json"
        receipt = advisor.read_json(receipt_path)
        receipt["auth_mode"] = "subscription"
        receipt_path.write_text(json.dumps(receipt))
        with self.assertRaisesRegex(ValueError, "prior"):
            advisor.run_review(self.request, self.run_dir, self.briefing, reason="retry", execute=self.fake)
        self.assertEqual(len(self.calls), before)

    def test_legacy_request_and_receipt_preserve_bytes(self):
        # Construct a synthetic legacy history: v1 before auth_mode existed.
        advisor.run_review(self.request, self.run_dir, self.briefing, execute=self.fake)
        request_path = self.run_dir / "request.json"
        legacy = advisor.read_json(request_path)
        legacy.pop("auth_mode")
        request_path.write_text(json.dumps(legacy))
        for name in ("started.json", "execution.json"):
            path = self.run_dir / "attempt-001" / name
            record = advisor.read_json(path)
            record.pop("auth_mode")
            record["request_sha256"] = advisor.digest(request_path.read_bytes())
            path.write_text(json.dumps(record))
        preserved = {path: path.read_bytes() for path in self.run_dir.rglob("*") if path.is_file()}
        result = advisor.run_review(self.request, self.run_dir, self.briefing, reason="retry", execute=self.fake)
        self.assertEqual(result["auth_mode"], "inherit")
        for path, data in preserved.items():
            self.assertEqual(path.read_bytes(), data)
        with self.assertRaisesRegex(ValueError, "Two-attempt"):
            advisor.run_review(self.request, self.run_dir, self.briefing, reason="retry", execute=self.fake)

    def test_standalone_preflight_filters_environment(self):
        observed = []

        def capture(argv, cwd, timeout, env=None):
            observed.append(env)
            return self.fake(argv, cwd, timeout)

        with patch.dict(os.environ, {"ANTHROPIC_API_KEY": "synthetic-key"}):
            result = advisor.preflight(sys.executable, self.root, execute=capture, auth_mode="subscription")
        self.assertEqual(result["auth_mode"], "subscription")
        self.assertEqual(len(observed), 2)
        self.assertTrue(all("ANTHROPIC_API_KEY" not in env for env in observed))

    def test_auth_failure_does_not_retry_or_switch_modes(self):
        self.request["auth_mode"] = "subscription"
        seen = []

        def failed(argv, cwd, timeout, env=None):
            result = self.fake(argv, cwd, timeout)
            if "--print" in argv:
                seen.append(env)
                result.update(exit_code=1, stdout=b'{"is_error":true,"api_error_status":401,"result":"Invalid synthetic key"}')
            return result

        with patch.dict(os.environ, {"ANTHROPIC_API_KEY": "synthetic-key"}):
            result = advisor.run_review(self.request, self.run_dir, self.briefing, execute=failed)
        self.assertEqual(result["execution_status"], "FAILED")
        self.assertEqual(result["response_status"], "NOT_EVALUATED")
        self.assertIsNone(result["verdict"])
        self.assertEqual(len(seen), 1)
        self.assertNotIn("ANTHROPIC_API_KEY", seen[0])
        self.assertFalse((self.run_dir / "attempt-002").exists())

    def test_subscription_receipt_requires_explicit_mode(self):
        self.request["auth_mode"] = "subscription"
        advisor.run_review(self.request, self.run_dir, self.briefing, execute=self.fake)
        path = self.run_dir / "attempt-001/execution.json"
        receipt = advisor.read_json(path)
        del receipt["auth_mode"]
        path.write_text(json.dumps(receipt))
        with self.assertRaisesRegex(ValueError, "prior"):
            advisor.run_review(self.request, self.run_dir, self.briefing, reason="retry", execute=self.fake)

    def test_preflight_cli_forwards_selected_mode(self):
        for arguments, expected in (([], "inherit"), (["--auth-mode", "subscription"], "subscription")):
            with contextlib.redirect_stdout(io.StringIO()), patch.object(advisor, "preflight", return_value={}) as preflight:
                self.assertEqual(advisor.main(["preflight", "--claude", sys.executable] + arguments), 0)
                self.assertEqual(preflight.call_args.kwargs["auth_mode"], expected)

    def test_auth_fixture_has_independent_expected_output(self):
        case = {"kind": "environment", "input": {"auth_mode": "subscription", "environment": {"ANTHROPIC_API_KEY": "fake", "KEEP": "value"}}}
        self.assertEqual(evaluation.observe(case), {"environment": {"KEEP": "value"}})


if __name__ == "__main__":
    unittest.main()
