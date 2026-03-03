"""
Test: AC#4 - tmp/ Directory Path Clarification
Story: STORY-505
Phase: Red (TDD)

Validates that Rule 2 specifies paths relative to project root
and clarifies CWD verification.
"""
import re
import pytest


class TestPathClarification:
    """AC#4: Rule 2 must clarify relative path construction and CWD verification."""

    def test_should_specify_relative_to_project_root(self, rule_file_content):
        """Rule 2 must specify path relative to project root."""
        content_lower = rule_file_content.lower()
        assert "project root" in content_lower or "project-root" in content_lower, (
            "Rule 2 must mention 'project root' for path construction"
        )

    def test_should_show_relative_path_example(self, rule_file_content):
        """Rule 2 must show relative path example like tmp/STORY-505/."""
        assert re.search(r"tmp/STORY-\d+/", rule_file_content), (
            "Rule 2 must show relative path example (e.g., tmp/STORY-505/)"
        )

    def test_should_clarify_cwd_verification(self, rule_file_content):
        """Rule 2 must clarify that relative paths require CWD verification."""
        content_lower = rule_file_content.lower()
        has_cwd_note = any(
            term in content_lower
            for term in ["cwd", "current working directory", "working directory"]
        )
        assert has_cwd_note, (
            "Rule 2 must clarify CWD verification for relative paths"
        )
