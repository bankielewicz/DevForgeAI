#!/bin/bash
# Test: AC#5 - Blocks with Exit Code 2 When Required Subagent Missing
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

echo "=== AC#5: Blocks with Exit Code 2 When Required Subagent Missing ==="
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

cat > "$TMPDIR/registry.json" <<'REGISTRY'
{
  "steps": [
    {"id": "02.2", "check": "test-automator invoked", "subagent": "test-automator", "conditional": false},
    {"id": "04.1", "check": "refactoring-specialist invoked", "subagent": "refactoring-specialist", "conditional": false}
  ]
}
REGISTRY

# --- Test 1: Required subagent missing -> exit 2 ---
cat > "$TMPDIR/phase-state.json" <<'STATE'
{
  "current_phase": "02",
  "subagents_invoked": {"02": ["context-validator"]}
}
STATE
TASK_JSON='{"task_id":"t1","subject":"Step 02.2: test-automator invoked","status":"completed"}'
EXIT_CODE=0
STDERR_OUTPUT=$(echo "$TASK_JSON" | REGISTRY_PATH="$TMPDIR/registry.json" PHASE_STATE_PATH="$TMPDIR/phase-state.json" bash "$HOOK_SCRIPT" 2>&1 1>/dev/null) || EXIT_CODE=$?
if [ "$EXIT_CODE" -eq 2 ]; then
    run_test "should_exit_2_when_required_subagent_missing" 0
else
    run_test "should_exit_2_when_required_subagent_missing (got exit $EXIT_CODE, expected 2)" 1
fi

# --- Test 2: Stderr should contain step_id info ---
if echo "$STDERR_OUTPUT" | grep -q "02.2"; then
    run_test "should_log_step_id_to_stderr" 0
else
    run_test "should_log_step_id_to_stderr" 1
fi

# --- Test 3: Stderr should mention required subagent ---
if echo "$STDERR_OUTPUT" | grep -q "test-automator"; then
    run_test "should_log_required_subagent_to_stderr" 0
else
    run_test "should_log_required_subagent_to_stderr" 1
fi

# --- Test 4: Required subagent present -> exit 0 ---
cat > "$TMPDIR/phase-state-ok.json" <<'STATE'
{
  "current_phase": "02",
  "subagents_invoked": {"02": ["test-automator"]}
}
STATE
EXIT_CODE=0
echo "$TASK_JSON" | REGISTRY_PATH="$TMPDIR/registry.json" PHASE_STATE_PATH="$TMPDIR/phase-state-ok.json" bash "$HOOK_SCRIPT" 2>/dev/null || EXIT_CODE=$?
run_test "should_exit_0_when_required_subagent_present" "$EXIT_CODE"

# --- Test 5: Missing phase-state file -> exit 0 (error condition, not a violation) ---
EXIT_CODE=0
echo "$TASK_JSON" | REGISTRY_PATH="$TMPDIR/registry.json" PHASE_STATE_PATH="$TMPDIR/nonexistent.json" bash "$HOOK_SCRIPT" 2>/dev/null || EXIT_CODE=$?
run_test "should_exit_0_when_phase_state_missing" "$EXIT_CODE"

# --- Test 6: Phase has no subagents_invoked key -> exit 0 (error condition) ---
cat > "$TMPDIR/phase-state-no-key.json" <<'STATE'
{
  "current_phase": "04",
  "subagents_invoked": {}
}
STATE
TASK_JSON_04='{"task_id":"t6","subject":"Step 04.1: refactoring-specialist invoked","status":"completed"}'
EXIT_CODE=0
echo "$TASK_JSON_04" | REGISTRY_PATH="$TMPDIR/registry.json" PHASE_STATE_PATH="$TMPDIR/phase-state-no-key.json" bash "$HOOK_SCRIPT" 2>/dev/null || EXIT_CODE=$?
if [ "$EXIT_CODE" -eq 2 ]; then
    run_test "should_exit_2_when_phase_has_no_invocations_key" 0
else
    run_test "should_exit_2_when_phase_has_no_invocations_key (got exit $EXIT_CODE, expected 2)" 1
fi

# --- Summary ---
echo ""
echo "Results: $PASSED passed, $FAILED failed"
[ "$FAILED" -eq 0 ] && exit 0 || exit 1
