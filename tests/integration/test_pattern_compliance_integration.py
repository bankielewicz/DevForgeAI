"""
Integration tests for pattern-compliance-auditor end-to-end workflows.

Tests complete audit cycle: command analysis → violation detection → report generation → roadmap.
"""

import pytest
import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent / "fixtures"))
from command_fixtures import FIXTURES

# These imports will FAIL in Red phase - this is expected!
from devforgeai.auditors.pattern_compliance_auditor import (
    PatternComplianceAuditor,
    ViolationType,
    ViolationSeverity,
    BudgetClassification,
    AuditReport,
)


class TestEndToEndAuditWorkflow:
    """Tests for complete audit workflow."""

    def test_audit_single_command_complete_workflow(self):
        """Test: Complete audit workflow for single command."""
        # Arrange
        auditor = PatternComplianceAuditor()
        content = FIXTURES['moderate']
        command_name = 'test-moderate'

        # Act
        violations = auditor.detect_violations(content)
        budget = auditor.classify_budget(content)
        effort = auditor.estimate_effort(content)
        report = auditor.generate_report(violations, command_name)

        # Assert
        assert len(violations) > 0
        assert budget in [
            BudgetClassification.COMPLIANT,
            BudgetClassification.WARNING,
            BudgetClassification.OVER,
        ]
        assert effort >= 0
        assert isinstance(report, dict)
        assert 'command' in report
        assert report['command'] == command_name
        assert 'violations' in report
        assert 'roadmap' in report

    def test_audit_multiple_commands_parallel(self):
        """Test: Audit multiple commands in parallel."""
        # Arrange
        auditor = PatternComplianceAuditor()
        commands = {
            'compliant': FIXTURES['compliant'],
            'moderate': FIXTURES['moderate'],
            'severe': FIXTURES['severe'],
        }

        # Act
        results = {}
        for name, content in commands.items():
            violations = auditor.detect_violations(content)
            budget = auditor.classify_budget(content)
            results[name] = {
                'violations': violations,
                'budget': budget,
            }

        # Assert
        assert len(results) == 3
        assert results['compliant']['budget'] == BudgetClassification.COMPLIANT
        assert results['moderate']['budget'] == BudgetClassification.WARNING
        assert results['severe']['budget'] == BudgetClassification.OVER

    def test_audit_generates_markdown_summary(self):
        """Test: Audit generates markdown summary."""
        # Arrange
        auditor = PatternComplianceAuditor()
        content = FIXTURES['moderate']

        # Act
        violations = auditor.detect_violations(content)
        markdown = auditor.generate_markdown_summary(violations, 'test-command')

        # Assert
        assert isinstance(markdown, str)
        assert len(markdown) > 0
        assert '#' in markdown  # Contains markdown headers
        assert 'Violation' in markdown or 'violation' in markdown

    def test_audit_generates_json_report(self):
        """Test: Audit generates valid JSON report."""
        # Arrange
        auditor = PatternComplianceAuditor()
        content = FIXTURES['moderate']

        # Act
        violations = auditor.detect_violations(content)
        report = auditor.generate_report(violations, 'test-command')
        json_str = json.dumps(report)
        parsed = json.loads(json_str)

        # Assert
        assert isinstance(parsed, dict)
        assert 'command' in parsed
        assert 'violations' in parsed
        assert 'summary' in parsed

    def test_audit_creates_actionable_roadmap(self):
        """Test: Audit creates actionable refactoring roadmap."""
        # Arrange
        auditor = PatternComplianceAuditor()
        commands = {
            'severe': FIXTURES['severe'],
            'moderate': FIXTURES['moderate'],
        }

        # Act
        violations_map = {}
        for name, content in commands.items():
            violations_map[name] = auditor.detect_violations(content)

        roadmap = auditor.generate_roadmap(violations_map, commands)

        # Assert
        assert isinstance(roadmap, list)
        assert len(roadmap) > 0
        # Each item should have actionable information
        for item in roadmap:
            assert 'command' in item
            assert 'priority' in item
            assert 'effort_hours' in item
            assert 'recommendations' in item

    def test_roadmap_ordered_by_priority(self):
        """Test: Roadmap orders commands by priority."""
        # Arrange
        auditor = PatternComplianceAuditor()
        commands = {
            'compliant': FIXTURES['compliant'],
            'moderate': FIXTURES['moderate'],
            'severe': FIXTURES['severe'],
        }

        # Act
        violations_map = {}
        for name, content in commands.items():
            violations_map[name] = auditor.detect_violations(content)

        roadmap = auditor.generate_roadmap(violations_map, commands)

        # Assert
        if len(roadmap) > 1:
            # Severe should come before moderate
            severe_idx = next(
                (i for i, r in enumerate(roadmap) if 'severe' in r['command']),
                float('inf'),
            )
            moderate_idx = next(
                (i for i, r in enumerate(roadmap) if 'moderate' in r['command']),
                float('inf'),
            )
            assert severe_idx < moderate_idx


class TestViolationCategorization:
    """Tests for violation categorization in reports."""

    def test_violations_grouped_by_type_in_report(self):
        """Test: Report groups violations by type."""
        # Arrange
        auditor = PatternComplianceAuditor()
        content = FIXTURES['severe']

        # Act
        violations = auditor.detect_violations(content)
        report = auditor.generate_report(violations, 'test-severe')

        # Assert
        assert 'categorization' in report or 'by_type' in report
        # Check that violations are organized

    def test_violations_grouped_by_severity_in_report(self):
        """Test: Report groups violations by severity."""
        # Arrange
        auditor = PatternComplianceAuditor()
        content = FIXTURES['severe']

        # Act
        violations = auditor.detect_violations(content)
        report = auditor.generate_report(violations, 'test-severe')

        # Assert
        # Report should indicate severity distribution
        assert any(
            k in report
            for k in ['severity_distribution', 'by_severity', 'severities']
        )

    def test_violation_frequency_analysis(self):
        """Test: Report includes frequency analysis."""
        # Arrange
        auditor = PatternComplianceAuditor()
        content = FIXTURES['severe']

        # Act
        violations = auditor.detect_violations(content)
        frequency = auditor.frequency_analysis(violations)

        # Assert
        assert isinstance(frequency, dict)
        assert len(frequency) > 0
        assert all(isinstance(count, int) for count in frequency.values())


class TestRoadmapGeneration:
    """Tests for refactoring roadmap generation."""

    def test_roadmap_identifies_critical_items(self):
        """Test: Roadmap identifies CRITICAL priority items."""
        # Arrange
        auditor = PatternComplianceAuditor()
        commands = {
            'severe': FIXTURES['severe'],
        }

        # Act
        violations_map = {}
        for name, content in commands.items():
            violations_map[name] = auditor.detect_violations(content)

        roadmap = auditor.generate_roadmap(violations_map, commands)

        # Assert
        critical_items = [r for r in roadmap if r['priority'] == 'CRITICAL']
        assert len(critical_items) > 0

    def test_roadmap_estimates_total_effort(self):
        """Test: Roadmap estimates total effort hours."""
        # Arrange
        auditor = PatternComplianceAuditor()
        commands = {
            'moderate': FIXTURES['moderate'],
            'severe': FIXTURES['severe'],
        }

        # Act
        violations_map = {}
        for name, content in commands.items():
            violations_map[name] = auditor.detect_violations(content)

        roadmap = auditor.generate_roadmap(violations_map, commands)
        total_effort = auditor.calculate_total_effort(roadmap)

        # Assert
        assert total_effort > 0
        assert all(r['effort_hours'] > 0 for r in roadmap)
        sum_effort = sum(r['effort_hours'] for r in roadmap)
        assert total_effort == sum_effort

    def test_roadmap_identifies_dependencies(self):
        """Test: Roadmap identifies refactoring dependencies."""
        # Arrange
        auditor = PatternComplianceAuditor()
        commands = {
            'moderate': FIXTURES['moderate'],
            'severe': FIXTURES['severe'],
        }

        # Act
        violations_map = {}
        for name, content in commands.items():
            violations_map[name] = auditor.detect_violations(content)

        roadmap = auditor.generate_roadmap(violations_map, commands)

        # Assert
        for item in roadmap:
            if 'dependencies' in item:
                assert isinstance(item['dependencies'], list)

    def test_roadmap_provides_recommendations(self):
        """Test: Roadmap provides actionable recommendations."""
        # Arrange
        auditor = PatternComplianceAuditor()
        content = FIXTURES['severe']

        # Act
        violations = auditor.detect_violations(content)
        roadmap_item = auditor.generate_roadmap(
            {'test': violations}, {'test': content}
        )[0]

        # Assert
        assert 'recommendations' in roadmap_item
        assert len(roadmap_item['recommendations']) > 0
        for rec in roadmap_item['recommendations']:
            assert 'action' in rec
            assert 'rationale' in rec


class TestBudgetAnalysis:
    """Tests for budget analysis in reports."""

    def test_report_includes_budget_status(self):
        """Test: Report includes budget classification."""
        # Arrange
        auditor = PatternComplianceAuditor()
        content = FIXTURES['moderate']

        # Act
        violations = auditor.detect_violations(content)
        budget = auditor.classify_budget(content)
        report = auditor.generate_report(violations, 'test-command')

        # Assert
        assert 'budget' in report
        assert report['budget']['classification'] == budget.name

    def test_report_includes_budget_percentage(self):
        """Test: Report includes budget percentage."""
        # Arrange
        auditor = PatternComplianceAuditor()
        content = FIXTURES['moderate']

        # Act
        violations = auditor.detect_violations(content)
        report = auditor.generate_report(violations, 'test-command')

        # Assert
        assert 'budget' in report
        assert 'percentage' in report['budget']
        assert 0 <= report['budget']['percentage'] <= 200

    def test_report_character_count(self):
        """Test: Report includes character count."""
        # Arrange
        auditor = PatternComplianceAuditor()
        content = FIXTURES['moderate']

        # Act
        violations = auditor.detect_violations(content)
        report = auditor.generate_report(violations, 'test-command')

        # Assert
        assert 'budget' in report
        assert 'character_count' in report['budget']
        assert report['budget']['character_count'] == len(content)

    def test_over_budget_commands_flagged(self):
        """Test: Over-budget commands are flagged in report."""
        # Arrange
        auditor = PatternComplianceAuditor()
        content = FIXTURES['severe']

        # Act
        violations = auditor.detect_violations(content)
        report = auditor.generate_report(violations, 'test-severe')

        # Assert
        assert report['budget']['classification'] == BudgetClassification.OVER.name
        # Should be marked as requiring refactoring
        assert any(
            'refactor' in rec.lower()
            for rec in report.get('recommendations', [])
        )


class TestComplexScenarios:
    """Tests for complex, realistic scenarios."""

    def test_audit_all_fixtures(self):
        """Test: Audit all fixtures successfully."""
        # Arrange
        auditor = PatternComplianceAuditor()

        # Act & Assert
        for name, content in FIXTURES.items():
            violations = auditor.detect_violations(content)
            budget = auditor.classify_budget(content)
            report = auditor.generate_report(violations, f'test-{name}')

            assert isinstance(violations, list)
            assert budget in [
                BudgetClassification.COMPLIANT,
                BudgetClassification.WARNING,
                BudgetClassification.OVER,
            ]
            assert isinstance(report, dict)

    def test_mixed_command_audit(self):
        """Test: Audit mix of compliant and non-compliant commands."""
        # Arrange
        auditor = PatternComplianceAuditor()
        commands = {
            'compliant': FIXTURES['compliant'],
            'bypass': FIXTURES['bypass'],
            'severe': FIXTURES['severe'],
        }

        # Act
        all_violations = {}
        for name, content in commands.items():
            all_violations[name] = auditor.detect_violations(content)

        # Assert
        assert len(all_violations['compliant']) == 0
        assert len(all_violations['bypass']) > 0
        assert len(all_violations['severe']) > 0

    def test_audit_preserves_order_in_roadmap(self):
        """Test: Roadmap maintains consistent ordering."""
        # Arrange
        auditor = PatternComplianceAuditor()
        commands = {
            'severe': FIXTURES['severe'],
            'moderate': FIXTURES['moderate'],
            'compliant': FIXTURES['compliant'],
        }

        # Act
        violations_map = {}
        for name, content in commands.items():
            violations_map[name] = auditor.detect_violations(content)

        roadmap1 = auditor.generate_roadmap(violations_map, commands)
        roadmap2 = auditor.generate_roadmap(violations_map, commands)

        # Assert
        assert [r['command'] for r in roadmap1] == [
            r['command'] for r in roadmap2
        ]

    def test_audit_handles_incremental_improvement(self):
        """Test: Track improvements across audit cycles."""
        # Arrange
        auditor = PatternComplianceAuditor()
        content_before = FIXTURES['severe']

        # Simulate improvement (fewer violations in "after" version)
        content_after = FIXTURES['moderate']

        # Act
        violations_before = auditor.detect_violations(content_before)
        violations_after = auditor.detect_violations(content_after)

        # Assert
        assert len(violations_after) < len(violations_before)


class TestReportFormatting:
    """Tests for report formatting and display."""

    def test_markdown_report_is_readable(self):
        """Test: Markdown report is human-readable."""
        # Arrange
        auditor = PatternComplianceAuditor()
        content = FIXTURES['moderate']

        # Act
        violations = auditor.detect_violations(content)
        markdown = auditor.generate_markdown_summary(violations, 'test-command')

        # Assert
        assert '\n' in markdown  # Has line breaks
        assert '#' in markdown or '##' in markdown  # Has headers
        assert '-' in markdown or '*' in markdown  # Has list formatting

    def test_json_report_contains_all_fields(self):
        """Test: JSON report contains all required fields."""
        # Arrange
        auditor = PatternComplianceAuditor()
        content = FIXTURES['moderate']

        # Act
        violations = auditor.detect_violations(content)
        report = auditor.generate_report(violations, 'test-command')

        # Assert - Required fields
        required_fields = [
            'command',
            'summary',
            'violations',
            'budget',
            'roadmap',
        ]
        for field in required_fields:
            assert field in report, f"Missing required field: {field}"

    def test_violation_details_in_report(self):
        """Test: Report includes detailed violation information."""
        # Arrange
        auditor = PatternComplianceAuditor()
        content = FIXTURES['moderate']

        # Act
        violations = auditor.detect_violations(content)
        report = auditor.generate_report(violations, 'test-command')

        # Assert
        if len(violations) > 0:
            assert len(report['violations']) > 0
            for violation in report['violations']:
                assert 'type' in violation
                assert 'severity' in violation
                assert 'line_number' in violation
                assert 'recommendation' in violation


class TestErrorHandling:
    """Tests for error handling in audit workflow."""

    def test_handle_invalid_yaml_gracefully(self):
        """Test: Handle invalid YAML frontmatter gracefully."""
        # Arrange
        auditor = PatternComplianceAuditor()
        content = FIXTURES['malformed']

        # Act & Assert
        # Should not raise exception
        violations = auditor.detect_violations(content)
        assert isinstance(violations, list)
        # Should detect YAML error
        assert any('yaml' in str(v).lower() or 'malformed' in str(v).lower()
                   for v in violations)

    def test_handle_empty_content(self):
        """Test: Handle empty command content."""
        # Arrange
        auditor = PatternComplianceAuditor()
        content = ""

        # Act
        violations = auditor.detect_violations(content)
        budget = auditor.classify_budget(content)

        # Assert
        assert violations == []
        assert budget == BudgetClassification.COMPLIANT

    def test_handle_very_large_content(self):
        """Test: Handle very large command files."""
        # Arrange
        auditor = PatternComplianceAuditor()
        large_content = "x" * 100000  # 100K chars

        # Act & Assert
        violations = auditor.detect_violations(large_content)
        budget = auditor.classify_budget(large_content)

        assert isinstance(violations, list)
        assert budget == BudgetClassification.OVER


class TestConsistency:
    """Tests for consistency across audit cycles."""

    def test_audit_results_deterministic(self):
        """Test: Audit results are deterministic."""
        # Arrange
        auditor = PatternComplianceAuditor()
        content = FIXTURES['moderate']

        # Act
        violations1 = auditor.detect_violations(content)
        violations2 = auditor.detect_violations(content)

        # Assert
        assert len(violations1) == len(violations2)
        for v1, v2 in zip(violations1, violations2):
            assert v1.type == v2.type
            assert v1.severity == v2.severity
            assert v1.line_number == v2.line_number

    def test_budget_classification_deterministic(self):
        """Test: Budget classification is deterministic."""
        # Arrange
        auditor = PatternComplianceAuditor()
        content = FIXTURES['moderate']

        # Act
        budget1 = auditor.classify_budget(content)
        budget2 = auditor.classify_budget(content)

        # Assert
        assert budget1 == budget2

    def test_effort_estimation_deterministic(self):
        """Test: Effort estimation is deterministic."""
        # Arrange
        auditor = PatternComplianceAuditor()
        content = FIXTURES['moderate']

        # Act
        effort1 = auditor.estimate_effort(content)
        effort2 = auditor.estimate_effort(content)

        # Assert
        assert effort1 == effort2


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
