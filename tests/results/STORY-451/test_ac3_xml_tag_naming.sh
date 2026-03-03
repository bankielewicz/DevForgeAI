#!/bin/bash
# Test: AC#3 - XML Tag Naming Standardized to Hyphenated Convention
# Story: STORY-451
# Generated: 2026-02-19
# TDD Phase: RED (tests must FAIL against current state)

PASSED=0
FAILED=0

SKILL_MD="/mnt/c/Projects/DevForgeAI2/src/claude/skills/discovering-requirements/SKILL.md"

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

echo "=== AC#3: XML Tag Naming Standardized to Hyphenated Convention ==="
echo ""

# === Arrange ===
# SKILL.md lines 193-209 contain underscored XML tags that must be replaced:
#   brainstorm_context → brainstorm-context
#   user_input → user-input
#   project_context → project-context

# === Act & Assert ===

# Test 1: brainstorm_context (underscored) must NOT appear as XML tag
# Current state: lines 193 and 198 contain <brainstorm_context> and </brainstorm_context> (FAIL expected)
! grep -q '<brainstorm_context>' "$SKILL_MD"
run_test "SKILL.md does not contain <brainstorm_context> opening tag" $?

# Test 2: brainstorm_context closing tag must NOT appear
! grep -q '</brainstorm_context>' "$SKILL_MD"
run_test "SKILL.md does not contain </brainstorm_context> closing tag" $?

# Test 3: brainstorm-context (hyphenated) MUST appear as XML tag
# Current state: hyphenated form absent (FAIL expected)
grep -q '<brainstorm-context>' "$SKILL_MD"
run_test "SKILL.md contains <brainstorm-context> opening tag" $?

# Test 4: user_input (underscored) must NOT appear as XML tag
# Current state: lines 200 and 203 contain <user_input> and </user_input> (FAIL expected)
! grep -q '<user_input>' "$SKILL_MD"
run_test "SKILL.md does not contain <user_input> opening tag" $?

# Test 5: user-input (hyphenated) MUST appear as XML tag
# Current state: hyphenated form absent (FAIL expected)
grep -q '<user-input>' "$SKILL_MD"
run_test "SKILL.md contains <user-input> opening tag" $?

# Test 6: project_context (underscored) must NOT appear as XML tag
# Current state: lines 205 and 209 contain <project_context> and </project_context> (FAIL expected)
! grep -q '<project_context>' "$SKILL_MD"
run_test "SKILL.md does not contain <project_context> opening tag" $?

# Test 7: project-context (hyphenated) MUST appear as XML tag
# Current state: hyphenated form absent (FAIL expected)
grep -q '<project-context>' "$SKILL_MD"
run_test "SKILL.md contains <project-context> opening tag" $?

echo ""
echo "Results: $PASSED passed, $FAILED failed"
[ $FAILED -eq 0 ] && exit 0 || exit 1
