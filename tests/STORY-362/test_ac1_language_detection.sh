#!/usr/bin/env bash
# =============================================================================
# STORY-362 AC#1: Language Support Detection via File Extension Checking
# =============================================================================
# Validates that treelint-search-patterns.md:
#   1. Contains a supported extensions list with exactly 7 extensions
#      (.py, .ts, .tsx, .js, .jsx, .rs, .md)
#   2. Extension check is the FIRST step in the Fallback Decision Tree
#   3. Unsupported extensions route to Grep (not Treelint)
#   4. Supported extensions match tech-stack.md lines 139-147 (BR-004)
#
# TDD Phase: RED - Tests expected to FAIL until implementation complete.
# =============================================================================

set -euo pipefail

PROJECT_ROOT="${PROJECT_ROOT:-/mnt/c/Projects/DevForgeAI2}"
TARGET_FILE="${PROJECT_ROOT}/src/claude/agents/references/treelint-search-patterns.md"
TECH_STACK="${PROJECT_ROOT}/devforgeai/specs/context/tech-stack.md"

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
echo "  AC#1: Language Support Detection"
echo "=============================================="
echo ""

# -----------------------------------------------------------------------------
# Test 1: Target file exists
# -----------------------------------------------------------------------------
echo "--- Test 1: File Existence ---"
if [[ -r "$TARGET_FILE" ]]; then
    pass "Reference file exists"
else
    fail "Reference file does not exist at src/claude/agents/references/treelint-search-patterns.md"
    echo ""
    echo "=============================================="
    echo "  AC#1 Results: ${PASS_COUNT} passed, ${FAIL_COUNT} failed (${TOTAL_COUNT} total)"
    echo "=============================================="
    echo "  STATUS: FAILED (file does not exist - RED phase expected)"
    exit 1
fi
echo ""

# -----------------------------------------------------------------------------
# Test 2: Contains all 7 supported extensions
# Each of .py, .ts, .tsx, .js, .jsx, .rs, .md must appear
# -----------------------------------------------------------------------------
echo "--- Test 2: Seven Supported Extensions Present ---"
extensions_found=0
for ext in ".py" ".ts" ".tsx" ".js" ".jsx" ".rs" ".md"; do
    # Use backtick-delimited search to match exact extension in markdown/code
    if grep -qF "$ext" "$TARGET_FILE" 2>/dev/null; then
        extensions_found=$((extensions_found + 1))
    fi
done

if [[ "$extensions_found" -eq 7 ]]; then
    pass "All 7 supported extensions found (.py, .ts, .tsx, .js, .jsx, .rs, .md)"
else
    fail "Only ${extensions_found}/7 supported extensions found"
fi
echo ""

# -----------------------------------------------------------------------------
# Test 3: Extension check is Step 1 in Decision Tree
# The story requires extension checking to be the FIRST gate
# -----------------------------------------------------------------------------
echo "--- Test 3: Extension Check Is First Step ---"
if grep -qiE 'Step 1.*((check|verify|evaluate).*(extension|file type)|extension.*(check|first))' "$TARGET_FILE" 2>/dev/null; then
    pass "Extension check documented as Step 1 in decision tree"
else
    fail "Extension check not documented as Step 1 (must be first gate per AC#1)"
fi
echo ""

# -----------------------------------------------------------------------------
# Test 4: Unsupported extensions listed with Grep fallback strategy
# Must have at least 4 unsupported language rows
# -----------------------------------------------------------------------------
echo "--- Test 4: Unsupported Extensions With Grep Strategy ---"
unsupported_count=0
for lang in ".cs" ".java" ".go" ".rb" ".php"; do
    if grep -qF "$lang" "$TARGET_FILE" 2>/dev/null; then
        unsupported_count=$((unsupported_count + 1))
    fi
done

if [[ "$unsupported_count" -ge 4 ]]; then
    pass "At least 4 unsupported extensions documented (found ${unsupported_count})"
else
    fail "Only ${unsupported_count} unsupported extensions documented (>= 4 required)"
fi
echo ""

# -----------------------------------------------------------------------------
# Test 5: Wildcard/catch-all row for unlisted extensions
# Must have a catch-all that defaults to Grep
# -----------------------------------------------------------------------------
echo "--- Test 5: Catch-All Default Row ---"
if grep -qiE '(other|\*|catch.?all|default|unlisted)' "$TARGET_FILE" 2>/dev/null; then
    pass "Catch-all/wildcard row present for unlisted extensions"
else
    fail "Missing catch-all row for extensions not in supported or unsupported list"
fi
echo ""

# -----------------------------------------------------------------------------
# Test 6: Supported list matches tech-stack.md (BR-004 cross-reference)
# Verify tech-stack.md also lists these 7 extensions
# -----------------------------------------------------------------------------
echo "--- Test 6: Cross-Reference With tech-stack.md (BR-004) ---"
if [[ -r "$TECH_STACK" ]]; then
    tech_match=0
    for ext in ".py" ".ts" ".tsx" ".js" ".jsx" ".rs" ".md"; do
        if grep -qF "$ext" "$TECH_STACK" 2>/dev/null; then
            tech_match=$((tech_match + 1))
        fi
    done
    if [[ "$tech_match" -ge 7 ]]; then
        pass "All 7 extensions also present in tech-stack.md"
    else
        fail "Only ${tech_match}/7 extensions found in tech-stack.md (BR-004 parity required)"
    fi
else
    fail "tech-stack.md not readable for BR-004 cross-reference"
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
