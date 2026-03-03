#!/usr/bin/env bash
# =============================================================================
# STORY-364 AC#2: God Class Detection Using Treelint AST Search
# =============================================================================
# Validates that the reference file contains:
#   1. treelint search --type class command pattern
#   2. --format json flag on the class search command
#   3. A threshold of 20 methods for God class detection (BR-002)
#   4. Bash() tool usage for Treelint invocation
#   5. Reporting fields: class name, file path, method count, line range
#
# TDD Phase: RED - Tests expected to FAIL until implementation complete.
# =============================================================================

set -euo pipefail

PROJECT_ROOT="${PROJECT_ROOT:-/mnt/c/Projects/DevForgeAI2}"
REFERENCE_FILE="${PROJECT_ROOT}/src/claude/agents/code-reviewer/references/treelint-review-patterns.md"

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
echo "  AC#2: God Class Detection via Treelint"
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
    echo "  AC#2 Results: ${PASS_COUNT} passed, ${FAIL_COUNT} failed (${TOTAL_COUNT} total)"
    echo "=============================================="
    echo "  STATUS: FAILED"
    exit 1
fi
echo ""

# -----------------------------------------------------------------------------
# Test 2: Contains treelint search --type class command
# -----------------------------------------------------------------------------
echo "--- Test 2: Treelint Class Search Command ---"
if grep -q 'treelint search.*--type class' "$REFERENCE_FILE" 2>/dev/null; then
    pass "Contains 'treelint search --type class' command pattern"
else
    fail "Missing 'treelint search --type class' command pattern"
fi
echo ""

# -----------------------------------------------------------------------------
# Test 3: Class search includes --format json flag
# -----------------------------------------------------------------------------
echo "--- Test 3: JSON Format Flag on Class Search ---"
if grep -E 'treelint search.*--type class' "$REFERENCE_FILE" 2>/dev/null | grep -q '\-\-format json'; then
    pass "Class search command includes --format json flag"
else
    fail "Class search command missing --format json flag"
fi
echo ""

# -----------------------------------------------------------------------------
# Test 4: Contains 20-method threshold for God class (BR-002)
# BR-002: God class threshold is >20 methods per class
# -----------------------------------------------------------------------------
echo "--- Test 4: 20-Method Threshold (BR-002) ---"
if grep -qE '(>?\s*20\s*method|method.*20|20.*method|threshold.*20|20.*threshold)' "$REFERENCE_FILE" 2>/dev/null; then
    pass "Contains 20-method threshold for God class detection"
else
    fail "Missing 20-method threshold documentation (BR-002 requires >20 methods)"
fi
echo ""

# -----------------------------------------------------------------------------
# Test 5: Uses Bash() tool for Treelint class search invocation
# -----------------------------------------------------------------------------
echo "--- Test 5: Bash Tool Usage ---"
if grep -qE 'Bash\(.*treelint.*class' "$REFERENCE_FILE" 2>/dev/null; then
    pass "Uses Bash() tool for Treelint class search invocation"
else
    fail "Missing Bash() tool usage for class search (should use Bash(command=\"treelint search --type class ...\"))"
fi
echo ""

# -----------------------------------------------------------------------------
# Test 6: Documents required reporting fields (name, file, method count, lines)
# The reference must document extracting class name, file path, method count,
# and line range from Treelint JSON output
# -----------------------------------------------------------------------------
echo "--- Test 6: Required Reporting Fields ---"
field_count=0

if grep -qiE '(class\s*name|name.*field|\"name\")' "$REFERENCE_FILE" 2>/dev/null; then
    field_count=$((field_count + 1))
fi

if grep -qiE '(file\s*path|\"file\"|file.*field)' "$REFERENCE_FILE" 2>/dev/null; then
    field_count=$((field_count + 1))
fi

if grep -qiE '(method\s*count|count.*method|number.*method)' "$REFERENCE_FILE" 2>/dev/null; then
    field_count=$((field_count + 1))
fi

if grep -qiE '(line\s*range|\"lines\"|lines.*field|start.*end)' "$REFERENCE_FILE" 2>/dev/null; then
    field_count=$((field_count + 1))
fi

if [[ "$field_count" -ge 3 ]]; then
    pass "Documents ${field_count}/4 required reporting fields (name, file, method count, lines)"
else
    fail "Only ${field_count}/4 required reporting fields documented (need name, file, method count, lines)"
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
