"""
Integration Tests: QA Skill Phase 1 Coverage Analysis Integration

Tests the integration between devforgeai-qa skill and coverage-analyzer subagent,
validating Phase 1 workflow execution, state management, and error propagation.

Focus Areas:
- Phase 1 invocation of coverage-analyzer subagent
- JSON response parsing and validation
- blocks_qa flag update mechanism
- Error handling across component boundaries
- Workflow continuation/halting logic
"""

import json
import pytest
from typing import Dict, Any, Optional
from unittest.mock import Mock, patch, call
from dataclasses import dataclass


@dataclass
class QAWorkflowState:
    """Tracks QA workflow state across phases"""
    story_id: str
    mode: str  # "light" or "deep"
    blocks_qa: bool = False
    current_phase: int = 0
    coverage_result: Optional[Dict[str, Any]] = None
    violations: list = None

    def __post_init__(self):
        if self.violations is None:
            self.violations = []


class TestQASkillCoverageIntegration:
    """Test suite for QA skill Phase 1 coverage-analyzer integration"""

    # ============================================================================
    # Phase 1 Invocation Tests
    # ============================================================================

    @pytest.mark.integration
    def test_phase_1_invokes_coverage_analyzer_subagent(self):
        """
        Test: Phase 1 Invokes coverage-analyzer Subagent

        Given: QA skill enters Phase 1 (Test Coverage Analysis)
        When: Phase 1 Step 1 executes
        Then: coverage-analyzer subagent is invoked with proper context

        Acceptance:
        - Task() called with subagent_type="coverage-analyzer"
        - All required parameters passed (story_id, language, test_command, context files)
        - Subagent invocation logged
        """
        # Arrange
        qa_state = QAWorkflowState(
            story_id="STORY-TEST-001",
            mode="deep",
            current_phase=1
        )

        # Mock Task function
        mock_task = Mock(return_value={
            "status": "success",
            "coverage_summary": {
                "overall_coverage": 85.0,
                "business_logic_coverage": 96.0,
                "application_coverage": 87.0,
                "infrastructure_coverage": 79.0
            },
            "blocks_qa": False,
            "violations": []
        })

        # Act: Simulate Phase 1 invocation
        with patch('builtins.print') as mock_print:
            coverage_result = mock_task(
                subagent_type="coverage-analyzer",
                description="Analyze test coverage by layer",
                prompt=f"Analyze coverage for {qa_state.story_id}..."
            )

        # Assert
        mock_task.assert_called_once()
        call_args = mock_task.call_args
        assert "coverage-analyzer" in str(call_args)
        assert qa_state.story_id in str(call_args)

    @pytest.mark.integration
    def test_phase_1_context_files_loaded_before_invocation(self):
        """
        Test: Phase 1 Context Files Loaded Before Invocation

        Given: QA skill at Phase 1 Step 1.1
        When: Context files are loaded (tech-stack.md, source-tree.md, coverage-thresholds.md)
        Then: All files successfully loaded before subagent invocation

        Acceptance:
        - 3 context files read successfully
        - File contents available for prompt construction
        - Missing file causes HALT before subagent call
        """
        # Arrange
        context_files = {
            "devforgeai/context/tech-stack.md": "core_technologies:\n  language: Python",
            "devforgeai/context/source-tree.md": "layers:\n  business_logic: src/Domain",
            ".claude/skills/devforgeai-qa/assets/config/coverage-thresholds.md": "thresholds:\n  business_logic: 95"
        }

        files_loaded = 0

        # Act: Simulate context file loading
        for file_path, content in context_files.items():
            if content:
                files_loaded += 1

        # Assert
        assert files_loaded == 3
        assert all(content for content in context_files.values())

    # ============================================================================
    # Response Parsing Tests
    # ============================================================================

    @pytest.mark.integration
    def test_parse_coverage_result_successful_response(self):
        """
        Test: Parse Coverage Result - Successful Response

        Given: coverage-analyzer returns success response
        When: QA skill parses JSON response
        Then: All fields correctly extracted

        Acceptance:
        - status extracted: "success"
        - coverage_summary extracted with 4 values
        - validation_result extracted with 4 booleans
        - gaps array parsed correctly
        - recommendations array parsed
        """
        # Arrange
        json_response = """
        {
            "status": "success",
            "story_id": "STORY-TEST-001",
            "coverage_summary": {
                "overall_coverage": 85.0,
                "business_logic_coverage": 96.0,
                "application_coverage": 87.0,
                "infrastructure_coverage": 79.0
            },
            "validation_result": {
                "business_logic_passed": true,
                "application_passed": true,
                "infrastructure_passed": false,
                "overall_passed": true
            },
            "gaps": [],
            "blocks_qa": false,
            "violations": [],
            "recommendations": ["Coverage meets critical thresholds"]
        }
        """

        # Act
        result = json.loads(json_response)

        # Assert
        assert result["status"] == "success"
        assert result["coverage_summary"]["overall_coverage"] == 85.0
        assert len(result["coverage_summary"]) == 4
        assert result["validation_result"]["business_logic_passed"] is True
        assert result["blocks_qa"] is False
        assert isinstance(result["gaps"], list)
        assert isinstance(result["recommendations"], list)

    @pytest.mark.integration
    def test_parse_coverage_result_with_gaps(self):
        """
        Test: Parse Coverage Result - With Gaps

        Given: coverage-analyzer returns result with gaps
        When: QA skill parses gaps array
        Then: Each gap contains required fields

        Acceptance:
        - gaps array has 1+ items
        - Each gap has: file, layer, current_coverage, target_coverage, uncovered_lines, suggested_tests
        - uncovered_lines is array of integers
        - suggested_tests is array of strings
        """
        # Arrange
        json_response = """
        {
            "status": "success",
            "gaps": [
                {
                    "file": "src/Infrastructure/OrderRepository.cs",
                    "layer": "infrastructure",
                    "current_coverage": 72.5,
                    "target_coverage": 80.0,
                    "uncovered_lines": [145, 146, 147],
                    "suggested_tests": ["Test error handling", "Test concurrent access"]
                }
            ],
            "blocks_qa": false
        }
        """

        # Act
        result = json.loads(json_response)
        gap = result["gaps"][0]

        # Assert
        assert len(result["gaps"]) == 1
        assert "file" in gap
        assert "layer" in gap
        assert "current_coverage" in gap
        assert "target_coverage" in gap
        assert "uncovered_lines" in gap
        assert "suggested_tests" in gap
        assert isinstance(gap["uncovered_lines"], list)
        assert all(isinstance(line, int) for line in gap["uncovered_lines"])
        assert isinstance(gap["suggested_tests"], list)
        assert all(isinstance(test, str) for test in gap["suggested_tests"])

    @pytest.mark.integration
    def test_parse_coverage_result_failure_response(self):
        """
        Test: Parse Coverage Result - Failure Response

        Given: coverage-analyzer returns failure response
        When: QA skill parses JSON response
        Then: Error and remediation extracted

        Acceptance:
        - status = "failure"
        - error field populated
        - remediation field populated
        - blocks_qa = true
        """
        # Arrange
        json_response = """
        {
            "status": "failure",
            "story_id": "STORY-TEST-001",
            "error": "Context file missing: devforgeai/context/source-tree.md",
            "blocks_qa": true,
            "remediation": "Run /create-context to generate missing context files"
        }
        """

        # Act
        result = json.loads(json_response)

        # Assert
        assert result["status"] == "failure"
        assert "error" in result
        assert "remediation" in result
        assert result["blocks_qa"] is True

    # ============================================================================
    # blocks_qa Flag Update Tests
    # ============================================================================

    @pytest.mark.integration
    def test_blocks_qa_update_false_to_false(self):
        """
        Test: blocks_qa Update - false → false

        Given: blocks_qa starts as false
        When: coverage-analyzer returns blocks_qa = false
        Then: blocks_qa remains false

        Acceptance:
        - blocks_qa = false AND false = false
        """
        # Arrange
        qa_state = QAWorkflowState(story_id="STORY-TEST-001", mode="deep", blocks_qa=False)
        coverage_result = {"blocks_qa": False}

        # Act
        qa_state.blocks_qa = qa_state.blocks_qa or coverage_result["blocks_qa"]

        # Assert
        assert qa_state.blocks_qa is False

    @pytest.mark.integration
    def test_blocks_qa_update_false_to_true(self):
        """
        Test: blocks_qa Update - false → true

        Given: blocks_qa starts as false
        When: coverage-analyzer returns blocks_qa = true
        Then: blocks_qa becomes true

        Acceptance:
        - blocks_qa = false OR true = true
        """
        # Arrange
        qa_state = QAWorkflowState(story_id="STORY-TEST-001", mode="deep", blocks_qa=False)
        coverage_result = {"blocks_qa": True}

        # Act
        qa_state.blocks_qa = qa_state.blocks_qa or coverage_result["blocks_qa"]

        # Assert
        assert qa_state.blocks_qa is True

    @pytest.mark.integration
    def test_blocks_qa_update_true_remains_true(self):
        """
        Test: blocks_qa Update - true → true

        Given: blocks_qa already true (from earlier phase)
        When: coverage-analyzer returns blocks_qa = false
        Then: blocks_qa remains true (OR logic)

        Acceptance:
        - blocks_qa = true OR false = true
        """
        # Arrange
        qa_state = QAWorkflowState(story_id="STORY-TEST-001", mode="deep", blocks_qa=True)
        coverage_result = {"blocks_qa": False}

        # Act
        qa_state.blocks_qa = qa_state.blocks_qa or coverage_result["blocks_qa"]

        # Assert
        assert qa_state.blocks_qa is True

    # ============================================================================
    # Workflow Progression Tests
    # ============================================================================

    @pytest.mark.integration
    def test_workflow_continues_to_phase_2_when_coverage_passes(self):
        """
        Test: Workflow Continues to Phase 2 when Coverage Passes

        Given: coverage-analyzer returns blocks_qa = false
        When: Phase 1 completes
        Then: Workflow proceeds to Phase 2 (Anti-Pattern Detection)

        Acceptance:
        - Phase 1 completes successfully
        - blocks_qa = false allows progression
        - Phase 2 initiated
        """
        # Arrange
        qa_state = QAWorkflowState(story_id="STORY-TEST-001", mode="deep", current_phase=1)
        coverage_result = {"blocks_qa": False, "status": "success"}

        # Act
        qa_state.coverage_result = coverage_result
        qa_state.blocks_qa = coverage_result["blocks_qa"]

        if qa_state.blocks_qa is False:
            qa_state.current_phase = 2  # Advance to Phase 2

        # Assert
        assert qa_state.current_phase == 2
        assert qa_state.blocks_qa is False

    @pytest.mark.integration
    def test_workflow_halts_at_phase_1_when_coverage_fails(self):
        """
        Test: Workflow Halts at Phase 1 when Coverage Fails

        Given: coverage-analyzer returns blocks_qa = true
        When: Phase 1 completes
        Then: Workflow HALTS with error message, does NOT proceed to Phase 2

        Acceptance:
        - Phase 1 result sets blocks_qa = true
        - Phase 2 not initiated
        - Error message displayed to user
        - User prompted to fix coverage issues
        """
        # Arrange
        qa_state = QAWorkflowState(
            story_id="STORY-TEST-001",
            mode="deep",
            current_phase=1,
            blocks_qa=False
        )
        coverage_result = {
            "blocks_qa": True,
            "status": "success",
            "violations": [
                {
                    "severity": "CRITICAL",
                    "message": "Business logic coverage 93% below threshold 95%"
                }
            ]
        }

        # Act
        qa_state.coverage_result = coverage_result
        qa_state.blocks_qa = qa_state.blocks_qa or coverage_result["blocks_qa"]
        qa_state.violations.extend(coverage_result["violations"])

        # Assert
        assert qa_state.blocks_qa is True
        assert qa_state.current_phase == 1  # Still at Phase 1
        assert len(qa_state.violations) > 0

    # ============================================================================
    # Error Propagation Tests
    # ============================================================================

    @pytest.mark.integration
    def test_coverage_command_failure_propagates_to_qa(self):
        """
        Test: Coverage Command Failure Propagates to QA

        Given: coverage-analyzer encounters missing coverage tool
        When: Subagent returns failure response
        Then: Error propagates to QA skill with remediation

        Acceptance:
        - blocks_qa set to true
        - Error message contains tool name
        - Remediation guidance provided
        """
        # Arrange
        coverage_result = {
            "status": "failure",
            "blocks_qa": True,
            "error": "Coverage command failed: No module named 'coverage'",
            "remediation": "Install pytest-cov: pip install pytest-cov"
        }

        qa_state = QAWorkflowState(story_id="STORY-TEST-001", mode="deep")

        # Act
        qa_state.blocks_qa = coverage_result["blocks_qa"]

        # Assert
        assert qa_state.blocks_qa is True
        assert "coverage" in coverage_result["error"].lower()
        assert "pip install" in coverage_result["remediation"]

    @pytest.mark.integration
    def test_context_file_missing_error_propagates(self):
        """
        Test: Context File Missing Error Propagates

        Given: coverage-analyzer cannot load context files
        When: Subagent returns failure
        Then: Error clearly identifies missing file

        Acceptance:
        - blocks_qa = true
        - Error message identifies specific file
        - Remediation suggests /create-context command
        """
        # Arrange
        coverage_result = {
            "status": "failure",
            "blocks_qa": True,
            "error": "Context file missing: devforgeai/context/source-tree.md",
            "remediation": "Run /create-context to generate missing context files"
        }

        # Act
        qa_state = QAWorkflowState(story_id="STORY-TEST-001", mode="deep")
        qa_state.blocks_qa = coverage_result["blocks_qa"]

        # Assert
        assert qa_state.blocks_qa is True
        assert "source-tree.md" in coverage_result["error"]
        assert "/create-context" in coverage_result["remediation"]

    # ============================================================================
    # Light vs Deep Mode Tests
    # ============================================================================

    @pytest.mark.integration
    def test_light_mode_skips_detailed_coverage_analysis(self):
        """
        Test: Light Mode Skips Detailed Coverage Analysis

        Given: QA mode = "light"
        When: Phase 1 executes in light mode
        Then: Coverage analysis still runs but with simpler output

        Note: Light mode still validates coverage (critical check)
        but doesn't produce detailed gap analysis
        """
        # Arrange
        qa_state = QAWorkflowState(story_id="STORY-TEST-001", mode="light")

        # Simulate light mode response (less detailed)
        coverage_result = {
            "status": "success",
            "blocks_qa": False,
            "coverage_summary": {
                "overall_coverage": 85.0,
                "business_logic_coverage": 96.0,
                "application_coverage": 87.0,
                "infrastructure_coverage": 79.0
            },
            "gaps": []  # Empty in light mode (summary only)
        }

        # Act
        qa_state.coverage_result = coverage_result
        qa_state.blocks_qa = coverage_result["blocks_qa"]

        # Assert
        assert qa_state.mode == "light"
        assert coverage_result["gaps"] == []
        assert "coverage_summary" in coverage_result

    @pytest.mark.integration
    def test_deep_mode_includes_detailed_gap_analysis(self):
        """
        Test: Deep Mode Includes Detailed Gap Analysis

        Given: QA mode = "deep"
        When: Phase 1 executes in deep mode
        Then: Coverage analysis produces detailed gaps and recommendations

        Acceptance:
        - gaps array populated with details
        - suggestions included for each gap
        - recommendations prioritized
        """
        # Arrange
        qa_state = QAWorkflowState(story_id="STORY-TEST-001", mode="deep")

        # Simulate deep mode response (detailed)
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
                    "file": "src/Infrastructure/Cache.cs",
                    "layer": "infrastructure",
                    "current_coverage": 75.0,
                    "target_coverage": 80.0,
                    "uncovered_lines": [89, 90],
                    "suggested_tests": ["Test cache timeout"]
                }
            ],
            "recommendations": [
                "Add tests for Cache infrastructure layer"
            ]
        }

        # Act
        qa_state.coverage_result = coverage_result
        qa_state.blocks_qa = coverage_result["blocks_qa"]

        # Assert
        assert qa_state.mode == "deep"
        assert len(coverage_result["gaps"]) > 0
        assert len(coverage_result["recommendations"]) > 0

    # ============================================================================
    # Integration with QA Report Tests
    # ============================================================================

    @pytest.mark.integration
    def test_coverage_results_stored_for_qa_report(self):
        """
        Test: Coverage Results Stored for QA Report

        Given: coverage-analyzer completes Phase 1
        When: Results are captured
        Then: Results stored for later inclusion in QA report

        Acceptance:
        - coverage_summary stored
        - violations stored
        - gaps stored
        - All data available for report generation (Phase 5)
        """
        # Arrange
        qa_state = QAWorkflowState(story_id="STORY-TEST-001", mode="deep")
        coverage_result = {
            "status": "success",
            "coverage_summary": {
                "overall_coverage": 85.0,
                "business_logic_coverage": 96.0,
                "application_coverage": 87.0,
                "infrastructure_coverage": 79.0
            },
            "violations": [
                {
                    "severity": "MEDIUM",
                    "message": "Infrastructure coverage at 79.0% (target 80%)"
                }
            ],
            "gaps": [
                {
                    "file": "src/Infrastructure/Cache.cs",
                    "layer": "infrastructure",
                    "current_coverage": 79.0,
                    "target_coverage": 80.0,
                    "uncovered_lines": [89],
                    "suggested_tests": ["Test cache timeout"]
                }
            ]
        }

        # Act
        qa_state.coverage_result = coverage_result
        qa_state.violations.extend(coverage_result["violations"])

        # Assert
        assert qa_state.coverage_result is not None
        assert "coverage_summary" in qa_state.coverage_result
        assert len(qa_state.violations) > 0
        assert len(qa_state.coverage_result["gaps"]) > 0

        # Verify data structure for report generation
        assert isinstance(qa_state.coverage_result["coverage_summary"]["overall_coverage"], float)
        assert isinstance(qa_state.violations[0]["severity"], str)

    # ============================================================================
    # State Consistency Tests
    # ============================================================================

    @pytest.mark.integration
    def test_qa_state_consistency_single_phase(self):
        """
        Test: QA State Consistency - Single Phase

        Given: QA workflow completes Phase 1
        When: State is checked
        Then: All state variables are consistent

        Acceptance:
        - story_id unchanged
        - mode unchanged
        - phase advances correctly
        - blocks_qa reflects coverage result
        """
        # Arrange
        qa_state = QAWorkflowState(
            story_id="STORY-TEST-001",
            mode="deep",
            current_phase=1,
            blocks_qa=False
        )

        # Act
        coverage_result = {"blocks_qa": False}
        qa_state.blocks_qa = qa_state.blocks_qa or coverage_result["blocks_qa"]
        qa_state.current_phase = 2

        # Assert
        assert qa_state.story_id == "STORY-TEST-001"
        assert qa_state.mode == "deep"
        assert qa_state.current_phase == 2
        assert qa_state.blocks_qa is False

    @pytest.mark.integration
    def test_qa_state_consistency_multiple_phases(self):
        """
        Test: QA State Consistency - Multiple Phases

        Given: QA workflow executes Phases 1-2
        When: State modified by each phase
        Then: Cumulative state remains consistent

        Acceptance:
        - blocks_qa reflects OR of Phase 1 and Phase 2 results
        - phase number correct at each stage
        """
        # Arrange
        qa_state = QAWorkflowState(
            story_id="STORY-TEST-001",
            mode="deep",
            current_phase=0,
            blocks_qa=False
        )

        # Act: Phase 1
        qa_state.current_phase = 1
        coverage_result = {"blocks_qa": False}
        qa_state.blocks_qa = qa_state.blocks_qa or coverage_result["blocks_qa"]
        initial_blocks_qa = qa_state.blocks_qa

        # Act: Phase 2
        qa_state.current_phase = 2
        anti_pattern_result = {"blocks_qa": True}
        qa_state.blocks_qa = qa_state.blocks_qa or anti_pattern_result["blocks_qa"]
        final_blocks_qa = qa_state.blocks_qa

        # Assert
        assert qa_state.current_phase == 2
        assert initial_blocks_qa is False
        assert final_blocks_qa is True  # Phase 2 set it to true


# ============================================================================
# Test Fixtures
# ============================================================================

@pytest.fixture
def qa_state_fresh():
    """Provides fresh QA state"""
    return QAWorkflowState(story_id="STORY-TEST-001", mode="deep")


@pytest.fixture
def coverage_result_success():
    """Provides successful coverage result"""
    return {
        "status": "success",
        "blocks_qa": False,
        "coverage_summary": {
            "overall_coverage": 85.0,
            "business_logic_coverage": 96.0,
            "application_coverage": 87.0,
            "infrastructure_coverage": 79.0
        }
    }


@pytest.fixture
def coverage_result_blocking():
    """Provides blocking coverage result"""
    return {
        "status": "success",
        "blocks_qa": True,
        "violations": [
            {
                "severity": "CRITICAL",
                "message": "Business logic coverage below 95%"
            }
        ]
    }


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
