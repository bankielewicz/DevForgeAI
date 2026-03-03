#!/usr/bin/env bash
# =============================================================================
# STORY-372 AC#5: Integration with Coverage Analyzer Reports
# =============================================================================
# Validates that coverage-analyzer.md (or its reference files) contains:
#   1. function_coverage key in output JSON
#   2. total_functions field
#   3. covered_functions field
#   4. uncovered_functions field
#   5. coverage_percentage field
#   6. uncovered_list array
#   7. Recommendations reference function gaps
#
# TDD Phase: RED - Tests expected to FAIL until implementation complete.
# =============================================================================

set -euo pipefail

PROJECT_ROOT="${PROJECT_ROOT:-/mnt/c/Projects/DevForgeAI2}"
TARGET_FILE="${PROJECT_ROOT}/src/claude/agents/coverage-analyzer.md"
REFERENCE_DIR="${PROJECT_ROOT}/src/claude/agents/coverage-analyzer/references"

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
    if [[ -d "$REFERENCE_DIR" ]]; then
        for f in "$REFERENCE_DIR"/*.md; do
            [[ -r "$f" ]] && files="$files $f"
        done
    fi
    echo "$files"
}

echo "=============================================="
echo "  AC#5: Integration with Coverage Analyzer Reports"
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
# Test 2: function_coverage key in output JSON
# -----------------------------------------------------------------------------
echo "--- Test 2: function_coverage Key ---"
if grep -qE '(function_coverage|"function_coverage")' $(search_files) 2>/dev/null; then
    pass "function_coverage key documented in output JSON"
else
    fail "Missing function_coverage key in coverage-analyzer output JSON"
fi
echo ""

# -----------------------------------------------------------------------------
# Test 3: total_functions field
# -----------------------------------------------------------------------------
echo "--- Test 3: total_functions Field ---"
if grep -qE '(total_functions|"total_functions")' $(search_files) 2>/dev/null; then
    pass "total_functions field documented"
else
    fail "Missing total_functions field in function_coverage output"
fi
echo ""

# -----------------------------------------------------------------------------
# Test 4: covered_functions field
# -----------------------------------------------------------------------------
echo "--- Test 4: covered_functions Field ---"
if grep -qE '(covered_functions|"covered_functions")' $(search_files) 2>/dev/null; then
    pass "covered_functions field documented"
else
    fail "Missing covered_functions field in function_coverage output"
fi
echo ""

# -----------------------------------------------------------------------------
# Test 5: uncovered_functions field
# -----------------------------------------------------------------------------
echo "--- Test 5: uncovered_functions Field ---"
if grep -qE '(uncovered_functions|"uncovered_functions")' $(search_files) 2>/dev/null; then
    pass "uncovered_functions field documented"
else
    fail "Missing uncovered_functions field in function_coverage output"
fi
echo ""

# -----------------------------------------------------------------------------
# Test 6: coverage_percentage field
# -----------------------------------------------------------------------------
echo "--- Test 6: coverage_percentage Field ---"
if grep -qE '(coverage_percentage|"coverage_percentage")' $(search_files) 2>/dev/null; then
    pass "coverage_percentage field documented"
else
    fail "Missing coverage_percentage field in function_coverage output"
fi
echo ""

# -----------------------------------------------------------------------------
# Test 7: uncovered_list array
# -----------------------------------------------------------------------------
echo "--- Test 7: uncovered_list Array ---"
if grep -qE '(uncovered_list|"uncovered_list")' $(search_files) 2>/dev/null; then
    pass "uncovered_list array documented"
else
    fail "Missing uncovered_list array in function_coverage output"
fi
echo ""

# -----------------------------------------------------------------------------
# Test 8: Recommendations reference function gaps
# -----------------------------------------------------------------------------
echo "--- Test 8: Recommendations Reference Function Gaps ---"
if grep -qiE '(recommend.*function.*gap|function.*gap.*recommend|recommend.*function.*coverage)' $(search_files) 2>/dev/null; then
    pass "Recommendations reference function-level gaps"
else
    fail "Missing recommendations referencing function-level gaps"
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
