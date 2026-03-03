"""
STORY-274: Test Fixtures and Configuration

Pytest fixtures for verification report generation tests.
These tests are TDD Red phase - implementation does not exist yet.
"""

import pytest
from unittest.mock import MagicMock, patch
from typing import Dict, List, Any


@pytest.fixture
def sample_story_id():
    """Fixture: Standard story ID for testing."""
    return "STORY-274"


@pytest.fixture
def sample_timestamp():
    """Fixture: Standard ISO 8601 timestamp."""
    return "2026-01-19T12:00:00Z"


@pytest.fixture
def sample_files_inspected():
    """Fixture: Sample list of inspected files."""
    return [
        "src/module/file1.py",
        "src/module/file2.py",
        "tests/test_module.py"
    ]


@pytest.fixture
def sample_ac_result_pass():
    """Fixture: Sample passing AC result."""
    return {
        "ac_id": "AC#1",
        "result": "PASS",
        "evidence": {
            "test_count": 5,
            "tests_passed": 5,
            "coverage": 95.0
        },
        "issues": []
    }


@pytest.fixture
def sample_ac_result_fail():
    """Fixture: Sample failing AC result with issues."""
    return {
        "ac_id": "AC#2",
        "result": "FAIL",
        "evidence": {
            "test_count": 3,
            "tests_passed": 1,
            "coverage": 60.0
        },
        "issues": [
            {
                "file_path": "src/module/file.py",
                "line_number": 42,
                "description": "Function not tested"
            },
            {
                "file_path": "src/module/file.py",
                "line_number": 67,
                "description": "Missing error handling test"
            }
        ]
    }


@pytest.fixture
def sample_verification_results_all_pass(sample_ac_result_pass, sample_files_inspected):
    """Fixture: Verification results where all ACs pass."""
    return {
        "acceptance_criteria": [
            {**sample_ac_result_pass, "ac_id": "AC#1"},
            {**sample_ac_result_pass, "ac_id": "AC#2"},
            {**sample_ac_result_pass, "ac_id": "AC#3"},
        ],
        "files_inspected": sample_files_inspected
    }


@pytest.fixture
def sample_verification_results_some_fail(
    sample_ac_result_pass, sample_ac_result_fail, sample_files_inspected
):
    """Fixture: Verification results with mixed PASS/FAIL."""
    return {
        "acceptance_criteria": [
            {**sample_ac_result_pass, "ac_id": "AC#1"},
            {**sample_ac_result_fail, "ac_id": "AC#2"},
            {**sample_ac_result_pass, "ac_id": "AC#3"},
        ],
        "files_inspected": sample_files_inspected
    }


@pytest.fixture
def mock_file_system():
    """Fixture: Mocked file system for testing file operations."""
    with patch('builtins.open', MagicMock()) as mock_open:
        with patch('os.makedirs') as mock_makedirs:
            with patch('os.path.exists', return_value=False):
                mock_file = MagicMock()
                mock_open.return_value.__enter__ = MagicMock(return_value=mock_file)
                mock_open.return_value.__exit__ = MagicMock(return_value=False)
                yield {
                    'open': mock_open,
                    'makedirs': mock_makedirs,
                    'file': mock_file
                }


@pytest.fixture
def sample_issue():
    """Fixture: Sample Issue object data."""
    return {
        "file_path": "src/module/file.py",
        "line_number": 42,
        "description": "Missing test coverage for function calculate_total()"
    }


@pytest.fixture
def sample_verification_report_dict(sample_timestamp, sample_files_inspected):
    """Fixture: Complete verification report as dictionary."""
    return {
        "story_id": "STORY-274",
        "verification_timestamp": sample_timestamp,
        "verification_duration_seconds": 30,
        "phase": "4.5",
        "overall_result": "PASS",
        "acceptance_criteria": [
            {
                "ac_id": "AC#1",
                "result": "PASS",
                "evidence": {"test_count": 5, "tests_passed": 5},
                "issues": []
            }
        ],
        "files_inspected": sample_files_inspected,
        "total_issues": 0
    }
