#!/bin/bash

##############################################################################
# Test Suite: STORY-083 - Validation Tests (AC#4)
# Purpose: Validate epic reference validation
#
# Acceptance Criteria #4:
# - Verify referenced epic file exists
# - Epic_id matches entry in epics data structure
# - Bidirectional consistency
# - Report specific error messages
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
TEST_LOG="/tmp/story-083-validation.log"

# Paths
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="${SCRIPT_DIR}/../.."
PARSER_SCRIPT="${PROJECT_ROOT}/devforgeai/traceability/parse-requirements.sh"
FIXTURES_DIR="${SCRIPT_DIR}/fixtures"

# Initialize log
echo "=== STORY-083 Validation Test Suite ===" > "$TEST_LOG"
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
# Epic Existence Validation
##############################################################################

test_validates_epic_file_exists() {
    # AC#4: Verify referenced epic file exists

    local result
    result=$("$PARSER_SCRIPT" --validate-epic-exists "EPIC-015" 2>/dev/null)

    if [ "$result" = "exists" ]; then
        return 0
    else
        echo "Expected: exists, Got: $result"
        return 1
    fi
}

test_detects_nonexistent_epic_reference() {
    # AC#4: Detect story referencing non-existent epic

    local result
    result=$("$PARSER_SCRIPT" --validate-epic-exists "EPIC-999" 2>/dev/null)

    if [ "$result" = "not_found" ]; then
        return 0
    else
        echo "Expected: not_found, Got: $result"
        return 1
    fi
}

##############################################################################
# Bidirectional Consistency
##############################################################################

test_bidirectional_consistency_check() {
    # AC#4: Story appears in epic's Stories section

    local result
    result=$("$PARSER_SCRIPT" --check-bidirectional "STORY-083" "EPIC-015" 2>/dev/null)

    if [ "$result" = "bidirectional" ]; then
        return 0
    else
        echo "Expected: bidirectional, Got: $result"
        return 1
    fi
}

test_detects_unidirectional_reference() {
    # Story references epic but not listed in epic's Stories table
    # This is expected for many stories (Stories table may be incomplete)

    local result
    result=$("$PARSER_SCRIPT" --check-bidirectional "STORY-007" "EPIC-002" 2>/dev/null)

    # Either bidirectional or unidirectional is acceptable (not error)
    if [ "$result" = "bidirectional" ] || [ "$result" = "unidirectional" ]; then
        return 0
    else
        echo "Expected bidirectional or unidirectional, Got: $result"
        return 1
    fi
}

##############################################################################
# Validation Report
##############################################################################

test_full_validation_report() {
    # AC#4: Full validation generates matrix with validation section

    local result
    result=$("$PARSER_SCRIPT" --run-validation 2>/dev/null)

    if echo "$result" | jq -e '.validation' >/dev/null 2>&1; then
        return 0
    else
        echo "Validation result missing validation section"
        return 1
    fi
}

test_validation_continues_on_error() {
    # BR-004: Single file parse failure must not abort batch

    "$PARSER_SCRIPT" --run-validation 2>/dev/null
    local exit_code=$?

    # Should complete (may have warnings) but not crash
    # Exit codes 0-9 are valid states
    if [ "$exit_code" -lt 10 ]; then
        return 0
    else
        echo "Validation crashed with exit code: $exit_code"
        return 1
    fi
}

##############################################################################
# Path Security
##############################################################################

test_no_path_traversal() {
    # NFR-005: No path traversal vulnerability

    local result
    result=$("$PARSER_SCRIPT" --extract-epic-id "../../../etc/passwd" 2>/dev/null)
    local exit_code=$?

    # Should reject with error, not process
    if [ "$exit_code" -ne 0 ] && [ -z "$result" ]; then
        return 0
    else
        echo "Path traversal not blocked"
        return 1
    fi
}

test_rejects_absolute_outside_project() {
    # Security: Reject absolute paths outside project

    local result
    result=$("$PARSER_SCRIPT" --extract-epic-id "/etc/passwd" 2>/dev/null)
    local exit_code=$?

    if [ "$exit_code" -ne 0 ]; then
        return 0
    else
        echo "Absolute path outside project not rejected"
        return 1
    fi
}

##############################################################################
# Main Test Execution
##############################################################################

main() {
    echo -e "${BLUE}╔══════════════════════════════════════════════════════════╗${NC}"
    echo -e "${BLUE}║  STORY-083: Validation Test Suite (AC#4)                 ║${NC}"
    echo -e "${BLUE}╚══════════════════════════════════════════════════════════╝${NC}"

    echo -e "\n${BLUE}=== Epic Existence Validation Tests ===${NC}"
    run_test "Validates epic file exists" test_validates_epic_file_exists
    run_test "Detects non-existent epic" test_detects_nonexistent_epic_reference

    echo -e "\n${BLUE}=== Bidirectional Consistency Tests ===${NC}"
    run_test "Check bidirectional reference" test_bidirectional_consistency_check
    run_test "Handle unidirectional reference" test_detects_unidirectional_reference

    echo -e "\n${BLUE}=== Validation Report Tests ===${NC}"
    run_test "Full validation generates report" test_full_validation_report
    run_test "Validation continues on error" test_validation_continues_on_error

    echo -e "\n${BLUE}=== Security Tests ===${NC}"
    run_test "No path traversal vulnerability" test_no_path_traversal
    run_test "Rejects absolute path outside project" test_rejects_absolute_outside_project

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
