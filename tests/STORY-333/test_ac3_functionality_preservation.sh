#!/bin/bash
# STORY-333 AC#3: Functionality Preservation (No Regression)
# Tests that all TDD functionality is preserved across core + references
# TDD Red Phase: These tests FAIL until implementation complete

set -e
CORE_FILE="src/claude/agents/test-automator.md"
REF_DIR="src/claude/agents/test-automator/references"

echo "=== AC#3: Functionality Preservation ==="

# Test 1: TDD test generation documented (core or references)
echo -n "Test 1: TDD test generation documented... "
if ! grep -rq "TDD\|Test-Driven" "$CORE_FILE" "$REF_DIR" 2>/dev/null; then
    echo "FAIL"
    exit 1
fi
echo "PASS"

# Test 2: Remediation mode workflow
echo -n "Test 2: Remediation mode documented... "
if ! grep -rqE "MODE.*REMEDIATION|remediation.mode" "$CORE_FILE" "$REF_DIR" 2>/dev/null; then
    echo "FAIL"
    exit 1
fi
echo "PASS"

# Test 3: 4-category exception coverage
echo -n "Test 3: 4-category exception framework... "
CATEGORIES=("HAPPY_PATH" "ERROR_PATHS" "EXCEPTION_HANDLERS" "BOUNDARY_CONDITIONS")
for CAT in "${CATEGORIES[@]}"; do
    if ! grep -rq "$CAT" "$CORE_FILE" "$REF_DIR" 2>/dev/null; then
        echo "FAIL (missing: $CAT)"
        exit 1
    fi
done
echo "PASS"

# Test 4: Technical specification parsing (RCA-006)
echo -n "Test 4: Tech spec dual-source generation... "
if ! grep -rqE "Technical.Specification|dual.source" "$CORE_FILE" "$REF_DIR" 2>/dev/null; then
    echo "FAIL"
    exit 1
fi
echo "PASS"

# Test 5: Framework-specific patterns (3 languages)
echo -n "Test 5: Multi-framework support (Python/JS/C#)... "
FRAMEWORKS=("pytest" "Jest" "xUnit")
for FW in "${FRAMEWORKS[@]}"; do
    if ! grep -rq "$FW" "$CORE_FILE" "$REF_DIR" 2>/dev/null; then
        echo "FAIL (missing: $FW)"
        exit 1
    fi
done
echo "PASS"

# Test 6: Test pyramid distribution
echo -n "Test 6: Test pyramid (70/20/10)... "
if ! grep -rqE "70.*20.*10|pyramid" "$CORE_FILE" "$REF_DIR" 2>/dev/null; then
    echo "FAIL"
    exit 1
fi
echo "PASS"

# Test 7: AAA pattern documented
echo -n "Test 7: AAA pattern documented... "
if ! grep -rqE "Arrange.*Act.*Assert|AAA" "$CORE_FILE" "$REF_DIR" 2>/dev/null; then
    echo "FAIL"
    exit 1
fi
echo "PASS"

echo ""
echo "AC#3: All tests PASSED"
