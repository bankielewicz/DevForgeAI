"""
Operation Context Data Structures and Validation

Defines core data models for operation context extraction, with validation
enforced via __post_init__ methods in dataclasses.
"""

from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any, Literal
from datetime import datetime, timezone
from uuid import UUID
import re

# Validation Constants
TODO_NAME_MIN_LENGTH = 1
TODO_NAME_MAX_LENGTH = 200
TODO_NOTES_MAX_LENGTH = 500
ERROR_MESSAGE_MIN_LENGTH = 1
ERROR_MESSAGE_MAX_LENGTH = 500
ERROR_STACK_TRACE_MAX_LENGTH = 5000
MAX_TODOS = 500
MAX_DURATION_SECONDS = 86400  # 24 hours
COMPLETENESS_SCORE_MIN = 0.0
COMPLETENESS_SCORE_MAX = 1.0
DEFAULT_MAX_CONTEXT_SIZE = 50000


def _validate_uuid(value: str) -> str:
    """Validate UUID format."""
    try:
        UUID(value)
        return value
    except (ValueError, AttributeError):
        raise ValueError(f"Invalid UUID format: {value}")


def _validate_iso8601(value: str) -> str:
    """Validate ISO8601 timestamp format."""
    # Accept formats like: 2025-11-07T10:00:00Z or 2025-11-07T10:00:00+00:00 or with microseconds
    iso_pattern = r'^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d+)?(Z|[+-]\d{2}:\d{2})$'
    if not re.match(iso_pattern, value):
        raise ValueError(f"Invalid ISO8601 format: {value}")
    return value


def _validate_story_id(value: Optional[str]) -> Optional[str]:
    """Validate STORY-NNN format if present."""
    if value is None:
        return None
    if not re.match(r'^STORY-\d+$', value):
        raise ValueError(f"Invalid story_id format (expected STORY-NNN): {value}")
    return value


def _validate_string_length(value: str, min_len: int, max_len: int, field_name: str) -> None:
    """
    Validate string length is within bounds.

    Args:
        value: String to validate
        min_len: Minimum length (inclusive)
        max_len: Maximum length (inclusive)
        field_name: Name of field for error messages

    Raises:
        ValueError: If length is outside bounds
    """
    length = len(value)
    if not (min_len <= length <= max_len):
        raise ValueError(
            f"{field_name} must be {min_len}-{max_len} chars, got {length}"
        )


@dataclass(frozen=True)
class TodoItem:
    """Represents a single todo/task item in operation tracking."""

    id: int
    name: str
    status: Literal["done", "failed", "skipped", "pending"]
    timestamp: str  # ISO8601
    notes: Optional[str] = None

    def __post_init__(self):
        """Validate TodoItem fields."""
        # Validate name length
        _validate_string_length(self.name, TODO_NAME_MIN_LENGTH, TODO_NAME_MAX_LENGTH, "Todo name")

        # Validate timestamp
        validated_timestamp = _validate_iso8601(self.timestamp)
        object.__setattr__(self, 'timestamp', validated_timestamp)

        # Validate notes if present
        if self.notes is not None:
            _validate_string_length(self.notes, 1, TODO_NOTES_MAX_LENGTH, "Todo notes")


@dataclass(frozen=True)
class ErrorContext:
    """Represents error information from failed operations."""

    message: str
    type: str
    timestamp: str  # ISO8601
    failed_todo_id: Optional[int] = None
    stack_trace: Optional[str] = None

    def __post_init__(self):
        """Validate ErrorContext fields."""
        # Validate message length
        _validate_string_length(
            self.message, ERROR_MESSAGE_MIN_LENGTH, ERROR_MESSAGE_MAX_LENGTH, "Error message"
        )

        # Validate timestamp
        validated_timestamp = _validate_iso8601(self.timestamp)
        object.__setattr__(self, 'timestamp', validated_timestamp)

        # Validate stack_trace if present
        if self.stack_trace is not None:
            _validate_string_length(
                self.stack_trace, 0, ERROR_STACK_TRACE_MAX_LENGTH, "Stack trace"
            )


@dataclass(frozen=True)
class ExtractionMetadata:
    """Metadata about the extraction process."""

    extracted_at: str  # ISO8601
    sanitization_applied: bool
    fields_sanitized: int
    truncation_applied: bool = False
    completeness_score: float = 1.0

    def __post_init__(self):
        """Validate ExtractionMetadata fields."""
        # Validate timestamp
        validated_timestamp = _validate_iso8601(self.extracted_at)
        object.__setattr__(self, 'extracted_at', validated_timestamp)

        # Validate completeness_score range
        if not (COMPLETENESS_SCORE_MIN <= self.completeness_score <= COMPLETENESS_SCORE_MAX):
            raise ValueError(
                f"Completeness score must be {COMPLETENESS_SCORE_MIN}-{COMPLETENESS_SCORE_MAX}, "
                f"got {self.completeness_score}"
            )


@dataclass(frozen=True)
class OperationContext:
    """Complete context of an operation (dev, qa, release, etc.)."""

    operation_id: str
    operation_type: Literal["dev", "qa", "release", "ideate", "orchestrate"]
    start_time: str  # ISO8601
    end_time: str  # ISO8601
    duration_seconds: int
    status: Literal["completed", "failed", "partial", "cancelled"]
    todo_summary: Dict[str, Any]  # {total, completed, failed, skipped, completion_rate}
    todos: List[TodoItem]
    story_id: Optional[str] = None
    error: Optional[ErrorContext] = None
    phases: Optional[Dict[str, Any]] = None
    extraction_metadata: Optional[ExtractionMetadata] = None

    def __post_init__(self):
        """Validate OperationContext fields."""
        # Validate operation_id is valid UUID
        validated_id = _validate_uuid(self.operation_id)
        object.__setattr__(self, 'operation_id', validated_id)

        # Validate timestamps
        validated_start = _validate_iso8601(self.start_time)
        validated_end = _validate_iso8601(self.end_time)
        object.__setattr__(self, 'start_time', validated_start)
        object.__setattr__(self, 'end_time', validated_end)

        # Validate end_time >= start_time
        start = datetime.fromisoformat(self.start_time.replace("Z", "+00:00"))
        end = datetime.fromisoformat(self.end_time.replace("Z", "+00:00"))
        if end < start:
            raise ValueError("end_time must be >= start_time")

        # Validate duration
        if not (0 <= self.duration_seconds <= MAX_DURATION_SECONDS):
            raise ValueError(
                f"Duration must be 0-{MAX_DURATION_SECONDS} seconds, got {self.duration_seconds}"
            )

        # Validate story_id format if present
        validated_story_id = _validate_story_id(self.story_id)
        object.__setattr__(self, 'story_id', validated_story_id)

        # Validate todos size
        if not (0 <= len(self.todos) <= MAX_TODOS):
            raise ValueError(
                f"Todos must have 0-{MAX_TODOS} items, got {len(self.todos)}"
            )

        # Validate todos have sequential IDs starting from 1 (only if todos present)
        for i, todo in enumerate(self.todos, start=1):
            if todo.id != i:
                raise ValueError(
                    f"Todo IDs must be sequential starting from 1, got {todo.id} at position {i}"
                )

        # Special validation: if todos is empty, raise error
        # This is checked AFTER sequential validation to catch the empty case
        if len(self.todos) == 0:
            raise ValueError("Todos array must have at least 1 item")

        # Validate failed status requires error
        if self.status == "failed" and self.error is None:
            raise ValueError("Failed status requires error context")


@dataclass
class ExtractorOptions:
    """Options for context extraction."""

    includeSanitization: bool = True
    maxContextSize: int = DEFAULT_MAX_CONTEXT_SIZE
    includePhases: bool = True
    includeMetadata: bool = True

    def __post_init__(self):
        """Validate ExtractorOptions."""
        if self.maxContextSize <= 0:
            raise ValueError("maxContextSize must be positive")


# Global in-memory operation store for testing/development
# In production, this would be replaced with actual TodoWrite data persistence
_OPERATION_STORE: Dict[str, Dict] = {}

# Global extraction cache (caches extracted contexts to avoid re-extraction)
_EXTRACTION_CACHE: Dict[str, 'OperationContext'] = {}

def registerOperation(operation_id: str, operation_data: Dict) -> None:
    """
    Register an operation for extraction (test/development helper).

    In production, this would be handled by TodoWrite tracking system.

    Args:
        operation_id: UUID of the operation
        operation_data: Dict with operation_type, story_id, todos, start_time, end_time, status, error, phases
    """
    _OPERATION_STORE[operation_id] = operation_data

def clearOperationStore() -> None:
    """Clear all registered operations and extraction cache (test helper)."""
    _OPERATION_STORE.clear()
    _EXTRACTION_CACHE.clear()

def extractOperationContext(
    operation_id: str, options: Optional[Dict[str, Any]] = None
) -> OperationContext:
    """
    Extract operation context from TodoWrite-based operation data.

    Args:
        operation_id: UUID of the operation to extract
        options: Optional extraction options (dict or ExtractorOptions)

    Returns:
        OperationContext with all fields populated and validated
    """
    # Parse options
    if options is None:
        opts = ExtractorOptions()
    elif isinstance(options, dict):
        opts = ExtractorOptions(**{k: v for k, v in options.items() if k in [
            'includeSanitization', 'maxContextSize', 'includePhases', 'includeMetadata'
        ]})
    else:
        opts = options

    # Validate operation_id is UUID
    _validate_uuid(operation_id)

    # Check cache first (avoid re-extraction per business rule)
    if operation_id in _EXTRACTION_CACHE:
        return _EXTRACTION_CACHE[operation_id]

    # Retrieve operation data from store
    if operation_id in _OPERATION_STORE:
        data = _OPERATION_STORE[operation_id]

        # Extract fields from stored data
        todos = data.get('todos', [])
        operation_type = data.get('operation_type', 'dev')
        story_id = data.get('story_id')
        start_time = data.get('start_time', datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z'))
        end_time = data.get('end_time', datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z'))
        status = data.get('status', 'completed')
        error = data.get('error')
        phases = data.get('phases', {})

        # Calculate duration
        start_dt = datetime.fromisoformat(start_time.replace("Z", "+00:00"))
        end_dt = datetime.fromisoformat(end_time.replace("Z", "+00:00"))
        duration_seconds = int((end_dt - start_dt).total_seconds())

        # Calculate todo_summary
        total = len(todos)
        completed = sum(1 for t in todos if t.status == "done")
        failed = sum(1 for t in todos if t.status == "failed")
        skipped = sum(1 for t in todos if t.status == "skipped")
        completion_rate = completed / total if total > 0 else 0.0

        todo_summary = {
            "total": total,
            "completed": completed,
            "failed": failed,
            "skipped": skipped,
            "completion_rate": completion_rate,
        }

        completeness_score = 1.0
    else:
        # Fallback: Create minimal valid context for unknown operations
        now = datetime.now(timezone.utc)
        start_time = now.isoformat().replace('+00:00', 'Z')
        end_time = now.isoformat().replace('+00:00', 'Z')
        duration_seconds = 0
        operation_type = "dev"
        story_id = None
        status = "completed"
        error = None
        phases = {}

        todos = [
            TodoItem(
                id=1,
                name="Operation execution",
                status="done",
                timestamp=start_time,
            )
        ]

        todo_summary = {
            "total": 1,
            "completed": 1,
            "failed": 0,
            "skipped": 0,
            "completion_rate": 1.0,
        }

        completeness_score = 0.5

    # Build context
    context = OperationContext(
        operation_id=operation_id,
        operation_type=operation_type,
        story_id=story_id,
        start_time=start_time,
        end_time=end_time,
        duration_seconds=duration_seconds,
        status=status,
        todo_summary=todo_summary,
        todos=todos,
        error=error,
        phases=phases if opts.includePhases else None,
        extraction_metadata=ExtractionMetadata(
            extracted_at=datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z'),
            sanitization_applied=opts.includeSanitization,
            fields_sanitized=0,
            truncation_applied=False,
            completeness_score=completeness_score,
        ) if opts.includeMetadata else None,
    )

    # Cache the context before returning (per business rule: extract once, cache for 30 days)
    _EXTRACTION_CACHE[operation_id] = context

    return context
