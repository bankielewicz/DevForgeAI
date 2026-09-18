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
- **STEP COUNT:** 9
- **REFERENCE FILES:**
  - `references/story-validation-workflow.md`
  - `references/validation-checklists.md`
  - `assets/templates/story-template.md`

---

## Reference Loading [MANDATORY]

```
Read(file_path=".claude/skills/spec-driven-stories/references/story-validation-workflow.md")
Read(file_path=".claude/skills/spec-driven-stories/references/validation-checklists.md")
$TEMPLATE_CONTENT = Read(file_path=".claude/skills/spec-driven-stories/assets/templates/story-template.md")
```

IF any of the 3 Read calls fails: HALT -- "Phase 07 reference files not loaded."

---

## Mandatory Steps (9)

### Step 7.1: Validate YAML Frontmatter

**EXECUTE:**
```
# Sprint 3.4 — Cache story content in-context for Step 7.5 reuse.
# $STORY_CONTENT_FRESH is reset to true on Read; set to false if any Edit fires
# during this phase. Step 7.5 re-reads only when stale.
$STORY_CONTENT = Read(file_path=$STORY_FILE_PATH)
$STORY_CONTENT_FRESH = true

# Extract YAML frontmatter between --- markers
frontmatter = extract_yaml($STORY_CONTENT)

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
  $STORY_CONTENT_FRESH = false   # Sprint 3.4 — cache invalidated by Edit
  Display: "Auto-corrected: Added {len(missing_fields)} missing frontmatter fields"

# Validate field values
IF frontmatter.id != $STORY_ID:
  HALT: "Frontmatter ID mismatch: {frontmatter.id} vs {$STORY_ID}"

# TCR-003: Dynamic version extraction -- hardcoded version strings FORBIDDEN
$EXPECTED_VERSION = extract_yaml($TEMPLATE_CONTENT).template_version
IF frontmatter.template_version != $EXPECTED_VERSION:
  # Backward-compatible: version mismatch is WARNING, not HALT -- older stories should still validate
  Display: "WARNING: Template version is {frontmatter.template_version}, expected {$EXPECTED_VERSION}"
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

### Steps 7.2.5 - 7.2.7 + 7.3.5 - 7.3.7: Delegated Validation (story-self-validator terminal subagent)

**EXECUTE:** Delegate the 6 RCA-050/FM-4/FM-5 remediation steps to the `story-self-validator` terminal subagent in a single batched Task() call. The subagent validates 7.2.5 + 7.2.6 + 7.2.7 + 7.3.5 + 7.3.6 + 7.3.7 read-only; returns per_step findings; primary unpacks and fires Display+VERIFY+RECORD per-substep below (preserves phase-state CLI chain). Steps 7.3, 7.4, 7.5 stay in primary (Edit auto-correction, CLI gates, HALT validations) and use $VALIDATION_FINDINGS as their authoritative findings list.

```
findings_batch = Task(subagent_type="story-self-validator", prompt=f"""
  STORY_ID: ${STORY_ID}
  STORY_FILE: ${STORY_FILE_PATH}
  EPIC_FILE: ${EPIC_FILE_PATH}  # null if standalone story

  Validate the 6 RCA-050/FM-4/FM-5 substeps. Return per_step JSON per your contract:
    - 7.2.5: Epic AC fidelity (AC count, branch preservation, threshold drift, DoD coverage)
    - 7.2.6: Pseudocode pattern sanity (Glob each pattern; >0 matches OR GROUNDED-EMPTY-SET)
    - 7.2.7: implements attribute consistency (COMP-NNN refs in tech_spec)
    - 7.3.5: Provenance depth (origin count >=2 for epic-linked; brainstorm trace)
    - 7.3.6: NFR provenance (numeric NFR targets have citations)
    - 7.3.7: Cross-section consistency (COMP-REQ thresholds match AC numeric values)

  IMPORTANT: Read STORY_FILE and EPIC_FILE fresh from disk (no cached state — Sprint 3.3 caveat).
  Read-only — do not Write or Edit any files.
  """)
state = parse_json(findings_batch)
```

### Step 7.2.5: Epic AC Fidelity (delegated)

**EXECUTE:** Surface epic-fidelity findings.
```
findings_7_2_5 = state["per_step"]["7.2.5"]["findings"]
$VALIDATION_FINDINGS.extend(findings_7_2_5)
IF state["per_step"]["7.2.5"].get("skipped"):
    Display: f"  Epic AC fidelity: SKIPPED ({state['per_step']['7.2.5']['skipped']})"
ELSE:
    Display: f"  Epic AC fidelity: {len(findings_7_2_5)} findings"
```

**VERIFY:** state["per_step"]["7.2.5"] is a dict with findings list.

**RECORD:**
```bash
devforgeai-validate phase-record ${SESSION_ID} --workflow=stories --phase=07 --step=7.2.5 --project-root=.
```
Update checkpoint: `phases["07"].steps_completed.append("7.2.5")`

---

### Step 7.2.6: AC Pseudocode Pattern Sanity (delegated)

**EXECUTE:** Surface pseudocode-pattern findings.
```
findings_7_2_6 = state["per_step"]["7.2.6"]["findings"]
$VALIDATION_FINDINGS.extend(findings_7_2_6)
Display: f"  Pseudocode pattern sanity: {len(findings_7_2_6)} findings"
```

**VERIFY:** state["per_step"]["7.2.6"] is a dict with findings list.

**RECORD:**
```bash
devforgeai-validate phase-record ${SESSION_ID} --workflow=stories --phase=07 --step=7.2.6 --project-root=.
```
Update checkpoint: `phases["07"].steps_completed.append("7.2.6")`

---

### Step 7.2.7: implements Attribute Consistency (delegated)

**EXECUTE:** Surface implements-consistency findings.
```
findings_7_2_7 = state["per_step"]["7.2.7"]["findings"]
$VALIDATION_FINDINGS.extend(findings_7_2_7)
Display: f"  implements consistency: {len(findings_7_2_7)} findings"
```

**VERIFY:** state["per_step"]["7.2.7"] is a dict with findings list.

**RECORD:**
```bash
devforgeai-validate phase-record ${SESSION_ID} --workflow=stories --phase=07 --step=7.2.7 --project-root=.
```
Update checkpoint: `phases["07"].steps_completed.append("7.2.7")`

---

### Step 7.3: Validate Technical Specification & NFRs

**EXECUTE:**
```
# Sprint A (STORY-646): CLI validator for structured v2.0 tech spec
# Distinct from Step 7.3.6 (NFR provenance). Each uses its own fallback stub.
cli_result = Bash(f"devforgeai-validate validate-tech-spec --story-file={$STORY_FILE_PATH} --format=json")
IF cli_result.exit_code == 0:
  Display: "Tech spec structure: VALID (validate-tech-spec CLI, STORY-646)"
ELSE IF cli_result.exit_code == 1:
  cli_parsed = json_parse(cli_result.stdout)
  FOR each err in cli_parsed.errors:
    Display: f"  HIGH: Tech spec error: {err}"
  $VALIDATION_FINDINGS.append({"severity": "HIGH", "message": f"Tech spec validation: {cli_parsed.error_count} error(s)"})
ELSE IF cli_result.exit_code == 127:
  Display: "WARNING: validate-tech-spec CLI not installed — skipping structured validation (exit 127)"

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

# Implementation Guide validation (warning-level only) — STORY-580
# Conditional: only validates when Implementation Guide is present in story file
# These checks are non-blocking: emit WARNING, do not HALT
IF Grep(pattern="## Implementation Guide", path=$STORY_FILE_PATH):
  # Check Implementation Guide subsection count
  guide_subsection_count = count ### headers between ## Implementation Guide and next ## header
  IF guide_subsection_count < 2:
    Display: "WARNING: Implementation Guide has fewer than 2 subsections ({guide_subsection_count} found)"

# <implementation> element validation (warning-level only) — STORY-580
impl_blocks = Grep(pattern="<implementation>", path=$STORY_FILE_PATH, output_mode="count")
IF impl_blocks > 0:
  # Verify each implementation element contains required sub-elements
  approach_blocks = Grep(pattern="<approach>", path=$STORY_FILE_PATH, output_mode="count")
  IF approach_blocks < impl_blocks:
    Display: f"WARNING: {impl_blocks - approach_blocks} <implementation> element(s) missing required <approach> sub-element"
```

**VERIFY:** Technical specification present. No vague NFR terms. No placeholders.

**RECORD:**
```bash
devforgeai-validate phase-record ${SESSION_ID} --workflow=stories --phase=07 --step=7.3 --project-root=.
```
Update checkpoint: `phases["07"].steps_completed.append("7.3")`

---

### Step 7.3.5: Provenance Depth (delegated)

**EXECUTE:** Surface provenance-depth findings (state already populated by Steps 7.2.5-7.2.7 batched Task call above).
```
findings_7_3_5 = state["per_step"]["7.3.5"]["findings"]
$VALIDATION_FINDINGS.extend(findings_7_3_5)
IF state["per_step"]["7.3.5"].get("skipped"):
    Display: f"  Provenance depth: SKIPPED ({state['per_step']['7.3.5']['skipped']})"
ELSE:
    Display: f"  Provenance depth: {len(findings_7_3_5)} findings"
```

**VERIFY:** state["per_step"]["7.3.5"] is a dict with findings list.

**RECORD:**
```bash
devforgeai-validate phase-record ${SESSION_ID} --workflow=stories --phase=07 --step=7.3.5 --project-root=.
```
Update checkpoint: `phases["07"].steps_completed.append("7.3.5")`

---

### Step 7.3.6: NFR Provenance (delegated)

**EXECUTE:** Surface NFR-provenance findings.
```
findings_7_3_6 = state["per_step"]["7.3.6"]["findings"]
$VALIDATION_FINDINGS.extend(findings_7_3_6)
Display: f"  NFR provenance: {len(findings_7_3_6)} findings"
```

**VERIFY:** state["per_step"]["7.3.6"] is a dict with findings list.

**RECORD:**
```bash
devforgeai-validate phase-record ${SESSION_ID} --workflow=stories --phase=07 --step=7.3.6 --project-root=.
```
Update checkpoint: `phases["07"].steps_completed.append("7.3.6")`

---

### Step 7.3.7: Cross-Section Consistency (delegated)

**EXECUTE:** Surface cross-section consistency findings + emit validator summary.
```
findings_7_3_7 = state["per_step"]["7.3.7"]["findings"]
$VALIDATION_FINDINGS.extend(findings_7_3_7)
Display: f"  Cross-section consistency: {len(findings_7_3_7)} findings"
Display: ""
Display: f"Validator summary (6 sub-steps): {state['steps_passed']}/{state['steps_total']} passed, {len(state['findings'])} total findings appended"
```

**VERIFY:** state["per_step"]["7.3.7"] is a dict with findings list; state.steps_total == 6.

**RECORD:**
```bash
devforgeai-validate phase-record ${SESSION_ID} --workflow=stories --phase=07 --step=7.3.7 --project-root=.
```
Update checkpoint: `phases["07"].steps_completed.append("7.3.7")`

---

### Step 7.4: Generate Validation Summary

**EXECUTE:**
```
$VALIDATION_FINDINGS = compile all findings from steps 7.1-7.3.7

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

**PERSIST FINDINGS (Sprint 2.6 — was discarded; now full-fidelity for /qa consumption):**

```
# Write the full $VALIDATION_FINDINGS list to disk so downstream consumers
# (spec-driven-qa, framework-analyst, manual review) can re-derive root causes
# without re-running validation. Previously only the boolean result persisted.

findings_dir  = "devforgeai/workflows/validation-findings"
findings_file = f"{findings_dir}/{SESSION_ID}-validation.json"

findings_payload = {
  "schema_version": "1.0",
  "session_id":          $SESSION_ID,
  "story_id":            $STORY_ID,
  "story_file":          $STORY_FILE_PATH,
  "validation_run_at":   <current ISO 8601 UTC timestamp>,
  "validation_result":   $VALIDATION_RESULT,
  "finding_count":       len($VALIDATION_FINDINGS),
  "findings":            $VALIDATION_FINDINGS  # full list, NOT a boolean reduction
}

# Ensure parent directory exists (safe; idempotent)
Bash("mkdir -p devforgeai/workflows/validation-findings")

# Atomic write
Write(file_path=findings_file, content=json_serialize(findings_payload, indent=2))

Display: "Persisted {len($VALIDATION_FINDINGS)} validation finding(s) to {findings_file}"
```

<!-- Cross-skill contract: spec-driven-qa Phase 02 reads devforgeai/workflows/validation-findings/SC-*-validation.json (absence treated as "no story-creation findings"; not an error). -->


**RECORD:**
```bash
devforgeai-validate phase-record ${SESSION_ID} --workflow=stories --phase=07 --step=7.4 --project-root=.
```
Update checkpoint: `output.validation_passed = true`
Update checkpoint: `output.validation_findings_file = "devforgeai/workflows/validation-findings/${SESSION_ID}-validation.json"`
Update checkpoint: `phases["07"].steps_completed.append("7.4")`

---

### Step 7.5: Self-Containment Validation (Content Quality Gate)

**EXECUTE:**
```
# Sprint 3.4 — Reuse $STORY_CONTENT cached in Step 7.1; re-read only when stale
# (Step 7.1 Edit auto-correct invalidated the cache).
IF $STORY_CONTENT_FRESH != true:
  $STORY_CONTENT = Read(file_path=$STORY_FILE_PATH)
  $STORY_CONTENT_FRESH = true

# Check 1: No dangling external references
external_ref_patterns = ["see plan file", "schema defined in", "refer to", "defined in external", "see .claude/plans/"]
FOR each pattern in external_ref_patterns:
  IF pattern found in story content (case-insensitive):
    HALT: "Story references external file. Embed the referenced content or remove the reference. Pattern found: '{pattern}'"

# Check 2: Schema embedding (if tech spec has DataModel or Configuration components)
IF story contains "type: \"DataModel\"" OR "type: \"Configuration\"" in technical_specification:
  IF story does NOT contain a JSON schema block (```json with field definitions) AND does NOT contain a field-by-field schema table:
    HALT: "Story has DataModel/Configuration component but no embedded schema definition. Embed the complete schema with field names, types, and constraints."

# Check 3: CLI specification (if tech spec references CLI commands)
IF story contains "cli.py" OR "commands/" in component file_path fields:
  IF story does NOT contain CLI argument definitions (flags, types, defaults, exit codes):
    HALT: "Story has CLI component but no embedded CLI specification. Embed command definitions with flags, types, defaults, and exit codes."

# Check 4: Concrete examples (if story >= 5 points)
IF $POINTS >= 5:
  IF story does NOT contain at least 1 concrete data example (```json block with actual values, not placeholders):
    HALT: "Story is >= 5 points but contains no concrete data examples. Embed at least 1 valid data example."

# Sprint 2.8: 5 CLI-validated HALT checks (exit 0=clean, 1=HALT, 2=validator error)

# Check 5: Aspirational language (Sprint 2.3)
result = Bash("devforgeai-validate detect-aspirational-language " \
              "--story-file=" + $STORY_FILE_PATH + " --format=json")
IF result.exit_code == 1:
  HALT: "Story contains aspirational language. /dev cannot execute aspirational " \
        "requirements. Fix each violation listed in: {result.violations}."
IF result.exit_code == 2:
  HALT: "detect-aspirational-language validator error: {result.error}"

# Check 6: Ambiguous qualifiers (Sprint 2.4)
result = Bash("devforgeai-validate detect-ambiguous-qualifiers " \
              "--story-file=" + $STORY_FILE_PATH + " --format=json")
IF result.exit_code == 1:
  HALT: "Story uses ambiguous qualifiers without measurable backing. " \
        "Add a numeric measurement, citation, or comparison operator to each. " \
        "Violations: {result.violations}."
IF result.exit_code == 2:
  HALT: "detect-ambiguous-qualifiers validator error: {result.error}"

# Check 7: Stub references (Sprint 2.5)
result = Bash("devforgeai-validate detect-stub-references " \
              "--story-file=" + $STORY_FILE_PATH + " --format=json")
IF result.exit_code == 1:
  HALT: "Story contains stub references in requirement contexts. " \
        "Replace each with the concrete specification. " \
        "Violations: {result.violations}."
IF result.exit_code == 2:
  HALT: "detect-stub-references validator error: {result.error}"

# Check 8: Implementation hint presence per AC (Target B #7, cross-check from Phase 02)
# Sprint 4 patch — PRIMARY path: CLI validator replaces the coarse inline count-check.
# Contract: src/claude/scripts/devforgeai_cli/validators/implementation_hints.py
# STRICTER than the prior inline check — also verifies <approach> child presence
# (master plan Target B #7 requires <implementation> with at least <approach>).
# Exit codes: 0 = clean, 1 = violations (HALT), 2 = IO, 127 = CLI absent.
cli_result = Bash(f"devforgeai-validate validate-implementation-hints-presence --story-file={$STORY_FILE_PATH} --format=json")

IF cli_result.exit_code == 0:
  Display: "Check 8: All ACs have <implementation><approach> (Sprint 4 patch, Target D #8)"
ELSE IF cli_result.exit_code == 1:
  cli_parsed = json_parse(cli_result.stdout)
  HALT: f"Check 8: {cli_parsed.violation_count}/{cli_parsed.ac_count} AC(s) missing " \
        f"<implementation> or <approach> (Target B #7). " \
        f"Violations: {cli_parsed.violations}. " \
        "Fix each AC via Phase 05 Step 5.3 embed-XML clause or direct edit."
ELSE IF cli_result.exit_code == 127:
  # CLI absent — inline fallback (deprecated, coarse count-only check).
  ac_count             = count "<acceptance_criteria" elements in story content
  implementation_count = count "<implementation>" elements in story content
  IF ac_count > 0 AND implementation_count < ac_count:
    missing_in_story = identify ACs in story missing <implementation>
    HALT: "Story file is missing <implementation> blocks that Phase 02 produced. " \
          "Phase 05 Step 5.3 must embed every Phase-02 <implementation> block. " \
          "Missing in story file for ACs: {missing_in_story}. " \
          "Re-run Phase 05 Step 5.3 with the embed-XML clause active."
ELSE:
  HALT: f"Check 8 CLI unexpected exit {cli_result.exit_code}: {cli_result.stdout}"

# Check 9: Epic provenance text inline (cross-check from Phase 05 Sprint 2.7)
IF $EPIC_ID is not null:
  IF story does NOT contain "### Epic Feature" subsection in ## Provenance:
    HALT: "Story is epic-linked ({EPIC_ID}) but ## Provenance lacks the " \
          "embedded '### Epic Feature' subsection. /dev cannot read the epic " \
          "file from a fresh session. Re-run Phase 05 Step 5.3 with the " \
          "epic-feature-embed clause (Sprint 2.7) active."
```

**VERIFY:** All 9 self-containment checks pass. Story is implementable by a fresh /dev session without external file dependencies, with zero aspirational language, zero ambiguous qualifiers, zero stub references, embedded `<implementation>` per AC, and inline epic feature text when epic-linked.

**RECORD:**
```bash
devforgeai-validate phase-record ${SESSION_ID} --workflow=stories --phase=07 --step=7.5 --project-root=.
```
Update checkpoint: `phases["07"].steps_completed.append("7.5")`

---

## Exit Gate

```bash
devforgeai-validate phase-complete ${SESSION_ID} --workflow=stories --phase=07 --checkpoint-passed --project-root=.
```

## Exit Verification Checklist (absorbs Phase 7-8 Gate)

- [ ] Frontmatter validation completed (Step 7.1)
- [ ] User story and AC validation completed (Step 7.2)
- [ ] Epic AC fidelity check completed or skipped (Step 7.2.5) — (RCA-050)
- [ ] Technical specification and NFR validation completed (Step 7.3)
- [ ] Provenance depth assessment completed (Step 7.3.5) — (RCA-049)
- [ ] NFR provenance check completed (Step 7.3.6) — (RCA-050)
- [ ] Cross-section consistency check completed (Step 7.3.7) — (RCA-050)
- [ ] Validation summary generated with explicit result (Step 7.4)
- [ ] Validation findings persisted to `devforgeai/workflows/validation-findings/${SESSION_ID}-validation.json` (Step 7.4, Sprint 2.6)
- [ ] Self-containment Check 1: No external file references
- [ ] Self-containment Check 2: Schemas embedded (if DataModel/Configuration)
- [ ] Self-containment Check 3: CLI specs embedded (if applicable)
- [ ] Self-containment Check 4: Concrete data example (if ≥5 points)
- [ ] Self-containment Check 5: No aspirational language (Sprint 2.3)
- [ ] Self-containment Check 6: No ambiguous qualifiers without backing (Sprint 2.4)
- [ ] Self-containment Check 7: No stub references in requirement sections (Sprint 2.5)
- [ ] Self-containment Check 8: `<implementation>` block present per AC in story file (Sprint 2.1 + 2.2)
- [ ] Self-containment Check 9: Epic feature text embedded inline in ## Provenance (Sprint 2.7, when epic-linked)

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

## Hook-backed OUT-Attestation

This phase has Phase-D dispatch entries in `subagent_out_attestation_registry.json`. When dispatching those named subagents, instruct them to return a `subagent-result-v1` result that includes `coverage_attestation` in the normal response. Phase completion is blocked by `subagent-out-attestation-gate.sh` when the hook-owned ledger line lacks `coverage_attestation_present:true`. This Phase-D path is OUT-attestation-only and does not require `tmp/<WORK_ID>/handoffs/`.
