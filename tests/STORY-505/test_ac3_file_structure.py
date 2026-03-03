"""
Test: AC#3 - Rule File Has Valid Structure
Story: STORY-505
Phase: Red (TDD)

Validates YAML frontmatter, exactly 2 numbered rules, and under 300 lines.
"""
import re
import pytest


class TestFileStructure:
    """AC#3: Rule file must have valid YAML frontmatter, 2 rules, under 300 lines."""

    def test_should_have_yaml_frontmatter(self, rule_file_content):
        """File must start with YAML frontmatter delimited by ---."""
        assert rule_file_content.startswith("---"), (
            "File must start with YAML frontmatter delimiter '---'"
        )
        # Must have closing delimiter
        parts = rule_file_content.split("---", 2)
        assert len(parts) >= 3, (
            "File must have opening and closing '---' YAML frontmatter delimiters"
        )

    def test_should_have_name_in_frontmatter(self, rule_file_content):
        """YAML frontmatter must contain 'name' field."""
        frontmatter = rule_file_content.split("---")[1]
        assert re.search(r"^name:", frontmatter, re.MULTILINE), (
            "YAML frontmatter must contain 'name' field"
        )

    def test_should_have_description_in_frontmatter(self, rule_file_content):
        """YAML frontmatter must contain 'description' field."""
        frontmatter = rule_file_content.split("---")[1]
        assert re.search(r"^description:", frontmatter, re.MULTILINE), (
            "YAML frontmatter must contain 'description' field"
        )

    def test_should_have_version_in_frontmatter(self, rule_file_content):
        """YAML frontmatter must contain 'version' field."""
        frontmatter = rule_file_content.split("---")[1]
        assert re.search(r"^version:", frontmatter, re.MULTILINE), (
            "YAML frontmatter must contain 'version' field"
        )

    def test_should_have_created_in_frontmatter(self, rule_file_content):
        """YAML frontmatter must contain 'created' field."""
        frontmatter = rule_file_content.split("---")[1]
        assert re.search(r"^created:", frontmatter, re.MULTILINE), (
            "YAML frontmatter must contain 'created' field"
        )

    def test_should_have_exactly_two_numbered_rules(self, rule_file_content):
        """File body must contain exactly 2 numbered rules."""
        # Match patterns like "## Rule 1:" or "### Rule 1:" or "## 1." etc.
        rule_headers = re.findall(
            r"^#{2,3}\s+Rule\s+\d+", rule_file_content, re.MULTILINE
        )
        assert len(rule_headers) == 2, (
            f"File must contain exactly 2 numbered rules, found {len(rule_headers)}: {rule_headers}"
        )

    def test_should_be_under_300_lines(self, rule_file_lines):
        """File must be under 300 lines."""
        line_count = len(rule_file_lines)
        assert line_count < 300, (
            f"File must be under 300 lines, found {line_count}"
        )
