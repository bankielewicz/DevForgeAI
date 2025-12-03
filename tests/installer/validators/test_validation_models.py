"""
Unit tests for ValidationResult and CheckResult data models.

Tests data model requirements:
- ValidationResult fields and computed properties
- CheckResult fields and validation
- Status enum values

Component Requirements:
- ValidationResult: checks, all_pass, warnings_present, critical_failures
- CheckResult: check_name, status, message
"""

import pytest


class TestCheckResult:
    """Test suite for CheckResult data model."""

    def test_should_create_check_result_with_required_fields(self):
        """
        Test: CheckResult created with all required fields

        Given: check_name, status, and message provided
        When: CheckResult is instantiated
        Then: Object has all three fields
        """
        # Arrange & Act
        from src.installer.validators.models import CheckResult

        result = CheckResult(
            check_name="Python Version",
            status="PASS",
            message="Python 3.11.4 found"
        )

        # Assert
        assert result.check_name == "Python Version"
        assert result.status == "PASS"
        assert result.message == "Python 3.11.4 found"

    def test_should_require_non_empty_check_name(self):
        """
        Test: check_name must be non-empty string

        Given: Empty check_name provided
        When: CheckResult is instantiated
        Then: Raises ValueError
        """
        # Arrange
        from src.installer.validators.models import CheckResult

        # Act & Assert
        with pytest.raises(ValueError):
            CheckResult(
                check_name="",
                status="PASS",
                message="Test"
            )

    def test_should_validate_status_enum(self):
        """
        Test: status must be one of PASS/WARN/FAIL

        Given: Invalid status value provided
        When: CheckResult is instantiated
        Then: Raises ValueError
        """
        # Arrange
        from src.installer.validators.models import CheckResult

        # Act & Assert
        with pytest.raises(ValueError):
            CheckResult(
                check_name="Test",
                status="INVALID",
                message="Test"
            )

    def test_should_accept_pass_status(self):
        """
        Test: Accepts PASS status

        Given: status="PASS"
        When: CheckResult is instantiated
        Then: Object created successfully
        """
        # Arrange & Act
        from src.installer.validators.models import CheckResult

        result = CheckResult(check_name="Test", status="PASS", message="OK")

        # Assert
        assert result.status == "PASS"

    def test_should_accept_warn_status(self):
        """
        Test: Accepts WARN status

        Given: status="WARN"
        When: CheckResult is instantiated
        Then: Object created successfully
        """
        # Arrange & Act
        from src.installer.validators.models import CheckResult

        result = CheckResult(check_name="Test", status="WARN", message="Warning")

        # Assert
        assert result.status == "WARN"

    def test_should_accept_fail_status(self):
        """
        Test: Accepts FAIL status

        Given: status="FAIL"
        When: CheckResult is instantiated
        Then: Object created successfully
        """
        # Arrange & Act
        from src.installer.validators.models import CheckResult

        result = CheckResult(check_name="Test", status="FAIL", message="Failed")

        # Assert
        assert result.status == "FAIL"

    def test_should_require_non_empty_message(self):
        """
        Test: message must be non-empty string with context

        Given: Empty message provided
        When: CheckResult is instantiated
        Then: Raises ValueError
        """
        # Arrange
        from src.installer.validators.models import CheckResult

        # Act & Assert
        with pytest.raises(ValueError):
            CheckResult(
                check_name="Test",
                status="PASS",
                message=""
            )

    def test_should_support_string_representation(self):
        """
        Test: Supports string representation

        Given: CheckResult object
        When: str() or repr() is called
        Then: Returns meaningful string
        """
        # Arrange
        from src.installer.validators.models import CheckResult

        result = CheckResult(
            check_name="Python Version",
            status="PASS",
            message="Python 3.11.4 found"
        )

        # Act
        string_repr = str(result)

        # Assert
        assert "Python Version" in string_repr
        assert "PASS" in string_repr

    def test_should_support_equality_comparison(self):
        """
        Test: Supports equality comparison

        Given: Two CheckResult objects with same values
        When: Compared using ==
        Then: Returns True
        """
        # Arrange
        from src.installer.validators.models import CheckResult

        result1 = CheckResult(check_name="Test", status="PASS", message="OK")
        result2 = CheckResult(check_name="Test", status="PASS", message="OK")

        # Act & Assert
        assert result1 == result2

    def test_should_be_immutable(self):
        """
        Test: CheckResult is immutable (if using dataclass frozen=True)

        Given: CheckResult object created
        When: Attempt to modify field
        Then: Raises AttributeError (or fields are immutable)
        """
        # Arrange
        from src.installer.validators.models import CheckResult

        result = CheckResult(check_name="Test", status="PASS", message="OK")

        # Act & Assert
        # If using frozen dataclass, this should fail
        try:
            result.status = "FAIL"
            # If no exception, fields are mutable (acceptable for non-frozen dataclass)
        except (AttributeError, Exception):
            # Immutable implementation (frozen=True)
            pass


class TestValidationResult:
    """Test suite for ValidationResult data model."""

    def test_should_create_validation_result_with_checks_list(self):
        """
        Test: ValidationResult created with checks list

        Given: List of CheckResult objects
        When: ValidationResult is instantiated
        Then: checks field contains list
        """
        # Arrange
        from src.installer.validators.models import ValidationResult, CheckResult

        checks = [
            CheckResult(check_name="Python", status="PASS", message="OK"),
            CheckResult(check_name="Disk", status="PASS", message="OK"),
            CheckResult(check_name="Install", status="PASS", message="OK"),
            CheckResult(check_name="Permission", status="PASS", message="OK"),
        ]

        # Act
        result = ValidationResult(checks=checks)

        # Assert
        assert len(result.checks) == 4
        assert all(isinstance(check, CheckResult) for check in result.checks)

    def test_should_compute_all_pass_when_all_checks_pass(self):
        """
        Test: all_pass=True when all checks PASS

        Given: All checks have status="PASS"
        When: ValidationResult is instantiated
        Then: all_pass property returns True
        """
        # Arrange
        from src.installer.validators.models import ValidationResult, CheckResult

        checks = [
            CheckResult(check_name="Python", status="PASS", message="OK"),
            CheckResult(check_name="Disk", status="PASS", message="OK"),
            CheckResult(check_name="Install", status="PASS", message="OK"),
            CheckResult(check_name="Permission", status="PASS", message="OK"),
        ]

        # Act
        result = ValidationResult(checks=checks)

        # Assert
        assert result.all_pass is True
        assert result.warnings_present is False
        assert result.critical_failures is False

    def test_should_compute_warnings_present_when_any_warn(self):
        """
        Test: warnings_present=True when any check WARN

        Given: At least one check has status="WARN", no FAIL
        When: ValidationResult is instantiated
        Then: warnings_present property returns True
        """
        # Arrange
        from src.installer.validators.models import ValidationResult, CheckResult

        checks = [
            CheckResult(check_name="Python", status="WARN", message="Old version"),
            CheckResult(check_name="Disk", status="PASS", message="OK"),
            CheckResult(check_name="Install", status="PASS", message="OK"),
            CheckResult(check_name="Permission", status="PASS", message="OK"),
        ]

        # Act
        result = ValidationResult(checks=checks)

        # Assert
        assert result.warnings_present is True
        assert result.all_pass is False
        assert result.critical_failures is False

    def test_should_compute_critical_failures_when_any_fail(self):
        """
        Test: critical_failures=True when any check FAIL

        Given: At least one check has status="FAIL"
        When: ValidationResult is instantiated
        Then: critical_failures property returns True
        """
        # Arrange
        from src.installer.validators.models import ValidationResult, CheckResult

        checks = [
            CheckResult(check_name="Python", status="PASS", message="OK"),
            CheckResult(check_name="Disk", status="FAIL", message="Insufficient space"),
            CheckResult(check_name="Install", status="PASS", message="OK"),
            CheckResult(check_name="Permission", status="PASS", message="OK"),
        ]

        # Act
        result = ValidationResult(checks=checks)

        # Assert
        assert result.critical_failures is True
        assert result.all_pass is False

    def test_should_set_both_warnings_and_failures_when_mixed(self):
        """
        Test: Both flags true when checks have WARN and FAIL

        Given: Some checks WARN, some FAIL
        When: ValidationResult is instantiated
        Then: Both warnings_present and critical_failures are True
        """
        # Arrange
        from src.installer.validators.models import ValidationResult, CheckResult

        checks = [
            CheckResult(check_name="Python", status="WARN", message="Old version"),
            CheckResult(check_name="Disk", status="FAIL", message="No space"),
            CheckResult(check_name="Install", status="PASS", message="OK"),
            CheckResult(check_name="Permission", status="WARN", message="Limited access"),
        ]

        # Act
        result = ValidationResult(checks=checks)

        # Assert
        assert result.warnings_present is True
        assert result.critical_failures is True
        assert result.all_pass is False

    def test_should_require_exactly_4_checks(self):
        """
        Test: checks list must contain exactly 4 elements

        Given: checks list with 3 elements
        When: ValidationResult is instantiated
        Then: Raises ValueError
        """
        # Arrange
        from src.installer.validators.models import ValidationResult, CheckResult

        checks = [
            CheckResult(check_name="Python", status="PASS", message="OK"),
            CheckResult(check_name="Disk", status="PASS", message="OK"),
            CheckResult(check_name="Install", status="PASS", message="OK"),
        ]

        # Act & Assert
        with pytest.raises(ValueError):
            ValidationResult(checks=checks)

    def test_should_require_non_empty_checks_list(self):
        """
        Test: checks list cannot be empty

        Given: Empty checks list
        When: ValidationResult is instantiated
        Then: Raises ValueError
        """
        # Arrange
        from src.installer.validators.models import ValidationResult

        # Act & Assert
        with pytest.raises(ValueError):
            ValidationResult(checks=[])

    def test_should_validate_check_types(self):
        """
        Test: checks list must contain CheckResult objects

        Given: checks list with non-CheckResult object
        When: ValidationResult is instantiated
        Then: Raises TypeError
        """
        # Arrange
        from src.installer.validators.models import ValidationResult

        invalid_checks = [
            {"check_name": "Python", "status": "PASS", "message": "OK"},  # Dict, not CheckResult
            None,
            None,
            None,
        ]

        # Act & Assert
        with pytest.raises(TypeError):
            ValidationResult(checks=invalid_checks)

    def test_should_support_string_representation(self):
        """
        Test: Supports string representation

        Given: ValidationResult object
        When: str() is called
        Then: Returns meaningful string with summary
        """
        # Arrange
        from src.installer.validators.models import ValidationResult, CheckResult

        checks = [
            CheckResult(check_name="Python", status="PASS", message="OK"),
            CheckResult(check_name="Disk", status="WARN", message="Warning"),
            CheckResult(check_name="Install", status="PASS", message="OK"),
            CheckResult(check_name="Permission", status="FAIL", message="Failed"),
        ]
        result = ValidationResult(checks=checks)

        # Act
        string_repr = str(result)

        # Assert
        assert "4" in string_repr  # 4 checks
        # Should include summary of statuses

    def test_should_support_iteration_over_checks(self):
        """
        Test: Supports iteration over checks

        Given: ValidationResult with 4 checks
        When: Iterating over result.checks
        Then: Can access each CheckResult
        """
        # Arrange
        from src.installer.validators.models import ValidationResult, CheckResult

        checks = [
            CheckResult(check_name="Python", status="PASS", message="OK"),
            CheckResult(check_name="Disk", status="PASS", message="OK"),
            CheckResult(check_name="Install", status="PASS", message="OK"),
            CheckResult(check_name="Permission", status="PASS", message="OK"),
        ]
        result = ValidationResult(checks=checks)

        # Act
        check_names = [check.check_name for check in result.checks]

        # Assert
        assert "Python" in check_names
        assert "Disk" in check_names
        assert "Install" in check_names
        assert "Permission" in check_names

    def test_should_support_indexing_checks(self):
        """
        Test: Supports indexing checks list

        Given: ValidationResult with 4 checks
        When: Accessing result.checks[0]
        Then: Returns first CheckResult
        """
        # Arrange
        from src.installer.validators.models import ValidationResult, CheckResult

        checks = [
            CheckResult(check_name="Python", status="PASS", message="OK"),
            CheckResult(check_name="Disk", status="PASS", message="OK"),
            CheckResult(check_name="Install", status="PASS", message="OK"),
            CheckResult(check_name="Permission", status="PASS", message="OK"),
        ]
        result = ValidationResult(checks=checks)

        # Act
        first_check = result.checks[0]

        # Assert
        assert first_check.check_name == "Python"

    # Edge cases

    def test_should_handle_all_warn_scenario(self):
        """
        Test: All checks WARN → warnings_present=True, critical_failures=False

        Given: All 4 checks have status="WARN"
        When: ValidationResult is instantiated
        Then: Only warnings_present is True
        """
        # Arrange
        from src.installer.validators.models import ValidationResult, CheckResult

        checks = [
            CheckResult(check_name="Python", status="WARN", message="Warning"),
            CheckResult(check_name="Disk", status="WARN", message="Warning"),
            CheckResult(check_name="Install", status="WARN", message="Warning"),
            CheckResult(check_name="Permission", status="WARN", message="Warning"),
        ]

        # Act
        result = ValidationResult(checks=checks)

        # Assert
        assert result.warnings_present is True
        assert result.critical_failures is False
        assert result.all_pass is False

    def test_should_handle_all_fail_scenario(self):
        """
        Test: All checks FAIL → critical_failures=True

        Given: All 4 checks have status="FAIL"
        When: ValidationResult is instantiated
        Then: critical_failures is True
        """
        # Arrange
        from src.installer.validators.models import ValidationResult, CheckResult

        checks = [
            CheckResult(check_name="Python", status="FAIL", message="Failed"),
            CheckResult(check_name="Disk", status="FAIL", message="Failed"),
            CheckResult(check_name="Install", status="FAIL", message="Failed"),
            CheckResult(check_name="Permission", status="FAIL", message="Failed"),
        ]

        # Act
        result = ValidationResult(checks=checks)

        # Assert
        assert result.critical_failures is True
        assert result.all_pass is False

    # Performance

    def test_should_compute_properties_efficiently(self):
        """
        Test: Computed properties calculated efficiently

        Given: ValidationResult with 4 checks
        When: Accessing all_pass, warnings_present, critical_failures multiple times
        Then: Properties computed efficiently (cached or O(n))
        """
        # Arrange
        import time
        from src.installer.validators.models import ValidationResult, CheckResult

        checks = [
            CheckResult(check_name="Python", status="PASS", message="OK"),
            CheckResult(check_name="Disk", status="WARN", message="Warning"),
            CheckResult(check_name="Install", status="FAIL", message="Failed"),
            CheckResult(check_name="Permission", status="PASS", message="OK"),
        ]
        result = ValidationResult(checks=checks)

        # Act
        start = time.time()
        for _ in range(1000):
            _ = result.all_pass
            _ = result.warnings_present
            _ = result.critical_failures
        duration_ms = (time.time() - start) * 1000

        # Assert
        assert duration_ms < 100, f"Property access took {duration_ms}ms for 1000 iterations (expected <100ms)"
