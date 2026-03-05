"""
Test: AC#5 - Parseable Output Structure
Story: STORY-537
Generated: 2026-03-05

Validates that customer-interviews.md has YAML frontmatter with required
fields, hypothesis sections with ## headers, numbered questions, and
a Next Steps section.
"""
import os
import re
import pytest
import yaml

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
OUTPUT_FILE = os.path.join(
    PROJECT_ROOT, "devforgeai", "specs", "business", "market-research", "customer-interviews.md"
)


def _extract_frontmatter(content: str) -> str:
    """Extract YAML frontmatter from markdown content."""
    match = re.match(r"^---\s*\n(.*?)\n---", content, re.DOTALL)
    assert match, "No YAML frontmatter found (expected --- delimiters)"
    return match.group(1)


class TestYAMLFrontmatter:
    """Verify output has valid YAML frontmatter with required fields."""

    def test_should_have_yaml_frontmatter(self, output_content):
        """AC5: Output must start with --- delimited YAML frontmatter."""
        assert output_content.strip().startswith("---"), (
            "customer-interviews.md must start with YAML frontmatter (---)"
        )
        _extract_frontmatter(output_content)

    def test_should_have_date_field(self, output_content):
        """AC5: Frontmatter must contain a date field."""
        fm_text = _extract_frontmatter(output_content)
        fm = yaml.safe_load(fm_text)
        assert "date" in fm, "YAML frontmatter missing 'date' field"

    def test_should_have_hypothesis_count_field(self, output_content):
        """AC5: Frontmatter must contain a hypothesis_count field."""
        fm_text = _extract_frontmatter(output_content)
        fm = yaml.safe_load(fm_text)
        assert "hypothesis_count" in fm, (
            "YAML frontmatter missing 'hypothesis_count' field"
        )

    def test_should_have_question_count_field(self, output_content):
        """AC5: Frontmatter must contain a question_count field."""
        fm_text = _extract_frontmatter(output_content)
        fm = yaml.safe_load(fm_text)
        assert "question_count" in fm, (
            "YAML frontmatter missing 'question_count' field"
        )

    def test_should_have_valid_counts(self, output_content):
        """AC5: Frontmatter counts must be positive integers."""
        fm_text = _extract_frontmatter(output_content)
        fm = yaml.safe_load(fm_text)
        assert isinstance(fm.get("hypothesis_count"), int) and fm["hypothesis_count"] > 0, (
            "hypothesis_count must be a positive integer"
        )
        assert isinstance(fm.get("question_count"), int) and fm["question_count"] > 0, (
            "question_count must be a positive integer"
        )


class TestHypothesisHeaders:
    """Verify output has ## hypothesis section headers."""

    def test_should_have_hypothesis_headers(self, output_content):
        """AC5: Output must have ## headers for hypothesis sections."""
        # Strip frontmatter
        body = re.sub(r"^---.*?---\s*", "", output_content, count=1, flags=re.DOTALL)
        headings = re.findall(r"^## (.+)", body, re.MULTILINE)
        hypothesis_headings = [
            h for h in headings if "next steps" not in h.lower()
        ]
        assert len(hypothesis_headings) >= 1, (
            "No ## hypothesis headings found in output body"
        )


class TestNumberedQuestions:
    """Verify questions are numbered under each hypothesis."""

    def test_should_have_numbered_questions(self, output_content):
        """AC5: Questions must be numbered (1. 2. 3. etc.)."""
        questions = re.findall(r"^\d+\.\s+.+", output_content, re.MULTILINE)
        assert len(questions) >= 10, (
            f"Expected >= 10 numbered questions, found {len(questions)}"
        )


class TestNextStepsSection:
    """Verify output contains a Next Steps section."""

    def test_should_have_next_steps_section(self, output_content):
        """AC5: Output must contain a '## Next Steps' section."""
        pattern = re.compile(r"^## Next Steps", re.MULTILINE | re.IGNORECASE)
        assert pattern.search(output_content), (
            "Missing '## Next Steps' section in customer-interviews.md"
        )

    def test_should_have_content_in_next_steps(self, output_content):
        """AC5: Next Steps section must contain actionable content."""
        match = re.search(
            r"^## Next Steps\s*\n(.+)", output_content,
            re.MULTILINE | re.IGNORECASE,
        )
        assert match, "Next Steps section is empty"
