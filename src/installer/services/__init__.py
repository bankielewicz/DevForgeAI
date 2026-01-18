"""Services package - Infrastructure layer for installer (STORY-074).

This package contains service implementations that handle low-level concerns:
- Backup operations (backup_service.py)
- Rollback operations (rollback_service.py)
- Installation logging (install_logger.py)
- Lock file management (lock_file_manager.py)

Services are designed to be independent, with no circular dependencies.
They are invoked by higher-level components (orchestrators, handlers).

Architecture pattern:
- Domain Layer: ErrorCategorizer (error_handler.py) - pure business logic
- Infrastructure Layer: ErrorRecoveryOrchestrator (error_orchestrator.py) - service composition
"""

from .backup_service import BackupService
from .rollback_service import RollbackService
from .install_logger import InstallLogger
from .lock_file_manager import LockFileManager

__all__ = [
    'BackupService',
    'RollbackService',
    'InstallLogger',
    'LockFileManager',
]
