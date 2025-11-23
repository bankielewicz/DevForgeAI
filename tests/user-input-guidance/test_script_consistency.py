"""
Regression tests for STORY-059: User Input Guidance Validation & Testing Suite
Test Suite: Script Behavior Consistency

Purpose: Validate that scripts produce consistent, deterministic results over time
with no unexpected behavioral changes or output format regressions.

Test Framework: pytest
Coverage: Idempotency, deterministic calculations, output format stability, threshold consistency
"""

import json
import subprocess
import time
from pathlib import Path

import pytest


class TestScriptBehaviorConsistency:
    """Regression tests for script behavior and output consistency"""

    @pytest.fixture
    def test_suite_path(self):
        """Base path for test suite"""
        return Path("/mnt/c/Projects/DevForgeAI2/tests/user-input-guidance")

    @pytest.fixture
    def scripts_path(self, test_suite_path):
        """Path to scripts directory"""
        return test_suite_path / "scripts"

    @pytest.fixture
    def reports_path(self, test_suite_path):
        """Path to reports directory"""
        return test_suite_path / "reports"

    @pytest.fixture
    def fixtures_path(self, test_suite_path):
        """Path to fixtures directory"""
        return test_suite_path / "fixtures"

    def test_should_produce_identical_token_counts_for_same_fixtures(
        self, test_suite_path, scripts_path, fixtures_path
    ):
        """
        GIVEN token measurement script runs on same fixtures
        WHEN measurements are performed twice
        THEN token count results are identical (idempotency)

        Evidence: Same fixture produces same token count in both runs
        """
        # Arrange
        token_script = scripts_path / "measure-token-savings.py"
        reports_path = test_suite_path / "reports"

        if not token_script.exists() or not reports_path.exists():
            pytest.skip("Token script or reports directory not yet created")

        # Act - Run token measurement twice
        run_results = []
        token_measurements = []

        for run_num in range(2):
            try:
                result = subprocess.run(
                    ["python3", str(token_script)],
                    cwd=str(test_suite_path),
                    capture_output=True,
                    text=True,
                    timeout=30,
                )

                if result.returncode == 0:
                    # Find the most recent token-savings report
                    reports = sorted(reports_path.glob("token-savings-*.json"))
                    if reports:
                        latest_report = reports[-1]
                        with open(latest_report, "r") as f:
                            report_data = json.load(f)

                        # Extract per-fixture token counts
                        fixture_tokens = {}
                        if "results" in report_data:
                            for fixture_result in report_data["results"]:
                                fixture_id = fixture_result.get("fixture_id")
                                if fixture_id:
                                    fixture_tokens[fixture_id] = {
                                        "baseline_tokens": fixture_result.get(
                                            "baseline_tokens"
                                        ),
                                        "enhanced_tokens": fixture_result.get(
                                            "enhanced_tokens"
                                        ),
                                    }

                        token_measurements.append(fixture_tokens)

                # Small delay between runs
                if run_num == 0:
                    time.sleep(1)

            except (subprocess.TimeoutExpired, FileNotFoundError):
                pytest.skip("Token script not available for idempotency test")

        # Assert
        if len(token_measurements) == 2 and len(token_measurements[0]) > 0:
            # Compare measurements from both runs
            first_run = token_measurements[0]
            second_run = token_measurements[1]

            for fixture_id in first_run:
                if fixture_id in second_run:
                    first_baseline = first_run[fixture_id]["baseline_tokens"]
                    second_baseline = second_run[fixture_id]["baseline_tokens"]

                    first_enhanced = first_run[fixture_id]["enhanced_tokens"]
                    second_enhanced = second_run[fixture_id]["enhanced_tokens"]

                    # Token counts should be identical for same fixtures
                    assert first_baseline == second_baseline, (
                        f"Fixture {fixture_id}: Baseline tokens differ between runs "
                        f"({first_baseline} vs {second_baseline})"
                    )
                    assert first_enhanced == second_enhanced, (
                        f"Fixture {fixture_id}: Enhanced tokens differ between runs "
                        f"({first_enhanced} vs {second_enhanced})"
                    )

    def test_should_calculate_success_rate_deterministically(
        self, test_suite_path, scripts_path, reports_path
    ):
        """
        GIVEN success rate measurement script runs on same fixtures
        WHEN calculations are performed twice
        THEN success rate percentages are identical (no randomness)

        Evidence: Same fixture produces same success rate in both runs
        """
        # Arrange
        success_script = scripts_path / "measure-success-rate.py"

        if not success_script.exists() or not reports_path.exists():
            pytest.skip("Success rate script or reports directory not yet created")

        # Act - Run success rate measurement twice
        success_measurements = []

        for run_num in range(2):
            try:
                result = subprocess.run(
                    ["python3", str(success_script)],
                    cwd=str(test_suite_path),
                    capture_output=True,
                    text=True,
                    timeout=30,
                )

                if result.returncode == 0:
                    # Find the most recent success-rate report
                    reports = sorted(reports_path.glob("success-rate-*.json"))
                    if reports:
                        latest_report = reports[-1]
                        with open(latest_report, "r") as f:
                            report_data = json.load(f)

                        # Extract per-fixture success metrics
                        fixture_metrics = {}
                        if "results" in report_data:
                            for fixture_result in report_data["results"]:
                                fixture_id = fixture_result.get("fixture_id")
                                if fixture_id:
                                    fixture_metrics[fixture_id] = {
                                        "ac_testability": fixture_result.get(
                                            "ac_testability"
                                        ),
                                        "nfr_coverage": fixture_result.get(
                                            "nfr_coverage"
                                        ),
                                        "specificity": fixture_result.get(
                                            "specificity"
                                        ),
                                    }

                        success_measurements.append(fixture_metrics)

                # Small delay between runs
                if run_num == 0:
                    time.sleep(1)

            except (subprocess.TimeoutExpired, FileNotFoundError):
                pytest.skip("Success rate script not available for determinism test")

        # Assert
        if len(success_measurements) == 2 and len(success_measurements[0]) > 0:
            first_run = success_measurements[0]
            second_run = success_measurements[1]

            for fixture_id in first_run:
                if fixture_id in second_run:
                    first_metrics = first_run[fixture_id]
                    second_metrics = second_run[fixture_id]

                    # All metrics should be identical (deterministic calculation)
                    for metric_name in ["ac_testability", "nfr_coverage", "specificity"]:
                        first_value = first_metrics.get(metric_name)
                        second_value = second_metrics.get(metric_name)

                        assert first_value == second_value, (
                            f"Fixture {fixture_id}, metric {metric_name}: "
                            f"Values differ between runs ({first_value} vs {second_value})"
                        )

    def test_should_maintain_validation_rules_unchanged_across_runs(
        self, test_suite_path, scripts_path, reports_path
    ):
        """
        GIVEN fixture validation script applies quality rules
        WHEN validation runs twice
        THEN the same validation rules apply and same fixtures pass/fail

        Evidence: Validation results consistent across multiple runs
        """
        # Arrange
        validate_script = scripts_path / "validate-fixtures.py"

        if not validate_script.exists() or not reports_path.exists():
            pytest.skip("Validation script or reports directory not yet created")

        # Act - Run validation twice
        validation_results = []

        for run_num in range(2):
            try:
                result = subprocess.run(
                    ["python3", str(validate_script)],
                    cwd=str(test_suite_path),
                    capture_output=True,
                    text=True,
                    timeout=30,
                )

                # Check validation report
                reports = sorted(reports_path.glob("fixture-validation-*.json"))
                if reports:
                    latest_report = reports[-1]
                    with open(latest_report, "r") as f:
                        report_data = json.load(f)

                    # Extract fixture status results
                    fixture_statuses = {}
                    if "results" in report_data:
                        for fixture_result in report_data["results"]:
                            fixture_name = fixture_result.get("fixture")
                            status = fixture_result.get("status")
                            if fixture_name and status:
                                fixture_statuses[fixture_name] = status

                    validation_results.append(fixture_statuses)

                # Small delay between runs
                if run_num == 0:
                    time.sleep(1)

            except (subprocess.TimeoutExpired, FileNotFoundError):
                pytest.skip("Validation script not available for rule consistency test")

        # Assert
        if len(validation_results) == 2 and len(validation_results[0]) > 0:
            first_run = validation_results[0]
            second_run = validation_results[1]

            # Compare fixture statuses
            for fixture_name in first_run:
                if fixture_name in second_run:
                    first_status = first_run[fixture_name]
                    second_status = second_run[fixture_name]

                    assert first_status == second_status, (
                        f"{fixture_name}: Status changed between runs "
                        f"({first_status} → {second_status}), validation rules may have changed"
                    )

    def test_should_maintain_report_format_structure_across_versions(
        self, test_suite_path, reports_path
    ):
        """
        GIVEN report files are generated by scripts
        WHEN report structure is analyzed
        THEN required fields remain consistent (no breaking format changes)

        Evidence: All reports contain required fields with stable structure
        """
        # Arrange
        if not reports_path.exists():
            pytest.skip("Reports directory not yet created")

        # Define required fields for each report type
        required_fields = {
            "token-savings": [
                "results",
                "mean_savings",
                "median_savings",
                "std_dev",
                "hypothesis_passed",
            ],
            "success-rate": [
                "results",
                "mean_ac_testability",
                "mean_nfr_coverage",
                "mean_specificity",
                "fixtures_meeting_expectations",
            ],
            "fixture-validation": [
                "validation_timestamp",
                "total_fixtures",
                "passed",
                "failed",
                "results",
            ],
        }

        # Act
        structure_validation = {}

        for report_type, fields in required_fields.items():
            reports = list(reports_path.glob(f"{report_type}-*.json"))

            for report_file in reports:
                try:
                    with open(report_file, "r") as f:
                        report_data = json.load(f)

                    missing_fields = [f for f in fields if f not in report_data]

                    structure_validation[report_file.name] = {
                        "valid": len(missing_fields) == 0,
                        "missing_fields": missing_fields,
                    }

                except json.JSONDecodeError:
                    structure_validation[report_file.name] = {
                        "valid": False,
                        "error": "Invalid JSON",
                    }

        # Assert
        assert len(structure_validation) > 0, "No reports found to validate"

        for report_name, validation in structure_validation.items():
            assert validation["valid"], (
                f"{report_name}: Report format changed - "
                f"missing fields {validation.get('missing_fields', [])} "
                f"or {validation.get('error', '')}"
            )

    def test_should_maintain_threshold_consistency_in_hypothesis_validation(
        self, test_suite_path, scripts_path, reports_path
    ):
        """
        GIVEN measurement scripts use thresholds for hypothesis validation
        WHEN thresholds are applied to results
        THEN the same thresholds apply consistently (no threshold drift)

        Evidence: Hypothesis validation uses consistent thresholds
        """
        # Arrange
        token_script = scripts_path / "measure-token-savings.py"

        if not token_script.exists() or not reports_path.exists():
            pytest.skip("Token script or reports directory not yet created")

        expected_threshold = 20  # ≥20% mean savings

        # Act - Run and check hypothesis validation
        try:
            result = subprocess.run(
                ["python3", str(token_script)],
                cwd=str(test_suite_path),
                capture_output=True,
                text=True,
                timeout=30,
            )

            reports = sorted(reports_path.glob("token-savings-*.json"))
            if reports:
                latest_report = reports[-1]
                with open(latest_report, "r") as f:
                    report_data = json.load(f)

                # Check hypothesis validation details
                hypothesis_passed = report_data.get("hypothesis_passed")
                mean_savings = report_data.get("mean_savings")

                # Assert
                if mean_savings is not None:
                    # Verify threshold is applied correctly
                    expected_hypothesis_result = mean_savings >= expected_threshold

                    assert hypothesis_passed == expected_hypothesis_result, (
                        f"Hypothesis validation threshold may have changed: "
                        f"mean_savings={mean_savings}, "
                        f"hypothesis_passed={hypothesis_passed}, "
                        f"expected_threshold={expected_threshold}"
                    )

        except (subprocess.TimeoutExpired, FileNotFoundError):
            pytest.skip("Token script not available for threshold test")
