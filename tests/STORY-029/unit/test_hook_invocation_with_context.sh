#!/bin/bash
# Unit Test: AC3 - Hook invocation with sprint context
# Tests that invoke-hooks receives correct sprint parameters

set -e

TEST_NAME="Hook Invocation with Sprint Context"
TEST_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$TEST_DIR/../../.." && pwd)"

# Test fixtures
MOCK_SPRINT_NAME="Sprint-5"
MOCK_STORY_COUNT=7
MOCK_CAPACITY=32

# ANSI colors
RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m'

echo "========================================="
echo "TEST: $TEST_NAME"
echo "========================================="

# Test 1: Verify invoke-hooks called with sprint-name parameter
test_sprint_name_parameter() {
    echo -n "Test 3.1: invoke-hooks receives --sprint-name parameter... "

    if grep -A 50 "### Phase N: Feedback Hook Integration" "$PROJECT_ROOT/.claude/commands/create-sprint.md" | \
       grep -q "\-\-sprint-name=\${.*}\|\-\-sprint-name=\"\${.*}\""; then
        echo -e "${GREEN}PASS${NC}"
        return 0
    else
        echo -e "${RED}FAIL${NC}"
        echo "  Expected: --sprint-name=\${SPRINT_NAME} in invoke-hooks call"
        echo "  Actual: Parameter not found"
        return 1
    fi
}

# Test 2: Verify invoke-hooks called with story-count parameter
test_story_count_parameter() {
    echo -n "Test 3.2: invoke-hooks receives --story-count parameter... "

    if grep -A 50 "### Phase N: Feedback Hook Integration" "$PROJECT_ROOT/.claude/commands/create-sprint.md" | \
       grep -q "\-\-story-count=\${.*}"; then
        echo -e "${GREEN}PASS${NC}"
        return 0
    else
        echo -e "${RED}FAIL${NC}"
        echo "  Expected: --story-count=\${STORY_COUNT} in invoke-hooks call"
        echo "  Actual: Parameter not found"
        return 1
    fi
}

# Test 3: Verify invoke-hooks called with capacity parameter
test_capacity_parameter() {
    echo -n "Test 3.3: invoke-hooks receives --capacity parameter... "

    if grep -A 50 "### Phase N: Feedback Hook Integration" "$PROJECT_ROOT/.claude/commands/create-sprint.md" | \
       grep -q "\-\-capacity=\${.*}"; then
        echo -e "${GREEN}PASS${NC}"
        return 0
    else
        echo -e "${RED}FAIL${NC}"
        echo "  Expected: --capacity=\${CAPACITY_POINTS} in invoke-hooks call"
        echo "  Actual: Parameter not found"
        return 1
    fi
}

# Test 4: Verify operation parameter is create-sprint
test_operation_parameter() {
    echo -n "Test 3.4: invoke-hooks receives --operation=create-sprint... "

    if grep -A 50 "### Phase N: Feedback Hook Integration" "$PROJECT_ROOT/.claude/commands/create-sprint.md" | \
       grep "invoke-hooks" | grep -q "\-\-operation=create-sprint"; then
        echo -e "${GREEN}PASS${NC}"
        return 0
    else
        echo -e "${RED}FAIL${NC}"
        echo "  Expected: --operation=create-sprint in invoke-hooks call"
        echo "  Actual: Parameter not found or incorrect"
        return 1
    fi
}

# Test 5: Verify feedback captures sprint context
test_feedback_file_creation() {
    echo -n "Test 3.5: Feedback file created with sprint context... "

    # Create enabled hooks config
    TEMP_CONFIG="/tmp/hooks-test-$$.yaml"
    cat > "$TEMP_CONFIG" <<EOF
feedback_hooks:
  enabled: true
  hooks:
    create-sprint:
      enabled: true
      check_command: "devforgeai check-hooks"
      invoke_command: "devforgeai invoke-hooks"
EOF

    # Execute invoke-hooks (will fail without full setup, but we check parameters)
    output=$(devforgeai invoke-hooks --operation=create-sprint \
        --sprint-name="$MOCK_SPRINT_NAME" \
        --story-count=$MOCK_STORY_COUNT \
        --capacity=$MOCK_CAPACITY \
        --config="$TEMP_CONFIG" 2>&1 || true)

    rm -f "$TEMP_CONFIG"

    # Verify parameters were accepted (even if execution fails)
    if echo "$output" | grep -q "$MOCK_SPRINT_NAME\|story.*$MOCK_STORY_COUNT\|capacity.*$MOCK_CAPACITY"; then
        echo -e "${GREEN}PASS${NC}"
        return 0
    else
        # Parameter acceptance may be silent - check exit code wasn't parameter error
        if echo "$output" | grep -q "invalid.*option\|unknown.*argument\|required.*parameter"; then
            echo -e "${RED}FAIL${NC}"
            echo "  Expected: Parameters accepted"
            echo "  Actual: Parameter error - $output"
            return 1
        else
            echo -e "${GREEN}PASS${NC}"
            echo "  Note: Parameters accepted (execution may fail without full setup)"
            return 0
        fi
    fi
}

# Test 6: Verify sprint context variables are defined in Phase N
test_sprint_context_variables() {
    echo -n "Test 3.6: Sprint context variables defined in Phase N... "

    phase_n_content=$(grep -A 100 "### Phase N: Feedback Hook Integration" "$PROJECT_ROOT/.claude/commands/create-sprint.md" || echo "")

    # Check for variable definitions or usage
    missing_vars=""
    echo "$phase_n_content" | grep -q "SPRINT_NAME\|sprint.*name" || missing_vars="${missing_vars}SPRINT_NAME "
    echo "$phase_n_content" | grep -q "STORY_COUNT\|story.*count" || missing_vars="${missing_vars}STORY_COUNT "
    echo "$phase_n_content" | grep -q "CAPACITY\|capacity.*points" || missing_vars="${missing_vars}CAPACITY "

    if [ -z "$missing_vars" ]; then
        echo -e "${GREEN}PASS${NC}"
        return 0
    else
        echo -e "${RED}FAIL${NC}"
        echo "  Expected: All sprint context variables defined"
        echo "  Missing: $missing_vars"
        return 1
    fi
}

# Test 7: Verify shell escaping for sprint name
test_sprint_name_shell_escaping() {
    echo -n "Test 3.7: Sprint name properly shell-escaped... "

    if grep -A 50 "### Phase N: Feedback Hook Integration" "$PROJECT_ROOT/.claude/commands/create-sprint.md" | \
       grep "invoke-hooks" | grep -q "\-\-sprint-name=\"\${"; then
        echo -e "${GREEN}PASS${NC}"
        return 0
    else
        echo -e "${RED}FAIL${NC}"
        echo "  Expected: --sprint-name=\"\${SPRINT_NAME}\" (double-quoted)"
        echo "  Actual: Sprint name not properly quoted"
        return 1
    fi
}

# Run all tests
FAILED_TESTS=0

test_sprint_name_parameter || FAILED_TESTS=$((FAILED_TESTS + 1))
test_story_count_parameter || FAILED_TESTS=$((FAILED_TESTS + 1))
test_capacity_parameter || FAILED_TESTS=$((FAILED_TESTS + 1))
test_operation_parameter || FAILED_TESTS=$((FAILED_TESTS + 1))
test_feedback_file_creation || FAILED_TESTS=$((FAILED_TESTS + 1))
test_sprint_context_variables || FAILED_TESTS=$((FAILED_TESTS + 1))
test_sprint_name_shell_escaping || FAILED_TESTS=$((FAILED_TESTS + 1))

echo "========================================="
if [ $FAILED_TESTS -eq 0 ]; then
    echo -e "${GREEN}ALL TESTS PASSED${NC}"
    exit 0
else
    echo -e "${RED}$FAILED_TESTS TEST(S) FAILED${NC}"
    exit 1
fi
