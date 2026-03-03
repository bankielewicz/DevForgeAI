"""
STORY-237: Enhanced Exit Codes - TDD Red Phase Tests

All tests will FAIL until implementation is complete (TDD Red phase).

Acceptance Criteria Covered:
- AC#1: New Exit Codes Defined (DISK_SPACE_ERROR=5, NTFS_PERMISSION=6, FILE_LOCKED=7)
- AC#2: Exit Code Documentation (docstring documents all 8 codes 0-7)
- AC#3: Platform-Aware Resolution Messages (Windows/WSL/Linux/macOS)
- AC#4: Exit Code Integration with Pre-Flight (exit codes for specific failures)
- AC#5: Resolution Messages by Exit Code (get_resolution_message function)

Technical Requirements Covered:
- BR-001: No duplicate exit code values
- BR-002: Code 6 (NTFS_PERMISSION) only relevant for WSL
- BR-003: Messages contain actionable commands
- NFR-001: Exit codes platform-independent
- SVC-005: get_resolution_message(code, platform) returns correct text

Coverage Target: 95%+
Test Framework: pytest (per tech-stack.md)
"""

import sys
from pathlib import Path
from unittest.mock import patch, MagicMock

import pytest

# Add parent directory to path so 'installer' module can be imported
sys.path.insert(0, str(Path(__file__).parent.parent.parent))


# =============================================================================
# AC#1: New Exit Codes Defined
# =============================================================================


class TestAC1_ExitCodesDefinition:
    """AC#1: New Exit Codes Defined - DISK_SPACE_ERROR=5, NTFS_PERMISSION=6, FILE_LOCKED=7"""

    def test_disk_space_error_value_equals_5(self):
        """Test: DISK_SPACE_ERROR = 5 is exported from ExitCodes class."""
        from installer.exit_codes import ExitCodes

        assert ExitCodes.DISK_SPACE_ERROR == 5, (
            f"Expected DISK_SPACE_ERROR = 5, got {ExitCodes.DISK_SPACE_ERROR}"
        )

    def test_ntfs_permission_value_equals_6(self):
        """Test: NTFS_PERMISSION = 6 is exported from ExitCodes class."""
        from installer.exit_codes import ExitCodes

        assert ExitCodes.NTFS_PERMISSION == 6, (
            f"Expected NTFS_PERMISSION = 6, got {ExitCodes.NTFS_PERMISSION}"
        )

    def test_file_locked_value_equals_7(self):
        """Test: FILE_LOCKED = 7 is exported from ExitCodes class."""
        from installer.exit_codes import ExitCodes

        assert ExitCodes.FILE_LOCKED == 7, (
            f"Expected FILE_LOCKED = 7, got {ExitCodes.FILE_LOCKED}"
        )

    def test_module_level_disk_space_error_constant(self):
        """Test: DISK_SPACE_ERROR module-level constant exported for direct import."""
        from installer.exit_codes import DISK_SPACE_ERROR

        assert DISK_SPACE_ERROR == 5, (
            f"Expected module-level DISK_SPACE_ERROR = 5, got {DISK_SPACE_ERROR}"
        )

    def test_module_level_ntfs_permission_constant(self):
        """Test: NTFS_PERMISSION module-level constant exported for direct import."""
        from installer.exit_codes import NTFS_PERMISSION

        assert NTFS_PERMISSION == 6, (
            f"Expected module-level NTFS_PERMISSION = 6, got {NTFS_PERMISSION}"
        )

    def test_module_level_file_locked_constant(self):
        """Test: FILE_LOCKED module-level constant exported for direct import."""
        from installer.exit_codes import FILE_LOCKED

        assert FILE_LOCKED == 7, (
            f"Expected module-level FILE_LOCKED = 7, got {FILE_LOCKED}"
        )

    def test_existing_exit_codes_preserved(self):
        """Test: Existing exit codes (0-4) remain unchanged after adding new codes."""
        from installer.exit_codes import (
            SUCCESS, MISSING_SOURCE, PERMISSION_DENIED,
            ROLLBACK_OCCURRED, VALIDATION_FAILED
        )

        assert SUCCESS == 0, "SUCCESS should remain 0"
        assert MISSING_SOURCE == 1, "MISSING_SOURCE should remain 1"
        assert PERMISSION_DENIED == 2, "PERMISSION_DENIED should remain 2"
        assert ROLLBACK_OCCURRED == 3, "ROLLBACK_OCCURRED should remain 3"
        assert VALIDATION_FAILED == 4, "VALIDATION_FAILED should remain 4"


# =============================================================================
# AC#2: Exit Code Documentation
# =============================================================================


class TestAC2_ExitCodeDocumentation:
    """AC#2: Exit Code Documentation - ExitCodes docstring documents all 8 codes"""

    def test_exitcodes_docstring_exists(self):
        """Test: ExitCodes class has a non-empty docstring."""
        from installer.exit_codes import ExitCodes

        assert ExitCodes.__doc__ is not None, "ExitCodes must have a docstring"
        assert len(ExitCodes.__doc__.strip()) > 0, "ExitCodes docstring must not be empty"

    def test_docstring_documents_success_code_0(self):
        """Test: Docstring documents SUCCESS = 0."""
        from installer.exit_codes import ExitCodes

        docstring = ExitCodes.__doc__.lower()
        assert "0" in docstring and "success" in docstring, (
            "Docstring must document exit code 0 (SUCCESS)"
        )

    def test_docstring_documents_missing_source_code_1(self):
        """Test: Docstring documents MISSING_SOURCE = 1."""
        from installer.exit_codes import ExitCodes

        docstring = ExitCodes.__doc__.lower()
        assert "1" in docstring and "missing" in docstring, (
            "Docstring must document exit code 1 (MISSING_SOURCE)"
        )

    def test_docstring_documents_permission_denied_code_2(self):
        """Test: Docstring documents PERMISSION_DENIED = 2."""
        from installer.exit_codes import ExitCodes

        docstring = ExitCodes.__doc__.lower()
        assert "2" in docstring and "permission" in docstring, (
            "Docstring must document exit code 2 (PERMISSION_DENIED)"
        )

    def test_docstring_documents_rollback_occurred_code_3(self):
        """Test: Docstring documents ROLLBACK_OCCURRED = 3."""
        from installer.exit_codes import ExitCodes

        docstring = ExitCodes.__doc__.lower()
        assert "3" in docstring and "rollback" in docstring, (
            "Docstring must document exit code 3 (ROLLBACK_OCCURRED)"
        )

    def test_docstring_documents_validation_failed_code_4(self):
        """Test: Docstring documents VALIDATION_FAILED = 4."""
        from installer.exit_codes import ExitCodes

        docstring = ExitCodes.__doc__.lower()
        assert "4" in docstring and "validation" in docstring, (
            "Docstring must document exit code 4 (VALIDATION_FAILED)"
        )

    def test_docstring_documents_disk_space_error_code_5(self):
        """Test: Docstring documents DISK_SPACE_ERROR = 5."""
        from installer.exit_codes import ExitCodes

        docstring = ExitCodes.__doc__.lower()
        assert "5" in docstring and "disk" in docstring and "space" in docstring, (
            "Docstring must document exit code 5 (DISK_SPACE_ERROR)"
        )

    def test_docstring_documents_ntfs_permission_code_6(self):
        """Test: Docstring documents NTFS_PERMISSION = 6."""
        from installer.exit_codes import ExitCodes

        docstring = ExitCodes.__doc__.lower()
        assert "6" in docstring and "ntfs" in docstring, (
            "Docstring must document exit code 6 (NTFS_PERMISSION)"
        )

    def test_docstring_documents_file_locked_code_7(self):
        """Test: Docstring documents FILE_LOCKED = 7."""
        from installer.exit_codes import ExitCodes

        docstring = ExitCodes.__doc__.lower()
        assert "7" in docstring and ("file" in docstring and "lock" in docstring), (
            "Docstring must document exit code 7 (FILE_LOCKED)"
        )

    def test_docstring_covers_all_8_exit_codes(self):
        """Test: Docstring documents all 8 exit codes (0-7)."""
        from installer.exit_codes import ExitCodes

        docstring = ExitCodes.__doc__

        # Check for all 8 code numbers
        for code_num in range(8):
            assert str(code_num) in docstring, (
                f"Docstring must document exit code {code_num}"
            )


# =============================================================================
# AC#3: Platform-Aware Resolution Messages
# =============================================================================


class TestAC3_PlatformAwareResolutionMessages:
    """AC#3: Platform-Aware Resolution Messages - Windows/WSL/Linux/macOS"""

    def test_windows_message_includes_run_as_administrator(self):
        """Test: Windows resolution messages include 'Run as Administrator'."""
        from installer.exit_codes import get_resolution_message, PERMISSION_DENIED

        message = get_resolution_message(PERMISSION_DENIED, "Windows")

        assert "administrator" in message.lower(), (
            f"Windows message must include 'Administrator', got: {message}"
        )

    def test_wsl_message_includes_remount_with_metadata(self):
        """Test: WSL resolution messages include 'remount with metadata'."""
        from installer.exit_codes import get_resolution_message, NTFS_PERMISSION

        message = get_resolution_message(NTFS_PERMISSION, "WSL")

        assert "remount" in message.lower() and "metadata" in message.lower(), (
            f"WSL message must include 'remount with metadata', got: {message}"
        )

    def test_linux_message_includes_run_with_sudo(self):
        """Test: Linux resolution messages include 'Run with sudo'."""
        from installer.exit_codes import get_resolution_message, PERMISSION_DENIED

        message = get_resolution_message(PERMISSION_DENIED, "Linux")

        assert "sudo" in message.lower(), (
            f"Linux message must include 'sudo', got: {message}"
        )

    def test_macos_message_includes_sudo_or_gatekeeper(self):
        """Test: macOS resolution messages include 'sudo' or 'Gatekeeper'."""
        from installer.exit_codes import get_resolution_message, PERMISSION_DENIED

        message = get_resolution_message(PERMISSION_DENIED, "Darwin")

        has_sudo = "sudo" in message.lower()
        has_gatekeeper = "gatekeeper" in message.lower()

        assert has_sudo or has_gatekeeper, (
            f"macOS message must include 'sudo' or 'Gatekeeper', got: {message}"
        )

    def test_wsl_linux_path_recommendation(self):
        """Test: WSL messages recommend using Linux-native path."""
        from installer.exit_codes import get_resolution_message, NTFS_PERMISSION

        message = get_resolution_message(NTFS_PERMISSION, "WSL")

        # Should recommend either Linux-native path OR remount
        has_linux_path = "linux" in message.lower() and "path" in message.lower()
        has_remount = "remount" in message.lower()

        assert has_linux_path or has_remount, (
            f"WSL message must recommend Linux-native path or remount, got: {message}"
        )


# =============================================================================
# AC#4: Exit Code Integration with Pre-Flight
# =============================================================================


class TestAC4_ExitCodeIntegrationWithPreflight:
    """AC#4: Exit Code Integration - Pre-flight failures map to correct exit codes"""

    def test_disk_space_below_25mb_returns_exit_code_5(self):
        """Test: Disk space < 25MB results in exit code 5 (DISK_SPACE_ERROR)."""
        from installer.exit_codes import DISK_SPACE_ERROR

        # Exit code value should be 5 for disk space errors
        assert DISK_SPACE_ERROR == 5, (
            f"DISK_SPACE_ERROR should be 5 for insufficient disk space, got {DISK_SPACE_ERROR}"
        )

    def test_ntfs_permission_on_wsl_returns_exit_code_6(self):
        """Test: NTFS permission on WSL results in exit code 6 (NTFS_PERMISSION)."""
        from installer.exit_codes import NTFS_PERMISSION

        # Exit code value should be 6 for NTFS permission issues on WSL
        assert NTFS_PERMISSION == 6, (
            f"NTFS_PERMISSION should be 6 for WSL NTFS issues, got {NTFS_PERMISSION}"
        )

    def test_file_locked_returns_exit_code_7(self):
        """Test: File locked by another process results in exit code 7 (FILE_LOCKED)."""
        from installer.exit_codes import FILE_LOCKED

        # Exit code value should be 7 for file lock errors
        assert FILE_LOCKED == 7, (
            f"FILE_LOCKED should be 7 for file lock errors, got {FILE_LOCKED}"
        )

    def test_exit_codes_unique_no_overlap(self):
        """Test BR-001: No duplicate exit code values across all 8 codes."""
        from installer.exit_codes import (
            SUCCESS, MISSING_SOURCE, PERMISSION_DENIED, ROLLBACK_OCCURRED,
            VALIDATION_FAILED, DISK_SPACE_ERROR, NTFS_PERMISSION, FILE_LOCKED
        )

        codes = [
            SUCCESS, MISSING_SOURCE, PERMISSION_DENIED, ROLLBACK_OCCURRED,
            VALIDATION_FAILED, DISK_SPACE_ERROR, NTFS_PERMISSION, FILE_LOCKED
        ]

        # All codes should be unique
        assert len(codes) == len(set(codes)), (
            f"Exit codes must be unique. Found duplicates: {codes}"
        )

    def test_exit_codes_in_valid_range_0_to_7(self):
        """Test: All exit codes are in range 0-7 (per story design)."""
        from installer.exit_codes import (
            SUCCESS, MISSING_SOURCE, PERMISSION_DENIED, ROLLBACK_OCCURRED,
            VALIDATION_FAILED, DISK_SPACE_ERROR, NTFS_PERMISSION, FILE_LOCKED
        )

        codes = [
            SUCCESS, MISSING_SOURCE, PERMISSION_DENIED, ROLLBACK_OCCURRED,
            VALIDATION_FAILED, DISK_SPACE_ERROR, NTFS_PERMISSION, FILE_LOCKED
        ]

        for code in codes:
            assert 0 <= code <= 7, f"Exit code {code} is out of range 0-7"


# =============================================================================
# AC#5: Resolution Messages by Exit Code
# =============================================================================


class TestAC5_ResolutionMessagesByExitCode:
    """AC#5: Resolution Messages - get_resolution_message(code, platform) function"""

    def test_get_resolution_message_function_exists(self):
        """Test SVC-005: get_resolution_message function exists in module."""
        from installer.exit_codes import get_resolution_message

        assert callable(get_resolution_message), (
            "get_resolution_message must be a callable function"
        )

    def test_get_resolution_message_returns_string(self):
        """Test: get_resolution_message returns a non-empty string."""
        from installer.exit_codes import get_resolution_message, DISK_SPACE_ERROR

        result = get_resolution_message(DISK_SPACE_ERROR, "Linux")

        assert isinstance(result, str), f"Expected string, got {type(result)}"
        assert len(result) > 0, "Resolution message must not be empty"

    def test_disk_space_error_message_mentions_25mb(self):
        """Test: DISK_SPACE_ERROR message mentions '25MB'."""
        from installer.exit_codes import get_resolution_message, DISK_SPACE_ERROR

        message = get_resolution_message(DISK_SPACE_ERROR, "Linux")

        assert "25" in message and "mb" in message.lower(), (
            f"DISK_SPACE_ERROR message must mention '25MB', got: {message}"
        )

    def test_ntfs_permission_wsl_message_includes_remount(self):
        """Test: NTFS_PERMISSION message for WSL includes 'remount'."""
        from installer.exit_codes import get_resolution_message, NTFS_PERMISSION

        message = get_resolution_message(NTFS_PERMISSION, "WSL")

        assert "remount" in message.lower(), (
            f"NTFS_PERMISSION WSL message must include 'remount', got: {message}"
        )

    def test_file_locked_message_mentions_vs_code(self):
        """Test: FILE_LOCKED message mentions 'VS Code'."""
        from installer.exit_codes import get_resolution_message, FILE_LOCKED

        message = get_resolution_message(FILE_LOCKED, "Windows")

        # Could be "VS Code", "vscode", or "Visual Studio Code"
        has_vscode = any(term in message.lower() for term in ["vs code", "vscode", "visual studio code"])

        assert has_vscode, (
            f"FILE_LOCKED message must mention 'VS Code', got: {message}"
        )

    def test_ntfs_permission_non_wsl_returns_generic_message(self):
        """Test BR-002: NTFS_PERMISSION on non-WSL returns generic message."""
        from installer.exit_codes import get_resolution_message, NTFS_PERMISSION

        message = get_resolution_message(NTFS_PERMISSION, "Windows")

        # Should return a generic or different message for non-WSL
        # The WSL-specific "remount with metadata" should not appear
        assert "metadata" not in message.lower() or "ntfs" not in message.lower(), (
            f"NTFS_PERMISSION on Windows should not mention WSL-specific remount: {message}"
        )

    def test_resolution_message_varies_by_platform(self):
        """Test: Same exit code returns different messages for different platforms."""
        from installer.exit_codes import get_resolution_message, PERMISSION_DENIED

        linux_msg = get_resolution_message(PERMISSION_DENIED, "Linux")
        windows_msg = get_resolution_message(PERMISSION_DENIED, "Windows")
        macos_msg = get_resolution_message(PERMISSION_DENIED, "Darwin")

        # At least some messages should be different
        messages = [linux_msg, windows_msg, macos_msg]
        unique_messages = set(messages)

        assert len(unique_messages) >= 2, (
            f"Resolution messages should vary by platform. Got: Linux='{linux_msg}', "
            f"Windows='{windows_msg}', macOS='{macos_msg}'"
        )


# =============================================================================
# Technical Requirements: Business Rules
# =============================================================================


class TestBusinessRules:
    """Business Rules tests from Technical Specification"""

    def test_br001_no_duplicate_exit_code_values(self):
        """Test BR-001: No duplicate exit code values."""
        from installer.exit_codes import ExitCodes

        # Collect all exit code values from ExitCodes class
        codes = []
        for attr in dir(ExitCodes):
            if attr.isupper() and not attr.startswith('_'):
                value = getattr(ExitCodes, attr)
                if isinstance(value, int):
                    codes.append((attr, value))

        # Check for duplicates
        values = [v for _, v in codes]
        duplicates = [v for v in values if values.count(v) > 1]

        assert len(duplicates) == 0, (
            f"Found duplicate exit code values: {duplicates}. Codes: {codes}"
        )

    def test_br002_ntfs_permission_only_for_wsl(self):
        """Test BR-002: Code 6 (NTFS_PERMISSION) only relevant for WSL."""
        from installer.exit_codes import get_resolution_message, NTFS_PERMISSION

        wsl_message = get_resolution_message(NTFS_PERMISSION, "WSL")
        linux_message = get_resolution_message(NTFS_PERMISSION, "Linux")

        # WSL message should have specific NTFS guidance
        assert "remount" in wsl_message.lower() or "ntfs" in wsl_message.lower() or "mount" in wsl_message.lower(), (
            f"WSL message for NTFS_PERMISSION should be specific: {wsl_message}"
        )

    def test_br003_messages_contain_actionable_commands(self):
        """Test BR-003: Messages must contain actionable commands."""
        from installer.exit_codes import get_resolution_message
        from installer.exit_codes import PERMISSION_DENIED, DISK_SPACE_ERROR, NTFS_PERMISSION

        # Check that messages contain command-like patterns
        actionable_patterns = [
            "run", "sudo", "administrator", "delete", "free", "close",
            "remount", "mount", "chmod", "check"
        ]

        messages_to_check = [
            (PERMISSION_DENIED, "Linux"),
            (PERMISSION_DENIED, "Windows"),
            (DISK_SPACE_ERROR, "Linux"),
            (NTFS_PERMISSION, "WSL"),
        ]

        for code, platform in messages_to_check:
            message = get_resolution_message(code, platform)
            has_action = any(pattern in message.lower() for pattern in actionable_patterns)

            assert has_action, (
                f"Message for code {code} on {platform} must contain actionable command: {message}"
            )


# =============================================================================
# Technical Requirements: Non-Functional Requirements
# =============================================================================


class TestNonFunctionalRequirements:
    """Non-Functional Requirements tests from Technical Specification"""

    def test_nfr001_exit_codes_platform_independent(self):
        """Test NFR-001: Exit codes must be consistent across all platforms."""
        from installer.exit_codes import (
            SUCCESS, MISSING_SOURCE, PERMISSION_DENIED, ROLLBACK_OCCURRED,
            VALIDATION_FAILED, DISK_SPACE_ERROR, NTFS_PERMISSION, FILE_LOCKED
        )

        # Exit codes are integer constants - they don't change by platform
        expected_codes = {
            "SUCCESS": 0,
            "MISSING_SOURCE": 1,
            "PERMISSION_DENIED": 2,
            "ROLLBACK_OCCURRED": 3,
            "VALIDATION_FAILED": 4,
            "DISK_SPACE_ERROR": 5,
            "NTFS_PERMISSION": 6,
            "FILE_LOCKED": 7,
        }

        actual_codes = {
            "SUCCESS": SUCCESS,
            "MISSING_SOURCE": MISSING_SOURCE,
            "PERMISSION_DENIED": PERMISSION_DENIED,
            "ROLLBACK_OCCURRED": ROLLBACK_OCCURRED,
            "VALIDATION_FAILED": VALIDATION_FAILED,
            "DISK_SPACE_ERROR": DISK_SPACE_ERROR,
            "NTFS_PERMISSION": NTFS_PERMISSION,
            "FILE_LOCKED": FILE_LOCKED,
        }

        assert expected_codes == actual_codes, (
            f"Exit codes must match expected values. Expected: {expected_codes}, Got: {actual_codes}"
        )


# =============================================================================
# Edge Cases and Error Handling
# =============================================================================


class TestEdgeCases:
    """Edge case tests for robustness"""

    def test_get_resolution_message_unknown_platform(self):
        """Test: get_resolution_message handles unknown platform gracefully."""
        from installer.exit_codes import get_resolution_message, PERMISSION_DENIED

        # Should not raise an exception
        message = get_resolution_message(PERMISSION_DENIED, "UnknownOS")

        assert isinstance(message, str), "Should return string for unknown platform"
        assert len(message) > 0, "Should return non-empty message for unknown platform"

    def test_get_resolution_message_unknown_exit_code(self):
        """Test: get_resolution_message handles unknown exit code gracefully."""
        from installer.exit_codes import get_resolution_message

        # Use an exit code that doesn't exist (99)
        message = get_resolution_message(99, "Linux")

        assert isinstance(message, str), "Should return string for unknown exit code"
        # Could be empty or generic message - implementation choice

    def test_get_resolution_message_case_insensitive_platform(self):
        """Test: get_resolution_message handles platform name case variations."""
        from installer.exit_codes import get_resolution_message, PERMISSION_DENIED

        # These should all work (implementation may normalize)
        platforms = ["Linux", "LINUX", "linux", "Windows", "WINDOWS", "windows"]

        for platform in platforms:
            message = get_resolution_message(PERMISSION_DENIED, platform)
            assert isinstance(message, str), f"Failed for platform: {platform}"


# =============================================================================
# Integration Tests
# =============================================================================


class TestIntegrationScenarios:
    """Integration scenarios combining multiple features"""

    def test_all_exit_codes_have_resolution_messages(self):
        """Test: Every exit code has a resolution message for each platform."""
        from installer.exit_codes import (
            get_resolution_message,
            SUCCESS, MISSING_SOURCE, PERMISSION_DENIED, ROLLBACK_OCCURRED,
            VALIDATION_FAILED, DISK_SPACE_ERROR, NTFS_PERMISSION, FILE_LOCKED
        )

        codes = [
            SUCCESS, MISSING_SOURCE, PERMISSION_DENIED, ROLLBACK_OCCURRED,
            VALIDATION_FAILED, DISK_SPACE_ERROR, NTFS_PERMISSION, FILE_LOCKED
        ]
        platforms = ["Linux", "Windows", "Darwin", "WSL"]

        for code in codes:
            for platform in platforms:
                message = get_resolution_message(code, platform)
                assert isinstance(message, str), (
                    f"Missing message for code {code} on {platform}"
                )

    def test_exit_code_constants_match_class_attributes(self):
        """Test: Module-level constants match ExitCodes class attributes."""
        from installer.exit_codes import ExitCodes
        from installer.exit_codes import (
            SUCCESS, MISSING_SOURCE, PERMISSION_DENIED, ROLLBACK_OCCURRED,
            VALIDATION_FAILED, DISK_SPACE_ERROR, NTFS_PERMISSION, FILE_LOCKED
        )

        assert SUCCESS == ExitCodes.SUCCESS
        assert MISSING_SOURCE == ExitCodes.MISSING_SOURCE
        assert PERMISSION_DENIED == ExitCodes.PERMISSION_DENIED
        assert ROLLBACK_OCCURRED == ExitCodes.ROLLBACK_OCCURRED
        assert VALIDATION_FAILED == ExitCodes.VALIDATION_FAILED
        assert DISK_SPACE_ERROR == ExitCodes.DISK_SPACE_ERROR
        assert NTFS_PERMISSION == ExitCodes.NTFS_PERMISSION
        assert FILE_LOCKED == ExitCodes.FILE_LOCKED


# =============================================================================
# Test that file_locked and disk_space error messages are actionable
# =============================================================================


class TestActionableMessages:
    """Verify resolution messages provide actionable guidance"""

    def test_disk_space_error_suggests_freeing_space(self):
        """Test: Disk space error message suggests freeing space."""
        from installer.exit_codes import get_resolution_message, DISK_SPACE_ERROR

        message = get_resolution_message(DISK_SPACE_ERROR, "Linux")

        has_free_suggestion = any(term in message.lower() for term in ["free", "delete", "clean", "remove"])

        assert has_free_suggestion or "25" in message, (
            f"Disk space message should suggest freeing space: {message}"
        )

    def test_file_locked_suggests_closing_programs(self):
        """Test: File locked message suggests closing programs."""
        from installer.exit_codes import get_resolution_message, FILE_LOCKED

        message = get_resolution_message(FILE_LOCKED, "Windows")

        has_close_suggestion = any(term in message.lower() for term in ["close", "exit", "quit", "stop"])

        assert has_close_suggestion, (
            f"File locked message should suggest closing programs: {message}"
        )

    def test_permission_denied_linux_suggests_sudo(self):
        """Test: Permission denied on Linux suggests sudo."""
        from installer.exit_codes import get_resolution_message, PERMISSION_DENIED

        message = get_resolution_message(PERMISSION_DENIED, "Linux")

        assert "sudo" in message.lower(), (
            f"Permission denied on Linux should suggest sudo: {message}"
        )

    def test_permission_denied_windows_suggests_administrator(self):
        """Test: Permission denied on Windows suggests Run as Administrator."""
        from installer.exit_codes import get_resolution_message, PERMISSION_DENIED

        message = get_resolution_message(PERMISSION_DENIED, "Windows")

        assert "administrator" in message.lower(), (
            f"Permission denied on Windows should suggest administrator: {message}"
        )


# =============================================================================
# AC#4: Exit Code Integration with Pre-Flight
# =============================================================================


class TestAC4_PreflightIntegration:
    """AC#4: get_exit_code_for_check function maps preflight failures to exit codes."""

    def test_get_exit_code_for_check_function_exists(self):
        """Test: get_exit_code_for_check function exists in module."""
        from installer.exit_codes import get_exit_code_for_check

        assert callable(get_exit_code_for_check), (
            "get_exit_code_for_check must be a callable function"
        )

    def test_disk_space_failure_returns_exit_code_5(self):
        """Test: disk_space check failure returns DISK_SPACE_ERROR (5)."""
        from installer.exit_codes import get_exit_code_for_check, DISK_SPACE_ERROR

        exit_code = get_exit_code_for_check("disk_space")

        assert exit_code == DISK_SPACE_ERROR == 5, (
            f"disk_space failure should return 5, got {exit_code}"
        )

    def test_write_permission_failure_returns_exit_code_2(self):
        """Test: write_permission check failure returns PERMISSION_DENIED (2)."""
        from installer.exit_codes import get_exit_code_for_check, PERMISSION_DENIED

        exit_code = get_exit_code_for_check("write_permission")

        assert exit_code == PERMISSION_DENIED == 2, (
            f"write_permission failure should return 2, got {exit_code}"
        )

    def test_write_permission_on_wsl_returns_exit_code_6(self):
        """Test: write_permission on WSL returns NTFS_PERMISSION (6)."""
        from installer.exit_codes import get_exit_code_for_check, NTFS_PERMISSION

        exit_code = get_exit_code_for_check("write_permission", is_wsl=True)

        assert exit_code == NTFS_PERMISSION == 6, (
            f"write_permission on WSL should return 6, got {exit_code}"
        )

    def test_file_locked_returns_exit_code_7(self):
        """Test: file_locked check failure returns FILE_LOCKED (7)."""
        from installer.exit_codes import get_exit_code_for_check, FILE_LOCKED

        exit_code = get_exit_code_for_check("file_locked")

        assert exit_code == FILE_LOCKED == 7, (
            f"file_locked failure should return 7, got {exit_code}"
        )

    def test_source_audit_failure_returns_exit_code_1(self):
        """Test: source_audit check failure returns MISSING_SOURCE (1)."""
        from installer.exit_codes import get_exit_code_for_check, MISSING_SOURCE

        exit_code = get_exit_code_for_check("source_audit")

        assert exit_code == MISSING_SOURCE == 1, (
            f"source_audit failure should return 1, got {exit_code}"
        )

    def test_unknown_check_returns_permission_denied(self):
        """Test: Unknown check name returns PERMISSION_DENIED (2) as fallback."""
        from installer.exit_codes import get_exit_code_for_check, PERMISSION_DENIED

        exit_code = get_exit_code_for_check("unknown_check")

        assert exit_code == PERMISSION_DENIED == 2, (
            f"Unknown check should return 2 (fallback), got {exit_code}"
        )

    def test_ntfs_permission_returns_exit_code_6(self):
        """Test: ntfs_permission check failure returns NTFS_PERMISSION (6)."""
        from installer.exit_codes import get_exit_code_for_check, NTFS_PERMISSION

        exit_code = get_exit_code_for_check("ntfs_permission")

        assert exit_code == NTFS_PERMISSION == 6, (
            f"ntfs_permission failure should return 6, got {exit_code}"
        )
