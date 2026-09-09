"""Independent synthetic expectations for the bounded revision-004 identity eval."""
import hashlib
import json
import tempfile
import unittest
from pathlib import Path

import reference_identity_v4 as identity


class ReferenceIdentityTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.artifact = {"schema_version": "devforge.artifact/v1", "artifact_id": "IDEAS-900",
                         "artifact_type": "idea-ledger", "project_id": "synthetic", "revision": 1}
        self.write("artifact.json", json.dumps(self.artifact))
        self.write("artifact.md", "---\n" + json.dumps(self.artifact) + "\n---\n# Ledger\n## Ideas [IDEAS-SECTION-900]\n| IDEA-900 | origin |\n")
        self.write("yaml.md", "---\nschema_version: devforge.artifact/v1\nartifact_id: IDEAS-901\nrevision: 2\n---\n# Ledger\n")
        self.write("receipt.json", json.dumps({"schema_version": "native.byte/v1", "receipt_id": "CHECK-900",
                                               "checked_input": {"artifact_id": "IDEAS-900", "revision": 1}}))
        self.write("note.md", "# Prior note [CONT-900]\n\n## Scope [SCOPE-900]\n\n```yaml\nartifact_id: FAKE-900\n```\n")
        self.write("selector.json", json.dumps({"artifact_id": "IDEAS-900", "revision": 1,
                                                "path": "artifact.json", "sha256": self.digest("artifact.json")}))

    def write(self, name, text):
        (self.root / name).write_text(text)

    def digest(self, name):
        return hashlib.sha256((self.root / name).read_bytes()).hexdigest()

    def ref(self, path, aid=None, rev=None, sections=None):
        return dict(artifact_id=aid, revision=rev, store="project", path=path,
                    sha256=self.digest(path), sections=sections or [])

    def check(self, meta, table=""):
        self.write("output.md", "---\n" + json.dumps(meta) + "\n---\n# Handoff\n" + table)
        return identity.inspect_document(self.root / "output.md", {"project": self.root})

    def test_operator_eight_contrasts(self):
        # Explicit expected verdicts derive from declarations in the fixtures.
        cases = [
            ("artifact.json", "upstream", "IDEAS-900", 1, "PASS"),
            ("receipt.json", "evidence", None, None, "PASS"),
            ("note.md", "evidence", None, None, "PASS"),
            ("selector.json", "evidence", None, None, "PASS"),
            ("receipt.json", "upstream", None, None, "PASS"),
            ("receipt.json", "upstream", "CHECK-900", None, "FAIL"),
            ("note.md", "upstream", "CONT-900", None, "FAIL"),
            ("selector.json", "upstream", "IDEAS-900", 1, "FAIL"),
        ]
        for path, field, aid, rev, expected in cases:
            with self.subTest(path=path, field=field, aid=aid):
                ref = self.ref(path, aid, rev)
                if field == "evidence":
                    ref.pop("artifact_id"); ref.pop("revision")
                self.assertEqual(self.check({field: [ref]})["result"], expected)

    def test_own_json_yaml_envelopes_and_mismatches(self):
        for path, aid, rev in [("artifact.md", "IDEAS-900", 1), ("yaml.md", "IDEAS-901", 2)]:
            self.assertEqual(self.check({"upstream": [self.ref(path, aid, rev)]})["result"], "PASS")
        for key, value in [("artifact_id", "IDEAS-999"), ("revision", 9), ("sha256", "0" * 64)]:
            ref = self.ref("artifact.json", "IDEAS-900", 1); ref[key] = value
            self.assertEqual(self.check({"upstream": [ref]})["result"], "FAIL")

    def test_repeated_and_nested_mappings(self):
        valid = self.ref("receipt.json")
        invalid = self.ref("receipt.json", "CHECK-900")
        for meta in [{"upstream": [valid, invalid]},
                     {"evidence": [{"observations": [valid, invalid]}]},
                     {"execution_ref": invalid}, {"supersedes": invalid}]:
            result = self.check(meta)
            self.assertEqual(result["result"], "FAIL")
            self.assertTrue(any(i["code"] == "raw-identity-promotion" for i in result["issues"]))

    def test_sections_are_actual_headings_not_rows_or_artifact_identity(self):
        self.assertEqual(self.check({"upstream": [self.ref("artifact.md", "IDEAS-900", 1, ["IDEAS-SECTION-900"])]})["result"], "PASS")
        self.assertEqual(self.check({"upstream": [self.ref("artifact.md", "IDEAS-900", 1, ["IDEA-900"])]})["result"], "FAIL")
        self.assertEqual(self.check({"evidence": [self.ref("note.md", sections=["CONT-900", "SCOPE-900"])]})["result"], "PASS")
        self.assertEqual(self.check({"evidence": [self.ref("note.md", sections=["FAKE-900"])]})["result"], "FAIL")

    def table(self, path, label):
        return ("| Direction | Artifact ID/revision | Store/path | SHA-256 | Relevant sections | Decision/freshness state |\n"
                "| --- | --- | --- | --- | --- | --- |\n"
                f"| input | {label} | project:{path} | {self.digest(path)} | [] | observed |\n")

    def test_table_only_promotions_and_valid_raw_table(self):
        for path, label in [("receipt.json", "CHECK-900@None"), ("note.md", "CONT-900@null"),
                            ("selector.json", "IDEAS-900@1 selector")]:
            result = self.check({"evidence": [self.ref(path)]}, self.table(path, label))
            self.assertEqual(result["result"], "FAIL")
            self.assertTrue(any(i["code"] == "table-raw-identity-promotion" for i in result["issues"]))
        result = self.check({"evidence": [self.ref("receipt.json")]},
                            self.table("receipt.json", "raw receipt; artifact ID/revision null; receipt_id CHECK-900"))
        self.assertEqual(result["result"], "PASS")
        self.assertEqual(result["manual_review"], "REQUIRED")
        self.assertEqual(len(result["table_occurrences"]), 1)

    def test_selector_and_target_stay_separate(self):
        refs = [self.ref("selector.json"), self.ref("artifact.json", "IDEAS-900", 1)]
        self.assertEqual(self.check({"upstream": refs}, self.table("artifact.json", "IDEAS-900@1"))["result"], "PASS")
        refs[1]["path"] = "selector.json"
        self.assertEqual(self.check({"upstream": refs})["result"], "FAIL")

    def test_ambiguous_duplicate_keys_and_unresolved_sources(self):
        self.write("duplicate.md", "---\nupstream: []\nupstream: []\n---\n")
        self.assertEqual(identity.inspect_document(self.root / "duplicate.md", {"project": self.root})["result"], "COULD_NOT_RUN")
        ref = self.ref("artifact.json", "IDEAS-900", 1); ref["path"] = "../artifact.json"
        self.assertEqual(self.check({"upstream": [ref]})["result"], "FAIL")

    def test_absolute_raw_evidence_requires_manual_location_resolution(self):
        raw = {"path": "/tmp/project/native-check.json", "sha256": self.digest("receipt.json")}
        result = self.check({"evidence": [raw]})
        self.assertEqual(result["result"], "PASS")
        self.assertEqual(result["manual_review"], "REQUIRED")
        self.assertEqual(result["occurrences"][0]["recognition"], "absolute-evidence-locator-manual-required")
        self.assertNotIn("source", result["occurrences"][0])
        ref = self.ref("artifact.json", "IDEAS-900", 1)
        ref["path"] = "/tmp/project/artifact.json"
        self.assertEqual(self.check({"upstream": [ref]})["result"], "FAIL")
        raw.update(artifact_id="CHECK-900", revision=None)
        self.assertEqual(self.check({"evidence": [raw]})["result"], "FAIL")


if __name__ == "__main__":
    unittest.main()
