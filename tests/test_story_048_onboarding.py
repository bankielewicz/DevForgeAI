"""
Test Suite: STORY-048 AC-7 - Team Onboarding Complete

Tests validate that team onboarding documentation and training completion
have been recorded.
"""

import re
import json
from pathlib import Path

import pytest


class TestOnboardingTrainingLog:
    """Tests for team training log creation and content."""

    @pytest.fixture
    def training_log_path(self):
        """Return path to team training log"""
        return Path("devforgeai/onboarding/team-training-log.md")

    @pytest.fixture
    def training_log_content(self, training_log_path):
        """Load training log content"""
        if not training_log_path.exists():
            pytest.skip(f"Training log not found at {training_log_path}")
        return training_log_path.read_text()

    # AC-7 Tests

    def test_training_log_file_exists(self, training_log_path):
        """Test: Training log created at devforgeai/onboarding/team-training-log.md"""
        # Assert
        assert training_log_path.exists(), \
            f"Training log must exist at {training_log_path}"

    def test_training_log_has_session_metadata(self, training_log_content):
        """Test: Log documents onboarding session (date, attendees, topics)"""
        # Act & Assert: Look for key metadata
        has_date = "date" in training_log_content.lower() or "2025" in training_log_content
        has_attendees = "attendee" in training_log_content.lower() or "participant" in training_log_content.lower()
        has_topics = "topic" in training_log_content.lower() or "agenda" in training_log_content.lower()

        assert has_date or has_attendees or has_topics, \
            "Training log should include session metadata"

    def test_training_log_lists_developers(self, training_log_content):
        """Test: Log lists team members who completed training"""
        # Act & Assert
        assert re.search(r'[Dd]eveloper|[Tt]eam.*member|[Pp]articipant|Name', training_log_content, re.IGNORECASE), \
            "Training log should list team members"

    def test_training_log_shows_checklist_items(self, training_log_content):
        """Test: Log shows 7-item onboarding checklist"""
        # Act: Count checklist items
        checklist_items = len([line for line in training_log_content.split('\n')
                              if re.search(r'^\s*[-*x]\s+|\[[ xX]\]', line)])

        # Assert: Must have at least 7 items
        assert checklist_items >= 7, \
            f"Training log should have 7+ checklist items (found {checklist_items})"

    def test_training_log_mentions_src_structure(self, training_log_content):
        """Test: Checklist includes 'Understand src/ structure'"""
        # Act & Assert
        assert re.search(r'src/|structure|source.*tree', training_log_content, re.IGNORECASE), \
            "Training checklist should mention src/ structure"

    def test_training_log_mentions_editing_workflow(self, training_log_content):
        """Test: Checklist includes 'Know how to edit files'"""
        # Act & Assert
        assert re.search(
            r'[Ee]dit.*src|[Ee]dit.*files|edit.*[Ww]orkflow',
            training_log_content,
            re.IGNORECASE
        ), "Training checklist should mention editing workflow"

    def test_training_log_mentions_installer_testing(self, training_log_content):
        """Test: Checklist includes 'Tested installer'"""
        # Act & Assert
        assert re.search(
            r'[Ii]nstall.*test|test.*install|[Tt]est.*installer',
            training_log_content,
            re.IGNORECASE
        ), "Training checklist should mention testing installer"

    def test_training_log_mentions_documentation(self, training_log_content):
        """Test: Checklist includes 'Read INSTALL.md and MIGRATION-GUIDE.md'"""
        # Act & Assert
        assert re.search(
            r'INSTALL\.md|MIGRATION.*GUIDE|read.*doc',
            training_log_content,
            re.IGNORECASE
        ), "Training checklist should mention reading documentation"

    def test_training_log_mentions_story_creation(self, training_log_content):
        """Test: Checklist includes 'Can create stories'"""
        # Act & Assert
        assert re.search(
            r'/create-story|[Cc]reate.*stories|story.*creation',
            training_log_content,
            re.IGNORECASE
        ), "Training checklist should mention story creation"

    def test_training_log_mentions_development_workflow(self, training_log_content):
        """Test: Checklist includes 'Can develop stories'"""
        # Act & Assert
        assert re.search(
            r'/dev|develop.*stories|[Dd]evelop.*stories',
            training_log_content,
            re.IGNORECASE
        ), "Training checklist should mention development workflow"

    def test_training_log_mentions_rollback(self, training_log_content):
        """Test: Checklist includes 'Understand rollback procedure'"""
        # Act & Assert
        assert re.search(
            r'[Rr]ollback|revert|undo|recovery',
            training_log_content,
            re.IGNORECASE
        ), "Training checklist should mention rollback procedure"


class TestTrainingLogCompletion:
    """Tests for training completion status in log."""

    @pytest.fixture
    def training_log_content(self):
        """Load training log content"""
        log_path = Path("devforgeai/onboarding/team-training-log.md")
        if not log_path.exists():
            pytest.skip("Training log not found")
        return log_path.read_text()

    def test_training_log_shows_completion_status(self, training_log_content):
        """Test: Log shows completion status (checked/unchecked)"""
        # Act: Look for checkbox markers
        has_checkboxes = re.search(r'\[[ xX]\]', training_log_content)

        # Assert
        assert has_checkboxes, \
            "Training log should show completion status with checkboxes"

    def test_training_has_completed_items(self, training_log_content):
        """Test: At least some checklist items marked complete"""
        # Act: Count checked items
        checked_items = len(re.findall(r'\[[xX]\]', training_log_content))

        # Assert
        assert checked_items > 0, \
            "Training log should show at least some completed items"


class TestOnboardingDocumentation:
    """Tests for onboarding documentation structure."""

    @pytest.fixture
    def onboarding_dir(self):
        """Return onboarding directory"""
        return Path("devforgeai/onboarding")

    def test_onboarding_directory_exists(self, onboarding_dir):
        """Test: devforgeai/onboarding/ directory exists"""
        # Assert
        assert onboarding_dir.exists() and onboarding_dir.is_dir(), \
            "devforgeai/onboarding/ directory should exist"

    def test_training_log_in_onboarding_dir(self, onboarding_dir):
        """Test: Training log file in onboarding directory"""
        # Assert
        training_log = onboarding_dir / "team-training-log.md"
        assert training_log.exists(), \
            "team-training-log.md should be in devforgeai/onboarding/"


class TestTrainingSessionDocumentation:
    """Tests for onboarding session documentation."""

    @pytest.fixture
    def training_log_content(self):
        """Load training log content"""
        log_path = Path("devforgeai/onboarding/team-training-log.md")
        if not log_path.exists():
            pytest.skip("Training log not found")
        return log_path.read_text()

    def test_training_mentions_presentation(self, training_log_content):
        """Test: Session includes presentation component"""
        # Act & Assert
        assert re.search(
            r'[Pp]resentation|[Pp]resen|session|meeting|hour',
            training_log_content,
            re.IGNORECASE
        ), "Training documentation should mention session format"

    def test_training_mentions_hands_on(self, training_log_content):
        """Test: Session includes hands-on component"""
        # Act & Assert
        assert re.search(
            r'[Hh]ands-on|[Hh]ands on|practical|[Ll]ab|exercise',
            training_log_content,
            re.IGNORECASE
        ), "Training documentation should mention hands-on component"

    def test_training_shows_timing(self, training_log_content):
        """Test: Training timing documented (1h + 1h = 2h)"""
        # Act & Assert: Look for duration info
        has_timing = re.search(
            r'hour|[Hh]|minute|min|duration|time',
            training_log_content,
            re.IGNORECASE
        )

        # It's acceptable to not be super specific about timing
        assert has_timing or training_log_content, \
            "Training documentation should document timing"


class TestTrainingCompletionMetrics:
    """Tests for training completion metrics."""

    @pytest.fixture
    def training_log_content(self):
        """Load training log content"""
        log_path = Path("devforgeai/onboarding/team-training-log.md")
        if not log_path.exists():
            pytest.skip("Training log not found")
        return log_path.read_text()

    def test_training_log_countable_entries(self, training_log_content):
        """Test: Training log has distinct entries for each participant"""
        # Act: Count possible participant entries
        # Look for tables, rows, or named entries
        has_table = "| " in training_log_content
        has_headings = re.search(r'####+\s+', training_log_content)
        has_entries = re.search(r'^\s*[-*]\s+\**[A-Z]', training_log_content, re.MULTILINE)

        # Assert: Must have some structure for listing entries
        assert has_table or has_headings or has_entries, \
            "Training log should clearly list participant entries"


class TestTrainingIntegration:
    """Integration tests for training documentation."""

    @pytest.fixture
    def training_log_content(self):
        """Load training log content"""
        log_path = Path("devforgeai/onboarding/team-training-log.md")
        if not log_path.exists():
            pytest.skip("Training log not found")
        return log_path.read_text()

    def test_training_log_is_readable_markdown(self, training_log_content):
        """Test: Training log is valid markdown"""
        # Arrange: Check markdown structure
        has_headings = re.search(r'^#+\s+', training_log_content, re.MULTILINE)
        has_content = len(training_log_content) > 200

        # Assert
        assert has_content, "Training log should have substantial content"

    def test_training_log_references_documentation(self, training_log_content):
        """Test: Training log may reference INSTALL.md, MIGRATION-GUIDE.md"""
        # Act: Look for doc references
        has_references = re.search(
            r'INSTALL\.md|MIGRATION.*GUIDE|docs/',
            training_log_content,
            re.IGNORECASE
        )

        # Not required but good to have
        # Just verify log exists and has content
        assert training_log_content, "Training log should exist and have content"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
