"""
Trigger condition evaluation for hook invocation.

Evaluates optional trigger conditions like duration, token usage, etc.
"""

from typing import Any, Dict, Optional
from dataclasses import dataclass
import logging

logger = logging.getLogger(__name__)

# Validation constants
MIN_PERCENT = 0
MAX_PERCENT = 100


@dataclass
class TriggerConditions:
    """Optional trigger conditions for hook invocation."""

    operation_duration_min_ms: Optional[int] = None
    operation_duration_max_ms: Optional[int] = None
    token_usage_percent_min: Optional[int] = None
    token_usage_percent_max: Optional[int] = None
    result_code: Optional[str] = None
    execution_order: Optional[int] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary, excluding None values."""
        return {k: v for k, v in self.__dict__.items() if v is not None}


class TriggerConditionEvaluator:
    """Evaluates trigger conditions against operation context."""

    def evaluate(
        self,
        context: Dict[str, Any],
        conditions: Optional[Dict[str, Any]] = None,
    ) -> bool:
        """
        Evaluate all trigger conditions against context.

        Args:
            context: Operation context with metadata
            conditions: Optional dict of trigger conditions

        Returns:
            True if all conditions match (or no conditions specified)

        """
        if not conditions:
            return True

        # Check duration range
        if "operation_duration_min_ms" in conditions:
            min_duration = conditions["operation_duration_min_ms"]
            if context.get("duration_ms", 0) < min_duration:
                return False

        if "operation_duration_max_ms" in conditions:
            max_duration = conditions["operation_duration_max_ms"]
            if context.get("duration_ms", 0) > max_duration:
                return False

        # Check token usage range
        if "token_usage_percent_min" in conditions:
            min_usage = conditions["token_usage_percent_min"]
            if context.get("token_usage", 0) < min_usage:
                return False

        if "token_usage_percent_max" in conditions:
            max_usage = conditions["token_usage_percent_max"]
            if context.get("token_usage", 0) > max_usage:
                return False

        # Check result code match
        if "result_code" in conditions:
            expected_code = conditions["result_code"]
            if context.get("result_code") != expected_code:
                return False

        # Check execution order
        if "execution_order" in conditions:
            expected_order = conditions["execution_order"]
            if context.get("execution_order") != expected_order:
                return False

        return True

    def validate_conditions(
        self, conditions: Dict[str, Any]
    ) -> tuple[bool, Optional[str]]:
        """
        Validate trigger conditions are well-formed.

        Args:
            conditions: Dict of trigger conditions

        Returns:
            Tuple of (is_valid, error_message)

        """
        if not conditions:
            return True, None

        # Validate duration ranges
        if "operation_duration_min_ms" in conditions and "operation_duration_max_ms" in conditions:
            min_val = conditions["operation_duration_min_ms"]
            max_val = conditions["operation_duration_max_ms"]
            if min_val > max_val:
                return False, "operation_duration_min_ms must be <= operation_duration_max_ms"

        # Validate token usage ranges
        if "token_usage_percent_min" in conditions:
            val = conditions["token_usage_percent_min"]
            if not (MIN_PERCENT <= val <= MAX_PERCENT):
                return False, f"token_usage_percent_min must be {MIN_PERCENT}-{MAX_PERCENT}"

        if "token_usage_percent_max" in conditions:
            val = conditions["token_usage_percent_max"]
            if not (MIN_PERCENT <= val <= MAX_PERCENT):
                return False, f"token_usage_percent_max must be {MIN_PERCENT}-{MAX_PERCENT}"

        # Validate min <= max for token usage
        if "token_usage_percent_min" in conditions and "token_usage_percent_max" in conditions:
            min_val = conditions["token_usage_percent_min"]
            max_val = conditions["token_usage_percent_max"]
            if min_val > max_val:
                return False, "token_usage_percent_min must be <= token_usage_percent_max"

        # Validate result_code is string if provided
        if "result_code" in conditions:
            if not isinstance(conditions["result_code"], str):
                return False, "result_code must be a string"

        return True, None
