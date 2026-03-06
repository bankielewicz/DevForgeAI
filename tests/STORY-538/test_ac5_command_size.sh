#!/bin/bash
# Test: AC#5 - Command Line Limit
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

echo "=== AC#5: Command Line Limit ==="

# === Test 1: Command file exists ===
test -f "$COMMAND_FILE"
run_test "Command file exists" $?

# === Test 2: Command file under 500 lines ===
if [ -f "$COMMAND_FILE" ]; then
    LINE_COUNT=$(wc -l < "$COMMAND_FILE")
    if [ "$LINE_COUNT" -lt 500 ]; then
        run_test "Command file under 500 lines (actual: $LINE_COUNT)" 0
    else
        run_test "Command file under 500 lines (actual: $LINE_COUNT)" 1
    fi
else
    run_test "Command file under 500 lines (file not found)" 1
fi

# === Test 3: No business logic in command (no TAM/SAM/SOM calculations) ===
if [ -f "$COMMAND_FILE" ]; then
    grep -qi "TAM\|SAM\|SOM\|fermi\|interview.*question\|SWOT\|Porter" "$COMMAND_FILE" 2>/dev/null
    # Inverse: grep finding these patterns means FAIL (business logic present)
    if [ $? -eq 0 ]; then
        run_test "No business logic in command (TAM/SAM/SOM/SWOT found)" 1
    else
        run_test "No business logic in command" 0
    fi
else
    run_test "No business logic in command (file not found)" 1
fi

# === Test 4: Command contains only delegation patterns ===
if [ -f "$COMMAND_FILE" ]; then
    grep -qi "skill\|delegate\|invoke\|researching-market" "$COMMAND_FILE" 2>/dev/null
    run_test "Command contains skill delegation patterns" $?
else
    run_test "Command contains skill delegation patterns (file not found)" 1
fi

# === Test 5: Command has YAML frontmatter ===
if [ -f "$COMMAND_FILE" ]; then
    head -1 "$COMMAND_FILE" | grep -q "^---"
    run_test "Command has YAML frontmatter" $?
else
    run_test "Command has YAML frontmatter (file not found)" 1
fi

# === Test 6: Command has argument-hint in frontmatter ===
if [ -f "$COMMAND_FILE" ]; then
    grep -q "argument-hint" "$COMMAND_FILE" 2>/dev/null
    run_test "Command has argument-hint in frontmatter" $?
else
    run_test "Command has argument-hint in frontmatter (file not found)" 1
fi

# === Summary ===
echo ""
echo "Results: $PASSED passed, $FAILED failed"
[ $FAILED -eq 0 ] && exit 0 || exit 1
