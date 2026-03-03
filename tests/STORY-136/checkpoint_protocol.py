"""
File-Based Checkpoint Protocol Implementation for STORY-136
Implements checkpoint lifecycle management for ideation sessions.

This module provides:
- CheckpointService: Main orchestrator for checkpoint lifecycle
- SessionIdGenerator: UUID v4 session ID generation
- TimestampGenerator: ISO 8601 timestamp generation
- Validators: Session ID, Timestamp, Phase, Complexity, Path, Checkpoint
- Utilities: SessionIdExtractor, TimestampParser, ResumeService, YamlValidator, SecretScanner

Business Rules (from tech-stack.md):
- BR-001: Use Write tool ONLY (no Bash for file ops)
- BR-002: Path MUST be devforgeai/temp/.ideation-checkpoint-{session_id}.yaml
- BR-003: Session ID generated once at session start and reused
- BR-004: Write failures MUST NOT crash session (graceful degradation)
"""

import re
import uuid
import json
from datetime import datetime, timezone
from typing import Dict, Any, Optional

import yaml


# ============================================================================
# Session ID Generation and Validation
# ============================================================================

class SessionIdGenerator:
    """Generates UUID v4 session identifiers for checkpoint correlation."""

    def generate(self) -> str:
        """
        Generate a unique UUID v4 session ID.

        Returns:
            str: UUID v4 format string (e.g., "550e8400-e29b-41d4-a716-446655440000")
        """
        return str(uuid.uuid4())


class SessionIdValidator:
    """Validates UUID v4 format for session IDs."""

    UUID_PATTERN = re.compile(
        r'^[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}$',
        re.IGNORECASE
    )

    def validate(self, session_id: str) -> None:
        """
        Validate session ID format (UUID v4).

        Args:
            session_id: String to validate

        Raises:
            ValueError: If session_id is not valid UUID v4
        """
        if not session_id:
            raise ValueError("session_id cannot be empty")

        # Normalize to lowercase for pattern matching
        session_id_lower = session_id.lower()

        if not self.UUID_PATTERN.match(session_id_lower):
            raise ValueError(f"Invalid UUID format: {session_id}")

        # Parse to verify it's a valid UUID v4
        try:
            parsed = uuid.UUID(session_id)
            if parsed.version != 4:
                raise ValueError(f"UUID must be version 4, got version {parsed.version}")
        except ValueError as e:
            raise ValueError(f"Invalid session_id: {e}")


class SessionIdExtractor:
    """Extracts session ID from checkpoint filename."""

    FILENAME_PATTERN = re.compile(
        r'\.ideation-checkpoint-([a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})\.yaml$',
        re.IGNORECASE
    )

    def extract_from_filename(self, filename: str) -> str:
        """
        Extract session ID from checkpoint filename.

        Args:
            filename: Checkpoint filename like '.ideation-checkpoint-{uuid}.yaml'

        Returns:
            str: Extracted session ID (UUID)

        Raises:
            ValueError: If filename format is invalid
        """
        match = self.FILENAME_PATTERN.search(filename)
        if not match:
            raise ValueError(f"Cannot extract session_id from filename: {filename}")
        return match.group(1)


# ============================================================================
# Timestamp Generation and Validation
# ============================================================================

class TimestampGenerator:
    """Generates ISO 8601 timestamps with millisecond precision."""

    def generate(self) -> str:
        """
        Generate current timestamp in ISO 8601 format.

        Returns:
            str: Timestamp in format YYYY-MM-DDTHH:MM:SS.fffZ
        """
        now = datetime.now(timezone.utc)
        # Format: YYYY-MM-DDTHH:MM:SS.fffZ (fff = milliseconds, Z = UTC)
        return now.strftime("%Y-%m-%dT%H:%M:%S.") + f"{now.microsecond // 1000:03d}Z"


class TimestampValidator:
    """Validates ISO 8601 timestamp format with milliseconds and Z suffix."""

    TIMESTAMP_PATTERN = re.compile(
        r'^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{3}Z$'
    )

    def validate(self, timestamp: str) -> None:
        """
        Validate timestamp format (ISO 8601 with milliseconds and Z).

        Args:
            timestamp: String to validate

        Raises:
            ValueError: If timestamp format is invalid
        """
        if not timestamp:
            raise ValueError("timestamp cannot be empty")

        if not self.TIMESTAMP_PATTERN.match(timestamp):
            raise ValueError(
                f"Invalid timestamp format: {timestamp}. "
                "Expected format: YYYY-MM-DDTHH:MM:SS.fffZ"
            )

        # Verify it parses correctly as datetime
        try:
            datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
        except ValueError as e:
            raise ValueError(f"Invalid timestamp: {e}")


class TimestampParser:
    """Parses ISO 8601 timestamps into components."""

    def __init__(self):
        self.validator = TimestampValidator()

    def parse(self, timestamp: str) -> Dict[str, int]:
        """
        Parse timestamp into components.

        Args:
            timestamp: ISO 8601 timestamp string

        Returns:
            Dict with keys: year, month, day, hour, minute, second, millisecond

        Raises:
            ValueError: If timestamp is invalid
        """
        # Validate first
        self.validator.validate(timestamp)

        # Parse datetime portion
        dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))

        # Extract milliseconds from string (more precise than from datetime)
        ms_str = timestamp.split('.')[1].rstrip('Z')

        return {
            'year': dt.year,
            'month': dt.month,
            'day': dt.day,
            'hour': dt.hour,
            'minute': dt.minute,
            'second': dt.second,
            'millisecond': int(ms_str)
        }


# ============================================================================
# Phase and Complexity Validation
# ============================================================================

class PhaseValidator:
    """Validates phase numbers (1-6 for ideation phases)."""

    MIN_PHASE = 1
    MAX_PHASE = 6

    def validate(self, checkpoint_data: Dict[str, Any]) -> None:
        """
        Validate phase number (1-6).

        Args:
            checkpoint_data: Checkpoint to validate

        Raises:
            ValueError: If phase is outside valid range
        """
        phase = checkpoint_data.get("current_phase")

        if phase is None:
            raise ValueError("current_phase is required")

        if not isinstance(phase, int):
            raise ValueError(f"current_phase must be an integer, got {type(phase).__name__}")

        if phase < self.MIN_PHASE or phase > self.MAX_PHASE:
            raise ValueError(
                f"current_phase must be {self.MIN_PHASE}-{self.MAX_PHASE}, got {phase}"
            )


class ComplexityValidator:
    """Validates complexity score (0-60 range)."""

    MIN_SCORE = 0
    MAX_SCORE = 60

    def validate(self, checkpoint: Dict[str, Any]) -> None:
        """
        Validate complexity score is 0-60.

        Args:
            checkpoint: Checkpoint to validate

        Raises:
            ValueError: If complexity_score is outside valid range
        """
        context = checkpoint.get("brainstorm_context", {})
        score = context.get("complexity_score")

        if score is None:
            return  # Optional field - no validation needed if missing

        if not isinstance(score, int):
            raise ValueError(
                f"complexity_score must be an integer, got {type(score).__name__}"
            )

        if score < self.MIN_SCORE or score > self.MAX_SCORE:
            raise ValueError(
                f"complexity_score must be {self.MIN_SCORE}-{self.MAX_SCORE}, got {score}"
            )


# ============================================================================
# Path Validation
# ============================================================================

class PathValidator:
    """Validates checkpoint file paths for security."""

    REQUIRED_PREFIX = "devforgeai/temp/"

    def validate(self, path: str) -> None:
        """
        Validate checkpoint path is safe.

        Args:
            path: File path to validate

        Raises:
            ValueError: If path is invalid or unsafe
        """
        if not path:
            raise ValueError("Path cannot be empty")

        # Check for directory traversal attack
        if '..' in path:
            raise ValueError("Path cannot contain '..' (directory traversal)")

        # Must be in devforgeai/temp/
        if not path.startswith(self.REQUIRED_PREFIX):
            raise ValueError(
                f"Path must be in {self.REQUIRED_PREFIX}, got {path}"
            )


# ============================================================================
# Checkpoint Validation
# ============================================================================

class CheckpointValidator:
    """Validates complete checkpoint structure with all required fields."""

    REQUIRED_FIELDS = [
        "session_id",
        "timestamp",
        "current_phase",
        "phase_completed",
        "brainstorm_context"
    ]

    REQUIRED_CONTEXT_FIELDS = [
        "problem_statement",
        "personas",
        "requirements",
        "complexity_score",
        "epics"
    ]

    def __init__(self):
        self.session_validator = SessionIdValidator()
        self.timestamp_validator = TimestampValidator()
        self.phase_validator = PhaseValidator()
        self.complexity_validator = ComplexityValidator()

    def validate(self, checkpoint_data: Dict[str, Any]) -> None:
        """
        Validate checkpoint data structure.

        Args:
            checkpoint_data: Dictionary to validate

        Raises:
            ValueError: If validation fails
        """
        # Check required top-level fields
        for field in self.REQUIRED_FIELDS:
            if field not in checkpoint_data:
                raise ValueError(f"Missing required field: {field}")

        # Validate session_id format
        self.session_validator.validate(checkpoint_data["session_id"])

        # Validate timestamp format
        self.timestamp_validator.validate(checkpoint_data["timestamp"])

        # Validate phase number
        self.phase_validator.validate(checkpoint_data)

        # Validate complexity score if present
        self.complexity_validator.validate(checkpoint_data)


# ============================================================================
# YAML Validation
# ============================================================================

class YamlValidator:
    """Validates YAML serialization capability."""

    def validate(self, data: Dict[str, Any]) -> bool:
        """
        Validate data can be serialized to valid YAML.

        Args:
            data: Dictionary to validate

        Returns:
            bool: True if valid, False otherwise
        """
        try:
            yaml_str = yaml.dump(data, default_flow_style=False)
            yaml.safe_load(yaml_str)
            return True
        except (yaml.YAMLError, TypeError):
            return False


# ============================================================================
# Secret Scanning
# ============================================================================

class SecretScanner:
    """Scans for secrets in checkpoint data (NFR-004: security)."""

    SECRET_PATTERNS = [
        r'api[_-]?key\s*[=:]\s*["\']?[\w-]+',
        r'password\s*[=:]\s*["\']?[\w-]+',
        r'secret\s*[=:]\s*["\']?[\w-]+',
        r'-----BEGIN.*PRIVATE KEY-----',
        r'token\s*[=:]\s*["\']?[\w-]+',
    ]

    def scan(self, checkpoint: Dict[str, Any]) -> bool:
        """
        Scan for secrets in checkpoint data.

        Args:
            checkpoint: Checkpoint data to scan

        Returns:
            bool: True if secrets found, False if clean
        """
        # Convert to JSON string for pattern matching
        content = json.dumps(checkpoint).lower()

        for pattern in self.SECRET_PATTERNS:
            if re.search(pattern, content, re.IGNORECASE):
                return True

        return False


# ============================================================================
# Resume Service
# ============================================================================

class ResumeService:
    """Extracts resumable state from checkpoint for session continuation."""

    def extract_resume_state(self, checkpoint: Dict[str, Any]) -> Dict[str, Any]:
        """
        Extract state for resuming session from checkpoint.

        Args:
            checkpoint: Checkpoint dictionary

        Returns:
            Dict with resume state information including:
            - session_id
            - current_phase
            - phase_completed
            - brainstorm_context
            - personas (convenience accessor)
            - requirements (convenience accessor)
        """
        context = checkpoint.get("brainstorm_context", {})

        return {
            "session_id": checkpoint.get("session_id"),
            "current_phase": checkpoint.get("current_phase"),
            "phase_completed": checkpoint.get("phase_completed"),
            "brainstorm_context": context,
            "personas": context.get("personas", []),
            "requirements": context.get("requirements", []),
        }


# ============================================================================
# Checkpoint Service (Main Orchestrator)
# ============================================================================

class CheckpointService:
    """
    Manages checkpoint lifecycle: create, update, validate checkpoints at phase boundaries.

    Business Rules:
    - BR-001: Uses Write tool exclusively (no Bash for file ops)
    - BR-002: Path is devforgeai/temp/.ideation-checkpoint-{session_id}.yaml
    - BR-003: Session ID consistency enforced via path
    - BR-004: Graceful degradation on write failures
    """

    CHECKPOINT_DIR = "devforgeai/temp"
    FILENAME_TEMPLATE = ".ideation-checkpoint-{session_id}.yaml"

    def __init__(self, write_tool=None):
        """
        Initialize CheckpointService with Write tool dependency.

        Args:
            write_tool: Mock or real Write tool with .write(path, content) method
        """
        self.write_tool = write_tool
        self.path_validator = PathValidator()

    def _get_checkpoint_path(self, session_id: str) -> str:
        """
        Build checkpoint file path from session_id.

        Args:
            session_id: UUID v4 session identifier

        Returns:
            str: Full checkpoint file path
        """
        filename = self.FILENAME_TEMPLATE.format(session_id=session_id)
        return f"{self.CHECKPOINT_DIR}/{filename}"

    def create_checkpoint(self, checkpoint_data: Dict[str, Any]) -> None:
        """
        Create or update checkpoint file with given data.

        Uses Write tool for atomic write semantics. Propagates errors
        to caller for handling (BR-004: caller handles graceful degradation).

        Args:
            checkpoint_data: Dictionary with session_id, timestamp, current_phase,
                           phase_completed, and brainstorm_context

        Raises:
            ValueError: If checkpoint_data is invalid
            IOError: If write operation fails (disk full, etc.)
            PermissionError: If write permission denied
        """
        if not self.write_tool:
            return  # No-op if no write tool provided (for testing without mock)

        # Get session_id for path construction
        session_id = checkpoint_data.get("session_id")
        if not session_id:
            raise ValueError("session_id is required in checkpoint_data")

        # Build file path (BR-002: correct path pattern)
        file_path = self._get_checkpoint_path(session_id)

        # Validate path for security
        self.path_validator.validate(file_path)

        # Convert to YAML for storage
        yaml_content = yaml.dump(checkpoint_data, default_flow_style=False)

        # Write using Write tool (BR-001: no Bash)
        # Errors propagate to caller for graceful handling (BR-004)
        self.write_tool.write(file_path, yaml_content)
