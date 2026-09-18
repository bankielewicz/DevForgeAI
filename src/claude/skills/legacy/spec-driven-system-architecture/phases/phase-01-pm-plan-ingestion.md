# Phase 01: PM Plan Ingestion & Validation

## Entry Gate

```bash
devforgeai-validate phase-check ${SYSARCH_ID} --workflow=system-architecture --from=00 --to=01 --project-root=. 2>&1
```

| Exit Code | Action |
|-----------|--------|
| 0 | Proceed to Phase 01 |
| 127 | CLI not installed — proceed without enforcement |
| Other | HALT — previous phase not complete |

---

## Contract

| Attribute | Value |
|-----------|-------|
| **PURPOSE** | Locate the persisted PM plan on disk, read it, and validate its structure against `ideation-output.schema.json` v1.0 BEFORE any architecture work. This is the structural fix for **Gap B** (PM→Architecture handoff non-enforcement) from ARCH-GAPS-001. |
| **REFERENCE** | `.claude/skills/spec-driven-system-architecture/references/ideation-output.schema.json` |
| **STEP COUNT** | 5 mandatory steps |

## Phase Exit Criteria

Before this phase can complete, ALL of the following MUST be true:

- [ ] `pm_plan_path` recorded and the file confirmed present on disk via `Glob()`
- [ ] PM plan content read from disk (NOT from conversation memory)
- [ ] YAML frontmatter extracted and non-empty
- [ ] All 12 required top-level keys present; `schema_version == "1.0"`
- [ ] `pm_plan_validation` recorded with a `validation_status` of `passed` or `passed_with_warnings`

**IF any criterion is unmet: HALT. Do NOT proceed to Phase 02.**

---

## Reference Loading

```
Read(file_path=".claude/skills/spec-driven-system-architecture/references/ideation-output.schema.json")
```

IF the Read fails: HALT — "Phase 01 input contract not loaded. Cannot validate the PM plan."

Do NOT rely on memory of previous reads. Load fresh every time this phase executes.

---

## Mandatory Steps

### Step 1.1: Locate the PM Plan on Disk

**EXECUTE:**
```
IF $PM_PLAN_PATH was provided as an argument:
  candidate = $PM_PLAN_PATH
ELSE:
  Glob(pattern="devforgeai/specs/requirements/*-requirements.md")
  IF exactly 1 match: candidate = that match
  IF 0 matches: HALT — "No PM plan found. Run /ideate first."
  IF >1 match:
    AskUserQuestion — present the candidate files, ask the user which PM plan
    this System Architecture consumes. candidate = user selection.
```

**VERIFY:**
- `candidate` is a non-empty relative path
- `Glob(pattern=candidate)` returns exactly 1 file

**RECORD:**
```bash
devforgeai-validate phase-record ${SYSARCH_ID} --workflow=system-architecture --phase=01 --step=1.1 --project-root=. 2>&1
```
```json
{ "phase": "01", "step": "1.1", "pm_plan_path": "<candidate>" }
```

---

### Step 1.2: Read the PM Plan From Disk

**EXECUTE:**
```
Read(file_path=<pm_plan_path>)
```

This is the **Gap B** enforcement point: the PM plan MUST be read from the
persisted file. Do NOT reconstruct, summarize, or assume PM-plan content from the
conversation context — even if `/ideate` ran in the same session.

**VERIFY:**
- Read returned content with length > 0
- The content begins with a YAML frontmatter delimiter (`---`)
- IF no frontmatter delimiter: HALT — "PM plan has no YAML frontmatter; cannot validate against the input contract."

**RECORD:**
```bash
devforgeai-validate phase-record ${SYSARCH_ID} --workflow=system-architecture --phase=01 --step=1.2 --project-root=. 2>&1
```
```json
{ "step": "1.2", "pm_plan_read": true, "content_length": "<int>" }
```

---

### Step 1.3: Extract the YAML Frontmatter

**EXECUTE:**
```
Extract the YAML block between the first two `---` delimiters of the PM plan.
This block is the structured ideation-output payload (per the
ideation-output.schema.json description: "The structured data lives in the YAML
frontmatter of devforgeai/specs/requirements/{project}-requirements.md").
Parse it into a structured object: pm_plan.
```

**VERIFY:**
- The frontmatter block is non-empty
- It parses as valid YAML (a top-level mapping, not a scalar or list)
- IF parse fails: HALT — "PM plan frontmatter is not valid YAML."

**RECORD:**
```bash
devforgeai-validate phase-record ${SYSARCH_ID} --workflow=system-architecture --phase=01 --step=1.3 --project-root=. 2>&1
```
```json
{ "step": "1.3", "frontmatter_extracted": true, "top_level_keys": ["<keys found>"] }
```

---

### Step 1.4: Structural Validation Against the Input Contract

**EXECUTE:**

The 4-step structural check is enforced by the deterministic CLI gate
`devforgeai-validate validate-pm-plan` (ADR-084). The CLI performs the
same 4 checks the prose used to enumerate inline — but as a binary gate
the orchestrator cannot abbreviate or skip:

1. **Required top-level keys (12).** Confirm ALL are present:
   `schema_version`, `project`, `created`, `scope_baseline`, `milestone_roadmap`,
   `risk_register`, `stakeholder_register`, `prioritized_requirements`,
   `assumptions`, `constraints`, `success_criteria`, `idea_backlog_ref`.
2. **Version pin.** Confirm `schema_version == "1.0"`.
3. **ID-pattern conformance** (sample-check each populated array):
   - `prioritized_requirements[].id` matches `^FR-[0-9]{3,}$`
   - `risk_register[].id` matches `^RISK-[0-9]{3,}$`
   - `assumptions[].id` matches `^ASMP-[0-9]{3,}$`
   - `success_criteria[].id` matches `^SC-[0-9]+$`
4. **Non-empty arrays.** `prioritized_requirements` and `success_criteria` each
   have ≥ 1 entry (an architecture cannot be grounded without them).

Checks 1 & 2 are blocking (`severity=fail`); checks 3 & 4 are
warning-capable (`severity=warning`). This is the same
Schema-Validation-Before-Consumption pattern that ADR-082 / H5
established at the DEVARCH → Stories handoff.

```
Bash:
  devforgeai-validate validate-pm-plan "$pm_plan_path" \
      --project-root=. --format=json
IF exit code != 0:
  Display the CLI's JSON `checks[]` array (each failing row carries
  `name`, `severity`, and `diagnostic`) so the user sees which checks
  failed.
  HALT — "PM Plan failed input-contract validation; cannot proceed."
```

Classify the outcome (the CLI emits `validation_status` directly — the
orchestrator does NOT re-classify):
- **passed** — all 4 checks pass
- **passed_with_warnings** — checks 1 & 2 pass; check 3 or 4 has a minor,
  non-blocking gap (recorded in the CLI's `warnings[]` field)
- **failed** — any required key missing OR `schema_version != "1.0"`
  (CLI exit code 1)

**VERIFY:**
- The CLI ran to completion and emitted a JSON payload
- A `validation_status` value is present in the CLI output

**RECORD:**

The CLI's `--format=json` output pre-rolls every field this RECORD
captures — extract them directly from the JSON output rather than
re-classifying:

```bash
devforgeai-validate phase-record ${SYSARCH_ID} --workflow=system-architecture --phase=01 --step=1.4 --project-root=. 2>&1
```
```json
{
  "step": "1.4",
  "missing_keys": ["<from CLI JSON missing_keys[]>"],
  "schema_version_found": "<from CLI JSON schema_version_found>",
  "id_pattern_violations": ["<from CLI JSON id_pattern_violations[]>"],
  "warnings": ["<from CLI JSON warnings[]>"]
}
```

---

### Step 1.5: Record the Validation Verdict

**EXECUTE:**
```
IF validation_status == "failed":
  Display the failure detail (missing keys / wrong version).
  HALT — "PM plan failed input-contract validation. Gap B guard tripped:
  the System Architecture cannot be built on a non-conforming PM plan.
  Re-run /ideate or correct the requirements file, then retry."

IF validation_status == "passed_with_warnings":
  Display the warnings and continue.

Build the pm_plan_validation object that Phase 07 embeds into the output:
pm_plan_validation = {
  "schema_id": "ideation-output-1.0",
  "validation_status": "<passed|passed_with_warnings>",
  "warnings": [<warning strings>]
}

Also capture provenance fields for downstream phases:
  source_pm_plan   = <pm_plan_path>
  source_brainstorm = pm_plan.source_brainstorm  (may be null)
  project_name     = pm_plan.project
```

**VERIFY:**
- `validation_status` is `passed` or `passed_with_warnings` (a `failed` status
  would have HALTed above)
- `source_pm_plan` is a non-empty path

**RECORD:**
```bash
devforgeai-validate phase-record ${SYSARCH_ID} --workflow=system-architecture --phase=01 --step=1.5 --project-root=. 2>&1
```
```json
checkpoint.phases["01"] = {
  "status": "completed",
  "pm_plan_path": "<source_pm_plan>",
  "pm_plan_validation": { "schema_id": "ideation-output-1.0",
                          "validation_status": "<status>", "warnings": [...] },
  "source_brainstorm": "<value|null>",
  "project_name": "<pm_plan.project>",
  "pm_plan": { "<the parsed PM-plan object, retained for Phases 02-07>" }
}
```

---

## Exit Gate

```bash
devforgeai-validate phase-complete ${SYSARCH_ID} --workflow=system-architecture --phase=01 --checkpoint-passed --project-root=. 2>&1
```

| Exit Code | Action |
|-----------|--------|
| 0 | Phase 01 complete — proceed to Phase 02 |
| 127 | CLI not installed — proceed without enforcement |
| Other | HALT — checkpoint/step validation failed |

---

## Phase Transition Display

```
Display:
  "Phase 01 Complete: PM Plan Ingestion & Validation"
  "PM plan: {pm_plan_path}  |  Validation: {validation_status}"
  "Requirements: {count}  Risks: {count}  Stakeholders: {count}"
  "Proceeding to Phase 02: Context Discovery"
```
