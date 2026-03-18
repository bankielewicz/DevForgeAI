# Phase 03: Technical Specification

## Entry Gate

```bash
devforgeai-validate phase-check ${SESSION_ID} --workflow=stories --from=02 --to=03 --project-root=.
```

| Exit Code | Action |
|-----------|--------|
| 0 | Prerequisites met. Proceed. |
| 1 | Phase 02 incomplete. HALT. |
| 127 | CLI not installed. Proceed without enforcement. |

---

## Contract

- **PURPOSE:** Define API contracts, data models, business rules, and dependencies using v2.0 structured YAML format
- **REQUIRED SUBAGENTS:** api-designer (CONDITIONAL - only if API endpoints detected)
- **REQUIRED ARTIFACTS:** Technical specification in v2.0 YAML format with components, business_rules, non_functional_requirements
- **STEP COUNT:** 5
- **REFERENCE FILES:**
  - `references/technical-specification-creation.md`
  - `references/technical-specification-guide.md`
  - `devforgeai/specs/STRUCTURED-FORMAT-SPECIFICATION.md` (external, read fresh)

---

## Reference Loading [MANDATORY]

```
Read(file_path="src/claude/skills/spec-driven-stories/references/technical-specification-creation.md")
Read(file_path="src/claude/skills/spec-driven-stories/references/technical-specification-guide.md")
Read(file_path="devforgeai/specs/STRUCTURED-FORMAT-SPECIFICATION.md")
```

IF any Read fails: HALT -- "Phase 03 reference files not loaded."

Do NOT rely on memory of previous reads. Load ALL references fresh.

---

## Mandatory Steps (5)

### Step 3.1: Evidence-Verification Pre-Flight (RCA-020)

**EXECUTE:**
```
# Identify target files that the technical specification will reference
target_files = extract file references from $REQUIREMENTS_OUTPUT

FOR each target_file in target_files:
  TRY:
    Read(file_path=target_file)
    Display: "Verified: {target_file} exists"
  CATCH:
    Display: "WARNING: Referenced file {target_file} does not exist"
    Remove from target_files list
```

**VERIFY:** All referenced target files have been verified (existing or removed from references).

**RECORD:**
```bash
devforgeai-validate phase-record ${SESSION_ID} --workflow=stories --phase=03 --step=3.1 --project-root=.
```
Update checkpoint: `phases["03"].steps_completed.append("3.1")`

---

### Step 3.2: Detect API Needs

**EXECUTE:**
```
# Scan requirements output for API indicators
api_indicators = ["endpoint", "API", "REST", "GraphQL", "gRPC", "HTTP", "POST", "GET", "PUT", "DELETE"]
api_detected = false

FOR each indicator in api_indicators:
  IF indicator found in $REQUIREMENTS_OUTPUT (case-insensitive):
    api_detected = true
    break

Display: "API endpoints detected: {api_detected}"
```

**VERIFY:** `api_detected` is boolean.

**RECORD:**
```bash
devforgeai-validate phase-record ${SESSION_ID} --workflow=stories --phase=03 --step=3.2 --project-root=.
```
Update checkpoint: `phases["03"].steps_completed.append("3.2")`

---

### Step 3.3: Invoke api-designer (CONDITIONAL)

**EXECUTE:**
```
IF api_detected == true:
  # Pre-invocation snapshot
  pre_snapshot_count = count files in workspace

  # Read contract
  Read(file_path="src/claude/skills/spec-driven-stories/contracts/api-designer-contract.yaml")

  # Invoke api-designer subagent
  Agent(subagent_type="api-designer") with prompt:
    - Feature: $FEATURE_DESCRIPTION
    - Requirements: $REQUIREMENTS_OUTPUT
    - Format: v2.0 structured YAML
    - Instructions: Generate API contracts, endpoints, request/response schemas

  $API_SPEC = captured output

  # Post-invocation verification
  post_snapshot_count = count files in workspace
  IF post_snapshot_count > pre_snapshot_count:
    Display: "WARNING: api-designer created unauthorized files"

ELSE:
  $API_SPEC = null
  Display: "No API endpoints detected. Skipping api-designer invocation."
```

**VERIFY:** If api_detected, `$API_SPEC` contains API contract YAML. If not api_detected, step explicitly skipped.

**RECORD:**
```bash
devforgeai-validate phase-record ${SESSION_ID} --workflow=stories --phase=03 --step=3.3 --project-root=.
```
Update checkpoint: `phases["03"].steps_completed.append("3.3")`

---

### Step 3.4: Generate Technical Specification (v2.0 YAML)

**EXECUTE:**
```
# Build v2.0 structured YAML technical specification
# Reference: STRUCTURED-FORMAT-SPECIFICATION.md for complete schema

$TECH_SPEC = construct YAML block with:
  technical_specification:
    components:
      - For each component identified in requirements:
        - name, type (Service/Worker/Configuration/API/Repository/DataModel/Logging)
        - description, file_path, dependencies
        - test_requirement (what to test for this component)
    business_rules:
      - For each business rule identified:
        - name, description, validation_logic
        - test_requirement
    non_functional_requirements:
      - For each NFR from Phase 02:
        - category, requirement, metric, threshold

IF $API_SPEC is not null:
  Merge API contracts into components section

Display: "Technical specification generated (v2.0 YAML format)"
Display: "  Components: {component_count}"
Display: "  Business rules: {rule_count}"
Display: "  NFRs: {nfr_count}"
```

**VERIFY:** `$TECH_SPEC` contains valid YAML with `components`, `business_rules`, and `non_functional_requirements` keys.

**RECORD:**
```bash
devforgeai-validate phase-record ${SESSION_ID} --workflow=stories --phase=03 --step=3.4 --project-root=.
```
Update checkpoint: `phases["03"].steps_completed.append("3.4")`

---

### Step 3.5: Identify Dependencies

**EXECUTE:**
```
# Extract dependencies from technical specification
$DEPENDENCIES = {
  prerequisite_stories: [],  # STORY-NNN that must complete first
  external_dependencies: [], # External services, APIs
  technology_dependencies: [] # Libraries, frameworks from tech-stack.md
}

# Validate technology dependencies against tech-stack.md
Read(file_path="devforgeai/specs/context/tech-stack.md")
FOR each tech_dep in $DEPENDENCIES.technology_dependencies:
  IF tech_dep NOT found in tech-stack.md:
    HALT: "Technology {tech_dep} not in tech-stack.md. Cannot proceed without ADR."
```

**VERIFY:** Dependencies list populated. All technology dependencies in tech-stack.md.

**RECORD:**
```bash
devforgeai-validate phase-record ${SESSION_ID} --workflow=stories --phase=03 --step=3.5 --project-root=.
```
Update checkpoint: `phases["03"].steps_completed.append("3.5")`

---

## Exit Gate

```bash
devforgeai-validate phase-complete ${SESSION_ID} --workflow=stories --phase=03 --checkpoint-passed --project-root=.
```

## Exit Verification Checklist

- [ ] Technical specification in v2.0 YAML format
- [ ] At least 1 component defined
- [ ] Business rules section present (may be empty for simple stories)
- [ ] NFR section present with measurable metrics
- [ ] All technology dependencies validated against tech-stack.md
- [ ] If API detected: api-designer output integrated

IF any unchecked: HALT -- "Phase 03 exit criteria not met"

## Phase Transition Display

```
Display: "Phase 03 complete. Technical specification generated."
Display: "Proceeding to Phase 04: UI Specification..."
```
