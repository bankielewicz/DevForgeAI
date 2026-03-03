#!/bin/bash
# Test AC#5: Observation Capture Section (EPIC-052 Compliance)
# STORY-331: Refactor agent-generator.md with Progressive Disclosure
#
# Validates:
# - Core file contains "Observation Capture" section
# - 7 categories present: friction, success, pattern, gap, idea, bug, warning
# - Severity levels documented: low, medium, high
# - Files array documented (optional field)
# - Marked as OPTIONAL for backward compatibility
#
# Expected: FAIL initially (TDD Red phase - observation capture section not yet added)

# Note: Not using set -e due to arithmetic operations with (( ))

# Configuration
PROJECT_ROOT="/mnt/c/Projects/DevForgeAI2"
CORE_FILE="$PROJECT_ROOT/src/claude/agents/agent-generator.md"

# EPIC-052 observation categories
REQUIRED_CATEGORIES=("friction" "success" "pattern" "gap" "idea" "bug" "warning")
SEVERITY_LEVELS=("low" "medium" "high")

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
# Test 1: Observation Capture section exists
# -----------------------------------------------------------------------------
test_observation_section_exists() {
    local test_name="Observation Capture section exists"

    if [ ! -f "$CORE_FILE" ]; then
        fail_test "$test_name" "Core file not found: $CORE_FILE"
        return
    fi

    if grep -qE "^## Observation Capture" "$CORE_FILE"; then
        pass_test "$test_name"
    else
        fail_test "$test_name" "Missing '## Observation Capture' section header"
    fi
}

# -----------------------------------------------------------------------------
# Test 2: Friction category documented
# -----------------------------------------------------------------------------
test_friction_category() {
    local test_name="Friction category documented"

    if [ ! -f "$CORE_FILE" ]; then
        fail_test "$test_name" "Core file not found"
        return
    fi

    if grep -qi "friction" "$CORE_FILE"; then
        pass_test "$test_name"
    else
        fail_test "$test_name" "Category 'friction' not found"
    fi
}

# -----------------------------------------------------------------------------
# Test 3: Success category documented
# -----------------------------------------------------------------------------
test_success_category() {
    local test_name="Success category documented"

    if [ ! -f "$CORE_FILE" ]; then
        fail_test "$test_name" "Core file not found"
        return
    fi

    if grep -qi "success" "$CORE_FILE"; then
        pass_test "$test_name"
    else
        fail_test "$test_name" "Category 'success' not found"
    fi
}

# -----------------------------------------------------------------------------
# Test 4: Pattern category documented
# -----------------------------------------------------------------------------
test_pattern_category() {
    local test_name="Pattern category documented"

    if [ ! -f "$CORE_FILE" ]; then
        fail_test "$test_name" "Core file not found"
        return
    fi

    if grep -qi "pattern" "$CORE_FILE"; then
        pass_test "$test_name"
    else
        fail_test "$test_name" "Category 'pattern' not found"
    fi
}

# -----------------------------------------------------------------------------
# Test 5: Gap category documented
# -----------------------------------------------------------------------------
test_gap_category() {
    local test_name="Gap category documented"

    if [ ! -f "$CORE_FILE" ]; then
        fail_test "$test_name" "Core file not found"
        return
    fi

    if grep -qi "gap" "$CORE_FILE"; then
        pass_test "$test_name"
    else
        fail_test "$test_name" "Category 'gap' not found"
    fi
}

# -----------------------------------------------------------------------------
# Test 6: Idea category documented
# -----------------------------------------------------------------------------
test_idea_category() {
    local test_name="Idea category documented"

    if [ ! -f "$CORE_FILE" ]; then
        fail_test "$test_name" "Core file not found"
        return
    fi

    if grep -qi "idea" "$CORE_FILE"; then
        pass_test "$test_name"
    else
        fail_test "$test_name" "Category 'idea' not found"
    fi
}

# -----------------------------------------------------------------------------
# Test 7: Bug category documented
# -----------------------------------------------------------------------------
test_bug_category() {
    local test_name="Bug category documented"

    if [ ! -f "$CORE_FILE" ]; then
        fail_test "$test_name" "Core file not found"
        return
    fi

    if grep -qi "bug" "$CORE_FILE"; then
        pass_test "$test_name"
    else
        fail_test "$test_name" "Category 'bug' not found"
    fi
}

# -----------------------------------------------------------------------------
# Test 8: Warning category documented
# -----------------------------------------------------------------------------
test_warning_category() {
    local test_name="Warning category documented"

    if [ ! -f "$CORE_FILE" ]; then
        fail_test "$test_name" "Core file not found"
        return
    fi

    if grep -qi "warning" "$CORE_FILE"; then
        pass_test "$test_name"
    else
        fail_test "$test_name" "Category 'warning' not found"
    fi
}

# -----------------------------------------------------------------------------
# Test 9: All 7 categories in observation section context
# -----------------------------------------------------------------------------
test_all_categories_in_observation() {
    local test_name="All 7 categories in observation section context"

    if [ ! -f "$CORE_FILE" ]; then
        fail_test "$test_name" "Core file not found"
        return
    fi

    # Extract observation capture section (from ## Observation Capture to next ##)
    local obs_section
    obs_section=$(sed -n '/^## Observation Capture/,/^## /p' "$CORE_FILE" | head -n -1)

    if [ -z "$obs_section" ]; then
        fail_test "$test_name" "Could not extract Observation Capture section"
        return
    fi

    local missing=""
    for cat in "${REQUIRED_CATEGORIES[@]}"; do
        if ! echo "$obs_section" | grep -qi "$cat"; then
            missing="$missing $cat"
        fi
    done

    if [ -z "$missing" ]; then
        pass_test "$test_name"
    else
        fail_test "$test_name" "Missing categories in section:$missing"
    fi
}

# -----------------------------------------------------------------------------
# Test 10: Severity levels documented
# -----------------------------------------------------------------------------
test_severity_levels() {
    local test_name="Severity levels documented (low, medium, high)"

    if [ ! -f "$CORE_FILE" ]; then
        fail_test "$test_name" "Core file not found"
        return
    fi

    local missing=""
    for level in "${SEVERITY_LEVELS[@]}"; do
        if ! grep -qi "$level" "$CORE_FILE"; then
            missing="$missing $level"
        fi
    done

    if [ -z "$missing" ]; then
        pass_test "$test_name"
    else
        fail_test "$test_name" "Missing severity levels:$missing"
    fi
}

# -----------------------------------------------------------------------------
# Test 11: Files array documented
# -----------------------------------------------------------------------------
test_files_array() {
    local test_name="Files array documented"

    if [ ! -f "$CORE_FILE" ]; then
        fail_test "$test_name" "Core file not found"
        return
    fi

    if grep -qiE "(files.*array|files.*\[\]|\"files\":)" "$CORE_FILE"; then
        pass_test "$test_name"
    else
        fail_test "$test_name" "Files array field not documented"
    fi
}

# -----------------------------------------------------------------------------
# Test 12: OPTIONAL marker present
# -----------------------------------------------------------------------------
test_optional_marker() {
    local test_name="OPTIONAL marker present for backward compatibility"

    if [ ! -f "$CORE_FILE" ]; then
        fail_test "$test_name" "Core file not found"
        return
    fi

    if grep -qiE "(OPTIONAL|optional|backward.*compat)" "$CORE_FILE"; then
        pass_test "$test_name"
    else
        fail_test "$test_name" "OPTIONAL marker not found (needed for backward compatibility)"
    fi
}

# -----------------------------------------------------------------------------
# Test 13: Observation JSON schema example present
# -----------------------------------------------------------------------------
test_observation_schema() {
    local test_name="Observation JSON/YAML schema example present"

    if [ ! -f "$CORE_FILE" ]; then
        fail_test "$test_name" "Core file not found"
        return
    fi

    if grep -qE "(observations:|\"observations\":|category.*note.*severity)" "$CORE_FILE"; then
        pass_test "$test_name"
    else
        fail_test "$test_name" "No observation schema example found"
    fi
}

# -----------------------------------------------------------------------------
# Main test execution
# -----------------------------------------------------------------------------
echo "=============================================="
echo "STORY-331 AC#5: Observation Capture Section"
echo "=============================================="
echo "Core file: $CORE_FILE"
echo "Required categories: ${REQUIRED_CATEGORIES[*]}"
echo "Severity levels: ${SEVERITY_LEVELS[*]}"
echo "----------------------------------------------"
echo ""

run_test "1" test_observation_section_exists
run_test "2" test_friction_category
run_test "3" test_success_category
run_test "4" test_pattern_category
run_test "5" test_gap_category
run_test "6" test_idea_category
run_test "7" test_bug_category
run_test "8" test_warning_category
run_test "9" test_all_categories_in_observation
run_test "10" test_severity_levels
run_test "11" test_files_array
run_test "12" test_optional_marker
run_test "13" test_observation_schema

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
