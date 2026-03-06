#!/bin/bash
# Test: AC#5 - Standalone Mode Operates Without Project Context
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

echo "=== AC#5: Standalone Mode ==="

# Test 1: Skill mentions standalone mode
grep -qi "standalone" "$SKILL_FILE" 2>/dev/null
run_test "test_should_support_standalone_mode_when_skill_evaluated" $?

# Test 2: Skill detects absence of project context
grep -qiE "no.*project|without.*project|project.*absent|context.*missing|source-tree.*absent" "$SKILL_FILE" 2>/dev/null
run_test "test_should_detect_no_project_context_when_skill_evaluated" $?

# Test 3: Skill completes gracefully without context
grep -qiE "graceful|omit.*project|skip.*context|unavailable" "$SKILL_FILE" 2>/dev/null
run_test "test_should_complete_gracefully_when_no_context" $?

# Test 4: Skill informs user about missing enrichment
grep -qiE "inform.*user|enrichment.*unavailable|project.*not.*available" "$SKILL_FILE" 2>/dev/null
run_test "test_should_inform_user_when_enrichment_unavailable" $?

echo ""
echo "Results: $PASSED passed, $FAILED failed"
[ $FAILED -eq 0 ] && exit 0 || exit 1
