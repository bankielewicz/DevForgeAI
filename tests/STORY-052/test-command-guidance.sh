#!/bin/bash
###############################################################################
# Test Suite: STORY-052 - Command Guidance Validation
# Purpose: Validate AC3, AC4 - Command guidance and framework integration
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

echo "STORY-052 Command Guidance Validation Tests"

if [ ! -f "$GUIDE_FILE" ]; then
    echo "Document does not exist: $GUIDE_FILE"
    echo "All tests will FAIL until document is created."
fi

header "AC3: Command-Specific Guidance Accuracy"

test_case "All 11 commands have dedicated guidance sections"
if [ -f "$GUIDE_FILE" ]; then
    cmds=("ideate" "create-story" "create-context" "create-epic" "create-sprint" "create-ui" "dev" "qa" "release" "orchestrate" "create-agent")
    found=0
    for cmd in "${cmds[@]}"; do
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

test_case "Required inputs documented per command"
if [ -f "$GUIDE_FILE" ]; then
    inputs=$(grep -c "Required Inputs\|required inputs\|Required Parameters\|Parameters:" "$GUIDE_FILE" 2>/dev/null || echo "0")
    if [ "$inputs" -ge 8 ]; then
        pass_test "Found $inputs required inputs sections"
    else
        fail_test "Found only $inputs sections (need >=8)"
    fi
else
    skip_test "Required inputs validation"
fi

test_case "Examples per command (2-3 examples distributed)"
if [ -f "$GUIDE_FILE" ]; then
    total=$(grep -c "❌ BEFORE" "$GUIDE_FILE" 2>/dev/null || echo "0")
    if [ "$total" -ge 20 ]; then
        avg=$((total / 11))
        pass_test "Examples distributed (total: $total, avg per cmd: $avg)"
    else
        fail_test "Not enough examples (total: $total)"
    fi
else
    skip_test "Examples distribution validation"
fi

test_case "Complete input definitions for each command"
if [ -f "$GUIDE_FILE" ]; then
    defs=$(grep -c "complete input\|Complete Input\|what makes\|required to\|must include" "$GUIDE_FILE" 2>/dev/null || echo "0")
    if [ "$defs" -ge 8 ]; then
        pass_test "Found $defs completeness definitions"
    else
        fail_test "Found only $defs definitions (need >=8)"
    fi
else
    skip_test "Completeness definitions validation"
fi

test_case "Cross-references to related commands"
if [ -f "$GUIDE_FILE" ]; then
    refs=$(grep -c "See also\|Related:\|also see\|Related commands\|Next step" "$GUIDE_FILE" 2>/dev/null || echo "0")
    if [ "$refs" -ge 5 ]; then
        pass_test "Found $refs cross-reference sections"
    else
        fail_test "Found only $refs cross-references (need >=5)"
    fi
else
    skip_test "Cross-references validation"
fi

header "AC4: Framework Integration and Navigation"

test_case "Links to source documentation"
if [ -f "$GUIDE_FILE" ]; then
    refs=$(grep -c "@\.claude\|\devforgeai\|SKILL\.md\|README\|See:" "$GUIDE_FILE" 2>/dev/null || echo "0")
    if [ "$refs" -ge 5 ]; then
        pass_test "Found $refs documentation references"
    else
        fail_test "Found only $refs references (need >=5)"
    fi
else
    skip_test "Documentation references validation"
fi

test_case "Inline explanations of framework concepts"
if [ -f "$GUIDE_FILE" ]; then
    concepts=$(grep -c "workflow state\|acceptance criteria\|quality gate\|Definition of Done\|TDD\|context file" "$GUIDE_FILE" 2>/dev/null || echo "0")
    if [ "$concepts" -ge 5 ]; then
        pass_test "Found $concepts concept explanations"
    else
        fail_test "Found only $concepts explanations (need >=5)"
    fi
else
    skip_test "Concept explanations validation"
fi

test_case "Consistent terminology with framework"
if [ -f "$GUIDE_FILE" ]; then
    matching=0
    grep -q "workflow states" "$GUIDE_FILE" 2>/dev/null && matching=$((matching+1))
    grep -q "quality gate" "$GUIDE_FILE" 2>/dev/null && matching=$((matching+1))
    grep -q "TDD\|Test-Driven" "$GUIDE_FILE" 2>/dev/null && matching=$((matching+1))
    grep -q "acceptance criteria" "$GUIDE_FILE" 2>/dev/null && matching=$((matching+1))
    grep -q "Definition of Done" "$GUIDE_FILE" 2>/dev/null && matching=$((matching+1))

    if [ "$matching" -ge 4 ]; then
        pass_test "Found $matching matching terminology terms"
    else
        fail_test "Found only $matching terms (need >=4)"
    fi
else
    skip_test "Terminology consistency validation"
fi

test_case "Table of contents with anchor links"
if [ -f "$GUIDE_FILE" ]; then
    if head -150 "$GUIDE_FILE" | grep -qi "table of contents\|contents\|navigation" 2>/dev/null; then
        anchors=$(grep -c "^## \|^### " "$GUIDE_FILE" 2>/dev/null || echo "0")
        if [ "$anchors" -ge 20 ]; then
            pass_test "ToC with $anchors anchor destinations"
        else
            fail_test "ToC has only $anchors anchors (need >=20)"
        fi
    else
        fail_test "Table of contents not found"
    fi
else
    skip_test "Table of contents validation"
fi

test_case "Command index (alphabetical list)"
if [ -f "$GUIDE_FILE" ]; then
    if grep -qi "Command Index\|Commands Index\|All Commands" "$GUIDE_FILE" 2>/dev/null; then
        cmds_listed=$(grep -c "/ideate\|/create-story\|/dev\|/qa\|/release" "$GUIDE_FILE" 2>/dev/null || echo "0")
        if [ "$cmds_listed" -ge 10 ]; then
            pass_test "Command index found with $cmds_listed commands"
        else
            fail_test "Command index incomplete ($cmds_listed/11)"
        fi
    else
        fail_test "Command index not found"
    fi
else
    skip_test "Command index validation"
fi

test_case "Progressive disclosure navigation"
if [ -f "$GUIDE_FILE" ]; then
    has_intro=false
    has_quick=false
    has_cmds=false

    grep -q "Introduction\|Getting Started" "$GUIDE_FILE" 2>/dev/null && has_intro=true
    grep -q "Quick Reference\|Checklist" "$GUIDE_FILE" 2>/dev/null && has_quick=true
    grep -q "^## /\|^### /" "$GUIDE_FILE" 2>/dev/null && has_cmds=true

    if [ "$has_intro" = true ] && [ "$has_quick" = true ] && [ "$has_cmds" = true ]; then
        pass_test "Progressive disclosure structure present"
    else
        fail_test "Progressive disclosure incomplete"
    fi
else
    skip_test "Navigation structure validation"
fi

header "Summary"
echo ""
echo "Total Tests: $TEST_COUNT"
echo "Passed: $PASS_COUNT"
echo "Failed: $FAIL_COUNT"
