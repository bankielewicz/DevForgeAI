#!/usr/bin/env bash
# STORY-400 AC#1: Phase 02 (Red) observation capture from test-automator
# TDD Red Phase - These tests MUST fail before implementation
# Verifies SKILL.md contains inline observation capture instructions after Phase 02

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

echo "=== AC#1: Phase 02 Observation Capture from test-automator ==="
echo ""

# Test 1: SKILL.md source file exists
if [ -f "$SKILL_FILE" ]; then
    run_test "SKILL.md source file exists" 0
else
    run_test "SKILL.md source file exists" 1
    echo "--- AC#1 Results: $PASS/$TOTAL passed, $FAIL failed ---"
    exit 1
fi

# Test 2: Inline Observation Capture section/heading exists in SKILL.md
# This is the NEW section that must be added - not the existing subagent table
if grep -qi '## Inline Observation Capture\|## Observation Capture' "$SKILL_FILE" 2>/dev/null; then
    run_test "Inline Observation Capture section heading exists" 0
else
    run_test "Inline Observation Capture section heading exists" 1
fi

# Test 3: Observation capture instruction block references appending to observations array
if grep -q 'append.*observations\|observations.*append' "$SKILL_FILE" 2>/dev/null; then
    run_test "Observation capture mentions appending to observations array" 0
else
    run_test "Observation capture mentions appending to observations array" 1
fi

# Test 4: Phase 02 observation capture specifically references test-automator source
# Must match a pattern like: source.*test-automator in observation context (not subagent table)
if grep -q 'source.*test-automator\|"source":.*"test-automator"' "$SKILL_FILE" 2>/dev/null; then
    run_test "Phase 02 observation source set to test-automator" 0
else
    run_test "Phase 02 observation source set to test-automator" 1
fi

echo ""
echo "--- AC#1 Results: $PASS/$TOTAL passed, $FAIL failed ---"

if [ "$FAIL" -gt 0 ]; then
    exit 1
fi
exit 0
