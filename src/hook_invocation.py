"""
Hook invocation logic with pattern matching and condition evaluation.

This module handles the core hook invocation workflow:
1. Find hooks matching operation context (type, name, status)
2. Apply pattern matching (exact, glob, regex) on operation names
3. Evaluate trigger conditions for selective invocation
4. Detect and prevent circular dependencies
5. Enforce max invocation depth to prevent stack overflow
6. Execute hooks with timeout protection
7. Collect results from all invoked hooks

Thread-safe implementation for async contexts using locks for result collection.

Key classes:
- HookInvocationContext: Metadata about the operation triggering hooks
- HookInvocationResult: Result of attempting to invoke a hook
- HookInvoker: Main orchestrator for finding and invoking matching hooks

Example usage:
    invoker = HookInvoker(registry, circular_detector)
    context = HookInvocationContext(...)
    results = await invoker.invoke_matching_hooks(context)
    for result in results:
        if result.status == "success":
            print(f"Hook {result.hook_id} succeeded in {result.duration_ms}ms")
        elif result.status == "timeout":
            print(f"Hook {result.hook_id} timed out")
        elif result.status == "skipped":
            print(f"Hook {result.hook_id} skipped: {result.error}")
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

# Constants for timeout and performance defaults
DEFAULT_TIMEOUT_MS = 5000
DEFAULT_ASYNC_SLEEP_SECONDS = 0.01
TIMEOUT_CONVERSION_FACTOR = 1000  # Convert ms to seconds for asyncio.wait_for


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
    """
    Main orchestrator for finding and invoking matching hooks.

    Responsibilities:
    - Find hooks matching operation context (type, name, status)
    - Apply pattern matching on operation names
    - Evaluate trigger conditions
    - Detect circular dependencies and enforce depth limits
    - Invoke hooks serially with timeout protection
    - Collect results thread-safely

    Thread-safety:
    - Results stored in thread-safe manner using self._results_lock
    - Safe to call from async contexts
    - Safe to call from multiple threads (though typically async only)

    Circular dependency prevention:
    - Uses stack to track invocation chain
    - Detects self-references and cycles (A→B→C→A)
    - Max depth limit (default: 3) prevents unbounded recursion
    - Skips hooks that would cause circular dependencies
    """

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
            if self._check_circular_dependency(hook_id, results):
                continue

            # Check depth limit
            if self._check_max_depth(hook_id, results):
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

    def _check_circular_dependency(self, hook_id: str, results: List[HookInvocationResult]) -> bool:
        """
        Check if hook has circular dependency and add skip result if detected.

        Args:
            hook_id: ID of the hook to check
            results: Results list to append skip result if circular

        Returns:
            True if circular dependency detected, False otherwise

        """
        if not self.circular_detector.is_circular(hook_id):
            return False

        logger.warning(f"Circular dependency detected for hook {hook_id}")
        results.append(HookInvocationResult(
            hook_id=hook_id,
            status="skipped",
            duration_ms=0,
            error="Circular dependency detected",
        ))
        return True

    def _check_max_depth(self, hook_id: str, results: List[HookInvocationResult]) -> bool:
        """
        Check if max invocation depth exceeded and add skip result if true.

        Args:
            hook_id: ID of the hook to check
            results: Results list to append skip result if max depth exceeded

        Returns:
            True if max depth exceeded, False otherwise

        """
        if not self.circular_detector.at_max_depth():
            return False

        logger.warning(f"Max invocation depth reached, skipping hook {hook_id}")
        results.append(HookInvocationResult(
            hook_id=hook_id,
            status="skipped",
            duration_ms=0,
            error="Max invocation depth exceeded",
        ))
        return True

    def _add_skip_result(self, hook_id: str, error_message: str, results: List[HookInvocationResult]) -> None:
        """
        Add a skipped result to the results list.

        Args:
            hook_id: ID of the hook that was skipped
            error_message: Reason for skipping
            results: Results list to append skip result

        """
        results.append(HookInvocationResult(
            hook_id=hook_id,
            status="skipped",
            duration_ms=0,
            error=error_message,
        ))

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
        matching_hooks = []

        # Get all hooks for this operation type and status
        # Note: Pass '*' as operation_pattern to get all hooks, then filter by pattern below
        candidate_hooks = self.registry.get_hooks_for_operation(
            operation_type=context.operation_type,
            operation_pattern='*',  # Get all hooks, filter by pattern matching below
            trigger_status=context.status,
        )

        for hook_entry in candidate_hooks:
            # Match operation pattern
            hook_pattern = hook_entry["operation_pattern"]
            if not self.pattern_matcher.matches(context.operation_name, hook_pattern):
                continue

            # Check trigger conditions if present
            trigger_conditions = hook_entry.get("trigger_conditions")
            if not self.condition_evaluator.evaluate(context.to_dict(), trigger_conditions):
                continue

            matching_hooks.append(hook_entry)

        return matching_hooks

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
            # Run hook with timeout (convert milliseconds to seconds)
            result = await asyncio.wait_for(
                hook_runner(hook_entry, context),
                timeout=timeout_ms / TIMEOUT_CONVERSION_FACTOR,
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
            timeout_error_msg = f"Hook exceeded max_duration_ms ({timeout_ms}ms)"
            logger.warning(f"Hook {hook_id} exceeded timeout of {timeout_ms}ms (actual: {duration_ms}ms)")

            return HookInvocationResult(
                hook_id=hook_id,
                status="timeout",
                duration_ms=duration_ms,
                error=timeout_error_msg,
            )

        except Exception as e:
            duration_ms = _calculate_duration_ms(start_time)
            error_msg = str(e)
            logger.error(f"Error running hook {hook_id}: {error_msg}")

            return HookInvocationResult(
                hook_id=hook_id,
                status="error",
                duration_ms=duration_ms,
                error=error_msg,
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
        await asyncio.sleep(DEFAULT_ASYNC_SLEEP_SECONDS)

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
