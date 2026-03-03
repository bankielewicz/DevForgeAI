#!/bin/bash
# Test: AC#7 - Generated File Output Paths
# Story: STORY-478
# Generated: 2026-02-23
set -uo pipefail

PROJECT_ROOT="/mnt/c/Projects/DevForgeAI2"
TARGET="$PROJECT_ROOT/src/claude/skills/designing-systems/references/domain-reference-generation.md"
PASSED=0
FAILED=0

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

echo "=== AC#7: Generated File Output Paths ==="

# Test 1: Documents output path pattern
grep -q "\.claude/agents/{agent-name}/references/project-{type}\.md" "$TARGET" || \
grep -q "\.claude/agents/.*references/project-.*\.md" "$TARGET"
run_test "test_should_document_output_path_pattern_when_reference_checked" $?

echo ""
echo "Results: $PASSED passed, $FAILED failed"
[ $FAILED -eq 0 ] && exit 0 || exit 1
