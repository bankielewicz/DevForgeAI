"""
STORY-148: Phase State File Module Tests

TDD Red Phase: All tests written before implementation.
These tests will FAIL until PhaseState module is implemented.

Acceptance Criteria Covered:
- AC#1: Create phase state file at workflow start
- AC#2: Record subagent invocation during phase execution
- AC#3: Mark phase as complete with checkpoint status
- AC#4: Read current phase state without modification
- AC#5: Validate state structure before persistence
- AC#6: Archive completed state files
- AC#7: Handle concurrent writes with file locking
"""

import json
import os
import sys
import tempfile
import threading
import time
from datetime import datetime, timezone
from pathlib import Path
from unittest.mock import patch, MagicMock

import pytest

# Add parent directory to path so 'installer' module can be imported
sys.path.insert(0, str(Path(__file__).parent.parent.parent))


# =============================================================================
# Test Fixtures
# =============================================================================


@pytest.fixture
def temp_project_dir():
    """Create a temporary project directory with workflows structure."""
    with tempfile.TemporaryDirectory() as tmpdir:
        project_root = Path(tmpdir)
        # Create devforgeai/workflows directory
        workflows_dir = project_root / "devforgeai" / "workflows"
        workflows_dir.mkdir(parents=True, exist_ok=True)
        # Create completed directory for archives
        completed_dir = workflows_dir / "completed"
        completed_dir.mkdir(parents=True, exist_ok=True)
        yield project_root


@pytest.fixture
def phase_state(temp_project_dir):
    """Create PhaseState instance with temp directory."""
    from installer.phase_state import PhaseState
    return PhaseState(project_root=temp_project_dir)


@pytest.fixture
def existing_state_file(temp_project_dir):
    """Create an existing phase state file for testing."""
    state = {
        "story_id": "STORY-001",
        "workflow_started": "2025-12-24T10:00:00Z",
        "current_phase": "02",
        "phases": {
            "01": {
                "status": "completed",
                "started_at": "2025-12-24T10:00:00Z",
                "completed_at": "2025-12-24T10:05:00Z",
                "subagents_required": ["git-validator", "tech-stack-detector"],
                "subagents_invoked": ["git-validator", "tech-stack-detector"],
                "checkpoint_passed": True
            },
            "02": {"status": "pending", "subagents_required": ["test-automator"], "subagents_invoked": []},
            "03": {"status": "pending", "subagents_required": [], "subagents_invoked": []},
            "04": {"status": "pending", "subagents_required": [], "subagents_invoked": []},
            "05": {"status": "pending", "subagents_required": [], "subagents_invoked": []},
            "06": {"status": "pending", "subagents_required": [], "subagents_invoked": []},
            "07": {"status": "pending", "subagents_required": [], "subagents_invoked": []},
            "08": {"status": "pending", "subagents_required": [], "subagents_invoked": []},
            "09": {"status": "pending", "subagents_required": [], "subagents_invoked": []},
            "10": {"status": "pending", "subagents_required": [], "subagents_invoked": []}
        },
        "validation_errors": [],
        "blocking_status": False
    }

    state_file = temp_project_dir / "devforgeai" / "workflows" / "STORY-001-phase-state.json"
    state_file.write_text(json.dumps(state, indent=2))
    return state_file


@pytest.fixture
def completed_state_file(temp_project_dir):
    """Create a fully completed state file for archive testing."""
    state = {
        "story_id": "STORY-002",
        "workflow_started": "2025-12-24T08:00:00Z",
        "workflow_completed": "2025-12-24T12:00:00Z",
        "current_phase": "10",
        "phases": {
            f"{i:02d}": {
                "status": "completed",
                "started_at": f"2025-12-24T{8+i-1:02d}:00:00Z",
                "completed_at": f"2025-12-24T{8+i:02d}:00:00Z",
                "subagents_required": [],
                "subagents_invoked": [],
                "checkpoint_passed": True
            }
            for i in range(1, 11)
        },
        "validation_errors": [],
        "blocking_status": False
    }

    state_file = temp_project_dir / "devforgeai" / "workflows" / "STORY-002-phase-state.json"
    state_file.write_text(json.dumps(state, indent=2))
    return state_file


# =============================================================================
# AC#1: Create phase state file at workflow start
# =============================================================================


class TestPhaseStateCreate:
    """Tests for AC#1: Create phase state file at workflow start."""

    def test_create_initializes_all_phases(self, phase_state, temp_project_dir):
        """Test that create() initializes all 10 phases with pending status."""
        result = phase_state.create("STORY-100")

        assert result is not None
        assert result["story_id"] == "STORY-100"
        assert result["current_phase"] == "01"
        assert len(result["phases"]) == 10

        # All phases should be pending
        for i in range(1, 11):
            phase_id = f"{i:02d}"
            assert result["phases"][phase_id]["status"] == "pending"

    def test_create_generates_iso_timestamp(self, phase_state):
        """Test that workflow_started is a valid ISO-8601 timestamp."""
        result = phase_state.create("STORY-101")

        # Should be parseable as ISO timestamp
        timestamp = result["workflow_started"]
        assert "T" in timestamp
        assert timestamp.endswith("Z") or "+" in timestamp

        # Should be parseable
        datetime.fromisoformat(timestamp.replace("Z", "+00:00"))

    def test_create_writes_to_correct_path(self, phase_state, temp_project_dir):
        """Test that state file is created at correct location."""
        phase_state.create("STORY-102")

        expected_path = temp_project_dir / "devforgeai" / "workflows" / "STORY-102-phase-state.json"
        assert expected_path.exists()

    def test_create_initializes_validation_errors_empty(self, phase_state):
        """Test that validation_errors is initialized as empty array."""
        result = phase_state.create("STORY-103")

        assert result["validation_errors"] == []

    def test_create_initializes_blocking_status_false(self, phase_state):
        """Test that blocking_status is initialized as false."""
        result = phase_state.create("STORY-104")

        assert result["blocking_status"] is False

    def test_create_is_idempotent(self, phase_state, existing_state_file):
        """Test that create() returns existing state if file exists (BR-004)."""
        # Existing state has current_phase "02"
        result = phase_state.create("STORY-001")

        # Should return existing state, not reset to phase 01
        assert result["current_phase"] == "02"
        assert result["phases"]["01"]["status"] == "completed"

    def test_create_with_invalid_story_id_raises_error(self, phase_state):
        """Test that invalid story_id raises ValueError."""
        with pytest.raises(ValueError, match="Invalid story_id"):
            phase_state.create("INVALID-001")

        with pytest.raises(ValueError, match="Invalid story_id"):
            phase_state.create("STORY-1")  # Must be 3 digits

        with pytest.raises(ValueError, match="Invalid story_id"):
            phase_state.create("story-001")  # Case sensitive

    def test_create_auto_creates_directories(self, temp_project_dir):
        """Test that create() auto-creates missing directories."""
        from installer.phase_state import PhaseState

        # Remove workflows directory
        workflows_dir = temp_project_dir / "devforgeai" / "workflows"
        if workflows_dir.exists():
            import shutil
            shutil.rmtree(workflows_dir)

        phase_state = PhaseState(project_root=temp_project_dir)
        result = phase_state.create("STORY-105")

        assert workflows_dir.exists()
        assert (workflows_dir / "STORY-105-phase-state.json").exists()


# =============================================================================
# AC#2: Record subagent invocation during phase execution
# =============================================================================


class TestPhaseStateRecordSubagent:
    """Tests for AC#2: Record subagent invocation during phase execution."""

    def test_record_subagent_appends_to_list(self, phase_state, existing_state_file):
        """Test that record_subagent appends to subagents_invoked list."""
        result = phase_state.record_subagent("STORY-001", "02", "test-automator")

        assert result is True

        # Verify by reading state
        state = phase_state.read("STORY-001")
        assert "test-automator" in state["phases"]["02"]["subagents_invoked"]

    def test_record_subagent_preserves_existing_entries(self, phase_state, existing_state_file):
        """Test that recording new subagent doesn't remove existing ones."""
        # Phase 01 already has git-validator and tech-stack-detector
        phase_state.record_subagent("STORY-001", "01", "new-subagent")

        state = phase_state.read("STORY-001")
        invoked = state["phases"]["01"]["subagents_invoked"]

        assert "git-validator" in invoked
        assert "tech-stack-detector" in invoked
        assert "new-subagent" in invoked

    def test_record_subagent_returns_false_for_missing_file(self, phase_state):
        """Test that record_subagent returns False if state file doesn't exist."""
        result = phase_state.record_subagent("STORY-999", "01", "test-automator")

        assert result is False

    def test_record_subagent_rejects_invalid_phase_id(self, phase_state, existing_state_file):
        """Test that invalid phase_id raises PhaseNotFoundError."""
        from installer.phase_state import PhaseNotFoundError

        with pytest.raises(PhaseNotFoundError):
            phase_state.record_subagent("STORY-001", "99", "test-automator")

        with pytest.raises(PhaseNotFoundError):
            phase_state.record_subagent("STORY-001", "0", "test-automator")

    def test_record_subagent_doesnt_modify_other_phase_data(self, phase_state, existing_state_file):
        """Test that recording subagent doesn't modify other phase data."""
        original = phase_state.read("STORY-001")
        original_phase_01 = dict(original["phases"]["01"])

        phase_state.record_subagent("STORY-001", "02", "test-automator")

        updated = phase_state.read("STORY-001")
        # Phase 01 should be unchanged
        assert updated["phases"]["01"] == original_phase_01


# =============================================================================
# AC#3: Mark phase as complete with checkpoint status
# =============================================================================


class TestPhaseStateCompletePhase:
    """Tests for AC#3: Mark phase as complete with checkpoint status."""

    def test_complete_phase_advances_workflow(self, phase_state, existing_state_file):
        """Test that complete_phase updates status and advances current_phase."""
        result = phase_state.complete_phase("STORY-001", "02", checkpoint_passed=True)

        assert result is True

        state = phase_state.read("STORY-001")
        assert state["phases"]["02"]["status"] == "completed"
        assert state["phases"]["02"]["checkpoint_passed"] is True
        assert state["current_phase"] == "03"

    def test_complete_phase_records_timestamp(self, phase_state, existing_state_file):
        """Test that complete_phase records completed_at timestamp."""
        phase_state.complete_phase("STORY-001", "02", checkpoint_passed=True)

        state = phase_state.read("STORY-001")
        assert "completed_at" in state["phases"]["02"]

        # Should be valid ISO timestamp
        timestamp = state["phases"]["02"]["completed_at"]
        datetime.fromisoformat(timestamp.replace("Z", "+00:00"))

    def test_complete_phase_with_checkpoint_failed(self, phase_state, existing_state_file):
        """Test that complete_phase can record checkpoint_passed=False."""
        phase_state.complete_phase("STORY-001", "02", checkpoint_passed=False)

        state = phase_state.read("STORY-001")
        assert state["phases"]["02"]["checkpoint_passed"] is False

    def test_complete_phase_10_doesnt_advance_beyond(self, phase_state, temp_project_dir):
        """Test that completing phase 10 doesn't advance beyond 10."""
        # Create state at phase 10
        state = phase_state.create("STORY-010")
        # Manually set to phase 10
        state["current_phase"] = "10"
        for i in range(1, 10):
            state["phases"][f"{i:02d}"]["status"] = "completed"

        state_file = temp_project_dir / "devforgeai" / "workflows" / "STORY-010-phase-state.json"
        state_file.write_text(json.dumps(state))

        phase_state.complete_phase("STORY-010", "10", checkpoint_passed=True)

        updated = phase_state.read("STORY-010")
        assert updated["current_phase"] == "10"  # Should stay at 10
        assert updated["phases"]["10"]["status"] == "completed"

    def test_complete_phase_requires_sequential_order(self, phase_state, existing_state_file):
        """Test that phases must be completed sequentially (BR-001)."""
        from installer.phase_state import PhaseTransitionError

        # Current phase is 02, can't complete phase 03
        with pytest.raises(PhaseTransitionError):
            phase_state.complete_phase("STORY-001", "03", checkpoint_passed=True)


# =============================================================================
# AC#4: Read current phase state without modification
# =============================================================================


class TestPhaseStateRead:
    """Tests for AC#4: Read current phase state without modification."""

    def test_read_returns_current_state(self, phase_state, existing_state_file):
        """Test that read() returns complete current state."""
        state = phase_state.read("STORY-001")

        assert state["story_id"] == "STORY-001"
        assert state["current_phase"] == "02"
        assert "phases" in state
        assert "workflow_started" in state

    def test_read_doesnt_modify_file(self, phase_state, existing_state_file):
        """Test that read() doesn't modify the state file."""
        original_content = existing_state_file.read_text()
        original_mtime = existing_state_file.stat().st_mtime

        time.sleep(0.01)  # Small delay to detect modifications
        _ = phase_state.read("STORY-001")

        assert existing_state_file.read_text() == original_content
        assert existing_state_file.stat().st_mtime == original_mtime

    def test_read_preserves_all_timestamps(self, phase_state, existing_state_file):
        """Test that read() preserves all timestamps accurately."""
        state = phase_state.read("STORY-001")

        assert state["workflow_started"] == "2025-12-24T10:00:00Z"
        assert state["phases"]["01"]["started_at"] == "2025-12-24T10:00:00Z"
        assert state["phases"]["01"]["completed_at"] == "2025-12-24T10:05:00Z"

    def test_read_preserves_subagent_invocations(self, phase_state, existing_state_file):
        """Test that read() preserves subagent invocation list."""
        state = phase_state.read("STORY-001")

        invoked = state["phases"]["01"]["subagents_invoked"]
        assert "git-validator" in invoked
        assert "tech-stack-detector" in invoked

    def test_read_returns_none_for_missing_file(self, phase_state):
        """Test that read() returns None if file doesn't exist."""
        result = phase_state.read("STORY-999")

        assert result is None

    def test_read_raises_error_for_corrupted_file(self, phase_state, temp_project_dir):
        """Test that read() raises StateFileCorruptionError for invalid JSON."""
        from installer.phase_state import StateFileCorruptionError

        # Create corrupted file
        corrupted_file = temp_project_dir / "devforgeai" / "workflows" / "STORY-BAD-phase-state.json"
        corrupted_file.write_text("{ invalid json }")

        with pytest.raises(StateFileCorruptionError):
            phase_state.read("STORY-BAD")


# =============================================================================
# AC#5: Validate state structure before persistence
# =============================================================================


class TestPhaseStateValidation:
    """Tests for AC#5: Validate state structure before persistence."""

    def test_validate_rejects_invalid_state(self, phase_state):
        """Test that validate_state rejects invalid state."""
        invalid_state = {"story_id": "STORY-001"}  # Missing required fields

        is_valid, error_msg = phase_state.validate_state(invalid_state)

        assert is_valid is False
        assert "Missing required field" in error_msg

    def test_validate_rejects_missing_current_phase(self, phase_state):
        """Test that validate_state rejects missing current_phase."""
        invalid_state = {
            "story_id": "STORY-001",
            "workflow_started": "2025-12-24T10:00:00Z",
            "phases": {},
            "validation_errors": [],
            "blocking_status": False
            # Missing current_phase
        }

        is_valid, error_msg = phase_state.validate_state(invalid_state)

        assert is_valid is False
        assert "current_phase" in error_msg

    def test_validate_rejects_invalid_phase_status(self, phase_state):
        """Test that validate_state rejects invalid phase status enum."""
        invalid_state = {
            "story_id": "STORY-001",
            "workflow_started": "2025-12-24T10:00:00Z",
            "current_phase": "01",
            "phases": {
                "01": {"status": "INVALID_STATUS", "subagents_invoked": []}
            },
            "validation_errors": [],
            "blocking_status": False
        }

        is_valid, error_msg = phase_state.validate_state(invalid_state)

        assert is_valid is False
        assert "Invalid status" in error_msg or "enum" in error_msg.lower()

    def test_validate_accepts_valid_state(self, phase_state):
        """Test that validate_state accepts valid state structure."""
        valid_state = {
            "story_id": "STORY-001",
            "workflow_started": "2025-12-24T10:00:00Z",
            "current_phase": "01",
            "phases": {
                f"{i:02d}": {
                    "status": "pending",
                    "subagents_required": [],
                    "subagents_invoked": []
                }
                for i in range(1, 11)
            },
            "validation_errors": [],
            "blocking_status": False
        }

        is_valid, error_msg = phase_state.validate_state(valid_state)

        assert is_valid is True
        assert error_msg == ""

    def test_validate_rejects_wrong_type_blocking_status(self, phase_state):
        """Test that validate_state rejects non-boolean blocking_status."""
        invalid_state = {
            "story_id": "STORY-001",
            "workflow_started": "2025-12-24T10:00:00Z",
            "current_phase": "01",
            "phases": {},
            "validation_errors": [],
            "blocking_status": "false"  # String instead of boolean
        }

        is_valid, error_msg = phase_state.validate_state(invalid_state)

        assert is_valid is False


# =============================================================================
# AC#6: Archive completed state files
# =============================================================================


class TestPhaseStateArchive:
    """Tests for AC#6: Archive completed state files."""

    def test_archive_moves_to_completed(self, phase_state, completed_state_file, temp_project_dir):
        """Test that archive moves state file to completed directory."""
        result = phase_state.archive("STORY-002")

        assert result is True

        # Original should be removed
        original_path = temp_project_dir / "devforgeai" / "workflows" / "STORY-002-phase-state.json"
        assert not original_path.exists()

        # Should exist in completed directory
        archived_path = temp_project_dir / "devforgeai" / "workflows" / "completed" / "STORY-002-phase-state.json"
        assert archived_path.exists()

    def test_archive_rejects_incomplete(self, phase_state, existing_state_file):
        """Test that archive rejects stories with pending phases (BR-003)."""
        from installer.phase_state import IncompleteWorkflowError

        # STORY-001 has phases 02-10 still pending
        with pytest.raises(IncompleteWorkflowError):
            phase_state.archive("STORY-001")

    def test_archive_returns_false_for_missing_file(self, phase_state):
        """Test that archive returns False if state file doesn't exist."""
        result = phase_state.archive("STORY-999")

        assert result is False

    def test_archive_creates_completed_directory_if_missing(self, phase_state, completed_state_file, temp_project_dir):
        """Test that archive creates completed directory if it doesn't exist."""
        import shutil

        completed_dir = temp_project_dir / "devforgeai" / "workflows" / "completed"
        shutil.rmtree(completed_dir)

        phase_state.archive("STORY-002")

        assert completed_dir.exists()


# =============================================================================
# AC#7: Handle concurrent writes with file locking
# =============================================================================


class TestPhaseStateConcurrency:
    """Tests for AC#7: Handle concurrent writes with file locking."""

    def test_concurrent_writes_blocked_by_lock(self, phase_state, temp_project_dir):
        """Test that concurrent writes are blocked by file locking."""
        # Create initial state
        phase_state.create("STORY-050")

        results = []
        errors = []

        def record_subagent(agent_name):
            try:
                result = phase_state.record_subagent("STORY-050", "01", agent_name)
                results.append((agent_name, result))
            except Exception as e:
                errors.append((agent_name, str(e)))

        # Launch concurrent threads
        threads = []
        for i in range(5):
            t = threading.Thread(target=record_subagent, args=(f"agent-{i}",))
            threads.append(t)

        for t in threads:
            t.start()

        for t in threads:
            t.join(timeout=10)

        # All should succeed (locked writes)
        assert len(results) == 5
        assert all(r[1] for r in results)

        # Verify all agents were recorded
        state = phase_state.read("STORY-050")
        invoked = state["phases"]["01"]["subagents_invoked"]
        for i in range(5):
            assert f"agent-{i}" in invoked

    def test_lock_timeout_raises_error(self, phase_state, temp_project_dir):
        """Test that lock timeout raises appropriate error."""
        from installer.phase_state import LockTimeoutError

        # Create initial state
        phase_state.create("STORY-051")

        state_file = temp_project_dir / "devforgeai" / "workflows" / "STORY-051-phase-state.json"
        lock_file = state_file.with_suffix(".lock")

        # Simulate another process holding the lock
        lock_file.write_text("locked")

        # This test requires platform-specific behavior
        # On Unix, use fcntl; on Windows, use msvcrt
        # For testing, we simulate with a mock
        with patch.object(phase_state, '_acquire_lock', side_effect=LockTimeoutError(str(state_file), 5)):
            with pytest.raises(LockTimeoutError):
                phase_state.record_subagent("STORY-051", "01", "test-agent")


# =============================================================================
# Business Rule Tests
# =============================================================================


class TestPhaseStateBusinessRules:
    """Tests for business rules from technical specification."""

    def test_phase_transition_ordering(self, phase_state, temp_project_dir):
        """Test BR-001: Phase transitions must follow strict ordering."""
        from installer.phase_state import PhaseTransitionError

        phase_state.create("STORY-060")

        # Can't skip from 01 to 03
        with pytest.raises(PhaseTransitionError):
            phase_state.complete_phase("STORY-060", "03", checkpoint_passed=True)

    def test_subagent_records_immutable(self, phase_state, existing_state_file):
        """Test BR-002: Subagent invocations are append-only."""
        original = phase_state.read("STORY-001")
        original_invoked = original["phases"]["01"]["subagents_invoked"].copy()

        # Add a new subagent
        phase_state.record_subagent("STORY-001", "01", "new-agent")

        updated = phase_state.read("STORY-001")

        # Original entries should still be there
        for agent in original_invoked:
            assert agent in updated["phases"]["01"]["subagents_invoked"]

    def test_create_is_idempotent_br004(self, phase_state, existing_state_file):
        """Test BR-004: State file creation is idempotent."""
        # Read current state
        original = phase_state.read("STORY-001")

        # Try to create again
        result = phase_state.create("STORY-001")

        # Should return existing state, not a new one
        assert result["current_phase"] == original["current_phase"]
        assert result["phases"]["01"]["status"] == original["phases"]["01"]["status"]


# =============================================================================
# Performance Tests
# =============================================================================


class TestPhaseStatePerformance:
    """Performance tests from non-functional requirements."""

    def test_create_performance(self, phase_state, temp_project_dir):
        """Test that state file creation completes in < 50ms."""
        import timeit

        def create_state():
            import uuid
            story_id = f"STORY-{str(uuid.uuid4())[:3].upper()}"
            # Use valid story ID format
            story_id = f"STORY-{hash(story_id) % 900 + 100:03d}"
            phase_state.create(story_id)

        # Warm up
        create_state()

        # Measure
        duration = timeit.timeit(create_state, number=10) / 10

        assert duration < 0.050  # 50ms p95

    def test_read_performance(self, phase_state, existing_state_file):
        """Test that state file read completes in < 20ms."""
        import timeit

        def read_state():
            phase_state.read("STORY-001")

        # Warm up
        read_state()

        # Measure
        duration = timeit.timeit(read_state, number=10) / 10

        assert duration < 0.020  # 20ms p95


# =============================================================================
# Edge Case Tests
# =============================================================================


class TestPhaseStateEdgeCases:
    """Tests for edge cases from STORY-148."""

    def test_story_id_validation_pattern(self, phase_state):
        """Test that story_id must match STORY-\\d{3} pattern."""
        # Valid patterns
        phase_state.create("STORY-001")
        phase_state.create("STORY-999")

        # Invalid patterns
        with pytest.raises(ValueError):
            phase_state.create("STORY-1234")  # Too many digits

        with pytest.raises(ValueError):
            phase_state.create("story-001")  # Lowercase

        with pytest.raises(ValueError):
            phase_state.create("TASK-001")  # Wrong prefix

    def test_corrupted_json_recovery(self, phase_state, temp_project_dir):
        """Test that corrupted JSON provides recovery instructions."""
        from installer.phase_state import StateFileCorruptionError

        corrupted_file = temp_project_dir / "devforgeai" / "workflows" / "STORY-BAD-phase-state.json"
        corrupted_file.write_text("{ not valid json")

        try:
            phase_state.read("STORY-BAD")
            pytest.fail("Should have raised StateFileCorruptionError")
        except StateFileCorruptionError as e:
            assert "recovery" in str(e).lower() or "corrupted" in str(e).lower()

    def test_atomic_write_safety(self, phase_state, temp_project_dir):
        """Test atomic writes using temp file + rename pattern."""
        phase_state.create("STORY-070")

        # The implementation should use temp file + rename
        # We verify by checking that partial writes don't corrupt
        state_file = temp_project_dir / "devforgeai" / "workflows" / "STORY-070-phase-state.json"

        # Read should always return valid JSON
        state = phase_state.read("STORY-070")
        assert state is not None
        assert state["story_id"] == "STORY-070"


# =============================================================================
# Module Import Test
# =============================================================================


class TestPhaseStateModuleImport:
    """Tests for module availability and imports."""

    def test_module_importable(self):
        """Test that phase_state module can be imported."""
        from installer import phase_state
        assert hasattr(phase_state, 'PhaseState')

    def test_exceptions_importable(self):
        """Test that custom exceptions can be imported."""
        from installer.phase_state import (
            PhaseNotFoundError,
            StateFileCorruptionError,
            IncompleteWorkflowError,
            PhaseTransitionError,
            LockTimeoutError
        )

        assert issubclass(PhaseNotFoundError, Exception)
        assert issubclass(StateFileCorruptionError, Exception)
        assert issubclass(IncompleteWorkflowError, Exception)
        assert issubclass(PhaseTransitionError, Exception)
        assert issubclass(LockTimeoutError, Exception)
