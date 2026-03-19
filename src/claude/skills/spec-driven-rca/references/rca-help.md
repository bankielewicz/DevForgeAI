# RCA Command - Help & Reference

**Source:** Extracted from `/rca` command for lean orchestration compliance (STORY-461)

---

## Quick Reference

```bash
# Perform RCA for framework breakdown
/rca "spec-driven-dev didn't validate context files"

# Specify severity explicitly
/rca "QA skill created autonomous deferrals" CRITICAL

# Simple issue description
/rca "orchestration skipped checkpoint detection"

# Multi-word description (quotes optional)
/rca Command had business logic in Phase 2
```

---

## Integration with DevForgeAI Framework

### When to Use

**Use /rca when:**
- Framework process didn't work as expected
- Skill/command violated intended workflow
- Quality gate was bypassed unexpectedly
- Context file constraints were ignored
- Workflow state transition was invalid
- Autonomous operations occurred (without user approval)
- User is confused about framework behavior

**Examples:**
```bash
/rca "spec-driven-dev didn't validate context files before TDD"
/rca "spec-driven-qa accepted pre-existing deferrals without challenge"
/rca "/dev command contains business logic in Phase 2"
/rca "Story transitioned to Released without QA Approved"
```

### Output

**Primary output:**
- RCA document in `devforgeai/RCA/RCA-{NNN}-{slug}.md`

**RCA document contains:**
- Issue description and metadata
- 5 Whys analysis with evidence
- Files examined (comprehensive excerpts)
- Recommendations by priority (CRITICAL/HIGH/MEDIUM/LOW)
- Exact implementation code/text (copy-paste ready)
- Testing procedures for each recommendation
- Implementation checklist
- Prevention strategy (short-term and long-term)
- Related RCAs

**Completion report displays:**
- RCA number and title
- Root cause (brief summary)
- Recommendation counts
- File path to full RCA document
- Next steps

### Framework-Aware Analysis

**The skill understands:**
- 6 immutable context files (tech-stack, source-tree, dependencies, coding-standards, architecture-constraints, anti-patterns)
- 4 quality gates (Context Validation, Test Passing, QA Approval, Release Readiness)
- 11 workflow states (Backlog → Released)
- Lean orchestration pattern (command/skill/subagent responsibilities)
- DevForgeAI architectural principles (spec-driven, evidence-based, progressive disclosure)

### Evidence-Based Recommendations

**All recommendations include:**
- Exact file paths (`.claude/skills/{skill}/SKILL.md`)
- Specific sections (Phase X, Step Y, Lines Z-W)
- Copy-paste ready implementation (exact code/text to add or modify)
- Evidence-based rationale (references files examined)
- Testing procedures (how to verify fix works)
- Effort estimates (time and complexity)
- Impact analysis (benefit, risk, scope)

**No aspirational content:**
- ❌ "We should probably add validation" (vague)
- ✅ "Add context file validation to Phase 0, Step 8" (specific)
- ❌ "Improve error handling" (aspirational)
- ✅ "Add error message with file list and /create-context suggestion" (actionable)

---

## Skill Workflow (8 Phases)

The spec-driven-rca skill executes:

1. **Phase 0:** Issue Clarification - Extract details, generate RCA number/title
2. **Phase 1:** Auto-Read Files - Read skills, commands, subagents, context files
3. **Phase 2:** 5 Whys Analysis - Progressive questioning to root cause
4. **Phase 3:** Evidence Collection - Organize excerpts, validate context files
5. **Phase 4:** Recommendation Generation - Prioritized fixes (CRITICAL → LOW)
6. **Phase 5:** RCA Document Creation - Write to devforgeai/RCA/RCA-XXX-slug.md
7. **Phase 6:** Validation & Self-Check - Verify completeness, self-heal issues
8. **Phase 7:** Completion Report - Return summary to command

---

## Error Handling Details

### Missing Argument
**Error:** User runs `/rca` with no arguments
**Recovery:** AskUserQuestion for issue description → extract → proceed

### Invalid Severity
**Error:** User provides invalid severity value
**Recovery:** AskUserQuestion with CRITICAL/HIGH/MEDIUM/LOW options → extract valid severity → proceed

### Skill Execution Failure
**Error:** spec-driven-rca skill fails during execution
**Recovery:**
```
Display skill error message
Guidance:
  - Read skill output for details
  - Verify issue description was clear
  - Check if affected component exists
  - Retry with more specific description
```

### RCA Document Already Exists
**Error:** RCA file with same name already exists
**Recovery:** Skill auto-increments RCA number. No user action needed.

---

## Examples

### Example 1: Skill Breakdown

```bash
$ /rca "spec-driven-dev didn't validate context files before TDD" CRITICAL

✓ Issue: spec-driven-dev didn't validate context files before TDD
✓ Severity: CRITICAL
✓ Proceeding with RCA analysis...

[Skill executes 8 phases...]

═══════════════════════════════════════════════
RCA COMPLETE: RCA-010
═══════════════════════════════════════════════

Title: Context File Validation Missing
Severity: CRITICAL
File: devforgeai/RCA/RCA-010-context-file-validation-missing.md

ROOT CAUSE:
No pre-flight validation in development skill enforces context file existence before TDD begins

RECOMMENDATIONS:
- CRITICAL: 1 (implement immediately)
- HIGH: 2 (implement this sprint)
- MEDIUM: 1 (next sprint)
- LOW: 0 (backlog)

NEXT STEPS:
Review CRITICAL recommendations immediately. Create story for implementation if substantial work (>2 hours).

Read complete RCA: devforgeai/RCA/RCA-010-context-file-validation-missing.md

═══════════════════════════════════════════════
```

### Example 2: Command Breakdown

```bash
$ /rca "/qa command has business logic in Phase 2"

✓ Issue: /qa command has business logic in Phase 2
✓ Severity: infer
✓ Proceeding with RCA analysis...

[Skill infers severity as HIGH from "business logic" keyword]
[Skill executes 8 phases...]

═══════════════════════════════════════════════
RCA COMPLETE: RCA-011
═══════════════════════════════════════════════

Title: QA Command Business Logic Violation
Severity: HIGH
File: devforgeai/RCA/RCA-011-qa-command-business-logic-violation.md

ROOT CAUSE:
Command contains report parsing and display logic that should be in skill or subagent (lean orchestration violation)

RECOMMENDATIONS:
- CRITICAL: 0
- HIGH: 3 (implement this sprint)
- MEDIUM: 1 (next sprint)
- LOW: 1 (backlog)

NEXT STEPS:
Review HIGH recommendations. Plan implementation in current sprint.

Read complete RCA: devforgeai/RCA/RCA-011-qa-command-business-logic-violation.md

═══════════════════════════════════════════════
```

---

## Integration Pattern

**Typical RCA workflow:**

```
1. User encounters framework breakdown
   ↓
2. User runs: /rca "[issue description]" [severity]
   ↓
3. Command validates arguments
   ↓
4. Command sets context markers
   ↓
5. Command invokes: Skill(command="spec-driven-rca")
   ↓
6. Skill performs 8-phase RCA workflow (isolated context)
   ↓
7. Skill generates RCA document in devforgeai/RCA/
   ↓
8. Skill returns completion report
   ↓
9. Command displays report to user
   ↓
10. User reads full RCA document
    ↓
11. User implements CRITICAL recommendations
    ↓
12. User creates story for substantial work (>2 hours)
    ↓
13. User commits RCA and fixes to git
```

---

## Related Commands

**Framework Analysis:**
- `/audit-deferrals` - Audit deferred work in stories
- `/audit-budget` - Audit command character budgets

**Framework Development:**
- `/create-story` - Create implementation stories for RCA recommendations
- `/dev` - Implement RCA recommendations via TDD

**Framework Documentation:**
- Commands reference: `.claude/memory/commands-reference.md`
- Skills reference: `.claude/memory/skills-reference.md`
- Framework overview: `CLAUDE.md`

---

## Performance

| Component | Tokens |
|-----------|--------|
| Command overhead | ~3K |
| Skill execution (isolated) | ~50-80K |
| Total main conversation | ~3K |

**Execution Time:** Simple RCA 3-5 min, Complex RCA 5-10 min
