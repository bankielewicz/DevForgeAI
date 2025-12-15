#!/bin/bash
###############################################################################
# Test Suite: STORY-053 - Framework Alignment Validation
# Purpose: Validate AC5 - Framework Alignment (100% terminology match)
# Tests: DOC-005, BR-004 - Terminology validation, reference file checks
###############################################################################

set -euo pipefail

GUIDANCE_FILE="src/claude/skills/devforgeai-ideation/references/user-input-guidance.md"
CLAUDE_MD="CLAUDE.md"
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

echo "STORY-053 Framework Alignment Validation Tests"

if [ ! -f "$GUIDANCE_FILE" ]; then
    echo "WARNING: Guidance file does not exist: $GUIDANCE_FILE"
    echo "All tests will FAIL in RED phase until file is created."
    echo ""
fi

header "AC5: Framework Alignment - Context Files"

test_case "Guidance references context files (tech-stack, source-tree, dependencies, etc.)"
if [ -f "$GUIDANCE_FILE" ]; then
    context_refs=$(grep -c "tech-stack\|source-tree\|dependencies\|coding-standards\|architecture-constraints\|anti-patterns" "$GUIDANCE_FILE" 2>/dev/null || echo "0")
    if [ "$context_refs" -ge 6 ]; then
        pass_test "Found $context_refs context file references (≥6 required)"
    else
        fail_test "Found only $context_refs context file references (need ≥6)"
    fi
else
    skip_test "Context file references validation"
fi

test_case "Guidance mentions all 6 context files by name"
if [ -f "$GUIDANCE_FILE" ]; then
    tech_stack=$(grep -c "tech-stack" "$GUIDANCE_FILE" 2>/dev/null || echo "0")
    source_tree=$(grep -c "source-tree" "$GUIDANCE_FILE" 2>/dev/null || echo "0")
    dependencies=$(grep -c "dependencies" "$GUIDANCE_FILE" 2>/dev/null || echo "0")
    coding=$(grep -c "coding-standards" "$GUIDANCE_FILE" 2>/dev/null || echo "0")
    constraints=$(grep -c "architecture-constraints" "$GUIDANCE_FILE" 2>/dev/null || echo "0")
    antipatterns=$(grep -c "anti-patterns" "$GUIDANCE_FILE" 2>/dev/null || echo "0")

    found_count=0
    [ "$tech_stack" -gt 0 ] && found_count=$((found_count + 1))
    [ "$source_tree" -gt 0 ] && found_count=$((found_count + 1))
    [ "$dependencies" -gt 0 ] && found_count=$((found_count + 1))
    [ "$coding" -gt 0 ] && found_count=$((found_count + 1))
    [ "$constraints" -gt 0 ] && found_count=$((found_count + 1))
    [ "$antipatterns" -gt 0 ] && found_count=$((found_count + 1))

    if [ "$found_count" -eq 6 ]; then
        pass_test "All 6 context files referenced in guidance"
    else
        fail_test "Only $found_count/6 context files referenced"
    fi
else
    skip_test "Individual context file validation"
fi

header "Framework Terminology - Quality Gates"

test_case "Guidance references all 4 quality gates"
if [ -f "$GUIDANCE_FILE" ]; then
    gate1=$(grep -c "Gate 1\|Quality Gate 1\|Context.*validation" "$GUIDANCE_FILE" 2>/dev/null || echo "0")
    gate2=$(grep -c "Gate 2\|Quality Gate 2\|Test.*passing" "$GUIDANCE_FILE" 2>/dev/null || echo "0")
    gate3=$(grep -c "Gate 3\|Quality Gate 3\|QA.*approv" "$GUIDANCE_FILE" 2>/dev/null || echo "0")
    gate4=$(grep -c "Gate 4\|Quality Gate 4\|Release.*readiness" "$GUIDANCE_FILE" 2>/dev/null || echo "0")

    gate_count=0
    [ "$gate1" -gt 0 ] && gate_count=$((gate_count + 1))
    [ "$gate2" -gt 0 ] && gate_count=$((gate_count + 1))
    [ "$gate3" -gt 0 ] && gate_count=$((gate_count + 1))
    [ "$gate4" -gt 0 ] && gate_count=$((gate_count + 1))

    if [ "$gate_count" -ge 3 ]; then
        pass_test "Found $gate_count/4 quality gates referenced"
    else
        fail_test "Found only $gate_count/4 quality gates (need ≥3)"
    fi
else
    skip_test "Quality gate validation"
fi

header "Framework Terminology - Workflow States"

test_case "Guidance references workflow states correctly"
if [ -f "$GUIDANCE_FILE" ]; then
    backlog=$(grep -c "Backlog" "$GUIDANCE_FILE" 2>/dev/null || echo "0")
    architecture=$(grep -c "Architecture" "$GUIDANCE_FILE" 2>/dev/null || echo "0")
    ready=$(grep -c "Ready for Dev" "$GUIDANCE_FILE" 2>/dev/null || echo "0")
    dev=$(grep -c "In Development\|Development" "$GUIDANCE_FILE" 2>/dev/null || echo "0")

    state_count=0
    [ "$backlog" -gt 0 ] && state_count=$((state_count + 1))
    [ "$architecture" -gt 0 ] && state_count=$((state_count + 1))
    [ "$ready" -gt 0 ] && state_count=$((state_count + 1))
    [ "$dev" -gt 0 ] && state_count=$((state_count + 1))

    if [ "$state_count" -ge 3 ]; then
        pass_test "Found $state_count/4 workflow states referenced"
    else
        fail_test "Found only $state_count/4 workflow states"
    fi
else
    skip_test "Workflow state validation"
fi

header "Framework Terminology - Story Structure"

test_case "Guidance uses correct story structure terminology"
if [ -f "$GUIDANCE_FILE" ]; then
    yaml=$(grep -c "YAML\|frontmatter\|metadata" "$GUIDANCE_FILE" 2>/dev/null || echo "0")
    given=$(grep -c "Given/When/Then\|Given.*When.*Then\|acceptance criteria" "$GUIDANCE_FILE" 2>/dev/null || echo "0")
    tech_spec=$(grep -c "Technical.*Specification\|technical specification" "$GUIDANCE_FILE" 2>/dev/null || echo "0")

    struct_count=0
    [ "$yaml" -gt 0 ] && struct_count=$((struct_count + 1))
    [ "$given" -gt 0 ] && struct_count=$((struct_count + 1))
    [ "$tech_spec" -gt 0 ] && struct_count=$((struct_count + 1))

    if [ "$struct_count" -ge 2 ]; then
        pass_test "Found $struct_count/3 story structure elements referenced"
    else
        fail_test "Found only $struct_count/3 story structure elements"
    fi
else
    skip_test "Story structure validation"
fi

header "Framework Terminology - Core Concepts"

test_case "Guidance uses DevForgeAI core concept terminology"
if [ -f "$GUIDANCE_FILE" ]; then
    dod=$(grep -c "Definition of Done\|DoD" "$GUIDANCE_FILE" 2>/dev/null || echo "0")
    tdd=$(grep -c "Test.*Driven\|TDD\|Red.*Green.*Refactor" "$GUIDANCE_FILE" 2>/dev/null || echo "0")
    aaa=$(grep -c "Arrange.*Act.*Assert\|AAA pattern" "$GUIDANCE_FILE" 2>/dev/null || echo "0")

    core_count=0
    [ "$dod" -gt 0 ] && core_count=$((core_count + 1))
    [ "$tdd" -gt 0 ] && core_count=$((core_count + 1))
    [ "$aaa" -gt 0 ] && core_count=$((core_count + 1))

    if [ "$core_count" -ge 2 ]; then
        pass_test "Found $core_count/3 core concept references"
    else
        fail_test "Found only $core_count/3 core concepts"
    fi
else
    skip_test "Core concept validation"
fi

header "BR-004: Reference File Path Validation"

test_case "All file path references use correct format (.claude/ or .devforgeai/)"
if [ -f "$GUIDANCE_FILE" ]; then
    # Check for file references
    claude_refs=$(grep -c "\.claude/" "$GUIDANCE_FILE" 2>/dev/null || echo "0")
    devforgeai_refs=$(grep -c "\.devforgeai/" "$GUIDANCE_FILE" 2>/dev/null || echo "0")

    if [ "$claude_refs" -gt 0 ] || [ "$devforgeai_refs" -gt 0 ]; then
        pass_test "Found framework file references ($claude_refs .claude/, $devforgeai_refs .devforgeai/)"
    else
        fail_test "No framework file references found"
    fi
else
    skip_test "File path format validation"
fi

test_case "No external URLs in guidance (references only to .claude/ and .devforgeai/)"
if [ -f "$GUIDANCE_FILE" ]; then
    external_urls=$(grep -c "http://\|https://\|www\." "$GUIDANCE_FILE" 2>/dev/null || echo "0")
    if [ "$external_urls" -eq 0 ]; then
        pass_test "No external URLs found (framework-only references)"
    else
        fail_test "Found $external_urls external URL references (should be 0)"
    fi
else
    skip_test "External URL validation"
fi

test_case "All referenced files exist in framework"
if [ -f "$GUIDANCE_FILE" ]; then
    # Sample some commonly referenced files
    files_to_check=(
        "CLAUDE.md"
        ".claude/memory/skills-reference.md"
        "devforgeai/context/tech-stack.md"
        "devforgeai/context/source-tree.md"
    )

    existing_count=0
    for file in "${files_to_check[@]}"; do
        if [ -f "$file" ] 2>/dev/null; then
            existing_count=$((existing_count + 1))
        fi
    done

    if [ "$existing_count" -ge 3 ]; then
        pass_test "Framework files exist ($existing_count/4 sampled files found)"
    else
        fail_test "Some referenced framework files may not exist"
    fi
else
    skip_test "Referenced file existence validation"
fi

header "CLAUDE.md Consistency Check"

test_case "Key DevForgeAI terms match CLAUDE.md definitions"
if [ -f "$CLAUDE_MD" ] && [ -f "$GUIDANCE_FILE" ]; then
    # Extract key terms from CLAUDE.md
    terms=("specification-driven" "TDD" "AAA pattern" "test pyramid" "Definition of Done")

    matching_terms=0
    for term in "${terms[@]}"; do
        if grep -q "$term" "$CLAUDE_MD" 2>/dev/null && grep -q "$term" "$GUIDANCE_FILE" 2>/dev/null; then
            matching_terms=$((matching_terms + 1))
        fi
    done

    if [ "$matching_terms" -ge 3 ]; then
        pass_test "Found $matching_terms matching terminology with CLAUDE.md"
    else
        fail_test "Found only $matching_terms matching terms (need ≥3)"
    fi
else
    skip_test "CLAUDE.md consistency check"
fi

header "Cross-Reference Documentation"

test_case "Guidance includes cross-references to effective-prompting-guide.md"
if [ -f "$GUIDANCE_FILE" ]; then
    prompt_refs=$(grep -c "effective-prompting\|prompting guide\|user-facing" "$GUIDANCE_FILE" 2>/dev/null || echo "0")
    if [ "$prompt_refs" -ge 2 ]; then
        pass_test "Found $prompt_refs references to prompting guide"
    else
        fail_test "Found only $prompt_refs references to prompting guide (need ≥2)"
    fi
else
    skip_test "Prompting guide cross-reference validation"
fi

test_case "Guidance includes cross-references to claude-code-terminal-expert"
if [ -f "$GUIDANCE_FILE" ]; then
    terminal_refs=$(grep -c "claude-code\|terminal\|Claude Code" "$GUIDANCE_FILE" 2>/dev/null || echo "0")
    if [ "$terminal_refs" -ge 2 ]; then
        pass_test "Found $terminal_refs references to Claude Code expert"
    else
        fail_test "Found only $terminal_refs references to Claude Code (need ≥2)"
    fi
else
    skip_test "Claude Code expert cross-reference validation"
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
