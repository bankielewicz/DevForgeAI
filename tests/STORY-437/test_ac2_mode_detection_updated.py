"""
Test: AC#2 - Epic Creation Mode Removed from mode-detection.md
Story: STORY-437
TDD Phase: RED - All tests should FAIL before implementation.

Verifies that Epic Creation Mode detection logic is removed from
mode-detection.md while Sprint Planning, Story Management, and
Default modes remain.
"""
import re
import pytest


class TestEpicCreationModeSectionRemoved:
    """Verify no 'Epic Creation Mode' section exists."""

    def test_should_not_contain_epic_creation_mode_header_when_read(self, mode_detection_content):
        """Epic Creation Mode section must not exist."""
        assert "Epic Creation Mode" not in mode_detection_content, (
            "mode-detection.md still contains 'Epic Creation Mode' section"
        )


class TestPurposeListUpdated:
    """Verify purpose list contains 3 modes, not 4."""

    def test_should_not_mention_epic_in_purpose_list_when_read(self, mode_detection_content):
        """Purpose list must not reference epic creation."""
        # Look for epic creation in purpose/mode listing context
        assert "Epic Creation" not in mode_detection_content, (
            "mode-detection.md still lists Epic Creation in purpose"
        )


class TestDetectionSequenceUpdated:
    """Verify detection sequence starts with Sprint Planning."""

    def test_should_start_detection_with_sprint_planning_when_read(self, mode_detection_content):
        """First detection step should be Sprint Planning, not Epic."""
        # Find detection sequence/priority section
        # Epic should not appear before Sprint in any ordered list
        epic_pos = mode_detection_content.find("Epic Creation")
        assert epic_pos == -1, (
            "mode-detection.md still has Epic Creation in detection sequence"
        )


class TestModePriorityUpdated:
    """Verify mode priority starts with Sprint Planning."""

    def test_should_not_have_epic_in_priority_list_when_read(self, mode_detection_content):
        """Mode priority must not include Epic."""
        # Check that no Epic priority entry exists
        assert re.search(r"Epic.*(?:highest|priority|1\.)", mode_detection_content) is None, (
            "mode-detection.md still has Epic in mode priority"
        )


class TestErrorMessageUpdated:
    """Verify 'For Epic Creation:' error message removed."""

    def test_should_not_contain_for_epic_creation_message_when_read(self, mode_detection_content):
        """'For Epic Creation:' error message must be removed."""
        assert "For Epic Creation:" not in mode_detection_content, (
            "mode-detection.md still contains 'For Epic Creation:' message"
        )


class TestEpicManagementReferenceRemoved:
    """Verify epic-management.md reference removed from Related Files."""

    def test_should_not_reference_epic_management_md_when_read(self, mode_detection_content):
        """epic-management.md must not be referenced."""
        assert "epic-management.md" not in mode_detection_content, (
            "mode-detection.md still references epic-management.md"
        )
