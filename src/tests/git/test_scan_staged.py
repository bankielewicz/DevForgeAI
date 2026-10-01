"""SPEC-007 VER-17: scan_staged.py blocks secrets and oversized files, warns on publishable risks,
passes clean content and never prints a secret's value."""
import contextlib
import io
import json
import os
import sys
import unittest
from unittest import mock

from gitfixture import SCRIPTS, Sandbox

# Fake secrets, assembled at run time so this file itself passes the scan (and GitHub's push protection).
AWS_KEY = "AKIA" + "Q3VZ7K2M9TXW4B8N"
GH_TOKEN = "ghp_" + "a1B2c3D4e5F6g7H8i9J0k1L2m3N4o5P6q7R8"
CRED = "Tr0ub4dor" + "-and-3"
PW = "pass" + "word"
KEY_PEM = "-----BEGIN OPENSSH " + "PRIVATE KEY-----\nb3BlbnNzaC1rZXktdjEAAAAA\n-----END OPENSSH PRIVATE KEY-----\n"
# Shaped like current OpenAI keys: bodies with _ and - early on, which v1's pattern missed.
OPENAI_PROJ = "sk-" + "proj-" + "Xq7_Lm2-Rt9aBc4Dk8_Wn3Pz6-Yh1Ve5Tg0Uj2Is7Of4Kd9Lr3Mx8Nq6Sp1Tz5Ua0Wb2Xc7Yd4Ze9"
OPENAI_SVC = "sk-" + "svcacct-" + "Hb5_Qe8-Wr2Ty6Ui0Op4As9Df3Gh7Jk1Lz5Xc8Vb2Nm6Qw0Er4Ty9Ui3Op7As1Df5"
OPENAI_ADMIN = "sk-" + "admin-" + "Pz3-Lk9_Mj2Nh6Bg0Vf4Cd8Xs1Za5Qw7Er3Ty9Ui2Op6As0Df4Gh8Jk2Lz6Xc1"
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

    # --- version 2 (SPEC-007 v2, VER-17) ------------------------------------------------------

    def test_blocks_current_openai_key_formats(self):
        keys = {"a.py": OPENAI_PROJ, "b.py": OPENAI_SVC, "c.py": OPENAI_ADMIN}
        for rel, key in keys.items():
            self.stage(rel, f'client = OpenAI(load("{key}"))\n')   # no keyword: only the key format can match
        report, out = self.scan()
        for rel, key in keys.items():
            self.assertIn("openai_key", self.checks(report["blocked"], rel), rel)
            self.assertNotIn(key, out)

    def test_url_credentials_block_or_warn_by_host(self):
        self.stage("deploy/remote.txt", f"endpoint https://deploy:{CRED}@api.acme-corp.io/v1\n")
        self.stage("docker-compose.yml", "DATABASE_URL: postgres://postgres:postgres@db:5432/app\n")
        self.stage("docs/dev.md", f"mysql://root:{CRED}@127.0.0.1/app\namqp://guest:{CRED}@rabbit.test/\n"
                                  f"https://user:{CRED}@example.com/x\nredis://app:{CRED}@localhost:6379\n"
                                  f"https://ci:{CRED}@ci.example.org/\nhttps://same:same@git.acme-corp.io/r\n")
        report, out = self.scan()
        blocked = sorted((f["path"], f.get("line")) for f in report["blocked"])
        self.assertEqual(blocked, [("deploy/remote.txt", 1)])
        warned = sorted((f["path"], f["line"]) for f in report["warnings"] if f["check"] == "url_credentials")
        self.assertEqual(warned, [("docker-compose.yml", 1)] + [("docs/dev.md", n) for n in range(1, 7)])
        self.assertNotIn(CRED, out)

    def test_literal_credential_in_test_paths_warns(self):
        line = f'client.login(username="alice", {PW}="pw1234")\n'
        tests = ["tests/test_login.py", "web/app.test.ts", "spec/models/user_spec.rb", "conftest.py",
                 "fixtures/users.json", "pkg/auth_test.go", "testdata/login.txt"]
        for rel in tests + ["src/contest.py", "src/testing_utils.py"]:
            self.stage(rel, line)
        self.stage("tests/test_api.py", f"TOKEN = '{GH_TOKEN}'\n")   # a token format blocks in tests too
        report, out = self.scan()
        warned = sorted(f["path"] for f in report["warnings"] if f["check"] == "literal_credential")
        self.assertEqual(warned, sorted(tests))
        blocked = sorted((f["check"], f["path"]) for f in report["blocked"])
        self.assertEqual(blocked, [("github_token", "tests/test_api.py"), ("literal_credential", "src/contest.py"),
                                   ("literal_credential", "src/testing_utils.py")])
        self.assertNotIn("pw1234", out)

    def test_added_line_starting_with_plus_plus(self):   # v1 read "+++x" as a diff header and skipped it
        self.stage("notes.txt", f"++ token {GH_TOKEN}\n")
        report, out = self.scan()
        self.assertIn("github_token", self.checks(report["blocked"], "notes.txt"))
        self.assertNotIn(GH_TOKEN, out)

    def test_non_utf8_content_and_path(self):
        (self.repo / "notes.txt").write_bytes(b"caf\xe9 \r\n")
        name = b"r\xe9sum\xe9.txt"
        with open(os.path.join(os.fsencode(self.repo), name), "wb") as f:
            f.write(b"x\n")
        self.sb.git(self.repo, "add", "--", "notes.txt", os.fsdecode(name))
        report, _ = self.scan()
        self.assertEqual(report["blocked"], [])
        self.assertEqual(report["files_scanned"], 2)
        self.assertIn("crlf_line_endings", self.checks(report["warnings"], "notes.txt"))

    def test_unexpected_error_exits_2(self):
        sys.dont_write_bytecode = True   # importing the script must not leave __pycache__ in the plugin
        sys.path.insert(0, str(SCRIPTS))
        try:
            import scan_staged
        finally:
            sys.path.remove(str(SCRIPTS))
        out = io.StringIO()
        with mock.patch.object(scan_staged, "scan", side_effect=RuntimeError("boom")), \
                contextlib.redirect_stdout(out):
            rc = scan_staged.main(["-C", str(self.repo)])
        self.assertEqual(rc, 2)
        self.assertIn("error", json.loads(out.getvalue()))


if __name__ == "__main__":
    unittest.main()
