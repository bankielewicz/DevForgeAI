#!/bin/bash
# Test: AC#1 - Command Invokes advising-legal Skill
# Story: STORY-546
# Generated: 2026-03-05

PASSED=0
FAILED=0
PROJECT_ROOT="/mnt/c/Projects/DevForgeAI2"
COMMAND_FILE="$PROJECT_ROOT/src/claude/commands/legal-check.md"

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

echo "=== AC#1: Command Delegates to advising-legal Skill ==="

# Test 1: Command file exists
test -f "$COMMAND_FILE"
run_test "test_should_exist_when_command_file_created" $?

# Test 2: Command file under 500 lines
LINE_COUNT=$(wc -l < "$COMMAND_FILE" 2>/dev/null || echo 9999)
[ "$LINE_COUNT" -lt 500 ]
run_test "test_should_be_under_500_lines_when_command_file_measured" $?

# Test 3: Command references advising-legal skill
grep -qi "advising-legal" "$COMMAND_FILE" 2>/dev/null
run_test "test_should_reference_skill_when_command_evaluated" $?

# Test 4: Command references SKILL.md path
grep -q "skills/advising-legal/SKILL.md" "$COMMAND_FILE" 2>/dev/null
run_test "test_should_reference_skill_path_when_command_evaluated" $?

# Test 5: No business logic patterns in command
! grep -qE "^(def |function |class |import |from )" "$COMMAND_FILE" 2>/dev/null
run_test "test_should_have_zero_business_logic_when_command_inspected" $?

echo ""
echo "Results: $PASSED passed, $FAILED failed"
[ $FAILED -eq 0 ] && exit 0 || exit 1
