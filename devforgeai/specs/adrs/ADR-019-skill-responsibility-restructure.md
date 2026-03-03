# ADR-019: Skill Responsibility Restructure — Epic Decomposition Migration

**Status:** Accepted
**Date:** 2026-02-17
**Decision Makers:** DevForgeAI Framework Team
**Context:** EPIC-067 (conformance remediation), ADR-017 (gerund naming)

---

## Context

Epic creation responsibility is currently split across **three skills**, none of which is the natural owner (architecture):

1. **`devforgeai-ideation`** owns epic analysis content: decomposition workflows, feasibility analysis, complexity assessment (~2,935 lines across 6 files)
2. **`devforgeai-orchestration`** owns the epic creation engine: Phase 4A with 8 sub-phases, feature decomposition patterns, technical assessment, validation (~3,770 lines across 7 files + template)
3. **`devforgeai-architecture`** owns zero epic content — only context files and ADRs (279-line SKILL.md)

This triple-ownership creates three problems:

- **Overlapping content:** Both ideation and orchestration have feature decomposition patterns (separate files, equivalent domain coverage). Both can independently generate epic files to the same output directory.
- **Incompatible scoring:** Ideation uses a 0-60 scale (4 dimensions) while orchestration uses a 0-10 scale (5 bands) for complexity — producing conflicting assessments.
- **Wrong ownership:** The architect role should own epic creation, but the architecture skill has zero epic functionality.

The current workflow:
```
brainstorming (BA) → ideation (PM + Architect) → architecture (context files only)
/create-epic → orchestration (epic engine) — bypasses architecture entirely
```

This violates the Single Responsibility Principle documented in `devforgeai/specs/context/architecture-constraints.md` (lines 28-34):
> **Single Responsibility Principle**:
> - Each skill handles ONE phase of development lifecycle
> - ✅ implementing-stories: TDD implementation only
> - ✅ validating-quality: Quality validation only
> - ❌ implementing-and-validating: Multiple responsibilities

The ideation skill is effectively "requirements-and-architecture" and the orchestration skill is "coordination-and-architecture" — both have leaked architectural responsibilities.

---

## Decision

### 1. Move epic creation engine from orchestration to architecture

The following reference files transfer from `devforgeai-orchestration` to `devforgeai-architecture`:

| File | Lines | Phase | Responsibility |
|------|-------|-------|---------------|
| `epic-management.md` | 514 | 4A.1-2 | Epic discovery, context gathering |
| `feature-decomposition-patterns.md` | 903 | 4A.3 | Domain-specific decomposition (7 patterns) |
| `feature-analyzer.md` | 282 | 4A.3 | Parallel feature analysis batching |
| `dependency-graph.md` | 221 | 4A.3 | Dependency detection, cycle detection |
| `technical-assessment-guide.md` | 914 | 4A.4 | Complexity scoring (0-10), risk identification |
| `epic-validation-checklist.md` | 760 | 4A.7 | 9 validation checks, self-healing |
| `epic-validation-hook.md` | 76 | 4A.6 | CLI validation hook |
| `assets/templates/epic-template.md` | 265 | 4A.5 | Epic document template |

**Total moved:** ~3,935 lines from orchestration → architecture

### 2. Move epic analysis references from ideation to architecture

The following reference files transfer from `devforgeai-ideation` to `devforgeai-architecture`:

| File | Lines | Responsibility |
|------|-------|---------------|
| `epic-decomposition-workflow.md` | 309 | Feature breakdown, prioritization matrix |
| `feasibility-analysis-workflow.md` | 543 | Technical feasibility assessment |
| `feasibility-analysis-framework.md` | ~600 | Deep feasibility scoring criteria |
| `complexity-assessment-workflow.md` | 333 | Complexity scoring execution |
| `complexity-assessment-matrix.md` | ~800 | 4-dimension scoring rubric |
| `artifact-generation.md` (epic sections) | ~350 | Epic template generation |

**Total moved:** ~2,935 lines from ideation → architecture

### 3. Resolve overlapping content and unify complexity scoring

Overlapping content between orchestration and ideation must be merged:
- **Feature decomposition:** Merge `epic-decomposition-workflow.md` (ideation) and `feature-decomposition-patterns.md` (orchestration) into single authoritative file
- **Complexity scoring:** Unify the 0-60 scale (ideation, 4 dimensions) and 0-10 scale (orchestration, 5 bands) into single scoring system

### 4. Redefine skill boundaries

**After restructure:**

| Skill | Role | Responsibility | Primary Output |
|-------|------|---------------|----------------|
| brainstorming | Business Analyst | Discovery, problem framing, domain exploration | `brainstorm.md` |
| ideation (renamed) | Product Manager | Requirements elicitation, PRD creation, success metrics | `requirements.md` |
| architecture (renamed) | Architect | Epic decomposition, context files, ADRs, technical specs | `epic.md` + `context/*.md` |

**Handoff chain:**
```
brainstorming → ideation → architecture → story-creation → implementing-stories
     BA             PM         Architect       PM/Dev            Developer
```

### 5. Update architecture skill phases

The architecture skill gains new phases for epic creation:

- **New Phase:** Epic Decomposition (receives requirements.md, produces epic.md with features)
- **New Phase:** Feasibility & Complexity Assessment (scores each feature)
- **New Phase:** Sprint Target Planning (groups features into sprints)
- **Existing Phase:** Context File Creation (unchanged)
- **Existing Phase:** ADR Creation (unchanged)

### 6. Remove Phase 4A from orchestration skill

The orchestration skill loses its entire Phase 4A (Epic Creation) mode:

- **Removed:** Phase 4A (8 sub-phases) and all epic-specific reference files
- **Removed:** Epic creation mode from `mode-detection.md`
- **Retained:** Story lifecycle management, sprint planning, audit deferrals, QA retry
- **Re-routed:** `/create-epic` command invokes architecture skill directly instead of orchestration

### 7. Update ideation skill phases and output format

The ideation skill sheds epic-related phases and adopts structured YAML output:

- **Retained:** Discovery workflow (stakeholder questions, problem framing)
- **Retained:** Requirements elicitation (structured requirements gathering)
- **Retained:** Validation & self-check
- **Changed:** Completion handoff produces YAML-structured requirements.md (not narrative PRD, not epic)
- **Removed:** Epic decomposition (moved to architecture)
- **Removed:** Feasibility analysis (moved to architecture)
- **Removed:** Complexity assessment (moved to architecture)

### 8. Define structured requirements schema for cross-session context preservation

Each workflow in DevForgeAI runs in a separate session with no memory of previous conversations. The handoff artifact between ideation (Session N) and architecture (Session N+1) must be machine-readable and unambiguous to prevent hallucination.

**Format:** YAML-structured document with:
- **Locked decisions** — each decision has `locked: true` flag, rejected alternatives with reasons, and rationale
- **Explicit scope boundaries** — `in:` and `out:` arrays, no ambiguity
- **Quantified success criteria** — measurable targets, not aspirational prose
- **Constraints and NFRs** — structured fields, not narrative paragraphs
- **Source provenance** — back-reference to brainstorm document

**Design principle:** Every field is unambiguous. A fresh session reads the schema and cannot hallucinate a different interpretation. Rejected alternatives are explicit to close doors the brainstorm left open.

---

## Rationale

### Single Responsibility Alignment

Each skill maps to ONE professional role:

| Principle | Before | After |
|-----------|--------|-------|
| brainstorming = BA | ✅ Already clean | ✅ No change |
| ideation = PM + Architect | ❌ Two roles | ✅ PM only |
| orchestration = Coordinator + Architect | ❌ Two roles | ✅ Coordinator only |
| architecture = Context files only | ⚠️ Underutilized | ✅ Full Architect role |

### Token Efficiency

- Ideation skill shrinks from ~13,345 → ~10,410 reference lines
- Orchestration skill shrinks by ~3,770 lines (Phase 4A removed)
- Architecture skill grows by ~6,870 lines but gains meaningful work (epic creation + context files)
- Progressive disclosure still applies — reference files loaded on demand
- Net effect: no token increase (content moves, doesn't duplicate)

### Conformance Analysis Resolution

- Addresses Finding 3.3 (skill scope concern) from EPIC-067 conformance analysis
- Reduces ideation reference file count from 28 → ~22
- Makes each skill more focused and easier to conform to Anthropic best practices

---

## Constitutional Files Affected

This ADR authorizes changes to the following LOCKED files:

### 1. `devforgeai/specs/context/architecture-constraints.md`
- **Lines 28-34:** Update skill responsibility examples to reflect new boundaries
- Add architecture skill's epic decomposition responsibility

### 2. `devforgeai/specs/context/source-tree.md`
- **Lines 28-52:** Update `devforgeai-ideation/references/` listing (remove transferred files)
- **Lines 58-66:** Update `devforgeai-architecture/references/` listing (add transferred files)
- Update directory names when renames occur (per ADR-017)

### 3. `devforgeai/specs/context/coding-standards.md`
- No structural changes needed (ADR-017 already updated naming convention)
- Documentation section order may need update for new architecture phases

---

## Consequences

### Positive
- Clean single-responsibility per skill (BA / PM / Architect)
- Reduced ideation skill complexity (~2,935 lines removed)
- Architecture skill becomes a meaningful "architect" role instead of just context file generator
- Cleaner handoff chain with explicit outputs at each stage
- Easier to maintain, test, and conform each skill independently

### Negative
- One-time migration effort to move reference files and update SKILL.md phases
- `/ideate` and `/create-epic` command handoff logic needs updating
- Existing brainstorm → epic workflows may need re-testing
- Transition period where documentation references old structure

### Risks
- **Broken handoff:** Ideation output format must match architecture input expectations → Mitigated by defining explicit handoff contract (requirements.md schema)
- **Missing references:** Moved files referenced by ideation SKILL.md → Mitigated by post-move grep scan
- **User confusion:** `/ideate` no longer produces epics directly → Mitigated by clear command output messaging ("Requirements complete. Run /create-epic to generate epic.")

---

## Implementation Sequence

1. **Phase 1:** Move reference files from ideation → architecture (no renames yet)
2. **Phase 2:** Update both SKILL.md files (remove/add phases)
3. **Phase 3:** Update `/ideate` and `/create-epic` commands for new handoff
4. **Phase 4:** Rename skills per ADR-017 (architecture → `designing-systems`, ideation → TBD after slimming)
5. **Phase 5:** Update context files (source-tree.md, architecture-constraints.md)
6. **Phase 6:** Full codebase sweep for stale references

---

## References

- ADR-017: Skill Gerund Naming Convention (rename authorization)
- EPIC-067: Ideation Anthropic Conformance Remediation (Finding 3.3)
- architecture-constraints.md: Single Responsibility Principle (lines 28-34)
- Conformance Analysis: `devforgeai/specs/analysis/ideation-anthropic-conformance-analysis.md`
