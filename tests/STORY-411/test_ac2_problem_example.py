"""
Test: AC#2 - Problem Example Documented
Story: STORY-411
Generated: 2026-02-16

Validates that a code example showing a command with manual steps
before Skill() invocation is documented within Anti-Pattern 6 section.
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


def test_should_contain_problem_code_block_in_antipattern6():
    """AC#2: Anti-Pattern 6 section must contain a code block with bad example."""
    section = _get_antipattern6_section()
    assert section, "Anti-Pattern 6 section not found"
    assert "```" in section, "Expected code block in Anti-Pattern 6 section"


def test_should_show_manual_steps_before_skill_in_antipattern6():
    """AC#2: Problem example must show manual steps executed before Skill()."""
    section = _get_antipattern6_section()
    assert section, "Anti-Pattern 6 section not found"
    # Look for step indicators before Skill() invocation, or explicit manual mentions
    has_manual = any(kw in section for kw in ["Step 1:", "Step 2:", "Step 3:", "manual", "executes this", "Claude executes"])
    assert has_manual, (
        "Expected problem example showing manual steps before Skill() invocation"
    )


def test_should_show_skill_invocation_in_antipattern6():
    """AC#2: Problem example must include Skill() call."""
    section = _get_antipattern6_section()
    assert section, "Anti-Pattern 6 section not found"
    assert "Skill(" in section, "Expected Skill() in Anti-Pattern 6 problem example"
