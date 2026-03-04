#!/bin/bash
# Test: AC#2 - Model-Specific Reference Loading
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

echo "=== AC#2: Model-Specific Reference Loading ==="
echo ""

# --- Act & Assert ---

# Test 1: SaaS guidance section with frameworks/metrics
grep -qi "saas" "$TARGET_FILE" 2>/dev/null && grep -iA 20 "saas" "$TARGET_FILE" 2>/dev/null | grep -qi "framework\|metric"
run_test "test_should_contain_saas_guidance_with_frameworks_when_model_guidance_defined" $?

# Test 2: Marketplace guidance section with frameworks/metrics
grep -qi "marketplace" "$TARGET_FILE" 2>/dev/null && grep -iA 20 "marketplace" "$TARGET_FILE" 2>/dev/null | grep -qi "framework\|metric"
run_test "test_should_contain_marketplace_guidance_with_frameworks_when_model_guidance_defined" $?

# Test 3: Service guidance section with frameworks/metrics
grep -qi "service" "$TARGET_FILE" 2>/dev/null && grep -iA 20 "service" "$TARGET_FILE" 2>/dev/null | grep -qi "framework\|metric"
run_test "test_should_contain_service_guidance_with_frameworks_when_model_guidance_defined" $?

# Test 4: Product guidance section with frameworks/metrics
grep -qi "product" "$TARGET_FILE" 2>/dev/null && grep -iA 20 "product" "$TARGET_FILE" 2>/dev/null | grep -qi "framework\|metric"
run_test "test_should_contain_product_guidance_with_frameworks_when_model_guidance_defined" $?

# Test 5: Per-model guidance sections exist (all 4)
GUIDANCE_COUNT=0
for model in "saas" "marketplace" "service" "product"; do
    grep -qi "${model}.*guidance\|guidance.*${model}\|## .*${model}" "$TARGET_FILE" 2>/dev/null && ((GUIDANCE_COUNT++))
done
[ "$GUIDANCE_COUNT" -ge 4 ]
run_test "test_should_have_guidance_for_all_4_models_when_reference_file_complete" $?

# Test 6: Metrics mentioned for at least one model
grep -qi "metric" "$TARGET_FILE" 2>/dev/null
run_test "test_should_contain_metrics_when_model_guidance_defined" $?

# === Summary ===
echo ""
echo "Results: $PASSED passed, $FAILED failed out of $((PASSED + FAILED)) tests"
[ $FAILED -eq 0 ] && exit 0 || exit 1
