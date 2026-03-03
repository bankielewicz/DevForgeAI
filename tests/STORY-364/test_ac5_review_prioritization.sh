#!/usr/bin/env bash
# =============================================================================
# STORY-364 AC#5: Review Prioritization Using Treelint Map Command
# =============================================================================
# Validates that the reference file contains:
#   1. treelint map --ranked command pattern
#   2. --format json flag on the map command
#   3. Bash() tool usage for map invocation
#   4. Prioritization logic (high-ranked = deep review, low-ranked = lighter review)
#   5. Documentation of prioritization rationale in review report
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
echo "  AC#5: Review Prioritization via Treelint Map"
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
    echo "  AC#5 Results: ${PASS_COUNT} passed, ${FAIL_COUNT} failed (${TOTAL_COUNT} total)"
    echo "=============================================="
    echo "  STATUS: FAILED"
    exit 1
fi
echo ""

# -----------------------------------------------------------------------------
# Test 2: Contains treelint map --ranked command
# -----------------------------------------------------------------------------
echo "--- Test 2: Treelint Map Ranked Command ---"
if grep -q 'treelint map.*--ranked' "$REFERENCE_FILE" 2>/dev/null; then
    pass "Contains 'treelint map --ranked' command pattern"
else
    fail "Missing 'treelint map --ranked' command pattern"
fi
echo ""

# -----------------------------------------------------------------------------
# Test 3: Map command includes --format json flag
# -----------------------------------------------------------------------------
echo "--- Test 3: JSON Format Flag on Map Command ---"
if grep -E 'treelint map.*--ranked' "$REFERENCE_FILE" 2>/dev/null | grep -q '\-\-format json'; then
    pass "Map command includes --format json flag"
else
    fail "Map command missing --format json flag"
fi
echo ""

# -----------------------------------------------------------------------------
# Test 4: Uses Bash() tool for map invocation
# -----------------------------------------------------------------------------
echo "--- Test 4: Bash Tool Usage ---"
if grep -qE 'Bash\(.*treelint map' "$REFERENCE_FILE" 2>/dev/null; then
    pass "Uses Bash() tool for Treelint map invocation"
else
    fail "Missing Bash() tool usage for map command (should use Bash(command=\"treelint map ...\"))"
fi
echo ""

# -----------------------------------------------------------------------------
# Test 5: Documents prioritization logic (high vs low ranking)
# Must describe how file ranking affects review depth
# -----------------------------------------------------------------------------
echo "--- Test 5: Prioritization Logic ---"
if grep -qiE '(high.*rank|prioriti[sz]|deep.*review|light.*review|rank.*file|important)' "$REFERENCE_FILE" 2>/dev/null; then
    pass "Documents review prioritization logic based on file ranking"
else
    fail "Missing prioritization logic documentation (high-ranked = deep review, low-ranked = light review)"
fi
echo ""

# -----------------------------------------------------------------------------
# Test 6: Documents rationale in review report
# Must instruct documenting WHY files were prioritized in the review output
# -----------------------------------------------------------------------------
echo "--- Test 6: Prioritization Rationale Documentation ---"
if grep -qiE '(rationale|document.*priorit|explain.*rank|review.*report|report.*priorit)' "$REFERENCE_FILE" 2>/dev/null; then
    pass "Documents prioritization rationale requirement in review report"
else
    fail "Missing documentation for including prioritization rationale in review report"
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
