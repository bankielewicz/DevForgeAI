#!/usr/bin/env bash
# =============================================================================
# STORY-368 AC#4: Coverage Data Correlation with Function Symbols
# =============================================================================
# Validates that coverage-analyzer.md (or its reference file) contains:
#   1. Coverage-to-function correlation section heading
#   2. Instructions for mapping uncovered_lines to function boundaries
#   3. Treelint line ranges [start, end] used for boundary mapping
#   4. Module-level uncovered code handled separately (BR-005)
#   5. Enhanced gaps array output with function-level detail
#   6. Nested function handling documented (BR-006)
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
echo "  AC#4: Coverage Data Correlation with Function Symbols"
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
    echo "  AC#4 Results: ${PASS_COUNT} passed, ${FAIL_COUNT} failed (${TOTAL_COUNT} total)"
    echo "=============================================="
    echo "  STATUS: FAILED"
    exit 1
fi
echo ""

# -----------------------------------------------------------------------------
# Test 2: Coverage-to-function correlation section heading
# -----------------------------------------------------------------------------
echo "--- Test 2: Correlation Section Heading ---"
if grep -qiE '^#{1,4}.*(correlat|mapp).*function.*(boundar|symbol|coverage)|^#{1,4}.*function.*(correlat|boundar).*coverage' $(search_files) 2>/dev/null; then
    pass "Coverage-to-function correlation section heading found"
else
    fail "Missing correlation section heading (e.g., '### Coverage Data Correlation with Function Boundaries')"
fi
echo ""

# -----------------------------------------------------------------------------
# Test 3: Mapping uncovered_lines to function boundaries
# -----------------------------------------------------------------------------
echo "--- Test 3: Uncovered Lines to Function Mapping ---"
if grep -qiE 'uncovered.*(line|range).*function.*(boundar|range)|function.*(boundar|range).*uncovered|correlat.*uncovered.*function' $(search_files) 2>/dev/null; then
    pass "Instructions for mapping uncovered lines to function boundaries found"
else
    fail "Missing instructions for mapping uncovered_lines to function boundaries"
fi
echo ""

# -----------------------------------------------------------------------------
# Test 4: Uses Treelint line ranges [start, end] for boundary mapping
# -----------------------------------------------------------------------------
echo "--- Test 4: Treelint Line Ranges for Boundary Mapping ---"
if grep -qiE '\[start.*end\].*function|function.*\[start.*end\]|line.*range.*start.*end|lines.*start.*end.*boundar' $(search_files) 2>/dev/null; then
    pass "Uses Treelint line ranges [start, end] for function boundary mapping"
else
    fail "Missing Treelint [start, end] line range usage for boundary mapping"
fi
echo ""

# -----------------------------------------------------------------------------
# Test 5: Module-level uncovered code handled separately (BR-005)
# -----------------------------------------------------------------------------
echo "--- Test 5: Module-Level Code Handling ---"
if grep -qiE 'module.level|outside.*function.*boundar|function_name.*null|lines.*not.*within.*function' $(search_files) 2>/dev/null; then
    pass "Module-level uncovered code handling documented"
else
    fail "Missing module-level uncovered code handling (BR-005: lines outside function boundaries)"
fi
echo ""

# -----------------------------------------------------------------------------
# Test 6: Enhanced gaps array with function-level detail
# -----------------------------------------------------------------------------
echo "--- Test 6: Enhanced Gaps Array with Function Detail ---"
if grep -qiE 'function_name|function_coverage|function_lines|function.*detail.*gap|gap.*function.*detail' $(search_files) 2>/dev/null; then
    pass "Enhanced gaps array includes function-level detail fields"
else
    fail "Missing function-level detail in gaps array (function_name, function_lines, function_coverage)"
fi
echo ""

# -----------------------------------------------------------------------------
# Test 7: Nested function handling documented (BR-006)
# -----------------------------------------------------------------------------
echo "--- Test 7: Nested Function Handling ---"
if grep -qiE 'nested.*function|inner.*function|innermost.*function|overlapping.*function|most specific.*function' $(search_files) 2>/dev/null; then
    pass "Nested function handling documented"
else
    fail "Missing nested function handling documentation (BR-006: attribute to innermost function)"
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
