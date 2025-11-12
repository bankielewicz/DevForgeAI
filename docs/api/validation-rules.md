# Data Validation Rules - Operation Context

**Module:** `devforgeai.operation_context`
**Version:** 1.0.0

---

## Overview

All data structures enforce validation via `__post_init__` methods. Invalid data is rejected immediately with clear error messages.

**Validation Philosophy:**
- **Fail Fast**: Reject invalid data at construction time
- **Clear Errors**: Include field names, expected ranges, actual values
- **Defense in Depth**: Multi-layer validation (format + logic + constraints)
- **Immutable Results**: Frozen dataclasses prevent post-construction modification

---

## Validation Constants

```python
# Todo validation
TODO_NAME_MIN_LENGTH = 1
TODO_NAME_MAX_LENGTH = 200
TODO_NOTES_MAX_LENGTH = 500

# Error validation
ERROR_MESSAGE_MIN_LENGTH = 1
ERROR_MESSAGE_MAX_LENGTH = 500
ERROR_STACK_TRACE_MAX_LENGTH = 5000

# Operation validation
MAX_TODOS = 500
MAX_DURATION_SECONDS = 86400  # 24 hours

# Metadata validation
COMPLETENESS_SCORE_MIN = 0.0
COMPLETENESS_SCORE_MAX = 1.0

# Context size
DEFAULT_MAX_CONTEXT_SIZE = 50000  # 50KB
```

---

## TodoItem Validation

### Rule 1: ID Sequential

**Requirement:** Todo IDs must be sequential starting from 1

**Valid:**
```python
todos = [
    TodoItem(id=1, name="Task 1", status="done", timestamp="..."),
    TodoItem(id=2, name="Task 2", status="done", timestamp="..."),
    TodoItem(id=3, name="Task 3", status="done", timestamp="..."),
]
# ✅ Sequential: 1, 2, 3
```

**Invalid:**
```python
todos = [
    TodoItem(id=1, name="Task 1", status="done", timestamp="..."),
    TodoItem(id=3, name="Task 3", status="done", timestamp="..."),  # Skips 2
]
# ❌ Raises: ValueError("Todo IDs must be sequential starting from 1, got 3 at position 2")
```

---

### Rule 2: Name Length

**Requirement:** Todo name must be 1-200 characters

**Valid:**
```python
TodoItem(id=1, name="Short", status="done", timestamp="...")  # ✅ 5 chars
TodoItem(id=1, name="A" * 200, status="done", timestamp="...")  # ✅ 200 chars
```

**Invalid:**
```python
TodoItem(id=1, name="", status="done", timestamp="...")  # ❌ 0 chars
TodoItem(id=1, name="A" * 201, status="done", timestamp="...")  # ❌ 201 chars
# Raises: ValueError("Todo name must be 1-200 chars, got X")
```

---

### Rule 3: Status Values

**Requirement:** Status must be one of: `done`, `failed`, `skipped`, `pending`

**Valid:**
```python
TodoItem(id=1, name="Task", status="done", timestamp="...")  # ✅
TodoItem(id=1, name="Task", status="failed", timestamp="...")  # ✅
```

**Invalid:**
```python
TodoItem(id=1, name="Task", status="in-progress", timestamp="...")
# ❌ TypeError (Literal type enforcement)
```

---

### Rule 4: Timestamp Format

**Requirement:** ISO8601 format with trailing Z

**Valid:**
```python
TodoItem(id=1, name="Task", status="done", timestamp="2025-11-12T10:00:00Z")  # ✅
TodoItem(id=1, name="Task", status="done", timestamp="2025-11-12T10:00:00.000Z")  # ✅
```

**Invalid:**
```python
TodoItem(id=1, name="Task", status="done", timestamp="2025-11-12 10:00:00")  # ❌ No Z
TodoItem(id=1, name="Task", status="done", timestamp="2025-13-45T99:99:99Z")  # ❌ Invalid date
# Raises: ValueError("Invalid ISO8601 timestamp: ...")
```

---

### Rule 5: Notes Length (Optional)

**Requirement:** Notes, if present, must be 1-500 characters

**Valid:**
```python
TodoItem(id=1, name="Task", status="done", timestamp="...", notes=None)  # ✅ Optional
TodoItem(id=1, name="Task", status="done", timestamp="...", notes="Note")  # ✅ 4 chars
TodoItem(id=1, name="Task", status="done", timestamp="...", notes="X" * 500)  # ✅ 500 chars
```

**Invalid:**
```python
TodoItem(id=1, name="Task", status="done", timestamp="...", notes="X" * 501)
# ❌ Raises: ValueError("Todo notes must be <= 500 chars, got 501")
```

---

## ErrorContext Validation

### Rule 6: Message Length

**Requirement:** Error message must be 1-500 characters

```python
# ✅ Valid
ErrorContext(message="Git commit failed", type="GitError", timestamp="...")

# ❌ Invalid
ErrorContext(message="", type="GitError", timestamp="...")  # Too short
ErrorContext(message="X" * 501, type="GitError", timestamp="...")  # Too long
```

---

### Rule 7: Stack Trace Length

**Requirement:** Stack trace, if present, must be <= 5000 characters

```python
# ✅ Valid
ErrorContext(message="Error", type="Type", timestamp="...", stack_trace="X" * 5000)
ErrorContext(message="Error", type="Type", timestamp="...", stack_trace=None)  # Optional

# ❌ Invalid
ErrorContext(message="Error", type="Type", timestamp="...", stack_trace="X" * 5001)
# Raises: ValueError("Stack trace must be <= 5000 chars, got 5001")
```

---

## OperationContext Validation

### Rule 8: UUID Format

**Requirement:** operation_id must be valid UUID v4

```python
# ✅ Valid
OperationContext(operation_id="550e8400-e29b-41d4-a716-446655440000", ...)

# ❌ Invalid
OperationContext(operation_id="not-a-uuid", ...)
# Raises: ValueError("Invalid UUID format: not-a-uuid")
```

---

### Rule 9: Timestamp Ordering

**Requirement:** end_time must be >= start_time

```python
# ✅ Valid
OperationContext(
    start_time="2025-11-12T10:00:00Z",
    end_time="2025-11-12T10:30:00Z",  # Later
    duration_seconds=1800,
    ...
)

# ❌ Invalid
OperationContext(
    start_time="2025-11-12T10:30:00Z",
    end_time="2025-11-12T10:00:00Z",  # Earlier!
    ...
)
# Raises: ValueError("end_time must be >= start_time")
```

---

### Rule 10: Duration Consistency

**Requirement:** duration_seconds must match (end - start) and be <= 24 hours

```python
# ✅ Valid
OperationContext(
    start_time="2025-11-12T10:00:00Z",
    end_time="2025-11-12T11:00:00Z",
    duration_seconds=3600,  # Matches 1 hour
    ...
)

# ❌ Invalid
OperationContext(
    duration_seconds=90000,  # > 24 hours
    ...
)
# Raises: ValueError("Duration must be 0-86400 seconds, got 90000")
```

---

### Rule 11: Story ID Format

**Requirement:** story_id, if present, must match STORY-NNN pattern

```python
# ✅ Valid
OperationContext(story_id="STORY-001", ...)  # Valid format
OperationContext(story_id="STORY-9999", ...)  # Valid
OperationContext(story_id=None, ...)  # None allowed

# ❌ Invalid
OperationContext(story_id="STR-001", ...)  # Wrong prefix
OperationContext(story_id="STORY-ABC", ...)  # Non-numeric
# Raises: ValueError("Invalid story_id format (expected STORY-NNN): ...")
```

---

### Rule 12: Todos Array Size

**Requirement:** Todos must have 1-500 items

```python
# ✅ Valid
OperationContext(todos=[TodoItem(...)], ...)  # 1 item
OperationContext(todos=[TodoItem(...)] * 500, ...)  # 500 items

# ❌ Invalid
OperationContext(todos=[], ...)  # Empty
# Raises: ValueError("Todos array must have at least 1 item")

OperationContext(todos=[TodoItem(...)] * 501, ...)  # Too many
# Raises: ValueError("Todos must have 0-500 items, got 501")
```

---

### Rule 13: Failed Status Requires Error

**Requirement:** status="failed" must have error context

```python
# ✅ Valid
OperationContext(
    status="failed",
    error=ErrorContext(message="Failed", type="Error", timestamp="..."),
    ...
)

# ❌ Invalid
OperationContext(
    status="failed",
    error=None,  # Missing error!
    ...
)
# Raises: ValueError("Failed status requires error context")
```

---

## ExtractionMetadata Validation

### Rule 14: Completeness Score Range

**Requirement:** completeness_score must be 0.0-1.0

```python
# ✅ Valid
ExtractionMetadata(extracted_at="...", sanitization_applied=True, fields_sanitized=0, completeness_score=0.0)  # Min
ExtractionMetadata(extracted_at="...", sanitization_applied=True, fields_sanitized=0, completeness_score=1.0)  # Max
ExtractionMetadata(extracted_at="...", sanitization_applied=True, fields_sanitized=0, completeness_score=0.5)  # Partial

# ❌ Invalid
ExtractionMetadata(extracted_at="...", sanitization_applied=True, fields_sanitized=0, completeness_score=1.5)
# Raises: ValueError("Completeness score must be 0.0-1.0, got 1.5")
```

---

## Validation Helper Functions

### _validate_uuid()

```python
def _validate_uuid(value: str) -> str:
    """Validate UUID format."""
    # Valid: "550e8400-e29b-41d4-a716-446655440000"
    # Invalid: "not-a-uuid" → ValueError
```

### _validate_iso8601()

```python
def _validate_iso8601(value: str) -> str:
    """Validate ISO8601 timestamp format."""
    # Valid: "2025-11-12T10:00:00Z" or "2025-11-12T10:00:00.000Z"
    # Invalid: "2025-11-12 10:00:00" → ValueError
```

### _validate_story_id()

```python
def _validate_story_id(value: Optional[str]) -> Optional[str]:
    """Validate STORY-NNN format if present."""
    # Valid: "STORY-001", "STORY-9999", None
    # Invalid: "STR-001", "STORY-ABC" → ValueError
```

### _validate_string_length()

```python
def _validate_string_length(value: str, min_len: int, max_len: int, field_name: str) -> None:
    """Validate string length is within bounds."""
    # Reusable function for name, notes, message, stack_trace validation
```

---

## Common Validation Errors

### Empty Todos Array

**Error:** `ValueError: Todos array must have at least 1 item`

**Cause:** OperationContext created with empty todos list

**Fix:** Ensure at least 1 TodoItem in todos array

---

### Non-Sequential Todo IDs

**Error:** `ValueError: Todo IDs must be sequential starting from 1, got 3 at position 2`

**Cause:** Todo IDs have gaps (1, 3, 5 instead of 1, 2, 3)

**Fix:** Renumber todos to be sequential from 1

---

### Invalid ISO8601 Timestamp

**Error:** `ValueError: Invalid ISO8601 timestamp: 2025-13-45T99:99:99Z`

**Cause:** Malformed timestamp (invalid month, day, hour, minute)

**Fix:** Use proper ISO8601 format: `datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z')`

---

### Failed Status Without Error

**Error:** `ValueError: Failed status requires error context`

**Cause:** status="failed" but error=None

**Fix:** Provide ErrorContext when status is "failed"

---

## Validation Order

Validation occurs in `__post_init__` in this order:

**OperationContext Validation Order:**
1. UUID format (operation_id)
2. ISO8601 format (start_time, end_time)
3. Timestamp ordering (end >= start)
4. Duration range (0-86400 seconds)
5. Story ID format (if present)
6. Todos array size (1-500)
7. Sequential todo IDs
8. At least 1 todo exists
9. Failed status has error context

**Early Termination:** Validation stops at first error (fail fast)

---

## See Also

- [API Documentation](./operation-context-api.md)
- [Sanitization Rules](./sanitization-guide.md)
