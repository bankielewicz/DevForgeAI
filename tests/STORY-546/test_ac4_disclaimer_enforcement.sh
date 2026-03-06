#!/bin/bash
# Test: AC#4 - Disclaimer Header on Every Output
# Story: STORY-546
# Generated: 2026-03-05

PASSED=0
FAILED=0
PROJECT_ROOT="/mnt/c/Projects/DevForgeAI2"
SKILL_FILE="$PROJECT_ROOT/src/claude/skills/advising-legal/SKILL.md"

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

echo "=== AC#4: Disclaimer Header on Every Output ==="

# Test 1: Skill mentions disclaimer requirement
grep -qi "disclaimer" "$SKILL_FILE" 2>/dev/null
run_test "test_should_mention_disclaimer_when_skill_evaluated" $?

# Test 2: Skill enforces disclaimer in first 10 lines of output
grep -qiE "first.*(10|ten).*lines|disclaimer.*header|prepend.*disclaimer" "$SKILL_FILE" 2>/dev/null
run_test "test_should_enforce_first_10_lines_when_skill_evaluated" $?

# Test 3: Skill contains disclaimer text or template reference
grep -qiE "not.legal.advice|disclaimer.*template|legal.*disclaimer|informational.purposes" "$SKILL_FILE" 2>/dev/null
run_test "test_should_contain_disclaimer_content_when_skill_evaluated" $?

# Test 4: Disclaimer applies in all modes (standalone included)
grep -qiE "standalone.*disclaimer|disclaimer.*standalone|every.*output|all.*output" "$SKILL_FILE" 2>/dev/null
run_test "test_should_apply_disclaimer_in_all_modes_when_skill_evaluated" $?

# Test 5: Skill specifies disclaimer is automatically prepended
grep -qiE "automatically.*prepend|prepend.*automatically|auto.*disclaimer" "$SKILL_FILE" 2>/dev/null
run_test "test_should_auto_prepend_disclaimer_when_skill_evaluated" $?

# Test 6: Disclaimer sourced from single canonical template
grep -qiE "canonical.*template|disclaimer.*template.*file|template.*disclaimer" "$SKILL_FILE" 2>/dev/null
run_test "test_should_use_canonical_template_when_skill_evaluated" $?

echo ""
echo "Results: $PASSED passed, $FAILED failed"
[ $FAILED -eq 0 ] && exit 0 || exit 1
