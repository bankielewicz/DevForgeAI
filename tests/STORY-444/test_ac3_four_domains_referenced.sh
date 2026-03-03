#!/bin/bash
# Test: AC#3 - Role text must reference all four domains
# Story: STORY-444
# Generated: 2026-02-18

PASSED=0
FAILED=0
SKILL_FILE="src/claude/skills/discovering-requirements/SKILL.md"
IDEATE_FILE="src/claude/commands/ideate.md"

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

echo "=== AC#3: Four Domains Referenced in Role Sections ==="

# Extract role section from SKILL.md (between "## Your Role" and next "##")
ROLE_CONTENT=$(sed -n '/^## Your Role/,/^## /p' "$SKILL_FILE" 2>/dev/null)

# Test 1: stakeholder discovery
echo "$ROLE_CONTENT" | grep -qi "stakeholder.*discovery\|stakeholder.*discover"
run_test "SKILL.md role references 'stakeholder discovery'" $?

# Test 2: requirements elicitation
echo "$ROLE_CONTENT" | grep -qi "requirements.*elicitation\|elicit.*requirements"
run_test "SKILL.md role references 'requirements elicitation'" $?

# Test 3: complexity assessment
echo "$ROLE_CONTENT" | grep -qi "complexity.*assessment\|assess.*complexity"
run_test "SKILL.md role references 'complexity assessment'" $?

# Test 4: epic decomposition
echo "$ROLE_CONTENT" | grep -qi "epic.*decomposition\|decompos.*epic"
run_test "SKILL.md role references 'epic decomposition'" $?

echo ""
echo "Results: $PASSED passed, $FAILED failed"
[ $FAILED -eq 0 ] && exit 0 || exit 1
