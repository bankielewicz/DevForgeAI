#!/bin/bash
# Test: AC#6 - Both Explicit and Extracted Observations Captured
# Story: STORY-336
# Expected: FAIL (RED phase) - Dual source capture not implemented yet

set -e

PHASE02=".claude/skills/devforgeai-development/phases/phase-02-test-first.md"
PHASE03=".claude/skills/devforgeai-development/phases/phase-03-implementation.md"
PHASE04=".claude/skills/devforgeai-development/phases/phase-04-refactoring.md"
TEST_NAME="AC6: Explicit and Extracted Observations"

echo "=== $TEST_NAME ==="

# Test 1: Verify 'source: "explicit"' documented
echo "Test 1: Checking for source: 'explicit' documentation..."
FOUND_EXPLICIT=false
for f in $PHASE02 $PHASE03 $PHASE04; do
    if grep -qE 'source.*explicit|"explicit"' "$f"; then
        FOUND_EXPLICIT=true
        break
    fi
done

if [ "$FOUND_EXPLICIT" = true ]; then
    echo "  PASS: source: 'explicit' found"
else
    echo "  FAIL: source: 'explicit' not documented"
    exit 1
fi

# Test 2: Verify 'source: "extracted"' documented
echo "Test 2: Checking for source: 'extracted' documentation..."
FOUND_EXTRACTED=false
for f in $PHASE02 $PHASE03 $PHASE04; do
    if grep -qE 'source.*extracted|"extracted"' "$f"; then
        FOUND_EXTRACTED=true
        break
    fi
done

if [ "$FOUND_EXTRACTED" = true ]; then
    echo "  PASS: source: 'extracted' found"
else
    echo "  FAIL: source: 'extracted' not documented"
    exit 1
fi

# Test 3: Verify observation-extractor subagent invocation for extracted observations
echo "Test 3: Checking for observation-extractor invocation..."
FOUND_EXTRACTOR=false
for f in $PHASE02 $PHASE03 $PHASE04; do
    if grep -q "observation-extractor" "$f"; then
        FOUND_EXTRACTOR=true
        break
    fi
done

if [ "$FOUND_EXTRACTOR" = true ]; then
    echo "  PASS: observation-extractor invocation found"
else
    echo "  FAIL: observation-extractor not invoked for extracted observations"
    exit 1
fi

# Test 4: Verify explicit observation collection instructions
echo "Test 4: Checking for explicit observation collection from subagent returns..."
FOUND_COLLECT=false
for f in $PHASE02 $PHASE03 $PHASE04; do
    if grep -qi "Collect Explicit\|explicit.*observation\|subagent.*observations\[\]" "$f"; then
        FOUND_COLLECT=true
        break
    fi
done

if [ "$FOUND_COLLECT" = true ]; then
    echo "  PASS: Explicit observation collection instructions found"
else
    echo "  FAIL: Explicit observation collection instructions missing"
    exit 1
fi

echo "=== All $TEST_NAME tests passed ==="
exit 0
