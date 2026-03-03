# ADR-016: Dead Code Detector Read-Only Constraint

**Status:** Accepted
**Date:** 2026-02-14
**Decision Makers:** DevForgeAI Framework Team
**Context:** STORY-403, EPIC-064

---

## Context

The dead-code-detector subagent identifies unused functions through call-graph analysis. Unlike refactoring tools that modify code, this subagent's purpose is detection only.

**Key consideration:** False positives in dead code detection are common due to:
- Dynamic dispatch (getattr, reflection)
- Framework-invoked functions (routes, fixtures, handlers)
- Inheritance and polymorphism
- Plugin/extension architectures

Granting Write/Edit access would create risk of incorrect code deletion.

---

## Decision

**The dead-code-detector subagent is restricted to read-only tools.**

**Allowed tools:**
- `Read` - Read source files for analysis
- `Bash(treelint:*)` - AST-aware code search via Treelint
- `Grep` - Text-based fallback for unsupported languages
- `Glob` - File pattern matching

**Prohibited tools:**
- `Write` - Cannot create files
- `Edit` - Cannot modify files

---

## Rationale

### Safety First

Dead code detection has inherent uncertainty. Even with high confidence (0.9), there's a 10% chance of false positive. Automated deletion based on analysis could:
- Remove framework-invoked code (routes, event handlers)
- Delete dynamically-called functions (reflection, string dispatch)
- Break plugin/extension interfaces
- Remove overridden methods used polymorphically

### Separation of Concerns

| Subagent | Purpose | Tools |
|----------|---------|-------|
| dead-code-detector | Detection (read-only) | Read, Bash(treelint:*), Grep, Glob |
| refactoring-specialist | Modification (write) | Read, Write, Edit, Bash(test) |

Dead code removal should be a deliberate user action after reviewing findings, not an automated operation.

### Principle of Least Privilege

Per tech-stack.md: "Only grant tools needed for subagent's domain."

Dead code detection requires:
- Reading source files (Read)
- Searching code structure (Treelint/Grep)
- Finding files (Glob)

It does NOT require writing or editing.

---

## Consequences

### Positive

- **Zero risk of incorrect deletion** - Subagent cannot modify code
- **User maintains control** - All removals are deliberate
- **Builds trust** - Safe to run on production codebases
- **Clear responsibility** - Detection vs. modification are separate

### Negative

- **Manual cleanup required** - User must remove dead code manually
- **Two-step process** - Detect with dead-code-detector, remove with refactoring-specialist
- **Slightly more effort** - Cannot "fix" in one step

### Acceptable Trade-off

The safety guarantee of read-only operation outweighs the convenience of automated deletion. Dead code removal is infrequent and low-urgency, making manual review appropriate.

---

## Compliance

**Enforcement:**
- Tools list in dead-code-detector.md frontmatter: `tools: Read, Bash(treelint:*), Grep, Glob`
- Test in tests/STORY-403/test_ac6_read_only_constraint.py validates no Write/Edit

**Audit:**
- Any modification to tools list requires ADR amendment
- PR review must verify read-only constraint preserved

---

## Related Decisions

- **ADR-013:** Treelint Integration for AST-aware code search
- **tech-stack.md:** Tool restriction patterns for subagents
- **architecture-constraints.md:** Principle of least privilege

---

## References

- STORY-403: Create Dead-Code-Detector Subagent
- EPIC-064: AI-Generated Code Smell Detection Gap Closure
