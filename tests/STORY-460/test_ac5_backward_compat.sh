#!/bin/bash
# Test: AC#5 - Backward compatibility for all 6 syntax variants
# Story: STORY-460
# Generated: 2026-02-21
# Expected: FAIL (TDD Red phase - commands not yet refactored to lean pattern)

set -uo pipefail

PROJECT_ROOT="$(cd "$(dirname "$0")/../.." && pwd)"

# === Test Configuration ===
PASSED=0
FAILED=0
TOTAL=0

CMD_QA="${PROJECT_ROOT}/src/claude/commands/qa.md"
CMD_UI="${PROJECT_ROOT}/src/claude/commands/create-ui.md"
CMD_IDEATE="${PROJECT_ROOT}/src/claude/commands/ideate.md"

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
echo "  AC#5: Backward Compatibility (6 Syntax Variants)"
echo "  Story: STORY-460"
echo "=============================================="
echo ""

# All 6 syntax variants must be documented in the refactored commands.
# The lean commands must handle: story+mode, story-only, standalone, brainstorm, etc.

# === Variant 1: /qa STORY-001 deep ===
test_result=0
if grep -qi 'deep\|mode' "$CMD_QA"; then
    test_result=0
else
    test_result=1
fi
run_test "qa.md: supports mode argument (deep/light)" "$test_result"

# === Variant 2: /qa STORY-001 (auto mode) ===
test_result=0
if grep -qi 'STORY\|story.*id\|story_id' "$CMD_QA"; then
    test_result=0
else
    test_result=1
fi
run_test "qa.md: supports story ID argument" "$test_result"

# === Variant 3: /create-ui STORY-001 ===
test_result=0
if grep -qi 'STORY\|story.*id\|story_id' "$CMD_UI"; then
    test_result=0
else
    test_result=1
fi
run_test "create-ui.md: supports story ID argument" "$test_result"

# === Variant 4: /create-ui "Login form" (standalone) ===
test_result=0
if grep -qi 'standalone\|description\|component\|spec' "$CMD_UI"; then
    test_result=0
else
    test_result=1
fi
run_test "create-ui.md: supports standalone description mode" "$test_result"

# === Variant 5: /ideate "app idea" ===
test_result=0
if grep -qi 'idea\|topic\|description' "$CMD_IDEATE"; then
    test_result=0
else
    test_result=1
fi
run_test "ideate.md: supports idea/topic argument" "$test_result"

# === Variant 6: /ideate (brainstorm auto-detection) ===
test_result=0
if grep -qi 'brainstorm\|auto.detect\|resume' "$CMD_IDEATE"; then
    test_result=0
else
    test_result=1
fi
run_test "ideate.md: supports brainstorm auto-detection" "$test_result"

# === Structural: All 3 commands have Skill() invocation ===
echo ""
echo "  --- Structural: Skill() invocation present ---"

for cmd_file in "$CMD_QA" "$CMD_UI" "$CMD_IDEATE"; do
    cmd_name=$(basename "$cmd_file")
    test_result=0
    if grep -q 'Skill(command=' "$cmd_file"; then
        test_result=0
    else
        test_result=1
    fi
    run_test "${cmd_name}: contains Skill(command=) invocation" "$test_result"
done

# === Summary ===
echo ""
echo "----------------------------------------------"
echo "Results: $PASSED passed, $FAILED failed out of $TOTAL tests"
echo "----------------------------------------------"
[ "$FAILED" -eq 0 ] && exit 0 || exit 1
