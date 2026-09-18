# Phase 02: Context Discovery

## Entry Gate

```bash
devforgeai-validate phase-check ${SYSARCH_ID} --workflow=system-architecture --from=01 --to=02 --project-root=. 2>&1
```

| Exit Code | Action |
|-----------|--------|
| 0 | Proceed to Phase 02 |
| 127 | CLI not installed — proceed without enforcement |
| Other | HALT — previous phase not complete |

---

## Contract

| Attribute | Value |
|-----------|-------|
| **PURPOSE** | Detect greenfield / brownfield project mode, inventory any existing technology, select the architecture style, and reconcile the discovered reality against the PM-plan constraints. Establishes the inputs the constitutional context files (Phase 03) are built from. |
| **REFERENCE** | `.claude/skills/spec-driven-system-architecture/references/system-architecture-output.schema.json` |
| **SUBAGENT** | `tech-stack-detector` (brownfield / partial projects only) |
| **STEP COUNT** | 4 mandatory steps |

## Phase Exit Criteria

Before this phase can complete, ALL of the following MUST be true:

- [ ] `project_mode` recorded as one of: `greenfield`, `brownfield`, `partial`
- [ ] `tech_inventory` recorded (or explicitly skipped with a recorded reason for greenfield)
- [ ] `architecture_style` recorded from a user selection
- [ ] PM-plan `constraints` reconciled against discovery; any conflict resolved via AskUserQuestion

**IF any criterion is unmet: HALT. Do NOT proceed to Phase 03.**

---

## Reference Loading

```
Read(file_path=".claude/skills/spec-driven-system-architecture/references/system-architecture-output.schema.json")
```

IF the Read fails: HALT — "Phase 02 output contract not loaded."

Do NOT rely on memory of previous reads. Load fresh every time this phase executes.

---

## Mandatory Steps

### Step 2.1: Detect Project Mode

**EXECUTE:**
```
Glob(pattern="devforgeai/specs/context/*.md")
```
Count the matching context files. Classification:
- 6 files found = `brownfield`
- 0 files found = `greenfield`
- 1-5 files found = `partial`

**VERIFY:**
- `Glob()` returned a result (even an empty array)
- `project_mode` is one of the three valid values
- IF `partial`: list which context files exist and which are missing

**RECORD:**
```bash
devforgeai-validate phase-record ${SYSARCH_ID} --workflow=system-architecture --phase=02 --step=2.1 --project-root=. 2>&1
```
```json
{
  "phase": "02", "step": "2.1",
  "project_mode": "<greenfield|brownfield|partial>",
  "existing_context_files": ["<found>"],
  "missing_context_files": ["<missing>"]
}
```

---

### Step 2.2: Technology Inventory (Brownfield / Partial)

**CONDITIONAL:** Execute only if `project_mode` is `brownfield` or `partial`. If
`greenfield`, skip with an explicit skip record.

**EXECUTE:**
```
Task(
  subagent_type="tech-stack-detector",
  prompt="Detect the technology stack of this project. Inventory languages,
    frameworks, test frameworks, build tools, and package managers from the
    codebase. IF devforgeai/specs/context/tech-stack.md exists, validate the
    detected stack against it and report any drift. Return structured JSON:
    { languages: [], frameworks: [], test_frameworks: [], build_tools: [],
      package_managers: [], tech_stack_md_present: bool, drift: [] }"
)
```
This is a BLOCKING task. Wait for the result before proceeding.

For `greenfield`, the technology stack is decided fresh in Phase 03 from the PM
plan — record the explicit skip instead.

**VERIFY:**
- Brownfield / partial: Task returned a `tech_inventory` object with a non-empty
  `languages` array
- Greenfield: the skip was explicitly recorded (not silently omitted)

**RECORD:**
```bash
devforgeai-validate phase-record ${SYSARCH_ID} --workflow=system-architecture --phase=02 --step=2.2 --project-root=. 2>&1
```
```json
{
  "step": "2.2",
  "executed": "<true|false>",
  "skip_reason": "<greenfield_project|null>",
  "tech_inventory": { "languages": [], "frameworks": [], "test_frameworks": [],
                      "build_tools": [], "package_managers": [], "drift": [] }
}
```

---

### Step 2.3: Select the Architecture Style

**EXECUTE:**
```
AskUserQuestion:
  Question: "What architecture style best fits this system?"
  Header: "Architecture Style"
  multiSelect: false
  Options:
    - label: "Monolithic"
      description: "Single deployable unit. Best for MVPs, small teams, simple domains."
    - label: "Modular Monolith"
      description: "One deployable with enforced module boundaries. Best for growing projects."
    - label: "Microservices"
      description: "Independent services per domain. Best for large teams, complex domains."
    - label: "Serverless / Event-Driven"
      description: "Function-as-a-Service. Best for event-driven, variable-load workloads."
```

Before asking, review the PM-plan `milestone_roadmap`, `scope_baseline`, and
`constraints` and state a one-line recommendation so the choice is informed.

**VERIFY:**
- User response is non-empty
- Response is one of the four options, OR a recorded verbatim custom answer

**RECORD:**
```bash
devforgeai-validate phase-record ${SYSARCH_ID} --workflow=system-architecture --phase=02 --step=2.3 --project-root=. 2>&1
```
```json
{ "step": "2.3", "architecture_style": "<selection>", "user_response_raw": "<verbatim>" }
```

---

### Step 2.4: Reconcile PM-Plan Constraints With Discovery

**EXECUTE:**
```
FOR each entry in pm_plan.constraints (from the Phase 01 checkpoint):
  Classify it: technical | business | regulatory | resource.
  IF a technical constraint conflicts with the discovered tech_inventory
     OR with the selected architecture_style:
    AskUserQuestion — present the conflict, ask the user to resolve it
    (adjust the style, override the constraint with an ADR note, or
    HALT and revise the PM plan).
Collect the reconciled constraint set as discovery.reconciled_constraints[].
```

**VERIFY:**
- Every PM-plan constraint was classified
- Every detected conflict has a recorded user resolution
- No unresolved conflict remains (Critical Rule 6 — conflicting requirements HALT)

**RECORD:**
```bash
devforgeai-validate phase-record ${SYSARCH_ID} --workflow=system-architecture --phase=02 --step=2.4 --project-root=. 2>&1
```
```json
checkpoint.phases["02"] = {
  "status": "completed",
  "project_mode": "<mode>",
  "tech_inventory": { ... },
  "architecture_style": "<style>",
  "reconciled_constraints": [ { "type": "...", "constraint": "...",
                                "resolution": "..." } ]
}
```

---

## Exit Gate

```bash
devforgeai-validate phase-complete ${SYSARCH_ID} --workflow=system-architecture --phase=02 --checkpoint-passed --project-root=. 2>&1
```

| Exit Code | Action |
|-----------|--------|
| 0 | Phase 02 complete — proceed to next phase |
| 127 | CLI not installed — proceed without enforcement |
| Other | HALT — checkpoint/step validation failed |

---

## Phase Transition Display

```
Display:
  "Phase 02 Complete: Context Discovery"
  "Mode: {project_mode}  |  Architecture style: {architecture_style}"
  "Constraints reconciled: {count}  |  Conflicts resolved: {count}"
  "Proceeding to Phase 03: Constitutional Context Files"
```

## Hook-backed OUT-Attestation

This phase has Phase-D dispatch entries in `subagent_out_attestation_registry.json`. When dispatching those named subagents, instruct them to return a `subagent-result-v1` result that includes `coverage_attestation` in the normal response. Phase completion is blocked by `subagent-out-attestation-gate.sh` when the hook-owned ledger line lacks `coverage_attestation_present:true`. This Phase-D path is OUT-attestation-only and does not require `tmp/<WORK_ID>/handoffs/`.
