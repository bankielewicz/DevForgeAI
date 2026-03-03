"""
Test: AC#1 - /create-epic Command Routes to Architecture Skill
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
    """Load create-epic.md content from src/ tree."""
    with open(CREATE_EPIC_SRC, "r", encoding="utf-8") as f:
        return f.read()


class TestCreateEpicSkillInvocation:
    """CMD-001: Skill invocation changed to devforgeai-architecture."""

    def test_should_contain_architecture_skill_invocation_when_routing_updated(self, create_epic_content):
        # Arrange
        expected_pattern = 'devforgeai-architecture'
        # Act
        has_architecture = expected_pattern in create_epic_content
        # Assert
        assert has_architecture, (
            "create-epic.md must contain 'devforgeai-architecture' in Skill() call"
        )

    def test_should_not_contain_orchestration_skill_invocation_when_routing_updated(self, create_epic_content):
        # Arrange
        forbidden_pattern = 'Skill(command="devforgeai-orchestration")'
        # Act
        has_orchestration = forbidden_pattern in create_epic_content
        # Assert
        assert not has_orchestration, (
            "create-epic.md must NOT contain 'Skill(command=\"devforgeai-orchestration\")'"
        )


class TestCreateEpicModeMarker:
    """CMD-002: Mode context marker for epic-creation."""

    def test_should_contain_epic_creation_mode_marker_when_routing_updated(self, create_epic_content):
        # Arrange
        expected_marker = "**Mode:** epic-creation"
        # Act
        has_marker = expected_marker in create_epic_content
        # Assert
        assert has_marker, (
            "create-epic.md must contain '**Mode:** epic-creation' context marker"
        )


class TestCreateEpicPhaseReferences:
    """CMD-003/CMD-004: Phase and reference path updates."""

    def test_should_not_reference_orchestration_phase_4a_when_updated(self, create_epic_content):
        # Arrange
        forbidden = "Phase 4A"
        # Act
        has_phase4a = forbidden in create_epic_content
        # Assert
        assert not has_phase4a, (
            "create-epic.md must NOT reference 'Phase 4A' (removed from orchestration)"
        )

    def test_should_reference_architecture_skill_path_when_updated(self, create_epic_content):
        # Arrange
        expected = "devforgeai-architecture"
        # Act
        lines_with_skill_ref = [
            line for line in create_epic_content.splitlines()
            if "skill" in line.lower() and "reference" in line.lower()
        ]
        has_arch_ref = any(expected in line for line in lines_with_skill_ref)
        # Assert - at least one skill reference line points to architecture
        assert has_arch_ref, (
            "create-epic.md skill reference paths must point to devforgeai-architecture"
        )


class TestCreateEpicSchemaPath:
    """CMD-005: Schema validation path updated."""

    def test_should_reference_architecture_schema_path_when_updated(self, create_epic_content):
        # Arrange
        expected_path = "devforgeai-architecture/references/skill-output-schemas.yaml"
        # Act
        has_schema_path = expected_path in create_epic_content
        # Assert
        assert has_schema_path, (
            "create-epic.md must reference architecture skill schema path"
        )
