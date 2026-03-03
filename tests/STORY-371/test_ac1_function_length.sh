#!/usr/bin/env bash
# =============================================================================
# STORY-371 AC#1: Function Length Extraction from AST
# =============================================================================
# Validates that code-quality-auditor.md documents:
#   1. treelint metrics --function-length command pattern
#   2. --file and --format json flags in the command
#   3. JSON response fields: name, line_start, line_end, length
#   4. Functions array in response schema
#   5. Bash(command=...) invocation example for treelint metrics
#
# TDD Phase: RED - Target file does not contain Treelint metrics yet.
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
echo "  AC#1: Function Length Extraction from AST"
echo "=============================================="
echo ""

# -----------------------------------------------------------------------------
# Test 1: Target file exists
# -----------------------------------------------------------------------------
echo "--- Test 1: File Existence ---"
if [[ -r "$TARGET_FILE" ]]; then
    pass "code-quality-auditor.md exists at src/claude/agents/"
else
    fail "code-quality-auditor.md not found at src/claude/agents/"
    echo ""
    echo "=============================================="
    echo "  AC#1 Results: ${PASS_COUNT} passed, ${FAIL_COUNT} failed (${TOTAL_COUNT} total)"
    echo "=============================================="
    echo "  STATUS: FAILED"
    exit 1
fi
echo ""

# -----------------------------------------------------------------------------
# Test 2: Contains treelint metrics --function-length command
# -----------------------------------------------------------------------------
echo "--- Test 2: Function Length Command Pattern ---"
if grep -q 'treelint metrics.*--function-length' "$TARGET_FILE" 2>/dev/null; then
    pass "Contains 'treelint metrics --function-length' command pattern"
else
    fail "Missing 'treelint metrics --function-length' command pattern"
fi
echo ""

# -----------------------------------------------------------------------------
# Test 3: Command includes --file flag and --format json
# -----------------------------------------------------------------------------
echo "--- Test 3: File and Format Flags ---"
if grep -qE 'treelint metrics.*--file.*--format json|treelint metrics.*--format json.*--file' "$TARGET_FILE" 2>/dev/null; then
    pass "Command includes --file and --format json flags"
else
    fail "Command missing --file or --format json flags"
fi
echo ""

# -----------------------------------------------------------------------------
# Test 4: JSON response documents 'functions' array
# -----------------------------------------------------------------------------
echo "--- Test 4: Functions Array in Response Schema ---"
if grep -qi 'functions.*array\|"functions".*\[' "$TARGET_FILE" 2>/dev/null; then
    pass "Documents functions array in JSON response"
else
    fail "Missing functions array documentation in JSON response"
fi
echo ""

# -----------------------------------------------------------------------------
# Test 5: Documents required fields (name, line_start, line_end, length)
# -----------------------------------------------------------------------------
echo "--- Test 5: Required JSON Fields ---"
fields_found=0

if grep -q 'name' "$TARGET_FILE" 2>/dev/null && \
   grep -q 'line_start' "$TARGET_FILE" 2>/dev/null && \
   grep -q 'line_end' "$TARGET_FILE" 2>/dev/null && \
   grep -q '"length"\|length.*integer\|length.*lines' "$TARGET_FILE" 2>/dev/null; then
    pass "Documents all 4 required fields: name, line_start, line_end, length"
else
    # Check each field individually for diagnostic
    for field in "line_start" "line_end"; do
        if ! grep -q "$field" "$TARGET_FILE" 2>/dev/null; then
            fail "Missing field: $field in JSON response documentation"
            fields_found=1
        fi
    done
    if [[ "$fields_found" -eq 0 ]]; then
        fail "Missing one or more required fields in JSON response documentation"
    fi
fi
echo ""

# -----------------------------------------------------------------------------
# Test 6: Contains Bash invocation for treelint metrics
# -----------------------------------------------------------------------------
echo "--- Test 6: Bash Invocation Example ---"
if grep -qE 'Bash\(command=.*treelint metrics' "$TARGET_FILE" 2>/dev/null; then
    pass "Contains Bash(command=...) invocation for treelint metrics"
else
    fail "Missing Bash(command=...) invocation for treelint metrics"
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
