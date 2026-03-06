#!/bin/bash
# Test: AC#6 - Skill Progressive Disclosure
# Story: STORY-538
# Generated: 2026-03-05

# === Test Configuration ===
PASSED=0
FAILED=0
PROJECT_ROOT="/mnt/c/Projects/DevForgeAI2"
SKILL_FILE="${PROJECT_ROOT}/src/claude/skills/researching-market/SKILL.md"
REF_DIR="${PROJECT_ROOT}/src/claude/skills/researching-market/references"

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

echo "=== AC#6: Skill Progressive Disclosure ==="

# === Test 1: SKILL.md exists ===
test -f "$SKILL_FILE"
run_test "SKILL.md exists" $?

# === Test 2: SKILL.md under 1000 lines ===
if [ -f "$SKILL_FILE" ]; then
    LINE_COUNT=$(wc -l < "$SKILL_FILE")
    if [ "$LINE_COUNT" -lt 1000 ]; then
        run_test "SKILL.md under 1000 lines (actual: $LINE_COUNT)" 0
    else
        run_test "SKILL.md under 1000 lines (actual: $LINE_COUNT)" 1
    fi
else
    run_test "SKILL.md under 1000 lines (file not found)" 1
fi

# === Test 3: References directory exists ===
test -d "$REF_DIR"
run_test "References directory exists" $?

# === Test 4: At least 3 reference files exist ===
if [ -d "$REF_DIR" ]; then
    REF_COUNT=$(find "$REF_DIR" -maxdepth 1 -name "*.md" -type f | wc -l)
    if [ "$REF_COUNT" -ge 3 ]; then
        run_test "At least 3 reference files (actual: $REF_COUNT)" 0
    else
        run_test "At least 3 reference files (actual: $REF_COUNT)" 1
    fi
else
    run_test "At least 3 reference files (directory not found)" 1
fi

# === Test 5: SKILL.md references files in references/ directory ===
grep -q "references/" "$SKILL_FILE" 2>/dev/null
run_test "SKILL.md references files in references/ directory" $?

# === Test 6: Progressive disclosure pattern (Read on demand) ===
grep -qi "Read.*references\|load.*on.*demand\|progressive.*disclosure\|reference.*load" "$SKILL_FILE" 2>/dev/null
run_test "SKILL.md uses progressive disclosure pattern" $?

# === Summary ===
echo ""
echo "Results: $PASSED passed, $FAILED failed"
[ $FAILED -eq 0 ] && exit 0 || exit 1
