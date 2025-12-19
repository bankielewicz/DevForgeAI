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
        from tests.helpers.devforgeai.operation_context import clearOperationStore
        clearOperationStore()
    except ImportError:
        pass  # Module not yet implemented
    yield
    try:
        from tests.helpers.devforgeai.operation_context import clearOperationStore
        clearOperationStore()
    except ImportError:
        pass


def pytest_configure(config):
    """Configure pytest with custom markers for all test suites"""
    markers = [
        "unit: mark test as a unit test (isolated from external dependencies)",
        "integration: mark test as an integration test (tests component interactions)",
        "regression: mark test as a regression test (tests backward compatibility)",
        "performance: mark test as testing performance requirements and timeouts",
        "edge_case: mark test as testing edge cases or boundary conditions",
        "security: mark test as testing security requirements or data protection",
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


# ============================================================================
# STORY-105: Test Cleanup Fixtures - Automatic temp file management
# ============================================================================

import json
import zipfile


@pytest.fixture
def temp_zip_dir():
    """
    Fixture: Temporary directory for creating test zip files.

    All files created in this directory are automatically cleaned up
    after the test completes (success or failure).

    Yields:
        Path: Path to the temporary directory

    Example:
        def test_example(temp_zip_dir):
            zip_path = temp_zip_dir / "test.zip"
            with zipfile.ZipFile(zip_path, 'w') as zf:
                zf.writestr("file.txt", "content")
            # zip_path automatically cleaned up after test
    """
    with tempfile.TemporaryDirectory(prefix="test_zip_") as tmpdir:
        yield Path(tmpdir)


@pytest.fixture
def create_test_zip(temp_zip_dir):
    """
    Fixture: Factory for creating test zip files with automatic cleanup.

    Returns a function that creates zip files in a temporary directory.
    All created files are automatically cleaned up after the test.

    Args:
        temp_zip_dir: The temporary directory fixture

    Yields:
        Callable: Function to create test zip files

    Example:
        def test_example(create_test_zip):
            zip_path = create_test_zip({
                "feedback-sessions/s.md": "content",
                "index.json": '{"sessions": []}',
                "manifest.json": '{}'
            })
            # Use zip_path in test
            # Automatically cleaned up after test
    """
    def _create(files: dict, prefix: str = "test") -> Path:
        """
        Create a test zip file with the specified contents.

        Args:
            files: Dictionary mapping filenames to content strings
            prefix: Optional prefix for the zip filename

        Returns:
            Path: Path to the created zip file
        """
        zip_path = temp_zip_dir / f"{prefix}_{uuid4().hex[:8]}.zip"
        with zipfile.ZipFile(zip_path, 'w') as zf:
            for filename, content in files.items():
                zf.writestr(filename, content)
        return zip_path

    return _create


@pytest.fixture
def valid_import_zip(create_test_zip):
    """
    Fixture: Pre-built valid import zip for testing.

    Creates a zip file with the standard structure expected by
    import_feedback_sessions: index.json, manifest.json, and
    feedback-sessions/ directory.

    Args:
        create_test_zip: The factory fixture for creating zips

    Returns:
        Path: Path to the valid import zip file

    Example:
        def test_import(valid_import_zip):
            from feedback_export_import import import_feedback_sessions
            result = import_feedback_sessions(archive_path=str(valid_import_zip))
            assert result["success"] is True
    """
    session_id = str(uuid4())
    return create_test_zip({
        "feedback-sessions/session1.md": "Sample feedback content",
        "index.json": json.dumps({
            "export_metadata": {
                "created_at": "2025-11-07T14:30:00Z",
                "exported_sessions_count": 1,
                "date_range": "last-30-days",
                "sanitization_applied": True,
                "framework_version": "1.0.1"
            },
            "sessions": [{
                "session_id": session_id,
                "timestamp": "2025-11-07T10:30:00Z",
                "operation_type": "command",
                "status": "success",
                "file_size_bytes": 100
            }]
        }),
        "manifest.json": json.dumps({
            "export_version": "1.0",
            "framework_version": "1.0.1",
            "min_framework_version": "1.0.0",
            "session_count": 1
        })
    }, prefix="valid_import")


@pytest.fixture
def larger_import_zip(create_test_zip):
    """
    Fixture: Larger import zip with many sessions for progress testing.

    Creates a zip file with 50+ session files to test progress indication
    and bulk operations.

    Args:
        create_test_zip: The factory fixture for creating zips

    Returns:
        Path: Path to the larger import zip file
    """
    files = {}
    sessions = []

    for i in range(50):
        session_id = str(uuid4())
        files[f"feedback-sessions/session{i}.md"] = f"Sample feedback content {i}" * 10
        sessions.append({
            "session_id": session_id,
            "timestamp": f"2025-11-{7+i%20:02d}T10:30:00Z",
            "operation_type": "command",
            "status": "success",
            "file_size_bytes": 100 + i * 10
        })

    files["index.json"] = json.dumps({
        "export_metadata": {
            "created_at": "2025-11-07T14:30:00Z",
            "exported_sessions_count": len(sessions),
            "date_range": "last-30-days",
            "sanitization_applied": True,
            "framework_version": "1.0.1"
        },
        "sessions": sessions
    })

    files["manifest.json"] = json.dumps({
        "export_version": "1.0",
        "framework_version": "1.0.1",
        "min_framework_version": "1.0.0",
        "session_count": len(sessions)
    })

    return create_test_zip(files, prefix="larger_import")


@pytest.fixture(autouse=False)
def verify_no_orphan_zips():
    """
    Fixture: Verify no orphaned zip files in project root after test.

    When used (not autouse by default), this fixture checks that no
    new .zip files were left in the project root after the test.

    Note: Set autouse=False to avoid impacting unrelated tests.
    Enable explicitly in test modules that create zip files.

    Yields:
        None

    Raises:
        pytest.fail: If orphaned zip files are found
    """
    project_root = Path(__file__).parent.parent

    # Record zip files before test
    before = set(project_root.glob("*.zip"))

    yield

    # Check for new zip files after test
    after = set(project_root.glob("*.zip"))
    orphans = after - before

    if orphans:
        # Clean up orphans for test hygiene
        for orphan in orphans:
            try:
                orphan.unlink()
            except Exception:
                pass

        pytest.fail(
            f"Test left orphaned zip files in project root: {[str(o.name) for o in orphans]}"
        )

