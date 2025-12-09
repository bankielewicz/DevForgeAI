"""Configuration manager service (STORY-082).

Manages installation configuration persistence:
- Loads configuration from `.devforgeai/.install-config.json`
- Saves configuration with validation
- Provides get/set operations for individual values
- Returns defaults if no configuration exists
"""

import json
from pathlib import Path
from datetime import datetime
from typing import Any, Optional

from installer.config.config_models import InstallConfig, MergeStrategy
from installer.config_validator import ConfigValidator
from installer.config.config_models import ValidationResult


class ConfigurationManager:
    """Manages installation configuration persistence.

    Implements SVC-001, SVC-002, SVC-003, SVC-004.
    Stores configuration at `.devforgeai/.install-config.json`.
    """

    CONFIG_FILE_NAME = ".install-config.json"

    def __init__(self, config_dir: str = ".devforgeai", validator: Optional[ConfigValidator] = None):
        """Initialize configuration manager.

        Args:
            config_dir: Directory containing .install-config.json.
                       Default: .devforgeai
            validator: ConfigValidator instance for validation.
                      Default: new instance created
        """
        self.config_dir = Path(config_dir)
        self.config_path = self.config_dir / self.CONFIG_FILE_NAME
        self.validator = validator or ConfigValidator()
        self._config: Optional[InstallConfig] = None

    def load(self) -> InstallConfig:
        """Load configuration from file.

        SVC-001: Loads configuration from `.devforgeai/.install-config.json`
        SVC-003: Returns default config if file doesn't exist

        Returns:
            InstallConfig loaded from file or defaults.

        Raises:
            ValueError: If configuration is invalid.
        """
        # Return cached config if available
        if self._config is not None:
            return self._config

        # Return defaults if file doesn't exist
        if not self.config_path.exists():
            return self._create_default_config()

        try:
            with open(self.config_path, "r") as f:
                data = json.load(f)

            # Validate loaded configuration
            validation = self.validator.validate(data)
            if not validation.is_valid:
                raise ValueError(
                    f"Configuration validation failed:\n"
                    + "\n".join(validation.errors)
                )

            config = InstallConfig.from_dict(data)
            self._config = config
            return config
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON in {self.config_path}: {e}")

    def save(self, config: InstallConfig) -> None:
        """Save configuration to file.

        SVC-002: Saves configuration to `.devforgeai/.install-config.json`

        Args:
            config: Configuration to save.

        Raises:
            ValueError: If configuration is invalid.
            IOError: If file cannot be written.
        """
        # Validate before saving
        validation = self.validator.validate(config.to_dict())
        if not validation.is_valid:
            raise ValueError(
                f"Configuration validation failed:\n"
                + "\n".join(validation.errors)
            )

        # Ensure directory exists
        self.config_dir.mkdir(parents=True, exist_ok=True)

        # Write configuration to file
        with open(self.config_path, "w") as f:
            json.dump(config.to_dict(), f, indent=2)

        # Update cache
        self._config = config

    def get(self, key: str) -> Any:
        """Get configuration value by key.

        SVC-004: Get individual configuration values

        Args:
            key: Configuration key to retrieve.

        Returns:
            Configuration value or None if key doesn't exist.
        """
        config = self.load()
        return getattr(config, key, None)

    def set(self, key: str, value: Any) -> None:
        """Set configuration value.

        SVC-004: Set individual configuration values

        Args:
            key: Configuration key to set.
            value: Value to set.

        Raises:
            ValueError: If key doesn't exist or value is invalid.
        """
        config = self.load()

        # Check key exists
        if not hasattr(config, key):
            raise ValueError(f"Unknown configuration key: {key}")

        # Set value
        setattr(config, key, value)

        # Re-validate after setting
        validation = self.validator.validate(config.to_dict())
        if not validation.is_valid:
            raise ValueError(
                f"Configuration validation failed:\n"
                + "\n".join(validation.errors)
            )

        # Save updated config
        self.save(config)

    def reset(self) -> InstallConfig:
        """Reset configuration to defaults.

        Returns:
            Default configuration.
        """
        default_config = self._create_default_config()
        self.save(default_config)
        return default_config

    def _create_default_config(self) -> InstallConfig:
        """Create default configuration.

        Returns:
            Default InstallConfig.
        """
        return InstallConfig(
            schema_version=1,
            target_path=str(Path.cwd()),
            merge_strategy=MergeStrategy.SMART_MERGE,
            optional_features=[],
            installed_at=datetime.utcnow().isoformat() + "Z",
        )
