"""
Test: AC#3 - skill-output-schemas.yaml Epic Schema Relocated
Story: STORY-439
Phase: RED (TDD - tests expected to FAIL)
Pattern: AAA (Arrange, Act, Assert)
"""
import os
import pytest

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
ARCH_SCHEMA = os.path.join(
    PROJECT_ROOT, "src", "claude", "skills",
    "devforgeai-architecture", "references", "skill-output-schemas.yaml"
)
ORCH_SCHEMA = os.path.join(
    PROJECT_ROOT, "src", "claude", "skills",
    "devforgeai-orchestration", "references", "skill-output-schemas.yaml"
)


class TestArchitectureSchemaExists:
    """SCH-003: Architecture skill has schema file."""

    def test_should_have_schema_file_in_architecture_skill_when_created(self):
        # Arrange / Act
        exists = os.path.isfile(ARCH_SCHEMA)
        # Assert
        assert exists, (
            f"Architecture skill must have skill-output-schemas.yaml at {ARCH_SCHEMA}"
        )


class TestEpicSchemaInArchitecture:
    """SCH-001: Epic schema exists in architecture skill schema file."""

    def test_should_contain_epic_schema_section_when_relocated(self):
        # Arrange
        with open(ARCH_SCHEMA, "r", encoding="utf-8") as f:
            content = f.read()
        # Act
        has_epic = "epic" in content.lower()
        # Assert
        assert has_epic, (
            "Architecture schema file must contain epic schema section"
        )


class TestOrchestrationRetainsNonEpic:
    """SCH-002: Orchestration retains non-epic schemas (brainstorm, ideation)."""

    def test_should_retain_brainstorm_schema_in_orchestration_when_epic_removed(self):
        # Arrange
        with open(ORCH_SCHEMA, "r", encoding="utf-8") as f:
            content = f.read()
        # Act
        has_brainstorm = "brainstorm:" in content.lower()
        # Assert
        assert has_brainstorm, (
            "Orchestration schema must retain brainstorm schema section"
        )

    def test_should_retain_ideation_schema_in_orchestration_when_epic_removed(self):
        # Arrange
        with open(ORCH_SCHEMA, "r", encoding="utf-8") as f:
            content = f.read()
        # Act
        has_ideation = "ideation:" in content.lower()
        # Assert
        assert has_ideation, (
            "Orchestration schema must retain ideation schema section"
        )
