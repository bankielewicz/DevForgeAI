"""
Test: AC#5 - artifact-generation.md Epic Code Path Removed
Story: STORY-438
Generated: 2026-02-18
TDD Phase: RED (tests should FAIL against current source)
"""
import os
import re
import pytest

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
ARTIFACT_MD = os.path.join(
    PROJECT_ROOT, "src", "claude", "skills", "devforgeai-ideation",
    "references", "artifact-generation.md",
)


@pytest.fixture
def artifact_content():
    assert os.path.exists(ARTIFACT_MD), f"artifact-generation.md not found at {ARTIFACT_MD}"
    with open(ARTIFACT_MD, "r", encoding="utf-8") as f:
        return f.read()


class TestAC5ArtifactGeneration:
    """Verify epic code path removed from artifact-generation.md."""

    def test_ac5_no_epic_template_loading(self, artifact_content):
        """AC5(a): No epic template loading instructions remain."""
        assert "epic-template" not in artifact_content.lower(), (
            "artifact-generation.md still references epic template loading"
        )
        assert "load constitutional epic template" not in artifact_content.lower(), (
            "artifact-generation.md still has 'Load Constitutional Epic Template' section"
        )

    def test_ac5_no_section_compliance_checklist(self, artifact_content):
        """AC5(b): No 'Section Compliance Checklist' for epic sections."""
        assert "section compliance checklist" not in artifact_content.lower(), (
            "artifact-generation.md still has Section Compliance Checklist"
        )

    def test_ac5_requirements_generation_retained(self, artifact_content):
        """AC5(c): Requirements specification generation is retained."""
        assert "requirements" in artifact_content.lower(), (
            "artifact-generation.md lost requirements generation content"
        )

    def test_ac5_output_format_yaml_requirements(self, artifact_content):
        """AC5(d): Output format changed to YAML requirements.md per F4 schema."""
        assert "requirements.md" in artifact_content, (
            "artifact-generation.md does not reference requirements.md output"
        )
        assert re.search(r"yaml|YAML", artifact_content), (
            "artifact-generation.md does not mention YAML format"
        )

    def test_ac5_no_epic_cross_session_context(self, artifact_content):
        """AC5(e): Cross-session context updated (no epic decomposition, feasibility refs)."""
        content_lower = artifact_content.lower()
        assert "epic decomposition" not in content_lower, (
            "artifact-generation.md still references epic decomposition in cross-session context"
        )
        assert "feasibility assessment" not in content_lower or \
               "feasibility analysis" not in content_lower, (
            "artifact-generation.md still references feasibility in cross-session context"
        )
