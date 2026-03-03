"""
Test: AC#2 - 4-Phase Workflow Implementation
Story: STORY-403
Generated: 2026-02-14

Validates that the dead-code-detector subagent implements a 4-phase
workflow: Phase 1 (Context Loading), Phase 2 (Function Discovery),
Phase 3 (Dependency Analysis), Phase 4 (Entry Point Exclusion + Results).

These tests MUST FAIL initially (TDD Red phase).
"""
import re
import pytest


class TestWorkflowPhases:
    """Verify 4-phase workflow is defined and ordered correctly."""

    def test_should_contain_phase_1_context_loading_when_workflow_defined(
        self, subagent_content
    ):
        """AC#2: Phase 1 (Context Loading) must be defined."""
        content = subagent_content
        assert re.search(
            r"(?i)phase\s*1.*context\s*load", content
        ), "Phase 1 (Context Loading) not found in workflow"

    def test_should_contain_phase_2_function_discovery_when_workflow_defined(
        self, subagent_content
    ):
        """AC#2: Phase 2 (Function Discovery) must be defined."""
        content = subagent_content
        assert re.search(
            r"(?i)phase\s*2.*function\s*discover", content
        ), "Phase 2 (Function Discovery) not found in workflow"

    def test_should_contain_phase_3_dependency_analysis_when_workflow_defined(
        self, subagent_content
    ):
        """AC#2: Phase 3 (Dependency Analysis) must be defined."""
        content = subagent_content
        assert re.search(
            r"(?i)phase\s*3.*dependenc", content
        ), "Phase 3 (Dependency Analysis) not found in workflow"

    def test_should_contain_phase_4_entry_point_exclusion_when_workflow_defined(
        self, subagent_content
    ):
        """AC#2: Phase 4 (Entry Point Exclusion + Results) must be defined."""
        content = subagent_content
        assert re.search(
            r"(?i)phase\s*4.*entry\s*point", content
        ), "Phase 4 (Entry Point Exclusion) not found in workflow"

    def test_should_execute_phases_in_order_1_2_3_4_when_workflow_runs(
        self, subagent_content
    ):
        """AC#2: Phases must appear in sequential order 1 -> 2 -> 3 -> 4."""
        content = subagent_content

        # Find positions of each phase in the document
        phase_1_match = re.search(r"(?i)phase\s*1", content)
        phase_2_match = re.search(r"(?i)phase\s*2", content)
        phase_3_match = re.search(r"(?i)phase\s*3", content)
        phase_4_match = re.search(r"(?i)phase\s*4", content)

        assert phase_1_match, "Phase 1 not found"
        assert phase_2_match, "Phase 2 not found"
        assert phase_3_match, "Phase 3 not found"
        assert phase_4_match, "Phase 4 not found"

        # Verify sequential ordering
        assert phase_1_match.start() < phase_2_match.start(), (
            "Phase 1 must appear before Phase 2"
        )
        assert phase_2_match.start() < phase_3_match.start(), (
            "Phase 2 must appear before Phase 3"
        )
        assert phase_3_match.start() < phase_4_match.start(), (
            "Phase 3 must appear before Phase 4"
        )

    def test_should_have_exactly_4_phases_when_workflow_complete(
        self, subagent_content
    ):
        """AC#2: Workflow must define exactly 4 phases (not more, not fewer)."""
        content = subagent_content
        # Count phase headers (Phase 1, Phase 2, Phase 3, Phase 4)
        phase_matches = re.findall(r"(?i)#+\s*phase\s*(\d+)", content)
        phase_numbers = sorted(set(int(m) for m in phase_matches))
        assert phase_numbers == [1, 2, 3, 4], (
            f"Expected phases [1, 2, 3, 4], found {phase_numbers}"
        )
