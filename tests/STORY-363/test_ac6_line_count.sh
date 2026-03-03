#!/usr/bin/env bash
# =============================================================================
# STORY-363 AC#6: Progressive Disclosure Compliance (500-Line Limit)
# =============================================================================
# Validates that:
#   1. test-automator.md file is <= 500 lines
#   2. If >500 lines, a reference file exists at
#      src/claude/agents/test-automator/references/treelint-patterns.md
#   3. If reference file exists, test-automator.md contains Read() for it
#
# TDD Phase: RED - Tests expected to FAIL until implementation complete.
# =============================================================================

set -euo pipefail

PROJECT_ROOT="${PROJECT_ROOT:-/mnt/c/Projects/DevForgeAI2}"
TARGET_FILE="${PROJECT_ROOT}/src/claude/agents/test-automator.md"
REFERENCE_FILE="${PROJECT_ROOT}/src/claude/agents/test-automator/references/treelint-patterns.md"

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
    pass "test-automator.md exists and is readable"
else
    fail "test-automator.md not found"
    echo ""
    echo "=============================================="
    echo "  AC#6 Results: ${PASS_COUNT} passed, ${FAIL_COUNT} failed (${TOTAL_COUNT} total)"
    echo "=============================================="
    echo "  STATUS: FAILED"
    exit 1
fi
echo ""

# -----------------------------------------------------------------------------
# Test 2: Line count <= 500
# -----------------------------------------------------------------------------
echo "--- Test 2: Line Count Check ---"
line_count=$(wc -l < "$TARGET_FILE")
echo "  Info: Current line count = ${line_count}"

if [[ "$line_count" -le 500 ]]; then
    pass "File is ${line_count} lines (<= 500 limit)"
else
    fail "File is ${line_count} lines (exceeds 500 limit)"
fi
echo ""

# -----------------------------------------------------------------------------
# Test 3: If >500 lines, reference file must exist
# -----------------------------------------------------------------------------
echo "--- Test 3: Reference File Existence (Conditional) ---"
if [[ "$line_count" -gt 500 ]]; then
    if [[ -r "$REFERENCE_FILE" ]]; then
        pass "Reference file exists at references/treelint-patterns.md (required since file >500 lines)"
    else
        fail "File exceeds 500 lines but reference file missing at src/claude/agents/test-automator/references/treelint-patterns.md"
    fi
else
    pass "File is within 500-line limit; reference file optional (skipping conditional check)"
fi
echo ""

# -----------------------------------------------------------------------------
# Test 4: If reference file exists, test-automator.md must have Read() for it
# -----------------------------------------------------------------------------
echo "--- Test 4: Read() Instruction for Reference File (Conditional) ---"
if [[ -r "$REFERENCE_FILE" ]]; then
    if grep -qE 'Read\(.*treelint-patterns' "$TARGET_FILE" 2>/dev/null; then
        pass "test-automator.md contains Read() instruction for treelint-patterns.md"
    else
        fail "Reference file exists but test-automator.md lacks Read() instruction for it"
    fi
else
    pass "Reference file does not exist; Read() instruction check skipped"
fi
echo ""

# -----------------------------------------------------------------------------
# Test 5: Treelint content exists (proves AC#6 is testable)
# At least one Treelint-related keyword must be in the file after implementation
# -----------------------------------------------------------------------------
echo "--- Test 5: Treelint Content Present ---"
if grep -qiE 'treelint' "$TARGET_FILE" 2>/dev/null; then
    pass "Treelint content found in test-automator.md"
else
    fail "No Treelint content found (STORY-363 implementation not yet applied)"
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
