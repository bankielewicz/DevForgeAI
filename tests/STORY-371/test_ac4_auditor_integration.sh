#!/usr/bin/env bash
# =============================================================================
# STORY-371 AC#4: Integration with code-quality-auditor Workflow
# =============================================================================
# Validates that code-quality-auditor.md documents:
#   1. Treelint version check (treelint --version >= v0.12.0)
#   2. Treelint as primary source for function length and nesting depth
#   3. Supplementing (not replacing) language-specific tools (radon, eslint)
#   4. Combined results under metrics key
#   5. Language extension mapping for supported files (.py, .ts, .js, .rs)
#   6. Treelint integration section or phase in workflow
#
# TDD Phase: RED - Target file does not contain Treelint integration workflow.
# =============================================================================

set -euo pipefail

PROJECT_ROOT="${PROJECT_ROOT:-/mnt/c/Projects/DevForgeAI2}"
TARGET_FILE="${PROJECT_ROOT}/src/claude/agents/code-quality-auditor.md"

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
echo "  AC#4: Auditor Workflow Integration"
echo "=============================================="
echo ""

# -----------------------------------------------------------------------------
# Test 1: Target file exists
# -----------------------------------------------------------------------------
echo "--- Test 1: File Existence ---"
if [[ -r "$TARGET_FILE" ]]; then
    pass "code-quality-auditor.md exists"
else
    fail "code-quality-auditor.md not found"
    echo ""
    echo "=============================================="
    echo "  AC#4 Results: ${PASS_COUNT} passed, ${FAIL_COUNT} failed (${TOTAL_COUNT} total)"
    echo "=============================================="
    echo "  STATUS: FAILED"
    exit 1
fi
echo ""

# -----------------------------------------------------------------------------
# Test 2: Documents Treelint version check (v0.12.0+)
# -----------------------------------------------------------------------------
echo "--- Test 2: Treelint Version Check ---"
if grep -qE 'treelint.*--version|version.*v0\.12\.0|v0\.12\.0.*check|treelint.*version.*check' "$TARGET_FILE" 2>/dev/null; then
    pass "Documents Treelint version check (v0.12.0+)"
else
    fail "Missing Treelint version check (v0.12.0+)"
fi
echo ""

# -----------------------------------------------------------------------------
# Test 3: Treelint as primary source for metrics
# -----------------------------------------------------------------------------
echo "--- Test 3: Treelint as Primary Source ---"
if grep -qiE 'treelint.*primary|primary.*source.*treelint|treelint.*first' "$TARGET_FILE" 2>/dev/null; then
    pass "Documents Treelint as primary metrics source"
else
    fail "Missing Treelint as primary metrics source documentation"
fi
echo ""

# -----------------------------------------------------------------------------
# Test 4: Supplements (not replaces) language-specific tools
# -----------------------------------------------------------------------------
echo "--- Test 4: Supplement Not Replace ---"
if grep -qiE 'supplement|not.*replac|alongside|in addition|combined.*with' "$TARGET_FILE" 2>/dev/null; then
    pass "Documents supplementing (not replacing) language-specific tools"
else
    fail "Missing supplement/not-replace documentation for language tools"
fi
echo ""

# -----------------------------------------------------------------------------
# Test 5: Language extension mapping (.py, .ts, .js, .rs)
# -----------------------------------------------------------------------------
echo "--- Test 5: Language Extension Mapping ---"
ext_found=0
for ext in ".py" ".ts" ".js" ".rs"; do
    if grep -q "$ext" "$TARGET_FILE" 2>/dev/null; then
        ext_found=$((ext_found + 1))
    fi
done

if [[ "$ext_found" -ge 4 ]]; then
    pass "Documents all 4 supported extensions: .py, .ts, .js, .rs"
else
    fail "Only ${ext_found}/4 supported extensions documented"
fi
echo ""

# -----------------------------------------------------------------------------
# Test 6: Treelint integration section/phase in workflow
# -----------------------------------------------------------------------------
echo "--- Test 6: Treelint Integration Section ---"
if grep -qiE '^#{1,4}.*[Tt]reelint.*[Ii]ntegration|^#{1,4}.*[Tt]reelint.*[Mm]etrics|^#{1,4}.*AST.*[Mm]etrics' "$TARGET_FILE" 2>/dev/null; then
    pass "Contains Treelint integration section heading"
else
    fail "Missing Treelint integration section heading"
fi
echo ""

# -----------------------------------------------------------------------------
# Test 7: Combined results documentation
# -----------------------------------------------------------------------------
echo "--- Test 7: Combined Results Documentation ---"
if grep -qiE 'combined.*result|metrics.*key|merge.*result|both.*source' "$TARGET_FILE" 2>/dev/null; then
    pass "Documents combined results from Treelint + language tools"
else
    fail "Missing combined results documentation"
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
