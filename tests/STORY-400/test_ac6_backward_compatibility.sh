#!/usr/bin/env bash
# STORY-400 AC#6: Backward compatibility with empty observations array
# TDD Red Phase - These tests MUST fail before implementation
# Verifies SKILL.md documents non-blocking capture and array initialization

set -uo pipefail

PROJECT_ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
SKILL_FILE="${PROJECT_ROOT}/src/claude/skills/devforgeai-development/SKILL.md"

PASS=0
FAIL=0
TOTAL=0

run_test() {
    local name="$1"
    local result="$2"
    TOTAL=$((TOTAL + 1))
    if [ "$result" -eq 0 ]; then
        PASS=$((PASS + 1))
        echo "  PASS: $name"
    else
        FAIL=$((FAIL + 1))
        echo "  FAIL: $name"
    fi
}

echo "=== AC#6: Backward Compatibility with Empty Observations Array ==="
echo ""

if [ ! -f "$SKILL_FILE" ]; then
    run_test "SKILL.md source file exists" 1
    echo "--- AC#6 Results: $PASS/$TOTAL passed, $FAIL failed ---"
    exit 1
fi

# Test 1: Non-blocking capture behavior documented
if grep -qi 'non-blocking\|non.blocking.*capture\|capture.*non.blocking\|not.*halt.*workflow\|workflow.*not.*halt' "$SKILL_FILE" 2>/dev/null; then
    run_test "Non-blocking capture behavior documented" 0
else
    run_test "Non-blocking capture behavior documented" 1
fi

# Test 2: Array initialization logic documented (initialize if absent)
if grep -qi 'initialize.*observations\|observations.*initialize\|observations.*absent\|absent.*observations\|create.*observations.*array' "$SKILL_FILE" 2>/dev/null; then
    run_test "Observations array initialization logic documented" 0
else
    run_test "Observations array initialization logic documented" 1
fi

# Test 3: Capture failure handling documented (log warning, proceed)
if grep -qi 'capture.*fail\|fail.*capture\|warning.*proceed\|graceful.*degradation\|log.*warning' "$SKILL_FILE" 2>/dev/null; then
    run_test "Capture failure handling documented (log and proceed)" 0
else
    run_test "Capture failure handling documented (log and proceed)" 1
fi

echo ""
echo "--- AC#6 Results: $PASS/$TOTAL passed, $FAIL failed ---"

if [ "$FAIL" -gt 0 ]; then
    exit 1
fi
exit 0
