"""
Test: AC#1 - Interview Question Output Structure
Story: STORY-537
Generated: 2026-03-05

Validates that customer-interviews.md exists at the correct path,
contains 10-20 questions organized under hypothesis headings,
and each hypothesis section contains 2-5 questions.
"""
import os
import re
import pytest

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
OUTPUT_FILE = os.path.join(
    PROJECT_ROOT, "devforgeai", "specs", "business", "market-research", "customer-interviews.md"
)


class TestOutputFileExists:
    """Verify the output file is created at the correct path."""

    def test_should_exist_at_market_research_path(self):
        """AC1: Output file must exist at devforgeai/specs/business/market-research/customer-interviews.md"""
        assert os.path.isfile(OUTPUT_FILE), (
            f"customer-interviews.md not found at {OUTPUT_FILE}"
        )

    def test_should_be_nonempty(self, output_content):
        """AC1: Output file must contain content."""
        assert len(output_content.strip()) > 0, "customer-interviews.md is empty"


class TestQuestionCount:
    """Verify total question count is 10-20."""

    def test_should_contain_at_least_10_questions(self, output_content):
        """AC1/BR-002: Output must contain at least 10 questions."""
        # Questions are numbered lines: "1. ...", "2. ...", etc.
        questions = re.findall(r"^\d+\.\s+.+", output_content, re.MULTILINE)
        assert len(questions) >= 10, (
            f"Expected >= 10 questions, found {len(questions)}"
        )

    def test_should_contain_at_most_20_questions(self, output_content):
        """AC1/BR-002: Output must contain at most 20 questions."""
        questions = re.findall(r"^\d+\.\s+.+", output_content, re.MULTILINE)
        assert len(questions) <= 20, (
            f"Expected <= 20 questions, found {len(questions)}"
        )


class TestHypothesisSections:
    """Verify questions are organized under hypothesis headings."""

    def test_should_have_hypothesis_headings(self, output_content):
        """AC1: Questions must be organized under ## hypothesis headings."""
        hypothesis_headings = re.findall(
            r"^## .+", output_content, re.MULTILINE
        )
        # Filter out non-hypothesis headings like "## Next Steps"
        hypothesis_headings = [
            h for h in hypothesis_headings
            if "next steps" not in h.lower()
            and "frontmatter" not in h.lower()
        ]
        assert len(hypothesis_headings) >= 2, (
            f"Expected >= 2 hypothesis headings, found {len(hypothesis_headings)}"
        )

    def test_should_have_2_to_5_questions_per_hypothesis(self, output_content):
        """AC1/BR-002: Each hypothesis section must contain 2-5 questions."""
        # Split by ## headings, extract question counts per section
        sections = re.split(r"^## ", output_content, flags=re.MULTILINE)
        for section in sections[1:]:  # skip content before first ##
            heading = section.split("\n")[0].strip()
            if "next steps" in heading.lower():
                continue
            questions = re.findall(r"^\d+\.\s+.+", section, re.MULTILINE)
            if len(questions) == 0:
                continue  # non-question section
            assert 2 <= len(questions) <= 5, (
                f"Hypothesis '{heading}' has {len(questions)} questions, expected 2-5"
            )
