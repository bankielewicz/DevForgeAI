#!/bin/bash
# STORY-313 AC#3: ADR documents decision
# Test: devforgeai/specs/adrs/ADR-XXX-triple-mirror-consolidation.md

set -e

# Test Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
ADR_DIR="$PROJECT_ROOT/devforgeai/specs/adrs"

# Test Results
TESTS_RUN=0
TESTS_PASSED=0
TESTS_FAILED=0

# Test Helper Functions
pass() {
    echo "[PASS] $1"
    TESTS_PASSED=$((TESTS_PASSED + 1))
    TESTS_RUN=$((TESTS_RUN + 1))
}

fail() {
    echo "[FAIL] $1"
    TESTS_FAILED=$((TESTS_FAILED + 1))
    TESTS_RUN=$((TESTS_RUN + 1))
}

# Find ADR file (pattern: ADR-*-triple-mirror*.md)
find_adr_file() {
    ADR_FILE=$(find "$ADR_DIR" -name "ADR-*triple-mirror*.md" 2>/dev/null | head -n 1)
    echo "$ADR_FILE"
}

# ------------------------------------------------------------------------------
# Test: ADR-000 - ADR file exists
# ------------------------------------------------------------------------------
test_adr_exists() {
    ADR_FILE=$(find_adr_file)
    if [ -n "$ADR_FILE" ] && [ -f "$ADR_FILE" ]; then
        pass "ADR-000: ADR file exists: $(basename "$ADR_FILE")"
    else
        fail "ADR-000: ADR file NOT FOUND matching pattern ADR-*triple-mirror*.md"
    fi
}

# ------------------------------------------------------------------------------
# Test: ADR-001 - ADR has Context section
# ------------------------------------------------------------------------------
test_adr_context_section() {
    ADR_FILE=$(find_adr_file)
    if [ -n "$ADR_FILE" ] && [ -f "$ADR_FILE" ]; then
        if grep -qiE "^#+\s*(Context|Background)" "$ADR_FILE"; then
            pass "ADR-001: ADR has Context section"
        else
            fail "ADR-001: ADR missing Context section"
        fi
    else
        fail "ADR-001: ADR not found, cannot check Context section"
    fi
}

# ------------------------------------------------------------------------------
# Test: ADR-001 - ADR has Decision section
# ------------------------------------------------------------------------------
test_adr_decision_section() {
    ADR_FILE=$(find_adr_file)
    if [ -n "$ADR_FILE" ] && [ -f "$ADR_FILE" ]; then
        if grep -qiE "^#+\s*Decision" "$ADR_FILE"; then
            pass "ADR-001: ADR has Decision section"
        else
            fail "ADR-001: ADR missing Decision section"
        fi
    else
        fail "ADR-001: ADR not found, cannot check Decision section"
    fi
}

# ------------------------------------------------------------------------------
# Test: ADR-001 - ADR has Consequences section
# ------------------------------------------------------------------------------
test_adr_consequences_section() {
    ADR_FILE=$(find_adr_file)
    if [ -n "$ADR_FILE" ] && [ -f "$ADR_FILE" ]; then
        if grep -qiE "^#+\s*Consequences" "$ADR_FILE"; then
            pass "ADR-001: ADR has Consequences section"
        else
            fail "ADR-001: ADR missing Consequences section"
        fi
    else
        fail "ADR-001: ADR not found, cannot check Consequences section"
    fi
}

# ------------------------------------------------------------------------------
# Test: ADR-001 - ADR mentions alternatives considered
# ------------------------------------------------------------------------------
test_adr_alternatives() {
    ADR_FILE=$(find_adr_file)
    if [ -n "$ADR_FILE" ] && [ -f "$ADR_FILE" ]; then
        if grep -qiE "(alternatives|options|considered|rejected)" "$ADR_FILE"; then
            pass "ADR-001: ADR discusses alternatives considered"
        else
            fail "ADR-001: ADR does not discuss alternatives"
        fi
    else
        fail "ADR-001: ADR not found, cannot check alternatives"
    fi
}

# ------------------------------------------------------------------------------
# Test: ADR has triple mirror / sync content
# ------------------------------------------------------------------------------
test_adr_content_relevance() {
    ADR_FILE=$(find_adr_file)
    if [ -n "$ADR_FILE" ] && [ -f "$ADR_FILE" ]; then
        if grep -qiE "(triple|mirror|sync|source.of.truth|src/claude)" "$ADR_FILE"; then
            pass "ADR-001: ADR content is relevant to triple mirror pattern"
        else
            fail "ADR-001: ADR content does not mention triple mirror pattern"
        fi
    else
        fail "ADR-001: ADR not found, cannot check content"
    fi
}

# ------------------------------------------------------------------------------
# Run All Tests
# ------------------------------------------------------------------------------
echo "=========================================="
echo "STORY-313 AC#3: ADR Tests"
echo "=========================================="
echo ""

test_adr_exists
test_adr_context_section
test_adr_decision_section
test_adr_consequences_section
test_adr_alternatives
test_adr_content_relevance

echo ""
echo "=========================================="
echo "Test Summary: $TESTS_PASSED/$TESTS_RUN passed"
echo "=========================================="

if [ $TESTS_FAILED -gt 0 ]; then
    exit 1
fi
exit 0
