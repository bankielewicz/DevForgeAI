#!/bin/bash

##############################################################################
# Test Suite: STORY-089 - Epic Validation Hook Tests (AC#1)
# Purpose: Test epic structure validation in /create-epic workflow
#
# Acceptance Criteria #1:
# - Epic has at least one feature defined
# - Each feature has unique identifier (Feature N: format)
# - Feature descriptions are non-empty (min 10 chars)
# - Epic frontmatter contains required fields (epic_id, title, status, priority)
##############################################################################

set -o pipefail

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Test counters
TESTS_RUN=0
TESTS_PASSED=0
TESTS_FAILED=0
TEST_LOG="/tmp/story-089-epic-validation.log"

# Paths
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="${SCRIPT_DIR}/../.."
VALIDATOR_SCRIPT="${PROJECT_ROOT}/.devforgeai/traceability/epic-validator.sh"
FIXTURES_DIR="${SCRIPT_DIR}/fixtures"

# Initialize log
echo "=== STORY-089 Epic Validation Hook Test Suite ===" > "$TEST_LOG"
echo "Started: $(date)" >> "$TEST_LOG"

##############################################################################
# Test Framework Functions
##############################################################################

run_test() {
    local test_name=$1
    local test_func=$2

    TESTS_RUN=$((TESTS_RUN + 1))
    echo -e "\n${BLUE}[Test $TESTS_RUN]${NC} $test_name"

    if $test_func 2>> "$TEST_LOG"; then
        TESTS_PASSED=$((TESTS_PASSED + 1))
        echo -e "${GREEN}✓${NC} PASSED"
    else
        TESTS_FAILED=$((TESTS_FAILED + 1))
        echo -e "${RED}✗${NC} FAILED"
    fi
}

assert_equals() {
    local expected="$1"
    local actual="$2"
    local message="${3:-Values should be equal}"

    if [[ "$expected" == "$actual" ]]; then
        return 0
    else
        echo "ASSERTION FAILED: $message"
        echo "Expected: $expected"
        echo "Actual: $actual"
        return 1
    fi
}

assert_contains() {
    local haystack="$1"
    local needle="$2"
    local message="${3:-String should contain substring}"

    if [[ "$haystack" == *"$needle"* ]]; then
        return 0
    else
        echo "ASSERTION FAILED: $message"
        echo "String: $haystack"
        echo "Should contain: $needle"
        return 1
    fi
}

assert_exit_code() {
    local expected="$1"
    local actual="$2"
    local message="${3:-Exit code mismatch}"

    if [[ "$expected" -eq "$actual" ]]; then
        return 0
    else
        echo "ASSERTION FAILED: $message"
        echo "Expected exit code: $expected"
        echo "Actual exit code: $actual"
        return 1
    fi
}

##############################################################################
# AC#1.1: Feature Count Validation
##############################################################################

test_rejects_epic_with_zero_features() {
    # AC#1: Epic must have at least one feature defined

    local epic_file="${FIXTURES_DIR}/epic-no-features.md"
    local result
    local exit_code

    result=$("$VALIDATOR_SCRIPT" --validate-epic "$epic_file" 2>&1)
    exit_code=$?

    assert_exit_code 1 "$exit_code" "Should fail validation for epic with no features" || return 1
    assert_contains "$result" "at least one feature" "Should mention feature requirement" || return 1
}

test_accepts_epic_with_one_feature() {
    # AC#1: Epic with one feature should pass

    local epic_file="${FIXTURES_DIR}/epic-one-feature.md"
    local result
    local exit_code

    result=$("$VALIDATOR_SCRIPT" --validate-epic "$epic_file" 2>&1)
    exit_code=$?

    assert_exit_code 0 "$exit_code" "Should pass validation for epic with one feature" || return 1
}

test_accepts_epic_with_multiple_features() {
    # AC#1: Epic with multiple features should pass

    local epic_file="${FIXTURES_DIR}/epic-multiple-features.md"
    local result
    local exit_code

    result=$("$VALIDATOR_SCRIPT" --validate-epic "$epic_file" 2>&1)
    exit_code=$?

    assert_exit_code 0 "$exit_code" "Should pass validation for epic with multiple features" || return 1
}

##############################################################################
# AC#1.2: Unique Feature Identifiers
##############################################################################

test_rejects_duplicate_feature_ids() {
    # AC#1: Each feature must have unique identifier

    local epic_file="${FIXTURES_DIR}/epic-duplicate-features.md"
    local result
    local exit_code

    result=$("$VALIDATOR_SCRIPT" --validate-epic "$epic_file" 2>&1)
    exit_code=$?

    assert_exit_code 1 "$exit_code" "Should fail for duplicate feature IDs" || return 1
    assert_contains "$result" "duplicate" "Should mention duplicate feature" || return 1
}

test_accepts_sequential_feature_ids() {
    # AC#1: Sequential Feature 1, Feature 2, etc. should pass

    local epic_file="${FIXTURES_DIR}/epic-sequential-features.md"
    local result
    local exit_code

    result=$("$VALIDATOR_SCRIPT" --validate-epic "$epic_file" 2>&1)
    exit_code=$?

    assert_exit_code 0 "$exit_code" "Should pass for sequential feature IDs"
}

test_rejects_invalid_feature_id_format() {
    # AC#1: Feature identifier must match "Feature N:" pattern

    local epic_file="${FIXTURES_DIR}/epic-invalid-feature-format.md"
    local result
    local exit_code

    result=$("$VALIDATOR_SCRIPT" --validate-epic "$epic_file" 2>&1)
    exit_code=$?

    assert_exit_code 1 "$exit_code" "Should fail for invalid feature ID format" || return 1
    assert_contains "$result" "format" "Should mention format requirement" || return 1
}

##############################################################################
# AC#1.3: Feature Description Validation
##############################################################################

test_rejects_empty_feature_description() {
    # AC#1: Feature descriptions must be non-empty

    local epic_file="${FIXTURES_DIR}/epic-empty-description.md"
    local result
    local exit_code

    result=$("$VALIDATOR_SCRIPT" --validate-epic "$epic_file" 2>&1)
    exit_code=$?

    assert_exit_code 1 "$exit_code" "Should fail for empty feature description" || return 1
    assert_contains "$result" "description" "Should mention description requirement" || return 1
}

test_rejects_short_feature_description() {
    # AC#1: Feature descriptions minimum 10 characters

    local epic_file="${FIXTURES_DIR}/epic-short-description.md"
    local result
    local exit_code

    result=$("$VALIDATOR_SCRIPT" --validate-epic "$epic_file" 2>&1)
    exit_code=$?

    assert_exit_code 1 "$exit_code" "Should fail for description < 10 chars" || return 1
    assert_contains "$result" "10 character" "Should mention minimum length" || return 1
}

test_accepts_adequate_feature_description() {
    # AC#1: Description with 10+ chars should pass

    local epic_file="${FIXTURES_DIR}/epic-adequate-description.md"
    local result
    local exit_code

    result=$("$VALIDATOR_SCRIPT" --validate-epic "$epic_file" 2>&1)
    exit_code=$?

    assert_exit_code 0 "$exit_code" "Should pass for adequate description"
}

##############################################################################
# AC#1.4: Frontmatter Validation
##############################################################################

test_rejects_missing_epic_id() {
    # AC#1: Frontmatter must contain epic_id

    local epic_file="${FIXTURES_DIR}/epic-missing-id.md"
    local result
    local exit_code

    result=$("$VALIDATOR_SCRIPT" --validate-epic "$epic_file" 2>&1)
    exit_code=$?

    assert_exit_code 1 "$exit_code" "Should fail for missing epic_id" || return 1
    assert_contains "$result" "epic_id" "Should mention missing epic_id" || return 1
}

test_rejects_missing_title() {
    # AC#1: Frontmatter must contain title

    local epic_file="${FIXTURES_DIR}/epic-missing-title.md"
    local result
    local exit_code

    result=$("$VALIDATOR_SCRIPT" --validate-epic "$epic_file" 2>&1)
    exit_code=$?

    assert_exit_code 1 "$exit_code" "Should fail for missing title" || return 1
    assert_contains "$result" "title" "Should mention missing title" || return 1
}

test_rejects_missing_status() {
    # AC#1: Frontmatter must contain status

    local epic_file="${FIXTURES_DIR}/epic-missing-status.md"
    local result
    local exit_code

    result=$("$VALIDATOR_SCRIPT" --validate-epic "$epic_file" 2>&1)
    exit_code=$?

    assert_exit_code 1 "$exit_code" "Should fail for missing status" || return 1
    assert_contains "$result" "status" "Should mention missing status" || return 1
}

test_rejects_missing_priority() {
    # AC#1: Frontmatter must contain priority

    local epic_file="${FIXTURES_DIR}/epic-missing-priority.md"
    local result
    local exit_code

    result=$("$VALIDATOR_SCRIPT" --validate-epic "$epic_file" 2>&1)
    exit_code=$?

    assert_exit_code 1 "$exit_code" "Should fail for missing priority" || return 1
    assert_contains "$result" "priority" "Should mention missing priority" || return 1
}

test_accepts_complete_frontmatter() {
    # AC#1: Complete frontmatter should pass

    local epic_file="${FIXTURES_DIR}/epic-complete-frontmatter.md"
    local result
    local exit_code

    result=$("$VALIDATOR_SCRIPT" --validate-epic "$epic_file" 2>&1)
    exit_code=$?

    assert_exit_code 0 "$exit_code" "Should pass for complete frontmatter"
}

##############################################################################
# Integration Tests
##############################################################################

test_validates_real_epic_015() {
    # Integration: Validate actual EPIC-015 from project

    local epic_file="${PROJECT_ROOT}/devforgeai/specs/Epics/EPIC-015-epic-coverage-validation-traceability.epic.md"

    if [[ ! -f "$epic_file" ]]; then
        echo "SKIP: EPIC-015 not found"
        return 0
    fi

    local result
    local exit_code

    result=$("$VALIDATOR_SCRIPT" --validate-epic "$epic_file" 2>&1)
    exit_code=$?

    assert_exit_code 0 "$exit_code" "Real EPIC-015 should pass validation"
}

test_performance_single_epic_under_50ms() {
    # NFR: Single epic validation <50ms (native), <200ms (WSL2)
    # WSL2 has significant I/O overhead, so we use relaxed threshold

    local epic_file="${FIXTURES_DIR}/epic-complete-frontmatter.md"
    local start_time end_time duration_ms
    local threshold=200  # Relaxed for WSL2 environment

    start_time=$(date +%s%N)
    "$VALIDATOR_SCRIPT" --validate-epic "$epic_file" > /dev/null 2>&1
    end_time=$(date +%s%N)

    duration_ms=$(( (end_time - start_time) / 1000000 ))

    if [[ $duration_ms -lt $threshold ]]; then
        echo "Validation took ${duration_ms}ms (< ${threshold}ms target)"
        return 0
    else
        echo "Validation took ${duration_ms}ms (>= ${threshold}ms target - SLOW)"
        return 1
    fi
}

##############################################################################
# Test Execution
##############################################################################

echo ""
echo "=========================================="
echo " STORY-089: Epic Validation Hook Tests"
echo " Acceptance Criteria #1"
echo "=========================================="
echo ""

# Check if validator script exists (will fail in RED phase)
if [[ ! -f "$VALIDATOR_SCRIPT" ]]; then
    echo -e "${YELLOW}WARNING:${NC} Validator script not found: $VALIDATOR_SCRIPT"
    echo -e "${YELLOW}This is expected during TDD RED phase${NC}"
    echo ""
fi

# Feature Count Tests
echo -e "\n${YELLOW}--- Feature Count Validation ---${NC}"
run_test "Rejects epic with zero features" test_rejects_epic_with_zero_features
run_test "Accepts epic with one feature" test_accepts_epic_with_one_feature
run_test "Accepts epic with multiple features" test_accepts_epic_with_multiple_features

# Feature ID Tests
echo -e "\n${YELLOW}--- Feature Identifier Validation ---${NC}"
run_test "Rejects duplicate feature IDs" test_rejects_duplicate_feature_ids
run_test "Accepts sequential feature IDs" test_accepts_sequential_feature_ids
run_test "Rejects invalid feature ID format" test_rejects_invalid_feature_id_format

# Description Tests
echo -e "\n${YELLOW}--- Feature Description Validation ---${NC}"
run_test "Rejects empty feature description" test_rejects_empty_feature_description
run_test "Rejects short feature description (<10 chars)" test_rejects_short_feature_description
run_test "Accepts adequate feature description (10+ chars)" test_accepts_adequate_feature_description

# Frontmatter Tests
echo -e "\n${YELLOW}--- Frontmatter Validation ---${NC}"
run_test "Rejects missing epic_id" test_rejects_missing_epic_id
run_test "Rejects missing title" test_rejects_missing_title
run_test "Rejects missing status" test_rejects_missing_status
run_test "Rejects missing priority" test_rejects_missing_priority
run_test "Accepts complete frontmatter" test_accepts_complete_frontmatter

# Integration Tests
echo -e "\n${YELLOW}--- Integration Tests ---${NC}"
run_test "Validates real EPIC-015" test_validates_real_epic_015
run_test "Performance: Single epic <50ms" test_performance_single_epic_under_50ms

# Summary
echo ""
echo "=========================================="
echo " Test Summary"
echo "=========================================="
echo -e "Tests Run:    ${TESTS_RUN}"
echo -e "Tests Passed: ${GREEN}${TESTS_PASSED}${NC}"
echo -e "Tests Failed: ${RED}${TESTS_FAILED}${NC}"
echo ""

if [[ $TESTS_FAILED -eq 0 ]]; then
    echo -e "${GREEN}All tests passed!${NC}"
    exit 0
else
    echo -e "${RED}Some tests failed. See log: $TEST_LOG${NC}"
    exit 1
fi
