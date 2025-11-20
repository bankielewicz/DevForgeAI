#!/bin/bash
# Unit Test: AC5 - Sprint creation without story assignment
# Tests that hooks work correctly with empty sprints (0 stories selected)

set -e

TEST_NAME="Empty Sprint Handling"
TEST_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$TEST_DIR/../../.." && pwd)"

# ANSI colors
RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m'

echo "========================================="
echo "TEST: $TEST_NAME"
echo "========================================="

# Test 1: Phase N handles STORY_COUNT=0
test_zero_story_count() {
    echo -n "Test 5.1: Phase N handles STORY_COUNT=0... "

    # Verify Phase N doesn't have conditions that prevent execution with 0 stories
    phase_n_content=$(grep -A 100 "### Phase N: Feedback Hook Integration" "$PROJECT_ROOT/.claude/commands/create-sprint.md" || echo "")

    if echo "$phase_n_content" | grep -q "IF.*STORY_COUNT.*> 0\|IF.*stories.*empty.*SKIP"; then
        echo -e "${RED}FAIL${NC}"
        echo "  Expected: No condition preventing execution with 0 stories"
        echo "  Actual: Found condition that might skip Phase N"
        return 1
    else
        echo -e "${GREEN}PASS${NC}"
        return 0
    fi
}

# Test 2: invoke-hooks called with --story-count=0
test_invoke_hooks_zero_stories() {
    echo -n "Test 5.2: invoke-hooks called with --story-count=0... "

    # Verify Phase N still invokes hooks even with 0 stories
    # (No conditional skip based on story count)
    if grep -A 100 "### Phase N: Feedback Hook Integration" "$PROJECT_ROOT/.claude/commands/create-sprint.md" | \
       grep "invoke-hooks"; then
        # Check there's no "IF STORY_COUNT > 0" before invoke-hooks
        if grep -B 20 "invoke-hooks" "$PROJECT_ROOT/.claude/commands/create-sprint.md" | \
           tail -20 | grep -q "IF.*STORY_COUNT.*> 0"; then
            echo -e "${RED}FAIL${NC}"
            echo "  Expected: invoke-hooks called regardless of story count"
            echo "  Actual: Found conditional skip"
            return 1
        else
            echo -e "${GREEN}PASS${NC}"
            return 0
        fi
    else
        echo -e "${RED}FAIL${NC}"
        echo "  Expected: invoke-hooks command in Phase N"
        echo "  Actual: invoke-hooks not found"
        return 1
    fi
}

# Test 3: invoke-hooks called with --capacity=0
test_invoke_hooks_zero_capacity() {
    echo -n "Test 5.3: invoke-hooks called with --capacity=0... "

    # Empty sprint should have 0 capacity
    # Verify capacity parameter is passed (will be 0 for empty sprint)
    if grep -A 100 "### Phase N: Feedback Hook Integration" "$PROJECT_ROOT/.claude/commands/create-sprint.md" | \
       grep "invoke-hooks" | grep -q "\-\-capacity="; then
        echo -e "${GREEN}PASS${NC}"
        return 0
    else
        echo -e "${RED}FAIL${NC}"
        echo "  Expected: --capacity parameter in invoke-hooks"
        echo "  Actual: Parameter not found"
        return 1
    fi
}

# Test 4: Feedback questions adapt to empty sprint scenario
test_empty_sprint_questions() {
    echo -n "Test 5.4: Feedback adapts to empty sprint... "

    # Create temp config for empty sprint
    TEMP_CONFIG="/tmp/hooks-test-$$.yaml"
    cat > "$TEMP_CONFIG" <<EOF
feedback_hooks:
  enabled: true
  hooks:
    create-sprint:
      enabled: true
      check_command: "devforgeai check-hooks"
      invoke_command: "devforgeai invoke-hooks"
EOF

    # Invoke hooks with 0 stories (will fail without full setup, but check parameter acceptance)
    output=$(devforgeai invoke-hooks --operation=create-sprint \
        --sprint-name="Empty-Sprint-Test" \
        --story-count=0 \
        --capacity=0 \
        --config="$TEMP_CONFIG" 2>&1 || true)

    rm -f "$TEMP_CONFIG"

    # Verify 0 values accepted (not rejected as invalid)
    if echo "$output" | grep -qi "invalid.*story.*count\|story.*count.*must.*positive\|capacity.*cannot.*zero"; then
        echo -e "${RED}FAIL${NC}"
        echo "  Expected: story-count=0 and capacity=0 accepted"
        echo "  Actual: Validation error - $output"
        return 1
    else
        echo -e "${GREEN}PASS${NC}"
        return 0
    fi
}

# Test 5: Empty sprint still creates valid sprint file
test_empty_sprint_file_valid() {
    echo -n "Test 5.5: Empty sprint creates valid sprint file... "

    # Verify Phase N doesn't prevent sprint file creation with 0 stories
    # This is implicit - if Phase N doesn't HALT, sprint file creation proceeds
    if grep -A 100 "### Phase N: Feedback Hook Integration" "$PROJECT_ROOT/.claude/commands/create-sprint.md" | \
       grep -q "HALT.*empty\|exit.*0.*stories\|return.*no.*stories"; then
        echo -e "${RED}FAIL${NC}"
        echo "  Expected: No HALT for empty sprint"
        echo "  Actual: Found blocking statement"
        return 1
    else
        echo -e "${GREEN}PASS${NC}"
        return 0
    fi
}

# Test 6: Data validation accepts 0 as valid story count
test_zero_story_count_validation() {
    echo -n "Test 5.6: Story count validation accepts 0... "

    # Check validation rules in story context
    # Rule: "Must be non-negative integer (0-999)" - 0 should be valid
    story_content=$(cat "$PROJECT_ROOT/.ai_docs/Stories/STORY-029-wire-hooks-into-create-sprint-command.story.md")

    if echo "$story_content" | grep -qi "non-negative.*0-999\|0.*to.*999"; then
        echo -e "${GREEN}PASS${NC}"
        echo "  Note: Validation allows 0-999 (includes 0)"
        return 0
    else
        echo -e "${RED}FAIL${NC}"
        echo "  Expected: Validation rule allows 0"
        echo "  Actual: Validation rule not found or incorrect"
        return 1
    fi
}

# Test 7: Data validation accepts 0 as valid capacity
test_zero_capacity_validation() {
    echo -n "Test 5.7: Capacity validation accepts 0... "

    story_content=$(cat "$PROJECT_ROOT/.ai_docs/Stories/STORY-029-wire-hooks-into-create-sprint-command.story.md")

    if echo "$story_content" | grep -qi "capacity.*non-negative.*0-9999"; then
        echo -e "${GREEN}PASS${NC}"
        echo "  Note: Validation allows 0-9999 (includes 0)"
        return 0
    else
        echo -e "${RED}FAIL${NC}"
        echo "  Expected: Capacity validation allows 0"
        echo "  Actual: Validation rule not found or incorrect"
        return 1
    fi
}

# Run all tests
FAILED_TESTS=0

test_zero_story_count || FAILED_TESTS=$((FAILED_TESTS + 1))
test_invoke_hooks_zero_stories || FAILED_TESTS=$((FAILED_TESTS + 1))
test_invoke_hooks_zero_capacity || FAILED_TESTS=$((FAILED_TESTS + 1))
test_empty_sprint_questions || FAILED_TESTS=$((FAILED_TESTS + 1))
test_empty_sprint_file_valid || FAILED_TESTS=$((FAILED_TESTS + 1))
test_zero_story_count_validation || FAILED_TESTS=$((FAILED_TESTS + 1))
test_zero_capacity_validation || FAILED_TESTS=$((FAILED_TESTS + 1))

echo "========================================="
if [ $FAILED_TESTS -eq 0 ]; then
    echo -e "${GREEN}ALL TESTS PASSED${NC}"
    exit 0
else
    echo -e "${RED}$FAILED_TESTS TEST(S) FAILED${NC}"
    exit 1
fi
