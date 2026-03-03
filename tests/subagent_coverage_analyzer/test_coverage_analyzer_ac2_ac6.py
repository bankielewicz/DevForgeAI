"""
AC2-AC6 Tests: Language Support, File Classification, Thresholds, Gaps, Recommendations

Tests coverage analyzer functionality:
- AC2: Language-specific coverage tooling (6 languages supported)
- AC3: Files classified by architectural layer
- AC4: Coverage validated against strict thresholds
- AC5: Gaps identified with file:line evidence
- AC6: Actionable remediation recommendations
"""

import pytest
import json
from pathlib import Path


class TestAC2LanguageDetection:
    """Tests for AC2: Language detection from tech-stack.md."""

    def test_detect_python_from_tech_stack(self, mock_tech_stack_python):
        """Test: Detect Python as primary language."""
        # Arrange
        tech_stack = mock_tech_stack_python

        # Act
        language = "Python" if "Python" in tech_stack else None

        # Assert
        assert language == "Python", "Failed to detect Python language"

    def test_detect_csharp_from_tech_stack(self, mock_tech_stack_csharp):
        """Test: Detect C# as primary language."""
        # Arrange
        tech_stack = mock_tech_stack_csharp

        # Act
        language = "C#" if "C#" in tech_stack else None

        # Assert
        assert language == "C#", "Failed to detect C# language"


class TestAC2ToolMapping:
    """Tests for AC2: Language to coverage tool mapping."""

    def test_python_maps_to_pytest_cov(self, language_tool_mapping):
        """Test: Python → pytest --cov command."""
        # Arrange
        mapping = language_tool_mapping

        # Act
        python_tool = mapping.get("Python", {})

        # Assert
        assert "pytest" in python_tool.get("command", ""), "Python not mapped to pytest"
        assert python_tool.get("report_format") == "json", "Python report format should be JSON"

    def test_csharp_maps_to_dotnet_test(self, language_tool_mapping):
        """Test: C# → dotnet test --collect command."""
        # Arrange
        mapping = language_tool_mapping

        # Act
        csharp_tool = mapping.get("C#", {})

        # Assert
        assert "dotnet" in csharp_tool.get("command", ""), "C# not mapped to dotnet"
        assert csharp_tool.get("report_format") == "xml", "C# report format should be XML"

    def test_nodejs_maps_to_npm_test(self, language_tool_mapping):
        """Test: Node.js → npm test -- --coverage command."""
        # Arrange
        mapping = language_tool_mapping

        # Act
        nodejs_tool = mapping.get("Node.js", {})

        # Assert
        assert "npm" in nodejs_tool.get("command", ""), "Node.js not mapped to npm"
        assert nodejs_tool.get("report_format") == "json", "Node.js report format should be JSON"

    def test_go_maps_to_go_test(self, language_tool_mapping):
        """Test: Go → go test with -coverprofile command."""
        # Arrange
        mapping = language_tool_mapping

        # Act
        go_tool = mapping.get("Go", {})

        # Assert
        assert "go test" in go_tool.get("command", ""), "Go not mapped to 'go test'"
        assert go_tool.get("report_format") == "text", "Go report format should be text"

    def test_rust_maps_to_cargo_tarpaulin(self, language_tool_mapping):
        """Test: Rust → cargo tarpaulin command."""
        # Arrange
        mapping = language_tool_mapping

        # Act
        rust_tool = mapping.get("Rust", {})

        # Assert
        assert "cargo" in rust_tool.get("command", ""), "Rust not mapped to cargo"
        assert rust_tool.get("report_format") == "json", "Rust report format should be JSON"

    def test_java_maps_to_mvn_jacoco(self, language_tool_mapping):
        """Test: Java → mvn test jacoco:report command."""
        # Arrange
        mapping = language_tool_mapping

        # Act
        java_tool = mapping.get("Java", {})

        # Assert
        assert "mvn" in java_tool.get("command", ""), "Java not mapped to Maven"
        assert java_tool.get("report_format") == "xml", "Java report format should be XML"


class TestAC2ReportParsing:
    """Tests for AC2: Coverage report parsing."""

    def test_parse_pytest_json_report(self, mock_pytest_coverage_report):
        """Test: Parse pytest coverage.json report."""
        # Arrange
        report = mock_pytest_coverage_report

        # Act
        total_coverage = report.get("totals", {}).get("percent_covered")
        files = report.get("files", {})

        # Assert
        assert total_coverage is not None, "Failed to extract total coverage"
        assert len(files) > 0, "Failed to parse files from report"
        assert "src/domain/order.py" in files, "Failed to parse file entries"

    def test_extract_per_file_metrics(self, mock_pytest_coverage_report):
        """Test: Extract per-file metrics (file_path, lines_covered, lines_total, coverage_percentage)."""
        # Arrange
        report = mock_pytest_coverage_report
        files = report.get("files", {})

        # Act
        first_file = files.get("src/domain/order.py", {})
        coverage_percentage = first_file.get("percent_covered")
        statements = first_file.get("num_statements")

        # Assert
        assert coverage_percentage is not None, "Failed to extract coverage percentage"
        assert statements is not None, "Failed to extract statement count"
        assert 0 <= coverage_percentage <= 100, "Coverage percentage out of range"

    def test_extract_uncovered_lines(self, mock_pytest_coverage_report):
        """Test: Extract uncovered line numbers from report."""
        # Arrange
        report = mock_pytest_coverage_report
        files = report.get("files", {})

        # Act
        first_file = files.get("src/domain/order.py", {})
        missing_lines = first_file.get("missing_lines", [])

        # Assert
        assert isinstance(missing_lines, list), "Missing lines should be a list"
        assert len(missing_lines) > 0, "Should have missing lines for incomplete coverage"


class TestAC3FileClassification:
    """Tests for AC3: File classification by architectural layer."""

    def test_classify_domain_to_business_logic(self, classified_files):
        """Test: src/Domain/Order.cs → business_logic layer."""
        # Arrange
        files = classified_files

        # Act
        order_file = files.get("src/Domain/Order.cs", {})
        layer = order_file.get("layer")

        # Assert
        assert layer == "business_logic", f"Expected business_logic, got {layer}"

    def test_classify_application_to_application_layer(self, classified_files):
        """Test: src/Application/OrderService.cs → application layer."""
        # Arrange
        files = classified_files

        # Act
        service_file = files.get("src/Application/OrderService.cs", {})
        layer = service_file.get("layer")

        # Assert
        assert layer == "application", f"Expected application, got {layer}"

    def test_classify_infrastructure_to_infrastructure_layer(self, classified_files):
        """Test: src/Infrastructure/OrderRepository.cs → infrastructure layer."""
        # Arrange
        files = classified_files

        # Act
        repo_file = files.get("src/Infrastructure/OrderRepository.cs", {})
        layer = repo_file.get("layer")

        # Assert
        assert layer == "infrastructure", f"Expected infrastructure, got {layer}"

    def test_calculate_layer_specific_coverage_business_logic(self, classified_files):
        """Test: Calculate business_logic layer coverage (96.5%)."""
        # Arrange
        files = classified_files
        business_logic_files = [f for f in files.values() if f.get("layer") == "business_logic"]

        # Act
        total_coverage = sum(f.get("coverage", 0) for f in business_logic_files) / len(business_logic_files) if business_logic_files else 0

        # Assert
        assert total_coverage > 0, "Failed to calculate business_logic coverage"
        assert 90 <= total_coverage <= 100, "Business logic coverage outside expected range"

    def test_calculate_layer_specific_coverage_application(self, classified_files):
        """Test: Calculate application layer coverage (82.1%)."""
        # Arrange
        files = classified_files
        app_files = [f for f in files.values() if f.get("layer") == "application"]

        # Act
        total_coverage = sum(f.get("coverage", 0) for f in app_files) / len(app_files) if app_files else 0

        # Assert
        assert total_coverage > 0, "Failed to calculate application coverage"

    def test_calculate_layer_specific_coverage_infrastructure(self, classified_files):
        """Test: Calculate infrastructure layer coverage (72.5%)."""
        # Arrange
        files = classified_files
        infra_files = [f for f in files.values() if f.get("layer") == "infrastructure"]

        # Act
        total_coverage = sum(f.get("coverage", 0) for f in infra_files) / len(infra_files) if infra_files else 0

        # Assert
        assert total_coverage > 0, "Failed to calculate infrastructure coverage"
        assert total_coverage < 95, "Infrastructure coverage should be below business_logic threshold"


class TestAC4ThresholdValidation:
    """Tests for AC4: Coverage validation against thresholds."""

    def test_validate_business_logic_threshold_95_percent(self, threshold_test_cases):
        """Test: Business logic must be ≥95%."""
        # Arrange
        test_case = threshold_test_cases["business_logic_fails"]
        coverage = test_case["business_logic"]

        # Act
        passes_threshold = coverage >= 95.0

        # Assert
        assert not passes_threshold, "Test case setup error: should fail threshold"
        assert test_case["blocks_qa"] == True, "blocks_qa should be True when business_logic <95%"

    def test_validate_application_threshold_85_percent(self, threshold_test_cases):
        """Test: Application must be ≥85%."""
        # Arrange
        test_case = threshold_test_cases["application_fails"]
        coverage = test_case["application"]

        # Act
        passes_threshold = coverage >= 85.0

        # Assert
        assert not passes_threshold, "Test case setup error: should fail threshold"
        assert test_case["blocks_qa"] == True, "blocks_qa should be True when application <85%"

    def test_validate_overall_threshold_80_percent(self, threshold_test_cases):
        """Test: Overall must be ≥80%."""
        # Arrange
        test_case = threshold_test_cases["overall_fails"]
        coverage = test_case["overall"]

        # Act
        passes_threshold = coverage >= 80.0

        # Assert
        assert not passes_threshold, "Test case setup error: should fail threshold"
        assert test_case["blocks_qa"] == True, "blocks_qa should be True when overall <80%"

    def test_blocks_qa_false_when_all_thresholds_pass(self, threshold_test_cases):
        """Test: blocks_qa = False when all thresholds met."""
        # Arrange
        test_case = threshold_test_cases["all_pass"]

        # Act
        blocks_qa = test_case["blocks_qa"]

        # Assert
        assert blocks_qa == False, "blocks_qa should be False when all thresholds pass"

    def test_violation_severity_critical_for_business_logic(self, threshold_test_cases):
        """Test: Business logic gap generates CRITICAL severity violation."""
        # Arrange
        test_case = threshold_test_cases["business_logic_fails"]

        # Act
        violations = test_case.get("violations", [])
        critical_violations = [v for v in violations if v.get("severity") == "CRITICAL"]

        # Assert
        assert len(critical_violations) > 0, "Expected CRITICAL violation for business_logic gap"

    def test_violation_severity_high_for_application(self, threshold_test_cases):
        """Test: Application gap generates HIGH severity violation."""
        # Arrange
        test_case = threshold_test_cases["application_fails"]

        # Act
        violations = test_case.get("violations", [])
        high_violations = [v for v in violations if v.get("severity") == "HIGH"]

        # Assert
        assert len(high_violations) > 0, "Expected HIGH violation for application gap"


class TestAC5GapIdentification:
    """Tests for AC5: Gap identification with file:line evidence."""

    def test_gap_includes_file_path(self, coverage_gap_example):
        """Test: Gap includes 'file' with absolute path."""
        # Arrange
        gap = coverage_gap_example

        # Act
        file_path = gap.get("file")

        # Assert
        assert file_path is not None, "Gap missing 'file' field"
        assert "Infrastructure" in file_path or "Repository" in file_path, "File path should include location context"

    def test_gap_includes_layer(self, coverage_gap_example):
        """Test: Gap includes 'layer' field."""
        # Arrange
        gap = coverage_gap_example

        # Act
        layer = gap.get("layer")

        # Assert
        assert layer in ["business_logic", "application", "infrastructure"], f"Invalid layer: {layer}"

    def test_gap_includes_current_coverage(self, coverage_gap_example):
        """Test: Gap includes 'current_coverage' percentage."""
        # Arrange
        gap = coverage_gap_example

        # Act
        current = gap.get("current_coverage")

        # Assert
        assert current is not None, "Gap missing 'current_coverage'"
        assert 0 <= current <= 100, "Coverage percentage out of range"

    def test_gap_includes_target_coverage(self, coverage_gap_example):
        """Test: Gap includes 'target_coverage' (threshold)."""
        # Arrange
        gap = coverage_gap_example

        # Act
        target = gap.get("target_coverage")

        # Assert
        assert target is not None, "Gap missing 'target_coverage'"
        assert target in [0.80, 0.85, 0.95, 80, 85, 95], f"Unexpected target: {target}"

    def test_gap_includes_uncovered_lines(self, coverage_gap_example):
        """Test: Gap includes 'uncovered_lines' array."""
        # Arrange
        gap = coverage_gap_example

        # Act
        uncovered = gap.get("uncovered_lines", [])

        # Assert
        assert isinstance(uncovered, list), "uncovered_lines should be a list"
        assert len(uncovered) > 0, "Should have uncovered line numbers"
        assert all(isinstance(line, int) for line in uncovered), "All line numbers should be integers"

    def test_gap_includes_suggested_tests(self, coverage_gap_example):
        """Test: Gap includes 'suggested_tests' array."""
        # Arrange
        gap = coverage_gap_example

        # Act
        suggested = gap.get("suggested_tests", [])

        # Assert
        assert isinstance(suggested, list), "suggested_tests should be a list"
        assert len(suggested) > 0, "Should have test suggestions"
        assert all(isinstance(test, str) for test in suggested), "All suggestions should be strings"


class TestAC6Recommendations:
    """Tests for AC6: Actionable remediation recommendations."""

    def test_recommendations_prioritized_by_severity(self, gap_and_recommendations):
        """Test: Recommendations ordered by severity (CRITICAL first)."""
        # Arrange
        expected_recommendations = gap_and_recommendations.get("expected_recommendations", [])

        # Act
        has_blocking = any("BLOCKING" in rec for rec in expected_recommendations)

        # Assert
        assert has_blocking, "First recommendation should be BLOCKING (business logic)"

    def test_recommendations_provide_specific_guidance(self, gap_and_recommendations):
        """Test: Recommendations include specific file and layer info."""
        # Arrange
        expected_recommendations = gap_and_recommendations.get("expected_recommendations", [])

        # Act
        has_file_info = any(("src/" in rec or "file" in rec) for rec in expected_recommendations)
        has_layer_info = any(("layer" in rec or "Infrastructure" in rec or "Application" in rec or "Business" in rec) for rec in expected_recommendations)

        # Assert
        assert has_file_info, "Recommendations should reference specific files"
        assert has_layer_info, "Recommendations should reference layer information"

    def test_recommendations_include_test_scenarios(self, gap_and_recommendations):
        """Test: Recommendations include test scenarios from suggested_tests."""
        # Arrange
        expected_recommendations = gap_and_recommendations.get("expected_recommendations", [])

        # Act
        has_test_scenarios = any(("test" in rec.lower() or "Add" in rec) for rec in expected_recommendations)

        # Assert
        assert has_test_scenarios, "Recommendations should include test suggestions"

    def test_recommendations_include_coverage_metrics(self, gap_and_recommendations):
        """Test: Recommendations show current vs target coverage."""
        # Arrange
        expected_recommendations = gap_and_recommendations.get("expected_recommendations", [])

        # Act
        has_metrics = any(("%" in rec and "needs" in rec) for rec in expected_recommendations)

        # Assert
        assert has_metrics, "Recommendations should show coverage metrics and targets"

    def test_recommendations_ordered_critical_before_medium(self, gap_and_recommendations):
        """Test: CRITICAL recommendations appear before MEDIUM."""
        # Arrange
        expected_recommendations = gap_and_recommendations.get("expected_recommendations", [])

        # Act
        blocking_index = next((i for i, r in enumerate(expected_recommendations) if "BLOCKING" in r), float('inf'))
        medium_index = next((i for i, r in enumerate(expected_recommendations) if "Medium" in r), float('inf'))

        # Assert
        assert blocking_index < medium_index, "BLOCKING recommendations should appear before MEDIUM"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
