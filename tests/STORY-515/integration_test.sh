#!/bin/bash
# Integration Tests for STORY-515
# Verify cross-reference integrity when restructuring phase-02-test-first.md
# NFR-001: Restructuring must not break cross-references

set -e

PROJECT_ROOT="/mnt/c/Projects/DevForgeAI2"
PHASE_02_FILE=".claude/skills/implementing-stories/phases/phase-02-test-first.md"
TEST_RESULTS="${PROJECT_ROOT}/tests/STORY-515/integration_results.txt"

echo "STORY-515 Integration Test Report" > "$TEST_RESULTS"
echo "=================================" >> "$TEST_RESULTS"
echo "" >> "$TEST_RESULTS"
echo "Test Timestamp: $(date -u +%Y-%m-%dT%H:%M:%SZ)" >> "$TEST_RESULTS"
echo "" >> "$TEST_RESULTS"

# Test 1: Verify SKILL.md references phase-02-test-first.md correctly
echo "TEST 1: SKILL.md Cross-Reference Integrity" >> "$TEST_RESULTS"
echo "-------------------------------------------" >> "$TEST_RESULTS"
cd "$PROJECT_ROOT"

SKILL_REF=$(grep -c "phase-02-test-first.md" .claude/skills/implementing-stories/SKILL.md || true)
if [ "$SKILL_REF" -gt 0 ]; then
  echo "✓ PASS: SKILL.md references phase-02-test-first.md ($SKILL_REF times)" >> "$TEST_RESULTS"
else
  echo "✗ FAIL: SKILL.md does not reference phase-02-test-first.md" >> "$TEST_RESULTS"
fi
echo "" >> "$TEST_RESULTS"

# Test 2: Verify Phase 03 section references match Phase 02 section names
echo "TEST 2: Phase 03 Section Name Consistency" >> "$TEST_RESULTS"
echo "------------------------------------------" >> "$TEST_RESULTS"

SECTIONS=("AC Checklist Update Verification" "Observation Capture" "Session Memory Update")

for section in "${SECTIONS[@]}"; do
  PHASE_02_COUNT=$(grep -c "### $section" "$PHASE_02_FILE" || true)
  PHASE_03_COUNT=$(grep -c "### $section" .claude/skills/implementing-stories/phases/phase-03-implementation.md || true)

  if [ "$PHASE_02_COUNT" -gt 0 ] && [ "$PHASE_03_COUNT" -gt 0 ]; then
    echo "✓ PASS: '$section' exists in both Phase 02 and Phase 03" >> "$TEST_RESULTS"
  else
    echo "✗ FAIL: Section name mismatch: '$section' (Phase02: $PHASE_02_COUNT, Phase03: $PHASE_03_COUNT)" >> "$TEST_RESULTS"
  fi
done
echo "" >> "$TEST_RESULTS"

# Test 3: Verify Phase 04 section references match Phase 02 section names
echo "TEST 3: Phase 04 Section Name Consistency" >> "$TEST_RESULTS"
echo "------------------------------------------" >> "$TEST_RESULTS"

for section in "${SECTIONS[@]}"; do
  PHASE_02_COUNT=$(grep -c "### $section" "$PHASE_02_FILE" || true)
  PHASE_04_COUNT=$(grep -c "### $section" .claude/skills/implementing-stories/phases/phase-04-refactoring.md || true)

  if [ "$PHASE_02_COUNT" -gt 0 ] && [ "$PHASE_04_COUNT" -gt 0 ]; then
    echo "✓ PASS: '$section' exists in both Phase 02 and Phase 04" >> "$TEST_RESULTS"
  else
    echo "✗ FAIL: Section name mismatch: '$section' (Phase02: $PHASE_02_COUNT, Phase04: $PHASE_04_COUNT)" >> "$TEST_RESULTS"
  fi
done
echo "" >> "$TEST_RESULTS"

# Test 4: Verify key content strings exist across all phase files
echo "TEST 4: Content Preservation Validation" >> "$TEST_RESULTS"
echo "--------------------------------------" >> "$TEST_RESULTS"

CONTENT_STRINGS=(
  "observation-extractor"
  "session_path"
  "Test Integrity Snapshot"
  "devforgeai-validate phase-complete"
)

for content in "${CONTENT_STRINGS[@]}"; do
  PHASE_02_FOUND=$(grep -c "$content" "$PHASE_02_FILE" || true)

  if [ "$PHASE_02_FOUND" -gt 0 ]; then
    echo "✓ PASS: Content '$content' found in Phase 02" >> "$TEST_RESULTS"
  else
    echo "✗ FAIL: Content '$content' NOT found in Phase 02" >> "$TEST_RESULTS"
  fi
done
echo "" >> "$TEST_RESULTS"

# Test 5: Verify Exit Gate section exists in Phase 02
echo "TEST 5: Exit Gate Section Presence" >> "$TEST_RESULTS"
echo "----------------------------------" >> "$TEST_RESULTS"

EXIT_GATE=$(grep -c "## Validation Checkpoint\|### Exit Gate" "$PHASE_02_FILE" || true)
if [ "$EXIT_GATE" -gt 0 ]; then
  echo "✓ PASS: Exit Gate or Validation Checkpoint section exists in Phase 02" >> "$TEST_RESULTS"
else
  echo "✗ FAIL: Exit Gate or Validation Checkpoint section not found in Phase 02" >> "$TEST_RESULTS"
fi
echo "" >> "$TEST_RESULTS"

# Summary
echo "SUMMARY" >> "$TEST_RESULTS"
echo "=======" >> "$TEST_RESULTS"
PASS_COUNT=$(grep -c "✓ PASS" "$TEST_RESULTS" || true)
FAIL_COUNT=$(grep -c "✗ FAIL" "$TEST_RESULTS" || true)
TOTAL=$((PASS_COUNT + FAIL_COUNT))

echo "Total Tests: $TOTAL" >> "$TEST_RESULTS"
echo "Passed: $PASS_COUNT" >> "$TEST_RESULTS"
echo "Failed: $FAIL_COUNT" >> "$TEST_RESULTS"
echo "" >> "$TEST_RESULTS"

if [ "$FAIL_COUNT" -eq 0 ]; then
  echo "Overall Result: PASS ✓" >> "$TEST_RESULTS"
  exit 0
else
  echo "Overall Result: FAIL ✗" >> "$TEST_RESULTS"
  exit 1
fi
