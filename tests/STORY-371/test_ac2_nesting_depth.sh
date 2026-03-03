#!/usr/bin/env bash
# =============================================================================
# STORY-371 AC#2: Nesting Depth Calculation from AST
# =============================================================================
# Validates that code-quality-auditor.md documents:
#   1. treelint metrics --nesting-depth command pattern
#   2. JSON response contains nesting_depth per function
#   3. Nesting depth definition (0 = no control structures)
#   4. Control structure types listed (if/else, for, while, try/catch, match)
#   5. Bash invocation example for nesting depth
#
# TDD Phase: RED - Target file does not contain nesting depth metrics yet.
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
echo "  AC#2: Nesting Depth Calculation from AST"
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
    echo "  AC#2 Results: ${PASS_COUNT} passed, ${FAIL_COUNT} failed (${TOTAL_COUNT} total)"
    echo "=============================================="
    echo "  STATUS: FAILED"
    exit 1
fi
echo ""

# -----------------------------------------------------------------------------
# Test 2: Contains treelint metrics --nesting-depth command
# -----------------------------------------------------------------------------
echo "--- Test 2: Nesting Depth Command Pattern ---"
if grep -q 'treelint metrics.*--nesting-depth' "$TARGET_FILE" 2>/dev/null; then
    pass "Contains 'treelint metrics --nesting-depth' command pattern"
else
    fail "Missing 'treelint metrics --nesting-depth' command pattern"
fi
echo ""

# -----------------------------------------------------------------------------
# Test 3: JSON response documents nesting_depth field
# -----------------------------------------------------------------------------
echo "--- Test 3: nesting_depth Field in Response ---"
if grep -q 'nesting_depth' "$TARGET_FILE" 2>/dev/null; then
    pass "Documents nesting_depth field in JSON response"
else
    fail "Missing nesting_depth field in JSON response documentation"
fi
echo ""

# -----------------------------------------------------------------------------
# Test 4: Describes nesting depth semantics (0 = no control structures)
# -----------------------------------------------------------------------------
echo "--- Test 4: Nesting Depth Semantics ---"
if grep -qiE 'nesting.*depth.*0.*no.*control|depth.*0.*means|nesting.*0.*no.*nested' "$TARGET_FILE" 2>/dev/null; then
    pass "Describes nesting depth 0 semantics (no control structures)"
else
    fail "Missing nesting depth semantics (0 = no control structures)"
fi
echo ""

# -----------------------------------------------------------------------------
# Test 5: Lists control structure types
# -----------------------------------------------------------------------------
echo "--- Test 5: Control Structure Types ---"
control_found=0
for structure in "if" "for" "while" "try"; do
    if grep -qi "$structure" "$TARGET_FILE" 2>/dev/null; then
        control_found=$((control_found + 1))
    fi
done

if [[ "$control_found" -ge 3 ]]; then
    pass "Lists ${control_found}/4 control structure types (if, for, while, try)"
else
    fail "Only ${control_found}/4 control structure types found (need >= 3)"
fi
echo ""

# -----------------------------------------------------------------------------
# Test 6: Contains Bash invocation for nesting depth
# -----------------------------------------------------------------------------
echo "--- Test 6: Bash Invocation Example ---"
if grep -qE 'Bash\(command=.*treelint metrics.*--nesting-depth' "$TARGET_FILE" 2>/dev/null; then
    pass "Contains Bash(command=...) invocation for nesting-depth"
else
    fail "Missing Bash(command=...) invocation for nesting-depth"
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
