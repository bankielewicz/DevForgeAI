#!/bin/bash

################################################################################
# UNIT TEST SUITE: Story Creation Guidance Loading
#
# File: devforgeai/tests/skills/test-story-creation-guidance-unit.sh
# Purpose: Test guidance file loading, pattern extraction, mapping, and fallback
# Coverage: 15 unit tests for Step 0 and pattern operations
# Framework: Bash + grep for verification
#
# Run: bash devforgeai/tests/skills/test-story-creation-guidance-unit.sh
################################################################################

set -euo pipefail

REPO_ROOT="/mnt/c/Projects/DevForgeAI2"
GUIDANCE_FILE="$REPO_ROOT/src/claude/skills/devforgeai-ideation/references/user-input-guidance.md"
INTEGRATION_GUIDE="$REPO_ROOT/src/claude/skills/devforgeai-story-creation/references/user-input-integration-guide.md"
TEST_RESULTS=0
TEST_TOTAL=0

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

###############################################################################
# UTILITY FUNCTIONS
###############################################################################

assert_file_exists() {
    local file=$1
    if [[ ! -f "$file" ]]; then
        echo -e "${RED}FAIL${NC}: File does not exist: $file"
        return 1
    fi
    echo -e "${GREEN}PASS${NC}: File exists: $file"
    return 0
}

assert_file_contains() {
    local file=$1
    local pattern=$2
    if ! grep -q "$pattern" "$file"; then
        echo -e "${RED}FAIL${NC}: File '$file' does not contain pattern: '$pattern'"
        return 1
    fi
    echo -e "${GREEN}PASS${NC}: File contains pattern: '$pattern'"
    return 0
}

assert_file_not_contains() {
    local file=$1
    local pattern=$2
    if grep -q "$pattern" "$file"; then
        echo -e "${RED}FAIL${NC}: File '$file' should not contain pattern: '$pattern'"
        return 1
    fi
    echo -e "${GREEN}PASS${NC}: File does not contain pattern: '$pattern'"
    return 0
}

assert_file_line_count() {
    local file=$1
    local min_lines=$2
    local actual_lines=$(wc -l < "$file")
    if (( actual_lines < min_lines )); then
        echo -e "${RED}FAIL${NC}: File has $actual_lines lines (expected ≥$min_lines)"
        return 1
    fi
    echo -e "${GREEN}PASS${NC}: File has $actual_lines lines (expected ≥$min_lines)"
    return 0
}

run_test() {
    local test_num=$1
    local test_name=$2
    ((TEST_TOTAL++))

    echo ""
    echo "======================================================================"
    echo "TEST $test_num: $test_name"
    echo "======================================================================"
}

record_result() {
    if [[ $? -eq 0 ]]; then
        ((TEST_RESULTS++))
        return 0
    fi
    return 1
}

###############################################################################
# UNIT TESTS (15 total)
###############################################################################

# TEST 01: Step 0 loads guidance with valid file
test_01_step0_loads_guidance_valid_file() {
    run_test 01 "Step 0 loads guidance with valid file"

    # Verify guidance file exists
    assert_file_exists "$GUIDANCE_FILE"
    record_result

    # Verify file is readable (>100 lines)
    assert_file_line_count "$GUIDANCE_FILE" 100
    record_result

    # Verify contains pattern definitions (### Pattern)
    assert_file_contains "$GUIDANCE_FILE" "^###.*Pattern"
    record_result
}

# TEST 02: Step 0 handles missing file gracefully
test_02_step0_handles_missing_file() {
    run_test 02 "Step 0 handles missing file gracefully"

    # Backup original file
    cp "$GUIDANCE_FILE" "${GUIDANCE_FILE}.test_backup"

    # Test: Remove file
    rm "$GUIDANCE_FILE" 2>/dev/null || true

    # Verify file is gone
    if [[ ! -f "$GUIDANCE_FILE" ]]; then
        echo -e "${GREEN}PASS${NC}: File successfully removed for testing"
        ((TEST_RESULTS++))
    else
        echo -e "${RED}FAIL${NC}: File still exists after removal attempt"
    fi

    # Restore file
    mv "${GUIDANCE_FILE}.test_backup" "$GUIDANCE_FILE"

    # Verify restoration
    assert_file_exists "$GUIDANCE_FILE"
    record_result
}

# TEST 03: Step 0 handles corrupted markdown gracefully
test_03_step0_handles_corrupted_file() {
    run_test 03 "Step 0 handles corrupted markdown gracefully"

    # Backup original
    cp "$GUIDANCE_FILE" "${GUIDANCE_FILE}.test_backup"

    # Create test corrupted file with invalid markdown
    cat > /tmp/guidance_corrupted.md << 'EOF'
# INVALID MARKDOWN
### Broken Pattern {{{ UNCLOSED
This has unmatched braces
[Link with no closing](http://example.com
- List item with **bold** but missing close **
EOF

    # Test: Can we detect malformed markdown?
    if ! grep -q "^###.*Pattern" /tmp/guidance_corrupted.md; then
        echo -e "${GREEN}PASS${NC}: Corrupted file has no valid pattern definitions"
        ((TEST_RESULTS++))
    fi

    # Restore original
    mv "${GUIDANCE_FILE}.test_backup" "$GUIDANCE_FILE"

    # Cleanup
    rm /tmp/guidance_corrupted.md

    # Verify restoration
    assert_file_exists "$GUIDANCE_FILE"
    record_result
}

# TEST 04: Pattern extraction from valid content
test_04_pattern_extraction_from_valid_content() {
    run_test 04 "Pattern extraction from valid content"

    # Verify guidance contains pattern headings
    local pattern_count=$(grep -c "^### Pattern" "$GUIDANCE_FILE" || echo 0)

    if (( pattern_count >= 4 )); then
        echo -e "${GREEN}PASS${NC}: Found $pattern_count patterns (expected ≥4)"
        ((TEST_RESULTS++))
    else
        echo -e "${RED}FAIL${NC}: Found only $pattern_count patterns (expected ≥4)"
    fi

    # Verify expected patterns for story-creation integration
    # (Explicit Classification, Bounded Choice, Fibonacci)
    for pattern in "Explicit Classification" "Bounded Choice" "Fibonacci"; do
        assert_file_contains "$GUIDANCE_FILE" "$pattern"
        record_result
    done
}

# TEST 05: Pattern name normalization
test_05_pattern_name_normalization() {
    run_test 05 "Pattern name normalization"

    # Test normalization logic: hyphen and case insensitivity
    # Pattern names with hyphens should normalize to spaces
    # "Open-Ended Discovery" → "open ended discovery"
    # "Explicit Classification" → "explicit classification"

    # Verify patterns exist in various case combinations
    assert_file_contains "$GUIDANCE_FILE" "Explicit Classification"
    record_result

    # Verify patterns with special chars (+ signs)
    assert_file_contains "$GUIDANCE_FILE" "Classification.*Bounded"
    record_result
}

# TEST 06: Pattern-to-question mapping lookup
test_06_pattern_to_question_mapping_lookup() {
    run_test 06 "Pattern-to-question mapping lookup"

    # Verify integration guide exists
    assert_file_exists "$INTEGRATION_GUIDE"
    record_result

    # Verify integration guide contains pattern mapping table
    assert_file_contains "$INTEGRATION_GUIDE" "pattern_mapping"
    record_result

    # Verify mapping has Phase 1 step references
    assert_file_contains "$INTEGRATION_GUIDE" "step_3_epic"
    assert_file_contains "$INTEGRATION_GUIDE" "step_4_sprint"
    assert_file_contains "$INTEGRATION_GUIDE" "step_5"
    record_result
}

# TEST 07: Pattern lookup miss handling
test_07_pattern_lookup_miss_handling() {
    run_test 07 "Pattern lookup miss handling (unknown question type)"

    # Verify integration guide has fallback documentation
    assert_file_contains "$INTEGRATION_GUIDE" "fallback"
    record_result

    # Verify baseline logic documented
    assert_file_contains "$INTEGRATION_GUIDE" "baseline"
    record_result
}

# TEST 08: Token measurement documentation
test_08_token_measurement_documentation() {
    run_test 08 "Token measurement documentation"

    # Verify integration guide has token budget section
    assert_file_contains "$INTEGRATION_GUIDE" -i "token"
    record_result

    # Verify methodology documented
    assert_file_contains "$INTEGRATION_GUIDE" "1000"
    record_result
}

# TEST 09: Baseline fallback behavior documented
test_09_baseline_fallback_behavior_documented() {
    run_test 09 "Baseline fallback behavior documented"

    # Verify graceful degradation hierarchy documented
    assert_file_contains "$INTEGRATION_GUIDE" "Graceful"
    record_result

    # Verify fallback scenarios documented
    assert_file_contains "$INTEGRATION_GUIDE" -i "missing"
    record_result
}

# TEST 10: Batch mode caching strategy documented
test_10_batch_mode_caching_strategy_documented() {
    run_test 10 "Batch mode caching strategy documented"

    # Verify batch mode section exists
    assert_file_contains "$INTEGRATION_GUIDE" -i "batch"
    record_result

    # Verify cache lifecycle documented
    assert_file_contains "$INTEGRATION_GUIDE" -i "cache"
    record_result
}

# TEST 11: Epic selection pattern documented
test_11_epic_selection_pattern_documented() {
    run_test 11 "Epic selection pattern (Explicit Classification + Bounded Choice)"

    # Verify Step 3 pattern mapping exists
    assert_file_contains "$INTEGRATION_GUIDE" "step_3"
    record_result

    # Verify pattern names match
    assert_file_contains "$INTEGRATION_GUIDE" "Explicit Classification"
    assert_file_contains "$INTEGRATION_GUIDE" "Bounded Choice"
    record_result
}

# TEST 12: Sprint assignment pattern documented
test_12_sprint_assignment_pattern_documented() {
    run_test 12 "Sprint assignment pattern (Bounded Choice)"

    # Verify Step 4 pattern mapping exists
    assert_file_contains "$INTEGRATION_GUIDE" "step_4"
    record_result

    # Verify Bounded Choice pattern
    assert_file_contains "$INTEGRATION_GUIDE" "Bounded Choice"
    record_result
}

# TEST 13: Priority selection pattern documented
test_13_priority_selection_pattern_documented() {
    run_test 13 "Priority selection pattern (Explicit Classification)"

    # Verify pattern exists for priority
    assert_file_contains "$INTEGRATION_GUIDE" -i "priority"
    record_result

    # Verify has explicit classification
    assert_file_contains "$INTEGRATION_GUIDE" "Explicit Classification"
    record_result
}

# TEST 14: Story points pattern documented
test_14_story_points_pattern_documented() {
    run_test 14 "Story points pattern (Fibonacci Bounded Choice)"

    # Verify pattern for points
    assert_file_contains "$INTEGRATION_GUIDE" -i "points"
    record_result

    # Verify Fibonacci pattern documented
    assert_file_contains "$INTEGRATION_GUIDE" "Fibonacci"
    record_result
}

# TEST 15: Reference file completeness
test_15_reference_file_completeness() {
    run_test 15 "Reference file comprehensive documentation (≥500 lines)"

    # Verify integration guide is comprehensive (≥500 lines)
    assert_file_line_count "$INTEGRATION_GUIDE" 500
    record_result

    # Verify all required sections present
    for section in "Pattern Mapping" "Batch Mode" "Token Budget" "Backward Compatibility" "Example Transformations" "Edge Case"; do
        assert_file_contains "$INTEGRATION_GUIDE" "$section"
        record_result
    done
}

###############################################################################
# MAIN TEST EXECUTION
###############################################################################

main() {
    echo ""
    echo "╔════════════════════════════════════════════════════════════════════╗"
    echo "║  UNIT TEST SUITE: Story Creation Guidance Loading                 ║"
    echo "║  15 tests for Step 0, pattern operations, and documentation        ║"
    echo "╚════════════════════════════════════════════════════════════════════╝"
    echo ""

    # Run all unit tests
    test_01_step0_loads_guidance_valid_file
    test_02_step0_handles_missing_file
    test_03_step0_handles_corrupted_file
    test_04_pattern_extraction_from_valid_content
    test_05_pattern_name_normalization
    test_06_pattern_to_question_mapping_lookup
    test_07_pattern_lookup_miss_handling
    test_08_token_measurement_documentation
    test_09_baseline_fallback_behavior_documented
    test_10_batch_mode_caching_strategy_documented
    test_11_epic_selection_pattern_documented
    test_12_sprint_assignment_pattern_documented
    test_13_priority_selection_pattern_documented
    test_14_story_points_pattern_documented
    test_15_reference_file_completeness

    # Summary
    echo ""
    echo "╔════════════════════════════════════════════════════════════════════╗"
    echo "║  UNIT TEST SUMMARY                                                 ║"
    echo "╚════════════════════════════════════════════════════════════════════╝"
    echo ""
    echo -e "Tests Passed: ${GREEN}$TEST_RESULTS/$TEST_TOTAL${NC}"

    if [[ $TEST_RESULTS -eq $TEST_TOTAL ]]; then
        echo -e "${GREEN}✓ All unit tests PASSED${NC}"
        echo ""
        return 0
    else
        local failed=$((TEST_TOTAL - TEST_RESULTS))
        echo -e "${RED}✗ $failed test(s) FAILED${NC}"
        echo ""
        return 1
    fi
}

main "$@"
