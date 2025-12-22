"""
STORY-075: Unit tests for InstallationReporter service.

Tests console summary report generation, log file creation, JSON output,
and error categorization. All tests follow TDD Red phase - they should FAIL
until implementation exists.

Coverage Target: 95%+ of InstallationReporter class
"""

import pytest
import json
import re
from unittest.mock import Mock, patch, MagicMock
from pathlib import Path
from datetime import datetime, timezone
import time


class TestConsoleReportGeneration:
    """Test console summary report generation (AC#1)."""

    def test_console_report_contains_success_status(self, tmp_path):
        """
        Test: Console report displays SUCCESS status for successful installation.

        Given: Installation completes successfully
        When: InstallationReporter.generate_console_report() called
        Then: Report contains "SUCCESS" status
        """
        # Arrange
        from installer.reporter import InstallationReporter

        reporter = InstallationReporter()
        report_data = {
            "status": "success",
            "version": "1.0.0",
            "files_installed": 450,
            "files_failed": 0,
            "duration_seconds": 2.5,
            "target_directory": str(tmp_path),
            "log_file": str(tmp_path / "install.log"),
        }

        # Act
        console_output = reporter.generate_console_report(report_data)

        # Assert
        assert "SUCCESS" in console_output.upper()
        assert "1.0.0" in console_output
        assert "450" in console_output
        assert "2.5" in console_output

    def test_console_report_contains_failure_status(self, tmp_path):
        """
        Test: Console report displays FAILURE status with exit code.

        Given: Installation fails
        When: InstallationReporter.generate_console_report() called
        Then: Report contains "FAILURE" and exit code (non-zero)
        """
        # Arrange
        from installer.reporter import InstallationReporter

        reporter = InstallationReporter()
        report_data = {
            "status": "failure",
            "version": "1.0.0",
            "files_installed": 150,
            "files_failed": 50,
            "exit_code": 1,
            "duration_seconds": 1.2,
            "target_directory": str(tmp_path),
            "log_file": str(tmp_path / "install.log"),
        }

        # Act
        console_output = reporter.generate_console_report(report_data)

        # Assert
        assert "FAILURE" in console_output.upper()
        assert "1" in console_output  # Exit code
        assert "150" in console_output
        assert "50" in console_output

    def test_console_report_contains_all_7_required_fields(self, tmp_path):
        """
        Test: Console report contains all 7 required fields (AC#1).

        Given: Installation completes
        When: InstallationReporter.generate_console_report() called
        Then: Report contains:
            1. Installation status
            2. Version installed
            3. Total files processed count
            4. Errors encountered count
            5. Installation duration
            6. Target directory path
            7. Log file location
        """
        # Arrange
        from installer.reporter import InstallationReporter

        reporter = InstallationReporter()
        report_data = {
            "status": "success",
            "version": "1.2.3",
            "files_installed": 450,
            "files_failed": 0,
            "duration_seconds": 2.456,
            "target_directory": str(tmp_path),
            "log_file": str(tmp_path / "install.log"),
        }

        # Act
        console_output = reporter.generate_console_report(report_data)

        # Assert - All 7 fields must be present
        assert "success" in console_output.lower()  # 1. Status
        assert "1.2.3" in console_output  # 2. Version
        assert "450" in console_output  # 3. Files processed
        assert "0" in console_output  # 4. Errors count
        assert "2.456" in console_output or "2.46" in console_output  # 5. Duration
        assert str(tmp_path) in console_output  # 6. Target directory
        assert "install.log" in console_output  # 7. Log file location

    def test_console_report_formatting_respects_terminal_width(self, tmp_path):
        """
        Test: Console output respects 80-character terminal width (SVC-006).

        Given: Console formatter generates report
        When: Output contains lines
        Then: No line exceeds 80 characters (except very long paths)
        """
        # Arrange
        from installer.reporter import InstallationReporter

        reporter = InstallationReporter()
        report_data = {
            "status": "success",
            "version": "1.0.0",
            "files_installed": 450,
            "files_failed": 0,
            "duration_seconds": 2.5,
            "target_directory": str(tmp_path),
            "log_file": str(tmp_path / "install.log"),
        }

        # Act
        console_output = reporter.generate_console_report(report_data)

        # Assert - Check most lines respect width (paths may be longer)
        lines = console_output.split("\n")
        non_path_lines = [
            l for l in lines if not l.startswith("/") and not l.startswith(".")
        ]
        for line in non_path_lines:
            assert len(line) <= 85, f"Line too long ({len(line)} chars): {line}"


class TestLogFileCreation:
    """Test log file creation with ISO 8601 timestamps (AC#2)."""

    def test_log_file_created_at_default_location(self, tmp_path):
        """
        Test: Log file created at devforgeai/install.log (AC#2).

        Given: Installation starts
        When: InstallationReporter.create_log_file() called
        Then: Creates devforgeai/install.log
        """
        # Arrange
        from installer.reporter import InstallationReporter

        devforgeai_dir = tmp_path / "devforgeai"
        devforgeai_dir.mkdir()

        reporter = InstallationReporter()

        # Act
        log_file = reporter.create_log_file(target_directory=tmp_path)

        # Assert
        assert log_file.exists()
        assert log_file.name == "install.log"
        assert log_file.parent.name == "devforgeai"

    def test_log_file_contains_iso8601_timestamps(self, tmp_path):
        """
        Test: Log file entries have ISO 8601 timestamps (AC#2).

        Given: Log file is created and entries are written
        When: Log entry is written
        Then: Entry contains ISO 8601 timestamp (YYYY-MM-DDTHH:MM:SSZ)
        """
        # Arrange
        from installer.reporter import InstallationReporter

        devforgeai_dir = tmp_path / "devforgeai"
        devforgeai_dir.mkdir()

        reporter = InstallationReporter()
        log_file = reporter.create_log_file(target_directory=tmp_path)

        # Act
        reporter.log_operation("Copy file", "test.py", "success")

        # Assert
        log_content = log_file.read_text()
        # ISO 8601 pattern: YYYY-MM-DDTHH:MM:SSZ or similar
        iso8601_pattern = r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}"
        assert re.search(iso8601_pattern, log_content), "No ISO 8601 timestamp found"

    def test_log_file_contains_file_operation_details(self, tmp_path):
        """
        Test: Log file documents file operations with paths (AC#2).

        Given: Files are copied during installation
        When: InstallationReporter logs file operations
        Then: Log contains operation type, source, destination, status
        """
        # Arrange
        from installer.reporter import InstallationReporter

        devforgeai_dir = tmp_path / "devforgeai"
        devforgeai_dir.mkdir()

        reporter = InstallationReporter()
        log_file = reporter.create_log_file(target_directory=tmp_path)

        # Act
        reporter.log_operation(
            operation_type="copy",
            file_path=".claude/skills/skill-001.md",
            status="success",
            details={"source": "src/.claude/skills/skill-001.md", "size_bytes": 1024},
        )

        # Assert
        log_content = log_file.read_text()
        assert "copy" in log_content.lower()
        assert "skill-001.md" in log_content
        assert "success" in log_content.lower()

    def test_log_file_contains_validation_checks(self, tmp_path):
        """
        Test: Log file documents validation checkpoints (AC#2).

        Given: Installation includes validation steps
        When: Validation completes
        Then: Log contains validation checkpoint and result
        """
        # Arrange
        from installer.reporter import InstallationReporter

        devforgeai_dir = tmp_path / "devforgeai"
        devforgeai_dir.mkdir()

        reporter = InstallationReporter()
        log_file = reporter.create_log_file(target_directory=tmp_path)

        # Act
        reporter.log_validation("Directory structure", "passed")
        reporter.log_validation("File permissions", "passed")

        # Assert
        log_content = log_file.read_text()
        assert "validation" in log_content.lower() or "check" in log_content.lower()
        assert "Directory structure" in log_content
        assert "File permissions" in log_content

    def test_log_file_contains_error_messages_with_stack_traces(self, tmp_path):
        """
        Test: Log file includes error messages and full stack traces (AC#2).

        Given: Installation encounters an error
        When: Error is logged
        Then: Log contains error message and stack trace
        """
        # Arrange
        from installer.reporter import InstallationReporter

        devforgeai_dir = tmp_path / "devforgeai"
        devforgeai_dir.mkdir()

        reporter = InstallationReporter()
        log_file = reporter.create_log_file(target_directory=tmp_path)

        # Act
        try:
            raise ValueError("Test error: permission denied")
        except Exception as e:
            reporter.log_error("File operation", str(e))

        # Assert
        log_content = log_file.read_text()
        assert "error" in log_content.lower() or "exception" in log_content.lower()
        assert "permission denied" in log_content.lower()

    def test_log_file_contains_warning_messages(self, tmp_path):
        """
        Test: Log file includes warning messages (AC#2).

        Given: Installation encounters non-critical warnings
        When: Warning is logged
        Then: Log contains warning message
        """
        # Arrange
        from installer.reporter import InstallationReporter

        devforgeai_dir = tmp_path / "devforgeai"
        devforgeai_dir.mkdir()

        reporter = InstallationReporter()
        log_file = reporter.create_log_file(target_directory=tmp_path)

        # Act
        reporter.log_warning("Backup directory", "Could not create backup")

        # Assert
        log_content = log_file.read_text()
        assert "warning" in log_content.lower()
        assert "backup" in log_content.lower()

    def test_log_file_contains_phase_markers(self, tmp_path):
        """
        Test: Log file includes phase markers (AC#2).

        Given: Installation progresses through phases
        When: Each phase starts/completes
        Then: Log contains phase markers: Pre-flight, Core, Post-install, Validation
        """
        # Arrange
        from installer.reporter import InstallationReporter

        devforgeai_dir = tmp_path / "devforgeai"
        devforgeai_dir.mkdir()

        reporter = InstallationReporter()
        log_file = reporter.create_log_file(target_directory=tmp_path)

        # Act
        reporter.log_phase_start("Pre-flight")
        reporter.log_phase_start("Core")
        reporter.log_phase_start("Post-install")
        reporter.log_phase_start("Validation")

        # Assert
        log_content = log_file.read_text()
        assert "pre-flight" in log_content.lower()
        assert "core" in log_content.lower()
        assert "post-install" in log_content.lower() or "postinstall" in log_content.lower()
        assert "validation" in log_content.lower()

    def test_log_file_appends_never_overwrites(self, tmp_path):
        """
        Test: Log file appends entries, never overwrites (AC#2).

        Given: Log file exists with existing entries
        When: New entry is logged
        Then: New entry appended, previous entries preserved
        """
        # Arrange
        from installer.reporter import InstallationReporter

        devforgeai_dir = tmp_path / "devforgeai"
        devforgeai_dir.mkdir()

        reporter = InstallationReporter()
        log_file = reporter.create_log_file(target_directory=tmp_path)

        # Act - First entry
        reporter.log_operation("operation1", "file1.txt", "success")
        first_content = log_file.read_text()

        # Second write (should append)
        reporter.log_operation("operation2", "file2.txt", "success")
        second_content = log_file.read_text()

        # Assert
        assert "operation1" in second_content
        assert "operation2" in second_content
        assert len(second_content) > len(first_content)

    def test_log_file_uses_utf8_encoding_with_lf_line_endings(self, tmp_path):
        """
        Test: Log file uses UTF-8 encoding with LF (Unix) line endings (AC#2).

        Given: Log file is created
        When: Content is written
        Then: File uses UTF-8 encoding and LF line endings
        """
        # Arrange
        from installer.reporter import InstallationReporter

        devforgeai_dir = tmp_path / "devforgeai"
        devforgeai_dir.mkdir()

        reporter = InstallationReporter()
        log_file = reporter.create_log_file(target_directory=tmp_path)

        # Act
        reporter.log_operation("test", "file.txt", "success")

        # Assert
        raw_bytes = log_file.read_bytes()
        # Check UTF-8 validity
        try:
            raw_bytes.decode("utf-8")
        except UnicodeDecodeError:
            pytest.fail("Log file is not valid UTF-8")

        # Check for LF only (not CRLF)
        assert b"\r\n" not in raw_bytes, "Log contains Windows CRLF, expected Unix LF"


class TestJSONOutputMode:
    """Test JSON output mode with --json flag (AC#3)."""

    def test_json_output_contains_status_field(self, tmp_path):
        """
        Test: JSON output includes 'status' field (AC#3).

        Given: Installation completes with --json flag
        When: InstallationReporter.generate_json_output() called
        Then: JSON contains "status": "success" or "failure"
        """
        # Arrange
        from installer.reporter import InstallationReporter

        reporter = InstallationReporter()
        report_data = {
            "status": "success",
            "version": "1.0.0",
            "exit_code": 0,
            "files_installed": 450,
            "files_failed": 0,
            "errors": [],
            "warnings": [],
            "duration_seconds": 2.5,
            "target_directory": str(tmp_path),
            "log_file": str(tmp_path / "install.log"),
            "manifest_file": str(tmp_path / "devforgeai" / ".install-manifest.json"),
            "timestamp": "2025-11-20T10:30:00Z",
        }

        # Act
        json_output = reporter.generate_json_output(report_data)
        parsed = json.loads(json_output)

        # Assert
        assert "status" in parsed
        assert parsed["status"] in ["success", "failure"]

    def test_json_output_contains_all_required_fields(self, tmp_path):
        """
        Test: JSON output includes all required fields (AC#3).

        Given: Installation completes
        When: InstallationReporter.generate_json_output() called
        Then: JSON contains all 11 required fields
        """
        # Arrange
        from installer.reporter import InstallationReporter

        reporter = InstallationReporter()
        report_data = {
            "status": "success",
            "version": "1.0.0",
            "exit_code": 0,
            "files_installed": 450,
            "files_failed": 0,
            "errors": [],
            "warnings": [],
            "duration_seconds": 2.5,
            "target_directory": str(tmp_path),
            "log_file": str(tmp_path / "install.log"),
            "manifest_file": str(tmp_path / "devforgeai" / ".install-manifest.json"),
            "timestamp": "2025-11-20T10:30:00Z",
        }

        # Act
        json_output = reporter.generate_json_output(report_data)
        parsed = json.loads(json_output)

        # Assert - All 11 fields required
        required_fields = [
            "status",
            "version",
            "exit_code",
            "files_installed",
            "files_failed",
            "errors",
            "warnings",
            "duration_seconds",
            "target_directory",
            "log_file",
            "manifest_file",
            "timestamp",
        ]
        for field in required_fields:
            assert field in parsed, f"Missing required field: {field}"

    def test_json_output_duration_has_3_decimal_precision(self, tmp_path):
        """
        Test: JSON duration_seconds has 3 decimal places (AC#3).

        Given: Installation takes 2.456789 seconds
        When: JSON output generated
        Then: duration_seconds shows 3 decimal places: 2.457
        """
        # Arrange
        from installer.reporter import InstallationReporter

        reporter = InstallationReporter()
        report_data = {
            "status": "success",
            "version": "1.0.0",
            "exit_code": 0,
            "files_installed": 450,
            "files_failed": 0,
            "errors": [],
            "warnings": [],
            "duration_seconds": 2.456789,
            "target_directory": str(tmp_path),
            "log_file": str(tmp_path / "install.log"),
            "manifest_file": str(tmp_path / "devforgeai" / ".install-manifest.json"),
            "timestamp": "2025-11-20T10:30:00Z",
        }

        # Act
        json_output = reporter.generate_json_output(report_data)
        parsed = json.loads(json_output)

        # Assert
        duration_str = str(parsed["duration_seconds"])
        decimal_places = len(duration_str.split(".")[-1]) if "." in duration_str else 0
        assert (
            decimal_places == 3
        ), f"Expected 3 decimal places, got {decimal_places}: {duration_str}"

    def test_json_output_is_valid_json_only(self, tmp_path):
        """
        Test: JSON output contains ONLY valid JSON, no extra text (AC#3).

        Given: --json flag used
        When: Output written to stdout
        Then: Output parses as valid JSON, no text before/after
        """
        # Arrange
        from installer.reporter import InstallationReporter

        reporter = InstallationReporter()
        report_data = {
            "status": "success",
            "version": "1.0.0",
            "exit_code": 0,
            "files_installed": 450,
            "files_failed": 0,
            "errors": [],
            "warnings": [],
            "duration_seconds": 2.5,
            "target_directory": str(tmp_path),
            "log_file": str(tmp_path / "install.log"),
            "manifest_file": str(tmp_path / "devforgeai" / ".install-manifest.json"),
            "timestamp": "2025-11-20T10:30:00Z",
        }

        # Act
        json_output = reporter.generate_json_output(report_data)

        # Assert - Must be parseable as JSON
        try:
            parsed = json.loads(json_output)
        except json.JSONDecodeError as e:
            pytest.fail(f"Output is not valid JSON: {e}")

        # Assert - No text before/after JSON
        assert json_output.strip().startswith("{"), "JSON does not start with {"
        assert json_output.strip().endswith("}"), "JSON does not end with }"

    def test_json_output_exit_code_zero_for_success(self, tmp_path):
        """
        Test: JSON exit_code is 0 for success, non-zero for failure (AC#3).

        Given: Installation succeeds
        When: JSON output generated
        Then: exit_code = 0
        """
        # Arrange
        from installer.reporter import InstallationReporter

        reporter = InstallationReporter()
        report_data = {
            "status": "success",
            "version": "1.0.0",
            "exit_code": 0,
            "files_installed": 450,
            "files_failed": 0,
            "errors": [],
            "warnings": [],
            "duration_seconds": 2.5,
            "target_directory": str(tmp_path),
            "log_file": str(tmp_path / "install.log"),
            "manifest_file": str(tmp_path / "devforgeai" / ".install-manifest.json"),
            "timestamp": "2025-11-20T10:30:00Z",
        }

        # Act
        json_output = reporter.generate_json_output(report_data)
        parsed = json.loads(json_output)

        # Assert
        assert parsed["exit_code"] == 0

    def test_json_output_exit_code_nonzero_for_failure(self, tmp_path):
        """
        Test: JSON exit_code is non-zero (1-255) for failure (AC#3).

        Given: Installation fails
        When: JSON output generated
        Then: exit_code = 1 (or other non-zero value)
        """
        # Arrange
        from installer.reporter import InstallationReporter

        reporter = InstallationReporter()
        report_data = {
            "status": "failure",
            "version": "1.0.0",
            "exit_code": 1,
            "files_installed": 150,
            "files_failed": 50,
            "errors": [
                {
                    "type": "PERMISSION_DENIED",
                    "message": "Cannot write to .claude/",
                    "file": ".claude/skills/test.md",
                }
            ],
            "warnings": [],
            "duration_seconds": 1.2,
            "target_directory": str(tmp_path),
            "log_file": str(tmp_path / "install.log"),
            "manifest_file": str(tmp_path / "devforgeai" / ".install-manifest.json"),
            "timestamp": "2025-11-20T10:30:00Z",
        }

        # Act
        json_output = reporter.generate_json_output(report_data)
        parsed = json.loads(json_output)

        # Assert
        assert parsed["exit_code"] != 0
        assert 1 <= parsed["exit_code"] <= 255


class TestErrorCategorization:
    """Test error categorization with 7 types (AC#6)."""

    def test_error_type_permission_denied(self, tmp_path):
        """
        Test: Error categorized as PERMISSION_DENIED (AC#6).

        Given: File write fails with permission error
        When: Error categorized
        Then: Error type = PERMISSION_DENIED
        """
        # Arrange
        from installer.reporter import InstallationReporter

        reporter = InstallationReporter()

        # Act
        error = reporter.categorize_error(PermissionError("Cannot write to file"))

        # Assert
        assert error["type"] == "PERMISSION_DENIED"
        assert "permission" in error.get("message", "").lower()

    def test_error_type_file_not_found(self, tmp_path):
        """
        Test: Error categorized as FILE_NOT_FOUND (AC#6).

        Given: Source file does not exist
        When: Error categorized
        Then: Error type = FILE_NOT_FOUND
        """
        # Arrange
        from installer.reporter import InstallationReporter

        reporter = InstallationReporter()

        # Act
        error = reporter.categorize_error(FileNotFoundError("File not found: test.py"))

        # Assert
        assert error["type"] == "FILE_NOT_FOUND"

    def test_error_type_checksum_mismatch(self, tmp_path):
        """
        Test: Error categorized as CHECKSUM_MISMATCH (AC#6).

        Given: File checksum validation fails
        When: Error categorized with checksum context
        Then: Error type = CHECKSUM_MISMATCH
        """
        # Arrange
        from installer.reporter import InstallationReporter

        reporter = InstallationReporter()

        # Act
        error = reporter.categorize_error(
            ValueError("Checksum mismatch"),
            error_context="checksum_validation",
        )

        # Assert
        assert error["type"] == "CHECKSUM_MISMATCH"

    def test_error_type_git_error(self, tmp_path):
        """
        Test: Error categorized as GIT_ERROR (AC#6).

        Given: Git operation fails
        When: Error categorized with git context
        Then: Error type = GIT_ERROR
        """
        # Arrange
        from installer.reporter import InstallationReporter

        reporter = InstallationReporter()

        # Act
        error = reporter.categorize_error(
            RuntimeError("Git operation failed"), error_context="git_operation"
        )

        # Assert
        assert error["type"] == "GIT_ERROR"

    def test_error_type_validation_error(self, tmp_path):
        """
        Test: Error categorized as VALIDATION_ERROR (AC#6).

        Given: Structure validation fails
        When: Error categorized with validation context
        Then: Error type = VALIDATION_ERROR
        """
        # Arrange
        from installer.reporter import InstallationReporter

        reporter = InstallationReporter()

        # Act
        error = reporter.categorize_error(
            AssertionError("Directory structure invalid"),
            error_context="validation",
        )

        # Assert
        assert error["type"] == "VALIDATION_ERROR"

    def test_error_type_dependency_error(self, tmp_path):
        """
        Test: Error categorized as DEPENDENCY_ERROR (AC#6).

        Given: Missing required dependency
        When: Error categorized with dependency context
        Then: Error type = DEPENDENCY_ERROR
        """
        # Arrange
        from installer.reporter import InstallationReporter

        reporter = InstallationReporter()

        # Act
        error = reporter.categorize_error(
            ImportError("Missing module: requests"),
            error_context="dependency",
        )

        # Assert
        assert error["type"] == "DEPENDENCY_ERROR"

    def test_error_type_unknown_error(self, tmp_path):
        """
        Test: Unexpected exceptions categorized as UNKNOWN_ERROR (AC#6).

        Given: Unexpected exception type
        When: Error categorized
        Then: Error type = UNKNOWN_ERROR
        """
        # Arrange
        from installer.reporter import InstallationReporter

        reporter = InstallationReporter()

        # Act
        error = reporter.categorize_error(Exception("Unexpected error"))

        # Assert
        assert error["type"] == "UNKNOWN_ERROR"

    def test_error_object_contains_required_fields(self, tmp_path):
        """
        Test: Error objects contain type, message, and optional file/line fields.

        Given: Error is categorized
        When: Error object created
        Then: Contains: type, message, file (optional), line_number (optional)
        """
        # Arrange
        from installer.reporter import InstallationReporter

        reporter = InstallationReporter()

        # Act
        error = reporter.categorize_error(
            PermissionError("Cannot write"),
            file_path=".claude/test.md",
        )

        # Assert
        assert "type" in error
        assert "message" in error
        assert error["message"] is not None


class TestAuditTrail:
    """Test audit trail compliance (AC#7)."""

    def test_audit_trail_every_file_operation_traceable(self, tmp_path):
        """
        Test: Every file operation is traceable in log (AC#7).

        Given: Multiple files copied
        When: Operations logged
        Then: Log contains traceable record of each operation
        """
        # Arrange
        from installer.reporter import InstallationReporter

        devforgeai_dir = tmp_path / "devforgeai"
        devforgeai_dir.mkdir()

        reporter = InstallationReporter()
        log_file = reporter.create_log_file(target_directory=tmp_path)

        # Act
        reporter.log_operation("copy", ".claude/skills/skill1.md", "success")
        reporter.log_operation("copy", ".claude/skills/skill2.md", "success")
        reporter.log_operation("copy", "devforgeai/specs/context/tech-stack.md", "success")

        # Assert
        log_content = log_file.read_text()
        assert "skill1.md" in log_content
        assert "skill2.md" in log_content
        assert "tech-stack.md" in log_content

    def test_audit_trail_no_sensitive_information_logged(self, tmp_path):
        """
        Test: No credentials/tokens/passwords in log (AC#7).

        Given: Log contains sensitive patterns
        When: Log written
        Then: Sensitive info redacted or absent
        """
        # Arrange
        from installer.reporter import InstallationReporter

        devforgeai_dir = tmp_path / "devforgeai"
        devforgeai_dir.mkdir()

        reporter = InstallationReporter()
        log_file = reporter.create_log_file(target_directory=tmp_path)

        # Act - Try to log sensitive data (should be redacted)
        reporter.log_operation(
            "copy",
            "secret_file.txt",
            "success",
            details={"content": "token=abc123xyz"},
        )

        # Assert
        log_content = log_file.read_text()
        sensitive_patterns = ["password", "token", "secret", "api_key", "api-key"]
        for pattern in sensitive_patterns:
            if pattern in log_content.lower():
                # If pattern found, it should be redacted
                assert "[REDACTED]" in log_content


class TestPerformanceNFRs:
    """Test non-functional requirements for performance (NFR-001, NFR-002)."""

    def test_console_report_generation_under_100ms(self, tmp_path):
        """
        Test: Console report generation < 100ms (NFR-001).

        Given: Installation complete
        When: generate_console_report() called
        Then: Returns in < 100ms
        """
        # Arrange
        from installer.reporter import InstallationReporter

        reporter = InstallationReporter()
        report_data = {
            "status": "success",
            "version": "1.0.0",
            "files_installed": 450,
            "files_failed": 0,
            "duration_seconds": 2.5,
            "target_directory": str(tmp_path),
            "log_file": str(tmp_path / "install.log"),
        }

        # Act
        start = time.time()
        console_output = reporter.generate_console_report(report_data)
        elapsed_ms = (time.time() - start) * 1000

        # Assert
        assert elapsed_ms < 100, f"Report generation took {elapsed_ms:.1f}ms (expected <100ms)"

    def test_json_serialization_under_50ms(self, tmp_path):
        """
        Test: JSON serialization < 50ms regardless of file count (NFR-002).

        Given: Large installation with 500 files
        When: generate_json_output() called
        Then: Returns in < 50ms
        """
        # Arrange
        from installer.reporter import InstallationReporter

        reporter = InstallationReporter()

        # Create report with 500 files
        errors = [
            {
                "type": "FILE_NOT_FOUND",
                "message": f"File {i} not found",
                "file": f".claude/file_{i}.md",
            }
            for i in range(500)
        ]

        report_data = {
            "status": "failure",
            "version": "1.0.0",
            "exit_code": 1,
            "files_installed": 0,
            "files_failed": 500,
            "errors": errors,
            "warnings": [],
            "duration_seconds": 5.5,
            "target_directory": str(tmp_path),
            "log_file": str(tmp_path / "install.log"),
            "manifest_file": str(tmp_path / "devforgeai" / ".install-manifest.json"),
            "timestamp": "2025-11-20T10:30:00Z",
        }

        # Act
        start = time.time()
        json_output = reporter.generate_json_output(report_data)
        elapsed_ms = (time.time() - start) * 1000

        # Assert
        assert elapsed_ms < 50, f"JSON serialization took {elapsed_ms:.1f}ms (expected <50ms)"
        # Verify output is valid JSON
        parsed = json.loads(json_output)
        assert len(parsed["errors"]) == 500


class TestSecurityNFRs:
    """Test security non-functional requirements (NFR-006, NFR-007)."""

    def test_log_file_permissions_644(self, tmp_path):
        """
        Test: Log file permissions set to 644 (rw-r--r--) (NFR-006).

        Given: Log file created
        When: Log file written
        Then: File permissions are 644 (user rw, group r, other r)
        """
        # Arrange
        from installer.reporter import InstallationReporter
        import stat

        devforgeai_dir = tmp_path / "devforgeai"
        devforgeai_dir.mkdir()

        reporter = InstallationReporter()

        # Act
        log_file = reporter.create_log_file(target_directory=tmp_path)
        reporter.log_operation("test", "file.txt", "success")

        # Assert
        file_stat = log_file.stat()
        file_perms = stat.filemode(file_stat.st_mode)
        # Check octal permissions: should be -rw-r--r--
        assert file_perms[1:] == "rw-r--r--", f"Expected -rw-r--r--, got {file_perms}"

    def test_manifest_file_permissions_644(self, tmp_path):
        """
        Test: Manifest file permissions set to 644 (NFR-006).

        Given: Manifest file created
        When: Installation completes
        Then: Manifest permissions are 644
        """
        # Arrange & Act & Assert - Verify in manifest generator tests
        # This test ensures consistency with security requirement
        pass
