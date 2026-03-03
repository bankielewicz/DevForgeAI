#!/bin/bash
# Test: AC#3 - Hook Configuration in settings.json with Matcher
# Story: STORY-529
# Verifies: SessionStart event added with matcher, existing hooks unchanged, valid JSON

set -uo pipefail

SETTINGS_FILE="src/claude/settings.json"
PASS=0
FAIL=0

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

echo "=== AC#3: Hook Configuration in settings.json ==="
echo "Target: $SETTINGS_FILE"
echo ""

# --- Test 1: settings.json exists ---
run_test "settings.json exists at $SETTINGS_FILE" \
    "$([ -f "$SETTINGS_FILE" ] && echo 0 || echo 1)"

# --- Test 2: settings.json is valid JSON ---
run_test "settings.json is valid JSON" \
    "$(python3 -c "import json; json.load(open('$SETTINGS_FILE'))" 2>/dev/null && echo 0 || echo 1)"

# --- Test 3: hooks key exists ---
HAS_HOOKS=$(python3 -c "
import json
with open('$SETTINGS_FILE') as f:
    data = json.load(f)
print('yes' if 'hooks' in data else 'no')
" 2>/dev/null || echo "no")
run_test "settings.json contains hooks key" \
    "$([ "$HAS_HOOKS" = "yes" ] && echo 0 || echo 1)"

# --- Test 4: SessionStart event exists in hooks ---
HAS_SESSION=$(python3 -c "
import json
with open('$SETTINGS_FILE') as f:
    data = json.load(f)
hooks = data.get('hooks', {})
print('yes' if 'SessionStart' in hooks else 'no')
" 2>/dev/null || echo "no")
run_test "hooks contains SessionStart event" \
    "$([ "$HAS_SESSION" = "yes" ] && echo 0 || echo 1)"

# --- Test 5: SessionStart has an entry with matcher "resume|compact" ---
HAS_MATCHER=$(python3 -c "
import json
with open('$SETTINGS_FILE') as f:
    data = json.load(f)
hooks = data.get('hooks', {}).get('SessionStart', [])
for h in hooks:
    m = h.get('matcher', '')
    if 'resume' in m and 'compact' in m:
        print('yes')
        exit(0)
print('no')
" 2>/dev/null || echo "no")
run_test "SessionStart has matcher containing resume|compact" \
    "$([ "$HAS_MATCHER" = "yes" ] && echo 0 || echo 1)"

# --- Test 6: SessionStart entry references inject-phase-context.sh ---
HAS_COMMAND=$(python3 -c "
import json
with open('$SETTINGS_FILE') as f:
    data = json.load(f)
entries = data.get('hooks', {}).get('SessionStart', [])
for entry in entries:
    for h in entry.get('hooks', []):
        cmd = h.get('command', '')
        if 'inject-phase-context' in cmd:
            print('yes')
            exit(0)
print('no')
" 2>/dev/null || echo "no")
run_test "SessionStart entry references inject-phase-context.sh" \
    "$([ "$HAS_COMMAND" = "yes" ] && echo 0 || echo 1)"

# --- Test 7: Existing Stop hook still present (unchanged) ---
HAS_STOP=$(python3 -c "
import json
with open('$SETTINGS_FILE') as f:
    data = json.load(f)
hooks = data.get('hooks', {})
print('yes' if 'Stop' in hooks else 'no')
" 2>/dev/null || echo "no")
run_test "Existing Stop hook is still present (unchanged)" \
    "$([ "$HAS_STOP" = "yes" ] && echo 0 || echo 1)"

# --- Test 8: SessionStart is an array (supports multiple hooks) ---
IS_ARRAY=$(python3 -c "
import json
with open('$SETTINGS_FILE') as f:
    data = json.load(f)
ss = data.get('hooks', {}).get('SessionStart', None)
print('yes' if isinstance(ss, list) else 'no')
" 2>/dev/null || echo "no")
run_test "SessionStart value is an array" \
    "$([ "$IS_ARRAY" = "yes" ] && echo 0 || echo 1)"

echo ""
echo "Results: $PASS passed, $FAIL failed"
[ "$FAIL" -eq 0 ] && exit 0 || exit 1
