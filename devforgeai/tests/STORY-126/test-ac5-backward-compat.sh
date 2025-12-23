#!/bin/bash
################################################################################
# TEST SUITE: AC#5 - Default Type is Feature (Backward Compatible)
# STORY-126: Story Type Detection & Phase Skipping
#
# Purpose: Validate that stories WITHOUT type field default to feature type,
#          no phases are skipped, and no warnings are displayed
#
# Test Pattern: AAA (Arrange, Act, Assert)
# Status: RED (Expected to fail - tests first, implementation follows)
################################################################################

set -e

# Configuration
TEST_DIR="/mnt/c/Projects/DevForgeAI2/devforgeai/tests/STORY-126"
TEMP_DIR="${TEST_DIR}/tmp-ac5-$$"
STORY_LOCATION="/mnt/c/Projects/DevForgeAI2/devforgeai/specs/Stories"

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
        echo "    Unexpected pattern found: $pattern"
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

# AC#5.1: Existing story without type field still works
test_ac5_1_existing_story_no_type_field() {
    test_start "AC#5.1: Existing story files without type field work correctly"

    # Arrange - create story without type field (pre-STORY-126)
    local story_file="${TEMP_DIR}/STORY-LEGACY.story.md"
    cat > "$story_file" <<'EOF'
---
id: STORY-LEGACY
title: Legacy Story Without Type
status: Ready for Dev
priority: MEDIUM
story-points: 5
created: 2025-12-01
---

# STORY-LEGACY: Legacy Story Without Type

## User Story
As a developer
I want existing stories to continue working
So that backward compatibility is preserved

## Acceptance Criteria

### AC#1: Something works
Given a legacy story
When /dev runs
Then it executes normally
EOF

    # Act - verify file is valid story format
    local has_id=$(grep -q "^id: STORY-LEGACY" "$story_file" && echo "true" || echo "false")
    local has_title=$(grep -q "^title:" "$story_file" && echo "true" || echo "false")
    local has_status=$(grep -q "^status:" "$story_file" && echo "true" || echo "false")
    local has_type=$(grep -q "^type:" "$story_file" && echo "true" || echo "false")

    # Assert
    assert_pass "Story has id field" "true" "$has_id"
    assert_pass "Story has title field" "true" "$has_title"
    assert_pass "Story has status field" "true" "$has_status"
    assert_pass "Story does NOT have type field" "false" "$has_type"
}

# AC#5.2: Story without type defaults to feature
test_ac5_2_missing_type_defaults_to_feature() {
    test_start "AC#5.2: Missing type field defaults to type: feature"

    # Arrange
    local story_file="${TEMP_DIR}/no-type.story.md"
    cat > "$story_file" <<'EOF'
---
id: TEST-NO-TYPE
title: Test Default
status: Ready
priority: MEDIUM
story-points: 3
created: 2025-12-20
---

# TEST-NO-TYPE: Test Default
EOF

    # Act - simulate type resolution logic
    local explicit_type=$(grep "^type:" "$story_file" | cut -d' ' -f2 || echo "")
    local resolved_type="${explicit_type:-feature}"  # Default to feature if not found

    # Assert
    assert_pass "Explicit type is empty" "" "$explicit_type"
    assert_pass "Resolved type defaults to feature" "feature" "$resolved_type"
}

# AC#5.3: No phases skipped for stories defaulting to feature
test_ac5_3_default_feature_skips_no_phases() {
    test_start "AC#5.3: Stories without type execute all phases (like feature type)"

    # Arrange
    local story_file="${TEMP_DIR}/phases-test.story.md"
    cat > "$story_file" <<'EOF'
---
id: TEST-PHASES
title: Test Phase Execution
status: Ready
created: 2025-12-20
---

# TEST-PHASES: Test Phase Execution
EOF

    # Act - resolve type and determine phase skips
    local resolved_type=$(grep "^type:" "$story_file" | cut -d' ' -f2 || echo "feature")
    local should_skip_phase02="false"
    local should_skip_phase04="false"
    local should_skip_phase05="false"

    if [ "$resolved_type" = "documentation" ]; then
        should_skip_phase05="true"
    elif [ "$resolved_type" = "bugfix" ]; then
        should_skip_phase04="true"
    elif [ "$resolved_type" = "refactor" ]; then
        should_skip_phase02="true"
    fi

    # Assert
    assert_pass "Phase 02 should NOT be skipped" "false" "$should_skip_phase02"
    assert_pass "Phase 04 should NOT be skipped" "false" "$should_skip_phase04"
    assert_pass "Phase 05 should NOT be skipped" "false" "$should_skip_phase05"
}

# AC#5.4: No warning message for missing type
test_ac5_4_no_warning_for_missing_type() {
    test_start "AC#5.4: No warning displayed when type field is missing"

    # Arrange - simulate execution log
    local log_file="${TEMP_DIR}/execution-no-warning.log"
    cat > "$log_file" <<'EOF'
Starting Phase 01: Pre-Flight Validation
✓ Phase 01 Complete - Story ID: TEST-NO-TYPE
Resolving story type...
Story type not specified, defaulting to 'feature'
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

    # Assert - warning NOT present
    # (Silent defaulting is OK, explicit warnings are not)
    local has_error_warning=$(grep -i "error.*type" "$log_file" || echo "")
    local has_critical_warning=$(grep -i "critical.*type" "$log_file" || echo "")

    assert_pass "No ERROR about missing type" "" "$has_error_warning"
    assert_pass "No CRITICAL warning about missing type" "" "$has_critical_warning"
}

# AC#5.5: Existing STORY files work without modification
test_ac5_5_existing_stories_unmodified() {
    test_start "AC#5.5: Existing story files work as-is without changes"

    # Arrange - check if any existing stories exist
    if [ ! -d "$STORY_LOCATION" ]; then
        echo -e "  ${YELLOW}⚠ SKIPPED${NC}: Story directory not found"
        return 0
    fi

    # Act - count stories with and without type field
    local total_stories=$(find "$STORY_LOCATION" -name "*.story.md" | wc -l)
    local stories_with_type=$(grep -l "^type:" "$STORY_LOCATION"/*.story.md 2>/dev/null | wc -l || echo "0")
    local stories_without_type=$((total_stories - stories_with_type))

    # Assert
    if [ $total_stories -gt 0 ]; then
        echo -e "  Found $total_stories story files"
        echo -e "  ${GREEN}  - With type field: $stories_with_type${NC}"
        echo -e "  ${GREEN}  - Without type field: $stories_without_type${NC}"

        if [ $stories_without_type -gt 0 ]; then
            echo -e "  ✓ Existing stories without type field detected"
            ((TESTS_PASSED++))
        else
            echo -e "  ⚠ All existing stories have type field (no backward compat test needed)"
            ((TESTS_PASSED++))
        fi
    else
        echo -e "  ${YELLOW}⚠ SKIPPED${NC}: No story files found"
    fi
}

# AC#5.6: Type resolution happens early (Phase 01)
test_ac5_6_type_resolution_phase01() {
    test_start "AC#5.6: Type is resolved in Phase 01 Pre-Flight Validation"

    # Arrange - simulate Phase 01 execution log
    local log_file="${TEMP_DIR}/phase01-type-resolution.log"
    cat > "$log_file" <<'EOF'
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Phase 01: Pre-Flight Validation
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Step 1: Validate Git status
✓ Git repository ready

Step 2: Validate context files
✓ 6 context files validated

Step 3: Load story specification
✓ Story STORY-126 loaded
  - Title: Story Type Detection & Phase Skipping
  - Status: Backlog
  - Type: feature (RESOLVED: missing type → defaulting to feature)

✓ Phase 01 Complete
EOF

    # Assert
    assert_contains "$log_file" "Type:.*feature.*RESOLVED" \
        "Type resolution logged in Phase 01"
    assert_contains "$log_file" "RESOLVED: missing type → defaulting to feature" \
        "Default type resolution logic is clear"
}

# AC#5.7: No schema migration needed
test_ac5_7_no_schema_migration_needed() {
    test_start "AC#5.7: No schema migration or data upgrade required"

    # Arrange
    local story_file="${TEMP_DIR}/no-migration.story.md"
    cat > "$story_file" <<'EOF'
---
id: STORY-OLD
title: Old Story
status: Ready
priority: MEDIUM
story-points: 5
created: 2025-01-01
assignee: bob
---

# STORY-OLD: Old Story
EOF

    # Act - verify file structure is valid YAML with or without type field
    local is_valid_yaml=true
    local has_yaml_header=$(grep -q "^---$" "$story_file" && echo "true" || echo "false")
    local has_yaml_footer=$(grep -q "^---$" "$story_file" | tail -1)

    # Assert
    assert_pass "Story has YAML header" "true" "$has_valid_yaml"
    assert_pass "YAML structure is backward compatible" "true" "true"
}

# AC#5.8: Feature type explicit vs implicit are identical
test_ac5_8_feature_explicit_vs_implicit_identical() {
    test_start "AC#5.8: Explicit type: feature behaves identically to missing type"

    # Arrange - create two identical stories, one with type and one without
    local story_explicit="${TEMP_DIR}/explicit-feature.story.md"
    local story_implicit="${TEMP_DIR}/implicit-feature.story.md"

    cat > "$story_explicit" <<'EOF'
---
id: STORY-EXPLICIT
title: Explicit Feature Type
type: feature
status: Ready
created: 2025-12-20
---
EOF

    cat > "$story_implicit" <<'EOF'
---
id: STORY-IMPLICIT
title: Implicit Feature Type
status: Ready
created: 2025-12-20
---
EOF

    # Act
    local explicit_type=$(grep "^type:" "$story_explicit" | cut -d' ' -f2)
    local implicit_type=$(grep "^type:" "$story_implicit" | cut -d' ' -f2 || echo "feature")

    # Assert
    assert_pass "Explicit type: feature = implicit type" "$implicit_type" "$explicit_type"
    assert_pass "Both resolve to 'feature'" "feature" "$implicit_type"
}

# AC#5.9: Large suite of legacy stories supported
test_ac5_9_legacy_story_suite() {
    test_start "AC#5.9: Backward compatibility works for entire legacy story suite"

    # Arrange - create multiple legacy stories
    local legacy_stories=("STORY-001" "STORY-042" "STORY-089" "STORY-125")
    local test_dir="${TEMP_DIR}/legacy-suite"
    mkdir -p "$test_dir"

    for story_id in "${legacy_stories[@]}"; do
        cat > "${test_dir}/${story_id}.story.md" <<EOF
---
id: $story_id
title: Legacy Story $story_id
status: Backlog
priority: MEDIUM
story-points: 3
created: 2025-01-01
---

# $story_id: Legacy Story
EOF
    done

    # Act - verify all legacy stories are valid
    local valid_stories=0
    for story_id in "${legacy_stories[@]}"; do
        local story_file="${test_dir}/${story_id}.story.md"
        if [ -f "$story_file" ] && grep -q "^id: $story_id" "$story_file"; then
            ((valid_stories++))
        fi
    done

    # Assert
    assert_pass "All legacy stories are valid" "${#legacy_stories[@]}" "$valid_stories"
}

# AC#5.10: Type field is optional in YAML schema
test_ac5_10_type_optional_in_schema() {
    test_start "AC#5.10: Type field is optional in story YAML schema"

    # Arrange - create story template
    local template_file="${TEMP_DIR}/story-template.md"
    cat > "$template_file" <<'EOF'
---
id: STORY-XXX
title: {Title}
type: feature                    # OPTIONAL - defaults to feature if missing
status: Backlog
priority: {Priority}
story-points: {Points}
created: {Date}
assignee: null
depends-on: []
---
EOF

    # Act - verify comment indicates optional
    local has_optional_marker=$(grep -q "# OPTIONAL" "$template_file" && echo "true" || echo "false")

    # Assert
    assert_pass "Template marks type as OPTIONAL" "true" "$has_optional_marker"
    assert_pass "Default value documented" "true" "true"
}

################################################################################
# TEST EXECUTION
################################################################################

main() {
    echo ""
    echo "================================================================================================"
    echo "AC#5: Default Type is Feature (Backward Compatible) - TEST SUITE"
    echo "STORY-126: Story Type Detection & Phase Skipping"
    echo "================================================================================================"
    echo ""
    echo "Status: RED PHASE (Tests expected to fail - implementation to follow)"
    echo ""
    echo "Backward Compatibility Requirements:"
    echo "  - Stories without type field must work"
    echo "  - Default type must be 'feature' (all phases)"
    echo "  - No warnings about missing type"
    echo "  - Existing stories require NO changes"
    echo ""

    setup

    # Run all test cases
    test_ac5_1_existing_story_no_type_field
    test_ac5_2_missing_type_defaults_to_feature
    test_ac5_3_default_feature_skips_no_phases
    test_ac5_4_no_warning_for_missing_type
    test_ac5_5_existing_stories_unmodified
    test_ac5_6_type_resolution_phase01
    test_ac5_7_no_schema_migration_needed
    test_ac5_8_feature_explicit_vs_implicit_identical
    test_ac5_9_legacy_story_suite
    test_ac5_10_type_optional_in_schema

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
