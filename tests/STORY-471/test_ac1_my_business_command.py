"""
Test: AC#1 - /my-business Command Structure
Story: STORY-471
Generated: 2026-03-04

Validates: my-business.md exists at src/claude/commands/my-business.md
with valid YAML frontmatter (description, argument-hint), under 500 lines,
and reads business artifacts.
"""
import os
import re
import pytest

PROJECT_ROOT = "/mnt/c/Projects/DevForgeAI2"
TARGET_FILE = os.path.join(PROJECT_ROOT, "src/claude/commands/my-business.md")


class TestMyBusinessCommandExists:
    """AC#1: Command file must exist at correct path."""

    def test_should_exist_at_src_commands_path(self):
        # Arrange
        expected_path = TARGET_FILE

        # Act
        exists = os.path.isfile(expected_path)

        # Assert
        assert exists, f"my-business.md not found at {expected_path}"


class TestMyBusinessYAMLFrontmatter:
    """AC#1: Valid YAML frontmatter with required keys."""

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


class TestMyBusinessLineCount:
    """NFR-001: Command must be under 500 lines."""

    def test_should_be_under_500_lines(self):
        # Arrange
        max_lines = 500

        # Act
        with open(TARGET_FILE, "r") as f:
            line_count = sum(1 for _ in f)

        # Assert
        assert line_count < max_lines, f"my-business.md is {line_count} lines (max {max_lines})"


class TestMyBusinessReadOnly:
    """BR-001: /my-business reads artifacts but NEVER writes."""

    @pytest.fixture
    def file_content(self):
        with open(TARGET_FILE, "r") as f:
            return f.read()

    def test_should_not_contain_write_calls(self, file_content):
        # Arrange
        forbidden_patterns = [r"Write\(", r"Edit\("]

        # Act & Assert
        for pattern in forbidden_patterns:
            match = re.search(pattern, file_content)
            assert match is None, f"Found forbidden write pattern: {pattern}"

    def test_should_contain_read_calls(self, file_content):
        # Arrange
        pattern = r"Read\("

        # Act
        match = re.search(pattern, file_content)

        # Assert
        assert match is not None, "my-business.md should contain Read() calls for artifact reading"


class TestMyBusinessReadsBusinessArtifacts:
    """AC#1: Command reads business artifacts from devforgeai/specs/business/."""

    @pytest.fixture
    def file_content(self):
        with open(TARGET_FILE, "r") as f:
            return f.read()

    def test_should_reference_business_artifacts_path(self, file_content):
        # Arrange
        pattern = r"devforgeai/specs/business/"

        # Act
        match = re.search(pattern, file_content)

        # Assert
        assert match is not None, "Should reference devforgeai/specs/business/ artifact path"
