#!/usr/bin/env bash
# STORY-457 AC#8: Backward-compatible output for all command modes
# Verifies help text, error messages, visual indicators preserved
set -euo pipefail

CMD1="src/claude/commands/validate-epic-coverage.md"
CMD2="src/claude/commands/create-missing-stories.md"
SKILL="src/claude/skills/validating-epic-coverage/SKILL.md"
AGENT="src/claude/agents/epic-coverage-result-interpreter.md"
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

echo "=== AC#8: Backward-Compatible Output ==="
echo ""

# Test 1: validate-epic-coverage help text sections
echo "--- validate-epic-coverage Help Sections ---"
if [ -f "$CMD1" ]; then
    assert_true "Help: USAGE section" grep -q 'USAGE:' "$CMD1"
    assert_true "Help: ARGUMENTS section" grep -q 'ARGUMENTS:' "$CMD1"
    assert_true "Help: OPTIONS section" grep -q 'OPTIONS:' "$CMD1"
    assert_true "Help: EXAMPLES section" grep -q 'EXAMPLES:' "$CMD1"
    assert_true "Help: OUTPUT section" grep -q 'OUTPUT:' "$CMD1"
    assert_true "Help: RELATED COMMANDS section" grep -q 'RELATED COMMANDS:' "$CMD1"
    assert_true "Help: EXIT CODES section" grep -q 'EXIT CODES:' "$CMD1"
else
    echo "  FAIL: Cannot check help - file missing"
    FAIL=$((FAIL + 1))
fi

# Test 2: create-missing-stories help text sections
echo "--- create-missing-stories Help Sections ---"
if [ -f "$CMD2" ]; then
    assert_true "Help: USAGE section" grep -q 'USAGE:' "$CMD2"
    assert_true "Help: ARGUMENTS section" grep -q 'ARGUMENTS:' "$CMD2"
    assert_true "Help: DESCRIPTION section" grep -q 'DESCRIPTION:' "$CMD2"
    assert_true "Help: EXAMPLES section" grep -q 'EXAMPLES:' "$CMD2"
    assert_true "Help: OUTPUT section" grep -q 'OUTPUT:' "$CMD2"
    assert_true "Help: ERROR HANDLING section" grep -q 'ERROR HANDLING:' "$CMD2"
    assert_true "Help: RELATED COMMANDS section" grep -q 'RELATED COMMANDS:' "$CMD2"
    assert_true "Help: EXIT CODES section" grep -q 'EXIT CODES:' "$CMD2"
else
    echo "  FAIL: Cannot check help - file missing"
    FAIL=$((FAIL + 1))
fi

# Test 3: Visual indicators preserved across all artifacts
echo "--- Visual Indicators ---"
# Check that indicators exist in agent or skill (display logic)
SEARCH_FILES=""
[ -f "$AGENT" ] && SEARCH_FILES="$AGENT"
[ -f "$SKILL" ] && SEARCH_FILES="$SEARCH_FILES $SKILL"
if [ -n "$SEARCH_FILES" ]; then
    assert_true "Green indicator (✅) in display logic" grep -lq '✅' $SEARCH_FILES
    assert_true "Yellow indicator (⚠️) in display logic" grep -lq '⚠️' $SEARCH_FILES
    assert_true "Red indicator (❌) in display logic" grep -lq '❌' $SEARCH_FILES
else
    echo "  FAIL: No display files found to check"
    FAIL=$((FAIL + 1))
fi

# Test 4: Error message format (emoji + message + suggestion)
echo "--- Error Message Format ---"
if [ -f "$CMD1" ]; then
    assert_true "validate-epic-coverage: emoji error format" grep -q '❌.*not found\|❌.*Invalid' "$CMD1"
fi
if [ -f "$CMD2" ]; then
    assert_true "create-missing-stories: emoji error format" grep -q '❌.*not found\|❌.*Invalid\|❌.*required' "$CMD2"
fi

echo ""
echo "=== Results: $PASS passed, $FAIL failed ==="
[ "$FAIL" -eq 0 ] && exit 0 || exit 1
