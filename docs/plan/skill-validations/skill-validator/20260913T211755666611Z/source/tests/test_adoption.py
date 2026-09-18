"""Adoption/schema-2 invariants; fixtures are not claimed as task trials."""
import copy
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

from adoption_fixture import build_adoption, build_v2, rows
from fixture_data import build_revision, file_ref, files, sha, write, write_json

PACKAGE = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("adoption_test_graders", PACKAGE / "scripts/graders.py")
graders = importlib.util.module_from_spec(spec)
spec.loader.exec_module(graders)


class AdoptionTests(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory(prefix="builder-adoption-")
        self.addCleanup(temp.cleanup)
        self.base = Path(temp.name)
        self.root = self.base / "candidate"
        self.root.mkdir()
        self.serial = 0

    def load(self, path):
        return json.loads((self.root / path).read_text(encoding="utf-8"))

    def edit(self, path, change):
        value = self.load(path)
        change(value)
        write_json(self.root / path, value)
        return value

    def grade(self, grader="adoption_consistency"):
        params = {"evidence": "adoption/evidence", "destination": "adoption/destination"}
        if grader == "revision_consistency_v2":
            params = {"path": "trace/evidence/revision-plan.json"}
        if grader == "build_traceability_v2":
            params = {"evidence": "trace/evidence", "destination": "trace/destination"}
        return graders.grade(grader, self.root, params)

    def reject(self, grader="adoption_consistency"):
        try:
            result = self.grade(grader)
        except (ValueError, KeyError, TypeError, OSError):
            return
        self.assertEqual(result["status"], "FAIL", result)

    def revision(self, **kwargs):
        return build_v2(self.root, sha((PACKAGE / "evals/build-manifest.json").read_bytes()), **kwargs)

    def helper(self, operation, request):
        self.serial += 1
        path = f"request-{self.serial}.json"
        write_json(self.root / path, request)
        return subprocess.run([sys.executable, "-B", "-X", "utf8", str(PACKAGE / "scripts/build_evidence.py"), operation,
                               "--snapshot-root", str(self.root), "--request", path], capture_output=True, text=True, timeout=30)

    def test_a01_accounting_and_helper_leave_target_unchanged(self):
        record = build_adoption(self.root)
        before = files(self.root / "adoption/destination")
        proposal = copy.deepcopy(record)
        proposal.pop("retained_user_paths")
        proposal.pop("recording_state")
        proc = self.helper("adoption-plan", {"operation": "adopt", "record": proposal})
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertEqual(json.loads(proc.stdout), record)
        self.assertEqual(before, files(self.root / "adoption/destination"))
        self.assertEqual(self.grade()["status"], "PASS")

    def test_a02_quality_failure_does_not_become_a_pass(self):
        build_adoption(self.root)
        before = (self.root / "adoption/evidence/quality.json").read_bytes()
        self.assertEqual(self.grade()["status"], "PASS")
        self.assertEqual(before, (self.root / "adoption/evidence/quality.json").read_bytes())
        self.assertEqual(self.load("adoption/evidence/quality.json")["quality"], "FAILED")

    def test_a03_validation_operation_and_unbound_authorization_rejected(self):
        record = build_adoption(self.root)
        proc = self.helper("adoption-plan", {"operation": "validate", "record": record})
        self.assertEqual(proc.returncode, 2)
        record["authorization"]["managed_manifest_sha256"] = "0" * 64
        proc = self.helper("adoption-plan", {"operation": "adopt", "record": record})
        self.assertEqual(proc.returncode, 1)
        self.assertEqual(json.loads(proc.stdout)["record"]["recording_state"], "INCOMPLETE")

    def test_a04_identical_unowned_collision_is_conflict(self):
        self.assertEqual(graders.revision_action(False, None, "same", "same", False)[0], "CONFLICT")

    def test_a05_retained_edit_has_distinct_generated_baseline(self):
        plan = self.revision()
        # schema.json is unchanged between B and N; retain a current user edit.
        p = "schema.json"
        edited = b'{"type":"object","description":"User edit"}\n'
        write(self.root / "revision2/current" / p, edited)
        write(self.root / "trace/destination" / p, edited)
        row = next(r for r in plan["rows"] if r["path"] == p)
        row.update(c_sha256=sha(edited), action="KEEP_CURRENT")
        write_json(self.root / "trace/evidence/revision-plan.json", plan)
        self.assertEqual(self.grade("revision_consistency_v2")["status"], "PASS")
        self.assertNotEqual((self.root / "trace/baseline" / p).read_bytes(), edited)

    def test_a06_source_and_spec_and_snapshot_drift_rejected(self):
        record = build_adoption(self.root)
        for relative in ("adoption/destination/SKILL.md", "adoption/evidence/origin.md", "adoption/evidence/snapshot/SKILL.md"):
            with self.subTest(path=relative):
                p = self.root / relative
                original = p.read_bytes()
                p.write_bytes(original + b"drift")
                self.reject()
                p.write_bytes(original)
        self.edit(record["source_readback"]["path"], lambda v: v.update(spec_after_sha256="0" * 64))
        self.reject()

    def test_a06_stale_pointer_and_missing_pointer_refuse_revision(self):
        plan = self.revision()
        pointer = self.root / plan["baseline_before"]["path"]
        pointer.write_bytes(pointer.read_bytes() + b" ")
        self.reject("revision_consistency_v2")
        pointer.unlink()
        self.reject("build_traceability_v2")

    def test_a07_full_ordered_three_way_table(self):
        cases = [
            (True, "b", "b", "n", False, "USE_NEW", "n"),
            (True, "b", "n", "n", False, "KEEP_CURRENT", "n"),
            (True, "b", "c", "b", False, "KEEP_CURRENT", "c"),
            (True, "b", "c", "n", False, "CONFLICT", "c"),
            (True, "b", "b", "b", False, "USE_NEW", "b"),
            (True, "b", "b", None, False, "USE_NEW", None),
            (True, "b", "c", None, False, "CONFLICT", "c"),
            (True, "b", None, "b", True, "CONFLICT", None),
            (False, None, "user", None, False, "KEEP_CURRENT", "user"),
            (False, None, None, "new", False, "USE_NEW", "new"),
            (False, None, "new", "new", False, "CONFLICT", "new"),
            (True, sha(b""), sha(b""), None, False, "USE_NEW", None),
        ]
        for owned, b, c, n, required, action, selected in cases:
            with self.subTest(values=(owned, b, c, n, required)):
                self.assertEqual(graders.revision_action(owned, b, c, n, required), (action, selected))

    def test_a08_partial_actual_delta_and_retry_use_same_origin(self):
        plan = self.revision(status="PLANNED")
        target = self.root / "trace/destination"
        try:
            write(target / "SKILL.md", (self.root / "trace/baseline/SKILL.md").read_bytes())
            raise OSError("Injected failure after first successful write")
        except OSError:
            plan.update(status="PARTIAL", applied_paths=["SKILL.md"], readback_passed=False, evaluation_passed=False)
        write_json(self.root / "trace/evidence/revision-plan.json", plan)
        self.assertEqual(self.grade("revision_consistency_v2")["status"], "PASS")
        write_json(self.root / "trace/evidence/partial-plan.json", plan)
        retry = copy.deepcopy(plan)
        retry["retry_of"] = file_ref(self.root, self.root / "trace/evidence/partial-plan.json")
        write_json(self.root / "trace/evidence/revision-plan.json", retry)
        self.assertEqual(self.grade("revision_consistency_v2")["status"], "PASS")
        self.edit("trace/evidence/partial-plan.json", lambda v: v["prior_origin"].update(sha256="0" * 64))
        self.reject("revision_consistency_v2")

    def test_a09_delivered_failure_cannot_publish(self):
        self.revision(advance=True)
        self.edit("trace/evidence/revision-plan.json", lambda v: v.update(readback_passed=False, evaluation_passed=False))
        self.reject("revision_consistency_v2")
        self.reject("build_traceability_v2")

    def test_a10_adoption_is_not_schema_one_generated_provenance(self):
        record = build_adoption(self.root)
        with self.assertRaises(ValueError):
            graders.prior_provenance_record(record)
        record.update(result="COMPLETE", ownership="generated")
        write_json(self.root / "adoption/evidence/adoption-record.json", record)
        self.reject()

    def test_a11_published_generation_passes_both_v2_graders(self):
        self.revision(advance=True)
        for grader in ("revision_consistency_v2", "build_traceability_v2"):
            self.assertEqual(self.grade(grader)["status"], "PASS", self.grade(grader))

    def test_a11_subsequent_origin_uses_new_baseline_and_adoption_link(self):
        plan = self.revision(advance=True)
        pointer = self.load(plan["baseline_after"]["path"])
        second = copy.deepcopy(plan)
        second.update(prior_origin=pointer["origin"], baseline_before=plan["baseline_after"])
        problems = []
        origin, baseline = graders.revision_origin(self.root, graders.snapshot(self.root), second, problems)
        self.assertEqual(problems, [])
        self.assertEqual(baseline, {p: sha(d) for p, d in files(self.root / "trace/baseline").items()})
        self.assertNotEqual(baseline["SKILL.md"], next(r["b_sha256"] for r in plan["rows"] if r["path"] == "SKILL.md"))
        self.assertEqual(origin["adoption_origin"], plan["adoption_origin"])

    def test_a12_corrupt_selected_history_is_not_erased(self):
        record = build_adoption(self.root)
        write(self.root / "adoption/evidence/failed-history.json", b'{"status":"FAILED"}\n')
        record["prior_evidence"] = [file_ref(self.root, self.root / "adoption/evidence/failed-history.json")]
        write_json(self.root / "adoption/evidence/adoption-record.json", record)
        write(self.root / "adoption/evidence/failed-history.json", b"corrupted history")
        self.reject()
        self.assertEqual((self.root / "adoption/evidence/failed-history.json").read_bytes(), b"corrupted history")

    def test_generated_origin_rehashes_contract_and_authorized_input(self):
        plan = self.revision(advance=True)
        pointer = self.load(plan["baseline_after"]["path"])
        second = {**plan, "prior_origin": pointer["origin"], "baseline_before": plan["baseline_after"]}
        for path in ("trace/input.md", "trace/evidence/build-contract.json", "trace/evidence/construction-observation.json"):
            with self.subTest(path=path):
                original = (self.root / path).read_bytes()
                write(self.root / path, original + b" ")
                problems = []
                graders.revision_origin(self.root, graders.snapshot(self.root), second, problems)
                self.assertTrue(problems)
                write(self.root / path, original)

    def test_a13_missing_duplicate_unobserved_unsafe_management(self):
        record = build_adoption(self.root)
        for selected in ([], ["SKILL.md", "SKILL.md"], ["absent.txt"], ["../escape"], ["/absolute"], ["x//y"]):
            with self.subTest(paths=selected):
                changed = copy.deepcopy(record)
                changed["managed_paths"] = selected
                write_json(self.root / "adoption/evidence/adoption-record.json", changed)
                self.reject()

    def test_a13_duplicate_json_and_nonfinite_rejected(self):
        for raw in ('{"x":1,"x":2}', '{"x":NaN}', '{"x":1e999}'):
            with self.assertRaises(ValueError):
                graders.strict_json(raw)

    def test_a13_snapshot_limits_enforced(self):
        build_adoption(self.root)
        for setting, limit in (("MAX_FILES", 1), ("MAX_BYTES", 1)):
            with patch.object(graders, setting, limit), self.assertRaises(ValueError):
                self.grade()

    def test_a13_link_boundary_rejected(self):
        build_adoption(self.root)
        # Boundary rejection is portable even where Windows cannot create symlinks.
        original = graders.is_link
        with patch.object(graders, "is_link", side_effect=lambda p: p.name == "snapshot" or original(p)):
            with self.assertRaises(ValueError):
                self.grade()

    def test_a14_operational_target_rejected(self):
        record = build_adoption(self.root)
        record["target_root"] = str(self.root / "project/.agents/skills/synthetic-total")
        record["authorization"]["target_root"] = record["target_root"]
        write_json(self.root / "adoption/evidence/adoption-record.json", record)
        self.reject()

    def test_a15_ready_handoff_does_not_override_selected_digests(self):
        record = build_adoption(self.root)
        packet = {"schema_version": "1", "target_root": record["target_root"], "target_manifest_sha256": record["snapshot_manifest"]["sha256"],
                  "managed_manifest_sha256": record["managed_manifest"]["sha256"], "origin_spec_sha256": "0" * 64,
                  "review_policy": "review-before-repair", "review_state": "reviewed", "builder_readiness": "READY",
                  "selected_references": [record["origin_spec"]]}
        write_json(self.root / "adoption/evidence/handoff.json", packet)
        record["handoff"] = file_ref(self.root, self.root / "adoption/evidence/handoff.json")
        write_json(self.root / "adoption/evidence/adoption-record.json", record)
        self.reject()

    def test_a16_unpublished_record_cannot_start_revision(self):
        plan = self.revision()
        (self.root / plan["baseline_before"]["path"]).write_bytes(b'{"schema_version":"2",')
        self.reject("revision_consistency_v2")
        self.assertEqual(self.load("adoption/evidence/adoption-record.json")["recording_state"], "ADOPTED")

    def test_v2_helper_preview_rejects_bad_origin_without_mutation(self):
        plan = self.revision(status="PLANNED")
        before = files(self.root / "trace/destination")
        proc = self.helper("revision-plan", plan)
        self.assertEqual(proc.returncode, 0, proc.stderr + proc.stdout)
        self.assertEqual(json.loads(proc.stdout)["rows"][0]["ownership"], "adopted")
        plan["prior_origin"]["sha256"] = "0" * 64
        proc = self.helper("revision-plan", plan)
        self.assertEqual(proc.returncode, 1, proc.stderr + proc.stdout)
        self.assertEqual(before, files(self.root / "trace/destination"))

    def test_v2_routing_adds_only_adoption_and_preserves_legacy(self):
        expected = [{"case_id": "adopt", "route": "adoption"}, {"case_id": "validate", "route": "unrelated"}]
        for path in ("expected.jsonl", "observed.jsonl"):
            write(self.root / path, "".join(json.dumps(r) + "\n" for r in expected))
        params = {"expected": "expected.jsonl", "observed": "observed.jsonl"}
        self.assertEqual(graders.grade("routing_outcomes_v2", self.root, params)["status"], "PASS")
        with self.assertRaises(ValueError):
            graders.grade("routing_outcomes", self.root, params)
        write(self.root / "observed.jsonl", json.dumps(expected[0]) + "\n" + json.dumps({"case_id": "validate", "route": "adoption"}) + "\n")
        self.assertEqual(graders.grade("routing_outcomes_v2", self.root, params)["status"], "FAIL")

    def test_unknown_versions_rejected(self):
        self.revision()
        self.edit("trace/evidence/revision-plan.json", lambda v: v.update(schema_version="3"))
        self.reject("revision_consistency_v2")

    def test_legacy_retry_allows_same_prior_digest_at_a_different_locator(self):
        plan = build_revision(self.root, status="PARTIAL")
        partial = copy.deepcopy(plan)
        original = self.root / plan["prior_build"]["path"]
        write(self.root / "revision/same-prior.json", original.read_bytes())
        partial["prior_build"]["path"] = "revision/same-prior.json"
        write_json(self.root / "revision/partial.json", partial)
        plan["retry_of"] = file_ref(self.root, self.root / "revision/partial.json")
        write_json(self.root / "revision/revision-plan.json", plan)
        outcome = graders.grade("revision_consistency", self.root, {"path": "revision/revision-plan.json"})
        self.assertEqual(outcome["status"], "PASS", outcome)

    def test_candidate_unjustified_ownership_fails_traceability(self):
        self.revision()
        write(self.root / "trace/baseline/unrequested.txt", b"unrequested")
        self.reject("build_traceability_v2")

    def test_adoption_snapshot_and_destination_cannot_overlap(self):
        build_adoption(self.root)
        with self.assertRaises(ValueError):
            graders.grade("adoption_consistency", self.root, {"evidence": "adoption/evidence", "destination": "adoption/evidence/snapshot"})


if __name__ == "__main__":
    unittest.main()
