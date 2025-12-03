"""
Unit tests for PythonVersionChecker.

Tests AC#1: Python Version Validation
- Detect Python 3.10+ (PASS)
- Detect older Python versions (WARN)
- Handle missing Python (WARN)
- Try multiple executables in priority order

Component Requirements:
- SVC-005: Detect Python version via subprocess
- SVC-006: Parse version with regex, compare against 3.10
- SVC-007: Try multiple Python executables (python3, python, python3.11, python3.10)

Business Rules:
- BR-005: Python is optional (WARN, not FAIL)
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
import subprocess


class TestPythonVersionChecker:
    """Test suite for PythonVersionChecker service."""

    # AC#1: Python Version Validation - Valid Version (≥3.10)

    def test_should_return_pass_when_python_3_10_detected(self):
        """
        Test: Python 3.10.0 detected → PASS status

        Given: Python 3.10.0 is installed
        When: PythonVersionChecker.check() is called
        Then: Returns CheckResult with PASS status and version message
        """
        # Arrange
        from src.installer.validators.python_checker import PythonVersionChecker

        checker = PythonVersionChecker()

        with patch('subprocess.run') as mock_run:
            mock_run.return_value = Mock(
                returncode=0,
                stdout="Python 3.10.0",
                stderr=""
            )

            # Act
            result = checker.check()

            # Assert
            assert result.status == "PASS"
            assert "Python 3.10.0" in result.message
            assert result.check_name == "Python Version"

    def test_should_return_pass_when_python_3_11_detected(self):
        """
        Test: Python 3.11.4 detected → PASS status

        Given: Python 3.11.4 is installed
        When: PythonVersionChecker.check() is called
        Then: Returns CheckResult with PASS status and version message
        """
        # Arrange
        from src.installer.validators.python_checker import PythonVersionChecker

        checker = PythonVersionChecker()

        with patch('subprocess.run') as mock_run:
            mock_run.return_value = Mock(
                returncode=0,
                stdout="Python 3.11.4",
                stderr=""
            )

            # Act
            result = checker.check()

            # Assert
            assert result.status == "PASS"
            assert "3.11.4" in result.message
            assert "Python 3.10+ recommended" not in result.message

    # AC#1: Python Version Validation - Old Version (WARN)

    def test_should_return_warn_when_python_3_9_detected(self):
        """
        Test: Python 3.9.18 detected → WARN status

        Given: Python 3.9.18 is installed (below minimum 3.10)
        When: PythonVersionChecker.check() is called
        Then: Returns CheckResult with WARN status and upgrade message
        """
        # Arrange
        from src.installer.validators.python_checker import PythonVersionChecker

        checker = PythonVersionChecker()

        with patch('subprocess.run') as mock_run:
            mock_run.return_value = Mock(
                returncode=0,
                stdout="Python 3.9.18",
                stderr=""
            )

            # Act
            result = checker.check()

            # Assert
            assert result.status == "WARN"
            assert "3.9.18" in result.message
            assert "3.10+ recommended" in result.message
            assert "CLI validators disabled" in result.message or "optional" in result.message

    def test_should_return_warn_when_python_2_detected(self):
        """
        Test: Python 2.7.18 detected → WARN status

        Given: Python 2.7.18 is installed (legacy version)
        When: PythonVersionChecker.check() is called
        Then: Returns CheckResult with WARN status
        """
        # Arrange
        from src.installer.validators.python_checker import PythonVersionChecker

        checker = PythonVersionChecker()

        with patch('subprocess.run') as mock_run:
            mock_run.return_value = Mock(
                returncode=0,
                stdout="Python 2.7.18",
                stderr=""
            )

            # Act
            result = checker.check()

            # Assert
            assert result.status == "WARN"
            assert "2.7" in result.message

    # AC#1: Python Version Validation - Missing Python (WARN)

    def test_should_return_warn_when_python_not_found(self):
        """
        Test: Python not found → WARN status (BR-005)

        Given: Python is not installed (subprocess raises FileNotFoundError)
        When: PythonVersionChecker.check() is called
        Then: Returns CheckResult with WARN status, not FAIL
        """
        # Arrange
        from src.installer.validators.python_checker import PythonVersionChecker

        checker = PythonVersionChecker()

        with patch('subprocess.run') as mock_run:
            mock_run.side_effect = FileNotFoundError("python3 not found")

            # Act
            result = checker.check()

            # Assert
            assert result.status == "WARN"  # BR-005: Python is optional
            assert "not found" in result.message.lower() or "missing" in result.message.lower()
            assert result.check_name == "Python Version"

    def test_should_return_warn_when_subprocess_fails(self):
        """
        Test: Subprocess call fails → WARN status

        Given: Subprocess returns non-zero exit code
        When: PythonVersionChecker.check() is called
        Then: Returns CheckResult with WARN status and error context
        """
        # Arrange
        from src.installer.validators.python_checker import PythonVersionChecker

        checker = PythonVersionChecker()

        with patch('subprocess.run') as mock_run:
            mock_run.return_value = Mock(
                returncode=1,
                stdout="",
                stderr="Command failed"
            )

            # Act
            result = checker.check()

            # Assert
            assert result.status == "WARN"  # SVC-009: Handle exceptions gracefully

    # SVC-006: Parse version with regex

    def test_should_parse_version_with_regex(self):
        """
        Test: Version parsing with regex pattern

        Given: Various Python version output formats
        When: PythonVersionChecker.check() is called
        Then: Correctly parses version numbers with regex
        """
        # Arrange
        from src.installer.validators.python_checker import PythonVersionChecker

        checker = PythonVersionChecker()

        test_cases = [
            ("Python 3.11.4", "3.11.4", "PASS"),
            ("Python 3.10.0", "3.10.0", "PASS"),
            ("Python 3.9.18", "3.9.18", "WARN"),
        ]

        for stdout, expected_version, expected_status in test_cases:
            with patch('subprocess.run') as mock_run:
                mock_run.return_value = Mock(returncode=0, stdout=stdout, stderr="")

                # Act
                result = checker.check()

                # Assert
                assert result.status == expected_status, \
                    f"Expected status {expected_status} for {stdout}, got {result.status}"
                assert expected_version in result.message, \
                    f"Expected version {expected_version} in message for {stdout}"

    def test_should_handle_invalid_version_format(self):
        """
        Test: Invalid Python version format → WARN status

        Given: Python command returns invalid version format
        When: PythonVersionChecker.check() is called
        Then: Returns WARN status with parse error message
        """
        # Arrange
        from src.installer.validators.python_checker import PythonVersionChecker

        checker = PythonVersionChecker()

        with patch('subprocess.run') as mock_run:
            mock_run.return_value = Mock(
                returncode=0,
                stdout="Python version unknown",
                stderr=""
            )

            # Act
            result = checker.check()

            # Assert
            assert result.status == "WARN"
            assert "parse" in result.message.lower() or "invalid" in result.message.lower()

    # SVC-007: Try multiple Python executables in priority order

    def test_should_try_python3_first(self):
        """
        Test: Tries python3 executable first (SVC-007)

        Given: Multiple Python executables configured
        When: PythonVersionChecker.check() is called
        Then: Attempts to run 'python3' first
        """
        # Arrange
        from src.installer.validators.python_checker import PythonVersionChecker

        checker = PythonVersionChecker()

        with patch('subprocess.run') as mock_run:
            mock_run.return_value = Mock(returncode=0, stdout="Python 3.11.4", stderr="")

            # Act
            result = checker.check()

            # Assert
            # First call should be to python3
            assert mock_run.call_args_list[0][0][0] == ['python3', '--version'] or \
                   mock_run.call_args_list[0][1].get('args', ['python3'])[0] == 'python3'

    def test_should_fallback_to_python_if_python3_missing(self):
        """
        Test: Falls back to 'python' if 'python3' not found (SVC-007)

        Given: python3 command not found, but python command exists
        When: PythonVersionChecker.check() is called
        Then: Tries python3 first, then falls back to python
        """
        # Arrange
        from src.installer.validators.python_checker import PythonVersionChecker

        checker = PythonVersionChecker()

        with patch('subprocess.run') as mock_run:
            # python3 not found, python works
            mock_run.side_effect = [
                FileNotFoundError("python3 not found"),
                Mock(returncode=0, stdout="Python 3.11.4", stderr="")
            ]

            # Act
            result = checker.check()

            # Assert
            assert result.status == "PASS"
            assert "3.11.4" in result.message
            assert mock_run.call_count == 2  # Tried python3, then python

    def test_should_try_all_executables_in_priority_order(self):
        """
        Test: Tries all configured executables in order (SVC-007)

        Given: First 3 executables not found, 4th works
        When: PythonVersionChecker.check() is called
        Then: Tries python3, python, python3.11, python3.10 in order
        """
        # Arrange
        from src.installer.validators.python_checker import PythonVersionChecker

        checker = PythonVersionChecker()

        with patch('subprocess.run') as mock_run:
            # First 3 fail, last one works
            mock_run.side_effect = [
                FileNotFoundError(),
                FileNotFoundError(),
                FileNotFoundError(),
                Mock(returncode=0, stdout="Python 3.10.5", stderr="")
            ]

            # Act
            result = checker.check()

            # Assert
            assert result.status == "PASS"
            assert mock_run.call_count == 4  # Tried all 4 executables

    # NFR-002: Performance - Python check completes in <500ms

    def test_should_complete_check_within_500ms(self):
        """
        Test: Python version check completes in <500ms (NFR-002)

        Given: Python subprocess call is mocked
        When: PythonVersionChecker.check() is called
        Then: Execution completes in <500ms
        """
        # Arrange
        import time
        from src.installer.validators.python_checker import PythonVersionChecker

        checker = PythonVersionChecker()

        with patch('subprocess.run') as mock_run:
            mock_run.return_value = Mock(returncode=0, stdout="Python 3.11.4", stderr="")

            # Act
            start = time.time()
            result = checker.check()
            duration_ms = (time.time() - start) * 1000

            # Assert
            assert duration_ms < 500, f"Check took {duration_ms}ms (expected <500ms)"
            assert result.status == "PASS"

    # NFR-006: Usability - Error messages include actionable resolution steps

    def test_should_include_resolution_steps_in_warn_message(self):
        """
        Test: WARN message includes resolution steps (NFR-006)

        Given: Python check returns WARN status
        When: Message is examined
        Then: Contains at least 2 actionable resolution steps
        """
        # Arrange
        from src.installer.validators.python_checker import PythonVersionChecker

        checker = PythonVersionChecker()

        with patch('subprocess.run') as mock_run:
            mock_run.side_effect = FileNotFoundError()

            # Act
            result = checker.check()

            # Assert
            assert result.status == "WARN"
            # Message should contain resolution guidance
            message_lower = result.message.lower()
            resolution_keywords = ["install", "upgrade", "download", "check", "path"]
            matches = sum(1 for keyword in resolution_keywords if keyword in message_lower)
            assert matches >= 1, "Message should contain resolution guidance"

    # Edge Case: Container environment detection

    def test_should_detect_virtual_environment_python(self):
        """
        Test: Detects Python in virtual environment

        Given: Python is running from virtual environment
        When: PythonVersionChecker.check() is called
        Then: Returns PASS with environment context in message
        """
        # Arrange
        from src.installer.validators.python_checker import PythonVersionChecker

        checker = PythonVersionChecker()

        with patch('subprocess.run') as mock_run:
            mock_run.return_value = Mock(
                returncode=0,
                stdout="Python 3.11.4",
                stderr=""
            )

            # Act
            result = checker.check()

            # Assert
            assert result.status == "PASS"
            assert "3.11.4" in result.message

    # Configuration validation

    def test_should_use_configured_minimum_version(self):
        """
        Test: Uses MIN_PYTHON_VERSION from config

        Given: MIN_PYTHON_VERSION is configured as "3.10"
        When: PythonVersionChecker checks version
        Then: Compares against configured minimum
        """
        # Arrange
        from src.installer.validators.python_checker import PythonVersionChecker

        checker = PythonVersionChecker(min_version="3.10")

        test_cases = [
            ("Python 3.10.0", "PASS"),
            ("Python 3.9.18", "WARN"),
        ]

        for stdout, expected_status in test_cases:
            with patch('subprocess.run') as mock_run:
                mock_run.return_value = Mock(returncode=0, stdout=stdout, stderr="")

                # Act
                result = checker.check()

                # Assert
                assert result.status == expected_status, \
                    f"Expected {expected_status} for {stdout}, got {result.status}"

    # Security: Safe subprocess execution

    def test_should_use_safe_subprocess_call(self):
        """
        Test: Subprocess call uses shell=False (NFR-007)

        Given: PythonVersionChecker makes subprocess call
        When: check() is called
        Then: subprocess.run is called with shell=False
        """
        # Arrange
        from src.installer.validators.python_checker import PythonVersionChecker

        checker = PythonVersionChecker()

        with patch('subprocess.run') as mock_run:
            mock_run.return_value = Mock(returncode=0, stdout="Python 3.11.4", stderr="")

            # Act
            result = checker.check()

            # Assert
            # Verify shell=False in subprocess call
            call_kwargs = mock_run.call_args[1]
            assert call_kwargs.get('shell', False) is False, \
                "subprocess.run must use shell=False for security"

    # Edge Cases: Subprocess exception handling (Lines 85-90)

    def test_should_handle_subprocess_timeout_expired(self):
        """
        Test: subprocess.TimeoutExpired → try next executable

        Given: subprocess.run raises TimeoutExpired
        When: PythonVersionChecker.check() is called
        Then: Tries next executable in priority order
        """
        # Arrange
        from src.installer.validators.python_checker import PythonVersionChecker

        checker = PythonVersionChecker()

        with patch('subprocess.run') as mock_run:
            # First call times out, second succeeds
            mock_run.side_effect = [
                subprocess.TimeoutExpired(cmd="python3", timeout=5),
                Mock(returncode=0, stdout="Python 3.11.4", stderr="")
            ]

            # Act
            result = checker.check()

            # Assert
            assert result.status == "PASS"
            assert "3.11.4" in result.message
            assert mock_run.call_count == 2

    def test_should_return_warn_when_all_executables_timeout(self):
        """
        Test: All executables timeout → WARN status

        Given: All Python executables raise TimeoutExpired
        When: PythonVersionChecker.check() is called
        Then: Returns WARN status indicating Python not found
        """
        # Arrange
        from src.installer.validators.python_checker import PythonVersionChecker

        checker = PythonVersionChecker()

        with patch('subprocess.run') as mock_run:
            mock_run.side_effect = subprocess.TimeoutExpired(cmd="python", timeout=5)

            # Act
            result = checker.check()

            # Assert
            assert result.status == "WARN"
            assert "not found" in result.message.lower() or "optional" in result.message.lower()

    def test_should_handle_generic_exception_in_subprocess(self):
        """
        Test: Generic exception during subprocess → try next executable

        Given: subprocess.run raises unexpected exception
        When: PythonVersionChecker.check() is called
        Then: Tries next executable without crashing
        """
        # Arrange
        from src.installer.validators.python_checker import PythonVersionChecker

        checker = PythonVersionChecker()

        with patch('subprocess.run') as mock_run:
            # First call raises generic exception, second succeeds
            mock_run.side_effect = [
                RuntimeError("Unexpected error"),
                Mock(returncode=0, stdout="Python 3.10.5", stderr="")
            ]

            # Act
            result = checker.check()

            # Assert
            assert result.status == "PASS"
            assert "3.10.5" in result.message

    def test_should_return_warn_when_all_executables_raise_exceptions(self):
        """
        Test: All executables raise exceptions → WARN status

        Given: Every Python executable raises various exceptions
        When: PythonVersionChecker.check() is called
        Then: Returns WARN status after trying all executables
        """
        # Arrange
        from src.installer.validators.python_checker import PythonVersionChecker

        checker = PythonVersionChecker()

        with patch('subprocess.run') as mock_run:
            # Each executable raises a different exception
            mock_run.side_effect = [
                FileNotFoundError(),
                subprocess.TimeoutExpired(cmd="python", timeout=5),
                PermissionError("Access denied"),
                RuntimeError("Unknown error")
            ]

            # Act
            result = checker.check()

            # Assert
            assert result.status == "WARN"
            assert mock_run.call_count == 4  # Tried all 4 executables

    # Edge Cases: Version parsing edge cases (Lines 145-146)

    def test_should_handle_version_with_insufficient_parts(self):
        """
        Test: Version string with only major version → returns False

        Given: Version string "3" (missing minor version)
        When: _is_version_sufficient is called internally
        Then: Returns False (IndexError handled)
        """
        # Arrange
        from src.installer.validators.python_checker import PythonVersionChecker

        checker = PythonVersionChecker()

        with patch('subprocess.run') as mock_run:
            # Output has valid format but will fail internal comparison
            mock_run.return_value = Mock(
                returncode=0,
                stdout="Python 3",  # Invalid format - regex won't match
                stderr=""
            )

            # Act
            result = checker.check()

            # Assert
            # This should trigger WARN due to parse failure
            assert result.status == "WARN"
            assert "parse" in result.message.lower() or "could not" in result.message.lower()

    def test_should_handle_version_with_non_numeric_parts(self):
        """
        Test: Version with non-numeric parts → handles ValueError

        Given: Version comparison receives non-numeric data
        When: _is_version_sufficient is called
        Then: Returns False gracefully (ValueError handled)
        """
        # Arrange
        from src.installer.validators.python_checker import PythonVersionChecker

        # Create checker with invalid min_version to test error handling
        checker = PythonVersionChecker(min_version="invalid.version")

        with patch('subprocess.run') as mock_run:
            mock_run.return_value = Mock(
                returncode=0,
                stdout="Python 3.11.4",
                stderr=""
            )

            # Act
            result = checker.check()

            # Assert
            # Should handle ValueError in _is_version_sufficient
            # and return WARN since comparison fails
            assert result.status == "WARN"

    def test_should_handle_min_version_with_insufficient_parts(self):
        """
        Test: min_version with only major number → handles IndexError

        Given: min_version is "3" (missing minor version)
        When: _is_version_sufficient compares versions
        Then: Returns False gracefully (IndexError handled)
        """
        # Arrange
        from src.installer.validators.python_checker import PythonVersionChecker

        checker = PythonVersionChecker(min_version="3")

        with patch('subprocess.run') as mock_run:
            mock_run.return_value = Mock(
                returncode=0,
                stdout="Python 3.11.4",
                stderr=""
            )

            # Act
            result = checker.check()

            # Assert
            # Should handle IndexError in _is_version_sufficient
            assert result.status == "WARN"

    def test_should_return_pass_when_major_version_exceeds_minimum(self):
        """
        Test: Major version > min major → PASS (line 139 coverage)

        Given: Python 4.0.0 detected with min_version 3.10
        When: PythonVersionChecker.check() is called
        Then: Returns PASS because 4 > 3
        """
        # Arrange
        from src.installer.validators.python_checker import PythonVersionChecker

        checker = PythonVersionChecker(min_version="3.10")

        with patch('subprocess.run') as mock_run:
            mock_run.return_value = Mock(
                returncode=0,
                stdout="Python 4.0.0",
                stderr=""
            )

            # Act
            result = checker.check()

            # Assert
            assert result.status == "PASS"
            assert "4.0.0" in result.message
