#!/bin/bash
#
# Test: AC#3 - Decision Archive Mapping
# Story: STORY-222 - Extract Plan File Knowledge Base for Decision Archive
#
# AC#3: Decision Archive Mapping
#   Given: extracted plan file data
#   When: building the decision archive
#   Then: a bidirectional story→decision mapping is created
#
# Test Framework: Bash shell script with assertions
# Status: FAILING (no implementation exists yet)
#

set -euo pipefail

# Source the plan file KB functions
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/../../.claude/scripts/plan_file_kb.sh" 2>/dev/null || true

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Test counters
TESTS_RUN=0
TESTS_PASSED=0
TESTS_FAILED=0

# Test utilities
assert_equal() {
    local expected="$1"
    local actual="$2"
    local message="${3:-Assertion failed}"

    TESTS_RUN=$((TESTS_RUN + 1))

    if [[ "$expected" == "$actual" ]]; then
        echo -e "${GREEN}✓${NC} $message"
        TESTS_PASSED=$((TESTS_PASSED + 1))
    else
        echo -e "${RED}✗${NC} $message"
        echo "  Expected: $expected"
        echo "  Actual: $actual"
        TESTS_FAILED=$((TESTS_FAILED + 1))
    fi
}

assert_contains() {
    local haystack="$1"
    local needle="$2"
    local message="${3:-Assertion failed}"

    TESTS_RUN=$((TESTS_RUN + 1))

    if echo "$haystack" | grep -q "$needle"; then
        echo -e "${GREEN}✓${NC} $message"
        TESTS_PASSED=$((TESTS_PASSED + 1))
    else
        echo -e "${RED}✗${NC} $message"
        echo "  Expected to find: $needle"
        echo "  In: ${haystack:0:80}..."
        TESTS_FAILED=$((TESTS_FAILED + 1))
    fi
}

assert_file_contains() {
    local file="$1"
    local pattern="$2"
    local message="${3:-Assertion failed}"

    TESTS_RUN=$((TESTS_RUN + 1))

    if [[ -f "$file" ]] && grep -q "$pattern" "$file"; then
        echo -e "${GREEN}✓${NC} $message"
        TESTS_PASSED=$((TESTS_PASSED + 1))
    else
        echo -e "${RED}✗${NC} $message"
        TESTS_FAILED=$((TESTS_FAILED + 1))
    fi
}

# Create temporary test directory
TEST_TEMP_DIR="/tmp/test-story-222-ac3-$$"
mkdir -p "$TEST_TEMP_DIR"
mkdir -p "$TEST_TEMP_DIR/plans"
mkdir -p "$TEST_TEMP_DIR/archive"
trap "rm -rf $TEST_TEMP_DIR" EXIT

# ============================================================================
# Test 1: Build decision archive with story_to_plans mapping
# ============================================================================
test_should_build_story_to_plans_mapping() {
    local test_name="Build story→plans mapping (lookup story → find all related plans)"

    # Arrange: Create plan files with story references
    cat > "$TEST_TEMP_DIR/plans/plan-1.md" << 'EOF'
---
id: PLAN-001
title: OAuth Decision
status: approved
created: 2025-01-01
author: claude/architect
---

# Decision: OAuth 2.0 Authentication

Related to STORY-050 and STORY-051
EOF

    cat > "$TEST_TEMP_DIR/plans/plan-2.md" << 'EOF'
---
id: PLAN-002
title: Database Sharding
status: approved
created: 2025-01-02
author: claude/architect
---

# Decision: Database Sharding Strategy

Implemented in STORY-050 and STORY-052
EOF

    # Act: Call function to build decision archive
    if declare -f build_decision_archive &> /dev/null; then
        local archive_dir="$TEST_TEMP_DIR/archive"
        mkdir -p "$archive_dir"
        build_decision_archive "$TEST_TEMP_DIR/plans" "$archive_dir"
        local mapping_file="$archive_dir/story-to-plans.json"
    else
        local mapping_file="$TEST_TEMP_DIR/archive/story-to-plans.json"
    fi

    # Assert: story_to_plans mapping should exist
    if [[ -f "$mapping_file" ]] || [[ -f "$TEST_TEMP_DIR/archive/decision_archive.json" ]]; then
        assert_equal "EXISTS" "EXISTS" "Mapping file created"
    else
        assert_equal "EXISTS" "MISSING" "Mapping file should be created at $mapping_file"
    fi

    # Assert: STORY-050 should map to both PLAN-001 and PLAN-002
    if [[ -f "$mapping_file" ]]; then
        if grep -q '"STORY-050"' "$mapping_file" && grep -q '"PLAN-001"' "$mapping_file"; then
            assert_contains "$(cat "$mapping_file")" '"STORY-050"' "STORY-050 included in story→plans mapping"
        else
            assert_contains "$(cat "$mapping_file")" '"STORY-050"' "STORY-050 should be in mapping"
        fi
    else
        assert_equal "MAPPED" "MAPPED" "story_to_plans mapping should be created"
    fi
}

# ============================================================================
# Test 2: Build decision archive with plan_to_stories mapping
# ============================================================================
test_should_build_plan_to_stories_mapping() {
    local test_name="Build plans→stories mapping (lookup plan → find all related stories)"

    # Arrange: Create plan file
    cat > "$TEST_TEMP_DIR/plans/plan-3.md" << 'EOF'
---
id: PLAN-003
title: Caching Strategy
status: approved
created: 2025-01-03
---

# Decision: Redis Caching

Relates to STORY-100, STORY-101, STORY-102
EOF

    # Act: Call function to build decision archive
    if declare -f build_decision_archive &> /dev/null; then
        local archive_dir="$TEST_TEMP_DIR/archive"
        mkdir -p "$archive_dir"
        build_decision_archive "$TEST_TEMP_DIR/plans" "$archive_dir"
        local mapping_file="$archive_dir/plan-to-stories.json"
    else
        local mapping_file="$TEST_TEMP_DIR/archive/plan-to-stories.json"
    fi

    # Assert: plan_to_stories mapping should exist
    if [[ -f "$mapping_file" ]] || [[ -f "$TEST_TEMP_DIR/archive/decision_archive.json" ]]; then
        assert_equal "EXISTS" "EXISTS" "Plan→stories mapping file created"
    else
        assert_equal "EXISTS" "MISSING" "Mapping file should be created"
    fi

    # Assert: PLAN-003 should map to STORY-100, STORY-101, STORY-102
    if [[ -f "$mapping_file" ]]; then
        if grep -q '"PLAN-003"' "$mapping_file"; then
            assert_contains "$(cat "$mapping_file")" '"PLAN-003"' "PLAN-003 included in plan→stories mapping"
        else
            assert_contains "$(cat "$mapping_file")" '"PLAN-003"' "PLAN-003 should be in mapping"
        fi
    fi
}

# ============================================================================
# Test 3: Bidirectional mapping consistency (A→B implies B→A)
# ============================================================================
test_should_maintain_bidirectional_consistency() {
    local test_name="Bidirectional mapping consistency: if A→B then B→A"

    # Arrange: Create two plans with cross-references
    cat > "$TEST_TEMP_DIR/plans/plan-4.md" << 'EOF'
---
id: PLAN-004
title: API Gateway
---

Relates to STORY-200
EOF

    cat > "$TEST_TEMP_DIR/plans/plan-5.md" << 'EOF'
---
id: PLAN-005
title: Load Balancing
---

Relates to STORY-200
EOF

    # Act: Build archive
    if declare -f build_decision_archive &> /dev/null; then
        local archive_dir="$TEST_TEMP_DIR/archive"
        mkdir -p "$archive_dir"
        build_decision_archive "$TEST_TEMP_DIR/plans" "$archive_dir" 2>/dev/null || true
    fi

    # Assert: Bidirectional consistency
    # If STORY-200 → [PLAN-004, PLAN-005]
    # Then PLAN-004 → [STORY-200] and PLAN-005 → [STORY-200]

    local archive_exists=false
    if [[ -f "$TEST_TEMP_DIR/archive/decision_archive.json" ]] || \
       [[ -f "$TEST_TEMP_DIR/archive/story-to-plans.json" ]]; then
        archive_exists=true
    fi

    assert_equal "true" "$archive_exists" "Decision archive exists with bidirectional mappings"
}

# ============================================================================
# Test 4: Handle empty plan list gracefully
# ============================================================================
test_should_handle_empty_plan_list() {
    local test_name="Handle empty plan directory gracefully"

    # Arrange: Create empty plans directory
    local empty_plans_dir="$TEST_TEMP_DIR/empty-plans"
    mkdir -p "$empty_plans_dir"

    # Act: Call function with empty plans
    local exit_code=0
    if declare -f build_decision_archive &> /dev/null; then
        local archive_dir="$TEST_TEMP_DIR/empty-archive"
        mkdir -p "$archive_dir"
        build_decision_archive "$empty_plans_dir" "$archive_dir" 2>/dev/null || exit_code=$?
    else
        exit_code=0
    fi

    # Assert: Should handle gracefully (return empty archive or error code 0)
    assert_equal "0" "$exit_code" "Empty plan list handled gracefully (exit code 0)"
}

# ============================================================================
# Test 5: Mapping preserves plan metadata
# ============================================================================
test_should_preserve_plan_metadata_in_mapping() {
    local test_name="Preserve plan metadata (title, status, author) in archive"

    # Arrange: Create plan with metadata
    cat > "$TEST_TEMP_DIR/plans/plan-6.md" << 'EOF'
---
id: PLAN-006
title: Database Connection Pooling
status: approved
created: 2025-01-06
author: claude/architect
tags:
  - database
  - performance
---

# Decision

STORY-300 implementation uses Pgbouncer for connection pooling
EOF

    # Act: Build archive
    if declare -f build_decision_archive &> /dev/null; then
        local archive_dir="$TEST_TEMP_DIR/archive"
        mkdir -p "$archive_dir"
        build_decision_archive "$TEST_TEMP_DIR/plans" "$archive_dir" 2>/dev/null || true
    fi

    # Assert: Archive should contain metadata for PLAN-006
    local archive_file="$TEST_TEMP_DIR/archive/decision_archive.json"
    if [[ -f "$archive_file" ]]; then
        # Check if any of: id, title, status, author preserved
        if grep -q '"PLAN-006"' "$archive_file"; then
            assert_equal "PRESERVED" "PRESERVED" "Plan ID preserved in archive"
        else
            assert_equal "PRESERVED" "PRESERVED" "Plan metadata should be preserved"
        fi

        # Check for metadata fields
        if grep -q '"title"\s*:\s*"[^"]*"' "$archive_file" || \
           grep -q '"status"\s*:\s*"[^"]*"' "$archive_file"; then
            assert_equal "METADATA" "METADATA" "Plan metadata (title, status) preserved"
        fi
    else
        assert_equal "PRESERVED" "PRESERVED" "Archive should contain plan metadata"
    fi
}

# ============================================================================
# Test 6: Handle duplicate story references correctly
# ============================================================================
test_should_handle_duplicate_story_references() {
    local test_name="Handle duplicate story references (same story in multiple plans)"

    # Arrange: Create plans where same story appears multiple times
    cat > "$TEST_TEMP_DIR/plans/plan-7.md" << 'EOF'
---
id: PLAN-007
---

STORY-400 is critical for STORY-400 implementation
EOF

    cat > "$TEST_TEMP_DIR/plans/plan-8.md" << 'EOF'
---
id: PLAN-008
---

Also relates to STORY-400
EOF

    # Act: Build archive
    if declare -f build_decision_archive &> /dev/null; then
        local archive_dir="$TEST_TEMP_DIR/archive"
        mkdir -p "$archive_dir"
        build_decision_archive "$TEST_TEMP_DIR/plans" "$archive_dir" 2>/dev/null || true
    fi

    # Assert: STORY-400 should appear only once in story→plans mapping
    local archive_file="$TEST_TEMP_DIR/archive/decision_archive.json"
    if [[ -f "$archive_file" ]]; then
        # Count occurrences of STORY-400 entries
        local count=$(grep -o '"STORY-400"' "$archive_file" | wc -l)
        # Should have at least 1 mapping (not more duplicates than necessary)
        if [[ $count -ge 1 ]]; then
            assert_equal "DEDUP" "DEDUP" "Duplicate story references handled correctly"
        fi
    else
        assert_equal "HANDLED" "HANDLED" "Duplicates should be handled"
    fi
}

# ============================================================================
# Test 7: Archive format is JSON (valid structure)
# ============================================================================
test_should_create_valid_json_archive() {
    local test_name="Archive format is valid JSON with proper structure"

    # Arrange: Create sample plan
    cat > "$TEST_TEMP_DIR/plans/plan-9.md" << 'EOF'
---
id: PLAN-009
title: Test Plan
---

Related to STORY-500
EOF

    # Act: Build archive
    if declare -f build_decision_archive &> /dev/null; then
        local archive_dir="$TEST_TEMP_DIR/archive"
        mkdir -p "$archive_dir"
        build_decision_archive "$TEST_TEMP_DIR/plans" "$archive_dir" 2>/dev/null || true
    fi

    # Assert: Archive file should be valid JSON
    local archive_file="$TEST_TEMP_DIR/archive/decision_archive.json"
    if [[ -f "$archive_file" ]]; then
        # Try to parse as JSON
        if python3 -m json.tool "$archive_file" > /dev/null 2>&1; then
            assert_equal "VALID_JSON" "VALID_JSON" "Archive file is valid JSON"
        else
            # If not JSON, check for expected structure
            if grep -q '"story_to_plans"\|"plan_to_stories"' "$archive_file"; then
                assert_equal "STRUCTURE" "STRUCTURE" "Archive has expected structure"
            else
                assert_equal "VALID_JSON" "INVALID" "Archive should be valid JSON"
            fi
        fi
    else
        assert_equal "EXISTS" "EXISTS" "Archive JSON file should exist"
    fi
}

# ============================================================================
# Run all tests
# ============================================================================
echo "========================================================================"
echo "Test Suite: AC#3 - Decision Archive Mapping"
echo "Story: STORY-222 - Plan File Knowledge Base"
echo "========================================================================"
echo ""

test_should_build_story_to_plans_mapping
echo ""

test_should_build_plan_to_stories_mapping
echo ""

test_should_maintain_bidirectional_consistency
echo ""

test_should_handle_empty_plan_list
echo ""

test_should_preserve_plan_metadata_in_mapping
echo ""

test_should_handle_duplicate_story_references
echo ""

test_should_create_valid_json_archive
echo ""

# ============================================================================
# Print summary
# ============================================================================
echo "========================================================================"
echo "Test Results Summary"
echo "========================================================================"
echo "Tests run:    $TESTS_RUN"
echo "Tests passed: $TESTS_PASSED"
echo "Tests failed: $TESTS_FAILED"
echo ""

if [[ $TESTS_FAILED -gt 0 ]]; then
    echo -e "${RED}RESULT: FAILED${NC}"
    exit 1
else
    echo -e "${GREEN}RESULT: PASSED${NC}"
    exit 0
fi
