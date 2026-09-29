"""SPEC-007 VER-17: scan_staged.py blocks secrets and oversized files, warns on publishable risks,
passes clean content and never prints a secret's value."""
import json
import os
import unittest

from gitfixture import Sandbox

# Fake secrets, assembled at run time so this file itself passes the scan (and GitHub's push protection).
AWS_KEY = "AKIA" + "Q3VZ7K2M9TXW4B8N"
GH_TOKEN = "ghp_" + "a1B2c3D4e5F6g7H8i9J0k1L2m3N4o5P6q7R8"
CRED = "Tr0ub4dor" + "-and-3"
PW = "pass" + "word"
KEY_PEM = "-----BEGIN OPENSSH " + "PRIVATE KEY-----\nb3BlbnNzaC1rZXktdjEAAAAA\n-----END OPENSSH PRIVATE KEY-----\n"
MB = 1024 * 1024


class ScanStagedTest(unittest.TestCase):
    def setUp(self):
        self.sb = Sandbox()
        self.repo = self.sb.repo("work")
        self.sb.write(self.repo, "README.md", "# demo\n\nContact dana@example.com.\n")
        self.sb.write(self.repo, "app.py", "print('hello')\n")
        self.sb.commit(self.repo, "Initial commit")

    def tearDown(self):
        self.sb.cleanup()

    def stage(self, rel, content):
        p = self.sb.write(self.repo, rel, content)
        self.sb.git(self.repo, "add", "--", rel)
        return p

    def stage_sized(self, rel, size):
        p = self.repo / rel
        with open(p, "wb") as f:
            f.truncate(size)
        self.sb.git(self.repo, "add", "--", rel)

    def scan(self):
        r = self.sb.run_script("scan_staged.py", "-C", str(self.repo))
        self.assertIn(r.returncode, (0, 1), r.stdout + r.stderr)
        report = json.loads(r.stdout)
        self.assertEqual(r.returncode == 1, bool(report["blocked"]))
        return report, r.stdout

    def checks(self, findings, path=None):
        return {f["check"] for f in findings if path is None or f["path"] == path}

    def test_clean_content_reports_nothing(self):
        self.stage("app.py", "print('hello, world')\n")
        self.stage("lib/util.py", "def add(a, b):\n    return a + b\n")
        report, _ = self.scan()
        self.assertEqual((report["blocked"], report["warnings"]), ([], []))
        self.assertEqual(report["files_scanned"], 2)

    def test_blocks_private_key(self):
        self.stage("deploy/key.txt", KEY_PEM)
        report, out = self.scan()
        self.assertIn("private_key", self.checks(report["blocked"], "deploy/key.txt"))
        self.assertNotIn("b3BlbnNzaC1rZXktdjEAAAAA", out)

    def test_blocks_aws_key_without_printing_it(self):
        self.stage("config.py", f"AWS_ACCESS_KEY_ID = '{AWS_KEY}'\n")
        report, out = self.scan()
        found = [f for f in report["blocked"] if f["check"] == "aws_access_key"]
        self.assertEqual([(f["path"], f["line"]) for f in found], [("config.py", 1)])
        self.assertNotIn(AWS_KEY, out)
        self.assertNotIn(AWS_KEY[4:], out)

    def test_blocks_github_token(self):
        self.stage("ci/env.sh", f"export TOKEN={GH_TOKEN}\n")
        report, out = self.scan()
        self.assertIn("github_token", self.checks(report["blocked"]))
        self.assertNotIn(GH_TOKEN, out)

    def test_blocks_literal_password(self):
        self.stage("settings.py", f'DEBUG = True\nDB_{PW.upper()} = "{CRED}"\n')
        report, out = self.scan()
        found = [f for f in report["blocked"] if f["check"] == "literal_credential"]
        self.assertEqual([(f["path"], f["line"]) for f in found], [("settings.py", 2)])
        self.assertNotIn(CRED, out)

    def test_placeholder_password_is_not_blocked(self):
        self.stage("settings.py", 'DB_PASSWORD = "${DB_PASSWORD}"\nAPI_KEY = "<your-api-key>"\n'
                                  'password = os.environ["PW"]\n')
        report, _ = self.scan()
        self.assertEqual(report["blocked"], [])

    def test_blocks_unquoted_credential_in_config_files(self):
        self.stage("deploy/app.ini", f"[db]\nhost = db.internal\nDB_{PW.upper()}={CRED}\n")
        self.stage("deploy/values.yaml", f"db:\n  {PW}: {CRED}\n")
        report, out = self.scan()
        found = sorted((f["path"], f["line"]) for f in report["blocked"] if f["check"] == "literal_credential")
        self.assertEqual(found, [("deploy/app.ini", 3), ("deploy/values.yaml", 2)])
        self.assertNotIn(CRED, out)

    def test_unquoted_references_and_code_are_not_blocked(self):
        self.stage("deploy/values.yaml", "db:\n  password: ${DB_PASSWORD}\n  api_key: !vault db/key\n")
        self.stage("lib/auth.py", "password = read_password()\napi_key = settings.API_KEY\n")
        report, _ = self.scan()
        self.assertEqual(report["blocked"], [])

    def test_blocks_env_file(self):
        self.stage(".env", "DEBUG=1\n")
        self.stage(".env.example", "DEBUG=\n")
        report, _ = self.scan()
        self.assertEqual([f["path"] for f in report["blocked"] if f["check"] == "env_file"], [".env"])

    def test_blocks_file_over_100mb(self):
        self.stage_sized("data.bin", 101 * MB)
        report, _ = self.scan()
        self.assertIn("file_over_100mb", self.checks(report["blocked"], "data.bin"))

    def test_warns_on_60mb_file(self):
        self.stage_sized("model.bin", 60 * MB)
        report, _ = self.scan()
        self.assertEqual(report["blocked"], [])
        self.assertIn("file_over_50mb", self.checks(report["warnings"], "model.bin"))

    def test_warns_on_home_path(self):
        self.stage("notes.md", "Run it from /home/alice/projects/demo.\nOr C:/Users/alice/demo.\n")
        report, _ = self.scan()
        self.assertEqual(sorted(f["line"] for f in report["warnings"] if f["check"] == "home_path"), [1, 2])
        self.assertEqual(report["blocked"], [])

    def test_warns_on_unknown_email_only(self):
        self.stage("AUTHORS", "Dana Reyes <dana@example.com>\nLee Park <lee.park@corp-mail.io>\n")
        report, _ = self.scan()
        emails = [f for f in report["warnings"] if f["check"] == "email_address"]
        self.assertEqual([(f["line"], f["match"]) for f in emails], [(2, "lee.park@corp-mail.io")])

    def test_warns_on_pdf(self):
        self.stage("docs/guide.pdf", b"%PDF-1.7\n\x00\x01binary\n")
        report, _ = self.scan()
        self.assertIn("third_party_document", self.checks(report["warnings"], "docs/guide.pdf"))

    def test_warns_on_crlf_in_lf_repository(self):
        self.stage("new.txt", "one\r\ntwo\r\n")
        report, _ = self.scan()
        self.assertIn("crlf_line_endings", self.checks(report["warnings"], "new.txt"))

    def test_crlf_allowed_by_attribute(self):
        self.stage(".gitattributes", "*.bat text eol=crlf\n")
        self.stage("run.bat", "echo one\r\necho two\r\n")
        report, _ = self.scan()
        self.assertNotIn("crlf_line_endings", self.checks(report["warnings"], "run.bat"))

    def test_warns_on_trailing_whitespace(self):
        self.stage("app.py", "print('hello')   \n")
        report, _ = self.scan()
        ws = [f for f in report["warnings"] if f["check"] == "whitespace"]
        self.assertEqual([(f["path"], f["line"]) for f in ws], [("app.py", 1)])

    def test_scans_only_added_lines_of_modified_files(self):
        self.sb.write(self.repo, "old.cfg", f'{PW} = "{CRED}"\n')
        self.sb.commit(self.repo, "Pre-existing file")   # already published: not this commit's problem
        self.stage("old.cfg", f'{PW} = "{CRED}"\nport = 8080\n')
        report, _ = self.scan()
        self.assertEqual(report["blocked"], [])

    def test_not_a_repository(self):
        plain = self.sb.dir / "plain"
        plain.mkdir()
        r = self.sb.run_script("scan_staged.py", "-C", str(plain))
        self.assertEqual(r.returncode, 2)


if __name__ == "__main__":
    unittest.main()
