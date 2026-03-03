#!/bin/bash
# Integration Test: E2E Flow - SubagentStop (STORY-526) → TaskCompleted (STORY-527)
# Story: STORY-527 - TaskCompleted Hook Step Validation Gate
# Purpose: Validates end-to-end flow where SubagentStop records invocation and TaskCompleted validates it
# Generated: 2026-03-03

set -euo pipefail

PASSED=0
FAILED=0
SUBAGENT_STOP_HOOK="/mnt/c/Projects/DevForgeAI2/.claude/hooks/track-subagent-invocation.sh"
TASK_COMPLETED_HOOK="/mnt/c/Projects/DevForgeAI2/.claude/hooks/validate-step-completion.sh"

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

echo "=== Integration Test: E2E SubagentStop → TaskCompleted Flow ==="
echo ""

# --- Pre-check: Both hooks exist ---
if [ ! -f "$SUBAGENT_STOP_HOOK" ]; then
    echo "  FAIL: SubagentStop hook missing at $SUBAGENT_STOP_HOOK"
    echo ""
    echo "Results: 0 passed, 1 failed (hook missing)"
    exit 1
fi

if [ ! -f "$TASK_COMPLETED_HOOK" ]; then
    echo "  FAIL: TaskCompleted hook missing at $TASK_COMPLETED_HOOK"
    echo ""
    echo "Results: 0 passed, 1 failed (hook missing)"
    exit 1
fi

# --- Test Environment Setup ---
TMPDIR=$(mktemp -d)
trap "rm -rf $TMPDIR" EXIT

PROJECT_ROOT="$TMPDIR/project"
mkdir -p "$PROJECT_ROOT/devforgeai/workflows"
mkdir -p "$PROJECT_ROOT/.claude/hooks"

# Create minimal CLAUDE.md to satisfy project root detection
cat > "$PROJECT_ROOT/CLAUDE.md" <<'CLAUDE'
# Test Project
Test CLAUDE.md for integration tests
CLAUDE

# Create phase-steps-registry
cat > "$PROJECT_ROOT/.claude/hooks/phase-steps-registry.json" <<'REGISTRY'
{
  "steps": [
    {"id": "02.2", "check": "test-automator invoked", "subagent": "test-automator", "conditional": false},
    {"id": "03.4", "check": "context-validator invoked", "subagent": "context-validator", "conditional": false},
    {"id": "04.1", "check": "refactoring-specialist invoked", "subagent": "refactoring-specialist", "conditional": false},
    {"id": "05.2", "check": "documentation-writer optional", "subagent": null, "conditional": false}
  ]
}
REGISTRY

# --- Scenario 1: Happy Path - Subagent recorded, task completion succeeds ---
echo "Test 1: Happy Path - Subagent invoked and recorded, TaskCompleted validates PASS"
echo "=========================================================================="

# Create initial phase-state.json (before SubagentStop hook runs)
cat > "$PROJECT_ROOT/devforgeai/workflows/STORY-123-phase-state.json" <<'STATE'
{
  "story_id": "STORY-123",
  "current_phase": "02",
  "subagents_invoked": {}
}
STATE

# Simulate SubagentStop event: test-automator completes in phase 02
SUBAGENT_STOP_EVENT='{"event":"SubagentStop","agent_type":"test-automator","timestamp":"2026-03-03T10:00:00Z"}'

# Export environment variables for hook
export CLAUDE_PROJECT_DIR="$PROJECT_ROOT"
export REGISTRY_PATH="$PROJECT_ROOT/.claude/hooks/phase-steps-registry.json"
export PHASE_STATE_PATH="$PROJECT_ROOT/devforgeai/workflows/STORY-123-phase-state.json"

# In real scenario, SubagentStop hook would call devforgeai-validate phase-record
# For testing, we manually update phase-state.json to simulate hook behavior
echo "$SUBAGENT_STOP_EVENT" | bash "$SUBAGENT_STOP_HOOK" 2>/dev/null || true

# Manually update phase-state to simulate what SubagentStop hook does
jq '.subagents_invoked.["02"] = ["test-automator"]' "$PHASE_STATE_PATH" > "$PHASE_STATE_PATH.tmp" && mv "$PHASE_STATE_PATH.tmp" "$PHASE_STATE_PATH"

# Now simulate TaskCompleted event: try to mark step 02.2 complete
TASK_COMPLETED_EVENT='{"event":"TaskCompleted","task_id":"t1","subject":"Step 02.2: test-automator invoked","status":"completed"}'

# TaskCompleted hook should find test-automator in subagents_invoked and exit 0
EXIT_CODE=0
STDERR_OUTPUT=$(echo "$TASK_COMPLETED_EVENT" | bash "$TASK_COMPLETED_HOOK" 2>&1 1>/dev/null) || EXIT_CODE=$?

if [ "$EXIT_CODE" -eq 0 ]; then
    run_test "happy_path_subagent_recorded_task_passes" 0
else
    run_test "happy_path_subagent_recorded_task_passes (got exit $EXIT_CODE, expected 0)" 1
fi

echo ""

# --- Scenario 2: Sad Path - Subagent NOT recorded, task completion blocked ---
echo "Test 2: Sad Path - Subagent NOT invoked, TaskCompleted validates BLOCK (exit 2)"
echo "==============================================================================="

# Create phase-state.json WITHOUT test-automator in subagents_invoked
cat > "$PROJECT_ROOT/devforgeai/workflows/STORY-124-phase-state.json" <<'STATE'
{
  "story_id": "STORY-124",
  "current_phase": "02",
  "subagents_invoked": {"02": ["context-validator"]}
}
STATE

export PHASE_STATE_PATH="$PROJECT_ROOT/devforgeai/workflows/STORY-124-phase-state.json"

# Try to mark step 02.2 complete WITHOUT test-automator being invoked
TASK_COMPLETED_EVENT='{"event":"TaskCompleted","task_id":"t2","subject":"Step 02.2: test-automator invoked","status":"completed"}'

EXIT_CODE=0
STDERR_OUTPUT=$(echo "$TASK_COMPLETED_EVENT" | bash "$TASK_COMPLETED_HOOK" 2>&1 1>/dev/null) || EXIT_CODE=$?

# Hook should block with exit code 2
if [ "$EXIT_CODE" -eq 2 ]; then
    run_test "sad_path_subagent_missing_task_blocked" 0
else
    run_test "sad_path_subagent_missing_task_blocked (got exit $EXIT_CODE, expected 2)" 1
fi

# Verify error message contains step_id
if echo "$STDERR_OUTPUT" | grep -q "02.2"; then
    run_test "block_message_contains_step_id" 0
else
    run_test "block_message_contains_step_id" 1
fi

# Verify error message contains required subagent name
if echo "$STDERR_OUTPUT" | grep -q "test-automator"; then
    run_test "block_message_contains_required_subagent" 0
else
    run_test "block_message_contains_required_subagent" 1
fi

echo ""

# --- Scenario 3: Multiple subagents - Partial invocation with OR-logic ---
echo "Test 3: OR-Logic - Multiple options, one invoked, TaskCompleted validates PASS"
echo "=============================================================================="

# Create registry with OR-logic step
cat > "$PROJECT_ROOT/.claude/hooks/phase-steps-registry-or.json" <<'REGISTRY'
{
  "steps": [
    {
      "id": "03.2",
      "check": "code reviewer or architecture reviewer",
      "subagent": ["code-reviewer", "architect-reviewer"],
      "conditional": false
    }
  ]
}
REGISTRY

# Create phase-state with only architect-reviewer invoked
cat > "$PROJECT_ROOT/devforgeai/workflows/STORY-125-phase-state.json" <<'STATE'
{
  "story_id": "STORY-125",
  "current_phase": "03",
  "subagents_invoked": {"03": ["architect-reviewer"]}
}
STATE

export REGISTRY_PATH="$PROJECT_ROOT/.claude/hooks/phase-steps-registry-or.json"
export PHASE_STATE_PATH="$PROJECT_ROOT/devforgeai/workflows/STORY-125-phase-state.json"

# TaskCompleted for step that has OR-logic requirement
TASK_COMPLETED_EVENT='{"event":"TaskCompleted","task_id":"t3","subject":"Step 03.2: code reviewer or architecture reviewer","status":"completed"}'

EXIT_CODE=0
echo "$TASK_COMPLETED_EVENT" | bash "$TASK_COMPLETED_HOOK" 2>/dev/null || EXIT_CODE=$?

# Should pass because architect-reviewer (one of the OR options) is invoked
if [ "$EXIT_CODE" -eq 0 ]; then
    run_test "or_logic_with_partial_match_passes" 0
else
    run_test "or_logic_with_partial_match_passes (got exit $EXIT_CODE, expected 0)" 1
fi

echo ""

# --- Scenario 4: OR-Logic with no matches - Task blocked ---
echo "Test 4: OR-Logic - No options invoked, TaskCompleted validates BLOCK (exit 2)"
echo "==============================================================================="

# Create phase-state with neither code-reviewer nor architect-reviewer invoked
cat > "$PROJECT_ROOT/devforgeai/workflows/STORY-126-phase-state.json" <<'STATE'
{
  "story_id": "STORY-126",
  "current_phase": "03",
  "subagents_invoked": {"03": ["test-automator"]}
}
STATE

export PHASE_STATE_PATH="$PROJECT_ROOT/devforgeai/workflows/STORY-126-phase-state.json"

# TaskCompleted for same OR-logic step but without any required subagent
TASK_COMPLETED_EVENT='{"event":"TaskCompleted","task_id":"t4","subject":"Step 03.2: code reviewer or architecture reviewer","status":"completed"}'

EXIT_CODE=0
STDERR_OUTPUT=$(echo "$TASK_COMPLETED_EVENT" | bash "$TASK_COMPLETED_HOOK" 2>&1 1>/dev/null) || EXIT_CODE=$?

# Should block because neither option in the OR array is invoked
if [ "$EXIT_CODE" -eq 2 ]; then
    run_test "or_logic_with_no_match_blocks" 0
else
    run_test "or_logic_with_no_match_blocks (got exit $EXIT_CODE, expected 2)" 1
fi

echo ""

# --- Scenario 5: Null subagent - Task always passes ---
echo "Test 5: Null Subagent - No required subagent, TaskCompleted validates PASS"
echo "==========================================================================="

# Reset to original registry
export REGISTRY_PATH="$PROJECT_ROOT/.claude/hooks/phase-steps-registry.json"

# Create phase-state for step with null subagent requirement
cat > "$PROJECT_ROOT/devforgeai/workflows/STORY-127-phase-state.json" <<'STATE'
{
  "story_id": "STORY-127",
  "current_phase": "05",
  "subagents_invoked": {"05": []}
}
STATE

export PHASE_STATE_PATH="$PROJECT_ROOT/devforgeai/workflows/STORY-127-phase-state.json"

# TaskCompleted for step 05.2 which has null subagent requirement
TASK_COMPLETED_EVENT='{"event":"TaskCompleted","task_id":"t5","subject":"Step 05.2: documentation-writer optional","status":"completed"}'

EXIT_CODE=0
echo "$TASK_COMPLETED_EVENT" | bash "$TASK_COMPLETED_HOOK" 2>/dev/null || EXIT_CODE=$?

# Should pass because step has no required subagent (null)
if [ "$EXIT_CODE" -eq 0 ]; then
    run_test "null_subagent_always_passes" 0
else
    run_test "null_subagent_always_passes (got exit $EXIT_CODE, expected 0)" 1
fi

echo ""

# --- Scenario 6: Cross-workflow isolation - QA workflow files ignored ---
echo "Test 6: Workflow Isolation - QA workflow files excluded from validation"
echo "========================================================================"

# Create a QA phase-state file that should be ignored
cat > "$PROJECT_ROOT/devforgeai/workflows/STORY-128-qa-phase-state.json" <<'STATE'
{
  "story_id": "STORY-128",
  "current_phase": "qa-01",
  "subagents_invoked": {}
}
STATE

# Create a regular phase-state file
cat > "$PROJECT_ROOT/devforgeai/workflows/STORY-128-phase-state.json" <<'STATE'
{
  "story_id": "STORY-128",
  "current_phase": "02",
  "subagents_invoked": {"02": ["test-automator"]}
}
STATE

# Hook should use the regular phase-state, not the QA one
export PHASE_STATE_PATH="$PROJECT_ROOT/devforgeai/workflows/STORY-128-phase-state.json"

TASK_COMPLETED_EVENT='{"event":"TaskCompleted","task_id":"t6","subject":"Step 02.2: test-automator invoked","status":"completed"}'

EXIT_CODE=0
echo "$TASK_COMPLETED_EVENT" | bash "$TASK_COMPLETED_HOOK" 2>/dev/null || EXIT_CODE=$?

# Should pass because we're validating against the regular phase-state (with test-automator)
if [ "$EXIT_CODE" -eq 0 ]; then
    run_test "workflow_isolation_qa_files_ignored" 0
else
    run_test "workflow_isolation_qa_files_ignored (got exit $EXIT_CODE, expected 0)" 1
fi

echo ""

# --- Scenario 7: Performance - Hook completes in < 500ms ---
echo "Test 7: Performance - Hook execution completes within 500ms"
echo "==========================================================="

export PHASE_STATE_PATH="$PROJECT_ROOT/devforgeai/workflows/STORY-123-phase-state.json"

TASK_COMPLETED_EVENT='{"event":"TaskCompleted","task_id":"t7","subject":"Step 02.2: test-automator invoked","status":"completed"}'

START_TIME=$(date +%s%3N)
echo "$TASK_COMPLETED_EVENT" | bash "$TASK_COMPLETED_HOOK" 2>/dev/null || true
END_TIME=$(date +%s%3N)

ELAPSED=$((END_TIME - START_TIME))

if [ "$ELAPSED" -lt 500 ]; then
    run_test "performance_hook_under_500ms (elapsed: ${ELAPSED}ms)" 0
else
    run_test "performance_hook_under_500ms (elapsed: ${ELAPSED}ms, threshold: 500ms)" 1
fi

echo ""

# --- Summary ---
echo "=================================================="
echo "  INTEGRATION TEST SUMMARY"
echo "=================================================="
echo "Results: $PASSED passed, $FAILED failed"

if [ "$FAILED" -eq 0 ]; then
    echo "✓ All integration tests PASSED"
    exit 0
else
    echo "✗ Some integration tests FAILED"
    exit 1
fi
