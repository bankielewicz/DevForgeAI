#!/bin/bash
# Test: AC#1 - Business Model Detection from Lean Canvas
# Story: STORY-533
# Generated: 2026-03-04

# === Test Configuration ===
PASSED=0
FAILED=0
TARGET_FILE="src/claude/skills/planning-business/references/business-model-patterns.md"

run_test() {
    local name="$1"
    local result="$2"
    if [ "$result" -eq 0 ]; then
        echo "  PASS: $name"
        ((PASSED++))
    else
        echo "  FAIL: $name"
        ((FAILED++))
    fi
}

echo "=== AC#1: Business Model Detection ==="
echo ""

# --- Arrange ---
# Target file must exist at the src/ tree path
# Tests validate business-model-patterns.md content

# --- Act & Assert ---

# Test 1: File exists
test -f "$TARGET_FILE"
run_test "test_should_exist_when_business_model_patterns_file_created" $?

# Test 2: SaaS model type defined
grep -qi "## .*saas" "$TARGET_FILE" 2>/dev/null
run_test "test_should_contain_saas_definition_when_model_types_defined" $?

# Test 3: Marketplace model type defined
grep -qi "## .*marketplace" "$TARGET_FILE" 2>/dev/null
run_test "test_should_contain_marketplace_definition_when_model_types_defined" $?

# Test 4: Service model type defined
grep -qi "## .*service" "$TARGET_FILE" 2>/dev/null
run_test "test_should_contain_service_definition_when_model_types_defined" $?

# Test 5: Product model type defined
grep -qi "## .*product" "$TARGET_FILE" 2>/dev/null
run_test "test_should_contain_product_definition_when_model_types_defined" $?

# Test 6: Detection signals linked to Canvas fields
grep -qi "detection signal" "$TARGET_FILE" 2>/dev/null
run_test "test_should_contain_detection_signals_when_canvas_field_mapping_defined" $?

# Test 7: Canvas field references present
grep -qi "canvas\|lean canvas" "$TARGET_FILE" 2>/dev/null
run_test "test_should_reference_canvas_fields_when_detection_signals_defined" $?

# Test 8: High confidence indicator explained
grep -qi "high" "$TARGET_FILE" 2>/dev/null && grep -qi "confidence" "$TARGET_FILE" 2>/dev/null
run_test "test_should_explain_high_confidence_when_confidence_indicators_defined" $?

# Test 9: Medium confidence indicator explained
grep -qi "medium" "$TARGET_FILE" 2>/dev/null && grep -qi "confidence" "$TARGET_FILE" 2>/dev/null
run_test "test_should_explain_medium_confidence_when_confidence_indicators_defined" $?

# Test 10: Low confidence indicator explained
grep -qi "low" "$TARGET_FILE" 2>/dev/null && grep -qi "confidence" "$TARGET_FILE" 2>/dev/null
run_test "test_should_explain_low_confidence_when_confidence_indicators_defined" $?

# === Summary ===
echo ""
echo "Results: $PASSED passed, $FAILED failed out of $((PASSED + FAILED)) tests"
[ $FAILED -eq 0 ] && exit 0 || exit 1
