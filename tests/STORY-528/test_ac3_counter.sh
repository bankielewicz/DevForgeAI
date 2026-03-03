#!/bin/bash
# Test: AC#3 - Stop Hook Counter Override
# Story: STORY-528
# Verifies: After 3 blocks, hook allows stop with warning

set -uo pipefail

HOOK_SCRIPT="src/claude/hooks/phase-completion-gate.sh"
PASS=0
FAIL=0
TMPDIR=""

cleanup() {
    [ -n "$TMPDIR" ] && rm -rf "$TMPDIR"
}
trap cleanup EXIT

run_test() {
    local description="$1"
    local result="$2"
    if [ "$result" -eq 0 ]; then
        echo "PASS: $description"
        ((PASS++))
    else
        echo "FAIL: $description"
        ((FAIL++))
    fi
}

echo "=== AC#3: Stop Hook Counter Override ==="
echo "Target: $HOOK_SCRIPT"
echo ""

# --- Test 1: Hook script exists ---
run_test "Hook script exists at $HOOK_SCRIPT" \
    "$([ -f "$HOOK_SCRIPT" ] && echo 0 || echo 1)"

# --- Setup: Incomplete workflow + counter at 3 ---
TMPDIR=$(mktemp -d)
mkdir -p "$TMPDIR/devforgeai/workflows"
mkdir -p "$TMPDIR/tmp/STORY-528"

cat > "$TMPDIR/devforgeai/workflows/STORY-777-phase-state.json" <<'PHASEJSON'
{
  "story_id": "STORY-777",
  "phases": {
    "01": {"name": "Pre-Flight", "status": "completed", "completed": true},
    "02": {"name": "Test-First", "status": "in_progress", "completed": false}
  }
}
PHASEJSON

# Counter file at threshold (3 attempts already)
echo "3" > "$TMPDIR/tmp/STORY-528/stop-hook-counter"

STOP_EVENT='{"event":"Stop","reason":"user_request"}'

STDERR_OUTPUT=$(echo "$STOP_EVENT" | CLAUDE_PROJECT_DIR="$TMPDIR" bash "$HOOK_SCRIPT" 2>&1 >/dev/null)
EXIT_CODE=$?

# --- Test 2: Exits 0 when counter exceeds 3 ---
run_test "Hook exits code 0 after 3 retriggers" \
    "$([ "$EXIT_CODE" -eq 0 ] && echo 0 || echo 1)"

# --- Test 3: Warning message in stderr ---
run_test "Stderr contains max retrigger warning" \
    "$(echo "$STDERR_OUTPUT" | grep -qi "max stop-hook retriggers exceeded" && echo 0 || echo 1)"

# --- Test 4: Counter file increments on block ---
# Reset counter to 1 (should block and increment)
echo "1" > "$TMPDIR/tmp/STORY-528/stop-hook-counter"

echo "$STOP_EVENT" | CLAUDE_PROJECT_DIR="$TMPDIR" bash "$HOOK_SCRIPT" 2>/dev/null
BLOCK_EXIT=$?

run_test "Hook blocks (exit 2) when counter below 3" \
    "$([ "$BLOCK_EXIT" -eq 2 ] && echo 0 || echo 1)"

COUNTER_VAL=$(cat "$TMPDIR/tmp/STORY-528/stop-hook-counter" 2>/dev/null)
run_test "Counter file incremented after block" \
    "$([ "$COUNTER_VAL" -gt 1 ] && echo 0 || echo 1)"

echo ""
echo "Results: $PASS passed, $FAIL failed"
[ "$FAIL" -eq 0 ] && exit 0 || exit 1
