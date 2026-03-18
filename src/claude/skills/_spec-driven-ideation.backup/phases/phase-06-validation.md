# Phase 06: Self-Validation

## Contract

| Attribute | Value |
|-----------|-------|
| **PURPOSE** | Validate the generated requirements.md against quality standards, F4 schema compliance, and content completeness. Uses a validate-fix-repeat loop (max 3 retries) with auto-correction for fixable issues. |
| **REFERENCE** | `.claude/skills/discovering-requirements/references/self-validation-workflow.md` (292 lines), `.claude/skills/discovering-requirements/references/validation-checklists.md` (651 lines) |
| **STEP COUNT** | 5 mandatory steps |
| **MINIMUM QUESTIONS** | 0-1 |

## Phase Exit Criteria

Before this phase can complete, ALL of the following MUST be true:

- [ ] validation_status in [PASSED, PASSED_WITH_WARNINGS]
- [ ] Schema compliance checked (session.phases["06"].schema_check is non-null)
- [ ] Content quality scanned (session.phases["06"].quality_issues is non-null)
- [ ] Auto-fix loop completed (max 3 retries, session.phases["06"].fix_attempts recorded)
- [ ] Validation report displayed (session.phases["06"].report_displayed == true)
- [ ] Checkpoint updated with phase data
- [ ] Context window check completed (session.phases["06"].context_check_completed == true)

**IF any criterion is unmet: HALT. Do NOT proceed to Phase 07.**

---

## Reference Loading [MANDATORY]

```
Read(file_path=".claude/skills/discovering-requirements/references/self-validation-workflow.md")
Read(file_path=".claude/skills/discovering-requirements/references/validation-checklists.md")
```

IF either Read fails: HALT -- "Phase 06 reference files not loaded. Cannot proceed without validation reference material."

Do NOT rely on memory of previous reads. Load fresh every time this phase executes.

---

## Mandatory Steps

### Step 6.1: Schema Compliance Check

**EXECUTE:**
```
# Read the generated requirements file
requirements_path = session.completed_outputs.requirements_file_path

IF requirements_path is null OR requirements_path == "":
  HALT -- "Step 6.1: No requirements file path recorded. Phase 05 must generate the file before validation."

Read(file_path=requirements_path)

IF Read fails:
  HALT -- "Step 6.1: Requirements file not readable at '{requirements_path}'. File may not exist on disk."

# Parse YAML frontmatter and body content
parsed = parse_yaml_frontmatter(file_content)

# F4 Required Fields Check
f4_required_fields = [
  "functional_requirements",
  "non_functional_requirements",
  "constraints",
  "dependencies"
]

schema_errors = []
schema_warnings = []

FOR each field in f4_required_fields:
  IF field not in parsed OR parsed[field] is null:
    schema_errors.append({
      field: field,
      severity: "CRITICAL",
      message: "Required F4 field '{field}' is missing from requirements document"
    })

# Functional Requirements Structure Validation
IF "functional_requirements" in parsed AND parsed.functional_requirements is not null:
  FOR each fr in parsed.functional_requirements:
    fr_required = ["id", "description", "acceptance_criteria", "priority"]
    FOR each sub_field in fr_required:
      IF sub_field not in fr OR fr[sub_field] is null OR fr[sub_field] == "":
        schema_errors.append({
          field: "functional_requirements.{fr.id}.{sub_field}",
          severity: "HIGH",
          message: "FR '{fr.id or 'unknown'}' missing required field '{sub_field}'"
        })

# Non-Functional Requirements Structure Validation
IF "non_functional_requirements" in parsed AND parsed.non_functional_requirements is not null:
  FOR each nfr in parsed.non_functional_requirements:
    nfr_required = ["id", "category", "metric", "target"]
    FOR each sub_field in nfr_required:
      IF sub_field not in nfr OR nfr[sub_field] is null OR nfr[sub_field] == "":
        schema_errors.append({
          field: "non_functional_requirements.{nfr.id}.{sub_field}",
          severity: "HIGH",
          message: "NFR '{nfr.id or 'unknown'}' missing required field '{sub_field}'"
        })

# YAML Syntax Validation
IF yaml_parse_error occurred:
  schema_errors.append({
    field: "yaml_frontmatter",
    severity: "CRITICAL",
    message: "YAML syntax error: {parse_error_detail}"
  })

# Determine schema compliance result
critical_errors = [e for e in schema_errors WHERE e.severity == "CRITICAL"]
high_errors = [e for e in schema_errors WHERE e.severity == "HIGH"]

IF len(critical_errors) > 0:
  schema_result = "FAILED"
ELSE IF len(high_errors) > 0:
  schema_result = "FAILED"
ELSE:
  schema_result = "PASSED"

Display:
"Schema Compliance Check: {schema_result}
  Critical errors: {len(critical_errors)}
  High errors: {len(high_errors)}
  Warnings: {len(schema_warnings)}"

IF len(schema_errors) > 0:
  Display: "Errors found:"
  FOR each error in schema_errors:
    Display: "  [{error.severity}] {error.field}: {error.message}"
```

**VERIFY:**
- `schema_result` is one of: "PASSED", "FAILED"
- IF schema_result is null: HALT -- "Step 6.1: Schema compliance check did not produce a result."
- `schema_errors` list is populated (can be empty if PASSED)
- Requirements file was successfully read and parsed

**RECORD:**
- `session.phases["06"].schema_check = { result: schema_result, errors: schema_errors, warnings: schema_warnings }`
- `session.phases["06"].step_6_1_completed = true`
- Update checkpoint: `{ phase: 6, step: "6.1", status: "complete" }`

---

### Step 6.2: Content Quality Check

**EXECUTE:**
```
quality_issues = []

# Vague Terms Detection
vague_terms = ["fast", "scalable", "secure", "easy", "simple", "good",
               "better", "efficient", "robust", "reliable", "flexible",
               "user-friendly", "intuitive", "performant", "modern"]

vague_count = 0
vague_locations = []

FOR each line_number, line in enumerate(file_content.lines):
  FOR each term in vague_terms:
    IF term in line.lower() AND no quantified metric on same line:
      vague_count += 1
      vague_locations.append({
        line: line_number,
        term: term,
        context: line.strip()
      })

IF vague_count > 10:
  quality_issues.append({
    type: "vague_terms",
    severity: "HIGH",
    count: vague_count,
    message: "{vague_count} vague terms found without quantified metrics",
    locations: vague_locations[:10]  # Show first 10
  })
ELSE IF vague_count > 0:
  quality_issues.append({
    type: "vague_terms",
    severity: "MEDIUM",
    count: vague_count,
    message: "{vague_count} vague term(s) found without quantified metrics",
    locations: vague_locations
  })

# Placeholder Detection
placeholder_terms = ["TBD", "TODO", "TBC", "FIXME", "XXX", "PLACEHOLDER",
                     "to be determined", "to be confirmed", "to be completed"]

placeholder_count = 0
placeholder_locations = []

FOR each line_number, line in enumerate(file_content.lines):
  FOR each term in placeholder_terms:
    IF term.lower() in line.lower():
      placeholder_count += 1
      placeholder_locations.append({
        line: line_number,
        term: term,
        context: line.strip()
      })

IF placeholder_count >= 5:
  quality_issues.append({
    type: "placeholders",
    severity: "MEDIUM",
    count: placeholder_count,
    message: "{placeholder_count} placeholder(s) found in requirements document",
    locations: placeholder_locations
  })
ELSE IF placeholder_count > 0:
  quality_issues.append({
    type: "placeholders",
    severity: "LOW",
    count: placeholder_count,
    message: "{placeholder_count} placeholder(s) found (minor)",
    locations: placeholder_locations
  })

# Completeness Check
completeness_issues = []

fr_count = len(parsed.functional_requirements or [])
IF fr_count < 5:
  completeness_issues.append({
    type: "insufficient_frs",
    severity: "HIGH",
    message: "Only {fr_count} functional requirements. Minimum 5 expected."
  })

nfr_count = len(parsed.non_functional_requirements or [])
IF nfr_count < 1:
  completeness_issues.append({
    type: "insufficient_nfrs",
    severity: "HIGH",
    message: "No non-functional requirements found. Minimum 1 expected."
  })

constraint_count = len(parsed.constraints or [])
IF constraint_count < 1:
  completeness_issues.append({
    type: "insufficient_constraints",
    severity: "HIGH",
    message: "No constraints found. Minimum 1 expected."
  })

dependency_count = len(parsed.dependencies or [])
IF dependency_count < 1:
  completeness_issues.append({
    type: "insufficient_dependencies",
    severity: "HIGH",
    message: "No dependencies found. Minimum 1 expected."
  })

quality_issues.extend(completeness_issues)

# Duplicate Detection
seen_descriptions = []
duplicate_pairs = []

FOR each fr in parsed.functional_requirements:
  FOR each seen in seen_descriptions:
    IF string_similarity(fr.description, seen.description) > 0.85:
      duplicate_pairs.append({
        item_a: seen.id,
        item_b: fr.id,
        similarity: computed_similarity
      })
  seen_descriptions.append(fr)

IF len(duplicate_pairs) > 0:
  quality_issues.append({
    type: "duplicates",
    severity: "MEDIUM",
    count: len(duplicate_pairs),
    message: "{len(duplicate_pairs)} potential duplicate requirement(s) detected",
    pairs: duplicate_pairs
  })

Display:
"Content Quality Check:
  Vague terms: {vague_count} instance(s)
  Placeholders: {placeholder_count} instance(s)
  Completeness: FRs={fr_count}, NFRs={nfr_count}, Constraints={constraint_count}, Dependencies={dependency_count}
  Duplicates: {len(duplicate_pairs)} potential pair(s)
  Total issues: {len(quality_issues)}"
```

**VERIFY:**
- `quality_issues` list is populated (can be empty if no issues found)
- Vague terms scan completed (vague_count is a number >= 0)
- Placeholder scan completed (placeholder_count is a number >= 0)
- Completeness check completed (all 4 counts captured)
- Duplicate scan completed (duplicate_pairs is a list)
- IF quality_issues is null (not empty list, but null): HALT -- "Step 6.2: Quality scan did not execute."

**RECORD:**
- `session.phases["06"].quality_issues = quality_issues`
- `session.phases["06"].vague_term_count = vague_count`
- `session.phases["06"].placeholder_count = placeholder_count`
- `session.phases["06"].completeness = { frs: fr_count, nfrs: nfr_count, constraints: constraint_count, dependencies: dependency_count }`
- `session.phases["06"].step_6_2_completed = true`
- Update checkpoint: `{ phase: 6, step: "6.2", status: "complete" }`

---

### Step 6.3: Auto-Fix Correctable Issues (Validate-Fix-Repeat Loop)

**EXECUTE:**
```
fix_attempt = 0
max_retries = 3
fixes_applied = []

WHILE fix_attempt < max_retries:
  fix_attempt += 1
  current_fixes = []

  # Re-read file for each attempt (ensures we operate on latest content)
  Read(file_path=requirements_path)

  # ── Tier 1: Auto-Correctable (no user input needed) ──

  # Fix 1.1: Missing optional YAML fields -- insert defaults
  optional_fields = ["version", "created_date", "session_id", "project_mode"]
  FOR each field in optional_fields:
    IF field not in parsed:
      Insert default value for field
      current_fixes.append({
        tier: 1,
        type: "missing_optional_field",
        field: field,
        action: "Inserted default value"
      })

  # Fix 1.2: Formatting inconsistencies -- normalize
  IF inconsistent_indentation_detected:
    Normalize YAML indentation to 2 spaces
    current_fixes.append({
      tier: 1,
      type: "formatting",
      action: "Normalized YAML indentation to 2 spaces"
    })

  # Fix 1.3: Trailing whitespace -- trim
  IF trailing_whitespace_detected:
    Trim trailing whitespace from all lines
    current_fixes.append({
      tier: 1,
      type: "whitespace",
      action: "Trimmed trailing whitespace from {count} line(s)"
    })

  # Fix 1.4: Duplicate IDs -- renumber
  IF duplicate_ids_detected:
    Renumber duplicate FR/NFR IDs sequentially
    current_fixes.append({
      tier: 1,
      type: "duplicate_ids",
      action: "Renumbered {count} duplicate ID(s)"
    })

  # ── Tier 2: User-Resolvable (report with guidance) ──

  tier_2_issues = []

  IF vague_count > 10:
    tier_2_issues.append({
      tier: 2,
      severity: "HIGH",
      type: "excessive_vague_terms",
      message: "{vague_count} vague terms found without metrics. Consider adding quantified targets.",
      guidance: "Replace vague terms with measurable values (e.g., 'fast' -> 'response time < 200ms')"
    })

  IF fr_count < 5:
    tier_2_issues.append({
      tier: 2,
      severity: "HIGH",
      type: "insufficient_requirements",
      message: "Only {fr_count} functional requirements. Minimum 5 recommended.",
      guidance: "Review scope boundaries and user personas for additional requirements"
    })

  IF placeholder_count >= 5:
    tier_2_issues.append({
      tier: 2,
      severity: "MEDIUM",
      type: "excessive_placeholders",
      message: "{placeholder_count} placeholders remain in document.",
      guidance: "Replace TBD/TODO entries with actual values or mark as 'Deferred to Phase N'"
    })

  # ── Tier 3: Critical (HALT required) ──

  tier_3_issues = []

  IF requirements_file_missing:
    tier_3_issues.append({
      tier: 3,
      severity: "CRITICAL",
      type: "missing_file",
      message: "Requirements file does not exist at expected path"
    })

  IF yaml_syntax_error_persists:
    tier_3_issues.append({
      tier: 3,
      severity: "CRITICAL",
      type: "yaml_invalid",
      message: "YAML syntax remains invalid after auto-fix attempt {fix_attempt}"
    })

  f4_missing = [f for f in f4_required_fields IF f not in parsed OR parsed[f] is null]
  IF len(f4_missing) > 0:
    tier_3_issues.append({
      tier: 3,
      severity: "CRITICAL",
      type: "f4_fields_missing",
      message: "Required F4 fields still missing after auto-fix: {f4_missing}"
    })

  # Apply Tier 1 fixes if any
  IF len(current_fixes) > 0:
    Write(file_path=requirements_path, content=updated_content)

    # Verify write
    verify = Glob(pattern=requirements_path)
    IF not found:
      HALT -- "Step 6.3: Failed to write auto-fixed requirements file."

    fixes_applied.extend(current_fixes)
    Display: "Attempt {fix_attempt}: Applied {len(current_fixes)} auto-fix(es)"

  # Check if Tier 3 issues remain
  IF len(tier_3_issues) > 0 AND fix_attempt >= max_retries:
    Display:
    "CRITICAL: {len(tier_3_issues)} unresolvable issue(s) after {max_retries} attempts:"
    FOR each issue in tier_3_issues:
      Display: "  [CRITICAL] {issue.message}"
    HALT -- "Step 6.3: Critical validation issues cannot be auto-fixed. Manual intervention required."

  # If no Tier 3 issues, break the loop
  IF len(tier_3_issues) == 0:
    BREAK

  Display: "Retry {fix_attempt}/{max_retries}: {len(tier_3_issues)} critical issue(s) remain."

# END WHILE

# Determine validation status
IF len(tier_3_issues) > 0:
  validation_status = "FAILED"
ELSE IF len(tier_2_issues) > 0:
  high_tier2 = [i for i in tier_2_issues WHERE i.severity == "HIGH"]
  IF len(high_tier2) > 0:
    validation_status = "PASSED_WITH_WARNINGS"
  ELSE:
    validation_status = "PASSED_WITH_WARNINGS"
ELSE:
  validation_status = "PASSED"

Display:
"Validation Status: {validation_status}
  Auto-fixes applied: {len(fixes_applied)}
  Tier 2 issues (user-resolvable): {len(tier_2_issues)}
  Tier 3 issues (critical): {len(tier_3_issues)}
  Fix attempts used: {fix_attempt}/{max_retries}"
```

**VERIFY:**
- `validation_status` is one of: "PASSED", "PASSED_WITH_WARNINGS", "FAILED"
- IF validation_status == "FAILED": HALT -- "Step 6.3: Validation FAILED after {fix_attempt} attempts. Critical issues remain."
- IF validation_status is null: HALT -- "Step 6.3: Validation loop did not produce a status."
- `fix_attempt` <= `max_retries` (loop did not exceed maximum)
- `fixes_applied` list is populated (can be empty if nothing to fix)

**RECORD:**
- `session.completed_outputs.validation_status = validation_status`
- `session.phases["06"].fix_attempts = fix_attempt`
- `session.phases["06"].fixes_applied = fixes_applied`
- `session.phases["06"].tier_2_issues = tier_2_issues`
- `session.phases["06"].tier_3_issues = tier_3_issues`
- `session.phases["06"].step_6_3_completed = true`
- Update checkpoint: `{ phase: 6, step: "6.3", status: "complete" }`

---

### Step 6.4: Display Validation Report

**EXECUTE:**
```
Display:
"
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Validation Report: {IDEATION_ID}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

File: {requirements_path}
Overall Status: {validation_status}

Schema Compliance: {session.phases['06'].schema_check.result}
  {IF schema_errors: FOR each error: '  [{severity}] {message}'}
  {IF no schema_errors: '  No schema errors found.'}

Content Quality:
  Vague Terms: {vague_count} instance(s)
    {IF vague_count > 0: 'Top occurrences:'}
    {FOR each location in vague_locations[:5]: '    Line {line}: \"{term}\" in \"{context}\"'}
  Placeholders: {placeholder_count} instance(s)
    {IF placeholder_count > 0: FOR each loc in placeholder_locations[:5]: '    Line {line}: \"{term}\"'}
  Duplicates: {len(duplicate_pairs)} potential pair(s)
    {IF duplicate_pairs: FOR each pair: '    {item_a} ~ {item_b} (similarity: {similarity})'}

Completeness:
  Functional Requirements: {fr_count} {IF fr_count >= 5: '[OK]' ELSE: '[INSUFFICIENT]'}
  Non-Functional Requirements: {nfr_count} {IF nfr_count >= 1: '[OK]' ELSE: '[INSUFFICIENT]'}
  Constraints: {constraint_count} {IF constraint_count >= 1: '[OK]' ELSE: '[INSUFFICIENT]'}
  Dependencies: {dependency_count} {IF dependency_count >= 1: '[OK]' ELSE: '[INSUFFICIENT]'}

Auto-Fixes Applied ({len(fixes_applied)}):
  {IF fixes_applied: FOR each fix: '  [{fix.tier}] {fix.type}: {fix.action}'}
  {IF not fixes_applied: '  None required.'}

Remaining Issues ({len(tier_2_issues)}):
  {IF tier_2_issues: FOR each issue: '  [{issue.severity}] {issue.type}: {issue.message}'}
  {IF tier_2_issues: FOR each issue: '    Guidance: {issue.guidance}'}
  {IF not tier_2_issues: '  None.'}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"

# If PASSED_WITH_WARNINGS, optionally ask user about remaining issues
IF validation_status == "PASSED_WITH_WARNINGS" AND len(tier_2_issues) > 0:
  AskUserQuestion:
    questions:
      - question: "Validation passed with {len(tier_2_issues)} warning(s). How would you like to proceed?"
        header: "Validation Warnings"
        multiSelect: false
        options:
          - label: "Accept warnings and proceed"
            description: "Continue to handoff with current warnings noted"
          - label: "Address warnings now"
            description: "I'll fix the issues before continuing"

  IF response == "Address warnings now":
    Display: "Please address the warnings listed above."
    Display: "After making changes, re-run validation by re-entering this phase."
    # Note: User would need to edit the file manually or re-run Phase 05
    # The validation will re-execute from Step 6.1 on resume

  session.phases["06"].warnings_acknowledged = response
```

**VERIFY:**
- Validation report displayed with all sections populated
- IF validation_status == "PASSED_WITH_WARNINGS": User response captured
- Report includes: schema result, quality metrics, completeness counts, fixes applied, remaining issues

**RECORD:**
- `session.phases["06"].report_displayed = true`
- `session.phases["06"].step_6_4_completed = true`
- IF warnings: `session.phases["06"].warnings_acknowledged = response`
- Update checkpoint: `{ phase: 6, step: "6.4", status: "complete" }`

---

### Step 6.5: Context Window Check

**EXECUTE:**
```
IF estimated_context_usage > 70%:
  AskUserQuestion:
    questions:
      - question: "Context window is approximately {PERCENT}% full. Would you like to:"
        header: "Session Management"
        multiSelect: false
        options:
          - label: "Continue in this session"
            description: "Proceed to Phase 7 (Completion & Handoff)"
          - label: "Save and continue later"
            description: "Create checkpoint and exit -- resume with /ideate --resume {IDEATION_ID}"

  IF response == "Save and continue later":
    # Save checkpoint with all Phase 06 data before exit
    checkpoint.progress.current_phase = 7
    checkpoint.progress.phases_completed.append("06")
    checkpoint.progress.completion_percentage = round(6/7 * 100)
    checkpoint.updated_at = "current ISO 8601 timestamp"

    Write(file_path="devforgeai/specs/ideation/${IDEATION_ID}.checkpoint.json", content=checkpoint)

    # Verify write
    verify_result = Glob(pattern="devforgeai/specs/ideation/${IDEATION_ID}.checkpoint.json")
    IF not found: HALT -- "Step 6.5: Checkpoint save failed during session exit."

    Display: "Session saved. Resume with: /ideate --resume ${IDEATION_ID}"
    EXIT skill

  ELSE:
    Display: "Continuing in current session."
    session.phases["06"].context_check_completed = true

ELSE:
  Display: "Context window healthy ({PERCENT}%). Proceeding to Phase 7."
  session.phases["06"].context_check_completed = true
```

**VERIFY:**
- Context window check was performed (either threshold triggered or healthy confirmation)
- `session.phases["06"].context_check_completed` is `true`
- IF check was skipped (value is null or false): HALT -- "Step 6.5: Context Window Check not performed."

**RECORD:**
- `session.phases["06"].context_check_completed = true`
- `session.phases["06"].step_6_5_completed = true`
- Update checkpoint: `{ phase: 6, step: "6.5", status: "complete" }`

---

## Phase Exit Verification

Before transitioning to Phase 07, verify ALL exit criteria:

```
VERIFY_EXIT:
  CHECK: session.completed_outputs.validation_status in ["PASSED", "PASSED_WITH_WARNINGS"]
    IF FAIL: HALT -- "Exit blocked: Validation status is '{status}'. Must be PASSED or PASSED_WITH_WARNINGS."

  CHECK: session.phases["06"].schema_check is not null AND session.phases["06"].schema_check.result is not null
    IF FAIL: HALT -- "Exit blocked: Schema compliance check was not performed."

  CHECK: session.phases["06"].quality_issues is not null
    IF FAIL: HALT -- "Exit blocked: Content quality scan was not performed."

  CHECK: session.phases["06"].fix_attempts is not null AND session.phases["06"].fix_attempts <= 3
    IF FAIL: HALT -- "Exit blocked: Auto-fix loop did not complete or exceeded max retries."

  CHECK: session.phases["06"].report_displayed == true
    IF FAIL: HALT -- "Exit blocked: Validation report was not displayed."

  CHECK: session.phases["06"].context_check_completed == true
    IF FAIL: HALT -- "Exit blocked: Context window check not completed."
```

Update checkpoint on successful exit:
```
checkpoint.progress.current_phase = 7
checkpoint.progress.phases_completed.append("06")
checkpoint.progress.completion_percentage = round(6/7 * 100)
checkpoint.updated_at = "current ISO 8601 timestamp"

checkpoint.phases["06"] = {
  "schema_check": session.phases["06"].schema_check,
  "quality_issues": session.phases["06"].quality_issues,
  "fix_attempts": session.phases["06"].fix_attempts,
  "fixes_applied": session.phases["06"].fixes_applied,
  "validation_status": session.completed_outputs.validation_status,
  "report_displayed": session.phases["06"].report_displayed,
  "context_check_completed": session.phases["06"].context_check_completed,
  "steps_completed": ["step_6_1", "step_6_2", "step_6_3", "step_6_4", "step_6_5"]
}

Write(file_path="devforgeai/specs/ideation/${IDEATION_ID}.checkpoint.json", content=checkpoint)
```

**VERIFY checkpoint write:** `Glob(pattern="devforgeai/specs/ideation/${IDEATION_ID}.checkpoint.json")`
IF not found: HALT -- "Phase 06 exit checkpoint was NOT saved."

---

## Phase Transition Display

```
Display:
"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Phase 6 Complete: Self-Validation
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Validation Status: {validation_status}

Schema Compliance: {schema_check.result}
Content Quality:
  Vague Terms: {vague_count}
  Placeholders: {placeholder_count}
  Duplicates: {len(duplicate_pairs)}

Completeness:
  FRs: {fr_count} | NFRs: {nfr_count} | Constraints: {constraint_count} | Dependencies: {dependency_count}

Auto-Fixes: {len(fixes_applied)} applied in {fix_attempts} attempt(s)
Remaining Warnings: {len(tier_2_issues)}

Proceeding to Phase 7: Completion & Handoff...
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
```

---

## Common Issues and Recovery

| Issue | Symptom | Recovery |
|-------|---------|----------|
| Requirements file missing | Read fails in Step 6.1 | HALT. Phase 05 must complete first. Check requirements_file_path. |
| Invalid YAML after 3 retries | Tier 3 persists | HALT with full error report. Manual YAML fix required. |
| Excessive vague terms (>10) | HIGH Tier 2 issue | Report with guidance. User decides to fix or accept warning. |
| Fewer than 5 FRs | HIGH Tier 2 issue | Report as warning. May indicate Phase 03 was insufficient. |
| Duplicate IDs | Tier 1 auto-fixable | Renumber automatically. No user action required. |
| Write fails during auto-fix | Glob verification fails | HALT. Check file permissions and disk space. |
