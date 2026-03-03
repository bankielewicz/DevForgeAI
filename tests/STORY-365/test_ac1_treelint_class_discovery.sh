#!/usr/bin/env bash
# =============================================================================
# STORY-365 AC#1: Treelint Integration for Class Discovery
# =============================================================================
# Validates that backend-architect.md (or its reference file) contains:
#   1. A treelint search --type class --format json instruction
#   2. The instruction uses Bash() tool for Treelint invocation
#   3. A section heading for Treelint-aware class discovery
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

# Determine search files: core file + reference file if it exists
search_files() {
    local files="$TARGET_FILE"
    if [[ -r "$REFERENCE_FILE" ]]; then
        files="$TARGET_FILE $REFERENCE_FILE"
    fi
    echo "$files"
}

echo "=============================================="
echo "  AC#1: Treelint Integration for Class Discovery"
echo "=============================================="
echo ""

# -----------------------------------------------------------------------------
# Test 1: Target file exists
# -----------------------------------------------------------------------------
echo "--- Test 1: File Existence ---"
if [[ -r "$TARGET_FILE" ]]; then
    pass "backend-architect.md exists and is readable"
else
    fail "backend-architect.md not found at src/claude/agents/backend-architect.md"
    echo ""
    echo "=============================================="
    echo "  AC#1 Results: ${PASS_COUNT} passed, ${FAIL_COUNT} failed (${TOTAL_COUNT} total)"
    echo "=============================================="
    echo "  STATUS: FAILED"
    exit 1
fi
echo ""

# -----------------------------------------------------------------------------
# Test 2: Contains treelint search --type class command
# -----------------------------------------------------------------------------
echo "--- Test 2: Treelint Class Search Command Present ---"
if grep -q 'treelint search.*--type class' $(search_files) 2>/dev/null; then
    pass "Contains 'treelint search --type class' instruction"
else
    fail "Missing 'treelint search --type class' instruction"
fi
echo ""

# -----------------------------------------------------------------------------
# Test 3: Contains --format json flag for class search
# -----------------------------------------------------------------------------
echo "--- Test 3: JSON Format Flag with Class Search ---"
if grep -q 'treelint search.*--type class.*--format json' $(search_files) 2>/dev/null; then
    pass "Contains '--format json' flag with class search"
else
    fail "Missing '--format json' flag in treelint class search instruction"
fi
echo ""

# -----------------------------------------------------------------------------
# Test 4: Uses Bash() tool for Treelint class invocation
# -----------------------------------------------------------------------------
echo "--- Test 4: Bash Tool Usage for Treelint Class Search ---"
if grep -qE 'Bash\(.*treelint.*class' $(search_files) 2>/dev/null; then
    pass "Uses Bash() tool for Treelint class invocation"
else
    fail "Missing Bash() tool usage for Treelint class search"
fi
echo ""

# -----------------------------------------------------------------------------
# Test 5: Section heading for Treelint class discovery
# -----------------------------------------------------------------------------
echo "--- Test 5: Treelint Class Discovery Section Heading ---"
if grep -qiE '^#{1,4}.*[Tt]reelint.*[Cc]lass.*[Dd]iscovery' $(search_files) 2>/dev/null; then
    pass "Treelint class discovery section heading found"
else
    fail "Missing section heading for Treelint class discovery (e.g., '### Treelint-Aware Class Discovery')"
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
