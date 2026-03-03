#!/bin/bash
# STORY-319 AC#5: AC-Compliance-Verifier Extraction Rules
# Tests that extraction rules for ac-compliance-verifier output are documented
# Expected: FAIL (file does not exist yet - TDD Red phase)

set -e

SOURCE_FILE="src/claude/agents/observation-extractor.md"

echo "=== AC#5: AC-Compliance-Verifier Extraction Rules Tests ==="

# Pre-check: File must exist
if [ ! -f "$SOURCE_FILE" ]; then
    echo "FAIL: Source file does not exist: $SOURCE_FILE"
    exit 1
fi

# Test 5.1: Extraction rule for verification_results[] exists
echo -n "Test 5.1: Extraction rule for 'verification_results' documented... "
if grep -q "verification_results" "$SOURCE_FILE"; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: Reference to 'verification_results' extraction rule"
    exit 1
fi

# Test 5.2: FAIL status extraction documented
echo -n "Test 5.2: FAIL status extraction documented... "
if grep -qi "FAIL\|fail\|failed" "$SOURCE_FILE"; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: Reference to FAIL status in extraction rules"
    exit 1
fi

# Test 5.3: Failed verifications map to category "gap"
echo -n "Test 5.3: Failed verifications map to category 'gap'... "
if grep -A10 -B10 "verification_results" "$SOURCE_FILE" | grep -qi "gap"; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: Failed verifications to map to category 'gap'"
    exit 1
fi

# Test 5.4: ac-compliance-verifier is mentioned as source subagent
echo -n "Test 5.4: ac-compliance-verifier mentioned as source subagent... "
if grep -qi "ac-compliance-verifier" "$SOURCE_FILE"; then
    echo "PASS"
else
    echo "FAIL"
    echo "  Expected: Reference to 'ac-compliance-verifier' subagent"
    exit 1
fi

echo ""
echo "=== AC#5: All tests passed ==="
exit 0
