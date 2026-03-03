#!/bin/bash
# Test: AC#1 - Project Type Detection from Build Configuration
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

echo "=== AC#1: Project Type Detection from Build Configuration ==="

# Test 1: Phase section titled "Project Type Classification" exists
grep -q "Project Type Classification" "$TARGET_FILE"
run_test "Section titled Project Type Classification exists" $?

# Test 2: Project Type Classification appears after Phase 0.2 Build/Compile
PHASE_02_LINE=$(grep -n "Phase 0\.2.*Build\|Build.*Phase 0\.2" "$TARGET_FILE" | head -1 | cut -d: -f1)
PTC_LINE=$(grep -n "Project Type Classification" "$TARGET_FILE" | head -1 | cut -d: -f1)
if [ -n "$PHASE_02_LINE" ] && [ -n "$PTC_LINE" ] && [ "$PTC_LINE" -gt "$PHASE_02_LINE" ]; then
    run_test "Project Type Classification appears after Phase 0.2 Build/Compile" 0
else
    run_test "Project Type Classification appears after Phase 0.2 Build/Compile" 1
fi

# Test 3: Rust detection - Cargo.toml mentioned within Project Type Classification section
grep -A50 "Project Type Classification" "$TARGET_FILE" | grep -q "Cargo\.toml"
run_test "Rust detection: Cargo.toml in Project Type Classification" $?

# Test 4: Node.js detection - package.json mentioned within Project Type Classification section
grep -A50 "Project Type Classification" "$TARGET_FILE" | grep -q "package\.json"
run_test "Node.js detection: package.json in Project Type Classification" $?

# Test 5: Python detection - pyproject.toml mentioned within Project Type Classification section
grep -A50 "Project Type Classification" "$TARGET_FILE" | grep -q "pyproject\.toml"
run_test "Python detection: pyproject.toml in Project Type Classification" $?

# Test 6: Classification includes "library" type within Project Type Classification
grep -A50 "Project Type Classification" "$TARGET_FILE" | grep -qi "library"
run_test "Classification includes library type" $?

# Test 7: Classification includes "cli" type within Project Type Classification
grep -A50 "Project Type Classification" "$TARGET_FILE" | grep -qi '"cli"\|: cli\| cli '
run_test "Classification includes cli type" $?

# Test 8: Classification includes "api" type within Project Type Classification
grep -A50 "Project Type Classification" "$TARGET_FILE" | grep -qi '"api"\|: api\| api '
run_test "Classification includes api type" $?

echo ""
echo "Results: $PASSED passed, $FAILED failed"
[ $FAILED -eq 0 ] && exit 0 || exit 1
