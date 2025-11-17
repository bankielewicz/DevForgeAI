#!/bin/bash
# Unit Test: AC2 - Graceful degradation when hooks disabled
# Tests that sprint creation succeeds when hooks are disabled

set -e

TEST_NAME="Graceful Degradation - Hooks Disabled"
TEST_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$TEST_DIR/../../.." && pwd)"

# Test fixtures
HOOKS_CONFIG_PATH="$PROJECT_ROOT/.devforgeai/config/hooks.yaml"
TEMP_HOOKS_CONFIG="/tmp/hooks-test-$$.yaml"

# ANSI colors
RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m'

echo "========================================="
echo "TEST: $TEST_NAME"
echo "========================================="

# Setup: Create disabled hooks config
setup_disabled_hooks() {
    cat > "$TEMP_HOOKS_CONFIG" <<EOF
feedback_hooks:
  enabled: true
  hooks:
    create-sprint:
      enabled: false
      check_command: "devforgeai check-hooks"
      invoke_command: "devforgeai invoke-hooks"
EOF
}

# Teardown: Remove temp config
teardown() {
    rm -f "$TEMP_HOOKS_CONFIG"
}

trap teardown EXIT

# Test 1: check-hooks returns non-zero when disabled
test_check_hooks_disabled_exit_code() {
    echo -n "Test 2.1: check-hooks returns non-zero when disabled... "

    setup_disabled_hooks

    # Execute check-hooks with disabled config
    if devforgeai check-hooks --operation=create-sprint --status=success --config="$TEMP_HOOKS_CONFIG" 2>/dev/null; then
        echo -e "${RED}FAIL${NC}"
        echo "  Expected: Non-zero exit code"
        echo "  Actual: Exit code 0 (hooks reported as enabled)"
        return 1
    else
        exit_code=$?
        if [ $exit_code -eq 1 ]; then
            echo -e "${GREEN}PASS${NC}"
            return 0
        else
            echo -e "${RED}FAIL${NC}"
            echo "  Expected: Exit code 1"
            echo "  Actual: Exit code $exit_code"
            return 1
        fi
    fi
}

# Test 2: Phase N skips hook invocation when check fails
test_hook_invocation_skipped() {
    echo -n "Test 2.2: Hook invocation skipped when check fails... "

    # Check if create-sprint.md has conditional logic for hook invocation
    if grep -A 20 "### Phase N: Feedback Hook Integration" "$PROJECT_ROOT/.claude/commands/create-sprint.md" | \
       grep -q "IF.*exit.*0\|if.*success\|when.*enabled"; then
        echo -e "${GREEN}PASS${NC}"
        return 0
    else
        echo -e "${RED}FAIL${NC}"
        echo "  Expected: Conditional hook invocation based on check-hooks exit code"
        echo "  Actual: No conditional logic found"
        return 1
    fi
}

# Test 3: Sprint creation completes successfully with hooks disabled
test_sprint_creation_succeeds() {
    echo -n "Test 2.3: Sprint creation succeeds with hooks disabled... "

    # Simulate sprint creation with disabled hooks
    # This would require full command execution - for now, verify command structure
    # Extract ONLY Phase N section (until next ### header)
    if sed -n '/### Phase N: Feedback Hook Integration/,/^###/p' "$PROJECT_ROOT/.claude/commands/create-sprint.md" | \
       grep -v "^###" | grep -q "HALT\|exit 1\|return 1"; then
        echo -e "${RED}FAIL${NC}"
        echo "  Expected: No HALT/exit in Phase N"
        echo "  Actual: Found blocking command (HALT/exit/return)"
        return 1
    else
        echo -e "${GREEN}PASS${NC}"
        return 0
    fi
}

# Test 4: No feedback prompts when hooks disabled
test_no_feedback_prompts() {
    echo -n "Test 2.4: No feedback prompts when hooks disabled... "

    # Verify that invoke-hooks is NOT called when check returns non-zero
    if grep -A 50 "### Phase N: Feedback Hook Integration" "$PROJECT_ROOT/.claude/commands/create-sprint.md" | \
       grep -B 5 "invoke-hooks" | grep -q "IF.*check.*0\|if.*success"; then
        echo -e "${GREEN}PASS${NC}"
        return 0
    else
        echo -e "${RED}FAIL${NC}"
        echo "  Expected: invoke-hooks only called when check succeeds"
        echo "  Actual: No conditional found"
        return 1
    fi
}

# Test 5: Disabled hook logged correctly
test_disabled_hook_logging() {
    echo -n "Test 2.5: Disabled hook status logged... "

    setup_disabled_hooks

    # Execute check-hooks and verify log output
    output=$(devforgeai check-hooks --operation=create-sprint --status=success --config="$TEMP_HOOKS_CONFIG" 2>&1 || true)

    if echo "$output" | grep -q "disabled\|not enabled\|skipped"; then
        echo -e "${GREEN}PASS${NC}"
        return 0
    else
        echo -e "${RED}FAIL${NC}"
        echo "  Expected: Log message indicating hooks disabled"
        echo "  Actual: $output"
        return 1
    fi
}

# Run all tests
FAILED_TESTS=0

test_check_hooks_disabled_exit_code || FAILED_TESTS=$((FAILED_TESTS + 1))
test_hook_invocation_skipped || FAILED_TESTS=$((FAILED_TESTS + 1))
test_sprint_creation_succeeds || FAILED_TESTS=$((FAILED_TESTS + 1))
test_no_feedback_prompts || FAILED_TESTS=$((FAILED_TESTS + 1))
test_disabled_hook_logging || FAILED_TESTS=$((FAILED_TESTS + 1))

echo "========================================="
if [ $FAILED_TESTS -eq 0 ]; then
    echo -e "${GREEN}ALL TESTS PASSED${NC}"
    exit 0
else
    echo -e "${RED}$FAILED_TESTS TEST(S) FAILED${NC}"
    exit 1
fi
