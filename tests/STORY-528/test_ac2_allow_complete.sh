#!/bin/bash
# Test: AC#2 - Allow Complete Workflows
# Story: STORY-528
# Verifies: Hook exits code 0 when all phases are completed

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

echo "=== AC#2: Allow Complete Workflows ==="
echo "Target: $HOOK_SCRIPT"
echo ""

# --- Test 1: Hook script exists ---
run_test "Hook script exists at $HOOK_SCRIPT" \
    "$([ -f "$HOOK_SCRIPT" ] && echo 0 || echo 1)"

# --- Test 2: Hook exits 0 when all phases complete ---
TMPDIR=$(mktemp -d)
mkdir -p "$TMPDIR/devforgeai/workflows"

cat > "$TMPDIR/devforgeai/workflows/STORY-888-phase-state.json" <<'PHASEJSON'
{
  "story_id": "STORY-888",
  "phases": {
    "01": {"name": "Pre-Flight", "status": "completed", "completed": true},
    "02": {"name": "Test-First", "status": "completed", "completed": true},
    "03": {"name": "Implementation", "status": "completed", "completed": true},
    "04": {"name": "Refactoring", "status": "completed", "completed": true},
    "05": {"name": "Integration", "status": "completed", "completed": true},
    "06": {"name": "Deferral", "status": "completed", "completed": true},
    "07": {"name": "DoD Update", "status": "completed", "completed": true},
    "08": {"name": "Git Workflow", "status": "completed", "completed": true},
    "09": {"name": "Feedback", "status": "completed", "completed": true},
    "10": {"name": "Result", "status": "completed", "completed": true}
  }
}
PHASEJSON

STOP_EVENT='{"event":"Stop","reason":"user_request"}'

echo "$STOP_EVENT" | CLAUDE_PROJECT_DIR="$TMPDIR" bash "$HOOK_SCRIPT" 2>/dev/null
EXIT_CODE=$?

run_test "Hook exits code 0 when all phases complete" \
    "$([ "$EXIT_CODE" -eq 0 ] && echo 0 || echo 1)"

echo ""
echo "Results: $PASS passed, $FAIL failed"
[ "$FAIL" -eq 0 ] && exit 0 || exit 1
