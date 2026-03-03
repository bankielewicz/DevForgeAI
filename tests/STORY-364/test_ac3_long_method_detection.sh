#!/usr/bin/env bash
# =============================================================================
# STORY-364 AC#3: Long Method Detection Using Treelint AST Search
# =============================================================================
# Validates that the reference file contains:
#   1. treelint search --type function command pattern
#   2. --format json flag on the function search command
#   3. A threshold of 50 lines for long method detection (BR-003)
#   4. Line calculation formula: lines[1] - lines[0]
#   5. Reporting fields: function name, file path, line count, start/end lines
#
# TDD Phase: RED - Tests expected to FAIL until implementation complete.
# =============================================================================

set -euo pipefail

PROJECT_ROOT="${PROJECT_ROOT:-/mnt/c/Projects/DevForgeAI2}"
REFERENCE_FILE="${PROJECT_ROOT}/src/claude/agents/code-reviewer/references/treelint-review-patterns.md"

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
echo "  AC#3: Long Method Detection via Treelint"
echo "=============================================="
echo ""

# -----------------------------------------------------------------------------
# Test 1: Reference file exists
# -----------------------------------------------------------------------------
echo "--- Test 1: File Existence ---"
if [[ -r "$REFERENCE_FILE" ]]; then
    pass "treelint-review-patterns.md exists and is readable"
else
    fail "treelint-review-patterns.md not found"
    echo ""
    echo "=============================================="
    echo "  AC#3 Results: ${PASS_COUNT} passed, ${FAIL_COUNT} failed (${TOTAL_COUNT} total)"
    echo "=============================================="
    echo "  STATUS: FAILED"
    exit 1
fi
echo ""

# -----------------------------------------------------------------------------
# Test 2: Contains treelint search --type function command
# -----------------------------------------------------------------------------
echo "--- Test 2: Treelint Function Search Command ---"
if grep -q 'treelint search.*--type function' "$REFERENCE_FILE" 2>/dev/null; then
    pass "Contains 'treelint search --type function' command pattern"
else
    fail "Missing 'treelint search --type function' command pattern"
fi
echo ""

# -----------------------------------------------------------------------------
# Test 3: Function search includes --format json flag
# -----------------------------------------------------------------------------
echo "--- Test 3: JSON Format Flag on Function Search ---"
if grep -E 'treelint search.*--type function' "$REFERENCE_FILE" 2>/dev/null | grep -q '\-\-format json'; then
    pass "Function search command includes --format json flag"
else
    fail "Function search command missing --format json flag"
fi
echo ""

# -----------------------------------------------------------------------------
# Test 4: Contains 50-line threshold for long methods (BR-003)
# BR-003: Long method threshold is >50 lines per function
# -----------------------------------------------------------------------------
echo "--- Test 4: 50-Line Threshold (BR-003) ---"
if grep -qE '(>?\s*50\s*line|line.*50|50.*line|threshold.*50|50.*threshold)' "$REFERENCE_FILE" 2>/dev/null; then
    pass "Contains 50-line threshold for long method detection"
else
    fail "Missing 50-line threshold documentation (BR-003 requires >50 lines)"
fi
echo ""

# -----------------------------------------------------------------------------
# Test 5: Documents line calculation formula (lines[1] - lines[0])
# The AC specifies calculating function length from lines[1] minus lines[0]
# -----------------------------------------------------------------------------
echo "--- Test 5: Line Calculation Formula ---"
if grep -qE '(lines\[1\].*lines\[0\]|end.*start|lines\.1.*lines\.0|line_count|length.*calculation)' "$REFERENCE_FILE" 2>/dev/null; then
    pass "Documents line length calculation formula"
else
    fail "Missing line length calculation formula (should document lines[1] - lines[0] or equivalent)"
fi
echo ""

# -----------------------------------------------------------------------------
# Test 6: Documents required reporting fields for long methods
# Must include: function name, file path, actual line count, start/end lines
# -----------------------------------------------------------------------------
echo "--- Test 6: Required Reporting Fields ---"
field_count=0

if grep -qiE '(function\s*name|name.*field|\"name\")' "$REFERENCE_FILE" 2>/dev/null; then
    field_count=$((field_count + 1))
fi

if grep -qiE '(file\s*path|\"file\"|file.*field)' "$REFERENCE_FILE" 2>/dev/null; then
    field_count=$((field_count + 1))
fi

if grep -qiE '(line\s*count|actual.*lines|function.*length)' "$REFERENCE_FILE" 2>/dev/null; then
    field_count=$((field_count + 1))
fi

if grep -qiE '(start.*end|line.*range|\"lines\"|lines.*field)' "$REFERENCE_FILE" 2>/dev/null; then
    field_count=$((field_count + 1))
fi

if [[ "$field_count" -ge 3 ]]; then
    pass "Documents ${field_count}/4 required reporting fields (name, file, line count, range)"
else
    fail "Only ${field_count}/4 required reporting fields documented (need name, file, line count, range)"
fi
echo ""

# =============================================================================
# Summary
# =============================================================================
echo "=============================================="
echo "  AC#3 Results: ${PASS_COUNT} passed, ${FAIL_COUNT} failed (${TOTAL_COUNT} total)"
echo "=============================================="

if [[ "$FAIL_COUNT" -gt 0 ]]; then
    echo "  STATUS: FAILED"
    exit 1
else
    echo "  STATUS: PASSED"
    exit 0
fi
