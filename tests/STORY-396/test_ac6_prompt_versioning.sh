#!/bin/bash
# Test: AC#6 - Prompt Versioning Integration for Rollback Capability
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
echo "AC#6: Prompt Versioning Tests"
echo "Story: STORY-396"
echo "============================================"
echo ""

# --- Test 1: Before-state snapshots exist ---
echo "--- Test Group 1: Before-state version snapshots ---"
for agent in "${AGENTS[@]}"; do
    SNAPSHOT_DIR="$PROJECT_ROOT/devforgeai/specs/prompt-versions/${agent}"
    if [ -d "$SNAPSHOT_DIR" ]; then
        # Check for any before-state file
        BEFORE_FILES=$(ls "$SNAPSHOT_DIR"/*before* "$SNAPSHOT_DIR"/*v1* 2>/dev/null | wc -l)
        if [ "$BEFORE_FILES" -gt 0 ]; then
            run_test "${agent} has before-state snapshot" 0
        else
            run_test "${agent} has before-state snapshot" 1
        fi
    else
        run_test "${agent} has before-state snapshot (dir missing)" 1
    fi
done
echo ""

# --- Test 2: After-state version records exist ---
echo "--- Test Group 2: After-state version records ---"
for agent in "${AGENTS[@]}"; do
    SNAPSHOT_DIR="$PROJECT_ROOT/devforgeai/specs/prompt-versions/${agent}"
    if [ -d "$SNAPSHOT_DIR" ]; then
        AFTER_FILES=$(ls "$SNAPSHOT_DIR"/*after* "$SNAPSHOT_DIR"/*v2* 2>/dev/null | wc -l)
        if [ "$AFTER_FILES" -gt 0 ]; then
            run_test "${agent} has after-state record" 0
        else
            run_test "${agent} has after-state record" 1
        fi
    else
        run_test "${agent} has after-state record (dir missing)" 1
    fi
done
echo ""

# --- Test 3: Version records contain SHA-256 hash ---
echo "--- Test Group 3: SHA-256 hash in version records ---"
for agent in "${AGENTS[@]}"; do
    SNAPSHOT_DIR="$PROJECT_ROOT/devforgeai/specs/prompt-versions/${agent}"
    if [ -d "$SNAPSHOT_DIR" ]; then
        if grep -rq 'sha256\|SHA-256\|SHA256\|[a-f0-9]\{64\}' "$SNAPSHOT_DIR/" 2>/dev/null; then
            run_test "${agent} version records have SHA-256 hash" 0
        else
            run_test "${agent} version records have SHA-256 hash" 1
        fi
    else
        run_test "${agent} version records have SHA-256 hash (dir missing)" 1
    fi
done
echo ""

# --- Test 4: All agents have version: "2.0.0" in YAML frontmatter ---
echo "--- Test Group 4: version 2.0.0 in frontmatter ---"
for agent in "${AGENTS[@]}"; do
    AGENT_FILE="$PROJECT_ROOT/src/claude/agents/${agent}.md"
    if [ -f "$AGENT_FILE" ]; then
        if grep -q 'version:.*"2\.0\.0"' "$AGENT_FILE" 2>/dev/null; then
            run_test "${agent} has version: \"2.0.0\" in frontmatter" 0
        else
            run_test "${agent} has version: \"2.0.0\" in frontmatter" 1
        fi
    else
        run_test "${agent} has version: \"2.0.0\" (file missing)" 1
    fi
done
echo ""

# --- Test 5: Version directories exist ---
echo "--- Test Group 5: Version directory naming ---"
for agent in "${AGENTS[@]}"; do
    SNAPSHOT_DIR="$PROJECT_ROOT/devforgeai/specs/prompt-versions/${agent}"
    if [ -d "$SNAPSHOT_DIR" ]; then
        run_test "${agent} version dir at prompt-versions/${agent}/" 0
    else
        run_test "${agent} version dir at prompt-versions/${agent}/" 1
    fi
done
echo ""

# === Summary ===
echo "============================================"
echo "AC#6 Results: $PASSED passed, $FAILED failed"
echo "============================================"
if [ "$FAILED" -eq 0 ]; then exit 0; else exit 1; fi
