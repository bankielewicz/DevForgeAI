#!/usr/bin/env bash
# STORY-457 AC#9: RCA-020 Story Quality Gates preserved in skill or references
set -euo pipefail

SKILL_DIR="src/claude/skills/validating-epic-coverage"
PASS=0
FAIL=0

assert_true() {
    local desc="$1"; shift
    if "$@" >/dev/null 2>&1; then
        echo "  PASS: $desc"
        PASS=$((PASS + 1))
    else
        echo "  FAIL: $desc"
        FAIL=$((FAIL + 1))
    fi
}

echo "=== AC#9: RCA-020 Story Quality Gates ==="
echo ""

# Test 1: RCA-020 reference exists in skill or references
echo "--- RCA-020 Reference ---"
if [ -d "$SKILL_DIR" ]; then
    assert_true "RCA-020 mentioned in skill/references" grep -rq 'RCA-020' "$SKILL_DIR"
else
    echo "  FAIL: Skill directory missing"
    FAIL=$((FAIL + 1))
fi

# Test 2: verified_violations reference
echo "--- Evidence Requirements ---"
if [ -d "$SKILL_DIR" ]; then
    assert_true "verified_violations mentioned" grep -rq 'verified_violations' "$SKILL_DIR"
    assert_true "Specific file paths requirement" grep -rqi 'file path\|line number' "$SKILL_DIR"
    assert_true "Target file validation requirement" grep -rqi 'target file\|file.*exist\|validation' "$SKILL_DIR"
    assert_true "No placeholders requirement" grep -rqi 'placeholder\|TBD\|TODO.*not\|no.*placeholder' "$SKILL_DIR"
else
    echo "  FAIL: Skill directory missing"
    FAIL=$((FAIL + 1))
fi

# Test 3: Failure reasons table preserved
echo "--- Failure Reasons Table ---"
if [ -d "$SKILL_DIR" ]; then
    assert_true "Has failure reasons table" grep -rq 'Target file not found\|Claim not verified' "$SKILL_DIR"
fi

# Test 4: Example error message format preserved
echo "--- Error Message Format ---"
if [ -d "$SKILL_DIR" ]; then
    assert_true "Has evidence verification error format" grep -rqi 'evidence.*verif\|Story creation blocked' "$SKILL_DIR"
fi

echo ""
echo "=== Results: $PASS passed, $FAIL failed ==="
[ "$FAIL" -eq 0 ] && exit 0 || exit 1
