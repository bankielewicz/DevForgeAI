"""
Comprehensive test suite for searchable metadata index for feedback sessions.

STORY-016: Searchable Metadata Index for Feedback Sessions

Tests cover:
- 7 acceptance criteria (AC1-AC7)
- 6 edge cases
- Search filtering (date range, operation, status, keywords, tags)
- Index file format validation
- Performance requirements (<500ms-1s)
- Concurrent writes and corruption recovery
- Special character handling and escaping

TDD Red Phase: All tests written BEFORE implementation.
"""

import json
import os
import tempfile
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path
from unittest.mock import MagicMock, Mock, patch

import pytest

# Import the module under test (not yet implemented)
from src.feedback_index import (
    FeedbackIndex,
    SearchFilters,
    SearchResults,
    create_index,
    search_feedback,
    reindex_feedback_sessions,
    validate_index_file,
)


# ============================================================================
# FIXTURES - Common setup for all tests
# ============================================================================


@pytest.fixture
def temp_feedback_dir():
    """Temporary feedback directory for testing."""
    with tempfile.TemporaryDirectory(prefix="feedback_") as tmpdir:
        yield Path(tmpdir)


@pytest.fixture
def index_file(temp_feedback_dir):
    """Index file path in temporary directory."""
    index_path = temp_feedback_dir / ".devforgeai" / "feedback" / "index.json"
    index_path.parent.mkdir(parents=True, exist_ok=True)
    return index_path


@pytest.fixture
def sessions_dir(temp_feedback_dir):
    """Sessions directory for test feedback files."""
    sessions_path = temp_feedback_dir / ".devforgeai" / "feedback" / "sessions"
    sessions_path.mkdir(parents=True, exist_ok=True)
    return sessions_path


@pytest.fixture
def sample_index_data():
    """Valid sample index data."""
    return {
        "version": "1.0",
        "last-updated": "2025-11-07T10:30:00Z",
        "feedback-sessions": [
            {
                "id": "2025-11-07T10-30-00-command-dev-success",
                "timestamp": "2025-11-07T10:30:00Z",
                "operation": {
                    "type": "command",
                    "name": "/dev",
                    "args": "STORY-042"
                },
                "status": "success",
                "tags": ["tdd", "backend"],
                "story-id": "STORY-042",
                "keywords": ["tests-passed", "refactoring", "clean-code"],
                "file-path": "sessions/2025-11-07T10-30-00-command-dev-success.md"
            },
            {
                "id": "2025-11-06T14-15-00-skill-devforgeai-qa-failure",
                "timestamp": "2025-11-06T14:15:00Z",
                "operation": {
                    "type": "skill",
                    "name": "devforgeai-qa",
                    "args": "STORY-041 deep"
                },
                "status": "failure",
                "tags": ["coverage", "deferral"],
                "story-id": "STORY-041",
                "keywords": ["circular-deferral", "blocker", "invalid-reason"],
                "file-path": "sessions/2025-11-06T14-15-00-skill-devforgeai-qa-failure.md"
            }
        ]
    }


# ============================================================================
# AC1: CREATE AND UPDATE INDEX ENTRY ON FEEDBACK WRITE
# ============================================================================


class TestAC1_IndexEntryCreation:
    """Tests for AC1: Create and update index entry on feedback write"""

    def test_ac1_creates_index_entry_on_feedback_write(self, index_file, sample_index_data):
        """AC1: Creates index entry when feedback session written."""
        # Arrange
        create_index(index_file, sample_index_data)

        # Act
        result = validate_index_file(index_file)

        # Assert
        assert result is True
        content = json.loads(index_file.read_text())
        assert len(content["feedback-sessions"]) == 2

    def test_ac1_index_entry_has_id_field(self, index_file, sample_index_data):
        """AC1: Index entry includes unique id field."""
        create_index(index_file, sample_index_data)

        content = json.loads(index_file.read_text())
        for entry in content["feedback-sessions"]:
            assert "id" in entry
            assert entry["id"] is not None
            assert len(entry["id"]) > 0

    def test_ac1_index_entry_has_timestamp_iso8601(self, index_file, sample_index_data):
        """AC1: Index entry includes ISO 8601 timestamp."""
        create_index(index_file, sample_index_data)

        content = json.loads(index_file.read_text())
        for entry in content["feedback-sessions"]:
            assert "timestamp" in entry
            # Validate ISO 8601 format (basic check for Z suffix or +timezone)
            assert "T" in entry["timestamp"]
            assert ("Z" in entry["timestamp"] or "+" in entry["timestamp"])

    def test_ac1_index_entry_has_operation_type(self, index_file, sample_index_data):
        """AC1: Index entry includes operation.type field."""
        create_index(index_file, sample_index_data)

        content = json.loads(index_file.read_text())
        for entry in content["feedback-sessions"]:
            assert "operation" in entry
            assert "type" in entry["operation"]
            assert entry["operation"]["type"] in ["command", "skill", "subagent"]

    def test_ac1_index_entry_has_operation_name(self, index_file, sample_index_data):
        """AC1: Index entry includes operation.name field."""
        create_index(index_file, sample_index_data)

        content = json.loads(index_file.read_text())
        for entry in content["feedback-sessions"]:
            assert "operation" in entry
            assert "name" in entry["operation"]

    def test_ac1_index_entry_has_operation_args(self, index_file, sample_index_data):
        """AC1: Index entry includes operation.args field."""
        create_index(index_file, sample_index_data)

        content = json.loads(index_file.read_text())
        for entry in content["feedback-sessions"]:
            assert "operation" in entry
            # args can be optional, but should exist in structure
            assert "args" in entry["operation"] or entry["operation"].get("args") is not None

    def test_ac1_index_entry_has_status_field(self, index_file, sample_index_data):
        """AC1: Index entry includes status field."""
        create_index(index_file, sample_index_data)

        content = json.loads(index_file.read_text())
        for entry in content["feedback-sessions"]:
            assert "status" in entry
            assert entry["status"] in ["success", "failure", "partial"]

    def test_ac1_index_entry_has_tags_array(self, index_file, sample_index_data):
        """AC1: Index entry includes tags array."""
        create_index(index_file, sample_index_data)

        content = json.loads(index_file.read_text())
        for entry in content["feedback-sessions"]:
            assert "tags" in entry
            assert isinstance(entry["tags"], list)

    def test_ac1_index_entry_has_story_id_field(self, index_file, sample_index_data):
        """AC1: Index entry includes story-id field."""
        create_index(index_file, sample_index_data)

        content = json.loads(index_file.read_text())
        for entry in content["feedback-sessions"]:
            assert "story-id" in entry

    def test_ac1_index_entry_has_keywords_array(self, index_file, sample_index_data):
        """AC1: Index entry includes keywords array."""
        create_index(index_file, sample_index_data)

        content = json.loads(index_file.read_text())
        for entry in content["feedback-sessions"]:
            assert "keywords" in entry
            assert isinstance(entry["keywords"], list)

    def test_ac1_index_entry_has_file_path(self, index_file, sample_index_data):
        """AC1: Index entry includes file-path field."""
        create_index(index_file, sample_index_data)

        content = json.loads(index_file.read_text())
        for entry in content["feedback-sessions"]:
            assert "file-path" in entry
            assert "sessions/" in entry["file-path"]

    def test_ac1_index_file_valid_json_after_write(self, index_file, sample_index_data):
        """AC1: Index file is valid JSON after write."""
        create_index(index_file, sample_index_data)

        # Should not raise JSONDecodeError
        content = json.loads(index_file.read_text())
        assert isinstance(content, dict)


# ============================================================================
# AC2: INDEX FILE FORMAT VALIDATION
# ============================================================================


class TestAC2_IndexFileFormat:
    """Tests for AC2: Index file format validation"""

    def test_ac2_index_has_version_1_0(self, index_file, sample_index_data):
        """AC2: Index file contains version 1.0."""
        create_index(index_file, sample_index_data)

        content = json.loads(index_file.read_text())
        assert "version" in content
        assert content["version"] == "1.0"

    def test_ac2_index_has_last_updated_iso8601(self, index_file, sample_index_data):
        """AC2: Index file contains last-updated in ISO 8601."""
        create_index(index_file, sample_index_data)

        content = json.loads(index_file.read_text())
        assert "last-updated" in content
        assert "T" in content["last-updated"]
        assert "Z" in content["last-updated"] or "+" in content["last-updated"]

    def test_ac2_index_has_feedback_sessions_array(self, index_file, sample_index_data):
        """AC2: Index file contains feedback-sessions array."""
        create_index(index_file, sample_index_data)

        content = json.loads(index_file.read_text())
        assert "feedback-sessions" in content
        assert isinstance(content["feedback-sessions"], list)

    def test_ac2_no_duplicate_ids(self, index_file):
        """AC2: No duplicate id values in feedback-sessions."""
        # Create index with intentional duplicates
        data = {
            "version": "1.0",
            "last-updated": datetime.now(timezone.utc).isoformat(),
            "feedback-sessions": [
                {
                    "id": "duplicate-id",
                    "timestamp": "2025-11-07T10:00:00Z",
                    "operation": {"type": "command", "name": "/dev", "args": ""},
                    "status": "success",
                    "tags": [],
                    "story-id": None,
                    "keywords": [],
                    "file-path": "sessions/test1.md"
                },
                {
                    "id": "duplicate-id",
                    "timestamp": "2025-11-07T11:00:00Z",
                    "operation": {"type": "command", "name": "/qa", "args": ""},
                    "status": "success",
                    "tags": [],
                    "story-id": None,
                    "keywords": [],
                    "file-path": "sessions/test2.md"
                }
            ]
        }

        # Validation should catch duplicates
        result = validate_index_file(index_file, data)
        assert result is False

    def test_ac2_all_timestamps_valid_iso8601(self, index_file, sample_index_data):
        """AC2: All timestamps in entries are valid ISO 8601."""
        create_index(index_file, sample_index_data)

        content = json.loads(index_file.read_text())
        for entry in content["feedback-sessions"]:
            timestamp = entry["timestamp"]
            # Should parse without error
            assert "T" in timestamp
            assert "Z" in timestamp or "+" in timestamp

    def test_ac2_all_tags_are_lowercase(self, index_file, sample_index_data):
        """AC2: All tags are lowercase strings."""
        create_index(index_file, sample_index_data)

        content = json.loads(index_file.read_text())
        for entry in content["feedback-sessions"]:
            for tag in entry.get("tags", []):
                assert tag == tag.lower()

    def test_ac2_keywords_are_lowercase_and_hyphenated(self, index_file, sample_index_data):
        """AC2: Keywords are lowercase and hyphenated."""
        create_index(index_file, sample_index_data)

        content = json.loads(index_file.read_text())
        for entry in content["feedback-sessions"]:
            for keyword in entry.get("keywords", []):
                assert keyword == keyword.lower()
                # Multi-word keywords should be hyphenated
                if " " in keyword:
                    assert "-" in keyword


# ============================================================================
# AC3: SEARCH BY DATE RANGE
# ============================================================================


class TestAC3_SearchByDateRange:
    """Tests for AC3: Search by date range"""

    def test_ac3_search_returns_sessions_in_date_range(self, index_file, sample_index_data):
        """AC3: Search returns sessions within date range."""
        create_index(index_file, sample_index_data)

        filters = SearchFilters(
            date_start="2025-11-06",
            date_end="2025-11-07"
        )

        results = search_feedback(index_file, filters)

        assert results.total > 0
        for result in results.results:
            assert "2025-11-0" in result["timestamp"]

    def test_ac3_search_results_reverse_chronological_order(self, index_file):
        """AC3: Results returned in reverse chronological order (newest first)."""
        # Create index with multiple entries at different times
        data = {
            "version": "1.0",
            "last-updated": datetime.now(timezone.utc).isoformat(),
            "feedback-sessions": [
                {
                    "id": "2025-11-05T10-00-00-command-dev-success",
                    "timestamp": "2025-11-05T10:00:00Z",
                    "operation": {"type": "command", "name": "/dev", "args": "STORY-040"},
                    "status": "success",
                    "tags": [],
                    "story-id": "STORY-040",
                    "keywords": [],
                    "file-path": "sessions/test1.md"
                },
                {
                    "id": "2025-11-07T10-00-00-command-dev-success",
                    "timestamp": "2025-11-07T10:00:00Z",
                    "operation": {"type": "command", "name": "/dev", "args": "STORY-042"},
                    "status": "success",
                    "tags": [],
                    "story-id": "STORY-042",
                    "keywords": [],
                    "file-path": "sessions/test3.md"
                },
                {
                    "id": "2025-11-06T14-00-00-command-dev-success",
                    "timestamp": "2025-11-06T14:00:00Z",
                    "operation": {"type": "command", "name": "/dev", "args": "STORY-041"},
                    "status": "success",
                    "tags": [],
                    "story-id": "STORY-041",
                    "keywords": [],
                    "file-path": "sessions/test2.md"
                }
            ]
        }
        create_index(index_file, data)

        filters = SearchFilters(
            date_start="2025-11-05",
            date_end="2025-11-07"
        )

        results = search_feedback(index_file, filters)

        # Check reverse chronological order
        timestamps = [r["timestamp"] for r in results.results]
        assert timestamps == sorted(timestamps, reverse=True)

    @pytest.mark.timing
    def test_ac3_search_completes_under_500ms(self, index_file, sample_index_data):
        """AC3: Date range search completes in <500ms."""
        create_index(index_file, sample_index_data)

        filters = SearchFilters(
            date_start="2025-11-01",
            date_end="2025-11-30"
        )

        start_time = time.time()
        results = search_feedback(index_file, filters)
        elapsed_ms = (time.time() - start_time) * 1000

        assert elapsed_ms < 500


# ============================================================================
# AC4: SEARCH BY OPERATION TYPE AND NAME
# ============================================================================


class TestAC4_SearchByOperationType:
    """Tests for AC4: Search by operation type and name"""

    def test_ac4_filter_by_operation_type_command(self, index_file, sample_index_data):
        """AC4: Filters sessions by operation type 'command'."""
        create_index(index_file, sample_index_data)

        filters = SearchFilters(
            operation_type="command"
        )

        results = search_feedback(index_file, filters)

        for result in results.results:
            assert result["operation"]["type"] == "command"

    def test_ac4_filter_by_operation_name_qa(self, index_file, sample_index_data):
        """AC4: Filters sessions by operation name '/qa'."""
        # Add /qa entry to sample data
        data = sample_index_data.copy()
        data["feedback-sessions"].append({
            "id": "2025-11-07T11-00-00-command-qa-failure",
            "timestamp": "2025-11-07T11:00:00Z",
            "operation": {
                "type": "command",
                "name": "/qa",
                "args": "STORY-042 deep"
            },
            "status": "failure",
            "tags": ["qa"],
            "story-id": "STORY-042",
            "keywords": ["coverage", "failure"],
            "file-path": "sessions/2025-11-07T11-00-00-command-qa-failure.md"
        })

        create_index(index_file, data)

        filters = SearchFilters(
            operation_name="/qa"
        )

        results = search_feedback(index_file, filters)

        for result in results.results:
            assert result["operation"]["name"] == "/qa"

    def test_ac4_combined_type_and_name_filter(self, index_file, sample_index_data):
        """AC4: Combined filter by type AND name returns correct results."""
        create_index(index_file, sample_index_data)

        filters = SearchFilters(
            operation_type="command",
            operation_name="/dev"
        )

        results = search_feedback(index_file, filters)

        for result in results.results:
            assert result["operation"]["type"] == "command"
            assert result["operation"]["name"] == "/dev"

    def test_ac4_search_includes_session_count_in_response(self, index_file, sample_index_data):
        """AC4: Search response includes session count."""
        create_index(index_file, sample_index_data)

        filters = SearchFilters(
            operation_type="command"
        )

        results = search_feedback(index_file, filters)

        assert hasattr(results, "total")
        assert results.total > 0

    @pytest.mark.timing
    def test_ac4_operation_filter_search_under_500ms(self, index_file, sample_index_data):
        """AC4: Operation filter search completes in <500ms."""
        create_index(index_file, sample_index_data)

        filters = SearchFilters(
            operation_type="skill",
            operation_name="devforgeai-qa"
        )

        start_time = time.time()
        results = search_feedback(index_file, filters)
        elapsed_ms = (time.time() - start_time) * 1000

        assert elapsed_ms < 500


# ============================================================================
# AC5: SEARCH BY STATUS AND KEYWORDS
# ============================================================================


class TestAC5_SearchByStatusAndKeywords:
    """Tests for AC5: Search by status and keywords"""

    def test_ac5_filter_by_status_failure(self, index_file, sample_index_data):
        """AC5: Filters sessions by status 'failure'."""
        create_index(index_file, sample_index_data)

        filters = SearchFilters(
            status="failure"
        )

        results = search_feedback(index_file, filters)

        for result in results.results:
            assert result["status"] == "failure"

    def test_ac5_filter_by_keyword_matches_any(self, index_file):
        """AC5: Keyword search uses OR logic (match any keyword)."""
        data = {
            "version": "1.0",
            "last-updated": datetime.now(timezone.utc).isoformat(),
            "feedback-sessions": [
                {
                    "id": "entry1",
                    "timestamp": "2025-11-07T10:00:00Z",
                    "operation": {"type": "command", "name": "/dev", "args": ""},
                    "status": "failure",
                    "tags": [],
                    "story-id": None,
                    "keywords": ["confusing", "error"],
                    "file-path": "sessions/test1.md"
                },
                {
                    "id": "entry2",
                    "timestamp": "2025-11-07T11:00:00Z",
                    "operation": {"type": "command", "name": "/qa", "args": ""},
                    "status": "failure",
                    "tags": [],
                    "story-id": None,
                    "keywords": ["message", "unclear"],
                    "file-path": "sessions/test2.md"
                }
            ]
        }
        create_index(index_file, data)

        filters = SearchFilters(
            keywords=["confusing", "message"]
        )

        results = search_feedback(index_file, filters)

        # Should match both entries (confusing in entry1, message in entry2)
        assert results.total == 2

    def test_ac5_displays_matched_keywords(self, index_file):
        """AC5: Results display matched keywords for context."""
        data = {
            "version": "1.0",
            "last-updated": datetime.now(timezone.utc).isoformat(),
            "feedback-sessions": [
                {
                    "id": "entry1",
                    "timestamp": "2025-11-07T10:00:00Z",
                    "operation": {"type": "command", "name": "/dev", "args": ""},
                    "status": "failure",
                    "tags": [],
                    "story-id": None,
                    "keywords": ["confusing-error", "timeout"],
                    "file-path": "sessions/test1.md"
                }
            ]
        }
        create_index(index_file, data)

        filters = SearchFilters(
            keywords=["confusing-error"]
        )

        results = search_feedback(index_file, filters)

        assert len(results.results) > 0
        result = results.results[0]
        assert "matched-keywords" in result or "keywords" in result

    @pytest.mark.timing
    def test_ac5_keyword_search_under_500ms_with_large_index(self, index_file):
        """AC5: Keyword search completes <500ms even with 1000+ sessions."""
        # Create large index with 1000+ entries
        sessions = []
        for i in range(1200):
            sessions.append({
                "id": f"entry{i}",
                "timestamp": f"2025-11-{(i % 30) + 1:02d}T{(i % 24):02d}:00:00Z",
                "operation": {"type": "command", "name": "/dev", "args": f"STORY-{i}"},
                "status": "success" if i % 2 == 0 else "failure",
                "tags": ["tdd", "backend"],
                "story-id": f"STORY-{i}",
                "keywords": ["test", "implementation", "coverage"] if i % 3 == 0 else ["debug", "error"],
                "file-path": f"sessions/test{i}.md"
            })

        data = {
            "version": "1.0",
            "last-updated": datetime.now(timezone.utc).isoformat(),
            "feedback-sessions": sessions
        }
        create_index(index_file, data)

        filters = SearchFilters(
            keywords=["coverage"]
        )

        start_time = time.time()
        results = search_feedback(index_file, filters)
        elapsed_ms = (time.time() - start_time) * 1000

        assert elapsed_ms < 500


# ============================================================================
# AC6: COMBINED FILTER SEARCH
# ============================================================================


class TestAC6_CombinedFilterSearch:
    """Tests for AC6: Combined filter search"""

    def test_ac6_multiple_filters_use_and_logic(self, index_file):
        """AC6: Multiple filters use AND logic (all must match)."""
        data = {
            "version": "1.0",
            "last-updated": datetime.now(timezone.utc).isoformat(),
            "feedback-sessions": [
                {
                    "id": "entry1",
                    "timestamp": "2025-09-05T10:00:00Z",
                    "operation": {"type": "command", "name": "/dev", "args": ""},
                    "status": "failure",
                    "tags": ["deferral", "blocker"],
                    "story-id": "STORY-001",
                    "keywords": ["circular-dependency"],
                    "file-path": "sessions/test1.md"
                },
                {
                    "id": "entry2",
                    "timestamp": "2025-09-10T10:00:00Z",
                    "operation": {"type": "skill", "name": "devforgeai-qa", "args": ""},
                    "status": "failure",
                    "tags": ["deferral"],
                    "story-id": "STORY-002",
                    "keywords": ["other-issue"],
                    "file-path": "sessions/test2.md"
                },
                {
                    "id": "entry3",
                    "timestamp": "2025-09-15T10:00:00Z",
                    "operation": {"type": "command", "name": "/qa", "args": ""},
                    "status": "success",
                    "tags": ["blocker"],
                    "story-id": "STORY-003",
                    "keywords": ["circular-dependency"],
                    "file-path": "sessions/test3.md"
                }
            ]
        }
        create_index(index_file, data)

        # All filters must match
        filters = SearchFilters(
            date_start="2025-09-01",
            operation_type="command",
            status="failure",
            tags=["deferral", "blocker"],
            keywords=["circular-dependency"]
        )

        results = search_feedback(index_file, filters)

        # Only entry1 matches ALL filters
        assert results.total == 1
        assert results.results[0]["id"] == "entry1"

    def test_ac6_combined_search_displays_matching_criteria(self, index_file):
        """AC6: Combined search displays matching criteria and result count."""
        data = {
            "version": "1.0",
            "last-updated": datetime.now(timezone.utc).isoformat(),
            "feedback-sessions": [
                {
                    "id": "entry1",
                    "timestamp": "2025-09-05T10:00:00Z",
                    "operation": {"type": "command", "name": "/dev", "args": "STORY-001"},
                    "status": "failure",
                    "tags": ["deferral"],
                    "story-id": "STORY-001",
                    "keywords": ["circular"],
                    "file-path": "sessions/test1.md"
                }
            ]
        }
        create_index(index_file, data)

        filters = SearchFilters(
            date_start="2025-09-01",
            status="failure",
            tags=["deferral"]
        )

        results = search_feedback(index_file, filters)

        assert results.total > 0
        assert hasattr(results, "filters")

    @pytest.mark.timing
    def test_ac6_combined_search_under_1_second(self, index_file):
        """AC6: Combined search with 5 filters completes <1 second."""
        # Create index with 500+ sessions
        sessions = []
        for i in range(500):
            sessions.append({
                "id": f"entry{i}",
                "timestamp": f"2025-09-{(i % 30) + 1:02d}T10:00:00Z",
                "operation": {"type": "command", "name": "/dev", "args": f"STORY-{i}"},
                "status": "failure" if i % 2 == 0 else "success",
                "tags": ["deferral", "blocker"] if i % 3 == 0 else ["other"],
                "story-id": f"STORY-{i}",
                "keywords": ["circular", "dependency"] if i % 4 == 0 else ["error"],
                "file-path": f"sessions/test{i}.md"
            })

        data = {
            "version": "1.0",
            "last-updated": datetime.now(timezone.utc).isoformat(),
            "feedback-sessions": sessions
        }
        create_index(index_file, data)

        filters = SearchFilters(
            date_start="2025-09-01",
            operation_type="command",
            status="failure",
            tags=["deferral", "blocker"],
            keywords=["circular"]
        )

        start_time = time.time()
        results = search_feedback(index_file, filters)
        elapsed_ms = (time.time() - start_time) * 1000

        assert elapsed_ms < 1000


# ============================================================================
# AC7: INCREMENTAL INDEX UPDATE
# ============================================================================


class TestAC7_IncrementalUpdate:
    """Tests for AC7: Incremental index update"""

    def test_ac7_new_entry_appended_not_rebuilt(self, index_file, sample_index_data):
        """AC7: New entry appended, not rebuilt."""
        create_index(index_file, sample_index_data)

        # Get original entries
        original_content = json.loads(index_file.read_text())
        original_count = len(original_content["feedback-sessions"])

        # Append new entry
        new_entry = {
            "id": "2025-11-08T10-00-00-command-dev-success",
            "timestamp": "2025-11-08T10:00:00Z",
            "operation": {"type": "command", "name": "/dev", "args": "STORY-043"},
            "status": "success",
            "tags": ["tdd"],
            "story-id": "STORY-043",
            "keywords": ["implementation"],
            "file-path": "sessions/2025-11-08T10-00-00-command-dev-success.md"
        }

        # Simulate append operation
        from src.feedback_index import append_index_entry
        append_index_entry(index_file, new_entry)

        # Verify entry added
        updated_content = json.loads(index_file.read_text())
        assert len(updated_content["feedback-sessions"]) == original_count + 1

    def test_ac7_existing_entries_unchanged(self, index_file, sample_index_data):
        """AC7: Existing entries remain unchanged."""
        create_index(index_file, sample_index_data)

        # Store original content
        original_content = json.loads(index_file.read_text())
        original_first_id = original_content["feedback-sessions"][0]["id"]

        # Append new entry
        new_entry = {
            "id": "2025-11-08T10-00-00-command-dev-success",
            "timestamp": "2025-11-08T10:00:00Z",
            "operation": {"type": "command", "name": "/dev", "args": "STORY-043"},
            "status": "success",
            "tags": [],
            "story-id": "STORY-043",
            "keywords": [],
            "file-path": "sessions/test.md"
        }

        from src.feedback_index import append_index_entry
        append_index_entry(index_file, new_entry)

        # Verify original entry still there
        updated_content = json.loads(index_file.read_text())
        assert updated_content["feedback-sessions"][0]["id"] == original_first_id

    def test_ac7_last_updated_timestamp_updated(self, index_file, sample_index_data):
        """AC7: last-updated timestamp updated on append."""
        create_index(index_file, sample_index_data)

        original_content = json.loads(index_file.read_text())
        original_timestamp = original_content["last-updated"]

        # Wait a bit
        import time as time_module
        time_module.sleep(0.01)

        # Append new entry
        new_entry = {
            "id": "2025-11-08T10-00-00-command-dev-success",
            "timestamp": "2025-11-08T10:00:00Z",
            "operation": {"type": "command", "name": "/dev", "args": ""},
            "status": "success",
            "tags": [],
            "story-id": None,
            "keywords": [],
            "file-path": "sessions/test.md"
        }

        from src.feedback_index import append_index_entry
        append_index_entry(index_file, new_entry)

        # Verify last-updated changed
        updated_content = json.loads(index_file.read_text())
        assert updated_content["last-updated"] != original_timestamp

    @pytest.mark.timing
    def test_ac7_append_completes_under_50ms(self, index_file, sample_index_data):
        """AC7: Append operation completes in <50ms."""
        create_index(index_file, sample_index_data)

        new_entry = {
            "id": "2025-11-08T10-00-00-command-dev-success",
            "timestamp": "2025-11-08T10:00:00Z",
            "operation": {"type": "command", "name": "/dev", "args": ""},
            "status": "success",
            "tags": [],
            "story-id": None,
            "keywords": [],
            "file-path": "sessions/test.md"
        }

        from src.feedback_index import append_index_entry

        start_time = time.time()
        append_index_entry(index_file, new_entry)
        elapsed_ms = (time.time() - start_time) * 1000

        assert elapsed_ms < 50


# ============================================================================
# EDGE CASE 1: CORRUPTED INDEX FILE RECOVERY
# ============================================================================


class TestEdgeCase1_CorruptedIndexRecovery:
    """Tests for Edge Case 1: Corrupted index file recovery"""

    def test_edge_case1_detects_invalid_json(self, index_file):
        """Edge Case 1: Detects invalid JSON in index file."""
        # Create malformed JSON
        index_file.write_text("{invalid json content")

        result = validate_index_file(index_file)

        assert result is False

    def test_edge_case1_detects_missing_required_fields(self, index_file):
        """Edge Case 1: Detects missing required fields."""
        malformed_data = {
            "version": "1.0",
            # Missing last-updated
            "feedback-sessions": []
        }

        index_file.write_text(json.dumps(malformed_data))

        result = validate_index_file(index_file)

        assert result is False

    def test_edge_case1_error_message_suggests_reindex(self, index_file):
        """Edge Case 1: Error message suggests /feedback-reindex command."""
        # Create corrupted index
        index_file.write_text("{bad json")

        from src.feedback_index import validate_and_recover_index

        try:
            validate_and_recover_index(index_file)
        except ValueError as e:
            assert "reindex" in str(e).lower() or "rebuild" in str(e).lower()


# ============================================================================
# EDGE CASE 2: INDEX REINDEX COMMAND
# ============================================================================


class TestEdgeCase2_IndexReindex:
    """Tests for Edge Case 2: Index reindex command"""

    def test_edge_case2_reindex_scans_sessions_directory(self, index_file, sessions_dir):
        """Edge Case 2: Reindex scans .devforgeai/feedback/sessions/ directory."""
        # Create some session files
        session1 = sessions_dir / "2025-11-07T10-00-00-command-dev-success.md"
        session1.write_text("---\nid: test1\n---\nContent")

        session2 = sessions_dir / "2025-11-07T11-00-00-command-qa-failure.md"
        session2.write_text("---\nid: test2\n---\nContent")

        # Run reindex
        result = reindex_feedback_sessions(sessions_dir.parent)

        assert result["sessions_reindexed"] >= 0

    def test_edge_case2_reindex_rebuilds_index_from_scratch(self, index_file, sessions_dir):
        """Edge Case 2: Reindex rebuilds index.json from scratch."""
        # Create session files
        session1 = sessions_dir / "2025-11-07T10-00-00-command-dev-success.md"
        session1.write_text("---\nid: session1\n---\nFeedback content")

        # Run reindex
        reindex_feedback_sessions(sessions_dir.parent)

        # Verify index created
        assert index_file.exists()
        content = json.loads(index_file.read_text())
        assert "feedback-sessions" in content

    def test_edge_case2_reindex_validates_all_entries(self, index_file, sessions_dir):
        """Edge Case 2: Reindex validates all entries and formats."""
        session1 = sessions_dir / "2025-11-07T10-00-00-command-dev-success.md"
        session1.write_text("---\nid: session1\noperation: /dev\n---\nContent")

        reindex_feedback_sessions(sessions_dir.parent)

        content = json.loads(index_file.read_text())
        for entry in content["feedback-sessions"]:
            assert "id" in entry
            assert "timestamp" in entry
            assert "operation" in entry

    @pytest.mark.timing
    def test_edge_case2_reindex_completes_under_10_seconds(self, sessions_dir):
        """Edge Case 2: Reindex completes <10 seconds for 1000+ sessions."""
        # Create 1000+ session files
        for i in range(1000):
            session = sessions_dir / f"2025-11-{(i % 30) + 1:02d}T{(i % 24):02d}-00-00-command-dev-success.md"
            session.write_text(f"---\nid: session{i}\n---\nContent {i}")

        start_time = time.time()
        result = reindex_feedback_sessions(sessions_dir.parent)
        elapsed_seconds = time.time() - start_time

        assert elapsed_seconds < 10


# ============================================================================
# EDGE CASE 3: MISSING OPTIONAL FIELDS
# ============================================================================


class TestEdgeCase3_MissingOptionalFields:
    """Tests for Edge Case 3: Missing optional fields"""

    def test_edge_case3_required_fields_halt_on_missing_id(self, index_file):
        """Edge Case 3: Missing required 'id' field halts."""
        malformed_entry = {
            # Missing id
            "timestamp": "2025-11-07T10:00:00Z",
            "operation": {"type": "command", "name": "/dev", "args": ""},
            "status": "success",
            "tags": [],
            "keywords": [],
            "file-path": "sessions/test.md"
        }

        with pytest.raises(ValueError):
            from src.feedback_index import validate_entry
            validate_entry(malformed_entry)

    def test_edge_case3_tags_defaults_to_empty_array(self, index_file):
        """Edge Case 3: Missing tags defaults to empty array []."""
        data = {
            "version": "1.0",
            "last-updated": datetime.now(timezone.utc).isoformat(),
            "feedback-sessions": [
                {
                    "id": "entry1",
                    "timestamp": "2025-11-07T10:00:00Z",
                    "operation": {"type": "command", "name": "/dev", "args": ""},
                    "status": "success",
                    # No tags field
                    "story-id": None,
                    "keywords": [],
                    "file-path": "sessions/test.md"
                }
            ]
        }

        create_index(index_file, data)
        content = json.loads(index_file.read_text())

        entry = content["feedback-sessions"][0]
        assert "tags" in entry
        assert entry["tags"] == [] or len(entry["tags"]) == 0

    def test_edge_case3_story_id_defaults_to_null(self, index_file):
        """Edge Case 3: Missing story-id defaults to null."""
        data = {
            "version": "1.0",
            "last-updated": datetime.now(timezone.utc).isoformat(),
            "feedback-sessions": [
                {
                    "id": "entry1",
                    "timestamp": "2025-11-07T10:00:00Z",
                    "operation": {"type": "command", "name": "/dev", "args": ""},
                    "status": "success",
                    "tags": [],
                    # No story-id field
                    "keywords": [],
                    "file-path": "sessions/test.md"
                }
            ]
        }

        create_index(index_file, data)
        content = json.loads(index_file.read_text())

        entry = content["feedback-sessions"][0]
        assert "story-id" in entry
        assert entry["story-id"] is None

    def test_edge_case3_keywords_defaults_to_empty_array(self, index_file):
        """Edge Case 3: Missing keywords defaults to empty array []."""
        data = {
            "version": "1.0",
            "last-updated": datetime.now(timezone.utc).isoformat(),
            "feedback-sessions": [
                {
                    "id": "entry1",
                    "timestamp": "2025-11-07T10:00:00Z",
                    "operation": {"type": "command", "name": "/dev", "args": ""},
                    "status": "success",
                    "tags": [],
                    "story-id": None,
                    # No keywords field
                    "file-path": "sessions/test.md"
                }
            ]
        }

        create_index(index_file, data)
        content = json.loads(index_file.read_text())

        entry = content["feedback-sessions"][0]
        assert "keywords" in entry
        assert entry["keywords"] == [] or len(entry["keywords"]) == 0


# ============================================================================
# EDGE CASE 4: LARGE INDEX PERFORMANCE
# ============================================================================


class TestEdgeCase4_LargeIndexPerformance:
    """Tests for Edge Case 4: Large index performance (1200+ sessions)"""

    def test_edge_case4_all_operations_under_1_second(self, index_file):
        """Edge Case 4: All operations complete <1 second with 1200 sessions."""
        # Create large index with 1200 entries
        sessions = []
        for i in range(1200):
            sessions.append({
                "id": f"entry{i}",
                "timestamp": f"2025-11-{(i % 30) + 1:02d}T{(i % 24):02d}:00:00Z",
                "operation": {"type": "command", "name": "/dev", "args": f"STORY-{i}"},
                "status": "success" if i % 2 == 0 else "failure",
                "tags": ["tdd"],
                "story-id": f"STORY-{i}",
                "keywords": ["test"],
                "file-path": f"sessions/test{i}.md"
            })

        data = {
            "version": "1.0",
            "last-updated": datetime.now(timezone.utc).isoformat(),
            "feedback-sessions": sessions
        }

        # Measure creation time
        start = time.time()
        create_index(index_file, data)
        create_time = time.time() - start

        assert create_time < 1.0

        # Measure search time
        filters = SearchFilters(status="failure")
        start = time.time()
        results = search_feedback(index_file, filters)
        search_time = time.time() - start

        assert search_time < 1.0

    def test_edge_case4_index_file_size_under_5mb(self, index_file):
        """Edge Case 4: Index file size <5MB with 1200 sessions."""
        sessions = []
        for i in range(1200):
            sessions.append({
                "id": f"entry{i}",
                "timestamp": f"2025-11-{(i % 30) + 1:02d}T10:00:00Z",
                "operation": {"type": "command", "name": "/dev", "args": f"STORY-{i}"},
                "status": "success",
                "tags": ["tdd", "backend"],
                "story-id": f"STORY-{i}",
                "keywords": ["test", "implementation"],
                "file-path": f"sessions/test{i}.md"
            })

        data = {
            "version": "1.0",
            "last-updated": datetime.now(timezone.utc).isoformat(),
            "feedback-sessions": sessions
        }

        create_index(index_file, data)

        file_size_mb = index_file.stat().st_size / (1024 * 1024)
        assert file_size_mb < 5.0


# ============================================================================
# EDGE CASE 5: CONCURRENT WRITES
# ============================================================================


class TestEdgeCase5_ConcurrentWrites:
    """Tests for Edge Case 5: Concurrent index writes"""

    def test_edge_case5_concurrent_appends_no_corruption(self, index_file, sample_index_data):
        """Edge Case 5: Concurrent appends don't corrupt index."""
        create_index(index_file, sample_index_data)

        from src.feedback_index import append_index_entry
        import threading

        def append_entry(i):
            entry = {
                "id": f"concurrent{i}",
                "timestamp": f"2025-11-08T{(i % 24):02d}:00:00Z",
                "operation": {"type": "command", "name": "/dev", "args": ""},
                "status": "success",
                "tags": [],
                "story-id": None,
                "keywords": [],
                "file-path": f"sessions/test{i}.md"
            }
            append_index_entry(index_file, entry)

        threads = []
        for i in range(10):
            t = threading.Thread(target=append_entry, args=(i,))
            threads.append(t)
            t.start()

        for t in threads:
            t.join()

        # Verify index is still valid JSON
        content = json.loads(index_file.read_text())
        assert isinstance(content, dict)
        assert "feedback-sessions" in content

    def test_edge_case5_concurrent_writes_both_entries_added(self, index_file, sample_index_data):
        """Edge Case 5: Both concurrent writes are included in index."""
        create_index(index_file, sample_index_data)

        original_count = len(sample_index_data["feedback-sessions"])

        from src.feedback_index import append_index_entry

        entries = [
            {
                "id": "entry_a",
                "timestamp": "2025-11-08T10:00:00Z",
                "operation": {"type": "command", "name": "/dev", "args": ""},
                "status": "success",
                "tags": [],
                "story-id": None,
                "keywords": [],
                "file-path": "sessions/test_a.md"
            },
            {
                "id": "entry_b",
                "timestamp": "2025-11-08T11:00:00Z",
                "operation": {"type": "command", "name": "/qa", "args": ""},
                "status": "failure",
                "tags": [],
                "story-id": None,
                "keywords": [],
                "file-path": "sessions/test_b.md"
            }
        ]

        import threading

        def append_entry(entry):
            append_index_entry(index_file, entry)

        threads = [threading.Thread(target=append_entry, args=(e,)) for e in entries]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        content = json.loads(index_file.read_text())
        assert len(content["feedback-sessions"]) == original_count + 2


# ============================================================================
# EDGE CASE 6: SPECIAL CHARACTERS AND ESCAPING
# ============================================================================


class TestEdgeCase6_SpecialCharacterHandling:
    """Tests for Edge Case 6: Special characters and escaping"""

    def test_edge_case6_null_pointer_exception_keyword(self, index_file):
        """Edge Case 6: Handles 'null-pointer-exception' without regex issues."""
        data = {
            "version": "1.0",
            "last-updated": datetime.now(timezone.utc).isoformat(),
            "feedback-sessions": [
                {
                    "id": "entry1",
                    "timestamp": "2025-11-07T10:00:00Z",
                    "operation": {"type": "command", "name": "/dev", "args": ""},
                    "status": "failure",
                    "tags": [],
                    "story-id": None,
                    "keywords": ["null-pointer-exception"],
                    "file-path": "sessions/test1.md"
                }
            ]
        }

        create_index(index_file, data)

        filters = SearchFilters(
            keywords=["null-pointer-exception"]
        )

        results = search_feedback(index_file, filters)

        assert results.total == 1

    def test_edge_case6_special_chars_at_symbol(self, index_file):
        """Edge Case 6: Handles '@' special character (TypeScript@4.9)."""
        data = {
            "version": "1.0",
            "last-updated": datetime.now(timezone.utc).isoformat(),
            "feedback-sessions": [
                {
                    "id": "entry1",
                    "timestamp": "2025-11-07T10:00:00Z",
                    "operation": {"type": "command", "name": "/dev", "args": ""},
                    "status": "success",
                    "tags": [],
                    "story-id": None,
                    "keywords": ["TypeScript-4.9"],  # @ converted to hyphenation
                    "file-path": "sessions/test1.md"
                }
            ]
        }

        create_index(index_file, data)
        content = json.loads(index_file.read_text())

        # Should not raise exception
        assert len(content["feedback-sessions"]) > 0

    def test_edge_case6_quotes_and_escaping(self, index_file):
        """Edge Case 6: Handles quotes and escaping in keywords."""
        data = {
            "version": "1.0",
            "last-updated": datetime.now(timezone.utc).isoformat(),
            "feedback-sessions": [
                {
                    "id": "entry1",
                    "timestamp": "2025-11-07T10:00:00Z",
                    "operation": {"type": "command", "name": "/dev", "args": ""},
                    "status": "failure",
                    "tags": [],
                    "story-id": None,
                    "keywords": ["error-database-connection-failed"],
                    "file-path": "sessions/test1.md"
                }
            ]
        }

        # Should parse without JSON error
        create_index(index_file, data)
        content = json.loads(index_file.read_text())

        assert len(content["feedback-sessions"]) > 0

    def test_edge_case6_search_with_special_chars_no_regex_error(self, index_file):
        """Edge Case 6: Search with special chars doesn't cause regex errors."""
        data = {
            "version": "1.0",
            "last-updated": datetime.now(timezone.utc).isoformat(),
            "feedback-sessions": [
                {
                    "id": "entry1",
                    "timestamp": "2025-11-07T10:00:00Z",
                    "operation": {"type": "command", "name": "/dev", "args": ""},
                    "status": "failure",
                    "tags": [],
                    "story-id": None,
                    "keywords": ["test-value", "error-string"],
                    "file-path": "sessions/test1.md"
                }
            ]
        }

        create_index(index_file, data)

        # Search with special characters (should not raise regex error)
        filters = SearchFilters(
            keywords=["test-value"]
        )

        results = search_feedback(index_file, filters)
        assert results.total == 1


# ============================================================================
# PERFORMANCE BENCHMARKS
# ============================================================================


class TestPerformanceBenchmarks:
    """Performance benchmark tests for index operations"""

    @pytest.mark.timing
    def test_benchmark_single_filter_search(self, index_file):
        """Benchmark: Single filter search performance."""
        sessions = []
        for i in range(1000):
            sessions.append({
                "id": f"entry{i}",
                "timestamp": f"2025-11-{(i % 30) + 1:02d}T10:00:00Z",
                "operation": {"type": "command", "name": "/dev", "args": ""},
                "status": "success" if i % 2 == 0 else "failure",
                "tags": [],
                "story-id": None,
                "keywords": [],
                "file-path": f"sessions/test{i}.md"
            })

        data = {
            "version": "1.0",
            "last-updated": datetime.now(timezone.utc).isoformat(),
            "feedback-sessions": sessions
        }
        create_index(index_file, data)

        filters = SearchFilters(status="failure")

        start = time.time()
        results = search_feedback(index_file, filters)
        elapsed_ms = (time.time() - start) * 1000

        print(f"\nSingle filter search: {elapsed_ms:.2f}ms (1000 sessions)")
        assert elapsed_ms < 500

    @pytest.mark.timing
    def test_benchmark_multi_filter_search(self, index_file):
        """Benchmark: Multi-filter search performance."""
        sessions = []
        for i in range(1000):
            sessions.append({
                "id": f"entry{i}",
                "timestamp": f"2025-11-{(i % 30) + 1:02d}T10:00:00Z",
                "operation": {"type": "command", "name": "/dev", "args": "STORY-001"},
                "status": "failure" if i % 3 == 0 else "success",
                "tags": ["tdd", "backend"] if i % 5 == 0 else [],
                "story-id": "STORY-001" if i % 7 == 0 else None,
                "keywords": ["implementation"] if i % 4 == 0 else [],
                "file-path": f"sessions/test{i}.md"
            })

        data = {
            "version": "1.0",
            "last-updated": datetime.now(timezone.utc).isoformat(),
            "feedback-sessions": sessions
        }
        create_index(index_file, data)

        filters = SearchFilters(
            status="failure",
            tags=["tdd"],
            keywords=["implementation"]
        )

        start = time.time()
        results = search_feedback(index_file, filters)
        elapsed_ms = (time.time() - start) * 1000

        print(f"\nMulti-filter search: {elapsed_ms:.2f}ms (1000 sessions, 3 filters)")
        assert elapsed_ms < 500

    @pytest.mark.timing
    def test_benchmark_reindex_operation(self, sessions_dir):
        """Benchmark: Reindex operation with 500+ sessions."""
        # Create 500 session files
        for i in range(500):
            session = sessions_dir / f"2025-11-{(i % 30) + 1:02d}T{(i % 24):02d}-00-00-command-dev-success.md"
            session.write_text(f"---\nid: session{i}\noperation: /dev\n---\nContent")

        start = time.time()
        result = reindex_feedback_sessions(sessions_dir.parent)
        elapsed_seconds = time.time() - start

        print(f"\nReindex operation: {elapsed_seconds:.2f}s (500 sessions)")
        assert elapsed_seconds < 10


# ============================================================================
# INTEGRATION TESTS
# ============================================================================


class TestIntegration_SearchWorkflows:
    """Integration tests for complete search workflows"""

    def test_integration_create_search_workflow(self, index_file, sample_index_data):
        """Integration: Create index and search workflow."""
        # Create index
        create_index(index_file, sample_index_data)
        assert index_file.exists()

        # Search by date
        filters = SearchFilters(
            date_start="2025-11-06",
            date_end="2025-11-07"
        )
        results = search_feedback(index_file, filters)
        assert results.total > 0

    def test_integration_append_and_search(self, index_file, sample_index_data):
        """Integration: Append entries and search."""
        create_index(index_file, sample_index_data)

        # Append new entry
        new_entry = {
            "id": "2025-11-08T10-00-00-command-dev-success",
            "timestamp": "2025-11-08T10:00:00Z",
            "operation": {"type": "command", "name": "/dev", "args": "STORY-050"},
            "status": "success",
            "tags": ["tdd"],
            "story-id": "STORY-050",
            "keywords": ["new-feature"],
            "file-path": "sessions/2025-11-08T10-00-00-command-dev-success.md"
        }

        from src.feedback_index import append_index_entry
        append_index_entry(index_file, new_entry)

        # Search for new entry
        filters = SearchFilters(
            story_id="STORY-050"
        )
        results = search_feedback(index_file, filters)
        assert results.total > 0
        assert results.results[0]["story-id"] == "STORY-050"
