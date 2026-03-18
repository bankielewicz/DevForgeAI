# Phase 04: Constitutional Compliance Pre-Check

## Contract

| Attribute | Value |
|-----------|-------|
| **PURPOSE** | Verify that proposed features respect the 6 immutable context files and flag any ADR creation requirements as Day 0 prerequisites. Protects downstream development by identifying constitutional conflicts early. |
| **REFERENCE** | `devforgeai/specs/context/tech-stack.md`, `devforgeai/specs/context/architecture-constraints.md`, `devforgeai/specs/context/dependencies.md`, `devforgeai/specs/context/source-tree.md`, `devforgeai/specs/context/coding-standards.md`, `devforgeai/specs/context/anti-patterns.md` |
| **STEP COUNT** | 4 mandatory steps |
| **MINIMUM QUESTIONS** | 0 |

## Phase Exit Criteria

Before this phase can complete, ALL of the following MUST be true:

- [ ] compliance_checked = true (check was performed or skipped for greenfield)
- [ ] adr_prerequisites list populated (can be empty)
- [ ] Compliance report displayed to user
- [ ] Checkpoint updated with phase data
- [ ] Context window check completed

**NOTE: This phase is NON-BLOCKING. Warnings do not halt the workflow.**

---

## Reference Loading [MANDATORY]

Context files are loaded DIRECTLY -- not from skill references. Loading is conditional on detection results in Step 4.1.

```
# Step 4.1 determines which files exist before loading.
# Do NOT pre-load all 6 files. Load only what Glob confirms present.
```

Do NOT rely on memory of previous reads. Load fresh every time this phase executes.

---

## Mandatory Steps

### Step 4.1: Context File Detection

**EXECUTE:**
```
context_results = Glob(pattern="devforgeai/specs/context/*.md")
context_count = len(context_results)

# Define the 6 constitutional files
expected_files = [
  "devforgeai/specs/context/tech-stack.md",
  "devforgeai/specs/context/architecture-constraints.md",
  "devforgeai/specs/context/dependencies.md",
  "devforgeai/specs/context/source-tree.md",
  "devforgeai/specs/context/coding-standards.md",
  "devforgeai/specs/context/anti-patterns.md"
]

found_files = [f for f in expected_files if f in context_results]
missing_files = [f for f in expected_files if f not in context_results]

IF context_count == 0:
  Display: "No context files found. Greenfield project -- skipping compliance analysis."
  session.phases["04"].mode = "greenfield_skip"
  session.phases["04"].compliance_checked = true
  session.completed_outputs.adr_prerequisites = []
  SKIP to Step 4.4

ELSE IF len(found_files) < 6:
  Display: "Partial context detected ({len(found_files)}/6 files found)."
  Display: "  Found:"
  FOR each file in found_files:
    Display: "    - {file}"
  Display: "  Missing (skipped):"
  FOR each file in missing_files:
    Display: "    - {file}"
  session.phases["04"].mode = "partial"

  # Load only files that exist
  FOR each file in found_files:
    Read(file_path=file)

ELSE:
  Display: "Full context detected (6/6 files). Loading all for compliance analysis."
  session.phases["04"].mode = "full"

  Read(file_path="devforgeai/specs/context/tech-stack.md")
  Read(file_path="devforgeai/specs/context/architecture-constraints.md")
  Read(file_path="devforgeai/specs/context/dependencies.md")
  Read(file_path="devforgeai/specs/context/source-tree.md")
  Read(file_path="devforgeai/specs/context/coding-standards.md")
  Read(file_path="devforgeai/specs/context/anti-patterns.md")
```

**VERIFY:**
- `context_count` is a non-negative integer
- `session.phases["04"].mode` is one of: "greenfield_skip", "partial", "full"
- IF mode is "greenfield_skip": verify SKIP to Step 4.4 occurs

**RECORD:**
- `session.phases["04"].context_files_found = len(found_files)`
- `session.phases["04"].context_files_missing = missing_files`
- `session.phases["04"].step_4_1_completed = true`

---

### Step 4.2: Feature-to-Context Conflict Analysis

**Condition:** Only execute if context files were found (`session.phases["04"].mode != "greenfield_skip"`).

```
IF session.phases["04"].mode == "greenfield_skip":
  Display: "Skipping conflict analysis -- no context files to check against."
  session.phases["04"].step_4_2_completed = true
  SKIP to Step 4.3
```

**EXECUTE:**
```
adr_prerequisites = []

# Retrieve functional requirements from Phase 03
requirements = session.completed_outputs.functional_requirements

FOR each requirement in requirements:

  affected_files = []
  adr_topic = null

  # Check 1: Does this feature imply new technology?
  # Compare requirement's implied tech against tech-stack.md
  IF requirement implies technology NOT listed in tech-stack.md:
    affected_files.append("tech-stack.md")
    adr_topic = "New technology: {implied_tech}"

  # Check 2: Does this feature imply a new dependency?
  # Compare against dependencies.md
  IF requirement implies external library or service NOT in dependencies.md:
    affected_files.append("dependencies.md")
    adr_topic = adr_topic or "New dependency: {implied_dependency}"

  # Check 3: Does this feature imply architecture change?
  # Compare against architecture-constraints.md
  IF requirement contradicts architecture patterns (e.g., adds new layer, breaks SRP):
    affected_files.append("architecture-constraints.md")
    adr_topic = adr_topic or "Architecture modification: {change_description}"

  # Check 4: Does this feature imply directory restructure?
  # Compare against source-tree.md
  IF requirement implies new directories or file locations NOT in source-tree.md:
    affected_files.append("source-tree.md")
    adr_topic = adr_topic or "Directory structure change: {new_path}"

  # Check 5: Does this feature imply coding convention change?
  # Compare against coding-standards.md
  IF requirement implies patterns that contradict coding-standards.md:
    affected_files.append("coding-standards.md")
    adr_topic = adr_topic or "Coding standard exception: {convention}"

  # Check 6: Does this feature imply new forbidden pattern or exception?
  # Compare against anti-patterns.md
  IF requirement would require a pattern listed in anti-patterns.md:
    affected_files.append("anti-patterns.md")
    adr_topic = adr_topic or "Anti-pattern exception: {pattern_name}"

  # If any context file is affected, record the prerequisite
  IF len(affected_files) > 0:
    adr_prerequisites.append({
      "feature": requirement.user_story or requirement.description,
      "affected_context_files": affected_files,
      "required_adr_topic": adr_topic,
      "status": "Day 0 prerequisite"
    })

session.completed_outputs.adr_prerequisites = adr_prerequisites
```

**VERIFY:**
- Analysis was attempted for ALL functional requirements from Phase 03
- `session.completed_outputs.adr_prerequisites` is a list (can be empty)
- Each entry in adr_prerequisites has: feature, affected_context_files, required_adr_topic, status

**RECORD:**
- `session.completed_outputs.adr_prerequisites = adr_prerequisites`
- `session.phases["04"].features_analyzed = len(requirements)`
- `session.phases["04"].conflicts_found = len(adr_prerequisites)`
- `session.phases["04"].step_4_2_completed = true`

---

### Step 4.3: Display Compliance Report

**EXECUTE:**
```
adr_prerequisites = session.completed_outputs.adr_prerequisites

IF len(adr_prerequisites) == 0:
  Display:
  "
  Constitutional Compliance: CLEAN
  All {session.phases['04'].features_analyzed} features analyzed.
  No ADR prerequisites detected. All proposed features are compatible
  with existing context files.
  "
  session.phases["04"].compliance_status = "clean"

ELSE:
  Display:
  "
  Constitutional Compliance: WARNINGS
  {len(adr_prerequisites)} feature(s) flagged out of {session.phases['04'].features_analyzed} analyzed.

  Flagged Features:
  "

  FOR each prereq in adr_prerequisites:
    Display:
    "
    Feature: {prereq.feature}
    Affected Files: {', '.join(prereq.affected_context_files)}
    Required ADR: {prereq.required_adr_topic}
    Status: Day 0 prerequisite -- ADR must be approved before implementation begins.
    "

  Display:
  "
  Summary: {len(adr_prerequisites)} features flagged, requiring ADR approval
  before implementation can proceed on those specific features.

  NOTE: This is NON-BLOCKING. The ideation workflow continues.
  These warnings will be included in the final specification output
  so the development team knows which ADRs to create on Day 0.
  "
  session.phases["04"].compliance_status = "warnings"
```

**VERIFY:**
- Report was displayed (either clean or with warnings)
- `session.phases["04"].compliance_status` is one of: "clean", "warnings"
- IF compliance_status is null: HALT -- "Step 4.3: Compliance report not displayed."

**RECORD:**
- `session.phases["04"].compliance_report_displayed = true`
- `session.phases["04"].compliance_status = status`
- `session.phases["04"].step_4_3_completed = true`

---

### Step 4.4: Context Window Check

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
            description: "Proceed to Phase 5"
          - label: "Save and continue later"
            description: "Create checkpoint and exit"

  IF response == "Save and continue later":
    checkpoint.progress.current_phase = 5
    checkpoint.progress.phases_completed.append("04")
    checkpoint.progress.completion_percentage = round(4/7 * 100)
    checkpoint.updated_at = "current ISO 8601 timestamp"

    Write(file_path="devforgeai/specs/ideation/${IDEATION_ID}.checkpoint.json", content=checkpoint)

    verify_result = Glob(pattern="devforgeai/specs/ideation/${IDEATION_ID}.checkpoint.json")
    IF not found: HALT -- "Step 4.4: Checkpoint save failed during session exit."

    Display: "Session saved. Resume with: /ideate --resume ${IDEATION_ID}"
    EXIT skill

  ELSE:
    Display: "Continuing in current session."
    session.phases["04"].context_check_completed = true

ELSE:
  Display: "Context window healthy ({PERCENT}%). Proceeding to Phase 5."
  session.phases["04"].context_check_completed = true
```

**VERIFY:**
- Context window check was performed
- `session.phases["04"].context_check_completed` is `true`
- IF check was skipped (value is null or false): HALT -- "Step 4.4: Context window check not performed."

**RECORD:**
- `session.phases["04"].context_check_completed = true`
- `session.phases["04"].step_4_4_completed = true`

---

## Phase Exit Verification

Before transitioning to Phase 05, verify ALL exit criteria:

```
VERIFY_EXIT:
  CHECK: session.phases["04"].compliance_checked == true
         OR session.phases["04"].mode == "greenfield_skip"
    IF FAIL: HALT -- "Exit blocked: Compliance check not performed."

  CHECK: session.completed_outputs.adr_prerequisites is not null (list, can be empty)
    IF FAIL: HALT -- "Exit blocked: ADR prerequisites list not populated."

  CHECK: session.phases["04"].compliance_report_displayed == true
         OR session.phases["04"].mode == "greenfield_skip"
    IF FAIL: HALT -- "Exit blocked: Compliance report not displayed."

  CHECK: session.phases["04"].context_check_completed == true
    IF FAIL: HALT -- "Exit blocked: Context window check not completed."
```

Update checkpoint on successful exit:
```
checkpoint.progress.current_phase = 5
checkpoint.progress.phases_completed.append("04")
checkpoint.progress.completion_percentage = round(4/7 * 100)
checkpoint.updated_at = "current ISO 8601 timestamp"

checkpoint.phases["04"] = {
  "mode": session.phases["04"].mode,
  "context_files_found": session.phases["04"].context_files_found,
  "features_analyzed": session.phases["04"].features_analyzed or 0,
  "conflicts_found": session.phases["04"].conflicts_found or 0,
  "compliance_status": session.phases["04"].compliance_status or "greenfield_skip",
  "compliance_report_displayed": session.phases["04"].compliance_report_displayed or true,
  "context_check_completed": true,
  "steps_completed": ["step_4_1", "step_4_2", "step_4_3", "step_4_4"]
}

checkpoint.completed_outputs.adr_prerequisites = session.completed_outputs.adr_prerequisites

Write(file_path="devforgeai/specs/ideation/${IDEATION_ID}.checkpoint.json", content=checkpoint)
```

**VERIFY checkpoint write:** `Glob(pattern="devforgeai/specs/ideation/${IDEATION_ID}.checkpoint.json")`
IF not found: HALT -- "Phase 04 exit checkpoint was NOT saved."

---

## Phase Transition Display

```
Display:
"
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Phase 4 Complete: Constitutional Compliance Pre-Check
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Context Files: {context_files_found}/6 found
Mode: {mode}
Compliance Status: {compliance_status}

{IF compliance_status == 'clean':
  No ADR prerequisites detected.
  All features are compatible with existing context files.
}
{IF compliance_status == 'warnings':
  ADR Prerequisites: {conflicts_found} feature(s) flagged
  These will be included as Day 0 prerequisites in the final output.
}
{IF mode == 'greenfield_skip':
  Greenfield project -- no context files to check against.
  Compliance check skipped (vacuously clean).
}

Questions Asked This Phase: 0

Proceeding to Phase 5...
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"
```

---

## Common Issues and Recovery

| Issue | Symptom | Recovery |
|-------|---------|----------|
| Context files exist but are empty | Read succeeds but content is blank | Treat as if file is missing for that check. Log in compliance report. |
| All features flagged | Every requirement triggers a warning | Likely indicates major scope change. Report accurately -- do not suppress warnings. |
| Feature uses ambiguous technology | Cannot determine if tech is in tech-stack.md | Flag conservatively as potential ADR prerequisite with "needs verification" note. |
| Greenfield with partial context | 1-5 files exist unexpectedly | Phase 01 already classified project type. Use that classification, read available files. |
