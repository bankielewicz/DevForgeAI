#!/usr/bin/env bash
# STORY-457 AC#11: AskUserQuestion calls reside in commands, zero in skill
set -euo pipefail

CMD1="src/claude/commands/validate-epic-coverage.md"
CMD2="src/claude/commands/create-missing-stories.md"
SKILL_FILE="src/claude/skills/validating-epic-coverage/SKILL.md"
PASS=0
FAIL=0

assert_true() {
    local desc="$1"; shift
    if "$@" >/dev/null 2>&1; then
        echo "  PASS: $desc"
        PASS=$((PASS + 1))
    else
        echo "  FAIL: $desc"
        FAIL=$((FAIL + 1))
    fi
}

assert_equal() {
    local desc="$1" actual="$2" expected="$3"
    if [ "$actual" = "$expected" ]; then
        echo "  PASS: $desc ($actual = $expected)"
        PASS=$((PASS + 1))
    else
        echo "  FAIL: $desc ($actual != $expected)"
        FAIL=$((FAIL + 1))
    fi
}

echo "=== AC#11: AskUserQuestion Placement ==="
echo ""

# Test 1: SKILL.md contains ZERO AskUserQuestion calls
echo "--- Skill Has Zero AskUserQuestion ---"
if [ -f "$SKILL_FILE" ]; then
    ASK_COUNT=$(grep -c 'AskUserQuestion' "$SKILL_FILE" || true)
    assert_equal "SKILL.md AskUserQuestion count = 0" "$ASK_COUNT" "0"
else
    echo "  FAIL: Skill file missing"
    FAIL=$((FAIL + 1))
fi

# Test 2: validate-epic-coverage has AskUserQuestion for interactive prompts
echo "--- validate-epic-coverage Has AskUserQuestion ---"
if [ -f "$CMD1" ]; then
    ASK_COUNT=$(grep -c 'AskUserQuestion' "$CMD1" || true)
    if [ "$ASK_COUNT" -gt 0 ]; then
        echo "  PASS: validate-epic-coverage has AskUserQuestion ($ASK_COUNT calls)"
        PASS=$((PASS + 1))
    else
        echo "  FAIL: validate-epic-coverage has no AskUserQuestion calls"
        FAIL=$((FAIL + 1))
    fi
fi

# Test 3: create-missing-stories has AskUserQuestion for metadata collection
echo "--- create-missing-stories Has AskUserQuestion ---"
if [ -f "$CMD2" ]; then
    ASK_COUNT=$(grep -c 'AskUserQuestion' "$CMD2" || true)
    if [ "$ASK_COUNT" -gt 0 ]; then
        echo "  PASS: create-missing-stories has AskUserQuestion ($ASK_COUNT calls)"
        PASS=$((PASS + 1))
    else
        echo "  FAIL: create-missing-stories has no AskUserQuestion calls"
        FAIL=$((FAIL + 1))
    fi
fi

# Test 4: Skill returns structured gap data
echo "--- Skill Returns Structured Data ---"
if [ -f "$SKILL_FILE" ]; then
    assert_true "Skill returns structured data" grep -qi 'return\|result\|structured.*data\|gap.*data\|JSON' "$SKILL_FILE"
fi

echo ""
echo "=== Results: $PASS passed, $FAIL failed ==="
[ "$FAIL" -eq 0 ] && exit 0 || exit 1
