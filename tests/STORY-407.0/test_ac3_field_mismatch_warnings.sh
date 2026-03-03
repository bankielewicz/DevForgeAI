#!/usr/bin/env bash
# =============================================================================
# STORY-407 AC#3: Field Name Mismatches Produce Non-Blocking Warnings
# =============================================================================
# Validates that story-requirements-analyst.md contains:
#   1. Warning format matching the specification pattern
#   2. Non-blocking behavior (continues after warning)
#   3. Closest match suggestion logic
#   4. WARNING severity level (not ERROR, not HALT)
#   5. Individual warning per mismatch
#
# Warning format from spec:
#   WARNING: Story references Treelint field '{field_name}' which does not
#   match canonical schema. Closest match: '{closest_field}'
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
echo "  AC#3: Field Name Mismatches Produce Non-Blocking Warnings"
echo "=============================================="
echo ""

# -----------------------------------------------------------------------------
# Test 1: Target file exists
# -----------------------------------------------------------------------------
echo "--- Test 1: File Existence ---"
if [[ -r "$TARGET_FILE" ]]; then
    pass "story-requirements-analyst.md exists and is readable"
else
    fail "story-requirements-analyst.md not found"
    echo ""
    echo "=============================================="
    echo "  AC#3 Results: ${PASS_COUNT} passed, ${FAIL_COUNT} failed (${TOTAL_COUNT} total)"
    echo "=============================================="
    echo "  STATUS: FAILED"
    exit 1
fi
echo ""

# -----------------------------------------------------------------------------
# Test 2: Contains WARNING format matching specification
# -----------------------------------------------------------------------------
echo "--- Test 2: Warning Format Matches Specification ---"
if grep -qE "WARNING.*[Ss]tory.*[Tt]reelint.*field.*canonical.*schema" "$TARGET_FILE" || \
   grep -qE "WARNING.*field.*does not match.*canonical" "$TARGET_FILE" || \
   grep -qE "WARNING.*[Tt]reelint field.*match" "$TARGET_FILE"; then
    pass "WARNING format matches specification pattern"
else
    fail "Missing WARNING format: 'WARNING: Story references Treelint field ... canonical schema'"
fi
echo ""

# -----------------------------------------------------------------------------
# Test 3: Contains closest match suggestion
# -----------------------------------------------------------------------------
echo "--- Test 3: Closest Match Suggestion ---"
if grep -qiE '[Cc]losest.match|closest_field|[Nn]earest.match|[Ss]uggested.field|[Dd]id.you.mean' "$TARGET_FILE"; then
    pass "Contains closest match suggestion logic"
else
    fail "Missing closest match suggestion (e.g., 'Closest match: {closest_field}')"
fi
echo ""

# -----------------------------------------------------------------------------
# Test 4: Non-blocking behavior (continues after warning)
# -----------------------------------------------------------------------------
echo "--- Test 4: Non-Blocking Behavior ---"
if grep -qiE '(non.blocking|continue.*generat|generation.*continue|do not.*halt|warning.*not.*halt|proceed.*after|does not.*stop)' "$TARGET_FILE"; then
    pass "Non-blocking behavior documented (continues after warning)"
else
    fail "Missing non-blocking behavior statement (warning should not halt generation)"
fi
echo ""

# -----------------------------------------------------------------------------
# Test 5: Uses WARNING severity (not ERROR, not HALT)
# -----------------------------------------------------------------------------
echo "--- Test 5: WARNING Severity Level ---"
# Check that the warning uses WARNING prefix (not ERROR or HALT)
if grep -qE '^WARNING:|`WARNING`|WARNING:' "$TARGET_FILE" || \
   grep -qiE 'severity.*warning|warning.*severity|emit.*warning|produce.*warning' "$TARGET_FILE"; then
    pass "Uses WARNING severity level"
else
    fail "Missing WARNING severity level (should use WARNING, not ERROR or HALT)"
fi
echo ""

# -----------------------------------------------------------------------------
# Test 6: Individual warning per mismatch
# -----------------------------------------------------------------------------
echo "--- Test 6: Individual Warning Per Mismatch ---"
if grep -qiE '(each.*mismatch|individual.*warning|per.*mismatch|each.*field|every.*mismatch)' "$TARGET_FILE"; then
    pass "Individual warning per field mismatch documented"
else
    fail "Missing individual warning per mismatch (each field mismatch should produce a separate warning)"
fi
echo ""

# -----------------------------------------------------------------------------
# Test 7: Contains canonical field set reference
# -----------------------------------------------------------------------------
echo "--- Test 7: Canonical Field Set Referenced ---"
if grep -qiE '(canonical.*field|field.*canonical|valid.*field.*names|canonical.*schema)' "$TARGET_FILE"; then
    pass "Canonical field set referenced"
else
    fail "Missing canonical field set reference (cross-reference against canonical names)"
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
