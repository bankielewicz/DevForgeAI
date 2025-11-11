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

