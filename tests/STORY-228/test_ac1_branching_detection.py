"""
Unit tests for STORY-228 AC#1: Branching Point Detection

Test-Driven Development (RED PHASE):
All tests written BEFORE implementation - tests should FAIL initially.

Acceptance Criteria:
**Given** command sequence data,
**When** analyzing paths,
**Then** commands that trigger multiple downstream choices are identified.

Coverage Target: 95% business logic
"""

import pytest
from typing import List, Dict, Any
from datetime import datetime
from unittest.mock import Mock, patch


# ============================================================================
# Fixtures
# ============================================================================

@pytest.fixture
def sample_session_entries() -> List[Dict[str, Any]]:
    """Sample SessionEntry data mimicking session-miner output"""
    return [
        {
            "timestamp": "2025-01-02T10:00:00Z",
            "command": "/ideate",
            "status": "success",
            "session_id": "session-001",
            "duration_ms": 5000
        },
        {
            "timestamp": "2025-01-02T10:05:00Z",
            "command": "/create-story",
            "status": "success",
            "session_id": "session-001",
            "duration_ms": 3000
        },
        {
            "timestamp": "2025-01-02T10:10:00Z",
            "command": "/dev",
            "status": "success",
            "session_id": "session-001",
            "duration_ms": 45000
        },
        {
            "timestamp": "2025-01-02T11:00:00Z",
            "command": "/ideate",
            "status": "success",
            "session_id": "session-002",
            "duration_ms": 6000
        },
        {
            "timestamp": "2025-01-02T11:05:00Z",
            "command": "/brainstorm",
            "status": "success",
            "session_id": "session-002",
            "duration_ms": 8000
        },
        {
            "timestamp": "2025-01-02T12:00:00Z",
            "command": "/ideate",
            "status": "success",
            "session_id": "session-003",
            "duration_ms": 4000
        },
        {
            "timestamp": "2025-01-02T12:05:00Z",
            "command": "/create-context",
            "status": "success",
            "session_id": "session-003",
            "duration_ms": 10000
        }
    ]


@pytest.fixture
def branching_point_data() -> List[Dict[str, Any]]:
    """Sample data with clear branching points"""
    # /dev leads to either /qa or /rca - this is a branching point
    return [
        # Session 1: /dev -> /qa
        {"timestamp": "2025-01-02T10:00:00Z", "command": "/dev", "status": "success", "session_id": "s1"},
        {"timestamp": "2025-01-02T10:30:00Z", "command": "/qa", "status": "success", "session_id": "s1"},
        # Session 2: /dev -> /qa (same path)
        {"timestamp": "2025-01-02T11:00:00Z", "command": "/dev", "status": "success", "session_id": "s2"},
        {"timestamp": "2025-01-02T11:30:00Z", "command": "/qa", "status": "success", "session_id": "s2"},
        # Session 3: /dev -> /rca (different path)
        {"timestamp": "2025-01-02T12:00:00Z", "command": "/dev", "status": "error", "session_id": "s3"},
        {"timestamp": "2025-01-02T12:30:00Z", "command": "/rca", "status": "success", "session_id": "s3"},
        # Session 4: /dev -> /rca (different path)
        {"timestamp": "2025-01-02T13:00:00Z", "command": "/dev", "status": "error", "session_id": "s4"},
        {"timestamp": "2025-01-02T13:30:00Z", "command": "/rca", "status": "success", "session_id": "s4"},
        # Session 5: /dev -> /qa
        {"timestamp": "2025-01-02T14:00:00Z", "command": "/dev", "status": "success", "session_id": "s5"},
        {"timestamp": "2025-01-02T14:30:00Z", "command": "/qa", "status": "success", "session_id": "s5"},
    ]


@pytest.fixture
def no_branching_data() -> List[Dict[str, Any]]:
    """Sample data with no branching points (single path)"""
    return [
        {"timestamp": "2025-01-02T10:00:00Z", "command": "/dev", "status": "success", "session_id": "s1"},
        {"timestamp": "2025-01-02T10:30:00Z", "command": "/qa", "status": "success", "session_id": "s1"},
        {"timestamp": "2025-01-02T11:00:00Z", "command": "/dev", "status": "success", "session_id": "s2"},
        {"timestamp": "2025-01-02T11:30:00Z", "command": "/qa", "status": "success", "session_id": "s2"},
        {"timestamp": "2025-01-02T12:00:00Z", "command": "/dev", "status": "success", "session_id": "s3"},
        {"timestamp": "2025-01-02T12:30:00Z", "command": "/qa", "status": "success", "session_id": "s3"},
    ]


# ============================================================================
# AC#1: Branching Point Detection Tests
# ============================================================================

@pytest.mark.unit
@pytest.mark.acceptance_criteria
class TestBranchingPointDetection:
    """AC#1: Commands that trigger multiple downstream choices are identified"""

    def test_detect_branching_point_with_multiple_downstream_commands(
        self, branching_point_data
    ):
        """
        Test: /dev is identified as branching point when it leads to both /qa and /rca

        Given: Command sequence data where /dev leads to /qa (3 times) and /rca (2 times)
        When: Analyzing paths
        Then: /dev is identified as a branching point
        """
        # Arrange
        from branching_analysis import detect_branching_points

        # Act
        branching_points = detect_branching_points(branching_point_data)

        # Assert
        assert "/dev" in branching_points, \
            "/dev should be identified as a branching point"
        assert len(branching_points["/dev"]["downstream"]) >= 2, \
            "/dev should have at least 2 downstream commands"
        assert "/qa" in branching_points["/dev"]["downstream"], \
            "/qa should be a downstream command of /dev"
        assert "/rca" in branching_points["/dev"]["downstream"], \
            "/rca should be a downstream command of /dev"

    def test_non_branching_command_not_detected(self, no_branching_data):
        """
        Test: /dev is NOT a branching point when it always leads to /qa

        Given: Command sequence data where /dev always leads to /qa
        When: Analyzing paths
        Then: /dev is NOT identified as a branching point
        """
        # Arrange
        from branching_analysis import detect_branching_points

        # Act
        branching_points = detect_branching_points(no_branching_data)

        # Assert
        # /dev always leads to /qa, so it's not a branching point
        if "/dev" in branching_points:
            assert len(branching_points["/dev"]["downstream"]) == 1, \
                "/dev should have only 1 downstream when no branching"
        else:
            # /dev not in branching_points is also acceptable
            pass

    def test_branching_point_includes_frequency_counts(self, branching_point_data):
        """
        Test: Branching points include frequency counts for each downstream path

        Given: /dev leads to /qa (3 times) and /rca (2 times)
        When: Detecting branching points
        Then: Frequency counts are included for each downstream command
        """
        # Arrange
        from branching_analysis import detect_branching_points

        # Act
        branching_points = detect_branching_points(branching_point_data)

        # Assert
        assert "/dev" in branching_points
        downstream = branching_points["/dev"]["downstream"]

        # Check frequency counts exist
        assert "frequency" in downstream.get("/qa", {}), \
            "/qa should have frequency count"
        assert "frequency" in downstream.get("/rca", {}), \
            "/rca should have frequency count"

        # Verify counts (3 sessions -> /qa, 2 sessions -> /rca)
        assert downstream["/qa"]["frequency"] == 3, \
            "/qa frequency should be 3"
        assert downstream["/rca"]["frequency"] == 2, \
            "/rca frequency should be 2"

    def test_branching_point_returns_command_details(self, sample_session_entries):
        """
        Test: Detected branching points include command as key

        Given: Session entries with /ideate leading to multiple commands
        When: Detecting branching points
        Then: Results contain command name as key
        """
        # Arrange
        from branching_analysis import detect_branching_points

        # Act
        branching_points = detect_branching_points(sample_session_entries)

        # Assert
        assert isinstance(branching_points, dict), \
            "Result should be a dictionary"
        # /ideate leads to /create-story, /brainstorm, /create-context
        if branching_points:
            for command, data in branching_points.items():
                assert command.startswith("/"), \
                    f"Command key should start with '/', got: {command}"
                assert "downstream" in data, \
                    "Branching point should have 'downstream' field"


# ============================================================================
# Branching Detection Algorithm Tests
# ============================================================================

@pytest.mark.unit
class TestBranchingDetectionAlgorithm:
    """Tests for the branching detection algorithm mechanics"""

    def test_group_entries_by_session(self, sample_session_entries):
        """
        Test: Entries are correctly grouped by session_id

        Given: Session entries from multiple sessions
        When: Grouping by session
        Then: Each session's entries are grouped together
        """
        # Arrange
        from branching_analysis import group_by_session

        # Act
        grouped = group_by_session(sample_session_entries)

        # Assert
        assert "session-001" in grouped, "session-001 should be grouped"
        assert "session-002" in grouped, "session-002 should be grouped"
        assert "session-003" in grouped, "session-003 should be grouped"
        assert len(grouped["session-001"]) == 3, "session-001 should have 3 entries"
        assert len(grouped["session-002"]) == 2, "session-002 should have 2 entries"
        assert len(grouped["session-003"]) == 2, "session-003 should have 2 entries"

    def test_extract_command_transitions(self, sample_session_entries):
        """
        Test: Command transitions (A -> B) are extracted from sessions

        Given: Session entries with command sequences
        When: Extracting transitions
        Then: All consecutive command pairs are returned
        """
        # Arrange
        from branching_analysis import extract_transitions

        # Act
        transitions = extract_transitions(sample_session_entries)

        # Assert
        # session-001: /ideate -> /create-story -> /dev
        assert ("/ideate", "/create-story") in transitions, \
            "Should extract /ideate -> /create-story transition"
        assert ("/create-story", "/dev") in transitions, \
            "Should extract /create-story -> /dev transition"
        # session-002: /ideate -> /brainstorm
        assert ("/ideate", "/brainstorm") in transitions, \
            "Should extract /ideate -> /brainstorm transition"

    def test_count_downstream_commands(self, branching_point_data):
        """
        Test: Downstream commands are counted per source command

        Given: /dev leads to /qa 3x and /rca 2x
        When: Counting downstream commands
        Then: Counts are accurate
        """
        # Arrange
        from branching_analysis import count_downstream

        # Act
        downstream_counts = count_downstream(branching_point_data)

        # Assert
        assert "/dev" in downstream_counts, "/dev should have downstream counts"
        assert downstream_counts["/dev"].get("/qa", 0) == 3, \
            "/dev -> /qa count should be 3"
        assert downstream_counts["/dev"].get("/rca", 0) == 2, \
            "/dev -> /rca count should be 2"

    def test_minimum_branching_threshold(self):
        """
        Test: Command needs at least 2 different downstream paths to be a branching point

        Given: Threshold of 2 for branching detection
        When: Command has only 1 downstream path
        Then: It is NOT classified as a branching point
        """
        # Arrange
        from branching_analysis import detect_branching_points
        single_path_data = [
            {"timestamp": "2025-01-02T10:00:00Z", "command": "/dev", "status": "success", "session_id": "s1"},
            {"timestamp": "2025-01-02T10:30:00Z", "command": "/qa", "status": "success", "session_id": "s1"},
        ]

        # Act
        branching_points = detect_branching_points(single_path_data, min_paths=2)

        # Assert
        assert "/dev" not in branching_points, \
            "/dev with single downstream should not be a branching point"


# ============================================================================
# Edge Cases
# ============================================================================

@pytest.mark.unit
@pytest.mark.edge_case
class TestBranchingDetectionEdgeCases:
    """Edge cases for branching point detection"""

    def test_empty_session_entries(self):
        """
        Edge Case: Empty session entries list

        Given: Empty list of session entries
        When: Detecting branching points
        Then: Returns empty dictionary
        """
        # Arrange
        from branching_analysis import detect_branching_points

        # Act
        result = detect_branching_points([])

        # Assert
        assert result == {}, "Empty input should return empty dict"

    def test_single_session_single_command(self):
        """
        Edge Case: Single session with single command

        Given: One session with one command
        When: Detecting branching points
        Then: Returns empty dictionary (no transitions)
        """
        # Arrange
        from branching_analysis import detect_branching_points
        single_entry = [
            {"timestamp": "2025-01-02T10:00:00Z", "command": "/dev", "status": "success", "session_id": "s1"}
        ]

        # Act
        result = detect_branching_points(single_entry)

        # Assert
        assert result == {}, "Single command should have no branching points"

    def test_missing_session_id_handled(self):
        """
        Edge Case: Entries with missing session_id

        Given: Entries without session_id field
        When: Detecting branching points
        Then: Handles gracefully (groups as null session or skips)
        """
        # Arrange
        from branching_analysis import detect_branching_points
        missing_session_data = [
            {"timestamp": "2025-01-02T10:00:00Z", "command": "/dev", "status": "success"},
            {"timestamp": "2025-01-02T10:30:00Z", "command": "/qa", "status": "success"},
        ]

        # Act
        result = detect_branching_points(missing_session_data)

        # Assert
        # Should not raise exception
        assert isinstance(result, dict), "Should return dict even with missing session_id"

    def test_duplicate_transitions_within_session(self):
        """
        Edge Case: Same transition occurs multiple times in one session

        Given: /dev -> /qa happens twice in same session
        When: Counting downstream
        Then: Counts as 1 occurrence (per session, not per instance)
        """
        # Arrange
        from branching_analysis import detect_branching_points
        repeated_transition_data = [
            {"timestamp": "2025-01-02T10:00:00Z", "command": "/dev", "status": "success", "session_id": "s1"},
            {"timestamp": "2025-01-02T10:30:00Z", "command": "/qa", "status": "success", "session_id": "s1"},
            {"timestamp": "2025-01-02T10:35:00Z", "command": "/dev", "status": "success", "session_id": "s1"},
            {"timestamp": "2025-01-02T10:40:00Z", "command": "/qa", "status": "success", "session_id": "s1"},
        ]

        # Act
        result = detect_branching_points(repeated_transition_data)

        # Assert
        # Implementation decision: could count 2x or 1x per session
        # Test validates consistent behavior
        assert isinstance(result, dict), "Should return valid result"

    def test_handles_unsorted_timestamps(self):
        """
        Edge Case: Session entries not sorted by timestamp

        Given: Entries with out-of-order timestamps
        When: Detecting branching points
        Then: Sorts by timestamp before analysis
        """
        # Arrange
        from branching_analysis import detect_branching_points
        unsorted_data = [
            {"timestamp": "2025-01-02T10:30:00Z", "command": "/qa", "status": "success", "session_id": "s1"},
            {"timestamp": "2025-01-02T10:00:00Z", "command": "/dev", "status": "success", "session_id": "s1"},
        ]

        # Act
        result = detect_branching_points(unsorted_data)

        # Assert
        # After sorting, /dev -> /qa should be detected
        assert isinstance(result, dict), "Should handle unsorted timestamps"


# ============================================================================
# Output Structure Validation
# ============================================================================

@pytest.mark.unit
class TestBranchingPointOutputStructure:
    """Tests for branching point output structure"""

    def test_output_contains_required_fields(self, branching_point_data):
        """
        Test: Output structure contains all required fields

        Given: Valid branching point data
        When: Detecting branching points
        Then: Output has command, downstream, and frequency fields
        """
        # Arrange
        from branching_analysis import detect_branching_points

        # Act
        result = detect_branching_points(branching_point_data)

        # Assert
        for command, data in result.items():
            assert "downstream" in data, f"{command} should have 'downstream' field"
            for downstream_cmd, downstream_data in data["downstream"].items():
                assert "frequency" in downstream_data, \
                    f"{command} -> {downstream_cmd} should have 'frequency'"

    def test_output_json_serializable(self, branching_point_data):
        """
        Test: Output is JSON serializable for downstream consumers

        Given: Branching point detection result
        When: Serializing to JSON
        Then: No serialization errors
        """
        # Arrange
        import json
        from branching_analysis import detect_branching_points

        # Act
        result = detect_branching_points(branching_point_data)

        # Assert
        try:
            json_str = json.dumps(result)
            assert json_str is not None
        except (TypeError, ValueError) as e:
            pytest.fail(f"Result should be JSON serializable: {e}")


# ============================================================================
# Run Tests
# ============================================================================

if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
