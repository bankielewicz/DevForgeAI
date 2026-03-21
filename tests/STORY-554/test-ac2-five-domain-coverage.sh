#!/bin/bash

##############################################################################
# Test Suite: STORY-554 AC#2 - Five Domain Coverage
#
# AC#2: Five Domain Coverage
# Given: a user initiates the MVP launch checklist workflow
# When: the checklist is generated
# Then: it covers all five domains (legal, financial, marketing, technical,
#       operations) with a minimum of 3 actionable items per domain
#
# Target file: src/claude/skills/operating-business/references/mvp-launch-checklist.md
#
# TDD Phase: RED - All tests expected to FAIL (target file does not exist)
# Story: STORY-554
# Generated: 2026-03-21
##############################################################################

set -euo pipefail

TEST_NAME="AC#2: Five Domain Coverage"
TEST_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$TEST_DIR/../../" && pwd)"
TARGET_FILE="src/claude/skills/operating-business/references/mvp-launch-checklist.md"

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

# Helper functions
run_test() {
    local test_name=$1
    local test_func=$2

    TESTS_RUN=$((TESTS_RUN + 1))
    echo -e "\n${BLUE}[Test $TESTS_RUN]${NC} $test_name"

    if $test_func; then
        TESTS_PASSED=$((TESTS_PASSED + 1))
        echo -e "${GREEN}  PASS${NC}"
    else
        TESTS_FAILED=$((TESTS_FAILED + 1))
        echo -e "${RED}  FAIL${NC}"
    fi
}

# Helper: Count checklist items under a domain section header
# Counts lines matching "- [ ]" pattern between one domain header and the next
count_domain_items() {
    local file="$1"
    local domain_pattern="$2"
    local count

    # Find the domain section and count checkbox items until next section header
    count=$(awk "
        BEGIN { in_section=0; count=0 }
        /^##.*${domain_pattern}/i { in_section=1; next }
        in_section && /^##/ { in_section=0 }
        in_section && /^- \[/ { count++ }
        END { print count }
    " "$file")

    echo "$count"
}

##############################################################################
# TEST 1: Reference file exists
##############################################################################

test_reference_file_exists() {
    local expected_path="$PROJECT_ROOT/$TARGET_FILE"

    if [ -f "$expected_path" ]; then
        echo "  Reference file found: $TARGET_FILE"
        return 0
    else
        echo "  ERROR: Reference file not found at $TARGET_FILE"
        return 1
    fi
}

##############################################################################
# TEST 2: Legal domain section exists
##############################################################################

test_legal_domain_exists() {
    local file="$PROJECT_ROOT/$TARGET_FILE"

    if [ ! -f "$file" ]; then
        echo "  ERROR: File does not exist: $TARGET_FILE"
        return 1
    fi

    if grep -qi "## .*legal" "$file"; then
        echo "  Legal domain section found"
        return 0
    else
        echo "  ERROR: No legal domain section found"
        return 1
    fi
}

##############################################################################
# TEST 3: Financial domain section exists
##############################################################################

test_financial_domain_exists() {
    local file="$PROJECT_ROOT/$TARGET_FILE"

    if [ ! -f "$file" ]; then
        echo "  ERROR: File does not exist: $TARGET_FILE"
        return 1
    fi

    if grep -qi "## .*financial\|## .*finance" "$file"; then
        echo "  Financial domain section found"
        return 0
    else
        echo "  ERROR: No financial domain section found"
        return 1
    fi
}

##############################################################################
# TEST 4: Marketing domain section exists
##############################################################################

test_marketing_domain_exists() {
    local file="$PROJECT_ROOT/$TARGET_FILE"

    if [ ! -f "$file" ]; then
        echo "  ERROR: File does not exist: $TARGET_FILE"
        return 1
    fi

    if grep -qi "## .*marketing" "$file"; then
        echo "  Marketing domain section found"
        return 0
    else
        echo "  ERROR: No marketing domain section found"
        return 1
    fi
}

##############################################################################
# TEST 5: Technical domain section exists
##############################################################################

test_technical_domain_exists() {
    local file="$PROJECT_ROOT/$TARGET_FILE"

    if [ ! -f "$file" ]; then
        echo "  ERROR: File does not exist: $TARGET_FILE"
        return 1
    fi

    if grep -qi "## .*technical" "$file"; then
        echo "  Technical domain section found"
        return 0
    else
        echo "  ERROR: No technical domain section found"
        return 1
    fi
}

##############################################################################
# TEST 6: Operations domain section exists
##############################################################################

test_operations_domain_exists() {
    local file="$PROJECT_ROOT/$TARGET_FILE"

    if [ ! -f "$file" ]; then
        echo "  ERROR: File does not exist: $TARGET_FILE"
        return 1
    fi

    if grep -qi "## .*operations\|## .*ops" "$file"; then
        echo "  Operations domain section found"
        return 0
    else
        echo "  ERROR: No operations domain section found"
        return 1
    fi
}

##############################################################################
# TEST 7: Legal domain has >= 3 actionable items
##############################################################################

test_legal_domain_minimum_items() {
    local file="$PROJECT_ROOT/$TARGET_FILE"

    if [ ! -f "$file" ]; then
        echo "  ERROR: File does not exist: $TARGET_FILE"
        return 1
    fi

    local count
    count=$(count_domain_items "$file" "legal")

    if [ "$count" -ge 3 ]; then
        echo "  Legal domain has $count items (minimum 3)"
        return 0
    else
        echo "  ERROR: Legal domain has only $count items (minimum 3 required)"
        return 1
    fi
}

##############################################################################
# TEST 8: Financial domain has >= 3 actionable items
##############################################################################

test_financial_domain_minimum_items() {
    local file="$PROJECT_ROOT/$TARGET_FILE"

    if [ ! -f "$file" ]; then
        echo "  ERROR: File does not exist: $TARGET_FILE"
        return 1
    fi

    local count
    count=$(count_domain_items "$file" "financ")

    if [ "$count" -ge 3 ]; then
        echo "  Financial domain has $count items (minimum 3)"
        return 0
    else
        echo "  ERROR: Financial domain has only $count items (minimum 3 required)"
        return 1
    fi
}

##############################################################################
# TEST 9: Marketing domain has >= 3 actionable items
##############################################################################

test_marketing_domain_minimum_items() {
    local file="$PROJECT_ROOT/$TARGET_FILE"

    if [ ! -f "$file" ]; then
        echo "  ERROR: File does not exist: $TARGET_FILE"
        return 1
    fi

    local count
    count=$(count_domain_items "$file" "marketing")

    if [ "$count" -ge 3 ]; then
        echo "  Marketing domain has $count items (minimum 3)"
        return 0
    else
        echo "  ERROR: Marketing domain has only $count items (minimum 3 required)"
        return 1
    fi
}

##############################################################################
# TEST 10: Technical domain has >= 3 actionable items
##############################################################################

test_technical_domain_minimum_items() {
    local file="$PROJECT_ROOT/$TARGET_FILE"

    if [ ! -f "$file" ]; then
        echo "  ERROR: File does not exist: $TARGET_FILE"
        return 1
    fi

    local count
    count=$(count_domain_items "$file" "technical")

    if [ "$count" -ge 3 ]; then
        echo "  Technical domain has $count items (minimum 3)"
        return 0
    else
        echo "  ERROR: Technical domain has only $count items (minimum 3 required)"
        return 1
    fi
}

##############################################################################
# TEST 11: Operations domain has >= 3 actionable items
##############################################################################

test_operations_domain_minimum_items() {
    local file="$PROJECT_ROOT/$TARGET_FILE"

    if [ ! -f "$file" ]; then
        echo "  ERROR: File does not exist: $TARGET_FILE"
        return 1
    fi

    local count
    count=$(count_domain_items "$file" "operat")

    if [ "$count" -ge 3 ]; then
        echo "  Operations domain has $count items (minimum 3)"
        return 0
    else
        echo "  ERROR: Operations domain has only $count items (minimum 3 required)"
        return 1
    fi
}

##############################################################################
# TEST 12: All five domains present in a single file
##############################################################################

test_all_five_domains_present() {
    local file="$PROJECT_ROOT/$TARGET_FILE"
    local missing=0

    if [ ! -f "$file" ]; then
        echo "  ERROR: File does not exist: $TARGET_FILE"
        return 1
    fi

    for domain in "legal" "financ" "marketing" "technical" "operat"; do
        if ! grep -qi "## .*$domain" "$file"; then
            echo "  ERROR: Domain section missing: $domain"
            missing=$((missing + 1))
        fi
    done

    if [ "$missing" -eq 0 ]; then
        echo "  All 5 domain sections present"
        return 0
    else
        echo "  ERROR: $missing domain sections missing"
        return 1
    fi
}

##############################################################################
# TEST 13: Each item includes a one-line description
##############################################################################

test_items_include_descriptions() {
    local file="$PROJECT_ROOT/$TARGET_FILE"

    if [ ! -f "$file" ]; then
        echo "  ERROR: File does not exist: $TARGET_FILE"
        return 1
    fi

    # Count checkbox items
    local total_items
    total_items=$(grep -c "^- \[" "$file" 2>/dev/null || echo "0")

    # Count checkbox items that have descriptive text (more than just a short label)
    # Items should have format: - [ ] **Item Name** - Description of why it matters
    local items_with_desc
    items_with_desc=$(grep -cE "^- \[.\] .+( - | -- | \| ).+" "$file" 2>/dev/null || echo "0")

    if [ "$total_items" -eq 0 ]; then
        echo "  ERROR: No checklist items found"
        return 1
    fi

    if [ "$items_with_desc" -ge "$total_items" ]; then
        echo "  All $total_items items include descriptions"
        return 0
    else
        echo "  ERROR: Only $items_with_desc of $total_items items include descriptions"
        return 1
    fi
}

##############################################################################
# TEST 14: Reference file under 1000 lines (NFR-002)
##############################################################################

test_reference_file_under_1000_lines() {
    local file="$PROJECT_ROOT/$TARGET_FILE"

    if [ ! -f "$file" ]; then
        echo "  ERROR: File does not exist: $TARGET_FILE"
        return 1
    fi

    local line_count
    line_count=$(wc -l < "$file")

    if [ "$line_count" -lt 1000 ]; then
        echo "  Reference file is $line_count lines (limit: 1000)"
        return 0
    else
        echo "  ERROR: Reference file is $line_count lines (exceeds 1000 line limit)"
        return 1
    fi
}

##############################################################################
# Run all tests
##############################################################################

echo "============================================================"
echo "STORY-554 | $TEST_NAME"
echo "Target: $TARGET_FILE"
echo "============================================================"

run_test "Reference file exists" test_reference_file_exists
run_test "Legal domain section exists" test_legal_domain_exists
run_test "Financial domain section exists" test_financial_domain_exists
run_test "Marketing domain section exists" test_marketing_domain_exists
run_test "Technical domain section exists" test_technical_domain_exists
run_test "Operations domain section exists" test_operations_domain_exists
run_test "Legal domain has >= 3 items" test_legal_domain_minimum_items
run_test "Financial domain has >= 3 items" test_financial_domain_minimum_items
run_test "Marketing domain has >= 3 items" test_marketing_domain_minimum_items
run_test "Technical domain has >= 3 items" test_technical_domain_minimum_items
run_test "Operations domain has >= 3 items" test_operations_domain_minimum_items
run_test "All five domains present" test_all_five_domains_present
run_test "Each item includes a one-line description" test_items_include_descriptions
run_test "Reference file under 1000 lines" test_reference_file_under_1000_lines

##############################################################################
# Summary
##############################################################################

echo ""
echo "============================================================"
echo "Results: $TESTS_PASSED passed, $TESTS_FAILED failed out of $TESTS_RUN tests"
echo "============================================================"

[ "$TESTS_FAILED" -eq 0 ] && exit 0 || exit 1
