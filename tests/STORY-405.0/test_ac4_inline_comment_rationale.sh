#!/bin/bash
# Test AC#4: Inline comment documents alignment rationale
# STORY-405: Unify God Class Threshold to >20 Methods
#
# Validates:
# - "REC-369-001" comment present in anti-pattern-scanner.md
# - "REC-369-001" comment present in phase5-code-smells.md
# - "REC-369-001" comment present in phase1-context-loading.md
#
# Expected: FAIL initially (TDD Red phase - no REC-369-001 comments exist yet)

PROJECT_ROOT="/mnt/c/Projects/DevForgeAI2"
SCANNER_FILE="$PROJECT_ROOT/src/claude/agents/anti-pattern-scanner.md"
PHASE5_FILE="$PROJECT_ROOT/src/claude/docs/agents/anti-pattern-scanner/phase5-code-smells.md"
PHASE1_FILE="$PROJECT_ROOT/src/claude/docs/agents/anti-pattern-scanner/phase1-context-loading.md"

TESTS_RUN=0
TESTS_PASSED=0
TESTS_FAILED=0

pass_test() {
    TESTS_PASSED=$((TESTS_PASSED + 1))
    echo "[PASS] $1"
}

fail_test() {
    TESTS_FAILED=$((TESTS_FAILED + 1))
    echo "[FAIL] $1: $2"
}

run_test() {
    TESTS_RUN=$((TESTS_RUN + 1))
    shift
    "$@"
}

# -----------------------------------------------------------------------------
# Test 1: anti-pattern-scanner.md contains "REC-369-001"
# -----------------------------------------------------------------------------
test_scanner_has_rec_comment() {
    local test_name="anti-pattern-scanner.md contains REC-369-001"
    local match_count
    match_count=$(grep -c "REC-369-001" "$SCANNER_FILE" 2>/dev/null)
    match_count=${match_count:-0}
    if [ "$match_count" -ge 1 ]; then
        pass_test "$test_name (found $match_count occurrences)"
    else
        fail_test "$test_name" "No REC-369-001 references found"
    fi
}

# -----------------------------------------------------------------------------
# Test 2: phase5-code-smells.md contains "REC-369-001"
# -----------------------------------------------------------------------------
test_phase5_has_rec_comment() {
    local test_name="phase5-code-smells.md contains REC-369-001"
    local match_count
    match_count=$(grep -c "REC-369-001" "$PHASE5_FILE" 2>/dev/null)
    match_count=${match_count:-0}
    if [ "$match_count" -ge 1 ]; then
        pass_test "$test_name (found $match_count occurrences)"
    else
        fail_test "$test_name" "No REC-369-001 references found"
    fi
}

# -----------------------------------------------------------------------------
# Test 3: phase1-context-loading.md contains "REC-369-001"
# -----------------------------------------------------------------------------
test_phase1_has_rec_comment() {
    local test_name="phase1-context-loading.md contains REC-369-001"
    local match_count
    match_count=$(grep -c "REC-369-001" "$PHASE1_FILE" 2>/dev/null)
    match_count=${match_count:-0}
    if [ "$match_count" -ge 1 ]; then
        pass_test "$test_name (found $match_count occurrences)"
    else
        fail_test "$test_name" "No REC-369-001 references found"
    fi
}

# -----------------------------------------------------------------------------
# Test 4: Comment contains rationale text "Treelint"
# -----------------------------------------------------------------------------
test_comment_has_rationale() {
    local test_name="REC-369-001 comment mentions Treelint alignment"
    if grep "REC-369-001" "$SCANNER_FILE" 2>/dev/null | grep -qi "treelint"; then
        pass_test "$test_name"
    else
        fail_test "$test_name" "REC-369-001 comment missing Treelint rationale"
    fi
}

echo "=============================================="
echo "STORY-405 AC#4: Inline Comment Rationale"
echo "=============================================="
echo ""

run_test "1" test_scanner_has_rec_comment
run_test "2" test_phase5_has_rec_comment
run_test "3" test_phase1_has_rec_comment
run_test "4" test_comment_has_rationale

echo ""
echo "=============================================="
echo "Test Summary: $TESTS_PASSED/$TESTS_RUN passed"
echo "=============================================="

if [ "$TESTS_FAILED" -gt 0 ]; then
    echo "Status: FAILED ($TESTS_FAILED failures)"
    exit 1
else
    echo "Status: PASSED"
    exit 0
fi
