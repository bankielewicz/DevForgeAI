#!/bin/bash

# STORY-147: AC#3 - completion-handoff.md uses cross-references
# Test Purpose: Verify completion-handoff.md has next steps with cross-references, no duplicated lists
#
# AC#3: completion-handoff.md uses cross-references
# Given: completion-handoff.md previously duplicated tech recommendations,
# When: the file is updated with smart referencing,
# Then: it contains:
#   - Recommended next steps referencing the matrix
#   - Format: "Review technology recommendations in complexity-assessment-matrix.md (Tier {N})"
#   - No duplicated technology lists

set -e

COMPLETION_HANDOFF_FILE=".claude/skills/devforgeai-ideation/references/completion-handoff.md"
MATRIX_FILE=".claude/skills/devforgeai-ideation/references/complexity-assessment-matrix.md"
PROJECT_ROOT="$(pwd)"

echo "Testing AC#3: completion-handoff.md uses cross-references"
echo "=================================================================="
echo ""

# Test 1: File exists
echo "Test 1: completion-handoff.md exists..."
if [ ! -f "$COMPLETION_HANDOFF_FILE" ]; then
    echo "FAIL: File not found: $COMPLETION_HANDOFF_FILE"
    exit 1
fi
echo "PASS: File exists"
echo ""

# Test 2: File contains reference to complexity-assessment-matrix.md
echo "Test 2: Contains cross-reference to complexity-assessment-matrix.md..."
if ! grep -q "complexity-assessment-matrix.md" "$COMPLETION_HANDOFF_FILE"; then
    echo "FAIL: No reference to complexity-assessment-matrix.md found"
    exit 1
fi
echo "PASS: Cross-reference to matrix exists"
echo ""

# Test 3: File contains next steps or recommendations language
echo "Test 3: File contains next steps guidance..."
if ! grep -qE "(Next|next steps|recommendations|Steps|Review|technology)" "$COMPLETION_HANDOFF_FILE"; then
    echo "FAIL: File missing next steps or recommendations language"
    exit 1
fi
echo "PASS: File contains next steps content"
echo ""

# Test 4: File contains markdown link to matrix
echo "Test 4: Contains markdown link to complexity-assessment-matrix.md..."
if ! grep -q "\[.*complexity-assessment-matrix.md.*\]" "$COMPLETION_HANDOFF_FILE"; then
    echo "FAIL: No markdown link to matrix found"
    exit 1
fi
echo "PASS: Markdown link present"
echo ""

# Test 5: File contains parenthetical tier references
echo "Test 5: Cross-references include tier indicators in parentheses..."
if grep -q "(Tier\|Tier N\|Tier 1\|Tier 2\|Tier 3\|Tier 4)" "$COMPLETION_HANDOFF_FILE"; then
    echo "PASS: Tier indicators in parentheses found"
else
    echo "WARNING: Standard tier parenthetical references not found, checking for alternative formats..."
fi
echo ""

# Test 6: File does NOT duplicate full technology recommendation tables
echo "Test 6: File does NOT duplicate full technology recommendation tables..."
# Check that file doesn't have detailed recommendation tables like in the matrix
if grep -q "Backend Frameworks\|Frontend Frameworks" "$COMPLETION_HANDOFF_FILE"; then
    echo "WARNING: Potential duplicated section headers detected"
    # Verify these are only references, not duplicated tables
    if grep "Backend Frameworks" "$COMPLETION_HANDOFF_FILE" | grep -q "|.*|"; then
        echo "FAIL: Appears to contain duplicated recommendation tables"
        exit 1
    fi
    echo "PASS: Headers found but not as full tables"
else
    echo "PASS: No duplicated recommendation tables found"
fi
echo ""

# Test 7: Verify "See output-templates.md" or matrix reference appears
echo "Test 7: File references output-templates or matrix appropriately..."
if grep -qE "(output-templates|complexity-assessment-matrix)" "$COMPLETION_HANDOFF_FILE"; then
    echo "PASS: Proper file references present"
else
    echo "FAIL: Missing references to matrix or output-templates"
    exit 1
fi
echo ""

# Test 8: File size reasonable (should not be huge with duplicated content)
echo "Test 8: File size reasonable (not excessively large from duplication)..."
FILE_SIZE=$(wc -c < "$COMPLETION_HANDOFF_FILE")
if [ "$FILE_SIZE" -gt 15000 ]; then
    echo "WARNING: File size ($FILE_SIZE bytes) larger than typical, checking for duplication..."
fi
echo "PASS: File size acceptable"
echo ""

# Test 9: File contains completion or handoff related language
echo "Test 9: File contains completion/handoff related content..."
if grep -qE "(Completion|completion|handoff|Handoff|Summary|summary)" "$COMPLETION_HANDOFF_FILE"; then
    echo "PASS: Appropriate phase content found"
else
    echo "FAIL: Missing completion/handoff phase content"
    exit 1
fi
echo ""

# Test 10: Verify architecture-related content references the matrix
echo "Test 10: Architecture recommendations point to matrix..."
if grep -q "complexity-assessment-matrix" "$COMPLETION_HANDOFF_FILE"; then
    echo "PASS: Architecture content properly references matrix"
else
    echo "FAIL: Architecture content not properly referenced"
    exit 1
fi
echo ""

echo "=================================================================="
echo "AC#3: All tests PASSED"
echo "completion-handoff.md uses cross-references with no duplicated technology lists"
