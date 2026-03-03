"""
Test: AC#5 - Dual-Path Sync (src/ and .claude/)
Story: STORY-439
Phase: RED (TDD - tests expected to FAIL)
Pattern: AAA (Arrange, Act, Assert)
"""
import os
import pytest

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

SYNC_PAIRS = [
    (
        os.path.join(PROJECT_ROOT, "src", "claude", "commands", "create-epic.md"),
        os.path.join(PROJECT_ROOT, ".claude", "commands", "create-epic.md"),
    ),
    (
        os.path.join(PROJECT_ROOT, "src", "claude", "commands", "ideate.md"),
        os.path.join(PROJECT_ROOT, ".claude", "commands", "ideate.md"),
    ),
    (
        os.path.join(PROJECT_ROOT, "src", "claude", "skills", "devforgeai-architecture", "references", "skill-output-schemas.yaml"),
        os.path.join(PROJECT_ROOT, ".claude", "skills", "devforgeai-architecture", "references", "skill-output-schemas.yaml"),
    ),
]


class TestDualPathSync:
    """BR-003: All changes in src/ must be mirrored to .claude/."""

    @pytest.mark.parametrize("src_path,op_path", SYNC_PAIRS, ids=[
        "create-epic.md",
        "ideate.md",
        "architecture-schema.yaml",
    ])
    def test_should_have_matching_content_when_both_paths_exist(self, src_path, op_path):
        # Arrange
        assert os.path.isfile(src_path), f"Source file missing: {src_path}"
        assert os.path.isfile(op_path), f"Operational file missing: {op_path}"
        with open(src_path, "r", encoding="utf-8") as f:
            src_content = f.read()
        with open(op_path, "r", encoding="utf-8") as f:
            op_content = f.read()
        # Act / Assert
        assert src_content == op_content, (
            f"Dual-path mismatch:\n  src: {src_path}\n  op:  {op_path}"
        )
