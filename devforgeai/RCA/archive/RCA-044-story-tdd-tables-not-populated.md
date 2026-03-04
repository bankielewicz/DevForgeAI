# RCA-044: Story TDD Tables Not Populated

| Field | Value |
|-------|-------|
| **RCA Number** | RCA-044 |
| **Title** | Story TDD Tables Not Populated |
| **Date** | 2026-02-28 |
| **Reporter** | User |
| **Severity** | MEDIUM |
| **Affected Component** | implementing-stories skill (Phase 07) |
| **Status** | OPEN |

---

## Issue Description

**What happened:** The TDD Workflow Summary and Files Created/Modified tables in story files are not being populated during /dev workflow execution. Empty template tables remain in the final committed story files.

**When:** Observed in STORY-513, STORY-514, and STORY-515 (the initial template portion).

**Where:** Story file `## Implementation Notes` section, specifically:
- `### TDD Workflow Summary` table (Phase/Status/Details columns)
- `### Files Created/Modified` table (File/Action/Lines columns)

**Expected:** Tables should be populated with actual TDD phase results and file modification records during the /dev workflow.

**Actual:** Tables remain empty with only header rows after story reaches Dev Complete status.

**Impact:** Loss of traceability — story files don't record which phases completed, what tests ran, or which files were modified. This information is available in phase-state.json but not in the human-readable story artifact.

---

## 5 Whys Analysis

**Issue Statement:** TDD Workflow Summary and Files Created/Modified tables in story files are empty after /dev workflow completion.

### Why #1: Why are the tables empty?

**Answer:** The orchestrator did not populate them during Phase 07 (DoD Update) or any other phase.

**Evidence:**
- `devforgeai/specs/Stories/STORY-513-move-snapshot-before-validation-checkpoint.story.md` lines 347-358 — empty tables
- `devforgeai/specs/Stories/STORY-514-snapshot-file-existence-verification.story.md` lines 309-318 — empty tables

### Why #2: Why didn't the orchestrator populate them?

**Answer:** Phase 07 (`phase-07-dod-update.md`) contains no instruction to populate these tables. Its 5 workflow steps focus exclusively on DoD checkbox management, Implementation Notes format compliance, Change Log updates, and format validation. TDD tables are not addressed.

**Evidence:**
- `.claude/skills/implementing-stories/phases/phase-07-dod-update.md` lines 36-78 — Steps 1-5 have no table population instructions
- Line 99 mentions `### TDD Workflow Summary (optional subsection OK)` only as a format comment

### Why #3: Why does Phase 07 not include table population instructions?

**Answer:** The reference file `dod-update-workflow.md` marks TDD Workflow Summary as "Optional but Recommended" (Step 5), and the phase file never surfaces this optional step as a mandatory action.

**Evidence:**
- `.claude/skills/implementing-stories/references/dod-update-workflow.md` line 304: `## Step 5: Add TDD Workflow Summary (Optional but Recommended)`
- Phase 07 phase file loads the reference but doesn't enforce Step 5

### Why #4: Why is populating these tables marked optional?

**Answer:** There is a design disconnect between the story template (which creates empty placeholder tables implying they will be filled) and the Phase 07 workflow (which was designed around pre-commit hook compliance, not comprehensive documentation).

**Evidence:**
- `.claude/skills/devforgeai-story-creation/assets/templates/story-template.md` lines 968-977 — creates placeholder tables
- Phase 07 design priority was DoD format validation (preventing commit failures), not documentation completeness

### Why #5 (ROOT CAUSE):

**ROOT CAUSE:** The story template added TDD Workflow Summary and Files Created/Modified tables as documentation placeholders, but no corresponding **mandatory** workflow step was created in Phase 07 to ensure they get populated. The "Optional but Recommended" label in the reference file does not create enforcement — the orchestrator treats optional steps as skippable, especially under token pressure.

---

## Evidence Collected

### Files Examined

**`.claude/skills/implementing-stories/phases/phase-07-dod-update.md`** (CRITICAL)
- Lines: 1-191 (entire file)
- Finding: No step instructs table population. Steps 1-5 focus on DoD checkboxes, Implementation Notes flat list, format validation, Change Log, and final validation.
- Significance: This is the phase file the orchestrator reads — if it's not here, it doesn't happen.

**`.claude/skills/implementing-stories/references/dod-update-workflow.md`** (HIGH)
- Lines: 304-359 (Step 5)
- Finding: Step 5 labeled "Optional but Recommended" with full template for TDD Workflow Summary and Files Created/Modified tables.
- Significance: The instructions exist but are marked optional, meaning the orchestrator can skip them without violation.

**`.claude/skills/devforgeai-story-creation/assets/templates/story-template.md`** (HIGH)
- Lines: 968-977
- Finding: Template creates empty tables with headers, creating expectation they will be populated during development.
- Significance: User expects tables to be filled because the template creates them.

**`devforgeai/specs/Stories/STORY-513-move-snapshot-before-validation-checkpoint.story.md`** (MEDIUM)
- Lines: 347-358
- Finding: Empty TDD Workflow Summary and Files Created/Modified tables in completed story.

**`devforgeai/specs/Stories/STORY-514-snapshot-file-existence-verification.story.md`** (MEDIUM)
- Lines: 309-318
- Finding: Same pattern — empty tables in completed story.

### Context Files Status

Not directly relevant to this issue (no context file constraint violation).

---

## Recommendations

### REC-1: Add Mandatory Table Population Step to Phase 07 (HIGH)

**Problem Addressed:** Phase 07 has no instruction to populate TDD Workflow Summary and Files Created/Modified tables.

**Proposed Solution:** Add a new Step 4.5 (between Step 4 Change Log and Step 5 Final Validation) to phase-07-dod-update.md that mandates populating both tables from phase-state.json data and observed file changes.

**Implementation Details:**
- **File:** `.claude/skills/implementing-stories/phases/phase-07-dod-update.md`
- **Section:** After Step 4 (Update Workflow Status), before Step 5 (Final Validation)
- **Change Type:** Add

**Code to Add (after line 72 in phase-07-dod-update.md):**

```markdown
4.5. **Populate TDD Workflow Summary and Files tables**
   ```
   # Read phase-state.json for phase completion data
   Read(file_path="devforgeai/workflows/${STORY_ID}-phase-state.json")

   # Update TDD Workflow Summary table with actual phase results
   Edit(
     file_path="${STORY_FILE}",
     old_string="| Phase | Status | Details |\n|-------|--------|---------|",
     new_string="| Phase | Status | Details |\n|-------|--------|---------|
| 01 Pre-Flight | ✅ Complete | {preflight_summary} |
| 02 Red | ✅ Complete | {test_count} tests, {failing_count} failing |
| 03 Green | ✅ Complete | {green_summary} |
| 04 Refactor | ✅ Complete | {refactor_summary} |
| 4.5 AC Verify | ✅ Complete | {ac_count} ACs verified |
| 05 Integration | ✅ Complete | {integration_summary} |
| 5.5 AC Verify | ✅ Complete | Post-integration verified |"
   )

   # Update Files Created/Modified table with actual file changes
   # Use git diff --name-status to get file changes
   Edit(
     file_path="${STORY_FILE}",
     old_string="| File | Action | Lines |\n|------|--------|-------|",
     new_string="| File | Action | Lines |\n|------|--------|-------|\n| {file1} | {action1} | {lines1} |\n..."
   )
   ```
```

**Rationale:** The story template creates these tables with the expectation they'll be populated. Making this step mandatory ensures documentation completeness without relying on orchestrator discretion. Data is available from phase-state.json and git diff.

**Testing:**
1. Run `/dev` on a test story
2. After Phase 07 completes, verify TDD Workflow Summary table has rows
3. Verify Files Created/Modified table has rows
4. Verify no format validation failures

**Effort Estimate:** Medium (1-2 hours including story creation, TDD, and testing)

**Implemented in:** STORY-516

**Impact:**
- Benefit: All story files will have complete development traceability
- Risk: Low — additional Edit operations in Phase 07
- Scope: phase-07-dod-update.md, dod-update-workflow.md

---

### REC-2: Change "Optional but Recommended" to "MANDATORY" in Reference File (MEDIUM)

**Problem Addressed:** dod-update-workflow.md Step 5 label allows orchestrator to skip table population.

**Proposed Solution:** Change Step 5 heading from "Optional but Recommended" to "MANDATORY" and move it before the final validation step.

**Implementation Details:**
- **File:** `.claude/skills/implementing-stories/references/dod-update-workflow.md`
- **Section:** Line 304
- **Change Type:** Modify

**Old Text:**
```
## Step 5: Add TDD Workflow Summary (Optional but Recommended)
```

**New Text:**
```
## Step 5: Populate TDD Workflow Summary and Files Tables [MANDATORY]
```

**Rationale:** Aligns the reference file with the phase file change from REC-1. Removes ambiguity about whether this step should be executed.

**Testing:** Verify reference file heading matches phase file instruction.

**Effort Estimate:** Low (15 minutes)

**Implemented in:** STORY-516 (combined with REC-1)

---

### REC-3: Backfill Empty Tables in STORY-513 and STORY-514 (LOW)

**Problem Addressed:** Existing completed stories have empty tables.

**Proposed Solution:** Backfill TDD Workflow Summary and Files Created/Modified tables in STORY-513 and STORY-514 from their phase-state.json files and git commit history.

**Implementation Details:**
- **Files:** STORY-513 and STORY-514 story files
- **Data Sources:** `devforgeai/workflows/STORY-513-phase-state.json`, `devforgeai/workflows/STORY-514-phase-state.json`, git log
- **Change Type:** Modify

**Rationale:** Restores documentation completeness for recently completed stories.

**Testing:** Verify tables populated with accurate data.

**Effort Estimate:** Low (30 minutes)

---

## Implementation Checklist

- [ ] Implement REC-1: Add mandatory table population step to Phase 07 — See STORY-516
- [ ] Implement REC-2: Change reference file label to MANDATORY — See STORY-516
- [ ] Implement REC-3: Backfill STORY-513 and STORY-514 tables
- [ ] Create story for REC-1 implementation (if >2 hours effort)
- [ ] Mark RCA-044 as RESOLVED after implementation

---

## Prevention Strategy

**Short-term:**
- Add mandatory Step 4.5 to Phase 07 for table population (REC-1)
- Update reference file label (REC-2)

**Long-term:**
- Consider adding pre-commit validation for table completeness (extend devforgeai-validate)
- Add template-to-workflow coverage audit to ensure all template placeholders have corresponding workflow steps

**Monitoring:**
- After REC-1 implementation, check next 3 stories for populated tables
- If tables still empty, investigate whether Phase 07 step is being skipped

---

## Related RCAs

- **RCA-003:** AC Checklist Workflow Not Enforced — similar pattern (workflow step existed but wasn't mandatory)
- **RCA-018:** Development Skill Phase Completion Skipping — related to phase steps being treated as optional
- **RCA-043:** Test Integrity Snapshot Skipped — same root pattern (optional steps get skipped under token pressure)

---

**RCA Status:** OPEN
**Created:** 2026-02-28
**Last Updated:** 2026-02-28
