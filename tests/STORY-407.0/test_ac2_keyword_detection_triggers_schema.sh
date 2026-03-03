#!/usr/bin/env bash
# =============================================================================
# STORY-407 AC#2: Treelint Keyword Detection Triggers Schema Loading
# =============================================================================
# Validates that story-requirements-analyst.md contains:
#   1. All 6 Treelint keywords for detection
#   2. Word-boundary matching for AST (\bAST\b)
#   3. Schema loading instruction (Read of treelint-search-patterns.md)
#   4. Case-insensitive keyword matching for "treelint"
#   5. Reference to the canonical schema source file
#
# Target: src/claude/agents/story-requirements-analyst.md
# TDD Phase: RED - Tests expected to FAIL until implementation complete.
# =============================================================================

set -euo pipefail

PROJECT_ROOT="${PROJECT_ROOT:-/mnt/c/Projects/DevForgeAI2}"
TARGET_FILE="${PROJECT_ROOT}/src/claude/agents/story-requirements-analyst.md"

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
echo "  AC#2: Treelint Keyword Detection Triggers Schema Loading"
echo "=============================================="
echo ""

# -----------------------------------------------------------------------------
# Test 1: Target file exists
# -----------------------------------------------------------------------------
echo "--- Test 1: File Existence ---"
if [[ -r "$TARGET_FILE" ]]; then
    pass "story-requirements-analyst.md exists and is readable"
else
    fail "story-requirements-analyst.md not found"
    echo ""
    echo "=============================================="
    echo "  AC#2 Results: ${PASS_COUNT} passed, ${FAIL_COUNT} failed (${TOTAL_COUNT} total)"
    echo "=============================================="
    echo "  STATUS: FAILED"
    exit 1
fi
echo ""

# -----------------------------------------------------------------------------
# Test 2: Contains keyword "treelint" in detection list
# -----------------------------------------------------------------------------
echo "--- Test 2: Keyword 'treelint' Listed ---"
if grep -qiE '(keyword|detect|trigger)' "$TARGET_FILE" && grep -qi 'treelint' "$TARGET_FILE"; then
    # More specific: check that "treelint" appears as a keyword item (in a list or backticks)
    if grep -qE '`treelint`|[- ] treelint' "$TARGET_FILE"; then
        pass "Keyword 'treelint' listed in detection keywords"
    else
        fail "Keyword 'treelint' not listed as a detectable keyword (expected in backticks or list)"
    fi
else
    fail "Missing keyword detection logic or 'treelint' keyword"
fi
echo ""

# -----------------------------------------------------------------------------
# Test 3: Contains keyword "AST" with word boundary
# -----------------------------------------------------------------------------
echo "--- Test 3: Keyword 'AST' with Word Boundary ---"
if grep -qE '\\bAST\\b|\\\\bAST\\\\b|word.bound.*AST|AST.*word.bound' "$TARGET_FILE"; then
    pass "Keyword 'AST' listed with word-boundary matching"
else
    fail "Missing 'AST' keyword with word-boundary matching (\\bAST\\b)"
fi
echo ""

# -----------------------------------------------------------------------------
# Test 4: Contains keyword "dependency graph"
# -----------------------------------------------------------------------------
echo "--- Test 4: Keyword 'dependency graph' ---"
if grep -qi 'dependency graph' "$TARGET_FILE"; then
    pass "Keyword 'dependency graph' listed"
else
    fail "Missing keyword 'dependency graph'"
fi
echo ""

# -----------------------------------------------------------------------------
# Test 5: Contains keyword "function signatures"
# -----------------------------------------------------------------------------
echo "--- Test 5: Keyword 'function signatures' ---"
if grep -qi 'function signatures' "$TARGET_FILE"; then
    pass "Keyword 'function signatures' listed"
else
    fail "Missing keyword 'function signatures'"
fi
echo ""

# -----------------------------------------------------------------------------
# Test 6: Contains keyword "syntax tree"
# -----------------------------------------------------------------------------
echo "--- Test 6: Keyword 'syntax tree' ---"
if grep -qi 'syntax tree' "$TARGET_FILE"; then
    pass "Keyword 'syntax tree' listed"
else
    fail "Missing keyword 'syntax tree'"
fi
echo ""

# -----------------------------------------------------------------------------
# Test 7: Contains keyword "code search"
# -----------------------------------------------------------------------------
echo "--- Test 7: Keyword 'code search' ---"
if grep -qi 'code search' "$TARGET_FILE"; then
    pass "Keyword 'code search' listed"
else
    fail "Missing keyword 'code search'"
fi
echo ""

# -----------------------------------------------------------------------------
# Test 8: Case-insensitive matching specified for treelint keyword
# -----------------------------------------------------------------------------
echo "--- Test 8: Case-Insensitive Matching Specified ---"
if grep -qiE 'case.insensitive|case.insensitive|[Cc]ase.[Ii]nsensitive' "$TARGET_FILE"; then
    pass "Case-insensitive matching specified for keyword detection"
else
    fail "Missing case-insensitive matching specification for keyword detection"
fi
echo ""

# -----------------------------------------------------------------------------
# Test 9: Schema loading instruction references correct file
# -----------------------------------------------------------------------------
echo "--- Test 9: Schema Loading References treelint-search-patterns.md ---"
if grep -qE 'Read\(.*treelint-search-patterns' "$TARGET_FILE" || grep -qE 'treelint-search-patterns\.md' "$TARGET_FILE"; then
    pass "Schema loading references treelint-search-patterns.md"
else
    fail "Missing schema loading instruction for treelint-search-patterns.md"
fi
echo ""

# -----------------------------------------------------------------------------
# Test 10: All 6 keywords documented (count check)
# -----------------------------------------------------------------------------
echo "--- Test 10: All 6 Keywords Documented ---"
keyword_count=0
grep -qi 'treelint' "$TARGET_FILE" && grep -qiE '`treelint`|[- ] treelint' "$TARGET_FILE" && keyword_count=$((keyword_count + 1))
grep -qE '\\bAST\\b|\\\\bAST\\\\b|`AST`' "$TARGET_FILE" && keyword_count=$((keyword_count + 1))
grep -qi 'dependency graph' "$TARGET_FILE" && keyword_count=$((keyword_count + 1))
grep -qi 'function signatures' "$TARGET_FILE" && keyword_count=$((keyword_count + 1))
grep -qi 'syntax tree' "$TARGET_FILE" && keyword_count=$((keyword_count + 1))
grep -qi 'code search' "$TARGET_FILE" && keyword_count=$((keyword_count + 1))

if [[ "$keyword_count" -ge 6 ]]; then
    pass "All 6 Treelint detection keywords documented (found ${keyword_count})"
else
    fail "Only ${keyword_count}/6 Treelint keywords documented"
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
