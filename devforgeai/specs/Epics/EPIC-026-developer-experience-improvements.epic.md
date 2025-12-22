---
id: EPIC-026
title: Developer Experience Improvements
business-value: Improve developer experience with plan file resume, git recovery, and CLI validation
status: Planning
priority: High
complexity-score: 7
architecture-tier: Tier 2 (Standard Application)
created: 2025-12-20
estimated-points: 7
target-sprints: 1
research-reference: STORY-114 observations
related-epics: [EPIC-024, EPIC-025]
stories: [STORY-127, STORY-128, STORY-129]
---

# Developer Experience Improvements

## Business Goal

Improve the developer experience in DevForgeAI workflows by addressing pain points observed during STORY-114 development session: plan file fragmentation, git lock file issues on WSL2, and missing CLI command validation. These improvements reduce friction and enable smoother session recovery.

**Success Metrics:**
- Plan file resume: Zero duplicate plan files for same story
- Git lock recovery: Documented recovery path for WSL2 lock issues
- CLI validation: Graceful fallback when CLI not installed
- Developer friction: Reduced time spent on tooling issues

## Features

### Feature 1: Plan File Resume Convention (STORY-127)
**Description:** Add convention to CLAUDE.md for checking existing plan files before creating new ones, preventing duplicate plan files for the same story.

**User Stories (high-level):**
1. As a developer, I want existing plan files detected before creating new ones
2. As a developer, I want plan files named with story ID when available
3. As a developer, I want backward compatibility with random-named plan files

**Estimated Effort:** 3 story points

**Files to Create/Modify:**
| Action | File Path | Purpose |
|--------|-----------|---------|
| MODIFY | `CLAUDE.md` | Add Plan File Convention section |
| MODIFY | `.claude/skills/devforgeai-development/SKILL.md` | Reference convention in Phase 0 |

**Convention:**
```markdown
## Plan File Convention

Before creating new plan file, check for existing:
1. `Glob(".claude/plans/*.md")`
2. Search for story ID in plan files
3. If found with matching story ID, resume existing plan
4. If not found, create new with story ID in filename

**Naming Convention:** Include story ID when known
- Good: `STORY-114-parallel-docs-plan.md`
- Avoid: Random adjective-noun combinations for story work
```

**Acceptance Criteria Themes:**
- AC#1: CLAUDE.md includes Plan File Convention section
- AC#2: /dev Phase 0 checks for existing plan files before creating new
- AC#3: Plan files with story ID are prioritized for resumption
- AC#4: Random-named plan files still work (backward compatible)

### Feature 2: Git Lock File Recovery (STORY-128)
**Description:** Add lock file recovery guidance to git-workflow-conventions.md with WSL2-specific troubleshooting.

**User Stories (high-level):**
1. As a developer, I want documented steps to recover from stale lock files
2. As a developer, I want WSL2-specific guidance for lock file issues
3. As a developer, I want prevention tips to avoid lock file problems

**Estimated Effort:** 2 story points

**Files to Create/Modify:**
| Action | File Path | Purpose |
|--------|-----------|---------|
| MODIFY | `.claude/skills/devforgeai-development/references/git-workflow-conventions.md` | Add Lock File Recovery section |

**Content:**
```markdown
## Lock File Recovery

If git fails with "index.lock exists":

**Diagnosis:**
```bash
ls -la .git/index.lock  # Check if exists
ps aux | grep git       # Check for running git processes
```

**Recovery (if no git process running):**
```bash
rm -f .git/index.lock
```

**WSL2 Note:** Lock files are common when:
- VS Code with Git extension is open
- Cross-filesystem access between Windows and WSL
- Previous git command crashed
```

**Acceptance Criteria Themes:**
- AC#1: git-workflow-conventions.md includes Lock File Recovery section
- AC#2: Diagnosis commands documented
- AC#3: WSL2-specific guidance included
- AC#4: Prevention tips documented

### Feature 3: CLI Command Availability Check (STORY-129)
**Description:** Add CLI availability check to preflight validation with graceful fallback when devforgeai CLI is not installed.

**User Stories (high-level):**
1. As a developer, I want warnings (not errors) when CLI is missing
2. As a developer, I want fallback validation when CLI unavailable
3. As a developer, I want to know which validations are skipped

**Estimated Effort:** 2 story points

**Files to Create/Modify:**
| Action | File Path | Purpose |
|--------|-----------|---------|
| MODIFY | `.claude/skills/devforgeai-development/references/preflight-validation.md` | Add CLI availability check |

**New Preflight Step (Step 0.0.5):**
```bash
if ! command -v devforgeai &> /dev/null; then
    echo "WARN: devforgeai CLI not installed"
    echo "  - Hook checks will be skipped"
    echo "  - Manual validation required"
    CLI_AVAILABLE=false
else
    CLI_AVAILABLE=true
    DEVFORGEAI_VERSION=$(devforgeai --version 2>/dev/null || echo "unknown")
    echo "✓ devforgeai CLI: $DEVFORGEAI_VERSION"
fi
```

**Acceptance Criteria Themes:**
- AC#1: Preflight Step 0.0.5 checks CLI availability
- AC#2: Warning displayed if CLI not installed (not error)
- AC#3: Downstream steps skip CLI calls gracefully
- AC#4: Fallback validation documented

## Requirements Summary

### Functional Requirements

| ID | Requirement | Priority | Story |
|----|-------------|----------|-------|
| FR-1 | Plan file convention documented in CLAUDE.md | HIGH | STORY-127 |
| FR-2 | /dev Phase 0 checks for existing plan files | HIGH | STORY-127 |
| FR-3 | Lock file recovery section in git-workflow-conventions.md | MEDIUM | STORY-128 |
| FR-4 | CLI availability check in preflight validation | MEDIUM | STORY-129 |
| FR-5 | Graceful fallback when CLI not installed | MEDIUM | STORY-129 |

### Non-Functional Requirements

| ID | Requirement | Target | Story |
|----|-------------|--------|-------|
| NFR-1 | Plan file search latency | <500ms (glob + grep) | STORY-127 |
| NFR-2 | Backward compatibility | 100% existing plan files work | STORY-127 |
| NFR-3 | CLI check overhead | <100ms | STORY-129 |

## Technical Approach

### Plan File Search Algorithm
```python
# Pseudocode for plan file resume logic
def find_existing_plan(story_id: str) -> Optional[str]:
    plan_files = glob(".claude/plans/*.md")
    for plan_file in plan_files:
        content = read(plan_file)
        if story_id in content:
            return plan_file
    return None
```

### CLI Availability Pattern
```bash
# Check once at preflight, store in variable
if command -v devforgeai &> /dev/null; then
    CLI_AVAILABLE=true
else
    CLI_AVAILABLE=false
    echo "WARN: devforgeai CLI not installed - some checks skipped"
fi

# Later in workflow
if [ "$CLI_AVAILABLE" = true ]; then
    devforgeai check-hooks --operation=dev
else
    echo "  Skipping: CLI-based hook checks (CLI not available)"
fi
```

## Dependencies

- None external
- All 3 stories are independent and can run in parallel

## Risks & Mitigations

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| Plan file naming conflicts | Low | Low | Use story ID prefix when available |
| CLI fallback misses validations | Medium | Medium | Document which validations are CLI-only |
| Lock file guidance causes data loss | Low | High | Include safety checks before rm -f |

## Sprint Allocation

**Sprint-8 or Sprint-9 (7 points):**
- STORY-127: Plan File Resume Convention (3 pts)
- STORY-128: Git Lock File Recovery (2 pts)
- STORY-129: CLI Command Availability Check (2 pts)

## Definition of Done

### Epic-Level Completion Criteria
- [ ] All 3 stories reach Released status
- [ ] Plan file convention documented and referenced in /dev workflow
- [ ] Lock file recovery tested on WSL2 environment
- [ ] CLI availability check integrated into preflight
- [ ] Fallback validations documented for CLI-less environments
