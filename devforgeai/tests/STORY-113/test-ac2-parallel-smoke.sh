#!/bin/bash
# STORY-113 AC#2: Parallel Release Smoke Tests
# Tests that Release skill runs 3-5 smoke tests concurrently


SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../../.." && pwd)"

# Test configuration
RELEASE_SKILL_PATH="$PROJECT_ROOT/.claude/skills/devforgeai-release/SKILL.md"
PARALLEL_REF_PATH="$PROJECT_ROOT/.claude/skills/devforgeai-release/references/parallel-smoke-tests.md"

echo "=============================================="
echo "STORY-113 AC#2: Parallel Release Smoke Tests"
echo "=============================================="

TESTS_PASSED=0
TESTS_FAILED=0

# Test 1: Release skill has parallel validation phase
echo ""
echo "Test 1: Release skill has parallel validation phase"
if grep -q "Parallel.*Validation\|Parallel.*Smoke" "$RELEASE_SKILL_PATH" 2>/dev/null; then
    echo "  ✓ PASS: Parallel validation/smoke phase exists"
    ((TESTS_PASSED++))
else
    echo "  ✗ FAIL: Parallel validation phase not found in Release skill"
    ((TESTS_FAILED++))
fi

# Test 2: Release skill references parallel-smoke-tests.md
echo ""
echo "Test 2: Release skill references parallel-smoke-tests.md"
if grep -q "parallel-smoke-tests.md" "$RELEASE_SKILL_PATH" 2>/dev/null; then
    echo "  ✓ PASS: parallel-smoke-tests.md reference exists"
    ((TESTS_PASSED++))
else
    echo "  ✗ FAIL: parallel-smoke-tests.md reference not found"
    ((TESTS_FAILED++))
fi

# Test 3: parallel-smoke-tests.md reference file exists
echo ""
echo "Test 3: parallel-smoke-tests.md reference file exists"
if [ -f "$PARALLEL_REF_PATH" ]; then
    echo "  ✓ PASS: parallel-smoke-tests.md exists"
    ((TESTS_PASSED++))
else
    echo "  ✗ FAIL: parallel-smoke-tests.md not found at $PARALLEL_REF_PATH"
    ((TESTS_FAILED++))
fi

# Test 4: Parallel reference mentions concurrent execution
echo ""
echo "Test 4: Parallel reference mentions concurrent execution"
if [ -f "$PARALLEL_REF_PATH" ]; then
    if grep -qi "concurrent\|parallel\|3-5\|batch" "$PARALLEL_REF_PATH"; then
        echo "  ✓ PASS: Concurrent execution pattern documented"
        ((TESTS_PASSED++))
    else
        echo "  ✗ FAIL: Concurrent execution not documented"
        ((TESTS_FAILED++))
    fi
else
    echo "  ✗ FAIL: Cannot check pattern - reference file missing"
    ((TESTS_FAILED++))
fi

# Test 5: Parallel reference defines result aggregation
echo ""
echo "Test 5: Parallel reference defines result aggregation"
if [ -f "$PARALLEL_REF_PATH" ]; then
    if grep -qi "aggregate\|PartialResult\|results" "$PARALLEL_REF_PATH"; then
        echo "  ✓ PASS: Result aggregation documented"
        ((TESTS_PASSED++))
    else
        echo "  ✗ FAIL: Result aggregation not documented"
        ((TESTS_FAILED++))
    fi
else
    echo "  ✗ FAIL: Cannot check aggregation - reference file missing"
    ((TESTS_FAILED++))
fi

# Test 6: Release skill loads parallel config
echo ""
echo "Test 6: Release skill loads parallel configuration"
if grep -q "parallel-orchestration.yaml\|max_concurrent" "$RELEASE_SKILL_PATH" 2>/dev/null || \
   ([ -f "$PARALLEL_REF_PATH" ] && grep -q "parallel-orchestration.yaml\|max_concurrent" "$PARALLEL_REF_PATH"); then
    echo "  ✓ PASS: Parallel configuration loading documented"
    ((TESTS_PASSED++))
else
    echo "  ✗ FAIL: Parallel configuration loading not found"
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
