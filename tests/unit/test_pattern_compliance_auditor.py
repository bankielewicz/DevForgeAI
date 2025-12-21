"""
Unit tests for pattern-compliance-auditor subagent.

Tests violation detection, classification, budget analysis, and roadmap generation.
"""

import pytest
from pathlib import Path
import sys

# Add fixtures to path
sys.path.insert(0, str(Path(__file__).parent.parent / "fixtures"))
from command_fixtures import FIXTURES, EXPECTED_VIOLATIONS, EXPECTED_BUDGET

# These imports will FAIL in Red phase - this is expected and correct!
# The auditor module doesn't exist yet.
from devforgeai.auditors.pattern_compliance_auditor import (
    PatternComplianceAuditor,
    Violation,
    BudgetClassification,
    ViolationType,
    ViolationSeverity,
)


class TestViolationDetection:
    """Tests for violation detection (6 violation types)."""

    def test_detect_business_logic_violation_simple(self):
        """Test: Detect simple business logic violation."""
        # Arrange
        content = """
        FOR each file:
            Calculate coverage percentage
            IF > threshold:
                Mark as failing
        """
        auditor = PatternComplianceAuditor()

        # Act
        violations = auditor.detect_violations(content)

        # Assert
        assert len(violations) > 0
        assert any(v.type == ViolationType.BUSINESS_LOGIC for v in violations)
        business_logic_violations = [
            v for v in violations if v.type == ViolationType.BUSINESS_LOGIC
        ]
        assert business_logic_violations[0].severity == ViolationSeverity.HIGH
        assert business_logic_violations[0].line_number > 0

    def test_detect_business_logic_violation_complex(self):
        """Test: Detect complex business logic violation."""
        # Arrange
        content = """
        IF status not in ["Dev Complete", "QA Approved"]:
            IF status == "In Development":
                Warn: "Dev still in progress"
            ELIF status == "QA Failed":
                Create follow-up story
            ELSE:
                Mark as error
        """
        auditor = PatternComplianceAuditor()

        # Act
        violations = auditor.detect_violations(content)

        # Assert
        business_logic = [
            v for v in violations if v.type == ViolationType.BUSINESS_LOGIC
        ]
        assert len(business_logic) > 0
        assert all(v.severity in [ViolationSeverity.HIGH] for v in business_logic)

    def test_detect_templates_violation_single(self):
        """Test: Detect single display template violation."""
        # Arrange
        content = """
        IF mode == "deep" AND status == "PASS":
          Display: "✅ Deep QA PASSED"
          Display: "Coverage: ${coverage}%"
          Display: "Anti-patterns: ${count}"
        """
        auditor = PatternComplianceAuditor()

        # Act
        violations = auditor.detect_violations(content)

        # Assert
        templates = [v for v in violations if v.type == ViolationType.TEMPLATES]
        assert len(templates) > 0
        assert templates[0].severity == ViolationSeverity.HIGH
        assert templates[0].line_number > 0
        assert "Display:" in templates[0].code_snippet

    def test_detect_templates_violation_multiple(self):
        """Test: Detect multiple display template violations."""
        # Arrange
        content = """
        IF mode == "deep":
          Display template 1 (50 lines)
        IF mode == "light":
          Display template 2 (40 lines)
        IF failure == "coverage":
          Display template 3 (45 lines)
        IF failure == "patterns":
          Display template 4 (50 lines)
        """
        auditor = PatternComplianceAuditor()

        # Act
        violations = auditor.detect_violations(content)

        # Assert
        templates = [v for v in violations if v.type == ViolationType.TEMPLATES]
        assert len(templates) > 0

    def test_detect_parsing_violation_file_reading(self):
        """Test: Detect file reading/parsing violation."""
        # Arrange
        content = """
        Read QA report from: devforgeai/qa/reports/$1-qa-report.md
        Extract sections:
          - Coverage metrics
          - Failed tests
        Parse YAML frontmatter
        Extract violation details
        """
        auditor = PatternComplianceAuditor()

        # Act
        violations = auditor.detect_violations(content)

        # Assert
        parsing = [v for v in violations if v.type == ViolationType.PARSING]
        assert len(parsing) > 0
        assert parsing[0].severity in [ViolationSeverity.MEDIUM, ViolationSeverity.HIGH]

    def test_detect_parsing_violation_json(self):
        """Test: Detect JSON parsing violation."""
        # Arrange
        content = """
        Read: devforgeai/qa/coverage/coverage-report.json
        Parse JSON
        Extract: coverage_percentage, uncovered_files
        FOR each uncovered_file:
          IF in violations_report:
            Link them together
        """
        auditor = PatternComplianceAuditor()

        # Act
        violations = auditor.detect_violations(content)

        # Assert
        parsing = [v for v in violations if v.type == ViolationType.PARSING]
        assert len(parsing) > 0

    def test_detect_decision_making_violation_simple(self):
        """Test: Detect simple decision-making violation."""
        # Arrange
        content = """
        IF coverage < 80:
          severity = "CRITICAL"
          action = "Must improve coverage"
        ELIF coverage < 95:
          severity = "MEDIUM"
          action = "Target for next sprint"
        ELSE:
          severity = "LOW"
        """
        auditor = PatternComplianceAuditor()

        # Act
        violations = auditor.detect_violations(content)

        # Assert
        decisions = [v for v in violations if v.type == ViolationType.DECISION_MAKING]
        assert len(decisions) > 0
        assert decisions[0].severity == ViolationSeverity.HIGH

    def test_detect_decision_making_violation_complex(self):
        """Test: Detect complex decision-making violation."""
        # Arrange
        content = """
        ANALYZE QA result:
        IF coverage < 50:
          COMBINE results:
          IF any severity == "CRITICAL":
            overall_status = "BLOCKED"
          ELIF any severity == "HIGH":
            overall_status = "AT_RISK"
          DETERMINE next action:
          IF overall_status == "BLOCKED":
            IF deferral_count > 0:
              IF all deferrals have reasons:
                action = "Create follow-up story"
        """
        auditor = PatternComplianceAuditor()

        # Act
        violations = auditor.detect_violations(content)

        # Assert
        decisions = [v for v in violations if v.type == ViolationType.DECISION_MAKING]
        assert len(decisions) > 0

    def test_detect_error_recovery_violation_simple(self):
        """Test: Detect simple error recovery violation."""
        # Arrange
        content = """
        ERROR: Story not found
          → AskUserQuestion with 3 options
          → Handle response
          → Retry logic
        """
        auditor = PatternComplianceAuditor()

        # Act
        violations = auditor.detect_violations(content)

        # Assert
        error_recovery = [
            v for v in violations if v.type == ViolationType.ERROR_RECOVERY
        ]
        assert len(error_recovery) > 0
        assert error_recovery[0].severity == ViolationSeverity.MEDIUM

    def test_detect_error_recovery_violation_complex(self):
        """Test: Detect complex error recovery violation."""
        # Arrange
        content = """
        TRY:
          Read QA report
          Parse JSON
        CATCH FileNotFound:
          Regenerate report
          Retry: Read and parse
          IF still fails:
            AskUserQuestion: "Generate new report?"
        CATCH JSONDecodeError:
          Log error
          AskUserQuestion: "Report corrupted. Regenerate?"
          IF yes:
            Delete report
            Invoke skill
        CATCH SkillExecutionError:
          Log error details
          IF error type is "missing_context":
            Suggest: Run /create-context
        """
        auditor = PatternComplianceAuditor()

        # Act
        violations = auditor.detect_violations(content)

        # Assert
        error_recovery = [
            v for v in violations if v.type == ViolationType.ERROR_RECOVERY
        ]
        assert len(error_recovery) > 0

    def test_detect_direct_subagent_bypass(self):
        """Test: Detect direct subagent invocation (bypass skill layer)."""
        # Arrange
        content = """
        Task(
          subagent_type="test-auditor",
          description="Audit command",
          prompt="Audit this..."
        )
        """
        auditor = PatternComplianceAuditor()

        # Act
        violations = auditor.detect_violations(content)

        # Assert
        bypass = [
            v
            for v in violations
            if v.type == ViolationType.DIRECT_SUBAGENT_BYPASS
        ]
        assert len(bypass) > 0
        assert bypass[0].severity == ViolationSeverity.CRITICAL

    def test_detect_direct_subagent_bypass_multiple(self):
        """Test: Detect multiple direct subagent invocations."""
        # Arrange
        content = """
        Task(subagent_type="test-1", description="Test 1", prompt="...")
        Task(subagent_type="test-2", description="Test 2", prompt="...")
        Task(subagent_type="test-3", description="Test 3", prompt="...")
        """
        auditor = PatternComplianceAuditor()

        # Act
        violations = auditor.detect_violations(content)

        # Assert
        bypass = [
            v
            for v in violations
            if v.type == ViolationType.DIRECT_SUBAGENT_BYPASS
        ]
        assert len(bypass) >= 3
        assert all(v.severity == ViolationSeverity.CRITICAL for v in bypass)


class TestViolationAccuracy:
    """Tests for violation detection accuracy (line numbers, severity)."""

    def test_violation_line_number_accuracy(self):
        """Test: Line numbers are accurate (±0 lines)."""
        # Arrange
        content = """Line 1: Header
Line 2: Description
Line 3: (empty)
Line 4: FOR each file:  <-- VIOLATION HERE
Line 5:   Calculate
Line 6:   Mark
"""
        auditor = PatternComplianceAuditor()

        # Act
        violations = auditor.detect_violations(content)

        # Assert
        assert len(violations) > 0
        # Line number should be exactly 4 (or contain "4" in line_number)
        assert any(v.line_number == 4 for v in violations)

    def test_violation_code_snippet_included(self):
        """Test: Code snippets included in violations."""
        # Arrange
        content = """
        IF condition:
            Do something
            Calculate value
            IF nested:
                Complex logic
        """
        auditor = PatternComplianceAuditor()

        # Act
        violations = auditor.detect_violations(content)

        # Assert
        assert len(violations) > 0
        assert all(v.code_snippet is not None for v in violations)
        assert all(len(v.code_snippet) > 0 for v in violations)

    def test_violation_has_recommendation(self):
        """Test: All violations have recommendations."""
        # Arrange
        content = """
        FOR each file:
            Calculate
            IF > threshold:
                Mark as failing
        """
        auditor = PatternComplianceAuditor()

        # Act
        violations = auditor.detect_violations(content)

        # Assert
        assert len(violations) > 0
        assert all(v.recommendation is not None for v in violations)
        assert all(len(v.recommendation) > 0 for v in violations)


class TestBudgetClassification:
    """Tests for character budget classification."""

    def test_classify_compliant_budget(self):
        """Test: Classify command as COMPLIANT (<12K chars)."""
        # Arrange
        auditor = PatternComplianceAuditor()
        content = FIXTURES['compliant']

        # Act
        classification = auditor.classify_budget(content)

        # Assert
        assert classification == BudgetClassification.COMPLIANT
        assert len(content) < 12000

    def test_classify_warning_budget(self):
        """Test: Classify command as WARNING (12-15K chars)."""
        # Arrange
        auditor = PatternComplianceAuditor()
        content = FIXTURES['moderate']

        # Act
        classification = auditor.classify_budget(content)

        # Assert
        assert classification == BudgetClassification.WARNING
        assert 12000 <= len(content) <= 15000

    def test_classify_over_budget(self):
        """Test: Classify command as OVER (>15K chars)."""
        # Arrange
        auditor = PatternComplianceAuditor()
        content = FIXTURES['severe']

        # Act
        classification = auditor.classify_budget(content)

        # Assert
        assert classification == BudgetClassification.OVER
        assert len(content) > 15000

    def test_budget_percentage_calculation(self):
        """Test: Budget percentage calculated correctly."""
        # Arrange
        auditor = PatternComplianceAuditor()
        content = FIXTURES['moderate']
        chars = len(content)
        expected_percentage = (chars / 15000) * 100

        # Act
        percentage = auditor.calculate_budget_percentage(chars)

        # Assert
        assert percentage == expected_percentage
        assert percentage == pytest.approx(expected_percentage, rel=0.01)

    def test_budget_classification_boundaries(self):
        """Test: Budget classification at boundaries."""
        # Arrange
        auditor = PatternComplianceAuditor()

        # Test at 12K boundary
        # Act & Assert
        assert auditor.classify_budget("x" * 11999) == BudgetClassification.COMPLIANT
        assert auditor.classify_budget("x" * 12000) == BudgetClassification.WARNING
        assert auditor.classify_budget("x" * 12001) == BudgetClassification.WARNING

        # Test at 15K boundary
        assert auditor.classify_budget("x" * 14999) == BudgetClassification.WARNING
        assert auditor.classify_budget("x" * 15000) == BudgetClassification.OVER
        assert auditor.classify_budget("x" * 15001) == BudgetClassification.OVER


class TestViolationCategorization:
    """Tests for violation categorization and grouping."""

    def test_group_violations_by_type(self):
        """Test: Group violations by type."""
        # Arrange
        auditor = PatternComplianceAuditor()
        content = FIXTURES['moderate']

        # Act
        violations = auditor.detect_violations(content)
        grouped = auditor.group_by_type(violations)

        # Assert
        assert isinstance(grouped, dict)
        assert all(isinstance(v_list, list) for v_list in grouped.values())

    def test_count_violations_by_type(self):
        """Test: Count violations by type."""
        # Arrange
        auditor = PatternComplianceAuditor()
        content = FIXTURES['moderate']

        # Act
        violations = auditor.detect_violations(content)
        counts = auditor.count_by_type(violations)

        # Assert
        assert isinstance(counts, dict)
        assert all(isinstance(count, int) for count in counts.values())
        assert sum(counts.values()) == len(violations)

    def test_count_violations_by_severity(self):
        """Test: Count violations by severity."""
        # Arrange
        auditor = PatternComplianceAuditor()
        content = FIXTURES['severe']

        # Act
        violations = auditor.detect_violations(content)
        severity_counts = auditor.count_by_severity(violations)

        # Assert
        assert isinstance(severity_counts, dict)
        assert all(
            sev in [
                ViolationSeverity.CRITICAL,
                ViolationSeverity.HIGH,
                ViolationSeverity.MEDIUM,
                ViolationSeverity.LOW,
            ]
            for sev in severity_counts.keys()
        )

    def test_frequency_analysis(self):
        """Test: Frequency analysis of violation types."""
        # Arrange
        auditor = PatternComplianceAuditor()
        content = FIXTURES['severe']

        # Act
        violations = auditor.detect_violations(content)
        frequency = auditor.frequency_analysis(violations)

        # Assert
        assert isinstance(frequency, dict)
        assert all(0 <= count for count in frequency.values())


class TestEffortEstimation:
    """Tests for refactoring effort estimation."""

    def test_estimate_effort_compliant(self):
        """Test: Estimate effort for compliant command (0 hours)."""
        # Arrange
        auditor = PatternComplianceAuditor()
        content = FIXTURES['compliant']

        # Act
        effort_hours = auditor.estimate_effort(content)

        # Assert
        assert effort_hours == 0

    def test_estimate_effort_moderate_violations(self):
        """Test: Estimate effort for moderate violations (2-3 hours)."""
        # Arrange
        auditor = PatternComplianceAuditor()
        content = FIXTURES['moderate']

        # Act
        effort_hours = auditor.estimate_effort(content)

        # Assert
        assert 2 <= effort_hours <= 3

    def test_estimate_effort_severe_violations(self):
        """Test: Estimate effort for severe violations (3-5 hours)."""
        # Arrange
        auditor = PatternComplianceAuditor()
        content = FIXTURES['severe']

        # Act
        effort_hours = auditor.estimate_effort(content)

        # Assert
        assert 3 <= effort_hours <= 5

    def test_estimate_effort_formula_consistent(self):
        """Test: Effort estimation formula is consistent."""
        # Arrange
        auditor = PatternComplianceAuditor()

        # Act & Assert
        # Same content should produce same estimate
        content = "Test content"
        effort1 = auditor.estimate_effort(content)
        effort2 = auditor.estimate_effort(content)

        assert effort1 == effort2

    def test_effort_increases_with_violations(self):
        """Test: Effort increases as violations increase."""
        # Arrange
        auditor = PatternComplianceAuditor()
        content_few = FIXTURES['compliant']
        content_some = FIXTURES['moderate']
        content_many = FIXTURES['severe']

        # Act
        effort_few = auditor.estimate_effort(content_few)
        effort_some = auditor.estimate_effort(content_some)
        effort_many = auditor.estimate_effort(content_many)

        # Assert
        assert effort_few <= effort_some <= effort_many


class TestPriorityQueue:
    """Tests for refactoring priority queue generation."""

    def test_generate_priority_queue_ordering(self):
        """Test: Priority queue orders commands correctly."""
        # Arrange
        auditor = PatternComplianceAuditor()
        commands = {
            'compliant': FIXTURES['compliant'],
            'moderate': FIXTURES['moderate'],
            'severe': FIXTURES['severe'],
        }

        # Act
        queue = auditor.generate_priority_queue(commands)

        # Assert
        assert len(queue) == 3
        # Severe should be first (highest priority)
        assert queue[0]['name'] == 'severe'
        # Moderate second
        assert queue[1]['name'] == 'moderate'
        # Compliant last (or not in queue)

    def test_priority_queue_has_effort_estimates(self):
        """Test: Priority queue includes effort estimates."""
        # Arrange
        auditor = PatternComplianceAuditor()
        commands = {
            'moderate': FIXTURES['moderate'],
            'severe': FIXTURES['severe'],
        }

        # Act
        queue = auditor.generate_priority_queue(commands)

        # Assert
        for item in queue:
            assert 'effort_hours' in item
            assert item['effort_hours'] > 0

    def test_priority_categories(self):
        """Test: Commands grouped into priority categories (P1/P2/P3)."""
        # Arrange
        auditor = PatternComplianceAuditor()
        commands = {
            'severe': FIXTURES['severe'],
            'moderate': FIXTURES['moderate'],
            'minimal': FIXTURES['minimal'],
        }

        # Act
        priorities = auditor.group_by_priority(commands)

        # Assert
        assert 'P1' in priorities or len(priorities) > 0
        # P1 should contain severe (over budget)
        if 'P1' in priorities:
            assert any('severe' in item['name'] for item in priorities['P1'])


class TestEdgeCases:
    """Tests for edge cases and special scenarios."""

    def test_empty_command_no_violations(self):
        """Test: Empty command has no violations."""
        # Arrange
        auditor = PatternComplianceAuditor()
        content = ""

        # Act
        violations = auditor.detect_violations(content)

        # Assert
        assert len(violations) == 0

    def test_minimal_command_no_violations(self):
        """Test: Minimal valid command has no violations."""
        # Arrange
        auditor = PatternComplianceAuditor()
        content = FIXTURES['minimal']

        # Act
        violations = auditor.detect_violations(content)

        # Assert
        assert len(violations) == 0

    def test_malformed_yaml_detected(self):
        """Test: Malformed YAML is detected as violation."""
        # Arrange
        auditor = PatternComplianceAuditor()
        content = FIXTURES['malformed']

        # Act
        violations = auditor.detect_violations(content)

        # Assert
        assert len(violations) > 0
        # Should have at least one YAML parsing violation

    def test_multiple_violation_types_same_command(self):
        """Test: Detect multiple violation types in single command."""
        # Arrange
        auditor = PatternComplianceAuditor()
        content = FIXTURES['severe']

        # Act
        violations = auditor.detect_violations(content)

        # Assert
        violation_types = set(v.type for v in violations)
        assert len(violation_types) > 1  # Multiple types detected

    def test_no_false_positives_on_compliant(self):
        """Test: Compliant command produces no violations."""
        # Arrange
        auditor = PatternComplianceAuditor()
        content = FIXTURES['compliant']

        # Act
        violations = auditor.detect_violations(content)

        # Assert
        assert len(violations) == 0

    def test_violation_objects_immutable(self):
        """Test: Violation objects are immutable (dataclass frozen)."""
        # Arrange
        auditor = PatternComplianceAuditor()
        content = FIXTURES['moderate']
        violations = auditor.detect_violations(content)

        # Act & Assert
        if len(violations) > 0:
            with pytest.raises(AttributeError):
                violations[0].severity = ViolationSeverity.LOW

    def test_handle_very_large_command(self):
        """Test: Handle very large command file gracefully."""
        # Arrange
        auditor = PatternComplianceAuditor()
        large_content = "Line of code\n" * 10000

        # Act
        violations = auditor.detect_violations(large_content)

        # Assert
        assert isinstance(violations, list)
        # Should complete without timeout

    def test_unicode_content_handling(self):
        """Test: Handle unicode characters in content."""
        # Arrange
        auditor = PatternComplianceAuditor()
        content = """
        Display: "✅ Validation PASSED"
        Display: "❌ Validation FAILED"
        """

        # Act
        violations = auditor.detect_violations(content)

        # Assert
        assert isinstance(violations, list)
        # Should handle unicode without errors


class TestFixtureValidation:
    """Tests that validate fixture content."""

    def test_fixture_compliant_is_compliant(self):
        """Test: Compliant fixture actually is compliant."""
        # Arrange
        auditor = PatternComplianceAuditor()
        content = FIXTURES['compliant']

        # Act
        violations = auditor.detect_violations(content)
        classification = auditor.classify_budget(content)

        # Assert
        assert len(violations) == EXPECTED_VIOLATIONS['compliant']
        assert classification == BudgetClassification.COMPLIANT

    def test_fixture_moderate_has_violations(self):
        """Test: Moderate fixture has expected violations."""
        # Arrange
        auditor = PatternComplianceAuditor()
        content = FIXTURES['moderate']

        # Act
        violations = auditor.detect_violations(content)

        # Assert
        assert len(violations) >= EXPECTED_VIOLATIONS['moderate']
        assert BudgetClassification.WARNING == auditor.classify_budget(content)

    def test_fixture_severe_over_budget(self):
        """Test: Severe fixture is over budget."""
        # Arrange
        auditor = PatternComplianceAuditor()
        content = FIXTURES['severe']

        # Act
        violations = auditor.detect_violations(content)
        classification = auditor.classify_budget(content)

        # Assert
        assert len(violations) >= EXPECTED_VIOLATIONS['severe']
        assert classification == BudgetClassification.OVER

    def test_fixture_bypass_detected(self):
        """Test: Bypass fixture has bypass violations."""
        # Arrange
        auditor = PatternComplianceAuditor()
        content = FIXTURES['bypass']

        # Act
        violations = auditor.detect_violations(content)

        # Assert
        assert any(
            v.type == ViolationType.DIRECT_SUBAGENT_BYPASS for v in violations
        )
        assert len(
            [
                v
                for v in violations
                if v.type == ViolationType.DIRECT_SUBAGENT_BYPASS
            ]
        ) >= EXPECTED_VIOLATIONS['bypass']


class TestReportGeneration:
    """Tests for report generation (structure, format)."""

    def test_report_has_summary_section(self):
        """Test: Report includes summary section."""
        # Arrange
        auditor = PatternComplianceAuditor()
        content = FIXTURES['moderate']
        violations = auditor.detect_violations(content)

        # Act
        report = auditor.generate_report(violations, 'test-command')

        # Assert
        assert 'summary' in report
        assert report['summary']['total_violations'] == len(violations)

    def test_report_json_serializable(self):
        """Test: Report is JSON serializable."""
        # Arrange
        auditor = PatternComplianceAuditor()
        content = FIXTURES['moderate']
        violations = auditor.detect_violations(content)

        # Act
        report = auditor.generate_report(violations, 'test-command')

        # Assert
        import json
        json_str = json.dumps(report)
        assert len(json_str) > 0

    def test_report_includes_violations(self):
        """Test: Report includes all violations."""
        # Arrange
        auditor = PatternComplianceAuditor()
        content = FIXTURES['moderate']
        violations = auditor.detect_violations(content)

        # Act
        report = auditor.generate_report(violations, 'test-command')

        # Assert
        assert 'violations' in report
        assert len(report['violations']) == len(violations)

    def test_report_includes_roadmap(self):
        """Test: Report includes refactoring roadmap."""
        # Arrange
        auditor = PatternComplianceAuditor()
        content = FIXTURES['severe']
        violations = auditor.detect_violations(content)

        # Act
        report = auditor.generate_report(violations, 'test-command')

        # Assert
        assert 'roadmap' in report
        if len(violations) > 0:
            assert len(report['roadmap']) > 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
