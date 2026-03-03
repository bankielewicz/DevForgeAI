"""
Test: AC#4 - Solution Example Documented
Story: STORY-411
Generated: 2026-02-16

Validates that a code example showing immediate skill invocation
(correct pattern) is documented within Anti-Pattern 6 section.
"""
import subprocess
import re
import pytest

TARGET_FILE = "devforgeai/protocols/lean-orchestration-pattern.md"


def _get_antipattern6_section() -> str:
    """Extract the Anti-Pattern 6 section content."""
    result = subprocess.run(
        ["cat", TARGET_FILE],
        capture_output=True, text=True,
    )
    content = result.stdout
    # Find Anti-Pattern 6 section - stop at horizontal rule (---) which separates sections
    match = re.search(
        r"(###\s*Anti-Pattern\s+6.*?)(?=\n---\n|\Z)",
        content, re.DOTALL | re.IGNORECASE,
    )
    return match.group(1) if match else ""


def test_should_contain_solution_code_block_in_antipattern6():
    """AC#4: Must contain at least 2 code blocks (problem + solution)."""
    section = _get_antipattern6_section()
    assert section, "Anti-Pattern 6 section not found"
    code_block_markers = re.findall(r"```", section)
    assert len(code_block_markers) >= 4, (
        f"Expected at least 2 code blocks (4 markers) in Anti-Pattern 6, "
        f"found {len(code_block_markers)} markers"
    )


def test_should_show_immediate_skill_invocation_in_solution():
    """AC#4: Solution must show Skill() called immediately."""
    section = _get_antipattern6_section()
    assert section, "Anti-Pattern 6 section not found"
    assert "Skill(" in section, "Expected Skill() in solution example"


def test_should_label_solution_as_correct_in_antipattern6():
    """AC#4: Solution should be labeled as correct/right pattern."""
    section = _get_antipattern6_section()
    assert section, "Anti-Pattern 6 section not found"
    has_label = bool(re.search(r"(?i)(correct|right|good|proper|solution|instead)", section))
    assert has_label, "Expected solution labeled as correct/right/proper pattern"
