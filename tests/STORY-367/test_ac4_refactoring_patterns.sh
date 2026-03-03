#!/usr/bin/env bash
# =============================================================================
# STORY-367 AC#4: Refactoring-Specific Treelint Patterns (Code Smell Detection)
# =============================================================================
# Validates that refactoring-specialist.md (or its reference file) contains:
#   1. God Object detection pattern (class >500 lines via line range)
#   2. Long Method detection pattern (function >50 lines via line range)
#   3. Extract Class candidates via treelint map --ranked
#   4. Long Parameter List detection via signature analysis (>4 params)
#   5. At least 4 distinct code smell patterns documented
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
echo "  AC#4: Refactoring-Specific Treelint Patterns"
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
    echo "  AC#4 Results: ${PASS_COUNT} passed, ${FAIL_COUNT} failed (${TOTAL_COUNT} total)"
    echo "=============================================="
    echo "  STATUS: FAILED"
    exit 1
fi
echo ""

# -----------------------------------------------------------------------------
# Test 2: God Object detection pattern (class >500 lines)
# -----------------------------------------------------------------------------
echo "--- Test 2: God Object Detection Pattern ---"
GOD_FOUND=0
if grep -qiE 'God Object' $(search_files) 2>/dev/null; then
    GOD_FOUND=$((GOD_FOUND + 1))
fi
if grep -qiE '>.*500.*line|500.*line|class.*500' $(search_files) 2>/dev/null; then
    GOD_FOUND=$((GOD_FOUND + 1))
fi
if grep -qiE 'treelint.*class.*line.*range|line.*range.*class|class.*size' $(search_files) 2>/dev/null; then
    GOD_FOUND=$((GOD_FOUND + 1))
fi

if [[ "$GOD_FOUND" -ge 2 ]]; then
    pass "God Object detection pattern documented with >500 line threshold"
else
    fail "Missing God Object detection pattern (need 'God Object' + '>500 lines' + treelint class analysis)"
fi
echo ""

# -----------------------------------------------------------------------------
# Test 3: Long Method detection pattern (function >50 lines)
# -----------------------------------------------------------------------------
echo "--- Test 3: Long Method Detection Pattern ---"
LONG_FOUND=0
if grep -qiE 'Long Method' $(search_files) 2>/dev/null; then
    LONG_FOUND=$((LONG_FOUND + 1))
fi
if grep -qiE '>.*50.*line|50.*line|function.*50' $(search_files) 2>/dev/null; then
    LONG_FOUND=$((LONG_FOUND + 1))
fi
if grep -qiE 'treelint.*function.*line|line.*range.*function|function.*size|method.*size' $(search_files) 2>/dev/null; then
    LONG_FOUND=$((LONG_FOUND + 1))
fi

if [[ "$LONG_FOUND" -ge 2 ]]; then
    pass "Long Method detection pattern documented with >50 line threshold"
else
    fail "Missing Long Method detection pattern (need 'Long Method' + '>50 lines' + treelint function analysis)"
fi
echo ""

# -----------------------------------------------------------------------------
# Test 4: Extract Class candidates via treelint map --ranked
# -----------------------------------------------------------------------------
echo "--- Test 4: Extract Class via Treelint Map Ranked ---"
if grep -qiE 'treelint map.*--ranked|Extract Class.*treelint|treelint.*Extract.*Class' $(search_files) 2>/dev/null; then
    pass "Extract Class candidates via treelint map --ranked documented"
else
    fail "Missing Extract Class candidates via treelint map --ranked"
fi
echo ""

# -----------------------------------------------------------------------------
# Test 5: Long Parameter List detection (>4 params)
# -----------------------------------------------------------------------------
echo "--- Test 5: Long Parameter List Detection ---"
PARAM_FOUND=0
if grep -qiE 'Long Parameter' $(search_files) 2>/dev/null; then
    PARAM_FOUND=$((PARAM_FOUND + 1))
fi
if grep -qiE '>.*4.*param|4.*param|param.*>.*4|more than 4' $(search_files) 2>/dev/null; then
    PARAM_FOUND=$((PARAM_FOUND + 1))
fi

if [[ "$PARAM_FOUND" -ge 2 ]]; then
    pass "Long Parameter List detection documented with >4 param threshold"
else
    fail "Missing Long Parameter List detection (need 'Long Parameter List' + '>4 parameters')"
fi
echo ""

# -----------------------------------------------------------------------------
# Test 6: At least 4 distinct code smell patterns with treelint integration
# -----------------------------------------------------------------------------
echo "--- Test 6: Minimum 4 Treelint-Powered Code Smell Patterns ---"
SMELL_COUNT=0
if grep -qiE 'God Object' $(search_files) 2>/dev/null; then
    SMELL_COUNT=$((SMELL_COUNT + 1))
fi
if grep -qiE 'Long Method' $(search_files) 2>/dev/null; then
    SMELL_COUNT=$((SMELL_COUNT + 1))
fi
if grep -qiE 'Extract Class' $(search_files) 2>/dev/null; then
    SMELL_COUNT=$((SMELL_COUNT + 1))
fi
if grep -qiE 'Long Parameter' $(search_files) 2>/dev/null; then
    SMELL_COUNT=$((SMELL_COUNT + 1))
fi

if [[ "$SMELL_COUNT" -ge 4 ]]; then
    pass "Found ${SMELL_COUNT} distinct code smell patterns (minimum 4 required)"
else
    fail "Only ${SMELL_COUNT} code smell patterns found (need at least 4: God Object, Long Method, Extract Class, Long Parameter List)"
fi
echo ""

# -----------------------------------------------------------------------------
# Test 7: Treelint command examples for code smell detection
# -----------------------------------------------------------------------------
echo "--- Test 7: Treelint Command Examples in Code Smell Section ---"
if grep -qiE 'treelint search.*--type (class|function).*--format json' $(search_files) 2>/dev/null; then
    pass "Treelint command examples present in code smell detection patterns"
else
    fail "Missing Treelint command examples in code smell detection section"
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
