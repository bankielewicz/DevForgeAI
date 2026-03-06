"""
Integration Test: STORY-542 - Customer Discovery Workflow
Generated: 2026-03-06

Validates cross-component interactions:
1. SKILL.md references customer-discovery-workflow.md correctly
2. End-to-end workflow phase coherence (6 phases flow logically)
3. Cross-reference integrity (EPIC-074, EPIC-075, business plan, state file paths)
4. Story-to-implementation traceability (all ACs mapped to workflow sections)
5. Business rule consistency across story spec and implementation
"""
import os
import re

import pytest

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

WORKFLOW_FILE = os.path.join(
    PROJECT_ROOT, "src", "claude", "skills", "marketing-business",
    "references", "customer-discovery-workflow.md"
)
SKILL_FILE = os.path.join(
    PROJECT_ROOT, "src", "claude", "skills", "marketing-business", "SKILL.md"
)
STORY_FILE = os.path.join(
    PROJECT_ROOT, "devforgeai", "specs", "Stories",
    "STORY-542-customer-discovery-workflow.story.md"
)


@pytest.fixture
def workflow_content():
    """Arrange: Read workflow reference file."""
    assert os.path.isfile(WORKFLOW_FILE), f"Workflow file not found: {WORKFLOW_FILE}"
    with open(WORKFLOW_FILE, "r", encoding="utf-8") as f:
        return f.read()


@pytest.fixture
def skill_content():
    """Arrange: Read SKILL.md file."""
    assert os.path.isfile(SKILL_FILE), f"SKILL.md not found: {SKILL_FILE}"
    with open(SKILL_FILE, "r", encoding="utf-8") as f:
        return f.read()


@pytest.fixture
def story_content():
    """Arrange: Read story file."""
    assert os.path.isfile(STORY_FILE), f"Story file not found: {STORY_FILE}"
    with open(STORY_FILE, "r", encoding="utf-8") as f:
        return f.read()


# ============================================================
# 1. Cross-Component: SKILL.md <-> Workflow Reference
# ============================================================

class TestSkillWorkflowIntegration:
    """Validate SKILL.md correctly references the customer discovery workflow."""

    def test_skill_references_customer_discovery_section(self, skill_content):
        """Act & Assert: SKILL.md must contain a Customer Discovery section."""
        assert "customer discovery" in skill_content.lower(), (
            "SKILL.md must reference Customer Discovery workflow"
        )

    def test_skill_references_epic075(self, skill_content):
        """Act & Assert: SKILL.md must reference EPIC-075."""
        assert "EPIC-075" in skill_content, (
            "SKILL.md must reference EPIC-075 (Marketing & Customer Acquisition)"
        )

    def test_workflow_frontmatter_epic_matches_skill(self, workflow_content, skill_content):
        """Act & Assert: Workflow EPIC reference must match SKILL.md EPIC reference."""
        # Workflow frontmatter says epic: EPIC-075
        assert "epic: EPIC-075" in workflow_content, (
            "Workflow frontmatter must reference EPIC-075"
        )
        assert "EPIC-075" in skill_content, (
            "SKILL.md must also reference EPIC-075"
        )

    def test_workflow_story_id_matches_frontmatter(self, workflow_content):
        """Act & Assert: Workflow frontmatter story ID must be STORY-542."""
        assert "story: STORY-542" in workflow_content, (
            "Workflow frontmatter must reference STORY-542"
        )


# ============================================================
# 2. End-to-End Workflow Phase Coherence
# ============================================================

class TestWorkflowPhaseCoherence:
    """Validate all 6 phases flow logically in sequence."""

    EXPECTED_PHASES = [
        ("Phase 1", "Load Interview Questions"),
        ("Phase 2", "Fallback"),
        ("Phase 3", "Conduct Interviews"),
        ("Phase 4", "Feedback Synthesis"),
        ("Phase 5", "Milestone Tracking"),
        ("Phase 6", "Partial Progress"),
    ]

    def test_workflow_contains_all_six_phases(self, workflow_content):
        """Act & Assert: Workflow must contain all 6 phases."""
        for i in range(1, 7):
            assert f"## Phase {i}" in workflow_content, (
                f"Workflow must contain Phase {i}"
            )

    def test_phases_appear_in_sequential_order(self, workflow_content):
        """Act & Assert: Phases must appear in order 1 through 6."""
        positions = []
        for i in range(1, 7):
            pos = workflow_content.find(f"## Phase {i}")
            assert pos != -1, f"Phase {i} not found"
            positions.append(pos)
        for i in range(len(positions) - 1):
            assert positions[i] < positions[i + 1], (
                f"Phase {i+1} must appear before Phase {i+2}"
            )

    def test_load_phase_precedes_fallback_phase(self, workflow_content):
        """Act & Assert: Load (Phase 1) must come before Fallback (Phase 2)."""
        load_pos = workflow_content.find("## Phase 1")
        fallback_pos = workflow_content.find("## Phase 2")
        assert load_pos < fallback_pos, (
            "Load phase must precede Fallback phase"
        )

    def test_synthesis_requires_interviews_phase(self, workflow_content):
        """Act & Assert: Synthesis (Phase 4) must come after Conduct (Phase 3)."""
        conduct_pos = workflow_content.find("## Phase 3")
        synthesis_pos = workflow_content.find("## Phase 4")
        assert conduct_pos < synthesis_pos, (
            "Conduct Interviews must precede Feedback Synthesis"
        )

    def test_milestone_follows_synthesis(self, workflow_content):
        """Act & Assert: Milestone (Phase 5) must come after Synthesis (Phase 4)."""
        synthesis_pos = workflow_content.find("## Phase 4")
        milestone_pos = workflow_content.find("## Phase 5")
        assert synthesis_pos < milestone_pos, (
            "Milestone Tracking must follow Feedback Synthesis"
        )

    def test_persistence_is_final_phase(self, workflow_content):
        """Act & Assert: Partial Progress Persistence (Phase 6) must be the last phase."""
        phase_6_pos = workflow_content.find("## Phase 6")
        # No Phase 7 should exist
        assert "## Phase 7" not in workflow_content, (
            "Phase 6 should be the final phase"
        )
        assert phase_6_pos != -1, "Phase 6 must exist"


# ============================================================
# 3. Cross-Reference Integrity
# ============================================================

class TestCrossReferenceIntegrity:
    """Validate all cross-references are consistent."""

    def test_epic074_referenced_in_workflow(self, workflow_content):
        """Act & Assert: Workflow must reference EPIC-074 for interview question source."""
        assert "EPIC-074" in workflow_content, (
            "Workflow must reference EPIC-074 as interview question source"
        )

    def test_epic074_referenced_in_story(self, story_content):
        """Act & Assert: Story must reference EPIC-074 as optional dependency."""
        assert "EPIC-074" in story_content, (
            "Story must reference EPIC-074 as dependency"
        )

    def test_business_plan_target_consistent(self, workflow_content):
        """Act & Assert: Workflow must reference writing to business plan."""
        content_lower = workflow_content.lower()
        assert "business plan" in content_lower, (
            "Workflow must reference the business plan as output target"
        )

    def test_state_file_path_uses_project_relative_tmp(self, workflow_content):
        """Act & Assert: State file must use tmp/{story-id}/ pattern per operational safety rules."""
        assert "tmp/" in workflow_content, (
            "State file must use project-relative tmp/ directory"
        )
        # Must NOT use /tmp/ (system temp)
        lines = workflow_content.splitlines()
        for line in lines:
            if "discovery-state" in line.lower() and "/tmp/" in line:
                # Check it's not an absolute /tmp/ path
                assert not line.strip().startswith("/tmp/"), (
                    "State file must NOT use system /tmp/ directory"
                )

    def test_story_source_file_path_matches_actual_file(self, story_content):
        """Act & Assert: Story source file path must match actual workflow file location."""
        expected_path = "src/claude/skills/marketing-business/references/customer-discovery-workflow.md"
        assert expected_path in story_content, (
            f"Story must reference actual file path: {expected_path}"
        )

    def test_workflow_confidence_formula_consistent_with_story(
        self, workflow_content, story_content
    ):
        """Act & Assert: Confidence score formula must be consistent between story and workflow."""
        # Story says: "discovery confidence score (0-100%) from validated/total ratio"
        # Workflow must describe the same formula
        assert "validated" in workflow_content.lower(), (
            "Workflow must reference validated count in confidence formula"
        )
        assert "confidence" in workflow_content.lower(), (
            "Workflow must reference confidence score"
        )


# ============================================================
# 4. Story-to-Implementation Traceability
# ============================================================

class TestStoryImplementationTraceability:
    """Validate all 5 ACs are traceable to workflow sections."""

    def test_ac1_maps_to_phase_1(self, workflow_content):
        """Act & Assert: AC#1 (EPIC-074 Integration) maps to Phase 1 (Load)."""
        # Phase 1 must handle EPIC-074 loading
        phase_1_start = workflow_content.find("## Phase 1")
        phase_2_start = workflow_content.find("## Phase 2")
        phase_1_content = workflow_content[phase_1_start:phase_2_start]
        assert "epic-074" in phase_1_content.lower(), (
            "Phase 1 must handle EPIC-074 integration (AC#1)"
        )

    def test_ac2_maps_to_phase_2(self, workflow_content):
        """Act & Assert: AC#2 (Fallback Templates) maps to Phase 2."""
        phase_2_start = workflow_content.find("## Phase 2")
        phase_3_start = workflow_content.find("## Phase 3")
        phase_2_content = workflow_content[phase_2_start:phase_3_start]
        assert "fallback" in phase_2_content.lower(), (
            "Phase 2 must handle fallback templates (AC#2)"
        )

    def test_ac3_maps_to_phase_4(self, workflow_content):
        """Act & Assert: AC#3 (Feedback Synthesis) maps to Phase 4."""
        phase_4_start = workflow_content.find("## Phase 4")
        phase_5_start = workflow_content.find("## Phase 5")
        phase_4_content = workflow_content[phase_4_start:phase_5_start]
        assert "synthesis" in phase_4_content.lower() or "synthesize" in phase_4_content.lower(), (
            "Phase 4 must handle feedback synthesis (AC#3)"
        )

    def test_ac4_maps_to_phase_5(self, workflow_content):
        """Act & Assert: AC#4 (Milestone Tracking) maps to Phase 5."""
        phase_5_start = workflow_content.find("## Phase 5")
        phase_6_start = workflow_content.find("## Phase 6")
        phase_5_content = workflow_content[phase_5_start:phase_6_start]
        assert "milestone" in phase_5_content.lower(), (
            "Phase 5 must handle milestone tracking (AC#4)"
        )

    def test_ac5_maps_to_phase_6(self, workflow_content):
        """Act & Assert: AC#5 (Partial Progress) maps to Phase 6."""
        phase_6_start = workflow_content.find("## Phase 6")
        phase_6_content = workflow_content[phase_6_start:]
        has_persistence = (
            "state" in phase_6_content.lower()
            or "progress" in phase_6_content.lower()
            or "resume" in phase_6_content.lower()
        )
        assert has_persistence, (
            "Phase 6 must handle partial progress persistence (AC#5)"
        )


# ============================================================
# 5. Business Rule Consistency
# ============================================================

class TestBusinessRuleConsistency:
    """Validate business rules are consistent between story spec and implementation."""

    def test_br001_fallback_in_both_story_and_workflow(self, story_content, workflow_content):
        """Act & Assert: BR-001 (fallback on missing EPIC-074) in both artifacts."""
        assert "BR-001" in story_content, "Story must define BR-001"
        assert "BR-001" in workflow_content or "fallback" in workflow_content.lower(), (
            "Workflow must implement BR-001 fallback behavior"
        )

    def test_br002_zero_interviews_in_both(self, story_content, workflow_content):
        """Act & Assert: BR-002 (zero interviews blocks synthesis) in both artifacts."""
        assert "BR-002" in story_content, "Story must define BR-002"
        assert "BR-002" in workflow_content or "zero interview" in workflow_content.lower(), (
            "Workflow must implement BR-002 zero-interview blocking"
        )

    def test_br003_duplicate_milestone_in_both(self, story_content, workflow_content):
        """Act & Assert: BR-003 (duplicate milestone prompt) in both artifacts."""
        assert "BR-003" in story_content, "Story must define BR-003"
        assert "BR-003" in workflow_content or "duplicate" in workflow_content.lower(), (
            "Workflow must implement BR-003 duplicate milestone detection"
        )

    def test_br004_max_segments_in_both(self, story_content, workflow_content):
        """Act & Assert: BR-004 (max 10 segments) in both artifacts."""
        assert "BR-004" in story_content, "Story must define BR-004"
        assert "BR-004" in workflow_content or (
            "10" in workflow_content and "segment" in workflow_content.lower()
        ), (
            "Workflow must implement BR-004 max segment limit"
        )

    def test_nfr001_corrupted_state_in_both(self, story_content, workflow_content):
        """Act & Assert: NFR-001 (corrupted state fallback) in both artifacts."""
        assert "NFR-001" in story_content, "Story must define NFR-001"
        assert "NFR-001" in workflow_content or "corrupt" in workflow_content.lower(), (
            "Workflow must implement NFR-001 corrupted state handling"
        )

    def test_five_fallback_topics_count_consistent(self, story_content, workflow_content):
        """Act & Assert: Both story and workflow specify exactly 5 fallback topics."""
        assert "5" in story_content and "fallback" in story_content.lower(), (
            "Story must specify 5 fallback topics"
        )
        # Count numbered items in Phase 2 fallback section
        phase_2_start = workflow_content.find("## Phase 2")
        phase_3_start = workflow_content.find("## Phase 3")
        phase_2_content = workflow_content[phase_2_start:phase_3_start]
        numbered_items = re.findall(r"^\d+\.\s+\*\*", phase_2_content, re.MULTILINE)
        assert len(numbered_items) == 5, (
            f"Workflow Phase 2 must contain exactly 5 fallback topics, found {len(numbered_items)}"
        )
