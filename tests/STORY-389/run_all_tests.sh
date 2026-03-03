#!/bin/bash
# Run all STORY-389 tests
# STORY-389: Update Agent-Generator with Template Compliance Enforcement
#
# Executes all 7 AC test files and produces aggregate summary

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "======================================================"
echo "STORY-389: Agent-Generator Template Compliance Tests"
echo "======================================================"
echo ""

TOTAL_FILES=0
PASSED_FILES=0
FAILED_FILES=0
FAILED_LIST=""

for test_file in "$SCRIPT_DIR"/test_ac*.sh; do
    if [ -f "$test_file" ]; then
        TOTAL_FILES=$((TOTAL_FILES + 1))
        test_name=$(basename "$test_file" .sh)
        echo "--- Running: $test_name ---"
        bash "$test_file"
        if [ $? -eq 0 ]; then
            PASSED_FILES=$((PASSED_FILES + 1))
        else
            FAILED_FILES=$((FAILED_FILES + 1))
            FAILED_LIST="$FAILED_LIST  - $test_name\n"
        fi
        echo ""
    fi
done

echo "======================================================"
echo "AGGREGATE SUMMARY"
echo "======================================================"
echo "Total test files: $TOTAL_FILES"
echo "Passed: $PASSED_FILES"
echo "Failed: $FAILED_FILES"

if [ "$FAILED_FILES" -gt 0 ]; then
    echo ""
    echo "Failed test files:"
    echo -e "$FAILED_LIST"
    echo "Status: FAILED"
    exit 1
else
    echo "Status: ALL PASSED"
    exit 0
fi
