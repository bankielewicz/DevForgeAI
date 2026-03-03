#!/usr/bin/env bash
# =============================================================================
# STORY-360 AC#1: All 6 Context Files Pass Syntax Validation
# =============================================================================
# Validates that all 6 context files:
#   1. Exist and are readable
#   2. Contain required header structure (Status, Last Updated, Version)
#   3. Have valid markdown structure (no broken headers, no empty files)
#   4. Have zero CRITICAL or HIGH violations
#
# TDD Phase: RED - These tests define expected structure for context files.
# =============================================================================

set -euo pipefail

PROJECT_ROOT="${PROJECT_ROOT:-/mnt/c/Projects/DevForgeAI2}"
CONTEXT_DIR="${PROJECT_ROOT}/devforgeai/specs/context"

PASS_COUNT=0
FAIL_COUNT=0
TOTAL_COUNT=0

# List of all 6 context files
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

echo "=============================================="
echo "  AC#1: Syntax Validation - All 6 Context Files"
echo "=============================================="
echo ""

# -----------------------------------------------------------------------------
# Test 1: All 6 context files exist and are readable
# -----------------------------------------------------------------------------
echo "--- Test 1: File Existence ---"
for file in "${CONTEXT_FILES[@]}"; do
    filepath="${CONTEXT_DIR}/${file}"
    if [[ -r "$filepath" ]]; then
        pass "${file} exists and is readable"
    else
        fail "${file} does not exist or is not readable at ${filepath}"
    fi
done
echo ""

# -----------------------------------------------------------------------------
# Test 2: All files are non-empty
# -----------------------------------------------------------------------------
echo "--- Test 2: Non-Empty Files ---"
for file in "${CONTEXT_FILES[@]}"; do
    filepath="${CONTEXT_DIR}/${file}"
    if [[ -s "$filepath" ]]; then
        pass "${file} is non-empty"
    else
        fail "${file} is empty (zero bytes)"
    fi
done
echo ""

# -----------------------------------------------------------------------------
# Test 3: All files contain the required 3 header fields
#   - **Status**: LOCKED
#   - **Last Updated**: YYYY-MM-DD
#   - **Version**: X.Y
# These must appear within the first 10 lines.
# -----------------------------------------------------------------------------
echo "--- Test 3: Required Header Fields (first 10 lines) ---"
for file in "${CONTEXT_FILES[@]}"; do
    filepath="${CONTEXT_DIR}/${file}"
    header=$(head -n 10 "$filepath" 2>/dev/null || echo "")

    # Check Status field
    if echo "$header" | grep -qE '^\*\*Status\*\*:'; then
        pass "${file} has Status field in header"
    else
        fail "${file} missing Status field in first 10 lines"
    fi

    # Check Last Updated field
    if echo "$header" | grep -qE '^\*\*Last Updated\*\*:.*[0-9]{4}-[0-9]{2}-[0-9]{2}'; then
        pass "${file} has Last Updated field with date"
    else
        fail "${file} missing or malformed Last Updated field in first 10 lines"
    fi

    # Check Version field
    if echo "$header" | grep -qE '^\*\*Version\*\*:.*[0-9]+\.[0-9]+'; then
        pass "${file} has Version field with X.Y format"
    else
        fail "${file} missing or malformed Version field in first 10 lines"
    fi
done
echo ""

# -----------------------------------------------------------------------------
# Test 4: All files start with a markdown H1 heading (# Title)
# -----------------------------------------------------------------------------
echo "--- Test 4: H1 Heading Present ---"
for file in "${CONTEXT_FILES[@]}"; do
    filepath="${CONTEXT_DIR}/${file}"
    if head -n 5 "$filepath" 2>/dev/null | grep -qE '^# '; then
        pass "${file} has H1 heading"
    else
        fail "${file} missing H1 heading in first 5 lines"
    fi
done
echo ""

# -----------------------------------------------------------------------------
# Test 5: No broken markdown headers (## with no space after ##)
# This is a CRITICAL syntax violation.
# -----------------------------------------------------------------------------
echo "--- Test 5: No Broken Markdown Headers ---"
for file in "${CONTEXT_FILES[@]}"; do
    filepath="${CONTEXT_DIR}/${file}"
    # Find lines starting with ## but without space after (broken header)
    broken_count=$(grep -cE '^#{2,6}[^ #]' "$filepath" 2>/dev/null | tr -d '\r\n' || echo "0")
    if [[ -z "$broken_count" ]]; then broken_count=0; fi
    if [[ "$broken_count" -eq 0 ]]; then
        pass "${file} has no broken markdown headers"
    else
        fail "${file} has ${broken_count} broken markdown header(s) (## without space)"
    fi
done
echo ""

# -----------------------------------------------------------------------------
# Test 6: No CRITICAL violations - files must not contain TODO/FIXME/HACK markers
# in the header section (first 10 lines). These would indicate incomplete edits.
# -----------------------------------------------------------------------------
echo "--- Test 6: No CRITICAL Markers in Header ---"
for file in "${CONTEXT_FILES[@]}"; do
    filepath="${CONTEXT_DIR}/${file}"
    header=$(head -n 10 "$filepath" 2>/dev/null || echo "")
    if echo "$header" | grep -qiE '(TODO|FIXME|HACK|BROKEN|PLACEHOLDER)'; then
        fail "${file} has CRITICAL marker (TODO/FIXME/HACK) in header section"
    else
        pass "${file} has no CRITICAL markers in header"
    fi
done
echo ""

# -----------------------------------------------------------------------------
# Test 7: Exactly 6 context files exist in the directory (no extras, no missing)
# -----------------------------------------------------------------------------
echo "--- Test 7: Exactly 6 Context Files ---"
actual_count=$(ls -1 "${CONTEXT_DIR}"/*.md 2>/dev/null | wc -l)
if [[ "$actual_count" -eq 6 ]]; then
    pass "Exactly 6 context files found in ${CONTEXT_DIR}"
else
    fail "Expected 6 context files, found ${actual_count} in ${CONTEXT_DIR}"
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
