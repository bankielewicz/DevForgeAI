#!/bin/bash
# Test AC#4: Core File Retains Essential Scanning Specification
# STORY-401: Extract Anti-Pattern-Scanner to Reference Files
#
# Validates core file retains:
# - YAML frontmatter
# - Purpose section
# - 4 Guardrails section
# - 6 Detection Categories (all 6 category headers)
# - Input/Output Contracts
# - 9-Phase Workflow summary (all 9 phase headers)
# - Error Handling
# - Success Criteria
# - Progressive Disclosure References table
#
# Expected: FAIL initially (some sections may be removed during extraction)

# Configuration
PROJECT_ROOT="/mnt/c/Projects/DevForgeAI2"
CORE_FILE="$PROJECT_ROOT/src/claude/agents/anti-pattern-scanner.md"

# Test tracking
TESTS_RUN=0
TESTS_PASSED=0
TESTS_FAILED=0

# Test helper functions
pass_test() {
    local test_name="$1"
    TESTS_PASSED=$((TESTS_PASSED + 1))
    echo "[PASS] $test_name"
}

fail_test() {
    local test_name="$1"
    local message="$2"
    TESTS_FAILED=$((TESTS_FAILED + 1))
    echo "[FAIL] $test_name: $message"
}

run_test() {
    local test_name="$1"
    TESTS_RUN=$((TESTS_RUN + 1))
    shift
    "$@"
}

# -----------------------------------------------------------------------------
# Test 1: YAML frontmatter present
# -----------------------------------------------------------------------------
test_yaml_frontmatter() {
    local test_name="YAML frontmatter present"

    if [ ! -f "$CORE_FILE" ]; then
        fail_test "$test_name" "Cannot check - file does not exist"
        return
    fi

    local first_line
    first_line=$(head -n 1 "$CORE_FILE")

    if [ "$first_line" = "---" ]; then
        if grep -n "^---$" "$CORE_FILE" | head -n 2 | tail -n 1 | grep -q ":"; then
            pass_test "$test_name"
        else
            fail_test "$test_name" "YAML frontmatter not properly closed"
        fi
    else
        fail_test "$test_name" "File does not start with YAML frontmatter delimiter (---)"
    fi
}

# -----------------------------------------------------------------------------
# Test 2: Purpose section present
# -----------------------------------------------------------------------------
test_purpose_section() {
    local test_name="Purpose section present"

    if [ ! -f "$CORE_FILE" ]; then
        fail_test "$test_name" "Cannot check - file does not exist"
        return
    fi

    if grep -qE "^## Purpose" "$CORE_FILE"; then
        pass_test "$test_name"
    else
        fail_test "$test_name" "Missing '## Purpose' section header"
    fi
}

# -----------------------------------------------------------------------------
# Test 3: 4 Guardrails section present
# -----------------------------------------------------------------------------
test_guardrails_section() {
    local test_name="4 Guardrails section present"

    if [ ! -f "$CORE_FILE" ]; then
        fail_test "$test_name" "Cannot check - file does not exist"
        return
    fi

    if grep -qE "^## 4 Guardrails" "$CORE_FILE"; then
        pass_test "$test_name"
    else
        fail_test "$test_name" "Missing '## 4 Guardrails' section header"
    fi
}

# -----------------------------------------------------------------------------
# Test 4: All 6 Detection Category headers present
# -----------------------------------------------------------------------------
test_six_detection_categories() {
    local test_name="All 6 Detection Category headers present"

    if [ ! -f "$CORE_FILE" ]; then
        fail_test "$test_name" "Cannot check - file does not exist"
        return
    fi

    local missing=""
    local categories=(
        "Category 1"
        "Category 2"
        "Category 3"
        "Category 4"
        "Category 5"
        "Category 6"
    )

    for cat in "${categories[@]}"; do
        if ! grep -q "### $cat" "$CORE_FILE"; then
            missing="$missing $cat"
        fi
    done

    if [ -z "$missing" ]; then
        pass_test "$test_name"
    else
        fail_test "$test_name" "Missing categories:$missing"
    fi
}

# -----------------------------------------------------------------------------
# Test 5: Input Contract section present
# -----------------------------------------------------------------------------
test_input_contract() {
    local test_name="Input Contract section present"

    if [ ! -f "$CORE_FILE" ]; then
        fail_test "$test_name" "Cannot check - file does not exist"
        return
    fi

    if grep -qE "^## Input Contract" "$CORE_FILE"; then
        pass_test "$test_name"
    else
        fail_test "$test_name" "Missing '## Input Contract' section header"
    fi
}

# -----------------------------------------------------------------------------
# Test 6: Output Contract section present
# -----------------------------------------------------------------------------
test_output_contract() {
    local test_name="Output Contract section present"

    if [ ! -f "$CORE_FILE" ]; then
        fail_test "$test_name" "Cannot check - file does not exist"
        return
    fi

    if grep -qE "^## Output Contract" "$CORE_FILE"; then
        pass_test "$test_name"
    else
        fail_test "$test_name" "Missing '## Output Contract' section header"
    fi
}

# -----------------------------------------------------------------------------
# Test 7: All 9 Phase headers present in workflow
# -----------------------------------------------------------------------------
test_nine_phase_headers() {
    local test_name="All 9 Phase headers present in workflow"

    if [ ! -f "$CORE_FILE" ]; then
        fail_test "$test_name" "Cannot check - file does not exist"
        return
    fi

    local missing=""

    for i in $(seq 1 9); do
        if ! grep -q "### Phase $i:" "$CORE_FILE"; then
            missing="$missing Phase$i"
        fi
    done

    if [ -z "$missing" ]; then
        pass_test "$test_name"
    else
        fail_test "$test_name" "Missing phases:$missing"
    fi
}

# -----------------------------------------------------------------------------
# Test 8: Error Handling section present
# -----------------------------------------------------------------------------
test_error_handling() {
    local test_name="Error Handling section present"

    if [ ! -f "$CORE_FILE" ]; then
        fail_test "$test_name" "Cannot check - file does not exist"
        return
    fi

    if grep -qE "^## Error Handling" "$CORE_FILE"; then
        pass_test "$test_name"
    else
        fail_test "$test_name" "Missing '## Error Handling' section header"
    fi
}

# -----------------------------------------------------------------------------
# Test 9: Success Criteria section present
# -----------------------------------------------------------------------------
test_success_criteria() {
    local test_name="Success Criteria section present"

    if [ ! -f "$CORE_FILE" ]; then
        fail_test "$test_name" "Cannot check - file does not exist"
        return
    fi

    if grep -qE "^## Success Criteria" "$CORE_FILE"; then
        pass_test "$test_name"
    else
        fail_test "$test_name" "Missing '## Success Criteria' section header"
    fi
}

# -----------------------------------------------------------------------------
# Test 10: Progressive Disclosure References section present
# -----------------------------------------------------------------------------
test_progressive_disclosure_references() {
    local test_name="Progressive Disclosure References section present"

    if [ ! -f "$CORE_FILE" ]; then
        fail_test "$test_name" "Cannot check - file does not exist"
        return
    fi

    if grep -qE "^## Progressive Disclosure References" "$CORE_FILE"; then
        pass_test "$test_name"
    else
        fail_test "$test_name" "Missing '## Progressive Disclosure References' section header"
    fi
}

# -----------------------------------------------------------------------------
# Main test execution
# -----------------------------------------------------------------------------
echo "=============================================="
echo "STORY-401 AC#4: Essential Scanning Spec"
echo "=============================================="
echo "Target file: $CORE_FILE"
echo "Required sections: 10"
echo "----------------------------------------------"
echo ""

run_test "1" test_yaml_frontmatter
run_test "2" test_purpose_section
run_test "3" test_guardrails_section
run_test "4" test_six_detection_categories
run_test "5" test_input_contract
run_test "6" test_output_contract
run_test "7" test_nine_phase_headers
run_test "8" test_error_handling
run_test "9" test_success_criteria
run_test "10" test_progressive_disclosure_references

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
