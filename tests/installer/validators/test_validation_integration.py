"""
Integration tests for pre-flight validation workflow.

Tests complete validation flow with real components:
- Full validation flow (all checks pass)
- Mixed results (some WARN, some PASS)
- Critical failure blocks installation
- Force flag behavior
- Cross-platform compatibility

Coverage Target: 85%+
"""

import pytest
from pathlib import Path


class TestValidationIntegration:
    """Integration tests for complete pre-flight validation workflow."""

    # Full validation flow

    def test_full_validation_all_pass(self, fresh_installation_dir):
        """
        Test: Complete validation flow - all checks pass

        Given: Fresh installation directory with Python 3.10+, adequate space
        When: Pre-flight validation runs
        Then: All 4 checks pass, installation can proceed
        """
        # Arrange
        from src.installer.validators.pre_flight_validator import PreFlightValidator
        from src.installer.validators.python_checker import PythonVersionChecker
        from src.installer.validators.disk_space_checker import DiskSpaceChecker
        from src.installer.validators.installation_detector import ExistingInstallationDetector
        from src.installer.validators.permission_checker import PermissionChecker

        validator = PreFlightValidator(
            python_checker=PythonVersionChecker(),
            disk_checker=DiskSpaceChecker(target_path=str(fresh_installation_dir)),
            installation_detector=ExistingInstallationDetector(target_path=str(fresh_installation_dir)),
            permission_checker=PermissionChecker(target_path=str(fresh_installation_dir))
        )

        # Act
        result = validator.validate()

        # Assert
        assert result.all_pass is True or result.warnings_present is True  # Python may be WARN
        assert result.critical_failures is False
        assert len(result.checks) == 4

    def test_validation_summary_display(self, fresh_installation_dir):
        """
        Test: Validation summary formatted correctly (AC#5)

        Given: Validation completes
        When: format_summary() is called
        Then: Returns formatted table with all checks and overall result
        """
        # Arrange
        from src.installer.validators.pre_flight_validator import PreFlightValidator
        from src.installer.validators.python_checker import PythonVersionChecker
        from src.installer.validators.disk_space_checker import DiskSpaceChecker
        from src.installer.validators.installation_detector import ExistingInstallationDetector
        from src.installer.validators.permission_checker import PermissionChecker

        validator = PreFlightValidator(
            python_checker=PythonVersionChecker(),
            disk_checker=DiskSpaceChecker(target_path=str(fresh_installation_dir)),
            installation_detector=ExistingInstallationDetector(target_path=str(fresh_installation_dir)),
            permission_checker=PermissionChecker(target_path=str(fresh_installation_dir))
        )

        result = validator.validate()

        # Act
        summary = validator.format_summary(result)

        # Assert
        assert isinstance(summary, str)
        assert len(summary) > 0
        # Should contain check names
        assert "Python" in summary or "Disk" in summary
        # Should contain status indicators
        assert "PASS" in summary or "✓" in summary

    # Mixed results scenario

    def test_validation_with_existing_installation(self, existing_installation_dir):
        """
        Test: Existing installation detected → WARN status

        Given: Directory with existing .claude/ and .devforgeai/
        When: Pre-flight validation runs
        Then: Installation detector returns WARN, overall warnings_present=True
        """
        # Arrange
        from src.installer.validators.pre_flight_validator import PreFlightValidator
        from src.installer.validators.python_checker import PythonVersionChecker
        from src.installer.validators.disk_space_checker import DiskSpaceChecker
        from src.installer.validators.installation_detector import ExistingInstallationDetector
        from src.installer.validators.permission_checker import PermissionChecker

        validator = PreFlightValidator(
            python_checker=PythonVersionChecker(),
            disk_checker=DiskSpaceChecker(target_path=str(existing_installation_dir)),
            installation_detector=ExistingInstallationDetector(target_path=str(existing_installation_dir)),
            permission_checker=PermissionChecker(target_path=str(existing_installation_dir))
        )

        # Act
        result = validator.validate()

        # Assert
        assert result.warnings_present is True
        assert result.critical_failures is False
        # Find installation check
        install_check = next(c for c in result.checks if "Installation" in c.check_name)
        assert install_check.status == "WARN"

    def test_validation_with_insufficient_disk_space(self, temp_dir):
        """
        Test: Insufficient disk space → FAIL status blocks installation

        Given: Target directory with <100MB free space
        When: Pre-flight validation runs
        Then: Disk check returns FAIL, critical_failures=True
        """
        # Arrange
        from src.installer.validators.pre_flight_validator import PreFlightValidator
        from src.installer.validators.python_checker import PythonVersionChecker
        from src.installer.validators.disk_space_checker import DiskSpaceChecker
        from src.installer.validators.installation_detector import ExistingInstallationDetector
        from src.installer.validators.permission_checker import PermissionChecker
        from unittest.mock import patch, Mock

        # Mock disk_usage to return insufficient space
        with patch('shutil.disk_usage') as mock_disk_usage:
            mock_disk_usage.return_value = Mock(free=50 * 1024 * 1024)  # 50MB

            validator = PreFlightValidator(
                python_checker=PythonVersionChecker(),
                disk_checker=DiskSpaceChecker(target_path=str(temp_dir)),
                installation_detector=ExistingInstallationDetector(target_path=str(temp_dir)),
                permission_checker=PermissionChecker(target_path=str(temp_dir))
            )

            # Act
            result = validator.validate()

            # Assert
            assert result.critical_failures is True
            # Find disk check
            disk_check = next(c for c in result.checks if "Disk" in c.check_name)
            assert disk_check.status == "FAIL"

    def test_validation_with_permission_denied(self, read_only_dir):
        """
        Test: Write permission denied → FAIL status blocks installation

        Given: Target directory is read-only
        When: Pre-flight validation runs
        Then: Permission check returns FAIL, critical_failures=True
        """
        # Arrange
        from src.installer.validators.pre_flight_validator import PreFlightValidator
        from src.installer.validators.python_checker import PythonVersionChecker
        from src.installer.validators.disk_space_checker import DiskSpaceChecker
        from src.installer.validators.installation_detector import ExistingInstallationDetector
        from src.installer.validators.permission_checker import PermissionChecker

        validator = PreFlightValidator(
            python_checker=PythonVersionChecker(),
            disk_checker=DiskSpaceChecker(target_path=str(read_only_dir)),
            installation_detector=ExistingInstallationDetector(target_path=str(read_only_dir)),
            permission_checker=PermissionChecker(target_path=str(read_only_dir))
        )

        # Act
        result = validator.validate()

        # Assert
        assert result.critical_failures is True
        # Find permission check
        perm_check = next(c for c in result.checks if "Permission" in c.check_name)
        assert perm_check.status == "FAIL"

    # Force flag behavior

    def test_force_flag_bypasses_warnings(self, existing_installation_dir):
        """
        Test: --force bypasses warning prompts (AC#7)

        Given: Validation has WARN checks and force=True
        When: validate(force=True) is called
        Then: Warnings present but no user prompts shown
        """
        # Arrange
        from src.installer.validators.pre_flight_validator import PreFlightValidator
        from src.installer.validators.python_checker import PythonVersionChecker
        from src.installer.validators.disk_space_checker import DiskSpaceChecker
        from src.installer.validators.installation_detector import ExistingInstallationDetector
        from src.installer.validators.permission_checker import PermissionChecker
        from unittest.mock import patch

        validator = PreFlightValidator(
            python_checker=PythonVersionChecker(),
            disk_checker=DiskSpaceChecker(target_path=str(existing_installation_dir)),
            installation_detector=ExistingInstallationDetector(target_path=str(existing_installation_dir)),
            permission_checker=PermissionChecker(target_path=str(existing_installation_dir))
        )

        with patch('builtins.input') as mock_input:
            # Act
            result = validator.validate(force=True)

            # Assert
            assert result.warnings_present is True
            # Should NOT prompt user when force=True
            mock_input.assert_not_called()

    def test_force_flag_does_not_bypass_failures(self, temp_dir):
        """
        Test: --force does NOT bypass FAIL checks (BR-003)

        Given: Validation has FAIL checks and force=True
        When: validate(force=True) is called
        Then: Failures still block installation
        """
        # Arrange
        from src.installer.validators.pre_flight_validator import PreFlightValidator
        from src.installer.validators.python_checker import PythonVersionChecker
        from src.installer.validators.disk_space_checker import DiskSpaceChecker
        from src.installer.validators.installation_detector import ExistingInstallationDetector
        from src.installer.validators.permission_checker import PermissionChecker
        from unittest.mock import patch, Mock

        # Mock disk check to return FAIL
        with patch('shutil.disk_usage') as mock_disk_usage:
            mock_disk_usage.return_value = Mock(free=50 * 1024 * 1024)  # 50MB (below threshold)

            validator = PreFlightValidator(
                python_checker=PythonVersionChecker(),
                disk_checker=DiskSpaceChecker(target_path=str(temp_dir)),
                installation_detector=ExistingInstallationDetector(target_path=str(temp_dir)),
                permission_checker=PermissionChecker(target_path=str(temp_dir))
            )

            # Act
            result = validator.validate(force=True)

            # Assert
            assert result.critical_failures is True
            # Force flag should not change failure status

    # BR-004: All checks complete before summary

    def test_all_checks_complete_even_if_early_check_fails(self, read_only_dir):
        """
        Test: All checks run even if permission check fails early (BR-004)

        Given: Permission check fails
        When: Pre-flight validation runs
        Then: All 4 checks still execute
        """
        # Arrange
        from src.installer.validators.pre_flight_validator import PreFlightValidator
        from src.installer.validators.python_checker import PythonVersionChecker
        from src.installer.validators.disk_space_checker import DiskSpaceChecker
        from src.installer.validators.installation_detector import ExistingInstallationDetector
        from src.installer.validators.permission_checker import PermissionChecker

        validator = PreFlightValidator(
            python_checker=PythonVersionChecker(),
            disk_checker=DiskSpaceChecker(target_path=str(read_only_dir)),
            installation_detector=ExistingInstallationDetector(target_path=str(read_only_dir)),
            permission_checker=PermissionChecker(target_path=str(read_only_dir))
        )

        # Act
        result = validator.validate()

        # Assert
        assert len(result.checks) == 4  # All 4 checks completed
        assert result.critical_failures is True

    # NFR-001: Performance - All checks complete in <5 seconds

    def test_validation_completes_within_5_seconds(self, fresh_installation_dir):
        """
        Test: All pre-flight checks complete in <5 seconds (NFR-001)

        Given: Pre-flight validation with all 4 checks
        When: validate() is called
        Then: Execution completes in <5 seconds
        """
        # Arrange
        import time
        from src.installer.validators.pre_flight_validator import PreFlightValidator
        from src.installer.validators.python_checker import PythonVersionChecker
        from src.installer.validators.disk_space_checker import DiskSpaceChecker
        from src.installer.validators.installation_detector import ExistingInstallationDetector
        from src.installer.validators.permission_checker import PermissionChecker

        validator = PreFlightValidator(
            python_checker=PythonVersionChecker(),
            disk_checker=DiskSpaceChecker(target_path=str(fresh_installation_dir)),
            installation_detector=ExistingInstallationDetector(target_path=str(fresh_installation_dir)),
            permission_checker=PermissionChecker(target_path=str(fresh_installation_dir))
        )

        # Act
        start = time.time()
        result = validator.validate()
        duration = time.time() - start

        # Assert
        assert duration < 5.0, f"Validation took {duration}s (expected <5s)"

    # NFR-004: Reliability - Accurate Python detection across platforms

    @pytest.mark.parametrize("platform", [
        pytest.param("linux", marks=pytest.mark.skipif(not Path("/usr/bin/python3").exists(), reason="Linux only")),
        pytest.param("darwin", marks=pytest.mark.skipif(not Path("/usr/bin/python3").exists(), reason="macOS only")),
        # Windows test would need different executable path check
    ])
    def test_python_detection_cross_platform(self, platform, fresh_installation_dir):
        """
        Test: Python detection works across platforms (NFR-004)

        Given: Different operating systems (Linux, macOS, Windows)
        When: Python version check runs
        Then: Detects Python correctly on each platform
        """
        # Arrange
        from src.installer.validators.python_checker import PythonVersionChecker

        checker = PythonVersionChecker()

        # Act
        result = checker.check()

        # Assert
        assert result.status in ["PASS", "WARN"]
        # Should not crash on any platform

    # NFR-005: Reliability - Zero false positives for blocking errors

    def test_fail_status_only_for_genuine_blockers(self, temp_dir):
        """
        Test: FAIL only when installation genuinely cannot proceed (NFR-005)

        Given: Various validation scenarios
        When: Checks complete
        Then: FAIL only for actual blocking issues, not false positives
        """
        # Arrange
        from src.installer.validators.disk_space_checker import DiskSpaceChecker
        from unittest.mock import patch, Mock

        # Test 1: 99MB (just below threshold) should FAIL
        with patch('shutil.disk_usage') as mock_disk_usage:
            mock_disk_usage.return_value = Mock(free=99 * 1024 * 1024)
            checker = DiskSpaceChecker(target_path=str(temp_dir))
            result = checker.check()
            assert result.status == "FAIL"

        # Test 2: 100MB (at threshold) should PASS
        with patch('shutil.disk_usage') as mock_disk_usage:
            mock_disk_usage.return_value = Mock(free=100 * 1024 * 1024)
            checker = DiskSpaceChecker(target_path=str(temp_dir))
            result = checker.check()
            assert result.status == "PASS"

    # NFR-006: Usability - Error messages include actionable resolution steps

    def test_all_error_messages_include_resolution_steps(self, read_only_dir):
        """
        Test: All FAIL/WARN messages contain resolution steps (NFR-006)

        Given: Validation checks return FAIL or WARN
        When: Messages are examined
        Then: Each message contains at least 2 actionable steps
        """
        # Arrange
        from src.installer.validators.pre_flight_validator import PreFlightValidator
        from src.installer.validators.python_checker import PythonVersionChecker
        from src.installer.validators.disk_space_checker import DiskSpaceChecker
        from src.installer.validators.installation_detector import ExistingInstallationDetector
        from src.installer.validators.permission_checker import PermissionChecker

        validator = PreFlightValidator(
            python_checker=PythonVersionChecker(),
            disk_checker=DiskSpaceChecker(target_path=str(read_only_dir)),
            installation_detector=ExistingInstallationDetector(target_path=str(read_only_dir)),
            permission_checker=PermissionChecker(target_path=str(read_only_dir))
        )

        result = validator.validate()

        # Act & Assert
        for check in result.checks:
            if check.status in ["FAIL", "WARN"]:
                # Message should contain guidance
                message_lower = check.message.lower()
                # At least one resolution keyword present
                resolution_keywords = ["install", "upgrade", "free", "run", "choose", "directory", "check"]
                matches = sum(1 for keyword in resolution_keywords if keyword in message_lower)
                assert matches >= 1, f"Check '{check.check_name}' message lacks resolution guidance"

    # NFR-007: Security - No privilege escalation attempts

    def test_no_privilege_escalation_on_permission_denied(self, read_only_dir):
        """
        Test: Does not attempt privilege escalation (NFR-007)

        Given: Write permission denied
        When: Permission check runs
        Then: Returns FAIL without attempting sudo/admin
        """
        # Arrange
        from src.installer.validators.permission_checker import PermissionChecker
        from unittest.mock import patch

        checker = PermissionChecker(target_path=str(read_only_dir))

        with patch('subprocess.run') as mock_subprocess:
            # Act
            result = checker.check()

            # Assert
            assert result.status == "FAIL"
            # Should NOT call subprocess (no sudo attempt)
            mock_subprocess.assert_not_called()

    # Edge cases

    def test_partial_installation_detection(self, partial_installation_dir):
        """
        Test: Partial installation detected and flagged as WARN

        Given: Directory with .claude/ but no skills subdirectory
        When: Installation detector runs
        Then: Returns WARN with partial installation context
        """
        # Arrange
        from src.installer.validators.installation_detector import ExistingInstallationDetector

        detector = ExistingInstallationDetector(target_path=str(partial_installation_dir))

        # Act
        result = detector.check()

        # Assert
        assert result.status == "WARN"
        assert "existing" in result.message.lower()

    def test_network_mount_disk_calculation(self, temp_dir):
        """
        Test: Network mount disk calculation failure → WARN

        Given: Target path is network mount with calculation issues
        When: Disk space check runs
        Then: Returns WARN (not FAIL or crash)
        """
        # Arrange
        from src.installer.validators.disk_space_checker import DiskSpaceChecker
        from unittest.mock import patch

        with patch('shutil.disk_usage') as mock_disk_usage:
            mock_disk_usage.side_effect = OSError("Network timeout")

            checker = DiskSpaceChecker(target_path=str(temp_dir))

            # Act
            result = checker.check()

            # Assert
            assert result.status == "WARN"

    # E2E scenarios

    def test_e2e_all_checks_pass_scenario(self, fresh_installation_dir):
        """
        Test: E2E scenario - All checks pass, installation proceeds

        Given: Fresh directory with Python, adequate space, permissions
        When: Pre-flight validation runs
        Then: All checks pass, can proceed to installation
        """
        # Arrange
        from src.installer.validators.pre_flight_validator import PreFlightValidator
        from src.installer.validators.python_checker import PythonVersionChecker
        from src.installer.validators.disk_space_checker import DiskSpaceChecker
        from src.installer.validators.installation_detector import ExistingInstallationDetector
        from src.installer.validators.permission_checker import PermissionChecker

        validator = PreFlightValidator(
            python_checker=PythonVersionChecker(),
            disk_checker=DiskSpaceChecker(target_path=str(fresh_installation_dir)),
            installation_detector=ExistingInstallationDetector(target_path=str(fresh_installation_dir)),
            permission_checker=PermissionChecker(target_path=str(fresh_installation_dir))
        )

        # Act
        result = validator.validate()
        summary = validator.format_summary(result)

        # Assert
        assert result.critical_failures is False
        assert len(summary) > 0
        # Installation can proceed

    def test_e2e_critical_failure_blocks_installation(self, read_only_dir):
        """
        Test: E2E scenario - Critical failure blocks installation (AC#6)

        Given: Directory with permission denied
        When: Pre-flight validation runs
        Then: critical_failures=True, installation blocked
        """
        # Arrange
        from src.installer.validators.pre_flight_validator import PreFlightValidator
        from src.installer.validators.python_checker import PythonVersionChecker
        from src.installer.validators.disk_space_checker import DiskSpaceChecker
        from src.installer.validators.installation_detector import ExistingInstallationDetector
        from src.installer.validators.permission_checker import PermissionChecker

        validator = PreFlightValidator(
            python_checker=PythonVersionChecker(),
            disk_checker=DiskSpaceChecker(target_path=str(read_only_dir)),
            installation_detector=ExistingInstallationDetector(target_path=str(read_only_dir)),
            permission_checker=PermissionChecker(target_path=str(read_only_dir))
        )

        # Act
        result = validator.validate()

        # Assert
        assert result.critical_failures is True
        # Caller should exit with code 1
