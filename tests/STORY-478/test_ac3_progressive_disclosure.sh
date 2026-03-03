#!/bin/bash
# Test: AC#3 - Progressive Disclosure Compliance
# Story: STORY-478
# Generated: 2026-02-23
set -uo pipefail

PROJECT_ROOT="/mnt/c/Projects/DevForgeAI2"
SKILLMD="$PROJECT_ROOT/src/claude/skills/designing-systems/SKILL.md"
REFFILE="$PROJECT_ROOT/src/claude/skills/designing-systems/references/domain-reference-generation.md"
PASSED=0
FAILED=0

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

echo "=== AC#3: Progressive Disclosure Compliance ==="

# Test 1: SKILL.md Phase 5.7 section is 25-30 lines (lean)
START_LINE=$(grep -n "Phase 5\.7" "$SKILLMD" | head -1 | cut -d: -f1)
# Find next phase header after Phase 5.7
END_LINE=$(awk "NR>$START_LINE && /^#.*Phase [0-9]/{print NR; exit}" "$SKILLMD")
SECTION_LINES=$((END_LINE - START_LINE))
[ "$SECTION_LINES" -ge 25 ] && [ "$SECTION_LINES" -le 30 ]
run_test "test_should_have_25_to_30_lines_when_skillmd_phase57_measured" $?

# Test 2: SKILL.md contains purpose statement
grep -A 30 "Phase 5\.7" "$SKILLMD" | grep -iq "purpose"
run_test "test_should_contain_purpose_when_skillmd_phase57_checked" $?

# Test 3: SKILL.md contains precondition
grep -A 30 "Phase 5\.7" "$SKILLMD" | grep -iq "precondition"
run_test "test_should_contain_precondition_when_skillmd_phase57_checked" $?

# Test 4: SKILL.md contains postcondition
grep -A 30 "Phase 5\.7" "$SKILLMD" | grep -iq "postcondition"
run_test "test_should_contain_postcondition_when_skillmd_phase57_checked" $?

# Test 5: Detailed workflow in reference file, not SKILL.md
REFLINES=$(wc -l < "$REFFILE")
[ "$REFLINES" -gt 100 ]
run_test "test_should_have_detailed_workflow_in_reference_file_when_checked" $?

echo ""
echo "Results: $PASSED passed, $FAILED failed"
[ $FAILED -eq 0 ] && exit 0 || exit 1
