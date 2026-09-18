# Workflow Deviation Protocol

**Source:** RCA-019 REC-4
**Purpose:** Require explicit user consent before phase skipping, subagent omission, out-of-sequence execution, or phase regression.

---

## Deviation Types

| Type | Description | Trigger |
|------|-------------|---------|
| **Phase Skipping** | Skip Phase N to N+2 | Claude considers phase unnecessary |
| **Subagent Omission** | Skip required subagent | Claude believes subagent adds no value |
| **Out-of-Sequence** | Execute N+1 before N | Claude wants to parallelize/reorder |
| **Phase Regression** | Return from Phase N to earlier Phase M (M < N) | Test infrastructure defect, subagent output defect, or other defect requiring earlier-phase re-execution |

**BLOCKING subagents = MANDATORY (cannot omit).** Conditional subagents = OPTIONAL (may skip with reason).

### Phase Regression Rules
- MUST be initiated via test-folder-protection AskUserQuestion "Return to Phase 02" option (for test defects)
- MUST re-invoke the authorized subagent for the target phase (e.g., test-automator for Phase 02)
- MUST regenerate any integrity snapshots (e.g., red-phase checksums) after re-execution
- Maximum 2 regressions per story per phase

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
