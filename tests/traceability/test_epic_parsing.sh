#!/bin/bash

##############################################################################
# Test Suite: STORY-083 - Epic Parsing Tests (AC#1)
# Purpose: Validate epic frontmatter parsing, features section extraction,
#          and stories table extraction
#
# Acceptance Criteria #1:
# - Extract epic_id (format: EPIC-NNN) from YAML frontmatter
# - Extract title from frontmatter
# - Extract Features section content
# - Extract Stories table content
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
TEST_LOG="/tmp/story-083-epic-parsing.log"

# Paths
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="${SCRIPT_DIR}/../.."
PARSER_SCRIPT="${PROJECT_ROOT}/.devforgeai/traceability/parse-requirements.sh"
FIXTURES_DIR="${SCRIPT_DIR}/fixtures"

# Initialize log
echo "=== STORY-083 Epic Parsing Test Suite ===" > "$TEST_LOG"
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
# COMPONENT 1: Epic ID Extraction (COMP-001)
##############################################################################

test_epic_id_extraction_from_frontmatter() {
    # COMP-001: Parse epic YAML frontmatter and extract epic_id
    # Given: EPIC-015 file with epic_id: EPIC-015 in frontmatter
    # When: Parser extracts epic_id
    # Then: Returns "EPIC-015"

    local epic_file="${PROJECT_ROOT}/.ai_docs/Epics/EPIC-015-epic-coverage-validation-traceability.epic.md"

    if [ ! -f "$epic_file" ]; then
        echo "Epic file not found: $epic_file"
        return 1
    fi

    local result
    result=$("$PARSER_SCRIPT" --extract-epic-id "$epic_file" 2>/dev/null)

    if [ "$result" = "EPIC-015" ]; then
        return 0
    else
        echo "Expected: EPIC-015, Got: $result"
        return 1
    fi
}

test_epic_id_extraction_using_id_field() {
    # Edge case: Some epics use id: instead of epic_id:
    # Given: An epic file with id: field instead of epic_id:
    # When: Parser extracts epic_id
    # Then: Returns the id value

    # Find an epic that might use id: instead of epic_id:
    local epic_file="${PROJECT_ROOT}/.ai_docs/Epics/EPIC-002-feedback-capture-interaction.epic.md"

    if [ ! -f "$epic_file" ]; then
        echo "Epic file not found: $epic_file"
        return 1
    fi

    local result
    result=$("$PARSER_SCRIPT" --extract-epic-id "$epic_file" 2>/dev/null)

    # Should extract EPIC-002 regardless of whether it's id: or epic_id:
    if [[ "$result" =~ ^EPIC-[0-9]{3}$ ]]; then
        return 0
    else
        echo "Expected EPIC-NNN pattern, Got: $result"
        return 1
    fi
}

##############################################################################
# COMPONENT 2: Epic Title Extraction
##############################################################################

test_epic_title_extraction() {
    # Extract title field from epic frontmatter
    # Given: EPIC-015 file with title in frontmatter
    # When: Parser extracts title
    # Then: Returns the title string

    local epic_file="${PROJECT_ROOT}/.ai_docs/Epics/EPIC-015-epic-coverage-validation-traceability.epic.md"

    if [ ! -f "$epic_file" ]; then
        echo "Epic file not found: $epic_file"
        return 1
    fi

    local result
    result=$("$PARSER_SCRIPT" --extract-epic-title "$epic_file" 2>/dev/null)

    # Title should contain "Epic Coverage Validation" (partial match)
    if [[ "$result" == *"Epic Coverage Validation"* ]]; then
        return 0
    else
        echo "Expected title containing 'Epic Coverage Validation', Got: $result"
        return 1
    fi
}

##############################################################################
# COMPONENT 3: Features Section Extraction (COMP-003)
##############################################################################

test_features_section_extraction() {
    # COMP-003: Extract features section from epic
    # Given: Epic file with ## Features section
    # When: Parser extracts features section
    # Then: Returns content containing Feature headers

    local epic_file="${PROJECT_ROOT}/.ai_docs/Epics/EPIC-015-epic-coverage-validation-traceability.epic.md"

    if [ ! -f "$epic_file" ]; then
        echo "Epic file not found: $epic_file"
        return 1
    fi

    local result
    result=$("$PARSER_SCRIPT" --extract-features "$epic_file" 2>/dev/null)

    # Should contain "Feature 0" or similar
    if [[ "$result" == *"Feature"* ]]; then
        return 0
    else
        echo "Expected features section containing 'Feature', Got nothing or: ${result:0:100}"
        return 1
    fi
}

test_features_count_extraction() {
    # COMP-003: Count features in epic
    # Given: EPIC-015 has Features 0-6 (7 features)
    # When: Parser counts features
    # Then: Returns count >= 7

    local epic_file="${PROJECT_ROOT}/.ai_docs/Epics/EPIC-015-epic-coverage-validation-traceability.epic.md"

    if [ ! -f "$epic_file" ]; then
        echo "Epic file not found: $epic_file"
        return 1
    fi

    local count
    count=$("$PARSER_SCRIPT" --count-features "$epic_file" 2>/dev/null)

    if [ "$count" -ge 7 ] 2>/dev/null; then
        return 0
    else
        echo "Expected >= 7 features, Got: $count"
        return 1
    fi
}

##############################################################################
# COMPONENT 4: Stories Table Extraction
##############################################################################

test_stories_table_extraction() {
    # AC#1: Extract Stories table from epic
    # Given: Epic file with ## Stories section containing a table
    # When: Parser extracts stories table
    # Then: Returns table content

    local epic_file="${PROJECT_ROOT}/.ai_docs/Epics/EPIC-015-epic-coverage-validation-traceability.epic.md"

    if [ ! -f "$epic_file" ]; then
        echo "Epic file not found: $epic_file"
        return 1
    fi

    local result
    result=$("$PARSER_SCRIPT" --extract-stories-table "$epic_file" 2>/dev/null)

    # Should contain STORY-083 (known to be in EPIC-015)
    if [[ "$result" == *"STORY-083"* ]]; then
        return 0
    else
        echo "Expected stories table containing 'STORY-083', Got: ${result:0:200}"
        return 1
    fi
}

test_stories_from_epic_table() {
    # Extract story IDs from Stories section table
    # Given: Epic with Stories table
    # When: Parser lists epic stories
    # Then: Returns list of STORY-NNN IDs

    local epic_file="${PROJECT_ROOT}/.ai_docs/Epics/EPIC-015-epic-coverage-validation-traceability.epic.md"

    if [ ! -f "$epic_file" ]; then
        echo "Epic file not found: $epic_file"
        return 1
    fi

    local result
    result=$("$PARSER_SCRIPT" --list-epic-stories "$epic_file" 2>/dev/null)

    # Should contain at least one STORY-NNN
    if [[ "$result" == *"STORY-"* ]]; then
        return 0
    else
        echo "Expected list containing 'STORY-', Got: $result"
        return 1
    fi
}

##############################################################################
# COMPONENT 5: Error Handling (COMP-004)
##############################################################################

test_malformed_yaml_handling() {
    # COMP-004: Handle malformed YAML gracefully
    # Given: File with malformed YAML (unclosed quote)
    # When: Parser attempts to extract
    # Then: Returns non-zero exit code but doesn't crash

    local fixture_file="${FIXTURES_DIR}/malformed-yaml.md"

    if [ ! -f "$fixture_file" ]; then
        echo "Fixture file not found: $fixture_file"
        return 1
    fi

    "$PARSER_SCRIPT" --extract-epic-id "$fixture_file" 2>/dev/null
    local exit_code=$?

    # Should return non-zero for error
    if [ "$exit_code" -ne 0 ]; then
        return 0
    else
        echo "Expected non-zero exit code for malformed YAML"
        return 1
    fi
}

test_epic_without_frontmatter() {
    # Edge case 3: Epic file without YAML frontmatter delimiters
    # Given: File with inline metadata (no --- delimiters)
    # When: Parser attempts extraction
    # Then: Should attempt fallback extraction or return appropriate code

    local fixture_file="${FIXTURES_DIR}/epic-inline-metadata.md"

    if [ ! -f "$fixture_file" ]; then
        echo "Fixture file not found: $fixture_file"
        return 1
    fi

    local result
    result=$("$PARSER_SCRIPT" --extract-epic-id "$fixture_file" 2>/dev/null)
    local exit_code=$?

    # Either extracts something or returns gracefully (not crash)
    # Accept either a result or a handled failure (exit code != 139 segfault)
    if [ "$exit_code" -ne 139 ]; then
        return 0
    else
        echo "Parser crashed (segfault) on file without frontmatter"
        return 1
    fi
}

test_empty_epic_file() {
    # Edge case 8: Empty file handling
    # Given: Empty file
    # When: Parser attempts extraction
    # Then: Returns non-zero exit code

    local fixture_file="${FIXTURES_DIR}/empty-file.md"

    if [ ! -f "$fixture_file" ]; then
        echo "Fixture file not found: $fixture_file"
        return 1
    fi

    "$PARSER_SCRIPT" --extract-epic-id "$fixture_file" 2>/dev/null
    local exit_code=$?

    # Should return non-zero for empty file
    if [ "$exit_code" -ne 0 ]; then
        return 0
    else
        echo "Expected non-zero exit code for empty file"
        return 1
    fi
}

test_large_epic_file() {
    # Edge case 10: Large file (>100KB) handling
    # Given: A large epic file
    # When: Parser processes it
    # Then: Should complete within 5 seconds without timeout

    # Use EPIC-010 which is one of the larger epics
    local epic_file="${PROJECT_ROOT}/.ai_docs/Epics/EPIC-010-parallel-story-development-cicd.epic.md"

    if [ ! -f "$epic_file" ]; then
        # Fallback to any epic
        epic_file=$(find "${PROJECT_ROOT}/.ai_docs/Epics" -name "EPIC-*.epic.md" 2>/dev/null | head -1)
    fi

    if [ -z "$epic_file" ] || [ ! -f "$epic_file" ]; then
        echo "No epic file found for large file test"
        return 1
    fi

    # Run with timeout
    timeout 5s "$PARSER_SCRIPT" --extract-epic-id "$epic_file" 2>/dev/null
    local exit_code=$?

    # Exit code 124 means timeout
    if [ "$exit_code" -ne 124 ]; then
        return 0
    else
        echo "Parser timed out on large file"
        return 1
    fi
}

##############################################################################
# COMPONENT 6: Batch Processing
##############################################################################

test_batch_epic_parsing() {
    # AC#1: Parse all epics in directory
    # Given: .ai_docs/Epics/ directory with epic files
    # When: Parser parses all epics
    # Then: Returns JSON with epics map

    local result
    result=$("$PARSER_SCRIPT" --parse-all-epics 2>/dev/null)

    # Should return valid JSON with epics key
    if echo "$result" | jq -e '.epics | length > 0' >/dev/null 2>&1; then
        return 0
    else
        echo "Expected JSON with non-empty epics map, Got: ${result:0:200}"
        return 1
    fi
}

##############################################################################
# Main Test Execution
##############################################################################

main() {
    echo -e "${BLUE}╔══════════════════════════════════════════════════════════╗${NC}"
    echo -e "${BLUE}║  STORY-083: Epic Parsing Test Suite (AC#1)               ║${NC}"
    echo -e "${BLUE}╚══════════════════════════════════════════════════════════╝${NC}"

    # Check if parser exists
    if ! check_parser_exists; then
        echo -e "${YELLOW}WARNING: Parser script not found. Tests will fail.${NC}"
        echo -e "${YELLOW}Expected at: ${PARSER_SCRIPT}${NC}"
    fi

    echo -e "\n${BLUE}=== Epic ID Extraction Tests ===${NC}"
    run_test "Extract epic_id from frontmatter (EPIC-015)" test_epic_id_extraction_from_frontmatter
    run_test "Extract epic_id using id: field" test_epic_id_extraction_using_id_field

    echo -e "\n${BLUE}=== Epic Title Extraction Tests ===${NC}"
    run_test "Extract epic title" test_epic_title_extraction

    echo -e "\n${BLUE}=== Features Section Extraction Tests ===${NC}"
    run_test "Extract features section" test_features_section_extraction
    run_test "Count features in epic" test_features_count_extraction

    echo -e "\n${BLUE}=== Stories Table Extraction Tests ===${NC}"
    run_test "Extract stories table" test_stories_table_extraction
    run_test "List epic stories from table" test_stories_from_epic_table

    echo -e "\n${BLUE}=== Error Handling Tests ===${NC}"
    run_test "Handle malformed YAML gracefully" test_malformed_yaml_handling
    run_test "Handle epic without frontmatter" test_epic_without_frontmatter
    run_test "Handle empty file" test_empty_epic_file
    run_test "Handle large file without timeout" test_large_epic_file

    echo -e "\n${BLUE}=== Batch Processing Tests ===${NC}"
    run_test "Batch parse all epics" test_batch_epic_parsing

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
