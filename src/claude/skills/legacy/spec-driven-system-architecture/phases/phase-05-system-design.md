# Phase 05: System Design

## Entry Gate

```bash
devforgeai-validate phase-check ${SYSARCH_ID} --workflow=system-architecture --from=04 --to=05 --project-root=. 2>&1
```

| Exit Code | Action |
|-----------|--------|
| 0 | Proceed to Phase 05 |
| 127 | CLI not installed — proceed without enforcement |
| Other | HALT — previous phase not complete |

---

## Contract

| Attribute | Value |
|-----------|-------|
| **PURPOSE** | Produce the macro system design: system boundary, integration topology, tech-stack rationale, system-level NFRs, and deployment architecture. These five artifacts are the substantive body of the System Architecture Document. |
| **REFERENCE** | `.claude/skills/spec-driven-system-architecture/references/system-architecture-output.schema.json` |
| **STEP COUNT** | 5 mandatory steps |

## Phase Exit Criteria

Before this phase can complete, ALL of the following MUST be true:

- [ ] `system_boundary` defined with a non-empty `summary`
- [ ] `integration_topology` enumerated (each point an `INT-NNN` with a direction)
- [ ] `tech_stack_rationale` assembled (each a `tech_decision` with rationale)
- [ ] `system_nfrs` defined (each an `SNFR-NNN` with category and statement)
- [ ] `deployment_architecture` defined

**IF any criterion is unmet: HALT. Do NOT proceed to Phase 06.**

---

## Reference Loading

```
Read(file_path=".claude/skills/spec-driven-system-architecture/references/system-architecture-output.schema.json")
```

The `$defs` (`integration_point`, `tech_decision`, `system_nfr`) and the
`properties` of this schema are the exact shapes each step below must produce.
IF the Read fails: HALT — "Phase 05 output contract not loaded."

Do NOT rely on memory of previous reads. Load fresh every time this phase executes.

---

## Mandatory Steps

### Step 5.1: Define the System Boundary

**EXECUTE:**

From the PM-plan `scope_baseline` (in/out/future) and `prioritized_requirements`,
articulate what the system **is** and **is not**:

```
system_boundary = {
  summary: "<one-paragraph statement of what this architecture governs>",
  in_system: [ "<capability / component inside the boundary>", ... ],
  out_of_system: [ "<explicitly external system, actor, or deferred capability>", ... ]
}
```

`scope_baseline.out_of_scope` items and `scope_baseline.future` items map to
`out_of_system`. IF scope is ambiguous: HALT and AskUserQuestion.

**VERIFY:**
- `summary` is a non-empty paragraph
- `in_system` has ≥ 1 entry

**RECORD:**
```bash
devforgeai-validate phase-record ${SYSARCH_ID} --workflow=system-architecture --phase=05 --step=5.1 --project-root=. 2>&1
```
```json
{ "phase": "05", "step": "5.1", "system_boundary": { ... } }
```

---

### Step 5.2: Map the Integration Topology

**EXECUTE:**

For every external system, service, or actor the system exchanges data with,
create an `integration_point`:

```
integration_topology = [
  {
    id: "INT-001",                       # ^INT-[0-9]{3,}$
    name: "<external system / service / actor>",
    direction: "inbound" | "outbound" | "bidirectional",
    protocol: "<e.g. REST/HTTPS, gRPC, message queue, file transfer>",
    trust_boundary: <true if it crosses a trust/security boundary>,
    description: "<what is exchanged and why>"
  }, ...
]
```

Source integrations from PM-plan requirements and constraints. A system with no
external integrations records an empty array — but state that explicitly, do not
silently omit. Every `trust_boundary: true` integration is a security-sensitive
decision (HALT trigger #7) — confirm its handling with the user.

**VERIFY:**
- Every integration point has `id`, `name`, `direction`
- Every `id` matches `^INT-[0-9]{3,}$` and is unique

**RECORD:**
```bash
devforgeai-validate phase-record ${SYSARCH_ID} --workflow=system-architecture --phase=05 --step=5.2 --project-root=. 2>&1
```
```json
{ "step": "5.2", "integration_topology": [ ... ] }
```

---

### Step 5.3: Assemble the Tech-Stack Rationale

**EXECUTE:**

For each locked technology in `tech-stack.md`, build a `tech_decision`:

```
tech_stack_rationale = [
  {
    component: "<language | framework | database | ORM | message bus | ...>",
    choice: "<the locked choice>",
    rationale: "<why, grounded in the PM plan / NFRs / constraints>",
    alternatives_considered: [ "<alt>", ... ],
    adr_ref: "ADR-NNN"               # present when the decision is significant
  }, ...
]
```

Cross-link `adr_ref` to the ADRs written in Phase 04. A decision with a real
alternative but no ADR → return to Phase 04 reasoning and create the ADR (do not
leave a significant decision uncaptured).

**VERIFY:**
- Every entry has `component`, `choice`, `rationale` (all non-empty)
- Every `adr_ref` present corresponds to an ADR file on disk

**RECORD:**
```bash
devforgeai-validate phase-record ${SYSARCH_ID} --workflow=system-architecture --phase=05 --step=5.3 --project-root=. 2>&1
```
```json
{ "step": "5.3", "tech_stack_rationale": [ ... ] }
```

---

### Step 5.4: Define System-Level NFRs

**EXECUTE:**

Refine the PM-plan NFRs and `success_criteria` into quantified, system-level
non-functional requirements:

```
system_nfrs = [
  {
    id: "SNFR-001",                  # ^SNFR-[0-9]{3,}$
    category: "performance" | "scalability" | "availability" | "security" |
              "maintainability" | "observability" | "compliance",
    statement: "<the requirement>",
    target: "<quantified target, e.g. 'p95 < 200ms', '99.9% uptime'>",
    source: "pm-plan:SC-NNN" | "system-architecture"
  }, ...
]
```

Each `success_criteria` entry from the PM plan should trace to at least one SNFR.
A non-functional concern with no quantifiable target → flag it and ask the user
for a measurable target rather than recording a vague statement.

**VERIFY:**
- Every SNFR has `id`, `category`, `statement`
- `category` is one of the 7 enum values
- Every `id` matches `^SNFR-[0-9]{3,}$` and is unique

**RECORD:**
```bash
devforgeai-validate phase-record ${SYSARCH_ID} --workflow=system-architecture --phase=05 --step=5.4 --project-root=. 2>&1
```
```json
{ "step": "5.4", "system_nfrs": [ ... ] }
```

---

### Step 5.5: Define the Deployment Architecture

**EXECUTE:**
```
deployment_architecture = {
  summary: "<how the system is deployed and operated>",
  environments: [ "<e.g. local, staging, production>", ... ],
  runtime_topology: "<hosting model + runtime layout, e.g. 'single container on
                      a managed PaaS', 'k8s cluster, 3 services + managed DB'>"
}
```

Deployment detail is recommended but may be coarse at inception — record what is
grounded and leave finer detail to `/create-solution-architecture`. Mark any
genuine unknown as an open question for the handoff (Phase 07).

**VERIFY:**
- `deployment_architecture.summary` is non-empty
- `environments` has ≥ 1 entry

**RECORD:**
```bash
devforgeai-validate phase-record ${SYSARCH_ID} --workflow=system-architecture --phase=05 --step=5.5 --project-root=. 2>&1
```
```json
checkpoint.phases["05"] = {
  "status": "completed",
  "system_boundary": { ... },
  "integration_topology": [ ... ],
  "tech_stack_rationale": [ ... ],
  "system_nfrs": [ ... ],
  "deployment_architecture": { ... }
}
```

---

## Exit Gate

```bash
devforgeai-validate phase-complete ${SYSARCH_ID} --workflow=system-architecture --phase=05 --checkpoint-passed --project-root=. 2>&1
```

| Exit Code | Action |
|-----------|--------|
| 0 | Phase 05 complete — proceed to next phase |
| 127 | CLI not installed — proceed without enforcement |
| Other | HALT — checkpoint/step validation failed |

---

## Phase Transition Display

```
Display:
  "Phase 05 Complete: System Design"
  "Integrations: {count}  |  Tech decisions: {count}  |  System NFRs: {count}"
  "Proceeding to Phase 06: Architecture Review"
```
