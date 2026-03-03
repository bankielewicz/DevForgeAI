#!/usr/bin/env bash
# =============================================================================
# STORY-372 AC#3: Semantic Correlation Between Test and Source Functions
# =============================================================================
# Validates that coverage-analyzer.md (or its reference files) contains:
#   1. Naming convention correlation rules
#   2. Source functions classified as covered or uncovered
#   3. Mapping stored as structured list (source_function, matched_tests, status)
#   4. Correlation section heading
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
echo "  AC#3: Semantic Correlation Between Test and Source Functions"
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
    echo "  AC#3 Results: ${PASS_COUNT} passed, ${FAIL_COUNT} failed (${TOTAL_COUNT} total)"
    echo "=============================================="
    echo "  STATUS: FAILED"
    exit 1
fi
echo ""

# -----------------------------------------------------------------------------
# Test 2: Naming convention correlation rules documented
# -----------------------------------------------------------------------------
echo "--- Test 2: Naming Convention Correlation Rules ---"
if grep -qiE '(naming.*convention.*correlat|correlat.*naming.*convention|naming.*convention.*rule|naming.*convention.*match)' $(search_files) 2>/dev/null; then
    pass "Naming convention correlation rules documented"
else
    fail "Missing naming convention correlation rules"
fi
echo ""

# -----------------------------------------------------------------------------
# Test 3: Source functions classified as covered/uncovered
# -----------------------------------------------------------------------------
echo "--- Test 3: Covered/Uncovered Classification ---"
if grep -qiE '(classif.*covered.*uncovered|covered.*uncovered.*classif|source.*function.*(covered|uncovered)|status.*(covered|uncovered))' $(search_files) 2>/dev/null; then
    pass "Source function covered/uncovered classification documented"
else
    fail "Missing covered/uncovered classification for source functions"
fi
echo ""

# -----------------------------------------------------------------------------
# Test 4: Mapping stored as structured list with source_function field
# -----------------------------------------------------------------------------
echo "--- Test 4: Structured Mapping with source_function ---"
if grep -qE '(source_function|"source_function")' $(search_files) 2>/dev/null; then
    pass "Mapping includes source_function field"
else
    fail "Missing source_function field in correlation mapping structure"
fi
echo ""

# -----------------------------------------------------------------------------
# Test 5: Mapping includes matched_tests field
# -----------------------------------------------------------------------------
echo "--- Test 5: Structured Mapping with matched_tests ---"
if grep -qE '(matched_tests|"matched_tests")' $(search_files) 2>/dev/null; then
    pass "Mapping includes matched_tests field"
else
    fail "Missing matched_tests field in correlation mapping structure"
fi
echo ""

# -----------------------------------------------------------------------------
# Test 6: Mapping includes status field (covered/uncovered)
# -----------------------------------------------------------------------------
echo "--- Test 6: Structured Mapping with status Field ---"
if grep -qE '("status"|status).*(covered|uncovered)' $(search_files) 2>/dev/null; then
    pass "Mapping includes status field with covered/uncovered values"
else
    fail "Missing status field in correlation mapping structure"
fi
echo ""

# -----------------------------------------------------------------------------
# Test 7: Section heading for semantic correlation
# -----------------------------------------------------------------------------
echo "--- Test 7: Semantic Correlation Section Heading ---"
if grep -qiE '^#{1,4}.*[Ss]emantic.*[Cc]orrelat|^#{1,4}.*[Cc]orrelat.*[Tt]est.*[Ss]ource' $(search_files) 2>/dev/null; then
    pass "Semantic correlation section heading found"
else
    fail "Missing section heading for semantic correlation between test and source functions"
fi
echo ""

# =============================================================================
# Summary
# =============================================================================
echo "=============================================="
echo "  AC#3 Results: ${PASS_COUNT} passed, ${FAIL_COUNT} failed (${TOTAL_COUNT} total)"
echo "=============================================="

if [[ "$FAIL_COUNT" -gt 0 ]]; then
    echo "  STATUS: FAILED"
    exit 1
else
    echo "  STATUS: PASSED"
    exit 0
fi
