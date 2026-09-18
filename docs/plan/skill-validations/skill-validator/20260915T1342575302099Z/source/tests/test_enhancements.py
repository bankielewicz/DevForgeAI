"""Regression tests for v2 evidence using disposable synthetic snapshots."""

from __future__ import annotations

import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

from fixture_data import build_candidate, build_revision, file_ref, files, sha, write, write_json


PACKAGE = Path(__file__).resolve().parents[1]
PROFILES = {
    "legacy-import-v1": {"package_links", "manifest_accounting"},
    "import-v2": {"package_links", "manifest_accounting", "build_traceability"},
    "spec-v1": {"package_links", "build_traceability"},
    "revision-import-v2": {"package_links", "manifest_accounting", "build_traceability", "revision_consistency"},
    "revision-spec-v1": {"package_links", "build_traceability", "revision_consistency"},
    "builder-v2": {"package_links", "manifest_accounting", "build_traceability", "revision_consistency", "routing_outcomes"},
}


class EnhancementTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory(prefix="builder-enhancement-test-")
        self.addCleanup(temporary.cleanup)
        self.base = Path(temporary.name)
        self.package = self.base / "builder"
        shutil.copytree(PACKAGE, self.package, ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
        self.root = self.base / "candidate"
        self.params = build_candidate(self.root, sha((self.package / "evals/build-manifest.json").read_bytes()))
        self.serial = 0

    def run_command(self, script, arguments):
        return subprocess.run(
            [sys.executable, "-B", "-X", "utf8", str(self.package / "scripts" / script), *arguments],
            capture_output=True, text=True, encoding="utf-8", timeout=30, check=False,
            env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
        )

    def evaluate(self, profile="builder-v2", *, grader_ids=None, supplied_profile=True):
        self.serial += 1
        selected = PROFILES.get(profile, PROFILES["builder-v2"]) if grader_ids is None else grader_ids
        cases = [{"case_id": grader, "grader_id": grader, "params": self.params[grader], "expected": "PASS"}
                 for grader in sorted(selected)]
        case_path = self.base / f"cases-{self.serial}.jsonl"
        write(case_path, "".join(json.dumps(case) + "\n" for case in cases))
        output = self.base / f"results-{self.serial}.jsonl"
        args = ["--package-root", str(self.package), "--candidate-root", str(self.root),
                "--cases", str(case_path), "--output", str(output), "--run-id", "enhancement-test"]
        if supplied_profile:
            args += ["--profile", profile]
        completed = self.run_command("run_evaluation.py", args)
        records = [json.loads(line) for line in output.read_text(encoding="utf-8").splitlines()] if output.exists() else []
        return completed, records

    def assert_pass(self, result):
        completed, records = result
        self.assertEqual(completed.returncode, 0, completed.stdout + completed.stderr + repr(records))
        self.assertTrue(records)
        self.assertTrue(all(r["status"] == "PASS" and r["expectation_met"] for r in records), records)
        return records

    def assert_rejected(self, result, grader=None, status=None):
        completed, records = result
        self.assertIn(completed.returncode, (1, 2), completed.stdout + completed.stderr + repr(records))
        self.assertTrue(records or completed.stderr.strip(), "Rejection requires a diagnostic.")
        if grader:
            selected = [r for r in records if r.get("grader_id") == grader]
            self.assertEqual(len(selected), 1, records)
            self.assertIn(selected[0]["status"], ("FAIL", "ERROR"), selected)
            self.assertFalse(selected[0]["expectation_met"], selected)
            if status:
                self.assertEqual(selected[0]["status"], status, selected)
        elif status:
            self.assertTrue(any(r.get("status") == status for r in records), records)

    def load(self, relative):
        return json.loads((self.root / relative).read_text(encoding="utf-8"))

    def contract_change(self, change):
        path = self.root / "trace/evidence/build-contract.json"
        contract = self.load("trace/evidence/build-contract.json")
        change(contract)
        write_json(path, contract)
        self.provenance_change(lambda value: value.update(contract_sha256=sha(path.read_bytes())))

    def provenance_change(self, change):
        path = self.root / "trace/evidence/build-provenance.json"
        value = self.load("trace/evidence/build-provenance.json")
        change(value)
        write_json(path, value)

    def plan_change(self, change):
        path = self.root / "revision/revision-plan.json"
        value = self.load("revision/revision-plan.json")
        change(value)
        write_json(path, value)

    def trace_rejected(self, status=None):
        self.assert_rejected(self.evaluate("spec-v1"), "build_traceability", status)

    def revision_rejected(self, status=None):
        self.assert_rejected(self.evaluate("revision-spec-v1"), "revision_consistency", status)

    def new_revision(self, baseline, current, candidate, **kwargs):
        # Delete only this test's known, private fixture subtree.
        revision = self.root / "revision"
        self.assertEqual(revision.resolve().parent, self.root.resolve())
        shutil.rmtree(revision)
        return build_revision(self.root, baseline, current, candidate, **kwargs)

    def test_every_profile_has_exact_required_graders_and_v2_evidence(self):
        for profile, expected in PROFILES.items():
            with self.subTest(profile=profile):
                records = self.assert_pass(self.evaluate(profile))
                self.assertEqual({r["grader_id"] for r in records}, expected)
                self.assertTrue(all(r["schema_version"] == "2" and r["profile"] == profile for r in records))
                self.assertTrue(all(isinstance(r["profile_version"], str) and r["profile_version"] for r in records))

    def test_omitted_profile_preserves_legacy_case_shape(self):
        records = self.assert_pass(self.evaluate("legacy-import-v1", supplied_profile=False))
        self.assertEqual({r["grader_id"] for r in records}, PROFILES["legacy-import-v1"])
        self.assertTrue(all(r["profile"] == "legacy-import-v1" and r["schema_version"] == "2" for r in records))

    def test_every_profile_rejects_an_omitted_required_grader(self):
        for profile, graders in PROFILES.items():
            with self.subTest(profile=profile):
                self.assert_rejected(self.evaluate(profile, grader_ids=graders - {sorted(graders)[-1]}), status="ERROR")

    def test_profile_rejects_extra_grader(self):
        self.assert_rejected(self.evaluate("spec-v1", grader_ids=PROFILES["builder-v2"]), status="ERROR")

    def test_unknown_profile_is_configuration_error(self):
        completed, records = self.evaluate("unknown-v7")
        self.assertEqual(completed.returncode, 2)
        self.assertTrue(records or completed.stderr)

    def test_tampered_profile_artifact_is_rejected(self):
        write(self.package / "evals/profiles.json", "{}\n")
        self.assert_rejected(self.evaluate("spec-v1"), status="ERROR")

    def test_input_mutation_is_observed(self):
        write(self.root / "trace/input.md", "Source changed after the contract was captured.\n")
        self.trace_rejected("FAIL")

    def test_input_byte_count_mismatch_is_observed(self):
        self.contract_change(lambda value: value["inputs"][0].update(bytes=0))
        self.trace_rejected()

    def test_excerpt_digest_mismatch_is_observed(self):
        self.contract_change(lambda value: value["requirements"][0]["source_refs"][0].update(sha256="0" * 64))
        self.trace_rejected("FAIL")

    def test_out_of_range_excerpt_is_rejected(self):
        self.contract_change(lambda value: value["requirements"][0]["source_refs"][0].update(end_byte=100000))
        self.trace_rejected()

    def test_negative_excerpt_start_is_rejected(self):
        self.contract_change(lambda value: value["requirements"][0]["source_refs"][0].update(start_byte=-1))
        self.trace_rejected()

    def test_unknown_excerpt_input_is_rejected(self):
        self.contract_change(lambda value: value["requirements"][0]["source_refs"][0].update(input_id="unrecorded"))
        self.trace_rejected()

    def test_duplicate_requirement_ids_are_rejected(self):
        self.contract_change(lambda value: value["requirements"].append(dict(value["requirements"][0])))
        self.trace_rejected()

    def test_missing_requirement_ids_are_rejected(self):
        self.contract_change(lambda value: value["requirements"].clear())
        self.trace_rejected()

    def test_unknown_artifact_requirement_id_is_rejected(self):
        self.contract_change(lambda value: value["artifacts"][0].update(requirement_ids=["unrecorded"]))
        self.trace_rejected()

    def test_requirement_mapping_must_agree_in_both_directions(self):
        self.contract_change(lambda value: value["requirements"][0].update(artifact_paths=["SKILL.md"]))
        self.trace_rejected()

    def test_missing_output_is_rejected(self):
        (self.root / "trace/destination/schema.json").unlink()
        self.trace_rejected("FAIL")

    def test_stale_output_digest_is_rejected(self):
        write(self.root / "trace/destination/schema.json", '{"type":"array"}\n')
        self.trace_rejected("FAIL")

    def test_unknown_extra_destination_file_is_rejected(self):
        write(self.root / "trace/destination/unrecorded.txt", "Unrecorded output.\n")
        self.trace_rejected("FAIL")

    def test_missing_baseline_file_is_rejected(self):
        (self.root / "trace/baseline/schema.json").unlink()
        self.trace_rejected()

    def test_stale_contract_digest_is_rejected(self):
        self.provenance_change(lambda value: value.update(contract_sha256="0" * 64))
        self.trace_rejected("FAIL")

    def test_stale_builder_digest_is_rejected(self):
        self.provenance_change(lambda value: value.update(builder_manifest_sha256="0" * 64))
        self.trace_rejected("FAIL")

    def test_missing_evaluation_mapping_is_rejected(self):
        self.provenance_change(lambda value: value["mappings"][0].update(evidence_ids=[]))
        self.trace_rejected()

    def test_unknown_evaluation_mapping_is_rejected(self):
        self.provenance_change(lambda value: value["mappings"][0].update(evidence_ids=["absent"]))
        self.trace_rejected()

    def test_evaluation_from_different_run_is_rejected(self):
        path = self.root / "trace/evidence/construction-observation.json"
        value = self.load("trace/evidence/construction-observation.json")
        value["run_id"] = "different-run"
        write_json(path, value)
        self.provenance_change(lambda item: item["evidence"][0].update(sha256=sha(path.read_bytes())))
        self.trace_rejected("FAIL")

    def test_evaluation_from_different_target_is_rejected(self):
        path = self.root / "trace/evidence/construction-observation.json"
        value = self.load("trace/evidence/construction-observation.json")
        value["target_name"] = "different-skill"
        write_json(path, value)
        self.provenance_change(lambda item: item["evidence"][0].update(sha256=sha(path.read_bytes())))
        self.trace_rejected("FAIL")

    def test_evidence_with_duplicate_json_keys_is_rejected(self):
        write(self.root / "trace/evidence/build-provenance.json", '{"schema_version":"1","schema_version":"2"}\n')
        self.trace_rejected("ERROR")

    def test_authorization_must_identify_current_input_hash(self):
        self.contract_change(lambda value: value["authorization"]["inputs"][0].update(sha256="0" * 64))
        self.trace_rejected()

    def test_regeneration_preserves_user_edit_when_generation_is_unchanged(self):
        self.new_revision({"SKILL.md": b"B"}, {"SKILL.md": b"USER", "notes": b"unrelated"}, {"SKILL.md": b"B"})
        self.assert_pass(self.evaluate("revision-spec-v1"))
        self.assertEqual((self.root / "revision/after/SKILL.md").read_bytes(), b"USER")
        self.assertEqual((self.root / "revision/after/notes").read_bytes(), b"unrelated")

    def test_regeneration_keeps_current_when_already_equal_to_candidate(self):
        plan = self.new_revision({"SKILL.md": b"B"}, {"SKILL.md": b"N"}, {"SKILL.md": b"N"})
        self.assertEqual(plan["rows"][0]["action"], "KEEP_CURRENT")
        self.assert_pass(self.evaluate("revision-spec-v1"))

    def test_regeneration_uses_new_when_current_matches_baseline(self):
        plan = self.load("revision/revision-plan.json")
        self.assertEqual(next(row for row in plan["rows"] if row["path"] == "SKILL.md")["action"], "USE_NEW")
        self.assert_pass(self.evaluate("revision-spec-v1"))

    def test_new_unoccupied_generated_file_can_be_added(self):
        plan = self.new_revision({}, {}, {"SKILL.md": b"new"})
        self.assertEqual(plan["rows"][0]["action"], "USE_NEW")
        self.assert_pass(self.evaluate("revision-spec-v1"))

    def test_equal_baseline_current_candidate_uses_first_matching_rule(self):
        plan = self.new_revision({"SKILL.md": b"same"}, {"SKILL.md": b"same"}, {"SKILL.md": b"same"})
        self.assertEqual(plan["rows"][0]["action"], "USE_NEW")
        self.assertEqual(plan["applied_paths"], [])
        self.assert_pass(self.evaluate("revision-spec-v1"))

    def test_divergent_owned_edits_produce_no_delta_conflict(self):
        plan = self.new_revision({"SKILL.md": b"B"}, {"SKILL.md": b"C"}, {"SKILL.md": b"N"})
        self.assertEqual(plan["status"], "CONFLICT")
        self.assert_pass(self.evaluate("revision-spec-v1"))
        self.assertEqual(files(self.root / "revision/current"), files(self.root / "revision/after"))

    def test_identical_unowned_collision_still_conflicts(self):
        plan = self.new_revision({}, {"SKILL.md": b"same"}, {"SKILL.md": b"same"})
        self.assertEqual(plan["status"], "CONFLICT")
        self.assert_pass(self.evaluate("revision-spec-v1"))

    def test_unmodified_obsolete_owned_file_can_be_removed(self):
        self.new_revision({"SKILL.md": b"B", "obsolete": b"old"},
                          {"SKILL.md": b"B", "obsolete": b"old"}, {"SKILL.md": b"N"})
        self.assert_pass(self.evaluate("revision-spec-v1"))
        self.assertFalse((self.root / "revision/after/obsolete").exists())

    def test_modified_obsolete_owned_file_conflicts(self):
        plan = self.new_revision({"SKILL.md": b"B", "obsolete": b"old"},
                                 {"SKILL.md": b"B", "obsolete": b"user"}, {"SKILL.md": b"N"})
        self.assertEqual(plan["status"], "CONFLICT")
        self.assert_pass(self.evaluate("revision-spec-v1"))

    def test_missing_required_candidate_artifact_is_rejected(self):
        self.new_revision({"SKILL.md": b"B"}, {"SKILL.md": b"B"}, {})
        self.revision_rejected()

    def test_required_result_cannot_preserve_a_user_deletion(self):
        plan = self.new_revision({"SKILL.md": b"B"}, {}, {"SKILL.md": b"B"})
        self.assertEqual(plan["status"], "CONFLICT")
        self.assert_pass(self.evaluate("revision-spec-v1"))

    def test_conflicted_run_cannot_modify_destination(self):
        self.new_revision({"SKILL.md": b"B"}, {"SKILL.md": b"C"}, {"SKILL.md": b"N"})
        write(self.root / "revision/after/SKILL.md", b"N")
        self.plan_change(lambda value: value.update(applied_paths=["SKILL.md"]))
        self.revision_rejected("FAIL")

    def test_plan_rows_cannot_claim_a_different_comparison_action(self):
        self.plan_change(lambda value: value["rows"][0].update(action="KEEP_CURRENT"))
        self.revision_rejected("FAIL")

    def test_unrelated_file_mutation_is_rejected(self):
        write(self.root / "revision/after/personal.txt", "Unexpected user-file change.\n")
        self.plan_change(lambda value: value.update(applied_paths=["SKILL.md", "personal.txt"]))
        self.revision_rejected("FAIL")

    def test_partial_application_records_exact_delta_without_baseline_advance(self):
        self.new_revision({"SKILL.md": b"B", "two": b"B2"},
                          {"SKILL.md": b"B", "two": b"B2"}, {"SKILL.md": b"N", "two": b"N2"}, status="PLANNED")
        write(self.root / "revision/after/SKILL.md", b"N")
        self.plan_change(lambda value: value.update(status="PARTIAL", applied_paths=["SKILL.md"], readback_passed=False))
        self.assert_pass(self.evaluate("revision-spec-v1"))

    def test_partial_application_cannot_publish_successful_baseline(self):
        self.plan_change(lambda value: value.update(status="PARTIAL", baseline_advanced=True, readback_passed=False))
        self.revision_rejected("FAIL")

    def test_applied_delta_cannot_omit_a_changed_path(self):
        self.plan_change(lambda value: value.update(applied_paths=[]))
        self.revision_rejected("FAIL")

    def test_applied_result_requires_evaluation_and_readback(self):
        self.plan_change(lambda value: value.update(evaluation_passed=False))
        self.revision_rejected("FAIL")

    def test_successful_baseline_publication_matches_new_generated_bytes(self):
        self.new_revision({"SKILL.md": b"B"}, {"SKILL.md": b"B"}, {"SKILL.md": b"N"}, advance=True)
        self.assert_pass(self.evaluate("revision-spec-v1"))

    def test_changed_pointer_cannot_be_reported_as_unadvanced(self):
        path = self.root / "revision/pointer-after.json"
        write_json(path, {"run_id": "unexpected", "baseline": []})
        self.plan_change(lambda value: value.update(baseline_after=file_ref(self.root, path)))
        self.revision_rejected("FAIL")

    def test_missing_previous_baseline_is_rejected(self):
        (self.root / "revision/previous-build.json").unlink()
        self.revision_rejected()

    def test_owned_paths_must_equal_previous_generated_baseline(self):
        self.plan_change(lambda value: value.update(owned_paths=[]))
        self.revision_rejected()

    def test_retry_does_not_redefine_baseline_after_partial_application(self):
        self.new_revision({"SKILL.md": b"B", "two": b"B2"},
                          {"SKILL.md": b"B", "two": b"B2"}, {"SKILL.md": b"N", "two": b"N2"}, status="PLANNED")
        write(self.root / "revision/after/SKILL.md", b"N")
        self.plan_change(lambda value: value.update(status="PARTIAL", applied_paths=["SKILL.md"]))
        partial = self.load("revision/revision-plan.json")
        for key in ("baseline", "current", "candidate", "after"):
            shutil.copytree(self.root / "revision" / key, self.root / "history" / key)
            partial[key] = "history/" + key
        write_json(self.root / "history/partial-plan.json", partial)
        self.new_revision({"SKILL.md": b"B", "two": b"B2"},
                          {"SKILL.md": b"N", "two": b"B2"}, {"SKILL.md": b"N", "two": b"N2"})
        self.plan_change(lambda value: value.update(retry_of=file_ref(self.root, self.root / "history/partial-plan.json")))
        self.assert_pass(self.evaluate("revision-spec-v1"))
        self.assertEqual((self.root / "revision/baseline/SKILL.md").read_bytes(), b"B")

    def test_routing_difference_fails(self):
        path = self.root / "routing/observed.jsonl"
        records = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()]
        records[0]["route"] = "unrelated"
        write(path, "".join(json.dumps(record) + "\n" for record in records))
        self.assert_rejected(self.evaluate(), "routing_outcomes", "FAIL")

    def test_missing_routing_result_is_error(self):
        path = self.root / "routing/observed.jsonl"
        write(path, "\n".join(path.read_text(encoding="utf-8").splitlines()[1:]) + "\n")
        self.assert_rejected(self.evaluate(), "routing_outcomes", "ERROR")

    def test_duplicate_routing_result_is_error(self):
        path = self.root / "routing/observed.jsonl"
        value = path.read_text(encoding="utf-8")
        write(path, value + value.splitlines()[0] + "\n")
        self.assert_rejected(self.evaluate(), "routing_outcomes", "ERROR")

    def test_unknown_route_is_error(self):
        path = self.root / "routing/observed.jsonl"
        records = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()]
        records[0]["route"] = "invented-phase"
        write(path, "".join(json.dumps(record) + "\n" for record in records))
        self.assert_rejected(self.evaluate(), "routing_outcomes", "ERROR")

    def test_explicit_spec_resolution_selects_supplied_file(self):
        project = self.base / "project"
        path = project / "docs/plan/explicit.md"
        write(path, "# Explicitly selected specification\n")
        completed = self.run_command("build_evidence.py", ["resolve-spec", "--project-root", str(project), "--spec", str(path)])
        self.assertEqual(completed.returncode, 0, completed.stdout + completed.stderr)
        self.assertIn(str(path.name), completed.stdout)

    def test_named_spec_resolution_searches_both_directories(self):
        project = self.base / "project"
        write(project / "docs/design/specs/found.md", "---\nskill_name: synthetic-total\n---\nDomain contract.\n")
        completed = self.run_command("build_evidence.py", ["resolve-spec", "--project-root", str(project), "--name", "synthetic-total"])
        self.assertEqual(completed.returncode, 0, completed.stdout + completed.stderr)
        self.assertIn("found.md", completed.stdout)

    def test_missing_named_spec_produces_gap(self):
        project = self.base / "project"
        project.mkdir()
        completed = self.run_command("build_evidence.py", ["resolve-spec", "--project-root", str(project), "--name", "absent"])
        self.assertEqual(completed.returncode, 1, completed.stdout + completed.stderr)
        self.assertIn("MISSING_INPUT", completed.stdout)

    def test_duplicate_named_specs_report_ambiguity_without_precedence(self):
        project = self.base / "project"
        for path in ("docs/plan/a.md", "docs/design/specs/b.md"):
            write(project / path, "---\nskill_name: synthetic-total\n---\nDomain contract.\n")
        completed = self.run_command("build_evidence.py", ["resolve-spec", "--project-root", str(project), "--name", "synthetic-total"])
        self.assertEqual(completed.returncode, 1, completed.stdout + completed.stderr)
        self.assertIn("AMBIGUOUS_INPUT", completed.stdout)
        self.assertIn("a.md", completed.stdout)
        self.assertIn("b.md", completed.stdout)

    def test_resolver_excludes_backup_before_reading_invalid_content(self):
        project = self.base / "project"
        write(project / "docs/plan/backup/ignored.md", b"\xff\xfeInvalid excluded bytes")
        write(project / "docs/plan/found.md", "---\nskill_name: synthetic-total\n---\nDomain contract.\n")
        completed = self.run_command("build_evidence.py", ["resolve-spec", "--project-root", str(project), "--name", "synthetic-total"])
        self.assertEqual(completed.returncode, 0, completed.stdout + completed.stderr)

    def test_input_record_hashes_raw_crlf_byte_excerpt(self):
        path = self.base / "spec.md"
        data = b"Header\r\nExact excerpt\r\n"
        write(path, data)
        completed = self.run_command("build_evidence.py", ["input-record", "--file", str(path), "--id", "source", "--snapshot-path", "inputs/spec.md", "--start-byte", "8", "--end-byte", str(len(data))])
        self.assertEqual(completed.returncode, 0, completed.stdout + completed.stderr)
        value = json.loads(completed.stdout)
        self.assertEqual(value["input"]["sha256"], sha(data))
        self.assertEqual(value["input"]["bytes"], len(data))
        self.assertEqual(value["source_ref"]["sha256"], sha(data[8:]))

    def test_input_record_rejects_empty_excerpt(self):
        path = self.base / "spec.md"
        write(path, "Nonempty input.\n")
        completed = self.run_command("build_evidence.py", ["input-record", "--file", str(path), "--id", "source", "--snapshot-path", "inputs/spec.md", "--start-byte", "0", "--end-byte", "0"])
        self.assertEqual(completed.returncode, 2, completed.stdout + completed.stderr)

    def test_revision_preview_does_not_write_destination(self):
        self.new_revision({"SKILL.md": b"B"}, {"SKILL.md": b"B"}, {"SKILL.md": b"N"}, status="PLANNED")
        plan = self.load("revision/revision-plan.json")
        plan.pop("rows")
        write_json(self.root / "revision/request.json", plan)
        before = files(self.root / "revision/current")
        completed = self.run_command("build_evidence.py", ["revision-plan", "--snapshot-root", str(self.root), "--request", "revision/request.json"])
        self.assertEqual(completed.returncode, 0, completed.stdout + completed.stderr)
        preview = json.loads(completed.stdout)
        self.assertEqual(preview["status"], "PLANNED")
        self.assertEqual(files(self.root / "revision/current"), before)
        self.assertTrue(preview["rows"])


if __name__ == "__main__":
    unittest.main()
