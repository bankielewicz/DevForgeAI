"""
Pattern matching for hook operation patterns.

Supports three pattern types:
- Exact match: "dev", "qa", "release"
- Glob patterns: "dev*", "create-*", "*-feedback"
- Regex patterns: "^dev$", "^(dev|qa)$", ".*feedback$"

Auto-detects pattern type based on content.
"""

import re
from enum import Enum
from fnmatch import fnmatch
from typing import Optional

# Pattern detection characters
REGEX_METACHARACTERS = r"^$.*+?{}[]|()"
GLOB_METACHARACTERS = "*?[]"


class PatternType(Enum):
    """Pattern type enumeration."""
    EXACT = "exact"
    GLOB = "glob"
    REGEX = "regex"


class PatternMatcher:
    """Matches operation patterns against hook patterns."""

    def __init__(self):
        """Initialize pattern matcher."""
        self._regex_cache: dict[str, re.Pattern] = {}

    @staticmethod
    def _detect_pattern_type(pattern: str) -> PatternType:
        """
        Detect pattern type based on content.

        Precedence:
        1. Regex if pattern starts with ^ or ends with $
        2. Glob if pattern contains *, ?, [
        3. Exact match otherwise

        Args:
            pattern: Pattern string to analyze

        Returns:
            PatternType enum value
        """
        # Regex has highest priority (^ and $ anchors)
        if pattern.startswith("^") or pattern.endswith("$"):
            return PatternType.REGEX

        # Check for regex metacharacters
        if any(c in pattern for c in REGEX_METACHARACTERS):
            return PatternType.REGEX

        # Check for glob patterns
        if any(c in pattern for c in GLOB_METACHARACTERS):
            return PatternType.GLOB

        # Default to exact match
        return PatternType.EXACT

    def matches(self, operation: str, pattern: str) -> bool:
        """
        Check if operation matches pattern.

        Args:
            operation: Operation name to match
            pattern: Pattern string (exact, glob, or regex)

        Returns:
            True if operation matches pattern, False otherwise

        Raises:
            ValueError: If operation or pattern is invalid
        """
        # Validate operation parameter
        if not isinstance(operation, str):
            raise ValueError(f"operation must be string, got {type(operation).__name__}")
        if not operation:
            raise ValueError("operation must be non-empty string")

        # Validate pattern parameter
        if not isinstance(pattern, str):
            raise ValueError(f"pattern must be string, got {type(pattern).__name__}")
        if not pattern:
            return False

        pattern_type = self._detect_pattern_type(pattern)

        if pattern_type == PatternType.EXACT:
            return operation == pattern

        elif pattern_type == PatternType.GLOB:
            return fnmatch(operation, pattern)

        elif pattern_type == PatternType.REGEX:
            try:
                # Use compiled pattern from cache if available
                if pattern not in self._regex_cache:
                    self._regex_cache[pattern] = re.compile(pattern)
                compiled = self._regex_cache[pattern]
                return bool(compiled.match(operation))
            except re.error as e:
                raise ValueError(f"Invalid regex pattern '{pattern}': {e}")

        return False

    def validate_pattern(self, pattern: str) -> tuple[bool, Optional[str]]:
        """
        Validate that a pattern is well-formed.

        Args:
            pattern: Pattern to validate

        Returns:
            Tuple of (is_valid, error_message)
        """
        if not pattern or not isinstance(pattern, str):
            return False, "Pattern must be a non-empty string"

        pattern_type = self._detect_pattern_type(pattern)

        if pattern_type == PatternType.REGEX:
            try:
                re.compile(pattern)
                return True, None
            except re.error as e:
                return False, f"Invalid regex: {e}"

        # Glob and exact patterns are always valid
        return True, None
