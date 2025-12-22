# Session Recovery Prompt: STORY-118 QA Architectural Review

**Use this prompt to resume work after context window reset or crash.**

---

## Recovery Prompt (Copy/Paste into New Session)

```
I am resuming work on the DevForgeAI framework after a context window reset or session crash.

## Previous Session Context

**Task:** Architectural Review of /qa STORY-118 Deep Execution
**Plan File:** /home/bryan/.claude/plans/frolicking-stirring-lecun.md
**Status:** POST-EXECUTION REVIEW - QA validation completed, architectural observations documented

## CRITICAL: Verify State Before Proceeding

The previous session may have been interrupted mid-operation. Before taking ANY action:

1. **Read the plan file first:**
   ```
   Read /home/bryan/.claude/plans/frolicking-stirring-lecun.md
   ```

2. **Check story status for in-flight modifications:**
   ```
   Grep "^status:" devforgeai/specs/Stories/STORY-118-core-antipattern-rules.story.md
   ```
   Expected: "status: QA Failed" (if QA completed) or "status: Dev Complete" (if interrupted)

3. **Verify QA artifacts exist:**
   ```
   Glob devforgeai/qa/reports/STORY-118*.{md,json}
   ```
   Expected: STORY-118-qa-report.md and STORY-118-gaps.json

4. **Check for lock files (indicates interrupted operation):**
   ```
   Glob tests/results/STORY-118/.qa-lock
   ```
   If found: Previous QA was interrupted. Delete lock and re-run if needed.

## What Was Completed

- [x] /qa STORY-118 deep executed
- [x] QA validation FAILED (8/59 tests failing, 86.4% pass rate)
- [x] Story status updated: Dev Complete → QA Failed
- [x] QA report generated: devforgeai/qa/reports/STORY-118-qa-report.md
- [x] Gaps file created: devforgeai/qa/reports/STORY-118-gaps.json
- [x] Architectural review documented in plan file
- [x] 5 improvement recommendations identified

## What May Need Verification

If session crashed during:
- **Phase 5 (Report Generation):** Check if QA report exists and is complete
- **Phase 6 (Feedback Hooks):** Non-blocking, can be skipped
- **Phase 7 (Story Update):** Check if story status and QA Validation History were added
- **Plan File Updates:** Check if architectural review sections are complete

## Key Files to Read

| Priority | File | Purpose |
|----------|------|---------|
| 1 | Plan file (above) | Full context and checkpoints |
| 2 | `devforgeai/specs/Stories/STORY-118-core-antipattern-rules.story.md` | Story status and QA history |
| 3 | `devforgeai/qa/reports/STORY-118-gaps.json` | Failing tests and remediation sequence |
| 4 | `.claude/skills/devforgeai-qa/SKILL.md` | QA skill (if reviewing phases) |

## Next Actions (Choose Based on State)

**If QA artifacts exist and story shows "QA Failed":**
→ Previous session completed successfully. Use plan file for next steps.
→ Options: `/dev STORY-118` (remediate) or create improvement stories

**If QA artifacts missing or incomplete:**
→ Re-run: `/qa STORY-118 deep`

**If story status is still "Dev Complete":**
→ QA was interrupted before completion. Re-run: `/qa STORY-118 deep`

**If lock file exists:**
→ Delete: `Bash rm tests/results/STORY-118/.qa-lock`
→ Then re-run QA if needed

## Framework Context

- **Project:** DevForgeAI Spec-Driven Development Framework
- **Location:** /mnt/c/Projects/DevForgeAI2
- **My Role:** Opus - architectural advisor providing grounded (not aspirational) improvements
- **Constraint:** All solutions must work within Claude Code Terminal capabilities

## Do NOT

- Make changes without reading the plan file first
- Assume previous session completed successfully
- Skip state verification steps
- Run /dev or /qa without checking current status

Please read the plan file and verify state, then ask me what I'd like to do next.
```

---

## Quick Verification Commands

Run these in order to assess state:

```bash
# 1. Read plan file
Read /home/bryan/.claude/plans/frolicking-stirring-lecun.md

# 2. Check story status
Grep "^status:" devforgeai/specs/Stories/STORY-118-core-antipattern-rules.story.md

# 3. Check QA artifacts
Glob devforgeai/qa/reports/STORY-118*.{md,json}

# 4. Check for lock files
Glob tests/results/STORY-118/.qa-lock

# 5. View QA Validation History (if exists)
Grep -A 30 "## QA Validation History" devforgeai/specs/Stories/STORY-118-core-antipattern-rules.story.md
```

---

## Expected State After Successful Completion

| Artifact | Expected State |
|----------|----------------|
| Story status | `status: QA Failed` |
| QA report | Exists at `devforgeai/qa/reports/STORY-118-qa-report.md` |
| Gaps JSON | Exists at `devforgeai/qa/reports/STORY-118-gaps.json` |
| QA Validation History | Added to story file |
| Workflow History | Entry for "Status: QA Failed" added |
| Lock file | Does NOT exist (released on completion) |
| Plan file | Contains "POST-EXECUTION REVIEW" status |

---

## Failing Tests Summary (for quick reference)

| Test | Rule | Fix Location |
|------|------|--------------|
| test_god_object_many_methods_python | AP-001 | `devforgeai/ast-grep/rules/python/anti-patterns/god-object.yml` |
| test_god_object_many_fields_python | AP-001 | `devforgeai/ast-grep/rules/python/anti-patterns/god-object.yml` |
| test_async_void_detected_csharp | AP-002 | `devforgeai/ast-grep/rules/csharp/anti-patterns/async-void.yml` |
| test_magic_numbers_detected_python | AP-004 | `devforgeai/ast-grep/rules/python/anti-patterns/magic-numbers.yml` |
| test_long_method_test_excluded | AP-005 | Test design issue |
| test_excessive_params_detected_python | AP-008 | `devforgeai/ast-grep/rules/python/anti-patterns/excessive-params.yml` |
| test_duplicate_code_detected_python | AP-009 | Architecture limitation (needs ADR) |
| test_empty_catch_detected_csharp | AP-010 | `devforgeai/ast-grep/rules/csharp/anti-patterns/empty-catch.yml` |

---

**Created:** 2025-12-21
**For Session:** STORY-118 QA Architectural Review
**Plan File:** /home/bryan/.claude/plans/frolicking-stirring-lecun.md
