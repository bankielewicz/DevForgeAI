"""
Hook invocation logic with pattern matching and condition evaluation.

Handles actual invocation of hooks, pattern matching, and condition checking.
Thread-safe implementation for async contexts.
"""

import asyncio
import time
import logging
import threading
from typing import Any, Dict, List, Optional, Callable, Awaitable
from dataclasses import dataclass, asdict
from datetime import datetime

from src.hook_patterns import PatternMatcher
from src.hook_conditions import TriggerConditionEvaluator
from src.hook_circular import CircularDependencyDetector
from src.hook_registry import HookRegistry, HookRegistryEntry

logger = logging.getLogger(__name__)

# Constants for timeout defaults
DEFAULT_TIMEOUT_MS = 5000


def _calculate_duration_ms(start_time: float) -> int:
    """
    Calculate elapsed duration in milliseconds.

    Args:
        start_time: Start time from time.time()

    Returns:
        Duration in milliseconds as integer
    """
    return int((time.time() - start_time) * 1000)


@dataclass
class HookInvocationContext:
    """Context for hook invocation with operation metadata."""

    invocation_id: str
    operation_id: str
    operation_type: str  # command, skill, subagent
    operation_name: str
    status: str  # success, failure, partial, deferred, completed
    duration_ms: int
    result_code: str
    token_usage: int  # percentage 0-100
    user_facing_output: str
    timestamp: str
    invocation_stack: List[str]
    trigger_conditions: Optional[Dict[str, Any]] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return asdict(self)


@dataclass
class HookInvocationResult:
    """Result of hook invocation."""

    hook_id: str
    status: str  # success, timeout, error, skipped
    duration_ms: int
    error: Optional[str] = None
    result: Optional[Dict[str, Any]] = None


class HookInvoker:
    """Invokes hooks based on pattern matching and conditions (thread-safe)."""

    def __init__(
        self,
        registry: HookRegistry,
        circular_detector: Optional[CircularDependencyDetector] = None,
    ):
        """
        Initialize hook invoker.

        Args:
            registry: Hook registry with loaded hooks
            circular_detector: Circular dependency detector (optional)

        """
        self.registry = registry
        self.circular_detector = circular_detector or CircularDependencyDetector()
        self.pattern_matcher = PatternMatcher()
        self.condition_evaluator = TriggerConditionEvaluator()
        self.invocation_results: List[HookInvocationResult] = []
        self._results_lock = threading.Lock()  # Protect invocation_results access

    async def invoke_matching_hooks(
        self,
        context: HookInvocationContext,
        hook_runner: Optional[Callable[[HookRegistryEntry, HookInvocationContext], Awaitable[Dict[str, Any]]]] = None,
    ) -> List[HookInvocationResult]:
        """
        Find and invoke all matching hooks.

        Args:
            context: Hook invocation context with operation metadata
            hook_runner: Optional async function to run hooks (for testing/mocking)

        Returns:
            List of invocation results

        """
        results = []

        # Find matching hooks
        matching_hooks = self._find_matching_hooks(context)

        # Invoke each hook serially in order
        for hook_entry in matching_hooks:
            hook_id = hook_entry["id"]

            # Check for circular dependency
            if self.circular_detector.is_circular(hook_id):
                logger.warning(f"Circular dependency detected for hook {hook_id}")
                results.append(HookInvocationResult(
                    hook_id=hook_id,
                    status="skipped",
                    duration_ms=0,
                    error="Circular dependency detected",
                ))
                continue

            # Check depth limit
            if self.circular_detector.at_max_depth():
                logger.warning(f"Max invocation depth reached, skipping hook {hook_id}")
                results.append(HookInvocationResult(
                    hook_id=hook_id,
                    status="skipped",
                    duration_ms=0,
                    error="Max invocation depth exceeded",
                ))
                continue

            # Push onto invocation stack
            if not self.circular_detector.push(hook_id):
                logger.warning(f"Cannot push {hook_id} onto invocation stack")
                continue

            try:
                # Invoke hook
                result = await self._invoke_hook(hook_entry, context, hook_runner)
                results.append(result)

            except Exception as e:
                logger.error(f"Error invoking hook {hook_id}: {e}")
                results.append(HookInvocationResult(
                    hook_id=hook_id,
                    status="error",
                    duration_ms=0,
                    error=str(e),
                ))

            finally:
                # Pop from stack
                self.circular_detector.pop(hook_id)

        # Store results thread-safely
        with self._results_lock:
            self.invocation_results = results
        return results

    def _find_matching_hooks(self, context: HookInvocationContext) -> List[HookRegistryEntry]:
        """
        Find hooks matching context criteria.

        Matches on:
        1. operation_type
        2. operation_pattern (using pattern matcher)
        3. trigger_status
        4. Optional trigger_conditions

        Args:
            context: Hook invocation context

        Returns:
            List of matching hook entries in registration order

        """
        matching = []

        # Get all hooks for this operation type and status
        # Note: Pass '*' as operation_pattern to get all hooks, then filter by pattern below
        candidates = self.registry.get_hooks_for_operation(
            operation_type=context.operation_type,
            operation_pattern='*',  # Get all hooks, filter by pattern matching below
            trigger_status=context.status,
        )

        for entry in candidates:
            # Match operation pattern
            pattern = entry["operation_pattern"]
            if not self.pattern_matcher.matches(context.operation_name, pattern):
                continue

            # Check trigger conditions if present
            trigger_conditions = entry.get("trigger_conditions")
            if not self.condition_evaluator.evaluate(context.to_dict(), trigger_conditions):
                continue

            matching.append(entry)

        return matching

    async def _invoke_hook(
        self,
        hook_entry: HookRegistryEntry,
        context: HookInvocationContext,
        hook_runner: Optional[Callable[[HookRegistryEntry, HookInvocationContext], Awaitable[Dict[str, Any]]]] = None,
    ) -> HookInvocationResult:
        """
        Invoke single hook with timeout protection.

        Args:
            hook_entry: Hook registry entry
            context: Hook invocation context
            hook_runner: Optional custom hook runner (for testing)

        Returns:
            HookInvocationResult

        """
        hook_id = hook_entry["id"]
        start_time = time.time()
        timeout_ms = hook_entry.get("max_duration_ms", DEFAULT_TIMEOUT_MS)

        # Use provided hook_runner or default
        if hook_runner is None:
            hook_runner = self._default_hook_runner

        try:
            # Run hook with timeout
            result = await asyncio.wait_for(
                hook_runner(hook_entry, context),
                timeout=timeout_ms / 1000,
            )

            duration_ms = _calculate_duration_ms(start_time)

            return HookInvocationResult(
                hook_id=hook_id,
                status="success",
                duration_ms=duration_ms,
                result=result,
            )

        except asyncio.TimeoutError:
            duration_ms = _calculate_duration_ms(start_time)
            logger.warning(f"Hook {hook_id} exceeded timeout of {timeout_ms}ms (actual: {duration_ms}ms)")

            return HookInvocationResult(
                hook_id=hook_id,
                status="timeout",
                duration_ms=duration_ms,
                error=f"Hook exceeded max_duration_ms ({timeout_ms}ms)",
            )

        except Exception as e:
            duration_ms = _calculate_duration_ms(start_time)
            logger.error(f"Error running hook {hook_id}: {e}")

            return HookInvocationResult(
                hook_id=hook_id,
                status="error",
                duration_ms=duration_ms,
                error=str(e),
            )

    async def _default_hook_runner(
        self,
        hook_entry: HookRegistryEntry,
        context: HookInvocationContext,
    ) -> Dict[str, Any]:
        """
        Default hook runner (can be overridden for testing).

        Args:
            hook_entry: Hook registry entry
            context: Hook invocation context

        Returns:
            Hook execution result

        """
        # Default implementation - just logs and returns success
        hook_id = hook_entry["id"]
        logger.info(f"Invoking hook {hook_id} for operation {context.operation_name}")

        # Simulate async work
        await asyncio.sleep(0.01)

        return {
            "hook_id": hook_id,
            "status": "success",
            "message": f"Hook {hook_id} executed successfully",
        }

    def get_results(self) -> List[HookInvocationResult]:
        """Get last invocation results (thread-safe)."""
        with self._results_lock:
            return self.invocation_results.copy()

    def clear_results(self) -> None:
        """Clear invocation results (thread-safe)."""
        with self._results_lock:
            self.invocation_results.clear()

    def reset_state(self) -> None:
        """Reset all internal state (thread-safe)."""
        self.circular_detector.reset()
        with self._results_lock:
            self.invocation_results.clear()
