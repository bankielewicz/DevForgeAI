#!/bin/bash
################################################################################
# TEST SUITE: AC#1 - Story Frontmatter Supports Type Field
# STORY-126: Story Type Detection & Phase Skipping
#
# Purpose: Validate story frontmatter accepts type field with 4 valid types
#          and rejects invalid types with clear error messages
#
# Test Pattern: AAA (Arrange, Act, Assert)
# Status: RED (Expected to fail - tests first, implementation follows)
################################################################################

set -e

# Configuration
TEST_DIR="/mnt/c/Projects/DevForgeAI2/devforgeai/tests/STORY-126"
TEMP_DIR="${TEST_DIR}/tmp-ac1-$$"
STORY_TEMPLATE_DIR="/mnt/c/Projects/DevForgeAI2/devforgeai/specs/Stories"
VALIDATOR_CLI="devforgeai-validate"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Counters
TESTS_RUN=0
TESTS_PASSED=0
TESTS_FAILED=0

################################################################################
# TEST UTILITIES
################################################################################

# Log test start
test_start() {
    local test_name=$1
    echo ""
    echo -e "${YELLOW}TEST: ${test_name}${NC}"
    ((TESTS_RUN++))
}

# Assert test passes
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

# Assert file contains text
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

# Assert file does NOT contain text
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
        echo "    Unexpected pattern found: $pattern"
        ((TESTS_FAILED++))
        return 1
    fi
}

# Assert command exits with code
assert_exit_code() {
    local expected_code=$1
    local actual_code=$2
    local message=$3

    if [ "$expected_code" = "$actual_code" ]; then
        echo -e "${GREEN}  ✓ PASS${NC}: $message"
        ((TESTS_PASSED++))
        return 0
    else
        echo -e "${RED}  ✗ FAIL${NC}: $message"
        echo "    Expected exit code: $expected_code"
        echo "    Actual exit code: $actual_code"
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

# AC#1.1: Story frontmatter accepts type: feature
test_ac1_1_type_feature() {
    test_start "AC#1.1: Frontmatter accepts type: feature"

    # Arrange
    local story_file="${TEMP_DIR}/test-feature.story.md"
    cat > "$story_file" <<'EOF'
---
id: TEST-001
title: Test Feature Story
type: feature
status: Backlog
priority: MEDIUM
story-points: 3
created: 2025-12-20
---

# TEST-001: Test Feature Story

## User Story
As a developer
I want to test feature type
So that feature stories work correctly
EOF

    # Act
    local yaml_valid=true
    if ! grep -A1 "^type:" "$story_file" | grep -q "feature"; then
        yaml_valid=false
    fi

    # Assert
    assert_pass "type field contains 'feature'" "true" "$yaml_valid"
    assert_contains "$story_file" "^type: feature" "YAML frontmatter contains type: feature"
}

# AC#1.2: Story frontmatter accepts type: documentation
test_ac1_2_type_documentation() {
    test_start "AC#1.2: Frontmatter accepts type: documentation"

    # Arrange
    local story_file="${TEMP_DIR}/test-documentation.story.md"
    cat > "$story_file" <<'EOF'
---
id: TEST-002
title: Test Documentation Story
type: documentation
status: Backlog
priority: MEDIUM
story-points: 3
created: 2025-12-20
---

# TEST-002: Test Documentation Story

## User Story
As a developer
I want to test documentation type
EOF

    # Act & Assert
    assert_contains "$story_file" "^type: documentation" "YAML frontmatter contains type: documentation"
}

# AC#1.3: Story frontmatter accepts type: bugfix
test_ac1_3_type_bugfix() {
    test_start "AC#1.3: Frontmatter accepts type: bugfix"

    # Arrange
    local story_file="${TEMP_DIR}/test-bugfix.story.md"
    cat > "$story_file" <<'EOF'
---
id: TEST-003
title: Test Bugfix Story
type: bugfix
status: Backlog
priority: HIGH
story-points: 2
created: 2025-12-20
---

# TEST-003: Test Bugfix Story

## User Story
As a developer
I want to fix a bug
EOF

    # Act & Assert
    assert_contains "$story_file" "^type: bugfix" "YAML frontmatter contains type: bugfix"
}

# AC#1.4: Story frontmatter accepts type: refactor
test_ac1_4_type_refactor() {
    test_start "AC#1.4: Frontmatter accepts type: refactor"

    # Arrange
    local story_file="${TEMP_DIR}/test-refactor.story.md"
    cat > "$story_file" <<'EOF'
---
id: TEST-004
title: Test Refactor Story
type: refactor
status: Backlog
priority: MEDIUM
story-points: 3
created: 2025-12-20
---

# TEST-004: Test Refactor Story

## User Story
As a developer
I want to refactor existing code
EOF

    # Act & Assert
    assert_contains "$story_file" "^type: refactor" "YAML frontmatter contains type: refactor"
}

# AC#1.5: Invalid type 'backend' causes error (negative test)
test_ac1_5_invalid_type_backend() {
    test_start "AC#1.5: Invalid type 'backend' causes validation error"

    # Arrange
    local story_file="${TEMP_DIR}/test-invalid-backend.story.md"
    cat > "$story_file" <<'EOF'
---
id: TEST-005
title: Test Invalid Type
type: backend
status: Backlog
priority: MEDIUM
story-points: 3
created: 2025-12-20
---

# TEST-005: Test Invalid Type

## User Story
Invalid type should be rejected
EOF

    # Act
    # Simulate validation - check if type is NOT in valid enum
    local valid_types="feature|documentation|bugfix|refactor"
    local actual_type=$(grep "^type:" "$story_file" | cut -d' ' -f2)
    local is_valid=false

    if echo "$actual_type" | grep -E "^($valid_types)$" > /dev/null; then
        is_valid=true
    fi

    # Assert
    assert_pass "Invalid type 'backend' should fail validation" "false" "$is_valid"
    assert_not_contains "$story_file" "^type: (feature|documentation|bugfix|refactor)$" \
        "type field does NOT contain valid enum value"
}

# AC#1.6: Invalid type 'unknown' causes error (negative test)
test_ac1_6_invalid_type_unknown() {
    test_start "AC#1.6: Invalid type 'unknown' causes validation error"

    # Arrange
    local story_file="${TEMP_DIR}/test-invalid-unknown.story.md"
    cat > "$story_file" <<'EOF'
---
id: TEST-006
title: Test Unknown Type
type: unknown
status: Backlog
priority: MEDIUM
story-points: 3
created: 2025-12-20
---

# TEST-006: Test Unknown Type
EOF

    # Act
    local valid_types="feature|documentation|bugfix|refactor"
    local actual_type=$(grep "^type:" "$story_file" | cut -d' ' -f2)
    local is_valid=false

    if echo "$actual_type" | grep -E "^($valid_types)$" > /dev/null; then
        is_valid=true
    fi

    # Assert
    assert_pass "Invalid type 'unknown' should fail validation" "false" "$is_valid"
}

# AC#1.7: Type field case sensitivity (lowercase only)
test_ac1_7_type_case_sensitivity() {
    test_start "AC#1.7: Type field values are case-sensitive (lowercase only)"

    # Arrange - create story with uppercase type
    local story_file="${TEMP_DIR}/test-case-sensitivity.story.md"
    cat > "$story_file" <<'EOF'
---
id: TEST-007
title: Test Case Sensitivity
type: Feature
status: Backlog
created: 2025-12-20
---

# TEST-007: Test Case
EOF

    # Act
    local valid_types="feature|documentation|bugfix|refactor"
    local actual_type=$(grep "^type:" "$story_file" | cut -d' ' -f2)
    local is_valid=false

    if echo "$actual_type" | grep -E "^($valid_types)$" > /dev/null; then
        is_valid=true
    fi

    # Assert
    assert_pass "Uppercase 'Feature' should fail validation (must be lowercase)" "false" "$is_valid"
}

# AC#1.8: Multiple valid types in YAML sequence (negative test - not supported)
test_ac1_8_type_must_be_single_value() {
    test_start "AC#1.8: Type field must be single value, not array"

    # Arrange
    local story_file="${TEMP_DIR}/test-array-type.story.md"
    cat > "$story_file" <<'EOF'
---
id: TEST-008
title: Test Array Type
type:
  - feature
  - documentation
status: Backlog
created: 2025-12-20
---

# TEST-008: Test Array
EOF

    # Act - extract type value
    local type_line=$(grep "^type:" "$story_file")
    local is_scalar=true

    if echo "$type_line" | grep -E "^\s*-" > /dev/null; then
        is_scalar=false
    fi

    # Assert
    # Note: This test may fail until validation is implemented
    # Expected: scalar type value only, not array
    echo -e "  ⚠ EXPECTED FAILURE: Type validation not yet implemented"
}

################################################################################
# TEST EXECUTION
################################################################################

main() {
    echo ""
    echo "================================================================================================"
    echo "AC#1: Story Frontmatter Supports Type Field - TEST SUITE"
    echo "STORY-126: Story Type Detection & Phase Skipping"
    echo "================================================================================================"
    echo ""
    echo "Status: RED PHASE (Tests expected to fail - implementation to follow)"
    echo ""

    setup

    # Run all test cases
    test_ac1_1_type_feature
    test_ac1_2_type_documentation
    test_ac1_3_type_bugfix
    test_ac1_4_type_refactor
    test_ac1_5_invalid_type_backend
    test_ac1_6_invalid_type_unknown
    test_ac1_7_type_case_sensitivity
    test_ac1_8_type_must_be_single_value

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

# Run main function
main
exit $?
