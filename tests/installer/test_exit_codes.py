"""
STORY-074: Unit tests for ExitCodes constants.

Tests that all 5 exit codes are defined with correct values.
All tests follow TDD Red phase - they should FAIL until implementation exists.

Coverage Target: 95%+
"""

import pytest


class TestExitCodeConstants:
    """Test all 5 exit code constants are defined (AC#6)."""

    def test_success_constant_equals_0(self):
        """
        Test: SUCCESS constant equals 0.

        Given: ExitCodes module is imported
        When: SUCCESS constant is accessed
        Then: Value is 0
        """
        # Arrange & Act
        from installer.exit_codes import ExitCodes

        # Assert
        assert ExitCodes.SUCCESS == 0

    def test_missing_source_constant_equals_1(self):
        """
        Test: MISSING_SOURCE constant equals 1.

        Given: ExitCodes module is imported
        When: MISSING_SOURCE constant is accessed
        Then: Value is 1
        """
        # Arrange & Act
        from installer.exit_codes import ExitCodes

        # Assert
        assert ExitCodes.MISSING_SOURCE == 1

    def test_permission_denied_constant_equals_2(self):
        """
        Test: PERMISSION_DENIED constant equals 2.

        Given: ExitCodes module is imported
        When: PERMISSION_DENIED constant is accessed
        Then: Value is 2
        """
        # Arrange & Act
        from installer.exit_codes import ExitCodes

        # Assert
        assert ExitCodes.PERMISSION_DENIED == 2

    def test_rollback_occurred_constant_equals_3(self):
        """
        Test: ROLLBACK_OCCURRED constant equals 3.

        Given: ExitCodes module is imported
        When: ROLLBACK_OCCURRED constant is accessed
        Then: Value is 3
        """
        # Arrange & Act
        from installer.exit_codes import ExitCodes

        # Assert
        assert ExitCodes.ROLLBACK_OCCURRED == 3

    def test_validation_failed_constant_equals_4(self):
        """
        Test: VALIDATION_FAILED constant equals 4.

        Given: ExitCodes module is imported
        When: VALIDATION_FAILED constant is accessed
        Then: Value is 4
        """
        # Arrange & Act
        from installer.exit_codes import ExitCodes

        # Assert
        assert ExitCodes.VALIDATION_FAILED == 4


class TestExitCodeUniqueness:
    """Test that all exit codes are unique (no duplicates)."""

    def test_all_exit_codes_are_unique(self):
        """
        Test: All 5 exit codes have unique values (no duplicates).

        Given: ExitCodes module is imported
        When: All constants are accessed
        Then: No duplicate values exist
        """
        # Arrange & Act
        from installer.exit_codes import ExitCodes

        exit_codes = [
            ExitCodes.SUCCESS,
            ExitCodes.MISSING_SOURCE,
            ExitCodes.PERMISSION_DENIED,
            ExitCodes.ROLLBACK_OCCURRED,
            ExitCodes.VALIDATION_FAILED,
        ]

        # Assert
        assert len(exit_codes) == len(set(exit_codes)), "Exit codes contain duplicates"


class TestExitCodeTypes:
    """Test that all exit codes are integers."""

    def test_all_exit_codes_are_integers(self):
        """
        Test: All exit code constants are integers.

        Given: ExitCodes module is imported
        When: All constants are accessed
        Then: All values are of type int
        """
        # Arrange & Act
        from installer.exit_codes import ExitCodes

        exit_codes = [
            ExitCodes.SUCCESS,
            ExitCodes.MISSING_SOURCE,
            ExitCodes.PERMISSION_DENIED,
            ExitCodes.ROLLBACK_OCCURRED,
            ExitCodes.VALIDATION_FAILED,
        ]

        # Assert
        for code in exit_codes:
            assert isinstance(code, int), f"Exit code {code} is not an integer"


class TestExitCodeRange:
    """Test that all exit codes are within valid range (0-4)."""

    def test_all_exit_codes_within_range_0_to_4(self):
        """
        Test: All exit codes are within range 0-4.

        Given: ExitCodes module is imported
        When: All constants are accessed
        Then: All values are between 0 and 4 (inclusive)
        """
        # Arrange & Act
        from installer.exit_codes import ExitCodes

        exit_codes = [
            ExitCodes.SUCCESS,
            ExitCodes.MISSING_SOURCE,
            ExitCodes.PERMISSION_DENIED,
            ExitCodes.ROLLBACK_OCCURRED,
            ExitCodes.VALIDATION_FAILED,
        ]

        # Assert
        for code in exit_codes:
            assert 0 <= code <= 4, f"Exit code {code} is outside valid range (0-4)"


class TestExitCodeConstantCount:
    """Test that exactly 5 exit codes are defined."""

    def test_exactly_5_exit_codes_defined(self):
        """
        Test: ExitCodes module defines exactly 5 constants.

        Given: ExitCodes module is imported
        When: Module attributes are inspected
        Then: Exactly 5 exit code constants exist (SUCCESS, MISSING_SOURCE, PERMISSION_DENIED, ROLLBACK_OCCURRED, VALIDATION_FAILED)
        """
        # Arrange & Act
        from installer.exit_codes import ExitCodes

        # Get all uppercase attributes (constants)
        constants = [attr for attr in dir(ExitCodes) if attr.isupper() and not attr.startswith('_')]

        # Assert
        assert len(constants) == 5, f"Expected 5 exit code constants, found {len(constants)}"
        assert "SUCCESS" in constants
        assert "MISSING_SOURCE" in constants
        assert "PERMISSION_DENIED" in constants
        assert "ROLLBACK_OCCURRED" in constants
        assert "VALIDATION_FAILED" in constants


class TestExitCodeDocumentation:
    """Test that exit codes have documentation."""

    def test_exit_codes_module_has_docstring(self):
        """
        Test: ExitCodes module has docstring explaining exit codes.

        Given: ExitCodes module is imported
        When: Module docstring is accessed
        Then: Docstring exists and explains exit codes
        """
        # Arrange & Act
        from installer import exit_codes

        # Assert
        assert exit_codes.__doc__ is not None
        assert len(exit_codes.__doc__) > 50, "Module docstring too short"


class TestExitCodeUsage:
    """Test exit code usage patterns."""

    def test_exit_code_can_be_used_in_sys_exit(self):
        """
        Test: Exit codes can be used with sys.exit().

        Given: ExitCodes constants are defined
        When: Used with sys.exit()
        Then: Works without errors (integers are valid)
        """
        # Arrange
        from installer.exit_codes import ExitCodes
        import sys

        # Act & Assert
        # This should not raise any errors
        exit_code = ExitCodes.SUCCESS
        assert isinstance(exit_code, int)
        # In real usage: sys.exit(ExitCodes.SUCCESS)

    def test_exit_code_can_be_compared_for_equality(self):
        """
        Test: Exit codes support equality comparison.

        Given: ExitCodes constants are defined
        When: Compared using ==
        Then: Equality works correctly
        """
        # Arrange & Act
        from installer.exit_codes import ExitCodes

        # Assert
        assert ExitCodes.SUCCESS == 0
        assert ExitCodes.MISSING_SOURCE == 1
        assert ExitCodes.SUCCESS != ExitCodes.MISSING_SOURCE


class TestExitCodeNaming:
    """Test exit code naming conventions."""

    def test_exit_code_names_are_uppercase(self):
        """
        Test: All exit code constants use UPPERCASE naming.

        Given: ExitCodes module is imported
        When: Constant names are inspected
        Then: All names are uppercase (Python constant convention)
        """
        # Arrange & Act
        from installer.exit_codes import ExitCodes

        constants = [attr for attr in dir(ExitCodes) if not attr.startswith('_') and attr.isupper()]

        # Assert
        for constant in constants:
            assert constant.isupper(), f"Constant {constant} is not uppercase"
            assert constant.replace('_', '').isalpha(), f"Constant {constant} contains non-alphabetic characters"


class TestExitCodeEnum:
    """Test if ExitCodes is implemented as Enum (optional pattern)."""

    def test_exit_codes_can_be_implemented_as_class_or_enum(self):
        """
        Test: ExitCodes can be implemented as class with attributes or Enum.

        Given: ExitCodes module is imported
        When: Implementation is checked
        Then: Either class with attributes OR Enum is acceptable
        """
        # Arrange & Act
        from installer.exit_codes import ExitCodes
        from enum import IntEnum

        # Assert
        # Both patterns are acceptable:
        # 1. class ExitCodes: SUCCESS = 0, MISSING_SOURCE = 1, ...
        # 2. class ExitCodes(IntEnum): SUCCESS = 0, MISSING_SOURCE = 1, ...
        is_class = isinstance(ExitCodes, type)
        is_enum = issubclass(ExitCodes, IntEnum) if is_class else False

        assert is_class, "ExitCodes should be a class or Enum"
