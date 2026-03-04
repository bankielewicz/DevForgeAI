# Custody Chain Audit: stories-554-558

**Audit Date:** 2026-03-03 (regenerated with --force)
**Scope:** range - STORY-554..STORY-558
**Stories Validated:** 5
**Epic:** EPIC-078 (Operations & Launch)
**Previous Audit:** 2026-03-03 (6 findings, 5 applied) — superseded by this regeneration

---

## 1. Document Inventory

| Layer | Document | Path | Exists |
|-------|----------|------|--------|
| brainstorms | BRAINSTORM-011 | `devforgeai/specs/brainstorms/BRAINSTORM-011-business-skills-framework.brainstorm.md` | ✅ |
| requirements | *(referenced)* | `devforgeai/specs/requirements/business-skills-framework-requirements.md` | ❌ MISSING |
| epics | EPIC-078 | `devforgeai/specs/Epics/EPIC-078-operations-launch.epic.md` | ✅ |
| sprints | Sprint-28 | `devforgeai/specs/Sprints/Sprint-28.md` | ✅ |
| stories | STORY-554 | `devforgeai/specs/Stories/STORY-554-mvp-launch-checklist.story.md` | ✅ |
| stories | STORY-555 | `devforgeai/specs/Stories/STORY-555-tool-selection-guide.story.md` | ✅ |
| stories | STORY-556 | `devforgeai/specs/Stories/STORY-556-ops-plan-command-skill-assembly.story.md` | ✅ |
| stories | STORY-557 | `devforgeai/specs/Stories/STORY-557-process-design-framework.story.md` | ✅ |
| stories | STORY-558 | `devforgeai/specs/Stories/STORY-558-scaling-readiness-assessment.story.md` | ✅ |
| adrs | ADR-017 | `devforgeai/specs/adrs/ADR-017-skill-gerund-naming-no-prefix.md` | ✅ |

---

## 2. Context Validation Results

| Story ID | Status | CRITICAL | HIGH | MEDIUM | LOW |
|----------|--------|----------|------|--------|-----|
| STORY-554 | FAILED | 1 | 0 | 0 | 0 |
| STORY-555 | FAILED | 1 | 0 | 0 | 0 |
| STORY-556 | FAILED | 1 | 0 | 0 | 0 |
| STORY-557 | FAILED | 1 | 0 | 0 | 0 |
| STORY-558 | FAILED | 1 | 0 | 0 | 0 |

**Compliance Rate:** 0/5 (0%)

**Notes:**
- All 6 context files loaded successfully (tech-stack ✅, source-tree ✅, dependencies ✅, coding-standards ✅, architecture-constraints ✅, anti-patterns ✅)
- No technology violations (all stories are Markdown-only, no new packages)
- No dependency violations
- No anti-pattern violations
- **Single systemic violation** across all 5 stories: source-tree path registration

---

## 3. Provenance Map

```
BRAINSTORM-011 (business-skills-framework)
  ├── [MISSING] requirements/business-skills-framework-requirements.md
  └── EPIC-078 (Operations & Launch)
        ├── Sprint-28 (all 5 stories assigned)
        ├── STORY-554 (Feature 1: MVP Launch Checklist, 3pts)
        ├── STORY-555 (Feature 2: Tool Selection Guide, 2pts)
        ├── STORY-556 (Feature 3: /ops-plan Command, 2pts)
        │     ├── depends_on: STORY-554 ✅
        │     └── depends_on: STORY-555 ✅
        ├── STORY-557 (Feature 4: Process Design Framework, 2pts)
        └── STORY-558 (Feature 5: Scaling Readiness Assessment, 1pt)
```

**Provenance Chain Status:**
- BRAINSTORM-011 → EPIC-078: ✅ Linked via `source_brainstorm` field
- EPIC-078 → Requirements: ❌ **BROKEN** — `source_requirements` references a file that does not exist
- EPIC-078 → Stories: ✅ All 5 stories correctly reference `epic: EPIC-078`
- Stories → Sprint: ✅ All 5 stories reference `sprint: Sprint-28`
- Story provenance XML: ✅ All 5 stories have `<provenance>` blocks with quotes and line references

**Dependency Graph:**
- STORY-556 depends on [STORY-554, STORY-555] — both exist and are in same sprint ✅
- STORY-554, STORY-555, STORY-557, STORY-558 have no blocking dependencies ✅
- No circular dependencies detected ✅

---

## 4. Findings

### F-001 (CRITICAL) — Development Paths Not in source-tree.md

| Field | Value |
|-------|-------|
| **Severity** | CRITICAL |
| **Type** | context/source-tree-violation |
| **Affected** | STORY-554, STORY-555, STORY-556, STORY-557, STORY-558 |
| **Summary** | `src/claude/skills/operating-business/` and `src/claude/commands/ops-plan.md` are NOT documented in source-tree.md. All 5 stories reference these development paths but they do not appear in the canonical directory structure. |
| **Evidence** | `Grep(pattern="operating-business\|ops-plan", path="devforgeai/specs/context/source-tree.md")` returns **no matches**. Source-tree v4.6 header mentions "devforgeai/specs/business/operations/" (output directory) but omits the skill/command development paths. |
| **Remediation** | Create ADR to update source-tree.md adding: `src/claude/skills/operating-business/SKILL.md`, `src/claude/skills/operating-business/references/` (with 4 reference files: mvp-launch-checklist.md, tool-selection-guide.md, process-design-framework.md, scaling-readiness-assessment.md), and `src/claude/commands/ops-plan.md` |
| **Verification** | `Grep(pattern="operating-business", path="devforgeai/specs/context/source-tree.md")` returns matches in directory tree |
| **Blocks** | All 5 stories — cannot create files outside documented source tree per HALT trigger |

---

### F-002 (HIGH) — Broken Provenance: Requirements File Missing

| Field | Value |
|-------|-------|
| **Severity** | HIGH |
| **Type** | provenance/missing-document |
| **Affected** | EPIC-078 (and transitively all 5 stories) |
| **Summary** | EPIC-078 frontmatter declares `source_requirements: devforgeai/specs/requirements/business-skills-framework-requirements.md` but this file does not exist |
| **Evidence** | `Glob(pattern="devforgeai/specs/requirements/*business*")` returns no files |
| **Remediation** | Option A: Generate requirements document from BRAINSTORM-011 via `/ideate`. Option B: Remove `source_requirements` from EPIC-078 frontmatter if requirements were embedded directly in the epic. Use AskUserQuestion to decide. |
| **Verification** | Either file exists at referenced path, or `source_requirements` field removed from EPIC-078 |

---

### F-003 (MEDIUM) — EPIC-078 Stories Table Status Mismatch

| Field | Value |
|-------|-------|
| **Severity** | MEDIUM |
| **Type** | quality/status-mismatch |
| **Affected** | EPIC-078 |
| **Summary** | EPIC-078 Stories table (lines 261-265) lists all 5 stories as "Backlog" but all story files have `status: Ready for Dev` in frontmatter |
| **Evidence** | EPIC-078 line 261: `STORY-554 ... Backlog` vs STORY-554 frontmatter line 7: `status: Ready for Dev` |
| **Remediation** | Update EPIC-078 Stories table status column to "Ready for Dev" for all 5 stories |
| **Verification** | `Grep(pattern="Backlog", path="devforgeai/specs/Epics/EPIC-078-operations-launch.epic.md")` returns 0 matches in Stories table |

---

### F-004 (MEDIUM) — EPIC-078 plan_file Uses Absolute Path

| Field | Value |
|-------|-------|
| **Severity** | MEDIUM |
| **Type** | quality/hardcoded-path |
| **Affected** | EPIC-078 |
| **Summary** | `plan_file: /home/bryan/.claude/plans/jiggly-launching-backus.md` uses an absolute system path. Per anti-patterns.md Category 10 (Hardcoded Paths, SEVERITY: MEDIUM), absolute paths are forbidden. |
| **Evidence** | EPIC-078 frontmatter line 16 |
| **Remediation** | Change to relative path `.claude/plans/jiggly-launching-backus.md` or remove field if plan file is session-specific and not needed for provenance |
| **Verification** | `plan_file` value does not start with `/` |

---

### F-005 (LOW) — STORY-554 Provenance Line Reference Imprecise

| Field | Value |
|-------|-------|
| **Severity** | LOW |
| **Type** | quality/provenance-precision |
| **Affected** | STORY-554 |
| **Summary** | Provenance `<line_reference>EPIC-078, line 22</line_reference>` points to the Business Goal narrative paragraph, not to the specific Feature 1 definition (lines 43-48). Other stories (555-558) use feature-specific line references. |
| **Remediation** | Update to `<line_reference>lines 43-48</line_reference>` to match Feature 1 scope section |
| **Verification** | Line reference points to Feature 1 section in EPIC-078 |

---

## 5. Cross-Cutting Issues

### Issue A: Source-Tree Gap Blocks All Stories

F-001 is a systemic blocker. The previous audit (same date) identified output path gaps (`devforgeai/specs/business/operations/`) and marked them as fixed via source-tree v4.6. However, the **development paths** (`src/claude/skills/operating-business/`, `src/claude/commands/ops-plan.md`) were NOT added. This means:
- The output directory is documented ✅
- The skill/command development directories are NOT documented ❌
- All 5 stories will trigger HALT during `/dev` Phase 01 preflight when creating files under `src/claude/skills/operating-business/`

**Resolution requires:** An ADR to update source-tree.md with the new skill and command paths.

### Issue B: Requirements Document Gap in Provenance Chain

EPIC-078 references a requirements document that was never created. This suggests the brainstorm-to-epic pipeline for business skills may have used a shortcut (embedding requirements directly in the epic). While the epic is detailed enough to serve as a requirements source, the dangling `source_requirements` reference creates a broken provenance link.

### Issue C: Previous Audit Partial Fix

The previous audit's F-001 fix (adding `devforgeai/specs/business/operations/` to source-tree) was correct but incomplete — it addressed output paths but not development paths. This `--force` regeneration catches the remaining gap.

---

## 6. Summary Statistics

| Metric | Count |
|--------|-------|
| Stories validated | 5 |
| Stories compliant | 0 |
| Stories failed | 5 |
| Total findings | 5 |
| CRITICAL | 1 |
| HIGH | 1 |
| MEDIUM | 2 |
| LOW | 1 |

---

## 7. Remediation Priority Order

1. **F-001** (CRITICAL) — Add `src/claude/skills/operating-business/` and `src/claude/commands/ops-plan.md` to source-tree.md (requires ADR)
2. **F-002** (HIGH) — Resolve dangling `source_requirements` reference in EPIC-078
3. **F-003** (MEDIUM) — Update EPIC-078 Stories table status from "Backlog" to "Ready for Dev"
4. **F-004** (MEDIUM) — Fix absolute path in EPIC-078 `plan_file` frontmatter
5. **F-005** (LOW) — Improve STORY-554 provenance line reference precision

---

## 8. Session Handoff Instructions

**For future Claude sessions reading this document:**

1. This document is self-contained. You do not need the original conversation.
2. Check current state before remediating — prior sessions may have fixed some items.
3. Use the verification step in each finding to confirm fixes were applied.
4. File paths are relative to project root.
5. For CRITICAL findings: these block story implementation. Prioritize them.
6. **F-001 is the top priority** — it blocks ALL 5 stories from `/dev` execution. Create an ADR to update source-tree.md with the operating-business skill directory and ops-plan command.
7. For F-002: Use AskUserQuestion to determine whether to create the requirements file or remove the dangling reference.
8. For F-003 and F-004: These are quick fixes that can be batched in one edit session.
