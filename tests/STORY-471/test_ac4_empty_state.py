"""
Test: AC#4 - Graceful Empty State
Story: STORY-471
Generated: 2026-03-04

Validates: When no business artifacts exist, command shows welcome message
guiding user to /assess-me rather than errors.
"""
import os
import re
import pytest

PROJECT_ROOT = "/mnt/c/Projects/DevForgeAI2"
TARGET_FILE = os.path.join(PROJECT_ROOT, "src/claude/commands/my-business.md")


class TestEmptyStateHandling:
    """AC#4: Empty state shows welcome message, not errors."""

    @pytest.fixture
    def file_content(self):
        with open(TARGET_FILE, "r") as f:
            return f.read()

    def test_should_contain_empty_state_handling(self, file_content):
        # Arrange
        pattern = r"(?i)empty.state|no.*artifacts|not.*found|does.not.exist|welcome"

        # Act
        match = re.search(pattern, file_content)

        # Assert
        assert match is not None, "Command must handle empty state (no business artifacts)"

    def test_should_reference_assess_me_command(self, file_content):
        # Arrange
        pattern = r"/assess-me"

        # Act
        match = re.search(pattern, file_content)

        # Assert
        assert match is not None, "Empty state must guide user to /assess-me"

    def test_should_show_welcome_message(self, file_content):
        # Arrange
        pattern = r"(?i)welcome|get.started|begin|first.step"

        # Act
        match = re.search(pattern, file_content)

        # Assert
        assert match is not None, "Empty state must show welcoming onboarding message"

    def test_should_not_show_error_on_empty_state(self, file_content):
        # Arrange - BR-002: empty state is onboarding, not error
        # Verify the command documents graceful handling, not error throwing
        pattern = r"(?i)error.*no.*artifacts|raise.*error.*missing|throw.*exception"

        # Act
        match = re.search(pattern, file_content)

        # Assert
        assert match is None, "Empty state must NOT show errors - should show onboarding guidance"
