"""Tests for exit code constants (AC#6)."""
import pytest
from src.installer.exit_codes import (
    SUCCESS,
    MISSING_SOURCE,
    PERMISSION_DENIED,
    ROLLBACK_OCCURRED,
    VALIDATION_FAILED,
)


class TestExitCodeDefinitions:
    """Test that all 5 exit codes are defined with correct values."""

    def test_success_constant_defined(self):
        """Test: SUCCESS constant exists and equals 0."""
        assert SUCCESS == 0

    def test_missing_source_constant_defined(self):
        """Test: MISSING_SOURCE constant exists and equals 1."""
        assert MISSING_SOURCE == 1

    def test_permission_denied_constant_defined(self):
        """Test: PERMISSION_DENIED constant exists and equals 2."""
        assert PERMISSION_DENIED == 2

    def test_rollback_occurred_constant_defined(self):
        """Test: ROLLBACK_OCCURRED constant exists and equals 3."""
        assert ROLLBACK_OCCURRED == 3

    def test_validation_failed_constant_defined(self):
        """Test: VALIDATION_FAILED constant exists and equals 4."""
        assert VALIDATION_FAILED == 4

    def test_all_constants_are_integers(self):
        """Test: All exit codes are integers."""
        assert isinstance(SUCCESS, int)
        assert isinstance(MISSING_SOURCE, int)
        assert isinstance(PERMISSION_DENIED, int)
        assert isinstance(ROLLBACK_OCCURRED, int)
        assert isinstance(VALIDATION_FAILED, int)

    def test_exit_codes_in_valid_range(self):
        """Test: All exit codes are 0-4."""
        codes = [SUCCESS, MISSING_SOURCE, PERMISSION_DENIED, ROLLBACK_OCCURRED, VALIDATION_FAILED]
        for code in codes:
            assert 0 <= code <= 4

    def test_exit_codes_are_unique(self):
        """Test: All exit codes have different values."""
        codes = [SUCCESS, MISSING_SOURCE, PERMISSION_DENIED, ROLLBACK_OCCURRED, VALIDATION_FAILED]
        assert len(codes) == len(set(codes)), "Exit codes must be unique"

    def test_success_is_zero(self):
        """Test: SUCCESS exit code is always 0."""
        assert SUCCESS == 0

    def test_error_codes_non_zero(self):
        """Test: All error codes are non-zero."""
        error_codes = [MISSING_SOURCE, PERMISSION_DENIED, ROLLBACK_OCCURRED, VALIDATION_FAILED]
        for code in error_codes:
            assert code != 0, "Error codes must be non-zero"

    def test_exit_codes_sequential(self):
        """Test: Exit codes follow expected sequence."""
        assert SUCCESS < MISSING_SOURCE
        assert MISSING_SOURCE < PERMISSION_DENIED
        assert PERMISSION_DENIED < ROLLBACK_OCCURRED
        assert ROLLBACK_OCCURRED < VALIDATION_FAILED

    def test_error_category_mapping(self):
        """Test: Exit codes match error categories."""
        # AC#1: Error Taxonomy requirement
        error_codes = {
            'MISSING_SOURCE': MISSING_SOURCE,
            'PERMISSION_DENIED': PERMISSION_DENIED,
            'ROLLBACK_OCCURRED': ROLLBACK_OCCURRED,
            'VALIDATION_FAILED': VALIDATION_FAILED,
        }
        expected_codes = [1, 2, 3, 4]
        actual_codes = sorted([code for code in error_codes.values()])
        assert actual_codes == expected_codes

    def test_exit_code_constants_importable(self):
        """Test: Exit codes can be imported for use."""
        # This test verifies the import path works
        from src.installer.exit_codes import SUCCESS as test_success
        assert test_success == 0

    def test_exit_codes_hashable(self):
        """Test: Exit codes can be used in sets/dicts."""
        exit_code_dict = {
            SUCCESS: 'success',
            MISSING_SOURCE: 'missing_source',
            PERMISSION_DENIED: 'permission_denied',
            ROLLBACK_OCCURRED: 'rollback_occurred',
            VALIDATION_FAILED: 'validation_failed',
        }
        assert len(exit_code_dict) == 5
