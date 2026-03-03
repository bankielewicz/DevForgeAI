"""
Test: AC#5 - Registry Is Authoritative Source for validate_phase_steps()
Story: STORY-525
Generated: 2026-03-02

Tests FAIL initially because validate_phase_steps() and _get_registry_path() don't exist.
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


class TestRegistryIsSourceOfTruth:
    """validate_phase_steps() loads from registry JSON, not hardcoded lists."""

    def test_validate_uses_registry_not_hardcoded(
        self, initialized_state, project_root
    ):
        """Arrange: Custom registry with unique steps. Act: validate. Assert: Uses registry steps."""
        ps = initialized_state

        # Create a custom registry with a non-standard step
        custom_registry = {
            "02": {
                "name": "Test Phase",
                "entry_gate": "test",
                "exit_gate": "test",
                "steps": [
                    {"id": "02.99", "check": "Custom step", "subagent": None, "conditional": False},
                ]
            }
        }
        reg_path = project_root / ".claude" / "hooks" / "phase-steps-registry.json"
        reg_path.parent.mkdir(parents=True, exist_ok=True)
        reg_path.write_text(json.dumps(custom_registry))

        with patch.object(ps, "_get_registry_path", return_value=reg_path):
            result = ps.validate_phase_steps("STORY-525", "02")

        # Should report 02.99 as missing (from registry), not hardcoded steps
        assert result["status"] == "FAIL"
        assert "02.99" in result["missing_steps"]

    def test_validate_does_not_use_dev_phases_dict(
        self, initialized_state, registry_with_file
    ):
        """Arrange: Registry differs from DEV_PHASES. Act: validate. Assert: Registry wins."""
        ps = initialized_state

        # DEV_PHASES has steps_required: ["test_generation", "test_failure_verification"]
        # Registry has steps: [02.1, 02.2, 02.3, 02.4]
        # validate_phase_steps must use registry, not DEV_PHASES
        with patch.object(ps, "_get_registry_path", return_value=registry_with_file):
            result = ps.validate_phase_steps("STORY-525", "02")

        # Missing steps should be registry step IDs (02.1, 02.2, 02.3), NOT DEV_PHASES keys
        assert result["status"] == "FAIL"
        for step_id in result["missing_steps"]:
            assert "." in step_id, f"Step ID '{step_id}' looks like DEV_PHASES key, not registry ID"


class TestRegistryAbsentRaisesFileNotFound:
    """FileNotFoundError if registry absent."""

    def test_validate_raises_file_not_found_when_registry_missing(self, initialized_state):
        """Arrange: No registry file. Act: validate. Assert: FileNotFoundError."""
        ps = initialized_state
        nonexistent = ps.project_root / ".claude" / "hooks" / "phase-steps-registry.json"
        assert not nonexistent.exists()

        with patch.object(ps, "_get_registry_path", return_value=nonexistent):
            with pytest.raises(FileNotFoundError):
                ps.validate_phase_steps("STORY-525", "02")


class TestRegistryMalformedRaisesJsonDecodeError:
    """json.JSONDecodeError if registry malformed."""

    def test_validate_raises_json_decode_error_when_registry_malformed(
        self, initialized_state, registry_path
    ):
        """Arrange: Malformed JSON in registry. Act: validate. Assert: JSONDecodeError."""
        ps = initialized_state
        registry_path.write_text("{invalid json content!!!")

        with patch.object(ps, "_get_registry_path", return_value=registry_path):
            with pytest.raises(json.JSONDecodeError):
                ps.validate_phase_steps("STORY-525", "02")


class TestGetRegistryPathMethod:
    """_get_registry_path() helper method must exist."""

    def test_get_registry_path_exists(self, phase_state):
        """Arrange: PhaseState instance. Act: Check method. Assert: callable."""
        assert hasattr(phase_state, "_get_registry_path"), (
            "PhaseState must have _get_registry_path() method"
        )

    def test_get_registry_path_returns_path(self, phase_state):
        """Arrange: PhaseState instance. Act: Call method. Assert: returns Path."""
        path = phase_state._get_registry_path()
        assert isinstance(path, Path)
        assert "phase-steps-registry.json" in str(path)
