"""
Test: AC#1 - Session Log Persistence
Story: STORY-468
Generated: 2026-03-04

Validates that src/claude/skills/coaching-entrepreneur/SKILL.md documents
the session log schema with emotional state enum, date, outcomes, overrides,
and YAML path.
"""
import os
import pytest

PROJECT_ROOT = "/mnt/c/Projects/DevForgeAI2"
SKILL_FILE = os.path.join(PROJECT_ROOT, "src/claude/skills/coaching-entrepreneur/SKILL.md")


@pytest.fixture
def skill_content():
    with open(SKILL_FILE, "r") as f:
        return f.read()


def test_session_log_section_exists(skill_content):
    """Arrange: SKILL.md content loaded. Act: Search for session log section. Assert: Section header present."""
    assert "session log" in skill_content.lower() or "Session Log" in skill_content, \
        "SKILL.md must contain a session log section"


def test_emotional_state_enum_documented(skill_content):
    """Arrange: SKILL.md content loaded. Act: Check enum values. Assert: All 7 enum values present."""
    required_states = ["energized", "focused", "neutral", "tired", "frustrated", "anxious", "overwhelmed"]
    for state in required_states:
        assert state in skill_content, \
            f"Emotional state enum value '{state}' must be documented in SKILL.md"


def test_session_date_field_documented(skill_content):
    """Arrange: SKILL.md content loaded. Act: Search for date field in schema. Assert: Session date field present."""
    import re
    pattern = re.compile(r"session.*date.*field|date.*DateTime|sessions\[\]\.date", re.IGNORECASE)
    assert pattern.search(skill_content), \
        "Session date field must be documented in session log schema in SKILL.md"


def test_session_outcomes_tracking_documented(skill_content):
    """Arrange: SKILL.md content loaded. Act: Search for outcomes. Assert: Outcomes tracking present."""
    assert "outcomes" in skill_content.lower(), \
        "Session outcomes tracking must be documented in SKILL.md"


def test_user_override_field_documented(skill_content):
    """Arrange: SKILL.md content loaded. Act: Search for override field. Assert: Override field in schema."""
    assert "override" in skill_content.lower(), \
        "User override field must be documented in session log schema"


def test_session_log_yaml_path_specified(skill_content):
    """Arrange: SKILL.md content loaded. Act: Search for YAML path. Assert: Correct path present."""
    assert "devforgeai/specs/business/coaching/session-log.yaml" in skill_content, \
        "Session log YAML path must be specified as devforgeai/specs/business/coaching/session-log.yaml"
