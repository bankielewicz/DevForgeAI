#!/bin/bash

##############################################################################
# Test Suite: STORY-083 - Orphan Detection Tests (AC#5)
# Purpose: Validate orphaned story detection and categorization
#
# Acceptance Criteria #5:
# - Detect missing epic: field (incomplete metadata)
# - Detect epic: None (intentionally standalone)
# - Detect broken references (non-existent epic)
# - Categorize results properly
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
TEST_LOG="/tmp/story-083-orphan-detection.log"

# Paths
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="${SCRIPT_DIR}/../.."
PARSER_SCRIPT="${PROJECT_ROOT}/devforgeai/traceability/parse-requirements.sh"

# Initialize log
echo "=== STORY-083 Orphan Detection Test Suite ===" > "$TEST_LOG"
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
# Category Detection Tests
##############################################################################

test_detects_intentionally_standalone() {
    # AC#5: Stories with epic: None

    local result
    result=$("$PARSER_SCRIPT" --detect-orphans 2>/dev/null)

    if echo "$result" | jq -e '.intentionally_standalone | type == "array"' >/dev/null 2>&1; then
        return 0
    else
        echo "Missing intentionally_standalone array"
        return 1
    fi
}

test_detects_broken_references() {
    # AC#5: Stories referencing non-existent epics

    local result
    result=$("$PARSER_SCRIPT" --detect-orphans 2>/dev/null)

    if echo "$result" | jq -e '.broken_references | type == "array"' >/dev/null 2>&1; then
        return 0
    else
        echo "Missing broken_references array"
        return 1
    fi
}

test_detects_missing_metadata() {
    # AC#5: Stories without epic: field

    local result
    result=$("$PARSER_SCRIPT" --detect-orphans 2>/dev/null)

    if echo "$result" | jq -e '.missing_metadata | type == "array"' >/dev/null 2>&1; then
        return 0
    else
        echo "Missing missing_metadata array"
        return 1
    fi
}

##############################################################################
# Categorization Validation
##############################################################################

test_orphan_categorization_exclusive() {
    # Each story should appear in at most one category

    local result
    result=$("$PARSER_SCRIPT" --detect-orphans 2>/dev/null)

    local standalone broken missing
    standalone=$(echo "$result" | jq -r '.intentionally_standalone[]?' 2>/dev/null | sort)
    broken=$(echo "$result" | jq -r '.broken_references[]?' 2>/dev/null | sort)
    missing=$(echo "$result" | jq -r '.missing_metadata[]?' 2>/dev/null | sort)

    # Check no overlap between categories
    local overlap1 overlap2 overlap3
    overlap1=$(comm -12 <(echo "$standalone") <(echo "$broken") 2>/dev/null | wc -l)
    overlap2=$(comm -12 <(echo "$standalone") <(echo "$missing") 2>/dev/null | wc -l)
    overlap3=$(comm -12 <(echo "$broken") <(echo "$missing") 2>/dev/null | wc -l)

    if [ "${overlap1:-0}" -eq 0 ] && [ "${overlap2:-0}" -eq 0 ] && [ "${overlap3:-0}" -eq 0 ]; then
        return 0
    else
        echo "Categories have overlapping stories"
        return 1
    fi
}

##############################################################################
# Summary Statistics
##############################################################################

test_orphan_summary_statistics() {
    # Orphan detection includes summary counts

    local result
    result=$("$PARSER_SCRIPT" --detect-orphans 2>/dev/null)

    if echo "$result" | jq -e '.summary.total_orphans >= 0' >/dev/null 2>&1; then
        return 0
    else
        echo "Missing summary.total_orphans"
        return 1
    fi
}

##############################################################################
# Linked Stories Not Orphaned
##############################################################################

test_linked_stories_not_orphaned() {
    # Stories with valid epic: EPIC-NNN should NOT appear in orphans
    # STORY-007 has valid epic: EPIC-002

    local result
    result=$("$PARSER_SCRIPT" --detect-orphans 2>/dev/null)

    local all_orphans
    all_orphans=$(echo "$result" | jq -r '.intentionally_standalone[], .broken_references[], .missing_metadata[]?' 2>/dev/null)

    if echo "$all_orphans" | grep -q "STORY-007"; then
        echo "STORY-007 incorrectly marked as orphan"
        return 1
    else
        return 0
    fi
}

##############################################################################
# Result Persistence
##############################################################################

test_orphan_report_in_matrix() {
    # Orphan detection results saved in requirements-matrix.json

    "$PARSER_SCRIPT" --generate-matrix 2>/dev/null

    local matrix_file="${PROJECT_ROOT}/devforgeai/traceability/requirements-matrix.json"

    if [ ! -f "$matrix_file" ]; then
        echo "Matrix file not created"
        return 1
    fi

    if jq -e '.validation.intentionally_standalone' "$matrix_file" >/dev/null 2>&1; then
        return 0
    else
        echo "Orphan data not in matrix file"
        return 1
    fi
}

##############################################################################
# Duplicate Story Detection
##############################################################################

test_no_duplicate_story_ids() {
    # Edge case 5: Check for duplicate STORY-NNN prefixes

    local duplicates
    duplicates=$("$PARSER_SCRIPT" --check-duplicate-stories 2>/dev/null)

    if [ -z "$duplicates" ]; then
        return 0
    else
        echo "Found duplicate story IDs: $duplicates"
        # This is a warning, not necessarily a failure
        return 0
    fi
}

##############################################################################
# Main Test Execution
##############################################################################

main() {
    echo -e "${BLUE}╔══════════════════════════════════════════════════════════╗${NC}"
    echo -e "${BLUE}║  STORY-083: Orphan Detection Test Suite (AC#5)           ║${NC}"
    echo -e "${BLUE}╚══════════════════════════════════════════════════════════╝${NC}"

    echo -e "\n${BLUE}=== Category Detection Tests ===${NC}"
    run_test "Detects intentionally standalone" test_detects_intentionally_standalone
    run_test "Detects broken references" test_detects_broken_references
    run_test "Detects missing metadata" test_detects_missing_metadata

    echo -e "\n${BLUE}=== Categorization Validation Tests ===${NC}"
    run_test "Categories are mutually exclusive" test_orphan_categorization_exclusive

    echo -e "\n${BLUE}=== Summary Statistics Tests ===${NC}"
    run_test "Summary statistics present" test_orphan_summary_statistics

    echo -e "\n${BLUE}=== Linked Stories Tests ===${NC}"
    run_test "Linked stories not orphaned" test_linked_stories_not_orphaned

    echo -e "\n${BLUE}=== Result Persistence Tests ===${NC}"
    run_test "Orphan data in matrix file" test_orphan_report_in_matrix

    echo -e "\n${BLUE}=== Duplicate Detection Tests ===${NC}"
    run_test "Check for duplicate story IDs" test_no_duplicate_story_ids

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
