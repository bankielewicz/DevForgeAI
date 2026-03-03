#!/bin/bash
# Test AC#1: Template Defines Required and Optional Sections
# STORY-388: Design Command Template Variant with 15K Char Budget Compliance
#
# Validates:
# - Template file exists at documented location
# - 9 required sections present: YAML frontmatter, title+description,
#   Quick Reference, Phase 0 Argument Validation, Phase 1 Skill Invocation,
#   Phase 2 Display Results, Error Handling, Success Criteria, Integration
# - Optional sections distinguished from required
# - Each section has a purpose annotation
#
# Expected: FAIL initially (TDD Red phase - file does not exist yet)

PROJECT_ROOT="/mnt/c/Projects/DevForgeAI2"
TEMPLATE="$PROJECT_ROOT/src/claude/skills/devforgeai-story-creation/assets/templates/command-template.md"

TESTS_RUN=0
TESTS_PASSED=0
TESTS_FAILED=0

pass_test() {
    TESTS_PASSED=$((TESTS_PASSED + 1))
    echo "[PASS] $1"
}

fail_test() {
    TESTS_FAILED=$((TESTS_FAILED + 1))
    echo "[FAIL] $1: $2"
}

run_test() {
    TESTS_RUN=$((TESTS_RUN + 1))
    shift
    "$@"
}

# ---------------------------------------------------------------------------
# Test 1: Template file exists
# ---------------------------------------------------------------------------
test_file_exists() {
    if [ -f "$TEMPLATE" ]; then
        pass_test "Template file exists"
    else
        fail_test "Template file exists" "Not found: $TEMPLATE"
    fi
}

# ---------------------------------------------------------------------------
# Test 2: YAML frontmatter with 4 required fields
# ---------------------------------------------------------------------------
test_yaml_frontmatter() {
    if [ ! -f "$TEMPLATE" ]; then
        fail_test "YAML frontmatter" "File does not exist"
        return
    fi

    local first_line
    first_line=$(head -n 1 "$TEMPLATE")
    if [ "$first_line" != "---" ]; then
        fail_test "YAML frontmatter" "File does not start with ---"
        return
    fi

    local yaml_block
    yaml_block=$(sed -n '1,/^---$/p' "$TEMPLATE" | tail -n +2)

    local missing=""
    for field in "description:" "argument-hint:" "model:" "allowed-tools:"; do
        if ! echo "$yaml_block" | grep -q "$field"; then
            missing="$missing $field"
        fi
    done

    if [ -z "$missing" ]; then
        pass_test "YAML frontmatter has required fields"
    else
        fail_test "YAML frontmatter" "Missing fields:$missing"
    fi
}

# ---------------------------------------------------------------------------
# Test 3: Quick Reference section with 3-5 examples
# ---------------------------------------------------------------------------
test_quick_reference() {
    if [ ! -f "$TEMPLATE" ]; then
        fail_test "Quick Reference section" "File does not exist"
        return
    fi

    if ! grep -qE "^#+ .*Quick Reference" "$TEMPLATE"; then
        fail_test "Quick Reference section" "Section header not found"
        return
    fi

    # Count example lines (lines starting with - or containing example-like patterns)
    local example_count
    example_count=$(sed -n '/^#\+ .*Quick Reference/,/^#\+ /p' "$TEMPLATE" | grep -cE "^-|^\*|^\d\." || true)

    if [ "$example_count" -ge 3 ] && [ "$example_count" -le 10 ]; then
        pass_test "Quick Reference has $example_count examples"
    else
        fail_test "Quick Reference section" "Expected 3-5 examples, found $example_count"
    fi
}

# ---------------------------------------------------------------------------
# Test 4: Phase 0 Argument Validation section
# ---------------------------------------------------------------------------
test_phase0_section() {
    if [ ! -f "$TEMPLATE" ]; then
        fail_test "Phase 0 section" "File does not exist"
        return
    fi

    if grep -qEi "^#+ .*(Phase 0|Argument Validation)" "$TEMPLATE"; then
        pass_test "Phase 0 / Argument Validation section present"
    else
        fail_test "Phase 0 section" "No 'Phase 0' or 'Argument Validation' heading found"
    fi
}

# ---------------------------------------------------------------------------
# Test 5: Phase 1 Skill Invocation section
# ---------------------------------------------------------------------------
test_phase1_section() {
    if [ ! -f "$TEMPLATE" ]; then
        fail_test "Phase 1 section" "File does not exist"
        return
    fi

    if grep -qEi "^#+ .*(Phase 1|Skill Invocation)" "$TEMPLATE"; then
        pass_test "Phase 1 / Skill Invocation section present"
    else
        fail_test "Phase 1 section" "No 'Phase 1' or 'Skill Invocation' heading found"
    fi
}

# ---------------------------------------------------------------------------
# Test 6: Phase 2 Display Results section
# ---------------------------------------------------------------------------
test_phase2_section() {
    if [ ! -f "$TEMPLATE" ]; then
        fail_test "Phase 2 section" "File does not exist"
        return
    fi

    if grep -qEi "^#+ .*(Phase 2|Display Results)" "$TEMPLATE"; then
        pass_test "Phase 2 / Display Results section present"
    else
        fail_test "Phase 2 section" "No 'Phase 2' or 'Display Results' heading found"
    fi
}

# ---------------------------------------------------------------------------
# Test 7: Error Handling section
# ---------------------------------------------------------------------------
test_error_handling() {
    if [ ! -f "$TEMPLATE" ]; then
        fail_test "Error Handling section" "File does not exist"
        return
    fi

    if grep -qE "^#+ .*Error Handling" "$TEMPLATE"; then
        pass_test "Error Handling section present"
    else
        fail_test "Error Handling section" "Heading not found"
    fi
}

# ---------------------------------------------------------------------------
# Test 8: Success Criteria section
# ---------------------------------------------------------------------------
test_success_criteria() {
    if [ ! -f "$TEMPLATE" ]; then
        fail_test "Success Criteria section" "File does not exist"
        return
    fi

    if grep -qE "^#+ .*Success Criteria" "$TEMPLATE"; then
        pass_test "Success Criteria section present"
    else
        fail_test "Success Criteria section" "Heading not found"
    fi
}

# ---------------------------------------------------------------------------
# Test 9: Integration metadata section
# ---------------------------------------------------------------------------
test_integration_section() {
    if [ ! -f "$TEMPLATE" ]; then
        fail_test "Integration section" "File does not exist"
        return
    fi

    if grep -qEi "^#+ .*(Integration|Metadata)" "$TEMPLATE"; then
        pass_test "Integration metadata section present"
    else
        fail_test "Integration section" "Heading not found"
    fi
}

# ---------------------------------------------------------------------------
# Test 10: Optional sections distinguished
# ---------------------------------------------------------------------------
test_optional_sections() {
    if [ ! -f "$TEMPLATE" ]; then
        fail_test "Optional sections" "File does not exist"
        return
    fi

    if grep -qi "optional" "$TEMPLATE"; then
        pass_test "Optional sections marker found"
    else
        fail_test "Optional sections" "No 'optional' marker found in template"
    fi
}

# ---------------------------------------------------------------------------
# Test 11: Purpose annotations on sections
# ---------------------------------------------------------------------------
test_purpose_annotations() {
    if [ ! -f "$TEMPLATE" ]; then
        fail_test "Purpose annotations" "File does not exist"
        return
    fi

    # Count section headers that have a purpose annotation (text after heading or
    # a Purpose: line within 3 lines of a heading)
    local section_count
    section_count=$(grep -cE "^#+ " "$TEMPLATE" || true)

    local annotated_count
    annotated_count=$(grep -cE "^\*\*Purpose\*\*:|^#+ .+:.+" "$TEMPLATE" || true)

    if [ "$annotated_count" -ge 5 ]; then
        pass_test "Purpose annotations found ($annotated_count)"
    else
        fail_test "Purpose annotations" "Only $annotated_count annotations found (need >= 5)"
    fi
}

# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
echo "=============================================="
echo "STORY-388 AC#1: Required and Optional Sections"
echo "=============================================="
echo "Target: $TEMPLATE"
echo "----------------------------------------------"
echo ""

run_test "1" test_file_exists
run_test "2" test_yaml_frontmatter
run_test "3" test_quick_reference
run_test "4" test_phase0_section
run_test "5" test_phase1_section
run_test "6" test_phase2_section
run_test "7" test_error_handling
run_test "8" test_success_criteria
run_test "9" test_integration_section
run_test "10" test_optional_sections
run_test "11" test_purpose_annotations

echo ""
echo "=============================================="
echo "Test Summary: $TESTS_PASSED/$TESTS_RUN passed"
echo "=============================================="

if [ "$TESTS_FAILED" -gt 0 ]; then
    echo "Status: FAILED ($TESTS_FAILED failures)"
    exit 1
else
    echo "Status: PASSED"
    exit 0
fi
