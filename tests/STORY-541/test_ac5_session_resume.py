"""
Test: AC#5 - Session Resume
Story: STORY-541
Generated: 2026-03-05

Validates:
- Detects prior session artifact
- Presents resume prompt
- BR-004: Never silently overwrites prior session
"""
import os
import re

import pytest

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
SKILL_FILE = os.path.join(PROJECT_ROOT, "src", "claude", "skills", "marketing-business", "SKILL.md")


@pytest.fixture
def skill_content():
    """Arrange: Read SKILL.md content."""
    assert os.path.isfile(SKILL_FILE), f"SKILL.md not found: {SKILL_FILE}"
    with open(SKILL_FILE, "r", encoding="utf-8") as f:
        return f.read()


class TestPriorSessionDetection:
    """Tests for prior session artifact detection."""

    def test_should_detect_prior_session_artifact(self, skill_content):
        """Act & Assert: Skill must detect prior session artifacts."""
        patterns = [
            "prior session",
            "existing session",
            "previous session",
            "session artifact",
            "session detect",
        ]
        found = any(p.lower() in skill_content.lower() for p in patterns)
        assert found, (
            "SKILL.md must describe prior session artifact detection"
        )

    def test_should_check_for_existing_output_files(self, skill_content):
        """Act & Assert: Skill must check for existing output files before writing."""
        patterns = ["exists", "check", "detect", "found", "prior"]
        found = sum(1 for p in patterns if p.lower() in skill_content.lower())
        assert found >= 2, (
            "SKILL.md must check for existing output files before writing"
        )


class TestResumePrompt:
    """Tests for resume prompt presentation."""

    def test_should_present_resume_prompt(self, skill_content):
        """Act & Assert: Skill must present resume prompt to user."""
        patterns = ["resume", "continue", "start fresh", "start over"]
        found = any(p.lower() in skill_content.lower() for p in patterns)
        assert found, (
            "SKILL.md must present resume prompt (resume/continue/start fresh)"
        )

    def test_should_show_last_completed_phase(self, skill_content):
        """Act & Assert: Skill must show last completed phase in resume prompt."""
        patterns = ["last completed", "completed phase", "last phase", "progress"]
        found = any(p.lower() in skill_content.lower() for p in patterns)
        assert found, (
            "SKILL.md must show last completed phase information in resume prompt"
        )


class TestNoSilentOverwrite:
    """Tests for BR-004: Prior session never silently overwritten."""

    def test_should_never_silently_overwrite(self, skill_content):
        """Act & Assert: Skill must never silently overwrite prior session."""
        patterns = [
            "never.*overwrite",
            "never.*silent",
            "no.*silent.*overwrite",
            "prompt.*before.*overwrite",
            "confirm.*before",
        ]
        found = any(re.search(p, skill_content, re.IGNORECASE) for p in patterns)
        assert found, (
            "SKILL.md must explicitly state that prior sessions are never silently overwritten (BR-004)"
        )

    def test_should_require_user_confirmation(self, skill_content):
        """Act & Assert: Skill must require user confirmation before modifying prior session."""
        patterns = [
            "user.*confirm",
            "user.*approv",
            "ask.*user",
            "prompt.*user",
            "AskUserQuestion",
        ]
        found = any(re.search(p, skill_content, re.IGNORECASE) for p in patterns)
        assert found, (
            "SKILL.md must require user confirmation before modifying prior session (BR-004)"
        )
