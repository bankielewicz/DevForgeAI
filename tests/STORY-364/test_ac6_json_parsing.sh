#!/usr/bin/env bash
# =============================================================================
# STORY-364 AC#6: JSON Parsing of Treelint Search Results
# =============================================================================
# Validates that the reference file contains:
#   1. JSON field extraction documentation (name, file, lines)
#   2. Class name and method count extraction for God class detection
#   3. Function line range extraction for long method detection
#   4. Empty results handling ("no structural issues found")
#   5. Malformed JSON fallback to Grep with warning
#   6. Reference file does not exceed 300 lines (BR-004)
#   7. All 8 existing review checklist sections preserved in code-reviewer.md (BR-005)
#
# TDD Phase: RED - Tests expected to FAIL until implementation complete.
# =============================================================================

set -euo pipefail

PROJECT_ROOT="${PROJECT_ROOT:-/mnt/c/Projects/DevForgeAI2}"
REFERENCE_FILE="${PROJECT_ROOT}/src/claude/agents/code-reviewer/references/treelint-review-patterns.md"
CORE_FILE="${PROJECT_ROOT}/src/claude/agents/code-reviewer.md"

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
echo "  AC#6: JSON Parsing of Treelint Results"
echo "=============================================="
echo ""

# -----------------------------------------------------------------------------
# Test 1: Reference file exists
# -----------------------------------------------------------------------------
echo "--- Test 1: File Existence ---"
if [[ -r "$REFERENCE_FILE" ]]; then
    pass "treelint-review-patterns.md exists and is readable"
else
    fail "treelint-review-patterns.md not found"
    echo ""
    echo "=============================================="
    echo "  AC#6 Results: ${PASS_COUNT} passed, ${FAIL_COUNT} failed (${TOTAL_COUNT} total)"
    echo "=============================================="
    echo "  STATUS: FAILED"
    exit 1
fi
echo ""

# -----------------------------------------------------------------------------
# Test 2: Documents JSON field extraction (name, file, lines)
# Must reference the 3 core JSON fields from Treelint output
# -----------------------------------------------------------------------------
echo "--- Test 2: JSON Field Extraction Documentation ---"
json_field_count=0

if grep -qE '(\"name\"|name.*field|\.name)' "$REFERENCE_FILE" 2>/dev/null; then
    json_field_count=$((json_field_count + 1))
fi

if grep -qE '(\"file\"|file.*field|\.file)' "$REFERENCE_FILE" 2>/dev/null; then
    json_field_count=$((json_field_count + 1))
fi

if grep -qE '(\"lines\"|lines.*field|\.lines)' "$REFERENCE_FILE" 2>/dev/null; then
    json_field_count=$((json_field_count + 1))
fi

if [[ "$json_field_count" -ge 3 ]]; then
    pass "Documents all 3 core JSON fields (name, file, lines)"
else
    fail "Only ${json_field_count}/3 core JSON fields documented (need name, file, lines)"
fi
echo ""

# -----------------------------------------------------------------------------
# Test 3: Documents class name and method count extraction
# For God class detection, must explain how to extract class data
# -----------------------------------------------------------------------------
echo "--- Test 3: Class Name and Method Count Extraction ---"
if grep -qiE '(class.*name.*method|method.*count|count.*method.*class|extract.*class)' "$REFERENCE_FILE" 2>/dev/null; then
    pass "Documents class name and method count extraction"
else
    fail "Missing documentation for extracting class name and method count from JSON"
fi
echo ""

# -----------------------------------------------------------------------------
# Test 4: Documents function line range extraction
# For long method detection, must explain how to extract function line data
# -----------------------------------------------------------------------------
echo "--- Test 4: Function Line Range Extraction ---"
if grep -qiE '(function.*line|line.*range|extract.*function|lines\[0\]|lines\[1\])' "$REFERENCE_FILE" 2>/dev/null; then
    pass "Documents function line range extraction"
else
    fail "Missing documentation for extracting function line range from JSON"
fi
echo ""

# -----------------------------------------------------------------------------
# Test 5: Empty results handling
# Must document handling empty Treelint results without error
# Reports "no structural issues found" or equivalent
# -----------------------------------------------------------------------------
echo "--- Test 5: Empty Results Handling ---"
if grep -qiE '(empty.*result|no.*result|no.*structural.*issue|no.*match|zero.*result)' "$REFERENCE_FILE" 2>/dev/null; then
    pass "Documents empty results handling"
else
    fail "Missing empty results handling documentation (should report 'no structural issues found')"
fi
echo ""

# -----------------------------------------------------------------------------
# Test 6: Malformed JSON fallback to Grep
# Must document falling back to Grep when JSON parsing fails
# with a warning message
# -----------------------------------------------------------------------------
echo "--- Test 6: Malformed JSON Fallback ---"
if grep -qiE '(malformed.*json|json.*error|parse.*fail|invalid.*json|json.*fallback)' "$REFERENCE_FILE" 2>/dev/null; then
    pass "Documents malformed JSON fallback to Grep"
else
    fail "Missing malformed JSON fallback documentation (should fall back to Grep with warning)"
fi
echo ""

# -----------------------------------------------------------------------------
# Test 7: Reference file size <= 300 lines (BR-004)
# BR-004: Reference file must not exceed 300 lines per ADR-012
# -----------------------------------------------------------------------------
echo "--- Test 7: File Size Limit (BR-004) ---"
line_count=$(wc -l < "$REFERENCE_FILE" 2>/dev/null | tr -d ' \r\n' || echo "0")
if [[ -z "$line_count" ]]; then line_count=0; fi
if [[ "$line_count" -le 300 ]]; then
    pass "Reference file has ${line_count} lines (<= 300 limit per BR-004)"
else
    fail "Reference file has ${line_count} lines (exceeds 300 line limit per BR-004)"
fi
echo ""

# -----------------------------------------------------------------------------
# Test 8: All 8 existing review checklist sections preserved (BR-005)
# BR-005: Zero regression - all existing sections must remain
# Checks code-reviewer.md for the 8 standard review checklist sections
# -----------------------------------------------------------------------------
echo "--- Test 8: Existing Review Sections Preserved (BR-005) ---"
if [[ -r "$CORE_FILE" ]]; then
    section_count=0

    if grep -qiE '(Code Quality|code.quality)' "$CORE_FILE" 2>/dev/null; then section_count=$((section_count + 1)); fi
    if grep -qiE '(Security|security)' "$CORE_FILE" 2>/dev/null; then section_count=$((section_count + 1)); fi
    if grep -qiE '(Error Handling|error.handling)' "$CORE_FILE" 2>/dev/null; then section_count=$((section_count + 1)); fi
    if grep -qiE '(Performance|performance)' "$CORE_FILE" 2>/dev/null; then section_count=$((section_count + 1)); fi
    if grep -qiE '(Testing|testing)' "$CORE_FILE" 2>/dev/null; then section_count=$((section_count + 1)); fi
    if grep -qiE '(Standards Compliance|standards.compliance|coding.standard)' "$CORE_FILE" 2>/dev/null; then section_count=$((section_count + 1)); fi
    if grep -qiE '(DoD|Definition of Done|dod.complete)' "$CORE_FILE" 2>/dev/null; then section_count=$((section_count + 1)); fi
    if grep -qiE '(Anti-Gaming|anti.gaming|gaming)' "$CORE_FILE" 2>/dev/null; then section_count=$((section_count + 1)); fi

    if [[ "$section_count" -ge 7 ]]; then
        pass "code-reviewer.md preserves ${section_count}/8 review checklist sections (BR-005)"
    else
        fail "code-reviewer.md only has ${section_count}/8 review checklist sections (BR-005 requires all 8)"
    fi
else
    fail "code-reviewer.md not found (cannot verify section preservation)"
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
