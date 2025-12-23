#!/bin/bash

###############################################################################
# STORY-125 Test Suite Runner
#
# Runs all acceptance criterion tests for STORY-125: DoD Template Extraction
# Provides summary of test results and exit status
###############################################################################

set -o pipefail

# Get the absolute path to this script's directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TEST_COUNT=0
PASSED_COUNT=0
FAILED_COUNT=0
SKIPPED_COUNT=0

echo ""
echo "╔════════════════════════════════════════════════════════════╗"
echo "║  STORY-125: DoD Template Extraction - Test Suite Runner     ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""
echo "Running test suite from: $SCRIPT_DIR"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Test 1: AC#1 Template File Created
echo "[ 1/5 ] Running test-ac1-template-exists.sh..."
if bash "$SCRIPT_DIR/test-ac1-template-exists.sh" > /dev/null 2>&1; then
    echo "        ✓ PASSED"
    PASSED_COUNT=$((PASSED_COUNT + 1))
else
    EXIT_CODE=$?
    if [ $EXIT_CODE -eq 0 ]; then
        echo "        ⊘ SKIPPED"
        SKIPPED_COUNT=$((SKIPPED_COUNT + 1))
    else
        echo "        ✗ FAILED"
        FAILED_COUNT=$((FAILED_COUNT + 1))
    fi
fi
TEST_COUNT=$((TEST_COUNT + 1))
echo ""

# Test 2: AC#2 Template Contains Required Sections
echo "[ 2/5 ] Running test-ac2-template-sections.sh..."
if bash "$SCRIPT_DIR/test-ac2-template-sections.sh" > /dev/null 2>&1; then
    echo "        ✓ PASSED"
    PASSED_COUNT=$((PASSED_COUNT + 1))
else
    EXIT_CODE=$?
    if [ $EXIT_CODE -eq 0 ]; then
        echo "        ⊘ SKIPPED"
        SKIPPED_COUNT=$((SKIPPED_COUNT + 1))
    else
        echo "        ✗ FAILED"
        FAILED_COUNT=$((FAILED_COUNT + 1))
    fi
fi
TEST_COUNT=$((TEST_COUNT + 1))
echo ""

# Test 3: AC#3 dod-update-workflow.md References Template
echo "[ 3/5 ] Running test-ac3-reference-check.sh..."
if bash "$SCRIPT_DIR/test-ac3-reference-check.sh" > /dev/null 2>&1; then
    echo "        ✓ PASSED"
    PASSED_COUNT=$((PASSED_COUNT + 1))
else
    EXIT_CODE=$?
    if [ $EXIT_CODE -eq 0 ]; then
        echo "        ⊘ SKIPPED"
        SKIPPED_COUNT=$((SKIPPED_COUNT + 1))
    else
        echo "        ✗ FAILED"
        FAILED_COUNT=$((FAILED_COUNT + 1))
    fi
fi
TEST_COUNT=$((TEST_COUNT + 1))
echo ""

# Test 4: AC#4 Pre-Commit Hook Validates Against Template
echo "[ 4/5 ] Running test-ac4-validation-format.sh..."
if bash "$SCRIPT_DIR/test-ac4-validation-format.sh" > /dev/null 2>&1; then
    EXIT_CODE=$?
    if [ $EXIT_CODE -eq 0 ]; then
        echo "        ⊘ SKIPPED"
        SKIPPED_COUNT=$((SKIPPED_COUNT + 1))
    else
        echo "        ✓ PASSED"
        PASSED_COUNT=$((PASSED_COUNT + 1))
    fi
else
    echo "        ✗ FAILED"
    FAILED_COUNT=$((FAILED_COUNT + 1))
fi
TEST_COUNT=$((TEST_COUNT + 1))
echo ""

# Test 5: AC#5 Backward Compatibility
echo "[ 5/5 ] Running test-ac5-backward-compat.sh..."
if bash "$SCRIPT_DIR/test-ac5-backward-compat.sh" > /dev/null 2>&1; then
    EXIT_CODE=$?
    if [ $EXIT_CODE -eq 0 ]; then
        echo "        ⊘ SKIPPED"
        SKIPPED_COUNT=$((SKIPPED_COUNT + 1))
    else
        echo "        ✓ PASSED"
        PASSED_COUNT=$((PASSED_COUNT + 1))
    fi
else
    echo "        ✗ FAILED"
    FAILED_COUNT=$((FAILED_COUNT + 1))
fi
TEST_COUNT=$((TEST_COUNT + 1))
echo ""

# Summary
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "Test Summary:"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "  Total Tests:    $TEST_COUNT"
echo "  Passed:         $PASSED_COUNT"
echo "  Failed:         $FAILED_COUNT"
echo "  Skipped:        $SKIPPED_COUNT"
echo ""

# Determine overall status
if [ "$FAILED_COUNT" -gt 0 ]; then
    echo "Overall Status:  RED ❌"
    echo "                 ($FAILED_COUNT test(s) failing)"
    echo ""
    echo "⚠️  TDD Red Phase: Tests are failing as expected"
    echo "                 Implementation needed to make tests GREEN"
    echo ""
    exit 1
elif [ "$PASSED_COUNT" -gt 0 ]; then
    echo "Overall Status:  GREEN ✅"
    echo "                 ($PASSED_COUNT test(s) passing)"
    echo ""
    exit 0
else
    echo "Overall Status:  INCONCLUSIVE"
    echo "                 (All tests skipped)"
    echo ""
    echo "Note: Tests may be skipped due to environment constraints"
    echo "      (Git not initialized, test data not available, etc.)"
    echo ""
    exit 0
fi
