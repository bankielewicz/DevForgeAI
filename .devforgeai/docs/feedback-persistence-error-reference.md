# Feedback File Persistence - Error Message Reference

**Version:** 1.0.0
**Date:** 2025-11-11
**Story:** STORY-013 (Feedback File Persistence with Atomic Writes)

---

## Overview

Complete catalog of all error messages from `persist_feedback_session()` with causes, remediation steps, and prevention strategies.

---

## Error Categories

1. **Validation Errors** (Input validation failures)
2. **Filesystem Errors** (Directory/file operation failures)
3. **Permission Errors** (Access control failures)
4. **Resource Errors** (Disk space, collision limits)
5. **System Errors** (Platform-specific failures)

---

## Validation Errors

### E001: Invalid Operation Type

**Message:**
```
Invalid operation_type: '{value}'. Must be one of: command, skill, subagent, workflow
```

**Cause:**
- operation_type parameter not in whitelist
- Typo in operation type (e.g., "cmd" instead of "command")
- Case mismatch (e.g., "Command" instead of "command")

**Remediation:**
```python
# ✅ Correct
persist_feedback_session(operation_type="command", ...)

# ❌ Incorrect
persist_feedback_session(operation_type="cmd", ...)  # ← Error
persist_feedback_session(operation_type="Command", ...)  # ← Error
```

**Prevention:**
- Use constants: `OPERATION_TYPE_COMMAND = "command"`
- Validate input before calling function

---

### E002: Invalid Status

**Message:**
```
Invalid status: '{value}'. Must be one of: success, failure, partial, skipped
```

**Cause:**
- status parameter not in whitelist
- Typo (e.g., "pass" instead of "success")
- Case mismatch (e.g., "SUCCESS" instead of "success")

**Remediation:**
```python
# ✅ Correct
persist_feedback_session(status="success", ...)

# ❌ Incorrect
persist_feedback_session(status="pass", ...)  # ← Error
persist_feedback_session(status="ok", ...)  # ← Error
```

**Prevention:**
- Use constants: `STATUS_SUCCESS = "success"`
- Map legacy values: `"ok" → "success"`, `"fail" → "failure"`

---

### E003: Invalid Session ID

**Message:**
```
session_id must be a non-empty string
```

**Cause:**
- session_id is None
- session_id is empty string (`""`)
- session_id is whitespace only (`"   "`)
- session_id is non-string type (e.g., int, UUID object)

**Remediation:**
```python
# ✅ Correct
session_id = str(uuid.uuid4())  # "550e8400-e29b-41d4-a716-446655440000"
persist_feedback_session(session_id=session_id, ...)

# ❌ Incorrect
persist_feedback_session(session_id="", ...)  # ← Error: empty
persist_feedback_session(session_id=None, ...)  # ← Error: None
persist_feedback_session(session_id=uuid.uuid4(), ...)  # ← Error: UUID object, not string
```

**Prevention:**
- Always generate: `session_id = str(uuid.uuid4())`
- Validate non-empty: `assert session_id and session_id.strip()`

---

### E004: Invalid Timestamp

**Message:**
```
timestamp must be a non-empty string
```

**Cause:**
- timestamp is None
- timestamp is empty string
- timestamp is non-string type

**Remediation:**
```python
# ✅ Correct
from datetime import datetime, timezone
timestamp = datetime.now(timezone.utc).isoformat()
persist_feedback_session(timestamp=timestamp, ...)

# ❌ Incorrect
persist_feedback_session(timestamp="", ...)  # ← Error: empty
persist_feedback_session(timestamp=None, ...)  # ← Error: None
```

**Prevention:**
- Always generate fresh timestamp
- Use UTC timezone for consistency

---

### E005: Missing Description

**Message:**
```
description must be a non-empty string
```

**Cause:**
- description parameter is None, empty, or whitespace-only

**Remediation:**
```python
# ✅ Correct
persist_feedback_session(description="TDD cycle completed", ...)

# ❌ Incorrect
persist_feedback_session(description="", ...)  # ← Error
persist_feedback_session(description=None, ...)  # ← Error
```

**Prevention:**
- Provide meaningful description (1-2 sentences)
- Include operation context: "TDD cycle for STORY-042"

---

### E006: Missing Operation Name

**Message:**
```
At least one operation name (command_name, skill_name, subagent_name, workflow_name) must be provided
```

**Cause:**
- All 4 operation name parameters are None
- operation_type specified but no corresponding name

**Remediation:**
```python
# ✅ Correct
persist_feedback_session(
    operation_type="command",
    command_name="/dev STORY-042",  # ← Provided
    skill_name=None,
    subagent_name=None,
    workflow_name=None,
    ...
)

# ❌ Incorrect
persist_feedback_session(
    operation_type="command",
    command_name=None,  # ← Missing
    skill_name=None,
    subagent_name=None,
    workflow_name=None,
    ...
)
```

**Prevention:**
- Match operation_type with corresponding name parameter
- command → command_name, skill → skill_name, etc.

---

## Filesystem Errors

### E101: Failed to Create Feedback Directory

**Message:**
```
Failed to create feedback directory: {path}
```

**Cause:**
- Parent directory not writable
- Permission denied
- Disk full
- Invalid path (e.g., path traversal blocked)

**Remediation:**
```bash
# Check parent directory permissions
ls -ld .devforgeai/

# Fix permissions
chmod 0755 .devforgeai/

# Check disk space
df -h .

# Verify path is valid
echo ".devforgeai/feedback/sessions" | grep -E '\.\./|//'
```

**Prevention:**
- Ensure `.devforgeai/` is writable
- Monitor disk space
- Use relative paths (not absolute)

---

### E102: File Write Verification Failed

**Message:**
```
File write verification failed: {filepath}
```

**Cause:**
- Filesystem inconsistency (extremely rare)
- File deleted immediately after write (external process)
- Network filesystem race condition

**Remediation:**
```bash
# Check if file exists manually
ls -l {filepath}

# Check filesystem health
fsck (requires unmount - do NOT run on live system)

# Retry operation
# Usually succeeds on retry
```

**Prevention:**
- Use local filesystem (not network mounts for feedback)
- Avoid external processes that delete feedback files

---

### E103: Too Many Collisions

**Message:**
```
Too many collisions for filename: {base_filename}. This suggests a timestamp resolution issue or excessive concurrent writes.
```

**Cause:**
- 10,000+ feedback sessions in same second (pathological)
- Timestamp not advancing (clock frozen)
- Extremely high concurrency (unlikely)

**Remediation:**
```bash
# Check system clock
date

# Check if clock advancing
date && sleep 2 && date

# If clock frozen, fix system time
ntpdate pool.ntp.org

# If high concurrency, review architecture
# 10,000 operations/second suggests design issue
```

**Prevention:**
- Ensure system clock is working
- Review concurrency patterns (10k/sec is excessive)
- Consider batching operations

---

## Permission Errors

### E201: Permission Denied on Directory Creation

**Message:**
```
Failed to create feedback directory: {path}
[Errno 13] Permission denied: '{path}'
```

**Cause:**
- User lacks write permission on parent directory
- Directory owned by different user
- Filesystem mounted read-only

**Remediation:**
```bash
# Check who owns parent directory
ls -ld .devforgeai/

# Change ownership (if root access)
sudo chown $USER:$USER .devforgeai/

# Or: Run as correct user
sudo -u correct_user /dev STORY-042

# Check filesystem mount
mount | grep "ro," # Look for read-only mounts
```

**Prevention:**
- Ensure project directory owned by current user
- Don't run DevForgeAI as root (creates permission issues)

---

### E202: Permission Denied on File Write

**Message:**
```
[Errno 13] Permission denied: '{filepath}.tmp'
```

**Cause:**
- feedback/sessions/ directory not writable
- Quota exceeded
- SELinux/AppArmor policy blocking write

**Remediation:**
```bash
# Check directory permissions
ls -ld .devforgeai/feedback/sessions/

# Fix permissions
chmod 0700 .devforgeai/feedback/sessions/

# Check disk quota
quota -s

# Check SELinux (if applicable)
getenforce  # Should be "Permissive" or "Disabled"
```

---

## Resource Errors

### E301: No Space Left on Device

**Message:**
```
[Errno 28] No space left on device: '{filepath}.tmp'
```

**Cause:**
- Filesystem full
- Disk quota exceeded
- Partition full (even if system has space)

**Remediation:**
```bash
# Check disk space
df -h .devforgeai/

# Free up space
# Option 1: Delete old feedback
find .devforgeai/feedback/ -name "*.md" -mtime +90 -delete

# Option 2: Move feedback to larger volume
mv .devforgeai/feedback/ /mnt/large_disk/
ln -s /mnt/large_disk/feedback/ .devforgeai/feedback

# Option 3: Enable retention policy
# Edit .devforgeai/config.yaml:
# retention:
#   enabled: true
#   max_age_days: 30
```

**Prevention:**
- Monitor disk space
- Enable retention policy
- Set up disk space alerts

---

### E302: Too Many Open Files

**Message:**
```
[Errno 24] Too many open files
```

**Cause:**
- File descriptor limit exceeded
- Feedback being written in tight loop without file closure

**Remediation:**
```bash
# Check current limit
ulimit -n

# Increase limit (temporary)
ulimit -n 4096

# Increase limit (permanent)
# Edit /etc/security/limits.conf:
# * soft nofile 4096
# * hard nofile 8192
```

**Prevention:**
- Feedback operations close files automatically (no leak)
- If hitting limit, check for leaks elsewhere in code

---

## System Errors

### E401: Operation Not Supported (Windows)

**Message:**
```
[Errno 95] Operation not supported
```

**Cause:**
- Attempting Unix-only operations on Windows
- Chmod called on FAT32/exFAT filesystem
- Symlink operations on Windows without admin rights

**Remediation:**
```python
# These are handled gracefully in implementation:
if os.name != "nt":
    filepath.chmod(0o600)  # Skipped on Windows

# No user action needed - operation continues
```

**Prevention:**
- None needed (implementation handles cross-platform differences)

---

### E402: Attribute Error (Platform Differences)

**Message:**
```
AttributeError: 'Path' object has no attribute 'chmod'
```

**Cause:**
- Platform doesn't support chmod
- Running in sandboxed environment
- pathlib mocked incorrectly in tests

**Remediation:**
- Implementation catches AttributeError automatically
- Operation continues without chmod
- File created with default permissions

**Prevention:**
- Set `permissions.enforce: false` in config (permissive mode)

---

## Error Handling Patterns

### Pattern 1: Validation Errors (Fail Fast)

```python
# Validate all inputs before any filesystem operations
try:
    _validate_operation_type(operation_type)
    _validate_status(status)
    _validate_session_id(session_id)
except ValueError as e:
    return FeedbackPersistenceResult(
        success=False,
        error=str(e)
    )
```

**When raised:** Immediately, before filesystem touched
**Recovery:** Fix input and retry

---

### Pattern 2: Filesystem Errors (Cleanup + Propagate)

```python
try:
    temp_file.write_text(content)
    temp_file.rename(final_file)
except OSError as e:
    # Cleanup temp file
    if temp_file.exists():
        temp_file.unlink()

    # Return error result
    return FeedbackPersistenceResult(
        success=False,
        error=f"Failed to create feedback directory: {e}"
    )
```

**When raised:** During filesystem operations
**Recovery:** Cleanup, then return error

---

### Pattern 3: Permission Errors (Continue Gracefully)

```python
try:
    filepath.chmod(0o600)
except (OSError, AttributeError):
    # Log warning, but continue
    logger.warning(f"Failed to set permissions on {filepath}")
    pass  # Continue despite permission failure
```

**When raised:** During permission setting
**Recovery:** Automatic (operation continues)

---

## Error Context Information

All error results include:
- `success`: false
- `error`: Descriptive message
- `duration_ms`: Time spent before failure
- `filepath`: null (file not created)
- `collision_resolved`: false
- `actual_filename`: null

**Example:**
```json
{
  "success": false,
  "filepath": null,
  "error": "Invalid operation_type: 'cmd'. Must be one of: command, skill, subagent, workflow",
  "duration_ms": 0,
  "collision_resolved": false,
  "actual_filename": null
}
```

---

## Common Error Scenarios and Solutions

### Scenario 1: First-Time Setup

**Error sequence:**
```
E101: Failed to create feedback directory: /home/user/project/.devforgeai/feedback/sessions
[Errno 13] Permission denied: '.devforgeai'
```

**Root cause:** Project directory owned by different user

**Solution:**
```bash
# Fix ownership
sudo chown -R $USER:$USER /home/user/project/

# Verify
ls -ld .devforgeai/
# Should show: drwxr-xr-x user user
```

---

### Scenario 2: Running in Container

**Error sequence:**
```
E202: Permission denied (chmod operation)
Warning: Failed to set permissions on feedback file
```

**Root cause:** Container filesystem doesn't support chmod

**Solution:**
```yaml
# Update .devforgeai/config.yaml
feedback:
  persistence:
    permissions:
      enforce: false  # ← Set to false for containers
```

---

### Scenario 3: Disk Full During Sprint

**Error sequence:**
```
E301: No space left on device
Failed during temp file write
```

**Root cause:** Disk full, large feedback volume

**Solution:**
```bash
# Immediate: Free space
rm -rf .devforgeai/feedback/sessions/2025-10-*.md  # Delete old feedback

# Long-term: Enable retention
# Edit .devforgeai/config.yaml:
feedback:
  persistence:
    retention:
      enabled: true
      max_age_days: 30
```

---

### Scenario 4: Concurrent Feedback Storm

**Error sequence:**
```
E103: Too many collisions for filename: 2025-11-11T14-30-00-subagent-success.md
This suggests excessive concurrent writes.
```

**Root cause:** 10,000+ subagents writing in same second (architectural issue)

**Solution:**
```python
# Short-term: Add jitter to timestamps
import random, time
time.sleep(random.uniform(0, 0.1))  # 0-100ms delay
persist_feedback_session(...)

# Long-term: Review architecture
# 10k operations/second suggests need for batching/queuing
```

---

## Debugging Checklist

When feedback persistence fails:

**Step 1: Check error message**
```python
result = persist_feedback_session(...)
if not result.success:
    print(f"Error: {result.error}")  # ← Read this carefully
```

**Step 2: Verify inputs**
```python
# All inputs non-null and valid?
assert operation_type in ["command", "skill", "subagent", "workflow"]
assert status in ["success", "failure", "partial", "skipped"]
assert session_id and session_id.strip()
assert description and description.strip()
```

**Step 3: Check filesystem**
```bash
# Directory exists and writable?
ls -ld .devforgeai/feedback/sessions/

# Disk space available?
df -h .devforgeai/

# File permissions correct?
ls -l .devforgeai/feedback/sessions/*.md | head -5
```

**Step 4: Check configuration**
```bash
# Config file exists?
cat .devforgeai/config.yaml

# Valid YAML?
python3 -m yaml .devforgeai/config.yaml

# Permissions enforce mode?
grep "enforce:" .devforgeai/config.yaml
```

**Step 5: Check logs**
```bash
# Look for warnings about chmod failures
grep -i "chmod" application.log

# Look for collision warnings
grep -i "collision" application.log
```

---

## Error Prevention Best Practices

### Input Validation

**✅ DO:**
```python
# Validate before calling
OPERATION_TYPE = "command"
STATUS = "success"
session_id = str(uuid.uuid4())

assert OPERATION_TYPE in ["command", "skill", "subagent", "workflow"]
assert STATUS in ["success", "failure", "partial", "skipped"]

result = persist_feedback_session(
    operation_type=OPERATION_TYPE,
    status=STATUS,
    session_id=session_id,
    ...
)
```

**❌ DON'T:**
```python
# No validation, pass raw user input
operation_type = user_input.get("type")  # Could be anything!
result = persist_feedback_session(operation_type=operation_type, ...)
```

---

### Filesystem Operations

**✅ DO:**
```python
# Check result before assuming success
result = persist_feedback_session(...)
if result.success:
    print(f"Saved to: {result.filepath}")
else:
    logger.error(f"Failed: {result.error}")
    # Handle error appropriately
```

**❌ DON'T:**
```python
# Assume success without checking
result = persist_feedback_session(...)
print(f"Saved to: {result.filepath}")  # ← May be None if failed!
```

---

### Error Logging

**✅ DO:**
```python
result = persist_feedback_session(...)
if not result.success:
    logger.error(
        f"Feedback persistence failed for {operation_type}",
        extra={
            "error": result.error,
            "duration_ms": result.duration_ms,
            "operation_type": operation_type,
            "status": status
        }
    )
```

**❌ DON'T:**
```python
# Silent failure
if not result.success:
    pass  # ❌ Error swallowed, debugging impossible
```

---

## Error Recovery Strategies

### Automatic Retry

**For transient errors** (disk full, permission temporary):
```python
def persist_with_retry(max_retries=3, delay=1.0, **kwargs):
    """Persist feedback with automatic retry."""
    for attempt in range(max_retries):
        result = persist_feedback_session(**kwargs)

        if result.success:
            return result

        # Transient error? Retry
        if "Permission denied" in result.error or "No space" in result.error:
            time.sleep(delay)
            continue

        # Validation error? Don't retry
        return result

    return result  # Failed after max retries
```

---

### Fallback Storage

**For permanent failures** (directory not creatable):
```python
def persist_with_fallback(**kwargs):
    """Persist with fallback to alternative location."""
    # Try primary location
    result = persist_feedback_session(base_path=Path(".devforgeai"), **kwargs)

    if result.success:
        return result

    # Fallback to temp directory
    logger.warning("Primary storage failed, using fallback: /tmp")
    result = persist_feedback_session(base_path=Path("/tmp/devforgeai-feedback"), **kwargs)

    return result
```

---

### Manual Recovery

**For disk full** (no automatic recovery):
```bash
# 1. Free disk space
du -sh .devforgeai/feedback/sessions/
# If > 100MB, delete old feedback

# 2. Enable retention to prevent recurrence
# Edit .devforgeai/config.yaml

# 3. Retry failed operation
/dev STORY-042  # Re-run command
```

---

## Error Rate Monitoring

### Expected Error Rates

| Error Type | Expected Rate | Threshold | Action if Exceeded |
|------------|---------------|-----------|-------------------|
| Validation errors | <1% | >5% | Review input validation |
| Filesystem errors | <0.1% | >1% | Check disk health |
| Permission errors | <0.01% | >0.1% | Check setup docs |
| Collision errors | <0.001% | >0.01% | Review concurrency |

### Monitoring

```python
# Track error rates
total_operations = 1000
validation_errors = 3
filesystem_errors = 1

validation_error_rate = (validation_errors / total_operations) * 100  # 0.3%
filesystem_error_rate = (filesystem_errors / total_operations) * 100  # 0.1%

if validation_error_rate > 5:
    alert("High validation error rate - check input handling")
if filesystem_error_rate > 1:
    alert("High filesystem error rate - check disk health")
```

---

## Related Documentation

- **Filename Format:** `feedback-persistence-filename-spec.md`
- **Atomic Writes:** `feedback-persistence-atomic-writes.md`
- **Configuration:** `feedback-persistence-config-guide.md`
- **Directory Layouts:** `feedback-persistence-directory-layouts.md`
- **Edge Cases:** `feedback-persistence-edge-cases.md`

---

## Changelog

- **v1.0.0 (2025-11-11):** Initial error reference catalog
  - 6 validation errors documented
  - 3 filesystem errors documented
  - 2 permission errors documented
  - 2 resource errors documented
  - 2 system errors documented
  - Recovery strategies provided

---

**This reference is authoritative for all DevForgeAI feedback persistence error handling.**
