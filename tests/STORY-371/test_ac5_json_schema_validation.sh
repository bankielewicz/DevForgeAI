#!/usr/bin/env bash
# =============================================================================
# STORY-371 AC#5: JSON Output Format Documented and Parsed
# =============================================================================
# Validates that code-quality-auditor.md documents:
#   1. Expected JSON schema for treelint metrics output
#   2. Required fields: file, functions array
#   3. Per-function fields: name, line_start, line_end, length, nesting_depth, complexity
#   4. Schema validation logic (validates against expected schema)
#   5. Structured error logging on schema mismatch
#
# TDD Phase: RED - Target file does not contain Treelint JSON schema docs.
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
echo "  AC#5: JSON Schema Validation"
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
    echo "  AC#5 Results: ${PASS_COUNT} passed, ${FAIL_COUNT} failed (${TOTAL_COUNT} total)"
    echo "=============================================="
    echo "  STATUS: FAILED"
    exit 1
fi
echo ""

# -----------------------------------------------------------------------------
# Test 2: Documents Treelint JSON response schema
# -----------------------------------------------------------------------------
echo "--- Test 2: Treelint JSON Schema Section ---"
if grep -qiE 'treelint.*json.*schema|json.*schema.*treelint|treelint.*response.*schema|treelint.*output.*format' "$TARGET_FILE" 2>/dev/null; then
    pass "Documents Treelint JSON response schema"
else
    fail "Missing Treelint JSON response schema documentation"
fi
echo ""

# -----------------------------------------------------------------------------
# Test 3: Schema includes 'file' field (top-level)
# -----------------------------------------------------------------------------
echo "--- Test 3: Top-Level 'file' Field ---"
if grep -qE '"file".*string|file:.*string|"file"' "$TARGET_FILE" 2>/dev/null; then
    pass "Schema includes 'file' field"
else
    fail "Missing 'file' field in schema documentation"
fi
echo ""

# -----------------------------------------------------------------------------
# Test 4: Schema includes per-function fields (name, line_start, line_end, length, nesting_depth, complexity)
# -----------------------------------------------------------------------------
echo "--- Test 4: Per-Function Schema Fields ---"
schema_fields_found=0
for field in "name" "line_start" "line_end" "nesting_depth" "complexity"; do
    if grep -q "$field" "$TARGET_FILE" 2>/dev/null; then
        schema_fields_found=$((schema_fields_found + 1))
    fi
done

if [[ "$schema_fields_found" -ge 5 ]]; then
    pass "Schema documents all 5 per-function fields"
else
    fail "Only ${schema_fields_found}/5 per-function schema fields documented"
fi
echo ""

# -----------------------------------------------------------------------------
# Test 5: Documents schema validation logic
# -----------------------------------------------------------------------------
echo "--- Test 5: Schema Validation Logic ---"
if grep -qiE 'validate.*schema|schema.*validat|verify.*schema|check.*schema|parse.*validat' "$TARGET_FILE" 2>/dev/null; then
    pass "Documents schema validation logic"
else
    fail "Missing schema validation logic documentation"
fi
echo ""

# -----------------------------------------------------------------------------
# Test 6: Documents structured error on schema mismatch
# -----------------------------------------------------------------------------
echo "--- Test 6: Structured Error on Mismatch ---"
if grep -qiE 'schema.*mismatch.*error|error.*schema.*mismatch|log.*error.*schema|structured.*error.*schema|schema.*fail.*log' "$TARGET_FILE" 2>/dev/null; then
    pass "Documents structured error logging on schema mismatch"
else
    fail "Missing structured error logging on schema mismatch"
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
