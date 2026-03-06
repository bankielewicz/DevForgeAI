"""
Test: AC#3 - Progressive Disclosure Architecture
Story: STORY-541
Generated: 2026-03-05

Validates:
- SKILL.md < 1,000 lines (BR-002)
- References loaded on demand from references/ directory
- References directory exists with workflow files
"""
import os

import pytest

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
SKILL_FILE = os.path.join(PROJECT_ROOT, "src", "claude", "skills", "marketing-business", "SKILL.md")
REFERENCES_DIR = os.path.join(PROJECT_ROOT, "src", "claude", "skills", "marketing-business", "references")


@pytest.fixture
def skill_content():
    """Arrange: Read SKILL.md content."""
    assert os.path.isfile(SKILL_FILE), f"SKILL.md not found: {SKILL_FILE}"
    with open(SKILL_FILE, "r", encoding="utf-8") as f:
        return f.read()


@pytest.fixture
def skill_lines(skill_content):
    """Arrange: Split SKILL.md into lines."""
    return skill_content.splitlines()


class TestSkillFileSizeLimit:
    """Tests for BR-002: SKILL.md < 1,000 lines."""

    def test_should_be_under_1000_lines(self, skill_lines):
        """Act & Assert: SKILL.md must be under 1,000 lines per BR-002."""
        line_count = len(skill_lines)
        assert line_count < 1000, (
            f"SKILL.md has {line_count} lines, exceeds 1,000 line limit (BR-002)"
        )


class TestReferencesDirectory:
    """Tests for references/ directory existence and content."""

    def test_should_have_references_directory(self):
        """Act & Assert: references/ directory must exist."""
        assert os.path.isdir(REFERENCES_DIR), (
            f"References directory not found: {REFERENCES_DIR}"
        )

    def test_should_have_at_least_one_reference_file(self):
        """Act & Assert: references/ must contain at least one file."""
        assert os.path.isdir(REFERENCES_DIR), f"References directory not found: {REFERENCES_DIR}"
        files = [f for f in os.listdir(REFERENCES_DIR) if os.path.isfile(os.path.join(REFERENCES_DIR, f))]
        assert len(files) >= 1, (
            "References directory must contain at least one reference file"
        )

    def test_should_have_markdown_reference_files(self):
        """Act & Assert: references/ must contain .md files."""
        assert os.path.isdir(REFERENCES_DIR), f"References directory not found: {REFERENCES_DIR}"
        md_files = [f for f in os.listdir(REFERENCES_DIR) if f.endswith(".md")]
        assert len(md_files) >= 1, (
            "References directory must contain at least one .md file"
        )


class TestOnDemandLoading:
    """Tests for on-demand reference loading pattern."""

    def test_should_reference_references_directory(self, skill_content):
        """Act & Assert: SKILL.md must reference the references/ directory."""
        assert "references/" in skill_content, (
            "SKILL.md must reference the references/ directory for on-demand loading"
        )

    def test_should_use_read_pattern_for_references(self, skill_content):
        """Act & Assert: SKILL.md must use Read() pattern for loading references."""
        load_patterns = ["Read(", "Read (", "load", "on-demand", "on demand"]
        found = any(p in skill_content for p in load_patterns)
        assert found, (
            "SKILL.md must use Read() or on-demand loading pattern for references"
        )
