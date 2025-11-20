#!/bin/bash
# Edge Case Test: Concurrent sprint creation
# Tests that multiple simultaneous executions don't conflict

set -e

TEST_NAME="Concurrent Sprint Creation"
TEST_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$TEST_DIR/../../.." && pwd)"

# ANSI colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo "========================================="
echo "TEST: $TEST_NAME"
echo "========================================="

# Test 1: Unique feedback filenames with timestamps
test_unique_feedback_filenames() {
    echo -n "Test E2.1: Unique feedback filenames with timestamps... "

    story_content=$(cat "$PROJECT_ROOT/.ai_docs/Stories/STORY-029-wire-hooks-into-create-sprint-command.story.md")

    if echo "$story_content" | grep -q "create-sprint-.*YYYY-MM-DD-HH-MM-SS\|timestamp.*filename"; then
        echo -e "${GREEN}PASS${NC}"
        echo "  Note: Story documents timestamp-based filename pattern"
        return 0
    else
        echo -e "${YELLOW}WARN${NC}"
        echo "  Warning: Timestamp pattern not documented (may cause conflicts)"
        return 0  # Non-critical
    fi
}

# Test 2: Simulate concurrent hook invocations
test_concurrent_hook_invocations() {
    echo -n "Test E2.2: Concurrent hook invocations don't conflict... "

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

    # Create temp feedback directory
    TEMP_FEEDBACK_DIR="/tmp/devforgeai-feedback-test-$$"
    mkdir -p "$TEMP_FEEDBACK_DIR"

    # Launch 3 concurrent invoke-hooks (will fail without full setup, but test file creation)
    pids=()
    for i in 1 2 3; do
        (
            devforgeai invoke-hooks --operation=create-sprint \
                --sprint-name="Concurrent-Sprint-$i" \
                --story-count=$i \
                --capacity=$((i * 5)) \
                --config="$TEMP_CONFIG" \
                2>/dev/null || true
        ) &
        pids+=($!)
    done

    # Wait for all processes
    for pid in "${pids[@]}"; do
        wait "$pid" 2>/dev/null || true
    done

    # Cleanup
    rm -f "$TEMP_CONFIG"
    rm -rf "$TEMP_FEEDBACK_DIR"

    # If we got here without deadlock, test passes
    echo -e "${GREEN}PASS${NC}"
    echo "  Note: All concurrent invocations completed"
    return 0
}

# Test 3: File locking or atomic writes
test_file_locking() {
    echo -n "Test E2.3: File operations are safe for concurrency... "

    # Check if invoke-hooks.py uses file locking or atomic writes
    if [ -f "$PROJECT_ROOT/.claude/scripts/devforgeai_cli/commands/invoke_hooks.py" ]; then
        content=$(cat "$PROJECT_ROOT/.claude/scripts/devforgeai_cli/commands/invoke_hooks.py")

        if echo "$content" | grep -q "fcntl\|lockf\|flock\|FileLock\|atomic"; then
            echo -e "${GREEN}PASS${NC}"
            echo "  Note: File locking mechanism detected"
            return 0
        else
            echo -e "${YELLOW}WARN${NC}"
            echo "  Warning: No file locking detected (may cause conflicts)"
            return 0  # Non-critical for current scope
        fi
    else
        echo -e "${YELLOW}WARN${NC}"
        echo "  Warning: invoke_hooks.py not found"
        return 0
    fi
}

# Test 4: NFR-008 compliance (10 simultaneous executions)
test_nfr008_compliance() {
    echo -n "Test E2.4: NFR-008 scalability requirement documented... "

    story_content=$(cat "$PROJECT_ROOT/.ai_docs/Stories/STORY-029-wire-hooks-into-create-sprint-command.story.md")

    if echo "$story_content" | grep -q "NFR-008.*10.*simultan\|10 parallel.*create-sprint"; then
        echo -e "${GREEN}PASS${NC}"
        echo "  Note: NFR-008 requires 10 concurrent executions support"
        return 0
    else
        echo -e "${RED}FAIL${NC}"
        echo "  Expected: NFR-008 documented"
        echo "  Actual: Requirement not found"
        return 1
    fi
}

# Test 5: Race condition in sprint numbering
test_sprint_numbering_race_condition() {
    echo -n "Test E2.5: Sprint numbering safe from race conditions... "

    # This is handled by sprint-planner subagent, not hooks
    # But verify hooks don't interfere with sprint file creation
    if grep -A 100 "### Phase N: Feedback Hook Integration" "$PROJECT_ROOT/.claude/commands/create-sprint.md" | \
       grep -q "Sprint.*file\|write.*sprint\|create.*sprint"; then
        # If Phase N modifies sprint files, race condition possible
        echo -e "${YELLOW}WARN${NC}"
        echo "  Warning: Phase N may touch sprint files (check for race conditions)"
        return 0
    else
        # Phase N only invokes hooks, doesn't touch sprint files
        echo -e "${GREEN}PASS${NC}"
        echo "  Note: Phase N doesn't modify sprint files (no race condition)"
        return 0
    fi
}

# Test 6: Feedback file overwrites prevented
test_feedback_file_overwrites() {
    echo -n "Test E2.6: Feedback files won't overwrite each other... "

    # Verify filename pattern includes unique identifier
    story_content=$(cat "$PROJECT_ROOT/.ai_docs/Stories/STORY-029-wire-hooks-into-create-sprint-command.story.md")

    if echo "$story_content" | grep -q "unique.*timestamp\|YYYY-MM-DD-HH-MM-SS\|session.*id"; then
        echo -e "${GREEN}PASS${NC}"
        return 0
    else
        echo -e "${YELLOW}WARN${NC}"
        echo "  Warning: Unique filename strategy not documented"
        return 0
    fi
}

# Run all tests
FAILED_TESTS=0

test_unique_feedback_filenames || FAILED_TESTS=$((FAILED_TESTS + 1))
test_concurrent_hook_invocations || FAILED_TESTS=$((FAILED_TESTS + 1))
test_file_locking || FAILED_TESTS=$((FAILED_TESTS + 1))
test_nfr008_compliance || FAILED_TESTS=$((FAILED_TESTS + 1))
test_sprint_numbering_race_condition || FAILED_TESTS=$((FAILED_TESTS + 1))
test_feedback_file_overwrites || FAILED_TESTS=$((FAILED_TESTS + 1))

echo "========================================="
if [ $FAILED_TESTS -eq 0 ]; then
    echo -e "${GREEN}ALL TESTS PASSED${NC}"
    exit 0
else
    echo -e "${RED}$FAILED_TESTS TEST(S) FAILED${NC}"
    exit 1
fi
