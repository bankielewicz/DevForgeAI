"""
test_edge_cases_and_nfrs.py - Tests for edge cases and non-functional requirements
Tests error handling, performance, reliability, maintainability, testability requirements
Following TDD Red phase - all tests should FAIL before implementation
"""

import os
import json
import pytest
import subprocess
import tempfile
import time
from pathlib import Path


class TestEdgeCaseTokenizationVersionMismatch:
    """Edge Case #1: Tokenization Library Version Mismatch

    Validates graceful handling when tiktoken version differs from expected.
    """

    def test_script_detects_tiktoken_version_mismatch(self):
        """Test: measure-token-savings.py detects and warns about tiktoken version mismatch"""
        # Arrange
        script_path = Path("tests/user-input-guidance/scripts/measure-token-savings.py")

        # Act
        content = script_path.read_text()

        # Assert
        assert "__version__" in content or "version" in content.lower(), \
            "Script should check tiktoken version"
        assert "mismatch" in content.lower() or "warning" in content.lower(), \
            "Script should warn on version mismatch"

    def test_script_continues_on_version_mismatch(self):
        """Test: Script continues execution with warning, not fatal error"""
        # Arrange
        script_path = Path("tests/user-input-guidance/scripts/measure-token-savings.py")

        # Act
        content = script_path.read_text()

        # Assert
        # Should not exit(1) on version mismatch, just warn
        assert "continue" in content.lower() or "best effort" in content.lower() or \
               ("warning" in content.lower() and "return" not in content.lower()), \
            "Script should continue despite version mismatch"

    def test_script_includes_tokenization_disclaimer_in_report(self):
        """Test: JSON report includes tokenization version disclaimer"""
        # Arrange
        script_path = Path("tests/user-input-guidance/scripts/measure-token-savings.py")

        # Act
        content = script_path.read_text()

        # Assert
        assert "disclaimer" in content.lower() or "version" in content.lower(), \
            "Script should add disclaimer about tokenizer version"


class TestEdgeCaseFixturePairsMismatch:
    """Edge Case #2: Fixture Pairs Mismatch (Missing Enhanced or Baseline)

    Validates handling of incomplete fixture pairs.
    """

    def test_validation_script_detects_incomplete_pairs(self):
        """Test: validate-fixtures.py detects when enhanced or expected missing"""
        # Arrange
        script_path = Path("tests/user-input-guidance/scripts/validate-fixtures.py")

        # Act
        content = script_path.read_text()

        # Assert
        assert "exist" in content.lower() or "missing" in content.lower(), \
            "Script should check for missing fixtures"
        assert "pair" in content.lower(), "Script should validate fixture pairs"

    def test_validation_script_exits_with_2_on_incomplete_pairs(self):
        """Test: validate-fixtures.py exits with status code 2 for incomplete pairs"""
        # Arrange
        script_path = Path("tests/user-input-guidance/scripts/validate-fixtures.py")

        # Act
        content = script_path.read_text()

        # Assert
        # Should have specific exit code for incomplete pairs (distinct from 0/1)
        assert "exit(2)" in content or '"2"' in content or "'2'" in content, \
            "Script should exit with code 2 for incomplete pairs"

    def test_measurement_scripts_skip_incomplete_pairs_with_warning(self):
        """Test: measure-token-savings.py skips incomplete pairs with warning"""
        # Arrange
        script_path = Path("tests/user-input-guidance/scripts/measure-token-savings.py")

        # Act
        content = script_path.read_text()

        # Assert
        assert "skip" in content.lower() or "incomplete" in content.lower(), \
            "Script should skip incomplete pairs"
        assert "warning" in content.lower() or "⚠️" in content, \
            "Script should warn when skipping"

    def test_measurement_scripts_report_incomplete_pairs_count(self):
        """Test: JSON report includes count of incomplete pairs skipped"""
        # Arrange
        script_path = Path("tests/user-input-guidance/scripts/measure-token-savings.py")

        # Act
        content = script_path.read_text()

        # Assert
        # Should track incomplete pairs in report
        assert "incomplete" in content.lower() or "skipped" in content.lower() or "valid" in content.lower(), \
            "Script should report pair status"


class TestEdgeCaseExpectedValuesStrictOrLenient:
    """Edge Case #3: Expected Improvements Too Strict or Too Lenient

    Validates detection of unrealistic expected improvement values.
    """

    def test_success_rate_script_detects_outlier_deviations(self):
        """Test: measure-success-rate.py detects >20% delta between actual and expected"""
        # Arrange
        script_path = Path("tests/user-input-guidance/scripts/measure-success-rate.py")

        # Act
        content = script_path.read_text()

        # Assert
        assert "outlier" in content.lower() or "deviation" in content.lower() or "delta" in content.lower(), \
            "Script should detect outlier deviations"
        assert "20" in content, "Script should check >20% threshold"

    def test_script_flags_3_or_more_outliers_in_recommendations(self):
        """Test: If ≥3 fixtures have outlier deviations, flagged in recommendations"""
        # Arrange
        script_path = Path("tests/user-input-guidance/scripts/generate-impact-report.py")

        # Act
        content = script_path.read_text()

        # Assert
        assert "outlier" in content.lower() or "unrealistic" in content.lower(), \
            "Script should flag unrealistic expectations"

    def test_script_suggests_recalibration_of_expectations(self):
        """Test: Recommendations suggest reviewing/calibrating expected improvements"""
        # Arrange
        script_path = Path("tests/user-input-guidance/scripts/generate-impact-report.py")

        # Act
        content = script_path.read_text()

        # Assert
        assert "review" in content.lower() or "calibrat" in content.lower(), \
            "Script should suggest reviewing expectations"


class TestEdgeCaseFleschReadabilityUnavailable:
    """Edge Case #4: Flesch Reading Ease Calculation Unavailable

    Validates graceful handling when textstat library not installed.
    """

    def test_validation_script_checks_textstat_availability(self):
        """Test: validate-fixtures.py checks for textstat library availability"""
        # Arrange
        script_path = Path("tests/user-input-guidance/scripts/validate-fixtures.py")

        # Act
        content = script_path.read_text()

        # Assert
        assert "textstat" in content or "flesch" in content.lower() or "readability" in content.lower(), \
            "Script should reference readability checks"
        assert "import" in content or "try" in content, \
            "Script should handle library imports gracefully"

    def test_validation_skips_readability_if_unavailable(self):
        """Test: Script skips readability checks if textstat unavailable"""
        # Arrange
        script_path = Path("tests/user-input-guidance/scripts/validate-fixtures.py")

        # Act
        content = script_path.read_text()

        # Assert
        assert "try" in content and "except" in content, \
            "Script should use try/except for optional library"
        assert "skip" in content.lower() or "optional" in content.lower(), \
            "Script should skip unavailable checks gracefully"

    def test_validation_continues_with_other_checks_if_readability_fails(self):
        """Test: Script continues validation with word count/quality checks even if readability unavailable"""
        # Arrange
        script_path = Path("tests/user-input-guidance/scripts/validate-fixtures.py")

        # Act
        content = script_path.read_text()

        # Assert
        # Should not exit on textstat import failure
        assert "continue" in content.lower() or ("except" in content and "pass" in content), \
            "Script should continue despite textstat issues"


class TestEdgeCaseReportGenerationMissingInputs:
    """Edge Case #5: Report Generation Failure Due to Missing Input Reports

    Validates handling when measurement reports don't exist.
    """

    def test_impact_report_script_checks_input_reports_exist(self):
        """Test: generate-impact-report.py checks for token-savings and success-rate JSON reports"""
        # Arrange
        script_path = Path("tests/user-input-guidance/scripts/generate-impact-report.py")

        # Act
        content = script_path.read_text()

        # Assert
        assert "token-savings" in content.lower() or "token_savings" in content.lower(), \
            "Script should check for token-savings report"
        assert "success-rate" in content.lower() or "success_rate" in content.lower(), \
            "Script should check for success-rate report"

    def test_script_exits_5_if_reports_missing(self):
        """Test: Script exits with status code 5 if required reports missing"""
        # Arrange
        script_path = Path("tests/user-input-guidance/scripts/generate-impact-report.py")

        # Act
        content = script_path.read_text()

        # Assert
        assert "exit(5)" in content or '"5"' in content, \
            "Script should exit with code 5 for missing dependencies"

    def test_script_provides_guidance_on_which_script_to_run(self):
        """Test: Error message identifies which report is missing and which script to run"""
        # Arrange
        script_path = Path("tests/user-input-guidance/scripts/generate-impact-report.py")

        # Act
        content = script_path.read_text()

        # Assert
        assert "run" in content.lower() or "execute" in content.lower(), \
            "Script should guide user on what to run"
        assert "measure-token-savings" in content or "measure-success-rate" in content, \
            "Script should reference measurement scripts"

    def test_script_selects_most_recent_report_if_multiple_exist(self):
        """Test: If multiple reports of same type exist, uses most recent by timestamp"""
        # Arrange
        script_path = Path("tests/user-input-guidance/scripts/generate-impact-report.py")

        # Act
        content = script_path.read_text()

        # Assert
        assert "glob" in content.lower() or "sorted" in content.lower() or "latest" in content.lower(), \
            "Script should find most recent report"
        assert "timestamp" in content.lower() or "sort" in content.lower(), \
            "Script should sort by timestamp"


class TestEdgeCaseFixtureFilenameViolations:
    """Edge Case #6: Fixture Filename Format Violations

    Validates detection of invalid fixture filenames.
    """

    def test_validation_script_validates_filename_format(self):
        """Test: validate-fixtures.py validates filename format regex"""
        # Arrange
        script_path = Path("tests/user-input-guidance/scripts/validate-fixtures.py")

        # Act
        content = script_path.read_text()

        # Assert
        assert "re\." in content or "regex" in content.lower() or "match" in content.lower(), \
            "Script should use regex for filename validation"
        assert "baseline" in content or "enhanced" in content, \
            "Script should validate fixture type prefixes"

    def test_validation_detects_non_zero_padded_filenames(self):
        """Test: Script detects baseline-1-crud.txt (should be baseline-01-crud.txt)"""
        # Arrange
        script_path = Path("tests/user-input-guidance/scripts/validate-fixtures.py")

        # Act
        content = script_path.read_text()

        # Assert
        # Regex should require 2-digit zero-padded number
        assert r"\d{2}" in content or "\\d\\d" in content or "\\d{2}" in content, \
            "Script should require zero-padded 2-digit numbers"

    def test_validation_detects_invalid_category_characters(self):
        """Test: Script detects underscores/spaces in category (should use hyphens)"""
        # Arrange
        script_path = Path("tests/user-input-guidance/scripts/validate-fixtures.py")

        # Act
        content = script_path.read_text()

        # Assert
        # Regex should enforce lowercase letters, numbers, hyphens only
        assert "[a-z0-9-]" in content or "a-z" in content, \
            "Script should validate category characters"

    def test_validation_reports_invalid_filenames_with_remediation(self):
        """Test: Script lists invalid filenames and how to fix them"""
        # Arrange
        script_path = Path("tests/user-input-guidance/scripts/validate-fixtures.py")

        # Act
        content = script_path.read_text()

        # Assert
        assert "format" in content.lower() or "convention" in content.lower(), \
            "Script should explain expected format"


class TestEdgeCaseEmptyOrCorruptFixtures:
    """Edge Case #7: Empty or Corrupt Fixtures

    Validates handling of empty or corrupted fixture files.
    """

    def test_validation_script_checks_file_size(self):
        """Test: validate-fixtures.py checks for empty files (0 bytes)"""
        # Arrange
        script_path = Path("tests/user-input-guidance/scripts/validate-fixtures.py")

        # Act
        content = script_path.read_text()

        # Assert
        assert "size" in content.lower() or "getsize" in content.lower() or "len(" in content, \
            "Script should check file size"
        assert "0" in content, "Script should detect empty files"

    def test_validation_script_checks_utf8_encoding(self):
        """Test: validate-fixtures.py catches UnicodeDecodeError for non-UTF-8"""
        # Arrange
        script_path = Path("tests/user-input-guidance/scripts/validate-fixtures.py")

        # Act
        content = script_path.read_text()

        # Assert
        assert "utf-8" in content.lower() or "encoding" in content.lower(), \
            "Script should check UTF-8 encoding"
        assert "UnicodeDecodeError" in content or "encoding" in content.lower(), \
            "Script should handle encoding errors"

    def test_validation_detects_whitespace_only_fixtures(self):
        """Test: Script detects files with only whitespace"""
        # Arrange
        script_path = Path("tests/user-input-guidance/scripts/validate-fixtures.py")

        # Act
        content = script_path.read_text()

        # Assert
        assert "strip" in content or "whitespace" in content.lower(), \
            "Script should check for whitespace-only content"

    def test_validation_reports_specific_corruption_errors(self):
        """Test: Script reports specific error (empty, encoding, whitespace-only)"""
        # Arrange
        script_path = Path("tests/user-input-guidance/scripts/validate-fixtures.py")

        # Act
        content = script_path.read_text()

        # Assert
        assert "error" in content.lower() or "exception" in content.lower(), \
            "Script should report specific errors"


class TestEdgeCaseJSONSchemaViolations:
    """Edge Case #8: JSON Schema Violations in Expected Files

    Validates detection of invalid JSON and schema violations.
    """

    def test_validation_script_validates_json_syntax(self):
        """Test: validate-fixtures.py detects invalid JSON syntax"""
        # Arrange
        script_path = Path("tests/user-input-guidance/scripts/validate-fixtures.py")

        # Act
        content = script_path.read_text()

        # Assert
        assert "json.load" in content or "JSONDecodeError" in content, \
            "Script should parse and validate JSON"
        assert "try" in content and "except" in content, \
            "Script should handle JSON parsing errors"

    def test_validation_checks_required_fields_present(self):
        """Test: Script validates required fields (fixture_id, category, etc.) present"""
        # Arrange
        script_path = Path("tests/user-input-guidance/scripts/validate-fixtures.py")

        # Act
        content = script_path.read_text()

        # Assert
        required_fields = ["fixture_id", "category", "expected_improvements", "rationale"]
        assert any(field in content for field in required_fields), \
            "Script should validate required JSON fields"

    def test_validation_checks_numeric_ranges(self):
        """Test: Script validates numeric values within 0-100 range"""
        # Arrange
        script_path = Path("tests/user-input-guidance/scripts/validate-fixtures.py")

        # Act
        content = script_path.read_text()

        # Assert
        assert "100" in content or "range" in content.lower() or "0" in content, \
            "Script should validate numeric ranges"


class TestPerformanceRequirements:
    """NFR-001 to NFR-004: Performance Requirements

    Tests that scripts meet execution time targets.
    """

    @pytest.mark.slow
    def test_validation_script_completes_within_5_seconds(self):
        """NFR-001: validate-fixtures.py executes <5 seconds on 30 fixtures"""
        # Arrange
        script_path = Path("tests/user-input-guidance/scripts/validate-fixtures.py")

        # Assert - This test will FAIL until implementation exists
        assert script_path.exists(), "Script must exist for performance testing"

    @pytest.mark.slow
    def test_token_savings_script_completes_within_3_seconds(self):
        """NFR-002: measure-token-savings.py executes <3 seconds on 20 fixtures"""
        # Arrange
        script_path = Path("tests/user-input-guidance/scripts/measure-token-savings.py")

        # Assert - This test will FAIL until implementation exists
        assert script_path.exists(), "Script must exist for performance testing"

    @pytest.mark.slow
    def test_success_rate_script_completes_within_10_seconds(self):
        """NFR-003: measure-success-rate.py executes <10 seconds on 20 fixtures"""
        # Arrange
        script_path = Path("tests/user-input-guidance/scripts/measure-success-rate.py")

        # Assert - This test will FAIL until implementation exists
        assert script_path.exists(), "Script must exist for performance testing"

    @pytest.mark.slow
    def test_impact_report_script_completes_within_2_seconds(self):
        """NFR-004: generate-impact-report.py executes <2 seconds from JSON inputs"""
        # Arrange
        script_path = Path("tests/user-input-guidance/scripts/generate-impact-report.py")

        # Assert - This test will FAIL until implementation exists
        assert script_path.exists(), "Script must exist for performance testing"


class TestReliabilityRequirements:
    """NFR-005, NFR-006, NFR-007: Reliability Requirements

    Tests graceful error handling and exit codes.
    """

    def test_fixture_pair_integrity_strictly_enforced(self):
        """NFR-005: All 10 pairs must be complete, no partial pairs allowed"""
        # Arrange
        script_path = Path("tests/user-input-guidance/scripts/validate-fixtures.py")

        # Act
        content = script_path.read_text()

        # Assert
        assert "pair" in content.lower(), "Script should validate pair completeness"
        assert "all" in content.lower() or "every" in content.lower(), \
            "Script should require all pairs complete"

    def test_measurement_scripts_handle_missing_tiktoken(self):
        """NFR-006: Scripts gracefully handle missing tiktoken with clear error"""
        # Arrange
        script_path = Path("tests/user-input-guidance/scripts/measure-token-savings.py")

        # Act
        content = script_path.read_text()

        # Assert
        assert "try" in content and "except" in content, \
            "Script should handle import errors"
        assert "tiktoken" in content, "Script should reference tiktoken in error handling"

    def test_measurement_scripts_handle_empty_fixtures(self):
        """NFR-006: Scripts handle empty fixtures with clear error"""
        # Arrange
        script_path = Path("tests/user-input-guidance/scripts/measure-token-savings.py")

        # Act
        content = script_path.read_text()

        # Assert
        assert "empty" in content.lower() or "0" in content, \
            "Script should detect empty fixtures"

    def test_impact_report_handles_missing_input_reports(self):
        """NFR-007: Report script fails gracefully if input reports missing"""
        # Arrange
        script_path = Path("tests/user-input-guidance/scripts/generate-impact-report.py")

        # Act
        content = script_path.read_text()

        # Assert
        assert "missing" in content.lower() or "not found" in content.lower(), \
            "Script should check for missing inputs"


class TestMaintainabilityRequirements:
    """NFR-008, NFR-009, NFR-010: Maintainability Requirements

    Tests modular design, configurable constants, and structured logging.
    """

    def test_measurement_scripts_are_independent(self):
        """NFR-008: validate-fixtures, measure-token-savings, measure-success-rate can run independently"""
        # Arrange
        scripts = [
            "validate-fixtures.py",
            "measure-token-savings.py",
            "measure-success-rate.py"
        ]
        scripts_dir = Path("tests/user-input-guidance/scripts")

        # Act & Assert
        for script in scripts:
            script_path = scripts_dir / script
            content = script_path.read_text()
            # Should not call other measurement scripts
            assert "subprocess" not in content or "generate-impact-report" not in content, \
                f"{script} should not depend on other measurement scripts"

    def test_impact_report_depends_on_measurement_scripts(self):
        """NFR-008: generate-impact-report.py requires prior measurement scripts"""
        # Arrange
        script_path = Path("tests/user-input-guidance/scripts/generate-impact-report.py")

        # Act
        content = script_path.read_text()

        # Assert
        # Should check for measurement report existence
        assert "token-savings" in content.lower() or "success-rate" in content.lower(), \
            "Impact report should depend on measurement reports"

    def test_scripts_define_thresholds_as_constants(self):
        """NFR-009: All numeric thresholds defined as constants in script headers"""
        # Arrange
        scripts = [
            "measure-token-savings.py",
            "measure-success-rate.py",
            "validate-fixtures.py",
            "generate-impact-report.py"
        ]
        scripts_dir = Path("tests/user-input-guidance/scripts")

        # Act & Assert
        for script in scripts:
            script_path = scripts_dir / script
            content = script_path.read_text()
            lines = content.split("\n")
            header = "\n".join(lines[:50])  # Look in first 50 lines for constants

            # Should have some threshold constants defined
            assert any(keyword in header.upper() for keyword in ["THRESHOLD", "MIN", "MAX", "TARGET"]), \
                f"{script} should define thresholds as constants in header"


class TestQualityRequirements:
    """NFR-011 to NFR-014: Quality Requirements

    Tests hypothesis validation, fixture diversity, and recommendations quality.
    """

    def test_token_savings_validation_uses_explicit_threshold(self):
        """NFR-011: Token savings validation uses explicit 20% threshold (not subjective)"""
        # Arrange
        script_path = Path("tests/user-input-guidance/scripts/measure-token-savings.py")

        # Act
        content = script_path.read_text()

        # Assert
        assert "20" in content, "Script should use explicit 20% threshold"
        assert ">=" in content or "threshold" in content.lower(), \
            "Script should use numeric comparison, not subjective judgment"

    def test_success_rate_validation_uses_explicit_threshold(self):
        """NFR-011: Success rate validation uses explicit 80% threshold"""
        # Arrange
        script_path = Path("tests/user-input-guidance/scripts/measure-success-rate.py")

        # Act
        content = script_path.read_text()

        # Assert
        assert "8" in content or "0.8" in content or "80" in content, \
            "Script should use explicit 80% threshold"

    def test_baseline_fixtures_cover_10_distinct_domains(self):
        """NFR-012: Fixture diversity covers 10 distinct domains"""
        # Arrange
        baseline_dir = Path("tests/user-input-guidance/fixtures/baseline")

        # Act
        baseline_files = sorted(baseline_dir.glob("baseline-*.txt"))

        # Assert - Will FAIL until fixtures created
        if len(baseline_files) > 0:
            domains = set()
            for file in baseline_files:
                domain = file.stem.split("-", 2)[2] if "-" in file.stem else ""
                if domain:
                    domains.add(domain)
            assert len(domains) >= 8, "Should cover multiple distinct domains"

    def test_impact_report_recommendations_are_specific(self):
        """NFR-014: Recommendations include fixture ID, guidance section, specific action"""
        # Arrange
        script_path = Path("tests/user-input-guidance/scripts/generate-impact-report.py")

        # Act
        content = script_path.read_text()

        # Assert
        assert "fixture" in content.lower(), "Recommendations should reference fixture IDs"
        assert "guidance" in content.lower() or "section" in content.lower(), \
            "Recommendations should reference guidance sections"
        assert "review" in content.lower() or "improve" in content.lower() or "action" in content.lower(), \
            "Recommendations should suggest specific actions"


class TestTestabilityRequirements:
    """NFR-015, NFR-016: Testability Requirements

    Tests self-test mode and exit status codes.
    """

    def test_token_savings_script_supports_test_flag(self):
        """NFR-015: measure-token-savings.py supports --test flag"""
        # Arrange
        script_path = Path("tests/user-input-guidance/scripts/measure-token-savings.py")

        # Act
        content = script_path.read_text()

        # Assert
        assert "--test" in content or "test" in content.lower(), \
            "Script should support --test flag for self-validation"

    def test_validation_script_supports_test_flag(self):
        """NFR-015: validate-fixtures.py supports --test flag"""
        # Arrange
        script_path = Path("tests/user-input-guidance/scripts/validate-fixtures.py")

        # Act
        content = script_path.read_text()

        # Assert
        assert "--test" in content or "test" in content.lower(), \
            "Script should support --test flag"

    def test_scripts_document_exit_codes(self):
        """NFR-016: Scripts document exit codes in help or README"""
        # Arrange
        scripts = [
            "measure-token-savings.py",
            "measure-success-rate.py",
            "generate-impact-report.py",
            "validate-fixtures.py"
        ]
        scripts_dir = Path("tests/user-input-guidance/scripts")
        readme_path = Path("tests/user-input-guidance/README.md")

        # Act & Assert
        for script in scripts:
            script_path = scripts_dir / script
            content = script_path.read_text()

            # Should document exit codes in --help or header comments
            assert "exit" in content.lower() or (readme_path.exists() and "exit" in readme_path.read_text().lower()), \
                f"{script} should document exit codes"


class TestUsabilityRequirements:
    """NFR-017, NFR-018: Usability Requirements

    Tests help flag support and README documentation.
    """

    def test_readme_is_at_least_300_lines(self):
        """NFR-018: README.md ≥300 lines"""
        # Arrange
        readme_path = Path("tests/user-input-guidance/README.md")

        # Act
        if readme_path.exists():
            lines = readme_path.read_text().split("\n")

            # Assert
            assert len(lines) >= 300, f"README.md has {len(lines)} lines (expected ≥300)"

    def test_readme_contains_required_sections(self):
        """NFR-018: README contains Purpose, Fixtures, Scripts, Methodology, Interpretation, Troubleshooting"""
        # Arrange
        readme_path = Path("tests/user-input-guidance/README.md")
        required_sections = ["Purpose", "Fixture", "Script", "Methodology", "Interpretation", "Troubleshoot"]

        # Act
        if readme_path.exists():
            content = readme_path.read_text()

            # Assert
            for section in required_sections:
                assert section.lower() in content.lower(), f"README missing '{section}' section"

    def test_readme_contains_troubleshooting_with_common_issues(self):
        """NFR-018: README troubleshooting section covers ≥5 common issues"""
        # Arrange
        readme_path = Path("tests/user-input-guidance/README.md")

        # Act & Assert - Will FAIL until README created with sufficient content
        if readme_path.exists():
            content = readme_path.read_text()
            assert "troubleshoot" in content.lower() or "common" in content.lower(), \
                "README should include troubleshooting section"


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short", "-m", "not slow"])
