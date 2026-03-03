"""
Tests for STORY-306: Subagent Enforcement in Phase State Completion

TDD Red Phase - All tests should FAIL initially until implementation is complete.

Test Coverage:
- AC1: PHASE_REQUIRED_SUBAGENTS constant
- AC2: subagents_required populated on state creation
- AC3: complete_phase() blocks on missing subagents
- AC4: complete_phase() succeeds with all subagents
- AC5: Escape hatch (checkpoint_passed=False)
- AC6: OR logic for Phase 03
- AC8: Backward compatibility for legacy state files
"""

import json
import pytest
import time
from pathlib import Path
from unittest.mock import patch

# Import will fail until implementation exists - expected for TDD Red
from devforgeai_cli.phase_state import (
    PhaseState,
    PhaseStateError,
    # These imports will fail until AC implementation
    # PHASE_REQUIRED_SUBAGENTS,  # AC1
    # SubagentEnforcementError,  # AC3
)


# =============================================================================
# Fixtures
# =============================================================================


@pytest.fixture
def temp_project(tmp_path):
    """Create temporary project structure for testing."""
    workflows_dir = tmp_path / "devforgeai" / "workflows"
    workflows_dir.mkdir(parents=True)
    return tmp_path


@pytest.fixture
def phase_state(temp_project):
    """Create PhaseState instance with temp project."""
    return PhaseState(project_root=temp_project)


@pytest.fixture
def initialized_state(phase_state, temp_project):
    """Create and return initialized state for STORY-001."""
    state = phase_state.create("STORY-001")
    return state


@pytest.fixture
def legacy_state_file(temp_project):
    """Create a legacy state file with empty subagents_required arrays."""
    workflows_dir = temp_project / "devforgeai" / "workflows"
    state_file = workflows_dir / "STORY-001-phase-state.json"

    legacy_state = {
        "story_id": "STORY-001",
        "current_phase": "01",
        "workflow_started": "2026-01-23T00:00:00Z",
        "blocking_status": False,
        "phases": {
            "01": {"status": "pending", "subagents_required": [], "subagents_invoked": []},
            "02": {"status": "pending", "subagents_required": [], "subagents_invoked": []},
            "03": {"status": "pending", "subagents_required": [], "subagents_invoked": []},
            "04": {"status": "pending", "subagents_required": [], "subagents_invoked": []},
            "4.5": {"status": "pending", "subagents_required": [], "subagents_invoked": []},
            "05": {"status": "pending", "subagents_required": [], "subagents_invoked": []},
            "5.5": {"status": "pending", "subagents_required": [], "subagents_invoked": []},
            "06": {"status": "pending", "subagents_required": [], "subagents_invoked": []},
            "07": {"status": "pending", "subagents_required": [], "subagents_invoked": []},
            "08": {"status": "pending", "subagents_required": [], "subagents_invoked": []},
            "09": {"status": "pending", "subagents_required": [], "subagents_invoked": []},
            "10": {"status": "pending", "subagents_required": [], "subagents_invoked": []},
        },
        "validation_errors": [],
        "observations": []
    }

    state_file.write_text(json.dumps(legacy_state, indent=2))
    return state_file


# =============================================================================
# AC1: PHASE_REQUIRED_SUBAGENTS constant tests
# =============================================================================


class TestPhaseRequiredSubagentsConstant:
    """AC1: PHASE_REQUIRED_SUBAGENTS constant defines subagent requirements."""

    def test_constant_exists_in_module(self):
        """PHASE_REQUIRED_SUBAGENTS constant should exist at module level."""
        from devforgeai_cli import phase_state
        assert hasattr(phase_state, 'PHASE_REQUIRED_SUBAGENTS'), \
            "PHASE_REQUIRED_SUBAGENTS constant not found in phase_state module"

    def test_constant_contains_all_12_phases(self):
        """Constant should have entries for all 12 valid phases."""
        from devforgeai_cli.phase_state import PHASE_REQUIRED_SUBAGENTS

        expected_phases = ["01", "02", "03", "04", "4.5", "05", "5.5",
                          "06", "07", "08", "09", "10"]

        for phase in expected_phases:
            assert phase in PHASE_REQUIRED_SUBAGENTS, \
                f"Phase {phase} missing from PHASE_REQUIRED_SUBAGENTS"

    def test_phase_01_requires_git_validator_and_tech_stack_detector(self):
        """Phase 01 should require git-validator and tech-stack-detector."""
        from devforgeai_cli.phase_state import PHASE_REQUIRED_SUBAGENTS

        required = PHASE_REQUIRED_SUBAGENTS["01"]
        assert "git-validator" in required, "Phase 01 should require git-validator"
        assert "tech-stack-detector" in required, "Phase 01 should require tech-stack-detector"

    def test_phase_02_requires_test_automator(self):
        """Phase 02 should require test-automator."""
        from devforgeai_cli.phase_state import PHASE_REQUIRED_SUBAGENTS

        required = PHASE_REQUIRED_SUBAGENTS["02"]
        assert "test-automator" in required, "Phase 02 should require test-automator"

    def test_phase_03_uses_tuple_for_or_logic(self):
        """Phase 03 should use tuple for OR logic (backend OR frontend)."""
        from devforgeai_cli.phase_state import PHASE_REQUIRED_SUBAGENTS

        required = PHASE_REQUIRED_SUBAGENTS["03"]
        # Find the tuple containing OR options
        or_group = None
        for item in required:
            if isinstance(item, tuple):
                or_group = item
                break

        assert or_group is not None, "Phase 03 should have tuple for OR logic"
        assert "backend-architect" in or_group, "OR group should contain backend-architect"
        assert "frontend-developer" in or_group, "OR group should contain frontend-developer"

    def test_phase_04_requires_refactoring_specialist_and_code_reviewer(self):
        """Phase 04 should require refactoring-specialist and code-reviewer."""
        from devforgeai_cli.phase_state import PHASE_REQUIRED_SUBAGENTS

        required = PHASE_REQUIRED_SUBAGENTS["04"]
        assert "refactoring-specialist" in required
        assert "code-reviewer" in required

    def test_phase_4_5_requires_ac_compliance_verifier(self):
        """Phase 4.5 should require ac-compliance-verifier."""
        from devforgeai_cli.phase_state import PHASE_REQUIRED_SUBAGENTS

        required = PHASE_REQUIRED_SUBAGENTS["4.5"]
        assert "ac-compliance-verifier" in required

    def test_phase_05_requires_integration_tester(self):
        """Phase 05 should require integration-tester."""
        from devforgeai_cli.phase_state import PHASE_REQUIRED_SUBAGENTS

        required = PHASE_REQUIRED_SUBAGENTS["05"]
        assert "integration-tester" in required

    def test_phase_5_5_requires_ac_compliance_verifier(self):
        """Phase 5.5 should require ac-compliance-verifier."""
        from devforgeai_cli.phase_state import PHASE_REQUIRED_SUBAGENTS

        required = PHASE_REQUIRED_SUBAGENTS["5.5"]
        assert "ac-compliance-verifier" in required

    def test_phase_06_requires_deferral_validator_conditional(self):
        """Phase 06 should require deferral-validator (conditional)."""
        from devforgeai_cli.phase_state import PHASE_REQUIRED_SUBAGENTS

        # Phase 06 may have conditional requirement or empty
        required = PHASE_REQUIRED_SUBAGENTS["06"]
        # Conditional subagent - can be empty or contain deferral-validator
        assert isinstance(required, (list, tuple))

    def test_phase_07_has_no_required_subagents(self):
        """Phase 07 should have no required subagents (file operations)."""
        from devforgeai_cli.phase_state import PHASE_REQUIRED_SUBAGENTS

        required = PHASE_REQUIRED_SUBAGENTS["07"]
        assert len(required) == 0, "Phase 07 should have no required subagents"

    def test_phase_08_has_no_required_subagents(self):
        """Phase 08 should have no required subagents (git operations)."""
        from devforgeai_cli.phase_state import PHASE_REQUIRED_SUBAGENTS

        required = PHASE_REQUIRED_SUBAGENTS["08"]
        assert len(required) == 0, "Phase 08 should have no required subagents"

    def test_phase_09_requires_framework_analyst(self):
        """Phase 09 should require framework-analyst (per RCA-027 fix)."""
        from devforgeai_cli.phase_state import PHASE_REQUIRED_SUBAGENTS

        required = PHASE_REQUIRED_SUBAGENTS["09"]
        assert "framework-analyst" in required, \
            "Phase 09 should require framework-analyst (RCA-027 fix)"

    def test_phase_10_requires_dev_result_interpreter(self):
        """Phase 10 should require dev-result-interpreter."""
        from devforgeai_cli.phase_state import PHASE_REQUIRED_SUBAGENTS

        required = PHASE_REQUIRED_SUBAGENTS["10"]
        assert "dev-result-interpreter" in required


# =============================================================================
# AC2: subagents_required populated on state creation
# =============================================================================


class TestSubagentsRequiredPopulation:
    """AC2: subagents_required populated from constant on state creation."""

    def test_new_state_has_populated_subagents_required(self, phase_state):
        """New state should have subagents_required populated, not empty."""
        state = phase_state.create("STORY-001")

        # Check Phase 02 specifically
        phase_02 = state["phases"]["02"]
        assert len(phase_02["subagents_required"]) > 0, \
            "Phase 02 subagents_required should not be empty"

    def test_phase_02_subagents_required_contains_test_automator(self, phase_state):
        """Phase 02 subagents_required should contain test-automator."""
        state = phase_state.create("STORY-001")

        phase_02_required = state["phases"]["02"]["subagents_required"]
        assert "test-automator" in phase_02_required

    def test_phase_09_subagents_required_contains_framework_analyst(self, phase_state):
        """Phase 09 subagents_required should contain framework-analyst."""
        state = phase_state.create("STORY-001")

        phase_09_required = state["phases"]["09"]["subagents_required"]
        assert "framework-analyst" in phase_09_required

    def test_phase_07_subagents_required_is_empty(self, phase_state):
        """Phase 07 subagents_required should be empty (no required subagents)."""
        state = phase_state.create("STORY-001")

        phase_07_required = state["phases"]["07"]["subagents_required"]
        assert len(phase_07_required) == 0

    def test_phase_08_subagents_required_is_empty(self, phase_state):
        """Phase 08 subagents_required should be empty (no required subagents)."""
        state = phase_state.create("STORY-001")

        phase_08_required = state["phases"]["08"]["subagents_required"]
        assert len(phase_08_required) == 0


# =============================================================================
# AC3: complete_phase() blocks when required subagents not invoked
# =============================================================================


class TestCompletePhaseBlocking:
    """AC3: complete_phase() raises error when required subagents missing."""

    def test_complete_phase_raises_error_without_required_subagents(self, phase_state):
        """complete_phase should raise SubagentEnforcementError when missing subagents."""
        from devforgeai_cli.phase_state import SubagentEnforcementError

        # Create state - subagents_required should be populated
        phase_state.create("STORY-001")

        # Complete Phase 01 first (to get to Phase 02)
        # Phase 01 requires git-validator and tech-stack-detector
        phase_state.record_subagent("STORY-001", "01", "git-validator")
        phase_state.record_subagent("STORY-001", "01", "tech-stack-detector")
        phase_state.complete_phase("STORY-001", "01", checkpoint_passed=True)

        # Now try to complete Phase 02 WITHOUT invoking test-automator
        with pytest.raises(SubagentEnforcementError):
            phase_state.complete_phase("STORY-001", "02", checkpoint_passed=True)

    def test_error_message_identifies_missing_subagent(self, phase_state):
        """Error message should identify which subagent is missing."""
        from devforgeai_cli.phase_state import SubagentEnforcementError

        phase_state.create("STORY-001")

        # Complete Phase 01
        phase_state.record_subagent("STORY-001", "01", "git-validator")
        phase_state.record_subagent("STORY-001", "01", "tech-stack-detector")
        phase_state.complete_phase("STORY-001", "01", checkpoint_passed=True)

        # Try to complete Phase 02 without test-automator
        with pytest.raises(SubagentEnforcementError) as exc_info:
            phase_state.complete_phase("STORY-001", "02", checkpoint_passed=True)

        assert "test-automator" in str(exc_info.value), \
            "Error message should identify missing subagent 'test-automator'"

    def test_error_lists_all_missing_subagents_for_partial_invocation(self, phase_state):
        """Error should list ALL missing subagents, not just first one."""
        from devforgeai_cli.phase_state import SubagentEnforcementError

        phase_state.create("STORY-001")

        # Try to complete Phase 01 with only git-validator (missing tech-stack-detector)
        phase_state.record_subagent("STORY-001", "01", "git-validator")

        with pytest.raises(SubagentEnforcementError) as exc_info:
            phase_state.complete_phase("STORY-001", "01", checkpoint_passed=True)

        assert "tech-stack-detector" in str(exc_info.value)

    def test_subagent_enforcement_error_has_required_attributes(self, phase_state):
        """SubagentEnforcementError should have story_id, phase, missing_subagents."""
        from devforgeai_cli.phase_state import SubagentEnforcementError

        phase_state.create("STORY-001")

        try:
            phase_state.complete_phase("STORY-001", "01", checkpoint_passed=True)
            pytest.fail("Expected SubagentEnforcementError")
        except SubagentEnforcementError as e:
            assert hasattr(e, 'story_id'), "Error should have story_id attribute"
            assert hasattr(e, 'phase'), "Error should have phase attribute"
            assert hasattr(e, 'missing_subagents'), "Error should have missing_subagents attribute"
            assert e.story_id == "STORY-001"
            assert e.phase == "01"
            assert isinstance(e.missing_subagents, list)


# =============================================================================
# AC4: complete_phase() succeeds when all required subagents invoked
# =============================================================================


class TestCompletePhaseSuccess:
    """AC4: complete_phase() succeeds when all required subagents invoked."""

    def test_complete_phase_succeeds_with_all_subagents_invoked(self, phase_state):
        """Phase completes successfully when all required subagents invoked."""
        phase_state.create("STORY-001")

        # Record required subagents for Phase 01
        phase_state.record_subagent("STORY-001", "01", "git-validator")
        phase_state.record_subagent("STORY-001", "01", "tech-stack-detector")

        # Should not raise
        state = phase_state.complete_phase("STORY-001", "01", checkpoint_passed=True)

        assert state["phases"]["01"]["status"] == "completed"

    def test_current_phase_advances_after_successful_completion(self, phase_state):
        """current_phase should advance to next phase after completion."""
        phase_state.create("STORY-001")

        # Complete Phase 01
        phase_state.record_subagent("STORY-001", "01", "git-validator")
        phase_state.record_subagent("STORY-001", "01", "tech-stack-detector")

        state = phase_state.complete_phase("STORY-001", "01", checkpoint_passed=True)

        assert state["current_phase"] == "02", \
            "current_phase should advance to '02' after completing '01'"

    def test_phase_02_completes_with_test_automator(self, phase_state):
        """Phase 02 should complete when test-automator is invoked."""
        phase_state.create("STORY-001")

        # Complete Phase 01 first
        phase_state.record_subagent("STORY-001", "01", "git-validator")
        phase_state.record_subagent("STORY-001", "01", "tech-stack-detector")
        phase_state.complete_phase("STORY-001", "01", checkpoint_passed=True)

        # Record test-automator for Phase 02
        phase_state.record_subagent("STORY-001", "02", "test-automator")

        # Should complete successfully
        state = phase_state.complete_phase("STORY-001", "02", checkpoint_passed=True)

        assert state["phases"]["02"]["status"] == "completed"
        assert state["current_phase"] == "03"


# =============================================================================
# AC5: Escape hatch (checkpoint_passed=False) bypasses validation
# =============================================================================


class TestEscapeHatch:
    """AC5: checkpoint_passed=False bypasses subagent validation."""

    def test_escape_hatch_allows_completion_without_subagents(self, phase_state):
        """checkpoint_passed=False should allow completion without validation."""
        phase_state.create("STORY-001")

        # Do NOT invoke any subagents
        # Complete with escape hatch
        state = phase_state.complete_phase("STORY-001", "01", checkpoint_passed=False)

        # Should complete without error
        assert state["phases"]["01"]["status"] == "completed"

    def test_escape_hatch_stores_checkpoint_passed_false(self, phase_state):
        """checkpoint_passed should be stored as False in state file."""
        phase_state.create("STORY-001")

        state = phase_state.complete_phase("STORY-001", "01", checkpoint_passed=False)

        assert state["phases"]["01"]["checkpoint_passed"] is False

    def test_escape_hatch_still_advances_current_phase(self, phase_state):
        """Escape hatch should still advance current_phase."""
        phase_state.create("STORY-001")

        state = phase_state.complete_phase("STORY-001", "01", checkpoint_passed=False)

        assert state["current_phase"] == "02"


# =============================================================================
# AC6: OR logic for Phase 03 subagents
# =============================================================================


class TestOrLogicPhase03:
    """AC6: OR logic handled for Phase 03 subagents."""

    def _advance_to_phase_03(self, phase_state):
        """Helper to advance state to Phase 03."""
        phase_state.create("STORY-001")

        # Complete Phase 01
        phase_state.record_subagent("STORY-001", "01", "git-validator")
        phase_state.record_subagent("STORY-001", "01", "tech-stack-detector")
        phase_state.complete_phase("STORY-001", "01", checkpoint_passed=True)

        # Complete Phase 02
        phase_state.record_subagent("STORY-001", "02", "test-automator")
        phase_state.complete_phase("STORY-001", "02", checkpoint_passed=True)

    def test_phase_03_completes_with_backend_architect_only(self, phase_state):
        """Phase 03 should complete with only backend-architect (not frontend)."""
        self._advance_to_phase_03(phase_state)

        # Record backend-architect and context-validator
        phase_state.record_subagent("STORY-001", "03", "backend-architect")
        phase_state.record_subagent("STORY-001", "03", "context-validator")

        state = phase_state.complete_phase("STORY-001", "03", checkpoint_passed=True)

        assert state["phases"]["03"]["status"] == "completed"

    def test_phase_03_completes_with_frontend_developer_only(self, phase_state):
        """Phase 03 should complete with only frontend-developer (not backend)."""
        self._advance_to_phase_03(phase_state)

        # Record frontend-developer and context-validator
        phase_state.record_subagent("STORY-001", "03", "frontend-developer")
        phase_state.record_subagent("STORY-001", "03", "context-validator")

        state = phase_state.complete_phase("STORY-001", "03", checkpoint_passed=True)

        assert state["phases"]["03"]["status"] == "completed"

    def test_phase_03_blocks_without_either_architect(self, phase_state):
        """Phase 03 should block if neither backend nor frontend invoked."""
        from devforgeai_cli.phase_state import SubagentEnforcementError

        self._advance_to_phase_03(phase_state)

        # Record only context-validator (missing backend OR frontend)
        phase_state.record_subagent("STORY-001", "03", "context-validator")

        with pytest.raises(SubagentEnforcementError):
            phase_state.complete_phase("STORY-001", "03", checkpoint_passed=True)

    def test_phase_03_completes_with_both_architects(self, phase_state):
        """Phase 03 should also complete if BOTH architects are invoked."""
        self._advance_to_phase_03(phase_state)

        # Record both architects and context-validator
        phase_state.record_subagent("STORY-001", "03", "backend-architect")
        phase_state.record_subagent("STORY-001", "03", "frontend-developer")
        phase_state.record_subagent("STORY-001", "03", "context-validator")

        state = phase_state.complete_phase("STORY-001", "03", checkpoint_passed=True)

        assert state["phases"]["03"]["status"] == "completed"


# =============================================================================
# AC8: Backward compatibility for legacy state files
# =============================================================================


class TestBackwardCompatibility:
    """AC8: Legacy state files get subagents_required populated on read."""

    def test_legacy_state_file_loads_successfully(self, phase_state, legacy_state_file):
        """Legacy state file with empty subagents_required should load."""
        state = phase_state.read("STORY-001")

        assert state is not None
        assert state["story_id"] == "STORY-001"

    def test_legacy_state_subagents_required_populated_on_read(self, phase_state, legacy_state_file):
        """Legacy state should have subagents_required populated after read."""
        state = phase_state.read("STORY-001")

        # Phase 02 should now have test-automator in subagents_required
        phase_02_required = state["phases"]["02"]["subagents_required"]
        assert "test-automator" in phase_02_required, \
            "Legacy state should have subagents_required populated after read"

    def test_legacy_state_phase_09_has_framework_analyst(self, phase_state, legacy_state_file):
        """Legacy state Phase 09 should have framework-analyst after read."""
        state = phase_state.read("STORY-001")

        phase_09_required = state["phases"]["09"]["subagents_required"]
        assert "framework-analyst" in phase_09_required

    def test_legacy_state_enforcement_works_after_migration(self, phase_state, legacy_state_file):
        """Subagent enforcement should work on migrated legacy state."""
        from devforgeai_cli.phase_state import SubagentEnforcementError

        # Read legacy state (triggers migration)
        phase_state.read("STORY-001")

        # Try to complete Phase 01 without subagents
        with pytest.raises(SubagentEnforcementError):
            phase_state.complete_phase("STORY-001", "01", checkpoint_passed=True)


# =============================================================================
# BR-003: Phases with no required subagents can complete
# =============================================================================


class TestPhasesWithNoRequirements:
    """BR-003: Phases 07 and 08 should complete without validation errors."""

    def _advance_to_phase_07(self, phase_state):
        """Helper to advance state to Phase 07."""
        phase_state.create("STORY-001")

        # Use escape hatch to quickly advance (for test purposes)
        for phase in ["01", "02", "03", "04", "4.5", "05", "5.5", "06"]:
            phase_state.complete_phase("STORY-001", phase, checkpoint_passed=False)

    def test_phase_07_completes_without_subagents(self, phase_state):
        """Phase 07 should complete even with no subagents invoked."""
        self._advance_to_phase_07(phase_state)

        # No subagents needed - should complete with checkpoint_passed=True
        state = phase_state.complete_phase("STORY-001", "07", checkpoint_passed=True)

        assert state["phases"]["07"]["status"] == "completed"

    def test_phase_08_completes_without_subagents(self, phase_state):
        """Phase 08 should complete even with no subagents invoked."""
        self._advance_to_phase_07(phase_state)
        phase_state.complete_phase("STORY-001", "07", checkpoint_passed=True)

        # No subagents needed - should complete with checkpoint_passed=True
        state = phase_state.complete_phase("STORY-001", "08", checkpoint_passed=True)

        assert state["phases"]["08"]["status"] == "completed"


# =============================================================================
# NFR-001: Performance benchmark
# =============================================================================


class TestPerformance:
    """NFR-001: Phase completion validation should complete within 10ms."""

    def test_complete_phase_validation_under_10ms(self, phase_state):
        """Subagent validation in complete_phase should take less than 10ms."""
        phase_state.create("STORY-001")

        # Record required subagents
        phase_state.record_subagent("STORY-001", "01", "git-validator")
        phase_state.record_subagent("STORY-001", "01", "tech-stack-detector")

        start_time = time.perf_counter()
        phase_state.complete_phase("STORY-001", "01", checkpoint_passed=True)
        elapsed_ms = (time.perf_counter() - start_time) * 1000

        assert elapsed_ms < 10, f"Validation took {elapsed_ms:.2f}ms (expected <10ms)"


# =============================================================================
# Exception Class Tests (COMP-008)
# =============================================================================


class TestSubagentEnforcementError:
    """COMP-008: SubagentEnforcementError exception class tests."""

    def test_exception_class_exists(self):
        """SubagentEnforcementError should exist in phase_state module."""
        from devforgeai_cli import phase_state
        assert hasattr(phase_state, 'SubagentEnforcementError'), \
            "SubagentEnforcementError class not found in phase_state module"

    def test_exception_inherits_from_phase_state_error(self):
        """SubagentEnforcementError should inherit from PhaseStateError."""
        from devforgeai_cli.phase_state import SubagentEnforcementError, PhaseStateError

        assert issubclass(SubagentEnforcementError, PhaseStateError)

    def test_exception_can_be_raised_with_required_params(self):
        """SubagentEnforcementError should accept story_id, phase, missing_subagents."""
        from devforgeai_cli.phase_state import SubagentEnforcementError

        exc = SubagentEnforcementError(
            story_id="STORY-001",
            phase="02",
            missing_subagents=["test-automator"]
        )

        assert exc.story_id == "STORY-001"
        assert exc.phase == "02"
        assert exc.missing_subagents == ["test-automator"]

    def test_exception_message_format(self):
        """Exception message should include story_id, phase, and missing list."""
        from devforgeai_cli.phase_state import SubagentEnforcementError

        exc = SubagentEnforcementError(
            story_id="STORY-001",
            phase="02",
            missing_subagents=["test-automator", "code-reviewer"]
        )

        message = str(exc)
        assert "STORY-001" in message
        assert "02" in message
        assert "test-automator" in message
        assert "code-reviewer" in message
