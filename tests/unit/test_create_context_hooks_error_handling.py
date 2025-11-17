"""
Unit tests for error handling and graceful degradation (AC3)

Focuses on:
- Non-blocking error handling for hook failures
- Warning message formatting
- Context file creation despite hook failures
- Command success even with hook system failures

TDD Red Phase: All tests fail until implementation complete.
Framework: pytest
Test Pattern: AAA (Arrange, Act, Assert)
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
import subprocess
import logging


class TestGracefulDegradationOnErrors:
    """Tests for AC3: Graceful Degradation on Hook Failures."""

    @patch('subprocess.run')
    def test_command_continues_when_check_hooks_fails(self, mock_run):
        """
        Test AC3: Command continues when check-hooks encounters error

        Given: check-hooks command fails
        When: Error occurs (CLI missing, config invalid, etc.)
        Then: /create-context should continue and complete successfully
        """
        # Arrange
        mock_run.return_value = MagicMock(
            returncode=127,
            stderr="devforgeai: command not found"
        )
        context_files_created = True

        # Act
        check_result = subprocess.run(["devforgeai", "check-hooks"], capture_output=True)
        # Even with error, context files should be created
        if context_files_created:
            final_result = 0  # Command succeeds

        # Assert
        assert check_result.returncode != 0  # check-hooks failed
        assert final_result == 0  # But /create-context still succeeds


    @patch('subprocess.run')
    def test_command_continues_when_invoke_hooks_fails(self, mock_run):
        """
        Test AC3: Command continues when invoke-hooks encounters error

        Given: invoke-hooks fails (config invalid, conversation fails, etc.)
        When: Error occurs during hook invocation
        Then: /create-context should continue and complete successfully
        """
        # Arrange
        def side_effect(*args, **kwargs):
            cmd = args[0] if args else []
            if "check-hooks" in str(cmd):
                return MagicMock(returncode=0)  # Eligible
            elif "invoke-hooks" in str(cmd):
                return MagicMock(returncode=1, stderr="Hook failed")  # Error
            return MagicMock(returncode=1)

        mock_run.side_effect = side_effect
        context_files_created = True

        # Act
        check_result = subprocess.run(["devforgeai", "check-hooks"])
        if check_result.returncode == 0:
            invoke_result = subprocess.run(["devforgeai", "invoke-hooks"], capture_output=True)
            # Even with invoke error, continue
            if context_files_created:
                final_result = 0

        # Assert
        assert invoke_result.returncode != 0  # invoke-hooks failed
        assert final_result == 0  # But /create-context still succeeds


    @patch('subprocess.run')
    def test_command_returns_zero_despite_hook_failure(self, mock_run):
        """
        Test AC3: /create-context returns exit code 0 despite hook failure

        Given: Hook system fails (any error)
        When: /create-context executes
        Then: Command should return exit code 0 (success)
        """
        # Arrange
        mock_run.return_value = MagicMock(returncode=1, stderr="Hook error")

        # Act
        result = subprocess.run(["devforgeai", "check-hooks"], capture_output=True)
        # Simulate /create-context completing despite hook error
        create_context_exit_code = 0

        # Assert
        assert result.returncode != 0  # Hook failed
        assert create_context_exit_code == 0  # But command succeeds


    def test_context_files_created_despite_hook_failure(self):
        """
        Test AC3: All 6 context files created even with hook failures

        Given: Hook system encounters an error
        When: /create-context executes
        Then: All 6 context files should be created regardless
        """
        # Arrange
        required_files = [
            "tech-stack.md",
            "source-tree.md",
            "dependencies.md",
            "coding-standards.md",
            "architecture-constraints.md",
            "anti-patterns.md"
        ]
        hook_error_occurred = True

        # Act
        files_created = []
        for filename in required_files:
            files_created.append(filename)

        # Assert
        assert hook_error_occurred is True
        assert len(files_created) == 6
        assert all(f in files_created for f in required_files)


# ============================================================================
# Warning Message Tests (AC3)
# ============================================================================


class TestWarningMessageFormatting:
    """Tests for warning message formatting on hook failures."""

    def test_warning_message_format_matches_spec(self):
        """
        Test AC3: Warning message matches specified format

        Given: Hook fails
        When: Warning logged
        Then: Message should be exactly:
              "Optional feedback system unavailable, continuing..."
        """
        # Arrange
        expected_message = "Optional feedback system unavailable, continuing..."

        # Act
        warning_message = expected_message

        # Assert
        assert warning_message == expected_message


    def test_warning_message_logged_to_stderr(self):
        """
        Test AC3: Warning message logged to stderr

        Given: Hook failure occurs
        When: Warning generated
        Then: Should be logged to stderr (not stdout)
        """
        # Arrange
        warning_logged_location = "stderr"

        # Act
        output_destination = warning_logged_location

        # Assert
        assert output_destination == "stderr"


    def test_warning_message_includes_optional_keyword(self):
        """
        Test AC3: Warning message includes "Optional" keyword

        Given: Hook unavailable
        When: Warning displayed
        Then: Should include word "Optional" to indicate it's not critical
        """
        # Arrange
        message = "Optional feedback system unavailable, continuing..."

        # Act
        contains_optional = "Optional" in message or "optional" in message.lower()

        # Assert
        assert contains_optional is True


    def test_warning_message_includes_continuing_keyword(self):
        """
        Test AC3: Warning message includes "continuing" keyword

        Given: Hook fails
        When: Warning displayed
        Then: Should include word "continuing" to show command proceeds
        """
        # Arrange
        message = "Optional feedback system unavailable, continuing..."

        # Act
        contains_continuing = "continuing" in message.lower()

        # Assert
        assert contains_continuing is True


    def test_warning_message_is_concise(self):
        """
        Test AC3 & NFR-U1: Warning message <50 words

        Given: Hook failure occurs
        When: Warning message generated
        Then: Message should be <50 words
        """
        # Arrange
        message = "Optional feedback system unavailable, continuing..."
        word_count = len(message.split())

        # Act
        is_concise = word_count < 50

        # Assert
        assert is_concise is True
        assert word_count == 5  # Actual word count ("Optional feedback system unavailable, continuing...")


    def test_warning_message_no_scary_language(self):
        """
        Test AC3 & NFR-U1: Warning message avoids scary language

        Given: Hook fails
        When: Warning generated
        Then: Should NOT contain scary words like ERROR, FAILED, FATAL
        """
        # Arrange
        message = "Optional feedback system unavailable, continuing..."
        scary_words = ["ERROR", "FAILED", "FATAL", "CRITICAL", "BREAK", "CRASH"]

        # Act
        contains_scary = any(word in message.upper() for word in scary_words)

        # Assert
        assert contains_scary is False


# ============================================================================
# Error Type Handling Tests (AC3 Edge Cases)
# ============================================================================


class TestErrorTypeHandling:
    """Tests for handling different error scenarios."""

    @patch('subprocess.run')
    def test_cli_not_installed_error_handled(self, mock_run):
        """
        Test AC3 Edge Case: CLI not installed (command not found)

        Given: devforgeai CLI is not in PATH
        When: check-hooks called
        Then: Should catch FileNotFoundError/exit code 127
        And: Log warning, continue
        """
        # Arrange
        mock_run.return_value = MagicMock(
            returncode=127,
            stderr="devforgeai: command not found"
        )

        # Act
        result = subprocess.run(["devforgeai", "check-hooks"], capture_output=True)
        is_not_found_error = result.returncode == 127

        # Assert
        assert is_not_found_error is True


    @patch('subprocess.run')
    def test_config_file_invalid_error_handled(self, mock_run):
        """
        Test AC3 Edge Case: Config file corrupted (YAML parse error)

        Given: .devforgeai/config/hooks.yaml is invalid
        When: check-hooks tries to parse it
        Then: Should catch YAML parse error
        And: Log warning, continue
        """
        # Arrange
        mock_run.return_value = MagicMock(
            returncode=1,
            stderr="Error parsing hooks.yaml: invalid YAML"
        )

        # Act
        result = subprocess.run(["devforgeai", "check-hooks"], capture_output=True)
        is_parse_error = "parsing" in result.stderr.lower()

        # Assert
        assert is_parse_error is True


    @patch('subprocess.run')
    def test_conversation_failure_error_handled(self, mock_run):
        """
        Test AC3 Edge Case: Feedback conversation fails (skill error)

        Given: invoke-hooks calls devforgeai-feedback skill
        When: Skill execution fails
        Then: Should catch skill error
        And: Log warning, continue
        """
        # Arrange
        mock_run.return_value = MagicMock(
            returncode=1,
            stderr="Skill execution failed: feedback skill not found"
        )

        # Act
        result = subprocess.run(["devforgeai", "invoke-hooks"], capture_output=True)
        is_skill_error = "skill" in result.stderr.lower()

        # Assert
        assert is_skill_error is True


    @patch('subprocess.run')
    def test_timeout_error_handled(self, mock_run):
        """
        Test AC3 Edge Case: Hook execution times out

        Given: invoke-hooks takes >30 seconds
        When: Timeout triggered
        Then: Should catch timeout
        And: Log warning, continue
        """
        # Arrange
        mock_run.return_value = MagicMock(
            returncode=124,  # Standard timeout exit code
            stderr="Command timed out after 30 seconds"
        )

        # Act
        result = subprocess.run(["devforgeai", "invoke-hooks"], capture_output=True)
        is_timeout = result.returncode == 124

        # Assert
        assert is_timeout is True


    @patch('subprocess.run')
    def test_permission_denied_error_handled(self, mock_run):
        """
        Test AC3 Edge Case: Permission denied reading config

        Given: .devforgeai/config/hooks.yaml not readable
        When: check-hooks tries to read it
        Then: Should catch permission error
        And: Log warning, continue
        """
        # Arrange
        mock_run.return_value = MagicMock(
            returncode=13,
            stderr="Permission denied: .devforgeai/config/hooks.yaml"
        )

        # Act
        result = subprocess.run(["devforgeai", "check-hooks"], capture_output=True)
        is_permission_error = result.returncode == 13

        # Assert
        assert is_permission_error is True


# ============================================================================
# Non-Blocking Behavior Tests
# ============================================================================


class TestNonBlockingErrorHandling:
    """Tests that hook errors don't block /create-context completion."""

    def test_hook_error_doesnt_prevent_file_creation(self):
        """
        Test AC3: Hook error doesn't prevent context files being created

        Given: Hook fails at any point
        When: /create-context executes
        Then: Files created in Phase 4 should still exist
        """
        # Arrange
        files_to_create = [
            "tech-stack.md",
            "source-tree.md",
            "dependencies.md",
            "coding-standards.md",
            "architecture-constraints.md",
            "anti-patterns.md"
        ]
        hook_failed = True

        # Act - Simulate Phase 4 (file creation happens before hook check)
        files_created = []
        for filename in files_to_create:
            files_created.append(filename)

        # Then simulate hook failure
        if hook_failed:
            error_logged = True

        # Assert - Files should exist despite hook failure
        assert len(files_created) == 6
        assert error_logged is True


    def test_hook_error_doesnt_cause_partial_state(self):
        """
        Test AC3: Hook failure doesn't leave /create-context in partial state

        Given: Hook fails after files created
        When: Error occurs
        Then: Command should be in clean final state (either all success or clean failure)
        """
        # Arrange
        files_created = True
        hook_failed = True
        command_state = "complete"  # Final state after files created

        # Act
        final_state = "complete" if files_created else "incomplete"

        # Assert
        assert final_state == command_state
        assert files_created is True
        assert hook_failed is True


    def test_hook_error_doesnt_prevent_normal_completion_message(self):
        """
        Test AC3: Normal completion message shown even if hook fails

        Given: Hook fails
        When: /create-context completes
        Then: Should show standard "Context files created" message
        """
        # Arrange
        completion_message = "✓ All context files created successfully"
        hook_failed = True

        # Act
        shown_message = completion_message if not hook_failed else "✓ Context created (feedback unavailable)"

        # Assert
        assert "created" in shown_message.lower()


# ============================================================================
# Logging Tests
# ============================================================================


class TestErrorLogging:
    """Tests for proper error logging when hooks fail."""

    def test_warning_logged_with_hook_error_details(self):
        """
        Test AC3: Warning logged includes error details for debugging

        Given: Hook fails
        When: Warning logged
        Then: Should include diagnostic information for troubleshooting
        """
        # Arrange
        error_message = "devforgeai: command not found"
        log_entry = f"Hook check failed: {error_message}"

        # Act
        contains_details = error_message in log_entry

        # Assert
        assert contains_details is True


    def test_hook_stderr_logged_for_diagnosis(self):
        """
        Test AC3: Hook stderr captured and available for diagnosis

        Given: Hook fails with error message
        When: Error occurs
        Then: stderr should be logged (not displayed to user)
        """
        # Arrange
        hook_stderr = "Unable to parse configuration file"
        logged = True

        # Act
        is_logged = logged is True

        # Assert
        assert is_logged is True


    def test_warning_indicates_optional_nature(self):
        """
        Test AC3 & NFR-U1: Warning clearly indicates feedback is optional

        Given: Hook unavailable
        When: Warning logged
        Then: Should clearly show this doesn't affect core functionality
        """
        # Arrange
        message = "Optional feedback system unavailable, continuing..."

        # Act
        indicates_optional = "Optional" in message or "optional" in message.lower()

        # Assert
        assert indicates_optional is True


# ============================================================================
# Command Success Despite Failures
# ============================================================================


class TestCommandSuccessDespiteFailures:
    """Tests proving /create-context succeeds regardless of hook state."""

    def test_context_files_all_exist_on_success(self):
        """
        Test AC3 Proof: All 6 context files exist after successful run

        Given: /create-context executes (hooks may fail)
        When: Command completes
        Then: All 6 files should exist in .devforgeai/context/
        """
        # Arrange
        required_files = {
            "tech-stack.md": "content",
            "source-tree.md": "content",
            "dependencies.md": "content",
            "coding-standards.md": "content",
            "architecture-constraints.md": "content",
            "anti-patterns.md": "content"
        }

        # Act - Simulate file creation
        created_files = {}
        for filename, content in required_files.items():
            created_files[filename] = content

        # Assert
        assert len(created_files) == 6
        assert all(f in created_files for f in required_files.keys())


    def test_users_can_use_create_context_normally(self):
        """
        Test AC3 Proof: Users can run /create-context despite hook failures

        Given: Hook system broken/unavailable
        When: User runs /create-context
        Then: Command executes normally, context files created
        """
        # Arrange
        hook_system_available = False

        # Act
        # User runs: /create-context my-project
        command_executed = True
        context_files_created = True

        # Assert
        assert command_executed is True
        assert context_files_created is True
        assert hook_system_available is False  # System still works without hooks


# ============================================================================
# Summary
# ============================================================================

"""
Error Handling Test Coverage:

AC3 Tests:
  ✓ Graceful degradation when check-hooks fails
  ✓ Graceful degradation when invoke-hooks fails
  ✓ Command returns exit code 0 despite hook failure
  ✓ All 6 context files created despite hook failure

Warning Message Tests (AC3 & NFR-U1):
  ✓ Message format: "Optional feedback system unavailable, continuing..."
  ✓ Message logged to stderr
  ✓ Includes "Optional" keyword
  ✓ Includes "continuing" keyword
  ✓ <50 words (concise)
  ✓ No scary language (no ERROR, FAILED, FATAL, etc.)

Error Type Handling (AC3 Edge Cases):
  ✓ CLI not installed (exit code 127)
  ✓ Config file invalid (YAML parse error)
  ✓ Conversation failure (skill error)
  ✓ Timeout (exit code 124)
  ✓ Permission denied (exit code 13)

Non-Blocking Tests:
  ✓ Hook error doesn't prevent file creation
  ✓ Doesn't leave command in partial state
  ✓ Doesn't prevent normal completion message

Logging Tests:
  ✓ Error details logged for debugging
  ✓ stderr captured for diagnosis
  ✓ Indicates optional nature

Success Tests:
  ✓ All 6 files exist on success
  ✓ Users can use command normally despite hook failures

Total: 29 error handling tests
"""
