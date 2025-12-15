# DevForgeAI Installer

Python-based interactive installer for the DevForgeAI framework.

## Components

### Pre-Flight Validation

The installer performs comprehensive environment validation before making any changes:

#### Validation Checks

1. **Python Version Check** (⚠ WARNING)
   - Detects Python 3.10+ installation
   - Tries multiple executables: python3, python, python3.11, python3.10
   - **Result:** PASS if ≥3.10, WARN if missing/older
   - **Impact:** Python 3.10+ recommended for CLI validators (optional)

2. **Disk Space Check** (✗ FAIL)
   - Calculates available disk space in installation directory
   - **Requirement:** Minimum 100MB free
   - **Result:** PASS if ≥100MB, FAIL if insufficient
   - **Impact:** Installation blocked if disk space too low

3. **Existing Installation Detection** (⚠ WARNING)
   - Checks for `.claude/` or `devforgeai/` directories
   - Reads version information if present
   - **Result:** PASS if none found, WARN if found
   - **Impact:** User prompted to choose: Upgrade, Fresh install, or Cancel

4. **Write Permission Check** (✗ FAIL)
   - Verifies write access to installation directory
   - Creates temporary test file (`devforgeai-write-test`)
   - **Result:** PASS if writable, FAIL if denied
   - **Impact:** Installation blocked if no write permission

#### Validation Summary

After all checks complete, installer displays:

```
═══════════════════════════════════════════════
PRE-FLIGHT VALIDATION RESULTS
═══════════════════════════════════════════════

Python Version          ⚠ WARN    Python 3.9 found (3.10+ recommended)
Disk Space              ✓ PASS    500MB available (required: 100MB)
Existing Installation   ✓ PASS    No previous installation detected
Write Permissions       ✓ PASS    Directory is writable

Overall: Warnings present (can proceed)
```

#### Force Mode

Use `--force` flag to bypass warning prompts:

```bash
python install.py --force
```

**Note:** `--force` only bypasses warnings (⚠ WARN), never critical failures (✗ FAIL).

---

## Error Resolution Guide

### Common Validation Errors

#### Error: Insufficient Disk Space

**Symptom:**
```
✗ FAIL    Insufficient space: 50MB available, 100MB required
```

**Resolution:**
1. Free up disk space:
   ```bash
   # Check disk usage
   df -h /installation/path

   # Remove unnecessary files
   rm -rf /tmp/*
   ```

2. Choose different installation directory:
   ```bash
   python install.py --target /path/with/more/space
   ```

---

#### Error: Write Permission Denied

**Symptom:**
```
✗ FAIL    Write permission denied on /installation/path
```

**Resolution:**
1. **Option A:** Run installer with appropriate permissions:
   ```bash
   # If user-owned directory
   chmod u+w /installation/path

   # If system directory (not recommended)
   sudo python install.py
   ```

2. **Option B:** Choose writable directory (recommended):
   ```bash
   python install.py --target ~/devforgeai
   ```

**Security Note:** Installer never attempts privilege escalation. If permission denied, choose a directory you own.

---

#### Warning: Python Version Too Old

**Symptom:**
```
⚠ WARN    Python 3.9 found (3.10+ recommended). CLI validators disabled.
```

**Resolution:**
1. **Option A:** Upgrade Python:
   ```bash
   # Ubuntu/Debian
   sudo apt install python3.10

   # macOS (Homebrew)
   brew install python@3.10

   # Windows
   # Download from python.org
   ```

2. **Option B:** Proceed without CLI validators:
   - Installation will continue
   - CLI validation tools (`devforgeai-validate`) disabled
   - Framework workflows still functional

---

#### Warning: Existing Installation Detected

**Symptom:**
```
⚠ WARN    Existing DevForgeAI v1.0.0 installation detected at /path
          Choose: [U]pgrade existing, [F]resh install, [C]ancel
```

**Resolution:**
1. **Upgrade (U):** Preserves user data and configurations
   - Updates framework files
   - Keeps `devforgeai/specs/` stories and epics
   - Migrates configuration if needed

2. **Fresh Install (F):** Removes old files completely
   - Backs up old installation to `devforgeai-backup-{timestamp}/`
   - Clean installation from scratch
   - **Warning:** User data not preserved

3. **Cancel (C):** Abort installation
   - No changes made
   - Review existing installation first

---

### Network/Timeout Errors

#### Error: Network Mount Disk Calculation Failed

**Symptom:**
```
⚠ WARN    Error calculating disk space: Network timeout
```

**Resolution:**
1. Check network mount availability:
   ```bash
   ls /network/mount/path
   ```

2. Use local directory instead:
   ```bash
   python install.py --target ~/devforgeai-local
   ```

---

### Cross-Platform Issues

#### Windows: Path with Spaces

**Symptom:**
```
Error: Invalid path 'C:\Program Files\DevForgeAI'
```

**Resolution:**
Use quotes around path:
```bash
python install.py --target "C:\Program Files\DevForgeAI"
```

Or use path without spaces (recommended):
```bash
python install.py --target C:\DevForgeAI
```

---

#### macOS: Permission Denied (SIP)

**Symptom:**
```
✗ FAIL    Permission denied (System Integrity Protection)
```

**Resolution:**
Avoid system-protected directories:
```bash
# Bad: System directory
python install.py --target /usr/local/devforgeai

# Good: User directory
python install.py --target ~/devforgeai
```

---

## Validation Configuration

Configuration file: `src/installer/config/validation_config.py`

```python
# Minimum Python version required (major.minor)
MIN_PYTHON_VERSION = "3.10"

# Minimum disk space required (MB)
MIN_DISK_SPACE_MB = 100

# Validation check timeout (seconds)
CHECK_TIMEOUT_SECONDS = 5

# Python executables to try (in priority order)
PYTHON_EXECUTABLES = ["python3", "python", "python3.11", "python3.10"]
```

---

## Performance Characteristics

- **Total validation time:** <5 seconds (typically ~0.7s)
- **Python check:** <500ms
- **Disk space check:** <200ms
- **Permission check:** <100ms
- **Installation detection:** <1 second

---

## Security

- **No shell injection:** All subprocess calls use `shell=False`
- **No privilege escalation:** Never attempts `sudo` or Run as Administrator
- **Safe file operations:** Uses `pathlib` for cross-platform compatibility
- **Temporary files cleaned:** Test files deleted immediately after checks

---

## Testing

Run validation tests:

```bash
# All validation tests
pytest tests/installer/validators/

# Specific check
pytest tests/installer/validators/test_python_checker.py

# With coverage
pytest tests/installer/validators/ --cov=src/installer/validators --cov-report=term
```

**Test coverage:** 92% (142 tests)

---

## API Reference

### PreFlightValidator

```python
from installer.validators.pre_flight_validator import PreFlightValidator

validator = PreFlightValidator()
result = validator.run()

if result.all_pass:
    print("All checks passed - proceed with installation")
elif result.warnings_present and not result.critical_failures:
    print("Warnings present - user confirmation needed")
else:
    print("Critical failures - installation blocked")
```

### Individual Checkers

```python
from installer.validators import (
    PythonVersionChecker,
    DiskSpaceChecker,
    ExistingInstallationDetector,
    PermissionChecker
)

# Python version check
python_checker = PythonVersionChecker(min_version="3.10")
result = python_checker.check()
print(f"{result.check_name}: {result.status} - {result.message}")

# Disk space check
disk_checker = DiskSpaceChecker(target_path="/install/path", min_space_mb=100)
result = disk_checker.check()

# Existing installation check
install_detector = ExistingInstallationDetector(target_path="/install/path")
result = install_detector.check()

# Permission check
permission_checker = PermissionChecker(target_path="/install/path")
result = permission_checker.check()
```

---

## Related Components

- **Epic:** EPIC-013 (Interactive Installer & Validation)
- **Story:** STORY-072 (Pre-Flight Validation Checks)
- **Dependencies:** Python 3.8+ (3.10+ recommended), standard library only

---

**Last Updated:** 2025-12-03
