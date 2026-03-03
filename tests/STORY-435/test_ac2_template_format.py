"""
Test: AC#2 - Requirements Template Uses YAML Frontmatter
Story: STORY-435
Generated: 2026-02-17 (TDD Red Phase)

Validates that requirements-template.md uses YAML frontmatter for ALL structured
data with a minimal markdown body for human readability only.
"""
import os
import re
import pytest
import yaml


class TestTemplateFileExists:
    """Template file must exist at the correct path."""

    def test_should_exist_at_correct_path(self, template_path):
        assert os.path.isfile(template_path), (
            f"Template file not found at {template_path}"
        )


class TestYAMLFrontmatter:
    """Template must have valid YAML frontmatter with all schema fields."""

    @pytest.fixture
    def template_content(self, template_path):
        with open(template_path, "r") as f:
            return f.read()

    @pytest.fixture
    def frontmatter(self, template_content):
        """Extract YAML frontmatter from template."""
        match = re.match(r"^---\n(.*?)\n---", template_content, re.DOTALL)
        assert match, "Template must start with YAML frontmatter (---)"
        return yaml.safe_load(match.group(1))

    def test_should_start_with_yaml_frontmatter(self, template_content):
        assert template_content.startswith("---\n"), (
            "Template must start with YAML frontmatter delimiter '---'"
        )

    def test_should_have_closing_frontmatter_delimiter(self, template_content):
        # Find second --- delimiter
        parts = template_content.split("---", 2)
        assert len(parts) >= 3, (
            "Template must have opening and closing '---' frontmatter delimiters"
        )

    def test_frontmatter_should_contain_decisions(self, frontmatter):
        assert "decisions" in frontmatter, "Frontmatter missing 'decisions' field"

    def test_frontmatter_should_contain_scope(self, frontmatter):
        assert "scope" in frontmatter, "Frontmatter missing 'scope' field"

    def test_frontmatter_should_contain_success_criteria(self, frontmatter):
        assert "success_criteria" in frontmatter, (
            "Frontmatter missing 'success_criteria' field"
        )

    def test_frontmatter_should_contain_constraints(self, frontmatter):
        assert "constraints" in frontmatter, "Frontmatter missing 'constraints' field"

    def test_frontmatter_should_contain_nfrs(self, frontmatter):
        assert "nfrs" in frontmatter, "Frontmatter missing 'nfrs' field"

    def test_frontmatter_should_contain_stakeholders(self, frontmatter):
        assert "stakeholders" in frontmatter, (
            "Frontmatter missing 'stakeholders' field"
        )

    def test_frontmatter_should_contain_source_brainstorm(self, frontmatter):
        assert "source_brainstorm" in frontmatter, (
            "Frontmatter missing 'source_brainstorm' field"
        )


class TestMarkdownBody:
    """Markdown body should be minimal - not duplicating YAML data."""

    @pytest.fixture
    def template_content(self, template_path):
        with open(template_path, "r") as f:
            return f.read()

    @pytest.fixture
    def markdown_body(self, template_content):
        """Extract markdown body (everything after frontmatter)."""
        parts = template_content.split("---", 2)
        assert len(parts) >= 3, "Template must have frontmatter"
        return parts[2].strip()

    def test_should_have_markdown_body(self, markdown_body):
        assert len(markdown_body) > 0, "Template must have a markdown body"

    def test_body_should_not_duplicate_decision_data(self, markdown_body):
        # Body should not contain full decision structures
        # It should reference YAML data, not repeat it
        decision_pattern = re.findall(r"rejected.*?option.*?reason", markdown_body, re.DOTALL)
        assert len(decision_pattern) == 0, (
            "Markdown body should not duplicate decision data from YAML frontmatter"
        )

    def test_body_should_be_minimal(self, markdown_body):
        # Markdown body should be significantly shorter than a full narrative template
        # Old template was ~300 lines; new body should be much less
        line_count = len(markdown_body.splitlines())
        assert line_count < 100, (
            f"Markdown body has {line_count} lines; should be minimal (< 100 lines)"
        )
