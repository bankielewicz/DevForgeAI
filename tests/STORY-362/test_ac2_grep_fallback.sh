#!/usr/bin/env bash
# =============================================================================
# STORY-362 AC#2: Automatic Grep Fallback for Unsupported File Types
# =============================================================================
# Validates that treelint-search-patterns.md:
#   1. Documents Grep fallback for function search (FALLBACK-002)
#   2. Documents Grep fallback for class search
#   3. Documents Grep fallback for map/ranked search
#   4. Documents Grep fallback for deps/calls search
#   5. Uses Grep() tool syntax (not Bash grep) for security (NFR-005)
#   6. Fallback patterns produce usable results (downstream analysis)
#
# TDD Phase: RED - Tests expected to FAIL until implementation complete.
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
echo "  AC#2: Automatic Grep Fallback"
echo "=============================================="
echo ""

# -----------------------------------------------------------------------------
# Test 1: File exists
# -----------------------------------------------------------------------------
echo "--- Test 1: File Existence ---"
if [[ -r "$TARGET_FILE" ]]; then
    pass "Reference file exists"
else
    fail "Reference file does not exist"
    echo ""
    echo "=============================================="
    echo "  AC#2 Results: ${PASS_COUNT} passed, ${FAIL_COUNT} failed (${TOTAL_COUNT} total)"
    echo "=============================================="
    echo "  STATUS: FAILED (file does not exist - RED phase expected)"
    exit 1
fi
echo ""

# -----------------------------------------------------------------------------
# Test 2: Grep fallback for function search
# Must contain Grep(pattern= with function-related regex (def, function, func)
# -----------------------------------------------------------------------------
echo "--- Test 2: Grep Fallback for Function Search ---"
if grep -qE 'Grep\(pattern=.*def ' "$TARGET_FILE" 2>/dev/null || \
   grep -qE 'Grep\(pattern=.*function ' "$TARGET_FILE" 2>/dev/null || \
   grep -qE 'Grep\(pattern=.*func ' "$TARGET_FILE" 2>/dev/null; then
    pass "Grep fallback pattern for function search documented"
else
    fail "Missing Grep fallback pattern for treelint search --type function"
fi
echo ""

# -----------------------------------------------------------------------------
# Test 3: Grep fallback for class search
# Must contain Grep(pattern= with class-related regex
# -----------------------------------------------------------------------------
echo "--- Test 3: Grep Fallback for Class Search ---"
if grep -qE 'Grep\(pattern=.*class ' "$TARGET_FILE" 2>/dev/null; then
    pass "Grep fallback pattern for class search documented"
else
    fail "Missing Grep fallback pattern for treelint search --type class"
fi
echo ""

# -----------------------------------------------------------------------------
# Test 4: Grep fallback for map/ranked search
# Can be Glob + Grep combination for file importance heuristic
# -----------------------------------------------------------------------------
echo "--- Test 4: Grep Fallback for Map/Ranked Search ---"
if grep -qiE '(Grep|Glob).*map|map.*(Grep|Glob|fallback)' "$TARGET_FILE" 2>/dev/null; then
    pass "Grep/Glob fallback pattern for map ranked search documented"
else
    fail "Missing Grep/Glob fallback pattern for treelint map --ranked"
fi
echo ""

# -----------------------------------------------------------------------------
# Test 5: Grep fallback for deps/calls search
# Must contain import/from pattern for dependency approximation
# -----------------------------------------------------------------------------
echo "--- Test 5: Grep Fallback for Deps/Calls Search ---"
if grep -qiE 'Grep\(pattern=.*import|deps.*(Grep|fallback)' "$TARGET_FILE" 2>/dev/null; then
    pass "Grep fallback pattern for deps/calls search documented"
else
    fail "Missing Grep fallback pattern for treelint deps --calls"
fi
echo ""

# -----------------------------------------------------------------------------
# Test 6: Uses Grep() tool syntax, NOT Bash grep (NFR-005 / FALLBACK-002)
# Fallback patterns must use native Grep tool for shell injection prevention
# -----------------------------------------------------------------------------
echo "--- Test 6: Native Grep Tool Usage (NFR-005) ---"
# Count instances of Bash(command="grep or Bash(command='grep in the file
bash_grep_count=$(grep -coiE 'Bash\(command=.*grep' "$TARGET_FILE" 2>/dev/null | tr -d '\r\n' || echo "0")
if [[ -z "$bash_grep_count" ]]; then bash_grep_count=0; fi

grep_tool_count=$(grep -coE 'Grep\(pattern=' "$TARGET_FILE" 2>/dev/null | tr -d '\r\n' || echo "0")
if [[ -z "$grep_tool_count" ]]; then grep_tool_count=0; fi

if [[ "$bash_grep_count" -eq 0 && "$grep_tool_count" -ge 4 ]]; then
    pass "Uses native Grep() tool (${grep_tool_count} patterns), zero Bash grep (NFR-005)"
elif [[ "$bash_grep_count" -gt 0 ]]; then
    fail "Found ${bash_grep_count} Bash(command=grep) usages - must use Grep() tool instead (NFR-005)"
else
    fail "Insufficient Grep() tool patterns (found ${grep_tool_count}, need >= 4)"
fi
echo ""

# -----------------------------------------------------------------------------
# Test 7: At least 4 distinct Grep fallback patterns (parity check)
# BR-002: Each Treelint search type must have a Grep equivalent
# -----------------------------------------------------------------------------
echo "--- Test 7: Minimum 4 Grep Patterns (FALLBACK-006) ---"
if [[ "$grep_tool_count" -ge 4 ]]; then
    pass "At least 4 Grep fallback patterns documented (found ${grep_tool_count})"
else
    fail "Only ${grep_tool_count} Grep fallback patterns (>= 4 required for function, class, map, deps)"
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
