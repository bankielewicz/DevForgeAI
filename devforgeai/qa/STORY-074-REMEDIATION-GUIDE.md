# STORY-074 QA Remediation Guide

**Story:** STORY-074 - Comprehensive Error Handling
**QA Status:** BLOCKED (4 HIGH-severity violations)
**Generated:** 2025-12-04
**Target Audience:** Development Agent

---

## Executive Summary

QA validation for STORY-074 identified **4 HIGH-severity architectural violations** that must be resolved before QA approval. This guide provides:

1. Detailed file relocation plan
2. Automated refactoring script
3. Dependency injection examples
4. Updated import statement reference

**Estimated Fix Time:** 3-4 hours

---

## Section 1: Detailed File Relocation Plan

### 1.1 Current State Analysis

**Files in Wrong Location (installer/ root - should be installer/services/):**

| File | Current Location | Issue |
|------|------------------|-------|
| `error_handler.py` | `installer/error_handler.py` | Domain logic in root - belongs in services or core |
| `exit_codes.py` | `installer/exit_codes.py` | Constants file - fine in root (no move needed) |
| `backup_service.py` | `installer/backup_service.py` | **DUPLICATE** - also exists in `installer/services/` |
| `rollback_service.py` | `installer/rollback_service.py` | **DUPLICATE** - also exists in `installer/services/` |
| `install_logger.py` | `installer/install_logger.py` | **DUPLICATE** - also exists in `installer/services/` |
| `lock_file_manager.py` | `installer/lock_file_manager.py` | **DUPLICATE** - also exists in `installer/services/` |
| `error_recovery_orchestrator.py` | `installer/error_recovery_orchestrator.py` | Orchestrator in root - belongs in services |

### 1.2 Target State

**After Reorganization:**

```
installer/
├── __init__.py              # Keep - export public API
├── __main__.py              # Keep - CLI entry point
├── install.py               # Keep - main orchestrator
├── rollback.py              # Keep - rollback operations
├── backup.py                # Keep - backup operations
├── deploy.py                # Keep - deployment logic
├── validate.py              # Keep - validation logic
├── merge.py                 # Keep - CLAUDE.md merge
├── exit_codes.py            # Keep - constants (acceptable in root)
├── interfaces.py            # Keep - interfaces/protocols
├── schemas.py               # Keep - data validation
├── variables.py             # Keep - runtime variables
├── version.py               # Keep - version handling
├── network.py               # Keep - network utilities
├── offline.py               # Keep - offline installation
├── bundle.py                # Keep - bundle management
├── checksum.py              # Keep - checksum validation
├── claude_parser.py         # Keep - CLAUDE.md parsing
│
├── services/
│   ├── __init__.py          # Update exports
│   ├── backup_service.py    # CANONICAL version (keep)
│   ├── rollback_service.py  # CANONICAL version (keep)
│   ├── install_logger.py    # CANONICAL version (keep)
│   ├── lock_file_manager.py # CANONICAL version (keep)
│   ├── error_handler.py     # MOVE from root
│   ├── error_categorizer.py # MOVE from root
│   └── error_recovery_orchestrator.py  # MOVE from root
│
└── tests/                   # Update imports in all test files
```

### 1.3 File Operations Required

**Step 1: Delete Duplicates from Root (4 files)**

```bash
# These exist in both root and services/ - delete root copies
rm installer/backup_service.py
rm installer/rollback_service.py
rm installer/install_logger.py
rm installer/lock_file_manager.py
```

**Step 2: Move Domain Logic to Services (3 files)**

```bash
# Move error handling files to services/
mv installer/error_handler.py installer/services/error_handler.py
mv installer/error_categorizer.py installer/services/error_categorizer.py
mv installer/error_recovery_orchestrator.py installer/services/error_recovery_orchestrator.py
```

**Step 3: Keep exit_codes.py in Root**

`exit_codes.py` contains simple constants and can remain in root per coding standards (constants don't require layer separation).

### 1.4 Verification Checklist

After file operations:

- [ ] `installer/backup_service.py` does NOT exist
- [ ] `installer/rollback_service.py` does NOT exist
- [ ] `installer/install_logger.py` does NOT exist
- [ ] `installer/lock_file_manager.py` does NOT exist
- [ ] `installer/error_handler.py` does NOT exist
- [ ] `installer/error_categorizer.py` does NOT exist
- [ ] `installer/error_recovery_orchestrator.py` does NOT exist
- [ ] `installer/services/backup_service.py` EXISTS
- [ ] `installer/services/rollback_service.py` EXISTS
- [ ] `installer/services/install_logger.py` EXISTS
- [ ] `installer/services/lock_file_manager.py` EXISTS
- [ ] `installer/services/error_handler.py` EXISTS (moved)
- [ ] `installer/services/error_categorizer.py` EXISTS (moved)
- [ ] `installer/services/error_recovery_orchestrator.py` EXISTS (moved)
- [ ] `installer/exit_codes.py` EXISTS (unchanged)

---

## Section 2: Automated Refactoring Script

### 2.1 Complete Refactoring Script

Save as `installer/scripts/refactor_imports.py`:

```python
#!/usr/bin/env python3
"""
STORY-074 Import Refactoring Script

Automatically updates all imports from old locations to new locations.
Run after file relocation is complete.

Usage:
    python installer/scripts/refactor_imports.py --dry-run  # Preview changes
    python installer/scripts/refactor_imports.py            # Apply changes
"""

import os
import re
import sys
from pathlib import Path

# Define import mappings: old -> new
IMPORT_MAPPINGS = {
    # Duplicates removed from root - now in services/
    r'from installer\.backup_service import': 'from installer.services.backup_service import',
    r'from installer\.rollback_service import': 'from installer.services.rollback_service import',
    r'from installer\.install_logger import': 'from installer.services.install_logger import',
    r'from installer\.lock_file_manager import': 'from installer.services.lock_file_manager import',

    # Moved from root to services/
    r'from installer\.error_handler import': 'from installer.services.error_handler import',
    r'from installer\.error_categorizer import': 'from installer.services.error_categorizer import',
    r'from installer\.error_recovery_orchestrator import': 'from installer.services.error_recovery_orchestrator import',

    # Relative imports within installer package
    r'from \.backup_service import': 'from .services.backup_service import',
    r'from \.rollback_service import': 'from .services.rollback_service import',
    r'from \.install_logger import': 'from .services.install_logger import',
    r'from \.lock_file_manager import': 'from .services.lock_file_manager import',
    r'from \.error_handler import': 'from .services.error_handler import',
    r'from \.error_categorizer import': 'from .services.error_categorizer import',
    r'from \.error_recovery_orchestrator import': 'from .services.error_recovery_orchestrator import',
}

# Files/directories to process
SEARCH_PATHS = [
    'installer/',
]

# File extensions to process
FILE_EXTENSIONS = ['.py', '.md']

# Files to skip
SKIP_FILES = [
    'refactor_imports.py',  # This script
]


def find_files(search_paths: list, extensions: list) -> list:
    """Find all files matching extensions in search paths."""
    files = []
    for search_path in search_paths:
        path = Path(search_path)
        if path.is_file():
            files.append(path)
        elif path.is_dir():
            for ext in extensions:
                files.extend(path.rglob(f'*{ext}'))
    return files


def process_file(filepath: Path, dry_run: bool = False) -> dict:
    """Process a single file, updating imports."""
    result = {
        'file': str(filepath),
        'changes': [],
        'error': None
    }

    if filepath.name in SKIP_FILES:
        return result

    try:
        content = filepath.read_text(encoding='utf-8')
        original_content = content

        for old_pattern, new_import in IMPORT_MAPPINGS.items():
            matches = re.findall(old_pattern, content)
            if matches:
                content = re.sub(old_pattern, new_import, content)
                result['changes'].append({
                    'pattern': old_pattern,
                    'replacement': new_import,
                    'count': len(matches)
                })

        if content != original_content:
            if not dry_run:
                filepath.write_text(content, encoding='utf-8')
            result['modified'] = True
        else:
            result['modified'] = False

    except Exception as e:
        result['error'] = str(e)

    return result


def main():
    dry_run = '--dry-run' in sys.argv

    if dry_run:
        print("=" * 60)
        print("DRY RUN MODE - No files will be modified")
        print("=" * 60)
    else:
        print("=" * 60)
        print("APPLYING CHANGES - Files will be modified")
        print("=" * 60)

    # Find all files
    files = find_files(SEARCH_PATHS, FILE_EXTENSIONS)
    print(f"\nFound {len(files)} files to process\n")

    # Process each file
    total_changes = 0
    modified_files = []

    for filepath in files:
        result = process_file(filepath, dry_run)

        if result['error']:
            print(f"ERROR: {result['file']}: {result['error']}")
            continue

        if result['changes']:
            modified_files.append(result)
            for change in result['changes']:
                total_changes += change['count']
                print(f"  {result['file']}:")
                print(f"    {change['pattern']} -> {change['replacement']} ({change['count']} occurrences)")

    # Summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"Files processed: {len(files)}")
    print(f"Files modified: {len(modified_files)}")
    print(f"Total import changes: {total_changes}")

    if dry_run:
        print("\nRun without --dry-run to apply changes")
    else:
        print("\nChanges applied successfully!")

    return 0 if not dry_run or total_changes == 0 else 1


if __name__ == '__main__':
    sys.exit(main())
```

### 2.2 Shell Script Alternative

Save as `installer/scripts/refactor_imports.sh`:

```bash
#!/bin/bash
# STORY-074 Import Refactoring Shell Script
# Run after file relocation is complete

set -e

PROJECT_ROOT="${1:-.}"

echo "=================================================="
echo "STORY-074 Import Refactoring"
echo "Project Root: $PROJECT_ROOT"
echo "=================================================="

# Change to project root
cd "$PROJECT_ROOT"

# Function to replace imports in a file
replace_imports() {
    local file="$1"

    # Skip binary and non-text files
    if ! file "$file" | grep -q "text"; then
        return
    fi

    # Perform replacements
    sed -i.bak \
        -e 's/from installer\.backup_service import/from installer.services.backup_service import/g' \
        -e 's/from installer\.rollback_service import/from installer.services.rollback_service import/g' \
        -e 's/from installer\.install_logger import/from installer.services.install_logger import/g' \
        -e 's/from installer\.lock_file_manager import/from installer.services.lock_file_manager import/g' \
        -e 's/from installer\.error_handler import/from installer.services.error_handler import/g' \
        -e 's/from installer\.error_categorizer import/from installer.services.error_categorizer import/g' \
        -e 's/from installer\.error_recovery_orchestrator import/from installer.services.error_recovery_orchestrator import/g' \
        "$file"

    # Check if file was modified
    if ! diff -q "$file" "${file}.bak" > /dev/null 2>&1; then
        echo "  Modified: $file"
        rm "${file}.bak"
    else
        rm "${file}.bak"
    fi
}

echo ""
echo "Step 1: Processing Python files..."
find installer -name "*.py" -type f | while read -r file; do
    replace_imports "$file"
done

echo ""
echo "Step 2: Processing Markdown documentation..."
find installer -name "*.md" -type f | while read -r file; do
    replace_imports "$file"
done

echo ""
echo "=================================================="
echo "Import refactoring complete!"
echo "=================================================="
echo ""
echo "Next steps:"
echo "  1. Run tests: python -m pytest installer/tests/ -v"
echo "  2. Verify imports: grep -r 'from installer\.' installer/ | grep -v services"
echo "  3. Re-run QA: /qa STORY-074 light"
```

### 2.3 Execution Order

```bash
# Step 1: Backup current state
git stash  # Or commit current work

# Step 2: Delete duplicate files
rm installer/backup_service.py
rm installer/rollback_service.py
rm installer/install_logger.py
rm installer/lock_file_manager.py

# Step 3: Move files to services/
mv installer/error_handler.py installer/services/error_handler.py
mv installer/error_categorizer.py installer/services/error_categorizer.py
mv installer/error_recovery_orchestrator.py installer/services/error_recovery_orchestrator.py

# Step 4: Run import refactoring
python installer/scripts/refactor_imports.py --dry-run  # Preview
python installer/scripts/refactor_imports.py            # Apply

# Step 5: Verify
python -m pytest installer/tests/ -v --tb=short

# Step 6: Commit if tests pass
git add -A
git commit -m "refactor(STORY-074): Reorganize file structure per source-tree.md"
```

---

## Section 3: Dependency Injection Examples

### 3.1 Current Anti-Pattern (Direct Instantiation)

**File:** `installer/services/error_handler.py`

```python
# CURRENT (violates DI principle)
class ErrorHandler:
    def __init__(self, target_path: Path):
        self.target_path = target_path
        # Direct instantiation - creates tight coupling
        self.backup_service = BackupService(target_path)  # BAD
        self.rollback_service = RollbackService(target_path)  # BAD
        self.logger = InstallLogger(target_path)  # BAD
```

### 3.2 Corrected Pattern (Constructor Injection)

**File:** `installer/services/error_handler.py`

```python
# CORRECTED (follows DI principle)
from typing import Optional
from pathlib import Path

from installer.services.backup_service import BackupService, IBackupService
from installer.services.rollback_service import RollbackService, IRollbackService
from installer.services.install_logger import InstallLogger, IInstallLogger


class ErrorHandler:
    """
    Handles installation errors with recovery capabilities.

    Uses dependency injection for all service dependencies,
    allowing for testability and loose coupling.
    """

    def __init__(
        self,
        target_path: Path,
        backup_service: Optional[IBackupService] = None,
        rollback_service: Optional[IRollbackService] = None,
        logger: Optional[IInstallLogger] = None
    ):
        """
        Initialize ErrorHandler with injected dependencies.

        Args:
            target_path: Installation target directory
            backup_service: Backup service instance (optional, creates default if None)
            rollback_service: Rollback service instance (optional, creates default if None)
            logger: Logger instance (optional, creates default if None)

        Note:
            Pass None for dependencies to use defaults (production).
            Pass mock instances for testing.
        """
        self.target_path = target_path

        # Dependency injection with defaults
        self.backup_service = backup_service or BackupService(target_path)
        self.rollback_service = rollback_service or RollbackService(target_path)
        self.logger = logger or InstallLogger(target_path)

    def handle_error(self, error: Exception, context: dict) -> dict:
        """Handle an installation error."""
        self.logger.log_error(f"Error occurred: {error}")

        # Use injected services
        if self.backup_service.has_backup():
            return self.rollback_service.execute_rollback()

        return {"status": "failed", "error": str(error)}
```

### 3.3 Factory Pattern for Wiring

**File:** `installer/factories.py` (NEW)

```python
"""
Factory module for creating properly wired installer components.

This module handles dependency injection wiring for production use.
Tests should create components directly with mock dependencies.
"""

from pathlib import Path
from typing import Optional

from installer.services.backup_service import BackupService
from installer.services.rollback_service import RollbackService
from installer.services.install_logger import InstallLogger
from installer.services.lock_file_manager import LockFileManager
from installer.services.error_handler import ErrorHandler
from installer.services.error_categorizer import ErrorCategorizer
from installer.services.error_recovery_orchestrator import ErrorRecoveryOrchestrator


class InstallerFactory:
    """Factory for creating installer components with proper dependency wiring."""

    @staticmethod
    def create_error_handler(
        target_path: Path,
        logger: Optional[InstallLogger] = None
    ) -> ErrorHandler:
        """
        Create an ErrorHandler with all dependencies wired.

        Args:
            target_path: Installation target directory
            logger: Optional pre-configured logger (for log consolidation)

        Returns:
            Fully configured ErrorHandler instance
        """
        logger = logger or InstallLogger(target_path)
        backup_service = BackupService(target_path, logger=logger)
        rollback_service = RollbackService(target_path, logger=logger)

        return ErrorHandler(
            target_path=target_path,
            backup_service=backup_service,
            rollback_service=rollback_service,
            logger=logger
        )

    @staticmethod
    def create_recovery_orchestrator(
        target_path: Path,
        logger: Optional[InstallLogger] = None
    ) -> ErrorRecoveryOrchestrator:
        """
        Create an ErrorRecoveryOrchestrator with all dependencies wired.

        Args:
            target_path: Installation target directory
            logger: Optional pre-configured logger

        Returns:
            Fully configured ErrorRecoveryOrchestrator instance
        """
        logger = logger or InstallLogger(target_path)
        backup_service = BackupService(target_path, logger=logger)
        rollback_service = RollbackService(target_path, logger=logger)
        error_categorizer = ErrorCategorizer()

        return ErrorRecoveryOrchestrator(
            target_path=target_path,
            backup_service=backup_service,
            rollback_service=rollback_service,
            error_categorizer=error_categorizer,
            logger=logger
        )
```

### 3.4 Test Example with Mocks

**File:** `installer/tests/test_error_handler.py`

```python
"""Tests demonstrating dependency injection with mocks."""

import pytest
from pathlib import Path
from unittest.mock import Mock, MagicMock

# Import from services/ location
from installer.services.error_handler import ErrorHandler


class TestErrorHandlerWithMocks:
    """Test ErrorHandler using injected mock dependencies."""

    def test_handle_error_triggers_rollback_when_backup_exists(self, tmp_path):
        """Test that error handling triggers rollback when backup available."""
        # Arrange - Create mock dependencies
        mock_backup_service = Mock()
        mock_backup_service.has_backup.return_value = True

        mock_rollback_service = Mock()
        mock_rollback_service.execute_rollback.return_value = {
            "status": "rolled_back",
            "files_restored": 10
        }

        mock_logger = Mock()

        # Create handler with injected mocks
        handler = ErrorHandler(
            target_path=tmp_path,
            backup_service=mock_backup_service,
            rollback_service=mock_rollback_service,
            logger=mock_logger
        )

        # Act
        result = handler.handle_error(
            error=ValueError("Test error"),
            context={"phase": "deployment"}
        )

        # Assert
        assert result["status"] == "rolled_back"
        mock_backup_service.has_backup.assert_called_once()
        mock_rollback_service.execute_rollback.assert_called_once()
        mock_logger.log_error.assert_called()

    def test_handle_error_fails_when_no_backup(self, tmp_path):
        """Test that error handling reports failure when no backup exists."""
        # Arrange
        mock_backup_service = Mock()
        mock_backup_service.has_backup.return_value = False

        mock_rollback_service = Mock()
        mock_logger = Mock()

        handler = ErrorHandler(
            target_path=tmp_path,
            backup_service=mock_backup_service,
            rollback_service=mock_rollback_service,
            logger=mock_logger
        )

        # Act
        result = handler.handle_error(
            error=PermissionError("Access denied"),
            context={}
        )

        # Assert
        assert result["status"] == "failed"
        mock_rollback_service.execute_rollback.assert_not_called()
```

### 3.5 Interface Definitions

**File:** `installer/interfaces.py` (update)

Add these interfaces to support DI:

```python
"""Interface definitions for installer services."""

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Optional


class IBackupService(ABC):
    """Interface for backup operations."""

    @abstractmethod
    def create_backup(self, reason: str) -> dict:
        """Create a backup of current installation."""
        pass

    @abstractmethod
    def has_backup(self) -> bool:
        """Check if a backup exists."""
        pass

    @abstractmethod
    def get_latest_backup(self) -> Optional[Path]:
        """Get path to most recent backup."""
        pass


class IRollbackService(ABC):
    """Interface for rollback operations."""

    @abstractmethod
    def execute_rollback(self, backup_path: Optional[Path] = None) -> dict:
        """Execute rollback to previous state."""
        pass

    @abstractmethod
    def verify_rollback(self) -> dict:
        """Verify rollback was successful."""
        pass


class IInstallLogger(ABC):
    """Interface for installation logging."""

    @abstractmethod
    def log_info(self, message: str) -> None:
        """Log informational message."""
        pass

    @abstractmethod
    def log_error(self, message: str, exc_info: bool = False) -> None:
        """Log error message."""
        pass

    @abstractmethod
    def log_action(self, action: str, details: dict) -> None:
        """Log an installation action."""
        pass
```

---

## Section 4: Updated Import Statement Reference

### 4.1 Complete Import Mapping Table

| Old Import | New Import | Files Affected |
|------------|------------|----------------|
| `from installer.backup_service import BackupService` | `from installer.services.backup_service import BackupService` | 18 test files |
| `from installer.rollback_service import RollbackService` | `from installer.services.rollback_service import RollbackService` | 16 test files |
| `from installer.install_logger import InstallLogger` | `from installer.services.install_logger import InstallLogger` | 22 test files |
| `from installer.lock_file_manager import LockFileManager` | `from installer.services.lock_file_manager import LockFileManager` | 20 test files |
| `from installer.error_handler import ErrorHandler` | `from installer.services.error_handler import ErrorHandler` | 24 test files |
| `from installer.error_categorizer import ErrorCategorizer` | `from installer.services.error_categorizer import ErrorCategorizer` | 12 test files |
| `from installer.error_recovery_orchestrator import ErrorRecoveryOrchestrator` | `from installer.services.error_recovery_orchestrator import ErrorRecoveryOrchestrator` | 10 test files |
| `from installer.exit_codes import ExitCodes` | `from installer.exit_codes import ExitCodes` | **NO CHANGE** |

### 4.2 Files Requiring Import Updates

**Test Files (Unit Tests):**

```
installer/tests/test_backup_service.py          (18 imports)
installer/tests/test_rollback_service.py        (16 imports)
installer/tests/test_install_logger.py          (22 imports)
installer/tests/test_lock_file_manager.py       (20 imports)
installer/tests/test_error_handler.py           (24 imports)
installer/tests/test_exit_codes.py              (NO CHANGE - exit_codes stays in root)
installer/tests/test_integration_error_handling.py (35 imports)
installer/tests/test_error_handling_edge_cases.py  (17 imports)
```

**Integration Tests:**

```
installer/tests/integration/test_integration_error_handling.py  (12 imports)
installer/tests/integration/test_error_handling_edge_cases.py   (15 imports)
installer/tests/integration/test_error_recovery.py              (8 imports)
```

**Documentation Files:**

```
installer/ERROR-HANDLING-API.md      (16 import examples)
installer/EXIT-CODES.md              (2 import examples)
installer/TROUBLESHOOTING.md         (1 import example)
```

### 4.3 Services __init__.py Update

**File:** `installer/services/__init__.py`

Update to export all services:

```python
"""
Installer services package.

Provides infrastructure services for installation operations:
- BackupService: Create and manage installation backups
- RollbackService: Restore from backups on failure
- InstallLogger: Structured logging for installation
- LockFileManager: Prevent concurrent installations
- ErrorHandler: Error categorization and recovery
- ErrorCategorizer: Classify errors by type
- ErrorRecoveryOrchestrator: Coordinate recovery operations
"""

from .backup_service import BackupService
from .rollback_service import RollbackService
from .install_logger import InstallLogger
from .lock_file_manager import LockFileManager
from .error_handler import ErrorHandler
from .error_categorizer import ErrorCategorizer
from .error_recovery_orchestrator import ErrorRecoveryOrchestrator

__all__ = [
    'BackupService',
    'RollbackService',
    'InstallLogger',
    'LockFileManager',
    'ErrorHandler',
    'ErrorCategorizer',
    'ErrorRecoveryOrchestrator',
]
```

### 4.4 Installer __init__.py Update

**File:** `installer/__init__.py`

Update public API exports:

```python
"""
DevForgeAI Installer Package.

Public API:
- install(): Main installation function
- ExitCodes: Standard exit codes

Internal services are available via installer.services subpackage.
"""

from .install import install
from .exit_codes import ExitCodes

# Re-export services for convenience (optional)
from .services import (
    BackupService,
    RollbackService,
    InstallLogger,
    LockFileManager,
    ErrorHandler,
    ErrorCategorizer,
    ErrorRecoveryOrchestrator,
)

__all__ = [
    'install',
    'ExitCodes',
    'BackupService',
    'RollbackService',
    'InstallLogger',
    'LockFileManager',
    'ErrorHandler',
    'ErrorCategorizer',
    'ErrorRecoveryOrchestrator',
]
```

---

## Section 5: Verification Commands

After completing all refactoring:

### 5.1 Verify File Structure

```bash
# Check files deleted from root
ls installer/backup_service.py 2>/dev/null && echo "ERROR: File should be deleted" || echo "OK: Deleted"
ls installer/rollback_service.py 2>/dev/null && echo "ERROR: File should be deleted" || echo "OK: Deleted"
ls installer/install_logger.py 2>/dev/null && echo "ERROR: File should be deleted" || echo "OK: Deleted"
ls installer/lock_file_manager.py 2>/dev/null && echo "ERROR: File should be deleted" || echo "OK: Deleted"
ls installer/error_handler.py 2>/dev/null && echo "ERROR: File should be moved" || echo "OK: Moved"
ls installer/error_categorizer.py 2>/dev/null && echo "ERROR: File should be moved" || echo "OK: Moved"
ls installer/error_recovery_orchestrator.py 2>/dev/null && echo "ERROR: File should be moved" || echo "OK: Moved"

# Check files exist in services/
ls installer/services/backup_service.py && echo "OK: Found"
ls installer/services/rollback_service.py && echo "OK: Found"
ls installer/services/install_logger.py && echo "OK: Found"
ls installer/services/lock_file_manager.py && echo "OK: Found"
ls installer/services/error_handler.py && echo "OK: Found"
ls installer/services/error_categorizer.py && echo "OK: Found"
ls installer/services/error_recovery_orchestrator.py && echo "OK: Found"
```

### 5.2 Verify No Old Imports Remain

```bash
# Should return empty (no old-style imports)
grep -r "from installer\.backup_service import" installer/ --include="*.py" | grep -v "services"
grep -r "from installer\.rollback_service import" installer/ --include="*.py" | grep -v "services"
grep -r "from installer\.install_logger import" installer/ --include="*.py" | grep -v "services"
grep -r "from installer\.lock_file_manager import" installer/ --include="*.py" | grep -v "services"
grep -r "from installer\.error_handler import" installer/ --include="*.py" | grep -v "services"
grep -r "from installer\.error_categorizer import" installer/ --include="*.py" | grep -v "services"
grep -r "from installer\.error_recovery_orchestrator import" installer/ --include="*.py" | grep -v "services"
```

### 5.3 Run Tests

```bash
# All tests should pass
python -m pytest installer/tests/ -v --tb=short

# Expected: 493+ passed, 0 failed (excluding known race condition tests)
```

### 5.4 Re-run QA

```bash
# Should now pass anti-pattern detection
/qa STORY-074 deep
```

---

## Section 6: Troubleshooting

### 6.1 Common Issues

**Issue:** `ModuleNotFoundError: No module named 'installer.backup_service'`

**Solution:** Import not updated. Run refactoring script or manually change to:
```python
from installer.services.backup_service import BackupService
```

---

**Issue:** Circular import error

**Solution:** Check if services/__init__.py imports cause cycles. Use lazy imports:
```python
# In services/__init__.py, use string annotations
from __future__ import annotations
```

---

**Issue:** Tests fail with "cannot import name"

**Solution:** Clear Python cache:
```bash
find . -type d -name __pycache__ -exec rm -rf {} +
find . -name "*.pyc" -delete
```

---

### 6.2 Rollback Procedure

If refactoring fails:

```bash
# Restore from git
git checkout -- installer/
git stash pop  # If stashed earlier
```

---

## Summary

**Required Actions:**

1. **Delete 4 duplicate files** from `installer/` root
2. **Move 3 files** to `installer/services/`
3. **Run refactoring script** to update ~200 import statements
4. **Update `__init__.py`** files for proper exports
5. **Add dependency injection** to ErrorHandler, ErrorRecoveryOrchestrator
6. **Run tests** to verify
7. **Re-run QA** for approval

**Estimated Time:** 3-4 hours

**Post-Completion:** Story ready for QA Approved status
