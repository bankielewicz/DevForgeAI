"""
Event-Driven Hook System for DevForgeAI.

Main orchestrator for hook management, loading, and invocation.

Features:
- Load hooks from .devforgeai/config/hooks.yaml
- Pattern matching (exact, glob, regex)
- Circular dependency detection
- Hook timeout protection
- Condition-based invocation
- Hot-reload support
"""

import asyncio
import logging
from pathlib import Path
from typing import Any, Dict, List, Optional, Callable, Awaitable
from datetime import datetime
import uuid

from src.hook_registry import HookRegistry, HookRegistryEntry
from src.hook_invocation import HookInvoker, HookInvocationContext, HookInvocationResult
from src.hook_circular import CircularDependencyDetector
from src.hook_patterns import PatternMatcher

logger = logging.getLogger(__name__)


class HookSystem:
    """Main hook system orchestrator."""

    def __init__(self, config_path: Optional[Path] = None):
        """
        Initialize hook system.

        Args:
            config_path: Path to hooks.yaml (default: .devforgeai/config/hooks.yaml)

        """
        self.config_path = config_path or Path(".devforgeai/config/hooks.yaml")
        self.registry = HookRegistry(self.config_path)
        self.circular_detector = CircularDependencyDetector(max_depth=3)
        self.invoker = HookInvoker(self.registry, self.circular_detector)
        self.pattern_matcher = PatternMatcher()
        self.hook_runner: Optional[Callable[[HookRegistryEntry, HookInvocationContext], Awaitable[Dict[str, Any]]]] = None

    def set_hook_runner(
        self,
        runner: Callable[[HookRegistryEntry, HookInvocationContext], Awaitable[Dict[str, Any]]],
    ) -> None:
        """
        Set custom hook runner for testing/integration.

        Args:
            runner: Async function(hook_entry, context) -> result dict

        """
        self.hook_runner = runner

    async def invoke_hooks(
        self,
        operation_id: str,
        operation_type: str,
        operation_name: str,
        status: str,
        duration_ms: int,
        result_code: str = "success",
        token_usage: int = 0,
        user_facing_output: str = "",
        trigger_conditions: Optional[Dict[str, Any]] = None,
    ) -> List[HookInvocationResult]:
        """
        Invoke hooks for operation completion.

        This is the main entry point called when an operation (command, skill, or
        subagent) completes.

        Args:
            operation_id: Unique operation identifier
            operation_type: Type of operation (command, skill, subagent)
            operation_name: Name of operation (e.g., "dev", "qa", "create-story")
            status: Operation status (success, failure, partial, deferred, completed)
            duration_ms: Operation duration in milliseconds
            result_code: Result code from operation (optional)
            token_usage: Token usage percentage 0-100 (optional)
            user_facing_output: User-facing output message (optional)
            trigger_conditions: Optional conditions for filtering (optional)

        Returns:
            List of HookInvocationResult for each invoked hook

        """
        # Create invocation context
        context = HookInvocationContext(
            invocation_id=str(uuid.uuid4()),
            operation_id=operation_id,
            operation_type=operation_type,
            operation_name=operation_name,
            status=status,
            duration_ms=duration_ms,
            result_code=result_code,
            token_usage=token_usage,
            user_facing_output=user_facing_output,
            timestamp=datetime.utcnow().isoformat() + "Z",
            invocation_stack=[],
            trigger_conditions=trigger_conditions,
        )

        logger.info(
            f"Invoking hooks for operation {operation_name} "
            f"(type: {operation_type}, status: {status})"
        )

        # Reset state for this invocation
        self.circular_detector.reset()

        # Invoke matching hooks
        results = await self.invoker.invoke_matching_hooks(context, self.hook_runner)

        # Log results
        success_count = sum(1 for r in results if r.status == "success")
        failure_count = sum(1 for r in results if r.status == "error")
        timeout_count = sum(1 for r in results if r.status == "timeout")
        skipped_count = sum(1 for r in results if r.status == "skipped")

        logger.info(
            f"Hook invocation complete: "
            f"{success_count} success, {failure_count} error, {timeout_count} timeout, {skipped_count} skipped"
        )

        return results

    def reload_config(self) -> bool:
        """
        Reload hook configuration from file.

        Preserves runtime state during reload.

        Returns:
            True if reload successful, False otherwise

        """
        logger.info(f"Reloading hook configuration from {self.config_path}")

        try:
            # Reload registry (preserves existing invoker state)
            success = self.registry.reload()

            if success:
                logger.info(f"Reloaded {self.registry.size()} hooks successfully")
            else:
                errors = self.registry.get_load_errors()
                logger.error(f"Reload errors: {errors}")

            return success

        except Exception as e:
            logger.error(f"Failed to reload config: {e}")
            return False

    def get_hooks(self) -> List[HookRegistryEntry]:
        """Get all registered hooks."""
        return self.registry.get_all_hooks()

    def get_hook(self, hook_id: str) -> Optional[HookRegistryEntry]:
        """Get hook by ID."""
        return self.registry.get_hook(hook_id)

    def get_hooks_for_operation(
        self,
        operation_type: str,
        trigger_status: str,
    ) -> List[HookRegistryEntry]:
        """
        Get hooks that would be invoked for given operation.

        Note: Does NOT check pattern matching - returns candidates only.

        Args:
            operation_type: Operation type (command, skill, subagent)
            trigger_status: Operation status

        Returns:
            List of candidate hook entries

        """
        return self.registry.get_hooks_for_operation(
            operation_type=operation_type,
            operation_pattern="*",  # Wildcard - caller should filter
            trigger_status=trigger_status,
        )

    def get_registry_size(self) -> int:
        """Get number of registered hooks."""
        return self.registry.size()

    def has_registry_errors(self) -> bool:
        """Check if registry has load errors."""
        return self.registry.has_errors()

    def get_registry_errors(self) -> List[str]:
        """Get registry load errors."""
        return self.registry.get_load_errors()

    def validate_pattern(self, pattern: str) -> tuple[bool, Optional[str]]:
        """
        Validate a hook pattern.

        Args:
            pattern: Pattern to validate

        Returns:
            Tuple of (is_valid, error_message)

        """
        return self.pattern_matcher.validate_pattern(pattern)

    def reset(self) -> None:
        """Reset hook system state."""
        self.circular_detector.reset()
        self.invoker.clear_results()
