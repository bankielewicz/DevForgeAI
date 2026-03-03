#!/bin/bash
# Test: AC#5 - Observation Capture Section (EPIC-052 Compliance)
# Story: STORY-332 - Refactor session-miner.md with Progressive Disclosure
# Purpose: Verify Observation Capture section with 7 categories and 3-step workflow
#
# Expected: FAIL (Red phase) - Refactored file does not exist yet

# set -e  # Removed to allow all tests to run

# Configuration
CORE_FILE="src/claude/agents/session-miner.md"

# 7 observation categories required by EPIC-052
OBSERVATION_CATEGORIES=(
    "friction"
    "success"
    "pattern"
    "gap"
    "idea"
    "bug"
    "warning"
)

# 3-step workflow components
WORKFLOW_STEPS=(
    "Construct.*JSON|JSON.*construct|Build.*observation|Output Format"
    "Write.*Disk|disk.*write|Write.file_path|Write Protocol"
    "Verify.*Write|write.*verify|Confirm.*file|devforgeai/feedback"
)

WORKFLOW_DESCRIPTIONS=(
    "Step 1: Construct JSON"
    "Step 2: Write to Disk"
    "Step 3: Verify Write"
)

# Test tracking
TESTS_PASSED=0
TESTS_FAILED=0

echo "=============================================="
echo "  AC#5: Observation Capture Section Tests"
echo "  STORY-332 - Progressive Disclosure Refactor"
echo "=============================================="
echo ""

# Test 1: Verify core file exists
echo "Test 1: Core file exists"
if [[ -f "$CORE_FILE" ]]; then
    echo "  PASS: $CORE_FILE exists"
    ((TESTS_PASSED++))
else
    echo "  FAIL: $CORE_FILE does not exist"
    ((TESTS_FAILED++))
    echo ""
    echo "=============================================="
    echo "  RESULT: $TESTS_PASSED passed, $TESTS_FAILED failed"
    echo "  STATUS: FAILED (cannot continue without file)"
    echo "=============================================="
    exit 1
fi

# Test 2: Verify Observation Capture section exists with MANDATORY marker
echo ""
echo "Test 2: Observation Capture section exists with MANDATORY marker"
if grep -qE "^## Observation Capture.*MANDATORY|^## Observation Capture" "$CORE_FILE"; then
    echo "  PASS: Observation Capture section found"
    ((TESTS_PASSED++))

    # Additional check for MANDATORY marker
    if grep -qE "MANDATORY" "$CORE_FILE"; then
        echo "  INFO: MANDATORY marker present"
    fi
else
    echo "  FAIL: Observation Capture section not found"
    echo "  Expected: '## Observation Capture (MANDATORY)' or '## Observation Capture'"
    ((TESTS_FAILED++))
fi

# Test 3: Verify all 7 observation categories present
echo ""
echo "Test 3: All 7 observation categories documented"
CATEGORIES_FOUND=0
MISSING_CATEGORIES=()

for category in "${OBSERVATION_CATEGORIES[@]}"; do
    if grep -qiE "$category" "$CORE_FILE"; then
        ((CATEGORIES_FOUND++))
    else
        MISSING_CATEGORIES+=("$category")
    fi
done

if [[ $CATEGORIES_FOUND -eq 7 ]]; then
    echo "  PASS: All 7 observation categories found"
    ((TESTS_PASSED++))
else
    echo "  FAIL: Only $CATEGORIES_FOUND/7 categories found"
    echo "  Missing categories:"
    for cat in "${MISSING_CATEGORIES[@]}"; do
        echo "    - $cat"
    done
    ((TESTS_FAILED++))
fi

# Test 4: Verify severity levels documented
echo ""
echo "Test 4: Severity levels documented"
SEVERITY_LEVELS=("low" "medium" "high")
SEVERITY_FOUND=0

for level in "${SEVERITY_LEVELS[@]}"; do
    if grep -qiE "severity.*$level|$level.*severity|\"$level\"|\\[$level" "$CORE_FILE"; then
        ((SEVERITY_FOUND++))
    fi
done

if [[ $SEVERITY_FOUND -ge 2 ]]; then
    echo "  PASS: Severity levels documented ($SEVERITY_FOUND/3)"
    ((TESTS_PASSED++))
else
    echo "  FAIL: Severity levels incomplete ($SEVERITY_FOUND/3)"
    echo "  Expected: low, medium, high severity levels"
    ((TESTS_FAILED++))
fi

# Test 5: Verify 3-step workflow documented
echo ""
echo "Test 5: 3-step observation workflow documented"
STEPS_FOUND=0
MISSING_STEPS=()

for i in "${!WORKFLOW_STEPS[@]}"; do
    pattern="${WORKFLOW_STEPS[$i]}"
    description="${WORKFLOW_DESCRIPTIONS[$i]}"

    if grep -qiE "$pattern" "$CORE_FILE"; then
        ((STEPS_FOUND++))
    else
        MISSING_STEPS+=("$description")
    fi
done

if [[ $STEPS_FOUND -eq 3 ]]; then
    echo "  PASS: All 3 workflow steps documented"
    ((TESTS_PASSED++))
else
    echo "  FAIL: Only $STEPS_FOUND/3 workflow steps found"
    echo "  Missing steps:"
    for step in "${MISSING_STEPS[@]}"; do
        echo "    - $step"
    done
    ((TESTS_FAILED++))
fi

# Test 6: Verify observation JSON schema elements
echo ""
echo "Test 6: Observation JSON schema elements present"
SCHEMA_ELEMENTS=(
    "subagent"
    "category"
    "note"
    "severity"
    "files"
)
SCHEMA_FOUND=0

for element in "${SCHEMA_ELEMENTS[@]}"; do
    # Check for YAML format (element:) or JSON format ("element":) or list format (- element:)
    if grep -qiE "\"$element\":|$element:|-.*$element" "$CORE_FILE"; then
        ((SCHEMA_FOUND++))
    fi
done

if [[ $SCHEMA_FOUND -ge 4 ]]; then
    echo "  PASS: JSON schema elements found ($SCHEMA_FOUND/5)"
    ((TESTS_PASSED++))
else
    echo "  FAIL: JSON schema incomplete ($SCHEMA_FOUND/5)"
    echo "  Expected: subagent, category, note, severity, files"
    ((TESTS_FAILED++))
fi

# Test 7: Verify output path pattern for observations
echo ""
echo "Test 7: Observation output path documented"
if grep -qE "devforgeai/feedback/ai-analysis|feedback/.*analysis" "$CORE_FILE"; then
    echo "  PASS: Observation output path documented"
    ((TESTS_PASSED++))
else
    echo "  FAIL: Observation output path not found"
    echo "  Expected: Path like devforgeai/feedback/ai-analysis/{STORY_ID}/"
    ((TESTS_FAILED++))
fi

# Summary
echo ""
echo "=============================================="
echo "  AC#5 TEST SUMMARY"
echo "=============================================="
echo "  Tests passed: $TESTS_PASSED"
echo "  Tests failed: $TESTS_FAILED"
echo ""

if [[ $TESTS_FAILED -eq 0 ]]; then
    echo "  STATUS: PASSED - All AC#5 requirements met"
    exit 0
else
    echo "  STATUS: FAILED - $TESTS_FAILED requirement(s) not met"
    exit 1
fi
