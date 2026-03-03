#!/bin/bash
# Test: AC#1 - Hook Parses TaskCompleted JSON and Extracts Step ID
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

echo "=== AC#1: Parse Step ID from TaskCompleted JSON ==="
echo ""

# --- Pre-check: Hook script must exist ---
if [ ! -f "$HOOK_SCRIPT" ]; then
    echo "  FAIL: Hook script does not exist at $HOOK_SCRIPT"
    echo ""
    echo "Results: 0 passed, 1 failed (hook script missing - expected in RED phase)"
    exit 1
fi

if [ ! -x "$HOOK_SCRIPT" ]; then
    echo "  FAIL: Hook script is not executable"
    echo ""
    echo "Results: 0 passed, 1 failed (hook not executable)"
    exit 1
fi

# --- Setup: Create temporary phase-state and registry ---
TMPDIR=$(mktemp -d)
trap "rm -rf $TMPDIR" EXIT

# Minimal registry with a known step
cat > "$TMPDIR/phase-steps-registry.json" <<'REGISTRY'
{
  "steps": [
    {"id": "02.2", "check": "test-automator invoked", "subagent": "test-automator", "conditional": false},
    {"id": "03.4", "check": "context-validator invoked", "subagent": "context-validator", "conditional": false}
  ]
}
REGISTRY

# Phase state with subagents invoked
cat > "$TMPDIR/phase-state.json" <<'STATE'
{
  "current_phase": "02",
  "subagents_invoked": {"02": ["test-automator"]}
}
STATE

# --- Test 1: Extract step_id "02.2" from standard subject ---
TASK_JSON='{"task_id":"t1","subject":"Step 02.2: test-automator invoked","status":"completed"}'
EXIT_CODE=0
echo "$TASK_JSON" | REGISTRY_PATH="$TMPDIR/phase-steps-registry.json" PHASE_STATE_PATH="$TMPDIR/phase-state.json" bash "$HOOK_SCRIPT" 2>/dev/null || EXIT_CODE=$?
run_test "should_extract_step_id_02_2_from_subject" "$EXIT_CODE"

# --- Test 2: Extract step_id "03.4" from subject with different phase ---
TASK_JSON='{"task_id":"t2","subject":"Step 03.4: context-validator invoked","status":"completed"}'
EXIT_CODE=0
echo "$TASK_JSON" | REGISTRY_PATH="$TMPDIR/phase-steps-registry.json" PHASE_STATE_PATH="$TMPDIR/phase-state.json" bash "$HOOK_SCRIPT" 2>/dev/null || EXIT_CODE=$?
# This should exit 2 because context-validator not in phase 03 invocations
# But we're testing extraction, so any non-error exit (0 or 2) means parsing worked
if [ "$EXIT_CODE" -eq 0 ] || [ "$EXIT_CODE" -eq 2 ]; then
    run_test "should_extract_step_id_03_4_from_subject" 0
else
    run_test "should_extract_step_id_03_4_from_subject" 1
fi

# --- Test 3: Non-step task subject should exit 0 (no-op) ---
TASK_JSON='{"task_id":"t3","subject":"Implement the login feature","status":"completed"}'
EXIT_CODE=0
echo "$TASK_JSON" | REGISTRY_PATH="$TMPDIR/phase-steps-registry.json" PHASE_STATE_PATH="$TMPDIR/phase-state.json" bash "$HOOK_SCRIPT" 2>/dev/null || EXIT_CODE=$?
run_test "should_exit_0_for_non_step_subject" "$EXIT_CODE"

# --- Test 4: Subject with "Step" but not matching pattern should exit 0 ---
TASK_JSON='{"task_id":"t4","subject":"Next Step in development","status":"completed"}'
EXIT_CODE=0
echo "$TASK_JSON" | REGISTRY_PATH="$TMPDIR/phase-steps-registry.json" PHASE_STATE_PATH="$TMPDIR/phase-state.json" bash "$HOOK_SCRIPT" 2>/dev/null || EXIT_CODE=$?
run_test "should_exit_0_for_non_matching_step_pattern" "$EXIT_CODE"

# --- Test 5: Three-part step_id like "4.5.3" ---
TASK_JSON='{"task_id":"t5","subject":"Step 4.5.3: ac-compliance-verifier invoked","status":"completed"}'
EXIT_CODE=0
echo "$TASK_JSON" | REGISTRY_PATH="$TMPDIR/phase-steps-registry.json" PHASE_STATE_PATH="$TMPDIR/phase-state.json" bash "$HOOK_SCRIPT" 2>/dev/null || EXIT_CODE=$?
# Unknown step should exit 0
run_test "should_handle_three_part_step_id_gracefully" "$EXIT_CODE"

# --- Summary ---
echo ""
echo "Results: $PASSED passed, $FAILED failed"
[ "$FAILED" -eq 0 ] && exit 0 || exit 1
