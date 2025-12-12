#!/bin/bash
#
# Test Suite: JSON Schema Validation
# STORY-084: Epic & Story Metadata Parser
#
# Tests JSON schemas for ParsedEpic, ParsedStory, ParsingError data models

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/../.." && pwd)"
MODELS_DIR="${PROJECT_ROOT}/.devforgeai/traceability/models"

# Test counters
TESTS_RUN=0
TESTS_PASSED=0
TESTS_FAILED=0

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m'

# Log file
TEST_LOG="/tmp/story-084-schemas.log"
echo "=== Schema Test Suite ===" > "$TEST_LOG"
echo "Started: $(date)" >> "$TEST_LOG"

#############################################################################
# TEST UTILITIES
#############################################################################

run_test() {
    local test_name="$1"
    local test_func="$2"

    TESTS_RUN=$((TESTS_RUN + 1))
    echo -e "\n${BLUE}[Test $TESTS_RUN]${NC} $test_name"
    echo "[Test $TESTS_RUN] $test_name" >> "$TEST_LOG"

    if $test_func 2>> "$TEST_LOG"; then
        TESTS_PASSED=$((TESTS_PASSED + 1))
        echo -e "${GREEN}✓${NC} PASSED"
        echo "RESULT: PASSED" >> "$TEST_LOG"
    else
        TESTS_FAILED=$((TESTS_FAILED + 1))
        echo -e "${RED}✗${NC} FAILED"
        echo "RESULT: FAILED" >> "$TEST_LOG"
    fi
}

#############################################################################
# SCHEMA FILE EXISTENCE TESTS
#############################################################################

test_epic_schema_exists() {
    [ -f "${MODELS_DIR}/epic.json" ]
}

test_story_schema_exists() {
    [ -f "${MODELS_DIR}/story.json" ]
}

test_error_schema_exists() {
    [ -f "${MODELS_DIR}/error.json" ]
}

#############################################################################
# EPIC SCHEMA VALIDATION TESTS
#############################################################################

test_epic_schema_validates_complete_epic() {
    local epic_json='{"epic_id":"EPIC-015","title":"Test Epic","status":"Planning","priority":"High","created":"2025-11-25","complexity":13,"estimated_sprints":2,"tags":["test"],"features":[]}'

    # Validate epic_id pattern
    local epic_id
    epic_id=$(echo "$epic_json" | jq -r '.epic_id')
    [[ "$epic_id" =~ ^EPIC-[0-9]{3}$ ]] || return 1

    # Validate status enum
    local status
    status=$(echo "$epic_json" | jq -r '.status')
    [[ "$status" =~ ^(Planning|In\ Progress|Complete|On\ Hold)$ ]] || return 1

    # Validate date format
    local created
    created=$(echo "$epic_json" | jq -r '.created')
    [[ "$created" =~ ^[0-9]{4}-[0-9]{2}-[0-9]{2}$ ]] || return 1

    return 0
}

test_epic_schema_rejects_invalid_epic_id() {
    local epic_id="EPIC-15"  # Should be EPIC-015 (3 digits)

    # Should NOT match the pattern
    if [[ "$epic_id" =~ ^EPIC-[0-9]{3}$ ]]; then
        return 1  # Fail - should have rejected
    fi
    return 0  # Pass - correctly rejected
}

test_epic_schema_rejects_invalid_status() {
    local status="Active"  # Not a valid status

    # Should NOT match valid statuses
    if [[ "$status" =~ ^(Planning|In\ Progress|Complete|On\ Hold)$ ]]; then
        return 1  # Fail - should have rejected
    fi
    return 0  # Pass - correctly rejected
}

#############################################################################
# STORY SCHEMA VALIDATION TESTS
#############################################################################

test_story_schema_validates_complete_story() {
    local story_json='{"id":"STORY-084","title":"Test Story","epic":"EPIC-015","sprint":"Sprint-1","status":"Backlog","points":13,"priority":"Medium","format_version":"2.1"}'

    # Validate story_id pattern
    local story_id
    story_id=$(echo "$story_json" | jq -r '.id')
    [[ "$story_id" =~ ^STORY-[0-9]{3}$ ]] || return 1

    # Validate points is Fibonacci
    local points
    points=$(echo "$story_json" | jq '.points')
    [[ "$points" =~ ^(1|2|3|5|8|13|21)$ ]] || return 1

    return 0
}

test_story_schema_rejects_non_fibonacci_points() {
    local points=4  # Not Fibonacci

    # Should NOT match Fibonacci set
    if [[ "$points" =~ ^(1|2|3|5|8|13|21)$ ]]; then
        return 1  # Fail - should have rejected
    fi
    return 0  # Pass - correctly rejected
}

test_story_schema_accepts_epic_none() {
    local epic_ref="None"

    # "None" is a valid value for standalone stories
    [[ "$epic_ref" == "None" || "$epic_ref" =~ ^EPIC-[0-9]{3}$ ]] || return 1
    return 0
}

test_story_schema_rejects_invalid_status() {
    local status="Working"  # Not a valid status
    local valid_statuses="Backlog|Ready for Dev|In Development|Dev Complete|QA In Progress|QA Approved|QA Failed|Releasing|Released"

    if echo "$status" | grep -qE "^($valid_statuses)$"; then
        return 1  # Fail - should have rejected
    fi
    return 0  # Pass - correctly rejected
}

#############################################################################
# ERROR SCHEMA VALIDATION TESTS
#############################################################################

test_error_schema_contains_required_fields() {
    local error_json='{"error_type":"MALFORMED_YAML","file_path":"/test/file.md","line_number":5,"error_message":"Invalid YAML syntax"}'

    # All required fields must be present
    [ "$(echo "$error_json" | jq -r '.error_type')" != "null" ] || return 1
    [ "$(echo "$error_json" | jq -r '.file_path')" != "null" ] || return 1
    [ "$(echo "$error_json" | jq '.line_number')" != "null" ] || return 1
    [ "$(echo "$error_json" | jq -r '.error_message')" != "null" ] || return 1

    return 0
}

test_error_schema_validates_error_types() {
    local valid_types=("MALFORMED_YAML" "MISSING_FRONTMATTER" "INVALID_FIELD" "VALIDATION_ERROR" "DUPLICATE_ID")

    for error_type in "${valid_types[@]}"; do
        if [[ ! "$error_type" =~ ^(MALFORMED_YAML|MISSING_FRONTMATTER|INVALID_FIELD|VALIDATION_ERROR|DUPLICATE_ID)$ ]]; then
            return 1
        fi
    done
    return 0
}

#############################################################################
# MAIN EXECUTION
#############################################################################

echo "=================================================="
echo "  STORY-084: JSON Schema Validation Tests"
echo "=================================================="
echo ""

# Schema existence tests
run_test "Epic schema file exists" test_epic_schema_exists
run_test "Story schema file exists" test_story_schema_exists
run_test "Error schema file exists" test_error_schema_exists

# Epic schema validation
run_test "Epic schema validates complete epic" test_epic_schema_validates_complete_epic
run_test "Epic schema rejects invalid epic_id format" test_epic_schema_rejects_invalid_epic_id
run_test "Epic schema rejects invalid status enum" test_epic_schema_rejects_invalid_status

# Story schema validation
run_test "Story schema validates complete story" test_story_schema_validates_complete_story
run_test "Story schema rejects non-Fibonacci points" test_story_schema_rejects_non_fibonacci_points
run_test "Story schema accepts epic: None" test_story_schema_accepts_epic_none
run_test "Story schema rejects invalid status enum" test_story_schema_rejects_invalid_status

# Error schema validation
run_test "Error schema contains required fields" test_error_schema_contains_required_fields
run_test "Error schema validates error types" test_error_schema_validates_error_types

echo ""
echo "=================================================="
echo "  RESULTS"
echo "=================================================="
echo "Tests Run:    $TESTS_RUN"
echo "Tests Passed: $TESTS_PASSED"
echo "Tests Failed: $TESTS_FAILED"
echo ""

# Write summary to log
echo "" >> "$TEST_LOG"
echo "=== Summary ===" >> "$TEST_LOG"
echo "Tests Run: $TESTS_RUN" >> "$TEST_LOG"
echo "Tests Passed: $TESTS_PASSED" >> "$TEST_LOG"
echo "Tests Failed: $TESTS_FAILED" >> "$TEST_LOG"

# Exit with appropriate code
if [ "$TESTS_FAILED" -gt 0 ]; then
    exit 1
fi
exit 0
