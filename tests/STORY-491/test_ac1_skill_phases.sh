#!/bin/bash
# Test: AC#1 - SKILL.md has YAML frontmatter, 4 phases in order, blocking language, <500 lines
# Story: STORY-491
# Generated: 2026-02-23

PASSED=0
FAILED=0
TARGET_FILE="/mnt/c/Projects/DevForgeAI2/src/claude/skills/root-cause-diagnosis/SKILL.md"

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

echo "=== AC#1: SKILL.md Skill Phases ==="

# Test 1: File exists
test -f "$TARGET_FILE"
run_test "SKILL.md file exists" $?

# Test 2: YAML frontmatter with name field
grep -q "^---" "$TARGET_FILE" 2>/dev/null && grep -q "^name:" "$TARGET_FILE" 2>/dev/null
run_test "YAML frontmatter contains name field" $?

# Test 3: Phase 1 CAPTURE exists
grep -qi "phase.*1.*capture\|capture.*phase" "$TARGET_FILE" 2>/dev/null
run_test "Phase 1 CAPTURE defined" $?

# Test 4: Phase 2 INVESTIGATE exists
grep -qi "phase.*2.*investigate\|investigate.*phase" "$TARGET_FILE" 2>/dev/null
run_test "Phase 2 INVESTIGATE defined" $?

# Test 5: Phase 3 HYPOTHESIZE exists
grep -qi "phase.*3.*hypothesize\|hypothesize.*phase" "$TARGET_FILE" 2>/dev/null
run_test "Phase 3 HYPOTHESIZE defined" $?

# Test 6: Phase 4 PRESCRIBE exists
grep -qi "phase.*4.*prescribe\|prescribe.*phase" "$TARGET_FILE" 2>/dev/null
run_test "Phase 4 PRESCRIBE defined" $?

# Test 7: Phases appear in correct order (CAPTURE before INVESTIGATE before HYPOTHESIZE before PRESCRIBE)
if [ -f "$TARGET_FILE" ]; then
    CAPTURE_LINE=$(grep -ni "capture" "$TARGET_FILE" 2>/dev/null | head -1 | cut -d: -f1)
    INVESTIGATE_LINE=$(grep -ni "investigate" "$TARGET_FILE" 2>/dev/null | head -1 | cut -d: -f1)
    HYPOTHESIZE_LINE=$(grep -ni "hypothesize" "$TARGET_FILE" 2>/dev/null | head -1 | cut -d: -f1)
    PRESCRIBE_LINE=$(grep -ni "prescribe" "$TARGET_FILE" 2>/dev/null | head -1 | cut -d: -f1)
    [ -n "$CAPTURE_LINE" ] && [ -n "$INVESTIGATE_LINE" ] && [ -n "$HYPOTHESIZE_LINE" ] && [ -n "$PRESCRIBE_LINE" ] && \
    [ "$CAPTURE_LINE" -lt "$INVESTIGATE_LINE" ] && [ "$INVESTIGATE_LINE" -lt "$HYPOTHESIZE_LINE" ] && [ "$HYPOTHESIZE_LINE" -lt "$PRESCRIBE_LINE" ]
    run_test "Phases appear in correct order (1-2-3-4)" $?
else
    run_test "Phases appear in correct order (1-2-3-4)" 1
fi

# Test 8: Contains blocking/HALT language
grep -qi "halt\|block\|must not proceed\|cannot proceed" "$TARGET_FILE" 2>/dev/null
run_test "Contains blocking/HALT language" $?

# Test 9: File is under 500 lines
if [ -f "$TARGET_FILE" ]; then
    LINE_COUNT=$(wc -l < "$TARGET_FILE")
    [ "$LINE_COUNT" -lt 500 ]
    run_test "File is under 500 lines (got: ${LINE_COUNT})" $?
else
    run_test "File is under 500 lines (file missing)" 1
fi

echo ""
echo "Results: $PASSED passed, $FAILED failed"
[ $FAILED -eq 0 ] && exit 0 || exit 1
