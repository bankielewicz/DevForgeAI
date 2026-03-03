"""
Test: AC#3 - Why This Fails Explanation Included
Story: STORY-411
Generated: 2026-02-16

Validates that explanation references Claude's instruction-following behavior
and RCA-037/038 as evidence.
"""
import subprocess
import pytest

TARGET_FILE = "devforgeai/protocols/lean-orchestration-pattern.md"


def _grep(pattern: str) -> bool:
    result = subprocess.run(
        ["grep", "-qP", pattern, TARGET_FILE],
        capture_output=True,
    )
    return result.returncode == 0


def test_should_reference_rca_037_when_explaining_why_fails():
    """AC#3: Explanation must reference RCA-037."""
    assert _grep(r"RCA-037"), (
        f"Expected reference to RCA-037 in {TARGET_FILE}"
    )


def test_should_reference_rca_038_when_explaining_why_fails():
    """AC#3: Explanation must reference RCA-038."""
    assert _grep(r"RCA-038"), (
        f"Expected reference to RCA-038 in {TARGET_FILE}"
    )


def test_should_reference_instruction_following_behavior():
    """AC#3: Must explain Claude's instruction-following behavior as root cause."""
    assert _grep(r"(?i)instruction.follow"), (
        "Expected explanation referencing Claude's instruction-following behavior"
    )
