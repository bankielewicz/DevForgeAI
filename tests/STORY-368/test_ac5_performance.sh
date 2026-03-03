#!/usr/bin/env bash
# =============================================================================
# STORY-368 AC#5: Performance Validation for Treelint Searches
# =============================================================================
# Validates that coverage-analyzer.md (or its reference file) contains:
#   1. Performance target documentation (<100ms)
#   2. stats.elapsed_ms field reference
#   3. Total overhead target (<200ms) documented
#
# TDD Phase: RED - Tests expected to FAIL until implementation complete.
# =============================================================================

set -euo pipefail

PROJECT_ROOT="${PROJECT_ROOT:-/mnt/c/Projects/DevForgeAI2}"
TARGET_FILE="${PROJECT_ROOT}/src/claude/agents/coverage-analyzer.md"
REFERENCE_FILE="${PROJECT_ROOT}/src/claude/agents/coverage-analyzer/references/treelint-patterns.md"

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

search_files() {
    local files="$TARGET_FILE"
    if [[ -r "$REFERENCE_FILE" ]]; then
        files="$TARGET_FILE $REFERENCE_FILE"
    fi
    echo "$files"
}

echo "=============================================="
echo "  AC#5: Performance Validation for Treelint Searches"
echo "=============================================="
echo ""

# -----------------------------------------------------------------------------
# Test 1: Target file exists
# -----------------------------------------------------------------------------
echo "--- Test 1: File Existence ---"
if [[ -r "$TARGET_FILE" ]]; then
    pass "coverage-analyzer.md exists and is readable"
else
    fail "coverage-analyzer.md not found"
    echo ""
    echo "=============================================="
    echo "  AC#5 Results: ${PASS_COUNT} passed, ${FAIL_COUNT} failed (${TOTAL_COUNT} total)"
    echo "=============================================="
    echo "  STATUS: FAILED"
    exit 1
fi
echo ""

# -----------------------------------------------------------------------------
# Test 2: Performance target (<100ms) documented
# -----------------------------------------------------------------------------
echo "--- Test 2: Performance Target Documentation ---"
if grep -qiE '100.*ms|100.*millisecond|< *100ms|under 100' $(search_files) 2>/dev/null; then
    pass "Performance target (<100ms) documented"
else
    fail "Missing performance target (<100ms) documentation for Treelint searches"
fi
echo ""

# -----------------------------------------------------------------------------
# Test 3: stats.elapsed_ms field referenced
# -----------------------------------------------------------------------------
echo "--- Test 3: stats.elapsed_ms Field Reference ---"
if grep -qE 'stats\.elapsed_ms|stats\[.elapsed_ms.\]|elapsed_ms' $(search_files) 2>/dev/null; then
    pass "stats.elapsed_ms field referenced for performance validation"
else
    fail "Missing stats.elapsed_ms field reference"
fi
echo ""

# -----------------------------------------------------------------------------
# Test 4: Total overhead target (<200ms) documented
# -----------------------------------------------------------------------------
echo "--- Test 4: Total Overhead Target ---"
if grep -qiE '200.*ms|200.*millisecond|< *200ms|under 200|overhead.*200' $(search_files) 2>/dev/null; then
    pass "Total overhead target (<200ms) documented"
else
    fail "Missing total overhead target (<200ms) documentation"
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
