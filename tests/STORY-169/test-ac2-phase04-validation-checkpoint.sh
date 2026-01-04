#!/bin/bash

# STORY-169: RCA-013 Phase Validation Checkpoint
# AC#2: Phase 3 (Refactoring/Phase 04) Validation Checkpoint
# Status: TDD Red (should FAIL - checkpoint not yet enhanced with explicit validation)
#
# This test verifies that Phase 04 (Refactoring) contains explicit validation
# checkpoint logic that verifies:
# - refactoring-specialist invoked
# - code-reviewer invoked
# - Light QA executed (devforgeai-qa --mode=light)
# - HALT if any check fails

set -e

# Load test library
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/test-lib.sh"

echo "========================================================================"
echo "STORY-169 AC#2: Phase 04 (Refactoring) Validation Checkpoint"
echo "========================================================================"
echo ""

# Test 1: Phase 04 file exists
echo "Test 1: Phase 04 refactoring file exists"
assert_file_exists "$PHASE_04_FILE" "phase-04-refactoring.md should exist"

# Test 2: Validation Checkpoint section exists
echo ""
echo "Test 2: Validation Checkpoint section exists in Phase 04"
PHASE_04_CONTENT=$(cat "$PHASE_04_FILE" 2>/dev/null || echo "")
# Accept either "## Validation Checkpoint" or "## Phase 04 Validation Checkpoint"
if echo "$PHASE_04_CONTENT" | grep -qE "## (Phase 04 )?Validation Checkpoint"; then
    echo -e "${GREEN}PASS${NC} Phase 04 should have Validation Checkpoint section"
    TESTS_RUN=$((TESTS_RUN + 1))
    TESTS_PASSED=$((TESTS_PASSED + 1))
else
    echo -e "${RED}FAIL${NC} Phase 04 should have Validation Checkpoint section"
    TESTS_RUN=$((TESTS_RUN + 1))
    TESTS_FAILED=$((TESTS_FAILED + 1))
fi

# Test 3: Checkpoint verifies refactoring-specialist invoked
echo ""
echo "Test 3: Checkpoint verifies refactoring-specialist invocation"
assert_pattern_exists "$PHASE_04_FILE" \
    "refactoring-specialist" \
    "Checkpoint should verify refactoring-specialist invoked"

# Test 4: Checkpoint verifies code-reviewer invoked
echo ""
echo "Test 4: Checkpoint verifies code-reviewer invocation"
assert_pattern_exists "$PHASE_04_FILE" \
    "code-reviewer" \
    "Checkpoint should verify code-reviewer invoked"

# Test 5: Checkpoint verifies Light QA executed
echo ""
echo "Test 5: Checkpoint verifies Light QA execution"
# Look for Light QA verification in the validation checkpoint
if grep -qiE "(light.*QA|qa.*--mode=light|Light QA.*validat)" "$PHASE_04_FILE"; then
    echo -e "${GREEN}PASS${NC} Phase 04 checkpoint verifies Light QA execution"
    TESTS_RUN=$((TESTS_RUN + 1))
    TESTS_PASSED=$((TESTS_PASSED + 1))
else
    echo -e "${RED}FAIL${NC} Phase 04 checkpoint missing Light QA verification"
    echo "  Expected: Verification of Light QA execution (devforgeai-qa --mode=light)"
    TESTS_RUN=$((TESTS_RUN + 1))
    TESTS_FAILED=$((TESTS_FAILED + 1))
fi

# Test 6: Checkpoint has explicit HALT on failure logic
echo ""
echo "Test 6: Checkpoint has explicit HALT logic for missing subagents"
if grep -qE "(HALT.*workflow|IF.*UNCHECKED.*HALT|HALT.*if.*check.*fail)" "$PHASE_04_FILE"; then
    echo -e "${GREEN}PASS${NC} Phase 04 has HALT logic for checkpoint failures"
    TESTS_RUN=$((TESTS_RUN + 1))
    TESTS_PASSED=$((TESTS_PASSED + 1))
else
    echo -e "${RED}FAIL${NC} Phase 04 missing explicit HALT logic for checkpoint failures"
    echo "  Expected: HALT instruction when validation checkpoint fails"
    TESTS_RUN=$((TESTS_RUN + 1))
    TESTS_FAILED=$((TESTS_FAILED + 1))
fi

# Test 7: NEW - Verify explicit subagent invocation verification template exists
# Per RCA-013 REC-3: Checkpoint should explicitly check for Task() calls
echo ""
echo "Test 7: Phase 04 has explicit subagent invocation verification template"
if grep -qE "Phase.*04.*Validation Checkpoint|### Phase 04 Validation Checkpoint" "$PHASE_04_FILE" && \
   grep -qE "verify.*Task\(\).*call|check.*for.*Task\(\)|invoked.*check" "$PHASE_04_FILE"; then
    echo -e "${GREEN}PASS${NC} Phase 04 has explicit subagent invocation verification"
    TESTS_RUN=$((TESTS_RUN + 1))
    TESTS_PASSED=$((TESTS_PASSED + 1))
else
    echo -e "${RED}FAIL${NC} Phase 04 missing explicit subagent invocation verification template"
    echo "  Expected: Verification that checks for Task() call in conversation"
    echo "  Per Technical Spec: 'verify: refactoring-specialist invoked (check for Task() call)'"
    TESTS_RUN=$((TESTS_RUN + 1))
    TESTS_FAILED=$((TESTS_FAILED + 1))
fi

# Print summary
print_test_summary "AC#2: Phase 04 Validation Checkpoint Tests"
exit_with_result
