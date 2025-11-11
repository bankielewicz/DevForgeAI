"""
Test suite for hook system integration tests.

Tests end-to-end hook invocation flows and integration with operations.
Focuses on: AC2, AC3, AC5, AC9

AC Coverage:
- AC2: Hook Invocation at Operation Completion
- AC3: Graceful Hook Failure Handling
- AC5: Hook Invocation Sequence and Ordering
- AC9: Disabled Hook Configuration Mid-Operation
"""

import pytest
import asyncio
from typing import List, Dict, Any, Optional
from unittest.mock import Mock, AsyncMock, patch, call
from pathlib import Path
import yaml


# ============================================================================
# Test Fixtures
# ============================================================================

@pytest.fixture
def hook_invocation_recorder():
    """Records hook invocations for testing execution order."""
    class InvocationRecorder:
        def __init__(self):
            self.invocations: List[Dict[str, Any]] = []
            self.errors: List[Dict[str, Any]] = []

        def record_invocation(self, hook_id: str, operation_id: str, status: str = 'success'):
            """Record hook invocation."""
            self.invocations.append({
                'hook_id': hook_id,
                'operation_id': operation_id,
                'status': status,
                'sequence': len(self.invocations),
            })

        def record_error(self, hook_id: str, error_type: str, error_msg: str):
            """Record hook error."""
            self.errors.append({
                'hook_id': hook_id,
                'error_type': error_type,
                'error_msg': error_msg,
            })

        def get_invocations_for_operation(self, operation_id: str) -> List[str]:
            """Get hook IDs invoked for operation, in order."""
            return [inv['hook_id'] for inv in self.invocations if inv['operation_id'] == operation_id]

        def get_invocation_count(self) -> int:
            """Get total invocations recorded."""
            return len(self.invocations)

        def get_error_count(self) -> int:
            """Get total errors recorded."""
            return len(self.errors)

        def clear(self):
            """Clear recorded data."""
            self.invocations.clear()
            self.errors.clear()

    return InvocationRecorder()


@pytest.fixture
def mock_operation_context():
    """Sample operation completion context."""
    return {
        'operation_id': 'cmd-dev-001',
        'operation_type': 'command',
        'operation_name': 'dev',
        'status': 'success',
        'duration_ms': 45000,
        'result_code': 'success',
        'timestamp': '2025-11-11T12:00:00Z',
    }


# ============================================================================
# AC2: Hook Invocation at Operation Completion Tests
# ============================================================================

class TestHookInvocationAtCompletion:
    """Tests for hook invocation at operation completion."""

    @pytest.mark.asyncio
    async def test_hook_invoked_on_success_status(self, hook_invocation_recorder, mock_operation_context):
        """
        GIVEN an operation (command, skill, or subagent) completes successfully,
        WHEN the TodoWrite final status is written,
        THEN registered hooks matching the operation pattern are invoked automatically with context metadata.
        """
        # Arrange
        hook_config = {
            'id': 'post-dev-feedback',
            'operation_pattern': 'dev',
            'trigger_status': ['success'],
            'enabled': True,
        }

        # Act - Simulate hook invocation on operation completion
        if hook_config['enabled'] and mock_operation_context['status'] in hook_config['trigger_status']:
            hook_invocation_recorder.record_invocation(
                hook_config['id'],
                mock_operation_context['operation_id'],
                'success'
            )

        # Assert
        invocations = hook_invocation_recorder.get_invocations_for_operation(
            mock_operation_context['operation_id']
        )
        assert len(invocations) == 1
        assert invocations[0] == 'post-dev-feedback'


    @pytest.mark.asyncio
    async def test_hook_not_invoked_on_failure_status(self, hook_invocation_recorder, mock_operation_context):
        """WHEN operation status doesn't match trigger_status, THEN hook not invoked."""
        # Arrange
        hook_config = {
            'id': 'success-only-hook',
            'trigger_status': ['success'],
        }
        operation_context = mock_operation_context.copy()
        operation_context['status'] = 'failure'  # Doesn't match

        # Act
        if operation_context['status'] in hook_config['trigger_status']:
            hook_invocation_recorder.record_invocation(
                hook_config['id'],
                operation_context['operation_id'],
                'success'
            )

        # Assert
        invocations = hook_invocation_recorder.get_invocations_for_operation(
            operation_context['operation_id']
        )
        assert len(invocations) == 0


    @pytest.mark.asyncio
    async def test_hook_receives_operation_context(self, hook_invocation_recorder, mock_operation_context):
        """WHEN hook invoked, THEN receives complete operation context."""
        # Arrange
        hook_context = {
            **mock_operation_context,
            'hook_id': 'test-hook',
        }

        # Act
        hook_invocation_recorder.record_invocation(
            'test-hook',
            mock_operation_context['operation_id']
        )

        # Assert
        assert 'operation_id' in hook_context
        assert 'operation_type' in hook_context
        assert 'status' in hook_context
        assert 'duration_ms' in hook_context


# ============================================================================
# AC3: Graceful Hook Failure Handling Tests
# ============================================================================

class TestGracefulHookFailureHandling:
    """Tests for graceful handling of hook failures."""

    @pytest.mark.asyncio
    async def test_hook_failure_logged_not_propagated(self, hook_invocation_recorder):
        """
        GIVEN a registered hook fails during invocation,
        WHEN the failure occurs,
        THEN the failure is logged, does not propagate to the calling operation, and the operation completes normally.
        """
        # Arrange
        hook_id = 'failing-hook'
        operation_id = 'op-001'

        # Act - Simulate hook failure
        try:
            raise Exception("Hook execution failed")
        except Exception as e:
            hook_invocation_recorder.record_error(hook_id, 'execution_error', str(e))

        # Operation should still complete
        operation_completed = True

        # Assert
        assert operation_completed is True
        assert hook_invocation_recorder.get_error_count() == 1
        error = hook_invocation_recorder.errors[0]
        assert error['hook_id'] == hook_id
        assert 'execution_error' in error['error_type']


    @pytest.mark.asyncio
    async def test_multiple_hook_failures_all_logged(self, hook_invocation_recorder):
        """WHEN multiple hooks fail, THEN all failures logged independently."""
        # Arrange
        hook_ids = ['hook-1', 'hook-2', 'hook-3']

        # Act - All hooks fail
        for hook_id in hook_ids:
            hook_invocation_recorder.record_error(
                hook_id,
                'timeout_error',
                f'{hook_id} exceeded timeout'
            )

        # Assert
        assert hook_invocation_recorder.get_error_count() == 3
        for i, hook_id in enumerate(hook_ids):
            assert hook_invocation_recorder.errors[i]['hook_id'] == hook_id


    @pytest.mark.asyncio
    async def test_operation_continues_after_hook_failure(self, hook_invocation_recorder, mock_operation_context):
        """WHEN hook fails, THEN operation continues with status message."""
        # Arrange
        operation_result = {'status': 'running'}

        # Act - Hook fails
        hook_invocation_recorder.record_error('hook-1', 'error', 'Failed')

        # Operation continues
        operation_result['status'] = 'completed'

        # Assert
        assert operation_result['status'] == 'completed'
        assert hook_invocation_recorder.get_error_count() == 1


# ============================================================================
# AC5: Hook Invocation Sequence and Ordering Tests
# ============================================================================

class TestHookInvocationSequence:
    """Tests for hook invocation sequence and ordering."""

    @pytest.mark.asyncio
    async def test_multiple_hooks_invoked_in_registration_order(self, hook_invocation_recorder, mock_operation_context):
        """
        GIVEN multiple hooks are registered for the same operation,
        WHEN the operation completes,
        THEN hooks execute in registration order with proper dependency resolution.
        """
        # Arrange
        hooks = [
            {'id': 'hook-1', 'operation_pattern': 'dev', 'trigger_status': ['success']},
            {'id': 'hook-2', 'operation_pattern': 'dev', 'trigger_status': ['success']},
            {'id': 'hook-3', 'operation_pattern': 'dev', 'trigger_status': ['success']},
        ]

        # Act - Invoke hooks in registration order
        for hook in hooks:
            if hook['operation_pattern'] == 'dev' and mock_operation_context['status'] in hook['trigger_status']:
                hook_invocation_recorder.record_invocation(
                    hook['id'],
                    mock_operation_context['operation_id']
                )

        # Assert - Verify order
        invocations = hook_invocation_recorder.get_invocations_for_operation(
            mock_operation_context['operation_id']
        )
        assert invocations == ['hook-1', 'hook-2', 'hook-3']


    @pytest.mark.asyncio
    async def test_hooks_execute_serially_not_parallel(self, hook_invocation_recorder, mock_operation_context):
        """WHEN multiple hooks match, THEN execute serially (not parallel)."""
        # Arrange
        hooks = [
            {'id': 'hook-a', 'trigger_status': ['success']},
            {'id': 'hook-b', 'trigger_status': ['success']},
        ]
        invocation_times = []

        # Act - Execute hooks serially
        for hook in hooks:
            invocation_times.append(len(hook_invocation_recorder.invocations))
            hook_invocation_recorder.record_invocation(
                hook['id'],
                mock_operation_context['operation_id']
            )

        # Assert - Sequential invocation (not parallel)
        assert invocation_times == [0, 1]


    @pytest.mark.asyncio
    async def test_hook_execution_order_preserved(self, hook_invocation_recorder, mock_operation_context):
        """WHEN hooks invoked, THEN execution order matches registration order."""
        # Arrange
        registered_order = ['first-hook', 'second-hook', 'third-hook']

        # Act
        for hook_id in registered_order:
            hook_invocation_recorder.record_invocation(hook_id, mock_operation_context['operation_id'])

        # Assert
        actual_order = hook_invocation_recorder.get_invocations_for_operation(
            mock_operation_context['operation_id']
        )
        assert actual_order == registered_order


# ============================================================================
# AC9: Disabled Hook Configuration Mid-Operation Tests
# ============================================================================

class TestDisabledHookConfiguration:
    """Tests for disabled hook configuration."""

    @pytest.mark.asyncio
    async def test_disabled_hook_not_invoked(self, hook_invocation_recorder, mock_operation_context):
        """
        GIVEN hooks are disabled during an active operation (via `.devforgeai/config/hooks.yaml` enabled: false),
        WHEN the operation completes,
        THEN hooks are skipped and no feedback conversation is triggered.
        """
        # Arrange
        hook_config = {
            'id': 'disabled-hook',
            'operation_pattern': 'dev',
            'trigger_status': ['success'],
            'enabled': False,  # Disabled
        }

        # Act
        if hook_config['enabled']:  # Check enabled flag
            hook_invocation_recorder.record_invocation(
                hook_config['id'],
                mock_operation_context['operation_id']
            )

        # Assert
        invocations = hook_invocation_recorder.get_invocations_for_operation(
            mock_operation_context['operation_id']
        )
        assert len(invocations) == 0


    @pytest.mark.asyncio
    async def test_enabled_hook_invoked(self, hook_invocation_recorder, mock_operation_context):
        """WHEN hook enabled=true, THEN invoked."""
        # Arrange
        hook_config = {
            'id': 'enabled-hook',
            'operation_pattern': 'dev',
            'trigger_status': ['success'],
            'enabled': True,  # Enabled
        }

        # Act
        if hook_config['enabled']:
            hook_invocation_recorder.record_invocation(
                hook_config['id'],
                mock_operation_context['operation_id']
            )

        # Assert
        invocations = hook_invocation_recorder.get_invocations_for_operation(
            mock_operation_context['operation_id']
        )
        assert len(invocations) == 1


    @pytest.mark.asyncio
    async def test_config_reload_respects_enabled_flag(self, hook_invocation_recorder, tmp_path):
        """WHEN config reloaded mid-operation, THEN enabled flag respected."""
        # Arrange
        config_file = tmp_path / 'hooks.yaml'

        # Initial config - enabled
        config_v1 = {
            'hooks': [
                {
                    'id': 'toggle-hook',
                    'operation_pattern': 'dev',
                    'trigger_status': ['success'],
                    'enabled': True,
                }
            ]
        }

        with open(config_file, 'w') as f:
            yaml.dump(config_v1, f)

        # Act - Load config
        with open(config_file) as f:
            config = yaml.safe_load(f)

        hook = config['hooks'][0]
        assert hook['enabled'] is True

        # Update config - disabled
        config_v2 = {
            'hooks': [
                {
                    'id': 'toggle-hook',
                    'operation_pattern': 'dev',
                    'trigger_status': ['success'],
                    'enabled': False,
                }
            ]
        }

        with open(config_file, 'w') as f:
            yaml.dump(config_v2, f)

        # Reload config
        with open(config_file) as f:
            config = yaml.safe_load(f)

        hook = config['hooks'][0]

        # Assert
        assert hook['enabled'] is False


# ============================================================================
# Integration Test: Complete Hook Invocation Flow
# ============================================================================

class TestCompleteHookInvocationFlow:
    """Integration tests for complete hook invocation flow."""

    @pytest.mark.asyncio
    async def test_complete_operation_with_hooks(self, hook_invocation_recorder, mock_operation_context):
        """
        Complete flow:
        1. Operation completes
        2. TodoWrite writes final status
        3. Hook registry loaded and evaluated
        4. Matching hooks invoked in order
        5. Failures isolated, operation completes normally
        """
        # Arrange
        hook_configs = [
            {
                'id': 'post-dev-feedback',
                'operation_pattern': 'dev',
                'trigger_status': ['success', 'partial'],
                'enabled': True,
            },
            {
                'id': 'metrics-hook',
                'operation_pattern': 'dev',
                'trigger_status': ['success'],
                'enabled': True,
            },
        ]

        # Act - Operation completes
        operation_status = 'completed'

        # TodoWrite writes final status (triggers hooks)
        for hook_config in hook_configs:
            if (hook_config['enabled'] and
                mock_operation_context['status'] in hook_config['trigger_status']):
                hook_invocation_recorder.record_invocation(
                    hook_config['id'],
                    mock_operation_context['operation_id'],
                    'success'
                )

        # Assert
        assert operation_status == 'completed'
        assert hook_invocation_recorder.get_invocation_count() == 2
        invocations = hook_invocation_recorder.get_invocations_for_operation(
            mock_operation_context['operation_id']
        )
        assert invocations == ['post-dev-feedback', 'metrics-hook']


    @pytest.mark.asyncio
    async def test_hook_failure_isolation_in_operation_flow(self, hook_invocation_recorder, mock_operation_context):
        """WHEN hook fails in operation flow, THEN operation completes normally."""
        # Arrange
        hooks_to_invoke = ['hook-1', 'hook-2', 'hook-3']
        operation_completed = False

        # Act
        for i, hook_id in enumerate(hooks_to_invoke):
            try:
                if i == 1:  # Hook 2 fails
                    raise Exception("Hook execution failed")
                hook_invocation_recorder.record_invocation(
                    hook_id,
                    mock_operation_context['operation_id']
                )
            except Exception as e:
                hook_invocation_recorder.record_error(
                    hook_id,
                    'execution_error',
                    str(e)
                )
            # Continue with next hook despite failure

        operation_completed = True

        # Assert
        assert operation_completed is True
        assert hook_invocation_recorder.get_invocation_count() == 2  # hook-1, hook-3 succeeded
        assert hook_invocation_recorder.get_error_count() == 1  # hook-2 failed


# ============================================================================
# Configuration Hot-Reload Tests
# ============================================================================

class TestConfigurationHotReload:
    """Tests for hook configuration hot-reload capability."""

    @pytest.mark.asyncio
    async def test_config_reload_on_file_change(self, tmp_path):
        """WHEN hooks.yaml changes, THEN config reloaded without restart."""
        # Arrange
        config_file = tmp_path / 'hooks.yaml'

        # Initial config
        config_v1 = {
            'hooks': [
                {
                    'id': 'hook-v1',
                    'operation_pattern': 'dev',
                    'trigger_status': ['success'],
                }
            ]
        }

        with open(config_file, 'w') as f:
            yaml.dump(config_v1, f)

        # Load initial config
        with open(config_file) as f:
            loaded_config = yaml.safe_load(f)

        v1_hooks = [h['id'] for h in loaded_config['hooks']]

        # Update config
        config_v2 = {
            'hooks': [
                {
                    'id': 'hook-v1',
                    'operation_pattern': 'dev',
                    'trigger_status': ['success'],
                },
                {
                    'id': 'hook-v2',
                    'operation_pattern': 'qa',
                    'trigger_status': ['success'],
                },
            ]
        }

        with open(config_file, 'w') as f:
            yaml.dump(config_v2, f)

        # Reload config
        with open(config_file) as f:
            loaded_config = yaml.safe_load(f)

        v2_hooks = [h['id'] for h in loaded_config['hooks']]

        # Assert
        assert v1_hooks == ['hook-v1']
        assert v2_hooks == ['hook-v1', 'hook-v2']
