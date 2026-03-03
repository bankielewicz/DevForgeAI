#!/bin/bash
# Test: AC#4 - No Regression in Existing Story Creation and Ideation Workflows
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

echo "=== AC#4: No Regression ==="
echo ""

if [ ! -f "$TARGET_FILE" ]; then
    echo "  FAIL: Target file does not exist: $TARGET_FILE"
    echo "Results: 0 passed, 1 failed"
    exit 1
fi

# === Test 1: YAML frontmatter valid (has --- delimiters) ===
HEAD_DELIM=$(head -1 "$TARGET_FILE")
[ "$HEAD_DELIM" = "---" ] && run_test "YAML frontmatter starts with --- delimiter" 0 || run_test "YAML frontmatter starts with --- delimiter" 1

# === Test 2: YAML frontmatter has name field ===
sed -n '1,/^---$/p' "$TARGET_FILE" | tail -n +2 | grep -q "^name:" && run_test "YAML frontmatter contains name field" 0 || run_test "YAML frontmatter contains name field" 1

# === Test 3: YAML frontmatter has tools field ===
sed -n '1,/^---$/p' "$TARGET_FILE" | tail -n +2 | grep -q "^tools:" && run_test "YAML frontmatter contains tools field" 0 || run_test "YAML frontmatter contains tools field" 1

# === Test 4: Tools field includes all 6 required tools ===
if grep -q "Read" "$TARGET_FILE" && grep -q "Write" "$TARGET_FILE" && grep -q "Edit" "$TARGET_FILE" && grep -q "Grep" "$TARGET_FILE" && grep -q "Glob" "$TARGET_FILE" && grep -q "AskUserQuestion" "$TARGET_FILE"; then
    run_test "Tools include Read, Write, Edit, Grep, Glob, AskUserQuestion" 0
else
    run_test "Tools include Read, Write, Edit, Grep, Glob, AskUserQuestion" 1
fi

# === Test 5-10: INVEST principles preserved ===
grep -qi "Independent" "$TARGET_FILE" && run_test "INVEST principle preserved: Independent" 0 || run_test "INVEST principle preserved: Independent" 1
grep -qi "Negotiable" "$TARGET_FILE" && run_test "INVEST principle preserved: Negotiable" 0 || run_test "INVEST principle preserved: Negotiable" 1
grep -qi "Valuable" "$TARGET_FILE" && run_test "INVEST principle preserved: Valuable" 0 || run_test "INVEST principle preserved: Valuable" 1
grep -qi "Estimable" "$TARGET_FILE" && run_test "INVEST principle preserved: Estimable" 0 || run_test "INVEST principle preserved: Estimable" 1
grep -qi "Small" "$TARGET_FILE" && run_test "INVEST principle preserved: Small" 0 || run_test "INVEST principle preserved: Small" 1
grep -qi "Testable" "$TARGET_FILE" && run_test "INVEST principle preserved: Testable" 0 || run_test "INVEST principle preserved: Testable" 1

# === Test 11: Given/When/Then BDD format preserved ===
if grep -qi "Given" "$TARGET_FILE" && grep -qi "When" "$TARGET_FILE" && grep -qi "Then" "$TARGET_FILE"; then
    run_test "Given/When/Then BDD format instructions preserved" 0
else
    run_test "Given/When/Then BDD format instructions preserved" 1
fi

# === Test 12: Story Format template preserved (As a/I want/So that) ===
grep -qiE "As a|I want|So that" "$TARGET_FILE" && run_test "Story Format template preserved (As a/I want/So that)" 0 || run_test "Story Format template preserved (As a/I want/So that)" 1

# === Test 13-17: Integration declarations ===
grep -q "devforgeai-orchestration" "$TARGET_FILE" && run_test "Integration declaration preserved: devforgeai-orchestration" 0 || run_test "Integration declaration preserved: devforgeai-orchestration" 1
grep -q "devforgeai-ideation" "$TARGET_FILE" && run_test "Integration declaration preserved: devforgeai-ideation" 0 || run_test "Integration declaration preserved: devforgeai-ideation" 1
grep -q "test-automator" "$TARGET_FILE" && run_test "Integration declaration preserved: test-automator" 0 || run_test "Integration declaration preserved: test-automator" 1
grep -q "backend-architect" "$TARGET_FILE" && run_test "Integration declaration preserved: backend-architect" 0 || run_test "Integration declaration preserved: backend-architect" 1
grep -q "api-designer" "$TARGET_FILE" && run_test "Integration declaration preserved: api-designer" 0 || run_test "Integration declaration preserved: api-designer" 1

# === Test 18: Error handling section preserved ===
grep -qiE "error handling|ambiguous requirements|story too large|insufficient" "$TARGET_FILE" && run_test "Error handling section preserved" 0 || run_test "Error handling section preserved" 1

# === Test 19: Token budget documented (< 30K) ===
grep -qiE "token|30.?K|budget" "$TARGET_FILE" && run_test "Token budget documented" 0 || run_test "Token budget documented" 1

# === Test 20: Story splitting techniques preserved ===
grep -qiE "split|splitting" "$TARGET_FILE" && run_test "Story splitting techniques preserved" 0 || run_test "Story splitting techniques preserved" 1

# === Test 21: Model field = opus ===
grep -q "model:.*opus" "$TARGET_FILE" && run_test "Model field set to opus (not Sonnet)" 0 || run_test "Model field set to opus (not Sonnet)" 1

# === Summary ===
echo ""
echo "Results: $PASSED passed, $FAILED failed"
[ "$FAILED" -eq 0 ] && exit 0 || exit 1
