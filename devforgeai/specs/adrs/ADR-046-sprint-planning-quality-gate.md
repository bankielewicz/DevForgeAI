# ADR-046: Sprint Planning Quality Gate (Gate 0S)

**Date**: 2026-03-22
**Status**: Accepted
**Deciders**: Project Owner, DevForgeAI Framework Architect
**Project**: DevForgeAI Spec-Driven Development Framework

---

## Context

The DevForgeAI framework defines 4 quality gates (Gates 1-4) covering the Architecture-through-Release workflow:

| Gate | Transition | Enforced By |
|------|-----------|-------------|
| Gate 1 | Architecture → Ready for Dev | spec-driven-lifecycle |
| Gate 2 | Dev Complete → QA In Progress | spec-driven-qa |
| Gate 3 | QA Approved → Releasing | spec-driven-release |
| Gate 4 | Releasing → Released | spec-driven-release |

(Source: `src/claude/skills/spec-driven-lifecycle/references/quality-gates.md`)

However, **no quality gate exists for the Planning-to-Sprint transition**. The `/create-sprint` command and Phase 03S (`src/claude/skills/spec-driven-lifecycle/phases/phase-03S-sprint-planning.md`) currently validate only:

1. Story files exist (Step 2, lines 43-82)
2. Story status equals "Backlog" (Step 2, line 60)
3. Total story points fall within the 20-40 optimal range (Step 3, lines 84-122)

This allows sprints to be created with:

- **Unresolved dependencies**: Stories with `depends_on` references to stories that are not in the sprint and not yet completed
- **Circular dependencies**: Mutually blocking stories included in the same sprint
- **File conflicts**: Multiple stories modifying the same source files without sequencing awareness
- **Incomplete functional areas**: Partial feature sets where only some stories for an epic feature are included
- **Multi-sprint assignment**: Stories already assigned to a different sprint being added to a new one

Two existing subagents already solve the dependency and overlap concerns but are only invoked during `/dev` Phase 01 (after sprint commitment):

- `dependency-graph-analyzer` (`.claude/agents/dependency-graph-analyzer.md`, 194 lines): Parses `depends_on` YAML, builds transitive graphs, detects cycles via DFS, validates dependency completion status
- `file-overlap-detector` (`.claude/agents/file-overlap-detector.md`, 200 lines): Parses `technical_specification` YAML for file paths, cross-references across stories, filters dependency-chain overlaps

The epic template already contains a `## Target Sprints` section (`src/claude/skills/spec-driven-architecture/assets/templates/epic-template.md`, lines 69-98) with feature-to-sprint-to-story mapping, but `/create-sprint` never reads this section.

This gap was identified through correlation analysis with RESEARCH-002 (Epic vs Sprint in the SDLC), which documents that corporate Agile frameworks validate dependency chains, feature cohesion, and functional completeness before sprint commitment.

---

## Decision

Introduce **Gate 0S (Sprint Planning Gate)** as a new quality gate that executes within Phase 03S. Gate 0S consists of 3 new validation steps inserted between existing Step 2 (Validate Selected Stories) and Step 3 (Calculate Capacity):

### New Steps

**Step 2.5: Dependency Chain Validation**
- Invoke `dependency-graph-analyzer` subagent for each selected story with `depends_on` entries
- Pass the sprint selection list so intra-sprint dependencies are accepted as satisfied
- Validate all dependencies are either (a) in the same sprint or (b) already completed (Dev Complete, QA Approved, or Released)
- Detect cycles among selected stories
- Status: BLOCKED if unresolved dependencies or cycles detected

**Step 2.6: File Overlap Detection**
- Invoke `file-overlap-detector` subagent in pre-flight mode across all selected stories
- Detect stories that modify the same files
- Filter overlaps from `depends_on` chains (intentional sequencing)
- Status: WARNING for 1-9 overlaps (recommend execution order), BLOCKED for 10+ overlaps

**Step 2.7: Feature Cohesion + Multi-Sprint Assignment Check**
- Parse the linked epic's `## Target Sprints` section (if present)
- Verify selected stories do not split a feature across this sprint and a future sprint (partial feature shipment)
- Verify no selected story is already assigned to a different sprint (`sprint:` field not empty/Backlog)
- Status: WARNING for partial features, BLOCKED for multi-sprint assignment
- Gracefully SKIP if epic has no Target Sprints section or no epic is linked

### Gate Properties

- **Follows existing Quality Gate Pattern** (Source: `devforgeai/specs/context/architecture-constraints.md`, lines 104-116)
- **Bypassable**: User can proceed with documented exception via AskUserQuestion (same as Gate 1)
- **Non-destructive**: Gate validates only; does not modify story files or sprint state
- **Incremental**: Each check runs independently; partial results are useful even if one check fails

### What Does NOT Change

- No modifications to `dependency-graph-analyzer` or `file-overlap-detector` agents (behavior driven by prompt)
- No modifications to immutable context files
- No changes to Gates 1-4 behavior
- Sprint planning mode phase sequence remains `[01, 03S, 08]`
- Existing sprint creation workflow (no deps, no overlaps) passes Gate 0S transparently

### Gate Hierarchy After This Decision

```
Gate 0S: Sprint Planning (Story Selection → Sprint Creation)
  ↓
Gate 1: Context Validation (Architecture → Ready for Dev)
  ↓
Gate 2: Test Passing (Dev Complete → QA In Progress)
  ↓
Gate 3: QA Approval (QA Approved → Releasing)
  ↓
Gate 4: Release Readiness (Releasing → Released)
```

---

## Consequences

### Positive

- Dependencies validated before sprint commitment, preventing blocked stories from entering sprints
- File overlaps surfaced early, enabling informed sequencing decisions and reducing merge conflict risk
- Feature cohesion prevents partial feature shipments that would deliver incomplete functionality
- Reuses existing subagents with no modifications (prompt-driven behavior)
- Aligns with corporate Agile best practices documented in RESEARCH-002
- Adds approximately 3 steps to Phase 03S (~200 lines), maintaining skill size within the 500-800 line target

### Negative

- Sprint creation takes slightly longer (2 subagent invocations add ~10-20 seconds each)
- Feature cohesion check requires epics to have populated `## Target Sprints` sections; older epics without this section will skip the check with an informational message
- Users must resolve or explicitly accept dependency/overlap issues before sprint creation completes

### Neutral

- Does not change any immutable context files (no ADR propagation to context layer needed)
- Does not change any existing quality gate behavior (Gates 1-4 unaffected)
- Does not modify `dependency-graph-analyzer` or `file-overlap-detector` agents
- Sprint planning mode phase sequence `[01, 03S, 08]` unchanged; gate logic is internal to 03S

---

## References

- RESEARCH-002: `devforgeai/specs/research/shared/RESEARCH-002-epic-vs-sprint-sdlc-relationship.md`
- Quality Gates: `src/claude/skills/spec-driven-lifecycle/references/quality-gates.md`
- Phase 03S: `src/claude/skills/spec-driven-lifecycle/phases/phase-03S-sprint-planning.md`
- Dependency Graph Analyzer: `.claude/agents/dependency-graph-analyzer.md`
- File Overlap Detector: `.claude/agents/file-overlap-detector.md`
- Architecture Constraints (Quality Gate Pattern): `devforgeai/specs/context/architecture-constraints.md`, lines 104-116
