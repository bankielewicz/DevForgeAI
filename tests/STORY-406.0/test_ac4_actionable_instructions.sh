#!/bin/bash
# Test AC#4: Template is actionable for a new batch
# STORY-406: Create Batch Sibling Story Session Template
#
# Validates:
# - Template contains concrete numbered instructions (e.g., "1.", "2.", "3.")
# - Template is not vague guidance (checks for imperative verbs)
# - No Treelint-specific terms in sections 1-4 (domain-agnostic)
#
# Expected: FAIL initially (TDD Red phase - file does not exist yet)

# Configuration
PROJECT_ROOT="/mnt/c/Projects/DevForgeAI2"
TARGET_FILE="$PROJECT_ROOT/src/claude/memory/batch-sibling-story-session-template.md"

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
# Test 1: Contains numbered instructions
# -----------------------------------------------------------------------------
test_numbered_instructions() {
    local test_name="Contains numbered instructions"
    if [ ! -f "$TARGET_FILE" ]; then
        fail_test "$test_name" "Cannot check - file does not exist"
        return
    fi

    # Count lines starting with a number followed by period (e.g., "1.", "2.")
    local numbered_count
    numbered_count=$(grep -cE '^\s*[0-9]+\.' "$TARGET_FILE")
    if [ "$numbered_count" -ge 5 ]; then
        pass_test "$test_name ($numbered_count numbered steps found)"
    else
        fail_test "$test_name" "Expected at least 5 numbered steps, found $numbered_count"
    fi
}

# -----------------------------------------------------------------------------
# Test 2: Contains imperative verbs (actionable language)
# -----------------------------------------------------------------------------
test_imperative_verbs() {
    local test_name="Contains imperative verbs (actionable language)"
    if [ ! -f "$TARGET_FILE" ]; then
        fail_test "$test_name" "Cannot check - file does not exist"
        return
    fi

    # Look for common imperative verbs at start of lines or after numbers
    local imperative_count
    imperative_count=$(grep -ciE '^\s*[0-9]*\.?\s*(Read|Load|Identify|Check|Run|Create|Update|Capture|Record|Extract|Verify|Document|List|Open|Compare|Note|Set|Write|Use|Apply|Review|Scan|Search|Execute)' "$TARGET_FILE")
    if [ "$imperative_count" -ge 3 ]; then
        pass_test "$test_name ($imperative_count imperative lines found)"
    else
        fail_test "$test_name" "Expected at least 3 imperative verb lines, found $imperative_count"
    fi
}

# -----------------------------------------------------------------------------
# Test 3: No Treelint references in sections 1-4 (domain-agnostic)
# -----------------------------------------------------------------------------
test_domain_agnostic_sections() {
    local test_name="Sections 1-4 are domain-agnostic (no Treelint references)"
    if [ ! -f "$TARGET_FILE" ]; then
        fail_test "$test_name" "Cannot check - file does not exist"
        return
    fi

    # Find the line number of the "Proof of Concept" section
    local poc_line
    poc_line=$(grep -niE '^## .*Proof of Concept' "$TARGET_FILE" | head -1 | cut -d: -f1)

    if [ -z "$poc_line" ]; then
        fail_test "$test_name" "Cannot determine section boundaries - 'Proof of Concept' heading not found"
        return
    fi

    # Extract content before Proof of Concept section and check for Treelint
    local treelint_in_sections_1_4
    treelint_in_sections_1_4=$(head -n "$((poc_line - 1))" "$TARGET_FILE" | grep -ci 'treelint')

    if [ "$treelint_in_sections_1_4" -eq 0 ]; then
        pass_test "$test_name"
    else
        fail_test "$test_name" "Found $treelint_in_sections_1_4 'Treelint' references before Proof of Concept section"
    fi
}

# -----------------------------------------------------------------------------
# Test 4: Contains bullet lists
# -----------------------------------------------------------------------------
test_bullet_lists() {
    local test_name="Contains bullet lists"
    if [ ! -f "$TARGET_FILE" ]; then
        fail_test "$test_name" "Cannot check - file does not exist"
        return
    fi

    local bullet_count
    bullet_count=$(grep -cE '^\s*[-*] ' "$TARGET_FILE")
    if [ "$bullet_count" -ge 5 ]; then
        pass_test "$test_name ($bullet_count bullet items found)"
    else
        fail_test "$test_name" "Expected at least 5 bullet list items, found $bullet_count"
    fi
}

# -----------------------------------------------------------------------------
# Main test execution
# -----------------------------------------------------------------------------
echo "=============================================="
echo "STORY-406 AC#4: Actionable Instructions"
echo "=============================================="
echo "Target file: $TARGET_FILE"
echo "----------------------------------------------"
echo ""

run_test "1" test_numbered_instructions
run_test "2" test_imperative_verbs
run_test "3" test_domain_agnostic_sections
run_test "4" test_bullet_lists

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
