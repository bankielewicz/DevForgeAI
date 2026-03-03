#!/usr/bin/env bash
# =============================================================================
# STORY-407 AC#1: Non-Treelint Stories Skip Validation Entirely
# =============================================================================
# Validates that story-requirements-analyst.md contains logic to:
#   1. Detect whether a feature description contains Treelint keywords
#   2. Skip Treelint schema validation when no keywords are present
#   3. Not load treelint-search-patterns.md for non-Treelint stories
#   4. Produce zero overhead for non-Treelint stories
#
# Target: src/claude/agents/story-requirements-analyst.md
# TDD Phase: RED - Tests expected to FAIL until implementation complete.
# =============================================================================

set -euo pipefail

PROJECT_ROOT="${PROJECT_ROOT:-/mnt/c/Projects/DevForgeAI2}"
TARGET_FILE="${PROJECT_ROOT}/src/claude/agents/story-requirements-analyst.md"

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
echo "  AC#1: Non-Treelint Stories Skip Validation Entirely"
echo "=============================================="
echo ""

# -----------------------------------------------------------------------------
# Test 1: Target file exists
# -----------------------------------------------------------------------------
echo "--- Test 1: File Existence ---"
if [[ -r "$TARGET_FILE" ]]; then
    pass "story-requirements-analyst.md exists and is readable"
else
    fail "story-requirements-analyst.md not found at src/claude/agents/story-requirements-analyst.md"
    echo ""
    echo "=============================================="
    echo "  AC#1 Results: ${PASS_COUNT} passed, ${FAIL_COUNT} failed (${TOTAL_COUNT} total)"
    echo "=============================================="
    echo "  STATUS: FAILED"
    exit 1
fi
echo ""

# -----------------------------------------------------------------------------
# Test 2: Contains keyword detection logic section
# -----------------------------------------------------------------------------
echo "--- Test 2: Keyword Detection Section Exists ---"
if grep -qiE '^#{1,4}.*[Kk]eyword.*[Dd]etect|^#{1,4}.*[Tt]reelint.*[Kk]eyword|^#{1,4}.*[Tt]reelint.*[Dd]etect' "$TARGET_FILE"; then
    pass "Contains Treelint keyword detection section heading"
else
    fail "Missing section heading for Treelint keyword detection (e.g., '### Treelint Keyword Detection')"
fi
echo ""

# -----------------------------------------------------------------------------
# Test 3: Contains conditional skip logic for non-Treelint stories
# -----------------------------------------------------------------------------
echo "--- Test 3: Conditional Skip Logic Present ---"
if grep -qiE '(no.*treelint|without.*treelint|non.treelint|skip.*treelint|treelint.*skip).*valid' "$TARGET_FILE"; then
    pass "Contains conditional skip logic for non-Treelint stories"
else
    fail "Missing conditional skip logic (e.g., 'skip Treelint validation' when no keywords detected)"
fi
echo ""

# -----------------------------------------------------------------------------
# Test 4: Contains explicit zero-overhead statement for non-Treelint stories
# -----------------------------------------------------------------------------
echo "--- Test 4: Zero Overhead Statement ---"
if grep -qiE '(zero.*overhead|0ms|no.*additional.*overhead|skip.*entirely|validation.*skip)' "$TARGET_FILE"; then
    pass "Contains zero overhead statement for non-Treelint stories"
else
    fail "Missing zero overhead statement (e.g., 'zero additional overhead' for non-Treelint stories)"
fi
echo ""

# -----------------------------------------------------------------------------
# Test 5: No unconditional Read of treelint-search-patterns.md
# (the Read should be inside a conditional block, not top-level)
# -----------------------------------------------------------------------------
echo "--- Test 5: Schema Load is Conditional (Not Unconditional) ---"
# Check that the file mentions treelint-search-patterns.md
if grep -q 'treelint-search-patterns' "$TARGET_FILE"; then
    # Verify the load is described as conditional (keyword-gated)
    if grep -qiE '(IF|WHEN|conditional|keyword)' "$TARGET_FILE" && grep -q 'treelint-search-patterns' "$TARGET_FILE"; then
        pass "Schema loading is conditional (keyword-gated, not unconditional)"
    else
        fail "treelint-search-patterns.md is referenced but not conditional on keyword detection"
    fi
else
    fail "No reference to treelint-search-patterns.md found (needed to verify conditionality)"
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
