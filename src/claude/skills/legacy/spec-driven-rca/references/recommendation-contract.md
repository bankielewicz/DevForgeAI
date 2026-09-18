# Recommendation Contract — Tiered Field Specification

**Status:** Authoritative (ADR-074)
**Last updated:** 2026-05-20
**Consumers MUST cite this file** when documenting how they ingest /rca recommendations.

This file is the single source of truth for the shape of each recommendation record emitted by `spec-driven-rca` Phase 05 and consumed by `github-incident-from-rca` and `create-stories-from-rca`. The emit format itself lives in `../assets/recommendation-template.md`; this file specifies which fields downstream consumers MUST ingest, MUST render, and MAY summarize.

---

## Tier Summary

| Tier | Cardinality | Consumer obligation |
|---|---|---|
| **Required** | 6 fields | MUST ingest. MUST render verbatim into the consumer's output artifact. |
| **Rendered** | 5 fields | MUST render into the consumer's output artifact. Rendering format is consumer-specific (table, bullet list, prose) but the field's content MUST appear. |
| **Context** | 2 fields | MAY summarize. MAY quote verbatim. MAY omit if obviously inapplicable (e.g. `current_code_context` for a documentation-only recommendation that emitted "N/A"). |

A consumer that fails to ingest a Required field, or fails to render a Rendered field, is in violation of this contract. The `pre-rca-recommendation-write.sh` hook enforces emit-side compliance preventatively.

---

## Required Tier (6 fields)

### `id`
- **Emit format:** `**Recommendation ID:** REC-{N}` (header line)
- **Type:** string matching `^REC-\d+$`
- **Consumer obligation:** MUST preserve verbatim. Used as cross-reference in `source_recommendation` (story) and issue title prefix (incident).

### `title`
- **Emit format:** `**Title:** {Brief descriptive title}` (header line)
- **Type:** string, verb-first imperative recommended (e.g., "Add input validation to ...")
- **Consumer obligation:** MUST render. Used as `feature_name` (story) and issue title (incident).

### `priority`
- **Emit format:** `**Priority:** {CRITICAL | HIGH | MEDIUM | LOW}` (header line)
- **Type:** enum: CRITICAL, HIGH, MEDIUM, LOW
- **Consumer obligation:** MUST ingest. Mapped per-consumer (CRITICAL→High for stories; CRITICAL→`priority:critical` label for incidents).

### `description`
- **Emit format:** the `### Problem Addressed` section body
- **Type:** free-form markdown paragraph
- **Consumer obligation:** MUST render verbatim into the consumer's body. Truncation is FORBIDDEN.

### `addresses_why` *(load-bearing 5-Whys traceability)*
- **Emit format:** `**Addresses:** Why #{N} — "{exact quoted text from 5 Whys answer}"` (line under `### Evidence Traceability [MANDATORY]`)
- **Type:** structured string: `Why #{N} — "{quoted answer}"`
- **Consumer obligation:** MUST render verbatim. For stories, render into the Provenance section. For incidents, render under the **Context** section of the issue body. This field carries the traceability chain from the RCA's 5-Whys analysis into the downstream artifact — without it the artifact is rootless.

### `evidence_files` *(load-bearing 5-Whys traceability)*
- **Emit format:** `**Evidence Files:** {comma-separated list of evidence file paths supporting this recommendation}` (line under `### Evidence Traceability [MANDATORY]`)
- **Type:** comma-separated list of relative paths
- **Consumer obligation:** MUST render verbatim. For stories, append to Provenance section as a bulleted file list. For incidents, render under the **Files to change** or **Context** section. Like `addresses_why`, this field is the evidence anchor — without it the recommendation is unprovenanced.

---

## Rendered Tier (5 fields)

### `test_specification`
- **Emit format:** the `### Test Specification [MANDATORY]` section (markdown table with Test Name / Input / Expected Output columns)
- **Type:** structured markdown table
- **Consumer obligation:** MUST render into the consumer's body. For stories, render into the Test Strategy section. For incidents, render into the **Test plan** section verbatim.

### `success_criteria`
- **Emit format:** the `### Success Criteria` section (markdown checkbox list)
- **Type:** markdown checklist
- **Consumer obligation:** MUST render into the consumer's body. For incidents, render into the **Acceptance criteria** section. For stories, render into the story's AC list.

### `effort_hours`
- **Emit format:** `**Time:** {N} hours` (line under `### Effort Estimate`)
- **Type:** integer
- **Consumer obligation:** MUST be available for rendering. Incidents render as effort estimate; stories use it to compute or validate `effort_points`.

### `effort_points`
- **Emit format:** `**Story Points:** {N}` (line under `### Effort Estimate`; calculated as ~hours/4)
- **Type:** integer
- **Consumer obligation:** Stories MUST use this value as story points (default 5 only if absent). Incidents MAY surface in body.

### `conditional`
- **Emit format:** `**Type:** {Unconditional | Conditional}` and (if Conditional) `**Condition:** {trigger}` (lines under `### Conditional vs Unconditional [MANDATORY]`)
- **Type:** struct: { type: enum, condition?: string }
- **Consumer obligation:** Conditional recommendations MUST surface the condition. Stories: render into Dependencies section. Incidents: render into the **Context** or **Dependencies** section. An unconditional recommendation surfaces as such.

---

## Context Tier (2 fields)

### `current_code_context`
- **Emit format:** the `### Current Code Context [MANDATORY for code changes]` section (file path + line range + verbatim code block)
- **Type:** structured (file, lines, language, code block)
- **Consumer obligation:** MAY summarize ("Modifies {file} lines {N}-{M}"). MAY quote verbatim. Documentation-only recommendations emit "N/A" — consumers MAY omit.

### `architecture_constraints`
- **Emit format:** the `### Architecture Constraints [MANDATORY for .rs file changes]` section (bullet list with `(Source: {file}, lines {N}-{M})` citations)
- **Type:** bullet list with citations
- **Consumer obligation:** MAY summarize. MAY quote verbatim. Non-Rust recommendations emit "N/A" — consumers MAY omit.

---

## Worked Example

A Phase 05 recommendation that fixes a missing input validation, traced to Why #3 of an RCA:

```markdown
**Recommendation ID:** REC-2
**Title:** Add path-prefix validation to MigrationConfig::from_file
**Priority:** HIGH

### Evidence Traceability [MANDATORY]
**Addresses:** Why #3 — "MigrationConfig accepted absolute paths without validation"
**Evidence Files:** src/migration/config.rs, tests/integration/migration_test.rs

### Conditional vs Unconditional [MANDATORY]
**Type:** Unconditional
**Condition:** Always implement — no trigger condition

### Problem Addressed
The MigrationConfig::from_file constructor does not enforce that supplied paths
are project-relative, allowing absolute-path injection that bypasses sandbox checks.

### Current Code Context [MANDATORY for code changes]
**File:** `src/migration/config.rs`
**Lines:** 42-58
**Language:** rust
```rust
impl MigrationConfig {
    pub fn from_file(path: &Path) -> Result<Self> {
        let raw = std::fs::read_to_string(path)?;
        ...
    }
}
```

[... rest of template fields populated ...]
```

### Consumer rendering matrix

| Consumer | Required tier | Rendered tier | Context tier |
|---|---|---|---|
| **github-incident-from-rca** | Issue title gets `id` + `title`; **Context** section gets `addresses_why` + `evidence_files`; body gets `description`, `priority` (as label) | **Test plan** ← `test_specification`; **Acceptance criteria** ← `success_criteria`; **Context** mentions `effort_hours` + `conditional` | MAY summarize `current_code_context` into **Files to change** section; MAY summarize `architecture_constraints` into **Context** |
| **create-stories-from-rca** | `feature_name` ← `title`; `feature_description` ← `description`; `source_recommendation` ← `id`; Provenance section ← `addresses_why` + `evidence_files` | Test Strategy ← `test_specification`; AC list ← `success_criteria`; story points ← `effort_points`; Dependencies ← `conditional` | MAY summarize into story Technical Specification section |

---

## Schema Versioning

This contract is v1.0 as of ADR-074. Future schema changes require:

1. A new ADR superseding ADR-074
2. A migration plan for both downstream consumers
3. A version stamp in this file's frontmatter

Field additions are non-breaking when they land in the Context tier. Required and Rendered tier changes are breaking.

---

## References

- **ADR:** `devforgeai/specs/adrs/ADR-074-rca-modernization.md`
- **Emit template:** `../assets/recommendation-template.md`
- **Phase 05 spec:** `../phases/phase-05-recommendation-generation.md`
- **Emit-side hook:** `.claude/hooks/pre-rca-recommendation-write.sh`
- **Consumer 1:** `.claude/skills/github-incident-from-rca/SKILL.md`
- **Consumer 2:** `.claude/commands/references/create-stories-from-rca/`
