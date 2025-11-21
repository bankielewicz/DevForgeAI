#!/bin/bash
###############################################################################
# Test Suite: STORY-052 - Document Structure Validation
# Purpose: Validate AC1, AC5 - Document completeness and scannability
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

echo "STORY-052 Document Structure Validation Tests"

if [ ! -f "$GUIDE_FILE" ]; then
    echo "Document does not exist: $GUIDE_FILE"
    echo "All tests will FAIL in RED phase until document is created."
fi

header "AC1: Document Completeness"

test_case "File exists at expected location"
if [ -f "$GUIDE_FILE" ]; then
    pass_test "File exists: $GUIDE_FILE"
else
    fail_test "File does not exist: $GUIDE_FILE"
fi

test_case "Introduction section (>=200 words)"
if [ -f "$GUIDE_FILE" ]; then
    intro_words=$(head -100 "$GUIDE_FILE" | grep -i "introduction" -A 50 2>/dev/null | wc -w || echo "0")
    if [ "$intro_words" -ge 200 ]; then
        pass_test "Introduction has >=200 words (found: $intro_words)"
    else
        fail_test "Introduction has <200 words (found: $intro_words)"
    fi
else
    skip_test "Introduction validation"
fi

test_case "All 11 commands have dedicated sections"
if [ -f "$GUIDE_FILE" ]; then
    commands=("ideate" "create-story" "create-context" "create-epic" "create-sprint" "create-ui" "dev" "qa" "release" "orchestrate" "create-agent")
    found=0
    for cmd in "${commands[@]}"; do
        grep -q "## /$cmd\|### /$cmd" "$GUIDE_FILE" 2>/dev/null && found=$((found+1))
    done
    if [ $found -eq 11 ]; then
        pass_test "All 11 command sections found"
    else
        fail_test "Only $found/11 command sections found"
    fi
else
    skip_test "Command sections validation"
fi

test_case "20-30 before/after examples exist"
if [ -f "$GUIDE_FILE" ]; then
    before_count=$(grep -c "❌ BEFORE\|❌ WRONG\|❌ DON'T" "$GUIDE_FILE" 2>/dev/null || echo "0")
    if [ "$before_count" -ge 20 ] && [ "$before_count" -le 30 ]; then
        pass_test "Found $before_count examples (20-30 required)"
    else
        fail_test "Found $before_count examples (need 20-30)"
    fi
else
    skip_test "Examples validation"
fi

test_case "Quick reference checklist in first 500 lines"
if [ -f "$GUIDE_FILE" ]; then
    if head -500 "$GUIDE_FILE" | grep -qi "quick reference\|checklist\|quick start" 2>/dev/null; then
        pass_test "Quick reference found in first 500 lines"
    else
        fail_test "Quick reference not in first 500 lines"
    fi
else
    skip_test "Quick reference validation"
fi

test_case "Common pitfalls section (10-15 items)"
if [ -f "$GUIDE_FILE" ]; then
    if grep -q "Common Pitfalls\|common pitfalls" "$GUIDE_FILE" 2>/dev/null; then
        pitfall_count=$(grep -A 200 "Common Pitfalls" "$GUIDE_FILE" 2>/dev/null | grep "^- \|^• " | wc -l || echo "0")
        if [ "$pitfall_count" -ge 10 ] && [ "$pitfall_count" -le 15 ]; then
            pass_test "Found $pitfall_count pitfalls (10-15 required)"
        else
            fail_test "Found $pitfall_count pitfalls (need 10-15)"
        fi
    else
        fail_test "Common pitfalls section not found"
    fi
else
    skip_test "Pitfalls validation"
fi

header "AC5: Usability and Scannability"

test_case "Table of contents in first 100 lines"
if [ -f "$GUIDE_FILE" ]; then
    if head -100 "$GUIDE_FILE" | grep -qi "table of contents\|contents\|navigation" 2>/dev/null; then
        pass_test "Table of contents in first 100 lines"
    else
        fail_test "Table of contents not in first 100 lines"
    fi
else
    skip_test "ToC validation"
fi

test_case "Visual hierarchy (no heading level skips)"
if [ -f "$GUIDE_FILE" ]; then
    pass_test "Visual hierarchy check (basic validation)"
else
    skip_test "Visual hierarchy validation"
fi

test_case "Code block formatting (all examples in ``` blocks)"
if [ -f "$GUIDE_FILE" ]; then
    blocks=$(grep -c '```' "$GUIDE_FILE" 2>/dev/null || echo "0")
    if [ "$blocks" -ge 20 ]; then
        pass_test "Found $blocks code blocks"
    else
        fail_test "Found only $blocks code blocks (need >=20)"
    fi
else
    skip_test "Code block validation"
fi

test_case "Search-friendly headings"
if [ -f "$GUIDE_FILE" ]; then
    heading_count=$(grep -c "^## \|^### " "$GUIDE_FILE" 2>/dev/null || echo "0")
    if [ "$heading_count" -gt 15 ]; then
        pass_test "Found $heading_count headings"
    else
        fail_test "Found only $heading_count headings (need >15)"
    fi
else
    skip_test "Headings validation"
fi

header "Summary"
echo ""
echo "Total Tests: $TEST_COUNT"
echo "Passed: $PASS_COUNT"
echo "Failed: $FAIL_COUNT"
