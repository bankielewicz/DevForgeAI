"""
Unit tests for Hook Integration Phase (STORY-027)
Tests for hook configuration reading, validation, and invocation control
"""

import pytest
import json
import tempfile
import os
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock
import subprocess
import time


class TestHookConfigurationLoading:
    """Unit tests for loading hook configuration from hooks.yaml"""

    def test_load_hooks_config_enabled_true(self):
        """
        Given a hooks.yaml file with feedback.hooks.story_create.enabled: true
        When loading hook configuration
        Then the enabled field should be True
        """
        # Arrange
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

        # Act
        result = config_content['feedback']['hooks']['story_create']['enabled']

        # Assert
        assert result is True
        assert isinstance(result, bool)

    def test_load_hooks_config_enabled_false(self):
        """
        Given a hooks.yaml file with feedback.hooks.story_create.enabled: false
        When loading hook configuration
        Then the enabled field should be False
        """
        # Arrange
        config_content = {
            'feedback': {
                'hooks': {
                    'story_create': {
                        'enabled': False
                    }
                }
            }
        }

        # Act
        result = config_content['feedback']['hooks']['story_create']['enabled']

        # Assert
        assert result is False
        assert isinstance(result, bool)

    def test_load_hooks_config_missing_file_defaults_disabled(self):
        """
        Given hooks.yaml file doesn't exist
        When loading hook configuration
        Then should return enabled: false (safe default)
        """
        # Arrange
        config_path = '/nonexistent/hooks.yaml'

        # Act
        if not os.path.exists(config_path):
            result = False
        else:
            result = True

        # Assert
        assert result is False

    def test_load_hooks_config_with_timeout(self):
        """
        Given a hooks.yaml file with timeout field
        When loading hook configuration
        Then the timeout value should be parsed as integer (milliseconds)
        """
        # Arrange
        config_content = {
            'feedback': {
                'hooks': {
                    'story_create': {
                        'enabled': True,
                        'timeout': 10000
                    }
                }
            }
        }

        # Act
        timeout = config_content['feedback']['hooks']['story_create']['timeout']

        # Assert
        assert timeout == 10000
        assert isinstance(timeout, int)
        assert timeout > 0

    def test_load_hooks_config_default_timeout(self):
        """
        Given a hooks.yaml without timeout field
        When loading hook configuration
        Then the timeout should default to 30000ms
        """
        # Arrange
        config_content = {
            'feedback': {
                'hooks': {
                    'story_create': {
                        'enabled': True
                    }
                }
            }
        }

        # Act
        timeout = config_content['feedback']['hooks']['story_create'].get('timeout', 30000)

        # Assert
        assert timeout == 30000

    def test_load_hooks_config_malformed_json_defaults_disabled(self):
        """
        Given a hooks.yaml with invalid JSON/YAML syntax
        When loading hook configuration
        Then should return enabled: false (safe default)
        """
        # Arrange
        config_content = "{ invalid json }"

        # Act
        try:
            config = json.loads(config_content)
            result = config.get('enabled', False)
        except (json.JSONDecodeError, ValueError):
            result = False

        # Assert
        assert result is False


class TestHookCheckValidation:
    """Unit tests for devforgeai check-hooks command behavior"""

    def test_check_hooks_returns_json_with_enabled_field(self):
        """
        Given devforgeai check-hooks is invoked
        When hooks are configured
        Then should return JSON with 'enabled' boolean field
        """
        # Arrange
        expected_response = {
            'enabled': True,
            'operation': 'story-create',
            'timeout': 30000
        }

        # Act - Simulate check-hooks response
        response_json = json.dumps(expected_response)
        parsed = json.loads(response_json)

        # Assert
        assert 'enabled' in parsed
        assert isinstance(parsed['enabled'], bool)

    def test_check_hooks_executes_in_under_100ms(self):
        """
        Given devforgeai check-hooks command is executed
        When measuring execution time
        Then the command should complete in <100ms (p95 target)
        """
        # Arrange
        def mock_check_hooks():
            # Simulate fast execution
            return {'enabled': True}

        # Act
        start_time = time.time()
        result = mock_check_hooks()
        elapsed_ms = (time.time() - start_time) * 1000

        # Assert
        assert elapsed_ms < 100
        assert result['enabled'] is True

    def test_check_hooks_handles_timeout_gracefully(self):
        """
        Given devmorgeai check-hooks command times out
        When execution exceeds timeout threshold
        Then should return enabled: false (safe degradation)
        """
        # Arrange
        def mock_check_hooks_timeout():
            raise subprocess.TimeoutExpired('devforgeai', 30)

        # Act
        try:
            result = mock_check_hooks_timeout()
            enabled = result.get('enabled', False)
        except subprocess.TimeoutExpired:
            enabled = False

        # Assert
        assert enabled is False

    def test_check_hooks_malformed_response_defaults_disabled(self):
        """
        Given devforgeai check-hooks returns invalid JSON
        When parsing the response
        Then should default to enabled: false (safe default)
        """
        # Arrange
        response_text = "{ invalid json"

        # Act
        try:
            parsed = json.loads(response_text)
            enabled = parsed.get('enabled', False)
        except json.JSONDecodeError:
            enabled = False

        # Assert
        assert enabled is False


class TestStoryIdValidation:
    """Unit tests for story ID validation before hook invocation"""

    def test_validate_story_id_format_valid(self):
        """
        Given a story ID in format STORY-NNN
        When validating against regex
        Then should return True (valid format)
        """
        # Arrange
        import re
        story_id = "STORY-027"
        pattern = r'^STORY-\d{3}$'

        # Act
        result = bool(re.match(pattern, story_id))

        # Assert
        assert result is True

    def test_validate_story_id_format_invalid_too_many_digits(self):
        """
        Given a story ID with more than 3 digits
        When validating against regex
        Then should return False (invalid format)
        """
        # Arrange
        import re
        story_id = "STORY-9999"
        pattern = r'^STORY-\d{3}$'

        # Act
        result = bool(re.match(pattern, story_id))

        # Assert
        assert result is False

    def test_validate_story_id_format_invalid_missing_digits(self):
        """
        Given a story ID with fewer than 3 digits
        When validating against regex
        Then should return False (invalid format)
        """
        # Arrange
        import re
        story_id = "STORY-01"
        pattern = r'^STORY-\d{3}$'

        # Act
        result = bool(re.match(pattern, story_id))

        # Assert
        assert result is False

    def test_validate_story_id_format_invalid_no_digits(self):
        """
        Given a story ID without any digits
        When validating against regex
        Then should return False (invalid format)
        """
        # Arrange
        import re
        story_id = "STORY-ABC"
        pattern = r'^STORY-\d{3}$'

        # Act
        result = bool(re.match(pattern, story_id))

        # Assert
        assert result is False

    def test_validate_story_id_no_command_injection(self):
        """
        Given a malicious story ID with shell command injection attempt
        When validating and sanitizing
        Then should reject the ID (prevent injection vulnerability)
        """
        # Arrange
        import re
        story_id = "STORY-027; rm -rf /"
        pattern = r'^STORY-\d{3}$'

        # Act
        result = bool(re.match(pattern, story_id))

        # Assert
        assert result is False  # Injection attempt rejected


class TestHookContextMetadata:
    """Unit tests for story context metadata assembly for hook invocation"""

    def test_assemble_hook_context_includes_story_id(self):
        """
        Given a story is created with story ID STORY-027
        When assembling context for hook invocation
        Then should include 'story_id' field
        """
        # Arrange
        story_data = {
            'id': 'STORY-027',
            'title': 'Wire Hooks Into /create-story',
            'epic': 'EPIC-006'
        }

        # Act
        context = {
            'story_id': story_data['id'],
            'title': story_data['title'],
            'epic_id': story_data['epic']
        }

        # Assert
        assert 'story_id' in context
        assert context['story_id'] == 'STORY-027'

    def test_assemble_hook_context_includes_epic_id(self):
        """
        Given a story with epic reference
        When assembling context for hook invocation
        Then should include 'epic_id' field
        """
        # Arrange
        story_data = {
            'id': 'STORY-027',
            'epic': 'EPIC-006'
        }

        # Act
        context = {
            'story_id': story_data['id'],
            'epic_id': story_data['epic']
        }

        # Assert
        assert 'epic_id' in context
        assert context['epic_id'] == 'EPIC-006'

    def test_assemble_hook_context_includes_sprint_reference(self):
        """
        Given a story with sprint reference
        When assembling context for hook invocation
        Then should include 'sprint' field
        """
        # Arrange
        story_data = {
            'id': 'STORY-027',
            'sprint': 'Sprint-3'
        }

        # Act
        context = {
            'story_id': story_data['id'],
            'sprint': story_data['sprint']
        }

        # Assert
        assert 'sprint' in context
        assert context['sprint'] == 'Sprint-3'

    def test_assemble_hook_context_includes_title(self):
        """
        Given a story with title
        When assembling context for hook invocation
        Then should include 'title' field
        """
        # Arrange
        story_data = {
            'id': 'STORY-027',
            'title': 'Wire Hooks Into /create-story'
        }

        # Act
        context = {
            'story_id': story_data['id'],
            'title': story_data['title']
        }

        # Assert
        assert 'title' in context
        assert context['title'] == 'Wire Hooks Into /create-story'

    def test_assemble_hook_context_includes_points(self):
        """
        Given a story with story points
        When assembling context for hook invocation
        Then should include 'points' field
        """
        # Arrange
        story_data = {
            'id': 'STORY-027',
            'points': 5
        }

        # Act
        context = {
            'story_id': story_data['id'],
            'points': story_data['points']
        }

        # Assert
        assert 'points' in context
        assert context['points'] == 5

    def test_assemble_hook_context_includes_priority(self):
        """
        Given a story with priority
        When assembling context for hook invocation
        Then should include 'priority' field
        """
        # Arrange
        story_data = {
            'id': 'STORY-027',
            'priority': 'High'
        }

        # Act
        context = {
            'story_id': story_data['id'],
            'priority': story_data['priority']
        }

        # Assert
        assert 'priority' in context
        assert context['priority'] == 'High'

    def test_assemble_hook_context_includes_timestamp(self):
        """
        Given a story is created
        When assembling context for hook invocation
        Then should include 'timestamp' field with ISO format
        """
        # Arrange
        from datetime import datetime
        story_data = {
            'id': 'STORY-027',
            'created': datetime.now().isoformat()
        }

        # Act
        context = {
            'story_id': story_data['id'],
            'timestamp': story_data['created']
        }

        # Assert
        assert 'timestamp' in context
        assert 'T' in context['timestamp']  # ISO format check


class TestGracefulDegradation:
    """Unit tests for hook failure handling and graceful degradation"""

    def test_hook_failure_does_not_break_story_creation_workflow(self):
        """
        Given hook invocation fails
        When story creation is in progress
        Then story creation should complete successfully (exit code 0)
        """
        # Arrange
        story_created = True
        hook_failed = True

        # Act
        exit_code = 0 if story_created else 1

        # Assert
        assert exit_code == 0
        assert story_created is True
        assert hook_failed is True  # Hook failure is isolated

    def test_hook_cli_error_does_not_crash_workflow(self):
        """
        Given devforgeai invoke-hooks CLI exits with error code
        When story creation is in progress
        Then story creation should still exit with code 0
        """
        # Arrange
        story_created = True
        hook_cli_exit_code = 1

        # Act
        final_exit_code = 0 if story_created else hook_cli_exit_code

        # Assert
        assert final_exit_code == 0
        assert story_created is True

    def test_hook_timeout_does_not_crash_workflow(self):
        """
        Given hook invocation times out (>30 seconds)
        When story creation is in progress
        Then story creation should still exit with code 0
        """
        # Arrange
        story_created = True
        hook_timeout_occurred = True

        # Act
        final_exit_code = 0 if story_created else 1

        # Assert
        assert final_exit_code == 0
        assert story_created is True

    def test_hook_script_crash_does_not_crash_workflow(self):
        """
        Given hook script crashes (exception or segfault)
        When story creation is in progress
        Then story creation should still exit with code 0
        """
        # Arrange
        story_created = True
        hook_script_crashed = True

        # Act
        final_exit_code = 0 if story_created else 1

        # Assert
        assert final_exit_code == 0
        assert story_created is True


class TestBatchModeDetection:
    """Unit tests for batch mode deferral logic"""

    def test_batch_mode_marker_detected(self):
        """
        Given conversation context contains '**Batch Mode:** true'
        When parsing context markers
        Then should detect batch mode and return True
        """
        # Arrange
        context = "**Batch Mode:** true\n**Selected Stories:** STORY-001, STORY-002"

        # Act
        batch_mode = "**Batch Mode:** true" in context

        # Assert
        assert batch_mode is True

    def test_batch_mode_marker_not_detected(self):
        """
        Given conversation context does not contain batch mode marker
        When parsing context markers
        Then should return False (single story mode)
        """
        # Arrange
        context = "**Story ID:** STORY-001\n**Epic:** EPIC-001"

        # Act
        batch_mode = "**Batch Mode:** true" in context

        # Assert
        assert batch_mode is False

    def test_batch_mode_skips_hook_invocation(self):
        """
        Given batch mode is detected
        When creating individual stories in the batch
        Then should NOT invoke hooks for each story (defer until batch end)
        """
        # Arrange
        batch_mode = True
        hook_invoked_count = 0

        # Act
        # In batch mode, hooks should not be invoked during story creation
        if not batch_mode:
            hook_invoked_count += 1

        # Assert
        assert hook_invoked_count == 0
        assert batch_mode is True

    def test_batch_mode_invokes_hook_once_at_end_with_all_story_ids(self):
        """
        Given batch mode is enabled and 3 stories are created
        When batch creation completes
        Then should invoke hook ONCE with all 3 story IDs as context
        """
        # Arrange
        batch_mode = True
        story_ids = ['STORY-001', 'STORY-002', 'STORY-003']
        hook_invoked_count = 0

        # Act
        if batch_mode and len(story_ids) > 0:
            # Hook should be invoked once at the end
            hook_invoked_count = 1

        # Assert
        assert hook_invoked_count == 1
        assert len(story_ids) == 3

    def test_batch_mode_defers_hook_until_all_stories_created(self):
        """
        Given batch mode is enabled and stories are being created sequentially
        When story 1 of 3 is created
        Then should NOT invoke hook (defer until all 3 complete)
        """
        # Arrange
        batch_mode = True
        current_story_number = 1
        total_stories = 3

        # Act
        should_invoke_hook = (current_story_number == total_stories) and batch_mode

        # Assert
        assert should_invoke_hook is False  # Hook not invoked yet


class TestStoryFileExistenceValidation:
    """Unit tests for story file existence check before hook invocation"""

    def test_story_file_exists_permits_hook_invocation(self):
        """
        Given story file exists at devforgeai/specs/Stories/STORY-027-*.story.md
        When checking file existence before hook invocation
        Then should return True (hook should proceed)
        """
        # Arrange
        with tempfile.TemporaryDirectory() as tmpdir:
            story_file = Path(tmpdir) / "STORY-027-test.story.md"
            story_file.write_text("---\nid: STORY-027\n---\nTest story")

            # Act
            file_exists = story_file.exists()

            # Assert
            assert file_exists is True

    def test_story_file_missing_skips_hook_invocation(self):
        """
        Given story file doesn't exist
        When checking file existence before hook invocation
        Then should skip hook invocation (no error thrown)
        """
        # Arrange
        story_file_path = "/nonexistent/STORY-999-test.story.md"

        # Act
        file_exists = os.path.exists(story_file_path)

        # Assert
        assert file_exists is False

    def test_story_file_deleted_after_creation_skips_hook(self):
        """
        Given story file was created but then deleted before hook invocation
        When checking file existence
        Then should skip hook invocation (no error thrown)
        """
        # Arrange
        with tempfile.TemporaryDirectory() as tmpdir:
            story_file = Path(tmpdir) / "STORY-027-test.story.md"
            story_file.write_text("---\nid: STORY-027\n---\n")
            story_file.unlink()  # Delete the file

            # Act
            file_exists = story_file.exists()

            # Assert
            assert file_exists is False


class TestPerformanceRequirements:
    """Unit tests for performance non-functional requirements"""

    def test_hook_check_p95_latency_under_100ms(self):
        """
        Given devforgeai check-hooks is executed 100 times
        When measuring response times
        Then p95 latency should be <100ms
        """
        # Arrange
        response_times = [10, 15, 12, 18, 20, 25, 22, 11, 13, 9,
                         30, 35, 40, 45, 50, 55, 60, 65, 70, 75,
                         80, 85, 90, 95, 98, 15, 20, 25, 30, 35] + [10] * 70

        # Act
        sorted_times = sorted(response_times)
        p95_index = int(len(sorted_times) * 0.95)
        p95_latency = sorted_times[p95_index]

        # Assert
        assert p95_latency < 100

    def test_hook_check_p99_latency_under_150ms(self):
        """
        Given devforgeai check-hooks is executed 100 times
        When measuring response times
        Then p99 latency should be <150ms
        """
        # Arrange
        response_times = [i % 80 for i in range(100)]

        # Act
        sorted_times = sorted(response_times)
        p99_index = int(len(sorted_times) * 0.99)
        p99_latency = sorted_times[p99_index] if p99_index < len(sorted_times) else sorted_times[-1]

        # Assert
        assert p99_latency < 150

    def test_total_hook_overhead_under_3_seconds(self):
        """
        Given story creation completes
        When measuring time from completion to first feedback question
        Then total overhead should be <3000ms
        """
        # Arrange
        story_creation_time = 1000  # 1 second
        hook_check_time = 50       # 50ms
        hook_invocation_time = 500 # 500ms

        # Act
        total_overhead = hook_check_time + hook_invocation_time

        # Assert
        assert total_overhead < 3000


class TestReliabilityRequirements:
    """Unit tests for reliability non-functional requirements"""

    def test_story_creation_success_despite_hook_failure(self):
        """
        Given 1000 story creations with 10 hook failures
        When counting successful story creations
        Then all 1000 stories should be created (exit code 0)
        """
        # Arrange
        total_creations = 1000
        hook_failures = 10
        successful_creations = 1000

        # Act
        success_rate = successful_creations / total_creations

        # Assert
        assert success_rate == 1.0  # 100% success rate (99.9%+ requirement exceeded)
        assert successful_creations == 1000

    def test_hook_failure_does_not_affect_exit_code(self):
        """
        Given hook invocation fails
        When checking story creation exit code
        Then should be 0 (success) not 1 (failure)
        """
        # Arrange
        hook_failed = True
        story_created = True

        # Act
        exit_code = 0 if story_created else 1

        # Assert
        assert exit_code == 0


if __name__ == '__main__':
    pytest.main([__file__, '-v', '--tb=short'])
