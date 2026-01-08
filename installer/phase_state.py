"""
STORY-148: Phase State File Module

Python module for TDD phase state tracking via JSON files.
Provides creation, reading, updating, and archiving of phase state files
for the Phase Execution Enforcement System.

Usage:
    from installer.phase_state import PhaseState

    ps = PhaseState(project_root=Path("/path/to/project"))
    state = ps.create("STORY-001")
    ps.record_subagent("STORY-001", "01", "git-validator")
    ps.complete_phase("STORY-001", "01", checkpoint_passed=True)
    current = ps.read("STORY-001")
    ps.archive("STORY-001")
"""

import fcntl
import json
import logging
import os
import re
import shutil
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional, Tuple

# Configure logging
logger = logging.getLogger(__name__)

# =============================================================================
# Configuration Constants
# =============================================================================

WORKFLOWS_DIR = "devforgeai/workflows"
ARCHIVE_DIR = "devforgeai/workflows/completed"
LOCK_TIMEOUT = 5  # Max seconds to wait for file lock
FILE_PATTERN = "{story_id}-phase-state.json"
STORY_ID_PATTERN = re.compile(r"^STORY-\d{3}$")

# Valid phase IDs
VALID_PHASES = [f"{i:02d}" for i in range(1, 11)]

# Valid phase statuses
VALID_STATUSES = ["pending", "in_progress", "completed", "skipped"]

# Observation categories (STORY-188: AC-4) - Single source of truth
VALID_CATEGORIES = ["friction", "gap", "success", "pattern"]

# Observation severities (STORY-188: AC-5) - Single source of truth
VALID_SEVERITIES = ["low", "medium", "high"]

# Required subagents per phase (from plan)
REQUIRED_SUBAGENTS = {
    1: ["git-validator", "tech-stack-detector"],
    2: ["test-automator"],
    3: [],  # backend-architect OR frontend-developer, context-validator
    4: ["refactoring-specialist", "code-reviewer"],
    5: ["integration-tester"],
    6: [],  # deferral-validator (conditional)
    7: [],  # none - file operations
    8: [],  # none - git operations
    9: [],  # none - hook invocation
    10: ["dev-result-interpreter"]
}


# =============================================================================
# Custom Exceptions
# =============================================================================


class PhaseStateError(Exception):
    """Base exception for phase state errors."""
    pass


class PhaseNotFoundError(PhaseStateError):
    """Raised when an invalid phase_id is provided."""

    def __init__(self, phase_id: str):
        self.phase_id = phase_id
        super().__init__(
            f"Invalid phase_id: '{phase_id}'. Valid phases: {VALID_PHASES}"
        )


class StateFileCorruptionError(PhaseStateError):
    """Raised when a state file contains invalid JSON or is corrupted."""

    def __init__(self, story_id: str, original_error: str):
        self.story_id = story_id
        self.original_error = original_error
        super().__init__(
            f"State file for {story_id} is corrupted: {original_error}. "
            "Recovery: Delete the corrupted file and re-run /dev to start fresh, "
            "or manually fix the JSON syntax."
        )


class IncompleteWorkflowError(PhaseStateError):
    """Raised when trying to archive a workflow with pending phases."""

    def __init__(self, story_id: str, pending_phases: List[str]):
        self.story_id = story_id
        self.pending_phases = pending_phases
        super().__init__(
            f"Cannot archive {story_id}: phases still pending: {pending_phases}. "
            "Complete all phases before archiving."
        )


class PhaseTransitionError(PhaseStateError):
    """Raised when attempting an invalid phase transition."""

    def __init__(self, story_id: str, current_phase: str, attempted_phase: str):
        self.story_id = story_id
        self.current_phase = current_phase
        self.attempted_phase = attempted_phase
        super().__init__(
            f"Invalid phase transition for {story_id}: "
            f"current phase is '{current_phase}', cannot complete phase '{attempted_phase}'. "
            "Phases must be completed sequentially."
        )


class LockTimeoutError(PhaseStateError):
    """Raised when file lock cannot be acquired within timeout."""

    def __init__(self, file_path: str, timeout: int):
        self.file_path = file_path
        self.timeout = timeout
        super().__init__(
            f"Could not acquire lock on {file_path} within {timeout} seconds. "
            "Another process may be writing to this file."
        )


# =============================================================================
# PhaseState Class
# =============================================================================


class PhaseState:
    """
    Manages TDD phase state files for development workflow tracking.

    State files are stored as JSON in devforgeai/workflows/STORY-XXX-phase-state.json.
    Provides thread-safe operations via file locking.

    Attributes:
        project_root: Path to the project root directory
        workflows_dir: Path to the workflows directory
        archive_dir: Path to the completed workflows archive
    """

    def __init__(self, project_root: Path):
        """
        Initialize PhaseState manager.

        Args:
            project_root: Path to the project root directory.
        """
        self.project_root = Path(project_root)
        self.workflows_dir = self.project_root / WORKFLOWS_DIR
        self.archive_dir = self.project_root / ARCHIVE_DIR

    def _get_state_path(self, story_id: str) -> Path:
        """Get the path to a state file for a story."""
        return self.workflows_dir / FILE_PATTERN.format(story_id=story_id)

    def _validate_story_id(self, story_id: str) -> None:
        """
        Validate story_id matches STORY-XXX pattern.

        Args:
            story_id: The story identifier to validate.

        Raises:
            ValueError: If story_id doesn't match pattern.
        """
        if not STORY_ID_PATTERN.match(story_id):
            raise ValueError(
                f"Invalid story_id: '{story_id}'. "
                f"Must match pattern STORY-XXX (e.g., STORY-001)"
            )

    def _validate_phase_id(self, phase_id: str) -> None:
        """
        Validate phase_id is a valid phase.

        Args:
            phase_id: The phase identifier to validate.

        Raises:
            PhaseNotFoundError: If phase_id is not valid.
        """
        if phase_id not in VALID_PHASES:
            raise PhaseNotFoundError(phase_id)

    def _ensure_directories(self) -> None:
        """Ensure workflows directories exist."""
        self.workflows_dir.mkdir(parents=True, exist_ok=True)
        self.archive_dir.mkdir(parents=True, exist_ok=True)

    def _get_timestamp(self) -> str:
        """Get current UTC timestamp in ISO-8601 format."""
        return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")

    def _acquire_lock(self, file_path: Path, timeout: int = LOCK_TIMEOUT) -> int:
        """
        Acquire an exclusive lock on a file.

        Args:
            file_path: Path to the file to lock.
            timeout: Max seconds to wait for lock.

        Returns:
            File descriptor for the locked file.

        Raises:
            LockTimeoutError: If lock cannot be acquired within timeout.
        """
        lock_path = file_path.with_suffix(".lock")

        # Create lock file if it doesn't exist
        lock_path.touch(exist_ok=True)

        fd = os.open(str(lock_path), os.O_RDWR)
        start_time = datetime.now()

        while True:
            try:
                fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
                return fd
            except (BlockingIOError, OSError):
                elapsed = (datetime.now() - start_time).total_seconds()
                if elapsed >= timeout:
                    os.close(fd)
                    raise LockTimeoutError(str(file_path), timeout)
                # Brief sleep before retry
                import time
                time.sleep(0.01)

    def _release_lock(self, fd: int) -> None:
        """Release a file lock."""
        try:
            fcntl.flock(fd, fcntl.LOCK_UN)
        finally:
            os.close(fd)

    def _atomic_write(self, file_path: Path, data: dict) -> None:
        """
        Write data atomically using temp file + rename pattern.

        Args:
            file_path: Target file path.
            data: Dictionary to write as JSON.
        """
        # Write to temp file first
        temp_fd, temp_path = tempfile.mkstemp(
            suffix=".tmp",
            dir=str(file_path.parent)
        )
        try:
            with os.fdopen(temp_fd, 'w') as f:
                json.dump(data, f, indent=2)

            # Atomic rename
            shutil.move(temp_path, str(file_path))
        except Exception:
            # Clean up temp file on error
            if os.path.exists(temp_path):
                os.unlink(temp_path)
            raise

    def _create_initial_state(self, story_id: str) -> dict:
        """
        Create initial state structure for a new workflow.

        Args:
            story_id: The story identifier.

        Returns:
            Initial state dictionary.
        """
        timestamp = self._get_timestamp()

        phases = {}
        for i in range(1, 11):
            phase_id = f"{i:02d}"
            phases[phase_id] = {
                "status": "pending",
                "subagents_required": REQUIRED_SUBAGENTS.get(i, []).copy(),
                "subagents_invoked": []
            }

        return {
            "story_id": story_id,
            "workflow_started": timestamp,
            "current_phase": "01",
            "phases": phases,
            "validation_errors": [],
            "blocking_status": False,
            "observations": []  # AC-6: Empty observations array (STORY-188)
        }

    # =========================================================================
    # Public Methods
    # =========================================================================

    def create(self, story_id: str) -> dict:
        """
        Create a new phase state file for a story.

        If a state file already exists (idempotent), returns the existing state.

        Args:
            story_id: The story identifier (e.g., "STORY-001").

        Returns:
            The created or existing state dictionary.

        Raises:
            ValueError: If story_id is invalid.
        """
        self._validate_story_id(story_id)
        self._ensure_directories()

        state_path = self._get_state_path(story_id)

        # Idempotent: return existing state if file exists (BR-004)
        if state_path.exists():
            return self.read(story_id)

        # Create new state
        state = self._create_initial_state(story_id)

        # Validate before writing
        is_valid, error = self.validate_state(state)
        if not is_valid:
            raise ValueError(f"Failed to create valid state: {error}")

        # Write with locking
        lock_fd = self._acquire_lock(state_path)
        try:
            self._atomic_write(state_path, state)
        finally:
            self._release_lock(lock_fd)

        logger.info(f"Created phase state file for {story_id}")
        return state

    def read(self, story_id: str) -> Optional[dict]:
        """
        Read the current phase state for a story.

        Args:
            story_id: The story identifier.

        Returns:
            The state dictionary, or None if file doesn't exist.

        Raises:
            StateFileCorruptionError: If JSON is invalid.
        """
        state_path = self._get_state_path(story_id)

        if not state_path.exists():
            return None

        try:
            content = state_path.read_text()
            return json.loads(content)
        except json.JSONDecodeError as e:
            raise StateFileCorruptionError(story_id, str(e))

    def record_subagent(
        self,
        story_id: str,
        phase_id: str,
        subagent_name: str
    ) -> bool:
        """
        Record a subagent invocation for a phase.

        Args:
            story_id: The story identifier.
            phase_id: The phase identifier (e.g., "01").
            subagent_name: Name of the subagent invoked.

        Returns:
            True if recorded successfully, False if state file doesn't exist.

        Raises:
            PhaseNotFoundError: If phase_id is invalid.
        """
        self._validate_phase_id(phase_id)

        state_path = self._get_state_path(story_id)

        if not state_path.exists():
            return False

        lock_fd = self._acquire_lock(state_path)
        try:
            state = self.read(story_id)
            if state is None:
                return False

            # Append subagent to list (BR-002: append-only)
            if subagent_name not in state["phases"][phase_id]["subagents_invoked"]:
                state["phases"][phase_id]["subagents_invoked"].append(subagent_name)

            # Record timestamp if not already started
            if "started_at" not in state["phases"][phase_id]:
                state["phases"][phase_id]["started_at"] = self._get_timestamp()

            self._atomic_write(state_path, state)
        finally:
            self._release_lock(lock_fd)

        logger.debug(f"Recorded subagent {subagent_name} for {story_id} phase {phase_id}")
        return True

    def add_observation(
        self,
        story_id: str,
        phase_id: str,
        category: str,
        note: str,
        severity: str = "medium"
    ) -> Optional[str]:
        """
        Add an observation to the phase state file.

        Observations capture friction, gaps, successes, and patterns
        during workflow execution for AI analysis.

        Args:
            story_id: The story identifier.
            phase_id: The phase identifier (e.g., "04").
            category: Observation category (friction, gap, success, pattern).
            note: Description of the observation.
            severity: Severity level (low, medium, high). Default: medium.

        Returns:
            The observation ID if successful, None if state file doesn't exist.

        Raises:
            PhaseNotFoundError: If phase_id is invalid.
            ValueError: If category or severity is invalid.
        """
        import uuid

        # Validate inputs
        self._validate_phase_id(phase_id)

        if category not in VALID_CATEGORIES:
            raise ValueError(
                f"Invalid category: '{category}'. "
                f"Must be one of: {VALID_CATEGORIES}"
            )

        if severity not in VALID_SEVERITIES:
            raise ValueError(
                f"Invalid severity: '{severity}'. "
                f"Must be one of: {VALID_SEVERITIES}"
            )

        if not note or not note.strip():
            raise ValueError("Observation note cannot be empty")

        state_path = self._get_state_path(story_id)

        if not state_path.exists():
            return None

        lock_fd = self._acquire_lock(state_path)
        try:
            state = self.read(story_id)
            if state is None:
                return None

            # Generate unique observation ID
            observation_id = f"obs-{phase_id}-{uuid.uuid4().hex[:8]}"

            # Create observation structure (AC-3)
            observation = {
                "id": observation_id,
                "phase": phase_id,
                "category": category,
                "note": note.strip(),
                "severity": severity,
                "timestamp": self._get_timestamp()
            }

            # Ensure observations array exists (backward compatibility)
            if "observations" not in state:
                state["observations"] = []

            # Append observation
            state["observations"].append(observation)

            self._atomic_write(state_path, state)
        finally:
            self._release_lock(lock_fd)

        logger.info(f"Added observation {observation_id} for {story_id} phase {phase_id}")
        return observation_id

    def complete_phase(
        self,
        story_id: str,
        phase_id: str,
        checkpoint_passed: bool
    ) -> bool:
        """
        Mark a phase as complete and advance to next phase.

        Args:
            story_id: The story identifier.
            phase_id: The phase identifier to complete.
            checkpoint_passed: Whether the phase checkpoint passed.

        Returns:
            True if completed successfully.

        Raises:
            PhaseTransitionError: If attempting to complete out of order.
            PhaseNotFoundError: If phase_id is invalid.
        """
        self._validate_phase_id(phase_id)

        state_path = self._get_state_path(story_id)

        if not state_path.exists():
            return False

        lock_fd = self._acquire_lock(state_path)
        try:
            state = self.read(story_id)
            if state is None:
                return False

            current_phase = state["current_phase"]

            # BR-001: Must complete current phase only (sequential order)
            if phase_id != current_phase:
                raise PhaseTransitionError(story_id, current_phase, phase_id)

            # Update phase status
            state["phases"][phase_id]["status"] = "completed"
            state["phases"][phase_id]["completed_at"] = self._get_timestamp()
            state["phases"][phase_id]["checkpoint_passed"] = checkpoint_passed

            # Advance to next phase (unless at phase 10)
            phase_num = int(phase_id)
            if phase_num < 10:
                state["current_phase"] = f"{phase_num + 1:02d}"

            # Validate before writing
            is_valid, error = self.validate_state(state)
            if not is_valid:
                raise ValueError(f"Invalid state after phase completion: {error}")

            self._atomic_write(state_path, state)
        finally:
            self._release_lock(lock_fd)

        logger.info(f"Completed phase {phase_id} for {story_id}")
        return True

    def archive(self, story_id: str) -> bool:
        """
        Archive a completed workflow's state file.

        Moves the state file to the completed/ directory.

        Args:
            story_id: The story identifier.

        Returns:
            True if archived successfully, False if file doesn't exist.

        Raises:
            IncompleteWorkflowError: If not all phases are completed.
        """
        state_path = self._get_state_path(story_id)

        if not state_path.exists():
            return False

        state = self.read(story_id)
        if state is None:
            return False

        # BR-003: Check all phases are completed
        pending_phases = []
        for phase_id, phase_data in state["phases"].items():
            if phase_data["status"] not in ["completed", "skipped"]:
                pending_phases.append(phase_id)

        if pending_phases:
            raise IncompleteWorkflowError(story_id, pending_phases)

        # Ensure archive directory exists
        self.archive_dir.mkdir(parents=True, exist_ok=True)

        # Move to archive
        archive_path = self.archive_dir / state_path.name
        shutil.move(str(state_path), str(archive_path))

        # Clean up lock file if exists
        lock_path = state_path.with_suffix(".lock")
        if lock_path.exists():
            lock_path.unlink()

        logger.info(f"Archived phase state for {story_id}")
        return True

    def validate_state(self, state: dict) -> Tuple[bool, str]:
        """
        Validate state structure before persistence.

        Checks:
        - Required fields present
        - Valid enum values for status
        - Correct types for all fields

        Args:
            state: The state dictionary to validate.

        Returns:
            Tuple of (is_valid, error_message).
        """
        # Required top-level fields
        required_fields = [
            "story_id",
            "workflow_started",
            "current_phase",
            "phases",
            "validation_errors",
            "blocking_status"
        ]

        for field in required_fields:
            if field not in state:
                return False, f"Missing required field: {field}"

        # Validate current_phase
        if state["current_phase"] not in VALID_PHASES:
            return False, f"Invalid current_phase: {state['current_phase']}"

        # Validate blocking_status type
        if not isinstance(state["blocking_status"], bool):
            return False, f"blocking_status must be boolean, got {type(state['blocking_status'])}"

        # Validate validation_errors is a list
        if not isinstance(state["validation_errors"], list):
            return False, "validation_errors must be an array"

        # Validate phases
        if not isinstance(state["phases"], dict):
            return False, "phases must be an object"

        for phase_id, phase_data in state["phases"].items():
            if "status" in phase_data:
                if phase_data["status"] not in VALID_STATUSES:
                    return False, f"Invalid status for phase {phase_id}: {phase_data['status']}"

        return True, ""
