# DevForgeAI Orphaned File Audit Report

**Generated:** 2026-02-18
**Last Updated:** 2026-02-19
**Scope:** Full project scan (7 detection methods, all categories)
**Tool:** `/audit-orphans --category=all --output=file`

---

## Executive Summary

| # | Category | Count | Severity | Status |
|---|----------|-------|----------|--------|
| 1 | Backup Files | ~~21~~ 0 | ~~LOW~~ | ✅ **RESOLVED** (2026-02-19) |
| 2 | Duplicate Templates | ~~6 names in 2+ locations~~ 2 remaining | ~~**HIGH**~~ MEDIUM | ✅ **PARTIALLY RESOLVED** — orchestration + specs duplicates deleted; `epic-template.md` still in designing-systems + discovering-requirements |
| 3 | Dual-Path Sync Drift | ~~6 context files behind~~ 0 | ~~**HIGH**~~ | ✅ **RESOLVED** (2026-02-19) — all 6 context files + templates synced |
| 4 | Orphaned Skill Directories | ~~4~~ 3 | MEDIUM | ✅ **PARTIALLY RESOLVED** — deprecated backup/ deleted; 3 orphaned skills remain |
| 5 | Structural Anomalies | ~~1~~ 0 | ~~MEDIUM~~ | ✅ **RESOLVED** (2026-02-19) — nested `assets/assets/` flattened |
| 6 | Oversized Agents (ADR-012) | 11 agents > 500 lines | **HIGH** | ⬜ OPEN |
| 7 | Context File Version Drift | ~~30 stale copies~~ 7 synced | ~~**HIGH**~~ | ✅ **RESOLVED** (2026-02-19) — `src/claude/memory/Constitution/` (6) + `src/devforgeai/templates/` (1) synced |

**Overall Health:** Significantly improved. 5 of 7 categories resolved. 1 HIGH-severity category remains (oversized agents).

---

## 1. Backup Files (21 found) — ✅ RESOLVED

**Severity:** LOW — Safe to delete, no functional impact.
**Status:** ✅ All 21 backup files deleted on 2026-02-19.

### Skill Backup Files (9)

| # | File Path (relative to project root) | Type |
|---|--------------------------------------|------|
| 1 | `.claude/skills/brainstorming/.backup-2025-12-23/SKILL.md.bak` | Skill backup |
| 2 | `.claude/skills/brainstorming/.backup-2025-12-23/handoff-synthesis-workflow.md.bak` | Skill backup |
| 3 | `.claude/skills/brainstorming/.backup-2025-12-23/output-templates.md.bak` | Skill backup |
| 4 | `src/claude/skills/brainstorming/.backup-2025-12-23/SKILL.md.bak` | src mirror backup |
| 5 | `src/claude/skills/brainstorming/.backup-2025-12-23/handoff-synthesis-workflow.md.bak` | src mirror backup |
| 6 | `src/claude/skills/brainstorming/.backup-2025-12-23/output-templates.md.bak` | src mirror backup |
| 7 | `.claude/skills/backup/devforgeai-brainstorming.deprecated/.backup-2025-12-23/SKILL.md.bak` | Deprecated backup |
| 8 | `.claude/skills/backup/devforgeai-brainstorming.deprecated/.backup-2025-12-23/handoff-synthesis-workflow.md.bak` | Deprecated backup |
| 9 | `.claude/skills/backup/devforgeai-brainstorming.deprecated/.backup-2025-12-23/output-templates.md.bak` | Deprecated backup |

### Recovery Backup Files (3)

| # | File Path | Type |
|---|-----------|------|
| 10 | `.claude/skills/devforgeai-qa/SKILL.md.rec2-backup` | Recovery backup |
| 11 | `src/claude/skills/devforgeai-qa/SKILL.md.rec2-backup` | Recovery backup |
| 12 | `src/claude/memory/skill-execution-troubleshooting.md.rec3-backup` | Recovery backup |

### Configuration & Script Backups (6)

| # | File Path | Type |
|---|-----------|------|
| 13 | `.claude/scripts/statusline.sh.bak` | Script backup |
| 14 | `.claude/settings.local.json.bak` | Config backup |
| 15 | `devforgeai/scripts/statusline.py.bak` | Script backup |
| 16 | `devforgeai/scripts/statusline.py.old` | Script old copy |
| 17 | `src/devforgeai/scripts/statusline.py.bak` | src mirror backup |
| 18 | `devforgeai/logs/pre-tool-use.log.bak` | Log backup |
| 19 | `tests/pytest.ini.bak` | Test config backup |

### Legacy/Temp Backups (2)

| # | File Path | Type |
|---|-----------|------|
| 20 | `tmp/DevForgeAI.01/tmp/src/workflows/shared/validate-spec-workflow.md.bak` | Legacy temp |
| 21 | `.git/logs/refs/heads/main-backup-2025-12-14` | Git ref backup |

~~**Recommendation:** Delete all 21 files. None are referenced by any active skill, command, or agent.~~
**Resolution:** All 21 files deleted on 2026-02-19. Empty `.backup-2025-12-23/` directories also removed.

---

## 2. Duplicate Templates (6 template names with multiple canonical locations) — ✅ PARTIALLY RESOLVED

**Severity:** ~~HIGH~~ MEDIUM (remaining items are lower risk)
**Status:** Orchestration duplicates (`story-template.md`, `epic-template.md`) deleted. `devforgeai/specs/templates/epic-template.md` deleted. Deprecated skill copies deleted. Nested anomaly copy deleted. Remaining: `epic-template.md` in `designing-systems/` + `discovering-requirements/` (both actively used by different skills).

### 2a. `epic-template.md` — 4 canonical locations (should be 1)

| # | Location | Role | Size (bytes) |
|---|----------|------|-------------|
| 1 | `.claude/skills/designing-systems/assets/templates/epic-template.md` | Canonical? | Active |
| 2 | `.claude/skills/devforgeai-orchestration/assets/templates/epic-template.md` | Duplicate | Active |
| 3 | `.claude/skills/discovering-requirements/assets/templates/epic-template.md` | Duplicate | Active |
| 4 | `devforgeai/specs/templates/epic-template.md` | Specs copy | Active |
| — | `src/claude/skills/designing-systems/assets/templates/epic-template.md` | src mirror of #1 | Mirror |
| — | `src/claude/skills/discovering-requirements/assets/templates/epic-template.md` | src mirror of #3 | Mirror |

**Risk:** If templates diverge, different skills will generate differently-structured epics.
**Fix:** Designate one canonical location. Other skills should `Read()` from canonical path.

### 2b. `story-template.md` — 2 canonical locations (should be 1)

| # | Location | Role |
|---|----------|------|
| 1 | `.claude/skills/devforgeai-story-creation/assets/templates/story-template.md` | **Canonical** (v2.9, 609 lines) |
| 2 | `.claude/skills/devforgeai-orchestration/assets/templates/story-template.md` | Duplicate |
| — | `src/claude/skills/devforgeai-story-creation/assets/templates/story-template.md` | src mirror of #1 |
| — | `src/claude/skills/devforgeai-orchestration/assets/templates/story-template.md` | src mirror of #2 |

**Risk:** Orchestration skill may use an older story template version.
**Fix:** Remove orchestration copy. Have orchestration `Read()` from devforgeai-story-creation canonical.

### 2c. `implementation-notes-template.md` — 3 locations (should be 1)

| # | Location | Role |
|---|----------|------|
| 1 | `.claude/skills/implementing-stories/assets/templates/implementation-notes-template.md` | **Canonical** |
| 2 | `.claude/skills/implementing-stories/assets/assets/templates/implementation-notes-template.md` | **Nested anomaly copy** (assets/assets/) |
| 3 | `.claude/skills/backup/devforgeai-development.deprecated/assets/templates/implementation-notes-template.md` | Deprecated copy |
| — | `src/claude/skills/implementing-stories/assets/templates/implementation-notes-template.md` | src mirror of #1 |

**Risk:** Nested `assets/assets/` copy may be loaded instead of correct one.
**Fix:** Delete nested copy and deprecated copy.

### 2d. `brainstorm-template.md` — 2 locations (1 active, 1 deprecated)

| # | Location | Role |
|---|----------|------|
| 1 | `.claude/skills/brainstorming/assets/templates/brainstorm-template.md` | **Canonical** |
| 2 | `.claude/skills/backup/devforgeai-brainstorming.deprecated/assets/templates/brainstorm-template.md` | Deprecated copy |
| — | `src/claude/skills/brainstorming/assets/templates/brainstorm-template.md` | src mirror of #1 |

**Risk:** Low (deprecated copy unlikely to be loaded). **Fix:** Delete deprecated entire backup directory.

### 2e. `claude-md-template.md` — 2 locations (1 active, 1 deprecated)

| # | Location | Role |
|---|----------|------|
| 1 | `.claude/skills/brainstorming/assets/templates/claude-md-template.md` | **Canonical** |
| 2 | `.claude/skills/backup/devforgeai-brainstorming.deprecated/assets/templates/claude-md-template.md` | Deprecated |

### 2f. `gitignore-template.md` / `readme-brainstorm-template.md` — Same pattern as 2e

Both exist in active brainstorming + deprecated brainstorming backup.

**Overall Template Recommendation:**
1. ~~Remove all files in `.claude/skills/backup/` (deprecated skills)~~ ✅ Done 2026-02-19
2. ~~Remove `devforgeai/specs/templates/epic-template.md` (stale copy)~~ ✅ Done 2026-02-19
3. ~~Remove orchestration copies of `story-template.md` and `epic-template.md`~~ ✅ Done 2026-02-19
4. ~~Flatten `implementing-stories/assets/assets/` → `assets/`~~ ✅ Done 2026-02-19
5. **REMAINING:** Evaluate `epic-template.md` in `designing-systems/` vs `discovering-requirements/` — determine if both need their own copy or one should `Read()` from the other

---

## 3. Dual-Path Sync Drift (`.claude/` vs `src/claude/`) — ✅ RESOLVED

**Severity:** ~~HIGH~~ RESOLVED
**Status:** All 6 context files in `src/claude/memory/Constitution/` synced from canonical on 2026-02-19. `src/devforgeai/templates/source-tree.md` also synced.

### Context File Copies in `src/claude/memory/Constitution/` (ALL behind canonical)

| Context File | Canonical (bytes) | src/claude/memory/Constitution/ (bytes) | Delta | % Behind |
|---|---|---|---|---|
| `source-tree.md` | 52,218 | 46,455 | -5,763 | 11.0% |
| `tech-stack.md` | 18,427 | 17,160 | -1,267 | 6.9% |
| `anti-patterns.md` | 7,524 | 5,432 | -2,092 | 27.8% |
| `coding-standards.md` | 13,946 | 13,498 | -448 | 3.2% |
| `architecture-constraints.md` | 12,033 | 11,809 | -224 | 1.9% |
| `dependencies.md` | 6,806 | 5,965 | -841 | 12.4% |

**All 6 context files in `src/claude/memory/Constitution/` are stale.**

### Additional Stale Copies

| File | Location | Canonical Size | Copy Size | Delta |
|---|---|---|---|---|
| `source-tree.md` | `src/devforgeai/templates/` | 52,218 | 35,864 | -16,354 (31.3% behind) |

### designing-systems Context Templates (Intentionally Different)

These are **generation templates** used by `/create-context`, not copies of canonical files. They contain template instructions + example content, so size differences are expected:

| File | Canonical (bytes) | context-template (bytes) | Notes |
|---|---|---|---|
| `source-tree.md` | 52,218 | 15,436 | Template is smaller (skeleton) |
| `tech-stack.md` | 18,427 | 13,868 | Template is smaller |
| `anti-patterns.md` | 7,524 | 24,883 | Template is LARGER (contains examples) |
| `coding-standards.md` | 13,946 | 16,294 | Template is larger |
| `architecture-constraints.md` | 12,033 | 19,167 | Template is larger |
| `dependencies.md` | 6,806 | 16,209 | Template is larger |

**These are NOT drift issues** — they are expected to differ. No action needed.

~~**Recommendation:**~~
1. ~~Sync all 6 files in `src/claude/memory/Constitution/` from `devforgeai/specs/context/`~~ ✅ Done 2026-02-19
2. ~~Either sync or remove `src/devforgeai/templates/source-tree.md` (31% behind)~~ ✅ Synced 2026-02-19

---

## 4. Orphaned Skill Directories (4 found) — ✅ PARTIALLY RESOLVED

**Severity:** MEDIUM — Dead weight, causes confusion, wastes context tokens if accidentally read.
**Status:** Deprecated backup/ directory and contents deleted on 2026-02-19. 3 orphaned skills remain.

| # | Directory | Issue | Contents | Status |
|---|-----------|-------|----------|--------|
| 1 | `.claude/skills/devforgeai-shared/` | No SKILL.md | `shared-phase-0-loader.md` only | ⬜ OPEN — Move loader or add SKILL.md |
| 2 | `.claude/skills/devforgeai-framework-enhancer/` | No SKILL.md | Empty `assets/templates/` and `references/` dirs | ⬜ OPEN — Delete empty shell |
| 3 | `.claude/skills/internet-sleuth-integration/` | No SKILL.md | Unknown | ⬜ OPEN — Investigate and merge or delete |
| 4 | ~~`.claude/skills/backup/`~~ | ~~Contains deprecated skills~~ | ~~2 deprecated skills~~ | ✅ **DELETED** 2026-02-19 |

### ~~Deprecated Skills in backup/~~ ✅ RESOLVED

| Deprecated Skill | Replacement | Status |
|---|---|---|
| ~~`devforgeai-brainstorming.deprecated/`~~ | `brainstorming/` | ✅ Deleted (16 files + directory tree) |
| ~~`devforgeai-development.deprecated/`~~ | `implementing-stories/` | ✅ Deleted (80 files + directory tree) |

---

## 5. Structural Anomalies (1 found) — ✅ RESOLVED

**Severity:** ~~MEDIUM~~ RESOLVED
**Status:** Nested `assets/assets/` flattened on 2026-02-19. `parallel.yaml.example` moved to correct `assets/templates/` location. Duplicate `implementation-notes-template.md` deleted. Empty nested directories removed.

| # | Path | Issue | Status |
|---|------|-------|--------|
| 1 | ~~`.claude/skills/implementing-stories/assets/assets/templates/`~~ | ~~Nested `assets/` inside `assets/`~~ | ✅ **RESOLVED** — flattened, nested dirs deleted |

---

## 6. Oversized Agents — ADR-012 Violations (11 found)

**Severity:** HIGH — Violates ADR-012 progressive disclosure pattern. Causes excessive token consumption on every agent invocation.

### Agents Exceeding 500-Line Limit

| # | Agent File | Lines | Over By | Has `references/` dir? |
|---|-----------|-------|---------|----------------------|
| 1 | `story-requirements-analyst.md` | 1,264 | +764 (153%) | No |
| 2 | `git-validator.md` | 1,164 | +664 (133%) | No |
| 3 | `internet-sleuth.md` | 1,134 | +634 (127%) | No |
| 4 | `ui-spec-formatter.md` | 1,071 | +571 (114%) | No |
| 5 | `dev-result-interpreter.md` | 1,019 | +519 (104%) | No |
| 6 | `qa-result-interpreter.md` | 911 | +411 (82%) | No |
| 7 | `git-worktree-manager.md` | 739 | +239 (48%) | No |
| 8 | `documentation-writer.md` | 671 | +171 (34%) | No |
| 9 | `architect-reviewer.md` | 649 | +149 (30%) | No |
| 10 | `sprint-planner.md` | 631 | +131 (26%) | No |
| 11 | `observation-extractor.md` | 585 | +85 (17%) | No |

### Impact Summary

| Metric | Value |
|--------|-------|
| Total agents | ~40 |
| Agents over 500 lines | 11 (28%) |
| Total excess lines | 3,838 |
| Avg excess per violation | 349 lines |
| Worst violator | `story-requirements-analyst.md` (1,264 lines) |

**Recommendation:** For each agent > 500 lines:
1. Create `.claude/agents/references/{agent-name}/` directory
2. Extract reference documentation, examples, and templates into reference files
3. Add `Read()` instructions in agent file to load references on-demand
4. Target: Agent body ≤ 500 lines after extraction

---

## 7. Context File Version Drift — Full Matrix — ✅ RESOLVED

**Severity:** ~~HIGH~~ RESOLVED
**Status:** All `src/claude/memory/Constitution/` and `src/devforgeai/templates/` copies synced to canonical on 2026-02-19.

### Complete Drift Matrix

**Legend:** Canonical = `devforgeai/specs/context/` | Constitution = `.claude/memory/Constitution/` | src Constitution = `src/claude/memory/Constitution/`

| Context File | Canonical | Constitution | src Constitution | src/templates | designing-systems template |
|---|---|---|---|---|---|
| **source-tree.md** | 52,218 | 52,218 ✅ | 46,455 ⚠️ (-11%) | 35,864 ❌ (-31%) | 15,436 (generation template) |
| **tech-stack.md** | 18,427 | 18,427 ✅ | 17,160 ⚠️ (-7%) | — | 13,868 (generation template) |
| **anti-patterns.md** | 7,524 | 7,524 ✅ | 5,432 ⚠️ (-28%) | — | 24,883 (generation template) |
| **coding-standards.md** | 13,946 | 13,946 ✅ | 13,498 ⚠️ (-3%) | — | 16,294 (generation template) |
| **architecture-constraints.md** | 12,033 | 12,033 ✅ | 11,809 ⚠️ (-2%) | — | 19,167 (generation template) |
| **dependencies.md** | 6,806 | 6,806 ✅ | 5,965 ⚠️ (-12%) | — | 16,209 (generation template) |

### Key Findings

- `.claude/memory/Constitution/` — **All 6 files synced** ✅
- `src/claude/memory/Constitution/` — **All 6 files stale** ⚠️ (2-28% behind)
- `src/devforgeai/templates/source-tree.md` — **31% behind** ❌ (very stale)
- `designing-systems/assets/context-templates/` — Intentionally different (generation templates, not copies)

---

## Recommended Next Steps (Priority Order)

### P0 — Immediate (blocks correctness)

1. ~~**Sync `src/claude/memory/Constitution/`** — Copy all 6 files from `devforgeai/specs/context/` to `src/claude/memory/Constitution/`~~ ✅ Done 2026-02-19
2. ~~**Resolve `epic-template.md` duplication** — Choose single canonical location, remove other copies~~ ✅ Orchestration + specs copies deleted. Remaining: designing-systems + discovering-requirements (evaluate if both need copies)
3. ~~**Resolve `story-template.md` duplication** — Remove orchestration copy~~ ✅ Done

### ~~P1 — Soon (reduces confusion)~~ ✅ ALL RESOLVED

4. ~~**Flatten nested `assets/assets/`** — Move files up, delete nested directory~~ ✅ Done
5. ~~**Delete all `.bak`, `.old`, `.rec*-backup` files** — 21 files, safe to remove~~ ✅ Done
6. ~~**Delete `.backup-2025-12-23/` hidden directories** — In brainstorming skill (3 locations)~~ ✅ Done
7. ~~**Delete deprecated skill backups** — Remove `.claude/skills/backup/` entirely~~ ✅ Done

### P2 — Next sprint (architectural compliance)

8. **Extract oversized agents** — 11 agents need `references/` directory extraction per ADR-012
9. **Remove orphaned skill directories** — Delete `devforgeai-framework-enhancer/`, `devforgeai-shared/`, `internet-sleuth-integration/`
10. ~~**Evaluate `src/devforgeai/templates/source-tree.md`** — Either sync or remove (31% stale)~~ ✅ Synced 2026-02-19

### P3 — Quarterly (housekeeping)

11. **Clean `tmp/` directory** — 2.1+ GB of experimental/legacy data
12. **Re-run `/audit-orphans`** — Verify all P0-P2 items resolved

---

## Appendix A: Files Deleted (Cleanup Log)

All files below were deleted on **2026-02-19**:

```
# Backup files (21) ✅ ALL DELETED
.claude/skills/brainstorming/.backup-2025-12-23/SKILL.md.bak
.claude/skills/brainstorming/.backup-2025-12-23/handoff-synthesis-workflow.md.bak
.claude/skills/brainstorming/.backup-2025-12-23/output-templates.md.bak
src/claude/skills/brainstorming/.backup-2025-12-23/SKILL.md.bak
src/claude/skills/brainstorming/.backup-2025-12-23/handoff-synthesis-workflow.md.bak
src/claude/skills/brainstorming/.backup-2025-12-23/output-templates.md.bak
.claude/skills/backup/devforgeai-brainstorming.deprecated/.backup-2025-12-23/SKILL.md.bak
.claude/skills/backup/devforgeai-brainstorming.deprecated/.backup-2025-12-23/handoff-synthesis-workflow.md.bak
.claude/skills/backup/devforgeai-brainstorming.deprecated/.backup-2025-12-23/output-templates.md.bak
.claude/skills/devforgeai-qa/SKILL.md.rec2-backup
src/claude/skills/devforgeai-qa/SKILL.md.rec2-backup
src/claude/memory/skill-execution-troubleshooting.md.rec3-backup
.claude/scripts/statusline.sh.bak
.claude/settings.local.json.bak
devforgeai/scripts/statusline.py.bak
devforgeai/scripts/statusline.py.old
src/devforgeai/scripts/statusline.py.bak
devforgeai/logs/pre-tool-use.log.bak
tests/pytest.ini.bak
tmp/DevForgeAI.01/tmp/src/workflows/shared/validate-spec-workflow.md.bak
tmp/DevForgeAI.01/.claude/settings.json.old

# Nested anomaly duplicate (1) ✅ DELETED + directory flattened
.claude/skills/implementing-stories/assets/assets/templates/implementation-notes-template.md
  → parallel.yaml.example moved to assets/templates/
  → Empty assets/assets/ directory removed

# Deprecated skill directories (entire trees) ✅ DELETED
.claude/skills/backup/devforgeai-brainstorming.deprecated/  (16 files)
.claude/skills/backup/devforgeai-development.deprecated/    (80 files)
  → Empty .claude/skills/backup/ directory removed

# Duplicate templates (3) ✅ DELETED
.claude/skills/devforgeai-orchestration/assets/templates/story-template.md
.claude/skills/devforgeai-orchestration/assets/templates/epic-template.md
devforgeai/specs/templates/epic-template.md
```

**Total files deleted:** 121 (21 backups + 1 nested duplicate + 96 deprecated skill files + 3 duplicate templates)

---

**Report generated by `/audit-orphans` command.**
**Cleanup performed:** 2026-02-19
**Remaining open items:** P2 #8 (oversized agents), P2 #9 (orphaned skill dirs)
**Next audit recommended:** After P2 items resolved.
