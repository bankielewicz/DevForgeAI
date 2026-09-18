# Phase 06: Architecture Review

## Entry Gate

```bash
devforgeai-validate phase-check ${SYSARCH_ID} --workflow=system-architecture --from=05 --to=06 --project-root=. 2>&1
```

| Exit Code | Action |
|-----------|--------|
| 0 | Proceed to Phase 06 |
| 127 | CLI not installed — proceed without enforcement |
| Other | HALT — previous phase not complete |

---

## Contract

| Attribute | Value |
|-----------|-------|
| **PURPOSE** | Independent review of the constitution and the system design for cross-layer alignment and architectural quality before the System Architecture Document is published. **BLOCKING** — no HIGH finding may remain unresolved. |
| **REFERENCE** | `.claude/skills/spec-driven-system-architecture/references/system-architecture-output.schema.json` |
| **SUBAGENTS** | `alignment-auditor` (cross-layer alignment); `architect-reviewer` (architectural quality — BLOCKING) |
| **STEP COUNT** | 4 mandatory steps |

## Phase Exit Criteria

Before this phase can complete, ALL of the following MUST be true:

- [ ] `alignment-auditor` invoked; contradictions / gaps surfaced
- [ ] `architect-reviewer` invoked and returned structured findings
- [ ] Every HIGH finding resolved (accepted, rejected with justification, or deferred)
- [ ] All MEDIUM findings presented and user decisions recorded
- [ ] Approved changes applied and re-validated (single round, no loop)

**IF any criterion is unmet: HALT. Do NOT proceed to Phase 07.**

---

## Reference Loading

```
Read(file_path=".claude/skills/spec-driven-system-architecture/references/system-architecture-output.schema.json")
```

IF the Read fails: HALT — "Phase 06 output contract not loaded."

Do NOT rely on memory of previous reads. Load fresh every time this phase executes.

---

## Mandatory Steps

### Step 6.1: Invoke alignment-auditor

**EXECUTE:**

Build the registry-protected Phase 06 handoff for `alignment-auditor`. This is
a floor-only handoff: create an empty changed-files list so
`context_pack.coverage_matrix` is `{}` and the role-domain floor supplies the
constitutional rules.

```bash
mkdir -p tmp/${SYSARCH_ID}
: > tmp/${SYSARCH_ID}/sysarch-phase06-handoff-changed-files.txt

devforgeai-validate build-subagent-handoff ${SYSARCH_ID} \
  --workflow=spec-driven-system-architecture \
  --phase=06 \
  --subagent=alignment-auditor \
  --changed-files-file=tmp/${SYSARCH_ID}/sysarch-phase06-handoff-changed-files.txt \
  --project-root=. 2>&1
```

Bind the returned path:

```text
HANDOFF_PATH_ALIGNMENT_AUDITOR=tmp/${SYSARCH_ID}/handoffs/phase-06-alignment-auditor-handoff.md
```

VERIFY before dispatch:
- `HANDOFF_PATH_ALIGNMENT_AUDITOR` exists and is non-empty.
- `tmp/${SYSARCH_ID}/handoffs/phase-06-alignment-auditor-handoff.manifest.json` exists.
- The manifest has `context_pack.coverage_matrix == {}` and `unresolved == []`.

```
Task(
  subagent_type="alignment-auditor",
  prompt="Handoff: ${HANDOFF_PATH_ALIGNMENT_AUDITOR}
    Read the handoff first. Use its context_pack.coverage_matrix and
    role-domain rules as the constitutional context source. If a required
    domain or artifact is absent, return H-CONTEXT-MISS and stop.

    Perform a pairwise cross-layer alignment audit for the generated
    constitutional artifacts and the ADRs created this session (${adr_refs}).
    Detect contradictions and gaps. Return structured JSON with file:line
    evidence and mutability-respecting resolution proposals.
    Include a subagent-result-v1 coverage_attestation with
    context_pack_path='${HANDOFF_PATH_ALIGNMENT_AUDITOR}',
    context_pack_consumed=true, and context_miss=[]."
)
```
This is a BLOCKING task. Wait for the result before proceeding.

**VERIFY:**
- Task returned a result containing an alignment findings array (possibly empty)

**RECORD:**
```bash
devforgeai-validate phase-record ${SYSARCH_ID} --workflow=system-architecture --phase=06 --subagent=alignment-auditor --project-root=. 2>&1
devforgeai-validate phase-record ${SYSARCH_ID} --workflow=system-architecture --phase=06 --step=6.1 --project-root=. 2>&1
```
```json
{ "phase": "06", "step": "6.1", "alignment_findings": [ ... ] }
```

---

### Step 6.2: Invoke architect-reviewer (BLOCKING)

**EXECUTE:**

Build the registry-protected Phase 06 handoff for `architect-reviewer`. This is
a floor-only handoff: create an empty changed-files list so
`context_pack.coverage_matrix` is `{}` and the role-domain floor supplies the
constitutional rules.

```bash
mkdir -p tmp/${SYSARCH_ID}
: > tmp/${SYSARCH_ID}/sysarch-phase06-architect-reviewer-handoff-changed-files.txt

HANDOFF_OUTPUT_ARCHITECT_REVIEWER=$(devforgeai-validate build-subagent-handoff ${SYSARCH_ID} \
  --workflow=spec-driven-system-architecture \
  --phase=06 \
  --subagent=architect-reviewer \
  --changed-files-file=tmp/${SYSARCH_ID}/sysarch-phase06-architect-reviewer-handoff-changed-files.txt \
  --project-root=. 2>&1)
HANDOFF_PATH_ARCHITECT_REVIEWER=$(echo "$HANDOFF_OUTPUT_ARCHITECT_REVIEWER" | jq -r '.handoff_md_path')
```

VERIFY before dispatch:
- `HANDOFF_PATH_ARCHITECT_REVIEWER` exists and is non-empty.
- `tmp/${SYSARCH_ID}/handoffs/phase-06-architect-reviewer-handoff.manifest.json` exists.
- The manifest has `context_pack.coverage_matrix == {}` and `unresolved == []`.

```
Task(
  subagent_type="architect-reviewer",
  prompt="Handoff: ${HANDOFF_PATH_ARCHITECT_REVIEWER}
    Read the handoff first. Use its context_pack.coverage_matrix and
    role-domain rules as the context source. If a required domain or artifact is
    absent, return H-CONTEXT-MISS and stop.

    Review the system architecture for this project.

    Inputs:
    - The 6 context files in devforgeai/specs/context/
    - The system design from this session: system_boundary, integration_topology,
      tech_stack_rationale, system_nfrs, deployment_architecture
    - The ADRs created this session: ${adr_refs}

    Evaluate against 5 criteria:
    1. SOUNDNESS    — do the architectural choices support the PM-plan requirements and NFRs?
    2. COHERENCE    — do the technology choices and integrations work together?
    3. COMPLETENESS — are there gaps (an NFR with no design response, an integration with no protocol)?
    4. CONSISTENCY  — do the context files, ADRs, and system design contradict each other?
    5. PRACTICALITY — is the architecture realistic for the project scope and constraints?

    Return structured JSON:
    { findings: [ { criterion, severity: 'HIGH'|'MEDIUM'|'LOW', file,
                    line_range, description, recommendation, evidence } ] }
    Include a subagent-result-v1 coverage_attestation with
    context_pack_path='${HANDOFF_PATH_ARCHITECT_REVIEWER}',
    context_pack_consumed=true, and context_miss=[]."
)
```
This is a BLOCKING task. Wait for the result before proceeding.

**VERIFY:**
- Task returned a result containing a `findings` array
- Each finding has: `criterion`, `severity`, `file`, `description`, `recommendation`
- Findings sorted by severity (HIGH first)

**RECORD:**
```bash
devforgeai-validate phase-record ${SYSARCH_ID} --workflow=system-architecture --phase=06 --step=6.2 --project-root=. 2>&1
```
```json
{
  "step": "6.2",
  "review_findings_by_severity": { "HIGH": 0, "MEDIUM": 0, "LOW": 0 },
  "raw_findings": [ ... ]
}
```

---

### Step 6.3: Present Findings and Capture Decisions

**EXECUTE:**

**HIGH-severity findings (BLOCKING)** — present each individually:
```
AskUserQuestion(
  question="HIGH finding [<criterion>]: <file> — <description>\n
            Evidence: '<evidence>'\n  Recommendation: <recommendation>",
  options=[
    { label: "Accept recommendation", description: "Apply the suggested change" },
    { label: "Reject with justification", description: "Keep as-is — provide a reason" },
    { label: "Defer to solution architecture", description: "Carry as an open question to /create-solution-architecture" }
  ]
)
```

**MEDIUM-severity findings (NON-BLOCKING)** — present as one batch:
```
AskUserQuestion( "Address all" | "Select individually" | "Log all for later" )
```

**LOW-severity findings** — log without user interaction; include in the document.

Apply the same flow to any contradiction the `alignment-auditor` raised.

**VERIFY:**
- Every HIGH finding has a recorded user decision
- Every rejected HIGH has a non-empty justification
- The MEDIUM batch was presented and answered

**RECORD:**
```bash
devforgeai-validate phase-record ${SYSARCH_ID} --workflow=system-architecture --phase=06 --step=6.3 --project-root=. 2>&1
```
```json
{
  "step": "6.3",
  "high_findings": { "total": 0, "accepted": 0, "rejected": 0, "deferred": 0,
                     "rejections": [ ... ], "deferrals": [ ... ] },
  "medium_findings": { "total": 0, "addressed": 0, "logged": 0 },
  "low_findings_logged": 0
}
```

---

### Step 6.4: Apply Approved Changes and Re-Validate

**EXECUTE:**

For each accepted recommendation, apply the `Edit` to the target context file or
system-design artifact. Context-file edits require the per-invocation
`DEVFORGEAI_ALLOW_CONTEXT_EDIT=1` bypass (Phase 03 note). If an accepted change
alters a locked decision, write a superseding ADR rather than editing an existing
one.

After ALL edits, re-validate in a **single round** — do NOT loop:
- Confirm each edit applied (new content present, old content absent)
- Confirm no edit introduced a new contradiction
- A new issue found during re-validation is logged as a finding for
  `/create-solution-architecture`, NOT re-entered into the edit cycle

**VERIFY:**
- Every accepted recommendation has a corresponding applied `Edit`
- Re-validation completed (single round only)
- No HIGH finding remains in an unresolved state

**RECORD:**
```bash
devforgeai-validate phase-record ${SYSARCH_ID} --workflow=system-architecture --phase=06 --step=6.4 --project-root=. 2>&1
```
```json
checkpoint.phases["06"] = {
  "status": "completed",
  "edits_applied": 0,
  "adrs_superseding": [ ... ],
  "revalidation_passed": true,
  "deferred_to_solution_architecture": [ ... ]
}
```

---

## Exit Gate

```bash
devforgeai-validate phase-complete ${SYSARCH_ID} --workflow=system-architecture --phase=06 --checkpoint-passed --project-root=. 2>&1
```

| Exit Code | Action |
|-----------|--------|
| 0 | Phase 06 complete — proceed to next phase |
| 127 | CLI not installed — proceed without enforcement |
| Other | HALT — checkpoint/step validation failed |

---

## Phase Transition Display

```
Display:
  "Phase 06 Complete: Architecture Review"
  "Findings: {H} HIGH, {M} MEDIUM, {L} LOW  |  Accepted: {n}  Deferred: {n}"
  "Re-validation: PASS"
  "Proceeding to Phase 07: System Architecture Document"
```
