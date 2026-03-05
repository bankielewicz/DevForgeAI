"""
Test: AC#3 - Hypothesis-Driven Questions
Story: STORY-537
Generated: 2026-03-05

Validates that each question maps to a named hypothesis, avoids leading
phrasing, and is open-ended (no closed-ended question starters).
"""
import os
import re
import pytest

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
OUTPUT_FILE = os.path.join(
    PROJECT_ROOT, "devforgeai", "specs", "business", "market-research", "customer-interviews.md"
)


# Closed-ended question starters that are FORBIDDEN per BR-001
FORBIDDEN_STARTERS = [
    "Do", "Is", "Are", "Was", "Were", "Will", "Would",
    "Can", "Could", "Should", "Did", "Has",
]


class TestQuestionsMappedToHypotheses:
    """Verify each question appears under a hypothesis heading."""

    def test_should_have_all_questions_under_hypothesis_sections(self, output_content):
        """AC3/BR-001: Every question must appear under a named hypothesis ## heading."""
        # Find all ## headings and their positions
        headings = list(re.finditer(r"^## (.+)", output_content, re.MULTILINE))
        questions = list(re.finditer(r"^\d+\.\s+.+", output_content, re.MULTILINE))

        assert len(questions) > 0, "No numbered questions found in output"

        for q in questions:
            # Find the closest heading before this question
            preceding_headings = [
                h for h in headings if h.start() < q.start()
            ]
            assert len(preceding_headings) > 0, (
                f"Question at line has no preceding hypothesis heading: "
                f"'{q.group().strip()[:60]}...'"
            )
            # Verify it's not under "Next Steps"
            closest_heading = preceding_headings[-1].group(1).strip()
            assert "next steps" not in closest_heading.lower(), (
                f"Question found under 'Next Steps' instead of a hypothesis: "
                f"'{q.group().strip()[:60]}...'"
            )


class TestOpenEndedQuestions:
    """Verify all questions are open-ended per BR-001."""

    def test_should_not_start_with_closed_ended_words(self, output_content):
        """AC3/BR-001: No question may start with Do/Is/Are/Was/Were/Will/Would/Can/Could/Should/Did/Has."""
        questions = re.findall(r"^\d+\.\s+(.+)", output_content, re.MULTILINE)
        assert len(questions) > 0, "No numbered questions found in output"

        violations = []
        for q_text in questions:
            first_word = q_text.strip().split()[0].rstrip("?.,:")
            if first_word in FORBIDDEN_STARTERS:
                violations.append(f"'{q_text.strip()[:80]}' starts with '{first_word}'")

        assert len(violations) == 0, (
            f"Found {len(violations)} closed-ended questions:\n"
            + "\n".join(f"  - {v}" for v in violations)
        )

    def test_should_start_with_open_ended_starters(self, output_content):
        """AC3: Questions should start with How, What, Tell me about, Describe, Walk me through."""
        open_starters = re.compile(
            r"^(How|What|Tell me about|Describe|Walk me through)",
            re.IGNORECASE,
        )
        questions = re.findall(r"^\d+\.\s+(.+)", output_content, re.MULTILINE)
        assert len(questions) > 0, "No numbered questions found in output"

        non_open = []
        for q_text in questions:
            if not open_starters.match(q_text.strip()):
                non_open.append(q_text.strip()[:80])

        assert len(non_open) == 0, (
            f"Found {len(non_open)} questions not starting with open-ended phrases:\n"
            + "\n".join(f"  - {q}" for q in non_open)
        )


class TestNoLeadingPhrasing:
    """Verify questions avoid leading/biased phrasing."""

    def test_should_not_contain_leading_phrases(self, output_content):
        """AC3: Questions must not contain leading phrases that suggest an answer."""
        leading_patterns = [
            r"don't you think",
            r"wouldn't you agree",
            r"isn't it true",
            r"obviously",
            r"clearly",
            r"of course",
        ]
        questions = re.findall(r"^\d+\.\s+(.+)", output_content, re.MULTILINE)
        assert len(questions) > 0, "No numbered questions found in output"

        violations = []
        for q_text in questions:
            for pattern in leading_patterns:
                if re.search(pattern, q_text, re.IGNORECASE):
                    violations.append(
                        f"'{q_text.strip()[:80]}' contains leading phrase matching '{pattern}'"
                    )

        assert len(violations) == 0, (
            f"Found {len(violations)} questions with leading phrasing:\n"
            + "\n".join(f"  - {v}" for v in violations)
        )
