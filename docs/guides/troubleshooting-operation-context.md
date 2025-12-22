# Troubleshooting Guide - Operation Context

**Module:** Operation Context Extraction (STORY-019)
**Version:** 1.0.0

---

## Common Issues

### Issue 1: Invalid UUID Format

**Error:**
```
ValueError: Invalid UUID format: not-a-uuid-string
```

**Cause:** operation_id parameter is not a valid UUID

**Solution:**
```python
from uuid import uuid4

# ✅ Correct - generate valid UUID
operation_id = str(uuid4())
context = extractOperationContext(operation_id)

# ❌ Wrong - invalid format
operation_id = "my-operation-123"  # Not a UUID
```

**Prevention:** Always use `uuid4()` to generate operation IDs

---

### Issue 2: Invalid ISO8601 Timestamp

**Error:**
```
ValueError: Invalid ISO8601 timestamp: 2025-11-12 10:00:00
```

**Cause:** Timestamp missing trailing 'Z' or in wrong format

**Solution:**
```python
from datetime import datetime, timezone

# ✅ Correct - ISO8601 with Z suffix
timestamp = datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z')
# "2025-11-12T10:00:00.123456Z"

# ❌ Wrong - missing Z
timestamp = "2025-11-12 10:00:00"
```

**Alternative:** Use `.replace('+00:00', 'Z')` to convert timezone-aware format

---

### Issue 3: Empty Todos Array

**Error:**
```
ValueError: Todos array must have at least 1 item
```

**Cause:** Trying to create OperationContext with `todos=[]`

**Solution:**
```python
# ✅ Correct - at least one todo
from devforgeai.operation_context import OperationContext, TodoItem

context = OperationContext(
    ...,
    todos=[
        TodoItem(id=1, name="Task 1", status="done", timestamp="...")
    ]
)

# ❌ Wrong - empty list
context = OperationContext(..., todos=[])
```

**Why this rule exists:** Operations must have tracked work (at least 1 todo item)

---

### Issue 4: Non-Sequential Todo IDs

**Error:**
```
ValueError: Todo IDs must be sequential starting from 1, got 3 at position 2
```

**Cause:** Todo IDs have gaps (e.g., 1, 3, 5 instead of 1, 2, 3)

**Solution:**
```python
# ✅ Correct - sequential IDs
todos = [
    TodoItem(id=1, name="Task 1", status="done", timestamp="..."),
    TodoItem(id=2, name="Task 2", status="done", timestamp="..."),
    TodoItem(id=3, name="Task 3", status="done", timestamp="..."),
]

# ❌ Wrong - skips ID 2
todos = [
    TodoItem(id=1, name="Task 1", status="done", timestamp="..."),
    TodoItem(id=3, name="Task 3", status="done", timestamp="..."),  # Gap!
]
```

**Fix:** Renumber todos to be sequential from 1

---

### Issue 5: end_time Before start_time

**Error:**
```
ValueError: end_time must be >= start_time
```

**Cause:** end_time is earlier than start_time (time travel!)

**Solution:**
```python
from datetime import datetime, timezone, timedelta

start = datetime.now(timezone.utc)
end = start + timedelta(seconds=1800)  # 30 minutes later

# ✅ Correct
context = OperationContext(
    start_time=start.isoformat().replace('+00:00', 'Z'),
    end_time=end.isoformat().replace('+00:00', 'Z'),
    duration_seconds=1800,
    ...
)

# ❌ Wrong - end before start
context = OperationContext(
    start_time="2025-11-12T11:00:00Z",
    end_time="2025-11-12T10:00:00Z",  # Earlier!
    ...
)
```

---

### Issue 6: Duration Exceeds 24 Hours

**Error:**
```
ValueError: Duration must be 0-86400 seconds, got 90000
```

**Cause:** Operation duration > 24 hours (86400 seconds)

**Solution:**
- Check if start_time and end_time are correct
- Verify duration calculation matches (end - start)
- Maximum allowed: 86400 seconds (24 hours)

**Why this limit:** Operations running >24 hours indicate system issues or incorrect timestamps

---

### Issue 7: Failed Status Without Error

**Error:**
```
ValueError: Failed status requires error context
```

**Cause:** status="failed" but error=None

**Solution:**
```python
from devforgeai.operation_context import ErrorContext

# ✅ Correct - failed status has error
context = OperationContext(
    status="failed",
    error=ErrorContext(
        message="Git commit failed",
        type="GitError",
        timestamp="2025-11-12T10:25:30Z",
        failed_todo_id=4
    ),
    ...
)

# ❌ Wrong - failed without error
context = OperationContext(
    status="failed",
    error=None,  # Missing!
    ...
)
```

---

### Issue 8: Invalid story_id Format

**Error:**
```
ValueError: Invalid story_id format (expected STORY-NNN): TICKET-001
```

**Cause:** story_id doesn't match STORY-NNN pattern

**Solution:**
```python
# ✅ Correct formats
story_id = "STORY-001"
story_id = "STORY-042"
story_id = "STORY-9999"
story_id = None  # None is valid for non-story operations

# ❌ Wrong formats
story_id = "TICKET-001"  # Wrong prefix
story_id = "STORY-ABC"  # Non-numeric
story_id = "story-001"  # Lowercase
```

---

### Issue 9: Context Size Too Large

**Error:** (Not an exception, but context truncated)

**Symptom:** Large operations (500 todos) have incomplete context

**Cause:** Context size exceeds 50KB limit

**Solution:**
```python
# Check if truncation occurred
context = extractOperationContext(op_id, options={"includeMetadata": True})

if context.extraction_metadata.truncation_applied:
    print("⚠️ Context was truncated to stay under size limit")
```

**Behavior:**
- Todos summarized (most recent + failed todos preserved)
- Stack traces truncated at 5000 characters
- Total context size kept < 50KB

---

### Issue 10: Completeness Score < 1.0

**Symptom:** `completeness_score = 0.5` indicating partial data

**Cause:** Operation not found in store (fallback context used)

**Explanation:**
- Score 1.0: Full context extracted from registered operation
- Score 0.5: Fallback minimal context (operation not found)
- Score 0.0-0.9: Partial context (some data missing/corrupted)

**Action:**
```python
context = extractOperationContext(op_id, options={"includeMetadata": True})

if context.extraction_metadata.completeness_score < 1.0:
    print(f"⚠️ Partial context: {context.extraction_metadata.completeness_score * 100}% complete")
    # Feedback conversation still proceeds with available data
```

---

### Issue 11: Sanitization Not Applied

**Symptom:** Sensitive data visible in feedback context

**Cause:** Sanitization disabled via options

**Solution:**
```python
# ✅ Correct - sanitization enabled (default)
context = extractOperationContext(op_id)
# or explicitly:
context = extractOperationContext(op_id, options={"includeSanitization": True})

# ❌ Dangerous - sanitization disabled
context = extractOperationContext(op_id, options={"includeSanitization": False})
```

**Security Note:** Never disable sanitization for production feedback conversations

---

### Issue 12: Cache Not Clearing in Tests

**Symptom:** Second test sees data from first test

**Cause:** `_EXTRACTION_CACHE` not cleared between tests

**Solution:**
```python
import pytest
from devforgeai.operation_context import clearOperationStore

@pytest.fixture(autouse=True)
def clear_cache():
    clearOperationStore()  # Clears both _OPERATION_STORE and _EXTRACTION_CACHE
    yield
    clearOperationStore()
```

**Note:** conftest.py already includes this fixture if configured properly

---

### Issue 13: Frozen Dataclass Modification Error

**Error:**
```
dataclasses.FrozenInstanceError: cannot assign to field 'status'
```

**Cause:** Trying to modify frozen dataclass after creation

**Solution:**
```python
# ❌ Wrong - trying to modify
context = extractOperationContext(op_id)
context.status = "modified"  # Raises FrozenInstanceError

# ✅ Correct - dataclasses are immutable by design
# Create new instance if you need different values
```

**Why frozen:** Immutability prevents accidental modification, ensures thread-safety

---

### Issue 14: Test Imports Failing

**Error:**
```
ImportError: cannot import name 'OperationContext' from 'devforgeai.operation_context'
```

**Cause:** Module not installed or path not configured

**Solution:**
```python
# In tests/conftest.py
import sys
from pathlib import Path

# Add src to Python path
project_root = Path(__file__).parent.parent
src_dir = project_root / "src"
if str(src_dir) not in sys.path:
    sys.path.insert(0, str(src_dir))
```

---

### Issue 15: Memory Usage High with Large Operations

**Symptom:** Memory consumption increases with 500 todo operations

**Cause:** Full context stored in cache

**Mitigation:**
1. Use `maxContextSize` option to limit size
2. Clear cache periodically: `clearOperationStore()`
3. In production, use Redis/Memcached with TTL

**Example:**
```python
# Limit context size for large operations
context = extractOperationContext(large_op_id, options={"maxContextSize": 25000})
```

---

## Performance Issues

### Slow Extraction (>200ms)

**Symptom:** `extractOperationContext()` takes >200ms

**Diagnostic:**
```python
import time

start = time.time()
context = extractOperationContext(op_id)
elapsed = (time.time() - start) * 1000

if elapsed > 200:
    print(f"⚠️ Slow extraction: {elapsed:.0f}ms")
```

**Common Causes:**
1. First extraction (not cached) with 500 todos
2. Complex sanitization (many secrets to redact)
3. Large stack traces (5000 characters)

**Solutions:**
- Cache is used on second call (~1ms)
- Reduce todos count if possible
- Truncate stack traces to essentials

---

### Large Context Size (>50KB)

**Symptom:** Context exceeds 50KB limit, truncation occurs

**Diagnostic:**
```python
import json
from dataclasses import asdict

context = extractOperationContext(op_id)
context_json = json.dumps(asdict(context))
size = len(context_json.encode("utf-8"))

if size > 50000:
    print(f"⚠️ Context size: {size} bytes (>50KB)")
```

**Solutions:**
1. Use `maxContextSize` option to enforce limit
2. Reduce phase detail (set `includePhases=False`)
3. Remove metadata (set `includeMetadata=False`)

---

## Testing Issues

### Test Failure: "Operation not registered"

**Cause:** Test calls `extractOperationContext()` without `registerOperation()` first

**Solution:**
```python
def test_my_feature():
    # ✅ Correct - register before extract
    op_id = str(uuid4())
    registerOperation(op_id, {
        "operation_type": "dev",
        "start_time": "...",
        "end_time": "...",
        "status": "completed",
        "todos": [TodoItem(...)],
        "error": None,
    })

    context = extractOperationContext(op_id)
    assert context.status == "completed"
```

---

## Debugging Tips

### Enable Verbose Logging

```python
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("devforgeai.operation_context")

# Now extraction will log debug info
context = extractOperationContext(op_id)
```

### Inspect Extraction Metadata

```python
context = extractOperationContext(op_id, options={"includeMetadata": True})

print("🔍 Extraction Metadata:")
print(f"  Extracted at: {context.extraction_metadata.extracted_at}")
print(f"  Sanitization: {context.extraction_metadata.sanitization_applied}")
print(f"  Fields sanitized: {context.extraction_metadata.fields_sanitized}")
print(f"  Truncation: {context.extraction_metadata.truncation_applied}")
print(f"  Completeness: {context.extraction_metadata.completeness_score * 100}%")
```

### Verify Sanitization

```python
from devforgeai.sanitization import redact_sensitive_data

test_string = "password=secret123 api_key=xyz"
sanitized = redact_sensitive_data(test_string)

print(f"Original: {test_string}")
print(f"Sanitized: {sanitized}")
# Should show [REDACTED] instead of actual secrets
```

---

## Getting Help

**Still having issues?**

1. **Check Logs:** Enable DEBUG logging to see extraction details
2. **Verify Data:** Use `extraction_metadata.completeness_score` to check data quality
3. **Review Validation:** See [Validation Rules](../api/validation-rules.md) for all constraints
4. **Test Helpers:** Use `registerOperation()` and `clearOperationStore()` in tests
5. **Security Audit:** Run full test suite with `pytest tests/integration/test_operation_context_edge_cases.py -v`

**Resources:**
- [API Documentation](../api/operation-context-api.md)
- [User Guide](./operation-context-user-guide.md)
- [Validation Rules](../api/validation-rules.md)
- [Sanitization Guide](../api/sanitization-guide.md)

**Report Issues:** Submit to DevForgeAI issue tracker with:
- Error message (full traceback)
- Minimal reproduction code
- Expected vs actual behavior
- Test environment details (Python version, pytest version)
