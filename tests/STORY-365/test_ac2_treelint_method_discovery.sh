#!/usr/bin/env bash
# =============================================================================
# STORY-365 AC#2: Treelint Integration for Method/Function Discovery
# =============================================================================
# Validates that backend-architect.md (or its reference file) contains:
#   1. A treelint search --type function --format json instruction
#   2. The instruction uses Bash() tool for Treelint invocation
#   3. A section heading for Treelint method/function discovery
#
# TDD Phase: RED - Tests expected to FAIL until implementation complete.
# =============================================================================

set -euo pipefail

PROJECT_ROOT="${PROJECT_ROOT:-/mnt/c/Projects/DevForgeAI2}"
TARGET_FILE="${PROJECT_ROOT}/src/claude/agents/backend-architect.md"
REFERENCE_FILE="${PROJECT_ROOT}/src/claude/agents/backend-architect/references/treelint-patterns.md"

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

search_files() {
    local files="$TARGET_FILE"
    if [[ -r "$REFERENCE_FILE" ]]; then
        files="$TARGET_FILE $REFERENCE_FILE"
    fi
    echo "$files"
}

echo "=============================================="
echo "  AC#2: Treelint Method/Function Discovery"
echo "=============================================="
echo ""

# -----------------------------------------------------------------------------
# Test 1: Target file exists
# -----------------------------------------------------------------------------
echo "--- Test 1: File Existence ---"
if [[ -r "$TARGET_FILE" ]]; then
    pass "backend-architect.md exists and is readable"
else
    fail "backend-architect.md not found"
    echo ""
    echo "=============================================="
    echo "  AC#2 Results: ${PASS_COUNT} passed, ${FAIL_COUNT} failed (${TOTAL_COUNT} total)"
    echo "=============================================="
    echo "  STATUS: FAILED"
    exit 1
fi
echo ""

# -----------------------------------------------------------------------------
# Test 2: Contains treelint search --type function command
# -----------------------------------------------------------------------------
echo "--- Test 2: Treelint Function Search Command Present ---"
if grep -q 'treelint search.*--type function' $(search_files) 2>/dev/null; then
    pass "Contains 'treelint search --type function' instruction"
else
    fail "Missing 'treelint search --type function' instruction"
fi
echo ""

# -----------------------------------------------------------------------------
# Test 3: Contains --format json flag for function search
# -----------------------------------------------------------------------------
echo "--- Test 3: JSON Format Flag with Function Search ---"
if grep -q 'treelint search.*--type function.*--format json' $(search_files) 2>/dev/null; then
    pass "Contains '--format json' flag with function search"
else
    fail "Missing '--format json' flag in treelint function search instruction"
fi
echo ""

# -----------------------------------------------------------------------------
# Test 4: Uses Bash() tool for Treelint function invocation
# -----------------------------------------------------------------------------
echo "--- Test 4: Bash Tool Usage for Treelint Function Search ---"
if grep -qE 'Bash\(.*treelint.*function' $(search_files) 2>/dev/null; then
    pass "Uses Bash() tool for Treelint function invocation"
else
    fail "Missing Bash() tool usage for Treelint function search"
fi
echo ""

# -----------------------------------------------------------------------------
# Test 5: Section heading for Treelint method/function discovery
# -----------------------------------------------------------------------------
echo "--- Test 5: Treelint Method Discovery Section Heading ---"
if grep -qiE '^#{1,4}.*[Tt]reelint.*([Mm]ethod|[Ff]unction).*[Dd]iscovery' $(search_files) 2>/dev/null; then
    pass "Treelint method/function discovery section heading found"
else
    fail "Missing section heading for Treelint method discovery (e.g., '### Treelint-Aware Method Discovery')"
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
