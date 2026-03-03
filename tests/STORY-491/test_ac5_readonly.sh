#!/bin/bash
# Test: AC#5 - diagnostic-analyst.md tools are exactly [Read, Grep, Glob] - no Write, Edit, Bash
# Story: STORY-491
# Generated: 2026-02-23

PASSED=0
FAILED=0
TARGET_FILE="/mnt/c/Projects/DevForgeAI2/src/claude/agents/diagnostic-analyst.md"

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

echo "=== AC#5: Read-Only Tool Constraint ==="

# Test 1: File exists
test -f "$TARGET_FILE"
run_test "diagnostic-analyst.md file exists" $?

# Test 2: Contains Read tool
grep -q "Read" "$TARGET_FILE" 2>/dev/null
run_test "Lists Read tool" $?

# Test 3: Contains Grep tool
grep -q "Grep" "$TARGET_FILE" 2>/dev/null
run_test "Lists Grep tool" $?

# Test 4: Contains Glob tool
grep -q "Glob" "$TARGET_FILE" 2>/dev/null
run_test "Lists Glob tool" $?

# Test 5: Does NOT contain Write tool in tools section
# We look for Write as a tool declaration (not just mentioned in prose)
if [ -f "$TARGET_FILE" ]; then
    # Extract tools line and check for Write
    TOOLS_LINE=$(grep -i "tools\|allowed.*tools\|tool.*access" "$TARGET_FILE" 2>/dev/null | head -3)
    echo "$TOOLS_LINE" | grep -qi "Write" 2>/dev/null
    [ $? -ne 0 ]
    run_test "Does NOT list Write tool" $?
else
    run_test "Does NOT list Write tool (file missing)" 1
fi

# Test 6: Does NOT contain Edit tool in tools section
if [ -f "$TARGET_FILE" ]; then
    TOOLS_LINE=$(grep -i "tools\|allowed.*tools\|tool.*access" "$TARGET_FILE" 2>/dev/null | head -3)
    echo "$TOOLS_LINE" | grep -qi "Edit" 2>/dev/null
    [ $? -ne 0 ]
    run_test "Does NOT list Edit tool" $?
else
    run_test "Does NOT list Edit tool (file missing)" 1
fi

# Test 7: Does NOT contain Bash tool in tools section
if [ -f "$TARGET_FILE" ]; then
    TOOLS_LINE=$(grep -i "tools\|allowed.*tools\|tool.*access" "$TARGET_FILE" 2>/dev/null | head -3)
    echo "$TOOLS_LINE" | grep -qi "Bash" 2>/dev/null
    [ $? -ne 0 ]
    run_test "Does NOT list Bash tool" $?
else
    run_test "Does NOT list Bash tool (file missing)" 1
fi

echo ""
echo "Results: $PASSED passed, $FAILED failed"
[ $FAILED -eq 0 ] && exit 0 || exit 1
