#!/bin/bash
# Test: AC#4 - No gaps.json for PASSED (Clean) Results
# Story: STORY-345
# Status: RED (failing) - Test written before implementation

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
TARGET_FILE="$PROJECT_ROOT/.claude/skills/devforgeai-qa/references/report-generation.md"

echo "=== AC#4: No gaps.json for PASSED (Clean) Results ==="
echo ""

# Test 1: Verify PASSED status does NOT trigger gap generation
echo "Test 1: PASSED status excluded from gap generation..."
STEP_35=$(sed -n '/## Step 3.5/,/## Step 3.6/p' "$TARGET_FILE")

# Check that generation condition explicitly excludes PASSED
if echo "$STEP_35" | grep -q 'overall_status == "PASS"[^"]' || \
   echo "$STEP_35" | grep -q 'overall_status.*PASS[^E]'; then
    # Need to verify it's conditional, not unconditional
    if ! echo "$STEP_35" | grep -q 'FAIL\|WARNINGS'; then
        echo "FAIL: Gap generation may trigger for PASSED status"
        echo "  Expected: Only FAIL or PASS WITH WARNINGS trigger generation"
        exit 1
    fi
fi

# Test 2: Verify explicit documentation that PASSED skips generation
echo "Test 2: Documentation states PASSED skips generation..."
if ! grep -q 'PASSED.*no gaps\|no gaps.*PASSED\|skip.*PASSED\|PASSED.*skip' "$TARGET_FILE" -i; then
    echo "FAIL: No explicit documentation that PASSED results skip gaps.json"
    echo "  Expected: Clear statement that clean PASSED results don't generate gaps.json"
    exit 1
fi

# Test 3: Verify qa_result PASSED description mentions no file
echo "Test 3: PASSED qa_result indicates no gaps..."
QA_RESULT_SECTION=$(sed -n '/### qa_result Field/,/### /p' "$TARGET_FILE")
if [ -n "$QA_RESULT_SECTION" ]; then
    if ! echo "$QA_RESULT_SECTION" | grep -q 'PASSED.*no gap\|No gap.*PASSED' -i; then
        echo "FAIL: qa_result PASSED description doesn't mention no gaps"
        echo "  Expected: PASSED = no gaps detected"
        exit 1
    fi
fi

# Test 4: Verify generation trigger is conditional
echo "Test 4: Generation trigger is conditional on status..."
if grep -q 'Always generate gaps.json\|unconditional' "$TARGET_FILE" -i; then
    echo "FAIL: Gap generation appears unconditional"
    echo "  Expected: Conditional generation based on status"
    exit 1
fi

echo ""
echo "PASS: AC#4 - PASSED results do not generate gaps.json"
exit 0
