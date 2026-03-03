#!/bin/bash
# Test: AC#4 - Orphaned phase-4-output Tag Removed and phase-3-output Extended
# Story: STORY-451
# Generated: 2026-02-19
# TDD Phase: RED (tests must FAIL against current state)

PASSED=0
FAILED=0

SKILL_MD="/mnt/c/Projects/DevForgeAI2/src/claude/skills/discovering-requirements/SKILL.md"

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

echo "=== AC#4: Orphaned phase-4-output Tag Removed and phase-3-output Extended ==="
echo ""

# === Arrange ===
# SKILL.md lines 301-303 contain orphaned <phase-4-output> block:
#   <phase-4-output>
#     mode, recommended_command, handoff_complete
#   </phase-4-output>
# These fields must be removed from phase-4-output and merged into phase-3-output.
# phase-3-output currently only has: requirements_md_path, yaml_schema_valid, completion_summary, next_action

# === Act & Assert ===

# Test 1: SKILL.md must NOT contain <phase-4-output> opening tag
# Current state: line 301 contains <phase-4-output> (FAIL expected)
! grep -q '<phase-4-output>' "$SKILL_MD"
run_test "SKILL.md does not contain <phase-4-output> opening tag" $?

# Test 2: SKILL.md must NOT contain </phase-4-output> closing tag
# Current state: line 303 contains </phase-4-output> (FAIL expected)
! grep -q '</phase-4-output>' "$SKILL_MD"
run_test "SKILL.md does not contain </phase-4-output> closing tag" $?

# Test 3: phase-3-output must contain 'mode' field (merged from phase-4-output)
# Current state: phase-3-output does NOT contain 'mode' (FAIL expected)
# Extract the phase-3-output block and check for 'mode'
sed -n '/<phase-3-output>/,/<\/phase-3-output>/p' "$SKILL_MD" | grep -q 'mode'
run_test "phase-3-output block contains 'mode' field" $?

# Test 4: phase-3-output must contain 'recommended_command' field (merged from phase-4-output)
# Current state: phase-3-output does NOT contain 'recommended_command' (FAIL expected)
sed -n '/<phase-3-output>/,/<\/phase-3-output>/p' "$SKILL_MD" | grep -q 'recommended_command'
run_test "phase-3-output block contains 'recommended_command' field" $?

# Test 5: phase-3-output must contain 'handoff_complete' field (merged from phase-4-output)
# Current state: phase-3-output does NOT contain 'handoff_complete' (FAIL expected)
sed -n '/<phase-3-output>/,/<\/phase-3-output>/p' "$SKILL_MD" | grep -q 'handoff_complete'
run_test "phase-3-output block contains 'handoff_complete' field" $?

# Test 6: phase-3-output must still contain original fields (non-regression)
# These pass in current state but verify no regression after merge
sed -n '/<phase-3-output>/,/<\/phase-3-output>/p' "$SKILL_MD" | grep -q 'requirements_md_path'
run_test "phase-3-output block retains 'requirements_md_path' field" $?

sed -n '/<phase-3-output>/,/<\/phase-3-output>/p' "$SKILL_MD" | grep -q 'completion_summary'
run_test "phase-3-output block retains 'completion_summary' field" $?

# Test 7: No orphaned consecutive blank lines where phase-4-output was removed
# After removal the area around former lines 301-303 should not have 3+ consecutive blank lines
# Check that there are no runs of 3+ blank lines in the file
! grep -qP '^\n\n\n' "$SKILL_MD"
awk 'BEGIN{blank=0} /^$/{blank++; if(blank>=3){found=1}} /^.+$/{blank=0} END{exit found}' "$SKILL_MD"
run_test "No triple consecutive blank lines (no orphaned whitespace)" $?

echo ""
echo "Results: $PASSED passed, $FAILED failed"
[ $FAILED -eq 0 ] && exit 0 || exit 1
