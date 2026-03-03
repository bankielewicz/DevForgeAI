#!/bin/bash
# Test: AC#6 - Human-Readable Reporting
# Story: STORY-528
# Verifies: Stderr lists each incomplete phase with details

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

echo "=== AC#6: Human-Readable Reporting ==="
echo "Target: $HOOK_SCRIPT"
echo ""

# --- Test 1: Hook script exists ---
run_test "Hook script exists at $HOOK_SCRIPT" \
    "$([ -f "$HOOK_SCRIPT" ] && echo 0 || echo 1)"

# --- Setup: Workflow with specific incomplete phases ---
TMPDIR=$(mktemp -d)
mkdir -p "$TMPDIR/devforgeai/workflows"

cat > "$TMPDIR/devforgeai/workflows/STORY-555-phase-state.json" <<'PHASEJSON'
{
  "story_id": "STORY-555",
  "phases": {
    "01": {"name": "Pre-Flight", "status": "completed", "completed": true},
    "02": {"name": "Test-First", "status": "completed", "completed": true},
    "03": {"name": "Implementation", "status": "in_progress", "completed": false},
    "04": {"name": "Refactoring", "status": "pending", "completed": false},
    "05": {"name": "Integration", "status": "pending", "completed": false}
  }
}
PHASEJSON

STOP_EVENT='{"event":"Stop","reason":"user_request"}'

STDERR_OUTPUT=$(echo "$STOP_EVENT" | CLAUDE_PROJECT_DIR="$TMPDIR" bash "$HOOK_SCRIPT" 2>&1 >/dev/null)
EXIT_CODE=$?

# --- Test 2: Exit code 2 ---
run_test "Hook exits code 2" \
    "$([ "$EXIT_CODE" -eq 2 ] && echo 0 || echo 1)"

# --- Test 3: Lists phase 03 as incomplete ---
run_test "Reports phase 03 (Implementation) as incomplete" \
    "$(echo "$STDERR_OUTPUT" | grep -qE "03|Implementation" && echo 0 || echo 1)"

# --- Test 4: Lists phase 04 as incomplete ---
run_test "Reports phase 04 (Refactoring) as incomplete" \
    "$(echo "$STDERR_OUTPUT" | grep -qE "04|Refactoring" && echo 0 || echo 1)"

# --- Test 5: Lists phase 05 as incomplete ---
run_test "Reports phase 05 (Integration) as incomplete" \
    "$(echo "$STDERR_OUTPUT" | grep -qE "05|Integration" && echo 0 || echo 1)"

# --- Test 6: Output is human-readable (contains structured info) ---
run_test "Output contains story identifier" \
    "$(echo "$STDERR_OUTPUT" | grep -q "STORY-555" && echo 0 || echo 1)"

# --- Test 7: Does NOT list completed phases as incomplete ---
run_test "Does not report completed phase 01 as incomplete" \
    "$(echo "$STDERR_OUTPUT" | grep -qE "Pre-Flight.*incomplete\|01.*incomplete" && echo 1 || echo 0)"

echo ""
echo "Results: $PASS passed, $FAIL failed"
[ "$FAIL" -eq 0 ] && exit 0 || exit 1
