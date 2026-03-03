#!/usr/bin/env bash
# =============================================================================
# STORY-372 AC#1: Source Function Discovery via Treelint
# =============================================================================
# Validates that coverage-analyzer.md (or its reference files) contains:
#   1. A treelint search --type function --file instruction for source files
#   2. JSON output returns function name, line range (start_line, end_line)
#   3. Enclosing class captured for methods
#   4. Zero functions omitted guarantee documented
#
# TDD Phase: RED - Tests expected to FAIL until implementation complete.
# =============================================================================

set -euo pipefail

PROJECT_ROOT="${PROJECT_ROOT:-/mnt/c/Projects/DevForgeAI2}"
TARGET_FILE="${PROJECT_ROOT}/src/claude/agents/coverage-analyzer.md"
REFERENCE_DIR="${PROJECT_ROOT}/src/claude/agents/coverage-analyzer/references"

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

# Collect all searchable files (core + references)
search_files() {
    local files="$TARGET_FILE"
    if [[ -d "$REFERENCE_DIR" ]]; then
        for f in "$REFERENCE_DIR"/*.md; do
            [[ -r "$f" ]] && files="$files $f"
        done
    fi
    echo "$files"
}

echo "=============================================="
echo "  AC#1: Source Function Discovery via Treelint"
echo "=============================================="
echo ""

# -----------------------------------------------------------------------------
# Test 1: Target file exists
# -----------------------------------------------------------------------------
echo "--- Test 1: File Existence ---"
if [[ -r "$TARGET_FILE" ]]; then
    pass "coverage-analyzer.md exists and is readable"
else
    fail "coverage-analyzer.md not found at src/claude/agents/coverage-analyzer.md"
    echo ""
    echo "=============================================="
    echo "  AC#1 Results: ${PASS_COUNT} passed, ${FAIL_COUNT} failed (${TOTAL_COUNT} total)"
    echo "=============================================="
    echo "  STATUS: FAILED"
    exit 1
fi
echo ""

# -----------------------------------------------------------------------------
# Test 2: Contains treelint search --type function --file instruction
# -----------------------------------------------------------------------------
echo "--- Test 2: Source File Discovery via Treelint ---"
if grep -q 'treelint search.*--type function.*--file' $(search_files) 2>/dev/null; then
    pass "Contains 'treelint search --type function --file' for source file discovery"
else
    fail "Missing 'treelint search --type function --file source_file' instruction"
fi
echo ""

# -----------------------------------------------------------------------------
# Test 3: JSON output includes function name field
# -----------------------------------------------------------------------------
echo "--- Test 3: JSON Contains Function Name ---"
if grep -qE '("name"|name).*[Ff]unction.*(identifier|name)' $(search_files) 2>/dev/null; then
    pass "JSON output documents function name field"
else
    fail "Missing documentation of function name field in JSON output"
fi
echo ""

# -----------------------------------------------------------------------------
# Test 4: JSON output includes line range (start_line, end_line)
# -----------------------------------------------------------------------------
echo "--- Test 4: JSON Contains Line Range ---"
if grep -qE '(start_line|end_line|"start"|"end"|start.*end.*line)' $(search_files) 2>/dev/null; then
    pass "JSON output documents line range fields (start_line, end_line)"
else
    fail "Missing documentation of line range fields in JSON output"
fi
echo ""

# -----------------------------------------------------------------------------
# Test 5: JSON output includes enclosing class
# -----------------------------------------------------------------------------
echo "--- Test 5: Enclosing Class Captured ---"
if grep -qiE '(enclosing.class|class.*context|parent.class|enclosing_class)' $(search_files) 2>/dev/null; then
    pass "JSON output documents enclosing class capture"
else
    fail "Missing documentation of enclosing class in function discovery output"
fi
echo ""

# -----------------------------------------------------------------------------
# Test 6: Zero functions omitted guarantee
# -----------------------------------------------------------------------------
echo "--- Test 6: Zero Functions Omitted Guarantee ---"
if grep -qiE '(zero.*omit|no.*function.*omit|all.*function.*listed|complete.*function.*list|every.*function)' $(search_files) 2>/dev/null; then
    pass "Documents zero functions omitted guarantee"
else
    fail "Missing 'zero functions omitted' guarantee in source function discovery"
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
