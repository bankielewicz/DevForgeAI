#!/usr/bin/env bash
# STORY-387 AC#2: Phase Instruction Pattern Specification
# Verifies zero-padded numbering, Objective statement, Pre-Flight, Read() hint syntax.
#
# TDD Phase: RED - These tests MUST fail until the template is created.
set -uo pipefail

TEMPLATE="src/claude/skills/devforgeai-subagent-creation/assets/templates/skill-template.md"
PROJECT_ROOT="/mnt/c/Projects/DevForgeAI2"
FILE="$PROJECT_ROOT/$TEMPLATE"
PASS=0
FAIL=0

assert_grep() {
  local description="$1"
  local pattern="$2"
  if grep -qiP "$pattern" "$FILE" 2>/dev/null; then
    echo "  PASS: $description"
    PASS=$((PASS + 1))
  else
    echo "  FAIL: $description"
    FAIL=$((FAIL + 1))
  fi
}

echo "=== AC#2: Phase Instruction Pattern Specification ==="
echo ""

# Test 1: File exists
echo "Test 1: Template file exists"
if [ -f "$FILE" ]; then
  echo "  PASS: Template file exists"
  PASS=$((PASS + 1))
else
  echo "  FAIL: Template file does not exist at $TEMPLATE"
  FAIL=$((FAIL + 1))
  echo ""
  echo "Results: $PASS passed, $FAIL failed"
  exit 1
fi

# Test 2: Zero-padded phase numbering pattern documented
echo "Test 2: Zero-padded phase numbering (Phase 01:, Phase 02:)"
assert_grep "Zero-padded phase numbering documented" "Phase 0[1-9]:|zero.padded"

# Test 3: Objective statement required per phase
echo "Test 3: Objective statement required per phase"
assert_grep "Objective statement in phase pattern" "Objective"

# Test 4: Pre-Flight verification pattern
echo "Test 4: Pre-Flight verification for prerequisite phases"
assert_grep "Pre-Flight verification documented" "Pre-Flight"

# Test 5: Read() hint syntax documented
echo "Test 5: Read() hint syntax for reference loading"
assert_grep "Read() hint syntax present" 'Read\(file_path='

# Test 6: Support for simple skills (3-5 phases)
echo "Test 6: Simple skills (3-5 phases) supported"
assert_grep "Simple skills supported" "3.*phase|simple.*skill|3-5"

# Test 7: Support for complex skills (8-10 phases)
echo "Test 7: Complex skills (8-10 phases) supported"
assert_grep "Complex skills supported" "8.*phase|complex.*skill|8-10|10.*phase"

echo ""
echo "Results: $PASS passed, $FAIL failed"
[ "$FAIL" -eq 0 ] || exit 1
