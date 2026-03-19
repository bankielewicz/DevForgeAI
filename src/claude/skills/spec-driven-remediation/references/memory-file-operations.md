# Memory File Operations for Remediation

Defines how session memory files are created, updated, and read for the remediation workflow. Adapted from the spec-driven-dev memory file pattern.

---

## Session Memory File

**Location:** `.claude/memory/sessions/${SESSION_ID}-remediation-session.md`

**Purpose:** Human-readable session state that persists across context window clears. Complements the machine-readable checkpoint YAML.

---

## Schema

```markdown
---
session_id: FIX-custody-chain-audit-stories-413-424
audit_file: devforgeai/qa/audit/custody-chain-audit-stories-413-424.md
workflow_name: remediation
current_phase: "03"
phase_progress: 0.6
mode: full
decisions:
  - timestamp: "2026-03-18T14:35:00Z"
    description: "Apply all automated fixes"
    rationale: "User approved batch application"
  - timestamp: "2026-03-18T14:40:00Z"
    description: "Defer F-001 (context/invalid_path)"
    rationale: "Requires ADR for source-tree.md change"
blockers:
  - id: B-001
    description: "F-003 verification failed after 2 retries"
    severity: medium
    resolution_status: deferred
---

# Remediation Session: FIX-custody-chain-audit-stories-413-424

## Summary

Remediating findings from custody-chain-audit-stories-413-424.md
- Total findings: 12
- Automated: 5 | Interactive: 4 | ADR: 2 | Advisory: 1

## Phase Progress

- [x] Phase 00: Context Loading (5 findings loaded)
- [x] Phase 01: Triage (5 auto, 4 interactive, 2 ADR, 1 advisory)
- [x] Phase 02: Preview (user approved: apply all)
- [ ] Phase 03: Execution (3/5 automated complete)
- [ ] Phase 04: Verification
- [ ] Phase 05: Reporting

## Applied Fixes

- F-002: quality/broken_file_reference → STORY-414 (use=xml-tags.md → use-xml-tags.md)
- F-003: provenance/missing_brainstorm_frontmatter → EPIC-066 (added brainstorm field)
- F-005: quality/stale_status_label → STORY-420 (status: Ready → In Development)

## Deferred Items

- F-001: context/invalid_path (requires ADR for source-tree.md)

## Notes

{Free-form notes about the session}
```

---

## Operations

### Create Session Memory (Phase 00)

```
Write(
    file_path=".claude/memory/sessions/${SESSION_ID}-remediation-session.md",
    content=<populated template with initial values>
)
```

### Update Session Memory (After Each Phase)

```
Read(file_path=".claude/memory/sessions/${SESSION_ID}-remediation-session.md")
Edit phase progress checkboxes
Edit applied fixes list
Edit deferred items list
```

### Read Session Memory (On Resume)

```
Read(file_path=".claude/memory/sessions/${SESSION_ID}-remediation-session.md")
Extract current_phase from frontmatter
Extract decisions and blockers
Use to display "Resuming session..." message
```

---

## Checkpoint vs Session Memory

| Aspect | Checkpoint (YAML) | Session Memory (MD) |
|--------|-------------------|---------------------|
| Format | Machine-readable YAML | Human-readable Markdown |
| Location | `devforgeai/temp/` | `.claude/memory/sessions/` |
| Purpose | Exact state for resume | Context summary for understanding |
| Updated | After every state change | After each phase |
| Read by | Phase orchestration loop | Resume detection, user reference |
