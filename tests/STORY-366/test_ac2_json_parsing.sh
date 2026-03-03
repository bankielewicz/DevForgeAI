#!/usr/bin/env bash
# =============================================================================
# STORY-366 AC#2: JSON Parsing of Treelint Security Search Results
# =============================================================================
# Validates that security-auditor.md contains:
#   1. JSON parsing instructions referencing the 'name' field
#   2. JSON parsing instructions referencing the 'file' field
#   3. JSON parsing instructions referencing the 'lines' field
#   4. JSON parsing instructions referencing the 'signature' field
#   5. Guidance on using parsed data for targeted security analysis
#
# TDD Phase: RED - Tests expected to FAIL until implementation complete.
# =============================================================================

set -euo pipefail

PROJECT_ROOT="${PROJECT_ROOT:-/mnt/c/Projects/DevForgeAI2}"
TARGET_FILE="${PROJECT_ROOT}/src/claude/agents/security-auditor.md"

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
echo "  AC#2: JSON Parsing of Treelint Security Search Results"
echo "=============================================="
echo ""

# -----------------------------------------------------------------------------
# Test 1: Target file exists
# -----------------------------------------------------------------------------
echo "--- Test 1: File Existence ---"
if [[ -r "$TARGET_FILE" ]]; then
    pass "security-auditor.md exists and is readable"
else
    fail "security-auditor.md not found"
    echo ""
    echo "=============================================="
    echo "  AC#2 Results: ${PASS_COUNT} passed, ${FAIL_COUNT} failed (${TOTAL_COUNT} total)"
    echo "=============================================="
    echo "  STATUS: FAILED"
    exit 1
fi
echo ""

# -----------------------------------------------------------------------------
# Test 2: JSON parsing references 'name' field
# Must contain reference to extracting function name from JSON results
# -----------------------------------------------------------------------------
echo "--- Test 2: JSON 'name' Field Reference ---"
if grep -qiE '(results?\[\]\.name|"name"|`name`|name.*field|field.*name)' "$TARGET_FILE" 2>/dev/null; then
    pass "JSON parsing references 'name' field"
else
    fail "Missing JSON 'name' field reference in parsing instructions"
fi
echo ""

# -----------------------------------------------------------------------------
# Test 3: JSON parsing references 'file' field
# Must contain reference to extracting file path from JSON results
# -----------------------------------------------------------------------------
echo "--- Test 3: JSON 'file' Field Reference ---"
if grep -qiE '(results?\[\]\.file|"file"|`file`|file.*field|field.*file.*path)' "$TARGET_FILE" 2>/dev/null; then
    pass "JSON parsing references 'file' field"
else
    fail "Missing JSON 'file' field reference in parsing instructions"
fi
echo ""

# -----------------------------------------------------------------------------
# Test 4: JSON parsing references 'lines' field
# Must contain reference to extracting line range from JSON results
# -----------------------------------------------------------------------------
echo "--- Test 4: JSON 'lines' Field Reference ---"
if grep -qiE '(results?\[\]\.lines|"lines"|`lines`|lines.*field|line.*range)' "$TARGET_FILE" 2>/dev/null; then
    pass "JSON parsing references 'lines' field"
else
    fail "Missing JSON 'lines' field reference in parsing instructions"
fi
echo ""

# -----------------------------------------------------------------------------
# Test 5: JSON parsing references 'signature' field
# Must contain reference to extracting function signature from JSON results
# -----------------------------------------------------------------------------
echo "--- Test 5: JSON 'signature' Field Reference ---"
if grep -qiE '(results?\[\]\.signature|"signature"|`signature`|signature.*field|field.*signature)' "$TARGET_FILE" 2>/dev/null; then
    pass "JSON parsing references 'signature' field"
else
    fail "Missing JSON 'signature' field reference in parsing instructions"
fi
echo ""

# -----------------------------------------------------------------------------
# Test 6: All 4 required fields mentioned in close proximity
# Validates that the 4 fields are documented as a cohesive set, not scattered
# At minimum, the file must contain all 4 field names
# -----------------------------------------------------------------------------
echo "--- Test 6: All 4 Required Fields Present ---"
fields_found=0
for field in name file lines signature; do
    if grep -qiE "(\"${field}\"|'${field}'|\`${field}\`|${field}.*field|field.*${field})" "$TARGET_FILE" 2>/dev/null; then
        fields_found=$((fields_found + 1))
    fi
done

if [[ "$fields_found" -ge 4 ]]; then
    pass "All 4 required JSON fields (name, file, lines, signature) referenced"
else
    fail "Only ${fields_found}/4 required JSON fields found (need: name, file, lines, signature)"
fi
echo ""

# -----------------------------------------------------------------------------
# Test 7: Guidance on using parsed data for security analysis
# Must mention using Treelint results for targeted/focused security analysis
# -----------------------------------------------------------------------------
echo "--- Test 7: Targeted Security Analysis Guidance ---"
if grep -qiE '(targeted.*security|security.*analysis|inspect.*function.*bod|Read\(\).*vulnerabilit|vulnerabilit.*Read)' "$TARGET_FILE" 2>/dev/null; then
    pass "Contains guidance on using parsed data for targeted security analysis"
else
    fail "Missing guidance on using parsed JSON data for targeted security analysis"
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
