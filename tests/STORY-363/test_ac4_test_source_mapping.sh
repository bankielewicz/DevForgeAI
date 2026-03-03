#!/usr/bin/env bash
# =============================================================================
# STORY-363 AC#4: Test File to Source File Mapping Using Semantic Search
# =============================================================================
# Validates that test-automator.md contains:
#   1. Test-to-source mapping instructions
#   2. Uses Treelint for bidirectional search (test->source and source->test)
#   3. Describes test_ prefix removal or describe()/it() subject extraction
#   4. Documents untested function identification
#
# TDD Phase: RED - Tests expected to FAIL until implementation complete.
# =============================================================================

set -euo pipefail

PROJECT_ROOT="${PROJECT_ROOT:-/mnt/c/Projects/DevForgeAI2}"
TARGET_FILE="${PROJECT_ROOT}/src/claude/agents/test-automator.md"

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
echo "  AC#4: Test-to-Source File Mapping"
echo "=============================================="
echo ""

# -----------------------------------------------------------------------------
# Test 1: Target file exists
# -----------------------------------------------------------------------------
echo "--- Test 1: File Existence ---"
if [[ -r "$TARGET_FILE" ]]; then
    pass "test-automator.md exists and is readable"
else
    fail "test-automator.md not found"
    echo ""
    echo "=============================================="
    echo "  AC#4 Results: ${PASS_COUNT} passed, ${FAIL_COUNT} failed (${TOTAL_COUNT} total)"
    echo "=============================================="
    echo "  STATUS: FAILED"
    exit 1
fi
echo ""

# -----------------------------------------------------------------------------
# Test 2: Test-to-source mapping section exists
# -----------------------------------------------------------------------------
echo "--- Test 2: Mapping Section Heading ---"
if grep -qiE '^#{1,4}.*(test.*source.*map|map.*test.*source|source.*map)' "$TARGET_FILE" 2>/dev/null; then
    pass "Test-to-source mapping section heading found"
else
    fail "Missing test-to-source mapping section heading"
fi
echo ""

# -----------------------------------------------------------------------------
# Test 3: Uses Treelint for bidirectional search
# Must reference treelint search in the mapping context
# -----------------------------------------------------------------------------
echo "--- Test 3: Treelint Used for Mapping ---"
if grep -qiE 'treelint.*search' "$TARGET_FILE" 2>/dev/null; then
    pass "Treelint search referenced for mapping"
else
    fail "Missing Treelint search reference in mapping instructions"
fi
echo ""

# -----------------------------------------------------------------------------
# Test 4: Describes test_ prefix removal or describe()/it() extraction
# Must document how test function names map to source function names
# -----------------------------------------------------------------------------
echo "--- Test 4: Name Mapping Strategy Documented ---"
if grep -qiE '(test_.*prefix|remove.*test_|describe\(\)|it\(\)|subject.*extract)' "$TARGET_FILE" 2>/dev/null; then
    pass "Name mapping strategy (prefix removal or subject extraction) documented"
else
    fail "Missing name mapping strategy (test_ prefix removal or describe()/it() extraction)"
fi
echo ""

# -----------------------------------------------------------------------------
# Test 5: Documents untested function identification
# Must mention identifying functions without corresponding tests
# -----------------------------------------------------------------------------
echo "--- Test 5: Untested Function Identification ---"
if grep -qiE '(untested|uncovered|missing.*test|coverage.*gap|no.*test)' "$TARGET_FILE" 2>/dev/null; then
    pass "Untested function identification documented"
else
    fail "Missing documentation for identifying untested functions"
fi
echo ""

# =============================================================================
# Summary
# =============================================================================
echo "=============================================="
echo "  AC#4 Results: ${PASS_COUNT} passed, ${FAIL_COUNT} failed (${TOTAL_COUNT} total)"
echo "=============================================="

if [[ "$FAIL_COUNT" -gt 0 ]]; then
    echo "  STATUS: FAILED"
    exit 1
else
    echo "  STATUS: PASSED"
    exit 0
fi
