#!/bin/bash

##############################################################################
# Test Suite: STORY-390 AC#3 - Rollback to Previous Version Within 2 Minutes
# Purpose: Verify rollback subcommand reads before_content from snapshot,
#          writes restored content, creates rollback version record,
#          completes in < 120 seconds
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
# AC#3 Tests: Rollback to Previous Version Within 2 Minutes
##############################################################################

# --- Structural Tests ---

test_implementation_file_exists() {
    [ -f "$IMPL_FILE" ]
}

test_has_rollback_subcommand_section() {
    # Must have a section documenting the rollback subcommand
    grep -qiE "^#{1,3}.*[Rr]ollback" "$IMPL_FILE"
}

# --- Pattern Tests: Content Restoration ---

test_rollback_reads_before_content() {
    # Rollback must read before_content from snapshot file
    grep -qiE "(read.*before_content|before_content.*read|Read\(.*snapshot)" "$IMPL_FILE"
}

test_rollback_writes_restored_content() {
    # Rollback must use Write() to restore content to component file
    grep -qiE "(Write\(.*restor|Write\(.*file_path|restore.*Write)" "$IMPL_FILE"
}

test_rollback_accepts_version_number() {
    # Rollback must accept target version_number parameter
    grep -qiE "(version_number|target.*version|version.*param)" "$IMPL_FILE"
}

test_rollback_accepts_previous_keyword() {
    # Rollback must accept "previous" keyword for latest pre-change state
    grep -qiE '("previous"|previous.*keyword|latest.*version)' "$IMPL_FILE"
}

# --- Pattern Tests: Rollback Version Record ---

test_rollback_creates_version_record() {
    # Rollback creates a new version record documenting the rollback
    grep -qiE "(rollback.*version.*record|type.*rollback|version.*entry.*rollback)" "$IMPL_FILE"
}

test_rollback_record_has_type_field() {
    # Rollback record must have type: "rollback"
    grep -qiE '(type.*"?rollback"?|"rollback".*type)' "$IMPL_FILE"
}

test_rollback_record_has_restored_from() {
    # Rollback record must have restored_from field with source version
    grep -qiE "(restored_from|restored.?from)" "$IMPL_FILE"
}

test_rollback_record_has_reason() {
    # Rollback record must have rollback_reason from operator
    grep -qiE "(rollback_reason|rollback.?reason)" "$IMPL_FILE"
}

# --- Pattern Tests: Performance Constraint ---

test_rollback_performance_constraint() {
    # Rollback must complete within 120 seconds (2 minutes)
    grep -qiE "(120.*second|2.*minute|under.*120|less.*than.*120)" "$IMPL_FILE"
}

# --- Pattern Tests: Confirmation Output ---

test_rollback_confirms_restored_path() {
    # Confirmation must include restored file path
    grep -qiE "(restored.*file.*path|file_path.*restor|Display.*path.*restor)" "$IMPL_FILE"
}

test_rollback_confirms_version_restored_to() {
    # Confirmation must include version restored to
    grep -qiE "(version.*restored.*to|restored.*version|Display.*version)" "$IMPL_FILE"
}

test_rollback_confirms_verification_hash() {
    # Confirmation must include verification hash
    grep -qiE "(verification.*hash|verify.*hash|hash.*verif)" "$IMPL_FILE"
}

# --- Business Rule Tests ---

test_br006_integrity_verification_required() {
    # BR-006: Rollback requires hash integrity verification
    grep -qiE "(integrity.*verif|hash.*verif.*before.*rollback|INTEGRITY_VERIFICATION)" "$IMPL_FILE"
}

test_br007_rollback_reason_required() {
    # BR-007: Change reason required for rollback (5-200 chars)
    grep -qiE "(rollback.*reason.*required|reason.*required.*rollback)" "$IMPL_FILE"
}

# --- Edge Case Tests ---

test_handles_deleted_component_file() {
    # Must handle rollback when component file has been deleted
    grep -qiE "(file.*deleted|no.*longer.*exist|recreate|AskUserQuestion)" "$IMPL_FILE"
}

test_handles_missing_snapshot_file() {
    # Must handle rollback when snapshot file is missing
    grep -qiE "(snapshot.*missing|snapshot.*not.*found|snapshot.*unavailable)" "$IMPL_FILE"
}

test_handles_no_version_history() {
    # Must handle rollback when component has no version history
    grep -qiE "(no.*version.*history|no.*prior.*version|history.*empty)" "$IMPL_FILE"
}

test_handles_invalid_version_number() {
    # Must handle rollback to nonexistent version number
    grep -qiE "(invalid.*version|version.*not.*found|version.*does.*not.*exist)" "$IMPL_FILE"
}

test_atomic_rollback_no_partial_writes() {
    # NFR-006: Rollback must be atomic - no partial writes
    grep -qiE "(atomic|no.*partial.*write|original.*preserved)" "$IMPL_FILE"
}

##############################################################################
# Test Execution
##############################################################################

echo "=============================================="
echo "  STORY-390 AC#3: Rollback Within 2 Minutes"
echo "  TDD Phase: RED (tests must fail)"
echo "=============================================="

# Structural Tests
run_test "Implementation file exists" test_implementation_file_exists
run_test "Has rollback subcommand section" test_has_rollback_subcommand_section

# Pattern Tests: Content Restoration
run_test "Rollback reads before_content" test_rollback_reads_before_content
run_test "Rollback writes restored content" test_rollback_writes_restored_content
run_test "Rollback accepts version number" test_rollback_accepts_version_number
run_test "Rollback accepts 'previous' keyword" test_rollback_accepts_previous_keyword

# Pattern Tests: Rollback Version Record
run_test "Rollback creates version record" test_rollback_creates_version_record
run_test "Rollback record has type field" test_rollback_record_has_type_field
run_test "Rollback record has restored_from" test_rollback_record_has_restored_from
run_test "Rollback record has reason" test_rollback_record_has_reason

# Pattern Tests: Performance
run_test "Rollback performance < 120 seconds" test_rollback_performance_constraint

# Pattern Tests: Confirmation
run_test "Rollback confirms restored path" test_rollback_confirms_restored_path
run_test "Rollback confirms version restored to" test_rollback_confirms_version_restored_to
run_test "Rollback confirms verification hash" test_rollback_confirms_verification_hash

# Business Rule Tests
run_test "BR-006: Integrity verification required" test_br006_integrity_verification_required
run_test "BR-007: Rollback reason required" test_br007_rollback_reason_required

# Edge Case Tests
run_test "Handles deleted component file" test_handles_deleted_component_file
run_test "Handles missing snapshot file" test_handles_missing_snapshot_file
run_test "Handles no version history" test_handles_no_version_history
run_test "Handles invalid version number" test_handles_invalid_version_number
run_test "Atomic rollback - no partial writes" test_atomic_rollback_no_partial_writes

##############################################################################
# Summary
##############################################################################

echo ""
echo "=============================================="
echo "  AC#3 Test Results"
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
