#!/bin/bash
# Test: AC#4 - OR-Logic Support for Required Subagents
# Story: STORY-527
# Generated: 2026-03-03

set -euo pipefail

PASSED=0
FAILED=0
HOOK_SCRIPT="/mnt/c/Projects/DevForgeAI2/.claude/hooks/validate-step-completion.sh"

run_test() {
    local name="$1"
    local result="$2"
    if [ "$result" -eq 0 ]; then
        echo "  PASS: $name"
        PASSED=$((PASSED + 1))
    else
        echo "  FAIL: $name"
        FAILED=$((FAILED + 1))
    fi
}

echo "=== AC#4: OR-Logic Support for Required Subagents ==="
echo ""

# --- Pre-check ---
if [ ! -f "$HOOK_SCRIPT" ]; then
    echo "  FAIL: Hook script does not exist at $HOOK_SCRIPT"
    echo ""
    echo "Results: 0 passed, 1 failed (hook script missing - expected in RED phase)"
    exit 1
fi

TMPDIR=$(mktemp -d)
trap "rm -rf $TMPDIR" EXIT

# Registry with OR-logic step (JSON array)
cat > "$TMPDIR/registry.json" <<'REGISTRY'
{
  "steps": [
    {"id": "03.2", "check": "backend-architect OR frontend-developer subagent invoked", "subagent": ["backend-architect", "frontend-developer"], "conditional": false}
  ]
}
REGISTRY

# --- Test 1: First option in OR-list invoked -> exit 0 ---
cat > "$TMPDIR/phase-state.json" <<'STATE'
{
  "current_phase": "03",
  "subagents_invoked": {"03": ["backend-architect", "context-validator"]}
}
STATE
TASK_JSON='{"task_id":"t1","subject":"Step 03.2: backend-architect OR frontend-developer subagent invoked","status":"completed"}'
EXIT_CODE=0
echo "$TASK_JSON" | REGISTRY_PATH="$TMPDIR/registry.json" PHASE_STATE_PATH="$TMPDIR/phase-state.json" bash "$HOOK_SCRIPT" 2>/dev/null || EXIT_CODE=$?
run_test "should_pass_when_first_or_option_invoked" "$EXIT_CODE"

# --- Test 2: Second option in OR-list invoked -> exit 0 ---
cat > "$TMPDIR/phase-state-fe.json" <<'STATE'
{
  "current_phase": "03",
  "subagents_invoked": {"03": ["frontend-developer", "context-validator"]}
}
STATE
EXIT_CODE=0
echo "$TASK_JSON" | REGISTRY_PATH="$TMPDIR/registry.json" PHASE_STATE_PATH="$TMPDIR/phase-state-fe.json" bash "$HOOK_SCRIPT" 2>/dev/null || EXIT_CODE=$?
run_test "should_pass_when_second_or_option_invoked" "$EXIT_CODE"

# --- Test 3: Both options invoked -> exit 0 ---
cat > "$TMPDIR/phase-state-both.json" <<'STATE'
{
  "current_phase": "03",
  "subagents_invoked": {"03": ["backend-architect", "frontend-developer"]}
}
STATE
EXIT_CODE=0
echo "$TASK_JSON" | REGISTRY_PATH="$TMPDIR/registry.json" PHASE_STATE_PATH="$TMPDIR/phase-state-both.json" bash "$HOOK_SCRIPT" 2>/dev/null || EXIT_CODE=$?
run_test "should_pass_when_both_or_options_invoked" "$EXIT_CODE"

# --- Test 4: NONE of OR options invoked -> exit 2 (block) ---
cat > "$TMPDIR/phase-state-none.json" <<'STATE'
{
  "current_phase": "03",
  "subagents_invoked": {"03": ["context-validator"]}
}
STATE
EXIT_CODE=0
echo "$TASK_JSON" | REGISTRY_PATH="$TMPDIR/registry.json" PHASE_STATE_PATH="$TMPDIR/phase-state-none.json" bash "$HOOK_SCRIPT" 2>/dev/null || EXIT_CODE=$?
if [ "$EXIT_CODE" -eq 2 ]; then
    run_test "should_block_exit_2_when_no_or_options_invoked" 0
else
    run_test "should_block_exit_2_when_no_or_options_invoked (got exit $EXIT_CODE, expected 2)" 1
fi

# --- Test 5: Empty subagents_invoked for phase -> exit 2 ---
cat > "$TMPDIR/phase-state-empty.json" <<'STATE'
{
  "current_phase": "03",
  "subagents_invoked": {"03": []}
}
STATE
EXIT_CODE=0
echo "$TASK_JSON" | REGISTRY_PATH="$TMPDIR/registry.json" PHASE_STATE_PATH="$TMPDIR/phase-state-empty.json" bash "$HOOK_SCRIPT" 2>/dev/null || EXIT_CODE=$?
if [ "$EXIT_CODE" -eq 2 ]; then
    run_test "should_block_exit_2_when_phase_has_empty_invocations" 0
else
    run_test "should_block_exit_2_when_phase_has_empty_invocations (got exit $EXIT_CODE, expected 2)" 1
fi

# --- Summary ---
echo ""
echo "Results: $PASSED passed, $FAILED failed"
[ "$FAILED" -eq 0 ] && exit 0 || exit 1
