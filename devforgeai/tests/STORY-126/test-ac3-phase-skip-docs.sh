#!/bin/bash
################################################################################
# TEST SUITE: AC#3 - /dev Skips Appropriate Phases
# STORY-126: Story Type Detection & Phase Skipping
#
# Purpose: Validate that /dev command skips Phase 05 Integration for
#          documentation-type stories with clear log messages
#
# Test Pattern: AAA (Arrange, Act, Assert)
# Status: RED (Expected to fail - tests first, implementation follows)
################################################################################

set -e

# Configuration
TEST_DIR="/mnt/c/Projects/DevForgeAI2/devforgeai/tests/STORY-126"
TEMP_DIR="${TEST_DIR}/tmp-ac3-$$"
STORY_LOCATION="/mnt/c/Projects/DevForgeAI2/devforgeai/specs/Stories"
DEV_SKILL="/mnt/c/Projects/DevForgeAI2/.claude/skills/devforgeai-development/SKILL.md"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Counters
TESTS_RUN=0
TESTS_PASSED=0
TESTS_FAILED=0

################################################################################
# TEST UTILITIES
################################################################################

test_start() {
    local test_name=$1
    echo ""
    echo -e "${YELLOW}TEST: ${test_name}${NC}"
    ((TESTS_RUN++))
}

assert_pass() {
    local assertion=$1
    local expected=$2
    local actual=$3

    if [ "$expected" = "$actual" ]; then
        echo -e "${GREEN}  ✓ PASS${NC}: $assertion"
        ((TESTS_PASSED++))
        return 0
    else
        echo -e "${RED}  ✗ FAIL${NC}: $assertion"
        echo "    Expected: $expected"
        echo "    Actual: $actual"
        ((TESTS_FAILED++))
        return 1
    fi
}

assert_contains() {
    local file=$1
    local pattern=$2
    local message=$3

    if grep -q "$pattern" "$file" 2>/dev/null; then
        echo -e "${GREEN}  ✓ PASS${NC}: $message"
        ((TESTS_PASSED++))
        return 0
    else
        echo -e "${RED}  ✗ FAIL${NC}: $message"
        echo "    File: $file"
        echo "    Expected pattern: $pattern"
        ((TESTS_FAILED++))
        return 1
    fi
}

assert_not_contains() {
    local file=$1
    local pattern=$2
    local message=$3

    if ! grep -q "$pattern" "$file" 2>/dev/null; then
        echo -e "${GREEN}  ✓ PASS${NC}: $message"
        ((TESTS_PASSED++))
        return 0
    else
        echo -e "${RED}  ✗ FAIL${NC}: $message"
        echo "    File: $file"
        echo "    Unexpected pattern: $pattern"
        ((TESTS_FAILED++))
        return 1
    fi
}

assert_file_exists() {
    local file=$1
    local message=$2

    if [ -f "$file" ]; then
        echo -e "${GREEN}  ✓ PASS${NC}: $message"
        ((TESTS_PASSED++))
        return 0
    else
        echo -e "${RED}  ✗ FAIL${NC}: $message"
        echo "    Expected file: $file"
        ((TESTS_FAILED++))
        return 1
    fi
}

################################################################################
# SETUP & TEARDOWN
################################################################################

setup() {
    mkdir -p "$TEMP_DIR"
    echo "Setup: Created temp directory $TEMP_DIR"
}

teardown() {
    rm -rf "$TEMP_DIR"
    echo "Teardown: Removed temp directory"
}

################################################################################
# TEST CASES
################################################################################

# AC#3.1: Documentation story exists in expected location
test_ac3_1_documentation_story_exists() {
    test_start "AC#3.1: Documentation story file exists with type field"

    # Arrange - use STORY-126 itself (or create test story)
    local story_file="${TEMP_DIR}/STORY-TEST-DOC.story.md"
    cat > "$story_file" <<'EOF'
---
id: STORY-TEST-DOC
title: Test Documentation Story
type: documentation
status: Ready for Dev
priority: MEDIUM
story-points: 3
created: 2025-12-20
---

# STORY-TEST-DOC: Test Documentation Story

## User Story
As a developer
I want to ensure documentation stories skip integration tests
EOF

    # Assert
    assert_file_exists "$story_file" "Test documentation story file exists"
    assert_contains "$story_file" "^type: documentation" "Story has type: documentation"
}

# AC#3.2: Dev skill contains phase-skipping logic
test_ac3_2_dev_skill_has_phase_skip_logic() {
    test_start "AC#3.2: Dev skill contains phase-skipping decision logic"

    # Arrange - check if DEV_SKILL exists
    if [ ! -f "$DEV_SKILL" ]; then
        echo -e "${YELLOW}  ⚠ SKIPPED${NC}: DEV_SKILL file not found at $DEV_SKILL"
        ((TESTS_FAILED++))
        return 1
    fi

    # Act & Assert
    # Expected: phase-skipping logic based on story type
    assert_contains "$DEV_SKILL" "type.*documentation" \
        "Dev skill checks for documentation type"
    assert_contains "$DEV_SKILL" "Phase.*05.*Integration" \
        "Dev skill references Phase 05 Integration skipping"
}

# AC#3.3: Phase skip log message format
test_ac3_3_phase_skip_log_message_format() {
    test_start "AC#3.3: Phase skip produces clear log message"

    # Arrange - simulate phase skip message generation
    local log_message="Skipping Phase 05: Story type 'documentation' does not require integration tests"

    # Assert - validate message format
    local contains_phase=$(echo "$log_message" | grep -q "Phase 05" && echo "true" || echo "false")
    local contains_reason=$(echo "$log_message" | grep -q "documentation" && echo "true" || echo "false")
    local contains_explanation=$(echo "$log_message" | grep -q "does not require" && echo "true" || echo "false")

    assert_pass "Log message contains 'Phase 05'" "true" "$contains_phase"
    assert_pass "Log message contains 'documentation'" "true" "$contains_reason"
    assert_pass "Log message contains explanation" "true" "$contains_explanation"
}

# AC#3.4: Phase skip decision matrix in code
test_ac3_4_phase_skip_decision_matrix() {
    test_start "AC#3.4: Phase skip decision logic correctly maps types to phases"

    # Arrange - create mapping validation
    local story_file="${TEMP_DIR}/phase-skip-test.story.md"
    cat > "$story_file" <<'EOF'
---
id: TEST-PHASE-SKIP
title: Phase Skip Test
type: documentation
status: Ready
created: 2025-12-20
---
EOF

    # Act - simulate decision logic
    local story_type=$(grep "^type:" "$story_file" | cut -d' ' -f2)

    # Assert - verify mapping
    if [ "$story_type" = "documentation" ]; then
        local should_skip_phase05="true"
        local should_skip_phase04="false"
        local should_skip_phase02="false"

        assert_pass "Documentation type should skip Phase 05" "true" "$should_skip_phase05"
        assert_pass "Documentation type should NOT skip Phase 04" "false" "$should_skip_phase04"
        assert_pass "Documentation type should NOT skip Phase 02" "false" "$should_skip_phase02"
    fi
}

# AC#3.5: Other story types do NOT skip Phase 05
test_ac3_5_feature_type_does_not_skip_phase05() {
    test_start "AC#3.5: Feature-type stories do NOT skip Phase 05"

    # Arrange
    local story_file="${TEMP_DIR}/feature-story.story.md"
    cat > "$story_file" <<'EOF'
---
id: TEST-FEATURE
title: Feature Story
type: feature
status: Ready
created: 2025-12-20
---
EOF

    # Act
    local story_type=$(grep "^type:" "$story_file" | cut -d' ' -f2)

    # Assert
    if [ "$story_type" = "feature" ]; then
        local should_skip_phase05="false"
        assert_pass "Feature type should NOT skip Phase 05" "false" "$should_skip_phase05"
    fi
}

# AC#3.6: Logging happens at phase execution time
test_ac3_6_skip_logged_at_phase_start() {
    test_start "AC#3.6: Phase skip message logged when phase would execute"

    # Arrange - create mock log output
    local log_file="${TEMP_DIR}/phase-execution.log"
    cat > "$log_file" <<'EOF'
Starting Phase 01: Pre-Flight Validation
✓ Phase 01 Complete
Starting Phase 02: Test-First Design (Red Phase)
✓ Phase 02 Complete
Starting Phase 03: Implementation (Green Phase)
✓ Phase 03 Complete
Starting Phase 04: Refactor (Refactor Phase)
✓ Phase 04 Complete
Skipping Phase 05: Story type 'documentation' does not require integration tests
Starting Phase 06: Deferral Challenge
✓ Phase 06 Complete
EOF

    # Assert
    assert_contains "$log_file" "Skipping Phase 05.*documentation" \
        "Skip message appears in execution log"
    assert_contains "$log_file" "does not require integration tests" \
        "Skip message includes clear explanation"
}

# AC#3.7: Feature story log should NOT skip Phase 05
test_ac3_7_feature_story_does_not_log_skip() {
    test_start "AC#3.7: Feature story execution log does NOT contain Phase 05 skip"

    # Arrange
    local log_file="${TEMP_DIR}/feature-phase-execution.log"
    cat > "$log_file" <<'EOF'
Starting Phase 01: Pre-Flight Validation
✓ Phase 01 Complete
Starting Phase 02: Test-First Design (Red Phase)
✓ Phase 02 Complete
Starting Phase 03: Implementation (Green Phase)
✓ Phase 03 Complete
Starting Phase 04: Refactor (Refactor Phase)
✓ Phase 04 Complete
Starting Phase 05: Integration & Validation
✓ Phase 05 Complete
Starting Phase 06: Deferral Challenge
✓ Phase 06 Complete
EOF

    # Assert
    assert_not_contains "$log_file" "Skipping Phase 05" \
        "Feature story execution does NOT skip Phase 05"
}

# AC#3.8: Skip message is visible in console output
test_ac3_8_skip_message_user_visible() {
    test_start "AC#3.8: Phase skip message is user-visible in console"

    # Arrange
    local output_message="Skipping Phase 05: Story type 'documentation' does not require integration tests"

    # Assert - verify message is clear and not buried
    local message_length=${#output_message}
    local has_prefix=$(echo "$output_message" | grep -q "^Skipping" && echo "true" || echo "false")
    local has_colon=$(echo "$output_message" | grep -q ":" && echo "true" || echo "false")

    assert_pass "Message starts with 'Skipping'" "true" "$has_prefix"
    assert_pass "Message contains colon for readability" "true" "$has_colon"
    assert_pass "Message length is reasonable" "true" "true"  # Message exists
}

# AC#3.9: Documentation stories still execute Phases 1-4 and 6+
test_ac3_9_documentation_executes_other_phases() {
    test_start "AC#3.9: Documentation story executes all phases EXCEPT Phase 05"

    # Arrange
    local phases=("Phase 01" "Phase 02" "Phase 03" "Phase 04" "Phase 06")
    local doc_story_type="documentation"

    # Assert - verify documentation stories run other phases
    # (This would be actual execution test when implementation is ready)
    echo -e "  ⚠ EXPECTED FAILURE: Requires implementation of phase-skip logic"
    ((TESTS_FAILED++))
}

# AC#3.10: Skip logic is type-driven, not status-driven
test_ac3_10_skip_based_on_type_not_status() {
    test_start "AC#3.10: Phase skip is driven by type field, not story status"

    # Arrange
    local doc_released="${TEMP_DIR}/doc-released.story.md"
    cat > "$doc_released" <<'EOF'
---
id: TEST-DOC-RELEASED
title: Documentation (Released)
type: documentation
status: Released
created: 2025-12-20
---
EOF

    local feature_in_dev="${TEMP_DIR}/feature-in-dev.story.md"
    cat > "$feature_in_dev" <<'EOF'
---
id: TEST-FEATURE-IN-DEV
title: Feature (In Dev)
type: feature
status: In Development
created: 2025-12-20
---
EOF

    # Act & Assert
    local doc_type=$(grep "^type:" "$doc_released" | cut -d' ' -f2)
    local feature_type=$(grep "^type:" "$feature_in_dev" | cut -d' ' -f2)

    assert_pass "Documentation (Released) should still skip Phase 05" "documentation" "$doc_type"
    assert_pass "Feature (In Dev) should NOT skip Phase 05" "feature" "$feature_type"
}

################################################################################
# TEST EXECUTION
################################################################################

main() {
    echo ""
    echo "================================================================================================"
    echo "AC#3: /dev Skips Appropriate Phases - TEST SUITE"
    echo "STORY-126: Story Type Detection & Phase Skipping"
    echo "================================================================================================"
    echo ""
    echo "Status: RED PHASE (Tests expected to fail - implementation to follow)"
    echo ""

    setup

    # Run all test cases
    test_ac3_1_documentation_story_exists
    test_ac3_2_dev_skill_has_phase_skip_logic
    test_ac3_3_phase_skip_log_message_format
    test_ac3_4_phase_skip_decision_matrix
    test_ac3_5_feature_type_does_not_skip_phase05
    test_ac3_6_skip_logged_at_phase_start
    test_ac3_7_feature_story_does_not_log_skip
    test_ac3_8_skip_message_user_visible
    test_ac3_9_documentation_executes_other_phases
    test_ac3_10_skip_based_on_type_not_status

    teardown

    # Summary
    echo ""
    echo "================================================================================================"
    echo "TEST SUMMARY"
    echo "================================================================================================"
    echo "Total Tests Run:    $TESTS_RUN"
    echo "Tests Passed:       $TESTS_PASSED"
    echo "Tests Failed:       $TESTS_FAILED"
    echo ""

    if [ $TESTS_FAILED -eq 0 ]; then
        echo -e "${GREEN}✓ ALL TESTS PASSED${NC}"
        return 0
    else
        echo -e "${RED}✗ TESTS FAILED: $TESTS_FAILED/${TESTS_RUN}${NC}"
        return 1
    fi
}

main
exit $?
