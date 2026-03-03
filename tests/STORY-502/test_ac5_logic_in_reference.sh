#!/bin/bash
# Test: AC#5 - Snapshot Logic Lives in Reference File
# Story: STORY-502
# Generated: 2026-02-27

# === Test Configuration ===
PASSED=0
FAILED=0
PROJECT_ROOT="/mnt/c/Projects/DevForgeAI2"
REF_FILE="${PROJECT_ROOT}/src/claude/skills/implementing-stories/references/test-integrity-snapshot.md"
SKILL_FILE="${PROJECT_ROOT}/src/claude/skills/implementing-stories/SKILL.md"

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

echo "=== AC#5: Snapshot Logic Lives in Reference File ==="

# === Test 1: Reference file exists at correct path ===
test -f "$REF_FILE"
run_test "Reference file exists at correct path" $?

# === Test 2: SKILL.md references test-integrity-snapshot.md ===
grep -q "test-integrity-snapshot.md" "$SKILL_FILE" 2>/dev/null
run_test "SKILL.md references test-integrity-snapshot.md" $?

# === Test 3: SKILL.md does NOT contain inline snapshot logic ===
# Snapshot algorithm should be in reference file, not inlined in SKILL.md
# Check that SKILL.md does not contain sha256sum/hashlib computation inline
INLINE_LOGIC=$(grep -c -i "sha256sum\|hashlib.*sha256\|compute.*checksum.*for.*file" "$SKILL_FILE" 2>/dev/null)
if [ "$INLINE_LOGIC" -eq 0 ] 2>/dev/null; then
    run_test "SKILL.md does not contain inline snapshot computation logic" 0
else
    run_test "SKILL.md does not contain inline snapshot computation logic" 1
fi

# === Test 4: SKILL.md stays within size limits (under 500 lines) ===
if [ -f "$SKILL_FILE" ]; then
    LINE_COUNT=$(wc -l < "$SKILL_FILE")
    if [ "$LINE_COUNT" -le 500 ]; then
        run_test "SKILL.md stays within 500-line size limit" 0
    else
        run_test "SKILL.md stays within 500-line size limit" 1
    fi
else
    run_test "SKILL.md stays within 500-line size limit" 1
fi

# === Test 5: Reference file contains substantial content (not stub) ===
if [ -f "$REF_FILE" ]; then
    REF_LINES=$(wc -l < "$REF_FILE")
    if [ "$REF_LINES" -ge 20 ]; then
        run_test "Reference file has substantial content (>= 20 lines)" 0
    else
        run_test "Reference file has substantial content (>= 20 lines)" 1
    fi
else
    run_test "Reference file has substantial content (>= 20 lines)" 1
fi

# === Summary ===
echo ""
echo "Results: $PASSED passed, $FAILED failed"
[ $FAILED -eq 0 ] && exit 0 || exit 1
