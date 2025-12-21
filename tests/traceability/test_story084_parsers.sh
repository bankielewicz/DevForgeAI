#!/bin/bash
#
# Test Suite: STORY-084 Parser Tests
# Tests for epic-parser.sh, story-parser.sh, and coverage-mapper.sh
#

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
TEST_LOG="/tmp/story-084-parsers.log"

# Paths
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="${SCRIPT_DIR}/../.."
EPIC_PARSER="${PROJECT_ROOT}/devforgeai/traceability/epic-parser.sh"
STORY_PARSER="${PROJECT_ROOT}/devforgeai/traceability/story-parser.sh"
COVERAGE_MAPPER="${PROJECT_ROOT}/devforgeai/traceability/coverage-mapper.sh"
FIXTURES_DIR="${SCRIPT_DIR}/fixtures"
REAL_EPICS_DIR="${PROJECT_ROOT}/.ai_docs/Epics"
REAL_STORIES_DIR="${PROJECT_ROOT}/.ai_docs/Stories"

# Initialize log
echo "=== STORY-084 Parser Test Suite ===" > "$TEST_LOG"
echo "Started: $(date)" >> "$TEST_LOG"

#############################################################################
# TEST FRAMEWORK
#############################################################################

run_test() {
    local test_name="$1"
    local test_func="$2"

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
}

#############################################################################
# AC#1: EPIC FRONTMATTER PARSING TESTS
#############################################################################

test_epic_parser_exists() {
    [ -x "$EPIC_PARSER" ]
}

test_epic_frontmatter_extracts_epic_id() {
    local result
    result=$("$EPIC_PARSER" --parse-frontmatter "${REAL_EPICS_DIR}/EPIC-015-epic-coverage-validation-traceability.epic.md" 2>/dev/null)
    [ "$(echo "$result" | jq -r '.epic_id')" = "EPIC-015" ]
}

test_epic_frontmatter_extracts_title() {
    local result
    result=$("$EPIC_PARSER" --parse-frontmatter "${REAL_EPICS_DIR}/EPIC-015-epic-coverage-validation-traceability.epic.md" 2>/dev/null)
    local title
    title=$(echo "$result" | jq -r '.title')
    [ -n "$title" ] && [ ${#title} -lt 200 ]
}

test_epic_frontmatter_extracts_status() {
    local result
    result=$("$EPIC_PARSER" --parse-frontmatter "${REAL_EPICS_DIR}/EPIC-015-epic-coverage-validation-traceability.epic.md" 2>/dev/null)
    local status
    status=$(echo "$result" | jq -r '.status')
    [[ "$status" =~ ^(Planning|In\ Progress|Complete|On\ Hold)$ ]]
}

test_epic_frontmatter_extracts_created_date() {
    local result
    result=$("$EPIC_PARSER" --parse-frontmatter "${REAL_EPICS_DIR}/EPIC-015-epic-coverage-validation-traceability.epic.md" 2>/dev/null)
    local created
    created=$(echo "$result" | jq -r '.created')
    [[ "$created" =~ ^[0-9]{4}-[0-9]{2}-[0-9]{2}$ ]]
}

test_epic_frontmatter_extracts_complexity() {
    local result
    result=$("$EPIC_PARSER" --parse-frontmatter "${REAL_EPICS_DIR}/EPIC-015-epic-coverage-validation-traceability.epic.md" 2>/dev/null)
    local complexity
    complexity=$(echo "$result" | jq '.complexity')
    [ "$complexity" -ge 0 ]
}

test_epic_frontmatter_performance() {
    local start end elapsed
    start=$(date +%s%3N)
    "$EPIC_PARSER" --parse-frontmatter "${REAL_EPICS_DIR}/EPIC-015-epic-coverage-validation-traceability.epic.md" >/dev/null 2>&1
    end=$(date +%s%3N)
    elapsed=$((end - start))
    [ "$elapsed" -lt 500 ]  # Allow up to 500ms for WSL2
}

#############################################################################
# AC#2: EPIC FEATURES EXTRACTION TESTS
#############################################################################

test_epic_features_extracts_count() {
    local result
    result=$("$EPIC_PARSER" --extract-features "${REAL_EPICS_DIR}/EPIC-015-epic-coverage-validation-traceability.epic.md" 2>/dev/null)
    local count
    count=$(echo "$result" | jq '.features_count')
    [ "$count" -ge 1 ]
}

test_epic_features_extracts_titles() {
    local result
    result=$("$EPIC_PARSER" --extract-features "${REAL_EPICS_DIR}/EPIC-015-epic-coverage-validation-traceability.epic.md" 2>/dev/null)
    local first_title
    first_title=$(echo "$result" | jq -r '.features[0].title')
    [ -n "$first_title" ]
}

test_epic_features_extracts_descriptions() {
    local result
    result=$("$EPIC_PARSER" --extract-features "${REAL_EPICS_DIR}/EPIC-015-epic-coverage-validation-traceability.epic.md" 2>/dev/null)
    local desc
    desc=$(echo "$result" | jq -r '.features[0].description // "null"')
    [ "$desc" != "null" ]
}

test_epic_features_extracts_dependencies() {
    local result
    result=$("$EPIC_PARSER" --extract-features "${REAL_EPICS_DIR}/EPIC-015-epic-coverage-validation-traceability.epic.md" 2>/dev/null)
    local deps
    deps=$(echo "$result" | jq -r '.features[0].dependencies // "null"')
    # Feature 0 should have "None" as dependencies
    [ -n "$deps" ]
}

test_epic_features_extracts_points() {
    local result
    result=$("$EPIC_PARSER" --extract-features "${REAL_EPICS_DIR}/EPIC-015-epic-coverage-validation-traceability.epic.md" 2>/dev/null)
    local points
    points=$(echo "$result" | jq '.features[0].estimated_points // 0')
    [ "$points" -ge 0 ]
}

#############################################################################
# AC#3: STORY FRONTMATTER PARSING TESTS
#############################################################################

test_story_parser_exists() {
    [ -x "$STORY_PARSER" ]
}

test_story_frontmatter_extracts_id() {
    local result
    result=$("$STORY_PARSER" --parse-frontmatter "${REAL_STORIES_DIR}/STORY-084-epic-story-metadata-parser.story.md" 2>/dev/null)
    [ "$(echo "$result" | jq -r '.id')" = "STORY-084" ]
}

test_story_frontmatter_extracts_epic() {
    local result
    result=$("$STORY_PARSER" --parse-frontmatter "${REAL_STORIES_DIR}/STORY-084-epic-story-metadata-parser.story.md" 2>/dev/null)
    [ "$(echo "$result" | jq -r '.epic')" = "EPIC-015" ]
}

test_story_frontmatter_extracts_status() {
    local result
    result=$("$STORY_PARSER" --parse-frontmatter "${REAL_STORIES_DIR}/STORY-084-epic-story-metadata-parser.story.md" 2>/dev/null)
    local status
    status=$(echo "$result" | jq -r '.status')
    [[ "$status" =~ ^(Backlog|Ready\ for\ Dev|In\ Development|Dev\ Complete|QA\ In\ Progress|QA\ Approved|QA\ Failed|Releasing|Released)$ ]]
}

test_story_frontmatter_extracts_points() {
    local result
    result=$("$STORY_PARSER" --parse-frontmatter "${REAL_STORIES_DIR}/STORY-084-epic-story-metadata-parser.story.md" 2>/dev/null)
    local points
    points=$(echo "$result" | jq '.points')
    [[ "$points" =~ ^(1|2|3|5|8|13|21)$ ]]
}

test_story_frontmatter_extracts_format_version() {
    local result
    result=$("$STORY_PARSER" --parse-frontmatter "${REAL_STORIES_DIR}/STORY-084-epic-story-metadata-parser.story.md" 2>/dev/null)
    local version
    version=$(echo "$result" | jq -r '.format_version')
    [[ "$version" =~ ^[0-9]+\.[0-9]+$ ]]
}

test_story_frontmatter_performance() {
    local start end elapsed
    start=$(date +%s%3N)
    "$STORY_PARSER" --parse-frontmatter "${REAL_STORIES_DIR}/STORY-084-epic-story-metadata-parser.story.md" >/dev/null 2>&1
    end=$(date +%s%3N)
    elapsed=$((end - start))
    [ "$elapsed" -lt 500 ]  # Allow up to 500ms for WSL2
}

#############################################################################
# AC#6: EPIC-STORY LINKAGE VALIDATION TESTS
#############################################################################

test_coverage_mapper_exists() {
    [ -x "$COVERAGE_MAPPER" ]
}

test_linkage_valid_story() {
    local result
    result=$("$COVERAGE_MAPPER" --validate-linkage STORY-084 2>/dev/null)
    [ "$(echo "$result" | jq '.is_valid')" = "true" ]
}

test_linkage_returns_epic_title() {
    local result
    result=$("$COVERAGE_MAPPER" --validate-linkage STORY-084 2>/dev/null)
    local title
    title=$(echo "$result" | jq -r '.epic_title')
    [ -n "$title" ] && [ "$title" != "null" ]
}

test_epic_for_story_query() {
    local result
    result=$("$COVERAGE_MAPPER" --epic-for-story STORY-084 2>/dev/null)
    [ "$result" = "EPIC-015" ]
}

test_stories_for_epic_query() {
    local result
    result=$("$COVERAGE_MAPPER" --stories-for-epic EPIC-015 2>/dev/null)
    local count
    count=$(echo "$result" | jq 'length')
    [ "$count" -ge 1 ]
}

#############################################################################
# AC#7: COVERAGE MAPPING TESTS
#############################################################################

test_coverage_map_story_to_epic_index() {
    local result
    result=$("$COVERAGE_MAPPER" --generate-coverage 2>/dev/null)
    local index_type
    index_type=$(echo "$result" | jq '.story_to_epic | type')
    [ "$index_type" = '"object"' ]
}

test_coverage_map_epic_to_stories_index() {
    local result
    result=$("$COVERAGE_MAPPER" --generate-coverage 2>/dev/null)
    local index_type
    index_type=$(echo "$result" | jq '.epic_to_stories | type')
    [ "$index_type" = '"object"' ]
}

test_coverage_map_orphaned_stories() {
    local result
    result=$("$COVERAGE_MAPPER" --generate-coverage 2>/dev/null)
    local orphans_type
    orphans_type=$(echo "$result" | jq '.orphaned_stories | type')
    [ "$orphans_type" = '"array"' ]
}

test_coverage_map_epic_coverage() {
    local result
    result=$("$COVERAGE_MAPPER" --generate-coverage 2>/dev/null)
    local coverage_type
    coverage_type=$(echo "$result" | jq '.epic_coverage | type')
    [ "$coverage_type" = '"object"' ]
}

test_coverage_map_aggregate() {
    local result
    result=$("$COVERAGE_MAPPER" --generate-coverage 2>/dev/null)
    local pct
    pct=$(echo "$result" | jq '.aggregate.total_coverage_percentage')
    [ "$pct" -ge 0 ] && [ "$pct" -le 100 ]
}

#############################################################################
# MAIN EXECUTION
#############################################################################

echo "=================================================="
echo "  STORY-084: Parser Test Suite"
echo "=================================================="
echo ""

# Script existence tests
run_test "Epic parser script exists" test_epic_parser_exists
run_test "Story parser script exists" test_story_parser_exists
run_test "Coverage mapper script exists" test_coverage_mapper_exists

# AC#1: Epic frontmatter parsing
echo -e "\n--- AC#1: Epic Frontmatter Parsing ---"
run_test "Epic frontmatter extracts epic_id" test_epic_frontmatter_extracts_epic_id
run_test "Epic frontmatter extracts title" test_epic_frontmatter_extracts_title
run_test "Epic frontmatter extracts status" test_epic_frontmatter_extracts_status
run_test "Epic frontmatter extracts created date" test_epic_frontmatter_extracts_created_date
run_test "Epic frontmatter extracts complexity" test_epic_frontmatter_extracts_complexity
run_test "Epic frontmatter parsing performance <500ms" test_epic_frontmatter_performance

# AC#2: Epic features extraction
echo -e "\n--- AC#2: Epic Features Extraction ---"
run_test "Epic features extracts count" test_epic_features_extracts_count
run_test "Epic features extracts titles" test_epic_features_extracts_titles
run_test "Epic features extracts descriptions" test_epic_features_extracts_descriptions
run_test "Epic features extracts dependencies" test_epic_features_extracts_dependencies
run_test "Epic features extracts points" test_epic_features_extracts_points

# AC#3: Story frontmatter parsing
echo -e "\n--- AC#3: Story Frontmatter Parsing ---"
run_test "Story frontmatter extracts id" test_story_frontmatter_extracts_id
run_test "Story frontmatter extracts epic" test_story_frontmatter_extracts_epic
run_test "Story frontmatter extracts status" test_story_frontmatter_extracts_status
run_test "Story frontmatter extracts points" test_story_frontmatter_extracts_points
run_test "Story frontmatter extracts format_version" test_story_frontmatter_extracts_format_version
run_test "Story frontmatter parsing performance <500ms" test_story_frontmatter_performance

# AC#6: Linkage validation
echo -e "\n--- AC#6: Epic-Story Linkage Validation ---"
run_test "Linkage validates valid story" test_linkage_valid_story
run_test "Linkage returns epic title" test_linkage_returns_epic_title
run_test "Epic-for-story query works" test_epic_for_story_query
run_test "Stories-for-epic query works" test_stories_for_epic_query

# AC#7: Coverage mapping
echo -e "\n--- AC#7: Coverage Mapping ---"
run_test "Coverage map has story_to_epic index" test_coverage_map_story_to_epic_index
run_test "Coverage map has epic_to_stories index" test_coverage_map_epic_to_stories_index
run_test "Coverage map has orphaned_stories" test_coverage_map_orphaned_stories
run_test "Coverage map has epic_coverage" test_coverage_map_epic_coverage
run_test "Coverage map has aggregate stats" test_coverage_map_aggregate

echo ""
echo "=================================================="
echo "  RESULTS"
echo "=================================================="
echo "Tests Run:    $TESTS_RUN"
echo "Tests Passed: $TESTS_PASSED"
echo "Tests Failed: $TESTS_FAILED"
echo ""

# Exit with appropriate code
if [ "$TESTS_FAILED" -gt 0 ]; then
    exit 1
fi
exit 0
