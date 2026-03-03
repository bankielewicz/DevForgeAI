#!/bin/bash
# Test: AC#3 - qa_result Field Reflects Actual Status
# Story: STORY-345
# Status: RED (failing) - Test written before implementation

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
TARGET_FILE="$PROJECT_ROOT/.claude/skills/devforgeai-qa/references/report-generation.md"

echo "=== AC#3: qa_result Field Reflects Actual Status ==="
echo ""

# Test 1: Verify all three qa_result values documented
echo "Test 1: All three qa_result values documented..."
FAILED_DOC=$(grep -c '"FAILED"\|FAILED' "$TARGET_FILE" || true)
WARNINGS_DOC=$(grep -c '"PASS WITH WARNINGS"\|PASS WITH WARNINGS' "$TARGET_FILE" || true)
PASSED_DOC=$(grep -c '"PASSED"\|PASSED' "$TARGET_FILE" || true)

if [ "$FAILED_DOC" -lt 1 ]; then
    echo "FAIL: qa_result 'FAILED' not documented"
    exit 1
fi

if [ "$WARNINGS_DOC" -lt 1 ]; then
    echo "FAIL: qa_result 'PASS WITH WARNINGS' not documented"
    exit 1
fi

if [ "$PASSED_DOC" -lt 1 ]; then
    echo "FAIL: qa_result 'PASSED' not documented"
    exit 1
fi

# Test 2: Verify qa_result field in gaps.json schema
echo "Test 2: qa_result field present in gaps.json schema..."
SCHEMA_SECTION=$(sed -n '/### gaps.json Schema/,/### /p' "$TARGET_FILE")
if ! echo "$SCHEMA_SECTION" | grep -q 'qa_result'; then
    echo "FAIL: qa_result field not in gaps.json schema section"
    echo "  Expected: 'qa_result' field documented in schema"
    exit 1
fi

# Test 3: Verify qa_result logic matches overall_status
echo "Test 3: qa_result derives from overall_status..."
if ! grep -q 'qa_result.*overall_status\|overall_status.*qa_result' "$TARGET_FILE"; then
    # Alternative: check if qa_result is set based on status conditions
    if ! grep -q '"qa_result":' "$TARGET_FILE"; then
        echo "FAIL: qa_result field assignment not documented"
        echo "  Expected: qa_result set from overall_status value"
        exit 1
    fi
fi

# Test 4: Verify qa_result field description exists
echo "Test 4: qa_result field has description..."
if ! grep -q 'qa_result Field\|### qa_result' "$TARGET_FILE"; then
    echo "FAIL: qa_result field lacks dedicated documentation section"
    echo "  Expected: Section explaining qa_result valid values and meaning"
    exit 1
fi

echo ""
echo "PASS: AC#3 - qa_result field accurately reflects QA outcome"
exit 0
