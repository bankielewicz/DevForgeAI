#!/usr/bin/env bash
# =============================================================================
# STORY-391 AC#1: Test-automator System Prompt Updated to Unified Template Structure
#
# Verifies the updated src/claude/agents/test-automator.md contains all 10
# required canonical template sections, Implementor category optional sections,
# version field set to 2.0.0, and file is between 100-500 lines.
#
# TDD Phase: RED (these tests must FAIL before implementation)
# =============================================================================

set -euo pipefail

PROJECT_ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
AGENT_FILE="${PROJECT_ROOT}/src/claude/agents/test-automator.md"

PASS_COUNT=0
FAIL_COUNT=0
TOTAL_TESTS=0

# --- Test Helper ---
run_test() {
    local test_name="$1"
    local test_result="$2"  # 0 = pass, non-zero = fail

    TOTAL_TESTS=$((TOTAL_TESTS + 1))
    if [ "$test_result" -eq 0 ]; then
        PASS_COUNT=$((PASS_COUNT + 1))
        echo "  PASS: ${test_name}"
    else
        FAIL_COUNT=$((FAIL_COUNT + 1))
        echo "  FAIL: ${test_name}"
    fi
}

echo "================================================================"
echo "STORY-391 AC#1: Unified Template Structure Tests"
echo "Target: ${AGENT_FILE}"
echo "================================================================"
echo ""

# --- Pre-check: File exists ---
if [ ! -f "$AGENT_FILE" ]; then
    echo "FATAL: Agent file not found at ${AGENT_FILE}"
    exit 1
fi

# =============================================================================
# Test 1: YAML Frontmatter section exists with --- delimiters
# =============================================================================
echo "--- Section 1: YAML Frontmatter ---"

# Check frontmatter starts with ---
FRONTMATTER_START=$(head -1 "$AGENT_FILE" | grep -c '^---$' || true)
run_test "Frontmatter opens with --- delimiter" "$( [ "$FRONTMATTER_START" -ge 1 ] && echo 0 || echo 1 )"

# Check frontmatter has closing ---
FRONTMATTER_END=$(sed -n '2,/^---$/p' "$AGENT_FILE" | tail -1 | grep -c '^---$' || true)
run_test "Frontmatter closes with --- delimiter" "$( [ "$FRONTMATTER_END" -ge 1 ] && echo 0 || echo 1 )"

# Check required frontmatter fields: name, description, tools, model
# Extract frontmatter content between the two --- delimiters (lines 2 through closing ---)
FRONTMATTER_BLOCK=$(awk 'BEGIN{n=0} /^---$/{n++; next} n==1{print}' "$AGENT_FILE")

HAS_NAME=$(echo "$FRONTMATTER_BLOCK" | grep -c '^name:' || true)
run_test "Frontmatter contains 'name' field" "$( [ "$HAS_NAME" -ge 1 ] && echo 0 || echo 1 )"

HAS_DESCRIPTION=$(echo "$FRONTMATTER_BLOCK" | grep -c '^description:' || true)
run_test "Frontmatter contains 'description' field" "$( [ "$HAS_DESCRIPTION" -ge 1 ] && echo 0 || echo 1 )"

HAS_TOOLS=$(echo "$FRONTMATTER_BLOCK" | grep -c '^tools:' || true)
run_test "Frontmatter contains 'tools' field" "$( [ "$HAS_TOOLS" -ge 1 ] && echo 0 || echo 1 )"

HAS_MODEL=$(echo "$FRONTMATTER_BLOCK" | grep -c '^model:' || true)
run_test "Frontmatter contains 'model' field" "$( [ "$HAS_MODEL" -ge 1 ] && echo 0 || echo 1 )"

# =============================================================================
# Test 2: Title H1 exists
# =============================================================================
echo ""
echo "--- Section 2: Title H1 ---"

HAS_H1=$(grep -c '^# ' "$AGENT_FILE" || true)
run_test "File contains at least one H1 heading" "$( [ "$HAS_H1" -ge 1 ] && echo 0 || echo 1 )"

# =============================================================================
# Test 3: Purpose section with identity statement ("You are")
# =============================================================================
echo ""
echo "--- Section 3: Purpose ---"

HAS_PURPOSE=$(grep -c '^## Purpose' "$AGENT_FILE" || true)
run_test "Section '## Purpose' exists" "$( [ "$HAS_PURPOSE" -ge 1 ] && echo 0 || echo 1 )"

HAS_IDENTITY=$(grep -ci 'You are' "$AGENT_FILE" || true)
run_test "Identity statement ('You are') present in Purpose" "$( [ "$HAS_IDENTITY" -ge 1 ] && echo 0 || echo 1 )"

# =============================================================================
# Test 4: When Invoked section with triggers
# =============================================================================
echo ""
echo "--- Section 4: When Invoked ---"

HAS_WHEN_INVOKED=$(grep -c '^## When Invoked' "$AGENT_FILE" || true)
run_test "Section '## When Invoked' exists" "$( [ "$HAS_WHEN_INVOKED" -ge 1 ] && echo 0 || echo 1 )"

HAS_PROACTIVE=$(grep -c 'Proactive triggers' "$AGENT_FILE" || true)
run_test "Proactive triggers subsection present" "$( [ "$HAS_PROACTIVE" -ge 1 ] && echo 0 || echo 1 )"

HAS_EXPLICIT=$(grep -c 'Explicit invocation' "$AGENT_FILE" || true)
run_test "Explicit invocation subsection present" "$( [ "$HAS_EXPLICIT" -ge 1 ] && echo 0 || echo 1 )"

HAS_AUTOMATIC=$(grep -c 'Automatic' "$AGENT_FILE" || true)
run_test "Automatic invocation subsection present" "$( [ "$HAS_AUTOMATIC" -ge 1 ] && echo 0 || echo 1 )"

# =============================================================================
# Test 5: Input/Output Specification section
# =============================================================================
echo ""
echo "--- Section 5: Input/Output Specification ---"

HAS_IO_SPEC=$(grep -c '^## Input/Output Specification' "$AGENT_FILE" || true)
run_test "Section '## Input/Output Specification' exists" "$( [ "$HAS_IO_SPEC" -ge 1 ] && echo 0 || echo 1 )"

HAS_INPUT=$(grep -c '### Input' "$AGENT_FILE" || true)
run_test "Input subsection present" "$( [ "$HAS_INPUT" -ge 1 ] && echo 0 || echo 1 )"

HAS_OUTPUT=$(grep -c '### Output' "$AGENT_FILE" || true)
run_test "Output subsection present" "$( [ "$HAS_OUTPUT" -ge 1 ] && echo 0 || echo 1 )"

# =============================================================================
# Test 6: Constraints and Boundaries section
# =============================================================================
echo ""
echo "--- Section 6: Constraints and Boundaries ---"

HAS_CONSTRAINTS=$(grep -c '^## Constraints and Boundaries' "$AGENT_FILE" || true)
run_test "Section '## Constraints and Boundaries' exists" "$( [ "$HAS_CONSTRAINTS" -ge 1 ] && echo 0 || echo 1 )"

# =============================================================================
# Test 7: Workflow section with numbered steps
# =============================================================================
echo ""
echo "--- Section 7: Workflow ---"

HAS_WORKFLOW=$(grep -c '^## Workflow' "$AGENT_FILE" || true)
run_test "Section '## Workflow' exists" "$( [ "$HAS_WORKFLOW" -ge 1 ] && echo 0 || echo 1 )"

# Verify numbered steps (at least 3 required by template)
NUMBERED_STEPS=$(grep -cE '^\s*[0-9]+\.\s+\*\*' "$AGENT_FILE" || true)
run_test "Workflow has at least 3 numbered steps" "$( [ "$NUMBERED_STEPS" -ge 3 ] && echo 0 || echo 1 )"

# =============================================================================
# Test 8: Success Criteria section with checklist
# =============================================================================
echo ""
echo "--- Section 8: Success Criteria ---"

HAS_SUCCESS=$(grep -c '^## Success Criteria' "$AGENT_FILE" || true)
run_test "Section '## Success Criteria' exists" "$( [ "$HAS_SUCCESS" -ge 1 ] && echo 0 || echo 1 )"

CHECKLIST_ITEMS=$(grep -cE '^\s*- \[ \]' "$AGENT_FILE" || true)
run_test "Success Criteria has at least 4 checklist items" "$( [ "$CHECKLIST_ITEMS" -ge 4 ] && echo 0 || echo 1 )"

# =============================================================================
# Test 9: Output Format section with structured format
# =============================================================================
echo ""
echo "--- Section 9: Output Format ---"

HAS_OUTPUT_FORMAT=$(grep -c '^## Output Format' "$AGENT_FILE" || true)
run_test "Section '## Output Format' exists" "$( [ "$HAS_OUTPUT_FORMAT" -ge 1 ] && echo 0 || echo 1 )"

# =============================================================================
# Test 10: Examples section with Task() pattern
# =============================================================================
echo ""
echo "--- Section 10: Examples ---"

HAS_EXAMPLES=$(grep -c '^## Examples' "$AGENT_FILE" || true)
run_test "Section '## Examples' exists" "$( [ "$HAS_EXAMPLES" -ge 1 ] && echo 0 || echo 1 )"

HAS_TASK_PATTERN=$(grep -c 'Task(' "$AGENT_FILE" || true)
run_test "At least one Task() invocation example present" "$( [ "$HAS_TASK_PATTERN" -ge 1 ] && echo 0 || echo 1 )"

# =============================================================================
# Test 11: Version field set to 2.0.0
# =============================================================================
echo ""
echo "--- Version Field ---"

HAS_VERSION_200=$(grep -cE '^version:\s*"?2\.0\.0"?' "$AGENT_FILE" || true)
run_test "Version field set to 2.0.0 in frontmatter" "$( [ "$HAS_VERSION_200" -ge 1 ] && echo 0 || echo 1 )"

# =============================================================================
# Test 12: Implementor category optional sections
# =============================================================================
echo ""
echo "--- Implementor Category Optional Sections ---"

# test-automator is Implementor + Analyzer per canonical template decision table
# Implementor optional: Implementation Patterns, Code Generation Rules, Test Requirements
# At least one Implementor optional section should be present (or repurposed equivalent)
HAS_IMPL_PATTERNS=$(grep -ci 'Implementation Patterns\|Code Generation Rules\|Test Requirements\|Test Generation Rules' "$AGENT_FILE" || true)
run_test "At least one Implementor category optional section present" "$( [ "$HAS_IMPL_PATTERNS" -ge 1 ] && echo 0 || echo 1 )"

# =============================================================================
# Test 13: Line count between 100 and 500
# =============================================================================
echo ""
echo "--- File Size ---"

LINE_COUNT=$(wc -l < "$AGENT_FILE")
run_test "File has at least 100 lines (actual: ${LINE_COUNT})" "$( [ "$LINE_COUNT" -ge 100 ] && echo 0 || echo 1 )"
run_test "File has at most 500 lines (actual: ${LINE_COUNT})" "$( [ "$LINE_COUNT" -le 500 ] && echo 0 || echo 1 )"

# =============================================================================
# Test 14: Count of all 10 required H2 section headings
# =============================================================================
echo ""
echo "--- Required Section Count ---"

SECTION_COUNT=0
for section in "Purpose" "When Invoked" "Input/Output Specification" "Constraints and Boundaries" "Workflow" "Success Criteria" "Output Format" "Examples"; do
    FOUND=$(grep -c "^## ${section}" "$AGENT_FILE" || true)
    if [ "$FOUND" -ge 1 ]; then
        SECTION_COUNT=$((SECTION_COUNT + 1))
    fi
done
# Frontmatter and Title are structural, not H2
# Add 2 for frontmatter (always present) and title (always present)
# But we count the 8 H2 sections above
run_test "All 8 required H2 sections present (found: ${SECTION_COUNT}/8)" "$( [ "$SECTION_COUNT" -ge 8 ] && echo 0 || echo 1 )"

# =============================================================================
# Summary
# =============================================================================
echo ""
echo "================================================================"
echo "AC#1 Results: ${PASS_COUNT} passed, ${FAIL_COUNT} failed out of ${TOTAL_TESTS} tests"
echo "================================================================"

if [ "$FAIL_COUNT" -gt 0 ]; then
    exit 1
else
    exit 0
fi
