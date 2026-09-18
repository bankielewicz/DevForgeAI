"""Focused finite prior-provenance observations; no protected-history claims."""

import copy
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

from fixture_data import build_candidate, build_revision, file_ref, sha, write_json


PACKAGE = Path(__file__).resolve().parents[1]
MODULE_SPEC = importlib.util.spec_from_file_location("review_provenance_graders", PACKAGE / "scripts/graders.py")
GRADERS = importlib.util.module_from_spec(MODULE_SPEC)
MODULE_SPEC.loader.exec_module(GRADERS)


class PriorProvenanceReviewTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory(prefix="builder-prior-provenance-")
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        build_revision(self.root)
        self.provenance_path = self.root / "revision/previous-provenance.json"
        self.original = json.loads(self.provenance_path.read_text(encoding="utf-8"))

    def install_provenance(self, value):
        write_json(self.provenance_path, value)
        projection_path = self.root / "revision/previous-build.json"
        projection = json.loads(projection_path.read_text(encoding="utf-8"))
        projection["provenance"] = file_ref(self.root, self.provenance_path)
        write_json(projection_path, projection)
        plan_path = self.root / "revision/revision-plan.json"
        plan = json.loads(plan_path.read_text(encoding="utf-8"))
        plan["prior_build"] = file_ref(self.root, projection_path)
        write_json(plan_path, plan)

    def observe(self):
        return GRADERS.revision_consistency(self.root, {"path": "revision/revision-plan.json"})

    def assert_rejected(self, change):
        value = copy.deepcopy(self.original)
        change(value)
        self.install_provenance(value)
        try:
            result = self.observe()
        except (ValueError, KeyError, TypeError):
            return
        self.assertEqual(result["status"], "FAIL", result["observations"])

    def test_complete_record_passes(self):
        self.assertEqual(self.observe()["status"], "PASS")

    def test_every_missing_provenance_field_is_rejected(self):
        for name in self.original:
            with self.subTest(field=name):
                self.assert_rejected(lambda value: value.pop(name))

    def test_unknown_provenance_field_is_rejected(self):
        self.assert_rejected(lambda value: value.update(unrecognized=True))

    def test_invalid_scalar_fields_are_rejected(self):
        for name, invalid in (("schema_version", "2"), ("mode", "unknown"), ("target_name", "../other"),
                              ("run_id", ""), ("builder_manifest_sha256", "not-a-digest"),
                              ("contract_sha256", None), ("result", "INCOMPLETE")):
            with self.subTest(field=name):
                self.assert_rejected(lambda value: value.update({name: invalid}))

    def test_input_rows_require_unique_ids_and_exact_fields(self):
        for change in (lambda value: value.update(inputs=[]),
                       lambda value: value["inputs"].append(dict(value["inputs"][0])),
                       lambda value: value["inputs"][0].update(extra="unexpected"),
                       lambda value: value["inputs"][0].update(sha256="invalid")):
            with self.subTest(change=change):
                self.assert_rejected(change)

    def test_dependencies_require_an_object_array(self):
        self.assert_rejected(lambda value: value.update(dependencies=["not-an-object"]))

    def test_output_rows_require_exact_fields_and_valid_paths(self):
        for change in (lambda value: value["outputs"][0].pop("sha256"),
                       lambda value: value["outputs"][0].update(sha256="invalid"),
                       lambda value: value["outputs"][0].update(baseline_path="../outside"),
                       lambda value: value["outputs"][0].update(extra=True)):
            with self.subTest(change=change):
                self.assert_rejected(change)

    def test_retained_user_output_cannot_claim_a_baseline(self):
        self.assert_rejected(lambda value: value["outputs"].append({"path": "user-note", "ownership": "retained_user",
                             "sha256": "1" * 64, "baseline_path": "historical/user-note", "baseline_sha256": "1" * 64}))

    def test_mapping_cannot_name_unknown_output_or_evidence(self):
        for change in (lambda value: value["mappings"][0].update(artifact_paths=["missing"]),
                       lambda value: value["mappings"][0].update(evidence_ids=["missing"]),
                       lambda value: value["mappings"][0].update(evidence_ids=[]),
                       lambda value: value["mappings"].append(dict(value["mappings"][0]))):
            with self.subTest(change=change):
                self.assert_rejected(change)

    def test_evidence_rows_require_exact_fields_and_digest_syntax(self):
        for change in (lambda value: value["evidence"][0].update(sha256="invalid"),
                       lambda value: value["evidence"][0].update(path="/absolute"),
                       lambda value: value["evidence"][0].update(extra=True),
                       lambda value: value["evidence"].append(dict(value["evidence"][0]))):
            with self.subTest(change=change):
                self.assert_rejected(change)

    def test_older_reference_requires_exact_shape(self):
        self.assert_rejected(lambda value: value.update(prior_build={"path": "older/provenance.json"}))

    def test_generated_digest_must_match_actual_B_bytes(self):
        self.assert_rejected(lambda value: value["outputs"][0].update(baseline_sha256="1" * 64))

    def test_previous_run_identity_must_match_projection(self):
        self.assert_rejected(lambda value: value.update(run_id="other-run"))

    def test_prior_builder_digest_need_not_equal_current_builder(self):
        value = copy.deepcopy(self.original)
        value["builder_manifest_sha256"] = "2" * 64
        self.install_provenance(value)
        self.assertEqual(self.observe()["status"], "PASS")

    def test_previous_delivered_user_edits_and_retained_user_rows_are_allowed(self):
        value = copy.deepcopy(self.original)
        value["outputs"][0]["sha256"] = "4" * 64
        value["outputs"].append({"path": "user-note", "ownership": "retained_user", "sha256": "5" * 64,
                                 "baseline_path": None, "baseline_sha256": None})
        self.install_provenance(value)
        self.assertEqual(self.observe()["status"], "PASS")

    def test_traceability_also_requires_a_complete_prior_record(self):
        params = build_candidate(self.root, sha((PACKAGE / "evals/build-manifest.json").read_bytes()))
        prior = copy.deepcopy(self.original)
        prior.pop("contract_sha256")
        write_json(self.provenance_path, prior)
        current_path = self.root / "trace/evidence/build-provenance.json"
        current = json.loads(current_path.read_text(encoding="utf-8"))
        current["prior_build"] = file_ref(self.root, self.provenance_path)
        write_json(current_path, current)
        with self.assertRaises(ValueError):
            GRADERS.build_traceability(self.root, params["build_traceability"])

    def test_traceability_compares_prior_target_with_current_contract(self):
        params = build_candidate(self.root, sha((PACKAGE / "evals/build-manifest.json").read_bytes()))
        prior = copy.deepcopy(self.original)
        prior["target_name"] = "another-valid-target"
        write_json(self.provenance_path, prior)
        current_path = self.root / "trace/evidence/build-provenance.json"
        current = json.loads(current_path.read_text(encoding="utf-8"))
        current["prior_build"] = file_ref(self.root, self.provenance_path)
        write_json(current_path, current)
        result = GRADERS.build_traceability(self.root, params["build_traceability"])
        self.assertEqual(result["status"], "FAIL")
        self.assertIn("prior successful provenance mismatch", result["observations"])

    def test_historical_paths_are_not_rebased_or_recursively_followed(self):
        value = copy.deepcopy(self.original)
        value["outputs"][0]["baseline_path"] = "previous-snapshot/generated/SKILL.md"
        value["evidence"][0]["path"] = "previous-snapshot/observations.json"
        value["prior_build"] = {"path": "older/provenance.json", "sha256": "3" * 64}
        self.install_provenance(value)
        self.assertEqual(self.observe()["status"], "PASS")


if __name__ == "__main__":
    unittest.main()
