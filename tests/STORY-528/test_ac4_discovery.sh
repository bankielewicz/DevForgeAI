#!/bin/bash
# Test: AC#4 - Workflow Discovery
# Story: STORY-528
# Verifies: Hook discovers active dev workflows, excludes QA files

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

echo "=== AC#4: Workflow Discovery ==="
echo "Target: $HOOK_SCRIPT"
echo ""

# --- Test 1: Hook script exists ---
run_test "Hook script exists at $HOOK_SCRIPT" \
    "$([ -f "$HOOK_SCRIPT" ] && echo 0 || echo 1)"

# --- Setup: Multiple workflow files ---
TMPDIR=$(mktemp -d)
mkdir -p "$TMPDIR/devforgeai/workflows"

# Dev workflow - incomplete (should be detected and block)
cat > "$TMPDIR/devforgeai/workflows/STORY-100-phase-state.json" <<'JSON'
{
  "story_id": "STORY-100",
  "phases": {
    "01": {"name": "Pre-Flight", "status": "completed", "completed": true},
    "02": {"name": "Test-First", "status": "in_progress", "completed": false}
  }
}
JSON

# Dev workflow - complete (should not block)
cat > "$TMPDIR/devforgeai/workflows/STORY-200-phase-state.json" <<'JSON'
{
  "story_id": "STORY-200",
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
JSON

# QA workflow - incomplete (should be EXCLUDED)
cat > "$TMPDIR/devforgeai/workflows/STORY-100-qa-phase-state.json" <<'JSON'
{
  "story_id": "STORY-100",
  "type": "qa",
  "phases": {
    "01": {"name": "QA Phase 1", "status": "in_progress", "completed": false}
  }
}
JSON

STOP_EVENT='{"event":"Stop","reason":"user_request"}'

STDERR_OUTPUT=$(echo "$STOP_EVENT" | CLAUDE_PROJECT_DIR="$TMPDIR" bash "$HOOK_SCRIPT" 2>&1 >/dev/null)
EXIT_CODE=$?

# --- Test 2: Blocks because STORY-100 dev workflow is incomplete ---
run_test "Blocks on incomplete dev workflow STORY-100" \
    "$([ "$EXIT_CODE" -eq 2 ] && echo 0 || echo 1)"

# --- Test 3: Stderr mentions STORY-100 ---
run_test "Stderr references STORY-100" \
    "$(echo "$STDERR_OUTPUT" | grep -q "STORY-100" && echo 0 || echo 1)"

# --- Test 4: QA file excluded (stderr should NOT mention qa) ---
run_test "QA workflow excluded from detection" \
    "$(echo "$STDERR_OUTPUT" | grep -qi "qa-phase-state" && echo 1 || echo 0)"

# --- Test 5: When only complete dev + incomplete qa, should allow ---
rm "$TMPDIR/devforgeai/workflows/STORY-100-phase-state.json"

echo "$STOP_EVENT" | CLAUDE_PROJECT_DIR="$TMPDIR" bash "$HOOK_SCRIPT" 2>/dev/null
EXIT_CODE2=$?

run_test "Allows stop when only complete dev workflows exist (QA excluded)" \
    "$([ "$EXIT_CODE2" -eq 0 ] && echo 0 || echo 1)"

echo ""
echo "Results: $PASS passed, $FAIL failed"
[ "$FAIL" -eq 0 ] && exit 0 || exit 1
