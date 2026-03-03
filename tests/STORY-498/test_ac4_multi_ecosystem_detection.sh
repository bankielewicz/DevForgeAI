#!/bin/bash
# Test: AC#4 - Multi-Ecosystem Detection Coverage
# Story: STORY-498
# Generated: 2026-02-24

PASSED=0
FAILED=0
TARGET_FILE="/mnt/c/Projects/DevForgeAI2/src/claude/skills/devforgeai-release/SKILL.md"

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

echo "=== AC#4: Multi-Ecosystem Detection Coverage ==="

# Test 1: Rust ecosystem detection within Project Type Classification section
grep -A80 "Project Type Classification" "$TARGET_FILE" | grep -qi "Rust"
run_test "Rust ecosystem documented in Project Type Classification" $?

# Test 2: Node.js ecosystem detection within Project Type Classification section
grep -A80 "Project Type Classification" "$TARGET_FILE" | grep -qi "Node"
run_test "Node.js ecosystem documented in Project Type Classification" $?

# Test 3: Python ecosystem detection within Project Type Classification section
grep -A80 "Project Type Classification" "$TARGET_FILE" | grep -qi "Python"
run_test "Python ecosystem documented in Project Type Classification" $?

# Test 4: All 3 ecosystems present in structured detection table/matrix
RUST_COUNT=$(grep -A80 "Project Type Classification" "$TARGET_FILE" | grep -ci "Cargo\.toml")
NODE_COUNT=$(grep -A80 "Project Type Classification" "$TARGET_FILE" | grep -ci "package\.json")
PYTHON_COUNT=$(grep -A80 "Project Type Classification" "$TARGET_FILE" | grep -ci "pyproject\.toml")
TOTAL=$((RUST_COUNT + NODE_COUNT + PYTHON_COUNT))
if [ "$TOTAL" -ge 3 ]; then
    run_test "All 3 ecosystems covered in detection section" 0
else
    run_test "All 3 ecosystems covered in detection section" 1
fi

echo ""
echo "Results: $PASSED passed, $FAILED failed"
[ $FAILED -eq 0 ] && exit 0 || exit 1
