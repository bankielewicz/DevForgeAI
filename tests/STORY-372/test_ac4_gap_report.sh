#!/usr/bin/env bash
# =============================================================================
# STORY-372 AC#4: Coverage Gap Identification at Function Level
# =============================================================================
# Validates that coverage-analyzer.md (or its reference files) contains:
#   1. function_level_gaps section in gap report
#   2. Gap entries include file path, function name, line range
#   3. Gap entries include suggested test scenario
#   4. Enclosing class in gap entries
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
echo "  AC#4: Coverage Gap Identification at Function Level"
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
# Test 2: function_level_gaps key documented in gap report
# -----------------------------------------------------------------------------
echo "--- Test 2: function_level_gaps Key ---"
if grep -qE '(function_level_gaps|"function_level_gaps")' $(search_files) 2>/dev/null; then
    pass "function_level_gaps key documented in gap report"
else
    fail "Missing function_level_gaps key in gap report documentation"
fi
echo ""

# -----------------------------------------------------------------------------
# Test 3: Gap entry includes file path
# -----------------------------------------------------------------------------
echo "--- Test 3: Gap Entry File Path ---"
if grep -qiE '(function_level_gaps|function.*gap)' $(search_files) 2>/dev/null && \
   grep -qE '("file"|file.*path|"file_path")' $(search_files) 2>/dev/null; then
    pass "Gap entries include file path"
else
    fail "Missing file path field in function-level gap entries"
fi
echo ""

# -----------------------------------------------------------------------------
# Test 4: Gap entry includes function name
# -----------------------------------------------------------------------------
echo "--- Test 4: Gap Entry Function Name ---"
if grep -qiE '(function_level_gaps|function.*gap)' $(search_files) 2>/dev/null && \
   grep -qE '("name"|function_name|"function_name")' $(search_files) 2>/dev/null; then
    pass "Gap entries include function name"
else
    fail "Missing function name field in function-level gap entries"
fi
echo ""

# -----------------------------------------------------------------------------
# Test 5: Gap entry includes line range
# -----------------------------------------------------------------------------
echo "--- Test 5: Gap Entry Line Range ---"
if grep -qiE '(function_level_gaps|function.*gap)' $(search_files) 2>/dev/null && \
   grep -qE '("lines"|line.*range|start.*end)' $(search_files) 2>/dev/null; then
    pass "Gap entries include line range"
else
    fail "Missing line range field in function-level gap entries"
fi
echo ""

# -----------------------------------------------------------------------------
# Test 6: Gap entry includes suggested test scenario
# -----------------------------------------------------------------------------
echo "--- Test 6: Suggested Test Scenario ---"
if grep -qiE '(suggested.*test|test.*suggest|suggested_test|test.*scenario)' $(search_files) 2>/dev/null; then
    pass "Gap entries include suggested test scenario"
else
    fail "Missing suggested test scenario in function-level gap entries"
fi
echo ""

# -----------------------------------------------------------------------------
# Test 7: Gap entry includes enclosing class
# -----------------------------------------------------------------------------
echo "--- Test 7: Enclosing Class in Gap Entries ---"
if grep -qiE '(function_level_gaps|function.*gap)' $(search_files) 2>/dev/null && \
   grep -qiE '(enclosing.class|enclosing_class|"class"|parent.class)' $(search_files) 2>/dev/null; then
    pass "Gap entries include enclosing class reference"
else
    fail "Missing enclosing class field in function-level gap entries"
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
