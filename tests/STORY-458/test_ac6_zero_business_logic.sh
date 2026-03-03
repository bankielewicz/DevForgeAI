#!/bin/bash
# Test: AC#6 - Zero business logic in refactored commands
# Story: STORY-458
# Generated: 2026-02-20
# Expected: FAIL (TDD Red phase - commands still contain business logic)

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

check_forbidden_pattern() {
    local file="$1"
    local pattern="$2"
    local description="$3"
    local filename
    filename=$(basename "$file")

    local count
    count=$(grep -c "$pattern" "$file" 2>/dev/null || true)
    test_result=0
    if [ "$count" -eq 0 ]; then
        test_result=0
    else
        test_result=1
    fi
    run_test "${filename}: Zero matches for '${description}' (found: ${count})" "$test_result"
}

echo "=============================================="
echo "  AC#6: Zero Business Logic in Commands"
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

# === create-sprint.md forbidden patterns ===
echo "  --- create-sprint.md ---"
check_forbidden_pattern "$CMD_SPRINT" 'FOR ' "FOR loop constructs"
check_forbidden_pattern "$CMD_SPRINT" 'Task(' "Task() invocations"
check_forbidden_pattern "$CMD_SPRINT" 'Write(' "Write() operations"
check_forbidden_pattern "$CMD_SPRINT" 'Edit(' "Edit() operations"
check_forbidden_pattern "$CMD_SPRINT" 'SUM(\|total_points' "Inline capacity calculation"

echo ""
echo "  --- recommendations-triage.md ---"
# === recommendations-triage.md forbidden patterns ===
check_forbidden_pattern "$CMD_TRIAGE" 'FOR ' "FOR loop constructs"
check_forbidden_pattern "$CMD_TRIAGE" 'Task(' "Task() invocations"
check_forbidden_pattern "$CMD_TRIAGE" 'Write(' "Write() operations"
check_forbidden_pattern "$CMD_TRIAGE" 'Edit(' "Edit() operations"
check_forbidden_pattern "$CMD_TRIAGE" 'SUM(\|total_points' "Inline capacity calculation"

# === Summary ===
echo ""
echo "----------------------------------------------"
echo "Results: $PASSED passed, $FAILED failed out of $TOTAL tests"
echo "----------------------------------------------"
[ "$FAILED" -eq 0 ] && exit 0 || exit 1
