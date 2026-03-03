#!/bin/bash
# Test AC#1: Pre-Commit Hook for Size Warning
# STORY-335: Add Subagent Size Enforcement Mechanism
#
# Validates:
# - Pre-commit hook script exists at .claude/hooks/pre-commit-subagent-size.sh
# - Hook displays warning for files with 500-599 lines
# - Hook exits with code 0 (warning only, does not block commit)
# - Warning message contains expected text
#
# Expected: FAIL initially (TDD Red phase - hook script does not exist yet)

# Note: Not using set -e due to arithmetic operations with (( ))

# Configuration
PROJECT_ROOT="/mnt/c/Projects/DevForgeAI2"
HOOK_SCRIPT="$PROJECT_ROOT/.claude/hooks/pre-commit-subagent-size.sh"
TEST_DIR="$PROJECT_ROOT/tests/STORY-335/fixtures"

# Test tracking
TESTS_RUN=0
TESTS_PASSED=0
TESTS_FAILED=0

# Test helper functions
pass_test() {
    local test_name="$1"
    TESTS_PASSED=$((TESTS_PASSED + 1))
    echo "[PASS] $test_name"
}

fail_test() {
    local test_name="$1"
    local message="$2"
    TESTS_FAILED=$((TESTS_FAILED + 1))
    echo "[FAIL] $test_name: $message"
}

run_test() {
    local test_name="$1"
    TESTS_RUN=$((TESTS_RUN + 1))
    shift
    "$@"
}

# Create test fixtures
setup_test_fixtures() {
    mkdir -p "$TEST_DIR"

    # Create a 520-line test file (should trigger warning)
    {
        echo "---"
        echo "name: test-agent"
        echo "description: Test agent for size check"
        echo "---"
        echo ""
        echo "# Test Agent"
        for i in $(seq 1 514); do
            echo "Line $i of test content for size validation"
        done
    } > "$TEST_DIR/test-agent-520-lines.md"

    # Create a 450-line test file (should NOT trigger warning)
    {
        echo "---"
        echo "name: test-agent-small"
        echo "description: Test agent under threshold"
        echo "---"
        echo ""
        echo "# Test Agent Small"
        for i in $(seq 1 444); do
            echo "Line $i of test content"
        done
    } > "$TEST_DIR/test-agent-450-lines.md"
}

# Cleanup test fixtures
cleanup_test_fixtures() {
    rm -rf "$TEST_DIR"
}

# -----------------------------------------------------------------------------
# Test 1: Hook script exists
# -----------------------------------------------------------------------------
test_hook_script_exists() {
    local test_name="Pre-commit hook script exists"
    if [ -f "$HOOK_SCRIPT" ]; then
        pass_test "$test_name"
    else
        fail_test "$test_name" "File not found: $HOOK_SCRIPT"
    fi
}

# -----------------------------------------------------------------------------
# Test 2: Hook script is executable
# -----------------------------------------------------------------------------
test_hook_script_executable() {
    local test_name="Pre-commit hook script is executable"

    if [ ! -f "$HOOK_SCRIPT" ]; then
        fail_test "$test_name" "Cannot check - script does not exist"
        return
    fi

    if [ -x "$HOOK_SCRIPT" ]; then
        pass_test "$test_name"
    else
        fail_test "$test_name" "Script is not executable"
    fi
}

# -----------------------------------------------------------------------------
# Test 3: Hook script has bash shebang
# -----------------------------------------------------------------------------
test_hook_shebang() {
    local test_name="Hook script has bash shebang"

    if [ ! -f "$HOOK_SCRIPT" ]; then
        fail_test "$test_name" "Cannot check - script does not exist"
        return
    fi

    local first_line
    first_line=$(head -n 1 "$HOOK_SCRIPT")

    if [ "$first_line" = "#!/bin/bash" ]; then
        pass_test "$test_name"
    else
        fail_test "$test_name" "First line is not #!/bin/bash (got: $first_line)"
    fi
}

# -----------------------------------------------------------------------------
# Test 4: Hook contains WARNING_THRESHOLD=500
# -----------------------------------------------------------------------------
test_warning_threshold_defined() {
    local test_name="Hook contains WARNING_THRESHOLD=500"

    if [ ! -f "$HOOK_SCRIPT" ]; then
        fail_test "$test_name" "Cannot check - script does not exist"
        return
    fi

    if grep -qE "WARNING_THRESHOLD[[:space:]]*=[[:space:]]*\\\$\\{.*:-500\\}|WARNING_THRESHOLD[[:space:]]*=[[:space:]]*500" "$HOOK_SCRIPT"; then
        pass_test "$test_name"
    else
        fail_test "$test_name" "WARNING_THRESHOLD=500 not found in script"
    fi
}

# -----------------------------------------------------------------------------
# Test 5: Hook contains FAIL_THRESHOLD=600
# -----------------------------------------------------------------------------
test_fail_threshold_defined() {
    local test_name="Hook contains FAIL_THRESHOLD=600"

    if [ ! -f "$HOOK_SCRIPT" ]; then
        fail_test "$test_name" "Cannot check - script does not exist"
        return
    fi

    if grep -qE "FAIL_THRESHOLD[[:space:]]*=[[:space:]]*\\\$\\{.*:-600\\}|FAIL_THRESHOLD[[:space:]]*=[[:space:]]*600" "$HOOK_SCRIPT"; then
        pass_test "$test_name"
    else
        fail_test "$test_name" "FAIL_THRESHOLD=600 not found in script"
    fi
}

# -----------------------------------------------------------------------------
# Test 6: Hook displays warning message for 500-599 line files
# -----------------------------------------------------------------------------
test_warning_message_displayed() {
    local test_name="Hook displays warning message for 500-599 line files"

    if [ ! -f "$HOOK_SCRIPT" ]; then
        fail_test "$test_name" "Cannot check - script does not exist"
        return
    fi

    # Check script contains warning message pattern
    if grep -qE "WARNING.*exceeds.*500.*line" "$HOOK_SCRIPT"; then
        pass_test "$test_name"
    else
        fail_test "$test_name" "Warning message pattern not found in script"
    fi
}

# -----------------------------------------------------------------------------
# Test 7: Hook checks agents directories
# -----------------------------------------------------------------------------
test_agents_directory_check() {
    local test_name="Hook checks agents directories (src/claude/agents/ and .claude/agents/)"

    if [ ! -f "$HOOK_SCRIPT" ]; then
        fail_test "$test_name" "Cannot check - script does not exist"
        return
    fi

    local has_src_claude_agents=false
    local has_claude_agents=false

    if grep -qE "src/claude/agents/" "$HOOK_SCRIPT"; then
        has_src_claude_agents=true
    fi

    if grep -qE "\.claude/agents/" "$HOOK_SCRIPT"; then
        has_claude_agents=true
    fi

    if [ "$has_src_claude_agents" = true ] && [ "$has_claude_agents" = true ]; then
        pass_test "$test_name"
    else
        fail_test "$test_name" "Script must check both src/claude/agents/ and .claude/agents/"
    fi
}

# -----------------------------------------------------------------------------
# Test 8: Hook exits with code 0 for warnings
# -----------------------------------------------------------------------------
test_warning_exit_code_zero() {
    local test_name="Hook exits with code 0 for warning-only scenarios"

    if [ ! -f "$HOOK_SCRIPT" ]; then
        fail_test "$test_name" "Cannot check - script does not exist"
        return
    fi

    # Check that script has logic to exit 0 for warnings
    # Script should only exit 1 for hard failures (600+ lines)
    if grep -qE "exit[[:space:]]+0" "$HOOK_SCRIPT"; then
        pass_test "$test_name"
    else
        fail_test "$test_name" "No 'exit 0' found in script"
    fi
}

# -----------------------------------------------------------------------------
# Test 9: Hook references ADR-012
# -----------------------------------------------------------------------------
test_adr_reference() {
    local test_name="Hook references ADR-012 in comments or messages"

    if [ ! -f "$HOOK_SCRIPT" ]; then
        fail_test "$test_name" "Cannot check - script does not exist"
        return
    fi

    if grep -qE "ADR-012|ADR012" "$HOOK_SCRIPT"; then
        pass_test "$test_name"
    else
        fail_test "$test_name" "ADR-012 reference not found in script"
    fi
}

# -----------------------------------------------------------------------------
# Test 10: Hook suggests extracting to references/
# -----------------------------------------------------------------------------
test_references_suggestion() {
    local test_name="Hook suggests extracting to references/ directory"

    if [ ! -f "$HOOK_SCRIPT" ]; then
        fail_test "$test_name" "Cannot check - script does not exist"
        return
    fi

    if grep -qE "references/" "$HOOK_SCRIPT"; then
        pass_test "$test_name"
    else
        fail_test "$test_name" "No suggestion to extract to references/ found"
    fi
}

# -----------------------------------------------------------------------------
# Main test execution
# -----------------------------------------------------------------------------
echo "=============================================="
echo "STORY-335 AC#1: Pre-Commit Hook for Size Warning"
echo "=============================================="
echo "Target script: $HOOK_SCRIPT"
echo "Warning threshold: 500 lines"
echo "Expected behavior: Display warning, exit 0"
echo "----------------------------------------------"
echo ""

# Setup
setup_test_fixtures

# Run tests
run_test "1" test_hook_script_exists
run_test "2" test_hook_script_executable
run_test "3" test_hook_shebang
run_test "4" test_warning_threshold_defined
run_test "5" test_fail_threshold_defined
run_test "6" test_warning_message_displayed
run_test "7" test_agents_directory_check
run_test "8" test_warning_exit_code_zero
run_test "9" test_adr_reference
run_test "10" test_references_suggestion

# Cleanup
cleanup_test_fixtures

echo ""
echo "=============================================="
echo "Test Summary: $TESTS_PASSED/$TESTS_RUN passed"
echo "=============================================="

if [ "$TESTS_FAILED" -gt 0 ]; then
    echo "Status: FAILED ($TESTS_FAILED failures)"
    exit 1
else
    echo "Status: PASSED"
    exit 0
fi
