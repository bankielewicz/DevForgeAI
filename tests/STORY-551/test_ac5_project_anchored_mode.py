"""
Test: AC#5 - Project-Anchored Mode Scopes Projections to Active Project
Story: STORY-551
Generated: 2026-03-05

Verifies SKILL.md has project-anchored mode, standalone mode as alternative,
and project name labeling in outputs.
"""

import re


class TestProjectAnchoredMode:
    """Verify SKILL.md documents project-anchored mode."""

    def test_should_have_project_anchored_mode_section(self, skill_content):
        """SKILL.md must document project-anchored mode."""
        assert re.search(
            r'(?i)project.anchored\s+mode',
            skill_content
        ), (
            "SKILL.md missing project-anchored mode section. "
            "AC#5: Must operate in project-anchored mode when project context exists."
        )

    def test_should_scope_projections_to_active_project(self, skill_content):
        """Project-anchored mode must scope projections to active project."""
        assert re.search(
            r'(?i)(scope|scoping).*project',
            skill_content
        ), (
            "SKILL.md does not describe scoping projections to active project."
        )

    def test_should_detect_active_project_context(self, skill_content):
        """SKILL.md must describe detecting active project context."""
        assert re.search(
            r'(?i)(detect|check|identify).*(?:active\s+project|project\s+context)',
            skill_content
        ), (
            "SKILL.md does not describe detecting active project context."
        )


class TestStandaloneMode:
    """Verify SKILL.md documents standalone mode as alternative."""

    def test_should_have_standalone_mode(self, skill_content):
        """SKILL.md must document standalone mode."""
        assert re.search(
            r'(?i)standalone\s+mode',
            skill_content
        ), (
            "SKILL.md missing standalone mode documentation. "
            "AC#5: Standalone mode must be available as alternative."
        )

    def test_should_produce_generic_projections_in_standalone(self, skill_content):
        """Standalone mode should produce generic (non-project-scoped) projections."""
        assert re.search(
            r'(?i)standalone.*(?:generic|general|unscoped)',
            skill_content,
            re.DOTALL
        ), (
            "SKILL.md does not describe generic projections in standalone mode."
        )


class TestProjectNameLabeling:
    """Verify outputs are labeled with project name."""

    def test_should_label_outputs_with_project_name(self, skill_content):
        """Project-anchored outputs must be labeled with project name."""
        assert re.search(
            r'(?i)(label|tag|title).*project\s+name',
            skill_content
        ), (
            "SKILL.md does not describe labeling outputs with project name. "
            "AC#5: Outputs must be labeled with the project name."
        )


class TestEdgeCaseEC003StandaloneFlag:
    """EC-003: --standalone flag overrides auto-detected project context."""

    def test_should_document_standalone_flag(self, skill_content):
        """SKILL.md must document --standalone flag behavior."""
        assert re.search(
            r'(?i)(--standalone|standalone\s+flag)',
            skill_content
        ), (
            "EC-003: SKILL.md does not document --standalone flag."
        )

    def test_should_give_flag_precedence_over_project_context(self, skill_content):
        """Explicit --standalone flag must take precedence over project context."""
        assert re.search(
            r'(?i)(--standalone|standalone\s+flag).*(?:precedence|override|overrides|takes\s+priority)',
            skill_content,
            re.DOTALL
        ), (
            "EC-003: --standalone flag must take precedence over "
            "auto-detected project context."
        )


class TestSkillLineCount:
    """NFR-005: SKILL.md must remain under 1,000 lines."""

    def test_should_have_fewer_than_1000_lines(self, skill_lines):
        """SKILL.md must be under 1,000 lines per NFR-005."""
        line_count = len(skill_lines)
        assert line_count < 1000, (
            f"SKILL.md has {line_count} lines (limit: 1,000). "
            "NFR-005: managing-finances SKILL.md must remain under 1,000 lines."
        )
