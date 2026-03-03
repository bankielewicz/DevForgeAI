"""
Test: AC#4 - Retained Phases Still Functional (Regression Guard)
Story: STORY-437
TDD Phase: RED - All tests should FAIL before implementation.

Verifies all 11 retained phases are present with correct headers,
and that Sprint Planning, Story Management, and Audit Deferrals modes
are still listed. Quality Gate Enforcement section must be unchanged.
"""
import pytest


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


class TestRetainedPhasesPresent:
    """Verify all 11 retained phases are present with headers."""

    @pytest.mark.parametrize("phase_id,phase_name", RETAINED_PHASES)
    def test_should_contain_phase_header_when_skill_read(self, skill_md_content, phase_id, phase_name):
        """Each retained phase header must be present."""
        assert phase_id in skill_md_content, (
            f"Retained {phase_id} ({phase_name}) missing from SKILL.md"
        )

    def test_should_have_exactly_11_retained_phases_when_skill_read(self, skill_md_content):
        """All 11 retained phases must be present, no Phase 4A."""
        for phase_id, _ in RETAINED_PHASES:
            assert phase_id in skill_md_content, f"Missing {phase_id}"
        assert "Phase 4A" not in skill_md_content, "Phase 4A should be removed"


class TestModesStillListed:
    """Verify Sprint Planning, Story Management, and Audit Deferrals modes listed."""

    def test_should_list_sprint_planning_mode_when_skill_read(self, skill_md_content):
        """Sprint Planning Mode must be listed."""
        assert "Sprint Planning" in skill_md_content, (
            "Sprint Planning mode missing from SKILL.md"
        )

    def test_should_list_story_management_mode_when_skill_read(self, skill_md_content):
        """Story Management Mode must be listed as default."""
        assert "Story Management" in skill_md_content, (
            "Story Management mode missing from SKILL.md"
        )

    def test_should_list_audit_deferrals_mode_when_skill_read(self, skill_md_content):
        """Audit Deferrals Mode must be listed."""
        assert "Audit Deferrals" in skill_md_content, (
            "Audit Deferrals mode missing from SKILL.md"
        )


class TestQualityGateEnforcement:
    """Verify Quality Gate Enforcement section unchanged."""

    def test_should_contain_quality_gate_enforcement_when_skill_read(self, skill_md_content):
        """Quality Gate Enforcement section must be present."""
        assert "Quality Gate" in skill_md_content, (
            "Quality Gate Enforcement section missing from SKILL.md"
        )

    def test_should_contain_context_markers_for_retained_modes_when_skill_read(self, skill_md_content):
        """Context markers for create-sprint, audit-deferrals must remain."""
        assert "create-sprint" in skill_md_content, (
            "create-sprint context marker missing"
        )
        assert "audit-deferrals" in skill_md_content, (
            "audit-deferrals context marker missing"
        )
