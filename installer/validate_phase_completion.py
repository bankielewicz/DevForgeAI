"""
STORY-149: Phase Completion Validation Script

CLI commands for phase validation that enforce phase transitions through exit codes.
Used by Phase Execution Enforcement System (Layer 2) to BLOCK phase transitions
when subagents are skipped or checkpoints fail.

Exit Codes:
    0 - Proceed: All validations passed, transition allowed
    1 - Blocked: Previous phase incomplete (missing subagents or checkpoint failed)
    2 - Error: Invalid input (story ID, phase ID) or state file missing/corrupt

Usage:
    from installer.validate_phase_completion import (
        phase_check_command,
        record_subagent_command,
        complete_phase_command,
        validate_subagents_invoked,
        validate_checkpoint_passed,
    )

    # Check if phase transition is allowed
    exit_code = phase_check_command("STORY-001", "01", "02", "/project/root")

    # Record a subagent invocation
    exit_code = record_subagent_command("STORY-001", "01", "git-validator", "/project/root")

    # Mark phase as complete
    exit_code = complete_phase_command("STORY-001", "01", True, "/project/root")
"""

import logging
import re
from pathlib import Path
from typing import List, Tuple

from installer.phase_state import (
    PhaseState,
    PhaseNotFoundError,
    StateFileCorruptionError,
    PhaseTransitionError,
    VALID_PHASES,
)

# Configure logging
logger = logging.getLogger(__name__)

# =============================================================================
# Exit Code Constants
# =============================================================================

EXIT_CODE_PROCEED = 0   # All validations passed, transition allowed
EXIT_CODE_BLOCKED = 1   # Previous phase incomplete, blocks progression
EXIT_CODE_ERROR = 2     # Error condition (invalid input, missing file, etc.)

# Story ID validation pattern
STORY_ID_PATTERN = re.compile(r"^STORY-\d{3}$")


# =============================================================================
# Pure Validation Functions
# =============================================================================


def validate_subagents_invoked(required: List[str], invoked: List[str]) -> bool:
    """
    Validate that all required subagents were invoked.

    Superset allowed - having extra subagents beyond required is acceptable.

    Args:
        required: List of subagent names that must be invoked.
        invoked: List of subagent names that were actually invoked.

    Returns:
        True if all required subagents are in invoked list, False otherwise.

    Examples:
        >>> validate_subagents_invoked(["git-validator"], ["git-validator"])
        True
        >>> validate_subagents_invoked(["a", "b"], ["a"])
        False
        >>> validate_subagents_invoked(["a"], ["a", "b"])
        True
        >>> validate_subagents_invoked([], [])
        True
    """
    if not required:
        # No subagents required = valid (e.g., Phase 07, 08, 09)
        return True

    required_set = set(required)
    invoked_set = set(invoked)

    # All required must be present in invoked (superset OK)
    return required_set.issubset(invoked_set)


def validate_checkpoint_passed(checkpoint_passed: bool) -> bool:
    """
    Validate that checkpoint passed flag is True.

    Missing or False checkpoint_passed blocks progression.

    Args:
        checkpoint_passed: The checkpoint_passed flag from phase data.

    Returns:
        True if checkpoint_passed is True, False otherwise.

    Examples:
        >>> validate_checkpoint_passed(True)
        True
        >>> validate_checkpoint_passed(False)
        False
    """
    return checkpoint_passed is True


# =============================================================================
# Input Validation Helpers
# =============================================================================


def _validate_story_id_format(story_id: str) -> Tuple[int, str]:
    """
    Validate story ID format (STORY-XXX).

    Returns: (exit_code, message) or (0, "") if valid.
    """
    if not STORY_ID_PATTERN.match(story_id):
        return (
            EXIT_CODE_ERROR,
            f"Invalid story_id: '{story_id}'. Must match pattern STORY-XXX (e.g., STORY-001)"
        )
    return (0, "")


def _validate_phase_ids(from_phase: str, to_phase: str) -> Tuple[int, str]:
    """
    Validate phase IDs are in valid range (01-10).

    Returns: (exit_code, message) or (0, "") if valid.
    """
    if from_phase not in VALID_PHASES:
        return (
            EXIT_CODE_ERROR,
            f"Invalid from_phase: '{from_phase}'. Valid phases: {VALID_PHASES}"
        )

    if to_phase not in VALID_PHASES:
        return (
            EXIT_CODE_ERROR,
            f"Invalid to_phase: '{to_phase}'. Valid phases: {VALID_PHASES}"
        )

    return (0, "")


def _validate_phase_sequence(from_phase: str, to_phase: str) -> Tuple[int, str]:
    """
    Validate sequential phase transition (no skipping).

    Returns: (exit_code, message) or (0, "") if valid.
    """
    from_num = int(from_phase)
    to_num = int(to_phase)
    if to_num != from_num + 1:
        return (
            EXIT_CODE_BLOCKED,
            f"Cannot skip phases: from '{from_phase}' to '{to_phase}'. "
            f"Must transition to '{from_num + 1:02d}'."
        )
    return (0, "")


def _read_phase_state(story_id: str, project_root: str) -> Tuple[dict, int, str]:
    """
    Read phase state file.

    Returns: (state_dict, exit_code, message).
    If state_dict is None, exit_code/message contain error info.
    """
    try:
        ps = PhaseState(Path(project_root))
        state = ps.read(story_id)
    except StateFileCorruptionError as e:
        return (None, EXIT_CODE_ERROR, f"State file corrupted: {e}")
    except Exception as e:
        return (None, EXIT_CODE_ERROR, f"Error reading state file: {e}")

    if state is None:
        return (None, EXIT_CODE_ERROR, f"State file not found for {story_id}")

    return (state, 0, "")


def _validate_phase_completion_status(phase_data: dict, from_phase: str) -> Tuple[int, str]:
    """
    Validate that phase has completed status.

    Returns: (exit_code, message) or (0, "") if valid.
    """
    if phase_data.get("status") != "completed":
        return (
            EXIT_CODE_BLOCKED,
            f"Phase {from_phase} not complete. Current status: {phase_data.get('status', 'unknown')}"
        )
    return (0, "")


def _validate_phase_subagents(phase_data: dict, from_phase: str) -> Tuple[int, str]:
    """
    Validate all required subagents were invoked for phase.

    Returns: (exit_code, message) or (0, "") if valid.
    """
    required = phase_data.get("subagents_required", [])
    invoked = phase_data.get("subagents_invoked", [])

    if not validate_subagents_invoked(required, invoked):
        missing = set(required) - set(invoked)
        return (
            EXIT_CODE_BLOCKED,
            f"Missing subagents for phase {from_phase}: {sorted(missing)}"
        )
    return (0, "")


def _validate_phase_checkpoint(phase_data: dict, from_phase: str) -> Tuple[int, str]:
    """
    Validate that phase checkpoint passed.

    Returns: (exit_code, message) or (0, "") if valid.
    """
    checkpoint = phase_data.get("checkpoint_passed", False)
    if not validate_checkpoint_passed(checkpoint):
        return (
            EXIT_CODE_BLOCKED,
            f"Checkpoint not passed for phase {from_phase}"
        )
    return (0, "")


# =============================================================================
# Validation Functions with Messages
# =============================================================================


def validate_phase_check(
    story_id: str,
    from_phase: str,
    to_phase: str,
    project_root: str
) -> Tuple[int, str]:
    """
    Full phase validation for phase-check command.

    Validates:
    1. Story ID format (STORY-XXX)
    2. Phase ID range (01-10)
    3. State file exists and is valid
    4. Previous phase is complete (all subagents + checkpoint passed)
    5. Phase transition is sequential (no skipping)

    Args:
        story_id: The story identifier (e.g., "STORY-001").
        from_phase: The phase to transition from (e.g., "01").
        to_phase: The phase to transition to (e.g., "02").
        project_root: Path to the project root directory.

    Returns:
        Tuple of (exit_code, message) where:
        - exit_code: 0 (proceed), 1 (blocked), or 2 (error)
        - message: Human-readable status message
    """
    # Validate story ID format
    code, msg = _validate_story_id_format(story_id)
    if code != 0:
        return (code, msg)

    # Validate phase IDs
    code, msg = _validate_phase_ids(from_phase, to_phase)
    if code != 0:
        return (code, msg)

    # Validate sequential transition (no skipping)
    code, msg = _validate_phase_sequence(from_phase, to_phase)
    if code != 0:
        return (code, msg)

    # Read state file
    state, code, msg = _read_phase_state(story_id, project_root)
    if state is None:
        return (code, msg)

    # Validate previous phase (from_phase) is complete
    phase_data = state.get("phases", {}).get(from_phase, {})

    # Validate phase completion status
    code, msg = _validate_phase_completion_status(phase_data, from_phase)
    if code != 0:
        return (code, msg)

    # Validate all required subagents were invoked
    code, msg = _validate_phase_subagents(phase_data, from_phase)
    if code != 0:
        return (code, msg)

    # Validate checkpoint passed
    code, msg = _validate_phase_checkpoint(phase_data, from_phase)
    if code != 0:
        return (code, msg)

    # All validations passed
    return (EXIT_CODE_PROCEED, f"Transition allowed: {from_phase} -> {to_phase}")


# =============================================================================
# CLI Command Functions
# =============================================================================


def phase_check_command(
    story_id: str,
    from_phase: str,
    to_phase: str,
    project_root: str
) -> int:
    """
    CLI command to validate phase completion before progression.

    Args:
        story_id: The story identifier (e.g., "STORY-001").
        from_phase: The phase to transition from (e.g., "01").
        to_phase: The phase to transition to (e.g., "02").
        project_root: Path to the project root directory.

    Returns:
        Exit code: 0 (proceed), 1 (blocked), or 2 (error).
    """
    exit_code, message = validate_phase_check(story_id, from_phase, to_phase, project_root)
    logger.info(f"phase-check {story_id} --from={from_phase} --to={to_phase}: {message}")
    return exit_code


def record_subagent_command(
    story_id: str,
    phase_id: str,
    subagent_name: str,
    project_root: str
) -> int:
    """
    CLI command to record a subagent invocation for a phase.

    Appends subagent to the phase's subagents_invoked list.
    Idempotent: recording same subagent twice has no effect.

    Args:
        story_id: The story identifier (e.g., "STORY-001").
        phase_id: The phase identifier (e.g., "01").
        subagent_name: Name of the subagent to record.
        project_root: Path to the project root directory.

    Returns:
        Exit code: 0 (success) or 2 (error).
    """
    # Validate story ID format
    if not STORY_ID_PATTERN.match(story_id):
        logger.error(f"Invalid story_id: '{story_id}'")
        return EXIT_CODE_ERROR

    # Validate phase ID
    if phase_id not in VALID_PHASES:
        logger.error(f"Invalid phase_id: '{phase_id}'")
        return EXIT_CODE_ERROR

    try:
        ps = PhaseState(Path(project_root))
        success = ps.record_subagent(story_id, phase_id, subagent_name)

        if not success:
            logger.error(f"State file not found for {story_id}")
            return EXIT_CODE_ERROR

        logger.info(f"Recorded subagent {subagent_name} for {story_id} phase {phase_id}")
        return EXIT_CODE_PROCEED

    except PhaseNotFoundError as e:
        logger.error(f"Invalid phase: {e}")
        return EXIT_CODE_ERROR
    except StateFileCorruptionError as e:
        logger.error(f"State file corrupted: {e}")
        return EXIT_CODE_ERROR
    except Exception as e:
        logger.error(f"Error recording subagent: {e}")
        return EXIT_CODE_ERROR


def _validate_inputs_for_phase_completion(
    story_id: str,
    phase_id: str,
    checkpoint_passed: bool
) -> int:
    """
    Validate inputs before attempting phase completion.

    Returns EXIT_CODE_ERROR (2) or EXIT_CODE_BLOCKED (1) if invalid, else 0.
    """
    if not STORY_ID_PATTERN.match(story_id):
        logger.error(f"Invalid story_id: '{story_id}'")
        return EXIT_CODE_ERROR

    if phase_id not in VALID_PHASES:
        logger.error(f"Invalid phase_id: '{phase_id}'")
        return EXIT_CODE_ERROR

    if not checkpoint_passed:
        logger.warning(f"Checkpoint not passed for {story_id} phase {phase_id}")
        return EXIT_CODE_BLOCKED

    return 0


def _verify_phase_subagents_for_completion(
    story_id: str,
    phase_id: str,
    state: dict
) -> int:
    """
    Verify all required subagents invoked before allowing completion.

    Returns EXIT_CODE_BLOCKED (1) if missing, else 0.
    """
    phase_data = state.get("phases", {}).get(phase_id, {})
    required = phase_data.get("subagents_required", [])
    invoked = phase_data.get("subagents_invoked", [])

    if not validate_subagents_invoked(required, invoked):
        missing = set(required) - set(invoked)
        logger.warning(f"Missing subagents for {story_id} phase {phase_id}: {sorted(missing)}")
        return EXIT_CODE_BLOCKED

    return 0


def _execute_phase_completion(
    story_id: str,
    phase_id: str,
    checkpoint_passed: bool,
    project_root: str
) -> int:
    """
    Execute phase completion in PhaseState.

    Returns EXIT_CODE_PROCEED (0) or EXIT_CODE_ERROR (2).
    """
    try:
        ps = PhaseState(Path(project_root))
        success = ps.complete_phase(story_id, phase_id, checkpoint_passed)

        if not success:
            logger.error(f"Failed to complete phase {phase_id} for {story_id}")
            return EXIT_CODE_ERROR

        logger.info(f"Completed phase {phase_id} for {story_id}")
        return EXIT_CODE_PROCEED

    except PhaseNotFoundError as e:
        logger.error(f"Invalid phase: {e}")
        return EXIT_CODE_ERROR
    except PhaseTransitionError as e:
        logger.error(f"Invalid phase transition: {e}")
        return EXIT_CODE_BLOCKED
    except StateFileCorruptionError as e:
        logger.error(f"State file corrupted: {e}")
        return EXIT_CODE_ERROR
    except Exception as e:
        logger.error(f"Error completing phase: {e}")
        return EXIT_CODE_ERROR


def complete_phase_command(
    story_id: str,
    phase_id: str,
    checkpoint_passed: bool,
    project_root: str
) -> int:
    """
    CLI command to mark a phase as complete.

    Updates phase status to "completed", records timestamp, and advances
    current_phase pointer.

    Args:
        story_id: The story identifier (e.g., "STORY-001").
        phase_id: The phase identifier to complete (e.g., "01").
        checkpoint_passed: Whether the phase checkpoint passed.
        project_root: Path to the project root directory.

    Returns:
        Exit code: 0 (success), 1 (blocked), or 2 (error).
    """
    # Validate inputs
    result = _validate_inputs_for_phase_completion(story_id, phase_id, checkpoint_passed)
    if result != 0:
        return result

    try:
        ps = PhaseState(Path(project_root))

        # Read state to check subagents before completing
        state = ps.read(story_id)
        if state is None:
            logger.error(f"State file not found for {story_id}")
            return EXIT_CODE_ERROR

        # Verify all required subagents were invoked (BR-002)
        result = _verify_phase_subagents_for_completion(story_id, phase_id, state)
        if result != 0:
            return result

        # Complete the phase
        return _execute_phase_completion(story_id, phase_id, checkpoint_passed, project_root)

    except Exception as e:
        logger.error(f"Unexpected error completing phase: {e}")
        return EXIT_CODE_ERROR


# =============================================================================
# ValidatePhaseCompletion Class (for OOP interface)
# =============================================================================


class ValidatePhaseCompletion:
    """
    Object-oriented interface for phase validation commands.

    Wraps the functional commands with an instance-based API.
    """

    def __init__(self, project_root: str):
        """
        Initialize ValidatePhaseCompletion.

        Args:
            project_root: Path to the project root directory.
        """
        self.project_root = project_root
        self.phase_state = PhaseState(Path(project_root))

    def phase_check(
        self,
        story_id: str,
        from_phase: str,
        to_phase: str
    ) -> int:
        """Check if phase transition is allowed."""
        return phase_check_command(story_id, from_phase, to_phase, self.project_root)

    def record_subagent(
        self,
        story_id: str,
        phase_id: str,
        subagent_name: str
    ) -> int:
        """Record a subagent invocation."""
        return record_subagent_command(story_id, phase_id, subagent_name, self.project_root)

    def complete_phase(
        self,
        story_id: str,
        phase_id: str,
        checkpoint_passed: bool = True
    ) -> int:
        """Mark a phase as complete."""
        return complete_phase_command(story_id, phase_id, checkpoint_passed, self.project_root)
