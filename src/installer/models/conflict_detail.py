"""
ConflictDetail dataclass for representing detected conflicts.

Stores detailed information about conflicts between user and framework sections.
"""

from dataclasses import dataclass


@dataclass
class ConflictDetail:
    """
    Details of a detected conflict between user and framework content.

    CRITICAL REQUIREMENT: Validate all numeric fields and truncate excerpts.

    Attributes:
        section_name: Header name of conflicting section (required, non-empty)
        line_start: Starting line number (required, positive integer)
        line_end: Ending line number (required, >= line_start)
        user_excerpt: User content excerpt (required, max 200 chars)
        framework_excerpt: Framework content excerpt (required, max 200 chars)
        similarity_ratio: Content similarity as float 0.0-1.0 (0.0=completely different, 1.0=identical)
    """
    section_name: str
    line_start: int
    line_end: int
    user_excerpt: str
    framework_excerpt: str
    similarity_ratio: float

    def __post_init__(self):
        """
        Validate ConflictDetail after initialization.

        Validations:
        - section_name: Non-empty string
        - line_start/line_end: Positive integers, end >= start
        - similarity_ratio: Float between 0.0 and 1.0
        - excerpts: Truncated to 200 chars max
        """
        # Validate section name
        if not self.section_name or not isinstance(self.section_name, str):
            raise ValueError(f"section_name must be non-empty string, got {self.section_name!r}")

        # Validate line numbers
        if not isinstance(self.line_start, int) or self.line_start <= 0:
            raise ValueError(f"line_start must be positive integer, got {self.line_start}")

        if not isinstance(self.line_end, int) or self.line_end <= 0:
            raise ValueError(f"line_end must be positive integer, got {self.line_end}")

        if self.line_end < self.line_start:
            raise ValueError(f"line_end ({self.line_end}) must be >= line_start ({self.line_start})")

        # Validate similarity ratio
        if not isinstance(self.similarity_ratio, (int, float)):
            raise ValueError(f"similarity_ratio must be number, got {type(self.similarity_ratio)}")

        if not (0.0 <= self.similarity_ratio <= 1.0):
            raise ValueError(
                f"similarity_ratio must be 0.0-1.0, got {self.similarity_ratio}"
            )

        # Truncate excerpts to 200 chars
        self.user_excerpt = self.user_excerpt[:200] if self.user_excerpt else ""
        self.framework_excerpt = self.framework_excerpt[:200] if self.framework_excerpt else ""
