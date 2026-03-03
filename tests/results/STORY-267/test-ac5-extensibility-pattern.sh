#!/bin/bash
# STORY-267 AC#5: Extensibility Pattern Documented
# Test: Configuration file reference and example YAML entry for new languages
#
# Expected: FAIL (documentation not yet expanded with extensibility pattern)

# Note: No 'set -e' - we need to track failures, not exit on first grep failure

TARGET_FILE="/mnt/c/Projects/DevForgeAI2/.claude/skills/devforgeai-qa/references/deep-validation-workflow.md"
STORY_ID="STORY-267"
AC_NUM="AC#5"

echo "================================================================"
echo "  ${STORY_ID} - ${AC_NUM}: Extensibility Pattern Documented"
echo "================================================================"
echo ""
echo "Target: ${TARGET_FILE}"
echo ""

# Track test results
TESTS_PASSED=0
TESTS_FAILED=0

# Check file exists
if [[ ! -f "${TARGET_FILE}" ]]; then
    echo "FAIL: Target file does not exist"
    exit 1
fi

# Extract the Runtime Smoke Test section
SECTION_CONTENT=""
if grep -q "^### 1\.4 Runtime Smoke Test" "${TARGET_FILE}"; then
    SECTION_CONTENT=$(sed -n '/^### 1\.4 Runtime Smoke Test/,/^##[#]* [0-9]/p' "${TARGET_FILE}")
elif grep -q "^### 1\.3 Runtime Smoke Test" "${TARGET_FILE}"; then
    echo "Note: Section 1.4 not found, checking section 1.3 (current state)"
    SECTION_CONTENT=$(sed -n '/^### 1\.3 Runtime Smoke Test/,/^##[#]* [0-9]/p' "${TARGET_FILE}")
fi

# Test 5.1: Configuration file location documented
echo "Test 5.1: Configuration file location documented"
# Per AC#5: ".claude/skills/devforgeai-qa/assets/language-smoke-tests.yaml"
if echo "${SECTION_CONTENT}" | grep -qE "language-smoke-tests\.yaml|language-smoke-tests\.yml"; then
    echo "  PASS: Configuration file (language-smoke-tests.yaml) referenced"
    ((TESTS_PASSED++))
else
    echo "  FAIL: Configuration file reference not found"
    echo "        Expected: language-smoke-tests.yaml"
    ((TESTS_FAILED++))
fi

# Test 5.2: Full path to configuration file documented
echo ""
echo "Test 5.2: Full configuration file path documented"
if echo "${SECTION_CONTENT}" | grep -qE "\.claude/skills/devforgeai-qa/assets/language-smoke-tests\.yaml"; then
    echo "  PASS: Full path to configuration file documented"
    ((TESTS_PASSED++))
else
    echo "  FAIL: Full path not documented"
    echo "        Expected: .claude/skills/devforgeai-qa/assets/language-smoke-tests.yaml"
    ((TESTS_FAILED++))
fi

# Test 5.3: Required fields per language entry documented
echo ""
echo "Test 5.3: Required fields per language entry documented"
FIELDS_FOUND=0

# Check for each required field
if echo "${SECTION_CONTENT}" | grep -qiE "detection_pattern|detection.pattern"; then
    echo "  - detection_pattern: FOUND"
    ((FIELDS_FOUND++))
else
    echo "  - detection_pattern: NOT FOUND"
fi

if echo "${SECTION_CONTENT}" | grep -qiE "smoke_test_command|smoke.test.command"; then
    echo "  - smoke_test_command: FOUND"
    ((FIELDS_FOUND++))
else
    echo "  - smoke_test_command: NOT FOUND"
fi

if echo "${SECTION_CONTENT}" | grep -qiE "entry_point_source|entry.point.source"; then
    echo "  - entry_point_source: FOUND"
    ((FIELDS_FOUND++))
else
    echo "  - entry_point_source: NOT FOUND"
fi

if echo "${SECTION_CONTENT}" | grep -qiE "remediation|remediation_guidance"; then
    echo "  - remediation: FOUND"
    ((FIELDS_FOUND++))
else
    echo "  - remediation: NOT FOUND"
fi

if [[ ${FIELDS_FOUND} -ge 3 ]]; then
    echo "  PASS: Required fields documented (${FIELDS_FOUND}/4)"
    ((TESTS_PASSED++))
else
    echo "  FAIL: Insufficient required fields documented (${FIELDS_FOUND}/4)"
    ((TESTS_FAILED++))
fi

# Test 5.4: Example YAML configuration entry exists
echo ""
echo "Test 5.4: Example YAML configuration entry exists"
YAML_BLOCK=$(echo "${SECTION_CONTENT}" | sed -n '/```yaml/,/```/p')

if [[ -n "${YAML_BLOCK}" ]]; then
    # Check if YAML contains language configuration structure
    if echo "${YAML_BLOCK}" | grep -qiE "(languages:|kotlin:|swift:|detection_pattern:|smoke_test_command:)"; then
        echo "  PASS: Example YAML configuration found"
        ((TESTS_PASSED++))
    else
        echo "  FAIL: YAML block found but missing language configuration structure"
        ((TESTS_FAILED++))
    fi
else
    echo "  FAIL: No YAML code block found"
    echo "        Expected: Example YAML entry for adding new language"
    ((TESTS_FAILED++))
fi

# Test 5.5: Example shows new language (not existing 6)
echo ""
echo "Test 5.5: Example uses new language (e.g., Kotlin, Swift)"
if echo "${SECTION_CONTENT}" | grep -qiE "(kotlin|swift|scala|elixir|ruby|php):"; then
    echo "  PASS: Example shows new language entry (not one of existing 6)"
    ((TESTS_PASSED++))
else
    echo "  FAIL: No new language example found"
    echo "        Expected: Example for Kotlin, Swift, or similar new language"
    ((TESTS_FAILED++))
fi

# Test 5.6: Configuration-only extension emphasized
echo ""
echo "Test 5.6: Configuration-only extension documented (no code modification)"
if echo "${SECTION_CONTENT}" | grep -qiE "(no code.*(modification|change)|configuration.only|config.only|without.*(code|modif))"; then
    echo "  PASS: Configuration-only extension documented"
    ((TESTS_PASSED++))
else
    echo "  FAIL: Configuration-only extension not emphasized"
    echo "        Expected: Statement that no code modification is required"
    ((TESTS_FAILED++))
fi

# Test 5.7: Verification steps documented
echo ""
echo "Test 5.7: Verification steps for new language support"
if echo "${SECTION_CONTENT}" | grep -qiE "(verification|verify|test|confirm).*new.*(language|support)|new.*(language|support).*(verification|verify|test)"; then
    echo "  PASS: Verification steps documented"
    ((TESTS_PASSED++))
else
    echo "  FAIL: Verification steps not documented"
    echo "        Expected: Steps to confirm new language support works"
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
