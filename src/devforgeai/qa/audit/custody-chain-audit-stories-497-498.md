# Custody Chain Audit: stories-497-498

**Audit Date:** 2026-02-24
**Scope:** range - stories-497-498
**Stories Validated:** 2

---

## 1. Document Inventory

| Layer | Document | Path |
|-------|----------|------|
| stories | STORY-497 | `devforgeai/specs/Stories/STORY-497-release-skill-phase-markers.story.md` |
| stories | STORY-498 | `devforgeai/specs/Stories/STORY-498-release-library-crate-path.story.md` |
| rca | RCA-041 | `devforgeai/RCA/RCA-041-release-skill-phase-skip-violation.md` |

## 2. Context Validation Results

| Story ID | Status | CRITICAL | HIGH | MEDIUM | LOW |
|----------|--------|----------|------|--------|-----|
| STORY-497 | COMPLIANT (with findings) | 0 | 1 | 1 | 0 |
| STORY-498 | COMPLIANT (with findings) | 0 | 1 | 1 | 0 |

**Compliance Rate:** 2/2 (100% — no CRITICAL violations)

## 3. Provenance Chain

```
RCA-041 (Release Skill Phase Skip Violation)
  ├── REC-1 (CRITICAL) → STORY-497 (Phase Marker Protocol)
  └── REC-2 (HIGH)     → STORY-498 (Library Crate Adaptive Path)
                              └── depends_on: [STORY-497]
```

**Provenance Status:** ✅ COMPLETE — Both stories trace to RCA-041 via `source_rca` frontmatter field.

**Epic Assignment:** ⚠️ Both stories have `epic: null`. Consider assigning to an existing epic (e.g., EPIC-031 Phase Execution Enforcement or EPIC-084 Structured Diagnostic Capabilities) or creating a new epic.

**Sprint Assignment:** Both stories are in `Backlog` status with `sprint: Backlog`.

## 4. Findings

### F-001 (HIGH): Target file path case mismatch

**Affected:** STORY-497, STORY-498
**Type:** context/source-tree
**Detail:** Technical specification references `file_path: ".claude/skills/devforgeai-release/skill.md"` (lowercase `skill.md`) but the actual file is `SKILL.md` (uppercase). This could cause failures on case-sensitive filesystems.
**Remediation:** Update `file_path` in both stories' technical specifications from `skill.md` to `SKILL.md`.

### F-002 (MEDIUM): Epic not assigned

**Affected:** STORY-497, STORY-498
**Type:** chain/missing-epic
**Detail:** Both stories have `epic: null` in frontmatter. Stories originating from RCA recommendations should be linked to a relevant epic for traceability.
**Remediation:** Assign to an appropriate epic (EPIC-031 Phase Execution Enforcement is a strong candidate) or create a new epic for release skill hardening.

### F-003 (HIGH): Dependency chain — STORY-498 depends on STORY-497

**Affected:** STORY-498
**Type:** chain/dependency
**Detail:** STORY-498 `depends_on: ["STORY-497"]` — this is correctly declared. STORY-497 must reach "Dev Complete" before STORY-498 can begin.
**Status:** ✅ Correctly declared, no issue. Informational only.

### F-004 (MEDIUM): Skill naming convention (ADR-017)

**Affected:** STORY-497, STORY-498
**Type:** context/coding-standards
**Detail:** Both stories target `devforgeai-release` skill which uses the old `devforgeai-` prefix naming convention. Per ADR-017 and coding-standards.md, skills should use gerund naming (e.g., `releasing-stories`). This is a pre-existing condition, not introduced by these stories.
**Remediation:** None required — renaming the skill is out of scope for these stories. Note for future tracking.

## 5. Cross-Cutting Issues

- **Both stories share the same target file** (`.claude/skills/devforgeai-release/SKILL.md`). If developed in parallel, file overlap will occur. The dependency chain (STORY-498 depends on STORY-497) correctly prevents this.
- **RCA-041 REC-3** (expand halt trigger language) has no story yet. Consider creating STORY-499 for it.

## 6. Summary Statistics

| Metric | Count |
|--------|-------|
| Stories validated | 2 |
| Stories compliant | 2 |
| Stories failed | 0 |
| Total findings | 4 |
| CRITICAL | 0 |
| HIGH | 2 |
| MEDIUM | 2 |
| LOW | 0 |

## 7. Remediation Priority Order

1. **F-001** (HIGH) - Fix `skill.md` → `SKILL.md` case in both stories' technical specs
2. **F-002** (MEDIUM) - Assign epic to both stories
3. **F-004** (MEDIUM) - Informational only, no action needed

## 8. Session Handoff Instructions

**For future Claude sessions reading this document:**

1. This document is self-contained. You do not need the original conversation.
2. Check current state before remediating — prior sessions may have fixed some items.
3. Use the verification step in each finding to confirm fixes were applied.
4. File paths are relative to project root.
5. For CRITICAL findings: these block story implementation. Prioritize them.
6. For quick fixes (path corrections, label updates): batch these in one session.
7. For architectural decisions: use AskUserQuestion to confirm approach before changing.
