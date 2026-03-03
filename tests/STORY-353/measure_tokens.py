"""
Shared token measurement utilities for STORY-353 A/B testing.

Token counting uses character count / 4 as approximation for LLM tokens.
"""
from typing import Union


def estimate_tokens(text: str) -> int:
    """
    Estimate token count using character count / 4 approximation.

    Args:
        text: Text to count tokens for

    Returns:
        Estimated token count (integer)
    """
    if not text:
        return 0
    return len(text) // 4


def calculate_reduction(grep_tokens: int, treelint_tokens: int) -> float:
    """
    Calculate token reduction percentage.

    Formula: ((grep_tokens - treelint_tokens) / grep_tokens) * 100

    Args:
        grep_tokens: Token count from Grep baseline
        treelint_tokens: Token count from Treelint

    Returns:
        Reduction percentage (0-100 scale)

    Raises:
        ValueError: If grep_tokens is zero (division by zero)
    """
    if grep_tokens == 0:
        raise ValueError("grep_tokens cannot be zero (division by zero)")

    return ((grep_tokens - treelint_tokens) / grep_tokens) * 100


def validate_threshold(reduction_pct: float, threshold: float = 40.0) -> bool:
    """
    Validate if reduction meets threshold (default 40%).

    Args:
        reduction_pct: Calculated reduction percentage
        threshold: Minimum reduction required (default 40.0)

    Returns:
        True if reduction >= threshold, False otherwise
    """
    return reduction_pct >= threshold


def calculate_average_reduction(reductions: list) -> float:
    """
    Calculate average reduction across multiple queries.

    Args:
        reductions: List of reduction percentages

    Returns:
        Average reduction percentage
    """
    if not reductions:
        return 0.0
    return sum(reductions) / len(reductions)
