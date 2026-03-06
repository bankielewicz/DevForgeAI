#!/bin/bash
# Test: AC#2 - Skill Assembles with Progressive Disclosure
# Story: STORY-546
# Generated: 2026-03-05

PASSED=0
FAILED=0
PROJECT_ROOT="/mnt/c/Projects/DevForgeAI2"
SKILL_FILE="$PROJECT_ROOT/src/claude/skills/advising-legal/SKILL.md"
REFS_DIR="$PROJECT_ROOT/src/claude/skills/advising-legal/references"

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

echo "=== AC#2: Progressive Disclosure ==="

# Test 1: SKILL.md exists
test -f "$SKILL_FILE"
run_test "test_should_exist_when_skill_file_created" $?

# Test 2: SKILL.md under 1000 lines
LINE_COUNT=$(wc -l < "$SKILL_FILE" 2>/dev/null || echo 9999)
[ "$LINE_COUNT" -lt 1000 ]
run_test "test_should_be_under_1000_lines_when_skill_file_measured" $?

# Test 3: references/ directory exists
test -d "$REFS_DIR"
run_test "test_should_have_references_dir_when_skill_inspected" $?

# Test 4: references/ contains at least one .md file
REF_COUNT=$(find "$REFS_DIR" -name "*.md" 2>/dev/null | wc -l)
[ "$REF_COUNT" -gt 0 ]
run_test "test_should_have_reference_files_when_refs_dir_listed" $?

# Test 5: SKILL.md references the references/ directory
grep -q "references/" "$SKILL_FILE" 2>/dev/null
run_test "test_should_reference_refs_dir_when_skill_evaluated" $?

# Test 6: SKILL.md uses Read tool pattern for progressive loading
grep -qE "Read\(|references/" "$SKILL_FILE" 2>/dev/null
run_test "test_should_use_progressive_loading_when_skill_evaluated" $?

# Test 7: SKILL.md references IP protection checklist (STORY-545 dependency)
grep -q "ip-protection-checklist" "$SKILL_FILE" 2>/dev/null
run_test "test_should_reference_ip_protection_checklist_when_skill_evaluated" $?

# Test 8: SKILL.md has Reference Loading table with multiple entries
REF_TABLE_ENTRIES=$(grep -c "references/" "$SKILL_FILE" 2>/dev/null || echo 0)
[ "$REF_TABLE_ENTRIES" -ge 3 ]
run_test "test_should_have_multiple_reference_entries_when_skill_evaluated" $?

# Test 9: Skill orchestrates references in declared order (phase structure)
grep -qiE "phase|step.*load.*reference|workflow.*order" "$SKILL_FILE" 2>/dev/null
run_test "test_should_orchestrate_refs_in_order_when_skill_evaluated" $?

echo ""
echo "Results: $PASSED passed, $FAILED failed"
[ $FAILED -eq 0 ] && exit 0 || exit 1
