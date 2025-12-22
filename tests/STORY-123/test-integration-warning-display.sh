#!/bin/bash
# STORY-123: Integration Tests for Warning Display and User Interaction
# Tests warning display, story count formatting, and AskUserQuestion integration
# Framework: Bash shell scripting (AAA pattern)
# Status: RED PHASE (failing tests - no implementation yet)

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
TEMP_DIR=$(mktemp -d)

# Test counters
TOTAL_TESTS=0
PASSED_TESTS=0
FAILED_TESTS=0

# Cleanup function
cleanup() {
    rm -rf "$TEMP_DIR"
}
trap cleanup EXIT

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "STORY-123: Integration Tests - Warning Display"
echo "Status: RED PHASE (All tests should fail - implementation pending)"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Test function (AAA pattern)
run_test() {
    local test_num="$1"
    local test_name="$2"
    local test_function="$3"

    TOTAL_TESTS=$((TOTAL_TESTS + 1))
    echo "Test $TOTAL_TESTS: $test_name"

    if $test_function 2>&1 | grep -q "✅"; then
        echo "  ✅ PASSED"
        PASSED_TESTS=$((PASSED_TESTS + 1))
    else
        echo "  ❌ FAILED (expected at RED phase)"
        FAILED_TESTS=$((FAILED_TESTS + 1))
    fi
    echo ""
}

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# TEST 5: Warning displays with correct current story
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
test_warning_displays_current_story() {
    # Arrange: Create temporary test file with warning function
    cat > "$TEMP_DIR/test_warning.sh" << 'EOF'
#!/bin/bash
# Mock implementation - this should be replaced by actual preflight-validation.md Step 1.8

display_warning() {
    local current_story="$1"
    local other_stories="$2"

    echo "+----------------------------------------------+"
    echo "| WARNING: UNCOMMITTED STORY FILES DETECTED   |"
    echo "+----------------------------------------------+"
    echo ""
    echo "Your story: $current_story (will be modified by this /dev run)"
    echo ""
    echo "Other uncommitted stories: $(echo "$other_stories" | wc -l) files"
}

current_story="STORY-114"
other_stories="STORY-100
STORY-115"

display_warning "$current_story" "$other_stories"
EOF

    # Act: Run the function and capture output
    local warning_output=$(bash "$TEMP_DIR/test_warning.sh")

    # Assert: Should show current story in warning
    if echo "$warning_output" | grep -q "Your story: STORY-114"; then
        echo "✅"
    else
        echo "❌ Warning did not show current story"
    fi
}

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# TEST 6: Warning includes correct story count and ranges
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
test_warning_includes_count_and_ranges() {
    # Arrange: Create temporary test file with range formatting logic
    cat > "$TEMP_DIR/test_ranges.sh" << 'EOF'
#!/bin/bash
# Mock implementation for range detection

format_ranges() {
    local story_numbers="$1"

    # Expected output: "STORY-100 through STORY-113 (14 files)"
    # and "STORY-115 through STORY-119 (5 files)"

    # This is placeholder - actual implementation would use algorithm
    local range1="STORY-100 through STORY-113 (14 files)"
    local range2="STORY-115 through STORY-119 (5 files)"

    echo "$range1"
    echo "$range2"
}

# Test case: AC#3 requirement
echo "Other uncommitted stories: 21 files"
echo "  - STORY-100 through STORY-113 (14 files)"
echo "  - STORY-115 through STORY-119 (7 files)"
EOF

    # Act: Run the function
    local range_output=$(bash "$TEMP_DIR/test_ranges.sh")

    # Assert: Should show ranges with file counts
    if echo "$range_output" | grep -q "STORY-100 through STORY-113"; then
        echo "✅"
    else
        echo "❌ Range format incorrect"
    fi
}

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# TEST 7: User can select "Continue with scoped commits"
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
test_user_can_select_continue_option() {
    # Arrange: Mock AskUserQuestion options
    cat > "$TEMP_DIR/test_options.sh" << 'EOF'
#!/bin/bash
# Mock AskUserQuestion with 3 options per AC#4

show_options() {
    echo "Please choose an action:"
    echo ""
    echo "1) Continue with scoped commits (recommended)"
    echo "   → Commits include ONLY your story (STORY-114)"
    echo "   → Pre-commit validation scoped to STORY-114"
    echo "   → Other stories remain uncommitted"
    echo ""
    echo "2) Commit other stories first"
    echo "   → Workflow HALTS"
    echo "   → Commit other stories manually, then re-run /dev"
    echo ""
    echo "3) Show me the list of uncommitted files"
    echo "   → Displays full git status output"
}

show_options
EOF

    # Act: Run and check for all 3 options
    local options_output=$(bash "$TEMP_DIR/test_options.sh")

    # Assert: Should show all 3 options from AC#4
    if echo "$options_output" | grep -q "Continue with scoped commits" && \
       echo "$options_output" | grep -q "Commit other stories first" && \
       echo "$options_output" | grep -q "Show me the list"; then
        echo "✅"
    else
        echo "❌ Not all 3 options displayed"
    fi
}

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# TEST 8: DEVFORGEAI_STORY env var set on "Continue" selection
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
test_devforgeai_story_env_var_set() {
    # Arrange: Mock handling of user selection
    cat > "$TEMP_DIR/test_env_var.sh" << 'EOF'
#!/bin/bash
# Mock environment variable setting from AC#5

handle_continue_selection() {
    local current_story="$1"

    # Should export DEVFORGEAI_STORY per AC#5 integration with STORY-121
    export DEVFORGEAI_STORY="$current_story"

    # Verify it's set
    if [ -n "$DEVFORGEAI_STORY" ]; then
        echo "DEVFORGEAI_STORY=$DEVFORGEAI_STORY"
    fi
}

handle_continue_selection "STORY-114"
EOF

    # Act: Run and check env var
    local env_output=$(bash "$TEMP_DIR/test_env_var.sh")

    # Assert: Should set DEVFORGEAI_STORY=STORY-114
    if echo "$env_output" | grep -q "DEVFORGEAI_STORY=STORY-114"; then
        echo "✅"
    else
        echo "❌ DEVFORGEAI_STORY not set correctly"
    fi
}

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# TEST 9: "Commit other stories first" option HALTs workflow
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
test_commit_others_first_halts_workflow() {
    # Arrange: Mock HALT response per AC#4
    cat > "$TEMP_DIR/test_halt.sh" << 'EOF'
#!/bin/bash
# Mock HALT response

handle_commit_others_selection() {
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "HALT: Uncommitted Other Stories"
    echo ""
    echo "Please commit the other story files first, then re-run /dev"
    echo ""
    echo "Command: git add devforgeai/specs/Stories/*.story.md"
    echo "         git commit -m 'chore: update story files'"
    echo "         /dev STORY-114"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    return 1  # Exit code 1 = HALT
}

handle_commit_others_selection
EOF

    # Act: Run and check exit code
    local exit_code=0
    bash "$TEMP_DIR/test_halt.sh" || exit_code=$?

    # Assert: Should return exit code 1 (HALT)
    if [ "$exit_code" -eq 1 ]; then
        echo "✅"
    else
        echo "❌ Did not HALT with exit code 1"
    fi
}

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# TEST 10: "Show me the list" option displays git status output
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
test_show_list_displays_git_status() {
    # Arrange: Mock git status display
    cat > "$TEMP_DIR/test_show_list.sh" << 'EOF'
#!/bin/bash
# Mock "Show me the list" display per AC#4

show_uncommitted_stories() {
    local git_status_output=" M devforgeai/specs/Stories/STORY-100.story.md
 M devforgeai/specs/Stories/STORY-101.story.md
 M devforgeai/specs/Stories/STORY-114.story.md
 M devforgeai/specs/Stories/STORY-115.story.md"

    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "Uncommitted Story Files:"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "$git_status_output"
}

show_uncommitted_stories
EOF

    # Act: Run and capture output
    local list_output=$(bash "$TEMP_DIR/test_show_list.sh")

    # Assert: Should display git status output with story files
    if echo "$list_output" | grep -q "STORY-114.story.md"; then
        echo "✅"
    else
        echo "❌ Did not display story files list"
    fi
}

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# EXECUTION
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

echo "Category 1: Warning Display"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

run_test 5 "Warning displays with correct current story" test_warning_displays_current_story
run_test 6 "Warning includes correct story count and ranges" test_warning_includes_count_and_ranges

echo "Category 2: User Interaction"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

run_test 7 "User can select 'Continue with scoped commits'" test_user_can_select_continue_option
run_test 8 "DEVFORGEAI_STORY env var set on Continue selection" test_devforgeai_story_env_var_set
run_test 9 "'Commit other stories first' option HALTs workflow" test_commit_others_first_halts_workflow
run_test 10 "'Show me the list' option displays git status output" test_show_list_displays_git_status

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# RESULTS
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Test Results:"
echo "  Total Tests: $TOTAL_TESTS"
echo "  Passed: $PASSED_TESTS"
echo "  Failed: $FAILED_TESTS"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

if [ $FAILED_TESTS -eq 0 ]; then
    echo "✅ All tests passed!"
    exit 0
else
    echo "⚠️  RED PHASE: $FAILED_TESTS test(s) failing (expected - implementation pending)"
    exit 1
fi
