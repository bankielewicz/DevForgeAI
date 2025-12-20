#!/bin/bash
# STORY-113 AC#1: Parallel QA Validation Subagents
# Tests that QA skill invokes 3 validators in parallel (single message with 3 Task calls)

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../../.." && pwd)"

# Test configuration
QA_SKILL_PATH="$PROJECT_ROOT/.claude/skills/devforgeai-qa/SKILL.md"
PARALLEL_REF_PATH="$PROJECT_ROOT/.claude/skills/devforgeai-qa/references/parallel-validation.md"

echo "=============================================="
echo "STORY-113 AC#1: Parallel QA Validation Subagents"
echo "=============================================="

TESTS_PASSED=0
TESTS_FAILED=0

# Test 1: QA skill has parallel validation phase
echo ""
echo "Test 1: QA skill has parallel validation phase"
if grep -q "Parallel Validation" "$QA_SKILL_PATH" 2>/dev/null; then
    echo "  ✓ PASS: Parallel Validation phase exists"
    ((TESTS_PASSED++))
else
    echo "  ✗ FAIL: Parallel Validation phase not found in QA skill"
    ((TESTS_FAILED++))
fi

# Test 2: QA skill references parallel-validation.md
echo ""
echo "Test 2: QA skill references parallel-validation.md"
if grep -q "parallel-validation.md" "$QA_SKILL_PATH" 2>/dev/null; then
    echo "  ✓ PASS: parallel-validation.md reference exists"
    ((TESTS_PASSED++))
else
    echo "  ✗ FAIL: parallel-validation.md reference not found"
    ((TESTS_FAILED++))
fi

# Test 3: parallel-validation.md reference file exists
echo ""
echo "Test 3: parallel-validation.md reference file exists"
if [ -f "$PARALLEL_REF_PATH" ]; then
    echo "  ✓ PASS: parallel-validation.md exists"
    ((TESTS_PASSED++))
else
    echo "  ✗ FAIL: parallel-validation.md not found at $PARALLEL_REF_PATH"
    ((TESTS_FAILED++))
fi

# Test 4: Parallel reference mentions all 3 validators
echo ""
echo "Test 4: Parallel reference mentions all 3 validators"
if [ -f "$PARALLEL_REF_PATH" ]; then
    VALIDATORS_FOUND=0
    if grep -q "test-automator" "$PARALLEL_REF_PATH"; then ((VALIDATORS_FOUND++)); fi
    if grep -q "code-reviewer" "$PARALLEL_REF_PATH"; then ((VALIDATORS_FOUND++)); fi
    if grep -q "security-auditor" "$PARALLEL_REF_PATH"; then ((VALIDATORS_FOUND++)); fi

    if [ "$VALIDATORS_FOUND" -eq 3 ]; then
        echo "  ✓ PASS: All 3 validators mentioned (test-automator, code-reviewer, security-auditor)"
        ((TESTS_PASSED++))
    else
        echo "  ✗ FAIL: Only $VALIDATORS_FOUND of 3 validators found"
        ((TESTS_FAILED++))
    fi
else
    echo "  ✗ FAIL: Cannot check validators - reference file missing"
    ((TESTS_FAILED++))
fi

# Test 5: Parallel reference defines single-message pattern
echo ""
echo "Test 5: Parallel reference defines single-message pattern"
if [ -f "$PARALLEL_REF_PATH" ]; then
    if grep -qi "single message\|ONE message\|parallel.*task" "$PARALLEL_REF_PATH"; then
        echo "  ✓ PASS: Single-message parallel pattern documented"
        ((TESTS_PASSED++))
    else
        echo "  ✗ FAIL: Single-message pattern not documented"
        ((TESTS_FAILED++))
    fi
else
    echo "  ✗ FAIL: Cannot check pattern - reference file missing"
    ((TESTS_FAILED++))
fi

# Test 6: QA skill has 66% success threshold (2 of 3 validators)
echo ""
echo "Test 6: QA skill has appropriate success threshold"
if grep -q "0\.66\|66%\|2 of 3" "$QA_SKILL_PATH" 2>/dev/null || \
   ([ -f "$PARALLEL_REF_PATH" ] && grep -q "0\.66\|66%\|2 of 3" "$PARALLEL_REF_PATH"); then
    echo "  ✓ PASS: 66% success threshold configured"
    ((TESTS_PASSED++))
else
    echo "  ✗ FAIL: 66% success threshold not found"
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
