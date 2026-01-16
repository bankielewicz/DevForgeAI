#!/bin/bash
# =============================================================================
# STORY-266 AC#1: Language Detection from tech-stack.md
# =============================================================================
# Tests that phase-01-deep-validation.md contains Step 1.3 for language
# detection and references tech-stack.md as the authoritative source.
#
# Expected: FAIL (RED state - files don't exist yet)
# =============================================================================

set -e

# Test configuration
PHASE_FILE=".claude/skills/devforgeai-qa/phases/phase-01-deep-validation.md"
PROJECT_ROOT="/mnt/c/Projects/DevForgeAI2"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m' # No Color

TESTS_PASSED=0
TESTS_FAILED=0

# -----------------------------------------------------------------------------
# Test Helper Functions
# -----------------------------------------------------------------------------
test_pass() {
    echo -e "${GREEN}PASS${NC}: $1"
    TESTS_PASSED=$((TESTS_PASSED + 1))
}

test_fail() {
    echo -e "${RED}FAIL${NC}: $1"
    TESTS_FAILED=$((TESTS_FAILED + 1))
}

# -----------------------------------------------------------------------------
# AC#1 Test Cases
# -----------------------------------------------------------------------------

echo "=============================================="
echo "STORY-266 AC#1: Language Detection Tests"
echo "=============================================="
echo ""

# Test 1.1: Phase file exists
echo "Test 1.1: Phase 01 deep validation file exists"
if [ -f "${PROJECT_ROOT}/${PHASE_FILE}" ]; then
    test_pass "Phase file exists: ${PHASE_FILE}"
else
    test_fail "Phase file missing: ${PHASE_FILE}"
fi

# Test 1.2: Step 1.3 section header exists
echo ""
echo "Test 1.2: Step 1.3 section header for runtime smoke test"
if [ -f "${PROJECT_ROOT}/${PHASE_FILE}" ]; then
    if grep -qE "^#+.*Step 1\.3.*[Rr]untime" "${PROJECT_ROOT}/${PHASE_FILE}"; then
        test_pass "Step 1.3 runtime section header found"
    else
        test_fail "Step 1.3 runtime section header NOT found (expected: '## Step 1.3: Runtime Smoke Test' or similar)"
    fi
else
    test_fail "Cannot check Step 1.3 - phase file missing"
fi

# Test 1.3: tech-stack.md referenced as source
echo ""
echo "Test 1.3: tech-stack.md referenced as authoritative source"
if [ -f "${PROJECT_ROOT}/${PHASE_FILE}" ]; then
    if grep -q "tech-stack.md" "${PROJECT_ROOT}/${PHASE_FILE}"; then
        test_pass "tech-stack.md is referenced"
    else
        test_fail "tech-stack.md is NOT referenced (should be authoritative source for language detection)"
    fi
else
    test_fail "Cannot check tech-stack.md reference - phase file missing"
fi

# Test 1.4: Supported languages listed
echo ""
echo "Test 1.4: All 6 supported languages mentioned"
LANGUAGES=("Python" "Node.js" "\.NET" "Go" "Java" "Rust")
if [ -f "${PROJECT_ROOT}/${PHASE_FILE}" ]; then
    for lang in "${LANGUAGES[@]}"; do
        if grep -qiE "$lang" "${PROJECT_ROOT}/${PHASE_FILE}"; then
            test_pass "Language mentioned: ${lang}"
        else
            test_fail "Language NOT mentioned: ${lang}"
        fi
    done
else
    for lang in "${LANGUAGES[@]}"; do
        test_fail "Cannot check language ${lang} - phase file missing"
    done
fi

# Test 1.5: Language detection logging pattern
echo ""
echo "Test 1.5: Language detection logging pattern documented"
if [ -f "${PROJECT_ROOT}/${PHASE_FILE}" ]; then
    if grep -qE "[Dd]etected.*language" "${PROJECT_ROOT}/${PHASE_FILE}"; then
        test_pass "Detection logging pattern found"
    else
        test_fail "Detection logging pattern NOT found (expected: 'Detected project language: {language}')"
    fi
else
    test_fail "Cannot check logging pattern - phase file missing"
fi

# -----------------------------------------------------------------------------
# Summary
# -----------------------------------------------------------------------------
echo ""
echo "=============================================="
echo "AC#1 Test Summary"
echo "=============================================="
echo "Passed: ${TESTS_PASSED}"
echo "Failed: ${TESTS_FAILED}"
echo ""

if [ ${TESTS_FAILED} -gt 0 ]; then
    echo -e "${RED}AC#1 TESTS FAILED (RED state - expected for TDD)${NC}"
    exit 1
else
    echo -e "${GREEN}AC#1 TESTS PASSED${NC}"
    exit 0
fi
