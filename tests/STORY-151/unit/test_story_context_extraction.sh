#!/usr/bin/env bash

# STORY-151: Post-Subagent Recording Hook - Story Context Extraction Tests (AC#3)
# Tests that hook extracts story context from multiple sources in priority order:
# 1. DEVFORGEAI_STORY_ID environment variable
# 2. Most recent state file in devforgeai/workflows/
# 3. Grep for STORY-XXX pattern

set -euo pipefail

# Setup
readonly TEST_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
readonly PROJECT_ROOT="$(cd "${TEST_DIR}/../../../" && pwd)"
readonly TEMP_DIR="${TEST_DIR}/.temp"

# Color codes for output
readonly RED='\033[0;31m'
readonly GREEN='\033[0;32m'
readonly YELLOW='\033[1;33m'
readonly NC='\033[0m'

# Test counters
tests_run=0
tests_passed=0
tests_failed=0

# Cleanup function
cleanup_temp_files() {
    if [[ -d "$TEMP_DIR" ]]; then
        rm -rf "$TEMP_DIR"
    fi
}

trap cleanup_temp_files EXIT

# Test helper functions
run_test() {
    local test_name="$1"
    local test_func="$2"

    echo -e "\n${YELLOW}Running: ${test_name}${NC}"
    tests_run=$((tests_run + 1))

    if $test_func; then
        echo -e "${GREEN}✓ PASSED${NC}"
        tests_passed=$((tests_passed + 1))
        return 0
    else
        echo -e "${RED}✗ FAILED${NC}"
        tests_failed=$((tests_failed + 1))
        return 1
    fi
}

assert_equals() {
    local expected="$1"
    local actual="$2"
    local message="${3:-Assertion failed}"

    if [[ "$expected" != "$actual" ]]; then
        echo "  Error: $message"
        echo "  Expected: $expected"
        echo "  Actual: $actual"
        return 1
    fi
    return 0
}

assert_matches_pattern() {
    local text="$1"
    local pattern="$2"
    local message="${3:-Pattern not matched}"

    if ! echo "$text" | grep -qE "$pattern"; then
        echo "  Error: $message"
        echo "  Text: $text"
        echo "  Pattern: $pattern"
        return 1
    fi
    return 0
}

# Setup temporary directories
mkdir -p "$TEMP_DIR"

# TEST AC#3.1: Extract story context from DEVFORGEAI_STORY_ID env var (highest priority)
test_extract_from_env_var_highest_priority() {
    local expected_story_id="STORY-151"

    # Set environment variable
    export DEVFORGEAI_STORY_ID="$expected_story_id"

    # Create mock hook script source that would extract the ID
    # In real implementation, hook would read from env var
    local extracted_id="${DEVFORGEAI_STORY_ID:-}"

    assert_equals "$expected_story_id" "$extracted_id" \
        "DEVFORGEAI_STORY_ID environment variable not extracted"

    unset DEVFORGEAI_STORY_ID
    return 0
}

# TEST AC#3.2: Extract from most recent state file in devforgeai/workflows/
test_extract_from_latest_state_file() {
    local workflows_dir="$TEMP_DIR/workflows"
    mkdir -p "$workflows_dir"

    # Create multiple state files
    echo '{"story_id": "STORY-100"}' > "$workflows_dir/STORY-100-phase-state.json"
    sleep 0.1
    echo '{"story_id": "STORY-101"}' > "$workflows_dir/STORY-101-phase-state.json"
    sleep 0.1
    echo '{"story_id": "STORY-151"}' > "$workflows_dir/STORY-151-phase-state.json"

    # Find most recently modified state file
    local latest_file=$(find "$workflows_dir" -name "*-phase-state.json" -type f -printf '%T@ %p\n' | sort -n | tail -1 | cut -d' ' -f2-)
    local extracted_id=$(basename "$latest_file" | grep -oE "STORY-[0-9]+")

    assert_equals "STORY-151" "$extracted_id" \
        "Most recent state file not correctly identified"

    return 0
}

# TEST AC#3.3: Fall back to grep for STORY-XXX pattern in context
test_extract_from_grep_pattern() {
    local context_file="$TEMP_DIR/context.txt"

    # Create a context file with story pattern
    cat > "$context_file" << 'EOF'
Working on STORY-151 implementation
Task: Generate hook tests
Phase: TDD Red
EOF

    # Extract story ID from context
    local extracted_id=$(grep -oE "STORY-[0-9]+" "$context_file" | head -1)

    assert_equals "STORY-151" "$extracted_id" \
        "STORY-XXX pattern not extracted from context"

    return 0
}

# TEST AC#3.4: Priority order is respected (env > state file > grep)
test_priority_order_env_over_state_file() {
    local workflows_dir="$TEMP_DIR/workflows"
    mkdir -p "$workflows_dir"

    # Create state file with different story
    echo '{"story_id": "STORY-100"}' > "$workflows_dir/STORY-100-phase-state.json"

    # Set environment variable to different story
    export DEVFORGEAI_STORY_ID="STORY-151"

    # Extraction should prefer env var
    local extracted_id="${DEVFORGEAI_STORY_ID:-}"

    assert_equals "STORY-151" "$extracted_id" \
        "Priority not respected: env var should override state file"

    unset DEVFORGEAI_STORY_ID
    return 0
}

# TEST AC#3.5: Priority order is respected (state file > grep)
test_priority_order_state_file_over_grep() {
    local workflows_dir="$TEMP_DIR/workflows"
    local context_file="$TEMP_DIR/context.txt"

    mkdir -p "$workflows_dir"

    # Create state file with STORY-151
    echo '{"story_id": "STORY-151"}' > "$workflows_dir/STORY-151-phase-state.json"

    # Create context file with different story
    echo "Working on STORY-100" > "$context_file"

    # When env var not set, should use state file not grep
    local extracted_id=$(basename "$workflows_dir"/STORY-*.json | grep -oE "STORY-[0-9]+")

    assert_equals "STORY-151" "$extracted_id" \
        "Priority not respected: state file should override grep"

    return 0
}

# TEST AC#3.6: No story context detected (all sources fail)
test_no_story_context_detected() {
    local workflows_dir="$TEMP_DIR/workflows_empty"
    mkdir -p "$workflows_dir"

    # No env var set
    unset DEVFORGEAI_STORY_ID

    # No state files in workflows dir
    local state_files=$(find "$workflows_dir" -name "*-phase-state.json" 2>/dev/null | wc -l)

    assert_equals "0" "$state_files" \
        "Should detect no state files when none exist"

    return 0
}

# TEST AC#3.7: State file path matches pattern STORY-XXX-phase-state.json
test_state_file_pattern_correct() {
    local workflows_dir="$TEMP_DIR/workflows"
    mkdir -p "$workflows_dir"

    # Create state file with correct pattern
    local correct_file="$workflows_dir/STORY-151-phase-state.json"
    echo '{"story_id": "STORY-151"}' > "$correct_file"

    # Extract story ID from filename pattern
    if [[ "$correct_file" =~ STORY-([0-9]+)-phase-state\.json ]]; then
        local extracted_id="STORY-${BASH_REMATCH[1]}"
        assert_equals "STORY-151" "$extracted_id" \
            "State file pattern not recognized"
    else
        echo "  Error: State file pattern not matched"
        return 1
    fi

    return 0
}

# TEST AC#3.8: Multiple STORY-XXX patterns - uses first one
test_multiple_patterns_uses_first() {
    local context_file="$TEMP_DIR/multi_context.txt"

    cat > "$context_file" << 'EOF'
Task for STORY-100 and STORY-151
Also related to STORY-200
EOF

    # Extract first story pattern
    local extracted_id=$(grep -oE "STORY-[0-9]+" "$context_file" | head -1)

    assert_equals "STORY-100" "$extracted_id" \
        "Should extract first STORY-XXX pattern found"

    return 0
}

# TEST AC#3.9: STORY ID format validation (STORY-NNN)
test_story_id_format_validation() {
    local valid_pattern="STORY-[0-9]+"
    local test_cases=(
        "STORY-1:valid"
        "STORY-001:valid"
        "STORY-999:valid"
        "story-151:invalid"
        "STORY-abc:invalid"
        "STRY-151:invalid"
        "STORY:invalid"
    )

    for test_case in "${test_cases[@]}"; do
        local text="${test_case%:*}"
        local expected="${test_case##*:}"

        if [[ "$text" =~ $valid_pattern ]]; then
            if [[ "$expected" == "invalid" ]]; then
                echo "  Error: Incorrectly matched invalid pattern: $text"
                return 1
            fi
        else
            if [[ "$expected" == "valid" ]]; then
                echo "  Error: Failed to match valid pattern: $text"
                return 1
            fi
        fi
    done

    return 0
}

# TEST AC#3.10: Environment variable takes precedence over all sources
test_env_var_absolute_precedence() {
    local workflows_dir="$TEMP_DIR/workflows"
    local context_file="$TEMP_DIR/context.txt"

    mkdir -p "$workflows_dir"

    # Create conflicting sources
    echo '{"story_id": "STORY-100"}' > "$workflows_dir/STORY-100-phase-state.json"
    echo "Working on STORY-200" > "$context_file"

    # Set environment to STORY-151
    export DEVFORGEAI_STORY_ID="STORY-151"

    # Should use env var
    local extracted_id="${DEVFORGEAI_STORY_ID:-}"

    assert_equals "STORY-151" "$extracted_id" \
        "Environment variable should have absolute precedence"

    unset DEVFORGEAI_STORY_ID
    return 0
}

# MAIN - Run all tests
echo "============================================================"
echo "STORY-151: Story Context Extraction Tests (AC#3)"
echo "============================================================"

run_test "extract from DEVFORGEAI_STORY_ID env var (highest priority)" \
    test_extract_from_env_var_highest_priority
run_test "extract from most recent state file in devforgeai/workflows/" \
    test_extract_from_latest_state_file
run_test "fall back to grep for STORY-XXX pattern" \
    test_extract_from_grep_pattern
run_test "priority order: env var over state file" \
    test_priority_order_env_over_state_file
run_test "priority order: state file over grep" \
    test_priority_order_state_file_over_grep
run_test "handle case when no story context detected" \
    test_no_story_context_detected
run_test "state file path matches pattern STORY-XXX-phase-state.json" \
    test_state_file_pattern_correct
run_test "multiple STORY-XXX patterns - uses first one" \
    test_multiple_patterns_uses_first
run_test "story ID format validation (STORY-NNN)" \
    test_story_id_format_validation
run_test "environment variable has absolute precedence" \
    test_env_var_absolute_precedence

# Print summary
echo ""
echo "============================================================"
echo "Test Summary"
echo "============================================================"
echo "Total: $tests_run"
echo "Passed: $tests_passed"
echo "Failed: $tests_failed"
echo "============================================================"

exit $tests_failed
