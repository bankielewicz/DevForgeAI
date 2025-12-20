#!/bin/bash
# STORY-113 AC#3: Concurrent Deployment Validation
# Tests that health checks and smoke tests run together (not sequentially)


SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../../.." && pwd)"

# Test configuration
RELEASE_SKILL_PATH="$PROJECT_ROOT/.claude/skills/devforgeai-release/SKILL.md"
PARALLEL_REF_PATH="$PROJECT_ROOT/.claude/skills/devforgeai-release/references/parallel-smoke-tests.md"

echo "=============================================="
echo "STORY-113 AC#3: Concurrent Deployment Validation"
echo "=============================================="

TESTS_PASSED=0
TESTS_FAILED=0

# Test 1: Release skill mentions health checks
echo ""
echo "Test 1: Release skill mentions health checks"
if grep -qi "health.*check\|health_endpoint\|HEALTH_ENDPOINT" "$RELEASE_SKILL_PATH" 2>/dev/null; then
    echo "  ✓ PASS: Health checks mentioned in Release skill"
    ((TESTS_PASSED++))
else
    echo "  ✗ FAIL: Health checks not found in Release skill"
    ((TESTS_FAILED++))
fi

# Test 2: Health checks and smoke tests documented together
echo ""
echo "Test 2: Health checks and smoke tests in same context"
if [ -f "$PARALLEL_REF_PATH" ]; then
    HEALTH_FOUND=$(grep -ci "health" "$PARALLEL_REF_PATH" || echo "0")
    SMOKE_FOUND=$(grep -ci "smoke" "$PARALLEL_REF_PATH" || echo "0")

    if [ "$HEALTH_FOUND" -gt 0 ] && [ "$SMOKE_FOUND" -gt 0 ]; then
        echo "  ✓ PASS: Both health checks ($HEALTH_FOUND refs) and smoke tests ($SMOKE_FOUND refs) documented"
        ((TESTS_PASSED++))
    else
        echo "  ✗ FAIL: Health ($HEALTH_FOUND) or smoke ($SMOKE_FOUND) not documented together"
        ((TESTS_FAILED++))
    fi
else
    echo "  ✗ FAIL: Cannot check - reference file missing"
    ((TESTS_FAILED++))
fi

# Test 3: Concurrent execution pattern for both
echo ""
echo "Test 3: Concurrent execution pattern for both types"
if [ -f "$PARALLEL_REF_PATH" ]; then
    if grep -qi "same.*batch\|concurrent.*health\|parallel.*health\|SINGLE.*message" "$PARALLEL_REF_PATH"; then
        echo "  ✓ PASS: Concurrent execution pattern documented"
        ((TESTS_PASSED++))
    else
        echo "  ✗ FAIL: Concurrent execution not explicitly documented"
        ((TESTS_FAILED++))
    fi
else
    echo "  ✗ FAIL: Cannot check pattern - reference file missing"
    ((TESTS_FAILED++))
fi

# Test 4: Release skill Phase 4 updated for parallel
echo ""
echo "Test 4: Phase 4 updated for parallel execution"
if grep -q "Phase 4.*Parallel\|Parallel.*Post-Deployment" "$RELEASE_SKILL_PATH" 2>/dev/null; then
    echo "  ✓ PASS: Phase 4 updated for parallel execution"
    ((TESTS_PASSED++))
else
    echo "  ✗ FAIL: Phase 4 not updated for parallel execution"
    ((TESTS_FAILED++))
fi

# Test 5: Aggregation handles mixed results (health + smoke)
echo ""
echo "Test 5: Aggregation handles mixed result types"
if [ -f "$PARALLEL_REF_PATH" ]; then
    if grep -qi "aggregate\|mixed\|combined\|merge" "$PARALLEL_REF_PATH"; then
        echo "  ✓ PASS: Mixed result aggregation documented"
        ((TESTS_PASSED++))
    else
        echo "  ✗ FAIL: Mixed result aggregation not documented"
        ((TESTS_FAILED++))
    fi
else
    echo "  ✗ FAIL: Cannot check aggregation - reference file missing"
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
