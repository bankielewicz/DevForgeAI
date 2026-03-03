#!/bin/bash

# STORY-147: AC#1 - complexity-assessment-matrix.md remains authoritative source
# Test Purpose: Verify matrix contains complete Tier 1-4 technology recommendations
#
# AC#1: complexity-assessment-matrix.md remains authoritative source
# Given: complexity-assessment-matrix.md contains full technology recommendations per tier,
# When: developers need detailed tech recommendations,
# Then: this file is the single source of truth with:
#   - Tier 1 (Simple) recommendations
#   - Tier 2 (Moderate) recommendations
#   - Tier 3 (Complex) recommendations
#   - Tier 4 (Enterprise) recommendations

set -e

MATRIX_FILE=".claude/skills/devforgeai-ideation/references/complexity-assessment-matrix.md"
PROJECT_ROOT="$(pwd)"

echo "Testing AC#1: complexity-assessment-matrix.md remains authoritative source"
echo "=================================================================="
echo ""

# Test 1: File exists
echo "Test 1: complexity-assessment-matrix.md exists..."
if [ ! -f "$MATRIX_FILE" ]; then
    echo "FAIL: File not found: $MATRIX_FILE"
    exit 1
fi
echo "PASS: File exists"
echo ""

# Test 2: File contains Tier 1 section
echo "Test 2: Matrix contains Tier 1 (Simple Application) section..."
if ! grep -q "### Tier 1: Simple Application" "$MATRIX_FILE"; then
    echo "FAIL: Missing '### Tier 1: Simple Application' header"
    exit 1
fi
echo "PASS: Tier 1 section found"
echo ""

# Test 3: File contains Tier 2 section
echo "Test 3: Matrix contains Tier 2 (Moderate Application) section..."
if ! grep -q "### Tier 2: Moderate Application" "$MATRIX_FILE"; then
    echo "FAIL: Missing '### Tier 2: Moderate Application' header"
    exit 1
fi
echo "PASS: Tier 2 section found"
echo ""

# Test 4: File contains Tier 3 section
echo "Test 4: Matrix contains Tier 3 (Complex Platform) section..."
if ! grep -q "### Tier 3: Complex Platform" "$MATRIX_FILE"; then
    echo "FAIL: Missing '### Tier 3: Complex Platform' header"
    exit 1
fi
echo "PASS: Tier 3 section found"
echo ""

# Test 5: File contains Tier 4 section
echo "Test 5: Matrix contains Tier 4 (Enterprise Platform) section..."
if ! grep -q "### Tier 4: Enterprise Platform" "$MATRIX_FILE"; then
    echo "FAIL: Missing '### Tier 4: Enterprise Platform' header"
    exit 1
fi
echo "PASS: Tier 4 section found"
echo ""

# Test 6: Tier 1 has technology recommendations (backend, frontend, database, etc)
echo "Test 6: Tier 1 section contains technology recommendations..."
TIER1_SECTION=$(awk '/### Tier 1: Simple Application/,/### Tier 2: Moderate Application/' "$MATRIX_FILE")
if ! echo "$TIER1_SECTION" | grep -q "Technology Stack Suggestions:"; then
    echo "FAIL: Tier 1 section missing technology recommendations"
    exit 1
fi
echo "PASS: Tier 1 has recommendations"
echo ""

# Test 7: Tier 2 has technology recommendations
echo "Test 7: Tier 2 section contains technology recommendations..."
TIER2_SECTION=$(awk '/### Tier 2: Moderate Application/,/### Tier 3: Complex Platform/' "$MATRIX_FILE")
if ! echo "$TIER2_SECTION" | grep -q "Technology Stack Suggestions:"; then
    echo "FAIL: Tier 2 section missing technology recommendations"
    exit 1
fi
echo "PASS: Tier 2 has recommendations"
echo ""

# Test 8: Tier 3 has technology recommendations
echo "Test 8: Tier 3 section contains technology recommendations..."
TIER3_SECTION=$(awk '/### Tier 3: Complex Platform/,/### Tier 4: Enterprise Platform/' "$MATRIX_FILE")
if ! echo "$TIER3_SECTION" | grep -q "Technology Stack Suggestions:"; then
    echo "FAIL: Tier 3 section missing technology recommendations"
    exit 1
fi
echo "PASS: Tier 3 has recommendations"
echo ""

# Test 9: Tier 4 has technology recommendations
echo "Test 9: Tier 4 section contains technology recommendations..."
TIER4_SECTION=$(awk '/### Tier 4: Enterprise Platform/,/^---/' "$MATRIX_FILE")
if ! echo "$TIER4_SECTION" | grep -q "Technology Stack Suggestions:"; then
    echo "FAIL: Tier 4 section missing technology recommendations"
    exit 1
fi
echo "PASS: Tier 4 has recommendations"
echo ""

# Test 10: Verify "Technology Recommendations by Tier" section exists
echo "Test 10: Matrix has 'Technology Recommendations by Tier' section..."
if ! grep -q "## Technology Recommendations by Tier" "$MATRIX_FILE"; then
    echo "FAIL: Missing main 'Technology Recommendations by Tier' section"
    exit 1
fi
echo "PASS: Technology Recommendations by Tier section exists"
echo ""

echo "=================================================================="
echo "AC#1: All tests PASSED"
echo "Matrix is verified as authoritative source with complete Tier 1-4 recommendations"
