"""
Test: AC#3 - validate_phase_steps() Returns Pass/Fail Based on Required Steps
Story: STORY-525
Generated: 2026-03-02

Tests FAIL initially because validate_phase_steps() does not exist on PhaseState.
"""

import json
import sys
from pathlib import Path
from unittest.mock import patch

import pytest

SRC_ROOT = Path(__file__).resolve().parents[2] / "src" / "claude" / "scripts"
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

from devforgeai_cli.phase_state import PhaseState


class TestValidatePhaseStepsExists:
    """validate_phase_steps() method must exist on PhaseState."""

    def test_validate_phase_steps_method_exists(self, phase_state):
        """Arrange: PhaseState instance. Act: Check method. Assert: callable."""
        assert hasattr(phase_state, "validate_phase_steps"), (
            "PhaseState must have validate_phase_steps() method"
        )
        assert callable(getattr(phase_state, "validate_phase_steps"))


class TestValidatePhaseStepsPass:
    """Returns PASS when all required steps present."""

    def test_validate_returns_pass_when_all_required_steps_present(
        self, initialized_state, registry_with_file, sample_registry
    ):
        """Arrange: All required steps recorded. Act: validate. Assert: PASS."""
        ps = initialized_state
        # Record all non-conditional steps for phase 02
        for step in sample_registry["02"]["steps"]:
            if not step.get("conditional", False):
                ps.record_step("STORY-525", "02", step["id"])

        with patch.object(ps, "_get_registry_path", return_value=registry_with_file):
            result = ps.validate_phase_steps("STORY-525", "02")

        assert result["status"] == "PASS"
        assert result["missing_steps"] == []


class TestValidatePhaseStepsFail:
    """Returns FAIL with missing step IDs when steps absent."""

    def test_validate_returns_fail_when_steps_missing(
        self, initialized_state, registry_with_file, sample_registry
    ):
        """Arrange: Only 1 of 3 required steps. Act: validate. Assert: FAIL with missing."""
        ps = initialized_state
        ps.record_step("STORY-525", "02", "02.1")

        with patch.object(ps, "_get_registry_path", return_value=registry_with_file):
            result = ps.validate_phase_steps("STORY-525", "02")

        assert result["status"] == "FAIL"
        assert len(result["missing_steps"]) > 0
        assert "02.2" in result["missing_steps"]
        assert "02.3" in result["missing_steps"]

    def test_validate_returns_fail_with_correct_missing_ids(
        self, initialized_state, registry_with_file
    ):
        """Arrange: No steps recorded. Act: validate. Assert: All required in missing."""
        ps = initialized_state

        with patch.object(ps, "_get_registry_path", return_value=registry_with_file):
            result = ps.validate_phase_steps("STORY-525", "02")

        assert result["status"] == "FAIL"
        # 3 required steps (02.1, 02.2, 02.3) should be missing; 02.4 is conditional
        assert "02.1" in result["missing_steps"]
        assert "02.2" in result["missing_steps"]
        assert "02.3" in result["missing_steps"]


class TestValidatePhaseStepsConditionalExcluded:
    """Conditional steps excluded from required set."""

    def test_validate_excludes_conditional_steps_from_required(
        self, initialized_state, registry_with_file, sample_registry
    ):
        """Arrange: All required done, conditional missing. Act: validate. Assert: PASS."""
        ps = initialized_state
        # Record only non-conditional steps
        for step in sample_registry["02"]["steps"]:
            if not step.get("conditional", False):
                ps.record_step("STORY-525", "02", step["id"])
        # Do NOT record 02.4 (conditional)

        with patch.object(ps, "_get_registry_path", return_value=registry_with_file):
            result = ps.validate_phase_steps("STORY-525", "02")

        assert result["status"] == "PASS"
        assert "02.4" not in result["missing_steps"]

    def test_validate_conditional_step_not_in_missing_when_absent(
        self, initialized_state, registry_with_file
    ):
        """Arrange: No steps done. Act: validate. Assert: conditional 02.4 NOT in missing."""
        ps = initialized_state

        with patch.object(ps, "_get_registry_path", return_value=registry_with_file):
            result = ps.validate_phase_steps("STORY-525", "02")

        assert "02.4" not in result["missing_steps"]


class TestValidatePhaseStepsEmptyCompleted:
    """Returns FAIL with all required steps when steps_completed absent/empty."""

    def test_validate_returns_fail_when_steps_completed_empty(
        self, initialized_state, registry_with_file
    ):
        """Arrange: Empty steps_completed. Act: validate. Assert: FAIL with all required."""
        ps = initialized_state

        with patch.object(ps, "_get_registry_path", return_value=registry_with_file):
            result = ps.validate_phase_steps("STORY-525", "02")

        assert result["status"] == "FAIL"
        assert len(result["missing_steps"]) == 3  # 3 non-conditional steps

    def test_validate_returns_fail_when_steps_completed_absent(
        self, initialized_state, registry_with_file
    ):
        """Arrange: Remove steps_completed key. Act: validate. Assert: FAIL."""
        ps = initialized_state
        # Manually remove steps_completed from state
        state = ps.read("STORY-525")
        if "steps_completed" in state["phases"].get("02", {}):
            del state["phases"]["02"]["steps_completed"]
        path = ps._get_state_path("STORY-525")
        ps._atomic_write(path, state)

        with patch.object(ps, "_get_registry_path", return_value=registry_with_file):
            result = ps.validate_phase_steps("STORY-525", "02")

        assert result["status"] == "FAIL"
        assert len(result["missing_steps"]) == 3


class TestValidatePhaseStepsReturnFormat:
    """Return dict has exactly status and missing_steps keys."""

    def test_validate_return_has_status_key(self, initialized_state, registry_with_file):
        """Arrange: State exists. Act: validate. Assert: 'status' in result."""
        ps = initialized_state
        with patch.object(ps, "_get_registry_path", return_value=registry_with_file):
            result = ps.validate_phase_steps("STORY-525", "02")
        assert "status" in result

    def test_validate_return_has_missing_steps_key(self, initialized_state, registry_with_file):
        """Arrange: State exists. Act: validate. Assert: 'missing_steps' in result."""
        ps = initialized_state
        with patch.object(ps, "_get_registry_path", return_value=registry_with_file):
            result = ps.validate_phase_steps("STORY-525", "02")
        assert "missing_steps" in result
        assert isinstance(result["missing_steps"], list)
