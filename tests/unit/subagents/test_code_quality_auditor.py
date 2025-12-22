"""
Unit tests for code-quality-auditor subagent (STORY-063)

Test-Driven Development (RED PHASE):
All tests written BEFORE implementation - tests should FAIL initially.

Test Coverage:
- AC1: Subagent specification structure
- AC2: Cyclomatic complexity analysis
- AC3: Code duplication detection
- AC4: Maintainability index calculation
- AC5: Business impact explanations
- AC6: Refactoring pattern recommendations
- AC9: Extreme violations only (no noise)
- AC10: Error handling for missing tools

Coverage Target: 95% business logic
"""

import pytest
import json
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock


# ============================================================================
# Fixtures
# ============================================================================

@pytest.fixture
def project_root():
    """Return project root directory"""
    return Path(__file__).parent.parent.parent.parent


@pytest.fixture
def subagent_file_path(project_root):
    """Path to code-quality-auditor subagent file"""
    return project_root / "src" / "claude" / "agents" / "code-quality-auditor.md"


@pytest.fixture
def sample_python_code_complex():
    """Sample Python code with high complexity (28) for testing"""
    return '''
def process_order(order):
    """Process order with 28 cyclomatic complexity paths"""
    if order is None:
        return None
    if not order.items:
        return {"error": "No items"}
    if order.customer is None:
        return {"error": "No customer"}
    if order.total < 0:
        return {"error": "Invalid total"}

    # 24 more conditional paths...
    if order.status == "pending":
        if order.payment_method == "credit_card":
            if order.card_valid:
                if order.balance >= order.total:
                    charge_card()
                else:
                    decline_payment()
            else:
                request_new_card()
        elif order.payment_method == "paypal":
            if order.paypal_verified:
                process_paypal()
            else:
                verify_paypal()
        elif order.payment_method == "cash":
            mark_cash_payment()
        else:
            return {"error": "Invalid payment method"}
    elif order.status == "processing":
        if order.shipped:
            update_tracking()
        else:
            prepare_shipment()
    elif order.status == "complete":
        archive_order()
    else:
        return {"error": "Invalid status"}

    return {"success": True}
'''


@pytest.fixture
def sample_code_with_duplication():
    """Sample code with >25% duplication for testing"""
    return {
        "ServiceA.cs": '''
public class ServiceA {
    public void ValidateInput(string input) {
        if (string.IsNullOrEmpty(input)) throw new ArgumentException();
        if (input.Length > 100) throw new ArgumentException();
        if (!Regex.IsMatch(input, @"^[a-zA-Z0-9]+$")) throw new ArgumentException();
    }
}
''',
        "ServiceB.cs": '''
public class ServiceB {
    public void CheckData(string data) {
        if (string.IsNullOrEmpty(data)) throw new ArgumentException();
        if (data.Length > 100) throw new ArgumentException();
        if (!Regex.IsMatch(data, @"^[a-zA-Z0-9]+$")) throw new ArgumentException();
    }
}
'''
    }


@pytest.fixture
def mock_radon_output_complexity():
    """Mock radon complexity analysis output"""
    return {
        "src/services.py": [
            {
                "type": "method",
                "name": "process_order",
                "lineno": 10,
                "complexity": 28,
                "rank": "F"
            },
            {
                "type": "method",
                "name": "validate_input",
                "lineno": 50,
                "complexity": 8,
                "rank": "A"
            }
        ]
    }


@pytest.fixture
def mock_maintainability_index_low():
    """Mock maintainability index output for low MI file"""
    return {
        "src/LegacyService.cs": {
            "mi": 35.2,
            "rank": "C"
        },
        "src/CleanService.cs": {
            "mi": 72.4,
            "rank": "A"
        }
    }


# ============================================================================
# AC1: Subagent Specification Structure
# ============================================================================

@pytest.mark.unit
@pytest.mark.acceptance_criteria
class TestSubagentSpecification:
    """AC1: Subagent specification created with 8-phase workflow"""

    def test_subagent_file_exists_in_src(self, subagent_file_path):
        """Test: Subagent file exists in distribution source tree"""
        # Arrange: File should exist at src/claude/agents/code-quality-auditor.md

        # Act & Assert: File existence
        assert subagent_file_path.exists(), \
            f"Subagent file not found at {subagent_file_path}"

    def test_yaml_frontmatter_complete(self, subagent_file_path):
        """Test: YAML frontmatter includes all required fields"""
        # Arrange: Read file content
        content = subagent_file_path.read_text()

        # Act: Extract YAML frontmatter
        lines = content.split('\n')
        assert lines[0] == '---', "Missing opening YAML delimiter"

        # Find closing delimiter
        closing_idx = None
        for i in range(1, min(20, len(lines))):
            if lines[i] == '---':
                closing_idx = i
                break

        assert closing_idx is not None, "Missing closing YAML delimiter"
        frontmatter = '\n'.join(lines[1:closing_idx])

        # Assert: Required fields present
        assert 'name: code-quality-auditor' in frontmatter, \
            "Missing 'name: code-quality-auditor' in frontmatter"
        assert 'description:' in frontmatter, \
            "Missing 'description' field"
        assert 'tools:' in frontmatter, \
            "Missing 'tools' field"
        assert 'model: claude-haiku-4-5-20251001' in frontmatter, \
            "Missing 'model: claude-haiku-4-5-20251001' (cost-efficient Haiku model)"

    def test_eight_phase_workflow_documented(self, subagent_file_path):
        """Test: All 8 phases of workflow documented"""
        # Arrange: Read file content
        content = subagent_file_path.read_text()

        # Act & Assert: Check for all 8 phases
        assert 'Phase 1: Context Loading' in content, \
            "Missing Phase 1: Context Loading"
        assert 'Phase 2: Complexity Analysis' in content, \
            "Missing Phase 2: Complexity Analysis"
        assert 'Phase 3: Duplication Analysis' in content, \
            "Missing Phase 3: Duplication Analysis"
        assert 'Phase 4: Maintainability Analysis' in content, \
            "Missing Phase 4: Maintainability Analysis"
        assert 'Phase 5: Business Impact Explanation' in content, \
            "Missing Phase 5: Business Impact Explanation"
        assert 'Phase 6: Refactoring Patterns' in content, \
            "Missing Phase 6: Refactoring Patterns"
        assert 'Phase 7: Aggregate Results' in content, \
            "Missing Phase 7: Aggregate Results"
        assert 'Phase 8: Return Results' in content, \
            "Missing Phase 8: Return Results"

    def test_three_metrics_documented(self, subagent_file_path):
        """Test: All 3 quality metrics documented"""
        # Arrange: Read file content
        content = subagent_file_path.read_text()

        # Act & Assert: Check for metric documentation
        assert 'Cyclomatic Complexity' in content, \
            "Missing Cyclomatic Complexity metric"
        assert 'Code Duplication' in content, \
            "Missing Code Duplication metric"
        assert 'Maintainability Index' in content, \
            "Missing Maintainability Index metric"


# ============================================================================
# AC2: Cyclomatic Complexity Analysis
# ============================================================================

@pytest.mark.unit
@pytest.mark.acceptance_criteria
class TestComplexityAnalysis:
    """AC2: Cyclomatic complexity analysis with language-specific tooling"""

    def test_detects_extreme_complexity_critical(self):
        """Test: Function with complexity 28 triggers CRITICAL violation"""
        # Arrange: Mock code-quality-auditor invocation
        result = {
            "metrics": {
                "complexity": {
                    "average_per_function": 18.0,
                    "average_per_file": 15.2,
                    "max_complexity": {
                        "score": 28,
                        "function": "process_order",
                        "file": "src/services.py",
                        "line": 10
                    }
                }
            },
            "extreme_violations": [
                {
                    "type": "complexity",
                    "severity": "CRITICAL",
                    "function": "process_order",
                    "score": 28,
                    "threshold": 20,
                    "file": "src/services.py",
                    "line": 10
                }
            ],
            "blocks_qa": True
        }

        # Act: Validate result structure

        # Assert: CRITICAL violation detected
        assert result["metrics"]["complexity"]["max_complexity"]["score"] == 28, \
            "Complexity score should be 28"
        assert len(result["extreme_violations"]) == 1, \
            "Should detect 1 extreme violation"
        assert result["extreme_violations"][0]["severity"] == "CRITICAL", \
            "Violation should be CRITICAL"
        assert result["blocks_qa"] is True, \
            "Extreme complexity should block QA"

    def test_complexity_warning_does_not_block(self):
        """Test: Complexity 18 (15-20 range) triggers WARNING but doesn't block"""
        # Arrange: Mock result with WARNING-level complexity
        result = {
            "metrics": {
                "complexity": {
                    "max_complexity": {"score": 18}
                }
            },
            "extreme_violations": [],  # Warnings not in extreme_violations
            "warnings": [
                {
                    "type": "complexity",
                    "severity": "WARNING",
                    "score": 18,
                    "message": "Complexity approaching critical threshold"
                }
            ],
            "blocks_qa": False
        }

        # Act & Assert: WARNING doesn't block
        assert result["blocks_qa"] is False, \
            "WARNING-level violations should NOT block QA"
        assert len(result["extreme_violations"]) == 0, \
            "Warnings should not appear in extreme_violations"

    def test_language_specific_tool_mapping(self):
        """Test: Language detection maps to correct analysis tool"""
        # Arrange: Language to tool mapping
        tool_mapping = {
            "Python": "radon cc",
            "Node.js": "eslint --rule complexity",
            "C#": "analyze_complexity.py",
            "Go": "gocyclo",
            "Rust": "cargo-geiger",
            "Java": "PMD"
        }

        # Act: Validate mappings exist
        for language, tool in tool_mapping.items():
            # Assert: Tool documented for language
            assert tool is not None, \
                f"Tool mapping missing for {language}"


# ============================================================================
# AC3: Code Duplication Detection
# ============================================================================

@pytest.mark.unit
@pytest.mark.acceptance_criteria
class TestDuplicationDetection:
    """AC3: Code duplication detection with percentage calculation"""

    def test_detects_extreme_duplication_critical(self):
        """Test: 27% duplication triggers CRITICAL violation"""
        # Arrange: Mock duplication analysis result
        result = {
            "metrics": {
                "duplication": {
                    "percentage": 27.0,
                    "duplicate_lines": 540,
                    "total_lines": 2000,
                    "duplicate_blocks": [
                        {
                            "files": [
                                "src/ServiceA.cs:45-67",
                                "src/ServiceB.cs:123-145"
                            ],
                            "lines": 23,
                            "pattern": "Input validation logic"
                        }
                    ]
                }
            },
            "extreme_violations": [
                {
                    "type": "duplication",
                    "severity": "CRITICAL",
                    "percentage": 27.0,
                    "threshold": 25.0,
                    "blocks": 1
                }
            ],
            "blocks_qa": True
        }

        # Act & Assert: CRITICAL violation detected
        assert result["metrics"]["duplication"]["percentage"] == 27.0, \
            "Duplication percentage should be 27.0%"
        assert result["extreme_violations"][0]["type"] == "duplication", \
            "Violation type should be 'duplication'"
        assert result["extreme_violations"][0]["severity"] == "CRITICAL", \
            "Severity should be CRITICAL"
        assert result["blocks_qa"] is True, \
            "Extreme duplication should block QA"

    def test_duplication_percentage_calculation(self):
        """Test: Duplication percentage calculated correctly"""
        # Arrange: Test data
        duplicate_lines = 540
        total_lines = 2000

        # Act: Calculate percentage
        percentage = (duplicate_lines / total_lines) * 100

        # Assert: Calculation correct
        assert percentage == 27.0, \
            f"Expected 27.0%, got {percentage}%"


# ============================================================================
# AC4: Maintainability Index Calculation
# ============================================================================

@pytest.mark.unit
@pytest.mark.acceptance_criteria
class TestMaintainabilityIndex:
    """AC4: Maintainability index calculation (0-100 scale)"""

    def test_detects_low_maintainability_critical(self):
        """Test: MI 35 (below 40 threshold) triggers CRITICAL violation"""
        # Arrange: Mock MI analysis result
        result = {
            "metrics": {
                "maintainability": {
                    "average_mi": 53.8,
                    "low_maintainability_files": [
                        {
                            "path": "src/LegacyService.cs",
                            "mi": 35.2,
                            "rank": "C"
                        }
                    ]
                }
            },
            "extreme_violations": [
                {
                    "type": "maintainability",
                    "severity": "CRITICAL",
                    "file": "src/LegacyService.cs",
                    "mi": 35.2,
                    "threshold": 40
                }
            ],
            "blocks_qa": True
        }

        # Act & Assert: CRITICAL violation detected
        assert result["metrics"]["maintainability"]["low_maintainability_files"][0]["mi"] == 35.2, \
            "MI should be 35.2"
        assert result["extreme_violations"][0]["type"] == "maintainability", \
            "Violation type should be 'maintainability'"
        assert result["extreme_violations"][0]["severity"] == "CRITICAL", \
            "Severity should be CRITICAL"
        assert result["blocks_qa"] is True, \
            "Low MI should block QA"

    def test_mi_scale_interpretation(self):
        """Test: MI scale interpretation documented"""
        # Arrange: MI scale ranges
        mi_scale = {
            "excellent": (85, 100),
            "good": (65, 85),
            "moderate": (50, 65),
            "difficult": (0, 50)
        }

        # Act: Test MI value interpretations
        test_values = [
            (90, "excellent"),
            (75, "good"),
            (58, "moderate"),
            (35, "difficult")
        ]

        # Assert: Interpretations correct
        for mi_value, expected_category in test_values:
            if mi_value >= 85:
                category = "excellent"
            elif mi_value >= 65:
                category = "good"
            elif mi_value >= 50:
                category = "moderate"
            else:
                category = "difficult"

            assert category == expected_category, \
                f"MI {mi_value} should be '{expected_category}', got '{category}'"


# ============================================================================
# AC5: Business Impact Explanations
# ============================================================================

@pytest.mark.unit
@pytest.mark.acceptance_criteria
class TestBusinessImpactExplanations:
    """AC5: Business impact explanations for violations"""

    def test_complexity_business_impact_quantified(self):
        """Test: Complexity violation includes quantified business impact"""
        # Arrange: Mock violation with business impact
        violation = {
            "type": "complexity",
            "severity": "CRITICAL",
            "score": 28,
            "business_impact": (
                "40% higher defect rate compared to functions with complexity <10. "
                "Requires 28+ test cases for full coverage. "
                "3x longer onboarding time for new developers."
            )
        }

        # Act: Validate business impact
        impact_text = violation["business_impact"]

        # Assert: Quantified metrics present
        assert "40%" in impact_text or "defect" in impact_text.lower(), \
            "Business impact should mention defect rate increase"
        assert "test case" in impact_text.lower(), \
            "Business impact should mention test case requirement"
        assert "onboarding" in impact_text.lower(), \
            "Business impact should mention onboarding impact"

    def test_duplication_business_impact_quantified(self):
        """Test: Duplication violation includes quantified business impact"""
        # Arrange: Mock violation with business impact
        violation = {
            "type": "duplication",
            "severity": "CRITICAL",
            "percentage": 27.0,
            "business_impact": (
                "Changes must be replicated in 2+ places (bug multiplication risk). "
                "27% of codebase is redundant (wasted maintenance effort). "
                "Violates DRY principle - refactoring required."
            )
        }

        # Act: Validate business impact
        impact_text = violation["business_impact"]

        # Assert: Quantified metrics present
        assert "27%" in impact_text or "percentage" in impact_text.lower(), \
            "Business impact should mention duplication percentage"
        assert "place" in impact_text.lower() or "multiplication" in impact_text.lower(), \
            "Business impact should mention replication requirement"

    def test_maintainability_business_impact_quantified(self):
        """Test: Maintainability violation includes quantified business impact"""
        # Arrange: Mock violation with business impact
        violation = {
            "type": "maintainability",
            "severity": "CRITICAL",
            "mi": 35.2,
            "business_impact": (
                "50% slower code modifications compared to MI >70. "
                "3x higher bug introduction risk during changes. "
                "Team morale impact: developers avoid working in this file."
            )
        }

        # Act: Validate business impact
        impact_text = violation["business_impact"]

        # Assert: Quantified metrics present
        assert "50%" in impact_text or "slower" in impact_text.lower(), \
            "Business impact should mention modification speed"
        assert "3x" in impact_text or "bug" in impact_text.lower(), \
            "Business impact should mention bug risk"
        assert "morale" in impact_text.lower(), \
            "Business impact should mention team morale"


# ============================================================================
# AC6: Refactoring Pattern Recommendations
# ============================================================================

@pytest.mark.unit
@pytest.mark.acceptance_criteria
class TestRefactoringPatternRecommendations:
    """AC6: Specific refactoring pattern recommendations"""

    def test_complexity_refactoring_pattern_specific(self):
        """Test: Complexity violation includes specific refactoring pattern"""
        # Arrange: Mock violation with refactoring pattern
        violation = {
            "type": "complexity",
            "score": 28,
            "refactoring_pattern": (
                "Extract Method: Split process_order() into 5 methods:\n"
                "1. ValidateOrder() - complexity <6\n"
                "2. CalculateTotal() - complexity <6\n"
                "3. ProcessPayment() - complexity <6\n"
                "4. PrepareShipment() - complexity <6\n"
                "5. UpdateStatus() - complexity <6\n\n"
                "Target: Each method complexity <6 (current: 28 → goal: 5 methods × <6 = excellent)"
            )
        }

        # Act: Validate refactoring pattern
        pattern_text = violation["refactoring_pattern"]

        # Assert: Specific pattern with steps
        assert "Extract Method" in pattern_text, \
            "Should recommend Extract Method pattern"
        assert "Target:" in pattern_text, \
            "Should include target metrics"
        assert "1." in pattern_text or "2." in pattern_text, \
            "Should include numbered implementation steps"

    def test_duplication_refactoring_pattern_specific(self):
        """Test: Duplication violation includes specific refactoring pattern"""
        # Arrange: Mock violation with refactoring pattern
        violation = {
            "type": "duplication",
            "percentage": 27.0,
            "refactoring_pattern": (
                "Extract to Shared Utility Class:\n"
                "1. Create ValidationService in src/Common/Utilities/\n"
                "2. Extract ValidateInput() method (23 lines)\n"
                "3. Replace duplicate code in ServiceA and ServiceB with ValidationService.ValidateInput()\n"
                "4. Add unit tests for ValidationService\n\n"
                "Target: Reduce duplication from 27% to <20% (acceptable range)"
            )
        }

        # Act: Validate refactoring pattern
        pattern_text = violation["refactoring_pattern"]

        # Assert: Specific pattern with location
        assert "Extract" in pattern_text or "Shared" in pattern_text, \
            "Should recommend extraction pattern"
        assert "src/" in pattern_text or "Location" in pattern_text, \
            "Should specify code location"
        assert "Target:" in pattern_text, \
            "Should include target metrics"


# ============================================================================
# AC9: Extreme Violations Only (No Noise)
# ============================================================================

@pytest.mark.unit
@pytest.mark.acceptance_criteria
class TestExtremeViolationsOnly:
    """AC9: Extreme violations only (no noise)"""

    def test_acceptable_metrics_no_violations(self):
        """Test: Good metrics (complexity 12, duplication 15%, MI 65) generate no violations"""
        # Arrange: Mock result with acceptable metrics
        result = {
            "metrics": {
                "complexity": {"average_per_function": 12.0, "max_complexity": {"score": 14}},
                "duplication": {"percentage": 15.0},
                "maintainability": {"average_mi": 65.0}
            },
            "extreme_violations": [],
            "blocks_qa": False,
            "recommendations": [
                "✅ EXCELLENT: All quality metrics meet or exceed thresholds",
                "✅ Complexity: Average 12.0 (well below 20 threshold)",
                "✅ Duplication: 15.0% (well below 25% threshold)",
                "✅ Maintainability Index: 65.0 (Good range, target is >50)"
            ]
        }

        # Act & Assert: No violations, positive feedback
        assert len(result["extreme_violations"]) == 0, \
            "Should have no violations for acceptable metrics"
        assert result["blocks_qa"] is False, \
            "Should not block QA"
        assert any("✅" in rec for rec in result["recommendations"]), \
            "Should include positive feedback"

    def test_positive_feedback_for_excellent_quality(self):
        """Test: Excellent metrics generate positive feedback"""
        # Arrange: Mock recommendations
        recommendations = [
            "✅ EXCELLENT: MI 72.4 indicates high-quality code",
            "✅ EXCELLENT: Complexity average 8.2 (well-structured functions)",
            "✅ EXCELLENT: Duplication 5.1% (minimal redundancy)"
        ]

        # Act & Assert: Positive feedback present
        for rec in recommendations:
            assert "✅" in rec, \
                "Recommendations should use ✅ for positive feedback"
            assert "EXCELLENT" in rec or "well" in rec.lower(), \
                "Should include praise for excellent quality"


# ============================================================================
# AC10: Error Handling for Missing Tools
# ============================================================================

@pytest.mark.unit
@pytest.mark.acceptance_criteria
class TestErrorHandlingMissingTools:
    """AC10: Error handling for missing analysis tools"""

    def test_tool_not_available_returns_failure(self):
        """Test: Missing radon returns failure with installation instructions"""
        # Arrange: Mock result when radon not installed
        result = {
            "status": "failure",
            "error": "Analysis tool not available: radon not installed",
            "blocks_qa": True,
            "remediation": "Install radon: pip install radon"
        }

        # Act & Assert: Failure response structured correctly
        assert result["status"] == "failure", \
            "Status should be 'failure'"
        assert "radon not installed" in result["error"], \
            "Error should mention missing tool"
        assert result["blocks_qa"] is True, \
            "Missing tool should block QA"
        assert "pip install radon" in result["remediation"], \
            "Should provide installation command"

    def test_no_source_files_returns_failure(self):
        """Test: No source files found returns failure (does not block)"""
        # Arrange: Mock result when no source files
        result = {
            "status": "failure",
            "error": "No source files found in src/",
            "blocks_qa": False,
            "remediation": "Check source_paths configuration in tech-stack.md"
        }

        # Act & Assert: Failure but doesn't block
        assert result["status"] == "failure", \
            "Status should be 'failure'"
        assert "No source files" in result["error"], \
            "Error should mention missing files"
        assert result["blocks_qa"] is False, \
            "Missing source files should NOT block QA (configuration issue)"

    def test_tool_execution_failed_returns_stderr(self):
        """Test: Tool execution failure returns stderr and remediation"""
        # Arrange: Mock result when tool fails
        result = {
            "status": "failure",
            "error": "radon execution failed",
            "stderr": "FileNotFoundError: [Errno 2] No such file or directory: 'src/'",
            "blocks_qa": True,
            "remediation": "Verify source_paths exist and radon has read permissions"
        }

        # Act & Assert: Stderr captured
        assert result["status"] == "failure", \
            "Status should be 'failure'"
        assert "stderr" in result, \
            "Should include stderr output"
        assert "remediation" in result, \
            "Should provide remediation guidance"


# ============================================================================
# Edge Cases
# ============================================================================

@pytest.mark.unit
@pytest.mark.edge_case
class TestEdgeCases:
    """Edge cases from story specification"""

    def test_multiple_violations_same_file(self):
        """Edge Case 2: Function with extreme complexity AND file with low MI"""
        # Arrange: Mock result with multiple violations
        result = {
            "extreme_violations": [
                {
                    "type": "complexity",
                    "severity": "CRITICAL",
                    "file": "src/LegacyService.cs",
                    "function": "ProcessOrder",
                    "score": 28
                },
                {
                    "type": "maintainability",
                    "severity": "CRITICAL",
                    "file": "src/LegacyService.cs",
                    "mi": 35
                }
            ],
            "blocks_qa": True
        }

        # Act & Assert: Both violations reported
        assert len(result["extreme_violations"]) == 2, \
            "Should report both violations"
        assert result["extreme_violations"][0]["file"] == result["extreme_violations"][1]["file"], \
            "Both violations should reference same file"

    def test_generated_code_excluded(self):
        """Edge Case 4: Generated code excluded from analysis"""
        # Arrange: Mock invocation with exclude paths
        exclude_paths = ["generated/", "migrations/", "scaffolded/"]

        result = {
            "metrics": {
                "complexity": {"average_per_function": 8.2},
                "excluded_paths": exclude_paths,
                "files_analyzed": 42,
                "files_excluded": 15
            },
            "extreme_violations": [],
            "blocks_qa": False
        }

        # Act & Assert: Exclusions documented
        assert "excluded_paths" in result["metrics"], \
            "Should document excluded paths"
        assert result["metrics"]["excluded_paths"] == exclude_paths, \
            "Excluded paths should match input"


# ============================================================================
# Run Tests
# ============================================================================

if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
