"""
Shared fixtures for STORY-228 test suite.

This conftest.py provides common test data fixtures used across
AC#1, AC#2, and AC#3 test files.
"""

import pytest
from typing import List, Dict, Any
from pathlib import Path


# ============================================================================
# Project Root Fixture
# ============================================================================

@pytest.fixture
def project_root() -> Path:
    """Return project root directory"""
    return Path(__file__).parent.parent.parent


# ============================================================================
# Session Entry Fixtures
# ============================================================================

@pytest.fixture
def minimal_session_entries() -> List[Dict[str, Any]]:
    """Minimal session data for basic tests"""
    return [
        {
            "timestamp": "2025-01-02T10:00:00Z",
            "command": "/dev",
            "status": "success",
            "session_id": "session-001",
            "duration_ms": 5000
        },
        {
            "timestamp": "2025-01-02T10:30:00Z",
            "command": "/qa",
            "status": "success",
            "session_id": "session-001",
            "duration_ms": 3000
        }
    ]


@pytest.fixture
def multi_session_entries() -> List[Dict[str, Any]]:
    """Session data from multiple sessions with different paths"""
    return [
        # Session 1: /ideate -> /create-story -> /dev -> /qa
        {"timestamp": "2025-01-02T10:00:00Z", "command": "/ideate", "status": "success", "session_id": "s1"},
        {"timestamp": "2025-01-02T10:05:00Z", "command": "/create-story", "status": "success", "session_id": "s1"},
        {"timestamp": "2025-01-02T10:10:00Z", "command": "/dev", "status": "success", "session_id": "s1"},
        {"timestamp": "2025-01-02T10:45:00Z", "command": "/qa", "status": "success", "session_id": "s1"},

        # Session 2: /ideate -> /brainstorm
        {"timestamp": "2025-01-02T11:00:00Z", "command": "/ideate", "status": "success", "session_id": "s2"},
        {"timestamp": "2025-01-02T11:05:00Z", "command": "/brainstorm", "status": "success", "session_id": "s2"},

        # Session 3: /ideate -> /create-context
        {"timestamp": "2025-01-02T12:00:00Z", "command": "/ideate", "status": "success", "session_id": "s3"},
        {"timestamp": "2025-01-02T12:05:00Z", "command": "/create-context", "status": "success", "session_id": "s3"},

        # Session 4: /dev -> /rca (error path)
        {"timestamp": "2025-01-02T13:00:00Z", "command": "/dev", "status": "error", "session_id": "s4"},
        {"timestamp": "2025-01-02T13:30:00Z", "command": "/rca", "status": "success", "session_id": "s4"},

        # Session 5: /dev -> /qa (success path)
        {"timestamp": "2025-01-02T14:00:00Z", "command": "/dev", "status": "success", "session_id": "s5"},
        {"timestamp": "2025-01-02T14:30:00Z", "command": "/qa", "status": "success", "session_id": "s5"},
    ]


@pytest.fixture
def comprehensive_session_data() -> List[Dict[str, Any]]:
    """
    Comprehensive session data for testing all AC scenarios.

    Branching points:
    - /ideate -> /create-story (4x), /brainstorm (3x), /create-context (3x)
    - /dev -> /qa (7x), /rca (3x)
    - /qa -> /release (6x), /dev (4x)
    """
    data = []
    session_counter = 0

    # /ideate branching (10 sessions)
    paths_from_ideate = [
        ("/create-story", 4),
        ("/brainstorm", 3),
        ("/create-context", 3)
    ]
    for next_cmd, count in paths_from_ideate:
        for _ in range(count):
            session_counter += 1
            session_id = f"ideate-{session_counter}"
            data.append({
                "timestamp": f"2025-01-02T{10+session_counter}:00:00Z",
                "command": "/ideate",
                "status": "success",
                "session_id": session_id
            })
            data.append({
                "timestamp": f"2025-01-02T{10+session_counter}:30:00Z",
                "command": next_cmd,
                "status": "success",
                "session_id": session_id
            })

    # /dev branching (10 sessions)
    paths_from_dev = [
        ("/qa", "success", 7),
        ("/rca", "error", 3)
    ]
    for next_cmd, status, count in paths_from_dev:
        for _ in range(count):
            session_counter += 1
            session_id = f"dev-{session_counter}"
            data.append({
                "timestamp": f"2025-01-02T{10+session_counter}:00:00Z",
                "command": "/dev",
                "status": status,
                "session_id": session_id
            })
            data.append({
                "timestamp": f"2025-01-02T{10+session_counter}:30:00Z",
                "command": next_cmd,
                "status": "success",
                "session_id": session_id
            })

    # /qa branching (10 sessions)
    paths_from_qa = [
        ("/release", 6),
        ("/dev", 4)  # Retry loop
    ]
    for next_cmd, count in paths_from_qa:
        for _ in range(count):
            session_counter += 1
            session_id = f"qa-{session_counter}"
            data.append({
                "timestamp": f"2025-01-02T{10+session_counter}:00:00Z",
                "command": "/qa",
                "status": "success",
                "session_id": session_id
            })
            data.append({
                "timestamp": f"2025-01-02T{10+session_counter}:30:00Z",
                "command": next_cmd,
                "status": "success",
                "session_id": session_id
            })

    return data


# ============================================================================
# Expected Results Fixtures
# ============================================================================

@pytest.fixture
def expected_branching_points() -> Dict[str, Dict]:
    """
    Expected branching points from comprehensive_session_data.

    Provides expected output for validation.
    """
    return {
        "/ideate": {
            "downstream": {
                "/create-story": {"frequency": 4},
                "/brainstorm": {"frequency": 3},
                "/create-context": {"frequency": 3}
            }
        },
        "/dev": {
            "downstream": {
                "/qa": {"frequency": 7},
                "/rca": {"frequency": 3}
            }
        },
        "/qa": {
            "downstream": {
                "/release": {"frequency": 6},
                "/dev": {"frequency": 4}
            }
        }
    }


@pytest.fixture
def expected_probabilities() -> Dict[str, Dict]:
    """
    Expected probability distributions.

    /ideate: 40% create-story, 30% brainstorm, 30% create-context
    /dev: 70% qa, 30% rca
    /qa: 60% release, 40% dev
    """
    return {
        "/ideate": {
            "/create-story": 0.40,
            "/brainstorm": 0.30,
            "/create-context": 0.30
        },
        "/dev": {
            "/qa": 0.70,
            "/rca": 0.30
        },
        "/qa": {
            "/release": 0.60,
            "/dev": 0.40
        }
    }


# ============================================================================
# Pytest Markers
# ============================================================================

def pytest_configure(config):
    """Register custom markers."""
    config.addinivalue_line(
        "markers", "acceptance_criteria: marks tests covering AC requirements"
    )
    config.addinivalue_line(
        "markers", "edge_case: marks tests for edge case scenarios"
    )
    config.addinivalue_line(
        "markers", "unit: marks unit tests (70% of pyramid)"
    )
    config.addinivalue_line(
        "markers", "integration: marks integration tests (20% of pyramid)"
    )
