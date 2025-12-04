"""
Configuration for CLAUDE.md merge operations.

Centralizes all merge-related configuration with validation.
"""


class MergeConfig:
    """
    Configuration for CLAUDE.md merge operations.

    CRITICAL REQUIREMENT: Validate all configuration values on access.

    Configuration Keys:
    - CONFLICT_THRESHOLD: Integer 0-100 (default 30)
      30% difference = CONFLICT (user changed >30% of framework section)
      Similarity >= 70% = NO CONFLICT
    - BACKUP_TIMESTAMP_FORMAT: strftime format (default "%Y%m%d-%H%M%S")
      Produces: YYYYMMDD-HHMMSS (e.g., 20251204-100000)
    - FRAMEWORK_SECTION_PATTERNS: List of framework section header names
      Used to identify which sections come from DevForgeAI
    - MAX_EXCERPT_LENGTH: Integer, max chars for conflict excerpts (default 200)
    """

    # Constants for validation
    MIN_CONFLICT_THRESHOLD = 0
    MAX_CONFLICT_THRESHOLD = 100
    MIN_EXCERPT_LENGTH = 1

    # Conflict threshold: 30% difference = conflict (70% similarity required)
    CONFLICT_THRESHOLD = 30

    # Backup timestamp format: YYYYMMDD-HHMMSS
    BACKUP_TIMESTAMP_FORMAT = "%Y%m%d-%H%M%S"

    # DevForgeAI framework section headers (used to identify framework vs user sections)
    # Only most distinctive framework headers to avoid false positives with user customization
    FRAMEWORK_SECTION_PATTERNS = [
        "CRITICAL: How Skills Work",
        "CRITICAL: Skill Invocation Constraints",
        "Core Philosophy",
        "DevForgeAI-CLI Validators",
        "Framework Status",
        "Learning DevForgeAI",
        "Root Cause Analysis Protocol",
        "Story Progress Tracking",
        "Acceptance Criteria vs. Tracking Mechanisms",
    ]

    # Maximum excerpt length for conflict details
    MAX_EXCERPT_LENGTH = 200

    @classmethod
    def validate(cls) -> bool:
        """
        Validate configuration values.

        Returns:
            True if all configuration is valid
        """
        # Validate CONFLICT_THRESHOLD
        if not isinstance(cls.CONFLICT_THRESHOLD, int):
            raise ValueError(
                f"CONFLICT_THRESHOLD must be int, got {type(cls.CONFLICT_THRESHOLD)}"
            )
        if not (cls.MIN_CONFLICT_THRESHOLD <= cls.CONFLICT_THRESHOLD <= cls.MAX_CONFLICT_THRESHOLD):
            raise ValueError(
                f"CONFLICT_THRESHOLD must be {cls.MIN_CONFLICT_THRESHOLD}-{cls.MAX_CONFLICT_THRESHOLD}, "
                f"got {cls.CONFLICT_THRESHOLD}"
            )

        # Validate BACKUP_TIMESTAMP_FORMAT
        if not isinstance(cls.BACKUP_TIMESTAMP_FORMAT, str):
            raise ValueError(
                f"BACKUP_TIMESTAMP_FORMAT must be str, got {type(cls.BACKUP_TIMESTAMP_FORMAT)}"
            )
        if not cls.BACKUP_TIMESTAMP_FORMAT:
            raise ValueError("BACKUP_TIMESTAMP_FORMAT must be non-empty")

        # Validate FRAMEWORK_SECTION_PATTERNS
        if not isinstance(cls.FRAMEWORK_SECTION_PATTERNS, list):
            raise ValueError(
                f"FRAMEWORK_SECTION_PATTERNS must be list, got {type(cls.FRAMEWORK_SECTION_PATTERNS)}"
            )
        if not cls.FRAMEWORK_SECTION_PATTERNS:
            raise ValueError("FRAMEWORK_SECTION_PATTERNS must be non-empty")
        for pattern in cls.FRAMEWORK_SECTION_PATTERNS:
            if not isinstance(pattern, str):
                raise ValueError(f"Pattern must be str, got {type(pattern)}")

        # Validate MAX_EXCERPT_LENGTH
        if not isinstance(cls.MAX_EXCERPT_LENGTH, int):
            raise ValueError(
                f"MAX_EXCERPT_LENGTH must be int, got {type(cls.MAX_EXCERPT_LENGTH)}"
            )
        if cls.MAX_EXCERPT_LENGTH < cls.MIN_EXCERPT_LENGTH:
            raise ValueError(
                f"MAX_EXCERPT_LENGTH must be >= {cls.MIN_EXCERPT_LENGTH}, got {cls.MAX_EXCERPT_LENGTH}"
            )

        return True

    @classmethod
    def get_similarity_threshold(cls) -> float:
        """
        Get similarity threshold as decimal (0.0-1.0).

        Returns:
            Similarity threshold as float (e.g., 0.70 for 70%)
        """
        return (100 - cls.CONFLICT_THRESHOLD) / 100.0

    @classmethod
    def is_framework_section(cls, section_name: str) -> bool:
        """
        Determine if section is framework section.

        Args:
            section_name: Header text of section

        Returns:
            True if section matches framework patterns
        """
        if not section_name:
            return False
        return section_name in cls.FRAMEWORK_SECTION_PATTERNS


# Validate configuration on import
MergeConfig.validate()
