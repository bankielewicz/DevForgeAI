#!/bin/bash
# Test: AC#1 - Decision Context Section Added to Epic Template
# Story: STORY-507
# Generated: 2026-02-28

# === Test Configuration ===
PASSED=0
FAILED=0
TARGET_FILE="/mnt/c/Projects/DevForgeAI2/src/claude/skills/designing-systems/assets/templates/epic-template.md"

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

echo "=== AC#1: Decision Context Section Added to Epic Template ==="
echo ""

# === Arrange ===
if [ ! -f "$TARGET_FILE" ]; then
    echo "  FAIL: Target file not found: $TARGET_FILE"
    exit 1
fi

# === Act & Assert ===

# Test 1: Main section header exists
grep -q "^## Decision Context" "$TARGET_FILE"
run_test "Section header '## Decision Context' exists" $?

# Test 2: Design Rationale subsection exists
grep -q "^### Design Rationale" "$TARGET_FILE"
run_test "Subsection '### Design Rationale' exists" $?

# Test 3: Rejected Alternatives subsection exists
grep -q "^### Rejected Alternatives" "$TARGET_FILE"
run_test "Subsection '### Rejected Alternatives' exists" $?

# Test 4: Adversary/Threat Model subsection exists
grep -q "^### Adversary/Threat Model" "$TARGET_FILE"
run_test "Subsection '### Adversary/Threat Model' exists" $?

# Test 5: Implementation Constraints subsection exists
grep -q "^### Implementation Constraints" "$TARGET_FILE"
run_test "Subsection '### Implementation Constraints' exists" $?

# Test 6: Key Insights from Discovery subsection exists
grep -q "^### Key Insights from Discovery" "$TARGET_FILE"
run_test "Subsection '### Key Insights from Discovery' exists" $?

# === Summary ===
echo ""
echo "Results: $PASSED passed, $FAILED failed"
[ $FAILED -eq 0 ] && exit 0 || exit 1
