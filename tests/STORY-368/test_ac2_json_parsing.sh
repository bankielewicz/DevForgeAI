#!/usr/bin/env bash
# =============================================================================
# STORY-368 AC#2: JSON Parsing of Treelint Search Results
# =============================================================================
# Validates that coverage-analyzer.md (or its reference file) contains:
#   1. JSON parsing instructions referencing the 'name' field
#   2. JSON parsing instructions referencing the 'file' field
#   3. JSON parsing instructions referencing the 'lines' field
#   4. JSON parsing instructions referencing the 'signature' field
#   5. All 4 fields mentioned together in a parsing context
#
# TDD Phase: RED - Tests expected to FAIL until implementation complete.
# =============================================================================

set -euo pipefail

PROJECT_ROOT="${PROJECT_ROOT:-/mnt/c/Projects/DevForgeAI2}"
TARGET_FILE="${PROJECT_ROOT}/src/claude/agents/coverage-analyzer.md"
REFERENCE_FILE="${PROJECT_ROOT}/src/claude/agents/coverage-analyzer/references/treelint-patterns.md"

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
echo "  AC#2: JSON Parsing of Treelint Search Results"
echo "=============================================="
echo ""

# -----------------------------------------------------------------------------
# Test 1: Target file exists
# -----------------------------------------------------------------------------
echo "--- Test 1: File Existence ---"
if [[ -r "$TARGET_FILE" ]]; then
    pass "coverage-analyzer.md exists and is readable"
else
    fail "coverage-analyzer.md not found"
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
# -----------------------------------------------------------------------------
echo "--- Test 2: JSON Field - name ---"
if grep -qE 'results.*\.name|"name"|`name`|name.*[Ff]unction name' $(search_files) 2>/dev/null; then
    pass "JSON parsing references 'name' field"
else
    fail "Missing 'name' field reference in JSON parsing instructions"
fi
echo ""

# -----------------------------------------------------------------------------
# Test 3: JSON parsing references 'file' field
# -----------------------------------------------------------------------------
echo "--- Test 3: JSON Field - file ---"
if grep -qE 'results.*\.file|"file"|`file`|file.*[Ff]ile path|file.*[Ss]ource' $(search_files) 2>/dev/null; then
    pass "JSON parsing references 'file' field"
else
    fail "Missing 'file' field reference in JSON parsing instructions"
fi
echo ""

# -----------------------------------------------------------------------------
# Test 4: JSON parsing references 'lines' field
# -----------------------------------------------------------------------------
echo "--- Test 4: JSON Field - lines ---"
if grep -qE 'results.*\.lines|"lines"|`lines`|lines.*\[start.*end\]|lines.*[Ll]ine range' $(search_files) 2>/dev/null; then
    pass "JSON parsing references 'lines' field"
else
    fail "Missing 'lines' field reference in JSON parsing instructions"
fi
echo ""

# -----------------------------------------------------------------------------
# Test 5: JSON parsing references 'signature' field
# -----------------------------------------------------------------------------
echo "--- Test 5: JSON Field - signature ---"
if grep -qE 'results.*\.signature|"signature"|`signature`|signature.*[Ff]unction signature' $(search_files) 2>/dev/null; then
    pass "JSON parsing references 'signature' field"
else
    fail "Missing 'signature' field reference in JSON parsing instructions"
fi
echo ""

# -----------------------------------------------------------------------------
# Test 6: All 4 fields mentioned in JSON parsing context
# -----------------------------------------------------------------------------
echo "--- Test 6: All 4 Required Fields Present ---"
name_found=false
file_found=false
lines_found=false
sig_found=false

if grep -qiE 'name' $(search_files) 2>/dev/null; then name_found=true; fi
if grep -qiE '\.file|"file"|`file`' $(search_files) 2>/dev/null; then file_found=true; fi
if grep -qiE '\.lines|"lines"|`lines`' $(search_files) 2>/dev/null; then lines_found=true; fi
if grep -qiE 'signature' $(search_files) 2>/dev/null; then sig_found=true; fi

if $name_found && $file_found && $lines_found && $sig_found; then
    pass "All 4 required JSON fields (name, file, lines, signature) are referenced"
else
    missing=""
    $name_found || missing="${missing} name"
    $file_found || missing="${missing} file"
    $lines_found || missing="${missing} lines"
    $sig_found || missing="${missing} signature"
    fail "Missing JSON field references:${missing}"
fi
echo ""

# -----------------------------------------------------------------------------
# Test 7: JSON parsing section or context exists
# -----------------------------------------------------------------------------
echo "--- Test 7: JSON Parsing Section ---"
if grep -qiE '(pars|extract).*JSON|JSON.*(pars|extract|response|results)' $(search_files) 2>/dev/null; then
    pass "JSON parsing section or context found"
else
    fail "Missing JSON parsing section (e.g., 'Parse JSON results' or 'Extract from JSON response')"
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
