#!/bin/bash
# Test: Edge Case - stop_hook_active Flag
# Story: STORY-528
# Verifies: Hook exits 0 immediately when stop_hook_active=true in input

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

echo "=== Edge Case: stop_hook_active Flag ==="
echo "Target: $HOOK_SCRIPT"
echo ""

run_test "Hook script exists at $HOOK_SCRIPT" \
    "$([ -f "$HOOK_SCRIPT" ] && echo 0 || echo 1)"

# Setup incomplete workflow that would normally block
TMPDIR=$(mktemp -d)
mkdir -p "$TMPDIR/devforgeai/workflows"

cat > "$TMPDIR/devforgeai/workflows/STORY-444-phase-state.json" <<'JSON'
{
  "story_id": "STORY-444",
  "phases": {
    "01": {"name": "Pre-Flight", "status": "in_progress", "completed": false}
  }
}
JSON

# Input with stop_hook_active=true should bypass all checks
STOP_EVENT='{"event":"Stop","reason":"user_request","stop_hook_active":true}'

echo "$STOP_EVENT" | CLAUDE_PROJECT_DIR="$TMPDIR" bash "$HOOK_SCRIPT" 2>/dev/null
EXIT_CODE=$?

run_test "Hook exits 0 immediately when stop_hook_active=true" \
    "$([ "$EXIT_CODE" -eq 0 ] && echo 0 || echo 1)"

echo ""
echo "Results: $PASS passed, $FAIL failed"
[ "$FAIL" -eq 0 ] && exit 0 || exit 1
