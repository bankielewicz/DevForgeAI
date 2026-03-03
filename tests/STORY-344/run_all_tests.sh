#!/bin/bash
# Run all STORY-344 tests
# Story: STORY-344 - Extend gaps.json Schema with Blocking Field
# Purpose: Execute all AC tests and report summary

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"

cd "$PROJECT_ROOT"

echo "=========================================="
echo "  STORY-344 Test Suite"
echo "  Extend gaps.json Schema with Blocking Field"
echo "=========================================="
echo ""

TOTAL_TESTS=4
PASSED_TESTS=0
FAILED_TESTS=0

# Run AC#1 tests
echo "Running AC#1 tests..."
if bash "$SCRIPT_DIR/test_ac1_schema_documentation_blocking_field.sh"; then
    ((PASSED_TESTS++))
else
    ((FAILED_TESTS++))
fi
echo ""

# Run AC#2 tests
echo "Running AC#2 tests..."
if bash "$SCRIPT_DIR/test_ac2_root_level_qa_result_field.sh"; then
    ((PASSED_TESTS++))
else
    ((FAILED_TESTS++))
fi
echo ""

# Run AC#3 tests
echo "Running AC#3 tests..."
if bash "$SCRIPT_DIR/test_ac3_gap_level_blocking_field.sh"; then
    ((PASSED_TESTS++))
else
    ((FAILED_TESTS++))
fi
echo ""

# Run AC#4 tests
echo "Running AC#4 tests..."
if bash "$SCRIPT_DIR/test_ac4_backward_compatibility.sh"; then
    ((PASSED_TESTS++))
else
    ((FAILED_TESTS++))
fi
echo ""

echo "=========================================="
echo "  STORY-344 Test Summary"
echo "=========================================="
echo "Total AC Tests: $TOTAL_TESTS"
echo "Passed: $PASSED_TESTS"
echo "Failed: $FAILED_TESTS"
echo ""

if [ $FAILED_TESTS -gt 0 ]; then
    echo "OVERALL STATUS: FAIL (expected in TDD RED phase)"
    exit 1
else
    echo "OVERALL STATUS: PASS"
    exit 0
fi
