"""
Test: AC#4 - Ambiguous Input Handling
Story: STORY-539
Generated: 2026-03-04

Tests validate that the go-to-market-framework.md contains guidance for
handling unknown/ambiguous business model inputs with clarifying questions
(max 3) and fallback behavior.
"""
import os
import re
import pytest

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
GTM_FRAMEWORK = os.path.join(PROJECT_ROOT, "src", "claude", "skills", "marketing-business", "references", "go-to-market-framework.md")


class TestAmbiguousInputSection:
    """AC#4: Framework must document ambiguous input handling."""

    @pytest.fixture
    def framework_content(self):
        with open(GTM_FRAMEWORK, "r") as f:
            return f.read()

    def test_should_have_ambiguity_handling_section(self, framework_content):
        # Arrange & Act
        has_section = bool(re.search(r"(?i)(ambig|unclear|unknown|fallback|clarif)", framework_content))
        # Assert
        assert has_section, "Framework missing ambiguity/clarification handling guidance"

    def test_should_specify_maximum_3_clarifying_questions(self, framework_content):
        # Arrange & Act
        has_limit = bool(re.search(r"(?i)(max(imum)?\s*(of\s*)?3\s*(clarif|question))|(\b3\b.*clarif)", framework_content))
        # Assert
        assert has_limit, "Framework must specify maximum 3 clarifying questions for ambiguous inputs"

    def test_should_document_clarifying_question_examples(self, framework_content):
        # Arrange & Act - look for question marks in clarification context
        clarify_section = ""
        sections = re.split(r"^##+ ", framework_content, flags=re.MULTILINE)
        for section in sections:
            if re.search(r"(?i)(ambig|clarif|unknown|fallback)", section):
                clarify_section = section
                break
        questions = re.findall(r"\?", clarify_section)
        # Assert
        assert len(questions) >= 1, "Expected at least 1 example clarifying question"


class TestFallbackBehavior:
    """AC#4: Must proceed without halting after clarification."""

    @pytest.fixture
    def framework_content(self):
        with open(GTM_FRAMEWORK, "r") as f:
            return f.read()

    def test_should_not_halt_on_unknown_model(self, framework_content):
        # Arrange & Act
        has_proceed = bool(re.search(r"(?i)(proceed|continue|fallback|default)", framework_content))
        # Assert
        assert has_proceed, "Framework must document proceed/fallback behavior for unknown models"

    def test_should_incorporate_answers_into_scoring(self, framework_content):
        # Arrange & Act
        has_incorporate = bool(re.search(r"(?i)(incorporat|adjust|refine|update).*(scor|rank|channel)", framework_content))
        # Assert
        assert has_incorporate, "Framework must describe incorporating clarification answers into channel scoring"
