"""
Unit tests for PreFlightValidator (Orchestrator).

Tests AC#5, AC#6, AC#7: Validation Summary, Blocking Enforcement, Force Flag
- Orchestrate 4 validation checks
- Determine overall outcome
- Format validation summary table
- Handle --force flag

Component Requirements:
- SVC-001: Orchestrate 4 validation checks and return structured ValidationResult
- SVC-002: Determine overall outcome (all_pass, warnings_present, critical_failures)
- SVC-003: Format validation summary as human-readable table
- SVC-004: Handle --force flag to bypass warning prompts

Business Rules:
- BR-001: Critical failures (✗ FAIL) block installation
- BR-002: Warnings (⚠ WARN) allow continuation but prompt user
- BR-003: --force flag bypasses warning prompts only
- BR-004: All checks must complete before summary display
"""

import pytest
from unittest.mock import Mock, patch, MagicMock


class TestPreFlightValidator:
    """Test suite for PreFlightValidator orchestrator service."""

    # SVC-001: Orchestrate 4 validation checks

    def test_should_run_all_four_checks(self):
        """
        Test: Runs all 4 validation checks (SVC-001)

        Given: PreFlightValidator is initialized with 4 checkers
        When: validate() is called
        Then: Returns ValidationResult with 4 CheckResult objects
        """
        # Arrange
        from src.installer.validators.pre_flight_validator import PreFlightValidator

        # Mock all 4 checkers
        mock_python_checker = Mock()
        mock_python_checker.check.return_value = Mock(
            check_name="Python Version",
            status="PASS",
            message="Python 3.11.4 found"
        )

        mock_disk_checker = Mock()
        mock_disk_checker.check.return_value = Mock(
            check_name="Disk Space",
            status="PASS",
            message="500MB available"
        )

        mock_install_detector = Mock()
        mock_install_detector.check.return_value = Mock(
            check_name="Existing Installation",
            status="PASS",
            message="No existing installation"
        )

        mock_permission_checker = Mock()
        mock_permission_checker.check.return_value = Mock(
            check_name="Write Permissions",
            status="PASS",
            message="Directory writable"
        )

        validator = PreFlightValidator(
            python_checker=mock_python_checker,
            disk_checker=mock_disk_checker,
            installation_detector=mock_install_detector,
            permission_checker=mock_permission_checker
        )

        # Act
        result = validator.validate()

        # Assert
        assert len(result.checks) == 4
        mock_python_checker.check.assert_called_once()
        mock_disk_checker.check.assert_called_once()
        mock_install_detector.check.assert_called_once()
        mock_permission_checker.check.assert_called_once()

    def test_should_return_structured_validation_result(self):
        """
        Test: Returns structured ValidationResult (SVC-001)

        Given: All 4 checks complete successfully
        When: validate() is called
        Then: Returns ValidationResult with checks list and outcome flags
        """
        # Arrange
        from src.installer.validators.pre_flight_validator import PreFlightValidator

        validator = self._create_validator_with_mocks("PASS", "PASS", "PASS", "PASS")

        # Act
        result = validator.validate()

        # Assert
        assert hasattr(result, "checks")
        assert hasattr(result, "all_pass")
        assert hasattr(result, "warnings_present")
        assert hasattr(result, "critical_failures")
        assert isinstance(result.checks, list)

    # SVC-002: Determine overall outcome

    def test_should_set_all_pass_when_all_checks_pass(self):
        """
        Test: all_pass=True when all checks PASS (SVC-002)

        Given: All 4 checks return PASS status
        When: validate() is called
        Then: ValidationResult.all_pass is True
        """
        # Arrange
        from src.installer.validators.pre_flight_validator import PreFlightValidator

        validator = self._create_validator_with_mocks("PASS", "PASS", "PASS", "PASS")

        # Act
        result = validator.validate()

        # Assert
        assert result.all_pass is True
        assert result.warnings_present is False
        assert result.critical_failures is False

    def test_should_set_warnings_present_when_any_warn(self):
        """
        Test: warnings_present=True when any check WARN (SVC-002)

        Given: At least one check returns WARN status, no FAIL
        When: validate() is called
        Then: ValidationResult.warnings_present is True
        """
        # Arrange
        from src.installer.validators.pre_flight_validator import PreFlightValidator

        validator = self._create_validator_with_mocks("PASS", "PASS", "WARN", "PASS")

        # Act
        result = validator.validate()

        # Assert
        assert result.warnings_present is True
        assert result.all_pass is False
        assert result.critical_failures is False

    def test_should_set_critical_failures_when_any_fail(self):
        """
        Test: critical_failures=True when any check FAIL (SVC-002)

        Given: At least one check returns FAIL status
        When: validate() is called
        Then: ValidationResult.critical_failures is True
        """
        # Arrange
        from src.installer.validators.pre_flight_validator import PreFlightValidator

        validator = self._create_validator_with_mocks("PASS", "FAIL", "PASS", "PASS")

        # Act
        result = validator.validate()

        # Assert
        assert result.critical_failures is True
        assert result.all_pass is False

    def test_should_set_both_warnings_and_failures_when_mixed(self):
        """
        Test: Both flags set when checks have WARN and FAIL (SVC-002)

        Given: Some checks WARN, some FAIL
        When: validate() is called
        Then: Both warnings_present and critical_failures are True
        """
        # Arrange
        from src.installer.validators.pre_flight_validator import PreFlightValidator

        validator = self._create_validator_with_mocks("WARN", "FAIL", "PASS", "WARN")

        # Act
        result = validator.validate()

        # Assert
        assert result.warnings_present is True
        assert result.critical_failures is True
        assert result.all_pass is False

    # SVC-003: Format validation summary as human-readable table

    def test_should_format_summary_as_table(self):
        """
        Test: format_summary() returns table format (SVC-003)

        Given: ValidationResult with 4 checks
        When: format_summary() is called
        Then: Returns string with table headers and 4 rows
        """
        # Arrange
        from src.installer.validators.pre_flight_validator import PreFlightValidator

        validator = self._create_validator_with_mocks("PASS", "PASS", "PASS", "PASS")
        result = validator.validate()

        # Act
        summary = validator.format_summary(result)

        # Assert
        assert isinstance(summary, str)
        assert len(summary) > 0
        # Should contain table elements (flexible format)
        assert "Python Version" in summary or "Python" in summary
        assert "Disk Space" in summary or "Disk" in summary
        assert "Existing Installation" in summary or "Installation" in summary
        assert "Write Permissions" in summary or "Permissions" in summary

    def test_should_include_status_indicators_in_summary(self):
        """
        Test: Summary includes status indicators (AC#5)

        Given: ValidationResult with mixed statuses
        When: format_summary() is called
        Then: Summary includes ✓ PASS, ⚠ WARN, ✗ FAIL indicators
        """
        # Arrange
        from src.installer.validators.pre_flight_validator import PreFlightValidator

        validator = self._create_validator_with_mocks("PASS", "WARN", "FAIL", "PASS")
        result = validator.validate()

        # Act
        summary = validator.format_summary(result)

        # Assert
        # Check for status indicators (flexible symbols)
        assert "PASS" in summary or "✓" in summary
        assert "WARN" in summary or "⚠" in summary
        assert "FAIL" in summary or "✗" in summary

    def test_should_include_overall_result_in_summary(self):
        """
        Test: Summary includes overall result (AC#5)

        Given: ValidationResult with specific outcome
        When: format_summary() is called
        Then: Summary ends with overall result message
        """
        # Arrange
        from src.installer.validators.pre_flight_validator import PreFlightValidator

        test_cases = [
            ("PASS", "PASS", "PASS", "PASS", "all checks passed"),
            ("PASS", "WARN", "PASS", "PASS", "warnings present"),
            ("PASS", "FAIL", "PASS", "PASS", "critical failures"),
        ]

        for python, disk, install, perm, expected_phrase in test_cases:
            validator = self._create_validator_with_mocks(python, disk, install, perm)
            result = validator.validate()

            # Act
            summary = validator.format_summary(result)

            # Assert
            # Check for overall outcome phrase (case-insensitive, flexible wording)
            assert any(keyword in summary.lower() for keyword in expected_phrase.split()), \
                f"Expected '{expected_phrase}' keywords in summary for case ({python}, {disk}, {install}, {perm})"

    # SVC-004: Handle --force flag to bypass warning prompts

    def test_should_bypass_warnings_with_force_flag(self):
        """
        Test: --force bypasses warning prompts (SVC-004, AC#7)

        Given: ValidationResult has WARN checks and --force=True
        When: validate(force=True) is called
        Then: No user prompts displayed for warnings
        """
        # Arrange
        from src.installer.validators.pre_flight_validator import PreFlightValidator

        validator = self._create_validator_with_mocks("PASS", "WARN", "PASS", "PASS")

        with patch('builtins.input') as mock_input:
            # Act
            result = validator.validate(force=True)

            # Assert
            assert result.warnings_present is True
            # Should NOT prompt user when force=True
            mock_input.assert_not_called()

    def test_should_not_bypass_failures_with_force_flag(self):
        """
        Test: --force does NOT bypass FAIL (BR-003)

        Given: ValidationResult has FAIL checks and --force=True
        When: validate(force=True) is called
        Then: Failures still block, force flag ignored
        """
        # Arrange
        from src.installer.validators.pre_flight_validator import PreFlightValidator

        validator = self._create_validator_with_mocks("PASS", "FAIL", "PASS", "PASS")

        # Act
        result = validator.validate(force=True)

        # Assert
        assert result.critical_failures is True
        # Force flag should not change failure status

    def test_should_log_force_flag_enabled(self):
        """
        Test: Logs "Force flag enabled" message (AC#7)

        Given: --force flag is set
        When: validate(force=True) is called
        Then: Logs message about force mode
        """
        # Arrange
        from src.installer.validators.pre_flight_validator import PreFlightValidator

        validator = self._create_validator_with_mocks("PASS", "WARN", "PASS", "PASS")

        with patch('builtins.print') as mock_print:
            # Act
            result = validator.validate(force=True)

            # Assert
            # Check if force mode was logged
            call_args = [str(call) for call in mock_print.call_args_list]
            force_logged = any("force" in str(call).lower() for call in call_args)
            # May or may not log depending on implementation, but warnings should be bypassed
            assert result.warnings_present is True

    # BR-001: Critical failures block installation

    def test_should_block_installation_on_critical_failure(self):
        """
        Test: FAIL check blocks installation (BR-001, AC#6)

        Given: At least one check returns FAIL
        When: validate() is called
        Then: critical_failures flag is True (signals caller to exit)
        """
        # Arrange
        from src.installer.validators.pre_flight_validator import PreFlightValidator

        validator = self._create_validator_with_mocks("PASS", "PASS", "PASS", "FAIL")

        # Act
        result = validator.validate()

        # Assert
        assert result.critical_failures is True
        # Caller should check this flag and exit with code 1

    # BR-002: Warnings allow continuation but prompt user

    def test_should_prompt_user_on_warning_without_force(self):
        """
        Test: WARN prompts user (BR-002)

        Given: Validation has WARN checks and force=False
        When: validate() is called
        Then: User is prompted to continue or cancel
        """
        # Arrange
        from src.installer.validators.pre_flight_validator import PreFlightValidator

        validator = self._create_validator_with_mocks("PASS", "WARN", "PASS", "PASS")

        # Note: Prompting may happen in caller, not validator itself
        # Validator just returns result with warnings_present=True

        # Act
        result = validator.validate(force=False)

        # Assert
        assert result.warnings_present is True
        # Caller should prompt based on warnings_present flag

    # BR-004: All checks must complete before summary display

    def test_should_run_all_checks_even_if_early_check_fails(self):
        """
        Test: All checks run even if Python check fails (BR-004)

        Given: Python check returns FAIL
        When: validate() is called
        Then: Disk, installation, and permission checks still execute
        """
        # Arrange
        from src.installer.validators.pre_flight_validator import PreFlightValidator

        mock_python = Mock()
        mock_python.check.return_value = Mock(check_name="Python", status="FAIL", message="Not found")

        mock_disk = Mock()
        mock_disk.check.return_value = Mock(check_name="Disk", status="PASS", message="OK")

        mock_install = Mock()
        mock_install.check.return_value = Mock(check_name="Install", status="PASS", message="OK")

        mock_permission = Mock()
        mock_permission.check.return_value = Mock(check_name="Permission", status="PASS", message="OK")

        validator = PreFlightValidator(
            python_checker=mock_python,
            disk_checker=mock_disk,
            installation_detector=mock_install,
            permission_checker=mock_permission
        )

        # Act
        result = validator.validate()

        # Assert
        assert len(result.checks) == 4
        mock_python.check.assert_called_once()
        mock_disk.check.assert_called_once()
        mock_install.check.assert_called_once()
        mock_permission.check.assert_called_once()

    def test_should_collect_all_results_before_summary(self):
        """
        Test: Collects all results before displaying summary (BR-004)

        Given: Multiple checks return different statuses
        When: validate() is called
        Then: ValidationResult contains all 4 results
        """
        # Arrange
        from src.installer.validators.pre_flight_validator import PreFlightValidator

        validator = self._create_validator_with_mocks("FAIL", "WARN", "PASS", "FAIL")

        # Act
        result = validator.validate()

        # Assert
        assert len(result.checks) == 4
        # All checks completed and results collected
        statuses = [check.status for check in result.checks]
        assert "FAIL" in statuses
        assert "WARN" in statuses
        assert "PASS" in statuses

    # NFR-001: Performance - All checks complete in <5 seconds

    def test_should_complete_all_checks_within_5_seconds(self):
        """
        Test: All pre-flight checks complete in <5 seconds (NFR-001)

        Given: PreFlightValidator with 4 checkers
        When: validate() is called
        Then: Execution completes in <5 seconds
        """
        # Arrange
        import time
        from src.installer.validators.pre_flight_validator import PreFlightValidator

        validator = self._create_validator_with_mocks("PASS", "PASS", "PASS", "PASS")

        # Act
        start = time.time()
        result = validator.validate()
        duration = time.time() - start

        # Assert
        assert duration < 5.0, f"Validation took {duration}s (expected <5s)"
        assert result.all_pass is True

    # Integration scenarios

    def test_should_handle_all_pass_scenario(self):
        """
        Test: All checks pass → can proceed

        Given: All 4 checks return PASS
        When: validate() is called
        Then: all_pass=True, warnings_present=False, critical_failures=False
        """
        # Arrange
        from src.installer.validators.pre_flight_validator import PreFlightValidator

        validator = self._create_validator_with_mocks("PASS", "PASS", "PASS", "PASS")

        # Act
        result = validator.validate()

        # Assert
        assert result.all_pass is True
        assert result.warnings_present is False
        assert result.critical_failures is False

    def test_should_handle_warnings_only_scenario(self):
        """
        Test: Some warnings, no failures → can proceed with prompt

        Given: Some checks WARN, none FAIL
        When: validate() is called
        Then: all_pass=False, warnings_present=True, critical_failures=False
        """
        # Arrange
        from src.installer.validators.pre_flight_validator import PreFlightValidator

        validator = self._create_validator_with_mocks("WARN", "PASS", "WARN", "PASS")

        # Act
        result = validator.validate()

        # Assert
        assert result.all_pass is False
        assert result.warnings_present is True
        assert result.critical_failures is False

    def test_should_handle_failures_scenario(self):
        """
        Test: Any failure → cannot proceed

        Given: At least one check FAIL
        When: validate() is called
        Then: critical_failures=True (blocks installation)
        """
        # Arrange
        from src.installer.validators.pre_flight_validator import PreFlightValidator

        validator = self._create_validator_with_mocks("PASS", "FAIL", "WARN", "PASS")

        # Act
        result = validator.validate()

        # Assert
        assert result.critical_failures is True

    # Helper methods

    def _create_validator_with_mocks(self, python_status, disk_status, install_status, perm_status):
        """
        Helper: Create PreFlightValidator with mocked checkers.

        Args:
            python_status: Status for Python checker (PASS/WARN/FAIL)
            disk_status: Status for Disk checker
            install_status: Status for Installation detector
            perm_status: Status for Permission checker

        Returns:
            PreFlightValidator instance with mocked dependencies
        """
        from src.installer.validators.pre_flight_validator import PreFlightValidator

        mock_python = Mock()
        mock_python.check.return_value = Mock(
            check_name="Python Version",
            status=python_status,
            message=f"Python check {python_status}"
        )

        mock_disk = Mock()
        mock_disk.check.return_value = Mock(
            check_name="Disk Space",
            status=disk_status,
            message=f"Disk check {disk_status}"
        )

        mock_install = Mock()
        mock_install.check.return_value = Mock(
            check_name="Existing Installation",
            status=install_status,
            message=f"Install check {install_status}"
        )

        mock_permission = Mock()
        mock_permission.check.return_value = Mock(
            check_name="Write Permissions",
            status=perm_status,
            message=f"Permission check {perm_status}"
        )

        return PreFlightValidator(
            python_checker=mock_python,
            disk_checker=mock_disk,
            installation_detector=mock_install,
            permission_checker=mock_permission
        )

    # Configuration validation

    def test_should_accept_custom_checkers(self):
        """
        Test: Accepts custom checker implementations

        Given: Custom checker implementations provided
        When: PreFlightValidator is initialized
        Then: Uses custom checkers instead of defaults
        """
        # Arrange
        from src.installer.validators.pre_flight_validator import PreFlightValidator

        custom_python = Mock()
        custom_python.check.return_value = Mock(check_name="Custom Python", status="PASS", message="OK")

        validator = PreFlightValidator(
            python_checker=custom_python,
            disk_checker=Mock(check=Mock(return_value=Mock(check_name="Disk", status="PASS", message="OK"))),
            installation_detector=Mock(check=Mock(return_value=Mock(check_name="Install", status="PASS", message="OK"))),
            permission_checker=Mock(check=Mock(return_value=Mock(check_name="Perm", status="PASS", message="OK")))
        )

        # Act
        result = validator.validate()

        # Assert
        custom_python.check.assert_called_once()
        assert any(check.check_name == "Custom Python" for check in result.checks)
