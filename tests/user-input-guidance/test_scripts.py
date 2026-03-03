"""
AC#2 Tests: Real Story Creation Script Execution

Tests validate that test scripts execute successfully, generate required JSON output,
and capture token usage and iteration cycle metrics.
"""

import pytest
import json
import subprocess
from pathlib import Path


class TestStoryCreationScriptStructure:
    """Tests for AC#2: Script files exist and have proper structure"""

    def test_should_have_test_story_creation_without_guidance_script_with_content(self):
        """Arrange: Baseline test script
        Act: Read script file
        Assert: Script exists and has content"""
        # Arrange
        script_file = Path("/mnt/c/Projects/DevForgeAI2/tests/user-input-guidance/scripts/test-story-creation-without-guidance.sh")

        # Act
        script_exists = script_file.exists() and script_file.is_file()
        has_content = False
        if script_exists:
            content = script_file.read_text()
            has_content = len(content.strip()) > 0

        # Assert
        assert script_exists, f"Baseline test script not found: {script_file}"
        assert has_content, "Baseline test script is empty"

    def test_should_have_test_story_creation_with_guidance_script_with_content(self):
        """Arrange: Enhanced test script
        Act: Read script file
        Assert: Script exists and has content"""
        # Arrange
        script_file = Path("/mnt/c/Projects/DevForgeAI2/tests/user-input-guidance/scripts/test-story-creation-with-guidance.sh")

        # Act
        script_exists = script_file.exists() and script_file.is_file()
        has_content = False
        if script_exists:
            content = script_file.read_text()
            has_content = len(content.strip()) > 0

        # Assert
        assert script_exists, f"Enhanced test script not found: {script_file}"
        assert has_content, "Enhanced test script is empty"

    def test_should_have_baseline_script_with_shebang(self):
        """Arrange: Baseline test script
        Act: Check for #!/bin/bash shebang
        Assert: Script has proper bash shebang"""
        # Arrange
        script_file = Path("/mnt/c/Projects/DevForgeAI2/tests/user-input-guidance/scripts/test-story-creation-without-guidance.sh")

        # Act
        has_shebang = False
        if script_file.exists():
            first_line = script_file.read_text().split('\n')[0]
            has_shebang = 'bash' in first_line

        # Assert
        assert has_shebang, "Baseline test script missing bash shebang"

    def test_should_have_enhanced_script_with_shebang(self):
        """Arrange: Enhanced test script
        Act: Check for #!/bin/bash shebang
        Assert: Script has proper bash shebang"""
        # Arrange
        script_file = Path("/mnt/c/Projects/DevForgeAI2/tests/user-input-guidance/scripts/test-story-creation-with-guidance.sh")

        # Act
        has_shebang = False
        if script_file.exists():
            first_line = script_file.read_text().split('\n')[0]
            has_shebang = 'bash' in first_line

        # Assert
        assert has_shebang, "Enhanced test script missing bash shebang"

    def test_should_have_baseline_script_with_help_flag(self):
        """Arrange: Baseline test script
        Act: Check for --help flag support
        Assert: Script documentation mentions help"""
        # Arrange
        script_file = Path("/mnt/c/Projects/DevForgeAI2/tests/user-input-guidance/scripts/test-story-creation-without-guidance.sh")

        # Act
        has_help = False
        if script_file.exists():
            content = script_file.read_text()
            has_help = '--help' in content or '-h' in content or 'help' in content.lower()

        # Assert
        assert has_help, "Baseline test script does not document help/usage"

    def test_should_have_enhanced_script_with_help_flag(self):
        """Arrange: Enhanced test script
        Act: Check for --help flag support
        Assert: Script documentation mentions help"""
        # Arrange
        script_file = Path("/mnt/c/Projects/DevForgeAI2/tests/user-input-guidance/scripts/test-story-creation-with-guidance.sh")

        # Act
        has_help = False
        if script_file.exists():
            content = script_file.read_text()
            has_help = '--help' in content or '-h' in content or 'help' in content.lower()

        # Assert
        assert has_help, "Enhanced test script does not document help/usage"

    def test_should_have_baseline_script_with_dry_run_flag(self):
        """Arrange: Baseline test script
        Act: Check for --dry-run flag support
        Assert: Script supports dry-run mode"""
        # Arrange
        script_file = Path("/mnt/c/Projects/DevForgeAI2/tests/user-input-guidance/scripts/test-story-creation-without-guidance.sh")

        # Act
        has_dry_run = False
        if script_file.exists():
            content = script_file.read_text()
            has_dry_run = '--dry-run' in content or 'dry-run' in content or 'DRY_RUN' in content

        # Assert
        assert has_dry_run, "Baseline test script does not support --dry-run flag"

    def test_should_have_enhanced_script_with_dry_run_flag(self):
        """Arrange: Enhanced test script
        Act: Check for --dry-run flag support
        Assert: Script supports dry-run mode"""
        # Arrange
        script_file = Path("/mnt/c/Projects/DevForgeAI2/tests/user-input-guidance/scripts/test-story-creation-with-guidance.sh")

        # Act
        has_dry_run = False
        if script_file.exists():
            content = script_file.read_text()
            has_dry_run = '--dry-run' in content or 'dry-run' in content or 'DRY_RUN' in content

        # Assert
        assert has_dry_run, "Enhanced test script does not support --dry-run flag"


class TestScriptOutputRequirements:
    """Tests for AC#2: Scripts generate proper JSON output"""

    def test_should_generate_baseline_results_json_structure(self):
        """Arrange: Baseline results expected output
        Act: Validate JSON output format
        Assert: JSON has proper structure with required fields"""
        # Arrange
        results_file = Path("/mnt/c/Projects/DevForgeAI2/tests/user-input-guidance/baseline-results.json")

        # Act
        required_fields = ["story_id", "fixture_name", "token_usage", "ac_count",
                          "nfr_present", "incomplete", "iterations"]
        json_valid = False
        missing_fields = []

        if results_file.exists():
            try:
                results = json.loads(results_file.read_text())
                json_valid = True

                # Validate structure
                if isinstance(results, dict):
                    entries = results.get("results", [])
                    if entries:
                        for field in required_fields:
                            if field not in entries[0]:
                                missing_fields.append(field)
            except json.JSONDecodeError:
                pass

        # Assert
        assert json_valid, "baseline-results.json is not valid JSON"
        assert not missing_fields, f"Missing fields in baseline-results.json: {', '.join(missing_fields)}"

    def test_should_generate_enhanced_results_json_structure(self):
        """Arrange: Enhanced results expected output
        Act: Validate JSON output format
        Assert: JSON has proper structure with required fields"""
        # Arrange
        results_file = Path("/mnt/c/Projects/DevForgeAI2/tests/user-input-guidance/enhanced-results.json")

        # Act
        required_fields = ["story_id", "fixture_name", "token_usage", "ac_count",
                          "nfr_present", "incomplete", "iterations"]
        json_valid = False
        missing_fields = []

        if results_file.exists():
            try:
                results = json.loads(results_file.read_text())
                json_valid = True

                # Validate structure
                if isinstance(results, dict):
                    entries = results.get("results", [])
                    if entries:
                        for field in required_fields:
                            if field not in entries[0]:
                                missing_fields.append(field)
            except json.JSONDecodeError:
                pass

        # Assert
        assert json_valid, "enhanced-results.json is not valid JSON"
        assert not missing_fields, f"Missing fields in enhanced-results.json: {', '.join(missing_fields)}"

    def test_should_have_10_baseline_story_results(self):
        """Arrange: Baseline results JSON
        Act: Count result entries
        Assert: Exactly 10 story results"""
        # Arrange
        results_file = Path("/mnt/c/Projects/DevForgeAI2/tests/user-input-guidance/baseline-results.json")

        # Act
        result_count = 0
        if results_file.exists():
            try:
                results = json.loads(results_file.read_text())
                result_count = len(results.get("results", []))
            except json.JSONDecodeError:
                pass

        # Assert
        assert result_count == 10, f"Expected 10 baseline results, found {result_count}"

    def test_should_have_10_enhanced_story_results(self):
        """Arrange: Enhanced results JSON
        Act: Count result entries
        Assert: Exactly 10 story results"""
        # Arrange
        results_file = Path("/mnt/c/Projects/DevForgeAI2/tests/user-input-guidance/enhanced-results.json")

        # Act
        result_count = 0
        if results_file.exists():
            try:
                results = json.loads(results_file.read_text())
                result_count = len(results.get("results", []))
            except json.JSONDecodeError:
                pass

        # Assert
        assert result_count == 10, f"Expected 10 enhanced results, found {result_count}"


class TestScriptOutputMetrics:
    """Tests for AC#2: Script output captures required metrics"""

    def test_should_capture_token_usage_per_story_baseline(self):
        """Arrange: Baseline results
        Act: Validate token_usage field presence and values
        Assert: All entries have token_usage > 0"""
        # Arrange
        results_file = Path("/mnt/c/Projects/DevForgeAI2/tests/user-input-guidance/baseline-results.json")

        # Act
        missing_token_usage = []
        if results_file.exists():
            try:
                results = json.loads(results_file.read_text())
                for entry in results.get("results", []):
                    if "token_usage" not in entry or entry.get("token_usage", 0) <= 0:
                        missing_token_usage.append(entry.get("fixture_name", "unknown"))
            except json.JSONDecodeError:
                pass

        # Assert
        assert not missing_token_usage, f"Entries missing valid token_usage: {', '.join(missing_token_usage)}"

    def test_should_capture_token_usage_per_story_enhanced(self):
        """Arrange: Enhanced results
        Act: Validate token_usage field presence and values
        Assert: All entries have token_usage > 0"""
        # Arrange
        results_file = Path("/mnt/c/Projects/DevForgeAI2/tests/user-input-guidance/enhanced-results.json")

        # Act
        missing_token_usage = []
        if results_file.exists():
            try:
                results = json.loads(results_file.read_text())
                for entry in results.get("results", []):
                    if "token_usage" not in entry or entry.get("token_usage", 0) <= 0:
                        missing_token_usage.append(entry.get("fixture_name", "unknown"))
            except json.JSONDecodeError:
                pass

        # Assert
        assert not missing_token_usage, f"Entries missing valid token_usage: {', '.join(missing_token_usage)}"

    def test_should_capture_iteration_count_baseline(self):
        """Arrange: Baseline results
        Act: Validate iterations field presence
        Assert: All entries have iterations ≥ 1"""
        # Arrange
        results_file = Path("/mnt/c/Projects/DevForgeAI2/tests/user-input-guidance/baseline-results.json")

        # Act
        missing_iterations = []
        if results_file.exists():
            try:
                results = json.loads(results_file.read_text())
                for entry in results.get("results", []):
                    if "iterations" not in entry or entry.get("iterations", 0) < 1:
                        missing_iterations.append(entry.get("fixture_name", "unknown"))
            except json.JSONDecodeError:
                pass

        # Assert
        assert not missing_iterations, f"Entries missing valid iterations: {', '.join(missing_iterations)}"

    def test_should_capture_iteration_count_enhanced(self):
        """Arrange: Enhanced results
        Act: Validate iterations field presence
        Assert: All entries have iterations ≥ 1"""
        # Arrange
        results_file = Path("/mnt/c/Projects/DevForgeAI2/tests/user-input-guidance/enhanced-results.json")

        # Act
        missing_iterations = []
        if results_file.exists():
            try:
                results = json.loads(results_file.read_text())
                for entry in results.get("results", []):
                    if "iterations" not in entry or entry.get("iterations", 0) < 1:
                        missing_iterations.append(entry.get("fixture_name", "unknown"))
            except json.JSONDecodeError:
                pass

        # Assert
        assert not missing_iterations, f"Entries missing valid iterations: {', '.join(missing_iterations)}"

    def test_should_capture_ac_count_per_story(self):
        """Arrange: Baseline results
        Act: Validate ac_count field presence
        Assert: All entries have ac_count > 0"""
        # Arrange
        results_file = Path("/mnt/c/Projects/DevForgeAI2/tests/user-input-guidance/baseline-results.json")

        # Act
        missing_ac_count = []
        if results_file.exists():
            try:
                results = json.loads(results_file.read_text())
                for entry in results.get("results", []):
                    if "ac_count" not in entry:
                        missing_ac_count.append(entry.get("fixture_name", "unknown"))
            except json.JSONDecodeError:
                pass

        # Assert
        assert not missing_ac_count, f"Entries missing ac_count: {', '.join(missing_ac_count)}"

    def test_should_capture_nfr_presence_flag(self):
        """Arrange: Enhanced results
        Act: Validate nfr_present field presence
        Assert: All entries have nfr_present boolean"""
        # Arrange
        results_file = Path("/mnt/c/Projects/DevForgeAI2/tests/user-input-guidance/enhanced-results.json")

        # Act
        missing_nfr = []
        if results_file.exists():
            try:
                results = json.loads(results_file.read_text())
                for entry in results.get("results", []):
                    if "nfr_present" not in entry or not isinstance(entry.get("nfr_present"), bool):
                        missing_nfr.append(entry.get("fixture_name", "unknown"))
            except json.JSONDecodeError:
                pass

        # Assert
        assert not missing_nfr, f"Entries missing valid nfr_present: {', '.join(missing_nfr)}"

    def test_should_capture_multiple_runs_per_fixture(self):
        """Arrange: Enhanced results
        Act: Check for runs array (3 measurements per fixture)
        Assert: Each entry has runs array with 3 elements"""
        # Arrange
        results_file = Path("/mnt/c/Projects/DevForgeAI2/tests/user-input-guidance/enhanced-results.json")

        # Act
        invalid_runs = []
        if results_file.exists():
            try:
                results = json.loads(results_file.read_text())
                for entry in results.get("results", []):
                    runs = entry.get("runs", [])
                    if len(runs) != 3:
                        invalid_runs.append(f"{entry.get('fixture_name')}: {len(runs)} runs (expected 3)")
            except json.JSONDecodeError:
                pass

        # Assert
        assert not invalid_runs, f"Invalid run counts: {', '.join(invalid_runs)}"
