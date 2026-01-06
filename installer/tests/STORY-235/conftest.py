"""
Pytest configuration for STORY-235 Platform Detection Module tests.

This conftest.py provides shared fixtures and configuration for the
platform detector test suite.
"""

import sys
from pathlib import Path

# Add project root to sys.path BEFORE any other imports
# This must happen in conftest.py which loads before test modules
_project_root = Path(__file__).parent.parent.parent
if str(_project_root) not in sys.path:
    sys.path.insert(0, str(_project_root))

import pytest
from unittest.mock import patch, mock_open


# Note: Cache clearing moved to test_platform_detector.py setup_imports fixture
# to avoid import issues with pytest's fixture loading order


@pytest.fixture
def mock_linux_platform():
    """Fixture for mocking Linux platform environment."""
    with patch("platform.system", return_value="Linux"):
        yield


@pytest.fixture
def mock_darwin_platform():
    """Fixture for mocking macOS (Darwin) platform environment."""
    with patch("platform.system", return_value="Darwin"):
        yield


@pytest.fixture
def mock_windows_platform():
    """Fixture for mocking Windows platform environment."""
    with patch("platform.system", return_value="Windows"):
        yield


@pytest.fixture
def mock_wsl2_proc_version():
    """Fixture for mocking WSL2 /proc/version content."""
    content = "Linux version 5.15.90.1-microsoft-standard-WSL2"
    with patch("builtins.open", mock_open(read_data=content)):
        yield content


@pytest.fixture
def mock_wsl1_proc_version():
    """Fixture for mocking WSL1 /proc/version content."""
    content = "Linux version 4.4.0-19041-Microsoft"
    with patch("builtins.open", mock_open(read_data=content)):
        yield content


@pytest.fixture
def mock_native_linux_proc_version():
    """Fixture for mocking native Linux /proc/version content."""
    content = "Linux version 5.15.0-generic (buildd@lgw01-amd64-016)"
    with patch("builtins.open", mock_open(read_data=content)):
        yield content


@pytest.fixture
def mock_missing_proc_version():
    """Fixture for mocking missing /proc/version file."""
    with patch("builtins.open", side_effect=FileNotFoundError("/proc/version")):
        yield
