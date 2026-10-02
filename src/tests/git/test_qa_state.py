"""SPEC-007 VER-25: qa_state.py derives the QA state from gh pr view --json labels,comments,headRefOid."""
import json
import unittest

if __package__:
    from .gitfixture import Sandbox
else:
    from gitfixture import Sandbox

HEAD = "a" * 40
OLD = "b" * 40


def comment(body, at):
    return {"author": {"login": "qa-bot"}, "body": body, "createdAt": at}


def pr(labels=(), comments=(), head=HEAD):
    return {"headRefOid": head, "labels": [{"name": n} for n in labels], "comments": list(comments)}


PASSED = comment(f"QA verdict: passed {HEAD}\nReviewed by: codex session s1\nFindings:\n- advisory x", "2026-09-28T10:00:00Z")
FAILED = comment(f"QA verdict: failed {HEAD}\nFindings:\n- blocking app.py:3 add a test", "2026-09-28T10:00:00Z")


class QaStateTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.sb = Sandbox()

    @classmethod
    def tearDownClass(cls):
        cls.sb.cleanup()

    def state(self, data, *args):
        r = self.sb.run_script("qa_state.py", *args, stdin=json.dumps(data))
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        return json.loads(r.stdout)

    def test_pending(self):
        s = self.state(pr())
        self.assertEqual((s["state"], s["merge_allowed"]), ("pending", False))

    def test_unverified(self):
        self.assertEqual(self.state(pr(["merge-approved"]))["state"], "unverified")

    def test_conflicting_both_labels(self):
        self.assertEqual(self.state(pr(["merge-approved", "qa-failed"], [PASSED]))["state"], "conflicting")

    def test_conflicting_label_contradicts_verdict(self):
        self.assertEqual(self.state(pr(["merge-approved"], [FAILED]))["state"], "conflicting")
        self.assertEqual(self.state(pr(["qa-failed"], [PASSED]))["state"], "conflicting")

    def test_stale(self):
        old = comment(f"QA verdict: passed {OLD}", "2026-09-28T10:00:00Z")
        s = self.state(pr(["merge-approved"], [old]))
        self.assertEqual((s["state"], s["merge_allowed"]), ("stale", False))

    def test_approved(self):
        s = self.state(pr(["merge-approved", "bug"], [PASSED]))
        self.assertEqual((s["state"], s["merge_allowed"]), ("approved", True))
        self.assertEqual(s["verdict"]["sha"], HEAD)

    def test_failed_with_findings(self):
        s = self.state(pr(["qa-failed"], [FAILED]))
        self.assertEqual((s["state"], s["merge_allowed"]), ("failed", False))
        self.assertIn("add a test", s["verdict"]["findings"])

    def test_latest_verdict_counts(self):
        early_fail = comment(f"QA verdict: failed {OLD}", "2026-09-27T09:00:00Z")
        later_pass = comment(f"QA verdict: passed {HEAD}", "2026-09-28T12:00:00Z")
        self.assertEqual(self.state(pr(["merge-approved"], [later_pass, early_fail]))["state"], "approved")
        early_pass = comment(f"QA verdict: passed {HEAD}", "2026-09-27T09:00:00Z")
        later_fail = comment(f"QA verdict: failed {HEAD}", "2026-09-28T12:00:00Z")
        self.assertEqual(self.state(pr(["qa-failed"], [early_pass, later_fail]))["state"], "failed")

    def test_ignores_verdict_not_on_first_line(self):
        c = comment(f"Looks good to me.\nQA verdict: passed {HEAD}", "2026-09-28T10:00:00Z")
        self.assertEqual(self.state(pr(["merge-approved"], [c]))["state"], "unverified")

    def test_ignores_short_sha(self):
        c = comment(f"QA verdict: passed {HEAD[:7]}", "2026-09-28T10:00:00Z")
        self.assertEqual(self.state(pr(["merge-approved"], [c]))["state"], "unverified")

    def test_verdict_without_label_is_pending(self):
        self.assertEqual(self.state(pr([], [PASSED]))["state"], "pending")

    def test_renamed_labels(self):
        s = self.state(pr(["qa-ok"], [PASSED]), "--approved-label", "qa-ok", "--failed-label", "qa-bad")
        self.assertEqual(s["state"], "approved")

    def test_crlf_body(self):
        c = comment(f"QA verdict: passed {HEAD}\r\nFindings: none", "2026-09-28T10:00:00Z")
        self.assertEqual(self.state(pr(["merge-approved"], [c]))["state"], "approved")

    def test_invalid_input(self):
        r = self.sb.run_script("qa_state.py", stdin="not json")
        self.assertEqual(r.returncode, 2)

    def test_unexpected_shape_exits_2(self):   # SPEC-007 v2 §2: no traceback, exit 2 with an error object
        r = self.sb.run_script("qa_state.py", stdin=json.dumps({"labels": 5, "comments": [], "headRefOid": HEAD}))
        self.assertEqual(r.returncode, 2, r.stderr)
        self.assertIn("error", json.loads(r.stdout))


if __name__ == "__main__":
    unittest.main()
