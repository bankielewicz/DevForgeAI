#!/usr/bin/env bash
# =============================================================================
# STORY-367 AC#5: Progressive Disclosure Compliance (500-Line Limit)
# =============================================================================
# Validates that:
#   1. refactoring-specialist.md core file is <= 500 lines
#   2. Reference file exists at references/treelint-refactoring-patterns.md
#   3. Core file contains Read() instruction pointing to reference file
#   4. Core file contains Read() instruction for STORY-361 shared reference
#
# TDD Phase: RED - Tests expected to FAIL until implementation complete.
# Current file is 595 lines (exceeds 500-line limit).
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

echo "=============================================="
echo "  AC#5: Progressive Disclosure Compliance"
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
    echo "  AC#5 Results: ${PASS_COUNT} passed, ${FAIL_COUNT} failed (${TOTAL_COUNT} total)"
    echo "=============================================="
    echo "  STATUS: FAILED"
    exit 1
fi
echo ""

# -----------------------------------------------------------------------------
# Test 2: Core file is <= 500 lines (BR-004)
# -----------------------------------------------------------------------------
echo "--- Test 2: Core File Line Count <= 500 ---"
LINE_COUNT=$(wc -l < "$TARGET_FILE")
if [[ "$LINE_COUNT" -le 500 ]]; then
    pass "refactoring-specialist.md is ${LINE_COUNT} lines (<= 500 limit)"
else
    fail "refactoring-specialist.md is ${LINE_COUNT} lines (exceeds 500-line limit per tech-stack.md)"
fi
echo ""

# -----------------------------------------------------------------------------
# Test 3: Reference file exists
# -----------------------------------------------------------------------------
echo "--- Test 3: Reference File Existence ---"
if [[ -r "$REFERENCE_FILE" ]]; then
    pass "treelint-refactoring-patterns.md reference file exists"
else
    fail "Missing reference file at src/claude/agents/refactoring-specialist/references/treelint-refactoring-patterns.md"
fi
echo ""

# -----------------------------------------------------------------------------
# Test 4: Core file contains Read() instruction for treelint-refactoring-patterns.md
# -----------------------------------------------------------------------------
echo "--- Test 4: Read() Instruction for Reference File ---"
if grep -qE 'Read\(.*treelint-refactoring-patterns' "$TARGET_FILE" 2>/dev/null; then
    pass "Core file contains Read() instruction for treelint-refactoring-patterns.md"
else
    fail "Missing Read() instruction for treelint-refactoring-patterns.md in core file"
fi
echo ""

# -----------------------------------------------------------------------------
# Test 5: Core file contains Read() instruction for STORY-361 shared reference
# -----------------------------------------------------------------------------
echo "--- Test 5: Read() Instruction for Shared Treelint Patterns ---"
if grep -qE 'Read\(.*treelint.*patterns' "$TARGET_FILE" 2>/dev/null; then
    pass "Core file contains Read() instruction for shared Treelint patterns reference"
else
    fail "Missing Read() instruction for shared Treelint patterns reference file"
fi
echo ""

# -----------------------------------------------------------------------------
# Test 6: Reference directory structure follows ADR-012 pattern
# -----------------------------------------------------------------------------
echo "--- Test 6: ADR-012 Directory Structure ---"
REF_DIR="${PROJECT_ROOT}/src/claude/agents/refactoring-specialist/references"
if [[ -d "$REF_DIR" ]]; then
    pass "Reference directory follows ADR-012 progressive disclosure pattern"
else
    fail "Missing references/ directory at src/claude/agents/refactoring-specialist/references/"
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
