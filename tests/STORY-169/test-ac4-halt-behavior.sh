#!/bin/bash

# STORY-169: RCA-013 Phase Validation Checkpoint
# AC#4: HALT Behavior
# Status: TDD Red (should FAIL - HALT behavior template not yet added)
#
# This test verifies that when a validation checkpoint fails:
# - Error message listing missing items is displayed
# - "Complete missing items before proceeding" message is shown
# - Workflow does NOT proceed to next phase

set -e

# Load test library
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/test-lib.sh"

echo "========================================================================"
echo "STORY-169 AC#4: HALT Behavior on Checkpoint Failure"
echo "========================================================================"
echo ""

# Test 1: SKILL.md contains HALT behavior template
echo "Test 1: SKILL.md contains checkpoint HALT behavior template"
SKILL_CONTENT=$(cat "$SKILL_FILE" 2>/dev/null || echo "")

# Look for the technical specification template pattern:
# IF any check fails:
#   Display: "Phase X incomplete: {missing items}"
#   HALT (do not proceed to Phase X+1)
#   Prompt: "Complete missing items before proceeding"

if echo "$SKILL_CONTENT" | grep -qE "Phase.*incomplete.*missing.*items"; then
    echo -e "${GREEN}PASS${NC} SKILL.md contains 'Phase X incomplete: missing items' message"
    TESTS_RUN=$((TESTS_RUN + 1))
    TESTS_PASSED=$((TESTS_PASSED + 1))
else
    echo -e "${RED}FAIL${NC} SKILL.md missing 'Phase X incomplete: missing items' message"
    echo "  Expected: Display template showing which items are missing"
    TESTS_RUN=$((TESTS_RUN + 1))
    TESTS_FAILED=$((TESTS_FAILED + 1))
fi

# Test 2: "Complete missing items before proceeding" message exists
echo ""
echo "Test 2: 'Complete missing items before proceeding' message exists"
if echo "$SKILL_CONTENT" | grep -qi "Complete missing items before proceeding"; then
    echo -e "${GREEN}PASS${NC} Contains 'Complete missing items before proceeding' message"
    TESTS_RUN=$((TESTS_RUN + 1))
    TESTS_PASSED=$((TESTS_PASSED + 1))
else
    echo -e "${RED}FAIL${NC} Missing 'Complete missing items before proceeding' message"
    echo "  Expected: Prompt instructing user to complete missing items"
    TESTS_RUN=$((TESTS_RUN + 1))
    TESTS_FAILED=$((TESTS_FAILED + 1))
fi

# Test 3: HALT explicitly prevents phase progression
echo ""
echo "Test 3: HALT explicitly prevents phase progression"
# Look for "do not proceed" or "HALT" instruction combined with phase reference
if echo "$SKILL_CONTENT" | grep -qiE "(do NOT proceed|HALT.*do not proceed|do not proceed.*Phase)"; then
    echo -e "${GREEN}PASS${NC} HALT behavior explicitly prevents phase progression"
    TESTS_RUN=$((TESTS_RUN + 1))
    TESTS_PASSED=$((TESTS_PASSED + 1))
else
    echo -e "${RED}FAIL${NC} Missing explicit 'do NOT proceed' instruction"
    echo "  Expected: HALT (do not proceed to Phase X+1)"
    TESTS_RUN=$((TESTS_RUN + 1))
    TESTS_FAILED=$((TESTS_FAILED + 1))
fi

# Test 4: Phase 03 contains HALT behavior
echo ""
echo "Test 4: Phase 03 contains HALT behavior with error display"
PHASE_03_CONTENT=$(cat "$PHASE_03_FILE" 2>/dev/null || echo "")
if echo "$PHASE_03_CONTENT" | grep -qE "(HALT.*workflow|IF.*UNCHECKED.*HALT)" && \
   echo "$PHASE_03_CONTENT" | grep -qiE "(missing|incomplete)"; then
    echo -e "${GREEN}PASS${NC} Phase 03 has HALT with error indication"
    TESTS_RUN=$((TESTS_RUN + 1))
    TESTS_PASSED=$((TESTS_PASSED + 1))
else
    echo -e "${RED}FAIL${NC} Phase 03 missing HALT behavior with error display"
    echo "  Expected: HALT with indication of what's missing"
    TESTS_RUN=$((TESTS_RUN + 1))
    TESTS_FAILED=$((TESTS_FAILED + 1))
fi

# Test 5: Phase 04 contains HALT behavior
echo ""
echo "Test 5: Phase 04 contains HALT behavior with error display"
PHASE_04_CONTENT=$(cat "$PHASE_04_FILE" 2>/dev/null || echo "")
if echo "$PHASE_04_CONTENT" | grep -qE "(HALT.*workflow|IF.*UNCHECKED.*HALT)" && \
   echo "$PHASE_04_CONTENT" | grep -qiE "(missing|incomplete)"; then
    echo -e "${GREEN}PASS${NC} Phase 04 has HALT with error indication"
    TESTS_RUN=$((TESTS_RUN + 1))
    TESTS_PASSED=$((TESTS_PASSED + 1))
else
    echo -e "${RED}FAIL${NC} Phase 04 missing HALT behavior with error display"
    echo "  Expected: HALT with indication of what's missing"
    TESTS_RUN=$((TESTS_RUN + 1))
    TESTS_FAILED=$((TESTS_FAILED + 1))
fi

# Test 6: Phase 05 contains HALT behavior
echo ""
echo "Test 6: Phase 05 contains HALT behavior with error display"
PHASE_05_CONTENT=$(cat "$PHASE_05_FILE" 2>/dev/null || echo "")
if echo "$PHASE_05_CONTENT" | grep -qE "(HALT.*workflow|IF.*UNCHECKED.*HALT)" && \
   echo "$PHASE_05_CONTENT" | grep -qiE "(missing|incomplete)"; then
    echo -e "${GREEN}PASS${NC} Phase 05 has HALT with error indication"
    TESTS_RUN=$((TESTS_RUN + 1))
    TESTS_PASSED=$((TESTS_PASSED + 1))
else
    echo -e "${RED}FAIL${NC} Phase 05 missing HALT behavior with error display"
    echo "  Expected: HALT with indication of what's missing"
    TESTS_RUN=$((TESTS_RUN + 1))
    TESTS_FAILED=$((TESTS_FAILED + 1))
fi

# Print summary
print_test_summary "AC#4: HALT Behavior Tests"
exit_with_result
