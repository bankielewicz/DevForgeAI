#!/usr/bin/env bash
# =============================================================================
# STORY-365 AC#4: Grep Fallback for Unsupported Languages
# =============================================================================
# Validates that backend-architect.md (or its reference file) contains:
#   1. Grep fallback section heading
#   2. Native Grep() tool usage (not Bash grep)
#   3. Warning-level messaging on fallback (not HALT)
#   4. Distinction between empty results (exit 0) and command failure (non-zero)
#   5. Treelint section appears before Grep fallback (BR-001)
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
echo "  AC#4: Grep Fallback for Unsupported Languages"
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
    echo "  AC#4 Results: ${PASS_COUNT} passed, ${FAIL_COUNT} failed (${TOTAL_COUNT} total)"
    echo "=============================================="
    echo "  STATUS: FAILED"
    exit 1
fi
echo ""

# -----------------------------------------------------------------------------
# Test 2: Grep fallback section heading exists
# -----------------------------------------------------------------------------
echo "--- Test 2: Grep Fallback Section Heading ---"
if grep -qiE '^#{1,4}.*[Ff]allback.*[Gg]rep|^#{1,4}.*[Gg]rep.*[Ff]allback' $(search_files) 2>/dev/null; then
    pass "Grep fallback section heading found"
else
    fail "Missing Grep fallback section heading (e.g., '### Fallback: Grep for Unsupported Languages')"
fi
echo ""

# -----------------------------------------------------------------------------
# Test 3: Uses native Grep() tool (not Bash grep)
# -----------------------------------------------------------------------------
echo "--- Test 3: Native Grep Tool Usage ---"
if grep -qE 'Grep\(pattern=' $(search_files) 2>/dev/null; then
    pass "Uses native Grep() tool for fallback"
else
    fail "Missing native Grep(pattern=...) tool usage in fallback section"
fi
echo ""

# -----------------------------------------------------------------------------
# Test 4: Warning-level messaging (not HALT on Treelint failure)
# -----------------------------------------------------------------------------
echo "--- Test 4: Warning-Level Messaging ---"
if grep -qiE 'warning.*fallback|fallback.*warning|warning-level|warning.level' $(search_files) 2>/dev/null; then
    pass "Warning-level messaging documented for fallback"
else
    fail "Missing warning-level messaging for Treelint fallback"
fi
echo ""

# -----------------------------------------------------------------------------
# Test 5: Distinguishes empty results from command failure (BR-002)
# -----------------------------------------------------------------------------
echo "--- Test 5: Empty Results vs Command Failure Distinction ---"
if grep -qiE 'exit code 0.*empty|empty.*exit code 0|zero.*match|no match.*valid|empty results.*NOT.*fail' $(search_files) 2>/dev/null; then
    pass "Distinguishes empty results (exit 0) from command failure"
else
    fail "Missing distinction between empty results and command failure (BR-002)"
fi
echo ""

# -----------------------------------------------------------------------------
# Test 6: No HALT on Treelint failure (BR-003)
# -----------------------------------------------------------------------------
echo "--- Test 6: No HALT on Treelint Failure ---"
# Check that fallback context does NOT instruct HALT on Treelint failure
# The word HALT should not appear near Treelint failure context
if grep -qiE 'treelint.*(fail|error).*HALT|HALT.*treelint.*(fail|error)' $(search_files) 2>/dev/null; then
    fail "Contains HALT instruction on Treelint failure (should use fallback, not HALT)"
else
    pass "No HALT instruction on Treelint failure (correct: uses fallback)"
fi
echo ""

# =============================================================================
# Summary
# =============================================================================
echo "=============================================="
echo "  AC#4 Results: ${PASS_COUNT} passed, ${FAIL_COUNT} failed (${TOTAL_COUNT} total)"
echo "=============================================="

if [[ "$FAIL_COUNT" -gt 0 ]]; then
    echo "  STATUS: FAILED"
    exit 1
else
    echo "  STATUS: PASSED"
    exit 0
fi
