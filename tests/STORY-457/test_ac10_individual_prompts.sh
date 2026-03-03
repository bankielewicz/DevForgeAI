#!/usr/bin/env bash
# STORY-457 AC#10: Individual per-story priority/points prompts functional
set -euo pipefail

CMD2="src/claude/commands/create-missing-stories.md"
SKILL_DIR="src/claude/skills/validating-epic-coverage"
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

echo "=== AC#10: Individual Per-Story Prompts ==="
echo ""

# Test 1: "Set individually" option for priority
echo "--- Priority Individual Option ---"
if [ -f "$CMD2" ]; then
    assert_true "Priority has 'Set individually' option" grep -q 'Set individually.*story\|individually.*per.*story' "$CMD2"
else
    echo "  FAIL: Command file missing"
    FAIL=$((FAIL + 1))
fi

# Test 2: "Set individually" option for points
echo "--- Points Individual Option ---"
if [ -f "$CMD2" ]; then
    assert_true "Points has 'Set individually' option" grep -q 'Set individually.*story\|individually.*per.*story' "$CMD2"
fi

# Test 3: Per-story AskUserQuestion in batch loop
echo "--- Per-Story Prompts ---"
if [ -f "$CMD2" ]; then
    assert_true "Has INDIVIDUAL_PRIORITY conditional" grep -q 'INDIVIDUAL_PRIORITY' "$CMD2"
    assert_true "Has INDIVIDUAL_POINTS conditional" grep -q 'INDIVIDUAL_POINTS' "$CMD2"
fi

# Test 4: Batch context markers
echo "--- Batch Context Markers ---"
# Check in command or skill for batch markers
SEARCH_FILES="$CMD2"
[ -d "$SKILL_DIR" ] && SEARCH_FILES="$SEARCH_FILES $(find "$SKILL_DIR" -name '*.md' 2>/dev/null | tr '\n' ' ')"

for marker in "Batch Index" "Batch Total" "Created From"; do
    FOUND=$(grep -rl "$marker" $SEARCH_FILES 2>/dev/null | wc -l || true)
    if [ "$FOUND" -gt 0 ]; then
        echo "  PASS: '$marker' context marker found"
        PASS=$((PASS + 1))
    else
        echo "  FAIL: '$marker' context marker missing"
        FAIL=$((FAIL + 1))
    fi
done

echo ""
echo "=== Results: $PASS passed, $FAIL failed ==="
[ "$FAIL" -eq 0 ] && exit 0 || exit 1
