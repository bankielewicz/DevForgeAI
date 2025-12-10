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

        self._validate_required_keys(config, result)
        self._validate_field_types(config, result)
        self._check_unknown_keys(config, result)

        return result

    def _validate_required_keys(self, config: Dict[str, Any], result: ValidationResult) -> None:
        """Check all required keys are present."""
        for key in self.REQUIRED_KEYS:
            if key not in config:
                result.add_error(f"Missing required key: {key}")

    def _validate_field_types(self, config: Dict[str, Any], result: ValidationResult) -> None:
        """Validate types and values for present fields."""
        for key, expected_type in self.REQUIRED_KEYS.items():
            if key not in config:
                continue

            value = config[key]
            if not isinstance(value, expected_type):
                result.add_error(
                    f"Invalid type for '{key}': expected {expected_type.__name__}, "
                    f"got {type(value).__name__}"
                )
                continue

            # Delegate to specialized validators
            self._validate_field_value(key, value, result)

    def _validate_field_value(self, key: str, value: Any, result: ValidationResult) -> None:
        """Validate specific field values based on key."""
        if key == "merge_strategy":
            self._validate_merge_strategy(value, result)
        elif key == "schema_version":
            self._validate_schema_version(value, result)
        elif key == "optional_features":
            self._validate_optional_features(value, result)

    def _validate_merge_strategy(self, value: str, result: ValidationResult) -> None:
        """Validate merge_strategy is a valid enum value."""
        if value not in self.VALID_STRATEGIES:
            result.add_error(
                f"Invalid merge_strategy '{value}'. "
                f"Must be one of: {', '.join(self.VALID_STRATEGIES)}"
            )

    def _validate_schema_version(self, value: int, result: ValidationResult) -> None:
        """Validate schema_version is positive."""
        if value < 1:
            result.add_error("schema_version must be positive integer")

    def _validate_optional_features(self, value: list, result: ValidationResult) -> None:
        """Validate optional_features contains only strings."""
        for item in value:
            if not isinstance(item, str):
                result.add_error(
                    f"optional_features must contain strings, got {type(item).__name__}"
                )

    def _check_unknown_keys(self, config: Dict[str, Any], result: ValidationResult) -> None:
        """Warn about unknown configuration keys."""
        for key in config.keys():
            if key not in self.KNOWN_KEYS:
                result.add_warning(f"Unknown key '{key}' - will be ignored")
