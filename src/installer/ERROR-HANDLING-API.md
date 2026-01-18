# Error Handling API Reference

**Version:** 1.0.0
**Story:** STORY-074 - Comprehensive Error Handling
**Status:** Production Ready (114 tests passing)

Comprehensive API documentation for error handling services: ExitCodes, ErrorHandler, BackupService, RollbackService, InstallLogger, and LockFileManager.

---

## Table of Contents

1. [ExitCodes Module](#exitcodes-module)
2. [ErrorHandler Service](#errorhandler-service)
3. [BackupService](#backupservice)
4. [InstallLogger](#installlogger)
5. [Common Patterns](#common-patterns)
6. [Examples](#examples)

---

## ExitCodes Module

**Module:** `installer.exit_codes`

Provides standardized exit codes for installation operations.

### Constants

```python
from installer.exit_codes import (
    SUCCESS,               # 0
    MISSING_SOURCE,        # 1
    PERMISSION_DENIED,     # 2
    ROLLBACK_OCCURRED,     # 3
    VALIDATION_FAILED,     # 4
)
```

### Class: ExitCodes

```python
class ExitCodes:
    """Standard exit codes for installer process."""

    SUCCESS = 0
    MISSING_SOURCE = 1
    PERMISSION_DENIED = 2
    ROLLBACK_OCCURRED = 3
    VALIDATION_FAILED = 4
```

### Usage

```python
from installer.exit_codes import ExitCodes

# Use via class
print(ExitCodes.SUCCESS)  # 0
print(ExitCodes.ROLLBACK_OCCURRED)  # 3

# Use direct imports
from installer.exit_codes import SUCCESS, ROLLBACK_OCCURRED
print(SUCCESS)  # 0
print(ROLLBACK_OCCURRED)  # 3
```

---

## ErrorHandler Service

**Module:** `installer.error_handler`

Handles error categorization, message formatting, and exit code determination.

### Class: ErrorHandler

```python
class ErrorHandler:
    """Handles error categorization and user-friendly message formatting."""

    def __init__(
        self,
        logger: Optional[InstallLogger] = None,
        rollback_service=None,
        backup_service=None
    )
```

**Parameters:**
- `logger` (InstallLogger): Logger instance for error logging
- `rollback_service` (RollbackService): Rollback service for error recovery
- `backup_service` (BackupService): Backup service for backup location info

### Methods

#### categorize_error()

```python
def categorize_error(
    self,
    error: Exception,
    rollback_triggered: bool = False,
    validation_phase: bool = False
) -> ErrorCategory
```

**Purpose:** Categorize error into one of 5 types.

**Parameters:**
- `error` (Exception): Exception to categorize
- `rollback_triggered` (bool): If True, force ROLLBACK_OCCURRED category
- `validation_phase` (bool): If True, force VALIDATION_FAILED category

**Returns:** ErrorCategory with name and exit_code

**Example:**
```python
handler = ErrorHandler()

error = FileNotFoundError("File not found")
category = handler.categorize_error(error)
print(category.name)  # "MISSING_SOURCE"
print(category.exit_code)  # 1

# Force rollback category
category = handler.categorize_error(error, rollback_triggered=True)
print(category.name)  # "ROLLBACK_OCCURRED"
print(category.exit_code)  # 3
```

---

#### format_console_message()

```python
def format_console_message(
    self,
    error: Optional[Exception] = None,
    include_rollback_info: bool = False
) -> str
```

**Purpose:** Format error as user-friendly console message (no stack traces).

**Parameters:**
- `error` (Exception): Exception to format (None = success)
- `include_rollback_info` (bool): Include backup location in message

**Returns:** Formatted string message

**Example:**
```python
handler = ErrorHandler()

error = PermissionError("[Errno 13] Permission denied")
message = handler.format_console_message(error)
print(message)
# Output:
# ERROR: Permission Denied
# Insufficient permissions for installation.
#
# Details: [Errno 13] Permission denied
#
# Resolution steps:
#   1. Run with appropriate permissions (sudo may be needed)
#   2. Check file ownership: chown user:group <path>
#   3. Verify directory write permissions: chmod u+w <path>
#
# For details, see log file: devforgeai/install.log
```

---

#### get_exit_code()

```python
def get_exit_code(
    self,
    error: Optional[Exception] = None,
    rollback_triggered: bool = False
) -> int
```

**Purpose:** Get exit code for an error.

**Parameters:**
- `error` (Exception): Exception (None = SUCCESS)
- `rollback_triggered` (bool): If True, return ROLLBACK_OCCURRED

**Returns:** Exit code (0, 1, 2, 3, or 4)

**Example:**
```python
handler = ErrorHandler()

# Success case
exit_code = handler.get_exit_code(None)
print(exit_code)  # 0

# Error cases
exit_code = handler.get_exit_code(FileNotFoundError("..."))
print(exit_code)  # 1

exit_code = handler.get_exit_code(PermissionError("..."))
print(exit_code)  # 2

# With rollback
exit_code = handler.get_exit_code(
    error=Exception("Generic error"),
    rollback_triggered=True
)
print(exit_code)  # 3
```

---

#### get_resolution_steps()

```python
def get_resolution_steps(
    self,
    error: Optional[Exception] = None
) -> List[str]
```

**Purpose:** Get 1-3 resolution steps for error.

**Parameters:**
- `error` (Exception): Exception (None = generic steps)

**Returns:** List of resolution steps (≤200 chars each)

**Example:**
```python
handler = ErrorHandler()

error = PermissionError("Permission denied")
steps = handler.get_resolution_steps(error)

for i, step in enumerate(steps, 1):
    print(f"{i}. {step}")

# Output:
# 1. Run with appropriate permissions (sudo may be needed)
# 2. Check file ownership: chown user:group <path>
# 3. Verify directory write permissions: chmod u+w <path>
```

---

#### handle_error()

```python
def handle_error(
    self,
    error: Optional[Exception] = None,
    phase: Optional[str] = None,
    include_rollback_info: bool = False
) -> ErrorResult
```

**Purpose:** Handle error with logging and optional rollback.

**Parameters:**
- `error` (Exception): Exception to handle
- `phase` (str): Installation phase (e.g., "file_copy")
- `include_rollback_info` (bool): Include backup location

**Returns:** ErrorResult with exit_code and console_message

**Example:**
```python
handler = ErrorHandler()

error = FileNotFoundError("File not found")
result = handler.handle_error(
    error=error,
    phase="file_copy",
    include_rollback_info=True
)

print(result.exit_code)  # 1
print(result.console_message)  # Formatted error message
```

---

#### check_concurrent_installation()

```python
def check_concurrent_installation(
    self,
    lock_file_exists: bool
) -> None
```

**Purpose:** Check if another installation in progress.

**Parameters:**
- `lock_file_exists` (bool): Whether lock file exists

**Raises:** RuntimeError if concurrent installation detected

**Example:**
```python
from pathlib import Path

handler = ErrorHandler()
lock_file = Path("devforgeai/install.lock")

try:
    handler.check_concurrent_installation(lock_file.exists())
except RuntimeError as e:
    print(f"Concurrent installation detected: {e}")
```

---

#### log_and_format_error()

```python
def log_and_format_error(
    self,
    error: Exception,
    file_paths: Optional[Dict] = None
) -> Tuple[str, int]
```

**Purpose:** Log error and return formatted message + exit code.

**Parameters:**
- `error` (Exception): Exception to handle
- `file_paths` (Dict): Dict with 'source' and 'target' keys

**Returns:** Tuple of (formatted_message, exit_code)

**Example:**
```python
handler = ErrorHandler()

error = PermissionError("Permission denied")
message, code = handler.log_and_format_error(
    error=error,
    file_paths={
        'source': 'src/claude/commands/dev.md',
        'target': '/path/to/project/.claude/commands/dev.md'
    }
)

print(f"Exit code: {code}")
print(f"Message:\n{message}")
```

---

## BackupService

**Module:** `installer.backup_service`

Creates and manages timestamped backups.

### Class: BackupService

```python
class BackupService:
    """Creates timestamped backups with structure preservation."""

    def __init__(self, logger: InstallLogger)
```

**Parameters:**
- `logger` (InstallLogger): Logger for backup operations

### Methods

#### create_backup()

```python
def create_backup(
    self,
    target_dir: Path,
    files_to_backup: List[Path]
) -> Path
```

**Purpose:** Create timestamped backup directory and copy files (AC#7).

**Parameters:**
- `target_dir` (Path): Base directory where devforgeai will be created
- `files_to_backup` (List[Path]): File paths to backup

**Returns:** Path to created backup directory

**Raises:**
- `PermissionError`: If backup directory cannot be created
- `OSError`: If file copy fails

**Example:**
```python
from pathlib import Path
from installer.backup_service import BackupService
from installer.install_logger import InstallLogger

logger = InstallLogger()
backup_service = BackupService(logger)

backup_dir = backup_service.create_backup(
    target_dir=Path("/path/to/project"),
    files_to_backup=[
        Path("/path/to/project/.claude/commands/dev.md"),
        Path("/path/to/project/devforgeai/protocols/"),
    ]
)

print(backup_dir)
# /path/to/project/devforgeai/install-backup-2025-12-03T14-30-45/
```

---

#### cleanup_old_backups()

```python
def cleanup_old_backups(
    self,
    target_dir: Path,
    max_age_days: int = 7,
    min_keep: int = 5
) -> List[Path]
```

**Purpose:** Remove backups older than max_age_days (keeping minimum).

**Parameters:**
- `target_dir` (Path): Target project directory
- `max_age_days` (int): Max backup age in days (default: 7)
- `min_keep` (int): Minimum backups to keep (default: 5)

**Returns:** List of removed backup paths

**Example:**
```python
backup_service = BackupService(logger)

removed = backup_service.cleanup_old_backups(
    target_dir=Path("/path/to/project"),
    max_age_days=7,
    min_keep=5
)

for backup_path in removed:
    print(f"Removed: {backup_path}")
```

---

## InstallLogger

**Module:** `installer.install_logger`

Logs installation operations with timestamps and stack traces.

### Class: InstallLogger

```python
class InstallLogger:
    """Thread-safe logging for installation operations."""

    def __init__(self, log_file: Optional[Path] = None)
```

**Parameters:**
- `log_file` (Path): Log file location (default: devforgeai/install.log)

### Methods

#### log_info()

```python
def log_info(
    self,
    message: str,
    phase: Optional[str] = None,
    details: Optional[Dict] = None
) -> None
```

**Purpose:** Log informational message.

**Parameters:**
- `message` (str): Message to log
- `phase` (str): Installation phase (e.g., "backup", "deploy")
- `details` (Dict): Additional context

**Example:**
```python
logger = InstallLogger()

logger.log_info(
    message="Starting deployment",
    phase="deploy",
    details={"files": 450}
)
# [2025-12-03T14:30:45.123Z] [INFO] [deploy] Starting deployment
```

---

#### log_error()

```python
def log_error(
    self,
    error: Exception,
    category: str,
    exit_code: int,
    message: Optional[str] = None,
    source_path: Optional[Path] = None,
    target_path: Optional[Path] = None
) -> None
```

**Purpose:** Log error with stack trace.

**Parameters:**
- `error` (Exception): Exception object
- `category` (str): Error category (MISSING_SOURCE, PERMISSION_DENIED, etc.)
- `exit_code` (int): Exit code (0-4)
- `message` (str): Custom message
- `source_path` (Path): Source file path (if applicable)
- `target_path` (Path): Target file path (if applicable)

**Example:**
```python
logger = InstallLogger()

try:
    # Do something
except PermissionError as e:
    logger.log_error(
        error=e,
        category="PERMISSION_DENIED",
        exit_code=2,
        message="Failed to write to target",
        source_path=Path("src/claude/commands/dev.md"),
        target_path=Path("/path/to/project/.claude/commands/dev.md")
    )
```

---

#### log_progress()

```python
def log_progress(
    self,
    step: str,
    total_steps: int,
    current_step: int
) -> None
```

**Purpose:** Log progress during deployment.

**Parameters:**
- `step` (str): Current step description
- `total_steps` (int): Total steps
- `current_step` (int): Current step number

**Example:**
```python
logger = InstallLogger()

for i in range(1, 11):
    logger.log_progress(
        step="Copying files",
        total_steps=10,
        current_step=i
    )
    # [2025-12-03T14:30:46.234Z] [INFO] Progress: 1/10 - Copying files
```

---

## Common Patterns

### Pattern 1: Error Handling with Rollback

```python
from installer.error_handler import ErrorHandler
from installer.rollback_service import RollbackService

error_handler = ErrorHandler(rollback_service=rollback_service)

try:
    # Do installation work
    pass
except Exception as error:
    # Handle error
    result = error_handler.handle_error(
        error=error,
        phase="file_copy",
        include_rollback_info=True
    )

    print(result.console_message)
    exit(result.exit_code)
```

---

### Pattern 2: Categorizing and Responding to Errors

```python
from installer.error_handler import ErrorHandler
from installer.exit_codes import (
    MISSING_SOURCE,
    PERMISSION_DENIED,
    ROLLBACK_OCCURRED
)

handler = ErrorHandler()

try:
    # Installation code
    pass
except Exception as error:
    category = handler.categorize_error(error)

    if category.exit_code == MISSING_SOURCE:
        print("Create missing source files")
    elif category.exit_code == PERMISSION_DENIED:
        print("Fix target directory permissions")
    elif category.exit_code == ROLLBACK_OCCURRED:
        print("Rollback will be triggered")
```

---

### Pattern 3: Creating Backups with Error Handling

```python
from pathlib import Path
from installer.backup_service import BackupService
from installer.install_logger import InstallLogger

logger = InstallLogger()
backup_service = BackupService(logger)

try:
    backup_dir = backup_service.create_backup(
        target_dir=Path("/path/to/project"),
        files_to_backup=[...]
    )
    print(f"Backup created: {backup_dir}")
except PermissionError:
    print("Cannot create backup - insufficient permissions")
    exit(2)
except OSError as e:
    print(f"Backup failed: {e}")
    exit(3)
```

---

### Pattern 4: Logging Installation Flow

```python
from installer.install_logger import InstallLogger

logger = InstallLogger()

logger.log_info("Starting installation", phase="init")
logger.log_info("Creating backup", phase="backup")

try:
    # Deploy files
    logger.log_progress("Deploying", total_steps=450, current_step=1)
except Exception as e:
    logger.log_error(
        error=e,
        category="PERMISSION_DENIED",
        exit_code=2,
        message="Deployment failed"
    )
```

---

## Examples

### Example 1: Handling Missing Source

```python
from installer.error_handler import ErrorHandler
from pathlib import Path

handler = ErrorHandler()

try:
    version_file = Path("src/devforgeai/version.json")
    if not version_file.exists():
        raise FileNotFoundError(f"Not found: {version_file}")
except FileNotFoundError as error:
    message = handler.format_console_message(error)
    exit_code = handler.get_exit_code(error)

    print(message)
    exit(exit_code)  # Exit code 1
```

**Output:**
```
ERROR: Missing Source Files
Required source files not found.

Details: Not found: src/devforgeai/version.json

Resolution steps:
  1. Verify .claude/ directory exists in source
  2. Check file permissions on source directory
  3. Ensure source path is correct

For details, see log file: devforgeai/install.log
```

---

### Example 2: Handling Concurrent Installation

```python
from pathlib import Path
from installer.error_handler import ErrorHandler

handler = ErrorHandler()
lock_file = Path("devforgeai/install.lock")

try:
    handler.check_concurrent_installation(lock_file.exists())
    # Continue with installation
except RuntimeError as error:
    print(handler.format_console_message(error))
    exit(handler.get_exit_code(error))
```

**Output (if lock exists):**
```
Concurrent installation detected. Another installation is currently
in progress. Wait for it to complete or remove the lock file at
devforgeai/install.lock
```

---

### Example 3: Complete Installation with Error Handling

```python
from pathlib import Path
from installer.error_handler import ErrorHandler
from installer.backup_service import BackupService
from installer.install_logger import InstallLogger

def install_with_error_handling(target_path):
    logger = InstallLogger()
    backup_service = BackupService(logger)
    error_handler = ErrorHandler(
        logger=logger,
        backup_service=backup_service
    )

    try:
        # Phase 1: Create backup
        logger.log_info("Creating backup", phase="backup")
        backup_dir = backup_service.create_backup(
            target_dir=Path(target_path),
            files_to_backup=[...]
        )

        # Phase 2: Deploy files
        logger.log_info("Deploying files", phase="deploy")
        # ... deployment code ...

        # Phase 3: Cleanup old backups
        logger.log_info("Cleaning up old backups", phase="cleanup")
        backup_service.cleanup_old_backups(Path(target_path))

        # Success
        message = error_handler.format_console_message(None)
        print(message)
        return 0

    except Exception as error:
        logger.log_error(
            error=error,
            category="ROLLBACK_OCCURRED",
            exit_code=3,
            message="Installation failed"
        )

        result = error_handler.handle_error(
            error=error,
            phase="deploy",
            include_rollback_info=True
        )

        print(result.console_message)
        return result.exit_code

if __name__ == "__main__":
    exit_code = install_with_error_handling("/path/to/project")
    exit(exit_code)
```

---

## Related Documentation

- **EXIT-CODES.md** - Exit code reference and usage
- **TROUBLESHOOTING.md** - Common issues and recovery
- **README.md** - Installation overview
- **STORY-074** - Complete error handling specification

---

**Last Updated:** 2025-12-03
**Version:** 1.0.0
**Story:** STORY-074 - Comprehensive Error Handling
