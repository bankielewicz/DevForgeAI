"""
Test: AC#3 - Output File Auto-Creation
Story: STORY-540
TDD Phase: Red (tests must FAIL before implementation)

Validates that positioning-strategy.md documents:
- Auto-creation of output directory
- YAML frontmatter fields (story_id, generated_date, skill)
- Required sections (## Positioning Statement, ## Key Messages)
"""
import re
import pytest


class TestDirectoryAutoCreation:
    """Verify the reference documents automatic directory creation."""

    def test_should_document_auto_directory_creation(self, strategy_content):
        assert re.search(
            r"(?i)(auto.*creat.*director|director.*creat.*automatic|mkdir|create.*path)",
            strategy_content,
        ), "Reference must document automatic directory creation for output path"


class TestYamlFrontmatter:
    """Verify the reference documents required YAML frontmatter fields."""

    def test_should_document_story_id_frontmatter_field(self, strategy_content):
        assert re.search(
            r"(?i)(story_id|story.id).*frontmatter|frontmatter.*story_id",
            strategy_content,
        ), "Reference must document 'story_id' YAML frontmatter field"

    def test_should_document_generated_date_frontmatter_field(self, strategy_content):
        assert re.search(
            r"(?i)(generated_date|generated.date).*frontmatter|frontmatter.*generated_date",
            strategy_content,
        ), "Reference must document 'generated_date' YAML frontmatter field"

    def test_should_document_skill_frontmatter_field(self, strategy_content):
        assert re.search(
            r"(?i)skill.*frontmatter|frontmatter.*skill",
            strategy_content,
        ), "Reference must document 'skill' YAML frontmatter field"

    def test_should_show_frontmatter_example_with_triple_dashes(self, strategy_content):
        # YAML frontmatter delimited by ---
        assert strategy_content.count("---") >= 2, (
            "Reference must include YAML frontmatter example delimited by ---"
        )


class TestRequiredOutputSections:
    """Verify the reference documents required output file sections."""

    def test_should_document_positioning_statement_section(self, strategy_content):
        assert re.search(
            r"##\s+Positioning\s+Statement", strategy_content
        ), "Reference must document '## Positioning Statement' section in output"

    def test_should_document_key_messages_section(self, strategy_content):
        assert re.search(
            r"##\s+Key\s+Messages", strategy_content
        ), "Reference must document '## Key Messages' section in output"


class TestOutputFilePath:
    """Verify the reference documents the correct output file path."""

    def test_should_document_output_file_path(self, strategy_content):
        assert re.search(
            r"devforgeai/specs/business/marketing/positioning\.md",
            strategy_content,
        ), "Reference must document output path: devforgeai/specs/business/marketing/positioning.md"
