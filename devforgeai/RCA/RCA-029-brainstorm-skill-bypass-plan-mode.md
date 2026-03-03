# RCA-029: Brainstorm Skill Bypass During Plan Mode

**Date:** 2026-01-26
**Reporter:** User
**Component:** /brainstorm command
**Severity:** HIGH

---

## Issue Description

When user invoked `/brainstorm "why am I not seeing any feedback..."`, Claude did NOT invoke the `devforgeai-brainstorming` skill as required by the command specification. Instead, Claude:

1. Performed manual exploratory research using Explore subagents
2. Wrote findings to the Plan Mode plan file
3. Created a brainstorm document manually with incorrect naming: `BRAINSTORM-FEEDBACK-001.md`

**Expected behavior:** Command should invoke `Skill(command="devforgeai-brainstorming")` which executes a 7-phase interactive workflow

**Actual behavior:** Skill was never invoked; manual document created with wrong naming convention

**Impact:**
- Brainstorm document doesn't follow framework naming convention
- 7-phase discovery workflow was bypassed
- Document lacks structured sections required by /ideate
- User didn't get the interactive brainstorming experience

---

## 5 Whys Analysis

### Problem Statement
/brainstorm command invoked but devforgeai-brainstorming skill NOT called

### Why #1: Why did Claude not invoke the devforgeai-brainstorming skill?
**Answer:** Claude was in Plan Mode when /brainstorm was invoked. Plan Mode restrictions state "you MUST NOT make any edits... This supercedes any other instructions."

**Evidence:** Conversation contained `<system-reminder>Plan mode is active...</system-reminder>` throughout session.

### Why #2: Why did Plan Mode prevent skill invocation?
**Answer:** The Skill tool invokes an interactive 7-phase workflow that asks questions and writes files. Plan Mode restricts all write operations except to the plan file.

**Evidence:** From devforgeai-brainstorming SKILL.md (line 593):
```
Write(
  file_path="devforgeai/specs/brainstorms/${brainstorm_id}-${short_name}.brainstorm.md",
  ...
)
```

### Why #3: Why did Claude proceed to create a brainstorm document manually?
**Answer:** Claude interpreted the request as "perform research about feedback visibility" rather than "execute formal /brainstorm workflow." The topic sounded like an investigation task.

**Evidence:** Claude used Explore subagents for research, then offered to "export brainstorm findings" - conflating research with formal brainstorming.

### Why #4: Why did Claude conflate research with formal brainstorming?
**Answer:** The /brainstorm command documentation doesn't explicitly state Plan Mode incompatibility. The command describes itself as "transform vague business problems into structured brainstorm documents" which sounds like research.

**Evidence:** From brainstorm.md (lines 8-10):
```
# /brainstorm - Business Analyst Discovery Session

Transform vague business problems into structured, AI-consumable brainstorm documents
```

### Why #5: ROOT CAUSE
**Answer:** **ROOT CAUSE:** The /brainstorm command lacks Plan Mode incompatibility detection. When invoked in Plan Mode, the command should HALT and inform the user, or exit Plan Mode first.

**Evidence:** The command has no Phase 0 pre-flight check for Plan Mode compatibility. Compare to /dev command which has extensive pre-flight validation.

---

## Evidence Collected

### Files Examined

#### `.claude/commands/brainstorm.md` (All lines)
- **Finding:** No Plan Mode compatibility check exists
- **Significance:** CRITICAL - Command allows invocation in incompatible mode
- **Excerpt (lines 60-74):**
```markdown
### Phase 2: Invoke Skill

Display:
"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  DevForgeAI Brainstorming Session
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Mode: ${MODE}
Topic: ${TOPIC || 'To be discovered'}

Delegating to devforgeai-brainstorming skill..."

Skill(command="devforgeai-brainstorming")
```

#### `.claude/skills/devforgeai-brainstorming/SKILL.md` (770 lines)
- **Finding:** Skill writes files and asks questions - incompatible with Plan Mode
- **Significance:** HIGH - Explains why skill couldn't execute
- **Excerpt (lines 591-598):**
```markdown
3. **Create brainstorm document:**
   Write(
     file_path="devforgeai/specs/brainstorms/${brainstorm_id}-${short_name}.brainstorm.md",
     content=BRAINSTORM_TEMPLATE with all values
   )
```

#### `devforgeai/specs/brainstorms/BRAINSTORM-FEEDBACK-001.md`
- **Finding:** Incorrect filename format
- **Significance:** HIGH - Naming convention violated
- **Expected:** `BRAINSTORM-007-feedback-visibility.brainstorm.md`
- **Actual:** `BRAINSTORM-FEEDBACK-001.md`

#### Existing Brainstorms (BRAINSTORM-001 through 006)
- **Finding:** All follow `BRAINSTORM-NNN-{slug}.brainstorm.md` pattern
- **Significance:** HIGH - Establishes the correct naming convention

### Naming Convention Comparison

| Correct Format | Incorrect File |
|----------------|----------------|
| `BRAINSTORM-001-ideate-improvements.brainstorm.md` | |
| `BRAINSTORM-002-phase-execution-enforcement.brainstorm.md` | |
| `BRAINSTORM-003-devforgeai-project-manager.brainstorm.md` | |
| `BRAINSTORM-004-agent-skills-compliance.brainstorm.md` | |
| `BRAINSTORM-005-spec-compliance-100-percent.brainstorm.md` | |
| `BRAINSTORM-006-technical-debt-automation.brainstorm.md` | |
| Expected: `BRAINSTORM-007-feedback-visibility.brainstorm.md` | Actual: `BRAINSTORM-FEEDBACK-001.md` |

---

## Recommendations

### CRITICAL Priority

#### REC-1: Add Plan Mode Detection to /brainstorm Command

**Problem:** Command invoked in Plan Mode which is incompatible with skill execution

**Solution:** Add Phase 0 pre-flight check

**File:** `.claude/commands/brainstorm.md`
**Location:** Before Phase 0: Argument Parsing
**Add:**

```markdown
### Pre-Flight: Plan Mode Check

```
IF plan_mode_active:
  Display:
  "⚠️ /brainstorm cannot run in Plan Mode.

  The brainstorming workflow requires:
  - Interactive questions (AskUserQuestion)
  - File creation (Write)
  - Skill invocation (Skill)

  These are blocked by Plan Mode restrictions.

  Options:
  1. Exit Plan Mode first, then run /brainstorm
  2. Use ExitPlanMode to request plan approval, then restart

  Command aborted."

  EXIT
```
```

**Rationale:** Plan Mode explicitly blocks file writes. Early detection prevents confusion.

**Testing:**
1. Enter Plan Mode
2. Run `/brainstorm "test"`
3. Verify error message displays
4. Verify skill NOT invoked
5. Exit Plan Mode, retry - should work

**Effort:** 15 minutes

---

### HIGH Priority

#### REC-2: Rename Incorrectly Created Brainstorm File

**Problem:** File violates naming convention

**Solution:** Rename to correct format

**Action:**
```bash
mv devforgeai/specs/brainstorms/BRAINSTORM-FEEDBACK-001.md \
   devforgeai/specs/brainstorms/BRAINSTORM-007-feedback-visibility.brainstorm.md
```

**Effort:** 5 minutes

---

#### REC-3: Document Plan Mode Incompatibility in SKILL.md

**Problem:** Skill doesn't indicate Plan Mode incompatibility

**File:** `.claude/skills/devforgeai-brainstorming/SKILL.md`
**Location:** Prerequisites section (lines 25-29)
**Add:**

```markdown
4. **NOT in Plan Mode** - This skill requires file writes and interactive questions which are blocked in Plan Mode
```

**Effort:** 5 minutes

---

### MEDIUM Priority

#### REC-4: Add Filename Validation to Brainstorm Skill

**Problem:** Manual file creation can bypass naming convention

**File:** `.claude/skills/devforgeai-brainstorming/SKILL.md`
**Location:** Phase 7, Step 3 (line 591)
**Add validation before Write:**

```markdown
# Validate filename format
filename_pattern = "BRAINSTORM-{NNN}-{slug}.brainstorm.md"

IF NOT filename matches pattern:
  HALT: "Invalid filename format. Expected: ${filename_pattern}"
```

**Effort:** 30 minutes

---

## Implementation Checklist

- [ ] Implement REC-1: Add Plan Mode check to /brainstorm command
- [ ] Implement REC-2: Rename BRAINSTORM-FEEDBACK-001.md
- [ ] Implement REC-3: Document Plan Mode incompatibility in skill
- [ ] Implement REC-4: Add filename validation (optional)
- [ ] Review this RCA for completeness
- [ ] Commit changes with reference to RCA-029
- [ ] Mark RCA as RESOLVED

---

## Prevention Strategy

### Short-term
- Add Plan Mode compatibility checks to commands that invoke skills
- Commands affected: /brainstorm, /ideate, /create-context, /create-epic, /create-story

### Long-term
- Create standardized pre-flight validation pattern for all commands
- Add automated test that verifies commands check for Plan Mode when they invoke skills
- Consider having Plan Mode system prompt auto-block skill invocations

### Monitoring
- Watch for: Files created outside of skill workflows
- Audit for: Incorrect naming conventions in brainstorms/epics/stories
- Escalation: If naming violations found, trace to determine if skill was bypassed

---

## Related RCAs

- **RCA-022:** Mandatory TDD Phases Skipped - Similar pattern of phase bypass
- **RCA-027:** Phase 09 Feedback Skipped - Similar workflow skip pattern

---

## Status

**Status:** OPEN
**Resolution:** Pending implementation of recommendations
