"""
Unit tests for STORY-059: User Input Guidance Validation & Testing Suite
Test Suite: AC#4 - Expected Improvements Documented

Purpose: Validate that expected improvements JSON files are created with correct
schema, numeric ranges, and evidence-based rationale.

Test Framework: pytest
Coverage: JSON file creation, schema validation, numeric ranges, evidence-based content
"""

import json
import re
from pathlib import Path

import pytest


class TestExpectedImprovementsFiles:
    """Tests for expected improvements JSON files (AC#4)"""

    @pytest.fixture
    def expected_fixtures_path(self):
        """Base path for expected fixtures directory"""
        return Path("/mnt/c/Projects/DevForgeAI2/tests/user-input-guidance/fixtures/expected")

    @pytest.fixture
    def expected_schema(self):
        """Expected JSON schema for improvements files"""
        return {
            "required_fields": [
                "fixture_id",
                "category",
                "baseline_issues",
                "expected_improvements",
                "rationale",
            ],
            "expected_improvements_fields": [
                "token_savings",
                "ac_completeness",
                "nfr_coverage",
                "specificity_score",
            ],
        }

    @pytest.fixture
    def valid_numeric_ranges(self):
        """Valid numeric ranges for expected improvements"""
        return {
            "token_savings": {"min": 15, "max": 35},
            "ac_completeness": {"min": 70, "max": 95},
            "nfr_coverage": {"min": 50, "max": 100, "increment": 25},
            "specificity_score": {"min": 60, "max": 90},
        }

    def test_should_create_10_expected_json_files(self, expected_fixtures_path):
        """
        GIVEN expected improvements need to be documented
        WHEN 10 JSON files are created
        THEN files exist with correct naming (expected-[NN]-[category].json)

        Evidence: All 10 expected JSON files created with correct naming
        """
        # Arrange
        expected_path = expected_fixtures_path

        # Act
        existing_files = []
        if expected_path.exists():
            existing_files = sorted([f.name for f in expected_path.glob("expected-*.json")])

        # Assert
        expected_count = 10
        assert len(existing_files) == expected_count, (
            f"Expected {expected_count} JSON files, found {len(existing_files)}: {existing_files}"
        )

        # Verify naming convention
        naming_pattern = re.compile(r"^expected-\d{2}-[a-z-]+\.json$")
        for filename in existing_files:
            assert naming_pattern.match(filename), (
                f"File '{filename}' does not match pattern 'expected-NN-category.json'"
            )

    def test_should_have_valid_json_syntax_parseable(self, expected_fixtures_path):
        """
        GIVEN JSON files are created for expected improvements
        WHEN syntax is validated
        THEN all files are valid JSON (parseable via json.load())

        Evidence: All JSON files parse without syntax errors
        """
        # Arrange
        expected_path = expected_fixtures_path

        # Act
        json_validation_results = {}
        if expected_path.exists():
            for json_file in sorted(expected_path.glob("expected-*.json")):
                try:
                    with open(json_file, "r") as f:
                        json.load(f)
                    json_validation_results[json_file.name] = {"valid": True, "error": None}
                except json.JSONDecodeError as e:
                    json_validation_results[json_file.name] = {
                        "valid": False,
                        "error": str(e),
                    }

        # Assert
        assert len(json_validation_results) > 0, "No JSON files found to validate"

        for filename, result in json_validation_results.items():
            assert result["valid"], f"{filename}: JSON syntax error - {result['error']}"

    def test_should_contain_all_required_fields(self, expected_fixtures_path, expected_schema):
        """
        GIVEN JSON files contain expected improvements data
        WHEN schema is validated
        THEN all required fields are present: fixture_id, category, baseline_issues, expected_improvements, rationale

        Evidence: All required fields present in JSON files
        """
        # Arrange
        expected_path = expected_fixtures_path
        required_fields = expected_schema["required_fields"]

        # Act
        schema_validation_results = {}
        if expected_path.exists():
            for json_file in sorted(expected_path.glob("expected-*.json")):
                with open(json_file, "r") as f:
                    data = json.load(f)

                missing_fields = []
                for field in required_fields:
                    if field not in data:
                        missing_fields.append(field)

                schema_validation_results[json_file.name] = {
                    "missing_fields": missing_fields,
                    "valid": len(missing_fields) == 0,
                }

        # Assert
        assert len(schema_validation_results) > 0, "No JSON files found to validate schema"

        for filename, result in schema_validation_results.items():
            assert result["valid"], (
                f"{filename}: Missing required fields: {result['missing_fields']}"
            )

    def test_should_contain_all_expected_improvements_subfields(
        self, expected_fixtures_path, expected_schema
    ):
        """
        GIVEN JSON files contain expected_improvements objects
        WHEN structure is validated
        THEN all expected_improvements subfields are present: token_savings, ac_completeness, nfr_coverage, specificity_score

        Evidence: All expected_improvements fields present in JSON
        """
        # Arrange
        expected_path = expected_fixtures_path
        improvement_fields = expected_schema["expected_improvements_fields"]

        # Act
        improvements_validation_results = {}
        if expected_path.exists():
            for json_file in sorted(expected_path.glob("expected-*.json")):
                with open(json_file, "r") as f:
                    data = json.load(f)

                missing_subfields = []
                if "expected_improvements" in data:
                    for field in improvement_fields:
                        if field not in data["expected_improvements"]:
                            missing_subfields.append(field)

                improvements_validation_results[json_file.name] = {
                    "missing_fields": missing_subfields,
                    "valid": len(missing_subfields) == 0,
                }

        # Assert
        assert (
            len(improvements_validation_results) > 0
        ), "No JSON files found to validate expected_improvements structure"

        for filename, result in improvements_validation_results.items():
            assert result["valid"], (
                f"{filename}: Missing expected_improvements fields: {result['missing_fields']}"
            )

    def test_should_have_numeric_values_in_valid_ranges(
        self, expected_fixtures_path, valid_numeric_ranges
    ):
        """
        GIVEN JSON files contain numeric expected improvements
        WHEN values are validated
        THEN all numeric values are within realistic and achievable ranges:
            - token_savings: 15-35% range
            - ac_completeness: 70-95% range
            - nfr_coverage: 50-100% range (in 25% increments)
            - specificity_score: 60-90% range

        Evidence: All numeric values within valid ranges
        """
        # Arrange
        expected_path = expected_fixtures_path
        ranges = valid_numeric_ranges

        # Act
        numeric_validation_results = {}
        if expected_path.exists():
            for json_file in sorted(expected_path.glob("expected-*.json")):
                with open(json_file, "r") as f:
                    data = json.load(f)

                out_of_range_values = {}
                if "expected_improvements" in data:
                    improvements = data["expected_improvements"]

                    for metric, value in improvements.items():
                        if metric in ranges:
                            valid_range = ranges[metric]
                            min_val = valid_range.get("min")
                            max_val = valid_range.get("max")

                            if not (min_val <= value <= max_val):
                                out_of_range_values[metric] = {
                                    "actual": value,
                                    "expected_range": f"{min_val}-{max_val}",
                                }

                            # Special check for nfr_coverage increments
                            if metric == "nfr_coverage" and "increment" in valid_range:
                                if value % valid_range["increment"] != 0:
                                    out_of_range_values[f"{metric}_increment"] = {
                                        "actual": value,
                                        "expected_increment": valid_range["increment"],
                                    }

                numeric_validation_results[json_file.name] = {
                    "out_of_range": out_of_range_values,
                    "valid": len(out_of_range_values) == 0,
                }

        # Assert
        assert len(numeric_validation_results) > 0, "No JSON files found to validate numeric ranges"

        for filename, result in numeric_validation_results.items():
            assert result["valid"], (
                f"{filename}: Values out of range: {result['out_of_range']}"
            )

    def test_should_have_evidence_based_rationale_citing_guidance(self, expected_fixtures_path):
        """
        GIVEN JSON files contain rationale for expected improvements
        WHEN rationale is validated
        THEN each rationale explains WHY improvements are expected with specific guidance references
              (references to guidance document recommendations or established patterns)

        Evidence: Rationale contains specific guidance references
        """
        # Arrange
        expected_path = expected_fixtures_path

        # Guidance document keywords to verify evidence-based rationale
        guidance_keywords = [
            "guidance",
            "recommend",
            "specify",
            "clear",
            "measurable",
            "metric",
            "specific",
            "scope",
            "testable",
            "criteria",
            "nfr",
            "given/when/then",
            "constraint",
        ]

        # Act
        rationale_validation_results = {}
        if expected_path.exists():
            for json_file in sorted(expected_path.glob("expected-*.json")):
                with open(json_file, "r") as f:
                    data = json.load(f)

                rationale = data.get("rationale", "").lower() if "rationale" in data else ""

                # Count guidance references
                references_found = sum(
                    1 for keyword in guidance_keywords if keyword in rationale
                )

                rationale_validation_results[json_file.name] = {
                    "rationale_length": len(rationale),
                    "references_found": references_found,
                    "has_evidence": references_found >= 3,
                    "rationale_empty": len(rationale) == 0,
                }

        # Assert
        assert len(rationale_validation_results) > 0, "No JSON files found to validate rationale"

        for filename, result in rationale_validation_results.items():
            assert not result["rationale_empty"], (
                f"{filename}: Rationale field is empty"
            )
            assert result["has_evidence"], (
                f"{filename}: Rationale lacks sufficient evidence "
                f"({result['references_found']} references found, expected ≥3)"
            )

    @pytest.mark.parametrize(
        "fixture_number,expected_category",
        [
            ("01", "crud-operations"),
            ("02", "authentication"),
            ("03", "api-integration"),
            ("04", "data-processing"),
            ("05", "ui-components"),
            ("06", "reporting"),
            ("07", "background-jobs"),
            ("08", "search-functionality"),
            ("09", "file-uploads"),
            ("10", "notifications"),
        ],
    )
    def test_should_have_expected_improvements_file_for_each_fixture(
        self, expected_fixtures_path, fixture_number, expected_category
    ):
        """
        GIVEN expected improvements are documented
        WHEN each fixture is checked
        THEN the expected JSON file exists and is parseable

        Evidence: All 10 expected JSON files exist and are valid
        Parameterized across all 10 fixtures
        """
        # Arrange
        expected_path = expected_fixtures_path
        expected_filename = f"expected-{fixture_number}-{expected_category}.json"
        expected_file = expected_path / expected_filename

        # Act
        file_exists = expected_file.exists() if expected_path.exists() else False
        is_valid_json = False

        if file_exists:
            try:
                with open(expected_file, "r") as f:
                    json.load(f)
                is_valid_json = True
            except json.JSONDecodeError:
                is_valid_json = False

        # Assert
        assert file_exists, f"Expected file '{expected_filename}' not found"
        assert is_valid_json, f"Expected file '{expected_filename}' contains invalid JSON"
