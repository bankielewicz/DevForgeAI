#!/usr/bin/env bash
# =============================================================================
# STORY-367 AC#1: Treelint Integration for Code Structure Analysis
# =============================================================================
# Validates that refactoring-specialist.md (or its reference file) contains:
#   1. A treelint search --type class --format json instruction
#   2. A treelint search --type function --format json instruction
#   3. The instructions use Bash() tool for Treelint invocation
#   4. A section heading for Treelint-aware code structure analysis
#
# TDD Phase: RED - Tests expected to FAIL until implementation complete.
# =============================================================================

set -euo pipefail

PROJECT_ROOT="${PROJECT_ROOT:-/mnt/c/Projects/DevForgeAI2}"
TARGET_FILE="${PROJECT_ROOT}/src/claude/agents/refactoring-specialist.md"
REFERENCE_FILE="${PROJECT_ROOT}/src/claude/agents/refactoring-specialist/references/treelint-refactoring-patterns.md"

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
echo "  AC#1: Treelint Integration for Code Structure Analysis"
echo "=============================================="
echo ""

# -----------------------------------------------------------------------------
# Test 1: Target file exists
# -----------------------------------------------------------------------------
echo "--- Test 1: File Existence ---"
if [[ -r "$TARGET_FILE" ]]; then
    pass "refactoring-specialist.md exists and is readable"
else
    fail "refactoring-specialist.md not found at src/claude/agents/refactoring-specialist.md"
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
# Test 3: Contains treelint search --type function command
# -----------------------------------------------------------------------------
echo "--- Test 3: Treelint Function Search Command Present ---"
if grep -q 'treelint search.*--type function' $(search_files) 2>/dev/null; then
    pass "Contains 'treelint search --type function' instruction"
else
    fail "Missing 'treelint search --type function' instruction"
fi
echo ""

# -----------------------------------------------------------------------------
# Test 4: Contains --format json flag for class search
# -----------------------------------------------------------------------------
echo "--- Test 4: JSON Format Flag with Class Search ---"
if grep -q 'treelint search.*--type class.*--format json' $(search_files) 2>/dev/null; then
    pass "Contains '--format json' flag with class search"
else
    fail "Missing '--format json' flag in treelint class search instruction"
fi
echo ""

# -----------------------------------------------------------------------------
# Test 5: Contains --format json flag for function search
# -----------------------------------------------------------------------------
echo "--- Test 5: JSON Format Flag with Function Search ---"
if grep -q 'treelint search.*--type function.*--format json' $(search_files) 2>/dev/null; then
    pass "Contains '--format json' flag with function search"
else
    fail "Missing '--format json' flag in treelint function search instruction"
fi
echo ""

# -----------------------------------------------------------------------------
# Test 6: Uses Bash() tool for Treelint invocation
# -----------------------------------------------------------------------------
echo "--- Test 6: Bash Tool Usage for Treelint Invocation ---"
if grep -qE 'Bash\(.*treelint' $(search_files) 2>/dev/null; then
    pass "Uses Bash() tool for Treelint invocation"
else
    fail "Missing Bash() tool usage for Treelint invocation"
fi
echo ""

# -----------------------------------------------------------------------------
# Test 7: Section heading for Treelint code structure analysis
# -----------------------------------------------------------------------------
echo "--- Test 7: Treelint Code Structure Analysis Section Heading ---"
if grep -qiE '^#{1,4}.*[Tt]reelint.*([Ss]tructure|[Cc]ode|[Aa]nalysis|[Rr]efactor)' $(search_files) 2>/dev/null; then
    pass "Treelint code structure analysis section heading found"
else
    fail "Missing section heading for Treelint code structure analysis (e.g., '### Treelint-Aware Code Structure Analysis')"
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
