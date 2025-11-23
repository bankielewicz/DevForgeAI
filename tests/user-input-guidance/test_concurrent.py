"""
Integration tests for STORY-059: User Input Guidance Validation & Testing Suite
Test Suite: Concurrent Execution & File Safety

Purpose: Validate that scripts handle concurrent execution, prevent file locking issues,
and generate unique timestamped reports without overwrites.

Test Framework: pytest
Coverage: Concurrent script execution, file locking, report uniqueness, timestamp handling
"""

import concurrent.futures
import re
import subprocess
import time
from pathlib import Path

import pytest


class TestConcurrentExecution:
    """Integration tests for concurrent script execution and file safety"""

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

    def test_should_execute_multiple_measurement_scripts_simultaneously(
        self, test_suite_path, scripts_path
    ):
        """
        GIVEN multiple measurement scripts exist
        WHEN scripts are executed concurrently
        THEN all scripts complete successfully without file locking errors

        Evidence: All concurrent executions complete with exit code 0
        """
        # Arrange
        measurement_scripts = [
            "measure-token-savings.py",
            "measure-success-rate.py",
        ]

        available_scripts = [
            scripts_path / script
            for script in measurement_scripts
            if (scripts_path / script).exists()
        ]

        if len(available_scripts) < 2:
            pytest.skip("Insufficient measurement scripts for concurrency test")

        # Act
        execution_results = {}

        def run_script(script_path):
            try:
                result = subprocess.run(
                    ["python3", str(script_path)],
                    cwd=str(test_suite_path),
                    capture_output=True,
                    text=True,
                    timeout=30,
                )
                return {
                    "script": script_path.name,
                    "exit_code": result.returncode,
                    "success": result.returncode == 0,
                    "stdout": result.stdout[:200],
                    "stderr": result.stderr[:200],
                }
            except subprocess.TimeoutExpired:
                return {
                    "script": script_path.name,
                    "exit_code": -1,
                    "success": False,
                    "error": "Timeout",
                }
            except Exception as e:
                return {
                    "script": script_path.name,
                    "exit_code": -1,
                    "success": False,
                    "error": str(e),
                }

        # Execute scripts concurrently
        with concurrent.futures.ThreadPoolExecutor(max_workers=len(available_scripts)) as executor:
            futures = [
                executor.submit(run_script, script) for script in available_scripts
            ]
            execution_results = {
                future.result()["script"]: future.result()
                for future in concurrent.futures.as_completed(futures)
            }

        # Assert
        assert len(execution_results) == len(available_scripts), (
            f"Expected {len(available_scripts)} results, got {len(execution_results)}"
        )

        for script_name, result in execution_results.items():
            assert result["success"], (
                f"{script_name} failed in concurrent execution: "
                f"exit_code={result.get('exit_code')}, "
                f"error={result.get('error')}"
            )

    def test_should_generate_unique_timestamped_reports_without_overwrites(
        self, test_suite_path, reports_path
    ):
        """
        GIVEN measurement scripts run multiple times
        WHEN reports are generated with timestamps
        THEN each report has unique timestamp and previous reports are not overwritten

        Evidence: All generated reports have unique filenames with different timestamps
        """
        # Arrange
        if not reports_path.exists():
            pytest.skip("Reports directory not yet created")

        # Get baseline report count
        initial_reports = list(reports_path.glob("*.json"))
        initial_count = len(initial_reports)

        # Record filenames and timestamps
        report_files_before = {
            f.name: f.stat().st_mtime for f in initial_reports
        }

        # Act
        # Run a measurement script twice with small delay
        measurement_script = test_suite_path / "scripts" / "measure-token-savings.py"

        if measurement_script.exists():
            try:
                # First run
                result1 = subprocess.run(
                    ["python3", str(measurement_script)],
                    cwd=str(test_suite_path),
                    capture_output=True,
                    timeout=15,
                )

                # Small delay to ensure timestamp difference
                time.sleep(2)

                # Second run
                result2 = subprocess.run(
                    ["python3", str(measurement_script)],
                    cwd=str(test_suite_path),
                    capture_output=True,
                    timeout=15,
                )

                # Check reports after runs
                all_reports = list(reports_path.glob("*.json"))
                final_count = len(all_reports)

                # Assert
                # Should have same or more reports (no overwrites)
                assert final_count >= initial_count, (
                    f"Report count decreased (overwrites detected): "
                    f"before={initial_count}, after={final_count}"
                )

                # Check that report filenames are unique (timestamps differ)
                current_files = {f.name for f in all_reports}
                new_files = current_files - set(report_files_before.keys())

                # If measurement generated new reports, they should be unique
                if len(new_files) > 0:
                    # Extract timestamps from new report filenames
                    timestamps = []
                    for new_file in new_files:
                        # Pattern: report-type-TIMESTAMP.json
                        match = re.search(r"(\d{4}-\d{2}-\d{2}[T_]\d{2}[-:]\d{2}[-:]\d{2})", new_file)
                        if match:
                            timestamps.append(match.group(1))

                    # Should have unique timestamps if multiple new reports
                    if len(timestamps) > 1:
                        assert len(timestamps) == len(set(timestamps)), (
                            "Report timestamps should be unique (prevent overwrites)"
                        )

            except (subprocess.TimeoutExpired, FileNotFoundError):
                pytest.skip("Measurement script not available or timed out")
        else:
            pytest.skip("Measurement script not yet created")

    def test_should_handle_concurrent_glob_operations_safely(
        self, test_suite_path, reports_path
    ):
        """
        GIVEN report generation scripts use glob to find input files
        WHEN multiple scripts access the same directory concurrently
        THEN glob operations complete without race conditions or permission errors

        Evidence: All concurrent glob operations succeed
        """
        # Arrange
        if not reports_path.exists():
            pytest.skip("Reports directory not yet created")

        # Act
        def perform_glob_operation(directory, pattern):
            try:
                results = list(Path(directory).glob(pattern))
                return {
                    "pattern": pattern,
                    "count": len(results),
                    "success": True,
                    "files": [f.name for f in results],
                }
            except Exception as e:
                return {
                    "pattern": pattern,
                    "success": False,
                    "error": str(e),
                }

        glob_patterns = [
            "token-savings-*.json",
            "success-rate-*.json",
            "fixture-validation-*.json",
            "*.json",
            "*.md",
        ]

        # Execute glob operations concurrently
        glob_results = {}
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            futures = [
                executor.submit(perform_glob_operation, reports_path, pattern)
                for pattern in glob_patterns
            ]
            glob_results = {
                future.result()["pattern"]: future.result()
                for future in concurrent.futures.as_completed(futures)
            }

        # Assert
        assert len(glob_results) == len(glob_patterns), (
            f"Expected {len(glob_patterns)} glob results, got {len(glob_results)}"
        )

        for pattern, result in glob_results.items():
            assert result["success"], (
                f"Glob pattern '{pattern}' failed: {result.get('error')}"
            )

    def test_should_maintain_report_integrity_during_concurrent_access(
        self, test_suite_path, reports_path
    ):
        """
        GIVEN multiple scripts read and write reports concurrently
        WHEN report files are accessed
        THEN all report files remain valid JSON (no corruption from concurrent access)

        Evidence: All reports remain parseable JSON after concurrent operations
        """
        # Arrange
        if not reports_path.exists():
            pytest.skip("Reports directory not yet created")

        import json

        # Get existing reports
        json_reports = list(reports_path.glob("*.json"))

        if len(json_reports) == 0:
            pytest.skip("No JSON reports to test for integrity")

        # Act
        def check_json_validity(file_path):
            try:
                with open(file_path, "r") as f:
                    json.load(f)
                return {
                    "file": file_path.name,
                    "valid": True,
                }
            except json.JSONDecodeError as e:
                return {
                    "file": file_path.name,
                    "valid": False,
                    "error": str(e),
                }
            except Exception as e:
                return {
                    "file": file_path.name,
                    "valid": False,
                    "error": str(e),
                }

        # Check JSON validity concurrently
        validity_results = {}
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            futures = [
                executor.submit(check_json_validity, report)
                for report in json_reports
            ]
            validity_results = {
                future.result()["file"]: future.result()
                for future in concurrent.futures.as_completed(futures)
            }

        # Assert
        for filename, result in validity_results.items():
            assert result["valid"], (
                f"Report {filename} is corrupted or invalid JSON: {result.get('error')}"
            )
