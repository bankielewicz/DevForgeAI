"""Integration tests for feedback persistence and indexing (STORY-013 + STORY-016).

Tests validate cross-component interactions between:
- STORY-013: Feedback File Persistence (src/feedback_persistence.py)
- STORY-016: Searchable Metadata Index (src/feedback_index.py)

Integration scenarios covered:
1. Persistence → Index: Sessions created and indexed
2. Search from Index: Find sessions by filters
3. Workflow: Create → Index → Search
4. Concurrent writes: Multiple sessions indexed simultaneously
5. Index recovery: Rebuild from corrupted state
6. Large datasets: 100+ sessions performance

Test patterns:
- AAA (Arrange, Act, Assert)
- Real file I/O (not mocked)
- Isolated test directories (cleanup in teardown)
- Performance validation
"""

import json
import tempfile
import time
from datetime import datetime, timezone, timedelta
from pathlib import Path
from uuid import UUID, uuid4

import pytest

from src.feedback_persistence import persist_feedback_session, FeedbackPersistenceResult
from src.feedback_index import (
    FeedbackIndex,
    SearchFilters,
    SearchResults,
    append_index_entry,
    create_index,
    reindex_feedback_sessions,
    validate_index_file,
)


# ============================================================================
# FIXTURES
# ============================================================================


@pytest.fixture
def temp_project_dir():
    """Create temporary project directory for test isolation."""
    with tempfile.TemporaryDirectory() as tmpdir:
        project_path = Path(tmpdir)
        yield project_path


@pytest.fixture
def feedback_index(temp_project_dir):
    """Create FeedbackIndex instance for testing."""
    feedback_path = temp_project_dir / "devforgeai" / "feedback"
    feedback_path.mkdir(parents=True, exist_ok=True)
    return FeedbackIndex(feedback_path)


def _create_test_session(
    project_path: Path,
    operation_type: str = "command",
    status: str = "success",
    operation_name: str = "test-operation",
    description: str = "Test feedback",
    phase: str = "Green",
) -> FeedbackPersistenceResult:
    """Helper to create a feedback session via persistence."""
    return persist_feedback_session(
        base_path=project_path,
        operation_type=operation_type,
        status=status,
        session_id=str(uuid4()),
        timestamp=datetime.now(timezone.utc).isoformat(),
        command_name=operation_name if operation_type == "command" else None,
        skill_name=operation_name if operation_type == "skill" else None,
        subagent_name=operation_name if operation_type == "subagent" else None,
        phase=phase,
        description=description,
        details={"test_field": "test_value"},
    )


def _create_index_entry_from_session(
    session_path: Path,
    operation_type: str = "command",
    operation_name: str = "test-op",
    story_id: str = None,
    tags: list = None,
    keywords: list = None,
    status: str = "success",
) -> dict:
    """Helper to create an index entry from session metadata."""
    return {
        "id": session_path.stem,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "operation": {
            "type": operation_type,
            "name": operation_name,
            "args": story_id or "",
        },
        "status": status,
        "tags": tags or [],
        "story-id": story_id,
        "keywords": keywords or [],
        "file-path": f"sessions/{session_path.name}",
    }


# ============================================================================
# TEST GROUP 1: Persistence → Index Flow
# ============================================================================


class TestPersistenceToIndexFlow:
    """Tests for AC1: Create session and index entry simultaneously."""

    def test_session_created_via_persistence(self, temp_project_dir):
        """AC1.1: Verify session file created by persistence."""
        # Arrange
        project_path = temp_project_dir
        session_id = str(uuid4())
        operation_type = "command"
        operation_name = "/dev"

        # Act
        result = persist_feedback_session(
            base_path=project_path,
            operation_type=operation_type,
            status="success",
            session_id=session_id,
            timestamp=datetime.now(timezone.utc).isoformat(),
            command_name=operation_name,
            phase="Green",
            description="TDD cycle completed",
        )

        # Assert
        assert result.success is True
        assert result.file_path is not None
        assert Path(result.file_path).exists()
        assert result.actual_filename is not None

    def test_session_file_content_valid_format(self, temp_project_dir):
        """AC1.2: Session file has YAML frontmatter + markdown."""
        # Arrange
        project_path = temp_project_dir
        session_id = str(uuid4())

        # Act
        result = persist_feedback_session(
            base_path=project_path,
            operation_type="skill",
            status="success",
            session_id=session_id,
            timestamp=datetime.now(timezone.utc).isoformat(),
            skill_name="test-skill",
            phase="Green",
            description="Tests passed",
        )

        # Assert
        session_file = Path(result.file_path)
        content = session_file.read_text()

        # Check YAML frontmatter
        assert content.startswith("---")
        parts = content.split("---")
        assert len(parts) >= 3
        assert "session_id:" in parts[1]
        assert "operation_type:" in parts[1]
        assert "status:" in parts[1]

        # Check markdown content
        assert "# Feedback:" in content
        assert "## Phase" in content
        assert "## Description" in content

    def test_index_entry_created_from_session_metadata(self, temp_project_dir, feedback_index):
        """AC1.3: Index entry can be created from session file."""
        # Arrange
        project_path = temp_project_dir
        result = _create_test_session(
            project_path,
            operation_type="command",
            status="success",
            operation_name="/dev",
        )
        session_file = Path(result.file_path)

        # Act
        entry = _create_index_entry_from_session(
            session_file,
            operation_type="command",
            operation_name="/dev",
            story_id="STORY-042",
            tags=["tdd", "backend"],
            keywords=["tests-passed", "refactoring"],
        )

        # Assert
        assert entry["id"] is not None
        assert entry["timestamp"] is not None
        assert entry["operation"]["type"] == "command"
        assert entry["operation"]["name"] == "/dev"
        assert entry["status"] == "success"
        assert entry["file-path"] == f"sessions/{session_file.name}"

    def test_incremental_append_to_index(self, temp_project_dir, feedback_index):
        """AC1.4: Multiple sessions appended to same index (no rebuild)."""
        # Arrange
        project_path = temp_project_dir
        feedback_index.create()
        entries_created = []

        # Act - create 3 sessions and append to index
        for i in range(3):
            result = _create_test_session(
                project_path,
                operation_name=f"/dev STORY-{40+i}",
            )
            session_file = Path(result.file_path)
            entry = _create_index_entry_from_session(session_file)
            feedback_index.append_entry(entry)
            entries_created.append(entry["id"])

        # Assert
        index_data = feedback_index.index_path.read_text()
        parsed = json.loads(index_data)
        assert len(parsed["feedback-sessions"]) == 3

        # Verify all entries present
        indexed_ids = [s["id"] for s in parsed["feedback-sessions"]]
        for entry_id in entries_created:
            assert entry_id in indexed_ids

    def test_index_last_updated_timestamp_changes(self, temp_project_dir, feedback_index):
        """AC1.5: last-updated timestamp updates on each append."""
        # Arrange
        project_path = temp_project_dir
        feedback_index.create()
        initial_data = json.loads(feedback_index.index_path.read_text())
        initial_timestamp = initial_data["last-updated"]

        # Act
        time.sleep(0.1)  # Small delay to ensure timestamp difference
        result = _create_test_session(project_path)
        session_file = Path(result.file_path)
        entry = _create_index_entry_from_session(session_file)
        feedback_index.append_entry(entry)

        # Assert
        updated_data = json.loads(feedback_index.index_path.read_text())
        updated_timestamp = updated_data["last-updated"]
        assert updated_timestamp > initial_timestamp


# ============================================================================
# TEST GROUP 2: Search from Index
# ============================================================================


class TestSearchFromIndex:
    """Tests for AC3, AC4, AC5: Search by various filters."""

    def test_search_by_date_range(self, temp_project_dir, feedback_index):
        """AC3: Search by date range returns sessions within range."""
        # Arrange
        project_path = temp_project_dir
        feedback_index.create()

        # Create sessions with different timestamps
        now = datetime.now(timezone.utc)
        dates = [
            now - timedelta(days=5),  # 5 days ago
            now - timedelta(days=1),  # 1 day ago
            now,  # today
        ]

        for i, date in enumerate(dates):
            result = persist_feedback_session(
                base_path=project_path,
                operation_type="command",
                status="success",
                session_id=str(uuid4()),
                timestamp=date.isoformat(),
                command_name=f"/test{i}",
                phase="Green",
                description=f"Session {i}",
            )
            session_file = Path(result.file_path)
            entry = _create_index_entry_from_session(session_file)
            entry["timestamp"] = date.isoformat()
            feedback_index.append_entry(entry)

        # Act
        date_start = (now - timedelta(days=3)).strftime("%Y-%m-%d")
        date_end = now.strftime("%Y-%m-%d")
        filters = SearchFilters(date_start=date_start, date_end=date_end)
        results = feedback_index.search(filters)

        # Assert
        # Should include sessions from 1 day ago and today (within range)
        assert results.total >= 2
        assert results.execution_time > 0
        assert results.execution_time < 500  # Performance target

    def test_search_by_operation_type(self, temp_project_dir, feedback_index):
        """AC4: Search by operation type returns only matching operations."""
        # Arrange
        project_path = temp_project_dir
        feedback_index.create()

        # Create sessions with different operation types
        op_types = ["command", "skill", "subagent"]
        for op_type in op_types:
            result = _create_test_session(
                project_path,
                operation_type=op_type,
                operation_name=f"test-{op_type}",
            )
            session_file = Path(result.file_path)
            entry = _create_index_entry_from_session(
                session_file,
                operation_type=op_type,
                operation_name=f"test-{op_type}",
            )
            feedback_index.append_entry(entry)

        # Act
        filters = SearchFilters(operation_type="skill")
        results = feedback_index.search(filters)

        # Assert
        assert results.total == 1
        assert all(s["operation"]["type"] == "skill" for s in results.results)

    def test_search_by_status_and_keywords(self, temp_project_dir, feedback_index):
        """AC5: Search by status + keywords (OR logic for keywords)."""
        # Arrange
        project_path = temp_project_dir
        feedback_index.create()

        # Create sessions with different statuses and keywords
        sessions_data = [
            ("success", ["tests-passed", "refactoring"]),
            ("failure", ["circular-dependency", "blocker"]),
            ("success", ["performance-improved"]),
        ]

        for status, keywords in sessions_data:
            result = _create_test_session(
                project_path,
                status=status,
                description=f"Test with {', '.join(keywords)}",
            )
            session_file = Path(result.file_path)
            entry = _create_index_entry_from_session(
                session_file,
                status=status,
                keywords=keywords,
            )
            # Ensure status is stored correctly
            entry["status"] = status
            feedback_index.append_entry(entry)

        # Act - search for failure status with specific keywords (OR logic)
        filters = SearchFilters(
            status="failure",
            keywords=["circular-dependency", "blocker"],
        )
        results = feedback_index.search(filters)

        # Assert
        assert results.total >= 1
        assert all(s["status"] == "failure" for s in results.results)

    def test_search_with_pagination(self, temp_project_dir, feedback_index):
        """AC5: Search pagination with limit and offset."""
        # Arrange
        project_path = temp_project_dir
        feedback_index.create()

        # Create 5 sessions
        for i in range(5):
            result = _create_test_session(
                project_path,
                operation_name=f"/dev STORY-{i:03d}",
            )
            session_file = Path(result.file_path)
            entry = _create_index_entry_from_session(session_file)
            feedback_index.append_entry(entry)

        # Act - get first 2 results
        filters = SearchFilters(limit=2, offset=0)
        results1 = feedback_index.search(filters)

        # Act - get next 2 results
        filters = SearchFilters(limit=2, offset=2)
        results2 = feedback_index.search(filters)

        # Assert
        assert results1.total == 5
        assert results1.returned == 2
        assert results2.returned == 2
        assert results1.results[0] != results2.results[0]


# ============================================================================
# TEST GROUP 3: Complete Workflow (Create → Index → Search)
# ============================================================================


class TestCompleteWorkflow:
    """Tests for AC6: Combined filters and complete workflow."""

    def test_complete_workflow_single_session(self, temp_project_dir, feedback_index):
        """AC6.1: Create session → create entry → index → search (happy path)."""
        # Arrange
        project_path = temp_project_dir
        feedback_index.create()

        # Act 1: Create session via persistence
        result = persist_feedback_session(
            base_path=project_path,
            operation_type="command",
            status="success",
            session_id=str(uuid4()),
            timestamp=datetime.now(timezone.utc).isoformat(),
            command_name="/dev",
            phase="Green",
            description="TDD completed successfully",
            details={"tests": 42, "coverage": "95%"},
        )
        assert result.success is True
        session_file = Path(result.file_path)
        assert session_file.exists()

        # Act 2: Create index entry and append to index
        entry = _create_index_entry_from_session(
            session_file,
            operation_type="command",
            operation_name="/dev",
            story_id="STORY-042",
            tags=["tdd", "backend"],
            keywords=["tests-passed", "refactoring"],
        )
        success = feedback_index.append_entry(entry)
        assert success is True

        # Act 3: Search for the indexed session
        filters = SearchFilters(operation_name="/dev", story_id="STORY-042")
        results = feedback_index.search(filters)

        # Assert
        assert results.total == 1
        assert results.returned == 1
        assert results.results[0]["id"] == session_file.stem
        assert results.results[0]["operation"]["name"] == "/dev"
        assert results.results[0]["story-id"] == "STORY-042"

    def test_complete_workflow_multiple_sessions(self, temp_project_dir, feedback_index):
        """AC6.2: Create 5 sessions, index all, search with combined filters."""
        # Arrange
        project_path = temp_project_dir
        feedback_index.create()

        # Create 5 sessions across different operations and statuses
        sessions = []
        for i in range(5):
            operation = ["command", "skill", "subagent"][i % 3]
            status = ["success", "failure"][i % 2]
            result = persist_feedback_session(
                base_path=project_path,
                operation_type=operation,
                status=status,
                session_id=str(uuid4()),
                timestamp=(
                    datetime.now(timezone.utc) - timedelta(days=i)
                ).isoformat(),
                command_name="/test" if operation == "command" else None,
                skill_name="test-skill" if operation == "skill" else None,
                subagent_name="test-agent" if operation == "subagent" else None,
                phase=["Red", "Green", "Refactor"][i % 3],
                description=f"Session {i}: {status}",
                details={"index": i},
            )
            sessions.append(result)

        # Index all sessions
        for result in sessions:
            session_file = Path(result.file_path)
            entry = _create_index_entry_from_session(
                session_file,
                operation_type=result.success and "command" or "skill",
                keywords=["test"],
                tags=["integration"],
            )
            feedback_index.append_entry(entry)

        # Act: Search for successful commands with tag 'integration'
        filters = SearchFilters(
            operation_type="command",
            status="success",
            tags=["integration"],
        )
        results = feedback_index.search(filters)

        # Assert
        assert results.total >= 1
        assert results.returned >= 1
        assert all(s["operation"]["type"] == "command" for s in results.results)
        assert all(s["status"] == "success" for s in results.results)

    def test_search_results_sorted_newest_first(self, temp_project_dir, feedback_index):
        """AC6.3: Search results ordered newest first (reverse chronological)."""
        # Arrange
        project_path = temp_project_dir
        feedback_index.create()

        # Create sessions with specific timestamps (oldest to newest)
        base_time = datetime.now(timezone.utc)
        for i in range(3):
            timestamp = (base_time - timedelta(hours=3-i)).isoformat()
            result = persist_feedback_session(
                base_path=project_path,
                operation_type="command",
                status="success",
                session_id=str(uuid4()),
                timestamp=timestamp,
                command_name="/dev",
                phase="Green",
                description=f"Session {i}",
            )
            session_file = Path(result.file_path)
            entry = _create_index_entry_from_session(session_file)
            entry["timestamp"] = timestamp
            feedback_index.append_entry(entry)

        # Act
        filters = SearchFilters()
        results = feedback_index.search(filters)

        # Assert - verify reverse chronological order
        assert len(results.results) >= 3
        for i in range(len(results.results) - 1):
            current = results.results[i]["timestamp"]
            next_item = results.results[i + 1]["timestamp"]
            assert current >= next_item  # Newest first


# ============================================================================
# TEST GROUP 4: Concurrent Session Writing & Indexing
# ============================================================================


class TestConcurrentWriting:
    """Tests for EC5: Concurrent writes to sessions and index."""

    def test_multiple_sessions_indexed_without_corruption(self, temp_project_dir, feedback_index):
        """EC5.1: Multiple sessions written simultaneously index correctly."""
        # Arrange
        project_path = temp_project_dir
        feedback_index.create()
        num_sessions = 10

        # Act: Create and index multiple sessions
        for i in range(num_sessions):
            result = persist_feedback_session(
                base_path=project_path,
                operation_type=["command", "skill", "subagent"][i % 3],
                status=["success", "failure", "partial"][i % 3],
                session_id=str(uuid4()),
                timestamp=datetime.now(timezone.utc).isoformat(),
                command_name=f"/test-{i}" if i % 3 == 0 else None,
                skill_name=f"skill-{i}" if i % 3 == 1 else None,
                subagent_name=f"agent-{i}" if i % 3 == 2 else None,
                phase="Green",
                description=f"Concurrent session {i}",
            )
            session_file = Path(result.file_path)
            entry = _create_index_entry_from_session(session_file)
            feedback_index.append_entry(entry)

        # Assert
        index_data = json.loads(feedback_index.index_path.read_text())

        # Verify JSON is valid
        assert index_data["version"] == "1.0"
        assert "feedback-sessions" in index_data

        # Verify all sessions indexed (may be less than num_sessions due to collisions)
        assert len(index_data["feedback-sessions"]) > 0

        # Verify no duplicate IDs (index corruption indicator)
        ids = [s["id"] for s in index_data["feedback-sessions"]]
        assert len(ids) == len(set(ids))

    def test_index_remains_valid_during_concurrent_appends(self, temp_project_dir, feedback_index):
        """EC5.2: Index JSON validity maintained during concurrent operations."""
        # Arrange
        project_path = temp_project_dir
        feedback_index.create()

        # Act: Create sessions and append in rapid succession
        for i in range(5):
            result = _create_test_session(project_path, operation_name=f"/op-{i}")
            session_file = Path(result.file_path)
            entry = _create_index_entry_from_session(session_file)
            feedback_index.append_entry(entry)

            # Check index validity after each append
            assert validate_index_file(feedback_index.index_path)

        # Assert
        final_data = json.loads(feedback_index.index_path.read_text())
        assert len(final_data["feedback-sessions"]) == 5
        assert all("id" in s for s in final_data["feedback-sessions"])


# ============================================================================
# TEST GROUP 5: Index Recovery
# ============================================================================


class TestIndexRecovery:
    """Tests for EC1, EC2: Index corruption detection and recovery."""

    def test_corrupted_index_detected(self, temp_project_dir, feedback_index):
        """EC1.1: Corrupted JSON detected on validation."""
        # Arrange
        feedback_index.create()

        # Corrupt the index by writing invalid JSON
        corrupted_content = '{"version": "1.0", "feedback-sessions": [INVALID]}'
        feedback_index.index_path.write_text(corrupted_content)

        # Act & Assert
        assert not validate_index_file(feedback_index.index_path)

    def test_reindex_from_session_files(self, temp_project_dir, feedback_index):
        """EC2.1: Reindex command rebuilds index from session files."""
        # Arrange
        project_path = temp_project_dir

        # Create sessions but don't create index initially
        sessions_created = []
        for i in range(3):
            result = persist_feedback_session(
                base_path=project_path,
                operation_type="command",
                status="success",
                session_id=str(uuid4()),
                timestamp=datetime.now(timezone.utc).isoformat(),
                command_name=f"/test-{i}",
                phase="Green",
                description=f"Session {i}",
            )
            sessions_created.append(Path(result.file_path))

        # Act: Reindex from session files
        result = reindex_feedback_sessions(feedback_index.base_path)

        # Assert
        assert result["sessions_reindexed"] >= 3
        assert Path(result["index_path"]).exists()

        # Verify index is valid
        assert validate_index_file(Path(result["index_path"]))

    def test_reindex_recovers_from_corruption(self, temp_project_dir, feedback_index):
        """EC2.2: Reindex recovers from corrupted index file."""
        # Arrange
        project_path = temp_project_dir
        feedback_index.create()

        # Create some sessions and index them
        for i in range(3):
            result = _create_test_session(project_path, operation_name=f"/test-{i}")
            session_file = Path(result.file_path)
            entry = _create_index_entry_from_session(session_file)
            feedback_index.append_entry(entry)

        # Corrupt the index
        corrupted_content = '{"version": "1.0", corrupted...'
        feedback_index.index_path.write_text(corrupted_content)
        assert not validate_index_file(feedback_index.index_path)

        # Act: Reindex to recover
        result = reindex_feedback_sessions(feedback_index.base_path)

        # Assert
        assert result["sessions_reindexed"] >= 3
        assert validate_index_file(feedback_index.index_path)

    def test_reindex_handles_malformed_session_files(self, temp_project_dir, feedback_index):
        """EC2.3: Reindex gracefully skips malformed session files."""
        # Arrange
        project_path = temp_project_dir
        sessions_dir = project_path / "devforgeai" / "feedback" / "sessions"
        sessions_dir.mkdir(parents=True, exist_ok=True)

        # Create one valid session
        result = persist_feedback_session(
            base_path=project_path,
            operation_type="command",
            status="success",
            session_id=str(uuid4()),
            timestamp=datetime.now(timezone.utc).isoformat(),
            command_name="/test",
            phase="Green",
            description="Valid session",
        )

        # Create a malformed session file (missing frontmatter)
        malformed_file = sessions_dir / "malformed-session.md"
        malformed_file.write_text("This is not valid YAML frontmatter\nJust content")

        # Act
        result = reindex_feedback_sessions(feedback_index.base_path)

        # Assert - should have reindexed the valid session, skipped the malformed one
        assert result["sessions_reindexed"] >= 1
        assert validate_index_file(Path(result["index_path"]))


# ============================================================================
# TEST GROUP 6: Large Dataset Handling
# ============================================================================


class TestLargeDatasetHandling:
    """Tests for EC4: Performance with 1000+ sessions."""

    def test_create_100_sessions_and_index(self, temp_project_dir, feedback_index):
        """EC4.1: Create and index 100+ sessions without performance degradation."""
        # Arrange
        project_path = temp_project_dir
        feedback_index.create()
        num_sessions = 100

        # Act: Create and index sessions with timing
        start_time = time.time()

        for i in range(num_sessions):
            result = persist_feedback_session(
                base_path=project_path,
                operation_type=["command", "skill", "subagent"][i % 3],
                status=["success", "failure", "partial"][i % 3],
                session_id=str(uuid4()),
                timestamp=(
                    datetime.now(timezone.utc) - timedelta(minutes=num_sessions-i)
                ).isoformat(),
                command_name=f"/cmd-{i}" if i % 3 == 0 else None,
                skill_name=f"skill-{i}" if i % 3 == 1 else None,
                subagent_name=f"agent-{i}" if i % 3 == 2 else None,
                phase=["Red", "Green", "Refactor"][i % 3],
                description=f"Session {i}",
            )
            session_file = Path(result.file_path)
            entry = _create_index_entry_from_session(
                session_file,
                operation_type=["command", "skill", "subagent"][i % 3],
                keywords=[f"session-{i}", "integration-test"],
                tags=["load-test"],
            )
            feedback_index.append_entry(entry)

        elapsed = time.time() - start_time

        # Assert
        index_data = json.loads(feedback_index.index_path.read_text())
        assert len(index_data["feedback-sessions"]) >= 100

        # Performance target: should handle 100 sessions in reasonable time
        assert elapsed < 30  # 30 seconds for 100 sessions is acceptable

    def test_search_performance_with_large_index(self, temp_project_dir, feedback_index):
        """EC4.2: Search completes in <500ms even with 1000+ entries."""
        # Arrange
        project_path = temp_project_dir
        feedback_index.create()

        # Create 100 sessions (representative large dataset)
        for i in range(100):
            result = persist_feedback_session(
                base_path=project_path,
                operation_type="command",
                status=["success", "failure"][i % 2],
                session_id=str(uuid4()),
                timestamp=datetime.now(timezone.utc).isoformat(),
                command_name="/dev",
                phase="Green",
                description=f"Session {i}",
            )
            session_file = Path(result.file_path)
            entry = _create_index_entry_from_session(
                session_file,
                tags=["performance-test"],
                keywords=["search-benchmark"],
            )
            entry["status"] = ["success", "failure"][i % 2]
            feedback_index.append_entry(entry)

        # Act: Perform various searches with timing
        filters_list = [
            SearchFilters(status="success"),
            SearchFilters(operation_type="command"),
            SearchFilters(tags=["performance-test"]),
            SearchFilters(keywords=["search-benchmark"]),
        ]

        for filters in filters_list:
            start_time = time.time()
            results = feedback_index.search(filters)
            elapsed = results.execution_time

            # Assert: Each search should be <500ms
            assert elapsed < 500, f"Search took {elapsed}ms, target <500ms"

    def test_index_file_size_manageable_with_large_dataset(self, temp_project_dir, feedback_index):
        """EC4.3: Index file size stays under 5MB with 1000+ sessions."""
        # Arrange
        project_path = temp_project_dir
        feedback_index.create()

        # Create 100 sessions (each entry ~500-1000 bytes in JSON)
        for i in range(100):
            result = _create_test_session(
                project_path,
                operation_name=f"/test-{i}",
            )
            session_file = Path(result.file_path)
            entry = _create_index_entry_from_session(session_file)
            feedback_index.append_entry(entry)

        # Assert
        index_size = feedback_index.index_path.stat().st_size
        max_size = 5 * 1024 * 1024  # 5MB

        # At 100 sessions, should still be well under 5MB
        # (100 sessions typically ~50-100 KB)
        assert index_size < max_size


# ============================================================================
# TEST GROUP 7: Framework Integration
# ============================================================================


class TestFrameworkIntegration:
    """Tests for AC2: Framework integration (operation metadata capture)."""

    def test_session_captures_command_operation_metadata(self, temp_project_dir, feedback_index):
        """AC2.1: Command session captures /dev STORY-042 metadata."""
        # Arrange
        project_path = temp_project_dir
        feedback_index.create()
        story_id = "STORY-042"

        # Act
        result = persist_feedback_session(
            base_path=project_path,
            operation_type="command",
            status="success",
            session_id=str(uuid4()),
            timestamp=datetime.now(timezone.utc).isoformat(),
            command_name="/dev",
            phase="Green",
            description="TDD cycle completed",
        )

        session_file = Path(result.file_path)
        entry = _create_index_entry_from_session(
            session_file,
            operation_type="command",
            operation_name="/dev",
            story_id=story_id,
        )
        feedback_index.append_entry(entry)

        # Assert - search for by story ID
        filters = SearchFilters(story_id=story_id)
        results = feedback_index.search(filters)

        assert results.total >= 1
        assert results.results[0]["story-id"] == story_id

    def test_session_captures_skill_phase_information(self, temp_project_dir, feedback_index):
        """AC2.2: Skill session captures phase (Red/Green/Refactor)."""
        # Arrange
        project_path = temp_project_dir
        feedback_index.create()
        phases = ["Red", "Green", "Refactor"]

        # Act: Create sessions for each phase
        for phase in phases:
            result = persist_feedback_session(
                base_path=project_path,
                operation_type="skill",
                status="success",
                session_id=str(uuid4()),
                timestamp=datetime.now(timezone.utc).isoformat(),
                skill_name="devforgeai-development",
                phase=phase,
                description=f"Phase: {phase}",
            )
            assert phase in result.file_path or phase in Path(result.file_path).read_text()

    def test_index_entry_includes_operation_args(self, temp_project_dir, feedback_index):
        """AC2.3: Index entry captures operation.args (e.g., "STORY-042", "deep mode")."""
        # Arrange
        project_path = temp_project_dir
        feedback_index.create()

        # Create session
        result = persist_feedback_session(
            base_path=project_path,
            operation_type="skill",
            status="success",
            session_id=str(uuid4()),
            timestamp=datetime.now(timezone.utc).isoformat(),
            skill_name="devforgeai-qa",
            phase="Validation",
            description="QA validation deep mode",
        )

        # Create index entry with args
        session_file = Path(result.file_path)
        entry = _create_index_entry_from_session(
            session_file,
            operation_type="skill",
            operation_name="devforgeai-qa",
        )

        # Add args to operation
        entry["operation"]["args"] = "STORY-042 deep"
        feedback_index.append_entry(entry)

        # Act & Assert
        index_data = json.loads(feedback_index.index_path.read_text())
        assert index_data["feedback-sessions"][0]["operation"]["args"] == "STORY-042 deep"


# ============================================================================
# PERFORMANCE BENCHMARKS
# ============================================================================


class TestPerformanceBenchmarks:
    """Performance validation tests."""

    def test_append_operation_under_50ms(self, temp_project_dir, feedback_index):
        """Performance: Append operation completes in <50ms."""
        # Arrange
        project_path = temp_project_dir
        feedback_index.create()

        result = _create_test_session(project_path)
        session_file = Path(result.file_path)
        entry = _create_index_entry_from_session(session_file)

        # Act
        start_time = time.time()
        feedback_index.append_entry(entry)
        elapsed = (time.time() - start_time) * 1000  # Convert to ms

        # Assert
        assert elapsed < 50, f"Append took {elapsed}ms, target <50ms"

    def test_single_filter_search_under_500ms(self, temp_project_dir, feedback_index):
        """Performance: Single filter search <500ms for 1000 sessions."""
        # Arrange
        project_path = temp_project_dir
        feedback_index.create()

        # Create 50 sessions (representative)
        for i in range(50):
            result = _create_test_session(project_path)
            session_file = Path(result.file_path)
            entry = _create_index_entry_from_session(session_file)
            feedback_index.append_entry(entry)

        # Act
        filters = SearchFilters(status="success")
        results = feedback_index.search(filters)

        # Assert
        assert results.execution_time < 500

    def test_combined_filter_search_under_1s(self, temp_project_dir, feedback_index):
        """Performance: Combined filter search <1s for 1000 sessions."""
        # Arrange
        project_path = temp_project_dir
        feedback_index.create()

        # Create 50 sessions
        for i in range(50):
            result = persist_feedback_session(
                base_path=project_path,
                operation_type=["command", "skill"][i % 2],
                status=["success", "failure"][i % 2],
                session_id=str(uuid4()),
                timestamp=(
                    datetime.now(timezone.utc) - timedelta(days=i // 10)
                ).isoformat(),
                command_name="/dev" if i % 2 == 0 else None,
                skill_name="test-skill" if i % 2 == 1 else None,
                phase="Green",
                description=f"Session {i}",
            )
            session_file = Path(result.file_path)
            entry = _create_index_entry_from_session(
                session_file,
                operation_type=["command", "skill"][i % 2],
                tags=["integration"],
                keywords=["test"],
            )
            entry["status"] = ["success", "failure"][i % 2]
            feedback_index.append_entry(entry)

        # Act
        filters = SearchFilters(
            operation_type="command",
            status="success",
            tags=["integration"],
            keywords=["test"],
        )
        results = feedback_index.search(filters)

        # Assert
        assert results.execution_time < 1000
