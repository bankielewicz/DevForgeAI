#!/bin/bash
# Test: AC#3 - Conditional Steps Always Pass
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

echo "=== AC#3: Conditional Steps Always Pass ==="
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

# Registry with conditional step
cat > "$TMPDIR/registry.json" <<'REGISTRY'
{
  "steps": [
    {"id": "01.5", "check": "Plan file check for resume", "subagent": null, "conditional": true},
    {"id": "06.1", "check": "deferral-validator if deferrals exist", "subagent": "deferral-validator", "conditional": true}
  ]
}
REGISTRY

# Phase state with NO subagents invoked (conditional should still pass)
cat > "$TMPDIR/phase-state.json" <<'STATE'
{
  "current_phase": "01",
  "subagents_invoked": {"01": []}
}
STATE

# --- Test 1: Conditional step with null subagent exits 0 ---
TASK_JSON='{"task_id":"t1","subject":"Step 01.5: Plan file check for resume","status":"completed"}'
EXIT_CODE=0
echo "$TASK_JSON" | REGISTRY_PATH="$TMPDIR/registry.json" PHASE_STATE_PATH="$TMPDIR/phase-state.json" bash "$HOOK_SCRIPT" 2>/dev/null || EXIT_CODE=$?
run_test "should_exit_0_for_conditional_null_subagent" "$EXIT_CODE"

# --- Test 2: Conditional step with named subagent but NOT invoked still exits 0 ---
cat > "$TMPDIR/phase-state-06.json" <<'STATE'
{
  "current_phase": "06",
  "subagents_invoked": {"06": []}
}
STATE
TASK_JSON='{"task_id":"t2","subject":"Step 06.1: deferral-validator if deferrals exist","status":"completed"}'
EXIT_CODE=0
echo "$TASK_JSON" | REGISTRY_PATH="$TMPDIR/registry.json" PHASE_STATE_PATH="$TMPDIR/phase-state-06.json" bash "$HOOK_SCRIPT" 2>/dev/null || EXIT_CODE=$?
run_test "should_exit_0_for_conditional_even_when_subagent_not_invoked" "$EXIT_CODE"

# --- Test 3: Conditional step with named subagent AND invoked still exits 0 ---
cat > "$TMPDIR/phase-state-06-invoked.json" <<'STATE'
{
  "current_phase": "06",
  "subagents_invoked": {"06": ["deferral-validator"]}
}
STATE
TASK_JSON='{"task_id":"t3","subject":"Step 06.1: deferral-validator if deferrals exist","status":"completed"}'
EXIT_CODE=0
echo "$TASK_JSON" | REGISTRY_PATH="$TMPDIR/registry.json" PHASE_STATE_PATH="$TMPDIR/phase-state-06-invoked.json" bash "$HOOK_SCRIPT" 2>/dev/null || EXIT_CODE=$?
run_test "should_exit_0_for_conditional_when_subagent_invoked" "$EXIT_CODE"

# --- Summary ---
echo ""
echo "Results: $PASSED passed, $FAILED failed"
[ "$FAILED" -eq 0 ] && exit 0 || exit 1
