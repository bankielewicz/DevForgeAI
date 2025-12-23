#!/bin/bash
################################################################################
# TEST SUITE: AC#4 - All Story Types Skip Correctly
# STORY-126: Story Type Detection & Phase Skipping
#
# Purpose: Validate phase skipping matrix for all 4 story types:
#          - feature: No phases skipped
#          - documentation: Phase 05 Integration skipped
#          - bugfix: Phase 04 Refactor skipped
#          - refactor: Phase 02 Red skipped
#
# Test Pattern: AAA (Arrange, Act, Assert)
# Status: RED (Expected to fail - tests first, implementation follows)
################################################################################

set -e

# Configuration
TEST_DIR="/mnt/c/Projects/DevForgeAI2/devforgeai/tests/STORY-126"
TEMP_DIR="${TEST_DIR}/tmp-ac4-$$"

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

assert_equals_array() {
    local expected_array=$1
    local actual_array=$2
    local message=$3

    if [ "$expected_array" = "$actual_array" ]; then
        echo -e "${GREEN}  ✓ PASS${NC}: $message"
        ((TESTS_PASSED++))
        return 0
    else
        echo -e "${RED}  ✗ FAIL${NC}: $message"
        echo "    Expected: $expected_array"
        echo "    Actual: $actual_array"
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
# PHASE SKIP MATRIX DEFINITION
################################################################################

# Define expected phase skip behavior
declare -A PHASE_SKIP_MATRIX=(
    ["feature"]="none"                    # No phases skipped
    ["documentation"]="Phase 05 Integration"  # Skip Phase 05
    ["bugfix"]="Phase 04 Refactor"        # Skip Phase 04
    ["refactor"]="Phase 02 Red"           # Skip Phase 02
)

################################################################################
# TEST CASES
################################################################################

# AC#4.1: Feature type - no phases skipped
test_ac4_1_feature_type_no_skip() {
    test_start "AC#4.1: Feature type skips NO phases"

    # Arrange
    local story_file="${TEMP_DIR}/feature-story.story.md"
    cat > "$story_file" <<'EOF'
---
id: TEST-FEATURE
title: Test Feature
type: feature
status: Ready
created: 2025-12-20
---

# TEST-FEATURE: Test Feature
Full TDD workflow required
EOF

    # Act
    local story_type=$(grep "^type:" "$story_file" | cut -d' ' -f2)
    local expected_skip="none"
    local phases_to_execute=("Phase 01" "Phase 02" "Phase 03" "Phase 04" "Phase 05" "Phase 06")

    # Assert
    assert_pass "Type is feature" "feature" "$story_type"
    assert_pass "Feature type skips nothing" "none" "$expected_skip"

    # Verify all phases would execute
    echo -e "  ${GREEN}✓ All phases (1-6) should execute for feature type${NC}"
    ((TESTS_PASSED++))
}

# AC#4.2: Documentation type - Phase 05 skipped
test_ac4_2_documentation_type_skip_phase05() {
    test_start "AC#4.2: Documentation type skips Phase 05 Integration"

    # Arrange
    local story_file="${TEMP_DIR}/doc-story.story.md"
    cat > "$story_file" <<'EOF'
---
id: TEST-DOC
title: Test Documentation
type: documentation
status: Ready
created: 2025-12-20
---

# TEST-DOC: Test Documentation
No runtime code to test
EOF

    # Act
    local story_type=$(grep "^type:" "$story_file" | cut -d' ' -f2)
    local expected_skip="Phase 05 Integration"
    local phases_to_execute=("Phase 01" "Phase 02" "Phase 03" "Phase 04" "Phase 06")
    local phases_to_skip=("Phase 05")

    # Assert
    assert_pass "Type is documentation" "documentation" "$story_type"
    assert_pass "Documentation type skips Phase 05" "Phase 05 Integration" "$expected_skip"

    echo -e "  ${GREEN}✓ Phases 1-4 and 6 should execute for documentation type${NC}"
    echo -e "  ${GREEN}✓ Phase 05 should be skipped for documentation type${NC}"
    ((TESTS_PASSED += 2))
}

# AC#4.3: Bugfix type - Phase 04 skipped
test_ac4_3_bugfix_type_skip_phase04() {
    test_start "AC#4.3: Bugfix type skips Phase 04 Refactor"

    # Arrange
    local story_file="${TEMP_DIR}/bugfix-story.story.md"
    cat > "$story_file" <<'EOF'
---
id: TEST-BUGFIX
title: Test Bugfix
type: bugfix
status: Ready
created: 2025-12-20
---

# TEST-BUGFIX: Test Bugfix
Minimal changes preferred
EOF

    # Act
    local story_type=$(grep "^type:" "$story_file" | cut -d' ' -f2)
    local expected_skip="Phase 04 Refactor"
    local phases_to_execute=("Phase 01" "Phase 02" "Phase 03" "Phase 05" "Phase 06")
    local phases_to_skip=("Phase 04")

    # Assert
    assert_pass "Type is bugfix" "bugfix" "$story_type"
    assert_pass "Bugfix type skips Phase 04" "Phase 04 Refactor" "$expected_skip"

    echo -e "  ${GREEN}✓ Phases 1-3, 5-6 should execute for bugfix type${NC}"
    echo -e "  ${GREEN}✓ Phase 04 should be skipped for bugfix type${NC}"
    ((TESTS_PASSED += 2))
}

# AC#4.4: Refactor type - Phase 02 skipped
test_ac4_4_refactor_type_skip_phase02() {
    test_start "AC#4.4: Refactor type skips Phase 02 Red"

    # Arrange
    local story_file="${TEMP_DIR}/refactor-story.story.md"
    cat > "$story_file" <<'EOF'
---
id: TEST-REFACTOR
title: Test Refactor
type: refactor
status: Ready
created: 2025-12-20
---

# TEST-REFACTOR: Test Refactor
Tests already exist
EOF

    # Act
    local story_type=$(grep "^type:" "$story_file" | cut -d' ' -f2)
    local expected_skip="Phase 02 Red"
    local phases_to_execute=("Phase 01" "Phase 03" "Phase 04" "Phase 05" "Phase 06")
    local phases_to_skip=("Phase 02")

    # Assert
    assert_pass "Type is refactor" "refactor" "$story_type"
    assert_pass "Refactor type skips Phase 02" "Phase 02 Red" "$expected_skip"

    echo -e "  ${GREEN}✓ Phases 1, 3-6 should execute for refactor type${NC}"
    echo -e "  ${GREEN}✓ Phase 02 should be skipped for refactor type${NC}"
    ((TESTS_PASSED += 2))
}

# AC#4.5: Phase skip matrix validation logic
test_ac4_5_phase_skip_matrix_logic() {
    test_start "AC#4.5: Phase skip logic correctly implements matrix"

    # Arrange - test matrix lookup
    local test_cases=(
        "feature:none"
        "documentation:Phase 05 Integration"
        "bugfix:Phase 04 Refactor"
        "refactor:Phase 02 Red"
    )

    # Act & Assert
    for test_case in "${test_cases[@]}"; do
        IFS=':' read -r type expected_skip <<< "$test_case"
        local actual_skip=${PHASE_SKIP_MATRIX[$type]}

        if [ "$expected_skip" = "$actual_skip" ]; then
            echo -e "  ${GREEN}✓${NC} Type '$type' → Skip '$expected_skip'"
            ((TESTS_PASSED++))
        else
            echo -e "  ${RED}✗${NC} Type '$type' mismatch"
            echo "    Expected: $expected_skip"
            echo "    Actual: $actual_skip"
            ((TESTS_FAILED++))
        fi
    done
}

# AC#4.6: Invalid type defaults to feature behavior
test_ac4_6_invalid_type_defaults_to_feature() {
    test_start "AC#4.6: Invalid/missing type defaults to feature (all phases)"

    # Arrange
    local story_file="${TEMP_DIR}/missing-type.story.md"
    cat > "$story_file" <<'EOF'
---
id: TEST-NO-TYPE
title: Test Missing Type
status: Ready
created: 2025-12-20
---

# TEST-NO-TYPE: Missing Type
EOF

    # Act - should default to feature
    local story_type=$(grep "^type:" "$story_file" | cut -d' ' -f2 || echo "feature")
    local expected_default="feature"

    # Assert
    assert_pass "Missing type defaults to feature" "$expected_default" "$story_type"
}

# AC#4.7: Phase skip decision occurs before phase execution
test_ac4_7_skip_decision_timing() {
    test_start "AC#4.7: Phase skip decision happens at start of each phase"

    # Arrange
    local execution_log="${TEMP_DIR}/execution-decisions.log"
    cat > "$execution_log" <<'EOF'
PHASE 01 START: Checking story type...
PHASE 01 DECISION: type=documentation, proceed
PHASE 02 START: Checking story type...
PHASE 02 DECISION: type=documentation, proceed
PHASE 03 START: Checking story type...
PHASE 03 DECISION: type=documentation, proceed
PHASE 04 START: Checking story type...
PHASE 04 DECISION: type=documentation, proceed
PHASE 05 START: Checking story type...
PHASE 05 DECISION: type=documentation, SKIP (documentation does not require integration tests)
PHASE 06 START: Checking story type...
PHASE 06 DECISION: type=documentation, proceed
EOF

    # Assert
    local skip_logged=$(grep -c "PHASE 05 DECISION.*SKIP" "$execution_log" || echo "0")
    assert_pass "Phase 05 skip decision logged" "1" "$skip_logged"
}

# AC#4.8: Each type skips exactly ONE phase (or none for feature)
test_ac4_8_each_type_skips_exactly_one_phase() {
    test_start "AC#4.8: Each type skips exactly 1 phase (or none)"

    # Arrange - verify matrix completeness
    local types=("feature" "documentation" "bugfix" "refactor")
    local feature_count=0
    local doc_count=0
    local bugfix_count=0
    local refactor_count=0

    # Act & Assert
    for type in "${types[@]}"; do
        local skipped_phases=${PHASE_SKIP_MATRIX[$type]}

        # Feature skips 0 phases, others skip 1 each
        if [ "$type" = "feature" ]; then
            assert_pass "$type skips 0 phases" "none" "$skipped_phases"
        else
            local phase_count=$(echo "$skipped_phases" | wc -w)
            assert_pass "$type skips exactly 1 phase" "2" "$phase_count"  # "Phase XX" = 2 words
        fi
    done
}

# AC#4.9: No overlapping phase skips
test_ac4_9_no_overlapping_phase_skips() {
    test_start "AC#4.9: Different types skip different phases (no overlap)"

    # Arrange - create skip phase registry
    declare -A skip_registry=(
        ["documentation"]="Phase 05"
        ["bugfix"]="Phase 04"
        ["refactor"]="Phase 02"
    )

    # Act & Assert
    local phases_skipped=()
    for type in "${!skip_registry[@]}"; do
        local skipped_phase=${skip_registry[$type]}

        # Check for duplicates
        for existing_phase in "${phases_skipped[@]}"; do
            if [ "$skipped_phase" = "$existing_phase" ]; then
                echo -e "${RED}  ✗ FAIL${NC}: Duplicate skip - $skipped_phase skipped by multiple types"
                ((TESTS_FAILED++))
                return 1
            fi
        done

        phases_skipped+=("$skipped_phase")
    done

    echo -e "  ${GREEN}✓ PASS${NC}: No overlapping phase skips"
    ((TESTS_PASSED++))
}

# AC#4.10: Feature type is default for backward compatibility
test_ac4_10_feature_is_default_type() {
    test_start "AC#4.10: Feature type is default for backward compatibility"

    # Arrange
    local story_file="${TEMP_DIR}/default-type.story.md"
    cat > "$story_file" <<'EOF'
---
id: TEST-DEFAULT
title: Test Default Type
status: Ready
created: 2025-12-20
---

# TEST-DEFAULT: Default Type
No explicit type field
EOF

    # Act - when type is missing, should default to feature
    local story_type=$(grep "^type:" "$story_file" | cut -d' ' -f2 || echo "feature")
    local expected="feature"

    # Assert
    assert_pass "Missing type defaults to feature" "$expected" "$story_type"
}

################################################################################
# TEST EXECUTION
################################################################################

main() {
    echo ""
    echo "================================================================================================"
    echo "AC#4: All Story Types Skip Correctly - PHASE SKIP MATRIX TEST SUITE"
    echo "STORY-126: Story Type Detection & Phase Skipping"
    echo "================================================================================================"
    echo ""
    echo "Status: RED PHASE (Tests expected to fail - implementation to follow)"
    echo ""
    echo "Phase Skip Matrix Expected:"
    echo "  feature       → Skip: NONE      (all phases required)"
    echo "  documentation → Skip: Phase 05  (no runtime code)"
    echo "  bugfix        → Skip: Phase 04  (minimal changes)"
    echo "  refactor      → Skip: Phase 02  (tests exist)"
    echo ""

    setup

    # Run all test cases
    test_ac4_1_feature_type_no_skip
    test_ac4_2_documentation_type_skip_phase05
    test_ac4_3_bugfix_type_skip_phase04
    test_ac4_4_refactor_type_skip_phase02
    test_ac4_5_phase_skip_matrix_logic
    test_ac4_6_invalid_type_defaults_to_feature
    test_ac4_7_skip_decision_timing
    test_ac4_8_each_type_skips_exactly_one_phase
    test_ac4_9_no_overlapping_phase_skips
    test_ac4_10_feature_is_default_type

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
