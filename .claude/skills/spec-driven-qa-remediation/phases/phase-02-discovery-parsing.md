# Phase 02: Discovery & Parsing

## Entry Gate

```bash
source .venv/bin/activate && devforgeai-validate phase-check ${SESSION_ID} --workflow=qa-remediation --from=01 --to=02 --project-root=. 2>&1
```

| Exit Code | Action |
|-----------|--------|
| 0 | Phase 01 complete. Proceed. |
| 1 | Phase 01 incomplete. HALT. |
| 2 | Validation error. HALT. |
| 127 | CLI not installed. Proceed without enforcement. |

---

## Contract

| Field | Value |
|-------|-------|
| **PURPOSE** | Find, parse, and normalize all gap files from configured sources |
| **REFERENCE** | `references/gap-discovery-workflow.md` |
| **STEP COUNT** | 5 mandatory steps |

---

## Phase Exit Criteria

- [ ] `$GAP_FILES` array populated with at least 1 file path
- [ ] `$ALL_GAPS` array populated with normalized entries
- [ ] `$FILES_PROCESSED` count > 0
- [ ] `$TOTAL_GAPS` count > 0
- [ ] Checkpoint updated with phase 02 data

IF any unchecked: HALT -- "Phase 02 exit criteria not met"

---

## Reference Loading [MANDATORY]

```
Read(file_path="src/claude/skills/spec-driven-qa-remediation/references/gap-discovery-workflow.md")
```

IF Read fails: HALT -- "Phase 02 reference file not loaded. Cannot proceed without gap discovery workflow reference."

Do NOT rely on memory of previous reads. Load reference fresh.

---

## Mandatory Steps (5)

### Step 2.1: Load Reference

**EXECUTE:**
```
Read(file_path="src/claude/skills/spec-driven-qa-remediation/references/gap-discovery-workflow.md")

Parse and internalize:
  - Source path resolution rules (local, imports, all)
  - JSON parsing requirements
  - Gap type schemas (coverage_gaps, anti_pattern_violations, code_quality_violations, deferral_issues)
  - Unified gap list construction algorithm
  - Backward compatibility rules (missing "blocking" field defaults to true)
  - Error handling (invalid JSON, missing fields, empty files)

Display: "Gap discovery reference loaded"
```

**VERIFY:** Reference content loaded and contains "Source Path Resolution", "JSON Parsing", and "Unified Gap List Construction" sections.

**RECORD:**
```bash
source .venv/bin/activate && devforgeai-validate phase-record ${SESSION_ID} --workflow=qa-remediation --phase=02 --step=2.1 --project-root=. 2>&1
```
Update checkpoint: `phases["02"].steps_completed.append("2.1")`

---

### Step 2.2: Glob Gap Files

**EXECUTE:**
```
$GAP_FILES = []

# Execute glob patterns based on $SOURCE (set in Phase 01)
IF $SOURCE == "local" OR $SOURCE == "all":
    local_results = Glob(pattern="devforgeai/qa/reports/*-gaps.json")
    $GAP_FILES.extend(local_results)

IF $SOURCE == "imports" OR $SOURCE == "all":
    import_results = Glob(pattern="devforgeai/qa/imports/**/*-gaps.json")
    $GAP_FILES.extend(import_results)

# Deduplicate (in case of overlapping patterns)
$GAP_FILES = unique($GAP_FILES)

Display: "Discovered ${len($GAP_FILES)} gap file(s):"
FOR file in $GAP_FILES:
    Display: "  - {file}"

IF len($GAP_FILES) == 0:
    HALT: "No gap files found. Ensure QA reports exist or import external gap files."
```

**VERIFY:** `$GAP_FILES` contains at least 1 file path. No duplicates.

**RECORD:**
```bash
source .venv/bin/activate && devforgeai-validate phase-record ${SESSION_ID} --workflow=qa-remediation --phase=02 --step=2.2 --project-root=. 2>&1
```
Update checkpoint: `phases["02"].steps_completed.append("2.2")`

---

### Step 2.3: Parse Each Gap File

**EXECUTE:**
```
$PARSED_DATA = []
$PARSE_ERRORS = []
$FILES_PROCESSED = 0

FOR each gap_file in $GAP_FILES:
    content = Read(file_path=gap_file)

    TRY:
        gap_data = JSON.parse(content)

        # Validate root-level required fields
        IF "story_id" not in gap_data:
            $PARSE_ERRORS.append({file: gap_file, error: "Missing required field: story_id"})
            Display: "Warning: Skipping {gap_file} - missing story_id"
            CONTINUE

        IF "qa_result" not in gap_data:
            $PARSE_ERRORS.append({file: gap_file, error: "Missing required field: qa_result"})
            Display: "Warning: Skipping {gap_file} - missing qa_result"
            CONTINUE

        # Extract gap arrays (all optional at root level)
        gap_data.coverage_gaps = gap_data.coverage_gaps OR []
        gap_data.anti_pattern_violations = gap_data.anti_pattern_violations OR []
        gap_data.code_quality_violations = gap_data.code_quality_violations OR []
        gap_data.deferral_issues = gap_data.deferral_issues OR []

        $PARSED_DATA.append({
            file_path: gap_file,
            story_id: gap_data.story_id,
            qa_result: gap_data.qa_result,
            coverage_gaps: gap_data.coverage_gaps,
            anti_pattern_violations: gap_data.anti_pattern_violations,
            code_quality_violations: gap_data.code_quality_violations,
            deferral_issues: gap_data.deferral_issues
        })
        $FILES_PROCESSED += 1
        Display: "Parsed: {gap_file} (story: {gap_data.story_id}, result: {gap_data.qa_result})"

    CATCH JSON parse error:
        $PARSE_ERRORS.append({file: gap_file, error: "Invalid JSON"})
        Display: "Warning: Skipping {gap_file} - Invalid JSON"
        CONTINUE

IF $FILES_PROCESSED == 0:
    HALT: "No gap files were successfully parsed. Check file format."

Display: "Successfully parsed ${FILES_PROCESSED} of ${len($GAP_FILES)} files"
IF len($PARSE_ERRORS) > 0:
    Display: "Parse errors: ${len($PARSE_ERRORS)} file(s) skipped"
```

**VERIFY:** `$FILES_PROCESSED > 0`. `$PARSED_DATA` has at least 1 entry.

**RECORD:**
```bash
source .venv/bin/activate && devforgeai-validate phase-record ${SESSION_ID} --workflow=qa-remediation --phase=02 --step=2.3 --project-root=. 2>&1
```
Update checkpoint: `phases["02"].steps_completed.append("2.3")`

---

### Step 2.4: Validate Gap Structure

**EXECUTE:**
```
$VALIDATION_WARNINGS = []

FOR each parsed in $PARSED_DATA:

    # Validate coverage_gaps entries
    FOR each gap in parsed.coverage_gaps:
        required = ["file", "layer", "current_coverage", "target_coverage"]
        FOR field in required:
            IF field not in gap:
                $VALIDATION_WARNINGS.append("coverage_gap in {parsed.file_path}: missing {field}")
                Mark gap as INVALID

        # Backward compatibility: missing "blocking" field defaults to true
        IF "blocking" not in gap:
            gap.blocking = true

    # Validate anti_pattern_violations entries
    FOR each gap in parsed.anti_pattern_violations:
        required = ["file", "type", "severity"]
        FOR field in required:
            IF field not in gap:
                $VALIDATION_WARNINGS.append("anti_pattern in {parsed.file_path}: missing {field}")
                Mark gap as INVALID

        # Backward compatibility: missing "blocking" field defaults to true
        IF "blocking" not in gap:
            gap.blocking = true

    # Validate code_quality_violations entries
    FOR each gap in parsed.code_quality_violations:
        required = ["file", "metric", "severity"]
        FOR field in required:
            IF field not in gap:
                $VALIDATION_WARNINGS.append("code_quality in {parsed.file_path}: missing {field}")
                Mark gap as INVALID

        # Backward compatibility: missing "blocking" field defaults to true
        IF "blocking" not in gap:
            gap.blocking = true

    # Validate deferral_issues entries
    FOR each gap in parsed.deferral_issues:
        required = ["item", "severity"]
        FOR field in required:
            IF field not in gap:
                $VALIDATION_WARNINGS.append("deferral in {parsed.file_path}: missing {field}")
                Mark gap as INVALID

        # Backward compatibility: missing "blocking" field defaults to true
        IF "blocking" not in gap:
            gap.blocking = true

IF len($VALIDATION_WARNINGS) > 0:
    Display: "Validation warnings (${len($VALIDATION_WARNINGS)}):"
    FOR warning in $VALIDATION_WARNINGS:
        Display: "  - {warning}"
    Display: "Invalid entries will be skipped during normalization"

Display: "Gap structure validation complete"
```

**VERIFY:** All valid gap entries have required fields populated. Missing "blocking" fields defaulted to `true`. Invalid entries flagged (not fatal -- they are skipped in Step 2.5).

**RECORD:**
```bash
source .venv/bin/activate && devforgeai-validate phase-record ${SESSION_ID} --workflow=qa-remediation --phase=02 --step=2.4 --project-root=. 2>&1
```
Update checkpoint: `phases["02"].steps_completed.append("2.4")`

---

### Step 2.5: Build Unified Gap List

**EXECUTE:**
```
$ALL_GAPS = []
$SEQUENCE = 1

FOR each parsed in $PARSED_DATA:

    # Process coverage_gaps
    FOR i, gap in enumerate(parsed.coverage_gaps):
        IF gap is INVALID: CONTINUE

        # Derive severity from layer
        IF gap.layer == "Business Logic": severity = "CRITICAL"
        ELIF gap.layer == "Application": severity = "HIGH"
        ELIF gap.layer == "Infrastructure": severity = "MEDIUM"
        ELSE: severity = "MEDIUM"

        $ALL_GAPS.append({
            id: "GAP-{$SEQUENCE}",
            source_file: parsed.file_path,
            source_story: parsed.story_id,
            source_array: "coverage_gaps",
            source_index: i,
            type: "coverage_gap",
            file: gap.file,
            severity: severity,
            blocking: gap.blocking,
            description: "{gap.layer} coverage gap in {gap.file}: {gap.current_coverage}% vs {gap.target_coverage}% target",
            details: gap
        })
        $SEQUENCE += 1

    # Process anti_pattern_violations
    FOR i, gap in enumerate(parsed.anti_pattern_violations):
        IF gap is INVALID: CONTINUE

        $ALL_GAPS.append({
            id: "GAP-{$SEQUENCE}",
            source_file: parsed.file_path,
            source_story: parsed.story_id,
            source_array: "anti_pattern_violations",
            source_index: i,
            type: "anti_pattern",
            file: gap.file,
            severity: gap.severity,
            blocking: gap.blocking,
            description: "{gap.type} violation in {gap.file}: {gap.description OR gap.type}",
            details: gap
        })
        $SEQUENCE += 1

    # Process code_quality_violations
    FOR i, gap in enumerate(parsed.code_quality_violations):
        IF gap is INVALID: CONTINUE

        $ALL_GAPS.append({
            id: "GAP-{$SEQUENCE}",
            source_file: parsed.file_path,
            source_story: parsed.story_id,
            source_array: "code_quality_violations",
            source_index: i,
            type: "code_quality",
            file: gap.file,
            severity: gap.severity,
            blocking: gap.blocking,
            description: "{gap.metric} issue in {gap.file}: {gap.current_value} vs {gap.threshold} threshold",
            details: gap
        })
        $SEQUENCE += 1

    # Process deferral_issues
    FOR i, gap in enumerate(parsed.deferral_issues):
        IF gap is INVALID: CONTINUE

        $ALL_GAPS.append({
            id: "GAP-{$SEQUENCE}",
            source_file: parsed.file_path,
            source_story: parsed.story_id,
            source_array: "deferral_issues",
            source_index: i,
            type: "deferral",
            file: gap.item,
            severity: gap.severity,
            blocking: gap.blocking,
            description: "Deferred DoD: {gap.item} ({gap.violation_type OR 'unspecified'})",
            details: gap
        })
        $SEQUENCE += 1

$TOTAL_GAPS = len($ALL_GAPS)

Display: "Unified gap list built:"
Display: "  Total gaps: ${TOTAL_GAPS}"
Display: "  Coverage gaps: {count where type == 'coverage_gap'}"
Display: "  Anti-pattern violations: {count where type == 'anti_pattern'}"
Display: "  Code quality violations: {count where type == 'code_quality'}"
Display: "  Deferral issues: {count where type == 'deferral'}"

IF $TOTAL_GAPS == 0:
    HALT: "No valid gaps found after normalization. All entries may have been invalid."
```

**VERIFY:** `$ALL_GAPS` array has at least 1 entry. Each entry has all required fields: `id`, `source_file`, `source_story`, `source_array`, `source_index`, `type`, `file`, `severity`, `blocking`, `description`, `details`. `$TOTAL_GAPS > 0`.

**RECORD:**
```bash
source .venv/bin/activate && devforgeai-validate phase-record ${SESSION_ID} --workflow=qa-remediation --phase=02 --step=2.5 --project-root=. 2>&1
```
Update checkpoint: `phases["02"].steps_completed.append("2.5")`

---

## Phase Exit Verification

```
Verify all exit criteria:
1. $GAP_FILES array populated (len >= 1)               -> CHECK
2. $ALL_GAPS array populated (len >= 1)                 -> CHECK
3. $FILES_PROCESSED count > 0                           -> CHECK
4. $TOTAL_GAPS count > 0                                -> CHECK

Update checkpoint with phase 02 output:
  output.gap_files_processed = $FILES_PROCESSED
  output.total_gaps = $TOTAL_GAPS
  progress.current_phase = 2
  progress.phases_completed.append("02")
  phases["02"].status = "completed"

IF any check fails: HALT -- "Phase 02 exit verification failed on: {failed_criteria}"

Display:
"Phase 02 Complete: Discovery & Parsing"
"  Files Processed: ${FILES_PROCESSED} of ${len($GAP_FILES)}"
"  Total Gaps Extracted: ${TOTAL_GAPS}"
"  Parse Errors: ${len($PARSE_ERRORS)}"
"  Validation Warnings: ${len($VALIDATION_WARNINGS)}"
"  Proceeding to Phase 03: Aggregation & Prioritization..."
```

## Exit Gate

```bash
source .venv/bin/activate && devforgeai-validate phase-complete ${SESSION_ID} --workflow=qa-remediation --phase=02 --checkpoint-passed --project-root=. 2>&1
# Exit 0: proceed to Phase 03 | Exit 1: HALT
```
