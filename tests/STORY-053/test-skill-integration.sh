#!/bin/bash
###############################################################################
# Test Suite: STORY-053 - Skill Integration Validation
# Purpose: Validate AC4 - Skill Integration Success (5 skills can load file)
# Tests: DOC-004, NFR-002, NFR-009 - Integration sections, Read commands, 5 skills
###############################################################################

set -euo pipefail

GUIDANCE_FILE="src/claude/skills/devforgeai-ideation/references/user-input-guidance.md"
SKILLS_DIR=".claude/skills"
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

echo "STORY-053 Skill Integration Validation Tests"

if [ ! -f "$GUIDANCE_FILE" ]; then
    echo "WARNING: Guidance file does not exist: $GUIDANCE_FILE"
    echo "All tests will FAIL in RED phase until file is created."
    echo ""
fi

header "AC4: Skill Integration Success"

test_case "File exists at expected location"
if [ -f "$GUIDANCE_FILE" ]; then
    pass_test "File exists: $GUIDANCE_FILE"
else
    fail_test "File does not exist: $GUIDANCE_FILE"
fi

test_case "Document includes 5 skill integration sections"
if [ -f "$GUIDANCE_FILE" ]; then
    # Look for integration sections for each skill
    ideation_count=$(grep -c "devforgeai-ideation\|Integration.*Ideation" "$GUIDANCE_FILE" 2>/dev/null || echo "0")
    story_creation_count=$(grep -c "devforgeai-story-creation\|Integration.*Story" "$GUIDANCE_FILE" 2>/dev/null || echo "0")
    architecture_count=$(grep -c "devforgeai-architecture\|Integration.*Architecture" "$GUIDANCE_FILE" 2>/dev/null || echo "0")
    ui_count=$(grep -c "devforgeai-ui-generator\|Integration.*UI" "$GUIDANCE_FILE" 2>/dev/null || echo "0")
    orchestration_count=$(grep -c "devforgeai-orchestration\|Integration.*Orchestration" "$GUIDANCE_FILE" 2>/dev/null || echo "0")

    integration_count=$((ideation_count + story_creation_count + architecture_count + ui_count + orchestration_count))

    if [ "$integration_count" -ge 5 ]; then
        pass_test "Found integration references for 5 skills"
    else
        fail_test "Found integration references for only $integration_count/5 skills"
    fi
else
    skip_test "Skill integration count validation"
fi

test_case "Each integration section specifies workflow phase"
if [ -f "$GUIDANCE_FILE" ]; then
    phase_refs=$(grep -c "Phase [0-9]\|Phase.*Step\|Workflow.*Phase" "$GUIDANCE_FILE" 2>/dev/null || echo "0")
    if [ "$phase_refs" -ge 5 ]; then
        pass_test "Found $phase_refs phase references (≥5 required)"
    else
        fail_test "Found only $phase_refs phase references (need ≥5)"
    fi
else
    skip_test "Workflow phase validation"
fi

test_case "Each integration section documents use cases (3-5 per skill)"
if [ -f "$GUIDANCE_FILE" ]; then
    use_case_lines=$(grep -c "Use case\|Scenario\|Example:\|When to use" "$GUIDANCE_FILE" 2>/dev/null || echo "0")
    if [ "$use_case_lines" -ge 15 ]; then
        pass_test "Found $use_case_lines use case references (need ≥15 for 3+ per skill)"
    else
        fail_test "Found only $use_case_lines use case references"
    fi
else
    skip_test "Use case validation"
fi

header "DOC-004: Read Command Syntax Validation"

test_case "Integration sections include valid Read commands"
if [ -f "$GUIDANCE_FILE" ]; then
    # Count Read(...) patterns
    read_commands=$(grep -c "Read(" "$GUIDANCE_FILE" 2>/dev/null || echo "0")
    if [ "$read_commands" -ge 5 ]; then
        pass_test "Found $read_commands Read command references"
    else
        fail_test "Found only $read_commands Read commands (need ≥5)"
    fi
else
    skip_test "Read command validation"
fi

test_case "Read commands reference user-input-guidance.md file path"
if [ -f "$GUIDANCE_FILE" ]; then
    file_refs=$(grep -c "user-input-guidance.md" "$GUIDANCE_FILE" 2>/dev/null || echo "0")
    if [ "$file_refs" -ge 2 ]; then
        pass_test "Found $file_refs references to user-input-guidance.md"
    else
        fail_test "Found only $file_refs references to the guidance file"
    fi
else
    skip_test "File path reference validation"
fi

test_case "Read commands use correct absolute file path format"
if [ -f "$GUIDANCE_FILE" ]; then
    # Check for proper path syntax
    proper_paths=$(grep -c 'src/claude/skills.*user-input-guidance.md\|\.claude/skills.*user-input-guidance.md' "$GUIDANCE_FILE" 2>/dev/null || echo "0")
    if [ "$proper_paths" -ge 1 ]; then
        pass_test "Found correct file path references ($proper_paths)"
    else
        fail_test "File path references may not use correct absolute paths"
    fi
else
    skip_test "Path format validation"
fi

header "NFR-002: Performance - Grep Search Time"

test_case "Document is searchable via Grep"
if [ -f "$GUIDANCE_FILE" ]; then
    # Time a grep search
    start_time=$(date +%s%N)
    grep_result=$(grep -c "Pattern\|Template\|Table" "$GUIDANCE_FILE" 2>/dev/null || echo "0")
    end_time=$(date +%s%N)

    elapsed_ns=$((end_time - start_time))
    elapsed_ms=$((elapsed_ns / 1000000))

    if [ "$elapsed_ms" -lt 30000 ]; then  # 30 seconds in milliseconds
        pass_test "Grep search completed in ${elapsed_ms}ms (< 30s required)"
    else
        fail_test "Grep search took ${elapsed_ms}ms (need < 30s)"
    fi

    if [ "$grep_result" -gt 20 ]; then
        pass_test "Grep found $grep_result searchable elements"
    fi
else
    skip_test "Grep performance test"
fi

header "NFR-009: Single File Reusability"

test_case "Only one user-input-guidance.md file exists"
if [ -f "$GUIDANCE_FILE" ]; then
    file_count=$(find . -name "user-input-guidance.md" -type f 2>/dev/null | wc -l || echo "0")
    if [ "$file_count" -eq 1 ]; then
        pass_test "Single guidance file found at: $GUIDANCE_FILE"
    else
        fail_test "Found $file_count user-input-guidance.md files (should be 1)"
    fi
else
    skip_test "File uniqueness validation"
fi

test_case "5 skills reference the same guidance file"
if [ -d "$SKILLS_DIR" ]; then
    # Check if each skill's SKILL.md references the guidance file
    skills_referencing=0

    for skill_dir in "$SKILLS_DIR"/devforgeai-{ideation,story-creation,architecture,ui-generator,orchestration}; do
        if [ -f "$skill_dir/SKILL.md" ]; then
            if grep -q "user-input-guidance" "$skill_dir/SKILL.md" 2>/dev/null; then
                skills_referencing=$((skills_referencing + 1))
                skill_name=$(basename "$skill_dir")
                echo "  ✓ $skill_name references guidance file"
            fi
        fi
    done

    if [ "$skills_referencing" -ge 5 ]; then
        pass_test "All 5 skills reference the guidance file"
    else
        fail_test "Only $skills_referencing/5 skills reference the guidance file"
    fi
else
    skip_test "Skill reference validation"
fi

header "Integration Completeness Validation"

test_case "Ideation skill integration documented"
if [ -f "$GUIDANCE_FILE" ]; then
    if grep -q "devforgeai-ideation" "$GUIDANCE_FILE" 2>/dev/null; then
        pass_test "Ideation skill integration found"
    else
        fail_test "Ideation skill integration not documented"
    fi
else
    skip_test "Ideation integration validation"
fi

test_case "Story-Creation skill integration documented"
if [ -f "$GUIDANCE_FILE" ]; then
    if grep -q "devforgeai-story-creation" "$GUIDANCE_FILE" 2>/dev/null; then
        pass_test "Story-Creation skill integration found"
    else
        fail_test "Story-Creation skill integration not documented"
    fi
else
    skip_test "Story-Creation integration validation"
fi

test_case "Architecture skill integration documented"
if [ -f "$GUIDANCE_FILE" ]; then
    if grep -q "devforgeai-architecture" "$GUIDANCE_FILE" 2>/dev/null; then
        pass_test "Architecture skill integration found"
    else
        fail_test "Architecture skill integration not documented"
    fi
else
    skip_test "Architecture integration validation"
fi

test_case "UI-Generator skill integration documented"
if [ -f "$GUIDANCE_FILE" ]; then
    if grep -q "devforgeai-ui-generator" "$GUIDANCE_FILE" 2>/dev/null; then
        pass_test "UI-Generator skill integration found"
    else
        fail_test "UI-Generator skill integration not documented"
    fi
else
    skip_test "UI-Generator integration validation"
fi

test_case "Orchestration skill integration documented"
if [ -f "$GUIDANCE_FILE" ]; then
    if grep -q "devforgeai-orchestration" "$GUIDANCE_FILE" 2>/dev/null; then
        pass_test "Orchestration skill integration found"
    else
        fail_test "Orchestration skill integration not documented"
    fi
else
    skip_test "Orchestration integration validation"
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
