"""
Integration Tests: STORY-525 - Phase Steps Registry + Step-Level Tracking

Tests cross-component interactions:
  1. Full CLI flow: phase_record_step_command → state file update → validate_phase_steps PASS
  2. Registry + Validation integration: write registry → record steps → validate passes
  3. Error propagation: missing registry → CLI command returns 1

All tests use tmp_path for isolation.
Imports from src/ tree per project conventions.
"""

import json
import sys
from pathlib import Path

import pytest

# Add src tree to path for imports
SRC_ROOT = Path(__file__).resolve().parents[2] / "src" / "claude" / "scripts"
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

from devforgeai_cli.phase_state import PhaseState
from devforgeai_cli.commands.phase_commands import phase_record_step_command


# ---------------------------------------------------------------------------
# Shared helpers
# ---------------------------------------------------------------------------

MINIMAL_REGISTRY = {
    "02": {
        "name": "Test-First (Red)",
        "entry_gate": "devforgeai-validate phase-check STORY-525 --from=01 --to=02",
        "exit_gate": "devforgeai-validate phase-complete STORY-525 --phase=02 --checkpoint-passed",
        "steps": [
            {
                "id": "02.1",
                "check": "test-automator subagent invoked",
                "subagent": "test-automator",
                "conditional": False,
            },
            {
                "id": "02.2",
                "check": "Failing tests written for all ACs",
                "subagent": "test-automator",
                "conditional": False,
            },
            {
                "id": "02.3",
                "check": "Test integrity snapshot captured",
                "subagent": None,
                "conditional": False,
            },
            {
                "id": "02.4",
                "check": "Optional pre-phase planning",
                "subagent": None,
                "conditional": True,
            },
        ],
    }
}


def _setup_project(tmp_path: Path) -> tuple[PhaseState, Path]:
    """
    Create an isolated project root with:
    - workflows directory
    - .claude/hooks directory for the registry

    Returns (PhaseState instance, registry path).
    """
    (tmp_path / "devforgeai" / "workflows").mkdir(parents=True)
    hooks_dir = tmp_path / ".claude" / "hooks"
    hooks_dir.mkdir(parents=True)
    registry_path = hooks_dir / "phase-steps-registry.json"
    return PhaseState(project_root=tmp_path), registry_path


# ---------------------------------------------------------------------------
# Scenario 1: Full CLI flow
#   phase_record_step_command → state file update → validate_phase_steps PASS
# ---------------------------------------------------------------------------


class TestFullCLIFlow:
    """Integration: CLI command drives state update; validate_phase_steps confirms PASS."""

    def test_cli_records_step_and_validate_passes(self, tmp_path):
        """
        Arrange: Create state + registry with 3 required steps.
        Act: Record all 3 required steps via phase_record_step_command.
        Assert: validate_phase_steps returns PASS with no missing steps.
        """
        ps, registry_path = _setup_project(tmp_path)
        registry_path.write_text(json.dumps(MINIMAL_REGISTRY, indent=2))

        # Create phase state
        ps.create("STORY-525")

        # Record all required steps via CLI command
        required_step_ids = ["02.1", "02.2", "02.3"]
        for step_id in required_step_ids:
            exit_code = phase_record_step_command(
                story_id="STORY-525",
                phase="02",
                step_id=step_id,
                project_root=str(tmp_path),
            )
            assert exit_code == 0, f"CLI command failed for step {step_id}"

        # Validate: all required steps done → PASS
        result = ps.validate_phase_steps("STORY-525", "02")
        assert result["status"] == "PASS"
        assert result["missing_steps"] == []

    def test_cli_partial_steps_then_validate_fails(self, tmp_path):
        """
        Arrange: Create state + registry with 3 required steps.
        Act: Record only 1 of 3 required steps via CLI.
        Assert: validate_phase_steps returns FAIL with 2 missing step IDs.
        """
        ps, registry_path = _setup_project(tmp_path)
        registry_path.write_text(json.dumps(MINIMAL_REGISTRY, indent=2))

        ps.create("STORY-525")

        # Record only the first step
        exit_code = phase_record_step_command(
            story_id="STORY-525",
            phase="02",
            step_id="02.1",
            project_root=str(tmp_path),
        )
        assert exit_code == 0

        # Validate: 2 required steps missing → FAIL
        result = ps.validate_phase_steps("STORY-525", "02")
        assert result["status"] == "FAIL"
        assert "02.2" in result["missing_steps"]
        assert "02.3" in result["missing_steps"]

    def test_cli_step_persisted_to_state_file(self, tmp_path):
        """
        Arrange: Create state + registry.
        Act: Record step via CLI.
        Assert: State file on disk contains the step_id under the correct phase.
        """
        ps, registry_path = _setup_project(tmp_path)
        registry_path.write_text(json.dumps(MINIMAL_REGISTRY, indent=2))

        ps.create("STORY-525")

        phase_record_step_command(
            story_id="STORY-525",
            phase="02",
            step_id="02.2",
            project_root=str(tmp_path),
        )

        # Read state directly from disk to confirm persistence
        state_file = tmp_path / "devforgeai" / "workflows" / "STORY-525-phase-state.json"
        assert state_file.exists(), "State file not found on disk"
        raw = json.loads(state_file.read_text())
        assert "02.2" in raw["phases"]["02"]["steps_completed"]

    def test_cli_idempotent_step_does_not_duplicate(self, tmp_path):
        """
        Arrange: Create state + registry.
        Act: Record same step twice via CLI.
        Assert: steps_completed contains the step exactly once.
        """
        ps, registry_path = _setup_project(tmp_path)
        registry_path.write_text(json.dumps(MINIMAL_REGISTRY, indent=2))

        ps.create("STORY-525")

        phase_record_step_command("STORY-525", "02", "02.1", str(tmp_path))
        phase_record_step_command("STORY-525", "02", "02.1", str(tmp_path))

        state = ps.read("STORY-525")
        assert state["phases"]["02"]["steps_completed"].count("02.1") == 1


# ---------------------------------------------------------------------------
# Scenario 2: Registry + Validation Integration
#   Write registry → record_step() directly → validate_phase_steps passes
# ---------------------------------------------------------------------------


class TestRegistryValidationIntegration:
    """Integration: PhaseState uses registry on disk to drive validation."""

    def test_write_registry_record_steps_validate_passes(self, tmp_path):
        """
        Arrange: Write registry to tmp_path; create phase state.
        Act: Call record_step() for all required steps directly.
        Assert: validate_phase_steps() returns PASS.
        """
        ps, registry_path = _setup_project(tmp_path)
        registry_path.write_text(json.dumps(MINIMAL_REGISTRY, indent=2))

        ps.create("STORY-525")

        # Required steps: 02.1, 02.2, 02.3 (02.4 is conditional)
        ps.record_step("STORY-525", "02", "02.1")
        ps.record_step("STORY-525", "02", "02.2")
        ps.record_step("STORY-525", "02", "02.3")

        result = ps.validate_phase_steps("STORY-525", "02")
        assert result["status"] == "PASS"
        assert result["missing_steps"] == []

    def test_conditional_step_missing_still_passes(self, tmp_path):
        """
        Arrange: Registry with 3 required + 1 conditional step.
        Act: Record only required steps (skip conditional 02.4).
        Assert: validate_phase_steps returns PASS — conditional step excluded.
        """
        ps, registry_path = _setup_project(tmp_path)
        registry_path.write_text(json.dumps(MINIMAL_REGISTRY, indent=2))

        ps.create("STORY-525")

        # Record only required steps; skip conditional 02.4
        ps.record_step("STORY-525", "02", "02.1")
        ps.record_step("STORY-525", "02", "02.2")
        ps.record_step("STORY-525", "02", "02.3")
        # 02.4 intentionally NOT recorded

        result = ps.validate_phase_steps("STORY-525", "02")
        assert result["status"] == "PASS"
        assert "02.4" not in result["missing_steps"]

    def test_empty_steps_completed_returns_all_required_as_missing(self, tmp_path):
        """
        Arrange: State initialized with no steps recorded; registry has 3 required steps.
        Act: validate_phase_steps with empty steps_completed.
        Assert: FAIL with all 3 required steps in missing_steps.
        """
        ps, registry_path = _setup_project(tmp_path)
        registry_path.write_text(json.dumps(MINIMAL_REGISTRY, indent=2))

        ps.create("STORY-525")
        # No record_step calls

        result = ps.validate_phase_steps("STORY-525", "02")
        assert result["status"] == "FAIL"
        assert set(result["missing_steps"]) == {"02.1", "02.2", "02.3"}

    def test_custom_registry_used_not_hardcoded_lists(self, tmp_path):
        """
        Arrange: Write a custom registry with a single required step '02.9'.
        Act: Record step '02.9' directly.
        Assert: validate_phase_steps returns PASS, proving registry (not hardcoded list) was used.
        """
        custom_registry = {
            "02": {
                "name": "Custom Phase",
                "entry_gate": "devforgeai-validate phase-check STORY-525 --from=01 --to=02",
                "exit_gate": "devforgeai-validate phase-complete STORY-525 --phase=02 --checkpoint-passed",
                "steps": [
                    {
                        "id": "02.9",
                        "check": "Custom required step",
                        "subagent": None,
                        "conditional": False,
                    }
                ],
            }
        }
        ps, registry_path = _setup_project(tmp_path)
        registry_path.write_text(json.dumps(custom_registry, indent=2))

        ps.create("STORY-525")
        ps.record_step("STORY-525", "02", "02.9")

        result = ps.validate_phase_steps("STORY-525", "02")
        assert result["status"] == "PASS"


# ---------------------------------------------------------------------------
# Scenario 3: Error propagation
#   Missing registry → CLI command returns 1
# ---------------------------------------------------------------------------


class TestErrorPropagation:
    """Integration: Missing registry causes CLI command to return exit code 1."""

    def test_missing_registry_cli_returns_1(self, tmp_path):
        """
        Arrange: Project root with no registry file at .claude/hooks/phase-steps-registry.json.
        Act: Call phase_record_step_command.
        Assert: Exit code is 1.
        """
        (tmp_path / "devforgeai" / "workflows").mkdir(parents=True)

        # Intentionally do NOT create .claude/hooks/ or registry file
        ps = PhaseState(project_root=tmp_path)
        ps.create("STORY-525")

        exit_code = phase_record_step_command(
            story_id="STORY-525",
            phase="02",
            step_id="02.1",
            project_root=str(tmp_path),
        )
        assert exit_code == 1

    def test_missing_registry_validate_raises_file_not_found(self, tmp_path):
        """
        Arrange: Project root with no registry file.
        Act: Call validate_phase_steps.
        Assert: FileNotFoundError is raised.
        """
        (tmp_path / "devforgeai" / "workflows").mkdir(parents=True)
        ps = PhaseState(project_root=tmp_path)
        ps.create("STORY-525")

        with pytest.raises(FileNotFoundError):
            ps.validate_phase_steps("STORY-525", "02")

    def test_malformed_registry_cli_returns_1(self, tmp_path, capsys):
        """
        Arrange: Registry file containing invalid JSON.
        Act: Call phase_record_step_command.
        Assert: Exit code is 1.
        """
        ps, registry_path = _setup_project(tmp_path)
        registry_path.write_text("{ NOT VALID JSON ]]]")

        ps.create("STORY-525")

        exit_code = phase_record_step_command(
            story_id="STORY-525",
            phase="02",
            step_id="02.1",
            project_root=str(tmp_path),
        )
        assert exit_code == 1

    def test_unknown_step_id_cli_returns_1(self, tmp_path):
        """
        Arrange: Valid registry.
        Act: Call CLI with a step_id not in registry.
        Assert: Exit code is 1 (error propagates up cleanly).
        """
        ps, registry_path = _setup_project(tmp_path)
        registry_path.write_text(json.dumps(MINIMAL_REGISTRY, indent=2))

        ps.create("STORY-525")

        exit_code = phase_record_step_command(
            story_id="STORY-525",
            phase="02",
            step_id="02.99",  # not in registry
            project_root=str(tmp_path),
        )
        assert exit_code == 1
