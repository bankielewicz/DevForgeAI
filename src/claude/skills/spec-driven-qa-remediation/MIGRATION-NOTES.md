# Migration Notes: devforgeai-qa-remediation -> spec-driven-qa-remediation

**Migration Date:** 2026-03-18
**Source Skill:** `src/claude/skills/devforgeai-qa-remediation/` (860 lines, 7 phases)
**Target Skill:** `src/claude/skills/spec-driven-qa-remediation/` (7 phases, Execute-Verify-Gate)
**Precedent:** spec-driven-release migration (ADR-039 pattern)
**Skill Inventory Row:** #16

---

## Why This Migration

The `devforgeai-qa-remediation` skill suffered from **token optimization bias** — Claude would skip phases/steps because it rationalized them as "simple" or "already covered." The spec-driven pattern prevents this with four independent anti-skip layers:

1. Fresh-context subagent execution
2. Binary CLI gates (devforgeai-validate)
3. Hook enforcement (shell scripts)
4. Step registry + artifact verification

This is the 10th skill family to be migrated to the spec-driven pattern.

---

## Phase Mapping (7 -> 7, no consolidation)

| New Phase | Name | Old Phase | Steps |
|-----------|------|-----------|-------|
| 01 | Pre-Flight Validation | Phase 01 + Flag Dependency Validation | 6 EVR |
| 02 | Discovery & Parsing | Phase 02 | 5 EVR |
| 03 | Aggregation & Prioritization | Phase 03 + Blocking-Only Filter | 6 EVR |
| 04 | Interactive Selection | Phase 04 | 4 EVR |
| 05 | Batch Story Creation | Phase 05 + Auto Mode | 7 EVR |
| 06 | Source Report Update | Phase 06 | 4 EVR |
| 07 | Technical Debt Integration | Phase 07 + Auto Mode | 8 EVR |

**Total:** 40 Execute-Verify-Record steps across 7 phases.

---

## Self-Sufficiency

All runtime dependencies are local to the new skill directory:

| Category | Count | Location |
|----------|-------|----------|
| Reference files | 5 | `references/` |
| Template files | 2 | `assets/templates/` |
| Phase files | 7 | `phases/` |
| Core | 2 | `SKILL.md`, `MIGRATION-NOTES.md` |
| **Total** | **16** | All under `spec-driven-qa-remediation/` |

**Zero cross-references to devforgeai-qa-remediation** — verified via Grep sweep.

---

## Key Structural Changes

1. **Execute-Verify-Record triplets** for every step (40 total)
2. **Binary CLI gates** (`devforgeai-validate --workflow=qa-remediation`) at entry/exit of every phase
3. **Phase files** separated into `phases/phase-XX-*.md` (7 files, was 2)
4. **Checkpoint persistence** at `devforgeai/workflows/checkpoints/qa-remediation-${SESSION_ID}.checkpoint.json`
5. **Self-check violation checklist** (8 items for token optimization bias detection)
6. **Anti-Skip Enforcement Contract** (4 independent layers)
7. **Resume detection** with checkpoint-based state recovery
8. **YAML frontmatter** with `model: claude-opus-4-6` and `effort: High`

---

## Unchanged Components

| Component | Status |
|-----------|--------|
| `/review-qa-reports` command | Updated to invoke `spec-driven-qa-remediation` (was `devforgeai-qa-remediation`) |
| `devforgeai/config/qa-remediation.yaml` | UNCHANGED — same config file |
| Gap file format (JSON) | UNCHANGED — same schema |
| Enhancement report format | UNCHANGED — same template |
| Technical debt register format | UNCHANGED — same entry format |
| `spec-driven-stories` batch mode | UNCHANGED — same invocation |

---

## Archive Plan

After validation:

1. Add HALT directive to archived `src/claude/skills/devforgeai-qa-remediation/SKILL.md`
2. Rename directory to `src/claude/skills/_devforgeai-qa-remediation.archive/`
3. Update `tmp/skill-inventory.md` row #16

---

## Migrated Files

### From old skill -> New skill

| Source | Target | Changes |
|--------|--------|---------|
| `SKILL.md` | `SKILL.md` | Complete rewrite with 10 structural elements |
| `phases/phase-01-preflight.md` | `phases/phase-01-preflight.md` | Converted to EVR format |
| `phases/phase-05-batch-creation.md` | `phases/phase-05-batch-story-creation.md` | Converted to EVR format |
| (inline in SKILL.md) | `phases/phase-02-discovery-parsing.md` | NEW: Extracted from SKILL.md |
| (inline in SKILL.md) | `phases/phase-03-aggregation-prioritization.md` | NEW: Extracted from SKILL.md |
| (inline in SKILL.md) | `phases/phase-04-interactive-selection.md` | NEW: Extracted from SKILL.md |
| (inline in SKILL.md) | `phases/phase-06-source-report-update.md` | NEW: Extracted from SKILL.md |
| (inline in SKILL.md) | `phases/phase-07-technical-debt-integration.md` | NEW: Extracted from SKILL.md |
| `references/*.md` (5 files) | `references/*.md` (5 files) | Updated header references |
| `assets/templates/*.md` (1 file) | `assets/templates/*.md` (1 file) | Updated footer attribution |
| `assets/templates/*.yaml` (1 file) | `assets/templates/*.yaml` (1 file) | No changes |

### New files (not in old skill)

| File | Purpose |
|------|---------|
| `MIGRATION-NOTES.md` | This file — migration documentation |

---

## Command Backup

Original command backed up to: `src/claude/commands/backup/review-qa-reports.md`

Contains the original `/review-qa-reports` command that invoked `devforgeai-qa-remediation`.
