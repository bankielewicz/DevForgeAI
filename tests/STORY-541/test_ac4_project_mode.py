"""
Test: AC#4 - Project-Anchored Mode
Story: STORY-541
Generated: 2026-03-05

Validates:
- --mode=project support in command
- Reads tech-stack.md, source-tree.md in project mode
- Output stored in devforgeai/specs/marketing/ with timestamp
- NFR-002: No Write() calls target context file paths
"""
import os
import re

import pytest

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
COMMAND_FILE = os.path.join(PROJECT_ROOT, "src", "claude", "commands", "marketing-plan.md")
SKILL_FILE = os.path.join(PROJECT_ROOT, "src", "claude", "skills", "marketing-business", "SKILL.md")

CONTEXT_FILE_PATHS = [
    "devforgeai/specs/context/tech-stack.md",
    "devforgeai/specs/context/source-tree.md",
    "devforgeai/specs/context/dependencies.md",
    "devforgeai/specs/context/coding-standards.md",
    "devforgeai/specs/context/architecture-constraints.md",
    "devforgeai/specs/context/anti-patterns.md",
]


@pytest.fixture
def command_content():
    """Arrange: Read command file content."""
    assert os.path.isfile(COMMAND_FILE), f"Command file not found: {COMMAND_FILE}"
    with open(COMMAND_FILE, "r", encoding="utf-8") as f:
        return f.read()


@pytest.fixture
def skill_content():
    """Arrange: Read SKILL.md content."""
    assert os.path.isfile(SKILL_FILE), f"SKILL.md not found: {SKILL_FILE}"
    with open(SKILL_FILE, "r", encoding="utf-8") as f:
        return f.read()


class TestProjectModeFlag:
    """Tests for --mode=project support."""

    def test_should_support_mode_project_flag(self, command_content):
        """Act & Assert: Command must support --mode=project flag."""
        assert "--mode=project" in command_content or "--mode" in command_content, (
            "Command must support --mode=project flag"
        )

    def test_should_document_standalone_as_default(self, command_content):
        """Act & Assert: Standalone mode should be the default."""
        patterns = ["standalone", "default"]
        found = sum(1 for p in patterns if p.lower() in command_content.lower())
        assert found >= 1, (
            "Command must document standalone as the default mode"
        )


class TestContextFileReading:
    """Tests for context file reading in project mode."""

    def test_should_read_tech_stack_in_project_mode(self, skill_content):
        """Act & Assert: Skill must read tech-stack.md in project mode."""
        assert "tech-stack" in skill_content.lower(), (
            "SKILL.md must reference reading tech-stack.md in project mode"
        )

    def test_should_read_source_tree_in_project_mode(self, skill_content):
        """Act & Assert: Skill must read source-tree.md in project mode."""
        assert "source-tree" in skill_content.lower(), (
            "SKILL.md must reference reading source-tree.md in project mode"
        )


class TestOutputStorage:
    """Tests for output stored in devforgeai/specs/marketing/."""

    def test_should_store_output_in_marketing_directory(self, skill_content):
        """Act & Assert: Skill must store output in devforgeai/specs/marketing/."""
        assert "devforgeai/specs/marketing/" in skill_content, (
            "SKILL.md must store output in devforgeai/specs/marketing/"
        )

    def test_should_use_timestamped_filename(self, skill_content):
        """Act & Assert: Skill must use timestamped filename for output."""
        timestamp_patterns = ["timestamp", "YYYY-MM-DD", "date", "datetime"]
        found = any(p.lower() in skill_content.lower() for p in timestamp_patterns)
        assert found, (
            "SKILL.md must use timestamped filename for output artifacts"
        )


class TestContextFileImmutability:
    """Tests for NFR-002: No Write() calls target context file paths."""

    def test_should_not_write_to_context_files(self, skill_content):
        """Act & Assert: Skill must not contain Write() targeting context paths."""
        for ctx_path in CONTEXT_FILE_PATHS:
            # Check for Write() calls that target context files
            write_pattern = rf'Write\([^)]*{re.escape(ctx_path)}'
            matches = re.findall(write_pattern, skill_content)
            assert len(matches) == 0, (
                f"SKILL.md must not Write() to context file: {ctx_path} (NFR-002)"
            )

    def test_should_declare_context_files_read_only(self, skill_content):
        """Act & Assert: Skill must declare context files as read-only."""
        patterns = ["read-only", "read only", "immutable", "never write"]
        found = any(p.lower() in skill_content.lower() for p in patterns)
        assert found, (
            "SKILL.md must declare context files as read-only (NFR-002)"
        )
