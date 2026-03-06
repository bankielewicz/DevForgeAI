"""
PhaseState Module - Workflow Phase Tracking for DevForgeAI CLI

This module provides the PhaseState class for managing workflow phase tracking
state files during /dev workflow execution. It enforces sequential phase
execution and provides atomic, concurrent-safe file operations.

STORY-253: Create PhaseState Module in Correct Location
Source RCA: RCA-001-phase-state-module-missing.md

Usage:
    from devforgeai_cli.phase_state import PhaseState

    ps = PhaseState(project_root=Path("/path/to/project"))
    state = ps.create(story_id="STORY-001")
    state = ps.complete_phase(story_id="STORY-001", phase="01", checkpoint_passed=True)

Platform Support:
    - Windows 10+: Uses msvcrt for file locking
    - macOS 11+: Uses fcntl for file locking
    - Linux (Ubuntu/Debian/RHEL): Uses fcntl for file locking
    - WSL 1/2: Uses fcntl for file locking
"""

from __future__ import annotations

import json
import logging
import os
import re
import shutil
import tempfile
import time
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

# Platform-aware file locking imports
if os.name == 'posix':
    import fcntl
    _HAS_FCNTL = True
else:
    _HAS_FCNTL = False

if os.name == 'nt':
    try:
        import msvcrt
        _HAS_MSVCRT = True
    except ImportError:
        _HAS_MSVCRT = False
else:
    _HAS_MSVCRT = False

logger = logging.getLogger(__name__)


# =============================================================================
# Custom Exceptions
# =============================================================================


class PhaseStateError(Exception):
    """Base exception for PhaseState errors."""
    pass


class PhaseNotFoundError(PhaseStateError):
    """Raised when an invalid phase ID is provided."""

    def __init__(self, phase_id: str, message: Optional[str] = None):
        self.phase_id = phase_id
        if message is None:
            message = (
                f"Invalid phase_id: '{phase_id}'. "
                "Valid phases are '01' through '10'."
            )
        super().__init__(message)


class StateFileCorruptionError(PhaseStateError):
    """Raised when a state file contains malformed JSON."""

    def __init__(self, story_id: str, original_error: Optional[Exception] = None):
        self.story_id = story_id
        self.original_error = original_error
        message = (
            f"State file for '{story_id}' is corrupted. "
            "Recovery: Delete the file and re-run the workflow."
        )
        super().__init__(message)


class PhaseTransitionError(PhaseStateError):
    """Raised when attempting to complete phases out of order."""

    def __init__(
        self,
        story_id: str,
        current_phase: str,
        attempted_phase: str
    ):
        self.story_id = story_id
        self.current_phase = current_phase
        self.attempted_phase = attempted_phase
        message = (
            f"Cannot complete phase '{attempted_phase}' for '{story_id}'. "
            f"Current phase is '{current_phase}'. "
            "Phases must be completed sequentially."
        )
        super().__init__(message)


class LockTimeoutError(PhaseStateError):
    """Raised when file lock acquisition times out."""

    def __init__(self, file_path: Union[str, Path], timeout: float):
        self.file_path = str(file_path)
        self.timeout = timeout
        message = (
            f"Failed to acquire lock on '{file_path}' "
            f"after {timeout} seconds."
        )
        super().__init__(message)


class SubagentEnforcementError(PhaseStateError):
    """Raised when required subagents not invoked before phase completion.

    STORY-306: Subagent Enforcement in Phase State Completion
    """

    def __init__(self, story_id: str, phase: str, missing_subagents: List[str]):
        self.story_id = story_id
        self.phase = phase
        self.missing_subagents = missing_subagents
        message = (
            f"Cannot complete phase '{phase}' for '{story_id}'. "
            f"Missing required subagents: {', '.join(missing_subagents)}"
        )
        super().__init__(message)


# =============================================================================
# Required Subagents Per Phase (STORY-306)
# =============================================================================

# Tuple indicates OR logic: any one subagent in tuple satisfies requirement
# Matches SKILL.md Required Subagents Per Phase table (lines 167-181)
# =============================================================================
# QA Workflow Phase Schema (STORY-517)
# =============================================================================

# =============================================================================
# Dev Workflow Phase Schema (STORY-521)
# =============================================================================

DEV_PHASES: Dict[str, Dict[str, Any]] = {
    "01": {"steps_required": ["git_validation", "context_validation", "tech_stack_detection"], "subagents_required": ["git-validator", "tech-stack-detector"], "checkpoint_description": "Pre-flight validation complete"},
    "02": {"steps_required": ["test_generation", "test_failure_verification"], "subagents_required": ["test-automator"], "checkpoint_description": "Failing tests written (Red)"},
    "03": {"steps_required": ["implementation", "test_pass_verification"], "subagents_required": [("backend-architect", "frontend-developer"), "context-validator"], "checkpoint_description": "Tests passing (Green)"},
    "04": {"steps_required": ["refactoring", "code_review"], "subagents_required": ["refactoring-specialist", "code-reviewer"], "checkpoint_description": "Code refactored and reviewed"},
    "4.5": {"steps_required": ["ac_verification"], "subagents_required": ["ac-compliance-verifier"], "checkpoint_description": "AC verification post-refactor"},
    "05": {"steps_required": ["integration_testing"], "subagents_required": ["integration-tester"], "checkpoint_description": "Integration tests passing"},
    "5.5": {"steps_required": ["ac_verification"], "subagents_required": ["ac-compliance-verifier"], "checkpoint_description": "AC verification post-integration"},
    "06": {"steps_required": ["deferral_review"], "subagents_required": [], "checkpoint_description": "Deferral challenge complete"},
    "07": {"steps_required": ["dod_update"], "subagents_required": [], "checkpoint_description": "DoD updated"},
    "08": {"steps_required": ["git_commit"], "subagents_required": [], "checkpoint_description": "Changes committed"},
    "09": {"steps_required": ["feedback_capture"], "subagents_required": ["framework-analyst"], "checkpoint_description": "Feedback captured"},
    "10": {"steps_required": ["result_interpretation"], "subagents_required": ["dev-result-interpreter"], "checkpoint_description": "Result interpreted"},
}

QA_PHASES: Dict[str, Dict[str, Any]] = {
    "01": {"steps_required": ["setup_validation", "story_file_loading"], "subagents_required": [], "checkpoint_description": "QA setup and story loading complete"},
    "02": {"steps_required": ["constraint_validation", "anti_pattern_scan", "security_audit"], "subagents_required": ["anti-pattern-scanner", "security-auditor"], "checkpoint_description": "Constraint and security validation complete"},
    "03": {"steps_required": ["diff_regression_detection", "test_integrity_verification"], "subagents_required": [], "checkpoint_description": "Diff regression and test integrity verified"},
    "04": {"steps_required": ["coverage_analysis", "code_quality_metrics"], "subagents_required": ["coverage-analyzer", "code-quality-auditor"], "checkpoint_description": "Coverage and quality analysis complete"},
    "05": {"steps_required": ["report_generation", "result_determination"], "subagents_required": ["qa-result-interpreter"], "checkpoint_description": "QA report generated"},
    "06": {"steps_required": ["cleanup", "state_preservation"], "subagents_required": [], "checkpoint_description": "QA cleanup complete"},
}

QA_VALID_PHASES: List[str] = ["01", "02", "03", "04", "05", "06"]

# =============================================================================
# Workflow Schemas Registry (STORY-521)
# =============================================================================

WORKFLOW_SCHEMAS: Dict[str, Dict[str, Any]] = {
    "dev": {
        "phases": DEV_PHASES,
        "valid_phases": ["01", "02", "03", "04", "4.5", "05", "5.5", "06", "07", "08", "09", "10"],
    },
    "qa": {
        "phases": QA_PHASES,
        "valid_phases": ["01", "02", "03", "04", "05", "06"],
    },
}

VALID_WORKFLOWS: List[str] = list(WORKFLOW_SCHEMAS.keys())


PHASE_REQUIRED_SUBAGENTS: Dict[str, List[Union[str, tuple]]] = {
    "01": ["git-validator", "tech-stack-detector"],
    "02": ["test-automator"],
    "03": [("backend-architect", "frontend-developer"), "context-validator"],  # tuple = OR
    "04": ["refactoring-specialist", "code-reviewer"],
    "4.5": ["ac-compliance-verifier"],
    "05": ["integration-tester"],
    "5.5": ["ac-compliance-verifier"],
    "06": [],  # deferral-validator is conditional
    "07": [],  # no required subagents (file operations)
    "08": [],  # no required subagents (git operations)
    "09": ["framework-analyst"],  # RCA-027 fix
    "10": ["dev-result-interpreter"],
}


# =============================================================================
# PhaseState Class
# =============================================================================


class PhaseState:
    """
    Manages workflow phase tracking state files for DevForgeAI.

    Provides atomic, concurrent-safe operations for creating, reading,
    and updating phase state during /dev workflow execution.

    Attributes:
        project_root: Path to the project root directory
        workflows_dir: Path to the workflows directory (project_root/devforgeai/workflows)

    Example:
        >>> ps = PhaseState(project_root=Path("/my/project"))
        >>> state = ps.create(story_id="STORY-001")
        >>> print(state["current_phase"])  # "01"
    """

    # Valid phase IDs (includes decimal phases 4.5 and 5.5 for AC verification)
    VALID_PHASES: List[str] = [
        "01", "02", "03", "04", "4.5", "05", "5.5",
        "06", "07", "08", "09", "10"
    ]

    # Valid observation categories
    VALID_CATEGORIES: List[str] = ["friction", "gap", "success", "pattern"]

    # Valid observation severities
    VALID_SEVERITIES: List[str] = ["low", "medium", "high"]

    # Story ID pattern
    STORY_ID_PATTERN: re.Pattern = re.compile(r'^STORY-\d{3}$')

    # Lock timeout in seconds
    LOCK_TIMEOUT: float = 5.0

    # Maximum note length
    MAX_NOTE_LENGTH: int = 1000

    def __init__(self, project_root: Path) -> None:
        """
        Initialize PhaseState with project root directory.

        Args:
            project_root: Path to the project root directory

        Example:
            >>> ps = PhaseState(project_root=Path("/my/project"))
            >>> ps.workflows_dir
            PosixPath('/my/project/devforgeai/workflows')
        """
        self.project_root = Path(project_root)
        self.workflows_dir = self.project_root / "devforgeai" / "workflows"
        logger.debug(f"PhaseState initialized: project_root={project_root}")

    def _validate_story_id(self, story_id: str) -> None:
        """
        Validate story ID format and check for path traversal.

        Args:
            story_id: Story identifier to validate

        Raises:
            ValueError: If story_id is invalid or contains path traversal
        """
        # Check for path traversal attempts
        if '..' in story_id or '/' in story_id or '\\' in story_id:
            raise ValueError(
                f"Invalid story_id: '{story_id}'. "
                "Must match pattern STORY-XXX (e.g., STORY-001)"
            )

        # Check for null bytes (security)
        if '\x00' in story_id:
            raise ValueError(
                f"Invalid story_id: '{story_id}'. "
                "Must match pattern STORY-XXX (e.g., STORY-001)"
            )

        # Check pattern match
        if not self.STORY_ID_PATTERN.match(story_id):
            raise ValueError(
                f"Invalid story_id: '{story_id}'. "
                "Must match pattern STORY-XXX (e.g., STORY-001)"
            )

    def _validate_phase_id(self, phase_id: str) -> None:
        """
        Validate phase ID is in valid range.

        Args:
            phase_id: Phase identifier to validate

        Raises:
            PhaseNotFoundError: If phase_id is not valid
        """
        if phase_id not in self.VALID_PHASES:
            raise PhaseNotFoundError(phase_id)

    def _get_state_path(self, story_id: str) -> Path:
        """
        Get the path to the state file for a story.

        Args:
            story_id: Story identifier

        Returns:
            Path to the state file

        Example:
            >>> ps = PhaseState(project_root=Path("/project"))
            >>> ps._get_state_path("STORY-001")
            PosixPath('/project/devforgeai/workflows/STORY-001-phase-state.json')
        """
        return self.workflows_dir / f"{story_id}-phase-state.json"

    def _serialize_subagents_required(
        self, items: List[Union[str, tuple, list]]
    ) -> List[Union[str, List[str]]]:
        """
        Convert subagent requirement items to JSON-serializable form.

        Tuples represent OR-groups (any one satisfies the requirement) and
        must be converted to lists for JSON serialization.

        Args:
            items: List of subagent names (str) or OR-groups (tuple/list)

        Returns:
            List with tuples converted to lists, other items unchanged
        """
        result = []
        for item in items:
            if isinstance(item, tuple):
                result.append(list(item))
            else:
                result.append(item)
        return result

    def _create_initial_state(self, story_id: str) -> Dict[str, Any]:
        """
        Create the initial state dictionary for a new story.

        Args:
            story_id: Story identifier

        Returns:
            Initial state dictionary
        """
        now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

        phases = {}
        for phase in self.VALID_PHASES:
            # Populate subagents_required from constant (AC2 - STORY-306)
            required = self._serialize_subagents_required(
                PHASE_REQUIRED_SUBAGENTS.get(phase, [])
            )

            phases[phase] = {
                "status": "pending",
                "subagents_required": required,
                "subagents_invoked": []
            }

        return {
            "story_id": story_id,
            "current_phase": "01",
            "workflow_started": now,
            "blocking_status": False,
            "phases": phases,
            "validation_errors": [],
            "observations": []
        }

    def _acquire_lock(self, fd: int, timeout: float) -> bool:
        """
        Acquire an exclusive lock on a file descriptor.

        Uses platform-aware locking:
        - Unix (Linux/macOS): fcntl.flock with LOCK_EX | LOCK_NB
        - Windows: msvcrt.locking with LK_NBLCK
        - Fallback: No locking (last-write-wins)

        Args:
            fd: File descriptor
            timeout: Maximum time to wait for lock

        Returns:
            True if lock acquired, False if locking not available

        Raises:
            LockTimeoutError: If lock cannot be acquired within timeout
        """
        start_time = time.time()

        while True:
            elapsed = time.time() - start_time
            if elapsed >= timeout:
                raise LockTimeoutError("<file>", timeout)

            try:
                if _HAS_FCNTL:
                    fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
                    return True
                elif _HAS_MSVCRT:
                    msvcrt.locking(fd, msvcrt.LK_NBLCK, 1)
                    return True
                else:
                    # No locking available - proceed without lock
                    logger.warning("File locking not available on this platform")
                    return False
            except (IOError, OSError):
                # Lock is held by another process, wait and retry
                time.sleep(0.1)

    def _release_lock(self, fd: int) -> None:
        """
        Release a lock on a file descriptor.

        Args:
            fd: File descriptor
        """
        try:
            if _HAS_FCNTL:
                fcntl.flock(fd, fcntl.LOCK_UN)
            elif _HAS_MSVCRT:
                msvcrt.locking(fd, msvcrt.LK_UNLCK, 1)
        except (IOError, OSError):
            pass  # Ignore errors during unlock

    def _atomic_write(self, path: Path, data: Dict[str, Any]) -> None:
        """
        Write data to file atomically using temp file + rename.

        Args:
            path: Target file path
            data: Dictionary to write as JSON
        """
        # Ensure parent directory exists
        path.parent.mkdir(parents=True, exist_ok=True)

        # Write to temp file in same directory
        fd, temp_path = tempfile.mkstemp(
            dir=str(path.parent),
            suffix='.tmp',
            prefix=path.stem
        )

        try:
            with os.fdopen(fd, 'w') as f:
                json.dump(data, f, indent=2)

            # Atomic rename
            shutil.move(temp_path, str(path))

            # Set permissions (0644)
            try:
                os.chmod(str(path), 0o644)
            except OSError:
                pass  # Ignore permission errors on some platforms

        except Exception:
            # Clean up temp file on error
            if os.path.exists(temp_path):
                os.unlink(temp_path)
            raise

    def _read_state(self, path: Path) -> Dict[str, Any]:
        """
        Read and parse state file with validation.

        Args:
            path: Path to state file

        Returns:
            Parsed state dictionary

        Raises:
            StateFileCorruptionError: If JSON is malformed or empty
        """
        story_id = path.stem.replace("-phase-state", "")

        try:
            content = path.read_text()

            # Check for empty file
            if not content.strip():
                raise StateFileCorruptionError(story_id)

            state = json.loads(content)

            # Backward compatibility: ensure all VALID_PHASES exist
            # (handles state files created before decimal phases 4.5/5.5 were added)
            self._ensure_phases_exist(state)

            return state

        except json.JSONDecodeError as e:
            raise StateFileCorruptionError(story_id, e)

    def _ensure_phases_exist(self, state: Dict[str, Any]) -> None:
        """
        Ensure all VALID_PHASES have entries in the phases dictionary.

        Adds missing phase entries with default values for backward compatibility
        with state files created before decimal phases (4.5, 5.5) were added.

        Also populates empty subagents_required from PHASE_REQUIRED_SUBAGENTS
        for legacy state files (AC8 - STORY-306).

        Args:
            state: State dictionary to update in-place
        """
        phases = state.get("phases", {})
        for phase in self.VALID_PHASES:
            if phase not in phases:
                # Create new phase entry with populated subagents_required
                required = self._serialize_subagents_required(
                    PHASE_REQUIRED_SUBAGENTS.get(phase, [])
                )
                phases[phase] = {
                    "status": "pending",
                    "subagents_required": required,
                    "subagents_invoked": []
                }
            else:
                # Migrate legacy: populate empty subagents_required (AC8)
                if not phases[phase].get("subagents_required"):
                    phases[phase]["subagents_required"] = self._serialize_subagents_required(
                        PHASE_REQUIRED_SUBAGENTS.get(phase, [])
                    )

        state["phases"] = phases

    def create(self, story_id: str) -> Dict[str, Any]:
        """
        Create a new phase state file for a story (idempotent).

        If a state file already exists, returns the existing state
        without modification.

        Args:
            story_id: Story identifier (must match STORY-XXX pattern)

        Returns:
            The state dictionary (new or existing)

        Raises:
            ValueError: If story_id is invalid

        Example:
            >>> ps = PhaseState(project_root=Path("/project"))
            >>> state = ps.create("STORY-001")
            >>> state["current_phase"]
            '01'
        """
        self._validate_story_id(story_id)

        path = self._get_state_path(story_id)

        # Idempotent: return existing state if file exists
        if path.exists():
            logger.debug(f"State file already exists for {story_id}")
            return self._read_state(path)

        # Create new state
        state = self._create_initial_state(story_id)
        self._atomic_write(path, state)

        logger.info(f"Created phase state for {story_id}")
        return state

    def read(self, story_id: str) -> Optional[Dict[str, Any]]:
        """
        Read the phase state for a story.

        Args:
            story_id: Story identifier

        Returns:
            State dictionary if file exists, None otherwise

        Raises:
            ValueError: If story_id is invalid
            StateFileCorruptionError: If state file is malformed

        Example:
            >>> ps = PhaseState(project_root=Path("/project"))
            >>> state = ps.read("STORY-001")
            >>> state is None  # If file doesn't exist
            True
        """
        self._validate_story_id(story_id)

        path = self._get_state_path(story_id)

        if not path.exists():
            return None

        return self._read_state(path)

    def complete_phase(
        self,
        story_id: str,
        phase: str,
        checkpoint_passed: bool
    ) -> Dict[str, Any]:
        """
        Complete a phase with sequential enforcement.

        A phase can only be completed if it is the current phase.
        After completion, current_phase advances to the next phase
        (except at phase 10).

        Args:
            story_id: Story identifier
            phase: Phase ID to complete (must be current phase)
            checkpoint_passed: Whether the phase checkpoint passed

        Returns:
            Updated state dictionary

        Raises:
            ValueError: If story_id is invalid
            PhaseNotFoundError: If phase is invalid
            PhaseTransitionError: If phase is not current phase
            FileNotFoundError: If state file doesn't exist

        Example:
            >>> ps = PhaseState(project_root=Path("/project"))
            >>> state = ps.complete_phase("STORY-001", "01", checkpoint_passed=True)
            >>> state["current_phase"]
            '02'
        """
        self._validate_story_id(story_id)
        self._validate_phase_id(phase)

        path = self._get_state_path(story_id)

        if not path.exists():
            raise FileNotFoundError(f"State file not found for {story_id}")

        state = self._read_state(path)
        current = state["current_phase"]

        # Sequential enforcement
        if phase != current:
            raise PhaseTransitionError(story_id, current, phase)

        # Subagent enforcement (AC3, AC4, AC5, AC6 - STORY-306)
        # Skip validation when checkpoint_passed=False (escape hatch - AC5)
        if checkpoint_passed:
            required = state["phases"][phase].get("subagents_required", [])
            invoked = set(state["phases"][phase].get("subagents_invoked", []))
            missing = []

            for requirement in required:
                if isinstance(requirement, list):
                    # OR logic (AC6): any one subagent in list satisfies requirement
                    if not any(subagent_name in invoked for subagent_name in requirement):
                        missing.append(f"({' OR '.join(requirement)})")
                else:
                    # Simple requirement: subagent must be in invoked set
                    if requirement not in invoked:
                        missing.append(requirement)

            if missing:
                logger.warning(
                    f"Phase {phase} completion blocked for {story_id}: "
                    f"Missing subagents: {', '.join(missing)}"
                )
                raise SubagentEnforcementError(story_id, phase, missing)
        else:
            # Escape hatch used - log for audit trail
            logger.info(
                f"Phase {phase} completed via escape hatch for {story_id} "
                "(checkpoint_passed=False)"
            )

        # Update phase status
        now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        state["phases"][phase]["status"] = "completed"
        state["phases"][phase]["completed_at"] = now
        state["phases"][phase]["checkpoint_passed"] = checkpoint_passed

        # Advance to next phase (unless at phase 10)
        phase_idx = self.VALID_PHASES.index(phase)
        if phase_idx < len(self.VALID_PHASES) - 1:
            state["current_phase"] = self.VALID_PHASES[phase_idx + 1]

        self._atomic_write(path, state)

        logger.info(f"Completed phase {phase} for {story_id}")
        return state

    def record_subagent(
        self,
        story_id: str,
        phase: str,
        subagent: str
    ) -> Dict[str, Any]:
        """
        Record a subagent invocation for a phase (idempotent).

        If the subagent is already recorded, does nothing.
        Also sets the phase started_at timestamp if not already set.

        Args:
            story_id: Story identifier
            phase: Phase ID
            subagent: Subagent name

        Returns:
            Updated state dictionary

        Raises:
            ValueError: If story_id is invalid
            PhaseNotFoundError: If phase is invalid
            FileNotFoundError: If state file doesn't exist

        Example:
            >>> ps = PhaseState(project_root=Path("/project"))
            >>> state = ps.record_subagent("STORY-001", "02", "test-automator")
            >>> "test-automator" in state["phases"]["02"]["subagents_invoked"]
            True
        """
        self._validate_story_id(story_id)
        self._validate_phase_id(phase)

        path = self._get_state_path(story_id)

        if not path.exists():
            raise FileNotFoundError(f"State file not found for {story_id}")

        state = self._read_state(path)

        # Idempotent: only add if not already present
        if subagent not in state["phases"][phase]["subagents_invoked"]:
            state["phases"][phase]["subagents_invoked"].append(subagent)

        # Set started_at if not present
        if "started_at" not in state["phases"][phase]:
            now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
            state["phases"][phase]["started_at"] = now

        self._atomic_write(path, state)

        logger.debug(f"Recorded subagent {subagent} for {story_id} phase {phase}")
        return state

    def add_observation(
        self,
        story_id: str,
        phase_id: str,
        category: str,
        note: str,
        severity: str
    ) -> str:
        """
        Add a workflow observation.

        Args:
            story_id: Story identifier
            phase_id: Phase ID (01-10)
            category: Observation category (friction, gap, success, pattern)
            note: Observation note (1-1000 characters, non-empty)
            severity: Observation severity (low, medium, high)

        Returns:
            Generated observation ID (format: obs-{phase_id}-{8-char-hex})

        Raises:
            ValueError: If any parameter is invalid
            PhaseNotFoundError: If phase_id is invalid
            FileNotFoundError: If state file doesn't exist

        Example:
            >>> ps = PhaseState(project_root=Path("/project"))
            >>> obs_id = ps.add_observation(
            ...     story_id="STORY-001",
            ...     phase_id="04",
            ...     category="friction",
            ...     note="Test took longer than expected",
            ...     severity="medium"
            ... )
            >>> obs_id.startswith("obs-04-")
            True
        """
        self._validate_story_id(story_id)
        self._validate_phase_id(phase_id)

        # Validate category
        if category not in self.VALID_CATEGORIES:
            raise ValueError(
                f"Invalid category: '{category}'. "
                f"Valid categories: {', '.join(self.VALID_CATEGORIES)}"
            )

        # Validate severity
        if severity not in self.VALID_SEVERITIES:
            raise ValueError(
                f"Invalid severity: '{severity}'. "
                f"Valid severities: {', '.join(self.VALID_SEVERITIES)}"
            )

        # Validate note
        note = note.strip() if note else ""
        if not note:
            raise ValueError("Observation note cannot be empty")

        if len(note) > self.MAX_NOTE_LENGTH:
            raise ValueError(
                f"Observation note too long ({len(note)} chars). "
                f"Maximum length is {self.MAX_NOTE_LENGTH} characters."
            )

        path = self._get_state_path(story_id)

        if not path.exists():
            raise FileNotFoundError(f"State file not found for {story_id}")

        state = self._read_state(path)

        # Generate unique observation ID
        hex_suffix = uuid.uuid4().hex[:8]
        obs_id = f"obs-{phase_id}-{hex_suffix}"

        # Create observation object
        now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        observation = {
            "id": obs_id,
            "phase": phase_id,
            "category": category,
            "note": note,
            "severity": severity,
            "timestamp": now
        }

        state["observations"].append(observation)
        self._atomic_write(path, state)

        logger.info(f"Added observation {obs_id} for {story_id}")
        return obs_id

    # =================================================================
    # Step-Level Tracking Methods (STORY-525)
    # =================================================================

    def _get_registry_path(self) -> Path:
        """
        Get the path to the phase-steps-registry.json file.

        Returns:
            Path to the registry JSON file
        """
        return self.project_root / ".claude" / "hooks" / "phase-steps-registry.json"

    def record_step(
        self,
        story_id: str,
        phase: str,
        step_id: str
    ) -> Dict[str, Any]:
        """
        Record a step completion for a phase (idempotent).

        Appends step_id to steps_completed list in the phase data.
        If step_id already present, does nothing (no duplicates).

        Args:
            story_id: Story identifier
            phase: Phase ID
            step_id: Step identifier (e.g., "02.1")

        Returns:
            Updated state dictionary

        Raises:
            ValueError: If story_id is invalid
            PhaseNotFoundError: If phase is invalid
            FileNotFoundError: If state file doesn't exist
        """
        self._validate_story_id(story_id)
        self._validate_phase_id(phase)

        path = self._get_state_path(story_id)

        if not path.exists():
            raise FileNotFoundError(f"State file not found for {story_id}")

        state = self._read_state(path)

        # Ensure steps_completed list exists
        if "steps_completed" not in state["phases"][phase]:
            state["phases"][phase]["steps_completed"] = []

        # Idempotent: only add if not already present
        if step_id not in state["phases"][phase]["steps_completed"]:
            state["phases"][phase]["steps_completed"].append(step_id)

        self._atomic_write(path, state)

        logger.debug(f"Recorded step {step_id} for {story_id} phase {phase}")
        return state

    def validate_phase_steps(
        self,
        story_id: str,
        phase: str
    ) -> Dict[str, Any]:
        """
        Validate that all required steps for a phase are completed.

        Loads the phase-steps-registry.json to determine required steps,
        filters out conditional steps, and checks against steps_completed.

        Args:
            story_id: Story identifier
            phase: Phase ID

        Returns:
            Dict with 'status' ('PASS'|'FAIL') and 'missing_steps' (list)

        Raises:
            ValueError: If story_id is invalid
            PhaseNotFoundError: If phase is invalid
            FileNotFoundError: If state file or registry missing
            json.JSONDecodeError: If registry is malformed
        """
        self._validate_story_id(story_id)
        self._validate_phase_id(phase)

        path = self._get_state_path(story_id)

        if not path.exists():
            raise FileNotFoundError(f"State file not found for {story_id}")

        state = self._read_state(path)

        # Load registry
        registry_path = self._get_registry_path()
        if not registry_path.exists():
            raise FileNotFoundError(
                f"Registry file not found at {registry_path}"
            )

        registry_content = registry_path.read_text()
        registry = json.loads(registry_content)

        # Get steps for this phase from registry
        phase_data = registry.get(phase, {})
        steps = phase_data.get("steps", [])

        # Filter to required steps only (conditional=false)
        required_step_ids = [
            step["id"] for step in steps
            if not step.get("conditional", False)
        ]

        # Get completed steps from state
        steps_completed = state["phases"].get(phase, {}).get(
            "steps_completed", []
        )

        # Find missing
        missing = [
            sid for sid in required_step_ids
            if sid not in steps_completed
        ]

        if missing:
            return {"status": "FAIL", "missing_steps": missing}
        else:
            return {"status": "PASS", "missing_steps": []}

    # =================================================================
    # QA Workflow Methods (STORY-517)
    # =================================================================

    def _get_qa_state_path(self, story_id: str) -> Path:
        """Get the path to the QA state file for a story."""
        return self.workflows_dir / f"{story_id}-qa-phase-state.json"

    def _get_workflow_path(self, story_id: str, workflow: str) -> Path:
        """
        Get the state file path for any workflow type.

        Centralises the dev/qa/generic path selection used by
        create_workflow() and complete_workflow_phase().

        Args:
            story_id: Story identifier
            workflow: Workflow type key (e.g. "dev", "qa")

        Returns:
            Path to the workflow state file
        """
        if workflow == "dev":
            return self._get_state_path(story_id)
        if workflow == "qa":
            return self._get_qa_state_path(story_id)
        # Defense-in-depth: currently unreachable via public API because
        # create_workflow() and complete_workflow_phase() validate against
        # WORKFLOW_SCHEMAS before calling this method. Retained as path
        # traversal protection for future callers that may bypass the registry.
        if not re.match(r'^[a-z][a-z0-9_-]*$', workflow):
            raise ValueError(
                f"Invalid workflow name: '{workflow}'. "
                "Must be lowercase alphanumeric with hyphens/underscores."
            )
        return self.workflows_dir / f"{story_id}-{workflow}-phase-state.json"

    def _create_qa_initial_state(self, story_id: str) -> Dict[str, Any]:
        """Create the initial QA state dictionary."""
        now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

        phases = {}
        for phase_key in QA_VALID_PHASES:
            phase_def = QA_PHASES[phase_key]
            phases[phase_key] = {
                "status": "pending",
                "steps_required": list(phase_def["steps_required"]),
                "steps_completed": [],
                "checkpoint_passed": False,
                "subagents_required": list(phase_def["subagents_required"]),
                "subagents_invoked": [],
            }

        return {
            "story_id": story_id,
            "workflow": "qa",
            "current_phase": "00",
            "workflow_started": now,
            "blocking_status": False,
            "phases": phases,
            "validation_errors": [],
            "observations": [],
        }

    def create_qa(self, story_id: str) -> Dict[str, Any]:
        """Create a new QA phase state file for a story (idempotent)."""
        self._validate_story_id(story_id)

        path = self._get_qa_state_path(story_id)

        if path.exists():
            logger.debug(f"QA state file already exists for {story_id}")
            return self._read_state(path)

        state = self._create_qa_initial_state(story_id)
        self._atomic_write(path, state)

        logger.info(f"Created QA phase state for {story_id}")
        return state

    def complete_workflow_phase(
        self,
        story_id: str,
        workflow: str,
        phase: str,
        checkpoint_passed: bool,
    ) -> Dict[str, Any]:
        """
        Complete a phase for any workflow type using WORKFLOW_SCHEMAS.

        Generic completion method that works for dev, qa, and any future
        workflow types. Uses sequential enforcement but delegates
        subagent/step validation to workflow-specific methods.

        STORY-521: Unified workflow phase completion via registry.

        Args:
            story_id: Story identifier
            workflow: Workflow type key from WORKFLOW_SCHEMAS
            phase: Phase ID to complete
            checkpoint_passed: Whether the phase checkpoint passed

        Returns:
            Updated state dictionary

        Raises:
            ValueError: If story_id, workflow, or phase is invalid
            FileNotFoundError: If state file doesn't exist
            PhaseTransitionError: If phase is not current phase
        """
        self._validate_story_id(story_id)

        schema = WORKFLOW_SCHEMAS.get(workflow)
        if schema is None:
            raise ValueError(f"Unknown workflow: '{workflow}'")

        valid_phases = schema["valid_phases"]
        if phase not in valid_phases:
            raise PhaseNotFoundError(phase, f"Invalid {workflow} phase: '{phase}'. Valid phases: {valid_phases}")

        path = self._get_workflow_path(story_id, workflow)

        if not path.exists():
            raise FileNotFoundError(f"State file not found for {story_id} ({workflow} workflow)")

        state = self._read_state(path)
        current = state["current_phase"]

        # Sequential enforcement
        if phase != current:
            raise PhaseTransitionError(story_id, current, phase)

        # Step validation for QA workflows (STORY-517 AC2)
        # QA phases track steps_required/steps_completed; reject if incomplete
        if workflow == "qa":
            phase_data = state["phases"][phase]
            required = set(phase_data.get("steps_required", []))
            completed = set(phase_data.get("steps_completed", []))
            missing = required - completed
            if missing:
                raise ValueError(
                    f"Cannot complete {workflow} phase '{phase}' for '{story_id}'. "
                    f"Missing required steps: {', '.join(sorted(missing))}"
                )

        # Update phase status
        now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        state["phases"][phase]["status"] = "completed"
        state["phases"][phase]["completed_at"] = now
        state["phases"][phase]["checkpoint_passed"] = checkpoint_passed

        # Advance to next phase
        phase_idx = valid_phases.index(phase)
        if phase_idx < len(valid_phases) - 1:
            state["current_phase"] = valid_phases[phase_idx + 1]

        self._atomic_write(path, state)
        logger.info(f"Completed {workflow} phase {phase} for {story_id}")
        return state


    def create_workflow(self, story_id: str, workflow: str) -> Dict[str, Any]:
        """
        Create state file for any workflow type using WORKFLOW_SCHEMAS.

        STORY-521: Unified workflow creation via registry.

        Args:
            story_id: Story identifier (must match STORY-XXX pattern)
            workflow: Workflow type key from WORKFLOW_SCHEMAS

        Returns:
            The state dictionary (new or existing)

        Raises:
            ValueError: If story_id is invalid or workflow is unknown
        """
        self._validate_story_id(story_id)

        schema = WORKFLOW_SCHEMAS.get(workflow)
        if schema is None:
            raise ValueError(f"Unknown workflow: '{workflow}'")

        path = self._get_workflow_path(story_id, workflow)

        if path.exists():
            return self._read_state(path)

        # Build initial state from schema
        now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        phases = {}
        for phase_key in schema["valid_phases"]:
            phase_def = schema["phases"][phase_key]
            required = self._serialize_subagents_required(
                phase_def.get("subagents_required", [])
            )
            phases[phase_key] = {
                "status": "pending",
                "steps_required": list(phase_def.get("steps_required", [])),
                "steps_completed": [],
                "checkpoint_passed": False,
                "subagents_required": required,
                "subagents_invoked": [],
            }

        state = {
            "story_id": story_id,
            "workflow": workflow,
            "current_phase": schema["valid_phases"][0],
            "workflow_started": now,
            "blocking_status": False,
            "phases": phases,
            "validation_errors": [],
            "observations": [],
        }

        self._atomic_write(path, state)
        logger.info(f"Created {workflow} phase state for {story_id}")
        return state

    def read_qa(self, story_id: str) -> Optional[Dict[str, Any]]:
        """Read the QA phase state for a story."""
        self._validate_story_id(story_id)

        path = self._get_qa_state_path(story_id)

        if not path.exists():
            return None

        return self._read_state(path)

    # complete_qa_phase() removed — step validation now in complete_workflow_phase()
    # See STORY-517 AC2 fix. The method had zero callers after STORY-521 unification.
