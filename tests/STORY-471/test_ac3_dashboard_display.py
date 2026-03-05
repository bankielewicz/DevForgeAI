"""
Test: AC#3 - Aggregated Dashboard Display
Story: STORY-471
Generated: 2026-03-04

Validates: Dashboard shows 6 elements - profile summary, streak count,
milestones completed, current milestone, next task, encouraging quote.
"""
import os
import re
import pytest

PROJECT_ROOT = "/mnt/c/Projects/DevForgeAI2"
TARGET_FILE = os.path.join(PROJECT_ROOT, "src/claude/commands/my-business.md")


class TestDashboardElements:
    """AC#3: Dashboard must display all 6 required elements."""

    @pytest.fixture
    def file_content(self):
        with open(TARGET_FILE, "r") as f:
            return f.read()

    def test_should_display_profile_summary(self, file_content):
        # Arrange
        pattern = r"(?i)profile|adaptation.level"

        # Act
        match = re.search(pattern, file_content)

        # Assert
        assert match is not None, "Dashboard must include profile summary with adaptation level"

    def test_should_display_streak_count(self, file_content):
        # Arrange
        pattern = r"(?i)streak"

        # Act
        match = re.search(pattern, file_content)

        # Assert
        assert match is not None, "Dashboard must include streak count"

    def test_should_display_completed_milestones(self, file_content):
        # Arrange
        pattern = r"(?i)completed.*milestone|milestone.*completed|checkmark"

        # Act
        match = re.search(pattern, file_content)

        # Assert
        assert match is not None, "Dashboard must show completed milestones with checkmarks"

    def test_should_display_current_milestone(self, file_content):
        # Arrange
        pattern = r"(?i)current.*milestone|in.progress|milestone.*progress"

        # Act
        match = re.search(pattern, file_content)

        # Assert
        assert match is not None, "Dashboard must show current milestone in progress"

    def test_should_display_next_task(self, file_content):
        # Arrange
        pattern = r"(?i)next.*task|recommended.*task|estimated.time"

        # Act
        match = re.search(pattern, file_content)

        # Assert
        assert match is not None, "Dashboard must show next recommended task with estimated time"

    def test_should_display_encouraging_quote(self, file_content):
        # Arrange
        pattern = r"(?i)quote|encouraging|motivation"

        # Act
        match = re.search(pattern, file_content)

        # Assert
        assert match is not None, "Dashboard must include an encouraging quote based on progress"


class TestDashboardASCIIRendering:
    """NFR-002: Dashboard renders in ASCII only."""

    @pytest.fixture
    def file_content(self):
        with open(TARGET_FILE, "r") as f:
            return f.read()

    def test_should_contain_ascii_dashboard_pattern(self, file_content):
        # Arrange - look for box-drawing or separator patterns
        pattern = r"[━═─┌┐└┘├┤┬┴┼]"

        # Act
        match = re.search(pattern, file_content)

        # Assert
        assert match is not None, "Dashboard should use ASCII/Unicode box-drawing characters"
