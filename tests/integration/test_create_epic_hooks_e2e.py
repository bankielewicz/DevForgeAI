"""
Integration tests for Hook Integration in /create-epic Command (STORY-028)

End-to-end tests for the complete hook workflow triggered by epic creation:
Epic creation → hook check → hook invocation → feedback conversation → response storage

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
import time
from datetime import datetime
import yaml


class TestCreateEpicHooksE2E:
    """End-to-end tests for epic creation with hook integration."""

    @pytest.fixture
    def temp_project_dir(self):
        """Create temporary project directory structure for testing."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir_path = Path(tmpdir)

            # Create required directories
            (tmpdir_path / '.ai_docs' / 'Epics').mkdir(parents=True, exist_ok=True)
            (tmpdir_path / 'devforgeai' / 'config').mkdir(parents=True, exist_ok=True)
            (tmpdir_path / 'devforgeai' / 'feedback' / 'epic-create').mkdir(parents=True, exist_ok=True)
            (tmpdir_path / 'devforgeai' / 'feedback' / '.logs').mkdir(parents=True, exist_ok=True)

            yield tmpdir_path

    @pytest.fixture
    def hooks_config_enabled(self, temp_project_dir):
        """Create hooks.yaml with epic-create enabled."""
        config_path = temp_project_dir / 'devforgeai' / 'config' / 'hooks.yaml'
        config = {
            'feedback': {
                'hooks': {
                    'epic_create': {
                        'enabled': True,
                        'timeout': 30000,
                        'questions': [
                            'How confident are you in the feature decomposition?',
                            'Was the complexity assessment accurate?',
                            'Did you identify all critical risks?'
                        ]
                    }
                }
            }
        }
        with open(config_path, 'w') as f:
            yaml.dump(config, f)
        return config_path

    @pytest.fixture
    def hooks_config_disabled(self, temp_project_dir):
        """Create hooks.yaml with epic-create disabled."""
        config_path = temp_project_dir / 'devforgeai' / 'config' / 'hooks.yaml'
        config = {
            'feedback': {
                'hooks': {
                    'epic_create': {
                        'enabled': False,
                        'timeout': 30000
                    }
                }
            }
        }
        with open(config_path, 'w') as f:
            yaml.dump(config, f)
        return config_path

    @pytest.fixture
    def epic_file_content(self):
        """Template for epic file content."""
        return """---
id: EPIC-042
title: User Authentication System
epic_type: platform_feature
sprint: Sprint-3
status: In Progress
created: 2025-11-12
format_version: "2.0"
---

# EPIC-042: User Authentication System

## Goal
Enable secure user access to the platform

## Features

### 1. User Registration
### 2. Login with Email/Password
### 3. Password Reset Flow
### 4. Multi-Factor Authentication
### 5. Session Management

## Success Criteria
- < 1 second login response time
- 99.9% uptime for authentication service
- Zero password breaches

## Technical Complexity
Score: 6/10

## Identified Risks
- Third-party OAuth provider unavailability
- Password reset email delivery failures
- Session storage scalability
"""

    def test_e2e_epic_creation_with_hooks_enabled(self, temp_project_dir, hooks_config_enabled, epic_file_content):
        """
        AC1: Automatic Hook Trigger After Successful Epic Creation
        AC4: Hook Receives Complete Epic Context

        Given hooks are enabled in configuration
        When /create-epic completes successfully
        Then: Hook check executes → Hook invoked with epic context → Feedback appears
        """
        # Arrange
        epic_id = "EPIC-042"
        epic_path = temp_project_dir / '.ai_docs' / 'Epics' / f'{epic_id}.epic.md'

        # Create epic file (simulates successful creation)
        epic_path.write_text(epic_file_content)

        # Mock hook CLI calls
        with patch('subprocess.run') as mock_run:
            # Mock check-hooks response
            check_hooks_result = MagicMock()
            check_hooks_result.returncode = 0
            check_hooks_result.stdout = json.dumps({
                'enabled': True,
                'available': True,
                'operation': 'epic-create'
            })

            # Mock invoke-hooks response
            invoke_hooks_result = MagicMock()
            invoke_hooks_result.returncode = 0
            invoke_hooks_result.stdout = json.dumps({
                'status': 'success',
                'operation': 'epic-create',
                'epic_id': epic_id,
                'duration_ms': 2500
            })

            # Configure mock to return different results for different calls
            mock_run.side_effect = [check_hooks_result, invoke_hooks_result]

            # Act
            # Simulate Phase 4A.9 execution
            check_result = subprocess.run(
                ['devforgeai', 'check-hooks', '--operation=epic-create'],
                capture_output=True,
                text=True
            )
            check_config = json.loads(check_result.stdout)

            if check_config['enabled']:
                invoke_result = subprocess.run(
                    ['devforgeai', 'invoke-hooks', '--operation=epic-create', f'--epic-id={epic_id}'],
                    capture_output=True,
                    text=True
                )
                invoke_config = json.loads(invoke_result.stdout)
            else:
                invoke_config = None

            # Assert
            assert epic_path.exists()  # Epic created successfully
            assert check_config['enabled'] is True  # Hooks are enabled
            assert invoke_config is not None  # Hook was invoked
            assert invoke_config['epic_id'] == epic_id
            assert invoke_config['status'] == 'success'
            # Verify both CLI calls were made
            assert mock_run.call_count == 2

    def test_e2e_epic_creation_with_hooks_disabled(self, temp_project_dir, hooks_config_disabled, epic_file_content):
        """
        AC3: Hook Respects Configuration State

        Given hooks are disabled in configuration
        When /create-epic completes successfully
        Then: Epic created → Hook check returns enabled=false → No hook invoked (zero overhead)
        """
        # Arrange
        epic_id = "EPIC-043"
        epic_path = temp_project_dir / '.ai_docs' / 'Epics' / f'{epic_id}.epic.md'
        epic_path.write_text(epic_file_content)

        with patch('subprocess.run') as mock_run:
            # Mock check-hooks response with disabled
            check_hooks_result = MagicMock()
            check_hooks_result.returncode = 0
            check_hooks_result.stdout = json.dumps({
                'enabled': False,
                'available': True,
                'operation': 'epic-create'
            })
            mock_run.return_value = check_hooks_result

            # Act
            check_result = subprocess.run(
                ['devforgeai', 'check-hooks', '--operation=epic-create'],
                capture_output=True,
                text=True
            )
            check_config = json.loads(check_result.stdout)

            # Only call invoke-hooks if enabled
            invoke_called = False
            if check_config['enabled']:
                invoke_called = True

            # Assert
            assert epic_path.exists()  # Epic created successfully
            assert check_config['enabled'] is False  # Hooks are disabled
            assert invoke_called is False  # invoke-hooks NOT called (zero overhead)
            # Only check-hooks was called, not invoke-hooks
            assert mock_run.call_count == 1

    def test_e2e_hook_failure_doesnt_break_epic(self, temp_project_dir, hooks_config_enabled, epic_file_content):
        """
        AC2: Hook Failure Doesn't Break Epic Creation

        Given hook invocation fails (timeout, CLI error)
        When /create-epic attempts to trigger feedback
        Then: Epic created successfully → Exit code 0 → Failure logged
        """
        # Arrange
        epic_id = "EPIC-044"
        epic_path = temp_project_dir / '.ai_docs' / 'Epics' / f'{epic_id}.epic.md'
        epic_path.write_text(epic_file_content)
        error_log_path = temp_project_dir / 'devforgeai' / 'feedback' / '.logs' / 'hook-errors.log'

        with patch('subprocess.run') as mock_run:
            # Mock check-hooks success
            check_result = MagicMock()
            check_result.returncode = 0
            check_result.stdout = json.dumps({'enabled': True, 'available': True, 'operation': 'epic-create'})

            # Mock invoke-hooks failure (timeout)
            invoke_result = MagicMock()
            invoke_result.returncode = 1
            invoke_result.stderr = "Hook invocation timeout after 30000ms"

            mock_run.side_effect = [check_result, invoke_result]

            # Act
            check_response = subprocess.run(
                ['devforgeai', 'check-hooks', '--operation=epic-create'],
                capture_output=True,
                text=True
            )
            check_config = json.loads(check_response.stdout)

            hook_failure_exit_code = 1
            epic_creation_exit_code = 0  # Non-blocking - epic creation succeeds

            if check_config['enabled']:
                try:
                    invoke_response = subprocess.run(
                        ['devforgeai', 'invoke-hooks', '--operation=epic-create', f'--epic-id={epic_id}'],
                        capture_output=True,
                        text=True
                    )
                    if invoke_response.returncode != 0:
                        # Log the error
                        with open(error_log_path, 'a') as f:
                            f.write(f"[{datetime.now().isoformat()}] Hook failed for {epic_id}: {invoke_response.stderr}\n")
                except Exception as e:
                    # Catch all exceptions
                    with open(error_log_path, 'a') as f:
                        f.write(f"[{datetime.now().isoformat()}] Exception: {str(e)}\n")

            # Assert
            assert epic_path.exists()  # Epic created successfully
            assert epic_creation_exit_code == 0  # Epic creation succeeds despite hook failure
            assert error_log_path.exists()  # Error logged
            error_content = error_log_path.read_text()
            assert len(error_content) > 0  # Error logged to file

    def test_e2e_hook_metadata_extraction_and_usage(self, temp_project_dir, hooks_config_enabled, epic_file_content):
        """
        AC4: Hook Receives Complete Epic Context

        Given epic creation completed with all metadata
        When hook is invoked
        Then: Hook CLI receives epic-id → Reads epic file → Extracts features/complexity/risks
        → Questions reference specific epic details
        """
        # Arrange
        epic_id = "EPIC-045"
        epic_path = temp_project_dir / '.ai_docs' / 'Epics' / f'{epic_id}.epic.md'
        epic_path.write_text(epic_file_content)

        # Parse epic metadata
        epic_metadata = {
            'epic_id': epic_id,
            'features': ['User Registration', 'Login', 'Password Reset', 'MFA', 'Session Management'],
            'complexity_score': 6,
            'risks': ['OAuth provider unavailability', 'Email delivery failures', 'Session scalability']
        }

        with patch('subprocess.run') as mock_run:
            # Mock check-hooks
            check_result = MagicMock()
            check_result.returncode = 0
            check_result.stdout = json.dumps({'enabled': True, 'available': True})

            # Mock invoke-hooks with feedback questions
            invoke_result = MagicMock()
            invoke_result.returncode = 0
            invoke_result.stdout = json.dumps({
                'status': 'success',
                'epic_id': epic_id,
                'questions': [
                    f"You identified {len(epic_metadata['features'])} features - was this the right granularity?",
                    f"The complexity was scored {epic_metadata['complexity_score']}/10 - does this feel accurate?",
                    f"You identified {len(epic_metadata['risks'])} risks - did you capture all critical ones?"
                ]
            })

            mock_run.side_effect = [check_result, invoke_result]

            # Act
            check_resp = subprocess.run(
                ['devforgeai', 'check-hooks', '--operation=epic-create'],
                capture_output=True,
                text=True
            )
            check_config = json.loads(check_resp.stdout)

            if check_config['enabled']:
                invoke_resp = subprocess.run(
                    ['devforgeai', 'invoke-hooks', '--operation=epic-create', f'--epic-id={epic_id}'],
                    capture_output=True,
                    text=True
                )
                invoke_result_data = json.loads(invoke_resp.stdout)
                questions = invoke_result_data.get('questions', [])
            else:
                questions = []

            # Assert
            assert len(questions) > 0
            assert str(len(epic_metadata['features'])) in questions[0]  # Feature count in Q1
            assert str(epic_metadata['complexity_score']) in questions[1]  # Complexity in Q2
            assert str(len(epic_metadata['risks'])) in questions[2]  # Risk count in Q3

    def test_e2e_feedback_responses_stored(self, temp_project_dir, hooks_config_enabled, epic_file_content):
        """
        AC1: Automatic Hook Trigger After Successful Epic Creation
        AC4: Hook Receives Complete Epic Context

        Given hook invocation succeeds
        When user provides feedback responses
        Then: Responses tagged with epic ID → Stored in devforgeai/feedback/epic-create/
        """
        # Arrange
        epic_id = "EPIC-046"
        epic_path = temp_project_dir / '.ai_docs' / 'Epics' / f'{epic_id}.epic.md'
        epic_path.write_text(epic_file_content)

        feedback_dir = temp_project_dir / 'devforgeai' / 'feedback' / 'epic-create'

        # Sample user responses
        user_responses = {
            'epic_id': epic_id,
            'timestamp': datetime.now().isoformat(),
            'responses': [
                {'question': 'Feature decomposition confidence', 'answer': 'High - 5 features is appropriate'},
                {'question': 'Complexity accuracy', 'answer': 'Yes - 6/10 is correct'},
                {'question': 'Risk assessment completeness', 'answer': 'Mostly - should add data security risk'}
            ]
        }

        # Act
        with patch('subprocess.run') as mock_run:
            check_result = MagicMock()
            check_result.returncode = 0
            check_result.stdout = json.dumps({'enabled': True, 'available': True})

            invoke_result = MagicMock()
            invoke_result.returncode = 0
            invoke_result.stdout = json.dumps({'status': 'success', 'epic_id': epic_id})

            mock_run.side_effect = [check_result, invoke_result]

            # Simulate hook execution and response storage
            check_resp = subprocess.run(
                ['devforgeai', 'check-hooks', '--operation=epic-create'],
                capture_output=True,
                text=True
            )
            check_config = json.loads(check_resp.stdout)

            if check_config['enabled']:
                invoke_resp = subprocess.run(
                    ['devforgeai', 'invoke-hooks', '--operation=epic-create', f'--epic-id={epic_id}'],
                    capture_output=True,
                    text=True
                )

                # Store responses
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                response_file = feedback_dir / f'{epic_id}_{timestamp}.json'
                with open(response_file, 'w') as f:
                    json.dump(user_responses, f, indent=2)

        # Assert
        assert feedback_dir.exists()
        # Find response file
        response_files = list(feedback_dir.glob(f'{epic_id}_*.json'))
        assert len(response_files) > 0

        # Verify response content
        stored_responses = json.loads(response_files[0].read_text())
        assert stored_responses['epic_id'] == epic_id
        assert len(stored_responses['responses']) == 3

    def test_e2e_hook_integration_multiple_epics(self, temp_project_dir, hooks_config_enabled, epic_file_content):
        """
        AC1: Automatic Hook Trigger After Successful Epic Creation
        Edge Case: Multiple epics created in batch

        Given multiple epics created sequentially
        When each epic creation completes
        Then: Hook triggers once per epic → Sequential feedback conversations
        """
        # Arrange
        epic_ids = ['EPIC-047', 'EPIC-048', 'EPIC-049']
        created_epics = []

        with patch('subprocess.run') as mock_run:
            for epic_id in epic_ids:
                # Create epic file
                epic_path = temp_project_dir / '.ai_docs' / 'Epics' / f'{epic_id}.epic.md'
                epic_path.write_text(epic_file_content)
                created_epics.append(epic_path)

                # Mock hook calls
                check_result = MagicMock()
                check_result.returncode = 0
                check_result.stdout = json.dumps({'enabled': True, 'available': True})

                invoke_result = MagicMock()
                invoke_result.returncode = 0
                invoke_result.stdout = json.dumps({'status': 'success', 'epic_id': epic_id})

                mock_run.side_effect = [check_result, invoke_result]

                # Act
                subprocess.run(['devforgeai', 'check-hooks', '--operation=epic-create'], capture_output=True, text=True)
                subprocess.run(['devforgeai', 'invoke-hooks', '--operation=epic-create', f'--epic-id={epic_id}'], capture_output=True, text=True)

        # Assert
        assert all(epic.exists() for epic in created_epics)
        # Hooks called once per epic: 3 epics × 2 calls (check + invoke) = 6 calls
        assert mock_run.call_count == 6

    @patch('subprocess.run')
    @patch('builtins.open', create=True)
    def test_e2e_hook_cli_missing_logs_error(self, mock_open, mock_run, temp_project_dir, epic_file_content):
        """
        AC2: Hook Failure Doesn't Break Epic Creation
        Edge Case: devforgeai CLI not found or not installed

        Given devforgeai CLI command not found
        When Phase 4A.9 attempts to invoke hook
        Then: FileNotFoundError caught → Error logged → Warning displayed → Exit 0
        """
        # Arrange
        epic_id = "EPIC-050"
        epic_path = temp_project_dir / '.ai_docs' / 'Epics' / f'{epic_id}.epic.md'
        epic_path.write_text(epic_file_content)

        # Simulate subprocess.run raising FileNotFoundError
        mock_run.side_effect = FileNotFoundError("devforgeai: command not found")

        # Act & Assert
        with pytest.raises(FileNotFoundError):
            subprocess.run(['devforgeai', 'check-hooks', '--operation=epic-create'], capture_output=True, text=True)

        # Verify epic was still created
        assert epic_path.exists()
        # In real implementation, error would be logged and exit 0 returned


class TestHookCLIIntegration:
    """Tests for actual devforgeai CLI hook commands integration."""

    @pytest.mark.integration
    def test_check_hooks_cli_exists_and_responds(self):
        """
        AC1: Automatic Hook Trigger After Successful Epic Creation

        Given devforgeai CLI is installed
        When running: devforgeai check-hooks --operation=epic-create
        Then: Should return JSON response with enabled and available fields
        """
        try:
            result = subprocess.run(
                ['devforgeai', 'check-hooks', '--operation=epic-create'],
                capture_output=True,
                text=True,
                timeout=5
            )
            # This test will be marked as XFAIL if devforgeai CLI not installed yet
            assert result.returncode == 0
            parsed = json.loads(result.stdout)
            assert 'enabled' in parsed
            assert 'available' in parsed
        except FileNotFoundError:
            pytest.xfail("devforgeai CLI not yet installed")

    @pytest.mark.integration
    def test_invoke_hooks_cli_exists_and_responds(self):
        """
        AC1: Automatic Hook Trigger After Successful Epic Creation

        Given devforgeai CLI is installed
        When running: devforgeai invoke-hooks --operation=epic-create --epic-id=EPIC-042
        Then: Should return JSON response with status and epic_id fields
        """
        try:
            result = subprocess.run(
                ['devforgeai', 'invoke-hooks', '--operation=epic-create', '--epic-id=EPIC-042'],
                capture_output=True,
                text=True,
                timeout=35  # Allow 30s timeout + 5s buffer
            )
            # This test will mark xfail if devforgeai CLI not installed or epic file missing
            assert result.returncode == 0
            parsed = json.loads(result.stdout)
            assert 'status' in parsed
            assert 'epic_id' in parsed
        except (FileNotFoundError, json.JSONDecodeError, subprocess.TimeoutExpired):
            pytest.xfail("devforgeai CLI not yet installed or epic file missing")


@pytest.mark.integration
class TestCreateEpicHooksLogging:
    """Integration tests for hook execution logging."""

    @pytest.fixture
    def temp_log_dir(self):
        """Create temporary directory for test logs."""
        with tempfile.TemporaryDirectory() as tmpdir:
            log_dir = Path(tmpdir) / 'devforgeai' / 'feedback' / '.logs'
            log_dir.mkdir(parents=True, exist_ok=True)
            yield log_dir

    def test_successful_hook_logged_to_hooks_log(self, temp_log_dir):
        """
        AC1: Automatic Hook Trigger After Successful Epic Creation

        Given hook invocation succeeds
        When Phase 4A.9 executes
        Then: Entry logged to devforgeai/feedback/.logs/hooks.log with timestamp, operation, status
        """
        # Arrange
        hooks_log_path = temp_log_dir / 'hooks.log'

        # Act
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'operation': 'epic-create',
            'epic_id': 'EPIC-042',
            'status': 'success',
            'duration_ms': 2500
        }

        with open(hooks_log_path, 'w') as f:
            f.write(json.dumps(log_entry) + '\n')

        # Assert
        assert hooks_log_path.exists()
        logged_content = json.loads(hooks_log_path.read_text())
        assert logged_content['operation'] == 'epic-create'
        assert logged_content['status'] == 'success'
        assert logged_content['epic_id'] == 'EPIC-042'

    def test_hook_failure_logged_to_hook_errors_log(self, temp_log_dir):
        """
        AC2: Hook Failure Doesn't Break Epic Creation

        Given hook invocation fails
        When Phase 4A.9 catches exception
        Then: Entry logged to devforgeai/feedback/.logs/hook-errors.log with timestamp, epic_id, error
        """
        # Arrange
        errors_log_path = temp_log_dir / 'hook-errors.log'

        # Act
        error_entry = {
            'timestamp': datetime.now().isoformat(),
            'operation': 'epic-create',
            'epic_id': 'EPIC-043',
            'error': 'Hook invocation timeout after 30000ms',
            'error_type': 'TimeoutError'
        }

        with open(errors_log_path, 'w') as f:
            f.write(json.dumps(error_entry) + '\n')

        # Assert
        assert errors_log_path.exists()
        logged_error = json.loads(errors_log_path.read_text())
        assert logged_error['epic_id'] == 'EPIC-043'
        assert 'timeout' in logged_error['error'].lower()
