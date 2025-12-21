# DevForgeAI Version-Aware Installer

**Version:** 1.0.0
**Status:** Production Ready
**Story:** STORY-045

---

## Overview

The DevForgeAI installer is a version-aware installation framework that provides safe, atomic installation, upgrade, and rollback operations for the DevForgeAI framework.

**Key Features:**
- ✅ Semantic version detection and comparison
- ✅ Automatic backup before any modifications
- ✅ Selective file updates for patch/minor upgrades (10x faster)
- ✅ User configuration preservation during upgrades
- ✅ Atomic transactions with auto-rollback on failure
- ✅ 5 installation modes (fresh, upgrade, rollback, validate, uninstall)
- ✅ SHA256 integrity verification for backups
- ✅ Cross-platform compatibility (Windows/Linux/macOS)

---

## Installation

```bash
# No installation needed - installer is self-contained
# Just ensure Python 3.8+ and dependencies available:

pip install packaging
```

---

## Quick Start

### Fresh Installation

Install DevForgeAI framework to a new project:

```python
from installer import install

result = install.install(
    target_path="/path/to/my/project",
    mode="fresh_install"
)

if result["status"] == "success":
    print(f"✅ Installed version {result['version']}")
    print(f"   Files deployed: {result['files_deployed']}")
else:
    print(f"❌ Installation failed: {result['errors']}")
```

**Expected:**
- Deploys ~450 framework files to `.claude/` and `devforgeai/`
- Creates `devforgeai/.version.json` with installation metadata
- Sets file permissions (755 for scripts, 644 for docs)
- Completes in <3 minutes

---

### Upgrade Existing Installation

Upgrade from v1.0.0 to v1.0.1:

```python
from installer import install

result = install.install(
    target_path="/path/to/existing/project",
    mode="upgrade"  # or auto-detect with mode=None
)

if result["status"] == "success":
    print(f"✅ Upgraded to version {result['version']}")
    print(f"   Backup: {result['backup_path']}")
    print(f"   Files updated: {result['files_deployed']}")
```

**Expected:**
- Detects current version (1.0.0) and source version (1.0.1)
- Creates automatic backup: `.backups/devforgeai-upgrade-YYYYMMDD-HHMMSS/`
- Selectively updates only changed files (patch/minor upgrades)
- Preserves user configs (hooks.yaml, context/*.md, feedback config)
- Updates `devforgeai/.version.json` to 1.0.1
- Completes in <30 seconds (selective update)

---

### Rollback to Previous Version

Restore from backup after upgrade:

```python
from installer import install

result = install.install(
    target_path="/path/to/project",
    mode="rollback"
)

if result["status"] == "success":
    print(f"✅ Rolled back to backup")
    print(f"   Backup used: {result['backup_path']}")
    print(f"   Files restored: {result['files_restored']}")
```

**Expected:**
- Lists available backups (sorted by timestamp, newest first)
- Uses most recent backup automatically
- Verifies backup integrity (SHA256 checksums)
- Restores all files from backup
- Reverts `.version.json` to backup version
- Completes in <45 seconds

---

### Validate Installation

Check installation health without modifications:

```python
from installer import install

result = install.install(
    target_path="/path/to/project",
    mode="validate"
)

if result["status"] == "success":
    print(f"✅ Installation valid")
    print(f"   Version: {result['version']}")
else:
    print(f"❌ Validation failed: {result['errors']}")
```

**Expected:**
- Validates directory structure (.claude/skills/, devforgeai/protocols/, etc.)
- Validates `.version.json` schema and consistency
- Checks CLI installed and accessible
- Verifies critical files exist (11+ commands, 10+ skills, 3+ protocols)
- Read-only (no modifications)
- Completes in <5 seconds

---

### Uninstall Framework

Remove DevForgeAI framework (preserves user data):

```python
from installer import install

result = install.install(
    target_path="/path/to/project",
    mode="uninstall"
)

if result["status"] == "success":
    print(f"✅ Framework uninstalled")
    print(f"   Backup: {result['backup_path']}")
    print(f"   User data preserved: devforgeai/specs/, context/")
```

**Expected:**
- Creates backup before removal
- Removes `.claude/` directory
- Removes `devforgeai/` subdirectories (preserves context/, config/)
- Removes CLAUDE.md DevForgeAI sections
- Preserves user data (`devforgeai/specs/`, context files)
- Removes `.version.json`
- Project can be re-installed later

---

## Installation Modes

### Auto-Detection

If `mode=None`, installer auto-detects based on target state:

```python
# Installer detects mode automatically
result = install.install(target_path="/path/to/project")

# Detection logic:
if no .version.json:
    mode = "fresh_install"
elif same_version:
    mode = "reinstall"
elif source > installed (patch):
    mode = "patch_upgrade"
elif source > installed (minor):
    mode = "minor_upgrade"
elif source > installed (major):
    mode = "major_upgrade"
elif source < installed:
    mode = "downgrade" (requires --force flag)
```

### Version Comparison

Installer uses **semantic versioning** (major.minor.patch):

| From | To | Mode | Breaking Changes? |
|------|-------|------|-------------------|
| None | 1.0.0 | fresh_install | N/A |
| 1.0.0 | 1.0.1 | patch_upgrade | No (bug fixes only) |
| 1.0.0 | 1.1.0 | minor_upgrade | No (backward compatible) |
| 1.0.0 | 2.0.0 | major_upgrade | Yes (requires user confirmation) |
| 1.0.0 | 1.0.0 | reinstall | No (repair installation) |
| 1.0.1 | 1.0.0 | downgrade | Maybe (requires --force flag) |

---

## Backup Management

### Backup Creation

Backups are automatically created before:
- Upgrade operations (all types)
- Downgrade operations
- Uninstall operations
- NOT created for: fresh_install, validate, rollback

**Backup location:** `.backups/devforgeai-upgrade-YYYYMMDD-HHMMSS/`

**Backup structure:**
```
.backups/devforgeai-upgrade-20251119-143000/
├── .claude/           # Complete copy
├── devforgeai/       # Complete copy
├── CLAUDE.md          # If exists
└── manifest.json      # Backup metadata
```

**manifest.json contents:**
```json
{
  "created_at": "2025-11-19T14:30:00Z",
  "reason": "upgrade",
  "from_version": "1.0.0",
  "to_version": "1.0.1",
  "files_backed_up": 450,
  "total_size_mb": 15.2,
  "backup_integrity_hash": "sha256:abc123..."
}
```

### Backup Integrity

All backups include SHA256 integrity hash:
- Calculated during backup creation
- Verified before rollback operations
- Must match 100% (strict validation)
- Detects corrupted backups

### Backup Cleanup

Backups accumulate over time. Clean manually when needed:

```bash
# List backups
ls -lh .backups/

# Remove old backups (keep last 5)
cd .backups
ls -t | tail -n +6 | xargs rm -rf
```

---

## User Configuration Preservation

### Protected Files

These files are **NEVER overwritten** during upgrades:

**User Configurations:**
- `devforgeai/config/hooks.yaml`
- `devforgeai/feedback/config.yaml`

**User Context:**
- `devforgeai/specs/context/*.md` (tech-stack, source-tree, dependencies, etc.)

**User Documentation:**
- `devforgeai/specs/` directory (stories, epics, sprints)

### New Configuration Templates

If framework adds new config options, installer provides templates:

**Example:**
```
Upgrade 1.0.0 → 1.1.0 adds new feature with config

Installer behavior:
✅ Preserves: devforgeai/config/hooks.yaml (user customizations)
ℹ️  Creates: devforgeai/config/hooks.yaml.example (new template)
📝 Message: "New config template available: hooks.yaml.example (review for new features)"
```

---

## Error Handling & Recovery

### Atomic Transactions

All operations are atomic:
- **Backup created BEFORE any modifications**
- If deployment fails → **auto-rollback** to previous state
- No partial installations (all-or-nothing)

### Auto-Rollback Scenarios

Installer automatically rolls back on:
- Permission denied during deployment
- Disk full during file copy
- Corruption detected during deployment
- Any OSError during modification phase

**Example:**
```python
result = install.install(target, mode="upgrade")

if result["status"] == "rollback":
    print(f"⚠️ Upgrade failed, auto-rolled back")
    print(f"   Error: {result['errors'][0]}")
    print(f"   Files restored: {result['files_restored']}")
    print(f"   Project state: Valid (previous version)")
```

### Manual Recovery

If installation fails and auto-rollback doesn't trigger:

```python
# List available backups
from installer import rollback

backups = rollback.list_backups(project_root)
for backup in backups:
    print(f"{backup['name']}: {backup['from_version']} → {backup['to_version']}")

# Restore manually
result = install.install(target, mode="rollback")
```

---

## API Reference

### install.install()

```python
def install(
    target_path: str | Path,
    source_path: str | Path = None,
    mode: str = None,
    force: bool = False,
) -> dict
```

**Parameters:**
- `target_path` (str | Path): Root directory of target project
- `source_path` (str | Path, optional): Root directory of source framework (default: `./src`)
- `mode` (str, optional): Installation mode (default: auto-detect)
  - `"fresh_install"`: Install to empty project
  - `"patch_upgrade"`: Upgrade within same minor version (1.0.0 → 1.0.1)
  - `"minor_upgrade"`: Upgrade to new minor version (1.0.0 → 1.1.0)
  - `"major_upgrade"`: Upgrade to new major version (1.0.0 → 2.0.0)
  - `"reinstall"`: Reinstall same version (repair)
  - `"downgrade"`: Install older version (requires force=True)
  - `"rollback"`: Restore from backup
  - `"validate"`: Check installation health
  - `"uninstall"`: Remove framework
- `force` (bool, optional): Force installation even if checks fail (default: False)

**Returns:**
```python
{
    "status": "success" | "failed" | "rollback",
    "mode": str,  # Mode used
    "version": str,  # Version installed/verified
    "backup_path": str | None,  # Backup created (if applicable)
    "files_deployed": int,  # Files deployed (if applicable)
    "files_restored": int,  # Files restored (if rollback)
    "errors": list[str],  # Error messages
    "warnings": list[str],  # Warning messages
    "messages": list[str],  # Info messages
}
```

---

## Performance Characteristics

| Operation | Time | Files | Mode |
|-----------|------|-------|------|
| Fresh Install | <180s | ~450 | Deploy all |
| Patch Upgrade | <30s | ~10 | Selective update |
| Minor Upgrade | <60s | ~50 | Selective update |
| Major Upgrade | <180s | ~450 | Full deployment |
| Backup Creation | <20s | ~450 | Copy + hash |
| Rollback | <45s | ~450 | Restore + verify |
| Validation | <5s | 0 | Read-only checks |

---

## Exit Codes

The installer returns standardized exit codes to indicate success or failure:

| Code | Status | Meaning | Recovery |
|------|--------|---------|----------|
| 0 | SUCCESS | Installation completed without errors | Continue |
| 1 | MISSING_SOURCE | Required source files not found | Create src/devforgeai/version.json |
| 2 | PERMISSION_DENIED | Insufficient permissions for target directory | `chmod -R u+w /path` |
| 3 | ROLLBACK_OCCURRED | Installation failed, system automatically rolled back | Fix root cause and retry |
| 4 | VALIDATION_FAILED | Installation completed but validation checks failed | Review log file |

**See:** [EXIT-CODES.md](EXIT-CODES.md) for detailed documentation of each exit code, recovery procedures, and usage examples.

---

## Testing

### Run Unit Tests

```bash
# All unit tests (76 tests)
pytest installer/tests/ -v

# Specific module
pytest installer/tests/test_version_detection.py -v
pytest installer/tests/test_backup_management.py -v
pytest installer/tests/test_deployment_engine.py -v
```

### Run Integration Tests

```bash
# All integration tests (44 tests)
pytest installer/tests/integration/ -v

# Specific workflow
pytest installer/tests/integration/test_fresh_install_workflow.py -v
pytest installer/tests/integration/test_upgrade_workflow.py -v
pytest installer/tests/integration/test_performance_benchmarks.py -v
```

### Generate Coverage Report

```bash
pytest installer/tests/ --cov=installer --cov-report=html
open htmlcov/index.html
```

**Target Coverage:**
- Business Logic: 95%+
- Application Layer: 85%+
- Overall: 80%+

---

## Troubleshooting

### Issue: "Source version not found"

**Cause:** Missing `src/devforgeai/version.json`

**Solution:**
```bash
# Create version.json in source
cat > src/devforgeai/version.json <<'EOF'
{
  "version": "1.0.0",
  "released_at": "2025-11-19T00:00:00Z",
  "schema_version": "1.0"
}
EOF
```

---

### Issue: "Backup path already exists"

**Cause:** Concurrent installation or timestamp collision

**Solution:**
```bash
# Wait 1 second and retry (timestamp resolution)
# Or clean up existing backup if safe:
rm -rf .backups/devforgeai-upgrade-YYYYMMDD-HHMMSS/
```

---

### Issue: "Permission denied" during deployment

**Cause:** Target directory not writable

**Solution:**
```bash
# Fix permissions
chmod -R u+w /path/to/project/.claude
chmod -R u+w /path/to/project/devforgeai

# Then retry installation
```

**Note:** Installer auto-rolls back on permission errors, project remains in valid state.

---

### Issue: Integration tests failing with "source_framework fixture not found"

**Cause:** Test needs real src/ directory structure

**Solution:**
```bash
# Ensure src/ directory exists with required structure:
mkdir -p src/claude src/devforgeai
echo '{"version": "1.0.0"}' > src/devforgeai/version.json

# Create minimal framework files for testing
touch src/claude/.gitkeep
touch src/devforgeai/.gitkeep
```

---

### Issue: "Rollback verification failed - checksums don't match"

**Cause:** Files modified after backup creation

**Solution:**
This is **expected** if files changed between backup and rollback. The installer is working correctly by detecting the mismatch.

To force rollback despite mismatch (use with caution):
```python
# Not implemented - by design
# Strict verification prevents data loss
```

---

## Architecture

### Module Overview

```
installer/
├── install.py       # Main orchestrator (5 modes)
├── version.py       # Version detection & comparison
├── backup.py        # Backup creation & integrity
├── deploy.py        # File deployment & permissions
├── rollback.py      # Backup restoration & verification
└── validate.py      # Installation validation & health checks
```

### Dependencies

**External:**
- `packaging` library (semantic versioning)

**Standard Library:**
- pathlib, shutil, json, datetime, subprocess, hashlib, stat, typing

**No other dependencies** - minimal footprint, maximum portability.

---

## Security

**Security measures implemented:**

1. **Path Traversal Protection**
   - All backup paths validated within `.backups/` directory
   - Symlinks rejected during backup restoration
   - copytree with `symlinks=False` prevents symlink following

2. **Atomic Operations**
   - Backup created before modifications
   - Auto-rollback on any error
   - No partial installations

3. **Permission Management**
   - Scripts: 755 (executable)
   - Docs/Data: 644 (read/write user, read-only others)
   - Directories: 755

4. **Integrity Verification**
   - SHA256 checksums for all backups
   - 100% hash match required for rollback validation
   - Manifest validation before restoration

5. **User Permission Only**
   - No sudo/root required
   - Runs with standard user permissions
   - Safe for multi-user environments

---

## FAQ

**Q: Can I run installer on Windows?**
A: Yes! Installer uses pathlib (cross-platform) and detects Windows vs Unix for CLI checks.

**Q: What happens if upgrade fails mid-deployment?**
A: Installer auto-rolls back to previous state using backup. Project remains functional.

**Q: Are my story files preserved during upgrade?**
A: Yes! `devforgeai/specs/` directory is never touched. Context files are also preserved.

**Q: How do I downgrade to an older version?**
A: Use `mode="downgrade"` with `force=True`. Note: May break compatibility.

**Q: Can I customize what files are deployed?**
A: Exclusion patterns are in `deploy.py`. Modify EXCLUDE_PATTERNS constant.

**Q: How many backups should I keep?**
A: Keep last 3-5 backups. Older backups can be removed manually.

---

## Contributing

See `STORY-045-version-aware-installer-core.story.md` for:
- Acceptance criteria
- Technical specification
- Edge cases
- Definition of done

**Test requirements:**
- All unit tests must pass (76 tests)
- All integration tests must pass (44 tests)
- Performance benchmarks within NFR thresholds
- Security review passed

---

## License

MIT License - See LICENSE file

---

## Documentation

**Comprehensive error handling documentation added in STORY-074:**

- **[EXIT-CODES.md](EXIT-CODES.md)** - Detailed reference for all 5 exit codes (0-4) with recovery procedures
- **[ERROR-HANDLING-API.md](ERROR-HANDLING-API.md)** - Complete API documentation for error handling services
- **[TROUBLESHOOTING.md](TROUBLESHOOTING.md)** - Common issues, error handling overview, and advanced diagnostics

---

## Support

For issues, see:
- **Exit codes:** [EXIT-CODES.md](EXIT-CODES.md) (quick reference)
- **Troubleshooting:** [TROUBLESHOOTING.md](TROUBLESHOOTING.md) (detailed guide)
- **API Reference:** [ERROR-HANDLING-API.md](ERROR-HANDLING-API.md) (for developers)
- **Test files:** `installer/tests/` (examples of all operations)
- **Integration tests:** `installer/tests/integration/` (end-to-end workflows)
- **Story files:**
  - `devforgeai/specs/Stories/STORY-045-version-aware-installer-core.story.md` (installer core)
  - `devforgeai/specs/Stories/STORY-074-comprehensive-error-handling.story.md` (error handling)

---

**Last Updated:** 2025-12-03
**Version:** 1.0.1 (STORY-074 - Error Handling Added)
**Stories:** STORY-045 (Installer Core) + STORY-074 (Error Handling)
