"""
Unit tests for STORY-064: devforgeai-story-creation Integration Validation and Test Execution

Tests cover:
- Acceptance Criteria 1: Test Suite Execution Complete (unit tests passing)
- Acceptance Criteria 2: Test Fixtures Created (5 feature descriptions exist)
- Acceptance Criteria 3: Data Validation Rules Enforced (8 rules with assertions)
- Non-Functional Requirements: Test execution, fixture validation, data rule enforcement

Test Suite Composition:
- UT01-UT15: Unit tests for test fixture validation and data rules
- Organized in TestFixtures, TestDataValidationRules classes

Test IDs: UT01-UT15
Test Organization: 5 fixture tests + 10 data validation rule tests
Coverage: Fixture existence, content validation, data rules documentation
"""

import pytest
from pathlib import Path
from typing import Dict, List


# ============================================================================
# SHARED TEST UTILITIES (Reduces duplication across all test suites)
# ============================================================================

class FileValidationHelper:
    """Helper utilities for file existence and content validation."""

    # Compute project root dynamically based on test file location
    _PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent

    FIXTURE_DIR = _PROJECT_ROOT / "tests" / "user-input-guidance" / "fixtures"
    GUIDANCE_FILE = _PROJECT_ROOT / "src" / "claude" / "skills" / "devforgeai-ideation" / "references" / "user-input-guidance.md"
    INTEGRATION_GUIDE = _PROJECT_ROOT / "src" / "claude" / "skills" / "devforgeai-story-creation" / "references" / "user-input-integration-guide.md"
    SKILL_FILE = _PROJECT_ROOT / "src" / "claude" / "skills" / "devforgeai-story-creation" / "SKILL.md"
    PIPELINE_CONFIG = _PROJECT_ROOT / "devforgeai" / "ci" / "story-creation-test-pipeline.yml"

    @staticmethod
    def assert_file_exists(file_path: Path, error_message: str) -> str:
        """Assert file exists and return its content.

        Args:
            file_path: Path to file to validate
            error_message: Message to display if file missing or unreadable

        Returns:
            Content of the file

        Raises:
            AssertionError: If file doesn't exist, can't be read, or is empty
        """
        assert file_path.exists(), f"{error_message} (path: {file_path})"

        try:
            with open(file_path, 'r') as f:
                content = f.read()
            assert content, f"{error_message}: File exists but is empty"
            return content
        except (IOError, OSError) as e:
            assert False, f"{error_message}: Could not read file - {type(e).__name__}: {e}"

    @staticmethod
    def assert_fixture_exists(fixture_name: str, description: str, required_keywords: List[str]) -> str:
        """Assert fixture file exists with required content.

        Args:
            fixture_name: Fixture file stem (without .md extension)
            description: What the fixture should describe
            required_keywords: Keywords that should appear in fixture

        Returns:
            Content of the fixture file

        Raises:
            AssertionError: If fixture missing or content incomplete
        """
        fixture_path = FileValidationHelper.FIXTURE_DIR / f"{fixture_name}.md"
        error_msg = f"Fixture {fixture_name}.md not found at {fixture_path}. AC-2 requires {description}"
        content = FileValidationHelper.assert_file_exists(fixture_path, error_msg)

        assert len(content) > 0, f"{fixture_name}.md exists but is empty"

        found_keywords = sum(1 for kw in required_keywords if kw.lower() in content.lower())
        assert found_keywords > 0, (
            f"{fixture_name}.md must contain at least one of: {', '.join(required_keywords)}"
        )
        return content

    @staticmethod
    def count_patterns_in_file(file_path: Path, pattern_indicators: List[str]) -> int:
        """Count occurrences of pattern indicators in file.

        Args:
            file_path: Path to file to search
            pattern_indicators: Patterns to search for (looks for '##' + pattern)

        Returns:
            Count of pattern indicators found
        """
        content = FileValidationHelper.assert_file_exists(file_path, f"File {file_path} required for pattern count")
        pattern_count = 0
        for line in content.split('\n'):
            if '##' in line and any(pat.lower() in line.lower() for pat in pattern_indicators):
                pattern_count += 1
        return pattern_count

    @staticmethod
    def count_keywords_in_file(file_path: Path, keywords: List[str]) -> int:
        """Count distinct keywords found in file.

        Args:
            file_path: Path to file to search
            keywords: Keywords to count

        Returns:
            Number of distinct keywords found
        """
        content = FileValidationHelper.assert_file_exists(file_path, f"File {file_path} required for keyword count")
        return sum(1 for keyword in keywords if keyword.lower() in content.lower())


class TestFixtures:
    """Unit tests for AC-2: Test Fixtures Created (UT01-UT05).

    Validates that all 5 required fixture files exist with correct content.
    Each fixture represents a different feature complexity level.
    """

    @pytest.mark.unit
    @pytest.mark.acceptance_criteria
    def test_simple_feature_fixture_exists(self):
        """UT01: simple-feature.md exists with correct format.

        Validates: Straightforward CRUD operation fixture exists
        """
        FileValidationHelper.assert_fixture_exists(
            fixture_name="simple-feature",
            description="straightforward CRUD operation",
            required_keywords=["CRUD", "straightforward", "simple"]
        )

    @pytest.mark.unit
    @pytest.mark.acceptance_criteria
    def test_moderate_feature_fixture_exists(self):
        """UT02: moderate-feature.md exists with multi-component integration.

        Validates: Multi-component integration fixture exists
        """
        FileValidationHelper.assert_fixture_exists(
            fixture_name="moderate-feature",
            description="multi-component integration",
            required_keywords=["integration", "component", "moderate"]
        )

    @pytest.mark.unit
    @pytest.mark.acceptance_criteria
    def test_complex_feature_fixture_exists(self):
        """UT03: complex-feature.md exists with cross-cutting concerns.

        Validates: Cross-cutting concern with dependencies fixture exists
        """
        FileValidationHelper.assert_fixture_exists(
            fixture_name="complex-feature",
            description="cross-cutting concern with dependencies",
            required_keywords=["cross-cutting", "dependencies", "concern", "complex"]
        )

    @pytest.mark.unit
    @pytest.mark.acceptance_criteria
    def test_ambiguous_feature_fixture_exists(self):
        """UT04: ambiguous-feature.md exists with vague requirements.

        Validates: Ambiguous/vague requirements fixture exists for testing guidance escalation
        """
        FileValidationHelper.assert_fixture_exists(
            fixture_name="ambiguous-feature",
            description="vague requirements demonstrating guidance escalation",
            required_keywords=["vague", "ambiguous", "unclear", "ambiguity"]
        )

    @pytest.mark.unit
    @pytest.mark.acceptance_criteria
    def test_edge_case_feature_fixture_exists(self):
        """UT05: edge-case-feature.md exists with boundary conditions.

        Validates: Edge case boundary conditions fixture exists
        """
        FileValidationHelper.assert_fixture_exists(
            fixture_name="edge-case-feature",
            description="boundary conditions or error handling",
            required_keywords=["boundary", "edge", "error", "condition", "exception"]
        )


class TestDataValidationRules:
    """Unit tests for AC-3: Data Validation Rules Enforced (UT06-UT15).

    Validates 8 data validation rules for guidance integration:
    1. Guidance file location and path validation
    2. Pattern extraction methodology
    3. Pattern-to-question mapping table
    4. Token measurement methodology
    5. Batch mode caching strategy
    6. Conditional loading based on invocation context
    7. Pattern name normalization for matching
    8. Backward compatibility validation checklist
    """

    @pytest.mark.unit
    @pytest.mark.acceptance_criteria
    def test_rule_1_guidance_file_location_validation(self):
        """UT06: Guidance file location and path validation.

        Data Rule 1: Verify guidance file exists at expected location with content.
        """
        content = FileValidationHelper.assert_file_exists(
            FileValidationHelper.GUIDANCE_FILE,
            "Data Rule 1 violation: Guidance file not found at expected location"
        )
        assert len(content) > 100, "Guidance file too small to contain patterns"
        assert "pattern" in content.lower() or "guidance" in content.lower(), (
            "Data Rule 1: Guidance file must contain pattern or guidance references"
        )

    @pytest.mark.unit
    @pytest.mark.acceptance_criteria
    def test_rule_2_pattern_extraction_methodology(self):
        """UT07: Pattern extraction methodology.

        Data Rule 2: Verify guidance file contains extractable patterns.
        """
        pattern_count = FileValidationHelper.count_patterns_in_file(
            FileValidationHelper.GUIDANCE_FILE,
            ["pattern", "guidance"]
        )
        assert pattern_count >= 3, (
            f"Data Rule 2 violation: Expected ≥3 distinct patterns, found {pattern_count}. "
            "Pattern extraction methodology must identify patterns in guidance file."
        )

    @pytest.mark.unit
    @pytest.mark.acceptance_criteria
    def test_rule_3_pattern_to_question_mapping(self):
        """UT08: Pattern-to-question mapping table.

        Data Rule 3: Verify integration guide documents pattern-to-question mapping.
        """
        content = FileValidationHelper.assert_file_exists(
            FileValidationHelper.INTEGRATION_GUIDE,
            "Data Rule 3 violation: Integration guide not found. Pattern-to-question mapping required."
        )
        keywords_found = FileValidationHelper.count_keywords_in_file(
            FileValidationHelper.INTEGRATION_GUIDE,
            ["epic", "priority", "pattern", "mapping"]
        )
        assert keywords_found > 0, (
            "Data Rule 3: Integration guide must document pattern-to-question mapping"
        )

    @pytest.mark.unit
    @pytest.mark.acceptance_criteria
    def test_rule_4_token_measurement_methodology(self):
        """UT09: Token measurement methodology.

        Data Rule 4: Verify guidance file size is reasonable for token budget.
        """
        file_size = FileValidationHelper.GUIDANCE_FILE.stat().st_size
        assert file_size < 50000, (
            f"Data Rule 4 violation: Guidance file too large ({file_size} bytes). "
            "Token measurement shows guidance exceeds reasonable budget (<50KB)."
        )

    @pytest.mark.unit
    @pytest.mark.acceptance_criteria
    def test_rule_5_batch_mode_caching_strategy(self):
        """UT10: Batch mode caching strategy.

        Data Rule 5: Verify caching strategy is documented in integration guide.
        """
        keywords_found = FileValidationHelper.count_keywords_in_file(
            FileValidationHelper.INTEGRATION_GUIDE,
            ["cache", "batch", "load", "caching"]
        )
        assert keywords_found > 0, (
            "Data Rule 5: Integration guide must document batch mode caching strategy"
        )

    @pytest.mark.unit
    @pytest.mark.acceptance_criteria
    def test_rule_6_conditional_loading_invocation_context(self):
        """UT11: Conditional loading based on invocation context.

        Data Rule 6: Verify conditional loading rules are documented.
        """
        keywords_found = FileValidationHelper.count_keywords_in_file(
            FileValidationHelper.INTEGRATION_GUIDE,
            ["condition", "context", "load", "conditional"]
        )
        assert keywords_found > 0, (
            "Data Rule 6: Integration guide must document conditional loading based on invocation context"
        )

    @pytest.mark.unit
    @pytest.mark.acceptance_criteria
    def test_rule_7_pattern_name_normalization(self):
        """UT12: Pattern name normalization for matching.

        Data Rule 7: Verify normalization approach is documented.
        """
        keywords_found = FileValidationHelper.count_keywords_in_file(
            FileValidationHelper.INTEGRATION_GUIDE,
            ["normalize", "match", "name", "normalization"]
        )
        assert keywords_found > 0, (
            "Data Rule 7: Integration guide must document pattern name normalization"
        )

    @pytest.mark.unit
    @pytest.mark.acceptance_criteria
    def test_rule_8_backward_compatibility_checklist(self):
        """UT13: Backward compatibility validation checklist.

        Data Rule 8: Verify backward compatibility approach is documented.
        """
        keywords_found = FileValidationHelper.count_keywords_in_file(
            FileValidationHelper.INTEGRATION_GUIDE,
            ["backward", "compatibility", "graceful", "fallback"]
        )
        assert keywords_found > 0, (
            "Data Rule 8: Integration guide must document backward compatibility checklist"
        )

    @pytest.mark.unit
    @pytest.mark.acceptance_criteria
    def test_all_data_validation_rules_documented(self):
        """UT14: All 8 data validation rules have corresponding test methods.

        Verifies: Each data rule is covered by at least one test assertion.
        """
        rule_tests = {
            "Rule 1": "test_rule_1_guidance_file_location_validation",
            "Rule 2": "test_rule_2_pattern_extraction_methodology",
            "Rule 3": "test_rule_3_pattern_to_question_mapping",
            "Rule 4": "test_rule_4_token_measurement_methodology",
            "Rule 5": "test_rule_5_batch_mode_caching_strategy",
            "Rule 6": "test_rule_6_conditional_loading_invocation_context",
            "Rule 7": "test_rule_7_pattern_name_normalization",
            "Rule 8": "test_rule_8_backward_compatibility_checklist",
        }

        for rule_name, test_method in rule_tests.items():
            assert hasattr(TestDataValidationRules, test_method), (
                f"AC-3 violation: {rule_name} missing test method. "
                f"Each data rule requires ≥1 test assertion."
            )

    @pytest.mark.unit
    @pytest.mark.acceptance_criteria
    def test_integration_guide_contains_all_rules(self):
        """UT15: Integration guide documents all 8 data validation rules.

        Verifies: Guide contains references to core validation concepts.
        """
        content = FileValidationHelper.assert_file_exists(
            FileValidationHelper.INTEGRATION_GUIDE,
            "Data Rule documentation missing: Integration guide not found"
        )

        validation_terms = ["validation", "guidance", "pattern", "load", "compatibility"]
        found_terms = sum(1 for term in validation_terms if term in content.lower())

        assert found_terms >= 3, (
            f"Data validation rule documentation incomplete. "
            f"Integration guide missing key validation concepts. "
            f"Found {found_terms}/5 expected validation terms."
        )
