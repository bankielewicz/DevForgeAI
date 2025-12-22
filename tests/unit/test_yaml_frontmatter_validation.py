"""
Unit tests for YAML frontmatter validation.

Tests validate:
1. All 3 stories have valid YAML syntax
2. YAML frontmatter contains required fields
3. YAML parsing succeeds without syntax errors
"""

import pytest
from pathlib import Path
import yaml
import sys
from pathlib import Path as PathlibPath

# Import helpers from conftest (parent directory)
sys.path.insert(0, str(PathlibPath(__file__).parent.parent))
from conftest import extract_yaml_frontmatter


# Story IDs and files for parametrized tests
STORY_FILES = [
    ("STORY-027", Path("devforgeai/specs/Stories/STORY-027-wire-hooks-into-create-story-command.story.md")),
    ("STORY-028", Path("devforgeai/specs/Stories/STORY-028-wire-hooks-into-create-epic-command.story.md")),
    ("STORY-029", Path("devforgeai/specs/Stories/STORY-029-wire-hooks-into-create-sprint-command.story.md")),
]

# Required YAML fields
REQUIRED_FIELDS = [
    "id",
    "title",
    "epic",
    "sprint",
    "status",
    "points",
    "priority",
    "assigned_to",
    "created",
    "format_version",
]

# Fields that must have non-null values
NON_NULL_FIELDS = ["id", "title", "status", "format_version"]


class TestYAML_FrontmatterValidation:
    """
    Test suite for YAML frontmatter integrity in story files.

    Validates YAML syntax, required fields, and field value constraints.
    """

    @pytest.mark.parametrize("story_id,story_file", STORY_FILES)
    def test_yaml_valid_syntax(self, story_id, story_file):
        """
        Test: YAML frontmatter has valid syntax and parses successfully.

        Validates that:
        - YAML can be extracted from story
        - YAML parses without syntax errors
        - Parsed content is a dictionary
        """
        if not story_file.exists():
            pytest.skip(f"{story_id}: Story file not found: {story_file.name}")

        content = story_file.read_text(encoding="utf-8")

        # Act: Extract and parse YAML
        yaml_text = extract_yaml_frontmatter(content)

        # Assert: YAML parses without errors
        try:
            parsed = yaml.safe_load(yaml_text)
            assert isinstance(parsed, dict), f"{story_id}: YAML did not parse to dictionary"
        except yaml.YAMLError as e:
            pytest.fail(f"{story_id}: YAML syntax error: {e}")

    @pytest.mark.parametrize("story_id,story_file", STORY_FILES)
    def test_required_fields_present(self, story_id, story_file):
        """
        Test: YAML contains all required fields with proper values.

        Validates that:
        - All required fields present in YAML
        - Non-null fields have actual values (not null/None)
        - Other fields can be null if needed
        """
        if not story_file.exists():
            pytest.skip(f"{story_id}: Story file not found: {story_file.name}")

        content = story_file.read_text(encoding="utf-8")
        yaml_text = extract_yaml_frontmatter(content)
        parsed = yaml.safe_load(yaml_text)

        # Act & Assert
        for field in REQUIRED_FIELDS:
            assert (
                field in parsed
            ), f"{story_id}: YAML missing required field: {field}"

            # Only enforce non-null for critical fields
            if field in NON_NULL_FIELDS:
                assert (
                    parsed[field] is not None
                ), f"{story_id}: YAML field '{field}' cannot be null"
