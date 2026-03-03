#!/usr/bin/env bash
# =============================================================================
# STORY-402: Add Git Staging Guidance for Parallel Stories
# Test Suite: Acceptance Criteria Validation (TDD RED Phase)
#
# Target File: src/claude/skills/devforgeai-development/references/git-workflow-conventions.md
#
# These tests validate that the new "Selective Staging for Parallel Stories"
# section exists and contains all required content per the acceptance criteria.
#
# All tests should FAIL initially (RED state) because the section has not
# been added yet.
# =============================================================================

set -uo pipefail

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
TARGET_FILE="$PROJECT_ROOT/src/claude/skills/devforgeai-development/references/git-workflow-conventions.md"

# Test counters
PASS_COUNT=0
FAIL_COUNT=0
TOTAL_COUNT=0

# ---------------------------------------------------------------------------
# Test Helper Functions
# ---------------------------------------------------------------------------

# Safe grep count - returns integer even when grep finds no matches
grep_count() {
    local result
    result=$(grep -c "$@" 2>/dev/null) || true
    echo "${result:-0}"
}

# Safe grep count case-insensitive
grep_count_i() {
    local result
    result=$(grep -ci "$@" 2>/dev/null) || true
    echo "${result:-0}"
}

assert_pass() {
    local test_name="$1"
    TOTAL_COUNT=$((TOTAL_COUNT + 1))
    PASS_COUNT=$((PASS_COUNT + 1))
    echo "  PASS: $test_name"
}

assert_fail() {
    local test_name="$1"
    local reason="$2"
    TOTAL_COUNT=$((TOTAL_COUNT + 1))
    FAIL_COUNT=$((FAIL_COUNT + 1))
    echo "  FAIL: $test_name"
    echo "        Reason: $reason"
}

print_summary() {
    echo ""
    echo "============================================================================="
    echo "  STORY-402 Test Results"
    echo "============================================================================="
    echo "  Total:  $TOTAL_COUNT"
    echo "  Passed: $PASS_COUNT"
    echo "  Failed: $FAIL_COUNT"
    echo "============================================================================="
    if [ "$FAIL_COUNT" -gt 0 ]; then
        echo "  STATUS: RED (failing tests - implementation needed)"
        exit 1
    else
        echo "  STATUS: GREEN (all tests passing)"
        exit 0
    fi
}

# ---------------------------------------------------------------------------
# Pre-flight: Verify target file exists
# ---------------------------------------------------------------------------
echo ""
echo "============================================================================="
echo "  STORY-402: Git Staging Guidance for Parallel Stories"
echo "  TDD Validation Tests"
echo "============================================================================="
echo ""
echo "Target: $TARGET_FILE"
echo ""

if [ ! -f "$TARGET_FILE" ]; then
    echo "FATAL: Target file does not exist: $TARGET_FILE"
    exit 2
fi

# ===========================================================================
# AC#1: New section exists with heading "## Selective Staging for Parallel Stories"
# ===========================================================================
echo "--- AC#1: Section Heading Exists ---"

# Test 1.1: Section heading exists exactly once
HEADING_COUNT=$(grep_count "^## Selective Staging for Parallel Stories" "$TARGET_FILE")
if [ "$HEADING_COUNT" -eq 1 ]; then
    assert_pass "AC1.1 - Section heading '## Selective Staging for Parallel Stories' exists exactly once"
else
    assert_fail "AC1.1 - Section heading '## Selective Staging for Parallel Stories' exists exactly once" \
        "Expected 1 match, found $HEADING_COUNT"
fi

# Test 1.2: Section is positioned after line 1100 (after existing staging strategy content)
if [ "$HEADING_COUNT" -ge 1 ]; then
    HEADING_LINE=$(grep -n "^## Selective Staging for Parallel Stories" "$TARGET_FILE" | head -1 | cut -d: -f1)
    if [ "$HEADING_LINE" -gt 1100 ]; then
        assert_pass "AC1.2 - Section positioned after existing staging content (line $HEADING_LINE > 1100)"
    else
        assert_fail "AC1.2 - Section positioned after existing staging content" \
            "Found at line $HEADING_LINE, expected after line 1100"
    fi
else
    assert_fail "AC1.2 - Section positioned after existing staging content" \
        "Section heading not found, cannot check position"
fi

# ===========================================================================
# AC#2: Pattern-based git add examples included
# ===========================================================================
echo ""
echo "--- AC#2: Pattern-based git add Examples ---"

# Test 2.1: At least 3 git add command examples with story-specific patterns
# Look for git add commands that reference STORY-XXX type patterns in the new section
# We search globally first; the section-scoped tests below validate context
GIT_ADD_STORY_COUNT=$(grep_count "git add.*STORY" "$TARGET_FILE")
if [ "$GIT_ADD_STORY_COUNT" -ge 3 ]; then
    assert_pass "AC2.1 - At least 3 git add examples with STORY-XXX patterns (found $GIT_ADD_STORY_COUNT)"
else
    assert_fail "AC2.1 - At least 3 git add examples with STORY-XXX patterns" \
        "Expected at least 3, found $GIT_ADD_STORY_COUNT"
fi

# Test 2.2: Story files pattern included (devforgeai/specs/Stories/STORY-*)
STORY_FILES_PATTERN=$(grep_count 'git add.*Stories/STORY\|git add.*story.*\.md\|git add.*STORY.*story' "$TARGET_FILE")
if [ "$STORY_FILES_PATTERN" -ge 1 ]; then
    assert_pass "AC2.2 - Story file staging pattern included (found $STORY_FILES_PATTERN)"
else
    assert_fail "AC2.2 - Story file staging pattern included" \
        "Expected at least 1 example showing story file staging, found $STORY_FILES_PATTERN"
fi

# Test 2.3: Phase state pattern included (devforgeai/workflows/STORY-*)
PHASE_STATE_PATTERN=$(grep_count 'git add.*workflows/STORY\|git add.*phase-state' "$TARGET_FILE")
if [ "$PHASE_STATE_PATTERN" -ge 1 ]; then
    assert_pass "AC2.3 - Phase state staging pattern included (found $PHASE_STATE_PATTERN)"
else
    assert_fail "AC2.3 - Phase state staging pattern included" \
        "Expected at least 1 example showing phase state staging, found $PHASE_STATE_PATTERN"
fi

# Test 2.4: Implementation-specific pattern included (tests/STORY-* or src/ patterns)
IMPL_PATTERN=$(grep_count 'git add.*tests/STORY\|git add.*src/.*STORY\|git add.*implementation' "$TARGET_FILE")
if [ "$IMPL_PATTERN" -ge 1 ]; then
    assert_pass "AC2.4 - Implementation-specific staging pattern included (found $IMPL_PATTERN)"
else
    assert_fail "AC2.4 - Implementation-specific staging pattern included" \
        "Expected at least 1 example showing implementation file staging, found $IMPL_PATTERN"
fi

# ===========================================================================
# AC#3: Verification command documented
# ===========================================================================
echo ""
echo "--- AC#3: Verification Command Documented ---"

# Test 3.1: git diff --cached --name-only command present
DIFF_CACHED_COUNT=$(grep_count "git diff --cached --name-only" "$TARGET_FILE")
if [ "$DIFF_CACHED_COUNT" -ge 1 ]; then
    assert_pass "AC3.1 - 'git diff --cached --name-only' verification command present (found $DIFF_CACHED_COUNT)"
else
    assert_fail "AC3.1 - 'git diff --cached --name-only' verification command present" \
        "Expected at least 1 occurrence, found $DIFF_CACHED_COUNT"
fi

# Test 3.2: Instruction to run before every commit
SELECTIVE_SECTION_EXISTS=$(grep_count "Selective Staging" "$TARGET_FILE")
if [ "$SELECTIVE_SECTION_EXISTS" -ge 1 ]; then
    # Extract content from the selective staging section and check for before-commit instruction
    SECTION_TEXT=$(sed -n '/## Selective Staging for Parallel Stories/,/^## /p' "$TARGET_FILE" 2>/dev/null)
    SECTION_INSTRUCTION=$(echo "$SECTION_TEXT" | grep -ci 'before.*commit\|before every commit\|prior to.*commit' 2>/dev/null) || true
    SECTION_INSTRUCTION="${SECTION_INSTRUCTION:-0}"
    if [ "$SECTION_INSTRUCTION" -ge 1 ]; then
        assert_pass "AC3.2 - Instruction to run verification before every commit (found in section)"
    else
        assert_fail "AC3.2 - Instruction to run verification before every commit" \
            "Section exists but instruction not found within it"
    fi
else
    assert_fail "AC3.2 - Instruction to run verification before every commit" \
        "Selective Staging section not found, cannot verify instruction placement"
fi

# ===========================================================================
# AC#4: Anti-pattern warning for broad staging commands
# ===========================================================================
echo ""
echo "--- AC#4: Anti-pattern Warning for Broad Staging ---"

if [ "$SELECTIVE_SECTION_EXISTS" -ge 1 ]; then
    # Extract the selective staging section content
    SECTION_CONTENT=$(sed -n '/## Selective Staging for Parallel Stories/,/^## /p' "$TARGET_FILE" 2>/dev/null)

    # Test 4.1: Warning about "git add ."
    GIT_ADD_DOT_WARNING=$(echo "$SECTION_CONTENT" | grep -c 'git add \.' 2>/dev/null) || true
    GIT_ADD_DOT_WARNING="${GIT_ADD_DOT_WARNING:-0}"
    if [ "$GIT_ADD_DOT_WARNING" -ge 1 ]; then
        assert_pass "AC4.1 - Warning about 'git add .' present in Selective Staging section"
    else
        assert_fail "AC4.1 - Warning about 'git add .' present in Selective Staging section" \
            "Warning not found in section content"
    fi

    # Test 4.2: Warning about "git add -A"
    GIT_ADD_A_WARNING=$(echo "$SECTION_CONTENT" | grep -c 'git add -A' 2>/dev/null) || true
    GIT_ADD_A_WARNING="${GIT_ADD_A_WARNING:-0}"
    if [ "$GIT_ADD_A_WARNING" -ge 1 ]; then
        assert_pass "AC4.2 - Warning about 'git add -A' present in Selective Staging section"
    else
        assert_fail "AC4.2 - Warning about 'git add -A' present in Selective Staging section" \
            "Warning not found in section content"
    fi

    # Test 4.3: Contamination explanation
    CONTAMINATE_WARNING=$(echo "$SECTION_CONTENT" | grep -ci 'contaminat\|unrelated.*changes\|wrong.*story\|cross-story\|mix.*changes' 2>/dev/null) || true
    CONTAMINATE_WARNING="${CONTAMINATE_WARNING:-0}"
    if [ "$CONTAMINATE_WARNING" -ge 1 ]; then
        assert_pass "AC4.3 - Contamination/mixing explanation present"
    else
        assert_fail "AC4.3 - Contamination/mixing explanation present" \
            "Expected explanation of how broad staging can contaminate commits, not found"
    fi
else
    assert_fail "AC4.1 - Warning about 'git add .' present in Selective Staging section" \
        "Selective Staging section not found"
    assert_fail "AC4.2 - Warning about 'git add -A' present in Selective Staging section" \
        "Selective Staging section not found"
    assert_fail "AC4.3 - Contamination/mixing explanation present" \
        "Selective Staging section not found"
fi

# ===========================================================================
# AC#5: Worktree recommendation with cross-reference
# ===========================================================================
echo ""
echo "--- AC#5: Worktree Recommendation with Cross-Reference ---"

if [ "$SELECTIVE_SECTION_EXISTS" -ge 1 ]; then
    SECTION_CONTENT=$(sed -n '/## Selective Staging for Parallel Stories/,/^## /p' "$TARGET_FILE" 2>/dev/null)

    # Test 5.1: Reference to existing lock coordination section
    LOCK_REF=$(echo "$SECTION_CONTENT" | grep -ci 'Lock Coordination\|Phase 08.0.5\|lock.*coordination' 2>/dev/null) || true
    LOCK_REF="${LOCK_REF:-0}"
    if [ "$LOCK_REF" -ge 1 ]; then
        assert_pass "AC5.1 - Reference to Lock Coordination / Phase 08.0.5 present"
    else
        assert_fail "AC5.1 - Reference to Lock Coordination / Phase 08.0.5 present" \
            "Expected cross-reference to Lock Coordination or Phase 08.0.5, not found"
    fi

    # Test 5.2: Worktree recommendation for stories touching shared files
    WORKTREE_REC=$(echo "$SECTION_CONTENT" | grep -ci 'worktree\|git worktree' 2>/dev/null) || true
    WORKTREE_REC="${WORKTREE_REC:-0}"
    if [ "$WORKTREE_REC" -ge 1 ]; then
        assert_pass "AC5.2 - Worktree recommendation present"
    else
        assert_fail "AC5.2 - Worktree recommendation present" \
            "Expected recommendation for git worktrees, not found"
    fi

    # Test 5.3: Shared files context for worktree recommendation
    SHARED_FILES_CONTEXT=$(echo "$SECTION_CONTENT" | grep -ci 'shared.*file\|many.*file\|overlapping\|multiple.*stories\|parallel.*stories' 2>/dev/null) || true
    SHARED_FILES_CONTEXT="${SHARED_FILES_CONTEXT:-0}"
    if [ "$SHARED_FILES_CONTEXT" -ge 1 ]; then
        assert_pass "AC5.3 - Shared files context for worktree recommendation present"
    else
        assert_fail "AC5.3 - Shared files context for worktree recommendation present" \
            "Expected mention of shared/overlapping files as worktree motivation, not found"
    fi
else
    assert_fail "AC5.1 - Reference to Lock Coordination / Phase 08.0.5 present" \
        "Selective Staging section not found"
    assert_fail "AC5.2 - Worktree recommendation present" \
        "Selective Staging section not found"
    assert_fail "AC5.3 - Shared files context for worktree recommendation present" \
        "Selective Staging section not found"
fi

# ===========================================================================
# Summary
# ===========================================================================
print_summary
