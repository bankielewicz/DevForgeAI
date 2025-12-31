---
name: create-stories-from-rca
description: Parse RCA documents and extract recommendations for story creation. Filters by effort threshold and sorts by priority.
argument-hint: RCA-NNN [--threshold HOURS]
---

# /create-stories-from-rca - RCA Document Parser

Parse RCA markdown files, extract structured recommendation data, and interactively select which recommendations to convert to user stories.

**Interactive Selection Flow:**
1. Parse RCA document and extract recommendations (Phases 1-4)
2. Display recommendation summary table with REC ID, Priority, Title, Effort (Phase 6)
3. Prompt user to select recommendations using multiSelect (Phase 7)
4. Handle selection: All, Individual, or Cancel (Phase 8)
5. Pass selected recommendations to batch story creation (Phase 9-10)

---

## Usage

```bash
/create-stories-from-rca RCA-NNN [--threshold HOURS]

# Examples:
/create-stories-from-rca RCA-022
/create-stories-from-rca RCA-022 --threshold 2
```

---

## Constants and Enums

```
VALID_PRIORITIES = [CRITICAL, HIGH, MEDIUM, LOW]
PRIORITY_ORDER = {CRITICAL: 0, HIGH: 1, MEDIUM: 2, LOW: 3}
DEFAULT_PRIORITY = "MEDIUM"
VALID_STATUSES = [OPEN, IN_PROGRESS, RESOLVED]
DEFAULT_STATUS = "OPEN"
STORY_POINTS_TO_HOURS = 4  # BR-003: 1 story point = 4 hours
```

---

## Argument Parsing

```
RCA_ID = extract from arguments matching "RCA-[0-9]+"
EFFORT_THRESHOLD = extract from --threshold flag (default: 0)

IF RCA_ID empty:
    Display: "Usage: /create-stories-from-rca RCA-NNN [--threshold HOURS]"
    HALT
```

---

## Phase Overview

| Phase | Description | Reference |
|-------|-------------|-----------|
| 1-5 | RCA Parsing Workflow | `references/create-stories-from-rca/parsing-workflow.md` |
| 6-9 | Interactive Selection | `references/create-stories-from-rca/selection-workflow.md` |
| 10 | Batch Story Creation | `references/create-stories-from-rca/batch-creation-workflow.md` |
| 11 | RCA-Story Linking (STORY-158) | Inline (below) |

---

## Phase 1-5: RCA Parsing (Summary)

**For detailed workflow, see:** `references/create-stories-from-rca/parsing-workflow.md`

1. **Phase 1 - Locate RCA File**: `Glob(pattern="devforgeai/RCA/${RCA_ID}*.md")`
2. **Phase 2 - Parse Frontmatter (AC#1)**: Extract id, title, date, severity, status, reporter
3. **Phase 3 - Extract Recommendations (AC#2, AC#3, AC#4)**: Parse `### REC-N:` sections with priority, effort, success criteria
4. **Phase 4 - Filter/Sort (AC#5)**: Apply effort threshold (BR-001), sort by priority (BR-002)
5. **Phase 5 - Display Results**: Show parsed RCA document and recommendations

---

## Phase 6-9: Interactive Selection (Summary)

**For detailed workflow, see:** `references/create-stories-from-rca/selection-workflow.md`

### Phase 6: Display Summary Table (AC#1)

```
┌─────────┬──────────┬────────────────────────────────────┬────────┐
│ REC ID  │ Priority │ Title                              │ Effort │
├─────────┼──────────┼────────────────────────────────────┼────────┤
│ REC-1   │ HIGH     │ Fix Database Connection            │    8h  │
└─────────┴──────────┴────────────────────────────────────┴────────┘
```

### Phase 7: Interactive Selection (AC#2, AC#3, AC#4)

```
AskUserQuestion(
    questions=[{
        question: "Which recommendations should be converted to stories?",
        multiSelect: true,
        options: ["All recommendations", "REC-1: {title}", "None - cancel"]
    }]
)
```

### Phase 8: Handle Selection

- **"None - cancel"**: Exit gracefully, display "No recommendations selected"
- **"All recommendations"**: Select all eligible recommendations
- **Individual selections**: Map REC IDs to recommendations

### Phase 9: Pass to Batch Creation

```
batch_input = {
    rca_document: {id, title, severity},
    selected_recommendations: [...],
    selection_count: N
}
```

---

## Phase 10: Batch Story Creation (STORY-157)

**For detailed workflow, see:** `references/create-stories-from-rca/batch-creation-workflow.md`

### AC#1: Map Recommendation Fields to Story Batch Markers

```
batch_context = {
    story_id: get_next_story_id(),      # Sequential STORY-NNN
    epic_id: rca_document.epic_id,
    feature_name: recommendation.title,
    feature_description: recommendation.description,
    priority: map_priority(recommendation.priority),  # CRITICAL/HIGH -> High
    points: recommendation.effort_points OR 5,
    type: "feature",
    sprint: selected_sprint OR "Backlog",
    batch_mode: true,
    source_rca: rca_document.id,
    source_recommendation: recommendation.id
}
```

### AC#2: Invoke Story Creation Skill in Batch Mode

```
# Phase 1 (interactive questions) is SKIPPED in batch mode
# Phases 2-7 execute normally
Skill(command="devforgeai-story-creation", args="--batch")
```

### AC#3: Sequential Processing with Progress Display

```
FOR recommendation in selected_recommendations:
    Display: "[${current}/${total}] Creating: ${recommendation.title}"
    batch_context = map_recommendation_to_batch_markers(recommendation)
    result = invoke_story_creation_batch(batch_context)
    IF result.success:
        Display: "  ✓ Created: ${batch_context.story_id}"
    ELSE:
        Display: "  ✗ Failed: ${result.error_message}"
        # BR-004: Continue to next (failure isolation)
```

### AC#4: Handle Story Creation Failure

Failures are tracked in a failed_stories array for the final report.

| Error Type | Handling | Recovery |
|------------|----------|----------|
| Validation Error | Log, add to failed_stories | Continue to next |
| Skill Invocation Error | Log, add to failed_stories | Continue to next |
| Story ID Conflict | Increment ID, retry once | Fail if still conflicts |

### AC#5: Report Success and Failure Summary

After all recommendations have been processed, display completion summary:

```
Display: "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
Display: "  Batch Story Creation Summary"
Display: "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
Display: "✅ Created: ${success_count} stories"
FOR story in created_stories:
    Display: "   • ${story.story_id}: ${story.feature_title}"
Display: "❌ Failed: ${failure_count} stories"
FOR failure in failed_stories:
    Display: "   • ${failure.feature_title}"
    Display: "     Reason: ${failure.error_message}"
```

---

## Phase 11: RCA-Story Linking (STORY-158)

**Entry Gate:**
```bash
devforgeai-validate phase-check ${RCA_ID} --from=10 --to=11

# Exit code 0: Transition allowed
# Exit code 1: Phase 10 not complete - HALT
# Exit code 2: No created stories from Phase 10 - HALT (no linking needed)
```

---

## Phase Workflow

**Purpose:** Update RCA document with story references for traceability and change implementation status

**Input:** `created_stories` array from Phase 10 with mapping of REC-ID → STORY-ID

**Steps:**

1. **Update Implementation Checklist (AC#1)**
   ```
   FOR story in created_stories:
       rec_id = story.source_recommendation  # e.g., "REC-1"
       story_id = story.story_id              # e.g., "STORY-155"

       # Check idempotency - skip if already linked (BR-002)
       IF RCA_FILE contains "- [ ] ${rec_id}: See STORY-":
           Display: "  ⚠ ${rec_id} already linked, skipping"
           CONTINUE

       # Update checklist line
       Edit(
           file_path="${RCA_FILE}",
           old_string="- [ ] ${rec_id}",
           new_string="- [ ] ${rec_id}: See ${story_id}"
       )
       Display: "  ✓ Updated checklist: ${rec_id} → ${story_id}"
   ```

2. **Add Inline Story References (AC#2)**
   ```
   FOR story in created_stories:
       rec_id = story.source_recommendation
       story_id = story.story_id

       # Find recommendation section header (Pattern: "### REC-N: Title")
       header_pattern = "### ${rec_id}:"

       # Check idempotency - skip if already has inline reference
       IF RCA_FILE contains "**Implemented in:** ${story_id}" after header_pattern:
           Display: "  ⚠ Inline reference exists for ${rec_id}, skipping"
           CONTINUE

       # Get the full header line (includes title)
       header_line = Grep(pattern="^### ${rec_id}:.*$", path="${RCA_FILE}")

       # Add inline reference after header
       Edit(
           file_path="${RCA_FILE}",
           old_string="${header_line}",
           new_string="${header_line}\n**Implemented in:** ${story_id}"
       )
       Display: "  ✓ Added inline reference: ${rec_id} → ${story_id}"
   ```

3. **Preserve Original Content (AC#3)**
   - Edit tool performs atomic string replacement
   - Only target strings are modified
   - All other content (Five Whys, Evidence, descriptions) preserved unchanged
   - No full file rewrites

4. **Handle Partial Story Creation (AC#4)**
   ```
   # Only process created_stories array
   # failed_stories array is NOT processed
   # Recommendations without stories remain unmarked

   linked_count = len(created_stories)
   unlinked_count = len(failed_stories)

   Display: "Linking Summary:"
   Display: "  ✓ Linked: ${linked_count} recommendations"
   Display: "  ○ Unlinked: ${unlinked_count} recommendations (story creation failed)"
   ```

5. **Update RCA Status Field (AC#5)**
   ```
   total_recommendations = len(created_stories) + len(failed_stories)

   IF len(created_stories) == total_recommendations:
       # All recommendations have stories - update status
       Edit(
           file_path="${RCA_FILE}",
           old_string="status: OPEN",
           new_string="status: IN_PROGRESS"
       )
       Display: "  ✓ RCA status updated: OPEN → IN_PROGRESS"
   ELSE:
       # Partial completion - keep status as OPEN
       Display: "  ○ RCA status unchanged (partial completion: ${len(created_stories)}/${total_recommendations})"
   ```

6. **Display RCA-Story Linking Summary**
   ```
   Display: ""
   Display: "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
   Display: "  RCA-Story Linking Complete"
   Display: "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
   Display: "  RCA Document: ${RCA_ID}"
   Display: "  Linked: ${linked_count} recommendations"
   Display: "  Status: ${new_status}"
   Display: ""
   Display: "  Traceability established:"
   FOR story in created_stories:
       Display: "    ${story.source_recommendation} → ${story.story_id}"
   Display: "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
   ```

**Business Rules for RCA-Story Linking (AC#6):**

| Rule | Implementation |
|------|----------------|
| BR-001: Traceability | Each story linked to source RCA via `source_rca` and `source_recommendation` fields |
| BR-002: Idempotency | Check for existing `: See STORY-` before adding link (no duplicates) |
| BR-003: Partial Linking | Only link recommendations in `created_stories` array; `failed_stories` remain unmarked |
| BR-004: Status Transition | RCA status → IN_PROGRESS only when ALL recommendations have stories |

**Reference:** `references/create-stories-from-rca/linking-workflow.md` for detailed workflow

---

## Validation Checkpoint

**Before proceeding to Phase 12 (or workflow completion), verify:**

- [ ] Checklist items updated for all created stories (AC#1)
- [ ] Inline references added for all created stories (AC#2)
- [ ] Original RCA content preserved (AC#3)
- [ ] Partial linking handled correctly (AC#4)
- [ ] RCA status field updated appropriately (AC#5)
- [ ] Summary display generated

**IF any checkbox UNCHECKED:** HALT workflow

---

## Observation Capture

**Before exiting this phase, reflect:**
1. Did I encounter any friction? (unclear docs, missing tools, workarounds)
2. Did anything work particularly well? (constraints that helped, patterns that fit)
3. Did I notice any repeated patterns?
4. Are there gaps in tooling/docs?
5. Did I discover any bugs?

**If YES to any:** Append to phase-state.json `observations` array:
```json
{
  "id": "obs-11-{seq}",
  "phase": "11",
  "category": "{friction|success|pattern|gap|idea|bug}",
  "note": "{1-2 sentence description}",
  "files": ["{relevant files}"],
  "severity": "{low|medium|high}"
}
```

**Reference:** `references/observation-capture.md`

---

**Exit Gate:**
```bash
devforgeai-validate phase-complete ${RCA_ID} --phase=11 --checkpoint-passed

# Exit code 0: Phase complete, RCA document updated with story links
# Exit code 1: Cannot complete - edit operations failed
```

---

## Business Rules

| Rule | Implementation |
|------|----------------|
| BR-001: Effort Threshold | Filter where effort_hours >= threshold |
| BR-002: Priority Sorting | CRITICAL(0) > HIGH(1) > MEDIUM(2) > LOW(3) |
| BR-003: Story Point Conversion | 1 story point = 4 hours |
| BR-004: Failure Isolation | Failure in story N does not affect story N+1 |

---

## Business Rules for Batch Story Creation (STORY-157)

| Rule | Implementation |
|------|----------------|
| BR-001: Priority Mapping | CRITICAL/HIGH -> High, MEDIUM -> Medium, LOW -> Low |
| BR-002: Points Calculation | Use recommendation.effort_points OR default to 5 |
| BR-003: Story ID Generation | Sequential STORY-NNN (no gaps in numbering) |
| BR-004: Failure Isolation | Each story creation is independent, failures logged and skipped |

---

## Edge Cases

| Edge Case | Behavior |
|-----------|----------|
| Missing frontmatter | Extract ID from filename, log warning |
| No recommendations | Return empty array, display message |
| Missing effort estimate | Return null for effort_hours |
| Malformed priority | Default to MEDIUM, log warning |
| All filtered out | Display "No recommendations meet effort threshold" |
| Invalid REC ID | Log warning and ignore invalid entries |

---

## Error Handling

| Error Type | Handling | Recovery |
|------------|----------|----------|
| Validation Error | Log error, add to failed_stories | Continue to next |
| Skill Invocation Error | Log error, add to failed_stories | Continue to next |
| Story ID Conflict | Increment ID, retry once | Fail if still conflicts |
| Context Window Limit | Process in batches of 5 | Automatic batching |

**Key Principle:** BR-004 ensures that a failure creating story N does not prevent or affect the creation of story N+1.

---

## Return Value

```json
{
  "rca_document": {
    "id": "RCA-NNN",
    "title": "string",
    "recommendations": [...]
  },
  "selected_recommendations": [...],
  "selection_count": "integer",
  "selection_mode": "all|individual|cancel"
}
```

---

## Non-Functional Requirements

| Requirement | Implementation |
|-------------|----------------|
| Performance <500ms | Single file read, in-memory parsing |
| Zero external deps | Uses only Read, Glob, Grep (Claude Code native) |
| Graceful degradation | Warnings for malformed data, no exceptions |

---

## Reference Files

For detailed pseudocode and implementation:

- **Parsing Workflow**: `references/create-stories-from-rca/parsing-workflow.md`
- **Selection Workflow**: `references/create-stories-from-rca/selection-workflow.md`
- **Batch Creation Workflow**: `references/create-stories-from-rca/batch-creation-workflow.md`
