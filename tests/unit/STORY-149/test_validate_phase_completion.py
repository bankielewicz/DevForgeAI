"""
STORY-149: Phase Completion Validation Script

Comprehensive test suite for the validate_phase_completion module.
Tests phase validation CLI commands that enforce phase transitions
through exit codes (0=proceed, 1=blocked, 2=error).

Test Coverage:
- AC#1: phase-check command validates phase completion
- AC#2: Validates all required subagents invoked
- AC#3: Validates checkpoint passed flag
- AC#4: record-subagent command appends invocation
- AC#5: complete-phase command marks completion
- AC#6: Exit codes enable external enforcement

Edge Cases:
- Invalid story ID format
- State file not found
- Incomplete phase validation
- Checkpoint failed
- Invalid phase IDs
"""

import sys
from pathlib import Path

# Add project root to Python path BEFORE imports
_project_root = Path(__file__).parent.parent.parent.parent
if str(_project_root) not in sys.path:
    sys.path.insert(0, str(_project_root))

import json
import pytest
import time
from tempfile import TemporaryDirectory

from installer.validate_phase_completion import (
    ValidatePhaseCompletion,
    phase_check_command,
    record_subagent_command,
    complete_phase_command,
    validate_phase_check,
    validate_subagents_invoked,
    validate_checkpoint_passed,
    EXIT_CODE_PROCEED,
    EXIT_CODE_BLOCKED,
    EXIT_CODE_ERROR,
)


# =============================================================================
# Test Fixtures
# =============================================================================


@pytest.fixture
def temp_project_dir():
    """Create a temporary project directory with workflows subdirectory."""
    with TemporaryDirectory() as tmpdir:
        project_path = Path(tmpdir)
        workflows_dir = project_path / "devforgeai" / "workflows"
        workflows_dir.mkdir(parents=True, exist_ok=True)
        yield project_path


@pytest.fixture
def phase_state_fixture():
    """Fixture for a complete phase state structure."""
    return {
        "story_id": "STORY-001",
        "workflow_started": "2025-12-28T10:00:00Z",
        "current_phase": "02",
        "phases": {
            "01": {
                "status": "completed",
                "subagents_required": ["git-validator", "tech-stack-detector"],
                "subagents_invoked": ["git-validator", "tech-stack-detector"],
                "checkpoint_passed": True,
                "completed_at": "2025-12-28T10:05:00Z"
            },
            "02": {
                "status": "pending",
                "subagents_required": ["test-automator"],
                "subagents_invoked": [],
                "checkpoint_passed": False
            },
            "03": {
                "status": "pending",
                "subagents_required": [],
                "subagents_invoked": [],
                "checkpoint_passed": False
            }
        },
        "validation_errors": [],
        "blocking_status": False
    }


@pytest.fixture
def incomplete_phase_state():
    """Fixture for phase state with missing subagents."""
    return {
        "story_id": "STORY-001",
        "workflow_started": "2025-12-28T10:00:00Z",
        "current_phase": "01",
        "phases": {
            "01": {
                "status": "pending",
                "subagents_required": ["git-validator", "tech-stack-detector"],
                "subagents_invoked": ["git-validator"],  # Missing tech-stack-detector
                "checkpoint_passed": False
            },
            "02": {
                "status": "pending",
                "subagents_required": ["test-automator"],
                "subagents_invoked": [],
                "checkpoint_passed": False
            }
        },
        "validation_errors": [],
        "blocking_status": False
    }


@pytest.fixture
def checkpoint_failed_state():
    """Fixture for phase state where checkpoint failed."""
    return {
        "story_id": "STORY-001",
        "workflow_started": "2025-12-28T10:00:00Z",
        "current_phase": "01",
        "phases": {
            "01": {
                "status": "completed",
                "subagents_required": ["git-validator", "tech-stack-detector"],
                "subagents_invoked": ["git-validator", "tech-stack-detector"],
                "checkpoint_passed": False  # Checkpoint failed!
            },
            "02": {
                "status": "pending",
                "subagents_required": ["test-automator"],
                "subagents_invoked": [],
                "checkpoint_passed": False
            }
        },
        "validation_errors": [],
        "blocking_status": False
    }


# =============================================================================
# AC#1: phase-check Command Validates Phase Completion
# =============================================================================


class TestPhaseCheckCommand:
    """Tests for AC#1: CLI command validates phase completion."""

    def test_phase_check_validates_completion_exit_code_zero(self, temp_project_dir, phase_state_fixture):
        """
        Scenario: phase-check succeeds when previous phase is complete
        Given: A completed phase with all subagents and checkpoint passed
        When: phase-check is called with --from=01 --to=02
        Then: Exit code 0 is returned (proceed)
        """
        # Arrange
        state_file = temp_project_dir / "devforgeai" / "workflows" / "STORY-001-phase-state.json"
        state_file.write_text(json.dumps(phase_state_fixture))

        # Act
        result = phase_check_command(
            story_id="STORY-001",
            from_phase="01",
            to_phase="02",
            project_root=str(temp_project_dir)
        )

        # Assert
        assert result == EXIT_CODE_PROCEED

    def test_phase_check_blocks_incomplete_phase(self, temp_project_dir, incomplete_phase_state):
        """
        Scenario: phase-check blocks progression when previous phase incomplete
        Given: A phase with status != completed
        When: phase-check is called
        Then: Exit code 1 is returned (blocked)
        """
        # Arrange
        state_file = temp_project_dir / "devforgeai" / "workflows" / "STORY-001-phase-state.json"
        state_file.write_text(json.dumps(incomplete_phase_state))

        # Act
        result = phase_check_command(
            story_id="STORY-001",
            from_phase="01",
            to_phase="02",
            project_root=str(temp_project_dir)
        )

        # Assert
        assert result == EXIT_CODE_BLOCKED

    def test_phase_check_errors_on_missing_state_file(self, temp_project_dir):
        """
        Scenario: phase-check returns error when state file missing
        Given: Story ID with no corresponding state file
        When: phase-check is called
        Then: Exit code 2 is returned (error)
        """
        # Arrange - no state file created

        # Act
        result = phase_check_command(
            story_id="STORY-999",
            from_phase="01",
            to_phase="02",
            project_root=str(temp_project_dir)
        )

        # Assert
        assert result == EXIT_CODE_ERROR

    def test_phase_check_invalid_story_id_format(self, temp_project_dir):
        """
        Scenario: phase-check rejects invalid story ID format
        Given: Story ID that doesn't match STORY-XXX pattern
        When: phase-check is called
        Then: Exit code 2 is returned (error)
        """
        # Act
        result = phase_check_command(
            story_id="INVALID-001",
            from_phase="01",
            to_phase="02",
            project_root=str(temp_project_dir)
        )

        # Assert
        assert result == EXIT_CODE_ERROR

    def test_phase_check_invalid_phase_ids(self, temp_project_dir, phase_state_fixture):
        """
        Scenario: phase-check rejects invalid phase IDs
        Given: Phase IDs outside valid range (01-10)
        When: phase-check is called
        Then: Exit code 2 is returned (error)
        """
        # Arrange
        state_file = temp_project_dir / "devforgeai" / "workflows" / "STORY-001-phase-state.json"
        state_file.write_text(json.dumps(phase_state_fixture))

        # Act
        result = phase_check_command(
            story_id="STORY-001",
            from_phase="00",  # Invalid
            to_phase="02",
            project_root=str(temp_project_dir)
        )

        # Assert
        assert result == EXIT_CODE_ERROR


# =============================================================================
# AC#2: Validates All Required Subagents Invoked
# =============================================================================


class TestSubagentValidation:
    """Tests for AC#2: Validates all required subagents invoked."""

    def test_phase_check_validates_all_subagents_invoked(self):
        """
        Scenario: phase-check verifies all required subagents were invoked
        Given: Phase with all required subagents in subagents_invoked list
        When: validate_subagents_invoked() is called
        Then: Returns True (validation passed)
        """
        # Arrange
        required = ["git-validator", "tech-stack-detector"]
        invoked = ["git-validator", "tech-stack-detector"]

        # Act
        result = validate_subagents_invoked(required, invoked)

        # Assert
        assert result is True

    def test_phase_check_rejects_missing_subagents(self):
        """
        Scenario: phase-check rejects phase with missing subagents
        Given: Phase missing one required subagent
        When: validate_subagents_invoked() is called
        Then: Returns False (validation failed)
        """
        # Arrange
        required = ["git-validator", "tech-stack-detector"]
        invoked = ["git-validator"]  # Missing tech-stack-detector

        # Act
        result = validate_subagents_invoked(required, invoked)

        # Assert
        assert result is False

    def test_phase_check_rejects_all_missing_subagents(self):
        """
        Scenario: phase-check rejects phase with zero subagents invoked
        Given: Phase requires subagents but invoked list is empty
        When: validate_subagents_invoked() is called
        Then: Returns False (validation failed)
        """
        # Arrange
        required = ["git-validator", "tech-stack-detector"]
        invoked = []

        # Act
        result = validate_subagents_invoked(required, invoked)

        # Assert
        assert result is False

    def test_phase_check_exact_match_subagents(self):
        """
        Scenario: phase-check validates exact match of required subagents
        Given: Exactly the same subagents in required and invoked lists
        When: validate_subagents_invoked() is called
        Then: Returns True (exact match passes)
        """
        # Arrange
        required = ["test-automator"]
        invoked = ["test-automator"]

        # Act
        result = validate_subagents_invoked(required, invoked)

        # Assert
        assert result is True

    def test_phase_check_extra_subagents_allowed(self):
        """
        Scenario: phase-check allows extra subagents beyond required set
        Given: More subagents invoked than required (superset)
        When: validate_subagents_invoked() is called
        Then: Returns True (superset of required is acceptable)
        """
        # Arrange
        required = ["test-automator"]
        invoked = ["test-automator", "code-reviewer"]  # Extra subagent OK

        # Act
        result = validate_subagents_invoked(required, invoked)

        # Assert
        assert result is True


# =============================================================================
# AC#3: Validates Checkpoint Passed Flag
# =============================================================================


class TestCheckpointValidation:
    """Tests for AC#3: Validates checkpoint passed flag."""

    def test_phase_check_validates_checkpoint_passed(self):
        """
        Scenario: phase-check validates checkpoint_passed=true
        Given: Phase with checkpoint_passed flag set to True
        When: validate_checkpoint_passed() is called
        Then: Returns True (validation passed)
        """
        # Act
        result = validate_checkpoint_passed(True)

        # Assert
        assert result is True

    def test_phase_check_rejects_checkpoint_failed(self):
        """
        Scenario: phase-check blocks progression when checkpoint failed
        Given: Phase with checkpoint_passed=false
        When: validate_checkpoint_passed() is called
        Then: Returns False (validation failed, blocks progression)
        """
        # Act
        result = validate_checkpoint_passed(False)

        # Assert
        assert result is False

    def test_phase_check_rejects_missing_checkpoint_flag(self):
        """
        Scenario: phase-check treats missing checkpoint flag as failed
        Given: Default False value
        When: validate_checkpoint_passed() is called
        Then: Returns False (no checkpoint data = not passed)
        """
        # Act
        result = validate_checkpoint_passed(False)

        # Assert
        assert result is False

    def test_phase_check_checkpoint_overrides_subagents(self, temp_project_dir, checkpoint_failed_state):
        """
        Scenario: checkpoint_passed flag is required regardless of subagents
        Given: All subagents invoked but checkpoint failed
        When: phase_check_command is called
        Then: Phase check is blocked
        """
        # Arrange
        state_file = temp_project_dir / "devforgeai" / "workflows" / "STORY-001-phase-state.json"
        state_file.write_text(json.dumps(checkpoint_failed_state))

        # Act
        result = phase_check_command(
            story_id="STORY-001",
            from_phase="01",
            to_phase="02",
            project_root=str(temp_project_dir)
        )

        # Assert - blocked because checkpoint failed
        assert result == EXIT_CODE_BLOCKED


# =============================================================================
# AC#4: Record Subagent Invocation Command
# =============================================================================


class TestRecordSubagentCommand:
    """Tests for AC#4: record-subagent appends invocation."""

    def test_record_subagent_appends_entry(self, temp_project_dir, phase_state_fixture):
        """
        Scenario: record-subagent appends subagent to invocation list
        Given: A story with phase state file
        When: record-subagent is called
        Then: subagent is added and exit code 0 returned
        """
        # Arrange
        state_file = temp_project_dir / "devforgeai" / "workflows" / "STORY-001-phase-state.json"
        state_file.write_text(json.dumps(phase_state_fixture))

        # Act
        result = record_subagent_command(
            story_id="STORY-001",
            phase_id="02",
            subagent_name="test-automator",
            project_root=str(temp_project_dir)
        )

        # Assert
        assert result == EXIT_CODE_PROCEED

        # Verify subagent was added
        updated_state = json.loads(state_file.read_text())
        assert "test-automator" in updated_state["phases"]["02"]["subagents_invoked"]

    def test_record_subagent_append_only_semantics(self, temp_project_dir, phase_state_fixture):
        """
        Scenario: record-subagent uses append-only semantics (no duplicates)
        Given: Subagent already recorded in list
        When: record-subagent is called again with same subagent
        Then: Subagent list contains exactly one copy (idempotent)
        """
        # Arrange
        state_file = temp_project_dir / "devforgeai" / "workflows" / "STORY-001-phase-state.json"
        phase_state_fixture["phases"]["02"]["subagents_invoked"] = ["test-automator"]
        state_file.write_text(json.dumps(phase_state_fixture))

        # Act - record same subagent again
        result = record_subagent_command(
            story_id="STORY-001",
            phase_id="02",
            subagent_name="test-automator",
            project_root=str(temp_project_dir)
        )

        # Assert - should succeed (idempotent)
        assert result == EXIT_CODE_PROCEED

        # Verify only one copy
        updated_state = json.loads(state_file.read_text())
        count = updated_state["phases"]["02"]["subagents_invoked"].count("test-automator")
        assert count == 1

    def test_record_subagent_errors_on_missing_state_file(self, temp_project_dir):
        """
        Scenario: record-subagent returns error when state file missing
        Given: Story ID with no state file
        When: record-subagent is called
        Then: Exit code 2 is returned (error)
        """
        # Act
        result = record_subagent_command(
            story_id="STORY-999",
            phase_id="01",
            subagent_name="git-validator",
            project_root=str(temp_project_dir)
        )

        # Assert
        assert result == EXIT_CODE_ERROR

    def test_record_subagent_invalid_phase_id(self, temp_project_dir, phase_state_fixture):
        """
        Scenario: record-subagent rejects invalid phase ID
        Given: Phase ID outside valid range (00 or 11)
        When: record-subagent is called
        Then: Exit code 2 is returned (error)
        """
        # Arrange
        state_file = temp_project_dir / "devforgeai" / "workflows" / "STORY-001-phase-state.json"
        state_file.write_text(json.dumps(phase_state_fixture))

        # Act
        result = record_subagent_command(
            story_id="STORY-001",
            phase_id="00",  # Invalid
            subagent_name="git-validator",
            project_root=str(temp_project_dir)
        )

        # Assert
        assert result == EXIT_CODE_ERROR


# =============================================================================
# AC#5: Complete Phase Command Marks Completion
# =============================================================================


class TestCompletePhaseCommand:
    """Tests for AC#5: complete-phase marks completion."""

    def test_complete_phase_marks_completion(self, temp_project_dir, phase_state_fixture):
        """
        Scenario: complete-phase updates phase status to completed
        Given: A phase with all subagents invoked
        When: complete-phase is called with checkpoint_passed=True
        Then: Phase status becomes "completed", exit code 0 returned
        """
        # Arrange - ensure phase 02 has required subagents
        phase_state_fixture["current_phase"] = "02"
        phase_state_fixture["phases"]["02"]["subagents_invoked"] = ["test-automator"]
        state_file = temp_project_dir / "devforgeai" / "workflows" / "STORY-001-phase-state.json"
        state_file.write_text(json.dumps(phase_state_fixture))

        # Act
        result = complete_phase_command(
            story_id="STORY-001",
            phase_id="02",
            checkpoint_passed=True,
            project_root=str(temp_project_dir)
        )

        # Assert
        assert result == EXIT_CODE_PROCEED

        # Verify phase is completed
        updated_state = json.loads(state_file.read_text())
        assert updated_state["phases"]["02"]["status"] == "completed"

    def test_complete_phase_requires_all_subagents(self, temp_project_dir, incomplete_phase_state):
        """
        Scenario: complete-phase blocked when subagents missing (BR-002)
        Given: Phase missing required subagents
        When: complete-phase is called
        Then: Returns blocked
        """
        # Arrange
        state_file = temp_project_dir / "devforgeai" / "workflows" / "STORY-001-phase-state.json"
        state_file.write_text(json.dumps(incomplete_phase_state))

        # Act
        result = complete_phase_command(
            story_id="STORY-001",
            phase_id="01",
            checkpoint_passed=True,
            project_root=str(temp_project_dir)
        )

        # Assert - blocked due to missing subagents
        assert result == EXIT_CODE_BLOCKED

    def test_complete_phase_requires_checkpoint_passed(self, temp_project_dir, phase_state_fixture):
        """
        Scenario: complete-phase blocked when checkpoint failed (BR-003)
        Given: checkpoint_passed=False
        When: complete-phase is called
        Then: Returns blocked
        """
        # Arrange
        state_file = temp_project_dir / "devforgeai" / "workflows" / "STORY-001-phase-state.json"
        state_file.write_text(json.dumps(phase_state_fixture))

        # Act
        result = complete_phase_command(
            story_id="STORY-001",
            phase_id="01",
            checkpoint_passed=False,
            project_root=str(temp_project_dir)
        )

        # Assert - blocked because checkpoint not passed
        assert result == EXIT_CODE_BLOCKED

    def test_complete_phase_errors_on_missing_state_file(self, temp_project_dir):
        """
        Scenario: complete-phase returns error when state file missing
        Given: Story ID with no state file
        When: complete-phase is called
        Then: Exit code 2 is returned (error)
        """
        # Act
        result = complete_phase_command(
            story_id="STORY-999",
            phase_id="01",
            checkpoint_passed=True,
            project_root=str(temp_project_dir)
        )

        # Assert
        assert result == EXIT_CODE_ERROR

    def test_complete_phase_advances_current_phase(self, temp_project_dir, phase_state_fixture):
        """
        Scenario: complete-phase advances current_phase pointer
        Given: current_phase is "02"
        When: complete-phase completes phase "02"
        Then: current_phase in state becomes "03"
        """
        # Arrange
        phase_state_fixture["current_phase"] = "02"
        phase_state_fixture["phases"]["02"]["subagents_invoked"] = ["test-automator"]
        state_file = temp_project_dir / "devforgeai" / "workflows" / "STORY-001-phase-state.json"
        state_file.write_text(json.dumps(phase_state_fixture))

        # Act
        result = complete_phase_command(
            story_id="STORY-001",
            phase_id="02",
            checkpoint_passed=True,
            project_root=str(temp_project_dir)
        )

        # Assert
        assert result == EXIT_CODE_PROCEED

        # Verify phase advanced
        updated_state = json.loads(state_file.read_text())
        assert updated_state["current_phase"] == "03"


# =============================================================================
# AC#6: Exit Codes Enable External Enforcement
# =============================================================================


class TestExitCodeEnforcement:
    """Tests for AC#6: Exit codes enable external enforcement."""

    def test_exit_code_zero_allows_progression(self, temp_project_dir, phase_state_fixture):
        """
        Scenario: exit code 0 signals OK to proceed
        Given: All validations pass
        When: phase-check is called
        Then: Exit code is exactly 0
        """
        # Arrange
        state_file = temp_project_dir / "devforgeai" / "workflows" / "STORY-001-phase-state.json"
        state_file.write_text(json.dumps(phase_state_fixture))

        # Act
        result = phase_check_command(
            story_id="STORY-001",
            from_phase="01",
            to_phase="02",
            project_root=str(temp_project_dir)
        )

        # Assert
        assert result == 0, "Exit code 0 required for successful progression"

    def test_exit_code_one_blocks_progression(self, temp_project_dir, incomplete_phase_state):
        """
        Scenario: exit code 1 signals BLOCKED - do not proceed
        Given: Phase incomplete
        When: phase-check is called
        Then: Exit code is 1
        """
        # Arrange
        state_file = temp_project_dir / "devforgeai" / "workflows" / "STORY-001-phase-state.json"
        state_file.write_text(json.dumps(incomplete_phase_state))

        # Act
        result = phase_check_command(
            story_id="STORY-001",
            from_phase="01",
            to_phase="02",
            project_root=str(temp_project_dir)
        )

        # Assert
        assert result == 1, "Exit code 1 required to block progression"

    def test_exit_code_two_signals_error(self, temp_project_dir):
        """
        Scenario: exit code 2 signals ERROR - state file invalid
        Given: State file missing
        When: phase-check is called
        Then: Exit code is 2
        """
        # Act
        result = phase_check_command(
            story_id="STORY-999",
            from_phase="01",
            to_phase="02",
            project_root=str(temp_project_dir)
        )

        # Assert
        assert result == 2, "Exit code 2 required for error conditions"

    def test_exit_codes_only_0_1_2(self, temp_project_dir, phase_state_fixture):
        """
        Scenario: All commands return exit codes from set {0, 1, 2}
        Given: Various conditions
        When: Commands are executed
        Then: Exit code is always 0, 1, or 2
        """
        # Arrange
        state_file = temp_project_dir / "devforgeai" / "workflows" / "STORY-001-phase-state.json"
        state_file.write_text(json.dumps(phase_state_fixture))

        valid_codes = {0, 1, 2}

        # Act & Assert
        result = phase_check_command(
            story_id="STORY-001",
            from_phase="01",
            to_phase="02",
            project_root=str(temp_project_dir)
        )
        assert result in valid_codes, f"Exit code {result} not in allowed set {valid_codes}"

    def test_exit_code_blocking_hooks(self, temp_project_dir, incomplete_phase_state):
        """
        Scenario: exit code 1 can be used in shell conditionals to block workflow
        Given: Phase incomplete
        When: phase-check returns exit code
        Then: Non-zero exit code blocks shell conditional
        """
        # Arrange
        state_file = temp_project_dir / "devforgeai" / "workflows" / "STORY-001-phase-state.json"
        state_file.write_text(json.dumps(incomplete_phase_state))

        # Act
        result = phase_check_command(
            story_id="STORY-001",
            from_phase="01",
            to_phase="02",
            project_root=str(temp_project_dir)
        )

        # Assert
        assert result != 0, "Non-zero exit code blocks shell conditional"


# =============================================================================
# Edge Cases and Error Conditions
# =============================================================================


class TestEdgeCases:
    """Edge cases and error conditions."""

    def test_story_id_validation_format(self):
        """Test story ID must match STORY-XXX pattern exactly."""
        invalid_ids = ["STORY-01", "STORY-0001", "story-001", "STORY_001", "STRY-001", ""]

        for invalid_id in invalid_ids:
            exit_code, msg = validate_phase_check(invalid_id, "01", "02", "/tmp")
            assert exit_code == EXIT_CODE_ERROR, f"Should reject {invalid_id}"

    def test_phase_id_validation_range(self, temp_project_dir, phase_state_fixture):
        """Test phase ID must be 01-10."""
        state_file = temp_project_dir / "devforgeai" / "workflows" / "STORY-001-phase-state.json"
        state_file.write_text(json.dumps(phase_state_fixture))

        invalid_phases = ["00", "11"]

        for invalid_phase in invalid_phases:
            result = phase_check_command(
                story_id="STORY-001",
                from_phase=invalid_phase,
                to_phase="02",
                project_root=str(temp_project_dir)
            )
            assert result == EXIT_CODE_ERROR, f"Should reject phase {invalid_phase}"

    def test_corrupt_state_file_json(self, temp_project_dir):
        """
        Scenario: Corrupted JSON in state file returns error
        Given: State file contains invalid JSON
        When: phase-check is called
        Then: Returns error (exit code 2)
        """
        # Arrange
        state_file = temp_project_dir / "devforgeai" / "workflows" / "STORY-001-phase-state.json"
        state_file.write_text("{invalid json}")

        # Act
        result = phase_check_command(
            story_id="STORY-001",
            from_phase="01",
            to_phase="02",
            project_root=str(temp_project_dir)
        )

        # Assert
        assert result == EXIT_CODE_ERROR

    def test_phase_order_validation(self, temp_project_dir, phase_state_fixture):
        """
        Scenario: Cannot skip phases (must complete in order)
        Given: Valid state
        When: Trying to transition from "01" to "03" (skip "02")
        Then: Returns blocked
        """
        # Arrange
        state_file = temp_project_dir / "devforgeai" / "workflows" / "STORY-001-phase-state.json"
        state_file.write_text(json.dumps(phase_state_fixture))

        # Act
        result = phase_check_command(
            story_id="STORY-001",
            from_phase="01",
            to_phase="03",  # Skipping phase 02
            project_root=str(temp_project_dir)
        )

        # Assert - blocked for skipping
        assert result == EXIT_CODE_BLOCKED

    def test_empty_state_file(self, temp_project_dir):
        """
        Scenario: Empty state file is treated as invalid
        Given: State file exists but is empty
        When: phase-check is called
        Then: Returns error (exit code 2)
        """
        # Arrange
        state_file = temp_project_dir / "devforgeai" / "workflows" / "STORY-001-phase-state.json"
        state_file.write_text("")

        # Act
        result = phase_check_command(
            story_id="STORY-001",
            from_phase="01",
            to_phase="02",
            project_root=str(temp_project_dir)
        )

        # Assert
        assert result == EXIT_CODE_ERROR

    def test_phase_with_no_required_subagents(self):
        """
        Scenario: Phases with no required subagents (e.g., Phase 07, 08, 09)
        Given: Phase with empty subagents_required list
        When: validate_subagents_invoked is called
        Then: Returns True (no subagents required = valid)
        """
        # Arrange
        required = []
        invoked = []

        # Act
        result = validate_subagents_invoked(required, invoked)

        # Assert
        assert result is True

    def test_multiple_invocations_same_subagent(self, temp_project_dir, phase_state_fixture):
        """
        Scenario: record-subagent called multiple times with same subagent
        Given: Subagent already in list
        When: record-subagent called again
        Then: List contains no duplicates (idempotent)
        """
        # Arrange
        phase_state_fixture["phases"]["02"]["subagents_invoked"] = ["test-automator"]
        state_file = temp_project_dir / "devforgeai" / "workflows" / "STORY-001-phase-state.json"
        state_file.write_text(json.dumps(phase_state_fixture))

        # Act - call twice
        result1 = record_subagent_command(
            story_id="STORY-001",
            phase_id="02",
            subagent_name="test-automator",
            project_root=str(temp_project_dir)
        )
        result2 = record_subagent_command(
            story_id="STORY-001",
            phase_id="02",
            subagent_name="test-automator",
            project_root=str(temp_project_dir)
        )

        # Assert - both succeed, no duplicates
        assert result1 == EXIT_CODE_PROCEED
        assert result2 == EXIT_CODE_PROCEED

        updated_state = json.loads(state_file.read_text())
        count = updated_state["phases"]["02"]["subagents_invoked"].count("test-automator")
        assert count == 1


# =============================================================================
# Performance and Non-Functional Requirements
# =============================================================================


class TestNonFunctionalRequirements:
    """Non-functional requirement tests."""

    def test_phase_check_performance_under_30ms(self, temp_project_dir, phase_state_fixture):
        """
        NFR: phase-check command completes in <30ms
        Given: Valid state file exists
        When: phase-check is executed
        Then: Command completes within 30ms
        """
        # Arrange
        state_file = temp_project_dir / "devforgeai" / "workflows" / "STORY-001-phase-state.json"
        state_file.write_text(json.dumps(phase_state_fixture))

        # Act
        start_time = time.time()
        result = phase_check_command(
            story_id="STORY-001",
            from_phase="01",
            to_phase="02",
            project_root=str(temp_project_dir)
        )
        elapsed_ms = (time.time() - start_time) * 1000

        # Assert
        assert elapsed_ms < 30, f"Command took {elapsed_ms:.2f}ms, should be <30ms"

    def test_error_messages_are_specific_and_actionable(self, temp_project_dir):
        """
        NFR: All validation errors include specific reason
        Given: Error condition (missing state file)
        When: validate_phase_check is called
        Then: Error message is specific
        """
        # Act
        exit_code, message = validate_phase_check(
            story_id="STORY-999",
            from_phase="01",
            to_phase="02",
            project_root=str(temp_project_dir)
        )

        # Assert
        assert exit_code == EXIT_CODE_ERROR
        assert "STORY-999" in message or "not found" in message.lower()


# =============================================================================
# Integration with PhaseState Module
# =============================================================================


class TestIntegrationWithPhaseState:
    """Integration tests with the PhaseState module from STORY-148."""

    def test_validate_phase_check_integration(self, temp_project_dir, phase_state_fixture):
        """
        Scenario: validate_phase_check uses PhaseState to read state
        Given: PhaseState module is available and state file exists
        When: validate_phase_check is called
        Then: Correctly validates phase and returns appropriate status
        """
        # Arrange
        state_file = temp_project_dir / "devforgeai" / "workflows" / "STORY-001-phase-state.json"
        state_file.write_text(json.dumps(phase_state_fixture))

        # Act
        result = validate_phase_check(
            story_id="STORY-001",
            from_phase="01",
            to_phase="02",
            project_root=str(temp_project_dir)
        )

        # Assert - returns tuple (exit_code, message)
        assert isinstance(result, tuple)
        assert len(result) == 2
        assert result[0] == EXIT_CODE_PROCEED

    def test_record_subagent_uses_phase_state(self, temp_project_dir, phase_state_fixture):
        """
        Scenario: record_subagent_command delegates to PhaseState.record_subagent()
        Given: State file exists
        When: record_subagent_command is called
        Then: Subagent is recorded in state file
        """
        # Arrange
        state_file = temp_project_dir / "devforgeai" / "workflows" / "STORY-001-phase-state.json"
        state_file.write_text(json.dumps(phase_state_fixture))

        # Act
        result = record_subagent_command(
            story_id="STORY-001",
            phase_id="02",
            subagent_name="test-automator",
            project_root=str(temp_project_dir)
        )

        # Assert
        assert result == EXIT_CODE_PROCEED
        updated = json.loads(state_file.read_text())
        assert "test-automator" in updated["phases"]["02"]["subagents_invoked"]

    def test_complete_phase_uses_phase_state(self, temp_project_dir, phase_state_fixture):
        """
        Scenario: complete_phase_command delegates to PhaseState.complete_phase()
        Given: State file exists with all subagents
        When: complete_phase_command is called
        Then: Phase is marked complete in state file
        """
        # Arrange
        phase_state_fixture["current_phase"] = "02"
        phase_state_fixture["phases"]["02"]["subagents_invoked"] = ["test-automator"]
        state_file = temp_project_dir / "devforgeai" / "workflows" / "STORY-001-phase-state.json"
        state_file.write_text(json.dumps(phase_state_fixture))

        # Act
        result = complete_phase_command(
            story_id="STORY-001",
            phase_id="02",
            checkpoint_passed=True,
            project_root=str(temp_project_dir)
        )

        # Assert
        assert result == EXIT_CODE_PROCEED
        updated = json.loads(state_file.read_text())
        assert updated["phases"]["02"]["status"] == "completed"


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
