#!/bin/bash
# Test AC#1: Core File Size Compliance
# STORY-331: Refactor agent-generator.md with Progressive Disclosure
#
# Validates:
# - Core file src/claude/agents/agent-generator.md contains <= 300 lines
# - All 8 required sections present:
#   1. YAML frontmatter
#   2. Purpose
#   3. When Invoked
#   4. Core Workflow
#   5. Success Criteria
#   6. Error Handling
#   7. Reference Loading
#   8. Observation Capture
#
# Expected: FAIL initially (TDD Red phase - file currently has 2,370 lines)

# Note: Not using set -e due to arithmetic operations with (( ))

# Configuration
PROJECT_ROOT="/mnt/c/Projects/DevForgeAI2"
CORE_FILE="$PROJECT_ROOT/src/claude/agents/agent-generator.md"
MAX_LINES=300

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
# Test 1: Core file exists
# -----------------------------------------------------------------------------
test_core_file_exists() {
    local test_name="Core file exists"
    if [ -f "$CORE_FILE" ]; then
        pass_test "$test_name"
    else
        fail_test "$test_name" "File not found: $CORE_FILE"
    fi
}

# -----------------------------------------------------------------------------
# Test 2: Core file line count <= 300
# -----------------------------------------------------------------------------
test_core_file_line_count() {
    local test_name="Core file line count <= $MAX_LINES"

    if [ ! -f "$CORE_FILE" ]; then
        fail_test "$test_name" "Cannot check - file does not exist"
        return
    fi

    local line_count
    line_count=$(wc -l < "$CORE_FILE")

    if [ "$line_count" -le "$MAX_LINES" ]; then
        pass_test "$test_name (actual: $line_count lines)"
    else
        fail_test "$test_name" "File has $line_count lines (max allowed: $MAX_LINES)"
    fi
}

# -----------------------------------------------------------------------------
# Test 3: YAML frontmatter present
# -----------------------------------------------------------------------------
test_yaml_frontmatter() {
    local test_name="YAML frontmatter present"

    if [ ! -f "$CORE_FILE" ]; then
        fail_test "$test_name" "Cannot check - file does not exist"
        return
    fi

    # Check for YAML frontmatter delimiters at start of file
    local first_line
    first_line=$(head -n 1 "$CORE_FILE")

    if [ "$first_line" = "---" ]; then
        # Check for closing delimiter
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
# Test 4: Required YAML fields present
# -----------------------------------------------------------------------------
test_yaml_required_fields() {
    local test_name="YAML frontmatter contains required fields"

    if [ ! -f "$CORE_FILE" ]; then
        fail_test "$test_name" "Cannot check - file does not exist"
        return
    fi

    local missing_fields=""
    local required_fields=("name:" "description:" "tools:" "model:")

    # Extract YAML frontmatter (between first two --- lines)
    local yaml_content
    yaml_content=$(sed -n '/^---$/,/^---$/p' "$CORE_FILE" | head -n 50)

    for field in "${required_fields[@]}"; do
        if ! echo "$yaml_content" | grep -q "^$field"; then
            missing_fields="$missing_fields $field"
        fi
    done

    if [ -z "$missing_fields" ]; then
        pass_test "$test_name"
    else
        fail_test "$test_name" "Missing required fields:$missing_fields"
    fi
}

# -----------------------------------------------------------------------------
# Test 5: Purpose section present
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
# Test 6: When Invoked section present
# -----------------------------------------------------------------------------
test_when_invoked_section() {
    local test_name="When Invoked section present"

    if [ ! -f "$CORE_FILE" ]; then
        fail_test "$test_name" "Cannot check - file does not exist"
        return
    fi

    if grep -qE "^## When Invoked" "$CORE_FILE"; then
        pass_test "$test_name"
    else
        fail_test "$test_name" "Missing '## When Invoked' section header"
    fi
}

# -----------------------------------------------------------------------------
# Test 7: Core Workflow section present
# -----------------------------------------------------------------------------
test_core_workflow_section() {
    local test_name="Core Workflow section present"

    if [ ! -f "$CORE_FILE" ]; then
        fail_test "$test_name" "Cannot check - file does not exist"
        return
    fi

    # Accept either "## Core Workflow" or "## Workflow" as valid
    if grep -qE "^## (Core )?Workflow" "$CORE_FILE"; then
        pass_test "$test_name"
    else
        fail_test "$test_name" "Missing '## Core Workflow' or '## Workflow' section header"
    fi
}

# -----------------------------------------------------------------------------
# Test 8: Success Criteria section present
# -----------------------------------------------------------------------------
test_success_criteria_section() {
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
# Test 9: Error Handling section present
# -----------------------------------------------------------------------------
test_error_handling_section() {
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
# Test 10: Reference Loading section present
# -----------------------------------------------------------------------------
test_reference_loading_section() {
    local test_name="Reference Loading section present"

    if [ ! -f "$CORE_FILE" ]; then
        fail_test "$test_name" "Cannot check - file does not exist"
        return
    fi

    if grep -qE "^## Reference(s)? Loading" "$CORE_FILE"; then
        pass_test "$test_name"
    else
        fail_test "$test_name" "Missing '## Reference Loading' section header"
    fi
}

# -----------------------------------------------------------------------------
# Test 11: Observation Capture section present
# -----------------------------------------------------------------------------
test_observation_capture_section() {
    local test_name="Observation Capture section present"

    if [ ! -f "$CORE_FILE" ]; then
        fail_test "$test_name" "Cannot check - file does not exist"
        return
    fi

    if grep -qE "^## Observation Capture" "$CORE_FILE"; then
        pass_test "$test_name"
    else
        fail_test "$test_name" "Missing '## Observation Capture' section header"
    fi
}

# -----------------------------------------------------------------------------
# Main test execution
# -----------------------------------------------------------------------------
echo "=============================================="
echo "STORY-331 AC#1: Core File Size Compliance"
echo "=============================================="
echo "Target file: $CORE_FILE"
echo "Max lines allowed: $MAX_LINES"
echo "Required sections: 8"
echo "----------------------------------------------"
echo ""

run_test "1" test_core_file_exists
run_test "2" test_core_file_line_count
run_test "3" test_yaml_frontmatter
run_test "4" test_yaml_required_fields
run_test "5" test_purpose_section
run_test "6" test_when_invoked_section
run_test "7" test_core_workflow_section
run_test "8" test_success_criteria_section
run_test "9" test_error_handling_section
run_test "10" test_reference_loading_section
run_test "11" test_observation_capture_section

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
