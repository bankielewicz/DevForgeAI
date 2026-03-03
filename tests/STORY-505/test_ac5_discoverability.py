"""
Test: AC#5 - File Is Discoverable from Rules README
Story: STORY-505
Phase: Red (TDD)

Validates that the workflow/ directory is listed in Rules README
and .gitignore contains tmp/ entry.
"""
import os
import pytest
from conftest import OPERATIONAL_SAFETY_PATH, GITIGNORE_PATH, RULES_README_PATH


class TestDiscoverability:
    """AC#5: File must be discoverable from Rules README."""

    def test_should_have_workflow_listed_in_rules_readme(self, rules_readme_content):
        """Rules README must list the workflow/ directory."""
        assert "workflow/" in rules_readme_content or "workflow" in rules_readme_content, (
            "Rules README must list workflow/ directory"
        )

    def test_should_have_operational_safety_file_exist(self):
        """operational-safety.md must exist at expected path."""
        assert os.path.isfile(OPERATIONAL_SAFETY_PATH), (
            f"operational-safety.md must exist at {OPERATIONAL_SAFETY_PATH}"
        )


class TestGitignoreTmpEntry:
    """BR-003: .gitignore must contain tmp/ entry."""

    def test_should_have_tmp_in_gitignore(self, gitignore_content):
        """gitignore must contain tmp/ entry to prevent accidental tracking."""
        lines = [l.strip() for l in gitignore_content.splitlines()]
        has_tmp = any(
            line == "tmp/" or line == "tmp" or line == "/tmp/"
            for line in lines
            if not line.startswith("#")
        )
        assert has_tmp, (
            ".gitignore must contain 'tmp/' entry"
        )
