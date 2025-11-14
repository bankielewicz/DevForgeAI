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


@pytest.fixture(scope="function")
def setup_feedback_sessions(request, monkeypatch):
    """Create test feedback sessions for export/import tests (requires explicit request)."""
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

    # Create SAFE temporary feedback directory with sample sessions
    # Use /tmp/test_feedback_junk/ instead of production .devforgeai/feedback/
    import tempfile
    import shutil

    # Create unique temporary directory for this test run
    temp_root = Path(tempfile.gettempdir()) / "test_feedback_junk"
    feedback_dir = temp_root / "feedback" / "sessions"
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

    # Cleanup: SAFELY remove ONLY the test junk directory
    # This will NEVER touch production .devforgeai/feedback/
    if temp_root.exists():
        shutil.rmtree(temp_root)


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
    """Configure pytest with custom markers for all test suites"""
    markers = [
        "unit: mark test as a unit test (isolated from external dependencies)",
        "integration: mark test as an integration test (tests component interactions)",
        "edge_case: mark test as testing edge cases or boundary conditions",
        "security: mark test as testing security requirements or data protection",
        "performance: mark test as testing performance requirements and timeouts",
        "acceptance_criteria: mark test as directly testing AC requirement",
        "e2e: mark test as an end-to-end test (real-world usage)",
        "slow: mark test as slow (may take >1 second)",
        "deterministic: mark test as deterministic (no flaky failures)",
        "story_015: mark test as part of STORY-015 DoD template test suite",
        "usability: mark test as testing usability requirements",
        "reliability: mark test as testing reliability requirements",
    ]

    for marker_line in markers:
        config.addinivalue_line("markers", marker_line)


# ============================================================================
# STORY-015 Test Suite Fixtures and Helpers
# ============================================================================


@pytest.fixture(scope="session")
def project_root_015():
    """Fixture: Project root directory for STORY-015 tests."""
    return Path(__file__).parent.parent


@pytest.fixture(scope="session")
def story_template_path_015(project_root_015):
    """
    Fixture: Path to story template file for STORY-015 tests (session scope).

    Returns:
        Path: Path to the story template file

    Raises:
        RuntimeError: If story template file not found (fails test, not skips)
    """
    path = project_root_015 / ".claude/skills/devforgeai-story-creation/assets/templates/story-template.md"
    if not path.exists():
        pytest.fail(f"Story template file not found: {path}")
    return path


@pytest.fixture(scope="session")
def story_files_015(project_root_015):
    """
    Fixture: List of story files for STORY-015 tests (session scope).

    Validates that all required story files exist before tests begin.

    Returns:
        dict: Mapping of story IDs to Path objects

    Raises:
        RuntimeError: If any required story file not found (fails test, not skips)
    """
    story_ids = ["STORY-027", "STORY-028", "STORY-029"]
    stories = {}
    story_dir = project_root_015 / ".ai_docs/Stories"

    for story_id in story_ids:
        # Find story file matching pattern
        matching_files = list(story_dir.glob(f"{story_id}*"))
        if not matching_files:
            pytest.fail(f"Story file not found: {story_id}*")
        stories[story_id] = matching_files[0]

    return stories


# ============================================================================
# STORY-015 Helper Functions - Centralized for Single Source of Truth
# ============================================================================


def extract_dod_section(content):
    """
    Helper: Extract Definition of Done section from markdown content.

    Extracts the text between '## Definition of Done' and '## Notes' markers.

    Args:
        content (str): Full markdown content of a story file

    Returns:
        str: The DoD section including the header, or None if section not found

    Example:
        >>> content = "## Definition of Done\\n- [ ] Item\\n## Notes\\nText"
        >>> section = extract_dod_section(content)
        >>> "Implementation" in section
        True
    """
    dod_start = content.find("## Definition of Done")
    notes_start = content.find("## Notes")

    if dod_start == -1 or notes_start == -1:
        return None

    return content[dod_start:notes_start]


def extract_yaml_frontmatter(content):
    """
    Helper: Extract YAML frontmatter from markdown content.

    Extracts the YAML metadata block between opening and closing '---' delimiters.
    Validates proper YAML structure.

    Args:
        content (str): Full markdown content of a story file

    Returns:
        str: YAML content without delimiters

    Raises:
        ValueError: If YAML delimiters missing or malformed

    Example:
        >>> content = "---\\nid: STORY-001\\n---\\n## Content"
        >>> yaml_text = extract_yaml_frontmatter(content)
        >>> "id: STORY-001" in yaml_text
        True
    """
    lines = content.split("\n")

    if not lines or lines[0].strip() != "---":
        raise ValueError("Content missing opening '---' YAML delimiter")

    # Find closing delimiter (search up to line 15 to avoid scanning entire content)
    closing_idx = None
    for i in range(1, min(15, len(lines))):
        if lines[i].strip() == "---":
            closing_idx = i
            break

    if closing_idx is None:
        raise ValueError("Content missing closing '---' YAML delimiter")

    return "\n".join(lines[1:closing_idx])


def extract_section_headers(content):
    """
    Helper: Extract all section headers from markdown content.

    Finds all top-level (##) markdown headers in order of appearance.

    Args:
        content (str): Full markdown content of a story file

    Returns:
        list: Ordered list of header strings (e.g., ['## Title', '## Content'])

    Example:
        >>> content = "## Section 1\\nText\\n## Section 2\\nMore text"
        >>> headers = extract_section_headers(content)
        >>> headers == ['## Section 1', '## Section 2']
        True
    """
    import re

    pattern = r"^## (.+)$"
    headers = []

    for line in content.split("\n"):
        match = re.match(pattern, line)
        if match:
            headers.append(f"## {match.group(1)}")

    return headers


def extract_dod_subsections(dod_section):
    """
    Helper: Extract subsection headers from DoD section.

    Finds all third-level (###) markdown headers within the DoD section.
    Used to validate DoD structure consistency.

    Args:
        dod_section (str): The DoD section (typically from extract_dod_section)

    Returns:
        list: Ordered list of subsection headers (e.g., ['### Implementation', '### Quality'])

    Example:
        >>> dod = "## Definition of Done\\n### Implementation\\n### Quality"
        >>> subs = extract_dod_subsections(dod)
        >>> "### Implementation" in subs
        True
    """
    import re

    pattern = r"^### (.+)$"
    subsections = []

    for line in dod_section.split("\n"):
        match = re.match(pattern, line)
        if match:
            subsections.append(f"### {match.group(1)}")

    return subsections

