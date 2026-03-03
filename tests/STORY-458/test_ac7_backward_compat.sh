#!/bin/bash
# Test: AC#7 - Backward compatibility maintained
# Story: STORY-458
# Generated: 2026-02-20
# Expected: FAIL (TDD Red phase - some frontmatter may change during refactoring)

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
echo "  AC#7: Backward Compatibility"
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

# Extract YAML frontmatter (between first two --- delimiters)
extract_frontmatter_field() {
    local file="$1"
    local field="$2"
    sed -n '/^---$/,/^---$/p' "$file" | grep "^${field}:" | head -1
}

# === Test 1: create-sprint.md description field preserved ===
SPRINT_DESC=$(extract_frontmatter_field "$CMD_SPRINT" "description")
test_result=0
if [ -n "$SPRINT_DESC" ]; then
    test_result=0
else
    test_result=1
fi
run_test "create-sprint.md has description field (${SPRINT_DESC:-MISSING})" "$test_result"

# === Test 2: create-sprint.md argument-hint preserved as [sprint-name] ===
SPRINT_HINT=$(extract_frontmatter_field "$CMD_SPRINT" "argument-hint")
test_result=0
if echo "$SPRINT_HINT" | grep -q 'sprint-name'; then
    test_result=0
else
    test_result=1
fi
run_test "create-sprint.md argument-hint contains [sprint-name] (${SPRINT_HINT:-MISSING})" "$test_result"

# === Test 3: recommendations-triage.md description field preserved ===
TRIAGE_DESC=$(extract_frontmatter_field "$CMD_TRIAGE" "description")
test_result=0
if [ -n "$TRIAGE_DESC" ]; then
    test_result=0
else
    test_result=1
fi
run_test "recommendations-triage.md has description field (${TRIAGE_DESC:-MISSING})" "$test_result"

# === Test 4: recommendations-triage.md argument-hint preserved ===
TRIAGE_HINT=$(extract_frontmatter_field "$CMD_TRIAGE" "argument-hint")
test_result=0
if [ -n "$TRIAGE_HINT" ]; then
    test_result=0
else
    test_result=1
fi
run_test "recommendations-triage.md has argument-hint field (${TRIAGE_HINT:-MISSING})" "$test_result"

# === Summary ===
echo ""
echo "----------------------------------------------"
echo "Results: $PASSED passed, $FAILED failed out of $TOTAL tests"
echo "----------------------------------------------"
[ "$FAILED" -eq 0 ] && exit 0 || exit 1
