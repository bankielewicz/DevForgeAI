#!/bin/bash
# STORY-130 AC#2: Command Delegates Validation to Skill Phase 6.4
# Tests that command invokes skill without pre/post validation
# Expected: No validation logic in command, skill handles all validation

# Note: No set -e because we want to run all tests even if some fail

IDEATE_FILE=".claude/commands/ideate.md"
PASS_COUNT=0
FAIL_COUNT=0
TOTAL_TESTS=6

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  STORY-130 AC#2: Command Delegates to Skill"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Test 1: Skill invocation present
if grep -q 'Skill(command="devforgeai-ideation")' "$IDEATE_FILE" 2>/dev/null; then
    echo "✓ PASS: Skill invocation present"
    ((PASS_COUNT++))
else
    echo "✗ FAIL: Skill invocation missing"
    ((FAIL_COUNT++))
fi

# Test 2: No pre-validation (checking artifact existence BEFORE skill call)
# Look for Glob patterns checking artifacts before the skill invocation line
SKILL_LINE=$(grep -n 'Skill(command="devforgeai-ideation")' "$IDEATE_FILE" | head -1 | cut -d: -f1)
if [ -n "$SKILL_LINE" ]; then
    # Check if any Glob for EPIC files appears before skill invocation
    PRE_GLOB=$(head -n "$SKILL_LINE" "$IDEATE_FILE" | grep -c 'Glob.*EPIC-.*epic.md' || true)
    if [ "$PRE_GLOB" -eq 0 ]; then
        echo "✓ PASS: No pre-validation artifact checks before skill"
        ((PASS_COUNT++))
    else
        echo "✗ FAIL: Pre-validation artifact checks found before skill invocation"
        ((FAIL_COUNT++))
    fi
else
    echo "✗ FAIL: Could not locate skill invocation line"
    ((FAIL_COUNT++))
fi

# Test 3: No post-validation (artifact checking section removed)
# After skill call, there should be no verification section
if grep -q "Check Skill Completion Status" "$IDEATE_FILE" 2>/dev/null; then
    echo "✗ FAIL: Post-validation section still exists"
    ((FAIL_COUNT++))
else
    echo "✓ PASS: No post-validation section"
    ((PASS_COUNT++))
fi

# Test 4: No YAML syntax validation CODE in command (documentation mentioning YAML is OK)
# Look for actual validation code patterns, not documentation
if grep -q "validate_frontmatter\|parse_yaml_frontmatter.*epic\|YAML.*valid.*check" "$IDEATE_FILE" 2>/dev/null; then
    echo "✗ FAIL: YAML validation logic (code) found in command"
    ((FAIL_COUNT++))
else
    echo "✓ PASS: No YAML validation code in command"
    ((PASS_COUNT++))
fi

# Test 5: No ID format validation CODE in command
# Look for validation code patterns like "id field matches filename", not documentation
if grep -q "id field matches filename\|id_mismatch\|correct_id = " "$IDEATE_FILE" 2>/dev/null; then
    echo "✗ FAIL: ID format validation code found in command"
    ((FAIL_COUNT++))
else
    echo "✓ PASS: No ID format validation code in command"
    ((PASS_COUNT++))
fi

# Test 6: Trust statement or delegation note present
if grep -qi "trust.*skill\|delegate.*skill\|skill.*handles\|Phase 6.4" "$IDEATE_FILE" 2>/dev/null; then
    echo "✓ PASS: Trust/delegation statement present"
    ((PASS_COUNT++))
else
    echo "✗ FAIL: No trust/delegation statement found"
    ((FAIL_COUNT++))
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  Results: $PASS_COUNT/$TOTAL_TESTS passed"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

if [ $FAIL_COUNT -gt 0 ]; then
    echo "  Status: FAILED ($FAIL_COUNT delegation issues)"
    exit 1
else
    echo "  Status: PASSED (command properly delegates to skill)"
    exit 0
fi
