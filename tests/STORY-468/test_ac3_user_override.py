"""
Test: AC#3 - User Override Support
Story: STORY-468
Generated: 2026-03-04

Validates that src/claude/skills/coaching-entrepreneur/SKILL.md documents
override handling, logging, and immediate respect of user overrides.
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


def test_override_handling_section_documented(skill_content):
    """Arrange: SKILL.md loaded. Act: Search for override handling. Assert: Section present."""
    pattern = re.compile(r"override\s+(handling|support|logic)", re.IGNORECASE)
    assert pattern.search(skill_content), \
        "Override handling section must be documented in SKILL.md"


def test_override_logging_behavior_specified(skill_content):
    """Arrange: SKILL.md loaded. Act: Search for override logging. Assert: Logging behavior documented."""
    has_logging = (
        re.search(r"log.*override", skill_content, re.IGNORECASE)
        or re.search(r"override.*log", skill_content, re.IGNORECASE)
    )
    assert has_logging, \
        "Override logging behavior must be specified in SKILL.md"


def test_immediate_override_respect_documented(skill_content):
    """Arrange: SKILL.md loaded. Act: Search for immediate respect. Assert: Immediate behavior documented."""
    has_immediate = (
        re.search(r"immediat.*override", skill_content, re.IGNORECASE)
        or re.search(r"override.*immediat", skill_content, re.IGNORECASE)
        or re.search(r"respect.*override", skill_content, re.IGNORECASE)
        or re.search(r"override.*respect", skill_content, re.IGNORECASE)
    )
    assert has_immediate, \
        "Immediate respect of user overrides must be documented in SKILL.md"
