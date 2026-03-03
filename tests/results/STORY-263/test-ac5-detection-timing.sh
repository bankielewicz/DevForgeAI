#!/bin/bash
# STORY-263 AC#5: Detection occurs before Phase 01.9.5
# Test: Detection timing is correct (after STORY_ID parsing, before Phase 1)
#
# Expected: FAIL (Step 0.3 not yet implemented)

# Note: No 'set -e' - we need to track failures, not exit on first grep failure

TARGET_FILE="/mnt/c/Projects/DevForgeAI2/.claude/commands/dev.md"
STORY_ID="STORY-263"
AC_NUM="AC#5"

echo "================================================================"
echo "  ${STORY_ID} - ${AC_NUM}: Detection occurs before Phase 01.9.5"
echo "================================================================"
echo ""
echo "Target: ${TARGET_FILE}"
echo ""

# Track test results
TESTS_PASSED=0
TESTS_FAILED=0

# Test 5.1: File exists
echo "Test 5.1: Target file exists"
if [[ -f "${TARGET_FILE}" ]]; then
    echo "  PASS: File exists"
    ((TESTS_PASSED++))
else
    echo "  FAIL: File does not exist"
    ((TESTS_FAILED++))
    echo ""
    echo "RESULT: FAILED (file not found)"
    exit 1
fi

# Test 5.2: Step 0.3 exists in Phase 0 section
echo ""
echo "Test 5.2: Step 0.3 exists in Phase 0 section"
# Get Phase 0 content (between "### Phase 0:" and "### Phase 1:")
PHASE_0_CONTENT=$(sed -n '/### Phase 0:/,/### Phase 1:/p' "${TARGET_FILE}" 2>/dev/null)
if echo "${PHASE_0_CONTENT}" | grep -qE "Step 0\.3"; then
    echo "  PASS: Step 0.3 is within Phase 0 section"
    ((TESTS_PASSED++))
else
    echo "  FAIL: Step 0.3 not found in Phase 0 section"
    echo "        Phase 0 should contain Steps 0.0, 0.1, 0.2, AND 0.3"
    ((TESTS_FAILED++))
fi

# Test 5.3: Step sequence is correct (0.0 -> 0.1 -> 0.2 -> 0.3)
echo ""
echo "Test 5.3: Step sequence ordering"
STEP_00_LINE=$(grep -n "Step 0\.0" "${TARGET_FILE}" | head -1 | cut -d: -f1)
STEP_01_LINE=$(grep -n "Step 0\.1" "${TARGET_FILE}" | head -1 | cut -d: -f1)
STEP_02_LINE=$(grep -n "Step 0\.2" "${TARGET_FILE}" | head -1 | cut -d: -f1)
STEP_03_LINE=$(grep -n "Step 0\.3" "${TARGET_FILE}" | head -1 | cut -d: -f1)

echo "  Step locations:"
echo "    Step 0.0: line ${STEP_00_LINE:-NOT FOUND}"
echo "    Step 0.1: line ${STEP_01_LINE:-NOT FOUND}"
echo "    Step 0.2: line ${STEP_02_LINE:-NOT FOUND}"
echo "    Step 0.3: line ${STEP_03_LINE:-NOT FOUND}"

if [[ -n "${STEP_02_LINE}" && -n "${STEP_03_LINE}" ]]; then
    if [[ ${STEP_03_LINE} -gt ${STEP_02_LINE} ]]; then
        echo "  PASS: Step 0.3 follows Step 0.2"
        ((TESTS_PASSED++))
    else
        echo "  FAIL: Step 0.3 does not follow Step 0.2"
        ((TESTS_FAILED++))
    fi
else
    echo "  FAIL: Cannot verify step ordering - Step 0.3 missing"
    ((TESTS_FAILED++))
fi

# Test 5.4: Step 0.3 before Phase 1 skill invocation
echo ""
echo "Test 5.4: Step 0.3 before Phase 1 skill invocation"
PHASE_1_LINE=$(grep -n "### Phase 1:" "${TARGET_FILE}" | head -1 | cut -d: -f1)
SKILL_INVOKE_LINE=$(grep -n 'Skill(command="devforgeai-development")' "${TARGET_FILE}" | head -1 | cut -d: -f1)

if [[ -n "${STEP_03_LINE}" && -n "${PHASE_1_LINE}" ]]; then
    if [[ ${STEP_03_LINE} -lt ${PHASE_1_LINE} ]]; then
        echo "  PASS: Step 0.3 (line ${STEP_03_LINE}) before Phase 1 (line ${PHASE_1_LINE})"
        ((TESTS_PASSED++))
    else
        echo "  FAIL: Step 0.3 should be before Phase 1"
        ((TESTS_FAILED++))
    fi
else
    if [[ -z "${STEP_03_LINE}" ]]; then
        echo "  FAIL: Step 0.3 not found - cannot verify timing"
    else
        echo "  FAIL: Phase 1 marker not found"
    fi
    ((TESTS_FAILED++))
fi

# Test 5.5: STORY_ID available for path construction (from Step 0.2)
echo ""
echo "Test 5.5: STORY_ID available before detection"
# Step 0.2 should parse STORY_ID, Step 0.3 uses it for path construction
STORY_ID_PARSE=$(grep -n "STORY_ID.*=" "${TARGET_FILE}" | head -1 | cut -d: -f1)
if [[ -n "${STORY_ID_PARSE}" && -n "${STEP_03_LINE}" ]]; then
    if [[ ${STORY_ID_PARSE} -lt ${STEP_03_LINE} ]]; then
        echo "  PASS: STORY_ID parsed (line ${STORY_ID_PARSE}) before Step 0.3 (line ${STEP_03_LINE})"
        ((TESTS_PASSED++))
    else
        echo "  FAIL: STORY_ID should be parsed before Step 0.3"
        ((TESTS_FAILED++))
    fi
elif [[ -z "${STEP_03_LINE}" ]]; then
    echo "  FAIL: Step 0.3 not implemented - cannot verify STORY_ID availability"
    ((TESTS_FAILED++))
else
    echo "  FAIL: STORY_ID parsing not found"
    ((TESTS_FAILED++))
fi

# Summary
echo ""
echo "================================================================"
echo "  SUMMARY: ${AC_NUM}"
echo "================================================================"
echo "  Tests Passed: ${TESTS_PASSED}"
echo "  Tests Failed: ${TESTS_FAILED}"
echo ""

if [[ ${TESTS_FAILED} -eq 0 ]]; then
    echo "RESULT: PASSED"
    exit 0
else
    echo "RESULT: FAILED"
    exit 1
fi
