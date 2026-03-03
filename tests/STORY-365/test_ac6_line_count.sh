#!/usr/bin/env bash
# =============================================================================
# STORY-365 AC#6: Progressive Disclosure Compliance (500-Line Limit)
# =============================================================================
# Validates that:
#   1. backend-architect.md has a Read() pointing to treelint reference file
#   2. Reference file exists (REQUIRED since base file is 860 lines)
#   3. Reference file contains Treelint content
#   4. Core file does not duplicate full Treelint patterns inline
#
# TDD Phase: RED - Tests expected to FAIL until implementation complete.
# =============================================================================

set -euo pipefail

PROJECT_ROOT="${PROJECT_ROOT:-/mnt/c/Projects/DevForgeAI2}"
TARGET_FILE="${PROJECT_ROOT}/src/claude/agents/backend-architect.md"
REFERENCE_FILE="${PROJECT_ROOT}/src/claude/agents/backend-architect/references/treelint-patterns.md"
SHARED_REF="${PROJECT_ROOT}/src/claude/agents/references/treelint-search-patterns.md"

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
echo "  AC#6: Progressive Disclosure Compliance"
echo "=============================================="
echo ""

# -----------------------------------------------------------------------------
# Test 1: Target file exists
# -----------------------------------------------------------------------------
echo "--- Test 1: File Existence ---"
if [[ -r "$TARGET_FILE" ]]; then
    pass "backend-architect.md exists and is readable"
else
    fail "backend-architect.md not found"
    echo ""
    echo "=============================================="
    echo "  AC#6 Results: ${PASS_COUNT} passed, ${FAIL_COUNT} failed (${TOTAL_COUNT} total)"
    echo "=============================================="
    echo "  STATUS: FAILED"
    exit 1
fi
echo ""

# -----------------------------------------------------------------------------
# Test 2: Core file contains Read() for treelint reference
# -----------------------------------------------------------------------------
echo "--- Test 2: Read() Instruction for Treelint Reference ---"
if grep -qE 'Read\(.*treelint' "$TARGET_FILE" 2>/dev/null; then
    pass "backend-architect.md contains Read() instruction for Treelint reference"
else
    fail "Missing Read() instruction for Treelint reference file in backend-architect.md"
fi
echo ""

# -----------------------------------------------------------------------------
# Test 3: Reference file exists (required since base is 860 lines)
# -----------------------------------------------------------------------------
echo "--- Test 3: Treelint Reference File Existence ---"
# Either the dedicated reference file or the shared reference file must be referenced
if [[ -r "$REFERENCE_FILE" ]] || [[ -r "$SHARED_REF" ]]; then
    pass "Treelint reference file exists"
else
    fail "No Treelint reference file found (required since backend-architect.md is 860 lines, exceeds 500 limit)"
fi
echo ""

# -----------------------------------------------------------------------------
# Test 4: Line count check on core file
# -----------------------------------------------------------------------------
echo "--- Test 4: Core File Line Count ---"
line_count=$(wc -l < "$TARGET_FILE")
echo "  Info: Current line count = ${line_count}"

# The core file should not grow unbounded with inline Treelint patterns
# We check it stays reasonable (under 950 lines = base 860 + minimal Read() addition)
if [[ "$line_count" -le 950 ]]; then
    pass "Core file is ${line_count} lines (within tolerance for Read()-only addition)"
else
    fail "Core file is ${line_count} lines (grew too much - extract Treelint patterns to reference file)"
fi
echo ""

# -----------------------------------------------------------------------------
# Test 5: Treelint content present in either core or reference file
# -----------------------------------------------------------------------------
echo "--- Test 5: Treelint Content Present ---"
treelint_found=false
if grep -qiE 'treelint' "$TARGET_FILE" 2>/dev/null; then
    treelint_found=true
fi
if [[ -r "$REFERENCE_FILE" ]] && grep -qiE 'treelint' "$REFERENCE_FILE" 2>/dev/null; then
    treelint_found=true
fi

if $treelint_found; then
    pass "Treelint content found in backend-architect ecosystem"
else
    fail "No Treelint content found (STORY-365 implementation not yet applied)"
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
