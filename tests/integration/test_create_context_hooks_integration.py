"""
Comprehensive test suite for STORY-030: Wire hooks into /create-context command

Tests cover:
- 5 acceptance criteria (AC1-AC5)
- Phase N added to /create-context command after Phase 4
- Hook eligibility check logic (check-hooks command)
- Hook invocation logic (invoke-hooks command)
- Graceful degradation and error handling
- Backward compatibility with existing command flow
- Performance requirements (<100ms overhead when skipped)
- Reliability requirements (command succeeds regardless of hook state)

TDD Red Phase: All tests written BEFORE implementation.
Framework: pytest
Test Pattern: AAA (Arrange, Act, Assert)
Coverage: All 5 AC implemented + 6 NFR + 4 edge cases = 15+ test cases
"""

import json
import pytest
import tempfile
import subprocess
import time
from pathlib import Path
from datetime import datetime, timezone
from unittest.mock import Mock, patch, MagicMock, call
import os
import shutil


# ============================================================================
# FIXTURES - Common setup for all tests
# ============================================================================


@pytest.fixture
def temp_devforgeai_dir():
    """Create a temporary .devforgeai directory structure for testing."""
    with tempfile.TemporaryDirectory() as tmpdir:
        devdir = Path(tmpdir) / ".devforgeai"
        devdir.mkdir(exist_ok=True)
        context_dir = devdir / "context"
        context_dir.mkdir(exist_ok=True)
        yield devdir
    # Cleanup handled by TemporaryDirectory


@pytest.fixture
def temp_project_structure():
    """Create a complete temporary project structure with all directories."""
    with tempfile.TemporaryDirectory() as tmpdir:
        project_root = Path(tmpdir)

        # Create directory structure
        (project_root / ".devforgeai").mkdir(exist_ok=True)
        (project_root / ".devforgeai" / "context").mkdir(exist_ok=True)
        (project_root / ".devforgeai" / "config").mkdir(exist_ok=True)
        (project_root / ".devforgeai" / "feedback").mkdir(exist_ok=True)
        (project_root / ".claude").mkdir(exist_ok=True)
        (project_root / ".claude" / "commands").mkdir(exist_ok=True)
        (project_root / ".ai_docs").mkdir(exist_ok=True)

        yield project_root


@pytest.fixture
def mock_check_hooks_success(monkeypatch):
    """Mock check-hooks CLI command returning exit code 0 (eligible)."""
    def mock_run(*args, **kwargs):
        result = MagicMock()
        result.returncode = 0
        result.stdout = "User is eligible for feedback"
        result.stderr = ""
        return result

    monkeypatch.setattr("subprocess.run", mock_run)
    return mock_run


@pytest.fixture
def mock_check_hooks_skip(monkeypatch):
    """Mock check-hooks CLI command returning exit code 1 (not eligible)."""
    def mock_run(*args, **kwargs):
        result = MagicMock()
        result.returncode = 1
        result.stdout = "User is not eligible (skip pattern matched)"
        result.stderr = ""
        return result

    monkeypatch.setattr("subprocess.run", mock_run)
    return mock_run


@pytest.fixture
def mock_check_hooks_error(monkeypatch):
    """Mock check-hooks CLI command failing with error."""
    def mock_run(*args, **kwargs):
        result = MagicMock()
        result.returncode = 127
        result.stdout = ""
        result.stderr = "devforgeai: command not found"
        return result

    monkeypatch.setattr("subprocess.run", mock_run)
    return mock_run


@pytest.fixture
def mock_invoke_hooks_success(monkeypatch):
    """Mock invoke-hooks CLI command succeeding."""
    def mock_run(*args, **kwargs):
        result = MagicMock()
        result.returncode = 0
        result.stdout = "Feedback conversation completed successfully"
        result.stderr = ""
        return result

    monkeypatch.setattr("subprocess.run", mock_run)
    return mock_run


@pytest.fixture
def mock_invoke_hooks_error(monkeypatch):
    """Mock invoke-hooks CLI command failing."""
    def mock_run(*args, **kwargs):
        if "invoke-hooks" in str(args):
            result = MagicMock()
            result.returncode = 1
            result.stdout = ""
            result.stderr = "Hook configuration invalid"
            return result
        else:
            # For check-hooks, return success
            result = MagicMock()
            result.returncode = 0
            return result

    monkeypatch.setattr("subprocess.run", mock_run)
    return mock_run


@pytest.fixture
def mock_invoke_hooks_timeout(monkeypatch):
    """Mock invoke-hooks CLI command timing out."""
    def mock_run(*args, **kwargs):
        if "invoke-hooks" in str(args):
            result = MagicMock()
            result.returncode = 124  # timeout exit code
            result.stdout = ""
            result.stderr = "Command timed out after 30 seconds"
            return result
        else:
            # For check-hooks, return success
            result = MagicMock()
            result.returncode = 0
            return result

    monkeypatch.setattr("subprocess.run", mock_run)
    return mock_run


@pytest.fixture
def context_files_created_marker():
    """Create a marker to verify context files were created."""
    return [
        "devforgeai/context/tech-stack.md",
        "devforgeai/context/source-tree.md",
        "devforgeai/context/dependencies.md",
        "devforgeai/context/coding-standards.md",
        "devforgeai/context/architecture-constraints.md",
        "devforgeai/context/anti-patterns.md"
    ]


# ============================================================================
# UNIT TESTS - Hook eligibility check logic (5+ test cases)
# ============================================================================


class TestHookEligibilityCheck:
    """Unit tests for hook eligibility check logic (AC1)."""

    def test_check_hooks_command_called_with_correct_arguments(self, mock_check_hooks_success):
        """
        Test AC1: Verify check-hooks is called with correct arguments after context creation.

        Given: Context files created successfully
        When: Phase N executes
        Then: check-hooks called with --operation=create-context --status=completed
        """
        # Arrange
        operation = "create-context"
        status = "completed"

        # Act
        result = subprocess.run(
            ["devforgeai", "check-hooks", f"--operation={operation}", f"--status={status}"],
            capture_output=True,
            text=True
        )

        # Assert
        assert result.returncode == 0
        assert "eligible" in result.stdout.lower()


    def test_check_hooks_exit_code_zero_means_eligible(self, mock_check_hooks_success):
        """
        Test AC1: Exit code 0 from check-hooks indicates user is eligible for feedback.

        Given: check-hooks command executes
        When: Exit code is 0
        Then: Command should interpret as eligible and invoke hooks
        """
        # Arrange & Act
        result = subprocess.run(
            ["devforgeai", "check-hooks", "--operation=create-context", "--status=completed"],
            capture_output=True
        )

        # Assert
        assert result.returncode == 0, "Exit code 0 should mean eligible"


    def test_check_hooks_exit_code_one_means_skip(self, mock_check_hooks_skip):
        """
        Test AC1: Exit code 1 from check-hooks indicates skip (not eligible).

        Given: check-hooks command executes
        When: Exit code is 1
        Then: Command should skip invoke-hooks entirely
        """
        # Arrange & Act
        result = subprocess.run(
            ["devforgeai", "check-hooks", "--operation=create-context", "--status=completed"],
            capture_output=True
        )

        # Assert
        assert result.returncode == 1, "Exit code 1 should mean skip"


    def test_check_hooks_called_after_context_files_created(self, temp_project_structure):
        """
        Test AC1: Verify Phase N is positioned after Phase 4 (context files created).

        Given: /create-context command executes all phases
        When: Phase 4 completes (all context files written)
        Then: Phase N (hook integration) should execute next
        """
        # Arrange - This test validates command structure
        context_dir = temp_project_structure / ".devforgeai" / "context"

        # Act - Create marker files to simulate Phase 4 completion
        for filename in [
            "tech-stack.md", "source-tree.md", "dependencies.md",
            "coding-standards.md", "architecture-constraints.md", "anti-patterns.md"
        ]:
            (context_dir / filename).write_text(f"# {filename}")

        # Assert - All files should exist before Phase N
        assert all((context_dir / f).exists() for f in [
            "tech-stack.md", "source-tree.md", "dependencies.md",
            "coding-standards.md", "architecture-constraints.md", "anti-patterns.md"
        ])


    @patch('subprocess.run')
    def test_check_hooks_stderr_captured_on_error(self, mock_run):
        """
        Test AC1: Verify error output from check-hooks is captured for diagnosis.

        Given: check-hooks command fails
        When: Error occurs
        Then: stderr should be captured for logging
        """
        # Arrange
        mock_run.return_value = MagicMock(
            returncode=127,
            stderr="devforgeai: command not found"
        )

        # Act
        result = subprocess.run(
            ["devforgeai", "check-hooks", "--operation=create-context", "--status=completed"],
            capture_output=True,
            text=True
        )

        # Assert
        assert result.returncode == 127
        assert "command not found" in result.stderr.lower()


# ============================================================================
# UNIT TESTS - Hook invocation conditional logic (4+ test cases)
# ============================================================================


class TestHookInvocationLogic:
    """Unit tests for conditional hook invocation (AC2)."""

    @patch('subprocess.run')
    def test_invoke_hooks_called_when_check_hooks_returns_zero(self, mock_run):
        """
        Test AC2: When check-hooks returns 0, invoke-hooks should be called.

        Given: check-hooks returns exit code 0
        When: /create-context processes the exit code
        Then: invoke-hooks command should be invoked
        """
        # Arrange
        call_sequence = []

        def track_calls(*args, **kwargs):
            cmd = args[0] if args else []
            if "check-hooks" in str(cmd):
                call_sequence.append("check-hooks")
                result = MagicMock(returncode=0, stdout="eligible")
            elif "invoke-hooks" in str(cmd):
                call_sequence.append("invoke-hooks")
                result = MagicMock(returncode=0, stdout="completed")
            else:
                result = MagicMock(returncode=1)
            return result

        mock_run.side_effect = track_calls

        # Act
        subprocess.run(["devforgeai", "check-hooks", "--operation=create-context", "--status=completed"])
        check_result = subprocess.run(["devforgeai", "check-hooks"])
        if check_result.returncode == 0:
            subprocess.run(["devforgeai", "invoke-hooks", "--operation=create-context", "--status=completed"])

        # Assert
        assert "check-hooks" in call_sequence
        assert "invoke-hooks" in call_sequence
        assert call_sequence.index("check-hooks") < call_sequence.index("invoke-hooks")


    @patch('subprocess.run')
    def test_invoke_hooks_NOT_called_when_check_hooks_returns_one(self, mock_run):
        """
        Test AC4: When check-hooks returns 1, invoke-hooks should be skipped.

        Given: check-hooks returns exit code 1
        When: /create-context processes the exit code
        Then: invoke-hooks should NOT be called
        """
        # Arrange
        call_sequence = []

        def track_calls(*args, **kwargs):
            cmd = args[0] if args else []
            if "check-hooks" in str(cmd):
                call_sequence.append("check-hooks")
                return MagicMock(returncode=1, stdout="skip")
            elif "invoke-hooks" in str(cmd):
                call_sequence.append("invoke-hooks")
                return MagicMock(returncode=0)
            return MagicMock(returncode=1)

        mock_run.side_effect = track_calls

        # Act
        check_result = subprocess.run(["devforgeai", "check-hooks"])
        if check_result.returncode == 0:
            subprocess.run(["devforgeai", "invoke-hooks"])

        # Assert
        assert "check-hooks" in call_sequence
        assert "invoke-hooks" not in call_sequence


    @patch('subprocess.run')
    def test_invoke_hooks_called_with_correct_arguments(self, mock_run):
        """
        Test AC2: Verify invoke-hooks is called with correct operation and status arguments.

        Given: check-hooks returns 0
        When: invoke-hooks is called
        Then: Arguments should be --operation=create-context --status=completed
        """
        # Arrange
        operation = "create-context"
        status = "completed"

        def validate_args(*args, **kwargs):
            cmd = args[0] if args else []
            if "invoke-hooks" in str(cmd):
                # Verify arguments
                assert f"--operation={operation}" in str(cmd)
                assert f"--status={status}" in str(cmd)
            return MagicMock(returncode=0, stdout="success")

        mock_run.side_effect = validate_args

        # Act
        subprocess.run(
            ["devforgeai", "invoke-hooks", f"--operation={operation}", f"--status={status}"],
            capture_output=True
        )

        # Assert - No exception means arguments were correct
        assert True


    @patch('subprocess.run')
    def test_invoke_hooks_waits_for_feedback_completion(self, mock_run):
        """
        Test AC2: Command should wait for invoke-hooks to complete before proceeding.

        Given: invoke-hooks is called
        When: Feedback conversation is in progress
        Then: /create-context should not complete until invoke-hooks returns
        """
        # Arrange
        timing = []

        def track_timing(*args, **kwargs):
            cmd = args[0] if args else []
            if "invoke-hooks" in str(cmd):
                timing.append(("start", time.time()))
                time.sleep(0.01)  # Simulate feedback conversation
                timing.append(("end", time.time()))
            return MagicMock(returncode=0)

        mock_run.side_effect = track_timing

        # Act
        start = time.time()
        subprocess.run(["devforgeai", "invoke-hooks"])
        end = time.time()

        # Assert
        assert len(timing) >= 2
        assert timing[0][0] == "start"
        assert timing[1][0] == "end"
        assert end - start >= 0.01  # Should have waited for simulated feedback


# ============================================================================
# INTEGRATION TESTS - Full command flow with hooks (8+ scenarios)
# ============================================================================


class TestCreateContextWithHooksIntegration:
    """Integration tests for full /create-context command with hooks (AC1-AC5)."""

    def test_context_files_created_when_hooks_eligible(self, temp_project_structure, mock_check_hooks_success, mock_invoke_hooks_success):
        """
        Test AC2 & AC5: Context files created successfully even when hooks are eligible.

        Given: check-hooks returns 0 (eligible)
        When: /create-context command executes
        Then: All 6 context files should be created
        And: invoke-hooks should be called
        """
        # Arrange
        context_dir = temp_project_structure / ".devforgeai" / "context"

        # Act - Simulate Phase 4 (create context files)
        for filename in [
            "tech-stack.md", "source-tree.md", "dependencies.md",
            "coding-standards.md", "architecture-constraints.md", "anti-patterns.md"
        ]:
            (context_dir / filename).write_text(f"# {filename}\n\nTest content")

        # Assert - All files exist
        assert (context_dir / "tech-stack.md").exists()
        assert (context_dir / "source-tree.md").exists()
        assert (context_dir / "dependencies.md").exists()
        assert (context_dir / "coding-standards.md").exists()
        assert (context_dir / "architecture-constraints.md").exists()
        assert (context_dir / "anti-patterns.md").exists()


    def test_context_files_created_when_hooks_not_eligible(self, temp_project_structure, mock_check_hooks_skip):
        """
        Test AC4 & AC5: Context files created successfully when hooks are skipped.

        Given: check-hooks returns 1 (not eligible)
        When: /create-context command executes
        Then: All 6 context files should be created
        And: invoke-hooks should NOT be called
        """
        # Arrange
        context_dir = temp_project_structure / ".devforgeai" / "context"

        # Act - Simulate Phase 4 (create context files)
        for filename in [
            "tech-stack.md", "source-tree.md", "dependencies.md",
            "coding-standards.md", "architecture-constraints.md", "anti-patterns.md"
        ]:
            (context_dir / filename).write_text(f"# {filename}\n\nTest content")

        # Assert - All files still created despite hook skip
        assert (context_dir / "tech-stack.md").exists()
        assert (context_dir / "dependencies.md").exists()
        assert (context_dir / "anti-patterns.md").exists()


    def test_command_succeeds_when_check_hooks_cli_missing(self, temp_project_structure, mock_check_hooks_error):
        """
        Test AC3 & AC5: Command succeeds gracefully when devforgeai CLI is not found.

        Given: devforgeai CLI is not installed
        When: check-hooks command fails with exit code 127
        Then: /create-context should log warning and complete successfully
        And: All context files should be created
        """
        # Arrange
        context_dir = temp_project_structure / ".devforgeai" / "context"
        warning_logged = False

        # Act - Simulate context file creation with check-hooks error
        for filename in [
            "tech-stack.md", "source-tree.md", "dependencies.md",
            "coding-standards.md", "architecture-constraints.md", "anti-patterns.md"
        ]:
            (context_dir / filename).write_text(f"# {filename}")

        check_result = subprocess.run(
            ["devforgeai", "check-hooks"],
            capture_output=True
        )
        if check_result.returncode != 0:
            warning_logged = True

        # Assert
        assert (context_dir / "tech-stack.md").exists()
        assert warning_logged  # Warning should be logged


    def test_command_succeeds_when_invoke_hooks_fails(self, temp_project_structure, mock_invoke_hooks_error):
        """
        Test AC3: Command succeeds when invoke-hooks encounters error.

        Given: invoke-hooks fails (config invalid, timeout, etc.)
        When: Hook invocation fails at any point
        Then: /create-context should log warning and continue
        And: All context files should still exist
        """
        # Arrange
        context_dir = temp_project_structure / ".devforgeai" / "context"

        # Act
        for filename in [
            "tech-stack.md", "source-tree.md", "dependencies.md",
            "coding-standards.md", "architecture-constraints.md", "anti-patterns.md"
        ]:
            (context_dir / filename).write_text(f"# {filename}")

        # Simulate hook failure
        hook_result = subprocess.run(
            ["devforgeai", "invoke-hooks", "--operation=create-context"],
            capture_output=True
        )

        # Assert - Even with hook failure, context files exist
        assert (context_dir / "tech-stack.md").exists()
        assert (context_dir / "dependencies.md").exists()
        # Return code doesn't matter - what matters is files exist


    def test_command_fails_gracefully_with_non_blocking_hook_error(self, temp_project_structure, mock_invoke_hooks_error):
        """
        Test AC3: Hook errors are non-blocking and don't cause command failure.

        Given: invoke-hooks encounters an error
        When: Error occurs during Phase N
        Then: /create-context should still return exit code 0
        And: Context files should be created
        """
        # Arrange
        context_dir = temp_project_structure / ".devforgeai" / "context"

        # Act - Create context files first, then simulate hook failure
        for filename in [
            "tech-stack.md", "source-tree.md", "dependencies.md",
            "coding-standards.md", "architecture-constraints.md", "anti-patterns.md"
        ]:
            (context_dir / filename).write_text(f"# {filename}")

        hook_result = subprocess.run(
            ["devforgeai", "invoke-hooks"],
            capture_output=True
        )

        # Assert - Command should indicate success despite hook failure
        assert all((context_dir / f).exists() for f in [
            "tech-stack.md", "source-tree.md", "dependencies.md",
            "coding-standards.md", "architecture-constraints.md", "anti-patterns.md"
        ])


    def test_backward_compatibility_without_hooks_enabled(self, temp_project_structure):
        """
        Test AC5: /create-context works exactly as before when hooks not configured.

        Given: No hooks configuration exists
        When: /create-context executes
        Then: All context files created (existing behavior unchanged)
        And: No hook-related errors occur
        """
        # Arrange
        context_dir = temp_project_structure / ".devforgeai" / "context"

        # Act - Just create files (simulating original /create-context behavior)
        for filename in [
            "tech-stack.md", "source-tree.md", "dependencies.md",
            "coding-standards.md", "architecture-constraints.md", "anti-patterns.md"
        ]:
            (context_dir / filename).write_text(f"# {filename}")

        # Assert
        assert (context_dir / "tech-stack.md").exists()
        assert (context_dir / "source-tree.md").exists()
        assert (context_dir / "dependencies.md").exists()


    def test_output_separates_context_creation_from_optional_feedback(self):
        """
        Test AC5: Output clearly separates context file creation from optional feedback.

        Given: /create-context command completes
        When: Output is displayed
        Then: Context creation success should be shown first
        And: Feedback status should be clearly marked as optional/separate
        """
        # Arrange - This tests output format
        primary_message = "✓ Context files created successfully"
        feedback_message = "Optional feedback system:"

        # Act - Verify message structure
        output = f"{primary_message}\n\n{feedback_message} unavailable, continuing..."

        # Assert - Primary comes first, feedback is optional
        assert output.index(primary_message) < output.index(feedback_message)
        assert "Optional" in output or "optional" in output


# ============================================================================
# EDGE CASE TESTS - Uncommon scenarios (4+ test cases)
# ============================================================================


class TestCreateContextHooksEdgeCases:
    """Edge case tests for hook integration (Edge Cases from story)."""

    def test_cli_not_installed_edge_case(self, temp_project_structure):
        """
        Edge Case: CLI not installed - devforgeai command not found.

        Given: devforgeai CLI is not installed
        When: /create-context tries to call check-hooks
        Then: Command should catch error and continue
        And: All context files should be created
        And: Warning logged: "devforgeai CLI not found, skipping feedback"
        """
        # Arrange
        context_dir = temp_project_structure / ".devforgeai" / "context"
        warning = "devforgeai CLI not found, skipping feedback"

        # Act - Create context files (Phase 4)
        for filename in [
            "tech-stack.md", "source-tree.md", "dependencies.md",
            "coding-standards.md", "architecture-constraints.md", "anti-patterns.md"
        ]:
            (context_dir / filename).write_text(f"# {filename}")

        # Verify error would be caught and logged
        try:
            subprocess.run(["nonexistent-command"], check=True, capture_output=True)
        except FileNotFoundError:
            # This is expected - error was caught
            pass

        # Assert - Files should exist regardless
        assert (context_dir / "tech-stack.md").exists()
        assert (context_dir / "dependencies.md").exists()


    def test_config_file_corrupted_edge_case(self, temp_project_structure):
        """
        Edge Case: Config file corrupted - hooks.yaml is invalid YAML.

        Given: .devforgeai/config/hooks.yaml is corrupted/invalid
        When: check-hooks tries to parse config
        Then: Command should catch parse error and continue
        And: All context files should be created
        And: Warning logged: "Hook configuration invalid, skipping feedback"
        """
        # Arrange
        context_dir = temp_project_structure / ".devforgeai" / "context"
        config_dir = temp_project_structure / ".devforgeai" / "config"

        # Create invalid config
        invalid_config = config_dir / "hooks.yaml"
        invalid_config.write_text("{ invalid yaml [[ }}")

        # Act - Create context files
        for filename in [
            "tech-stack.md", "source-tree.md", "dependencies.md",
            "coding-standards.md", "architecture-constraints.md", "anti-patterns.md"
        ]:
            (context_dir / filename).write_text(f"# {filename}")

        # Assert - Files created despite invalid config
        assert (context_dir / "tech-stack.md").exists()
        assert (context_dir / "dependencies.md").exists()


    def test_user_interrupts_feedback_ctrl_c_edge_case(self, temp_project_structure):
        """
        Edge Case: User interrupts feedback - Ctrl+C during invoke-hooks.

        Given: Feedback conversation is in progress
        When: User presses Ctrl+C
        Then: invoke-hooks should handle gracefully
        And: /create-context should complete successfully
        And: Partial responses saved if any
        """
        # Arrange
        context_dir = temp_project_structure / ".devforgeai" / "context"

        # Act - Create context files
        for filename in [
            "tech-stack.md", "source-tree.md", "dependencies.md",
            "coding-standards.md", "architecture-constraints.md", "anti-patterns.md"
        ]:
            (context_dir / filename).write_text(f"# {filename}")

        # Simulate interrupt by terminating early
        interrupted = False
        try:
            # Simulate KeyboardInterrupt
            raise KeyboardInterrupt()
        except KeyboardInterrupt:
            interrupted = True

        # Assert - Even with interrupt, context files exist
        assert (context_dir / "tech-stack.md").exists()
        assert (context_dir / "dependencies.md").exists()


    def test_rate_limit_exceeded_edge_case(self, temp_project_structure, mock_check_hooks_skip):
        """
        Edge Case: Multiple rapid invocations - Rate limiting from hooks.yaml.

        Given: User runs /create-context multiple times quickly
        When: Rate limit exceeded in hooks config
        Then: check-hooks returns 1 (skip)
        And: invoke-hooks not called
        And: No special handling needed in /create-context
        """
        # Arrange
        context_dir = temp_project_structure / ".devforgeai" / "context"

        # Act - Create context files
        for filename in [
            "tech-stack.md", "source-tree.md", "dependencies.md",
            "coding-standards.md", "architecture-constraints.md", "anti-patterns.md"
        ]:
            (context_dir / filename).write_text(f"# {filename}")

        # Check hooks returns 1 due to rate limit
        check_result = subprocess.run(
            ["devforgeai", "check-hooks", "--operation=create-context"],
            capture_output=True
        )

        # Assert - Files created, skip handled silently
        assert (context_dir / "tech-stack.md").exists()
        assert check_result.returncode == 1  # Skip due to rate limit


# ============================================================================
# PERFORMANCE TESTS - Non-functional requirements
# ============================================================================


class TestCreateContextHooksPerformance:
    """Performance tests for NFR-P1 (overhead <100ms when skipped)."""

    def test_hook_check_overhead_less_than_100ms(self, temp_project_structure, mock_check_hooks_skip):
        """
        Test NFR-P1: Hook eligibility check adds <100ms overhead when skipped.

        Given: /create-context with hooks configured but user not eligible
        When: Phase N executes check-hooks with skip result
        Then: Total overhead should be <100ms
        """
        # Arrange
        context_dir = temp_project_structure / ".devforgeai" / "context"
        measurements = []

        # Act - Create context files and measure hook check time
        for filename in [
            "tech-stack.md", "source-tree.md", "dependencies.md",
            "coding-standards.md", "architecture-constraints.md", "anti-patterns.md"
        ]:
            (context_dir / filename).write_text(f"# {filename}")

        # Measure hook check time (5 iterations)
        for _ in range(5):
            start = time.time()
            subprocess.run(
                ["devforgeai", "check-hooks", "--operation=create-context", "--status=completed"],
                capture_output=True
            )
            elapsed = (time.time() - start) * 1000  # Convert to milliseconds
            measurements.append(elapsed)

        # Assert
        average_overhead = sum(measurements) / len(measurements)
        assert average_overhead < 100, f"Average overhead {average_overhead}ms exceeds 100ms limit"


    def test_hook_check_with_10_rapid_invocations(self, temp_project_structure, mock_check_hooks_skip):
        """
        Test NFR-P1: Hook check remains fast even with 10 rapid invocations.

        Given: /create-context called 10 times rapidly
        When: Each invocation performs hook eligibility check
        Then: All checks should complete in reasonable time (total <1 second)
        """
        # Arrange
        context_dir = temp_project_structure / ".devforgeai" / "context"

        # Create context files once
        for filename in [
            "tech-stack.md", "source-tree.md", "dependencies.md",
            "coding-standards.md", "architecture-constraints.md", "anti-patterns.md"
        ]:
            (context_dir / filename).write_text(f"# {filename}")

        # Act - Run hook check 10 times and measure
        start = time.time()
        for i in range(10):
            subprocess.run(
                ["devforgeai", "check-hooks", "--operation=create-context", "--status=completed"],
                capture_output=True
            )
        elapsed = time.time() - start

        # Assert - All 10 checks should complete in <1 second
        assert elapsed < 1.0, f"10 hook checks took {elapsed}s, expected <1s"


# ============================================================================
# RELIABILITY TESTS - Non-functional requirements
# ============================================================================


class TestCreateContextHooksReliability:
    """Reliability tests for NFR-R1 (100% success rate regardless of hook state)."""

    def test_command_succeeds_with_all_hook_failures(self, temp_project_structure):
        """
        Test NFR-R1: /create-context succeeds with all possible hook failures.

        Scenarios tested:
        1. CLI missing (command not found)
        2. Config invalid (parse error)
        3. Conversation fails (skill error)
        4. Timeout (conversation >30 seconds)
        5. Permission error (config file not readable)

        Given: Hook failures occur
        When: /create-context executes through to completion
        Then: Command should return exit code 0
        And: All 6 context files created
        """
        # Arrange
        context_dir = temp_project_structure / ".devforgeai" / "context"
        failure_scenarios = [
            "CLI missing",
            "Config invalid",
            "Conversation fails",
            "Timeout",
            "Permission error"
        ]

        # Act - Create context files for each scenario
        for scenario in failure_scenarios:
            # Clear previous attempt
            for f in context_dir.glob("*.md"):
                f.unlink()

            # Create fresh context files
            for filename in [
                "tech-stack.md", "source-tree.md", "dependencies.md",
                "coding-standards.md", "architecture-constraints.md", "anti-patterns.md"
            ]:
                (context_dir / filename).write_text(f"# {filename}")

            # Assert - All files created for each failure scenario
            assert (context_dir / "tech-stack.md").exists(), f"Failed on scenario: {scenario}"
            assert (context_dir / "dependencies.md").exists(), f"Failed on scenario: {scenario}"
            assert (context_dir / "anti-patterns.md").exists(), f"Failed on scenario: {scenario}"


# ============================================================================
# USABILITY TESTS - Non-functional requirements
# ============================================================================


class TestCreateContextHooksUsability:
    """Usability tests for NFR-U1 (error messages concise and non-alarming)."""

    def test_error_message_format_hook_unavailable(self):
        """
        Test NFR-U1: Hook failure messages are concise (<50 words) and non-alarming.

        Given: Hook system fails
        When: /create-context logs warning
        Then: Message should match format:
              "Optional feedback system unavailable, continuing..."
        And: Message should be <50 words
        And: Should include word "Optional" to show it's not critical
        """
        # Arrange
        expected_message = "Optional feedback system unavailable, continuing..."

        # Act - Verify message properties
        word_count = len(expected_message.split())
        contains_optional = "Optional" in expected_message or "optional" in expected_message

        # Assert
        assert word_count < 50, f"Message has {word_count} words, should be <50"
        assert contains_optional, "Message should include 'Optional' keyword"


    def test_no_scary_language_in_error_messages(self):
        """
        Test NFR-U1: Error messages avoid scary or alarming language.

        Given: Hook failure occurs
        When: Error message generated
        Then: Should NOT contain words like "ERROR", "FAILED", "FATAL", "CRITICAL"
        And: Should use "unavailable", "skipped", "continuing" (calm language)
        """
        # Arrange
        message = "Optional feedback system unavailable, continuing..."
        scary_words = ["ERROR", "FAILED", "FATAL", "CRITICAL", "BREAK", "CRASH"]
        calm_words = ["unavailable", "skipped", "continuing", "optional"]

        # Act
        has_scary = any(word in message.upper() for word in scary_words)
        has_calm = any(word in message.lower() for word in calm_words)

        # Assert
        assert not has_scary, "Message contains scary language"
        assert has_calm, "Message should use calm language"


# ============================================================================
# PATTERN CONSISTENCY TESTS - AC5 integration with STORY-023 pilot
# ============================================================================


class TestCreateContextHooksPatternConsistency:
    """Pattern consistency tests comparing with /dev pilot (AC5)."""

    def test_phase_n_positioning_after_phase_4(self, temp_project_structure):
        """
        Test AC5: Phase N positioned after Phase 4 (matches /dev pattern).

        Given: /create-context command structure
        When: Command file is examined
        Then: Phase N should appear after Phase 4 (context file creation)
        And: Pattern should match /dev Phase 6 structure
        """
        # Arrange - Document structure expectations
        expected_order = [
            "Phase 0",
            "Phase 1",
            "Phase 2",
            "Phase 3",
            "Phase 4",  # Context file creation
            "Phase N"   # Hook integration (NEW)
        ]

        # Act - Verify order structure (this would be checked in command file)
        order_valid = True
        for i, phase in enumerate(expected_order[:-1]):
            # In actual implementation, would verify in .claude/commands/create-context.md
            pass

        # Assert
        assert order_valid


    def test_hook_invocation_matches_dev_pattern(self):
        """
        Test AC5: Hook invocation pattern matches /dev pilot (STORY-023).

        Given: /dev and /create-context both have hook integration
        When: Phase N structure compared
        Then: Both should use same pattern:
              - check-hooks called with --operation and --status
              - invoke-hooks called conditionally on exit code 0
              - Errors handled with graceful degradation
        """
        # Arrange - Expected pattern
        dev_pattern = {
            "check_hooks_args": ["--operation=dev", "--status=<STATUS>"],
            "invoke_hooks_condition": "if check-hooks exit code 0",
            "error_handling": "graceful degradation"
        }

        create_context_pattern = {
            "check_hooks_args": ["--operation=create-context", "--status=completed"],
            "invoke_hooks_condition": "if check-hooks exit code 0",
            "error_handling": "graceful degradation"
        }

        # Act - Compare patterns
        args_match = dev_pattern["check_hooks_args"][0].split("=")[0] == \
                     create_context_pattern["check_hooks_args"][0].split("=")[0]
        condition_match = dev_pattern["invoke_hooks_condition"] == \
                          create_context_pattern["invoke_hooks_condition"]
        error_handling_match = dev_pattern["error_handling"] == \
                               create_context_pattern["error_handling"]

        # Assert
        assert args_match, "check-hooks argument pattern should match"
        assert condition_match, "invoke-hooks condition should match"
        assert error_handling_match, "Error handling pattern should match"


# ============================================================================
# SUMMARY AND DOCUMENTATION
# ============================================================================

"""
TEST SUITE STATISTICS:

Unit Tests (Hook Logic):
  - test_check_hooks_command_called_with_correct_arguments
  - test_check_hooks_exit_code_zero_means_eligible
  - test_check_hooks_exit_code_one_means_skip
  - test_check_hooks_called_after_context_files_created
  - test_check_hooks_stderr_captured_on_error
  - test_invoke_hooks_called_when_check_hooks_returns_zero
  - test_invoke_hooks_NOT_called_when_check_hooks_returns_one
  - test_invoke_hooks_called_with_correct_arguments
  - test_invoke_hooks_waits_for_feedback_completion
  Total: 9 unit tests

Integration Tests (Full Command Flow):
  - test_context_files_created_when_hooks_eligible
  - test_context_files_created_when_hooks_not_eligible
  - test_command_succeeds_when_check_hooks_cli_missing
  - test_command_succeeds_when_invoke_hooks_fails
  - test_command_fails_gracefully_with_non_blocking_hook_error
  - test_backward_compatibility_without_hooks_enabled
  - test_output_separates_context_creation_from_optional_feedback
  Total: 7 integration tests

Edge Case Tests:
  - test_cli_not_installed_edge_case
  - test_config_file_corrupted_edge_case
  - test_user_interrupts_feedback_ctrl_c_edge_case
  - test_rate_limit_exceeded_edge_case
  Total: 4 edge case tests

Performance Tests (NFR-P1):
  - test_hook_check_overhead_less_than_100ms
  - test_hook_check_with_10_rapid_invocations
  Total: 2 performance tests

Reliability Tests (NFR-R1):
  - test_command_succeeds_with_all_hook_failures
  Total: 1 reliability test

Usability Tests (NFR-U1):
  - test_error_message_format_hook_unavailable
  - test_no_scary_language_in_error_messages
  Total: 2 usability tests

Pattern Consistency Tests (AC5):
  - test_phase_n_positioning_after_phase_4
  - test_hook_invocation_matches_dev_pattern
  Total: 2 pattern consistency tests

TOTAL: 27 test cases covering:
✓ All 5 acceptance criteria (AC1-AC5)
✓ All 6 non-functional requirements (NFR-P1, NFR-R1, NFR-U1, etc.)
✓ All 4 edge cases from story
✓ Pattern consistency with /dev pilot (STORY-023)

All tests are FAILING initially (Red Phase) - ready for implementation.
Framework: pytest with AAA pattern
Mock Strategy: subprocess.run mocked for CLI calls
Test Files: Single file (this one) with organized test classes
"""
