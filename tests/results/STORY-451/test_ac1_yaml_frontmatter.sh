#!/bin/bash
# Test: AC#1 - YAML Frontmatter Conforms to Anthropic Spec
# Story: STORY-451
# Generated: 2026-02-19
# TDD Phase: RED (tests must FAIL against current state)

PASSED=0
FAILED=0

SKILL_MD="/mnt/c/Projects/DevForgeAI2/src/claude/skills/discovering-requirements/SKILL.md"
IDEATE_MD="/mnt/c/Projects/DevForgeAI2/src/claude/commands/ideate.md"

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

echo "=== AC#1: YAML Frontmatter Conforms to Anthropic Spec ==="
echo ""

# === Arrange ===
# Target: SKILL.md line 4 must be: allowed-tools: Read Write Edit Glob Grep AskUserQuestion Bash Task
# Target: SKILL.md line 5 must be: model: opus
# Target: ideate.md line 5 must be: allowed-tools: Read Write Edit Glob Task AskUserQuestion

# === Act & Assert ===

# Test 1: SKILL.md allowed-tools line must NOT be quoted
# Current state: allowed-tools: "Read Write Edit Glob Grep AskUserQuestion WebFetch Bash Task" (FAIL expected)
skill_line4=$(sed -n '4p' "$SKILL_MD")
! echo "$skill_line4" | grep -q '"'
run_test "SKILL.md allowed-tools field has no quoted strings" $?

# Test 2: SKILL.md allowed-tools must NOT contain WebFetch
# Current state: line 4 contains WebFetch (FAIL expected)
skill_line4=$(sed -n '4p' "$SKILL_MD")
! echo "$skill_line4" | grep -q 'WebFetch'
run_test "SKILL.md allowed-tools does not contain WebFetch" $?

# Test 3: SKILL.md allowed-tools must contain exact unquoted value
# Current state: quoted with WebFetch present (FAIL expected)
grep -qP '^allowed-tools: Read Write Edit Glob Grep AskUserQuestion Bash Task$' "$SKILL_MD"
run_test "SKILL.md line 4 reads: allowed-tools: Read Write Edit Glob Grep AskUserQuestion Bash Task" $?

# Test 4: SKILL.md model field must NOT be quoted
# Current state: model: "opus" (FAIL expected)
skill_line5=$(sed -n '5p' "$SKILL_MD")
! echo "$skill_line5" | grep -q '"'
run_test "SKILL.md model field has no quoted strings" $?

# Test 5: SKILL.md model must be exactly: model: opus (unquoted)
# Current state: model: "opus" (FAIL expected)
grep -qP '^model: opus$' "$SKILL_MD"
run_test "SKILL.md line 5 reads: model: opus (unquoted)" $?

# Test 6: ideate.md allowed-tools must NOT be quoted
# Current state: allowed-tools: "Read Write Edit Glob Task AskUserQuestion" (FAIL expected)
ideate_line5=$(sed -n '5p' "$IDEATE_MD")
! echo "$ideate_line5" | grep -q '"'
run_test "ideate.md allowed-tools field has no quoted strings" $?

# Test 7: ideate.md allowed-tools must contain exact unquoted value
# Current state: quoted (FAIL expected)
grep -qP '^allowed-tools: Read Write Edit Glob Task AskUserQuestion$' "$IDEATE_MD"
run_test "ideate.md line 5 reads: allowed-tools: Read Write Edit Glob Task AskUserQuestion" $?

echo ""
echo "Results: $PASSED passed, $FAILED failed"
[ $FAILED -eq 0 ] && exit 0 || exit 1
