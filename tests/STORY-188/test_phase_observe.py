"""
STORY-188: Add Observation Capture Command to Phase CLI - TDD Red Phase Tests

All tests will FAIL until implementation is complete (TDD Red phase).

Acceptance Criteria Covered:
- AC-1: New command `devforgeai-validate phase-observe STORY-XXX --phase=04 --category=friction --note="..."`
- AC-2: Observations array added to phase state file
- AC-3: Observation structure: id, phase, category, note, severity, timestamp
- AC-4: Categories: friction, gap, success, pattern
- AC-5: Severities: low, medium, high
- AC-6: phase-init creates empty observations array

Technical Requirements:
- CLI uses argparse (NOT Click) - see cli.py
- Phase commands in `.claude/scripts/devforgeai_cli/commands/phase_commands.py`
- PhaseState class in `installer/phase_state.py`
- Test framework: pytest (per tech-stack.md Python 3.10+)

Coverage Target: 95%+
Test Framework: pytest (per tech-stack.md)
"""

import json
import sys
import tempfile
import uuid
from datetime import datetime, timezone
from pathlib import Path
from unittest.mock import patch, MagicMock

import pytest

# Add parent directory to path so modules can be imported
sys.path.insert(0, str(Path(__file__).parent.parent.parent))


# =============================================================================
# Fixtures
# =============================================================================


@pytest.fixture
def temp_project_root(tmp_path):
    """Create a temporary project root with workflows directory."""
    workflows_dir = tmp_path / "devforgeai" / "workflows"
    workflows_dir.mkdir(parents=True)
    return tmp_path


@pytest.fixture
def existing_phase_state(temp_project_root):
    """Create an existing phase state file for testing."""
    workflows_dir = temp_project_root / "devforgeai" / "workflows"
    state_file = workflows_dir / "STORY-188-phase-state.json"

    # Create initial state without observations (pre-implementation)
    state = {
        "story_id": "STORY-188",
        "workflow_started": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "current_phase": "04",
        "phases": {
            f"{i:02d}": {
                "status": "pending" if i > 4 else "completed",
                "subagents_required": [],
                "subagents_invoked": []
            }
            for i in range(1, 11)
        },
        "validation_errors": [],
        "blocking_status": False,
        "observations": []  # AC-2: Empty observations array
    }

    state_file.write_text(json.dumps(state, indent=2))
    return state_file


@pytest.fixture
def state_without_observations(temp_project_root):
    """Create a phase state file WITHOUT observations array (legacy format)."""
    workflows_dir = temp_project_root / "devforgeai" / "workflows"
    state_file = workflows_dir / "STORY-099-phase-state.json"

    # Create state without observations array (simulates legacy state file)
    state = {
        "story_id": "STORY-099",
        "workflow_started": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
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
        # NOTE: No "observations" key - legacy format
    }

    state_file.write_text(json.dumps(state, indent=2))
    return state_file


# =============================================================================
# AC-1: New Command Available
# =============================================================================


class TestAC1_CommandAvailable:
    """AC-1: New command `devforgeai-validate phase-observe` available"""

    def test_phase_observe_command_exists_in_cli_module(self):
        """Test: phase_observe_command function exists in phase_commands.py"""
        from devforgeai_cli.commands.phase_commands import phase_observe_command

        assert callable(phase_observe_command), (
            "phase_observe_command must be a callable function"
        )

    def test_phase_observe_accepts_story_id_argument(self):
        """Test: phase_observe_command accepts story_id as first argument"""
        from devforgeai_cli.commands.phase_commands import phase_observe_command

        # Should accept story_id without raising TypeError for missing argument
        # This will fail with appropriate error, not missing argument error
        try:
            result = phase_observe_command(
                story_id="STORY-188",
                phase="04",
                category="friction",
                note="Test observation",
                severity="medium",
                project_root=".",
                format="text"
            )
        except Exception as e:
            # Any exception other than TypeError for missing args is acceptable
            # The function signature is correct if we get here
            assert not str(e).startswith("phase_observe_command() missing"), (
                f"Function signature incorrect: {e}"
            )

    def test_phase_observe_accepts_phase_option(self):
        """Test: phase_observe_command accepts --phase option"""
        from devforgeai_cli.commands.phase_commands import phase_observe_command
        import inspect

        sig = inspect.signature(phase_observe_command)
        params = list(sig.parameters.keys())

        assert "phase" in params, (
            f"phase_observe_command must accept 'phase' parameter. Got: {params}"
        )

    def test_phase_observe_accepts_category_option(self):
        """Test: phase_observe_command accepts --category option"""
        from devforgeai_cli.commands.phase_commands import phase_observe_command
        import inspect

        sig = inspect.signature(phase_observe_command)
        params = list(sig.parameters.keys())

        assert "category" in params, (
            f"phase_observe_command must accept 'category' parameter. Got: {params}"
        )

    def test_phase_observe_accepts_note_option(self):
        """Test: phase_observe_command accepts --note option"""
        from devforgeai_cli.commands.phase_commands import phase_observe_command
        import inspect

        sig = inspect.signature(phase_observe_command)
        params = list(sig.parameters.keys())

        assert "note" in params, (
            f"phase_observe_command must accept 'note' parameter. Got: {params}"
        )

    def test_phase_observe_accepts_severity_option(self):
        """Test: phase_observe_command accepts --severity option"""
        from devforgeai_cli.commands.phase_commands import phase_observe_command
        import inspect

        sig = inspect.signature(phase_observe_command)
        params = list(sig.parameters.keys())

        assert "severity" in params, (
            f"phase_observe_command must accept 'severity' parameter. Got: {params}"
        )

    def test_phase_observe_returns_exit_code(self):
        """Test: phase_observe_command returns integer exit code"""
        from devforgeai_cli.commands.phase_commands import phase_observe_command

        # Should return 0 on success, 1 on error
        # Will fail until implementation exists
        result = phase_observe_command(
            story_id="STORY-188",
            phase="04",
            category="friction",
            note="Test observation",
            severity="medium",
            project_root="/nonexistent",  # Will fail, but should return int
            format="text"
        )

        assert isinstance(result, int), (
            f"phase_observe_command must return int exit code, got {type(result)}"
        )


class TestAC1_CLIRegistration:
    """AC-1: Command registered in cli.py argparse"""

    def test_phase_observe_subparser_exists(self):
        """Test: 'phase-observe' subparser registered in cli.py"""
        # Import the CLI module and verify phase-observe is a valid command
        from devforgeai_cli.cli import main
        import argparse

        # Parse with --help to check subcommands (won't execute, just parse)
        # If phase-observe doesn't exist, argparse will fail
        with pytest.raises(SystemExit) as exc_info:
            import sys
            old_argv = sys.argv
            sys.argv = ['devforgeai', 'phase-observe', '--help']
            try:
                main()
            finally:
                sys.argv = old_argv

        # Exit code 0 means help was displayed successfully (command exists)
        assert exc_info.value.code == 0, (
            "phase-observe command not registered in CLI"
        )


# =============================================================================
# AC-2: Observations Array Added to Phase State File
# =============================================================================


class TestAC2_ObservationsArrayInState:
    """AC-2: Observations array added to phase state file"""

    def test_add_observation_updates_state_file(self, temp_project_root, existing_phase_state):
        """Test: Adding observation modifies the phase state file"""
        from devforgeai_cli.commands.phase_commands import phase_observe_command

        result = phase_observe_command(
            story_id="STORY-188",
            phase="04",
            category="friction",
            note="Context switching overhead",
            severity="medium",
            project_root=str(temp_project_root),
            format="text"
        )

        assert result == 0, "phase_observe_command should return 0 on success"

        # Read back the state file and verify observations
        state = json.loads(existing_phase_state.read_text())
        assert "observations" in state, "State file must contain 'observations' key"
        assert len(state["observations"]) == 1, "Should have exactly 1 observation"

    def test_observations_is_array_type(self, temp_project_root, existing_phase_state):
        """Test: Observations field is a list/array type"""
        from devforgeai_cli.commands.phase_commands import phase_observe_command

        phase_observe_command(
            story_id="STORY-188",
            phase="04",
            category="success",
            note="TDD workflow worked well",
            severity="low",
            project_root=str(temp_project_root),
            format="text"
        )

        state = json.loads(existing_phase_state.read_text())
        assert isinstance(state.get("observations"), list), (
            f"observations must be a list, got {type(state.get('observations'))}"
        )

    def test_multiple_observations_append_to_array(self, temp_project_root, existing_phase_state):
        """Test: Multiple observations append to existing array"""
        from devforgeai_cli.commands.phase_commands import phase_observe_command

        # Add first observation
        phase_observe_command(
            story_id="STORY-188",
            phase="04",
            category="friction",
            note="First observation",
            severity="low",
            project_root=str(temp_project_root),
            format="text"
        )

        # Add second observation
        phase_observe_command(
            story_id="STORY-188",
            phase="04",
            category="success",
            note="Second observation",
            severity="high",
            project_root=str(temp_project_root),
            format="text"
        )

        state = json.loads(existing_phase_state.read_text())
        assert len(state["observations"]) == 2, (
            f"Should have 2 observations, got {len(state['observations'])}"
        )

    def test_observation_persists_across_reads(self, temp_project_root, existing_phase_state):
        """Test: Observations persist in file across multiple reads"""
        from devforgeai_cli.commands.phase_commands import phase_observe_command

        phase_observe_command(
            story_id="STORY-188",
            phase="04",
            category="pattern",
            note="Consistent TDD pattern observed",
            severity="low",
            project_root=str(temp_project_root),
            format="text"
        )

        # Read file multiple times
        state1 = json.loads(existing_phase_state.read_text())
        state2 = json.loads(existing_phase_state.read_text())

        assert state1["observations"] == state2["observations"], (
            "Observations should be identical across reads"
        )


# =============================================================================
# AC-3: Observation Structure
# =============================================================================


class TestAC3_ObservationStructure:
    """AC-3: Observation structure: id, phase, category, note, severity, timestamp"""

    def test_observation_has_id_field(self, temp_project_root, existing_phase_state):
        """Test: Each observation has an 'id' field"""
        from devforgeai_cli.commands.phase_commands import phase_observe_command

        phase_observe_command(
            story_id="STORY-188",
            phase="04",
            category="friction",
            note="Test observation",
            severity="medium",
            project_root=str(temp_project_root),
            format="text"
        )

        state = json.loads(existing_phase_state.read_text())
        observation = state["observations"][0]

        assert "id" in observation, "Observation must have 'id' field"
        assert observation["id"], "Observation id must not be empty"

    def test_observation_id_is_unique(self, temp_project_root, existing_phase_state):
        """Test: Each observation has a unique id"""
        from devforgeai_cli.commands.phase_commands import phase_observe_command

        # Add multiple observations
        for i in range(3):
            phase_observe_command(
                story_id="STORY-188",
                phase="04",
                category="friction",
                note=f"Observation {i}",
                severity="medium",
                project_root=str(temp_project_root),
                format="text"
            )

        state = json.loads(existing_phase_state.read_text())
        ids = [obs["id"] for obs in state["observations"]]

        assert len(ids) == len(set(ids)), (
            f"Observation IDs must be unique. Got: {ids}"
        )

    def test_observation_has_phase_field(self, temp_project_root, existing_phase_state):
        """Test: Each observation has a 'phase' field"""
        from devforgeai_cli.commands.phase_commands import phase_observe_command

        phase_observe_command(
            story_id="STORY-188",
            phase="04",
            category="friction",
            note="Test observation",
            severity="medium",
            project_root=str(temp_project_root),
            format="text"
        )

        state = json.loads(existing_phase_state.read_text())
        observation = state["observations"][0]

        assert "phase" in observation, "Observation must have 'phase' field"
        assert observation["phase"] == "04", (
            f"Expected phase '04', got '{observation['phase']}'"
        )

    def test_observation_has_category_field(self, temp_project_root, existing_phase_state):
        """Test: Each observation has a 'category' field"""
        from devforgeai_cli.commands.phase_commands import phase_observe_command

        phase_observe_command(
            story_id="STORY-188",
            phase="04",
            category="gap",
            note="Missing documentation",
            severity="high",
            project_root=str(temp_project_root),
            format="text"
        )

        state = json.loads(existing_phase_state.read_text())
        observation = state["observations"][0]

        assert "category" in observation, "Observation must have 'category' field"
        assert observation["category"] == "gap", (
            f"Expected category 'gap', got '{observation['category']}'"
        )

    def test_observation_has_note_field(self, temp_project_root, existing_phase_state):
        """Test: Each observation has a 'note' field"""
        from devforgeai_cli.commands.phase_commands import phase_observe_command

        expected_note = "This is the observation note content"

        phase_observe_command(
            story_id="STORY-188",
            phase="04",
            category="success",
            note=expected_note,
            severity="low",
            project_root=str(temp_project_root),
            format="text"
        )

        state = json.loads(existing_phase_state.read_text())
        observation = state["observations"][0]

        assert "note" in observation, "Observation must have 'note' field"
        assert observation["note"] == expected_note, (
            f"Expected note '{expected_note}', got '{observation['note']}'"
        )

    def test_observation_has_severity_field(self, temp_project_root, existing_phase_state):
        """Test: Each observation has a 'severity' field"""
        from devforgeai_cli.commands.phase_commands import phase_observe_command

        phase_observe_command(
            story_id="STORY-188",
            phase="04",
            category="friction",
            note="High severity issue",
            severity="high",
            project_root=str(temp_project_root),
            format="text"
        )

        state = json.loads(existing_phase_state.read_text())
        observation = state["observations"][0]

        assert "severity" in observation, "Observation must have 'severity' field"
        assert observation["severity"] == "high", (
            f"Expected severity 'high', got '{observation['severity']}'"
        )

    def test_observation_has_timestamp_field(self, temp_project_root, existing_phase_state):
        """Test: Each observation has a 'timestamp' field"""
        from devforgeai_cli.commands.phase_commands import phase_observe_command

        phase_observe_command(
            story_id="STORY-188",
            phase="04",
            category="pattern",
            note="Observed pattern",
            severity="medium",
            project_root=str(temp_project_root),
            format="text"
        )

        state = json.loads(existing_phase_state.read_text())
        observation = state["observations"][0]

        assert "timestamp" in observation, "Observation must have 'timestamp' field"
        assert observation["timestamp"], "Timestamp must not be empty"

    def test_observation_timestamp_is_iso8601(self, temp_project_root, existing_phase_state):
        """Test: Timestamp is in ISO-8601 format"""
        from devforgeai_cli.commands.phase_commands import phase_observe_command

        phase_observe_command(
            story_id="STORY-188",
            phase="04",
            category="friction",
            note="Test timestamp format",
            severity="low",
            project_root=str(temp_project_root),
            format="text"
        )

        state = json.loads(existing_phase_state.read_text())
        timestamp = state["observations"][0]["timestamp"]

        # Should be parseable as ISO-8601
        try:
            # Handle Z suffix (UTC indicator)
            if timestamp.endswith('Z'):
                timestamp = timestamp[:-1] + '+00:00'
            datetime.fromisoformat(timestamp)
        except ValueError:
            pytest.fail(f"Timestamp '{timestamp}' is not valid ISO-8601 format")


# =============================================================================
# AC-4: Categories Defined
# =============================================================================


class TestAC4_CategoriesDefined:
    """AC-4: Categories: friction, gap, success, pattern"""

    def test_category_friction_accepted(self, temp_project_root, existing_phase_state):
        """Test: Category 'friction' is valid"""
        from devforgeai_cli.commands.phase_commands import phase_observe_command

        result = phase_observe_command(
            story_id="STORY-188",
            phase="04",
            category="friction",
            note="Friction observation",
            severity="medium",
            project_root=str(temp_project_root),
            format="text"
        )

        assert result == 0, "Category 'friction' should be accepted"

    def test_category_gap_accepted(self, temp_project_root, existing_phase_state):
        """Test: Category 'gap' is valid"""
        from devforgeai_cli.commands.phase_commands import phase_observe_command

        result = phase_observe_command(
            story_id="STORY-188",
            phase="04",
            category="gap",
            note="Gap observation",
            severity="high",
            project_root=str(temp_project_root),
            format="text"
        )

        assert result == 0, "Category 'gap' should be accepted"

    def test_category_success_accepted(self, temp_project_root, existing_phase_state):
        """Test: Category 'success' is valid"""
        from devforgeai_cli.commands.phase_commands import phase_observe_command

        result = phase_observe_command(
            story_id="STORY-188",
            phase="04",
            category="success",
            note="Success observation",
            severity="low",
            project_root=str(temp_project_root),
            format="text"
        )

        assert result == 0, "Category 'success' should be accepted"

    def test_category_pattern_accepted(self, temp_project_root, existing_phase_state):
        """Test: Category 'pattern' is valid"""
        from devforgeai_cli.commands.phase_commands import phase_observe_command

        result = phase_observe_command(
            story_id="STORY-188",
            phase="04",
            category="pattern",
            note="Pattern observation",
            severity="medium",
            project_root=str(temp_project_root),
            format="text"
        )

        assert result == 0, "Category 'pattern' should be accepted"

    def test_invalid_category_rejected(self, temp_project_root, existing_phase_state):
        """Test: Invalid category is rejected with non-zero exit code"""
        from devforgeai_cli.commands.phase_commands import phase_observe_command

        result = phase_observe_command(
            story_id="STORY-188",
            phase="04",
            category="invalid_category",
            note="Should fail",
            severity="medium",
            project_root=str(temp_project_root),
            format="text"
        )

        assert result != 0, "Invalid category should return non-zero exit code"

    def test_all_valid_categories_constant_defined(self):
        """Test: VALID_CATEGORIES constant is defined in phase_commands or phase_state"""
        try:
            from devforgeai_cli.commands.phase_commands import VALID_CATEGORIES
        except ImportError:
            try:
                from installer.phase_state import VALID_CATEGORIES
            except ImportError:
                pytest.fail("VALID_CATEGORIES constant not defined in either module")

        expected = {"friction", "gap", "success", "pattern"}
        actual = set(VALID_CATEGORIES)

        assert actual == expected, (
            f"VALID_CATEGORIES should be {expected}, got {actual}"
        )


# =============================================================================
# AC-5: Severities Defined
# =============================================================================


class TestAC5_SeveritiesDefined:
    """AC-5: Severities: low, medium, high"""

    def test_severity_low_accepted(self, temp_project_root, existing_phase_state):
        """Test: Severity 'low' is valid"""
        from devforgeai_cli.commands.phase_commands import phase_observe_command

        result = phase_observe_command(
            story_id="STORY-188",
            phase="04",
            category="friction",
            note="Low severity observation",
            severity="low",
            project_root=str(temp_project_root),
            format="text"
        )

        assert result == 0, "Severity 'low' should be accepted"

    def test_severity_medium_accepted(self, temp_project_root, existing_phase_state):
        """Test: Severity 'medium' is valid"""
        from devforgeai_cli.commands.phase_commands import phase_observe_command

        result = phase_observe_command(
            story_id="STORY-188",
            phase="04",
            category="friction",
            note="Medium severity observation",
            severity="medium",
            project_root=str(temp_project_root),
            format="text"
        )

        assert result == 0, "Severity 'medium' should be accepted"

    def test_severity_high_accepted(self, temp_project_root, existing_phase_state):
        """Test: Severity 'high' is valid"""
        from devforgeai_cli.commands.phase_commands import phase_observe_command

        result = phase_observe_command(
            story_id="STORY-188",
            phase="04",
            category="friction",
            note="High severity observation",
            severity="high",
            project_root=str(temp_project_root),
            format="text"
        )

        assert result == 0, "Severity 'high' should be accepted"

    def test_invalid_severity_rejected(self, temp_project_root, existing_phase_state):
        """Test: Invalid severity is rejected with non-zero exit code"""
        from devforgeai_cli.commands.phase_commands import phase_observe_command

        result = phase_observe_command(
            story_id="STORY-188",
            phase="04",
            category="friction",
            note="Should fail",
            severity="critical",  # Invalid severity
            project_root=str(temp_project_root),
            format="text"
        )

        assert result != 0, "Invalid severity should return non-zero exit code"

    def test_severity_default_is_medium(self, temp_project_root, existing_phase_state):
        """Test: Default severity is 'medium' when not specified"""
        from devforgeai_cli.commands.phase_commands import phase_observe_command
        import inspect

        sig = inspect.signature(phase_observe_command)

        # Check if severity has a default value
        if "severity" in sig.parameters:
            default = sig.parameters["severity"].default
            # If default is not Parameter.empty, it should be 'medium'
            if default != inspect.Parameter.empty:
                assert default == "medium", (
                    f"Default severity should be 'medium', got '{default}'"
                )

    def test_all_valid_severities_constant_defined(self):
        """Test: VALID_SEVERITIES constant is defined"""
        try:
            from devforgeai_cli.commands.phase_commands import VALID_SEVERITIES
        except ImportError:
            try:
                from installer.phase_state import VALID_SEVERITIES
            except ImportError:
                pytest.fail("VALID_SEVERITIES constant not defined in either module")

        expected = {"low", "medium", "high"}
        actual = set(VALID_SEVERITIES)

        assert actual == expected, (
            f"VALID_SEVERITIES should be {expected}, got {actual}"
        )


# =============================================================================
# AC-6: phase-init Creates Empty Observations Array
# =============================================================================


class TestAC6_PhaseInitCreatesObservationsArray:
    """AC-6: phase-init creates empty observations array"""

    def test_phase_init_includes_observations_array(self, temp_project_root):
        """Test: phase-init creates state file with observations array"""
        from devforgeai_cli.commands.phase_commands import phase_init_command

        result = phase_init_command(
            story_id="STORY-200",
            project_root=str(temp_project_root),
            format="text"
        )

        assert result == 0, "phase_init should succeed"

        # Read the created state file
        state_path = temp_project_root / "devforgeai" / "workflows" / "STORY-200-phase-state.json"
        assert state_path.exists(), "State file should be created"

        state = json.loads(state_path.read_text())
        assert "observations" in state, "State must include 'observations' key"

    def test_phase_init_observations_is_empty_array(self, temp_project_root):
        """Test: phase-init creates empty observations array (not null)"""
        from devforgeai_cli.commands.phase_commands import phase_init_command

        phase_init_command(
            story_id="STORY-201",
            project_root=str(temp_project_root),
            format="text"
        )

        state_path = temp_project_root / "devforgeai" / "workflows" / "STORY-201-phase-state.json"
        state = json.loads(state_path.read_text())

        assert state["observations"] == [], (
            f"observations should be empty list, got {state['observations']}"
        )

    def test_phase_init_observations_is_list_type(self, temp_project_root):
        """Test: observations field is specifically a list (not dict, not None)"""
        from devforgeai_cli.commands.phase_commands import phase_init_command

        phase_init_command(
            story_id="STORY-202",
            project_root=str(temp_project_root),
            format="text"
        )

        state_path = temp_project_root / "devforgeai" / "workflows" / "STORY-202-phase-state.json"
        state = json.loads(state_path.read_text())

        assert isinstance(state["observations"], list), (
            f"observations must be list type, got {type(state['observations'])}"
        )


# =============================================================================
# PhaseState Class Integration
# =============================================================================


class TestPhaseStateIntegration:
    """Test PhaseState class integration with observations"""

    def test_phase_state_add_observation_method_exists(self):
        """Test: PhaseState class has add_observation method"""
        from installer.phase_state import PhaseState

        assert hasattr(PhaseState, 'add_observation'), (
            "PhaseState must have 'add_observation' method"
        )
        assert callable(getattr(PhaseState, 'add_observation')), (
            "add_observation must be callable"
        )

    def test_phase_state_add_observation_returns_observation_id(self, temp_project_root):
        """Test: add_observation returns the observation ID"""
        from installer.phase_state import PhaseState

        ps = PhaseState(project_root=temp_project_root)
        ps.create("STORY-203")

        result = ps.add_observation(
            story_id="STORY-203",
            phase_id="04",
            category="friction",
            note="Test note",
            severity="medium"
        )

        assert result is not None, "add_observation should return observation ID"
        assert isinstance(result, str), "Observation ID should be a string"

    def test_phase_state_validate_state_accepts_observations(self, temp_project_root):
        """Test: PhaseState.validate_state accepts state with observations"""
        from installer.phase_state import PhaseState

        ps = PhaseState(project_root=temp_project_root)

        state = {
            "story_id": "STORY-204",
            "workflow_started": "2026-01-07T12:00:00Z",
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
            "blocking_status": False,
            "observations": [
                {
                    "id": "obs-001",
                    "phase": "01",
                    "category": "friction",
                    "note": "Test observation",
                    "severity": "medium",
                    "timestamp": "2026-01-07T12:00:00Z"
                }
            ]
        }

        is_valid, error = ps.validate_state(state)
        assert is_valid, f"State with observations should be valid: {error}"

    def test_phase_state_create_initial_state_includes_observations(self, temp_project_root):
        """Test: _create_initial_state includes empty observations array"""
        from installer.phase_state import PhaseState

        ps = PhaseState(project_root=temp_project_root)
        state = ps._create_initial_state("STORY-205")

        assert "observations" in state, "Initial state must include 'observations'"
        assert state["observations"] == [], "Initial observations must be empty list"


# =============================================================================
# Error Handling
# =============================================================================


class TestErrorHandling:
    """Error handling tests"""

    def test_phase_observe_nonexistent_story_returns_error(self, temp_project_root):
        """Test: phase_observe for non-existent story returns error code"""
        from devforgeai_cli.commands.phase_commands import phase_observe_command

        result = phase_observe_command(
            story_id="STORY-999",  # Does not exist
            phase="04",
            category="friction",
            note="Should fail",
            severity="medium",
            project_root=str(temp_project_root),
            format="text"
        )

        assert result != 0, "Should return non-zero for non-existent story"

    def test_phase_observe_invalid_story_id_format_returns_error(self, temp_project_root):
        """Test: Invalid story ID format returns error"""
        from devforgeai_cli.commands.phase_commands import phase_observe_command

        result = phase_observe_command(
            story_id="INVALID-ID",  # Wrong format
            phase="04",
            category="friction",
            note="Should fail",
            severity="medium",
            project_root=str(temp_project_root),
            format="text"
        )

        assert result != 0, "Should return non-zero for invalid story ID"

    def test_phase_observe_invalid_phase_returns_error(self, temp_project_root, existing_phase_state):
        """Test: Invalid phase number returns error"""
        from devforgeai_cli.commands.phase_commands import phase_observe_command

        result = phase_observe_command(
            story_id="STORY-188",
            phase="99",  # Invalid phase
            category="friction",
            note="Should fail",
            severity="medium",
            project_root=str(temp_project_root),
            format="text"
        )

        assert result != 0, "Should return non-zero for invalid phase"

    def test_phase_observe_empty_note_returns_error(self, temp_project_root, existing_phase_state):
        """Test: Empty note returns error"""
        from devforgeai_cli.commands.phase_commands import phase_observe_command

        result = phase_observe_command(
            story_id="STORY-188",
            phase="04",
            category="friction",
            note="",  # Empty note
            severity="medium",
            project_root=str(temp_project_root),
            format="text"
        )

        assert result != 0, "Should return non-zero for empty note"


# =============================================================================
# JSON Output Format
# =============================================================================


class TestJSONOutput:
    """Test JSON output format"""

    def test_phase_observe_json_format_returns_valid_json(
        self, temp_project_root, existing_phase_state, capsys
    ):
        """Test: --format=json returns valid JSON"""
        from devforgeai_cli.commands.phase_commands import phase_observe_command

        phase_observe_command(
            story_id="STORY-188",
            phase="04",
            category="friction",
            note="Test observation",
            severity="medium",
            project_root=str(temp_project_root),
            format="json"
        )

        captured = capsys.readouterr()
        output = captured.out.strip()

        try:
            parsed = json.loads(output)
        except json.JSONDecodeError:
            pytest.fail(f"Output is not valid JSON: {output}")

        assert "success" in parsed, "JSON output should have 'success' field"

    def test_phase_observe_json_includes_observation_id(
        self, temp_project_root, existing_phase_state, capsys
    ):
        """Test: JSON output includes observation_id"""
        from devforgeai_cli.commands.phase_commands import phase_observe_command

        phase_observe_command(
            story_id="STORY-188",
            phase="04",
            category="friction",
            note="Test observation",
            severity="medium",
            project_root=str(temp_project_root),
            format="json"
        )

        captured = capsys.readouterr()
        parsed = json.loads(captured.out.strip())

        assert "observation_id" in parsed, "JSON output should include observation_id"


# =============================================================================
# Backward Compatibility
# =============================================================================


class TestBackwardCompatibility:
    """Test backward compatibility with existing state files"""

    def test_add_observation_to_legacy_state_without_observations(
        self, temp_project_root, state_without_observations
    ):
        """Test: Adding observation to state file without observations array works"""
        from devforgeai_cli.commands.phase_commands import phase_observe_command

        result = phase_observe_command(
            story_id="STORY-099",
            phase="01",
            category="friction",
            note="First observation on legacy state",
            severity="low",
            project_root=str(temp_project_root),
            format="text"
        )

        # Should auto-create observations array if missing
        assert result == 0, "Should succeed even without existing observations array"

        state = json.loads(state_without_observations.read_text())
        assert "observations" in state, "observations array should be created"
        assert len(state["observations"]) == 1, "Should have one observation"
