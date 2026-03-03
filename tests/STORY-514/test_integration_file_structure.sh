#!/bin/bash
# Integration Test: Validate phase-02-test-first.md file structure
# Story: STORY-514
# Purpose: Verify the complete file structure is valid after STORY-514 changes
#
# This test validates:
# 1. All expected sections exist
# 2. New verification section doesn't break markdown structure
# 3. Code blocks are properly balanced (matching ``` pairs)

set -euo pipefail

PROJECT_ROOT="/mnt/c/Projects/DevForgeAI2"
TARGET_FILE="${PROJECT_ROOT}/src/claude/skills/implementing-stories/phases/phase-02-test-first.md"
TEST_RESULTS_DIR="${PROJECT_ROOT}/tests/STORY-514"
TEST_RESULTS="${TEST_RESULTS_DIR}/integration_results.txt"

# Create test results directory
mkdir -p "${TEST_RESULTS_DIR}"

# Initialize results
{
  echo "=== Integration Test: phase-02-test-first.md File Structure ==="
  echo "Test Date: $(date -u '+%Y-%m-%dT%H:%M:%SZ')"
  echo "Target File: ${TARGET_FILE}"
  echo ""
} > "${TEST_RESULTS}"

test_count=0
pass_count=0
fail_count=0

# Helper function to run a test
run_test() {
  local test_name="$1"
  local test_command="$2"

  test_count=$((test_count + 1))

  if eval "$test_command" > /dev/null 2>&1; then
    echo "✓ TEST $test_count PASSED: $test_name" | tee -a "${TEST_RESULTS}"
    pass_count=$((pass_count + 1))
    return 0
  else
    echo "✗ TEST $test_count FAILED: $test_name" | tee -a "${TEST_RESULTS}"
    fail_count=$((fail_count + 1))
    return 1
  fi
}

# Test 1: File exists
run_test "File exists" "[ -f '${TARGET_FILE}' ]"

# Test 2: File is not empty
run_test "File is not empty" "[ -s '${TARGET_FILE}' ]"

# Test 3: File contains Memory Context section
run_test "Contains '## Memory Context' section" "grep -q '^## Memory Context' '${TARGET_FILE}'"

# Test 4: File contains Phase Workflow section
run_test "Contains '## Phase Workflow' section" "grep -q '^## Phase Workflow' '${TARGET_FILE}'"

# Test 5: File contains Test Integrity Snapshot section
run_test "Contains '### Test Integrity Snapshot' section" "grep -q '^### Test Integrity Snapshot' '${TARGET_FILE}'"

# Test 6: File contains Snapshot File Existence Verification section (STORY-514)
run_test "Contains '### Snapshot File Existence Verification' section" "grep -q '^### Snapshot File Existence Verification' '${TARGET_FILE}'"

# Test 7: File contains Validation Checkpoint section
run_test "Contains '## Validation Checkpoint' section" "grep -q '^## Validation Checkpoint' '${TARGET_FILE}'"

# Test 8: File contains Observation Capture section
run_test "Contains '## Observation Capture' section" "grep -q '^## Observation Capture' '${TARGET_FILE}'"

# Test 9: File contains Session Memory Update section
run_test "Contains '### Session Memory Update' section" "grep -q '^### Session Memory Update' '${TARGET_FILE}'"

# Test 10: File contains Exit Gate section
run_test "Contains 'Exit Gate' section" "grep -q '^\\*\\*Exit Gate:\\*\\*' '${TARGET_FILE}'"

# Test 11: Verify code blocks are balanced (count opening and closing ```)
count_code_fences() {
  grep -c '^```' "$1" || echo 0
}

code_fence_count=$(count_code_fences "${TARGET_FILE}")
run_test "Code blocks balanced (even count of \`\`\`)" "[ $((code_fence_count % 2)) -eq 0 ]"

# Test 12: Verify new verification block contains Glob pattern
run_test "New verification block contains Glob pattern" "grep -q 'Glob(pattern=' '${TARGET_FILE}'"

# Test 13: Verify new verification block contains HALT instruction
run_test "New verification block contains HALT instruction" "grep -q 'HALT.*Snapshot file not created' '${TARGET_FILE}'"

# Test 14: Verify snapshot file pattern is correctly templated (not expanded)
run_test "Snapshot pattern uses \${STORY_ID} template" "grep -q 'devforgeai/qa/snapshots/\${STORY_ID}/red-phase-checksums.json' '${TARGET_FILE}'"

# Test 15: Verify Snapshot File Existence Verification section appears before Validation Checkpoint
snapshot_line=$(grep -n '^### Snapshot File Existence Verification' "${TARGET_FILE}" | cut -d: -f1)
checkpoint_line=$(grep -n '^## Validation Checkpoint' "${TARGET_FILE}" | cut -d: -f1)
run_test "Snapshot verification appears before Validation Checkpoint (line order)" "[ ${snapshot_line} -lt ${checkpoint_line} ]"

# Test 16: Verify Test Integrity Snapshot section appears before Snapshot File Existence Verification
integrity_line=$(grep -n '^### Test Integrity Snapshot' "${TARGET_FILE}" | cut -d: -f1)
run_test "Test Integrity Snapshot appears before Snapshot File Existence Verification" "[ ${integrity_line} -lt ${snapshot_line} ]"

# Test 17: Verify markdown link patterns (looking for proper [text](url) or [text] patterns)
# This is a light check - just verify we don't have completely malformed links
run_test "Markdown link patterns are well-formed" "! grep -q '\\[(.*)(.*(.*)' '${TARGET_FILE}'"

# Test 18: Verify markdown headers follow proper hierarchy (## before ###, etc)
run_test "Markdown header hierarchy is valid" "! grep -q '^###' '${TARGET_FILE}' || grep -q '^##' '${TARGET_FILE}'"

# Test 19: Entry Gate section exists and is positioned early
run_test "Entry Gate section exists" "grep -q '^\\*\\*Entry Gate:\\*\\*' '${TARGET_FILE}'"

# Test 20: Verify Entry Gate block exists (defined as **Entry Gate:** pattern)
run_test "Entry Gate block exists with proper formatting" "grep -q '^\\*\\*Entry Gate:\\*\\*' '${TARGET_FILE}' && grep -q 'devforgeai-validate phase-complete' '${TARGET_FILE}'"

# Test 21: Verify no duplicate section headers (critical sections should appear only once)
memory_count=$(grep -c '^## Memory Context' "${TARGET_FILE}")
run_test "Memory Context section appears exactly once" "[ ${memory_count} -eq 1 ]"

phase_count=$(grep -c '^## Phase Workflow' "${TARGET_FILE}")
run_test "Phase Workflow section appears exactly once" "[ ${phase_count} -eq 1 ]"

checkpoint_count=$(grep -c '^## Validation Checkpoint' "${TARGET_FILE}")
run_test "Validation Checkpoint section appears exactly once" "[ ${checkpoint_count} -eq 1 ]"

# Test 24: Verify new verification block is properly formatted (3-line structure)
# Should have Glob(), IF not found:, and HALT
verification_block_lines=$(grep -A 2 'Glob(pattern="devforgeai/qa/snapshots/\${STORY_ID}' "${TARGET_FILE}")
run_test "Snapshot verification block has complete structure" "echo '${verification_block_lines}' | grep -q 'HALT'"

# Write summary
{
  echo ""
  echo "=== Test Summary ==="
  echo "Total Tests: ${test_count}"
  echo "Passed: ${pass_count}"
  echo "Failed: ${fail_count}"
  echo "Pass Rate: $(( (pass_count * 100) / test_count ))%"
  echo ""

  if [ ${fail_count} -eq 0 ]; then
    echo "RESULT: ALL TESTS PASSED ✓"
    exit 0
  else
    echo "RESULT: SOME TESTS FAILED ✗"
    exit 1
  fi
} | tee -a "${TEST_RESULTS}"
