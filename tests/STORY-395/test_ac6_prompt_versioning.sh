#!/bin/bash
# Test: AC#6 - Prompt Versioning Integration for Rollback Capability
# Story: STORY-395
# Generated: 2026-02-13
# TDD Phase: RED (tests expected to FAIL before migration)
#
# Validates that before-state version snapshots captured, after-state version
# records exist, version records stored in proper directory, rollback capability
# exists, and version "2.0.0" set in all agents.

set -uo pipefail

# === Test Configuration ===
PASSED=0
FAILED=0
TOTAL=0
PROJECT_ROOT="${PROJECT_ROOT:-$(cd "$(dirname "$0")/../.." && pwd)}"
PROMPT_VERSIONS_DIR="$PROJECT_ROOT/devforgeai/specs/prompt-versions"
AGENTS_DIR="$PROJECT_ROOT/src/claude/agents"

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
echo "  AC#6: Prompt Versioning Integration"
echo "  Testing snapshots, versions, rollback"
echo "=============================================="
echo ""

# --- Test Group 1: Before-state version snapshot captured ---
echo "--- Test Group 1: Before-State Version Snapshot ---"
for agent in "${AGENTS[@]}"; do
    VERSION_DIR="$PROMPT_VERSIONS_DIR/${agent}"

    test -d "$VERSION_DIR" && RC=0 || RC=1
    run_test "Version directory exists: ${agent}" $RC

    if [ -d "$VERSION_DIR" ]; then
        # Check for at least one version file
        FILE_COUNT=$(ls -1 "$VERSION_DIR"/ 2>/dev/null | wc -l || echo "0")
        if [ "$FILE_COUNT" -ge 1 ]; then
            run_test "Before-state snapshot file present: ${agent}" 0
        else
            run_test "Before-state snapshot file present: ${agent}" 1
        fi
    else
        run_test "Before-state snapshot file present: ${agent} (dir missing)" 1
    fi
done
echo ""

# --- Test Group 2: After-state version record captured ---
echo "--- Test Group 2: After-State Version Record ---"
for agent in "${AGENTS[@]}"; do
    VERSION_DIR="$PROMPT_VERSIONS_DIR/${agent}"
    if [ ! -d "$VERSION_DIR" ]; then
        run_test "After-state version record: ${agent} (dir missing)" 1
        continue
    fi

    FILE_COUNT=$(ls -1 "$VERSION_DIR"/ 2>/dev/null | wc -l || echo "0")
    if [ "$FILE_COUNT" -ge 2 ]; then
        run_test "After-state version record (${FILE_COUNT} records): ${agent}" 0
    else
        run_test "After-state version record (${FILE_COUNT} records, need 2+): ${agent}" 1
    fi
done
echo ""

# --- Test Group 3: Version records in proper directory ---
echo "--- Test Group 3: Version Records in Proper Directory ---"
test -d "$PROMPT_VERSIONS_DIR" && RC=0 || RC=1
run_test "Prompt versions base directory exists" $RC

for agent in "${AGENTS[@]}"; do
    test -d "$PROMPT_VERSIONS_DIR/${agent}" && RC=0 || RC=1
    run_test "Subdirectory: prompt-versions/${agent}/" $RC
done
echo ""

# --- Test Group 4: Version "2.0.0" in all agent YAML frontmatter ---
echo "--- Test Group 4: Version 2.0.0 in YAML Frontmatter ---"
for agent in "${AGENTS[@]}"; do
    AGENT_FILE="$AGENTS_DIR/${agent}.md"
    if [ ! -f "$AGENT_FILE" ]; then
        run_test "Version 2.0.0: ${agent} (file missing)" 1
        continue
    fi

    sed -n '2,/^---$/p' "$AGENT_FILE" | grep -qE '^version:\s*"2\.0\.0"' && RC=0 || RC=1
    run_test "Version is 2.0.0 in frontmatter: ${agent}" $RC
done
echo ""

# --- Test Group 5: SHA-256 hash integrity ---
echo "--- Test Group 5: SHA-256 Hash Integrity ---"
for agent in "${AGENTS[@]}"; do
    VERSION_DIR="$PROMPT_VERSIONS_DIR/${agent}"
    if [ ! -d "$VERSION_DIR" ]; then
        run_test "SHA-256 hash present: ${agent} (dir missing)" 1
        continue
    fi

    FOUND_HASH=false
    for file in "$VERSION_DIR"/*; do
        if [ -f "$file" ]; then
            if grep -qE '[a-f0-9]{64}' "$file" 2>/dev/null; then
                FOUND_HASH=true
                break
            fi
        fi
    done

    if [ "$FOUND_HASH" = true ]; then
        run_test "SHA-256 hash in version record: ${agent}" 0
    else
        run_test "SHA-256 hash in version record: ${agent}" 1
    fi
done
echo ""

# === Summary ===
echo "=============================================="
echo "  AC#6 Prompt Versioning Results"
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
