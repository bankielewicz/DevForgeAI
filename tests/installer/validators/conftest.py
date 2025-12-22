"""
Shared fixtures for pre-flight validation tests.

Provides common setup for validator testing including:
- Mock filesystem structures
- Temporary directories
- Common test data
- Shared utilities
"""

import pytest
import tempfile
import shutil
from pathlib import Path
from typing import Generator


@pytest.fixture
def temp_dir() -> Generator[Path, None, None]:
    """
    Create temporary directory for test isolation.

    Automatically cleaned up after test completion.
    """
    tmp = Path(tempfile.mkdtemp())
    yield tmp
    shutil.rmtree(tmp, ignore_errors=True)


@pytest.fixture
def existing_installation_dir(temp_dir: Path) -> Path:
    """
    Create directory with existing DevForgeAI installation structure.

    Contains:
    - .claude/skills/ directory
    - devforgeai/context/ directory
    - version.json file
    """
    claude_dir = temp_dir / ".claude" / "skills"
    claude_dir.mkdir(parents=True)

    devforgeai_dir = temp_dir / "devforgeai" / "context"
    devforgeai_dir.mkdir(parents=True)

    # Create version.json
    version_file = temp_dir / "version.json"
    version_file.write_text('{"version": "1.0.0", "release_date": "2025-11-25"}')

    return temp_dir


@pytest.fixture
def partial_installation_dir(temp_dir: Path) -> Path:
    """
    Create directory with partial/incomplete DevForgeAI installation.

    Contains:
    - .claude/ directory (but no skills subdirectory)
    """
    claude_dir = temp_dir / ".claude"
    claude_dir.mkdir()

    return temp_dir


@pytest.fixture
def fresh_installation_dir(temp_dir: Path) -> Path:
    """
    Create empty directory for fresh installation.

    No existing DevForgeAI files present.
    """
    return temp_dir


@pytest.fixture
def read_only_dir(temp_dir: Path) -> Path:
    """
    Create read-only directory to test permission failures.

    Note: Requires manual cleanup if test fails before restoring permissions.
    """
    read_only = temp_dir / "readonly"
    read_only.mkdir()
    read_only.chmod(0o444)  # Read-only for owner, group, others

    yield read_only

    # Restore write permissions for cleanup
    read_only.chmod(0o755)


@pytest.fixture
def mock_python_version_output():
    """
    Common Python version strings for testing.

    Returns dict with various Python version outputs.
    """
    return {
        "valid_3_11": "Python 3.11.4",
        "valid_3_10": "Python 3.10.0",
        "invalid_3_9": "Python 3.9.18",
        "invalid_2_7": "Python 2.7.18",
        "invalid_format": "Python version 3.11.4",
        "empty": "",
    }


@pytest.fixture
def validation_config():
    """
    Default validation configuration values.

    Matches ValidationConfig in technical specification.
    """
    return {
        "MIN_PYTHON_VERSION": "3.10",
        "MIN_DISK_SPACE_MB": 100,
        "CHECK_TIMEOUT_SECONDS": 5,
        "PYTHON_EXECUTABLES": ["python3", "python", "python3.11", "python3.10"],
    }


@pytest.fixture
def check_status_enum():
    """
    Check status enum values.

    Used for asserting CheckResult.status values.
    """
    from enum import Enum

    class CheckStatus(Enum):
        PASS = "PASS"
        WARN = "WARN"
        FAIL = "FAIL"

    return CheckStatus


# Utility functions for test assertions

def assert_check_result_valid(check_result, expected_status: str, expected_check_name: str):
    """
    Assert CheckResult has expected structure and values.

    Args:
        check_result: CheckResult object to validate
        expected_status: Expected status (PASS/WARN/FAIL)
        expected_check_name: Expected check name string
    """
    assert check_result is not None, "CheckResult is None"
    assert hasattr(check_result, "check_name"), "CheckResult missing check_name"
    assert hasattr(check_result, "status"), "CheckResult missing status"
    assert hasattr(check_result, "message"), "CheckResult missing message"

    assert check_result.check_name == expected_check_name, \
        f"Expected check_name '{expected_check_name}', got '{check_result.check_name}'"
    assert check_result.status == expected_status, \
        f"Expected status '{expected_status}', got '{check_result.status}'"
    assert len(check_result.message) > 0, "CheckResult message is empty"


def assert_validation_result_valid(validation_result):
    """
    Assert ValidationResult has expected structure.

    Args:
        validation_result: ValidationResult object to validate
    """
    assert validation_result is not None, "ValidationResult is None"
    assert hasattr(validation_result, "checks"), "ValidationResult missing checks"
    assert hasattr(validation_result, "all_pass"), "ValidationResult missing all_pass"
    assert hasattr(validation_result, "warnings_present"), "ValidationResult missing warnings_present"
    assert hasattr(validation_result, "critical_failures"), "ValidationResult missing critical_failures"

    assert isinstance(validation_result.checks, list), "checks must be a list"
    assert len(validation_result.checks) > 0, "checks list is empty"
