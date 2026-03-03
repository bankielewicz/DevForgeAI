#!/bin/bash

##############################################################################
# Test Suite: STORY-390 AC#1 - Version Snapshot Captured on Component Modification
# Purpose: Verify capture subcommand reads file content, computes SHA-256,
#          writes snapshot to devforgeai/specs/prompt-versions/{component_id}/
#          with naming {timestamp}-{short_hash}.snapshot.md
#
# Implementation: src/claude/commands/prompt-version.md (Slash Command)
# Test Type: Structural + Pattern (Markdown Command Testing Pattern)
#
# All tests MUST FAIL (TDD RED) until implementation exists.
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

# Paths
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="${SCRIPT_DIR}/../.."
IMPL_FILE="${PROJECT_ROOT}/src/claude/commands/prompt-version.md"

##############################################################################
# Test Framework Functions
##############################################################################

run_test() {
    local test_name=$1
    local test_func=$2

    TESTS_RUN=$((TESTS_RUN + 1))
    echo -e "\n${BLUE}[Test $TESTS_RUN]${NC} $test_name"

    if $test_func 2>/dev/null; then
        TESTS_PASSED=$((TESTS_PASSED + 1))
        echo -e "  ${GREEN}PASS${NC}: $test_name"
    else
        TESTS_FAILED=$((TESTS_FAILED + 1))
        echo -e "  ${RED}FAIL${NC}: $test_name"
    fi
}

##############################################################################
# AC#1 Tests: Version Snapshot Captured on Component Modification
##############################################################################

# --- Structural Tests ---

test_implementation_file_exists() {
    # The implementation file must exist at src/claude/commands/prompt-version.md
    [ -f "$IMPL_FILE" ]
}

test_has_yaml_frontmatter() {
    # Slash commands MUST have YAML frontmatter with description and argument-hint
    head -5 "$IMPL_FILE" | grep -q "^---"
}

test_has_description_field() {
    # YAML frontmatter must contain description field
    grep -qE "^description:" "$IMPL_FILE"
}

test_has_argument_hint_field() {
    # YAML frontmatter must contain argument-hint field
    grep -qE "^argument-hint:" "$IMPL_FILE"
}

test_has_capture_subcommand_section() {
    # Must have a section documenting the capture subcommand
    grep -qiE "^#{1,3}.*[Cc]apture" "$IMPL_FILE"
}

test_has_snapshot_directory_reference() {
    # Must reference the snapshot storage path: devforgeai/specs/prompt-versions/
    grep -q "devforgeai/specs/prompt-versions/" "$IMPL_FILE"
}

# --- Pattern Tests: SHA-256 Hash Computation ---

test_capture_references_sha256() {
    # Capture subcommand must reference SHA-256 hash computation
    grep -qiE "(sha-?256|sha256sum|hashlib)" "$IMPL_FILE"
}

test_capture_references_read_tool() {
    # Capture must use Read() tool to read component file content
    grep -qE 'Read\(' "$IMPL_FILE"
}

test_capture_references_write_tool() {
    # Capture must use Write() tool to create snapshot file
    grep -qE 'Write\(' "$IMPL_FILE"
}

test_capture_references_bash_sha256() {
    # Must reference Bash for SHA-256 computation (sha256sum or python hashlib fallback)
    grep -qE "(Bash.*sha256|sha256sum|hashlib\.sha256)" "$IMPL_FILE"
}

# --- Pattern Tests: Snapshot File Structure ---

test_snapshot_naming_pattern() {
    # Snapshot filename must follow {timestamp}-{short_hash}.snapshot.md pattern
    grep -qE "\{?timestamp\}?.*\{?short.?hash\}?.*\.snapshot\.md" "$IMPL_FILE"
}

test_snapshot_has_component_id_field() {
    # Snapshot must contain component_id field
    grep -q "component_id" "$IMPL_FILE"
}

test_snapshot_has_component_type_field() {
    # Snapshot must contain component_type field
    grep -q "component_type" "$IMPL_FILE"
}

test_snapshot_has_file_path_field() {
    # Snapshot must contain file_path field
    grep -q "file_path" "$IMPL_FILE"
}

test_snapshot_has_before_hash_field() {
    # Snapshot must contain before_hash field
    grep -q "before_hash" "$IMPL_FILE"
}

test_snapshot_has_capture_timestamp_field() {
    # Snapshot must contain capture_timestamp field (ISO-8601)
    grep -q "capture_timestamp" "$IMPL_FILE"
}

test_snapshot_has_before_content_section() {
    # Snapshot must contain before_content section for full content storage
    grep -q "before_content" "$IMPL_FILE"
}

# --- Pattern Tests: Confirmation Output ---

test_capture_outputs_component_name() {
    # Capture confirmation must include component name display
    grep -qiE "(component.?name|component_id|Display.*component)" "$IMPL_FILE"
}

test_capture_outputs_hash() {
    # Capture confirmation must include the computed hash
    grep -qiE "(before_hash|hash.*confirm|Display.*hash)" "$IMPL_FILE"
}

test_capture_outputs_snapshot_path() {
    # Capture confirmation must include the snapshot file path
    grep -qiE "(snapshot.?path|snapshot.*file|Display.*snapshot)" "$IMPL_FILE"
}

# --- Business Rule Tests ---

test_br001_component_id_validation_pattern() {
    # BR-001: Component ID must match ^[a-z][a-z0-9-]{1,63}$
    grep -qE '\^?\[a-z\]' "$IMPL_FILE"
}

test_br003_file_path_prefix_validation() {
    # BR-003: File paths must start with src/claude/ and end with .md
    grep -qE "src/claude/" "$IMPL_FILE" && grep -qE "\.md" "$IMPL_FILE"
}

test_br004_sha256_hash_format() {
    # BR-004: SHA-256 hash format ^[0-9a-f]{64}$ or sentinel NEW_COMPONENT
    grep -qE "(\[0-9a-f\]\{64\}|NEW_COMPONENT)" "$IMPL_FILE"
}

test_br008_new_component_sentinel() {
    # BR-008: New components use NEW_COMPONENT sentinel as before_hash
    grep -q "NEW_COMPONENT" "$IMPL_FILE"
}

# --- Edge Case Tests ---

test_handles_nonexistent_component_file() {
    # Must handle case where component file does not exist
    grep -qiE "(file.*not.*found|does.*not.*exist|HALT.*missing)" "$IMPL_FILE"
}

test_handles_iso8601_timestamp() {
    # Must use ISO-8601 timestamp format
    grep -qiE "(ISO.?8601|YYYY-MM-DD|iso.*timestamp)" "$IMPL_FILE"
}

##############################################################################
# Test Execution
##############################################################################

echo "=============================================="
echo "  STORY-390 AC#1: Version Snapshot Capture"
echo "  TDD Phase: RED (tests must fail)"
echo "=============================================="

# Structural Tests
run_test "Implementation file exists" test_implementation_file_exists
run_test "Has YAML frontmatter" test_has_yaml_frontmatter
run_test "Has description field" test_has_description_field
run_test "Has argument-hint field" test_has_argument_hint_field
run_test "Has capture subcommand section" test_has_capture_subcommand_section
run_test "Has snapshot directory reference" test_has_snapshot_directory_reference

# Pattern Tests: SHA-256
run_test "Capture references SHA-256" test_capture_references_sha256
run_test "Capture references Read() tool" test_capture_references_read_tool
run_test "Capture references Write() tool" test_capture_references_write_tool
run_test "Capture references Bash sha256" test_capture_references_bash_sha256

# Pattern Tests: Snapshot Structure
run_test "Snapshot naming pattern" test_snapshot_naming_pattern
run_test "Snapshot has component_id" test_snapshot_has_component_id_field
run_test "Snapshot has component_type" test_snapshot_has_component_type_field
run_test "Snapshot has file_path" test_snapshot_has_file_path_field
run_test "Snapshot has before_hash" test_snapshot_has_before_hash_field
run_test "Snapshot has capture_timestamp" test_snapshot_has_capture_timestamp_field
run_test "Snapshot has before_content" test_snapshot_has_before_content_section

# Pattern Tests: Confirmation Output
run_test "Capture outputs component name" test_capture_outputs_component_name
run_test "Capture outputs hash" test_capture_outputs_hash
run_test "Capture outputs snapshot path" test_capture_outputs_snapshot_path

# Business Rule Tests
run_test "BR-001: Component ID validation" test_br001_component_id_validation_pattern
run_test "BR-003: File path prefix validation" test_br003_file_path_prefix_validation
run_test "BR-004: SHA-256 hash format" test_br004_sha256_hash_format
run_test "BR-008: NEW_COMPONENT sentinel" test_br008_new_component_sentinel

# Edge Case Tests
run_test "Handles nonexistent component file" test_handles_nonexistent_component_file
run_test "Handles ISO-8601 timestamp" test_handles_iso8601_timestamp

##############################################################################
# Summary
##############################################################################

echo ""
echo "=============================================="
echo "  AC#1 Test Results"
echo "=============================================="
echo -e "  Total:  ${TESTS_RUN}"
echo -e "  Passed: ${GREEN}${TESTS_PASSED}${NC}"
echo -e "  Failed: ${RED}${TESTS_FAILED}${NC}"
echo "=============================================="

if [ "$TESTS_FAILED" -gt 0 ]; then
    echo -e "${RED}RESULT: FAIL${NC} - $TESTS_FAILED test(s) failed (TDD RED confirmed)"
    exit 1
else
    echo -e "${GREEN}RESULT: PASS${NC} - All tests passed"
    exit 0
fi
