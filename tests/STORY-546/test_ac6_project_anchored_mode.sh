#!/bin/bash
# Test: AC#6 - Project-Anchored Mode Enriches Assessment
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

echo "=== AC#6: Project-Anchored Mode ==="

# Test 1: Skill mentions project-anchored mode
grep -qiE "project.anchored|project.mode|anchored.mode" "$SKILL_FILE" 2>/dev/null
run_test "test_should_support_project_anchored_mode_when_skill_evaluated" $?

# Test 2: Skill uses source-tree.md as mode detection heuristic
grep -q "source-tree.md" "$SKILL_FILE" 2>/dev/null
run_test "test_should_detect_mode_via_source_tree_when_skill_evaluated" $?

# Test 3: Skill reads context files in read-only mode
grep -qE "Read\(.*context" "$SKILL_FILE" 2>/dev/null
run_test "test_should_read_context_files_when_project_anchored" $?

# Test 4: Skill cites source context file and line range
grep -qiE "cite|citation|source.*line|line.*range" "$SKILL_FILE" 2>/dev/null
run_test "test_should_cite_context_sources_when_project_anchored" $?

echo ""
echo "Results: $PASSED passed, $FAILED failed"
[ $FAILED -eq 0 ] && exit 0 || exit 1
