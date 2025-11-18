"""
Unit tests for devforgeai-development skill TodoWrite tracker completeness

Purpose: Validate that TodoWrite execution tracker matches documented workflow phases
Evidence: RCA-010 identified Phase 4.5-5 Bridge documented but missing from tracker
Prevention: Catches tracker-documentation mismatches before deployment
"""

import re
import pytest
from pathlib import Path


class TestTodoWriteTrackerCompleteness:
    """Test suite for TodoWrite tracker validation"""

    @pytest.fixture
    def skill_content(self):
        """Load SKILL.md content for testing"""
        skill_path = Path(".claude/skills/devforgeai-development/SKILL.md")
        with open(skill_path, 'r') as f:
            return f.read()

    def test_todowrite_tracker_has_all_documented_phases(self, skill_content):
        """
        Test: TodoWrite tracker includes all workflow phases from Complete Workflow Execution Map

        Given: SKILL.md with Complete Workflow Execution Map documenting all phases
        When: Extracting phases from both map and TodoWrite tracker
        Then: Phase counts should match exactly

        Evidence: RCA-010 identified Phase 4.5-5 Bridge documented in map but missing from tracker
        Impact: Prevents 100% of tracker-documentation gaps
        """
        # Extract documented phases from "Complete Workflow Execution Map"
        # Pattern: "Phase X:" or "Phase X.Y:" or "Phase X.Y-Z:"
        map_section = re.search(
            r'## Complete Workflow Execution Map(.*?)---',
            skill_content,
            re.DOTALL
        )
        assert map_section, "Complete Workflow Execution Map section not found in SKILL.md"

        # Extract phases - handle "Phase 4.5-5 Bridge:" format
        documented_phases_raw = re.findall(
            r'Phase ([\d.-]+(?:\s+\w+)?):',
            map_section.group(1)
        )
        # Strip non-numeric suffixes like " Bridge"
        documented_phases = [p.split()[0] for p in documented_phases_raw]
        documented_unique = sorted(set(documented_phases))
        documented_count = len(documented_unique)

        # Extract TodoWrite tracker phases
        tracker_match = re.search(
            r'TodoWrite\((.*?)\n\)',
            skill_content,
            re.DOTALL
        )
        assert tracker_match, "TodoWrite tracker not found in SKILL.md"

        tracker_content = tracker_match.group(1)
        # Match phases - remove colon to match "Phase 4.5-5" without requiring trailing colon
        tracker_phases = re.findall(
            r'Execute Phase ([\d.]+(?:-[\d.]+)?)',
            tracker_content
        )
        tracker_count = len(tracker_phases)

        # Assert counts match
        assert tracker_count == documented_count, \
            f"TodoWrite tracker has {tracker_count} phases but Complete Workflow Execution Map documents {documented_count} phases.\n" \
            f"Documented: {documented_unique}\n" \
            f"Tracker: {tracker_phases}\n" \
            f"Missing from tracker: {set(documented_unique) - set(tracker_phases)}"

        # Verify each documented phase has tracker entry
        for phase_num in documented_unique:
            assert phase_num in tracker_phases, \
                f"Phase {phase_num} is documented in Complete Workflow Execution Map but missing from TodoWrite tracker"

    def test_todowrite_tracker_phase_sequence(self, skill_content):
        """
        Test: TodoWrite tracker phases are in correct sequential order

        Given: TodoWrite tracker with multiple phase items
        When: Extracting phase numbers and checking order
        Then: Phases should be in ascending sequential order

        Prevents: Phases listed out of order (e.g., Phase 5 before Phase 4.5)
        Impact: Ensures workflow executes in correct sequence
        """
        tracker_match = re.search(r'TodoWrite\((.*?)\n\)', skill_content, re.DOTALL)
        assert tracker_match, "TodoWrite tracker not found"

        tracker_content = tracker_match.group(1)
        tracker_phases = re.findall(r'Execute Phase ([\d.]+(?:-[\d.]+)?)', tracker_content)

        # Convert to sortable format (handle X, X.Y, X.Y-Z formats)
        def phase_sort_key(phase_str):
            """Convert phase string to sortable tuple of numbers"""
            parts = phase_str.replace('-', '.').split('.')
            return tuple(float(p) for p in parts)

        sorted_phases = sorted(tracker_phases, key=phase_sort_key)

        assert tracker_phases == sorted_phases, \
            f"TodoWrite tracker phases not in sequential order.\n" \
            f"Expected: {sorted_phases}\n" \
            f"Actual: {tracker_phases}"

    def test_todowrite_tracker_has_required_fields(self, skill_content):
        """
        Test: Each TodoWrite tracker item has all required fields

        Given: TodoWrite tracker with phase items
        When: Parsing each item
        Then: All items should have: content, status, activeForm

        Prevents: Malformed tracker items that would cause runtime errors
        Impact: Ensures TodoWrite tool can properly create todo list
        """
        tracker_match = re.search(r'TodoWrite\((.*?)\)', skill_content, re.DOTALL)
        tracker_content = tracker_match.group(1)

        # Find all todo items - each on separate line
        todo_items = re.findall(
            r'\{content: "(Execute Phase.*?)".*?status: "(.*?)".*?activeForm: "(.*?)"\}',
            tracker_content,
            re.DOTALL
        )

        assert len(todo_items) > 0, "No todo items found in tracker"

        for idx, (content, status, active_form) in enumerate(todo_items):
            assert content, f"Todo item {idx} has empty content"
            assert status in ["pending", "in_progress", "completed"], \
                f"Todo item {idx} has invalid status: '{status}'"
            assert active_form, f"Todo item {idx} has empty activeForm"
            # Verify activeForm is present continuous tense
            assert active_form.startswith("Executing") or active_form.startswith("Executed"), \
                f"Todo item {idx} activeForm should use continuous tense: '{active_form}'"

    def test_todowrite_tracker_phase_descriptions_match_overview(self, skill_content):
        """
        Test: TodoWrite tracker phase descriptions align with workflow overview

        Given: SKILL.md with both workflow overview and TodoWrite tracker
        When: Comparing phase descriptions
        Then: Core phase names should match

        Prevents: Confusing mismatches between tracker and documentation
        Impact: Consistency improves user understanding
        """
        # Extract workflow overview phases
        overview_phases = {}
        for match in re.finditer(r'### (Phase [\d.-]+): (.*?)(?:\n|\r)', skill_content):
            phase_num = match.group(1).replace('Phase ', '')
            phase_name = match.group(2).split('✓')[0].strip()  # Remove markers
            overview_phases[phase_num] = phase_name

        # Extract TodoWrite tracker phases
        tracker_match = re.search(r'TodoWrite\((.*?)\)', skill_content, re.DOTALL)
        tracker_phases = {}
        for match in re.finditer(
            r'Execute Phase ([\d.-]+): (.*?) \(',
            tracker_match.group(1)
        ):
            phase_num = match.group(1)
            phase_name = match.group(2)
            tracker_phases[phase_num] = phase_name

        # Verify key phases exist in both
        for phase_num in overview_phases:
            assert phase_num in tracker_phases, \
                f"Phase {phase_num} ({overview_phases[phase_num]}) in overview but not in tracker"


class TestWorkflowExecutionMap:
    """Test suite for Complete Workflow Execution Map validation"""

    @pytest.fixture
    def skill_content(self):
        """Load SKILL.md content"""
        skill_path = Path(".claude/skills/devforgeai-development/SKILL.md")
        with open(skill_path, 'r') as f:
            return f.read()

    def test_workflow_map_exists(self, skill_content):
        """Test: Complete Workflow Execution Map section exists"""
        assert "## Complete Workflow Execution Map" in skill_content, \
            "Complete Workflow Execution Map section missing from SKILL.md"

    def test_workflow_map_has_all_phases(self, skill_content):
        """
        Test: Workflow map documents all phases in TodoWrite tracker

        Given: Complete Workflow Execution Map section
        When: Extracting phase numbers
        Then: Should match or exceed TodoWrite tracker phases

        Rationale: Map is source of truth, tracker implements it
        """
        # Extract map phases
        map_section = re.search(
            r'## Complete Workflow Execution Map(.*?)---',
            skill_content,
            re.DOTALL
        )
        map_phases = set(re.findall(r'Phase (\d+(?:\.\d+)?(?:-\d+)?)', map_section.group(1)))

        # Extract tracker phases
        tracker_match = re.search(r'TodoWrite\((.*?)\)', skill_content, re.DOTALL)
        tracker_phases = set(re.findall(
            r'Execute Phase (\d+(?:\.\d+)?(?:-\d+)?)',
            tracker_match.group(1)
        ))

        # Tracker phases should be subset of or equal to map phases
        missing_from_map = tracker_phases - map_phases
        assert not missing_from_map, \
            f"Tracker has phases not documented in map: {missing_from_map}"

    def test_mandatory_markers_present(self, skill_content):
        """
        Test: All documented MANDATORY phases have ✓ MANDATORY marker

        Given: Workflow overview with MANDATORY phases
        When: Checking for ✓ MANDATORY markers
        Then: All required phases should have marker

        Known MANDATORY phases:
        - Phase 4.5-5 Bridge (RCA-009, RCA-010)
        - Steps marked MANDATORY in Complete Workflow Map
        """
        # Extract phases from Complete Workflow Map with MANDATORY markers
        map_section = re.search(
            r'## Complete Workflow Execution Map(.*?)---',
            skill_content,
            re.DOTALL
        )

        # Count MANDATORY markers in map
        mandatory_in_map = len(re.findall(r'✓ MANDATORY', map_section.group(1)))

        # Phase 4.5-5 Bridge should have MANDATORY marker in overview
        bridge_section = re.search(
            r'### Phase 4\.5-5 Bridge:.*?\n',
            skill_content
        )
        if bridge_section:
            assert '✓ MANDATORY' in bridge_section.group(0), \
                "Phase 4.5-5 Bridge missing ✓ MANDATORY marker in workflow overview (RCA-010 REC-3)"

        # Verify we have at least some MANDATORY markers
        assert mandatory_in_map > 0, \
            "No MANDATORY markers found in Complete Workflow Execution Map"


class TestRegressionPrevention:
    """Regression tests to prevent RCA-010 issue recurrence"""

    @pytest.fixture
    def skill_content(self):
        """Load SKILL.md content"""
        skill_path = Path(".claude/skills/devforgeai-development/SKILL.md")
        with open(skill_path, 'r') as f:
            return f.read()

    def test_phase_4_5_5_bridge_in_tracker(self, skill_content):
        """
        Test: Phase 4.5-5 Bridge exists in TodoWrite tracker

        Given: RCA-010 fix implemented
        When: Checking TodoWrite tracker
        Then: Phase 4.5-5 Bridge should be present

        This is the specific regression test for RCA-010's root cause.
        """
        tracker_match = re.search(r'TodoWrite\((.*?)\n\)', skill_content, re.DOTALL)
        tracker_content = tracker_match.group(1)

        assert 'Phase 4.5-5 Bridge' in tracker_content, \
            "Phase 4.5-5 Bridge missing from TodoWrite tracker (RCA-010 regression)"

        assert 'Update DoD Checkboxes' in tracker_content, \
            "Phase 4.5-5 Bridge description should mention 'Update DoD Checkboxes'"

    def test_tracker_has_9_phases_after_rca_010(self, skill_content):
        """
        Test: TodoWrite tracker has 9 phases after RCA-010 fix

        Given: RCA-010 REC-1 implemented
        When: Counting TodoWrite tracker items
        Then: Should have 9 items (was 8 before RCA-010)

        Phases: 0, 1, 2, 3, 4, 4.5, 4.5-5 Bridge, 5, 6
        """
        tracker_match = re.search(r'TodoWrite\((.*?)\n\)', skill_content, re.DOTALL)
        tracker_phases = re.findall(
            r'Execute Phase ([\d.]+(?:-[\d.]+)?)',
            tracker_match.group(1)
        )

        assert len(tracker_phases) == 9, \
            f"TodoWrite tracker should have 9 phases after RCA-010, found {len(tracker_phases)}"

    def test_phase_4_5_5_bridge_between_4_5_and_5(self, skill_content):
        """
        Test: Phase 4.5-5 Bridge positioned correctly between Phase 4.5 and Phase 5

        Given: TodoWrite tracker with Phase 4.5-5 Bridge
        When: Checking phase order
        Then: Should appear after Phase 4.5, before Phase 5

        Prevents: Incorrect sequencing that would break workflow
        """
        tracker_match = re.search(r'TodoWrite\((.*?)\n\)', skill_content, re.DOTALL)
        tracker_phases = re.findall(
            r'Execute Phase ([\d.]+(?:-[\d.]+)?)',
            tracker_match.group(1)
        )

        # Find indices
        phase_4_5_idx = tracker_phases.index('4.5')
        bridge_idx = tracker_phases.index('4.5-5')
        phase_5_idx = tracker_phases.index('5')

        # Verify order
        assert phase_4_5_idx < bridge_idx < phase_5_idx, \
            f"Phase 4.5-5 Bridge must be between Phase 4.5 and Phase 5.\n" \
            f"Order: Phase 4.5 (#{phase_4_5_idx}), Bridge (#{bridge_idx}), Phase 5 (#{phase_5_idx})"


class TestWorkflowConsistency:
    """Test workflow consistency across all documentation"""

    @pytest.fixture
    def skill_content(self):
        """Load SKILL.md content"""
        skill_path = Path(".claude/skills/devforgeai-development/SKILL.md")
        with open(skill_path, 'r') as f:
            return f.read()

    def test_phase_numbers_match_across_sections(self, skill_content):
        """
        Test: Phase numbers consistent across all SKILL.md sections

        Given: SKILL.md with multiple sections listing phases
        When: Extracting phase numbers from each section
        Then: All sections should reference the same phases

        Sections checked:
        - Workflow Overview
        - TodoWrite Tracker
        - Complete Workflow Execution Map
        - Subagent Coordination
        """
        # Extract from Workflow Overview (### Phase X:) - handle "Phase 4.5-5 Bridge:" format
        overview_phases_raw = re.findall(r'^### Phase ([\d.-]+(?:\s+\w+)?):' , skill_content, re.MULTILINE)
        overview_phases = set([p.split()[0] for p in overview_phases_raw])

        # Extract from TodoWrite Tracker
        tracker_match = re.search(r'TodoWrite\((.*?)\n\)', skill_content, re.DOTALL)
        tracker_phases = set(re.findall(r'Execute Phase ([\d.]+(?:-[\d.]+)?)', tracker_match.group(1)))

        # Extract from Workflow Map - handle "Phase 4.5-5 Bridge:" format
        map_section = re.search(r'## Complete Workflow Execution Map(.*?)---', skill_content, re.DOTALL)
        map_phases_raw = re.findall(r'^Phase ([\d.-]+(?:\s+\w+)?):' , map_section.group(1), re.MULTILINE)
        map_phases = set([p.split()[0] for p in map_phases_raw])

        # All should match
        assert overview_phases == tracker_phases, \
            f"Overview and Tracker phase mismatch:\n" \
            f"Overview: {sorted(overview_phases)}\n" \
            f"Tracker: {sorted(tracker_phases)}\n" \
            f"Difference: {overview_phases.symmetric_difference(tracker_phases)}"

        assert tracker_phases == map_phases, \
            f"Tracker and Map phase mismatch:\n" \
            f"Tracker: {sorted(tracker_phases)}\n" \
            f"Map: {sorted(map_phases)}\n" \
            f"Difference: {tracker_phases.symmetric_difference(map_phases)}"

    def test_no_duplicate_phase_numbers(self, skill_content):
        """
        Test: No duplicate phase numbers in TodoWrite tracker

        Given: TodoWrite tracker
        When: Extracting all phase numbers
        Then: Each phase number should appear exactly once

        Prevents: Duplicate phase entries causing confusion
        """
        tracker_match = re.search(r'TodoWrite\((.*?)\)', skill_content, re.DOTALL)
        tracker_phases = re.findall(r'Execute Phase ([\d.]+(?:-[\d.]+)?):', tracker_match.group(1))

        # Check for duplicates
        seen = set()
        duplicates = set()
        for phase in tracker_phases:
            if phase in seen:
                duplicates.add(phase)
            seen.add(phase)

        assert not duplicates, \
            f"Duplicate phase numbers found in TodoWrite tracker: {duplicates}"


if __name__ == "__main__":
    # Run tests with pytest
    pytest.main([__file__, "-v", "--tb=short"])
