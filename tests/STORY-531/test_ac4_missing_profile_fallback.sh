#!/bin/bash
# Test: AC#4 - Missing Adaptive Profile Fallback
# Story: STORY-531
# Generated: 2026-03-03

set -uo pipefail

PROJECT_ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
SKILL_FILE="$PROJECT_ROOT/src/claude/skills/planning-business/SKILL.md"

PASSED=0
FAILED=0

run_test() {
    local name="$1"
    local result="$2"
    if [ "$result" -eq 0 ]; then
        echo "  PASS: $name"
        PASSED=$((PASSED+1))
    else
        echo "  FAIL: $name"
        FAILED=$((FAILED+1))
    fi
}

echo "=== AC#4: Missing Adaptive Profile Fallback ==="

# Test 1: SKILL.md exists
test -f "$SKILL_FILE"; run_test "SKILL.md exists" $?

# Test 2: Documents fallback to intermediate
grep -qiE "(fallback|default).*intermediate" "$SKILL_FILE" 2>/dev/null; run_test "SKILL.md documents fallback to intermediate level" $?

# Test 3: Documents missing profile scenario
grep -qiE "(missing|no|absent|unavailable).*profile" "$SKILL_FILE" 2>/dev/null; run_test "SKILL.md documents missing profile scenario" $?

# Test 4: Warning logged for missing profile
grep -qiE "(warn|warning|log|alert).*missing.*profile" "$SKILL_FILE" 2>/dev/null; run_test "Warning documented for missing profile" $?

echo ""
echo "Results: $PASSED passed, $FAILED failed"
[ $FAILED -eq 0 ] && exit 0 || exit 1
