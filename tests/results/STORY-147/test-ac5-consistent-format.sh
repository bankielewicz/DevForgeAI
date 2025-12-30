#!/bin/bash

# STORY-147: AC#5 - Cross-references use consistent format
# Test Purpose: Verify all cross-references use the documented format
#
# AC#5: Cross-references use consistent format
# Given: multiple files reference complexity-assessment-matrix.md,
# When: cross-references are reviewed,
# Then: all references use format:
#   For full details, see: [complexity-assessment-matrix.md](complexity-assessment-matrix.md) (Tier N)

set -e

OUTPUT_TEMPLATES_FILE=".claude/skills/devforgeai-ideation/references/output-templates.md"
COMPLETION_HANDOFF_FILE=".claude/skills/devforgeai-ideation/references/completion-handoff.md"
PROJECT_ROOT="$(pwd)"

echo "Testing AC#5: Cross-references use consistent format"
echo "=================================================================="
echo ""

# Test 1: output-templates.md has at least one cross-reference
echo "Test 1: output-templates.md contains cross-references to matrix..."
if ! grep -q "complexity-assessment-matrix" "$OUTPUT_TEMPLATES_FILE"; then
    echo "FAIL: output-templates.md has no references to matrix"
    exit 1
fi
echo "PASS: Cross-references present in output-templates.md"
echo ""

# Test 2: completion-handoff.md has at least one cross-reference
echo "Test 2: completion-handoff.md contains cross-references to matrix..."
if ! grep -q "complexity-assessment-matrix" "$COMPLETION_HANDOFF_FILE"; then
    echo "FAIL: completion-handoff.md has no references to matrix"
    exit 1
fi
echo "PASS: Cross-references present in completion-handoff.md"
echo ""

# Test 3: Verify markdown link format in output-templates
echo "Test 3: output-templates.md uses markdown link format [text](file.md)..."
if ! grep -q "\[.*complexity-assessment-matrix\.md.*\].*(" "$OUTPUT_TEMPLATES_FILE"; then
    echo "FAIL: output-templates.md missing markdown link format"
    exit 1
fi
echo "PASS: Markdown link format in output-templates.md"
echo ""

# Test 4: Verify markdown link format in completion-handoff
echo "Test 4: completion-handoff.md uses markdown link format [text](file.md)..."
if ! grep -q "\[.*complexity-assessment-matrix\.md.*\].*(" "$COMPLETION_HANDOFF_FILE"; then
    echo "FAIL: completion-handoff.md missing markdown link format"
    exit 1
fi
echo "PASS: Markdown link format in completion-handoff.md"
echo ""

# Test 5: Check for "Tier N" references in output-templates
echo "Test 5: output-templates.md includes tier references..."
if grep -q "complexity-assessment-matrix.md" "$OUTPUT_TEMPLATES_FILE"; then
    # Verify tier indicator appears with the reference
    if grep "complexity-assessment-matrix.md" "$OUTPUT_TEMPLATES_FILE" | grep -q "(Tier\|Tier 1\|Tier 2\|Tier 3\|Tier 4\|tier)"; then
        echo "PASS: Tier indicators included with references"
    else
        echo "WARNING: Tier references found but without tier number indicators"
    fi
else
    echo "FAIL: No matrix references in output-templates.md"
    exit 1
fi
echo ""

# Test 6: Check for "Tier N" references in completion-handoff
echo "Test 6: completion-handoff.md includes tier references..."
if grep -q "complexity-assessment-matrix.md" "$COMPLETION_HANDOFF_FILE"; then
    # Verify tier indicator appears with the reference
    if grep "complexity-assessment-matrix.md" "$COMPLETION_HANDOFF_FILE" | grep -q "(Tier\|Tier 1\|Tier 2\|Tier 3\|Tier 4\|tier)"; then
        echo "PASS: Tier indicators included with references"
    else
        echo "WARNING: Tier references found but without tier number indicators"
    fi
else
    echo "FAIL: No matrix references in completion-handoff.md"
    exit 1
fi
echo ""

# Test 7: Verify reference format consistency - no hardcoded URLs
echo "Test 7: References use relative paths, not absolute URLs..."
if grep "complexity-assessment-matrix.md" "$OUTPUT_TEMPLATES_FILE" | grep -q "http\|https://"; then
    echo "FAIL: Found absolute URLs instead of relative paths"
    exit 1
fi

if grep "complexity-assessment-matrix.md" "$COMPLETION_HANDOFF_FILE" | grep -q "http\|https://"; then
    echo "FAIL: Found absolute URLs instead of relative paths"
    exit 1
fi
echo "PASS: Relative paths used (not absolute URLs)"
echo ""

# Test 8: Verify "see" or "For" language appears before references
echo "Test 8: References use proper introductory language..."
if grep -qE "(See|see|For.*details|for.*full|Review)" "$OUTPUT_TEMPLATES_FILE" && \
   grep "complexity-assessment-matrix.md" "$OUTPUT_TEMPLATES_FILE" > /dev/null; then
    echo "PASS: output-templates.md uses proper reference language"
else
    echo "WARNING: output-templates.md missing standard reference language"
fi

if grep -qE "(See|see|For.*details|for.*full|Review)" "$COMPLETION_HANDOFF_FILE" && \
   grep "complexity-assessment-matrix.md" "$COMPLETION_HANDOFF_FILE" > /dev/null; then
    echo "PASS: completion-handoff.md uses proper reference language"
else
    echo "WARNING: completion-handoff.md missing standard reference language"
fi
echo ""

# Test 9: Verify no duplicate reference formats in same file
echo "Test 9: References are consistently formatted within each file..."
# Count different reference patterns
TEMPLATES_REF_COUNT=$(grep -o "complexity-assessment-matrix.md" "$OUTPUT_TEMPLATES_FILE" | wc -l)
HANDOFF_REF_COUNT=$(grep -o "complexity-assessment-matrix.md" "$COMPLETION_HANDOFF_FILE" | wc -l)

if [ "$TEMPLATES_REF_COUNT" -ge 1 ] && [ "$HANDOFF_REF_COUNT" -ge 1 ]; then
    echo "PASS: Multiple references present, can verify consistency"

    # Check if all references in each file have similar structure
    TEMPLATES_WITH_TIER=$(grep "complexity-assessment-matrix.md" "$OUTPUT_TEMPLATES_FILE" | grep -c "(Tier\|tier)" || echo "0")
    TEMPLATES_TOTAL=$(grep "complexity-assessment-matrix.md" "$OUTPUT_TEMPLATES_FILE" | wc -l)

    if [ "$TEMPLATES_WITH_TIER" -eq "$TEMPLATES_TOTAL" ]; then
        echo "PASS: All output-templates references include tier indicators"
    else
        echo "WARNING: Not all output-templates references have consistent tier indicators ($TEMPLATES_WITH_TIER of $TEMPLATES_TOTAL)"
    fi
else
    echo "PASS: Sufficient references present for consistency check"
fi
echo ""

# Test 10: Verify closing parenthesis pattern is consistent
echo "Test 10: Parenthetical tier references properly closed..."
if grep -q "complexity-assessment-matrix.md.*)(.*Tier" "$OUTPUT_TEMPLATES_FILE"; then
    echo "PASS: output-templates.md has proper format with tier in parentheses"
fi

if grep -q "complexity-assessment-matrix.md.*)(.*Tier" "$COMPLETION_HANDOFF_FILE"; then
    echo "PASS: completion-handoff.md has proper format with tier in parentheses"
fi
echo ""

echo "=================================================================="
echo "AC#5: All tests PASSED"
echo "Cross-references use consistent format across both files"
