"""
Test: AC#1 - Coaching Skill File Structure
Story: STORY-467 - Dynamic Persona Blend Engine
Generated: 2026-03-04

Validates:
- SKILL.md exists at src/claude/skills/coaching-entrepreneur/SKILL.md
- Valid YAML frontmatter with name: coaching-entrepreneur
- Description contains "Use when" trigger phrase
- Under 1000 lines
- Contains persona blend instructions as core workflow
"""
import os
import re

import pytest

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SKILL_PATH = os.path.join(PROJECT_ROOT, "src", "claude", "skills", "coaching-entrepreneur", "SKILL.md")


@pytest.fixture
def skill_content():
    """Read the SKILL.md file content."""
    assert os.path.isfile(SKILL_PATH), f"SKILL.md not found at {SKILL_PATH}"
    with open(SKILL_PATH, "r", encoding="utf-8") as f:
        return f.read()


@pytest.fixture
def skill_lines(skill_content):
    """Return SKILL.md as list of lines."""
    return skill_content.splitlines()


@pytest.fixture
def frontmatter(skill_content):
    """Extract YAML frontmatter from SKILL.md."""
    match = re.match(r"^---\s*\n(.*?)\n---", skill_content, re.DOTALL)
    assert match is not None, "SKILL.md must have YAML frontmatter delimited by ---"
    return match.group(1)


class TestSkillFileExists:
    """Verify SKILL.md exists at the correct path."""

    def test_skill_file_exists(self):
        assert os.path.isfile(SKILL_PATH), (
            f"SKILL.md must exist at {SKILL_PATH}"
        )


class TestYamlFrontmatter:
    """Verify SKILL.md has valid YAML frontmatter."""

    def test_has_frontmatter_delimiters(self, skill_content):
        """SKILL.md must start with --- and have closing ---."""
        assert skill_content.startswith("---"), "SKILL.md must start with YAML frontmatter delimiter ---"
        # Find second ---
        second_delim = skill_content.find("---", 3)
        assert second_delim > 3, "SKILL.md must have closing YAML frontmatter delimiter ---"

    def test_frontmatter_contains_name(self, frontmatter):
        """Frontmatter must contain name: coaching-entrepreneur."""
        assert re.search(r"^name:\s*coaching-entrepreneur\s*$", frontmatter, re.MULTILINE), (
            "Frontmatter must contain 'name: coaching-entrepreneur'"
        )

    def test_frontmatter_contains_description(self, frontmatter):
        """Frontmatter must contain a description field."""
        assert re.search(r"^description:", frontmatter, re.MULTILINE), (
            "Frontmatter must contain a 'description:' field"
        )

    def test_description_contains_use_when_trigger(self, frontmatter):
        """Description must contain 'Use when' trigger phrase."""
        desc_match = re.search(r"^description:\s*(.+)$", frontmatter, re.MULTILINE)
        assert desc_match is not None, "Frontmatter must have description field"
        description = desc_match.group(1).strip().strip('"').strip("'")
        assert "Use when" in description, (
            f"Description must contain 'Use when' trigger phrase, got: '{description}'"
        )


class TestLineCount:
    """Verify SKILL.md is under 1000 lines."""

    def test_under_1000_lines(self, skill_lines):
        line_count = len(skill_lines)
        assert line_count < 1000, (
            f"SKILL.md must be under 1000 lines, found {line_count}"
        )


class TestPersonaBlendInstructions:
    """Verify SKILL.md contains persona blend instructions as core workflow."""

    def test_contains_persona_blend_section(self, skill_content):
        """SKILL.md must contain persona blend as a documented section."""
        assert re.search(r"(?i)persona\s+blend", skill_content), (
            "SKILL.md must contain 'persona blend' instructions"
        )

    def test_persona_blend_in_workflow(self, skill_content):
        """Persona blend must be part of the core workflow, not just mentioned."""
        # Look for persona blend under a workflow or phase heading
        has_workflow = re.search(r"(?i)##\s+.*workflow", skill_content)
        has_persona_blend = re.search(r"(?i)persona\s+blend", skill_content)
        assert has_workflow and has_persona_blend, (
            "SKILL.md must have a Workflow section containing persona blend instructions"
        )
