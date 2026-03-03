#!/bin/bash
# Test: Edge Case - Malformed JSON
# Story: STORY-528
# Verifies: Hook exits 0 (graceful degradation) on malformed phase-state

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

echo "=== Edge Case: Malformed JSON ==="
echo "Target: $HOOK_SCRIPT"
echo ""

run_test "Hook script exists at $HOOK_SCRIPT" \
    "$([ -f "$HOOK_SCRIPT" ] && echo 0 || echo 1)"

TMPDIR=$(mktemp -d)
mkdir -p "$TMPDIR/devforgeai/workflows"

# Malformed JSON phase-state
echo "{ this is not valid json !!!" > "$TMPDIR/devforgeai/workflows/STORY-666-phase-state.json"

STOP_EVENT='{"event":"Stop","reason":"user_request"}'

echo "$STOP_EVENT" | CLAUDE_PROJECT_DIR="$TMPDIR" bash "$HOOK_SCRIPT" 2>/dev/null
EXIT_CODE=$?

run_test "Hook exits 0 on malformed phase-state JSON (graceful degradation)" \
    "$([ "$EXIT_CODE" -eq 0 ] && echo 0 || echo 1)"

echo ""
echo "Results: $PASS passed, $FAIL failed"
[ "$FAIL" -eq 0 ] && exit 0 || exit 1
