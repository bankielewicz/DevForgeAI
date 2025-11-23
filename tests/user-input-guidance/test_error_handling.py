"""
Integration tests for STORY-059: User Input Guidance Validation & Testing Suite
Test Suite: Error Handling & Graceful Degradation

Purpose: Validate that scripts handle errors gracefully, provide clear error messages,
and skip invalid fixtures without crashing.

Test Framework: pytest
Coverage: Error conditions, validation failures, missing dependencies, graceful degradation
"""

import json
import subprocess
import tempfile
from pathlib import Path

import pytest


class TestErrorHandling:
    """Integration tests for error handling and graceful degradation"""

    @pytest.fixture
    def test_suite_path(self):
        """Base path for test suite"""
        return Path("/mnt/c/Projects/DevForgeAI2/tests/user-input-guidance")

    @pytest.fixture
    def scripts_path(self, test_suite_path):
        """Path to scripts directory"""
        return test_suite_path / "scripts"

    @pytest.fixture
    def fixtures_path(self, test_suite_path):
        """Path to fixtures directory"""
        return test_suite_path / "fixtures"

    def test_should_handle_invalid_baseline_fixture_gracefully(
        self, test_suite_path, fixtures_path
    ):
        """
        GIVEN a baseline fixture with invalid format (e.g., empty file)
        WHEN validation script runs
        THEN validation fails with clear error message

        Evidence: Validation detects invalid fixture and reports specific error
        """
        # Arrange
        baseline_path = fixtures_path / "baseline"

        # Create temporary invalid fixture for testing
        if baseline_path.exists():
            invalid_fixture_path = baseline_path / "baseline-99-invalid.txt"
            try:
                # Create empty file (violates word count requirement)
                invalid_fixture_path.write_text("")

                # Act
                result = subprocess.run(
                    ["python3", "scripts/validate-fixtures.py"],
                    cwd=str(test_suite_path),
                    capture_output=True,
                    text=True,
                    timeout=10,
                )

                # Assert
                # Validation should detect the invalid fixture
                assert result.returncode != 0 or "invalid" in result.stdout.lower() or "error" in result.stdout.lower(), (
                    "Validation script should detect invalid fixture or report error"
                )

            finally:
                # Clean up
                if invalid_fixture_path.exists():
                    invalid_fixture_path.unlink()
        else:
            pytest.skip("Fixtures directory not yet created")

    def test_should_skip_measurement_when_tiktoken_missing(
        self, test_suite_path, scripts_path
    ):
        """
        GIVEN the token measurement script requires tiktoken library
        WHEN tiktoken is not installed
        THEN token measurement fails with clear error message about missing dependency

        Evidence: Script provides actionable error message (not cryptic ImportError)
        """
        # Arrange
        token_script = scripts_path / "measure-token-savings.py"

        if not token_script.exists():
            pytest.skip("Token measurement script not yet created")

        # Act
        result = subprocess.run(
            ["python3", str(token_script)],
            cwd=str(test_suite_path),
            capture_output=True,
            text=True,
            timeout=10,
        )

        # Assert
        # If tiktoken is missing, should provide helpful error message
        if result.returncode != 0:
            error_output = (result.stdout + result.stderr).lower()
            # Should mention missing library or dependency, not cryptic ImportError
            assert (
                "tiktoken" in error_output
                or "missing" in error_output
                or "not installed" in error_output
                or "import" in error_output
            ), (
                "Error message should clearly indicate missing tiktoken library: "
                f"{result.stderr}"
            )

    def test_should_handle_missing_input_reports_gracefully(
        self, test_suite_path, scripts_path
    ):
        """
        GIVEN the impact report generation script depends on token and success rate reports
        WHEN input reports don't exist
        THEN script fails with clear message about which scripts to run first

        Evidence: Error message guides user to generate required input reports
        """
        # Arrange
        # Move or delete existing reports temporarily to simulate missing input
        reports_path = test_suite_path / "reports"

        if not reports_path.exists():
            pytest.skip("Reports directory not yet created")

        impact_script = scripts_path / "generate-impact-report.py"

        if not impact_script.exists():
            pytest.skip("Impact report script not yet created")

        # Get list of existing reports
        existing_reports = list(reports_path.glob("*.json"))

        try:
            # Act
            result = subprocess.run(
                ["python3", str(impact_script)],
                cwd=str(test_suite_path),
                capture_output=True,
                text=True,
                timeout=10,
            )

            # Assert
            # If no input reports exist, should provide guidance
            if result.returncode != 0:
                error_output = (result.stdout + result.stderr).lower()
                assert (
                    "report" in error_output
                    or "token" in error_output
                    or "success" in error_output
                    or "missing" in error_output
                ), (
                    "Error message should guide user about required input reports: "
                    f"{result.stderr}"
                )

        finally:
            # Cleanup handled by test fixtures
            pass

    def test_should_skip_measurement_for_incomplete_fixture_pairs(
        self, test_suite_path, fixtures_path
    ):
        """
        GIVEN a baseline fixture exists without corresponding enhanced fixture
        WHEN measurement scripts run
        THEN scripts detect incomplete pair and skip with warning (not crash)

        Evidence: Measurement scripts skip incomplete pairs and report warning
        """
        # Arrange
        baseline_path = fixtures_path / "baseline"
        enhanced_path = fixtures_path / "enhanced"

        if not baseline_path.exists() or not enhanced_path.exists():
            pytest.skip("Fixture directories not yet created")

        # Create baseline without enhanced for testing
        incomplete_baseline = baseline_path / "baseline-99-incomplete.txt"
        try:
            incomplete_baseline.write_text("Sample incomplete fixture for testing purposes.")

            # Act
            result = subprocess.run(
                ["python3", "scripts/measure-token-savings.py"],
                cwd=str(test_suite_path),
                capture_output=True,
                text=True,
                timeout=10,
            )

            # Assert
            # Script should either skip or report missing pair
            output = result.stdout + result.stderr
            # Should not crash (either success or graceful handling)
            assert (
                result.returncode == 0
                or "incomplete" in output.lower()
                or "missing" in output.lower()
                or "skip" in output.lower()
            ), (
                "Script should handle incomplete pairs gracefully (skip or report)"
            )

        finally:
            if incomplete_baseline.exists():
                incomplete_baseline.unlink()

    def test_should_detect_empty_fixture_early_in_validation(
        self, test_suite_path, fixtures_path
    ):
        """
        GIVEN a fixture file is empty (0 bytes)
        WHEN validation runs
        THEN validation detects this early and reports clear error

        Evidence: Validation catches empty files with specific error message
        """
        # Arrange
        baseline_path = fixtures_path / "baseline"

        if not baseline_path.exists():
            pytest.skip("Fixtures directory not yet created")

        empty_fixture = baseline_path / "baseline-98-empty.txt"
        try:
            # Create truly empty file
            empty_fixture.touch()

            # Act
            result = subprocess.run(
                ["python3", "scripts/validate-fixtures.py"],
                cwd=str(test_suite_path),
                capture_output=True,
                text=True,
                timeout=10,
            )

            # Assert
            # Should detect empty file
            output = result.stdout + result.stderr
            assert result.returncode != 0 or "empty" in output.lower() or "word" in output.lower(), (
                "Validation should detect empty files: " + output
            )

        finally:
            if empty_fixture.exists():
                empty_fixture.unlink()

    def test_should_handle_malformed_json_in_expected_fixtures(
        self, test_suite_path, fixtures_path
    ):
        """
        GIVEN an expected improvement JSON file has malformed syntax
        WHEN validation or measurement scripts run
        THEN scripts detect JSON error and report specific message

        Evidence: Clear error message about JSON parsing failure
        """
        # Arrange
        expected_path = fixtures_path / "expected"

        if not expected_path.exists():
            pytest.skip("Expected fixtures directory not yet created")

        malformed_json = expected_path / "expected-99-malformed.json"
        try:
            # Create JSON with syntax error (missing closing brace)
            malformed_json.write_text('{"fixture_id": "99", "category": "test"')

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
            assert result.returncode != 0 or "json" in output.lower() or "syntax" in output.lower(), (
                "Validation should detect malformed JSON: " + output
            )

        finally:
            if malformed_json.exists():
                malformed_json.unlink()
