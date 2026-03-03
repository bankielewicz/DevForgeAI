#!/usr/bin/env bash
# =============================================================================
# STORY-364 AC#1: Code-Reviewer Reference File with Treelint Review Patterns
# =============================================================================
# Validates that:
#   1. Reference file exists at src/claude/agents/code-reviewer/references/treelint-review-patterns.md
#   2. Contains God class detection pattern section
#   3. Contains long method detection pattern section
#   4. Contains file prioritization/map pattern section
#   5. code-reviewer.md has Read() instruction pointing to reference file
#   6. Reference file is non-empty and has YAML-compatible frontmatter or heading
#
# TDD Phase: RED - Tests expected to FAIL until implementation complete.
# =============================================================================

set -euo pipefail

PROJECT_ROOT="${PROJECT_ROOT:-/mnt/c/Projects/DevForgeAI2}"
REFERENCE_FILE="${PROJECT_ROOT}/src/claude/agents/code-reviewer/references/treelint-review-patterns.md"
CORE_FILE="${PROJECT_ROOT}/src/claude/agents/code-reviewer.md"

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
echo "  AC#1: Code-Reviewer Reference File Created"
echo "=============================================="
echo ""

# -----------------------------------------------------------------------------
# Test 1: Reference file exists and is readable
# -----------------------------------------------------------------------------
echo "--- Test 1: Reference File Existence ---"
if [[ -r "$REFERENCE_FILE" ]]; then
    pass "treelint-review-patterns.md exists at src/claude/agents/code-reviewer/references/"
else
    fail "treelint-review-patterns.md not found at src/claude/agents/code-reviewer/references/"
    echo ""
    echo "=============================================="
    echo "  AC#1 Results: ${PASS_COUNT} passed, ${FAIL_COUNT} failed (${TOTAL_COUNT} total)"
    echo "=============================================="
    echo "  STATUS: FAILED (file does not exist - RED phase expected)"
    exit 1
fi
echo ""

# -----------------------------------------------------------------------------
# Test 2: Reference file is non-empty
# -----------------------------------------------------------------------------
echo "--- Test 2: Non-Empty File ---"
if [[ -s "$REFERENCE_FILE" ]]; then
    pass "Reference file is non-empty"
else
    fail "Reference file is empty (zero bytes)"
fi
echo ""

# -----------------------------------------------------------------------------
# Test 3: Contains God class detection pattern section
# -----------------------------------------------------------------------------
echo "--- Test 3: God Class Detection Section ---"
if grep -qiE '^#{1,4}.*[Gg]od [Cc]lass' "$REFERENCE_FILE" 2>/dev/null; then
    pass "Contains God class detection section heading"
else
    fail "Missing God class detection section heading (e.g., '### God Class Detection via Treelint')"
fi
echo ""

# -----------------------------------------------------------------------------
# Test 4: Contains long method detection pattern section
# -----------------------------------------------------------------------------
echo "--- Test 4: Long Method Detection Section ---"
if grep -qiE '^#{1,4}.*[Ll]ong [Mm]ethod' "$REFERENCE_FILE" 2>/dev/null; then
    pass "Contains long method detection section heading"
else
    fail "Missing long method detection section heading (e.g., '### Long Method Detection via Treelint')"
fi
echo ""

# -----------------------------------------------------------------------------
# Test 5: Contains file prioritization/review prioritization section
# -----------------------------------------------------------------------------
echo "--- Test 5: File Prioritization Section ---"
if grep -qiE '^#{1,4}.*(prioriti[sz]ation|file.*rank|ranked|map)' "$REFERENCE_FILE" 2>/dev/null; then
    pass "Contains file prioritization/ranking section heading"
else
    fail "Missing file prioritization section heading (e.g., '### Review Prioritization via Treelint Map')"
fi
echo ""

# -----------------------------------------------------------------------------
# Test 6: code-reviewer.md has Read() pointing to reference file
# -----------------------------------------------------------------------------
echo "--- Test 6: Read() Instruction in code-reviewer.md ---"
if [[ -r "$CORE_FILE" ]]; then
    if grep -q 'Read.*treelint-review-patterns' "$CORE_FILE" 2>/dev/null; then
        pass "code-reviewer.md contains Read() instruction for treelint-review-patterns.md"
    else
        fail "code-reviewer.md missing Read() instruction for treelint-review-patterns.md"
    fi
else
    fail "code-reviewer.md not found at src/claude/agents/code-reviewer.md"
fi
echo ""

# -----------------------------------------------------------------------------
# Test 7: code-reviewer.md has Treelint integration section
# -----------------------------------------------------------------------------
echo "--- Test 7: Treelint Section in code-reviewer.md ---"
if [[ -r "$CORE_FILE" ]]; then
    if grep -qiE '^#{1,4}.*(Treelint|AST-[Aa]ware)' "$CORE_FILE" 2>/dev/null; then
        pass "code-reviewer.md contains Treelint integration section heading"
    else
        fail "code-reviewer.md missing Treelint/AST-Aware section heading"
    fi
else
    fail "code-reviewer.md not found (cannot check for Treelint section)"
fi
echo ""

# =============================================================================
# Summary
# =============================================================================
echo "=============================================="
echo "  AC#1 Results: ${PASS_COUNT} passed, ${FAIL_COUNT} failed (${TOTAL_COUNT} total)"
echo "=============================================="

if [[ "$FAIL_COUNT" -gt 0 ]]; then
    echo "  STATUS: FAILED"
    exit 1
else
    echo "  STATUS: PASSED"
    exit 0
fi
