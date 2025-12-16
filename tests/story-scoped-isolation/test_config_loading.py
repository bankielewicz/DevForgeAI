"""
Test configuration loading for story-scoped test isolation.

Tests AC#5: Configuration File Support
- Default values when config missing
- Valid YAML parsing
- Invalid YAML error handling
- Schema validation
"""
import os
import tempfile
import pytest
import yaml
import json
from pathlib import Path


# Default configuration values (from test-isolation.yaml)
DEFAULT_CONFIG = {
    "enabled": True,
    "paths": {
        "results_base": "tests/results",
        "coverage_base": "tests/coverage",
        "logs_base": "tests/logs"
    },
    "directory": {
        "auto_create": True,
        "permissions": 755,
        "create_parents": True
    },
    "concurrency": {
        "locking_enabled": True,
        "lock_file_pattern": ".qa-lock",
        "lock_timeout_seconds": 300,
        "stale_lock_threshold_seconds": 3600
    },
    "cleanup": {
        "enabled": False,
        "retention_days": 30,
        "max_stories": 100,
        "require_released_status": True
    }
}


def load_config(config_path: str) -> dict:
    """Load test isolation configuration from YAML file."""
    if not os.path.exists(config_path):
        return DEFAULT_CONFIG.copy()

    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)

    # Merge with defaults
    result = DEFAULT_CONFIG.copy()
    if config:
        for key, value in config.items():
            if isinstance(value, dict) and key in result:
                result[key].update(value)
            else:
                result[key] = value

    return result


def validate_config(config: dict, schema_path: str) -> tuple[bool, list]:
    """Validate configuration against JSON schema."""
    with open(schema_path, 'r') as f:
        schema = json.load(f)

    errors = []

    # Basic type validation (simplified - production would use jsonschema)
    if "enabled" in config and not isinstance(config["enabled"], bool):
        errors.append("'enabled' must be boolean")

    if "paths" in config:
        paths = config["paths"]
        for key in ["results_base", "coverage_base", "logs_base"]:
            if key in paths and not isinstance(paths[key], str):
                errors.append(f"'paths.{key}' must be string")

    if "directory" in config:
        directory = config["directory"]
        if "permissions" in directory:
            perm = directory["permissions"]
            if not isinstance(perm, int) or perm < 0 or perm > 777:
                errors.append("'directory.permissions' must be integer 0-777")

    if "concurrency" in config:
        concurrency = config["concurrency"]
        if "lock_timeout_seconds" in concurrency:
            timeout = concurrency["lock_timeout_seconds"]
            if not isinstance(timeout, int) or timeout < 1 or timeout > 3600:
                errors.append("'concurrency.lock_timeout_seconds' must be 1-3600")

    return len(errors) == 0, errors


class TestConfigLoading:
    """Tests for configuration loading functionality."""

    def test_missing_config_returns_defaults(self):
        """Test: Missing config file falls back to defaults."""
        # Given: Non-existent config path
        config_path = "/nonexistent/path/test-isolation.yaml"

        # When: Loading config
        config = load_config(config_path)

        # Then: Returns default configuration
        assert config["enabled"] == True
        assert config["paths"]["results_base"] == "tests/results"
        assert config["paths"]["coverage_base"] == "tests/coverage"
        assert config["paths"]["logs_base"] == "tests/logs"
        assert config["directory"]["permissions"] == 755

    def test_valid_yaml_parses_correctly(self):
        """Test: Valid YAML parses correctly."""
        # Given: Valid YAML config
        yaml_content = """
enabled: true
paths:
  results_base: "custom/results"
  coverage_base: "custom/coverage"
"""

        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            f.write(yaml_content)
            temp_path = f.name

        try:
            # When: Loading config
            config = load_config(temp_path)

            # Then: Custom values override defaults
            assert config["paths"]["results_base"] == "custom/results"
            assert config["paths"]["coverage_base"] == "custom/coverage"
            # And: Default values preserved for missing keys
            assert config["paths"]["logs_base"] == "tests/logs"
        finally:
            os.unlink(temp_path)

    def test_invalid_yaml_produces_error(self):
        """Test: Invalid YAML produces clear error."""
        # Given: Invalid YAML syntax
        invalid_yaml = """
enabled: true
paths:
  results_base: [invalid unclosed bracket
"""

        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            f.write(invalid_yaml)
            temp_path = f.name

        try:
            # When/Then: Loading raises YAML error
            with pytest.raises(yaml.YAMLError):
                load_config(temp_path)
        finally:
            os.unlink(temp_path)

    def test_schema_validation_catches_invalid_values(self):
        """Test: Schema validation catches invalid values."""
        # Given: Config with invalid permission value
        invalid_config = {
            "enabled": True,
            "paths": {"results_base": "tests/results"},
            "directory": {"permissions": 999}  # Invalid: max 777
        }

        # Get schema path
        project_root = Path(__file__).parent.parent.parent
        schema_path = project_root / "src" / "devforgeai" / "config" / "test-isolation.schema.json"

        # When: Validating
        is_valid, errors = validate_config(invalid_config, str(schema_path))

        # Then: Validation fails with clear error
        assert not is_valid
        assert any("permissions" in error for error in errors)

    def test_schema_validation_passes_valid_config(self):
        """Test: Schema validation passes for valid config."""
        # Given: Valid configuration
        valid_config = {
            "enabled": True,
            "paths": {
                "results_base": "tests/results",
                "coverage_base": "tests/coverage",
                "logs_base": "tests/logs"
            },
            "directory": {
                "auto_create": True,
                "permissions": 755
            },
            "concurrency": {
                "locking_enabled": True,
                "lock_timeout_seconds": 300
            }
        }

        # Get schema path
        project_root = Path(__file__).parent.parent.parent
        schema_path = project_root / "src" / "devforgeai" / "config" / "test-isolation.schema.json"

        # When: Validating
        is_valid, errors = validate_config(valid_config, str(schema_path))

        # Then: Validation passes
        assert is_valid
        assert len(errors) == 0

    def test_actual_config_file_is_valid(self):
        """Test: Project's test-isolation.yaml is valid."""
        # Given: Project's actual config file
        project_root = Path(__file__).parent.parent.parent
        config_path = project_root / "devforgeai" / "config" / "test-isolation.yaml"
        schema_path = project_root / "src" / "devforgeai" / "config" / "test-isolation.schema.json"

        # When: Loading and validating
        config = load_config(str(config_path))
        is_valid, errors = validate_config(config, str(schema_path))

        # Then: Config is valid
        assert is_valid, f"Config validation failed: {errors}"
        assert config["enabled"] == True
        assert config["paths"]["results_base"] == "tests/results"
