"""
MergeConflictDetectionService for detecting conflicts during merge.

Requirements:
- SVC-010: Parse CLAUDE.md into sections
- SVC-011: Identify framework vs user sections
- SVC-012: Detect conflicts using similarity threshold (>30% change)
- SVC-013: Handle user sections with DevForgeAI-like headers
- BR-002: User sections preserved verbatim (content hash unchanged)
- BR-003: Conflicts trigger user escalation (>30% difference)
"""

import difflib
from pathlib import Path
from typing import Protocol, Optional, List

from .markdown_parser import MarkdownParser
from ..models.conflict_detail import ConflictDetail
from ..config.merge_config import MergeConfig


class Logger(Protocol):
    """Logger protocol for dependency injection."""
    def log(self, message: str) -> None: ...


class MergeConflictDetectionService:
    """
    Service for detecting conflicts between user and framework content.

    CRITICAL REQUIREMENT: Use similarity threshold (70% = no conflict).
    30% difference triggers conflict (similarity < 70%).
    """

    def __init__(self, logger: Optional[Logger] = None):
        """
        Initialize conflict detection service.

        Args:
            logger: Optional logger following ILogger protocol. If provided, all conflict
                   detection results and calculations will be logged.
        """
        self.logger = logger
        self.parser = MarkdownParser()
        self._log = self.logger.log if logger else lambda msg: None

    def detect_conflicts(self, user_content: str, framework_content: str) -> dict:
        """
        Detect conflicts between user and framework content.

        Requirements:
        - SVC-010: Parse CLAUDE.md into sections
        - SVC-011: Identify framework vs user sections
        - SVC-012: Detect conflicts using similarity threshold

        Args:
            user_content: Existing CLAUDE.md content
            framework_content: DevForgeAI framework template content

        Returns:
            Dictionary with structure:
            {
                "has_conflicts": bool,
                "conflicts": List[ConflictDetail],
                "user_sections": List[Dict],
                "framework_sections": List[Dict]
            }
        """
        # Parse sections
        user_sections = self.parser.parse(user_content)
        framework_sections = self.parser.parse(framework_content)

        # Identify framework vs user sections
        conflicts = []

        for user_section in user_sections:
            section_name = user_section.get("title", "")
            is_framework = self._is_framework_section(section_name)

            if is_framework:
                # Find matching framework section
                matching_framework = None
                for fw_section in framework_sections:
                    if fw_section.get("title") == section_name:
                        matching_framework = fw_section
                        break

                if matching_framework:
                    # Check for conflict using similarity threshold
                    user_text = user_section.get("content", "")
                    fw_text = matching_framework.get("content", "")

                    similarity = self._calculate_similarity(user_text, fw_text)
                    threshold = MergeConfig.get_similarity_threshold()

                    if similarity < threshold:
                        # CONFLICT: User changed >30% of content
                        # Ensure line numbers are positive (1-indexed)
                        line_start = user_section.get("line_start", 1)
                        line_end = user_section.get("line_end", line_start + 1)
                        if line_start <= 0:
                            line_start = 1
                        if line_end <= line_start:
                            line_end = line_start + 1

                        conflict = ConflictDetail(
                            section_name=section_name,
                            line_start=line_start,
                            line_end=line_end,
                            user_excerpt=user_text,
                            framework_excerpt=fw_text,
                            similarity_ratio=similarity
                        )
                        conflicts.append(conflict)
                        self._log(
                            f"Conflict detected in '{section_name}': "
                            f"similarity {similarity:.1%} (threshold {threshold:.1%})"
                        )

        return {
            "has_conflicts": len(conflicts) > 0,
            "conflicts": conflicts,
            "user_sections": user_sections,
            "framework_sections": framework_sections
        }

    def _is_framework_section(self, section_name: str) -> bool:
        """
        Determine if section is framework section.

        Args:
            section_name: Header text of section

        Returns:
            True if section is framework section
        """
        return MergeConfig.is_framework_section(section_name)

    def _calculate_similarity(self, text1: str, text2: str) -> float:
        """
        Calculate similarity ratio between two texts (private method).

        Uses difflib.SequenceMatcher for similarity calculation.
        Returns 1.0 for identical, 0.0 for completely different.

        CRITICAL: This drives conflict detection logic.
        If similarity < 70% (threshold), conflict is triggered.

        Special cases:
        - Both empty → 1.0 (identical)
        - One empty, one not → 0.0 (completely different)
        - Otherwise → SequenceMatcher ratio (0.0-1.0)

        Args:
            text1: First text (user content)
            text2: Second text (framework content)

        Returns:
            Similarity ratio as float 0.0-1.0
        """
        if not text1 and not text2:
            return 1.0  # Both empty = identical

        if not text1 or not text2:
            return 0.0  # One empty, one not = completely different

        matcher = difflib.SequenceMatcher(None, text1, text2)
        return matcher.ratio()
