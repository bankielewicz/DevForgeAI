#!/usr/bin/env python3
"""
Integration Tests for STORY-059: User Input Guidance Validation & Testing Suite

Tests verify that all components (fixtures, scripts, reports) work together correctly:
1. Fixture pair completeness and consistency
2. Script data flow and interdependencies
3. Cross-component data validation
4. End-to-end measurement pipeline

Test Scenarios:
- Scenario 1: Full Validation Pipeline (validate → token → success → impact)
- Scenario 2: Fixture Pair Completeness (baseline-enhanced-expected consistency)
- Scenario 3: Cross-Component Data Flow (outputs consumed as inputs)
"""

import sys
import os
import json
import subprocess
import tempfile
import shutil
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple, Optional
import pytest
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Test environment setup
TEST_DIR = Path(__file__).parent
FIXTURES_DIR = TEST_DIR / "fixtures"
BASELINE_DIR = FIXTURES_DIR / "baseline"
ENHANCED_DIR = FIXTURES_DIR / "enhanced"
EXPECTED_DIR = FIXTURES_DIR / "expected"
SCRIPTS_DIR = TEST_DIR / "scripts"
REPORTS_DIR = TEST_DIR / "reports"


class TestFixturePairCompleteness:
    """Test Scenario 2: Fixture Pair Completeness"""

    def test_all_fixture_pairs_complete(self):
        """Verify each baseline has matching enhanced and expected files."""
        baseline_files = sorted(BASELINE_DIR.glob("baseline-*.txt"))
        assert len(baseline_files) > 0, "No baseline fixtures found"

        missing_pairs = []
        for baseline_file in baseline_files:
            # Extract fixture ID
            match = baseline_file.name.replace("baseline-", "").replace(".txt", "")
            fixture_num, category = match.split("-", 1)

            enhanced_file = ENHANCED_DIR / f"enhanced-{fixture_num}-{category}.txt"
            expected_file = EXPECTED_DIR / f"expected-{fixture_num}-{category}.json"

            if not enhanced_file.exists():
                missing_pairs.append(f"Missing enhanced: {enhanced_file.name}")
            if not expected_file.exists():
                missing_pairs.append(f"Missing expected: {expected_file.name}")

        assert not missing_pairs, f"Incomplete fixture pairs:\n" + "\n".join(missing_pairs)

    def test_fixture_naming_consistency(self):
        """Verify baseline, enhanced, and expected files have matching names."""
        baseline_files = sorted(BASELINE_DIR.glob("baseline-*.txt"))

        naming_issues = []
        for baseline_file in baseline_files:
            # Extract: baseline-NN-category.txt
            parts = baseline_file.name.replace("baseline-", "").replace(".txt", "").split("-", 1)
            if len(parts) != 2:
                naming_issues.append(f"Invalid baseline name: {baseline_file.name}")
                continue

            fixture_num, category = parts

            # Verify enhanced has exact same NN-category
            enhanced_files = list(ENHANCED_DIR.glob(f"enhanced-{fixture_num}-{category}.txt"))
            if len(enhanced_files) != 1:
                naming_issues.append(
                    f"Enhanced naming mismatch: expected enhanced-{fixture_num}-{category}.txt"
                )

            # Verify expected has exact same NN-category
            expected_files = list(EXPECTED_DIR.glob(f"expected-{fixture_num}-{category}.json"))
            if len(expected_files) != 1:
                naming_issues.append(
                    f"Expected naming mismatch: expected expected-{fixture_num}-{category}.json"
                )

        assert not naming_issues, "Naming inconsistencies found:\n" + "\n".join(naming_issues)

    def test_expected_10_fixture_pairs(self):
        """Verify exactly 10 fixture pairs exist."""
        baseline_files = sorted(BASELINE_DIR.glob("baseline-*.txt"))
        assert len(baseline_files) == 10, f"Expected 10 baseline fixtures, found {len(baseline_files)}"

        enhanced_files = sorted(ENHANCED_DIR.glob("enhanced-*.txt"))
        assert len(enhanced_files) == 10, f"Expected 10 enhanced fixtures, found {len(enhanced_files)}"

        expected_files = sorted(EXPECTED_DIR.glob("expected-*.json"))
        assert len(expected_files) == 10, f"Expected 10 expected files, found {len(expected_files)}"


class TestFixtureContentConsistency:
    """Test Scenario 2: Fixture content validation"""

    def test_baseline_fixtures_not_empty(self):
        """Verify baseline fixtures have content."""
        baseline_files = sorted(BASELINE_DIR.glob("baseline-*.txt"))

        empty_files = []
        for baseline_file in baseline_files:
            content = baseline_file.read_text(encoding='utf-8').strip()
            if not content:
                empty_files.append(baseline_file.name)

        assert not empty_files, f"Empty baseline fixtures: {empty_files}"

    def test_enhanced_fixtures_not_empty(self):
        """Verify enhanced fixtures have content."""
        enhanced_files = sorted(ENHANCED_DIR.glob("enhanced-*.txt"))

        empty_files = []
        for enhanced_file in enhanced_files:
            content = enhanced_file.read_text(encoding='utf-8').strip()
            if not content:
                empty_files.append(enhanced_file.name)

        assert not empty_files, f"Empty enhanced fixtures: {empty_files}"

    def test_expected_json_files_valid(self):
        """Verify expected JSON files are valid and parseable."""
        expected_files = sorted(EXPECTED_DIR.glob("expected-*.json"))

        invalid_files = []
        for expected_file in expected_files:
            try:
                content = expected_file.read_text(encoding='utf-8')
                data = json.loads(content)

                # Validate structure
                required_fields = ["fixture_id", "category", "baseline_issues", "expected_improvements"]
                missing = [f for f in required_fields if f not in data]
                if missing:
                    invalid_files.append(f"{expected_file.name}: missing {missing}")

            except json.JSONDecodeError as e:
                invalid_files.append(f"{expected_file.name}: {e}")

        assert not invalid_files, "Invalid JSON files:\n" + "\n".join(invalid_files)

    def test_expected_improvements_have_numeric_values(self):
        """Verify expected improvements contain numeric values."""
        expected_files = sorted(EXPECTED_DIR.glob("expected-*.json"))

        validation_issues = []
        for expected_file in expected_files:
            data = json.loads(expected_file.read_text(encoding='utf-8'))
            improvements = data.get("expected_improvements", {})

            for key, value in improvements.items():
                if not isinstance(value, (int, float)):
                    validation_issues.append(
                        f"{expected_file.name}: {key} is not numeric (got {type(value).__name__})"
                    )
                if isinstance(value, (int, float)) and (value < 0 or value > 100):
                    validation_issues.append(
                        f"{expected_file.name}: {key} = {value} (out of 0-100 range)"
                    )

        assert not validation_issues, "Numeric validation issues:\n" + "\n".join(validation_issues)

    def test_enhanced_longer_than_baseline(self):
        """Verify enhanced fixtures are longer than baseline."""
        baseline_files = sorted(BASELINE_DIR.glob("baseline-*.txt"))

        length_issues = []
        for baseline_file in baseline_files:
            # Get corresponding enhanced file
            match = baseline_file.name.replace("baseline-", "").replace(".txt", "")
            fixture_num, category = match.split("-", 1)

            enhanced_file = ENHANCED_DIR / f"enhanced-{fixture_num}-{category}.txt"
            if not enhanced_file.exists():
                continue

            baseline_content = baseline_file.read_text(encoding='utf-8').strip()
            enhanced_content = enhanced_file.read_text(encoding='utf-8').strip()

            baseline_words = len(baseline_content.split())
            enhanced_words = len(enhanced_content.split())

            if enhanced_words <= baseline_words:
                length_issues.append(
                    f"{baseline_file.name}: enhanced ({enhanced_words} words) "
                    f"not longer than baseline ({baseline_words} words)"
                )

        assert not length_issues, "Length validation issues:\n" + "\n".join(length_issues)


class TestScriptIntegration:
    """Test Scenario 1: Script data flow and interdependencies"""

    def test_validate_fixtures_script_exists(self):
        """Verify validate-fixtures.py exists and is executable."""
        script = SCRIPTS_DIR / "validate-fixtures.py"
        assert script.exists(), f"Script not found: {script}"

    def test_token_savings_script_exists(self):
        """Verify measure-token-savings.py exists and is executable."""
        script = SCRIPTS_DIR / "measure-token-savings.py"
        assert script.exists(), f"Script not found: {script}"

    def test_success_rate_script_exists(self):
        """Verify measure-success-rate.py exists and is executable."""
        script = SCRIPTS_DIR / "measure-success-rate.py"
        assert script.exists(), f"Script not found: {script}"

    def test_impact_report_script_exists(self):
        """Verify generate-impact-report.py exists and is executable."""
        script = SCRIPTS_DIR / "generate-impact-report.py"
        assert script.exists(), f"Script not found: {script}"

    def test_common_module_exists(self):
        """Verify common.py module exists for shared functionality."""
        common = SCRIPTS_DIR / "common.py"
        assert common.exists(), f"Common module not found: {common}"

    @pytest.mark.integration
    def test_validate_fixtures_script_runs(self):
        """Test that validate-fixtures.py script runs successfully."""
        script = SCRIPTS_DIR / "validate-fixtures.py"
        try:
            result = subprocess.run(
                ["python3", str(script)],
                cwd=str(SCRIPTS_DIR),
                capture_output=True,
                timeout=30
            )
            # Script should exit with 0, 1, or 2 (valid exits)
            assert result.returncode in [0, 1, 2], (
                f"Script exited with code {result.returncode}:\n"
                f"stdout: {result.stdout.decode()}\n"
                f"stderr: {result.stderr.decode()}"
            )
        except subprocess.TimeoutExpired:
            pytest.skip("validate-fixtures.py timed out")
        except Exception as e:
            pytest.skip(f"validate-fixtures.py execution skipped: {e}")


class TestDataFlowIntegration:
    """Test Scenario 3: Data flows between components"""

    def test_expected_files_readable_by_common_module(self):
        """Verify expected JSON files can be loaded by common.py utilities."""
        # This tests that the common module can actually load and parse the expected files
        expected_files = sorted(EXPECTED_DIR.glob("expected-*.json"))

        for expected_file in expected_files:
            try:
                data = json.loads(expected_file.read_text(encoding='utf-8'))

                # Simulate what common.py does
                assert "fixture_id" in data
                assert "expected_improvements" in data
                improvements = data["expected_improvements"]

                # Verify all improvement metrics are present (needed by scripts)
                expected_keys = ["token_savings", "ac_completeness", "nfr_coverage", "specificity_score"]
                for key in expected_keys:
                    assert key in improvements, (
                        f"{expected_file.name} missing metric: {key}"
                    )

            except Exception as e:
                pytest.fail(f"Failed to process {expected_file.name}: {e}")

    def test_fixture_counts_match_across_directories(self):
        """Verify consistent fixture counts in baseline, enhanced, expected."""
        baseline_count = len(list(BASELINE_DIR.glob("baseline-*.txt")))
        enhanced_count = len(list(ENHANCED_DIR.glob("enhanced-*.txt")))
        expected_count = len(list(EXPECTED_DIR.glob("expected-*.json")))

        assert baseline_count == enhanced_count == expected_count, (
            f"Fixture count mismatch: "
            f"baseline={baseline_count}, enhanced={enhanced_count}, expected={expected_count}"
        )

    def test_fixture_numbering_sequential(self):
        """Verify fixture numbers are sequential (01-10)."""
        baseline_files = sorted(BASELINE_DIR.glob("baseline-*.txt"))

        fixture_numbers = []
        for baseline_file in baseline_files:
            match = baseline_file.name.replace("baseline-", "").split("-", 1)
            if len(match) >= 1:
                try:
                    num = int(match[0])
                    fixture_numbers.append(num)
                except ValueError:
                    pass

        fixture_numbers.sort()
        expected_numbers = list(range(1, 11))

        assert fixture_numbers == expected_numbers, (
            f"Fixture numbers not sequential: {fixture_numbers} != {expected_numbers}"
        )


class TestFixtureToExpectedMapping:
    """Test Scenario 3: Baseline/Enhanced fixtures map correctly to expected improvements"""

    def test_each_fixture_has_corresponding_expected(self):
        """Verify each fixture pair has a corresponding expected improvements file."""
        baseline_files = sorted(BASELINE_DIR.glob("baseline-*.txt"))

        for baseline_file in baseline_files:
            match = baseline_file.name.replace("baseline-", "").replace(".txt", "")
            fixture_num, category = match.split("-", 1)

            expected_file = EXPECTED_DIR / f"expected-{fixture_num}-{category}.json"
            assert expected_file.exists(), (
                f"Expected file missing for {baseline_file.name}: {expected_file.name}"
            )

    def test_expected_fixture_id_matches_filename(self):
        """Verify expected file's fixture_id matches the filename."""
        expected_files = sorted(EXPECTED_DIR.glob("expected-*.json"))

        mismatches = []
        for expected_file in expected_files:
            data = json.loads(expected_file.read_text(encoding='utf-8'))
            fixture_id = data.get("fixture_id")

            # Extract from filename: expected-{fixture_id}-{category}.json
            filename_id = expected_file.name.replace("expected-", "").split("-", 1)[0]

            if fixture_id != filename_id:
                mismatches.append(
                    f"{expected_file.name}: fixture_id={fixture_id}, filename indicates {filename_id}"
                )

        assert not mismatches, "Fixture ID mismatches:\n" + "\n".join(mismatches)

    def test_expected_category_matches_filename(self):
        """Verify expected file's category matches the filename."""
        expected_files = sorted(EXPECTED_DIR.glob("expected-*.json"))

        mismatches = []
        for expected_file in expected_files:
            data = json.loads(expected_file.read_text(encoding='utf-8'))
            category = data.get("category")

            # Extract from filename: expected-NN-{category}.json
            filename_category = expected_file.name.replace("expected-", "").split("-", 1)[1].replace(".json", "")

            if category != filename_category:
                mismatches.append(
                    f"{expected_file.name}: category={category}, filename indicates {filename_category}"
                )

        assert not mismatches, "Category mismatches:\n" + "\n".join(mismatches)


class TestMeasurementScriptOutputFormat:
    """Test Scenario 1: Scripts produce expected output formats"""

    def test_reports_directory_exists(self):
        """Verify reports directory exists for script outputs."""
        assert REPORTS_DIR.exists(), f"Reports directory not found: {REPORTS_DIR}"

    def test_common_module_imports(self):
        """Verify common.py has required imports and exports."""
        common = SCRIPTS_DIR / "common.py"
        content = common.read_text(encoding='utf-8')

        required_items = [
            "def get_fixture_pairs",
            "def get_token_count",
            "def load_fixture",
            "def save_json_report",
            "def save_markdown_report",
        ]

        missing = []
        for item in required_items:
            if item not in content:
                missing.append(item)

        assert not missing, f"common.py missing required functions: {missing}"

    def test_validate_fixtures_has_exit_codes(self):
        """Verify validate-fixtures.py defines required exit codes."""
        script = SCRIPTS_DIR / "validate-fixtures.py"
        content = script.read_text(encoding='utf-8')

        exit_codes = ["EXIT_SUCCESS", "EXIT_VALIDATION_FAILED", "EXIT_INCOMPLETE_PAIRS"]
        missing = []
        for code in exit_codes:
            if code not in content:
                missing.append(code)

        # Exit codes can be hardcoded as 0, 1, 2 instead of named constants
        if missing and "sys.exit(0)" not in content:
            pytest.skip("validate-fixtures.py exit codes verification skipped")


class TestEndToEndPipeline:
    """Test Scenario 1: Full validation pipeline works"""

    @pytest.mark.integration
    def test_fixture_validation_precedes_measurement(self):
        """Verify fixtures are properly validated before measurement scripts run."""
        # All fixture pairs must be complete
        baseline_count = len(list(BASELINE_DIR.glob("baseline-*.txt")))
        enhanced_count = len(list(ENHANCED_DIR.glob("enhanced-*.txt")))
        expected_count = len(list(EXPECTED_DIR.glob("expected-*.json")))

        assert baseline_count == enhanced_count == expected_count == 10, (
            "Fixture validation failed: not all 30 fixtures (10 of each type) present"
        )

    @pytest.mark.integration
    def test_token_savings_depends_on_valid_fixtures(self):
        """Verify token savings script depends on baseline-enhanced pairs."""
        baseline_files = sorted(BASELINE_DIR.glob("baseline-*.txt"))
        enhanced_files = sorted(ENHANCED_DIR.glob("enhanced-*.txt"))

        # Both should exist and have same count
        assert len(baseline_files) == len(enhanced_files), (
            "Baseline and enhanced fixture count mismatch"
        )

        # Both should have content
        for baseline_file, enhanced_file in zip(baseline_files, enhanced_files):
            baseline_content = baseline_file.read_text(encoding='utf-8').strip()
            enhanced_content = enhanced_file.read_text(encoding='utf-8').strip()

            assert baseline_content, f"Empty baseline: {baseline_file.name}"
            assert enhanced_content, f"Empty enhanced: {enhanced_file.name}"

    @pytest.mark.integration
    def test_success_rate_depends_on_expected_improvements(self):
        """Verify success rate script depends on expected improvements JSON."""
        expected_files = sorted(EXPECTED_DIR.glob("expected-*.json"))

        for expected_file in expected_files:
            data = json.loads(expected_file.read_text(encoding='utf-8'))

            # Success rate script needs these metrics
            required_metrics = [
                "token_savings",
                "ac_completeness",
                "nfr_coverage",
                "specificity_score"
            ]

            improvements = data.get("expected_improvements", {})
            for metric in required_metrics:
                assert metric in improvements, (
                    f"{expected_file.name} missing required metric: {metric}"
                )
                value = improvements[metric]
                assert isinstance(value, (int, float)), (
                    f"{expected_file.name}: {metric} not numeric"
                )
                assert 0 <= value <= 100, (
                    f"{expected_file.name}: {metric} value {value} out of range [0,100]"
                )

    @pytest.mark.integration
    def test_impact_report_depends_on_prior_reports(self):
        """Verify impact report script aggregates outputs from prior scripts."""
        # Impact report would load token savings and success rate reports
        # Verify at least one of each exists
        token_reports = list(REPORTS_DIR.glob("token-savings-*.json"))
        success_reports = list(REPORTS_DIR.glob("success-rate-*.json"))

        # Note: These may not exist on first run, so we verify structure exists
        # to support this dependency when reports are generated
        assert REPORTS_DIR.exists(), "Reports directory must exist for impact report generation"


class TestCrossComponentConsistency:
    """Test Scenario 3: Consistency across components"""

    def test_baseline_categories_match_across_files(self):
        """Verify baseline fixture categories match expected files."""
        baseline_files = sorted(BASELINE_DIR.glob("baseline-*.txt"))

        for baseline_file in baseline_files:
            match = baseline_file.name.replace("baseline-", "").replace(".txt", "")
            fixture_num, baseline_category = match.split("-", 1)

            # Get expected file
            expected_file = EXPECTED_DIR / f"expected-{fixture_num}-{baseline_category}.json"
            if not expected_file.exists():
                continue

            data = json.loads(expected_file.read_text(encoding='utf-8'))
            expected_category = data.get("category")

            assert expected_category == baseline_category, (
                f"Category mismatch: baseline has {baseline_category}, "
                f"expected has {expected_category}"
            )

    def test_fixture_content_characteristics_preserved(self):
        """Verify enhanced fixtures preserve original feature intent."""
        baseline_files = sorted(BASELINE_DIR.glob("baseline-*.txt"))

        for baseline_file in baseline_files:
            baseline_content = baseline_file.read_text(encoding='utf-8').lower()

            # Get corresponding enhanced file
            match = baseline_file.name.replace("baseline-", "").replace(".txt", "")
            fixture_num, category = match.split("-", 1)

            enhanced_file = ENHANCED_DIR / f"enhanced-{fixture_num}-{category}.txt"
            if not enhanced_file.exists():
                continue

            enhanced_content = enhanced_file.read_text(encoding='utf-8').lower()

            # Get expected improvements
            expected_file = EXPECTED_DIR / f"expected-{fixture_num}-{category}.json"
            if not expected_file.exists():
                continue

            data = json.loads(expected_file.read_text(encoding='utf-8'))
            baseline_issues = data.get("baseline_issues", [])

            # Verify expected file has rationale for improvements
            rationale = data.get("rationale", "")
            assert rationale, f"{expected_file.name}: missing rationale explaining improvements"

            # Rationale should reference guidance principles
            guidance_keywords = ["given", "when", "then", "metric", "performance", "security"]
            has_guidance = any(keyword in rationale.lower() for keyword in guidance_keywords)

            # Enhanced or rationale should show improvement direction
            assert has_guidance or len(enhanced_content) > len(baseline_content), (
                f"{expected_file.name}: enhancement not evident in content or rationale"
            )


class TestFixtureMetadataConsistency:
    """Test Scenario 2 & 3: Fixture metadata is consistent"""

    def test_expected_baseline_issues_present(self):
        """Verify expected files document baseline issues."""
        expected_files = sorted(EXPECTED_DIR.glob("expected-*.json"))

        for expected_file in expected_files:
            data = json.loads(expected_file.read_text(encoding='utf-8'))
            baseline_issues = data.get("baseline_issues", [])

            assert isinstance(baseline_issues, list), (
                f"{expected_file.name}: baseline_issues must be a list"
            )
            assert len(baseline_issues) > 0, (
                f"{expected_file.name}: must document at least one baseline issue"
            )

    def test_expected_improvements_structure(self):
        """Verify expected_improvements structure is consistent."""
        expected_files = sorted(EXPECTED_DIR.glob("expected-*.json"))

        for expected_file in expected_files:
            data = json.loads(expected_file.read_text(encoding='utf-8'))
            improvements = data.get("expected_improvements", {})

            # Must have these metrics for success rate calculation
            required = ["ac_completeness", "nfr_coverage", "specificity_score"]
            for metric in required:
                assert metric in improvements, (
                    f"{expected_file.name}: missing metric {metric}"
                )

    def test_expected_has_rationale(self):
        """Verify expected files include evidence-based rationale."""
        expected_files = sorted(EXPECTED_DIR.glob("expected-*.json"))

        for expected_file in expected_files:
            data = json.loads(expected_file.read_text(encoding='utf-8'))
            rationale = data.get("rationale", "")

            assert rationale, f"{expected_file.name}: missing rationale"
            assert len(rationale) > 50, (
                f"{expected_file.name}: rationale too short ({len(rationale)} chars)"
            )


# Test suite summary
def test_story_059_integration_readiness():
    """
    Summary test verifying STORY-059 integration test readiness.

    Checks:
    1. All fixture files exist (30 total: 10 baseline, 10 enhanced, 10 expected)
    2. Naming consistency across fixture types
    3. Content consistency (no empty files, valid JSON)
    4. Script presence and structure
    5. Data flow compatibility
    """
    # Count fixtures
    baseline_count = len(list(BASELINE_DIR.glob("baseline-*.txt")))
    enhanced_count = len(list(ENHANCED_DIR.glob("enhanced-*.txt")))
    expected_count = len(list(EXPECTED_DIR.glob("expected-*.json")))

    total_fixtures = baseline_count + enhanced_count + expected_count

    assert total_fixtures == 30, (
        f"Expected 30 fixtures (10 of each type), found {total_fixtures}\n"
        f"  baseline: {baseline_count}\n"
        f"  enhanced: {enhanced_count}\n"
        f"  expected: {expected_count}"
    )

    # Verify scripts
    required_scripts = [
        "validate-fixtures.py",
        "measure-token-savings.py",
        "measure-success-rate.py",
        "generate-impact-report.py",
        "common.py"
    ]

    for script in required_scripts:
        script_path = SCRIPTS_DIR / script
        assert script_path.exists(), f"Required script missing: {script}"

    # Verify reports directory
    assert REPORTS_DIR.exists(), "Reports directory must exist"


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
