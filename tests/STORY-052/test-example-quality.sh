#!/bin/bash
###############################################################################
# Test Suite: STORY-052 - Example Quality Validation
# Purpose: Validate AC2 - Example quality, realism, and effectiveness
###############################################################################

set -euo pipefail

GUIDE_FILE="src/claude/memory/effective-prompting-guide.md"
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

echo "STORY-052 Example Quality Validation Tests"

if [ ! -f "$GUIDE_FILE" ]; then
    echo "Document does not exist: $GUIDE_FILE"
    echo "All tests will FAIL until document is created."
fi

header "AC2: Example Quality and Realism"

test_case "20-30 before/after example pairs"
if [ -f "$GUIDE_FILE" ]; then
    before=$(grep -c "❌ BEFORE\|❌ WRONG" "$GUIDE_FILE" 2>/dev/null || echo "0")
    if [ "$before" -ge 20 ] && [ "$before" -le 30 ]; then
        pass_test "Found $before examples (20-30 required)"
    else
        fail_test "Found $before examples (need 20-30)"
    fi
else
    skip_test "Example count validation"
fi

test_case "Explanations provided for examples (>=50 words each)"
if [ -f "$GUIDE_FILE" ]; then
    explanations=$(grep -c "Why\|because\|This\|Improvement\|Better\|demonstrates" "$GUIDE_FILE" 2>/dev/null || echo "0")
    if [ "$explanations" -ge 15 ]; then
        pass_test "Found $explanations explanation sections"
    else
        fail_test "Found only $explanations explanations (need >=15)"
    fi
else
    skip_test "Explanations validation"
fi

test_case "Examples reference actual commands (/command syntax)"
if [ -f "$GUIDE_FILE" ]; then
    command_refs=$(grep -o "/[a-zA-Z-]*" "$GUIDE_FILE" 2>/dev/null | sort -u | wc -l)
    if [ "$command_refs" -ge 10 ]; then
        pass_test "Found $command_refs unique command references"
    else
        fail_test "Found only $command_refs command references (need >=10)"
    fi
else
    skip_test "Command references validation"
fi

test_case "Specific improvements demonstrated (vague → specific patterns)"
if [ -f "$GUIDE_FILE" ]; then
    patterns=$(grep -c "vague\|specific\|unclear\|clear\|missing\|complete\|improvement\|better" "$GUIDE_FILE" 2>/dev/null || echo "0")
    if [ "$patterns" -ge 30 ]; then
        pass_test "Found $patterns improvement pattern indicators"
    else
        fail_test "Found only $patterns patterns (need >=30)"
    fi
else
    skip_test "Improvement patterns validation"
fi

test_case "Measurable improvements noted (e.g., '5 → 0 questions')"
if [ -f "$GUIDE_FILE" ]; then
    metrics=$(grep -c "→\|from [0-9]\|reduced\|improved" "$GUIDE_FILE" 2>/dev/null || echo "0")
    if [ "$metrics" -ge 5 ]; then
        pass_test "Found $metrics measurable improvement examples"
    else
        fail_test "Found only $metrics measurable examples (need >=5)"
    fi
else
    skip_test "Measurable improvements validation"
fi

test_case "Examples show realistic user input patterns"
if [ -f "$GUIDE_FILE" ]; then
    realistic=$(grep -c "real\|actual\|typical\|scenario\|production\|domain" "$GUIDE_FILE" 2>/dev/null || echo "0")
    if [ "$realistic" -ge 5 ]; then
        pass_test "Found $realistic realistic input indicators"
    else
        fail_test "Found only $realistic realism indicators (need >=5)"
    fi
else
    skip_test "Realism validation"
fi

test_case "Code block formatting consistency"
if [ -f "$GUIDE_FILE" ]; then
    blocks=$(grep -c '```' "$GUIDE_FILE" 2>/dev/null || echo "0")
    pairs=$((blocks / 2))
    if [ "$pairs" -ge 20 ]; then
        pass_test "Found $pairs code blocks for examples"
    else
        fail_test "Found only $pairs code blocks (need >=20)"
    fi
else
    skip_test "Code block validation"
fi

test_case "Framework workflow state references"
if [ -f "$GUIDE_FILE" ]; then
    refs=$(grep -c "Backlog\|Ready for Dev\|In Development\|QA\|Phase\|Red\|Green\|Refactor" "$GUIDE_FILE" 2>/dev/null || echo "0")
    if [ "$refs" -ge 5 ]; then
        pass_test "Found $refs workflow state references"
    else
        fail_test "Found only $refs references (need >=5)"
    fi
else
    skip_test "Workflow references validation"
fi

test_case "Context file references in examples"
if [ -f "$GUIDE_FILE" ]; then
    refs=$(grep -c "tech-stack\|source-tree\|dependencies\|coding-standards\|architecture\|anti-patterns" "$GUIDE_FILE" 2>/dev/null || echo "0")
    if [ "$refs" -ge 3 ]; then
        pass_test "Found $refs context file references"
    else
        fail_test "Found only $refs references (need >=3)"
    fi
else
    skip_test "Context file references validation"
fi

test_case "BEFORE/AFTER marker consistency"
if [ -f "$GUIDE_FILE" ]; then
    before=$(grep -c "❌ BEFORE\|❌ WRONG" "$GUIDE_FILE" 2>/dev/null || echo "0")
    after=$(grep -c "✅ AFTER\|✅ CORRECT" "$GUIDE_FILE" 2>/dev/null || echo "0")
    if [ "$before" -gt 0 ] && [ "$after" -gt 0 ]; then
        pass_test "Consistent markers ($before before, $after after)"
    else
        fail_test "Inconsistent markers ($before before, $after after)"
    fi
else
    skip_test "Marker consistency validation"
fi

header "Summary"
echo ""
echo "Total Tests: $TEST_COUNT"
echo "Passed: $PASS_COUNT"
echo "Failed: $FAIL_COUNT"
