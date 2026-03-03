#!/usr/bin/env bash
# =============================================================================
# STORY-363 AC#1: Treelint Integration for Function Discovery
# =============================================================================
# Validates that test-automator.md contains:
#   1. A treelint search --type function --format json instruction
#   2. The instruction uses Bash() tool for Treelint invocation
#   3. A section heading for Treelint-aware function discovery
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
echo "  AC#1: Treelint Integration for Function Discovery"
echo "=============================================="
echo ""

# -----------------------------------------------------------------------------
# Test 1: Target file exists
# -----------------------------------------------------------------------------
echo "--- Test 1: File Existence ---"
if [[ -r "$TARGET_FILE" ]]; then
    pass "test-automator.md exists and is readable"
else
    fail "test-automator.md not found at src/claude/agents/test-automator.md"
    echo ""
    echo "=============================================="
    echo "  AC#1 Results: ${PASS_COUNT} passed, ${FAIL_COUNT} failed (${TOTAL_COUNT} total)"
    echo "=============================================="
    echo "  STATUS: FAILED"
    exit 1
fi
echo ""

# -----------------------------------------------------------------------------
# Test 2: Contains treelint search --type function command
# -----------------------------------------------------------------------------
echo "--- Test 2: Treelint Search Command Present ---"
if grep -q 'treelint search.*--type function' "$TARGET_FILE" 2>/dev/null; then
    pass "Contains 'treelint search --type function' instruction"
else
    fail "Missing 'treelint search --type function' instruction"
fi
echo ""

# -----------------------------------------------------------------------------
# Test 3: Contains --format json flag
# -----------------------------------------------------------------------------
echo "--- Test 3: JSON Format Flag Present ---"
if grep -q '\-\-format json' "$TARGET_FILE" 2>/dev/null; then
    pass "Contains '--format json' flag"
else
    fail "Missing '--format json' flag in treelint search instruction"
fi
echo ""

# -----------------------------------------------------------------------------
# Test 4: Uses Bash() tool for Treelint invocation
# -----------------------------------------------------------------------------
echo "--- Test 4: Bash Tool Usage for Treelint ---"
if grep -qE 'Bash\(.*treelint' "$TARGET_FILE" 2>/dev/null; then
    pass "Uses Bash() tool for Treelint invocation"
else
    fail "Missing Bash() tool usage for Treelint (should use Bash(command=\"treelint ...\"))"
fi
echo ""

# -----------------------------------------------------------------------------
# Test 5: Section heading for Treelint function discovery
# -----------------------------------------------------------------------------
echo "--- Test 5: Treelint Section Heading ---"
if grep -qiE '^#{1,4}.*[Tt]reelint.*([Ff]unction|[Dd]iscovery)' "$TARGET_FILE" 2>/dev/null; then
    pass "Treelint function discovery section heading found"
else
    fail "Missing section heading for Treelint function discovery (e.g., '### Treelint-Aware Function Discovery')"
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
