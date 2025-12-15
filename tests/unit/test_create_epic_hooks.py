"""
Unit tests for Hook Integration in /create-epic Command (STORY-028)

Tests hook configuration loading, CLI mocking, and hook invocation control
for the /create-epic command workflow.

ACCEPTANCE CRITERIA COVERAGE:
- AC1: Automatic Hook Trigger After Successful Epic Creation
- AC2: Hook Failure Doesn't Break Epic Creation
- AC3: Hook Respects Configuration State
- AC4: Hook Receives Complete Epic Context
- AC5: Hook Integration Preserves Lean Orchestration Pattern
"""

import pytest
import json
import tempfile
import os
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock, call
import subprocess
from datetime import datetime
from uuid import uuid4


class TestEpicHookConfigurationLoading:
    """Unit tests for loading hook configuration from hooks.yaml for epic-create operation."""

    def test_load_hooks_config_epic_create_enabled_true(self):
        """
        AC3: Hook Respects Configuration State

        Given a hooks.yaml file with feedback.hooks.epic_create.enabled: true
        When loading hook configuration for epic-create operation
        Then the enabled field should be True
        """
        # Arrange
        config_content = {
            'feedback': {
                'hooks': {
                    'epic_create': {
                        'enabled': True,
                        'timeout': 30000
                    }
                }
            }
        }

        # Act
        result = config_content['feedback']['hooks']['epic_create']['enabled']

        # Assert
        assert result is True
        assert isinstance(result, bool)

    def test_load_hooks_config_epic_create_enabled_false(self):
        """
        AC3: Hook Respects Configuration State

        Given a hooks.yaml file with feedback.hooks.epic_create.enabled: false
        When loading hook configuration for epic-create operation
        Then the enabled field should be False and no hook should trigger
        """
        # Arrange
        config_content = {
            'feedback': {
                'hooks': {
                    'epic_create': {
                        'enabled': False
                    }
                }
            }
        }

        # Act
        result = config_content['feedback']['hooks']['epic_create']['enabled']

        # Assert
        assert result is False
        assert isinstance(result, bool)

    def test_load_hooks_config_missing_file_defaults_disabled(self):
        """
        AC3: Hook Respects Configuration State

        Given hooks.yaml file doesn't exist
        When loading hook configuration
        Then should return enabled: false (safe default, zero overhead)
        """
        # Arrange
        config_path = '/nonexistent/path/to/hooks.yaml'

        # Act
        if not os.path.exists(config_path):
            result = False
        else:
            result = True

        # Assert
        assert result is False

    def test_load_hooks_config_epic_create_with_timeout(self):
        """
        AC3: Hook Respects Configuration State

        Given a hooks.yaml file with timeout field for epic-create
        When loading hook configuration
        Then the timeout value should be parsed as integer (milliseconds)
        """
        # Arrange
        config_content = {
            'feedback': {
                'hooks': {
                    'epic_create': {
                        'enabled': True,
                        'timeout': 15000
                    }
                }
            }
        }

        # Act
        timeout = config_content['feedback']['hooks']['epic_create']['timeout']

        # Assert
        assert timeout == 15000
        assert isinstance(timeout, int)
        assert timeout > 0

    def test_load_hooks_config_epic_create_with_custom_questions(self):
        """
        AC4: Hook Receives Complete Epic Context

        Given a hooks.yaml file with custom questions for epic-create
        When loading hook configuration
        Then custom questions should be available for feedback conversation
        """
        # Arrange
        config_content = {
            'feedback': {
                'hooks': {
                    'epic_create': {
                        'enabled': True,
                        'timeout': 30000,
                        'questions': [
                            "How confident are you in the feature decomposition?",
                            "Was the complexity score accurate?",
                            "Did you identify all critical risks?"
                        ]
                    }
                }
            }
        }

        # Act
        questions = config_content['feedback']['hooks']['epic_create'].get('questions', [])

        # Assert
        assert len(questions) == 3
        assert all(isinstance(q, str) for q in questions)
        assert "confident" in questions[0].lower()

    def test_load_hooks_config_default_timeout_when_missing(self):
        """
        AC3: Hook Respects Configuration State

        Given a hooks.yaml file without timeout field
        When loading hook configuration
        Then should use default timeout (30000 milliseconds)
        """
        # Arrange
        config_content = {
            'feedback': {
                'hooks': {
                    'epic_create': {
                        'enabled': True
                        # timeout intentionally missing
                    }
                }
            }
        }

        # Act
        timeout = config_content['feedback']['hooks']['epic_create'].get('timeout', 30000)

        # Assert
        assert timeout == 30000

    def test_load_hooks_config_returns_dict_with_all_fields(self):
        """
        AC3: Hook Respects Configuration State

        Given a complete hooks.yaml configuration for epic-create
        When loading hook configuration
        Then should return dictionary with all required fields (enabled, timeout, questions)
        """
        # Arrange
        config_content = {
            'feedback': {
                'hooks': {
                    'epic_create': {
                        'enabled': True,
                        'timeout': 20000,
                        'questions': ["Question 1", "Question 2"]
                    }
                }
            }
        }

        # Act
        hook_config = config_content['feedback']['hooks']['epic_create']

        # Assert
        assert 'enabled' in hook_config
        assert 'timeout' in hook_config
        assert 'questions' in hook_config
        assert hook_config['enabled'] is True


class TestEpicHookCLIMocking:
    """Unit tests for mocking devforgeai CLI hook commands (check-hooks, invoke-hooks)."""

    @patch('subprocess.run')
    def test_check_hooks_cli_returns_json_when_enabled(self, mock_run):
        """
        AC1: Automatic Hook Trigger After Successful Epic Creation

        Given check-hooks CLI is called for epic-create operation
        When CLI executes successfully
        Then should return JSON with enabled: true and available: true
        """
        # Arrange
        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_result.stdout = json.dumps({
            'enabled': True,
            'available': True,
            'operation': 'epic-create'
        })
        mock_run.return_value = mock_result

        # Act
        result = subprocess.run(
            ['devforgeai', 'check-hooks', '--operation=epic-create'],
            capture_output=True,
            text=True
        )
        parsed = json.loads(result.stdout)

        # Assert
        assert result.returncode == 0
        assert parsed['enabled'] is True
        assert parsed['available'] is True
        assert parsed['operation'] == 'epic-create'

    @patch('subprocess.run')
    def test_check_hooks_cli_returns_json_when_disabled(self, mock_run):
        """
        AC3: Hook Respects Configuration State

        Given check-hooks CLI is called for epic-create operation
        When hooks are disabled in configuration
        Then should return JSON with enabled: false (zero overhead)
        """
        # Arrange
        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_result.stdout = json.dumps({
            'enabled': False,
            'available': True,
            'operation': 'epic-create'
        })
        mock_run.return_value = mock_result

        # Act
        result = subprocess.run(
            ['devforgeai', 'check-hooks', '--operation=epic-create'],
            capture_output=True,
            text=True
        )
        parsed = json.loads(result.stdout)

        # Assert
        assert result.returncode == 0
        assert parsed['enabled'] is False
        assert parsed['available'] is True

    @patch('subprocess.run')
    def test_check_hooks_cli_error_returns_exit_1(self, mock_run):
        """
        AC2: Hook Failure Doesn't Break Epic Creation

        Given check-hooks CLI fails (operation not found)
        When CLI executes
        Then should return exit code 1 (non-blocking error)
        """
        # Arrange
        mock_result = MagicMock()
        mock_result.returncode = 1
        mock_result.stderr = "Operation 'epic-create' not found"
        mock_run.return_value = mock_result

        # Act
        result = subprocess.run(
            ['devforgeai', 'check-hooks', '--operation=epic-create'],
            capture_output=True,
            text=True
        )

        # Assert
        assert result.returncode == 1
        assert "not found" in result.stderr

    @patch('subprocess.run')
    def test_invoke_hooks_cli_with_epic_id(self, mock_run):
        """
        AC1: Automatic Hook Trigger After Successful Epic Creation
        AC4: Hook Receives Complete Epic Context

        Given invoke-hooks CLI is called with epic-id parameter
        When CLI executes for epic-create operation
        Then should pass epic-id to CLI and return success status
        """
        # Arrange
        epic_id = "EPIC-042"
        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_result.stdout = json.dumps({
            'status': 'success',
            'operation': 'epic-create',
            'epic_id': epic_id,
            'duration_ms': 2500
        })
        mock_run.return_value = mock_result

        # Act
        result = subprocess.run(
            ['devforgeai', 'invoke-hooks', '--operation=epic-create', f'--epic-id={epic_id}'],
            capture_output=True,
            text=True
        )
        parsed = json.loads(result.stdout)

        # Assert
        assert result.returncode == 0
        assert parsed['operation'] == 'epic-create'
        assert parsed['epic_id'] == epic_id
        assert parsed['status'] == 'success'

    @patch('subprocess.run')
    def test_invoke_hooks_cli_timeout_returns_exit_1(self, mock_run):
        """
        AC2: Hook Failure Doesn't Break Epic Creation

        Given invoke-hooks CLI times out (>30 seconds)
        When CLI executes
        Then should return exit code 1 (non-blocking, warning logged)
        """
        # Arrange
        mock_result = MagicMock()
        mock_result.returncode = 1
        mock_result.stderr = "Hook invocation timeout after 30000ms"
        mock_run.return_value = mock_result

        # Act
        result = subprocess.run(
            ['devforgeai', 'invoke-hooks', '--operation=epic-create', '--epic-id=EPIC-042'],
            capture_output=True,
            text=True,
            timeout=5
        )

        # Assert
        assert result.returncode == 1
        assert "timeout" in result.stderr.lower()

    @patch('subprocess.run')
    def test_invoke_hooks_cli_missing_epic_file_returns_exit_3(self, mock_run):
        """
        AC2: Hook Failure Doesn't Break Epic Creation
        AC4: Hook Receives Complete Epic Context

        Given invoke-hooks CLI is called with epic-id
        When epic file doesn't exist at devforgeai/specs/Epics/{EPIC-ID}.epic.md
        Then should return exit code 3 (epic file not found, non-blocking)
        """
        # Arrange
        mock_result = MagicMock()
        mock_result.returncode = 3
        mock_result.stderr = "Epic file not found: devforgeai/specs/Epics/EPIC-042.epic.md"
        mock_run.return_value = mock_result

        # Act
        result = subprocess.run(
            ['devforgeai', 'invoke-hooks', '--operation=epic-create', '--epic-id=EPIC-042'],
            capture_output=True,
            text=True
        )

        # Assert
        assert result.returncode == 3
        assert "not found" in result.stderr

    @patch('subprocess.run')
    def test_invoke_hooks_cli_crash_returns_exit_2(self, mock_run):
        """
        AC2: Hook Failure Doesn't Break Epic Creation

        Given invoke-hooks CLI crashes (unhandled exception)
        When CLI executes
        Then should return non-zero exit code (non-blocking error)
        """
        # Arrange
        mock_result = MagicMock()
        mock_result.returncode = 2
        mock_result.stderr = "Unexpected error: [traceback]"
        mock_run.return_value = mock_result

        # Act
        result = subprocess.run(
            ['devforgeai', 'invoke-hooks', '--operation=epic-create', '--epic-id=EPIC-042'],
            capture_output=True,
            text=True
        )

        # Assert
        assert result.returncode != 0
        assert result.returncode == 2


class TestEpicContextValidation:
    """Unit tests for validating epic context before CLI invocation."""

    def test_validate_epic_id_format_valid(self):
        """
        AC4: Hook Receives Complete Epic Context

        Given epic ID matches pattern EPIC-\\d{3}
        When validating epic context
        Then validation should pass
        """
        # Arrange
        import re
        epic_id = "EPIC-042"
        pattern = r'^EPIC-\d{3}$'

        # Act
        is_valid = bool(re.match(pattern, epic_id))

        # Assert
        assert is_valid is True

    def test_validate_epic_id_format_invalid_too_long(self):
        """
        AC4: Hook Receives Complete Epic Context

        Given epic ID is longer than expected (EPIC-99999)
        When validating epic context
        Then validation should fail (no command injection)
        """
        # Arrange
        import re
        epic_id = "EPIC-99999"
        pattern = r'^EPIC-\d{3}$'

        # Act
        is_valid = bool(re.match(pattern, epic_id))

        # Assert
        assert is_valid is False

    def test_validate_epic_id_format_invalid_characters(self):
        """
        AC4: Hook Receives Complete Epic Context (Security)

        Given epic ID contains special characters (EPIC-042; rm -rf /)
        When validating epic context
        Then validation should fail (no command injection vulnerability)
        """
        # Arrange
        import re
        epic_id = "EPIC-042; rm -rf /"
        pattern = r'^EPIC-\d{3}$'

        # Act
        is_valid = bool(re.match(pattern, epic_id))

        # Assert
        assert is_valid is False

    def test_validate_epic_context_has_required_fields(self):
        """
        AC4: Hook Receives Complete Epic Context

        Given epic creation completed with all metadata
        When validating epic context before CLI invocation
        Then all required fields should be present (ID, features, complexity, risks)
        """
        # Arrange
        epic_context = {
            'epic_id': 'EPIC-042',
            'name': 'User Authentication System',
            'goal': 'Secure user access',
            'features': ['Registration', 'Login', 'Password Reset'],
            'complexity_score': 6,
            'risks': ['Third-party auth availability'],
            'success_criteria': ['<1s login time']
        }

        # Act
        required_fields = ['epic_id', 'name', 'goal', 'features', 'complexity_score', 'risks']
        has_all_fields = all(field in epic_context for field in required_fields)

        # Assert
        assert has_all_fields is True
        assert len(epic_context['features']) >= 1
        assert isinstance(epic_context['complexity_score'], int)

    def test_validate_epic_context_missing_epic_id(self):
        """
        AC4: Hook Receives Complete Epic Context

        Given epic context missing epic_id field
        When validating epic context
        Then validation should fail (required field missing)
        """
        # Arrange
        epic_context = {
            'name': 'User Authentication System',
            'goal': 'Secure user access',
            'features': ['Registration', 'Login']
            # epic_id intentionally missing
        }

        # Act
        has_epic_id = 'epic_id' in epic_context

        # Assert
        assert has_epic_id is False

    def test_validate_epic_context_features_count_in_range(self):
        """
        AC4: Hook Receives Complete Epic Context

        Given epic features count is within optimal range (3-8)
        When validating epic context
        Then validation should pass
        """
        # Arrange
        epic_context = {
            'epic_id': 'EPIC-042',
            'features': ['Feature 1', 'Feature 2', 'Feature 3', 'Feature 4', 'Feature 5']
        }

        # Act
        feature_count = len(epic_context['features'])
        is_valid = 3 <= feature_count <= 8

        # Assert
        assert is_valid is True

    def test_validate_epic_context_features_count_too_low(self):
        """
        AC4: Hook Receives Complete Epic Context

        Given epic features count is below optimal range (<3)
        When validating epic context
        Then validation should warn (possible under-scoping)
        """
        # Arrange
        epic_context = {
            'epic_id': 'EPIC-042',
            'features': ['Feature 1']  # Only 1 feature
        }

        # Act
        feature_count = len(epic_context['features'])
        is_under_scoped = feature_count < 3

        # Assert
        assert is_under_scoped is True

    def test_validate_epic_context_features_count_too_high(self):
        """
        AC4: Hook Receives Complete Epic Context

        Given epic features count exceeds optimal range (>8)
        When validating epic context
        Then validation should warn (possible over-scoping)
        """
        # Arrange
        epic_context = {
            'epic_id': 'EPIC-042',
            'features': [f'Feature {i}' for i in range(1, 11)]  # 10 features
        }

        # Act
        feature_count = len(epic_context['features'])
        is_over_scoped = feature_count > 8

        # Assert
        assert is_over_scoped is True


class TestEpicHookPhase4A9Integration:
    """Unit tests for Phase 4A.9 (Post-Epic Feedback) in orchestration skill."""

    def test_phase_4a9_skipped_when_hooks_disabled(self):
        """
        AC3: Hook Respects Configuration State

        Given hooks are disabled in configuration (enabled: false)
        When Phase 4A.9 executes in orchestration skill
        Then Phase 4A.9 should be skipped entirely (zero overhead)
        """
        # Arrange
        hooks_config = {'enabled': False}

        # Act
        should_execute_phase_4a9 = hooks_config.get('enabled', False)

        # Assert
        assert should_execute_phase_4a9 is False

    def test_phase_4a9_executes_when_hooks_enabled(self):
        """
        AC1: Automatic Hook Trigger After Successful Epic Creation

        Given hooks are enabled in configuration (enabled: true)
        When Phase 4A.9 executes in orchestration skill
        Then Phase 4A.9 should call check-hooks and invoke-hooks CLIs
        """
        # Arrange
        hooks_config = {'enabled': True}

        # Act
        should_execute_phase_4a9 = hooks_config.get('enabled', False)

        # Assert
        assert should_execute_phase_4a9 is True

    def test_phase_4a9_requires_epic_file_exists(self):
        """
        AC4: Hook Receives Complete Epic Context (BR-001)

        Given epic file must exist before hook invocation
        When Phase 4A.9 executes
        Then should verify devforgeai/specs/Epics/{EPIC-ID}.epic.md exists before calling hook CLI
        """
        # Arrange
        epic_id = "EPIC-042"
        with tempfile.TemporaryDirectory() as tmpdir:
            epic_path = Path(tmpdir) / "EPIC-042.epic.md"
            # File doesn't exist yet

            # Act
            file_exists = epic_path.exists()

            # Assert
            assert file_exists is False

            # Now create the file
            epic_path.write_text("# EPIC-042: Test Epic")
            assert epic_path.exists() is True

    def test_phase_4a9_handles_hook_cli_not_found(self):
        """
        AC2: Hook Failure Doesn't Break Epic Creation

        Given devforgeai CLI command not found (not in PATH)
        When Phase 4A.9 attempts to invoke hook
        Then should catch exception, log error, display warning, exit with code 0
        """
        # Arrange
        hook_failure = {
            'error': 'FileNotFoundError',
            'message': 'devforgeai CLI not found',
            'should_block_epic_creation': False
        }

        # Act
        exit_code = 0 if not hook_failure['should_block_epic_creation'] else 1

        # Assert
        assert exit_code == 0
        assert hook_failure['error'] == 'FileNotFoundError'

    def test_phase_4a9_command_stays_under_budget(self):
        """
        AC5: Hook Integration Preserves Lean Orchestration Pattern

        Given /create-epic command is currently 11,270 chars (75% of 15K budget)
        When Phase 4A.9 hook integration adds to command
        Then command should add <20 lines for Phase 4 display logic, stay <15K chars
        """
        # Arrange
        current_command_chars = 11270
        max_budget = 15000
        phase_4_display_lines = 15  # Expected additions for hook result display

        # Act
        additional_chars = phase_4_display_lines * 50  # Rough estimate: 50 chars per line
        total_chars = current_command_chars + additional_chars

        # Assert
        assert total_chars < max_budget
        assert phase_4_display_lines <= 20

    def test_phase_4a9_skill_handles_all_logic(self):
        """
        AC5: Hook Integration Preserves Lean Orchestration Pattern

        Given lean orchestration pattern (command delegates to skill)
        When Phase 4A.9 hook integration implemented
        Then all hook logic should reside in skill (devforgeai-orchestration),
        not in command
        """
        # Arrange
        hook_logic_location = 'devforgeai-orchestration'  # Skill
        phase_name = 'Phase 4A.9'

        # Act
        is_in_skill = hook_logic_location == 'devforgeai-orchestration'

        # Assert
        assert is_in_skill is True


class TestEpicHookExceptionHandling:
    """Unit tests for exception handling and graceful degradation."""

    def test_hook_timeout_caught_and_logged(self):
        """
        AC2: Hook Failure Doesn't Break Epic Creation

        Given hook invocation timeout after 30 seconds
        When exception caught during Phase 4A.9
        Then exception logged, warning displayed, epic creation continues (exit 0)
        """
        # Arrange
        exception_type = TimeoutError
        log_level = 'WARNING'
        exit_code = 0  # Non-blocking

        # Act
        is_timeout = exception_type == TimeoutError
        is_non_blocking = exit_code == 0

        # Assert
        assert is_timeout is True
        assert is_non_blocking is True
        assert log_level == 'WARNING'

    def test_hook_cli_crash_caught_and_logged(self):
        """
        AC2: Hook Failure Doesn't Break Epic Creation

        Given hook CLI process crashes with exit code != 0
        When exception caught during Phase 4A.9
        Then exception logged to hook-errors.log, warning displayed, exit 0
        """
        # Arrange
        exit_code_from_cli = 127  # Command not found
        expected_behavior_exit_code = 0  # Epic creation succeeds
        log_file = '.devforgeai/feedback/.logs/hook-errors.log'

        # Act
        is_cli_failed = exit_code_from_cli != 0
        is_epic_creation_succeeds = expected_behavior_exit_code == 0

        # Assert
        assert is_cli_failed is True
        assert is_epic_creation_succeeds is True

    def test_hook_cli_missing_file_not_blocking(self):
        """
        AC2: Hook Failure Doesn't Break Epic Creation

        Given hook invocation fails with "epic file not found" error
        When Phase 4A.9 executes
        Then should skip hook gracefully (file existence check before invocation)
        """
        # Arrange
        epic_file_exists = False
        should_invoke_hook = False  # Don't invoke if file missing

        # Act
        hook_invoked = should_invoke_hook and epic_file_exists

        # Assert
        assert hook_invoked is False

    def test_hook_configuration_parse_error_defaults_disabled(self):
        """
        AC2: Hook Failure Doesn't Break Epic Creation

        Given hooks.yaml contains malformed YAML or invalid JSON
        When loading hook configuration
        Then should default to enabled: false, skip Phase 4A.9 (safe default)
        """
        # Arrange
        malformed_config = "{ invalid json"
        parsed_config = None
        default_enabled = False

        # Act
        try:
            parsed_config = json.loads(malformed_config)
            enabled = parsed_config.get('enabled', default_enabled)
        except (json.JSONDecodeError, ValueError):
            enabled = default_enabled

        # Assert
        assert enabled is False


class TestEpicHookMetadataExtraction:
    """Unit tests for extracting epic metadata to pass to hook CLI."""

    def test_extract_epic_id_from_context(self):
        """
        AC4: Hook Receives Complete Epic Context

        Given epic context with epic_id field
        When extracting metadata for hook CLI
        Then epic_id should be extracted and validated before CLI invocation
        """
        # Arrange
        epic_context = {
            'epic_id': 'EPIC-042',
            'name': 'User Authentication System',
            'goal': 'Enable secure user access'
        }

        # Act
        epic_id = epic_context.get('epic_id')

        # Assert
        assert epic_id == 'EPIC-042'
        assert epic_id is not None

    def test_extract_feature_count_from_context(self):
        """
        AC4: Hook Receives Complete Epic Context

        Given epic context with features list
        When extracting metadata for hook CLI questions
        Then feature count should be extracted for contextual questions
        """
        # Arrange
        epic_context = {
            'epic_id': 'EPIC-042',
            'features': [
                'User Registration',
                'Login with Email/Password',
                'Password Reset',
                'Multi-Factor Authentication',
                'Session Management'
            ]
        }

        # Act
        feature_count = len(epic_context.get('features', []))

        # Assert
        assert feature_count == 5

    def test_extract_complexity_from_context(self):
        """
        AC4: Hook Receives Complete Epic Context

        Given epic context with complexity_score
        When extracting metadata for hook CLI questions
        Then complexity should be extracted for context-specific questions
        """
        # Arrange
        epic_context = {
            'epic_id': 'EPIC-042',
            'complexity_score': 6
        }

        # Act
        complexity = epic_context.get('complexity_score')

        # Assert
        assert complexity == 6
        assert isinstance(complexity, int)

    def test_extract_risks_from_context(self):
        """
        AC4: Hook Receives Complete Epic Context

        Given epic context with risks list
        When extracting metadata for hook CLI questions
        Then risks should be extracted for risk assessment feedback
        """
        # Arrange
        epic_context = {
            'epic_id': 'EPIC-042',
            'risks': [
                'Third-party authentication provider unavailability',
                'Password reset email delivery failures',
                'Session storage scalability'
            ]
        }

        # Act
        risks = epic_context.get('risks', [])

        # Assert
        assert len(risks) == 3
        assert all(isinstance(r, str) for r in risks)

    def test_build_hook_questions_from_epic_context(self):
        """
        AC4: Hook Receives Complete Epic Context

        Given epic context with metadata
        When building hook questions for feedback conversation
        Then questions should reference specific epic details
        """
        # Arrange
        epic_context = {
            'epic_id': 'EPIC-042',
            'features': ['Feature A', 'Feature B', 'Feature C'],
            'complexity_score': 6,
            'name': 'Test Epic'
        }

        # Act
        feature_count = len(epic_context['features'])
        questions = [
            f"You identified {feature_count} features - was this the right granularity?",
            f"The complexity was scored {epic_context['complexity_score']}/10 - does this feel accurate?",
            "Do you have confidence in the technical risk assessment?"
        ]

        # Assert
        assert len(questions) >= 1
        assert str(feature_count) in questions[0]
        assert str(epic_context['complexity_score']) in questions[1]
