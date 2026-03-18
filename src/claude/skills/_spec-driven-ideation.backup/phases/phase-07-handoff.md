# Phase 07: Completion & Handoff

## Contract

| Attribute | Value |
|-----------|-------|
| **PURPOSE** | Present the completion summary, determine the next action based on project mode (greenfield vs brownfield), and hand off to the user with clear next steps. |
| **REFERENCE** | `.claude/skills/discovering-requirements/references/completion-handoff.md` (645 lines), `.claude/skills/discovering-requirements/references/output-templates.md` (365 lines) |
| **STEP COUNT** | 5 mandatory steps |
| **MINIMUM QUESTIONS** | 1-3 |

## Phase Exit Criteria

Before this phase can complete, ALL of the following MUST be true:

- [ ] completion_summary_displayed = true (session.completed_outputs.completion_summary_displayed)
- [ ] next_action_determined = true (session.completed_outputs.next_action_determined)
- [ ] User confirmed next steps (session.phases["07"].user_confirmed_next_steps == true)
- [ ] Checkpoint marked as complete (session.status == "complete")
- [ ] Requirements file path confirmed accessible (Glob returns match for requirements_file_path)

**IF any criterion is unmet: HALT. Workflow is NOT complete.**

---

## Reference Loading [MANDATORY]

```
Read(file_path=".claude/skills/discovering-requirements/references/completion-handoff.md")
Read(file_path=".claude/skills/discovering-requirements/references/output-templates.md")
```

IF either Read fails: HALT -- "Phase 07 reference files not loaded. Cannot proceed without handoff reference material."

Do NOT rely on memory of previous reads. Load fresh every time this phase executes.

---

## Mandatory Steps

### Step 7.1: Compile Completion Summary

**EXECUTE:**
```
# Gather all session data into structured summary
summary = {}

# Session metadata
summary.session_id = IDEATION_ID
summary.start_time = checkpoint.created_at
summary.end_time = "current ISO 8601 timestamp"
summary.duration = calculate_duration(summary.start_time, summary.end_time)
summary.total_questions = checkpoint.progress.total_questions_asked

# Problem statement
summary.problem_statement = session.completed_outputs.problem_statement

# User personas
summary.persona_count = len(session.completed_outputs.personas or [])
summary.persona_names = [p.name for p in session.completed_outputs.personas]

# Functional requirements by priority
all_frs = session.completed_outputs.functional_requirements or []
summary.fr_total = len(all_frs)
summary.fr_by_priority = {
  "Must Have": len([fr for fr in all_frs WHERE fr.priority == "Must Have"]),
  "Should Have": len([fr for fr in all_frs WHERE fr.priority == "Should Have"]),
  "Could Have": len([fr for fr in all_frs WHERE fr.priority == "Could Have"]),
  "Won't Have": len([fr for fr in all_frs WHERE fr.priority == "Won't Have"])
}

# Non-functional requirements
summary.nfr_count = len(session.completed_outputs.nfr_requirements or [])

# Data entities
summary.data_entity_count = len(session.completed_outputs.data_entities or [])

# Integrations
summary.integration_count = len(session.completed_outputs.integrations or [])

# Complexity
summary.complexity_tier = session.completed_outputs.complexity_assessment.tier if session.completed_outputs.complexity_assessment else "Unknown"
summary.complexity_label = session.completed_outputs.complexity_assessment.tier_label if session.completed_outputs.complexity_assessment else "Unknown"

# ADR prerequisites
summary.adr_count = len(session.completed_outputs.adr_prerequisites or [])

# Validation status
summary.validation_status = session.completed_outputs.validation_status

# Requirements file path
summary.requirements_file = session.completed_outputs.requirements_file_path

# Project mode
summary.project_mode = session.completed_outputs.project_type

Display:
"Compiling completion summary...
  Session: {summary.session_id}
  Duration: {summary.duration}
  Questions Asked: {summary.total_questions}
  Problem: {summary.problem_statement[:80]}...
  Personas: {summary.persona_count}
  FRs: {summary.fr_total} (Must: {summary.fr_by_priority['Must Have']}, Should: {summary.fr_by_priority['Should Have']}, Could: {summary.fr_by_priority['Could Have']})
  NFRs: {summary.nfr_count}
  Data Entities: {summary.data_entity_count}
  Integrations: {summary.integration_count}
  Complexity: Tier {summary.complexity_tier} ({summary.complexity_label})
  ADR Prerequisites: {summary.adr_count}
  Validation: {summary.validation_status}
  File: {summary.requirements_file}"
```

**VERIFY:**
- All summary fields populated (no null values for critical fields)
- `summary.session_id` is non-null and matches IDEATION_ID
- `summary.problem_statement` is non-null and non-empty
- `summary.fr_total` >= 0 (number, not null)
- `summary.validation_status` is one of: "PASSED", "PASSED_WITH_WARNINGS"
- `summary.requirements_file` is non-null
- IF any critical field is null: HALT -- "Step 7.1: Summary field '{field}' is null. Cannot compile completion summary."

**RECORD:**
- `session.phases["07"].summary = summary`
- `session.phases["07"].summary_compiled = true`
- `session.phases["07"].step_7_1_completed = true`
- Update checkpoint: `{ phase: 7, step: "7.1", status: "complete" }`

---

### Step 7.2: Determine Next Action (Mode-Based)

**EXECUTE:**
```
project_mode = session.completed_outputs.project_type

# ── Greenfield Path ──
IF project_mode == "greenfield":
  # Check if context files already exist (edge case: user created them mid-session)
  context_results = Glob(pattern="devforgeai/specs/context/*.md")
  context_count = len(context_results)

  IF context_count == 0:
    # No context files -- standard greenfield flow
    recommended_action = "create-epic"
    next_steps = [
      {
        order: 1,
        command: "/create-epic {project_name}",
        description: "Generate epic with stories from requirements",
        status: "recommended"
      },
      {
        order: 2,
        command: "/create-context",
        description: "Generate 6 constitutional context files for architecture",
        status: "required_before_dev"
      },
      {
        order: 3,
        command: "/create-sprint 1",
        description: "Plan first sprint from epic stories",
        status: "after_context"
      },
      {
        order: 4,
        command: "/dev {STORY-ID}",
        description: "Begin TDD development on first story",
        status: "after_sprint"
      }
    ]

    Display:
    "Project Mode: Greenfield (no existing context files)

    Recommended workflow:
      1. /create-epic {project_name} -- Generate epic from requirements
      2. /create-context -- Create architecture context files
      3. /create-sprint 1 -- Plan first sprint
      4. /dev {STORY-ID} -- Start development"

  ELSE:
    # Context files appeared during session (unusual for greenfield)
    Display: "Note: {context_count} context file(s) detected despite greenfield mode."
    recommended_action = "create-epic"
    next_steps = [
      {
        order: 1,
        command: "/create-epic {project_name}",
        description: "Generate epic with stories from requirements",
        status: "recommended"
      },
      {
        order: 2,
        command: "/create-sprint 1",
        description: "Plan first sprint (context files already exist)",
        status: "after_epic"
      }
    ]

# ── Brownfield Path ──
ELSE IF project_mode in ["brownfield", "modernization"]:
  # Validate requirements against existing constraints
  context_results = Glob(pattern="devforgeai/specs/context/*.md")
  context_count = len(context_results)

  conflicts = []

  IF context_count >= 1:
    # Check for potential conflicts with existing tech-stack
    tech_stack_exists = Glob(pattern="devforgeai/specs/context/tech-stack.md")
    IF tech_stack_exists:
      Read(file_path="devforgeai/specs/context/tech-stack.md")
      # Surface-level conflict check: new requirements vs existing constraints
      # Deep validation is deferred to /create-epic or /create-context
      IF requirements_imply_new_technology:
        conflicts.append({
          type: "tech_stack_conflict",
          message: "New requirements may require technologies not in current tech-stack.md",
          resolution: "ADR required before development"
        })

    # Check for architecture constraint conflicts
    arch_exists = Glob(pattern="devforgeai/specs/context/architecture-constraints.md")
    IF arch_exists:
      Read(file_path="devforgeai/specs/context/architecture-constraints.md")
      IF requirements_conflict_with_architecture:
        conflicts.append({
          type: "architecture_conflict",
          message: "New requirements may conflict with existing architecture constraints",
          resolution: "ADR required before development"
        })

  IF len(conflicts) > 0:
    Display:
    "Potential conflicts detected with existing context:
      {FOR each conflict: '  [{conflict.type}] {conflict.message}'}
      Resolution: {conflict.resolution}

    These conflicts should be resolved via ADR creation before development begins."

    recommended_action = "create-epic"
    next_steps = [
      {
        order: 1,
        command: "/create-epic {project_name}",
        description: "Generate epic (will flag conflict stories)",
        status: "recommended"
      },
      {
        order: 2,
        command: "Create ADR(s) for conflicts",
        description: "Resolve {len(conflicts)} conflict(s) via Architecture Decision Records",
        status: "required_before_dev"
      },
      {
        order: 3,
        command: "/create-sprint 1",
        description: "Plan sprint after conflict resolution",
        status: "after_adr"
      }
    ]

  ELSE:
    # No conflicts -- standard brownfield flow
    recommended_action = "create-epic"
    next_steps = [
      {
        order: 1,
        command: "/create-epic {project_name}",
        description: "Generate epic from requirements",
        status: "recommended"
      },
      {
        order: 2,
        command: "/create-sprint 1",
        description: "Plan first sprint (context files already exist)",
        status: "after_epic"
      },
      {
        order: 3,
        command: "/dev {STORY-ID}",
        description: "Begin TDD development",
        status: "after_sprint"
      }
    ]

    Display:
    "Project Mode: Brownfield (existing context files compatible)

    Recommended workflow:
      1. /create-epic {project_name} -- Generate epic from requirements
      2. /create-sprint 1 -- Plan first sprint
      3. /dev {STORY-ID} -- Start development"

session.phases["07"].conflicts = conflicts
```

**VERIFY:**
- `recommended_action` is one of: "create-epic", "create-context", "create-sprint"
- `next_steps` is a non-empty list with at least 1 entry
- Each next_step has: order, command, description, status
- IF project_mode is null: HALT -- "Step 7.2: Project mode not set. Cannot determine next action."
- IF recommended_action is null: HALT -- "Step 7.2: No recommended action determined."

**RECORD:**
- `session.completed_outputs.next_action = recommended_action`
- `session.phases["07"].next_steps = next_steps`
- `session.phases["07"].conflicts = conflicts`
- `session.phases["07"].step_7_2_completed = true`
- Update checkpoint: `{ phase: 7, step: "7.2", status: "complete" }`

---

### Step 7.3: Display Completion Banner

**EXECUTE:**
```
# Extract project name from requirements path or session data
project_name = extract_project_name(session.completed_outputs.requirements_file_path)

Display:
"
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  IDEATION COMPLETE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Project: {project_name}
Mode: {summary.project_mode}
Session: {summary.session_id}
Duration: {summary.duration}
Questions Asked: {summary.total_questions}

Generated Artifacts:
  Requirements File: {summary.requirements_file}
  Functional Requirements: {summary.fr_total}
    Must Have:   {summary.fr_by_priority['Must Have']}
    Should Have: {summary.fr_by_priority['Should Have']}
    Could Have:  {summary.fr_by_priority['Could Have']}
    Won't Have:  {summary.fr_by_priority['Won't Have']}
  Non-Functional Requirements: {summary.nfr_count}
  Constraints: {len(session.completed_outputs.constraints or [])}
  Data Entities: {summary.data_entity_count}
  Integrations: {summary.integration_count}

Complexity: Tier {summary.complexity_tier} ({summary.complexity_label})
Validation: {summary.validation_status}
ADR Prerequisites: {summary.adr_count}
{IF summary.adr_count > 0:
  FOR each adr in session.completed_outputs.adr_prerequisites:
    '  - {adr.description}'
}

{IF len(conflicts) > 0:
  'Conflicts Detected: {len(conflicts)}'
  FOR each conflict in conflicts:
    '  - {conflict.message}'
}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Next Steps (in order)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

{FOR each step in next_steps:
  '{step.order}. {step.command}'
  '   {step.description}'
}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"
```

**VERIFY:**
- Banner displayed with all fields populated (no {placeholder} text remaining)
- `summary.requirements_file` matches a real file path
- Verify file still accessible: `Glob(pattern=summary.requirements_file)`
- IF Glob returns empty: HALT -- "Step 7.3: Requirements file no longer accessible at '{summary.requirements_file}'."
- Next steps list displayed with correct ordering

**RECORD:**
- `session.completed_outputs.completion_summary_displayed = true`
- `session.phases["07"].step_7_3_completed = true`
- Update checkpoint: `{ phase: 7, step: "7.3", status: "complete" }`

---

### Step 7.4: User Confirmation of Next Steps

**EXECUTE:**
```
# Build options based on project mode
options = []

# Always offer the recommended action
options.append({
  label: "Run /create-epic {project_name}",
  description: "Generate epic with stories from requirements (recommended)"
})

options.append({
  label: "Review the requirements first",
  description: "Open {summary.requirements_file} and review before continuing"
})

options.append({
  label: "Save and come back later",
  description: "Session is complete -- resume the DevForgeAI workflow anytime"
})

# Brownfield-specific option
IF project_mode in ["brownfield", "modernization"] AND len(conflicts) == 0:
  options.append({
    label: "Run /create-sprint directly",
    description: "Skip epic creation (context files exist, plan sprint now)"
  })

# Conflict-specific option
IF len(conflicts) > 0:
  options.append({
    label: "Create ADR for conflicts first",
    description: "Resolve {len(conflicts)} conflict(s) before proceeding"
  })

AskUserQuestion:
  questions:
    - question: "What would you like to do next?"
      header: "Next Action"
      multiSelect: false
      options: options

# Handle response
IF response == "Run /create-epic {project_name}":
  Display:
  "Run: /create-epic {project_name}

  The requirements file will be automatically detected:
    {summary.requirements_file}

  Key inputs will be pre-populated from your ideation session."

ELSE IF response == "Review the requirements first":
  Display:
  "Requirements document location:
    {summary.requirements_file}

  After review, run:
    /create-epic {project_name}"

ELSE IF response == "Save and come back later":
  Display:
  "Your requirements are saved and ready.

  File: {summary.requirements_file}
  Session: {summary.session_id}

  When ready, run:
    /create-epic {project_name}"

ELSE IF response == "Run /create-sprint directly":
  Display:
  "Run: /create-sprint 1

  Requirements will be loaded from:
    {summary.requirements_file}"

ELSE IF response == "Create ADR for conflicts first":
  Display:
  "Conflicts to resolve:
  {FOR each conflict in conflicts: '  - [{conflict.type}] {conflict.message}'}

  Create ADRs in devforgeai/specs/adrs/ to resolve each conflict.
  After ADR approval, run:
    /create-epic {project_name}"
```

**VERIFY:**
- User responded with a valid selection
- Appropriate guidance displayed for the chosen option
- IF response is null or empty: HALT -- "Step 7.4: User did not confirm next steps."

**RECORD:**
- `session.completed_outputs.next_action_determined = true`
- `session.phases["07"].user_next_action = response`
- `session.phases["07"].user_confirmed_next_steps = true`
- `session.phases["07"].step_7_4_completed = true`
- Update checkpoint: `{ phase: 7, step: "7.4", status: "complete" }`

---

### Step 7.5: Finalize Session

**EXECUTE:**
```
# Update checkpoint to complete status
checkpoint.status = "complete"
checkpoint.progress.current_phase = 7
checkpoint.progress.phases_completed.append("07")
checkpoint.progress.completion_percentage = 100
checkpoint.updated_at = "current ISO 8601 timestamp"
checkpoint.completed_at = "current ISO 8601 timestamp"

checkpoint.phases["07"] = {
  "summary_compiled": session.phases["07"].summary_compiled,
  "next_action": session.completed_outputs.next_action,
  "conflicts": session.phases["07"].conflicts,
  "completion_summary_displayed": session.completed_outputs.completion_summary_displayed,
  "next_action_determined": session.completed_outputs.next_action_determined,
  "user_next_action": session.phases["07"].user_next_action,
  "user_confirmed_next_steps": session.phases["07"].user_confirmed_next_steps,
  "steps_completed": ["step_7_1", "step_7_2", "step_7_3", "step_7_4", "step_7_5"]
}

checkpoint.completed_outputs = session.completed_outputs

# Write final checkpoint to disk
Write(file_path="devforgeai/specs/ideation/${IDEATION_ID}.checkpoint.json", content=checkpoint)

# Verify checkpoint write
verify_result = Glob(pattern="devforgeai/specs/ideation/${IDEATION_ID}.checkpoint.json")
IF not found:
  HALT -- "Step 7.5: Final checkpoint was NOT saved to disk."

# Verify checkpoint content shows complete status
Read(file_path="devforgeai/specs/ideation/${IDEATION_ID}.checkpoint.json")
IF checkpoint.status != "complete":
  HALT -- "Step 7.5: Checkpoint was saved but status is not 'complete'."

# Final confirmation message
Display:
"Ideation session {IDEATION_ID} complete.
Requirements saved to {summary.requirements_file}.
Checkpoint saved to devforgeai/specs/ideation/${IDEATION_ID}.checkpoint.json (status: complete)."
```

**VERIFY:**
- Checkpoint file exists on disk (Glob confirms)
- Checkpoint `status` field is "complete"
- Checkpoint `completion_percentage` is 100
- Checkpoint `phases_completed` contains all 7 phases: ["01", "02", "03", "04", "05", "06", "07"]
- Requirements file still accessible: `Glob(pattern=summary.requirements_file)` returns match
- IF checkpoint missing: HALT -- "Step 7.5: Finalization failed. Checkpoint not on disk."
- IF requirements file missing: HALT -- "Step 7.5: Requirements file no longer accessible after finalization."

**RECORD:**
- `session.status = "complete"`
- `session.phases["07"].step_7_5_completed = true`
- `session.phases["07"].finalized = true`
- Final checkpoint written (no further updates needed)

---

## Phase Exit Verification

Before declaring the workflow complete, verify ALL exit criteria:

```
VERIFY_EXIT:
  CHECK: session.completed_outputs.completion_summary_displayed == true
    IF FAIL: HALT -- "Exit blocked: Completion summary was not displayed."

  CHECK: session.completed_outputs.next_action_determined == true
    IF FAIL: HALT -- "Exit blocked: Next action was not determined."

  CHECK: session.phases["07"].user_confirmed_next_steps == true
    IF FAIL: HALT -- "Exit blocked: User did not confirm next steps."

  CHECK: session.status == "complete"
    IF FAIL: HALT -- "Exit blocked: Session status is not 'complete'."

  CHECK: Glob(pattern=session.completed_outputs.requirements_file_path) returns match
    IF FAIL: HALT -- "Exit blocked: Requirements file not accessible at '{path}'."

  CHECK: checkpoint.progress.completion_percentage == 100
    IF FAIL: HALT -- "Exit blocked: Completion percentage is {pct}%, expected 100%."

  CHECK: len(checkpoint.progress.phases_completed) == 7
    IF FAIL: HALT -- "Exit blocked: Only {count}/7 phases completed."
```

---

## Phase Transition Display

```
Display:
"
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  IDEATION WORKFLOW COMPLETE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Session: {IDEATION_ID}
Status: Complete
Duration: {summary.duration}
Questions Asked: {summary.total_questions}
Phases Completed: 7/7

Deliverable:
  {summary.requirements_file}
  FRs: {summary.fr_total} | NFRs: {summary.nfr_count}
  Validation: {summary.validation_status}
  Complexity: Tier {summary.complexity_tier}

Next Action: {session.phases['07'].user_next_action}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"
```

**Checkpoint Path:** `devforgeai/specs/ideation/${IDEATION_ID}.checkpoint.json`

---

## Common Issues and Recovery

| Issue | Symptom | Recovery |
|-------|---------|----------|
| Summary field is null | Critical data missing from earlier phase | Check checkpoint for the missing phase. May need to re-run that phase. |
| Requirements file disappeared | Glob returns empty in Step 7.3 | HALT. Phase 05 file write may have failed silently. Re-run Phase 05. |
| Conflict detection false positive | Brownfield conflict flagged incorrectly | User can choose "Run /create-epic" anyway. Conflicts are advisory. |
| Checkpoint write fails | Glob verification fails in Step 7.5 | Check disk space and permissions. Retry write once. |
| Context files changed mid-session | Greenfield detected context files | Unusual but handled. Adjusts next steps accordingly. |
| User wants to re-run validation | Warnings from Phase 06 concern user | User should edit requirements file, then re-invoke /ideate --resume to re-run Phase 06. |
