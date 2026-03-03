"""
Test: AC#1 - Anti-Pattern 6 Section Added
Story: STORY-411
Generated: 2026-02-16

Validates that a new 'Anti-Pattern 6: Hybrid Command/Skill Workflow' section
exists in lean-orchestration-pattern.md after existing anti-patterns.
"""
import subprocess
import pytest

TARGET_FILE = "devforgeai/protocols/lean-orchestration-pattern.md"


def _grep(pattern: str) -> bool:
    """Return True if pattern found in target file."""
    result = subprocess.run(
        ["grep", "-qP", pattern, TARGET_FILE],
        capture_output=True,
    )
    return result.returncode == 0


def test_should_contain_antipattern_6_header_when_section_added():
    """AC#1: Anti-Pattern 6 section header must exist."""
    assert _grep(r"Anti-Pattern\s+6"), (
        f"Expected 'Anti-Pattern 6' header in {TARGET_FILE}"
    )


def test_should_contain_hybrid_command_skill_in_title_when_section_added():
    """AC#1: Title must reference Hybrid Command/Skill Workflow."""
    assert _grep(r"Hybrid\s+Command/Skill\s+Workflow"), (
        f"Expected 'Hybrid Command/Skill Workflow' in {TARGET_FILE}"
    )


def test_should_place_antipattern_6_after_existing_antipatterns():
    """AC#1: Anti-Pattern 6 must appear after Anti-Pattern 5 (or last existing)."""
    result = subprocess.run(
        ["grep", "-n", "Anti-Pattern", TARGET_FILE],
        capture_output=True, text=True,
    )
    lines = result.stdout.strip().split("\n")
    ap6_lines = [l for l in lines if "Anti-Pattern 6" in l or "Anti-Pattern  6" in l]
    other_lines = [l for l in lines if "Anti-Pattern 6" not in l and l.strip()]

    assert len(ap6_lines) > 0, "Anti-Pattern 6 not found"
    assert len(other_lines) > 0, "No other anti-patterns found to verify ordering"

    ap6_line_num = int(ap6_lines[0].split(":")[0])
    max_other = max(int(l.split(":")[0]) for l in other_lines)
    assert ap6_line_num > max_other, (
        f"Anti-Pattern 6 (line {ap6_line_num}) should appear after "
        f"last existing anti-pattern (line {max_other})"
    )
