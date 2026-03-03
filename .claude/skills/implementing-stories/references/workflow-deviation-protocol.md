# Workflow Deviation Protocol

**Source:** RCA-019 REC-4
**Purpose:** Require explicit user consent before phase skipping, subagent omission, or out-of-sequence execution.

---

## Deviation Types

| Type | Description | Trigger |
|------|-------------|---------|
| **Phase Skipping** | Skip Phase N to N+2 | Claude considers phase unnecessary |
| **Subagent Omission** | Skip required subagent | Claude believes subagent adds no value |
| **Out-of-Sequence** | Execute N+1 before N | Claude wants to parallelize/reorder |

**BLOCKING subagents = MANDATORY (cannot omit).** Conditional subagents = OPTIONAL (may skip with reason).

---

## Consent Protocol (MANDATORY)

IF considering ANY workflow deviation, you MUST invoke AskUserQuestion:

```
AskUserQuestion(questions=[{
  question: "I am considering: {deviation}. This deviates from TDD workflow. How should I proceed?",
  header: "Workflow Deviation Request",
  options: [
    {label: "Follow workflow", description: "Execute required {phase/subagent} as documented"},
    {label: "Skip with documentation", description: "Skip and document in story Implementation Notes"},
    {label: "User override", description: "I authorize this specific deviation"}
  ]
}])
```

**Do NOT proceed until user responds.**

---

## Response Processing

| Option | Action | Story File Update |
|--------|--------|-------------------|
| **Follow workflow** | Execute required phase/subagent | None |
| **Skip with documentation** | Update Implementation Notes with: Deviation, Reason, Authorization timestamp, Impact | `### Authorized Deviations` table |
| **User override** | Record override with timestamp | `### User Overrides` list |

**Optional:** After "Skip with documentation", suggest: *"Consider running '/rca {reason}' to analyze deviation pattern."*

---

## Enforcement

Per architecture-constraints.md HALT pattern: Claude MUST NOT rationalize deviations without explicit user consent via AskUserQuestion.
