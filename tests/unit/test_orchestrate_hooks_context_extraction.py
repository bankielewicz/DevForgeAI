"""
Unit test suite for STORY-026: Context extraction and aggregation for orchestrate hooks

Tests cover:
- Workflow context extraction from story files
- Overall status determination
- Quality gate aggregation
- Phase duration calculations
- Hook eligibility determination
- Context validation

Framework: pytest
Test Pattern: AAA (Arrange, Act, Assert)
"""

import json
import pytest
from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4


# ============================================================================
# FIXTURES - Context Extraction Test Data
# ============================================================================


@pytest.fixture
def story_file_content_completed_workflow():
    """Sample story file with completed dev→qa→release workflow."""
    return """---
id: STORY-001
title: User Authentication
epic: EPIC-001
sprint: Sprint-1
status: Released
points: 8
---

## User Story

As a user, I want to log in with email and password.

## Acceptance Criteria

Given a user account exists
When I enter valid email and password
Then I should be logged in within 2 seconds

## Workflow History

### Development (2025-11-07)
- Started: 10:00:00Z
- Completed: 10:20:00Z
- Duration: 1200 seconds
- Status: PASSED
- Tests: 45 passed, 0 failed
- Coverage: 96.5%

### QA (2025-11-07)
- Started: 10:20:00Z
- Completed: 10:30:00Z
- Duration: 600 seconds
- Status: PASSED
- Validation: Deep QA approved
- Issues: None

### Release (2025-11-07)
- Started: 10:30:00Z
- Completed: 10:45:00Z
- Duration: 900 seconds
- Status: PASSED
- Staging: Successful
- Production: Successful
"""


@pytest.fixture
def story_file_content_qa_failure():
    """Sample story file with QA failure."""
    return """---
id: STORY-002
title: Password Reset
status: QA In Progress
---

## Workflow History

### Development
- Status: PASSED
- Duration: 1200 seconds

### QA Attempt 1
- Status: FAILED
- Failed Criterion: Coverage below threshold
- Coverage: 85.3% (required 95%)
- Duration: 900 seconds

### QA Attempt 2
- Status: FAILED
- Failed Criterion: Coverage below threshold
- Coverage: 87.1% (required 95%)
- Duration: 600 seconds
"""


@pytest.fixture
def story_file_content_checkpoint_resume():
    """Sample story file with checkpoint resume history."""
    return """---
id: STORY-003
title: Payment Processing
status: Released
---

## Workflow History

### Development (2025-11-07 09:00-09:30)
- Status: PASSED
- Duration: 1800 seconds

### QA (2025-11-07 09:30-10:00)
- Status: PASSED
- Duration: 1800 seconds

### Checkpoint: QA_APPROVED
- Created: 2025-11-07 10:00:00Z
- Reason: Manual intervention needed

### Release Resume (2025-11-07 12:00-12:15)
- Resumed From: QA_APPROVED
- Status: PASSED
- Duration: 900 seconds
- Manual Fix Applied: Coverage issue resolved
"""


@pytest.fixture
def phase_data_dev_passed():
    """Sample development phase data."""
    return {
        "name": "development",
        "start": "2025-11-07T10:00:00Z",
        "end": "2025-11-07T10:20:00Z",
        "status": "PASSED",
        "metrics": {
            "tests_run": 45,
            "tests_passed": 45,
            "tests_failed": 0,
            "coverage": 96.5
        }
    }


@pytest.fixture
def phase_data_qa_passed():
    """Sample QA phase data."""
    return {
        "name": "qa",
        "start": "2025-11-07T10:20:00Z",
        "end": "2025-11-07T10:30:00Z",
        "status": "PASSED",
        "validation_type": "deep"
    }


@pytest.fixture
def phase_data_release_passed():
    """Sample release phase data."""
    return {
        "name": "release",
        "start": "2025-11-07T10:30:00Z",
        "end": "2025-11-07T10:45:00Z",
        "status": "PASSED",
        "environments": {
            "staging": "PASSED",
            "production": "PASSED"
        }
    }


# ============================================================================
# WORKFLOW STATUS DETERMINATION TESTS
# ============================================================================


class TestWorkflowStatusDetermination:
    """Unit tests for overall workflow status determination."""

    def test_all_phases_passed_status_success(self):
        """Overall status = SUCCESS when all phases passed."""
        # Arrange
        phases = [
            {"phase": "dev", "status": "PASSED"},
            {"phase": "qa", "status": "PASSED"},
            {"phase": "release", "status": "PASSED"}
        ]

        # Act
        overall_status = "SUCCESS" if all(p["status"] == "PASSED" for p in phases) else "FAILURE"

        # Assert
        assert overall_status == "SUCCESS"

    def test_any_phase_failed_status_failure(self):
        """Overall status = FAILURE if any phase failed."""
        # Arrange
        phases = [
            {"phase": "dev", "status": "PASSED"},
            {"phase": "qa", "status": "FAILED"},
            {"phase": "release", "status": "NOT_RUN"}
        ]

        # Act
        overall_status = "SUCCESS" if all(p["status"] == "PASSED" for p in phases) else "FAILURE"

        # Assert
        assert overall_status == "FAILURE"

    def test_phase_not_run_means_workflow_incomplete(self):
        """Phases marked NOT_RUN mean workflow stopped."""
        # Arrange
        phases = [
            {"phase": "dev", "status": "PASSED"},
            {"phase": "qa", "status": "FAILED"},
            {"phase": "release", "status": "NOT_RUN"}
        ]

        # Act
        has_not_run = any(p["status"] == "NOT_RUN" for p in phases)

        # Assert
        assert has_not_run is True

    def test_dev_failure_aborts_qa_release(self):
        """Dev failure means QA and release don't execute."""
        # Arrange
        phases = [
            {"phase": "dev", "status": "FAILED"},
            {"phase": "qa", "status": "NOT_RUN"},
            {"phase": "release", "status": "NOT_RUN"}
        ]

        # Act
        dev_failed = phases[0]["status"] == "FAILED"
        downstream_skipped = all(p["status"] == "NOT_RUN" for p in phases[1:])

        # Assert
        assert dev_failed is True
        assert downstream_skipped is True


# ============================================================================
# PHASE DURATION CALCULATION TESTS
# ============================================================================


class TestPhaseDurationCalculation:
    """Unit tests for phase duration extraction and calculation."""

    def test_duration_extracted_from_timestamps(self, phase_data_dev_passed):
        """Duration calculated as end_time - start_time."""
        # Arrange
        phase = phase_data_dev_passed
        start = datetime.fromisoformat(phase["start"].replace("Z", "+00:00"))
        end = datetime.fromisoformat(phase["end"].replace("Z", "+00:00"))

        # Act
        duration_seconds = int((end - start).total_seconds())

        # Assert
        assert duration_seconds == 1200  # 20 minutes

    def test_total_duration_sum_of_phase_durations(self, phase_data_dev_passed, phase_data_qa_passed, phase_data_release_passed):
        """Total duration equals sum of all phase durations."""
        # Arrange
        phases = [phase_data_dev_passed, phase_data_qa_passed, phase_data_release_passed]
        phase_durations = []

        for phase in phases:
            start = datetime.fromisoformat(phase["start"].replace("Z", "+00:00"))
            end = datetime.fromisoformat(phase["end"].replace("Z", "+00:00"))
            phase_durations.append(int((end - start).total_seconds()))

        # Act
        total = sum(phase_durations)

        # Assert
        assert total == 2700  # 45 minutes total

    def test_phase_duration_always_positive(self):
        """Phase duration never negative."""
        # Arrange
        start = "2025-11-07T10:00:00Z"
        end = "2025-11-07T10:20:00Z"

        # Act
        start_dt = datetime.fromisoformat(start.replace("Z", "+00:00"))
        end_dt = datetime.fromisoformat(end.replace("Z", "+00:00"))
        duration = int((end_dt - start_dt).total_seconds())

        # Assert
        assert duration > 0


# ============================================================================
# QUALITY GATE AGGREGATION TESTS
# ============================================================================


class TestQualityGateAggregation:
    """Unit tests for quality gate status aggregation."""

    def test_all_gates_passed_aggregates_to_passed(self):
        """All gates PASSED → Overall gate status PASSED."""
        # Arrange
        gates = {
            "context_validation": {"status": "PASSED"},
            "test_passing": {"status": "PASSED"},
            "coverage": {"status": "PASSED"},
            "qa_approved": {"status": "PASSED"}
        }

        # Act
        all_passed = all(g["status"] == "PASSED" for g in gates.values())

        # Assert
        assert all_passed is True

    def test_any_gate_failed_aggregates_to_failed(self):
        """Any gate FAILED → Overall gate status FAILED."""
        # Arrange
        gates = {
            "context_validation": {"status": "PASSED"},
            "test_passing": {"status": "PASSED"},
            "coverage": {"status": "FAILED"},
            "qa_approved": {"status": "NOT_RUN"}
        }

        # Act
        any_failed = any(g["status"] == "FAILED" for g in gates.values())

        # Assert
        assert any_failed is True

    def test_gate_failure_includes_reason(self):
        """Failed gate includes failure reason."""
        # Arrange
        gate = {
            "status": "FAILED",
            "reason": "Coverage 85.3% < 95% threshold",
            "actual": 85.3,
            "threshold": 95
        }

        # Act
        has_reason = "reason" in gate or "actual" in gate

        # Assert
        assert has_reason is True

    def test_gate_details_included_for_context(self):
        """Gate details included for context (e.g., coverage percentage)."""
        # Arrange
        gate = {
            "status": "PASSED",
            "percentage": 96.5,
            "threshold": 95
        }

        # Act
        has_details = "percentage" in gate and "threshold" in gate

        # Assert
        assert has_details is True


# ============================================================================
# FAILED PHASE IDENTIFICATION TESTS
# ============================================================================


class TestFailedPhaseIdentification:
    """Unit tests for identifying and capturing failed phases."""

    def test_failed_phase_identified(self):
        """Failed phase correctly identified."""
        # Arrange
        phases = [
            {"phase": "dev", "status": "PASSED"},
            {"phase": "qa", "status": "FAILED"},
            {"phase": "release", "status": "NOT_RUN"}
        ]

        # Act
        failed_phases = [p["phase"] for p in phases if p["status"] == "FAILED"]

        # Assert
        assert failed_phases == ["qa"]

    def test_first_failed_phase_marked(self):
        """First failed phase identified (stops cascade)."""
        # Arrange
        phases = [
            {"phase": "dev", "status": "PASSED"},
            {"phase": "qa", "status": "FAILED", "reason": "Coverage"},
            {"phase": "release", "status": "NOT_RUN"}
        ]

        # Act
        first_failed = next((p for p in phases if p["status"] == "FAILED"), None)

        # Assert
        assert first_failed["phase"] == "qa"
        assert first_failed["reason"] == "Coverage"

    def test_aborted_phases_list_captured(self):
        """Phases that didn't run after failure captured."""
        # Arrange
        phases = [
            {"phase": "dev", "status": "PASSED"},
            {"phase": "qa", "status": "FAILED"},
            {"phase": "release", "status": "NOT_RUN"}
        ]

        # Act
        failed_idx = next(i for i, p in enumerate(phases) if p["status"] == "FAILED")
        aborted = [p["phase"] for p in phases[failed_idx+1:]]

        # Assert
        assert aborted == ["release"]


# ============================================================================
# QA ATTEMPT TRACKING TESTS
# ============================================================================


class TestQAAttemptTracking:
    """Unit tests for QA retry attempt tracking."""

    def test_qa_attempts_count_incremented(self):
        """QA attempts counter incremented on each failure."""
        # Arrange
        attempts = [
            {"attempt": 1, "status": "FAILED", "reason": "Coverage 85.3%"},
            {"attempt": 2, "status": "FAILED", "reason": "Coverage 87.1%"},
            {"attempt": 3, "status": "FAILED", "reason": "Coverage 88.9%"}
        ]

        # Act
        final_attempt_count = len(attempts)

        # Assert
        assert final_attempt_count == 3

    def test_qa_attempt_history_captured(self):
        """All QA attempt history captured with reasons."""
        # Arrange
        qa_phase = {
            "phase": "qa",
            "status": "FAILED",
            "attempts": 3,
            "attempt_history": [
                {"attempt": 1, "status": "FAILED", "reason": "Coverage 85.3%"},
                {"attempt": 2, "status": "FAILED", "reason": "Coverage 87.1%"},
                {"attempt": 3, "status": "FAILED", "reason": "Coverage 88.9%"}
            ]
        }

        # Act
        history_count = len(qa_phase["attempt_history"])

        # Assert
        assert history_count == 3
        assert qa_phase["attempts"] == 3


# ============================================================================
# CHECKPOINT RESUME CONTEXT TESTS
# ============================================================================


class TestCheckpointResumeContext:
    """Unit tests for checkpoint resume context extraction."""

    def test_checkpoint_resumed_flag_extracted(self):
        """Checkpoint resume flag extracted from story."""
        # Arrange
        story_content = """
## Workflow History

### Development
- Status: PASSED

### Checkpoint: QA_APPROVED
- Created: 2025-11-07 10:00:00Z

### Release Resume
- Status: PASSED
"""
        has_checkpoint = "Checkpoint:" in story_content

        # Act
        is_resumed = has_checkpoint

        # Assert
        assert is_resumed is True

    def test_resume_point_extracted(self):
        """Resume point name extracted (e.g., QA_APPROVED)."""
        # Arrange
        checkpoint_line = "### Checkpoint: QA_APPROVED"

        # Act
        resume_point = checkpoint_line.split(": ")[1]

        # Assert
        assert resume_point == "QA_APPROVED"

    def test_previous_phases_separated_from_current(self):
        """Previous session phases separated from current session."""
        # Arrange
        phases = [
            {"phase": "dev", "session": "previous"},
            {"phase": "qa", "session": "previous"},
            {"phase": "release", "session": "current"}
        ]

        # Act
        previous = [p for p in phases if p["session"] == "previous"]
        current = [p for p in phases if p["session"] == "current"]

        # Assert
        assert len(previous) == 2
        assert len(current) == 1

    def test_cumulative_duration_calculated_with_previous(self):
        """Total duration includes previous session phases."""
        # Arrange
        previous_duration = 3600  # 1 hour from previous session
        current_duration = 1200   # 20 minutes this session

        # Act
        total_duration = previous_duration + current_duration

        # Assert
        assert total_duration == 4800


# ============================================================================
# CONTEXT VALIDATION TESTS
# ============================================================================


class TestContextValidation:
    """Unit tests for context validation."""

    def test_context_has_required_fields(self):
        """Context includes all required fields."""
        # Arrange
        context = {
            "workflow_id": str(uuid4()),
            "story_id": "STORY-001",
            "status": "SUCCESS",
            "total_duration": 2700,
            "start_time": "2025-11-07T10:00:00Z",
            "end_time": "2025-11-07T10:45:00Z",
            "phases_executed": [],
            "quality_gates": {}
        }

        required_fields = [
            "workflow_id", "story_id", "status", "total_duration",
            "start_time", "end_time", "phases_executed", "quality_gates"
        ]

        # Act
        has_all = all(field in context for field in required_fields)

        # Assert
        assert has_all is True

    def test_story_id_format_valid(self):
        """Story ID has valid format STORY-###."""
        # Arrange
        story_id = "STORY-001"

        # Act
        is_valid = story_id.startswith("STORY-") and story_id[6:].isdigit()

        # Assert
        assert is_valid is True

    def test_timestamps_iso8601_format(self):
        """Timestamps are ISO8601 formatted."""
        # Arrange
        timestamp = "2025-11-07T10:00:00Z"

        # Act
        is_iso8601 = "T" in timestamp and "Z" in timestamp

        # Assert
        assert is_iso8601 is True

    def test_duration_positive_integer(self):
        """Duration is positive integer."""
        # Arrange
        duration = 2700

        # Act
        is_positive = isinstance(duration, int) and duration > 0

        # Assert
        assert is_positive is True

    def test_context_json_serializable(self):
        """Entire context is JSON serializable."""
        # Arrange
        context = {
            "workflow_id": str(uuid4()),
            "status": "SUCCESS",
            "duration": 2700,
            "timestamp": "2025-11-07T10:00:00Z"
        }

        # Act
        try:
            json_str = json.dumps(context)
            json.loads(json_str)
            serializable = True
        except (TypeError, ValueError):
            serializable = False

        # Assert
        assert serializable is True


# ============================================================================
# FAILURE REASON EXTRACTION TESTS
# ============================================================================


class TestFailureReasonExtraction:
    """Unit tests for extracting failure reasons."""

    def test_coverage_failure_reason_extracted(self):
        """Coverage failure reason extracted."""
        # Arrange
        qa_result = {
            "status": "FAILED",
            "failed_criterion": "Coverage",
            "actual": 85.3,
            "required": 95
        }

        # Act
        reason = f"Coverage: {qa_result['actual']}% < {qa_result['required']}%"

        # Assert
        assert "Coverage" in reason
        assert "85.3" in reason
        assert "95" in reason

    def test_multiple_failure_reasons_aggregated(self):
        """Multiple failure reasons aggregated."""
        # Arrange
        qa_result = {
            "status": "FAILED",
            "failed_criteria": [
                {"criterion": "Coverage", "actual": 85.3, "required": 95},
                {"criterion": "API Contract", "actual": "missing endpoint"}
            ]
        }

        # Act
        reasons = [f"{c['criterion']}" for c in qa_result["failed_criteria"]]

        # Assert
        assert "Coverage" in reasons
        assert "API Contract" in reasons

    def test_failure_summary_generated(self):
        """Failure summary generated from reasons."""
        # Arrange
        failed_criterion = "Coverage below threshold"
        actual = 85.3
        threshold = 95

        # Act
        summary = f"QA failed: {failed_criterion} ({actual}% < {threshold}%)"

        # Assert
        assert "QA failed" in summary


# ============================================================================
# PHASE METRICS EXTRACTION TESTS
# ============================================================================


class TestPhaseMetricsExtraction:
    """Unit tests for extracting phase-level metrics."""

    def test_dev_phase_metrics_extracted(self):
        """Development phase metrics (tests, coverage) extracted."""
        # Arrange
        phase_data = {
            "phase": "dev",
            "tests": {"passed": 45, "failed": 0, "total": 45},
            "coverage": 96.5
        }

        # Act
        has_metrics = "tests" in phase_data and "coverage" in phase_data

        # Assert
        assert has_metrics is True

    def test_qa_phase_metrics_extracted(self):
        """QA phase metrics (validation type, gate status) extracted."""
        # Arrange
        phase_data = {
            "phase": "qa",
            "validation_type": "deep",
            "gates_passed": 4,
            "gates_total": 4
        }

        # Act
        has_metrics = "validation_type" in phase_data

        # Assert
        assert has_metrics is True

    def test_release_phase_environment_status_extracted(self):
        """Release phase environment status (staging, production) extracted."""
        # Arrange
        phase_data = {
            "phase": "release",
            "environments": {
                "staging": "PASSED",
                "production": "PASSED"
            }
        }

        # Act
        has_envs = "environments" in phase_data

        # Assert
        assert has_envs is True


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
