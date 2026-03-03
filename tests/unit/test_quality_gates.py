"""
Test suite for AC5: Documentation Quality Gate

Tests coverage verification, API documentation checks,
README existence verification, diagram validation, and release blocking.
"""

import pytest
from pathlib import Path
from unittest.mock import Mock, MagicMock, patch
from typing import Dict, List


class TestDocumentationCoverageVerification:
    """Test documentation coverage verification."""

    def test_should_calculate_coverage_percentage(self):
        """Test that coverage percentage is calculated correctly."""
        # Arrange
        documented_items = 80
        total_items = 100

        # Act
        from devforgeai_documentation import CoverageCalculator
        calc = CoverageCalculator()
        coverage = calc.calculate_coverage(documented_items, total_items)

        # Assert
        assert coverage == 80 or coverage == 80.0

    def test_should_verify_minimum_80_percent_coverage(self):
        """Test that coverage must be ≥80% to pass gate."""
        # Arrange
        test_cases = [
            (80, 100, True),   # 80% - passes
            (79, 100, False),  # 79% - fails
            (95, 100, True),   # 95% - passes
            (100, 100, True),  # 100% - passes
        ]

        # Act
        from devforgeai_documentation import QualityGate
        gate = QualityGate()

        # Assert
        for documented, total, expected in test_cases:
            result = gate.verify_coverage(documented, total)
            assert result == expected

    def test_should_report_coverage_percentage(self):
        """Test that coverage percentage is reported to user."""
        # Arrange
        documented = 85
        total = 100

        # Act
        from devforgeai_documentation import CoverageReporter
        reporter = CoverageReporter()
        report = reporter.create_report(documented, total)

        # Assert
        assert report is not None
        assert "85" in str(report) or "coverage" in str(report).lower()

    def test_should_identify_undocumented_items(self):
        """Test that system identifies which items are undocumented."""
        # Arrange
        items = [
            {"name": "API endpoint 1", "documented": True},
            {"name": "API endpoint 2", "documented": False},
            {"name": "API endpoint 3", "documented": True},
            {"name": "API endpoint 4", "documented": False}
        ]

        # Act
        from devforgeai_documentation import CoverageAnalyzer
        analyzer = CoverageAnalyzer()
        undocumented = analyzer.find_undocumented(items)

        # Assert
        assert undocumented is not None
        assert len(undocumented) == 2
        assert any("endpoint 2" in str(item) for item in undocumented)


class TestPublicAPIDocumentation:
    """Test verification that public APIs are documented."""

    def test_should_verify_all_public_apis_documented(self):
        """Test that all public API endpoints have documentation."""
        # Arrange
        public_apis = [
            {"endpoint": "GET /api/users", "documented": True},
            {"endpoint": "POST /api/users", "documented": True},
            {"endpoint": "GET /api/users/:id", "documented": True}
        ]

        # Act
        from devforgeai_documentation import APIDocumentationVerifier
        verifier = APIDocumentationVerifier()
        all_documented = verifier.verify_all_documented(public_apis)

        # Assert
        assert all_documented is True

    def test_should_fail_if_any_api_undocumented(self):
        """Test that gate fails if any API endpoint is undocumented."""
        # Arrange
        public_apis = [
            {"endpoint": "GET /api/users", "documented": True},
            {"endpoint": "POST /api/users", "documented": False},  # Missing!
            {"endpoint": "GET /api/users/:id", "documented": True}
        ]

        # Act
        from devforgeai_documentation import APIDocumentationVerifier
        verifier = APIDocumentationVerifier()
        result = verifier.verify_all_documented(public_apis)

        # Assert
        assert result is False

    def test_should_list_undocumented_apis(self):
        """Test that system lists undocumented API endpoints."""
        # Arrange
        public_apis = [
            {"endpoint": "GET /api/users", "documented": True},
            {"endpoint": "DELETE /api/users/:id", "documented": False}
        ]

        # Act
        from devforgeai_documentation import APIDocumentationVerifier
        verifier = APIDocumentationVerifier()
        undocumented = verifier.find_undocumented_apis(public_apis)

        # Assert
        assert undocumented is not None
        assert len(undocumented) == 1
        assert "DELETE" in str(undocumented)

    def test_should_check_api_documentation_completeness(self):
        """Test that API docs include all required sections (request, response, errors)."""
        # Arrange
        api_doc = {
            "endpoint": "POST /api/users",
            "has_request_schema": True,
            "has_response_example": True,
            "has_error_codes": True,
            "has_description": True
        }

        # Act
        from devforgeai_documentation import APIDocCompletenessChecker
        checker = APIDocCompletenessChecker()
        is_complete = checker.check_completeness(api_doc)

        # Assert
        assert is_complete is True

    def test_should_fail_if_api_doc_incomplete(self):
        """Test that documentation is considered incomplete if missing sections."""
        # Arrange
        api_doc = {
            "endpoint": "POST /api/users",
            "has_request_schema": True,
            "has_response_example": False,  # Missing response example!
            "has_error_codes": True,
            "has_description": True
        }

        # Act
        from devforgeai_documentation import APIDocCompletenessChecker
        checker = APIDocCompletenessChecker()
        is_complete = checker.check_completeness(api_doc)

        # Assert
        assert is_complete is False


class TestReadmeExistenceVerification:
    """Test verification that README.md exists and is current."""

    def test_should_verify_readme_exists(self):
        """Test that README.md file exists in project root."""
        # Arrange
        project_files = ["README.md", "src/index.ts", "package.json"]

        # Act
        from devforgeai_documentation import ReadmeVerifier
        verifier = ReadmeVerifier()
        exists = verifier.check_exists(project_files)

        # Assert
        assert exists is True

    def test_should_fail_if_readme_missing(self):
        """Test that gate fails if README.md is missing."""
        # Arrange
        project_files = ["src/index.ts", "package.json"]  # No README!

        # Act
        from devforgeai_documentation import ReadmeVerifier
        verifier = ReadmeVerifier()
        exists = verifier.check_exists(project_files)

        # Assert
        assert exists is False

    def test_should_verify_readme_is_current(self):
        """Test that README.md is not outdated (recently updated)."""
        # Arrange
        readme_metadata = {
            "path": "README.md",
            "last_updated": "2025-11-18",
            "current_date": "2025-11-18"
        }

        # Act
        from devforgeai_documentation import ReadmeVerifier
        verifier = ReadmeVerifier()
        is_current = verifier.check_is_current(readme_metadata)

        # Assert
        assert is_current is True

    def test_should_fail_if_readme_outdated(self):
        """Test that gate fails if README is older than 30 days."""
        # Arrange
        readme_metadata = {
            "last_updated": "2025-09-01",  # 2+ months old
            "current_date": "2025-11-18"
        }

        # Act
        from devforgeai_documentation import ReadmeVerifier
        verifier = ReadmeVerifier()
        is_current = verifier.check_is_current(readme_metadata)

        # Assert
        assert is_current is False

    def test_should_check_readme_content_quality(self):
        """Test that README has minimum required sections."""
        # Arrange
        readme_content = """# Project Name

## Installation
npm install

## Usage
npm run dev

## Contributing
See CONTRIBUTING.md
"""
        required_sections = ["Installation", "Usage"]

        # Act
        from devforgeai_documentation import ReadmeVerifier
        verifier = ReadmeVerifier()
        has_sections = verifier.check_has_sections(readme_content, required_sections)

        # Assert
        assert has_sections is True


class TestDiagramRenderingValidation:
    """Test validation that diagrams render correctly."""

    def test_should_validate_mermaid_diagram_syntax(self):
        """Test that Mermaid diagrams have valid syntax."""
        # Arrange
        diagram = """graph TD
            A[Start]
            B{Decision}
            C[End]
            A --> B
            B -->|Yes| C
            B -->|No| A
        """

        # Act
        from devforgeai_documentation import DiagramRenderingValidator
        validator = DiagramRenderingValidator()
        is_valid = validator.validate_syntax(diagram)

        # Assert
        assert is_valid is True

    def test_should_fail_if_diagram_has_syntax_error(self):
        """Test that validation fails for malformed diagrams."""
        # Arrange
        diagram = """graph TD
            A[Start
            B{Decision}
            A --> B
        """  # Missing closing bracket

        # Act
        from devforgeai_documentation import DiagramRenderingValidator
        validator = DiagramRenderingValidator()
        is_valid = validator.validate_syntax(diagram)

        # Assert
        assert is_valid is False

    def test_should_check_all_diagrams_in_documentation(self):
        """Test that all embedded diagrams are validated."""
        # Arrange
        documentation = """# Architecture

## System Design

\`\`\`mermaid
graph TD
    A[Component A]
    B[Component B]
    A --> B
\`\`\`

## Data Flow

\`\`\`mermaid
sequenceDiagram
    A->>B: Request
    B->>A: Response
\`\`\`
"""

        # Act
        from devforgeai_documentation import DiagramRenderingValidator
        validator = DiagramRenderingValidator()
        diagrams = validator.extract_diagrams(documentation)

        # Assert
        assert diagrams is not None
        assert len(diagrams) == 2

    def test_should_validate_all_diagram_syntax(self):
        """Test that all extracted diagrams are validated."""
        # Arrange
        diagrams = [
            "graph TD\nA[Node]\n",  # Valid
            "graph TD\nB{Decision}\n",  # Valid
        ]

        # Act
        from devforgeai_documentation import DiagramRenderingValidator
        validator = DiagramRenderingValidator()
        all_valid = all(validator.validate_syntax(d) for d in diagrams)

        # Assert
        assert all_valid is True


class TestQualityGateEnforcement:
    """Test enforcement of quality gates."""

    def test_should_block_release_if_coverage_insufficient(self):
        """Test that release is blocked if coverage <80%."""
        # Arrange
        coverage = 75  # Below 80%
        threshold = 80

        # Act
        from devforgeai_documentation import ReleaseGate
        gate = ReleaseGate()
        allowed = gate.check_coverage_gate(coverage, threshold)

        # Assert
        assert allowed is False

    def test_should_block_release_if_readme_missing(self):
        """Test that release is blocked if README.md missing."""
        # Arrange
        has_readme = False

        # Act
        from devforgeai_documentation import ReleaseGate
        gate = ReleaseGate()
        allowed = gate.check_readme_gate(has_readme)

        # Assert
        assert allowed is False

    def test_should_block_release_if_api_undocumented(self):
        """Test that release is blocked if any API undocumented."""
        # Arrange
        apis = [
            {"endpoint": "GET /api/users", "documented": True},
            {"endpoint": "POST /api/users", "documented": False}
        ]

        # Act
        from devforgeai_documentation import ReleaseGate
        gate = ReleaseGate()
        allowed = gate.check_api_documentation_gate(apis)

        # Assert
        assert allowed is False

    def test_should_block_release_if_diagram_invalid(self):
        """Test that release is blocked if diagrams have errors."""
        # Arrange
        diagrams = [
            {"valid": True},
            {"valid": False}  # Invalid!
        ]

        # Act
        from devforgeai_documentation import ReleaseGate
        gate = ReleaseGate()
        allowed = gate.check_diagram_gate(diagrams)

        # Assert
        assert allowed is False

    def test_should_allow_release_if_all_gates_pass(self):
        """Test that release is allowed when all gates pass."""
        # Arrange
        gates = {
            "coverage": True,  # ≥80%
            "readme": True,    # Exists and current
            "api_docs": True,  # All documented
            "diagrams": True   # All valid
        }

        # Act
        from devforgeai_documentation import ReleaseGate
        gate = ReleaseGate()
        allowed = gate.check_all_gates(gates)

        # Assert
        assert allowed is True

    def test_should_provide_blocking_reason(self):
        """Test that system explains why release is blocked."""
        # Arrange
        coverage = 75
        has_readme = False
        threshold = 80

        # Act
        from devforgeai_documentation import ReleaseGate
        gate = ReleaseGate()
        reasons = gate.get_blocking_reasons(coverage, has_readme, threshold)

        # Assert
        assert reasons is not None
        assert isinstance(reasons, list)
        assert len(reasons) >= 1
        # Should mention coverage and README
        reasons_text = str(reasons).lower()
        assert "coverage" in reasons_text or "80" in reasons_text
        assert "readme" in reasons_text


class TestQualityGateReporting:
    """Test quality gate validation reporting."""

    def test_should_generate_gate_report(self):
        """Test that quality gate validation report is generated."""
        # Arrange
        results = {
            "coverage": {"passed": True, "value": 85, "threshold": 80},
            "readme": {"passed": True},
            "api_docs": {"passed": False, "undocumented": ["GET /api/users"]},
            "diagrams": {"passed": True}
        }

        # Act
        from devforgeai_documentation import GateReporter
        reporter = GateReporter()
        report = reporter.generate_report(results)

        # Assert
        assert report is not None
        assert isinstance(report, str)

    def test_report_should_show_pass_fail_summary(self):
        """Test that report shows summary of passed/failed gates."""
        # Arrange
        results = {
            "coverage": True,
            "readme": True,
            "api_docs": False,
            "diagrams": True
        }

        # Act
        from devforgeai_documentation import GateReporter
        reporter = GateReporter()
        report = reporter.generate_report(results)

        # Assert
        assert report is not None
        # Should show 3 passed, 1 failed
        assert "3" in report or "pass" in report.lower()
        assert "1" in report or "fail" in report.lower()

    def test_report_should_include_remediation_steps(self):
        """Test that report suggests how to fix failing gates."""
        # Arrange
        failures = [
            {"gate": "coverage", "reason": "Only 75%, need 80%"},
            {"gate": "api_docs", "missing": ["GET /api/users"]}
        ]

        # Act
        from devforgeai_documentation import GateReporter
        reporter = GateReporter()
        remediation = reporter.get_remediation_steps(failures)

        # Assert
        assert remediation is not None
        assert isinstance(remediation, list)
        # Should suggest running /document
        remediation_text = str(remediation).lower()
        assert "document" in remediation_text or "generate" in remediation_text or "add" in remediation_text


class TestIntegrationWithReleaseCommand:
    """Test integration of quality gates with /release command."""

    def test_release_command_should_invoke_quality_gate(self):
        """Test that /release command checks documentation quality gate."""
        # Arrange
        story_id = "STORY-040"

        # Act
        from devforgeai_documentation import ReleaseQualityValidator
        validator = ReleaseQualityValidator()
        result = validator.validate_before_release(story_id)

        # Assert
        assert result is not None
        # Should return pass/fail result

    def test_should_display_gate_results_to_user(self):
        """Test that quality gate results are displayed clearly."""
        # Arrange
        gate_results = {
            "coverage": {"passed": True, "value": 85},
            "readme": {"passed": False},
            "api_docs": {"passed": True}
        }

        # Act
        from devforgeai_documentation import ResultDisplayer
        displayer = ResultDisplayer()
        output = displayer.format_results(gate_results)

        # Assert
        assert output is not None
        assert "✓" in output or "✗" in output or "PASS" in output or "FAIL" in output


class TestEdgeCases:
    """Test edge cases in quality gate validation."""

    def test_should_handle_zero_items(self):
        """Test that coverage calculation handles zero total items."""
        # Arrange
        documented = 0
        total = 0

        # Act
        from devforgeai_documentation import CoverageCalculator
        calc = CoverageCalculator()
        # Should handle gracefully (no division by zero)
        result = calc.calculate_coverage(documented, total)

        # Assert
        assert result is not None
        # Could be 0, 100, or special value

    def test_should_handle_no_public_apis(self):
        """Test that API gate passes if there are no public APIs."""
        # Arrange
        public_apis = []

        # Act
        from devforgeai_documentation import APIDocumentationVerifier
        verifier = APIDocumentationVerifier()
        result = verifier.verify_all_documented(public_apis)

        # Assert
        assert result is True  # No undocumented APIs = pass

    def test_should_handle_readme_with_no_sections(self):
        """Test that README validation handles minimal content."""
        # Arrange
        readme = "# My Project"

        # Act
        from devforgeai_documentation import ReadmeVerifier
        verifier = ReadmeVerifier()
        # Should not crash
        result = verifier.check_has_sections(readme, ["Installation"])

        # Assert
        assert result is not None
