#!/bin/bash
# Integration Tests: STORY-538 - Cross-Component Validation
# Tests command-to-skill flow, reference links, consistency, subagent deps, output paths
# Generated: 2026-03-05

PASSED=0
FAILED=0
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"

pass() { echo "  PASS: $1"; ((PASSED++)); }
fail() { echo "  FAIL: $1"; ((FAILED++)); }

echo "============================================="
echo "  STORY-538: Integration Tests"
echo "============================================="
echo ""

# --- IT-1: Command-to-Skill Flow ---
echo "--- IT-1: Command References Correct Skill Name ---"

# Command must reference "researching-market" skill name
SKILL_REF=$(grep -c 'researching-market' "$PROJECT_ROOT/src/claude/commands/market-research.md")
if [ "$SKILL_REF" -ge 1 ]; then
    pass "Command references 'researching-market' skill"
else
    fail "Command does not reference 'researching-market' skill"
fi

# Skill directory must exist at the path the command expects
if [ -d "$PROJECT_ROOT/src/claude/skills/researching-market" ]; then
    pass "Skill directory exists at src/claude/skills/researching-market/"
else
    fail "Skill directory missing at src/claude/skills/researching-market/"
fi

# Skill SKILL.md must exist
if [ -f "$PROJECT_ROOT/src/claude/skills/researching-market/SKILL.md" ]; then
    pass "SKILL.md exists in skill directory"
else
    fail "SKILL.md missing in skill directory"
fi

echo ""

# --- IT-2: Skill-to-Reference Links ---
echo "--- IT-2: All Reference Files in SKILL.md Exist on Disk ---"

REF_DIR="$PROJECT_ROOT/src/claude/skills/researching-market/references"

# Extract reference file names from SKILL.md reference table
for ref_file in market-sizing-methodology.md fermi-estimation.md competitive-analysis-framework.md customer-interview-guide.md; do
    # Verify SKILL.md mentions this reference
    if grep -q "$ref_file" "$PROJECT_ROOT/src/claude/skills/researching-market/SKILL.md"; then
        # Verify file exists on disk
        if [ -f "$REF_DIR/$ref_file" ]; then
            pass "Reference '$ref_file' mentioned in SKILL.md and exists on disk"
        else
            fail "Reference '$ref_file' mentioned in SKILL.md but MISSING on disk"
        fi
    else
        fail "Reference '$ref_file' not mentioned in SKILL.md"
    fi
done

echo ""

# --- IT-3: Cross-File Consistency (Allowed Tools) ---
echo "--- IT-3: Command YAML Frontmatter Tool Consistency ---"

# Command's allowed-tools must include tools the skill needs for delegation
# Command needs at minimum: Read (to load skill), Skill (to invoke skill)
CMD_FILE="$PROJECT_ROOT/src/claude/commands/market-research.md"

if grep -q 'allowed-tools:' "$CMD_FILE"; then
    ALLOWED_TOOLS=$(grep 'allowed-tools:' "$CMD_FILE")
    # Command must have Read tool (needed to load files)
    if echo "$ALLOWED_TOOLS" | grep -q 'Read'; then
        pass "Command allowed-tools includes 'Read'"
    else
        fail "Command allowed-tools missing 'Read'"
    fi
    # Command must have AskUserQuestion (for argument validation errors)
    if echo "$ALLOWED_TOOLS" | grep -q 'AskUserQuestion'; then
        pass "Command allowed-tools includes 'AskUserQuestion'"
    else
        fail "Command allowed-tools missing 'AskUserQuestion'"
    fi
else
    fail "Command file missing 'allowed-tools' YAML frontmatter"
fi

# Verify skill tools header lists tools it actually uses in workflow
SKILL_FILE="$PROJECT_ROOT/src/claude/skills/researching-market/SKILL.md"
SKILL_TOOLS=$(grep '^tools:' "$SKILL_FILE")

for tool in Read Write AskUserQuestion Agent; do
    if echo "$SKILL_TOOLS" | grep -q "$tool"; then
        pass "Skill tools includes '$tool'"
    else
        fail "Skill tools missing '$tool' (used in workflow)"
    fi
done

echo ""

# --- IT-4: Subagent Dependencies ---
echo "--- IT-4: Referenced Subagents Exist ---"

# SKILL.md references internet-sleuth and market-analyst subagents
for agent in internet-sleuth market-analyst; do
    if grep -q "$agent" "$SKILL_FILE"; then
        if [ -f "$PROJECT_ROOT/.claude/agents/$agent.md" ]; then
            pass "Subagent '$agent' referenced in SKILL.md and exists in .claude/agents/"
        else
            fail "Subagent '$agent' referenced in SKILL.md but MISSING in .claude/agents/"
        fi
    else
        fail "Subagent '$agent' not referenced in SKILL.md"
    fi
done

echo ""

# --- IT-5: Output Path Consistency ---
echo "--- IT-5: Output Paths Consistent Across Skill Sections ---"

# Market sizing output path should be consistent
MS_PATH="devforgeai/specs/business/market-research/market-sizing.md"
CA_PATH="devforgeai/specs/business/market-research/competitive-analysis.md"
CI_PATH="devforgeai/specs/business/market-research/customer-interviews.md"

for output_path in "$MS_PATH" "$CA_PATH" "$CI_PATH"; do
    # Count occurrences - should appear in both workflow and output specification sections
    COUNT=$(grep -c "$output_path" "$SKILL_FILE")
    if [ "$COUNT" -ge 2 ]; then
        pass "Output path '$output_path' referenced consistently ($COUNT occurrences)"
    else
        fail "Output path '$output_path' referenced only $COUNT time(s) - may be inconsistent"
    fi
done

echo ""

# --- IT-6: Phase Argument Enum Consistency ---
echo "--- IT-6: Phase Arguments Match Between Command and Skill ---"

# Valid phases defined in command
for phase in market-sizing competitive-analysis customer-interviews full; do
    CMD_HAS=$(grep -c "$phase" "$CMD_FILE")
    SKILL_HAS=$(grep -c "$phase" "$SKILL_FILE")
    if [ "$CMD_HAS" -ge 1 ] && [ "$SKILL_HAS" -ge 1 ]; then
        pass "Phase '$phase' present in both command and skill"
    else
        fail "Phase '$phase' missing from command ($CMD_HAS) or skill ($SKILL_HAS)"
    fi
done

echo ""

# --- IT-7: Skill Name in YAML Frontmatter Matches Directory ---
echo "--- IT-7: Skill YAML Name Matches Directory Name ---"

SKILL_NAME=$(grep '^name:' "$SKILL_FILE" | sed 's/name: *//')
DIR_NAME=$(basename "$(dirname "$SKILL_FILE")")
if [ "$SKILL_NAME" = "$DIR_NAME" ]; then
    pass "Skill YAML name '$SKILL_NAME' matches directory name '$DIR_NAME'"
else
    fail "Skill YAML name '$SKILL_NAME' does not match directory name '$DIR_NAME'"
fi

echo ""

# --- Summary ---
echo "============================================="
TOTAL=$((PASSED + FAILED))
echo "  Integration Tests: $PASSED/$TOTAL passed, $FAILED failed"
echo "============================================="

[ $FAILED -eq 0 ] && exit 0 || exit 1
