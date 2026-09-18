# Phase 04: ADR Creation

## Entry Gate

```bash
devforgeai-validate phase-check ${SYSARCH_ID} --workflow=system-architecture --from=03 --to=04 --project-root=. 2>&1
```

| Exit Code | Action |
|-----------|--------|
| 0 | Proceed to Phase 04 |
| 127 | CLI not installed — proceed without enforcement |
| Other | HALT — previous phase not complete |

---

## Contract

| Attribute | Value |
|-----------|-------|
| **PURPOSE** | Capture every architecturally significant decision made while building the constitution as an Architecture Decision Record. ADRs make the *why* behind the locked tech stack and constraints durable and auditable. |
| **REFERENCE** | `.claude/skills/spec-driven-system-architecture/assets/adr-examples/ADR-EXAMPLE-001-database-selection.md` (canonical ADR structure) |
| **STEP COUNT** | 4 mandatory steps |

## Phase Exit Criteria

Before this phase can complete, ALL of the following MUST be true:

- [ ] Architecturally significant decisions enumerated (≥ 1)
- [ ] One ADR file written per significant decision, numbered without collision
- [ ] Each ADR has Status, Date, Context, Decision, Consequences sections
- [ ] `adr_refs[]` recorded for the Phase 07 output contract

**IF any criterion is unmet: HALT. Do NOT proceed to Phase 05.**

---

## Reference Loading

```
Read(file_path=".claude/skills/spec-driven-system-architecture/assets/adr-examples/ADR-EXAMPLE-001-database-selection.md")
```

IF the Read fails: HALT — "Phase 04 ADR template not loaded."

Do NOT rely on memory of previous reads. Load fresh every time this phase executes.

---

## Mandatory Steps

### Step 4.1: Identify Architecturally Significant Decisions

**EXECUTE:**

A decision is **architecturally significant** when it is costly to reverse, shapes
multiple components, or locks a constraint. Scan the Phase 02–03 checkpoints for:

- The architecture style selection (Phase 02)
- Each locked technology in `tech-stack.md` that had a real alternative
- Integration / boundary decisions implied by PM-plan integrations
- Any PM-plan constraint resolved by overriding rather than complying (Phase 02 Step 2.4)

```
significant_decisions = [ { topic, context, decision, alternatives, consequences } ]
```

**VERIFY:**
- At least 1 significant decision identified (a project always has ≥ 1 — the
  architecture style itself)
- Each decision records the alternatives that were considered

**RECORD:**
```bash
devforgeai-validate phase-record ${SYSARCH_ID} --workflow=system-architecture --phase=04 --step=4.1 --project-root=. 2>&1
```
```json
{ "phase": "04", "step": "4.1", "significant_decisions": [ { "topic": "..." } ] }
```

---

### Step 4.2: Allocate ADR Numbers

**EXECUTE:**
```
Glob(pattern="devforgeai/specs/adrs/ADR-*.md")
Determine the highest existing ADR-NNN. Allocate the next N consecutive numbers,
one per significant decision. ADRs are append-only — never reuse or edit an
existing number (configuration-layer-mutability rule).
```

**VERIFY:**
- No allocated number collides with an existing ADR file
- The count of allocated numbers equals the count of significant decisions

**RECORD:**
```bash
devforgeai-validate phase-record ${SYSARCH_ID} --workflow=system-architecture --phase=04 --step=4.2 --project-root=. 2>&1
```
```json
{ "step": "4.2", "adr_numbers_allocated": ["ADR-NNN", "..."] }
```

---

### Step 4.3: Write the ADR Files

**EXECUTE:**

For each significant decision, write an ADR following the loaded template:

```
Write(
  file_path="devforgeai/specs/adrs/ADR-<NNN>-<kebab-topic>.md",
  content="
# ADR-<NNN>: <Decision Title>

**Status:** Accepted
**Date:** <ISO 8601 date>
**Source:** spec-driven-system-architecture / ${SYSARCH_ID}

## Context
<the forces and PM-plan grounding behind the decision>

## Decision
<the choice that was made>

## Alternatives Considered
<each alternative and why it was rejected>

## Consequences
<positive outcomes, trade-offs, and follow-up implications>
"
)
```

Cross-link: each ADR that locks a technology should be referenced from the
matching `tech_decision.adr_ref` field assembled in Phase 05.

**VERIFY:**
- `Glob(pattern="devforgeai/specs/adrs/ADR-*.md")` count increased by exactly the
  number of significant decisions
- Each new ADR contains all 5 sections (Status, Date, Context, Decision,
  Consequences) and no placeholder text

**RECORD:**
```bash
devforgeai-validate phase-record ${SYSARCH_ID} --workflow=system-architecture --phase=04 --step=4.3 --project-root=. 2>&1
```
```json
{ "step": "4.3", "adrs_written": [ { "path": "...", "topic": "..." } ] }
```

---

### Step 4.4: Record ADR References

**EXECUTE:**
```
adr_refs = [ the ADR-NNN id of every ADR written this phase ]
```

**VERIFY:**
- `adr_refs` is non-empty
- Every id matches `^ADR-[0-9]{3,}$`

**RECORD:**
```bash
devforgeai-validate phase-record ${SYSARCH_ID} --workflow=system-architecture --phase=04 --step=4.4 --project-root=. 2>&1
```
```json
checkpoint.phases["04"] = {
  "status": "completed",
  "adr_refs": ["ADR-NNN", "..."],
  "adrs_written": [ { "path": "...", "topic": "..." } ]
}
```

---

## Exit Gate

```bash
devforgeai-validate phase-complete ${SYSARCH_ID} --workflow=system-architecture --phase=04 --checkpoint-passed --project-root=. 2>&1
```

| Exit Code | Action |
|-----------|--------|
| 0 | Phase 04 complete — proceed to next phase |
| 127 | CLI not installed — proceed without enforcement |
| Other | HALT — checkpoint/step validation failed |

---

## Phase Transition Display

```
Display:
  "Phase 04 Complete: ADR Creation"
  "ADRs created: {count} ({adr_refs joined})"
  "Proceeding to Phase 05: System Design"
```
