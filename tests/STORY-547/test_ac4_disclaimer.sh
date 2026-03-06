#!/bin/bash
# Test: AC#4 - Disclaimer Prominent and Non-Skippable
# Story: STORY-547
# Generated: 2026-03-06
# TDD Phase: RED - These tests MUST fail before implementation

# === Test Configuration ===
PASSED=0
FAILED=0
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"

REFERENCE_FILE="$PROJECT_ROOT/src/claude/skills/advising-legal/references/when-to-hire-professional.md"

run_test() {
    local name="$1"
    local result="$2"
    if [ "$result" -eq 0 ]; then
        echo "  PASS: $name"
        ((PASSED++))
    else
        echo "  FAIL: $name"
        ((FAILED++))
    fi
}

echo "=== AC#4: Disclaimer Prominent and Non-Skippable ==="
echo ""

# === Act & Assert ===

# Test 1: Reference file exists
test -f "$REFERENCE_FILE"
run_test "Reference file exists" $?

# Test 2: Disclaimer appears within first 20 lines (prominent placement)
if [ -f "$REFERENCE_FILE" ]; then
    head -20 "$REFERENCE_FILE" | grep -qi "disclaimer"
    run_test "Disclaimer appears within first 20 lines" $?
else
    run_test "Disclaimer appears within first 20 lines" 1
fi

# Test 3: Required element - "educational" purpose
grep -qi "educational" "$REFERENCE_FILE" 2>/dev/null
run_test "Contains required element: educational purpose" $?

# Test 4: Required element - not legal advice
grep -qi "not legal advice\|does not constitute legal advice\|not.*legal advice" "$REFERENCE_FILE" 2>/dev/null
run_test "Contains required element: not legal advice" $?

# Test 5: Required element - no attorney-client relationship
grep -qi "no attorney-client\|no attorney.client\|attorney-client relationship" "$REFERENCE_FILE" 2>/dev/null
run_test "Contains required element: no attorney-client relationship" $?

# Test 6: Disclaimer appears BEFORE any substantive content sections
if [ -f "$REFERENCE_FILE" ]; then
    disclaimer_line=$(grep -ni "disclaimer" "$REFERENCE_FILE" 2>/dev/null | head -1 | cut -d: -f1)
    first_content_line=$(grep -nE "^## [^D]" "$REFERENCE_FILE" 2>/dev/null | head -1 | cut -d: -f1)
    if [ -n "$disclaimer_line" ] && [ -n "$first_content_line" ] && [ "$disclaimer_line" -lt "$first_content_line" ]; then
        run_test "Disclaimer appears before first content section" 0
    else
        run_test "Disclaimer appears before first content section" 1
    fi
else
    run_test "Disclaimer appears before first content section" 1
fi

# Test 7: Disclaimer uses visually distinct formatting (bold, blockquote, or banner)
if [ -f "$REFERENCE_FILE" ]; then
    head -25 "$REFERENCE_FILE" | grep -qE "^\*\*|^>|^---" 2>/dev/null
    run_test "Disclaimer uses visually distinct formatting" $?
else
    run_test "Disclaimer uses visually distinct formatting" 1
fi

# === Summary ===
echo ""
echo "Results: $PASSED passed, $FAILED failed"
[ $FAILED -eq 0 ] && exit 0 || exit 1
