#!/bin/bash
# STORY-135: Run all Acceptance Criteria tests
# Display-Only Architecture Handoff

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo ""
echo -e "${BLUE}╔════════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║      STORY-135: Display-Only Architecture Handoff          ║${NC}"
echo -e "${BLUE}║                    Test Suite                              ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════════════════════════╝${NC}"
echo ""

TOTAL_PASS=0
TOTAL_FAIL=0
TESTS_RUN=0

run_test() {
    local test_file="$1"
    local test_name="$2"

    echo -e "${YELLOW}Running: $test_name${NC}"
    echo "----------------------------------------"

    if bash "$SCRIPT_DIR/$test_file" 2>&1; then
        ((TOTAL_PASS++))
        echo -e "${GREEN}✓ $test_name PASSED${NC}"
    else
        ((TOTAL_FAIL++))
        echo -e "${RED}✗ $test_name FAILED${NC}"
    fi

    ((TESTS_RUN++))
    echo ""
}

# Continue even when tests fail
set +e

# Run all AC tests
run_test "test-ac1-no-auto-architecture-invocation.sh" "AC#1: No Auto-Architecture Invocation"
run_test "test-ac2-skill-displays-next-action.sh" "AC#2: Skill Displays Next Action"
run_test "test-ac3-display-without-invoking.sh" "AC#3: Display Without Invoking"
run_test "test-ac4-user-control.sh" "AC#4: User Control"

# Summary
echo -e "${BLUE}╔════════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║                    TEST SUMMARY                             ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════════════════════════╝${NC}"
echo ""
echo "Total Tests: $TESTS_RUN"
echo -e "Passed: ${GREEN}$TOTAL_PASS${NC}"
echo -e "Failed: ${RED}$TOTAL_FAIL${NC}"
echo ""

if [ $TOTAL_FAIL -eq 0 ]; then
    echo -e "${GREEN}═══════════════════════════════════════════════════════════${NC}"
    echo -e "${GREEN}  ALL TESTS PASSED - STORY-135 Implementation Complete     ${NC}"
    echo -e "${GREEN}═══════════════════════════════════════════════════════════${NC}"
    exit 0
else
    echo -e "${RED}═══════════════════════════════════════════════════════════${NC}"
    echo -e "${RED}  TESTS FAILED - Implementation Required                    ${NC}"
    echo -e "${RED}═══════════════════════════════════════════════════════════${NC}"
    exit 1
fi
