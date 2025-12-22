"""
Test suite for GrepFallbackAnalyzer - STORY-115 AC#3.

TDD Test-First Implementation for grep-based pattern matching fallback.
"""

import os
import sys
import json
import pytest
import logging
from pathlib import Path
from unittest.mock import Mock, patch

# Imports will work because conftest.py adds src/ to sys.path
from claude.scriptsdevforgeai_cli.validators.grep_fallback import (
    GrepFallbackAnalyzer,
    log_fallback_warning,
    GrepPattern,
    Violation
)

# Fixtures directory
FIXTURES_DIR = Path(__file__).parent.parent / "fixtures"


# =============================================================================
# Phase 5: Grep Fallback Tests (7 tests) - AC#3
# =============================================================================

class TestPatternMatching:
    """Test grep-based pattern detection."""

    @pytest.fixture
    def analyzer(self):
        """Fixture: Create GrepFallbackAnalyzer instance."""
        return GrepFallbackAnalyzer()

    def test_analyze_file_sql_injection(self, analyzer):
        """Test: Detect SQL injection pattern in test fixture."""
        fixture_path = FIXTURES_DIR / "ast_grep_sql_injection_sample.py"

        violations = analyzer.analyze_file(str(fixture_path))

        # Should find at least one SQL injection violation
        assert len(violations) > 0
        sql_violations = [v for v in violations if "sql" in v.get("rule_id", "").lower()
                         or "sql" in v.get("message", "").lower()]
        assert len(sql_violations) > 0

    def test_analyze_file_clean_code(self, analyzer):
        """Test: No false positives on clean code fixture."""
        fixture_path = FIXTURES_DIR / "ast_grep_clean_code_sample.py"

        violations = analyzer.analyze_file(str(fixture_path))

        # Should find no violations in clean code
        assert len(violations) == 0

    def test_analyze_directory_recursive(self, analyzer):
        """Test: Scans all files in directory recursively."""
        violations = analyzer.analyze_directory(str(FIXTURES_DIR))

        # Should find violations from sql_injection and hardcoded_secret fixtures
        assert len(violations) > 0

        # Check that multiple files were scanned
        files_with_violations = set(v.get("file") for v in violations)
        assert len(files_with_violations) >= 1


class TestOutputFormatting:
    """Test output format generation."""

    @pytest.fixture
    def analyzer(self):
        """Fixture: Create GrepFallbackAnalyzer instance."""
        return GrepFallbackAnalyzer()

    @pytest.fixture
    def sample_violations(self):
        """Fixture: Sample violation list for formatting tests."""
        return [
            {
                "file": "test.py",
                "line": 10,
                "column": 5,
                "rule_id": "SEC-001",
                "severity": "CRITICAL",
                "message": "SQL injection detected",
                "evidence": 'query = "SELECT * FROM users WHERE id = " + user_id',
                "analysis_method": "grep-fallback"
            },
            {
                "file": "config.py",
                "line": 25,
                "column": 1,
                "rule_id": "SEC-002",
                "severity": "HIGH",
                "message": "Hardcoded secret detected",
                "evidence": 'API_KEY = "sk-abc123"',
                "analysis_method": "grep-fallback"
            }
        ]

    def test_format_json_output(self, analyzer, sample_violations):
        """Test: JSON output is valid and matches schema."""
        result = analyzer.format_results(sample_violations, format="json")

        # Should be valid JSON
        parsed = json.loads(result)

        # Check schema
        assert "violations" in parsed
        assert "analysis_method" in parsed
        assert "summary" in parsed
        assert parsed["analysis_method"] == "grep-fallback"
        assert len(parsed["violations"]) == 2

    def test_format_text_output(self, analyzer, sample_violations):
        """Test: Text output is human-readable."""
        result = analyzer.format_results(sample_violations, format="text")

        # Should contain key information
        assert "test.py" in result
        assert "10" in result  # Line number
        assert "SQL injection" in result
        assert "CRITICAL" in result

    def test_analysis_method_field(self, analyzer):
        """Test: All violations have analysis_method='grep-fallback'."""
        fixture_path = FIXTURES_DIR / "ast_grep_sql_injection_sample.py"

        violations = analyzer.analyze_file(str(fixture_path))

        for violation in violations:
            assert violation.get("analysis_method") == "grep-fallback"

    def test_fallback_warning_logged(self, caplog):
        """Test: Warning about reduced accuracy is logged."""
        with caplog.at_level(logging.WARNING):
            log_fallback_warning()

        # Check warning was logged
        assert len(caplog.records) > 0
        warning_text = caplog.text.lower()
        assert "fallback" in warning_text or "accuracy" in warning_text or "60" in warning_text


# =============================================================================
# Additional Pattern Tests
# =============================================================================

class TestSecurityPatterns:
    """Test built-in security pattern detection."""

    @pytest.fixture
    def analyzer(self):
        """Fixture: Create GrepFallbackAnalyzer instance."""
        return GrepFallbackAnalyzer()

    def test_detect_hardcoded_secrets(self, analyzer):
        """Test: Detect hardcoded secrets in fixture."""
        fixture_path = FIXTURES_DIR / "ast_grep_hardcoded_secret_sample.py"

        violations = analyzer.analyze_file(str(fixture_path))

        # Should find secret violations
        secret_violations = [v for v in violations
                           if "secret" in v.get("message", "").lower()
                           or "key" in v.get("message", "").lower()
                           or "password" in v.get("message", "").lower()]
        assert len(secret_violations) > 0

    def test_filter_by_category(self, analyzer):
        """Test: Category filter works correctly."""
        violations = analyzer.analyze_directory(
            str(FIXTURES_DIR),
            category="security"
        )

        # All violations should be security-related
        for violation in violations:
            assert (violation.get("category") == "security"
                   or "SEC" in violation.get("rule_id", ""))

    def test_filter_by_language(self, analyzer):
        """Test: Language filter works correctly."""
        violations = analyzer.analyze_directory(
            str(FIXTURES_DIR),
            language="python"
        )

        # All violations should be from Python files
        for violation in violations:
            assert violation.get("file", "").endswith(".py")


class TestEdgeCases:
    """Test edge cases and error handling."""

    @pytest.fixture
    def analyzer(self):
        """Fixture: Create GrepFallbackAnalyzer instance."""
        return GrepFallbackAnalyzer()

    def test_analyze_nonexistent_file(self, analyzer):
        """Test: Graceful handling of nonexistent file."""
        violations = analyzer.analyze_file("/nonexistent/path/file.py")

        # Should return empty list, not raise exception
        assert violations == []

    def test_analyze_empty_directory(self, analyzer, tmp_path):
        """Test: Graceful handling of empty directory."""
        empty_dir = tmp_path / "empty"
        empty_dir.mkdir()

        violations = analyzer.analyze_directory(str(empty_dir))

        assert violations == []

    def test_analyze_binary_file(self, analyzer, tmp_path):
        """Test: Graceful handling of binary file."""
        binary_file = tmp_path / "binary.bin"
        binary_file.write_bytes(b"\x00\x01\x02\x03\xff\xfe")

        violations = analyzer.analyze_file(str(binary_file))

        # Should handle gracefully (skip or return empty)
        assert isinstance(violations, list)

    def test_format_markdown_output(self, analyzer):
        """Test: Markdown output format."""
        violations = [
            {
                "file": "test.py",
                "line": 10,
                "column": 5,
                "rule_id": "SEC-001",
                "severity": "CRITICAL",
                "message": "SQL injection detected",
                "evidence": "unsafe code here",
                "analysis_method": "grep-fallback"
            }
        ]

        result = analyzer.format_results(violations, format="markdown")

        # Should contain markdown formatting
        assert "#" in result or "**" in result or "`" in result
        assert "SEC-001" in result
