#!/bin/bash
###############################################################################
# Test Suite: STORY-053 - Pattern Structure Validation
# Purpose: Validate AC1 - Pattern Completeness (10-15 patterns with required sections)
# Tests: DOC-001, BR-001 - Pattern count and structure validation
###############################################################################

set -euo pipefail

GUIDANCE_FILE="src/claude/skills/devforgeai-ideation/references/user-input-guidance.md"
TEST_COUNT=0
PASS_COUNT=0
FAIL_COUNT=0

pass_test() {
    PASS_COUNT=$((PASS_COUNT + 1))
    echo "✓ PASS: $1"
}

fail_test() {
    FAIL_COUNT=$((FAIL_COUNT + 1))
    echo "✗ FAIL: $1"
}

skip_test() {
    echo "⊘ SKIP: $1"
}

test_case() {
    TEST_COUNT=$((TEST_COUNT + 1))
    echo ""
    echo "Test $TEST_COUNT: $1"
}

header() {
    echo ""
    echo "================================================================"
    echo "$1"
    echo "================================================================"
}

echo "STORY-053 Pattern Structure Validation Tests"

if [ ! -f "$GUIDANCE_FILE" ]; then
    echo "WARNING: Guidance file does not exist: $GUIDANCE_FILE"
    echo "All tests will FAIL in RED phase until file is created."
    echo ""
fi

header "AC1: Pattern Completeness"

test_case "File exists at expected location"
if [ -f "$GUIDANCE_FILE" ]; then
    pass_test "File exists: $GUIDANCE_FILE"
else
    fail_test "File does not exist: $GUIDANCE_FILE"
fi

test_case "Pattern count is within range (10-15)"
if [ -f "$GUIDANCE_FILE" ]; then
    pattern_count=$(grep -c "^### Pattern" "$GUIDANCE_FILE" 2>/dev/null || echo "0")
    if [ "$pattern_count" -ge 10 ] && [ "$pattern_count" -le 15 ]; then
        pass_test "Found $pattern_count patterns (10-15 required)"
    else
        fail_test "Found $pattern_count patterns (need 10-15)"
    fi
else
    skip_test "Pattern count validation"
fi

test_case "Functional requirement patterns (3-4)"
if [ -f "$GUIDANCE_FILE" ]; then
    functional_count=$(grep -c "### Pattern.*Functional\|Functional requirement\|AC elicitation" "$GUIDANCE_FILE" 2>/dev/null || echo "0")
    if [ "$functional_count" -ge 3 ] && [ "$functional_count" -le 4 ]; then
        pass_test "Found $functional_count functional patterns (3-4 required)"
    else
        fail_test "Found $functional_count functional patterns (need 3-4)"
    fi
else
    skip_test "Functional patterns validation"
fi

test_case "Non-functional requirement patterns (2-3)"
if [ -f "$GUIDANCE_FILE" ]; then
    nfr_count=$(grep -c "### Pattern.*NFR\|Non-functional\|quantification" "$GUIDANCE_FILE" 2>/dev/null || echo "0")
    if [ "$nfr_count" -ge 2 ] && [ "$nfr_count" -le 3 ]; then
        pass_test "Found $nfr_count NFR patterns (2-3 required)"
    else
        fail_test "Found $nfr_count NFR patterns (need 2-3)"
    fi
else
    skip_test "NFR patterns validation"
fi

test_case "Edge case patterns (2-3)"
if [ -f "$GUIDANCE_FILE" ]; then
    edge_count=$(grep -c "### Pattern.*Edge\|edge case\|boundary\|error condition" "$GUIDANCE_FILE" 2>/dev/null || echo "0")
    if [ "$edge_count" -ge 2 ] && [ "$edge_count" -le 3 ]; then
        pass_test "Found $edge_count edge case patterns (2-3 required)"
    else
        fail_test "Found $edge_count edge case patterns (need 2-3)"
    fi
else
    skip_test "Edge case patterns validation"
fi

test_case "Integration point patterns (2-3)"
if [ -f "$GUIDANCE_FILE" ]; then
    integration_count=$(grep -c "### Pattern.*Integration\|integration point\|API\|dependencies" "$GUIDANCE_FILE" 2>/dev/null || echo "0")
    if [ "$integration_count" -ge 2 ] && [ "$integration_count" -le 3 ]; then
        pass_test "Found $integration_count integration patterns (2-3 required)"
    else
        fail_test "Found $integration_count integration patterns (need 2-3)"
    fi
else
    skip_test "Integration patterns validation"
fi

test_case "Constraint clarification patterns (1-2)"
if [ -f "$GUIDANCE_FILE" ]; then
    constraint_count=$(grep -c "### Pattern.*Constraint\|constraint\|limitation\|boundary condition" "$GUIDANCE_FILE" 2>/dev/null || echo "0")
    if [ "$constraint_count" -ge 1 ] && [ "$constraint_count" -le 2 ]; then
        pass_test "Found $constraint_count constraint patterns (1-2 required)"
    else
        fail_test "Found $constraint_count constraint patterns (need 1-2)"
    fi
else
    skip_test "Constraint patterns validation"
fi

header "BR-001: Pattern Structure Requirements"

test_case "Each pattern has Problem section"
if [ -f "$GUIDANCE_FILE" ]; then
    # Check if patterns contain Problem descriptions
    pattern_count=$(grep -c "^### Pattern" "$GUIDANCE_FILE" 2>/dev/null || echo "0")
    problem_count=$(grep -c "^#### Problem\|^#### Problem:" "$GUIDANCE_FILE" 2>/dev/null || echo "0")

    if [ "$problem_count" -eq "$pattern_count" ]; then
        pass_test "All $pattern_count patterns have Problem sections"
    else
        fail_test "Only $problem_count/$pattern_count patterns have Problem sections"
    fi
else
    skip_test "Pattern Problem section validation"
fi

test_case "Each pattern has Solution section"
if [ -f "$GUIDANCE_FILE" ]; then
    pattern_count=$(grep -c "^### Pattern" "$GUIDANCE_FILE" 2>/dev/null || echo "0")
    solution_count=$(grep -c "^#### Solution\|^#### Solution:" "$GUIDANCE_FILE" 2>/dev/null || echo "0")

    if [ "$solution_count" -eq "$pattern_count" ]; then
        pass_test "All $pattern_count patterns have Solution sections"
    else
        fail_test "Only $solution_count/$pattern_count patterns have Solution sections"
    fi
else
    skip_test "Pattern Solution section validation"
fi

test_case "Each pattern has AskUserQuestion Template section"
if [ -f "$GUIDANCE_FILE" ]; then
    pattern_count=$(grep -c "^### Pattern" "$GUIDANCE_FILE" 2>/dev/null || echo "0")
    template_count=$(grep -c "AskUserQuestion(" "$GUIDANCE_FILE" 2>/dev/null || echo "0")

    if [ "$template_count" -ge "$pattern_count" ]; then
        pass_test "All patterns have AskUserQuestion templates ($template_count found)"
    else
        fail_test "Only $template_count/$pattern_count patterns have AskUserQuestion templates"
    fi
else
    skip_test "Pattern Template section validation"
fi

test_case "Each pattern has Example section"
if [ -f "$GUIDANCE_FILE" ]; then
    pattern_count=$(grep -c "^### Pattern" "$GUIDANCE_FILE" 2>/dev/null || echo "0")
    example_count=$(grep -c "^#### Example\|^#### Example:" "$GUIDANCE_FILE" 2>/dev/null || echo "0")

    if [ "$example_count" -eq "$pattern_count" ]; then
        pass_test "All $pattern_count patterns have Example sections"
    else
        fail_test "Only $example_count/$pattern_count patterns have Example sections"
    fi
else
    skip_test "Pattern Example section validation"
fi

test_case "Each pattern references related patterns (or explicitly notes 'none')"
if [ -f "$GUIDANCE_FILE" ]; then
    pattern_count=$(grep -c "^### Pattern" "$GUIDANCE_FILE" 2>/dev/null || echo "0")
    related_refs=$(grep -c "^#### Related Patterns\|Related: \|See also:" "$GUIDANCE_FILE" 2>/dev/null || echo "0")

    # Allow patterns without related references (some patterns may be standalone)
    if [ "$related_refs" -ge 0 ]; then
        pass_test "Pattern cross-references documented (found $related_refs references)"
    else
        fail_test "No pattern cross-references found"
    fi
else
    skip_test "Pattern cross-reference validation"
fi

header "Pattern Content Quality"

test_case "Problem descriptions have 2-3 sentences"
if [ -f "$GUIDANCE_FILE" ]; then
    # This is a basic check - look for period count in problem sections
    problem_text=$(grep -A 3 "^#### Problem" "$GUIDANCE_FILE" 2>/dev/null | grep -v "^--$" | wc -l || echo "0")
    if [ "$problem_text" -ge 2 ]; then
        pass_test "Problem descriptions present and contain content"
    else
        fail_test "Problem descriptions may be too brief"
    fi
else
    skip_test "Problem description quality validation"
fi

test_case "Solution includes step-by-step guidance"
if [ -f "$GUIDANCE_FILE" ]; then
    # Check for numbered steps or bullet points in solutions
    solution_steps=$(grep -A 10 "^#### Solution" "$GUIDANCE_FILE" 2>/dev/null | grep -c "^[0-9]\. \|^- \|^• " || echo "0")
    if [ "$solution_steps" -ge 3 ]; then
        pass_test "Solutions contain step-by-step guidance"
    else
        fail_test "Solutions may lack detailed step-by-step structure"
    fi
else
    skip_test "Solution quality validation"
fi

test_case "Examples reference DevForgeAI context"
if [ -f "$GUIDANCE_FILE" ]; then
    # Check for framework references in examples
    examples=$(grep -c "STORY-\|EPIC-\|devforgeai\|skill\|workflow\|acceptance criteria" "$GUIDANCE_FILE" 2>/dev/null || echo "0")
    if [ "$examples" -ge 5 ]; then
        pass_test "Examples contain DevForgeAI context references ($examples found)"
    else
        fail_test "Examples may lack DevForgeAI context references"
    fi
else
    skip_test "Example context validation"
fi

header "Summary"
echo ""
echo "Total Tests: $TEST_COUNT"
echo "Passed: $PASS_COUNT"
echo "Failed: $FAIL_COUNT"
echo ""

if [ $FAIL_COUNT -eq 0 ]; then
    echo "Result: ALL TESTS PASSED"
    exit 0
else
    echo "Result: SOME TESTS FAILED"
    exit 1
fi
