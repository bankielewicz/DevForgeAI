#!/bin/bash

##############################################################################
# Test Suite: STORY-390 AC#2 - Before/After State Recorded After Modification
# Purpose: Verify finalize subcommand updates snapshot with after_hash,
#          after_content, appends VERSION-HISTORY.md entry with
#          auto-incremented version number
#
# Implementation: src/claude/commands/prompt-version.md (Slash Command)
# Test Type: Structural + Pattern (Markdown Command Testing Pattern)
#
# All tests MUST FAIL (TDD RED) until implementation exists.
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

# Paths
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="${SCRIPT_DIR}/../.."
IMPL_FILE="${PROJECT_ROOT}/src/claude/commands/prompt-version.md"

##############################################################################
# Test Framework Functions
##############################################################################

run_test() {
    local test_name=$1
    local test_func=$2

    TESTS_RUN=$((TESTS_RUN + 1))
    echo -e "\n${BLUE}[Test $TESTS_RUN]${NC} $test_name"

    if $test_func 2>/dev/null; then
        TESTS_PASSED=$((TESTS_PASSED + 1))
        echo -e "  ${GREEN}PASS${NC}: $test_name"
    else
        TESTS_FAILED=$((TESTS_FAILED + 1))
        echo -e "  ${RED}FAIL${NC}: $test_name"
    fi
}

##############################################################################
# AC#2 Tests: Before/After State Recorded After Modification
##############################################################################

# --- Structural Tests ---

test_implementation_file_exists() {
    [ -f "$IMPL_FILE" ]
}

test_has_finalize_subcommand_section() {
    # Must have a section documenting the finalize subcommand
    grep -qiE "^#{1,3}.*[Ff]inalize" "$IMPL_FILE"
}

test_has_version_history_reference() {
    # Must reference VERSION-HISTORY.md file
    grep -q "VERSION-HISTORY.md" "$IMPL_FILE"
}

# --- Pattern Tests: After-State Recording ---

test_finalize_computes_after_hash() {
    # Finalize must compute SHA-256 of the after-state (modified file)
    grep -qiE "(after_hash|after.?hash)" "$IMPL_FILE"
}

test_finalize_stores_after_content() {
    # Finalize must store after_content in the snapshot
    grep -q "after_content" "$IMPL_FILE"
}

test_finalize_records_change_reason() {
    # Finalize must record change_reason provided by operator
    grep -q "change_reason" "$IMPL_FILE"
}

test_finalize_records_timestamp() {
    # Finalize must record finalized_timestamp
    grep -q "finalized_timestamp" "$IMPL_FILE"
}

test_finalize_updates_existing_snapshot() {
    # Finalize must update the existing snapshot record (not create new)
    grep -qiE "(update.*snapshot|Edit\(|read.*snapshot.*write)" "$IMPL_FILE"
}

# --- Pattern Tests: VERSION-HISTORY.md Structure ---

test_version_history_has_table_format() {
    # VERSION-HISTORY.md must use Markdown table format
    grep -qiE "(Version.*Date.*Hash|Markdown.*table|\|.*Version.*\|)" "$IMPL_FILE"
}

test_version_history_has_version_column() {
    # Table must have Version column
    grep -qiE "(version_number|Version.*column|\|.*[Vv]ersion)" "$IMPL_FILE"
}

test_version_history_has_before_hash_column() {
    # Table must have Before Hash column
    grep -qiE "([Bb]efore.?[Hh]ash)" "$IMPL_FILE"
}

test_version_history_has_after_hash_column() {
    # Table must have After Hash column
    grep -qiE "([Aa]fter.?[Hh]ash)" "$IMPL_FILE"
}

test_version_history_has_date_column() {
    # Table must have Date column
    grep -qiE "(change_date|[Dd]ate.*column|\|.*[Dd]ate)" "$IMPL_FILE"
}

test_version_history_has_reason_column() {
    # Table must have Reason column
    grep -qiE "(change_reason|[Rr]eason.*column|\|.*[Rr]eason)" "$IMPL_FILE"
}

test_version_history_has_snapshot_reference() {
    # Each entry must reference the snapshot file
    grep -qiE "(snapshot_file|snapshot.*reference|\|.*[Ss]napshot)" "$IMPL_FILE"
}

# --- Pattern Tests: Auto-Increment ---

test_version_number_auto_increment() {
    # Version number must be auto-incremented
    grep -qiE "(auto.?increment|version.*\+.*1|next.*version|increment)" "$IMPL_FILE"
}

test_version_number_starts_at_one() {
    # Version numbering starts at 1 for new components
    grep -qiE "(start.*1|version.*1|initial.*version)" "$IMPL_FILE"
}

# --- Pattern Tests: Diff Summary ---

test_finalize_reports_diff_summary() {
    # Finalize must report diff summary (lines added, removed, changed)
    grep -qiE "(diff.*summary|lines.*added|lines.*removed|lines.*changed)" "$IMPL_FILE"
}

# --- Business Rule Tests ---

test_br007_change_reason_required() {
    # BR-007: Change reason is required (5-200 chars) for finalize
    grep -qiE "(change.?reason.*required|5.*200.*char|reason.*length)" "$IMPL_FILE"
}

test_br007_change_reason_min_length() {
    # BR-007: Change reason minimum 5 characters
    grep -qE "(min.*5|5.*char|length.*5)" "$IMPL_FILE"
}

test_br005_concurrent_capture_detection() {
    # BR-005: Concurrent captures detected and blocked
    grep -qiE "(concurrent|pending.*capture|already.*captured)" "$IMPL_FILE"
}

# --- Edge Case Tests ---

test_handles_missing_prior_capture() {
    # Must handle case where finalize is called without prior capture
    grep -qiE "(no.*prior.*capture|capture.*first|pending.*snapshot.*not.*found)" "$IMPL_FILE"
}

test_handles_unchanged_file() {
    # Must handle case where file was not actually modified (same hash)
    grep -qiE "(unchanged|identical|same.*hash|no.*modification)" "$IMPL_FILE"
}

##############################################################################
# Test Execution
##############################################################################

echo "=============================================="
echo "  STORY-390 AC#2: Before/After State Recording"
echo "  TDD Phase: RED (tests must fail)"
echo "=============================================="

# Structural Tests
run_test "Implementation file exists" test_implementation_file_exists
run_test "Has finalize subcommand section" test_has_finalize_subcommand_section
run_test "Has VERSION-HISTORY.md reference" test_has_version_history_reference

# Pattern Tests: After-State
run_test "Finalize computes after_hash" test_finalize_computes_after_hash
run_test "Finalize stores after_content" test_finalize_stores_after_content
run_test "Finalize records change_reason" test_finalize_records_change_reason
run_test "Finalize records finalized_timestamp" test_finalize_records_timestamp
run_test "Finalize updates existing snapshot" test_finalize_updates_existing_snapshot

# Pattern Tests: VERSION-HISTORY.md
run_test "VERSION-HISTORY has table format" test_version_history_has_table_format
run_test "VERSION-HISTORY has Version column" test_version_history_has_version_column
run_test "VERSION-HISTORY has Before Hash column" test_version_history_has_before_hash_column
run_test "VERSION-HISTORY has After Hash column" test_version_history_has_after_hash_column
run_test "VERSION-HISTORY has Date column" test_version_history_has_date_column
run_test "VERSION-HISTORY has Reason column" test_version_history_has_reason_column
run_test "VERSION-HISTORY has snapshot reference" test_version_history_has_snapshot_reference

# Pattern Tests: Auto-Increment
run_test "Version number auto-increment" test_version_number_auto_increment
run_test "Version number starts at 1" test_version_number_starts_at_one

# Pattern Tests: Diff Summary
run_test "Finalize reports diff summary" test_finalize_reports_diff_summary

# Business Rule Tests
run_test "BR-007: Change reason required" test_br007_change_reason_required
run_test "BR-007: Change reason min length" test_br007_change_reason_min_length
run_test "BR-005: Concurrent capture detection" test_br005_concurrent_capture_detection

# Edge Case Tests
run_test "Handles missing prior capture" test_handles_missing_prior_capture
run_test "Handles unchanged file" test_handles_unchanged_file

##############################################################################
# Summary
##############################################################################

echo ""
echo "=============================================="
echo "  AC#2 Test Results"
echo "=============================================="
echo -e "  Total:  ${TESTS_RUN}"
echo -e "  Passed: ${GREEN}${TESTS_PASSED}${NC}"
echo -e "  Failed: ${RED}${TESTS_FAILED}${NC}"
echo "=============================================="

if [ "$TESTS_FAILED" -gt 0 ]; then
    echo -e "${RED}RESULT: FAIL${NC} - $TESTS_FAILED test(s) failed (TDD RED confirmed)"
    exit 1
else
    echo -e "${GREEN}RESULT: PASS${NC} - All tests passed"
    exit 0
fi
