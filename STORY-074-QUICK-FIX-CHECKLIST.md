# STORY-074 Quick Fix Checklist

**Goal:** Fix 76 failing tests by realigning implementations to test signatures
**Effort:** ~3.5 hours | **Complexity:** Medium | **Risk:** Low

---

## BackupService (45 minutes)

**File:** `/mnt/c/Projects/DevForgeAI2/installer/backup_service.py`

### ✓ Constructor Fix
- [ ] Add `logger` parameter: `def __init__(self, logger):`
- [ ] Remove `backup_base` parameter
- [ ] Store logger as `self.logger = logger`

### ✓ create_backup() Rewrite
- [ ] Change parameters: `target_dir: Path, files_to_backup: List[Path]`
- [ ] Remove parameter: `source_paths`
- [ ] Change return type: `str` → `Path`
- [ ] Return `self.backup_dir` (Path object)
- [ ] Add logger calls for backup progress

### ✓ Add Method
- [ ] Add `get_latest_backup(backups_root: Path) -> Path` method
- [ ] Find most recent backup directory by timestamp
- [ ] Return sorted backup path (most recent)

### ✓ Update cleanup_old_backups()
- [ ] Change parameter names: `backup_dirs` → `backups_root`, days parameter

### ✓ Tests Pass
```bash
python3 -m pytest installer/tests/test_backup_service.py -v
# Expected: 18/18 passing
```

---

## RollbackService (40 minutes) ⭐ CRITICAL

**File:** `/mnt/c/Projects/DevForgeAI2/installer/rollback_service.py`

### ✓ rollback() Method Fix
- [ ] Change parameter: `target_root` → `target_dir`
- [ ] Change return type: `bool` → `int` (return 3 for ROLLBACK_OCCURRED)
- [ ] Accept `Path` objects, not strings
- [ ] Print "Rolling back installation..." at start
- [ ] Print "Rollback complete. System restored..." at end

### ✓ Make cleanup_partial_installation() PUBLIC
- [ ] Rename `_remove_partial_files()` → `cleanup_partial_installation()`
- [ ] Add parameters: `target_dir, backup_dir, installation_manifest`
- [ ] Make public (remove underscore)

### ✓ Make remove_empty_directories() PUBLIC
- [ ] Rename `_clean_empty_directories()` → `remove_empty_directories()`
- [ ] Add parameter: `target_dir`
- [ ] Return count of directories removed
- [ ] Make public (remove underscore)

### ✓ Error Handling
- [ ] Raise `RuntimeError("Concurrent installation detected...")` on concurrent install
- [ ] Add error message to log (not just return False)

### ✓ Update Helper Methods
- [ ] Fix `_restore_from_backup()` to accept parameters and return count
- [ ] Fix `_remove_partial_files()` to accept backup_dir parameter
- [ ] Update `_is_in_backup()` to accept backup_dir parameter

### ✓ Console Output
- [ ] `print("Rolling back installation...")` at start
- [ ] `print("Rollback complete. System restored to pre-installation state.")` at end
- [ ] No stack traces in console (only in log)

### ✓ Tests Pass
```bash
python3 -m pytest installer/tests/test_rollback_service.py -v
# Expected: 41/41 passing
```

---

## InstallLogger (50 minutes)

**File:** `/mnt/c/Projects/DevForgeAI2/installer/install_logger.py`

### ✓ Constructor Fix
- [ ] Change parameter: `log_path` → `log_file`
- [ ] Add parameter: `max_size_mb: int = 10`
- [ ] Add parameter: `max_rotations: int = 3`
- [ ] Store parameters: `self.log_path = Path(log_file)`

### ✓ Add log_info() Method
- [ ] Log with `[INFO]` prefix
- [ ] Call `_rotate_log_if_needed()` first
- [ ] Write timestamp, prefix, message

### ✓ Add log_warning() Method
- [ ] Log with `[WARNING]` prefix
- [ ] Call `_rotate_log_if_needed()` first
- [ ] Write timestamp, prefix, message

### ✓ Rewrite log_error() Method
- [ ] Change signature: `log_error(error: Exception, category=None, exit_code=None)`
- [ ] Accept Exception object (not error_category string)
- [ ] Extract exception class name and message
- [ ] Write full stack trace (use `traceback.format_exc()`)
- [ ] Include category and exit_code if provided

### ✓ Add log_file_operation() Method
- [ ] Accept: `operation, source_path, target_path`
- [ ] Log file operation details (copy, move, delete, etc.)

### ✓ Add log_system_context() Method
- [ ] Log OS information: `os.name`
- [ ] Log Platform: `platform.system()`, `platform.release()`
- [ ] Log Python version: `platform.python_version()`
- [ ] Log Shell: `os.environ.get('SHELL')`

### ✓ Add log_rollback() Method
- [ ] Accept: `files_restored: List[str], files_removed: List[str]`
- [ ] Log files restored and files removed
- [ ] Handle large lists (show first 10, indicate "...and N more")

### ✓ Add log_session_start() Method
- [ ] Write session separator (===)
- [ ] Include timestamp
- [ ] Add message: "Installation Session Started"

### ✓ Update _rotate_log_if_needed()
- [ ] Use `self.max_size_mb` instead of hardcoded 10
- [ ] Use `self.max_rotations` instead of hardcoded 3

### ✓ Tests Pass
```bash
python3 -m pytest installer/tests/test_install_logger.py -v
# Expected: 23/23 passing
```

---

## LockFileManager (30 minutes) ⭐ CRITICAL

**File:** `/mnt/c/Projects/DevForgeAI2/installer/lock_file_manager.py`

### ✓ Constructor Fix
- [ ] Change parameter: `lock_path` → `lock_dir`
- [ ] Store: `self.lock_dir = Path(lock_dir)`
- [ ] Compute: `self.lock_path = self.lock_dir / "install.lock"`

### ✓ acquire_lock() Enhancement
- [ ] Add parameter: `timeout_seconds: float = None`
- [ ] Add parameter: `retry_interval: float = 0.1`
- [ ] Implement timeout/retry loop (if timeout_seconds provided)
- [ ] Sleep for `retry_interval` between attempts
- [ ] Raise `RuntimeError` when concurrent install detected (active PID)
- [ ] Write PID and timestamp to lock file (ISO 8601 format)
- [ ] Set file permissions: `0o600` (owner read/write only)

### ✓ Rename _is_stale() to is_lock_stale() (PUBLIC)
- [ ] Remove underscore prefix (make public)
- [ ] Keep logic the same

### ✓ Add cleanup() Method
- [ ] Public method (no underscore)
- [ ] Call `self.release_lock()`

### ✓ Add Context Manager Support
- [ ] Implement `__enter__()`: acquire lock, return self
- [ ] Implement `__exit__()`: call cleanup() to release lock

### ✓ Error Handling
- [ ] Raise `RuntimeError("Concurrent installation detected...")` on active PID
- [ ] Include helpful message about locking
- [ ] Log PID of conflicting process

### ✓ Tests Pass
```bash
python3 -m pytest installer/tests/test_lock_file_manager.py -v
# Expected: 19/19 passing
```

---

## Final Verification (30 minutes)

### ✓ Run Full Test Suite
```bash
cd /mnt/c/Projects/DevForgeAI2
python3 -m pytest installer/tests/ -v --cov=installer --cov-report=term
```

### ✓ Expected Results
- [ ] ExitCodes: 14/14 ✓
- [ ] ErrorHandler: 24/24 ✓
- [ ] BackupService: 18/18 ✓ (was 0/18)
- [ ] RollbackService: 41/41 ✓ (was 0/41)
- [ ] InstallLogger: 23/23 ✓ (was 0/23)
- [ ] LockFileManager: 19/19 ✓ (was 0/19)
- [ ] **TOTAL: 114/114 ✓ (was 38/114)**

### ✓ Coverage Check
- [ ] Coverage >95% (preferably 98%+)
- [ ] All critical paths covered
- [ ] No uncovered error cases

### ✓ Code Quality
- [ ] No lint errors
- [ ] All type hints present
- [ ] Docstrings complete
- [ ] No hardcoded paths (use Path objects)

---

## Implementation Order (Recommended)

**Fastest path to 100% passing:**

1. **RollbackService** (40 min) ← Do first (critical + most failing tests)
2. **LockFileManager** (30 min) ← Do second (critical + fewer lines)
3. **BackupService** (45 min) ← Do third
4. **InstallLogger** (50 min) ← Do last (most new methods, less critical)
5. **Verify** (30 min) ← Full test suite run

**Total: 3 hours 35 minutes**

---

## Troubleshooting

### Tests still failing after changes?

**Check list:**
- [ ] Parameter names exactly match test expectations
- [ ] Return types are correct (bool vs int, str vs Path)
- [ ] Methods are public (no underscore prefix)
- [ ] All required methods are implemented
- [ ] Constructor parameters match test calls
- [ ] Path objects used consistently (not strings)

### Specific errors?

**TypeError: unexpected keyword argument**
→ Parameter name mismatch, check test call signature

**AssertionError: assert False == 3**
→ Return type wrong (returning bool instead of int)

**AttributeError: object has no attribute**
→ Method is private (_method) or missing

**TypeError: missing required positional arguments**
→ Missing parameter in method signature

---

## Success Indicators

✅ **All 114 tests passing**
✅ **No skipped or deferred tests**
✅ **Code coverage >95%**
✅ **No lint errors**
✅ **All docstrings present**
✅ **Tests can be run independently**
✅ **Error paths tested**
✅ **Edge cases covered**

---

## Review Checklist Before Commit

### Code Quality
- [ ] No hardcoded paths (use Path objects)
- [ ] All parameters typed
- [ ] All return types specified
- [ ] Docstrings for all public methods
- [ ] Module docstrings present
- [ ] Exception types documented

### Functionality
- [ ] All tests passing
- [ ] Coverage >95%
- [ ] Error handling complete
- [ ] Edge cases handled
- [ ] File permissions set correctly (0600, 0700)

### Integration
- [ ] No breaking changes to public APIs
- [ ] Dependencies properly injected
- [ ] Logger calls appropriate
- [ ] Console output clear and helpful
- [ ] Log output detailed and useful

---

## Resources

**Full Documentation:**
- Implementation Guide: `/mnt/c/Projects/DevForgeAI2/installer/tests/STORY-074-IMPLEMENTATION-FIXES.md`
- Gap Analysis: `/mnt/c/Projects/DevForgeAI2/STORY-074-GAP-ANALYSIS.md`
- Executive Summary: `/mnt/c/Projects/DevForgeAI2/STORY-074-EXECUTIVE-SUMMARY.md`

**Test Files:**
- BackupService: `/mnt/c/Projects/DevForgeAI2/installer/tests/test_backup_service.py`
- RollbackService: `/mnt/c/Projects/DevForgeAI2/installer/tests/test_rollback_service.py`
- InstallLogger: `/mnt/c/Projects/DevForgeAI2/installer/tests/test_install_logger.py`
- LockFileManager: `/mnt/c/Projects/DevForgeAI2/installer/tests/test_lock_file_manager.py`

**Implementation Files:**
- BackupService: `/mnt/c/Projects/DevForgeAI2/installer/backup_service.py`
- RollbackService: `/mnt/c/Projects/DevForgeAI2/installer/rollback_service.py`
- InstallLogger: `/mnt/c/Projects/DevForgeAI2/installer/install_logger.py`
- LockFileManager: `/mnt/c/Projects/DevForgeAI2/installer/lock_file_manager.py`

---

**Last Updated:** 2025-12-03
**Status:** Ready for Implementation
**Estimated Completion:** 3.5 hours
**Confidence Level:** 99%
