#!/bin/bash
# STORY-267 AC#3: Project Type Detection Logic Documented
# Test: CLI/API/Library classification with decision table
#
# Expected: FAIL (documentation not yet expanded with decision table)

# Note: No 'set -e' - we need to track failures, not exit on first grep failure

TARGET_FILE="/mnt/c/Projects/DevForgeAI2/.claude/skills/devforgeai-qa/references/deep-validation-workflow.md"
STORY_ID="STORY-267"
AC_NUM="AC#3"

echo "================================================================"
echo "  ${STORY_ID} - ${AC_NUM}: Project Type Detection Logic Documented"
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

# Test 3.1: CLI project type documented
echo "Test 3.1: CLI project type detection documented"
if echo "${SECTION_CONTENT}" | grep -qiE "CLI.*(detect|project|type)|project type.*CLI|(command.line|command-line).*interface"; then
    echo "  PASS: CLI project type documented"
    ((TESTS_PASSED++))
else
    echo "  FAIL: CLI project type detection not documented"
    ((TESTS_FAILED++))
fi

# Test 3.2: API project type documented
echo ""
echo "Test 3.2: API project type detection documented"
if echo "${SECTION_CONTENT}" | grep -qiE "API.*(detect|project|type|skip)|project type.*API|web.*(service|server)|REST|GraphQL"; then
    echo "  PASS: API project type documented"
    ((TESTS_PASSED++))
else
    echo "  FAIL: API project type detection not documented"
    ((TESTS_FAILED++))
fi

# Test 3.3: Library project type documented
echo ""
echo "Test 3.3: Library project type detection documented"
if echo "${SECTION_CONTENT}" | grep -qiE "library.*(detect|project|type|skip)|project type.*library|package.*library"; then
    echo "  PASS: Library project type documented"
    ((TESTS_PASSED++))
else
    echo "  FAIL: Library project type detection not documented"
    ((TESTS_FAILED++))
fi

# Test 3.4: Detection priority documented (tech-stack.md authoritative > file system fallback)
echo ""
echo "Test 3.4: Detection priority documented (tech-stack.md authoritative)"
if echo "${SECTION_CONTENT}" | grep -qiE "tech-stack.md.*(authoritative|priority|source)|priority.*(tech-stack|detection)|authoritative.*source"; then
    echo "  PASS: Detection priority (tech-stack.md authoritative) documented"
    ((TESTS_PASSED++))
else
    echo "  FAIL: Detection priority not documented"
    ((TESTS_FAILED++))
fi

# Test 3.5: Decision table or flowchart exists
echo ""
echo "Test 3.5: Decision table or flowchart for project type detection"

# Look for table format (markdown tables have | characters)
TABLE_EXISTS=false
FLOWCHART_EXISTS=false

# Check for decision table
if echo "${SECTION_CONTENT}" | grep -qE "\|.*(CLI|API|Library|Project Type).*\|"; then
    TABLE_EXISTS=true
fi

# Check for flowchart/decision tree (mermaid or text-based)
if echo "${SECTION_CONTENT}" | grep -qiE "(flowchart|decision tree|mermaid|graph|IF.*THEN|-->)"; then
    FLOWCHART_EXISTS=true
fi

# Check for structured decision logic
if echo "${SECTION_CONTENT}" | grep -qE "^\s*(IF|WHEN|CASE).*:"; then
    FLOWCHART_EXISTS=true
fi

if [[ "${TABLE_EXISTS}" == true ]]; then
    echo "  PASS: Decision table found"
    ((TESTS_PASSED++))
elif [[ "${FLOWCHART_EXISTS}" == true ]]; then
    echo "  PASS: Decision flowchart/tree found"
    ((TESTS_PASSED++))
else
    echo "  FAIL: No decision table or flowchart found"
    echo "        Expected: Table with Project Type, Detection Method, Smoke Test Action columns"
    ((TESTS_FAILED++))
fi

# Test 3.6: Each project type has smoke test action documented
echo ""
echo "Test 3.6: Smoke test action for each project type"
ACTION_COUNT=0

# CLI should have run/execute action
if echo "${SECTION_CONTENT}" | grep -qiE "CLI.*(run|execute|smoke|test)|smoke test.*CLI"; then
    echo "  - CLI smoke test action: FOUND"
    ((ACTION_COUNT++))
else
    echo "  - CLI smoke test action: NOT FOUND"
fi

# API may have skip or health check
if echo "${SECTION_CONTENT}" | grep -qiE "API.*(skip|health|endpoint)|API.*smoke"; then
    echo "  - API smoke test action: FOUND"
    ((ACTION_COUNT++))
else
    echo "  - API smoke test action: NOT FOUND"
fi

# Library should have skip rationale
if echo "${SECTION_CONTENT}" | grep -qiE "library.*(skip|not applicable)|skip.*library"; then
    echo "  - Library smoke test action: FOUND (skip)"
    ((ACTION_COUNT++))
else
    echo "  - Library smoke test action: NOT FOUND"
fi

if [[ ${ACTION_COUNT} -ge 3 ]]; then
    echo "  PASS: All project types have documented smoke test actions"
    ((TESTS_PASSED++))
else
    echo "  FAIL: Missing smoke test actions for some project types (${ACTION_COUNT}/3)"
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
