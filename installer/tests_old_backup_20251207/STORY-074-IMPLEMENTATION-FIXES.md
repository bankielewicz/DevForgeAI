# STORY-074 Implementation Fixes - Detailed Code Changes

**Purpose:** Fix signature mismatches between tests and implementations
**Approach:** Realign implementations to match test-driven specifications
**Expected Result:** 76 failing tests become passing

---

## Fix #1: BackupService Constructor and Method Signatures

### Current Code (WRONG)
```python
class BackupService:
    def __init__(self, backup_base: str = ".devforgeai"):
        self.backup_base = Path(backup_base)

    def create_backup(self, source_paths: List[str]) -> str:
        # ... creates backup directory
        return str(self.backup_dir)
```

### What Tests Expect
```python
from unittest.mock import Mock

# Constructor should accept logger
service = BackupService(logger=Mock())

# create_backup() should accept target_dir and files_to_backup (Path objects)
backup_dir = service.create_backup(
    target_dir=tmp_path / "target",        # Path object
    files_to_backup=[tmp_path / "file.txt"]  # List[Path]
)

# Return type should be Path
assert isinstance(backup_dir, Path)
assert backup_dir.exists()

# Should support getting latest backup
latest = service.get_latest_backup(backups_root=Path(".devforgeai"))
```

### Changes Required

**1. Update __init__() signature:**
```python
def __init__(self, logger):  # Add logger parameter
    """Initialize backup service with logger dependency."""
    self.logger = logger
    self.backup_base = Path(".devforgeai")
    self.backup_base.mkdir(parents=True, exist_ok=True)
    self.backup_dir: Optional[Path] = None
```

**2. Rewrite create_backup() signature:**
```python
def create_backup(self, target_dir: Path, files_to_backup: List[Path]) -> Path:
    """Create timestamped backup of files before they're modified.

    Args:
        target_dir: Target directory containing files to backup
        files_to_backup: List of file paths to backup (from target_dir)

    Returns:
        Path to created backup directory (e.g., devforgeai/install-backup-2025-12-03T...)

    Raises:
        PermissionError: If backup directory creation fails
    """
    timestamp = self._get_timestamp()
    self.backup_dir = self.backup_base / f"install-backup-{timestamp}"

    try:
        self.backup_dir.mkdir(parents=True, exist_ok=True)

        # Log backup creation start
        if self.logger:
            self.logger.log_info(f"Creating backup: {self.backup_dir}")

        backed_up_count = 0
        for file_path in files_to_backup:
            if not file_path.exists():
                if self.logger:
                    self.logger.log_warning(f"File not found, skipping: {file_path}")
                continue

            # Preserve relative directory structure in backup
            rel_path = file_path.relative_to(target_dir)
            dest = self.backup_dir / rel_path

            if file_path.is_file():
                dest.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(file_path, dest)
                backed_up_count += 1
            elif file_path.is_dir():
                dest.mkdir(parents=True, exist_ok=True)
                shutil.copytree(file_path, dest, dirs_exist_ok=True)

        # Set permissions (0700 - owner access only)
        self.backup_dir.chmod(0o700)

        if self.logger:
            self.logger.log_info(f"Backup created: {backed_up_count} files backed up")

        return self.backup_dir  # Return Path, not str!

    except PermissionError as e:
        # Clean up partial backup on failure
        if self.backup_dir and self.backup_dir.exists():
            shutil.rmtree(self.backup_dir, ignore_errors=True)
        raise
```

**3. Add get_latest_backup() method:**
```python
def get_latest_backup(self, backups_root: Path) -> Optional[Path]:
    """Get the most recent backup directory.

    Args:
        backups_root: Root directory containing backups

    Returns:
        Path to most recent backup, or None if no backups exist
    """
    backup_dirs = [
        d for d in backups_root.iterdir()
        if d.is_dir() and d.name.startswith('install-backup-')
    ]

    if not backup_dirs:
        return None

    # Sort by name (ISO 8601 format sorts chronologically)
    return sorted(backup_dirs)[-1]
```

**4. Update cleanup_old_backups() signature:**
```python
def cleanup_old_backups(self, backups_root: Path, days: int = 7) -> None:
    """Clean up old backups (>N days, keep last 5).

    Args:
        backups_root: Root directory containing backups
        days: Delete backups older than this many days
    """
    # Keep implementation logic, just update parameter names
    backup_dirs = sorted([d for d in backups_root.iterdir()
                        if d.is_dir() and d.name.startswith('install-backup-')],
                       key=lambda x: x.name, reverse=True)

    from time import time
    now = time()
    max_age_seconds = days * 24 * 60 * 60

    for backup_dir in backup_dirs[5:]:  # Keep at least 5
        if now - backup_dir.stat().st_mtime > max_age_seconds:
            shutil.rmtree(backup_dir, ignore_errors=True)
```

---

## Fix #2: RollbackService Method Signatures and Return Types

### Current Code (WRONG)
```python
class RollbackService:
    def rollback(self, backup_dir: str, target_root: Optional[str] = None) -> bool:
        # ... restore from backup
        return True  # Returns bool, not int!

    def _remove_partial_files(self) -> None:  # PRIVATE - tests expect PUBLIC
        pass

    def _clean_empty_directories(self) -> None:  # PRIVATE - tests expect PUBLIC
        pass
```

### What Tests Expect
```python
service = RollbackService(logger=mock_logger)

# rollback() should accept target_dir parameter
exit_code = service.rollback(
    backup_dir=tmp_path / "backup",  # Path object
    target_dir=tmp_path / "target"   # Changed from target_root!
)

# Return type should be int (exit code 3)
assert exit_code == 3

# cleanup_partial_installation() should be PUBLIC method
service.cleanup_partial_installation(
    target_dir=tmp_path / "target",
    backup_dir=tmp_path / "backup",
    installation_manifest=[tmp_path / "new_file.txt"]
)

# remove_empty_directories() should be PUBLIC method
service.remove_empty_directories(tmp_path / "target")

# Console output expected
# "Rolling back installation..."
# "Rollback complete. System restored to pre-installation state."
```

### Changes Required

**1. Fix rollback() signature:**
```python
def rollback(self, backup_dir: Path, target_dir: Path) -> int:
    """Execute full rollback: restore from backup, remove partials, clean dirs.

    Args:
        backup_dir: Path to backup directory
        target_dir: Path to target directory (where files were being installed)

    Returns:
        Exit code 3 (ROLLBACK_OCCURRED) on success

    Raises:
        FileNotFoundError: If backup directory doesn't exist
    """
    try:
        # Display user-friendly message (no stack traces)
        print("Rolling back installation...")

        if self.logger:
            self.logger.log_info(f"ROLLBACK_START from backup {backup_dir}")

        # Restore files from backup
        restored_count = self._restore_from_backup(backup_dir, target_dir)

        # Remove partial files created during failed installation
        removed_count = self._remove_partial_files(target_dir, backup_dir)

        # Clean up empty directories created during installation
        empty_dir_count = self._clean_empty_directories(target_dir)

        print("Rollback complete. System restored to pre-installation state.")

        if self.logger:
            self.logger.log_rollback(
                files_restored=[str(p) for p in range(restored_count)],
                files_removed=[str(p) for p in range(removed_count)]
            )
            self.logger.log_info("ROLLBACK_COMPLETE")

        return 3  # ROLLBACK_OCCURRED exit code

    except FileNotFoundError as e:
        error_msg = f"Backup directory not found: {backup_dir}. Manual intervention required."
        if self.logger:
            self.logger.log_error(e, category="ROLLBACK_FAILED", exit_code=3)
        raise FileNotFoundError(error_msg)

    except Exception as e:
        if self.logger:
            self.logger.log_error(e, category="ROLLBACK_FAILED", exit_code=3)
        return 3
```

**2. Rewrite _restore_from_backup() to accept parameters:**
```python
def _restore_from_backup(self, backup_dir: Path, target_dir: Path) -> int:
    """Restore all files from backup directory.

    Returns:
        Number of files restored
    """
    if not backup_dir.exists():
        raise FileNotFoundError(f"Backup directory not found: {backup_dir}")

    restored_count = 0
    for backup_file in backup_dir.rglob("*"):
        if backup_file.is_file():
            rel_path = backup_file.relative_to(backup_dir)
            target_file = target_dir / rel_path

            try:
                target_file.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(backup_file, target_file)
                restored_count += 1

                if self.logger:
                    self.logger.log_info(f"RESTORED: {target_file}")
            except Exception as e:
                if self.logger:
                    self.logger.log_warning(f"Failed to restore {target_file}: {e}")

    return restored_count
```

**3. Make cleanup_partial_installation() PUBLIC:**
```python
def cleanup_partial_installation(self, target_dir: Path, backup_dir: Path,
                                 installation_manifest: List[Path]) -> None:
    """Remove files created but not in backup.

    Args:
        target_dir: Target installation directory
        backup_dir: Backup directory containing pre-installation files
        installation_manifest: List of files created during failed installation
    """
    for file_path in installation_manifest:
        if file_path.exists() and not self._is_in_backup(file_path, backup_dir):
            try:
                file_path.unlink()
                if self.logger:
                    self.logger.log_info(f"REMOVED_PARTIAL: {file_path}")
            except Exception as e:
                if self.logger:
                    self.logger.log_warning(f"Failed to remove {file_path}: {e}")
```

**4. Make remove_empty_directories() PUBLIC:**
```python
def remove_empty_directories(self, target_dir: Path) -> int:
    """Remove empty directories created during installation.

    Args:
        target_dir: Target directory to clean

    Returns:
        Number of empty directories removed
    """
    removed_count = 0
    # Walk from deepest to shallowest
    for dir_path in sorted(target_dir.rglob("*"), key=lambda p: len(p.parts), reverse=True):
        if dir_path.is_dir() and not any(dir_path.iterdir()):
            try:
                dir_path.rmdir()
                removed_count += 1
                if self.logger:
                    self.logger.log_info(f"REMOVED_EMPTY_DIR: {dir_path}")
            except Exception:
                pass  # Directory not empty or removal failed

    return removed_count
```

**5. Update _remove_partial_files() to accept parameters:**
```python
def _remove_partial_files(self, target_dir: Path, backup_dir: Path) -> int:
    """Remove files that were created but not in backup.

    Returns:
        Number of partial files removed
    """
    removed_count = 0
    for file_path in self.files_created:
        if file_path.exists() and not self._is_in_backup(file_path, backup_dir):
            try:
                file_path.unlink()
                removed_count += 1
                if self.logger:
                    self.logger.log_info(f"REMOVED_PARTIAL: {file_path}")
            except Exception as e:
                if self.logger:
                    self.logger.log_warning(f"Remove partial failed {file_path}: {e}")

    return removed_count
```

**6. Fix is_in_backup() helper:**
```python
def _is_in_backup(self, file_path: Path, backup_dir: Path) -> bool:
    """Check if file exists in backup directory."""
    if not backup_dir.exists():
        return False

    try:
        rel_path = file_path.relative_to(file_path.parent.parent)
        return (backup_dir / rel_path).exists()
    except ValueError:
        return False
```

---

## Fix #3: InstallLogger Methods and Signatures

### Current Code (WRONG)
```python
class InstallLogger:
    def __init__(self, log_path: str = "devforgeai/install.log"):  # Wrong param name
        pass

    # Missing: log_info(), log_warning()
    # Wrong: log_error() signature
```

### What Tests Expect
```python
logger = InstallLogger(log_file=tmp_path / "install.log")  # Parameter name!
logger = InstallLogger(
    log_file=tmp_path / "install.log",
    max_size_mb=10,
    max_rotations=3
)

# log_info() for INFO level
logger.log_info("Installation started")

# log_warning() for WARNING level
logger.log_warning("File not found, skipping")

# log_error() with exception object
try:
    raise FileNotFoundError("Missing source")
except FileNotFoundError as e:
    logger.log_error(e, category="MISSING_SOURCE", exit_code=1)

# Specialized logging
logger.log_file_operation(
    operation="copy",
    source_path="/source/file.txt",
    target_path="/target/file.txt"
)
logger.log_system_context()
logger.log_rollback(files_restored=["file1.txt"], files_removed=["partial.txt"])
logger.log_session_start()
```

### Changes Required

**1. Fix __init__() signature:**
```python
def __init__(self, log_file: Path, max_size_mb: int = 10, max_rotations: int = 3):
    """Initialize logger with target log file path.

    Args:
        log_file: Path to log file
        max_size_mb: Maximum log file size before rotation (default 10MB)
        max_rotations: Number of rotations to keep (default 3)
    """
    self.log_path = Path(log_file)
    self.max_size_mb = max_size_mb
    self.max_rotations = max_rotations
    self._ensure_log_dir()
    self._set_permissions()
```

**2. Add log_info() method:**
```python
def log_info(self, message: str) -> None:
    """Log INFO level message.

    Args:
        message: Message to log
    """
    self._rotate_log_if_needed()

    timestamp = self._get_iso_timestamp()
    log_entry = f"[{timestamp}] [INFO] {message}\n"

    with open(self.log_path, 'a') as f:
        f.write(log_entry)

    self._set_permissions()
```

**3. Add log_warning() method:**
```python
def log_warning(self, message: str) -> None:
    """Log WARNING level message.

    Args:
        message: Message to log
    """
    self._rotate_log_if_needed()

    timestamp = self._get_iso_timestamp()
    log_entry = f"[{timestamp}] [WARNING] {message}\n"

    with open(self.log_path, 'a') as f:
        f.write(log_entry)

    self._set_permissions()
```

**4. Rewrite log_error() signature:**
```python
def log_error(self, error: Exception, category: str = None, exit_code: int = None) -> None:
    """Log ERROR level message with full stack trace.

    Args:
        error: Exception object
        category: Error category (e.g., MISSING_SOURCE)
        exit_code: Exit code integer
    """
    self._rotate_log_if_needed()

    timestamp = self._get_iso_timestamp()
    log_entry = f"[{timestamp}] [ERROR] {error.__class__.__name__}\n"

    if category:
        log_entry += f"  Category: {category}\n"

    if exit_code is not None:
        log_entry += f"  Exit Code: {exit_code}\n"

    log_entry += f"  Message: {str(error)}\n"

    # Add full stack trace
    import traceback
    stack_trace = traceback.format_exc()
    if "Traceback" in stack_trace:
        log_entry += f"  Stack Trace:\n{stack_trace}\n"

    log_entry += f"  OS: {os.name}\n\n"

    with open(self.log_path, 'a') as f:
        f.write(log_entry)

    self._set_permissions()
```

**5. Add log_file_operation() method:**
```python
def log_file_operation(self, operation: str, source_path: str, target_path: str) -> None:
    """Log file operation (copy, move, delete, etc.).

    Args:
        operation: Operation type (copy, move, delete, etc.)
        source_path: Source file path
        target_path: Target file path
    """
    self._rotate_log_if_needed()

    timestamp = self._get_iso_timestamp()
    log_entry = f"[{timestamp}] [INFO] FILE_OP: {operation}\n"
    log_entry += f"  Source: {source_path}\n"
    log_entry += f"  Target: {target_path}\n\n"

    with open(self.log_path, 'a') as f:
        f.write(log_entry)

    self._set_permissions()
```

**6. Add log_system_context() method:**
```python
def log_system_context(self) -> None:
    """Log system context information (OS, shell version, etc.)."""
    self._rotate_log_if_needed()

    timestamp = self._get_iso_timestamp()
    import platform

    log_entry = f"[{timestamp}] [INFO] SYSTEM_CONTEXT\n"
    log_entry += f"  OS: {os.name}\n"
    log_entry += f"  Platform: {platform.system()} {platform.release()}\n"
    log_entry += f"  Python: {platform.python_version()}\n"
    log_entry += f"  Shell: {os.environ.get('SHELL', 'unknown')}\n\n"

    with open(self.log_path, 'a') as f:
        f.write(log_entry)

    self._set_permissions()
```

**7. Add log_rollback() method:**
```python
def log_rollback(self, files_restored: List[str], files_removed: List[str]) -> None:
    """Log rollback actions taken.

    Args:
        files_restored: List of files restored from backup
        files_removed: List of partial files removed
    """
    self._rotate_log_if_needed()

    timestamp = self._get_iso_timestamp()
    log_entry = f"[{timestamp}] [INFO] ROLLBACK_SUMMARY\n"
    log_entry += f"  Files Restored: {len(files_restored)}\n"

    for file_path in files_restored[:10]:  # Log first 10
        log_entry += f"    - {file_path}\n"

    if len(files_restored) > 10:
        log_entry += f"    ... and {len(files_restored) - 10} more\n"

    log_entry += f"  Files Removed: {len(files_removed)}\n"

    for file_path in files_removed[:10]:  # Log first 10
        log_entry += f"    - {file_path}\n"

    if len(files_removed) > 10:
        log_entry += f"    ... and {len(files_removed) - 10} more\n"

    log_entry += "\n"

    with open(self.log_path, 'a') as f:
        f.write(log_entry)

    self._set_permissions()
```

**8. Add log_session_start() method:**
```python
def log_session_start(self) -> None:
    """Log installation session separator."""
    self._rotate_log_if_needed()

    timestamp = self._get_iso_timestamp()
    log_entry = "\n" + "="*80 + "\n"
    log_entry += f"[{timestamp}] === Installation Session Started ===\n"
    log_entry += "="*80 + "\n\n"

    with open(self.log_path, 'a') as f:
        f.write(log_entry)

    self._set_permissions()
```

**9. Update _rotate_log_if_needed():**
```python
def _rotate_log_if_needed(self) -> None:
    """Rotate log file when exceeding max_size_mb."""
    if not self.log_path.exists():
        return

    max_size_bytes = self.max_size_mb * 1024 * 1024

    if self.log_path.stat().st_size > max_size_bytes:
        # Shift rotation files
        for i in range(self.max_rotations - 1, 0, -1):
            old_path = Path(f"{self.log_path}.{i}")
            new_path = Path(f"{self.log_path}.{i + 1}")

            if old_path.exists():
                if i + 1 <= self.max_rotations:
                    old_path.rename(new_path)
                else:
                    old_path.unlink()

        # Rename current log to .1
        self.log_path.rename(Path(f"{self.log_path}.1"))
        self._set_permissions()
```

---

## Fix #4: LockFileManager Constructor and Methods

### Current Code (WRONG)
```python
class LockFileManager:
    def __init__(self, lock_path: str = "devforgeai/install.lock"):  # Wrong param!
        pass

    # Missing: cleanup(), context manager support
    # Wrong visibility: _is_stale() should be public
    # Missing: timeout support
```

### What Tests Expect
```python
manager = LockFileManager(lock_dir=tmp_path / ".devforgeai")  # Parameter name!

# Normal acquire
success = manager.acquire_lock()  # Returns bool
assert success is True

# With timeout
success = manager.acquire_lock(timeout_seconds=2, retry_interval=0.1)

# Public method to check staleness
is_stale = manager.is_lock_stale()  # Not _is_stale()!

# Cleanup method
manager.cleanup()

# Context manager support
with LockFileManager(lock_dir=lock_dir) as mgr:
    # Lock is held
    assert (lock_dir / "install.lock").exists()
# Lock released after context exit
assert not (lock_dir / "install.lock").exists()

# Raise RuntimeError on concurrent (not return False)
with pytest.raises(RuntimeError) as exc_info:
    manager2.acquire_lock()
assert "concurrent" in str(exc_info.value).lower()
```

### Changes Required

**1. Fix __init__() signature:**
```python
def __init__(self, lock_dir: Path):
    """Initialize lock file manager.

    Args:
        lock_dir: Directory where devforgeai/install.lock will be created
    """
    self.lock_dir = Path(lock_dir)
    self.lock_dir.mkdir(parents=True, exist_ok=True)
    self.lock_path = self.lock_dir / "install.lock"
```

**2. Update acquire_lock() with timeout support:**
```python
def acquire_lock(self, timeout_seconds: float = None, retry_interval: float = 0.1) -> bool:
    """Create lock file with current process ID.

    Args:
        timeout_seconds: Max seconds to wait for lock (None = no wait)
        retry_interval: Seconds between retry attempts

    Returns:
        True if lock acquired

    Raises:
        RuntimeError: If concurrent installation detected (active PID)
    """
    import time

    start_time = time.time()

    while True:
        # Check for existing lock with active PID
        if self.lock_path.exists():
            if not self._is_stale():
                # Lock held by active process
                error_msg = "Concurrent installation detected. Another installer is running."
                raise RuntimeError(error_msg)
            else:
                # Remove stale lock
                try:
                    self.lock_path.unlink()
                except Exception:
                    pass

        # Try to create new lock file with PID
        try:
            # Write PID and timestamp atomically
            from datetime import datetime
            timestamp = datetime.now().isoformat()
            lock_content = f"{os.getpid()}\n{timestamp}\n"

            # Use temporary file for atomic write
            temp_path = self.lock_path.parent / f".lock.tmp.{os.getpid()}"
            with open(temp_path, 'w') as f:
                f.write(lock_content)

            # Atomic rename
            temp_path.rename(self.lock_path)

            # Set permissions (0600 - owner read/write only)
            self.lock_path.chmod(0o600)

            return True

        except FileExistsError:
            # Race condition - another process created it
            # Check if it's stale or active
            if timeout_seconds is None:
                # No timeout, raise error immediately
                if self.lock_path.exists() and not self._is_stale():
                    error_msg = "Concurrent installation detected. Another installer is running."
                    raise RuntimeError(error_msg)
            else:
                # With timeout, retry
                elapsed = time.time() - start_time
                if elapsed >= timeout_seconds:
                    raise RuntimeError("Concurrent installation detected. Lock acquisition timeout.")

                time.sleep(retry_interval)
                continue

        except Exception:
            return False
```

**3. Add cleanup() method:**
```python
def cleanup(self) -> None:
    """Clean up lock file (called on exit or exception)."""
    self.release_lock()
```

**4. Rename _is_stale() to public is_lock_stale():**
```python
def is_lock_stale(self) -> bool:
    """Check if lock file has dead process PID.

    Returns:
        True if lock is stale (process dead), False if active
    """
    if not self.lock_path.exists():
        return True

    try:
        with open(self.lock_path, 'r') as f:
            pid_str = f.read().strip().split('\n')[0]  # Get first line (PID)

        # Try to parse PID
        try:
            pid = int(pid_str)
        except ValueError:
            return True  # Invalid PID format, consider stale

        # Check if process is running
        return not self._process_exists(pid)

    except Exception:
        return True
```

**5. Update release_lock() to use correct path:**
```python
def release_lock(self) -> None:
    """Remove lock file."""
    if self.lock_path.exists():
        try:
            self.lock_path.unlink()
        except Exception:
            pass
```

**6. Add context manager support:**
```python
def __enter__(self):
    """Enter context manager (acquire lock)."""
    self.acquire_lock()
    return self

def __exit__(self, exc_type, exc_val, exc_tb):
    """Exit context manager (release lock)."""
    self.cleanup()
    return False  # Don't suppress exceptions
```

**7. Keep is_locked() and get_locked_pid() as-is:**
```python
def is_locked(self) -> bool:
    """Check if installation is currently locked."""
    if not self.lock_path.exists():
        return False
    return not self.is_lock_stale()  # Use public version

def get_locked_pid(self) -> Optional[int]:
    """Return PID of process holding lock, or None."""
    if not self.lock_path.exists():
        return None

    try:
        with open(self.lock_path, 'r') as f:
            return int(f.read().strip().split('\n')[0])
    except Exception:
        return None
```

---

## Summary of Changes

### BackupService
- ✅ Fix constructor: add `logger` parameter
- ✅ Fix create_backup(): accept `target_dir` and `files_to_backup` (Path objects)
- ✅ Fix return type: str → Path
- ✅ Add get_latest_backup() method
- ✅ Update cleanup_old_backups() parameter names

### RollbackService
- ✅ Fix rollback(): change `target_root` → `target_dir`
- ✅ Fix return type: bool → int (exit code 3)
- ✅ Make cleanup_partial_installation() public
- ✅ Make remove_empty_directories() public
- ✅ Add console output messages
- ✅ Raise RuntimeError on concurrent install

### InstallLogger
- ✅ Fix constructor param: `log_path` → `log_file`
- ✅ Add max_size_mb and max_rotations parameters
- ✅ Add log_info() method
- ✅ Add log_warning() method
- ✅ Rewrite log_error() signature
- ✅ Add log_file_operation() method
- ✅ Add log_system_context() method
- ✅ Add log_rollback() method
- ✅ Add log_session_start() method

### LockFileManager
- ✅ Fix constructor param: `lock_path` → `lock_dir`
- ✅ Add timeout_seconds and retry_interval to acquire_lock()
- ✅ Make is_lock_stale() public (was _is_stale())
- ✅ Add cleanup() method
- ✅ Implement context manager (__enter__, __exit__)
- ✅ Raise RuntimeError on concurrent install

---

## Verification Steps

After making changes, run:

```bash
# Test individual services
python3 -m pytest installer/tests/test_backup_service.py -v
python3 -m pytest installer/tests/test_rollback_service.py -v
python3 -m pytest installer/tests/test_install_logger.py -v
python3 -m pytest installer/tests/test_lock_file_manager.py -v

# Test all services
python3 -m pytest installer/tests/test_*.py -v --cov=installer

# Expected: 114/114 tests passing (100%)
```

---

## Implementation Timeline

| Service | Estimated Time | Critical | Notes |
|---------|----------------|----------|-------|
| BackupService | 45 minutes | No | Read/write to disk, structure preservation |
| RollbackService | 40 minutes | YES | Must return exit code, console output |
| InstallLogger | 50 minutes | No | 6 new methods to implement |
| LockFileManager | 30 minutes | YES | Context manager, timeout handling |
| **Total** | **~3.5 hours** | - | Verification + testing included |

**Priority:** RollbackService and LockFileManager (critical for exit codes and error handling)

