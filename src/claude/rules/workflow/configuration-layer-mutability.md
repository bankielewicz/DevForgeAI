# Configuration Layer Mutability Rules

**Purpose:** Define which configuration layers can be edited, and how.
**Reference:** ADR-021 (Configuration Layer Alignment Protocol)

---

## Layer Mutability

| Layer | Mutability | Edit Protocol |
|-------|-----------|---------------|
| **CLAUDE.md** | MUTABLE | Direct edit with user approval via AskUserQuestion |
| **System Prompt** | MUTABLE | Direct edit with user approval via AskUserQuestion |
| **Context Files** (6 in `devforgeai/specs/context/`) | IMMUTABLE | Requires ADR approval + `/create-context` workflow. Never call Edit() directly. |
| **Rules** (`.claude/rules/`) | MUTABLE | Direct edit with user approval via AskUserQuestion |
| **ADRs** (`devforgeai/specs/adrs/`) | APPEND-ONLY | Never edit existing ADRs. Create new ADR to supersede. |

---

## Context Files (IMMUTABLE)

The following 6 files are constitutional and cannot be modified without an ADR:

1. `devforgeai/specs/context/tech-stack.md`
2. `devforgeai/specs/context/source-tree.md`
3. `devforgeai/specs/context/dependencies.md`
4. `devforgeai/specs/context/coding-standards.md`
5. `devforgeai/specs/context/architecture-constraints.md`
6. `devforgeai/specs/context/anti-patterns.md`

**HALT Trigger:** Any attempt to call Edit() or Write() on these files without an accepted ADR must HALT immediately.

---

## ADR Propagation Verification

When an ADR is accepted, verify its decisions are propagated to all affected layers:

1. Check CLAUDE.md for references to the ADR's decisions
2. Check rules files for enforcement of the ADR's decisions
3. Check system prompt for alignment with the ADR's decisions
4. Run `/audit-alignment` to detect drift

**Unpropagated ADRs** are detected as "adr_drift" findings by the alignment-auditor subagent.

---

## Contradiction Resolution

When two layers contradict:

1. **IMMUTABLE wins over MUTABLE** — Context files take precedence
2. **Newer ADR wins over older** — Latest accepted ADR is authoritative
3. **Specific wins over general** — Rule file beats CLAUDE.md summary
4. **When ambiguous** — HALT and use AskUserQuestion
