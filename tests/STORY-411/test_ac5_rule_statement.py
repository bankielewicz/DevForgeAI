"""
Test: AC#5 - Rule Statement Added
Story: STORY-411
Generated: 2026-02-16

Validates that the clear rule statement is provided:
"If workflow step belongs in skill, don't document it in command with code blocks"
"""
import subprocess
import pytest

TARGET_FILE = "devforgeai/protocols/lean-orchestration-pattern.md"


def _grep(pattern: str) -> bool:
    result = subprocess.run(
        ["grep", "-qPi", pattern, TARGET_FILE],
        capture_output=True,
    )
    return result.returncode == 0


def test_should_contain_rule_about_skill_workflow_steps():
    """AC#5: Must state that workflow steps belong in skill, not command."""
    assert _grep(r"workflow.*step.*belong.*skill"), (
        "Expected rule statement: workflow steps that belong in skill"
    )


def test_should_contain_rule_about_not_documenting_in_command():
    """AC#5: Must state not to document skill logic in command with code blocks."""
    assert _grep(r"don.t.*document.*command.*code.block"), (
        "Expected rule: don't document it in command with code blocks"
    )


def test_should_contain_complete_rule_statement():
    """AC#5: Full rule statement must be present (exact or near-exact)."""
    has_rule = (
        _grep(r"(?i)if.*workflow.*step.*belongs.*skill.*don.t.*document.*command.*code.block") or
        _grep(r"(?i)workflow.*step.*belongs.*skill.*don.t.*document.*command")
    )
    assert has_rule, (
        "Expected complete rule statement: "
        "'If workflow step belongs in skill, don't document it in command with code blocks'"
    )
