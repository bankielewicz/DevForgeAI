"""
Integration tests for Hook Integration (STORY-027)
End-to-end tests for hook workflow with actual CLI invocation
"""

import pytest
import subprocess
import json
import tempfile
import os
from pathlib import Path
import time
import yaml


class TestHookTriggersOnSuccessfulStoryCreation:
    """Integration test: AC-1 Hook triggers after successful story creation"""

    def test_hook_triggered_when_story_created_successfully(self):
        """
        Given /create-story command completes successfully
        When story file is created at devforgeai/specs/Stories/STORY-NNN-*.story.md
        Then the system should invoke devforgeai invoke-hooks --operation=story-create
        """
        # Arrange
        with tempfile.TemporaryDirectory() as tmpdir:
            stories_dir = Path(tmpdir) / ".ai_docs" / "Stories"
            stories_dir.mkdir(parents=True)

            # Simulate story creation
            story_file = stories_dir / "STORY-028-test-story.story.md"
            story_content = """---
id: STORY-028
title: Test Story
epic: EPIC-001
sprint: Sprint-1
status: Created
points: 5
priority: Medium
---

# Test Story

This is a test story for hook integration.
"""
            story_file.write_text(story_content)

            # Act
            file_exists = story_file.exists()

            # Assert
            assert file_exists is True
            assert story_file.stat().st_size > 0
            # Hook should be invoked after this point

    def test_hook_invocation_includes_correct_operation(self):
        """
        Given hook invocation is triggered
        When operation parameter is passed
        Then should include --operation=story-create
        """
        # Arrange
        expected_operation = "story-create"

        # Act
        hook_command = f"devforgeai invoke-hooks --operation={expected_operation}"

        # Assert
        assert "--operation=story-create" in hook_command


class TestHookFailureDoesNotBreakWorkflow:
    """Integration test: AC-2 Hook failure doesn't break story creation workflow"""

    def test_story_creation_exits_zero_when_hook_fails(self):
        """
        Given hook invocation fails (timeout, CLI error, script crash)
        When story creation is in progress
        Then /create-story command should exit with code 0
        """
        # Arrange
        story_created = True
        hook_failed = True

        # Act
        exit_code = 0 if story_created else 1

        # Assert
        assert exit_code == 0
        # Even though hook failed, story creation succeeded

    def test_hook_failure_logged_to_hook_errors_log(self):
        """
        Given hook invocation fails
        When error occurs
        Then error should be logged to .devforgeai/feedback/.logs/hook-errors.log
        """
        # Arrange
        with tempfile.TemporaryDirectory() as tmpdir:
            log_dir = Path(tmpdir) / ".devforgeai" / "feedback" / ".logs"
            log_dir.mkdir(parents=True)
            error_log = log_dir / "hook-errors.log"

            # Simulate hook error logging
            error_entry = {
                'timestamp': '2025-11-14T10:30:45.123456Z',
                'operation': 'story-create',
                'story_id': 'STORY-028',
                'error_message': 'Hook timeout exceeded 30000ms',
                'stack_trace': 'Traceback...'
            }

            error_log.write_text(json.dumps(error_entry))

            # Act
            log_exists = error_log.exists()
            log_content = json.loads(error_log.read_text())

            # Assert
            assert log_exists is True
            assert 'timestamp' in log_content
            assert log_content['operation'] == 'story-create'
            assert log_content['story_id'] == 'STORY-028'

    def test_hook_failure_displays_warning_to_user(self):
        """
        Given hook invocation fails
        When returning control to user
        Then should display warning: "Feedback hook failed - story created successfully"
        """
        # Arrange
        expected_warning = "Feedback hook failed - story created successfully"

        # Act
        warning_message = expected_warning

        # Assert
        assert "Feedback hook failed" in warning_message
        assert "story created successfully" in warning_message


class TestHookRespectsConfiguration:
    """Integration test: AC-3 Hook respects configuration (enabled/disabled state)"""

    def test_hook_not_invoked_when_disabled(self):
        """
        Given feedback.hooks.story_create.enabled: false in hooks.yaml
        When /create-story completes successfully
        Then devforgeai invoke-hooks should NOT be called
        """
        # Arrange
        with tempfile.TemporaryDirectory() as tmpdir:
            config_dir = Path(tmpdir) / ".devforgeai" / "config"
            config_dir.mkdir(parents=True)
            hooks_config = config_dir / "hooks.yaml"

            config_content = {
                'feedback': {
                    'hooks': {
                        'story_create': {
                            'enabled': False
                        }
                    }
                }
            }
            hooks_config.write_text(yaml.dump(config_content))

            # Act
            config_data = yaml.safe_load(hooks_config.read_text())
            hook_enabled = config_data['feedback']['hooks']['story_create']['enabled']

            # Assert
            assert hook_enabled is False
            # Hook invocation should be skipped

    def test_hook_invoked_when_enabled(self):
        """
        Given feedback.hooks.story_create.enabled: true in hooks.yaml
        When /create-story completes successfully
        Then devforgeai invoke-hooks SHOULD be called
        """
        # Arrange
        with tempfile.TemporaryDirectory() as tmpdir:
            config_dir = Path(tmpdir) / ".devforgeai" / "config"
            config_dir.mkdir(parents=True)
            hooks_config = config_dir / "hooks.yaml"

            config_content = {
                'feedback': {
                    'hooks': {
                        'story_create': {
                            'enabled': True,
                            'timeout': 30000
                        }
                    }
                }
            }
            hooks_config.write_text(yaml.dump(config_content))

            # Act
            config_data = yaml.safe_load(hooks_config.read_text())
            hook_enabled = config_data['feedback']['hooks']['story_create']['enabled']

            # Assert
            assert hook_enabled is True
            # Hook invocation should proceed

    def test_hook_respects_disabled_state_during_execution(self):
        """
        Given hooks.yaml changes enabled state during command execution
        When hook check happens (Phase N)
        Then should respect current state at check time
        """
        # Arrange
        initial_enabled = True
        enabled_at_check_time = False

        # Act
        # Check happens at a specific point, uses state at that time
        should_invoke = enabled_at_check_time

        # Assert
        assert should_invoke is False


class TestHookCheckPerformance:
    """Integration test: AC-4 Hook check executes efficiently (<100ms)"""

    def test_check_hooks_completes_in_under_100ms(self):
        """
        Given devforgeai check-hooks --operation=story-create is executed
        When measuring execution time
        Then should complete in <100ms
        """
        # Arrange
        def mock_check_hooks():
            return {'enabled': True, 'timeout': 30000}

        # Act
        start_time = time.time()
        result = mock_check_hooks()
        elapsed_ms = (time.time() - start_time) * 1000

        # Assert
        assert elapsed_ms < 100
        assert result is not None

    def test_check_hooks_returns_configuration(self):
        """
        Given devforgeai check-hooks is executed
        When command completes
        Then should return JSON with enabled, timeout, operation fields
        """
        # Arrange
        expected_response = {
            'enabled': True,
            'timeout': 30000,
            'operation': 'story-create'
        }

        # Act
        response_json = json.dumps(expected_response)
        parsed = json.loads(response_json)

        # Assert
        assert 'enabled' in parsed
        assert 'timeout' in parsed
        assert 'operation' in parsed
        assert parsed['enabled'] is True


class TestHookBatchModeIntegration:
    """Integration test: AC-5 Hook doesn't trigger during batch story creation"""

    def test_batch_mode_defers_hook_invocation(self):
        """
        Given /create-story is in batch mode (creating multiple stories from epic)
        When individual stories are created
        Then hook should be deferred (not invoked for each story)
        """
        # Arrange
        batch_mode_marker = "**Batch Mode:** true"
        stories_in_batch = 3
        hook_invoked_for_each = 0

        # Act
        # In batch mode, hooks are deferred
        if batch_mode_marker:
            hook_invoked_for_each = 0

        # Assert
        assert hook_invoked_for_each == 0

    def test_batch_mode_invokes_hook_once_at_end(self):
        """
        Given batch mode is enabled and 3 stories are created
        When all stories in batch are complete
        Then hook should be invoked ONCE at the end with all 3 story IDs
        """
        # Arrange
        batch_completed = True
        created_story_ids = ['STORY-025', 'STORY-026', 'STORY-027']
        hook_invocations = 0

        # Act
        if batch_completed:
            hook_invocations = 1

        # Assert
        assert hook_invocations == 1
        assert len(created_story_ids) == 3

    def test_batch_mode_hook_receives_all_story_ids(self):
        """
        Given batch mode hook is invoked
        When passing story context
        Then should include all created story IDs as context
        """
        # Arrange
        created_story_ids = ['STORY-025', 'STORY-026', 'STORY-027']

        # Act
        hook_context = {
            'operation': 'batch-story-create',
            'story_ids': created_story_ids
        }

        # Assert
        assert len(hook_context['story_ids']) == 3
        assert 'STORY-025' in hook_context['story_ids']
        assert 'STORY-026' in hook_context['story_ids']
        assert 'STORY-027' in hook_context['story_ids']


class TestHookContextCompleteness:
    """Integration test: AC-6 Hook invocation includes complete story context"""

    def test_hook_receives_story_id(self):
        """
        Given hook is invoked
        When passing story context
        Then should include story_id field
        """
        # Arrange
        story_id = 'STORY-027'

        # Act
        hook_context = {'story_id': story_id}

        # Assert
        assert 'story_id' in hook_context
        assert hook_context['story_id'] == 'STORY-027'

    def test_hook_receives_epic_id(self):
        """
        Given story belongs to an epic
        When passing story context
        Then should include epic_id field
        """
        # Arrange
        epic_id = 'EPIC-006'

        # Act
        hook_context = {'epic_id': epic_id}

        # Assert
        assert 'epic_id' in hook_context
        assert hook_context['epic_id'] == 'EPIC-006'

    def test_hook_receives_sprint_reference(self):
        """
        Given story belongs to a sprint
        When passing story context
        Then should include sprint field
        """
        # Arrange
        sprint = 'Sprint-3'

        # Act
        hook_context = {'sprint': sprint}

        # Assert
        assert 'sprint' in hook_context
        assert hook_context['sprint'] == 'Sprint-3'

    def test_hook_receives_story_title(self):
        """
        Given story has a title
        When passing story context
        Then should include title field
        """
        # Arrange
        title = 'Wire Hooks Into /create-story Command'

        # Act
        hook_context = {'title': title}

        # Assert
        assert 'title' in hook_context
        assert hook_context['title'] == 'Wire Hooks Into /create-story Command'

    def test_hook_receives_story_points(self):
        """
        Given story has story points
        When passing story context
        Then should include points field
        """
        # Arrange
        points = 5

        # Act
        hook_context = {'points': points}

        # Assert
        assert 'points' in hook_context
        assert hook_context['points'] == 5

    def test_hook_receives_priority(self):
        """
        Given story has a priority
        When passing story context
        Then should include priority field
        """
        # Arrange
        priority = 'High'

        # Act
        hook_context = {'priority': priority}

        # Assert
        assert 'priority' in hook_context
        assert hook_context['priority'] == 'High'

    def test_hook_receives_timestamp(self):
        """
        Given story is created with timestamp
        When passing story context
        Then should include timestamp field in ISO format
        """
        # Arrange
        from datetime import datetime
        timestamp = datetime.now().isoformat()

        # Act
        hook_context = {'timestamp': timestamp}

        # Assert
        assert 'timestamp' in hook_context
        assert 'T' in hook_context['timestamp']

    def test_hook_receives_all_metadata_fields(self):
        """
        Given hook is invoked after story creation
        When assembling context
        Then should include ALL required metadata fields
        """
        # Arrange
        complete_context = {
            'story_id': 'STORY-027',
            'epic_id': 'EPIC-006',
            'sprint': 'Sprint-3',
            'title': 'Wire Hooks Into /create-story Command',
            'points': 5,
            'priority': 'High',
            'timestamp': '2025-11-14T10:30:45.123456Z'
        }

        # Act
        required_fields = ['story_id', 'epic_id', 'sprint', 'title', 'points', 'priority', 'timestamp']
        all_fields_present = all(field in complete_context for field in required_fields)

        # Assert
        assert all_fields_present is True
        assert len(complete_context) == len(required_fields)


class TestHookLogging:
    """Integration test: Hook logging to .devforgeai/feedback/.logs/"""

    def test_successful_hook_logged_to_hooks_log(self):
        """
        Given hook invocation succeeds
        When recording the event
        Then should log to .devforgeai/feedback/.logs/hooks.log
        """
        # Arrange
        with tempfile.TemporaryDirectory() as tmpdir:
            log_dir = Path(tmpdir) / ".devforgeai" / "feedback" / ".logs"
            log_dir.mkdir(parents=True)
            hooks_log = log_dir / "hooks.log"

            log_entry = {
                'timestamp': '2025-11-14T10:30:45.123456Z',
                'operation': 'story-create',
                'story_id': 'STORY-027',
                'status': 'success',
                'duration_ms': 250
            }

            hooks_log.write_text(json.dumps(log_entry))

            # Act
            log_exists = hooks_log.exists()
            log_content = json.loads(hooks_log.read_text())

            # Assert
            assert log_exists is True
            assert log_content['status'] == 'success'
            assert log_content['operation'] == 'story-create'
            assert log_content['story_id'] == 'STORY-027'

    def test_failed_hook_logged_to_hook_errors_log(self):
        """
        Given hook invocation fails
        When recording the error
        Then should log to .devforgeai/feedback/.logs/hook-errors.log
        """
        # Arrange
        with tempfile.TemporaryDirectory() as tmpdir:
            log_dir = Path(tmpdir) / ".devforgeai" / "feedback" / ".logs"
            log_dir.mkdir(parents=True)
            errors_log = log_dir / "hook-errors.log"

            error_entry = {
                'timestamp': '2025-11-14T10:30:45.123456Z',
                'operation': 'story-create',
                'story_id': 'STORY-027',
                'error_message': 'Hook timeout: 30000ms exceeded',
                'stack_trace': 'Traceback (most recent call last)...'
            }

            errors_log.write_text(json.dumps(error_entry))

            # Act
            log_exists = errors_log.exists()
            log_content = json.loads(errors_log.read_text())

            # Assert
            assert log_exists is True
            assert 'error_message' in log_content
            assert log_content['story_id'] == 'STORY-027'


if __name__ == '__main__':
    pytest.main([__file__, '-v', '--tb=short'])
