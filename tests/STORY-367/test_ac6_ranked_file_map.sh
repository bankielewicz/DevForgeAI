#!/usr/bin/env bash
# =============================================================================
# STORY-367 AC#6: Ranked File Map for Refactoring Prioritization
# =============================================================================
# Validates that refactoring-specialist.md (or its reference file) contains:
#   1. treelint map --ranked --format json command documented
#   2. JSON parsing for ranked results documented
#   3. File prioritization by symbol density / complexity
#   4. Integration into Step 1 (Detect Code Smells) workflow
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

search_files() {
    local files="$TARGET_FILE"
    if [[ -r "$REFERENCE_FILE" ]]; then
        files="$TARGET_FILE $REFERENCE_FILE"
    fi
    echo "$files"
}

echo "=============================================="
echo "  AC#6: Ranked File Map for Refactoring Prioritization"
echo "=============================================="
echo ""

# -----------------------------------------------------------------------------
# Test 1: Target file exists
# -----------------------------------------------------------------------------
echo "--- Test 1: File Existence ---"
if [[ -r "$TARGET_FILE" ]]; then
    pass "refactoring-specialist.md exists and is readable"
else
    fail "refactoring-specialist.md not found"
    echo ""
    echo "=============================================="
    echo "  AC#6 Results: ${PASS_COUNT} passed, ${FAIL_COUNT} failed (${TOTAL_COUNT} total)"
    echo "=============================================="
    echo "  STATUS: FAILED"
    exit 1
fi
echo ""

# -----------------------------------------------------------------------------
# Test 2: Contains treelint map --ranked command
# -----------------------------------------------------------------------------
echo "--- Test 2: Treelint Map Ranked Command ---"
if grep -q 'treelint map.*--ranked' $(search_files) 2>/dev/null; then
    pass "Contains 'treelint map --ranked' command"
else
    fail "Missing 'treelint map --ranked' command"
fi
echo ""

# -----------------------------------------------------------------------------
# Test 3: Contains --format json with treelint map --ranked
# -----------------------------------------------------------------------------
echo "--- Test 3: JSON Format with Ranked Map ---"
if grep -q 'treelint map.*--ranked.*--format json' $(search_files) 2>/dev/null; then
    pass "Contains '--format json' flag with treelint map --ranked"
else
    fail "Missing '--format json' flag in treelint map --ranked instruction"
fi
echo ""

# -----------------------------------------------------------------------------
# Test 4: File prioritization / ranking concept documented
# -----------------------------------------------------------------------------
echo "--- Test 4: File Prioritization Documentation ---"
if grep -qiE 'prioriti[sz].*file|rank.*file|file.*rank|highest.*symbol|symbol.*density|most.*complex' $(search_files) 2>/dev/null; then
    pass "File prioritization by complexity/density documented"
else
    fail "Missing file prioritization documentation for ranked map results"
fi
echo ""

# -----------------------------------------------------------------------------
# Test 5: Uses Bash() tool for treelint map invocation
# -----------------------------------------------------------------------------
echo "--- Test 5: Bash Tool for Treelint Map ---"
if grep -qE 'Bash\(.*treelint map' $(search_files) 2>/dev/null; then
    pass "Uses Bash() tool for treelint map invocation"
else
    fail "Missing Bash() tool usage for treelint map invocation"
fi
echo ""

# -----------------------------------------------------------------------------
# Test 6: Integration with refactoring workflow (Step 1 or code smell detection)
# -----------------------------------------------------------------------------
echo "--- Test 6: Workflow Integration ---"
if grep -qiE 'Detect Code Smell|Step 1|refactoring.*priori|priori.*refactoring|highest.*impact|impactful.*file' $(search_files) 2>/dev/null; then
    pass "Ranked map integrated into refactoring workflow"
else
    fail "Missing integration of ranked map into refactoring workflow (Step 1: Detect Code Smells)"
fi
echo ""

# =============================================================================
# Summary
# =============================================================================
echo "=============================================="
echo "  AC#6 Results: ${PASS_COUNT} passed, ${FAIL_COUNT} failed (${TOTAL_COUNT} total)"
echo "=============================================="

if [[ "$FAIL_COUNT" -gt 0 ]]; then
    echo "  STATUS: FAILED"
    exit 1
else
    echo "  STATUS: PASSED"
    exit 0
fi
