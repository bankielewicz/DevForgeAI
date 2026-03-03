"""Test AC#1: Assessment Skill File Structure.

Story: STORY-465
Validates that SKILL.md exists at the correct path with valid YAML
frontmatter containing name and description fields.
"""
import pytest
from pathlib import Path
from conftest import parse_yaml_frontmatter


class TestSkillFileExists:
    """Tests for SKILL.md file existence and location."""

    def test_should_exist_at_correct_path(self, skill_file):
        """SKILL.md must exist at src/claude/skills/assessing-entrepreneur/SKILL.md."""
        assert skill_file.exists(), (
            f"SKILL.md not found at {skill_file}. "
            "The assessing-entrepreneur skill file must be created."
        )

    def test_should_be_a_file_not_directory(self, skill_file):
        """SKILL.md must be a regular file, not a directory."""
        assert skill_file.is_file(), f"{skill_file} exists but is not a regular file."


class TestSkillFrontmatter:
    """Tests for YAML frontmatter validity."""

    def test_should_have_yaml_frontmatter(self, skill_file):
        """SKILL.md must start with valid YAML frontmatter delimited by ---."""
        content = skill_file.read_text(encoding="utf-8")
        assert content.startswith("---"), (
            "SKILL.md must begin with YAML frontmatter (--- delimiter)."
        )
        assert "---" in content[3:], (
            "SKILL.md frontmatter must have closing --- delimiter."
        )

    def test_should_have_name_field(self, skill_file):
        """Frontmatter must contain a 'name' field."""
        fm = parse_yaml_frontmatter(skill_file)
        assert "name" in fm, "YAML frontmatter missing required 'name' field."

    def test_should_have_name_equal_to_assessing_entrepreneur(self, skill_file):
        """The name field must equal 'assessing-entrepreneur'."""
        fm = parse_yaml_frontmatter(skill_file)
        assert fm["name"] == "assessing-entrepreneur", (
            f"Expected name 'assessing-entrepreneur', got '{fm.get('name')}'."
        )

    def test_should_have_description_field(self, skill_file):
        """Frontmatter must contain a 'description' field."""
        fm = parse_yaml_frontmatter(skill_file)
        assert "description" in fm, "YAML frontmatter missing required 'description' field."

    def test_should_have_use_when_trigger_in_description(self, skill_file):
        """Description must contain 'Use when' trigger phrase."""
        fm = parse_yaml_frontmatter(skill_file)
        description = str(fm.get("description", ""))
        assert "Use when" in description, (
            f"Description must contain 'Use when' trigger phrase. "
            f"Got: '{description[:100]}...'"
        )


class TestSkillFileSize:
    """Tests for SKILL.md size constraints."""

    def test_should_be_under_1000_lines(self, skill_file):
        """SKILL.md must be under 1000 lines for token budget compliance."""
        content = skill_file.read_text(encoding="utf-8")
        line_count = len(content.splitlines())
        assert line_count < 1000, (
            f"SKILL.md has {line_count} lines, exceeds 1000 line limit."
        )

    def test_should_be_non_empty(self, skill_file):
        """SKILL.md must contain substantive content."""
        content = skill_file.read_text(encoding="utf-8")
        # At minimum: frontmatter + heading + some content
        assert len(content.strip()) > 50, (
            "SKILL.md appears empty or contains only minimal content."
        )
