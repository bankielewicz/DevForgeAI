#!/bin/bash
# Test: AC#10 - Summary Report Display
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

echo "=== AC#10: Summary Report Display ==="

# Test 1: Step 5 documents report
grep -q "Step 5" "$TARGET"
run_test "test_should_contain_step5_report_when_reference_checked" $?

# Test 2: Contains count of files generated
grep -iq "count\|files generated\|number of" "$TARGET"
run_test "test_should_contain_file_count_in_report_when_checked" $?

# Test 3: Contains file paths in report
grep -iq "file path" "$TARGET" || grep -iq "output path" "$TARGET"
run_test "test_should_contain_file_paths_in_report_when_checked" $?

# Test 4: Contains source context files reference
grep -iq "source context" "$TARGET" || grep -iq "context file" "$TARGET"
run_test "test_should_reference_source_context_files_when_checked" $?

# Test 5: Contains regeneration command
grep -q "/audit-alignment --generate-refs" "$TARGET"
run_test "test_should_contain_regeneration_command_when_checked" $?

echo ""
echo "Results: $PASSED passed, $FAILED failed"
[ $FAILED -eq 0 ] && exit 0 || exit 1
