"""
Test: AC#2 - /coach-me Command Structure
Story: STORY-471
Generated: 2026-03-04

Validates: coach-me.md exists at src/claude/commands/coach-me.md
with valid YAML frontmatter, under 500 lines, invokes coaching-entrepreneur skill.
"""
import os
import re
import pytest

PROJECT_ROOT = "/mnt/c/Projects/DevForgeAI2"
TARGET_FILE = os.path.join(PROJECT_ROOT, "src/claude/commands/coach-me.md")


class TestCoachMeCommandExists:
    """AC#2: Command file must exist at correct path."""

    def test_should_exist_at_src_commands_path(self):
        # Arrange
        expected_path = TARGET_FILE

        # Act
        exists = os.path.isfile(expected_path)

        # Assert
        assert exists, f"coach-me.md not found at {expected_path}"


class TestCoachMeYAMLFrontmatter:
    """AC#2: Valid YAML frontmatter with required keys."""

    @pytest.fixture
    def file_content(self):
        with open(TARGET_FILE, "r") as f:
            return f.read()

    def test_should_have_yaml_frontmatter_delimiters(self, file_content):
        # Arrange
        pattern = r"^---\n.*?---"

        # Act
        match = re.search(pattern, file_content, re.DOTALL)

        # Assert
        assert match is not None, "Missing YAML frontmatter (--- delimiters)"

    def test_should_have_description_field(self, file_content):
        # Arrange
        pattern = r"^---\n.*?description:\s*.+.*?---"

        # Act
        match = re.search(pattern, file_content, re.DOTALL)

        # Assert
        assert match is not None, "Missing 'description' field in frontmatter"

    def test_should_have_argument_hint_field(self, file_content):
        # Arrange
        pattern = r"^---\n.*?argument-hint:\s*.+.*?---"

        # Act
        match = re.search(pattern, file_content, re.DOTALL)

        # Assert
        assert match is not None, "Missing 'argument-hint' field in frontmatter"


class TestCoachMeLineCount:
    """NFR-001: Command must be under 500 lines."""

    def test_should_be_under_500_lines(self):
        # Arrange
        max_lines = 500

        # Act
        with open(TARGET_FILE, "r") as f:
            line_count = sum(1 for _ in f)

        # Assert
        assert line_count < max_lines, f"coach-me.md is {line_count} lines (max {max_lines})"


class TestCoachMeSkillInvocation:
    """BR-003: /coach-me invokes coaching-entrepreneur skill via Skill() call."""

    @pytest.fixture
    def file_content(self):
        with open(TARGET_FILE, "r") as f:
            return f.read()

    def test_should_contain_skill_invocation(self, file_content):
        # Arrange
        pattern = r"Skill\(.*coaching-entrepreneur.*\)"

        # Act
        match = re.search(pattern, file_content)

        # Assert
        assert match is not None, "coach-me.md must contain Skill() call with 'coaching-entrepreneur'"

    def test_should_reference_coaching_entrepreneur_skill(self, file_content):
        # Arrange
        pattern = r"coaching-entrepreneur"

        # Act
        match = re.search(pattern, file_content)

        # Assert
        assert match is not None, "coach-me.md must reference coaching-entrepreneur skill"
