#!/bin/bash
# Test: AC#3 - Before-State Captured and After-State Evaluated via Pipeline
# Story: STORY-396
# Generated: 2026-02-13
# TDD Phase: RED (tests should FAIL before migration)

# === Test Configuration ===
PASSED=0
FAILED=0
PROJECT_ROOT="/mnt/c/Projects/DevForgeAI2"

AGENTS=(
    "backend-architect"
    "frontend-developer"
    "code-reviewer"
    "refactoring-specialist"
    "integration-tester"
    "api-designer"
    "deployment-engineer"
    "security-auditor"
    "code-analyzer"
)

run_test() {
    local name="$1"
    local result="$2"
    if [ "$result" -eq 0 ]; then
        echo "  PASS: $name"
        PASSED=$((PASSED + 1))
    else
        echo "  FAIL: $name"
        FAILED=$((FAILED + 1))
    fi
}

echo "============================================"
echo "AC#3: Before/After Evaluation Tests"
echo "Story: STORY-396"
echo "============================================"
echo ""

# --- Test 1: Before-state snapshots exist for all 9 agents ---
echo "--- Test Group 1: Before-state snapshots ---"
for agent in "${AGENTS[@]}"; do
    SNAPSHOT_DIR="$PROJECT_ROOT/devforgeai/specs/prompt-versions/${agent}"
    if [ -d "$SNAPSHOT_DIR" ]; then
        run_test "${agent} has prompt-versions directory" 0
    else
        run_test "${agent} has prompt-versions directory" 1
    fi
done
echo ""

# --- Test 2: Before-state snapshots contain SHA-256 hash ---
echo "--- Test Group 2: SHA-256 hash in before-state ---"
for agent in "${AGENTS[@]}"; do
    SNAPSHOT_DIR="$PROJECT_ROOT/devforgeai/specs/prompt-versions/${agent}"
    if [ -d "$SNAPSHOT_DIR" ]; then
        if grep -rq "sha256\|SHA-256\|SHA256" "$SNAPSHOT_DIR/" 2>/dev/null; then
            run_test "${agent} before-state has SHA-256 hash" 0
        else
            run_test "${agent} before-state has SHA-256 hash" 1
        fi
    else
        run_test "${agent} before-state has SHA-256 hash (dir missing)" 1
    fi
done
echo ""

# --- Test 3: Wave 2 evaluation results document exists ---
echo "--- Test Group 3: Wave 2 evaluation results ---"
WAVE2_RESULTS="$PROJECT_ROOT/devforgeai/specs/research/wave2-evaluation-results.md"
if [ -f "$WAVE2_RESULTS" ]; then
    run_test "wave2-evaluation-results.md exists" 0
else
    run_test "wave2-evaluation-results.md exists" 1
fi

for agent in "${AGENTS[@]}"; do
    if [ -f "$WAVE2_RESULTS" ]; then
        if grep -q "$agent" "$WAVE2_RESULTS" 2>/dev/null; then
            run_test "${agent} listed in wave2 results" 0
        else
            run_test "${agent} listed in wave2 results" 1
        fi
    else
        run_test "${agent} listed in wave2 results (file missing)" 1
    fi
done
echo ""

# --- Test 4: Quality dimensions - 3 of 5 improved, 0 regressed ---
echo "--- Test Group 4: Quality dimension improvements ---"
if [ -f "$WAVE2_RESULTS" ]; then
    if grep -qi "improved\|improvement" "$WAVE2_RESULTS" 2>/dev/null; then
        run_test "Wave2 results contain improvement metrics" 0
    else
        run_test "Wave2 results contain improvement metrics" 1
    fi
    if grep -qi "0.*regress\|regress.*0\|no.*regress" "$WAVE2_RESULTS" 2>/dev/null; then
        run_test "Wave2 results show 0 regressions" 0
    else
        run_test "Wave2 results show 0 regressions" 1
    fi
else
    run_test "Wave2 results contain improvement metrics (file missing)" 1
    run_test "Wave2 results show 0 regressions (file missing)" 1
fi
echo ""

# === Summary ===
echo "============================================"
echo "AC#3 Results: $PASSED passed, $FAILED failed"
echo "============================================"
if [ "$FAILED" -eq 0 ]; then exit 0; else exit 1; fi
