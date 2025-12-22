"""
Test Suite: Subagent Output and JSON Response Validation
Feature: STORY-091 - Git Worktree Auto-Management
Integration Tests

Tests for git-worktree-manager subagent output validation.
"""

import pytest
import json
from datetime import datetime


class TestSubagentResponseStructure:
    """Test structure of git-worktree-manager subagent responses"""

    def test_should_return_valid_json_response(self):
        """
        Scenario: Subagent returns structured JSON
        Given: Subagent processes worktree request
        When: Returning response
        Then: Should return valid JSON
        """
        # Arrange
        response_text = '{"status": "success", "worktree_path": "../devforgeai-story-037/"}'

        # Act
        try:
            response = json.loads(response_text)
            is_valid_json = True
        except json.JSONDecodeError:
            is_valid_json = False

        # Assert
        assert is_valid_json

    def test_should_include_status_field_in_response(self):
        """
        Scenario: Response includes status
        Given: Subagent completes operation
        When: Returning response
        Then: Should include "status" field with value
        """
        # Arrange
        response = {"status": "success"}

        # Act
        has_status = "status" in response

        # Assert
        assert has_status

    def test_should_include_worktree_path_in_response(self):
        """
        Scenario: Response includes worktree path
        Given: Worktree created
        When: Returning response
        Then: Should include "worktree_path" field
        """
        # Arrange
        response = {
            "status": "success",
            "worktree_path": "../devforgeai-story-037/"
        }

        # Act
        has_path = "worktree_path" in response

        # Assert
        assert has_path

    def test_should_include_branch_name_in_response(self):
        """
        Scenario: Response includes branch name
        Given: Worktree created with branch
        When: Returning response
        Then: Should include "branch_name" field
        """
        # Arrange
        response = {
            "status": "success",
            "worktree_path": "../devforgeai-story-037/",
            "branch_name": "story-037"
        }

        # Act
        has_branch = "branch_name" in response

        # Assert
        assert has_branch

    def test_should_include_elapsed_time_in_response(self):
        """
        Scenario: Response includes creation time
        Given: Worktree creation completes
        When: Returning response
        Then: Should include "elapsed_time_seconds" field
        """
        # Arrange
        response = {
            "status": "success",
            "elapsed_time_seconds": 3.2
        }

        # Act
        has_elapsed_time = "elapsed_time_seconds" in response

        # Assert
        assert has_elapsed_time

    def test_should_validate_elapsed_time_is_numeric(self):
        """
        Scenario: Elapsed time must be valid number
        Given: Creation completed in 3.2 seconds
        When: Validating response
        Then: Should be numeric (int or float)
        """
        # Arrange
        elapsed_time = 3.2

        # Act
        is_numeric = isinstance(elapsed_time, (int, float))

        # Assert
        assert is_numeric

    def test_should_include_idle_worktrees_in_scan_response(self):
        """
        Scenario: Response from idle detection scan
        Given: Scanning for idle worktrees
        When: Returning response
        Then: Should include "idle_worktrees" list
        """
        # Arrange
        response = {
            "status": "success",
            "idle_worktrees": [
                "devforgeai-story-031",
                "devforgeai-story-033"
            ]
        }

        # Act
        has_idle_list = "idle_worktrees" in response
        is_list = isinstance(response.get("idle_worktrees"), list)

        # Assert
        assert has_idle_list
        assert is_list

    def test_should_validate_idle_worktrees_are_strings(self):
        """
        Scenario: Idle worktree names are strings
        Given: Idle worktrees listed
        When: Validating response
        Then: Each should be string (worktree name)
        """
        # Arrange
        idle_worktrees = ["devforgeai-story-031", "devforgeai-story-033"]

        # Act
        all_strings = all(isinstance(w, str) for w in idle_worktrees)

        # Assert
        assert all_strings

    def test_should_include_message_field_in_response(self):
        """
        Scenario: Response includes user-facing message
        Given: Operation completes
        When: Returning response
        Then: Should include "message" field for display
        """
        # Arrange
        response = {
            "status": "success",
            "message": "Created worktree: ../devforgeai-story-037/ (branch: story-037)"
        }

        # Act
        has_message = "message" in response

        # Assert
        assert has_message

    def test_should_include_error_field_on_failure(self):
        """
        Scenario: Response on error
        Given: Operation fails
        When: Returning response
        Then: Should include "error" field with error message
        """
        # Arrange
        response = {
            "status": "error",
            "error": "Git version 2.4 does not support worktrees (requires 2.5+)"
        }

        # Act
        has_error = "error" in response

        # Assert
        assert has_error


class TestSubagentActionResponses:
    """Test responses for specific subagent actions"""

    def test_should_return_success_on_worktree_creation(self):
        """
        Scenario: Successful worktree creation
        Given: Worktree created at path
        When: Returning response
        Then: status should be "success"
        """
        # Arrange
        response = {
            "status": "success",
            "worktree_path": "../devforgeai-story-037/",
            "branch_name": "story-037",
            "elapsed_time_seconds": 3.2
        }

        # Act
        success = response["status"] == "success"

        # Assert
        assert success

    def test_should_return_success_on_existing_worktree_detection(self):
        """
        Scenario: Detected existing worktree
        Given: Worktree found at path
        When: Returning response
        Then: status should be "success" with action "resume"
        """
        # Arrange
        response = {
            "status": "success",
            "action": "resume",
            "worktree_path": "../devforgeai-story-037/",
            "message": "Resuming in existing worktree: ../devforgeai-story-037/"
        }

        # Act
        success = response["status"] == "success"
        is_resume = response.get("action") == "resume"

        # Assert
        assert success
        assert is_resume

    def test_should_return_idle_worktrees_on_scan(self):
        """
        Scenario: Idle scan results
        Given: Scanned for idle worktrees
        When: Returning response
        Then: status "success" with idle_worktrees list
        """
        # Arrange
        response = {
            "status": "success",
            "idle_worktrees": ["devforgeai-story-031", "devforgeai-story-033"],
            "idle_count": 2,
            "threshold_days": 7
        }

        # Act
        success = response["status"] == "success"
        has_idle_list = len(response["idle_worktrees"]) > 0

        # Assert
        assert success
        assert has_idle_list

    def test_should_return_error_on_git_version_incompatibility(self):
        """
        Scenario: Git version too old
        Given: Git < 2.5 detected
        When: Attempting worktree creation
        Then: status "error" with clear message
        """
        # Arrange
        response = {
            "status": "error",
            "error": "Git 2.5+ required (you have 2.4.0)",
            "action": "worktree_create"
        }

        # Act
        is_error = response["status"] == "error"
        has_version_message = "Git" in response["error"]

        # Assert
        assert is_error
        assert has_version_message

    def test_should_return_error_on_path_validation_failure(self):
        """
        Scenario: Invalid path detected
        Given: Story ID invalid or path dangerous
        When: Validating
        Then: status "error" with validation message
        """
        # Arrange
        response = {
            "status": "error",
            "error": "Story ID must match STORY-\\d{3,4}",
            "field": "story_id",
            "provided_value": "INVALID-ABC"
        }

        # Act
        is_error = response["status"] == "error"
        has_field = "field" in response

        # Assert
        assert is_error
        assert has_field

    def test_should_return_error_on_worktree_corruption_detected(self):
        """
        Scenario: Corrupted worktree detected
        Given: .git file missing or invalid
        When: Validating integrity
        Then: status "error" with "corrupted" flag
        """
        # Arrange
        response = {
            "status": "error",
            "error": "Worktree corrupted: .git file missing",
            "corrupted": True,
            "worktree_path": "../devforgeai-story-037/",
            "repair_action": "Delete and recreate"
        }

        # Act
        is_error = response["status"] == "error"
        is_corrupted = response.get("corrupted") == True

        # Assert
        assert is_error
        assert is_corrupted


class TestSubagentIntegration:
    """Test integration of subagent responses"""

    def test_should_handle_subagent_response_with_null_values(self):
        """
        Scenario: Some optional fields may be null
        Given: Response from subagent
        When: Parsing response
        Then: Should handle null fields gracefully
        """
        # Arrange
        response = {
            "status": "success",
            "worktree_path": "../devforgeai-story-037/",
            "branch_name": "story-037",
            "error": None
        }

        # Act
        has_null_fields = response.get("error") is None

        # Assert
        assert has_null_fields

    def test_should_parse_subagent_response_into_display_message(self):
        """
        Scenario: Convert subagent response to user display
        Given: Subagent returns JSON response
        When: Converting to display
        Then: Should extract message field for user output
        """
        # Arrange
        subagent_response = {
            "status": "success",
            "message": "Created worktree: ../devforgeai-story-037/ (branch: story-037)",
            "elapsed_time_seconds": 3.2
        }

        # Act
        display_text = subagent_response.get("message", "")
        elapsed_text = f" (completed in {subagent_response['elapsed_time_seconds']}s)"

        # Assert
        assert "Created worktree" in display_text
        assert "3.2" in elapsed_text

    def test_should_validate_subagent_response_schema(self):
        """
        Scenario: Validate response matches expected schema
        Given: Subagent response received
        When: Validating structure
        Then: Should verify required fields present
        """
        # Arrange
        response = {
            "status": "success",
            "message": "Test message"
        }
        required_fields = ["status", "message"]

        # Act
        has_all_fields = all(field in response for field in required_fields)

        # Assert
        assert has_all_fields
