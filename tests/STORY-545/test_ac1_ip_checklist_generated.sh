#!/bin/bash
# Test: AC#1 - IP Protection Checklist Generated for Software Project
# Story: STORY-545
# Generated: 2026-03-05
# TDD Phase: RED - These tests MUST fail before implementation

# === Test Configuration ===
PASSED=0
FAILED=0
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"

REFERENCE_FILE="$PROJECT_ROOT/src/claude/skills/advising-legal/references/ip-protection-checklist.md"
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

echo "=== AC#1: IP Protection Checklist Generated for Software Project ==="
echo ""

# === Arrange ===
# Both files must exist for any AC#1 tests to pass

# === Act & Assert ===

# Test 1: Reference file exists
test -f "$REFERENCE_FILE"
run_test "Reference file exists at src/claude/skills/advising-legal/references/ip-protection-checklist.md" $?

# Test 2: Output artifact exists
test -f "$OUTPUT_FILE"
run_test "Output artifact exists at devforgeai/specs/business/legal/ip-protection.md" $?

# Test 3: Copyright category heading present in reference
grep -qi "copyright" "$REFERENCE_FILE" 2>/dev/null
run_test "Copyright category present in reference file" $?

# Test 4: Trademark category heading present in reference
grep -qi "trademark" "$REFERENCE_FILE" 2>/dev/null
run_test "Trademark category present in reference file" $?

# Test 5: Patent basics category heading present in reference
grep -qi "patent" "$REFERENCE_FILE" 2>/dev/null
run_test "Patent basics category present in reference file" $?

# Test 6: Trade secrets category heading present in reference
grep -qi "trade secret" "$REFERENCE_FILE" 2>/dev/null
run_test "Trade secrets category present in reference file" $?

# Test 7: Output file contains all four category headings
if [ -f "$OUTPUT_FILE" ]; then
    count=0
    grep -qi "copyright" "$OUTPUT_FILE" && ((count++))
    grep -qi "trademark" "$OUTPUT_FILE" && ((count++))
    grep -qi "patent" "$OUTPUT_FILE" && ((count++))
    grep -qi "trade secret" "$OUTPUT_FILE" && ((count++))
    [ "$count" -eq 4 ]
    run_test "Output file contains all 4 IP categories" $?
else
    run_test "Output file contains all 4 IP categories" 1
fi

# Test 8: Output file contains disclaimer
grep -qi "disclaimer" "$OUTPUT_FILE" 2>/dev/null
run_test "Output file includes a disclaimer" $?

# Test 9: Reference file has software-specific examples
grep -qiE "software|SaaS|code|application" "$REFERENCE_FILE" 2>/dev/null
run_test "Reference file contains software-specific context" $?

# === Summary ===
echo ""
echo "Results: $PASSED passed, $FAILED failed"
[ $FAILED -eq 0 ] && exit 0 || exit 1
