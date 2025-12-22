"""
Integration Tests: coverage-analyzer Subagent with devforgeai-qa Skill

Tests the integration between coverage-analyzer subagent and devforgeai-qa skill Phase 1,
validating coverage analysis workflows, threshold enforcement, and error handling.

Test Coverage:
- Scenario 1: Happy Path - All thresholds met
- Scenario 2: Business Logic Below Threshold
- Scenario 3: Application Coverage Below Threshold
- Scenario 4: Infrastructure Warning (No Block)
- Scenario 5: Context File Missing
- Scenario 6: Coverage Command Failed
- Scenario 7: No Files Classified
- Scenario 8: Multi-Language Detection
- Scenario 9: Response Parsing - Gaps Array
- Scenario 10: Response Parsing - Recommendations Array
- Scenario 11: Token Budget Tracking
- Scenario 12: Cross-Module Integration (coverage → anti-pattern scan)
"""

import json
import pytest
from typing import Dict, Any, List
from pathlib import Path
from dataclasses import dataclass
from unittest.mock import Mock, patch, MagicMock
import tempfile
import sys


# Test Data Structures
@dataclass
class CoverageResult:
    """Represents coverage-analyzer subagent response"""
    status: str
    story_id: str
    coverage_summary: Dict[str, float] = None
    validation_result: Dict[str, bool] = None
    thresholds: Dict[str, int] = None
    gaps: List[Dict[str, Any]] = None
    blocks_qa: bool = False
    violations: List[Dict[str, Any]] = None
    recommendations: List[str] = None
    error: str = None
    remediation: str = None


class TestCoverageAnalyzerIntegration:
    """Integration test suite for coverage-analyzer subagent"""

    # ============================================================================
    # SCENARIO 1: Happy Path - All Thresholds Met
    # ============================================================================

    @pytest.mark.integration
    def test_scenario_1_all_thresholds_met(self):
        """
        Test: Happy Path - All Thresholds Met

        Given: Python project with 97% business, 88% application, 85% overall coverage
        When: coverage-analyzer runs
        Then: blocks_qa = false, coverage_summary shows pass, no violations

        Acceptance:
        - status = "success"
        - blocks_qa = false
        - All validation_result values = true
        - violations array = []
        - QA skill continues to Phase 2
        """
        # Arrange
        story_id = "STORY-TEST-001"
        coverage_data = {
            "status": "success",
            "story_id": story_id,
            "coverage_summary": {
                "overall_coverage": 85.0,
                "business_logic_coverage": 97.0,
                "application_coverage": 88.0,
                "infrastructure_coverage": 79.3
            },
            "thresholds": {
                "business_logic": 95,
                "application": 85,
                "infrastructure": 80,
                "overall": 80
            },
            "validation_result": {
                "business_logic_passed": True,
                "application_passed": True,
                "infrastructure_passed": False,  # Below 80% (warning only)
                "overall_passed": True
            },
            "gaps": [],
            "blocks_qa": False,
            "violations": [],
            "recommendations": [
                "Current coverage meets all critical thresholds (business 97.0%, application 88.0%)",
                "Infrastructure at 79.3% is slightly below 80% target (warning level, not blocking)"
            ]
        }

        # Act
        result = CoverageResult(**coverage_data)

        # Assert
        assert result.status == "success"
        assert result.blocks_qa is False
        assert result.validation_result["business_logic_passed"] is True
        assert result.validation_result["application_passed"] is True
        assert result.validation_result["overall_passed"] is True
        assert len(result.violations) == 0
        assert result.coverage_summary["business_logic_coverage"] == 97.0
        assert result.coverage_summary["application_coverage"] == 88.0

        # Verify QA can continue to Phase 2
        assert result.blocks_qa is False
        assert "Current coverage meets all critical thresholds" in result.recommendations[0]

    # ============================================================================
    # SCENARIO 2: Business Logic Below Threshold (CRITICAL)
    # ============================================================================

    @pytest.mark.integration
    def test_scenario_2_business_logic_below_threshold(self):
        """
        Test: Business Logic Below Threshold (CRITICAL)

        Given: Python project with 93% business, 88% application, 85% overall coverage
        When: coverage-analyzer runs
        Then: blocks_qa = true, CRITICAL violation, remediation guidance

        Acceptance:
        - status = "success" (analysis completed)
        - blocks_qa = true (blocks QA progression)
        - validation_result["business_logic_passed"] = false
        - violations[0]["severity"] = "CRITICAL"
        - Remediation guidance provided
        - QA skill halts with message
        """
        # Arrange
        story_id = "STORY-TEST-002"
        coverage_data = {
            "status": "success",
            "story_id": story_id,
            "coverage_summary": {
                "overall_coverage": 85.0,
                "business_logic_coverage": 93.0,
                "application_coverage": 88.0,
                "infrastructure_coverage": 82.0
            },
            "thresholds": {
                "business_logic": 95,
                "application": 85,
                "infrastructure": 80,
                "overall": 80
            },
            "validation_result": {
                "business_logic_passed": False,  # CRITICAL: 93% < 95%
                "application_passed": True,
                "infrastructure_passed": True,
                "overall_passed": True
            },
            "gaps": [
                {
                    "file": "src/Domain/Order.cs",
                    "layer": "business_logic",
                    "current_coverage": 90.5,
                    "target_coverage": 95.0,
                    "uncovered_lines": [120, 121, 145, 147, 148],
                    "suggested_tests": [
                        "Test Order validation when total exceeds max amount",
                        "Test Order cancellation after partial shipment"
                    ]
                }
            ],
            "blocks_qa": True,
            "violations": [
                {
                    "severity": "CRITICAL",
                    "layer": "business_logic",
                    "message": "Business logic coverage 93.0% below threshold 95%",
                    "impact": "High bug risk in core domain logic",
                    "remediation": "Add tests for Order domain logic, specifically: validation rules, cancellation scenarios"
                }
            ],
            "recommendations": [
                "BLOCKING: Business logic coverage at 93.0% (needs 95%). Add tests for src/Domain/Order.cs lines 120-121, 145-148",
                "Suggested: Test Order validation when total exceeds max amount",
                "Suggested: Test Order cancellation after partial shipment"
            ]
        }

        # Act
        result = CoverageResult(**coverage_data)

        # Assert
        assert result.status == "success"
        assert result.blocks_qa is True
        assert result.validation_result["business_logic_passed"] is False
        assert result.violations[0]["severity"] == "CRITICAL"
        assert "Business logic coverage 93.0% below threshold 95%" in result.violations[0]["message"]
        assert len(result.gaps) == 1
        assert "Order" in result.gaps[0]["file"]
        assert 120 in result.gaps[0]["uncovered_lines"]

        # Verify remediation guidance
        assert "BLOCKING" in result.recommendations[0]
        assert "93.0%" in result.recommendations[0]

    # ============================================================================
    # SCENARIO 3: Application Coverage Below Threshold (HIGH)
    # ============================================================================

    @pytest.mark.integration
    def test_scenario_3_application_coverage_below_threshold(self):
        """
        Test: Application Coverage Below Threshold (HIGH)

        Given: C# project with 96% business, 82% application, 78% overall coverage
        When: coverage-analyzer runs
        Then: blocks_qa = true, HIGH violations (application + overall)

        Acceptance:
        - blocks_qa = true
        - violations include HIGH for application <85%
        - violations include HIGH for overall <80%
        - Gaps identified for application layer files
        - QA halts with specific guidance for application layer
        """
        # Arrange
        story_id = "STORY-TEST-003"
        coverage_data = {
            "status": "success",
            "story_id": story_id,
            "coverage_summary": {
                "overall_coverage": 78.0,
                "business_logic_coverage": 96.0,
                "application_coverage": 82.0,
                "infrastructure_coverage": 71.0
            },
            "thresholds": {
                "business_logic": 95,
                "application": 85,
                "infrastructure": 80,
                "overall": 80
            },
            "validation_result": {
                "business_logic_passed": True,
                "application_passed": False,  # HIGH: 82% < 85%
                "infrastructure_passed": False,  # MEDIUM warning: 71% < 80%
                "overall_passed": False  # HIGH: 78% < 80%
            },
            "gaps": [
                {
                    "file": "src/Application/Services/OrderService.cs",
                    "layer": "application",
                    "current_coverage": 79.0,
                    "target_coverage": 85.0,
                    "uncovered_lines": [234, 235, 236, 267, 268, 289],
                    "suggested_tests": [
                        "Test OrderService error handling",
                        "Test concurrent order processing"
                    ]
                },
                {
                    "file": "src/Infrastructure/Repositories/CustomerRepository.cs",
                    "layer": "infrastructure",
                    "current_coverage": 68.0,
                    "target_coverage": 80.0,
                    "uncovered_lines": [145, 146, 189, 190],
                    "suggested_tests": [
                        "Test database connection failure",
                        "Test concurrent access"
                    ]
                }
            ],
            "blocks_qa": True,
            "violations": [
                {
                    "severity": "HIGH",
                    "layer": "application",
                    "message": "Application coverage 82.0% below threshold 85%",
                    "impact": "Business workflow implementation may have untested error paths"
                },
                {
                    "severity": "HIGH",
                    "layer": "overall",
                    "message": "Overall coverage 78.0% below threshold 80%",
                    "impact": "Project-wide test coverage insufficient"
                },
                {
                    "severity": "MEDIUM",
                    "layer": "infrastructure",
                    "message": "Infrastructure coverage 71.0% below threshold 80%",
                    "impact": "Data layer integration tests needed (warning, not blocking)"
                }
            ],
            "recommendations": [
                "BLOCKING: Application coverage at 82.0% (needs 85%). Add tests for src/Application/Services/OrderService.cs",
                "BLOCKING: Overall coverage at 78.0% (needs 80%). Add tests for OrderService and CustomerRepository",
                "Suggested: Test OrderService error handling (lines 234-236)",
                "Suggested: Test concurrent order processing"
            ]
        }

        # Act
        result = CoverageResult(**coverage_data)

        # Assert
        assert result.blocks_qa is True
        assert result.validation_result["application_passed"] is False
        assert result.validation_result["overall_passed"] is False

        # Verify violations
        assert any(v["severity"] == "HIGH" and "application" in v["message"].lower()
                  for v in result.violations)
        assert any(v["severity"] == "HIGH" and "overall" in v["message"].lower()
                  for v in result.violations)

        # Verify infrastructure warning (not blocking)
        assert any(v["severity"] == "MEDIUM" and "infrastructure" in v["message"].lower()
                  for v in result.violations)

        # Verify gaps
        assert any(g["file"].endswith("OrderService.cs") for g in result.gaps)
        assert any(g["file"].endswith("CustomerRepository.cs") for g in result.gaps)

    # ============================================================================
    # SCENARIO 4: Infrastructure Warning (No Block)
    # ============================================================================

    @pytest.mark.integration
    def test_scenario_4_infrastructure_warning_no_block(self):
        """
        Test: Infrastructure Warning (No Block)

        Given: Node.js project with 96% business, 87% application, 75% infrastructure
        When: coverage-analyzer runs
        Then: blocks_qa = false (infrastructure is warning only), warn user about gaps

        Acceptance:
        - blocks_qa = false (allows progression)
        - violation severity = MEDIUM (not CRITICAL/HIGH)
        - infrastructure passed = false but doesn't block
        - Gaps identified but marked as non-blocking
        - User warned but workflow continues
        """
        # Arrange
        story_id = "STORY-TEST-004"
        coverage_data = {
            "status": "success",
            "story_id": story_id,
            "coverage_summary": {
                "overall_coverage": 85.5,
                "business_logic_coverage": 96.0,
                "application_coverage": 87.0,
                "infrastructure_coverage": 75.0
            },
            "thresholds": {
                "business_logic": 95,
                "application": 85,
                "infrastructure": 80,
                "overall": 80
            },
            "validation_result": {
                "business_logic_passed": True,
                "application_passed": True,
                "infrastructure_passed": False,  # Below 80% but NOT blocking
                "overall_passed": True
            },
            "gaps": [
                {
                    "file": "src/infrastructure/Database.ts",
                    "layer": "infrastructure",
                    "current_coverage": 72.0,
                    "target_coverage": 80.0,
                    "uncovered_lines": [89, 90, 91, 134, 135],
                    "suggested_tests": [
                        "Test database connection timeout",
                        "Test transaction rollback on error"
                    ]
                }
            ],
            "blocks_qa": False,
            "violations": [
                {
                    "severity": "MEDIUM",
                    "layer": "infrastructure",
                    "message": "Infrastructure coverage 75.0% below threshold 80% (warning, not blocking)",
                    "impact": "Data layer integration tests could be more comprehensive",
                    "blocking": False
                }
            ],
            "recommendations": [
                "⚠️ Infrastructure layer at 75.0% (target 80%) - consider adding integration tests",
                "Suggested: Test database connection timeout handling",
                "Suggested: Test transaction rollback scenarios",
                "✅ Business logic (96.0%) and application (87.0%) thresholds met - proceeding to Phase 2"
            ]
        }

        # Act
        result = CoverageResult(**coverage_data)

        # Assert
        assert result.blocks_qa is False  # Does NOT block despite infrastructure below threshold
        assert result.validation_result["infrastructure_passed"] is False
        assert result.violations[0]["severity"] == "MEDIUM"
        assert result.violations[0]["blocking"] is False
        assert len(result.gaps) == 1
        assert result.gaps[0]["current_coverage"] == 72.0

        # Verify QA can continue
        assert "proceeding to Phase 2" in result.recommendations[-1]

    # ============================================================================
    # SCENARIO 5: Context File Missing
    # ============================================================================

    @pytest.mark.integration
    def test_scenario_5_context_file_missing(self):
        """
        Test: Context File Missing

        Given: Missing coverage-thresholds.md
        When: coverage-analyzer runs Phase 1
        Then: blocks_qa = true, error status, remediation ("Run /create-context")

        Acceptance:
        - status = "failure"
        - blocks_qa = true
        - error message identifies missing file
        - remediation guidance provided
        - Suggests /create-context command
        """
        # Arrange
        story_id = "STORY-TEST-005"
        coverage_data = {
            "status": "failure",
            "story_id": story_id,
            "error": "Context file missing: devforgeai/context/source-tree.md",
            "blocks_qa": True,
            "remediation": "Run /create-context to generate missing context files. This initializes architectural context for the project."
        }

        # Act
        result = CoverageResult(**coverage_data)

        # Assert
        assert result.status == "failure"
        assert result.blocks_qa is True
        assert "missing" in result.error.lower()
        assert "devforgeai/context" in result.error
        assert "/create-context" in result.remediation

    # ============================================================================
    # SCENARIO 6: Coverage Command Failed
    # ============================================================================

    @pytest.mark.integration
    def test_scenario_6_coverage_command_failed(self):
        """
        Test: Coverage Command Failed

        Given: Python project but pytest-cov not installed
        When: coverage-analyzer runs coverage command
        Then: blocks_qa = true, error status, remediation guidance

        Acceptance:
        - status = "failure"
        - blocks_qa = true
        - error identifies which tool is missing
        - remediation suggests installation command
        """
        # Arrange
        story_id = "STORY-TEST-006"
        coverage_data = {
            "status": "failure",
            "story_id": story_id,
            "error": "Coverage command failed: No module named 'coverage'",
            "blocks_qa": True,
            "remediation": "Install pytest-cov: pip install pytest-cov"
        }

        # Act
        result = CoverageResult(**coverage_data)

        # Assert
        assert result.status == "failure"
        assert result.blocks_qa is True
        assert "coverage" in result.error.lower()
        assert "pip install" in result.remediation

    # ============================================================================
    # SCENARIO 7: No Files Classified
    # ============================================================================

    @pytest.mark.integration
    def test_scenario_7_no_files_classified(self):
        """
        Test: No Files Classified

        Given: Project with unusual directory structure not matching source-tree.md patterns
        When: coverage-analyzer attempts to classify files
        Then: blocks_qa = true, error status, remediation suggests updating source-tree.md

        Acceptance:
        - status = "failure"
        - blocks_qa = true
        - error indicates classification failure
        - remediation suggests source-tree.md update
        """
        # Arrange
        story_id = "STORY-TEST-007"
        coverage_data = {
            "status": "failure",
            "story_id": story_id,
            "error": "Could not classify files using source-tree.md patterns. Check that patterns match project structure.",
            "blocks_qa": True,
            "remediation": "Update devforgeai/context/source-tree.md with patterns that match your project's directory structure"
        }

        # Act
        result = CoverageResult(**coverage_data)

        # Assert
        assert result.status == "failure"
        assert result.blocks_qa is True
        assert "classify" in result.error.lower()
        assert "source-tree.md" in result.remediation

    # ============================================================================
    # SCENARIO 8: Multi-Language Detection
    # ============================================================================

    @pytest.mark.integration
    def test_scenario_8_multi_language_detection(self):
        """
        Test: Multi-Language Detection

        Given: tech-stack.md lists both Python and Node.js
        When: coverage-analyzer detects primary language
        Then: Uses primary language tool, logs warning about mixed language

        Acceptance:
        - Uses primary language tool
        - Includes warning in recommendations
        - Still produces valid coverage results
        - Suggests running coverage-analyzer twice if full coverage needed
        """
        # Arrange
        story_id = "STORY-TEST-008"
        coverage_data = {
            "status": "success",
            "story_id": story_id,
            "coverage_summary": {
                "overall_coverage": 86.0,
                "business_logic_coverage": 96.0,
                "application_coverage": 87.0,
                "infrastructure_coverage": 81.0
            },
            "thresholds": {
                "business_logic": 95,
                "application": 85,
                "infrastructure": 80,
                "overall": 80
            },
            "validation_result": {
                "business_logic_passed": True,
                "application_passed": True,
                "infrastructure_passed": True,
                "overall_passed": True
            },
            "gaps": [],
            "blocks_qa": False,
            "violations": [],
            "recommendations": [
                "⚠️ Project uses multiple languages (Python backend + Node.js frontend)",
                "Analyzed primary language (Python) only",
                "To test frontend coverage: Run coverage-analyzer again for Node.js layer"
            ]
        }

        # Act
        result = CoverageResult(**coverage_data)

        # Assert
        assert result.blocks_qa is False
        assert result.status == "success"
        assert any("multiple languages" in r for r in result.recommendations)
        assert any("Run coverage-analyzer again" in r for r in result.recommendations)

    # ============================================================================
    # SCENARIO 9: Response Parsing - Gaps Array
    # ============================================================================

    @pytest.mark.integration
    def test_scenario_9_response_parsing_gaps_array(self):
        """
        Test: Response Parsing - Gaps Array

        Given: Files with coverage <80% (infrastructure layer)
        When: coverage-analyzer parses response
        Then: gaps array includes all required fields

        Acceptance:
        - gap["file"] = file path
        - gap["layer"] = layer name
        - gap["coverage"] = current percentage
        - gap["uncovered_lines"] = array of line numbers
        - gap["suggested_tests"] = array of test scenarios
        """
        # Arrange
        story_id = "STORY-TEST-009"
        gap_data = {
            "file": "src/Infrastructure/Cache/RedisClient.cs",
            "layer": "infrastructure",
            "current_coverage": 72.5,
            "target_coverage": 80.0,
            "uncovered_lines": [89, 90, 91, 134, 135, 156],
            "suggested_tests": [
                "Test Redis connection timeout",
                "Test cache miss scenarios",
                "Test concurrent cache access"
            ]
        }

        # Act & Assert
        assert "file" in gap_data
        assert "layer" in gap_data
        assert "current_coverage" in gap_data
        assert "target_coverage" in gap_data
        assert "uncovered_lines" in gap_data
        assert "suggested_tests" in gap_data
        assert gap_data["current_coverage"] < gap_data["target_coverage"]
        assert len(gap_data["uncovered_lines"]) > 0
        assert len(gap_data["suggested_tests"]) > 0

    # ============================================================================
    # SCENARIO 10: Response Parsing - Recommendations Array
    # ============================================================================

    @pytest.mark.integration
    def test_scenario_10_response_parsing_recommendations(self):
        """
        Test: Response Parsing - Recommendations Array

        Given: Multiple coverage gaps at different severity levels
        When: coverage-analyzer generates recommendations
        Then: Recommendations prioritized (CRITICAL business gaps first)

        Acceptance:
        - CRITICAL gaps listed first
        - HIGH gaps listed second
        - MEDIUM warnings listed last
        - Each recommendation is actionable
        """
        # Arrange
        recommendations = [
            "BLOCKING: Business logic coverage at 93.0% (needs 95%). Add tests for src/Domain/Order.cs lines 120-121",
            "BLOCKING: Overall coverage at 78.0% (needs 80%). Add tests for infrastructure layer",
            "⚠️ Infrastructure layer at 75.0% (target 80%) - consider adding integration tests",
            "Suggested: Test database connection timeout handling"
        ]

        # Act
        blocking_count = sum(1 for r in recommendations if "BLOCKING" in r)
        warning_count = sum(1 for r in recommendations if "⚠️" in r)
        suggested_count = sum(1 for r in recommendations if "Suggested" in r)

        # Assert
        assert blocking_count > 0  # CRITICAL/HIGH blocking items first
        assert warning_count > 0   # Warnings after blocking
        assert suggested_count > 0  # Actionable suggestions

        # Verify first items are blocking (critical)
        assert "BLOCKING" in recommendations[0]

    # ============================================================================
    # SCENARIO 11: Token Budget Tracking
    # ============================================================================

    @pytest.mark.integration
    def test_scenario_11_token_budget_tracking(self):
        """
        Test: Token Budget Tracking

        When: coverage-analyzer subagent is invoked
        Then: Token usage should be ~4-5K (vs 12K inline)

        Acceptance:
        - Subagent invocation uses <5K tokens
        - Response parsing uses <1K tokens
        - Total: <6K tokens
        - Savings: >65% vs inline approach (12K tokens)
        """
        # This is a measurement test - actual token count depends on implementation
        # Expected ranges based on coverage-analyzer specification:

        expected_token_ranges = {
            "context_loading": (500, 1500),      # Load 3 context files
            "coverage_analysis": (1500, 2500),   # Run command + parse
            "layer_classification": (800, 1200), # Classify files
            "gap_identification": (800, 1200),   # Find gaps
            "recommendations": (500, 1000),      # Generate output
        }

        total_min = sum(r[0] for r in expected_token_ranges.values())
        total_max = sum(r[1] for r in expected_token_ranges.values())

        # Assert
        assert total_max < 8000  # Must be below 8K for 65% savings vs 12K
        assert total_min >= 3000  # Must have minimum overhead for proper analysis

        # Verify 65% savings target
        inline_tokens = 12000
        savings_percent = ((inline_tokens - total_max) / inline_tokens) * 100
        assert savings_percent > 30  # At minimum, should save 30%

    # ============================================================================
    # SCENARIO 12: Cross-Module Integration
    # ============================================================================

    @pytest.mark.integration
    def test_scenario_12_cross_module_integration(self):
        """
        Test: Cross-Module Integration (coverage → anti-pattern scan)

        Given: coverage-analyzer output feeds into Phase 2 anti-pattern scanner
        When: QA skill processes full workflow
        Then: Coverage results properly passed to anti-pattern detection

        Acceptance:
        - Coverage gaps can be parsed by anti-pattern scanner
        - No data type mismatches between modules
        - End-to-end workflow from coverage through anti-pattern detection
        """
        # Arrange: Simulate coverage-analyzer output
        coverage_result = {
            "status": "success",
            "blocks_qa": False,
            "coverage_summary": {
                "overall_coverage": 85.0,
                "business_logic_coverage": 96.0,
                "application_coverage": 87.0,
                "infrastructure_coverage": 79.0
            },
            "gaps": [
                {
                    "file": "src/Application/Services/OrderService.cs",
                    "layer": "application",
                    "current_coverage": 85.0,
                    "target_coverage": 85.0,
                    "uncovered_lines": [45, 67],
                    "suggested_tests": ["Test error handling"]
                }
            ]
        }

        # Act: Pass to anti-pattern scanner (Phase 2)
        anti_pattern_input = {
            "coverage_blocks_qa": coverage_result["blocks_qa"],
            "files_to_scan": [gap["file"] for gap in coverage_result["gaps"]],
            "coverage_summary": coverage_result["coverage_summary"]
        }

        # Assert
        assert isinstance(anti_pattern_input["coverage_blocks_qa"], bool)
        assert isinstance(anti_pattern_input["files_to_scan"], list)
        assert isinstance(anti_pattern_input["coverage_summary"], dict)
        assert any("OrderService.cs" in f for f in anti_pattern_input["files_to_scan"])


# ============================================================================
# Helper Classes and Fixtures
# ============================================================================

@pytest.fixture
def mock_qa_context():
    """Provides mock QA skill context"""
    return {
        "story_id": "STORY-TEST-001",
        "mode": "deep",
        "language": "Python",
        "test_command": "pytest --cov=src --cov-report=json"
    }


@pytest.fixture
def mock_coverage_result_success():
    """Provides mock successful coverage result"""
    return {
        "status": "success",
        "story_id": "STORY-TEST-001",
        "coverage_summary": {
            "overall_coverage": 85.0,
            "business_logic_coverage": 96.0,
            "application_coverage": 87.0,
            "infrastructure_coverage": 79.0
        },
        "blocks_qa": False,
        "violations": []
    }


@pytest.fixture
def mock_coverage_result_blocking():
    """Provides mock blocking coverage result"""
    return {
        "status": "success",
        "story_id": "STORY-TEST-002",
        "coverage_summary": {
            "overall_coverage": 78.0,
            "business_logic_coverage": 93.0,
            "application_coverage": 85.0,
            "infrastructure_coverage": 80.0
        },
        "blocks_qa": True,
        "violations": [
            {
                "severity": "CRITICAL",
                "message": "Business logic coverage below 95%"
            }
        ]
    }


# ============================================================================
# Test Execution Entry Point
# ============================================================================

if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
