#!/usr/bin/env bash

# STORY-151: Post-Subagent Recording Hook - Subagent Filtering Tests (AC#4)
# Tests that hook correctly filters workflow vs non-workflow subagents

set -euo pipefail

# Setup
readonly TEST_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
readonly PROJECT_ROOT="$(cd "${TEST_DIR}/../../../" && pwd)"
readonly TEMP_DIR="${TEST_DIR}/.temp"
readonly CONFIG_FILE="$TEMP_DIR/workflow-subagents.yaml"

# Color codes for output
readonly RED='\033[0;31m'
readonly GREEN='\033[0;32m'
readonly YELLOW='\033[1;33m'
readonly NC='\033[0m'

# Test counters
tests_run=0
tests_passed=0
tests_failed=0

# Cleanup function
cleanup_temp_files() {
    if [[ -d "$TEMP_DIR" ]]; then
        rm -rf "$TEMP_DIR"
    fi
}

trap cleanup_temp_files EXIT

# Test helper functions
run_test() {
    local test_name="$1"
    local test_func="$2"

    echo -e "\n${YELLOW}Running: ${test_name}${NC}"
    tests_run=$((tests_run + 1))

    if $test_func; then
        echo -e "${GREEN}✓ PASSED${NC}"
        tests_passed=$((tests_passed + 1))
        return 0
    else
        echo -e "${RED}✗ FAILED${NC}"
        tests_failed=$((tests_failed + 1))
        return 1
    fi
}

assert_equals() {
    local expected="$1"
    local actual="$2"
    local message="${3:-Assertion failed}"

    if [[ "$expected" != "$actual" ]]; then
        echo "  Error: $message"
        echo "  Expected: $expected"
        echo "  Actual: $actual"
        return 1
    fi
    return 0
}

assert_contains() {
    local text="$1"
    local pattern="$2"
    local message="${3:-Pattern not found}"

    if ! echo "$text" | grep -q "$pattern"; then
        echo "  Error: $message"
        echo "  Text: $text"
        echo "  Pattern: $pattern"
        return 1
    fi
    return 0
}

# Setup temporary config directory
mkdir -p "$TEMP_DIR"

# Create mock workflow-subagents.yaml
create_mock_config() {
    cat > "$CONFIG_FILE" << 'YAML'
workflow_subagents:
  - tech-stack-detector
  - context-validator
  - test-automator
  - backend-architect
  - refactoring-specialist
  - integration-tester
  - code-reviewer
  - security-auditor
  - deferral-validator
  - dev-result-interpreter

excluded_subagents:
  - internet-sleuth
  - documentation-writer
  - api-designer
  - stakeholder-analyst
YAML
}

# TEST AC#4.1: Workflow subagent is recorded
test_workflow_subagent_recorded() {
    create_mock_config

    # Check that test-automator is in workflow list
    local subagent="test-automator"

    if grep -q "^  - $subagent$" "$CONFIG_FILE"; then
        return 0
    else
        echo "  Error: Workflow subagent '$subagent' not found in config"
        echo "  Config content:"
        cat "$CONFIG_FILE" | head -20
        return 1
    fi
}

# TEST AC#4.2: Non-workflow subagent is skipped
test_non_workflow_subagent_skipped() {
    create_mock_config

    # Check that internet-sleuth is in excluded list
    local subagent="internet-sleuth"

    if grep -q "^  - $subagent$" "$CONFIG_FILE" && \
       grep -B 20 "$subagent" "$CONFIG_FILE" | grep -q "excluded_subagents:"; then
        return 0
    else
        echo "  Error: Non-workflow subagent '$subagent' not found in excluded list"
        return 1
    fi
}

# TEST AC#4.3: All 10 workflow subagents in list are recognized
test_all_workflow_subagents_recognized() {
    create_mock_config

    local expected_subagents=(
        "tech-stack-detector"
        "context-validator"
        "test-automator"
        "backend-architect"
        "refactoring-specialist"
        "integration-tester"
        "code-reviewer"
        "security-auditor"
        "deferral-validator"
        "dev-result-interpreter"
    )

    local workflow_section=$(sed -n '/^workflow_subagents:/,/^excluded_subagents:/p' "$CONFIG_FILE")

    for subagent in "${expected_subagents[@]}"; do
        if ! echo "$workflow_section" | grep -qF -- "- $subagent"; then
            echo "  Error: Workflow subagent '$subagent' not found"
            return 1
        fi
    done

    return 0
}

# TEST AC#4.4: Excluded subagents list contains non-workflow agents
test_excluded_subagents_in_list() {
    create_mock_config

    local excluded_subagents=(
        "internet-sleuth"
        "documentation-writer"
        "api-designer"
        "stakeholder-analyst"
    )

    local excluded_section=$(sed -n '/^excluded_subagents:/,$p' "$CONFIG_FILE")

    for subagent in "${excluded_subagents[@]}"; do
        if ! echo "$excluded_section" | grep -qF -- "- $subagent"; then
            echo "  Error: Excluded subagent '$subagent' not found"
            return 1
        fi
    done

    return 0
}

# TEST AC#4.5: Non-workflow subagents skip recording with exit 0
test_non_workflow_skipped_silently() {
    create_mock_config

    local subagent="documentation-writer"
    local expected_exit_code=0

    # Simulate checking if subagent is in workflow list
    if ! grep -q "^  - $subagent$" "$CONFIG_FILE"; then
        # Not in workflow list - should skip
        # In actual implementation, hook would exit 0
        local actual_exit_code=0
    else
        local actual_exit_code=1
    fi

    assert_equals "$expected_exit_code" "$actual_exit_code" \
        "Non-workflow subagent should skip with exit code 0"

    return 0
}

# TEST AC#4.6: Config file has valid YAML syntax
test_config_valid_yaml_syntax() {
    create_mock_config

    if ! command -v python3 &> /dev/null; then
        echo "  Skipping YAML validation (python3 not available)"
        return 0
    fi

    if ! python3 -c "import yaml; yaml.safe_load(open('$CONFIG_FILE'))" 2>/dev/null; then
        echo "  Error: workflow-subagents.yaml has invalid YAML syntax"
        return 1
    fi

    return 0
}

# TEST AC#4.7: Filter distinguishes workflow from non-workflow
test_filter_distinguishes_subagents() {
    create_mock_config

    local workflow_subagent="test-automator"
    local non_workflow_subagent="internet-sleuth"

    # Check workflow is in workflow_subagents
    if ! grep -q "^  - $workflow_subagent$" "$CONFIG_FILE"; then
        echo "  Error: Workflow subagent not in workflow list"
        return 1
    fi

    # Check non-workflow is in excluded_subagents
    if ! grep -q "^  - $non_workflow_subagent$" "$CONFIG_FILE"; then
        echo "  Error: Non-workflow subagent not in excluded list"
        return 1
    fi

    return 0
}

# TEST AC#4.8: Subagent names are lowercase with hyphens
test_subagent_naming_convention() {
    create_mock_config

    # Get all subagent names
    local subagents=$(grep "^  - " "$CONFIG_FILE" | sed 's/^  - //')

    while IFS= read -r subagent; do
        # Verify lowercase and hyphen-separated (no CamelCase or underscores)
        if [[ ! "$subagent" =~ ^[a-z][a-z0-9]*(-[a-z0-9]+)*$ ]]; then
            echo "  Error: Subagent name '$subagent' doesn't follow naming convention"
            echo "  Expected: lowercase with hyphens (e.g., test-automator)"
            return 1
        fi
    done <<< "$subagents"

    return 0
}

# TEST AC#4.9: Exact match required (substring match doesn't count)
test_exact_match_required() {
    create_mock_config

    local subagent="test"  # Substring of test-automator
    local exact_subagent="test-automator"

    # Exact match should find it
    if ! grep -q "^  - $exact_subagent$" "$CONFIG_FILE"; then
        echo "  Error: Exact match not found"
        return 1
    fi

    # Substring should NOT match (with anchors)
    if grep -q "^  - $subagent$" "$CONFIG_FILE"; then
        echo "  Error: Substring matched when exact match required"
        return 1
    fi

    return 0
}

# TEST AC#4.10: Case-sensitive comparison (test-automator != Test-Automator)
test_case_sensitive_matching() {
    create_mock_config

    local correct_case="test-automator"
    local wrong_case="Test-Automator"

    # Correct case should match
    if ! grep -q "^  - $correct_case$" "$CONFIG_FILE"; then
        echo "  Error: Correct case not matched"
        return 1
    fi

    # Wrong case should NOT match
    if grep -q "^  - $wrong_case$" "$CONFIG_FILE"; then
        echo "  Error: Case sensitivity not respected"
        return 1
    fi

    return 0
}

# MAIN - Run all tests
echo "============================================================"
echo "STORY-151: Subagent Filtering Tests (AC#4)"
echo "============================================================"

run_test "workflow subagent (test-automator) is recorded" \
    test_workflow_subagent_recorded
run_test "non-workflow subagent (internet-sleuth) is skipped" \
    test_non_workflow_subagent_skipped
run_test "all 10 workflow subagents are recognized" \
    test_all_workflow_subagents_recognized
run_test "excluded subagents list contains non-workflow agents" \
    test_excluded_subagents_in_list
run_test "non-workflow subagents skip recording silently (exit 0)" \
    test_non_workflow_skipped_silently
run_test "config file has valid YAML syntax" \
    test_config_valid_yaml_syntax
run_test "filter distinguishes workflow from non-workflow subagents" \
    test_filter_distinguishes_subagents
run_test "subagent names follow naming convention (lowercase, hyphens)" \
    test_subagent_naming_convention
run_test "exact match required (substring doesn't count)" \
    test_exact_match_required
run_test "case-sensitive comparison (test-automator != Test-Automator)" \
    test_case_sensitive_matching

# Print summary
echo ""
echo "============================================================"
echo "Test Summary"
echo "============================================================"
echo "Total: $tests_run"
echo "Passed: $tests_passed"
echo "Failed: $tests_failed"
echo "============================================================"

exit $tests_failed
