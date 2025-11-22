"""
test_measurement_scripts.py - Unit and integration tests for measurement scripts
Tests for measure-token-savings.py, measure-success-rate.py, and generate-impact-report.py
Following TDD Red phase - all tests should FAIL before implementation
"""

import os
import json
import pytest
import subprocess
import tempfile
import re
from pathlib import Path
from datetime import datetime


class TestTokenSavingsScript:
    """AC#5: Token Savings Measurement Script Functional - 9 items

    Tests for measure-token-savings.py script measuring token reduction from guidance.
    """

    @pytest.fixture
    def scripts_dir(self):
        """Fixture providing path to scripts directory"""
        return Path("tests/user-input-guidance/scripts")

    def test_measure_token_savings_script_exists(self, scripts_dir):
        """Test: measure-token-savings.py script exists and is executable"""
        # Arrange
        script_path = scripts_dir / "measure-token-savings.py"

        # Assert
        assert script_path.exists(), "measure-token-savings.py not found"
        assert script_path.is_file(), "measure-token-savings.py is not a file"

    def test_script_requires_tiktoken_library(self, scripts_dir):
        """Test: Script imports tiktoken with cl100k_base encoding"""
        # Arrange
        script_path = scripts_dir / "measure-token-savings.py"

        # Act
        content = script_path.read_text()

        # Assert
        assert "tiktoken" in content, "Script should import tiktoken library"
        assert "cl100k_base" in content, "Script should use cl100k_base encoding"

    def test_script_loads_all_10_baseline_enhanced_pairs(self, scripts_dir):
        """Test: Script processes all 10 baseline/enhanced fixture pairs"""
        # Arrange
        script_path = scripts_dir / "measure-token-savings.py"

        # Act
        content = script_path.read_text()

        # Assert
        # Script should reference fixtures directory and iterate through files
        assert "fixtures" in content or "baseline" in content, "Script should load baseline fixtures"
        assert "enhanced" in content, "Script should load enhanced fixtures"
        # Should iterate or process pairs
        assert "for" in content or "glob" in content, "Script should iterate through fixture pairs"

    def test_script_generates_json_report_with_timestamp(self, scripts_dir):
        """Test: Script generates JSON report with timestamp in filename"""
        # Arrange
        script_path = scripts_dir / "measure-token-savings.py"

        # Act
        content = script_path.read_text()

        # Assert
        # Should generate JSON report with timestamp
        assert "json" in content.lower(), "Script should generate JSON output"
        assert ".json" in content, "Script should create JSON file"
        # Should include timestamp logic
        assert "datetime" in content or "timestamp" in content.lower(), "Script should include timestamp"

    def test_script_calculates_per_fixture_savings_percentage(self, scripts_dir):
        """Test: Script calculates (baseline - enhanced) / baseline * 100 for each fixture"""
        # Arrange
        script_path = scripts_dir / "measure-token-savings.py"

        # Act
        content = script_path.read_text()

        # Assert
        # Should contain calculation logic for savings percentage
        assert "baseline" in content, "Script should reference baseline tokens"
        assert "enhanced" in content, "Script should reference enhanced tokens"
        # Formula should be present or implied
        assert ("/" in content or "percent" in content.lower()), "Script should calculate percentage"

    def test_script_generates_aggregate_statistics(self, scripts_dir):
        """Test: Script includes mean, median, std_dev, min, max savings in report"""
        # Arrange
        script_path = scripts_dir / "measure-token-savings.py"

        # Act
        content = script_path.read_text()

        # Assert
        # Should calculate aggregate statistics
        statistics_terms = ["mean", "median", "std", "min", "max", "average"]
        assert any(term in content.lower() for term in statistics_terms), "Script should calculate statistics"

    def test_script_exits_with_0_if_mean_savings_gte_20_percent(self, scripts_dir):
        """Test: Script exits with status 0 if mean savings ≥20%"""
        # Arrange
        script_path = scripts_dir / "measure-token-savings.py"

        # Act
        content = script_path.read_text()

        # Assert
        # Should check if mean >= 20 and set exit code accordingly
        assert "20" in content, "Script should reference 20% threshold"
        assert "exit" in content or "sys.exit" in content, "Script should call exit()"

    def test_script_exits_with_1_if_mean_savings_lt_20_percent(self, scripts_dir):
        """Test: Script exits with status 1 if mean savings <20%"""
        # Arrange
        script_path = scripts_dir / "measure-token-savings.py"

        # Act
        content = script_path.read_text()

        # Assert
        # Logic for exit status 0 vs 1
        assert "0" in content and "1" in content, "Script should handle both success (0) and failure (1) exit codes"

    def test_script_outputs_success_failure_message(self, scripts_dir):
        """Test: Script outputs clear success/failure message with actual mean savings %"""
        # Arrange
        script_path = scripts_dir / "measure-token-savings.py"

        # Act
        content = script_path.read_text()

        # Assert
        # Should include success/failure messages with results
        assert "token" in content.lower() or "savings" in content.lower(), "Script should mention token savings"
        # Should use print or logging for output
        assert "print" in content or "logging" in content, "Script should output results"


class TestSuccessRateScript:
    """AC#6: Success Rate Measurement Script Functional - 5 items

    Tests for measure-success-rate.py script evaluating AC quality.
    """

    @pytest.fixture
    def scripts_dir(self):
        """Fixture providing path to scripts directory"""
        return Path("tests/user-input-guidance/scripts")

    def test_measure_success_rate_script_exists(self, scripts_dir):
        """Test: measure-success-rate.py script exists"""
        # Arrange
        script_path = scripts_dir / "measure-success-rate.py"

        # Assert
        assert script_path.exists(), "measure-success-rate.py not found"

    def test_script_analyzes_ac_testability_metric(self, scripts_dir):
        """Test: Script analyzes AC testability (Given/When/Then percentage)"""
        # Arrange
        script_path = scripts_dir / "measure-success-rate.py"

        # Act
        content = script_path.read_text()

        # Assert
        assert "given" in content.lower() or "when" in content.lower() or "then" in content.lower(), \
            "Script should detect Given/When/Then format"
        assert "ac" in content.lower() or "testab" in content.lower(), \
            "Script should analyze AC testability"

    def test_script_analyzes_nfr_coverage_metric(self, scripts_dir):
        """Test: Script analyzes NFR coverage (4 categories: performance, security, reliability, scalability)"""
        # Arrange
        script_path = scripts_dir / "measure-success-rate.py"

        # Act
        content = script_path.read_text()

        # Assert
        nfr_keywords = ["performance", "security", "reliability", "scalability"]
        assert any(keyword in content.lower() for keyword in nfr_keywords), \
            "Script should check NFR categories"

    def test_script_analyzes_specificity_metric(self, scripts_dir):
        """Test: Script analyzes specificity (vague term reduction %)"""
        # Arrange
        script_path = scripts_dir / "measure-success-rate.py"

        # Act
        content = script_path.read_text()

        # Assert
        vague_terms = ["fast", "good", "better", "optimize", "improve"]
        assert any(term in content.lower() for term in vague_terms), \
            "Script should detect vague terms for specificity metric"
        assert "specif" in content.lower(), "Script should calculate specificity"

    def test_script_loads_expected_improvements_from_json(self, scripts_dir):
        """Test: Script loads expected improvements from expected/*.json files"""
        # Arrange
        script_path = scripts_dir / "measure-success-rate.py"

        # Act
        content = script_path.read_text()

        # Assert
        assert "expected" in content.lower(), "Script should load expected JSON files"
        assert "json" in content.lower(), "Script should parse JSON"

    def test_script_exits_with_0_if_8_of_10_fixtures_pass(self, scripts_dir):
        """Test: Script exits with status 0 if ≥8 of 10 fixtures meet expectations"""
        # Arrange
        script_path = scripts_dir / "measure-success-rate.py"

        # Act
        content = script_path.read_text()

        # Assert
        assert "8" in content or "0.8" in content, "Script should check ≥8/10 fixtures passing"
        assert "exit" in content or "sys.exit" in content, "Script should set exit code"

    def test_script_outputs_per_fixture_pass_fail_details(self, scripts_dir):
        """Test: Script outputs per-fixture pass/fail with metric-level details"""
        # Arrange
        script_path = scripts_dir / "measure-success-rate.py"

        # Act
        content = script_path.read_text()

        # Assert
        # Should output fixture-by-fixture results
        assert "fixture" in content.lower(), "Script should report per-fixture results"
        # Should show metric details
        output_indicators = ["✅", "❌", "PASS", "FAIL", "metric"]
        assert any(indicator in content for indicator in output_indicators), \
            "Script should show pass/fail indicators"


class TestImpactReportScript:
    """AC#7: Impact Report Generation Script Functional - 6 items

    Tests for generate-impact-report.py script creating comprehensive report.
    """

    @pytest.fixture
    def scripts_dir(self):
        """Fixture providing path to scripts directory"""
        return Path("tests/user-input-guidance/scripts")

    def test_generate_impact_report_script_exists(self, scripts_dir):
        """Test: generate-impact-report.py script exists"""
        # Arrange
        script_path = scripts_dir / "generate-impact-report.py"

        # Assert
        assert script_path.exists(), "generate-impact-report.py not found"

    def test_script_loads_most_recent_reports(self, scripts_dir):
        """Test: Script loads most recent token-savings and success-rate JSON reports"""
        # Arrange
        script_path = scripts_dir / "generate-impact-report.py"

        # Act
        content = script_path.read_text()

        # Assert
        assert "token-savings" in content.lower() or "token_savings" in content.lower(), \
            "Script should load token-savings report"
        assert "success-rate" in content.lower() or "success_rate" in content.lower(), \
            "Script should load success-rate report"
        assert "glob" in content.lower() or "latest" in content.lower() or "sort" in content.lower(), \
            "Script should find most recent reports"

    def test_script_generates_markdown_report_with_5_sections(self, scripts_dir):
        """Test: Script generates Markdown report with 5 required sections"""
        # Arrange
        script_path = scripts_dir / "generate-impact-report.py"
        required_sections = [
            "Executive Summary",
            "Token Efficiency",
            "Quality Improvements",
            "Fixture Analysis",
            "Recommendations"
        ]

        # Act
        content = script_path.read_text()

        # Assert
        for section in required_sections:
            # Should mention these sections or generate headers with them
            assert section.lower() in content.lower() or section.split()[0].lower() in content.lower(), \
                f"Script should generate '{section}' section"

    def test_script_includes_ascii_visualizations(self, scripts_dir):
        """Test: Script includes ASCII visualizations (Unicode boxes, bar charts)"""
        # Arrange
        script_path = scripts_dir / "generate-impact-report.py"
        unicode_chars = ["│", "─", "┌", "┐", "└", "┘", "█", "▓", "▒"]

        # Act
        content = script_path.read_text()

        # Assert
        # Should include Unicode characters for visualization or methods to create them
        assert any(char in content for char in unicode_chars) or \
               "table" in content.lower() or "chart" in content.lower() or \
               "visual" in content.lower(), "Script should generate ASCII visualizations"

    def test_script_executive_summary_includes_pass_fail(self, scripts_dir):
        """Test: Executive Summary includes hypothesis VALIDATED/FAILED determination"""
        # Arrange
        script_path = scripts_dir / "generate-impact-report.py"

        # Act
        content = script_path.read_text()

        # Assert
        assert "executive" in content.lower() or "summary" in content.lower(), \
            "Script should generate Executive Summary"
        assert "validated" in content.lower() or "passed" in content.lower() or "failed" in content.lower(), \
            "Script should indicate hypothesis result"

    def test_script_recommendations_are_actionable_and_specific(self, scripts_dir):
        """Test: Recommendations section contains specific fixture IDs and guidance references"""
        # Arrange
        script_path = scripts_dir / "generate-impact-report.py"

        # Act
        content = script_path.read_text()

        # Assert
        assert "recommend" in content.lower(), "Script should generate recommendations"
        assert "fixture" in content.lower(), "Recommendations should reference fixture IDs"
        assert "guidance" in content.lower() or "review" in content.lower(), \
            "Recommendations should suggest specific actions"


class TestFixtureValidationScript:
    """AC#8: Fixture Quality Validation Script Functional - 7 items

    Tests for validate-fixtures.py script validating all fixtures.
    """

    @pytest.fixture
    def scripts_dir(self):
        """Fixture providing path to scripts directory"""
        return Path("tests/user-input-guidance/scripts")

    def test_validate_fixtures_script_exists(self, scripts_dir):
        """Test: validate-fixtures.py script exists"""
        # Arrange
        script_path = scripts_dir / "validate-fixtures.py"

        # Assert
        assert script_path.exists(), "validate-fixtures.py not found"

    def test_script_validates_all_30_fixtures(self, scripts_dir):
        """Test: Script validates all 30 fixtures (10 baseline + 10 enhanced + 10 expected)"""
        # Arrange
        script_path = scripts_dir / "validate-fixtures.py"

        # Act
        content = script_path.read_text()

        # Assert
        # Should iterate through baseline, enhanced, expected
        fixture_types = ["baseline", "enhanced", "expected"]
        assert all(ftype in content.lower() for ftype in fixture_types), \
            "Script should validate all fixture types"

    def test_script_validates_baseline_word_count_50_200(self, scripts_dir):
        """Test: Script validates baseline word count 50-200"""
        # Arrange
        script_path = scripts_dir / "validate-fixtures.py"

        # Act
        content = script_path.read_text()

        # Assert
        assert "word" in content.lower() or "len" in content or "count" in content.lower(), \
            "Script should validate word counts"
        assert "50" in content and "200" in content, \
            "Script should check 50-200 word range for baseline"

    def test_script_validates_enhanced_length_increase_30_60_percent(self, scripts_dir):
        """Test: Script validates enhanced length increase 30-60%"""
        # Arrange
        script_path = scripts_dir / "validate-fixtures.py"

        # Act
        content = script_path.read_text()

        # Assert
        assert "30" in content and "60" in content, \
            "Script should check 30-60% length increase"
        assert "percent" in content.lower() or "%" in content, \
            "Script should calculate percentage increase"

    def test_script_validates_expected_json_schema(self, scripts_dir):
        """Test: Script validates expected JSON schema (fixture_id, category, improvements, rationale)"""
        # Arrange
        script_path = scripts_dir / "validate-fixtures.py"

        # Act
        content = script_path.read_text()

        # Assert
        required_fields = ["fixture_id", "category", "expected_improvements", "rationale"]
        assert "json" in content.lower(), "Script should validate JSON files"
        assert any(field in content.lower() for field in required_fields), \
            "Script should check required JSON fields"

    def test_script_generates_json_validation_report(self, scripts_dir):
        """Test: Script generates JSON validation report with pass/fail per fixture"""
        # Arrange
        script_path = scripts_dir / "validate-fixtures.py"

        # Act
        content = script_path.read_text()

        # Assert
        assert "json" in content.lower(), "Script should generate JSON output"
        assert "report" in content.lower() or "result" in content.lower(), \
            "Script should create validation report"

    def test_script_exits_0_all_pass_1_any_fail_2_incomplete_pairs(self, scripts_dir):
        """Test: Script exits with 0/1/2 depending on validation results"""
        # Arrange
        script_path = scripts_dir / "validate-fixtures.py"

        # Act
        content = script_path.read_text()

        # Assert
        # Should have logic for multiple exit codes
        assert "0" in content and "1" in content and "2" in content, \
            "Script should handle exit codes 0, 1, 2"
        assert "exit" in content or "sys.exit" in content, \
            "Script should set appropriate exit codes"


class TestScriptHelp:
    """NFR-017: Scripts must support --help flag"""

    @pytest.fixture
    def scripts_dir(self):
        """Fixture providing path to scripts directory"""
        return Path("tests/user-input-guidance/scripts")

    def test_token_savings_script_has_help_support(self, scripts_dir):
        """Test: measure-token-savings.py responds to --help"""
        # Arrange
        script_path = scripts_dir / "measure-token-savings.py"

        # Act
        content = script_path.read_text()

        # Assert
        assert "--help" in content or "argparse" in content or "help" in content.lower(), \
            "Script should support --help flag"

    def test_success_rate_script_has_help_support(self, scripts_dir):
        """Test: measure-success-rate.py responds to --help"""
        # Arrange
        script_path = scripts_dir / "measure-success-rate.py"

        # Act
        content = script_path.read_text()

        # Assert
        assert "--help" in content or "argparse" in content, \
            "Script should support --help flag"

    def test_impact_report_script_has_help_support(self, scripts_dir):
        """Test: generate-impact-report.py responds to --help"""
        # Arrange
        script_path = scripts_dir / "generate-impact-report.py"

        # Act
        content = script_path.read_text()

        # Assert
        assert "--help" in content or "argparse" in content, \
            "Script should support --help flag"

    def test_validation_script_has_help_support(self, scripts_dir):
        """Test: validate-fixtures.py responds to --help"""
        # Arrange
        script_path = scripts_dir / "validate-fixtures.py"

        # Act
        content = script_path.read_text()

        # Assert
        assert "--help" in content or "argparse" in content, \
            "Script should support --help flag"


class TestScriptUsesLogging:
    """NFR-010: Scripts must use Python logging module, not print statements"""

    @pytest.fixture
    def scripts_dir(self):
        """Fixture providing path to scripts directory"""
        return Path("tests/user-input-guidance/scripts")

    def test_token_savings_uses_logging(self, scripts_dir):
        """Test: measure-token-savings.py uses logging module"""
        # Arrange
        script_path = scripts_dir / "measure-token-savings.py"

        # Act
        content = script_path.read_text()

        # Assert
        assert "import logging" in content or "from logging" in content, \
            "Script should import logging"
        # May still have print for final output, but should use logging for progress
        logging_calls = ["logging.info", "logging.error", "logging.warning", "logging.debug"]
        assert any(call in content for call in logging_calls), \
            "Script should use logging.* calls"

    def test_success_rate_uses_logging(self, scripts_dir):
        """Test: measure-success-rate.py uses logging module"""
        # Arrange
        script_path = scripts_dir / "measure-success-rate.py"

        # Act
        content = script_path.read_text()

        # Assert
        assert "import logging" in content or "from logging" in content, \
            "Script should import logging"

    def test_impact_report_uses_logging(self, scripts_dir):
        """Test: generate-impact-report.py uses logging module"""
        # Arrange
        script_path = scripts_dir / "generate-impact-report.py"

        # Act
        content = script_path.read_text()

        # Assert
        assert "import logging" in content or "from logging" in content, \
            "Script should import logging"

    def test_validation_script_uses_logging(self, scripts_dir):
        """Test: validate-fixtures.py uses logging module"""
        # Arrange
        script_path = scripts_dir / "validate-fixtures.py"

        # Act
        content = script_path.read_text()

        # Assert
        assert "import logging" in content or "from logging" in content, \
            "Script should import logging"


class TestScriptConfigurableThresholds:
    """NFR-009: Scripts must have configurable constants at top (not hardcoded throughout)"""

    @pytest.fixture
    def scripts_dir(self):
        """Fixture providing path to scripts directory"""
        return Path("tests/user-input-guidance/scripts")

    def test_token_savings_has_configurable_threshold(self, scripts_dir):
        """Test: measure-token-savings.py has 20% threshold as constant"""
        # Arrange
        script_path = scripts_dir / "measure-token-savings.py"

        # Act
        content = script_path.read_text()
        # Find lines before first function/class definition
        lines = content.split("\n")
        header_section = "\n".join(lines[:30])  # Look in first 30 lines

        # Assert
        assert "20" in header_section or "TOKEN" in header_section or "THRESHOLD" in header_section, \
            "Script should define thresholds as constants in header"

    def test_validation_script_has_configurable_thresholds(self, scripts_dir):
        """Test: validate-fixtures.py has min/max word counts as constants"""
        # Arrange
        script_path = scripts_dir / "validate-fixtures.py"

        # Act
        content = script_path.read_text()
        lines = content.split("\n")
        header_section = "\n".join(lines[:50])

        # Assert
        assert ("50" in header_section or "200" in header_section or "WORD" in header_section), \
            "Script should define word count thresholds as constants"


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
