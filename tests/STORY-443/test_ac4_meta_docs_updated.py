"""AC#4: CLAUDE.md and Memory Files Updated.

Tests that CLAUDE.md and skills-reference.md (in both src/ and .claude/) use new skill names:
  (a) No Skill(command="devforgeai-brainstorming") invocations
  (b) No Skill(command="devforgeai-development") invocations
  (c) No devforgeai-brainstorming as a current skill catalog entry
  (d) No devforgeai-development listed as active skill in catalog
  (e) skills-reference.md skill count summary uses new names
  (f) CLAUDE.md Key Entry Points table uses new skill names

All tests MUST FAIL before implementation (TDD Red phase).
Story: STORY-443
"""
import os

from conftest import SRC_SKILLS_REF, OPS_SKILLS_REF, CLAUDE_MD, PROJECT_ROOT


def _read_src_skills_ref() -> str:
    with open(SRC_SKILLS_REF, encoding="utf-8") as f:
        return f.read()


def _read_ops_skills_ref() -> str:
    with open(OPS_SKILLS_REF, encoding="utf-8") as f:
        return f.read()


def _read_claude_md() -> str:
    with open(CLAUDE_MD, encoding="utf-8") as f:
        return f.read()


class TestAC4SkillsReferenceNoOldInvocations:
    """Verify skills-reference.md (src/) does not show old skill invocations."""

    def test_should_not_have_skill_command_devforgeai_brainstorming_when_updated(self):
        """Skill(command="devforgeai-brainstorming") must not appear in src skills-reference."""
        content = _read_src_skills_ref()
        assert 'Skill(command="devforgeai-brainstorming")' not in content, (
            'src/claude/memory/skills-reference.md must not contain '
            'Skill(command="devforgeai-brainstorming")'
        )

    def test_should_not_have_skill_command_devforgeai_development_when_updated(self):
        """Skill(command="devforgeai-development") must not appear in src skills-reference."""
        content = _read_src_skills_ref()
        assert 'Skill(command="devforgeai-development")' not in content, (
            'src/claude/memory/skills-reference.md must not contain '
            'Skill(command="devforgeai-development")'
        )

    def test_should_not_have_skill_command_devforgeai_ideation_when_updated(self):
        """Skill(command="devforgeai-ideation") must not appear in src skills-reference."""
        content = _read_src_skills_ref()
        assert 'Skill(command="devforgeai-ideation")' not in content, (
            'src/claude/memory/skills-reference.md must not contain '
            'Skill(command="devforgeai-ideation")'
        )


class TestAC4SkillsReferenceCatalogUsesNewNames:
    """Verify the skill catalog section in src/skills-reference.md uses new names."""

    def test_should_have_brainstorming_section_header_not_devforgeai_brainstorming_when_updated(self):
        """The brainstorming skill section must use the new name 'brainstorming'."""
        content = _read_src_skills_ref()
        # The section header should be '### brainstorming' not '### devforgeai-brainstorming'
        assert "### brainstorming\n" in content or "### brainstorming\r\n" in content or "\n### brainstorming\n" in content, (
            "skills-reference.md must have a '### brainstorming' section header for the brainstorming skill"
        )

    def test_should_not_have_devforgeai_development_section_header_when_updated(self):
        """There must be no '### devforgeai-development' section header."""
        content = _read_src_skills_ref()
        assert "### devforgeai-development\n" not in content and "### devforgeai-development\r\n" not in content, (
            "skills-reference.md must not have a '### devforgeai-development' section header"
        )

    def test_should_have_implementing_stories_section_header_when_updated(self):
        """The development skill section must use the new name 'implementing-stories'."""
        content = _read_src_skills_ref()
        assert "### implementing-stories\n" in content or "### implementing-stories\r\n" in content, (
            "skills-reference.md must have a '### implementing-stories' section header"
        )

    def test_should_not_have_old_skill_count_referencing_devforgeai_prefix_when_updated(self):
        """The Skill Count Summary must not describe devforgeai-brainstorming/ideation/development."""
        content = _read_src_skills_ref()
        # Find the Skill Count Summary section
        summary_start = content.find("## Skill Count Summary")
        if summary_start != -1:
            summary_section = content[summary_start:summary_start + 600]
            # The old summary listed: 'devforgeai-* (15): brainstorming, ideation, ..., development'
            # The new summary must not list those old names as current skills
            assert "devforgeai-brainstorming" not in summary_section, (
                "Skill Count Summary must not reference devforgeai-brainstorming"
            )
            assert "devforgeai-ideation" not in summary_section, (
                "Skill Count Summary must not reference devforgeai-ideation"
            )
            assert ", development," not in summary_section, (
                "Skill Count Summary must not list 'development' as devforgeai-* skill name"
            )

    def test_should_have_workflow_sequence_using_brainstorming_not_devforgeai_brainstorming_when_updated(self):
        """Workflow sequence section must use 'brainstorming' not 'devforgeai-brainstorming'."""
        content = _read_src_skills_ref()
        workflow_start = content.find("## Workflow Sequences")
        if workflow_start != -1:
            workflow_section = content[workflow_start:workflow_start + 1000]
            assert "devforgeai-brainstorming" not in workflow_section, (
                "Workflow Sequences section must not reference devforgeai-brainstorming"
            )


class TestAC4OpsSkillsReferenceNoOldInvocations:
    """Verify .claude/memory/skills-reference.md (operational copy) also uses new names."""

    def test_should_not_have_skill_command_devforgeai_brainstorming_in_ops_copy_when_updated(self):
        """Skill(command="devforgeai-brainstorming") must not appear in .claude/memory copy."""
        content = _read_ops_skills_ref()
        assert 'Skill(command="devforgeai-brainstorming")' not in content, (
            '.claude/memory/skills-reference.md must not contain '
            'Skill(command="devforgeai-brainstorming")'
        )

    def test_should_not_have_skill_command_devforgeai_development_in_ops_copy_when_updated(self):
        """Skill(command="devforgeai-development") must not appear in .claude/memory copy."""
        content = _read_ops_skills_ref()
        assert 'Skill(command="devforgeai-development")' not in content, (
            '.claude/memory/skills-reference.md must not contain '
            'Skill(command="devforgeai-development")'
        )


class TestAC4ClaudeMdMetaDocsUpdated:
    """Verify CLAUDE.md root file uses new skill names."""

    def test_should_not_have_devforgeai_brainstorming_as_current_skill_in_claudemd_when_updated(self):
        """CLAUDE.md must not list devforgeai-brainstorming as a current skill name."""
        content = _read_claude_md()
        # devforgeai-brainstorming should not appear in CLAUDE.md as an active skill reference
        # (Historical context in subagent registry or change log is acceptable)
        # The Development Workflow and Commands sections must use the new name
        # Check the Key Entry Points table and Workflow section specifically
        key_entry_start = content.find("## Key Entry Points")
        if key_entry_start == -1:
            key_entry_start = content.find("Key Entry Points")
        if key_entry_start != -1:
            next_section = content.find("##", key_entry_start + 3)
            key_section = content[key_entry_start:next_section] if next_section != -1 else content[key_entry_start:]
            assert "devforgeai-brainstorming" not in key_section, (
                "CLAUDE.md Key Entry Points section must not reference devforgeai-brainstorming"
            )

    def test_should_not_have_devforgeai_development_as_dev_workflow_skill_in_claudemd_when_updated(self):
        """CLAUDE.md Development Workflow section must not cite devforgeai-development."""
        content = _read_claude_md()
        # Find the Workflow section
        workflow_start = content.find("## Workflow")
        if workflow_start != -1:
            next_section = content.find("##", workflow_start + 3)
            workflow_section = content[workflow_start:next_section] if next_section != -1 else content[workflow_start:]
            assert "devforgeai-development" not in workflow_section, (
                "CLAUDE.md Workflow section must not reference devforgeai-development"
            )

    def test_should_not_invoke_skill_devforgeai_brainstorming_anywhere_in_claudemd_when_updated(self):
        """CLAUDE.md must not contain Skill(command="devforgeai-brainstorming")."""
        content = _read_claude_md()
        assert 'Skill(command="devforgeai-brainstorming")' not in content, (
            'CLAUDE.md must not contain Skill(command="devforgeai-brainstorming")'
        )

    def test_should_not_invoke_skill_devforgeai_development_anywhere_in_claudemd_when_updated(self):
        """CLAUDE.md must not contain Skill(command="devforgeai-development")."""
        content = _read_claude_md()
        assert 'Skill(command="devforgeai-development")' not in content, (
            'CLAUDE.md must not contain Skill(command="devforgeai-development")'
        )
