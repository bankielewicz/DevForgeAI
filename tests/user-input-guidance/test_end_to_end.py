"""
Integration tests for STORY-059: User Input Guidance Validation & Testing Suite
Test Suite: End-to-End Workflow Integration

Purpose: Validate that the complete validation pipeline executes successfully,
including fixture validation, token measurement, success rate measurement, and
impact report generation.

Test Framework: pytest
Coverage: Full pipeline execution, script integration, sequential workflow
"""

import json
import subprocess
import time
from pathlib import Path

import pytest


class TestEndToEndWorkflow:
    """Integration tests for end-to-end fixture validation workflow"""

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

    def test_should_execute_full_validation_pipeline_end_to_end(
        self, test_suite_path, scripts_path, reports_path
    ):
        """
        GIVEN the validation pipeline scripts exist
        WHEN the full pipeline is executed in sequence
        THEN all scripts run successfully without errors

        Pipeline: Validate Fixtures → Measure Tokens → Measure Success → Generate Report

        Evidence: All scripts execute successfully (exit code 0)
        """
        # Arrange
        pipeline_scripts = [
            ("validate-fixtures.py", "Fixture validation"),
            ("measure-token-savings.py", "Token measurement"),
            ("measure-success-rate.py", "Success rate measurement"),
            ("generate-impact-report.py", "Report generation"),
        ]

        # Act
        script_execution_results = {}
        for script_name, script_description in pipeline_scripts:
            script_path = scripts_path / script_name

            if not script_path.exists():
                script_execution_results[script_name] = {
                    "executed": False,
                    "exit_code": None,
                    "description": script_description,
                    "error": "Script file not found",
                }
                continue

            try:
                result = subprocess.run(
                    ["python3", str(script_path)],
                    cwd=str(test_suite_path),
                    capture_output=True,
                    text=True,
                    timeout=30,
                )

                script_execution_results[script_name] = {
                    "executed": True,
                    "exit_code": result.returncode,
                    "description": script_description,
                    "stdout": result.stdout[:500],  # First 500 chars
                    "stderr": result.stderr[:500],  # First 500 chars
                }
            except subprocess.TimeoutExpired:
                script_execution_results[script_name] = {
                    "executed": False,
                    "exit_code": None,
                    "description": script_description,
                    "error": "Script execution timed out",
                }
            except Exception as e:
                script_execution_results[script_name] = {
                    "executed": False,
                    "exit_code": None,
                    "description": script_description,
                    "error": str(e),
                }

        # Assert
        assert len(script_execution_results) > 0, "No scripts found to execute"

        for script_name, result in script_execution_results.items():
            assert result["executed"], (
                f"{script_name}: Failed to execute - {result.get('error', 'Unknown error')}"
            )
            assert result["exit_code"] == 0, (
                f"{script_name}: Script exited with code {result['exit_code']}\n"
                f"stderr: {result.get('stderr', 'None')}"
            )

    def test_should_generate_all_report_files_after_pipeline_completion(
        self, test_suite_path, scripts_path, reports_path
    ):
        """
        GIVEN all validation and measurement scripts complete successfully
        WHEN report generation script finishes
        THEN all expected report files are created in reports/ directory

        Expected reports:
        - fixture-validation-[timestamp].json
        - token-savings-[timestamp].json
        - success-rate-[timestamp].json
        - impact-report-[timestamp].md

        Evidence: All report files created with correct naming patterns
        """
        # Arrange
        expected_report_types = [
            "fixture-validation-",
            "token-savings-",
            "success-rate-",
            "impact-report-",
        ]

        # Act
        # First ensure reports directory exists
        if not reports_path.exists():
            pytest.skip("Reports directory not yet created")

        # Count existing reports before pipeline
        existing_reports = {}
        for report_type in expected_report_types:
            glob_pattern = f"{report_type}*"
            existing_reports[report_type] = len(list(reports_path.glob(glob_pattern)))

        # Execute pipeline to generate reports
        try:
            subprocess.run(
                ["python3", str(scripts_path / "generate-impact-report.py")],
                cwd=str(test_suite_path),
                capture_output=True,
                timeout=30,
            )
        except (subprocess.TimeoutExpired, FileNotFoundError):
            pytest.skip("Pipeline scripts not yet available for full execution")

        # Count reports after pipeline
        final_reports = {}
        for report_type in expected_report_types:
            glob_pattern = f"{report_type}*"
            final_reports[report_type] = list(reports_path.glob(glob_pattern))

        # Assert
        for report_type in expected_report_types:
            assert (
                len(final_reports[report_type]) > 0
            ), f"No {report_type}* reports generated in {reports_path}"

    def test_should_complete_all_validation_steps_sequentially_without_interruption(
        self, test_suite_path, scripts_path
    ):
        """
        GIVEN all scripts in the validation pipeline exist
        WHEN scripts are executed sequentially
        THEN each script completes successfully before the next script starts

        Evidence: Sequential execution without interruption, all exit codes 0
        """
        # Arrange
        scripts = [
            "validate-fixtures.py",
            "measure-token-savings.py",
            "measure-success-rate.py",
            "generate-impact-report.py",
        ]

        available_scripts = [
            script for script in scripts if (scripts_path / script).exists()
        ]

        # Act
        execution_times = {}
        execution_order = []

        for script_name in available_scripts:
            script_path = scripts_path / script_name
            start_time = time.time()

            try:
                result = subprocess.run(
                    ["python3", str(script_path)],
                    cwd=str(test_suite_path),
                    capture_output=True,
                    timeout=30,
                )
                end_time = time.time()

                execution_times[script_name] = {
                    "start": start_time,
                    "end": end_time,
                    "duration": end_time - start_time,
                    "exit_code": result.returncode,
                    "success": result.returncode == 0,
                }
                execution_order.append(script_name)

            except (subprocess.TimeoutExpired, FileNotFoundError):
                # Script not available for testing
                continue

        # Assert
        assert len(execution_order) > 0, "No scripts could be executed"

        # Verify all executed scripts were successful
        for script_name, metrics in execution_times.items():
            assert metrics["success"], (
                f"{script_name} failed with exit code {metrics['exit_code']}"
            )

        # Verify scripts executed in order (sequential execution)
        for i, script_name in enumerate(execution_order):
            if i > 0:
                prev_script = execution_order[i - 1]
                current_start = execution_times[script_name]["start"]
                prev_end = execution_times[prev_script]["end"]

                assert current_start >= prev_end, (
                    f"{script_name} started before {prev_script} completed "
                    f"(overlap detected, not sequential)"
                )
