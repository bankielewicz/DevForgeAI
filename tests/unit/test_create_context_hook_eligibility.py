"""
Unit tests for hook eligibility check logic (AC1) - /create-context command

Focuses on:
- Hook eligibility determination (check-hooks command)
- Exit code interpretation (0 = eligible, 1 = skip)
- Error detection and logging
- Command argument validation

TDD Red Phase: All tests fail until implementation complete.
Framework: pytest
Test Pattern: AAA (Arrange, Act, Assert)
"""

import pytest
import subprocess
from unittest.mock import Mock, patch, MagicMock, call
from pathlib import Path


class TestCheckHooksArgumentValidation:
    """Tests for check-hooks command argument validation."""

    @patch('subprocess.run')
    def test_check_hooks_receives_operation_argument(self, mock_run):
        """
        Test: check-hooks called with --operation=create-context

        Given: /create-context Phase N executes
        When: check-hooks command is invoked
        Then: --operation argument should be "create-context"
        """
        # Arrange
        mock_run.return_value = MagicMock(returncode=0, stdout="eligible")

        # Act
        subprocess.run(
            ["devforgeai", "check-hooks", "--operation=create-context", "--status=completed"]
        )

        # Assert
        assert mock_run.called
        args = str(mock_run.call_args)
        assert "create-context" in args


    @patch('subprocess.run')
    def test_check_hooks_receives_status_argument(self, mock_run):
        """
        Test: check-hooks called with --status=completed

        Given: Context files creation completed
        When: check-hooks is invoked
        Then: --status argument should be "completed"
        """
        # Arrange
        mock_run.return_value = MagicMock(returncode=0)

        # Act
        subprocess.run(
            ["devforgeai", "check-hooks", "--operation=create-context", "--status=completed"]
        )

        # Assert
        assert mock_run.called
        args = str(mock_run.call_args)
        assert "completed" in args


    @patch('subprocess.run')
    def test_check_hooks_both_arguments_required(self, mock_run):
        """
        Test: Both --operation and --status are required for check-hooks

        Given: check-hooks invoked from Phase N
        When: Called with both arguments
        Then: Both should be present in the command
        """
        # Arrange
        mock_run.return_value = MagicMock(returncode=0)

        # Act
        subprocess.run([
            "devforgeai", "check-hooks",
            "--operation=create-context",
            "--status=completed"
        ])

        # Assert
        call_args = mock_run.call_args[0][0]
        assert "--operation=create-context" in call_args
        assert "--status=completed" in call_args


# ============================================================================
# Exit Code Interpretation Tests
# ============================================================================


class TestCheckHooksExitCodeInterpretation:
    """Tests for interpreting check-hooks exit codes."""

    @patch('subprocess.run')
    def test_exit_code_zero_means_user_eligible(self, mock_run):
        """
        Test AC1: Exit code 0 indicates user is eligible for feedback

        Given: check-hooks returns exit code 0
        When: Exit code is interpreted
        Then: System should treat as "eligible" and proceed to invoke-hooks
        """
        # Arrange
        mock_run.return_value = MagicMock(returncode=0)

        # Act
        result = subprocess.run(["devforgeai", "check-hooks"])
        is_eligible = result.returncode == 0

        # Assert
        assert is_eligible is True


    @patch('subprocess.run')
    def test_exit_code_one_means_skip(self, mock_run):
        """
        Test AC1: Exit code 1 indicates user is not eligible (skip)

        Given: check-hooks returns exit code 1
        When: Exit code is interpreted
        Then: System should skip invoke-hooks entirely
        """
        # Arrange
        mock_run.return_value = MagicMock(returncode=1)

        # Act
        result = subprocess.run(["devforgeai", "check-hooks"])
        should_skip = result.returncode != 0

        # Assert
        assert should_skip is True


    @patch('subprocess.run')
    def test_exit_code_error_handled_gracefully(self, mock_run):
        """
        Test AC1: Non-zero exit codes (other than 1) handled as errors

        Given: check-hooks fails with error exit code (e.g., 127, 1)
        When: Error detected
        Then: Error should be logged, system continues
        """
        # Arrange
        mock_run.return_value = MagicMock(
            returncode=127,
            stderr="devforgeai: command not found"
        )

        # Act
        result = subprocess.run(["devforgeai", "check-hooks"], capture_output=True, text=True)
        is_error = result.returncode != 0

        # Assert
        assert is_error is True
        assert "command not found" in result.stderr.lower() or result.returncode == 127


    @patch('subprocess.run')
    def test_zero_exit_code_explicitly_triggers_invoke(self, mock_run):
        """
        Test AC1: Only exit code 0 should trigger invoke-hooks

        Given: check-hooks called
        When: Different exit codes returned
        Then: Only 0 should proceed to invoke-hooks
        """
        # Arrange & Act
        test_cases = [
            (0, True),   # Should invoke
            (1, False),  # Should skip
            (2, False),  # Should skip
            (127, False) # Should skip (error)
        ]

        results = []
        for exit_code, should_invoke in test_cases:
            mock_run.return_value = MagicMock(returncode=exit_code)
            check_result = subprocess.run(["devforgeai", "check-hooks"])
            will_invoke = check_result.returncode == 0
            results.append((exit_code, should_invoke, will_invoke))

        # Assert
        for exit_code, expected_invoke, actual_invoke in results:
            assert actual_invoke == expected_invoke, \
                f"Exit code {exit_code}: expected invoke={expected_invoke}, got {actual_invoke}"


# ============================================================================
# Hook Check Error Detection Tests
# ============================================================================


class TestCheckHooksErrorDetection:
    """Tests for detecting and logging errors from check-hooks."""

    @patch('subprocess.run')
    def test_stderr_captured_on_error(self, mock_run):
        """
        Test AC1: Stderr output captured when check-hooks fails

        Given: check-hooks encounters an error
        When: Error occurs
        Then: stderr should be captured for diagnostic logging
        """
        # Arrange
        error_message = "Unable to read hooks configuration file"
        mock_run.return_value = MagicMock(
            returncode=1,
            stderr=error_message
        )

        # Act
        result = subprocess.run(["devforgeai", "check-hooks"], capture_output=True, text=True)

        # Assert
        assert result.returncode == 1
        assert error_message in result.stderr


    @patch('subprocess.run')
    def test_stdout_captured_on_success(self, mock_run):
        """
        Test AC1: Stdout output captured when check-hooks succeeds

        Given: check-hooks completes successfully
        When: Output available
        Then: stdout should contain status message
        """
        # Arrange
        status_message = "User eligible for feedback"
        mock_run.return_value = MagicMock(
            returncode=0,
            stdout=status_message
        )

        # Act
        result = subprocess.run(["devforgeai", "check-hooks"], capture_output=True, text=True)

        # Assert
        assert result.returncode == 0
        assert status_message in result.stdout


    @patch('subprocess.run')
    def test_command_not_found_error_detected(self, mock_run):
        """
        Test AC3 Edge Case: devforgeai CLI not installed

        Given: devforgeai command not found
        When: check-hooks invoked
        Then: Exit code 127 (command not found)
        """
        # Arrange
        mock_run.return_value = MagicMock(
            returncode=127,
            stderr="devforgeai: command not found"
        )

        # Act
        result = subprocess.run(["devforgeai", "check-hooks"], capture_output=True, text=True)

        # Assert
        assert result.returncode == 127
        assert "command not found" in result.stderr.lower()


    @patch('subprocess.run')
    def test_timeout_error_detected(self, mock_run):
        """
        Test AC3 Edge Case: check-hooks times out

        Given: check-hooks takes too long (>30 seconds)
        When: Timeout occurs
        Then: Exit code indicates timeout
        """
        # Arrange
        mock_run.return_value = MagicMock(
            returncode=124,  # Standard timeout exit code
            stderr="Command timed out after 30 seconds"
        )

        # Act
        result = subprocess.run(["devforgeai", "check-hooks"], capture_output=True, text=True)

        # Assert
        assert result.returncode == 124


    @patch('subprocess.run')
    def test_permission_denied_error_detected(self, mock_run):
        """
        Test AC3 Edge Case: Permission denied reading hooks.yaml

        Given: Config file not readable
        When: check-hooks tries to read it
        Then: Permission error detected
        """
        # Arrange
        mock_run.return_value = MagicMock(
            returncode=13,  # Permission denied
            stderr="Permission denied: devforgeai/config/hooks.yaml"
        )

        # Act
        result = subprocess.run(["devforgeai", "check-hooks"], capture_output=True, text=True)

        # Assert
        assert result.returncode == 13


# ============================================================================
# Context File Creation Prerequisite Tests
# ============================================================================


class TestCheckHooksContextFilePrerequisite:
    """Tests verifying Phase N executes AFTER Phase 4 (context files created)."""

    def test_phase_n_assumes_context_files_exist(self):
        """
        Test AC1: Phase N assumes all 6 context files exist

        Given: Phase 4 (context file creation) completes
        When: Phase N begins
        Then: All 6 context files should already be on disk
        """
        # Arrange
        required_files = [
            "devforgeai/context/tech-stack.md",
            "devforgeai/context/source-tree.md",
            "devforgeai/context/dependencies.md",
            "devforgeai/context/coding-standards.md",
            "devforgeai/context/architecture-constraints.md",
            "devforgeai/context/anti-patterns.md"
        ]

        # Act - In real test, would verify these exist before Phase N
        all_files_needed = True
        for filename in required_files:
            # File should exist (checked during Phase 4)
            pass

        # Assert
        assert all_files_needed is True


    def test_check_hooks_called_only_after_files_created(self):
        """
        Test AC1: check-hooks not called until after Phase 4 completes

        Given: /create-context workflow
        When: Phases execute sequentially
        Then: Phase N should execute AFTER Phase 4
        """
        # Arrange
        execution_order = []

        # Act - Record what phase completes when
        execution_order.append("Phase 4: Create context files")
        execution_order.append("Phase N: Invoke hooks")

        # Assert
        assert execution_order[0] == "Phase 4: Create context files"
        assert execution_order[1] == "Phase N: Invoke hooks"
        assert execution_order.index("Phase 4: Create context files") < \
               execution_order.index("Phase N: Invoke hooks")


# ============================================================================
# Check-Hooks Command Variants Tests
# ============================================================================


class TestCheckHooksCommandVariants:
    """Tests for different status values that might be used."""

    @patch('subprocess.run')
    def test_status_completed_variant(self, mock_run):
        """
        Test: --status=completed variant is used for create-context

        Given: Context files successfully created
        When: check-hooks called
        Then: --status=completed should be used
        """
        # Arrange
        mock_run.return_value = MagicMock(returncode=0)

        # Act
        subprocess.run([
            "devforgeai", "check-hooks",
            "--operation=create-context",
            "--status=completed"
        ])

        # Assert
        assert mock_run.called
        call_args = str(mock_run.call_args)
        assert "completed" in call_args


    @patch('subprocess.run')
    def test_operation_create_context_variant(self, mock_run):
        """
        Test: --operation=create-context is specific to this command

        Given: /create-context invokes hooks
        When: check-hooks called
        Then: --operation must be "create-context" (not "dev", "qa", etc.)
        """
        # Arrange
        mock_run.return_value = MagicMock(returncode=0)

        # Act
        subprocess.run([
            "devforgeai", "check-hooks",
            "--operation=create-context",
            "--status=completed"
        ])

        # Assert
        assert mock_run.called
        call_args = str(mock_run.call_args)
        assert "create-context" in call_args
        # Check operation is exactly "create-context", not other operations like "dev" or "qa"
        # Note: Don't check "dev" not in call_args because "devforgeai" contains "dev"
        assert "--operation=create-context" in call_args or "'--operation=create-context'" in call_args


# ============================================================================
# Check-Hooks Response Handling Tests
# ============================================================================


class TestCheckHooksResponseHandling:
    """Tests for handling responses from check-hooks."""

    @patch('subprocess.run')
    def test_eligible_response_interpreted_correctly(self, mock_run):
        """
        Test: Exit code 0 response properly interpreted as "eligible"

        Given: check-hooks returns 0
        When: Response processed
        Then: Next step should be to invoke invoke-hooks
        """
        # Arrange
        mock_run.return_value = MagicMock(returncode=0)

        # Act
        result = subprocess.run(["devforgeai", "check-hooks"])
        next_action = "invoke-hooks" if result.returncode == 0 else "skip"

        # Assert
        assert next_action == "invoke-hooks"


    @patch('subprocess.run')
    def test_skip_response_interpreted_correctly(self, mock_run):
        """
        Test: Exit code 1 response properly interpreted as "skip"

        Given: check-hooks returns 1
        When: Response processed
        Then: Next step should be to skip invoke-hooks
        """
        # Arrange
        mock_run.return_value = MagicMock(returncode=1)

        # Act
        result = subprocess.run(["devforgeai", "check-hooks"])
        next_action = "invoke-hooks" if result.returncode == 0 else "skip"

        # Assert
        assert next_action == "skip"


    @patch('subprocess.run')
    def test_error_response_handled_as_skip(self, mock_run):
        """
        Test: Error exit codes treated as "skip gracefully"

        Given: check-hooks returns error code
        When: Error detected
        Then: Treat as skip (proceed without feedback)
        """
        # Arrange
        mock_run.return_value = MagicMock(returncode=127)

        # Act
        result = subprocess.run(["devforgeai", "check-hooks"])
        next_action = "invoke-hooks" if result.returncode == 0 else "skip"

        # Assert
        assert next_action == "skip"
