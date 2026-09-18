"""Synthetic CLI regressions derived from CODEX-SKILL-VALIDATOR-SPEC-001.

The CLI is always executed in a subprocess. Expected observations are defined
from the specification, independently of helper-produced pass flags. Temporary
fixtures obey the caller's TEMP/TMPDIR and never touch an operational skill.
"""

import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest


HELPER = Path(__file__).resolve().parents[1] / "scripts" / "observe.py"
VALID_SKILL = "---\nname: example\ndescription: Deliver a named local summary.\n---\n\n# Example\n\nWrite the requested summary and return its path.\n"


def sha256(data):
    return hashlib.sha256(data).hexdigest()


class ObserveCliTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="validator-helper-")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.skill = self.root / "project with spaces" / "example"
        self.skill.mkdir(parents=True)
        self.write("SKILL.md", VALID_SKILL)

    def write(self, relative, content):
        path = self.skill / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(content.encode("utf-8") if isinstance(content, str) else content)
        return path

    def invoke(self, *arguments, expected=0):
        command = [sys.executable, "-B", "-X", "utf8", str(HELPER), *map(str, arguments)]
        receipt_root = os.environ.get("SV_TEST_RECEIPT_DIR")
        receipt = None
        if receipt_root:
            receipts = Path(receipt_root)
            receipts.mkdir(parents=True, exist_ok=True)
            receipt = receipts / f"{len(list(receipts.iterdir())) + 1:04}-{self._testMethodName}"
            receipt.mkdir()
            shutil.copytree(self.root, receipt / "input", symlinks=True)
            rows = []
            for path in sorted((receipt / "input").rglob("*")):
                if path.is_file() and not path.is_symlink():
                    data = path.read_bytes()
                    rows.append({"path": path.relative_to(receipt / "input").as_posix(), "bytes": len(data), "sha256": sha256(data)})
            (receipt / "input-manifest.json").write_text(json.dumps(rows, ensure_ascii=False, indent=2), encoding="utf-8")
            (receipt / "command.json").write_text(json.dumps({"argv": command, "cwd": str(self.root), "expected_exit": expected}, ensure_ascii=False, indent=2), encoding="utf-8")
        result = subprocess.run(
            command,
            cwd=self.root,
            capture_output=True,
            encoding="utf-8",
            timeout=30,
            check=False,
        )
        if receipt is not None:
            (receipt / "stdout.txt").write_text(result.stdout, encoding="utf-8")
            (receipt / "stderr.txt").write_text(result.stderr, encoding="utf-8")
            (receipt / "result.json").write_text(json.dumps({"exit_code": result.returncode, "matched": result.returncode == expected}), encoding="utf-8")
        self.assertEqual(
            expected, result.returncode,
            f"Command arguments: {arguments!r}\nstdout:\n{result.stdout}\nstderr:\n{result.stderr}",
        )
        return result

    def snapshot(self, expected=0):
        destination = self.root / "snapshot output"
        result = self.invoke("snapshot", "--source", self.skill, "--output", destination, expected=expected)
        return destination, result

    def test_cli_help_and_each_command_help(self):
        for command in (None, "snapshot", "structure", "readback", "records"):
            with self.subTest(command=command):
                arguments = [command, "--help"] if command else ["--help"]
                self.assertIn("usage:", self.invoke(*arguments).stdout.lower())

    def test_unknown_command_and_missing_argument_are_usage_errors(self):
        self.invoke("invented-command", expected=2)
        self.invoke("snapshot", "--source", self.skill, expected=2)

    def test_exact_bytes_unicode_paths_and_independent_package_digest(self):
        self.write("references/café 日本語.md", "# Café\r\n\r\nRésumé 日本語.\r\n")
        self.write("assets/binary.dat", bytes(range(256)) + b"\x00\r\n\xff")
        expected_rows = []
        for path in sorted(self.skill.rglob("*")):
            if path.is_file():
                data = path.read_bytes()
                expected_rows.append({"path": path.relative_to(self.skill).as_posix(), "bytes": len(data), "sha256": sha256(data)})
        expected_rows.sort(key=lambda row: row["path"])
        output, observation = self.snapshot()
        json.loads(observation.stdout)
        manifest = json.loads((output / "source-manifest.json").read_text(encoding="utf-8"))
        self.assertEqual(expected_rows, manifest["files"])
        canonical = json.dumps(expected_rows, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
        self.assertEqual(sha256(canonical), manifest["package_digest"])
        self.assertTrue(manifest["complete"])
        for row in expected_rows:
            self.assertEqual((self.skill / row["path"]).read_bytes(), (output / "source" / row["path"]).read_bytes())

    def test_readback_detects_changed_added_and_removed_files(self):
        output, _ = self.snapshot()
        manifest = output / "source-manifest.json"
        original = (self.skill / "SKILL.md").read_bytes()
        match = self.invoke("readback", "--source", self.skill, "--manifest", manifest)
        self.assertEqual("MATCH", json.loads(match.stdout)["status"])
        scenarios = (
            ("changed", lambda: self.write("SKILL.md", original + b"changed\n")),
            ("added", lambda: self.write("new.md", b"new\n")),
            ("removed", lambda: (self.skill / "SKILL.md").unlink()),
        )
        for label, change in scenarios:
            with self.subTest(change=label):
                self.write("SKILL.md", original)
                (self.skill / "new.md").unlink(missing_ok=True)
                change()
                result = self.invoke("readback", "--source", self.skill, "--manifest", manifest, expected=1)
                self.assertEqual("SOURCE_CHANGED", json.loads(result.stdout)["status"])

    def test_existing_snapshot_output_is_rejected_without_overwrite(self):
        output = self.root / "already there"
        output.mkdir()
        marker = output / "keep.bin"
        marker.write_bytes(b"original")
        self.invoke("snapshot", "--source", self.skill, "--output", output, expected=2)
        self.assertEqual(["keep.bin"], sorted(path.name for path in output.iterdir()))
        self.assertEqual(b"original", marker.read_bytes())

    def test_duplicate_manifest_keys_are_rejected(self):
        output, _ = self.snapshot()
        manifest = output / "source-manifest.json"
        text = manifest.read_text(encoding="utf-8").rstrip()
        manifest.write_text(text[:-1] + ',"package_digest":"' + "0" * 64 + '"}', encoding="utf-8")
        self.invoke("readback", "--source", self.skill, "--manifest", manifest, expected=2)

    def test_manifest_path_traversal_is_rejected(self):
        output, _ = self.snapshot()
        manifest = output / "source-manifest.json"
        data = json.loads(manifest.read_text(encoding="utf-8"))
        data["files"][0]["path"] = "../outside.txt"
        data["package_digest"] = sha256(json.dumps(data["files"], ensure_ascii=False, separators=(",", ":")).encode("utf-8"))
        manifest.write_text(json.dumps(data), encoding="utf-8")
        self.invoke("readback", "--source", self.skill, "--manifest", manifest, expected=2)

    def test_nested_snapshot_output_is_rejected_before_creation(self):
        output = self.skill / "nested" / "snapshot"
        before = (self.skill / "SKILL.md").read_bytes()
        self.invoke("snapshot", "--source", self.skill, "--output", output, expected=2)
        self.assertFalse(output.exists())
        self.assertEqual(before, (self.skill / "SKILL.md").read_bytes())

    def test_ancestor_output_is_rejected(self):
        self.invoke("snapshot", "--source", self.skill, "--output", self.root, expected=2)
        self.assertFalse((self.root / "source-manifest.json").exists())

    def test_missing_source_and_manifest_are_execution_errors(self):
        self.invoke("snapshot", "--source", self.root / "absent", "--output", self.root / "output", expected=2)
        self.invoke("structure", "--source", self.root / "absent", expected=2)
        self.invoke("readback", "--source", self.skill, "--manifest", self.root / "absent.json", expected=2)

    def test_backup_and_legacy_boundaries_are_explicitly_incomplete(self):
        self.write("backup/private.txt", "must not copy")
        self.write("devforgeai_cli/private.txt", "must not copy")
        output, _ = self.snapshot(expected=1)
        manifest = json.loads((output / "source-manifest.json").read_text(encoding="utf-8"))
        self.assertFalse(manifest["complete"])
        self.assertTrue(manifest["excluded_boundaries"])
        self.assertEqual(["SKILL.md"], [row["path"] for row in manifest["files"]])
        self.assertFalse((output / "source" / "backup").exists())
        self.assertFalse((output / "source" / "devforgeai_cli").exists())

    def test_file_count_ceiling_cannot_silently_truncate(self):
        for number in range(2000):
            self.write(f"files/{number:04}.txt", b"")
        output, result = self.snapshot(expected=2)
        if (output / "source-manifest.json").exists():
            manifest = json.loads((output / "source-manifest.json").read_text(encoding="utf-8"))
            self.assertFalse(manifest["complete"])
        self.assertTrue(result.stderr.strip() or result.stdout.strip())

    def test_byte_ceiling_cannot_silently_truncate(self):
        path = self.skill / "oversize.dat"
        with path.open("wb") as handle:
            handle.truncate(32 * 1024 * 1024 + 1)
        output, _ = self.snapshot(expected=2)
        if (output / "source-manifest.json").exists():
            manifest = json.loads((output / "source-manifest.json").read_text(encoding="utf-8"))
            self.assertFalse(manifest["complete"])

    def test_symlink_omission_when_host_supports_creation(self):
        secret = self.root / "outside.txt"
        secret.write_text("outside selected boundary", encoding="utf-8")
        try:
            (self.skill / "outside-link.txt").symlink_to(secret)
        except (OSError, NotImplementedError) as error:
            self.skipTest(f"Host does not permit symlink fixture creation: {error}")
        output, _ = self.snapshot(expected=1)
        self.assertFalse((output / "source" / "outside-link.txt").exists())
        self.assertFalse(json.loads((output / "source-manifest.json").read_text(encoding="utf-8"))["complete"])

    def test_minimal_instruction_only_skill_passes_without_optional_folders(self):
        before = (self.skill / "SKILL.md").read_bytes()
        result = self.invoke("structure", "--source", self.skill)
        json.loads(result.stdout)
        self.assertEqual(["SKILL.md"], sorted(path.name for path in self.skill.iterdir()))
        self.assertEqual(before, (self.skill / "SKILL.md").read_bytes())

    def test_invalid_yaml_reports_mismatch(self):
        self.write("SKILL.md", "---\nname: [unterminated\ndescription: test\n---\n# Broken\n")
        self.invoke("structure", "--source", self.skill, expected=1)

    def test_absent_required_metadata_reports_mismatch(self):
        for content in ("# No frontmatter\n", "---\nname: example\n---\n# Missing description\n", "---\ndescription: test\n---\n# Missing name\n"):
            with self.subTest(content=content):
                self.write("SKILL.md", content)
                self.invoke("structure", "--source", self.skill, expected=1)

    def test_required_metadata_types_report_mismatch(self):
        for content in ("---\nname: [example]\ndescription: test\n---\n", "---\nname: example\ndescription: 25\n---\n", "---\nname: example\ndescription: ''\n---\n"):
            with self.subTest(content=content):
                self.write("SKILL.md", content)
                self.invoke("structure", "--source", self.skill, expected=1)

    def test_absent_entrypoint_reports_mismatch(self):
        (self.skill / "SKILL.md").unlink()
        self.invoke("structure", "--source", self.skill, expected=1)

    def test_valid_relative_link_and_heading_anchor(self):
        self.write("references/guide.md", "# Guide\n\n## Named outcome\n\nReturn the result.\n")
        self.write("SKILL.md", VALID_SKILL + "\nRead [the guide](references/guide.md#named-outcome).\n")
        self.invoke("structure", "--source", self.skill)

    def test_missing_local_resource_reports_mismatch(self):
        self.write("SKILL.md", VALID_SKILL + "\nRead [absent](references/missing.md).\n")
        self.invoke("structure", "--source", self.skill, expected=1)

    def test_absent_heading_anchor_reports_mismatch(self):
        self.write("references/guide.md", "# Guide\n\n## Real heading\n")
        self.write("SKILL.md", VALID_SKILL + "\nRead [guide](references/guide.md#not-a-heading).\n")
        self.invoke("structure", "--source", self.skill, expected=1)

    def test_duplicate_json_keys_are_record_mismatches(self):
        run = self.root / "records"
        run.mkdir()
        (run / "findings.json").write_text('{"schema_version":"1","findings":[],"findings":[]}', encoding="utf-8")
        self.invoke("records", "--run-root", run, expected=1)

    def records_fixture(self):
        run = self.root / "records"
        run.mkdir()
        checks = []
        for dimension in ("standards", "workflow", "instructions", "behavior"):
            checks.append({"schema_version": "1", "run_id": "synthetic", "check_id": dimension,
                           "rule_id": "R-test", "subject_path": "SKILL.md", "method": "deterministic",
                           "required": True, "applicability": "applicable", "result": "PASS",
                           "reason": "Synthetic independent observation", "evidence": [], "dimension": dimension})
        self.save_checks(run, checks)
        return run, checks

    def save_checks(self, run, checks):
        (run / "checks.jsonl").write_text("".join(json.dumps(row) + "\n" for row in checks), encoding="utf-8")

    def save_record(self, run, filename, record):
        (run / filename).write_text(json.dumps(record, ensure_ascii=False, indent=2), encoding="utf-8")

    def test_records_valid_required_checks_and_references(self):
        run, checks = self.records_fixture()
        observation = b"factual source observation\n"
        (run / "observation.txt").write_bytes(observation)
        checks[0]["evidence"] = [{"path": "observation.txt", "sha256": sha256(observation)}]
        self.save_checks(run, checks)
        result = json.loads(self.invoke("records", "--run-root", run).stdout)
        self.assertEqual("PASS", result["overall_assessment"])
        self.assertEqual(4, result["required_coverage"]["required_evaluated"])
        self.assertEqual(4, result["required_coverage"]["required_total"])

    def test_records_missing_and_changed_reference_bytes(self):
        run, checks = self.records_fixture()
        checks[0]["evidence"] = [{"path": "observation.txt", "sha256": sha256(b"expected\n")}]
        self.save_checks(run, checks)
        self.invoke("records", "--run-root", run, expected=1)
        (run / "observation.txt").write_bytes(b"changed\n")
        self.invoke("records", "--run-root", run, expected=1)

    def test_findings_identity_uses_full_independent_hash_and_deduplicates(self):
        run, _ = self.records_fixture()
        identity = ["R-test", "SKILL.md", "MISSING_FILE", 0]
        finding_id = "F-" + sha256(json.dumps(identity, ensure_ascii=False, separators=(",", ":")).encode("utf-8"))
        finding = {"finding_id": finding_id, "identity": identity, "rule_id": "R-test", "subject_path": "SKILL.md",
                   "category": "resource/tool issues", "severity": "major", "source_refs": [],
                   "observation_refs": [], "description": "A required entrypoint is absent.",
                   "user_impact": "The workflow cannot be loaded.", "proposed_correction": "Restore the entrypoint after review.",
                   "preserved_requirements": ["review before repair"], "verification_cases": ["entrypoint exists"], "disposition": "proposed"}
        document = {"schema_version": "1", "run_id": "synthetic", "target_name": "example", "findings": [finding]}
        self.save_record(run, "findings.json", document)
        self.invoke("records", "--run-root", run)
        finding["finding_id"] = "F-" + "0" * 64
        self.save_record(run, "findings.json", document)
        self.invoke("records", "--run-root", run, expected=1)
        finding["finding_id"] = finding_id
        document["findings"].append(dict(finding))
        self.save_record(run, "findings.json", document)
        self.invoke("records", "--run-root", run, expected=1)

    def test_fail_precedes_incomplete_and_coverage_stays_visible(self):
        run, checks = self.records_fixture()
        checks[1]["result"] = "FAIL"
        checks[3]["result"] = "NOT_RUN"
        checks[3]["reason"] = "Required runner unavailable"
        self.save_checks(run, checks)
        result = json.loads(self.invoke("records", "--run-root", run).stdout)
        self.assertEqual("FAIL", result["overall_assessment"])
        self.assertEqual("FAIL", result["dimensions"]["workflow"]["outcome"])
        self.assertEqual("INCOMPLETE", result["dimensions"]["behavior"]["outcome"])
        self.assertIn("behavior", result["required_coverage"]["incomplete_check_ids"])
        self.assertEqual(3, result["required_coverage"]["required_evaluated"])
        self.assertEqual(4, result["required_coverage"]["required_total"])

    def test_false_pass_declared_assessment_is_mismatch(self):
        run, checks = self.records_fixture()
        checks[1]["result"] = "FAIL"
        self.save_checks(run, checks)
        self.save_record(run, "assessment.json", {"overall_assessment": "PASS", "dimensions": {row["dimension"]: "PASS" for row in checks}})
        self.invoke("records", "--run-root", run, expected=1)

    def test_unknown_applicability_cannot_be_not_applicable(self):
        run, checks = self.records_fixture()
        checks[0].update(applicability="unknown", result="NOT_APPLICABLE")
        self.save_checks(run, checks)
        self.invoke("records", "--run-root", run, expected=1)
        checks[0]["result"] = "NOT_RUN"
        self.save_checks(run, checks)
        result = json.loads(self.invoke("records", "--run-root", run).stdout)
        self.assertEqual("INCOMPLETE", result["overall_assessment"])

    def test_source_changed_keeps_assessment_incomplete(self):
        run, _ = self.records_fixture()
        self.save_record(run, "origin-record.json", {"source_readback_state": "SOURCE_CHANGED", "history_kind": "observed"})
        result = json.loads(self.invoke("records", "--run-root", run).stdout)
        self.assertEqual("INCOMPLETE", result["overall_assessment"])

    def test_claimed_generated_history_requires_evidence(self):
        run, _ = self.records_fixture()
        self.save_record(run, "origin-record.json", {"source_readback_state": "UNCHANGED", "history_kind": "generated", "prior_evidence": None})
        self.invoke("records", "--run-root", run, expected=1)

    def test_ready_requires_current_review_bound_to_proposal_and_target(self):
        run, _ = self.records_fixture()
        proposal = b"# Proposed behavior\n"
        baseline = b"synthetic baseline evidence; semantic history verification separate\n"
        (run / "proposal.md").write_bytes(proposal)
        (run / "baseline.txt").write_bytes(baseline)
        self.save_record(run, "origin-record.json", {"source_readback_state": "UNCHANGED", "history_kind": "observed"})
        handoff = {"builder_readiness": "READY", "proposal_review_state": "approved", "review_instruction": "Synthetic authorization for these exact bytes",
                   "selected_finding_ids": [], "deferred_finding_ids": [], "adoption_required": False,
                   "baseline_reference": {"path": "baseline.txt", "sha256": sha256(baseline)},
                   "proposed_spec": {"path": "proposal.md", "sha256": sha256(proposal)},
                   "target_package_digest": "a" * 64,
                   "review_authorization": {"proposal_sha256": sha256(proposal), "target_package_digest": "a" * 64}}
        self.save_record(run, "handoff.json", handoff)
        self.invoke("records", "--run-root", run)
        for field, wrong in (("proposal_sha256", "b" * 64), ("target_package_digest", "c" * 64)):
            with self.subTest(changed=field):
                original = handoff["review_authorization"][field]
                handoff["review_authorization"][field] = wrong
                self.save_record(run, "handoff.json", handoff)
                self.invoke("records", "--run-root", run, expected=1)
                handoff["review_authorization"][field] = original
        handoff["proposal_review_state"] = "pending"
        self.save_record(run, "handoff.json", handoff)
        self.invoke("records", "--run-root", run, expected=1)

    def test_pending_review_is_distinct_from_assessment_and_not_ready(self):
        run, _ = self.records_fixture()
        self.save_record(run, "handoff.json", {"builder_readiness": "REVIEW_REQUIRED", "proposal_review_state": "pending", "selected_finding_ids": [], "deferred_finding_ids": []})
        self.invoke("records", "--run-root", run)


if __name__ == "__main__":
    unittest.main()
