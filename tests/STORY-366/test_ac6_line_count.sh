#!/usr/bin/env bash
# =============================================================================
# STORY-366 AC#6: Progressive Disclosure Compliance (500-Line Limit)
# =============================================================================
# Validates that:
#   1. security-auditor.md file line count is <= 500 OR
#      a reference file exists at references/treelint-security-patterns.md
#   2. If >500 lines, reference file MUST exist
#   3. If reference file exists, security-auditor.md MUST contain Read() for it
#   4. Treelint content is present in the file (proves implementation applied)
#
# NOTE: The current security-auditor.md is already 554 lines (over limit).
#       The story notes indicate Treelint patterns MUST go to reference file.
#
# TDD Phase: RED - Tests expected to FAIL until implementation complete.
# =============================================================================

set -euo pipefail

PROJECT_ROOT="${PROJECT_ROOT:-/mnt/c/Projects/DevForgeAI2}"
TARGET_FILE="${PROJECT_ROOT}/src/claude/agents/security-auditor.md"
REFERENCE_FILE="${PROJECT_ROOT}/src/claude/agents/security-auditor/references/treelint-security-patterns.md"

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
    pass "security-auditor.md exists and is readable"
else
    fail "security-auditor.md not found"
    echo ""
    echo "=============================================="
    echo "  AC#6 Results: ${PASS_COUNT} passed, ${FAIL_COUNT} failed (${TOTAL_COUNT} total)"
    echo "=============================================="
    echo "  STATUS: FAILED"
    exit 1
fi
echo ""

# -----------------------------------------------------------------------------
# Test 2: Line count check
# File must be <= 500 lines, OR if >500, reference file must exist
# -----------------------------------------------------------------------------
echo "--- Test 2: Line Count Check ---"
line_count=$(wc -l < "$TARGET_FILE")
echo "  Info: Current line count = ${line_count}"

if [[ "$line_count" -le 500 ]]; then
    pass "File is ${line_count} lines (<= 500 limit)"
else
    # File exceeds 500 lines - reference file MUST exist
    if [[ -r "$REFERENCE_FILE" ]]; then
        pass "File exceeds 500 lines (${line_count}) but reference file exists (progressive disclosure)"
    else
        fail "File is ${line_count} lines (exceeds 500 limit) and no reference file at src/claude/agents/security-auditor/references/treelint-security-patterns.md"
    fi
fi
echo ""

# -----------------------------------------------------------------------------
# Test 3: If >500 lines, reference file must exist
# This is the hard requirement from ADR-012
# -----------------------------------------------------------------------------
echo "--- Test 3: Reference File Existence (Conditional) ---"
if [[ "$line_count" -gt 500 ]]; then
    if [[ -r "$REFERENCE_FILE" ]]; then
        pass "Reference file exists at references/treelint-security-patterns.md (required since file >500 lines)"
    else
        fail "File exceeds 500 lines but reference file missing at src/claude/agents/security-auditor/references/treelint-security-patterns.md"
    fi
else
    pass "File is within 500-line limit; reference file optional (skipping conditional check)"
fi
echo ""

# -----------------------------------------------------------------------------
# Test 4: If reference file exists, security-auditor.md must have Read() for it
# -----------------------------------------------------------------------------
echo "--- Test 4: Read() Instruction for Reference File (Conditional) ---"
if [[ -r "$REFERENCE_FILE" ]]; then
    if grep -qE 'Read\(.*treelint-security-patterns' "$TARGET_FILE" 2>/dev/null; then
        pass "security-auditor.md contains Read() instruction for treelint-security-patterns.md"
    else
        fail "Reference file exists but security-auditor.md lacks Read() instruction for it"
    fi
else
    pass "Reference file does not exist; Read() instruction check skipped"
fi
echo ""

# -----------------------------------------------------------------------------
# Test 5: Treelint content exists (proves implementation was applied)
# At least one Treelint-related keyword must be in the file
# -----------------------------------------------------------------------------
echo "--- Test 5: Treelint Content Present ---"
if grep -qiE 'treelint' "$TARGET_FILE" 2>/dev/null; then
    pass "Treelint content found in security-auditor.md"
else
    fail "No Treelint content found (STORY-366 implementation not yet applied)"
fi
echo ""

# -----------------------------------------------------------------------------
# Test 6: Shared reference file loading (STORY-361)
# Must contain Read() instruction for the shared treelint-search-patterns.md
# -----------------------------------------------------------------------------
echo "--- Test 6: Shared Treelint Reference File Loading ---"
if grep -qE 'Read\(.*treelint.*patterns' "$TARGET_FILE" 2>/dev/null; then
    pass "Contains Read() instruction for shared Treelint reference file"
else
    fail "Missing Read() instruction for shared treelint-search-patterns.md reference (STORY-361 dependency)"
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
