#!/usr/bin/env bash
# =============================================================================
# STORY-365 AC#5: Implementation Pattern Discovery via Treelint
# =============================================================================
# Validates that backend-architect.md (or its reference file) contains:
#   1. Pattern discovery instructions using Treelint
#   2. Interface/class pattern search examples
#   3. Targeted Read() from Treelint results for implementation analysis
#   4. Integration with Phase 3 (Design Solution) workflow
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
echo "  AC#5: Implementation Pattern Discovery"
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
    echo "  AC#5 Results: ${PASS_COUNT} passed, ${FAIL_COUNT} failed (${TOTAL_COUNT} total)"
    echo "=============================================="
    echo "  STATUS: FAILED"
    exit 1
fi
echo ""

# -----------------------------------------------------------------------------
# Test 2: Pattern discovery section heading
# -----------------------------------------------------------------------------
echo "--- Test 2: Pattern Discovery Section Heading ---"
if grep -qiE '^#{1,4}.*(pattern|implementation).*([Dd]iscover|[Tt]reelint)|^#{1,4}.*[Tt]reelint.*(pattern|implementation)' $(search_files) 2>/dev/null; then
    pass "Pattern discovery section heading found"
else
    fail "Missing section heading for implementation pattern discovery via Treelint"
fi
echo ""

# -----------------------------------------------------------------------------
# Test 3: Uses Treelint to discover class/interface patterns
# -----------------------------------------------------------------------------
echo "--- Test 3: Treelint Class/Interface Pattern Search ---"
if grep -qiE 'treelint.*class.*pattern|treelint.*Repository|treelint.*Service|treelint.*interface' $(search_files) 2>/dev/null; then
    pass "Treelint used for class/interface pattern discovery"
else
    fail "Missing Treelint usage for class/interface pattern discovery"
fi
echo ""

# -----------------------------------------------------------------------------
# Test 4: Uses Read() with line ranges from Treelint results
# -----------------------------------------------------------------------------
echo "--- Test 4: Targeted Read() from Treelint Results ---"
if grep -qiE 'Read\(.*line|line.*range.*Read|targeted.*Read|Read.*offset' $(search_files) 2>/dev/null; then
    pass "Targeted Read() operations using Treelint line ranges documented"
else
    fail "Missing targeted Read() operations from Treelint line range results"
fi
echo ""

# -----------------------------------------------------------------------------
# Test 5: References Phase 3 (Design Solution) workflow context
# -----------------------------------------------------------------------------
echo "--- Test 5: Phase 3 / Design Solution Context ---"
if grep -qiE 'Phase 3|Design Solution|design.*pattern|layer.*placement' $(search_files) 2>/dev/null; then
    pass "References Phase 3 / Design Solution workflow context"
else
    fail "Missing Phase 3 / Design Solution workflow context for pattern discovery"
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
