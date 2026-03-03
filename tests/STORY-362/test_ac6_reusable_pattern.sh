#!/usr/bin/env bash
# =============================================================================
# STORY-362 AC#6: Reusable Fallback Pattern Documented in Reference File
# =============================================================================
# Validates that treelint-search-patterns.md:
#   1. Contains a complete decision tree with 6 numbered steps
#   2. Grep equivalents for all 4 search types (function, class, map, deps)
#   3. Pattern is subagent-agnostic (no agent-specific branches)
#   4. Decision tree section exists with proper heading
#   5. Steps are in correct order per AC#6 specification
#
# TDD Phase: RED - Tests expected to FAIL until implementation complete.
# =============================================================================

set -euo pipefail

PROJECT_ROOT="${PROJECT_ROOT:-/mnt/c/Projects/DevForgeAI2}"
TARGET_FILE="${PROJECT_ROOT}/src/claude/agents/references/treelint-search-patterns.md"

PASS_COUNT=0
FAIL_COUNT=0
TOTAL_COUNT=0

pass() {
    PASS_COUNT=$((PASS_COUNT + 1))
    TOTAL_COUNT=$((TOTAL_COUNT + 1))
    echo "  PASS: $1"
}

fail() {
    FAIL_COUNT=$((FAIL_COUNT + 1))
    TOTAL_COUNT=$((TOTAL_COUNT + 1))
    echo "  FAIL: $1"
}

echo "=============================================="
echo "  AC#6: Reusable Fallback Pattern"
echo "=============================================="
echo ""

# -----------------------------------------------------------------------------
# Test 1: File exists
# -----------------------------------------------------------------------------
echo "--- Test 1: File Existence ---"
if [[ -r "$TARGET_FILE" ]]; then
    pass "Reference file exists"
else
    fail "Reference file does not exist"
    echo ""
    echo "=============================================="
    echo "  AC#6 Results: ${PASS_COUNT} passed, ${FAIL_COUNT} failed (${TOTAL_COUNT} total)"
    echo "=============================================="
    echo "  STATUS: FAILED (file does not exist - RED phase expected)"
    exit 1
fi
echo ""

# -----------------------------------------------------------------------------
# Test 2: Fallback Decision Tree section exists
# Must have a section heading containing "Fallback Decision Tree"
# -----------------------------------------------------------------------------
echo "--- Test 2: Decision Tree Section Heading ---"
if grep -qiE '^#{1,3} .*Fallback Decision Tree' "$TARGET_FILE" 2>/dev/null; then
    pass "Fallback Decision Tree section heading found"
else
    fail "Missing 'Fallback Decision Tree' section heading"
fi
echo ""

# -----------------------------------------------------------------------------
# Test 3: Decision tree contains 6 numbered steps
# AC#6 requires: (1) check extension, (2) attempt Treelint, (3) detect failure,
# (4) fall back to Grep, (5) log warning, (6) return results
# Note: Current file has 4 steps; AC#6 requires 6 for the full pattern
# -----------------------------------------------------------------------------
echo "--- Test 3: Six Decision Tree Steps ---"
step_count=0

# Step 1: Check file extension
if grep -qiE 'Step 1' "$TARGET_FILE" 2>/dev/null; then
    step_count=$((step_count + 1))
fi

# Step 2: Attempt Treelint if supported
if grep -qiE 'Step 2' "$TARGET_FILE" 2>/dev/null; then
    step_count=$((step_count + 1))
fi

# Step 3: Detect failure via exit code
if grep -qiE 'Step 3' "$TARGET_FILE" 2>/dev/null; then
    step_count=$((step_count + 1))
fi

# Step 4: Fall back to Grep with equivalent pattern
if grep -qiE 'Step 4' "$TARGET_FILE" 2>/dev/null; then
    step_count=$((step_count + 1))
fi

# Step 5: Log warning with reason
if grep -qiE 'Step 5' "$TARGET_FILE" 2>/dev/null; then
    step_count=$((step_count + 1))
fi

# Step 6: Return results
if grep -qiE 'Step 6' "$TARGET_FILE" 2>/dev/null; then
    step_count=$((step_count + 1))
fi

if [[ "$step_count" -ge 6 ]]; then
    pass "Decision tree contains 6 numbered steps (found ${step_count})"
else
    fail "Decision tree has only ${step_count} steps (6 required per AC#6)"
fi
echo ""

# -----------------------------------------------------------------------------
# Test 4: Step order validation
# Step 1 must be extension check, Step 5 must be warning, Step 6 must be return
# -----------------------------------------------------------------------------
echo "--- Test 4: Step Order Validation ---"

# Step 1 must be about extension checking
if grep -qiE 'Step 1.*extension|Step 1.*file type|Step 1.*check' "$TARGET_FILE" 2>/dev/null; then
    pass "Step 1 is extension check (correct order)"
else
    fail "Step 1 is not extension check (must be first per AC#6)"
fi

# Step 5 must be about warning/logging
if grep -qiE 'Step 5.*(warn|log|emit|display)' "$TARGET_FILE" 2>/dev/null; then
    pass "Step 5 is warning/logging (correct order)"
else
    fail "Step 5 is not warning/logging step"
fi

# Step 6 must be about returning results
if grep -qiE 'Step 6.*(return|results|output|complete)' "$TARGET_FILE" 2>/dev/null; then
    pass "Step 6 is return results (correct order)"
else
    fail "Step 6 is not return results step"
fi
echo ""

# -----------------------------------------------------------------------------
# Test 5: Grep equivalents for all 4 Treelint search types
# Count distinct Grep patterns for: function, class, map, deps
# -----------------------------------------------------------------------------
echo "--- Test 5: Grep Equivalents for 4 Search Types ---"
search_type_coverage=0

if grep -qiE 'function.*(Grep|fallback)|Grep.*function' "$TARGET_FILE" 2>/dev/null; then
    search_type_coverage=$((search_type_coverage + 1))
fi

if grep -qiE 'class.*(Grep|fallback)|Grep.*class' "$TARGET_FILE" 2>/dev/null; then
    search_type_coverage=$((search_type_coverage + 1))
fi

if grep -qiE 'map.*(Grep|Glob|fallback)|(Grep|Glob).*map' "$TARGET_FILE" 2>/dev/null; then
    search_type_coverage=$((search_type_coverage + 1))
fi

if grep -qiE 'deps.*(Grep|fallback)|Grep.*deps|import.*(Grep|fallback)' "$TARGET_FILE" 2>/dev/null; then
    search_type_coverage=$((search_type_coverage + 1))
fi

if [[ "$search_type_coverage" -ge 4 ]]; then
    pass "Grep equivalents for all 4 search types (function, class, map, deps)"
else
    fail "Only ${search_type_coverage}/4 search types have Grep equivalents"
fi
echo ""

# -----------------------------------------------------------------------------
# Test 6: Pattern is subagent-agnostic (NFR-004)
# Must NOT contain agent-specific conditional logic
# Check for absence of individual subagent names in conditional branches
# -----------------------------------------------------------------------------
echo "--- Test 6: Subagent-Agnostic Pattern (NFR-004) ---"
agent_specific_count=0

# Check for conditional branches that name specific agents
for agent in "test-automator" "backend-architect" "code-reviewer" "security-auditor" "refactoring-specialist" "coverage-analyzer" "anti-pattern-scanner"; do
    if grep -qiE "(if|when|case).*${agent}" "$TARGET_FILE" 2>/dev/null; then
        agent_specific_count=$((agent_specific_count + 1))
    fi
done

if [[ "$agent_specific_count" -eq 0 ]]; then
    pass "No subagent-specific conditional branches found (NFR-004)"
else
    fail "Found ${agent_specific_count} subagent-specific conditional branches (NFR-004 violation)"
fi
echo ""

# =============================================================================
# Summary
# =============================================================================
echo "=============================================="
echo "  AC#6 Results: ${PASS_COUNT} passed, ${FAIL_COUNT} failed (${TOTAL_COUNT} total)"
echo "=============================================="

if [[ "$FAIL_COUNT" -gt 0 ]]; then
    echo "  STATUS: FAILED"
    exit 1
else
    echo "  STATUS: PASSED"
    exit 0
fi
