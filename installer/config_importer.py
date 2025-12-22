"""Configuration importer service (STORY-082).

Imports configuration from JSON file:
- Validates configuration before importing
- Checks schema version compatibility
- Auto-migrates if schema differs
- Applies valid configuration
"""

import json
from pathlib import Path
from typing import Tuple, List, Dict, Any, Optional

from installer.config.config_models import InstallConfig
from installer.config_validator import ConfigValidator
from installer.config_migrator import ConfigMigrator


class ConfigImporter:
    """Imports and validates configuration from files.

    Implements SVC-014, SVC-015, SVC-016.
    """

    def __init__(
        self,
        config_dir: str = "devforgeai",
        validator: Optional[ConfigValidator] = None,
        migrator: Optional[ConfigMigrator] = None,
    ):
        """Initialize configuration importer.

        Args:
            config_dir: Target directory for .install-config.json.
            validator: ConfigValidator instance.
            migrator: ConfigMigrator instance.
        """
        self.config_dir = Path(config_dir)
        self.validator = validator or ConfigValidator()
        self.migrator = migrator or ConfigMigrator(config_dir)

    def import_config(self, file_path: str) -> Tuple[InstallConfig, List[str]]:
        """Import and apply configuration from JSON file.

        SVC-014: Import configuration from JSON file
        SVC-015: Validate before importing
        SVC-016: Migrate if schema version differs

        Args:
            file_path: Path to configuration JSON file.

        Returns:
            Tuple of (InstallConfig, list of messages about migration/defaults).

        Raises:
            ValueError: If configuration is invalid.
            IOError: If file cannot be read.
        """
        messages = []

        # Read JSON file
        file_path_obj = Path(file_path)
        if not file_path_obj.exists():
            raise IOError(f"Configuration file not found: {file_path}")

        try:
            with open(file_path_obj, "r") as f:
                config_data = json.load(f)
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON in {file_path}: {e}")

        # Check if migration is needed
        if self.migrator.needs_migration(config_data):
            migrated_config, migration_result = self.migrator.migrate(config_data)
            config_data = migrated_config
            messages.append(
                f"Configuration migrated from v{migration_result.from_version} "
                f"to v{migration_result.to_version}"
            )

        # Validate configuration
        validation = self.validator.validate(config_data)
        if not validation.is_valid:
            error_msg = "Configuration validation failed:\n" + "\n".join(
                validation.errors
            )
            raise ValueError(error_msg)

        if validation.warnings:
            messages.extend(validation.warnings)

        # Create InstallConfig from validated data
        config = InstallConfig.from_dict(config_data)

        return config, messages
