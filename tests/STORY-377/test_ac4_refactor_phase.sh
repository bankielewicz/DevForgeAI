#!/bin/bash
# Test AC#4: Phase 04 (Refactor) Includes Treelint Context in Both Subagent Invocations
# STORY-377: Update devforgeai-development Skill for Treelint
#
# Validates:
# - tdd-refactor-phase.md Task(subagent_type="refactoring-specialist") prompt contains Treelint context
# - tdd-refactor-phase.md Task(subagent_type="code-reviewer") prompt contains Treelint context
# - Each Treelint context note is under 800 characters
# - Existing refactoring and review invocation structures are preserved
#
# Expected: FAIL initially (TDD Red phase - tdd-refactor-phase.md has no Treelint context)

# Configuration
PROJECT_ROOT="/mnt/c/Projects/DevForgeAI2"
REFACTOR_PHASE_FILE="$PROJECT_ROOT/src/claude/skills/devforgeai-development/references/tdd-refactor-phase.md"
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
# Test 1: tdd-refactor-phase.md file exists
# -----------------------------------------------------------------------------
test_file_exists() {
    local test_name="tdd-refactor-phase.md file exists"
    if [ -f "$REFACTOR_PHASE_FILE" ]; then
        pass_test "$test_name"
    else
        fail_test "$test_name" "File not found: $REFACTOR_PHASE_FILE"
    fi
}

# -----------------------------------------------------------------------------
# Test 2: File contains refactoring-specialist Task invocation
# -----------------------------------------------------------------------------
test_has_refactoring_specialist_task() {
    local test_name="File contains refactoring-specialist Task invocation"

    if [ ! -f "$REFACTOR_PHASE_FILE" ]; then
        fail_test "$test_name" "Cannot check - file does not exist"
        return
    fi

    if grep -q 'subagent_type="refactoring-specialist"' "$REFACTOR_PHASE_FILE"; then
        pass_test "$test_name"
    else
        fail_test "$test_name" "No refactoring-specialist Task invocation found"
    fi
}

# -----------------------------------------------------------------------------
# Test 3: File contains code-reviewer Task invocation
# -----------------------------------------------------------------------------
test_has_code_reviewer_task() {
    local test_name="File contains code-reviewer Task invocation"

    if [ ! -f "$REFACTOR_PHASE_FILE" ]; then
        fail_test "$test_name" "Cannot check - file does not exist"
        return
    fi

    if grep -q 'subagent_type="code-reviewer"' "$REFACTOR_PHASE_FILE"; then
        pass_test "$test_name"
    else
        fail_test "$test_name" "No code-reviewer Task invocation found"
    fi
}

# -----------------------------------------------------------------------------
# Test 4: Treelint keyword present in refactoring-specialist context
# -----------------------------------------------------------------------------
test_treelint_in_refactoring_specialist() {
    local test_name="Treelint context in refactoring-specialist prompt"

    if [ ! -f "$REFACTOR_PHASE_FILE" ]; then
        fail_test "$test_name" "Cannot check - file does not exist"
        return
    fi

    # Extract the refactoring-specialist Task block and check for Treelint
    local refactoring_block
    refactoring_block=$(sed -n '/subagent_type="refactoring-specialist"/,/^)$/p' "$REFACTOR_PHASE_FILE")

    if echo "$refactoring_block" | grep -qi "treelint"; then
        pass_test "$test_name"
    else
        fail_test "$test_name" "No Treelint keyword in refactoring-specialist Task prompt"
    fi
}

# -----------------------------------------------------------------------------
# Test 5: Treelint keyword present in code-reviewer context
# -----------------------------------------------------------------------------
test_treelint_in_code_reviewer() {
    local test_name="Treelint context in code-reviewer prompt"

    if [ ! -f "$REFACTOR_PHASE_FILE" ]; then
        fail_test "$test_name" "Cannot check - file does not exist"
        return
    fi

    # Extract the code-reviewer Task block and check for Treelint
    local reviewer_block
    reviewer_block=$(sed -n '/subagent_type="code-reviewer"/,/^)$/p' "$REFACTOR_PHASE_FILE")

    if echo "$reviewer_block" | grep -qi "treelint"; then
        pass_test "$test_name"
    else
        fail_test "$test_name" "No Treelint keyword in code-reviewer Task prompt"
    fi
}

# -----------------------------------------------------------------------------
# Test 6: Treelint note in refactoring-specialist under 800 chars
# -----------------------------------------------------------------------------
test_refactoring_note_size() {
    local test_name="Refactoring-specialist Treelint note under $MAX_NOTE_CHARS characters"

    if [ ! -f "$REFACTOR_PHASE_FILE" ]; then
        fail_test "$test_name" "Cannot check - file does not exist"
        return
    fi

    # Extract Treelint content near refactoring-specialist
    local treelint_block
    treelint_block=$(sed -n '/subagent_type="refactoring-specialist"/,/^)$/p' "$REFACTOR_PHASE_FILE" | grep -i -A5 "treelint")

    if [ -z "$treelint_block" ]; then
        fail_test "$test_name" "No Treelint content found in refactoring-specialist block"
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
# Test 7: Treelint note in code-reviewer under 800 chars
# -----------------------------------------------------------------------------
test_reviewer_note_size() {
    local test_name="Code-reviewer Treelint note under $MAX_NOTE_CHARS characters"

    if [ ! -f "$REFACTOR_PHASE_FILE" ]; then
        fail_test "$test_name" "Cannot check - file does not exist"
        return
    fi

    # Extract Treelint content near code-reviewer
    local treelint_block
    treelint_block=$(sed -n '/subagent_type="code-reviewer"/,/^)$/p' "$REFACTOR_PHASE_FILE" | grep -i -A5 "treelint")

    if [ -z "$treelint_block" ]; then
        fail_test "$test_name" "No Treelint content found in code-reviewer block"
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
# Test 8: Existing refactoring-specialist invocation preserved
# -----------------------------------------------------------------------------
test_refactoring_invocation_preserved() {
    local test_name="Existing refactoring-specialist invocation preserved"

    if [ ! -f "$REFACTOR_PHASE_FILE" ]; then
        fail_test "$test_name" "Cannot check - file does not exist"
        return
    fi

    local has_description has_anti_patterns has_test_cmd
    has_description=$(grep -c 'Refactor.*code.*keeping.*tests\|Refactor the implementation' "$REFACTOR_PHASE_FILE")
    has_anti_patterns=$(grep -c 'anti-patterns' "$REFACTOR_PHASE_FILE")
    has_test_cmd=$(grep -c 'TEST_COMMAND' "$REFACTOR_PHASE_FILE")

    if [ "$has_description" -ge 1 ] && [ "$has_anti_patterns" -ge 1 ] && [ "$has_test_cmd" -ge 1 ]; then
        pass_test "$test_name"
    else
        fail_test "$test_name" "Original refactoring-specialist Task structure appears modified"
    fi
}

# -----------------------------------------------------------------------------
# Test 9: Existing code-reviewer invocation preserved
# -----------------------------------------------------------------------------
test_reviewer_invocation_preserved() {
    local test_name="Existing code-reviewer invocation preserved"

    if [ ! -f "$REFACTOR_PHASE_FILE" ]; then
        fail_test "$test_name" "Cannot check - file does not exist"
        return
    fi

    local has_review has_security has_priority
    has_review=$(grep -c 'code review\|code-reviewer' "$REFACTOR_PHASE_FILE")
    has_security=$(grep -c 'Security\|security' "$REFACTOR_PHASE_FILE")
    has_priority=$(grep -c 'CRITICAL\|HIGH\|MEDIUM\|LOW' "$REFACTOR_PHASE_FILE")

    if [ "$has_review" -ge 1 ] && [ "$has_security" -ge 1 ] && [ "$has_priority" -ge 1 ]; then
        pass_test "$test_name"
    else
        fail_test "$test_name" "Original code-reviewer Task structure appears modified"
    fi
}

# -----------------------------------------------------------------------------
# Main test execution
# -----------------------------------------------------------------------------
echo "=============================================="
echo "STORY-377 AC#4: Phase 04 Refactor Treelint"
echo "=============================================="
echo "Target file: $REFACTOR_PHASE_FILE"
echo "----------------------------------------------"
echo ""

run_test "1" test_file_exists
run_test "2" test_has_refactoring_specialist_task
run_test "3" test_has_code_reviewer_task
run_test "4" test_treelint_in_refactoring_specialist
run_test "5" test_treelint_in_code_reviewer
run_test "6" test_refactoring_note_size
run_test "7" test_reviewer_note_size
run_test "8" test_refactoring_invocation_preserved
run_test "9" test_reviewer_invocation_preserved

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
