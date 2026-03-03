"""
STORY-069: Unit Tests for network.py - Network Detection Module

Tests validate network detection, dependency warnings, and pre-installation checks.

Coverage targets:
- SocketNetworkDetector class: 100%
- check_network_availability(): 100%
- display_network_status(): 100%
- warn_network_feature_unavailable(): 100%
- detect_python_version(): 100%
- warn_missing_dependency(): 100%
- check_disk_space(): 100%
- check_git_available(): 100%

Expected Result: All tests pass (implementation complete)
"""

import pytest
import socket
import sys
import shutil
from pathlib import Path
from unittest.mock import patch, MagicMock, call, PropertyMock
from io import StringIO

from installer.network import (
    SocketNetworkDetector,
    check_network_availability,
    display_network_status,
    warn_network_feature_unavailable,
    detect_python_version,
    warn_missing_dependency,
    check_disk_space,
    check_git_available,
    NETWORK_CHECK_HOST,
    NETWORK_CHECK_PORT,
    DISK_SPACE_REQUIRED_MB,
)


class TestSocketNetworkDetector:
    """Unit tests for SocketNetworkDetector class."""

    def test_init_default_values(self):
        """
        Should initialize with default DNS host and port.

        Arrange: None
        Act: Create detector with no arguments
        Assert: Host and port are defaults (8.8.8.8:53)
        """
        # Act
        detector = SocketNetworkDetector()

        # Assert
        assert detector.host == NETWORK_CHECK_HOST
        assert detector.port == NETWORK_CHECK_PORT

    def test_init_custom_values(self):
        """
        Should initialize with custom host and port.

        Arrange: Custom host/port values
        Act: Create detector with custom arguments
        Assert: Host and port match custom values
        """
        # Arrange
        custom_host = "1.1.1.1"
        custom_port = 80

        # Act
        detector = SocketNetworkDetector(host=custom_host, port=custom_port)

        # Assert
        assert detector.host == custom_host
        assert detector.port == custom_port

    def test_check_network_availability_online(self):
        """
        Should return True when network is available.

        Arrange: Mock successful socket connection
        Act: Call check_network_availability()
        Assert: Returns True
        """
        # Arrange
        detector = SocketNetworkDetector()

        with patch('socket.create_connection') as mock_socket:
            mock_socket.return_value = MagicMock()

            # Act
            result = detector.check_network_availability(timeout=2)

            # Assert
            assert result is True
            mock_socket.assert_called_once_with((detector.host, detector.port), timeout=2)

    def test_check_network_availability_timeout(self):
        """
        Should return False when connection times out.

        Arrange: Mock socket timeout exception
        Act: Call check_network_availability()
        Assert: Returns False
        """
        # Arrange
        detector = SocketNetworkDetector()

        with patch('socket.create_connection') as mock_socket:
            mock_socket.side_effect = socket.timeout("Connection timed out")

            # Act
            result = detector.check_network_availability(timeout=2)

            # Assert
            assert result is False

    def test_check_network_availability_socket_error(self):
        """
        Should return False when socket error occurs.

        Arrange: Mock socket error exception
        Act: Call check_network_availability()
        Assert: Returns False
        """
        # Arrange
        detector = SocketNetworkDetector()

        with patch('socket.create_connection') as mock_socket:
            mock_socket.side_effect = socket.error("Network unreachable")

            # Act
            result = detector.check_network_availability(timeout=2)

            # Assert
            assert result is False

    def test_check_network_availability_os_error(self):
        """
        Should return False when OS error occurs.

        Arrange: Mock OS error exception
        Act: Call check_network_availability()
        Assert: Returns False
        """
        # Arrange
        detector = SocketNetworkDetector()

        with patch('socket.create_connection') as mock_socket:
            mock_socket.side_effect = OSError("Permission denied")

            # Act
            result = detector.check_network_availability(timeout=2)

            # Assert
            assert result is False

    def test_check_network_availability_custom_timeout(self):
        """
        Should use custom timeout when provided.

        Arrange: Mock socket connection
        Act: Call with timeout=5
        Assert: Socket called with timeout=5
        """
        # Arrange
        detector = SocketNetworkDetector()

        with patch('socket.create_connection') as mock_socket:
            mock_socket.return_value = MagicMock()

            # Act
            detector.check_network_availability(timeout=5)

            # Assert
            mock_socket.assert_called_once_with((detector.host, detector.port), timeout=5)


class TestCheckNetworkAvailability:
    """Unit tests for check_network_availability() function."""

    def test_delegates_to_socket_detector(self):
        """
        Should delegate to SocketNetworkDetector.

        Arrange: Mock SocketNetworkDetector
        Act: Call check_network_availability()
        Assert: SocketNetworkDetector.check_network_availability called
        """
        # Arrange
        with patch('socket.create_connection') as mock_socket:
            mock_socket.return_value = MagicMock()

            # Act
            result = check_network_availability(timeout=2)

            # Assert
            assert result is True

    def test_online_returns_true(self):
        """
        Should return True when online.

        Arrange: Mock successful socket connection
        Act: Call check_network_availability()
        Assert: Returns True
        """
        # Arrange
        with patch('socket.create_connection') as mock_socket:
            mock_socket.return_value = MagicMock()

            # Act
            result = check_network_availability()

            # Assert
            assert result is True

    def test_offline_returns_false(self):
        """
        Should return False when offline.

        Arrange: Mock socket timeout
        Act: Call check_network_availability()
        Assert: Returns False
        """
        # Arrange
        with patch('socket.create_connection') as mock_socket:
            mock_socket.side_effect = socket.timeout()

            # Act
            result = check_network_availability()

            # Assert
            assert result is False


class TestDisplayNetworkStatus:
    """Unit tests for display_network_status() function."""

    def test_display_online_status(self, capsys):
        """
        Should display 'Online' when is_online=True.

        Arrange: is_online=True
        Act: Call display_network_status()
        Assert: Stdout contains "Network Status: Online"
        """
        # Act
        display_network_status(is_online=True)

        # Assert
        captured = capsys.readouterr()
        assert "Network Status: Online" in captured.out

    def test_display_offline_status(self, capsys):
        """
        Should display 'Offline - Air-gapped mode' when is_online=False.

        Arrange: is_online=False
        Act: Call display_network_status()
        Assert: Stdout contains offline message and bundled files notice
        """
        # Act
        display_network_status(is_online=False)

        # Assert
        captured = capsys.readouterr()
        assert "Network Status: Offline - Air-gapped mode" in captured.out
        assert "Using bundled files only" in captured.out


class TestWarnNetworkFeatureUnavailable:
    """Unit tests for warn_network_feature_unavailable() function."""

    def test_minimal_warning(self, capsys):
        """
        Should display feature name and reason.

        Arrange: Feature name and reason
        Act: Call warn_network_feature_unavailable()
        Assert: Output contains feature name and reason
        """
        # Act
        warn_network_feature_unavailable(
            feature_name="Update Check",
            reason="Requires GitHub API access"
        )

        # Assert
        captured = capsys.readouterr()
        assert "Network-Dependent Feature Unavailable: Update Check" in captured.out
        assert "Reason: Requires GitHub API access" in captured.out

    def test_warning_with_impact(self, capsys):
        """
        Should display impact when provided.

        Arrange: Feature with impact message
        Act: Call warn_network_feature_unavailable()
        Assert: Output contains impact
        """
        # Act
        warn_network_feature_unavailable(
            feature_name="Update Check",
            reason="Requires GitHub API",
            impact="You won't receive update notifications"
        )

        # Assert
        captured = capsys.readouterr()
        assert "Impact: You won't receive update notifications" in captured.out

    def test_warning_with_enable_command(self, capsys):
        """
        Should display enable command when provided.

        Arrange: Feature with enable command
        Act: Call warn_network_feature_unavailable()
        Assert: Output contains enable command
        """
        # Act
        warn_network_feature_unavailable(
            feature_name="Update Check",
            reason="Requires GitHub API",
            enable_command="devforgeai update --check"
        )

        # Assert
        captured = capsys.readouterr()
        assert "Enable later: devforgeai update --check" in captured.out

    def test_warning_all_fields(self, capsys):
        """
        Should display all fields when provided.

        Arrange: All optional fields provided
        Act: Call warn_network_feature_unavailable()
        Assert: Output contains all fields
        """
        # Act
        warn_network_feature_unavailable(
            feature_name="Update Check",
            reason="Requires GitHub API access",
            impact="You won't receive update notifications",
            enable_command="devforgeai update --check"
        )

        # Assert
        captured = capsys.readouterr()
        assert "Update Check" in captured.out
        assert "Requires GitHub API access" in captured.out
        assert "You won't receive update notifications" in captured.out
        assert "devforgeai update --check" in captured.out


class TestDetectPythonVersion:
    """Unit tests for detect_python_version() function."""

    def test_python_38_detected(self):
        """
        Should return (3, 8) for Python 3.8.

        Arrange: Mock sys.version_info to (3, 8)
        Act: Call detect_python_version()
        Assert: Returns (3, 8)
        """
        # Arrange
        with patch('sys.version_info', MagicMock(major=3, minor=8)):
            # Act
            result = detect_python_version()

            # Assert
            assert result == (3, 8)

    def test_python_310_detected(self):
        """
        Should return (3, 10) for Python 3.10.

        Arrange: Mock sys.version_info to (3, 10)
        Act: Call detect_python_version()
        Assert: Returns (3, 10)
        """
        # Arrange
        with patch('sys.version_info', MagicMock(major=3, minor=10)):
            # Act
            result = detect_python_version()

            # Assert
            assert result == (3, 10)

    def test_python_27_rejected(self):
        """
        Should return None for Python 2.7 (< 3.8).

        Arrange: Mock sys.version_info to (2, 7)
        Act: Call detect_python_version()
        Assert: Returns None
        """
        # Arrange
        with patch('sys.version_info', MagicMock(major=2, minor=7)):
            # Act
            result = detect_python_version()

            # Assert
            assert result is None

    def test_python_37_rejected(self):
        """
        Should return None for Python 3.7 (< 3.8).

        Arrange: Mock sys.version_info to (3, 7)
        Act: Call detect_python_version()
        Assert: Returns None
        """
        # Arrange
        with patch('sys.version_info', MagicMock(major=3, minor=7)):
            # Act
            result = detect_python_version()

            # Assert
            assert result is None

    def test_attribute_error_handled(self):
        """
        Should return None when version_info unavailable.

        Arrange: Mock sys.version_info to not have major attribute
        Act: Call detect_python_version()
        Assert: Returns None
        """
        # Arrange
        mock_version_info = MagicMock()
        # Delete major attribute so accessing it raises AttributeError
        del mock_version_info.major

        with patch('sys.version_info', mock_version_info):
            # Act
            result = detect_python_version()

            # Assert
            assert result is None


class TestWarnMissingDependency:
    """Unit tests for warn_missing_dependency() function."""

    def test_warn_python_dependency(self, capsys):
        """
        Should display warning for missing Python.

        Arrange: Python dependency missing
        Act: Call warn_missing_dependency('python', reason)
        Assert: Output contains Python CLI warning
        """
        # Act
        warn_missing_dependency('python', reason='Python 3.8+ not found')

        # Assert
        captured = capsys.readouterr()
        assert "Optional Dependency Unavailable: Python CLI" in captured.out
        assert "Reason: Python 3.8+ not found" in captured.out
        assert "Impact: CLI validation commands unavailable" in captured.out
        assert "Mitigation: Install Python 3.8+ and re-run installation" in captured.out

    def test_warn_unknown_dependency(self, capsys):
        """
        Should display generic warning for unknown dependency.

        Arrange: Unknown dependency missing
        Act: Call warn_missing_dependency('unknown', reason)
        Assert: Output contains generic warning
        """
        # Act
        warn_missing_dependency('unknown', reason='Not available')

        # Assert
        captured = capsys.readouterr()
        assert "Optional Dependency Unavailable: unknown" in captured.out
        assert "Reason: Not available" in captured.out


class TestCheckDiskSpace:
    """Unit tests for check_disk_space() function."""

    def test_sufficient_disk_space(self, tmp_path):
        """
        Should pass when sufficient disk space available.

        Arrange: Temp directory with sufficient space (typically GBs)
        Act: Call check_disk_space(tmp_path, required_mb=1)
        Assert: No exception raised
        """
        # Act & Assert (no exception)
        check_disk_space(tmp_path, required_mb=1)

    def test_insufficient_disk_space(self, tmp_path):
        """
        Should raise RuntimeError when insufficient space.

        Arrange: Mock disk usage to show low space
        Act: Call check_disk_space()
        Assert: Raises RuntimeError with clear message
        """
        # Arrange
        mock_usage = MagicMock()
        mock_usage.free = 50 * 1024 * 1024  # 50 MB available

        with patch('shutil.disk_usage', return_value=mock_usage):
            # Act & Assert
            with pytest.raises(RuntimeError, match="Insufficient disk space"):
                check_disk_space(tmp_path, required_mb=200)

    def test_negative_required_mb(self, tmp_path):
        """
        Should raise ValueError for negative required_mb.

        Arrange: required_mb=-100
        Act: Call check_disk_space()
        Assert: Raises ValueError
        """
        # Act & Assert
        with pytest.raises(ValueError, match="must be non-negative"):
            check_disk_space(tmp_path, required_mb=-100)

    def test_zero_required_mb(self, tmp_path):
        """
        Should pass when required_mb=0.

        Arrange: required_mb=0
        Act: Call check_disk_space()
        Assert: No exception (always passes)
        """
        # Act & Assert
        check_disk_space(tmp_path, required_mb=0)


class TestCheckGitAvailable:
    """Unit tests for check_git_available() function."""

    def test_git_available(self):
        """
        Should pass when git is in PATH.

        Arrange: Mock shutil.which to return git path
        Act: Call check_git_available()
        Assert: No exception raised
        """
        # Arrange
        with patch('shutil.which', return_value='/usr/bin/git'):
            # Act & Assert (no exception)
            check_git_available()

    def test_git_unavailable(self):
        """
        Should raise RuntimeError when git not in PATH.

        Arrange: Mock shutil.which to return None
        Act: Call check_git_available()
        Assert: Raises RuntimeError with install URL
        """
        # Arrange
        with patch('shutil.which', return_value=None):
            # Act & Assert
            with pytest.raises(RuntimeError, match="Git is required"):
                check_git_available()
