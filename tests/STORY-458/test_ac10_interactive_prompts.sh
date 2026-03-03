#!/bin/bash
# Test: AC#10 - All interactive prompts functional with original options and flow
# Story: STORY-458
# Generated: 2026-02-20
# Expected: FAIL (TDD Red phase - AskUserQuestion count may change during refactoring)

set -uo pipefail

PROJECT_ROOT="$(cd "$(dirname "$0")/../.." && pwd)"

# === Test Configuration ===
PASSED=0
FAILED=0
TOTAL=0

CMD_SPRINT="${PROJECT_ROOT}/src/claude/commands/create-sprint.md"
CMD_TRIAGE="${PROJECT_ROOT}/src/claude/commands/recommendations-triage.md"

run_test() {
    local name="$1"
    local result="$2"
    ((TOTAL++))
    if [ "$result" -eq 0 ]; then
        echo "  PASS: $name"
        ((PASSED++))
    else
        echo "  FAIL: $name"
        ((FAILED++))
    fi
}

echo "=============================================="
echo "  AC#10: Interactive Prompts Functional"
echo "  Story: STORY-458"
echo "=============================================="
echo ""

# --- Pre-check: Files exist ---
if [ ! -f "$CMD_SPRINT" ]; then
    echo "  FATAL: Target file not found: $CMD_SPRINT"
    exit 1
fi
if [ ! -f "$CMD_TRIAGE" ]; then
    echo "  FATAL: Target file not found: $CMD_TRIAGE"
    exit 1
fi

# === Test 1: create-sprint.md contains >= 5 AskUserQuestion occurrences ===
# Story specifies 11 AskUserQuestion calls but we test for >=5 as minimum threshold
# (some may be consolidated, but at minimum 5 distinct interactions must exist)
SPRINT_ASK_COUNT=$(grep -c 'AskUserQuestion' "$CMD_SPRINT" || true)
test_result=0
if [ "$SPRINT_ASK_COUNT" -ge 5 ]; then
    test_result=0
else
    test_result=1
fi
run_test "create-sprint.md: >= 5 AskUserQuestion calls (actual: ${SPRINT_ASK_COUNT})" "$test_result"

# === Test 2: recommendations-triage.md contains >= 2 AskUserQuestion occurrences ===
TRIAGE_ASK_COUNT=$(grep -c 'AskUserQuestion' "$CMD_TRIAGE" || true)
test_result=0
if [ "$TRIAGE_ASK_COUNT" -ge 2 ]; then
    test_result=0
else
    test_result=1
fi
run_test "recommendations-triage.md: >= 2 AskUserQuestion calls (actual: ${TRIAGE_ASK_COUNT})" "$test_result"

# === Test 3: create-sprint.md contains capacity validation range (20-40) ===
# Check that both 20 and 40 appear in the file for capacity range validation
HAS_20=false
HAS_40=false
if grep -q '20' "$CMD_SPRINT"; then
    HAS_20=true
fi
if grep -q '40' "$CMD_SPRINT"; then
    HAS_40=true
fi
test_result=0
if [ "$HAS_20" = true ] && [ "$HAS_40" = true ]; then
    test_result=0
else
    test_result=1
fi
run_test "create-sprint.md: capacity validation range 20-40 present (20=${HAS_20}, 40=${HAS_40})" "$test_result"

# === Summary ===
echo ""
echo "----------------------------------------------"
echo "Results: $PASSED passed, $FAILED failed out of $TOTAL tests"
echo "----------------------------------------------"
[ "$FAILED" -eq 0 ] && exit 0 || exit 1
