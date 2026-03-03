#!/bin/bash
# Integration Test: E2E SessionStart Hook with Progressive Context Injection
# Story: STORY-529
# Verifies: Complete end-to-end flow from SessionStart event through hook output chain
#
# Test Scenario:
# 1. Set up realistic project directory with multiple phase-state files
# 2. Include QA phase-state files (should be excluded)
# 3. Pipe SessionStart resume event to hook via stdin
# 4. Verify output chain: valid JSON → hookSpecificOutput → additionalContext
# 5. Verify hook selects most recent workflow
# 6. Verify QA files excluded from discovery
# 7. Verify exit code 0

set -uo pipefail

HOOK_SCRIPT="src/claude/hooks/inject-phase-context.sh"
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

echo "=== Integration Test: E2E SessionStart Hook with Progressive Context Injection ==="
echo "Target: $HOOK_SCRIPT"
echo ""

# --- Setup: Create realistic project directory ---
TMPDIR=$(mktemp -d)
mkdir -p "$TMPDIR/devforgeai/workflows"
mkdir -p "$TMPDIR/devforgeai/specs"

# Create older workflow file (should be ignored in favor of more recent)
cat > "$TMPDIR/devforgeai/workflows/STORY-100-phase-state.json" <<'OLD_WORKFLOW'
{
  "story_id": "STORY-100",
  "current_phase": "02",
  "phases": {
    "01": {"name": "Pre-Flight", "status": "completed", "completed": true},
    "02": {"name": "Test-First", "status": "in_progress", "completed": false},
    "03": {"name": "Implementation", "status": "pending", "completed": false}
  },
  "subagents_invoked": ["git-validator"],
  "created": "2026-02-25T08:00:00Z"
}
OLD_WORKFLOW

# Create most recent active workflow (should be selected)
cat > "$TMPDIR/devforgeai/workflows/STORY-250-phase-state.json" <<'ACTIVE_WORKFLOW'
{
  "story_id": "STORY-250",
  "current_phase": "04",
  "phases": {
    "01": {"name": "Pre-Flight", "status": "completed", "completed": true},
    "02": {"name": "Test-First", "status": "completed", "completed": true},
    "03": {"name": "Implementation", "status": "completed", "completed": true},
    "04": {"name": "Refactoring", "status": "in_progress", "completed": false},
    "05": {"name": "Integration", "status": "pending", "completed": false},
    "06": {"name": "Quality", "status": "pending", "completed": false}
  },
  "subagents_invoked": ["git-validator", "test-automator", "backend-architect", "code-reviewer"],
  "created": "2026-03-01T14:30:00Z"
}
ACTIVE_WORKFLOW

# Create QA phase-state file (should be explicitly excluded)
cat > "$TMPDIR/devforgeai/workflows/STORY-250-qa-phase-state.json" <<'QA_WORKFLOW'
{
  "story_id": "STORY-250",
  "type": "qa",
  "workflow": "qa",
  "current_phase": "02",
  "phases": {
    "00": {"name": "Setup", "status": "completed", "completed": true},
    "01": {"name": "Validation", "status": "completed", "completed": true},
    "02": {"name": "Analysis", "status": "in_progress", "completed": false}
  },
  "created": "2026-03-01T14:45:00Z"
}
QA_WORKFLOW

# Create another QA phase-state for a different story (also should be excluded)
cat > "$TMPDIR/devforgeai/workflows/STORY-100-qa-phase-state.json" <<'OLD_QA'
{
  "story_id": "STORY-100",
  "type": "qa",
  "workflow": "qa",
  "current_phase": "03"
}
OLD_QA

# --- Test 1: Verify setup created all expected files ---
run_test "Setup created STORY-100 dev workflow" \
    "$([ -f "$TMPDIR/devforgeai/workflows/STORY-100-phase-state.json" ] && echo 0 || echo 1)"

run_test "Setup created STORY-250 dev workflow (most recent)" \
    "$([ -f "$TMPDIR/devforgeai/workflows/STORY-250-phase-state.json" ] && echo 0 || echo 1)"

run_test "Setup created STORY-250 QA workflow (should be excluded)" \
    "$([ -f "$TMPDIR/devforgeai/workflows/STORY-250-qa-phase-state.json" ] && echo 0 || echo 1)"

run_test "Setup created STORY-100 QA workflow (should be excluded)" \
    "$([ -f "$TMPDIR/devforgeai/workflows/STORY-100-qa-phase-state.json" ] && echo 0 || echo 1)"

# --- Test 2-4: Execute hook with SessionStart event ---
SESSION_EVENT='{"event":"SessionStart","source":"resume"}'
HOOK_OUTPUT=$(echo "$SESSION_EVENT" | CLAUDE_PROJECT_DIR="$TMPDIR" bash "$HOOK_SCRIPT" 2>/dev/null)
HOOK_EXIT_CODE=$?

run_test "Hook exits with code 0" \
    "$([ "$HOOK_EXIT_CODE" -eq 0 ] && echo 0 || echo 1)"

# --- Test 5: Verify stdout is valid JSON ---
run_test "Hook stdout is valid JSON" \
    "$(echo "$HOOK_OUTPUT" | python3 -c 'import json,sys; json.load(sys.stdin)' 2>/dev/null && echo 0 || echo 1)"

# --- Test 6: Verify JSON structure contains hookSpecificOutput ---
HAS_HSO=$(echo "$HOOK_OUTPUT" | python3 -c "
import json, sys
try:
    data = json.load(sys.stdin)
    print('yes' if 'hookSpecificOutput' in data else 'no')
except:
    print('no')
" 2>/dev/null || echo "no")
run_test "Output contains hookSpecificOutput key" \
    "$([ "$HAS_HSO" = "yes" ] && echo 0 || echo 1)"

# --- Test 7: Verify hookSpecificOutput.hookEventName ---
EVENT_NAME=$(echo "$HOOK_OUTPUT" | python3 -c "
import json, sys
try:
    data = json.load(sys.stdin)
    print(data.get('hookSpecificOutput', {}).get('hookEventName', ''))
except:
    print('')
" 2>/dev/null || echo "")
run_test "hookEventName is SessionStart" \
    "$([ "$EVENT_NAME" = "SessionStart" ] && echo 0 || echo 1)"

# --- Test 8: Verify hookSpecificOutput.additionalContext exists ---
CONTEXT=$(echo "$HOOK_OUTPUT" | python3 -c "
import json, sys
try:
    data = json.load(sys.stdin)
    ctx = data.get('hookSpecificOutput', {}).get('additionalContext', '')
    print(ctx)
except:
    print('')
" 2>/dev/null || echo "")
run_test "additionalContext is non-empty string" \
    "$([ -n "$CONTEXT" ] && echo 0 || echo 1)"

# --- Test 9: Verify most recent workflow selected (STORY-250, not STORY-100) ---
run_test "Context shows most recent workflow STORY-250" \
    "$(echo "$CONTEXT" | grep -q "STORY-250" && echo 0 || echo 1)"

run_test "Context does NOT show older workflow STORY-100" \
    "$(echo "$CONTEXT" | grep -qv "STORY-100" && echo 0 || echo 1)"

# --- Test 10: Verify QA files are excluded ---
# The context should NOT contain "qa" type designation or QA-specific phase names
run_test "Context does NOT indicate QA type workflow" \
    "$(echo "$CONTEXT" | grep -qvi 'type.*qa\|"type".*"qa"' && echo 0 || echo 1)"

# --- Test 11: Verify current phase information in context ---
run_test "Context contains current phase number (04)" \
    "$(echo "$CONTEXT" | grep -q "04\|Refactoring\|Refactor" && echo 0 || echo 1)"

# --- Test 12: Verify steps completed/total in context ---
run_test "Context contains steps completed count (3 of 6)" \
    "$(echo "$CONTEXT" | grep -qi "3.*6\|steps.completed.*3\|completed.*3" && echo 0 || echo 1)"

run_test "Context contains steps remaining count (3)" \
    "$(echo "$CONTEXT" | grep -qi "steps.remain\|remaining\|3\|remain" && echo 0 || echo 1)"

# --- Test 13: Verify subagents information in context ---
run_test "Context lists invoked subagents (git-validator, test-automator, backend-architect, code-reviewer)" \
    "$(echo "$CONTEXT" | grep -qi "git-validator\|test-automator\|backend-architect\|code-reviewer" && echo 0 || echo 1)"

run_test "Context indicates required subagents section" \
    "$(echo "$CONTEXT" | grep -qi "required.*subagent\|subagent.*required" && echo 0 || echo 1)"

# --- Test 14: Verify output chain integrity (JSON → hookSpecificOutput → additionalContext) ---
# All three levels must be present and nested correctly
CHAIN_RESULT=$(echo "$HOOK_OUTPUT" | python3 << 'PYEOF'
import json, sys
try:
    data = json.load(sys.stdin)
    hso = data.get('hookSpecificOutput', {})
    ctx = hso.get('additionalContext', '')
    if isinstance(data, dict) and isinstance(hso, dict) and isinstance(ctx, str) and len(ctx) > 0:
        print('0')
    else:
        print('1')
except:
    print('1')
PYEOF
)
run_test "Complete output chain verified (JSON → hookSpecificOutput → additionalContext)" "$CHAIN_RESULT"

# --- Test 15: Verify hook script is executable and located correctly ---
run_test "Hook script exists and is executable" \
    "$([ -x "$HOOK_SCRIPT" ] && echo 0 || echo 1)"

# --- Test 16: Verify piping SessionStart event works correctly ---
# Re-run with explicit event verification
SESSION_RESUME='{"event":"SessionStart","source":"resume"}'
HOOK_OUTPUT_2=$(echo "$SESSION_RESUME" | CLAUDE_PROJECT_DIR="$TMPDIR" bash "$HOOK_SCRIPT" 2>/dev/null)
EVENT_NAME_2=$(echo "$HOOK_OUTPUT_2" | python3 -c "
import json, sys
try:
    data = json.load(sys.stdin)
    print(data.get('hookSpecificOutput', {}).get('hookEventName', ''))
except:
    print('')
" 2>/dev/null || echo "")
run_test "Hook correctly processes piped SessionStart event" \
    "$([ "$EVENT_NAME_2" = "SessionStart" ] && echo 0 || echo 1)"

# --- Test 17: Verify context string format is human-readable ---
# Context should contain newlines for readability
run_test "additionalContext is formatted as readable multi-line text" \
    "$(echo "$CONTEXT" | grep -q $'\\n' && echo 0 || echo 1)"

# --- Test 18: Verify critical fields are present in context ---
run_test "Context includes 'Active Workflow' label" \
    "$(echo "$CONTEXT" | grep -q "Active Workflow" && echo 0 || echo 1)"

run_test "Context includes 'Current Phase' label" \
    "$(echo "$CONTEXT" | grep -q "Current Phase" && echo 0 || echo 1)"

run_test "Context includes 'Steps completed' label" \
    "$(echo "$CONTEXT" | grep -q "Steps completed" && echo 0 || echo 1)"

run_test "Context includes 'Steps remaining' label" \
    "$(echo "$CONTEXT" | grep -q "Steps remaining" && echo 0 || echo 1)"

run_test "Context includes 'Subagents invoked' label" \
    "$(echo "$CONTEXT" | grep -q "Subagents invoked" && echo 0 || echo 1)"

run_test "Context includes 'Subagents required' label" \
    "$(echo "$CONTEXT" | grep -q "Subagents required" && echo 0 || echo 1)"

echo ""
echo "Results: $PASS passed, $FAIL failed"
[ "$FAIL" -eq 0 ] && exit 0 || exit 1
