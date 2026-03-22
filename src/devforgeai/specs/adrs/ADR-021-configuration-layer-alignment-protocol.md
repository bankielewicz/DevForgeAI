# ADR-021: Configuration Layer Alignment Protocol (CLAP)

**Status:** Accepted
**Date:** 2026-02-23
**Epic:** EPIC-081
**Story:** STORY-472

---

## Context

DevForgeAI loads multiple configuration layers at session start (CLAUDE.md, system prompt, 6 context files, rules, ADRs), but no existing validator performs cross-layer configuration analysis. All existing validators check in ONE direction only:

| Existing Validator | What It Checks | What It CANNOT Check |
|--------------------|----------------|----------------------|
| `context-validator` | Source code vs context files | CLAUDE.md vs context files |
| `tech-stack-detector` | Project files vs tech-stack.md | System prompt vs tech-stack.md |
| `/validate-stories` | Story content vs context files | Context files vs each other |
| `context-preservation-validator` | Story provenance chain | ADR propagation to context files |

None reads CLAUDE.md, the system prompt, or rules against context files. None reads context files against each other. This validation gap was discovered during the ENH-CLAP-001 investigation on the GPUXtend project, where a manual 5-step reasoning process uncovered 5 HIGH-severity configuration gaps including direct contradictions between CLAUDE.md and anti-patterns.md.

## Decision

We adopt the **Configuration Layer Alignment Protocol (CLAP)** — a codified 5-step methodology for cross-layer configuration validation, implemented through four framework components:

### 1. The 5-Step CLAP Methodology

1. **Layer Identification** — Catalogue every configuration surface loaded at session start
2. **Layer Purpose & Authority Analysis** — Determine precedence for contradiction resolution
3. **Cross-Reference Validation** — Pairwise comparison across layers for contradiction detection
4. **Completeness Analysis** — Verify the orchestrator has enough context to delegate effectively
5. **Minimal Intervention Design** — Apply smallest change that closes all gaps

### 2. New `alignment-auditor` Subagent

A read-only subagent (model: haiku) that performs pairwise comparison across all configuration layers. Tools restricted to Read, Glob, Grep. Implements 15 validation checks (10 contradiction checks, 4 completeness checks, 1 ADR propagation check). Output is structured JSON with severity-based findings.

### 3. New `/audit-alignment` Command

A user-facing entry point for on-demand auditing with layer filtering (`--layer`) and fix proposals (`--fix`). Follows lean orchestration pattern. Invokes the alignment-auditor subagent via Task().

### 4. Phase 5.5 Integration into `designing-systems` Skill

Automatic alignment check after `/create-context` creates context files, before epic creation begins. Phase 5.5 ("Prompt Alignment") inserts between Phase 5 (Validate Spec Against Context) and Phase 6 (Epic Creation). HIGH-severity contradictions block progression.

### 5. Authorized source-tree.md Additions

This ADR authorizes adding the following 5 new files to source-tree.md:

1. `.claude/agents/alignment-auditor.md` — Subagent definition
2. `.claude/agents/alignment-auditor/references/validation-matrix.md` — 15 validation check definitions
3. `.claude/commands/audit-alignment.md` — On-demand audit command
4. `.claude/skills/designing-systems/references/prompt-alignment-workflow.md` — Phase 5.5 workflow reference
5. `.claude/skills/designing-systems/references/domain-reference-generation.md` — EPIC-082 downstream deliverable (same ENH-CLAP-001 origin)

## Rationale

**Why alignment-auditor is separate from context-validator (Single Responsibility Principle):**

The `context-validator` enforces constraints against code changes — it validates that implementation code complies with context files. The `alignment-auditor` verifies cross-layer referential consistency between framework configuration files — it validates that CLAUDE.md, system prompt, rules, and ADRs are consistent with context files and with each other.

| Dimension | context-validator | alignment-auditor |
|-----------|-------------------|-------------------|
| **Trigger** | Before git commit, during /dev | After /create-context, on-demand via /audit-alignment, after ADR acceptance |
| **Input** | Code changes + context files | CLAUDE.md + system prompt + context files + rules + ADRs |
| **Model** | opus (code analysis) | haiku (text comparison, cost-efficient) |
| **Direction** | Code → Context (one-way) | All layers ↔ All layers (pairwise) |
| **Output** | Pass/fail per violation | Structured JSON with contradictions, gaps, ADR drift |

Different trigger points, different input sets, different model requirements (haiku vs opus) — merging them would violate SRP and increase cost (opus for text comparison tasks that haiku handles efficiently).

## Consequences

### When CLAP Runs (Trigger Points)

1. **After `/create-context`** — Phase 5.5 runs automatically after context file creation
2. **On-demand via `/audit-alignment`** — User invokes when monitoring configuration drift
3. **After ADR acceptance** — Proactive trigger to verify ADR decisions propagated to context files

### Where CLAP Does NOT Run (Exclusions)

- **Not during `/dev`** — Too frequent; context-validator handles code compliance per-commit
- **Not during `/qa`** — QA validates implementation quality, not meta-configuration
- **Not during story creation** — Stories reference context files, already validated by /validate-stories

### Mutability Rules

CLAP never auto-modifies context files per Critical Rule #4 (context files are immutable without ADR authorization). The `--fix` flag on `/audit-alignment` proposes edits only for MUTABLE layers (CLAUDE.md, system prompt, rules) and requires explicit user approval via AskUserQuestion for every proposed change. Context file changes are flagged for ADR creation.

## References

- **ENH-CLAP-001:** Configuration Layer Alignment Protocol proposal (GPUXtend investigation)
- **Requirements Specification:** `devforgeai/specs/requirements/clap-configuration-layer-alignment-requirements.md`
- **EPIC-081:** Configuration Layer Alignment Protocol epic
- **ADR-020:** Structural Changes Authorization (format precedent)
- **ADR-012:** Progressive Disclosure (agent size limits, reference file pattern)
