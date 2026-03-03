#!/bin/bash
# Test: AC#2 - diagnostic-analyst.md references all 6 context files, spec drift methodology, XML output
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

echo "=== AC#2: Spec Drift Detection ==="

# Test 1: File exists
test -f "$TARGET_FILE"
run_test "diagnostic-analyst.md file exists" $?

# Test 2-7: References all 6 context files
CONTEXT_FILES=("tech-stack.md" "source-tree.md" "dependencies.md" "coding-standards.md" "architecture-constraints.md" "anti-patterns.md")
for ctx in "${CONTEXT_FILES[@]}"; do
    grep -q "$ctx" "$TARGET_FILE" 2>/dev/null
    run_test "References context file: $ctx" $?
done

# Test 8: Contains spec drift methodology
grep -qi "spec.*drift\|specification.*drift" "$TARGET_FILE" 2>/dev/null
run_test "Contains spec drift detection methodology" $?

# Test 9: Contains XML output format
grep -q "<diagnostic\|<diagnosis\|<finding\|<result" "$TARGET_FILE" 2>/dev/null
run_test "Contains XML output format" $?

echo ""
echo "Results: $PASSED passed, $FAILED failed"
[ $FAILED -eq 0 ] && exit 0 || exit 1
