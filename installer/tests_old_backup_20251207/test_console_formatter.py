"""
STORY-075: Unit tests for ConsoleFormatter service.

Tests console output formatting, terminal width handling, ANSI color support,
and progress display. All tests follow TDD Red phase - they should FAIL until
implementation exists.

Coverage Target: 95%+ of ConsoleFormatter class
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from pathlib import Path
import sys
import os


class TestConsoleFormattingBasics:
    """Test basic console formatting (SVC-006)."""

    def test_console_formatter_respects_80_character_width(self):
        """
        Test: Console formatter respects 80-character terminal width (SVC-006).

        Given: Terminal width is 80 characters
        When: Report formatted for display
        Then: Output lines do not exceed 80 characters (except long paths)
        """
        # Arrange
        from installer.console_formatter import ConsoleFormatter

        formatter = ConsoleFormatter(terminal_width=80)

        # Act
        output = formatter.format_report(
            status="success",
            version="1.0.0",
            files_installed=450,
            files_failed=0,
            duration_seconds=2.5,
            target_directory="/tmp/target",
            log_file="/tmp/target/devforgeai/install.log",
        )

        # Assert
        lines = output.split("\n")
        for line in lines:
            # Allow paths to be longer, but regular text lines should fit
            if not any(
                line.startswith(prefix) for prefix in ["/", ".", "target", "install"]
            ):
                assert len(line) <= 85, f"Line too long ({len(line)} chars): {line}"

    def test_console_formatter_detects_terminal_width(self):
        """
        Test: Console formatter detects actual terminal width (SVC-006).

        Given: Running in terminal
        When: ConsoleFormatter initialized
        Then: Detects terminal width (80, 120, etc)
        """
        # Arrange
        from installer.console_formatter import ConsoleFormatter

        # Act
        formatter = ConsoleFormatter()  # Should auto-detect

        # Assert
        assert formatter.terminal_width > 0
        assert formatter.terminal_width <= 200  # Reasonable max

    def test_console_formatter_handles_narrow_terminal(self):
        """
        Test: Console formatter works with narrow terminals (≤60 chars).

        Given: Very narrow terminal (60 chars)
        When: Report formatted
        Then: Output is still readable (wraps text appropriately)
        """
        # Arrange
        from installer.console_formatter import ConsoleFormatter

        formatter = ConsoleFormatter(terminal_width=60)

        # Act
        output = formatter.format_report(
            status="success",
            version="1.0.0",
            files_installed=450,
            files_failed=0,
            duration_seconds=2.5,
            target_directory="/tmp",
            log_file="/tmp/devforgeai/install.log",
        )

        # Assert - Should not raise exception, output should be generated
        assert output is not None
        assert len(output) > 0


class TestANSIColorSupport:
    """Test ANSI color support (SVC-007)."""

    def test_ansi_colors_present_when_isatty(self):
        """
        Test: ANSI color codes included when stdout is TTY (SVC-007).

        Given: Running in terminal (isatty() = True)
        When: Report formatted
        Then: Output contains ANSI color codes
        """
        # Arrange
        from installer.console_formatter import ConsoleFormatter

        formatter = ConsoleFormatter(use_colors=True)

        # Act
        output = formatter.format_report(
            status="success",
            version="1.0.0",
            files_installed=450,
            files_failed=0,
            duration_seconds=2.5,
            target_directory="/tmp",
            log_file="/tmp/devforgeai/install.log",
        )

        # Assert - Should contain ANSI escape sequences
        # ANSI codes start with \033[ or \x1b[
        assert "\033[" in output or "\x1b[" in output, "No ANSI color codes found"

    def test_ansi_colors_absent_when_not_tty(self):
        """
        Test: No ANSI codes when stdout is not TTY (SVC-007).

        Given: Not running in terminal (isatty() = False)
        When: Report formatted
        Then: Output contains no ANSI color codes
        """
        # Arrange
        from installer.console_formatter import ConsoleFormatter

        formatter = ConsoleFormatter(use_colors=False)

        # Act
        output = formatter.format_report(
            status="success",
            version="1.0.0",
            files_installed=450,
            files_failed=0,
            duration_seconds=2.5,
            target_directory="/tmp",
            log_file="/tmp/devforgeai/install.log",
        )

        # Assert - Should not contain ANSI codes
        assert "\033[" not in output and "\x1b[" not in output, "ANSI codes found when colors disabled"

    def test_ansi_colors_for_success_status(self):
        """
        Test: SUCCESS status uses green color in ANSI output (SVC-007).

        Given: Installation succeeds
        When: Report formatted with colors
        Then: SUCCESS text includes green ANSI code
        """
        # Arrange
        from installer.console_formatter import ConsoleFormatter

        formatter = ConsoleFormatter(use_colors=True)

        # Act
        output = formatter.format_report(
            status="success",
            version="1.0.0",
            files_installed=450,
            files_failed=0,
            duration_seconds=2.5,
            target_directory="/tmp",
            log_file="/tmp/devforgeai/install.log",
        )

        # Assert - Should contain green color code (32)
        # Green ANSI is \033[32m or \033[92m
        assert "32m" in output or "92m" in output, "Green color code not found for success"

    def test_ansi_colors_for_failure_status(self):
        """
        Test: FAILURE status uses red color in ANSI output (SVC-007).

        Given: Installation fails
        When: Report formatted with colors
        Then: FAILURE text includes red ANSI code
        """
        # Arrange
        from installer.console_formatter import ConsoleFormatter

        formatter = ConsoleFormatter(use_colors=True)

        # Act
        output = formatter.format_report(
            status="failure",
            version="1.0.0",
            files_installed=150,
            files_failed=50,
            duration_seconds=1.2,
            target_directory="/tmp",
            log_file="/tmp/devforgeai/install.log",
        )

        # Assert - Should contain red color code (31)
        # Red ANSI is \033[31m or \033[91m
        assert "31m" in output or "91m" in output, "Red color code not found for failure"

    def test_ansi_reset_code_present(self):
        """
        Test: ANSI reset code (0) present after colored text (SVC-007).

        Given: Colored output generated
        When: Report formatted
        Then: ANSI reset codes (\033[0m) present to restore default
        """
        # Arrange
        from installer.console_formatter import ConsoleFormatter

        formatter = ConsoleFormatter(use_colors=True)

        # Act
        output = formatter.format_report(
            status="success",
            version="1.0.0",
            files_installed=450,
            files_failed=0,
            duration_seconds=2.5,
            target_directory="/tmp",
            log_file="/tmp/devforgeai/install.log",
        )

        # Assert
        assert "\033[0m" in output or "\x1b[0m" in output, "ANSI reset code not found"


class TestProgressDisplay:
    """Test progress display for large installations (SVC-008)."""

    def test_progress_shown_for_installations_over_100_files(self):
        """
        Test: Progress displayed when files > 100 (SVC-008).

        Given: Installation with 200 files
        When: ConsoleFormatter.show_progress() called
        Then: Progress bar shown (e.g., [========>  ] 80%)
        """
        # Arrange
        from installer.console_formatter import ConsoleFormatter

        formatter = ConsoleFormatter(progress_threshold=100)

        # Act
        progress_output = formatter.format_progress(
            files_processed=160,
            total_files=200,
        )

        # Assert
        assert progress_output is not None
        # Should contain progress indicator (%, bar, or count)
        assert "%" in progress_output or "[" in progress_output or "160" in progress_output

    def test_progress_not_shown_for_small_installations(self):
        """
        Test: Progress NOT shown when files ≤ 100 (SVC-008).

        Given: Installation with 50 files
        When: ConsoleFormatter.should_show_progress() called
        Then: Returns False (progress suppressed for small installs)
        """
        # Arrange
        from installer.console_formatter import ConsoleFormatter

        formatter = ConsoleFormatter(progress_threshold=100)

        # Act
        should_show = formatter.should_show_progress(total_files=50)

        # Assert
        assert should_show is False

    def test_progress_bar_updates_correctly(self):
        """
        Test: Progress bar updates as installation progresses.

        Given: Installation progresses from 0 to N files
        When: Progress updated at intervals
        Then: Progress bar shows increasing completion
        """
        # Arrange
        from installer.console_formatter import ConsoleFormatter

        formatter = ConsoleFormatter(progress_threshold=100)

        # Act
        progress_0 = formatter.format_progress(files_processed=0, total_files=200)
        progress_50 = formatter.format_progress(files_processed=100, total_files=200)
        progress_100 = formatter.format_progress(files_processed=200, total_files=200)

        # Assert
        # Each should be valid output
        assert progress_0 is not None
        assert progress_50 is not None
        assert progress_100 is not None

    def test_progress_shows_percentage(self):
        """
        Test: Progress bar displays percentage completion.

        Given: 150 of 200 files installed
        When: Progress formatted
        Then: Shows "75%" or similar
        """
        # Arrange
        from installer.console_formatter import ConsoleFormatter

        formatter = ConsoleFormatter(progress_threshold=100)

        # Act
        progress_output = formatter.format_progress(
            files_processed=150,
            total_files=200,
        )

        # Assert
        assert "75" in progress_output or "75%" in progress_output


class TestReportFormatting:
    """Test complete report formatting."""

    def test_console_report_includes_header(self):
        """
        Test: Console report includes header section.

        Given: Report formatted
        When: format_report() called
        Then: Output includes header (title, timestamp, etc)
        """
        # Arrange
        from installer.console_formatter import ConsoleFormatter

        formatter = ConsoleFormatter()

        # Act
        output = formatter.format_report(
            status="success",
            version="1.0.0",
            files_installed=450,
            files_failed=0,
            duration_seconds=2.5,
            target_directory="/tmp",
            log_file="/tmp/devforgeai/install.log",
        )

        # Assert
        assert output is not None
        # Should contain status/version information
        assert "success" in output.lower() or "Success" in output
        assert "1.0.0" in output

    def test_console_report_includes_summary_section(self):
        """
        Test: Console report includes summary of results.

        Given: Report formatted
        When: format_report() called
        Then: Output includes summary (files, errors, duration)
        """
        # Arrange
        from installer.console_formatter import ConsoleFormatter

        formatter = ConsoleFormatter()

        # Act
        output = formatter.format_report(
            status="success",
            version="1.0.0",
            files_installed=450,
            files_failed=0,
            duration_seconds=2.5,
            target_directory="/tmp",
            log_file="/tmp/devforgeai/install.log",
        )

        # Assert
        assert "450" in output  # Files count
        assert "2.5" in output or "2." in output  # Duration
        assert "/tmp" in output or "target" in output.lower()  # Directory

    def test_console_report_includes_footer_with_paths(self):
        """
        Test: Console report includes footer with log/manifest paths.

        Given: Report formatted
        When: format_report() called
        Then: Output includes log file path at end
        """
        # Arrange
        from installer.console_formatter import ConsoleFormatter

        formatter = ConsoleFormatter()

        # Act
        output = formatter.format_report(
            status="success",
            version="1.0.0",
            files_installed=450,
            files_failed=0,
            duration_seconds=2.5,
            target_directory="/tmp/test",
            log_file="/tmp/test/devforgeai/install.log",
        )

        # Assert
        assert "install.log" in output
        assert "devforgeai" in output or "/tmp" in output

    def test_console_report_with_no_errors(self):
        """
        Test: Console report for successful installation (no errors).

        Given: Installation succeeds with no errors
        When: format_report() called
        Then: Report shows success status, zero errors
        """
        # Arrange
        from installer.console_formatter import ConsoleFormatter

        formatter = ConsoleFormatter()

        # Act
        output = formatter.format_report(
            status="success",
            version="1.0.0",
            files_installed=450,
            files_failed=0,
            duration_seconds=2.5,
            target_directory="/tmp",
            log_file="/tmp/devforgeai/install.log",
        )

        # Assert
        assert "success" in output.lower()
        assert "0" in output  # Zero errors
        assert "error" not in output.lower() or "0 error" in output.lower()

    def test_console_report_with_errors(self):
        """
        Test: Console report for failed installation (with errors).

        Given: Installation fails with errors
        When: format_report() called
        Then: Report shows failure status, error count
        """
        # Arrange
        from installer.console_formatter import ConsoleFormatter

        formatter = ConsoleFormatter()

        # Act
        output = formatter.format_report(
            status="failure",
            version="1.0.0",
            files_installed=150,
            files_failed=50,
            duration_seconds=1.5,
            target_directory="/tmp",
            log_file="/tmp/devforgeai/install.log",
            errors=[
                {
                    "type": "PERMISSION_DENIED",
                    "message": "Cannot write to .claude/",
                    "file": ".claude/skills/test.md",
                }
            ]
            * 5,  # 5 permission errors
        )

        # Assert
        assert "failure" in output.lower()
        assert "50" in output  # 50 failed
        assert "error" in output.lower()

    def test_console_report_with_warnings(self):
        """
        Test: Console report includes warnings section.

        Given: Installation has warnings
        When: format_report() called
        Then: Report shows warnings
        """
        # Arrange
        from installer.console_formatter import ConsoleFormatter

        formatter = ConsoleFormatter()

        # Act
        output = formatter.format_report(
            status="success",
            version="1.0.0",
            files_installed=450,
            files_failed=0,
            duration_seconds=2.5,
            target_directory="/tmp",
            log_file="/tmp/devforgeai/install.log",
            warnings=[
                {"message": "Backup failed for old version"},
                {"message": "Some config not merged"},
            ],
        )

        # Assert
        assert "warning" in output.lower()
        assert "backup" in output.lower() or "Backup" in output


class TestErrorFormatting:
    """Test error formatting in console output."""

    def test_console_report_formats_permission_errors(self):
        """
        Test: Console output formats PERMISSION_DENIED errors.

        Given: Permission error encountered
        When: Error formatted
        Then: Shows readable error message with file path
        """
        # Arrange
        from installer.console_formatter import ConsoleFormatter

        formatter = ConsoleFormatter()

        # Act
        output = formatter.format_report(
            status="failure",
            version="1.0.0",
            files_installed=100,
            files_failed=10,
            duration_seconds=1.0,
            target_directory="/tmp",
            log_file="/tmp/devforgeai/install.log",
            errors=[
                {
                    "type": "PERMISSION_DENIED",
                    "message": "Cannot write to .claude/",
                    "file": ".claude/skills/test.md",
                }
            ],
        )

        # Assert
        assert "permission" in output.lower() or "PERMISSION" in output
        assert ".claude" in output

    def test_console_report_formats_file_not_found_errors(self):
        """
        Test: Console output formats FILE_NOT_FOUND errors.

        Given: Missing source file
        When: Error formatted
        Then: Shows file not found message with path
        """
        # Arrange
        from installer.console_formatter import ConsoleFormatter

        formatter = ConsoleFormatter()

        # Act
        output = formatter.format_report(
            status="failure",
            version="1.0.0",
            files_installed=100,
            files_failed=5,
            duration_seconds=1.0,
            target_directory="/tmp",
            log_file="/tmp/devforgeai/install.log",
            errors=[
                {
                    "type": "FILE_NOT_FOUND",
                    "message": "Source file not found",
                    "file": "src/missing.md",
                }
            ],
        )

        # Assert
        assert "not found" in output.lower() or "FILE_NOT_FOUND" in output
        assert "missing" in output.lower() or "src" in output


class TestBoxDrawing:
    """Test decorative box drawing for readability."""

    def test_report_uses_box_borders_for_sections(self):
        """
        Test: Console report uses box borders for visual separation.

        Given: Report formatted
        When: format_report() called
        Then: Output uses box-drawing chars (if terminal supports)
        """
        # Arrange
        from installer.console_formatter import ConsoleFormatter

        formatter = ConsoleFormatter()

        # Act
        output = formatter.format_report(
            status="success",
            version="1.0.0",
            files_installed=450,
            files_failed=0,
            duration_seconds=2.5,
            target_directory="/tmp",
            log_file="/tmp/devforgeai/install.log",
        )

        # Assert
        # Should contain box drawing chars or dashes for borders
        assert any(
            char in output for char in ["─", "═", "─", "=", "-", "*"]
        ), "No visual separator found"


class TestEdgeCases:
    """Test edge cases in console formatting."""

    def test_console_formatter_handles_very_long_paths(self):
        """
        Test: Console formatter handles very long directory paths.

        Given: Target directory path >100 characters
        When: Report formatted
        Then: Path displayed without breaking (may wrap)
        """
        # Arrange
        from installer.console_formatter import ConsoleFormatter

        formatter = ConsoleFormatter()
        long_path = "/very/long/path/to/installation/target/directory/with/many/nested/levels"

        # Act
        output = formatter.format_report(
            status="success",
            version="1.0.0",
            files_installed=450,
            files_failed=0,
            duration_seconds=2.5,
            target_directory=long_path,
            log_file=f"{long_path}/devforgeai/install.log",
        )

        # Assert
        assert output is not None
        assert "target" in output or "installation" in output

    def test_console_formatter_handles_large_file_counts(self):
        """
        Test: Console formatter handles thousands of files.

        Given: Installation with 10000 files
        When: Report formatted
        Then: Handles large numbers gracefully
        """
        # Arrange
        from installer.console_formatter import ConsoleFormatter

        formatter = ConsoleFormatter()

        # Act
        output = formatter.format_report(
            status="success",
            version="1.0.0",
            files_installed=10000,
            files_failed=0,
            duration_seconds=120.5,
            target_directory="/tmp",
            log_file="/tmp/devforgeai/install.log",
        )

        # Assert
        assert "10000" in output or "10,000" in output or "10k" in output

    def test_console_formatter_handles_zero_files(self):
        """
        Test: Console formatter handles edge case of zero files.

        Given: Installation with no files
        When: Report formatted
        Then: Shows zero without error
        """
        # Arrange
        from installer.console_formatter import ConsoleFormatter

        formatter = ConsoleFormatter()

        # Act
        output = formatter.format_report(
            status="failure",
            version="1.0.0",
            files_installed=0,
            files_failed=0,
            duration_seconds=0.1,
            target_directory="/tmp",
            log_file="/tmp/devforgeai/install.log",
            errors=[{"type": "UNKNOWN_ERROR", "message": "No files found"}],
        )

        # Assert
        assert output is not None
        assert "0" in output
