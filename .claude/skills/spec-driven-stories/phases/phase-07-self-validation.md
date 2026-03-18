# Phase 07: Self-Validation

## Entry Gate

```bash
devforgeai-validate phase-check ${SESSION_ID} --workflow=stories --from=06 --to=07 --project-root=.
```

| Exit Code | Action |
|-----------|--------|
| 0 | Prerequisites met. Proceed. |
| 1 | Phase 06 incomplete. HALT. |
| 127 | CLI not installed. Proceed without enforcement. |

---

## Contract

- **PURPOSE:** Quality checks on the generated story file with auto-correction of common issues
- **REQUIRED SUBAGENTS:** none
- **REQUIRED ARTIFACTS:** Validation evidence (findings list or explicit "all checks passed" statement)
- **STEP COUNT:** 4
- **REFERENCE FILES:**
  - `references/story-validation-workflow.md`
  - `references/validation-checklists.md`

---

## Reference Loading [MANDATORY]

```
Read(file_path="src/claude/skills/spec-driven-stories/references/story-validation-workflow.md")
Read(file_path="src/claude/skills/spec-driven-stories/references/validation-checklists.md")
```

IF any Read fails: HALT -- "Phase 07 reference files not loaded."

Do NOT rely on memory of previous reads. Load ALL references fresh.

---

## Mandatory Steps (4)

### Step 7.1: Validate YAML Frontmatter

**EXECUTE:**
```
Read(file_path=$STORY_FILE_PATH)

# Extract YAML frontmatter between --- markers
frontmatter = extract_yaml(story_content)

# Validate required fields
required_fields = ["id", "title", "status", "priority", "points", "type", "created", "template_version"]
missing_fields = []

FOR each field in required_fields:
  IF field NOT in frontmatter:
    missing_fields.append(field)

IF missing_fields:
  Display: "Frontmatter missing fields: {missing_fields}"
  # Auto-correct: Add missing fields with default values
  FOR each field in missing_fields:
    Add field with appropriate default value
  Edit(file_path=$STORY_FILE_PATH, ...)
  Display: "Auto-corrected: Added {len(missing_fields)} missing frontmatter fields"

# Validate field values
IF frontmatter.id != $STORY_ID:
  HALT: "Frontmatter ID mismatch: {frontmatter.id} vs {$STORY_ID}"

IF frontmatter.template_version != "2.8":
  Display: "WARNING: Template version is {frontmatter.template_version}, expected 2.8"
```

**VERIFY:** All required frontmatter fields present and valid.

**RECORD:**
```bash
devforgeai-validate phase-record ${SESSION_ID} --workflow=stories --phase=07 --step=7.1 --project-root=.
```
Update checkpoint: `phases["07"].steps_completed.append("7.1")`

---

### Step 7.2: Validate User Story & Acceptance Criteria

**EXECUTE:**
```
# Validate user story format
Grep(pattern="As a .+ I want .+ So that", path=$STORY_FILE_PATH)
IF not found:
  Display: "WARNING: User story does not follow As a/I want/So that format"
  # Auto-correct if possible

# Validate AC format (Given/When/Then)
ac_sections = Grep(pattern="^### AC#", path=$STORY_FILE_PATH)
ac_count = count(ac_sections)

IF ac_count < 3:
  Display: "WARNING: Only {ac_count} ACs found. Minimum 3 required."
  # Cannot auto-correct ACs - they require domain knowledge

# Validate each AC has Given/When/Then
FOR each AC section:
  IF NOT contains "Given" AND "When" AND "Then":
    Display: "WARNING: AC missing Given/When/Then structure"
```

**VERIFY:** User story format valid. AC count >= 3.

**RECORD:**
```bash
devforgeai-validate phase-record ${SESSION_ID} --workflow=stories --phase=07 --step=7.2 --project-root=.
```
Update checkpoint: `phases["07"].steps_completed.append("7.2")`

---

### Step 7.3: Validate Technical Specification & NFRs

**EXECUTE:**
```
# Validate v2.0 YAML technical specification
Grep(pattern="technical_specification:", path=$STORY_FILE_PATH)
IF not found:
  Display: "WARNING: No v2.0 YAML technical specification found"

# Validate NFRs have measurable metrics
nfr_section = extract section "## Non-Functional Requirements" from story file
vague_terms = ["fast", "scalable", "reliable", "secure", "efficient", "good"]

FOR each term in vague_terms:
  IF term found in nfr_section without accompanying metric:
    Display: "WARNING: Vague NFR term '{term}' without metric"
    # Auto-correct: Add placeholder metric
    Edit to replace vague term with measurable version

# Validate no TBD/TODO placeholders
Grep(pattern="TBD|TODO|PLACEHOLDER", path=$STORY_FILE_PATH)
IF found:
  Display: "WARNING: Found placeholder text in story file"
  # Cannot auto-correct placeholders - need user input
```

**VERIFY:** Technical specification present. No vague NFR terms. No placeholders.

**RECORD:**
```bash
devforgeai-validate phase-record ${SESSION_ID} --workflow=stories --phase=07 --step=7.3 --project-root=.
```
Update checkpoint: `phases["07"].steps_completed.append("7.3")`

---

### Step 7.4: Generate Validation Summary

**EXECUTE:**
```
$VALIDATION_FINDINGS = compile all findings from steps 7.1-7.3

IF $VALIDATION_FINDINGS is empty:
  Display: "All validation checks passed. No issues found."
  $VALIDATION_RESULT = "PASSED"
ELSE:
  Display: "Validation findings ({len(findings)} items):"
  FOR each finding in $VALIDATION_FINDINGS:
    Display: "  - {finding.severity}: {finding.message}"

  auto_corrected = count findings where auto-correction applied
  remaining = count findings where auto-correction not possible

  Display: "Auto-corrected: {auto_corrected}"
  Display: "Remaining warnings: {remaining}"

  IF remaining == 0:
    $VALIDATION_RESULT = "PASSED (with auto-corrections)"
  ELSE:
    $VALIDATION_RESULT = "PASSED WITH WARNINGS"
```

**VERIFY:** `$VALIDATION_RESULT` is set and `$VALIDATION_FINDINGS` is populated (even if empty).

**RECORD:**
```bash
devforgeai-validate phase-record ${SESSION_ID} --workflow=stories --phase=07 --step=7.4 --project-root=.
```
Update checkpoint: `output.validation_passed = true`
Update checkpoint: `phases["07"].steps_completed.append("7.4")`

---

## Exit Gate

```bash
devforgeai-validate phase-complete ${SESSION_ID} --workflow=stories --phase=07 --checkpoint-passed --project-root=.
```

## Exit Verification Checklist (absorbs Phase 7-8 Gate)

- [ ] Frontmatter validation completed (Step 7.1)
- [ ] User story and AC validation completed (Step 7.2)
- [ ] Technical specification and NFR validation completed (Step 7.3)
- [ ] Validation summary generated with explicit result (Step 7.4)

**Gate Check (formerly Phase 7-8 Gate):**
```
IF $VALIDATION_RESULT is null or empty:
  HALT: "Phase 7-8 Gate FAILED: No validation evidence found."
Display: "Phase 7-8 Gate PASSED: Validation evidence confirmed ({$VALIDATION_RESULT})"
```

IF any unchecked: HALT -- "Phase 07 exit criteria not met"

## Phase Transition Display

```
Display: "Phase 07 complete. Validation result: ${VALIDATION_RESULT}"
Display: "Proceeding to Phase 08: Completion Report..."
```
