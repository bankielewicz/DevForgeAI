"""
Circular dependency detection for hook invocation chains.

Tracks hook invocation stacks to prevent infinite loops and circular dependencies.
Thread-safe implementation for async contexts.
"""

from typing import List, Optional
import logging
import threading

logger = logging.getLogger(__name__)

# Configuration constants
DEFAULT_MAX_DEPTH = 3


class CircularDependencyDetector:
    """Detects and prevents circular hook invocation chains (thread-safe)."""

    def __init__(self, max_depth: int = DEFAULT_MAX_DEPTH):
        """
        Initialize circular dependency detector.

        Args:
            max_depth: Maximum allowed invocation depth (default: 3)

        Raises:
            ValueError: If max_depth < 1
        """
        if max_depth < 1:
            raise ValueError("max_depth must be >= 1")

        self.max_depth = max_depth
        self.stack: List[str] = []
        self.invocation_history: List[dict] = []
        self._lock = threading.RLock()  # Reentrant lock for thread-safety

    def push(self, hook_id: str) -> bool:
        """
        Push hook onto invocation stack (thread-safe).

        Checks for:
        1. Circular dependency (hook already in stack)
        2. Max depth exceeded

        Args:
            hook_id: Hook ID to push

        Returns:
            True if push allowed, False if circular or depth exceeded

        """
        with self._lock:
            # Check for circular dependency
            if hook_id in self.stack:
                logger.warning(
                    f"Circular dependency detected: {hook_id} already in stack {self.stack}"
                )
                return False

            # Check depth limit
            if len(self.stack) >= self.max_depth:
                logger.warning(
                    f"Max invocation depth ({self.max_depth}) exceeded, cannot invoke {hook_id}"
                )
                return False

            # Push hook and record
            self.stack.append(hook_id)
            self.invocation_history.append({
                "hook_id": hook_id,
                "depth": len(self.stack),
                "action": "push",
            })

            return True

    def pop(self, hook_id: str) -> bool:
        """
        Pop hook from invocation stack (thread-safe).

        Args:
            hook_id: Hook ID to pop

        Returns:
            True if popped successfully, False if not at top of stack

        """
        with self._lock:
            if not self.stack:
                return False

            if self.stack[-1] != hook_id:
                logger.warning(
                    f"Cannot pop {hook_id}: top of stack is {self.stack[-1]}"
                )
                return False

            self.stack.pop()
            self.invocation_history.append({
                "hook_id": hook_id,
                "depth": len(self.stack),
                "action": "pop",
            })

            return True

    def is_circular(self, hook_id: str) -> bool:
        """
        Check if invoking hook_id would create circular dependency (thread-safe).

        Args:
            hook_id: Hook ID to check

        Returns:
            True if hook_id already in stack (would be circular)

        """
        with self._lock:
            return hook_id in self.stack

    def at_max_depth(self) -> bool:
        """
        Check if current depth equals max depth (thread-safe).

        Returns:
            True if at or exceeding max depth

        """
        with self._lock:
            return len(self.stack) >= self.max_depth

    def get_stack(self) -> List[str]:
        """
        Get copy of current invocation stack (thread-safe).

        Returns:
            Copy of invocation stack

        """
        with self._lock:
            return self.stack.copy()

    def get_current_depth(self) -> int:
        """
        Get current invocation depth (thread-safe).

        Returns:
            Number of hooks currently on stack

        """
        with self._lock:
            return len(self.stack)

    def reset(self) -> None:
        """Reset stack and history (thread-safe)."""
        with self._lock:
            self.stack.clear()
            self.invocation_history.clear()

    def get_history(self) -> List[dict]:
        """
        Get invocation history (thread-safe).

        Returns:
            List of invocation history entries

        """
        with self._lock:
            return self.invocation_history.copy()
