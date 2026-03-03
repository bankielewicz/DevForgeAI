#!/usr/bin/env bash
# =============================================================================
# STORY-368 AC#6: Progressive Disclosure Compliance (500-Line Limit)
# =============================================================================
# Validates that:
#   1. coverage-analyzer.md is <= 500 lines
#   2. If >500 lines, reference file exists at references/treelint-patterns.md
#   3. Core file contains Read() for treelint reference
#   4. Treelint content is present in either core or reference file
#
# TDD Phase: RED - Tests expected to FAIL until implementation complete.
# =============================================================================

set -euo pipefail

PROJECT_ROOT="${PROJECT_ROOT:-/mnt/c/Projects/DevForgeAI2}"
TARGET_FILE="${PROJECT_ROOT}/src/claude/agents/coverage-analyzer.md"
REFERENCE_FILE="${PROJECT_ROOT}/src/claude/agents/coverage-analyzer/references/treelint-patterns.md"
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
# Test 2: Line count check (<= 500 lines)
# -----------------------------------------------------------------------------
echo "--- Test 2: File Line Count ---"
line_count=$(wc -l < "$TARGET_FILE")
echo "  Info: Current line count = ${line_count}"

if [[ "$line_count" -le 500 ]]; then
    pass "coverage-analyzer.md is ${line_count} lines (<= 500 limit)"
else
    fail "coverage-analyzer.md is ${line_count} lines (exceeds 500-line limit)"
    # If over 500, reference file MUST exist
    echo ""
    echo "--- Test 2b: Reference File Required (>500 lines) ---"
    if [[ -r "$REFERENCE_FILE" ]]; then
        pass "Reference file exists (required since core exceeds 500 lines)"
    else
        fail "Reference file missing at references/treelint-patterns.md (required since core exceeds 500 lines)"
    fi
fi
echo ""

# -----------------------------------------------------------------------------
# Test 3: Core file contains Read() for treelint reference
# -----------------------------------------------------------------------------
echo "--- Test 3: Read() Instruction for Treelint Reference ---"
if grep -qE 'Read\(.*treelint' "$TARGET_FILE" 2>/dev/null; then
    pass "coverage-analyzer.md contains Read() instruction for Treelint reference"
else
    fail "Missing Read() instruction for Treelint reference file in coverage-analyzer.md"
fi
echo ""

# -----------------------------------------------------------------------------
# Test 4: Treelint content present in either core or reference file
# -----------------------------------------------------------------------------
echo "--- Test 4: Treelint Content Present ---"
treelint_found=false
if grep -qiE 'treelint' "$TARGET_FILE" 2>/dev/null; then
    treelint_found=true
fi
if [[ -r "$REFERENCE_FILE" ]] && grep -qiE 'treelint' "$REFERENCE_FILE" 2>/dev/null; then
    treelint_found=true
fi
if [[ -r "$SHARED_REF" ]] && grep -qiE 'treelint' "$SHARED_REF" 2>/dev/null; then
    treelint_found=true
fi

if $treelint_found; then
    pass "Treelint content found in coverage-analyzer ecosystem"
else
    fail "No Treelint content found (STORY-368 implementation not yet applied)"
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
