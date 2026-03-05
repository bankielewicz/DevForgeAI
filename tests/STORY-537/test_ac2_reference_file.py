"""
Test: AC#2 - Best Practices Reference File
Story: STORY-537
Generated: 2026-03-05

Validates that customer-interview-guide.md exists and contains
required sections: open-ended techniques, bias avoidance, follow-up patterns.
"""
import os
import re
import pytest

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
REFERENCE_FILE = os.path.join(
    PROJECT_ROOT, "src", "claude", "skills", "researching-market", "references", "customer-interview-guide.md"
)


class TestReferenceFileExists:
    """Verify the reference file exists at the correct path."""

    def test_should_exist_at_references_path(self):
        """AC2: Reference file must exist at src/claude/skills/researching-market/references/customer-interview-guide.md"""
        assert os.path.isfile(REFERENCE_FILE), (
            f"customer-interview-guide.md not found at {REFERENCE_FILE}"
        )

    def test_should_be_nonempty(self, reference_content):
        """AC2: Reference file must contain content."""
        assert len(reference_content.strip()) > 0, (
            "customer-interview-guide.md is empty"
        )


class TestRequiredSections:
    """Verify reference file contains all required methodology sections."""

    def test_should_contain_open_ended_techniques_section(self, reference_content):
        """AC2: Must contain a section on open-ended question techniques."""
        pattern = re.compile(r"^#+\s+.*open.ended.*technique", re.MULTILINE | re.IGNORECASE)
        assert pattern.search(reference_content), (
            "Missing section on open-ended question techniques"
        )

    def test_should_contain_bias_avoidance_section(self, reference_content):
        """AC2: Must contain a section on bias avoidance."""
        pattern = re.compile(r"^#+\s+.*bias\s+avoidance", re.MULTILINE | re.IGNORECASE)
        assert pattern.search(reference_content), (
            "Missing section on bias avoidance"
        )

    def test_should_contain_follow_up_patterns_section(self, reference_content):
        """AC2: Must contain a section on follow-up patterns."""
        pattern = re.compile(r"^#+\s+.*follow.up\s+pattern", re.MULTILINE | re.IGNORECASE)
        assert pattern.search(reference_content), (
            "Missing section on follow-up patterns"
        )


class TestReferenceContent:
    """Verify reference file has substantive content in each section."""

    def test_should_have_question_examples_in_open_ended_section(self, reference_content):
        """AC2: Open-ended techniques section should include example question starters."""
        # Look for typical open-ended starters documented as examples
        starters = ["How", "What", "Tell me about", "Describe", "Walk me through"]
        found_any = any(starter in reference_content for starter in starters)
        assert found_any, (
            "Open-ended techniques section missing example question starters "
            "(How, What, Tell me about, Describe, Walk me through)"
        )

    def test_should_have_anti_patterns_in_bias_section(self, reference_content):
        """AC2: Bias avoidance section should list leading question anti-patterns."""
        # Look for closed-ended starters as anti-patterns
        anti_patterns = ["Do you", "Is it", "Are you", "Would you"]
        found_any = any(pattern in reference_content for pattern in anti_patterns)
        assert found_any, (
            "Bias avoidance section missing leading question anti-patterns"
        )
