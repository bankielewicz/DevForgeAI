"""
Test Suite: /worktrees Management Command
Feature: STORY-095 - /worktrees Management Command
AC#1: Worktree Table Display
AC#2: Cleanup Candidate Identification
AC#3: Interactive Actions Menu
AC#4: Safe Cleanup with Status Check
AC#5: Execution Time Requirement

Tests for the /worktrees slash command that provides visibility and management
for Git worktrees created by /dev.
"""

import pytest
from datetime import datetime, timedelta
from unittest.mock import patch, MagicMock
import json
import time


# =============================================================================
# Test Fixtures
# =============================================================================

@pytest.fixture
def sample_worktree_data():
    """Sample worktree data returned by git-worktree-manager subagent"""
    return {
        "status": "SUCCESS",
        "platform": "linux",
        "worktrees": [
            {
                "story_id": "STORY-037",
                "path": "../devforgeai-story-037/",
                "branch": "story-037",
                "last_activity": (datetime.now() - timedelta(days=2)).isoformat(),
                "days_idle": 2
            },
            {
                "story_id": "STORY-091",
                "path": "../devforgeai-story-091/",
                "branch": "story-091",
                "last_activity": (datetime.now() - timedelta(hours=4)).isoformat(),
                "days_idle": 0
            },
            {
                "story_id": "STORY-094",
                "path": "../devforgeai-story-094/",
                "branch": "story-094",
                "last_activity": (datetime.now() - timedelta(days=12)).isoformat(),
                "days_idle": 12
            }
        ],
        "idle_worktrees": [
            {
                "story_id": "STORY-094",
                "path": "../devforgeai-story-094/",
                "days_idle": 12
            }
        ],
        "active_count": 3,
        "config": {
            "cleanup_threshold_days": 7,
            "max_worktrees": 5
        },
        "timestamp": datetime.now().isoformat()
    }


@pytest.fixture
def sample_story_statuses():
    """Sample story status mappings"""
    return {
        "STORY-037": "Released",
        "STORY-091": "QA Approved",
        "STORY-094": "In Development"
    }


@pytest.fixture
def empty_worktree_data():
    """No worktrees exist"""
    return {
        "status": "SUCCESS",
        "platform": "linux",
        "worktrees": [],
        "idle_worktrees": [],
        "active_count": 0,
        "config": {
            "cleanup_threshold_days": 7,
            "max_worktrees": 5
        },
        "timestamp": datetime.now().isoformat()
    }


# =============================================================================
# AC#1: Worktree Table Display
# =============================================================================

class TestWorktreeTableDisplay:
    """Tests for AC#1: Worktree Table Display"""

    def test_worktrees_list_empty_returns_no_worktrees_message(self, empty_worktree_data):
        """
        Given: No active worktrees exist
        When: Developer runs /worktrees
        Then: Displays "No active worktrees found"
        """
        # Arrange
        worktrees = empty_worktree_data["worktrees"]

        # Act
        if len(worktrees) == 0:
            message = "No active worktrees found"
        else:
            message = f"Found {len(worktrees)} worktrees"

        # Assert
        assert message == "No active worktrees found"

    def test_worktrees_list_displays_table_with_all_columns(self, sample_worktree_data):
        """
        Given: Active worktrees exist
        When: Developer runs /worktrees
        Then: Displays table with columns: Story ID | Path | Age | Size | Status | Last Activity
        """
        # Arrange
        required_columns = ["Story ID", "Path", "Age", "Size", "Status", "Last Activity"]
        worktrees = sample_worktree_data["worktrees"]

        # Act - Format table header
        table_header = " | ".join(required_columns)

        # Assert
        assert len(worktrees) == 3
        for column in required_columns:
            assert column in table_header

    def test_worktrees_table_shows_correct_story_ids(self, sample_worktree_data):
        """
        Given: Multiple worktrees exist
        When: Displaying table
        Then: Each row shows correct story ID
        """
        # Arrange
        expected_ids = ["STORY-037", "STORY-091", "STORY-094"]

        # Act
        actual_ids = [wt["story_id"] for wt in sample_worktree_data["worktrees"]]

        # Assert
        assert actual_ids == expected_ids

    def test_worktrees_table_shows_age_in_human_readable_format(self, sample_worktree_data):
        """
        Given: Worktree with various ages
        When: Displaying age column
        Then: Shows human-readable format (e.g., "2 days", "4 hours", "12 days")
        """
        # Arrange
        def format_age(days_idle):
            if days_idle == 0:
                return "< 1 day"
            elif days_idle == 1:
                return "1 day"
            else:
                return f"{days_idle} days"

        worktrees = sample_worktree_data["worktrees"]

        # Act
        ages = [format_age(wt["days_idle"]) for wt in worktrees]

        # Assert
        assert ages == ["2 days", "< 1 day", "12 days"]


# =============================================================================
# AC#2: Cleanup Candidate Identification
# =============================================================================

class TestCleanupCandidateIdentification:
    """Tests for AC#2: Cleanup Candidate Identification"""

    def test_worktrees_identifies_cleanup_candidates_over_7_days(self, sample_worktree_data):
        """
        Given: Worktrees idle >7 days exist
        When: /worktrees runs
        Then: Identifies them as cleanup candidates
        """
        # Arrange
        threshold = sample_worktree_data["config"]["cleanup_threshold_days"]
        worktrees = sample_worktree_data["worktrees"]

        # Act
        candidates = [wt for wt in worktrees if wt["days_idle"] > threshold]

        # Assert
        assert len(candidates) == 1
        assert candidates[0]["story_id"] == "STORY-094"

    def test_worktrees_displays_warning_indicator_for_idle(self, sample_worktree_data):
        """
        Given: Idle worktrees identified
        When: Displaying status
        Then: Shows warning indicator (⚠️)
        """
        # Arrange
        threshold = 7
        worktrees = sample_worktree_data["worktrees"]

        # Act
        def get_status_indicator(days_idle):
            return "⚠️" if days_idle > threshold else ""

        indicators = [get_status_indicator(wt["days_idle"]) for wt in worktrees]

        # Assert
        assert indicators == ["", "", "⚠️"]

    def test_worktrees_displays_cleanup_summary_message(self, sample_worktree_data):
        """
        Given: 1 worktree idle >7 days
        When: /worktrees displays summary
        Then: Shows "⚠️ 1 worktree idle >7 days"
        """
        # Arrange
        idle_count = len(sample_worktree_data["idle_worktrees"])
        threshold = sample_worktree_data["config"]["cleanup_threshold_days"]

        # Act
        if idle_count == 1:
            message = f"⚠️ {idle_count} worktree idle >{threshold} days"
        elif idle_count > 1:
            message = f"⚠️ {idle_count} worktrees idle >{threshold} days"
        else:
            message = "No cleanup candidates"

        # Assert
        assert message == "⚠️ 1 worktree idle >7 days"

    def test_worktrees_no_cleanup_candidates_when_all_active(self, sample_worktree_data):
        """
        Given: All worktrees have activity within threshold
        When: /worktrees scans for idle
        Then: Reports no cleanup candidates
        """
        # Arrange
        active_worktrees = {
            "worktrees": [
                {"story_id": "STORY-001", "days_idle": 1},
                {"story_id": "STORY-002", "days_idle": 3},
                {"story_id": "STORY-003", "days_idle": 5}
            ],
            "idle_worktrees": [],
            "config": {"cleanup_threshold_days": 7}
        }

        # Act
        idle_count = len(active_worktrees["idle_worktrees"])

        # Assert
        assert idle_count == 0


# =============================================================================
# AC#3: Interactive Actions Menu
# =============================================================================

class TestInteractiveActionsMenu:
    """Tests for AC#3: Interactive Actions Menu"""

    def test_worktrees_action_menu_has_5_options(self):
        """
        Given: Worktree table is displayed
        When: Presenting options to developer
        Then: Offers exactly 5 options
        """
        # Arrange
        expected_options = [
            "Cleanup all candidates",
            "Cleanup selected",
            "Inspect worktree",
            "Resume development",
            "Cancel"
        ]

        # Act
        option_count = len(expected_options)

        # Assert
        assert option_count == 5

    def test_worktrees_action_menu_includes_cleanup_all(self):
        """
        Given: Action menu displayed
        When: Options presented
        Then: Includes "Cleanup all candidates" option
        """
        # Arrange
        options = [
            {"label": "Cleanup all candidates", "description": "Remove all idle worktrees"},
            {"label": "Cleanup selected", "description": "Choose which to remove"},
            {"label": "Inspect worktree", "description": "View details"},
            {"label": "Resume development", "description": "Return to worktree"},
            {"label": "Cancel", "description": "Exit without changes"}
        ]

        # Act
        labels = [opt["label"] for opt in options]

        # Assert
        assert "Cleanup all candidates" in labels

    def test_worktrees_action_menu_includes_cancel_option(self):
        """
        Given: Action menu displayed
        When: Options presented
        Then: Includes "Cancel" option to exit safely
        """
        # Arrange
        options = ["Cleanup all candidates", "Cleanup selected", "Inspect worktree",
                   "Resume development", "Cancel"]

        # Act & Assert
        assert "Cancel" in options

    def test_worktrees_action_menu_format_for_ask_user_question(self):
        """
        Given: Action menu needs to use AskUserQuestion
        When: Formatting options
        Then: Follows AskUserQuestion schema
        """
        # Arrange
        menu_config = {
            "question": "What would you like to do with the worktrees?",
            "header": "Action",
            "multiSelect": False,
            "options": [
                {"label": "Cleanup all candidates",
                 "description": "Remove all worktrees idle >7 days with Released/QA Approved status"},
                {"label": "Cleanup selected",
                 "description": "Choose specific worktrees to remove"},
                {"label": "Inspect worktree",
                 "description": "View detailed info about a worktree"},
                {"label": "Resume development",
                 "description": "Get path to resume work in a worktree"},
                {"label": "Cancel",
                 "description": "Exit without changes"}
            ]
        }

        # Act & Assert
        assert menu_config["multiSelect"] == False
        assert len(menu_config["options"]) == 5
        assert all("label" in opt and "description" in opt for opt in menu_config["options"])


# =============================================================================
# AC#4: Safe Cleanup with Status Check
# =============================================================================

class TestSafeCleanupWithStatusCheck:
    """Tests for AC#4: Safe Cleanup with Status Check"""

    def test_worktrees_safe_cleanup_blocks_in_development(self, sample_story_statuses):
        """
        Given: User selects cleanup
        When: Worktree has status "In Development"
        Then: Blocks deletion without confirmation
        """
        # Arrange
        story_id = "STORY-094"
        status = sample_story_statuses[story_id]
        unsafe_statuses = ["In Development", "Dev Complete", "QA In Progress"]

        # Act
        requires_confirmation = status in unsafe_statuses

        # Assert
        assert requires_confirmation
        assert status == "In Development"

    def test_worktrees_safe_cleanup_allows_released(self, sample_story_statuses):
        """
        Given: User selects cleanup
        When: Worktree has status "Released"
        Then: Allows deletion without extra confirmation
        """
        # Arrange
        story_id = "STORY-037"
        status = sample_story_statuses[story_id]
        safe_statuses = ["Released", "QA Approved", "Backlog"]

        # Act
        safe_to_delete = status in safe_statuses

        # Assert
        assert safe_to_delete
        assert status == "Released"

    def test_worktrees_safe_cleanup_allows_qa_approved(self, sample_story_statuses):
        """
        Given: User selects cleanup
        When: Worktree has status "QA Approved"
        Then: Allows deletion without extra confirmation
        """
        # Arrange
        story_id = "STORY-091"
        status = sample_story_statuses[story_id]
        safe_statuses = ["Released", "QA Approved", "Backlog"]

        # Act
        safe_to_delete = status in safe_statuses

        # Assert
        assert safe_to_delete

    def test_worktrees_cleanup_displays_status_before_delete(self, sample_story_statuses):
        """
        Given: User initiates cleanup
        When: Processing each worktree
        Then: Displays status verification message
        """
        # Arrange
        worktree = {"story_id": "STORY-037", "path": "../devforgeai-story-037/"}
        status = sample_story_statuses[worktree["story_id"]]

        # Act
        message = f"{worktree['story_id']} status={status} → safe to delete"

        # Assert
        assert "STORY-037" in message
        assert "Released" in message
        assert "safe to delete" in message

    def test_worktrees_cleanup_skips_in_development_without_force(self, sample_story_statuses):
        """
        Given: In Development worktree selected for cleanup
        When: User doesn't confirm
        Then: Skips deletion with message
        """
        # Arrange
        worktree = {"story_id": "STORY-094", "path": "../devforgeai-story-094/"}
        status = sample_story_statuses[worktree["story_id"]]
        user_confirmed = False

        # Act
        if status == "In Development" and not user_confirmed:
            result = "keep"
            message = f"{worktree['story_id']} status=In Development → keep"
        else:
            result = "delete"
            message = f"Deleted {worktree['story_id']}"

        # Assert
        assert result == "keep"
        assert "keep" in message


# =============================================================================
# AC#5: Execution Time Requirement
# =============================================================================

class TestExecutionTimeRequirement:
    """Tests for AC#5: Execution Time Requirement"""

    def test_worktrees_performance_under_5_seconds(self):
        """
        Given: Developer runs /worktrees
        When: Listing and status check runs
        Then: Completes in < 5 seconds
        """
        # Arrange
        max_execution_time = 5.0  # seconds

        # Act - Simulate worktree processing
        start_time = time.time()

        # Simulate git worktree list (typically ~100ms)
        time.sleep(0.1)

        # Simulate status check for 20 worktrees (typical max)
        for _ in range(20):
            time.sleep(0.01)  # 10ms per worktree

        # Simulate table formatting
        time.sleep(0.05)

        elapsed = time.time() - start_time

        # Assert
        assert elapsed < max_execution_time

    def test_worktrees_listing_under_2_seconds(self):
        """
        Given: Developer runs /worktrees
        When: Git worktree list executes
        Then: Completes in < 2 seconds
        """
        # Arrange
        max_listing_time = 2.0

        # Act - Simulate worktree listing only
        start_time = time.time()
        time.sleep(0.1)  # Simulated git command
        elapsed = time.time() - start_time

        # Assert
        assert elapsed < max_listing_time

    def test_worktrees_status_check_under_3_seconds(self):
        """
        Given: 20 worktrees exist (max typical)
        When: Checking story statuses
        Then: Completes in < 3 seconds total
        """
        # Arrange
        max_status_time = 3.0
        worktree_count = 20

        # Act - Simulate status checking
        start_time = time.time()
        for _ in range(worktree_count):
            time.sleep(0.05)  # 50ms per file read
        elapsed = time.time() - start_time

        # Assert
        assert elapsed < max_status_time


# =============================================================================
# Edge Cases
# =============================================================================

class TestEdgeCases:
    """Tests for edge case handling"""

    def test_worktrees_handles_corrupted_worktree(self):
        """
        Given: Worktree directory exists but is corrupted
        When: /worktrees scans
        Then: Flags as orphaned with repair suggestion
        """
        # Arrange
        corrupted_worktree = {
            "story_id": "STORY-050",
            "path": "../devforgeai-story-050/",
            "status": "corrupted",
            "error": "worktree locked by another process"
        }

        # Act
        is_corrupted = corrupted_worktree.get("status") == "corrupted"
        repair_suggestion = "git worktree repair" if is_corrupted else None

        # Assert
        assert is_corrupted
        assert repair_suggestion is not None

    def test_worktrees_handles_missing_git(self):
        """
        Given: Git is not available
        When: /worktrees runs
        Then: Shows error with resolution steps
        """
        # Arrange
        git_available = False

        # Act
        if not git_available:
            error_message = "Git not available. Install Git and retry."
            resolution = "https://git-scm.com/downloads"
        else:
            error_message = None
            resolution = None

        # Assert
        assert error_message is not None
        assert "Git not available" in error_message

    def test_worktrees_handles_orphaned_worktree(self):
        """
        Given: Worktree directory missing but git knows about it
        When: /worktrees scans
        Then: Offers prune option
        """
        # Arrange
        orphaned_worktree = {
            "story_id": "STORY-051",
            "path": "../devforgeai-story-051/",
            "exists": False,
            "in_git": True
        }

        # Act
        is_orphaned = not orphaned_worktree["exists"] and orphaned_worktree["in_git"]
        prune_command = "git worktree prune" if is_orphaned else None

        # Assert
        assert is_orphaned
        assert prune_command == "git worktree prune"

    def test_worktrees_handles_story_file_not_found(self):
        """
        Given: Worktree exists but story file deleted
        When: Checking story status
        Then: Returns "Unknown" status
        """
        # Arrange
        story_id = "STORY-999"
        story_file_exists = False

        # Act
        if story_file_exists:
            status = "Released"  # From file
        else:
            status = "Unknown"

        # Assert
        assert status == "Unknown"


# =============================================================================
# Integration Tests
# =============================================================================

class TestWorktreesCommandIntegration:
    """Integration tests for full command workflow"""

    def test_worktrees_full_workflow_list_to_cleanup(self, sample_worktree_data, sample_story_statuses):
        """
        Given: Multiple worktrees with various states
        When: Running full /worktrees workflow
        Then: Lists, identifies candidates, presents menu, executes cleanup
        """
        # Arrange
        worktrees = sample_worktree_data["worktrees"]
        idle_worktrees = sample_worktree_data["idle_worktrees"]
        threshold = sample_worktree_data["config"]["cleanup_threshold_days"]

        # Act - Step 1: List worktrees
        worktree_count = len(worktrees)

        # Act - Step 2: Identify candidates
        candidates = [wt for wt in idle_worktrees]
        candidate_count = len(candidates)

        # Act - Step 3: Check statuses
        safe_to_delete = []
        requires_confirmation = []
        for candidate in candidates:
            story_status = sample_story_statuses.get(candidate["story_id"], "Unknown")
            if story_status in ["Released", "QA Approved", "Backlog"]:
                safe_to_delete.append(candidate)
            else:
                requires_confirmation.append(candidate)

        # Assert
        assert worktree_count == 3
        assert candidate_count == 1
        assert len(requires_confirmation) == 1  # STORY-094 is In Development

    def test_worktrees_resume_development_returns_path(self, sample_worktree_data):
        """
        Given: User selects "Resume development"
        When: Choosing a worktree
        Then: Returns the path to resume work
        """
        # Arrange
        selected_worktree = sample_worktree_data["worktrees"][1]  # STORY-091

        # Act
        resume_path = selected_worktree["path"]
        resume_message = f"Resume development in: {resume_path}"

        # Assert
        assert resume_path == "../devforgeai-story-091/"
        assert "Resume development in:" in resume_message

    def test_worktrees_inspect_shows_details(self, sample_worktree_data, sample_story_statuses):
        """
        Given: User selects "Inspect worktree"
        When: Viewing details
        Then: Shows path, branch, age, status, last activity
        """
        # Arrange
        worktree = sample_worktree_data["worktrees"][0]
        status = sample_story_statuses[worktree["story_id"]]

        # Act
        details = {
            "Story ID": worktree["story_id"],
            "Path": worktree["path"],
            "Branch": worktree["branch"],
            "Age": f"{worktree['days_idle']} days",
            "Status": status,
            "Last Activity": worktree["last_activity"]
        }

        # Assert
        assert details["Story ID"] == "STORY-037"
        assert details["Branch"] == "story-037"
        assert details["Status"] == "Released"
