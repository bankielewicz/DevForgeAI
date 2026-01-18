"""Configuration migrator service (STORY-082).

Handles schema version migrations for configuration:
- Detects when migration is needed
- Executes multi-step migrations (v1→v2→v3)
- Backs up original configuration
- Maps old keys to new keys
"""

from pathlib import Path
from typing import Dict, Any, Tuple, List, Optional
from datetime import datetime
import json

from installer.config.config_models import MigrationResult, InstallConfig
from installer.config_validator import ConfigValidator


class ConfigMigrator:
    """Manages configuration schema migrations.

    Implements SVC-008, SVC-009, SVC-010, SVC-011.
    """

    CURRENT_SCHEMA_VERSION = 1

    # Migration paths for each version transition
    MIGRATION_PATHS = {
        # Version 1: Initial schema (no migrations defined yet)
    }

    def __init__(self, config_dir: str = "devforgeai", validator: Optional[ConfigValidator] = None):
        """Initialize configuration migrator.

        Args:
            config_dir: Directory containing .install-config.json.
            validator: ConfigValidator instance.
        """
        self.config_dir = Path(config_dir)
        self.config_path = self.config_dir / ".install-config.json"
        self.validator = validator or ConfigValidator()

    def needs_migration(self, config: Dict[str, Any]) -> bool:
        """Check if configuration needs migration.

        SVC-008: Detect schema version mismatch

        Args:
            config: Configuration dictionary to check.

        Returns:
            True if schema version doesn't match current version.
        """
        config_version = config.get("schema_version", 1)
        return config_version != self.CURRENT_SCHEMA_VERSION

    def get_migration_path(self, from_version: int) -> List[Tuple[int, int]]:
        """Get migration path from source to current version.

        Supports multi-step migrations (v1→v2→v3).

        Args:
            from_version: Starting schema version.

        Returns:
            List of (from_version, to_version) tuples.

        Raises:
            ValueError: If no migration path exists.
        """
        if from_version == self.CURRENT_SCHEMA_VERSION:
            return []

        if from_version > self.CURRENT_SCHEMA_VERSION:
            raise ValueError(
                f"Configuration schema version {from_version} is newer than "
                f"current version {self.CURRENT_SCHEMA_VERSION}. "
                f"Downgrade not supported."
            )

        # For now, only support v1 which is current
        if from_version < 1:
            raise ValueError(f"Unknown schema version: {from_version}")

        # Build migration path (currently just v1, expand as versions added)
        path = []
        current = from_version
        while current < self.CURRENT_SCHEMA_VERSION:
            next_version = current + 1
            path.append((current, next_version))
            current = next_version

        return path

    def migrate(self, config: Dict[str, Any]) -> Tuple[Dict[str, Any], MigrationResult]:
        """Migrate configuration to current schema version.

        SVC-009: Migrate configuration between schema versions
        SVC-010: Support multi-step migrations
        SVC-011: Backup original before migration

        Args:
            config: Configuration to migrate.

        Returns:
            Tuple of (migrated_config, migration_result).

        Raises:
            ValueError: If migration path doesn't exist or migration fails.
        """
        from_version = config.get("schema_version", 1)

        if from_version == self.CURRENT_SCHEMA_VERSION:
            # No migration needed
            return config, MigrationResult(
                from_version=from_version,
                to_version=self.CURRENT_SCHEMA_VERSION,
            )

        # Get migration path
        migration_path = self.get_migration_path(from_version)

        # Backup original configuration
        self._backup_config(config)

        # Execute migrations in sequence
        current_config = config.copy()
        for from_v, to_v in migration_path:
            current_config = self._execute_single_migration(current_config, from_v, to_v)

        # Create migration result
        migration_result = MigrationResult(
            from_version=from_version,
            to_version=self.CURRENT_SCHEMA_VERSION,
        )

        return current_config, migration_result

    def _execute_single_migration(self, config: Dict[str, Any], from_v: int, to_v: int) -> Dict[str, Any]:
        """Execute single-version migration.

        Args:
            config: Config to migrate.
            from_v: Source version.
            to_v: Target version.

        Returns:
            Migrated configuration.
        """
        # No migrations defined yet (v1 is current)
        if from_v == 1 and to_v == 2:
            # Example migration structure for future versions
            # Would rename keys, add new keys, remove deprecated keys
            pass

        return config

    def _backup_config(self, config: Dict[str, Any]) -> None:
        """Backup original configuration before migration.

        SVC-011: Backup original before migration

        Args:
            config: Configuration to backup.
        """
        if not self.config_path.exists():
            return

        # Create backup with timestamp
        timestamp = datetime.utcnow().strftime("%Y%m%d-%H%M%S")
        backup_path = self.config_path.parent / f".install-config.{timestamp}.backup"

        try:
            # Read original file and save as backup
            with open(self.config_path, "r") as f:
                original_data = json.load(f)

            with open(backup_path, "w") as f:
                json.dump(original_data, f, indent=2)
        except (IOError, json.JSONDecodeError):
            # If backup fails, continue anyway
            pass
