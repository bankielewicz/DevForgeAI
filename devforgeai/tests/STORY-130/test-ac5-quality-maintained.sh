#!/bin/bash
# STORY-130 AC#5: All Artifacts Still Verified Despite Validation Removal
# Tests that artifact quality is maintained through skill Phase 6.4
# Expected: Skill's self-validation workflow handles all artifact verification

# Note: No set -e because we want to run all tests even if some fail

IDEATE_FILE=".claude/commands/ideate.md"
SKILL_FILE=".claude/skills/devforgeai-ideation/SKILL.md"
VALIDATION_FILE=".claude/skills/devforgeai-ideation/references/self-validation-workflow.md"
PASS_COUNT=0
FAIL_COUNT=0
TOTAL_TESTS=5

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  STORY-130 AC#5: Quality Maintained via Skill Validation"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Test 1: Skill file exists
if [ -f "$SKILL_FILE" ]; then
    echo "✓ PASS: devforgeai-ideation skill file exists"
    ((PASS_COUNT++))
else
    echo "✗ FAIL: devforgeai-ideation skill file not found"
    ((FAIL_COUNT++))
fi

# Test 2: Self-validation workflow reference exists
if [ -f "$VALIDATION_FILE" ]; then
    echo "✓ PASS: Self-validation workflow reference exists"
    ((PASS_COUNT++))
else
    echo "✗ FAIL: Self-validation workflow reference not found"
    ((FAIL_COUNT++))
fi

# Test 3: Skill mentions Phase 6.4 validation
if grep -q "Phase 6.4\|self-validation\|Self-Validation" "$SKILL_FILE" 2>/dev/null; then
    echo "✓ PASS: Skill includes Phase 6.4 validation reference"
    ((PASS_COUNT++))
else
    echo "✗ FAIL: Skill missing Phase 6.4 validation reference"
    ((FAIL_COUNT++))
fi

# Test 4: Validation workflow includes artifact checks
if grep -q "epic.*valid\|requirements.*valid\|YAML.*frontmatter" "$VALIDATION_FILE" 2>/dev/null; then
    echo "✓ PASS: Validation workflow includes artifact quality checks"
    ((PASS_COUNT++))
else
    echo "✗ FAIL: Validation workflow missing artifact quality checks"
    ((FAIL_COUNT++))
fi

# Test 5: Command references skill's validation (Phase 6.4 or self-validation)
if grep -qi "Phase 6.4\|self-validation\|skill.*valid" "$IDEATE_FILE" 2>/dev/null; then
    echo "✓ PASS: Command references skill's validation capability"
    ((PASS_COUNT++))
else
    echo "✗ FAIL: Command does not reference skill's validation"
    ((FAIL_COUNT++))
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  Results: $PASS_COUNT/$TOTAL_TESTS passed"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

if [ $FAIL_COUNT -gt 0 ]; then
    echo "  Status: FAILED ($FAIL_COUNT quality maintenance issues)"
    exit 1
else
    echo "  Status: PASSED (artifact quality maintained via skill)"
    exit 0
fi
