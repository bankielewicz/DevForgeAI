"""
STORY-074: Unit tests for InstallLogger.

Tests ISO 8601 timestamps, stack traces in log, append mode, and log rotation.
All tests follow TDD Red phase - they should FAIL until implementation exists.

Coverage Target: 95%+
"""

import pytest
from unittest.mock import Mock, patch
from pathlib import Path
import re
from datetime import datetime


class TestTimestampFormat:
    """Test ISO 8601 timestamp format in log entries (AC#5, LOG-001)."""

    def test_log_entries_have_iso_8601_timestamps(self, tmp_path):
        """
        Test: InstallLogger writes log entries with ISO 8601 timestamps (LOG-001).

        Given: InstallLogger logs an entry
        When: Entry is written to install.log
        Then: Timestamp matches ISO 8601 format (YYYY-MM-DDTHH:MM:SS.sss)
        """
        # Arrange
        from installer.services.install_logger import InstallLogger
        log_file = tmp_path / "install.log"
        logger = InstallLogger(log_file=log_file)

        # Act
        logger.log_info("Test message")

        # Assert
        log_content = log_file.read_text()
        # Regex for ISO 8601 with milliseconds: 2025-12-03T10:30:45.123
        iso_regex = r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{3}'
        assert re.search(iso_regex, log_content), "Log missing ISO 8601 timestamp"

    def test_timestamp_includes_milliseconds(self, tmp_path):
        """
        Test: InstallLogger timestamps include milliseconds.

        Given: InstallLogger logs an entry
        When: Entry is written
        Then: Timestamp has millisecond precision (.sss)
        """
        # Arrange
        from installer.services.install_logger import InstallLogger
        log_file = tmp_path / "install.log"
        logger = InstallLogger(log_file=log_file)

        # Act
        logger.log_info("Test message")

        # Assert
        log_content = log_file.read_text()
        # Check for milliseconds (3 digits after decimal)
        assert re.search(r'\.\d{3}', log_content), "Timestamp missing milliseconds"

    def test_timestamp_uses_utc_timezone(self, tmp_path):
        """
        Test: InstallLogger timestamps use UTC timezone.

        Given: InstallLogger logs an entry
        When: Entry is written
        Then: Timestamp ends with Z (UTC) or +00:00
        """
        # Arrange
        from installer.services.install_logger import InstallLogger
        log_file = tmp_path / "install.log"
        logger = InstallLogger(log_file=log_file)

        # Act
        logger.log_info("Test message")

        # Assert
        log_content = log_file.read_text()
        assert "Z" in log_content or "+00:00" in log_content


class TestStackTraces:
    """Test stack traces in log file (AC#5, LOG-003)."""

    def test_log_includes_stack_trace_on_error(self, tmp_path):
        """
        Test: InstallLogger includes full stack traces for errors (LOG-003).

        Given: An error occurs during installation
        When: InstallLogger logs the error
        Then: Log includes full stack trace with line numbers
        """
        # Arrange
        from installer.services.install_logger import InstallLogger
        log_file = tmp_path / "install.log"
        logger = InstallLogger(log_file=log_file)

        try:
            raise FileNotFoundError("Test error")
        except FileNotFoundError as e:
            # Act
            logger.log_error(e)

        # Assert
        log_content = log_file.read_text()
        assert "Traceback" in log_content
        assert "FileNotFoundError" in log_content
        assert "Test error" in log_content

    def test_log_includes_file_paths_and_line_numbers(self, tmp_path):
        """
        Test: InstallLogger stack traces include file paths and line numbers.

        Given: An error with stack trace is logged
        When: InstallLogger writes the error
        Then: Log includes file paths and line numbers (File "...", line X)
        """
        # Arrange
        from installer.services.install_logger import InstallLogger
        log_file = tmp_path / "install.log"
        logger = InstallLogger(log_file=log_file)

        try:
            raise ValueError("Test error with stack trace")
        except ValueError as e:
            # Act
            logger.log_error(e)

        # Assert
        log_content = log_file.read_text()
        assert re.search(r'File ".*", line \d+', log_content)


class TestAppendMode:
    """Test log file append mode (AC#5, LOG-002)."""

    def test_append_to_existing_log_file(self, tmp_path):
        """
        Test: InstallLogger appends to existing log file (LOG-002).

        Given: A log file exists from previous installation
        When: InstallLogger logs new entries
        Then: Existing entries are preserved, new entries appended
        """
        # Arrange
        from installer.services.install_logger import InstallLogger
        log_file = tmp_path / "install.log"
        log_file.write_text("2025-12-01T10:00:00.000Z [INFO] Previous install\n")

        logger = InstallLogger(log_file=log_file)

        # Act
        logger.log_info("New install")

        # Assert
        log_content = log_file.read_text()
        assert "Previous install" in log_content
        assert "New install" in log_content

    def test_second_install_preserves_first_install_logs(self, tmp_path):
        """
        Test: Second installation preserves first installation's logs (LOG-002).

        Given: First installation writes log entries
        When: Second installation starts logging
        Then: First installation's logs remain in file
        """
        # Arrange
        from installer.services.install_logger import InstallLogger
        log_file = tmp_path / "install.log"

        # First installation
        logger1 = InstallLogger(log_file=log_file)
        logger1.log_info("First install message")

        # Second installation
        logger2 = InstallLogger(log_file=log_file)

        # Act
        logger2.log_info("Second install message")

        # Assert
        log_content = log_file.read_text()
        lines = log_content.split('\n')
        assert any("First install" in line for line in lines)
        assert any("Second install" in line for line in lines)

    def test_log_separates_installation_sessions(self, tmp_path):
        """
        Test: InstallLogger separates installation sessions with separator.

        Given: A new installation starts with existing log
        When: InstallLogger initializes
        Then: Session separator added (e.g., "=== Installation Started ===")
        """
        # Arrange
        from installer.services.install_logger import InstallLogger
        log_file = tmp_path / "install.log"
        log_file.write_text("Previous log content\n")

        # Act
        logger = InstallLogger(log_file=log_file)
        logger.log_session_start()

        # Assert
        log_content = log_file.read_text()
        assert "===" in log_content or "Installation" in log_content


class TestLogContent:
    """Test log content includes required information (AC#5)."""

    def test_log_includes_error_category_and_exit_code(self, tmp_path):
        """
        Test: InstallLogger includes error category and exit code.

        Given: An error with category is logged
        When: InstallLogger writes error entry
        Then: Log includes error category and exit code
        """
        # Arrange
        from installer.services.install_logger import InstallLogger
        log_file = tmp_path / "install.log"
        logger = InstallLogger(log_file=log_file)

        # Act
        logger.log_error(
            error=FileNotFoundError("Missing source"),
            category="MISSING_SOURCE",
            exit_code=1
        )

        # Assert
        log_content = log_file.read_text()
        assert "MISSING_SOURCE" in log_content
        assert "exit code 1" in log_content or "exit_code: 1" in log_content

    def test_log_includes_file_paths_involved(self, tmp_path):
        """
        Test: InstallLogger includes file paths involved in operation (AC#5).

        Given: File operation is logged
        When: InstallLogger writes entry
        Then: Log includes source and target file paths
        """
        # Arrange
        from installer.services.install_logger import InstallLogger
        log_file = tmp_path / "install.log"
        logger = InstallLogger(log_file=log_file)

        # Act
        logger.log_file_operation(
            operation="copy",
            source_path="/source/.claude/commands/dev.md",
            target_path="/target/.claude/commands/dev.md"
        )

        # Assert
        log_content = log_file.read_text()
        assert "/source/.claude/commands/dev.md" in log_content
        assert "/target/.claude/commands/dev.md" in log_content

    def test_log_includes_system_context(self, tmp_path):
        """
        Test: InstallLogger includes system context (OS, shell version) (AC#5).

        Given: InstallLogger initializes
        When: First log entry is written
        Then: Log includes OS and shell version
        """
        # Arrange
        from installer.services.install_logger import InstallLogger
        log_file = tmp_path / "install.log"

        # Act
        logger = InstallLogger(log_file=log_file)
        logger.log_system_context()

        # Assert
        log_content = log_file.read_text()
        # Should include OS info (Linux, Darwin, Windows)
        assert any(os_name in log_content for os_name in ["Linux", "Darwin", "Windows", "OS:"])

    def test_log_includes_rollback_actions_taken(self, tmp_path):
        """
        Test: InstallLogger includes rollback actions when rollback occurs (AC#5).

        Given: Rollback is performed
        When: InstallLogger logs rollback
        Then: Log includes actions taken (files restored, files removed)
        """
        # Arrange
        from installer.services.install_logger import InstallLogger
        log_file = tmp_path / "install.log"
        logger = InstallLogger(log_file=log_file)

        # Act
        logger.log_rollback(
            files_restored=["file1.txt", "file2.txt"],
            files_removed=["partial.txt"]
        )

        # Assert
        log_content = log_file.read_text()
        assert "rollback" in log_content.lower()
        assert "file1.txt" in log_content
        assert "file2.txt" in log_content
        assert "partial.txt" in log_content


class TestLogRotation:
    """Test log file rotation at 10MB (LOG-004)."""

    def test_log_rotates_when_exceeding_10mb(self, tmp_path):
        """
        Test: InstallLogger rotates log file when exceeding 10MB (LOG-004).

        Given: Log file exceeds 10MB
        When: InstallLogger writes new entry
        Then: Log is rotated, old log renamed to install.log.1
        """
        # Arrange
        from installer.services.install_logger import InstallLogger
        log_file = tmp_path / "install.log"

        # Create 10MB+ log file
        large_content = "x" * (10 * 1024 * 1024 + 1000)  # 10MB + 1KB
        log_file.write_text(large_content)

        logger = InstallLogger(log_file=log_file, max_size_mb=10)

        # Act
        logger.log_info("New entry after rotation")

        # Assert
        rotated_log = tmp_path / "install.log.1"
        assert rotated_log.exists()
        assert rotated_log.stat().st_size > 10 * 1024 * 1024

    def test_log_keeps_3_rotations(self, tmp_path):
        """
        Test: InstallLogger keeps 3 rotations (LOG-004).

        Given: Multiple log rotations occur
        When: 4th rotation happens
        Then: Oldest rotation (install.log.3) is deleted, keeps install.log.1, .2, .3
        """
        # Arrange
        from installer.services.install_logger import InstallLogger
        log_file = tmp_path / "install.log"

        # Create existing rotations
        (tmp_path / "install.log.1").write_text("rotation 1")
        (tmp_path / "install.log.2").write_text("rotation 2")
        (tmp_path / "install.log.3").write_text("rotation 3")

        # Create large log to trigger rotation
        log_file.write_text("x" * (10 * 1024 * 1024 + 1000))

        logger = InstallLogger(log_file=log_file, max_size_mb=10, max_rotations=3)

        # Act
        logger.log_info("Trigger rotation")

        # Assert
        assert (tmp_path / "install.log.1").exists()
        assert (tmp_path / "install.log.2").exists()
        assert (tmp_path / "install.log.3").exists()
        # 4th rotation should not exist (oldest deleted)


class TestLogLevels:
    """Test different log levels (INFO, WARNING, ERROR)."""

    def test_log_info_level(self, tmp_path):
        """
        Test: InstallLogger logs INFO level messages.

        Given: InstallLogger is initialized
        When: log_info() is called
        Then: Log entry has [INFO] prefix
        """
        # Arrange
        from installer.services.install_logger import InstallLogger
        log_file = tmp_path / "install.log"
        logger = InstallLogger(log_file=log_file)

        # Act
        logger.log_info("Info message")

        # Assert
        log_content = log_file.read_text()
        assert "[INFO]" in log_content or "INFO:" in log_content

    def test_log_warning_level(self, tmp_path):
        """
        Test: InstallLogger logs WARNING level messages.

        Given: InstallLogger is initialized
        When: log_warning() is called
        Then: Log entry has [WARNING] prefix
        """
        # Arrange
        from installer.services.install_logger import InstallLogger
        log_file = tmp_path / "install.log"
        logger = InstallLogger(log_file=log_file)

        # Act
        logger.log_warning("Warning message")

        # Assert
        log_content = log_file.read_text()
        assert "[WARNING]" in log_content or "WARNING:" in log_content

    def test_log_error_level(self, tmp_path):
        """
        Test: InstallLogger logs ERROR level messages.

        Given: InstallLogger is initialized
        When: log_error() is called
        Then: Log entry has [ERROR] prefix
        """
        # Arrange
        from installer.services.install_logger import InstallLogger
        log_file = tmp_path / "install.log"
        logger = InstallLogger(log_file=log_file)

        # Act
        logger.log_error(Exception("Error message"))

        # Assert
        log_content = log_file.read_text()
        assert "[ERROR]" in log_content or "ERROR:" in log_content


class TestLogFilePermissions:
    """Test log file permissions (NFR-006)."""

    def test_log_file_created_with_0600_permissions(self, tmp_path):
        """
        Test: InstallLogger creates log file with 0600 permissions (owner read/write only).

        Given: InstallLogger creates new log file
        When: File is created
        Then: Permissions are 0600 (owner read/write only)
        """
        # Arrange
        from installer.services.install_logger import InstallLogger
        log_file = tmp_path / "install.log"

        # Act
        logger = InstallLogger(log_file=log_file)
        logger.log_info("Test message")

        # Assert
        import stat
        file_mode = log_file.stat().st_mode
        permissions = stat.filemode(file_mode)
        # Should be -rw------- (0600)
        assert permissions == "-rw-------" or (file_mode & 0o777) == 0o600


class TestLogEdgeCases:
    """Test log edge case scenarios."""

    def test_log_handles_unicode_characters(self, tmp_path):
        """
        Test: InstallLogger handles unicode characters in messages.

        Given: Log message contains unicode characters
        When: InstallLogger writes entry
        Then: Unicode characters preserved in log
        """
        # Arrange
        from installer.services.install_logger import InstallLogger
        log_file = tmp_path / "install.log"
        logger = InstallLogger(log_file=log_file)

        # Act
        logger.log_info("Test with unicode: 你好世界 🎉")

        # Assert
        log_content = log_file.read_text(encoding="utf-8")
        assert "你好世界" in log_content
        assert "🎉" in log_content

    def test_log_handles_multiline_messages(self, tmp_path):
        """
        Test: InstallLogger handles multiline messages correctly.

        Given: Log message contains newlines
        When: InstallLogger writes entry
        Then: Multiline message is properly formatted
        """
        # Arrange
        from installer.services.install_logger import InstallLogger
        log_file = tmp_path / "install.log"
        logger = InstallLogger(log_file=log_file)

        # Act
        logger.log_info("Line 1\nLine 2\nLine 3")

        # Assert
        log_content = log_file.read_text()
        assert "Line 1" in log_content
        assert "Line 2" in log_content
        assert "Line 3" in log_content

    def test_log_handles_very_long_messages(self, tmp_path):
        """
        Test: InstallLogger handles very long messages (>10KB).

        Given: Log message is very long (10KB+)
        When: InstallLogger writes entry
        Then: Full message is written without truncation
        """
        # Arrange
        from installer.services.install_logger import InstallLogger
        log_file = tmp_path / "install.log"
        logger = InstallLogger(log_file=log_file)

        long_message = "x" * (10 * 1024)  # 10KB

        # Act
        logger.log_info(long_message)

        # Assert
        log_content = log_file.read_text()
        assert len(log_content) >= 10 * 1024

    def test_log_handles_log_file_deletion_during_operation(self, tmp_path):
        """
        Test: InstallLogger handles log file deletion during operation.

        Given: Log file is deleted while logger is active
        When: InstallLogger attempts to write
        Then: Recreates log file and continues logging
        """
        # Arrange
        from installer.services.install_logger import InstallLogger
        log_file = tmp_path / "install.log"
        logger = InstallLogger(log_file=log_file)

        logger.log_info("Before deletion")

        # Act
        log_file.unlink()  # Delete log file
        logger.log_info("After deletion")

        # Assert
        assert log_file.exists()
        log_content = log_file.read_text()
        assert "After deletion" in log_content
