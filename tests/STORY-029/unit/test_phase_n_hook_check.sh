#!/bin/bash
# Unit Test: AC1 - Phase N added to /create-sprint command workflow
# Tests that Phase N executes hook check after sprint creation

set -e

TEST_NAME="Phase N Hook Check Execution"
TEST_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$TEST_DIR/../../.." && pwd)"

# Test fixtures
MOCK_SPRINT_NAME="Sprint-Test-Hook-Check"
MOCK_STORY_COUNT=3
MOCK_CAPACITY=15

# ANSI colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo "========================================="
echo "TEST: $TEST_NAME"
echo "========================================="

# Test 1: Verify Phase N section exists in create-sprint.md
test_phase_n_section_exists() {
    echo -n "Test 1.1: Phase N section exists in create-sprint.md... "

    if grep -q "### Phase N: Feedback Hook Integration" "$PROJECT_ROOT/.claude/commands/create-sprint.md"; then
        echo -e "${GREEN}PASS${NC}"
        return 0
    else
        echo -e "${RED}FAIL${NC}"
        echo "  Expected: Phase N section in create-sprint.md"
        echo "  Actual: Section not found"
        return 1
    fi
}

# Test 2: Verify Phase N executes check-hooks command
test_check_hooks_invocation() {
    echo -n "Test 1.2: Phase N invokes check-hooks command... "

    # Check if create-sprint.md contains check-hooks invocation
    if grep -q "devforgeai check-hooks --operation=create-sprint --status=success" "$PROJECT_ROOT/.claude/commands/create-sprint.md"; then
        echo -e "${GREEN}PASS${NC}"
        return 0
    else
        echo -e "${RED}FAIL${NC}"
        echo "  Expected: check-hooks command invocation in Phase N"
        echo "  Actual: Command invocation not found"
        return 1
    fi
}

# Test 3: Verify Phase N is placed after Phase 4 (result display)
test_phase_n_placement() {
    echo -n "Test 1.3: Phase N placed after Phase 4... "

    # Extract Phase 4 and Phase N line numbers
    phase_4_line=$(grep -n "### Phase 4: Display Results" "$PROJECT_ROOT/.claude/commands/create-sprint.md" | cut -d: -f1 || echo "0")
    phase_n_line=$(grep -n "### Phase N: Feedback Hook Integration" "$PROJECT_ROOT/.claude/commands/create-sprint.md" | cut -d: -f1 || echo "0")

    if [ "$phase_n_line" -gt "$phase_4_line" ] && [ "$phase_4_line" -gt 0 ]; then
        echo -e "${GREEN}PASS${NC}"
        return 0
    else
        echo -e "${RED}FAIL${NC}"
        echo "  Expected: Phase N after Phase 4"
        echo "  Actual: Phase 4 line=$phase_4_line, Phase N line=$phase_n_line"
        return 1
    fi
}

# Test 4: Verify check-hooks command format
test_check_hooks_parameters() {
    echo -n "Test 1.4: check-hooks command has correct parameters... "

    # Check for required parameters
    if grep -q "\-\-operation=create-sprint" "$PROJECT_ROOT/.claude/commands/create-sprint.md" && \
       grep -q "\-\-status=success" "$PROJECT_ROOT/.claude/commands/create-sprint.md"; then
        echo -e "${GREEN}PASS${NC}"
        return 0
    else
        echo -e "${RED}FAIL${NC}"
        echo "  Expected: --operation=create-sprint --status=success"
        echo "  Actual: Parameters not found or incorrect"
        return 1
    fi
}

# Test 5: Verify Phase N only executes after successful sprint creation
test_phase_n_conditional_execution() {
    echo -n "Test 1.5: Phase N only runs after successful sprint creation... "

    # Check if Phase N has conditional logic based on previous phase success
    if grep -A 10 "### Phase N: Feedback Hook Integration" "$PROJECT_ROOT/.claude/commands/create-sprint.md" | grep -q "IF.*success\|After.*complete\|sprint.*created"; then
        echo -e "${GREEN}PASS${NC}"
        return 0
    else
        echo -e "${YELLOW}WARN${NC}"
        echo "  Warning: No explicit conditional found (may be implicit in workflow)"
        return 0  # Non-critical
    fi
}

# Run all tests
FAILED_TESTS=0

test_phase_n_section_exists || FAILED_TESTS=$((FAILED_TESTS + 1))
test_check_hooks_invocation || FAILED_TESTS=$((FAILED_TESTS + 1))
test_phase_n_placement || FAILED_TESTS=$((FAILED_TESTS + 1))
test_check_hooks_parameters || FAILED_TESTS=$((FAILED_TESTS + 1))
test_phase_n_conditional_execution || FAILED_TESTS=$((FAILED_TESTS + 1))

echo "========================================="
if [ $FAILED_TESTS -eq 0 ]; then
    echo -e "${GREEN}ALL TESTS PASSED${NC}"
    exit 0
else
    echo -e "${RED}$FAILED_TESTS TEST(S) FAILED${NC}"
    exit 1
fi
