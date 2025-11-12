"""pytest configuration for DevForgeAI STORY-017 tests."""

import sys
import pytest
import tempfile
import shutil
from pathlib import Path
from datetime import datetime, timedelta, timezone
import os

# Add src directory to Python path so tests can import modules
project_root = Path(__file__).parent.parent
src_dir = project_root / "src"

if str(src_dir) not in sys.path:
    sys.path.insert(0, str(src_dir))


@pytest.fixture(scope="function", autouse=True)
def setup_feedback_sessions(request, monkeypatch):
    """Automatically create test feedback sessions for export/import tests."""
    # Check if this test uses temp_project_dir fixture
    if 'temp_project_dir' in request.fixturenames:
        # Test uses temp_project_dir - monkeypatch cwd to temp_project_dir
        # so that export/import functions work correctly within temp directory
        temp_dir = request.getfixturevalue('temp_project_dir')
        original_cwd = os.getcwd()
        monkeypatch.chdir(temp_dir)
        yield
        os.chdir(original_cwd)
        return

    # Create temporary feedback directory with sample sessions
    feedback_dir = Path(".devforgeai/feedback/sessions")
    feedback_dir.mkdir(parents=True, exist_ok=True)

    # Create sample feedback session files for testing
    base_time = datetime(2025, 10, 8, 0, 0, 0, tzinfo=timezone.utc)

    for i in range(15):
        timestamp = base_time + timedelta(days=i, hours=i*2)
        timestamp_str = timestamp.strftime("%Y-%m-%dT%H-%M-%S")

        filename = f"{timestamp_str}-command-dev-success.md"
        content = f"""# Feedback Session {i}

Operation: /dev STORY-{42+i}
Status: success
Timestamp: {timestamp.isoformat()}Z

## Content
Feedback for STORY-{42+i}. Project path: /home/user/my-project.
Custom field: sensitive_value_{i}

Repository: git@github.com:user/my-repo.git
Details about the operation execution and feedback...
"""

        session_file = feedback_dir / filename
        with open(session_file, 'w', encoding='utf-8') as f:
            f.write(content)

    yield

    # Cleanup: remove the feedback directory after test
    import shutil
    if Path(".devforgeai").exists():
        # Only remove feedback directory, not all .devforgeai
        if (Path(".devforgeai/feedback")).exists():
            shutil.rmtree(Path(".devforgeai/feedback"))


# ========== STORY-019: Operation Context Extraction Fixtures ==========

from uuid import uuid4


@pytest.fixture
def simple_operation_context():
    """Fixture: Simple completed operation with 5 todos"""
    return {
        "operation_id": str(uuid4()),
        "operation_type": "dev",
        "story_id": "STORY-001",
        "start_time": "2025-11-07T10:00:00Z",
        "end_time": "2025-11-07T10:35:42Z",
        "duration_seconds": 2142,
        "status": "completed",
        "todo_summary": {
            "total": 5,
            "completed": 5,
            "failed": 0,
            "skipped": 0,
            "completion_rate": 1.0,
        },
        "todos": [
            {
                "id": 1,
                "name": "Generate failing tests",
                "status": "done",
                "timestamp": "2025-11-07T10:00:00Z",
            },
            {
                "id": 2,
                "name": "Implement red phase",
                "status": "done",
                "timestamp": "2025-11-07T10:10:00Z",
            },
            {
                "id": 3,
                "name": "Run test suite",
                "status": "done",
                "timestamp": "2025-11-07T10:20:00Z",
            },
            {
                "id": 4,
                "name": "Refactor code",
                "status": "done",
                "timestamp": "2025-11-07T10:30:00Z",
            },
            {
                "id": 5,
                "name": "Final validation",
                "status": "done",
                "timestamp": "2025-11-07T10:35:42Z",
            },
        ],
        "error": None,
        "phases": {
            "red": {"duration_seconds": 420, "success": True},
            "green": {"duration_seconds": 480, "success": True},
            "refactor": {"duration_seconds": 1242, "success": True},
        },
    }


@pytest.fixture
def failed_operation_context():
    """Fixture: Failed operation with error context"""
    return {
        "operation_id": str(uuid4()),
        "operation_type": "dev",
        "story_id": "STORY-002",
        "start_time": "2025-11-07T10:00:00Z",
        "end_time": "2025-11-07T10:25:30Z",
        "duration_seconds": 1530,
        "status": "failed",
        "todo_summary": {
            "total": 5,
            "completed": 3,
            "failed": 1,
            "skipped": 1,
            "completion_rate": 0.6,
        },
        "todos": [
            {"id": 1, "name": "Generate failing tests", "status": "done", "timestamp": "2025-11-07T10:00:00Z"},
            {"id": 2, "name": "Implement red phase", "status": "done", "timestamp": "2025-11-07T10:10:00Z"},
            {"id": 3, "name": "Run test suite", "status": "done", "timestamp": "2025-11-07T10:20:00Z"},
            {"id": 4, "name": "Git commit", "status": "failed", "timestamp": "2025-11-07T10:25:30Z", "notes": "Authentication failed"},
            {"id": 5, "name": "Push to remote", "status": "skipped", "timestamp": None},
        ],
        "error": {
            "message": "Git commit failed: authentication required",
            "type": "GitAuthenticationError",
            "timestamp": "2025-11-07T10:25:30Z",
            "failed_todo_id": 4,
            "stack_trace": "GitAuthenticationError: Authentication required",
        },
        "phases": {
            "red": {"duration_seconds": 420, "success": True},
            "green": {"duration_seconds": 480, "success": True},
            "refactor": {"duration_seconds": 630, "success": False},
        },
    }


@pytest.fixture
def feedback_session_id():
    """Fixture: Generate a feedback session ID"""
    return str(uuid4())


@pytest.fixture
def extraction_options():
    """Fixture: Standard extraction options"""
    return {
        "includeSanitization": True,
        "includeSummary": True,
        "maxContextSize": 50000,
    }


@pytest.fixture
def iso8601_timestamp():
    """Fixture: Generate ISO8601 timestamp"""
    return datetime.utcnow().isoformat() + "Z"


@pytest.fixture
def uuid_id():
    """Fixture: Generate UUID"""
    return str(uuid4())


@pytest.fixture(autouse=True)
def clear_operation_store():
    """Automatically clear operation store before each test"""
    try:
        from devforgeai.operation_context import clearOperationStore
        clearOperationStore()
    except ImportError:
        pass  # Module not yet implemented
    yield
    try:
        from devforgeai.operation_context import clearOperationStore
        clearOperationStore()
    except ImportError:
        pass


def pytest_configure(config):
    """Configure pytest with custom markers for STORY-019 tests"""
    markers = [
        "unit: mark test as a unit test (isolated from external dependencies)",
        "integration: mark test as an integration test (tests component interactions)",
        "edge_case: mark test as testing edge cases or boundary conditions",
        "security: mark test as testing security requirements or data protection",
        "performance: mark test as testing performance requirements and timeouts",
        "acceptance_criteria: mark test as directly testing AC requirement",
    ]

    for marker_line in markers:
        config.addinivalue_line("markers", marker_line)

