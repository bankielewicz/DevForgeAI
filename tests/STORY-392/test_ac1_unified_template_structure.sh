#!/usr/bin/env bash
# =============================================================================
# STORY-392 AC#1: AC-Compliance-Verifier Updated to Unified Template Structure
#
# Verifies the updated src/claude/agents/ac-compliance-verifier.md contains
# all 10 required canonical template sections, Validator category optional
# sections, version field updated, and file between 100-500 lines.
#
# TDD Phase: RED (these tests must FAIL before implementation)
# =============================================================================

set -euo pipefail

PROJECT_ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
AGENT_FILE="${PROJECT_ROOT}/src/claude/agents/ac-compliance-verifier.md"

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
echo "STORY-392 AC#1: Unified Template Structure Tests"
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

# Extract frontmatter content between the two --- delimiters
FRONTMATTER_BLOCK=$(awk 'BEGIN{n=0} /^---$/{n++; next} n==1{print}' "$AGENT_FILE")

HAS_NAME=$(echo "$FRONTMATTER_BLOCK" | grep -c '^name:' || true)
run_test "Frontmatter contains 'name' field" "$( [ "$HAS_NAME" -ge 1 ] && echo 0 || echo 1 )"

HAS_DESCRIPTION=$(echo "$FRONTMATTER_BLOCK" | grep -c '^description:' || true)
run_test "Frontmatter contains 'description' field" "$( [ "$HAS_DESCRIPTION" -ge 1 ] && echo 0 || echo 1 )"

HAS_TOOLS=$(echo "$FRONTMATTER_BLOCK" | grep -c '^tools:' || true)
run_test "Frontmatter contains 'tools' field" "$( [ "$HAS_TOOLS" -ge 1 ] && echo 0 || echo 1 )"

HAS_MODEL=$(echo "$FRONTMATTER_BLOCK" | grep -c '^model:' || true)
run_test "Frontmatter contains 'model' field" "$( [ "$HAS_MODEL" -ge 1 ] && echo 0 || echo 1 )"

# Check for version field in frontmatter
HAS_VERSION=$(echo "$FRONTMATTER_BLOCK" | grep -c '^version:' || true)
run_test "Frontmatter contains 'version' field" "$( [ "$HAS_VERSION" -ge 1 ] && echo 0 || echo 1 )"

# =============================================================================
# Test 2: Title H1 exists
# =============================================================================
echo ""
echo "--- Section 2: Title H1 ---"

HAS_H1=$(grep -c '^# ' "$AGENT_FILE" || true)
run_test "File contains at least one H1 heading" "$( [ "$HAS_H1" -ge 1 ] && echo 0 || echo 1 )"

# =============================================================================
# Test 3: Purpose section with identity and fresh-context technique
# =============================================================================
echo ""
echo "--- Section 3: Purpose ---"

HAS_PURPOSE=$(grep -c '^## Purpose' "$AGENT_FILE" || true)
run_test "Section '## Purpose' exists" "$( [ "$HAS_PURPOSE" -ge 1 ] && echo 0 || echo 1 )"

# Purpose must contain identity statement ("You are")
PURPOSE_CONTENT=$(sed -n '/^## Purpose/,/^## [A-Z]/p' "$AGENT_FILE" | head -n -1)

HAS_IDENTITY=$(echo "$PURPOSE_CONTENT" | grep -c 'You are' || true)
run_test "Purpose contains 'You are' identity statement" "$( [ "$HAS_IDENTITY" -ge 1 ] && echo 0 || echo 1 )"

# Purpose must mention fresh-context technique
HAS_FRESH_CONTEXT=$(echo "$PURPOSE_CONTENT" | grep -ci 'fresh.context' || true)
run_test "Purpose mentions fresh-context technique" "$( [ "$HAS_FRESH_CONTEXT" -ge 1 ] && echo 0 || echo 1 )"

# =============================================================================
# Test 4: When Invoked section with Phase 4.5/5.5 triggers
# =============================================================================
echo ""
echo "--- Section 4: When Invoked ---"

HAS_WHEN_INVOKED=$(grep -c '^## When Invoked' "$AGENT_FILE" || true)
run_test "Section '## When Invoked' exists" "$( [ "$HAS_WHEN_INVOKED" -ge 1 ] && echo 0 || echo 1 )"

# Must mention Phase 4.5
HAS_PHASE_45=$(grep -c 'Phase 4\.5\|Phase 4.5' "$AGENT_FILE" || true)
run_test "When Invoked references Phase 4.5" "$( [ "$HAS_PHASE_45" -ge 1 ] && echo 0 || echo 1 )"

# Must mention Phase 5.5
HAS_PHASE_55=$(grep -c 'Phase 5\.5\|Phase 5.5' "$AGENT_FILE" || true)
run_test "When Invoked references Phase 5.5" "$( [ "$HAS_PHASE_55" -ge 1 ] && echo 0 || echo 1 )"

# Must have proactive/automatic triggers
HAS_PROACTIVE=$(grep -ci 'Proactive\|Automatic' "$AGENT_FILE" || true)
run_test "When Invoked contains Proactive/Automatic triggers" "$( [ "$HAS_PROACTIVE" -ge 1 ] && echo 0 || echo 1 )"

# Must have explicit invocation
HAS_EXPLICIT=$(grep -ci 'Explicit invocation\|Explicit' "$AGENT_FILE" || true)
run_test "When Invoked contains Explicit invocation subsection" "$( [ "$HAS_EXPLICIT" -ge 1 ] && echo 0 || echo 1 )"

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
# Test 6: Constraints and Boundaries section with READ-ONLY enforcement
# =============================================================================
echo ""
echo "--- Section 6: Constraints and Boundaries ---"

HAS_CONSTRAINTS=$(grep -c '^## Constraints and Boundaries' "$AGENT_FILE" || true)
run_test "Section '## Constraints and Boundaries' exists" "$( [ "$HAS_CONSTRAINTS" -ge 1 ] && echo 0 || echo 1 )"

# Must enforce READ-ONLY within Constraints
CONSTRAINTS_CONTENT=$(sed -n '/^## Constraints and Boundaries/,/^## [A-Z]/p' "$AGENT_FILE" | head -n -1)

HAS_READONLY=$(echo "$CONSTRAINTS_CONTENT" | grep -ci 'READ.ONLY' || true)
run_test "Constraints section states READ-ONLY enforcement" "$( [ "$HAS_READONLY" -ge 1 ] && echo 0 || echo 1 )"

# =============================================================================
# Test 7: Workflow section with numbered steps
# =============================================================================
echo ""
echo "--- Section 7: Workflow ---"

HAS_WORKFLOW=$(grep -c '^## Workflow' "$AGENT_FILE" || true)
run_test "Section '## Workflow' exists" "$( [ "$HAS_WORKFLOW" -ge 1 ] && echo 0 || echo 1 )"

# Verify numbered steps (at least 3 required by template)
WORKFLOW_CONTENT=$(sed -n '/^## Workflow/,/^## [A-Z]/p' "$AGENT_FILE" | head -n -1)
NUMBERED_STEPS=$(echo "$WORKFLOW_CONTENT" | grep -cE '^\s*[0-9]+\.\s+\*\*|^### Step [0-9]' || true)
run_test "Workflow has at least 3 numbered steps (found: ${NUMBERED_STEPS})" "$( [ "$NUMBERED_STEPS" -ge 3 ] && echo 0 || echo 1 )"

# =============================================================================
# Test 8: Success Criteria section with checklist
# =============================================================================
echo ""
echo "--- Section 8: Success Criteria ---"

HAS_SUCCESS=$(grep -c '^## Success Criteria' "$AGENT_FILE" || true)
run_test "Section '## Success Criteria' exists" "$( [ "$HAS_SUCCESS" -ge 1 ] && echo 0 || echo 1 )"

CHECKLIST_ITEMS=$(grep -cE '^\s*- \[ \]' "$AGENT_FILE" || true)
run_test "Success Criteria has at least 4 checklist items (found: ${CHECKLIST_ITEMS})" "$( [ "$CHECKLIST_ITEMS" -ge 4 ] && echo 0 || echo 1 )"

# =============================================================================
# Test 9: Output Format section with JSON schema
# =============================================================================
echo ""
echo "--- Section 9: Output Format ---"

HAS_OUTPUT_FORMAT=$(grep -c '^## Output Format' "$AGENT_FILE" || true)
run_test "Section '## Output Format' exists" "$( [ "$HAS_OUTPUT_FORMAT" -ge 1 ] && echo 0 || echo 1 )"

# Output Format must contain JSON schema/template
OUTPUT_FORMAT_CONTENT=$(sed -n '/^## Output Format/,/^## [A-Z]/p' "$AGENT_FILE" | head -n -1)
HAS_JSON_SCHEMA=$(echo "$OUTPUT_FORMAT_CONTENT" | grep -c '```json\|"story_id"\|"results"\|"observations_for_persistence"' || true)
run_test "Output Format contains JSON schema/template (found: ${HAS_JSON_SCHEMA})" "$( [ "$HAS_JSON_SCHEMA" -ge 1 ] && echo 0 || echo 1 )"

# =============================================================================
# Test 10: Examples section with Task() pattern
# =============================================================================
echo ""
echo "--- Section 10: Examples ---"

HAS_EXAMPLES=$(grep -c '^## Examples' "$AGENT_FILE" || true)
run_test "Section '## Examples' exists" "$( [ "$HAS_EXAMPLES" -ge 1 ] && echo 0 || echo 1 )"

HAS_TASK_PATTERN=$(grep -c 'Task(' "$AGENT_FILE" || true)
run_test "At least one Task() invocation example present (found: ${HAS_TASK_PATTERN})" "$( [ "$HAS_TASK_PATTERN" -ge 1 ] && echo 0 || echo 1 )"

# =============================================================================
# Test 11: Validator category optional sections
# =============================================================================
echo ""
echo "--- Validator Category Optional Sections ---"

# ac-compliance-verifier is a Validator agent per canonical template
# Validator optional sections: Scoring Methodology, Verification Rules, Evidence Requirements
HAS_VALIDATOR_SECTIONS=$(grep -ciE 'Scoring|Verification Rules|Evidence|Validation Rules|Verification Methodology' "$AGENT_FILE" || true)
run_test "At least one Validator category optional section present (found: ${HAS_VALIDATOR_SECTIONS})" "$( [ "$HAS_VALIDATOR_SECTIONS" -ge 1 ] && echo 0 || echo 1 )"

# =============================================================================
# Test 12: Version field updated (not 2.1 or original version)
# =============================================================================
echo ""
echo "--- Version Field ---"

# The current file has "Version: 2.1" at the bottom. After template migration,
# the version should be in YAML frontmatter and updated (e.g., 3.0.0 or similar)
HAS_VERSION_UPDATED=$(grep -cE '^version:\s*"?[3-9]\.' "$AGENT_FILE" || true)
run_test "Version field updated in frontmatter (>= 3.0)" "$( [ "$HAS_VERSION_UPDATED" -ge 1 ] && echo 0 || echo 1 )"

# =============================================================================
# Test 13: Line count between 100 and 500
# =============================================================================
echo ""
echo "--- File Size ---"

LINE_COUNT=$(wc -l < "$AGENT_FILE")
run_test "File has at least 100 lines (actual: ${LINE_COUNT})" "$( [ "$LINE_COUNT" -ge 100 ] && echo 0 || echo 1 )"
run_test "File has at most 500 lines (actual: ${LINE_COUNT})" "$( [ "$LINE_COUNT" -le 500 ] && echo 0 || echo 1 )"

# =============================================================================
# Test 14: Count of all 8 required H2 section headings
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
# Count the 8 H2 sections above (YAML Frontmatter + Title = 2 structural = 10 total)
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
