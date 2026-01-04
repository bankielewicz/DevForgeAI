#!/bin/bash
#
# Test: AC#1 - Migration Script Created
# Story: STORY-168 - RCA-012 Story Migration Script
#
# AC#1: Migration Script Created
#   Given: the DevForgeAI framework
#   When: I look in `.claude/scripts/`
#   Then: there should be a `migrate-ac-headers.sh` script
#
# Additional Requirements:
#   - Script has proper shebang (#!/bin/bash)
#   - Script has usage documentation
#   - Script is executable (chmod +x)
#
# Test Framework: Bash shell script with assertions
# Uses shared test library: test-lib.sh
#

set -euo pipefail

# Import shared test library
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/test-lib.sh"

echo "========================================================================"
echo "Test Suite: AC#1 - Migration Script Created"
echo "Story: STORY-168 - RCA-012 Story Migration Script"
echo "========================================================================"
echo ""

# ============================================================================
# Test 1: Script file exists at expected location
# ============================================================================
test_should_find_migration_script_file() {
    echo "Test 1: Script file exists at .claude/scripts/migrate-ac-headers.sh"
    assert_file_exists "$SCRIPT_FILE" "Migration script should exist at $SCRIPT_PATH"
}

# ============================================================================
# Test 2: Script has proper bash shebang
# ============================================================================
test_should_have_bash_shebang() {
    echo "Test 2: Script has proper #!/bin/bash shebang"

    if [[ ! -f "$SCRIPT_FILE" ]]; then
        TESTS_RUN=$((TESTS_RUN + 1))
        TESTS_FAILED=$((TESTS_FAILED + 1))
        echo -e "${RED}FAIL${NC} Script file not found, cannot check shebang"
        return
    fi

    local first_line=$(head -n 1 "$SCRIPT_FILE" | tr -d '\r')
    assert_equal "#!/bin/bash" "$first_line" "First line should be bash shebang"
}

# ============================================================================
# Test 3: Script has usage documentation
# ============================================================================
test_should_have_usage_documentation() {
    echo "Test 3: Script has usage documentation"

    if [[ ! -f "$SCRIPT_FILE" ]]; then
        TESTS_RUN=$((TESTS_RUN + 1))
        TESTS_FAILED=$((TESTS_FAILED + 1))
        echo -e "${RED}FAIL${NC} Script file not found, cannot check usage"
        return
    fi

    local content=$(cat "$SCRIPT_FILE")
    assert_contains "$content" "Usage:" "Script should contain usage documentation"
}

# ============================================================================
# Test 4: Script is executable
# ============================================================================
test_should_be_executable() {
    echo "Test 4: Script is executable (chmod +x)"
    assert_executable "$SCRIPT_FILE" "Script should have executable permission"
}

# ============================================================================
# Test 5: Script contains usage examples
# ============================================================================
test_should_have_usage_examples() {
    echo "Test 5: Script has usage examples"

    if [[ ! -f "$SCRIPT_FILE" ]]; then
        TESTS_RUN=$((TESTS_RUN + 1))
        TESTS_FAILED=$((TESTS_FAILED + 1))
        echo -e "${RED}FAIL${NC} Script file not found, cannot check examples"
        return
    fi

    local content=$(cat "$SCRIPT_FILE")
    assert_contains "$content" "Examples:" "Script should contain usage examples"
}

# ============================================================================
# Test 6: Script shows usage when run without arguments
# ============================================================================
test_should_show_usage_when_no_args() {
    echo "Test 6: Script shows usage when run without arguments"

    if [[ ! -f "$SCRIPT_FILE" ]]; then
        TESTS_RUN=$((TESTS_RUN + 1))
        TESTS_FAILED=$((TESTS_FAILED + 1))
        echo -e "${RED}FAIL${NC} Script file not found, cannot test no-args behavior"
        return
    fi

    local output=$("$SCRIPT_FILE" 2>&1 || true)
    assert_contains "$output" "Usage:" "Running script without args should show usage"
}

# ============================================================================
# Test 7: Script exits with non-zero when run without arguments
# ============================================================================
test_should_exit_nonzero_when_no_args() {
    echo "Test 7: Script exits with non-zero when run without arguments"

    if [[ ! -f "$SCRIPT_FILE" ]]; then
        TESTS_RUN=$((TESTS_RUN + 1))
        TESTS_FAILED=$((TESTS_FAILED + 1))
        echo -e "${RED}FAIL${NC} Script file not found, cannot test exit code"
        return
    fi

    set +e
    "$SCRIPT_FILE" > /dev/null 2>&1
    local exit_code=$?
    set -e

    assert_exit_code 1 "$exit_code" "Script should exit with code 1 when no arguments provided"
}

# ============================================================================
# Run all tests
# ============================================================================

test_should_find_migration_script_file
echo ""

test_should_have_bash_shebang
echo ""

test_should_have_usage_documentation
echo ""

test_should_be_executable
echo ""

test_should_have_usage_examples
echo ""

test_should_show_usage_when_no_args
echo ""

test_should_exit_nonzero_when_no_args
echo ""

# ============================================================================
# Print summary
# ============================================================================
print_test_summary "AC#1 Test Results Summary"
exit_with_result
