#!/bin/bash
################################################################################
# TEST SUITE: AC#4 - Configuration Validation
# Story: STORY-108
# Description: Validates the validation script (scripts/validate-parallel-config.sh)
#
# Acceptance Criteria:
# - Validation script exists and is executable
# - BR-001: max_concurrent_tasks range 1-10 enforced
# - BR-002: timeout_ms range 1000-600000 enforced
# - BR-003: Preset locking warning for non-standard presets
#
# Test Status: FAILING (Red Phase)
################################################################################

set -uo pipefail

PROJECT_ROOT="/mnt/c/Projects/DevForgeAI2"
SCRIPT_FILE="$PROJECT_ROOT/scripts/validate-parallel-config.sh"
TEST_DIR="$PROJECT_ROOT/devforgeai/tests/STORY-108/temp"
TEST_NAME="AC#4: Configuration Validation"

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Counters
TESTS_RUN=0
TESTS_PASSED=0
TESTS_FAILED=0

################################################################################
# Setup and Teardown
################################################################################

setup() {
    mkdir -p "$TEST_DIR"
}

teardown() {
    rm -rf "$TEST_DIR"
}

################################################################################
# Helper Functions
################################################################################

assert_script_executable() {
    local script_path="$1"
    local description="$2"
    ((TESTS_RUN++))

    if [ -x "$script_path" ]; then
        echo -e "${GREEN}✓ PASS${NC}: $description"
        ((TESTS_PASSED++))
        return 0
    else
        echo -e "${RED}✗ FAIL${NC}: $description"
        echo "  Script not found or not executable: $script_path"
        ((TESTS_FAILED++))
        return 1
    fi
}

create_test_config() {
    local content="$1"
    local config_file="$TEST_DIR/test-config.yaml"

    cat > "$config_file" << EOF
version: "1.0"
default_profile: "test"
profiles:
  test:
    $content
    retry:
      max_attempts: 3
      backoff_ms: 1000
EOF
    echo "$config_file"
}

create_preset_override_config() {
    local profile="$1"
    local override="$2"
    local config_file="$TEST_DIR/test-preset-config.yaml"

    cat > "$config_file" << EOF
version: "1.0"
default_profile: "$profile"
profiles:
  $profile:
    $override
    timeout_ms: 120000
    retry:
      max_attempts: 3
      backoff_ms: 1000
EOF
    echo "$config_file"
}

assert_validation_fails() {
    local config_file="$1"
    local description="$2"
    ((TESTS_RUN++))

    if [ ! -x "$SCRIPT_FILE" ]; then
        echo -e "${RED}✗ FAIL${NC}: $description"
        echo "  Validation script not found: $SCRIPT_FILE"
        ((TESTS_FAILED++))
        return 1
    fi

    if ! bash "$SCRIPT_FILE" "$config_file" > /dev/null 2>&1; then
        echo -e "${GREEN}✓ PASS${NC}: $description"
        echo "  Validation correctly rejected invalid config"
        ((TESTS_PASSED++))
        return 0
    else
        echo -e "${RED}✗ FAIL${NC}: $description"
        echo "  Validation should have rejected but passed"
        ((TESTS_FAILED++))
        return 1
    fi
}

assert_validation_passes() {
    local config_file="$1"
    local description="$2"
    ((TESTS_RUN++))

    if [ ! -x "$SCRIPT_FILE" ]; then
        echo -e "${RED}✗ FAIL${NC}: $description"
        echo "  Validation script not found: $SCRIPT_FILE"
        ((TESTS_FAILED++))
        return 1
    fi

    if bash "$SCRIPT_FILE" "$config_file" > /dev/null 2>&1; then
        echo -e "${GREEN}✓ PASS${NC}: $description"
        echo "  Validation correctly accepted valid config"
        ((TESTS_PASSED++))
        return 0
    else
        echo -e "${RED}✗ FAIL${NC}: $description"
        echo "  Validation should have passed but rejected"
        ((TESTS_FAILED++))
        return 1
    fi
}

assert_error_message_contains() {
    local config_file="$1"
    local expected_pattern="$2"
    local description="$3"
    ((TESTS_RUN++))

    if [ ! -x "$SCRIPT_FILE" ]; then
        echo -e "${RED}✗ FAIL${NC}: $description"
        echo "  Validation script not found: $SCRIPT_FILE"
        ((TESTS_FAILED++))
        return 1
    fi

    local output
    # Strip ANSI escape codes from output for pattern matching
    output=$(bash "$SCRIPT_FILE" "$config_file" 2>&1 | sed 's/\x1b\[[0-9;]*m//g' || true)

    # Split pattern by | and check each part exists in output
    local pattern_found=false
    IFS='|' read -ra PATTERNS <<< "$expected_pattern"
    for pattern in "${PATTERNS[@]}"; do
        # For patterns with .* we need each part to exist (not necessarily same line)
        if [[ "$pattern" == *".*"* ]]; then
            local part1="${pattern%%.*\**}"
            local part2="${pattern##*.*\*}"
            if echo "$output" | grep -q "$part1" && echo "$output" | grep -q "$part2"; then
                pattern_found=true
                break
            fi
        elif echo "$output" | grep -qE "$pattern"; then
            pattern_found=true
            break
        fi
    done

    if $pattern_found; then
        echo -e "${GREEN}✓ PASS${NC}: $description"
        echo "  Found expected pattern in output"
        ((TESTS_PASSED++))
        return 0
    else
        echo -e "${RED}✗ FAIL${NC}: $description"
        echo "  Expected pattern: $expected_pattern"
        echo "  Actual output: $output"
        ((TESTS_FAILED++))
        return 1
    fi
}

assert_warning_contains() {
    local config_file="$1"
    local expected_pattern="$2"
    local description="$3"
    ((TESTS_RUN++))

    if [ ! -x "$SCRIPT_FILE" ]; then
        echo -e "${RED}✗ FAIL${NC}: $description"
        echo "  Validation script not found: $SCRIPT_FILE"
        ((TESTS_FAILED++))
        return 1
    fi

    local output
    output=$(bash "$SCRIPT_FILE" "$config_file" 2>&1 || true)

    if echo "$output" | grep -qiE "$expected_pattern"; then
        echo -e "${GREEN}✓ PASS${NC}: $description"
        echo "  Found expected warning in output"
        ((TESTS_PASSED++))
        return 0
    else
        echo -e "${RED}✗ FAIL${NC}: $description"
        echo "  Expected pattern: $expected_pattern"
        echo "  Actual output: $output"
        ((TESTS_FAILED++))
        return 1
    fi
}

################################################################################
# Test Suite
################################################################################

echo ""
echo "========================================"
echo "  $TEST_NAME"
echo "  Story: STORY-108"
echo "========================================"
echo ""

setup

echo -e "${BLUE}Test Group 1: Script Existence${NC}"
echo "----------------------------------------"

# Test 1: Script exists and is executable
assert_script_executable "$SCRIPT_FILE" "Validation script exists and is executable"

echo ""
echo -e "${BLUE}Test Group 2: BR-001 - max_concurrent_tasks Range (1-10)${NC}"
echo "----------------------------------------"

# Test 2: Value 0 should FAIL
config_file=$(create_test_config "max_concurrent_tasks: 0
    timeout_ms: 120000")
assert_validation_fails "$config_file" "max_concurrent_tasks=0 rejected (below minimum)"

# Test 3: Value 11 should FAIL
config_file=$(create_test_config "max_concurrent_tasks: 11
    timeout_ms: 120000")
assert_validation_fails "$config_file" "max_concurrent_tasks=11 rejected (above maximum)"

# Test 4: Value 1 should PASS (edge case - minimum)
config_file=$(create_test_config "max_concurrent_tasks: 1
    timeout_ms: 120000")
assert_validation_passes "$config_file" "max_concurrent_tasks=1 accepted (valid minimum)"

# Test 5: Value 10 should PASS (edge case - maximum)
config_file=$(create_test_config "max_concurrent_tasks: 10
    timeout_ms: 120000")
assert_validation_passes "$config_file" "max_concurrent_tasks=10 accepted (valid maximum)"

# Test 6: Error message format for max_concurrent_tasks
config_file=$(create_test_config "max_concurrent_tasks: 99
    timeout_ms: 120000")
assert_error_message_contains "$config_file" "max_concurrent_tasks.*1-10|1-10.*max_concurrent_tasks" "Error message mentions field and valid range"

echo ""
echo -e "${BLUE}Test Group 3: BR-002 - timeout_ms Range (1000-600000)${NC}"
echo "----------------------------------------"

# Test 7: Value 999 should FAIL (below minimum)
config_file=$(create_test_config "max_concurrent_tasks: 4
    timeout_ms: 999")
assert_validation_fails "$config_file" "timeout_ms=999 rejected (below minimum 1000)"

# Test 8: Value 600001 should FAIL (above maximum)
config_file=$(create_test_config "max_concurrent_tasks: 4
    timeout_ms: 600001")
assert_validation_fails "$config_file" "timeout_ms=600001 rejected (above maximum 600000)"

# Test 9: Value 1000 should PASS (edge case - minimum)
config_file=$(create_test_config "max_concurrent_tasks: 4
    timeout_ms: 1000")
assert_validation_passes "$config_file" "timeout_ms=1000 accepted (valid minimum)"

# Test 10: Value 600000 should PASS (edge case - maximum)
config_file=$(create_test_config "max_concurrent_tasks: 4
    timeout_ms: 600000")
assert_validation_passes "$config_file" "timeout_ms=600000 accepted (valid maximum)"

# Test 11: Error message format for timeout_ms
config_file=$(create_test_config "max_concurrent_tasks: 4
    timeout_ms: 999999")
assert_error_message_contains "$config_file" "timeout_ms.*1000-600000|1000-600000.*timeout_ms" "Error message mentions field and valid range"

echo ""
echo -e "${BLUE}Test Group 4: BR-003 - Preset Locking Warning${NC}"
echo "----------------------------------------"

# Test 12: Overriding 'pro' preset should trigger warning
config_file=$(create_preset_override_config "pro" "max_concurrent_tasks: 8")
assert_warning_contains "$config_file" "WARNING.*preset|non-standard" "Warning shown when preset profile has non-standard values"

teardown

################################################################################
# Summary
################################################################################

echo ""
echo "========================================"
echo "  Test Summary"
echo "========================================"
echo "Tests Run:    $TESTS_RUN"
echo "Tests Passed: $TESTS_PASSED"
echo "Tests Failed: $TESTS_FAILED"
echo ""

if [ $TESTS_FAILED -gt 0 ]; then
    echo -e "${RED}RESULT: FAILED${NC}"
    exit 1
else
    echo -e "${GREEN}RESULT: PASSED${NC}"
    exit 0
fi
