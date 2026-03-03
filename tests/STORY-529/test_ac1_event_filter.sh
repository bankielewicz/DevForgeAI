#!/bin/bash
# Test: AC#1 - Hook Activates on Resume/Compact Events
# Story: STORY-529
# Verifies: settings.json matcher "resume|compact" for SessionStart; hook produces output when triggered

set -uo pipefail

HOOK_SCRIPT="src/claude/hooks/inject-phase-context.sh"
SETTINGS_FILE="src/claude/settings.json"
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

echo "=== AC#1: Hook Activates on Resume/Compact Events ==="
echo "Target: $HOOK_SCRIPT"
echo ""

# --- Test 1: Hook script exists ---
run_test "Hook script exists at $HOOK_SCRIPT" \
    "$([ -f "$HOOK_SCRIPT" ] && echo 0 || echo 1)"

# --- Test 2: Hook script is executable ---
run_test "Hook script is executable" \
    "$([ -x "$HOOK_SCRIPT" ] && echo 0 || echo 1)"

# --- Test 3: settings.json contains SessionStart event ---
run_test "settings.json contains SessionStart hook event" \
    "$(grep -q '"SessionStart"' "$SETTINGS_FILE" && echo 0 || echo 1)"

# --- Test 4: SessionStart matcher is "resume|compact" ---
# Extract matcher value for SessionStart hooks
MATCHER=$(python3 -c "
import json, sys
with open('$SETTINGS_FILE') as f:
    data = json.load(f)
hooks = data.get('hooks', {}).get('SessionStart', [])
for h in hooks:
    m = h.get('matcher', '')
    if 'resume' in m and 'compact' in m:
        print('found')
        sys.exit(0)
sys.exit(1)
" 2>/dev/null || echo "")
run_test "SessionStart matcher contains resume|compact" \
    "$([ "$MATCHER" = "found" ] && echo 0 || echo 1)"

# --- Test 5: Hook produces output when triggered with active workflow ---
TMPDIR=$(mktemp -d)
mkdir -p "$TMPDIR/devforgeai/workflows"

cat > "$TMPDIR/devforgeai/workflows/STORY-900-phase-state.json" <<'PHASEJSON'
{
  "story_id": "STORY-900",
  "current_phase": "03",
  "phases": {
    "01": {"name": "Pre-Flight", "status": "completed", "completed": true},
    "02": {"name": "Test-First", "status": "completed", "completed": true},
    "03": {"name": "Implementation", "status": "in_progress", "completed": false}
  },
  "subagents_invoked": ["git-validator", "test-automator"],
  "created": "2026-03-01T10:00:00Z"
}
PHASEJSON

SESSION_EVENT='{"event":"SessionStart","source":"resume"}'
STDOUT_OUTPUT=$(echo "$SESSION_EVENT" | CLAUDE_PROJECT_DIR="$TMPDIR" bash "$HOOK_SCRIPT" 2>/dev/null)
EXIT_CODE=$?

run_test "Hook produces non-empty stdout on resume event with active workflow" \
    "$([ -n "$STDOUT_OUTPUT" ] && echo 0 || echo 1)"

# --- Test 6: Hook output contains hookSpecificOutput ---
run_test "Hook stdout contains hookSpecificOutput" \
    "$(echo "$STDOUT_OUTPUT" | grep -q "hookSpecificOutput" && echo 0 || echo 1)"

echo ""
echo "Results: $PASS passed, $FAIL failed"
[ "$FAIL" -eq 0 ] && exit 0 || exit 1
