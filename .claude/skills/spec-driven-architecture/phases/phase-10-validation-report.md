# Phase 10: Validation Report

## Contract

| Attribute | Value |
|-----------|-------|
| **PURPOSE** | Post-creation completeness validation. Verify all required artifacts exist, contain real content (no placeholders), and are ready for development |
| **REFERENCES** | `.claude/skills/spec-driven-architecture/references/post-creation-validation.md` |
| **STEP COUNT** | 4 mandatory steps |

## Phase Exit Criteria

Before this phase can complete, ALL of the following MUST be true:
- [ ] All 6 core context files verified present and non-empty (> 100 characters each)
- [ ] Zero placeholder patterns remain unresolved (or user accepted as-is)
- [ ] At least 1 ADR exists with required sections
- [ ] Success report displayed to user

**IF any criterion is unmet: HALT. Do NOT proceed to Phase 11.**

---

## Reference Loading [MANDATORY]

```
Read(file_path=".claude/skills/spec-driven-architecture/references/post-creation-validation.md")
```

Do NOT rely on memory of previous reads. Load fresh every time this phase executes.

---

## Mandatory Steps

### Step 10.1: Verify File Completeness

**EXECUTE:**
```
Glob(pattern="devforgeai/specs/context/*.md")
```
Count the matching files. At minimum, these 6 MUST exist:
- `tech-stack.md`
- `source-tree.md`
- `dependencies.md`
- `coding-standards.md`
- `architecture-constraints.md`
- `anti-patterns.md`

For each file found, read and measure content:
```
Read(file_path="devforgeai/specs/context/tech-stack.md")
Read(file_path="devforgeai/specs/context/source-tree.md")
Read(file_path="devforgeai/specs/context/dependencies.md")
Read(file_path="devforgeai/specs/context/coding-standards.md")
Read(file_path="devforgeai/specs/context/architecture-constraints.md")
Read(file_path="devforgeai/specs/context/anti-patterns.md")
```
All 6 reads may be issued in parallel.

For each file, calculate character count. Flag any file with fewer than 100 characters as FAILED (empty/stub).

**VERIFY:**
- Glob returned at least 6 files
- All 6 required files are present in the results
- Every required file has character count > 100
- If any file is missing or undersized: HALT with specific failure message

**RECORD:**
```json
checkpoint.phase_10.step_10_1 = {
  "file_count": "<total context files found>",
  "required_files_present": true,
  "file_details": {
    "tech-stack.md": { "exists": true, "char_count": "<N>", "pass": true },
    "source-tree.md": { "exists": true, "char_count": "<N>", "pass": true },
    "dependencies.md": { "exists": true, "char_count": "<N>", "pass": true },
    "coding-standards.md": { "exists": true, "char_count": "<N>", "pass": true },
    "architecture-constraints.md": { "exists": true, "char_count": "<N>", "pass": true },
    "anti-patterns.md": { "exists": true, "char_count": "<N>", "pass": true }
  },
  "all_passed": true
}
```

---

### Step 10.2: Check for Placeholder Content

**EXECUTE:**
```
Grep(pattern="(TODO|TBD|\\[FILL IN\\]|\\[PLACEHOLDER\\]|XXX|FIXME)", path="devforgeai/specs/context/", output_mode="content", -n=true)
```

If matches found, display each occurrence with file path and line number.

For each placeholder found:
```
AskUserQuestion:
  Question: "Placeholder found in {file_path} at line {line_number}:\n`{matched_line}`\nResolve now or accept as-is?"
  Header: "Placeholder Resolution"
  Options:
    - label: "Resolve now"
      description: "Provide replacement text for this placeholder"
    - label: "Accept as-is"
      description: "Keep placeholder — will need resolution before development"
  multiSelect: false
```

If user chooses "Resolve now": Gather replacement text and apply:
```
Edit(file_path=<path>, old_string=<placeholder_line>, new_string=<resolved_line>)
```

**VERIFY:**
- Grep executed without error across all context files
- Every placeholder either resolved (Edit applied) or explicitly accepted by user
- No silent skipping of found placeholders

**RECORD:**
```json
checkpoint.phase_10.step_10_2 = {
  "placeholder_count": "<total found>",
  "resolved": "<count fixed via Edit>",
  "accepted_as_is": "<count user accepted>",
  "resolutions": [
    { "file": "<path>", "line": "<N>", "action": "<resolved|accepted>", "original": "<text>" }
  ],
  "all_addressed": true
}
```

---

### Step 10.3: Verify ADR Creation

**EXECUTE:**
```
Glob(pattern="devforgeai/specs/adrs/ADR-*.md")
```
Count matching files. At least 1 ADR must exist (created during earlier architecture phases).

Read the first ADR found to verify structural completeness:
```
Read(file_path="devforgeai/specs/adrs/<first_match>")
```

Verify the ADR contains all required sections by checking for these headings:
```
Grep(pattern="^## (Context|Decision|Rationale|Consequences|Alternatives|Enforcement)", path="devforgeai/specs/adrs/<first_match>", output_mode="content")
```

Required sections: Context, Decision, Rationale, Consequences, Alternatives, Enforcement.

**VERIFY:**
- At least 1 ADR file found by Glob
- First ADR contains all 6 required section headings
- If any section missing: log as warning (non-blocking) with specific missing section names

**RECORD:**
```json
checkpoint.phase_10.step_10_3 = {
  "adr_count": "<total ADR files found>",
  "adr_files": ["<list of ADR paths>"],
  "first_adr_validated": true,
  "sections_found": ["Context", "Decision", "Rationale", "Consequences", "Alternatives", "Enforcement"],
  "sections_missing": [],
  "validation_passed": true
}
```

---

### Step 10.4: Display Success Report

**EXECUTE:**
Generate and display a formatted validation report:

```
============================================================
  ARCHITECTURE VALIDATION REPORT
============================================================

  Context Files
  ─────────────
  [PASS] tech-stack.md              ({N} chars)
  [PASS] source-tree.md             ({N} chars)
  [PASS] dependencies.md            ({N} chars)
  [PASS] coding-standards.md        ({N} chars)
  [PASS] architecture-constraints.md ({N} chars)
  [PASS] anti-patterns.md           ({N} chars)

  ADRs Created
  ────────────
  {adr_count} ADR(s): {list of ADR filenames}

  Design System
  ─────────────
  Status: [Created / Skipped (no UI framework)]

  Placeholder Status
  ──────────────────
  Found: {N} | Resolved: {N} | Accepted: {N}

  ════════════════════════════════════════════════════════════
  RESULT: READY FOR DEVELOPMENT
  ════════════════════════════════════════════════════════════

  Next Steps:
    /create-epic   → Create epics from requirements
    /create-sprint → Plan sprint with story selection
    /dev           → Begin story development (TDD)
============================================================
```

**VERIFY:**
- Report displayed with all sections populated (no empty placeholders in output)
- File counts match Step 10.1 data
- ADR counts match Step 10.3 data
- Placeholder counts match Step 10.2 data

**RECORD:**
```json
checkpoint.phase_10.step_10_4 = {
  "report_displayed": true,
  "result": "READY_FOR_DEVELOPMENT",
  "files_created": "<count>",
  "adrs_created": "<count>",
  "design_system": "<created|skipped>",
  "placeholders_clean": "<true|false>"
}
checkpoint.phase_10.status = "completed"
```

---

## Phase Transition Display

```
============================================================
  PHASE 10 COMPLETE: Validation Report
============================================================
  Context files validated:   {N}/6
  ADRs validated:            {N}
  Placeholders resolved:     {resolved}/{total}
  Overall result:            READY FOR DEVELOPMENT
------------------------------------------------------------
  Architecture workflow complete.
  Use /create-epic to begin epic creation (Phase 11).
============================================================
```
