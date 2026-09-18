"""Exercise evaluator behavior using disposable synthetic packages only.

Run with: python -B -X utf8 -m unittest discover -s <this-directory> -v
No fixture is an imported project skill; all candidate files are made in a
temporary directory, and no command from fixture content is executed.
"""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest


PACKAGE = Path(__file__).resolve().parents[1]


class EvaluationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory(prefix="skill-evaluation-test-")
        self.addCleanup(self.temporary.cleanup)
        self.base = Path(self.temporary.name)
        self.package = self.base / "builder"
        shutil.copytree(
            PACKAGE,
            self.package,
            ignore=shutil.ignore_patterns("__pycache__", "*.pyc"),
        )
        self.candidate = self.base / "candidate"
        self.source = self.candidate / "source"
        self.destination = self.candidate / "destination"
        self.evidence = self.candidate / "evidence"
        self.source.mkdir(parents=True)
        self.destination.mkdir(parents=True)
        self.evidence.mkdir(parents=True)
        self.results = self.base / "results"
        self.results.mkdir()
        self.output = self.results / "observations.jsonl"
        self.cases = self.base / "cases.jsonl"
        self.write(self.source / "SKILL.md", "# Synthetic skill\n\n[Details](references/detail.md)\n")
        self.write(self.source / "references/detail.md", "# Synthetic detail\n")
        shutil.copytree(self.source, self.destination, dirs_exist_ok=True)
        self.write_evidence()
        # Every suite exercises both bound graders. Keep independent control
        # inputs so a deliberately broken candidate cannot spoil the control.
        original_roots = self.source, self.destination, self.evidence
        self.source = self.candidate / "control/source"
        self.destination = self.candidate / "control/destination"
        self.evidence = self.candidate / "control/evidence"
        self.source.mkdir(parents=True)
        self.destination.mkdir(parents=True)
        self.evidence.mkdir(parents=True)
        self.write(self.source / "SKILL.md", "# Independent control fixture\n")
        shutil.copytree(self.source, self.destination, dirs_exist_ok=True)
        self.write_evidence()
        self.source, self.destination, self.evidence = original_roots

    @staticmethod
    def write(path: Path, content: str) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8", newline="\n")

    @staticmethod
    def digest(path: Path) -> str:
        return hashlib.sha256(path.read_bytes()).hexdigest()

    def inventory(self, directory: Path) -> dict:
        return {
            "schema_version": "1",
            "root": str(directory.resolve()),
            "captured_at_utc": "2026-09-11T00:00:00Z",
            "files": [
                {
                    "path": path.relative_to(directory).as_posix(),
                    "bytes": path.stat().st_size,
                    "sha256": self.digest(path),
                }
                for path in sorted(directory.rglob("*"))
                if path.is_file()
            ],
            "excluded_boundaries": [],
        }

    def write_json(self, path: Path, value: dict) -> None:
        self.write(path, json.dumps(value, indent=2) + "\n")

    def write_evidence(self) -> None:
        source_manifest = self.inventory(self.source)
        self.write_json(self.evidence / "source-manifest.json", source_manifest)
        self.write_json(self.evidence / "source-after-manifest.json", source_manifest)
        self.write_json(self.evidence / "destination-manifest.json", self.inventory(self.destination))
        self.write_json(
            self.evidence / "file-dispositions.json",
            {
                "schema_version": "1",
                "files": [
                    {
                        "source_path": entry["path"],
                        "source_sha256": entry["sha256"],
                        "role": "entrypoint" if entry["path"] == "SKILL.md" else "reference",
                        "disposition": "PRESERVE",
                        "target_paths": [entry["path"]],
                        "rationale": "Synthetic byte-preservation case.",
                        "behavior_preserved_or_changed": "Preserved fixture bytes.",
                        "dependencies": [],
                        "planned_verification": "Compare manifests and actual bytes.",
                        "performed_review": "Produced by test fixture setup.",
                    }
                    for entry in source_manifest["files"]
                ],
            },
        )

    @staticmethod
    def case(case_id: str, grader_id: str, params: dict, expected: str = "PASS") -> dict:
        return {"case_id": case_id, "grader_id": grader_id, "params": params, "expected": expected}

    def accounting(self, expected: str = "PASS") -> dict:
        return self.case(
            "accounting",
            "manifest_accounting",
            {"source": "source", "destination": "destination", "evidence": "evidence"},
            expected,
        )

    def links(self, expected: str = "PASS", path: str = "destination") -> dict:
        return self.case("links", "package_links", {"path": path}, expected)

    def run_cases(self, cases: list[dict] | None = None, raw: str | None = None) -> tuple[subprocess.CompletedProcess, list[dict]]:
        if raw is None:
            self.assertIsNotNone(cases)
            cases = list(cases)
            grader_ids = {case["grader_id"] for case in cases}
            if "package_links" not in grader_ids:
                cases.append(self.case("__control_links", "package_links", {"path": "control/destination"}))
            if "manifest_accounting" not in grader_ids:
                cases.append(self.case(
                    "__control_accounting",
                    "manifest_accounting",
                    {"source": "control/source", "destination": "control/destination", "evidence": "control/evidence"},
                ))
            raw = "".join(json.dumps(case) + "\n" for case in cases)
        self.write(self.cases, raw)
        environment = os.environ.copy()
        environment["PYTHONDONTWRITEBYTECODE"] = "1"
        command = [
            sys.executable,
            "-B",
            "-X",
            "utf8",
            str(self.package / "scripts/run_evaluation.py"),
            "--package-root", str(self.package),
            "--candidate-root", str(self.candidate),
            "--cases", str(self.cases),
            "--output", str(self.output),
            "--run-id", "unittest-run",
        ]
        completed = subprocess.run(
            command,
            capture_output=True,
            text=True,
            encoding="utf-8",
            env=environment,
            timeout=30,
            check=False,
        )
        records = []
        if self.output.is_file():
            try:
                records = [json.loads(line) for line in self.output.read_text(encoding="utf-8").splitlines()]
            except json.JSONDecodeError:
                # Some rejection cases intentionally use a preexisting sentinel.
                records = []
        return completed, records

    def assert_exit(self, completed: subprocess.CompletedProcess, expected: int) -> None:
        self.assertEqual(
            completed.returncode,
            expected,
            f"stdout:\n{completed.stdout}\nstderr:\n{completed.stderr}",
        )

    def assert_observation(self, records: list[dict], expected_status: str, met: bool = True) -> None:
        controls = [record for record in records if str(record.get("case_id", "")).startswith("__control")]
        for control in controls:
            self.assertEqual(control["status"], "PASS", control)
            self.assertTrue(control["expectation_met"], control)
        records = [record for record in records if not str(record.get("case_id", "")).startswith("__control")]
        self.assertEqual(len(records), 1)
        record = records[0]
        required = {
            "schema_version", "run_id", "case_id", "grader_id", "grader_version",
            "grader_sha256", "candidate_digests", "observations", "status",
            "expected", "expectation_met", "error",
        }
        self.assertTrue(required.issubset(record), record)
        self.assertEqual(record["run_id"], "unittest-run")
        self.assertEqual(record["status"], expected_status)
        self.assertEqual(record["expectation_met"], met)
        self.assertIsNone(record["error"])
        self.assertRegex(record["grader_sha256"], r"^[a-f0-9]{64}$")
        self.assertIsInstance(record["observations"], list)
        self.assertIsInstance(record["candidate_digests"], dict)
        for digest in record["candidate_digests"].values():
            self.assertRegex(digest, r"^[a-f0-9]{64}$")

    def assert_configuration_error(self, completed: subprocess.CompletedProcess, records: list[dict]) -> None:
        self.assert_exit(completed, 2)
        diagnostic = completed.stdout + completed.stderr
        if records:
            self.assertTrue(any(record.get("status") == "ERROR" for record in records), records)
            diagnostic += json.dumps(records)
        self.assertTrue(diagnostic.strip(), "Configuration rejection must expose a diagnostic.")

    def test_complete_byte_preserving_accounting_passes_with_digest_evidence(self) -> None:
        completed, records = self.run_cases([self.accounting()])
        self.assert_exit(completed, 0)
        self.assert_observation(records, "PASS")
        self.assertTrue(records[0]["candidate_digests"])

    def test_source_mutation_is_observed_even_when_baseline_files_agree(self) -> None:
        self.write(self.source / "references/detail.md", "Modified after baseline capture.\n")
        completed, records = self.run_cases([self.accounting("FAIL")])
        self.assert_exit(completed, 0)
        self.assert_observation(records, "FAIL")

    def test_preserve_mismatch_fails_even_with_current_destination_manifest(self) -> None:
        self.write(self.destination / "references/detail.md", "Different destination bytes.\n")
        self.write_json(self.evidence / "destination-manifest.json", self.inventory(self.destination))
        completed, records = self.run_cases([self.accounting("FAIL")])
        self.assert_exit(completed, 0)
        self.assert_observation(records, "FAIL")

    def test_incomplete_dispositions_fail(self) -> None:
        path = self.evidence / "file-dispositions.json"
        value = json.loads(path.read_text(encoding="utf-8"))
        value["files"].pop()
        self.write_json(path, value)
        completed, records = self.run_cases([self.accounting("FAIL")])
        self.assert_exit(completed, 0)
        self.assert_observation(records, "FAIL")

    def test_unmanifested_source_file_fails(self) -> None:
        self.write(self.source / "unrecorded.txt", "No inventory entry.\n")
        completed, records = self.run_cases([self.accounting("FAIL")])
        self.assert_exit(completed, 0)
        self.assert_observation(records, "FAIL")

    def test_missing_disposition_target_fails(self) -> None:
        (self.destination / "references/detail.md").unlink()
        self.write_json(self.evidence / "destination-manifest.json", self.inventory(self.destination))
        completed, records = self.run_cases([self.accounting("FAIL")])
        self.assert_exit(completed, 0)
        self.assert_observation(records, "FAIL")

    def test_existing_inline_and_reference_links_pass(self) -> None:
        self.write(
            self.destination / "SKILL.md",
            "# Synthetic\n[Inline](references/detail.md)\n[Reference][detail]\n"
            "[External](https://example.invalid/)\n[Email](mailto:sample@example.invalid)\n"
            "[Anchor](#synthetic)\n\n[detail]: references/detail.md\n",
        )
        completed, records = self.run_cases([self.links()])
        self.assert_exit(completed, 0)
        self.assert_observation(records, "PASS")

    def test_missing_inline_link_fails(self) -> None:
        self.write(self.destination / "SKILL.md", "[Missing](references/absent.md)\n")
        completed, records = self.run_cases([self.links("FAIL")])
        self.assert_exit(completed, 0)
        self.assert_observation(records, "FAIL")

    def test_missing_reference_style_link_fails(self) -> None:
        self.write(self.destination / "SKILL.md", "[Missing][reference]\n\n[reference]: absent.md\n")
        completed, records = self.run_cases([self.links("FAIL")])
        self.assert_exit(completed, 0)
        self.assert_observation(records, "FAIL")

    def test_link_escaping_selected_package_fails_even_if_file_exists(self) -> None:
        self.write(self.candidate / "outside.md", "Outside selected package.\n")
        self.write(self.destination / "SKILL.md", "[Escaping](../outside.md)\n")
        completed, records = self.run_cases([self.links("FAIL")])
        self.assert_exit(completed, 0)
        self.assert_observation(records, "FAIL")

    def test_unexpected_failure_sets_exit_one(self) -> None:
        self.write(self.destination / "SKILL.md", "[Missing](missing.md)\n")
        completed, records = self.run_cases([self.links()])
        self.assert_exit(completed, 1)
        self.assert_observation(records, "FAIL", met=False)

    def test_malformed_jsonl_is_execution_error(self) -> None:
        completed, records = self.run_cases(raw="{broken json}\n")
        self.assert_configuration_error(completed, records)

    def test_duplicate_case_ids_are_execution_error(self) -> None:
        completed, records = self.run_cases([self.links(), self.links()])
        self.assert_configuration_error(completed, records)

    def test_unknown_grader_is_execution_error(self) -> None:
        completed, records = self.run_cases([self.case("unknown", "execute_shell", {})])
        self.assert_configuration_error(completed, records)

    def test_suite_cannot_omit_a_required_grader(self) -> None:
        completed, records = self.run_cases(raw=json.dumps(self.links()) + "\n")
        self.assert_configuration_error(completed, records)

    def test_grader_root_cannot_escape_candidate(self) -> None:
        completed, records = self.run_cases([self.links(path="../builder")])
        self.assert_configuration_error(completed, records)

    def test_nonfinite_json_is_rejected(self) -> None:
        completed, records = self.run_cases(
            raw='{"case_id":"nan","grader_id":"package_links","params":{"path":NaN},"expected":"PASS"}\n'
        )
        self.assert_configuration_error(completed, records)

    def test_duplicate_json_keys_are_rejected(self) -> None:
        completed, records = self.run_cases(
            raw='{"case_id":"a","case_id":"b","grader_id":"package_links","params":{"path":"destination"},"expected":"PASS"}\n'
        )
        self.assert_configuration_error(completed, records)

    def test_missing_required_grader_artifact_is_execution_error(self) -> None:
        (self.package / "scripts/graders.py").unlink()
        completed, records = self.run_cases([self.links()])
        self.assert_configuration_error(completed, records)

    def test_tampered_grader_artifact_is_rejected_before_import(self) -> None:
        # A top-level side effect proves a failed binding cannot import the file.
        artifact = self.package / "scripts/graders.py"
        marker = self.base / "untrusted-import-ran.txt"
        self.write(artifact, f"from pathlib import Path\nPath({str(marker)!r}).write_text('executed')\n")
        completed, records = self.run_cases([self.links()])
        self.assert_configuration_error(completed, records)
        self.assertFalse(marker.exists(), "Tampered grader was imported before digest verification.")

    def test_missing_build_manifest_is_execution_error(self) -> None:
        (self.package / "evals/build-manifest.json").unlink()
        completed, records = self.run_cases([self.links()])
        self.assert_configuration_error(completed, records)

    def test_nonobject_build_manifest_is_execution_error(self) -> None:
        for index, value in enumerate(([], None)):
            with self.subTest(manifest=value):
                self.write(
                    self.package / "evals/build-manifest.json",
                    json.dumps(value) + "\n",
                )
                self.output = self.results / f"nonobject-manifest-{index}.jsonl"
                completed, records = self.run_cases([self.links()])
                self.assert_configuration_error(completed, records)

    def test_existing_output_is_never_overwritten(self) -> None:
        original = b"preexisting evidence must survive\n"
        self.output.write_bytes(original)
        completed, records = self.run_cases([self.links()])
        self.assert_configuration_error(completed, records)
        self.assertEqual(self.output.read_bytes(), original)

    def test_output_inside_candidate_is_rejected_without_write(self) -> None:
        self.output = self.candidate / "forbidden-results.jsonl"
        completed, records = self.run_cases([self.links()])
        self.assert_configuration_error(completed, records)
        self.assertFalse(self.output.exists())

    def test_output_inside_builder_is_rejected_without_write(self) -> None:
        self.output = self.package / "forbidden-results.jsonl"
        completed, records = self.run_cases([self.links()])
        self.assert_configuration_error(completed, records)
        self.assertFalse(self.output.exists())


if __name__ == "__main__":
    unittest.main()
