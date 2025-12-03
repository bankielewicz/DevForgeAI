"""
Summary Formatter Service - STORY-073

Handles formatting of detection results into human-readable summaries.

Requirements:
- SVC-020: Format DetectionResult into human-readable summary
- SVC-021: Apply color coding for terminal output
- SVC-022: Paginate conflict lists (show first 10)

Business Rules:
- BR-002: Summary displays before any user prompts
- NFR-008: Summary uses color coding when supported
"""

import logging
import sys
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from .auto_detection_service import DetectionResult

logger = logging.getLogger(__name__)


class SummaryFormatterService:
    """
    Service for formatting DetectionResult into human-readable summaries.

    Lifecycle: Singleton
    Dependencies: typing, datetime
    """

    # ANSI color codes
    COLOR_RESET = "\033[0m"
    COLOR_GREEN = "\033[92m"
    COLOR_YELLOW = "\033[93m"
    COLOR_RED = "\033[91m"
    COLOR_CYAN = "\033[96m"
    COLOR_BOLD = "\033[1m"

    # Pagination limit
    CONFLICT_PAGINATION_LIMIT = 10

    def __init__(self, use_colors: Optional[bool] = None, source_version: Optional[str] = None):
        """
        Initialize summary formatter service.

        Args:
            use_colors: Force color usage (True/False), or auto-detect if None
            source_version: Version being installed (for upgrade recommendations)
        """
        if use_colors is None:
            self.use_colors = self._supports_color()
        else:
            self.use_colors = use_colors
        self.source_version = source_version

    def format_summary(self, detection_result: 'DetectionResult') -> str:
        """
        Format DetectionResult into human-readable summary with 4 sections.

        Args:
            detection_result: Complete detection results

        Returns:
            Multi-line string with formatted summary

        Test Requirements:
            - Contains 4 sections: Installation Status, Project Context, Conflicts, Recommendations
            - Shows "Clean install" when version_info is None
            - Shows existing version when version_info present
            - Shows git root path when git_info present
            - Shows "No git repository" when git_info is None
            - Shows conflict counts by category
            - Paginates conflicts (first 10 only)
            - Applies ANSI colors when supported
        """
        sections = []

        # Section 1: Installation Status
        sections.append(self._format_installation_status(detection_result))

        # Section 2: Project Context
        sections.append(self._format_project_context(detection_result))

        # Section 3: Conflicts
        sections.append(self._format_conflicts(detection_result))

        # Section 4: Recommendations
        sections.append(self._format_recommendations(detection_result))

        # Join sections with blank lines
        return "\n\n".join(sections)

    def _colorize(self, text: str, color_code: str) -> str:
        """
        Apply color to text if colors are enabled.

        Args:
            text: Text to colorize
            color_code: ANSI color code (e.g., COLOR_GREEN)

        Returns:
            Colored text if colors enabled, otherwise plain text
        """
        if self.use_colors:
            return f"{color_code}{text}{self.COLOR_RESET}"
        return text

    def _add_section_header(self, header: str) -> list:
        """
        Add formatted section header with optional colors.

        Args:
            header: Section title text

        Returns:
            List with formatted header lines
        """
        lines = []
        lines.append(self._colorize(header, f"{self.COLOR_BOLD}{self.COLOR_CYAN}"))
        lines.append("-" * len(header))
        return lines

    def _format_installation_status(self, detection_result: 'DetectionResult') -> str:
        """Format Installation Status section."""
        lines = self._add_section_header("Installation Status")

        # Version information
        if detection_result.version_info is None:
            lines.append("Status: Clean install (no existing installation detected)")
        else:
            version = detection_result.version_info.installed_version
            installed_at = detection_result.version_info.installed_at
            source = detection_result.version_info.installation_source

            colored_version = self._colorize(f"v{version}", self.COLOR_GREEN)
            lines.append(f"Found existing DevForgeAI installation: {colored_version}")
            lines.append(f"Installed: {installed_at}")
            lines.append(f"Source: {source}")

        return "\n".join(lines)

    def _format_project_context(self, detection_result: 'DetectionResult') -> str:
        """Format Project Context section."""
        lines = self._add_section_header("Project Context")

        # Git repository information
        if detection_result.git_info is None or detection_result.git_info.repository_root is None:
            lines.append("Git: No git repository detected")
        else:
            git_root = detection_result.git_info.repository_root
            colored_path = self._colorize(git_root, self.COLOR_GREEN)
            lines.append(f"Git repository detected: {colored_path}")

            if detection_result.git_info.is_submodule:
                lines.append("  (Submodule detected)")

        # CLAUDE.md information
        if detection_result.claudemd_info and detection_result.claudemd_info.exists:
            size = detection_result.claudemd_info.size
            needs_backup = detection_result.claudemd_info.needs_backup

            lines.append(f"CLAUDE.md: Found ({size} bytes)")

            if needs_backup:
                backup_msg = self._colorize("Backup recommended", self.COLOR_YELLOW)
                lines.append(f"  {backup_msg}")

        return "\n".join(lines)

    def _format_conflicts(self, detection_result: 'DetectionResult') -> str:
        """Format Conflicts section."""
        lines = self._add_section_header("File Conflicts")

        conflicts = detection_result.conflicts
        total_conflicts = len(conflicts.conflicts)

        if total_conflicts == 0:
            lines.append("No file conflicts detected")
        else:
            # Summary counts
            framework_count = conflicts.framework_count
            user_count = conflicts.user_count

            conflict_count = self._colorize(f"{total_conflicts} files", self.COLOR_RED)
            lines.append(f"Conflicts detected: {conflict_count}")
            lines.append(f"  Framework files: {framework_count}")
            lines.append(f"  User files: {user_count}")

            # Paginated conflict list (SVC-022)
            lines.append("")
            lines.append("Conflicting files:")

            conflicts_to_show = conflicts.conflicts[:self.CONFLICT_PAGINATION_LIMIT]
            for conflict in conflicts_to_show:
                lines.append(f"  - {conflict}")

            # Show pagination message
            remaining = total_conflicts - self.CONFLICT_PAGINATION_LIMIT
            if remaining > 0:
                pagination_msg = self._colorize(f"...and {remaining} more", self.COLOR_YELLOW)
                lines.append(f"  {pagination_msg}")

        return "\n".join(lines)

    def _format_recommendations(self, detection_result: 'DetectionResult') -> str:
        """Format Recommendations section."""
        lines = self._add_section_header("Recommendations")

        # Determine recommendation based on detection results
        if detection_result.version_info is None:
            lines.append("Action: Fresh installation")
            lines.append("  - No existing installation detected")
            lines.append("  - Safe to proceed with installation")
        else:
            # Version comparison message would go here
            # (For now, just show that we detected existing version)
            lines.append("Action: Upgrade/Reinstall")
            lines.append("  - Existing installation detected")
            lines.append("  - Review conflicts before proceeding")

        # Conflict-based recommendations
        total_conflicts = len(detection_result.conflicts.conflicts)
        if total_conflicts > 0:
            warning_label = self._colorize("Warning:", self.COLOR_YELLOW)
            lines.append(f"\n{warning_label} File conflicts detected")
            lines.append("  - Backup recommended before installation")
            lines.append("  - Review conflicting files to avoid data loss")

        return "\n".join(lines)

    def _supports_color(self) -> bool:
        """
        Check if terminal supports ANSI color codes.

        Returns:
            True if colors are supported, False otherwise

        Detection strategy:
            - Check if stdout is a TTY
            - Check TERM environment variable
            - Check if running on Windows without ANSI support
        """
        # Check if stdout is a TTY
        if not hasattr(sys.stdout, 'isatty') or not sys.stdout.isatty():
            return False

        # Check TERM environment variable
        import os
        term = os.environ.get('TERM', '')
        if term == 'dumb':
            return False

        # Assume color support for TTY terminals
        return True
