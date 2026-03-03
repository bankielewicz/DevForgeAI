"""
Test: AC#4 - Error Handling References Updated
Story: STORY-439
Phase: RED (TDD - tests expected to FAIL)
Pattern: AAA (Arrange, Act, Assert)
"""
import os
import pytest

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
CREATE_EPIC_SRC = os.path.join(PROJECT_ROOT, "src", "claude", "commands", "create-epic.md")


@pytest.fixture
def create_epic_content():
    with open(CREATE_EPIC_SRC, "r", encoding="utf-8") as f:
        return f.read()


class TestErrorHandlingArchitectureRef:
    """ERROR-001(a): Error handling references architecture skill."""

    def test_should_reference_architecture_in_error_handling_when_updated(self, create_epic_content):
        # Arrange
        error_lines = [
            line for line in create_epic_content.splitlines()
            if "error" in line.lower() or "fail" in line.lower() or "recovery" in line.lower()
        ]
        # Act
        has_arch_ref = any("architecture" in line.lower() for line in error_lines)
        # Assert
        assert has_arch_ref, (
            "Error handling lines must reference architecture skill"
        )


class TestNoPhase4AReferences:
    """ERROR-001(b): No Phase 4A error references."""

    def test_should_not_reference_phase_4a_in_error_handling_when_updated(self, create_epic_content):
        # Arrange / Act
        has_phase4a = "Phase 4A" in create_epic_content
        # Assert
        assert not has_phase4a, (
            "create-epic.md must NOT reference Phase 4A (no longer exists)"
        )


class TestSchemaFailureMessages:
    """ERROR-001(c): Schema validation failure messages reference architecture."""

    def test_should_reference_architecture_in_schema_validation_errors_when_updated(self, create_epic_content):
        # Arrange
        schema_lines = [
            line for line in create_epic_content.splitlines()
            if "schema" in line.lower() and ("valid" in line.lower() or "fail" in line.lower())
        ]
        # Act
        has_arch = any("architecture" in line.lower() for line in schema_lines)
        # Assert
        assert has_arch or len(schema_lines) == 0, (
            "Schema validation failure messages must reference architecture skill"
        )


class TestRecoveryInstructions:
    """ERROR-001(d): Recovery instructions point to architecture docs."""

    def test_should_not_reference_orchestration_in_recovery_when_updated(self, create_epic_content):
        # Arrange
        recovery_lines = [
            line for line in create_epic_content.splitlines()
            if "recovery" in line.lower() or "troubleshoot" in line.lower()
        ]
        # Act
        has_orch = any("orchestration" in line.lower() for line in recovery_lines)
        # Assert
        assert not has_orch, (
            "Recovery instructions must NOT reference orchestration skill"
        )
