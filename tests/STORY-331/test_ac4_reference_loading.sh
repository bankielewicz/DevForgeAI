#!/bin/bash
# Test AC#4: Reference Loading Pattern Implementation
# STORY-331: Refactor agent-generator.md with Progressive Disclosure
#
# Validates:
# - Core file contains "Reference Loading" section
# - Contains Read() instructions for each reference file
# - Read() calls point to correct reference directory path
# - Clear context about when each reference should be loaded
#
# Expected: FAIL initially (TDD Red phase - reference loading section not yet added)

# Note: Not using set -e due to arithmetic operations with (( ))

# Configuration
PROJECT_ROOT="/mnt/c/Projects/DevForgeAI2"
CORE_FILE="$PROJECT_ROOT/src/claude/agents/agent-generator.md"
REF_DIR="$PROJECT_ROOT/src/claude/agents/agent-generator/references"
REF_PATH_PATTERN="src/claude/agents/agent-generator/references/"

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
# Test 1: Reference Loading section exists
# -----------------------------------------------------------------------------
test_reference_loading_section() {
    local test_name="Reference Loading section exists"

    if [ ! -f "$CORE_FILE" ]; then
        fail_test "$test_name" "Core file not found: $CORE_FILE"
        return
    fi

    if grep -qE "^## Reference(s)? Loading" "$CORE_FILE"; then
        pass_test "$test_name"
    else
        fail_test "$test_name" "Missing '## Reference Loading' section header"
    fi
}

# -----------------------------------------------------------------------------
# Test 2: Read() instructions present in core file
# -----------------------------------------------------------------------------
test_read_instructions_present() {
    local test_name="Read() instructions present in core file"

    if [ ! -f "$CORE_FILE" ]; then
        fail_test "$test_name" "Core file not found"
        return
    fi

    local read_count
    read_count=$(grep -cE "Read\s*\(" "$CORE_FILE" || echo "0")

    if [ "$read_count" -gt 0 ]; then
        pass_test "$test_name (found $read_count Read() calls)"
    else
        fail_test "$test_name" "No Read() instructions found"
    fi
}

# -----------------------------------------------------------------------------
# Test 3: Read() calls point to reference directory
# -----------------------------------------------------------------------------
test_read_points_to_references() {
    local test_name="Read() calls point to reference directory"

    if [ ! -f "$CORE_FILE" ]; then
        fail_test "$test_name" "Core file not found"
        return
    fi

    local ref_reads
    # Use grep without -c to avoid regex issues with slashes, then count lines
    ref_reads=$(grep -E "Read.*agent-generator/references/" "$CORE_FILE" 2>/dev/null | wc -l)

    if [ "$ref_reads" -gt 0 ]; then
        pass_test "$test_name (found $ref_reads reference Read() calls)"
    else
        fail_test "$test_name" "No Read() calls point to $REF_PATH_PATTERN"
    fi
}

# -----------------------------------------------------------------------------
# Test 4: Each reference file has corresponding Read() call
# -----------------------------------------------------------------------------
test_read_for_each_reference() {
    local test_name="Each reference file has corresponding Read() call"

    if [ ! -f "$CORE_FILE" ]; then
        fail_test "$test_name" "Core file not found"
        return
    fi

    if [ ! -d "$REF_DIR" ]; then
        fail_test "$test_name" "Reference directory not found - cannot verify Read() coverage"
        return
    fi

    local missing_reads=""
    local ref_count=0
    local found_count=0

    while IFS= read -r file; do
        local basename
        basename=$(basename "$file")
        ((ref_count++))

        if grep -qE "Read\s*\(.*$basename" "$CORE_FILE"; then
            ((found_count++))
        else
            missing_reads="$missing_reads $basename"
        fi
    done < <(find "$REF_DIR" -maxdepth 1 -type f -name "*.md")

    if [ -z "$missing_reads" ]; then
        pass_test "$test_name ($found_count/$ref_count files covered)"
    else
        fail_test "$test_name" "Missing Read() for:$missing_reads"
    fi
}

# -----------------------------------------------------------------------------
# Test 5: Read() calls use file_path parameter
# -----------------------------------------------------------------------------
test_read_uses_file_path() {
    local test_name="Read() calls use file_path parameter"

    if [ ! -f "$CORE_FILE" ]; then
        fail_test "$test_name" "Core file not found"
        return
    fi

    local proper_format
    proper_format=$(grep -cE 'Read\s*\(\s*file_path\s*=' "$CORE_FILE" || echo "0")

    if [ "$proper_format" -gt 0 ]; then
        pass_test "$test_name (found $proper_format properly formatted calls)"
    else
        fail_test "$test_name" "Read() calls should use file_path= parameter"
    fi
}

# -----------------------------------------------------------------------------
# Test 6: Loading context documented (when to load)
# -----------------------------------------------------------------------------
test_loading_context_documented() {
    local test_name="Loading context documented (when to load each reference)"

    if [ ! -f "$CORE_FILE" ]; then
        fail_test "$test_name" "Core file not found"
        return
    fi

    # Look for context about when to load references
    if grep -qE "(when|during|before|after|if|trigger).*(load|read|reference)" "$CORE_FILE"; then
        pass_test "$test_name"
    else
        fail_test "$test_name" "No loading context (when/during/before) found for references"
    fi
}

# -----------------------------------------------------------------------------
# Test 7: Reference file descriptions present
# -----------------------------------------------------------------------------
test_reference_descriptions() {
    local test_name="Reference file descriptions present"

    if [ ! -f "$CORE_FILE" ]; then
        fail_test "$test_name" "Core file not found"
        return
    fi

    # Look for a table or list with reference file descriptions
    if grep -qE "(\|.*reference.*\||\-.*\.md.*\:|\*\*.*\.md\*\*)" "$CORE_FILE"; then
        pass_test "$test_name"
    else
        fail_test "$test_name" "No reference file descriptions found (expected table or list)"
    fi
}

# -----------------------------------------------------------------------------
# Test 8: On-demand loading pattern documented
# -----------------------------------------------------------------------------
test_on_demand_pattern() {
    local test_name="On-demand loading pattern documented"

    if [ ! -f "$CORE_FILE" ]; then
        fail_test "$test_name" "Core file not found"
        return
    fi

    if grep -qEi "(on.demand|progressive.*disclosure|load.*when.*needed|lazy.*load)" "$CORE_FILE"; then
        pass_test "$test_name"
    else
        fail_test "$test_name" "On-demand/progressive disclosure pattern not documented"
    fi
}

# -----------------------------------------------------------------------------
# Main test execution
# -----------------------------------------------------------------------------
echo "=============================================="
echo "STORY-331 AC#4: Reference Loading Pattern"
echo "=============================================="
echo "Core file: $CORE_FILE"
echo "Reference path pattern: $REF_PATH_PATTERN"
echo "----------------------------------------------"
echo ""

run_test "1" test_reference_loading_section
run_test "2" test_read_instructions_present
run_test "3" test_read_points_to_references
run_test "4" test_read_for_each_reference
run_test "5" test_read_uses_file_path
run_test "6" test_loading_context_documented
run_test "7" test_reference_descriptions
run_test "8" test_on_demand_pattern

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
