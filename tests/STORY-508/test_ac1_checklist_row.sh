#!/bin/bash
# Test: AC#1 - Checklist Updated to 13 Sections
# Story: STORY-508
# Generated: 2026-02-28

PASSED=0
FAILED=0
TARGET_FILE="/mnt/c/Projects/DevForgeAI2/src/claude/skills/designing-systems/references/artifact-generation.md"

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

echo "=== AC#1: Checklist Updated to 13 Sections ==="

# Test 1: Decision Context row exists in the checklist table
grep -q "Decision Context" "$TARGET_FILE"
run_test "Decision Context row exists in checklist table" $?

# Test 2: Decision Context row has Required=checkmark
grep "Decision Context" "$TARGET_FILE" | grep -q "✓"
run_test "Decision Context row has Required checkmark" $?

# Test 3: Decision Context row has correct Purpose text
grep "Decision Context" "$TARGET_FILE" | grep -qi "design rationale.*rejected alternatives.*constraints.*key insights"
run_test "Decision Context row has correct Purpose description" $?

# Test 4: Table has exactly 13 data rows (excluding header and separator)
ROW_COUNT=$(grep -c "^|" "$TARGET_FILE" | head -1)
# Count rows containing checkmark in the compliance table section
SECTION_ROWS=$(sed -n '/Section Compliance Checklist/,/^[^|]/p' "$TARGET_FILE" | grep -c "| ✓")
[ "$SECTION_ROWS" -eq 13 ]
run_test "Checklist table has exactly 13 required sections" $?

echo ""
echo "Results: $PASSED passed, $FAILED failed"
[ $FAILED -eq 0 ] && exit 0 || exit 1
