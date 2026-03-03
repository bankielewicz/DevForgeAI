"""
Test: AC#2 - record_step() Persists Step Completion to Phase State File
Story: STORY-525
Generated: 2026-03-02

Tests FAIL initially because record_step() method does not exist on PhaseState.
"""

import json
import sys
from pathlib import Path
from unittest.mock import patch, MagicMock

import pytest

SRC_ROOT = Path(__file__).resolve().parents[2] / "src" / "claude" / "scripts"
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

from devforgeai_cli.phase_state import PhaseState


class TestRecordStepExists:
    """record_step() method must exist on PhaseState."""

    def test_record_step_method_exists(self, phase_state):
        """Arrange: PhaseState instance. Act: Check method. Assert: callable."""
        assert hasattr(phase_state, "record_step"), "PhaseState must have record_step() method"
        assert callable(getattr(phase_state, "record_step"))


class TestRecordStepAppendsStep:
    """record_step() appends step_id to steps_completed."""

    def test_record_step_adds_step_to_steps_completed(self, initialized_state):
        """Arrange: Initialized state. Act: record_step. Assert: step in steps_completed."""
        ps = initialized_state
        ps.record_step("STORY-525", "02", "02.2")

        state = ps.read("STORY-525")
        assert "steps_completed" in state["phases"]["02"]
        assert "02.2" in state["phases"]["02"]["steps_completed"]

    def test_record_step_multiple_steps(self, initialized_state):
        """Arrange: Initialized state. Act: Record 2 steps. Assert: Both present."""
        ps = initialized_state
        ps.record_step("STORY-525", "02", "02.1")
        ps.record_step("STORY-525", "02", "02.2")

        state = ps.read("STORY-525")
        steps = state["phases"]["02"]["steps_completed"]
        assert "02.1" in steps
        assert "02.2" in steps


class TestRecordStepIdempotent:
    """record_step() with same args is idempotent (no duplicates)."""

    def test_record_step_idempotent_no_duplicates(self, initialized_state):
        """Arrange: Initialized state. Act: Record same step twice. Assert: Appears once."""
        ps = initialized_state
        ps.record_step("STORY-525", "02", "02.2")
        ps.record_step("STORY-525", "02", "02.2")

        state = ps.read("STORY-525")
        steps = state["phases"]["02"]["steps_completed"]
        assert steps.count("02.2") == 1, "Duplicate step recorded"


class TestRecordStepAtomicWrite:
    """record_step() must use _atomic_write() for persistence."""

    def test_record_step_uses_atomic_write(self, initialized_state):
        """Arrange: Patch _atomic_write. Act: record_step. Assert: _atomic_write called."""
        ps = initialized_state
        with patch.object(ps, "_atomic_write", wraps=ps._atomic_write) as mock_write:
            ps.record_step("STORY-525", "02", "02.1")
            mock_write.assert_called_once()


class TestRecordStepNoMutation:
    """record_step() must not mutate other phase data."""

    def test_record_step_does_not_mutate_other_phases(self, initialized_state):
        """Arrange: Snapshot other phases. Act: record_step on 02. Assert: Others unchanged."""
        ps = initialized_state
        state_before = ps.read("STORY-525")
        phase_01_before = json.dumps(state_before["phases"]["01"])

        ps.record_step("STORY-525", "02", "02.1")

        state_after = ps.read("STORY-525")
        phase_01_after = json.dumps(state_after["phases"]["01"])
        assert phase_01_before == phase_01_after, "Phase 01 was mutated by record_step on phase 02"

    def test_record_step_preserves_current_phase(self, initialized_state):
        """Arrange: Note current_phase. Act: record_step. Assert: current_phase unchanged."""
        ps = initialized_state
        state_before = ps.read("STORY-525")
        current_before = state_before["current_phase"]

        ps.record_step("STORY-525", "02", "02.1")

        state_after = ps.read("STORY-525")
        assert state_after["current_phase"] == current_before


class TestRecordStepValidation:
    """record_step() validates inputs."""

    def test_record_step_invalid_story_id_raises(self, phase_state):
        """Arrange: Invalid story ID. Act: record_step. Assert: ValueError."""
        with pytest.raises(ValueError):
            phase_state.record_step("INVALID", "02", "02.1")

    def test_record_step_invalid_phase_raises(self, initialized_state):
        """Arrange: Invalid phase. Act: record_step. Assert: PhaseNotFoundError."""
        from devforgeai_cli.phase_state import PhaseNotFoundError
        with pytest.raises(PhaseNotFoundError):
            initialized_state.record_step("STORY-525", "99", "99.1")

    def test_record_step_missing_state_file_raises(self, phase_state):
        """Arrange: No state file. Act: record_step. Assert: FileNotFoundError."""
        with pytest.raises(FileNotFoundError):
            phase_state.record_step("STORY-525", "02", "02.1")
