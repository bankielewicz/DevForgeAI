"""
Test: AC#2 - Tone Adaptation on Session Start
Story: STORY-468
Generated: 2026-03-04

Validates that src/claude/skills/coaching-entrepreneur/SKILL.md documents
previous session read logic and tone adaptation examples.
"""
import os
import re
import pytest

PROJECT_ROOT = "/mnt/c/Projects/DevForgeAI2"
SKILL_FILE = os.path.join(PROJECT_ROOT, "src/claude/skills/coaching-entrepreneur/SKILL.md")


@pytest.fixture
def skill_content():
    with open(SKILL_FILE, "r") as f:
        return f.read()


def test_tone_adaptation_section_exists(skill_content):
    """Arrange: SKILL.md loaded. Act: Search for tone adaptation section. Assert: Section present."""
    pattern = re.compile(r"tone\s+adaptation", re.IGNORECASE)
    assert pattern.search(skill_content), \
        "SKILL.md must contain a tone adaptation section"


def test_previous_session_read_logic_documented(skill_content):
    """Arrange: SKILL.md loaded. Act: Search for previous session read logic. Assert: Read logic present."""
    has_read_logic = (
        "previous session" in skill_content.lower()
        or "read.*session" in skill_content.lower()
        or "session-log.yaml" in skill_content
    )
    assert has_read_logic, \
        "Previous session read logic must be documented in SKILL.md"


def test_tone_adaptation_examples_provided(skill_content):
    """Arrange: SKILL.md loaded. Act: Count tone adaptation examples. Assert: At least 2 examples."""
    # Look for quoted examples like the ones in the AC
    example_patterns = [
        r"['\"].*frustrated.*['\"]",
        r"['\"].*momentum.*['\"]",
        r"['\"].*energized.*['\"]",
        r"['\"].*tired.*['\"]",
        r"['\"].*anxious.*['\"]",
        r"['\"].*overwhelmed.*['\"]",
        r"['\"].*focused.*['\"]",
        r"['\"].*neutral.*['\"]",
    ]
    example_count = sum(1 for p in example_patterns if re.search(p, skill_content, re.IGNORECASE))
    assert example_count >= 2, \
        f"At least 2 tone adaptation examples required, found {example_count}"
