#!/bin/bash
# Test AC#3: Phase 03 (Green) Includes Treelint Context in backend-architect Invocation
# STORY-377: Update devforgeai-development Skill for Treelint
#
# Validates:
# - tdd-green-phase.md Task(subagent_type=IMPLEMENTATION_AGENT) prompt contains Treelint context
#   when IMPLEMENTATION_AGENT is backend-architect
# - frontend-developer prompt does NOT contain Treelint keywords
# - Treelint context note is under 800 characters
# - Existing backend-architect invocation structure is preserved
#
# Expected: FAIL initially (TDD Red phase - tdd-green-phase.md has no Treelint context)

# Configuration
PROJECT_ROOT="/mnt/c/Projects/DevForgeAI2"
GREEN_PHASE_FILE="$PROJECT_ROOT/src/claude/skills/devforgeai-development/references/tdd-green-phase.md"
MAX_NOTE_CHARS=800

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
# Test 1: tdd-green-phase.md file exists
# -----------------------------------------------------------------------------
test_file_exists() {
    local test_name="tdd-green-phase.md file exists"
    if [ -f "$GREEN_PHASE_FILE" ]; then
        pass_test "$test_name"
    else
        fail_test "$test_name" "File not found: $GREEN_PHASE_FILE"
    fi
}

# -----------------------------------------------------------------------------
# Test 2: File contains IMPLEMENTATION_AGENT Task invocation
# -----------------------------------------------------------------------------
test_has_implementation_agent_task() {
    local test_name="File contains IMPLEMENTATION_AGENT Task invocation"

    if [ ! -f "$GREEN_PHASE_FILE" ]; then
        fail_test "$test_name" "Cannot check - file does not exist"
        return
    fi

    if grep -q 'subagent_type=IMPLEMENTATION_AGENT' "$GREEN_PHASE_FILE"; then
        pass_test "$test_name"
    else
        fail_test "$test_name" "No IMPLEMENTATION_AGENT Task invocation found"
    fi
}

# -----------------------------------------------------------------------------
# Test 3: File contains Treelint keyword in backend-architect context
# -----------------------------------------------------------------------------
test_contains_treelint_for_backend() {
    local test_name="File contains Treelint keyword in backend-architect context"

    if [ ! -f "$GREEN_PHASE_FILE" ]; then
        fail_test "$test_name" "Cannot check - file does not exist"
        return
    fi

    # The Treelint context should appear conditionally for backend-architect
    if grep -qi "treelint" "$GREEN_PHASE_FILE"; then
        pass_test "$test_name"
    else
        fail_test "$test_name" "No Treelint keyword found in tdd-green-phase.md"
    fi
}

# -----------------------------------------------------------------------------
# Test 4: Treelint context is conditional on backend-architect
# -----------------------------------------------------------------------------
test_treelint_conditional_on_backend() {
    local test_name="Treelint context is conditional on backend-architect"

    if [ ! -f "$GREEN_PHASE_FILE" ]; then
        fail_test "$test_name" "Cannot check - file does not exist"
        return
    fi

    # The file should show Treelint context tied to backend-architect selection
    # Look for conditional logic mentioning backend-architect and Treelint together
    local has_conditional
    has_conditional=$(grep -i -c "backend-architect" "$GREEN_PHASE_FILE")

    local has_treelint_near_backend
    has_treelint_near_backend=$(grep -i -A10 -B2 "backend-architect" "$GREEN_PHASE_FILE" | grep -ci "treelint")

    if [ "$has_treelint_near_backend" -ge 1 ]; then
        pass_test "$test_name"
    else
        fail_test "$test_name" "Treelint not found conditionally tied to backend-architect"
    fi
}

# -----------------------------------------------------------------------------
# Test 5: frontend-developer prompt does NOT contain Treelint keywords
# -----------------------------------------------------------------------------
test_frontend_no_treelint() {
    local test_name="frontend-developer prompt does NOT contain Treelint keywords"

    if [ ! -f "$GREEN_PHASE_FILE" ]; then
        fail_test "$test_name" "Cannot check - file does not exist"
        return
    fi

    # Extract content near frontend-developer references
    local frontend_context
    frontend_context=$(grep -i -A10 -B2 "frontend-developer" "$GREEN_PHASE_FILE" 2>/dev/null)

    if [ -z "$frontend_context" ]; then
        # No frontend-developer reference at all is acceptable (may not be modified)
        pass_test "$test_name (no frontend-developer reference found)"
        return
    fi

    # Check that Treelint is NOT mentioned in frontend-developer context
    if echo "$frontend_context" | grep -qi "treelint"; then
        fail_test "$test_name" "Treelint keyword found in frontend-developer context (should be backend-only)"
    else
        pass_test "$test_name"
    fi
}

# -----------------------------------------------------------------------------
# Test 6: Treelint context note under 800 characters
# -----------------------------------------------------------------------------
test_note_size_limit() {
    local test_name="Treelint context note under $MAX_NOTE_CHARS characters"

    if [ ! -f "$GREEN_PHASE_FILE" ]; then
        fail_test "$test_name" "Cannot check - file does not exist"
        return
    fi

    local treelint_block
    treelint_block=$(sed -n '/[Tt]reelint/,/^$/p' "$GREEN_PHASE_FILE" | head -20)

    if [ -z "$treelint_block" ]; then
        fail_test "$test_name" "No Treelint content found to measure"
        return
    fi

    local char_count
    char_count=$(echo "$treelint_block" | wc -c)

    if [ "$char_count" -le "$MAX_NOTE_CHARS" ]; then
        pass_test "$test_name (actual: $char_count chars)"
    else
        fail_test "$test_name" "Treelint note has $char_count characters (max: $MAX_NOTE_CHARS)"
    fi
}

# -----------------------------------------------------------------------------
# Test 7: Existing implementation invocation structure preserved
# -----------------------------------------------------------------------------
test_existing_invocation_preserved() {
    local test_name="Existing implementation invocation structure preserved"

    if [ ! -f "$GREEN_PHASE_FILE" ]; then
        fail_test "$test_name" "Cannot check - file does not exist"
        return
    fi

    # Verify key elements of the existing Task are still present
    local has_description has_context has_test_cmd
    has_description=$(grep -c 'Implement.*code.*pass.*tests\|Implement minimal code' "$GREEN_PHASE_FILE")
    has_context=$(grep -c 'tech-stack.md' "$GREEN_PHASE_FILE")
    has_test_cmd=$(grep -c 'TEST_COMMAND' "$GREEN_PHASE_FILE")

    if [ "$has_description" -ge 1 ] && [ "$has_context" -ge 1 ] && [ "$has_test_cmd" -ge 1 ]; then
        pass_test "$test_name"
    else
        fail_test "$test_name" "Original implementation Task structure appears modified (desc=$has_description, ctx=$has_context, cmd=$has_test_cmd)"
    fi
}

# -----------------------------------------------------------------------------
# Main test execution
# -----------------------------------------------------------------------------
echo "=============================================="
echo "STORY-377 AC#3: Phase 03 Green Phase Treelint"
echo "=============================================="
echo "Target file: $GREEN_PHASE_FILE"
echo "----------------------------------------------"
echo ""

run_test "1" test_file_exists
run_test "2" test_has_implementation_agent_task
run_test "3" test_contains_treelint_for_backend
run_test "4" test_treelint_conditional_on_backend
run_test "5" test_frontend_no_treelint
run_test "6" test_note_size_limit
run_test "7" test_existing_invocation_preserved

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
