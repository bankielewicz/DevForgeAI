#!/bin/bash
# Test AC#2: Phase 02 (Red) Includes Treelint Context in test-automator Invocation
# STORY-377: Update devforgeai-development Skill for Treelint
#
# Validates:
# - tdd-red-phase.md Task(subagent_type="test-automator") prompt contains Treelint context note
# - Note mentions "Treelint-enabled" (or "Treelint" capability)
# - Note mentions "fallback" (Grep fallback when Treelint unavailable)
# - Treelint context note is under 800 characters
#
# Expected: FAIL initially (TDD Red phase - tdd-red-phase.md has no Treelint context)

# Configuration
PROJECT_ROOT="/mnt/c/Projects/DevForgeAI2"
RED_PHASE_FILE="$PROJECT_ROOT/src/claude/skills/devforgeai-development/references/tdd-red-phase.md"
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
# Test 1: tdd-red-phase.md file exists
# -----------------------------------------------------------------------------
test_file_exists() {
    local test_name="tdd-red-phase.md file exists"
    if [ -f "$RED_PHASE_FILE" ]; then
        pass_test "$test_name"
    else
        fail_test "$test_name" "File not found: $RED_PHASE_FILE"
    fi
}

# -----------------------------------------------------------------------------
# Test 2: File contains test-automator Task invocation
# -----------------------------------------------------------------------------
test_has_test_automator_task() {
    local test_name="File contains test-automator Task invocation"

    if [ ! -f "$RED_PHASE_FILE" ]; then
        fail_test "$test_name" "Cannot check - file does not exist"
        return
    fi

    if grep -q 'subagent_type="test-automator"' "$RED_PHASE_FILE"; then
        pass_test "$test_name"
    else
        fail_test "$test_name" "No test-automator Task invocation found"
    fi
}

# -----------------------------------------------------------------------------
# Test 3: test-automator prompt contains Treelint keyword
# -----------------------------------------------------------------------------
test_prompt_contains_treelint() {
    local test_name="test-automator prompt contains Treelint keyword"

    if [ ! -f "$RED_PHASE_FILE" ]; then
        fail_test "$test_name" "Cannot check - file does not exist"
        return
    fi

    # Extract the Task block for test-automator (from Task( to closing ))
    # Search for Treelint within the test-automator prompt context
    local task_content
    task_content=$(sed -n '/subagent_type="test-automator"/,/^)$/p' "$RED_PHASE_FILE")

    if echo "$task_content" | grep -qi "treelint"; then
        pass_test "$test_name"
    else
        fail_test "$test_name" "No Treelint keyword in test-automator Task prompt"
    fi
}

# -----------------------------------------------------------------------------
# Test 4: Prompt mentions "Treelint-enabled" capability
# -----------------------------------------------------------------------------
test_mentions_treelint_enabled() {
    local test_name="Prompt mentions Treelint-enabled capability"

    if [ ! -f "$RED_PHASE_FILE" ]; then
        fail_test "$test_name" "Cannot check - file does not exist"
        return
    fi

    # Check broadly in the file since the Treelint context note may appear
    # near but not inside the Task() block
    if grep -qi "treelint-enabled\|treelint.enabled\|Treelint.*enabled" "$RED_PHASE_FILE"; then
        pass_test "$test_name"
    else
        fail_test "$test_name" "No mention of Treelint-enabled in tdd-red-phase.md"
    fi
}

# -----------------------------------------------------------------------------
# Test 5: Prompt mentions "fallback" for Grep
# -----------------------------------------------------------------------------
test_mentions_fallback() {
    local test_name="Prompt mentions fallback for Grep"

    if [ ! -f "$RED_PHASE_FILE" ]; then
        fail_test "$test_name" "Cannot check - file does not exist"
        return
    fi

    # Look for fallback mention in the Treelint context area
    if grep -qi "fallback" "$RED_PHASE_FILE"; then
        # Verify it is in context of Treelint (not unrelated fallback references)
        local treelint_area
        treelint_area=$(grep -i -A5 -B2 "treelint" "$RED_PHASE_FILE" 2>/dev/null)

        if echo "$treelint_area" | grep -qi "fallback"; then
            pass_test "$test_name"
        else
            fail_test "$test_name" "fallback keyword exists but not in Treelint context"
        fi
    else
        fail_test "$test_name" "No 'fallback' keyword found in tdd-red-phase.md Treelint context"
    fi
}

# -----------------------------------------------------------------------------
# Test 6: Treelint context note under 800 characters
# -----------------------------------------------------------------------------
test_note_size_limit() {
    local test_name="Treelint context note under $MAX_NOTE_CHARS characters"

    if [ ! -f "$RED_PHASE_FILE" ]; then
        fail_test "$test_name" "Cannot check - file does not exist"
        return
    fi

    # Extract Treelint-related content (lines mentioning Treelint and surrounding context)
    # Look for a contiguous Treelint context block
    local treelint_block
    treelint_block=$(sed -n '/[Tt]reelint/,/^$/p' "$RED_PHASE_FILE" | head -20)

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
# Test 7: Existing test-automator invocation preserved (no regression)
# -----------------------------------------------------------------------------
test_existing_invocation_preserved() {
    local test_name="Existing test-automator invocation structure preserved"

    if [ ! -f "$RED_PHASE_FILE" ]; then
        fail_test "$test_name" "Cannot check - file does not exist"
        return
    fi

    # Verify key elements of the existing test-automator Task are still present
    local has_description has_prompt has_ac_reference
    has_description=$(grep -c 'description="Generate failing tests' "$RED_PHASE_FILE")
    has_prompt=$(grep -c 'acceptance criteria' "$RED_PHASE_FILE")
    has_ac_reference=$(grep -c 'source-tree.md' "$RED_PHASE_FILE")

    if [ "$has_description" -ge 1 ] && [ "$has_prompt" -ge 1 ] && [ "$has_ac_reference" -ge 1 ]; then
        pass_test "$test_name"
    else
        fail_test "$test_name" "Original test-automator Task structure appears modified"
    fi
}

# -----------------------------------------------------------------------------
# Main test execution
# -----------------------------------------------------------------------------
echo "=============================================="
echo "STORY-377 AC#2: Phase 02 Red Phase Treelint"
echo "=============================================="
echo "Target file: $RED_PHASE_FILE"
echo "----------------------------------------------"
echo ""

run_test "1" test_file_exists
run_test "2" test_has_test_automator_task
run_test "3" test_prompt_contains_treelint
run_test "4" test_mentions_treelint_enabled
run_test "5" test_mentions_fallback
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
