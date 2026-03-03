#!/bin/bash
# Test: AC#3 - Before-State Captured and After-State Evaluated via Pipeline
# Story: STORY-395
# Generated: 2026-02-13
# TDD Phase: RED (tests expected to FAIL before migration)
#
# Validates that before-state snapshots are captured via prompt versioning,
# after-state evaluation scores 5+ dimensions, and wave summary exists.

set -uo pipefail

# === Test Configuration ===
PASSED=0
FAILED=0
TOTAL=0
PROJECT_ROOT="${PROJECT_ROOT:-$(cd "$(dirname "$0")/../.." && pwd)}"
PROMPT_VERSIONS_DIR="$PROJECT_ROOT/devforgeai/specs/prompt-versions"
WAVE_SUMMARY="$PROJECT_ROOT/devforgeai/specs/research/wave1-evaluation-results.md"

AGENTS=(
    "anti-pattern-scanner"
    "context-validator"
    "context-preservation-validator"
    "coverage-analyzer"
    "code-quality-auditor"
    "deferral-validator"
    "dependency-graph-analyzer"
    "file-overlap-detector"
    "pattern-compliance-auditor"
    "tech-stack-detector"
)

run_test() {
    local name="$1"
    local result="$2"
    ((TOTAL++))
    if [ "$result" -eq 0 ]; then
        echo "  PASS: $name"
        ((PASSED++))
    else
        echo "  FAIL: $name"
        ((FAILED++))
    fi
}

echo "=============================================="
echo "  AC#3: Before/After Evaluation Pipeline"
echo "  Testing snapshots, evaluation, wave summary"
echo "=============================================="
echo ""

# --- Test Group 1: Before-state snapshots exist ---
echo "--- Test Group 1: Before-State Snapshots ---"
for agent in "${AGENTS[@]}"; do
    test -d "$PROMPT_VERSIONS_DIR/${agent}" && RC=0 || RC=1
    run_test "Prompt versions directory exists: ${agent}" $RC
done
echo ""

# --- Test Group 2: Before-state contains SHA-256 hash ---
echo "--- Test Group 2: SHA-256 Hash in Snapshots ---"
for agent in "${AGENTS[@]}"; do
    AGENT_VERSION_DIR="$PROMPT_VERSIONS_DIR/${agent}"
    if [ ! -d "$AGENT_VERSION_DIR" ]; then
        run_test "SHA-256 hash present: ${agent} (dir missing)" 1
        continue
    fi

    FOUND_HASH=false
    for file in "$AGENT_VERSION_DIR"/*; do
        if [ -f "$file" ]; then
            if grep -qE '[a-f0-9]{64}' "$file" 2>/dev/null; then
                FOUND_HASH=true
                break
            fi
        fi
    done

    if [ "$FOUND_HASH" = true ]; then
        run_test "SHA-256 hash in snapshot: ${agent}" 0
    else
        run_test "SHA-256 hash in snapshot: ${agent}" 1
    fi
done
echo ""

# --- Test Group 3: Before-state snapshot has original content ---
echo "--- Test Group 3: Before-State Contains Original Content ---"
for agent in "${AGENTS[@]}"; do
    AGENT_VERSION_DIR="$PROMPT_VERSIONS_DIR/${agent}"
    if [ ! -d "$AGENT_VERSION_DIR" ]; then
        run_test "Original content preserved: ${agent} (dir missing)" 1
        continue
    fi

    FOUND_CONTENT=false
    for file in "$AGENT_VERSION_DIR"/*; do
        if [ -f "$file" ]; then
            LINE_COUNT=$(wc -l < "$file" 2>/dev/null || echo "0")
            if [ "$LINE_COUNT" -gt 50 ]; then
                FOUND_CONTENT=true
                break
            fi
        fi
    done

    if [ "$FOUND_CONTENT" = true ]; then
        run_test "Original content preserved (>50 lines): ${agent}" 0
    else
        run_test "Original content preserved (>50 lines): ${agent}" 1
    fi
done
echo ""

# --- Test Group 4: Wave summary document exists ---
echo "--- Test Group 4: Wave Summary Document ---"
test -f "$WAVE_SUMMARY" && RC=0 || RC=1
run_test "Wave summary file exists: wave1-evaluation-results.md" $RC

if [ -f "$WAVE_SUMMARY" ]; then
    for agent in "${AGENTS[@]}"; do
        grep -qi "${agent}" "$WAVE_SUMMARY" && RC=0 || RC=1
        run_test "Agent mentioned in wave summary: ${agent}" $RC
    done

    DIMENSION_COUNT=$(grep -ciE '(dimension|quality|score|metric|criterion)' "$WAVE_SUMMARY" || true)
    if [ "$DIMENSION_COUNT" -ge 5 ]; then
        run_test "Wave summary has 5+ quality dimension references" 0
    else
        run_test "Wave summary has 5+ quality dimension references (found: $DIMENSION_COUNT)" 1
    fi

    grep -qiE '(improved|improvement|regress)' "$WAVE_SUMMARY" && RC=0 || RC=1
    run_test "Wave summary contains improvement/regression analysis" $RC
else
    for agent in "${AGENTS[@]}"; do
        run_test "Agent mentioned in wave summary: ${agent} (file missing)" 1
    done
    run_test "Wave summary has 5+ quality dimension references (file missing)" 1
    run_test "Wave summary contains improvement/regression analysis (file missing)" 1
fi
echo ""

# === Summary ===
echo "=============================================="
echo "  AC#3 Before/After Evaluation Results"
echo "=============================================="
echo "  Total:  $TOTAL"
echo "  Passed: $PASSED"
echo "  Failed: $FAILED"
echo "=============================================="

if [ "$FAILED" -eq 0 ]; then
    echo "  STATUS: ALL TESTS PASSED"
    exit 0
else
    echo "  STATUS: $FAILED TESTS FAILED"
    exit 1
fi
