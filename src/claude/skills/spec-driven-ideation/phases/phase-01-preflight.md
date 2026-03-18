# Phase 01: Pre-Flight & Context Detection

## Contract

| Attribute | Value |
|-----------|-------|
| **PURPOSE** | Validate project context, detect greenfield/brownfield mode, load user input patterns, and process brainstorm handoff data if present |
| **REFERENCE** | `.claude/skills/spec-driven-ideation/references/brainstorm-handoff-workflow.md`, `.claude/skills/spec-driven-ideation/references/brainstorm-data-mapping.md`, `.claude/skills/spec-driven-ideation/references/user-input-guidance.md` |
| **STEP COUNT** | 6 mandatory steps |
| **MINIMUM QUESTIONS** | 0-3 (depends on whether brainstorm context provided and project type) |

## Phase Exit Criteria

Before this phase can complete, ALL of the following MUST be true:

- [ ] project_type determined (session.completed_outputs.project_type is one of: greenfield, brownfield, modernization)
- [ ] User input patterns load attempted (session.phases["01"].user_input_patterns_loaded is true or false)
- [ ] If brainstorm: handoff processed and validated (session.brainstorm_input.validated == true)
- [ ] If brownfield: existing system analysis completed (session.completed_outputs.existing_system is non-null)
- [ ] Checkpoint updated with phase data
- [ ] Context window check completed (session.phases["01"].context_check_completed == true)

**IF any criterion is unmet: HALT. Do NOT proceed to Phase 02.**

---

## Reference Loading [MANDATORY]

```
Read(file_path=".claude/skills/spec-driven-ideation/references/user-input-guidance.md")
Read(file_path=".claude/skills/spec-driven-ideation/references/brainstorm-handoff-workflow.md")
Read(file_path=".claude/skills/spec-driven-ideation/references/brainstorm-data-mapping.md")
```

**Error-Tolerant Loading:** Unlike other phases, Phase 01 reference loading uses graceful degradation.
- `user-input-guidance.md`: IF Read fails, set `session.phases["01"].user_input_patterns_loaded = false` and CONTINUE. Do NOT halt. This file enhances question quality but is not blocking.
- `brainstorm-handoff-workflow.md`: IF Read fails AND brainstorm context exists, HALT -- "Brainstorm handoff reference required but not loadable."
- `brainstorm-handoff-workflow.md`: IF Read fails AND NO brainstorm context, set graceful degradation and CONTINUE.
- `brainstorm-data-mapping.md`: Same conditional logic as brainstorm-handoff-workflow.md above.

Do NOT rely on memory of previous reads. Load fresh every time this phase executes.

---

## Mandatory Steps

### Step 1.1: Load User Input Patterns (Error-Tolerant)

**EXECUTE:**
```
Read(file_path=".claude/skills/spec-driven-ideation/references/user-input-guidance.md")

IF Read succeeds:
  Parse elicitation patterns (15 patterns expected)
  Parse AskUserQuestion templates (28 templates expected)
  Display: "User input guidance loaded: {pattern_count} elicitation patterns, {template_count} question templates."
  session.phases["01"].user_input_patterns_loaded = true

IF Read fails:
  Display: "User input guidance not available. Proceeding with built-in question patterns."
  session.phases["01"].user_input_patterns_loaded = false
  # NO HALT - this is graceful degradation
```

**VERIFY:**
- `session.phases["01"].user_input_patterns_loaded` is explicitly set to `true` or `false`
- IF value is null or undefined: HALT -- "Step 1.1: User input patterns load status not recorded."

**RECORD:**
- Update checkpoint: `session.phases["01"].user_input_patterns_loaded = true/false`
- Update checkpoint: `session.phases["01"].step_1_1_completed = true`

---

### Step 1.2: Detect Project Type

**EXECUTE:**
```
# Check for existing DevForgeAI context files
context_results = Glob(pattern="devforgeai/specs/context/*.md")
context_count = len(context_results)

IF context_count == 6:
  # All 6 constitutional context files present
  detected_type = "brownfield"
  Display: "Detected: Brownfield project (all 6 context files present)"
  Display files found:
    FOR each file in context_results:
      Display: "  - {filename}"

ELSE IF context_count == 0:
  detected_type = "greenfield"
  Display: "Detected: Greenfield project (no context files found)"

ELSE:
  # Partial context files (1-5 found)
  detected_type = "partial"
  Display: "Detected: Partial context ({context_count}/6 files found)"
  Display files found and missing:
    FOR each file in context_results:
      Display: "  Found: {filename}"
    FOR each missing file:
      Display: "  Missing: {filename}"
```

**Decision Logic (partial detection):**
```
IF detected_type == "partial":
  AskUserQuestion:
    questions:
      - question: "Found {context_count} of 6 context files. How should we classify this project?"
        header: "Project Type"
        multiSelect: false
        options:
          - label: "Brownfield - extending existing system"
            description: "Adding features to an established project"
          - label: "Greenfield - starting fresh"
            description: "Existing files are from a different effort"
          - label: "Modernization - replacing existing system"
            description: "Building new system to replace current one"

  IF response == "Brownfield - extending existing system":
    detected_type = "brownfield"
  ELSE IF response == "Greenfield - starting fresh":
    detected_type = "greenfield"
  ELSE IF response == "Modernization - replacing existing system":
    detected_type = "modernization"

  Increment question counter by 1
```

**VERIFY:**
- `detected_type` is one of: "greenfield", "brownfield", "modernization"
- IF detected_type is null, empty, or "partial": HALT -- "Step 1.2: Project type not resolved. Must be greenfield, brownfield, or modernization."
- Store in `session.completed_outputs.project_type`

**RECORD:**
- Update checkpoint: `session.completed_outputs.project_type = detected_type`
- Update checkpoint: `session.phases["01"].context_file_count = context_count`
- Update checkpoint: `session.phases["01"].step_1_2_completed = true`
- IF question asked (partial case): `session.phases["01"].questions_answered += 1`

---

### Step 1.3: Process Brainstorm Handoff (Conditional)

**Condition:** Only execute if `session.brainstorm_input.brainstorm_id` is not null (brainstorm file was loaded and parsed during Phase 00 Initialization Step 0.3).

```
IF session.brainstorm_input.brainstorm_id is null:
  Display: "No brainstorm input detected. Skipping brainstorm handoff processing."
  session.phases["01"].brainstorm_handoff_processed = false
  session.phases["01"].step_1_3_completed = true
  SKIP to Step 1.5
```

**EXECUTE:**
```
# Load brainstorm handoff workflow reference
Read(file_path=".claude/skills/spec-driven-ideation/references/brainstorm-handoff-workflow.md")
IF Read fails: HALT -- "Step 1.3: brainstorm-handoff-workflow.md required but not loadable."

# Load brainstorm data mapping reference
Read(file_path=".claude/skills/spec-driven-ideation/references/brainstorm-data-mapping.md")
IF Read fails: HALT -- "Step 1.3: brainstorm-data-mapping.md required but not loadable."

# Apply data mapping from brainstorm output to ideation input
pre_populated = []

# Map problem_statement
IF session.problem_statement is not null AND session.problem_statement != "":
  pre_populated.append("problem_statement")

# Map user_personas
IF session.user_personas is not null AND len(session.user_personas) > 0:
  pre_populated.append("user_personas")

# Map constraints (hard_constraints from brainstorm -> constraints in ideation)
IF session.constraints is not null AND len(session.constraints) > 0:
  pre_populated.append("constraints")

# Map must_have_requirements (must_have_capabilities from brainstorm)
IF session.must_have_requirements is not null AND len(session.must_have_requirements) > 0:
  pre_populated.append("must_haves")

# Calculate confidence level
confidence = session.brainstorm_input.confidence_level
IF confidence is null:
  # Derive from field coverage
  IF len(pre_populated) >= 4:
    confidence = "HIGH"
  ELSE IF len(pre_populated) >= 2:
    confidence = "MEDIUM"
  ELSE:
    confidence = "LOW"
  session.brainstorm_input.confidence_level = confidence

# Display pre-population summary
Display:
"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Brainstorm Handoff Summary
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Source: {session.brainstorm_input.brainstorm_id}
Confidence: {confidence}
Fields Pre-Populated: {len(pre_populated)}/{4 possible}

Pre-Populated Fields:
{FOR each field in pre_populated: '  [x] ' + field}
{FOR each field NOT in pre_populated: '  [ ] ' + field}

{IF confidence == 'HIGH': 'Full discovery questions will be reduced.'}
{IF confidence == 'MEDIUM': 'Some discovery questions will be asked for validation.'}
{IF confidence == 'LOW': 'Full discovery questions will be asked despite brainstorm input.'}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
```

**VERIFY:**
- `pre_populated` list is non-empty (at least 1 field mapped from brainstorm)
- IF `pre_populated` is empty AND brainstorm_id was provided: HALT -- "Step 1.3: Brainstorm file was provided but no fields could be extracted. Verify brainstorm file format."
- `session.brainstorm_input.confidence_level` is one of: "HIGH", "MEDIUM", "LOW"
- IF confidence_level is null: HALT -- "Step 1.3: Confidence level not determined after brainstorm processing."

**RECORD:**
- Update checkpoint: `session.brainstorm_input.pre_populated_fields = pre_populated`
- Update checkpoint: `session.brainstorm_input.confidence_level = confidence`
- Update checkpoint: `session.phases["01"].brainstorm_handoff_processed = true`
- Update checkpoint: `session.phases["01"].step_1_3_completed = true`

---

### Step 1.4: Brainstorm Confidence Assessment (Conditional)

**Condition:** Only execute if brainstorm data was pre-populated in Step 1.3 (`session.phases["01"].brainstorm_handoff_processed == true`).

```
IF session.phases["01"].brainstorm_handoff_processed != true:
  Display: "No brainstorm data to assess. Skipping confidence assessment."
  session.brainstorm_input.validated = true  # Vacuously true -- nothing to validate
  session.phases["01"].step_1_4_completed = true
  SKIP to Step 1.5
```

**EXECUTE:**
```
confidence = session.brainstorm_input.confidence_level

IF confidence == "HIGH":
  # High confidence -- trust brainstorm data, skip full discovery
  Display: "HIGH confidence brainstorm data detected."
  Display: "Pre-populated fields will be used directly. Focused elicitation will supplement gaps."
  Display: "Skipping full discovery questions for pre-populated fields."

  session.brainstorm_input.validated = true
  session.brainstorm_input.validation_method = "auto-accepted (HIGH confidence)"

ELSE IF confidence == "MEDIUM":
  # Medium confidence -- show pre-populated data and ask user to validate
  Display: "MEDIUM confidence brainstorm data detected. Displaying for validation."
  Display: ""
  Display: "Pre-populated from brainstorm:"

  IF "problem_statement" in session.brainstorm_input.pre_populated_fields:
    Display: "  Problem: {session.problem_statement}"
  IF "user_personas" in session.brainstorm_input.pre_populated_fields:
    Display: "  Personas: {count} persona(s) defined"
    FOR each persona in session.user_personas:
      Display: "    - {persona.name}: {persona.summary}"
  IF "constraints" in session.brainstorm_input.pre_populated_fields:
    Display: "  Constraints: {count} constraint(s)"
  IF "must_haves" in session.brainstorm_input.pre_populated_fields:
    Display: "  Must-Haves: {count} requirement(s)"

  AskUserQuestion:
    questions:
      - question: "Please review the pre-populated data above. Is this accurate?"
        header: "Validate Brainstorm Data"
        multiSelect: false
        options:
          - label: "Looks correct"
            description: "Use this data as-is"
          - label: "Needs corrections"
            description: "I'll point out what needs changing"
          - label: "Start fresh"
            description: "Ignore brainstorm data, ask me everything"

  IF response == "Looks correct":
    session.brainstorm_input.validated = true
    session.brainstorm_input.validation_method = "user-confirmed"

  ELSE IF response == "Needs corrections":
    AskUserQuestion:
      questions:
        - question: "Which fields need correction?"
          header: "Corrections"
          multiSelect: true
          options:
            - label: "Problem statement"
              description: "The problem description needs updating"
            - label: "User personas"
              description: "The persona definitions are wrong"
            - label: "Constraints"
              description: "The constraints are incorrect"
            - label: "Must-haves"
              description: "The must-have requirements are wrong"

    FOR each selected field:
      AskUserQuestion:
        questions:
          - question: "What is the correct value for {field}?"
            header: "Correct: {field}"
            multiSelect: false
            options:
              - label: "Let me describe it"
                description: "I'll provide the corrected information"

      Apply user's correction to session data for that field
      Update pre_populated_fields status

    session.brainstorm_input.validated = true
    session.brainstorm_input.validation_method = "user-corrected"
    Increment question counter by 1 + number of corrections

  ELSE IF response == "Start fresh":
    # Clear all pre-populated data
    session.problem_statement = null
    session.user_personas = []
    session.constraints = []
    session.must_have_requirements = []
    session.brainstorm_input.pre_populated_fields = []
    session.brainstorm_input.confidence_level = "DISCARDED"
    session.brainstorm_input.validated = true
    session.brainstorm_input.validation_method = "user-discarded"
    Display: "Brainstorm data cleared. Full discovery will proceed in Phase 2."

  Increment question counter by 1

ELSE IF confidence == "LOW":
  # Low confidence -- warn user and ask whether to keep any data
  Display: "LOW confidence brainstorm data detected."
  Display: "Only {len(pre_populated)} of 4 fields could be extracted."
  Display: "Full discovery questions will be asked regardless."

  AskUserQuestion:
    questions:
      - question: "Low confidence brainstorm data available. How should we proceed?"
        header: "Low Confidence Data"
        multiSelect: false
        options:
          - label: "Use as starting hints"
            description: "Pre-fill what we can, ask about everything"
          - label: "Ignore brainstorm data"
            description: "Start completely fresh"

  IF response == "Use as starting hints":
    session.brainstorm_input.validated = true
    session.brainstorm_input.validation_method = "user-accepted-as-hints"
  ELSE IF response == "Ignore brainstorm data":
    session.problem_statement = null
    session.user_personas = []
    session.constraints = []
    session.must_have_requirements = []
    session.brainstorm_input.pre_populated_fields = []
    session.brainstorm_input.confidence_level = "DISCARDED"
    session.brainstorm_input.validated = true
    session.brainstorm_input.validation_method = "user-discarded"
    Display: "Brainstorm data cleared."

  Increment question counter by 1
```

**VERIFY:**
- `session.brainstorm_input.validated` is explicitly `true`
- IF `session.brainstorm_input.validated` is null or false: HALT -- "Step 1.4: Brainstorm confidence assessment incomplete. Validation required before proceeding."
- `session.brainstorm_input.validation_method` is one of: "auto-accepted (HIGH confidence)", "user-confirmed", "user-corrected", "user-discarded", "user-accepted-as-hints"
- IF validation_method is null: HALT -- "Step 1.4: Validation method not recorded."

**RECORD:**
- Update checkpoint: `session.brainstorm_input.validated = true`
- Update checkpoint: `session.brainstorm_input.validation_method = method`
- Update checkpoint: `session.phases["01"].step_1_4_completed = true`
- IF questions asked: `session.phases["01"].questions_answered += count`

---

### Step 1.5: Existing System Analysis (Brownfield Only)

**Condition:** Only execute if `session.completed_outputs.project_type == "brownfield"`.

```
IF session.completed_outputs.project_type != "brownfield":
  Display: "Project type is {project_type}. Skipping existing system analysis."
  session.phases["01"].step_1_5_completed = true
  SKIP to Step 1.6
```

**EXECUTE:**
```
# Ask about current technology stack
AskUserQuestion:
  questions:
    - question: "What technology stack does the current system use?"
      header: "Current Tech Stack"
      multiSelect: true
      options:
        - label: "Python/Django/Flask"
          description: "Python-based backend"
        - label: "Node.js/TypeScript"
          description: "JavaScript/TypeScript backend"
        - label: "Java/Spring"
          description: "Java-based backend"
        - label: ".NET/C#"
          description: "Microsoft stack"
        - label: "React/Angular/Vue"
          description: "JavaScript frontend framework"
        - label: "SQL Database (PostgreSQL, MySQL, etc.)"
          description: "Relational database"
        - label: "NoSQL Database (MongoDB, DynamoDB, etc.)"
          description: "Non-relational database"
        - label: "Other"
          description: "I'll describe it"

IF "Other" selected:
  AskUserQuestion:
    questions:
      - question: "Please describe the technology stack."
        header: "Tech Details"
        multiSelect: false
        options:
          - label: "Let me describe it"
            description: "I'll provide details"

  Capture user description
  Increment question counter by 1

Store in session.completed_outputs.existing_system.tech_stack
Increment question counter by 1
```

```
# Ask about pain points with current system
AskUserQuestion:
  questions:
    - question: "What are the biggest pain points with the current system?"
      header: "Pain Points"
      multiSelect: true
      options:
        - label: "Performance issues"
          description: "Slow, unresponsive, or resource-heavy"
        - label: "Reliability problems"
          description: "Crashes, data loss, or downtime"
        - label: "Difficult to maintain"
          description: "Hard to modify, fragile codebase"
        - label: "Poor user experience"
          description: "Users complain about usability"
        - label: "Missing features"
          description: "Cannot do what users need"
        - label: "Security concerns"
          description: "Vulnerabilities or compliance gaps"
        - label: "Scaling limitations"
          description: "Cannot handle growth"

Store in session.completed_outputs.existing_system.pain_points
Increment question counter by 1
```

```
# Ask what to keep vs replace
AskUserQuestion:
  questions:
    - question: "Which parts of the current system should be preserved?"
      header: "Keep vs Replace"
      multiSelect: true
      options:
        - label: "Database/data"
          description: "Keep existing data and schema"
        - label: "Business logic"
          description: "Core algorithms and rules work well"
        - label: "Integrations"
          description: "Current API connections should remain"
        - label: "User interface"
          description: "Frontend is acceptable"
        - label: "Infrastructure"
          description: "Hosting/deployment setup is good"
        - label: "Nothing - full replacement"
          description: "Start from scratch"

Store in session.completed_outputs.existing_system.preserve_list
Increment question counter by 1
```

**VERIFY:**
- `session.completed_outputs.existing_system` is non-null
- `session.completed_outputs.existing_system.tech_stack` is non-empty (at least 1 technology identified)
- IF tech_stack is null or empty: HALT -- "Step 1.5: Current technology stack not captured for brownfield project."
- `session.completed_outputs.existing_system.pain_points` is non-empty (at least 1 pain point)
- IF pain_points is null or empty: HALT -- "Step 1.5: Pain points not captured for brownfield project."
- `session.completed_outputs.existing_system.preserve_list` is non-empty (at least 1 selection)
- IF preserve_list is null or empty: HALT -- "Step 1.5: Keep-vs-replace decision not captured for brownfield project."

**RECORD:**
- Update checkpoint: `session.completed_outputs.existing_system = {tech_stack, pain_points, preserve_list}`
- Update checkpoint: `session.phases["01"].step_1_5_completed = true`
- Update checkpoint: `session.phases["01"].questions_answered += 3` (minimum 3 questions for brownfield)

---

### Step 1.6: Context Window Check

**EXECUTE:**
```
IF estimated_context_usage > 70%:
  AskUserQuestion:
    questions:
      - question: "Context window is approximately {PERCENT}% full. Would you like to:"
        header: "Session Health"
        multiSelect: false
        options:
          - label: "Continue in this session"
            description: "Proceed to Phase 2 (Discovery & Problem Understanding)"
          - label: "Save and continue later"
            description: "Create checkpoint and exit"

  IF response == "Save and continue later":
    # Update checkpoint with all Phase 01 data before exit
    checkpoint.progress.current_phase = 2
    checkpoint.progress.phases_completed.append("01")
    checkpoint.progress.completion_percentage = round(1/7 * 100)
    checkpoint.updated_at = "current ISO 8601 timestamp"

    Write(file_path="devforgeai/specs/ideation/${IDEATION_ID}.checkpoint.json", content=checkpoint)

    # Verify write
    verify_result = Glob(pattern="devforgeai/specs/ideation/${IDEATION_ID}.checkpoint.json")
    IF not found: HALT -- "Step 1.6: Checkpoint save failed during session exit."

    Display: "Session saved. Resume with: /ideate --resume ${IDEATION_ID}"
    EXIT skill

  ELSE:
    Display: "Continuing in current session."
    session.phases["01"].context_check_completed = true

ELSE:
  Display: "Context window healthy ({PERCENT}%). Proceeding to Phase 2."
  session.phases["01"].context_check_completed = true
```

**VERIFY:**
- Context window check was performed (either threshold check triggered or healthy confirmation displayed)
- `session.phases["01"].context_check_completed` is `true`
- IF check was skipped (value is null or false): HALT -- "Step 1.6: Context Window Check not performed."

**RECORD:**
- Update checkpoint: `session.phases["01"].context_check_completed = true`
- Update checkpoint: `session.phases["01"].step_1_6_completed = true`

---

## Phase Exit Verification

Before transitioning to Phase 02, verify ALL exit criteria:

```
VERIFY_EXIT:
  CHECK: session.completed_outputs.project_type in ["greenfield", "brownfield", "modernization"]
    IF FAIL: HALT -- "Exit blocked: project_type not determined. Must be greenfield, brownfield, or modernization."

  CHECK: session.phases["01"].user_input_patterns_loaded is true OR false (explicitly set, not null)
    IF FAIL: HALT -- "Exit blocked: User input patterns load status not recorded."

  CHECK: IF session.brainstorm_input.brainstorm_id is not null
         THEN session.brainstorm_input.validated == true
    IF FAIL: HALT -- "Exit blocked: Brainstorm handoff data exists but was not validated."

  CHECK: IF session.completed_outputs.project_type == "brownfield"
         THEN session.completed_outputs.existing_system is not null
              AND session.completed_outputs.existing_system.tech_stack is non-empty
              AND session.completed_outputs.existing_system.pain_points is non-empty
              AND session.completed_outputs.existing_system.preserve_list is non-empty
    IF FAIL: HALT -- "Exit blocked: Brownfield project detected but existing system analysis incomplete."

  CHECK: session.phases["01"].context_check_completed == true
    IF FAIL: HALT -- "Exit blocked: Context window check not completed."

  CHECK: session.phases["01"].questions_answered >= 0
    IF FAIL: HALT -- "Exit blocked: Question counter not initialized."
```

Update checkpoint on successful exit:
```
checkpoint.progress.current_phase = 2
checkpoint.progress.phases_completed.append("01")
checkpoint.progress.completion_percentage = round(1/7 * 100)
checkpoint.updated_at = "current ISO 8601 timestamp"

checkpoint.phases["01"] = {
  "user_input_patterns_loaded": session.phases["01"].user_input_patterns_loaded,
  "context_file_count": session.phases["01"].context_file_count,
  "brainstorm_handoff_processed": session.phases["01"].brainstorm_handoff_processed or false,
  "context_check_completed": session.phases["01"].context_check_completed,
  "questions_answered": session.phases["01"].questions_answered,
  "steps_completed": [
    "step_1_1", "step_1_2",
    "step_1_3" if applicable,
    "step_1_4" if applicable,
    "step_1_5" if applicable,
    "step_1_6"
  ]
}

Write(file_path="devforgeai/specs/ideation/${IDEATION_ID}.checkpoint.json", content=checkpoint)
```

**VERIFY checkpoint write:** `Glob(pattern="devforgeai/specs/ideation/${IDEATION_ID}.checkpoint.json")`
IF not found: HALT -- "Phase 01 exit checkpoint was NOT saved."

---

## Phase Transition Display

```
Display:
"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Phase 1 Complete: Pre-Flight & Context Detection
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Project Type: {project_type}
Context Files: {context_file_count}/6 found
User Input Patterns: {loaded ? 'Loaded' : 'Graceful degradation'}

Brainstorm Input: {brainstorm_id ? brainstorm_id : 'None'}
{IF brainstorm_id:
  Confidence: {confidence_level}
  Pre-Populated: {pre_populated_count} field(s)
  Validation: {validation_method}
}

{IF project_type == 'brownfield':
  Existing System:
    Tech Stack: {tech_stack_summary}
    Pain Points: {pain_point_count} identified
    Preserve: {preserve_count} component(s)
}

Questions Asked: {questions_answered}

Proceeding to Phase 2: Discovery & Problem Understanding...
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
```

---

## Common Issues and Recovery

| Issue | Symptom | Recovery |
|-------|---------|----------|
| Brainstorm file exists but schema invalid | Step 0.3 validation WARN/FAIL | Phase 00 handles this. Phase 01 receives validated data or null. |
| Context files partially present | 1-5 files found in Step 1.2 | Ask user to classify project type. Do not assume. |
| User input guidance missing | Read fails in Step 1.1 | Graceful degradation. Continue with built-in patterns. |
| Brainstorm confidence LOW but user wants to keep data | User selects "Use as starting hints" | Accept as hints, full discovery proceeds anyway in Phase 2. |
| Brownfield but user cannot describe tech stack | "Other" selected but no description | Re-prompt once. If still empty, record as "Unknown - requires investigation". |
| Context window already high at Phase 01 | > 70% before any questions | Offer save-and-resume immediately. User may have large brainstorm input. |
