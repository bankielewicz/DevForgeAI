#!/usr/bin/env bash
# =============================================================================
# STORY-392 AC#2: Anthropic Prompt Engineering Patterns Applied
#
# Verifies the updated src/claude/agents/ac-compliance-verifier.md contains:
# 1. Chain-of-thought reasoning (e.g., "Think step-by-step")
# 2. Structured JSON output specification
# 3. At least one worked example showing complete AC verification flow
# 4. Role-based identity statement ("You are...")
# 5. Clear constraint boundaries including READ-ONLY
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
    local test_result="$2"

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
echo "STORY-392 AC#2: Anthropic Prompt Engineering Patterns Tests"
echo "Target: ${AGENT_FILE}"
echo "================================================================"
echo ""

# --- Pre-check: File exists ---
if [ ! -f "$AGENT_FILE" ]; then
    echo "FATAL: Agent file not found at ${AGENT_FILE}"
    exit 1
fi

# =============================================================================
# Pattern 1: Chain-of-thought reasoning in Workflow section
# =============================================================================
echo "--- Pattern 1: Chain-of-thought reasoning ---"

# Must contain explicit chain-of-thought directive
# AC says: e.g., "Think step-by-step: first parse XML ACs, then discover source files..."
HAS_STEP_BY_STEP=$(grep -ci 'step-by-step\|step by step\|Think.*step' "$AGENT_FILE" || true)
run_test "Chain-of-thought: 'step-by-step' reasoning directive (found: ${HAS_STEP_BY_STEP})" "$( [ "$HAS_STEP_BY_STEP" -ge 1 ] && echo 0 || echo 1 )"

# Must contain multi-step verification reasoning
# AC says: "first parse XML ACs, then discover source files, then verify"
HAS_COT_SEQUENCE=$(grep -ci 'first.*then\|parse.*then.*verify\|step 1.*step 2' "$AGENT_FILE" || true)
run_test "Chain-of-thought: sequential reasoning (first...then) (found: ${HAS_COT_SEQUENCE})" "$( [ "$HAS_COT_SEQUENCE" -ge 1 ] && echo 0 || echo 1 )"

# Extract Workflow section for focused checks
WORKFLOW_CONTENT=$(sed -n '/^## Workflow/,/^## [A-Z]/p' "$AGENT_FILE" | head -n -1)

COT_IN_WORKFLOW=$(echo "$WORKFLOW_CONTENT" | grep -ciE 'reason|think|analyze|determine|consider|evaluate' || true)
run_test "Chain-of-thought phrases within Workflow section (found: ${COT_IN_WORKFLOW})" "$( [ "$COT_IN_WORKFLOW" -ge 2 ] && echo 0 || echo 1 )"

# Workflow must have numbered reasoning steps
COT_STEPS=$(echo "$WORKFLOW_CONTENT" | grep -cE '^\s*[0-9]+\.' || true)
run_test "Chain-of-thought: at least 3 numbered reasoning steps (found: ${COT_STEPS})" "$( [ "$COT_STEPS" -ge 3 ] && echo 0 || echo 1 )"

# =============================================================================
# Pattern 2: Structured JSON output specification
# =============================================================================
echo ""
echo "--- Pattern 2: Structured JSON output specification ---"

# Output Format section must exist
HAS_OUTPUT_FORMAT=$(grep -c '^## Output Format' "$AGENT_FILE" || true)
run_test "Output Format section exists" "$( [ "$HAS_OUTPUT_FORMAT" -ge 1 ] && echo 0 || echo 1 )"

# Extract Output Format content
OUTPUT_FORMAT_CONTENT=$(sed -n '/^## Output Format/,/^## [A-Z]/p' "$AGENT_FILE" | head -n -1)

# Must contain JSON code block
HAS_JSON_BLOCK=$(echo "$OUTPUT_FORMAT_CONTENT" | grep -c '```json' || true)
run_test "Output Format contains JSON code block (found: ${HAS_JSON_BLOCK})" "$( [ "$HAS_JSON_BLOCK" -ge 1 ] && echo 0 || echo 1 )"

# JSON schema must define verification report structure
HAS_VERIFICATION_FIELDS=$(echo "$OUTPUT_FORMAT_CONTENT" | grep -ciE '"story_id"|"results"|"overall_status"|"details"|"observations_for_persistence"' || true)
run_test "JSON schema defines verification report fields (found: ${HAS_VERIFICATION_FIELDS})" "$( [ "$HAS_VERIFICATION_FIELDS" -ge 3 ] && echo 0 || echo 1 )"

# Must specify per-AC PASS/FAIL in schema
HAS_PER_AC_STATUS=$(echo "$OUTPUT_FORMAT_CONTENT" | grep -ciE '"PASS"|"FAIL"|"BLOCKED"|per.AC|ac_id|status.*PASS' || true)
run_test "JSON schema specifies per-AC PASS/FAIL status (found: ${HAS_PER_AC_STATUS})" "$( [ "$HAS_PER_AC_STATUS" -ge 1 ] && echo 0 || echo 1 )"

# =============================================================================
# Pattern 3: At least one worked example showing complete AC verification flow
# =============================================================================
echo ""
echo "--- Pattern 3: Worked example(s) ---"

# Examples section must exist
HAS_EXAMPLES=$(grep -c '^## Examples' "$AGENT_FILE" || true)
run_test "Examples section exists" "$( [ "$HAS_EXAMPLES" -ge 1 ] && echo 0 || echo 1 )"

# Extract Examples section content
EXAMPLES_CONTENT=$(sed -n '/^## Examples/,/^## [A-Z]/p' "$AGENT_FILE" | head -n -1)

# At least one worked example (sub-heading with "Example")
EXAMPLE_COUNT=$(echo "$EXAMPLES_CONTENT" | grep -cE '^### Example|^### .*[Ee]xample' || true)
run_test "At least one worked example present (found: ${EXAMPLE_COUNT})" "$( [ "$EXAMPLE_COUNT" -ge 1 ] && echo 0 || echo 1 )"

# Example must contain Task() invocation pattern
TASK_IN_EXAMPLES=$(echo "$EXAMPLES_CONTENT" | grep -c 'Task(' || true)
run_test "Example contains Task() invocation pattern (found: ${TASK_IN_EXAMPLES})" "$( [ "$TASK_IN_EXAMPLES" -ge 1 ] && echo 0 || echo 1 )"

# Example must show AC verification flow (mention of story, AC, verify, result)
VERIFICATION_FLOW=$(echo "$EXAMPLES_CONTENT" | grep -ciE 'story|AC|verify|verification|PASS|FAIL|result' || true)
run_test "Example shows AC verification flow elements (found: ${VERIFICATION_FLOW})" "$( [ "$VERIFICATION_FLOW" -ge 3 ] && echo 0 || echo 1 )"

# =============================================================================
# Pattern 4: Role-based identity statement
# =============================================================================
echo ""
echo "--- Pattern 4: Role-based identity statement ---"

# Extract Purpose section
PURPOSE_CONTENT=$(sed -n '/^## Purpose/,/^## [A-Z]/p' "$AGENT_FILE" | head -n -1)

# Must contain "You are" identity statement
HAS_YOU_ARE=$(echo "$PURPOSE_CONTENT" | grep -c 'You are' || true)
run_test "Purpose contains 'You are' identity anchoring (found: ${HAS_YOU_ARE})" "$( [ "$HAS_YOU_ARE" -ge 1 ] && echo 0 || echo 1 )"

# Must describe specialization (verification, compliance, validation)
HAS_SPECIALIZATION=$(echo "$PURPOSE_CONTENT" | grep -ciE 'verification|compliance|validation|verif|specializ|expert' || true)
run_test "Purpose describes verification specialization (found: ${HAS_SPECIALIZATION})" "$( [ "$HAS_SPECIALIZATION" -ge 1 ] && echo 0 || echo 1 )"

# =============================================================================
# Pattern 5: Clear constraint boundaries including READ-ONLY
# =============================================================================
echo ""
echo "--- Pattern 5: Clear constraint boundaries with READ-ONLY ---"

# Constraints and Boundaries section must exist
HAS_CONSTRAINTS=$(grep -c '^## Constraints and Boundaries' "$AGENT_FILE" || true)
run_test "Constraints and Boundaries section exists" "$( [ "$HAS_CONSTRAINTS" -ge 1 ] && echo 0 || echo 1 )"

# Extract Constraints section
CONSTRAINTS_CONTENT=$(sed -n '/^## Constraints and Boundaries/,/^## [A-Z]/p' "$AGENT_FILE" | head -n -1)

# Must state READ-ONLY constraint
HAS_READONLY=$(echo "$CONSTRAINTS_CONTENT" | grep -ci 'READ.ONLY' || true)
run_test "Constraints state READ-ONLY limitation (found: ${HAS_READONLY})" "$( [ "$HAS_READONLY" -ge 1 ] && echo 0 || echo 1 )"

# Must contain DO NOT / NEVER / MUST NOT prohibitions
HAS_PROHIBITIONS=$(echo "$CONSTRAINTS_CONTENT" | grep -cE 'DO NOT|NEVER|MUST NOT' || true)
run_test "Constraints contain prohibitions (DO NOT/NEVER/MUST NOT) (found: ${HAS_PROHIBITIONS})" "$( [ "$HAS_PROHIBITIONS" -ge 1 ] && echo 0 || echo 1 )"

# Must have at least 3 constraint statements
CONSTRAINT_BULLETS=$(echo "$CONSTRAINTS_CONTENT" | grep -cE '^\s*-\s+' || true)
run_test "Constraints contain at least 3 constraint statements (found: ${CONSTRAINT_BULLETS})" "$( [ "$CONSTRAINT_BULLETS" -ge 3 ] && echo 0 || echo 1 )"

# =============================================================================
# Pattern Traceability
# =============================================================================
echo ""
echo "--- Pattern Traceability ---"

# Chain-of-thought must be in Workflow (not just anywhere)
COT_IN_WORKFLOW_SECTION=$(echo "$WORKFLOW_CONTENT" | grep -ci 'step-by-step\|step by step\|Think.*step' || true)
run_test "Chain-of-thought is within Workflow section" "$( [ "$COT_IN_WORKFLOW_SECTION" -ge 1 ] && echo 0 || echo 1 )"

# Identity anchoring must be in Purpose (not just anywhere)
IDENTITY_IN_PURPOSE=$(echo "$PURPOSE_CONTENT" | grep -c 'You are' || true)
run_test "Identity anchoring is within Purpose section" "$( [ "$IDENTITY_IN_PURPOSE" -ge 1 ] && echo 0 || echo 1 )"

# No pattern conflicts with existing reference file content
# Verify the agent does not redefine reference content inline
# (reference content should be loaded on-demand, not duplicated)
HAS_NO_INLINE_SCORING=$(grep -c '^## Scoring Methodology' "$AGENT_FILE" || true)
HAS_NO_INLINE_REPORT_GEN=$(grep -c '^## Report Generation' "$AGENT_FILE" || true)
# These should NOT appear as top-level H2 sections (they belong in references)
INLINE_CONFLICT=$((HAS_NO_INLINE_SCORING + HAS_NO_INLINE_REPORT_GEN))
run_test "No inline conflict with reference file content (found: ${INLINE_CONFLICT}, want 0)" "$( [ "$INLINE_CONFLICT" -eq 0 ] && echo 0 || echo 1 )"

# =============================================================================
# Summary
# =============================================================================
echo ""
echo "================================================================"
echo "AC#2 Results: ${PASS_COUNT} passed, ${FAIL_COUNT} failed out of ${TOTAL_TESTS} tests"
echo "================================================================"

if [ "$FAIL_COUNT" -gt 0 ]; then
    exit 1
else
    exit 0
fi
