# Plan: Migrate cross-ai-collaboration → spec-driven-collaboration

**Created:** 2026-03-19
**Status:** COMPLETE
**Decision:** Skill name = `spec-driven-collaboration` (user-approved)

---

## Context

The `cross-ai-collaboration` skill generates self-contained collaboration documents for sharing issues with external AI systems (Gemini, ChatGPT, etc.). It has 6 phases, a 10-section output template, and a `/collaborate` slash command.

**Problem:** The current skill lacks the structural anti-skip enforcement (Execute-Verify-Gate pattern) used by all other `spec-driven-*` skills. This causes Claude to skip phases/steps due to token optimization bias, creating double work and undermining framework integrity.

**Goal:** Create `spec-driven-collaboration` as a full replacement with:
- Execute-Verify-Record anti-skip enforcement at every step
- Per-phase reference loading (no consolidated reads)
- Phase files for progressive disclosure
- Binary CLI gate enforcement
- Self-sufficient (all references local, no external dependencies)

After migration, `cross-ai-collaboration` will be archived and eventually deleted. No framework file will reference the old skill.

---

## TODO Checklist

- [x] 1. Explore existing cross-ai-collaboration skill (6 phases, 10-section template)
- [x] 2. Explore spec-driven-* patterns (Execute-Verify-Gate, anti-skip enforcement)
- [x] 3. Explore skill-creator, inventory, command patterns
- [x] 4. User approved name: `spec-driven-collaboration`
- [x] 5. Write plan file (this document)
- [x] 6. Invoke `/skill-creator` to create `spec-driven-collaboration`
- [x] 7. Backup `src/claude/commands/collaborate.md` → `src/claude/commands/backup/collaborate.md`
- [x] 8. Update `src/claude/commands/collaborate.md` to invoke new skill
- [x] 9. Update `src/claude/memory/skills-reference.md` (replace old skill entry)
- [x] 10. Update `src/claude/memory/commands-reference.md` (update /collaborate entry)
- [x] 11. Update `tmp/skill-inventory.md` (archive old, add new, migration chain)
- [x] 12. Verify all files created correctly

---

## Key Files Inventory

### Files to CREATE (via /skill-creator)

| File | Purpose |
|------|---------|
| `src/claude/skills/spec-driven-collaboration/SKILL.md` | Main skill definition with anti-skip enforcement |
| `src/claude/skills/spec-driven-collaboration/phases/phase-01-context-gathering.md` | Interactive issue collection via AskUserQuestion |
| `src/claude/skills/spec-driven-collaboration/phases/phase-02-constitution-loading.md` | Load 6 constitutional files, extract constraints |
| `src/claude/skills/spec-driven-collaboration/phases/phase-03-code-collection.md` | Read affected files, tests, error output |
| `src/claude/skills/spec-driven-collaboration/phases/phase-04-analysis-template.md` | Load template, reason through issue, populate 10 sections |
| `src/claude/skills/spec-driven-collaboration/phases/phase-05-document-generation.md` | Write document to tmp/, verify write |
| `src/claude/skills/spec-driven-collaboration/phases/phase-06-completion-report.md` | Display summary and next steps |
| `src/claude/skills/spec-driven-collaboration/references/collaboration-prompt-template.md` | 10-section output document template (migrated from old skill) |
| `src/claude/skills/spec-driven-collaboration/references/context-gathering-guide.md` | Detailed guide for Phase 01 interactive gathering |
| `src/claude/skills/spec-driven-collaboration/references/code-collection-patterns.md` | Patterns for finding related files, tests, configs |
| `src/claude/skills/spec-driven-collaboration/references/analysis-reasoning-guide.md` | Guide for Phase 04 reasoning (hypotheses, constraints, questions) |

### Files to MODIFY

| File | Change |
|------|--------|
| `src/claude/commands/collaborate.md` | Change `Skill(command="cross-ai-collaboration")` → `Skill(command="spec-driven-collaboration")` |
| `src/claude/memory/skills-reference.md` | Replace cross-ai-collaboration entry with spec-driven-collaboration |
| `src/claude/memory/commands-reference.md` | Update /collaborate skill reference |
| `tmp/skill-inventory.md` | Archive row #28, add new #28b, add Table 4 migration chain |

### Files to BACKUP

| Source | Backup Destination |
|--------|-------------------|
| `src/claude/commands/collaborate.md` | `src/claude/commands/backup/collaborate.md` |

### Files to ARCHIVE (later, not in this task)

| File | Note |
|------|------|
| `src/claude/skills/cross-ai-collaboration/SKILL.md` | Archive after new skill verified working |
| `src/claude/skills/cross-ai-collaboration/references/collaboration-prompt-template.md` | Template migrated into new skill |

---

## Phase Mapping: Old → New

The 6 original phases are preserved 1:1. Each gets Execute-Verify-Record enforcement:

| Old Phase | New Phase | Phase File | Key Changes |
|-----------|-----------|------------|-------------|
| Phase 01: Context Gathering | Phase 01: Context Gathering | `phase-01-context-gathering.md` | + EVR triplets for each step, + gate verification with HALT |
| Phase 02: Constitution Loading | Phase 02: Constitution Loading | `phase-02-constitution-loading.md` | + Parallel Read() for 6 files, + constraint extraction verification |
| Phase 03: Code Collection | Phase 03: Code Collection | `phase-03-code-collection.md` | + Artifact count verification, + test file discovery patterns |
| Phase 04: Analysis & Template Population | Phase 04: Analysis & Template Population | `phase-04-analysis-template.md` | + Per-section completeness check, + reasoning documentation |
| Phase 05: Document Generation | Phase 05: Document Generation | `phase-05-document-generation.md` | + Write verification (read-back), + section count validation |
| Phase 06: Completion Report | Phase 06: Completion Report | `phase-06-completion-report.md` | + Final gate with artifact summary |

### Anti-Skip Enforcement Added Per Phase

Every step gets the Execute-Verify-Record triplet:

```
### Step N.M: Description

EXECUTE: <exact tool call - Read, Write, AskUserQuestion, Glob, Grep>

VERIFY: <How to confirm it happened - file exists, content matches, count correct>
IF verification fails: HALT

RECORD: Phase state updated
```

---

## SKILL.md Structure (What /skill-creator Will Generate)

```yaml
---
name: spec-driven-collaboration
description: >
  Generate self-contained collaboration documents for external AI systems
  with structural anti-skip enforcement (Execute-Verify-Record pattern).
allowed-tools:
  - Read, Write, Edit, Glob, Grep, AskUserQuestion, Skill
model: opus
effort: High
---
```

### Required Sections in SKILL.md

1. **Execution Model** - Self-check violation list (8 items)
2. **Anti-Skip Enforcement Contract** - 4-layer enforcement documentation
3. **Parameter Extraction** - How ISSUE_DESCRIPTION and TARGET_AI come from conversation
4. **Phase Table** - 6 phases with file paths, step counts, required tools
5. **Phase Orchestration Loop** - Sequential execution with entry/exit gates
6. **State Persistence** - Phase tracking location
7. **Success Criteria** - Document generated, all sections populated, file verified
8. **Reference Files Inventory** - All reference files with purpose

### Token Optimization Bias Prevention (Mandatory in SKILL.md)

```markdown
## Token Optimization Bias Prevention

NEVER skip, compress, or shortcut a phase step to save tokens.

Prohibited rationalizations:
- "The template is simple enough to populate from memory" — Load the template file fresh
- "I already read the constitution files" — Read them again in Phase 02
- "The document is short, no need to verify" — Read it back to verify
- "Phase 06 is just a display, I can skip it" — Execute it fully
```

---

## /collaborate Command Update

### Before (current)
```
Skill(command="cross-ai-collaboration")
```

### After
```
Skill(command="spec-driven-collaboration")
```

### Other Changes to collaborate.md
- Update skill reference path: `.claude/skills/spec-driven-collaboration/SKILL.md`
- Update template reference path: `.claude/skills/spec-driven-collaboration/references/collaboration-prompt-template.md`
- Keep same argument handling (issue-description, --target=AI)
- Keep same lean orchestration pattern

---

## Memory File Updates

### skills-reference.md Changes

**Replace** the cross-ai-collaboration entry (lines ~1509-1527) with:

```markdown
### spec-driven-collaboration
- **Command:** `/collaborate`
- **Purpose:** Generate self-contained collaboration documents for external AI systems (Gemini, ChatGPT, etc.)
- **Phases:** 6 (Context Gathering → Constitution Loading → Code Collection → Analysis & Template → Document Generation → Completion Report)
- **Anti-Skip:** Execute-Verify-Record pattern at every step
- **Output:** `tmp/collaborate-{target_ai}-{slug}-{date}.md`
- **Migration:** Replaces `cross-ai-collaboration` (ADR-024 still applies)
```

### commands-reference.md Changes

**Update** the /collaborate entry (lines ~2156-2182):
- Change skill reference from `cross-ai-collaboration` to `spec-driven-collaboration`
- Update skill path references
- Keep same usage syntax

---

## skill-inventory.md Updates

### Table 1 Changes

**Row #28 becomes:**
```
| 28 | `cross-ai-collaboration/` | *(archived)* | `cross-ai-collaboration` | **ARCHIVED** -- Absorbed into spec-driven-collaboration. All references, templates migrated. Archived 2026-03-19. | Complete |
| 28b | `spec-driven-collaboration/` | `/collaborate` | `spec-driven-collaboration` | **ACTIVE** -- 6-phase cross-AI collaboration with anti-skip enforcement (Execute-Verify-Record). Self-sufficient (4 refs + 6 phase files + 1 template migrated from cross-ai-collaboration) | Complete |
```

### Table 4 Migration Chain Entry

```
| cross-ai-collaboration → spec-driven-collaboration | 2026-03-19 | Anti-skip enforcement, per-phase reference loading, EVR triplets | ADR-024 (original), no new ADR needed |
```

---

## Execution Strategy

### Step 1: Invoke /skill-creator (Task #4)
- Provide full context about the 6 phases, 10-section template, EVR pattern
- Skill-creator generates SKILL.md, phase files, and reference files
- All files created in `src/claude/skills/spec-driven-collaboration/`

### Step 2: Backup and Update Command (Task #5)
- Copy `src/claude/commands/collaborate.md` → `src/claude/commands/backup/collaborate.md`
- Edit `src/claude/commands/collaborate.md` to reference new skill

### Step 3: Update Memory Files (Task #6)
- Edit `src/claude/memory/skills-reference.md`
- Edit `src/claude/memory/commands-reference.md`

### Step 4: Update Inventory (Task #7)
- Edit `tmp/skill-inventory.md`

### Step 5: Verification
- Glob to confirm all new files exist
- Read SKILL.md to confirm EVR pattern present
- Read collaborate.md to confirm skill reference updated
- Grep for "cross-ai-collaboration" across src/ to confirm no remaining references

---

## Verification Checklist

After all tasks complete, verify:

- [ ] `src/claude/skills/spec-driven-collaboration/SKILL.md` exists and has EVR pattern
- [ ] All 6 phase files exist in `phases/` subdirectory
- [ ] `references/collaboration-prompt-template.md` migrated (10 sections)
- [ ] Additional reference files created (3-4 files)
- [ ] `src/claude/commands/backup/collaborate.md` is the backup of old command
- [ ] `src/claude/commands/collaborate.md` invokes `spec-driven-collaboration`
- [ ] `src/claude/memory/skills-reference.md` has new skill entry
- [ ] `src/claude/memory/commands-reference.md` references new skill
- [ ] `tmp/skill-inventory.md` has archived row #28 and new #28b
- [ ] `grep "cross-ai-collaboration" src/` returns zero matches in active files

---

## Recovery Instructions (For New Sessions)

If this plan is resumed in a new session:

1. **Read this plan file first:** `.claude/plans/spec-driven-collaboration-migration.md`
2. **Check TODO checklist above** to see what's completed
3. **Glob** `src/claude/skills/spec-driven-collaboration/` to see if skill was already created
4. **Read** `src/claude/commands/collaborate.md` to check if command was updated
5. **Grep** `cross-ai-collaboration` in `src/` to find remaining references
6. Resume from the first unchecked TODO item

---

## References

| Reference | Path |
|-----------|------|
| Old skill SKILL.md | `src/claude/skills/cross-ai-collaboration/SKILL.md` |
| Old template | `src/claude/skills/cross-ai-collaboration/references/collaboration-prompt-template.md` |
| Old command | `src/claude/commands/collaborate.md` |
| ADR-024 (original skill) | `devforgeai/specs/adrs/ADR-024-cross-ai-collaboration-skill.md` |
| Spec-driven patterns (dev) | `src/claude/skills/spec-driven-dev/SKILL.md` |
| Spec-driven patterns (stories) | `src/claude/skills/spec-driven-stories/SKILL.md` |
| Skills reference | `src/claude/memory/skills-reference.md` |
| Commands reference | `src/claude/memory/commands-reference.md` |
| Skill inventory | `tmp/skill-inventory.md` |
| Source tree (for path validation) | `devforgeai/specs/context/source-tree.md` |
