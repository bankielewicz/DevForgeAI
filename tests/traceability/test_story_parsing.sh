#!/bin/bash

##############################################################################
# Test Suite: STORY-083 - Story Parsing Tests (AC#2)
# Purpose: Validate story epic reference parsing and story ID extraction
#
# Acceptance Criteria #2:
# - Extract story_id from filename pattern (STORY-NNN-slug.story.md)
# - Extract epic: field value from YAML frontmatter
# - Handle epic: None (standalone story)
# - Handle missing epic: field (flagged as incomplete metadata)
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
TEST_LOG="/tmp/story-083-story-parsing.log"

# Paths
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="${SCRIPT_DIR}/../.."
PARSER_SCRIPT="${PROJECT_ROOT}/.devforgeai/traceability/parse-requirements.sh"
FIXTURES_DIR="${SCRIPT_DIR}/fixtures"

# Initialize log
echo "=== STORY-083 Story Parsing Test Suite ===" > "$TEST_LOG"
echo "Started: $(date)" >> "$TEST_LOG"
echo "" >> "$TEST_LOG"

##############################################################################
# Test Framework Functions
##############################################################################

run_test() {
    local test_name=$1
    local test_func=$2

    TESTS_RUN=$((TESTS_RUN + 1))
    echo -e "\n${BLUE}[Test $TESTS_RUN]${NC} $test_name"
    echo "[Test $TESTS_RUN] $test_name" >> "$TEST_LOG"

    if $test_func 2>> "$TEST_LOG"; then
        TESTS_PASSED=$((TESTS_PASSED + 1))
        echo -e "${GREEN}✓${NC} PASSED"
        echo "RESULT: PASSED" >> "$TEST_LOG"
    else
        TESTS_FAILED=$((TESTS_FAILED + 1))
        echo -e "${RED}✗${NC} FAILED"
        echo "RESULT: FAILED" >> "$TEST_LOG"
    fi
    echo "" >> "$TEST_LOG"
}

check_parser_exists() {
    if [ ! -f "$PARSER_SCRIPT" ]; then
        echo -e "${YELLOW}⊘${NC} Parser script not found at: $PARSER_SCRIPT"
        return 1
    fi
    if [ ! -x "$PARSER_SCRIPT" ]; then
        echo -e "${YELLOW}⊘${NC} Parser script not executable"
        return 1
    fi
    return 0
}

##############################################################################
# COMPONENT 1: Story ID Extraction from Filename (BR-002)
##############################################################################

test_story_id_from_filename() {
    # BR-002: Story ID extracted from filename
    # Pattern: STORY-NNN-slug.story.md
    # Given: Filename "STORY-007-post-operation-retrospective-conversation.story.md"
    # When: Parser extracts story_id from filename
    # Then: Returns "STORY-007"

    local result
    result=$("$PARSER_SCRIPT" --extract-story-id-from-filename "STORY-007-post-operation-retrospective-conversation.story.md" 2>/dev/null)

    if [ "$result" = "STORY-007" ]; then
        return 0
    else
        echo "Expected: STORY-007, Got: $result"
        return 1
    fi
}

test_story_id_format_validation() {
    # BR-002: Story ID must match ^STORY-\d{3}$
    # Given: Various story ID formats
    # When: Parser validates
    # Then: STORY-007 accepted, STORY-7 rejected, STORY-0007 rejected

    # Valid format
    "$PARSER_SCRIPT" --validate-story-id "STORY-007" 2>/dev/null
    local valid_exit=$?

    # Invalid: too few digits
    "$PARSER_SCRIPT" --validate-story-id "STORY-7" 2>/dev/null
    local invalid1_exit=$?

    # Invalid: too many digits
    "$PARSER_SCRIPT" --validate-story-id "STORY-0007" 2>/dev/null
    local invalid2_exit=$?

    if [ "$valid_exit" -eq 0 ] && [ "$invalid1_exit" -ne 0 ] && [ "$invalid2_exit" -ne 0 ]; then
        return 0
    else
        echo "Validation failed: valid=$valid_exit, invalid1=$invalid1_exit, invalid2=$invalid2_exit"
        return 1
    fi
}

##############################################################################
# COMPONENT 2: Epic Field Extraction (AC#2)
##############################################################################

test_epic_field_extraction() {
    # AC#2: Extract epic: field from story frontmatter
    # Given: STORY-007 file with epic: EPIC-002
    # When: Parser extracts epic: field
    # Then: Returns "EPIC-002"

    local story_file="${PROJECT_ROOT}/devforgeai/specs/Stories/STORY-007-post-operation-retrospective-conversation.story.md"

    if [ ! -f "$story_file" ]; then
        echo "Story file not found: $story_file"
        return 1
    fi

    local result
    result=$("$PARSER_SCRIPT" --extract-story-epic "$story_file" 2>/dev/null)

    if [ "$result" = "EPIC-002" ]; then
        return 0
    else
        echo "Expected: EPIC-002, Got: $result"
        return 1
    fi
}

test_story_title_extraction() {
    # Extract title field from story frontmatter
    # Given: STORY-007 file with title in frontmatter
    # When: Parser extracts title
    # Then: Returns the title string

    local story_file="${PROJECT_ROOT}/devforgeai/specs/Stories/STORY-007-post-operation-retrospective-conversation.story.md"

    if [ ! -f "$story_file" ]; then
        echo "Story file not found: $story_file"
        return 1
    fi

    local result
    result=$("$PARSER_SCRIPT" --extract-story-title "$story_file" 2>/dev/null)

    # Title should contain something meaningful
    if [[ -n "$result" ]]; then
        return 0
    else
        echo "Expected non-empty title, Got: $result"
        return 1
    fi
}

##############################################################################
# COMPONENT 3: Handle epic: None (AC#2)
##############################################################################

test_epic_none_handling() {
    # AC#2: Handle epic: None (intentionally standalone)
    # Given: Story file with epic: None
    # When: Parser extracts epic field
    # Then: Returns "None"

    local fixture_file="${FIXTURES_DIR}/epic-none.md"

    if [ ! -f "$fixture_file" ]; then
        echo "Fixture file not found: $fixture_file"
        return 1
    fi

    local result
    result=$("$PARSER_SCRIPT" --extract-story-epic "$fixture_file" 2>/dev/null)

    if [ "$result" = "None" ]; then
        return 0
    else
        echo "Expected: None, Got: $result"
        return 1
    fi
}

##############################################################################
# COMPONENT 4: Handle Missing Epic Field (AC#2)
##############################################################################

test_missing_epic_field() {
    # AC#2: Handle missing epic: field
    # Given: Story file without epic: field
    # When: Parser extracts epic field
    # Then: Returns exit code 2 (missing metadata)

    local fixture_file="${FIXTURES_DIR}/story-missing-epic.md"

    if [ ! -f "$fixture_file" ]; then
        echo "Fixture file not found: $fixture_file"
        return 1
    fi

    "$PARSER_SCRIPT" --extract-story-epic "$fixture_file" 2>/dev/null
    local exit_code=$?

    # Should return exit code 2 for missing metadata
    if [ "$exit_code" -eq 2 ]; then
        return 0
    else
        echo "Expected exit code 2 (missing metadata), Got: $exit_code"
        return 1
    fi
}

##############################################################################
# COMPONENT 5: Epic Reference Validation (BR-003)
##############################################################################

test_validate_epic_reference_valid() {
    # BR-003: Valid epic reference format
    # Given: "EPIC-015"
    # When: Parser validates
    # Then: Returns "valid"

    local result
    result=$("$PARSER_SCRIPT" --validate-epic-reference "EPIC-015" 2>/dev/null)

    if [ "$result" = "valid" ]; then
        return 0
    else
        echo "Expected: valid, Got: $result"
        return 1
    fi
}

test_validate_epic_reference_standalone() {
    # BR-003: Standalone story reference
    # Given: "None"
    # When: Parser validates
    # Then: Returns "standalone"

    local result
    result=$("$PARSER_SCRIPT" --validate-epic-reference "None" 2>/dev/null)

    if [ "$result" = "standalone" ]; then
        return 0
    else
        echo "Expected: standalone, Got: $result"
        return 1
    fi
}

test_story_references_story_instead_of_epic() {
    # Edge case 6: Story contains epic: STORY-XXX (referencing story instead of epic)
    # Given: "STORY-001"
    # When: Parser validates
    # Then: Returns "invalid"

    local result
    result=$("$PARSER_SCRIPT" --validate-epic-reference "STORY-001" 2>/dev/null)

    if [ "$result" = "invalid" ]; then
        return 0
    else
        echo "Expected: invalid, Got: $result"
        return 1
    fi
}

test_invalid_epic_reference() {
    # BR-003: Invalid epic reference format
    # Given: "INVALID-123"
    # When: Parser validates
    # Then: Returns "invalid"

    local result
    result=$("$PARSER_SCRIPT" --validate-epic-reference "INVALID-123" 2>/dev/null)

    if [ "$result" = "invalid" ]; then
        return 0
    else
        echo "Expected: invalid, Got: $result"
        return 1
    fi
}

##############################################################################
# COMPONENT 6: Batch Story Parsing
##############################################################################

test_batch_story_parsing() {
    # AC#2: Parse all stories in directory
    # Given: devforgeai/specs/Stories/ directory with story files
    # When: Parser parses all stories
    # Then: Returns JSON with stories map

    local result
    result=$("$PARSER_SCRIPT" --parse-all-stories 2>/dev/null)

    # Should return valid JSON with stories key
    if echo "$result" | jq -e '.stories | length > 0' >/dev/null 2>&1; then
        return 0
    else
        echo "Expected JSON with non-empty stories map, Got: ${result:0:200}"
        return 1
    fi
}

##############################################################################
# Main Test Execution
##############################################################################

main() {
    echo -e "${BLUE}╔══════════════════════════════════════════════════════════╗${NC}"
    echo -e "${BLUE}║  STORY-083: Story Parsing Test Suite (AC#2)              ║${NC}"
    echo -e "${BLUE}╚══════════════════════════════════════════════════════════╝${NC}"

    # Check if parser exists
    if ! check_parser_exists; then
        echo -e "${YELLOW}WARNING: Parser script not found. Tests will fail.${NC}"
    fi

    echo -e "\n${BLUE}=== Story ID Extraction Tests ===${NC}"
    run_test "Extract story_id from filename" test_story_id_from_filename
    run_test "Validate story ID format" test_story_id_format_validation

    echo -e "\n${BLUE}=== Epic Field Extraction Tests ===${NC}"
    run_test "Extract epic: field from story" test_epic_field_extraction
    run_test "Extract story title" test_story_title_extraction

    echo -e "\n${BLUE}=== Handle epic: None Tests ===${NC}"
    run_test "Handle epic: None (standalone)" test_epic_none_handling

    echo -e "\n${BLUE}=== Handle Missing Epic Field Tests ===${NC}"
    run_test "Handle missing epic: field" test_missing_epic_field

    echo -e "\n${BLUE}=== Epic Reference Validation Tests ===${NC}"
    run_test "Validate valid epic reference" test_validate_epic_reference_valid
    run_test "Validate standalone reference (None)" test_validate_epic_reference_standalone
    run_test "Detect story referencing story" test_story_references_story_instead_of_epic
    run_test "Detect invalid epic reference" test_invalid_epic_reference

    echo -e "\n${BLUE}=== Batch Processing Tests ===${NC}"
    run_test "Batch parse all stories" test_batch_story_parsing

    # Summary
    echo ""
    echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"
    echo -e "Tests Run:    ${TESTS_RUN}"
    echo -e "Tests Passed: ${GREEN}${TESTS_PASSED}${NC}"
    echo -e "Tests Failed: ${RED}${TESTS_FAILED}${NC}"
    echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"

    # Log summary
    echo "" >> "$TEST_LOG"
    echo "=== Summary ===" >> "$TEST_LOG"
    echo "Tests Run: $TESTS_RUN" >> "$TEST_LOG"
    echo "Tests Passed: $TESTS_PASSED" >> "$TEST_LOG"
    echo "Tests Failed: $TESTS_FAILED" >> "$TEST_LOG"
    echo "Completed: $(date)" >> "$TEST_LOG"

    # Exit with appropriate code
    if [ "$TESTS_FAILED" -gt 0 ]; then
        exit 1
    fi
    exit 0
}

main "$@"
