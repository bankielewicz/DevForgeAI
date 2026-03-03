"""
Pytest configuration for STORY-236 Pre-Flight Validator tests.

This conftest.py provides shared fixtures and configuration for the
preflight validator test suite.
"""

import sys
from pathlib import Path

# Add project root to sys.path BEFORE any other imports
# This must happen in conftest.py which loads before test modules
_project_root = Path(__file__).parent.parent.parent
if str(_project_root) not in sys.path:
    sys.path.insert(0, str(_project_root))

import pytest
from unittest.mock import patch, mock_open, MagicMock
import tempfile
import shutil


@pytest.fixture
def temp_directory():
    """Create a temporary directory for tests."""
    temp_dir = tempfile.mkdtemp()
    yield temp_dir
    # Cleanup
    try:
        shutil.rmtree(temp_dir)
    except OSError:
        pass


@pytest.fixture
def mock_platform_info_wsl():
    """Fixture for mocking WSL PlatformInfo."""
    # Lazy import to avoid import errors before tests setup
    from installer.platform_detector import PlatformInfo
    return PlatformInfo(
        os_type="Linux",
        is_wsl=True,
        wsl_version=2,
        filesystem="ntfs-wsl",
        is_cross_filesystem=True,
        supports_chmod=False
    )


@pytest.fixture
def mock_platform_info_native_linux():
    """Fixture for mocking native Linux PlatformInfo."""
    from installer.platform_detector import PlatformInfo
    return PlatformInfo(
        os_type="Linux",
        is_wsl=False,
        wsl_version=None,
        filesystem="ext4",
        is_cross_filesystem=False,
        supports_chmod=True
    )


@pytest.fixture
def mock_disk_usage_sufficient():
    """Fixture for mocking sufficient disk space (>25MB)."""
    # 100MB total, 50MB free
    mock_usage = MagicMock()
    mock_usage.free = 50 * 1024 * 1024  # 50 MB
    mock_usage.total = 100 * 1024 * 1024  # 100 MB
    with patch("shutil.disk_usage", return_value=mock_usage):
        yield mock_usage


@pytest.fixture
def mock_disk_usage_insufficient():
    """Fixture for mocking insufficient disk space (<25MB)."""
    # 100MB total, only 10MB free
    mock_usage = MagicMock()
    mock_usage.free = 10 * 1024 * 1024  # 10 MB
    mock_usage.total = 100 * 1024 * 1024  # 100 MB
    with patch("shutil.disk_usage", return_value=mock_usage):
        yield mock_usage


@pytest.fixture
def mock_disk_usage_exact_threshold():
    """Fixture for mocking exactly 25MB disk space (boundary condition)."""
    mock_usage = MagicMock()
    mock_usage.free = 25 * 1024 * 1024  # Exactly 25 MB
    mock_usage.total = 100 * 1024 * 1024  # 100 MB
    with patch("shutil.disk_usage", return_value=mock_usage):
        yield mock_usage
