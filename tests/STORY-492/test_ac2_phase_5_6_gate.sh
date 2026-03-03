#!/bin/bash
# Test: AC#2 - Phase 5-6 Checkpoint verifies all 28 required story file sections
# Story: STORY-492
# Generated: 2026-02-23

# === Test Configuration ===
PASSED=0
FAILED=0
TARGET_FILE="/mnt/c/Projects/DevForgeAI2/src/claude/skills/devforgeai-story-creation/SKILL.md"

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

echo "=== AC#2: Phase 5-6 Gate Tests ==="
echo ""

# --- Test 1: Phase 5-6 Gate header exists ---
grep -q "^## Phase 5 - Phase 6 Gate" "$TARGET_FILE"
run_test "Phase 5-6 Gate header exists with ## level" $?

# Extract the gate block (up to next ## header)
GATE_BLOCK=$(sed -n '/^## Phase 5 - Phase 6 Gate/,/^## /p' "$TARGET_FILE" | head -n -1)

# --- Test 2: Gate contains 12 required ## header checks ---
# The 12 required ## headers that must be checked
REQUIRED_H2=(
    "Description"
    "Acceptance Criteria"
    "Technical Specification"
    "Technical Limitations"
    "Non-Functional Requirements"
    "Dependencies"
    "Test Strategy"
    "Acceptance Criteria Verification Checklist"
    "Implementation Notes"
    "Definition of Done"
    "Change Log"
    "Notes"
)

h2_count=0
for header in "${REQUIRED_H2[@]}"; do
    if echo "$GATE_BLOCK" | grep -q "$header"; then
        ((h2_count++))
    fi
done
[ "$h2_count" -eq 12 ]
run_test "Gate checks all 12 required ## headers (found $h2_count/12)" $?

# --- Test 3: Gate contains 16 required ### subsection checks ---
REQUIRED_H3=(
    "Performance"
    "Security"
    "Scalability"
    "Reliability"
    "Observability"
    "Prerequisite Stories"
    "External Dependencies"
    "Technology Dependencies"
    "Unit Tests"
    "Integration Tests"
    "Implementation"
    "Quality"
    "Testing"
    "Documentation"
    "TDD Workflow Summary"
    "Files Created"
)

h3_count=0
for header in "${REQUIRED_H3[@]}"; do
    if echo "$GATE_BLOCK" | grep -q "$header"; then
        ((h3_count++))
    fi
done
[ "$h3_count" -eq 16 ]
run_test "Gate checks all 16 required ### subsections (found $h3_count/16)" $?

# --- Test 4: Total section checks = 28 ---
total=$((h2_count + h3_count))
[ "$total" -eq 28 ]
run_test "Total section checks equal 28 (found $total)" $?

# --- Test 5: Uses anchored patterns (^##) ---
echo "$GATE_BLOCK" | grep -q '\^##'
run_test "Gate uses anchored ^## pattern for header checks" $?

# --- Test 6: Uses anchored patterns (^###) ---
echo "$GATE_BLOCK" | grep -q '\^###'
run_test "Gate uses anchored ^### pattern for subsection checks" $?

# --- Test 7: ## Provenance NOT in MUST-match list ---
# Provenance should not appear as a required/must-match section
echo "$GATE_BLOCK" | grep -i "must\|required" | grep -qv "Provenance"
PROV_NOT_REQUIRED=$?
# Also check it's not in the main check list at all, or explicitly marked optional
echo "$GATE_BLOCK" | grep -q "Provenance.*MUST"
PROV_MUST=$?
[ "$PROV_MUST" -ne 0 ]
run_test "## Provenance excluded from MUST-match list" $?

# --- Test 8: Gate contains HALT directive ---
echo "$GATE_BLOCK" | grep -q "HALT"
run_test "Gate contains HALT directive" $?

# === Summary ===
echo ""
echo "Results: $PASSED passed, $FAILED failed out of 8 tests"
[ $FAILED -eq 0 ] && exit 0 || exit 1
