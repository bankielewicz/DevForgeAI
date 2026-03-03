#!/bin/bash
# Test: AC#8 - Cross-Epic Additive Modification
# Story: STORY-479
# Generated: 2026-02-23

PASSED=0
FAILED=0
TARGET_FILE="src/claude/commands/audit-alignment.md"

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

echo "=== AC#8: Cross-Epic Additive Modification ==="

# Test 1: STORY-474 Phase 0 section still present
grep -q 'Phase 0' "$TARGET_FILE"
run_test "test_should_retain_phase_0_when_modified" $?

# Test 2: STORY-474 Phase 1-5 sections still present
grep -q 'Phase 1' "$TARGET_FILE" && grep -q 'Phase 2' "$TARGET_FILE" && grep -q 'Phase 3' "$TARGET_FILE" && grep -q 'Phase 4' "$TARGET_FILE" && grep -q 'Phase 5' "$TARGET_FILE"
run_test "test_should_retain_phases_1_through_5_when_modified" $?

# Test 3: Error Handling section still present
grep -qi 'Error Handling' "$TARGET_FILE"
run_test "test_should_retain_error_handling_section_when_modified" $?

# Test 4: Integration section still present
grep -qi 'Integration' "$TARGET_FILE"
run_test "test_should_retain_integration_section_when_modified" $?

# Test 5: --generate-refs documented in argument-hint frontmatter
grep -A 10 'argument-hint' "$TARGET_FILE" | grep -q '\-\-generate-refs'
run_test "test_should_include_generate_refs_in_argument_hint_when_modified" $?

# Test 6: Quick Reference includes --generate-refs usage
grep -A 20 -i 'Quick Reference' "$TARGET_FILE" | grep -q '\-\-generate-refs'
run_test "test_should_include_generate_refs_in_quick_reference_when_modified" $?

echo ""
echo "Results: $PASSED passed, $FAILED failed"
[ $FAILED -eq 0 ] && exit 0 || exit 1
