#!/usr/bin/env bash
# STORY-400 AC#3: Phase 04 (Refactor) observation capture from refactoring-specialist
# TDD Red Phase - These tests MUST fail before implementation
# Verifies SKILL.md contains inline observation capture instructions after Phase 04

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

echo "=== AC#3: Phase 04 Observation Capture from refactoring-specialist ==="
echo ""

if [ ! -f "$SKILL_FILE" ]; then
    run_test "SKILL.md source file exists" 1
    echo "--- AC#3 Results: $PASS/$TOTAL passed, $FAIL failed ---"
    exit 1
fi

# Test 1: Phase 04 observation source set to refactoring-specialist
if grep -q 'source.*refactoring-specialist\|"source":.*"refactoring-specialist"' "$SKILL_FILE" 2>/dev/null; then
    run_test "Phase 04 observation source set to refactoring-specialist" 0
else
    run_test "Phase 04 observation source set to refactoring-specialist" 1
fi

# Test 2: Phase 04 observation capture sets phase field to "04"
if grep -q '"phase":.*"04"\|phase.*=.*"04"' "$SKILL_FILE" 2>/dev/null; then
    run_test "Phase 04 observation sets phase field to 04" 0
else
    run_test "Phase 04 observation sets phase field to 04" 1
fi

echo ""
echo "--- AC#3 Results: $PASS/$TOTAL passed, $FAIL failed ---"

if [ "$FAIL" -gt 0 ]; then
    exit 1
fi
exit 0
