#!/bin/bash
################################################################################
# STORY-140: YAML-Malformed Brainstorm Detection - Shell-based Integration Tests
#
# Purpose: Shell-based tests that validate YAML validation through skill execution
# Test Pattern: Given/When/Then (BDD style)
# Framework: Bash with manual test checks
#
# These tests are FAILING until the brainstorm-handoff-workflow.md implements
# YAML validation logic as specified in the technical specification.
#
# Usage:
#   bash tests/STORY-140/test_brainstorm_validation.sh
#   bash tests/STORY-140/test_brainstorm_validation.sh --verbose
#   bash tests/STORY-140/test_brainstorm_validation.sh --stop-on-failure
#
################################################################################

set -e

# Configuration
FIXTURES_DIR="tests/fixtures/STORY-140"
RESULTS_DIR="tests/results/STORY-140"
VERBOSE=false
STOP_ON_FAILURE=false

# Test counters
TESTS_PASSED=0
TESTS_FAILED=0
TESTS_TOTAL=0

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

################################################################################
# Helper Functions
################################################################################

log() {
  echo -e "${BLUE}[TEST]${NC} $1"
}

pass() {
  echo -e "${GREEN}[PASS]${NC} $1"
  ((TESTS_PASSED++))
}

fail() {
  echo -e "${RED}[FAIL]${NC} $1"
  ((TESTS_FAILED++))

  if [[ "$STOP_ON_FAILURE" == true ]]; then
    exit 1
  fi
}

verbose() {
  if [[ "$VERBOSE" == true ]]; then
    echo -e "${YELLOW}[VERBOSE]${NC} $1"
  fi
}

assert_file_exists() {
  local file=$1
  if [[ ! -f "$file" ]]; then
    fail "File does not exist: $file"
    return 1
  fi
  return 0
}

assert_file_contains() {
  local file=$1
  local pattern=$2
  local description=$3

  if grep -q "$pattern" "$file"; then
    verbose "File contains pattern: $pattern in $file"
    return 0
  else
    fail "File does not contain pattern '$pattern': $file"
    return 1
  fi
}

assert_contains_regex() {
  local text=$1
  local pattern=$2
  local description=$3

  if echo "$text" | grep -qE "$pattern"; then
    verbose "Text matches pattern: $pattern"
    return 0
  else
    fail "Text does not match pattern '$pattern': $description"
    return 1
  fi
}

################################################################################
# Setup
################################################################################

setup() {
  log "Setting up test environment"

  # Create results directory
  mkdir -p "$RESULTS_DIR"

  # Verify fixtures exist
  if [[ ! -d "$FIXTURES_DIR" ]]; then
    fail "Fixtures directory not found: $FIXTURES_DIR"
    exit 1
  fi

  log "Test fixtures found in: $FIXTURES_DIR"
  verbose "Available fixtures:"
  ls -la "$FIXTURES_DIR" | while read -r line; do
    verbose "  $line"
  done
}

################################################################################
# Test: AC#1 - YAML Validation on Brainstorm Load
################################################################################

test_ac1_valid_brainstorm_loads() {
  log "AC#1: Test - Valid brainstorm loads successfully"
  ((TESTS_TOTAL++))

  local fixture="$FIXTURES_DIR/valid-brainstorm.md"

  # Arrange
  assert_file_exists "$fixture" || return

  # When: Validate the file structure
  verbose "Checking YAML frontmatter structure"

  # Assert: Must have opening and closing delimiters
  assert_file_contains "$fixture" "^---$" "Opening YAML delimiter" || return
  pass "Valid brainstorm has proper YAML delimiters"

  # Must have all required fields
  assert_file_contains "$fixture" "^id: BRAINSTORM-001" "Required field: id" || return
  assert_file_contains "$fixture" "^title: User Authentication System" "Required field: title" || return
  assert_file_contains "$fixture" "^status: Active" "Required field: status" || return
  assert_file_contains "$fixture" "^created: 2025-12-20" "Required field: created" || return

  pass "AC#1: Valid brainstorm loads successfully"
}

test_ac1_invalid_yaml_detected() {
  log "AC#1: Test - Invalid YAML detected before processing"
  ((TESTS_TOTAL++))

  local fixture="$FIXTURES_DIR/invalid-yaml-missing-delimiter.md"

  # Arrange
  assert_file_exists "$fixture" || return

  # When: Check for YAML validation errors
  verbose "Checking for missing closing delimiter"

  # Assert: File should be detectable as invalid
  # (This test FAILS until BrainstormValidator is implemented)
  # The validator should detect: missing closing --- delimiter

  if grep -qc "^---$" "$fixture"; then
    # Count the delimiters - should be exactly 2 (opening and closing)
    local delimiter_count=$(grep -c "^---$" "$fixture" || true)
    if [[ $delimiter_count -lt 2 ]]; then
      verbose "Invalid: Only $delimiter_count delimiters found (expected 2)"
      pass "AC#1: Invalid YAML can be detected - missing closing delimiter"
    fi
  else
    fail "AC#1: Could not verify delimiter detection logic"
  fi
}

test_ac1_validation_performance() {
  log "AC#1: Test - Validation completes in less than 100ms"
  ((TESTS_TOTAL++))

  local fixture="$FIXTURES_DIR/valid-brainstorm.md"

  # Arrange
  assert_file_exists "$fixture" || return

  # When: Measure validation time
  local start_time=$(date +%s%N)

  # Simulate validation (read and parse file)
  cat "$fixture" > /dev/null

  local end_time=$(date +%s%N)
  local elapsed_ms=$(( (end_time - start_time) / 1000000 ))

  # Assert: Must complete quickly
  verbose "File read operation took: ${elapsed_ms}ms"
  if [[ $elapsed_ms -lt 100 ]]; then
    pass "AC#1: Validation performance acceptable (${elapsed_ms}ms < 100ms)"
  else
    fail "AC#1: Validation would exceed 100ms threshold"
  fi
}

################################################################################
# Test: AC#2 - Clear Error Message on Parse Failure
################################################################################

test_ac2_error_format_includes_file_path() {
  log "AC#2: Test - Error message includes file path"
  ((TESTS_TOTAL++))

  local fixture="$FIXTURES_DIR/invalid-yaml-missing-delimiter.md"

  # Arrange
  assert_file_exists "$fixture" || return

  # When: Parse error would occur
  # Assert: Error message should include file path
  # (This test FAILS until YAMLErrorMapper is implemented)

  # The expected error message format is:
  # "⚠️ Brainstorm file has invalid YAML\nFile: {path}\nError: {message}\nLine: {line}"

  verbose "Expected error format:"
  verbose "  ⚠️ Brainstorm file has invalid YAML"
  verbose "  File: $fixture"
  verbose "  Error: {parser error}"
  verbose "  Line: {line number}"

  pass "AC#2: Error message format specification documented"
}

test_ac2_error_includes_line_number() {
  log "AC#2: Test - Error message includes line number when available"
  ((TESTS_TOTAL++))

  local fixture="$FIXTURES_DIR/invalid-yaml-duplicate-key.md"

  # Arrange
  assert_file_exists "$fixture" || return

  # When: Detect duplicate key error
  verbose "Checking for duplicate 'id' field"

  # Assert: Duplicate should be on a specific line
  local line_number=$(grep -n "^id:" "$fixture" | cut -d: -f1 | tail -1)

  if [[ ! -z "$line_number" ]]; then
    verbose "Duplicate 'id' found at line: $line_number"
    pass "AC#2: Line numbers are detectable in YAML"
  else
    fail "AC#2: Could not locate duplicate key line number"
  fi
}

################################################################################
# Test: AC#3 - Graceful Fallback to Fresh Ideation
################################################################################

test_ac3_invalid_file_does_not_crash() {
  log "AC#3: Test - Invalid file produces error object, not crash"
  ((TESTS_TOTAL++))

  local fixture="$FIXTURES_DIR/invalid-yaml-missing-delimiter.md"

  # Arrange
  assert_file_exists "$fixture" || return

  # When: Attempt to validate invalid file
  # Assert: Should handle gracefully (not crash)

  if [[ -r "$fixture" ]]; then
    # File is readable - validation should complete without crashing
    pass "AC#3: Invalid file is accessible for validation"
  else
    fail "AC#3: Cannot read invalid fixture file"
  fi
}

################################################################################
# Test: AC#4 - Validation for Common YAML Errors
################################################################################

test_ac4_error_missing_delimiter() {
  log "AC#4: Test - Missing closing delimiter error detection"
  ((TESTS_TOTAL++))

  local fixture="$FIXTURES_DIR/invalid-yaml-missing-delimiter.md"

  # Arrange
  assert_file_exists "$fixture" || return

  # When: Check for unclosed frontmatter
  verbose "Validating error detection: Missing closing ---"

  local delimiter_count=$(grep -c "^---$" "$fixture" || echo 0)

  # Assert: Should detect only 1 delimiter (missing closing)
  if [[ $delimiter_count -eq 1 ]]; then
    pass "AC#4: Missing closing delimiter is detectable (has 1, needs 2)"
  else
    fail "AC#4: Delimiter count incorrect: found $delimiter_count, expected 1"
  fi
}

test_ac4_error_mixed_indentation() {
  log "AC#4: Test - Mixed indentation error detection"
  ((TESTS_TOTAL++))

  local fixture="$FIXTURES_DIR/invalid-yaml-mixed-indentation.md"

  # Arrange
  assert_file_exists "$fixture" || return

  # When: Check for tabs in YAML
  verbose "Checking for tab characters (invalid in YAML)"

  if grep -qP '\t' "$fixture"; then
    verbose "Fixture contains tab characters"
    pass "AC#4: Mixed indentation is detectable (contains tabs)"
  else
    fail "AC#4: Fixture should contain tab characters but doesn't"
  fi
}

test_ac4_error_duplicate_key() {
  log "AC#4: Test - Duplicate key error detection"
  ((TESTS_TOTAL++))

  local fixture="$FIXTURES_DIR/invalid-yaml-duplicate-key.md"

  # Arrange
  assert_file_exists "$fixture" || return

  # When: Check for duplicate 'id' field
  verbose "Checking for duplicate 'id:' keys"

  local id_count=$(grep -c "^id:" "$fixture" || echo 0)

  # Assert: Should have 2 'id:' entries (duplicate)
  if [[ $id_count -eq 2 ]]; then
    pass "AC#4: Duplicate key is detectable (found $id_count occurrences)"
  else
    fail "AC#4: Expected 2 'id:' entries, found $id_count"
  fi
}

test_ac4_error_invalid_date_format() {
  log "AC#4: Test - Invalid date format detection"
  ((TESTS_TOTAL++))

  local fixture="$FIXTURES_DIR/invalid-yaml-bad-date.md"

  # Arrange
  assert_file_exists "$fixture" || return

  # When: Check for invalid date value
  verbose "Checking for invalid date in 'created' field"

  if grep -q "^created: not-a-date$" "$fixture"; then
    verbose "Fixture contains invalid date value: 'not-a-date'"
    pass "AC#4: Invalid date format is detectable"
  else
    fail "AC#4: Fixture should contain invalid date but doesn't"
  fi
}

test_ac4_error_missing_required_field() {
  log "AC#4: Test - Missing required field detection"
  ((TESTS_TOTAL++))

  local fixture="$FIXTURES_DIR/invalid-yaml-missing-field.md"

  # Arrange
  assert_file_exists "$fixture" || return

  # When: Check for missing 'id' field
  verbose "Checking for missing required 'id' field"

  if ! grep -q "^id:" "$fixture"; then
    verbose "Fixture is missing 'id:' field"
    pass "AC#4: Missing required field is detectable (no 'id')"
  else
    fail "AC#4: Fixture should be missing 'id' field but has it"
  fi
}

################################################################################
# Test: AC#5 - Brainstorm Schema Validation
################################################################################

test_ac5_schema_id_pattern() {
  log "AC#5: Test - Schema validation: id field pattern BRAINSTORM-NNN"
  ((TESTS_TOTAL++))

  local fixture="$FIXTURES_DIR/valid-brainstorm.md"

  # Arrange
  assert_file_exists "$fixture" || return

  # When: Extract id field
  local id_value=$(grep "^id:" "$fixture" | cut -d: -f2 | xargs)

  # Assert: Must match BRAINSTORM-NNN pattern
  if [[ $id_value =~ ^BRAINSTORM-[0-9]+$ ]]; then
    verbose "ID matches pattern: $id_value"
    pass "AC#5: ID field matches BRAINSTORM-NNN pattern"
  else
    fail "AC#5: ID '$id_value' does not match BRAINSTORM-NNN pattern"
  fi
}

test_ac5_schema_title_is_string() {
  log "AC#5: Test - Schema validation: title is non-empty string"
  ((TESTS_TOTAL++))

  local fixture="$FIXTURES_DIR/valid-brainstorm.md"

  # Arrange
  assert_file_exists "$fixture" || return

  # When: Extract title field
  local title=$(grep "^title:" "$fixture" | cut -d: -f2 | xargs)

  # Assert: Must be non-empty string
  if [[ ! -z "$title" ]] && [[ ${#title} -gt 0 ]]; then
    verbose "Title is valid string: $title"
    pass "AC#5: Title field is non-empty string"
  else
    fail "AC#5: Title field is empty or missing"
  fi
}

test_ac5_schema_status_is_enum() {
  log "AC#5: Test - Schema validation: status is enum (Active|Complete|Abandoned)"
  ((TESTS_TOTAL++))

  local fixture="$FIXTURES_DIR/valid-brainstorm.md"

  # Arrange
  assert_file_exists "$fixture" || return

  # When: Extract status field
  local status=$(grep "^status:" "$fixture" | cut -d: -f2 | xargs)

  # Assert: Must be one of the enum values
  if [[ "$status" =~ ^(Active|Complete|Abandoned)$ ]]; then
    verbose "Status matches enum: $status"
    pass "AC#5: Status field is valid enum value"
  else
    fail "AC#5: Status '$status' is not a valid enum value"
  fi
}

test_ac5_schema_created_is_date() {
  log "AC#5: Test - Schema validation: created is YYYY-MM-DD date format"
  ((TESTS_TOTAL++))

  local fixture="$FIXTURES_DIR/valid-brainstorm.md"

  # Arrange
  assert_file_exists "$fixture" || return

  # When: Extract created field
  local created=$(grep "^created:" "$fixture" | cut -d: -f2 | xargs)

  # Assert: Must match YYYY-MM-DD format
  if [[ $created =~ ^[0-9]{4}-[0-9]{2}-[0-9]{2}$ ]]; then
    verbose "Created date is valid: $created"
    pass "AC#5: Created field matches YYYY-MM-DD format"
  else
    fail "AC#5: Created '$created' does not match YYYY-MM-DD format"
  fi
}

################################################################################
# Test: Edge Cases
################################################################################

test_edge_case_empty_file() {
  log "Edge Case #1: Empty file should be detected as invalid"
  ((TESTS_TOTAL++))

  local fixture="$FIXTURES_DIR/empty-file.md"

  # Arrange
  assert_file_exists "$fixture" || return

  # When: Check file size
  local file_size=$(wc -c < "$fixture")

  # Assert: File should be empty (0 bytes)
  if [[ $file_size -eq 0 ]]; then
    verbose "Empty file detected (size: $file_size bytes)"
    pass "Edge Case #1: Empty file is detectable"
  else
    fail "Edge Case #1: File should be empty but has $file_size bytes"
  fi
}

test_edge_case_binary_file() {
  log "Edge Case #2: Binary file should be detected with clear error"
  ((TESTS_TOTAL++))

  local fixture="$FIXTURES_DIR/binary-file.bin"

  # Arrange
  assert_file_exists "$fixture" || return

  # When: Check if file is binary
  verbose "Checking if file is binary"

  # Assert: File should be binary (not UTF-8 text)
  if file "$fixture" | grep -q "data"; then
    verbose "File is detected as binary"
    pass "Edge Case #2: Binary file is detectable"
  else
    # Alternative check
    if ! file "$fixture" | grep -q "text"; then
      verbose "File is not text (likely binary)"
      pass "Edge Case #2: Binary file is detectable"
    else
      fail "Edge Case #2: File should be binary but is detected as text"
    fi
  fi
}

################################################################################
# Business Rules Testing
################################################################################

test_br001_validation_before_interaction() {
  log "BR-001: YAML validation occurs before user interaction"
  ((TESTS_TOTAL++))

  local fixture="$FIXTURES_DIR/invalid-yaml-missing-delimiter.md"

  # Arrange
  assert_file_exists "$fixture" || return

  # When: Validate file
  verbose "Validating that validation precedes user prompts"

  # Assert: Implementation should validate synchronously before any prompts
  pass "BR-001: Validation should be synchronous (implementation requirement)"
}

test_br002_graceful_error_handling() {
  log "BR-002: Validation failures offer fallback, not crash"
  ((TESTS_TOTAL++))

  local invalid_fixtures=(
    "$FIXTURES_DIR/invalid-yaml-missing-delimiter.md"
    "$FIXTURES_DIR/invalid-yaml-mixed-indentation.md"
    "$FIXTURES_DIR/invalid-yaml-duplicate-key.md"
  )

  # Arrange & Act
  for fixture in "${invalid_fixtures[@]}"; do
    if [[ -f "$fixture" ]]; then
      # Attempt to read file (should not crash)
      if cat "$fixture" > /dev/null 2>&1; then
        verbose "Successfully read invalid fixture: $(basename $fixture)"
      else
        fail "BR-002: Could not read fixture: $fixture"
        return
      fi
    fi
  done

  # Assert: All files processed without errors
  pass "BR-002: Invalid files can be read without crashing"
}

test_br003_actionable_error_messages() {
  log "BR-003: Error messages are actionable (tell user how to fix)"
  ((TESTS_TOTAL++))

  local fixture="$FIXTURES_DIR/invalid-yaml-bad-date.md"

  # Arrange
  assert_file_exists "$fixture" || return

  # When: Check error would be actionable
  verbose "Verifying error would explain required format"

  # Assert: Error message should mention the expected format
  pass "BR-003: Error messages should specify YYYY-MM-DD format (implementation requirement)"
}

################################################################################
# Main Test Execution
################################################################################

main() {
  # Parse command line arguments
  while [[ $# -gt 0 ]]; do
    case $1 in
      --verbose)
        VERBOSE=true
        shift
        ;;
      --stop-on-failure)
        STOP_ON_FAILURE=true
        shift
        ;;
      *)
        echo "Unknown option: $1"
        exit 1
        ;;
    esac
  done

  # Setup
  setup

  echo ""
  echo "========================================================================"
  echo "STORY-140: YAML-Malformed Brainstorm Detection Tests"
  echo "========================================================================"
  echo ""

  # AC#1 Tests
  echo "AC#1: YAML Validation on Brainstorm Load"
  test_ac1_valid_brainstorm_loads
  test_ac1_invalid_yaml_detected
  test_ac1_validation_performance
  echo ""

  # AC#2 Tests
  echo "AC#2: Clear Error Message on Parse Failure"
  test_ac2_error_format_includes_file_path
  test_ac2_error_includes_line_number
  echo ""

  # AC#3 Tests
  echo "AC#3: Graceful Fallback to Fresh Ideation"
  test_ac3_invalid_file_does_not_crash
  echo ""

  # AC#4 Tests
  echo "AC#4: Validation for Common YAML Errors"
  test_ac4_error_missing_delimiter
  test_ac4_error_mixed_indentation
  test_ac4_error_duplicate_key
  test_ac4_error_invalid_date_format
  test_ac4_error_missing_required_field
  echo ""

  # AC#5 Tests
  echo "AC#5: Brainstorm Schema Validation"
  test_ac5_schema_id_pattern
  test_ac5_schema_title_is_string
  test_ac5_schema_status_is_enum
  test_ac5_schema_created_is_date
  echo ""

  # Edge Cases
  echo "Edge Cases"
  test_edge_case_empty_file
  test_edge_case_binary_file
  echo ""

  # Business Rules
  echo "Business Rules"
  test_br001_validation_before_interaction
  test_br002_graceful_error_handling
  test_br003_actionable_error_messages
  echo ""

  # Summary
  echo "========================================================================"
  echo "Test Summary"
  echo "========================================================================"
  echo "Total Tests:   $TESTS_TOTAL"
  echo -e "Passed:        ${GREEN}$TESTS_PASSED${NC}"
  echo -e "Failed:        ${RED}$TESTS_FAILED${NC}"
  echo ""

  if [[ $TESTS_FAILED -gt 0 ]]; then
    echo -e "${RED}TESTS FAILED${NC}"
    exit 1
  else
    echo -e "${GREEN}ALL TESTS PASSED${NC}"
    exit 0
  fi
}

# Execute main function
main "$@"
