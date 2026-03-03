"""
Tests for AC#1: Per-Command Metrics

Acceptance Criteria:
Given command execution data,
When calculating metrics,
Then completion rate, error rate, and retry rate are computed per command type.

Test Framework: pytest
Test Pattern: AAA (Arrange, Act, Assert)
TDD Phase: Red (all tests should FAIL initially - no implementation exists)
"""
import pytest
from typing import Dict, List, Any

# Import the module under test (does not exist yet - TDD Red phase)
# These stub functions will fail tests until real implementation is created
try:
    from devforgeai_cli.metrics.command_metrics import (
        calculate_completion_rate,
        calculate_error_rate,
        calculate_retry_rate,
        calculate_per_command_metrics,
    )
except ModuleNotFoundError:
    # Stub functions that raise NotImplementedError for TDD Red phase
    def calculate_completion_rate(data, command_type):
        raise NotImplementedError("Module devforgeai_cli.metrics.command_metrics not implemented")

    def calculate_error_rate(data, command_type):
        raise NotImplementedError("Module devforgeai_cli.metrics.command_metrics not implemented")

    def calculate_retry_rate(data, command_type):
        raise NotImplementedError("Module devforgeai_cli.metrics.command_metrics not implemented")

    def calculate_per_command_metrics(data):
        raise NotImplementedError("Module devforgeai_cli.metrics.command_metrics not implemented")


class TestCalculateCompletionRate:
    """Tests for completion rate calculation per command type."""

    def test_calculate_completion_rate_returns_percentage(
        self, sample_command_execution_data: List[Dict[str, Any]]
    ):
        """
        Given: Command execution data with mixed success/error statuses
        When: Calculating completion rate for /dev command
        Then: Returns percentage of completed executions (60% = 3/5)
        """
        # Arrange
        command_type = "/dev"

        # Act
        result = calculate_completion_rate(sample_command_execution_data, command_type)

        # Assert
        assert result == 60.0, f"Expected 60.0% completion rate for /dev, got {result}%"

    def test_calculate_completion_rate_returns_100_for_all_successful(
        self, sample_command_execution_data: List[Dict[str, Any]]
    ):
        """
        Given: Command execution data where all /create-story commands succeeded
        When: Calculating completion rate for /create-story
        Then: Returns 100.0%
        """
        # Arrange
        command_type = "/create-story"

        # Act
        result = calculate_completion_rate(sample_command_execution_data, command_type)

        # Assert
        assert result == 100.0, f"Expected 100.0% for /create-story, got {result}%"

    def test_calculate_completion_rate_with_empty_data_returns_zero(
        self, empty_command_execution_data: List[Dict[str, Any]]
    ):
        """
        Given: Empty command execution data
        When: Calculating completion rate
        Then: Returns 0.0 (graceful handling of empty input)
        """
        # Arrange
        command_type = "/dev"

        # Act
        result = calculate_completion_rate(empty_command_execution_data, command_type)

        # Assert
        assert result == 0.0, f"Expected 0.0% for empty data, got {result}%"

    def test_calculate_completion_rate_for_nonexistent_command(
        self, sample_command_execution_data: List[Dict[str, Any]]
    ):
        """
        Given: Command execution data
        When: Calculating completion rate for a command that doesn't exist in data
        Then: Returns 0.0
        """
        # Arrange
        command_type = "/nonexistent"

        # Act
        result = calculate_completion_rate(sample_command_execution_data, command_type)

        # Assert
        assert result == 0.0, f"Expected 0.0% for nonexistent command, got {result}%"


class TestCalculateErrorRate:
    """Tests for error rate calculation per command type."""

    def test_calculate_error_rate_per_command_type(
        self, sample_command_execution_data: List[Dict[str, Any]]
    ):
        """
        Given: Command execution data with errors
        When: Calculating error rate for /dev command
        Then: Returns percentage of failed executions (40% = 2/5)
        """
        # Arrange
        command_type = "/dev"

        # Act
        result = calculate_error_rate(sample_command_execution_data, command_type)

        # Assert
        assert result == 40.0, f"Expected 40.0% error rate for /dev, got {result}%"

    def test_calculate_error_rate_for_qa_command(
        self, sample_command_execution_data: List[Dict[str, Any]]
    ):
        """
        Given: Command execution data
        When: Calculating error rate for /qa command
        Then: Returns correct percentage (33.33% = 1/3)
        """
        # Arrange
        command_type = "/qa"

        # Act
        result = calculate_error_rate(sample_command_execution_data, command_type)

        # Assert
        # 1 error out of 3 /qa commands = 33.33%
        assert abs(result - 33.33) < 0.01, f"Expected ~33.33% error rate for /qa, got {result}%"

    def test_calculate_error_rate_with_no_errors_returns_zero(
        self, sample_command_execution_data: List[Dict[str, Any]]
    ):
        """
        Given: Command execution data where /create-story has no errors
        When: Calculating error rate for /create-story
        Then: Returns 0.0%
        """
        # Arrange
        command_type = "/create-story"

        # Act
        result = calculate_error_rate(sample_command_execution_data, command_type)

        # Assert
        assert result == 0.0, f"Expected 0.0% error rate for /create-story, got {result}%"

    def test_calculate_error_rate_with_empty_data_returns_zero(
        self, empty_command_execution_data: List[Dict[str, Any]]
    ):
        """
        Given: Empty command execution data
        When: Calculating error rate
        Then: Returns 0.0 (graceful handling)
        """
        # Arrange
        command_type = "/dev"

        # Act
        result = calculate_error_rate(empty_command_execution_data, command_type)

        # Assert
        assert result == 0.0


class TestCalculateRetryRate:
    """Tests for retry rate calculation per command type."""

    def test_calculate_retry_rate_per_command_type(
        self, sample_command_execution_data: List[Dict[str, Any]]
    ):
        """
        Given: Command execution data with retries
        When: Calculating retry rate for /dev command
        Then: Returns percentage of executions that had retries (40% = 2/5 had retry_count > 0)
        """
        # Arrange
        command_type = "/dev"

        # Act
        result = calculate_retry_rate(sample_command_execution_data, command_type)

        # Assert
        # 2 out of 5 /dev commands had retry_count > 0
        assert result == 40.0, f"Expected 40.0% retry rate for /dev, got {result}%"

    def test_calculate_retry_rate_for_qa_command(
        self, sample_command_execution_data: List[Dict[str, Any]]
    ):
        """
        Given: Command execution data
        When: Calculating retry rate for /qa command
        Then: Returns correct percentage (33.33% = 1/3)
        """
        # Arrange
        command_type = "/qa"

        # Act
        result = calculate_retry_rate(sample_command_execution_data, command_type)

        # Assert
        # 1 out of 3 /qa commands had retry_count > 0
        assert abs(result - 33.33) < 0.01, f"Expected ~33.33% retry rate for /qa, got {result}%"

    def test_calculate_retry_rate_with_no_retries_returns_zero(
        self, sample_command_execution_data: List[Dict[str, Any]]
    ):
        """
        Given: Command execution data where /create-story had no retries
        When: Calculating retry rate for /create-story
        Then: Returns 0.0%
        """
        # Arrange
        command_type = "/create-story"

        # Act
        result = calculate_retry_rate(sample_command_execution_data, command_type)

        # Assert
        assert result == 0.0, f"Expected 0.0% retry rate for /create-story, got {result}%"

    def test_calculate_retry_rate_with_empty_data_returns_zero(
        self, empty_command_execution_data: List[Dict[str, Any]]
    ):
        """
        Given: Empty command execution data
        When: Calculating retry rate
        Then: Returns 0.0 (graceful handling)
        """
        # Arrange
        command_type = "/dev"

        # Act
        result = calculate_retry_rate(empty_command_execution_data, command_type)

        # Assert
        assert result == 0.0


class TestCalculatePerCommandMetrics:
    """Tests for aggregated per-command metrics calculation."""

    def test_metrics_with_mixed_command_types(
        self, sample_command_execution_data: List[Dict[str, Any]]
    ):
        """
        Given: Command execution data with multiple command types
        When: Calculating metrics for all commands
        Then: Returns metrics dictionary with completion_rate, error_rate, retry_rate per command
        """
        # Arrange & Act
        result = calculate_per_command_metrics(sample_command_execution_data)

        # Assert
        assert "/dev" in result, "Expected /dev in metrics"
        assert "/qa" in result, "Expected /qa in metrics"
        assert "/create-story" in result, "Expected /create-story in metrics"

        # Verify structure for each command
        for command in ["/dev", "/qa", "/create-story"]:
            assert "completion_rate" in result[command], f"Missing completion_rate for {command}"
            assert "error_rate" in result[command], f"Missing error_rate for {command}"
            assert "retry_rate" in result[command], f"Missing retry_rate for {command}"
            assert "total_executions" in result[command], f"Missing total_executions for {command}"

    def test_metrics_structure_contains_expected_fields(
        self, sample_command_execution_data: List[Dict[str, Any]]
    ):
        """
        Given: Command execution data
        When: Calculating per-command metrics
        Then: Each command entry contains required metric fields
        """
        # Arrange & Act
        result = calculate_per_command_metrics(sample_command_execution_data)

        # Assert
        expected_fields = {"completion_rate", "error_rate", "retry_rate", "total_executions"}

        for command, metrics in result.items():
            actual_fields = set(metrics.keys())
            missing = expected_fields - actual_fields
            assert not missing, f"Missing fields {missing} for command {command}"

    def test_metrics_with_empty_data_returns_empty_dict(
        self, empty_command_execution_data: List[Dict[str, Any]]
    ):
        """
        Given: Empty command execution data
        When: Calculating per-command metrics
        Then: Returns empty dictionary
        """
        # Arrange & Act
        result = calculate_per_command_metrics(empty_command_execution_data)

        # Assert
        assert result == {}, f"Expected empty dict for empty data, got {result}"

    def test_metrics_values_are_numeric(
        self, sample_command_execution_data: List[Dict[str, Any]]
    ):
        """
        Given: Command execution data
        When: Calculating per-command metrics
        Then: All rate values are floats between 0 and 100
        """
        # Arrange & Act
        result = calculate_per_command_metrics(sample_command_execution_data)

        # Assert
        for command, metrics in result.items():
            assert isinstance(metrics["completion_rate"], float), f"completion_rate not float for {command}"
            assert isinstance(metrics["error_rate"], float), f"error_rate not float for {command}"
            assert isinstance(metrics["retry_rate"], float), f"retry_rate not float for {command}"
            assert 0 <= metrics["completion_rate"] <= 100, f"completion_rate out of range for {command}"
            assert 0 <= metrics["error_rate"] <= 100, f"error_rate out of range for {command}"
            assert 0 <= metrics["retry_rate"] <= 100, f"retry_rate out of range for {command}"

    def test_total_executions_counts_correctly(
        self, sample_command_execution_data: List[Dict[str, Any]]
    ):
        """
        Given: Command execution data with known counts
        When: Calculating per-command metrics
        Then: total_executions matches actual count per command type
        """
        # Arrange & Act
        result = calculate_per_command_metrics(sample_command_execution_data)

        # Assert
        assert result["/dev"]["total_executions"] == 5, "Expected 5 /dev executions"
        assert result["/qa"]["total_executions"] == 3, "Expected 3 /qa executions"
        assert result["/create-story"]["total_executions"] == 2, "Expected 2 /create-story executions"
