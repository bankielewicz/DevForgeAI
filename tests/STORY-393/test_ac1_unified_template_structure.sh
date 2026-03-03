#!/bin/bash
# Test: AC#1 - Requirements-Analyst System Prompt Updated to Unified Template Structure
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

echo "=== AC#1: Unified Template Structure ==="
echo ""

# === Verify file exists ===
if [ ! -f "$TARGET_FILE" ]; then
    echo "  FAIL: Target file does not exist: $TARGET_FILE"
    echo "Results: 0 passed, 1 failed"
    exit 1
fi

# === Test 1: YAML Frontmatter present ===
grep -q "^---" "$TARGET_FILE" && run_test "YAML Frontmatter delimiters present" 0 || run_test "YAML Frontmatter delimiters present" 1

# === Test 2: Title H1 present ===
grep -qE "^# " "$TARGET_FILE" && run_test "Title H1 heading present" 0 || run_test "Title H1 heading present" 1

# === Test 3: Purpose section present ===
grep -q "^## Purpose" "$TARGET_FILE" && run_test "Purpose section (H2) present" 0 || run_test "Purpose section (H2) present" 1

# === Test 4: When Invoked section present ===
grep -q "^## When Invoked" "$TARGET_FILE" && run_test "When Invoked section (H2) present" 0 || run_test "When Invoked section (H2) present" 1

# === Test 5: Input/Output Specification section present ===
grep -q "^## Input/Output Specification" "$TARGET_FILE" && run_test "Input/Output Specification section (H2) present" 0 || run_test "Input/Output Specification section (H2) present" 1

# === Test 6: Constraints and Boundaries section present ===
grep -q "^## Constraints and Boundaries" "$TARGET_FILE" && run_test "Constraints and Boundaries section (H2) present" 0 || run_test "Constraints and Boundaries section (H2) present" 1

# === Test 7: Workflow section present ===
grep -q "^## Workflow" "$TARGET_FILE" && run_test "Workflow section (H2) present" 0 || run_test "Workflow section (H2) present" 1

# === Test 8: Success Criteria section present ===
grep -q "^## Success Criteria" "$TARGET_FILE" && run_test "Success Criteria section (H2) present" 0 || run_test "Success Criteria section (H2) present" 1

# === Test 9: Output Format section present ===
grep -q "^## Output Format" "$TARGET_FILE" && run_test "Output Format section (H2) present" 0 || run_test "Output Format section (H2) present" 1

# === Test 10: Examples section present ===
grep -q "^## Examples" "$TARGET_FILE" && run_test "Examples section (H2) present" 0 || run_test "Examples section (H2) present" 1

# === Test 11: All 10 required sections counted ===
SECTION_COUNT=$(grep -cE "^## (Purpose|When Invoked|Input/Output Specification|Constraints and Boundaries|Workflow|Success Criteria|Output Format|Examples)" "$TARGET_FILE" || echo "0")
[ "$SECTION_COUNT" -ge 8 ] && run_test "At least 8 of 10 required H2 sections present (count=$SECTION_COUNT)" 0 || run_test "At least 8 of 10 required H2 sections present (count=$SECTION_COUNT)" 1

# === Test 12: Version field set to 2.0.0 ===
grep -q 'version:.*2\.0\.0' "$TARGET_FILE" && run_test "Version field set to 2.0.0" 0 || run_test "Version field set to 2.0.0" 1

# === Test 13: File between 100-500 lines ===
LINE_COUNT=$(wc -l < "$TARGET_FILE")
if [ "$LINE_COUNT" -ge 100 ] && [ "$LINE_COUNT" -le 500 ]; then
    run_test "File between 100-500 lines (actual=$LINE_COUNT)" 0
else
    run_test "File between 100-500 lines (actual=$LINE_COUNT)" 1
fi

# === Summary ===
echo ""
echo "Results: $PASSED passed, $FAILED failed"
[ "$FAILED" -eq 0 ] && exit 0 || exit 1
