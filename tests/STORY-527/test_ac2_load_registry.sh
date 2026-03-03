#!/bin/bash
# Test: AC#2 - Hook Loads Registry and Retrieves Required Subagent
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

echo "=== AC#2: Load Registry and Retrieve Required Subagent ==="
echo ""

# --- Pre-check: Hook script must exist ---
if [ ! -f "$HOOK_SCRIPT" ]; then
    echo "  FAIL: Hook script does not exist at $HOOK_SCRIPT"
    echo ""
    echo "Results: 0 passed, 1 failed (hook script missing - expected in RED phase)"
    exit 1
fi

TMPDIR=$(mktemp -d)
trap "rm -rf $TMPDIR" EXIT

# --- Test 1: Registry exists, step found, single subagent retrieved ---
cat > "$TMPDIR/registry.json" <<'REGISTRY'
{
  "steps": [
    {"id": "02.2", "check": "test-automator invoked", "subagent": "test-automator", "conditional": false}
  ]
}
REGISTRY
cat > "$TMPDIR/phase-state.json" <<'STATE'
{
  "current_phase": "02",
  "subagents_invoked": {"02": ["test-automator"]}
}
STATE

TASK_JSON='{"task_id":"t1","subject":"Step 02.2: test-automator invoked","status":"completed"}'
EXIT_CODE=0
echo "$TASK_JSON" | REGISTRY_PATH="$TMPDIR/registry.json" PHASE_STATE_PATH="$TMPDIR/phase-state.json" bash "$HOOK_SCRIPT" 2>/dev/null || EXIT_CODE=$?
run_test "should_retrieve_single_subagent_from_registry" "$EXIT_CODE"

# --- Test 2: Missing registry file should exit 0 ---
TASK_JSON='{"task_id":"t2","subject":"Step 02.2: test-automator invoked","status":"completed"}'
EXIT_CODE=0
echo "$TASK_JSON" | REGISTRY_PATH="$TMPDIR/nonexistent-registry.json" PHASE_STATE_PATH="$TMPDIR/phase-state.json" bash "$HOOK_SCRIPT" 2>/dev/null || EXIT_CODE=$?
run_test "should_exit_0_when_registry_missing" "$EXIT_CODE"

# --- Test 3: Unknown step_id should exit 0 ---
TASK_JSON='{"task_id":"t3","subject":"Step 99.9: unknown step","status":"completed"}'
EXIT_CODE=0
echo "$TASK_JSON" | REGISTRY_PATH="$TMPDIR/registry.json" PHASE_STATE_PATH="$TMPDIR/phase-state.json" bash "$HOOK_SCRIPT" 2>/dev/null || EXIT_CODE=$?
run_test "should_exit_0_for_unknown_step_id" "$EXIT_CODE"

# --- Test 4: Malformed JSON registry should exit 0 ---
echo "NOT VALID JSON {{{" > "$TMPDIR/bad-registry.json"
TASK_JSON='{"task_id":"t4","subject":"Step 02.2: test-automator invoked","status":"completed"}'
EXIT_CODE=0
echo "$TASK_JSON" | REGISTRY_PATH="$TMPDIR/bad-registry.json" PHASE_STATE_PATH="$TMPDIR/phase-state.json" bash "$HOOK_SCRIPT" 2>/dev/null || EXIT_CODE=$?
run_test "should_exit_0_for_malformed_registry_json" "$EXIT_CODE"

# --- Test 5: Step with null subagent should exit 0 ---
cat > "$TMPDIR/null-registry.json" <<'REGISTRY'
{
  "steps": [
    {"id": "01.5", "check": "Plan file check", "subagent": null, "conditional": true}
  ]
}
REGISTRY
TASK_JSON='{"task_id":"t5","subject":"Step 01.5: Plan file check","status":"completed"}'
EXIT_CODE=0
echo "$TASK_JSON" | REGISTRY_PATH="$TMPDIR/null-registry.json" PHASE_STATE_PATH="$TMPDIR/phase-state.json" bash "$HOOK_SCRIPT" 2>/dev/null || EXIT_CODE=$?
run_test "should_exit_0_for_null_subagent" "$EXIT_CODE"

# --- Summary ---
echo ""
echo "Results: $PASSED passed, $FAILED failed"
[ "$FAILED" -eq 0 ] && exit 0 || exit 1
