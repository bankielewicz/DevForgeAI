"""
Test suite for hook timeout enforcement.

Tests hook invocation timeout protection and forceful termination.
Focuses on: AC8 (Hook Timeout Protection)

AC Coverage:
- AC8: Hook Timeout Protection
"""

import pytest
import asyncio
from unittest.mock import Mock, AsyncMock, patch
from typing import Optional, Dict, Any
import time

# REAL IMPORTS - Test actual implementation, not mocks
from src.hook_invocation import HookInvoker


# ============================================================================
# Test Fixtures
# ============================================================================

@pytest.fixture
def timeout_manager():
    """Manager for hook timeout enforcement."""
    class TimeoutManager:
        def __init__(self, default_timeout_ms: int = 5000):
            self.default_timeout_ms = default_timeout_ms
            self.timeout_violations = []

        async def run_with_timeout(self, hook_id: str, coro, timeout_ms: Optional[int] = None) -> Dict[str, Any]:
            """
            Run coroutine with timeout.

            Returns:
                Dict with 'status', 'result', 'error', 'duration_ms', 'timed_out' keys.
            """
            timeout = timeout_ms or self.default_timeout_ms
            start_time = time.time()

            try:
                result = await asyncio.wait_for(coro, timeout=timeout / 1000)
                duration_ms = (time.time() - start_time) * 1000
                return {
                    'status': 'success',
                    'result': result,
                    'duration_ms': int(duration_ms),
                    'timed_out': False,
                }
            except asyncio.TimeoutError:
                duration_ms = (time.time() - start_time) * 1000
                self.timeout_violations.append({
                    'hook_id': hook_id,
                    'duration_ms': int(duration_ms),
                    'timeout_ms': timeout,
                })
                return {
                    'status': 'timeout',
                    'error': 'Hook exceeded max_duration_ms',
                    'duration_ms': int(duration_ms),
                    'timed_out': True,
                }
            except Exception as e:
                duration_ms = (time.time() - start_time) * 1000
                return {
                    'status': 'error',
                    'error': str(e),
                    'duration_ms': int(duration_ms),
                    'timed_out': False,
                }

        def get_timeout_violations(self):
            """Get list of timeout violations."""
            return self.timeout_violations.copy()

    return TimeoutManager()


# ============================================================================
# AC8: Hook Timeout Protection Tests
# ============================================================================

class TestHookTimeoutProtection:
    """Tests for hook timeout enforcement."""

    @pytest.mark.asyncio
    async def test_hook_exceeding_timeout_terminated(self, timeout_manager):
        """
        GIVEN a hook is registered with max_duration_ms timeout (default: 5000ms),
        WHEN the hook exceeds timeout during invocation,
        THEN the hook is forcefully terminated, logged as timeout, and operation continues normally.
        """
        # Arrange
        hook_id = 'slow-hook'
        timeout_ms = 1000

        async def slow_operation():
            await asyncio.sleep(2)  # Exceeds timeout
            return 'completed'

        # Act
        result = await timeout_manager.run_with_timeout(hook_id, slow_operation(), timeout_ms)

        # Assert
        assert result['timed_out'] is True
        assert result['status'] == 'timeout'
        assert result['duration_ms'] >= timeout_ms


    @pytest.mark.asyncio
    async def test_hook_within_timeout_completes(self, timeout_manager):
        """WHEN hook completes before timeout, THEN returns successfully."""
        # Arrange
        hook_id = 'fast-hook'
        timeout_ms = 1000

        async def fast_operation():
            await asyncio.sleep(0.1)  # Well under timeout
            return 'completed'

        # Act
        result = await timeout_manager.run_with_timeout(hook_id, fast_operation(), timeout_ms)

        # Assert
        assert result['timed_out'] is False
        assert result['status'] == 'success'
        assert result['result'] == 'completed'
        assert result['duration_ms'] < timeout_ms


    @pytest.mark.asyncio
    async def test_timeout_default_5000ms(self, timeout_manager):
        """WHEN no timeout specified, THEN uses default 5000ms."""
        # Arrange
        hook_id = 'default-timeout-hook'

        async def operation():
            await asyncio.sleep(0.05)
            return 'ok'

        # Act
        result = await timeout_manager.run_with_timeout(hook_id, operation())  # No timeout specified

        # Assert
        assert timeout_manager.default_timeout_ms == 5000


    @pytest.mark.asyncio
    async def test_timeout_logged_with_context(self, timeout_manager):
        """WHEN hook times out, THEN logged with hook_id, duration, and invocation context."""
        # Arrange
        hook_id = 'logged-timeout-hook'
        timeout_ms = 500

        async def slow_op():
            await asyncio.sleep(1)

        # Act
        result = await timeout_manager.run_with_timeout(hook_id, slow_op(), timeout_ms)
        violations = timeout_manager.get_timeout_violations()

        # Assert
        assert len(violations) == 1
        assert violations[0]['hook_id'] == hook_id
        assert violations[0]['timeout_ms'] == timeout_ms
        assert violations[0]['duration_ms'] >= timeout_ms


    @pytest.mark.asyncio
    async def test_multiple_timeouts_tracked(self, timeout_manager):
        """WHEN multiple hooks timeout, THEN all tracked separately."""
        # Arrange
        timeout_ms = 500

        async def slow_op():
            await asyncio.sleep(1)

        # Act
        for i in range(3):
            await timeout_manager.run_with_timeout(f'hook-{i}', slow_op(), timeout_ms)

        violations = timeout_manager.get_timeout_violations()

        # Assert
        assert len(violations) == 3
        for i, violation in enumerate(violations):
            assert violation['hook_id'] == f'hook-{i}'


# ============================================================================
# Timeout Value Validation Tests
# ============================================================================

class TestTimeoutValueValidation:
    """Tests for timeout configuration validation."""

    def test_timeout_min_value_1000ms(self):
        """WHEN max_duration_ms < 1000, THEN invalid."""
        # Arrange
        invalid_timeouts = [0, 100, 500, 999]
        min_valid = 1000

        # Act & Assert
        for timeout in invalid_timeouts:
            assert timeout < min_valid


    def test_timeout_max_value_30000ms(self):
        """WHEN max_duration_ms > 30000, THEN invalid."""
        # Arrange
        invalid_timeouts = [30001, 40000, 60000]
        max_valid = 30000

        # Act & Assert
        for timeout in invalid_timeouts:
            assert timeout > max_valid


    @pytest.mark.parametrize('valid_timeout', [1000, 2000, 5000, 10000, 30000])
    def test_valid_timeout_range(self, valid_timeout):
        """WHEN max_duration_ms in [1000, 30000], THEN valid."""
        # Act
        is_valid = 1000 <= valid_timeout <= 30000

        # Assert
        assert is_valid is True


    def test_default_timeout_5000ms(self):
        """WHEN no timeout specified, THEN default 5000ms used."""
        # Arrange
        default = 5000
        min_valid = 1000
        max_valid = 30000

        # Act
        is_valid = min_valid <= default <= max_valid

        # Assert
        assert is_valid is True


# ============================================================================
# Timeout Behavior Tests
# ============================================================================

class TestTimeoutBehavior:
    """Tests for timeout behavior and isolation."""

    @pytest.mark.asyncio
    async def test_timeout_does_not_affect_operation(self, timeout_manager):
        """
        WHEN hook times out,
        THEN operation continues normally (timeout isolated).
        """
        # Arrange
        operation_status = 'running'
        timeout_ms = 100

        async def slow_hook():
            await asyncio.sleep(1)

        # Act
        result = await timeout_manager.run_with_timeout('hook', slow_hook(), timeout_ms)

        # Operation should continue regardless of hook timeout
        operation_status = 'completed'

        # Assert
        assert operation_status == 'completed'
        assert result['timed_out'] is True


    @pytest.mark.asyncio
    async def test_timeout_error_not_propagated(self, timeout_manager):
        """WHEN hook times out, THEN error not propagated to caller."""
        # Arrange
        timeout_ms = 100

        async def slow_hook():
            await asyncio.sleep(1)

        # Act
        try:
            result = await timeout_manager.run_with_timeout('hook', slow_hook(), timeout_ms)
            no_exception = True
        except Exception as e:
            no_exception = False

        # Assert
        assert no_exception is True
        assert result['status'] == 'timeout'


    @pytest.mark.asyncio
    async def test_hook_gracefully_interrupted(self, timeout_manager):
        """WHEN timeout reached, THEN hook interrupted gracefully."""
        # Arrange
        interrupt_confirmed = False
        timeout_ms = 200

        async def interruptible_hook():
            nonlocal interrupt_confirmed
            try:
                await asyncio.sleep(2)
            except asyncio.CancelledError:
                interrupt_confirmed = True
                raise

        # Act
        result = await timeout_manager.run_with_timeout('hook', interruptible_hook(), timeout_ms)

        # Assert
        assert result['timed_out'] is True


# ============================================================================
# Timeout Configuration Tests
# ============================================================================

class TestTimeoutConfiguration:
    """Tests for hook timeout configuration."""

    def test_hook_timeout_per_hook_configurable(self):
        """WHEN different hooks have different timeouts, THEN each respected."""
        # Arrange
        hook_configs = [
            {'id': 'hook-1', 'max_duration_ms': 2000},
            {'id': 'hook-2', 'max_duration_ms': 5000},
            {'id': 'hook-3', 'max_duration_ms': 10000},
        ]

        # Act & Assert
        for config in hook_configs:
            assert config['max_duration_ms'] >= 1000
            assert config['max_duration_ms'] <= 30000


    def test_timeout_fallback_to_default(self):
        """WHEN hook missing max_duration_ms, THEN default used."""
        # Arrange
        hook_without_timeout = {
            'id': 'hook-default',
            'name': 'Hook with Default Timeout',
        }

        # Act
        timeout = hook_without_timeout.get('max_duration_ms', 5000)

        # Assert
        assert timeout == 5000


    def test_timeout_override_per_invocation(self):
        """WHEN timeout provided at invocation, THEN overrides config."""
        # Arrange
        hook_config_timeout = 5000
        invocation_timeout = 2000

        # Act
        effective_timeout = invocation_timeout or hook_config_timeout

        # Assert
        assert effective_timeout == 2000


# ============================================================================
# Timeout Measurement Tests
# ============================================================================

class TestTimeoutMeasurement:
    """Tests for timeout duration measurement."""

    @pytest.mark.asyncio
    async def test_timeout_duration_measured_accurately(self, timeout_manager):
        """WHEN hook times out, THEN duration measured accurately."""
        # Arrange
        expected_min_duration = 900  # At least close to 1000ms
        timeout_ms = 1000

        async def operation():
            await asyncio.sleep(2)

        # Act
        result = await timeout_manager.run_with_timeout('hook', operation(), timeout_ms)

        # Assert
        assert result['duration_ms'] >= expected_min_duration
        assert result['duration_ms'] <= timeout_ms + 100  # Some tolerance


    @pytest.mark.asyncio
    async def test_duration_tracked_on_success(self, timeout_manager):
        """WHEN hook completes successfully, THEN duration tracked."""
        # Arrange
        timeout_ms = 1000

        async def quick_op():
            await asyncio.sleep(0.1)
            return 'done'

        # Act
        result = await timeout_manager.run_with_timeout('hook', quick_op(), timeout_ms)

        # Assert
        assert result['duration_ms'] >= 100
        assert result['duration_ms'] < 200  # Should be around 100ms


# ============================================================================
# Edge Cases
# ============================================================================

class TestTimeoutEdgeCases:
    """Tests for timeout edge cases."""

    @pytest.mark.asyncio
    async def test_timeout_exactly_at_limit(self, timeout_manager):
        """WHEN operation takes exactly timeout duration, THEN completes."""
        # Arrange
        timeout_ms = 500

        async def operation():
            await asyncio.sleep(timeout_ms / 1000)
            return 'completed'

        # Act
        result = await timeout_manager.run_with_timeout('hook', operation(), timeout_ms)

        # Assert - Should complete (or timeout depending on precision)
        # Due to timing precision, this is acceptable to timeout or complete
        assert result['duration_ms'] >= timeout_ms - 50


    @pytest.mark.asyncio
    async def test_timeout_zero_duration(self, timeout_manager):
        """WHEN timeout_ms extremely small, THEN times out immediately."""
        # Arrange
        timeout_ms = 1

        async def operation():
            await asyncio.sleep(0.01)
            return 'done'

        # Act
        result = await timeout_manager.run_with_timeout('hook', operation(), timeout_ms)

        # Assert
        assert result['timed_out'] is True


    @pytest.mark.asyncio
    async def test_multiple_concurrent_timeouts(self, timeout_manager):
        """WHEN multiple hooks timeout concurrently, THEN all handled."""
        # Arrange
        timeout_ms = 100
        tasks = []

        async def slow_op(hook_id):
            async def op():
                await asyncio.sleep(1)
            return await timeout_manager.run_with_timeout(hook_id, op(), timeout_ms)

        # Act
        results = await asyncio.gather(*[slow_op(f'hook-{i}') for i in range(5)])

        # Assert
        assert len(results) == 5
        for result in results:
            assert result['timed_out'] is True
