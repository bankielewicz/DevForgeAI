#!/bin/bash
# Test: AC#4 - Disclaimer is Prominent and Cannot Be Missed
# Story: STORY-545
# Generated: 2026-03-05
# TDD Phase: RED - These tests MUST fail before implementation

# === Test Configuration ===
PASSED=0
FAILED=0
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"

OUTPUT_FILE="$PROJECT_ROOT/devforgeai/specs/business/legal/ip-protection.md"

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

echo "=== AC#4: Disclaimer is Prominent and Cannot Be Missed ==="
echo ""

# === Arrange ===
# Output file must exist

# === Act & Assert ===

# Test 1: Output file exists
test -f "$OUTPUT_FILE"
run_test "Output file exists at devforgeai/specs/business/legal/ip-protection.md" $?

# Test 2: Disclaimer appears at TOP of file (within first 20 lines)
if [ -f "$OUTPUT_FILE" ]; then
    head -20 "$OUTPUT_FILE" | grep -qi "disclaimer"
    run_test "Disclaimer appears within first 20 lines of output" $?
else
    run_test "Disclaimer appears within first 20 lines of output" 1
fi

# Test 3: Required phrase - "educational purposes only"
grep -qi "educational purposes only" "$OUTPUT_FILE" 2>/dev/null
run_test "Contains required phrase: educational purposes only" $?

# Test 4: Required phrase - "does not constitute legal advice"
grep -qi "does not constitute legal advice" "$OUTPUT_FILE" 2>/dev/null
run_test "Contains required phrase: does not constitute legal advice" $?

# Test 5: Required phrase - "consulting a licensed attorney"
grep -qi "consulting a licensed attorney" "$OUTPUT_FILE" 2>/dev/null
run_test "Contains required phrase: consulting a licensed attorney" $?

# Test 6: Disclaimer appears BEFORE any checklist content
if [ -f "$OUTPUT_FILE" ]; then
    disclaimer_line=$(grep -ni "disclaimer" "$OUTPUT_FILE" 2>/dev/null | head -1 | cut -d: -f1)
    first_category_line=$(grep -niE "^#.*copyright|^#.*trademark|^#.*patent|^#.*trade secret" "$OUTPUT_FILE" 2>/dev/null | head -1 | cut -d: -f1)
    if [ -n "$disclaimer_line" ] && [ -n "$first_category_line" ] && [ "$disclaimer_line" -lt "$first_category_line" ]; then
        run_test "Disclaimer appears before first IP category heading" 0
    else
        run_test "Disclaimer appears before first IP category heading" 1
    fi
else
    run_test "Disclaimer appears before first IP category heading" 1
fi

# === Summary ===
echo ""
echo "Results: $PASSED passed, $FAILED failed"
[ $FAILED -eq 0 ] && exit 0 || exit 1
