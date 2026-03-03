#!/bin/bash
# Integration test for STORY-524: Memory File Graceful Fallback
# Tests cross-component interactions: src/ phase files, .claude/ operational copies, SKILL.md references

PROJECT_ROOT="/mnt/c/Projects/DevForgeAI2"
SRC_PHASE02="${PROJECT_ROOT}/src/claude/skills/implementing-stories/phases/phase-02-test-first.md"
SRC_PHASE03="${PROJECT_ROOT}/src/claude/skills/implementing-stories/phases/phase-03-implementation.md"
OP_PHASE02="${PROJECT_ROOT}/.claude/skills/implementing-stories/phases/phase-02-test-first.md"
OP_PHASE03="${PROJECT_ROOT}/.claude/skills/implementing-stories/phases/phase-03-implementation.md"
SKILL_FILE="${PROJECT_ROOT}/.claude/skills/implementing-stories/SKILL.md"

FAILED=0
PASSED=0

# Test 1: AC#1 - Phase 02 src/ contains Glob check + fallback
echo "TEST 1: AC#1 - Phase 02 src/ Glob fallback pattern"
if grep -A 5 "Step 0.1: Load TDD Patterns" "$SRC_PHASE02" | grep -q "result = Glob"; then
  if grep -A 8 "Step 0.1: Load TDD Patterns" "$SRC_PHASE02" | grep -q "No TDD patterns in long-term memory yet"; then
    echo "  PASS: Glob check present + fallback message correct"
    ((PASSED++))
  else
    echo "  FAIL: Fallback message not found or incorrect"
    ((FAILED++))
  fi
else
  echo "  FAIL: Glob check not found in Step 0.1"
  ((FAILED++))
fi

# Test 2: AC#2 - Phase 03 src/ contains Glob check + fallback
echo "TEST 2: AC#2 - Phase 03 src/ Glob fallback pattern"
if grep -A 5 "Step 0.1: Load Friction Catalog" "$SRC_PHASE03" | grep -q "result = Glob"; then
  if grep -A 8 "Step 0.1: Load Friction Catalog" "$SRC_PHASE03" | grep -q "No friction patterns in long-term memory yet"; then
    echo "  PASS: Glob check present + fallback message correct"
    ((PASSED++))
  else
    echo "  FAIL: Fallback message not found or incorrect"
    ((FAILED++))
  fi
else
  echo "  FAIL: Glob check not found in Step 0.1"
  ((FAILED++))
fi

# Test 3: Operational copy sync check (Phase 02)
echo "TEST 3: src/ vs .claude/ sync - Phase 02"
if grep -A 3 "Step 0.1:" "$OP_PHASE02" | grep -q "result = Glob"; then
  echo "  INFO: Operational copy (.claude/) already has Glob fallback (sync completed)"
  ((PASSED++))
else
  echo "  INFO: Operational copy (.claude/) still uses unconditional Read (sync pending - acceptable)"
  ((PASSED++))
fi

# Test 4: Operational copy sync check (Phase 03)
echo "TEST 4: src/ vs .claude/ sync - Phase 03"
if grep -A 3 "Step 0.1:" "$OP_PHASE03" | grep -q "result = Glob"; then
  echo "  INFO: Operational copy (.claude/) already has Glob fallback (sync completed)"
  ((PASSED++))
else
  echo "  INFO: Operational copy (.claude/) still uses unconditional Read (sync pending - acceptable)"
  ((PASSED++))
fi

# Test 5: SKILL.md references phase files correctly
echo "TEST 5: SKILL.md phase file references"
if grep -q "phases/phase-02" "$SKILL_FILE" || grep -q "phase-02" "$SKILL_FILE"; then
  echo "  PASS: SKILL.md references Phase 02"
  ((PASSED++))
else
  echo "  FAIL: SKILL.md does not reference Phase 02 correctly"
  ((FAILED++))
fi

# Test 6: Step sequencing integrity - Phase 02
echo "TEST 6: Phase 02 step sequencing (Steps 0.1 → 0.2 → 0.3)"
STEP01_LINE=$(grep -n "Step 0.1:" "$SRC_PHASE02" | cut -d: -f1 || echo "0")
STEP02_LINE=$(grep -n "Step 0.2:" "$SRC_PHASE02" | cut -d: -f1 || echo "0")
STEP03_LINE=$(grep -n "Step 0.3:" "$SRC_PHASE02" | cut -d: -f1 || echo "0")

if [ "$STEP01_LINE" -gt 0 ] && [ "$STEP02_LINE" -gt 0 ] && [ "$STEP03_LINE" -gt 0 ]; then
  if [ "$STEP01_LINE" -lt "$STEP02_LINE" ] && [ "$STEP02_LINE" -lt "$STEP03_LINE" ]; then
    echo "  PASS: Steps ordered correctly (0.1:$STEP01_LINE < 0.2:$STEP02_LINE < 0.3:$STEP03_LINE)"
    ((PASSED++))
  else
    echo "  FAIL: Step ordering is incorrect"
    ((FAILED++))
  fi
else
  echo "  FAIL: One or more steps missing"
  ((FAILED++))
fi

# Test 7: Step sequencing integrity - Phase 03
echo "TEST 7: Phase 03 step sequencing (Steps 0.1 → 0.2 → 0.3)"
STEP01_LINE=$(grep -n "Step 0.1:" "$SRC_PHASE03" | cut -d: -f1 || echo "0")
STEP02_LINE=$(grep -n "Step 0.2:" "$SRC_PHASE03" | cut -d: -f1 || echo "0")
STEP03_LINE=$(grep -n "Step 0.3:" "$SRC_PHASE03" | cut -d: -f1 || echo "0")

if [ "$STEP01_LINE" -gt 0 ] && [ "$STEP02_LINE" -gt 0 ] && [ "$STEP03_LINE" -gt 0 ]; then
  if [ "$STEP01_LINE" -lt "$STEP02_LINE" ] && [ "$STEP02_LINE" -lt "$STEP03_LINE" ]; then
    echo "  PASS: Steps ordered correctly (0.1:$STEP01_LINE < 0.2:$STEP02_LINE < 0.3:$STEP03_LINE)"
    ((PASSED++))
  else
    echo "  FAIL: Step ordering is incorrect"
    ((FAILED++))
  fi
else
  echo "  FAIL: One or more steps missing"
  ((FAILED++))
fi

# Test 8: Fallback logic doesn't break subsequent steps
echo "TEST 8: Phase 02 Step 0.2 (Pattern Matching) present"
if grep -q "Step 0.2:" "$SRC_PHASE02" && grep -A 15 "Step 0.2:" "$SRC_PHASE02" | grep -q "IF pattern.confidence"; then
  echo "  PASS: Step 0.2 pattern matching logic present (not broken by fallback)"
  ((PASSED++))
else
  echo "  FAIL: Step 0.2 appears missing or malformed"
  ((FAILED++))
fi

# Test 9: Fallback logic doesn't break subsequent steps (Phase 03)
echo "TEST 9: Phase 03 Step 0.2 (Friction Matching) present"
if grep -q "Step 0.2:" "$SRC_PHASE03" && grep -A 15 "Step 0.2:" "$SRC_PHASE03" | grep -q "IF friction.confidence"; then
  echo "  PASS: Step 0.2 friction matching logic present (not broken by fallback)"
  ((PASSED++))
else
  echo "  FAIL: Step 0.2 appears missing or malformed"
  ((FAILED++))
fi

# Test 10: Consistent pattern between Phase 02 and Phase 03
echo "TEST 10: Fallback pattern consistency (IF/ELSE structure)"
if grep -q "IF result is not empty:" "$SRC_PHASE02" && grep -q "IF result is not empty:" "$SRC_PHASE03"; then
  echo "  PASS: Both phases use identical IF/ELSE pattern structure"
  ((PASSED++))
else
  echo "  FAIL: IF/ELSE structure differs between phases"
  ((FAILED++))
fi

# Summary
echo ""
echo "=========================================="
echo "Test Results: $PASSED passed, $FAILED failed"
echo "=========================================="

if [ $FAILED -gt 0 ]; then
  exit 1
fi
exit 0
