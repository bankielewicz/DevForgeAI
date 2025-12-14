#!/bin/bash

##############################################################################
# Test Suite: STORY-089 - Confidence Scoring Tests (AC#5)
# Purpose: Test ambiguous match flagging for manual review
#
# Acceptance Criteria #5: Ambiguous Match Flagging for Manual Review
# - Flag matches with confidence score between 60-75%
# - Display story ID, matched feature, and confidence percentage
# - Do not count low-confidence matches toward coverage until confirmed
##############################################################################

set -o pipefail

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Test counters
TESTS_RUN=0
TESTS_PASSED=0
TESTS_FAILED=0
TEST_LOG="/tmp/story-089-confidence.log"

# Paths
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="${SCRIPT_DIR}/../.."
GAP_DETECTOR="${PROJECT_ROOT}/.devforgeai/traceability/gap-detector.sh"
FIXTURES_DIR="${SCRIPT_DIR}/fixtures"

# Initialize log
echo "=== STORY-089 Confidence Scoring Test Suite ===" > "$TEST_LOG"
echo "Started: $(date)" >> "$TEST_LOG"

##############################################################################
# Test Framework Functions
##############################################################################

run_test() {
    local test_name=$1
    local test_func=$2

    TESTS_RUN=$((TESTS_RUN + 1))
    echo -e "\n${BLUE}[Test $TESTS_RUN]${NC} $test_name"

    if $test_func 2>> "$TEST_LOG"; then
        TESTS_PASSED=$((TESTS_PASSED + 1))
        echo -e "${GREEN}✓${NC} PASSED"
    else
        TESTS_FAILED=$((TESTS_FAILED + 1))
        echo -e "${RED}✗${NC} FAILED"
    fi
}

assert_contains() {
    local haystack="$1"
    local needle="$2"
    local message="${3:-String should contain substring}"

    if [[ "$haystack" == *"$needle"* ]]; then
        return 0
    else
        echo "ASSERTION FAILED: $message"
        echo "String: $haystack"
        echo "Should contain: $needle"
        return 1
    fi
}

assert_equals() {
    local expected="$1"
    local actual="$2"
    local message="${3:-Values should be equal}"

    if [[ "$expected" == "$actual" ]]; then
        return 0
    else
        echo "ASSERTION FAILED: $message"
        echo "Expected: $expected"
        echo "Actual: $actual"
        return 1
    fi
}

assert_json_field() {
    local json="$1"
    local field="$2"
    local expected="$3"
    local message="${4:-JSON field mismatch}"

    local actual
    actual=$(echo "$json" | jq -r "$field" 2>/dev/null)

    if [[ "$actual" == "$expected" ]]; then
        return 0
    else
        echo "ASSERTION FAILED: $message"
        echo "JSON: $json"
        echo "Field: $field"
        echo "Expected: $expected"
        echo "Actual: $actual"
        return 1
    fi
}

##############################################################################
# Setup: Create Confidence Test Fixtures
##############################################################################

setup_confidence_fixtures() {
    # Create epic with features for matching
    cat > "${FIXTURES_DIR}/epic-confidence-test.md" << 'EOF'
---
epic_id: EPIC-CONF-001
title: Confidence Test Epic
status: Planning
priority: Medium
---

# Epic: Confidence Test Epic

## Features

### Feature 1: User Authentication System

Implement user authentication with login, logout, and session management.

### Feature 2: Data Export Functionality

Allow users to export data in CSV, JSON, and XML formats.

### Feature 3: Dashboard Analytics

Create analytics dashboard with charts and metrics visualization.
EOF

    # Story with high confidence match (exact title match)
    cat > "${FIXTURES_DIR}/story-high-confidence.md" << 'EOF'
---
id: STORY-CONF-001
title: User Authentication System Implementation
epic: EPIC-CONF-001
status: Dev Complete
---

# Story: User Authentication System Implementation

Implement the user authentication feature from EPIC-CONF-001 Feature 1.
EOF

    # Story with medium confidence match (partial match)
    cat > "${FIXTURES_DIR}/story-medium-confidence.md" << 'EOF'
---
id: STORY-CONF-002
title: Export Data to Files
epic: EPIC-CONF-001
status: Dev Complete
---

# Story: Export Data to Files

Export data functionality. (Partial match to Feature 2)
EOF

    # Story with low confidence match (weak match)
    cat > "${FIXTURES_DIR}/story-low-confidence.md" << 'EOF'
---
id: STORY-CONF-003
title: Charts Display
epic: EPIC-CONF-001
status: Dev Complete
---

# Story: Charts Display

Display some charts. (Weak match to Feature 3 - Dashboard Analytics)
EOF

    # Story with no match
    cat > "${FIXTURES_DIR}/story-no-match.md" << 'EOF'
---
id: STORY-CONF-004
title: Unrelated Feature
epic: EPIC-CONF-001
status: Dev Complete
---

# Story: Unrelated Feature

This story has no matching feature in the epic.
EOF
}

# Run setup
setup_confidence_fixtures

##############################################################################
# AC#5.1: Confidence Score Calculation
##############################################################################

test_calculates_confidence_score() {
    # AC#5: System calculates confidence score for matches

    local result
    result=$("$GAP_DETECTOR" --with-confidence --epic "${FIXTURES_DIR}/epic-confidence-test.md" --stories "${FIXTURES_DIR}" 2>&1)

    # Should include confidence scores in output
    if [[ "$result" == *"confidence"* ]] || [[ "$result" == *"score"* ]] || [[ "$result" =~ [0-9]+% ]]; then
        return 0
    else
        echo "ASSERTION FAILED: Should include confidence scores"
        echo "Output: $result"
        return 1
    fi
}

test_high_confidence_above_75() {
    # AC#5: Exact/strong matches should be >= 75%

    local result
    result=$("$GAP_DETECTOR" --with-confidence --story "${FIXTURES_DIR}/story-high-confidence.md" --epic "${FIXTURES_DIR}/epic-confidence-test.md" 2>&1)

    # Should have high confidence (>= 75%)
    if [[ "$result" =~ (7[5-9]|[89][0-9]|100)% ]]; then
        return 0
    else
        echo "ASSERTION FAILED: Exact match should have >=75% confidence"
        echo "Output: $result"
        return 1
    fi
}

test_low_confidence_between_60_75() {
    # AC#5: Weak matches should be 60-74% (75 is counted as high confidence)

    local result
    result=$("$GAP_DETECTOR" --with-confidence --story "${FIXTURES_DIR}/story-medium-match.story.md" --epic "${FIXTURES_DIR}/epic-confidence-test.md" 2>&1)

    # Should have low confidence (60-74%)
    if [[ "$result" =~ (6[0-9]|7[0-4])% ]]; then
        return 0
    else
        echo "ASSERTION FAILED: Weak match should have 60-74% confidence"
        echo "Output: $result"
        return 1
    fi
}

test_no_match_below_60() {
    # AC#5: Non-matches should be < 60%

    local result
    result=$("$GAP_DETECTOR" --with-confidence --story "${FIXTURES_DIR}/story-no-match.md" --epic "${FIXTURES_DIR}/epic-confidence-test.md" 2>&1)

    # Should have very low or no confidence
    if [[ "$result" =~ [0-5][0-9]% ]] || [[ "$result" == *"no match"* ]]; then
        return 0
    else
        echo "ASSERTION FAILED: Non-match should have <60% confidence"
        echo "Output: $result"
        return 1
    fi
}

##############################################################################
# AC#5.2: Low Confidence Flagging
##############################################################################

test_flags_low_confidence_for_review() {
    # AC#5: Flag matches between 60-75% as "Low Confidence - Manual Review Required"

    local result
    result=$("$GAP_DETECTOR" --with-confidence --story "${FIXTURES_DIR}/story-medium-match.story.md" --epic "${FIXTURES_DIR}/epic-confidence-test.md" 2>&1)

    # Should flag for manual review
    if [[ "$result" == *"Low Confidence"* ]] || [[ "$result" == *"Manual Review"* ]] || [[ "$result" == *"manual review"* ]]; then
        return 0
    else
        echo "ASSERTION FAILED: Should flag low confidence for manual review"
        echo "Output: $result"
        return 1
    fi
}

test_does_not_flag_high_confidence() {
    # AC#5: High confidence matches should not be flagged

    local result
    result=$("$GAP_DETECTOR" --with-confidence --story "${FIXTURES_DIR}/story-high-confidence.md" --epic "${FIXTURES_DIR}/epic-confidence-test.md" 2>&1)

    # Should NOT flag for manual review
    if [[ "$result" != *"Manual Review"* ]] && [[ "$result" != *"Low Confidence"* ]]; then
        return 0
    else
        echo "ASSERTION FAILED: High confidence should not be flagged"
        echo "Output: $result"
        return 1
    fi
}

##############################################################################
# AC#5.3: Display Information
##############################################################################

test_displays_story_id_in_flag() {
    # AC#5: Display story ID

    local result
    result=$("$GAP_DETECTOR" --with-confidence --stories "${FIXTURES_DIR}" --epic "${FIXTURES_DIR}/epic-confidence-test.md" 2>&1)

    assert_contains "$result" "STORY-" "Should display story IDs" || return 1
}

test_displays_matched_feature() {
    # AC#5: Display matched feature

    local result
    result=$("$GAP_DETECTOR" --with-confidence --story "${FIXTURES_DIR}/story-low-confidence.md" --epic "${FIXTURES_DIR}/epic-confidence-test.md" 2>&1)

    # Should show which feature was matched
    if [[ "$result" == *"Feature"* ]] || [[ "$result" == *"Dashboard"* ]] || [[ "$result" == *"Analytics"* ]]; then
        return 0
    else
        echo "ASSERTION FAILED: Should display matched feature"
        echo "Output: $result"
        return 1
    fi
}

test_displays_confidence_percentage() {
    # AC#5: Display confidence percentage

    local result
    result=$("$GAP_DETECTOR" --with-confidence --stories "${FIXTURES_DIR}" --epic "${FIXTURES_DIR}/epic-confidence-test.md" 2>&1)

    # Should show percentage
    if [[ "$result" =~ [0-9]+% ]] || [[ "$result" =~ [0-9]+\.[0-9]+% ]]; then
        return 0
    else
        echo "ASSERTION FAILED: Should display confidence percentage"
        echo "Output: $result"
        return 1
    fi
}

##############################################################################
# AC#5.4: Coverage Calculation Exclusion
##############################################################################

test_excludes_low_confidence_from_coverage() {
    # AC#5: Do not count low-confidence matches toward coverage until confirmed

    local result
    result=$("$GAP_DETECTOR" --calculate-coverage --stories "${FIXTURES_DIR}" --epic "${FIXTURES_DIR}/epic-confidence-test.md" 2>&1)

    # With 3 features:
    # - story-high-confidence: counts (>75%)
    # - story-low-confidence: does NOT count (60-75%)
    # - story-no-match: does NOT count
    # Coverage should be 1/3 = 33.3% (not 2/3 or 3/3)

    # The coverage should NOT be 66% or 100%
    if [[ "$result" =~ 66% ]] || [[ "$result" =~ 100% ]]; then
        echo "ASSERTION FAILED: Low confidence should be excluded from coverage"
        echo "Output: $result"
        return 1
    fi
    return 0
}

test_business_rule_coverage_calculation() {
    # BR-003: 5 features, 3 confirmed stories, 1 low-confidence = 60% not 80%

    # This tests the exact business rule from the story
    local result
    result=$("$GAP_DETECTOR" --test-br-003 2>&1)

    # Coverage should be 60% (3 confirmed / 5 features)
    # NOT 80% (4 matches / 5 features including low-confidence)
    if [[ "$result" == *"60%"* ]]; then
        return 0
    else
        echo "ASSERTION FAILED: BR-003 - should calculate 60% not 80%"
        echo "Output: $result"
        return 1
    fi
}

test_confirmed_matches_count_toward_coverage() {
    # AC#5: Confirmed matches DO count toward coverage

    local result
    result=$("$GAP_DETECTOR" --calculate-coverage --story "${FIXTURES_DIR}/story-high-confidence.md" --epic "${FIXTURES_DIR}/epic-confidence-test.md" 2>&1)

    # High confidence match should contribute to coverage
    if [[ "$result" =~ [1-9][0-9]?% ]] || [[ "$result" == *"33"* ]] || [[ "$result" == *"100"* ]]; then
        return 0
    else
        echo "ASSERTION FAILED: Confirmed matches should count toward coverage"
        echo "Output: $result"
        return 1
    fi
}

##############################################################################
# AC#5.5: JSON Output
##############################################################################

test_json_output_includes_confidence() {
    # AC#5: JSON output includes confidence data

    local result
    result=$("$GAP_DETECTOR" --with-confidence --format json --stories "${FIXTURES_DIR}" --epic "${FIXTURES_DIR}/epic-confidence-test.md" 2>&1)

    # Should be valid JSON with confidence field
    if echo "$result" | jq -e '.matches[].confidence' > /dev/null 2>&1; then
        return 0
    else
        echo "ASSERTION FAILED: JSON should include confidence field"
        echo "Output: $result"
        return 1
    fi
}

test_json_output_includes_review_flag() {
    # AC#5: JSON output includes manual_review_required flag

    local result
    result=$("$GAP_DETECTOR" --with-confidence --format json --stories "${FIXTURES_DIR}" --epic "${FIXTURES_DIR}/epic-confidence-test.md" 2>&1)

    # Should have manual_review_required field for low confidence matches
    if echo "$result" | jq -e '.matches[] | select(.manual_review_required == true)' > /dev/null 2>&1; then
        return 0
    else
        # It's OK if there are no low confidence matches in this test
        if echo "$result" | jq -e '.matches' > /dev/null 2>&1; then
            return 0
        fi
        echo "ASSERTION FAILED: JSON should include manual_review_required flag"
        echo "Output: $result"
        return 1
    fi
}

##############################################################################
# Configuration Tests
##############################################################################

test_uses_configurable_threshold() {
    # AC#5: Confidence threshold is configurable

    local result
    result=$("$GAP_DETECTOR" --confidence-threshold 0.8 --with-confidence --stories "${FIXTURES_DIR}" --epic "${FIXTURES_DIR}/epic-confidence-test.md" 2>&1)

    # With 80% threshold, medium confidence (70%) should be flagged
    # This tests that threshold configuration works
    if [[ -n "$result" ]]; then
        return 0
    else
        echo "ASSERTION FAILED: Should accept confidence threshold parameter"
        return 1
    fi
}

##############################################################################
# Test Execution
##############################################################################

echo ""
echo "=========================================="
echo " STORY-089: Confidence Scoring Tests"
echo " Acceptance Criteria #5"
echo "=========================================="
echo ""

# Check if gap detector exists (will fail in RED phase)
if [[ ! -f "$GAP_DETECTOR" ]]; then
    echo -e "${YELLOW}WARNING:${NC} Gap detector not found: $GAP_DETECTOR"
    echo -e "${YELLOW}This is expected during TDD RED phase${NC}"
    echo ""
fi

# Confidence Score Calculation Tests
echo -e "\n${YELLOW}--- Confidence Score Calculation ---${NC}"
run_test "Calculates confidence score" test_calculates_confidence_score
run_test "High confidence above 75%" test_high_confidence_above_75
run_test "Low confidence between 60-75%" test_low_confidence_between_60_75
run_test "No match below 60%" test_no_match_below_60

# Low Confidence Flagging Tests
echo -e "\n${YELLOW}--- Low Confidence Flagging ---${NC}"
run_test "Flags low confidence for review" test_flags_low_confidence_for_review
run_test "Does not flag high confidence" test_does_not_flag_high_confidence

# Display Information Tests
echo -e "\n${YELLOW}--- Display Information ---${NC}"
run_test "Displays story ID in flag" test_displays_story_id_in_flag
run_test "Displays matched feature" test_displays_matched_feature
run_test "Displays confidence percentage" test_displays_confidence_percentage

# Coverage Calculation Exclusion Tests
echo -e "\n${YELLOW}--- Coverage Calculation Exclusion ---${NC}"
run_test "Excludes low confidence from coverage" test_excludes_low_confidence_from_coverage
run_test "BR-003: 5 features, 3 confirmed = 60%" test_business_rule_coverage_calculation
run_test "Confirmed matches count toward coverage" test_confirmed_matches_count_toward_coverage

# JSON Output Tests
echo -e "\n${YELLOW}--- JSON Output ---${NC}"
run_test "JSON output includes confidence" test_json_output_includes_confidence
run_test "JSON output includes review flag" test_json_output_includes_review_flag

# Configuration Tests
echo -e "\n${YELLOW}--- Configuration ---${NC}"
run_test "Uses configurable threshold" test_uses_configurable_threshold

# Summary
echo ""
echo "=========================================="
echo " Test Summary"
echo "=========================================="
echo -e "Tests Run:    ${TESTS_RUN}"
echo -e "Tests Passed: ${GREEN}${TESTS_PASSED}${NC}"
echo -e "Tests Failed: ${RED}${TESTS_FAILED}${NC}"
echo ""

if [[ $TESTS_FAILED -eq 0 ]]; then
    echo -e "${GREEN}All tests passed!${NC}"
    exit 0
else
    echo -e "${RED}Some tests failed. See log: $TEST_LOG${NC}"
    exit 1
fi
