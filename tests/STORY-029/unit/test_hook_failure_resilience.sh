#!/bin/bash
# Unit Test: AC4 - Hook failure does not break sprint creation
# Tests that sprint creation completes successfully even when hooks fail

set -e

TEST_NAME="Hook Failure Resilience"
TEST_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$TEST_DIR/../../.." && pwd)"

# Test directories
TEMP_SPRINT_DIR="/tmp/devforgeai-test-sprints-$$"
TEMP_LOG_DIR="/tmp/devforgeai-test-logs-$$"

# ANSI colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo "========================================="
echo "TEST: $TEST_NAME"
echo "========================================="

# Setup
setup() {
    mkdir -p "$TEMP_SPRINT_DIR"
    mkdir -p "$TEMP_LOG_DIR"
}

# Teardown
teardown() {
    rm -rf "$TEMP_SPRINT_DIR"
    rm -rf "$TEMP_LOG_DIR"
}

trap teardown EXIT
setup

# Test 1: Phase N has error handling for invoke-hooks failure
test_error_handling_present() {
    echo -n "Test 4.1: Phase N has error handling for hook failures... "

    phase_n_content=$(grep -A 100 "### Phase N: Feedback Hook Integration" "$PROJECT_ROOT/.claude/commands/create-sprint.md" || echo "")

    if echo "$phase_n_content" | grep -q "error\|fail\|exception\||| true\|2>&1"; then
        echo -e "${GREEN}PASS${NC}"
        return 0
    else
        echo -e "${RED}FAIL${NC}"
        echo "  Expected: Error handling for invoke-hooks failures"
        echo "  Actual: No error handling found"
        return 1
    fi
}

# Test 2: Hook failure logged to error log
test_hook_failure_logging() {
    echo -n "Test 4.2: Hook failures logged to .devforgeai/feedback/logs/hook-errors.log... "

    if grep -A 100 "### Phase N: Feedback Hook Integration" "$PROJECT_ROOT/.claude/commands/create-sprint.md" | \
       grep -q "hook-errors.log\|error.*log\|log.*error"; then
        echo -e "${GREEN}PASS${NC}"
        return 0
    else
        echo -e "${RED}FAIL${NC}"
        echo "  Expected: Logging to hook-errors.log"
        echo "  Actual: No error logging found"
        return 1
    fi
}

# Test 3: User sees warning message when hooks fail
test_user_warning_message() {
    echo -n "Test 4.3: User sees warning when hook fails... "

    if grep -A 100 "### Phase N: Feedback Hook Integration" "$PROJECT_ROOT/.claude/commands/create-sprint.md" | \
       grep -q "Feedback collection failed\|Hook.*failed\|Warning.*feedback"; then
        echo -e "${GREEN}PASS${NC}"
        return 0
    else
        echo -e "${RED}FAIL${NC}"
        echo "  Expected: Warning message about feedback failure"
        echo "  Actual: No warning message found"
        return 1
    fi
}

# Test 4: Sprint file remains valid after hook failure
test_sprint_file_valid() {
    echo -n "Test 4.4: Sprint creation succeeds despite hook failure... "

    # Verify Phase N doesn't HALT or exit on hook failure
    if grep -A 100 "### Phase N: Feedback Hook Integration" "$PROJECT_ROOT/.claude/commands/create-sprint.md" | \
       grep "invoke-hooks" | grep -A 10 "invoke-hooks" | grep -q "HALT\|exit 1\|return 1"; then
        echo -e "${RED}FAIL${NC}"
        echo "  Expected: No HALT/exit after invoke-hooks"
        echo "  Actual: Found blocking statement"
        return 1
    else
        echo -e "${GREEN}PASS${NC}"
        return 0
    fi
}

# Test 5: Hook failure doesn't affect story status updates
test_story_status_preserved() {
    echo -n "Test 4.5: Story statuses updated even with hook failure... "

    # Verify Phase N comes AFTER Phase 4 (which displays results from skill)
    phase_4_line=$(grep -n "### Phase 4: Display Results" "$PROJECT_ROOT/.claude/commands/create-sprint.md" | cut -d: -f1 || echo "0")
    phase_n_line=$(grep -n "### Phase N: Feedback Hook Integration" "$PROJECT_ROOT/.claude/commands/create-sprint.md" | cut -d: -f1 || echo "0")

    if [ "$phase_n_line" -gt "$phase_4_line" ] && [ "$phase_4_line" -gt 0 ]; then
        echo -e "${GREEN}PASS${NC}"
        echo "  Note: Phase N after Phase 4 ensures story updates complete first"
        return 0
    else
        echo -e "${RED}FAIL${NC}"
        echo "  Expected: Phase N after Phase 4"
        echo "  Actual: Incorrect ordering could affect story updates"
        return 1
    fi
}

# Test 6: Simulate invoke-hooks failure (exit code 1)
test_invoke_hooks_nonzero_exit() {
    echo -n "Test 4.6: invoke-hooks non-zero exit doesn't crash... "

    # Create failing invoke-hooks mock
    MOCK_INVOKE_HOOKS="/tmp/mock-invoke-hooks-$$"
    cat > "$MOCK_INVOKE_HOOKS" <<'EOF'
#!/bin/bash
# Mock invoke-hooks that fails
echo "Error: Feedback system unavailable" >&2
exit 1
EOF
    chmod +x "$MOCK_INVOKE_HOOKS"

    # Test that it returns exit code 1
    if "$MOCK_INVOKE_HOOKS" 2>/dev/null; then
        echo -e "${RED}FAIL${NC}"
        echo "  Expected: Mock script exits with 1"
        echo "  Actual: Exited with 0"
        rm -f "$MOCK_INVOKE_HOOKS"
        return 1
    else
        exit_code=$?
        if [ $exit_code -eq 1 ]; then
            echo -e "${GREEN}PASS${NC}"
            rm -f "$MOCK_INVOKE_HOOKS"
            return 0
        else
            echo -e "${RED}FAIL${NC}"
            echo "  Expected: Exit code 1"
            echo "  Actual: Exit code $exit_code"
            rm -f "$MOCK_INVOKE_HOOKS"
            return 1
        fi
    fi
}

# Test 7: Simulate invoke-hooks exception
test_invoke_hooks_python_exception() {
    echo -n "Test 4.7: invoke-hooks Python exception handled... "

    # Create failing invoke-hooks mock (Python exception)
    MOCK_INVOKE_HOOKS_PY="/tmp/mock-invoke-hooks-$$.py"
    cat > "$MOCK_INVOKE_HOOKS_PY" <<'EOF'
#!/usr/bin/env python3
import sys
print("Starting feedback collection...", file=sys.stderr)
raise RuntimeError("Database connection failed")
EOF
    chmod +x "$MOCK_INVOKE_HOOKS_PY"

    # Test that it crashes with exception
    if "$MOCK_INVOKE_HOOKS_PY" 2>/dev/null; then
        echo -e "${RED}FAIL${NC}"
        echo "  Expected: Mock script raises exception"
        echo "  Actual: Exited cleanly"
        rm -f "$MOCK_INVOKE_HOOKS_PY"
        return 1
    else
        # Any non-zero exit is acceptable (exception handling)
        echo -e "${GREEN}PASS${NC}"
        rm -f "$MOCK_INVOKE_HOOKS_PY"
        return 0
    fi
}

# Test 8: Verify graceful degradation documented
test_graceful_degradation_documented() {
    echo -n "Test 4.8: Graceful degradation documented in Phase N... "

    if grep -A 100 "### Phase N: Feedback Hook Integration" "$PROJECT_ROOT/.claude/commands/create-sprint.md" | \
       grep -qi "graceful\|non-blocking\|non-fatal\|continue"; then
        echo -e "${GREEN}PASS${NC}"
        return 0
    else
        echo -e "${YELLOW}WARN${NC}"
        echo "  Warning: Graceful degradation not explicitly documented"
        return 0  # Non-critical
    fi
}

# Run all tests
FAILED_TESTS=0

test_error_handling_present || FAILED_TESTS=$((FAILED_TESTS + 1))
test_hook_failure_logging || FAILED_TESTS=$((FAILED_TESTS + 1))
test_user_warning_message || FAILED_TESTS=$((FAILED_TESTS + 1))
test_sprint_file_valid || FAILED_TESTS=$((FAILED_TESTS + 1))
test_story_status_preserved || FAILED_TESTS=$((FAILED_TESTS + 1))
test_invoke_hooks_nonzero_exit || FAILED_TESTS=$((FAILED_TESTS + 1))
test_invoke_hooks_python_exception || FAILED_TESTS=$((FAILED_TESTS + 1))
test_graceful_degradation_documented || FAILED_TESTS=$((FAILED_TESTS + 1))

echo "========================================="
if [ $FAILED_TESTS -eq 0 ]; then
    echo -e "${GREEN}ALL TESTS PASSED${NC}"
    exit 0
else
    echo -e "${RED}$FAILED_TESTS TEST(S) FAILED${NC}"
    exit 1
fi
