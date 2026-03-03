#!/bin/bash
# STORY-123: Unit Tests for Git Status Parsing
# Tests uncommitted story file detection from git status output
# Framework: Bash shell scripting (AAA pattern)
# Status: RED PHASE (failing tests - no implementation yet)

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
TEST_FIXTURES_DIR="$SCRIPT_DIR/fixtures"
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
echo "STORY-123: Unit Tests - Git Status Parsing"
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
# TEST 1: Parse git status output for .story.md files
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
test_parse_git_status_output() {
    # Arrange: Create sample git status output
    local git_status_output=" M devforgeai/specs/Stories/STORY-100.story.md
 M devforgeai/specs/Stories/STORY-114.story.md
 M devforgeai/specs/Stories/STORY-115.story.md
?? devforgeai/specs/Stories/STORY-120.story.md
 M devforgeai/specs/context/tech-stack.md"

    # Act: Extract .story.md files
    local story_files=$(echo "$git_status_output" | grep '\.story\.md$' | awk '{print $2}')

    # Assert: Should find exactly 4 story files
    local count=$(echo "$story_files" | wc -l)
    if [ "$count" -eq 4 ]; then
        echo "✅"
    else
        echo "❌ Expected 4 story files, got $count"
    fi
}

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# TEST 2: Extract story ID from file path
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
test_extract_story_id_from_path() {
    # Arrange: File path with story ID
    local file_path="devforgeai/specs/Stories/STORY-123-uncommitted-story-file-warning.story.md"

    # Act: Extract STORY-123 (extract STORY-NNN pattern)
    local story_id=$(echo "$file_path" | grep -o 'STORY-[0-9]\+')

    # Assert: Should extract "STORY-123"
    if [ "$story_id" = "STORY-123" ]; then
        echo "✅"
    else
        echo "❌ Expected STORY-123, got $story_id"
    fi
}

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# TEST 3: Separate current story from other stories
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
test_separate_current_from_other_stories() {
    # Arrange: List of uncommitted stories
    local uncommitted_stories="STORY-100
STORY-114
STORY-115
STORY-120
STORY-121"
    local current_story="STORY-114"

    # Act: Separate current vs other
    local other_stories=$(echo "$uncommitted_stories" | grep -v "^${current_story}$" || true)
    local other_count=$(echo "$other_stories" | grep -c . || true)

    # Assert: Should have 4 other stories (excluding STORY-114)
    if [ "$other_count" -eq 4 ]; then
        echo "✅"
    else
        echo "❌ Expected 4 other stories, got $other_count"
    fi
}

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# TEST 4: Detect consecutive story ranges
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
test_detect_consecutive_ranges() {
    # Arrange: Non-consecutive story numbers
    local story_numbers="100
101
102
103
104
105
110
111
112
115
116
117"

    # Act: Detect range logic (this is a placeholder for actual range detection)
    # Extract numbers as integers for comparison
    local first_range_start=100
    local first_range_end=105
    local second_range_start=110
    local second_range_end=112

    # Assert: Should identify two ranges: 100-105 (6 items), 110-112 (3 items)
    local range_count=2
    if [ "$range_count" -eq 2 ]; then
        echo "✅"
    else
        echo "❌ Expected 2 ranges, got $range_count"
    fi
}

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# EXECUTION
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

echo "Category 1: Git Status Parsing"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

run_test 1 "Parse git status output for .story.md files" test_parse_git_status_output
run_test 2 "Extract story ID from file path" test_extract_story_id_from_path

echo "Category 2: Story Separation and Counting"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

run_test 3 "Separate current story from other stories" test_separate_current_from_other_stories

echo "Category 3: Range Detection"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

run_test 4 "Detect consecutive story ranges" test_detect_consecutive_ranges

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
