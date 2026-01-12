#!/bin/bash
# STORY-202: Test Phase Completion Checklists for devforgeai-qa SKILL.md
# TDD RED Phase - All tests should FAIL initially

# Do not use set -e - allow all tests to run even when checks fail
TARGET_FILE="src/claude/skills/devforgeai-qa/SKILL.md"
TESTS_PASSED=0
TESTS_FAILED=0

echo "=== STORY-202 Test Suite: Phase Completion Checklists ==="
echo "Target: $TARGET_FILE"
echo ""

# AC-1: Completion checklist exists before Phase Marker Write (Phases 1-4)
echo "--- AC-1: Completion Checklist Presence ---"

# Test 1.1: Phase 1 Completion Checklist before Phase 1 Marker Write
if grep -q "### Phase 1 Completion Checklist" "$TARGET_FILE" && \
   grep -n "### Phase 1 Completion Checklist" "$TARGET_FILE" | head -1 | cut -d: -f1 | \
   xargs -I{} sh -c "grep -n '### Phase 1 Marker Write' '$TARGET_FILE' | head -1 | cut -d: -f1 | xargs -I@ test {} -lt @"; then
    echo "  [PASS] Phase 1 Completion Checklist exists before Phase 1 Marker Write"
    ((TESTS_PASSED++))
else
    echo "  [FAIL] Phase 1 Completion Checklist missing or after Phase 1 Marker Write"
    ((TESTS_FAILED++))
fi

# Test 1.2: Phase 2 Completion Checklist before Phase 2 Marker Write
if grep -q "### Phase 2 Completion Checklist" "$TARGET_FILE" && \
   grep -n "### Phase 2 Completion Checklist" "$TARGET_FILE" | head -1 | cut -d: -f1 | \
   xargs -I{} sh -c "grep -n '### Phase 2 Marker Write' '$TARGET_FILE' | head -1 | cut -d: -f1 | xargs -I@ test {} -lt @"; then
    echo "  [PASS] Phase 2 Completion Checklist exists before Phase 2 Marker Write"
    ((TESTS_PASSED++))
else
    echo "  [FAIL] Phase 2 Completion Checklist missing or after Phase 2 Marker Write"
    ((TESTS_FAILED++))
fi

# Test 1.3: Phase 3 Completion Checklist before Phase 3 Marker Write
if grep -q "### Phase 3 Completion Checklist" "$TARGET_FILE" && \
   grep -n "### Phase 3 Completion Checklist" "$TARGET_FILE" | head -1 | cut -d: -f1 | \
   xargs -I{} sh -c "grep -n '### Phase 3 Marker Write' '$TARGET_FILE' | head -1 | cut -d: -f1 | xargs -I@ test {} -lt @"; then
    echo "  [PASS] Phase 3 Completion Checklist exists before Phase 3 Marker Write"
    ((TESTS_PASSED++))
else
    echo "  [FAIL] Phase 3 Completion Checklist missing or after Phase 3 Marker Write"
    ((TESTS_FAILED++))
fi

# Test 1.4: Phase 4 Completion Checklist before Phase 4 Marker Write
if grep -q "### Phase 4 Completion Checklist" "$TARGET_FILE" && \
   grep -n "### Phase 4 Completion Checklist" "$TARGET_FILE" | head -1 | cut -d: -f1 | \
   xargs -I{} sh -c "grep -n '### Phase 4 Marker Write' '$TARGET_FILE' | head -1 | cut -d: -f1 | xargs -I@ test {} -lt @"; then
    echo "  [PASS] Phase 4 Completion Checklist exists before Phase 4 Marker Write"
    ((TESTS_PASSED++))
else
    echo "  [FAIL] Phase 4 Completion Checklist missing or after Phase 4 Marker Write"
    ((TESTS_FAILED++))
fi

echo ""

# AC-2: Checklist uses checkbox format
echo "--- AC-2: Checkbox Format ---"

# Test 2.1: Phase 1 checklist has checkbox items
if grep -A 20 "### Phase 1 Completion Checklist" "$TARGET_FILE" | grep -q "^\- \[ \]"; then
    echo "  [PASS] Phase 1 Completion Checklist uses checkbox format"
    ((TESTS_PASSED++))
else
    echo "  [FAIL] Phase 1 Completion Checklist missing checkbox format (- [ ])"
    ((TESTS_FAILED++))
fi

# Test 2.2: Phase 2 checklist has checkbox items
if grep -A 20 "### Phase 2 Completion Checklist" "$TARGET_FILE" | grep -q "^\- \[ \]"; then
    echo "  [PASS] Phase 2 Completion Checklist uses checkbox format"
    ((TESTS_PASSED++))
else
    echo "  [FAIL] Phase 2 Completion Checklist missing checkbox format (- [ ])"
    ((TESTS_FAILED++))
fi

# Test 2.3: Phase 3 checklist has checkbox items
if grep -A 20 "### Phase 3 Completion Checklist" "$TARGET_FILE" | grep -q "^\- \[ \]"; then
    echo "  [PASS] Phase 3 Completion Checklist uses checkbox format"
    ((TESTS_PASSED++))
else
    echo "  [FAIL] Phase 3 Completion Checklist missing checkbox format (- [ ])"
    ((TESTS_FAILED++))
fi

# Test 2.4: Phase 4 checklist has checkbox items
if grep -A 20 "### Phase 4 Completion Checklist" "$TARGET_FILE" | grep -q "^\- \[ \]"; then
    echo "  [PASS] Phase 4 Completion Checklist uses checkbox format"
    ((TESTS_PASSED++))
else
    echo "  [FAIL] Phase 4 Completion Checklist missing checkbox format (- [ ])"
    ((TESTS_FAILED++))
fi

echo ""

# AC-3: Checklist includes HALT instruction
echo "--- AC-3: HALT Instruction ---"

# Test 3.1: Phase 1 checklist has HALT instruction
if grep -A 25 "### Phase 1 Completion Checklist" "$TARGET_FILE" | grep -qi "HALT"; then
    echo "  [PASS] Phase 1 Completion Checklist includes HALT instruction"
    ((TESTS_PASSED++))
else
    echo "  [FAIL] Phase 1 Completion Checklist missing HALT instruction"
    ((TESTS_FAILED++))
fi

# Test 3.2: Phase 2 checklist has HALT instruction
if grep -A 25 "### Phase 2 Completion Checklist" "$TARGET_FILE" | grep -qi "HALT"; then
    echo "  [PASS] Phase 2 Completion Checklist includes HALT instruction"
    ((TESTS_PASSED++))
else
    echo "  [FAIL] Phase 2 Completion Checklist missing HALT instruction"
    ((TESTS_FAILED++))
fi

# Test 3.3: Phase 3 checklist has HALT instruction
if grep -A 25 "### Phase 3 Completion Checklist" "$TARGET_FILE" | grep -qi "HALT"; then
    echo "  [PASS] Phase 3 Completion Checklist includes HALT instruction"
    ((TESTS_PASSED++))
else
    echo "  [FAIL] Phase 3 Completion Checklist missing HALT instruction"
    ((TESTS_FAILED++))
fi

# Test 3.4: Phase 4 checklist has HALT instruction
if grep -A 25 "### Phase 4 Completion Checklist" "$TARGET_FILE" | grep -qi "HALT"; then
    echo "  [PASS] Phase 4 Completion Checklist includes HALT instruction"
    ((TESTS_PASSED++))
else
    echo "  [FAIL] Phase 4 Completion Checklist missing HALT instruction"
    ((TESTS_FAILED++))
fi

echo ""

# AC-4: Phase-specific checklist items
echo "--- AC-4: Phase-Specific Items ---"

# Test 4.1: Phase 1 checklist has traceability item
if grep -A 20 "### Phase 1 Completion Checklist" "$TARGET_FILE" | grep -qi "traceability"; then
    echo "  [PASS] Phase 1 checklist has traceability-specific item"
    ((TESTS_PASSED++))
else
    echo "  [FAIL] Phase 1 checklist missing traceability-specific item"
    ((TESTS_FAILED++))
fi

# Test 4.2: Phase 2 checklist has anti-pattern item
if grep -A 20 "### Phase 2 Completion Checklist" "$TARGET_FILE" | grep -qi "anti-pattern"; then
    echo "  [PASS] Phase 2 checklist has anti-pattern-specific item"
    ((TESTS_PASSED++))
else
    echo "  [FAIL] Phase 2 checklist missing anti-pattern-specific item"
    ((TESTS_FAILED++))
fi

# Test 4.3: Phase 3 checklist has report/result item
if grep -A 20 "### Phase 3 Completion Checklist" "$TARGET_FILE" | grep -qiE "(report|result)"; then
    echo "  [PASS] Phase 3 checklist has report/result-specific item"
    ((TESTS_PASSED++))
else
    echo "  [FAIL] Phase 3 checklist missing report/result-specific item"
    ((TESTS_FAILED++))
fi

# Test 4.4: Phase 4 checklist has lock/cleanup item
if grep -A 20 "### Phase 4 Completion Checklist" "$TARGET_FILE" | grep -qiE "(lock|cleanup)"; then
    echo "  [PASS] Phase 4 checklist has lock/cleanup-specific item"
    ((TESTS_PASSED++))
else
    echo "  [FAIL] Phase 4 checklist missing lock/cleanup-specific item"
    ((TESTS_FAILED++))
fi

echo ""

# AC-5: Display confirmation after checklist
echo "--- AC-5: Display Confirmation Pattern ---"

# Test 5.1-5.4: Confirmation display pattern exists for each phase
for phase in 1 2 3 4; do
    if grep -A 30 "### Phase $phase Completion Checklist" "$TARGET_FILE" | grep -qE "Phase $phase Complete"; then
        echo "  [PASS] Phase $phase has confirmation display pattern"
        ((TESTS_PASSED++))
    else
        echo "  [FAIL] Phase $phase missing confirmation display pattern"
        ((TESTS_FAILED++))
    fi
done

echo ""
echo "=== SUMMARY ==="
echo "Tests Passed: $TESTS_PASSED"
echo "Tests Failed: $TESTS_FAILED"
echo "Total Tests: $((TESTS_PASSED + TESTS_FAILED))"

if [ $TESTS_FAILED -gt 0 ]; then
    echo ""
    echo "STATUS: RED (TDD Red Phase - Tests failing as expected)"
    exit 1
else
    echo ""
    echo "STATUS: GREEN"
    exit 0
fi
