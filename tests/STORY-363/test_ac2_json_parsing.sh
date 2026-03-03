#!/usr/bin/env bash
# =============================================================================
# STORY-363 AC#2: JSON Parsing of Treelint Search Results
# =============================================================================
# Validates that test-automator.md contains JSON parsing instructions
# referencing all 4 required fields: name, file, lines, signature
#
# TDD Phase: RED - Tests expected to FAIL until implementation complete.
# =============================================================================

set -euo pipefail

PROJECT_ROOT="${PROJECT_ROOT:-/mnt/c/Projects/DevForgeAI2}"
TARGET_FILE="${PROJECT_ROOT}/src/claude/agents/test-automator.md"

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
echo "  AC#2: JSON Parsing of Treelint Search Results"
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
    echo "  AC#2 Results: ${PASS_COUNT} passed, ${FAIL_COUNT} failed (${TOTAL_COUNT} total)"
    echo "=============================================="
    echo "  STATUS: FAILED"
    exit 1
fi
echo ""

# -----------------------------------------------------------------------------
# Test 2: References 'name' field in JSON parsing context
# -----------------------------------------------------------------------------
echo "--- Test 2: JSON Field 'name' Referenced ---"
if grep -qiE '(name|function.?name)' "$TARGET_FILE" 2>/dev/null && \
   grep -qiE '(JSON|parse|field|result)' "$TARGET_FILE" 2>/dev/null && \
   grep -qiE '`name`|"name"|\bname\b.*field' "$TARGET_FILE" 2>/dev/null; then
    pass "JSON field 'name' referenced in parsing instructions"
else
    fail "JSON field 'name' not found in Treelint parsing instructions"
fi
echo ""

# -----------------------------------------------------------------------------
# Test 3: References 'file' field in JSON parsing context
# -----------------------------------------------------------------------------
echo "--- Test 3: JSON Field 'file' Referenced ---"
if grep -qiE '`file`|"file"|\bfile\b.*field|file.*path' "$TARGET_FILE" 2>/dev/null; then
    pass "JSON field 'file' referenced in parsing instructions"
else
    fail "JSON field 'file' not found in Treelint parsing instructions"
fi
echo ""

# -----------------------------------------------------------------------------
# Test 4: References 'lines' field in JSON parsing context
# -----------------------------------------------------------------------------
echo "--- Test 4: JSON Field 'lines' Referenced ---"
if grep -qiE '`lines`|"lines"|\blines\b.*\[|line.*range' "$TARGET_FILE" 2>/dev/null; then
    pass "JSON field 'lines' referenced in parsing instructions"
else
    fail "JSON field 'lines' not found in Treelint parsing instructions"
fi
echo ""

# -----------------------------------------------------------------------------
# Test 5: References 'signature' field in JSON parsing context
# -----------------------------------------------------------------------------
echo "--- Test 5: JSON Field 'signature' Referenced ---"
if grep -qiE '`signature`|"signature"|signature.*field|function.*signature' "$TARGET_FILE" 2>/dev/null; then
    pass "JSON field 'signature' referenced in parsing instructions"
else
    fail "JSON field 'signature' not found in Treelint parsing instructions"
fi
echo ""

# -----------------------------------------------------------------------------
# Test 6: All 4 fields appear together or in same section
# A composite check that all 4 field names appear in the file
# -----------------------------------------------------------------------------
echo "--- Test 6: All 4 Required Fields Present ---"
field_count=0
for field in "name" "file" "lines" "signature"; do
    if grep -qw "$field" "$TARGET_FILE" 2>/dev/null; then
        field_count=$((field_count + 1))
    fi
done

if [[ "$field_count" -eq 4 ]]; then
    pass "All 4 required JSON fields (name, file, lines, signature) present"
else
    fail "Only ${field_count}/4 required JSON fields found (need: name, file, lines, signature)"
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
