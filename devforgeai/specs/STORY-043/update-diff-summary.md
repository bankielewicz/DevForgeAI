# Path Update Summary: .claude/ → src/claude/

**Date Generated:** November 19, 2025
**Status:** Ready for Implementation

## Overview

This document summarizes the path updates needed to migrate from `.claude/` and `devforgeai/` source locations to `src/claude/` and `src/devforgeai/` as part of the package distribution refactoring (STORY-043).

## Classification Summary

Based on path audit scan of 12,869 references across 450+ files:

| Category | Count | Action |
|----------|-------|--------|
| **Deploy-time** (KEEP AS-IS) | 1,047 | No updates needed |
| **Source-time** (UPDATE) | 1,774 | Apply sed transforms |
| **Ambiguous** (MANUAL REVIEW) | 9,723 | Developer review required |
| **Excluded** (BACKUP/ARCHIVE) | 325 | Skip updates |
| **TOTAL** | **12,869** | — |

## Deploy-Time References (1,047 refs - PRESERVE)

**Rationale:** These references are used at runtime after the framework is installed. They should NOT be changed as they reference the deployed framework structure.

### Categories

1. **CLAUDE.md @file references** (~21 refs)
   - Example: `@.claude/memory/skills-reference.md`
   - Action: KEEP UNCHANGED
   - Reason: References deployed framework files loaded at runtime

2. **devforgeai/context/ paths** (~417 refs)
   - Example: Files reading `devforgeai/context/tech-stack.md`
   - Action: KEEP UNCHANGED
   - Reason: These are architectural constraint files deployed with framework

3. **package.json scripts** (~251 refs)
   - Example: `"scripts": { "setup": "bash .claude/scripts/install_hooks.sh" }`
   - Action: KEEP UNCHANGED
   - Reason: Installation scripts reference deployed locations

4. **CLI tool references** (~358 refs)
   - Example: `devforgeai/RCA/` references
   - Action: KEEP UNCHANGED
   - Reason: Framework deployment locations

## Source-Time References (1,774 refs - UPDATE)

**Rationale:** These are references in source code files that need to be updated to point to the new `src/` structure during development/build.

### Update Patterns

#### Pattern 1: Skills Read() Calls (~74 refs)
**Files affected:** `.claude/skills/*/SKILL.md`

**Before:**
```markdown
Read(file_path="../../../.claude/skills/devforgeai-development/references/tdd-workflow-guide.md")
Read(file_path="./.claude/memory/skills-reference.md")
Read(file_path=".claude/skills/devforgeai-qa/references/quality-metrics-guide.md")
```

**After:**
```markdown
Read(file_path="src/claude/skills/devforgeai-development/references/tdd-workflow-guide.md")
Read(file_path="src/claude/memory/skills-reference.md")
Read(file_path="src/claude/skills/devforgeai-qa/references/quality-metrics-guide.md")
```

**sed command:**
```bash
sed -i 's|Read(file_path="\.\./\.\./\.\./\.claude/|Read(file_path="src/claude/|g' file.md
sed -i 's|Read(file_path="\.\./.claude/|Read(file_path="src/claude/|g' file.md
sed -i 's|Read(file_path="\.claude/|Read(file_path="src/claude/|g' file.md
```

#### Pattern 2: Documentation References (~52 refs)
**Files affected:** `.claude/skills/*/references/` markdown files

**Before:**
```markdown
For skill references, see Read(file_path=".claude/memory/skills-reference.md")
The QA framework is documented in .claude/skills/devforgeai-qa/references/quality-metrics-guide.md
```

**After:**
```markdown
For skill references, see Read(file_path="src/claude/memory/skills-reference.md")
The QA framework is documented in src/claude/skills/devforgeai-qa/references/quality-metrics-guide.md
```

**sed command:**
```bash
sed -i 's|Read(file_path="\.claude/memory|Read(file_path="src/claude/memory|g' file.md
sed -i 's|\.claude/skills|src/claude/skills|g' file.md
```

#### Pattern 3: Agent/Subagent Integration (~38 refs)
**Files affected:** `.claude/agents/*.md`, `.claude/commands/*.md`

**Before:**
```markdown
Task(subagent_type="test-automator",
     prompt="See ../.claude/agents/test-automator.md for details")

Skill(command="devforgeai-development")
# Loads from .claude/skills/devforgeai-development/references/
```

**After:**
```markdown
Task(subagent_type="test-automator",
     prompt="See src/claude/agents/test-automator.md for details")

Skill(command="devforgeai-development")
# Loads from src/claude/skills/devforgeai-development/references/
```

## Ambiguous References (9,723 refs - MANUAL REVIEW)

These references may be deploy-time or source-time depending on context. Manual review required for classification:

**Examples of ambiguous patterns:**
- References in comments or documentation strings
- References in code that might be loaded at different times
- References in test files
- Relative paths that could be interpreted multiple ways

**Recommendation:** Create a separate ticket for detailed analysis of ambiguous category.

## Excluded References (325 refs - SKIP)

Files matching these patterns are excluded from updates:

- `*.backup` - Backup copies
- `*.original` - Original versions
- `*.pre-*` - Pre-migration copies

**Reason:** These files preserve history and should not be modified.

## Update Strategy

### Phase 1: Skills (74 refs)
**Duration:** ~5 seconds
**Files:** 25 SKILL.md files
**Pattern:** `.claude/skills/*/` → `src/claude/skills/*/`

### Phase 2: Documentation (52 refs)
**Duration:** ~3 seconds
**Files:** 15 reference documentation files
**Pattern:** `.claude/memory/` → `src/claude/memory/`

### Phase 3: Agent Integration (38 refs)
**Duration:** ~2 seconds
**Files:** 10 agent/command files
**Pattern:** Agent and skill references

## Safety Measures

1. **Pre-flight checks:** Git status clean, 50 MB disk space available
2. **Backup creation:** Timestamped backup before any modifications
3. **Atomic operations:** sed with .bak files
4. **Validation:** Post-update validation to detect broken references
5. **Rollback:** Auto-rollback on validation failure

## Validation Checklist

After updates:

- [ ] Syntax check: No old `.claude/` patterns in Read() calls
- [ ] Semantic check: All Read() paths resolve to files
- [ ] Behavioral check: 3 test workflows pass without errors
- [ ] Preservation: 1,047 deploy-time refs unchanged
- [ ] Coverage: 1,774 source-time refs updated
- [ ] Performance: Update < 30 seconds
- [ ] Rollback: Backup restoration successful

## Expected Results

**After Update:**
```
✓ 164 source-time references updated across 87 files
✓ 0 errors encountered during updates
✓ Deploy-time references preserved
✓ Validation report: PASSED
✓ 0 broken references detected
✓ 3/3 test workflows pass
✓ All skills load references correctly
```

## Next Steps

1. Run: `bash src/scripts/audit-path-references.sh` (generates classification files)
2. Review: `devforgeai/specs/STORY-043/path-audit-*.txt` files
3. Run: `bash src/scripts/update-paths.sh` (applies updates with backup)
4. Validate: `bash src/scripts/validate-paths.sh` (checks for broken refs)
5. Test: Run 3 integration workflows (`/create-epic`, `/create-story`, `/dev`)
6. Commit: Stage 87 updated files to git

## References

- Story: `devforgeai/specs/Stories/STORY-043-update-path-references-to-src.story.md`
- Audit Report: `devforgeai/specs/STORY-043/path-audit-report.txt`
- Update Script: `src/scripts/update-paths.sh`
- Validation Script: `src/scripts/validate-paths.sh`
- Rollback Script: `src/scripts/rollback-path-updates.sh`
