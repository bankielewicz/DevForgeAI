#!/bin/bash

##############################################################################
# Test Suite: STORY-390 AC#6 - Integrity Verification on Rollback
# Purpose: Verify SHA-256 recomputed from stored content, hash match allows
#          rollback, hash mismatch triggers HALT with INTEGRITY_VERIFICATION_FAILED
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
# AC#6 Tests: Integrity Verification on Rollback
##############################################################################

# --- Structural Tests ---

test_implementation_file_exists() {
    [ -f "$IMPL_FILE" ]
}

test_has_integrity_verification_section() {
    # Must have a section documenting integrity verification
    grep -qiE "^#{1,3}.*(integrity|verification|hash.*check)" "$IMPL_FILE"
}

# --- Pattern Tests: SHA-256 Recomputation ---

test_recomputes_sha256_from_stored_content() {
    # Must recompute SHA-256 from stored before_content
    grep -qiE "(recomput.*sha|sha.*256.*stored|compute.*hash.*stored_content|sha256.*before_content)" "$IMPL_FILE"
}

test_compares_computed_against_recorded() {
    # Must compare computed hash against recorded before_hash
    grep -qiE "(compare.*hash|hash.*match|computed.*vs.*recorded|before_hash.*compare)" "$IMPL_FILE"
}

# --- Pattern Tests: Hash Match (Happy Path) ---

test_hash_match_allows_rollback() {
    # If hashes match, proceed with rollback
    grep -qiE "(hash.*match.*proceed|match.*rollback|proceed.*with.*rollback)" "$IMPL_FILE"
}

# --- Pattern Tests: Hash Mismatch (Error Path) ---

test_hash_mismatch_triggers_halt() {
    # If hashes do NOT match, HALT execution
    grep -qiE "(mismatch.*HALT|HALT.*mismatch|hash.*not.*match.*HALT)" "$IMPL_FILE"
}

test_integrity_verification_failed_error() {
    # Must output INTEGRITY_VERIFICATION_FAILED error code
    grep -q "INTEGRITY_VERIFICATION_FAILED" "$IMPL_FILE"
}

test_displays_expected_vs_actual_hash() {
    # Must display expected vs actual hash on mismatch
    grep -qiE "(expected.*actual|expected.*hash.*actual.*hash|expected.*vs.*actual)" "$IMPL_FILE"
}

test_refuses_to_restore_corrupted_content() {
    # Must refuse to restore potentially corrupted content
    grep -qiE "(refuse.*restor|corrupt.*content|do.*not.*restor)" "$IMPL_FILE"
}

# --- Pattern Tests: User Recovery Options ---

test_offers_force_restore_option() {
    # Must offer force restore option (with warning)
    grep -qiE "(force.*restor|force.*option|AskUserQuestion.*force)" "$IMPL_FILE"
}

test_offers_cancel_rollback_option() {
    # Must offer cancel rollback option
    grep -qiE "(cancel.*rollback|cancel.*option|AskUserQuestion.*cancel)" "$IMPL_FILE"
}

test_offers_git_history_fallback() {
    # Must offer restore from git history as fallback option
    grep -qiE "(git.*history|git.*fallback|restore.*from.*git)" "$IMPL_FILE"
}

test_uses_ask_user_question() {
    # Must use AskUserQuestion tool for recovery options
    grep -qiE "AskUserQuestion" "$IMPL_FILE"
}

# --- Business Rule Tests ---

test_br004_sha256_hash_format_validation() {
    # BR-004: SHA-256 hash format ^[0-9a-f]{64}$ or sentinel NEW_COMPONENT
    grep -qiE "(\[0-9a-f\]\{64\}|64.*hex.*char|NEW_COMPONENT)" "$IMPL_FILE"
}

test_br006_integrity_before_every_rollback() {
    # BR-006: Rollback requires integrity verification before content restoration
    grep -qiE "(integrity.*before.*rollback|verify.*before.*restor|check.*integrity.*first)" "$IMPL_FILE"
}

# --- NFR Tests ---

test_nfr004_path_traversal_prevention() {
    # NFR-004: All paths validated against src/claude/ prefix
    grep -qiE "(path.*traversal|src/claude/.*prefix|validate.*path)" "$IMPL_FILE"
}

test_nfr005_sha256_on_every_rollback() {
    # NFR-005: SHA-256 comparison on every rollback
    grep -qiE "(every.*rollback.*sha|sha.*every.*rollback|always.*verify)" "$IMPL_FILE"
}

test_nfr005_halt_on_mismatch() {
    # NFR-005: HALT on hash mismatch
    grep -qiE "(HALT.*mismatch|mismatch.*HALT)" "$IMPL_FILE"
}

# --- Edge Case Tests ---

test_handles_new_component_sentinel() {
    # Must handle NEW_COMPONENT sentinel during integrity check
    grep -qiE "(NEW_COMPONENT.*sentinel|sentinel.*NEW_COMPONENT|skip.*integrity.*NEW_COMPONENT)" "$IMPL_FILE"
}

test_handles_corrupted_snapshot_file() {
    # Must handle corrupted snapshot file (cannot parse content)
    grep -qiE "(corrupted.*snapshot|malformed.*snapshot|cannot.*parse.*snapshot)" "$IMPL_FILE"
}

test_handles_missing_before_content_in_snapshot() {
    # Must handle snapshot missing before_content section
    grep -qiE "(missing.*before_content|before_content.*missing|incomplete.*snapshot)" "$IMPL_FILE"
}

test_handles_missing_before_hash_in_snapshot() {
    # Must handle snapshot missing before_hash field
    grep -qiE "(missing.*before_hash|before_hash.*missing|no.*before_hash)" "$IMPL_FILE"
}

##############################################################################
# Test Execution
##############################################################################

echo "=============================================="
echo "  STORY-390 AC#6: Integrity Verification"
echo "  TDD Phase: RED (tests must fail)"
echo "=============================================="

# Structural Tests
run_test "Implementation file exists" test_implementation_file_exists
run_test "Has integrity verification section" test_has_integrity_verification_section

# Pattern Tests: SHA-256 Recomputation
run_test "Recomputes SHA-256 from stored content" test_recomputes_sha256_from_stored_content
run_test "Compares computed against recorded hash" test_compares_computed_against_recorded

# Pattern Tests: Hash Match
run_test "Hash match allows rollback" test_hash_match_allows_rollback

# Pattern Tests: Hash Mismatch
run_test "Hash mismatch triggers HALT" test_hash_mismatch_triggers_halt
run_test "INTEGRITY_VERIFICATION_FAILED error" test_integrity_verification_failed_error
run_test "Displays expected vs actual hash" test_displays_expected_vs_actual_hash
run_test "Refuses to restore corrupted content" test_refuses_to_restore_corrupted_content

# Pattern Tests: User Recovery
run_test "Offers force restore option" test_offers_force_restore_option
run_test "Offers cancel rollback option" test_offers_cancel_rollback_option
run_test "Offers git history fallback" test_offers_git_history_fallback
run_test "Uses AskUserQuestion tool" test_uses_ask_user_question

# Business Rule Tests
run_test "BR-004: SHA-256 hash format validation" test_br004_sha256_hash_format_validation
run_test "BR-006: Integrity before every rollback" test_br006_integrity_before_every_rollback

# NFR Tests
run_test "NFR-004: Path traversal prevention" test_nfr004_path_traversal_prevention
run_test "NFR-005: SHA-256 on every rollback" test_nfr005_sha256_on_every_rollback
run_test "NFR-005: HALT on mismatch" test_nfr005_halt_on_mismatch

# Edge Case Tests
run_test "Handles NEW_COMPONENT sentinel" test_handles_new_component_sentinel
run_test "Handles corrupted snapshot file" test_handles_corrupted_snapshot_file
run_test "Handles missing before_content" test_handles_missing_before_content_in_snapshot
run_test "Handles missing before_hash" test_handles_missing_before_hash_in_snapshot

##############################################################################
# Summary
##############################################################################

echo ""
echo "=============================================="
echo "  AC#6 Test Results"
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
