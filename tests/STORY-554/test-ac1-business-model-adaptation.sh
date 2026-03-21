#!/bin/bash

##############################################################################
# Test Suite: STORY-554 AC#1 - Business Model Adaptation
#
# AC#1: Business Model Adaptation
# Given: a user has completed business planning and their business model type
#        is known (SaaS, marketplace, service, or product)
# When: the MVP launch checklist skill is invoked
# Then: the checklist adapts its domain sections and specific line items to
#       match the detected business model type, omitting irrelevant items
#       and including model-specific items
#
# Target file: src/claude/skills/operating-business/references/mvp-launch-checklist.md
#
# TDD Phase: RED - All tests expected to FAIL (target file does not exist)
# Story: STORY-554
# Generated: 2026-03-21
##############################################################################

set -euo pipefail

TEST_NAME="AC#1: Business Model Adaptation"
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

##############################################################################
# TEST 1: Reference file exists
##############################################################################

test_reference_file_exists() {
    # Arrange: Define expected path
    local expected_path="$PROJECT_ROOT/$TARGET_FILE"

    # Act & Assert: File must exist
    if [ -f "$expected_path" ]; then
        echo "  Reference file found: $TARGET_FILE"
        return 0
    else
        echo "  ERROR: Reference file not found at $TARGET_FILE"
        return 1
    fi
}

##############################################################################
# TEST 2: SaaS business model section exists
##############################################################################

test_saas_model_section_exists() {
    # Arrange
    local file="$PROJECT_ROOT/$TARGET_FILE"

    # Act & Assert: SaaS model section/marker must exist
    if [ ! -f "$file" ]; then
        echo "  ERROR: File does not exist: $TARGET_FILE"
        return 1
    fi

    if grep -qi "saas" "$file"; then
        echo "  SaaS business model content found"
        return 0
    else
        echo "  ERROR: No SaaS business model content found"
        return 1
    fi
}

##############################################################################
# TEST 3: Marketplace business model section exists
##############################################################################

test_marketplace_model_section_exists() {
    # Arrange
    local file="$PROJECT_ROOT/$TARGET_FILE"

    # Act & Assert: Marketplace model section/marker must exist
    if [ ! -f "$file" ]; then
        echo "  ERROR: File does not exist: $TARGET_FILE"
        return 1
    fi

    if grep -qi "marketplace" "$file"; then
        echo "  Marketplace business model content found"
        return 0
    else
        echo "  ERROR: No Marketplace business model content found"
        return 1
    fi
}

##############################################################################
# TEST 4: Service business model section exists
##############################################################################

test_service_model_section_exists() {
    # Arrange
    local file="$PROJECT_ROOT/$TARGET_FILE"

    # Act & Assert: Service model section/marker must exist
    if [ ! -f "$file" ]; then
        echo "  ERROR: File does not exist: $TARGET_FILE"
        return 1
    fi

    if grep -qi "service" "$file"; then
        echo "  Service business model content found"
        return 0
    else
        echo "  ERROR: No Service business model content found"
        return 1
    fi
}

##############################################################################
# TEST 5: Product business model section exists
##############################################################################

test_product_model_section_exists() {
    # Arrange
    local file="$PROJECT_ROOT/$TARGET_FILE"

    # Act & Assert: Product model section/marker must exist
    if [ ! -f "$file" ]; then
        echo "  ERROR: File does not exist: $TARGET_FILE"
        return 1
    fi

    if grep -qi "product" "$file"; then
        echo "  Product business model content found"
        return 0
    else
        echo "  ERROR: No Product business model content found"
        return 1
    fi
}

##############################################################################
# TEST 6: All four business model types referenced
##############################################################################

test_all_four_model_types_present() {
    # Arrange
    local file="$PROJECT_ROOT/$TARGET_FILE"
    local missing=0

    # Act & Assert: All 4 models must appear
    if [ ! -f "$file" ]; then
        echo "  ERROR: File does not exist: $TARGET_FILE"
        return 1
    fi

    for model in "saas" "marketplace" "service" "product"; do
        if ! grep -qi "$model" "$file"; then
            echo "  ERROR: Business model type missing: $model"
            missing=$((missing + 1))
        fi
    done

    if [ "$missing" -eq 0 ]; then
        echo "  All 4 business model types present"
        return 0
    else
        echo "  ERROR: $missing business model types missing"
        return 1
    fi
}

##############################################################################
# TEST 7: SaaS model includes subscription billing
##############################################################################

test_saas_includes_subscription_billing() {
    # Arrange
    local file="$PROJECT_ROOT/$TARGET_FILE"

    # Act & Assert: SaaS-specific item must exist
    if [ ! -f "$file" ]; then
        echo "  ERROR: File does not exist: $TARGET_FILE"
        return 1
    fi

    if grep -qi "subscription.*billing\|billing.*subscription\|recurring.*payment\|subscription.*payment" "$file"; then
        echo "  SaaS subscription billing item found"
        return 0
    else
        echo "  ERROR: SaaS model missing subscription billing item"
        return 1
    fi
}

##############################################################################
# TEST 8: Marketplace model includes seller/buyer onboarding
##############################################################################

test_marketplace_includes_seller_buyer_onboarding() {
    # Arrange
    local file="$PROJECT_ROOT/$TARGET_FILE"

    # Act & Assert: Marketplace-specific item must exist
    if [ ! -f "$file" ]; then
        echo "  ERROR: File does not exist: $TARGET_FILE"
        return 1
    fi

    if grep -qi "seller.*onboarding\|buyer.*onboarding\|seller.*registration\|vendor.*onboarding" "$file"; then
        echo "  Marketplace seller/buyer onboarding item found"
        return 0
    else
        echo "  ERROR: Marketplace model missing seller/buyer onboarding item"
        return 1
    fi
}

##############################################################################
# TEST 9: Model-specific items are tagged or grouped by model type
##############################################################################

test_model_specific_items_tagged() {
    # Arrange
    local file="$PROJECT_ROOT/$TARGET_FILE"

    # Act & Assert: Items must be identifiable by model type (tagged, grouped, or conditional)
    if [ ! -f "$file" ]; then
        echo "  ERROR: File does not exist: $TARGET_FILE"
        return 1
    fi

    # Look for model type indicators (section headers, tags, or conditional markers)
    local model_markers
    model_markers=$(grep -ciE "(saas|marketplace|service|product).*(specific|only|model|applicable)" "$file" 2>/dev/null || echo "0")

    if [ "$model_markers" -ge 2 ]; then
        echo "  Model-specific item markers found: $model_markers"
        return 0
    else
        echo "  ERROR: Insufficient model-specific item markers (found $model_markers, expected >= 2)"
        return 1
    fi
}

##############################################################################
# TEST 10: SaaS model omits inventory management
##############################################################################

test_saas_omits_inventory_management() {
    # Arrange
    local file="$PROJECT_ROOT/$TARGET_FILE"

    # Act & Assert: SaaS section should not include inventory management
    # This test validates that model adaptation OMITS irrelevant items
    if [ ! -f "$file" ]; then
        echo "  ERROR: File does not exist: $TARGET_FILE"
        return 1
    fi

    # If there's a SaaS-specific section, check it doesn't contain inventory
    # We look for inventory being explicitly marked as product/marketplace only
    # or absent from SaaS sections
    if grep -qi "inventory.*management" "$file"; then
        # Inventory management exists in the file - verify it's NOT under SaaS
        # It should be under product or marketplace only
        if grep -qiP "(?:product|marketplace|physical).*inventory|inventory.*(?:product|marketplace|physical)" "$file"; then
            echo "  Inventory management correctly scoped to product/marketplace models"
            return 0
        else
            echo "  WARNING: Inventory management present but not clearly scoped away from SaaS"
            return 1
        fi
    else
        # No inventory management at all is also acceptable for a SaaS-focused check
        echo "  No inventory management items present (acceptable for SaaS adaptation)"
        return 0
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
run_test "SaaS business model section exists" test_saas_model_section_exists
run_test "Marketplace business model section exists" test_marketplace_model_section_exists
run_test "Service business model section exists" test_service_model_section_exists
run_test "Product business model section exists" test_product_model_section_exists
run_test "All four business model types present" test_all_four_model_types_present
run_test "SaaS model includes subscription billing" test_saas_includes_subscription_billing
run_test "Marketplace includes seller/buyer onboarding" test_marketplace_includes_seller_buyer_onboarding
run_test "Model-specific items are tagged by model type" test_model_specific_items_tagged
run_test "SaaS model omits inventory management" test_saas_omits_inventory_management

##############################################################################
# Summary
##############################################################################

echo ""
echo "============================================================"
echo "Results: $TESTS_PASSED passed, $TESTS_FAILED failed out of $TESTS_RUN tests"
echo "============================================================"

[ "$TESTS_FAILED" -eq 0 ] && exit 0 || exit 1
