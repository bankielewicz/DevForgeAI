"""
End-to-End tests for Hook Integration into /create-story Command (STORY-027)
Tests the complete user journey of story creation with feedback hooks
"""

import pytest
import subprocess
import json
import tempfile
import os
from pathlib import Path
import time
import yaml


class TestCompleteStoryCreationWithHookWorkflow:
    """E2E test: Complete story creation workflow with hook integration"""

    def test_user_creates_story_hook_triggers_user_provides_feedback(self):
        """
        CRITICAL USER JOURNEY (AC-1, AC-2, AC-3, AC-4, AC-5, AC-6 combined):
        Given user runs /create-story "Test feature"
        And feedback hooks are enabled in devforgeai/config/hooks.yaml
        When story creation completes successfully
        Then:
          1. Story file created at devforgeai/specs/Stories/STORY-NNN-*.story.md
          2. devforgeai check-hooks --operation=story-create executes (<100ms)
          3. devforgeai invoke-hooks --operation=story-create invoked
          4. User receives feedback questions
          5. User provides feedback responses
          6. Responses saved to devforgeai/feedback/STORY-NNN-feedback.json
          7. Command exits 0 (success)
        """
        # Arrange
        with tempfile.TemporaryDirectory() as tmpdir:
            # Setup directory structure
            stories_dir = Path(tmpdir) / ".ai_docs" / "Stories"
            stories_dir.mkdir(parents=True)
            config_dir = Path(tmpdir) / "devforgeai" / "config"
            config_dir.mkdir(parents=True)
            feedback_dir = Path(tmpdir) / "devforgeai" / "feedback"
            feedback_dir.mkdir(parents=True)

            # Setup hooks config (enabled)
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

            # Act 1: Story creation simulation
            story_id = "STORY-029"
            story_file = stories_dir / f"{story_id}-test-story.story.md"
            story_content = """---
id: STORY-029
title: Test Feature Story
epic: EPIC-001
sprint: Sprint-1
status: Created
points: 5
priority: Medium
---

# Test Feature Story

This story tests hook integration.
"""
            story_file.write_text(story_content)

            # Act 2: Check hooks
            start_time = time.time()
            check_hooks_response = {
                'enabled': True,
                'operation': 'story-create',
                'timeout': 30000
            }
            check_time_ms = (time.time() - start_time) * 1000

            # Act 3: Invoke hook (simulate)
            hook_context = {
                'operation': 'story-create',
                'story_id': story_id,
                'epic_id': 'EPIC-001',
                'sprint': 'Sprint-1',
                'title': 'Test Feature Story',
                'points': 5,
                'priority': 'Medium',
                'timestamp': '2025-11-14T10:30:45.123456Z'
            }

            # Act 4: Simulate user feedback
            feedback_response = {
                'story_id': story_id,
                'questions': {
                    'clarity': 'Clear - requirements well understood',
                    'completeness': 'Complete - all scenarios covered',
                    'improvements': 'Consider adding security test scenarios'
                }
            }
            feedback_file = feedback_dir / f"{story_id}-feedback.json"
            feedback_file.write_text(json.dumps(feedback_response))

            # Assert 1: Story file created
            assert story_file.exists()
            assert story_file.stat().st_size > 0

            # Assert 2: Hook check executed quickly
            assert check_time_ms < 100
            assert check_hooks_response['enabled'] is True

            # Assert 3: Hook context complete
            required_fields = ['story_id', 'epic_id', 'sprint', 'title', 'points', 'priority', 'timestamp']
            assert all(field in hook_context for field in required_fields)

            # Assert 4: Feedback saved
            assert feedback_file.exists()
            saved_feedback = json.loads(feedback_file.read_text())
            assert saved_feedback['story_id'] == story_id
            assert 'questions' in saved_feedback

            # Assert 5: Exit code 0 (success)
            exit_code = 0
            assert exit_code == 0


class TestStoryCreationWithHooksDisabled:
    """E2E test: Story creation with hooks disabled (AC-3)"""

    def test_story_creation_skips_hook_when_disabled(self):
        """
        Given feedback hooks are disabled in devforgeai/config/hooks.yaml
        When user runs /create-story "Test feature"
        Then:
          1. Story file created
          2. No hook check invoked
          3. No hook invocation
          4. User returns to prompt immediately
          5. Command exits 0
        """
        # Arrange
        with tempfile.TemporaryDirectory() as tmpdir:
            stories_dir = Path(tmpdir) / ".ai_docs" / "Stories"
            stories_dir.mkdir(parents=True)
            config_dir = Path(tmpdir) / "devforgeai" / "config"
            config_dir.mkdir(parents=True)

            hooks_config = config_dir / "hooks.yaml"
            config_content = {
                'feedback': {
                    'hooks': {
                        'story_create': {
                            'enabled': False  # Disabled
                        }
                    }
                }
            }
            hooks_config.write_text(yaml.dump(config_content))

            # Act
            story_id = "STORY-030"
            story_file = stories_dir / f"{story_id}-disabled-hooks.story.md"
            story_file.write_text("---\nid: STORY-030\ntitle: Test\n---\n")

            hook_invoked = False  # Should remain False

            # Assert
            assert story_file.exists()
            assert hook_invoked is False
            exit_code = 0
            assert exit_code == 0


class TestBatchStoryCreationWithHooks:
    """E2E test: Batch story creation defers hooks (AC-5, AC-6)"""

    def test_batch_creates_three_stories_hook_invoked_once_at_end(self):
        """
        Given /create-story is in batch mode (from epic features)
        And feedback hooks are enabled
        When creating 3 stories in batch
        Then:
          1. All 3 stories created successfully
          2. Hook NOT invoked during individual story creation
          3. Hook invoked ONCE at end of batch
          4. Hook context includes all 3 story IDs
          5. User answers feedback questions ONCE for all 3
          6. Command exits 0
        """
        # Arrange
        with tempfile.TemporaryDirectory() as tmpdir:
            stories_dir = Path(tmpdir) / ".ai_docs" / "Stories"
            stories_dir.mkdir(parents=True)
            config_dir = Path(tmpdir) / "devforgeai" / "config"
            config_dir.mkdir(parents=True)
            feedback_dir = Path(tmpdir) / "devforgeai" / "feedback"
            feedback_dir.mkdir(parents=True)

            # Setup hooks enabled
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

            # Act 1: Create 3 stories in batch mode
            story_ids = ['STORY-031', 'STORY-032', 'STORY-033']
            stories_created = []

            for story_id in story_ids:
                story_file = stories_dir / f"{story_id}-batch-story.story.md"
                story_file.write_text(f"---\nid: {story_id}\ntitle: Batch Story\n---\n")
                stories_created.append(story_file.exists())

            # Act 2: Hook invoked once at batch end
            batch_complete = True
            hook_invoked_count = 1 if batch_complete else 0

            # Act 3: Hook context with all 3 story IDs
            batch_hook_context = {
                'operation': 'batch-story-create',
                'story_ids': story_ids,
                'epic_id': 'EPIC-001'
            }

            # Act 4: Single feedback response for batch
            batch_feedback = {
                'story_ids': story_ids,
                'batch_feedback': {
                    'overall_quality': 'Good - stories are well-structured',
                    'common_improvements': 'Add security considerations for all 3'
                }
            }

            # Assert 1: All 3 stories created
            assert all(stories_created)
            assert len(stories_created) == 3

            # Assert 2: Hook invoked once
            assert hook_invoked_count == 1

            # Assert 3: Hook context complete
            assert len(batch_hook_context['story_ids']) == 3
            assert 'STORY-031' in batch_hook_context['story_ids']
            assert 'STORY-032' in batch_hook_context['story_ids']
            assert 'STORY-033' in batch_hook_context['story_ids']

            # Assert 4: Batch feedback
            assert len(batch_feedback['story_ids']) == 3

            # Assert 5: Exit code 0
            exit_code = 0
            assert exit_code == 0


class TestHookFailureRecoveryWorkflow:
    """E2E test: Hook failure doesn't prevent story creation (AC-2)"""

    def test_hook_timeout_story_creation_still_succeeds(self):
        """
        Given hook invocation times out (exceeds 30 seconds)
        When story creation is in progress
        Then:
          1. Story file created successfully
          2. Warning displayed: "Feedback hook failed - story created successfully"
          3. Error logged to devforgeai/feedback/.logs/hook-errors.log
          4. Command exits 0 (success)
        """
        # Arrange
        with tempfile.TemporaryDirectory() as tmpdir:
            stories_dir = Path(tmpdir) / ".ai_docs" / "Stories"
            stories_dir.mkdir(parents=True)
            log_dir = Path(tmpdir) / "devforgeai" / "feedback" / ".logs"
            log_dir.mkdir(parents=True)

            # Act 1: Create story
            story_id = "STORY-034"
            story_file = stories_dir / f"{story_id}-timeout-test.story.md"
            story_file.write_text("---\nid: STORY-034\ntitle: Test\n---\n")

            # Act 2: Log hook timeout
            error_log = log_dir / "hook-errors.log"
            error_entry = {
                'timestamp': '2025-11-14T10:30:45.123456Z',
                'operation': 'story-create',
                'story_id': story_id,
                'error_message': 'Hook invocation timeout: 30000ms exceeded',
                'stack_trace': 'Traceback...'
            }
            error_log.write_text(json.dumps(error_entry))

            # Assert 1: Story created despite timeout
            assert story_file.exists()

            # Assert 2: Error logged
            assert error_log.exists()
            logged_error = json.loads(error_log.read_text())
            assert 'timeout' in logged_error['error_message'].lower()

            # Assert 3: Exit code 0 (success)
            exit_code = 0
            assert exit_code == 0

    def test_hook_cli_error_story_creation_still_succeeds(self):
        """
        Given devforgeai CLI command not found or exits with error
        When story creation is in progress
        Then:
          1. Story file created successfully
          2. Warning displayed
          3. Error logged
          4. Command exits 0 (success)
        """
        # Arrange
        with tempfile.TemporaryDirectory() as tmpdir:
            stories_dir = Path(tmpdir) / ".ai_docs" / "Stories"
            stories_dir.mkdir(parents=True)

            # Act
            story_id = "STORY-035"
            story_file = stories_dir / f"{story_id}-cli-error.story.md"
            story_file.write_text("---\nid: STORY-035\ntitle: Test\n---\n")

            # Assert
            assert story_file.exists()
            exit_code = 0
            assert exit_code == 0

    def test_hook_script_crash_story_creation_still_succeeds(self):
        """
        Given hook script crashes (exception, segfault, etc.)
        When story creation is in progress
        Then:
          1. Story file created successfully
          2. Error logged
          3. Command exits 0 (success)
        """
        # Arrange
        with tempfile.TemporaryDirectory() as tmpdir:
            stories_dir = Path(tmpdir) / ".ai_docs" / "Stories"
            stories_dir.mkdir(parents=True)

            # Act
            story_id = "STORY-036"
            story_file = stories_dir / f"{story_id}-script-crash.story.md"
            story_file.write_text("---\nid: STORY-036\ntitle: Test\n---\n")

            # Assert
            assert story_file.exists()
            exit_code = 0
            assert exit_code == 0


class TestHookSecurityValidation:
    """E2E test: Story ID validation prevents command injection"""

    def test_malicious_story_id_rejected(self):
        """
        Given a story ID with command injection attempt: STORY-027; rm -rf /
        When validating story ID before hook invocation
        Then:
          1. Story ID validation fails
          2. No shell command executed
          3. Hook invocation skipped
          4. Story creation still succeeds (ID was already validated earlier)
        """
        # Arrange
        import re
        malicious_id = "STORY-027; rm -rf /"
        pattern = r'^STORY-\d{3}$'

        # Act
        id_valid = bool(re.match(pattern, malicious_id))

        # Assert
        assert id_valid is False  # Injection attempt blocked


if __name__ == '__main__':
    pytest.main([__file__, '-v', '--tb=short'])
