#!/bin/bash
# =============================================================================
# STORY-266 AC#2: Language-Specific Command Execution
# =============================================================================
# Tests that language-smoke-tests.yaml exists with valid structure and
# contains required fields for each language entry.
#
# Expected: FAIL (RED state - files don't exist yet)
# =============================================================================

set -e

# Test configuration
CONFIG_FILE=".claude/skills/devforgeai-qa/assets/language-smoke-tests.yaml"
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
# AC#2 Test Cases
# -----------------------------------------------------------------------------

echo "=============================================="
echo "STORY-266 AC#2: Command Execution Tests"
echo "=============================================="
echo ""

# Test 2.1: Configuration file exists
echo "Test 2.1: Language configuration file exists"
if [ -f "${PROJECT_ROOT}/${CONFIG_FILE}" ]; then
    test_pass "Config file exists: ${CONFIG_FILE}"
else
    test_fail "Config file missing: ${CONFIG_FILE}"
fi

# Test 2.2: Valid YAML syntax
echo ""
echo "Test 2.2: Valid YAML syntax"
if [ -f "${PROJECT_ROOT}/${CONFIG_FILE}" ]; then
    # Check for basic YAML structure (key: value patterns)
    if grep -qE "^[a-zA-Z_]+:" "${PROJECT_ROOT}/${CONFIG_FILE}"; then
        test_pass "YAML structure appears valid (has key: value patterns)"
    else
        test_fail "YAML structure invalid (no key: value patterns found)"
    fi
else
    test_fail "Cannot check YAML syntax - config file missing"
fi

# Test 2.3: Required fields present for each language
echo ""
echo "Test 2.3: Required fields (detection_pattern, smoke_test_command, entry_point_source, remediation)"
REQUIRED_FIELDS=("detection_pattern" "smoke_test_command" "entry_point_source" "remediation")

if [ -f "${PROJECT_ROOT}/${CONFIG_FILE}" ]; then
    for field in "${REQUIRED_FIELDS[@]}"; do
        if grep -q "${field}:" "${PROJECT_ROOT}/${CONFIG_FILE}"; then
            test_pass "Required field present: ${field}"
        else
            test_fail "Required field missing: ${field}"
        fi
    done
else
    for field in "${REQUIRED_FIELDS[@]}"; do
        test_fail "Cannot check field ${field} - config file missing"
    done
fi

# Test 2.4: All 6 languages have entries
echo ""
echo "Test 2.4: All 6 languages have entries in config"
LANGUAGES=("python" "nodejs" "dotnet" "go" "java" "rust")

if [ -f "${PROJECT_ROOT}/${CONFIG_FILE}" ]; then
    for lang in "${LANGUAGES[@]}"; do
        if grep -qiE "^[[:space:]]*${lang}:" "${PROJECT_ROOT}/${CONFIG_FILE}"; then
            test_pass "Language entry exists: ${lang}"
        else
            test_fail "Language entry missing: ${lang}"
        fi
    done
else
    for lang in "${LANGUAGES[@]}"; do
        test_fail "Cannot check language ${lang} - config file missing"
    done
fi

# Test 2.5: Python command pattern
echo ""
echo "Test 2.5: Python command pattern (python -m)"
if [ -f "${PROJECT_ROOT}/${CONFIG_FILE}" ]; then
    if grep -qE "python -m" "${PROJECT_ROOT}/${CONFIG_FILE}"; then
        test_pass "Python command pattern found (python -m)"
    else
        test_fail "Python command pattern NOT found (expected: python -m {package})"
    fi
else
    test_fail "Cannot check Python command - config file missing"
fi

# Test 2.6: Node.js command pattern
echo ""
echo "Test 2.6: Node.js command pattern (node or npm)"
if [ -f "${PROJECT_ROOT}/${CONFIG_FILE}" ]; then
    if grep -qE "(node |npm )" "${PROJECT_ROOT}/${CONFIG_FILE}"; then
        test_pass "Node.js command pattern found"
    else
        test_fail "Node.js command pattern NOT found (expected: node {entry} or npm start)"
    fi
else
    test_fail "Cannot check Node.js command - config file missing"
fi

# Test 2.7: .NET command pattern
echo ""
echo "Test 2.7: .NET command pattern (dotnet run)"
if [ -f "${PROJECT_ROOT}/${CONFIG_FILE}" ]; then
    if grep -qE "dotnet run" "${PROJECT_ROOT}/${CONFIG_FILE}"; then
        test_pass ".NET command pattern found (dotnet run)"
    else
        test_fail ".NET command pattern NOT found (expected: dotnet run --project)"
    fi
else
    test_fail "Cannot check .NET command - config file missing"
fi

# Test 2.8: Go command pattern
echo ""
echo "Test 2.8: Go command pattern (go run)"
if [ -f "${PROJECT_ROOT}/${CONFIG_FILE}" ]; then
    if grep -qE "go run" "${PROJECT_ROOT}/${CONFIG_FILE}"; then
        test_pass "Go command pattern found (go run)"
    else
        test_fail "Go command pattern NOT found (expected: go run)"
    fi
else
    test_fail "Cannot check Go command - config file missing"
fi

# Test 2.9: Java command pattern
echo ""
echo "Test 2.9: Java command pattern (java -jar)"
if [ -f "${PROJECT_ROOT}/${CONFIG_FILE}" ]; then
    if grep -qE "java -jar" "${PROJECT_ROOT}/${CONFIG_FILE}"; then
        test_pass "Java command pattern found (java -jar)"
    else
        test_fail "Java command pattern NOT found (expected: java -jar)"
    fi
else
    test_fail "Cannot check Java command - config file missing"
fi

# Test 2.10: Rust command pattern
echo ""
echo "Test 2.10: Rust command pattern (cargo run)"
if [ -f "${PROJECT_ROOT}/${CONFIG_FILE}" ]; then
    if grep -qE "cargo run" "${PROJECT_ROOT}/${CONFIG_FILE}"; then
        test_pass "Rust command pattern found (cargo run)"
    else
        test_fail "Rust command pattern NOT found (expected: cargo run)"
    fi
else
    test_fail "Cannot check Rust command - config file missing"
fi

# Test 2.11: Timeout configuration (10 seconds)
echo ""
echo "Test 2.11: Timeout configuration (10 seconds)"
if [ -f "${PROJECT_ROOT}/${CONFIG_FILE}" ]; then
    if grep -qE "timeout.*10|10.*second" "${PROJECT_ROOT}/${CONFIG_FILE}"; then
        test_pass "Timeout configuration found (10 seconds)"
    else
        test_fail "Timeout configuration NOT found (expected: 10 seconds)"
    fi
else
    test_fail "Cannot check timeout - config file missing"
fi

# -----------------------------------------------------------------------------
# Summary
# -----------------------------------------------------------------------------
echo ""
echo "=============================================="
echo "AC#2 Test Summary"
echo "=============================================="
echo "Passed: ${TESTS_PASSED}"
echo "Failed: ${TESTS_FAILED}"
echo ""

if [ ${TESTS_FAILED} -gt 0 ]; then
    echo -e "${RED}AC#2 TESTS FAILED (RED state - expected for TDD)${NC}"
    exit 1
else
    echo -e "${GREEN}AC#2 TESTS PASSED${NC}"
    exit 0
fi
