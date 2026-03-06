#!/bin/bash
# Test: AC#1 - Command Invokes Skill Correctly
# Story: STORY-538
# Generated: 2026-03-05

# === Test Configuration ===
PASSED=0
FAILED=0
PROJECT_ROOT="/mnt/c/Projects/DevForgeAI2"
COMMAND_FILE="${PROJECT_ROOT}/src/claude/commands/market-research.md"

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

echo "=== AC#1: Command Invokes Skill Correctly ==="

# === Test 1: Command file exists ===
test -f "$COMMAND_FILE"
run_test "Command file exists at src/claude/commands/market-research.md" $?

# === Test 2: Command references researching-market skill ===
grep -q "researching-market" "$COMMAND_FILE" 2>/dev/null
run_test "Command references researching-market skill" $?

# === Test 3: Command lists valid phase arguments ===
grep -q "market-sizing" "$COMMAND_FILE" 2>/dev/null && \
grep -q "competitive-analysis" "$COMMAND_FILE" 2>/dev/null && \
grep -q "customer-interviews" "$COMMAND_FILE" 2>/dev/null && \
grep -q "full" "$COMMAND_FILE" 2>/dev/null
run_test "Command lists all 4 valid phase arguments" $?

# === Test 4: Command has argument validation logic ===
# Must contain validation/error handling for invalid arguments
grep -qi "invalid\|error\|valid.*options\|argument.*validation\|ARGUMENTS" "$COMMAND_FILE" 2>/dev/null
run_test "Command contains argument validation logic" $?

# === Test 5: Command delegates to skill (not inline business logic) ===
# Command should invoke skill, not contain phase-specific logic like TAM/SAM/SOM
grep -q -i "skill\|invoke\|delegate" "$COMMAND_FILE" 2>/dev/null
run_test "Command delegates to skill" $?

# === Test 6: Command handles invalid arguments with error message ===
# Must show valid options when invalid arg provided
grep -qi "valid.*options\|supported.*phases\|available.*phases\|must be one of" "$COMMAND_FILE" 2>/dev/null
run_test "Command shows valid options on invalid argument" $?

# === Summary ===
echo ""
echo "Results: $PASSED passed, $FAILED failed"
[ $FAILED -eq 0 ] && exit 0 || exit 1
