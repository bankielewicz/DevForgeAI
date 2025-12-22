# Session Recovery Prompt for STORY-118

**Use this prompt when starting a new Claude session after context window reset or crash.**

Copy everything below the line and paste as your first message:

---

## RECOVERY PROMPT - PASTE THIS INTO NEW SESSION

```
You are resuming work on DevForgeAI framework. The previous session's context window was reset or crashed. There may be incomplete in-flight work.

## CRITICAL: Check for Incomplete Work First

Before proceeding, execute these verification steps IN ORDER:

### Step 1: Load the Plan File
Read /home/bryan/.claude/plans/frolicking-stirring-lecun.md

This plan contains:
- Quick Resume Guide with current state
- Reference files table with Read commands
- Progress checkpoints to track completion
- Session recovery procedure
- All file paths needed to resume

### Step 2: Check for In-Flight File Modifications

Run these commands to detect incomplete edits:

```bash
# Check git status for uncommitted changes
git status --short

# Check for partial writes (files modified in last hour)
find devforgeai/ast-grep/rules -name "*.yml" -mmin -60 2>/dev/null

# Check for backup files indicating interrupted edits
find . -name "*.bak" -o -name "*~" -o -name "*.swp" 2>/dev/null | head -10
```

### Step 3: Verify Story State

```bash
# Get current story status
grep "^status:" devforgeai/specs/Stories/STORY-118-core-antipattern-rules.story.md

# Check if QA report exists
ls -la devforgeai/qa/reports/STORY-118*

# Check if gaps.json exists (indicates QA failed and remediation needed)
cat devforgeai/qa/reports/STORY-118-gaps.json 2>/dev/null | head -20
```

### Step 4: Determine Recovery Path

Based on story status:

| Status | Action |
|--------|--------|
| `status: QA Failed` | Run `/dev STORY-118` to enter remediation mode |
| `status: Dev Complete` | Run `/qa STORY-118 deep` to validate |
| `status: In Development` | Check gaps.json, continue fixing tests |
| `status: QA Approved` | Run `/release STORY-118` |

### Step 5: If In-Flight Work Detected

If git status shows uncommitted changes:

1. **Review changes**: `git diff`
2. **If changes look complete**: Commit them
3. **If changes look incomplete**:
   - Check the plan file's "Failing Tests" table
   - Identify which rule file was being edited
   - Complete the edit based on test requirements
   - Verify with: `pytest tests/unit/test_antipattern_rules_story118.py -v -k "<test_name>"`

### Step 6: Resume from Checkpoint

The plan file has Progress Checkpoints. Find the first unchecked item and resume from there.

Key checkpoints for STORY-118:
- [ ] Fix AP-001 (god-object.yml) - 2 tests
- [ ] Fix AP-002 (async-void.yml) - 1 test
- [ ] Fix AP-004 (magic-numbers.yml) - 1 test
- [ ] Fix AP-008 (excessive-params.yml) - 1 test
- [ ] Fix AP-010 (empty-catch.yml) - 1 test
- [ ] Decision: AP-009 duplicate code
- [ ] Decision: AP-005 test exclusion
- [ ] Re-run: /qa STORY-118 deep

## Context Summary

**What happened**: `/qa STORY-118 deep` was executed and FAILED with 8/59 tests failing.

**Current state**: Story is "QA Failed", gaps.json created for remediation.

**Key files**:
- Plan: `/home/bryan/.claude/plans/frolicking-stirring-lecun.md`
- Story: `devforgeai/specs/Stories/STORY-118-core-antipattern-rules.story.md`
- Gaps: `devforgeai/qa/reports/STORY-118-gaps.json`
- QA Report: `devforgeai/qa/reports/STORY-118-qa-report.md`
- Test File: `tests/unit/test_antipattern_rules_story118.py`

**Failing tests mapped to rule files**:
1. AP-001: `devforgeai/ast-grep/rules/python/anti-patterns/god-object.yml`
2. AP-002: `devforgeai/ast-grep/rules/csharp/anti-patterns/async-void.yml`
3. AP-004: `devforgeai/ast-grep/rules/python/anti-patterns/magic-numbers.yml`
4. AP-008: `devforgeai/ast-grep/rules/python/anti-patterns/excessive-params.yml`
5. AP-010: `devforgeai/ast-grep/rules/csharp/anti-patterns/empty-catch.yml`

## Your Role

You are Opus - the architectural advisor for DevForgeAI. You:
- Delegate to subagents in `.claude/agents/` and skills in `.claude/skills/`
- Create todo lists to track progress
- HALT on ambiguity and use AskUserQuestion
- Ensure all work follows spec-driven development

Now execute Step 1: Read the plan file and report current state.
```

---

## QUICK VERSION (If full prompt too long)

```
Resume STORY-118 remediation. Context was lost.

1. Read /home/bryan/.claude/plans/frolicking-stirring-lecun.md
2. Run: git status --short
3. Run: grep "^status:" devforgeai/specs/Stories/STORY-118*.story.md
4. Check: ls devforgeai/qa/reports/STORY-118*
5. If "QA Failed": Run /dev STORY-118
6. Report findings and continue from plan checkpoints

Key context: 8 tests failing in STORY-118, need to fix ast-grep rule patterns.
```

---

## EMERGENCY MINIMAL VERSION

```
Read /home/bryan/.claude/plans/frolicking-stirring-lecun.md and resume STORY-118 work. Check git status for in-flight changes first.
```
