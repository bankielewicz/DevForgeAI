#!/usr/bin/env bash
# =============================================================================
# STORY-392 AC#6: Reference Files Remain Compatible
#
# Verifies the updated src/claude/agents/ac-compliance-verifier.md:
# 1. All 4 reference files are correctly referenced via Read() in core agent
# 2. Reference files are NOT modified (out of scope - verify they exist)
# 3. Reference file paths resolve correctly
# 4. Core agent uses correct path patterns for reference loading
#
# TDD Phase: RED (these tests must FAIL before implementation)
# =============================================================================

set -euo pipefail

PROJECT_ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
AGENT_FILE="${PROJECT_ROOT}/src/claude/agents/ac-compliance-verifier.md"
REF_DIR="${PROJECT_ROOT}/src/claude/agents/ac-compliance-verifier/references"

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
echo "STORY-392 AC#6: Reference File Compatibility Tests"
echo "Target: ${AGENT_FILE}"
echo "Reference Dir: ${REF_DIR}"
echo "================================================================"
echo ""

# --- Pre-check: Agent file exists ---
if [ ! -f "$AGENT_FILE" ]; then
    echo "FATAL: Agent file not found at ${AGENT_FILE}"
    exit 1
fi

# =============================================================================
# Test 1: All 4 reference files exist on disk
# =============================================================================
echo "--- Reference Files Exist ---"

REF_1="${REF_DIR}/xml-parsing-protocol.md"
REF_2="${REF_DIR}/verification-workflow.md"
REF_3="${REF_DIR}/scoring-methodology.md"
REF_4="${REF_DIR}/report-generation.md"

run_test "xml-parsing-protocol.md exists" "$( [ -f "$REF_1" ] && echo 0 || echo 1 )"
run_test "verification-workflow.md exists" "$( [ -f "$REF_2" ] && echo 0 || echo 1 )"
run_test "scoring-methodology.md exists" "$( [ -f "$REF_3" ] && echo 0 || echo 1 )"
run_test "report-generation.md exists" "$( [ -f "$REF_4" ] && echo 0 || echo 1 )"

# =============================================================================
# Test 2: Core agent references all 4 files via Read()
# =============================================================================
echo ""
echo "--- References in Core Agent ---"

# Each reference file must be referenced in the core agent with Read() pattern
HAS_XML_REF=$(grep -c 'xml-parsing-protocol.md' "$AGENT_FILE" || true)
run_test "Core agent references xml-parsing-protocol.md (found: ${HAS_XML_REF})" "$( [ "$HAS_XML_REF" -ge 1 ] && echo 0 || echo 1 )"

HAS_WORKFLOW_REF=$(grep -c 'verification-workflow.md' "$AGENT_FILE" || true)
run_test "Core agent references verification-workflow.md (found: ${HAS_WORKFLOW_REF})" "$( [ "$HAS_WORKFLOW_REF" -ge 1 ] && echo 0 || echo 1 )"

HAS_SCORING_REF=$(grep -c 'scoring-methodology.md' "$AGENT_FILE" || true)
run_test "Core agent references scoring-methodology.md (found: ${HAS_SCORING_REF})" "$( [ "$HAS_SCORING_REF" -ge 1 ] && echo 0 || echo 1 )"

HAS_REPORT_REF=$(grep -c 'report-generation.md' "$AGENT_FILE" || true)
run_test "Core agent references report-generation.md (found: ${HAS_REPORT_REF})" "$( [ "$HAS_REPORT_REF" -ge 1 ] && echo 0 || echo 1 )"

# =============================================================================
# Test 3: References use Read() invocation pattern
# =============================================================================
echo ""
echo "--- Read() Invocation Pattern ---"

# Each reference must be loaded via Read(file_path="...") pattern
HAS_READ_XML=$(grep -c 'Read(file_path=.*xml-parsing-protocol' "$AGENT_FILE" || true)
run_test "xml-parsing-protocol loaded via Read() (found: ${HAS_READ_XML})" "$( [ "$HAS_READ_XML" -ge 1 ] && echo 0 || echo 1 )"

HAS_READ_WORKFLOW=$(grep -c 'Read(file_path=.*verification-workflow' "$AGENT_FILE" || true)
run_test "verification-workflow loaded via Read() (found: ${HAS_READ_WORKFLOW})" "$( [ "$HAS_READ_WORKFLOW" -ge 1 ] && echo 0 || echo 1 )"

HAS_READ_SCORING=$(grep -c 'Read(file_path=.*scoring-methodology' "$AGENT_FILE" || true)
run_test "scoring-methodology loaded via Read() (found: ${HAS_READ_SCORING})" "$( [ "$HAS_READ_SCORING" -ge 1 ] && echo 0 || echo 1 )"

HAS_READ_REPORT=$(grep -c 'Read(file_path=.*report-generation' "$AGENT_FILE" || true)
run_test "report-generation loaded via Read() (found: ${HAS_READ_REPORT})" "$( [ "$HAS_READ_REPORT" -ge 1 ] && echo 0 || echo 1 )"

# =============================================================================
# Test 4: Path patterns resolve correctly
# =============================================================================
echo ""
echo "--- Path Pattern Validation ---"

# Extract all reference paths from the agent file
# They should use the .claude/agents/ac-compliance-verifier/references/ path
REF_PATH_COUNT=$(grep -c 'ac-compliance-verifier/references/' "$AGENT_FILE" || true)
run_test "References use ac-compliance-verifier/references/ path (found: ${REF_PATH_COUNT}, want >= 4)" "$( [ "$REF_PATH_COUNT" -ge 4 ] && echo 0 || echo 1 )"

# Verify all paths use consistent prefix (.claude/agents/ pattern)
CONSISTENT_PREFIX=$(grep -c '\.claude/agents/ac-compliance-verifier/references/' "$AGENT_FILE" || true)
run_test "All paths use .claude/agents/ prefix (found: ${CONSISTENT_PREFIX}, want >= 4)" "$( [ "$CONSISTENT_PREFIX" -ge 4 ] && echo 0 || echo 1 )"

# =============================================================================
# Test 5: Total reference count (exactly 4 reference files referenced)
# =============================================================================
echo ""
echo "--- Reference Count ---"

UNIQUE_REFS=0
for ref_name in "xml-parsing-protocol.md" "verification-workflow.md" "scoring-methodology.md" "report-generation.md"; do
    FOUND=$(grep -c "${ref_name}" "$AGENT_FILE" || true)
    if [ "$FOUND" -ge 1 ]; then
        UNIQUE_REFS=$((UNIQUE_REFS + 1))
    fi
done
run_test "All 4 unique reference files referenced (found: ${UNIQUE_REFS}/4)" "$( [ "$UNIQUE_REFS" -ge 4 ] && echo 0 || echo 1 )"

# =============================================================================
# Test 6: Reference Loading section exists (canonical template requirement)
# =============================================================================
echo ""
echo "--- Reference Loading Section (Template Requirement) ---"

# The canonical template requires a dedicated "Reference Loading" section
# that documents on-demand reference loading with When/Load patterns
HAS_REF_LOADING_SECTION=$(grep -c '^## Reference Loading' "$AGENT_FILE" || true)
run_test "Dedicated '## Reference Loading' section exists" "$( [ "$HAS_REF_LOADING_SECTION" -ge 1 ] && echo 0 || echo 1 )"

# Reference Loading section must contain When/Load context per canonical template
REF_LOADING_CONTENT=$(sed -n '/^## Reference Loading/,/^## [A-Z]/p' "$AGENT_FILE" 2>/dev/null | head -n -1 || true)
HAS_WHEN_LOAD=$(echo "$REF_LOADING_CONTENT" | grep -ciE 'When:|Load:|on-demand|on demand' || true)
run_test "Reference Loading describes when to load each reference (found: ${HAS_WHEN_LOAD})" "$( [ "$HAS_WHEN_LOAD" -ge 1 ] && echo 0 || echo 1 )"

# =============================================================================
# Test 7: References organized within Workflow section (not scattered)
# =============================================================================
echo ""
echo "--- Reference Organization ---"

# In the canonical template, the Workflow section should reference when to load
# each reference file contextually (e.g., "For XML parsing, load: ...")
WORKFLOW_CONTENT=$(sed -n '/^## Workflow/,/^## [A-Z]/p' "$AGENT_FILE" 2>/dev/null | head -n -1 || true)
WORKFLOW_REFS=$(echo "$WORKFLOW_CONTENT" | grep -c 'references/' || true)
run_test "Workflow section contains reference loading instructions (found: ${WORKFLOW_REFS})" "$( [ "$WORKFLOW_REFS" -ge 2 ] && echo 0 || echo 1 )"

# =============================================================================
# Summary
# =============================================================================
echo ""
echo "================================================================"
echo "AC#6 Results: ${PASS_COUNT} passed, ${FAIL_COUNT} failed out of ${TOTAL_TESTS} tests"
echo "================================================================"

if [ "$FAIL_COUNT" -gt 0 ]; then
    exit 1
else
    exit 0
fi
