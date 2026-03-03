#!/bin/bash
# Test: AC#2 - Anthropic Prompt Engineering Patterns Applied
# Story: STORY-393
# Generated: 2026-02-12
# Target: src/claude/agents/requirements-analyst.md

set -uo pipefail

PASSED=0
FAILED=0
TARGET_FILE="/mnt/c/Projects/DevForgeAI2/src/claude/agents/requirements-analyst.md"

run_test() {
    local name="$1"
    local result="$2"
    if [ "$result" -eq 0 ]; then
        echo "  PASS: $name"
        PASSED=$((PASSED + 1))
    else
        echo "  FAIL: $name"
        FAILED=$((FAILED + 1))
    fi
}

echo "=== AC#2: Anthropic Prompt Engineering Patterns ==="
echo ""

if [ ! -f "$TARGET_FILE" ]; then
    echo "  FAIL: Target file does not exist: $TARGET_FILE"
    echo "Results: 0 passed, 1 failed"
    exit 1
fi

# === Test 1: Chain-of-thought reasoning in Workflow section ===
sed -n '/^## Workflow/,/^## /p' "$TARGET_FILE" | grep -qiE "(reasoning|think step|step-by-step|first.*then|reason about)" && run_test "Chain-of-thought reasoning in Workflow section" 0 || run_test "Chain-of-thought reasoning in Workflow section" 1

# === Test 2: Structured output in Output Format section ===
sed -n '/^## Output Format/,/^## /p' "$TARGET_FILE" | grep -qiE "(format|structure|template|schema|specification)" && run_test "Structured output specification in Output Format section" 0 || run_test "Structured output specification in Output Format section" 1

# === Test 3: At least 2 worked examples with Task() pattern ===
TASK_COUNT=$(grep -c 'Task(' "$TARGET_FILE" || echo "0")
[ "$TASK_COUNT" -ge 2 ] && run_test "At least 2 Task() invocation examples (count=$TASK_COUNT)" 0 || run_test "At least 2 Task() invocation examples (count=$TASK_COUNT)" 1

# === Test 4: Examples in Examples section specifically ===
sed -n '/^## Examples/,/^## /p' "$TARGET_FILE" | grep -q 'Task(' && run_test "Task() pattern appears within Examples section" 0 || run_test "Task() pattern appears within Examples section" 1

# === Test 5: Role/identity anchoring in Purpose section ===
sed -n '/^## Purpose/,/^## /p' "$TARGET_FILE" | grep -qiE "(you are|your role|specialist|expert|responsible for)" && run_test "Role/identity anchoring in Purpose section" 0 || run_test "Role/identity anchoring in Purpose section" 1

# === Test 6: DO list in Constraints section ===
sed -n '/^## Constraints and Boundaries/,/^## /p' "$TARGET_FILE" | grep -qE "^\*\*DO[:\*]|^DO:" && run_test "DO list in Constraints and Boundaries section" 0 || run_test "DO list in Constraints and Boundaries section" 1

# === Test 7: DO NOT list in Constraints section ===
sed -n '/^## Constraints and Boundaries/,/^## /p' "$TARGET_FILE" | grep -qiE "DO NOT|DON'T" && run_test "DO NOT list in Constraints and Boundaries section" 0 || run_test "DO NOT list in Constraints and Boundaries section" 1

# === Test 8: Given/When/Then in examples ===
sed -n '/^## Examples/,/^## /p' "$TARGET_FILE" | grep -qiE "(given|when|then)" && run_test "Given/When/Then BDD format in worked examples" 0 || run_test "Given/When/Then BDD format in worked examples" 1

# === Summary ===
echo ""
echo "Results: $PASSED passed, $FAILED failed"
[ "$FAILED" -eq 0 ] && exit 0 || exit 1
