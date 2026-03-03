#!/usr/bin/env bash
# =============================================================================
# STORY-372 AC#6: Handle Multiple Test Files per Source File
# =============================================================================
# Validates that coverage-analyzer.md (or its reference files) contains:
#   1. Multi-file test aggregation logic
#   2. Tests aggregated from multiple test files before correlation
#   3. Source function covered if any test file contains matching test
#   4. matched_tests lists originating test file
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
echo "  AC#6: Handle Multiple Test Files per Source File"
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
    echo "  AC#6 Results: ${PASS_COUNT} passed, ${FAIL_COUNT} failed (${TOTAL_COUNT} total)"
    echo "=============================================="
    echo "  STATUS: FAILED"
    exit 1
fi
echo ""

# -----------------------------------------------------------------------------
# Test 2: Multi-file test aggregation documented
# -----------------------------------------------------------------------------
echo "--- Test 2: Multi-File Test Aggregation ---"
if grep -qiE '(multi.*file.*aggregat|aggregat.*multi.*file|multiple.*test.*file.*aggregat|aggregat.*test.*function.*multiple)' $(search_files) 2>/dev/null; then
    pass "Multi-file test aggregation logic documented"
else
    fail "Missing multi-file test aggregation logic"
fi
echo ""

# -----------------------------------------------------------------------------
# Test 3: Tests aggregated before correlation
# -----------------------------------------------------------------------------
echo "--- Test 3: Aggregation Before Correlation ---"
if grep -qiE '(aggregat.*before.*correlat|collect.*test.*before.*correlat|all.*test.*file.*before)' $(search_files) 2>/dev/null; then
    pass "Tests aggregated before correlation step"
else
    fail "Missing documentation that tests are aggregated before correlation"
fi
echo ""

# -----------------------------------------------------------------------------
# Test 4: Source function covered if any test file matches
# -----------------------------------------------------------------------------
echo "--- Test 4: Covered if Any Test File Matches ---"
if grep -qiE '(covered.*any.*test.*file|any.*test.*file.*match.*covered|at least one.*test.*covered|any.*matching.*test.*covered)' $(search_files) 2>/dev/null; then
    pass "Source function marked covered if any test file contains matching test"
else
    fail "Missing 'covered if any test file matches' rule"
fi
echo ""

# -----------------------------------------------------------------------------
# Test 5: matched_tests includes originating test file
# -----------------------------------------------------------------------------
echo "--- Test 5: matched_tests Lists Originating File ---"
if grep -qiE '(matched_tests.*file|originating.*test.*file|test.*file.*matched_tests|matched_tests.*origin)' $(search_files) 2>/dev/null; then
    pass "matched_tests includes originating test file"
else
    fail "Missing matched_tests with originating test file tracking"
fi
echo ""

# -----------------------------------------------------------------------------
# Test 6: Section heading for multi-file handling
# -----------------------------------------------------------------------------
echo "--- Test 6: Multi-File Handling Section ---"
if grep -qiE '^#{1,4}.*[Mm]ulti.*[Tt]est.*[Ff]ile|^#{1,4}.*[Mm]ultiple.*[Tt]est.*[Ff]ile|^#{1,4}.*[Aa]ggregat.*[Tt]est' $(search_files) 2>/dev/null; then
    pass "Multi-file handling section heading found"
else
    fail "Missing section heading for multi-file test handling"
fi
echo ""

# =============================================================================
# Summary
# =============================================================================
echo "=============================================="
echo "  AC#6 Results: ${PASS_COUNT} passed, ${FAIL_COUNT} failed (${TOTAL_COUNT} total)"
echo "=============================================="

if [[ "$FAIL_COUNT" -gt 0 ]]; then
    echo "  STATUS: FAILED"
    exit 1
else
    echo "  STATUS: PASSED"
    exit 0
fi
