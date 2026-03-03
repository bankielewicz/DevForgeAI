#!/usr/bin/env bash
# =============================================================================
# STORY-361 AC#2: JSON Output Parsing Examples Documented for AI Consumption
# =============================================================================
# Validates that:
#   1. Reference file exists
#   2. Contains "## JSON Output Parsing" section heading (or similar)
#   3. Contains 3+ JSON code block examples:
#      a. Function search result (with type, name, file, lines, signature fields)
#      b. Class search result with member enumeration
#      c. treelint map --ranked result showing file importance ranking
#   4. Each JSON example has a narrative explanation following it
#
# TDD Phase: RED - Target file does not exist yet.
# =============================================================================

set -euo pipefail

PROJECT_ROOT="${PROJECT_ROOT:-/mnt/c/Projects/DevForgeAI2}"
TARGET_FILE="${PROJECT_ROOT}/src/claude/agents/references/treelint-search-patterns.md"

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
echo "  AC#2: JSON Output Parsing Examples"
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
    echo "  AC#2 Results: ${PASS_COUNT} passed, ${FAIL_COUNT} failed (${TOTAL_COUNT} total)"
    echo "=============================================="
    echo "  STATUS: FAILED (file does not exist - RED phase expected)"
    exit 1
fi
echo ""

# -----------------------------------------------------------------------------
# Test 2: Contains JSON Output Parsing section heading
# -----------------------------------------------------------------------------
echo "--- Test 2: JSON Output Parsing Section ---"
if grep -qE '^#{1,3} .*JSON Output Parsing' "$TARGET_FILE" 2>/dev/null; then
    pass "Contains 'JSON Output Parsing' section heading"
else
    fail "Missing 'JSON Output Parsing' section heading"
fi
echo ""

# -----------------------------------------------------------------------------
# Test 3: Contains at least 3 JSON code blocks
# Count occurrences of ```json opening markers
# -----------------------------------------------------------------------------
echo "--- Test 3: Minimum 3 JSON Code Blocks ---"
json_block_count=$(grep -c '```json' "$TARGET_FILE" 2>/dev/null | tr -d '\r\n' || echo "0")
if [[ -z "$json_block_count" ]]; then json_block_count=0; fi
if [[ "$json_block_count" -ge 3 ]]; then
    pass "Contains ${json_block_count} JSON code blocks (>= 3 required)"
else
    fail "Only ${json_block_count} JSON code blocks found (>= 3 required)"
fi
echo ""

# -----------------------------------------------------------------------------
# Test 4: Function search JSON example
# Must contain fields indicating a function search result
# -----------------------------------------------------------------------------
echo "--- Test 4: Function Search JSON Example ---"
if grep -q '"type".*"function"' "$TARGET_FILE" 2>/dev/null || \
   grep -q '"type": "function"' "$TARGET_FILE" 2>/dev/null; then
    pass "Contains function search JSON example with type: function"
else
    fail "Missing function search JSON example (expected '\"type\": \"function\"')"
fi

# Check for required fields in function result: name, file, lines, signature
func_fields_found=0
for field in '"name"' '"file"' '"line' '"signature"'; do
    if grep -q "$field" "$TARGET_FILE" 2>/dev/null; then
        func_fields_found=$((func_fields_found + 1))
    fi
done
if [[ "$func_fields_found" -ge 4 ]]; then
    pass "Function search example contains all required fields (name, file, line, signature)"
else
    fail "Function search example missing fields (found ${func_fields_found}/4: name, file, line, signature)"
fi
echo ""

# -----------------------------------------------------------------------------
# Test 5: Class search JSON example
# Must show class result with member enumeration
# -----------------------------------------------------------------------------
echo "--- Test 5: Class Search JSON Example ---"
if grep -q '"type".*"class"' "$TARGET_FILE" 2>/dev/null || \
   grep -q '"type": "class"' "$TARGET_FILE" 2>/dev/null; then
    pass "Contains class search JSON example with type: class"
else
    fail "Missing class search JSON example (expected '\"type\": \"class\"')"
fi

# Check for member enumeration (methods, members, or similar)
if grep -qE '"(methods|members|children)"' "$TARGET_FILE" 2>/dev/null; then
    pass "Class search example includes member enumeration"
else
    fail "Class search example missing member enumeration (expected methods/members/children field)"
fi
echo ""

# -----------------------------------------------------------------------------
# Test 6: Map ranked JSON example
# Must show ranked file importance results
# -----------------------------------------------------------------------------
echo "--- Test 6: Map Ranked JSON Example ---"
if grep -qE '"(rank|importance|score)"' "$TARGET_FILE" 2>/dev/null; then
    pass "Contains map ranked JSON example with ranking field"
else
    fail "Missing map ranked JSON example (expected rank/importance/score field)"
fi
echo ""

# -----------------------------------------------------------------------------
# Test 7: Each JSON example has narrative explanation
# Check that text content (non-code-block) appears between/after JSON blocks
# At minimum, there should be explanatory lines containing words like
# "parse", "extract", "field", "result", "shows", or "contains"
# -----------------------------------------------------------------------------
echo "--- Test 7: Narrative Explanations ---"
narrative_count=$(grep -ciE '(parse|extract|field|result|shows|contains|represents|indicates)' "$TARGET_FILE" 2>/dev/null | tr -d '\r\n' || echo "0")
if [[ -z "$narrative_count" ]]; then narrative_count=0; fi
if [[ "$narrative_count" -ge 3 ]]; then
    pass "Contains ${narrative_count} narrative explanation lines (>= 3 required)"
else
    fail "Only ${narrative_count} narrative explanation lines found (>= 3 required for 3 examples)"
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
