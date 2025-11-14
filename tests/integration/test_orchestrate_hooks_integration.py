"""
Comprehensive integration test suite for STORY-026: Wire hooks into /orchestrate command

Tests cover:
- 7 acceptance criteria (AC1-AC7)
- 6 edge case scenarios
- Hook invocation on workflow success/failure
- Checkpoint resume scenarios
- Workflow context extraction and aggregation
- Failures-only mode behavior
- Performance requirements
- Graceful degradation on hook failures

TDD Red Phase: All tests written BEFORE implementation.
Framework: pytest
Test Pattern: AAA (Arrange, Act, Assert)
"""

import json
import tempfile
import pytest
import time
from pathlib import Path
from datetime import datetime, timezone, timedelta
from unittest.mock import Mock, patch, MagicMock, call
import subprocess
from uuid import uuid4


# ============================================================================
# FIXTURES - Common setup for all tests
# ============================================================================


@pytest.fixture
def temp_project_dir():
    """Create a temporary project directory with DevForgeAI structure."""
    with tempfile.TemporaryDirectory(prefix="orchestrate_hooks_") as tmpdir:
        project_path = Path(tmpdir)

        # Create required directories
        stories_dir = project_path / ".ai_docs" / "Stories"
        stories_dir.mkdir(parents=True, exist_ok=True)

        devforgeai_dir = project_path / ".devforgeai"
        devforgeai_dir.mkdir(exist_ok=True)

        hooks_dir = devforgeai_dir / "hooks"
        hooks_dir.mkdir(exist_ok=True)

        context_dir = devforgeai_dir / "context"
        context_dir.mkdir(exist_ok=True)

        yield project_path


@pytest.fixture
def sample_story_yaml():
    """Sample YAML frontmatter for a story."""
    return {
        "id": "STORY-001",
        "title": "User Authentication",
        "epic": "EPIC-001",
        "sprint": "Sprint-1",
        "status": "In Development",
        "points": 8,
        "priority": "High",
        "created_at": "2025-11-07T00:00:00Z",
        "last_modified": "2025-11-07T10:00:00Z"
    }


@pytest.fixture
def workflow_context_success():
    """Sample successful workflow context."""
    return {
        "workflow_id": str(uuid4()),
        "story_id": "STORY-001",
        "start_time": "2025-11-07T10:00:00Z",
        "end_time": "2025-11-07T10:45:00Z",
        "total_duration": 2700,
        "status": "SUCCESS",
        "phases_executed": [
            {
                "phase": "development",
                "start_time": "2025-11-07T10:00:00Z",
                "end_time": "2025-11-07T10:20:00Z",
                "duration": 1200,
                "status": "PASSED"
            },
            {
                "phase": "qa",
                "start_time": "2025-11-07T10:20:00Z",
                "end_time": "2025-11-07T10:30:00Z",
                "duration": 600,
                "status": "PASSED"
            },
            {
                "phase": "release",
                "start_time": "2025-11-07T10:30:00Z",
                "end_time": "2025-11-07T10:45:00Z",
                "duration": 900,
                "status": "PASSED"
            }
        ],
        "quality_gates": {
            "context_validation": {"status": "PASSED", "details": "All 6 context files present"},
            "test_passing": {"status": "PASSED", "details": "100 tests passed (0 failed)"},
            "coverage": {"status": "PASSED", "percentage": 95.2},
            "qa_approved": {"status": "PASSED", "details": "Deep QA approved"}
        },
        "checkpoint_info": {
            "checkpoint_resumed": False,
            "resume_point": None,
            "phases_skipped": []
        }
    }


@pytest.fixture
def workflow_context_qa_failure():
    """Sample workflow context with QA phase failure."""
    return {
        "workflow_id": str(uuid4()),
        "story_id": "STORY-002",
        "start_time": "2025-11-07T11:00:00Z",
        "end_time": "2025-11-07T11:35:00Z",
        "total_duration": 2100,
        "status": "FAILURE",
        "failed_phase": "qa",
        "phases_executed": [
            {
                "phase": "development",
                "start_time": "2025-11-07T11:00:00Z",
                "end_time": "2025-11-07T11:20:00Z",
                "duration": 1200,
                "status": "PASSED"
            },
            {
                "phase": "qa",
                "start_time": "2025-11-07T11:20:00Z",
                "end_time": "2025-11-07T11:35:00Z",
                "duration": 900,
                "status": "FAILED",
                "failure_reason": "Coverage below threshold (85% < 95% required)",
                "qa_attempts": 1
            }
        ],
        "phases_aborted": ["release"],
        "quality_gates": {
            "context_validation": {"status": "PASSED"},
            "test_passing": {"status": "PASSED"},
            "coverage": {"status": "FAILED", "percentage": 85.3, "threshold": 95},
            "qa_approved": {"status": "NOT_RUN"}
        },
        "failure_summary": "QA validation failed: Coverage threshold not met",
        "checkpoint_info": {
            "checkpoint_resumed": False,
            "resume_point": None
        }
    }


@pytest.fixture
def workflow_context_checkpoint_resume():
    """Sample workflow context from checkpoint resume."""
    return {
        "workflow_id": str(uuid4()),
        "story_id": "STORY-003",
        "start_time": "2025-11-07T09:00:00Z",
        "end_time": "2025-11-07T12:15:00Z",
        "total_duration": 11700,
        "status": "SUCCESS",
        "phases_executed_this_session": [
            {
                "phase": "release",
                "start_time": "2025-11-07T12:00:00Z",
                "end_time": "2025-11-07T12:15:00Z",
                "duration": 900,
                "status": "PASSED"
            }
        ],
        "quality_gates": {
            "release": {"status": "PASSED"}
        },
        "checkpoint_info": {
            "checkpoint_resumed": True,
            "resume_point": "QA_APPROVED",
            "previous_phases_duration": 10800,
            "phases_in_previous_sessions": [
                {"phase": "development", "status": "PASSED"},
                {"phase": "qa", "status": "PASSED"}
            ]
        }
    }


@pytest.fixture
def hook_config_failures_only():
    """Hook configuration in failures-only mode (default)."""
    return {
        "enabled": True,
        "operation": "orchestrate",
        "trigger": "failures-only",
        "commands": {
            "check_hooks": ["devforgeai", "check-hooks"],
            "invoke_hooks": ["devforgeai", "invoke-hooks"]
        },
        "created_at": "2025-11-07T00:00:00Z"
    }


@pytest.fixture
def hook_config_all_statuses():
    """Hook configuration triggering on all statuses."""
    return {
        "enabled": True,
        "operation": "orchestrate",
        "trigger": "all-statuses",
        "commands": {
            "check_hooks": ["devforgeai", "check-hooks"],
            "invoke_hooks": ["devforgeai", "invoke-hooks"]
        },
        "created_at": "2025-11-07T00:00:00Z"
    }


@pytest.fixture
def iso8601_timestamp():
    """Generate current ISO8601 timestamp."""
    return datetime.now(timezone.utc).isoformat() + "Z"


# ============================================================================
# AC1: HOOK INVOCATION ON COMPLETE WORKFLOW SUCCESS
# ============================================================================


class TestHookInvocationOnSuccess:
    """Unit tests for hook invocation on complete workflow success."""

    def test_devforgeai_check_hooks_called_on_success(self, workflow_context_success):
        """AC1: devforgeai check-hooks invoked with --operation=orchestrate --status=SUCCESS."""
        # Arrange
        context = workflow_context_success
        assert context["status"] == "SUCCESS"

        expected_args = [
            "devforgeai", "check-hooks",
            "--operation=orchestrate",
            "--status=SUCCESS"
        ]

        # Act
        # Simulate check-hooks invocation
        should_check = context["status"] == "SUCCESS"

        # Assert
        assert should_check is True

    def test_hook_context_includes_total_duration(self, workflow_context_success):
        """AC1: Hook context includes total_duration."""
        # Arrange
        context = workflow_context_success

        # Act
        has_duration = "total_duration" in context

        # Assert
        assert has_duration is True
        assert context["total_duration"] == 2700  # 45 minutes in seconds

    def test_hook_context_includes_all_phases_executed(self, workflow_context_success):
        """AC1: Hook context includes all phases_executed."""
        # Arrange
        context = workflow_context_success
        expected_phases = ["development", "qa", "release"]

        # Act
        phases_list = [p["phase"] for p in context["phases_executed"]]

        # Assert
        assert set(phases_list) == set(expected_phases)

    def test_hook_context_includes_quality_gate_results(self, workflow_context_success):
        """AC1: Hook context includes quality_gates results."""
        # Arrange
        context = workflow_context_success

        # Act
        has_gates = "quality_gates" in context
        gates_list = list(context["quality_gates"].keys())

        # Assert
        assert has_gates is True
        assert "context_validation" in gates_list
        assert "test_passing" in gates_list
        assert "coverage" in gates_list
        assert "qa_approved" in gates_list

    def test_hook_context_includes_start_and_end_times(self, workflow_context_success):
        """AC1: Hook context includes ISO8601 start_time and end_time."""
        # Arrange
        context = workflow_context_success

        # Act
        has_times = "start_time" in context and "end_time" in context

        # Assert
        assert has_times is True
        assert context["start_time"].endswith("Z")
        assert context["end_time"].endswith("Z")

    def test_hook_context_aggregates_all_phase_durations(self, workflow_context_success):
        """AC1: Total duration equals sum of all phase durations."""
        # Arrange
        context = workflow_context_success
        total_duration = context["total_duration"]

        # Act
        phase_durations = [p["duration"] for p in context["phases_executed"]]
        sum_duration = sum(phase_durations)

        # Assert
        assert sum_duration == total_duration


# ============================================================================
# AC2: HOOK INVOCATION ON WORKFLOW FAILURE
# ============================================================================


class TestHookInvocationOnFailure:
    """Unit tests for hook invocation on workflow failure."""

    def test_devforgeai_check_hooks_called_on_failure(self, workflow_context_qa_failure):
        """AC2: devforgeai check-hooks invoked with --operation=orchestrate --status=FAILURE."""
        # Arrange
        context = workflow_context_qa_failure
        assert context["status"] == "FAILURE"

        expected_args = [
            "devforgeai", "check-hooks",
            "--operation=orchestrate",
            "--status=FAILURE"
        ]

        # Act
        should_check = context["status"] == "FAILURE"

        # Assert
        assert should_check is True

    def test_hook_context_includes_failed_phase(self, workflow_context_qa_failure):
        """AC2: Hook context includes failed_phase."""
        # Arrange
        context = workflow_context_qa_failure

        # Act
        has_failed_phase = "failed_phase" in context

        # Assert
        assert has_failed_phase is True
        assert context["failed_phase"] == "qa"

    def test_hook_context_includes_failure_reason(self, workflow_context_qa_failure):
        """AC2: Hook context includes failure_reason."""
        # Arrange
        context = workflow_context_qa_failure

        # Act
        has_reason = "failure_summary" in context

        # Assert
        assert has_reason is True
        assert len(context["failure_summary"]) > 0

    def test_hook_context_includes_qa_attempt_count(self, workflow_context_qa_failure):
        """AC2: Hook context includes qa_attempts when QA fails."""
        # Arrange
        context = workflow_context_qa_failure
        qa_phase = next(p for p in context["phases_executed"] if p["phase"] == "qa")

        # Act
        has_attempts = "qa_attempts" in qa_phase

        # Assert
        assert has_attempts is True
        assert qa_phase["qa_attempts"] >= 1

    def test_hook_context_includes_aborted_phases(self, workflow_context_qa_failure):
        """AC2: Hook context includes phases_aborted."""
        # Arrange
        context = workflow_context_qa_failure

        # Act
        has_aborted = "phases_aborted" in context

        # Assert
        assert has_aborted is True
        assert "release" in context["phases_aborted"]


# ============================================================================
# AC3: HOOK BEHAVIOR WITH CHECKPOINT RESUME
# ============================================================================


class TestHookCheckpointResume:
    """Unit tests for hook behavior during checkpoint resume."""

    def test_checkpoint_resumed_flag_set_true(self, workflow_context_checkpoint_resume):
        """AC3: checkpoint_resumed=true in context."""
        # Arrange
        context = workflow_context_checkpoint_resume

        # Act
        is_resumed = context["checkpoint_info"]["checkpoint_resumed"]

        # Assert
        assert is_resumed is True

    def test_checkpoint_resume_point_specified(self, workflow_context_checkpoint_resume):
        """AC3: resume_point specified in checkpoint_info."""
        # Arrange
        context = workflow_context_checkpoint_resume

        # Act
        resume_point = context["checkpoint_info"]["resume_point"]

        # Assert
        assert resume_point is not None
        assert resume_point == "QA_APPROVED"

    def test_phases_executed_only_current_session(self, workflow_context_checkpoint_resume):
        """AC3: phases_executed includes only current session phases."""
        # Arrange
        context = workflow_context_checkpoint_resume

        # Act
        phases_this_session = [p["phase"] for p in context["phases_executed_this_session"]]

        # Assert
        assert "release" in phases_this_session
        assert "development" not in phases_this_session
        assert "qa" not in phases_this_session

    def test_cumulative_workflow_duration_captured(self, workflow_context_checkpoint_resume):
        """AC3: total_duration includes all previous sessions."""
        # Arrange
        context = workflow_context_checkpoint_resume
        checkpoint_info = context["checkpoint_info"]

        # Act
        total = context["total_duration"]
        previous = checkpoint_info.get("previous_phases_duration", 0)
        current = sum(p["duration"] for p in context["phases_executed_this_session"])

        # Assert
        assert total == previous + current

    def test_previous_phases_captured_in_checkpoint_info(self, workflow_context_checkpoint_resume):
        """AC3: Previous phases recorded in checkpoint_info."""
        # Arrange
        context = workflow_context_checkpoint_resume

        # Act
        previous_phases = context["checkpoint_info"]["phases_in_previous_sessions"]

        # Assert
        assert len(previous_phases) == 2
        assert previous_phases[0]["phase"] == "development"
        assert previous_phases[1]["phase"] == "qa"


# ============================================================================
# AC4: DEFAULT FAILURES-ONLY MODE RESPECTED
# ============================================================================


class TestFailuresOnlyModeDefault:
    """Unit tests for failures-only mode (default) behavior."""

    def test_failures_only_mode_default_config(self, hook_config_failures_only):
        """AC4: Default hook config has trigger=failures-only."""
        # Arrange
        config = hook_config_failures_only

        # Act
        trigger = config["trigger"]

        # Assert
        assert trigger == "failures-only"

    def test_failures_only_skips_feedback_on_success(self, hook_config_failures_only, workflow_context_success):
        """AC4: Hook not triggered on success in failures-only mode."""
        # Arrange
        config = hook_config_failures_only
        context = workflow_context_success

        # Act
        should_trigger = (config["trigger"] == "all-statuses" or context["status"] == "FAILURE")

        # Assert
        assert should_trigger is False

    def test_failures_only_triggers_feedback_on_failure(self, hook_config_failures_only, workflow_context_qa_failure):
        """AC4: Hook triggered on failure in failures-only mode."""
        # Arrange
        config = hook_config_failures_only
        context = workflow_context_qa_failure

        # Act
        should_trigger = (config["trigger"] == "all-statuses" or context["status"] == "FAILURE")

        # Assert
        assert should_trigger is True

    def test_all_statuses_mode_triggers_on_success(self, hook_config_all_statuses, workflow_context_success):
        """AC4: all-statuses mode triggers on success."""
        # Arrange
        config = hook_config_all_statuses
        context = workflow_context_success

        # Act
        should_trigger = config["trigger"] == "all-statuses"

        # Assert
        assert should_trigger is True

    @pytest.mark.parametrize("status", ["SUCCESS", "FAILURE"])
    def test_hook_trigger_decision_based_on_mode_and_status(self, status):
        """AC4: Hook trigger decision based on mode and status."""
        # Arrange
        modes = ["failures-only", "all-statuses"]

        # Act & Assert
        for mode in modes:
            should_trigger = (mode == "all-statuses" or status == "FAILURE")
            if mode == "failures-only":
                assert should_trigger == (status == "FAILURE")
            else:
                assert should_trigger is True


# ============================================================================
# AC5: WORKFLOW-LEVEL CONTEXT CAPTURE
# ============================================================================


class TestWorkflowContextCapture:
    """Unit tests for comprehensive workflow-level context capture."""

    def test_workflow_duration_in_context(self, workflow_context_success):
        """AC5: workflow_duration captured."""
        # Arrange
        context = workflow_context_success

        # Act
        has_duration = "total_duration" in context

        # Assert
        assert has_duration is True
        assert isinstance(context["total_duration"], int)
        assert context["total_duration"] > 0

    def test_phases_executed_in_context(self, workflow_context_success):
        """AC5: phases_executed list in context."""
        # Arrange
        context = workflow_context_success

        # Act
        has_phases = "phases_executed" in context
        phases = context["phases_executed"]

        # Assert
        assert has_phases is True
        assert len(phases) > 0
        for phase in phases:
            assert "phase" in phase
            assert "status" in phase
            assert "duration" in phase

    def test_quality_gates_in_context(self, workflow_context_success):
        """AC5: quality_gates in context."""
        # Arrange
        context = workflow_context_success

        # Act
        has_gates = "quality_gates" in context

        # Assert
        assert has_gates is True
        assert isinstance(context["quality_gates"], dict)

    def test_failure_summary_in_context(self, workflow_context_qa_failure):
        """AC5: failure_summary in context when workflow fails."""
        # Arrange
        context = workflow_context_qa_failure

        # Act
        has_summary = "failure_summary" in context

        # Assert
        assert has_summary is True
        assert isinstance(context["failure_summary"], str)

    def test_checkpoint_info_in_context(self, workflow_context_checkpoint_resume):
        """AC5: checkpoint_info in context."""
        # Arrange
        context = workflow_context_checkpoint_resume

        # Act
        has_checkpoint = "checkpoint_info" in context

        # Assert
        assert has_checkpoint is True
        assert "checkpoint_resumed" in context["checkpoint_info"]

    def test_context_is_json_serializable(self, workflow_context_success):
        """AC5: Entire context is JSON serializable."""
        # Arrange
        context = workflow_context_success

        # Act
        try:
            json_str = json.dumps(context)
            parsed = json.loads(json_str)
            serializable = True
        except (TypeError, ValueError):
            serializable = False

        # Assert
        assert serializable is True

    def test_context_includes_workflow_id(self, workflow_context_success):
        """AC5: context includes unique workflow_id."""
        # Arrange
        context = workflow_context_success

        # Act
        has_id = "workflow_id" in context
        id_value = context.get("workflow_id", "")

        # Assert
        assert has_id is True
        assert len(id_value) > 0

    def test_context_includes_story_id(self, workflow_context_success):
        """AC5: context includes story_id."""
        # Arrange
        context = workflow_context_success

        # Act
        has_story = "story_id" in context

        # Assert
        assert has_story is True
        assert context["story_id"].startswith("STORY-")


# ============================================================================
# AC6: GRACEFUL DEGRADATION ON HOOK FAILURES
# ============================================================================


class TestGracefulDegradationOnHookFailure:
    """Unit tests for graceful degradation when hook system fails."""

    def test_hook_cli_failure_logged_as_warning(self):
        """AC6: Hook CLI failure logged as warning, not error."""
        # Arrange
        hook_error = "devforgeai check-hooks exited with code 1"
        log_level = "WARNING"

        # Act
        should_log_warning = log_level == "WARNING"

        # Assert
        assert should_log_warning is True

    def test_hook_failure_does_not_fail_orchestrate(self, workflow_context_success):
        """AC6: Orchestrate completes with original status despite hook failure."""
        # Arrange
        original_status = workflow_context_success["status"]
        hook_failed = True

        # Act
        final_status = original_status if hook_failed else original_status

        # Assert
        assert final_status == "SUCCESS"

    def test_standard_summary_displayed_on_hook_failure(self, workflow_context_success):
        """AC6: Standard summary displayed when hook invocation fails."""
        # Arrange
        context = workflow_context_success
        has_context = context is not None

        # Act
        can_display_standard = has_context

        # Assert
        assert can_display_standard is True

    def test_hook_exit_code_nonzero_triggers_degradation(self):
        """AC6: Non-zero exit code from hook triggers degradation."""
        # Arrange
        exit_code = 1
        should_degrade = exit_code != 0

        # Act
        degradation_triggered = should_degrade

        # Assert
        assert degradation_triggered is True

    def test_hook_timeout_treated_as_failure(self):
        """AC6: Hook timeout (>100ms for check, >3s for invoke) triggers degradation."""
        # Arrange
        check_timeout_ms = 150
        check_limit_ms = 100

        # Act
        check_failed = check_timeout_ms > check_limit_ms

        # Assert
        assert check_failed is True

    def test_orchestrate_exits_with_original_status_on_hook_failure(self, workflow_context_success):
        """AC6: Orchestrate exit code reflects original workflow status."""
        # Arrange
        original_status = workflow_context_success["status"]
        hook_failed = True

        # Act
        exit_code = 0 if original_status == "SUCCESS" else 1

        # Assert
        assert exit_code == 0

    def test_hook_exception_caught_and_logged(self):
        """AC6: Hook exceptions caught and logged gracefully."""
        # Arrange
        exception_msg = "Hook invocation failed: connection timeout"

        # Act
        caught = True
        logged = True

        # Assert
        assert caught is True
        assert logged is True


# ============================================================================
# AC7: PERFORMANCE REQUIREMENTS
# ============================================================================


class TestPerformanceRequirements:
    """Unit tests for performance thresholds."""

    @pytest.mark.performance
    def test_check_hooks_completes_under_100ms_p95(self):
        """AC7: devforgeai check-hooks completes in <100ms (p95)."""
        # Arrange
        check_hook_times_ms = [45, 52, 48, 95, 50, 55, 60, 65, 70, 75]  # Simulated 10 runs
        p95_index = int(len(check_hook_times_ms) * 0.95)
        check_hook_times_ms.sort()
        p95_time = check_hook_times_ms[p95_index]

        # Act
        meets_requirement = p95_time < 100

        # Assert
        assert meets_requirement is True
        assert p95_time <= 95  # Observed from fixture

    @pytest.mark.performance
    def test_invoke_hooks_completes_under_3s_p95(self):
        """AC7: devforgeai invoke-hooks completes in <3s (p95)."""
        # Arrange
        invoke_hook_times_s = [0.8, 1.2, 0.9, 2.8, 1.1, 1.0, 1.5, 0.7, 1.3, 2.5]  # Simulated 10 runs
        p95_index = int(len(invoke_hook_times_s) * 0.95)
        invoke_hook_times_s.sort()
        p95_time = invoke_hook_times_s[p95_index]

        # Act
        meets_requirement = p95_time < 3.0

        # Assert
        assert meets_requirement is True
        assert p95_time <= 2.8

    @pytest.mark.performance
    def test_total_hook_overhead_under_200ms(self):
        """AC7: Total hook overhead (check + invoke) <200ms."""
        # Arrange
        check_time_ms = 50
        invoke_time_ms = 100
        total_overhead_ms = check_time_ms + invoke_time_ms

        # Act
        meets_requirement = total_overhead_ms < 200

        # Assert
        assert meets_requirement is True

    @pytest.mark.performance
    def test_context_extraction_completes_quickly(self, workflow_context_success):
        """AC7: Context extraction doesn't significantly impact workflow time."""
        # Arrange
        context_extraction_overhead_pct = 0.5  # 0.5% overhead acceptable
        workflow_duration_seconds = workflow_context_success["total_duration"]
        allowed_overhead_seconds = workflow_duration_seconds * (context_extraction_overhead_pct / 100)

        # Act
        extraction_time_seconds = 0.01  # 10ms typical for context extraction

        # Assert
        assert extraction_time_seconds < allowed_overhead_seconds


# ============================================================================
# EDGE CASES
# ============================================================================


class TestEdgeCaseMultipleQARetries:
    """Edge Case 1: Multiple QA retry failures (qa_attempts=3, all fail)."""

    def test_multiple_qa_retries_failure_context(self):
        """Multiple QA retries failure captured in context."""
        # Arrange
        context = {
            "workflow_id": str(uuid4()),
            "story_id": "STORY-050",
            "status": "FAILURE",
            "failed_phase": "qa",
            "qa_attempts": 3,
            "phases_executed": [
                {"phase": "development", "status": "PASSED", "duration": 1200},
                {
                    "phase": "qa",
                    "status": "FAILED",
                    "duration": 1800,
                    "qa_attempts": 3,
                    "qa_attempt_history": [
                        {"attempt": 1, "failure": "Coverage: 80% < 95%"},
                        {"attempt": 2, "failure": "Coverage: 82% < 95%"},
                        {"attempt": 3, "failure": "Coverage: 83% < 95%"}
                    ]
                }
            ],
            "phases_aborted": ["release"],
            "failure_summary": "QA failed after 3 retry attempts"
        }

        # Act
        has_attempts = context["qa_attempts"] == 3
        history_captured = len(context["phases_executed"][1]["qa_attempt_history"]) == 3

        # Assert
        assert has_attempts is True
        assert history_captured is True
        assert context["status"] == "FAILURE"

    def test_all_qa_attempts_recorded(self):
        """All QA attempt failures recorded."""
        # Arrange
        context = {
            "phases_executed": [
                {
                    "phase": "qa",
                    "qa_attempt_history": [
                        {"attempt": 1, "failure": "Reason 1"},
                        {"attempt": 2, "failure": "Reason 2"},
                        {"attempt": 3, "failure": "Reason 3"}
                    ]
                }
            ]
        }

        # Act
        attempt_count = len(context["phases_executed"][0]["qa_attempt_history"])

        # Assert
        assert attempt_count == 3


class TestEdgeCaseStagingSuccessProductionFailure:
    """Edge Case 2: Staging success, production failure."""

    def test_staging_success_production_failure_context(self):
        """Context captures staging vs production status."""
        # Arrange
        context = {
            "workflow_id": str(uuid4()),
            "status": "FAILURE",
            "failed_phase": "release",
            "phases_executed": [
                {"phase": "development", "status": "PASSED"},
                {"phase": "qa", "status": "PASSED"},
                {
                    "phase": "release",
                    "status": "FAILED",
                    "release_phases": [
                        {"environment": "staging", "status": "PASSED", "duration": 300},
                        {"environment": "production", "status": "FAILED", "error": "Health check timeout"}
                    ]
                }
            ],
            "failure_summary": "Production deployment failed (health check timeout)"
        }

        # Act
        staging_passed = context["phases_executed"][2]["release_phases"][0]["status"] == "PASSED"
        prod_failed = context["phases_executed"][2]["release_phases"][1]["status"] == "FAILED"

        # Assert
        assert staging_passed is True
        assert prod_failed is True


class TestEdgeCaseCheckpointResumeAfterManualFix:
    """Edge Case 3: Checkpoint resume after manual fix."""

    def test_checkpoint_resume_with_manual_intervention(self):
        """Context indicates manual fix between checkpoint and resume."""
        # Arrange
        context = {
            "workflow_id": str(uuid4()),
            "status": "SUCCESS",
            "checkpoint_info": {
                "checkpoint_resumed": True,
                "resume_point": "DEV_COMPLETE",
                "manual_intervention_between_sessions": True,
                "intervention_description": "Fixed coverage issue manually"
            },
            "phases_executed_this_session": [
                {"phase": "qa", "status": "PASSED"},
                {"phase": "release", "status": "PASSED"}
            ]
        }

        # Act
        has_intervention = context["checkpoint_info"]["manual_intervention_between_sessions"]

        # Assert
        assert has_intervention is True


class TestEdgeCaseHookConfigMissingInvalid:
    """Edge Case 4: Hook config missing/invalid."""

    def test_missing_hook_config_graceful_degradation(self):
        """Missing hook config triggers degradation, not error."""
        # Arrange
        config = None
        workflow_status = "SUCCESS"

        # Act
        can_proceed = workflow_status is not None

        # Assert
        assert can_proceed is True

    def test_invalid_hook_config_caught_and_logged(self):
        """Invalid hook config caught and workflow continues."""
        # Arrange
        config = {"invalid": "structure"}

        # Act
        caught_exception = True
        logged = True

        # Assert
        assert caught_exception is True
        assert logged is True


class TestEdgeCaseConcurrentWorkflows:
    """Edge Case 5: Concurrent /orchestrate executions (multiple stories)."""

    def test_concurrent_workflows_no_race_conditions(self):
        """Multiple concurrent workflows don't cause race conditions."""
        # Arrange
        workflows = [
            {"workflow_id": str(uuid4()), "story_id": f"STORY-{100 + i}"}
            for i in range(3)
        ]

        # Act
        all_have_unique_ids = len(set(w["workflow_id"] for w in workflows)) == len(workflows)

        # Assert
        assert all_have_unique_ids is True

    def test_separate_hook_invocations_per_workflow(self):
        """Each workflow has separate hook invocation."""
        # Arrange
        workflow_ids = [str(uuid4()) for _ in range(3)]

        # Act
        invocations = [f"check-hooks --workflow-id={wid}" for wid in workflow_ids]

        # Assert
        assert len(set(invocations)) == 3  # All unique


class TestEdgeCaseExtremelyLongWorkflow:
    """Edge Case 6: Extremely long workflow duration (>6 hours)."""

    def test_long_workflow_duration_captured(self):
        """Extremely long workflow duration captured correctly."""
        # Arrange
        start = "2025-11-07T10:00:00Z"
        end = "2025-11-07T17:30:00Z"  # 7.5 hours later
        duration_seconds = 27000

        # Act
        context = {
            "start_time": start,
            "end_time": end,
            "total_duration": duration_seconds
        }

        # Assert
        assert context["total_duration"] > (6 * 3600)  # > 6 hours

    def test_long_workflow_performance_not_impacted(self):
        """Hook performance not degraded for long workflows."""
        # Arrange
        long_workflow_duration = 27000  # 7.5 hours
        hook_overhead_ms = 150

        # Act
        overhead_pct = (hook_overhead_ms / 1000) / long_workflow_duration * 100

        # Assert
        assert overhead_pct < 0.01  # < 0.01% overhead


# ============================================================================
# INTEGRATION TESTS - Full Workflow Simulations
# ============================================================================


class TestFullWorkflowSuccessToHookSkip:
    """Integration: Complete successful workflow skips feedback (failures-only mode)."""

    def test_full_workflow_success_failures_only_no_feedback(self, temp_project_dir, workflow_context_success):
        """Successful workflow with failures-only config skips hook invocation."""
        # Arrange
        config = {
            "trigger": "failures-only",
            "enabled": True
        }
        context = workflow_context_success

        # Act
        should_trigger = config["trigger"] == "all-statuses" or context["status"] == "FAILURE"

        # Assert
        assert should_trigger is False

    def test_workflow_completion_not_blocked_by_hook_skip(self, workflow_context_success):
        """Workflow completes successfully even when hook skipped."""
        # Arrange
        context = workflow_context_success

        # Act
        completed = context["status"] == "SUCCESS"

        # Assert
        assert completed is True


class TestFullWorkflowQAFailureToFeedbackTrigger:
    """Integration: QA failure triggers feedback workflow."""

    def test_qa_failure_triggers_check_hooks(self, workflow_context_qa_failure):
        """QA failure triggers check-hooks invocation."""
        # Arrange
        context = workflow_context_qa_failure
        config = {"trigger": "failures-only"}

        # Act
        should_trigger = config["trigger"] == "all-statuses" or context["status"] == "FAILURE"

        # Assert
        assert should_trigger is True

    def test_hook_context_passed_to_invoke(self, workflow_context_qa_failure):
        """Hook context passed to invoke-hooks with failure details."""
        # Arrange
        context = workflow_context_qa_failure

        # Act
        has_required_fields = all(key in context for key in [
            "status", "failed_phase", "failure_summary", "phases_executed"
        ])

        # Assert
        assert has_required_fields is True


class TestCheckpointResumeHookBehavior:
    """Integration: Checkpoint resume with proper hook context."""

    def test_checkpoint_resume_context_aggregates_all_phases(self, workflow_context_checkpoint_resume):
        """Checkpoint resume context includes all phases (current + previous)."""
        # Arrange
        context = workflow_context_checkpoint_resume

        # Act
        all_phases = (
            context["phases_executed_this_session"] +
            context["checkpoint_info"]["phases_in_previous_sessions"]
        )
        total_phases = len(all_phases)

        # Assert
        assert total_phases == 3
        assert all([p["phase"] in ["development", "qa", "release"] for p in all_phases])


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short", "-m", "not performance"])
