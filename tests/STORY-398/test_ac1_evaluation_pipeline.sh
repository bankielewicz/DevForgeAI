#!/bin/bash
# Test: AC#1 - Evaluation Pipeline Run on Representative Sample
# Story: STORY-398
# Generated: 2026-02-13

set -euo pipefail

# === Test Configuration ===
PASSED=0
FAILED=0
PROJECT_ROOT="/mnt/c/Projects/DevForgeAI2"
TARGET_FILE="${PROJECT_ROOT}/devforgeai/feedback/ai-analysis/STORY-398/evaluation-results.json"

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

echo "=== AC#1: Evaluation Pipeline Run on Representative Sample ==="
echo ""

# --- Arrange ---
# Target: evaluation-results.json at documented path

# --- Act & Assert ---

# Test 1: evaluation-results.json file exists
test -f "$TARGET_FILE"
run_test "evaluation-results.json exists" $?

# Test 2: File contains template_conformance field
grep -q '"template_conformance"' "$TARGET_FILE"
run_test "Contains template_conformance field" $?

# Test 3: File contains quality_metrics field
grep -q '"quality_metrics"' "$TARGET_FILE"
run_test "Contains quality_metrics field" $?

# Test 4: File contains zero critical errors indicator
grep -q '"critical_errors"' "$TARGET_FILE"
run_test "Contains critical_errors field" $?

# Test 5: Sample includes at least 5 agents
AGENT_COUNT=$(grep -o '"type"[[:space:]]*:[[:space:]]*"agent"' "$TARGET_FILE" | wc -l)
[ "$AGENT_COUNT" -ge 5 ]
run_test "Sample includes 5+ agents (found: $AGENT_COUNT)" $?

# Test 6: Sample includes at least 3 skills
SKILL_COUNT=$(grep -o '"type"[[:space:]]*:[[:space:]]*"skill"' "$TARGET_FILE" | wc -l)
[ "$SKILL_COUNT" -ge 3 ]
run_test "Sample includes 3+ skills (found: $SKILL_COUNT)" $?

# Test 7: Sample includes at least 3 commands
CMD_COUNT=$(grep -o '"type"[[:space:]]*:[[:space:]]*"command"' "$TARGET_FILE" | wc -l)
[ "$CMD_COUNT" -ge 3 ]
run_test "Sample includes 3+ commands (found: $CMD_COUNT)" $?

# Test 8: Template conformance score is 100%
grep -qE '"template_conformance"[[:space:]]*:[[:space:]]*100' "$TARGET_FILE"
run_test "Template conformance score equals 100%" $?

# Test 9: Valid JSON format
python3 -c "import json; json.load(open('$TARGET_FILE'))" 2>/dev/null
run_test "File is valid JSON" $?

# === Summary ===
echo ""
echo "Results: $PASSED passed, $FAILED failed"
[ "$FAILED" -eq 0 ] && exit 0 || exit 1
