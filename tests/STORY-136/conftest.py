"""
Shared pytest fixtures and test configuration for STORY-136
File-Based Checkpoint Protocol for Ideation Sessions

This module provides:
- Checkpoint data fixtures (valid, invalid, edge cases)
- Mock Write tool fixtures
- Mock filesystem fixtures
- UUID and timestamp fixtures
"""

import json
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Any, Optional

import pytest
from unittest.mock import Mock, MagicMock, patch


# ============================================================================
# Session ID Fixtures (UUID v4 format)
# ============================================================================

@pytest.fixture
def valid_session_id() -> str:
    """Generate a valid UUID v4 session ID"""
    return str(uuid.uuid4())


@pytest.fixture
def fixed_session_id() -> str:
    """Provide a fixed session ID for reproducible tests"""
    return "550e8400-e29b-41d4-a716-446655440000"


@pytest.fixture
def invalid_session_ids() -> list[str]:
    """Provide invalid session ID formats"""
    return [
        "not-a-uuid",                           # Invalid format
        "550e8400-e29b-41d4-a716",              # Incomplete UUID
        "550e8400e29b41d4a716446655440000",    # No hyphens
        "550e8400-e29b-41d4-a716-44665544000G", # Invalid hex character
        "123456789",                            # Too short
        "",                                     # Empty
    ]


# ============================================================================
# Timestamp Fixtures (ISO 8601 format)
# ============================================================================

@pytest.fixture
def valid_iso_timestamp() -> str:
    """Generate a valid ISO 8601 timestamp with milliseconds"""
    now = datetime.now(timezone.utc)
    return now.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"


@pytest.fixture
def fixed_iso_timestamp() -> str:
    """Provide a fixed timestamp for reproducible tests"""
    return "2025-12-22T15:30:45.123Z"


@pytest.fixture
def invalid_timestamps() -> list[str]:
    """Provide invalid timestamp formats"""
    return [
        "2025-12-22 15:30:45",                  # Missing T separator
        "2025-12-22T15:30:45",                  # Missing milliseconds and Z
        "2025-12-22T15:30:45.123",              # Missing Z suffix
        "2025-12-22T15:30:45.123+00:00",        # Wrong timezone format
        "22/12/2025 15:30:45",                  # US date format
        "not-a-timestamp",                      # Invalid format
        "",                                     # Empty
    ]


# ============================================================================
# Brainstorm Context Fixtures
# ============================================================================

@pytest.fixture
def valid_brainstorm_context() -> Dict[str, Any]:
    """Provide valid brainstorm context with all required fields"""
    return {
        "problem_statement": "Build a task management app for remote teams",
        "personas": [
            {
                "name": "Project Manager",
                "needs": ["task assignment", "progress tracking", "team communication"]
            },
            {
                "name": "Developer",
                "needs": ["task details", "time estimates", "dependencies"]
            }
        ],
        "requirements": [
            {
                "id": "FR-001",
                "description": "Create and assign tasks",
                "priority": "High"
            },
            {
                "id": "FR-002",
                "description": "Track task progress",
                "priority": "High"
            }
        ],
        "complexity_score": 37,
        "epics": [
            {
                "id": "E1",
                "title": "User Authentication",
                "features": 3
            },
            {
                "id": "E2",
                "title": "Task Management",
                "features": 5
            }
        ]
    }


@pytest.fixture
def minimal_brainstorm_context() -> Dict[str, Any]:
    """Provide minimal valid brainstorm context"""
    return {
        "problem_statement": "Sample problem",
        "personas": [],
        "requirements": [],
        "complexity_score": 0,
        "epics": []
    }


@pytest.fixture
def large_brainstorm_context() -> Dict[str, Any]:
    """Provide large brainstorm context for file size testing"""
    return {
        "problem_statement": "Build a comprehensive enterprise application with extensive features and integrations",
        "personas": [
            {
                "name": f"Persona {i}",
                "needs": [f"need {j}" for j in range(10)]
            }
            for i in range(20)
        ],
        "requirements": [
            {
                "id": f"FR-{i:03d}",
                "description": f"Requirement {i}: " + "x" * 100,
                "priority": "High" if i % 2 == 0 else "Medium"
            }
            for i in range(100)
        ],
        "complexity_score": 60,
        "epics": [
            {
                "id": f"E{i}",
                "title": f"Epic {i}: " + "x" * 50,
                "features": 10
            }
            for i in range(30)
        ]
    }


# ============================================================================
# Checkpoint Document Fixtures
# ============================================================================

@pytest.fixture
def valid_checkpoint_phase_1(
    fixed_session_id: str,
    fixed_iso_timestamp: str,
    valid_brainstorm_context: Dict[str, Any]
) -> Dict[str, Any]:
    """Provide a valid checkpoint after Phase 1 completion"""
    return {
        "session_id": fixed_session_id,
        "timestamp": fixed_iso_timestamp,
        "current_phase": 1,
        "phase_completed": True,
        "brainstorm_context": valid_brainstorm_context,
        "phase_completion": {
            "phase_1": True,
            "phase_2": False,
            "phase_3": False,
            "phase_4": False,
            "phase_5": False,
            "phase_6": False,
        }
    }


@pytest.fixture
def valid_checkpoint_phase_3(
    fixed_session_id: str,
    fixed_iso_timestamp: str,
    valid_brainstorm_context: Dict[str, Any]
) -> Dict[str, Any]:
    """Provide a valid checkpoint after Phase 3 completion"""
    return {
        "session_id": fixed_session_id,
        "timestamp": fixed_iso_timestamp,
        "current_phase": 3,
        "phase_completed": True,
        "brainstorm_context": valid_brainstorm_context,
        "phase_completion": {
            "phase_1": True,
            "phase_2": True,
            "phase_3": True,
            "phase_4": False,
            "phase_5": False,
            "phase_6": False,
        }
    }


@pytest.fixture
def checkpoint_missing_session_id(
    fixed_iso_timestamp: str,
    valid_brainstorm_context: Dict[str, Any]
) -> Dict[str, Any]:
    """Provide checkpoint missing session_id field"""
    return {
        "timestamp": fixed_iso_timestamp,
        "current_phase": 1,
        "phase_completed": True,
        "brainstorm_context": valid_brainstorm_context,
    }


@pytest.fixture
def checkpoint_missing_timestamp(
    fixed_session_id: str,
    valid_brainstorm_context: Dict[str, Any]
) -> Dict[str, Any]:
    """Provide checkpoint missing timestamp field"""
    return {
        "session_id": fixed_session_id,
        "current_phase": 1,
        "phase_completed": True,
        "brainstorm_context": valid_brainstorm_context,
    }


@pytest.fixture
def checkpoint_invalid_uuid(
    fixed_iso_timestamp: str,
    valid_brainstorm_context: Dict[str, Any]
) -> Dict[str, Any]:
    """Provide checkpoint with invalid UUID format"""
    return {
        "session_id": "not-a-valid-uuid",
        "timestamp": fixed_iso_timestamp,
        "current_phase": 1,
        "phase_completed": True,
        "brainstorm_context": valid_brainstorm_context,
    }


@pytest.fixture
def checkpoint_invalid_timestamp(
    fixed_session_id: str,
    valid_brainstorm_context: Dict[str, Any]
) -> Dict[str, Any]:
    """Provide checkpoint with invalid timestamp format"""
    return {
        "session_id": fixed_session_id,
        "timestamp": "2025-12-22 15:30:45",  # Missing T and Z
        "current_phase": 1,
        "phase_completed": True,
        "brainstorm_context": valid_brainstorm_context,
    }


@pytest.fixture
def checkpoint_out_of_range_phase(
    fixed_session_id: str,
    fixed_iso_timestamp: str,
    valid_brainstorm_context: Dict[str, Any]
) -> Dict[str, Any]:
    """Provide checkpoint with current_phase > 6"""
    return {
        "session_id": fixed_session_id,
        "timestamp": fixed_iso_timestamp,
        "current_phase": 7,  # Invalid: > 6
        "phase_completed": True,
        "brainstorm_context": valid_brainstorm_context,
    }


@pytest.fixture
def checkpoint_invalid_complexity_score(
    fixed_session_id: str,
    fixed_iso_timestamp: str,
    valid_brainstorm_context: Dict[str, Any]
) -> Dict[str, Any]:
    """Provide checkpoint with complexity_score > 60"""
    context = valid_brainstorm_context.copy()
    context["complexity_score"] = 75  # Invalid: > 60
    return {
        "session_id": fixed_session_id,
        "timestamp": fixed_iso_timestamp,
        "current_phase": 1,
        "phase_completed": True,
        "brainstorm_context": context,
    }


# ============================================================================
# Mock Tool Fixtures
# ============================================================================

@pytest.fixture
def mock_write_tool() -> Mock:
    """Mock the Write tool to capture checkpoint content"""
    mock = Mock()
    mock.write = Mock(return_value=None)
    return mock


@pytest.fixture
def mock_write_tool_with_error() -> Mock:
    """Mock the Write tool that raises an error"""
    mock = Mock()
    mock.write = Mock(side_effect=IOError("Disk full"))
    return mock


@pytest.fixture
def mock_read_tool() -> Mock:
    """Mock the Read tool to return checkpoint content"""
    mock = Mock()
    mock.read = Mock()
    return mock


@pytest.fixture
def mock_filesystem(tmp_path) -> Path:
    """Provide a temporary filesystem for testing"""
    checkpoint_dir = tmp_path / "devforgeai" / "temp"
    checkpoint_dir.mkdir(parents=True, exist_ok=True)
    return checkpoint_dir


# ============================================================================
# Test Configuration Fixtures
# ============================================================================

@pytest.fixture
def checkpoint_dir_path() -> str:
    """Provide the standard checkpoint directory path"""
    return "devforgeai/temp"


@pytest.fixture
def checkpoint_filename_pattern() -> str:
    """Provide the checkpoint filename pattern"""
    return ".ideation-checkpoint-{session_id}.yaml"


@pytest.fixture
def all_valid_phases() -> list[int]:
    """Provide list of all valid phase numbers"""
    return [1, 2, 3, 4, 5, 6]


@pytest.fixture
def all_invalid_phases() -> list[int]:
    """Provide list of all invalid phase numbers"""
    return [0, 7, 10, -1, 100]


@pytest.fixture
def valid_complexity_scores() -> list[int]:
    """Provide list of valid complexity scores"""
    return [0, 1, 30, 59, 60]


@pytest.fixture
def invalid_complexity_scores() -> list[int]:
    """Provide list of invalid complexity scores"""
    return [-1, 61, 100]


# ============================================================================
# Parameterization Fixtures
# ============================================================================

@pytest.fixture(params=[0, 1, 30, 59, 60])
def valid_complexity_score(request) -> int:
    """Parameterized fixture for valid complexity scores"""
    return request.param


@pytest.fixture(params=[-1, 61, 100])
def invalid_complexity_score(request) -> int:
    """Parameterized fixture for invalid complexity scores"""
    return request.param


@pytest.fixture(params=[1, 2, 3, 4, 5, 6])
def valid_phase_number(request) -> int:
    """Parameterized fixture for valid phase numbers"""
    return request.param


@pytest.fixture(params=[0, 7, 10, -1, 100])
def invalid_phase_number(request) -> int:
    """Parameterized fixture for invalid phase numbers"""
    return request.param
