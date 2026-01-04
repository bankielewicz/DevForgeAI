#!/bin/bash

# STORY-169: RCA-013 Phase Validation Checkpoint
# AC#5: PASS Behavior
# Status: TDD Red (should FAIL - PASS behavior template not yet added)
#
# This test verifies that when all mandatory subagents are verified:
# - Display: "Phase X validation passed - all mandatory steps completed"
# - Proceed to next phase

set -e

# Load test library
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/test-lib.sh"

echo "========================================================================"
echo "STORY-169 AC#5: PASS Behavior on Checkpoint Success"
echo "========================================================================"
echo ""

# Test 1: SKILL.md contains PASS behavior template
echo "Test 1: SKILL.md contains checkpoint PASS behavior template"
SKILL_CONTENT=$(cat "$SKILL_FILE" 2>/dev/null || echo "")

# Look for the technical specification template pattern:
# IF all checks pass:
#   Display: "Phase X validation passed - all mandatory steps completed"
#   Proceed to Phase X+1

if echo "$SKILL_CONTENT" | grep -qiE "Phase.*validation passed.*all mandatory steps completed"; then
    echo -e "${GREEN}PASS${NC} SKILL.md contains 'Phase X validation passed - all mandatory steps completed' message"
    TESTS_RUN=$((TESTS_RUN + 1))
    TESTS_PASSED=$((TESTS_PASSED + 1))
else
    echo -e "${RED}FAIL${NC} SKILL.md missing 'Phase X validation passed - all mandatory steps completed' message"
    echo "  Expected: Display template confirming all mandatory steps completed"
    TESTS_RUN=$((TESTS_RUN + 1))
    TESTS_FAILED=$((TESTS_FAILED + 1))
fi

# Test 2: PASS behavior includes proceed instruction
echo ""
echo "Test 2: PASS behavior includes 'Proceed to Phase X+1' instruction"
if echo "$SKILL_CONTENT" | grep -qiE "(Proceed to Phase|proceed.*next phase|Proceeding to Phase)"; then
    echo -e "${GREEN}PASS${NC} Contains proceed to next phase instruction"
    TESTS_RUN=$((TESTS_RUN + 1))
    TESTS_PASSED=$((TESTS_PASSED + 1))
else
    echo -e "${RED}FAIL${NC} Missing proceed to next phase instruction"
    echo "  Expected: Proceed to Phase X+1"
    TESTS_RUN=$((TESTS_RUN + 1))
    TESTS_FAILED=$((TESTS_FAILED + 1))
fi

# Test 3: Phase 03 contains PASS behavior with success message
echo ""
echo "Test 3: Phase 03 contains PASS behavior with success message"
PHASE_03_CONTENT=$(cat "$PHASE_03_FILE" 2>/dev/null || echo "")
# Look for validation passed message or all checks pass logic
if echo "$PHASE_03_CONTENT" | grep -qiE "(validation passed|all.*checks.*pass|proceed.*Phase 04|Proceeding to Phase)"; then
    echo -e "${GREEN}PASS${NC} Phase 03 has PASS behavior"
    TESTS_RUN=$((TESTS_RUN + 1))
    TESTS_PASSED=$((TESTS_PASSED + 1))
else
    echo -e "${RED}FAIL${NC} Phase 03 missing PASS behavior with success message"
    echo "  Expected: Success message and proceed instruction"
    TESTS_RUN=$((TESTS_RUN + 1))
    TESTS_FAILED=$((TESTS_FAILED + 1))
fi

# Test 4: Phase 04 contains PASS behavior with success message
echo ""
echo "Test 4: Phase 04 contains PASS behavior with success message"
PHASE_04_CONTENT=$(cat "$PHASE_04_FILE" 2>/dev/null || echo "")
if echo "$PHASE_04_CONTENT" | grep -qiE "(validation passed|all.*checks.*pass|proceed.*Phase 05|Proceeding to Phase)"; then
    echo -e "${GREEN}PASS${NC} Phase 04 has PASS behavior"
    TESTS_RUN=$((TESTS_RUN + 1))
    TESTS_PASSED=$((TESTS_PASSED + 1))
else
    echo -e "${RED}FAIL${NC} Phase 04 missing PASS behavior with success message"
    echo "  Expected: Success message and proceed instruction"
    TESTS_RUN=$((TESTS_RUN + 1))
    TESTS_FAILED=$((TESTS_FAILED + 1))
fi

# Test 5: Phase 05 contains PASS behavior with success message
echo ""
echo "Test 5: Phase 05 contains PASS behavior with success message"
PHASE_05_CONTENT=$(cat "$PHASE_05_FILE" 2>/dev/null || echo "")
if echo "$PHASE_05_CONTENT" | grep -qiE "(validation passed|all.*checks.*pass|proceed.*Phase 06|Proceeding to Phase)"; then
    echo -e "${GREEN}PASS${NC} Phase 05 has PASS behavior"
    TESTS_RUN=$((TESTS_RUN + 1))
    TESTS_PASSED=$((TESTS_PASSED + 1))
else
    echo -e "${RED}FAIL${NC} Phase 05 missing PASS behavior with success message"
    echo "  Expected: Success message and proceed instruction"
    TESTS_RUN=$((TESTS_RUN + 1))
    TESTS_FAILED=$((TESTS_FAILED + 1))
fi

# Test 6: NEW - Verify explicit "IF all checks pass" conditional exists
# Per Technical Specification: This is the expected checkpoint template format
echo ""
echo "Test 6: Checkpoint template has 'IF all checks pass' conditional"
if echo "$SKILL_CONTENT" | grep -qiE "IF.*all.*checks.*pass"; then
    echo -e "${GREEN}PASS${NC} Checkpoint has 'IF all checks pass' conditional"
    TESTS_RUN=$((TESTS_RUN + 1))
    TESTS_PASSED=$((TESTS_PASSED + 1))
else
    echo -e "${RED}FAIL${NC} Missing 'IF all checks pass' conditional in checkpoint template"
    echo "  Expected: IF all checks pass: Display: 'Phase X validation passed...'"
    TESTS_RUN=$((TESTS_RUN + 1))
    TESTS_FAILED=$((TESTS_FAILED + 1))
fi

# Print summary
print_test_summary "AC#5: PASS Behavior Tests"
exit_with_result
