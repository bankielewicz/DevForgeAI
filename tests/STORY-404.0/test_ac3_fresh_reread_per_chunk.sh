#!/usr/bin/env bash
# STORY-404 AC#3: Fresh re-read per chunk
# TDD Red Phase - These tests MUST fail before implementation
#
# Validates that the ac-compliance-verifier specification documents:
# - Story file re-read at start of each chunk
# - Fresh Read() call per chunk (not reusing cached content)
# - This applies specifically to chunked mode (5+ ACs)
#
# Expected: FAIL initially (chunking logic not yet in verifier spec)

set -uo pipefail

PROJECT_ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
VERIFIER_FILE="${PROJECT_ROOT}/src/claude/agents/ac-compliance-verifier.md"

PASS=0
FAIL=0
TOTAL=0

run_test() {
    local name="$1"
    local result="$2"
    TOTAL=$((TOTAL + 1))
    if [ "$result" -eq 0 ]; then
        PASS=$((PASS + 1))
        echo "  PASS: $name"
    else
        FAIL=$((FAIL + 1))
        echo "  FAIL: $name"
    fi
}

echo "=== AC#3: Fresh Re-Read Per Chunk ==="
echo ""

# Test 1: Verifier source file exists
if [ -f "$VERIFIER_FILE" ]; then
    run_test "Verifier source file exists" 0
else
    run_test "Verifier source file exists" 1
    echo "--- AC#3 Results: $PASS/$TOTAL passed, $FAIL failed ---"
    exit 1
fi

# Test 2: Spec documents re-reading the story file per chunk
# Must specifically mention re-reading in context of chunks (not generic fresh-context)
if grep -qiP 're-?read.*chunk|chunk.*re-?read|Read\(\).*each chunk|Read\(\).*per chunk|read.*story.*each.*chunk' "$VERIFIER_FILE" 2>/dev/null; then
    run_test "Spec documents re-reading story file per chunk" 0
else
    run_test "Spec documents re-reading story file per chunk" 1
fi

# Test 3: Spec mentions fresh context per chunk (not reusing cached content)
if grep -qiP 'fresh.*context.*chunk|fresh.*per.*chunk|no.*cached|avoid.*stale|start.*fresh.*each.*chunk' "$VERIFIER_FILE" 2>/dev/null; then
    run_test "Spec mentions fresh context per chunk" 0
else
    run_test "Spec mentions fresh context per chunk" 1
fi

# Test 4: Spec shows Read() call pattern for per-chunk re-reading
if grep -qP 'Read\(.*file_path.*story.*\).*chunk|FOR.*each.*chunk.*Read\(' "$VERIFIER_FILE" 2>/dev/null; then
    run_test "Spec shows Read() call pattern for per-chunk operation" 0
else
    run_test "Spec shows Read() call pattern for per-chunk operation" 1
fi

echo ""
echo "--- AC#3 Results: $PASS/$TOTAL passed, $FAIL failed ---"

if [ "$FAIL" -gt 0 ]; then
    exit 1
fi
exit 0
