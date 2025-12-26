"""
Shared pytest fixtures and test configuration for STORY-137
Resume-from-Checkpoint Logic for Ideation Sessions

This module provides:
- Checkpoint data fixtures (valid, invalid, multiple)
- Mock tool fixtures (Glob, Read, AskUserQuestion)
- Session fixtures with various phase completions
- Checkpoint file operation fixtures
"""

import json
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Any, List, Optional

import pytest
from unittest.mock import Mock, MagicMock, patch


# ============================================================================
# Session ID Fixtures
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
def second_session_id() -> str:
    """Provide a second session ID for multi-checkpoint tests"""
    return "660e8400-e29b-41d4-a716-446655440001"


@pytest.fixture
def third_session_id() -> str:
    """Provide a third session ID for multi-checkpoint tests"""
    return "770e8400-e29b-41d4-a716-446655440002"


# ============================================================================
# Timestamp Fixtures
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
def old_iso_timestamp() -> str:
    """Provide an old timestamp (>30 days old)"""
    return "2025-11-15T10:00:00.000Z"


@pytest.fixture
def newer_iso_timestamp() -> str:
    """Provide a newer timestamp for sorting tests"""
    return "2025-12-23T10:30:45.456Z"


@pytest.fixture
def newest_iso_timestamp() -> str:
    """Provide the newest timestamp for sorting tests"""
    return "2025-12-24T15:45:30.789Z"


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
                "needs": ["task assignment", "progress tracking"]
            },
            {
                "name": "Developer",
                "needs": ["task details", "dependencies"]
            }
        ],
        "requirements": [
            {
                "id": "FR-001",
                "description": "Create and assign tasks",
                "priority": "High"
            }
        ],
        "complexity_score": 37,
        "epics": [
            {
                "id": "E1",
                "title": "User Authentication",
                "features": 3
            }
        ]
    }


@pytest.fixture
def minimal_brainstorm_context() -> Dict[str, Any]:
    """Provide minimal valid brainstorm context"""
    return {
        "problem_statement": "Simple problem statement",
        "personas": [],
        "requirements": [],
        "complexity_score": 0,
        "epics": []
    }


# ============================================================================
# Checkpoint Fixtures - Single Sessions
# ============================================================================

@pytest.fixture
def checkpoint_phase_1(
    fixed_session_id: str,
    fixed_iso_timestamp: str,
    valid_brainstorm_context: Dict[str, Any]
) -> Dict[str, Any]:
    """Checkpoint after Phase 1 completion"""
    return {
        "session_id": fixed_session_id,
        "timestamp": fixed_iso_timestamp,
        "current_phase": 1,
        "phase_completed": True,
        "brainstorm_context": valid_brainstorm_context,
    }


@pytest.fixture
def checkpoint_phase_2(
    fixed_session_id: str,
    fixed_iso_timestamp: str,
    valid_brainstorm_context: Dict[str, Any]
) -> Dict[str, Any]:
    """Checkpoint after Phase 2 completion"""
    return {
        "session_id": fixed_session_id,
        "timestamp": fixed_iso_timestamp,
        "current_phase": 2,
        "phase_completed": True,
        "brainstorm_context": valid_brainstorm_context,
    }


@pytest.fixture
def checkpoint_phase_3(
    fixed_session_id: str,
    fixed_iso_timestamp: str,
    valid_brainstorm_context: Dict[str, Any]
) -> Dict[str, Any]:
    """Checkpoint after Phase 3 completion"""
    return {
        "session_id": fixed_session_id,
        "timestamp": fixed_iso_timestamp,
        "current_phase": 3,
        "phase_completed": True,
        "brainstorm_context": valid_brainstorm_context,
    }


@pytest.fixture
def checkpoint_phase_4(
    fixed_session_id: str,
    fixed_iso_timestamp: str,
    valid_brainstorm_context: Dict[str, Any]
) -> Dict[str, Any]:
    """Checkpoint after Phase 4 completion"""
    return {
        "session_id": fixed_session_id,
        "timestamp": fixed_iso_timestamp,
        "current_phase": 4,
        "phase_completed": True,
        "brainstorm_context": valid_brainstorm_context,
    }


@pytest.fixture
def checkpoint_phase_5(
    fixed_session_id: str,
    fixed_iso_timestamp: str,
    valid_brainstorm_context: Dict[str, Any]
) -> Dict[str, Any]:
    """Checkpoint after Phase 5 completion"""
    return {
        "session_id": fixed_session_id,
        "timestamp": fixed_iso_timestamp,
        "current_phase": 5,
        "phase_completed": True,
        "brainstorm_context": valid_brainstorm_context,
    }


@pytest.fixture
def checkpoint_phase_incomplete(
    fixed_session_id: str,
    fixed_iso_timestamp: str,
    valid_brainstorm_context: Dict[str, Any]
) -> Dict[str, Any]:
    """Checkpoint with phase_completed=False"""
    return {
        "session_id": fixed_session_id,
        "timestamp": fixed_iso_timestamp,
        "current_phase": 2,
        "phase_completed": False,
        "brainstorm_context": valid_brainstorm_context,
    }


# ============================================================================
# Checkpoint Fixtures - Multiple Sessions
# ============================================================================

@pytest.fixture
def checkpoint_session_1(
    fixed_session_id: str,
    fixed_iso_timestamp: str,
    valid_brainstorm_context: Dict[str, Any]
) -> Dict[str, Any]:
    """First session checkpoint"""
    return {
        "session_id": fixed_session_id,
        "timestamp": fixed_iso_timestamp,
        "current_phase": 2,
        "phase_completed": True,
        "brainstorm_context": valid_brainstorm_context,
    }


@pytest.fixture
def checkpoint_session_2(
    second_session_id: str,
    newer_iso_timestamp: str,
    valid_brainstorm_context: Dict[str, Any]
) -> Dict[str, Any]:
    """Second session checkpoint (newer)"""
    return {
        "session_id": second_session_id,
        "timestamp": newer_iso_timestamp,
        "current_phase": 3,
        "phase_completed": True,
        "brainstorm_context": valid_brainstorm_context,
    }


@pytest.fixture
def checkpoint_session_3(
    third_session_id: str,
    newest_iso_timestamp: str,
    valid_brainstorm_context: Dict[str, Any]
) -> Dict[str, Any]:
    """Third session checkpoint (newest)"""
    return {
        "session_id": third_session_id,
        "timestamp": newest_iso_timestamp,
        "current_phase": 1,
        "phase_completed": True,
        "brainstorm_context": valid_brainstorm_context,
    }


@pytest.fixture
def checkpoint_old_session(
    fixed_session_id: str,
    old_iso_timestamp: str,
    valid_brainstorm_context: Dict[str, Any]
) -> Dict[str, Any]:
    """Old checkpoint for age validation"""
    return {
        "session_id": fixed_session_id,
        "timestamp": old_iso_timestamp,
        "current_phase": 2,
        "phase_completed": True,
        "brainstorm_context": valid_brainstorm_context,
    }


# ============================================================================
# Invalid Checkpoint Fixtures
# ============================================================================

@pytest.fixture
def checkpoint_malformed_yaml() -> str:
    """Malformed YAML content"""
    return """
session_id: 550e8400-e29b-41d4-a716-446655440000
timestamp: 2025-12-22T15:30:45.123Z
current_phase: 1
  invalid_indentation: true
    too_deep: value
brainstorm_context:
  problem_statement: test
  - unbalanced list
"""


@pytest.fixture
def checkpoint_missing_session_id(
    fixed_iso_timestamp: str,
    valid_brainstorm_context: Dict[str, Any]
) -> Dict[str, Any]:
    """Checkpoint missing session_id field"""
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
    """Checkpoint missing timestamp field"""
    return {
        "session_id": fixed_session_id,
        "current_phase": 1,
        "phase_completed": True,
        "brainstorm_context": valid_brainstorm_context,
    }


@pytest.fixture
def checkpoint_missing_context(
    fixed_session_id: str,
    fixed_iso_timestamp: str
) -> Dict[str, Any]:
    """Checkpoint missing brainstorm_context field"""
    return {
        "session_id": fixed_session_id,
        "timestamp": fixed_iso_timestamp,
        "current_phase": 1,
        "phase_completed": True,
    }


@pytest.fixture
def checkpoint_invalid_uuid(
    fixed_iso_timestamp: str,
    valid_brainstorm_context: Dict[str, Any]
) -> Dict[str, Any]:
    """Checkpoint with invalid UUID format"""
    return {
        "session_id": "not-a-valid-uuid",
        "timestamp": fixed_iso_timestamp,
        "current_phase": 1,
        "phase_completed": True,
        "brainstorm_context": valid_brainstorm_context,
    }


# ============================================================================
# Mock Tool Fixtures
# ============================================================================

@pytest.fixture
def mock_glob_tool() -> Mock:
    """Mock the Glob tool to return checkpoint filenames"""
    mock = Mock()
    mock.glob = Mock(return_value=[])
    return mock


@pytest.fixture
def mock_glob_tool_with_checkpoints(
    fixed_session_id: str,
    second_session_id: str,
    third_session_id: str
) -> Mock:
    """Mock the Glob tool that returns multiple checkpoint files"""
    mock = Mock()
    checkpoints = [
        f"/mnt/c/Projects/DevForgeAI2/devforgeai/temp/.ideation-checkpoint-{third_session_id}.yaml",
        f"/mnt/c/Projects/DevForgeAI2/devforgeai/temp/.ideation-checkpoint-{second_session_id}.yaml",
        f"/mnt/c/Projects/DevForgeAI2/devforgeai/temp/.ideation-checkpoint-{fixed_session_id}.yaml",
    ]
    mock.glob = Mock(return_value=checkpoints)
    return mock


@pytest.fixture
def mock_read_tool() -> Mock:
    """Mock the Read tool to return checkpoint content"""
    mock = Mock()
    mock.read = Mock()
    return mock


@pytest.fixture
def mock_read_tool_with_yaml(checkpoint_phase_1: Dict[str, Any]) -> Mock:
    """Mock the Read tool that returns valid YAML checkpoint"""
    import yaml
    mock = Mock()
    yaml_content = yaml.dump(checkpoint_phase_1)
    mock.read = Mock(return_value=yaml_content)
    return mock


@pytest.fixture
def mock_ask_user_question() -> Mock:
    """Mock the AskUserQuestion tool"""
    mock = Mock()
    mock.ask = Mock(return_value={"choice": "resume"})
    return mock


@pytest.fixture
def mock_ask_user_question_fresh_start() -> Mock:
    """Mock AskUserQuestion returning fresh start choice"""
    mock = Mock()
    mock.ask = Mock(return_value={"choice": "fresh"})
    return mock


@pytest.fixture
def mock_ask_user_question_keep_answers() -> Mock:
    """Mock AskUserQuestion returning keep answers choice"""
    mock = Mock()
    mock.ask = Mock(return_value={"choice": "keep"})
    return mock


@pytest.fixture
def mock_ask_user_question_update_answers() -> Mock:
    """Mock AskUserQuestion returning update answers choice"""
    mock = Mock()
    mock.ask = Mock(return_value={"choice": "update"})
    return mock


@pytest.fixture
def mock_ask_user_question_select_checkpoint(second_session_id: str) -> Mock:
    """Mock AskUserQuestion for checkpoint selection"""
    mock = Mock()
    mock.ask = Mock(return_value={"selected_checkpoint": second_session_id})
    return mock


# ============================================================================
# Checkpoint File Path Fixtures
# ============================================================================

@pytest.fixture
def checkpoint_glob_pattern() -> str:
    """Checkpoint glob pattern from AC#1"""
    return "devforgeai/temp/.ideation-checkpoint-*.yaml"


@pytest.fixture
def checkpoint_dir_path() -> str:
    """Standard checkpoint directory path"""
    return "devforgeai/temp"


# ============================================================================
# Multiple Checkpoint Scenarios
# ============================================================================

@pytest.fixture
def two_checkpoints(
    checkpoint_session_1: Dict[str, Any],
    checkpoint_session_2: Dict[str, Any]
) -> List[Dict[str, Any]]:
    """Two checkpoint files for selection testing"""
    return [checkpoint_session_2, checkpoint_session_1]  # Newest first


@pytest.fixture
def three_checkpoints(
    checkpoint_session_1: Dict[str, Any],
    checkpoint_session_2: Dict[str, Any],
    checkpoint_session_3: Dict[str, Any]
) -> List[Dict[str, Any]]:
    """Three checkpoint files for sorting validation"""
    return [checkpoint_session_3, checkpoint_session_2, checkpoint_session_1]  # Newest first


@pytest.fixture
def five_checkpoints(
    checkpoint_session_1: Dict[str, Any],
    checkpoint_session_2: Dict[str, Any],
    checkpoint_session_3: Dict[str, Any],
    checkpoint_old_session: Dict[str, Any]
) -> List[Dict[str, Any]]:
    """Five checkpoint files (using variations)"""
    context = checkpoint_session_1["brainstorm_context"]

    extra_checkpoint_1 = {
        "session_id": str(uuid.uuid4()),
        "timestamp": "2025-12-20T08:15:00.000Z",
        "current_phase": 1,
        "phase_completed": True,
        "brainstorm_context": context,
    }

    extra_checkpoint_2 = {
        "session_id": str(uuid.uuid4()),
        "timestamp": "2025-12-21T12:45:30.500Z",
        "current_phase": 2,
        "phase_completed": True,
        "brainstorm_context": context,
    }

    # Return sorted by timestamp (newest first)
    checkpoints = [
        checkpoint_session_3,  # 2025-12-24T15:45:30.789Z
        checkpoint_session_2,  # 2025-12-23T10:30:45.456Z
        checkpoint_session_1,  # 2025-12-22T15:30:45.123Z
        extra_checkpoint_2,    # 2025-12-21T12:45:30.500Z
        checkpoint_old_session,  # 2025-11-15T10:00:00.000Z
    ]
    return checkpoints


# ============================================================================
# Resume State Fixtures
# ============================================================================

@pytest.fixture
def expected_resume_state_phase_1(
    fixed_session_id: str,
    valid_brainstorm_context: Dict[str, Any]
) -> Dict[str, Any]:
    """Expected resume state after Phase 1"""
    return {
        "session_id": fixed_session_id,
        "current_phase": 1,
        "phase_completed": True,
        "brainstorm_context": valid_brainstorm_context,
        "next_phase": 2,
        "should_replay": False,
    }


@pytest.fixture
def expected_resume_state_phase_3(
    fixed_session_id: str,
    valid_brainstorm_context: Dict[str, Any]
) -> Dict[str, Any]:
    """Expected resume state after Phase 3"""
    return {
        "session_id": fixed_session_id,
        "current_phase": 3,
        "phase_completed": True,
        "brainstorm_context": valid_brainstorm_context,
        "next_phase": 4,
        "should_replay": False,
    }


# ============================================================================
# Edge Case Fixtures
# ============================================================================

@pytest.fixture
def checkpoint_deleted_between_detection_and_load(
    checkpoint_phase_1: Dict[str, Any]
) -> None:
    """Simulate checkpoint file deleted between detection and load"""
    return None


@pytest.fixture
def checkpoint_corrupted_partial_data(
    fixed_session_id: str,
) -> Dict[str, Any]:
    """Checkpoint with partial phase data (not fully completed)"""
    return {
        "session_id": fixed_session_id,
        "timestamp": "2025-12-22T15:30:45.123Z",
        "current_phase": 2,
        "phase_completed": False,  # Incomplete
        "brainstorm_context": {
            "problem_statement": "Partial data",
            # Missing: personas, requirements, complexity_score, epics
        }
    }
