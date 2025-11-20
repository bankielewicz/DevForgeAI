# DevForgeAI Installer API Documentation

**Version:** 1.0.0
**Story:** STORY-045

Complete API reference for all installer modules and functions.

---

## Module: install.py

Main orchestrator for all installation operations.

### install.install()

```python
def install(
    target_path: str | Path,
    source_path: str | Path = None,
    mode: str = None,
    force: bool = False,
) -> dict
```

**Purpose:** Execute installation in specified mode with atomic transaction semantics.

**Parameters:**
- `target_path` (str | Path): Root directory of target project (required)
- `source_path` (str | Path, optional): Root directory of source framework files (default: `./src`)
- `mode` (str, optional): Installation mode (default: auto-detect from target state)
  - Options: `"fresh_install"`, `"patch_upgrade"`, `"minor_upgrade"`, `"major_upgrade"`, `"reinstall"`, `"downgrade"`, `"rollback"`, `"validate"`, `"uninstall"`
- `force` (bool, optional): Force installation even if checks fail (default: False)

**Returns:** `dict` with installation result

**Return Schema:**
```python
{
    "status": "success" | "failed" | "rollback",  # Overall result
    "mode": str,                                  # Mode used
    "version": str,                               # Version installed/verified
    "backup_path": str | None,                    # Backup created (if applicable)
    "files_deployed": int,                        # Files deployed (fresh/upgrade)
    "files_restored": int,                        # Files restored (rollback)
    "errors": list[str],                          # Error messages
    "warnings": list[str],                        # Warning messages
    "messages": list[str],                        # Info messages
}
```

**Raises:**
- `FileNotFoundError`: If source version.json missing
- `ValueError`: If mode is invalid
- `OSError`: If file operations fail (caught and returned in errors)

**Example Usage:**
```python
from installer import install

# Fresh install with auto-detection
result = install.install("/path/to/project")

# Explicit upgrade
result = install.install(
    target_path="/path/to/project",
    source_path="/custom/src",
    mode="upgrade"
)

# Forced downgrade
result = install.install(
    target_path="/path/to/project",
    mode="downgrade",
    force=True
)
```

---

## Module: version.py

Version detection and semantic version comparison.

### version.get_installed_version()

```python
def get_installed_version(devforgeai_path: Path) -> dict | None
```

**Purpose:** Read installed version from target project.

**Parameters:**
- `devforgeai_path` (Path): Path to `.devforgeai/` directory

**Returns:**
- `dict` with version data if `.version.json` exists
- `None` if no installation found

**Return Schema:**
```python
{
    "version": "1.0.0",
    "installed_at": "2025-11-19T14:30:00Z",
    "mode": "fresh_install",
    "schema_version": "1.0"
}
```

**Example:**
```python
from pathlib import Path
from installer import version

devforgeai_path = Path("/path/to/project/.devforgeai")
installed = version.get_installed_version(devforgeai_path)

if installed:
    print(f"Installed version: {installed['version']}")
else:
    print("No installation found")
```

---

### version.get_source_version()

```python
def get_source_version(source_devforgeai_path: Path) -> dict
```

**Purpose:** Read source version from framework source directory.

**Parameters:**
- `source_devforgeai_path` (Path): Path to `src/devforgeai/` directory

**Returns:** `dict` with source version data

**Return Schema:**
```python
{
    "version": "1.0.1",
    "released_at": "2025-11-19T00:00:00Z",
    "schema_version": "1.0",
    "description": "...",
    "homepage": "...",
    "license": "MIT"
}
```

**Raises:**
- `FileNotFoundError`: If `version.json` not found in source
- `json.JSONDecodeError`: If version.json is malformed
- `ValueError`: If required fields missing

**Example:**
```python
from pathlib import Path
from installer import version

source_path = Path("./src/devforgeai")
source = version.get_source_version(source_path)

print(f"Source version: {source['version']}")
print(f"Released: {source['released_at']}")
```

---

### version.compare_versions()

```python
def compare_versions(installed: str | None, source: str) -> str
```

**Purpose:** Compare semantic versions and determine installation mode.

**Parameters:**
- `installed` (str | None): Installed version string (e.g., "1.0.0"), or None for fresh install
- `source` (str): Source version string (e.g., "1.0.1")

**Returns:** `str` - Installation mode

**Modes Returned:**
- `"fresh_install"`: No installed version (installed=None)
- `"patch_upgrade"`: 1.0.0 → 1.0.1 (bug fixes, backward compatible)
- `"minor_upgrade"`: 1.0.0 → 1.1.0 (new features, backward compatible)
- `"major_upgrade"`: 1.0.0 → 2.0.0 (breaking changes, may require migration)
- `"reinstall"`: 1.0.0 → 1.0.0 (same version, repair installation)
- `"downgrade"`: 1.0.1 → 1.0.0 (source older than installed, requires --force)

**Raises:**
- `ValueError`: If version format invalid, type incorrect, or empty string

**Example:**
```python
from installer import version

mode = version.compare_versions("1.0.0", "1.0.1")
assert mode == "patch_upgrade"

mode = version.compare_versions("1.0.0", "1.1.0")
assert mode == "minor_upgrade"

mode = version.compare_versions(None, "1.0.0")
assert mode == "fresh_install"
```

---

## Module: backup.py

Backup creation and integrity management.

### backup.create_backup()

```python
def create_backup(
    project_root: Path,
    reason: str,
    from_version: str | None = None,
    to_version: str | None = None,
) -> tuple[Path, dict]
```

**Purpose:** Create timestamped backup of framework directories before modifications.

**Parameters:**
- `project_root` (Path): Root directory of project
- `reason` (str): Backup reason ("upgrade", "uninstall", "manual")
- `from_version` (str | None, optional): Current installed version
- `to_version` (str | None, optional): Target version

**Returns:** `tuple[Path, dict]`
- `Path`: Backup directory path
- `dict`: Backup manifest

**Manifest Schema:**
```python
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

**Raises:**
- `OSError`: If backup directory can't be created (race condition, disk full)
- `IOError`: If files can't be copied

**Example:**
```python
from pathlib import Path
from installer import backup

backup_path, manifest = backup.create_backup(
    project_root=Path("/path/to/project"),
    reason="upgrade",
    from_version="1.0.0",
    to_version="1.0.1"
)

print(f"Backup created: {backup_path}")
print(f"Files backed up: {manifest['files_backed_up']}")
print(f"Integrity hash: {manifest['backup_integrity_hash']}")
```

---

### backup.verify_backup_integrity()

```python
def verify_backup_integrity(backup_path: Path) -> dict
```

**Purpose:** Verify backup integrity using manifest and checksums.

**Parameters:**
- `backup_path` (Path): Path to backup directory

**Returns:** `dict` with verification result

**Return Schema:**
```python
{
    "valid": bool,                    # True if backup is valid
    "file_count_match": bool,         # Backup file count matches manifest
    "hash_match": bool,               # Hash matches manifest
    "errors": list[str],              # Validation errors
    "expected_files": int,            # From manifest
    "actual_files": int,              # Found in backup
    "manifest": dict                  # Manifest contents
}
```

**Example:**
```python
from pathlib import Path
from installer import backup

backup_path = Path("/path/to/project/.backups/devforgeai-upgrade-20251119-143000")
verification = backup.verify_backup_integrity(backup_path)

if verification["valid"]:
    print("✅ Backup integrity verified")
else:
    print(f"❌ Backup corrupted: {verification['errors']}")
```

---

## Module: deploy.py

Framework file deployment and permission management.

### deploy.deploy_framework_files()

```python
def deploy_framework_files(
    source_root: Path,
    target_root: Path,
    preserve_configs: bool = True,
) -> dict
```

**Purpose:** Deploy framework files from source to target with exclusions and preservation rules.

**Parameters:**
- `source_root` (Path): Source framework root (contains `claude/` and `devforgeai/`)
- `target_root` (Path): Target project root
- `preserve_configs` (bool, optional): Preserve user configs during deployment (default: True)

**Returns:** `dict` with deployment report

**Return Schema:**
```python
{
    "status": "success" | "failed",
    "files_deployed": int,        # Files copied
    "files_skipped": int,         # Files excluded
    "directories_created": int,   # Directories created
    "errors": list[str]           # Error messages
}
```

**Deployment Rules:**
- Deploys: `src/claude/` → `.claude/`, `src/devforgeai/` → `.devforgeai/`
- Excludes: `*.backup*`, `__pycache__/`, `*.pyc`, `qa/reports/`, `RCA/`, `adrs/`, `feedback/imported/`, `logs/`
- Preserves (if preserve_configs=True): `hooks.yaml`, `feedback/config.yaml`, `context/*.md`
- Never touches: `.ai_docs/` directory

**Example:**
```python
from pathlib import Path
from installer import deploy

result = deploy.deploy_framework_files(
    source_root=Path("./src"),
    target_root=Path("/path/to/project"),
    preserve_configs=True
)

print(f"Deployed: {result['files_deployed']} files")
print(f"Skipped: {result['files_skipped']} files")
```

---

### deploy.set_file_permissions()

```python
def set_file_permissions(target_root: Path) -> dict
```

**Purpose:** Set appropriate file permissions after deployment.

**Parameters:**
- `target_root` (Path): Target project root

**Returns:** `dict` with permission setting report

**Return Schema:**
```python
{
    "status": "success" | "failed",
    "permissions_set": int,       # Files/dirs updated
    "errors": list[str]           # Error messages
}
```

**Permission Rules:**
- Directories: 755 (rwxr-xr-x)
- Executable files (.sh, devforgeai, claude-code): 755
- Data files (.md, .py, .json, .yaml): 644 (rw-r--r--)

**Example:**
```python
from pathlib import Path
from installer import deploy

result = deploy.set_file_permissions(Path("/path/to/project"))

if result["status"] == "success":
    print(f"Set permissions on {result['permissions_set']} files")
```

---

## Module: rollback.py

Backup restoration and verification.

### rollback.list_backups()

```python
def list_backups(project_root: Path) -> list[dict]
```

**Purpose:** List available backups sorted by timestamp (newest first).

**Parameters:**
- `project_root` (Path): Root directory of project

**Returns:** `list[dict]` - Backup metadata

**Return Schema (per backup):**
```python
{
    "name": "devforgeai-upgrade-20251119-143000",
    "path": Path("/path/.backups/devforgeai-upgrade-20251119-143000"),
    "created_at": "2025-11-19T14:30:00Z",
    "from_version": "1.0.0",
    "to_version": "1.0.1",
    "files_backed_up": 450,
    "size_mb": 15.2
}
```

**Example:**
```python
from pathlib import Path
from installer import rollback

backups = rollback.list_backups(Path("/path/to/project"))

for backup in backups:
    print(f"{backup['name']}: {backup['from_version']} → {backup['to_version']}")
```

---

### rollback.restore_from_backup()

```python
def restore_from_backup(project_root: Path, backup_path: Path) -> dict
```

**Purpose:** Restore all files from backup to project root.

**Parameters:**
- `project_root` (Path): Root directory of project
- `backup_path` (Path): Path to backup directory

**Returns:** `dict` with restoration report

**Return Schema:**
```python
{
    "status": "success" | "failed",
    "files_restored": int,
    "version_reverted": bool,
    "errors": list[str]
}
```

**Security Validations:**
- Backup path must be within `.backups/` directory
- Symlinks in backup are rejected
- copytree with `symlinks=False` prevents symlink following

**Raises:**
- `FileNotFoundError`: If backup doesn't exist
- `ValueError`: If backup path outside .backups/ (security violation)
- `OSError`: If files can't be restored

**Example:**
```python
from pathlib import Path
from installer import rollback

backup_path = Path("/path/.backups/devforgeai-upgrade-20251119-143000")
result = rollback.restore_from_backup(Path("/path/to/project"), backup_path)

if result["status"] == "success":
    print(f"✅ Restored {result['files_restored']} files")
    if result["version_reverted"]:
        print("✅ Version.json reverted")
```

---

### rollback.verify_rollback()

```python
def verify_rollback(project_root: Path, backup_path: Path) -> dict
```

**Purpose:** Verify restored files match backup (checksum validation).

**Parameters:**
- `project_root` (Path): Root directory of project
- `backup_path` (Path): Path to backup directory

**Returns:** `dict` with verification result

**Return Schema:**
```python
{
    "valid": bool,                      # True if 100% checksum match
    "checksums_match": bool,            # All hashes match
    "file_count_match": bool,           # File counts match
    "backup_files": int,                # Expected file count
    "restored_files": int,              # Actual file count
    "errors": list[str]                 # Validation errors
}
```

**Validation:**
- Requires 100% hash match (strict validation, no tolerance)
- Counts all files in .claude/, .devforgeai/, CLAUDE.md
- Compares SHA256 checksums

**Example:**
```python
from pathlib import Path
from installer import rollback

backup_path = Path("/path/.backups/devforgeai-upgrade-20251119-143000")
verification = rollback.verify_rollback(Path("/path/to/project"), backup_path)

if verification["valid"]:
    print(f"✅ Rollback verified: {verification['restored_files']} files match")
else:
    print(f"❌ Verification failed: {verification['errors']}")
```

---

## Module: validate.py

Installation validation and health checks.

### validate.validate_installation()

```python
def validate_installation(project_root: Path) -> dict
```

**Purpose:** Comprehensive validation of installation health (read-only).

**Parameters:**
- `project_root` (Path): Root directory of project

**Returns:** `dict` with validation report

**Return Schema:**
```python
{
    "valid": bool,                      # Overall health
    "version": str,                     # Installed version
    "structure_valid": bool,            # Directory structure OK
    "version_json_valid": bool,         # .version.json OK
    "cli_installed": bool,              # CLI accessible
    "critical_files_present": bool,     # All critical files exist
    "errors": list[str],                # Validation errors
    "warnings": list[str],              # Warning messages
    "checks": {
        "directories": list[str],       # Missing directories
        "critical_files": list[str],    # Missing critical files
        "cli_path": str | None          # CLI location
    }
}
```

**Checks Performed:**
1. Directory structure (.claude/skills/, .claude/agents/, .devforgeai/protocols/)
2. .version.json schema validation
3. CLI installed and accessible (platform-aware: which/where)
4. Critical files present (11+ commands, 10+ skills, 3+ protocols, CLAUDE.md)

**Example:**
```python
from pathlib import Path
from installer import validate

validation = validate.validate_installation(Path("/path/to/project"))

if validation["valid"]:
    print(f"✅ Installation healthy: v{validation['version']}")
else:
    print(f"❌ Issues found: {validation['errors']}")
```

---

### validate.validate_version_json()

```python
def validate_version_json(version_file: Path) -> dict
```

**Purpose:** Validate .version.json schema and consistency.

**Parameters:**
- `version_file` (Path): Path to `.version.json` file

**Returns:** `dict` with validation result

**Return Schema:**
```python
{
    "valid": bool,
    "version": str | None,
    "schema_valid": bool,
    "required_fields_present": bool,
    "errors": list[str]
}
```

**Required Fields:**
- `version`: str (semantic version like "1.0.0")
- `installed_at`: str (ISO 8601 timestamp)
- `mode`: str (installation mode used)
- `schema_version`: str (optional, defaults to "1.0")

**Example:**
```python
from pathlib import Path
from installer import validate

version_file = Path("/path/.devforgeai/.version.json")
validation = validate.validate_version_json(version_file)

if validation["valid"]:
    print(f"✅ Version.json valid: v{validation['version']}")
```

---

## Constants Reference

### Installation Modes (version.py)

```python
MODE_FRESH_INSTALL = "fresh_install"
MODE_PATCH_UPGRADE = "patch_upgrade"
MODE_MINOR_UPGRADE = "minor_upgrade"
MODE_MAJOR_UPGRADE = "major_upgrade"
MODE_REINSTALL = "reinstall"
MODE_DOWNGRADE = "downgrade"
```

### Backup Constants (backup.py)

```python
HASH_ALGORITHM = "sha256"           # Integrity hash algorithm
CHUNK_SIZE = 65536                  # File reading chunk size (64KB)
BACKUP_SUBDIRS = [".claude", ".devforgeai", "CLAUDE.md"]
```

### Deployment Constants (deploy.py)

```python
EXCLUDE_PATTERNS = [
    "*.backup", "*.tmp", "__pycache__", "*.pyc"
]

NO_DEPLOY_DIRS = [
    "qa/reports", "RCA", "adrs", "feedback/imported", "logs"
]

PRESERVE_PATHS = [
    "config/hooks.yaml",
    "feedback/config.yaml",
    "context"  # All context/*.md files
]

PERMISSIONS_DIR = 0o755             # rwxr-xr-x
PERMISSIONS_FILE = 0o644            # rw-r--r--
PERMISSIONS_EXECUTABLE = 0o755      # rwxr-xr-x
```

### Validation Constants (validate.py)

```python
MIN_COMMANDS = 11                   # Minimum command count
MIN_SKILLS = 10                     # Minimum skill count
MIN_PROTOCOLS = 3                   # Minimum protocol count
CLI_CHECK_TIMEOUT = 5               # Seconds for CLI check
```

---

## Error Handling

All functions follow consistent error handling patterns:

### Error Return Pattern

```python
{
    "status": "failed",
    "errors": ["Error message 1", "Error message 2"],
    "warnings": ["Warning message"],
    ...  # Other fields
}
```

### Exception Raising Pattern

Functions raise exceptions for:
- Missing required files (`FileNotFoundError`)
- Invalid input (`ValueError`)
- Security violations (`ValueError`)
- OS errors (`OSError`, `IOError`)

### Auto-Recovery Pattern

`install.install()` provides auto-rollback on deployment failure:

```python
try:
    # Deploy files
    deploy_result = deploy.deploy_framework_files(...)
    if deploy_result["status"] == "failed":
        # Auto-rollback if backup exists
        if backup_path:
            result["status"] = "rollback"
            restore_result = rollback.restore_from_backup(...)
            result["messages"].append("Auto-rolled back due to deployment failure")
        return result
except Exception as e:
    # Auto-rollback on exception
    if backup_path:
        rollback.restore_from_backup(...)
    raise
```

---

## Performance Notes

### Selective Update Optimization

For patch/minor upgrades, installer compares checksums and updates only changed files:

**Example:**
```
Upgrade 1.0.0 → 1.0.1 (5 files changed)
- Total files: 450
- Changed files: 5
- Update strategy: Selective (only 5 files copied)
- Time: <30 seconds (vs <180s for full deployment)
- Speedup: 6x faster
```

### Backup Performance

Backup creation is parallelizable (future enhancement):

**Current:**
- Sequential file copy (~450 files)
- Single-threaded SHA256 hashing
- Time: <20 seconds

**Future Enhancement:**
- Parallel file hashing (multiprocessing)
- Incremental backups (only changed files)
- Compressed backups (gzip/bz2)

---

## See Also

- **README.md** - Quick start guide and usage examples
- **installer/tests/** - Unit test examples (76 tests)
- **installer/tests/integration/** - Integration test workflows (44 tests)
- **STORY-045-version-aware-installer-core.story.md** - Complete specification

---

**Last Updated:** 2025-11-19
**API Version:** 1.0.0
**Story:** STORY-045
