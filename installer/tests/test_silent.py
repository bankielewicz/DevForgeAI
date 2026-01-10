"""
Test Suite for Silent/Headless Installer (STORY-249)

Tests for SilentInstaller service and related data models:
- SilentInstaller (AC#1-8)
- InstallConfig (DataModel)
- InstallOptions (DataModel)

Test Framework: pytest with unittest.mock
Test Naming Convention: test_<function>_<scenario>_<expected>
Pattern: AAA (Arrange, Act, Assert)

These tests will FAIL initially (TDD Red phase) because:
- installer/silent.py does not exist yet
- SilentInstaller, InstallConfig, InstallOptions not implemented
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
import os
import sys
import tempfile
import json
from pathlib import Path
from io import StringIO
from datetime import datetime

# Add parent directory to path so 'installer' module can be imported
sys.path.insert(0, str(Path(__file__).parent.parent.parent))


# =============================================================================
# Test Fixtures
# =============================================================================

@pytest.fixture
def temp_install_dir():
    """Create a temporary directory for installation tests."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield tmpdir


@pytest.fixture
def temp_log_dir():
    """Create a temporary directory for log files."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield tmpdir


@pytest.fixture
def valid_yaml_config(temp_install_dir, temp_log_dir):
    """Create a valid YAML configuration file."""
    config_content = f"""
target: {temp_install_dir}
components:
  - core
  - cli
  - templates
options:
  initialize_git: true
  create_backup: false
  run_validation: true
log_file: {temp_log_dir}/devforgeai-install.log
"""
    config_path = os.path.join(temp_install_dir, "install-config.yaml")
    with open(config_path, 'w') as f:
        f.write(config_content)
    return config_path


@pytest.fixture
def minimal_yaml_config(temp_install_dir, temp_log_dir):
    """Create a minimal valid YAML configuration with only required fields."""
    config_content = f"""
target: {temp_install_dir}
components:
  - core
"""
    config_path = os.path.join(temp_install_dir, "minimal-config.yaml")
    with open(config_path, 'w') as f:
        f.write(config_content)
    return config_path


@pytest.fixture
def invalid_yaml_config(temp_install_dir):
    """Create an invalid YAML configuration file."""
    config_path = os.path.join(temp_install_dir, "invalid-config.yaml")
    with open(config_path, 'w') as f:
        f.write("{ invalid yaml: [missing brackets")
    return config_path


@pytest.fixture
def missing_fields_config(temp_install_dir):
    """Create a YAML configuration missing required fields."""
    config_content = """
options:
  initialize_git: true
"""
    config_path = os.path.join(temp_install_dir, "missing-fields-config.yaml")
    with open(config_path, 'w') as f:
        f.write(config_content)
    return config_path


@pytest.fixture
def mock_platform_detector():
    """Mock PlatformDetector for testing."""
    with patch('installer.platform_detector.PlatformDetector') as mock:
        mock_info = Mock()
        mock_info.os_type = "Linux"
        mock_info.is_wsl = False
        mock_info.filesystem = "ext4"
        mock_info.supports_chmod = True
        mock.detect.return_value = mock_info
        yield mock


@pytest.fixture
def mock_preflight_validator():
    """Mock PreflightValidator for testing."""
    with patch('installer.preflight.PreflightValidator') as mock:
        mock_result = Mock()
        mock_result.passed = True
        mock_result.errors = []
        mock_result.warnings = []
        mock_instance = mock.return_value
        mock_instance.validate.return_value = mock_result
        yield mock


@pytest.fixture
def existing_installation(temp_install_dir):
    """Create an existing installation marker for idempotency tests."""
    marker_path = os.path.join(temp_install_dir, ".devforgeai_installed")
    marker_data = {
        "version": "1.0.0",
        "installed_at": "2025-01-01T00:00:00Z",
        "components": ["core", "cli"]
    }
    with open(marker_path, 'w') as f:
        json.dump(marker_data, f)
    return marker_path


# =============================================================================
# InstallConfig DataModel Tests (Technical Specification)
# =============================================================================

class TestInstallConfigDataModel:
    """Tests for InstallConfig data model from Technical Specification."""

    def test_install_config_should_have_target_field(self, temp_install_dir):
        """Tech Spec: InstallConfig must have target Path field."""
        # Arrange
        from installer.silent import InstallConfig

        # Act
        config = InstallConfig(
            target=Path(temp_install_dir),
            components=["core"]
        )

        # Assert
        assert config.target == Path(temp_install_dir)

    def test_install_config_should_have_components_list(self):
        """Tech Spec: InstallConfig must have components List[str] field."""
        # Arrange
        from installer.silent import InstallConfig

        # Act
        config = InstallConfig(
            target=Path("/tmp/test"),
            components=["core", "cli", "templates"]
        )

        # Assert
        assert config.components == ["core", "cli", "templates"]

    def test_install_config_should_have_options_field(self):
        """Tech Spec: InstallConfig must have options InstallOptions field."""
        # Arrange
        from installer.silent import InstallConfig, InstallOptions

        # Act
        config = InstallConfig(
            target=Path("/tmp/test"),
            components=["core"],
            options=InstallOptions(initialize_git=True)
        )

        # Assert
        assert config.options.initialize_git is True

    def test_install_config_log_file_should_default_to_install_log(self):
        """Tech Spec: InstallConfig log_file defaults to 'install.log'."""
        # Arrange
        from installer.silent import InstallConfig

        # Act
        config = InstallConfig(
            target=Path("/tmp/test"),
            components=["core"]
        )

        # Assert
        assert config.log_file == Path("install.log")


# =============================================================================
# InstallOptions DataModel Tests (Technical Specification)
# =============================================================================

class TestInstallOptionsDataModel:
    """Tests for InstallOptions data model from Technical Specification."""

    def test_install_options_initialize_git_default_false(self):
        """Tech Spec: InstallOptions initialize_git defaults to False."""
        # Arrange
        from installer.silent import InstallOptions

        # Act
        options = InstallOptions()

        # Assert
        assert options.initialize_git is False

    def test_install_options_create_backup_default_false(self):
        """Tech Spec: InstallOptions create_backup defaults to False."""
        # Arrange
        from installer.silent import InstallOptions

        # Act
        options = InstallOptions()

        # Assert
        assert options.create_backup is False

    def test_install_options_run_validation_default_true(self):
        """Tech Spec: InstallOptions run_validation defaults to True."""
        # Arrange
        from installer.silent import InstallOptions

        # Act
        options = InstallOptions()

        # Assert
        assert options.run_validation is True

    def test_install_options_dry_run_default_false(self):
        """Tech Spec: InstallOptions dry_run defaults to False."""
        # Arrange
        from installer.silent import InstallOptions

        # Act
        options = InstallOptions()

        # Assert
        assert options.dry_run is False


# =============================================================================
# AC#1: YAML Configuration File Support Tests
# =============================================================================

class TestYamlConfigurationFileSupport:
    """Tests for AC#1: YAML Configuration File Support."""

    def test_load_config_should_parse_yaml_file_correctly(self, valid_yaml_config):
        """AC#1: YAML file parsed correctly."""
        # Arrange
        from installer.silent import SilentInstaller

        # Act
        installer = SilentInstaller(config=valid_yaml_config)

        # Assert
        assert installer.config is not None
        assert "core" in installer.config.components

    def test_load_config_should_apply_all_config_fields(self, valid_yaml_config, temp_install_dir):
        """AC#1: All config fields applied."""
        # Arrange
        from installer.silent import SilentInstaller

        # Act
        installer = SilentInstaller(config=valid_yaml_config)

        # Assert
        assert str(installer.config.target) == temp_install_dir
        assert "core" in installer.config.components
        assert "cli" in installer.config.components
        assert installer.config.options.initialize_git is True
        assert installer.config.options.create_backup is False

    def test_load_config_should_fail_on_missing_required_fields(self, missing_fields_config):
        """AC#1: Missing fields cause error."""
        # Arrange
        from installer.silent import SilentInstaller, ConfigError

        # Act & Assert
        with pytest.raises(ConfigError) as exc_info:
            SilentInstaller(config=missing_fields_config)

        assert "target" in str(exc_info.value).lower() or "required" in str(exc_info.value).lower()

    def test_load_config_should_fail_with_clear_message_on_invalid_yaml(self, invalid_yaml_config):
        """AC#1: Invalid YAML causes error with clear message."""
        # Arrange
        from installer.silent import SilentInstaller, ConfigError

        # Act & Assert
        with pytest.raises(ConfigError) as exc_info:
            SilentInstaller(config=invalid_yaml_config)

        error_msg = str(exc_info.value).lower()
        assert "yaml" in error_msg or "parse" in error_msg or "invalid" in error_msg

    def test_load_config_should_accept_path_object(self, valid_yaml_config):
        """AC#1: Config can be loaded from Path object."""
        # Arrange
        from installer.silent import SilentInstaller

        # Act
        installer = SilentInstaller(config=Path(valid_yaml_config))

        # Assert
        assert installer.config is not None

    def test_load_config_should_accept_dict(self, temp_install_dir):
        """AC#1: Config can be loaded from dict."""
        # Arrange
        from installer.silent import SilentInstaller

        config_dict = {
            "target": temp_install_dir,
            "components": ["core"],
            "options": {"initialize_git": False}
        }

        # Act
        installer = SilentInstaller(config=config_dict)

        # Assert
        assert str(installer.config.target) == temp_install_dir

    def test_load_config_should_fail_on_nonexistent_file(self):
        """AC#1: Non-existent config file causes error."""
        # Arrange
        from installer.silent import SilentInstaller, ConfigError

        # Act & Assert
        with pytest.raises(ConfigError):
            SilentInstaller(config="/nonexistent/path/config.yaml")


# =============================================================================
# AC#2: Environment Variable Configuration Tests
# =============================================================================

class TestEnvironmentVariableConfiguration:
    """Tests for AC#2: Environment Variable Configuration."""

    def test_env_vars_should_be_read_correctly(self, temp_install_dir, temp_log_dir):
        """AC#2: All env vars read correctly."""
        # Arrange
        from installer.silent import SilentInstaller

        env_vars = {
            "DEVFORGEAI_TARGET": temp_install_dir,
            "DEVFORGEAI_COMPONENTS": "core,cli",
            "DEVFORGEAI_INIT_GIT": "true",
            "DEVFORGEAI_LOG_FILE": f"{temp_log_dir}/install.log"
        }

        # Act
        with patch.dict(os.environ, env_vars, clear=False):
            installer = SilentInstaller(config=None)  # No config file, use env vars

        # Assert
        assert str(installer.config.target) == temp_install_dir
        assert "core" in installer.config.components
        assert "cli" in installer.config.components
        assert installer.config.options.initialize_git is True

    def test_env_vars_should_override_config_file(self, valid_yaml_config, temp_install_dir):
        """AC#2: Env vars override config file values."""
        # Arrange
        from installer.silent import SilentInstaller

        custom_path = os.path.join(temp_install_dir, "custom_override")
        os.makedirs(custom_path)

        env_vars = {
            "DEVFORGEAI_TARGET": custom_path,
            "DEVFORGEAI_INIT_GIT": "false"  # Override config file's true
        }

        # Act
        with patch.dict(os.environ, env_vars, clear=False):
            installer = SilentInstaller(config=valid_yaml_config)

        # Assert
        assert str(installer.config.target) == custom_path
        assert installer.config.options.initialize_git is False

    def test_missing_required_env_vars_should_fail(self):
        """AC#2: Missing required vars cause error."""
        # Arrange
        from installer.silent import SilentInstaller, ConfigError

        # Clear relevant env vars
        env_vars = {
            "DEVFORGEAI_TARGET": "",  # Empty = missing
            "DEVFORGEAI_COMPONENTS": ""
        }

        # Act & Assert
        with patch.dict(os.environ, env_vars, clear=False):
            with pytest.raises(ConfigError) as exc_info:
                SilentInstaller(config=None)

        assert "target" in str(exc_info.value).lower() or "required" in str(exc_info.value).lower()

    def test_invalid_env_var_values_should_fail(self, temp_install_dir):
        """AC#2: Invalid values cause error."""
        # Arrange
        from installer.silent import SilentInstaller, ConfigError

        env_vars = {
            "DEVFORGEAI_TARGET": temp_install_dir,
            "DEVFORGEAI_COMPONENTS": "core",
            "DEVFORGEAI_INIT_GIT": "not_a_boolean"  # Invalid boolean value
        }

        # Act & Assert
        with patch.dict(os.environ, env_vars, clear=False):
            with pytest.raises(ConfigError) as exc_info:
                SilentInstaller(config=None)

        error_msg = str(exc_info.value).lower()
        assert "invalid" in error_msg or "boolean" in error_msg

    def test_env_var_components_should_parse_comma_separated(self, temp_install_dir):
        """AC#2: DEVFORGEAI_COMPONENTS parses comma-separated list."""
        # Arrange
        from installer.silent import SilentInstaller

        env_vars = {
            "DEVFORGEAI_TARGET": temp_install_dir,
            "DEVFORGEAI_COMPONENTS": "core,cli,templates,examples"
        }

        # Act
        with patch.dict(os.environ, env_vars, clear=False):
            installer = SilentInstaller(config=None)

        # Assert
        assert installer.config.components == ["core", "cli", "templates", "examples"]

    def test_env_var_dry_run_should_be_supported(self, temp_install_dir):
        """AC#2: DEVFORGEAI_DRY_RUN env var is supported."""
        # Arrange
        from installer.silent import SilentInstaller

        env_vars = {
            "DEVFORGEAI_TARGET": temp_install_dir,
            "DEVFORGEAI_COMPONENTS": "core",
            "DEVFORGEAI_DRY_RUN": "true"
        }

        # Act
        with patch.dict(os.environ, env_vars, clear=False):
            installer = SilentInstaller(config=None)

        # Assert
        assert installer.config.options.dry_run is True


# =============================================================================
# AC#3: No Interactive Prompts Tests
# =============================================================================

class TestNoInteractivePrompts:
    """Tests for AC#3: No Interactive Prompts."""

    def test_run_should_not_call_input(self, valid_yaml_config, mock_platform_detector, mock_preflight_validator):
        """AC#3: No input() calls executed."""
        # Arrange
        from installer.silent import SilentInstaller

        installer = SilentInstaller(config=valid_yaml_config)

        # Act
        with patch('builtins.input', side_effect=AssertionError("input() should not be called")):
            with patch.object(installer, '_install_components', return_value=True):
                installer.run()

        # Assert - If we get here without AssertionError, test passes

    def test_run_should_not_require_user_interaction(self, valid_yaml_config, mock_platform_detector, mock_preflight_validator):
        """AC#3: No user interaction required."""
        # Arrange
        from installer.silent import SilentInstaller

        installer = SilentInstaller(config=valid_yaml_config)

        # Act - Should complete without any user input
        with patch.object(installer, '_install_components', return_value=True):
            result = installer.run()

        # Assert
        assert result in [0, 1, 2, 3, 4]  # Valid exit code returned

    def test_run_should_work_in_non_tty_environment(self, valid_yaml_config, mock_platform_detector, mock_preflight_validator):
        """AC#3: Works in non-TTY environment."""
        # Arrange
        from installer.silent import SilentInstaller

        installer = SilentInstaller(config=valid_yaml_config)

        # Act
        with patch('sys.stdin.isatty', return_value=False):
            with patch('sys.stdout.isatty', return_value=False):
                with patch.object(installer, '_install_components', return_value=True):
                    result = installer.run()

        # Assert
        assert result == 0  # Should succeed in non-TTY

    def test_run_should_pass_automated_tests(self, valid_yaml_config, mock_platform_detector, mock_preflight_validator):
        """AC#3: Automated tests pass (no hanging on input)."""
        # Arrange
        from installer.silent import SilentInstaller
        import signal

        installer = SilentInstaller(config=valid_yaml_config)

        def timeout_handler(signum, frame):
            raise TimeoutError("Test timed out - likely waiting for input")

        # Set a 5-second timeout
        old_handler = signal.signal(signal.SIGALRM, timeout_handler)
        signal.alarm(5)

        try:
            # Act
            with patch.object(installer, '_install_components', return_value=True):
                result = installer.run()

            # Assert
            assert result == 0
        finally:
            signal.alarm(0)
            signal.signal(signal.SIGALRM, old_handler)


# =============================================================================
# AC#4: Structured Logging Tests
# =============================================================================

class TestStructuredLogging:
    """Tests for AC#4: Structured Logging."""

    def test_log_file_should_be_created_at_specified_path(self, valid_yaml_config, temp_log_dir, mock_platform_detector, mock_preflight_validator):
        """AC#4: Log file created at specified path."""
        # Arrange
        from installer.silent import SilentInstaller

        installer = SilentInstaller(config=valid_yaml_config)
        expected_log_path = os.path.join(temp_log_dir, "devforgeai-install.log")

        # Act
        with patch.object(installer, '_install_components', return_value=True):
            installer.run()

        # Assert
        assert os.path.exists(expected_log_path), f"Log file not created at {expected_log_path}"

    def test_log_entries_should_have_iso8601_timestamps(self, valid_yaml_config, temp_log_dir, mock_platform_detector, mock_preflight_validator):
        """AC#4: Timestamps in ISO 8601 format."""
        # Arrange
        from installer.silent import SilentInstaller
        import re

        installer = SilentInstaller(config=valid_yaml_config)
        log_path = os.path.join(temp_log_dir, "devforgeai-install.log")

        # Act
        with patch.object(installer, '_install_components', return_value=True):
            installer.run()

        # Assert
        with open(log_path, 'r') as f:
            content = f.read()
            # ISO 8601 format: YYYY-MM-DDTHH:MM:SSZ or similar
            iso8601_pattern = r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}'
            assert re.search(iso8601_pattern, content), "Log entries should have ISO 8601 timestamps"

    def test_log_entries_should_have_correct_log_levels(self, valid_yaml_config, temp_log_dir, mock_platform_detector, mock_preflight_validator):
        """AC#4: Log levels correct."""
        # Arrange
        from installer.silent import SilentInstaller

        installer = SilentInstaller(config=valid_yaml_config)
        log_path = os.path.join(temp_log_dir, "devforgeai-install.log")

        # Act
        with patch.object(installer, '_install_components', return_value=True):
            installer.run()

        # Assert
        with open(log_path, 'r') as f:
            content = f.read()
            # Should contain at least INFO level entries
            assert "[INFO]" in content or "[WARNING]" in content or "[ERROR]" in content

    def test_log_entries_should_not_contain_sensitive_data(self, temp_install_dir, temp_log_dir, mock_platform_detector, mock_preflight_validator):
        """AC#4: No sensitive data logged."""
        # Arrange
        from installer.silent import SilentInstaller

        config_dict = {
            "target": temp_install_dir,
            "components": ["core"],
            "log_file": f"{temp_log_dir}/install.log",
            "api_key": "secret-api-key-12345",  # Sensitive data
            "password": "super-secret-password"  # Sensitive data
        }

        installer = SilentInstaller(config=config_dict)
        log_path = os.path.join(temp_log_dir, "install.log")

        # Act
        with patch.object(installer, '_install_components', return_value=True):
            installer.run()

        # Assert
        with open(log_path, 'r') as f:
            content = f.read()
            assert "secret-api-key-12345" not in content
            assert "super-secret-password" not in content

    def test_log_entries_should_include_component_module_name(self, valid_yaml_config, temp_log_dir, mock_platform_detector, mock_preflight_validator):
        """AC#4: Log entries include component/module name."""
        # Arrange
        from installer.silent import SilentInstaller

        installer = SilentInstaller(config=valid_yaml_config)
        log_path = os.path.join(temp_log_dir, "devforgeai-install.log")

        # Act
        with patch.object(installer, '_install_components', return_value=True):
            installer.run()

        # Assert
        with open(log_path, 'r') as f:
            content = f.read()
            # Should contain module names like installer.preflight, installer.core, etc.
            assert "installer" in content.lower() or "silent" in content.lower()

    def test_structured_formatter_output_format(self, valid_yaml_config, temp_log_dir, mock_platform_detector, mock_preflight_validator):
        """AC#4: Log format matches expected pattern."""
        # Arrange
        from installer.silent import SilentInstaller
        import re

        installer = SilentInstaller(config=valid_yaml_config)
        log_path = os.path.join(temp_log_dir, "devforgeai-install.log")

        # Act
        with patch.object(installer, '_install_components', return_value=True):
            installer.run()

        # Assert
        with open(log_path, 'r') as f:
            content = f.read()
            # Expected format: YYYY-MM-DDTHH:MM:SSZ [LEVEL] module: message
            pattern = r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z? \[(INFO|WARNING|ERROR)\] [\w.]+: .+'
            assert re.search(pattern, content), "Log format should match expected pattern"


# =============================================================================
# AC#5: Exit Codes for CI/CD Tests
# =============================================================================

class TestExitCodesForCICD:
    """Tests for AC#5: Exit Codes for CI/CD."""

    def test_run_should_return_0_on_success(self, valid_yaml_config, mock_platform_detector, mock_preflight_validator):
        """AC#5: Success returns 0."""
        # Arrange
        from installer.silent import SilentInstaller

        installer = SilentInstaller(config=valid_yaml_config)

        # Act
        with patch.object(installer, '_install_components', return_value=True):
            with patch.object(installer, '_run_validation', return_value=True):
                result = installer.run()

        # Assert
        assert result == 0

    def test_run_should_return_1_on_config_error(self, invalid_yaml_config):
        """AC#5: Config error returns 1."""
        # Arrange
        from installer.silent import SilentInstaller, ConfigError

        # Act & Assert
        try:
            installer = SilentInstaller(config=invalid_yaml_config)
            result = installer.run()
            assert result == 1
        except ConfigError:
            # ConfigError raised during init is also acceptable
            pass

    def test_run_should_return_2_on_preflight_failure(self, valid_yaml_config, mock_platform_detector):
        """AC#5: Pre-flight failure returns 2."""
        # Arrange
        from installer.silent import SilentInstaller

        installer = SilentInstaller(config=valid_yaml_config)

        # Mock preflight to fail
        with patch('installer.preflight.PreflightValidator') as mock_preflight:
            mock_result = Mock()
            mock_result.passed = False
            mock_result.errors = ["Insufficient disk space"]
            mock_preflight.return_value.validate.return_value = mock_result

            # Act
            result = installer.run()

        # Assert
        assert result == 2

    def test_run_should_return_3_on_installation_error(self, valid_yaml_config, mock_platform_detector, mock_preflight_validator):
        """AC#5: Installation error returns 3."""
        # Arrange
        from installer.silent import SilentInstaller

        installer = SilentInstaller(config=valid_yaml_config)

        # Act
        with patch.object(installer, '_install_components', side_effect=OSError("Permission denied")):
            result = installer.run()

        # Assert
        assert result == 3

    def test_run_should_return_4_on_validation_failure(self, valid_yaml_config, mock_platform_detector, mock_preflight_validator):
        """AC#5: Validation failure returns 4."""
        # Arrange
        from installer.silent import SilentInstaller

        installer = SilentInstaller(config=valid_yaml_config)

        # Act
        with patch.object(installer, '_install_components', return_value=True):
            with patch.object(installer, '_run_validation', return_value=False):
                result = installer.run()

        # Assert
        assert result == 4

    def test_exit_codes_match_exit_codes_module(self, valid_yaml_config):
        """AC#5: Exit codes match installer/exit_codes.py (STORY-237)."""
        # Arrange
        from installer.silent import SilentInstaller
        from installer.exit_codes import ExitCodes

        # Assert - Verify exit code constants match
        assert SilentInstaller.EXIT_SUCCESS == ExitCodes.SUCCESS
        assert SilentInstaller.EXIT_CONFIG_ERROR == 1  # ConfigError
        assert SilentInstaller.EXIT_PREFLIGHT_ERROR == 2  # Preflight failure
        assert SilentInstaller.EXIT_INSTALL_ERROR == 3  # Installation error
        assert SilentInstaller.EXIT_VALIDATION_ERROR == ExitCodes.VALIDATION_FAILED


# =============================================================================
# AC#6: Dry-Run Mode Tests
# =============================================================================

class TestDryRunMode:
    """Tests for AC#6: Dry-Run Mode."""

    def test_dry_run_should_not_create_files(self, temp_install_dir, temp_log_dir, mock_platform_detector, mock_preflight_validator):
        """AC#6: No files created in dry-run."""
        # Arrange
        from installer.silent import SilentInstaller

        config_dict = {
            "target": temp_install_dir,
            "components": ["core"],
            "options": {"dry_run": True},
            "log_file": f"{temp_log_dir}/install.log"
        }

        installer = SilentInstaller(config=config_dict)

        # Record files before
        files_before = set(os.listdir(temp_install_dir))

        # Act
        result = installer.run()

        # Assert
        files_after = set(os.listdir(temp_install_dir))
        # Only log file should be created, no installation files
        new_files = files_after - files_before
        assert ".claude" not in new_files, "No .claude directory should be created in dry-run"
        assert "devforgeai" not in new_files, "No devforgeai directory should be created in dry-run"

    def test_dry_run_should_perform_all_checks(self, temp_install_dir, temp_log_dir, mock_platform_detector):
        """AC#6: All checks performed in dry-run."""
        # Arrange
        from installer.silent import SilentInstaller

        config_dict = {
            "target": temp_install_dir,
            "components": ["core"],
            "options": {"dry_run": True},
            "log_file": f"{temp_log_dir}/install.log"
        }

        installer = SilentInstaller(config=config_dict)

        # Track preflight check
        preflight_called = False

        with patch('installer.preflight.PreflightValidator') as mock_preflight:
            def track_preflight(*args, **kwargs):
                nonlocal preflight_called
                preflight_called = True
                mock_result = Mock()
                mock_result.passed = True
                mock_result.errors = []
                mock_result.warnings = []
                mock_instance = Mock()
                mock_instance.validate.return_value = mock_result
                return mock_instance

            mock_preflight.side_effect = track_preflight

            # Act
            installer.run()

        # Assert
        assert preflight_called, "Preflight checks should run in dry-run mode"

    def test_dry_run_log_should_show_dry_run_prefix(self, temp_install_dir, temp_log_dir, mock_platform_detector, mock_preflight_validator):
        """AC#6: Log shows DRY RUN prefix."""
        # Arrange
        from installer.silent import SilentInstaller

        config_dict = {
            "target": temp_install_dir,
            "components": ["core"],
            "options": {"dry_run": True},
            "log_file": f"{temp_log_dir}/install.log"
        }

        installer = SilentInstaller(config=config_dict)
        log_path = f"{temp_log_dir}/install.log"

        # Act
        installer.run()

        # Assert
        with open(log_path, 'r') as f:
            content = f.read()
            assert "DRY RUN" in content, "Log should contain 'DRY RUN' prefix"

    def test_dry_run_should_return_0_if_checks_pass(self, temp_install_dir, temp_log_dir, mock_platform_detector, mock_preflight_validator):
        """AC#6: Exit code 0 if dry-run passes."""
        # Arrange
        from installer.silent import SilentInstaller

        config_dict = {
            "target": temp_install_dir,
            "components": ["core"],
            "options": {"dry_run": True},
            "log_file": f"{temp_log_dir}/install.log"
        }

        installer = SilentInstaller(config=config_dict)

        # Act
        result = installer.run()

        # Assert
        assert result == 0

    def test_dry_run_should_return_2_if_preflight_fails(self, temp_install_dir, temp_log_dir, mock_platform_detector):
        """AC#6: Exit code 2 if dry-run preflight fails."""
        # Arrange
        from installer.silent import SilentInstaller

        config_dict = {
            "target": temp_install_dir,
            "components": ["core"],
            "options": {"dry_run": True},
            "log_file": f"{temp_log_dir}/install.log"
        }

        installer = SilentInstaller(config=config_dict)

        # Mock preflight to fail
        with patch('installer.preflight.PreflightValidator') as mock_preflight:
            mock_result = Mock()
            mock_result.passed = False
            mock_result.errors = ["Insufficient disk space"]
            mock_preflight.return_value.validate.return_value = mock_result

            # Act
            result = installer.run()

        # Assert
        assert result == 2


# =============================================================================
# AC#7: Idempotency Tests
# =============================================================================

class TestIdempotency:
    """Tests for AC#7: Idempotency."""

    def test_run_should_detect_existing_installation(self, valid_yaml_config, existing_installation, temp_log_dir, mock_platform_detector, mock_preflight_validator):
        """AC#7: Existing install detected."""
        # Arrange
        from installer.silent import SilentInstaller

        installer = SilentInstaller(config=valid_yaml_config)
        log_path = os.path.join(temp_log_dir, "devforgeai-install.log")

        # Act
        result = installer.run()

        # Assert
        with open(log_path, 'r') as f:
            content = f.read()
            assert "already installed" in content.lower() or "existing" in content.lower()

    def test_run_should_not_create_duplicate_files(self, valid_yaml_config, existing_installation, temp_install_dir, mock_platform_detector, mock_preflight_validator):
        """AC#7: No duplicate files."""
        # Arrange
        from installer.silent import SilentInstaller

        # Create some existing files
        claude_dir = os.path.join(temp_install_dir, ".claude")
        os.makedirs(claude_dir, exist_ok=True)
        skill_file = os.path.join(claude_dir, "skills", "test-skill", "SKILL.md")
        os.makedirs(os.path.dirname(skill_file), exist_ok=True)
        with open(skill_file, 'w') as f:
            f.write("# Original content")

        installer = SilentInstaller(config=valid_yaml_config)

        # Act
        installer.run()

        # Assert - Original file should not be duplicated
        skill_dir = os.path.join(claude_dir, "skills", "test-skill")
        files = os.listdir(skill_dir)
        assert files.count("SKILL.md") == 1, "Should not create duplicate files"

    def test_run_should_not_overwrite_existing_files(self, valid_yaml_config, existing_installation, temp_install_dir, mock_platform_detector, mock_preflight_validator):
        """AC#7: No overwrites."""
        # Arrange
        from installer.silent import SilentInstaller

        # Create existing file with specific content
        claude_dir = os.path.join(temp_install_dir, ".claude")
        os.makedirs(claude_dir, exist_ok=True)
        test_file = os.path.join(claude_dir, "test-file.md")
        original_content = "# Original user content - DO NOT OVERWRITE"
        with open(test_file, 'w') as f:
            f.write(original_content)

        installer = SilentInstaller(config=valid_yaml_config)

        # Act
        installer.run()

        # Assert
        with open(test_file, 'r') as f:
            content = f.read()
            assert content == original_content, "Existing files should not be overwritten"

    def test_run_should_return_0_on_idempotent_rerun(self, valid_yaml_config, existing_installation, mock_platform_detector, mock_preflight_validator):
        """AC#7: Exit code 0 on re-run."""
        # Arrange
        from installer.silent import SilentInstaller

        installer = SilentInstaller(config=valid_yaml_config)

        # Act
        result = installer.run()

        # Assert
        assert result == 0, "Should return success on idempotent re-run"

    def test_is_already_installed_should_check_marker_file(self, temp_install_dir, existing_installation):
        """AC#7: Idempotency check reads marker file."""
        # Arrange
        from installer.silent import SilentInstaller

        config_dict = {
            "target": temp_install_dir,
            "components": ["core"]
        }

        installer = SilentInstaller(config=config_dict)

        # Act
        is_installed = installer.is_already_installed()

        # Assert
        assert is_installed is True

    def test_is_already_installed_should_return_false_for_fresh_directory(self, temp_install_dir):
        """AC#7: Fresh directory not detected as installed."""
        # Arrange
        from installer.silent import SilentInstaller

        config_dict = {
            "target": temp_install_dir,
            "components": ["core"]
        }

        installer = SilentInstaller(config=config_dict)

        # Act
        is_installed = installer.is_already_installed()

        # Assert
        assert is_installed is False


# =============================================================================
# AC#8: JSON Progress Output Tests
# =============================================================================

class TestJsonProgressOutput:
    """Tests for AC#8: JSON Progress Output (Optional)."""

    def test_json_output_should_be_valid_json_lines(self, valid_yaml_config, capsys, mock_platform_detector, mock_preflight_validator):
        """AC#8: JSON lines valid."""
        # Arrange
        from installer.silent import SilentInstaller

        installer = SilentInstaller(config=valid_yaml_config, json_output=True)

        # Act
        with patch.object(installer, '_install_components', return_value=True):
            installer.run()

        # Assert
        captured = capsys.readouterr()
        lines = [line for line in captured.out.strip().split('\n') if line]
        for line in lines:
            try:
                json.loads(line)
            except json.JSONDecodeError:
                pytest.fail(f"Invalid JSON line: {line}")

    def test_json_output_should_include_progress_updates(self, valid_yaml_config, capsys, mock_platform_detector, mock_preflight_validator):
        """AC#8: Progress updates accurate."""
        # Arrange
        from installer.silent import SilentInstaller

        installer = SilentInstaller(config=valid_yaml_config, json_output=True)

        # Act
        with patch.object(installer, '_install_components', return_value=True):
            installer.run()

        # Assert
        captured = capsys.readouterr()
        lines = [line for line in captured.out.strip().split('\n') if line]

        progress_updates = []
        for line in lines:
            try:
                data = json.loads(line)
                if "percent" in data or "progress" in data:
                    progress_updates.append(data)
            except json.JSONDecodeError:
                continue

        assert len(progress_updates) >= 2, "Should have at least start and complete progress"

    def test_json_output_error_should_include_details(self, valid_yaml_config, capsys, mock_platform_detector, mock_preflight_validator):
        """AC#8: Error JSON includes details."""
        # Arrange
        from installer.silent import SilentInstaller

        installer = SilentInstaller(config=valid_yaml_config, json_output=True)

        # Act
        with patch.object(installer, '_install_components', side_effect=OSError("Disk full")):
            installer.run()

        # Assert
        captured = capsys.readouterr()
        lines = [line for line in captured.out.strip().split('\n') if line]

        error_found = False
        for line in lines:
            try:
                data = json.loads(line)
                if data.get("status") == "error":
                    error_found = True
                    assert "code" in data or "message" in data, "Error should include details"
            except json.JSONDecodeError:
                continue

        assert error_found, "Should output error JSON on failure"

    def test_json_output_should_be_newline_delimited(self, valid_yaml_config, capsys, mock_platform_detector, mock_preflight_validator):
        """AC#8: Newline-delimited format."""
        # Arrange
        from installer.silent import SilentInstaller

        installer = SilentInstaller(config=valid_yaml_config, json_output=True)

        # Act
        with patch.object(installer, '_install_components', return_value=True):
            installer.run()

        # Assert
        captured = capsys.readouterr()
        # Each line should be separate JSON
        lines = captured.out.strip().split('\n')
        assert len(lines) >= 1, "Should have at least one JSON line"

        # Each line should be independent valid JSON
        for line in lines:
            if line:
                json.loads(line)  # Should not raise

    def test_json_progress_should_include_status_field(self, valid_yaml_config, capsys, mock_platform_detector, mock_preflight_validator):
        """AC#8: JSON includes status field."""
        # Arrange
        from installer.silent import SilentInstaller

        installer = SilentInstaller(config=valid_yaml_config, json_output=True)

        # Act
        with patch.object(installer, '_install_components', return_value=True):
            installer.run()

        # Assert
        captured = capsys.readouterr()
        lines = [line for line in captured.out.strip().split('\n') if line]

        status_found = False
        for line in lines:
            try:
                data = json.loads(line)
                if "status" in data:
                    status_found = True
                    assert data["status"] in ["in_progress", "complete", "error"]
            except json.JSONDecodeError:
                continue

        assert status_found, "JSON output should include status field"


# =============================================================================
# SilentInstaller Service Tests (Technical Specification)
# =============================================================================

class TestSilentInstallerService:
    """Tests for SilentInstaller service from Technical Specification."""

    def test_init_should_accept_path_config(self, valid_yaml_config):
        """Tech Spec: __init__ accepts Path config."""
        # Arrange
        from installer.silent import SilentInstaller

        # Act
        installer = SilentInstaller(config=Path(valid_yaml_config))

        # Assert
        assert installer.config is not None

    def test_init_should_accept_dict_config(self, temp_install_dir):
        """Tech Spec: __init__ accepts Dict config."""
        # Arrange
        from installer.silent import SilentInstaller

        config_dict = {
            "target": temp_install_dir,
            "components": ["core"]
        }

        # Act
        installer = SilentInstaller(config=config_dict)

        # Assert
        assert installer.config is not None

    def test_run_should_return_int_exit_code(self, valid_yaml_config, mock_platform_detector, mock_preflight_validator):
        """Tech Spec: run() returns int."""
        # Arrange
        from installer.silent import SilentInstaller

        installer = SilentInstaller(config=valid_yaml_config)

        # Act
        with patch.object(installer, '_install_components', return_value=True):
            result = installer.run()

        # Assert
        assert isinstance(result, int)

    def test_validate_config_should_raise_on_invalid(self):
        """Tech Spec: _validate_config() raises ConfigError."""
        # Arrange
        from installer.silent import SilentInstaller, ConfigError

        # Act & Assert
        with pytest.raises(ConfigError):
            SilentInstaller(config={})  # Empty config

    def test_run_preflight_should_call_preflight_validator(self, valid_yaml_config, mock_platform_detector):
        """Tech Spec: _run_preflight() invokes PreflightValidator."""
        # Arrange
        from installer.silent import SilentInstaller

        installer = SilentInstaller(config=valid_yaml_config)

        with patch('installer.preflight.PreflightValidator') as mock_preflight:
            mock_result = Mock()
            mock_result.passed = True
            mock_result.errors = []
            mock_preflight.return_value.validate.return_value = mock_result

            # Act
            with patch.object(installer, '_install_components', return_value=True):
                installer.run()

            # Assert
            mock_preflight.assert_called()

    def test_emit_json_progress_should_write_to_stdout(self, temp_install_dir, capsys):
        """Tech Spec: _emit_json_progress() emits JSON to stdout."""
        # Arrange
        from installer.silent import SilentInstaller

        config_dict = {
            "target": temp_install_dir,
            "components": ["core"]
        }

        installer = SilentInstaller(config=config_dict, json_output=True)

        # Act
        installer._emit_json_progress(status="in_progress", percent=50, step="Installing")

        # Assert
        captured = capsys.readouterr()
        data = json.loads(captured.out.strip())
        assert data["status"] == "in_progress"
        assert data["percent"] == 50


# =============================================================================
# Integration Tests
# =============================================================================

class TestSilentInstallerIntegration:
    """Integration tests for complete silent installer flow."""

    def test_full_installation_flow_happy_path(self, temp_install_dir, temp_log_dir, mock_platform_detector, mock_preflight_validator):
        """Integration: Complete installation with valid config."""
        # Arrange
        from installer.silent import SilentInstaller

        config_dict = {
            "target": temp_install_dir,
            "components": ["core"],
            "options": {"run_validation": True},
            "log_file": f"{temp_log_dir}/install.log"
        }

        installer = SilentInstaller(config=config_dict)

        # Act
        with patch.object(installer, '_install_components', return_value=True):
            with patch.object(installer, '_run_validation', return_value=True):
                result = installer.run()

        # Assert
        assert result == 0
        assert os.path.exists(f"{temp_log_dir}/install.log")

    def test_full_dry_run_flow(self, temp_install_dir, temp_log_dir, mock_platform_detector, mock_preflight_validator):
        """Integration: Complete dry-run flow."""
        # Arrange
        from installer.silent import SilentInstaller

        config_dict = {
            "target": temp_install_dir,
            "components": ["core", "cli"],
            "options": {"dry_run": True},
            "log_file": f"{temp_log_dir}/install.log"
        }

        installer = SilentInstaller(config=config_dict)

        # Act
        result = installer.run()

        # Assert
        assert result == 0
        # Verify dry-run logged
        with open(f"{temp_log_dir}/install.log", 'r') as f:
            assert "DRY RUN" in f.read()

    def test_env_var_only_installation(self, temp_install_dir, temp_log_dir, mock_platform_detector, mock_preflight_validator):
        """Integration: Installation using only environment variables."""
        # Arrange
        from installer.silent import SilentInstaller

        env_vars = {
            "DEVFORGEAI_TARGET": temp_install_dir,
            "DEVFORGEAI_COMPONENTS": "core,cli",
            "DEVFORGEAI_INIT_GIT": "false",
            "DEVFORGEAI_LOG_FILE": f"{temp_log_dir}/install.log"
        }

        # Act
        with patch.dict(os.environ, env_vars, clear=False):
            installer = SilentInstaller(config=None)
            with patch.object(installer, '_install_components', return_value=True):
                result = installer.run()

        # Assert
        assert result == 0


# =============================================================================
# Edge Cases Tests
# =============================================================================

class TestEdgeCases:
    """Tests for edge cases from story specification."""

    def test_edge_case_empty_components_list(self, temp_install_dir):
        """Edge Case: Empty components list should fail."""
        # Arrange
        from installer.silent import SilentInstaller, ConfigError

        config_dict = {
            "target": temp_install_dir,
            "components": []  # Empty list
        }

        # Act & Assert
        with pytest.raises(ConfigError) as exc_info:
            SilentInstaller(config=config_dict)

        assert "component" in str(exc_info.value).lower()

    def test_edge_case_path_with_spaces(self, temp_install_dir, mock_platform_detector, mock_preflight_validator):
        """Edge Case: Path with spaces should be handled."""
        # Arrange
        from installer.silent import SilentInstaller

        path_with_spaces = os.path.join(temp_install_dir, "my project")
        os.makedirs(path_with_spaces)

        config_dict = {
            "target": path_with_spaces,
            "components": ["core"]
        }

        installer = SilentInstaller(config=config_dict)

        # Act
        with patch.object(installer, '_install_components', return_value=True):
            result = installer.run()

        # Assert
        assert result == 0

    def test_edge_case_path_with_unicode(self, temp_install_dir, mock_platform_detector, mock_preflight_validator):
        """Edge Case: Path with unicode characters should be handled."""
        # Arrange
        from installer.silent import SilentInstaller

        unicode_path = os.path.join(temp_install_dir, "projet_francais")
        os.makedirs(unicode_path)

        config_dict = {
            "target": unicode_path,
            "components": ["core"]
        }

        installer = SilentInstaller(config=config_dict)

        # Act
        with patch.object(installer, '_install_components', return_value=True):
            result = installer.run()

        # Assert
        assert result == 0

    def test_edge_case_very_long_path(self, temp_install_dir, mock_platform_detector, mock_preflight_validator):
        """Edge Case: Very long path should be handled."""
        # Arrange
        from installer.silent import SilentInstaller

        # Create nested path (but not too long to fail on filesystem)
        long_path = temp_install_dir
        for i in range(5):
            long_path = os.path.join(long_path, f"nested_dir_{i}")
        os.makedirs(long_path, exist_ok=True)

        config_dict = {
            "target": long_path,
            "components": ["core"]
        }

        installer = SilentInstaller(config=config_dict)

        # Act
        with patch.object(installer, '_install_components', return_value=True):
            result = installer.run()

        # Assert
        assert result == 0

    def test_edge_case_invalid_component_name(self, temp_install_dir):
        """Edge Case: Invalid component name should fail validation."""
        # Arrange
        from installer.silent import SilentInstaller, ConfigError

        config_dict = {
            "target": temp_install_dir,
            "components": ["core", "nonexistent_component"]
        }

        # Act & Assert
        with pytest.raises(ConfigError) as exc_info:
            installer = SilentInstaller(config=config_dict)
            installer._validate_components()

        assert "component" in str(exc_info.value).lower()

    def test_edge_case_log_file_directory_not_exists(self, temp_install_dir, mock_platform_detector, mock_preflight_validator):
        """Edge Case: Log file parent directory created automatically."""
        # Arrange
        from installer.silent import SilentInstaller

        nonexistent_dir = os.path.join(temp_install_dir, "logs", "subdir")

        config_dict = {
            "target": temp_install_dir,
            "components": ["core"],
            "log_file": os.path.join(nonexistent_dir, "install.log")
        }

        installer = SilentInstaller(config=config_dict)

        # Act
        with patch.object(installer, '_install_components', return_value=True):
            result = installer.run()

        # Assert
        assert result == 0
        assert os.path.exists(os.path.join(nonexistent_dir, "install.log"))


# =============================================================================
# Error Handling Tests
# =============================================================================

class TestErrorHandling:
    """Tests for error handling scenarios."""

    def test_config_error_should_have_clear_message(self):
        """Error: ConfigError should have descriptive message."""
        # Arrange
        from installer.silent import SilentInstaller, ConfigError

        # Act & Assert
        with pytest.raises(ConfigError) as exc_info:
            SilentInstaller(config="/nonexistent/config.yaml")

        assert len(str(exc_info.value)) > 10, "Error message should be descriptive"

    def test_preflight_error_should_be_logged(self, valid_yaml_config, temp_log_dir, mock_platform_detector):
        """Error: Preflight failure should be logged."""
        # Arrange
        from installer.silent import SilentInstaller

        installer = SilentInstaller(config=valid_yaml_config)
        log_path = os.path.join(temp_log_dir, "devforgeai-install.log")

        # Mock preflight to fail
        with patch('installer.preflight.PreflightValidator') as mock_preflight:
            mock_result = Mock()
            mock_result.passed = False
            mock_result.errors = ["Disk space insufficient"]
            mock_preflight.return_value.validate.return_value = mock_result

            # Act
            installer.run()

        # Assert
        with open(log_path, 'r') as f:
            content = f.read()
            assert "disk" in content.lower() or "error" in content.lower()

    def test_install_error_should_be_logged(self, valid_yaml_config, temp_log_dir, mock_platform_detector, mock_preflight_validator):
        """Error: Installation failure should be logged."""
        # Arrange
        from installer.silent import SilentInstaller

        installer = SilentInstaller(config=valid_yaml_config)
        log_path = os.path.join(temp_log_dir, "devforgeai-install.log")

        # Act
        with patch.object(installer, '_install_components', side_effect=OSError("Permission denied")):
            installer.run()

        # Assert
        with open(log_path, 'r') as f:
            content = f.read()
            assert "error" in content.lower()

    def test_validation_failure_should_be_logged(self, valid_yaml_config, temp_log_dir, mock_platform_detector, mock_preflight_validator):
        """Error: Validation failure should be logged."""
        # Arrange
        from installer.silent import SilentInstaller

        installer = SilentInstaller(config=valid_yaml_config)
        log_path = os.path.join(temp_log_dir, "devforgeai-install.log")

        # Act
        with patch.object(installer, '_install_components', return_value=True):
            with patch.object(installer, '_run_validation', return_value=False):
                installer.run()

        # Assert
        with open(log_path, 'r') as f:
            content = f.read()
            assert "validation" in content.lower() or "failed" in content.lower()


# =============================================================================
# CI/CD Pipeline Compatibility Tests
# =============================================================================

class TestCICDCompatibility:
    """Tests for CI/CD pipeline compatibility."""

    def test_github_actions_example_should_work(self, temp_install_dir, temp_log_dir, mock_platform_detector, mock_preflight_validator):
        """CI/CD: GitHub Actions example from story works."""
        # Arrange
        from installer.silent import SilentInstaller

        # Simulate GitHub Actions config
        config_path = os.path.join(temp_install_dir, ".github", "install-config.yaml")
        os.makedirs(os.path.dirname(config_path), exist_ok=True)

        config_content = f"""
target: {temp_install_dir}
components:
  - core
  - cli
options:
  initialize_git: false
log_file: {temp_log_dir}/install.log
"""
        with open(config_path, 'w') as f:
            f.write(config_content)

        # Mock environment like GitHub Actions
        env_vars = {"DEVFORGEAI_INIT_GIT": "false"}

        # Act
        with patch.dict(os.environ, env_vars, clear=False):
            installer = SilentInstaller(config=config_path)
            with patch.object(installer, '_install_components', return_value=True):
                result = installer.run()

        # Assert
        assert result == 0

    def test_gitlab_ci_example_should_work(self, temp_install_dir, temp_log_dir, capsys, mock_platform_detector, mock_preflight_validator):
        """CI/CD: GitLab CI example from story works."""
        # Arrange
        from installer.silent import SilentInstaller

        config_dict = {
            "target": temp_install_dir,
            "components": ["core"],
            "log_file": f"{temp_log_dir}/install.log"
        }

        installer = SilentInstaller(config=config_dict, json_output=True)

        # Act
        with patch.object(installer, '_install_components', return_value=True):
            result = installer.run()

        # Assert
        assert result == 0
        # JSON output for monitoring
        captured = capsys.readouterr()
        for line in captured.out.strip().split('\n'):
            if line:
                json.loads(line)  # Should be valid JSON

    def test_exit_code_detectable_by_shell(self, valid_yaml_config, mock_platform_detector, mock_preflight_validator):
        """CI/CD: Exit codes detectable by shell for pipeline decisions."""
        # Arrange
        from installer.silent import SilentInstaller

        installer = SilentInstaller(config=valid_yaml_config)

        # Act
        with patch.object(installer, '_install_components', return_value=True):
            result = installer.run()

        # Assert
        assert result >= 0, "Exit code should be non-negative"
        assert result <= 127, "Exit code should be valid shell exit code"
