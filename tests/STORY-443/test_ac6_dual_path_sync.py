"""AC#6: Dual-Path Sync Verified.

Tests that src/claude/memory/ and .claude/memory/ are consistent in skill names:
  (a) Both files reference the same new skill names
  (b) Neither file references old devforgeai-brainstorming/ideation/development as current
  (c) The skill catalog in both files is consistent

Story: STORY-443
All tests MUST FAIL before implementation (TDD Red phase).
"""
import os

from conftest import (
    SRC_SKILLS_REF,
    OPS_SKILLS_REF,
    PROJECT_ROOT,
)

# Old skill names that must be absent from both copies
OLD_SKILL_INVOCATIONS = [
    'Skill(command="devforgeai-brainstorming")',
    'Skill(command="devforgeai-development")',
    'Skill(command="devforgeai-ideation")',
]

# New skill invocations that must be present in both copies
NEW_SKILL_INVOCATIONS = [
    'Skill(command="brainstorming")',
    'Skill(command="implementing-stories")',
    'Skill(command="discovering-requirements")',
]


def _read_src() -> str:
    with open(SRC_SKILLS_REF, encoding="utf-8") as f:
        return f.read()


def _read_ops() -> str:
    with open(OPS_SKILLS_REF, encoding="utf-8") as f:
        return f.read()


class TestAC6BothCopiesHaveNoOldInvocations:
    """Both src/ and .claude/ skills-reference.md must not have old Skill() invocations."""

    def test_should_not_have_devforgeai_brainstorming_invocation_in_src_copy_when_synced(self):
        content = _read_src()
        assert 'Skill(command="devforgeai-brainstorming")' not in content, (
            'src/claude/memory/skills-reference.md must not have '
            'Skill(command="devforgeai-brainstorming")'
        )

    def test_should_not_have_devforgeai_brainstorming_invocation_in_ops_copy_when_synced(self):
        content = _read_ops()
        assert 'Skill(command="devforgeai-brainstorming")' not in content, (
            '.claude/memory/skills-reference.md must not have '
            'Skill(command="devforgeai-brainstorming")'
        )

    def test_should_not_have_devforgeai_development_invocation_in_src_copy_when_synced(self):
        content = _read_src()
        assert 'Skill(command="devforgeai-development")' not in content, (
            'src/claude/memory/skills-reference.md must not have '
            'Skill(command="devforgeai-development")'
        )

    def test_should_not_have_devforgeai_development_invocation_in_ops_copy_when_synced(self):
        content = _read_ops()
        assert 'Skill(command="devforgeai-development")' not in content, (
            '.claude/memory/skills-reference.md must not have '
            'Skill(command="devforgeai-development")'
        )

    def test_should_not_have_devforgeai_ideation_invocation_in_src_copy_when_synced(self):
        content = _read_src()
        assert 'Skill(command="devforgeai-ideation")' not in content, (
            'src/claude/memory/skills-reference.md must not have '
            'Skill(command="devforgeai-ideation")'
        )

    def test_should_not_have_devforgeai_ideation_invocation_in_ops_copy_when_synced(self):
        content = _read_ops()
        assert 'Skill(command="devforgeai-ideation")' not in content, (
            '.claude/memory/skills-reference.md must not have '
            'Skill(command="devforgeai-ideation")'
        )


class TestAC6BothCopiesHaveNewInvocations:
    """Both src/ and .claude/ skills-reference.md must use new Skill() invocations."""

    def test_should_have_brainstorming_invocation_in_src_copy_when_synced(self):
        content = _read_src()
        assert 'Skill(command="brainstorming")' in content, (
            'src/claude/memory/skills-reference.md must have Skill(command="brainstorming")'
        )

    def test_should_have_brainstorming_invocation_in_ops_copy_when_synced(self):
        content = _read_ops()
        assert 'Skill(command="brainstorming")' in content, (
            '.claude/memory/skills-reference.md must have Skill(command="brainstorming")'
        )

    def test_should_have_implementing_stories_invocation_in_src_copy_when_synced(self):
        content = _read_src()
        assert 'Skill(command="implementing-stories")' in content, (
            'src/claude/memory/skills-reference.md must have Skill(command="implementing-stories")'
        )

    def test_should_have_implementing_stories_invocation_in_ops_copy_when_synced(self):
        content = _read_ops()
        assert 'Skill(command="implementing-stories")' in content, (
            '.claude/memory/skills-reference.md must have Skill(command="implementing-stories")'
        )

    def test_should_have_discovering_requirements_invocation_in_src_copy_when_synced(self):
        content = _read_src()
        assert 'Skill(command="discovering-requirements")' in content, (
            'src/claude/memory/skills-reference.md must have Skill(command="discovering-requirements")'
        )

    def test_should_have_discovering_requirements_invocation_in_ops_copy_when_synced(self):
        content = _read_ops()
        assert 'Skill(command="discovering-requirements")' in content, (
            '.claude/memory/skills-reference.md must have Skill(command="discovering-requirements")'
        )


class TestAC6BothCopiesConsistent:
    """src/ and .claude/ copies must be consistent in skill name usage."""

    def test_should_have_same_brainstorming_section_presence_in_both_copies_when_synced(self):
        """Both copies must have the '### brainstorming' section."""
        src_content = _read_src()
        ops_content = _read_ops()
        src_has = "### brainstorming" in src_content
        ops_has = "### brainstorming" in ops_content
        assert src_has == ops_has, (
            f"Inconsistency: src/ has '### brainstorming': {src_has}, "
            f".claude/ has '### brainstorming': {ops_has}"
        )
        assert src_has, "Both copies must have '### brainstorming' section"

    def test_should_have_same_implementing_stories_section_presence_in_both_copies_when_synced(self):
        """Both copies must have '### implementing-stories' section."""
        src_content = _read_src()
        ops_content = _read_ops()
        src_has = "### implementing-stories" in src_content
        ops_has = "### implementing-stories" in ops_content
        assert src_has == ops_has, (
            f"Inconsistency: src/ has '### implementing-stories': {src_has}, "
            f".claude/ has '### implementing-stories': {ops_has}"
        )
        assert src_has, "Both copies must have '### implementing-stories' section"

    def test_should_have_same_discovering_requirements_section_presence_in_both_copies_when_synced(self):
        """Both copies must have '### discovering-requirements' section."""
        src_content = _read_src()
        ops_content = _read_ops()
        src_has = "### discovering-requirements" in src_content
        ops_has = "### discovering-requirements" in ops_content
        assert src_has == ops_has, (
            f"Inconsistency: src/ has '### discovering-requirements': {src_has}, "
            f".claude/ has '### discovering-requirements': {ops_has}"
        )
        assert src_has, "Both copies must have '### discovering-requirements' section"

    def test_should_have_same_old_devforgeai_brainstorming_absence_in_both_copies_when_synced(self):
        """devforgeai-brainstorming invocation must be absent from both copies."""
        src_content = _read_src()
        ops_content = _read_ops()
        src_absent = 'Skill(command="devforgeai-brainstorming")' not in src_content
        ops_absent = 'Skill(command="devforgeai-brainstorming")' not in ops_content
        assert src_absent and ops_absent, (
            f"devforgeai-brainstorming invocation found: "
            f"in src/: {not src_absent}, in .claude/: {not ops_absent}"
        )

    def test_should_have_same_old_devforgeai_development_absence_in_both_copies_when_synced(self):
        """devforgeai-development invocation must be absent from both copies."""
        src_content = _read_src()
        ops_content = _read_ops()
        src_absent = 'Skill(command="devforgeai-development")' not in src_content
        ops_absent = 'Skill(command="devforgeai-development")' not in ops_content
        assert src_absent and ops_absent, (
            f"devforgeai-development invocation found: "
            f"in src/: {not src_absent}, in .claude/: {not ops_absent}"
        )
