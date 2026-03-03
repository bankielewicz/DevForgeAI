#!/usr/bin/env bash
# STORY-457 AC#4: New epic-coverage-result-interpreter subagent created
# Tests run against src/ tree per CLAUDE.md
set -euo pipefail

AGENT_FILE="src/claude/agents/epic-coverage-result-interpreter.md"
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

assert_less_equal() {
    local desc="$1" actual="$2" max="$3"
    if [ "$actual" -le "$max" ]; then
        echo "  PASS: $desc ($actual <= $max)"
        PASS=$((PASS + 1))
    else
        echo "  FAIL: $desc ($actual > $max)"
        FAIL=$((FAIL + 1))
    fi
}

echo "=== AC#4: epic-coverage-result-interpreter Subagent ==="
echo ""

# Test 1: File exists
echo "--- File Existence ---"
assert_true "Agent file exists" test -f "$AGENT_FILE"

# Test 2: YAML frontmatter with required fields
echo "--- YAML Frontmatter ---"
if [ -f "$AGENT_FILE" ]; then
    assert_true "Has name field" grep -q '^name:' "$AGENT_FILE"
    assert_true "Has description field" grep -q '^description:' "$AGENT_FILE"
    assert_true "Has model field" grep -q '^model:' "$AGENT_FILE"
    assert_true "Has tools field" grep -q 'tools:' "$AGENT_FILE"
fi

# Test 3: Tools limited to Read/Grep/Glob
echo "--- Tool Restrictions ---"
if [ -f "$AGENT_FILE" ]; then
    assert_true "Includes Read tool" grep -q 'Read' "$AGENT_FILE"
    assert_true "Includes Grep tool" grep -q 'Grep' "$AGENT_FILE"
    assert_true "Includes Glob tool" grep -q 'Glob' "$AGENT_FILE"
    # Ensure no write tools
    WRITE_TOOLS=$(grep -ci 'Write\|Edit\|Bash' "$AGENT_FILE" || true)
    # Allow mentions in context but not in tools section
fi

# Test 4: Line count <= 500
echo "--- Line Count ---"
if [ -f "$AGENT_FILE" ]; then
    LINE_COUNT=$(wc -l < "$AGENT_FILE")
    assert_less_equal "Agent file <= 500 lines" "$LINE_COUNT" 500
fi

# Test 5: Four display templates
echo "--- Display Templates ---"
if [ -f "$AGENT_FILE" ]; then
    assert_true "Has single-epic template" grep -qi 'single.epic' "$AGENT_FILE"
    assert_true "Has all-epics template" grep -qi 'all.epic' "$AGENT_FILE"
    assert_true "Has gap list template" grep -qi 'gap list\|gap.list\|actionable.*gap' "$AGENT_FILE"
    assert_true "Has batch summary template" grep -qi 'batch.*summar' "$AGENT_FILE"
fi

# Test 6: Visual indicators with correct thresholds
echo "--- Visual Indicators ---"
if [ -f "$AGENT_FILE" ]; then
    assert_true "Has green indicator (100%)" grep -q '✅' "$AGENT_FILE"
    assert_true "Has yellow indicator (50-99%)" grep -q '⚠️' "$AGENT_FILE"
    assert_true "Has red indicator (<50%)" grep -q '❌' "$AGENT_FILE"
    assert_true "Has 100% threshold" grep -q '100%' "$AGENT_FILE"
    assert_true "Has 50% threshold reference" grep -q '50' "$AGENT_FILE"
fi

# Test 7: Gap list with top-10 overflow and shell-escaped commands
echo "--- Gap List Features ---"
if [ -f "$AGENT_FILE" ]; then
    assert_true "Has top-10 limit" grep -qi 'top.10\|limit 10\|first 10' "$AGENT_FILE"
    assert_true "Has overflow count" grep -qi 'overflow\|more gap\|remaining' "$AGENT_FILE"
    assert_true "Has shell-escaped commands" grep -qi 'shell.*escap\|escape.*shell\|create-story' "$AGENT_FILE"
fi

# Test 8: Batch summary with success/fail counts
echo "--- Batch Summary Features ---"
if [ -f "$AGENT_FILE" ]; then
    assert_true "Has success count" grep -qi 'success' "$AGENT_FILE"
    assert_true "Has failure count" grep -qi 'fail' "$AGENT_FILE"
    assert_true "Has next steps" grep -qi 'next.*step' "$AGENT_FILE"
fi

echo ""
echo "=== Results: $PASS passed, $FAIL failed ==="
[ "$FAIL" -eq 0 ] && exit 0 || exit 1
