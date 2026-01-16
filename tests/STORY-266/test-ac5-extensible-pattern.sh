#!/bin/bash
# =============================================================================
# STORY-266 AC#5: Extensible Language Detection Pattern
# =============================================================================
# Tests that the language configuration is extensible and adding a new
# language requires only configuration changes (not code changes).
#
# Expected: FAIL (RED state - files don't exist yet)
# =============================================================================

set -e

# Test configuration
CONFIG_FILE=".claude/skills/devforgeai-qa/assets/language-smoke-tests.yaml"
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
# AC#5 Test Cases
# -----------------------------------------------------------------------------

echo "=============================================="
echo "STORY-266 AC#5: Extensible Pattern Tests"
echo "=============================================="
echo ""

# Test 5.1: Config has all 6 languages
echo "Test 5.1: Configuration contains all 6 languages"
LANGUAGES=("python" "nodejs" "dotnet" "go" "java" "rust")
LANG_COUNT=0

if [ -f "${PROJECT_ROOT}/${CONFIG_FILE}" ]; then
    for lang in "${LANGUAGES[@]}"; do
        if grep -qiE "^[[:space:]]*${lang}:" "${PROJECT_ROOT}/${CONFIG_FILE}"; then
            LANG_COUNT=$((LANG_COUNT + 1))
        fi
    done

    if [ ${LANG_COUNT} -eq 6 ]; then
        test_pass "All 6 languages present in config"
    else
        test_fail "Only ${LANG_COUNT}/6 languages found in config"
    fi
else
    test_fail "Cannot check languages - config file missing"
fi

# Test 5.2: Each language has detection_pattern
echo ""
echo "Test 5.2: Each language has detection_pattern field"
if [ -f "${PROJECT_ROOT}/${CONFIG_FILE}" ]; then
    PATTERN_COUNT=$(grep -c "detection_pattern:" "${PROJECT_ROOT}/${CONFIG_FILE}" 2>/dev/null || echo "0")
    if [ "${PATTERN_COUNT}" -ge 6 ]; then
        test_pass "detection_pattern field present for languages (${PATTERN_COUNT} found)"
    else
        test_fail "detection_pattern field missing (found ${PATTERN_COUNT}, need >= 6)"
    fi
else
    test_fail "Cannot check detection_pattern - config file missing"
fi

# Test 5.3: Each language has smoke_test_command
echo ""
echo "Test 5.3: Each language has smoke_test_command field"
if [ -f "${PROJECT_ROOT}/${CONFIG_FILE}" ]; then
    CMD_COUNT=$(grep -c "smoke_test_command:" "${PROJECT_ROOT}/${CONFIG_FILE}" 2>/dev/null || echo "0")
    if [ "${CMD_COUNT}" -ge 6 ]; then
        test_pass "smoke_test_command field present for languages (${CMD_COUNT} found)"
    else
        test_fail "smoke_test_command field missing (found ${CMD_COUNT}, need >= 6)"
    fi
else
    test_fail "Cannot check smoke_test_command - config file missing"
fi

# Test 5.4: Each language has entry_point_source
echo ""
echo "Test 5.4: Each language has entry_point_source field"
if [ -f "${PROJECT_ROOT}/${CONFIG_FILE}" ]; then
    ENTRY_COUNT=$(grep -c "entry_point_source:" "${PROJECT_ROOT}/${CONFIG_FILE}" 2>/dev/null || echo "0")
    if [ "${ENTRY_COUNT}" -ge 6 ]; then
        test_pass "entry_point_source field present for languages (${ENTRY_COUNT} found)"
    else
        test_fail "entry_point_source field missing (found ${ENTRY_COUNT}, need >= 6)"
    fi
else
    test_fail "Cannot check entry_point_source - config file missing"
fi

# Test 5.5: Each language has remediation_guidance
echo ""
echo "Test 5.5: Each language has remediation_guidance (or remediation) field"
if [ -f "${PROJECT_ROOT}/${CONFIG_FILE}" ]; then
    REM_COUNT=$(grep -cE "remediation(_guidance)?:" "${PROJECT_ROOT}/${CONFIG_FILE}" 2>/dev/null || echo "0")
    if [ "${REM_COUNT}" -ge 6 ]; then
        test_pass "remediation field present for languages (${REM_COUNT} found)"
    else
        test_fail "remediation field missing (found ${REM_COUNT}, need >= 6)"
    fi
else
    test_fail "Cannot check remediation - config file missing"
fi

# Test 5.6: Documentation explains extensibility
echo ""
echo "Test 5.6: Documentation explains how to extend languages"
if [ -f "${PROJECT_ROOT}/${PHASE_FILE}" ]; then
    if grep -qiE "extend|add.*language|new.*language|config.*only" "${PROJECT_ROOT}/${PHASE_FILE}"; then
        test_pass "Extensibility documentation found"
    else
        test_fail "Extensibility documentation NOT found (should explain adding new languages)"
    fi
else
    test_fail "Cannot check extensibility docs - phase file missing"
fi

# Test 5.7: Config uses YAML dictionary format
echo ""
echo "Test 5.7: Config uses structured YAML dictionary format"
if [ -f "${PROJECT_ROOT}/${CONFIG_FILE}" ]; then
    # Check for indented structure (dictionary pattern)
    if grep -qE "^[[:space:]]+[a-z_]+:" "${PROJECT_ROOT}/${CONFIG_FILE}"; then
        test_pass "YAML dictionary structure detected"
    else
        test_fail "YAML dictionary structure NOT detected (expected nested keys)"
    fi
else
    test_fail "Cannot check YAML structure - config file missing"
fi

# Test 5.8: No hardcoded language logic in phase file
echo ""
echo "Test 5.8: No hardcoded language-specific logic in workflow"
if [ -f "${PROJECT_ROOT}/${PHASE_FILE}" ]; then
    # Check that the workflow references config, not hardcoded languages
    if grep -qiE "config|language-smoke-tests\.yaml" "${PROJECT_ROOT}/${PHASE_FILE}"; then
        test_pass "Phase file references config (not hardcoded)"
    else
        test_fail "Phase file should reference language-smoke-tests.yaml for extensibility"
    fi
else
    test_fail "Cannot check for hardcoding - phase file missing"
fi

# Test 5.9: Config file location documented
echo ""
echo "Test 5.9: Config file location documented in phase file"
if [ -f "${PROJECT_ROOT}/${PHASE_FILE}" ]; then
    if grep -qE "\.claude/skills/devforgeai-qa/assets/|language-smoke-tests\.yaml" "${PROJECT_ROOT}/${PHASE_FILE}"; then
        test_pass "Config file location documented"
    else
        test_fail "Config file location NOT documented"
    fi
else
    test_fail "Cannot check config location docs - phase file missing"
fi

# -----------------------------------------------------------------------------
# Summary
# -----------------------------------------------------------------------------
echo ""
echo "=============================================="
echo "AC#5 Test Summary"
echo "=============================================="
echo "Passed: ${TESTS_PASSED}"
echo "Failed: ${TESTS_FAILED}"
echo ""

if [ ${TESTS_FAILED} -gt 0 ]; then
    echo -e "${RED}AC#5 TESTS FAILED (RED state - expected for TDD)${NC}"
    exit 1
else
    echo -e "${GREEN}AC#5 TESTS PASSED${NC}"
    exit 0
fi
