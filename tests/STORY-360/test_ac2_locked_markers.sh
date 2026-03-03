#!/usr/bin/env bash
# =============================================================================
# STORY-360 AC#2: LOCKED Markers Remain Intact in All Files
# =============================================================================
# Validates that each of the 6 context files contains exactly one
# **Status**: LOCKED marker within the first 10 lines, and no file has
# the marker removed, altered, or relocated.
#
# TDD Phase: RED - These tests define expected LOCKED marker behavior.
# =============================================================================

set -euo pipefail

PROJECT_ROOT="${PROJECT_ROOT:-/mnt/c/Projects/DevForgeAI2}"
CONTEXT_DIR="${PROJECT_ROOT}/devforgeai/specs/context"

PASS_COUNT=0
FAIL_COUNT=0
TOTAL_COUNT=0

CONTEXT_FILES=(
    "tech-stack.md"
    "source-tree.md"
    "dependencies.md"
    "coding-standards.md"
    "architecture-constraints.md"
    "anti-patterns.md"
)

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

# WSL-safe grep count: strips carriage returns from grep -c output
gcount() {
    local result
    result=$(grep -c "$@" 2>/dev/null | tr -d '\r\n' || true)
    if [[ -z "$result" ]]; then echo "0"; else echo "$result"; fi
}

gcountF() {
    local result
    result=$(grep -cF "$@" 2>/dev/null | tr -d '\r\n' || true)
    if [[ -z "$result" ]]; then echo "0"; else echo "$result"; fi
}

echo "=============================================="
echo "  AC#2: LOCKED Markers Intact in All Files"
echo "=============================================="
echo ""

# -----------------------------------------------------------------------------
# Test 1: Each file contains **Status**: LOCKED within the first 10 lines
# -----------------------------------------------------------------------------
echo "--- Test 1: LOCKED Marker in First 10 Lines ---"
for file in "${CONTEXT_FILES[@]}"; do
    filepath="${CONTEXT_DIR}/${file}"
    header=$(head -n 10 "$filepath" 2>/dev/null || echo "")

    if echo "$header" | grep -qF '**Status**: LOCKED'; then
        pass "${file} has **Status**: LOCKED in first 10 lines"
    else
        fail "${file} is MISSING **Status**: LOCKED in first 10 lines (CRITICAL)"
    fi
done
echo ""

# -----------------------------------------------------------------------------
# Test 2: Each file has EXACTLY ONE **Status**: LOCKED marker in first 10 lines
# Note: Some files (e.g., tech-stack.md) use **Status**: LOCKED for subsection
# markers later in the file. The AC requires exactly one in the HEADER (first 10 lines).
# -----------------------------------------------------------------------------
echo "--- Test 2: Exactly One LOCKED Marker in Header (first 10 lines) ---"
for file in "${CONTEXT_FILES[@]}"; do
    filepath="${CONTEXT_DIR}/${file}"
    header=$(head -n 10 "$filepath" 2>/dev/null || echo "")
    lock_count=$(echo "$header" | grep -cF '**Status**: LOCKED' 2>/dev/null | tr -d '\r\n' || true)
    if [[ -z "$lock_count" ]]; then lock_count=0; fi

    if [[ "$lock_count" -eq 1 ]]; then
        pass "${file} has exactly 1 LOCKED marker in header"
    elif [[ "$lock_count" -eq 0 ]]; then
        fail "${file} has NO LOCKED marker in header (removed)"
    else
        fail "${file} has ${lock_count} LOCKED markers in header (duplicated)"
    fi
done
echo ""

# -----------------------------------------------------------------------------
# Test 3: LOCKED marker text is unaltered (exact match)
# Checks that the marker is not modified to e.g. UNLOCKED, DRAFT, etc.
# -----------------------------------------------------------------------------
echo "--- Test 3: No Altered Status Markers ---"
for file in "${CONTEXT_FILES[@]}"; do
    filepath="${CONTEXT_DIR}/${file}"
    header=$(head -n 10 "$filepath" 2>/dev/null || echo "")

    # Check for any **Status**: line that is NOT LOCKED
    status_lines=$(echo "$header" | grep -E '^\*\*Status\*\*:' || true)
    non_locked=$(echo "$status_lines" | grep -vcF 'LOCKED' 2>/dev/null | tr -d '\r\n' || true)
    if [[ -z "$non_locked" ]]; then non_locked=0; fi

    if [[ "$non_locked" -eq 0 ]]; then
        pass "${file} status marker is unaltered (LOCKED)"
    else
        fail "${file} has an altered status marker (not LOCKED)"
    fi
done
echo ""

# -----------------------------------------------------------------------------
# Test 4: LOCKED marker is not relocated beyond line 10
# (Check if marker exists in entire file but NOT in first 10 lines)
# -----------------------------------------------------------------------------
echo "--- Test 4: LOCKED Marker Not Relocated Beyond Line 10 ---"
for file in "${CONTEXT_FILES[@]}"; do
    filepath="${CONTEXT_DIR}/${file}"
    header=$(head -n 10 "$filepath" 2>/dev/null || echo "")
    full_count=$(gcountF '**Status**: LOCKED' "$filepath")
    if echo "$header" | grep -qF '**Status**: LOCKED'; then
        header_has=1
    else
        header_has=0
    fi

    if [[ "$full_count" -gt 0 && "$header_has" -eq 0 ]]; then
        fail "${file} LOCKED marker found but relocated beyond line 10"
    elif [[ "$full_count" -eq 0 ]]; then
        fail "${file} LOCKED marker completely missing from file"
    else
        pass "${file} LOCKED marker is in correct position (first 10 lines)"
    fi
done
echo ""

# -----------------------------------------------------------------------------
# Test 5: All 6 files have LOCKED status (aggregate check)
# -----------------------------------------------------------------------------
echo "--- Test 5: Aggregate - All 6 Files LOCKED ---"
locked_count=0
for file in "${CONTEXT_FILES[@]}"; do
    filepath="${CONTEXT_DIR}/${file}"
    header=$(head -n 10 "$filepath" 2>/dev/null || echo "")
    if echo "$header" | grep -qF '**Status**: LOCKED'; then
        locked_count=$((locked_count + 1))
    fi
done

if [[ "$locked_count" -eq 6 ]]; then
    pass "All 6 context files have LOCKED status"
else
    fail "Only ${locked_count}/6 context files have LOCKED status"
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
