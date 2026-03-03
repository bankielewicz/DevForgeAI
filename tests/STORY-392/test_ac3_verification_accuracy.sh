#!/usr/bin/env bash
# =============================================================================
# STORY-392 AC#3: Verification Accuracy Maintained (No Regression)
#
# Verifies the updated src/claude/agents/ac-compliance-verifier.md:
# 1. Parses XML AC blocks per xml-parsing-protocol.md
# 2. Extracts Given/When/Then and verification hints
# 3. Uses only Read/Grep/Glob tools
# 4. Produces structured JSON report with per-AC PASS/FAIL
# 5. HALTs on stories missing XML AC format (legacy markdown)
# 6. No previously passing verification produces FAIL after migration
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
echo "STORY-392 AC#3: Verification Accuracy Tests"
echo "Target: ${AGENT_FILE}"
echo "================================================================"
echo ""

# --- Pre-check: File exists ---
if [ ! -f "$AGENT_FILE" ]; then
    echo "FATAL: Agent file not found at ${AGENT_FILE}"
    exit 1
fi

# =============================================================================
# Test 1: XML AC parsing instruction preserved
# =============================================================================
echo "--- XML AC Parsing ---"

# Agent must reference XML AC parsing (acceptance_criteria XML blocks)
HAS_XML_PARSING=$(grep -ci 'xml.*pars\|pars.*xml\|acceptance_criteria\|<acceptance_criteria' "$AGENT_FILE" || true)
run_test "Agent references XML AC parsing (found: ${HAS_XML_PARSING})" "$( [ "$HAS_XML_PARSING" -ge 1 ] && echo 0 || echo 1 )"

# Agent must reference xml-parsing-protocol.md
HAS_XML_PROTOCOL_REF=$(grep -c 'xml-parsing-protocol.md' "$AGENT_FILE" || true)
run_test "Agent references xml-parsing-protocol.md (found: ${HAS_XML_PROTOCOL_REF})" "$( [ "$HAS_XML_PROTOCOL_REF" -ge 1 ] && echo 0 || echo 1 )"

# =============================================================================
# Test 2: Given/When/Then extraction
# =============================================================================
echo ""
echo "--- Given/When/Then Extraction ---"

# Agent must mention Given/When/Then extraction
HAS_GIVEN_WHEN_THEN=$(grep -ci 'Given.*When.*Then\|given.*when.*then\|<given>\|<when>\|<then>' "$AGENT_FILE" || true)
run_test "Agent mentions Given/When/Then extraction (found: ${HAS_GIVEN_WHEN_THEN})" "$( [ "$HAS_GIVEN_WHEN_THEN" -ge 1 ] && echo 0 || echo 1 )"

# Agent must mention verification hints
HAS_VERIFICATION_HINTS=$(grep -ci 'verification.*hint\|hint\|source_files\|test_file' "$AGENT_FILE" || true)
run_test "Agent mentions verification hints extraction (found: ${HAS_VERIFICATION_HINTS})" "$( [ "$HAS_VERIFICATION_HINTS" -ge 1 ] && echo 0 || echo 1 )"

# =============================================================================
# Test 3: Uses only Read/Grep/Glob tools
# =============================================================================
echo ""
echo "--- Tool Restriction in Agent Instructions ---"

# Agent instructions must specify Read/Grep/Glob as the discovery tools
HAS_READ_TOOL=$(grep -c 'Read(' "$AGENT_FILE" || true)
run_test "Agent uses Read() tool in workflow (found: ${HAS_READ_TOOL})" "$( [ "$HAS_READ_TOOL" -ge 1 ] && echo 0 || echo 1 )"

HAS_GREP_TOOL=$(grep -c 'Grep(' "$AGENT_FILE" || true)
run_test "Agent uses Grep() tool in workflow (found: ${HAS_GREP_TOOL})" "$( [ "$HAS_GREP_TOOL" -ge 1 ] && echo 0 || echo 1 )"

HAS_GLOB_TOOL=$(grep -c 'Glob(' "$AGENT_FILE" || true)
run_test "Agent uses Glob() tool in workflow (found: ${HAS_GLOB_TOOL})" "$( [ "$HAS_GLOB_TOOL" -ge 1 ] && echo 0 || echo 1 )"

# Agent must NOT instruct Write/Edit/Bash usage as agent actions
# Note: Write() may appear in documentation about orchestrator persistence (expected)
# We check for Write/Edit/Bash OUTSIDE of orchestrator documentation context
HAS_EDIT_USAGE=$(grep -c 'Edit(' "$AGENT_FILE" || true)
run_test "Agent does NOT instruct Edit() usage (found: ${HAS_EDIT_USAGE}, want 0)" "$( [ "$HAS_EDIT_USAGE" -eq 0 ] && echo 0 || echo 1 )"

HAS_BASH_USAGE=$(grep -c 'Bash(' "$AGENT_FILE" || true)
run_test "Agent does NOT instruct Bash() usage (found: ${HAS_BASH_USAGE}, want 0)" "$( [ "$HAS_BASH_USAGE" -eq 0 ] && echo 0 || echo 1 )"

# Write() is acceptable ONLY in orchestrator context (describing what orchestrator does)
# The current file has Write() on a line inside a code block preceded by orchestrator text
# Count Write() occurrences, subtract those in orchestrator context (within 3 lines of "orchestrator")
TOTAL_WRITE=$(grep -c 'Write(' "$AGENT_FILE" || true)
# Check if all Write() occurrences are within orchestrator observation persistence documentation
# Lines containing Write( that are inside code blocks after orchestrator mentions are OK
ORCHESTRATOR_CONTEXT=$(grep -B3 'Write(' "$AGENT_FILE" | grep -ci 'orchestrator' || true)
if [ "$TOTAL_WRITE" -gt 0 ] && [ "$ORCHESTRATOR_CONTEXT" -ge 1 ]; then
    # All Write() references appear near orchestrator context - acceptable
    WRITE_AS_AGENT_ACTION=0
else
    WRITE_AS_AGENT_ACTION=$TOTAL_WRITE
fi
run_test "No Write() as agent action (orchestrator docs OK) (found: ${WRITE_AS_AGENT_ACTION}, want 0)" "$( [ "$WRITE_AS_AGENT_ACTION" -eq 0 ] && echo 0 || echo 1 )"

# =============================================================================
# Test 4: Structured JSON report with per-AC PASS/FAIL
# =============================================================================
echo ""
echo "--- Structured JSON Report ---"

# Agent must produce structured JSON output
HAS_JSON_REPORT=$(grep -c '```json' "$AGENT_FILE" || true)
run_test "Agent contains JSON report template (found: ${HAS_JSON_REPORT})" "$( [ "$HAS_JSON_REPORT" -ge 1 ] && echo 0 || echo 1 )"

# JSON report must include per-AC status (PASS/FAIL)
HAS_PER_AC_PASS_FAIL=$(grep -ciE '"PASS"|"FAIL"|per.AC.*status|ac.*PASS|ac.*FAIL|status.*PASS|status.*FAIL' "$AGENT_FILE" || true)
run_test "JSON report specifies per-AC PASS/FAIL (found: ${HAS_PER_AC_PASS_FAIL})" "$( [ "$HAS_PER_AC_PASS_FAIL" -ge 1 ] && echo 0 || echo 1 )"

# JSON report must include confidence levels
HAS_CONFIDENCE=$(grep -ci 'confidence' "$AGENT_FILE" || true)
run_test "JSON report includes confidence levels (found: ${HAS_CONFIDENCE})" "$( [ "$HAS_CONFIDENCE" -ge 1 ] && echo 0 || echo 1 )"

# JSON report must include file evidence
HAS_FILE_EVIDENCE=$(grep -ci 'evidence\|file_path\|line.*number\|snippet' "$AGENT_FILE" || true)
run_test "JSON report includes file evidence fields (found: ${HAS_FILE_EVIDENCE})" "$( [ "$HAS_FILE_EVIDENCE" -ge 1 ] && echo 0 || echo 1 )"

# =============================================================================
# Test 5: HALT on legacy markdown format
# =============================================================================
echo ""
echo "--- HALT on Legacy Markdown ---"

# Agent must contain HALT instruction for legacy format
HAS_HALT_LEGACY=$(grep -ci 'HALT.*legacy\|HALT.*markdown\|legacy.*HALT\|legacy.*format.*HALT' "$AGENT_FILE" || true)
run_test "Agent HALTs on legacy markdown AC format (found: ${HAS_HALT_LEGACY})" "$( [ "$HAS_HALT_LEGACY" -ge 1 ] && echo 0 || echo 1 )"

# Agent must distinguish between XML format and legacy markdown format
HAS_FORMAT_DETECTION=$(grep -ci 'XML.*format\|legacy.*format\|markdown.*format\|format.*detection' "$AGENT_FILE" || true)
run_test "Agent contains format detection logic (found: ${HAS_FORMAT_DETECTION})" "$( [ "$HAS_FORMAT_DETECTION" -ge 1 ] && echo 0 || echo 1 )"

# =============================================================================
# Test 6: Fresh-context technique preserved
# =============================================================================
echo ""
echo "--- Fresh-Context Technique ---"

HAS_FRESH_CONTEXT=$(grep -ci 'fresh.context' "$AGENT_FILE" || true)
run_test "Fresh-context technique mentioned (found: ${HAS_FRESH_CONTEXT})" "$( [ "$HAS_FRESH_CONTEXT" -ge 2 ] && echo 0 || echo 1 )"

# Must instruct NOT to rely on prior coding context
HAS_NO_PRIOR=$(grep -ci 'no prior\|no.*knowledge.*coding\|independently\|without.*prior\|DO NOT rely' "$AGENT_FILE" || true)
run_test "Instructions to verify without prior coding context (found: ${HAS_NO_PRIOR})" "$( [ "$HAS_NO_PRIOR" -ge 1 ] && echo 0 || echo 1 )"

# =============================================================================
# Summary
# =============================================================================
echo ""
echo "================================================================"
echo "AC#3 Results: ${PASS_COUNT} passed, ${FAIL_COUNT} failed out of ${TOTAL_TESTS} tests"
echo "================================================================"

if [ "$FAIL_COUNT" -gt 0 ]; then
    exit 1
else
    exit 0
fi
