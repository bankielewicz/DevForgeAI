"""
Console Formatter Service (STORY-075).

Handles:
- Terminal width detection and respect (SVC-006)
- ANSI color support detection (SVC-007)
- Progress display for large installations (SVC-008)
- Box drawing for visual formatting
"""

import sys
import shutil
from typing import Optional, List, Dict, Any


class ConsoleFormatter:
    """
    Service for formatting console output.

    Singleton lifecycle: One instance per installation session.
    Responsibilities:
    - Format console reports within terminal width
    - Apply ANSI color codes when appropriate
    - Display progress for large installations
    - Use box-drawing characters for visual separation
    """

    def __init__(
        self,
        terminal_width: Optional[int] = None,
        use_colors: Optional[bool] = None,
        progress_threshold: int = 100,
    ):
        """
        Initialize console formatter.

        Args:
            terminal_width: Override terminal width (auto-detect if None)
            use_colors: Override color detection (auto-detect if None)
            progress_threshold: Show progress for installations with > this many files
        """
        # Detect terminal width
        if terminal_width is None:
            self.terminal_width = shutil.get_terminal_size((80, 24)).columns
        else:
            self.terminal_width = terminal_width

        # Detect color support
        if use_colors is None:
            # Only use colors if stdout is a TTY
            self.use_colors = sys.stdout.isatty()
        else:
            self.use_colors = use_colors

        self.progress_threshold = progress_threshold

        # ANSI color codes
        self.COLOR_GREEN = "\033[32m" if self.use_colors else ""
        self.COLOR_RED = "\033[31m" if self.use_colors else ""
        self.COLOR_YELLOW = "\033[33m" if self.use_colors else ""
        self.COLOR_RESET = "\033[0m" if self.use_colors else ""

    def format_report(
        self,
        status: str,
        version: str,
        files_installed: int,
        files_failed: int,
        duration_seconds: float,
        target_directory: str,
        log_file: str,
        errors: Optional[List[Dict[str, Any]]] = None,
        warnings: Optional[List[Dict[str, Any]]] = None,
    ) -> str:
        """
        Format a complete installation report for console display.

        Args:
            status: Installation status (success or failure)
            version: Version installed
            files_installed: Count of successful files
            files_failed: Count of failed files
            duration_seconds: Installation duration
            target_directory: Installation target path
            log_file: Path to log file
            errors: Optional list of error objects
            warnings: Optional list of warning objects

        Returns:
            Formatted report string respecting terminal width
        """
        lines = []
        separator = "─" * min(70, self.terminal_width - 2)

        # Build report sections
        lines.extend(self._format_header(separator, status))
        lines.extend(self._format_summary(version, files_installed, files_failed,
                                          duration_seconds))
        lines.extend(self._format_errors(errors))
        lines.extend(self._format_warnings(warnings))
        lines.extend(self._format_paths(target_directory, log_file))
        lines.append(f"{separator}")

        return "\n".join(lines)

    def _format_header(self, separator: str, status: str) -> List[str]:
        """Format report header with status."""
        status_upper = status.upper()
        status_colored = self._colorize_status(status_upper)
        return [
            f"{separator}",
            f"Installation Report - Status: {status_colored}",
            f"{separator}",
            "",
        ]

    def _colorize_status(self, status: str) -> str:
        """Apply color to status based on success/failure."""
        if status == "SUCCESS":
            return f"{self.COLOR_GREEN}{status}{self.COLOR_RESET}"
        return f"{self.COLOR_RED}{status}{self.COLOR_RESET}"

    def _format_summary(
        self,
        version: str,
        files_installed: int,
        files_failed: int,
        duration_seconds: float,
    ) -> List[str]:
        """Format summary section."""
        total_files = files_installed + files_failed
        return [
            "Summary:",
            f"  Version:          {version}",
            f"  Files Processed:  {total_files}",
            f"    ✓ Successful:   {files_installed}",
            f"    ✗ Failed:       {files_failed}",
            f"  Duration:         {duration_seconds:.3f} seconds",
            "",
        ]

    def _format_errors(self, errors: Optional[List[Dict[str, Any]]]) -> List[str]:
        """Format errors section if present."""
        if not errors:
            return []

        lines = ["Errors:"]
        for error in errors[:5]:  # Show first 5 errors
            lines.append(self._format_error_line(error))

        if len(errors) > 5:
            lines.append(f"  ... and {len(errors) - 5} more errors")
        lines.append("")

        return lines

    def _format_error_line(self, error: Dict[str, Any]) -> str:
        """Format single error line."""
        error_type = error.get("type", "UNKNOWN")
        error_msg = error.get("message", "")
        file_path = error.get("file", "")

        if file_path:
            return f"  [{error_type}] {file_path}: {error_msg}"
        return f"  [{error_type}] {error_msg}"

    def _format_warnings(self, warnings: Optional[List[Dict[str, Any]]]) -> List[str]:
        """Format warnings section if present."""
        if not warnings:
            return []

        lines = ["Warnings:"]
        for warning in warnings[:3]:  # Show first 3 warnings
            warning_msg = warning.get("message", "")
            lines.append(f"  ⚠ {warning_msg}")
        lines.append("")

        return lines

    def _format_paths(self, target_directory: str, log_file: str) -> List[str]:
        """Format paths section."""
        return [
            "Paths:",
            f"  Target Directory: {target_directory}",
            f"  Log File:         {log_file}",
            "",
        ]

    def format_progress(self, files_processed: int, total_files: int) -> str:
        """
        Format progress bar for installation (SVC-008).

        Args:
            files_processed: Number of files processed so far
            total_files: Total number of files

        Returns:
            Progress bar string with percentage
        """
        if total_files == 0:
            percentage = 0
        else:
            percentage = int((files_processed / total_files) * 100)

        # Create progress bar
        bar_width = 20
        filled = int((files_processed / total_files) * bar_width) if total_files > 0 else 0
        empty = bar_width - filled

        progress_bar = "[" + "=" * filled + ">" + " " * (empty - 1) + "]"

        return f"{progress_bar} {percentage}% ({files_processed}/{total_files})"

    def should_show_progress(self, total_files: int) -> bool:
        """
        Determine if progress should be shown (SVC-008).

        Args:
            total_files: Total number of files being installed

        Returns:
            True if total_files > progress_threshold
        """
        return total_files > self.progress_threshold

    def _wrap_text(self, text: str, width: Optional[int] = None) -> str:
        """
        Wrap text to fit within terminal width.

        Args:
            text: Text to wrap
            width: Width to wrap to (defaults to terminal_width - 2)

        Returns:
            Wrapped text
        """
        if width is None:
            width = self.terminal_width - 2

        lines = []
        for line in text.split("\n"):
            if len(line) <= width:
                lines.append(line)
            else:
                lines.extend(self._wrap_long_line(line, width))

        return "\n".join(lines)

    def _wrap_long_line(self, line: str, width: int) -> List[str]:
        """
        Wrap a single long line to fit within width.

        Args:
            line: Line to wrap
            width: Maximum width

        Returns:
            List of wrapped lines
        """
        wrapped = []
        current_line = ""

        for word in line.split(" "):
            # Check if adding word to current line would exceed width
            test_line = f"{current_line} {word}".lstrip()
            if len(test_line) <= width:
                current_line = test_line
            else:
                # Word doesn't fit, save current line and start new one
                if current_line:
                    wrapped.append(current_line)
                current_line = word

        if current_line:
            wrapped.append(current_line)

        return wrapped
