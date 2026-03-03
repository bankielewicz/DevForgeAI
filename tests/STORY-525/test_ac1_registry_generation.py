"""
Test: AC#1 - Registry JSON Created from 12 Phase Pre-Exit Checklists
Story: STORY-525
Generated: 2026-03-02

Tests validate the registry JSON file structure, schema, and content.
These tests FAIL initially because the registry file does not exist yet.
"""

import json
import re
import sys
from pathlib import Path

import pytest

# Registry location in src/ tree for testing
REGISTRY_PATH = Path(__file__).resolve().parents[2] / "src" / "claude" / "hooks" / "phase-steps-registry.json"

EXPECTED_PHASE_KEYS = ["01", "02", "03", "04", "4.5", "05", "5.5", "06", "07", "08", "09", "10"]
EXPECTED_TOTAL_STEPS = 72
STEP_ID_PATTERN = re.compile(r"^\d+\.?\d*\.\d+$")


class TestRegistryFileExists:
    """Registry JSON file must exist at expected path."""

    def test_registry_file_exists_at_expected_path(self):
        """Arrange: Expected path defined. Act: Check existence. Assert: File exists."""
        assert REGISTRY_PATH.exists(), (
            f"Registry file not found at {REGISTRY_PATH}. "
            "AC#1 requires .claude/hooks/phase-steps-registry.json"
        )


class TestRegistryJsonValid:
    """Registry must be valid JSON parseable by json.loads()."""

    def test_registry_valid_json_loads(self):
        """Arrange: Read registry file. Act: Parse with json.loads(). Assert: No exception."""
        content = REGISTRY_PATH.read_text()
        registry = json.loads(content)
        assert isinstance(registry, dict)

    def test_registry_valid_json_tool(self):
        """Arrange: Read registry. Act: Validate structure. Assert: Top-level is dict of phases."""
        content = REGISTRY_PATH.read_text()
        registry = json.loads(content)
        assert len(registry) > 0, "Registry must not be empty"


class TestRegistryPhaseKeys:
    """Registry must contain exactly 12 phase keys."""

    def test_registry_has_12_phase_keys(self):
        """Arrange: Load registry. Act: Count keys. Assert: 12 phases."""
        content = REGISTRY_PATH.read_text()
        registry = json.loads(content)
        assert len(registry) == 12, f"Expected 12 phase keys, got {len(registry)}"

    def test_registry_has_all_expected_phase_keys(self):
        """Arrange: Load registry. Act: Check keys. Assert: All 12 phase IDs present."""
        content = REGISTRY_PATH.read_text()
        registry = json.loads(content)
        for phase_key in EXPECTED_PHASE_KEYS:
            assert phase_key in registry, f"Missing phase key: {phase_key}"


class TestRegistryStepCount:
    """Registry must contain 72 total steps across all phases."""

    def test_registry_has_72_total_steps(self):
        """Arrange: Load registry. Act: Sum step counts. Assert: 72 total."""
        content = REGISTRY_PATH.read_text()
        registry = json.loads(content)
        total = sum(len(phase["steps"]) for phase in registry.values())
        assert total == EXPECTED_TOTAL_STEPS, f"Expected {EXPECTED_TOTAL_STEPS} steps, got {total}"


class TestRegistryStepSchema:
    """Each step must have required fields with correct types."""

    def test_step_has_id_field(self):
        """Arrange: Load registry. Act: Check each step. Assert: id field present."""
        content = REGISTRY_PATH.read_text()
        registry = json.loads(content)
        for phase_key, phase_data in registry.items():
            for step in phase_data["steps"]:
                assert "id" in step, f"Step missing 'id' in phase {phase_key}"

    def test_step_id_matches_dotted_format(self):
        """Arrange: Load registry. Act: Validate step IDs. Assert: NN.M format."""
        content = REGISTRY_PATH.read_text()
        registry = json.loads(content)
        for phase_key, phase_data in registry.items():
            for step in phase_data["steps"]:
                assert STEP_ID_PATTERN.match(step["id"]), (
                    f"Step ID '{step['id']}' in phase {phase_key} does not match NN.M format"
                )

    def test_step_has_check_field_nonempty(self):
        """Arrange: Load registry. Act: Check each step. Assert: check is non-empty string."""
        content = REGISTRY_PATH.read_text()
        registry = json.loads(content)
        for phase_key, phase_data in registry.items():
            for step in phase_data["steps"]:
                assert "check" in step, f"Step missing 'check' in phase {phase_key}"
                assert isinstance(step["check"], str) and len(step["check"]) > 0

    def test_step_subagent_is_string_array_or_null(self):
        """Arrange: Load registry. Act: Check subagent types. Assert: string|array|null."""
        content = REGISTRY_PATH.read_text()
        registry = json.loads(content)
        for phase_key, phase_data in registry.items():
            for step in phase_data["steps"]:
                assert "subagent" in step, f"Step missing 'subagent' in phase {phase_key}"
                val = step["subagent"]
                assert val is None or isinstance(val, str) or isinstance(val, list), (
                    f"subagent must be string, array, or null. Got {type(val)} in phase {phase_key}"
                )

    def test_step_conditional_is_boolean(self):
        """Arrange: Load registry. Act: Check conditional field. Assert: boolean type."""
        content = REGISTRY_PATH.read_text()
        registry = json.loads(content)
        for phase_key, phase_data in registry.items():
            for step in phase_data["steps"]:
                conditional = step.get("conditional", False)
                assert isinstance(conditional, bool), (
                    f"conditional must be boolean in phase {phase_key}, step {step.get('id')}"
                )


class TestRegistryPhaseMetadata:
    """Each phase must have name, entry_gate, exit_gate, and steps array."""

    def test_phase_has_name(self):
        """Arrange: Load registry. Act: Check each phase. Assert: name is non-empty string."""
        content = REGISTRY_PATH.read_text()
        registry = json.loads(content)
        for phase_key, phase_data in registry.items():
            assert "name" in phase_data, f"Phase {phase_key} missing 'name'"
            assert isinstance(phase_data["name"], str) and len(phase_data["name"]) > 0

    def test_phase_has_entry_gate(self):
        """Arrange: Load registry. Act: Check each phase. Assert: entry_gate present."""
        content = REGISTRY_PATH.read_text()
        registry = json.loads(content)
        for phase_key, phase_data in registry.items():
            assert "entry_gate" in phase_data, f"Phase {phase_key} missing 'entry_gate'"

    def test_phase_has_exit_gate(self):
        """Arrange: Load registry. Act: Check each phase. Assert: exit_gate present."""
        content = REGISTRY_PATH.read_text()
        registry = json.loads(content)
        for phase_key, phase_data in registry.items():
            assert "exit_gate" in phase_data, f"Phase {phase_key} missing 'exit_gate'"

    def test_phase_has_steps_array(self):
        """Arrange: Load registry. Act: Check each phase. Assert: steps is a list."""
        content = REGISTRY_PATH.read_text()
        registry = json.loads(content)
        for phase_key, phase_data in registry.items():
            assert "steps" in phase_data, f"Phase {phase_key} missing 'steps'"
            assert isinstance(phase_data["steps"], list)
