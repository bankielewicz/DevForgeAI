"""
Shared fixtures for STORY-227: Calculate Workflow Success Metrics tests.

These fixtures provide sample data for testing metrics calculation functionality.
"""
import pytest
from typing import Dict, List, Any
from datetime import datetime, timedelta


@pytest.fixture
def sample_command_execution_data() -> List[Dict[str, Any]]:
    """
    Sample command execution data for testing per-command metrics.

    Contains mixed success, error, and retry scenarios across multiple command types.
    """
    return [
        # /dev commands
        {"command": "/dev", "status": "completed", "retry_count": 0, "timestamp": "2026-01-01T10:00:00Z"},
        {"command": "/dev", "status": "completed", "retry_count": 1, "timestamp": "2026-01-01T11:00:00Z"},
        {"command": "/dev", "status": "error", "error_type": "test_failure", "retry_count": 0, "timestamp": "2026-01-01T12:00:00Z"},
        {"command": "/dev", "status": "completed", "retry_count": 0, "timestamp": "2026-01-01T13:00:00Z"},
        {"command": "/dev", "status": "error", "error_type": "coverage_gap", "retry_count": 2, "timestamp": "2026-01-01T14:00:00Z"},

        # /qa commands
        {"command": "/qa", "status": "completed", "retry_count": 0, "timestamp": "2026-01-01T10:30:00Z"},
        {"command": "/qa", "status": "completed", "retry_count": 0, "timestamp": "2026-01-01T11:30:00Z"},
        {"command": "/qa", "status": "error", "error_type": "validation_failure", "retry_count": 1, "timestamp": "2026-01-01T12:30:00Z"},

        # /create-story commands
        {"command": "/create-story", "status": "completed", "retry_count": 0, "timestamp": "2026-01-01T09:00:00Z"},
        {"command": "/create-story", "status": "completed", "retry_count": 0, "timestamp": "2026-01-01T09:30:00Z"},
    ]


@pytest.fixture
def empty_command_execution_data() -> List[Dict[str, Any]]:
    """Empty command execution data for edge case testing."""
    return []


@pytest.fixture
def sample_error_entries() -> List[Dict[str, Any]]:
    """
    Sample error entries for testing failure mode identification.

    Contains various error types with different frequencies.
    """
    return [
        # Most common: test_failure (4 occurrences)
        {"error_type": "test_failure", "command": "/dev", "message": "Tests failed", "timestamp": "2026-01-01T10:00:00Z"},
        {"error_type": "test_failure", "command": "/dev", "message": "Tests failed", "timestamp": "2026-01-01T11:00:00Z"},
        {"error_type": "test_failure", "command": "/dev", "message": "Tests failed", "timestamp": "2026-01-01T12:00:00Z"},
        {"error_type": "test_failure", "command": "/qa", "message": "Tests failed", "timestamp": "2026-01-01T13:00:00Z"},

        # Second most common: coverage_gap (3 occurrences)
        {"error_type": "coverage_gap", "command": "/qa", "message": "Coverage below threshold", "timestamp": "2026-01-01T10:30:00Z"},
        {"error_type": "coverage_gap", "command": "/dev", "message": "Coverage below threshold", "timestamp": "2026-01-01T11:30:00Z"},
        {"error_type": "coverage_gap", "command": "/qa", "message": "Coverage below threshold", "timestamp": "2026-01-01T12:30:00Z"},

        # Third: validation_failure (2 occurrences)
        {"error_type": "validation_failure", "command": "/create-story", "message": "Validation failed", "timestamp": "2026-01-01T14:00:00Z"},
        {"error_type": "validation_failure", "command": "/qa", "message": "Validation failed", "timestamp": "2026-01-01T14:30:00Z"},

        # Least common: timeout (1 occurrence)
        {"error_type": "timeout", "command": "/dev", "message": "Command timed out", "timestamp": "2026-01-01T15:00:00Z"},
    ]


@pytest.fixture
def empty_error_entries() -> List[Dict[str, Any]]:
    """Empty error entries for edge case testing."""
    return []


@pytest.fixture
def sample_workflow_metrics_with_story_points() -> List[Dict[str, Any]]:
    """
    Sample workflow metrics with story point assignments for segmentation testing.

    Contains metrics for stories with valid points (1, 2, 3, 5, 8) and some invalid.
    """
    return [
        # 1-point stories
        {"story_id": "STORY-001", "story_points": 1, "completion_rate": 100.0, "error_rate": 0.0, "duration_minutes": 30},
        {"story_id": "STORY-002", "story_points": 1, "completion_rate": 100.0, "error_rate": 5.0, "duration_minutes": 45},

        # 2-point stories
        {"story_id": "STORY-003", "story_points": 2, "completion_rate": 95.0, "error_rate": 10.0, "duration_minutes": 60},
        {"story_id": "STORY-004", "story_points": 2, "completion_rate": 90.0, "error_rate": 15.0, "duration_minutes": 90},

        # 3-point stories
        {"story_id": "STORY-005", "story_points": 3, "completion_rate": 85.0, "error_rate": 20.0, "duration_minutes": 120},
        {"story_id": "STORY-006", "story_points": 3, "completion_rate": 80.0, "error_rate": 25.0, "duration_minutes": 150},
        {"story_id": "STORY-007", "story_points": 3, "completion_rate": 90.0, "error_rate": 10.0, "duration_minutes": 110},

        # 5-point stories
        {"story_id": "STORY-008", "story_points": 5, "completion_rate": 75.0, "error_rate": 30.0, "duration_minutes": 240},
        {"story_id": "STORY-009", "story_points": 5, "completion_rate": 70.0, "error_rate": 35.0, "duration_minutes": 300},

        # 8-point stories
        {"story_id": "STORY-010", "story_points": 8, "completion_rate": 60.0, "error_rate": 40.0, "duration_minutes": 480},

        # Invalid story points (should be excluded)
        {"story_id": "STORY-011", "story_points": 0, "completion_rate": 50.0, "error_rate": 50.0, "duration_minutes": 60},
        {"story_id": "STORY-012", "story_points": 4, "completion_rate": 80.0, "error_rate": 20.0, "duration_minutes": 100},
        {"story_id": "STORY-013", "story_points": 13, "completion_rate": 55.0, "error_rate": 45.0, "duration_minutes": 600},
    ]


@pytest.fixture
def workflow_metrics_missing_points() -> List[Dict[str, Any]]:
    """Workflow metrics with some missing story_points fields."""
    return [
        {"story_id": "STORY-001", "story_points": 3, "completion_rate": 90.0, "error_rate": 10.0},
        {"story_id": "STORY-002", "completion_rate": 85.0, "error_rate": 15.0},  # Missing story_points
        {"story_id": "STORY-003", "story_points": 5, "completion_rate": 75.0, "error_rate": 25.0},
        {"story_id": "STORY-004", "story_points": None, "completion_rate": 70.0, "error_rate": 30.0},  # None value
    ]


@pytest.fixture
def valid_story_points() -> List[int]:
    """Valid Fibonacci-based story points per AC#3."""
    return [1, 2, 3, 5, 8]
