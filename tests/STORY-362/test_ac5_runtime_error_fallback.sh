#!/usr/bin/env bash
# =============================================================================
# STORY-362 AC#5: Treelint Command Failure Fallback (Runtime Errors)
# =============================================================================
# Validates that treelint-search-patterns.md:
#   1. Documents malformed JSON output handling
#   2. Specifies Grep fallback for runtime errors
#   3. Distinguishes empty results (exit 0) from failure (BR-003)
#   4. One-shot fallback: no retry loop (BR-002)
#   5. No exception propagation to parent skill
#
# TDD Phase: RED - Tests expected to FAIL until implementation complete.
# =============================================================================

set -euo pipefail

PROJECT_ROOT="${PROJECT_ROOT:-/mnt/c/Projects/DevForgeAI2}"
TARGET_FILE="${PROJECT_ROOT}/src/claude/agents/references/treelint-search-patterns.md"

PASS_COUNT=0
FAIL_COUNT=0
TOTAL_COUNT=0

pass() {
    PASS_COUNT=$((PASS_COUNT + 1))
    TOTAL_COUNT=$((TOTAL_COUNT + 1))
    echo "  PASS: $1"
}

fail() {
    FAIL_COUNT=$((FAIL_COUNT + 1))
    TOTAL_COUNT=$((TOTAL_COUNT + 1))
    echo "  FAIL: $1"
}

echo "=============================================="
echo "  AC#5: Runtime Error Fallback"
echo "=============================================="
echo ""

# -----------------------------------------------------------------------------
# Test 1: File exists
# -----------------------------------------------------------------------------
echo "--- Test 1: File Existence ---"
if [[ -r "$TARGET_FILE" ]]; then
    pass "Reference file exists"
else
    fail "Reference file does not exist"
    echo ""
    echo "=============================================="
    echo "  AC#5 Results: ${PASS_COUNT} passed, ${FAIL_COUNT} failed (${TOTAL_COUNT} total)"
    echo "=============================================="
    echo "  STATUS: FAILED (file does not exist - RED phase expected)"
    exit 1
fi
echo ""

# -----------------------------------------------------------------------------
# Test 2: Malformed JSON handling documented (FALLBACK-005)
# Must mention JSON parse failure / malformed output
# -----------------------------------------------------------------------------
echo "--- Test 2: Malformed JSON Handling ---"
if grep -qiE '(malformed|invalid|corrupt|broken|unparseable).*(JSON|output)' "$TARGET_FILE" 2>/dev/null || \
   grep -qiE 'JSON.*(malformed|invalid|parse.*(error|fail)|corrupt)' "$TARGET_FILE" 2>/dev/null; then
    pass "Malformed JSON handling documented"
else
    fail "Missing malformed JSON output handling documentation"
fi
echo ""

# -----------------------------------------------------------------------------
# Test 3: Grep fallback for malformed JSON
# When JSON parse fails, must fall back to Grep
# -----------------------------------------------------------------------------
echo "--- Test 3: Grep Fallback for Malformed JSON ---"
if grep -qiE '(malformed|parse|JSON).*(Grep|fall.?back)' "$TARGET_FILE" 2>/dev/null || \
   grep -qiE '(fall.?back|Grep).*(malformed|parse|JSON)' "$TARGET_FILE" 2>/dev/null; then
    pass "Grep fallback specified for malformed JSON"
else
    fail "Missing Grep fallback for malformed JSON scenario"
fi
echo ""

# -----------------------------------------------------------------------------
# Test 4: Empty results distinguished from failure (BR-003)
# Empty results (exit 0, count:0) must NOT trigger fallback
# -----------------------------------------------------------------------------
echo "--- Test 4: Empty Results != Failure (BR-003) ---"
if grep -qiE '(empty.*(result|set).*(not|valid|success|NOT.*error|NOT.*fail))' "$TARGET_FILE" 2>/dev/null || \
   grep -qiE '(count.*0|results.*\[\]).*(not|valid|success)' "$TARGET_FILE" 2>/dev/null || \
   grep -qiE 'NOT.*(an )?error.*empty' "$TARGET_FILE" 2>/dev/null; then
    pass "Empty results explicitly distinguished from failure (BR-003)"
else
    fail "Missing distinction between empty results and failure (BR-003)"
fi
echo ""

# -----------------------------------------------------------------------------
# Test 5: One-shot fallback, no retry loop (BR-002)
# Must not contain retry/loop/re-attempt language for Treelint after failure
# The fallback path should go directly to Grep
# -----------------------------------------------------------------------------
echo "--- Test 5: One-Shot Fallback, No Retry (BR-002) ---"
# Check for absence of retry/loop language in fallback context
retry_count=$(grep -ciE '(retry|re.?try|re.?attempt|loop|repeat).*treelint' "$TARGET_FILE" 2>/dev/null || echo "0")
retry_count=$(echo "$retry_count" | tr -d '\r\n')

if [[ "$retry_count" -eq 0 ]]; then
    pass "No Treelint retry/loop language found (BR-002 one-shot fallback)"
else
    fail "Found ${retry_count} retry/loop reference(s) - violates BR-002 one-shot fallback"
fi
echo ""

# -----------------------------------------------------------------------------
# Test 6: Non-zero exit code handling documented
# Must mention handling of non-zero exit codes generally
# -----------------------------------------------------------------------------
echo "--- Test 6: Non-Zero Exit Code Handling ---"
if grep -qiE '(non.?zero|exit.?code|exit code [1-9])' "$TARGET_FILE" 2>/dev/null; then
    pass "Non-zero exit code handling documented"
else
    fail "Missing general non-zero exit code handling documentation"
fi
echo ""

# -----------------------------------------------------------------------------
# Test 7: No exception propagation to parent skill
# Must not propagate errors - all failures caught and handled
# -----------------------------------------------------------------------------
echo "--- Test 7: No Exception Propagation ---"
# Check for recovery/catch language in error handling sections
if grep -qiE '(recover|catch|handle|fallback|fall back)' "$TARGET_FILE" 2>/dev/null; then
    pass "Error recovery language present (catch/handle/fallback)"
else
    fail "Missing error recovery language - errors may propagate to parent skill"
fi
echo ""

# =============================================================================
# Summary
# =============================================================================
echo "=============================================="
echo "  AC#5 Results: ${PASS_COUNT} passed, ${FAIL_COUNT} failed (${TOTAL_COUNT} total)"
echo "=============================================="

if [[ "$FAIL_COUNT" -gt 0 ]]; then
    echo "  STATUS: FAILED"
    exit 1
else
    echo "  STATUS: PASSED"
    exit 0
fi
