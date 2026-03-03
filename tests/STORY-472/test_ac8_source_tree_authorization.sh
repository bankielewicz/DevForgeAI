#!/bin/bash
# Test: AC#8 - Decision Authorizes source-tree.md Updates for All 5 CLAP Files
# Story: STORY-472
# Generated: 2026-02-23

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

echo "=== AC#8: Decision Authorizes source-tree.md Updates for All 5 CLAP Files ==="

# === Arrange ===
TARGET_FILE="devforgeai/specs/adrs/ADR-021-configuration-layer-alignment-protocol.md"

# === Act & Assert ===

# Test 1: File path 1 - alignment-auditor.md
grep -q "\.claude/agents/alignment-auditor\.md" "$TARGET_FILE" 2>/dev/null
run_test "Authorizes .claude/agents/alignment-auditor.md" $?

# Test 2: File path 2 - validation-matrix.md
grep -q "\.claude/agents/alignment-auditor/references/validation-matrix\.md" "$TARGET_FILE" 2>/dev/null
run_test "Authorizes .claude/agents/alignment-auditor/references/validation-matrix.md" $?

# Test 3: File path 3 - audit-alignment.md
grep -q "\.claude/commands/audit-alignment\.md" "$TARGET_FILE" 2>/dev/null
run_test "Authorizes .claude/commands/audit-alignment.md" $?

# Test 4: File path 4 - prompt-alignment-workflow.md
grep -q "\.claude/skills/designing-systems/references/prompt-alignment-workflow\.md" "$TARGET_FILE" 2>/dev/null
run_test "Authorizes .claude/skills/designing-systems/references/prompt-alignment-workflow.md" $?

# Test 5: File path 5 - domain-reference-generation.md
grep -q "\.claude/skills/designing-systems/references/domain-reference-generation\.md" "$TARGET_FILE" 2>/dev/null
run_test "Authorizes .claude/skills/designing-systems/references/domain-reference-generation.md" $?

# === Summary ===
echo ""
echo "Results: $PASSED passed, $FAILED failed"
[ $FAILED -eq 0 ] && exit 0 || exit 1
