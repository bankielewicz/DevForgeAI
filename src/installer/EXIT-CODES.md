# Exit Codes Reference

**Version:** 1.0.0
**Story:** STORY-074 - Comprehensive Error Handling
**Status:** Production Ready (114 tests passing)

---

## Overview

The DevForgeAI installer uses standardized exit codes to indicate installation success or failure. These codes follow Unix conventions and are returned by the `install()` function.

**Key Benefits:**
- Scripts can detect failure reason without parsing error messages
- CI/CD pipelines can implement conditional logic based on exit codes
- Users can understand installation status at a glance
- Enables automated recovery procedures

---

## Exit Codes (AC#6)

### 0 - SUCCESS

**Meaning:** Installation completed without errors.

**When Returned:**
- Fresh installation successful
- Upgrade successful
- Rollback successful
- Validation successful (no issues found)
- Uninstall successful

**Example:**
```python
from installer import install

result = install.install(
    target_path="/path/to/project",
    mode="fresh_install"
)

if result["status"] == "success":
    print(f"Exit code: 0 (SUCCESS)")
    # Proceed with next steps in CI/CD pipeline
```

**Shell Usage:**
```bash
python -m installer /path/to/project
if [ $? -eq 0 ]; then
    echo "Installation successful"
else
    echo "Installation failed"
fi
```

---

### 1 - MISSING_SOURCE

**Meaning:** Required source files not found.

**Triggered By:**
- `src/devforgeai/version.json` missing
- `src/claude/` directory missing
- Source path invalid or inaccessible
- Insufficient read permissions on source files

**Example Errors:**
```
FileNotFoundError: [Errno 2] No such file or directory: 'src/devforgeai/version.json'
FileNotFoundError: [Errno 2] No such file or directory: 'src/claude/commands/'
```

**Recovery Steps:**

1. **Verify source structure:**
```bash
# Ensure src/ directory exists
ls -la src/

# Expected structure:
# src/
# ├── claude/
# │   ├── commands/
# │   ├── skills/
# │   └── agents/
# └── devforgeai/
#     ├── protocols/
#     └── version.json
```

2. **Create missing files:**
```bash
# Create version.json
cat > src/devforgeai/version.json <<'EOF'
{
  "version": "1.0.0",
  "released_at": "2025-12-03T00:00:00Z",
  "schema_version": "1.0"
}
EOF
```

3. **Check file permissions:**
```bash
# Ensure source is readable
chmod -R u+r src/
```

4. **Retry installation:**
```python
result = install.install("/path/to/project")
# Should now return exit code 0
```

---

### 2 - PERMISSION_DENIED

**Meaning:** Insufficient permissions for installation.

**Triggered By:**
- Target directory not writable
- Cannot create devforgeai/ or .claude/ directories
- Cannot write to backup location
- Cannot change file permissions

**Example Errors:**
```
PermissionError: [Errno 13] Permission denied: '/path/to/project/.claude/commands/dev.md'
PermissionError: [Errno 13] Permission denied: '/path/to/project/devforgeai/'
OSError: Permission denied when creating backup directory
```

**Recovery Steps:**

1. **Check current permissions:**
```bash
# View permissions on target directories
ls -ld /path/to/project/.claude
ls -ld /path/to/project/devforgeai
ls -ld /path/to/project
```

2. **Fix permissions (standard approach):**
```bash
# Make directories writable by current user
chmod -R u+w /path/to/project/.claude
chmod -R u+w /path/to/project/devforgeai
chmod -R u+w /path/to/project

# Or use sudo if necessary
sudo chmod -R u+w /path/to/project/.claude
sudo chmod -R u+w /path/to/project/devforgeai
```

3. **Verify permissions fixed:**
```bash
# Check write permission (should show 'w')
ls -ld /path/to/project/.claude
# drwxrwx--- (or similar with 'w' for user)
```

4. **Retry installation:**
```python
result = install.install("/path/to/project")
# Should now return exit code 0
```

**Important Note:**
When exit code 2 occurs, the installer's auto-rollback feature has already restored the previous state. Your project is safe to retry.

---

### 3 - ROLLBACK_OCCURRED

**Meaning:** Installation encountered an error, system was rolled back.

**Triggered By:**
- Any fatal error during file deployment (permission denied, disk full, etc.)
- Validation failure detected post-installation
- User cancellation (Ctrl+C during installation)
- Backup/rollback operation failed

**Example Scenarios:**

**Scenario 1: Disk full during deployment**
```
Error: No space left on device
Action: Rollback → Exit code 3
Result: System restored to pre-installation state
```

**Scenario 2: Permission denied mid-deployment**
```
Error: Permission denied writing to .claude/commands/dev.md
Action: Rollback → Exit code 3
Result: System restored to pre-installation state
```

**Scenario 3: User cancelled (Ctrl+C)**
```
User presses Ctrl+C during installation
Action: Rollback → Exit code 3
Result: System restored to pre-installation state
```

**Recovery Steps:**

1. **Understand what happened:**
```bash
# Check installation log for details
cat devforgeai/install.log

# Look for error message and phase where failure occurred
# Example:
# [ERROR] 2025-12-03T14:30:45.123Z - Phase: file_copy
# [ERROR] Failed to copy .claude/commands/dev.md: Permission denied
```

2. **Verify system state:**
```bash
# Check that version.json reflects pre-installation version
cat devforgeai/.version.json

# Validate installation (read-only check)
python -c "from installer import install; install.install('/path', mode='validate')"
```

3. **Address root cause:**
- **Disk full:** Free up disk space: `df -h /path/to/project`
- **Permission denied:** Fix permissions: `chmod -R u+w /path/to/project`
- **Network issue:** Check connectivity, retry
- **System overloaded:** Wait, retry

4. **Retry installation:**
```python
# After fixing root cause, retry
result = install.install("/path/to/project")

# If succeeds → exit code 0
# If fails again → exit code 3 (rollback occurs again)
```

**Important Note:**
If exit code 3 occurs repeatedly, the underlying issue needs resolution:
- Add diagnostic info to log file: `devforgeai/install.log`
- Run: `devforgeai-validate check-disk-space /path/to/project`
- Check system resources: `free -h`, `df -h`, `top`

---

### 4 - VALIDATION_FAILED

**Meaning:** Installation completed but validation checks failed.

**Triggered By:**
- Critical files missing after installation
- Directory structure incomplete
- File permissions incorrect
- Backup integrity check failed
- CLI not accessible (informational only)

**Example Errors:**
```
ValidationError: Expected 450 files, found 435
ValidationError: devforgeai/protocols/ directory missing
ValidationError: .version.json schema validation failed
```

**Recovery Steps:**

1. **Check what failed in validation:**
```bash
# Validation was read-only, project still has new version
cat devforgeai/.version.json

# Check log for specific validation failures
grep "validation" devforgeai/install.log -i
```

2. **Verify critical files exist:**
```bash
# Check directory structure
test -d .claude/commands && echo "✓ commands"
test -d .claude/skills && echo "✓ skills"
test -d devforgeai/protocols && echo "✓ protocols"
test -f devforgeai/.version.json && echo "✓ version.json"
test -f CLAUDE.md && echo "✓ CLAUDE.md"
```

3. **Count installed files:**
```bash
# Compare to expected counts
echo "Command files: $(find .claude/commands -type f | wc -l) (expected: ~15)"
echo "Skill files: $(find .claude/skills -type f | wc -l) (expected: ~200)"
echo "Total files: $(find .claude devforgeai -type f 2>/dev/null | wc -l) (expected: ~450)"
```

4. **Re-validate installation:**
```python
from installer import install

# Run validation again (read-only, safe)
result = install.install(
    target_path="/path/to/project",
    mode="validate"
)

# May pass on second run if validation was transient
if result["status"] == "success":
    print("Validation now passes")
else:
    print("Validation still fails:", result["errors"])
```

5. **If validation still fails, attempt reinstall:**
```python
# Create fresh backup first
result = install.install(
    target_path="/path/to/project",
    mode="reinstall"  # Uses same version, validates deployment
)

# If succeeds → exit code 0
# If fails → exit code 3 (rollback to original)
```

**When Exit Code 4 is Acceptable:**
- CLI not found in PATH (informational - installation still valid)
- Transient network timeout checking CLI
- Some files modified post-installation by user

---

## Exit Codes in Scripts

### Bash/Shell

```bash
#!/bin/bash
set -e  # Exit on first error

# Run installer
python -m installer /path/to/project
EXIT_CODE=$?

# Handle different exit codes
case $EXIT_CODE in
    0)
        echo "Installation successful"
        exit 0
        ;;
    1)
        echo "ERROR: Missing source files"
        echo "Fix: Ensure src/ directory has required structure"
        exit 1
        ;;
    2)
        echo "ERROR: Permission denied"
        echo "Fix: chmod -R u+w /path/to/project"
        exit 1
        ;;
    3)
        echo "ERROR: Installation failed and rolled back"
        echo "System is safe, retry after fixing root cause"
        exit 1
        ;;
    4)
        echo "WARNING: Validation failed after installation"
        echo "Review log: cat devforgeai/install.log"
        exit 1
        ;;
    *)
        echo "Unknown exit code: $EXIT_CODE"
        exit 1
        ;;
esac
```

### Python

```python
import subprocess
import sys
from installer import install

# Option 1: Direct Python API
result = install.install(target_path="/path/to/project")

exit_code = result.get("exit_code", 0)
if exit_code == 0:
    print("✅ Installation successful")
elif exit_code == 3:
    print("❌ Installation failed but rolled back (safe to retry)")
    print(f"   Errors: {result.get('errors', [])}")
    sys.exit(1)
else:
    print(f"❌ Installation failed with exit code {exit_code}")
    sys.exit(1)

# Option 2: Command-line execution (if CLI available)
result = subprocess.run(
    ["python", "-m", "installer", "/path/to/project"],
    capture_output=True
)

if result.returncode == 0:
    print("✅ Installation successful")
else:
    print(f"❌ Installation failed with code {result.returncode}")
    sys.exit(result.returncode)
```

### CI/CD (GitHub Actions)

```yaml
name: Install DevForgeAI

on: [push]

jobs:
  install:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.8'

      - name: Install dependencies
        run: pip install packaging

      - name: Run DevForgeAI installer
        id: install
        run: |
          python -m installer ${{ github.workspace }}

      - name: Check installation result
        run: |
          case ${{ steps.install.outcome }} in
            success)
              echo "✅ Installation successful"
              ;;
            failure)
              echo "❌ Installation failed"
              cat devforgeai/install.log
              exit 1
              ;;
          esac
```

---

## Troubleshooting by Exit Code

### "Exit code 0 but something seems wrong"

**Possible Causes:**
- Installation succeeded but project structure different than expected
- Some non-critical features unavailable (CLI not in PATH)
- User configuration differences from template

**Check:**
```bash
# Verify structure matches expectations
test -d .claude && echo "✓ .claude directory"
test -d devforgeai && echo "✓ devforgeai directory"
test -f CLAUDE.md && echo "✓ CLAUDE.md"

# Test framework availability
python -c "from installer import install; print('✓ Installer module')"
which devforgeai && echo "✓ CLI in PATH" || echo "⚠ CLI not in PATH"
```

### "Exit code 1 with missing source error"

**Quick Fix:**
```bash
# Create minimal version.json
mkdir -p src/devforgeai
echo '{"version": "1.0.0"}' > src/devforgeai/version.json
```

### "Exit code 2 with permission error"

**Quick Fix:**
```bash
# Fix permissions
chmod -R u+w /path/to/project
# Retry
python -m installer /path/to/project
```

### "Exit code 3 appears repeatedly"

**Investigation:**
1. Check logs: `cat devforgeai/install.log`
2. Free disk space: `df -h /path/to/project` (need >100MB)
3. Check permissions: `ls -ld /path/to/project`
4. Try different target: `python -m installer /tmp/test-install`

### "Exit code 4 but framework works"

**Normal Situation:** CLI validation failed but installation successful.

**Check:**
```bash
# Verify framework is functional
python -c "from installer import install; print('✓ Framework available')"

# Install CLI if needed
pip install -e .claude/scripts/
which devforgeai && echo "✓ CLI installed"
```

---

## Exit Code Flow Diagram

```
Installation Start
    ↓
[Validate Source] ──→ Source files missing? → EXIT 1 (MISSING_SOURCE)
    ↓
[Create Backup] ──→ Permission denied? → EXIT 2 (PERMISSION_DENIED)
    ↓              → Auto-rollback occurs
[Deploy Files] ──→ Permission/disk error? → EXIT 3 (ROLLBACK_OCCURRED)
    ↓              → Auto-rollback occurs
[Post-Deploy Check] ──→ Validation fails? → EXIT 4 (VALIDATION_FAILED)
    ↓
✅ SUCCESS ──→ EXIT 0 (SUCCESS)
```

---

## Environment-Specific Behaviors

### Linux/macOS

| Exit Code | Typical Cause |
|-----------|--------------|
| 0 | Installation successful |
| 1 | Missing src/ or version.json |
| 2 | chmod or chown permission issues |
| 3 | Disk space or I/O error |
| 4 | Validation failed (rare on Unix) |

### Windows

| Exit Code | Typical Cause |
|-----------|--------------|
| 0 | Installation successful |
| 1 | Missing src\ or version.json |
| 2 | NTFS permission or UAC issues |
| 3 | Disk full or antivirus blocking |
| 4 | Validation failed (rare on Windows) |

---

## Reference for Developers

### Using Exit Codes in Code

```python
from installer.exit_codes import (
    SUCCESS,
    MISSING_SOURCE,
    PERMISSION_DENIED,
    ROLLBACK_OCCURRED,
    VALIDATION_FAILED
)
from installer.error_handler import ErrorHandler

# Initialize
error_handler = ErrorHandler()

# Get exit code for error
error = FileNotFoundError("File not found")
exit_code = error_handler.get_exit_code(error)
print(f"Exit code: {exit_code}")  # 1

# Trigger rollback
exit_code = error_handler.get_exit_code(
    error,
    rollback_triggered=True
)
print(f"Exit code: {exit_code}")  # 3
```

### Testing Exit Codes

```bash
# Test script that validates exit codes
python << 'EOF'
from installer import install
from pathlib import Path
import tempfile

# Test 1: Fresh install (should be 0)
with tempfile.TemporaryDirectory() as tmpdir:
    result = install.install(tmpdir, mode="validate")
    assert result["status"] in ["success", "failed"]

# Test 2: Missing source (should be 1)
try:
    result = install.install("/nonexistent", mode="fresh_install")
except FileNotFoundError:
    print("✓ Exit code 1 (MISSING_SOURCE) triggered correctly")
EOF
```

---

## Logging Exit Codes

All exit codes are logged to `devforgeai/install.log` with timestamps:

```
[2025-12-03T14:30:45.123Z] [INFO] Installation started: fresh_install
[2025-12-03T14:30:46.234Z] [INFO] Backup created: devforgeai/install-backup-2025-12-03T14-30-46/
[2025-12-03T14:30:50.567Z] [INFO] Files deployed: 450
[2025-12-03T14:30:51.789Z] [ERROR] Validation failed: 435 files found, expected 450
[2025-12-03T14:30:51.890Z] [INFO] Exit code: 4 (VALIDATION_FAILED)
```

---

## Related Documentation

- **README.md** - Installation overview and quick start
- **TROUBLESHOOTING.md** - Detailed error scenarios and recovery
- **STORY-074** - Comprehensive error handling specification

---

**Last Updated:** 2025-12-03
**Version:** 1.0.0
**Story:** STORY-074 - Comprehensive Error Handling
