# Test Failure to Research Pattern Mapping

**Purpose:** Connect each failing test directly to the research patterns and implementation solutions
**Document Type:** Reference Guide
**Use This When:** "Why is test X failing?" or "How do I fix test Y?"

---

## Quick Lookup by Test Name

### Search by Test File

- **test_backup_service.py** → [Section 2: File System Errors](#backup-service-tests)
- **test_rollback_service.py** → [Section 3: Rollback Operations](#rollback-service-tests)
- **test_lock_file_manager.py** → [Section 4: Lock File Management](#lock-file-manager-tests)
- **test_install_logger.py** → [Section 5: Logging](#install-logger-tests)
- **test_error_handling_edge_cases.py** → [Section 6: Edge Cases](#edge-case-tests)
- **test_integration_error_handling.py** → [Section 7: Integration](#integration-tests)

---

## 1. Subprocess Timeout Tests (3-5 tests)

### Tests Affected
- `test_subprocess_timeout_command_return`
- `test_command_not_found_error`
- `test_nonzero_exit_code_captured`

### Research Pattern
**Source:** PYTHON-ERROR-HANDLING-RESEARCH-REPORT.md § 1 (Subprocess Error Handling)

**Pattern Name:** Comprehensive Exception Handling Pattern

**Code Location:** Research Report, Section 1, subsection "Solution: Comprehensive Exception Handling Pattern"

### Implementation Pattern
```python
try:
    result = subprocess.run(
        cmd,
        timeout=timeout_seconds,
        check=False,  # Don't raise on non-zero
        capture_output=True,
        text=True
    )
    if result.returncode != 0:
        raise RuntimeError(f"Command failed: {result.stderr}")
except subprocess.TimeoutExpired as e:
    raise RuntimeError(f"Timeout: {' '.join(cmd)}")
except FileNotFoundError as e:
    raise RuntimeError(f"Executable not found: {cmd[0]}")
```

### Expected Test Result
```python
# Test will pass when:
# 1. TimeoutExpired is caught and message contains "timed out"
# 2. CalledProcessError contains stderr output
# 3. FileNotFoundError contains "not found"
```

### Integration Guide
**File to Implement:** `installer/services/deployment_engine.py` (or similar)
**Method:** `run_command(cmd: list, timeout_seconds: int) -> int`

**Related Tests:** STORY-069 offline installation may use this for network timeouts

---

## 2. File System Error Categorization Tests (6-8 tests)

### Tests Affected
- `test_backup_fails_on_permission_error`
- `test_disk_full_error_cleanup_partial_backup`
- `test_rollback_handles_readonly_filesystem`
- `test_backup_creates_directory`
- `test_backup_preserves_directory_structure`
- `test_copy_file_atomic_operation`
- `test_file_not_found_during_backup`
- `test_partial_backup_cleanup_on_error`

### Research Pattern
**Source:** PYTHON-ERROR-HANDLING-RESEARCH-REPORT.md § 2 (File System Error Handling)

**Pattern Name:** Categorized Error Handling with errno Values

**Key Patterns:**
1. errno categorization (errno.EACCES=13, errno.ENOSPC=28, errno.EROFS=30)
2. Atomic file operations (write-to-temp-then-rename)
3. Partial backup cleanup on failure

**Code Locations:**
- Error categorization: Research Report § 2, subsection "Key errno Values for Recovery"
- Atomic file copy: Research Report § 2, subsection "Solution: Categorized Error Handling", method `_copy_file_atomic()`
- Cleanup pattern: Research Report § 2, subsection "Recovery Strategy", method `_cleanup_backup()`

### Implementation Pattern
```python
# Pattern 1: errno categorization
import errno
try:
    # file operation
except OSError as e:
    if e.errno == errno.EACCES:
        raise RuntimeError("Permission denied...")
    elif e.errno == errno.ENOSPC:
        raise RuntimeError("Disk full...")
    elif e.errno == errno.EROFS:
        raise RuntimeError("Read-only filesystem...")

# Pattern 2: atomic file copy
import tempfile, os
with tempfile.NamedTemporaryFile(dir=dst.parent, delete=False) as tmp:
    try:
        # write to tmp
        tmp.flush()
        os.fsync(tmp.fileno())
        tmp_path.replace(dst)  # atomic rename
    except:
        tmp_path.unlink(missing_ok=True)
        raise
```

### Expected Test Results
```python
# Tests will pass when:
# 1. PermissionError is caught with message "Permission denied"
# 2. ENOSPC error raises "Disk full"
# 3. Atomic copy preserves file integrity (no partial files)
# 4. Partial backup is cleaned up on error
# 5. Directory structure is mirrored in backup
```

### Integration Guide
**File to Implement:** `installer/services/backup_service.py`
**Methods:**
- `create_backup(target_dir: Path, files_to_backup: List[Path]) -> Path`
- `_copy_file_atomic(src_file: Path, backup_dir: Path, target_dir: Path)`
- `_categorize_and_raise(error: OSError, operation: str)`
- `_cleanup_backup(backup_dir: Path)`

**Constructor:** `__init__(self, logger=None)`

**Test Command:**
```bash
pytest installer/tests/test_backup_service.py -v
```

**Expected:** 18/18 passing

---

## 3. Atomic Rollback Operations Tests (5-7 tests)

### Tests Affected
- `test_rollback_restores_all_files_from_backup`
- `test_rollback_removes_partial_install_files`
- `test_rollback_returns_exit_code_3`
- `test_rollback_displays_console_message`
- `test_partial_rollback_continues_on_failure`
- `test_rollback_removes_empty_directories`
- `test_rollback_logs_actions`

### Research Pattern
**Source:** PYTHON-ERROR-HANDLING-RESEARCH-REPORT.md § 2 & § 5 (Rollback Operations)

**Pattern Name:** File Restoration with Partial Failure Tolerance

**Key Patterns:**
1. File-by-file restoration from backup (continue on single file failure)
2. Remove files created during installation (not in backup)
3. Remove empty directories (cleanup)
4. Return exit code 3 (ROLLBACK_OCCURRED)
5. Display console messages during rollback

**Code Locations:**
- File restoration: Research Report, Implementation Guide § 3, method `_restore_from_backup()`
- Partial file removal: Implementation Guide § 3, method `_remove_created_files()`
- Empty directory removal: Implementation Guide § 3, method `_remove_empty_directories()`
- Console messages: Implementation Guide § 3, line with `print("Rolling back...")`

### Implementation Pattern
```python
def rollback(self, backup_dir: Path, target_dir: Path) -> int:
    """Returns: 3 (ROLLBACK_OCCURRED)"""
    if not backup_dir.exists():
        raise FileNotFoundError(f"Backup not found: {backup_dir}")

    print("Rolling back installation...")  # Console message

    restored = self._restore_from_backup(backup_dir, target_dir)
    removed = self._remove_created_files(backup_dir, target_dir)
    empty_removed = self._remove_empty_directories(target_dir)

    print("Rollback complete. System restored to pre-installation state.")
    return 3  # ROLLBACK_OCCURRED

def _restore_from_backup(self, backup_dir: Path, target_dir: Path) -> int:
    """Continue on partial failures"""
    restored_count = 0
    for backup_file in backup_dir.rglob("*"):
        if backup_file.is_file():
            rel_path = backup_file.relative_to(backup_dir)
            target_file = target_dir / rel_path
            try:
                shutil.copy2(backup_file, target_file)
                restored_count += 1
            except PermissionError:
                self.logger.error(f"Failed to restore {target_file}")
                continue  # Continue with other files
    return restored_count
```

### Expected Test Results
```python
# Tests will pass when:
# 1. Exit code = 3 (integer)
# 2. Files restored from backup
# 3. Partial install files removed
# 4. Empty directories removed
# 5. Partial failures don't stop rollback
# 6. Console message shown
# 7. All actions logged
```

### Integration Guide
**File to Implement:** `installer/services/rollback_service.py`
**Methods:**
- `rollback(backup_dir: Path, target_dir: Path) -> int`
- `_restore_from_backup(backup_dir: Path, target_dir: Path) -> int`
- `_remove_created_files(backup_dir: Path, target_dir: Path) -> int`
- `_remove_empty_directories(target_dir: Path) -> int`

**Constructor:** `__init__(self, logger=None)`

**Test Command:**
```bash
pytest installer/tests/test_rollback_service.py -v
```

**Expected:** 16/16 passing

---

## 4. Lock File Management Tests (5-7 tests)

### Tests Affected
- `test_lock_file_prevents_concurrent_install`
- `test_stale_lock_file_removed_automatically`
- `test_lock_file_permission_0600`
- `test_lock_context_manager_cleanup`
- `test_lock_acquisition_with_timeout`
- `test_lock_retry_on_held_lock`
- `test_process_pid_validation`

### Research Pattern
**Source:** PYTHON-ERROR-HANDLING-RESEARCH-REPORT.md § 4 (Concurrent File Access - Lock File Management)

**Pattern Name:** PID-Based Stale Lock Detection with Atomic Lock Creation

**Key Patterns:**
1. Atomic lock creation using `os.O_EXCL | os.O_CREAT`
2. PID validation using `os.kill(pid, signal.SIG_DFL)` (doesn't kill, just checks)
3. Stale lock detection (process doesn't exist)
4. Timeout with retry mechanism
5. Context manager for guaranteed cleanup
6. File permissions 0o600

**Code Locations:**
- Atomic lock creation: Research Report § 4, subsection "Solution", method `acquire_lock()`
- PID validation: Research Report § 4, method `_process_exists()`
- Stale detection: Implementation Guide § 4, subsection "Fix Pattern", stale lock removal
- Context manager: Research Report § 4, methods `__enter__()`, `__exit__()`

### Implementation Pattern
```python
import os, signal, time
from pathlib import Path

def acquire_lock(self, timeout_seconds: int = 5) -> bool:
    """Returns: True if acquired, False if timeout"""
    self.lock_dir.mkdir(parents=True, exist_ok=True)
    start_time = time.time()

    while True:
        if self.lock_file.exists():
            pid, timestamp = self._read_lock()
            if not self._process_exists(pid):
                # Stale lock - remove and retry
                self.lock_file.unlink()
                continue
            # Process running - concurrent install
            raise RuntimeError(f"Installation in progress (PID {pid})")

        try:
            # Atomic create (O_EXCL fails if exists)
            fd = os.open(
                str(self.lock_file),
                os.O_CREAT | os.O_EXCL | os.O_WRONLY,
                0o600  # Permissions: owner read/write only
            )
            lock_content = f"{os.getpid()}:{time.time()}"
            os.write(fd, lock_content.encode())
            os.close(fd)
            return True
        except FileExistsError:
            if time.time() - start_time >= timeout_seconds:
                return False  # Timeout
            time.sleep(0.1)

@staticmethod
def _process_exists(pid: int) -> bool:
    """Check if process exists without killing it"""
    try:
        os.kill(pid, signal.SIG_DFL)  # signal 0 = check only
        return True
    except ProcessLookupError:
        return False  # Process dead

def __enter__(self):
    if not self.acquire_lock():
        raise RuntimeError("Could not acquire lock")
    return self

def __exit__(self, *args):
    self.release_lock()
```

### Expected Test Results
```python
# Tests will pass when:
# 1. Lock file created with 0o600 permissions (not 0o644)
# 2. Second process cannot acquire lock (concurrent blocked)
# 3. Stale lock (dead PID) is removed automatically
# 4. Context manager calls __exit__ even on error
# 5. Timeout returns False (doesn't raise)
# 6. Lock file contains valid PID:timestamp
```

### Integration Guide
**File to Implement:** `installer/services/lock_file_manager.py`
**Methods:**
- `acquire_lock(timeout_seconds: int, retry_interval: float) -> bool`
- `release_lock() -> None`
- `_read_lock() -> tuple` (returns pid, timestamp)
- `_process_exists(pid: int) -> bool` (static method)
- `cleanup() -> None`
- `__enter__()` and `__exit__()` (context manager)

**Constructor:** `__init__(self, lock_dir: Path = None)`

**Test Command:**
```bash
pytest installer/tests/test_lock_file_manager.py -v
```

**Expected:** 20/20 passing

---

## 5. Install Logger Tests (4-6 tests)

### Tests Affected
- `test_log_entry_has_iso8601_timestamp`
- `test_log_rotation_at_10mb`
- `test_log_file_permissions_0600`
- `test_log_append_mode_preserves_history`
- `test_log_includes_stack_trace_on_error`
- `test_log_session_separator`

### Research Pattern
**Source:** PYTHON-ERROR-HANDLING-RESEARCH-REPORT.md § 5 & Implementation Guide § 5 (Logging)

**Pattern Name:** ISO 8601 Timestamps with Log Rotation and Stack Traces

**Key Patterns:**
1. ISO 8601 timestamps with milliseconds and UTC timezone
2. Log rotation at 10MB (keep 3 rotations)
3. File permissions 0o600
4. Append mode (never overwrite)
5. Stack traces in log file (but not console)
6. Session separators

**Code Locations:**
- ISO 8601 timestamps: Research Report § 5, code example "Get ISO 8601 timestamp..."
- Log rotation: Implementation Guide § 5, method `_rotate_log_if_needed()`
- Stack traces: Implementation Guide § 5, method `log_error()`

### Implementation Pattern
```python
from datetime import datetime, timezone
import os

def __init__(self, log_file: Path, max_size_mb: int = 10, max_rotations: int = 3):
    self.log_file = Path(log_file)
    self.max_size_bytes = max_size_mb * 1024 * 1024
    self.max_rotations = max_rotations
    self.log_file.parent.mkdir(parents=True, exist_ok=True)

def _get_timestamp(self) -> str:
    """ISO 8601 with milliseconds: 2025-12-04T15:30:45.123+00:00"""
    now = datetime.now(timezone.utc)
    return now.isoformat(timespec='milliseconds')

def _rotate_log_if_needed(self) -> None:
    """Rotate at 10MB, keep 3 rotations"""
    if not self.log_file.exists():
        return

    file_size = self.log_file.stat().st_size
    if file_size < self.max_size_bytes:
        return

    # Rotate: log -> log.1 -> log.2 -> log.3 (discard)
    for i in range(self.max_rotations - 1, 0, -1):
        old_file = Path(f"{self.log_file}.{i}")
        new_file = Path(f"{self.log_file}.{i + 1}")
        if old_file.exists():
            new_file.unlink(missing_ok=True)
            old_file.rename(new_file)

    Path(f"{self.log_file}.1").unlink(missing_ok=True)
    self.log_file.rename(f"{self.log_file}.1")

def log_error(self, error: Exception) -> None:
    """Log error with full traceback"""
    import traceback
    timestamp = self._get_timestamp()
    error_type = type(error).__name__
    error_msg = str(error)
    traceback_str = traceback.format_exc()

    log_content = (
        f"[{timestamp}] ERROR: {error_type}: {error_msg}\n"
        f"Traceback:\n{traceback_str}\n"
    )
    self._write_log(log_content)

def log_session_start(self) -> None:
    """Log session start with separator"""
    timestamp = self._get_timestamp()
    separator = "=" * 80
    message = f"\n{separator}\nSESSION START: {timestamp}\n{separator}\n"
    self._write_log(message)

def _write_log(self, content: str) -> None:
    """Write to log with rotation and permissions"""
    self._rotate_log_if_needed()

    with open(self.log_file, 'a', encoding='utf-8') as f:
        f.write(content)

    # Ensure 0o600 permissions
    os.chmod(self.log_file, 0o600)
```

### Expected Test Results
```python
# Tests will pass when:
# 1. Timestamp format: YYYY-MM-DDTHH:MM:SS.mmmZ (with milliseconds)
# 2. Timezone: UTC (+00:00)
# 3. Log file permissions: 0o600 (owner read/write only)
# 4. Append mode: Second install preserves first install's logs
# 5. Log rotation: Creates .1, .2, .3 files at 10MB
# 6. Stack trace: Full traceback in log file
# 7. Session separator: "SESSION START:" markers between sessions
```

### Integration Guide
**File to Implement:** `installer/services/install_logger.py`
**Methods:**
- `__init__(log_file: Path, max_size_mb: int, max_rotations: int)`
- `_get_timestamp() -> str` (ISO 8601 with milliseconds)
- `_rotate_log_if_needed() -> None`
- `log_session_start() -> None`
- `log_info(message: str) -> None`
- `log_warning(message: str) -> None`
- `log_error(error: Exception) -> None`
- `log_file_operation(operation: str, source: str, dest: str) -> None`
- `_write_log(content: str) -> None`

**Test Command:**
```bash
pytest installer/tests/test_install_logger.py -v
```

**Expected:** 22/22 passing

---

## 6. Edge Case Tests (5-10 tests)

### Tests Affected
- `test_rollback_fails_when_backup_missing`
- `test_partial_rollback_when_some_files_fail`
- `test_stale_lock_file_removed_automatically`
- `test_malformed_config_uses_defaults`
- `test_disk_full_during_backup`
- `test_readonly_filesystem_error`
- `test_permission_error_during_restore`

### Research Pattern
**Source:** PYTHON-ERROR-HANDLING-RESEARCH-REPORT.md § 3 (JSON/YAML Error Recovery) + § 2 (File System Errors)

**Pattern Name:** Error Categorization with Fallback Strategies

### Implementation Pattern
```python
# Pattern 1: Malformed config fallback
def parse_json_with_fallback(file_path, default_config, logger):
    try:
        # Try full parse
        return json.load(open(file_path))
    except json.JSONDecodeError:
        # Try partial recovery
        content = open(file_path).read()
        recovered = find_valid_json(content)
        if recovered:
            config = default_config.copy()
            config.update(recovered)
            return config
        # Use defaults
        return default_config

# Pattern 2: Partial rollback continues
for file in files_to_restore:
    try:
        restore_file(file)
    except PermissionError:
        logger.error(f"Failed: {file}")
        continue  # Continue with other files
```

### Integration Guide
- Implement JSON recovery in config parsing
- Ensure rollback continues on partial failures
- Add errno checks for disk full/permission errors

**Test Command:**
```bash
pytest installer/tests/test_error_handling_edge_cases.py -v
```

---

## 7. Integration Tests (3-5 tests)

### Tests Affected
- `test_error_after_file_copy_triggers_complete_rollback`
- `test_concurrent_installation_prevented`
- `test_full_workflow_with_error_and_recovery`
- `test_lock_file_prevents_race_condition`
- `test_rollback_performance_under_5_seconds`

### Research Pattern
**Source:** All sections combined (coordinated error handling)

**Pattern Name:** Full Error Recovery Orchestration

### Implementation Pattern
```python
class ErrorRecoveryOrchestrator:
    def handle_error(self, context):
        # 1. Categorize error
        error_category = self.categorizer.categorize(context.error)

        # 2. Log error
        self.logger.log_error(context.error)

        # 3. Rollback if needed
        if context.phase == "file_copy":
            exit_code = self.rollback_service.rollback(
                context.backup_dir,
                context.target_dir
            )
            return ErrorRecoveryResult(exit_code=exit_code)
```

### Integration Guide
**File to Implement:** `installer/error_recovery_orchestrator.py` (already exists, may need fixes)
**Method:** `handle_error(context: ErrorRecoveryContext) -> ErrorRecoveryResult`

**Test Command:**
```bash
pytest installer/tests/integration/test_integration_error_handling.py -v
```

---

## Quick Reference Table

### By Error Type

| Error Type | Research Section | Implementation File | Key Method |
|------------|------------------|-------------------|------------|
| subprocess.TimeoutExpired | § 1 | deployment_engine.py | run_command() |
| OSError (Permission) | § 2 | backup_service.py | _categorize_and_raise() |
| OSError (Disk Full) | § 2 | backup_service.py | _categorize_and_raise() |
| FileNotFoundError | § 2 | rollback_service.py | _restore_from_backup() |
| Lock conflict | § 4 | lock_file_manager.py | acquire_lock() |
| Stale lock | § 4 | lock_file_manager.py | _process_exists() |
| JSON parse error | § 3 | config_parser.py | parse_json_with_fallback() |
| Log rotation needed | § 5 | install_logger.py | _rotate_log_if_needed() |

### By Test File

| Test File | Tests | Implementation | Status |
|-----------|-------|-----------------|--------|
| test_backup_service.py | 18 | BackupService | ✅ Ready |
| test_rollback_service.py | 16 | RollbackService | ✅ Ready |
| test_lock_file_manager.py | 20 | LockFileManager | ✅ Ready |
| test_install_logger.py | 22 | InstallLogger | ✅ Ready |
| test_error_handling_edge_cases.py | 24 | All services | ✅ Ready |
| test_integration_error_handling.py | 11 | Orchestrator | ✅ Ready |
| **TOTAL** | **114** | **4 services** | **✅ Ready** |

---

## Debugging Checklist

When test fails, check:

1. **Import issue?** → `python3 -c "from installer.services.X import Y"`
2. **Method exists?** → `grep "def method_name" installer/services/X.py`
3. **Signature matches?** → Compare with test expectations
4. **Logger parameter?** → Constructor should accept `logger=None`
5. **Return type?** → Check if returns Path (not str) or int (not bool)
6. **Permissions?** → Use `0o600` (octal) not `600` (decimal)
7. **Timezone?** → Use `timezone.utc` not local time

---

## Document References

- **Research Report:** Section numbers (§ 1-8)
- **Implementation Guide:** Service-specific sections
- **STORY-074 File:** `devforgeai/specs/Stories/STORY-074-comprehensive-error-handling.story.md`

---

**End of Test Failure Mapping**

*Use this document to find which research pattern applies to each failing test.*

