"""
Test: AC#1 - Phase 4A Removed from SKILL.md
Story: STORY-437
TDD Phase: RED - All tests should FAIL before implementation.

Verifies that Phase 4A (Epic Creation) content is removed from
the orchestration SKILL.md while all retained phases remain intact.
"""
import re
import pytest


class TestPhase4AHeaderRemoved:
    """Verify no Phase 4A header exists in SKILL.md."""

    def test_should_not_contain_phase_4a_header_when_skill_read(self, skill_md_content):
        """Phase 4A header must not exist."""
        assert "Phase 4A" not in skill_md_content, (
            "SKILL.md still contains 'Phase 4A' header"
        )

    def test_should_not_contain_phase_4a_epic_creation_when_skill_read(self, skill_md_content):
        """Phase 4A: Epic Creation must not exist."""
        assert "Epic Creation" not in skill_md_content, (
            "SKILL.md still contains 'Epic Creation' reference"
        )


class TestPhase4A9ImplementationRemoved:
    """Verify Phase 4A.9 detailed implementation section is removed."""

    def test_should_not_contain_phase_4a9_when_skill_read(self, skill_md_content):
        """Phase 4A.9 implementation section must be removed."""
        assert "4A.9" not in skill_md_content, (
            "SKILL.md still contains Phase 4A.9 implementation section"
        )


class TestEpicManagementReferenceRemoved:
    """Verify 'Epic Management (6 files)' reference section is removed."""

    def test_should_not_contain_epic_management_reference_when_skill_read(self, skill_md_content):
        """Epic Management reference section must be removed."""
        assert "Epic Management" not in skill_md_content, (
            "SKILL.md still contains 'Epic Management' reference section"
        )


class TestYAMLFrontmatterUpdated:
    """Verify YAML frontmatter description no longer mentions 'starting epics'."""

    def test_should_not_mention_starting_epics_in_description_when_skill_read(self, skill_md_content):
        """YAML description must not mention 'starting epics'."""
        # Extract YAML frontmatter (between --- markers)
        match = re.search(r"^---\n(.*?)\n---", skill_md_content, re.DOTALL)
        assert match is not None, "No YAML frontmatter found"
        frontmatter = match.group(1)
        assert "starting epics" not in frontmatter.lower(), (
            "YAML frontmatter still mentions 'starting epics'"
        )


class TestWhenToUseSectionUpdated:
    """Verify 'When to Use' section doesn't list 'Starting a new epic'."""

    def test_should_not_list_starting_new_epic_when_skill_read(self, skill_md_content):
        """'Starting a new epic' must not appear in When to Use section."""
        assert "Starting a new epic" not in skill_md_content, (
            "SKILL.md still lists 'Starting a new epic' in When to Use"
        )


class TestContextMarkersUpdated:
    """Verify context markers no longer include 'create-epic'."""

    def test_should_not_contain_create_epic_context_marker_when_skill_read(self, skill_md_content):
        """create-epic context marker must be removed."""
        assert "create-epic" not in skill_md_content, (
            "SKILL.md still contains 'create-epic' context marker"
        )


class TestModeCountUpdated:
    """Verify mode count updated from 5 to 4."""

    def test_should_show_4_modes_not_5_when_skill_read(self, skill_md_content):
        """Mode count must be 4, not 5."""
        # Should NOT contain "5 modes"
        assert "5 modes" not in skill_md_content, (
            "SKILL.md still references '5 modes'"
        )
        # Should contain "4 modes"
        assert "4 modes" in skill_md_content or "four modes" in skill_md_content.lower(), (
            "SKILL.md does not reference '4 modes'"
        )


class TestRetainedPhasesIntact:
    """Verify all 11 retained phases remain intact."""

    RETAINED_PHASES = [
        ("Phase 0", "Checkpoint Detection"),
        ("Phase 1", "Story Validation"),
        ("Phase 2", "Skill Invocation"),
        ("Phase 3", "Sprint Planning"),
        ("Phase 3A", "Story Status Update"),
        ("Phase 3.5", "QA Retry"),
        ("Phase 4.5", "Deferred Work Tracking"),
        ("Phase 5", "Next Action"),
        ("Phase 6", "Finalization"),
        ("Phase 7", "Audit Deferrals"),
        ("Phase 7A", "Sprint Retrospective"),
    ]

    @pytest.mark.parametrize("phase_id,phase_name", RETAINED_PHASES)
    def test_should_contain_retained_phase_when_skill_read(self, skill_md_content, phase_id, phase_name):
        """Each retained phase must still be present."""
        assert phase_id in skill_md_content, (
            f"SKILL.md is missing retained {phase_id}"
        )
