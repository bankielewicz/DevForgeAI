# Phase 04: Validation & Quality Gates

## Entry Gate

```bash
devforgeai-validate phase-check ${SESSION_ID} --workflow=feedback --from=03 --to=04 --project-root=.
```

| Exit Code | Action |
|-----------|--------|
| 0 | Prerequisites met. Proceed. |
| 1 | Phase 03 incomplete. HALT. |
| 2 | Validation error. HALT. |
| 127 | CLI not installed. Proceed without enforcement. |

---

## Contract

- **PURPOSE:** Validate captured feedback data meets quality standards before persistence
- **REQUIRED SUBAGENTS:** none
- **REQUIRED ARTIFACTS:** Validated feedback data with schema check, content quality, field mappings, and cross-references confirmed
- **STEP COUNT:** 4
- **REFERENCE FILES:**
  - `.claude/skills/devforgeai-feedback/references/feedback-analysis-patterns.md`
  - `.claude/skills/devforgeai-feedback/references/field-mapping-guide.md`

---

## Reference Loading [MANDATORY]

```
Read(file_path=".claude/skills/devforgeai-feedback/references/feedback-analysis-patterns.md")
Read(file_path=".claude/skills/devforgeai-feedback/references/field-mapping-guide.md")
```

IF either Read fails: HALT -- "Phase 04 reference files not loaded. Cannot proceed without reference material."

Do NOT rely on memory of previous reads. Load ALL references fresh.

---

## Mandatory Steps (4)

### Step 4.1: Schema Validation

**EXECUTE:**
```
Validate feedback data against type-specific schema:

SWITCH $FEEDBACK_TYPE:
  CASE "conversation":
    REQUIRED: session-id, operation, status, timestamp, template-used
    REQUIRED: at least 1 content section with non-empty text

  CASE "summary":
    REQUIRED: session-id, operation, status, timestamp
    REQUIRED: sections "Operation Details", "Results", "Next Steps"

  CASE "metrics":
    REQUIRED: session_id, timestamp, operation_type, metrics object
    REQUIRED: at least 1 numeric metric in metrics object

  CASE "checklist":
    REQUIRED: session-id, timestamp, completion-percentage
    REQUIRED: at least 1 checklist item

  CASE "ai_analysis":
    REQUIRED: story_id, timestamp, ai_analysis object
    REQUIRED: what_worked_well, areas_for_improvement, recommendations arrays
    REQUIRED: each recommendation has title, description, effort_estimate, priority

  CASE "triage":
    REQUIRED: stories_created array (even if empty)
    REQUIRED: queue_updated boolean

  CASE "config", "search", "export", "import":
    REQUIRED: operation completed successfully (result displayed to user)
    # These types produce operational results, not feedback documents
    # Validation is lighter — confirm the operation succeeded
```

**VERIFY:** All required fields present and valid for the feedback type.
```
IF any required field is missing:
  Display: "Schema validation failed: missing {field_name}"
  HALT -- "Feedback data does not meet schema requirements"
```

**RECORD:**
```bash
devforgeai-validate phase-record ${SESSION_ID} --workflow=feedback --phase=04 --step=4.1 --project-root=.
```
Update checkpoint:
```
checkpoint.phases["04"].schema_valid = true
checkpoint.phases["04"].steps_completed.append("4.1")
```

---

### Step 4.2: Content Quality Check

**EXECUTE:**
```
SWITCH $FEEDBACK_TYPE:
  CASE "ai_analysis":
    # Aspirational language check
    aspirational_words = ["could", "might", "consider", "perhaps", "possibly", "maybe", "should consider"]
    FOR each recommendation in ai_analysis.recommendations:
      IF any aspirational_word found in recommendation.description:
        Rewrite to imperative form OR remove recommendation
        Log: "Removed aspirational language from recommendation: {title}"

    # Evidence check
    FOR each observation in what_worked_well + areas_for_improvement:
      IF observation.evidence is empty or null:
        Flag: "Missing evidence for observation: {observation text}"
        IF critical (areas_for_improvement): HALT
        IF non-critical (what_worked_well): warn and continue

  CASE "conversation":
    # Response quality check
    IF all responses are single-word or less than 10 characters:
      Log: "Low quality responses detected — may indicate user disengagement"
      # Do NOT halt — low quality is still valid data

  CASE "metrics":
    # Range check
    IF test_pass_rate < 0 OR test_pass_rate > 100: Fix to valid range
    IF execution_time_ms < 0: Set to 0

  CASE "checklist":
    # Completion percentage check
    IF completion_percentage < 0 OR completion_percentage > 100: Fix to valid range

  DEFAULT:
    # No additional quality checks for config/search/export/import
```

**VERIFY:** Content quality check completed. No HALT-worthy issues remain.

**RECORD:**
```bash
devforgeai-validate phase-record ${SESSION_ID} --workflow=feedback --phase=04 --step=4.2 --project-root=.
```
Update checkpoint:
```
checkpoint.phases["04"].quality_check_passed = true
checkpoint.phases["04"].steps_completed.append("4.2")
```

---

### Step 4.3: Field Mapping Validation

**EXECUTE:**
```
IF $FEEDBACK_TYPE in ["conversation", "summary", "checklist"]:
  # These types use template field mappings
  Load field mapping from field-mapping-guide.md

  FOR each template field in template.field-mappings:
    Check that feedback data has a corresponding content section
    IF unmapped: assign to "additional-feedback" section
    IF missing required mapping: log warning

  unmapped_count = count of fields without mappings
  missing_count = count of required mappings not found

ELSE:
  # Non-template types — no field mapping validation needed
  unmapped_count = 0
  missing_count = 0
```

**VERIFY:**
```
IF missing_count > 0 AND $FEEDBACK_TYPE requires template:
  Display: "{missing_count} required field mappings not found"
  # Do NOT halt — missing mappings are warnings, not blockers
unmapped fields assigned to "additional-feedback"
```

**RECORD:**
```bash
devforgeai-validate phase-record ${SESSION_ID} --workflow=feedback --phase=04 --step=4.3 --project-root=.
```
Update checkpoint:
```
checkpoint.phases["04"].field_mapping_valid = true
checkpoint.phases["04"].unmapped_fields = unmapped_count
checkpoint.phases["04"].steps_completed.append("4.3")
```

---

### Step 4.4: Cross-Reference Validation

**EXECUTE:**
```
# Verify referenced entities exist

IF $OPERATION_CONTEXT.story_id is not null:
  story_results = Glob(pattern="devforgeai/specs/Stories/${OPERATION_CONTEXT.story_id}*.story.md")
  IF not found:
    Log: "Referenced story ${OPERATION_CONTEXT.story_id} not found on disk"
    # Do NOT halt — story may have been archived or renamed

IF $FEEDBACK_TYPE == "triage" AND output.stories_created.length > 0:
  FOR each story_id in output.stories_created:
    story_results = Glob(pattern="devforgeai/specs/Stories/${story_id}*.story.md")
    IF not found:
      Log: "Created story ${story_id} not found on disk — may still be generating"

IF $FEEDBACK_TYPE == "ai_analysis":
  # Verify affected_files in recommendations exist
  FOR each recommendation in ai_analysis.recommendations:
    FOR each file_path in recommendation.affected_files:
      file_exists = Glob(pattern=file_path)
      IF not found:
        Log: "Affected file ${file_path} not found — recommendation may be stale"
```

**VERIFY:** Cross-reference validation completed (warnings logged but do not block).

**RECORD:**
```bash
devforgeai-validate phase-record ${SESSION_ID} --workflow=feedback --phase=04 --step=4.4 --project-root=.
```
Update checkpoint:
```
checkpoint.phases["04"].cross_reference_valid = true
checkpoint.phases["04"].status = "completed"
checkpoint.phases["04"].steps_completed.append("4.4")
checkpoint.progress.current_phase = 5
checkpoint.progress.phases_completed.append("04")
```
Write updated checkpoint to disk.

---

## Exit Gate

```bash
devforgeai-validate phase-complete ${SESSION_ID} --workflow=feedback --phase=04 --checkpoint-passed --project-root=.
```

---

## Exit Verification Checklist

Before proceeding to Phase 05, verify ALL:

- [ ] feedback-analysis-patterns.md loaded successfully
- [ ] field-mapping-guide.md loaded successfully
- [ ] Schema validation passed
- [ ] Content quality check passed
- [ ] Field mapping validation completed
- [ ] Cross-reference validation completed
- [ ] Checkpoint updated with phase 04 completion
- [ ] Checkpoint written to disk (verified via Glob)

**IF any criterion is unmet: HALT. Do NOT proceed to Phase 05.**

---

## Phase Transition Display

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Phase 04: Validation ✓
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Schema: Valid
  Quality: Passed
  Field Mappings: ${unmapped_count} unmapped
  Cross-References: Checked
  Steps: 4/4
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```
