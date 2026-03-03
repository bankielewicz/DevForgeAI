#!/usr/bin/env bash
# STORY-400 AC#5: Phase 09 framework-analyst reads accumulated observations
# TDD Red Phase - These tests MUST fail before implementation
# Verifies the SKILL.md documents that Phase 09 receives accumulated observations

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

echo "=== AC#5: Phase 09 framework-analyst Reads Accumulated Observations ==="
echo ""

if [ ! -f "$SKILL_FILE" ]; then
    run_test "SKILL.md source file exists" 1
    echo "--- AC#5 Results: $PASS/$TOTAL passed, $FAIL failed ---"
    exit 1
fi

# Test 1: SKILL.md mentions accumulated observations in context of Phase 09
if grep -q 'accumulated.*observations\|observations.*accumulated' "$SKILL_FILE" 2>/dev/null; then
    run_test "SKILL.md references accumulated observations" 0
else
    run_test "SKILL.md references accumulated observations" 1
fi

# Test 2: framework-analyst receives observations from phase-state.json
if grep -q 'framework-analyst.*observations\|observations.*framework-analyst' "$SKILL_FILE" 2>/dev/null; then
    run_test "framework-analyst linked to observations processing" 0
else
    run_test "framework-analyst linked to observations processing" 1
fi

# Test 3: Inline observation capture section exists in SKILL.md
if grep -qi 'Inline Observation Capture\|Observation Capture' "$SKILL_FILE" 2>/dev/null; then
    run_test "Inline Observation Capture section exists in SKILL.md" 0
else
    run_test "Inline Observation Capture section exists in SKILL.md" 1
fi

echo ""
echo "--- AC#5 Results: $PASS/$TOTAL passed, $FAIL failed ---"

if [ "$FAIL" -gt 0 ]; then
    exit 1
fi
exit 0
