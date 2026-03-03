#!/bin/bash
# Test: AC#8 - Story Discovery Reference File Updated
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

echo "=== AC#8: Documentation Updated ==="

# Test 1: All 6 batch steps documented
for step in "0.1" "0.2" "0.3" "0.4" "0.5" "0.6"; do
    grep -q "Step ${step}" "$TARGET_FILE" 2>/dev/null
    run_test "Step ${step} documented in story-discovery.md" $?
done

# Test 2: Pseudocode present (code blocks or indented logic)
grep -cE '^\s{4}|IF |FOR |ELSE' "$TARGET_FILE" 2>/dev/null | grep -q "[1-9]"
run_test "Pseudocode present in documentation" $?

# Test 3: Error handling documented for batch steps
grep -qi "error.*handling\|error.*case\|fallback\|exception" "$TARGET_FILE" 2>/dev/null
run_test "Error handling documented for batch steps" $?

# Test 4: Integration points with Steps 1.0-1.6 documented
grep -qi "integration\|Step 1\.\|existing.*workflow" "$TARGET_FILE" 2>/dev/null
run_test "Integration points with existing steps documented" $?

# Test 5: SKILL.md Phase 1 references batch mode
SKILL_FILE="src/claude/skills/devforgeai-story-creation/SKILL.md"
grep -qi "batch\|Step 0\." "$SKILL_FILE" 2>/dev/null
run_test "SKILL.md Phase 1 references batch mode" $?

echo ""
echo "Results: $PASSED passed, $FAILED failed"
[ $FAILED -eq 0 ] && exit 0 || exit 1
