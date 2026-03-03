#!/usr/bin/env bash
# =============================================================================
# STORY-365 AC#3: JSON Parsing of Treelint Search Results
# =============================================================================
# Validates that backend-architect.md (or its reference file) contains:
#   1. JSON parsing instructions referencing 'name' field
#   2. JSON parsing instructions referencing 'file' field
#   3. JSON parsing instructions referencing 'lines' field
#   4. JSON parsing instructions referencing 'signature' field
#
# TDD Phase: RED - Tests expected to FAIL until implementation complete.
# =============================================================================

set -euo pipefail

PROJECT_ROOT="${PROJECT_ROOT:-/mnt/c/Projects/DevForgeAI2}"
TARGET_FILE="${PROJECT_ROOT}/src/claude/agents/backend-architect.md"
REFERENCE_FILE="${PROJECT_ROOT}/src/claude/agents/backend-architect/references/treelint-patterns.md"

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
echo "  AC#3: JSON Parsing of Treelint Results"
echo "=============================================="
echo ""

# -----------------------------------------------------------------------------
# Test 1: Target file exists
# -----------------------------------------------------------------------------
echo "--- Test 1: File Existence ---"
if [[ -r "$TARGET_FILE" ]]; then
    pass "backend-architect.md exists and is readable"
else
    fail "backend-architect.md not found"
    echo ""
    echo "=============================================="
    echo "  AC#3 Results: ${PASS_COUNT} passed, ${FAIL_COUNT} failed (${TOTAL_COUNT} total)"
    echo "=============================================="
    echo "  STATUS: FAILED"
    exit 1
fi
echo ""

# -----------------------------------------------------------------------------
# Test 2: References 'name' field in JSON parsing context
# -----------------------------------------------------------------------------
echo "--- Test 2: JSON Field - name ---"
if grep -qE '(results|response|JSON).*name|name.*field|`name`' $(search_files) 2>/dev/null; then
    pass "JSON parsing references 'name' field"
else
    fail "Missing 'name' field reference in JSON parsing instructions"
fi
echo ""

# -----------------------------------------------------------------------------
# Test 3: References 'file' field in JSON parsing context
# -----------------------------------------------------------------------------
echo "--- Test 3: JSON Field - file ---"
if grep -qE '(results|response|JSON).*file|file.*field|`file`' $(search_files) 2>/dev/null; then
    pass "JSON parsing references 'file' field"
else
    fail "Missing 'file' field reference in JSON parsing instructions"
fi
echo ""

# -----------------------------------------------------------------------------
# Test 4: References 'lines' field in JSON parsing context
# -----------------------------------------------------------------------------
echo "--- Test 4: JSON Field - lines ---"
if grep -qE '(results|response|JSON).*lines|lines.*field|`lines`|\[start, end\]|line range' $(search_files) 2>/dev/null; then
    pass "JSON parsing references 'lines' field"
else
    fail "Missing 'lines' field reference in JSON parsing instructions"
fi
echo ""

# -----------------------------------------------------------------------------
# Test 5: References 'signature' field in JSON parsing context
# -----------------------------------------------------------------------------
echo "--- Test 5: JSON Field - signature ---"
if grep -qE '(results|response|JSON).*signature|signature.*field|`signature`' $(search_files) 2>/dev/null; then
    pass "JSON parsing references 'signature' field"
else
    fail "Missing 'signature' field reference in JSON parsing instructions"
fi
echo ""

# -----------------------------------------------------------------------------
# Test 6: All 4 fields mentioned together or in a structured list
# -----------------------------------------------------------------------------
echo "--- Test 6: All 4 Required Fields Referenced ---"
has_name=false
has_file=false
has_lines=false
has_signature=false

if grep -qiE '`name`|name.*:.*[Ff]unction name' $(search_files) 2>/dev/null; then has_name=true; fi
if grep -qiE '`file`|file.*:.*[Ff]ile path' $(search_files) 2>/dev/null; then has_file=true; fi
if grep -qiE '`lines`|lines.*:.*[Ll]ine range' $(search_files) 2>/dev/null; then has_lines=true; fi
if grep -qiE '`signature`|signature.*:.*[Ss]ignature' $(search_files) 2>/dev/null; then has_signature=true; fi

if $has_name && $has_file && $has_lines && $has_signature; then
    pass "All 4 required JSON fields (name, file, lines, signature) documented"
else
    fail "Not all 4 required JSON fields documented (name=$has_name, file=$has_file, lines=$has_lines, signature=$has_signature)"
fi
echo ""

# =============================================================================
# Summary
# =============================================================================
echo "=============================================="
echo "  AC#3 Results: ${PASS_COUNT} passed, ${FAIL_COUNT} failed (${TOTAL_COUNT} total)"
echo "=============================================="

if [[ "$FAIL_COUNT" -gt 0 ]]; then
    echo "  STATUS: FAILED"
    exit 1
else
    echo "  STATUS: PASSED"
    exit 0
fi
