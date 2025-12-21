#!/bin/bash

################################################################################
# TEST SUITE: AC#3 - Version Tracking File Created with Valid Schema
# Story: STORY-041
# Description: Verify version.json exists with valid JSON schema
#
# Acceptance Criteria:
# - File exists: version.json in project root
# - Valid JSON schema with required fields:
#   - version: "1.0.0" (semantic versioning)
#   - release_date: "[YYYY-MM-DD format]"
#   - framework_status: one of (DEVELOPMENT, BETA, PRODUCTION, ARCHIVED)
#   - components: object with skills, agents, commands, memory_files, context_templates, protocols
#   - changelog_url: "devforgeai/CHANGELOG.md"
#   - migration_status: object with phase, src_structure_complete, content_migration_complete, installer_ready
#
# Validation:
# - Valid JSON (python -m json.tool validates successfully)
# - Semantic versioning: ^\d+\.\d+\.\d+$
# - ISO 8601 date: ^\d{4}-\d{2}-\d{2}$
# - framework_status is valid enum
# - Component counts are integers ≥ 0
#
# Test Status: FAILING (Red Phase) - version.json does not yet exist
################################################################################

set -e  # Exit on first error

PROJECT_ROOT="/mnt/c/Projects/DevForgeAI2"
TEST_NAME="AC#3: Version Tracking File Created with Valid Schema"

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Test counters
TESTS_RUN=0
TESTS_PASSED=0
TESTS_FAILED=0

# Helper function to assert file exists
assert_file_exists() {
    local file_path="$1"
    local description="$2"
    ((TESTS_RUN++))

    if [ -f "$file_path" ]; then
        echo -e "${GREEN}✓ PASS${NC}: $description"
        echo "  File: $file_path"
        ((TESTS_PASSED++))
        return 0
    else
        echo -e "${RED}✗ FAIL${NC}: $description"
        echo "  Expected file: $file_path"
        ((TESTS_FAILED++))
        return 1
    fi
}

# Helper function to assert valid JSON
assert_valid_json() {
    local file_path="$1"
    local description="$2"
    ((TESTS_RUN++))

    if python3 -m json.tool "$file_path" > /dev/null 2>&1; then
        echo -e "${GREEN}✓ PASS${NC}: $description"
        echo "  File: $file_path"
        ((TESTS_PASSED++))
        return 0
    else
        echo -e "${RED}✗ FAIL${NC}: $description"
        echo "  File: $file_path"
        echo "  Error: Invalid JSON syntax"
        ((TESTS_FAILED++))
        return 1
    fi
}

# Helper function to assert JSON field exists and has expected value
assert_json_field() {
    local file_path="$1"
    local field_path="$2"
    local description="$3"
    ((TESTS_RUN++))

    local value=$(python3 -c "import json; data=json.load(open('$file_path')); print(json.dumps(eval('data' + '$field_path')))" 2>/dev/null)

    if [ -n "$value" ] && [ "$value" != "null" ]; then
        echo -e "${GREEN}✓ PASS${NC}: $description"
        echo "  Field: $field_path = $value"
        ((TESTS_PASSED++))
        return 0
    else
        echo -e "${RED}✗ FAIL${NC}: $description"
        echo "  Field: $field_path not found or null"
        ((TESTS_FAILED++))
        return 1
    fi
}

# Helper function to validate semantic version format
assert_semantic_version() {
    local file_path="$1"
    local description="$2"
    ((TESTS_RUN++))

    local version=$(python3 -c "import json; print(json.load(open('$file_path')).get('version', ''))" 2>/dev/null)

    if echo "$version" | grep -E "^\d+\.\d+\.\d+$" > /dev/null 2>&1; then
        echo -e "${GREEN}✓ PASS${NC}: $description"
        echo "  Version: $version"
        ((TESTS_PASSED++))
        return 0
    else
        echo -e "${RED}✗ FAIL${NC}: $description"
        echo "  Version: $version (expected format: X.Y.Z)"
        ((TESTS_FAILED++))
        return 1
    fi
}

# Helper function to validate ISO 8601 date format
assert_iso8601_date() {
    local file_path="$1"
    local description="$2"
    ((TESTS_RUN++))

    local release_date=$(python3 -c "import json; print(json.load(open('$file_path')).get('release_date', ''))" 2>/dev/null)

    if echo "$release_date" | grep -E "^\d{4}-\d{2}-\d{2}$" > /dev/null 2>&1; then
        echo -e "${GREEN}✓ PASS${NC}: $description"
        echo "  Release Date: $release_date"
        ((TESTS_PASSED++))
        return 0
    else
        echo -e "${RED}✗ FAIL${NC}: $description"
        echo "  Release Date: $release_date (expected format: YYYY-MM-DD)"
        ((TESTS_FAILED++))
        return 1
    fi
}

# Helper function to validate enum value
assert_enum_value() {
    local file_path="$1"
    local field_path="$2"
    local valid_values="$3"  # Space-separated string
    local description="$4"
    ((TESTS_RUN++))

    local value=$(python3 -c "import json; data=json.load(open('$file_path')); print(eval('data' + '$field_path'))" 2>/dev/null)

    if echo "$valid_values" | grep -w "$value" > /dev/null 2>&1; then
        echo -e "${GREEN}✓ PASS${NC}: $description"
        echo "  Value: $value (valid enum)"
        ((TESTS_PASSED++))
        return 0
    else
        echo -e "${RED}✗ FAIL${NC}: $description"
        echo "  Value: $value (valid options: $valid_values)"
        ((TESTS_FAILED++))
        return 1
    fi
}

# Helper function to assert integer component count
assert_component_count() {
    local file_path="$1"
    local field_path="$2"
    local description="$3"
    ((TESTS_RUN++))

    local count=$(python3 -c "import json; data=json.load(open('$file_path')); print(eval('data' + '$field_path'))" 2>/dev/null)

    if [ -n "$count" ] && [ "$count" -ge 0 ] 2>/dev/null; then
        echo -e "${GREEN}✓ PASS${NC}: $description"
        echo "  Count: $count"
        ((TESTS_PASSED++))
        return 0
    else
        echo -e "${RED}✗ FAIL${NC}: $description"
        echo "  Count: $count (expected: non-negative integer)"
        ((TESTS_FAILED++))
        return 1
    fi
}

echo ""
echo -e "${BLUE}═══════════════════════════════════════════════════════════════${NC}"
echo -e "${BLUE}TEST SUITE: $TEST_NAME${NC}"
echo -e "${BLUE}═══════════════════════════════════════════════════════════════${NC}"
echo ""

cd "$PROJECT_ROOT" || exit 1

################################################################################
# TEST GROUP 1: File Exists
################################################################################

echo -e "${BLUE}Test Group 1: File Exists${NC}"
echo ""

assert_file_exists "version.json" "version.json file exists in project root"

echo ""

################################################################################
# TEST GROUP 2: Valid JSON Format
################################################################################

echo -e "${BLUE}Test Group 2: Valid JSON Format${NC}"
echo ""

assert_valid_json "version.json" "version.json contains valid JSON"

echo ""

################################################################################
# TEST GROUP 3: Required Fields Present
################################################################################

echo -e "${BLUE}Test Group 3: Required Fields Present${NC}"
echo ""

assert_json_field "version.json" "['version']" "Field 'version' exists"
assert_json_field "version.json" "['release_date']" "Field 'release_date' exists"
assert_json_field "version.json" "['framework_status']" "Field 'framework_status' exists"
assert_json_field "version.json" "['components']" "Field 'components' exists"
assert_json_field "version.json" "['changelog_url']" "Field 'changelog_url' exists"
assert_json_field "version.json" "['migration_status']" "Field 'migration_status' exists"

echo ""

################################################################################
# TEST GROUP 4: Version Format (Semantic Versioning)
################################################################################

echo -e "${BLUE}Test Group 4: Version Format (Semantic Versioning)${NC}"
echo ""

assert_semantic_version "version.json" "Version follows semantic versioning (X.Y.Z format)"

echo ""

################################################################################
# TEST GROUP 5: Release Date Format (ISO 8601)
################################################################################

echo -e "${BLUE}Test Group 5: Release Date Format (ISO 8601)${NC}"
echo ""

assert_iso8601_date "version.json" "Release date follows ISO 8601 format (YYYY-MM-DD)"

echo ""

################################################################################
# TEST GROUP 6: Framework Status Enum
################################################################################

echo -e "${BLUE}Test Group 6: Framework Status Enum${NC}"
echo ""

assert_enum_value "version.json" "['framework_status']" "DEVELOPMENT BETA PRODUCTION ARCHIVED" "framework_status is valid enum value"

echo ""

################################################################################
# TEST GROUP 7: Component Counts - Skills
################################################################################

echo -e "${BLUE}Test Group 7: Component Counts - Valid Integers${NC}"
echo ""

assert_component_count "version.json" "['components']['skills']" "Component count: skills is non-negative integer"
assert_component_count "version.json" "['components']['agents']" "Component count: agents is non-negative integer"
assert_component_count "version.json" "['components']['commands']" "Component count: commands is non-negative integer"
assert_component_count "version.json" "['components']['memory_files']" "Component count: memory_files is non-negative integer"
assert_component_count "version.json" "['components']['context_templates']" "Component count: context_templates is non-negative integer"
assert_component_count "version.json" "['components']['protocols']" "Component count: protocols is non-negative integer"

echo ""

################################################################################
# TEST GROUP 8: Component Counts - Expected Values
################################################################################

echo -e "${BLUE}Test Group 8: Component Counts - Expected Values${NC}"
echo ""

((TESTS_RUN++))
local skills_count=$(python3 -c "import json; print(json.load(open('version.json')).get('components', {}).get('skills', 0))" 2>/dev/null)
if [ "$skills_count" -eq 9 ] || [ "$skills_count" -eq 10 ]; then
    echo -e "${GREEN}✓ PASS${NC}: Skills count is 9 or 10 (matches framework)"
    echo "  Count: $skills_count"
    ((TESTS_PASSED++))
else
    echo -e "${RED}✗ FAIL${NC}: Skills count should be 9 or 10"
    echo "  Count: $skills_count (expected: 9 or 10)"
    ((TESTS_FAILED++))
fi

((TESTS_RUN++))
local agents_count=$(python3 -c "import json; print(json.load(open('version.json')).get('components', {}).get('agents', 0))" 2>/dev/null)
if [ "$agents_count" -eq 21 ] || [ "$agents_count" -ge 20 ]; then
    echo -e "${GREEN}✓ PASS${NC}: Agents count is 21+ (matches framework)"
    echo "  Count: $agents_count"
    ((TESTS_PASSED++))
else
    echo -e "${RED}✗ FAIL${NC}: Agents count should be ≥20"
    echo "  Count: $agents_count (expected: ≥20)"
    ((TESTS_FAILED++))
fi

((TESTS_RUN++))
local commands_count=$(python3 -c "import json; print(json.load(open('version.json')).get('components', {}).get('commands', 0))" 2>/dev/null)
if [ "$commands_count" -ge 13 ]; then
    echo -e "${GREEN}✓ PASS${NC}: Commands count is 13+ (matches framework)"
    echo "  Count: $commands_count"
    ((TESTS_PASSED++))
else
    echo -e "${RED}✗ FAIL${NC}: Commands count should be ≥13"
    echo "  Count: $commands_count (expected: ≥13)"
    ((TESTS_FAILED++))
fi

echo ""

################################################################################
# TEST GROUP 9: Migration Status Fields
################################################################################

echo -e "${BLUE}Test Group 9: Migration Status Fields${NC}"
echo ""

assert_json_field "version.json" "['migration_status']['phase']" "Migration status: phase field exists"
assert_json_field "version.json" "['migration_status']['src_structure_complete']" "Migration status: src_structure_complete field exists"
assert_json_field "version.json" "['migration_status']['content_migration_complete']" "Migration status: content_migration_complete field exists"
assert_json_field "version.json" "['migration_status']['installer_ready']" "Migration status: installer_ready field exists"

echo ""

################################################################################
# TEST GROUP 10: Migration Status Phase Value
################################################################################

echo -e "${BLUE}Test Group 10: Migration Status Phase Value${NC}"
echo ""

((TESTS_RUN++))
local phase=$(python3 -c "import json; print(json.load(open('version.json')).get('migration_status', {}).get('phase', ''))" 2>/dev/null)
if [ "$phase" = "1-directory-setup" ]; then
    echo -e "${GREEN}✓ PASS${NC}: Phase is '1-directory-setup'"
    echo "  Phase: $phase"
    ((TESTS_PASSED++))
else
    echo -e "${RED}✗ FAIL${NC}: Phase should be '1-directory-setup'"
    echo "  Phase: $phase (expected: '1-directory-setup')"
    ((TESTS_FAILED++))
fi

echo ""

################################################################################
# TEST GROUP 11: Migration Status Boolean Values
################################################################################

echo -e "${BLUE}Test Group 11: Migration Status Boolean Values${NC}"
echo ""

((TESTS_RUN++))
local src_complete=$(python3 -c "import json; print(json.load(open('version.json')).get('migration_status', {}).get('src_structure_complete', 'null'))" 2>/dev/null)
if [ "$src_complete" = "True" ] || [ "$src_complete" = "true" ]; then
    echo -e "${GREEN}✓ PASS${NC}: src_structure_complete is true"
    echo "  Value: $src_complete"
    ((TESTS_PASSED++))
else
    echo -e "${RED}✗ FAIL${NC}: src_structure_complete should be true"
    echo "  Value: $src_complete (expected: true)"
    ((TESTS_FAILED++))
fi

((TESTS_RUN++))
local content_complete=$(python3 -c "import json; print(json.load(open('version.json')).get('migration_status', {}).get('content_migration_complete', 'null'))" 2>/dev/null)
if [ "$content_complete" = "False" ] || [ "$content_complete" = "false" ]; then
    echo -e "${GREEN}✓ PASS${NC}: content_migration_complete is false (Phase 2 work)"
    echo "  Value: $content_complete"
    ((TESTS_PASSED++))
else
    echo -e "${RED}✗ FAIL${NC}: content_migration_complete should be false"
    echo "  Value: $content_complete (expected: false)"
    ((TESTS_FAILED++))
fi

((TESTS_RUN++))
local installer_ready=$(python3 -c "import json; print(json.load(open('version.json')).get('migration_status', {}).get('installer_ready', 'null'))" 2>/dev/null)
if [ "$installer_ready" = "False" ] || [ "$installer_ready" = "false" ]; then
    echo -e "${GREEN}✓ PASS${NC}: installer_ready is false (Phase 5 work)"
    echo "  Value: $installer_ready"
    ((TESTS_PASSED++))
else
    echo -e "${RED}✗ FAIL${NC}: installer_ready should be false"
    echo "  Value: $installer_ready (expected: false)"
    ((TESTS_FAILED++))
fi

echo ""

################################################################################
# TEST GROUP 12: Changelog URL Field
################################################################################

echo -e "${BLUE}Test Group 12: Changelog URL Field${NC}"
echo ""

((TESTS_RUN++))
local changelog_url=$(python3 -c "import json; print(json.load(open('version.json')).get('changelog_url', ''))" 2>/dev/null)
if [ "$changelog_url" = "devforgeai/CHANGELOG.md" ]; then
    echo -e "${GREEN}✓ PASS${NC}: changelog_url is correct"
    echo "  URL: $changelog_url"
    ((TESTS_PASSED++))
else
    echo -e "${RED}✗ FAIL${NC}: changelog_url should be 'devforgeai/CHANGELOG.md'"
    echo "  URL: $changelog_url"
    ((TESTS_FAILED++))
fi

echo ""

################################################################################
# TEST GROUP 13: No Sensitive Data in JSON
################################################################################

echo -e "${BLUE}Test Group 13: No Sensitive Data in JSON${NC}"
echo ""

((TESTS_RUN++))
if ! grep -iE '(api_key|token|password|secret)' "version.json" > /dev/null 2>&1; then
    echo -e "${GREEN}✓ PASS${NC}: No sensitive data (API keys, tokens, passwords) in version.json"
    echo "  Check: grep for api_key, token, password, secret returned 0 matches"
    ((TESTS_PASSED++))
else
    echo -e "${RED}✗ FAIL${NC}: Sensitive data found in version.json"
    echo "  Contains: API keys, tokens, or passwords"
    ((TESTS_FAILED++))
fi

echo ""

################################################################################
# TEST SUMMARY
################################################################################

echo -e "${BLUE}═══════════════════════════════════════════════════════════════${NC}"
echo -e "${BLUE}TEST SUMMARY: AC#3${NC}"
echo -e "${BLUE}═══════════════════════════════════════════════════════════════${NC}"
echo ""
echo "Tests Run:    $TESTS_RUN"
echo "Tests Passed: $TESTS_PASSED"
echo "Tests Failed: $TESTS_FAILED"
echo ""

if [ $TESTS_FAILED -gt 0 ]; then
    echo -e "${RED}STATUS: FAILING (Red Phase) ✗${NC}"
    echo ""
    echo "Expected: All tests should be FAILING initially (TDD Red phase)"
    echo "Reason:   version.json does not yet exist or has incorrect schema"
    echo ""
    echo "Next Step (Green Phase): Create version.json with valid schema"
    echo ""
    exit 1
else
    echo -e "${GREEN}STATUS: PASSING ✓${NC}"
    echo ""
    echo "All assertions passed. AC#3 requirements satisfied."
    echo ""
    exit 0
fi
