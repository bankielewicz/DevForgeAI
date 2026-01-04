#!/bin/bash

# STORY-169: RCA-013 Phase Validation Checkpoint
# AC#1: Phase 2 (Implementation/Phase 03) Validation Checkpoint
# Status: TDD Red (should FAIL - checkpoint not yet enhanced with explicit validation)
#
# This test verifies that Phase 03 (Implementation) contains explicit validation
# checkpoint logic that verifies:
# - backend-architect OR frontend-developer invoked
# - context-validator invoked
# - HALT if any check fails

set -e

# Load test library
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/test-lib.sh"

echo "========================================================================"
echo "STORY-169 AC#1: Phase 03 (Implementation) Validation Checkpoint"
echo "========================================================================"
echo ""

# Test 1: Phase 03 file exists
echo "Test 1: Phase 03 implementation file exists"
assert_file_exists "$PHASE_03_FILE" "phase-03-implementation.md should exist"

# Test 2: Validation Checkpoint section exists
echo ""
echo "Test 2: Validation Checkpoint section exists in Phase 03"
PHASE_03_CONTENT=$(cat "$PHASE_03_FILE" 2>/dev/null || echo "")
# Accept either "## Validation Checkpoint" or "## Phase 03 Validation Checkpoint"
if echo "$PHASE_03_CONTENT" | grep -qE "## (Phase 03 )?Validation Checkpoint"; then
    echo -e "${GREEN}PASS${NC} Phase 03 should have Validation Checkpoint section"
    TESTS_RUN=$((TESTS_RUN + 1))
    TESTS_PASSED=$((TESTS_PASSED + 1))
else
    echo -e "${RED}FAIL${NC} Phase 03 should have Validation Checkpoint section"
    TESTS_RUN=$((TESTS_RUN + 1))
    TESTS_FAILED=$((TESTS_FAILED + 1))
fi

# Test 3: Checkpoint verifies backend-architect OR frontend-developer invoked
echo ""
echo "Test 3: Checkpoint verifies backend-architect OR frontend-developer invocation"
assert_pattern_exists "$PHASE_03_FILE" \
    "backend-architect.*OR.*frontend-developer|frontend-developer.*OR.*backend-architect" \
    "Checkpoint should verify backend-architect OR frontend-developer invoked"

# Test 4: Checkpoint verifies context-validator invoked
echo ""
echo "Test 4: Checkpoint verifies context-validator invocation"
assert_pattern_exists "$PHASE_03_FILE" \
    "context-validator" \
    "Checkpoint should verify context-validator invoked"

# Test 5: Checkpoint has explicit HALT on failure logic
# AC#1 requires: "And HALT if any check fails"
echo ""
echo "Test 5: Checkpoint has explicit HALT logic for missing subagents"
# Look for explicit HALT instruction tied to missing subagent verification
if grep -qE "(HALT.*workflow|IF.*UNCHECKED.*HALT|HALT.*if.*check.*fail)" "$PHASE_03_FILE"; then
    echo -e "${GREEN}PASS${NC} Phase 03 has HALT logic for checkpoint failures"
    TESTS_RUN=$((TESTS_RUN + 1))
    TESTS_PASSED=$((TESTS_PASSED + 1))
else
    echo -e "${RED}FAIL${NC} Phase 03 missing explicit HALT logic for checkpoint failures"
    echo "  Expected: HALT instruction when validation checkpoint fails"
    TESTS_RUN=$((TESTS_RUN + 1))
    TESTS_FAILED=$((TESTS_FAILED + 1))
fi

# Test 6: NEW - Verify explicit subagent invocation verification template exists
# Per RCA-013 REC-3: "explicit validation checkpoints at the END of each phase"
echo ""
echo "Test 6: Phase 03 has explicit subagent invocation verification template"
# Look for the new checkpoint template format from STORY-169 Technical Specification
if grep -qE "Phase.*03.*Validation Checkpoint|### Phase 03 Validation Checkpoint" "$PHASE_03_FILE" && \
   grep -qE "verify.*Task\(\).*call|check.*for.*Task\(\)|invoked.*check" "$PHASE_03_FILE"; then
    echo -e "${GREEN}PASS${NC} Phase 03 has explicit subagent invocation verification"
    TESTS_RUN=$((TESTS_RUN + 1))
    TESTS_PASSED=$((TESTS_PASSED + 1))
else
    echo -e "${RED}FAIL${NC} Phase 03 missing explicit subagent invocation verification template"
    echo "  Expected: Verification that checks for Task() call in conversation"
    echo "  Per Technical Spec: 'verify: backend-architect OR frontend-developer invoked (check for Task() call)'"
    TESTS_RUN=$((TESTS_RUN + 1))
    TESTS_FAILED=$((TESTS_FAILED + 1))
fi

# Print summary
print_test_summary "AC#1: Phase 03 Validation Checkpoint Tests"
exit_with_result
