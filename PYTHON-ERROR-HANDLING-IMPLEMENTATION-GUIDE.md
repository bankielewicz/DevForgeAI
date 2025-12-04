# Python Error Handling Implementation Guide for STORY-074

**Document Purpose:** Actionable implementation guidance for fixing 25 remaining test failures
**Target Services:** RollbackService, BackupService, LockFileManager, InstallLogger
**Research Basis:** PYTHON-ERROR-HANDLING-RESEARCH-REPORT.md
**Implementation Time:** 3-4 hours for Phase 1 (service interface fixes)

---

## Test Failure Categories and Solutions

### Category 1: Subprocess Timeout Handling (3-5 tests)

**Failing Tests:**
- `test_subprocess_timeout_triggers_error_code_X`
- `test_command_failure_captured_in_log`
- `test_offline_install_network_timeout_recovery`

**Root Cause:** Missing timeout exception handling

**Fix Pattern:**

```python
# FILE: installer/services/deployment_engine.py

import subprocess
import time

class DeploymentEngine:
    def run_command(self, cmd: list, timeout_seconds: int = 30, logger=None) -> int:
        """
        Execute command with timeout and comprehensive error handling.

        Returns: exit code (0 = success)
        Raises: RuntimeError with categorized error message
        """
        try:
            result = subprocess.run(
                cmd,
                timeout=timeout_seconds,
                check=False,  # Don't raise on non-zero
                capture_output=True,
                text=True
            )

            if result.returncode != 0:
                error_msg = result.stderr or result.stdout or "Unknown error"
                if logger:
                    logger.error(f"Command failed: {error_msg}")
                raise RuntimeError(f"Command {cmd[0]} failed: {error_msg}")

            return result.returncode

        except subprocess.TimeoutExpired as e:
            # Timeout - process was killed
            if logger:
                logger.error(f"Command timed out after {timeout_seconds}s: {' '.join(cmd)}")
            raise RuntimeError(f"Timeout: {' '.join(cmd)}") from e

        except FileNotFoundError as e:
            # Executable not found
            if logger:
                logger.error(f"Command not found: {cmd[0]}")
            raise RuntimeError(f"Executable not found: {cmd[0]}") from e
```

**Test Fix Verification:**
```bash
pytest installer/tests/test_deployment_engine.py -k timeout -v
# Should see: "Command timed out after Xs" in exception message
```

---

### Category 2: File System Error Categorization (6-8 tests)

**Failing Tests:**
- `test_backup_fails_on_permission_error`
- `test_disk_full_error_cleanup_partial_backup`
- `test_rollback_handles_readonly_filesystem`
- `test_copy_file_atomic_operation`

**Root Cause:** Missing errno categorization and atomic file operations

**Fix Pattern:**

```python
# FILE: installer/services/backup_service.py

import errno
import os
import tempfile
from pathlib import Path
from typing import List

class BackupService:
    def __init__(self, logger=None):
        self.logger = logger
        self.backup_base = Path(".devforgeai")

    def create_backup(
        self,
        target_dir: Path,
        files_to_backup: List[Path]
    ) -> Path:
        """
        Create timestamped backup with atomic file operations.

        Returns: Path to backup directory
        Raises: RuntimeError with specific error category
        """
        from datetime import datetime

        # Create timestamped backup directory
        timestamp = datetime.now().strftime("%Y-%m-%dT%H-%M-%S")
        backup_dir = self.backup_base / f"backup-{timestamp}"

        try:
            backup_dir.mkdir(parents=True, exist_ok=True)
            self.logger.info(f"Created backup directory: {backup_dir}")
        except OSError as e:
            self._categorize_and_raise(e, "backup directory creation")

        # Copy files with atomic operations
        for file_path in files_to_backup:
            if not file_path.exists():
                self.logger.warning(f"File not found, skipping: {file_path}")
                continue

            try:
                self._copy_file_atomic(file_path, backup_dir, target_dir)
            except RuntimeError as e:
                # Cleanup partial backup on error
                self._cleanup_backup(backup_dir)
                raise

        return backup_dir

    def _copy_file_atomic(
        self,
        src_file: Path,
        backup_dir: Path,
        target_dir: Path
    ) -> None:
        """
        Copy file atomically using write-to-temp-then-rename pattern.
        """
        # Preserve directory structure in backup
        rel_path = src_file.relative_to(target_dir)
        backup_file = backup_dir / rel_path

        # Create subdirectories
        backup_file.parent.mkdir(parents=True, exist_ok=True)

        try:
            # Write to temporary file in same directory (for atomic rename)
            with tempfile.NamedTemporaryFile(
                dir=backup_file.parent,
                delete=False,
                mode='wb'
            ) as tmp_file:
                tmp_path = Path(tmp_file.name)

                try:
                    # Copy in chunks
                    with open(src_file, 'rb') as src_f:
                        while True:
                            chunk = src_f.read(1024 * 1024)  # 1MB chunks
                            if not chunk:
                                break
                            tmp_file.write(chunk)

                    # Flush to disk
                    tmp_file.flush()
                    os.fsync(tmp_file.fileno())

                except (IOError, OSError) as e:
                    tmp_path.unlink(missing_ok=True)
                    self._categorize_and_raise(e, f"copying {src_file}")

            # Atomic rename
            try:
                tmp_path.replace(backup_file)
                self.logger.debug(f"Backed up: {src_file} -> {backup_file}")
            except OSError as e:
                tmp_path.unlink(missing_ok=True)
                self._categorize_and_raise(e, "finalizing backup copy")

        except Exception as e:
            # Cleanup any remaining temp files
            try:
                tmp_path.unlink(missing_ok=True)
            except:
                pass
            raise

    @staticmethod
    def _categorize_and_raise(error: OSError, operation: str) -> None:
        """Categorize OSError and raise with context."""
        if isinstance(error, PermissionError) or error.errno == errno.EACCES:
            raise RuntimeError(
                f"Permission denied during {operation}: {error}\n"
                f"Check directory permissions or run with elevated privileges."
            ) from error
        elif error.errno == errno.ENOSPC:
            raise RuntimeError(
                f"Disk full during {operation}: {error}\n"
                f"Free up disk space and retry."
            ) from error
        elif error.errno == errno.EROFS:
            raise RuntimeError(
                f"Read-only filesystem during {operation}: {error}\n"
                f"Target directory is on read-only filesystem."
            ) from error
        else:
            raise RuntimeError(
                f"File operation failed ({operation}): {error}"
            ) from error

    def _cleanup_backup(self, backup_dir: Path) -> None:
        """Remove backup directory on failure."""
        try:
            import shutil
            shutil.rmtree(backup_dir, ignore_errors=True)
            self.logger.info(f"Cleaned up partial backup: {backup_dir}")
        except Exception as e:
            self.logger.error(f"Failed to cleanup backup {backup_dir}: {e}")
```

**Test Fix Verification:**
```bash
pytest installer/tests/test_backup_service.py -k "permission or disk_full" -v
# Should see specific error messages for each error type
```

---

### Category 3: Atomic Rollback Operations (5-7 tests)

**Failing Tests:**
- `test_rollback_restores_all_files_from_backup`
- `test_rollback_removes_partial_install_files`
- `test_rollback_returns_exit_code_3`
- `test_partial_rollback_continues_on_failure`

**Root Cause:** Missing atomic restore and partial cleanup logic

**Fix Pattern:**

```python
# FILE: installer/services/rollback_service.py

import os
import shutil
from pathlib import Path
from typing import Optional

class RollbackService:
    def __init__(self, logger=None):
        self.logger = logger

    def rollback(
        self,
        backup_dir: Path,
        target_dir: Path
    ) -> int:
        """
        Restore files from backup and cleanup partial installation.

        Returns: 3 (ROLLBACK_OCCURRED)
        Raises: FileNotFoundError if backup_dir doesn't exist
        """
        if not backup_dir.exists():
            raise FileNotFoundError(
                f"Backup directory not found: {backup_dir}\n"
                f"Manual intervention required: Check backup location."
            )

        print("Rolling back installation...")  # Console message (AC#4)

        try:
            # Step 1: Restore files from backup
            restored_count = self._restore_from_backup(backup_dir, target_dir)
            self.logger.info(f"Restored {restored_count} files from backup")

            # Step 2: Remove files created during failed installation
            removed_count = self._remove_created_files(backup_dir, target_dir)
            self.logger.info(f"Removed {removed_count} partial installation files")

            # Step 3: Remove empty directories created during installation
            empty_removed = self._remove_empty_directories(target_dir)
            self.logger.info(f"Removed {empty_removed} empty directories")

            print("Rollback complete. System restored to pre-installation state.")
            return 3  # ROLLBACK_OCCURRED

        except Exception as e:
            # Log error but continue cleanup
            self.logger.error(f"Error during rollback: {e}")
            # Still return 3 - partial rollback is better than nothing
            return 3

    def _restore_from_backup(self, backup_dir: Path, target_dir: Path) -> int:
        """
        Restore all files from backup to target.

        Returns: Number of files restored
        """
        restored_count = 0

        for backup_file in backup_dir.rglob("*"):
            if backup_file.is_file():
                # Calculate target path
                rel_path = backup_file.relative_to(backup_dir)
                target_file = target_dir / rel_path

                # Create parent directories
                target_file.parent.mkdir(parents=True, exist_ok=True)

                try:
                    # Copy from backup to target (overwrite)
                    shutil.copy2(backup_file, target_file)
                    restored_count += 1
                    self.logger.debug(f"Restored: {target_file}")

                except PermissionError as e:
                    # Continue with remaining files even if one fails
                    self.logger.error(f"Failed to restore {target_file}: Permission denied")
                    continue

                except Exception as e:
                    self.logger.error(f"Failed to restore {target_file}: {e}")
                    continue

        return restored_count

    def _remove_created_files(self, backup_dir: Path, target_dir: Path) -> int:
        """
        Remove files created during failed installation (not in backup).

        Returns: Number of files removed
        """
        removed_count = 0

        # Collect files that are in backup
        backup_files = set()
        for backup_file in backup_dir.rglob("*"):
            if backup_file.is_file():
                rel_path = backup_file.relative_to(backup_dir)
                backup_files.add(rel_path)

        # Remove target files not in backup
        if target_dir.exists():
            for target_file in target_dir.rglob("*"):
                if target_file.is_file():
                    rel_path = target_file.relative_to(target_dir)

                    if rel_path not in backup_files:
                        try:
                            target_file.unlink()
                            removed_count += 1
                            self.logger.debug(f"Removed partial file: {target_file}")
                        except Exception as e:
                            self.logger.warning(f"Failed to remove {target_file}: {e}")
                            continue

        return removed_count

    def _remove_empty_directories(self, target_dir: Path) -> int:
        """
        Remove empty directories created during installation.

        Returns: Number of directories removed
        """
        removed_count = 0

        if not target_dir.exists():
            return 0

        # Walk bottom-up (deepest first) to remove empty dirs
        for dir_path in sorted(target_dir.rglob("*"), reverse=True):
            if dir_path.is_dir():
                try:
                    # Try to remove - will succeed only if empty
                    dir_path.rmdir()
                    removed_count += 1
                    self.logger.debug(f"Removed empty directory: {dir_path}")
                except OSError:
                    # Directory not empty or other error - skip
                    continue

        return removed_count
```

**Test Fix Verification:**
```bash
pytest installer/tests/test_rollback_service.py -v
# Should see: restore count > 0, exit code = 3, console message
```

---

### Category 4: PID-Based Lock File Management (5-7 tests)

**Failing Tests:**
- `test_lock_file_prevents_concurrent_install`
- `test_stale_lock_file_removed_automatically`
- `test_lock_file_permission_0600`
- `test_lock_context_manager_cleanup`

**Root Cause:** Missing PID validation and atomic lock creation

**Fix Pattern:**

```python
# FILE: installer/services/lock_file_manager.py

import os
import signal
import time
from pathlib import Path

class LockFileManager:
    """
    Lock file manager with PID validation and stale lock detection.

    Lock file format: .devforgeai/install.lock
    Contents: <pid>:<timestamp>
    """

    def __init__(self, lock_dir: Path = None):
        self.lock_dir = lock_dir or Path(".devforgeai")
        self.lock_file = self.lock_dir / "install.lock"
        self.current_pid = os.getpid()
        self._lock_acquired = False

    def acquire_lock(
        self,
        timeout_seconds: int = 5,
        retry_interval: float = 0.1
    ) -> bool:
        """
        Acquire lock with timeout and retry.

        Returns: True if acquired, False if timeout
        Raises: RuntimeError if concurrent install detected
        """
        self.lock_dir.mkdir(parents=True, exist_ok=True)
        start_time = time.time()

        while True:
            elapsed = time.time() - start_time

            # Check for existing lock
            if self.lock_file.exists():
                try:
                    pid, timestamp = self._read_lock()

                    # Check if process still running (stale detection)
                    if not self._process_exists(pid):
                        # Stale lock - remove and retry
                        self.lock_file.unlink()
                        continue

                    # Process still running - concurrent install
                    raise RuntimeError(
                        f"Installation already in progress (PID {pid}). "
                        f"Remove {self.lock_file} if this is incorrect."
                    )

                except ValueError:
                    # Lock file malformed - remove and retry
                    self.lock_file.unlink(missing_ok=True)
                    continue

            # Try atomic lock creation (O_EXCL ensures atomic)
            try:
                fd = os.open(
                    str(self.lock_file),
                    os.O_CREAT | os.O_EXCL | os.O_WRONLY,
                    0o600  # Permissions: owner read/write only (AC#7 requirement)
                )

                # Write lock contents
                lock_content = f"{self.current_pid}:{time.time()}"
                os.write(fd, lock_content.encode())
                os.close(fd)

                self._lock_acquired = True
                return True

            except FileExistsError:
                # Another process beat us - check timeout
                if elapsed >= timeout_seconds:
                    return False  # Timeout

                time.sleep(retry_interval)

            except PermissionError as e:
                raise RuntimeError(
                    f"Cannot create lock file {self.lock_file}: "
                    f"Permission denied"
                ) from e

    def release_lock(self) -> None:
        """Release lock file."""
        if self.lock_file.exists():
            try:
                pid, _ = self._read_lock()
                if pid == self.current_pid:
                    self.lock_file.unlink()
                    self._lock_acquired = False
            except Exception:
                self.lock_file.unlink(missing_ok=True)

    def _read_lock(self) -> tuple:
        """
        Read lock file.

        Returns: (pid: int, timestamp: float)
        Raises: ValueError if format invalid
        """
        content = self.lock_file.read_text().strip()
        parts = content.split(':')

        if len(parts) != 2:
            raise ValueError(f"Invalid lock format: {content}")

        try:
            pid = int(parts[0])
            timestamp = float(parts[1])
            return (pid, timestamp)
        except ValueError:
            raise ValueError(f"Invalid lock values: {content}")

    @staticmethod
    def _process_exists(pid: int) -> bool:
        """
        Check if process exists (stale lock detection).

        Uses signal(0) which is cross-platform and doesn't kill process.
        """
        if pid <= 0:
            return False

        try:
            # signal(0) = send no signal, just check if process exists
            os.kill(pid, signal.SIG_DFL)
            return True
        except ProcessLookupError:
            # Process doesn't exist
            return False
        except PermissionError:
            # Process exists but different user - treat as existing
            return True
        except Exception:
            # Fail safe - assume process exists
            return True

    def cleanup(self) -> None:
        """Remove lock file on exit."""
        self.release_lock()

    def __enter__(self):
        """Context manager entry."""
        if not self.acquire_lock():
            raise RuntimeError("Could not acquire lock")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.cleanup()
        return False
```

**Test Fix Verification:**
```bash
pytest installer/tests/test_lock_file_manager.py -v
# Should see: lock created with 0o600 perms, stale locks removed
```

---

### Category 5: ISO 8601 Timestamps and Log Rotation (4-6 tests)

**Failing Tests:**
- `test_log_entry_has_iso8601_timestamp`
- `test_log_rotation_at_10mb`
- `test_log_file_permissions_0600`
- `test_log_append_mode_preserves_history`

**Root Cause:** Missing timestamp formatting and log rotation

**Fix Pattern:**

```python
# FILE: installer/services/install_logger.py

import os
from datetime import datetime, timezone
from pathlib import Path

class InstallLogger:
    """
    Installation logger with ISO 8601 timestamps, rotation, and stack traces.
    """

    def __init__(
        self,
        log_file: Path,
        max_size_mb: int = 10,
        max_rotations: int = 3
    ):
        self.log_file = Path(log_file)
        self.max_size_bytes = max_size_mb * 1024 * 1024
        self.max_rotations = max_rotations

        # Create directory
        self.log_file.parent.mkdir(parents=True, exist_ok=True)

        # Set permissions (0600 = owner read/write only) if file exists
        if self.log_file.exists():
            os.chmod(self.log_file, 0o600)

    def _get_timestamp(self) -> str:
        """
        Get ISO 8601 timestamp with milliseconds and UTC timezone.

        Format: 2025-12-04T15:30:45.123456+00:00
        """
        now = datetime.now(timezone.utc)
        # ISO format with microseconds, then replace microseconds with milliseconds
        return now.isoformat(timespec='milliseconds')

    def _rotate_log_if_needed(self) -> None:
        """Rotate log file if exceeding max size."""
        if not self.log_file.exists():
            return

        file_size = self.log_file.stat().st_size
        if file_size < self.max_size_bytes:
            return

        # Rotate: keep last N rotations
        for i in range(self.max_rotations - 1, 0, -1):
            old_file = Path(f"{self.log_file}.{i}")
            new_file = Path(f"{self.log_file}.{i + 1}")

            if old_file.exists():
                if new_file.exists():
                    new_file.unlink()
                old_file.rename(new_file)

        # Move current to .1
        if self.log_file.exists():
            Path(f"{self.log_file}.1").unlink(missing_ok=True)
            self.log_file.rename(f"{self.log_file}.1")

    def log_session_start(self) -> None:
        """Log session start marker."""
        timestamp = self._get_timestamp()
        separator = "=" * 80
        message = f"\n{separator}\nSESSION START: {timestamp}\n{separator}\n"
        self._write_log(message)

    def log_info(self, message: str) -> None:
        """Log informational message."""
        timestamp = self._get_timestamp()
        log_line = f"[{timestamp}] INFO: {message}\n"
        self._write_log(log_line)

    def log_warning(self, message: str) -> None:
        """Log warning message."""
        timestamp = self._get_timestamp()
        log_line = f"[{timestamp}] WARNING: {message}\n"
        self._write_log(log_line)

    def log_error(self, error: Exception) -> None:
        """Log error with full traceback."""
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

    def log_file_operation(self, operation: str, source: str, dest: str) -> None:
        """Log file operation (copy, move, delete)."""
        timestamp = self._get_timestamp()
        log_line = f"[{timestamp}] FILE_OP: {operation} {source} -> {dest}\n"
        self._write_log(log_line)

    def log_system_context(self, context: dict) -> None:
        """Log system context (OS, Python version, etc.)."""
        timestamp = self._get_timestamp()
        context_str = ", ".join(f"{k}={v}" for k, v in context.items())
        log_line = f"[{timestamp}] CONTEXT: {context_str}\n"
        self._write_log(log_line)

    def log_rollback(self, backup_dir: str, files_restored: int) -> None:
        """Log rollback action."""
        timestamp = self._get_timestamp()
        log_line = f"[{timestamp}] ROLLBACK: Restored {files_restored} files from {backup_dir}\n"
        self._write_log(log_line)

    def _write_log(self, content: str) -> None:
        """Write to log file with append mode and rotation."""
        # Rotate if needed
        self._rotate_log_if_needed()

        # Write in append mode
        with open(self.log_file, 'a', encoding='utf-8') as f:
            f.write(content)

        # Ensure correct permissions
        try:
            os.chmod(self.log_file, 0o600)
        except Exception:
            pass  # Non-critical


# USAGE EXAMPLE:
if __name__ == "__main__":
    from pathlib import Path
    import tempfile

    with tempfile.TemporaryDirectory() as tmpdir:
        log_file = Path(tmpdir) / ".devforgeai" / "install.log"
        logger = InstallLogger(log_file)

        logger.log_session_start()
        logger.log_info("Installation started")
        logger.log_file_operation("copy", "/source/file", "/target/file")

        try:
            raise RuntimeError("Test error")
        except Exception as e:
            logger.log_error(e)

        logger.log_rollback("/backup/dir", 5)

        # Verify log contents
        print(log_file.read_text())
```

**Test Fix Verification:**
```bash
pytest installer/tests/test_install_logger.py -v
# Should see: ISO 8601 timestamps, 0600 permissions, rotation logic
```

---

## Integration Test Coverage Map

### Test File: `test_error_handling_edge_cases.py`

| Test Category | Test Name | Fix Applied | Status |
|---------------|-----------|-------------|--------|
| Rollback Failures | `test_rollback_fails_missing_backup` | RollbackService FileNotFoundError | ✅ Ready |
| Rollback Failures | `test_partial_rollback_continues` | RollbackService error handling | ✅ Ready |
| Disk Full | `test_backup_fails_disk_full` | BackupService errno check | ✅ Ready |
| Permission Denied | `test_backup_fails_permission_error` | BackupService PermissionError | ✅ Ready |
| Lock File | `test_stale_lock_removed` | LockFileManager PID check | ✅ Ready |
| Config Parsing | `test_malformed_config_uses_defaults` | ConfigParser fallback | ✅ Ready |
| Interruption | `test_sigint_triggers_rollback` | Signal handler + cleanup | ⏳ Phase 2 |
| Path Sanitization | `test_error_output_sanitizes_paths` | Logger output filtering | ⏳ Phase 2 |

### Test File: `test_integration_error_handling.py`

| Test Category | Test Name | Fix Applied | Status |
|---------------|-----------|-------------|--------|
| Full Rollback | `test_error_after_file_copy_triggers_rollback` | Integration coordination | ✅ Ready |
| Concurrent | `test_concurrent_install_blocked` | LockFileManager | ✅ Ready |
| SIGINT | `test_sigint_graceful_rollback` | Signal handler | ⏳ Phase 2 |
| Performance | `test_rollback_performance_<5s` | Benchmark validation | ✅ Ready |
| Log Output | `test_log_contains_iso8601` | InstallLogger timestamps | ✅ Ready |

---

## Implementation Checklist

### Phase 1: Service Interface Fixes (3-4 hours)

**BackupService** (45 minutes)
- [ ] Fix constructor: accept `logger` parameter
- [ ] Fix `create_backup()` signature: `target_dir, files_to_backup -> Path`
- [ ] Implement atomic file copy with tempfile
- [ ] Add error categorization (errno checks)
- [ ] Run tests: `pytest installer/tests/test_backup_service.py -v`

**RollbackService** (40 minutes)
- [ ] Fix `rollback()` signature: `backup_dir, target_dir -> int`
- [ ] Return exit code 3
- [ ] Implement file restoration from backup
- [ ] Implement partial file cleanup
- [ ] Add console messages
- [ ] Run tests: `pytest installer/tests/test_rollback_service.py -v`

**LockFileManager** (30 minutes)
- [ ] Fix constructor: `lock_dir` parameter
- [ ] Implement `acquire_lock()` with timeout and retry
- [ ] Add PID validation using `os.kill(pid, signal.SIG_DFL)`
- [ ] Implement stale lock detection
- [ ] Add context manager support (`__enter__`, `__exit__`)
- [ ] Run tests: `pytest installer/tests/test_lock_file_manager.py -v`

**InstallLogger** (50 minutes)
- [ ] Fix constructor: `log_file`, `max_size_mb`, `max_rotations`
- [ ] Implement ISO 8601 timestamps (millisecond precision)
- [ ] Add logging methods: `log_info()`, `log_warning()`, `log_error()`, etc.
- [ ] Implement log rotation at 10MB
- [ ] Set file permissions to 0600
- [ ] Run tests: `pytest installer/tests/test_install_logger.py -v`

**Verification** (30 minutes)
- [ ] Run full test suite: `pytest installer/tests/ -v --cov=installer`
- [ ] Verify coverage >95%
- [ ] Verify all 114 tests passing

### Phase 2: Edge Case Coverage (Future)
- [ ] SIGINT/Ctrl+C signal handling
- [ ] Path sanitization in error output
- [ ] Network timeout with exponential backoff
- [ ] Disk full edge case handling
- [ ] Zombie process cleanup

---

## Quick Debugging Tips

### Test Still Failing After Fix?

**Check 1: Import paths**
```bash
python3 -c "from installer.services.backup_service import BackupService; print(BackupService)"
# Should print: <class 'installer.services.backup_service.BackupService'>
```

**Check 2: Method signature**
```python
# In Python REPL:
from installer.services.backup_service import BackupService
import inspect
print(inspect.signature(BackupService.create_backup))
# Should show: (self, target_dir: Path, files_to_backup: List[Path]) -> Path
```

**Check 3: Run single test with verbose output**
```bash
pytest installer/tests/test_backup_service.py::TestBackupService::test_create_backup -vv -s
# -s shows print() output
```

**Check 4: Check test expectations**
```bash
grep -n "expected" installer/tests/test_backup_service.py | head -5
# Find what test expects
```

---

## Code Quality Checklist

Before committing changes:

- [ ] No syntax errors: `python3 -m py_compile src/installer/services/*.py`
- [ ] Imports work: `python3 -c "from installer.services import *"`
- [ ] Logger calls work: `grep -n "self.logger" src/installer/services/*.py` has no typos
- [ ] Path handling uses `Path` objects, not strings
- [ ] errno constants imported: `import errno`
- [ ] Permissions use octal: `0o600` not `600`
- [ ] Timestamps use timezone.utc: `datetime.now(timezone.utc)`
- [ ] File operations wrapped in try-except

---

## Success Metrics

After completing Phase 1:

✅ **114/114 tests passing** (currently 33/114 = 29%)
✅ **Coverage >95%** (business logic + error paths)
✅ **No uncaught exceptions** in service methods
✅ **All console messages** match AC specifications
✅ **Exit codes** correct (0=success, 3=rollback, etc.)
✅ **Log file** contains ISO 8601 timestamps
✅ **Lock file** prevents concurrent installs
✅ **Backup** uses atomic file operations

---

## Reference: Error Categorization by Service

### BackupService
```
OSError
├── PermissionError (errno 13) -> "Permission denied"
├── ENOSPC (errno 28) -> "Disk full"
├── EROFS (errno 30) -> "Read-only filesystem"
└── Other -> "Unknown OSError"
```

### RollbackService
```
Returns: 3 (ROLLBACK_OCCURRED)
Raises: FileNotFoundError if backup missing
Logs: All errors, continues on partial failures
```

### LockFileManager
```
ProcessLookupError -> Stale lock
PermissionError -> Permission denied
FileExistsError -> Lock held by other process
Returns: bool (True=acquired, False=timeout)
```

### InstallLogger
```
All log lines: [ISO8601_TIMESTAMP] LEVEL: message
Timestamps: 2025-12-04T15:30:45.123+00:00 (millisecond precision)
File perms: 0o600
Rotation: At 10MB, keep 3 rotations
```

---

## Related Documents

- **Research Report:** PYTHON-ERROR-HANDLING-RESEARCH-REPORT.md
- **Story File:** `.ai_docs/Stories/STORY-074-comprehensive-error-handling.story.md`
- **Gap Analysis:** STORY-074-GAP-ANALYSIS.md
- **Test Results:** installer/tests/STORY-074-TEST-RESULTS.md

---

**Document Version:** 1.0
**Last Updated:** 2025-12-04
**Implementation Status:** Ready for Phase 1
**Estimated Time to 100% Passing:** 3-4 hours

