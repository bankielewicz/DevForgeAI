# Phase 02: Type Dispatch & Preparation

## Entry Gate

```bash
devforgeai-validate phase-check ${SESSION_ID} --workflow=feedback --from=01 --to=02 --project-root=.
```

| Exit Code | Action |
|-----------|--------|
| 0 | Prerequisites met. Proceed. |
| 1 | Phase 01 incomplete. HALT. |
| 2 | Validation error. HALT. |
| 127 | CLI not installed. Proceed without enforcement. |

---

## Contract

- **PURPOSE:** Load type-specific references, select template, prepare execution parameters for the resolved feedback type
- **REQUIRED SUBAGENTS:** none
- **REQUIRED ARTIFACTS:** Type-specific references loaded, template selected, execution parameters prepared
- **STEP COUNT:** 4
- **REFERENCE FILES:** Varies by `$FEEDBACK_TYPE` — see Step 2.2 for conditional loading

---

## Reference Loading [MANDATORY - CONDITIONAL BY TYPE]

Load base references first, then type-specific references. The exact set depends on `$FEEDBACK_TYPE` resolved in Phase 01.

**Base references (always loaded):**
```
Read(file_path=".claude/skills/devforgeai-feedback/references/template-format-specification.md")
```

**Type-specific references — load based on $FEEDBACK_TYPE:**

| Feedback Type | References to Load |
|---------------|--------------------|
| conversation | `adaptive-questioning.md`, `feedback-question-templates.md` |
| summary | `feedback-persistence-guide.md` |
| metrics | `feedback-export-formats.md` |
| checklist | `feedback-question-templates.md` |
| ai_analysis | `feedback-analysis-patterns.md`, `feedback-question-templates.md` |
| triage | `triage-workflow.md` |
| config | `user-customization-guide.md` |
| search | `feedback-search-help.md` |
| export | `feedback-export-formats.md` |
| import | `feedback-export-formats.md` |

IF any Read fails: HALT -- "Phase 02 reference files not loaded."

Do NOT rely on memory of previous reads. Load ALL references fresh.

---

## Mandatory Steps (4)

### Step 2.1: Load Base Template Reference

**EXECUTE:**
```
Read(file_path=".claude/skills/devforgeai-feedback/references/template-format-specification.md")
```

**VERIFY:** Content loaded contains "template-id" field definition.
```
IF content does NOT contain "template-id": HALT -- "template-format-specification.md did not load correctly"
```

**RECORD:**
```bash
devforgeai-validate phase-record ${SESSION_ID} --workflow=feedback --phase=02 --step=2.1 --project-root=.
```
Update checkpoint:
```
checkpoint.phases["02"].steps_completed.append("2.1")
checkpoint.phases["02"].references_loaded.append("template-format-specification.md")
```

---

### Step 2.2: Load Type-Specific References

**EXECUTE:**
```
SWITCH $FEEDBACK_TYPE:
  CASE "conversation":
    Read(file_path=".claude/skills/devforgeai-feedback/references/adaptive-questioning.md")
    Read(file_path=".claude/skills/devforgeai-feedback/references/feedback-question-templates.md")

  CASE "summary":
    Read(file_path=".claude/skills/devforgeai-feedback/references/feedback-persistence-guide.md")

  CASE "metrics":
    Read(file_path=".claude/skills/devforgeai-feedback/references/feedback-export-formats.md")

  CASE "checklist":
    Read(file_path=".claude/skills/devforgeai-feedback/references/feedback-question-templates.md")

  CASE "ai_analysis":
    Read(file_path=".claude/skills/devforgeai-feedback/references/feedback-analysis-patterns.md")
    Read(file_path=".claude/skills/devforgeai-feedback/references/feedback-question-templates.md")

  CASE "triage":
    Read(file_path=".claude/skills/devforgeai-feedback/references/triage-workflow.md")

  CASE "config":
    Read(file_path=".claude/skills/devforgeai-feedback/references/user-customization-guide.md")

  CASE "search":
    Read(file_path=".claude/skills/devforgeai-feedback/references/feedback-search-help.md")

  CASE "export":
    Read(file_path=".claude/skills/devforgeai-feedback/references/feedback-export-formats.md")

  CASE "import":
    Read(file_path=".claude/skills/devforgeai-feedback/references/feedback-export-formats.md")
```

**VERIFY:** At least 1 type-specific reference loaded successfully (content is non-empty).
```
IF no reference content loaded: HALT -- "Type-specific references for ${FEEDBACK_TYPE} failed to load"
```

**RECORD:**
```bash
devforgeai-validate phase-record ${SESSION_ID} --workflow=feedback --phase=02 --step=2.2 --project-root=.
```
Update checkpoint:
```
checkpoint.phases["02"].steps_completed.append("2.2")
checkpoint.phases["02"].references_loaded.append(loaded_reference_names)
```

---

### Step 2.3: Select and Load Template

**EXECUTE:**
```
# Determine template based on operation type and status
IF $FEEDBACK_TYPE in ["conversation", "summary", "metrics", "checklist", "ai_analysis"]:
  # Map operation type to template category
  IF $OPERATION_CONTEXT.operation_type == "command":
    IF $OPERATION_CONTEXT.status == "success":
      template_file = "command-passed.yaml"
    ELSE:
      template_file = "command-failed.yaml"
  ELSE IF $OPERATION_CONTEXT.operation_type == "skill":
    IF $OPERATION_CONTEXT.status == "success":
      template_file = "skill-passed.yaml"
    ELSE:
      template_file = "skill-failed.yaml"
  ELSE IF $OPERATION_CONTEXT.operation_type == "subagent":
    IF $OPERATION_CONTEXT.status == "success":
      template_file = "subagent-passed.yaml"
    ELSE:
      template_file = "subagent-failed.yaml"
  ELSE:
    template_file = "generic.yaml"

  # Load the template
  Read(file_path=".claude/skills/devforgeai-feedback/templates/${template_file}")

ELSE IF $FEEDBACK_TYPE in ["triage", "config", "search", "export", "import"]:
  # These types do not use question templates
  template_file = "N/A"
  # No template load needed
```

**VERIFY:**
```
IF template_file != "N/A":
  Content loaded contains "template-id" YAML field
  IF NOT: HALT -- "Template ${template_file} failed to load"
ELSE:
  VERIFY: $FEEDBACK_TYPE is in ["triage", "config", "search", "export", "import"]
```

**RECORD:**
```bash
devforgeai-validate phase-record ${SESSION_ID} --workflow=feedback --phase=02 --step=2.3 --project-root=.
```
Update checkpoint:
```
checkpoint.phases["02"].template_loaded = (template_file != "N/A")
checkpoint.phases["02"].template_file = template_file
checkpoint.phases["02"].steps_completed.append("2.3")
```

---

### Step 2.4: Prepare Execution Parameters

**EXECUTE:**
```
Build execution_params object by merging:
  1. $OPERATION_CONTEXT (from Phase 01)
  2. Template field mappings (from Step 2.3, if applicable)
  3. Type-specific configuration:

  SWITCH $FEEDBACK_TYPE:
    CASE "conversation":
      params.question_count_min = 3
      params.question_count_max = 7
      params.allow_skip = false
      params.question_selection_algorithm = "adaptive"  # From adaptive-questioning.md

    CASE "summary":
      params.required_sections = ["duration", "test_results", "phases", "next_steps"]
      params.format = "markdown"

    CASE "metrics":
      params.metric_fields = ["execution_time", "token_usage", "test_pass_rate"]
      params.format = "json"

    CASE "checklist":
      params.multiSelect = true
      params.calculate_completion = true

    CASE "ai_analysis":
      params.subagent = "framework-analyst"
      params.output_schema = "AI Analysis Output Schema"  # From SKILL.md
      params.merit_filter = true
      params.aspirational_language_check = true

    CASE "triage":
      params.queue_path = "devforgeai/feedback/ai-analysis/aggregated/recommendations-queue.json"
      params.story_creation_skill = "devforgeai-story-creation"
      params.priority_filter = $PRIORITY_FILTER
      params.selected_items = $SELECTED_ITEMS

    CASE "config":
      params.config_path = "devforgeai/feedback/config.yaml"
      params.subcommand = $SUBCOMMAND

    CASE "search":
      params.index_path = "devforgeai/feedback/index.json"
      params.query = $SEARCH_QUERY
      params.severity = $SEVERITY
      params.status = $STATUS
      params.limit = $LIMIT or 10
      params.page = $PAGE or 1

    CASE "export":
      params.format = $FORMAT or "json"
      params.date_range = $DATE_RANGE
      params.story_ids = $STORY_IDS
      params.sanitize = $SANITIZE or true

    CASE "import":
      params.archive_path = $ARCHIVE_PATH
```

**VERIFY:** `execution_params` object is non-empty and contains type-specific required fields.
```
IF execution_params is empty: HALT -- "Execution parameters not prepared"
IF $FEEDBACK_TYPE == "conversation" AND params.question_count_min is null: HALT
IF $FEEDBACK_TYPE == "triage" AND params.queue_path is null: HALT
IF $FEEDBACK_TYPE == "search" AND params.query is null AND $SEARCH_QUERY is null: HALT
```

**RECORD:**
```bash
devforgeai-validate phase-record ${SESSION_ID} --workflow=feedback --phase=02 --step=2.4 --project-root=.
```
Update checkpoint:
```
checkpoint.phases["02"].exec_params_ready = true
checkpoint.phases["02"].status = "completed"
checkpoint.phases["02"].steps_completed.append("2.4")
checkpoint.progress.current_phase = 3
checkpoint.progress.phases_completed.append("02")
```
Write updated checkpoint to disk.

---

## Exit Gate

```bash
devforgeai-validate phase-complete ${SESSION_ID} --workflow=feedback --phase=02 --checkpoint-passed --project-root=.
```

---

## Exit Verification Checklist

Before proceeding to Phase 03, verify ALL:

- [ ] Base template reference loaded (template-format-specification.md)
- [ ] Type-specific references loaded for `$FEEDBACK_TYPE`
- [ ] Template selected and loaded (or N/A for non-template types)
- [ ] Execution parameters prepared with all required fields
- [ ] Checkpoint updated with phase 02 completion
- [ ] Checkpoint written to disk (verified via Glob)

**IF any criterion is unmet: HALT. Do NOT proceed to Phase 03.**

---

## Phase Transition Display

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Phase 02: Type Dispatch ✓
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Feedback Type: ${FEEDBACK_TYPE}
  Template: ${template_file}
  References: ${references_loaded.length} loaded
  Parameters: Ready
  Steps: 4/4
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```
