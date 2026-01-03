#!/bin/bash

################################################################################
# STORY-164 Test Suite Runner
#
# Runs all acceptance criteria tests for:
# STORY-164: RCA-011 Self-Check Display for Phase Completion
#
# Tests validate that self-check displays have been added to:
# .claude/skills/devforgeai-development/SKILL.md
#
# For Phase 2, 3, and 7 completion markers.
#
# Location: devforgeai/tests/STORY-164/run-all-tests.sh
################################################################################

set -uo pipefail
# Note: -e disabled to allow test failures to be counted

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Test directory
TEST_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$TEST_DIR/../../../" # Navigate to project root

# Track overall results
TOTAL_TESTS=0
TOTAL_PASSED=0
TOTAL_FAILED=0

echo ""
echo "╔═══════════════════════════════════════════════════════════════════╗"
echo "║  STORY-164: RCA-011 Self-Check Display for Phase Completion      ║"
echo "║  Test Suite Runner                                               ║"
echo "╚═══════════════════════════════════════════════════════════════════╝"
echo ""

# Define test scripts (actual file names with correct naming convention)
TESTS=(
    "devforgeai/tests/STORY-164/test-ac1-phase2-completion-display.sh"
    "devforgeai/tests/STORY-164/test-ac2-phase3-completion-display.sh"
    "devforgeai/tests/STORY-164/test-ac3-phase7-completion-display.sh"
    "devforgeai/tests/STORY-164/test-ac4-line-number-references.sh"
)

# Run each test
for test_script in "${TESTS[@]}"; do
    if [[ ! -f "$test_script" ]]; then
        echo -e "${RED}✗ SKIP${NC}: Test file not found: $test_script"
        continue
    fi

    echo ""
    echo "Running: $(basename "$test_script")"
    echo "───────────────────────────────────────────────────────────────────"

    # Run test and capture exit code
    if bash "$test_script"; then
        TEST_RESULT=$?
        ((TOTAL_PASSED++))
    else
        TEST_RESULT=$?
        ((TOTAL_FAILED++))
    fi

    ((TOTAL_TESTS++))
done

# Summary
echo ""
echo "╔═══════════════════════════════════════════════════════════════════╗"
echo "║  Test Summary                                                    ║"
echo "╚═══════════════════════════════════════════════════════════════════╝"
echo ""
echo -e "Total Tests Run: ${BLUE}$TOTAL_TESTS${NC}"
echo -e "Passed:          ${GREEN}$TOTAL_PASSED${NC}"
echo -e "Failed:          ${RED}$TOTAL_FAILED${NC}"
echo ""

if [[ $TOTAL_FAILED -eq 0 ]]; then
    echo -e "${GREEN}✓ ALL TESTS PASSED${NC}"
    echo ""
    echo "STORY-164 is ready for implementation!"
    echo ""
    exit 0
else
    echo -e "${RED}✗ SOME TESTS FAILED${NC}"
    echo ""
    echo "Action items:"
    echo "1. Add self-check display sections to SKILL.md for Phases 2, 3, and 7"
    echo "2. Include visual separators and confirmation messages"
    echo "3. Fill in actual conversation line numbers where Task/Skill was invoked"
    echo "4. Re-run this test suite to verify"
    echo ""
    exit 1
fi
