# DevForgeAI Fix Command Usage Guide

**Story:** STORY-079 - Fix/Repair Installation Mode
**Version:** 1.0
**Last Updated:** 2025-12-06

---

## Overview

The `devforgeai fix` command validates installation integrity and repairs corrupted or incomplete DevForgeAI installations automatically.

**Use Cases:**
- Installation corrupted after incomplete upgrade
- Files manually deleted or modified by mistake
- Disk errors causing file corruption
- Manifest out of sync with actual files

---

## Command Syntax

```bash
python -m installer fix <target_path> [--force] [--verbose] [--source <source_path>]
```

### Arguments

| Argument | Required | Description |
|----------|----------|-------------|
| `<target_path>` | Yes | Path to DevForgeAI installation root directory |
| `--force` | No | Skip user prompts and repair all files automatically |
| `--verbose` | No | Display detailed issue list and repair operations |
| `--source <path>` | No | Path to source package (for repairs). Auto-detected if omitted |

---

## Usage Examples

### 1. Basic Fix (Interactive Mode)

```bash
python -m installer fix /path/to/project
```

**What happens:**
1. Validates all files against `.devforgeai/.install-manifest.json`
2. Detects issues (missing, corrupted, extra files)
3. Prompts for user-modified files (keep/restore/show diff/backup)
4. Repairs issues automatically
5. Updates manifest with new checksums
6. Saves report to `.devforgeai/logs/fix-{timestamp}.log`

**Example output:**
```
Installation Validation:
  Files checked: 450
  Issues found: 3
  - MISSING: .claude/commands/dev.md
  - CORRUPTED: .devforgeai/context/tech-stack.md (user-modified)
  - EXTRA: custom_script.py (warning only)

User-modified file detected: .devforgeai/context/tech-stack.md
Options:
  1. Keep my version (skip repair)
  2. Restore original (overwrite with source)
  3. Show diff (display differences)
  4. Backup and restore (save my version, restore original)
Choice [1/2/3/4]: 4

Repair Operations:
  ✓ Restored: .claude/commands/dev.md
  ✓ Backed up and restored: .devforgeai/context/tech-stack.md
  ⚠ Skipped: custom_script.py (extra file, warning only)

Repair Summary:
  Files Checked: 450
  Issues Found: 3
  Issues Fixed: 2
  Issues Skipped: 0
  Duration: 2.3s

✓ All issues repaired successfully
Log saved to: .devforgeai/logs/fix-20251206-103045.log
```

---

### 2. Force Mode (Non-Interactive)

```bash
python -m installer fix /path/to/project --force
```

**What happens:**
- Repairs ALL files without prompting
- Overwrites user-modified files with source versions
- Useful for automated recovery or CI/CD

**⚠️ Warning:** User modifications will be lost. Use with caution.

---

### 3. Verbose Mode (Detailed Output)

```bash
python -m installer fix /path/to/project --verbose
```

**What happens:**
- Shows detailed issue list with expected/actual values
- Displays repair operations as they occur
- Helpful for troubleshooting and understanding issues

---

### 4. Custom Source Package

```bash
python -m installer fix /path/to/project --source /path/to/source-package
```

**What happens:**
- Uses specified source directory instead of auto-detection
- Useful when source is in non-standard location

---

## Exit Codes

| Code | Meaning | Next Steps |
|------|---------|------------|
| **0** | Success - all issues fixed or no issues found | Installation is healthy |
| **1** | Missing source - repair files not available | Provide --source path or reinstall |
| **2** | Permission denied - cannot write to installation | Check file permissions, run as appropriate user |
| **3** | Partial repair - some issues fixed, some skipped | Review log file, manually fix skipped issues |
| **4** | Validation failed - post-repair validation failed | Run fix again or reinstall |
| **5** | Manual merge needed - user-modified files need attention | Review user-modified files, choose how to proceed |

---

## Handling Missing Manifest

If `.devforgeai/.install-manifest.json` is missing:

```
Manifest file (.devforgeai/.install-manifest.json) not found.

Options:
  1. Regenerate manifest from current files (treat as source of truth)
  2. Reinstall DevForgeAI (fresh install)
  3. Abort (exit without changes)

Choice [1/2/3]:
```

**Option 1: Regenerate**
- Scans current installation
- Creates new manifest with current checksums
- Useful if files are correct but manifest lost

**Option 2: Reinstall**
- Exit code 1
- User manually runs `python -m installer install`

**Option 3: Abort**
- No changes made
- Exit code 0

---

## User-Modified File Prompts

When a user-modified file is detected:

```
User-modified file detected: .devforgeai/context/tech-stack.md

Options:
  1. Keep my version (skip repair)
  2. Restore original (overwrite with source)
  3. Show diff (display differences)
  4. Backup and restore (save my version, restore original)

Choice [1/2/3/4]:
```

**Option 1: Keep**
- Preserves your modifications
- Issue remains (exit code may be 3 or 5)

**Option 2: Restore**
- Overwrites with source version
- Your changes are lost
- Issue is fixed

**Option 3: Show diff**
- Displays unified diff
- Re-prompts for action after viewing
- Helps you decide

**Option 4: Backup and restore**
- Saves your version to `.backups/install-backup-{timestamp}/`
- Restores original from source
- Best of both worlds

---

## Performance

**Validation Speed:**
- Standard installation (450 files): ~1-3 seconds
- Large installation (1000 files): ~5-10 seconds
- Performance target: <30 seconds for any installation

**Checksum Calculation:**
- Efficient chunked reading (8KB chunks)
- 100MB file: ~2-5 seconds
- Memory-efficient for large files

---

## Security

**Scope Limitation:**
- Only repairs files in `.claude/`, `.devforgeai/`, and `CLAUDE.md`
- User files outside DevForgeAI directories are never modified
- Directory traversal attempts are blocked

**User File Protection:**
- User-modified files detected automatically
- Non-destructive by default (requires confirmation)
- Backup option available before overwrite

---

## Logging

**Repair logs saved to:**
```
.devforgeai/logs/fix-{timestamp}.log
```

**Log includes:**
- Timestamp and duration
- Files checked count
- Issues found/fixed/skipped/remaining
- Detailed messages, warnings, errors
- Exit code

**Example log:**
```
Fix Report - 2025-12-06T10:30:45Z
============================================================
Status: partial
Files Checked: 450
Issues Found: 3
Issues Fixed: 2
Issues Skipped: 1
Issues Remaining: 0
Duration: 2.34s
Exit Code: 3

Messages:
  - Fixed 2 issues. 1 user-modified file requires manual attention.
  - Log saved to: .devforgeai/logs/fix-20251206-103045.log

Warnings:
  - EXTRA: custom_script.py
```

---

## Troubleshooting

See `FIX-COMMAND-TROUBLESHOOTING.md` for common issues and solutions.

---

## See Also

- **STORY-079:** Complete technical specification
- **Troubleshooting Guide:** `installer/docs/FIX-COMMAND-TROUBLESHOOTING.md`
- **Installation Guide:** `installer/docs/INSTALL.md`
- **API Documentation:** `installer/docs/API.md`
