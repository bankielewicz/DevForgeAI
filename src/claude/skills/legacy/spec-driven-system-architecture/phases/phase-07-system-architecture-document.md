# Phase 07: System Architecture Document

## Entry Gate

```bash
devforgeai-validate phase-check ${SYSARCH_ID} --workflow=system-architecture --from=06 --to=07 --project-root=. 2>&1
```

| Exit Code | Action |
|-----------|--------|
| 0 | Proceed to Phase 07 |
| 127 | CLI not installed — proceed without enforcement |
| Other | HALT — previous phase not complete |

---

## Contract

| Attribute | Value |
|-----------|-------|
| **PURPOSE** | Synthesize every prior phase into the System Architecture Document — a self-contained HTML file carrying a schema-valid JSON data island — and produce the explicit handoff payload for `/create-solution-architecture`. |
| **REFERENCES** | `.claude/skills/spec-driven-system-architecture/references/system-architecture-output.schema.json`; `.claude/skills/spec-driven-system-architecture/assets/templates/system-architecture-template.html` |
| **STEP COUNT** | 5 mandatory steps |

## Phase Exit Criteria

Before this phase can complete, ALL of the following MUST be true:

- [ ] The output object assembled with all 12 required schema fields populated
- [ ] `handoff.recommended_approach` is non-empty
- [ ] The output object passes structural validation against `system-architecture-output.schema.json` v1.0
- [ ] The HTML document is on disk with an embedded, schema-valid JSON data island
- [ ] Next steps displayed to the user

**IF any criterion is unmet: HALT. The workflow is NOT complete.**

---

## Reference Loading

```
Read(file_path=".claude/skills/spec-driven-system-architecture/references/system-architecture-output.schema.json")
Read(file_path=".claude/skills/spec-driven-system-architecture/assets/templates/system-architecture-template.html")
```

IF either Read fails: HALT — "Phase 07 reference files not loaded."

Do NOT rely on memory of previous reads. Load fresh every time this phase executes.

---

## Mandatory Steps

### Step 7.1: Assemble the Output Object

**EXECUTE:**

Build the `system_architecture_output` object from the checkpoint data of Phases
01–06, matching `system-architecture-output.schema.json` v1.0:

```
system_architecture_output = {
  schema_version: "1.0",
  id: "${SYSARCH_ID}",                       # ^SYSARCH-[0-9]{3,}$
  title: "<project name> System Architecture",
  status: "Draft",
  created: "<ISO 8601 date>",
  source_pm_plan: "<Phase 01 pm_plan_path>",
  pm_plan_validation: { schema_id: "ideation-output-1.0",
                        validation_status: "...", warnings: [...] },
  source_brainstorm: <Phase 01 value | null>,
  system_boundary:        <Phase 05>,
  integration_topology:   <Phase 05>,
  tech_stack_rationale:   <Phase 05>,
  system_nfrs:            <Phase 05>,
  deployment_architecture:<Phase 05>,
  adr_refs:               <Phase 04>,
  context_files_generated:<Phase 03 — the 12 relative paths>,
  handoff: { ... }                            # built in Step 7.2
}
```

**VERIFY:**
- All 12 schema-required fields are present and non-null:
  `schema_version`, `id`, `title`, `status`, `created`, `source_pm_plan`,
  `pm_plan_validation`, `system_boundary`, `integration_topology`,
  `tech_stack_rationale`, `system_nfrs`, `context_files_generated`, `handoff`
- `context_files_generated` lists all 12 constitution artifacts

**RECORD:**
```bash
devforgeai-validate phase-record ${SYSARCH_ID} --workflow=system-architecture --phase=07 --step=7.1 --project-root=. 2>&1
```
```json
{ "phase": "07", "step": "7.1", "output_object_assembled": true }
```

---

### Step 7.2: Build the Handoff Payload

**EXECUTE:**

The handoff is what `/create-solution-architecture` consumes:

```
handoff = {
  recommended_approach: "<the strategic system-design direction the solution
                          architect must work within — non-empty>",
  critical_constraints: [ "<system-level constraint the solution architecture
                            must not violate>", ... ],
  open_questions: [ "<unresolved question, incl. Phase 06 deferrals and any
                      coarse deployment unknowns>", ... ]
}
```

`critical_constraints` draws from `architecture-constraints.md`, the system NFRs,
and any PM-plan constraint resolved by override. `open_questions` includes every
Phase 06 `deferred_to_solution_architecture` item.

**VERIFY:**
- `handoff.recommended_approach` is a non-empty string
- `critical_constraints` and `open_questions` are arrays (may be empty, never null)

**RECORD:**
```bash
devforgeai-validate phase-record ${SYSARCH_ID} --workflow=system-architecture --phase=07 --step=7.2 --project-root=. 2>&1
```
```json
{ "step": "7.2", "handoff": { "recommended_approach": "...",
  "critical_constraints": [ ... ], "open_questions": [ ... ] } }
```

---

### Step 7.3: Validate Against the Output Contract

**EXECUTE:**

Structurally validate `system_architecture_output` against
`system-architecture-output.schema.json` v1.0:

1. All 12 required top-level keys present
2. `schema_version == "1.0"`; `id` matches `^SYSARCH-[0-9]{3,}$`;
   `status` is one of `Draft`/`Reviewed`/`Accepted`/`Superseded`
3. Each `integration_topology[].id` matches `^INT-[0-9]{3,}$`;
   each `system_nfrs[].id` matches `^SNFR-[0-9]{3,}$`;
   each `adr_refs[]` matches `^ADR-[0-9]{3,}$`
4. `system_nfrs[].category` is one of the 7 enum values
5. `pm_plan_validation.validation_status` is `passed` / `passed_with_warnings` / `failed`
6. `handoff` has a non-empty `recommended_approach`

**VERIFY:**
- All 6 checks pass
- IF any check fails: HALT — "Output object fails the system-architecture-output
  contract. Fix the offending field before rendering the document."

**RECORD:**
```bash
devforgeai-validate phase-record ${SYSARCH_ID} --workflow=system-architecture --phase=07 --step=7.3 --project-root=. 2>&1
```
```json
{ "step": "7.3", "schema_validation": "passed" }
```

---

### Step 7.4: Render and Write the HTML Document

**EXECUTE:**

Render the loaded template (`system-architecture-template.html`):

1. Substitute every `{{TOKEN}}` placeholder with rendered content from the output
   object (title, id, status, created, boundary, topology table, tech-stack
   table, NFR table, deployment block, ADR list, handoff).
2. Replace each `data-section` body with the rendered section content.
3. Serialize the **entire** `system_architecture_output` object as compact JSON
   into the data island:
   `<script type="application/json" id="system-architecture-data"> … </script>`
4. The file MUST be self-contained — inline CSS, no external assets. The JSON
   island is the machine-readable contract; the HTML is the human-facing carrier.

```
short_name = kebab-case of the project name
output_path = "devforgeai/specs/architecture/${SYSARCH_ID}-${short_name}.system-architecture.html"
Write(file_path=output_path, content=<rendered HTML>)
```

**VERIFY:**
- `Glob(pattern=output_path)` returns exactly 1 file
- The file contains the `id="system-architecture-data"` script tag
- No unrendered `{{TOKEN}}` placeholder remains in the file
- The embedded JSON parses and equals the validated output object from Step 7.3

**RECORD:**
```bash
devforgeai-validate phase-record ${SYSARCH_ID} --workflow=system-architecture --phase=07 --step=7.4 --project-root=. 2>&1
```
```json
{ "step": "7.4", "output_file": "<output_path>", "document_written": true }
```

---

### Step 7.5: Display Completion and Handoff

**EXECUTE:**
```
Display:
"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  SYSTEM ARCHITECTURE COMPLETE — ${SYSARCH_ID}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Document: {output_path}
Constitution: 6 context files + 5 .ai.md + test-plan.ai.yaml
ADRs created: {adr_refs}
Integrations: {n}  |  System NFRs: {n}  |  Tech decisions: {n}

Next step:
  /create-solution-architecture — per-epic technical design,
  consuming this document's JSON data island.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
```

Then `AskUserQuestion` — confirm the document is accurate, or open it for review
before proceeding.

**VERIFY:**
- Completion banner displayed with no `{placeholder}` text remaining
- User responded to the confirmation question

**RECORD:**
```bash
devforgeai-validate phase-record ${SYSARCH_ID} --workflow=system-architecture --phase=07 --step=7.5 --project-root=. 2>&1
```
```json
checkpoint.phases["07"] = {
  "status": "completed",
  "output_file": "<output_path>",
  "handoff": { ... },
  "user_confirmed": true
}
```

---

## Exit Gate

```bash
devforgeai-validate phase-complete ${SYSARCH_ID} --workflow=system-architecture --phase=07 --checkpoint-passed --project-root=. 2>&1
```

| Exit Code | Action |
|-----------|--------|
| 0 | Phase 07 complete — proceed to next phase |
| 127 | CLI not installed — proceed without enforcement |
| Other | HALT — checkpoint/step validation failed |

---

## Phase Transition Display

```
Display:
  "Phase 07 Complete: System Architecture Document"
  "Workflow complete — 7/7 phases. Document on disk at {output_path}."
```
