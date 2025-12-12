#!/bin/bash

##############################################################################
# Test Suite: STORY-083 - Data Model Tests (AC#3)
# Purpose: Validate relationship data structure (JSON output)
#
# Acceptance Criteria #3:
# - epics map with epic_id as key
# - stories map with story_id as key
# - orphaned_stories list
# - unlinked_epics list
# - Persisted to requirements-matrix.json
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
TEST_LOG="/tmp/story-083-data-model.log"

# Paths
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="${SCRIPT_DIR}/../.."
PARSER_SCRIPT="${PROJECT_ROOT}/.devforgeai/traceability/parse-requirements.sh"
OUTPUT_FILE="${PROJECT_ROOT}/.devforgeai/traceability/requirements-matrix.json"

# Initialize log
echo "=== STORY-083 Data Model Test Suite ===" > "$TEST_LOG"
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

##############################################################################
# DATA-001: Epics Map Structure
##############################################################################

test_epics_map_structure() {
    # DATA-001: JSON contains epics map
    "$PARSER_SCRIPT" --generate-matrix 2>/dev/null

    if [ ! -f "$OUTPUT_FILE" ]; then
        echo "Output file not created"
        return 1
    fi

    if jq -e '.epics' "$OUTPUT_FILE" >/dev/null 2>&1; then
        return 0
    else
        echo "Missing epics map in JSON"
        return 1
    fi
}

test_epic_entry_has_required_fields() {
    # DATA-001: Each epic entry has title, file_path, linked_stories

    if [ ! -f "$OUTPUT_FILE" ]; then
        "$PARSER_SCRIPT" --generate-matrix 2>/dev/null
    fi

    # Get first epic and check fields
    local has_fields
    has_fields=$(jq -e '.epics | to_entries | .[0].value | has("title") and has("file_path") and has("linked_stories")' "$OUTPUT_FILE" 2>/dev/null)

    if [ "$has_fields" = "true" ]; then
        return 0
    else
        echo "Epic entry missing required fields"
        return 1
    fi
}

##############################################################################
# DATA-002: Stories Map Structure
##############################################################################

test_stories_map_structure() {
    # DATA-002: JSON contains stories map

    if jq -e '.stories' "$OUTPUT_FILE" >/dev/null 2>&1; then
        return 0
    else
        echo "Missing stories map in JSON"
        return 1
    fi
}

test_story_entry_has_required_fields() {
    # DATA-002: Each story has title, epic_ref, status, file_path

    local has_fields
    has_fields=$(jq -e '.stories | to_entries | .[0].value | has("title") and has("epic_ref") and has("status") and has("file_path")' "$OUTPUT_FILE" 2>/dev/null)

    if [ "$has_fields" = "true" ]; then
        return 0
    else
        echo "Story entry missing required fields"
        return 1
    fi
}

##############################################################################
# DATA-003: Validation Section
##############################################################################

test_validation_section_exists() {
    # DATA-003: JSON contains validation section with arrays

    local has_validation
    has_validation=$(jq -e '.validation | has("intentionally_standalone") and has("broken_references") and has("missing_metadata")' "$OUTPUT_FILE" 2>/dev/null)

    if [ "$has_validation" = "true" ]; then
        return 0
    else
        echo "Missing validation section or arrays"
        return 1
    fi
}

##############################################################################
# DATA-004: Metadata Fields
##############################################################################

test_metadata_fields_exist() {
    # DATA-004: JSON contains version and generated_at

    local has_metadata
    has_metadata=$(jq -e 'has("version") and has("generated_at")' "$OUTPUT_FILE" 2>/dev/null)

    if [ "$has_metadata" = "true" ]; then
        return 0
    else
        echo "Missing version or generated_at"
        return 1
    fi
}

##############################################################################
# BR-005: JSON Validity and Idempotency
##############################################################################

test_json_valid_format() {
    # Basic: Generated JSON must be valid

    if jq empty "$OUTPUT_FILE" 2>/dev/null; then
        return 0
    else
        echo "Invalid JSON format"
        return 1
    fi
}

test_idempotent_output() {
    # BR-005: Running parser twice produces identical output

    "$PARSER_SCRIPT" --generate-matrix 2>/dev/null
    local hash1
    hash1=$(sha256sum "$OUTPUT_FILE" | cut -d' ' -f1)

    sleep 1  # Ensure timestamp differs
    "$PARSER_SCRIPT" --generate-matrix 2>/dev/null
    local hash2
    hash2=$(sha256sum "$OUTPUT_FILE" | cut -d' ' -f1)

    # Note: Timestamps will differ, so we compare structure not exact bytes
    # Instead, check that epics and stories content matches
    local epics1 stories1 epics2 stories2
    epics1=$(jq -S '.epics' "$OUTPUT_FILE")
    stories1=$(jq -S '.stories' "$OUTPUT_FILE")

    "$PARSER_SCRIPT" --generate-matrix 2>/dev/null
    epics2=$(jq -S '.epics' "$OUTPUT_FILE")
    stories2=$(jq -S '.stories' "$OUTPUT_FILE")

    if [ "$epics1" = "$epics2" ] && [ "$stories1" = "$stories2" ]; then
        return 0
    else
        echo "Output not idempotent (content changed between runs)"
        return 1
    fi
}

##############################################################################
# Main Test Execution
##############################################################################

main() {
    echo -e "${BLUE}╔══════════════════════════════════════════════════════════╗${NC}"
    echo -e "${BLUE}║  STORY-083: Data Model Test Suite (AC#3)                 ║${NC}"
    echo -e "${BLUE}╚══════════════════════════════════════════════════════════╝${NC}"

    echo -e "\n${BLUE}=== Epics Map Structure Tests ===${NC}"
    run_test "Epics map exists in JSON" test_epics_map_structure
    run_test "Epic entry has required fields" test_epic_entry_has_required_fields

    echo -e "\n${BLUE}=== Stories Map Structure Tests ===${NC}"
    run_test "Stories map exists in JSON" test_stories_map_structure
    run_test "Story entry has required fields" test_story_entry_has_required_fields

    echo -e "\n${BLUE}=== Validation Section Tests ===${NC}"
    run_test "Validation section exists" test_validation_section_exists

    echo -e "\n${BLUE}=== Metadata Tests ===${NC}"
    run_test "Metadata fields exist" test_metadata_fields_exist

    echo -e "\n${BLUE}=== JSON Quality Tests ===${NC}"
    run_test "JSON is valid format" test_json_valid_format
    run_test "Output is idempotent" test_idempotent_output

    # Summary
    echo ""
    echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"
    echo -e "Tests Run:    ${TESTS_RUN}"
    echo -e "Tests Passed: ${GREEN}${TESTS_PASSED}${NC}"
    echo -e "Tests Failed: ${RED}${TESTS_FAILED}${NC}"
    echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"

    if [ "$TESTS_FAILED" -gt 0 ]; then
        exit 1
    fi
    exit 0
}

main "$@"
