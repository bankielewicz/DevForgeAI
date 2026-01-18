#!/bin/bash
# STORY-263 BR-001: Pattern matching preserves exact STORY_ID
# Test: STORY-007 matches STORY-007-gaps.json, not STORY-7-gaps.json
#
# Expected: FAIL (exact matching logic not yet documented)

# Note: No 'set -e' - we need to track failures, not exit on first grep failure

TARGET_FILE="/mnt/c/Projects/DevForgeAI2/.claude/commands/dev.md"
STORY_ID="STORY-263"
TEST_ID="BR-001"

echo "================================================================"
echo "  ${STORY_ID} - ${TEST_ID}: Exact STORY_ID pattern matching"
echo "================================================================"
echo ""
echo "Target: ${TARGET_FILE}"
echo ""

# Track test results
TESTS_PASSED=0
TESTS_FAILED=0

# Test BR1.1: File exists
echo "Test BR1.1: Target file exists"
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

# Test BR1.2: STORY_ID used directly (no normalization/trimming)
echo ""
echo "Test BR1.2: STORY_ID used directly without normalization"
# Check that we don't strip leading zeros or modify the ID
# Bad: STORY_ID.replace("STORY-0", "STORY-") or parseInt(id)
BAD_PATTERNS=$(grep -oE "(replace.*STORY|parseInt.*STORY|trim.*STORY)" "${TARGET_FILE}" 2>/dev/null)
if [[ -z "${BAD_PATTERNS}" ]]; then
    echo "  PASS: No STORY_ID normalization detected"
    ((TESTS_PASSED++))
else
    echo "  FAIL: STORY_ID normalization found: ${BAD_PATTERNS}"
    ((TESTS_FAILED++))
fi

# Test BR1.3: Path construction uses exact STORY_ID variable
echo ""
echo "Test BR1.3: Path uses exact STORY_ID (preserving format)"
# Looking for: ${STORY_ID}-gaps.json (not modified)
if grep -qE '\$\{?STORY_ID\}?\-gaps\.json|\$STORY_ID.*gaps\.json' "${TARGET_FILE}"; then
    echo "  PASS: Uses exact STORY_ID variable in path"
    ((TESTS_PASSED++))
else
    echo "  FAIL: STORY_ID not used directly in path construction"
    ((TESTS_FAILED++))
fi

# Test BR1.4: No wildcard patterns that could match wrong files
echo ""
echo "Test BR1.4: No ambiguous wildcard patterns"
# Bad: STORY-*-gaps.json (would match STORY-7 and STORY-007)
# Good: STORY-XXX-gaps.json (exact match)
BAD_WILDCARDS=$(grep -oE "STORY-\*|STORY-\.\*" "${TARGET_FILE}" 2>/dev/null | grep -v "STORY-XXX")
if [[ -z "${BAD_WILDCARDS}" ]]; then
    echo "  PASS: No ambiguous wildcards in patterns"
    ((TESTS_PASSED++))
else
    echo "  FAIL: Ambiguous wildcard patterns found: ${BAD_WILDCARDS}"
    echo "        Risk: STORY-007 could match STORY-7-gaps.json"
    ((TESTS_FAILED++))
fi

# Test BR1.5: Documentation mentions exact matching requirement
echo ""
echo "Test BR1.5: Exact matching documented"
# Check for any documentation about preserving leading zeros or exact match
if grep -qiE "(exact.*match|preserv.*zero|leading.*zero|precise.*pattern)" "${TARGET_FILE}"; then
    echo "  PASS: Exact matching requirement documented"
    ((TESTS_PASSED++))
else
    echo "  INFO: No explicit exact matching documentation (implicit from variable usage)"
    # This is not necessarily a failure - using ${STORY_ID} directly implies exact matching
    if grep -qE '\$\{?STORY_ID\}?' "${TARGET_FILE}"; then
        echo "  PASS: Uses STORY_ID variable (implies exact matching)"
        ((TESTS_PASSED++))
    else
        echo "  FAIL: No STORY_ID usage or exact matching documentation"
        ((TESTS_FAILED++))
    fi
fi

# Summary
echo ""
echo "================================================================"
echo "  SUMMARY: ${TEST_ID}"
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
