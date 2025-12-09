"""Configuration validator service (STORY-082).

Validates installation configuration against schema:
- Checks required keys present
- Validates value types
- Warns about unknown keys
"""

from typing import Dict, Any, List
from installer.config.config_models import ValidationResult, MergeStrategy


class ConfigValidator:
    """Validates configuration data against schema.

    Implements SVC-005, SVC-006, SVC-007.
    """

    # Required keys for valid configuration
    REQUIRED_KEYS = {
        "schema_version": int,
        "target_path": str,
        "merge_strategy": str,
        "optional_features": list,
        "installed_at": str,
    }

    # Valid merge strategy values
    VALID_STRATEGIES = {strategy.value for strategy in MergeStrategy}

    # Known optional keys
    KNOWN_KEYS = REQUIRED_KEYS.keys() | {"last_upgraded_at"}

    def validate(self, config: Dict[str, Any]) -> ValidationResult:
        """Validate configuration against schema.

        SVC-005: Validates required keys present
        SVC-006: Validates value types
        SVC-007: Warns about unknown keys

        Args:
            config: Configuration dictionary to validate.

        Returns:
            ValidationResult indicating validity and any errors/warnings.
        """
        result = ValidationResult(is_valid=True)

        # Check required keys
        for key, expected_type in self.REQUIRED_KEYS.items():
            if key not in config:
                result.add_error(f"Missing required key: {key}")
                continue

            # Validate type
            value = config[key]
            if not isinstance(value, expected_type):
                result.add_error(
                    f"Invalid type for '{key}': expected {expected_type.__name__}, "
                    f"got {type(value).__name__}"
                )

            # Special validation for specific keys
            if key == "merge_strategy" and isinstance(value, str):
                if value not in self.VALID_STRATEGIES:
                    result.add_error(
                        f"Invalid merge_strategy '{value}'. "
                        f"Must be one of: {', '.join(self.VALID_STRATEGIES)}"
                    )

            if key == "schema_version" and isinstance(value, int):
                if value < 1:
                    result.add_error("schema_version must be positive integer")

            if key == "optional_features" and not isinstance(value, list):
                result.add_error("optional_features must be array")
            elif key == "optional_features":
                # Validate array contains strings
                for item in value:
                    if not isinstance(item, str):
                        result.add_error(
                            f"optional_features must contain strings, got {type(item).__name__}"
                        )

        # Warn about unknown keys
        for key in config.keys():
            if key not in self.KNOWN_KEYS:
                result.add_warning(f"Unknown key '{key}' - will be ignored")

        return result
