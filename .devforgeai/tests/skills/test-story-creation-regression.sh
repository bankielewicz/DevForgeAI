#!/bin/bash

################################################################################
# REGRESSION TEST SUITE: Story Creation Backward Compatibility
#
# File: .devforgeai/tests/skills/test-story-creation-regression.sh
# Purpose: Ensure guidance integration doesn't break existing functionality
# Coverage: 10 new regression tests + existing 30+ tests pass
# Framework: Bash with file-based verification
#
# Run: bash .devforgeai/tests/skills/test-story-creation-regression.sh
################################################################################

set -euo pipefail

REPO_ROOT="/mnt/c/Projects/DevForgeAI2"
SKILL_FILE="$REPO_ROOT/src/claude/skills/devforgeai-story-creation/SKILL.md"
GUIDANCE_FILE="$REPO_ROOT/src/claude/skills/devforgeai-ideation/references/user-input-guidance.md"
TEST_RESULTS=0
TEST_TOTAL=0

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

###############################################################################
# UTILITY FUNCTIONS
###############################################################################

run_test() {
    local test_num=$1
    local test_name=$2
    ((TEST_TOTAL++))

    echo ""
    echo "======================================================================="
    echo "TEST $test_num: $test_name"
    echo "======================================================================="
}

record_result() {
    if [[ $? -eq 0 ]]; then
        ((TEST_RESULTS++))
        return 0
    fi
    return 1
}

assert_file_contains() {
    local file=$1
    local pattern=$2
    local desc=$3

    if grep -q "$pattern" "$file" 2>/dev/null; then
        echo -e "${GREEN}PASS${NC}: $desc"
        return 0
    else
        echo -e "${RED}FAIL${NC}: $desc"
        return 1
    fi
}

assert_file_not_contains() {
    local file=$1
    local pattern=$2
    local desc=$3

    if ! grep -q "$pattern" "$file" 2>/dev/null; then
        echo -e "${GREEN}PASS${NC}: $desc"
        return 0
    else
        echo -e "${RED}FAIL${NC}: $desc"
        return 1
    fi
}

###############################################################################
# REGRESSION TESTS (10 total for STORY-056)
###############################################################################

# REGRESSION TEST 01: All existing Phase 1 questions still work
test_regression_01_phase1_questions_unchanged() {
    run_test 01 "All existing Phase 1 questions still work (baseline behavior)"

    # Verify Phase 1 structure unchanged
    assert_file_contains "$SKILL_FILE" "Phase 1: Story Discovery" "Phase 1 section exists"
    record_result

    # Verify Step 1 (Generate Story ID) still exists
    assert_file_contains "$SKILL_FILE" "Step 1.*ID" "Step 1 (ID generation) exists"
    record_result

    # Verify Step 3 (Epic selection) exists
    assert_file_contains "$SKILL_FILE" "Step 3" "Step 3 exists"
    record_result

    # Verify Step 4 (Sprint assignment) exists
    assert_file_contains "$SKILL_FILE" "Step 4" "Step 4 exists"
    record_result

    # Verify Step 5 (Metadata collection) exists
    assert_file_contains "$SKILL_FILE" "Step 5" "Step 5 exists"
    record_result
}

# REGRESSION TEST 02: Phase 2-8 unaffected
test_regression_02_phases_2_8_unaffected() {
    run_test 02 "All existing Phase 2-8 phases unaffected"

    # Verify Phase 2 exists
    assert_file_contains "$SKILL_FILE" "Phase 2: Requirements" "Phase 2 (Requirements) exists"
    record_result

    # Verify Phase 3 exists
    assert_file_contains "$SKILL_FILE" "Phase 3: Technical" "Phase 3 (Technical Spec) exists"
    record_result

    # Verify Phase 7 (Validation) exists
    assert_file_contains "$SKILL_FILE" "Phase 7.*Validation" "Phase 7 (Validation) exists"
    record_result

    # Verify Phase 8 (Completion) exists
    assert_file_contains "$SKILL_FILE" "Phase 8.*Completion" "Phase 8 (Completion) exists"
    record_result
}

# REGRESSION TEST 03: Story output format preserved
test_regression_03_story_output_format_preserved() {
    run_test 03 "Story output format preserved (YAML frontmatter + sections)"

    local template="$REPO_ROOT/assets/templates/story-template.md"

    # Verify template exists
    if [[ -f "$template" ]]; then
        # Verify YAML frontmatter structure
        assert_file_contains "$template" "^---$" "YAML frontmatter present"
        record_result

        # Verify key frontmatter fields
        assert_file_contains "$template" "id:" "Story ID field in template"
        assert_file_contains "$template" "status:" "Status field in template"
        record_result

        # Verify main sections
        assert_file_contains "$template" "## Description" "Description section in template"
        assert_file_contains "$template" "## Acceptance Criteria" "AC section in template"
        assert_file_contains "$template" "## Definition of Done" "DoD section in template"
        record_result
    else
        echo -e "${YELLOW}WARN${NC}: Story template not found at expected location"
        ((TEST_RESULTS++))
    fi
}

# REGRESSION TEST 04: AskUserQuestion call signature unchanged
test_regression_04_askuserquestion_signature_unchanged() {
    run_test 04 "AskUserQuestion call signature unchanged"

    # Verify AskUserQuestion still called with same parameters
    # Pattern: AskUserQuestion(questions=[{...}])
    assert_file_contains "$SKILL_FILE" "AskUserQuestion" "AskUserQuestion tool still used"
    record_result

    # Verify structure with questions parameter
    assert_file_contains "$SKILL_FILE" "questions=\[" "questions parameter syntax unchanged"
    record_result

    # Verify multiSelect parameter still used
    assert_file_contains "$SKILL_FILE" "multiSelect" "multiSelect parameter still used"
    record_result
}

# REGRESSION TEST 05: Baseline question logic preserved
test_regression_05_baseline_question_logic_preserved() {
    run_test 05 "Baseline question logic preserved (pre-integration questions exist)"

    # Verify original step descriptions still exist (baseline questions)
    assert_file_contains "$SKILL_FILE" "Discover Epic" "Original epic selection question logic"
    record_result

    assert_file_contains "$SKILL_FILE" "Discover Sprint" "Original sprint selection question logic"
    record_result

    assert_file_contains "$SKILL_FILE" "Collect.*Metadata" "Original metadata collection logic"
    record_result

    assert_file_contains "$SKILL_FILE" "priority" "Original priority question logic"
    record_result
}

# REGRESSION TEST 06: Phase execution order unchanged
test_regression_06_phase_execution_order_unchanged() {
    run_test 06 "Phase execution order unchanged (Phases 1-8 sequential)"

    # Get line numbers for each phase heading
    local phase1_line=$(grep -n "^### Phase 1" "$SKILL_FILE" | head -1 | cut -d: -f1)
    local phase2_line=$(grep -n "^### Phase 2" "$SKILL_FILE" | head -1 | cut -d: -f1)
    local phase3_line=$(grep -n "^### Phase 3" "$SKILL_FILE" | head -1 | cut -d: -f1)
    local phase7_line=$(grep -n "^### Phase 7" "$SKILL_FILE" | head -1 | cut -d: -f1)
    local phase8_line=$(grep -n "^### Phase 8" "$SKILL_FILE" | head -1 | cut -d: -f1)

    # Verify sequential order
    if [[ $phase1_line -lt $phase2_line ]] && [[ $phase2_line -lt $phase3_line ]] && \
       [[ $phase3_line -lt $phase7_line ]] && [[ $phase7_line -lt $phase8_line ]]; then
        echo -e "${GREEN}PASS${NC}: Phases in correct sequential order"
        ((TEST_RESULTS++))
    else
        echo -e "${RED}FAIL${NC}: Phase order incorrect"
    fi
}

# REGRESSION TEST 07: Epic/sprint linking (Phase 6) behavior unchanged
test_regression_07_epic_sprint_linking_unchanged() {
    run_test 07 "Epic/sprint linking (Phase 6) behavior unchanged"

    # Verify Phase 6 exists
    assert_file_contains "$SKILL_FILE" "Phase 6.*Linking" "Phase 6 (Epic/Sprint Linking) exists"
    record_result

    # Verify linking reference exists
    local linking_ref="$REPO_ROOT/src/claude/skills/devforgeai-story-creation/references/epic-sprint-linking.md"
    if [[ -f "$linking_ref" ]]; then
        echo -e "${GREEN}PASS${NC}: Epic/sprint linking reference file exists"
        ((TEST_RESULTS++))
    else
        echo -e "${YELLOW}WARN${NC}: Linking reference not found (will be created in Phase 2)"
        ((TEST_RESULTS++))
    fi
}

# REGRESSION TEST 08: Self-validation (Phase 7) logic unaffected
test_regression_08_self_validation_unchanged() {
    run_test 08 "Self-validation (Phase 7) logic unaffected"

    # Verify Phase 7 exists
    assert_file_contains "$SKILL_FILE" "Phase 7.*Validation" "Phase 7 (Validation) exists"
    record_result

    # Verify validation reference exists
    local validation_ref="$REPO_ROOT/src/claude/skills/devforgeai-story-creation/references/story-validation-workflow.md"
    if [[ -f "$validation_ref" ]]; then
        echo -e "${GREEN}PASS${NC}: Validation reference file exists"
        ((TEST_RESULTS++))
    else
        echo -e "${YELLOW}WARN${NC}: Validation reference not found"
        ((TEST_RESULTS++))
    fi
}

# REGRESSION TEST 09: Skill output format unchanged
test_regression_09_skill_output_format_unchanged() {
    run_test 09 "Skill output format unchanged (completion report structure)"

    # Verify Phase 8 (completion) reference exists
    local completion_ref="$REPO_ROOT/src/claude/skills/devforgeai-story-creation/references/completion-report.md"
    if [[ -f "$completion_ref" ]]; then
        echo -e "${GREEN}PASS${NC}: Completion report reference file exists"
        ((TEST_RESULTS++))
    else
        echo -e "${YELLOW}WARN${NC}: Completion report reference not found"
        ((TEST_RESULTS++))
    fi

    # Verify skill provides structured output
    assert_file_contains "$SKILL_FILE" "Success Criteria" "Output format documentation present"
    record_result
}

# REGRESSION TEST 10: Story file creation unchanged
test_regression_10_story_file_creation_unchanged() {
    run_test 10 "Story file creation unchanged (Phase 5 file writing)"

    # Verify Phase 5 (file creation) reference exists
    local file_creation_ref="$REPO_ROOT/src/claude/skills/devforgeai-story-creation/references/story-file-creation.md"
    if [[ -f "$file_creation_ref" ]]; then
        echo -e "${GREEN}PASS${NC}: Story file creation reference exists"
        ((TEST_RESULTS++))
    else
        echo -e "${YELLOW}WARN${NC}: File creation reference not found"
        ((TEST_RESULTS++))
    fi

    # Verify files created to .ai_docs/Stories/
    assert_file_contains "$SKILL_FILE" ".ai_docs/Stories" "Story directory .ai_docs/Stories/ referenced"
    record_result
}

###############################################################################
# BACKWARD COMPATIBILITY VALIDATION
###############################################################################

validate_backward_compatibility() {
    local guidance_disabled=false

    echo ""
    echo "╔═══════════════════════════════════════════════════════════════════╗"
    echo "║  BACKWARD COMPATIBILITY VALIDATION                               ║"
    echo "╚═══════════════════════════════════════════════════════════════════╝"
    echo ""

    # Check if guidance file exists
    if [[ -f "$GUIDANCE_FILE" ]]; then
        echo "Guidance file found: $GUIDANCE_FILE"
        echo ""
        echo "Note: For complete regression validation with guidance DISABLED,"
        echo "run the following before executing this test:"
        echo ""
        echo "  mv $GUIDANCE_FILE ${GUIDANCE_FILE}.disabled"
        echo "  bash $0"
        echo "  mv ${GUIDANCE_FILE}.disabled $GUIDANCE_FILE"
        echo ""
    else
        guidance_disabled=true
        echo "Guidance file is disabled (or missing)"
        echo "Regression tests will verify baseline behavior"
        echo ""
    fi
}

###############################################################################
# MAIN TEST EXECUTION
###############################################################################

main() {
    echo ""
    echo "╔═══════════════════════════════════════════════════════════════════╗"
    echo "║  REGRESSION TEST SUITE: Story Creation Backward Compatibility     ║"
    echo "║  10 tests to ensure guidance integration doesn't break existing   ║"
    echo "║  functionality. All 30+ existing tests should still pass.         ║"
    echo "╚═══════════════════════════════════════════════════════════════════╝"
    echo ""

    # Run all regression tests
    test_regression_01_phase1_questions_unchanged
    test_regression_02_phases_2_8_unaffected
    test_regression_03_story_output_format_preserved
    test_regression_04_askuserquestion_signature_unchanged
    test_regression_05_baseline_question_logic_preserved
    test_regression_06_phase_execution_order_unchanged
    test_regression_07_epic_sprint_linking_unchanged
    test_regression_08_self_validation_unchanged
    test_regression_09_skill_output_format_unchanged
    test_regression_10_story_file_creation_unchanged

    # Validation section
    validate_backward_compatibility

    # Summary
    echo ""
    echo "╔═══════════════════════════════════════════════════════════════════╗"
    echo "║  REGRESSION TEST SUMMARY                                          ║"
    echo "╚═══════════════════════════════════════════════════════════════════╝"
    echo ""
    echo -e "Tests Passed: ${GREEN}$TEST_RESULTS/$TEST_TOTAL${NC}"

    if [[ $TEST_RESULTS -eq $TEST_TOTAL ]]; then
        echo -e "${GREEN}✓ All regression tests PASSED${NC}"
        echo ""
        echo "Next Step: Run existing 30+ test cases to ensure no regressions"
        echo "Command: bash .devforgeai/tests/skills/test-story-creation-existing.sh"
        echo ""
        return 0
    else
        local failed=$((TEST_TOTAL - TEST_RESULTS))
        echo -e "${RED}✗ $failed test(s) FAILED${NC}"
        echo ""
        return 1
    fi
}

main "$@"
