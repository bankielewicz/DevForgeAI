"""
Test: AC#3 - Subagent Invocations Registered
Story: STORY-436
Generated: 2026-02-18

Validates requirements-analyst and architect-reviewer are registered
with Task() call templates in Phase 6.
"""
import re
from pathlib import Path

import pytest

SKILL_MD = Path(__file__).resolve().parents[2] / "src" / "claude" / "skills" / "devforgeai-architecture" / "SKILL.md"


@pytest.fixture
def skill_content():
    assert SKILL_MD.exists(), f"SKILL.md not found at {SKILL_MD}"
    return SKILL_MD.read_text(encoding="utf-8")


@pytest.fixture
def phase6_section(skill_content):
    match = re.search(r"(##\s+Phase\s+6.*?)(?=\n##\s+[^#]|\Z)", skill_content, re.DOTALL)
    assert match, "Phase 6 section not found"
    return match.group(1)


class TestRequirementsAnalystRegistered:
    """requirements-analyst subagent must be registered in Phase 6.3."""

    def test_should_register_requirements_analyst(self, phase6_section):
        assert "requirements-analyst" in phase6_section, \
            "Phase 6 must reference requirements-analyst subagent"

    def test_should_have_task_call_for_requirements_analyst(self, phase6_section):
        pattern = r'Task\(.*subagent_type\s*=\s*["\']requirements-analyst["\']'
        assert re.search(pattern, phase6_section, re.DOTALL), \
            "Phase 6 must include Task() template with subagent_type='requirements-analyst'"

    def test_should_place_requirements_analyst_in_phase_6_3(self, phase6_section):
        # Find 6.3 section and verify it mentions requirements-analyst
        match = re.search(r"6\.3.*?(?=6\.4|\Z)", phase6_section, re.DOTALL)
        assert match, "Sub-phase 6.3 not found"
        assert "requirements-analyst" in match.group(0), \
            "requirements-analyst must be in Phase 6.3 (Feature Decomposition)"


class TestArchitectReviewerRegistered:
    """architect-reviewer subagent must be registered in Phase 6.4."""

    def test_should_register_architect_reviewer(self, phase6_section):
        assert "architect-reviewer" in phase6_section, \
            "Phase 6 must reference architect-reviewer subagent"

    def test_should_have_task_call_for_architect_reviewer(self, phase6_section):
        pattern = r'Task\(.*subagent_type\s*=\s*["\']architect-reviewer["\']'
        assert re.search(pattern, phase6_section, re.DOTALL), \
            "Phase 6 must include Task() template with subagent_type='architect-reviewer'"

    def test_should_place_architect_reviewer_in_phase_6_4(self, phase6_section):
        match = re.search(r"6\.4.*?(?=6\.5|\Z)", phase6_section, re.DOTALL)
        assert match, "Sub-phase 6.4 not found"
        assert "architect-reviewer" in match.group(0), \
            "architect-reviewer must be in Phase 6.4 (Technical Assessment)"


class TestTaskCallTemplates:
    """Task() call templates must include required fields."""

    def test_should_include_description_in_task_calls(self, phase6_section):
        task_calls = re.findall(r"Task\([^)]+\)", phase6_section, re.DOTALL)
        assert len(task_calls) >= 2, \
            f"Expected at least 2 Task() call templates, found {len(task_calls)}"
        for call in task_calls:
            assert "description" in call, \
                f"Task() call must include 'description' field: {call[:80]}"
