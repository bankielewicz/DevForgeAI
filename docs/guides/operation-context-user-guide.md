# Operation Context User Guide

**Feature:** Operation Lifecycle Integration (STORY-019)
**Audience:** DevForgeAI users and framework maintainers
**Version:** 1.0.0

---

## What is Operation Context?

Operation Context captures rich metadata about your development operations (/dev, /qa, /release) including:
- ✅ What todos were completed/failed
- ✅ How long each phase took
- ✅ What errors occurred (if any)
- ✅ Which story was being worked on

This context powers **smarter retrospective conversations** that can ask:
- "During the refactor phase, you spent 20 minutes - what made that challenging?"
- "The 'Git commit' todo failed - what was the root cause?"
- "You completed all 5 todos successfully - how confident are you in the results?"

---

## Quick Start

### 1. Run an Operation

```bash
# Example: Develop a story
/dev STORY-001
```

During execution, DevForgeAI automatically tracks:
- Todo items created via TodoWrite
- Phase durations (Red, Green, Refactor)
- Success/failure status
- Error details (if failures occur)

###2. Context Extracted Automatically

When the operation completes, context is extracted automatically:

```python
# Behind the scenes (automatic)
context = extractOperationContext(operation_id)

# Context includes:
# - operation_id: "550e8400-e29b-41d4-a716-446655440000"
# - operation_type: "dev"
# - story_id: "STORY-001"
# - todos: [TodoItem(...), TodoItem(...), ...]
# - duration_seconds: 2142
# - status: "completed"
```

### 3. Feedback Conversation Initiated

If enabled, retrospective feedback conversation starts automatically with context:

```
🔄 Retrospective Feedback for Operation dev (STORY-001)

Operation completed successfully in 35 minutes with 5 todos.

1. What went well during this operation?
2. Were there any unexpected challenges?
3. How confident are you in the results?
```

**Questions adapt based on context:**
- Completed operations → Ask about successes and challenges
- Failed operations → Ask about specific failed todo and root cause
- Long operations (>1 hour) → Ask about time-consuming phases

---

## Viewing Operation Context

### Programmatic Access

```python
from devforgeai.operation_context import extractOperationContext

# Extract context for an operation
operation_id = "550e8400-e29b-41d4-a716-446655440000"
context = extractOperationContext(operation_id)

# Access fields
print(f"Operation: {context.operation_type}")
print(f"Story: {context.story_id}")
print(f"Status: {context.status}")
print(f"Duration: {context.duration_seconds} seconds")

# Check todos
for todo in context.todos:
    status_icon = "✅" if todo.status == "done" else "❌"
    print(f"{status_icon} {todo.name} ({todo.status})")

# Check if operation failed
if context.status == "failed" and context.error:
    print(f"Error: {context.error.message}")
    print(f"Failed todo: {context.error.failed_todo_id}")
```

---

## Security & Privacy

### Automatic Sanitization

**All sensitive data is automatically redacted:**

```python
# Original error message
"Git auth failed: password=SuperSecret123 for user@github.com"

# Sanitized version (what feedback system sees)
"Git auth failed: [REDACTED] for [email@example.com]"
```

**Redacted Data:**
- ✅ Passwords, API keys, tokens
- ✅ IP addresses (IPv4 and IPv6)
- ✅ Email addresses (PII)
- ✅ Internal domain names
- ✅ File paths (keeps filename, removes directory)
- ✅ Database connection strings

**Audit Trail:**

Every sanitization is logged:

```python
context = extractOperationContext(operation_id, options={"includeMetadata": True})

if context.extraction_metadata.sanitization_applied:
    print(f"Redacted {context.extraction_metadata.fields_sanitized} fields")
    # "Redacted 3 fields"
```

---

## Querying Operation History

### By Operation ID

```python
from devforgeai.operation_history import OperationHistory

# Get specific operation history
history = OperationHistory.get(operation_id)

if history:
    print(f"Feedback session: {history.get('feedback_session_id')}")
    print(f"Status: {history.get('feedback_status')}")
```

### By Feedback Linked Status

```python
# Query operations with feedback
operations_with_feedback = OperationHistory.query(feedback_linked=True)

print(f"Found {len(operations_with_feedback)} operations with feedback")

# Query standalone operations (no feedback)
standalone_ops = OperationHistory.query(feedback_linked=False)
```

---

## Common Workflows

### Workflow 1: View Recent Operation Context

```python
from devforgeai.operation_context import extractOperationContext

# After running /dev STORY-001
operation_id = "your-operation-uuid"  # Logged during execution

context = extractOperationContext(operation_id)

# Summary
print(f"📊 Operation Summary")
print(f"Type: {context.operation_type}")
print(f"Story: {context.story_id or 'Standalone'}")
print(f"Duration: {context.duration_seconds}s ({context.duration_seconds // 60} min)")
print(f"Status: {context.status}")
print(f"Todos: {context.todo_summary['completed']}/{context.todo_summary['total']} completed")

if context.status == "failed":
    print(f"⚠️ Failed: {context.error.message}")
```

---

### Workflow 2: Analyze Failed Operation

```python
# Find what went wrong
context = extractOperationContext(failed_operation_id)

if context.error:
    print(f"❌ Failure Details:")
    print(f"   Error: {context.error.message}")
    print(f"   Type: {context.error.type}")
    print(f"   Failed todo: #{context.error.failed_todo_id}")

    # Find which todo failed
    failed_todo = next(t for t in context.todos if t.id == context.error.failed_todo_id)
    print(f"   Todo name: {failed_todo.name}")

    # Show preceding successful todos
    successful = [t for t in context.todos if t.id < context.error.failed_todo_id and t.status == "done"]
    print(f"   Completed before failure: {len(successful)} todos")
```

---

### Workflow 3: Performance Analysis

```python
# Check operation performance
context = extractOperationContext(operation_id)

if "phases" in context and context.phases:
    print("⏱️ Phase Breakdown:")
    for phase_name, phase_data in context.phases.items():
        duration = phase_data["duration_seconds"]
        status = "✅" if phase_data["success"] else "❌"
        print(f"   {status} {phase_name}: {duration}s ({duration // 60} min)")

    # Identify slow phases
    slow_phases = [
        (name, data["duration_seconds"])
        for name, data in context.phases.items()
        if data["duration_seconds"] > 600  # > 10 minutes
    ]

    if slow_phases:
        print("\n🐌 Slow phases (>10 min):")
        for name, duration in slow_phases:
            print(f"   - {name}: {duration // 60} minutes")
```

---

## Troubleshooting

### Issue: "Operation not found"

**Error:** `extractOperationContext()` returns minimal fallback context with completeness_score=0.5

**Cause:** Operation was never registered (or cache cleared)

**Solution:**
- Verify operation_id is correct (UUID format)
- Check if operation completed recently (cache retains 30 days)
- In tests, ensure `registerOperation()` called before extraction

---

### Issue: "Invalid UUID format"

**Error:** `ValueError: Invalid UUID format: not-a-uuid`

**Cause:** operation_id is not valid UUID

**Solution:**
```python
from uuid import uuid4

# Generate valid UUID
operation_id = str(uuid4())
```

---

### Issue: "Todos array must have at least 1 item"

**Error:** `ValueError: Todos array must have at least 1 item`

**Cause:** Tried to create OperationContext with empty todos list

**Solution:** Ensure operation has at least one todo tracked

---

### Issue: Incomplete context (completeness_score < 1.0)

**Symptom:** Context extraction returns partial data

**Cause:** Operation had minimal TodoWrite tracking or data is missing

**Expected Behavior:** System proceeds gracefully with available data

**Check completeness:**
```python
context = extractOperationContext(op_id, options={"includeMetadata": True})

if context.extraction_metadata.completeness_score < 1.0:
    print(f"⚠️ Partial context: {context.extraction_metadata.completeness_score * 100}% complete")
    print(f"Available todos: {len(context.todos)}")
```

---

## Advanced Usage

### Custom Extraction Options

```python
# Disable sanitization (for internal debugging only)
context = extractOperationContext(op_id, options={"includeSanitization": False})

# Limit context size
context = extractOperationContext(op_id, options={"maxContextSize": 25000})  # 25KB

# Exclude phases (reduce size)
context = extractOperationContext(op_id, options={"includePhases": False})

# Exclude metadata
context = extractOperationContext(op_id, options={"includeMetadata": False})
```

---

### Feedback Integration

```python
from devforgeai.feedback_integration import pass_context_to_feedback, prepopulate_feedback_template

# Convert context to feedback format
feedback_data = pass_context_to_feedback(context)

# Access adaptive questions
for question in feedback_data["questions"]:
    print(f"Q: {question}")

# Use in feedback template
template = prepopulate_feedback_template(context, template_type="retrospective")

print(template["metadata"]["operation_type"])  # "dev"
print(template["metadata"]["duration_minutes"])  # 35
print(template["metadata"]["todo_count"])  # 5
```

---

## Best Practices

### 1. Always Enable Sanitization

```python
# ✅ Good - sanitization enabled by default
context = extractOperationContext(op_id)

# ❌ Bad - disables sanitization (use only for internal debugging)
context = extractOperationContext(op_id, options={"includeSanitization": False})
```

### 2. Check Completeness Score

```python
context = extractOperationContext(op_id, options={"includeMetadata": True})

if context.extraction_metadata.completeness_score < 0.8:
    print("⚠️ Warning: Partial context - some data may be missing")
```

### 3. Handle Failed Operations Gracefully

```python
if context.status == "failed":
    if context.error:
        print(f"Error: {context.error.message}")
    else:
        print("Error details unavailable")
```

### 4. Use Immutability

```python
# ✅ Dataclasses are frozen - prevents accidental mutation
context = extractOperationContext(op_id)

# This raises FrozenInstanceError (good!)
# context.status = "modified"  # ❌ Won't work

# Create new instance instead
# (Not typical - contexts are read-only by design)
```

---

## Integration with DevForgeAI Workflow

**When context is extracted:**
1. **/dev completes** → Context extracted automatically
2. **/qa completes** → Context extracted automatically
3. **Feedback initiated** → Context passed to feedback conversation
4. **History updated** → Feedback link added to operation history

**Viewing context in stories:**

Story files include operation history:

```markdown
## Workflow History

### 2025-11-12 10:35 - Development Complete
- Phase: TDD (Red → Green → Refactor)
- Duration: 35 minutes
- Tests: 100/100 passing
- Coverage: 97% business logic
- Operation ID: 550e8400-e29b-41d4-a716-446655440000
- Feedback: Linked to session feedback-abc123 (collected)
```

---

## FAQ

**Q: How long is context cached?**
A: 30 days (per business rule). Cache is checked on first `extractOperationContext()` call.

**Q: Can I view unsanitized context?**
A: Only the operation initiator can access unsanitized context (security policy). Feedback conversations always receive sanitized context.

**Q: What happens if TodoWrite tracking is minimal?**
A: System extracts available data and sets completeness_score < 1.0. Feedback conversation proceeds with "Limited context" notice.

**Q: Are contexts immutable?**
A: Yes, all dataclasses are frozen. Attempting to modify raises FrozenInstanceError.

**Q: How do I test my own code that uses extractOperationContext()?**
A: Use `registerOperation()` helper in tests to simulate TodoWrite tracking, then `extractOperationContext()` to retrieve.

---

## Next Steps

- [API Reference](../api/operation-context-api.md) - Complete API documentation
- [Validation Rules](../api/validation-rules.md) - All validation constraints
- [Sanitization Guide](../api/sanitization-guide.md) - Security sanitization patterns
- [Troubleshooting Guide](./troubleshooting-operation-context.md) - Common issues
