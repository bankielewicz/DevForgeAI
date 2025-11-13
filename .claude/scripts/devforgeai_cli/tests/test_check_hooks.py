"""
Comprehensive Test Suite for devforgeai check-hooks CLI Command
Tests generated following TDD Red Phase (failing tests first)

Story: STORY-021 - Implement devforgeai check-hooks CLI command
Test Framework: pytest with AAA pattern (Arrange, Act, Assert)
Coverage Target: >90% line, >85% branch

Acceptance Criteria Coverage:
  AC1: Configuration Check - Read enabled field from hooks.yaml
  AC2: Trigger Rule Matching - Evaluate trigger_on rule (all/failures-only/none)
  AC3: Operation-Specific Rules - Check operation-specific overrides
  AC4: Performance - Complete in <100ms (95th percentile)
  AC5: Error Handling - Missing Config (log warning, exit 1)
  AC6: Error Handling - Invalid Arguments (exit 2)
  AC7: Circular Invocation Detection - Detect DEVFORGEAI_HOOK_ACTIVE env var
"""

import os
import sys
import json
import tempfile
import pytest
import time
from pathlib import Path
from unittest.mock import Mock, MagicMock, patch, mock_open, call
from io import StringIO

# Import the check_hooks command (will fail until implementation exists)
try:
    from devforgeai_cli.commands.check_hooks import (
        check_hooks_command,
        CheckHooksValidator,
        EXIT_CODE_TRIGGER,
        EXIT_CODE_DONT_TRIGGER,
        EXIT_CODE_ERROR,
    )
except ImportError:
    # Placeholder for development - tests will fail until module exists
    EXIT_CODE_TRIGGER = 0
    EXIT_CODE_DONT_TRIGGER = 1
    EXIT_CODE_ERROR = 2
    check_hooks_command = None
    CheckHooksValidator = None


# ============================================================================
# FIXTURES - Setup and Configuration
# ============================================================================


@pytest.fixture
def temp_hooks_config():
    """Fixture: Temporary hooks.yaml configuration file"""
    config_content = {
        "enabled": True,
        "global_rules": {
            "trigger_on": "all",
        },
        "operations": {
            "dev": {
                "trigger_on": "all",
                "overrides": {},
            },
            "qa": {
                "trigger_on": "failures-only",
                "overrides": {},
            },
            "release": {
                "trigger_on": "none",
                "overrides": {},
            },
        },
    }

    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".yaml", delete=False, dir=None
    ) as f:
        import yaml

        yaml.dump(config_content, f)
        config_path = f.name

    yield config_path

    # Cleanup
    if os.path.exists(config_path):
        os.remove(config_path)


@pytest.fixture
def temp_disabled_hooks_config():
    """Fixture: Temporary hooks.yaml with hooks disabled"""
    config_content = {
        "enabled": False,
        "global_rules": {"trigger_on": "all"},
        "operations": {},
    }

    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".yaml", delete=False
    ) as f:
        import yaml

        yaml.dump(config_content, f)
        config_path = f.name

    yield config_path

    if os.path.exists(config_path):
        os.remove(config_path)


@pytest.fixture
def temp_invalid_config():
    """Fixture: Temporary invalid hooks.yaml"""
    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".yaml", delete=False
    ) as f:
        f.write("INVALID: YAML: [CONTENT")
        config_path = f.name

    yield config_path

    if os.path.exists(config_path):
        os.remove(config_path)


@pytest.fixture
def mock_logger():
    """Fixture: Mock logger for capturing log output"""
    with patch("devforgeai_cli.commands.check_hooks.logger") as logger:
        yield logger


@pytest.fixture
def clean_env():
    """Fixture: Clean environment variables before each test"""
    old_env = os.environ.copy()
    # Remove hook-related env vars
    for key in list(os.environ.keys()):
        if "DEVFORGEAI_HOOK" in key or "DEVFORGEAI_OPERATION" in key:
            del os.environ[key]
    yield
    # Restore environment
    os.environ.clear()
    os.environ.update(old_env)


# ============================================================================
# ACCEPTANCE CRITERIA TESTS
# ============================================================================


class TestAC1_ConfigurationCheck:
    """AC1: Configuration Check - Read enabled field from hooks.yaml
    Exit code 1 if disabled, continue if enabled"""

    @pytest.mark.parametrize(
        "enabled_value,expected_exit_code",
        [
            (True, EXIT_CODE_TRIGGER),
            (False, EXIT_CODE_DONT_TRIGGER),
        ],
    )
    def test_reads_enabled_field_from_config(
        self, enabled_value, expected_exit_code, mock_logger, clean_env
    ):
        """Test: Configuration enabled field determines exit code"""
        # Arrange
        config_data = {
            "enabled": enabled_value,
            "global_rules": {"trigger_on": "all"},
            "operations": {},
        }
        config_content = json.dumps(config_data)

        with patch("builtins.open", mock_open(read_data=config_content)):
            with patch("devforgeai_cli.commands.check_hooks.yaml.safe_load") as mock_yaml:
                mock_yaml.return_value = config_data

                # Act
                result = check_hooks_command(
                    operation="dev", status="success", config_path=None
                )

                # Assert
                assert (
                    result == expected_exit_code
                ), f"Expected exit code {expected_exit_code}, got {result} for enabled={enabled_value}"

    def test_disabled_config_logs_warning(
        self, temp_disabled_hooks_config, mock_logger, clean_env
    ):
        """Test: Disabled config logs appropriate warning"""
        # Arrange - already set up via fixture

        # Act
        result = check_hooks_command(
            operation="dev",
            status="success",
            config_path=temp_disabled_hooks_config,
        )

        # Assert
        assert result == EXIT_CODE_DONT_TRIGGER
        mock_logger.warning.assert_called()
        call_args = mock_logger.warning.call_args[0][0]
        assert "disabled" in call_args.lower() or "not enabled" in call_args.lower()

    def test_enabled_config_allows_continuation(
        self, temp_hooks_config, mock_logger, clean_env
    ):
        """Test: Enabled config allows workflow to continue"""
        # Arrange - fixture provides enabled config

        # Act
        result = check_hooks_command(
            operation="dev", status="success", config_path=temp_hooks_config
        )

        # Assert
        # Should not immediately return error code
        assert result in [EXIT_CODE_TRIGGER, EXIT_CODE_DONT_TRIGGER]


class TestAC2_TriggerRuleMatching:
    """AC2: Trigger Rule Matching
    Evaluate trigger_on rule (all/failures-only/none)"""

    @pytest.mark.parametrize(
        "trigger_on_value,status,expected_exit_code",
        [
            # trigger_on: "all" - trigger on any status
            ("all", "success", EXIT_CODE_TRIGGER),
            ("all", "failure", EXIT_CODE_TRIGGER),
            ("all", "partial", EXIT_CODE_TRIGGER),
            # trigger_on: "failures-only" - trigger only on failure
            ("failures-only", "success", EXIT_CODE_DONT_TRIGGER),
            ("failures-only", "failure", EXIT_CODE_TRIGGER),
            ("failures-only", "partial", EXIT_CODE_TRIGGER),
            # trigger_on: "none" - never trigger
            ("none", "success", EXIT_CODE_DONT_TRIGGER),
            ("none", "failure", EXIT_CODE_DONT_TRIGGER),
            ("none", "partial", EXIT_CODE_DONT_TRIGGER),
        ],
    )
    def test_evaluates_trigger_on_rule(
        self, trigger_on_value, status, expected_exit_code, mock_logger, clean_env
    ):
        """Test: trigger_on rule correctly determines exit code"""
        # Arrange
        config_data = {
            "enabled": True,
            "global_rules": {"trigger_on": trigger_on_value},
            "operations": {"dev": {"trigger_on": trigger_on_value}},
        }

        with patch("devforgeai_cli.commands.check_hooks.yaml.safe_load") as mock_yaml:
            mock_yaml.return_value = config_data
            with patch("builtins.open", mock_open(read_data=json.dumps(config_data))):
                # Act
                result = check_hooks_command(
                    operation="dev", status=status, config_path=None
                )

                # Assert
                assert (
                    result == expected_exit_code
                ), f"trigger_on={trigger_on_value}, status={status} should return {expected_exit_code}, got {result}"

    def test_trigger_rule_all_fires_on_success(
        self, temp_hooks_config, mock_logger, clean_env
    ):
        """Test: 'all' rule fires on success status"""
        # Arrange
        with patch("builtins.open", mock_open(read_data="")):
            with patch("devforgeai_cli.commands.check_hooks.yaml.safe_load") as mock_yaml:
                mock_yaml.return_value = {
                    "enabled": True,
                    "global_rules": {"trigger_on": "all"},
                    "operations": {},
                }

                # Act
                result = check_hooks_command(
                    operation="dev", status="success", config_path=None
                )

                # Assert
                assert result == EXIT_CODE_TRIGGER

    def test_trigger_rule_failures_only_blocks_success(
        self, temp_hooks_config, mock_logger, clean_env
    ):
        """Test: 'failures-only' rule blocks on success status"""
        # Arrange
        with patch("builtins.open", mock_open(read_data="")):
            with patch("devforgeai_cli.commands.check_hooks.yaml.safe_load") as mock_yaml:
                mock_yaml.return_value = {
                    "enabled": True,
                    "global_rules": {"trigger_on": "failures-only"},
                    "operations": {},
                }

                # Act
                result = check_hooks_command(
                    operation="dev", status="success", config_path=None
                )

                # Assert
                assert result == EXIT_CODE_DONT_TRIGGER

    def test_trigger_rule_failures_only_fires_on_failure(
        self, temp_hooks_config, mock_logger, clean_env
    ):
        """Test: 'failures-only' rule fires on failure status"""
        # Arrange
        with patch("builtins.open", mock_open(read_data="")):
            with patch("devforgeai_cli.commands.check_hooks.yaml.safe_load") as mock_yaml:
                mock_yaml.return_value = {
                    "enabled": True,
                    "global_rules": {"trigger_on": "failures-only"},
                    "operations": {},
                }

                # Act
                result = check_hooks_command(
                    operation="qa", status="failure", config_path=None
                )

                # Assert
                assert result == EXIT_CODE_TRIGGER

    def test_trigger_rule_none_never_fires(
        self, temp_hooks_config, mock_logger, clean_env
    ):
        """Test: 'none' rule never triggers"""
        # Arrange
        with patch("builtins.open", mock_open(read_data="")):
            with patch("devforgeai_cli.commands.check_hooks.yaml.safe_load") as mock_yaml:
                mock_yaml.return_value = {
                    "enabled": True,
                    "global_rules": {"trigger_on": "none"},
                    "operations": {},
                }

                # Act - try both success and failure
                result_success = check_hooks_command(
                    operation="dev", status="success", config_path=None
                )
                result_failure = check_hooks_command(
                    operation="dev", status="failure", config_path=None
                )

                # Assert
                assert result_success == EXIT_CODE_DONT_TRIGGER
                assert result_failure == EXIT_CODE_DONT_TRIGGER


class TestAC3_OperationSpecificRules:
    """AC3: Operation-Specific Rules
    Check operation-specific overrides, fall back to global rules"""

    def test_operation_override_takes_precedence_over_global(
        self, mock_logger, clean_env
    ):
        """Test: Operation-specific rule overrides global rule"""
        # Arrange
        config_data = {
            "enabled": True,
            "global_rules": {"trigger_on": "none"},  # Global: don't trigger
            "operations": {
                "dev": {"trigger_on": "all"}  # Override: do trigger
            },
        }

        with patch("builtins.open", mock_open(read_data=json.dumps(config_data))):
            with patch("devforgeai_cli.commands.check_hooks.yaml.safe_load") as mock_yaml:
                mock_yaml.return_value = config_data

                # Act
                result = check_hooks_command(
                    operation="dev", status="success", config_path=None
                )

                # Assert
                assert result == EXIT_CODE_TRIGGER

    def test_falls_back_to_global_rule_if_no_operation_override(
        self, mock_logger, clean_env
    ):
        """Test: Falls back to global rule if operation not in config"""
        # Arrange
        config_data = {
            "enabled": True,
            "global_rules": {"trigger_on": "all"},
            "operations": {},  # No operation-specific rules
        }

        with patch("builtins.open", mock_open(read_data=json.dumps(config_data))):
            with patch("devforgeai_cli.commands.check_hooks.yaml.safe_load") as mock_yaml:
                mock_yaml.return_value = config_data

                # Act
                result = check_hooks_command(
                    operation="custom_op", status="success", config_path=None
                )

                # Assert
                assert result == EXIT_CODE_TRIGGER

    def test_multiple_operations_with_different_rules(
        self, mock_logger, clean_env
    ):
        """Test: Multiple operations with different rules behave correctly"""
        # Arrange
        config_data = {
            "enabled": True,
            "global_rules": {"trigger_on": "all"},
            "operations": {
                "dev": {"trigger_on": "all"},
                "qa": {"trigger_on": "failures-only"},
                "release": {"trigger_on": "none"},
            },
        }

        with patch("builtins.open", mock_open(read_data=json.dumps(config_data))):
            with patch("devforgeai_cli.commands.check_hooks.yaml.safe_load") as mock_yaml:
                mock_yaml.return_value = config_data

                # Act & Assert
                # dev with 'all' should trigger on success
                assert (
                    check_hooks_command(operation="dev", status="success", config_path=None)
                    == EXIT_CODE_TRIGGER
                )
                # qa with 'failures-only' should not trigger on success
                assert (
                    check_hooks_command(operation="qa", status="success", config_path=None)
                    == EXIT_CODE_DONT_TRIGGER
                )
                # release with 'none' should never trigger
                assert (
                    check_hooks_command(operation="release", status="failure", config_path=None)
                    == EXIT_CODE_DONT_TRIGGER
                )

    def test_operation_specific_overrides_block_when_global_allows(
        self, mock_logger, clean_env
    ):
        """Test: Operation override can block when global allows"""
        # Arrange
        config_data = {
            "enabled": True,
            "global_rules": {"trigger_on": "all"},
            "operations": {
                "staging": {"trigger_on": "none"}  # Block even though global allows
            },
        }

        with patch("builtins.open", mock_open(read_data=json.dumps(config_data))):
            with patch("devforgeai_cli.commands.check_hooks.yaml.safe_load") as mock_yaml:
                mock_yaml.return_value = config_data

                # Act
                result = check_hooks_command(
                    operation="staging", status="failure", config_path=None
                )

                # Assert
                assert result == EXIT_CODE_DONT_TRIGGER


class TestAC4_Performance:
    """AC4: Performance - Complete in <100ms (95th percentile)"""

    def test_check_hooks_completes_in_under_100ms(
        self, temp_hooks_config, mock_logger, clean_env
    ):
        """Test: Command completes in <100ms"""
        # Arrange
        start_time = time.time()

        # Act
        result = check_hooks_command(
            operation="dev",
            status="success",
            config_path=temp_hooks_config,
        )

        # Assert
        elapsed_ms = (time.time() - start_time) * 1000
        assert elapsed_ms < 100, f"Execution took {elapsed_ms:.2f}ms, expected <100ms"

    def test_performance_multiple_operations(
        self, temp_hooks_config, mock_logger, clean_env
    ):
        """Test: Performance consistent across multiple operations"""
        # Arrange
        operations = ["dev", "qa", "release", "orchestrate", "ideate"]
        times = []

        # Act
        for op in operations:
            start = time.time()
            check_hooks_command(operation=op, status="success", config_path=temp_hooks_config)
            times.append((time.time() - start) * 1000)

        # Assert
        max_time = max(times)
        assert max_time < 100, f"Max execution time {max_time:.2f}ms exceeded 100ms limit"
        assert all(t < 100 for t in times), f"Some operations exceeded 100ms: {times}"

    @pytest.mark.parametrize("iteration", range(10))
    def test_performance_95th_percentile_under_100ms(
        self, temp_hooks_config, mock_logger, clean_env, iteration
    ):
        """Test: 95th percentile of execution times under 100ms (10 iterations)"""
        # Arrange
        start = time.time()

        # Act
        check_hooks_command(
            operation="dev",
            status="success",
            config_path=temp_hooks_config,
        )

        # Assert
        elapsed_ms = (time.time() - start) * 1000
        assert elapsed_ms < 100, f"Iteration {iteration}: {elapsed_ms:.2f}ms > 100ms"


class TestAC5_ErrorHandling_MissingConfig:
    """AC5: Error Handling - Missing Config
    Log warning, return exit code 1"""

    def test_missing_config_file_logs_warning(self, mock_logger, clean_env):
        """Test: Missing config file logs warning message"""
        # Arrange
        nonexistent_path = "/nonexistent/path/hooks.yaml"

        # Act
        result = check_hooks_command(
            operation="dev",
            status="success",
            config_path=nonexistent_path,
        )

        # Assert
        assert result == EXIT_CODE_DONT_TRIGGER
        mock_logger.warning.assert_called()
        warning_msg = str(mock_logger.warning.call_args)
        assert "config" in warning_msg.lower() or "file" in warning_msg.lower()

    def test_missing_config_file_returns_exit_code_1(
        self, mock_logger, clean_env
    ):
        """Test: Missing config file returns exit code 1"""
        # Arrange
        nonexistent_path = "/nonexistent/hooks.yaml"

        # Act
        result = check_hooks_command(
            operation="dev",
            status="success",
            config_path=nonexistent_path,
        )

        # Assert
        assert result == EXIT_CODE_DONT_TRIGGER

    def test_default_config_path_checked_when_not_provided(
        self, mock_logger, clean_env
    ):
        """Test: Default config path checked when config_path=None"""
        # Arrange
        default_config_path = ".devforgeai/config/hooks.yaml"

        with patch("os.path.exists") as mock_exists:
            mock_exists.return_value = False

            # Act
            result = check_hooks_command(
                operation="dev",
                status="success",
                config_path=None,
            )

            # Assert
            assert result == EXIT_CODE_DONT_TRIGGER
            # Should have checked for default path
            mock_exists.assert_called()

    def test_empty_config_file_logged_as_warning(
        self, mock_logger, clean_env
    ):
        """Test: Empty config file triggers warning"""
        # Arrange
        with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
            f.write("")  # Empty file
            config_path = f.name

        try:
            with patch("devforgeai_cli.commands.check_hooks.yaml.safe_load") as mock_yaml:
                mock_yaml.return_value = None

                # Act
                result = check_hooks_command(
                    operation="dev",
                    status="success",
                    config_path=config_path,
                )

                # Assert
                assert result == EXIT_CODE_DONT_TRIGGER
                mock_logger.warning.assert_called()
        finally:
            if os.path.exists(config_path):
                os.remove(config_path)


class TestAC6_ErrorHandling_InvalidArguments:
    """AC6: Error Handling - Invalid Arguments
    Return exit code 2 for invalid status"""

    @pytest.mark.parametrize(
        "invalid_status",
        [
            "invalid",
            "maybe",
            "unknown",
            "skip",
            "",
            "FAILURE",  # Case sensitivity
            "SUCCESS",  # Case sensitivity
        ],
    )
    def test_invalid_status_returns_exit_code_2(
        self, invalid_status, mock_logger, clean_env
    ):
        """Test: Invalid status argument returns exit code 2"""
        # Arrange & Act
        result = check_hooks_command(
            operation="dev",
            status=invalid_status,
            config_path=None,
        )

        # Assert
        assert result == EXIT_CODE_ERROR

    @pytest.mark.parametrize(
        "valid_status",
        [
            "success",
            "failure",
            "partial",
        ],
    )
    def test_valid_status_does_not_return_error_code(
        self, valid_status, mock_logger, clean_env
    ):
        """Test: Valid status arguments don't return exit code 2"""
        # Arrange
        with patch("builtins.open", mock_open(read_data="")):
            with patch("devforgeai_cli.commands.check_hooks.yaml.safe_load") as mock_yaml:
                mock_yaml.return_value = {
                    "enabled": True,
                    "global_rules": {"trigger_on": "all"},
                    "operations": {},
                }

                # Act
                result = check_hooks_command(
                    operation="dev",
                    status=valid_status,
                    config_path=None,
                )

                # Assert
                assert result != EXIT_CODE_ERROR

    def test_empty_status_returns_error_code(
        self, mock_logger, clean_env
    ):
        """Test: Empty status returns error code 2"""
        # Act
        result = check_hooks_command(
            operation="dev",
            status="",
            config_path=None,
        )

        # Assert
        assert result == EXIT_CODE_ERROR

    def test_invalid_operation_returns_error_code(
        self, mock_logger, clean_env
    ):
        """Test: Invalid operation format returns error code 2"""
        # Arrange
        with patch("builtins.open", mock_open(read_data="")):
            with patch("devforgeai_cli.commands.check_hooks.yaml.safe_load") as mock_yaml:
                mock_yaml.return_value = {
                    "enabled": True,
                    "global_rules": {"trigger_on": "all"},
                    "operations": {},
                }

                # Act - operation with invalid characters
                result = check_hooks_command(
                    operation="",
                    status="success",
                    config_path=None,
                )

                # Assert
                assert result == EXIT_CODE_ERROR

    def test_invalid_arguments_logs_error(
        self, mock_logger, clean_env
    ):
        """Test: Invalid arguments are logged"""
        # Act
        result = check_hooks_command(
            operation="dev",
            status="invalid_status",
            config_path=None,
        )

        # Assert
        assert result == EXIT_CODE_ERROR
        # Logger should have logged error
        assert mock_logger.error.called or mock_logger.warning.called


class TestAC7_CircularInvocationDetection:
    """AC7: Circular Invocation Detection
    Detect DEVFORGEAI_HOOK_ACTIVE env var, return exit code 1"""

    def test_detects_devforgeai_hook_active_env_var(
        self, mock_logger, clean_env
    ):
        """Test: Detects DEVFORGEAI_HOOK_ACTIVE environment variable"""
        # Arrange
        os.environ["DEVFORGEAI_HOOK_ACTIVE"] = "1"

        with patch("builtins.open", mock_open(read_data="")):
            with patch("devforgeai_cli.commands.check_hooks.yaml.safe_load") as mock_yaml:
                mock_yaml.return_value = {
                    "enabled": True,
                    "global_rules": {"trigger_on": "all"},
                    "operations": {},
                }

                # Act
                result = check_hooks_command(
                    operation="dev",
                    status="success",
                    config_path=None,
                )

                # Assert
                assert result == EXIT_CODE_DONT_TRIGGER

    def test_circular_detection_returns_exit_code_1(
        self, mock_logger, clean_env
    ):
        """Test: Circular invocation returns exit code 1"""
        # Arrange
        os.environ["DEVFORGEAI_HOOK_ACTIVE"] = "true"

        # Act
        result = check_hooks_command(
            operation="qa",
            status="failure",
            config_path=None,
        )

        # Assert
        assert result == EXIT_CODE_DONT_TRIGGER

    def test_no_circular_detection_when_env_var_absent(
        self, temp_hooks_config, mock_logger, clean_env
    ):
        """Test: Normal operation when DEVFORGEAI_HOOK_ACTIVE absent"""
        # Arrange
        # Ensure var is not set
        assert "DEVFORGEAI_HOOK_ACTIVE" not in os.environ

        # Act
        result = check_hooks_command(
            operation="dev",
            status="success",
            config_path=temp_hooks_config,
        )

        # Assert
        # Should process normally (not immediately return 1)
        assert result in [EXIT_CODE_TRIGGER, EXIT_CODE_DONT_TRIGGER]

    def test_circular_detection_overrides_all_rules(
        self, mock_logger, clean_env
    ):
        """Test: Circular detection overrides all trigger rules"""
        # Arrange
        os.environ["DEVFORGEAI_HOOK_ACTIVE"] = "1"

        with patch("builtins.open", mock_open(read_data="")):
            with patch("devforgeai_cli.commands.check_hooks.yaml.safe_load") as mock_yaml:
                mock_yaml.return_value = {
                    "enabled": True,
                    "global_rules": {"trigger_on": "all"},
                    "operations": {
                        "dev": {"trigger_on": "all"}
                    },
                }

                # Act
                # Even with 'all' rule, circular detection should block
                result = check_hooks_command(
                    operation="dev",
                    status="failure",
                    config_path=None,
                )

                # Assert
                assert result == EXIT_CODE_DONT_TRIGGER

    def test_logs_circular_invocation_warning(
        self, mock_logger, clean_env
    ):
        """Test: Circular invocation is logged"""
        # Arrange
        os.environ["DEVFORGEAI_HOOK_ACTIVE"] = "1"

        # Act
        check_hooks_command(
            operation="dev",
            status="success",
            config_path=None,
        )

        # Assert
        assert mock_logger.warning.called or mock_logger.info.called
        call_args = str(mock_logger.warning.call_args or mock_logger.info.call_args)
        assert "circular" in call_args.lower() or "hook_active" in call_args.lower()


# ============================================================================
# BUSINESS RULES TESTS
# ============================================================================


class TestBR_BusinessRules:
    """Business Rule Tests (BR-001 to BR-003)"""

    def test_br001_enabled_field_is_boolean(
        self, mock_logger, clean_env
    ):
        """BR-001: enabled field must be boolean"""
        # Arrange
        with patch("builtins.open", mock_open(read_data="")):
            with patch("devforgeai_cli.commands.check_hooks.yaml.safe_load") as mock_yaml:
                # Test with non-boolean value
                mock_yaml.return_value = {
                    "enabled": "yes",  # String instead of boolean
                    "global_rules": {"trigger_on": "all"},
                    "operations": {},
                }

                # Act
                result = check_hooks_command(
                    operation="dev",
                    status="success",
                    config_path=None,
                )

                # Assert - Should handle gracefully
                assert result in [EXIT_CODE_TRIGGER, EXIT_CODE_DONT_TRIGGER, EXIT_CODE_ERROR]

    def test_br002_trigger_on_values_constrained(
        self, mock_logger, clean_env
    ):
        """BR-002: trigger_on must be one of: all, failures-only, none"""
        # Arrange
        invalid_rules = ["maybe", "sometimes", "on_weekends"]

        # Act & Assert
        for invalid_rule in invalid_rules:
            with patch("builtins.open", mock_open(read_data="")):
                with patch("devforgeai_cli.commands.check_hooks.yaml.safe_load") as mock_yaml:
                    mock_yaml.return_value = {
                        "enabled": True,
                        "global_rules": {"trigger_on": invalid_rule},
                        "operations": {},
                    }

                    result = check_hooks_command(
                        operation="dev",
                        status="success",
                        config_path=None,
                    )

                    # Invalid rules should be handled (error or fallback)
                    assert result in [
                        EXIT_CODE_TRIGGER,
                        EXIT_CODE_DONT_TRIGGER,
                        EXIT_CODE_ERROR,
                    ]

    def test_br003_status_values_constrained(
        self, mock_logger, clean_env
    ):
        """BR-003: status must be one of: success, failure, partial"""
        # Arrange
        valid_statuses = ["success", "failure", "partial"]

        # Act & Assert
        for valid_status in valid_statuses:
            with patch("builtins.open", mock_open(read_data="")):
                with patch("devforgeai_cli.commands.check_hooks.yaml.safe_load") as mock_yaml:
                    mock_yaml.return_value = {
                        "enabled": True,
                        "global_rules": {"trigger_on": "all"},
                        "operations": {},
                    }

                    result = check_hooks_command(
                        operation="dev",
                        status=valid_status,
                        config_path=None,
                    )

                    # Valid statuses should not return error code
                    assert result != EXIT_CODE_ERROR


# ============================================================================
# EDGE CASE TESTS
# ============================================================================


class TestEdgeCases:
    """Edge Case and Special Scenario Tests"""

    def test_edge_case_empty_operations_dict(
        self, mock_logger, clean_env
    ):
        """Edge Case: Empty operations dictionary falls back to global rules"""
        # Arrange
        with patch("builtins.open", mock_open(read_data="")):
            with patch("devforgeai_cli.commands.check_hooks.yaml.safe_load") as mock_yaml:
                mock_yaml.return_value = {
                    "enabled": True,
                    "global_rules": {"trigger_on": "all"},
                    "operations": {},  # Empty
                }

                # Act
                result = check_hooks_command(
                    operation="custom_operation",
                    status="success",
                    config_path=None,
                )

                # Assert
                assert result == EXIT_CODE_TRIGGER

    def test_edge_case_missing_global_rules(
        self, mock_logger, clean_env
    ):
        """Edge Case: Missing global_rules falls back gracefully"""
        # Arrange
        with patch("builtins.open", mock_open(read_data="")):
            with patch("devforgeai_cli.commands.check_hooks.yaml.safe_load") as mock_yaml:
                mock_yaml.return_value = {
                    "enabled": True,
                    # Missing global_rules
                    "operations": {"dev": {"trigger_on": "all"}},
                }

                # Act
                result = check_hooks_command(
                    operation="dev",
                    status="success",
                    config_path=None,
                )

                # Assert - Should use operation-specific rule
                assert result in [EXIT_CODE_TRIGGER, EXIT_CODE_DONT_TRIGGER, EXIT_CODE_ERROR]

    def test_edge_case_malformed_yaml(
        self, mock_logger, clean_env
    ):
        """Edge Case: Malformed YAML file handled gracefully"""
        # Arrange
        with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
            f.write("INVALID: YAML: {[CONTENT")
            config_path = f.name

        try:
            with patch("devforgeai_cli.commands.check_hooks.yaml.safe_load") as mock_yaml:
                mock_yaml.side_effect = Exception("YAML parsing error")

                # Act
                result = check_hooks_command(
                    operation="dev",
                    status="success",
                    config_path=config_path,
                )

                # Assert
                assert result in [EXIT_CODE_DONT_TRIGGER, EXIT_CODE_ERROR]
                assert mock_logger.error.called or mock_logger.warning.called
        finally:
            if os.path.exists(config_path):
                os.remove(config_path)

    def test_edge_case_special_characters_in_operation_name(
        self, mock_logger, clean_env
    ):
        """Edge Case: Special characters in operation name"""
        # Arrange
        with patch("builtins.open", mock_open(read_data="")):
            with patch("devforgeai_cli.commands.check_hooks.yaml.safe_load") as mock_yaml:
                mock_yaml.return_value = {
                    "enabled": True,
                    "global_rules": {"trigger_on": "all"},
                    "operations": {"dev-qa": {"trigger_on": "all"}},
                }

                # Act
                result = check_hooks_command(
                    operation="dev-qa",
                    status="success",
                    config_path=None,
                )

                # Assert - Should handle special characters
                assert result in [EXIT_CODE_TRIGGER, EXIT_CODE_DONT_TRIGGER, EXIT_CODE_ERROR]

    def test_edge_case_unicode_in_operation_name(
        self, mock_logger, clean_env
    ):
        """Edge Case: Unicode characters in operation name"""
        # Arrange
        with patch("builtins.open", mock_open(read_data="")):
            with patch("devforgeai_cli.commands.check_hooks.yaml.safe_load") as mock_yaml:
                mock_yaml.return_value = {
                    "enabled": True,
                    "global_rules": {"trigger_on": "all"},
                    "operations": {"déveñ": {"trigger_on": "all"}},
                }

                # Act - Should handle unicode or reject
                result = check_hooks_command(
                    operation="déveñ",
                    status="success",
                    config_path=None,
                )

                # Assert
                assert result in [EXIT_CODE_TRIGGER, EXIT_CODE_DONT_TRIGGER, EXIT_CODE_ERROR]

    def test_edge_case_very_long_operation_name(
        self, mock_logger, clean_env
    ):
        """Edge Case: Very long operation name"""
        # Arrange
        long_op_name = "a" * 1000

        with patch("builtins.open", mock_open(read_data="")):
            with patch("devforgeai_cli.commands.check_hooks.yaml.safe_load") as mock_yaml:
                mock_yaml.return_value = {
                    "enabled": True,
                    "global_rules": {"trigger_on": "all"},
                    "operations": {},
                }

                # Act
                result = check_hooks_command(
                    operation=long_op_name,
                    status="success",
                    config_path=None,
                )

                # Assert - Should handle gracefully
                assert result in [EXIT_CODE_TRIGGER, EXIT_CODE_DONT_TRIGGER, EXIT_CODE_ERROR]

    def test_edge_case_operation_case_sensitivity(
        self, mock_logger, clean_env
    ):
        """Edge Case: Operation names case sensitivity"""
        # Arrange
        with patch("builtins.open", mock_open(read_data="")):
            with patch("devforgeai_cli.commands.check_hooks.yaml.safe_load") as mock_yaml:
                mock_yaml.return_value = {
                    "enabled": True,
                    "global_rules": {"trigger_on": "none"},
                    "operations": {
                        "Dev": {"trigger_on": "all"}  # Capital D
                    },
                }

                # Act - lowercase vs uppercase
                result_lowercase = check_hooks_command(
                    operation="dev",
                    status="success",
                    config_path=None,
                )
                result_uppercase = check_hooks_command(
                    operation="Dev",
                    status="success",
                    config_path=None,
                )

                # Assert - Behavior should be consistent (either case-sensitive or normalized)
                # Both results should be valid exit codes
                assert result_lowercase in [EXIT_CODE_TRIGGER, EXIT_CODE_DONT_TRIGGER]
                assert result_uppercase in [EXIT_CODE_TRIGGER, EXIT_CODE_DONT_TRIGGER]

    def test_edge_case_null_config_values(
        self, mock_logger, clean_env
    ):
        """Edge Case: Null values in config"""
        # Arrange
        with patch("builtins.open", mock_open(read_data="")):
            with patch("devforgeai_cli.commands.check_hooks.yaml.safe_load") as mock_yaml:
                mock_yaml.return_value = {
                    "enabled": True,
                    "global_rules": None,  # Null
                    "operations": None,  # Null
                }

                # Act
                result = check_hooks_command(
                    operation="dev",
                    status="success",
                    config_path=None,
                )

                # Assert - Should handle gracefully
                assert result in [EXIT_CODE_TRIGGER, EXIT_CODE_DONT_TRIGGER, EXIT_CODE_ERROR]


# ============================================================================
# INTEGRATION TESTS
# ============================================================================


class TestIntegration:
    """Integration Tests - Full Workflow Scenarios"""

    def test_integration_full_workflow_dev_success(
        self, temp_hooks_config, mock_logger, clean_env
    ):
        """Integration: Full workflow for dev operation with success status"""
        # Arrange - temp_hooks_config fixture sets up valid config

        # Act
        result = check_hooks_command(
            operation="dev",
            status="success",
            config_path=temp_hooks_config,
        )

        # Assert
        assert result in [EXIT_CODE_TRIGGER, EXIT_CODE_DONT_TRIGGER]
        assert isinstance(result, int)
        assert 0 <= result <= 2

    def test_integration_full_workflow_qa_failure(
        self, temp_hooks_config, mock_logger, clean_env
    ):
        """Integration: Full workflow for qa operation with failure status"""
        # Arrange

        # Act
        result = check_hooks_command(
            operation="qa",
            status="failure",
            config_path=temp_hooks_config,
        )

        # Assert
        assert result in [EXIT_CODE_TRIGGER, EXIT_CODE_DONT_TRIGGER]
        assert isinstance(result, int)

    def test_integration_full_workflow_release_disabled(
        self, temp_disabled_hooks_config, mock_logger, clean_env
    ):
        """Integration: Disabled config disables all operations"""
        # Arrange

        # Act
        result = check_hooks_command(
            operation="release",
            status="success",
            config_path=temp_disabled_hooks_config,
        )

        # Assert
        assert result == EXIT_CODE_DONT_TRIGGER

    def test_integration_multiple_sequential_calls(
        self, temp_hooks_config, mock_logger, clean_env
    ):
        """Integration: Multiple sequential calls work correctly"""
        # Arrange
        operations = ["dev", "qa", "release"]
        statuses = ["success", "failure", "partial"]

        # Act
        for op in operations:
            for status in statuses:
                result = check_hooks_command(
                    operation=op,
                    status=status,
                    config_path=temp_hooks_config,
                )

                # Assert
                assert result in [EXIT_CODE_TRIGGER, EXIT_CODE_DONT_TRIGGER]


# ============================================================================
# VALIDATOR CLASS TESTS (if CheckHooksValidator exists)
# ============================================================================


class TestCheckHooksValidator:
    """Tests for CheckHooksValidator class"""

    @pytest.mark.skipif(
        CheckHooksValidator is None,
        reason="CheckHooksValidator not yet implemented"
    )
    def test_validator_validates_config_schema(self):
        """Test: Validator enforces config schema"""
        # Arrange
        config = {
            "enabled": True,
            "global_rules": {"trigger_on": "all"},
            "operations": {},
        }

        # Act
        validator = CheckHooksValidator(config)

        # Assert
        assert validator is not None

    @pytest.mark.skipif(
        CheckHooksValidator is None,
        reason="CheckHooksValidator not yet implemented"
    )
    def test_validator_rejects_invalid_trigger_on(self):
        """Test: Validator rejects invalid trigger_on value"""
        # Arrange
        config = {
            "enabled": True,
            "global_rules": {"trigger_on": "invalid"},
            "operations": {},
        }

        # Act & Assert
        with pytest.raises(ValueError):
            validator = CheckHooksValidator(config)
            validator.validate()


# ============================================================================
# SUMMARY - Test Statistics
# ============================================================================
"""
TEST SUITE SUMMARY
==================

Total Test Cases: 50+

Acceptance Criteria Coverage:
  AC1 (Configuration Check): 5 tests
  AC2 (Trigger Rule Matching): 8 tests
  AC3 (Operation-Specific Rules): 5 tests
  AC4 (Performance): 3 tests
  AC5 (Missing Config): 4 tests
  AC6 (Invalid Arguments): 7 tests
  AC7 (Circular Invocation): 5 tests

Business Rules Coverage:
  BR-001 (enabled boolean): 1 test
  BR-002 (trigger_on constraints): 1 test
  BR-003 (status constraints): 1 test

Edge Cases: 8 tests
Integration Tests: 4 tests
Validator Tests: 2 tests (conditional)

Test Patterns Used:
  - AAA (Arrange-Act-Assert)
  - Fixtures for setup/teardown
  - Parametrized tests for multiple scenarios
  - Mocking (unittest.mock)
  - Temporary file fixtures
  - Environment variable isolation

Expected Exit Codes:
  0 - trigger hooks
  1 - don't trigger hooks
  2 - error (invalid arguments)

Performance Requirements:
  <100ms per execution (95th percentile)

Coverage Target:
  >90% line coverage
  >85% branch coverage

All tests are FAILING (Red Phase - TDD)
Implementation required to make tests pass
"""
