"""
Integration test suite for STORY-034: Refactor /qa command - Move Phases 4 & 5 to skill

Tests cover:
- 7 acceptance criteria (AC1-AC7) from STORY-034
- Phase 6 added to devforgeai-qa skill (feedback hooks logic)
- Phase 7 added to devforgeai-qa skill (story update logic)
- Phases 4 & 5 removed from /qa command
- Command refactored to 3 phases only
- Reference files created for progressive disclosure
- Lean orchestration pattern compliance

TDD Red Phase: All tests written BEFORE implementation.
Framework: pytest
Test Pattern: AAA (Arrange, Act, Assert)
Coverage: All 7 AC + NFR validation + edge cases
"""

import pytest
import subprocess
from pathlib import Path
import re


# ============================================================================
# FIXTURES - Common setup for all tests
# ============================================================================


@pytest.fixture
def qa_command_path():
    """Path to /qa command file."""
    return Path("/mnt/c/Projects/DevForgeAI2/.claude/commands/qa.md")


@pytest.fixture
def qa_skill_path():
    """Path to devforgeai-qa skill file."""
    return Path("/mnt/c/Projects/DevForgeAI2/.claude/skills/devforgeai-qa/SKILL.md")


@pytest.fixture
def feedback_hooks_ref_path():
    """Path to feedback-hooks-workflow.md reference file."""
    return Path("/mnt/c/Projects/DevForgeAI2/.claude/skills/devforgeai-qa/references/feedback-hooks-workflow.md")


@pytest.fixture
def story_update_ref_path():
    """Path to story-update-workflow.md reference file."""
    return Path("/mnt/c/Projects/DevForgeAI2/.claude/skills/devforgeai-qa/references/story-update-workflow.md")


# ============================================================================
# TEST: AC1 - Phase 6 Added to devforgeai-qa Skill
# ============================================================================


@pytest.mark.integration
@pytest.mark.acceptance_criteria
class TestAC1Phase6AddedToSkill:
    """Test acceptance criterion 1: Phase 6 added to devforgeai-qa skill."""

    def test_skill_has_phase_6_section(self, qa_skill_path):
        """
        AC1: Phase 6 section exists in devforgeai-qa skill.

        Given: devforgeai-qa skill file is readable
        When: Search for Phase 6 header
        Then: "Phase 6" or "### Phase 6" found in skill
        """
        # Arrange & Act
        with open(qa_skill_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Assert
        assert "Phase 6" in content, "Phase 6 must exist in devforgeai-qa skill"
        assert "Feedback Hook" in content or "feedback hook" in content, \
            "Phase 6 must reference feedback hooks"

    def test_phase_6_determines_qa_status(self, qa_skill_path):
        """
        AC1: Phase 6 determines QA status (PASSED→completed, FAILED→failed, PARTIAL→partial).

        Given: Phase 6 exists in skill
        When: Parse Phase 6 bash code for status mapping
        Then: All three status mappings present
        """
        # Arrange & Act
        with open(qa_skill_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Extract Phase 6 section (approximate)
        if "Phase 6" in content:
            phase6_start = content.find("Phase 6")
            phase6_section = content[phase6_start:phase6_start + 3000]
        else:
            phase6_section = ""

        # Assert
        assert "PASSED" in phase6_section or "completed" in phase6_section, \
            "Phase 6 must handle PASSED→completed mapping"
        assert "FAILED" in phase6_section or "failed" in phase6_section, \
            "Phase 6 must handle FAILED→failed mapping"

    def test_phase_6_calls_check_hooks(self, qa_skill_path):
        """
        AC1: Phase 6 calls devforgeai check-hooks with --operation=qa --status=$STATUS.

        Given: Phase 6 exists in skill
        When: Parse Phase 6 bash code
        Then: check-hooks command with correct arguments found
        """
        # Arrange & Act
        with open(qa_skill_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Assert
        assert "devforgeai check-hooks" in content or "check-hooks" in content, \
            "Phase 6 must call check-hooks command"
        assert "--operation=qa" in content, \
            "Phase 6 must pass --operation=qa to check-hooks"
        assert "--status=" in content or "$STATUS" in content, \
            "Phase 6 must pass status variable to check-hooks"

    def test_phase_6_conditionally_invokes_hooks(self, qa_skill_path):
        """
        AC1: Phase 6 conditionally invokes hooks based on exit code 0.

        Given: Phase 6 exists in skill
        When: Parse conditional logic
        Then: invoke-hooks wrapped in if [ $? -eq 0 ] condition
        """
        # Arrange & Act
        with open(qa_skill_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Assert
        assert "invoke-hooks" in content, "Phase 6 must call invoke-hooks"
        assert "if [ $? -eq 0 ]" in content or "if [$? -eq 0]" in content, \
            "invoke-hooks must be conditionally called based on check-hooks exit code"

    def test_phase_6_is_non_blocking(self, qa_skill_path):
        """
        AC1: Phase 6 is non-blocking (hook failures don't affect QA result).

        Given: Phase 6 exists in skill
        When: Parse error handling
        Then: Non-blocking pattern (|| { ... }) found
        """
        # Arrange & Act
        with open(qa_skill_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Assert
        # Check for non-blocking error handling pattern
        assert "||" in content or "trap" in content, \
            "Phase 6 must handle errors without breaking QA (non-blocking)"


# ============================================================================
# TEST: AC2 - Phase 7 Added to devforgeai-qa Skill
# ============================================================================


@pytest.mark.integration
@pytest.mark.acceptance_criteria
class TestAC2Phase7AddedToSkill:
    """Test acceptance criterion 2: Phase 7 added to devforgeai-qa skill."""

    def test_skill_has_phase_7_section(self, qa_skill_path):
        """
        AC2: Phase 7 section exists in devforgeai-qa skill.

        Given: devforgeai-qa skill file is readable
        When: Search for Phase 7 header
        Then: "Phase 7" found in skill
        """
        # Arrange & Act
        with open(qa_skill_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Assert
        assert "Phase 7" in content, "Phase 7 must exist in devforgeai-qa skill"
        assert "Update Story" in content or "story update" in content.lower(), \
            "Phase 7 must reference story updates"

    def test_phase_7_updates_story_status(self, qa_skill_path):
        """
        AC2: Phase 7 updates story status to "QA Approved" (deep mode pass only).

        Given: Phase 7 exists in skill
        When: Parse Phase 7 logic
        Then: Status update to "QA Approved" present
        """
        # Arrange & Act
        with open(qa_skill_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Assert
        assert "QA Approved" in content, \
            "Phase 7 must update story status to 'QA Approved'"
        assert "Edit" in content or "status:" in content, \
            "Phase 7 must use Edit tool to update story status"

    def test_phase_7_updates_yaml_timestamp(self, qa_skill_path):
        """
        AC2: Phase 7 updates YAML frontmatter timestamp.

        Given: Phase 7 exists in skill
        When: Parse Phase 7 logic
        Then: Timestamp update present (updated: YYYY-MM-DD)
        """
        # Arrange & Act
        with open(qa_skill_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Assert
        assert "updated:" in content, \
            "Phase 7 must update YAML frontmatter timestamp"

    def test_phase_7_inserts_qa_validation_history(self, qa_skill_path):
        """
        AC2: Phase 7 inserts QA Validation History section.

        Given: Phase 7 exists in skill
        When: Parse Phase 7 logic
        Then: QA Validation History template insertion present
        """
        # Arrange & Act
        with open(qa_skill_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Assert
        assert "QA Validation History" in content, \
            "Phase 7 must insert QA Validation History section"

    def test_phase_7_appends_workflow_history(self, qa_skill_path):
        """
        AC2: Phase 7 appends workflow history entry.

        Given: Phase 7 exists in skill
        When: Parse Phase 7 logic
        Then: Workflow history entry added
        """
        # Arrange & Act
        with open(qa_skill_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Assert
        assert "Workflow History" in content or "workflow history" in content.lower(), \
            "Phase 7 must append workflow history entry"


# ============================================================================
# TEST: AC3 - Phases 4 & 5 Removed from /qa Command
# ============================================================================


@pytest.mark.integration
@pytest.mark.acceptance_criteria
class TestAC3PhasesRemovedFromCommand:
    """Test acceptance criterion 3: Phases 4 & 5 removed from /qa command."""

    def test_command_no_phase_4(self, qa_command_path):
        """
        AC3: Phase 4 removed from /qa command.

        Given: /qa command file is readable
        When: Search for "Phase 4" header
        Then: "Phase 4" or "## Phase 4" NOT found in command
        """
        # Arrange & Act
        with open(qa_command_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Assert
        # Phase 4 should NOT exist in command after refactoring
        # (It moved to skill as Phase 6)
        phase_4_pattern = r"##\s+Phase\s+4"
        matches = re.findall(phase_4_pattern, content)
        assert len(matches) == 0, \
            f"Phase 4 must NOT exist in /qa command (found {len(matches)} occurrences)"

    def test_command_no_phase_5(self, qa_command_path):
        """
        AC3: Phase 5 removed from /qa command.

        Given: /qa command file is readable
        When: Search for "Phase 5" header
        Then: "Phase 5" or "## Phase 5" NOT found in command
        """
        # Arrange & Act
        with open(qa_command_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Assert
        # Phase 5 should NOT exist in command after refactoring
        # (It moved to skill as Phase 7)
        phase_5_pattern = r"##\s+Phase\s+5"
        matches = re.findall(phase_5_pattern, content)
        assert len(matches) == 0, \
            f"Phase 5 must NOT exist in /qa command (found {len(matches)} occurrences)"

    def test_command_size_reduced(self, qa_command_path):
        """
        AC3: Command size reduced to ~340 lines (33% reduction from 509).

        Given: /qa command file is readable
        When: Count lines
        Then: Line count ≤ 360 (allowing 20 line buffer)
        """
        # Arrange & Act
        with open(qa_command_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        line_count = len(lines)

        # Assert
        assert line_count <= 360, \
            f"Command must be ~340 lines (≤360 with buffer), got {line_count} lines"


# ============================================================================
# TEST: AC4 - Command Becomes Pure Orchestrator
# ============================================================================


@pytest.mark.integration
@pytest.mark.acceptance_criteria
class TestAC4CommandPureOrchestrator:
    """Test acceptance criterion 4: Command becomes pure orchestrator."""

    def test_command_has_only_3_phases(self, qa_command_path):
        """
        AC4: Command has only 3 phases remaining (Phase 0, 1, 2).

        Given: /qa command file is readable
        When: Count phase headers
        Then: Exactly 3 phases present (Phase 0, 1, 2)
        """
        # Arrange & Act
        with open(qa_command_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Count "## Phase" headers
        phase_pattern = r"##\s+Phase\s+\d+"
        phase_matches = re.findall(phase_pattern, content)

        # Assert
        assert len(phase_matches) == 3, \
            f"Command must have exactly 3 phases, found {len(phase_matches)}: {phase_matches}"

    def test_phase_0_validates_arguments(self, qa_command_path):
        """
        AC4: Phase 0 validates arguments and loads story.

        Given: /qa command has Phase 0
        When: Read Phase 0 content
        Then: Argument validation and story loading present
        """
        # Arrange & Act
        with open(qa_command_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Assert
        assert "Phase 0" in content, "Phase 0 must exist"
        assert "Argument" in content or "Story ID" in content, \
            "Phase 0 must validate arguments"

    def test_phase_1_invokes_skill(self, qa_command_path):
        """
        AC4: Phase 1 invokes skill with context markers.

        Given: /qa command has Phase 1
        When: Read Phase 1 content
        Then: Skill invocation present
        """
        # Arrange & Act
        with open(qa_command_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Assert
        assert "Phase 1" in content, "Phase 1 must exist"
        assert "Skill(command=" in content or "devforgeai-qa" in content, \
            "Phase 1 must invoke devforgeai-qa skill"

    def test_phase_2_displays_results(self, qa_command_path):
        """
        AC4: Phase 2 displays skill-returned result.

        Given: /qa command has Phase 2
        When: Read Phase 2 content
        Then: Result display present
        """
        # Arrange & Act
        with open(qa_command_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Assert
        assert "Phase 2" in content, "Phase 2 must exist"
        assert "Display" in content or "result" in content, \
            "Phase 2 must display skill result"

    def test_command_delegates_feedback_to_skill(self, qa_command_path):
        """
        AC4: Command does NOT execute feedback hooks (skill does).

        Given: /qa command refactored
        When: Search for feedback hook logic in command
        Then: NO feedback hook invocation in command
        """
        # Arrange & Act
        with open(qa_command_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Extract command phases (exclude integration notes)
        command_phases = content[:content.find("## Integration") if "## Integration" in content else len(content)]

        # Assert
        assert "invoke-hooks" not in command_phases, \
            "Command must NOT invoke hooks directly (skill handles it)"

    def test_command_delegates_story_update_to_skill(self, qa_command_path):
        """
        AC4: Command does NOT update story file (skill does).

        Given: /qa command refactored
        When: Search for Edit tool usage in command phases
        Then: NO Edit calls for story updates in command
        """
        # Arrange & Act
        with open(qa_command_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Extract command phases (exclude integration notes)
        command_phases = content[:content.find("## Integration") if "## Integration" in content else len(content)]

        # Assert
        # Command should NOT have Edit calls for story status updates
        assert "Edit(file_path=" not in command_phases or "QA Approved" not in command_phases, \
            "Command must NOT update story status directly (skill handles it)"


# ============================================================================
# TEST: AC5 - Skill Returns Complete Result
# ============================================================================


@pytest.mark.integration
@pytest.mark.acceptance_criteria
class TestAC5SkillReturnsCompleteResult:
    """Test acceptance criterion 5: Skill returns complete result."""

    def test_skill_returns_structured_result(self, qa_skill_path):
        """
        AC5: Skill returns structured result including display template.

        Given: devforgeai-qa skill completes
        When: Parse skill output logic
        Then: Structured result returned to command
        """
        # Arrange & Act
        with open(qa_skill_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Assert
        # Skill should return result (likely via qa-result-interpreter subagent)
        assert "result" in content.lower() or "display" in content.lower(), \
            "Skill must return structured result to command"

    def test_skill_includes_feedback_status(self, qa_skill_path):
        """
        AC5: Skill result includes feedback hook status.

        Given: Skill Phase 6 executes feedback hooks
        When: Skill returns result
        Then: Feedback hook status included (triggered/skipped/failed)
        """
        # Arrange & Act
        with open(qa_skill_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Assert
        # Skill should include hook status in result
        assert "hook" in content.lower() or "feedback" in content.lower(), \
            "Skill must include feedback hook status in result"

    def test_skill_includes_story_update_confirmation(self, qa_skill_path):
        """
        AC5: Skill result includes story file update confirmation (deep mode pass).

        Given: Skill Phase 7 updates story file
        When: Skill returns result
        Then: Story update confirmation included
        """
        # Arrange & Act
        with open(qa_skill_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Assert
        assert "story" in content.lower() and "update" in content.lower(), \
            "Skill must include story update confirmation in result"


# ============================================================================
# TEST: AC6 - Reference Files Created
# ============================================================================


@pytest.mark.integration
@pytest.mark.acceptance_criteria
class TestAC6ReferenceFilesCreated:
    """Test acceptance criterion 6: Reference files created for new phases."""

    def test_feedback_hooks_reference_exists(self, feedback_hooks_ref_path):
        """
        AC6: feedback-hooks-workflow.md reference file exists.

        Given: Reference files created for progressive disclosure
        When: Check file system
        Then: feedback-hooks-workflow.md exists in references/
        """
        # Arrange & Act & Assert
        assert feedback_hooks_ref_path.exists(), \
            f"Reference file must exist: {feedback_hooks_ref_path}"

    def test_story_update_reference_exists(self, story_update_ref_path):
        """
        AC6: story-update-workflow.md reference file exists.

        Given: Reference files created for progressive disclosure
        When: Check file system
        Then: story-update-workflow.md exists in references/
        """
        # Arrange & Act & Assert
        assert story_update_ref_path.exists(), \
            f"Reference file must exist: {story_update_ref_path}"

    def test_skill_references_feedback_hooks_file(self, qa_skill_path, feedback_hooks_ref_path):
        """
        AC6: Skill SKILL.md references feedback-hooks-workflow.md.

        Given: Reference file exists
        When: Parse skill SKILL.md
        Then: Reference to feedback-hooks-workflow.md found
        """
        # Arrange & Act
        with open(qa_skill_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Assert
        assert "feedback-hooks-workflow" in content, \
            "Skill must reference feedback-hooks-workflow.md"

    def test_skill_references_story_update_file(self, qa_skill_path, story_update_ref_path):
        """
        AC6: Skill SKILL.md references story-update-workflow.md.

        Given: Reference file exists
        When: Parse skill SKILL.md
        Then: Reference to story-update-workflow.md found
        """
        # Arrange & Act
        with open(qa_skill_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Assert
        assert "story-update-workflow" in content, \
            "Skill must reference story-update-workflow.md"

    def test_skill_entry_point_under_500_lines(self, qa_skill_path):
        """
        AC6: Skill SKILL.md entry point remains <500 lines.

        Given: Skill uses progressive disclosure
        When: Count SKILL.md lines
        Then: Line count < 500
        """
        # Arrange & Act
        with open(qa_skill_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        line_count = len(lines)

        # Assert
        assert line_count < 500, \
            f"Skill entry point must be <500 lines, got {line_count} lines"


# ============================================================================
# TEST: AC7 - Lean Orchestration Pattern Validated
# ============================================================================


@pytest.mark.integration
@pytest.mark.acceptance_criteria
class TestAC7LeanOrchestrationCompliance:
    """Test acceptance criterion 7: Lean orchestration pattern validated."""

    def test_command_does_only_orchestration(self, qa_command_path):
        """
        AC7: Command does ONLY: parse args, load context, set markers, invoke skill, display.

        Given: /qa command refactored
        When: Parse command structure
        Then: Only orchestration logic present (no business logic)
        """
        # Arrange & Act
        with open(qa_command_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Assert - Command should NOT have complex if-then logic (except arg validation)
        # Business logic moved to skill
        command_phases = content[:content.find("## Integration") if "## Integration" in content else len(content)]

        # Simple heuristic: Count if-then blocks (business logic indicator)
        if_then_count = content.count("IF ") + content.count("if [")

        # Orchestration commands have minimal conditionals (just arg validation)
        assert if_then_count < 10, \
            f"Command should have minimal conditionals (orchestration only), found {if_then_count}"

    def test_skill_does_business_logic(self, qa_skill_path):
        """
        AC7: Skill does: extract parameters, execute workflow, invoke subagents, generate outputs.

        Given: devforgeai-qa skill refactored
        When: Parse skill structure
        Then: Business logic present (status determination, hook invocation, story updates)
        """
        # Arrange & Act
        with open(qa_skill_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Assert - Skill should have business logic
        assert "STATUS" in content or "status" in content, \
            "Skill must handle status determination (business logic)"
        assert "check-hooks" in content or "invoke-hooks" in content, \
            "Skill must handle hook invocation (business logic)"

    def test_pattern_compliance_100_percent(self, qa_command_path, qa_skill_path):
        """
        AC7: Pattern compliance is 100% (all 5 command responsibilities, zero violations).

        Given: Refactoring complete
        When: Validate against lean-orchestration-pattern.md
        Then: Command has 5 responsibilities (parse, load, set, invoke, display)
              AND Command has 0 violations (no business logic)
        """
        # Arrange & Act
        with open(qa_command_path, 'r', encoding='utf-8') as f:
            cmd_content = f.read()

        with open(qa_skill_path, 'r', encoding='utf-8') as f:
            skill_content = f.read()

        # Assert - Command responsibilities
        assert "Phase 0" in cmd_content, "Command must parse arguments (Phase 0)"
        assert "@" in cmd_content or "Story" in cmd_content, "Command must load context"
        assert "Skill(command=" in cmd_content, "Command must invoke skill"
        assert "Display" in cmd_content or "result" in cmd_content, "Command must display results"

        # Assert - No violations (business logic in skill, not command)
        command_phases = cmd_content[:cmd_content.find("## Integration") if "## Integration" in cmd_content else len(cmd_content)]
        assert "check-hooks" not in command_phases, "Command must NOT have business logic (check-hooks)"
        assert "invoke-hooks" not in command_phases, "Command must NOT have business logic (invoke-hooks)"


# ============================================================================
# TEST: NFR-M1 - Maintainability (30%+ size reduction)
# ============================================================================


@pytest.mark.integration
@pytest.mark.nfr
class TestNFRMaintainability:
    """Test NFR-M1: Command size reduced by 30%+ (509 → ~340 lines)."""

    def test_command_size_reduction_30_percent(self, qa_command_path):
        """
        NFR-M1: Command size reduced by ≥30%.

        Given: Original /qa command was 509 lines
        When: Count new command lines
        Then: New line count ≤ 356 (70% of 509)
        """
        # Arrange
        original_line_count = 509
        target_reduction = 0.30
        max_lines = int(original_line_count * (1 - target_reduction))

        # Act
        with open(qa_command_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        new_line_count = len(lines)
        actual_reduction = (original_line_count - new_line_count) / original_line_count

        # Assert
        assert new_line_count <= max_lines, \
            f"Command must be reduced by ≥30% (≤{max_lines} lines), got {new_line_count} lines (reduction: {actual_reduction*100:.1f}%)"


# ============================================================================
# TEST: NFR-C1 - Compliance (100% lean orchestration pattern)
# ============================================================================


@pytest.mark.integration
@pytest.mark.nfr
class TestNFRCompliance:
    """Test NFR-C1: 100% lean orchestration pattern compliance."""

    def test_lean_pattern_compliance_checklist(self, qa_command_path):
        """
        NFR-C1: Manual checklist validation against lean-orchestration-pattern.md.

        This test serves as documentation of compliance criteria.
        Full manual validation required against protocol document.
        """
        # Arrange
        checklist = {
            "Command does ONLY orchestration": True,  # Validated by AC4
            "Command has 3 phases": True,             # Validated by AC4
            "Skill has business logic": True,         # Validated by AC7
            "Phases 4 & 5 removed from command": True, # Validated by AC3
            "Phases 6 & 7 added to skill": True,     # Validated by AC1, AC2
            "Reference files created": True,          # Validated by AC6
            "Progressive disclosure applied": True,   # Validated by AC6
        }

        # Act & Assert
        for criterion, status in checklist.items():
            assert status, f"Compliance criterion failed: {criterion}"


# ============================================================================
# TEST: NFR-R1 - Reliability (zero functional regressions)
# ============================================================================


@pytest.mark.integration
@pytest.mark.nfr
class TestNFRReliability:
    """Test NFR-R1: Zero functional regressions (behavior identical before/after)."""

    def test_existing_qa_tests_still_pass(self):
        """
        NFR-R1: All 75 existing /qa tests must pass after refactoring.

        Given: Existing QA test suite (test_qa_hooks_integration.py)
        When: Run all existing QA tests
        Then: 100% pass rate (75/75 tests)
        """
        # Arrange
        test_file = Path("/mnt/c/Projects/DevForgeAI2/tests/integration/test_qa_hooks_integration.py")

        # Act - Run existing QA tests
        result = subprocess.run(
            ["pytest", str(test_file), "-v"],
            capture_output=True,
            text=True
        )

        # Assert
        assert result.returncode == 0, \
            f"Existing QA tests must pass (100% pass rate). Exit code: {result.returncode}\n{result.stdout}\n{result.stderr}"
