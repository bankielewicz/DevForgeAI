#!/usr/bin/env bash
# =============================================================================
# STORY-367 AC#2: JSON Parsing of Treelint Search Results
# =============================================================================
# Validates that refactoring-specialist.md (or its reference file) contains:
#   1. JSON parsing instructions referencing 'name' field
#   2. JSON parsing instructions referencing 'file' field
#   3. JSON parsing instructions referencing 'lines' field
#   4. JSON parsing instructions referencing 'signature' field
#   5. Line range calculation for code smell detection (lines[1] - lines[0])
#   6. Refactoring candidate prioritization from parsed data
#
# TDD Phase: RED - Tests expected to FAIL until implementation complete.
# =============================================================================

set -euo pipefail

PROJECT_ROOT="${PROJECT_ROOT:-/mnt/c/Projects/DevForgeAI2}"
TARGET_FILE="${PROJECT_ROOT}/src/claude/agents/refactoring-specialist.md"
REFERENCE_FILE="${PROJECT_ROOT}/src/claude/agents/refactoring-specialist/references/treelint-refactoring-patterns.md"

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
echo "  AC#2: JSON Parsing of Treelint Search Results"
echo "=============================================="
echo ""

# -----------------------------------------------------------------------------
# Test 1: Target file exists
# -----------------------------------------------------------------------------
echo "--- Test 1: File Existence ---"
if [[ -r "$TARGET_FILE" ]]; then
    pass "refactoring-specialist.md exists and is readable"
else
    fail "refactoring-specialist.md not found"
    echo ""
    echo "=============================================="
    echo "  AC#2 Results: ${PASS_COUNT} passed, ${FAIL_COUNT} failed (${TOTAL_COUNT} total)"
    echo "=============================================="
    echo "  STATUS: FAILED"
    exit 1
fi
echo ""

# -----------------------------------------------------------------------------
# Test 2: References 'name' field in JSON parsing
# -----------------------------------------------------------------------------
echo "--- Test 2: JSON Field - name ---"
if grep -qiE 'name.*field|field.*name|results?\[\]\.name|\bname\b.*function name|extract.*name' $(search_files) 2>/dev/null; then
    pass "JSON parsing references 'name' field"
else
    fail "Missing 'name' field reference in JSON parsing instructions"
fi
echo ""

# -----------------------------------------------------------------------------
# Test 3: References 'file' field in JSON parsing
# -----------------------------------------------------------------------------
echo "--- Test 3: JSON Field - file ---"
if grep -qiE 'file.*field|field.*file|results?\[\]\.file|\bfile\b.*path|file.*source' $(search_files) 2>/dev/null; then
    pass "JSON parsing references 'file' field"
else
    fail "Missing 'file' field reference in JSON parsing instructions"
fi
echo ""

# -----------------------------------------------------------------------------
# Test 4: References 'lines' field in JSON parsing
# -----------------------------------------------------------------------------
echo "--- Test 4: JSON Field - lines ---"
if grep -qiE 'lines.*field|field.*lines|results?\[\]\.lines|line.*range|lines\[|lines.*start.*end' $(search_files) 2>/dev/null; then
    pass "JSON parsing references 'lines' field"
else
    fail "Missing 'lines' field reference in JSON parsing instructions"
fi
echo ""

# -----------------------------------------------------------------------------
# Test 5: References 'signature' field in JSON parsing
# -----------------------------------------------------------------------------
echo "--- Test 5: JSON Field - signature ---"
if grep -qiE 'signature.*field|field.*signature|results?\[\]\.signature|function.*signature|signature.*param' $(search_files) 2>/dev/null; then
    pass "JSON parsing references 'signature' field"
else
    fail "Missing 'signature' field reference in JSON parsing instructions"
fi
echo ""

# -----------------------------------------------------------------------------
# Test 6: Line range used for size calculation (code smell detection)
# -----------------------------------------------------------------------------
echo "--- Test 6: Line Range Calculation for Code Smell Detection ---"
if grep -qiE 'lines\[1\].*lines\[0\]|end.*start|line.*range.*calculat|line.*count.*smell|size.*line.*range' $(search_files) 2>/dev/null; then
    pass "Line range calculation documented for code smell detection"
else
    fail "Missing line range calculation for code smell detection (e.g., 'lines[1] - lines[0]')"
fi
echo ""

# -----------------------------------------------------------------------------
# Test 7: Parameter count detection from signature
# -----------------------------------------------------------------------------
echo "--- Test 7: Parameter Count from Signature ---"
if grep -qiE 'param.*count|parameter.*count|signature.*param|\>4.*param|param.*\>.*4' $(search_files) 2>/dev/null; then
    pass "Parameter count detection from signature documented"
else
    fail "Missing parameter count detection from signature for Long Parameter List smell"
fi
echo ""

# =============================================================================
# Summary
# =============================================================================
echo "=============================================="
echo "  AC#2 Results: ${PASS_COUNT} passed, ${FAIL_COUNT} failed (${TOTAL_COUNT} total)"
echo "=============================================="

if [[ "$FAIL_COUNT" -gt 0 ]]; then
    echo "  STATUS: FAILED"
    exit 1
else
    echo "  STATUS: PASSED"
    exit 0
fi
