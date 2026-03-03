# ADR-018: Code Smell Catalog Location Decision

## Status

Accepted

## Context

The anti-pattern-scanner subagent detects 11 code smell types during Phase 5 (Code Smells Scan). As the detection catalog has grown from 5 to 11 smell types across STORY-399 through STORY-407, a canonical location for the complete detection rules, thresholds, and test scenarios is needed.

Two candidate locations were considered:

1. **Constitutional anti-patterns.md** (`devforgeai/specs/context/anti-patterns.md`) — the framework's locked anti-pattern constraints
2. **Anti-pattern-scanner reference files** (`.claude/agents/anti-pattern-scanner/references/`) — the subagent's progressive disclosure reference directory

## Decision

Code smell detection rules are placed in anti-pattern-scanner reference files (`.claude/agents/anti-pattern-scanner/references/code-smell-catalog.md`), rather than in the constitutional anti-patterns.md context file.

The catalog is NOT added to anti-patterns.md because that file serves a different purpose: defining framework-level anti-patterns that all agents must avoid, not project-level code smell detection rules for a specific scanner subagent.

## Rationale

The anti-patterns.md v1.1 file (line 285) explicitly distinguishes between framework anti-patterns and project-level patterns:

> "Projects using DevForgeAI will have their own anti-patterns.md with project-specific forbidden patterns (SQL injection, N+1 queries, God objects, etc.)."

This distinction between framework vs project patterns means:

- **Framework anti-patterns** (anti-patterns.md): Tool usage violations, monolithic components, assumptions, size violations — these apply to the DevForgeAI framework itself
- **Project code smells** (code-smell-catalog.md): God objects, long methods, magic numbers — these are detection rules the scanner applies to user project code

Placing project-level detection rules in the constitutional file would:
1. Violate the separation of concerns between framework constraints and project scanning rules
2. Bloat the LOCKED context file beyond its 600-line target (adding 11 detailed smell sections)
3. Require a LOCKED status change and ADR for every threshold adjustment

The progressive disclosure pattern (ADR-012) already supports reference subdirectories for subagents exceeding 500 lines, making `.claude/agents/anti-pattern-scanner/references/` the natural location.

## Consequences

- No constitutional file modification required — anti-patterns.md remains unchanged
- No LOCKED status change needed — the LOCKED status of anti-patterns.md is preserved unchanged
- The code-smell-catalog.md can be updated without requiring an ADR (it is reference documentation, not a constitutional constraint)
- The anti-pattern-scanner loads the catalog via progressive disclosure: `Read(file_path=".claude/agents/anti-pattern-scanner/references/code-smell-catalog.md")`
- Source-tree.md is updated to v3.9 to document the new reference file path
