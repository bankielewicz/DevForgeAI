#!/usr/bin/env bash
# =============================================================================
# STORY-361 AC#1: Treelint Search Command Pattern Reference File Created
# =============================================================================
# Validates that:
#   1. Reference file exists at src/claude/agents/references/treelint-search-patterns.md
#   2. Contains "## Search Command Patterns" section heading
#   3. Documents 4 required Treelint command patterns:
#      - treelint search --type function
#      - treelint search --type class
#      - treelint map --ranked
#      - treelint deps --calls
#   4. Each command pattern has a Bash(command=...) invocation example
#   5. All treelint commands include --format json flag (BR-001)
#   6. File size is under 400 lines (BR-003)
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
echo "  AC#1: Treelint Search Command Patterns"
echo "=============================================="
echo ""

# -----------------------------------------------------------------------------
# Test 1: Target file exists and is readable
# -----------------------------------------------------------------------------
echo "--- Test 1: File Existence ---"
if [[ -r "$TARGET_FILE" ]]; then
    pass "Reference file exists at src/claude/agents/references/treelint-search-patterns.md"
else
    fail "Reference file does not exist at src/claude/agents/references/treelint-search-patterns.md"
    echo ""
    echo "=============================================="
    echo "  AC#1 Results: ${PASS_COUNT} passed, ${FAIL_COUNT} failed (${TOTAL_COUNT} total)"
    echo "=============================================="
    echo "  STATUS: FAILED (file does not exist - RED phase expected)"
    exit 1
fi
echo ""

# -----------------------------------------------------------------------------
# Test 2: File is non-empty
# -----------------------------------------------------------------------------
echo "--- Test 2: Non-Empty File ---"
if [[ -s "$TARGET_FILE" ]]; then
    pass "Reference file is non-empty"
else
    fail "Reference file is empty (zero bytes)"
fi
echo ""

# -----------------------------------------------------------------------------
# Test 3: Contains Search Command Patterns section heading
# -----------------------------------------------------------------------------
echo "--- Test 3: Search Command Patterns Section ---"
if grep -qE '^#{1,3} .*Search Command Patterns' "$TARGET_FILE" 2>/dev/null; then
    pass "Contains 'Search Command Patterns' section heading"
else
    fail "Missing 'Search Command Patterns' section heading"
fi
echo ""

# -----------------------------------------------------------------------------
# Test 4: Documents all 4 required Treelint command patterns
# -----------------------------------------------------------------------------
echo "--- Test 4: Four Required Command Patterns ---"

# 4a: treelint search --type function
if grep -q 'treelint search --type function' "$TARGET_FILE" 2>/dev/null; then
    pass "Contains 'treelint search --type function' pattern"
else
    fail "Missing 'treelint search --type function' pattern"
fi

# 4b: treelint search --type class
if grep -q 'treelint search --type class' "$TARGET_FILE" 2>/dev/null; then
    pass "Contains 'treelint search --type class' pattern"
else
    fail "Missing 'treelint search --type class' pattern"
fi

# 4c: treelint map --ranked
if grep -q 'treelint map --ranked' "$TARGET_FILE" 2>/dev/null; then
    pass "Contains 'treelint map --ranked' pattern"
else
    fail "Missing 'treelint map --ranked' pattern"
fi

# 4d: treelint deps --calls
if grep -q 'treelint deps --calls' "$TARGET_FILE" 2>/dev/null; then
    pass "Contains 'treelint deps --calls' pattern"
else
    fail "Missing 'treelint deps --calls' pattern"
fi
echo ""

# -----------------------------------------------------------------------------
# Test 5: Each command has a Bash(command=...) invocation example
# -----------------------------------------------------------------------------
echo "--- Test 5: Bash Invocation Examples ---"
bash_example_count=$(grep -c 'Bash(command=' "$TARGET_FILE" 2>/dev/null | tr -d '\r\n' || echo "0")
if [[ -z "$bash_example_count" ]]; then bash_example_count=0; fi
if [[ "$bash_example_count" -ge 4 ]]; then
    pass "Contains ${bash_example_count} Bash(command=...) invocation examples (>= 4 required)"
else
    fail "Only ${bash_example_count} Bash(command=...) invocation examples found (>= 4 required)"
fi
echo ""

# -----------------------------------------------------------------------------
# Test 6: All treelint commands include --format json (BR-001)
# BR-001 rule: All Treelint command examples must use --format json flag
# Strategy: Find treelint command invocations and check each has --format json
# -----------------------------------------------------------------------------
echo "--- Test 6: --format json Flag (BR-001) ---"
treelint_cmd_count=$(grep -cE 'treelint (search|map|deps)' "$TARGET_FILE" 2>/dev/null | tr -d '\r\n' || echo "0")
if [[ -z "$treelint_cmd_count" ]]; then treelint_cmd_count=0; fi

treelint_with_json=$(grep -E 'treelint (search|map|deps)' "$TARGET_FILE" 2>/dev/null | grep -c '\-\-format json' | tr -d '\r\n' || echo "0")
if [[ -z "$treelint_with_json" ]]; then treelint_with_json=0; fi

if [[ "$treelint_cmd_count" -gt 0 ]] && [[ "$treelint_with_json" -eq "$treelint_cmd_count" ]]; then
    pass "All ${treelint_cmd_count} treelint commands include --format json flag"
else
    fail "${treelint_with_json} of ${treelint_cmd_count} treelint commands include --format json flag (all must have it)"
fi
echo ""

# -----------------------------------------------------------------------------
# Test 7: File size under 400 lines (BR-003)
# -----------------------------------------------------------------------------
echo "--- Test 7: File Size Limit (BR-003) ---"
line_count=$(wc -l < "$TARGET_FILE" 2>/dev/null | tr -d ' \r\n' || echo "0")
if [[ -z "$line_count" ]]; then line_count=0; fi
if [[ "$line_count" -lt 400 ]]; then
    pass "File has ${line_count} lines (< 400 limit)"
else
    fail "File has ${line_count} lines (exceeds 400 line limit)"
fi
echo ""

# -----------------------------------------------------------------------------
# Test 8: Version reference specifies v0.12.0+ minimum (BR-004)
# -----------------------------------------------------------------------------
echo "--- Test 8: Version Reference (BR-004) ---"
if grep -q 'v0\.12\.0' "$TARGET_FILE" 2>/dev/null; then
    pass "Contains v0.12.0 minimum version reference"
else
    fail "Missing v0.12.0 minimum version reference"
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
