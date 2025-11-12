# Operation Context API Documentation

**Module:** `devforgeai.operation_context`
**Version:** 1.0.0
**Status:** Production Ready

---

## Overview

The Operation Context API provides extraction and management of operation metadata from TodoWrite-based tracking systems. This enables rich, context-aware feedback conversations and retrospective analysis.

**Core Capabilities:**
- Extract operation context from TodoWrite tracking data
- Validate data structures (OperationContext, TodoItem, ErrorContext)
- Sanitize sensitive data (secrets, PII, credentials)
- Integrate with feedback template system
- Track operation history with feedback linking

---

## API Reference

### Data Models

#### OperationContext

Complete context of an operation (dev, qa, release, ideate, orchestrate).

```python
@dataclass(frozen=True)
class OperationContext:
    operation_id: str  # UUID
    operation_type: Literal["dev", "qa", "release", "ideate", "orchestrate"]
    start_time: str  # ISO8601
    end_time: str  # ISO8601
    duration_seconds: int  # 0-86400 (24 hours max)
    status: Literal["completed", "failed", "partial", "cancelled"]
    todo_summary: Dict[str, Any]  # total, completed, failed, skipped, completion_rate
    todos: List[TodoItem]  # 1-500 items, sequential IDs
    story_id: Optional[str] = None  # STORY-NNN format
    error: Optional[ErrorContext] = None  # Required if status="failed"
    phases: Optional[Dict[str, Any]] = None  # red, green, refactor phases
    extraction_metadata: Optional[ExtractionMetadata] = None
```

**Validation Rules:**
- `operation_id`: Must be valid UUID v4
- `start_time`, `end_time`: ISO8601 format, end >= start
- `duration_seconds`: 0-86400 (24 hours), must match end - start
- `story_id`: STORY-NNN pattern if present
- `todos`: 1-500 items with sequential IDs starting from 1
- `status="failed"` requires `error` to be non-None

**Example:**
```python
from devforgeai.operation_context import OperationContext, TodoItem

context = OperationContext(
    operation_id="550e8400-e29b-41d4-a716-446655440000",
    operation_type="dev",
    story_id="STORY-001",
    start_time="2025-11-12T10:00:00Z",
    end_time="2025-11-12T10:35:42Z",
    duration_seconds=2142,
    status="completed",
    todo_summary={
        "total": 5,
        "completed": 5,
        "failed": 0,
        "skipped": 0,
        "completion_rate": 1.0
    },
    todos=[
        TodoItem(id=1, name="Generate tests", status="done", timestamp="2025-11-12T10:00:00Z"),
        TodoItem(id=2, name="Implement code", status="done", timestamp="2025-11-12T10:15:00Z"),
        # ... 3 more todos
    ],
    error=None
)
```

---

#### TodoItem

Represents a single task/todo item in operation tracking.

```python
@dataclass(frozen=True)
class TodoItem:
    id: int  # Sequential starting from 1
    name: str  # 1-200 characters
    status: Literal["done", "failed", "skipped", "pending"]
    timestamp: str  # ISO8601
    notes: Optional[str] = None  # 0-500 characters
```

**Validation Rules:**
- `id`: Must be sequential (1, 2, 3, ...), no gaps
- `name`: 1-200 characters (descriptive task name)
- `timestamp`: Valid ISO8601 format
- `notes`: Optional, max 500 characters

---

#### ErrorContext

Error information from failed operations.

```python
@dataclass(frozen=True)
class ErrorContext:
    message: str  # 1-500 characters
    type: str  # Error type (GitError, ValidationError, etc.)
    timestamp: str  # ISO8601
    failed_todo_id: Optional[int] = None  # Which todo failed
    stack_trace: Optional[str] = None  # Max 5000 characters
```

---

#### ExtractionMetadata

Metadata about the extraction process.

```python
@dataclass(frozen=True)
class ExtractionMetadata:
    extracted_at: str  # ISO8601
    sanitization_applied: bool
    fields_sanitized: int  # Count of redacted fields
    truncation_applied: bool
    completeness_score: float  # 0.0-1.0 (1.0 = complete, 0.5 = fallback)
```

---

### Functions

#### extractOperationContext()

Extract operation context from TodoWrite-based operation data.

```python
def extractOperationContext(
    operation_id: str,
    options: Optional[Dict[str, Any]] = None
) -> OperationContext
```

**Parameters:**
- `operation_id` (str): UUID of the operation to extract
- `options` (Optional[Dict]): Extraction options
  - `includeSanitization` (bool): Apply sanitization (default: True)
  - `maxContextSize` (int): Max context size in bytes (default: 50000)
  - `includePhases` (bool): Include phase metrics (default: True)
  - `includeMetadata` (bool): Include extraction metadata (default: True)

**Returns:**
- `OperationContext`: Fully validated context with all fields populated

**Raises:**
- `ValueError`: If operation_id is invalid UUID or data validation fails

**Example:**
```python
from devforgeai.operation_context import extractOperationContext

# Extract with defaults (sanitization enabled)
context = extractOperationContext("550e8400-e29b-41d4-a716-446655440000")

# Extract with custom options
context = extractOperationContext(
    "550e8400-e29b-41d4-a716-446655440000",
    options={
        "includeSanitization": True,
        "maxContextSize": 50000,
        "includeMetadata": True
    }
)

print(f"Operation {context.operation_type} completed in {context.duration_seconds}s")
print(f"Todos: {context.todo_summary['completed']}/{context.todo_summary['total']} done")
```

**Caching Behavior:**
- First call: Extracts from storage, caches result
- Subsequent calls: Returns cached result (same extraction_metadata.extracted_at)
- Cache invalidation: Use `clearOperationStore()` in tests

---

#### registerOperation() [Test Helper]

Register an operation for extraction (test/development only).

```python
def registerOperation(operation_id: str, operation_data: Dict) -> None
```

**Parameters:**
- `operation_id` (str): UUID of operation
- `operation_data` (Dict): Operation details with keys:
  - `operation_type` (str): dev, qa, release, ideate, orchestrate
  - `story_id` (Optional[str]): STORY-NNN
  - `start_time` (str): ISO8601
  - `end_time` (str): ISO8601
  - `status` (str): completed, failed, partial, cancelled
  - `todos` (List[TodoItem]): Todo items
  - `error` (Optional[ErrorContext]): Error if failed
  - `phases` (Optional[Dict]): Phase metrics

**Note:** In production, TodoWrite tracking system would handle registration automatically.

---

#### clearOperationStore() [Test Helper]

Clear all registered operations and extraction cache (test cleanup).

```python
def clearOperationStore() -> None
```

**Usage:**
```python
# In pytest fixture
@pytest.fixture(autouse=True)
def clear_operation_store():
    from devforgeai.operation_context import clearOperationStore
    clearOperationStore()
    yield
    clearOperationStore()
```

---

### Integration Functions

#### pass_context_to_feedback()

Convert and sanitize operation context for feedback system.

```python
def pass_context_to_feedback(context: OperationContext) -> Dict[str, Any]
```

**Parameters:**
- `context` (OperationContext): Operation context to convert

**Returns:**
- Dict with feedback-ready context:
  - `operation_id` (str)
  - `operation_type` (str)
  - `story_id` (Optional[str])
  - `status` (str)
  - `todos` (List[Dict]): Converted to dicts
  - `duration_seconds` (int)
  - `error` (Optional[Dict]): If failed
  - `metadata` (Dict): Pre-populated metadata for template
  - `questions` (List[str]): Adaptive questions based on status
  - `summary` (str): Human-readable summary

**Example:**
```python
context = extractOperationContext(operation_id)
feedback_data = pass_context_to_feedback(context)

print(feedback_data["summary"])
# "Operation completed successfully in 2142 seconds with 5 todos."

for question in feedback_data["questions"]:
    print(f"Q: {question}")
# Q: What went well during this operation?
# Q: Were there any unexpected challenges?
```

---

#### prepopulate_feedback_template()

Generate feedback template pre-populated with operation metadata.

```python
def prepopulate_feedback_template(
    context: OperationContext,
    template_type: str = "retrospective"
) -> Dict[str, Any]
```

**Parameters:**
- `context` (OperationContext): Operation context
- `template_type` (str): Template variant (default: "retrospective")

**Returns:**
- Dict with template structure and pre-populated metadata

---

#### update_operation_history()

Update operation history with feedback session information.

```python
def update_operation_history(
    operation_id: str,
    feedback_session_id: Optional[str] = None,
    feedback_status: Optional[str] = None,
    collection_timestamp: Optional[str] = None,
    initiated_by: Optional[str] = None,
    initiated_at: Optional[str] = None
) -> Dict[str, Any]
```

**Parameters:**
- `operation_id` (str): UUID of operation
- `feedback_session_id` (Optional[str]): Feedback session UUID
- `feedback_status` (str): initiated, collected, skipped, incomplete
- `collection_timestamp` (Optional[str]): ISO8601 when collected
- `initiated_by` (Optional[str]): User who initiated feedback
- `initiated_at` (Optional[str]): ISO8601 when initiated

**Returns:**
- Dict with updated history entry

**Example:**
```python
# Link feedback session to operation
history = update_operation_history(
    operation_id="550e8400-e29b-41d4-a716-446655440000",
    feedback_session_id="660f9500-f39c-42e5-b827-557766551111",
    feedback_status="collected",
    collection_timestamp="2025-11-12T11:00:00Z"
)
```

---

## Error Handling

All validation errors are raised immediately in `__post_init__` with clear messages:

```python
# UUID validation error
ValueError: Invalid UUID format: not-a-uuid

# ISO8601 validation error
ValueError: Invalid ISO8601 timestamp: 2025-13-45T99:99:99Z

# Story ID format error
ValueError: Invalid story_id format (expected STORY-NNN): INVALID-001

# Duration error
ValueError: Duration must be 0-86400 seconds, got 90000

# Sequential ID error
ValueError: Todo IDs must be sequential starting from 1, got 3 at position 2

# Empty todos error
ValueError: Todos array must have at least 1 item

# Failed status error
ValueError: Failed status requires error context
```

**Best Practice:** Always wrap construction in try/except for validation errors.

---

## Security

### Sanitization

Use `redact_sensitive_data()` to sanitize strings before sharing:

```python
from devforgeai.sanitization import redact_sensitive_data

error_log = "Git failed: password=SuperSecret123 for user@github.com"
sanitized = redact_sensitive_data(error_log)
print(sanitized)
# "Git failed: [REDACTED] for [email@example.com]"
```

**Redacted Patterns:**
- Passwords, API keys, tokens
- IPv4/IPv6 addresses
- Email addresses (PII)
- Internal domain names
- Database connection strings
- File paths (keeps filename only)

---

## Performance Considerations

### Caching

`extractOperationContext()` caches results automatically:

```python
# First call: Extracts and caches
context1 = extractOperationContext(op_id)  # ~10-50ms

# Second call: Returns cached (same extracted_at timestamp)
context2 = extractOperationContext(op_id)  # ~1ms

assert context1.extraction_metadata.extracted_at == context2.extraction_metadata.extracted_at
```

**Cache invalidation:** Call `clearOperationStore()` (primarily for tests)

### Context Size

Contexts are limited to 50KB by default:

```python
# Enforce smaller limit
context = extractOperationContext(op_id, options={"maxContextSize": 25000})
```

Large todo lists (100+ items) are automatically summarized.

---

## Complete Example

```python
from devforgeai.operation_context import (
    OperationContext,
    TodoItem,
    ErrorContext,
    extractOperationContext,
    registerOperation,
)
from devforgeai.feedback_integration import pass_context_to_feedback
from devforgeai.operation_history import update_operation_history

# 1. Register operation (in production, TodoWrite handles this)
operation_id = "550e8400-e29b-41d4-a716-446655440000"
registerOperation(operation_id, {
    "operation_type": "dev",
    "story_id": "STORY-001",
    "start_time": "2025-11-12T10:00:00Z",
    "end_time": "2025-11-12T10:35:42Z",
    "status": "completed",
    "todos": [
        TodoItem(id=1, name="Generate tests", status="done", timestamp="2025-11-12T10:00:00Z"),
        TodoItem(id=2, name="Implement code", status="done", timestamp="2025-11-12T10:20:00Z"),
        TodoItem(id=3, name="Refactor", status="done", timestamp="2025-11-12T10:35:42Z"),
    ],
    "error": None,
    "phases": {
        "red": {"duration_seconds": 600, "success": True},
        "green": {"duration_seconds": 1200, "success": True},
        "refactor": {"duration_seconds": 342, "success": True}
    }
})

# 2. Extract context (with caching)
context = extractOperationContext(operation_id)

# 3. Pass to feedback system (sanitized + metadata)
feedback_data = pass_context_to_feedback(context)

print(feedback_data["summary"])
# "Operation completed successfully in 2142 seconds with 3 todos."

for question in feedback_data["questions"]:
    print(f"- {question}")
# - What went well during this operation?
# - Were there any unexpected challenges?
# - How confident are you in the results?

# 4. Update history with feedback link
history = update_operation_history(
    operation_id,
    feedback_session_id="feedback-123",
    feedback_status="collected"
)

print(f"History updated: {history['feedback_session_id']}")
# History updated: feedback-123
```

---

## Migration Guide

### From camelCase to snake_case

The API provides backward-compatible aliases for all functions:

```python
# OLD (deprecated, still works)
from devforgeai.sanitization import redactSensitiveData, sanitizeContext
from devforgeai.feedback_integration import passContextToFeedback, prepopulateFeedbackTemplate
from devforgeai.operation_history import updateOperationHistory

# NEW (preferred, PEP 8 compliant)
from devforgeai.sanitization import redact_sensitive_data, sanitize_context
from devforgeai.feedback_integration import pass_context_to_feedback, prepopulate_feedback_template
from devforgeai.operation_history import update_operation_history
```

**Recommendation:** Migrate to snake_case for better Python convention compliance.

---

## Testing

### Test Helpers

```python
import pytest
from devforgeai.operation_context import registerOperation, clearOperationStore, TodoItem

@pytest.fixture(autouse=True)
def clear_store():
    clearOperationStore()
    yield
    clearOperationStore()

def test_extract_completed_operation():
    # Arrange
    op_id = "550e8400-e29b-41d4-a716-446655440000"
    registerOperation(op_id, {
        "operation_type": "dev",
        "start_time": "2025-11-12T10:00:00Z",
        "end_time": "2025-11-12T10:30:00Z",
        "status": "completed",
        "todos": [TodoItem(id=1, name="Test", status="done", timestamp="2025-11-12T10:00:00Z")],
        "error": None,
    })

    # Act
    context = extractOperationContext(op_id)

    # Assert
    assert context.status == "completed"
    assert len(context.todos) == 1
```

---

## See Also

- [Data Validation Rules](./validation-rules.md)
- [Sanitization Documentation](./sanitization-guide.md)
- [User Guide](../guides/operation-context-user-guide.md)
- [Troubleshooting](../guides/troubleshooting-operation-context.md)
