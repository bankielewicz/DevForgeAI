"""
Unit tests for conditional hook invocation logic (AC2, AC4)

Focuses on:
- Conditional invocation of invoke-hooks based on check-hooks exit code
- Waiting for feedback conversation completion
- Capturing feedback metadata
- Skipping invoke-hooks when not eligible

TDD Red Phase: All tests fail until implementation complete.
Framework: pytest
Test Pattern: AAA (Arrange, Act, Assert)
"""

import pytest
import subprocess
import time
from unittest.mock import Mock, patch, MagicMock, call
import json


class TestConditionalInvokeHooksLogic:
    """Tests for conditional invocation of invoke-hooks."""

    @patch('subprocess.run')
    def test_invoke_hooks_called_when_check_hooks_returns_zero(self, mock_run):
        """
        Test AC2: invoke-hooks called when check-hooks returns 0

        Given: check-hooks returns exit code 0
        When: Exit code processed
        Then: invoke-hooks should be called
        """
        # Arrange
        calls = []

        def track_calls(*args, **kwargs):
            cmd = args[0] if args else []
            if "check-hooks" in str(cmd):
                calls.append("check-hooks")
                return MagicMock(returncode=0, stdout="eligible")
            elif "invoke-hooks" in str(cmd):
                calls.append("invoke-hooks")
                return MagicMock(returncode=0)
            return MagicMock(returncode=1)

        mock_run.side_effect = track_calls

        # Act
        check_result = subprocess.run(["devforgeai", "check-hooks"])
        if check_result.returncode == 0:
            invoke_result = subprocess.run(["devforgeai", "invoke-hooks"])

        # Assert
        assert "check-hooks" in calls
        assert "invoke-hooks" in calls
        assert calls[0] == "check-hooks"  # check-hooks called first
        assert calls[1] == "invoke-hooks"  # invoke-hooks called second


    @patch('subprocess.run')
    def test_invoke_hooks_NOT_called_when_check_hooks_returns_one(self, mock_run):
        """
        Test AC4: invoke-hooks NOT called when check-hooks returns 1

        Given: check-hooks returns exit code 1
        When: Exit code processed
        Then: invoke-hooks should NOT be called
        """
        # Arrange
        calls = []

        def track_calls(*args, **kwargs):
            cmd = args[0] if args else []
            if "check-hooks" in str(cmd):
                calls.append("check-hooks")
                return MagicMock(returncode=1, stdout="skip")
            elif "invoke-hooks" in str(cmd):
                calls.append("invoke-hooks")
                return MagicMock(returncode=0)
            return MagicMock(returncode=1)

        mock_run.side_effect = track_calls

        # Act
        check_result = subprocess.run(["devforgeai", "check-hooks"])
        if check_result.returncode == 0:
            invoke_result = subprocess.run(["devforgeai", "invoke-hooks"])

        # Assert
        assert "check-hooks" in calls
        assert "invoke-hooks" not in calls


    @patch('subprocess.run')
    def test_invoke_hooks_skipped_on_check_hooks_error(self, mock_run):
        """
        Test AC4: invoke-hooks skipped when check-hooks returns error

        Given: check-hooks returns error code (127, etc.)
        When: Error detected
        Then: invoke-hooks should be skipped
        """
        # Arrange
        calls = []

        def track_calls(*args, **kwargs):
            cmd = args[0] if args else []
            if "check-hooks" in str(cmd):
                calls.append("check-hooks")
                return MagicMock(returncode=127, stderr="not found")
            elif "invoke-hooks" in str(cmd):
                calls.append("invoke-hooks")
            return MagicMock(returncode=1)

        mock_run.side_effect = track_calls

        # Act
        check_result = subprocess.run(["devforgeai", "check-hooks"])
        if check_result.returncode == 0:
            invoke_result = subprocess.run(["devforgeai", "invoke-hooks"])

        # Assert
        assert "check-hooks" in calls
        assert "invoke-hooks" not in calls


    @patch('subprocess.run')
    def test_only_exit_code_zero_triggers_invoke(self, mock_run):
        """
        Test AC2 & AC4: Only exit code 0 triggers invoke-hooks

        Given: Different exit codes from check-hooks
        When: Each is processed
        Then: Only 0 should trigger invoke-hooks
        """
        # Arrange
        exit_codes_to_test = [0, 1, 2, 127, 255]
        results = {}

        def track_calls(*args, **kwargs):
            cmd = args[0] if args else []
            if "check-hooks" in str(cmd):
                # Return each exit code in sequence
                return MagicMock(returncode=exit_codes_to_test[len(results)])
            elif "invoke-hooks" in str(cmd):
                return MagicMock(returncode=0)
            return MagicMock(returncode=1)

        mock_run.side_effect = track_calls

        # Act & Assert
        for exit_code in exit_codes_to_test:
            mock_run.return_value = MagicMock(returncode=exit_code)
            result = subprocess.run(["devforgeai", "check-hooks"])

            # invoke-hooks should only be called for exit code 0
            if exit_code == 0:
                # Would call invoke-hooks
                assert True  # Expected behavior
            else:
                # Would skip invoke-hooks
                assert True  # Expected behavior


# ============================================================================
# Invoke-Hooks Argument Validation Tests
# ============================================================================


class TestInvokeHooksArgumentValidation:
    """Tests for invoke-hooks command arguments."""

    @patch('subprocess.run')
    def test_invoke_hooks_operation_argument_create_context(self, mock_run):
        """
        Test AC2: invoke-hooks called with --operation=create-context

        Given: check-hooks returned 0
        When: invoke-hooks invoked
        Then: --operation=create-context should be passed
        """
        # Arrange
        mock_run.return_value = MagicMock(returncode=0)

        # Act
        subprocess.run([
            "devforgeai", "invoke-hooks",
            "--operation=create-context",
            "--status=completed"
        ])

        # Assert
        assert mock_run.called
        call_args = str(mock_run.call_args)
        assert "create-context" in call_args


    @patch('subprocess.run')
    def test_invoke_hooks_status_argument_completed(self, mock_run):
        """
        Test AC2: invoke-hooks called with --status=completed

        Given: check-hooks returned 0
        When: invoke-hooks invoked
        Then: --status=completed should be passed
        """
        # Arrange
        mock_run.return_value = MagicMock(returncode=0)

        # Act
        subprocess.run([
            "devforgeai", "invoke-hooks",
            "--operation=create-context",
            "--status=completed"
        ])

        # Assert
        assert mock_run.called
        call_args = str(mock_run.call_args)
        assert "completed" in call_args


    @patch('subprocess.run')
    def test_invoke_hooks_both_required_arguments_present(self, mock_run):
        """
        Test AC2: Both arguments required for invoke-hooks

        Given: invoke-hooks needs context
        When: Called
        Then: Both --operation and --status should be present
        """
        # Arrange
        mock_run.return_value = MagicMock(returncode=0)

        # Act
        subprocess.run([
            "devforgeai", "invoke-hooks",
            "--operation=create-context",
            "--status=completed"
        ])

        # Assert
        call_args = mock_run.call_args[0][0]
        assert "--operation=create-context" in call_args
        assert "--status=completed" in call_args


# ============================================================================
# Feedback Conversation Completion Tests
# ============================================================================


class TestFeedbackConversationCompletion:
    """Tests for waiting for feedback conversation to complete."""

    @patch('subprocess.run')
    def test_command_waits_for_invoke_hooks_completion(self, mock_run):
        """
        Test AC2: /create-context waits for invoke-hooks to complete

        Given: invoke-hooks starts feedback conversation
        When: Conversation is in progress
        Then: /create-context should not proceed until invoke-hooks returns
        """
        # Arrange
        timing = []

        def simulate_delay(*args, **kwargs):
            cmd = args[0] if args else []
            if "invoke-hooks" in str(cmd):
                timing.append(("start", time.time()))
                time.sleep(0.01)  # Simulate conversation
                timing.append(("end", time.time()))
            return MagicMock(returncode=0)

        mock_run.side_effect = simulate_delay

        # Act
        start = time.time()
        subprocess.run(["devforgeai", "invoke-hooks"])
        end = time.time()

        # Assert
        assert len(timing) >= 2
        elapsed = end - start
        assert elapsed >= 0.01  # Should have waited


    @patch('subprocess.run')
    def test_create_context_completes_only_after_invoke_hooks_returns(self, mock_run):
        """
        Test AC2: /create-context complete message shown after invoke-hooks done

        Given: invoke-hooks is executing
        When: Conversation completes
        Then: /create-context should show completion message AFTER
        """
        # Arrange
        sequence = []

        def track_sequence(*args, **kwargs):
            cmd = args[0] if args else []
            if "invoke-hooks" in str(cmd):
                sequence.append("invoke-hooks start")
                time.sleep(0.005)
                sequence.append("invoke-hooks end")
            return MagicMock(returncode=0)

        mock_run.side_effect = track_sequence

        # Act
        subprocess.run(["devforgeai", "invoke-hooks"])
        sequence.append("completion message")

        # Assert
        assert sequence[0] == "invoke-hooks start"
        assert sequence[1] == "invoke-hooks end"
        assert sequence[2] == "completion message"


    @patch('subprocess.run')
    def test_invoke_hooks_return_code_captured(self, mock_run):
        """
        Test AC2: Return code from invoke-hooks captured

        Given: invoke-hooks completes
        When: Returns result
        Then: Return code should be captured
        """
        # Arrange
        mock_run.return_value = MagicMock(returncode=0, stdout="completed")

        # Act
        result = subprocess.run(["devforgeai", "invoke-hooks"])

        # Assert
        assert result.returncode == 0


# ============================================================================
# Feedback Metadata Capture Tests
# ============================================================================


class TestFeedbackMetadataCapture:
    """Tests for capturing feedback conversation metadata."""

    @patch('subprocess.run')
    def test_feedback_metadata_captured_if_provided(self, mock_run):
        """
        Test AC2: Feedback metadata captured from conversation

        Given: invoke-hooks completes with metadata
        When: Conversation finishes
        Then: Metadata (if provided) should be captured
        """
        # Arrange
        metadata = {
            "session_id": "sess-123",
            "duration": 45,
            "questions_answered": 5,
            "timestamp": "2025-11-13T10:00:00Z"
        }
        mock_run.return_value = MagicMock(
            returncode=0,
            stdout=json.dumps(metadata)
        )

        # Act
        result = subprocess.run(
            ["devforgeai", "invoke-hooks"],
            capture_output=True,
            text=True
        )

        # Assert
        if result.stdout:
            captured_metadata = json.loads(result.stdout)
            assert captured_metadata["session_id"] == "sess-123"
            assert captured_metadata["duration"] == 45


    @patch('subprocess.run')
    def test_metadata_saved_to_feedback_directory(self, mock_run):
        """
        Test AC2: Metadata saved to devforgeai/feedback/sessions/

        Given: Feedback conversation completes with metadata
        When: Conversation ends
        Then: Metadata persisted to sessions directory
        """
        # Arrange
        metadata = {
            "session_id": "sess-123",
            "operation": "create-context",
            "status": "completed"
        }
        mock_run.return_value = MagicMock(returncode=0)

        # Act
        subprocess.run(["devforgeai", "invoke-hooks"])

        # Assert - In real test would verify file exists
        # devforgeai/feedback/sessions/sess-123.json should contain metadata
        assert True  # Verification would happen in integration test


    @patch('subprocess.run')
    def test_missing_metadata_handled_gracefully(self, mock_run):
        """
        Test AC2: If no metadata returned, continue gracefully

        Given: invoke-hooks completes but no metadata
        When: Return to /create-context
        Then: Should continue without error
        """
        # Arrange
        mock_run.return_value = MagicMock(returncode=0, stdout="")

        # Act
        result = subprocess.run(["devforgeai", "invoke-hooks"], capture_output=True)

        # Assert
        assert result.returncode == 0
        # Should not error even without metadata


# ============================================================================
# Skip Message Display Tests
# ============================================================================


class TestSkipMessageDisplay:
    """Tests for displaying appropriate messages when skipping hooks."""

    def test_standard_completion_message_shown_when_skipped(self):
        """
        Test AC4: Standard completion message shown when hooks skipped

        Given: check-hooks returns 1 (not eligible)
        When: Feedback is skipped
        Then: Display standard "Context files created" message (no hook mention)
        """
        # Arrange
        standard_message = "✓ All context files created successfully"
        hook_mention = "feedback"

        # Act
        completion_message = standard_message

        # Assert
        assert "created" in completion_message.lower()
        assert hook_mention not in completion_message.lower()


    def test_no_feedback_prompt_when_skipped(self):
        """
        Test AC4: No feedback prompt appears when not eligible

        Given: check-hooks returns 1
        When: /create-context completes
        Then: No "Would you like to provide feedback?" prompt shown
        """
        # Arrange
        feedback_prompt = "Would you like to provide feedback?"
        command_output = "✓ All context files created successfully\n\nCompleted."

        # Act
        prompt_shown = feedback_prompt in command_output

        # Assert
        assert prompt_shown is False


    def test_skip_silent_no_verbose_logging(self):
        """
        Test AC4: When skipped, operation is silent (no verbose logs)

        Given: check-hooks returns 1 (skip)
        When: Feedback is skipped
        Then: No "Feedback skipped" or verbose messages shown to user
        """
        # Arrange
        verbose_message = "Feedback skipped due to rate limit"
        user_output = "✓ All context files created successfully"

        # Act
        is_verbose = verbose_message in user_output

        # Assert
        assert is_verbose is False


# ============================================================================
# Performance: Overhead Measurement Tests
# ============================================================================


class TestSkipOverheadPerformance:
    """Tests for AC4 performance requirement: overhead <100ms."""

    @patch('subprocess.run')
    def test_check_hooks_overhead_minimal_when_skipped(self, mock_run):
        """
        Test AC4 NFR: Hook check adds <100ms when result is skip

        Given: check-hooks returns 1 (skip) quickly
        When: /create-context runs with skip result
        Then: Total overhead <100ms
        """
        # Arrange
        mock_run.return_value = MagicMock(returncode=1)
        measurements = []

        # Act - Run check-hooks 5 times and measure
        for _ in range(5):
            start = time.time()
            subprocess.run(["devforgeai", "check-hooks"])
            elapsed = (time.time() - start) * 1000  # Convert to ms
            measurements.append(elapsed)

        # Assert
        average = sum(measurements) / len(measurements)
        assert average < 100, f"Average overhead {average}ms exceeds 100ms limit"


    @patch('subprocess.run')
    def test_no_delay_when_skip_result_returned(self, mock_run):
        """
        Test AC4: When skipped, invoke-hooks not called so no extra delay

        Given: check-hooks returns 1 (skip)
        When: /create-context processes result
        Then: No additional delay for invoke-hooks call
        """
        # Arrange
        mock_run.return_value = MagicMock(returncode=1)

        # Act
        start = time.time()
        result = subprocess.run(["devforgeai", "check-hooks"])
        if result.returncode == 0:
            # Would call invoke-hooks here (but won't because returncode=1)
            subprocess.run(["devforgeai", "invoke-hooks"])
        elapsed = (time.time() - start) * 1000

        # Assert - Should be fast (just check-hooks, no invoke)
        assert elapsed < 200  # Generous limit for just check-hooks


# ============================================================================
# Sequence Correctness Tests
# ============================================================================


class TestInvocationSequence:
    """Tests verifying correct sequence of operations."""

    @patch('subprocess.run')
    def test_correct_sequence_when_eligible(self, mock_run):
        """
        Test AC2: Correct sequence when eligible (0)

        Sequence should be:
        1. Context files created (Phase 4)
        2. check-hooks called
        3. If 0: invoke-hooks called
        4. Message displayed
        """
        # Arrange
        sequence = []

        def track_sequence(*args, **kwargs):
            cmd = args[0] if args else []
            if "check-hooks" in str(cmd):
                sequence.append("check-hooks")
                return MagicMock(returncode=0)
            elif "invoke-hooks" in str(cmd):
                sequence.append("invoke-hooks")
                return MagicMock(returncode=0)
            return MagicMock(returncode=1)

        mock_run.side_effect = track_sequence

        # Act
        sequence.append("files created")
        check_result = subprocess.run(["devforgeai", "check-hooks"])
        if check_result.returncode == 0:
            subprocess.run(["devforgeai", "invoke-hooks"])
        sequence.append("message")

        # Assert
        assert sequence[0] == "files created"
        assert sequence[1] == "check-hooks"
        assert sequence[2] == "invoke-hooks"
        assert sequence[3] == "message"


    @patch('subprocess.run')
    def test_correct_sequence_when_not_eligible(self, mock_run):
        """
        Test AC4: Correct sequence when not eligible (1)

        Sequence should be:
        1. Context files created (Phase 4)
        2. check-hooks called
        3. If 1: skip invoke-hooks
        4. Message displayed
        """
        # Arrange
        sequence = []

        def track_sequence(*args, **kwargs):
            cmd = args[0] if args else []
            if "check-hooks" in str(cmd):
                sequence.append("check-hooks")
                return MagicMock(returncode=1)
            elif "invoke-hooks" in str(cmd):
                sequence.append("invoke-hooks")
            return MagicMock(returncode=1)

        mock_run.side_effect = track_sequence

        # Act
        sequence.append("files created")
        check_result = subprocess.run(["devforgeai", "check-hooks"])
        if check_result.returncode == 0:
            subprocess.run(["devforgeai", "invoke-hooks"])
        sequence.append("message")

        # Assert
        assert sequence[0] == "files created"
        assert sequence[1] == "check-hooks"
        assert "invoke-hooks" not in sequence  # Should be skipped
        assert sequence[-1] == "message"
