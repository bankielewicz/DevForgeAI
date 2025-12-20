#!/bin/bash
# STORY-113 AC#4: Consistent Error Handling
# Tests that QA and Release skills use same error handling patterns as orchestration skill


SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../../.." && pwd)"

# Test configuration
QA_SKILL_PATH="$PROJECT_ROOT/.claude/skills/devforgeai-qa/SKILL.md"
RELEASE_SKILL_PATH="$PROJECT_ROOT/.claude/skills/devforgeai-release/SKILL.md"
QA_REF_PATH="$PROJECT_ROOT/.claude/skills/devforgeai-qa/references/parallel-validation.md"
RELEASE_REF_PATH="$PROJECT_ROOT/.claude/skills/devforgeai-release/references/parallel-smoke-tests.md"
ERROR_PATTERNS_PATH="$PROJECT_ROOT/.claude/skills/devforgeai-orchestration/references/error-handling-patterns.md"

echo "=============================================="
echo "STORY-113 AC#4: Consistent Error Handling"
echo "=============================================="

TESTS_PASSED=0
TESTS_FAILED=0

# Test 1: Error handling patterns file exists (prerequisite)
echo ""
echo "Test 1: Error handling patterns file exists (STORY-110)"
if [ -f "$ERROR_PATTERNS_PATH" ]; then
    echo "  ✓ PASS: error-handling-patterns.md exists"
    ((TESTS_PASSED++))
else
    echo "  ✗ FAIL: error-handling-patterns.md not found (STORY-110 dependency)"
    ((TESTS_FAILED++))
fi

# Test 2: QA reference uses PartialResult model
echo ""
echo "Test 2: QA reference uses PartialResult model"
if [ -f "$QA_REF_PATH" ]; then
    if grep -qi "PartialResult\|partial.*result" "$QA_REF_PATH"; then
        echo "  ✓ PASS: QA uses PartialResult model"
        ((TESTS_PASSED++))
    else
        echo "  ✗ FAIL: PartialResult not found in QA reference"
        ((TESTS_FAILED++))
    fi
else
    echo "  ✗ FAIL: QA reference file missing"
    ((TESTS_FAILED++))
fi

# Test 3: Release reference uses PartialResult model
echo ""
echo "Test 3: Release reference uses PartialResult model"
if [ -f "$RELEASE_REF_PATH" ]; then
    if grep -qi "PartialResult\|partial.*result" "$RELEASE_REF_PATH"; then
        echo "  ✓ PASS: Release uses PartialResult model"
        ((TESTS_PASSED++))
    else
        echo "  ✗ FAIL: PartialResult not found in Release reference"
        ((TESTS_FAILED++))
    fi
else
    echo "  ✗ FAIL: Release reference file missing"
    ((TESTS_FAILED++))
fi

# Test 4: QA has min_success_rate threshold
echo ""
echo "Test 4: QA has min_success_rate threshold"
if [ -f "$QA_REF_PATH" ]; then
    if grep -qi "min_success_rate\|success_rate\|threshold" "$QA_REF_PATH"; then
        echo "  ✓ PASS: QA has success rate threshold"
        ((TESTS_PASSED++))
    else
        echo "  ✗ FAIL: Success rate threshold not found in QA"
        ((TESTS_FAILED++))
    fi
else
    echo "  ✗ FAIL: QA reference file missing"
    ((TESTS_FAILED++))
fi

# Test 5: Release has min_success_rate threshold
echo ""
echo "Test 5: Release has min_success_rate threshold"
if [ -f "$RELEASE_REF_PATH" ]; then
    if grep -qi "min_success_rate\|success_rate\|threshold" "$RELEASE_REF_PATH"; then
        echo "  ✓ PASS: Release has success rate threshold"
        ((TESTS_PASSED++))
    else
        echo "  ✗ FAIL: Success rate threshold not found in Release"
        ((TESTS_FAILED++))
    fi
else
    echo "  ✗ FAIL: Release reference file missing"
    ((TESTS_FAILED++))
fi

# Test 6: References cross-reference error-handling-patterns.md
echo ""
echo "Test 6: References cite error-handling-patterns.md"
CITED=0
if [ -f "$QA_REF_PATH" ] && grep -qi "error-handling-patterns\|STORY-110" "$QA_REF_PATH"; then
    ((CITED++))
fi
if [ -f "$RELEASE_REF_PATH" ] && grep -qi "error-handling-patterns\|STORY-110" "$RELEASE_REF_PATH"; then
    ((CITED++))
fi

if [ "$CITED" -ge 1 ]; then
    echo "  ✓ PASS: $CITED reference(s) cite error-handling-patterns.md"
    ((TESTS_PASSED++))
else
    echo "  ✗ FAIL: No references cite error-handling-patterns.md"
    ((TESTS_FAILED++))
fi

# Test 7: Both skills use aggregate_parallel_results function
echo ""
echo "Test 7: Both skills use aggregate_parallel_results pattern"
AGGREGATE_FOUND=0
if [ -f "$QA_REF_PATH" ] && grep -qi "aggregate.*result\|aggregat" "$QA_REF_PATH"; then
    ((AGGREGATE_FOUND++))
fi
if [ -f "$RELEASE_REF_PATH" ] && grep -qi "aggregate.*result\|aggregat" "$RELEASE_REF_PATH"; then
    ((AGGREGATE_FOUND++))
fi

if [ "$AGGREGATE_FOUND" -eq 2 ]; then
    echo "  ✓ PASS: Both skills use aggregation pattern"
    ((TESTS_PASSED++))
else
    echo "  ✗ FAIL: Only $AGGREGATE_FOUND of 2 skills use aggregation"
    ((TESTS_FAILED++))
fi

# Summary
echo ""
echo "=============================================="
echo "SUMMARY: $TESTS_PASSED passed, $TESTS_FAILED failed"
echo "=============================================="

if [ "$TESTS_FAILED" -gt 0 ]; then
    exit 1
else
    exit 0
fi
