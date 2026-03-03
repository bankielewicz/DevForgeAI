#!/bin/bash
# Test: AC#3 - TaskUpdate Instruction for Step Completion
# Story: STORY-530
# Generated: 2026-03-03
#
# Validates that each phase file's Progressive Task Disclosure section
# includes TaskUpdate completion instructions with variable placeholders.

set -uo pipefail

PASSED=0
FAILED=0
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
PHASES_DIR="$PROJECT_ROOT/src/claude/skills/implementing-stories/phases"

run_test() {
    local name="$1"
    local result="$2"
    if [ "$result" -eq 0 ]; then
        echo "  PASS: $name"
        ((PASSED++))
    else
        echo "  FAIL: $name"
        ((FAILED++))
    fi
}

echo "=== AC#3: TaskUpdate Completion Instruction Tests ==="
echo ""

PHASE_FILES=(
    "phase-01-preflight.md"
    "phase-02-test-first.md"
    "phase-03-implementation.md"
    "phase-04-refactoring.md"
    "phase-04.5-ac-verification.md"
    "phase-05-integration.md"
    "phase-05.5-ac-verification.md"
    "phase-06-deferral.md"
    "phase-07-dod-update.md"
    "phase-08-git-workflow.md"
    "phase-09-feedback.md"
    "phase-10-result.md"
)

# Test 1: Each phase contains TaskUpdate in Progressive Task Disclosure section
echo "--- Test Group: TaskUpdate presence ---"
for file in "${PHASE_FILES[@]}"; do
    filepath="$PHASES_DIR/$file"

    if [ ! -f "$filepath" ]; then
        run_test "$file exists" 1
        continue
    fi

    section=$(sed -n '/^## Progressive Task Disclosure/,/^## /p' "$filepath" | head -n -1)

    echo "$section" | grep -q "TaskUpdate" 2>/dev/null
    run_test "$file contains TaskUpdate in section" $?
done

# Test 2: TaskUpdate includes status completed
echo ""
echo "--- Test Group: TaskUpdate completion status ---"
for file in "${PHASE_FILES[@]}"; do
    filepath="$PHASES_DIR/$file"
    [ ! -f "$filepath" ] && continue

    section=$(sed -n '/^## Progressive Task Disclosure/,/^## /p' "$filepath" | head -n -1)

    echo "$section" | grep -qi 'status.*completed\|completed.*status\|"completed"' 2>/dev/null
    run_test "$file TaskUpdate references completed status" $?
done

# Test 3: Variable placeholders present (e.g., ${TASK_ID}, ${STEP_ID}, taskId)
echo ""
echo "--- Test Group: Variable placeholders ---"
for file in "${PHASE_FILES[@]}"; do
    filepath="$PHASES_DIR/$file"
    [ ! -f "$filepath" ] && continue

    section=$(sed -n '/^## Progressive Task Disclosure/,/^## /p' "$filepath" | head -n -1)

    # Should contain variable placeholders like ${...} or taskId= or similar
    echo "$section" | grep -qE '\$\{.*\}|taskId|task_id' 2>/dev/null
    run_test "$file contains variable placeholders" $?
done

echo ""
echo "=== Results: $PASSED passed, $FAILED failed ==="
[ "$FAILED" -eq 0 ] && exit 0 || exit 1
