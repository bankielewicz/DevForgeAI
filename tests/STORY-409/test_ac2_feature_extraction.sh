#!/bin/bash
# Test: AC#2 - Feature Extraction from Epic File
# Story: STORY-409
# Generated: 2026-02-16

PASSED=0
FAILED=0
TARGET_FILE="src/claude/skills/devforgeai-story-creation/references/story-discovery.md"

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

echo "=== AC#2: Feature Extraction ==="

# Test 1: Step 0.2 section exists
grep -q "Step 0\.2" "$TARGET_FILE" 2>/dev/null
run_test "Step 0.2 section exists in story-discovery.md" $?

# Test 2: Glob tool usage for epic file location
grep -qi "Glob" "$TARGET_FILE" 2>/dev/null
run_test "Glob tool used to locate epic file" $?

# Test 3: Read tool usage for epic content
grep -q "Read(" "$TARGET_FILE" 2>/dev/null
run_test "Read tool used to get epic content" $?

# Test 4: Feature header parsing pattern
grep -qE "### Feature|Feature.*header" "$TARGET_FILE" 2>/dev/null
run_test "Feature header parsing pattern documented" $?

# Test 5: Structured list output (number, name, description)
grep -qi "feature.*number\|feature.*name\|feature.*description" "$TARGET_FILE" 2>/dev/null
run_test "Feature metadata extraction (number, name, description)" $?

echo ""
echo "Results: $PASSED passed, $FAILED failed"
[ $FAILED -eq 0 ] && exit 0 || exit 1
