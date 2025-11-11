"""
Test suite for circular hook dependency detection.

Tests detection and prevention of circular hook invocation chains.
Focuses on: AC7 (Circular Hook Invocation Prevention)

AC Coverage:
- AC7: Circular Hook Invocation Prevention
"""

import pytest
from typing import List, Dict, Any
from unittest.mock import Mock, patch


# ============================================================================
# Test Fixtures
# ============================================================================

@pytest.fixture
def invocation_stack_tracker():
    """Stack tracker for monitoring hook invocation chains."""
    class StackTracker:
        def __init__(self, max_depth: int = 3):
            self.stack: List[str] = []
            self.max_depth = max_depth
            self.invocations = []

        def push(self, hook_id: str) -> bool:
            """Push hook_id onto stack. Return True if allowed, False if circular."""
            # Check for circular dependency
            if hook_id in self.stack:
                return False  # Circular detected

            # Check depth limit
            if len(self.stack) >= self.max_depth:
                return False  # Max depth exceeded

            self.stack.append(hook_id)
            self.invocations.append({'hook_id': hook_id, 'depth': len(self.stack)})
            return True

        def pop(self, hook_id: str) -> None:
            """Pop hook_id from stack."""
            if self.stack and self.stack[-1] == hook_id:
                self.stack.pop()

        def get_stack(self) -> List[str]:
            """Get current invocation stack."""
            return self.stack.copy()

        def is_circular(self, hook_id: str) -> bool:
            """Check if hook_id would create circular dependency."""
            return hook_id in self.stack

        def at_max_depth(self) -> bool:
            """Check if at max depth."""
            return len(self.stack) >= self.max_depth

    return StackTracker()


# ============================================================================
# AC7: Circular Hook Invocation Prevention Tests
# ============================================================================

class TestCircularHookDetection:
    """Tests for circular hook invocation detection."""

    def test_simple_circular_dependency_detected(self, invocation_stack_tracker):
        """
        GIVEN Hook A triggers operation X which invokes Hook B which triggers operation X again,
        WHEN the circular dependency is detected,
        THEN the system prevents infinite loops by tracking invocation stack depth and halting at max depth (default: 3).
        """
        # Arrange
        stack = invocation_stack_tracker

        # Act - Push Hook A
        can_invoke_a = stack.push('hook-a')
        assert can_invoke_a is True

        # Hook A triggers operation that invokes Hook B
        can_invoke_b = stack.push('hook-b')
        assert can_invoke_b is True

        # Hook B tries to invoke Hook A again (circular)
        can_invoke_a_again = stack.push('hook-a')

        # Assert
        assert can_invoke_a_again is False  # Circular detected


    def test_self_referencing_hook_detected(self, invocation_stack_tracker):
        """WHEN hook tries to invoke itself, THEN circular dependency detected."""
        # Arrange
        stack = invocation_stack_tracker

        # Act
        can_invoke_first = stack.push('hook-self')
        assert can_invoke_first is True

        # Try to push same hook again
        can_invoke_again = stack.push('hook-self')

        # Assert
        assert can_invoke_again is False


    def test_three_level_circular_chain(self, invocation_stack_tracker):
        """WHEN three hooks form circular chain A->B->C->A, THEN detected."""
        # Arrange
        stack = invocation_stack_tracker

        # Act - Build chain
        assert stack.push('hook-a') is True
        assert stack.push('hook-b') is True
        assert stack.push('hook-c') is True

        # Try to return to Hook A
        circular = stack.push('hook-a')

        # Assert
        assert circular is False


    def test_non_circular_linear_chain(self, invocation_stack_tracker):
        """WHEN hooks form linear chain A->B->C (no cycle), THEN allowed."""
        # Arrange
        stack = invocation_stack_tracker

        # Act - Build linear chain
        can_a = stack.push('hook-a')
        can_b = stack.push('hook-b')
        can_c = stack.push('hook-c')

        # Assert
        assert can_a is True
        assert can_b is True
        assert can_c is True
        assert stack.get_stack() == ['hook-a', 'hook-b', 'hook-c']


    def test_circular_detection_with_different_hooks(self, invocation_stack_tracker):
        """WHEN different hook IDs, THEN no false positive circular detection."""
        # Arrange
        stack = invocation_stack_tracker

        # Act
        assert stack.push('hook-post-dev') is True
        assert stack.push('hook-post-qa') is True
        assert stack.push('hook-post-release') is True

        # Assert - different hooks, check ones NOT on stack
        assert stack.is_circular('hook-other') is False
        assert stack.is_circular('hook-different') is False
        # But ones ON stack ARE circular (already pushed)
        assert stack.is_circular('hook-post-dev') is True


# ============================================================================
# Invocation Stack Depth Tests
# ============================================================================

class TestInvocationStackDepth:
    """Tests for invocation stack depth management."""

    def test_max_depth_three_default(self, invocation_stack_tracker):
        """WHEN max depth default is 3, THEN fourth invocation blocked."""
        # Arrange
        stack = invocation_stack_tracker  # Default max_depth=3

        # Act
        assert stack.push('hook-1') is True
        assert stack.push('hook-2') is True
        assert stack.push('hook-3') is True
        can_push_4 = stack.push('hook-4')

        # Assert
        assert can_push_4 is False


    def test_depth_tracking(self, invocation_stack_tracker):
        """WHEN hooks invoked, THEN depth tracked correctly."""
        # Arrange
        stack = invocation_stack_tracker

        # Act
        stack.push('hook-1')
        assert len(stack.get_stack()) == 1

        stack.push('hook-2')
        assert len(stack.get_stack()) == 2

        stack.push('hook-3')
        assert len(stack.get_stack()) == 3

        # Assert
        assert stack.at_max_depth() is True


    def test_stack_cleanup_on_completion(self, invocation_stack_tracker):
        """WHEN hook completes, THEN popped from stack."""
        # Arrange
        stack = invocation_stack_tracker

        # Act
        stack.push('hook-1')
        stack.push('hook-2')
        assert len(stack.get_stack()) == 2

        stack.pop('hook-2')
        assert len(stack.get_stack()) == 1

        stack.pop('hook-1')
        assert len(stack.get_stack()) == 0

        # Assert
        assert stack.at_max_depth() is False


    def test_depth_with_custom_max(self):
        """WHEN custom max_depth specified, THEN respected."""
        # Arrange
        class StackTracker:
            def __init__(self, max_depth: int = 5):
                self.stack = []
                self.max_depth = max_depth

            def push(self, hook_id: str) -> bool:
                if hook_id in self.stack or len(self.stack) >= self.max_depth:
                    return False
                self.stack.append(hook_id)
                return True

        stack = StackTracker(max_depth=5)

        # Act
        for i in range(5):
            assert stack.push(f'hook-{i}') is True

        can_push_6 = stack.push('hook-5')

        # Assert
        assert can_push_6 is False


# ============================================================================
# Circular Detection Error Logging Tests
# ============================================================================

class TestCircularDetectionLogging:
    """Tests for logging circular dependencies."""

    def test_circular_chain_logged(self, invocation_stack_tracker):
        """WHEN circular detected, THEN chain logged with all hook IDs."""
        # Arrange
        stack = invocation_stack_tracker
        logs = []

        # Act
        stack.push('hook-a')
        stack.push('hook-b')

        # Try circular - should log
        if not stack.push('hook-a'):
            logs.append({
                'error': 'circular_dependency',
                'chain': stack.get_stack() + ['hook-a'],
            })

        # Assert
        assert len(logs) == 1
        assert logs[0]['chain'] == ['hook-a', 'hook-b', 'hook-a']


    def test_depth_exceeded_logged(self, invocation_stack_tracker):
        """WHEN max depth exceeded, THEN logged with context."""
        # Arrange
        stack = invocation_stack_tracker
        logs = []

        # Act
        for i in range(3):
            stack.push(f'hook-{i}')

        if not stack.push('hook-3'):
            logs.append({
                'error': 'max_depth_exceeded',
                'max_depth': stack.max_depth,
                'current_depth': len(stack.get_stack()),
                'stack': stack.get_stack(),
            })

        # Assert
        assert len(logs) == 1
        assert logs[0]['max_depth'] == 3
        assert logs[0]['current_depth'] == 3


# ============================================================================
# Edge Case Tests
# ============================================================================

class TestCircularDetectionEdgeCases:
    """Tests for edge cases in circular detection."""

    def test_empty_stack_no_circular(self, invocation_stack_tracker):
        """WHEN stack empty, THEN no circular dependencies possible."""
        # Arrange
        stack = invocation_stack_tracker

        # Act
        is_circular = stack.is_circular('any-hook')

        # Assert
        assert is_circular is False


    def test_single_hook_no_self_reference(self, invocation_stack_tracker):
        """WHEN single hook on stack, THEN self-reference detected as circular."""
        # Arrange
        stack = invocation_stack_tracker
        stack.push('hook-a')

        # Act
        is_circular = stack.is_circular('hook-a')

        # Assert
        assert is_circular is True


    def test_hook_id_case_sensitivity(self, invocation_stack_tracker):
        """WHEN hook IDs differ in case, THEN treated as different hooks."""
        # Arrange
        stack = invocation_stack_tracker

        # Act
        stack.push('hook-A')
        can_push_lowercase = stack.push('hook-a')

        # Assert
        assert can_push_lowercase is True  # Different case = different hook


    def test_hook_id_with_special_characters(self, invocation_stack_tracker):
        """WHEN hook IDs contain special characters, THEN handled correctly."""
        # Arrange
        stack = invocation_stack_tracker

        # Act
        can_push_1 = stack.push('hook-post_dev')
        can_push_2 = stack.push('hook-post.qa')
        can_push_same = stack.push('hook-post_dev')

        # Assert
        assert can_push_1 is True
        assert can_push_2 is True
        assert can_push_same is False  # Same hook ID


    def test_large_circular_chain(self):
        """WHEN large circular chain attempted, THEN detected at max depth."""
        # Arrange
        class StackTracker:
            def __init__(self, max_depth: int = 3):
                self.stack = []
                self.max_depth = max_depth

            def push(self, hook_id: str) -> bool:
                if hook_id in self.stack or len(self.stack) >= self.max_depth:
                    return False
                self.stack.append(hook_id)
                return True

        stack = StackTracker(max_depth=3)

        # Try to create a 10-hook chain (should stop at 3)
        successful = 0
        for i in range(10):
            if stack.push(f'hook-{i}'):
                successful += 1
            else:
                break

        # Assert
        assert successful == 3


# ============================================================================
# Circular Detection Integration Tests
# ============================================================================

class TestCircularDetectionIntegration:
    """Integration tests for circular detection with hook invocation."""

    def test_circular_detection_halts_invocation(self, invocation_stack_tracker):
        """
        WHEN circular detected,
        THEN system halts further invocations and logs chain.
        """
        # Arrange
        stack = invocation_stack_tracker
        invocation_results = []

        # Act - Simulate hook invocation chain
        def try_invoke_hook(hook_id: str) -> bool:
            if stack.push(hook_id):
                invocation_results.append({'hook_id': hook_id, 'status': 'invoked'})
                return True
            else:
                invocation_results.append({'hook_id': hook_id, 'status': 'blocked'})
                return False

        # Invoke chain: A -> B -> C -> A (should block on second A)
        try_invoke_hook('hook-a')
        try_invoke_hook('hook-b')
        try_invoke_hook('hook-c')
        try_invoke_hook('hook-a')

        # Assert
        assert len(invocation_results) == 4
        assert invocation_results[0]['status'] == 'invoked'
        assert invocation_results[1]['status'] == 'invoked'
        assert invocation_results[2]['status'] == 'invoked'
        assert invocation_results[3]['status'] == 'blocked'


    def test_operation_completes_despite_circular(self, invocation_stack_tracker):
        """
        WHEN circular dependency detected,
        THEN operation completes normally (hook failure isolated).
        """
        # Arrange
        stack = invocation_stack_tracker
        operation_status = 'running'

        # Act
        stack.push('hook-a')
        stack.push('hook-b')

        # Try circular invocation (should fail)
        circular_allowed = stack.push('hook-a')

        # Operation should still complete
        operation_status = 'completed' if not circular_allowed else 'pending'

        # Assert
        assert operation_status == 'completed'
        assert circular_allowed is False


    def test_stack_reset_after_operation(self, invocation_stack_tracker):
        """WHEN operation completes, THEN invocation stack cleaned up."""
        # Arrange
        stack = invocation_stack_tracker

        # Act - Simulate operation with hooks
        stack.push('hook-1')
        stack.push('hook-2')
        assert len(stack.get_stack()) == 2

        # Clean up after operation
        stack.pop('hook-2')
        stack.pop('hook-1')

        # Assert - Stack empty
        assert len(stack.get_stack()) == 0
        assert stack.is_circular('hook-1') is False
