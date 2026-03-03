#!/bin/bash
# Test: AC#4 - devforgeai-qa SKILL.md prerequisite size reduction
# Story: STORY-460
# Generated: 2026-02-21
# Expected: FAIL (TDD Red phase - SKILL.md is currently 1,012 lines, must be <=800)

set -uo pipefail

PROJECT_ROOT="$(cd "$(dirname "$0")/../.." && pwd)"

# === Test Configuration ===
PASSED=0
FAILED=0
TOTAL=0

SKILL_FILE="${PROJECT_ROOT}/src/claude/skills/devforgeai-qa/SKILL.md"
REFERENCES_DIR="${PROJECT_ROOT}/src/claude/skills/devforgeai-qa/references"

run_test() {
    local name="$1"
    local result="$2"
    ((TOTAL++))
    if [ "$result" -eq 0 ]; then
        echo "  PASS: $name"
        ((PASSED++))
    else
        echo "  FAIL: $name"
        ((FAILED++))
    fi
}

echo "=============================================="
echo "  AC#4: devforgeai-qa SKILL.md Prerequisite"
echo "  Story: STORY-460"
echo "=============================================="
echo ""

# --- Pre-check: File exists ---
if [ ! -f "$SKILL_FILE" ]; then
    echo "  FATAL: Target file not found: $SKILL_FILE"
    echo ""
    echo "Results: 0 passed, 3 failed out of 3 tests"
    exit 1
fi

# === Test 1: SKILL.md line count <=800 ===
LINE_COUNT=$(wc -l < "$SKILL_FILE")
test_result=0
if [ "$LINE_COUNT" -le 800 ]; then
    test_result=0
else
    test_result=1
fi
run_test "SKILL.md line count <= 800 (actual: ${LINE_COUNT})" "$test_result"

# === Test 2: References directory exists ===
test_result=0
if [ -d "$REFERENCES_DIR" ]; then
    test_result=0
else
    test_result=1
fi
run_test "References directory exists at ${REFERENCES_DIR}" "$test_result"

# === Test 3: At least 1 reference file created from extraction ===
if [ -d "$REFERENCES_DIR" ]; then
    REF_COUNT=$(find "$REFERENCES_DIR" -name "*.md" -type f 2>/dev/null | wc -l)
    test_result=0
    if [ "$REF_COUNT" -ge 1 ]; then
        test_result=0
    else
        test_result=1
    fi
    run_test "At least 1 reference file in references/ (actual: ${REF_COUNT})" "$test_result"
else
    run_test "At least 1 reference file in references/ (dir missing)" 1
fi

# === Test 4: SKILL.md references the extracted content ===
test_result=0
if grep -q 'references/' "$SKILL_FILE"; then
    test_result=0
else
    test_result=1
fi
run_test "SKILL.md references extracted content via references/" "$test_result"

# === Summary ===
echo ""
echo "----------------------------------------------"
echo "Results: $PASSED passed, $FAILED failed out of $TOTAL tests"
echo "----------------------------------------------"
[ "$FAILED" -eq 0 ] && exit 0 || exit 1
