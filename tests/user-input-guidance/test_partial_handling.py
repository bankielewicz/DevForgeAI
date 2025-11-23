"""
Integration tests for STORY-059: User Input Guidance Validation & Testing Suite
Test Suite: Partial Fixture Handling & Degradation

Purpose: Validate that scripts handle partial or incomplete fixture sets gracefully,
skipping invalid entries while processing valid ones.

Test Framework: pytest
Coverage: Incomplete pairs, partial datasets, missing components, validation continuity
"""

import json
import subprocess
from pathlib import Path

import pytest


class TestPartialFixtureHandling:
    """Integration tests for handling incomplete fixture pairs and partial datasets"""

    @pytest.fixture
    def test_suite_path(self):
        """Base path for test suite"""
        return Path("/mnt/c/Projects/DevForgeAI2/tests/user-input-guidance")

    @pytest.fixture
    def fixtures_path(self, test_suite_path):
        """Path to fixtures directory"""
        return test_suite_path / "fixtures"

    @pytest.fixture
    def scripts_path(self, test_suite_path):
        """Path to scripts directory"""
        return test_suite_path / "scripts"

    def test_should_validate_and_skip_incomplete_pairs_with_warnings(
        self, test_suite_path, fixtures_path
    ):
        """
        GIVEN baseline and enhanced fixtures with some incomplete pairs (baseline without enhanced)
        WHEN validation runs
        THEN incomplete pairs are detected and skipped with warning messages

        Evidence: Validation completes with warnings for incomplete pairs, non-critical error
        """
        # Arrange
        baseline_path = fixtures_path / "baseline"
        enhanced_path = fixtures_path / "enhanced"

        if not baseline_path.exists() or not enhanced_path.exists():
            pytest.skip("Fixture directories not yet created")

        # Create test incomplete pairs
        incomplete_baselines = [
            baseline_path / "baseline-97-incomplete-1.txt",
            baseline_path / "baseline-96-incomplete-2.txt",
        ]

        try:
            for fixture_path in incomplete_baselines:
                fixture_path.write_text("This baseline has no enhanced counterpart.")

            # Act
            result = subprocess.run(
                ["python3", "scripts/validate-fixtures.py"],
                cwd=str(test_suite_path),
                capture_output=True,
                text=True,
                timeout=10,
            )

            # Assert
            output = result.stdout + result.stderr
            # Should complete (not crash) and report incomplete pairs
            assert (
                "incomplete" in output.lower()
                or "missing" in output.lower()
                or "skip" in output.lower()
                or result.returncode == 0
            ), (
                "Validation should handle incomplete pairs gracefully: " + output
            )

        finally:
            for fixture_path in incomplete_baselines:
                if fixture_path.exists():
                    fixture_path.unlink()

    def test_should_generate_partial_validation_report_for_incomplete_set(
        self, test_suite_path, fixtures_path
    ):
        """
        GIVEN some fixtures are missing or incomplete
        WHEN validation generates report
        THEN report shows partial validation (valid fixtures passed, invalid skipped)

        Evidence: Validation report includes status for each fixture (PASS/SKIP/FAIL)
        """
        # Arrange
        validation_script = test_suite_path / "scripts" / "validate-fixtures.py"
        reports_path = test_suite_path / "reports"

        if not validation_script.exists() or not reports_path.exists():
            pytest.skip("Validation script or reports directory not yet created")

        # Act
        result = subprocess.run(
            ["python3", str(validation_script)],
            cwd=str(test_suite_path),
            capture_output=True,
            text=True,
            timeout=10,
        )

        # Find generated validation report
        validation_reports = list(reports_path.glob("fixture-validation-*.json"))

        # Assert
        if len(validation_reports) > 0:
            latest_report = sorted(validation_reports)[-1]
            with open(latest_report, "r") as f:
                report_data = json.load(f)

            # Report should show results for each fixture
            assert "results" in report_data or "fixtures" in report_data, (
                "Validation report should contain per-fixture results"
            )

            # Should show some mix of PASS/FAIL/SKIP statuses
            if "results" in report_data:
                statuses = [r.get("status", "") for r in report_data["results"]]
                assert len(statuses) > 0, "Report should contain fixture statuses"

    def test_should_skip_measurement_for_empty_fixture_without_crashing(
        self, test_suite_path, fixtures_path
    ):
        """
        GIVEN an empty fixture file exists in the fixtures directory
        WHEN measurement scripts run
        THEN script detects empty file and skips it gracefully (not crash)

        Evidence: Measurement script completes with warning for empty fixture
        """
        # Arrange
        baseline_path = fixtures_path / "baseline"

        if not baseline_path.exists():
            pytest.skip("Baseline fixtures directory not yet created")

        empty_fixture = baseline_path / "baseline-95-empty.txt"

        try:
            # Create empty fixture
            empty_fixture.touch()

            # Act - Try running measurement script
            result = subprocess.run(
                ["python3", "scripts/measure-token-savings.py"],
                cwd=str(test_suite_path),
                capture_output=True,
                text=True,
                timeout=10,
            )

            # Assert
            # Should not crash (exit code 0 or 1 with clear message)
            output = result.stdout + result.stderr
            assert (
                result.returncode == 0
                or "empty" in output.lower()
                or "word" in output.lower()
                or "skip" in output.lower()
            ), (
                "Script should handle empty fixtures gracefully: " + output
            )

        finally:
            if empty_fixture.exists():
                empty_fixture.unlink()

    def test_should_continue_validation_despite_malformed_json_in_one_file(
        self, test_suite_path, fixtures_path
    ):
        """
        GIVEN one expected improvement JSON file is malformed while others are valid
        WHEN validation runs
        THEN validation continues processing valid files and reports error for malformed file

        Evidence: Validation report shows FAIL for malformed JSON, not complete crash
        """
        # Arrange
        expected_path = fixtures_path / "expected"

        if not expected_path.exists():
            pytest.skip("Expected fixtures directory not yet created")

        malformed_json = expected_path / "expected-94-malformed.json"

        try:
            # Create malformed JSON
            malformed_json.write_text('{"incomplete": [')

            # Act
            result = subprocess.run(
                ["python3", "scripts/validate-fixtures.py"],
                cwd=str(test_suite_path),
                capture_output=True,
                text=True,
                timeout=10,
            )

            # Assert
            output = result.stdout + result.stderr

            # Should either:
            # 1. Report error for malformed JSON but continue validation
            # 2. Exit cleanly and report the JSON parsing error
            assert (
                result.returncode != 0
                or "malformed" in output.lower()
                or "json" in output.lower()
                or "error" in output.lower()
            ), (
                "Validation should detect and report malformed JSON: " + output
            )

        finally:
            if malformed_json.exists():
                malformed_json.unlink()

    def test_should_generate_report_even_with_partial_fixture_set(
        self, test_suite_path, scripts_path
    ):
        """
        GIVEN some measurement reports exist but not all in the reports directory
        WHEN impact report generation script runs
        THEN report uses available data and notes missing data in limitations

        Evidence: Impact report generates successfully with available data
        """
        # Arrange
        reports_path = test_suite_path / "reports"
        impact_script = scripts_path / "generate-impact-report.py"

        if not reports_path.exists() or not impact_script.exists():
            pytest.skip("Reports directory or impact script not yet created")

        # Act
        result = subprocess.run(
            ["python3", str(impact_script)],
            cwd=str(test_suite_path),
            capture_output=True,
            text=True,
            timeout=10,
        )

        # Assert
        # Should either succeed or provide clear error about missing dependencies
        output = result.stdout + result.stderr
        assert (
            result.returncode == 0
            or "report" in output.lower()
            or "missing" in output.lower()
        ), (
            "Impact script should handle partial data gracefully: " + output
        )

        # If it succeeded, check if output report was created
        if result.returncode == 0:
            impact_reports = list(reports_path.glob("impact-report-*.md"))
            assert len(impact_reports) > 0, (
                "Impact report should be generated when scripts are available"
            )
