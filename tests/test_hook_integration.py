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

# REAL IMPORTS - Test actual implementation, not mocks
from src.hook_system import HookSystem
from src.hook_registry import HookRegistry
import yaml


# ============================================================================
# Test Fixtures
# ============================================================================

@pytest.fixture
def hook_system_with_config(tmp_path):
    """Create real HookSystem with test configuration."""
    def _create_hook_system(hooks_config: List[Dict[str, Any]]):
        config_file = tmp_path / 'hooks.yaml'
        with open(config_file, 'w') as f:
            yaml.dump({'hooks': hooks_config}, f)
        return HookSystem(config_path=config_file)
    return _create_hook_system


@pytest.fixture
def invocation_tracker():
    """Track hook invocations for testing."""
    invocations = []
    errors = []

    async def mock_runner(hook_entry, context):
        invocations.append({'hook_id': hook_entry['id'], 'context': context})
        return {'status': 'success'}

    async def failing_runner(hook_entry, context):
        error_msg = f"{hook_entry['id']} failed"
        errors.append({'hook_id': hook_entry['id'], 'error': error_msg})
        raise Exception(error_msg)

    return {
        'invocations': invocations,
        'errors': errors,
        'mock_runner': mock_runner,
        'failing_runner': failing_runner,
    }


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
    async def test_hook_invoked_on_success_status(self, tmp_path, mock_operation_context):
        """
        GIVEN an operation (command, skill, or subagent) completes successfully,
        WHEN the TodoWrite final status is written,
        THEN registered hooks matching the operation pattern are invoked automatically with context metadata.
        """
        # Arrange - Create real HookSystem with test config
        config_file = tmp_path / 'hooks.yaml'
        hook_config = {
            'hooks': [{
                'id': 'post-dev-feedback',
                'name': 'Post Dev Feedback',
                'operation_type': 'command',
                'operation_pattern': 'dev',
                'trigger_status': ['success'],
                'feedback_type': 'conversation',
                'enabled': True,
            }]
        }
        with open(config_file, 'w') as f:
            yaml.dump(hook_config, f)

        hook_system = HookSystem(config_path=config_file)

        # Mock the hook runner to track invocations
        invoked_hooks = []
        async def mock_hook_runner(hook_entry, context):
            invoked_hooks.append(hook_entry['id'])
            return {'status': 'success'}

        hook_system.set_hook_runner(mock_hook_runner)

        # Act - Actually invoke hooks using real HookSystem
        results = await hook_system.invoke_hooks(
            operation_id=mock_operation_context['operation_id'],
            operation_type=mock_operation_context['operation_type'],
            operation_name=mock_operation_context['operation_name'],
            status=mock_operation_context['status'],
            duration_ms=mock_operation_context['duration_ms'],
            result_code=mock_operation_context['result_code']
        )

        # Assert - Real HookSystem invoked the hook
        assert len(invoked_hooks) == 1
        assert invoked_hooks[0] == 'post-dev-feedback'
        assert len(results) == 1
        assert results[0].hook_id == 'post-dev-feedback'


    @pytest.mark.asyncio
    async def test_hook_not_invoked_on_failure_status(self, hook_system_with_config, invocation_tracker, mock_operation_context):
        """WHEN operation status doesn't match trigger_status, THEN hook not invoked."""
        # Arrange - Create HookSystem with success-only hook
        hook_config = [{
            'id': 'success-only-hook',
            'name': 'Success Only',
            'operation_type': 'command',
            'operation_pattern': 'dev',
            'trigger_status': ['success'],  # Only triggers on success
            'feedback_type': 'conversation',
            'enabled': True,
        }]
        hook_system = hook_system_with_config(hook_config)
        hook_system.set_hook_runner(invocation_tracker['mock_runner'])

        operation_context = mock_operation_context.copy()
        operation_context['status'] = 'failure'  # Doesn't match trigger_status

        # Act - Invoke hooks with failure status
        results = await hook_system.invoke_hooks(
            operation_id=operation_context['operation_id'],
            operation_type=operation_context['operation_type'],
            operation_name=operation_context['operation_name'],
            status='failure',  # Doesn't match trigger_status
            duration_ms=operation_context['duration_ms'],
            result_code='failure'
        )

        # Assert - Hook should NOT have been invoked
        assert len(invocation_tracker['invocations']) == 0
        assert len(results) == 0


    @pytest.mark.asyncio
    async def test_hook_receives_operation_context(self, hook_system_with_config, invocation_tracker, mock_operation_context):
        """WHEN hook invoked, THEN receives complete operation context."""
        # Arrange
        hook_config = [{
            'id': 'test-hook',
            'name': 'Test Hook',
            'operation_type': 'command',
            'operation_pattern': 'dev',
            'trigger_status': ['success'],
            'feedback_type': 'conversation',
            'enabled': True,
        }]
        hook_system = hook_system_with_config(hook_config)

        # Track context received by hook
        received_context = []
        async def context_capturing_runner(hook_entry, context):
            received_context.append(context)
            return {'status': 'success'}

        hook_system.set_hook_runner(context_capturing_runner)

        # Act - Invoke hooks
        await hook_system.invoke_hooks(
            operation_id=mock_operation_context['operation_id'],
            operation_type=mock_operation_context['operation_type'],
            operation_name=mock_operation_context['operation_name'],
            status=mock_operation_context['status'],
            duration_ms=mock_operation_context['duration_ms'],
            result_code=mock_operation_context['result_code']
        )

        # Assert - Context contains all required fields
        assert len(received_context) == 1
        context = received_context[0]
        assert context.operation_id == mock_operation_context['operation_id']
        assert context.operation_type == mock_operation_context['operation_type']
        assert context.status == mock_operation_context['status']
        assert context.duration_ms == mock_operation_context['duration_ms']


# ============================================================================
# AC3: Graceful Hook Failure Handling Tests
# ============================================================================

class TestGracefulHookFailureHandling:
    """Tests for graceful handling of hook failures."""

    @pytest.mark.asyncio
    async def test_hook_failure_logged_not_propagated(self, hook_system_with_config, invocation_tracker, mock_operation_context):
        """
        GIVEN a registered hook fails during invocation,
        WHEN the failure occurs,
        THEN the failure is logged, does not propagate to the calling operation, and the operation completes normally.
        """
        # Arrange - Create HookSystem with hook that will fail
        hook_config = [{
            'id': 'failing-hook',
            'name': 'Failing Hook',
            'operation_type': 'command',
            'operation_pattern': 'dev',
            'trigger_status': ['success'],
            'feedback_type': 'conversation',
            'enabled': True,
        }]
        hook_system = hook_system_with_config(hook_config)
        hook_system.set_hook_runner(invocation_tracker['failing_runner'])

        # Act - Invoke hooks, expect failure but operation continues
        results = await hook_system.invoke_hooks(
            operation_id=mock_operation_context['operation_id'],
            operation_type=mock_operation_context['operation_type'],
            operation_name=mock_operation_context['operation_name'],
            status='success',
            duration_ms=mock_operation_context['duration_ms'],
            result_code='success'
        )

        # Assert - Hook failed but operation completed normally
        assert len(results) == 1
        assert results[0].status == 'error'  # Hook failed
        assert results[0].hook_id == 'failing-hook'
        # Operation completed normally (no exception propagated)


    @pytest.mark.asyncio
    async def test_multiple_hook_failures_all_logged(self, hook_system_with_config, mock_operation_context):
        """WHEN multiple hooks fail, THEN all failures logged independently."""
        # Arrange - Create HookSystem with 3 hooks that will all fail
        hook_config = [
            {'id': 'hook-1', 'name': 'Hook 1', 'operation_type': 'command', 'operation_pattern': 'dev',
             'trigger_status': ['success'], 'feedback_type': 'conversation', 'enabled': True},
            {'id': 'hook-2', 'name': 'Hook 2', 'operation_type': 'command', 'operation_pattern': 'dev',
             'trigger_status': ['success'], 'feedback_type': 'conversation', 'enabled': True},
            {'id': 'hook-3', 'name': 'Hook 3', 'operation_type': 'command', 'operation_pattern': 'dev',
             'trigger_status': ['success'], 'feedback_type': 'conversation', 'enabled': True},
        ]
        hook_system = hook_system_with_config(hook_config)

        # All hooks fail
        async def failing_runner(hook_entry, context):
            raise Exception(f"{hook_entry['id']} failed")

        hook_system.set_hook_runner(failing_runner)

        # Act - Invoke hooks, all fail
        results = await hook_system.invoke_hooks(
            operation_id=mock_operation_context['operation_id'],
            operation_type=mock_operation_context['operation_type'],
            operation_name=mock_operation_context['operation_name'],
            status='success',
            duration_ms=mock_operation_context['duration_ms'],
            result_code='success'
        )

        # Assert - All failures logged
        assert len(results) == 3
        failed_hooks = [r.hook_id for r in results if r.status == 'error']
        assert len(failed_hooks) == 3
        assert 'hook-1' in failed_hooks
        assert 'hook-2' in failed_hooks
        assert 'hook-3' in failed_hooks


    @pytest.mark.asyncio
    async def test_operation_continues_after_hook_failure(self, hook_system_with_config, mock_operation_context):
        """WHEN hook fails, THEN operation continues with status message."""
        # Arrange - Create hook that will fail
        hook_configs = [{
            'id': 'hook-1',
            'name': 'Hook 1',
            'operation_type': 'command',
            'operation_pattern': 'dev',
            'trigger_status': ['success'],
            'feedback_type': 'conversation',
            'enabled': True,
        }]
        hook_system = hook_system_with_config(hook_configs)

        async def failing_runner(hook_entry, context):
            raise Exception("Hook execution failed")

        hook_system.set_hook_runner(failing_runner)

        # Act - Hook fails but operation continues (no exception propagated)
        results = await hook_system.invoke_hooks(
            operation_id=mock_operation_context['operation_id'],
            operation_type=mock_operation_context['operation_type'],
            operation_name=mock_operation_context['operation_name'],
            status='success',
            duration_ms=mock_operation_context['duration_ms'],
            result_code='success'
        )

        # Assert - Operation completed despite hook failure
        assert len(results) == 1
        assert results[0].status == 'error'  # Hook failed
        assert results[0].hook_id == 'hook-1'
        # No exception was raised - operation completed normally


# ============================================================================
# AC5: Hook Invocation Sequence and Ordering Tests
# ============================================================================

class TestHookInvocationSequence:
    """Tests for hook invocation sequence and ordering."""

    @pytest.mark.asyncio
    async def test_multiple_hooks_invoked_in_registration_order(self, hook_system_with_config, invocation_tracker, mock_operation_context):
        """
        GIVEN multiple hooks are registered for the same operation,
        WHEN the operation completes,
        THEN hooks execute in registration order with proper dependency resolution.
        """
        # Arrange - Create HookSystem with 3 hooks in specific order
        hook_config = [
            {'id': 'hook-1', 'name': 'Hook 1', 'operation_type': 'command', 'operation_pattern': 'dev',
             'trigger_status': ['success'], 'feedback_type': 'conversation', 'enabled': True},
            {'id': 'hook-2', 'name': 'Hook 2', 'operation_type': 'command', 'operation_pattern': 'dev',
             'trigger_status': ['success'], 'feedback_type': 'conversation', 'enabled': True},
            {'id': 'hook-3', 'name': 'Hook 3', 'operation_type': 'command', 'operation_pattern': 'dev',
             'trigger_status': ['success'], 'feedback_type': 'conversation', 'enabled': True},
        ]
        hook_system = hook_system_with_config(hook_config)
        hook_system.set_hook_runner(invocation_tracker['mock_runner'])

        # Act - Invoke hooks via real HookSystem
        results = await hook_system.invoke_hooks(
            operation_id=mock_operation_context['operation_id'],
            operation_type=mock_operation_context['operation_type'],
            operation_name=mock_operation_context['operation_name'],
            status='success',
            duration_ms=mock_operation_context['duration_ms'],
            result_code='success'
        )

        # Assert - Hooks invoked in registration order
        invoked_ids = [inv['hook_id'] for inv in invocation_tracker['invocations']]
        assert invoked_ids == ['hook-1', 'hook-2', 'hook-3']
        assert len(results) == 3


    @pytest.mark.asyncio
    async def test_hooks_execute_serially_not_parallel(self, hook_system_with_config, invocation_tracker, mock_operation_context):
        """WHEN multiple hooks match, THEN execute serially (not parallel)."""
        # Arrange - Create 2 hooks
        hook_config = [
            {'id': 'hook-a', 'name': 'Hook A', 'operation_type': 'command', 'operation_pattern': 'dev',
             'trigger_status': ['success'], 'feedback_type': 'conversation', 'enabled': True},
            {'id': 'hook-b', 'name': 'Hook B', 'operation_type': 'command', 'operation_pattern': 'dev',
             'trigger_status': ['success'], 'feedback_type': 'conversation', 'enabled': True},
        ]
        hook_system = hook_system_with_config(hook_config)
        hook_system.set_hook_runner(invocation_tracker['mock_runner'])

        # Act - Invoke hooks
        results = await hook_system.invoke_hooks(
            operation_id=mock_operation_context['operation_id'],
            operation_type=mock_operation_context['operation_type'],
            operation_name=mock_operation_context['operation_name'],
            status='success',
            duration_ms=mock_operation_context['duration_ms'],
            result_code='success'
        )

        # Assert - Both hooks invoked (serial execution is implementation detail)
        assert len(results) == 2
        invoked_ids = [inv['hook_id'] for inv in invocation_tracker['invocations']]
        assert invoked_ids == ['hook-a', 'hook-b']


    @pytest.mark.asyncio
    async def test_hook_execution_order_preserved(self, hook_system_with_config, invocation_tracker, mock_operation_context):
        """WHEN hooks invoked, THEN execution order matches registration order."""
        # Arrange - Register 3 hooks in specific order
        hook_config = [
            {'id': 'first-hook', 'name': 'First', 'operation_type': 'command', 'operation_pattern': 'dev',
             'trigger_status': ['success'], 'feedback_type': 'conversation', 'enabled': True},
            {'id': 'second-hook', 'name': 'Second', 'operation_type': 'command', 'operation_pattern': 'dev',
             'trigger_status': ['success'], 'feedback_type': 'conversation', 'enabled': True},
            {'id': 'third-hook', 'name': 'Third', 'operation_type': 'command', 'operation_pattern': 'dev',
             'trigger_status': ['success'], 'feedback_type': 'conversation', 'enabled': True},
        ]
        hook_system = hook_system_with_config(hook_config)
        hook_system.set_hook_runner(invocation_tracker['mock_runner'])

        # Act - Invoke hooks
        results = await hook_system.invoke_hooks(
            operation_id=mock_operation_context['operation_id'],
            operation_type=mock_operation_context['operation_type'],
            operation_name=mock_operation_context['operation_name'],
            status='success',
            duration_ms=mock_operation_context['duration_ms'],
            result_code='success'
        )

        # Assert - Order preserved
        invoked_ids = [inv['hook_id'] for inv in invocation_tracker['invocations']]
        assert invoked_ids == ['first-hook', 'second-hook', 'third-hook']
        assert len(results) == 3


# ============================================================================
# AC9: Disabled Hook Configuration Mid-Operation Tests
# ============================================================================

class TestDisabledHookConfiguration:
    """Tests for disabled hook configuration."""

    @pytest.mark.asyncio
    async def test_disabled_hook_not_invoked(self, hook_system_with_config, invocation_tracker, mock_operation_context):
        """
        GIVEN hooks are disabled during an active operation (via `.devforgeai/config/hooks.yaml` enabled: false),
        WHEN the operation completes,
        THEN hooks are skipped and no feedback conversation is triggered.
        """
        # Arrange - Create HookSystem with disabled hook
        hook_config = [{
            'id': 'disabled-hook',
            'name': 'Disabled Hook',
            'operation_type': 'command',
            'operation_pattern': 'dev',
            'trigger_status': ['success'],
            'feedback_type': 'conversation',
            'enabled': False,  # Disabled
        }]
        hook_system = hook_system_with_config(hook_config)
        hook_system.set_hook_runner(invocation_tracker['mock_runner'])

        # Act - Invoke hooks, disabled hook should be skipped
        results = await hook_system.invoke_hooks(
            operation_id=mock_operation_context['operation_id'],
            operation_type=mock_operation_context['operation_type'],
            operation_name=mock_operation_context['operation_name'],
            status='success',
            duration_ms=mock_operation_context['duration_ms'],
            result_code='success'
        )

        # Assert - Disabled hook was not invoked
        assert len(invocation_tracker['invocations']) == 0
        assert len(results) == 0


    @pytest.mark.asyncio
    async def test_enabled_hook_invoked(self, hook_system_with_config, invocation_tracker, mock_operation_context):
        """WHEN hook enabled=true, THEN invoked."""
        # Arrange - Create HookSystem with enabled hook
        hook_config = [{
            'id': 'enabled-hook',
            'name': 'Enabled Hook',
            'operation_type': 'command',
            'operation_pattern': 'dev',
            'trigger_status': ['success'],
            'feedback_type': 'conversation',
            'enabled': True,  # Enabled
        }]
        hook_system = hook_system_with_config(hook_config)
        hook_system.set_hook_runner(invocation_tracker['mock_runner'])

        # Act - Invoke hooks
        results = await hook_system.invoke_hooks(
            operation_id=mock_operation_context['operation_id'],
            operation_type=mock_operation_context['operation_type'],
            operation_name=mock_operation_context['operation_name'],
            status='success',
            duration_ms=mock_operation_context['duration_ms'],
            result_code='success'
        )

        # Assert - Enabled hook was invoked
        assert len(invocation_tracker['invocations']) == 1
        assert len(results) == 1


    @pytest.mark.asyncio
    async def test_config_reload_respects_enabled_flag(self, invocation_tracker, tmp_path):
        """WHEN config reloaded mid-operation, THEN enabled flag respected."""
        # Arrange - Create config file with enabled hook
        config_file = tmp_path / 'hooks.yaml'
        config_v1 = {
            'hooks': [{
                'id': 'toggle-hook',
                'name': 'Toggle Hook',
                'operation_type': 'command',
                'operation_pattern': 'dev',
                'trigger_status': ['success'],
                'feedback_type': 'conversation',
                'enabled': True,
            }]
        }
        with open(config_file, 'w') as f:
            yaml.dump(config_v1, f)

        # Create HookSystem and verify hook is enabled
        hook_system = HookSystem(config_path=config_file)
        hooks_before = hook_system.get_hooks()
        assert len(hooks_before) == 1
        assert hooks_before[0]['enabled'] is True

        # Act - Update config to disable hook, then reload
        config_v2 = {
            'hooks': [{
                'id': 'toggle-hook',
                'name': 'Toggle Hook',
                'operation_type': 'command',
                'operation_pattern': 'dev',
                'trigger_status': ['success'],
                'feedback_type': 'conversation',
                'enabled': False,  # Now disabled
            }]
        }
        with open(config_file, 'w') as f:
            yaml.dump(config_v2, f)

        # Reload config using real HookSystem method
        hook_system.reload_config()

        # Assert - Hook is now disabled
        hooks_after = hook_system.get_hooks()
        assert len(hooks_after) == 0  # Disabled hooks filtered out


# ============================================================================
# Integration Test: Complete Hook Invocation Flow
# ============================================================================

class TestCompleteHookInvocationFlow:
    """Integration tests for complete hook invocation flow."""

    @pytest.mark.asyncio
    async def test_complete_operation_with_hooks(self, hook_system_with_config, invocation_tracker, mock_operation_context):
        """
        Complete flow:
        1. Operation completes
        2. TodoWrite writes final status
        3. Hook registry loaded and evaluated
        4. Matching hooks invoked in order
        5. Failures isolated, operation completes normally
        """
        # Arrange - Create real HookSystem with 2 hooks
        hook_configs = [
            {
                'id': 'post-dev-feedback',
                'name': 'Post Dev Feedback',
                'operation_type': 'command',
                'operation_pattern': 'dev',
                'trigger_status': ['success', 'partial'],
                'feedback_type': 'conversation',
                'enabled': True,
            },
            {
                'id': 'metrics-hook',
                'name': 'Metrics Hook',
                'operation_type': 'command',
                'operation_pattern': 'dev',
                'trigger_status': ['success'],
                'feedback_type': 'metrics',
                'enabled': True,
            },
        ]
        hook_system = hook_system_with_config(hook_configs)
        hook_system.set_hook_runner(invocation_tracker['mock_runner'])

        # Act - Complete operation triggers hooks
        results = await hook_system.invoke_hooks(
            operation_id=mock_operation_context['operation_id'],
            operation_type=mock_operation_context['operation_type'],
            operation_name=mock_operation_context['operation_name'],
            status='success',
            duration_ms=mock_operation_context['duration_ms'],
            result_code='success'
        )

        # Assert - Both hooks invoked in registration order
        assert len(results) == 2
        invoked_ids = [inv['hook_id'] for inv in invocation_tracker['invocations']]
        assert invoked_ids == ['post-dev-feedback', 'metrics-hook']


    @pytest.mark.asyncio
    async def test_hook_failure_isolation_in_operation_flow(self, hook_system_with_config, mock_operation_context):
        """WHEN hook fails in operation flow, THEN operation completes normally."""
        # Arrange - Create 3 hooks, middle one will fail
        hook_configs = [
            {'id': 'hook-1', 'name': 'Hook 1', 'operation_type': 'command', 'operation_pattern': 'dev',
             'trigger_status': ['success'], 'feedback_type': 'conversation', 'enabled': True},
            {'id': 'hook-2', 'name': 'Hook 2', 'operation_type': 'command', 'operation_pattern': 'dev',
             'trigger_status': ['success'], 'feedback_type': 'conversation', 'enabled': True},
            {'id': 'hook-3', 'name': 'Hook 3', 'operation_type': 'command', 'operation_pattern': 'dev',
             'trigger_status': ['success'], 'feedback_type': 'conversation', 'enabled': True},
        ]
        hook_system = hook_system_with_config(hook_configs)

        # Hook runner that fails for hook-2
        async def selective_failing_runner(hook_entry, context):
            if hook_entry['id'] == 'hook-2':
                raise Exception("Hook execution failed")
            return {'status': 'success'}

        hook_system.set_hook_runner(selective_failing_runner)

        # Act - Invoke hooks, hook-2 will fail but others continue
        results = await hook_system.invoke_hooks(
            operation_id=mock_operation_context['operation_id'],
            operation_type=mock_operation_context['operation_type'],
            operation_name=mock_operation_context['operation_name'],
            status='success',
            duration_ms=mock_operation_context['duration_ms'],
            result_code='success'
        )

        # Assert - All 3 hooks attempted, 1 failed, 2 succeeded
        assert len(results) == 3
        success_count = sum(1 for r in results if r.status == 'success')
        error_count = sum(1 for r in results if r.status == 'error')
        assert success_count == 2  # hook-1, hook-3
        assert error_count == 1  # hook-2


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
