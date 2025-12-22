---
id: EPIC-024
title: Session Recovery and Story Isolation
business-value: Resilient development workflow that survives context window fills and isolates parallel story work
status: Ready for Dev
priority: High
complexity-score: 21
architecture-tier: Tier 2 (Standard Application)
created: 2025-12-20
estimated-points: 21
target-sprints: 1
research-reference: STORY-114 observations
stories:
  - STORY-120-session-checkpoint-protocol.story.md
  - STORY-121-story-scoped-pre-commit-validation.story.md
  - STORY-122-line-ending-normalization.story.md
  - STORY-123-uncommitted-story-file-warning.story.md
  - STORY-124-wsl-test-execution-documentation.story.md
---

# Session Recovery and Story Isolation

## Business Goal

Transform architectural observations from STORY-114 development session into actionable improvements for the DevForgeAI framework. Address context crash recovery, git commit scoping, line endings, story isolation warnings, and WSL documentation.

**Success Metrics:**
- Session recovery: 100% of TDD phase progress persisted across context window fills
- Commit scoping: Zero false positive pre-commit blocks from unrelated stories
- Line endings: Zero CRLF/LF related git diff noise
- Story isolation: Clear warnings when uncommitted story files exist
- Documentation: WSL test execution documented for all common issues

## Features

### Feature 1: Session Checkpoint Protocol (STORY-120)
**Description:** Create checkpoint files at each TDD phase completion to enable session recovery when context window fills. Checkpoints stored in `devforgeai/sessions/{STORY-ID}/checkpoint.json`.

**User Stories (high-level):**
1. As a developer, I want TDD progress checkpointed so I can resume after context window fills
2. As a developer, I want `/resume-dev` to auto-detect resumption point from checkpoint
3. As a developer, I want checkpoints cleaned up after story completion

**Estimated Effort:** 8 story points

**Files to Create/Modify:**
| Action | File Path | Purpose |
|--------|-----------|---------|
| CREATE | `.claude/skills/devforgeai-development/references/session-checkpoint.md` | Checkpoint protocol documentation |
| CREATE | `src/claude/scripts/devforgeai_cli/session/checkpoint.py` | Checkpoint read/write utilities |
| CREATE | `src/claude/scripts/devforgeai_cli/session/__init__.py` | Package init |
| MODIFY | `.claude/skills/devforgeai-development/SKILL.md` | Add checkpoint writes at phase transitions |
| MODIFY | `.claude/commands/resume-dev.md` | Add checkpoint file reading for auto-detect |

**Checkpoint JSON Schema:**
```json
{
  "story_id": "STORY-XXX",
  "phase": 3,
  "phase_name": "Refactor",
  "timestamp": "2025-12-20T15:30:00Z",
  "progress_percentage": 67,
  "dod_completion": {
    "implementation": [5, 8],
    "quality": [2, 6],
    "testing": [3, 5],
    "documentation": [1, 4]
  },
  "last_action": "code-reviewer subagent completed",
  "next_action": "Phase 4: Integration Testing"
}
```

**Acceptance Criteria Themes:**
- AC#1: Checkpoint file written at each phase completion (0-7)
- AC#2: Checkpoint includes: story_id, phase, timestamp, progress_pct, dod_status
- AC#3: `/resume-dev` reads checkpoint file for auto-detection when no phase specified
- AC#4: Checkpoint cleaned up on story completion (Released status)
- AC#5: Graceful handling if checkpoint file missing/corrupted (fallback to Phase 0)

### Feature 2: Story-Scoped Pre-Commit Validation (STORY-121)
**Description:** Add environment variable `DEVFORGEAI_STORY` to scope pre-commit validation to specific story, preventing blocks from unrelated story validation errors.

**User Stories (high-level):**
1. As a developer, I want commits scoped to current story so other stories don't block me
2. As a developer, I want backward compatibility when env var is not set
3. As a developer, I want clear messaging showing which story is being validated

**Estimated Effort:** 5 story points

**Files to Create/Modify:**
| Action | File Path | Purpose |
|--------|-----------|---------|
| MODIFY | `.git/hooks/pre-commit` (lines 44-58) | Add DEVFORGEAI_STORY env var filtering |
| MODIFY | `src/claude/scripts/install_hooks.sh` | Update hook template with scoping logic |
| CREATE | `devforgeai/docs/STORY-SCOPED-COMMITS.md` | User documentation for scoped commits |

**Implementation Code:**
```bash
# In .git/hooks/pre-commit (replace lines 44-58)
if [ -n "$DEVFORGEAI_STORY" ]; then
    # Scoped validation - only validate specific story
    STORY_FILES=$(git diff --cached --name-only --diff-filter=d | grep "${DEVFORGEAI_STORY}" | grep -v '^tests/' || true)
    echo "  Scoped to: $DEVFORGEAI_STORY"
else
    # Default behavior - validate all staged story files
    STORY_FILES=$(git diff --cached --name-only --diff-filter=d | grep '\.story\.md$' | grep -v '^tests/' || true)
fi
```

**Usage Pattern:**
```bash
# Scoped commit (validates only STORY-114)
DEVFORGEAI_STORY=STORY-114 git commit -m "feat(STORY-114): implement checkpoint protocol"

# Unscoped commit (validates ALL staged story files - backward compatible)
git commit -m "chore: update documentation"
```

**Acceptance Criteria Themes:**
- AC#1: `DEVFORGEAI_STORY=STORY-XXX` environment variable scopes validation to that story only
- AC#2: If env var unset, validate all staged story files (backward compatible)
- AC#3: Clear console message: "Scoped to: STORY-XXX" when scoping active
- AC#4: Pre-commit hook template in install_hooks.sh updated with scoping logic
- AC#5: User documentation explains when and how to use scoped commits

### Feature 3: Line Ending Normalization (STORY-122)
**Description:** Create `.gitattributes` with LF normalization to prevent CRLF/LF inconsistencies on WSL.

**User Stories (high-level):**
1. As a developer, I want text files auto-normalized to LF
2. As a developer, I want shell scripts explicitly LF to prevent WSL issues
3. As a developer, I want binary files excluded from normalization

**Estimated Effort:** 3 story points

**Files to Create/Modify:**
| Action | File Path | Purpose |
|--------|-----------|---------|
| CREATE | `.gitattributes` | Line ending normalization rules |

**File Content (.gitattributes):**
```gitattributes
# Auto-detect text files and normalize to LF
* text=auto eol=lf

# Shell scripts must use LF (critical for WSL)
*.sh text eol=lf

# Python files
*.py text eol=lf

# Markdown files
*.md text eol=lf

# JSON/YAML config files
*.json text eol=lf
*.yaml text eol=lf
*.yml text eol=lf

# TypeScript/JavaScript
*.ts text eol=lf
*.tsx text eol=lf
*.js text eol=lf
*.jsx text eol=lf

# Binary files (no normalization)
*.png binary
*.jpg binary
*.jpeg binary
*.gif binary
*.ico binary
*.pdf binary
*.zip binary
*.tar binary
*.gz binary
```

**Post-Creation Command:**
```bash
# Renormalize existing files after .gitattributes is added
git add --renormalize .
git commit -m "chore: normalize line endings to LF"
```

**Acceptance Criteria Themes:**
- AC#1: `.gitattributes` file created at project root
- AC#2: All text files auto-normalize to LF on commit
- AC#3: Shell scripts (.sh) explicitly set to LF (prevents WSL execution errors)
- AC#4: Binary files (images, archives) marked as binary (no normalization)
- AC#5: Existing repository files can be renormalized with `git add --renormalize .`

### Feature 4: Uncommitted Story File Warning (STORY-123)
**Description:** Add story-specific conflict detection to preflight validation, distinguishing "your story" vs "other stories" with clear guidance.

**User Stories (high-level):**
1. As a developer, I want warnings when uncommitted story files exist
2. As a developer, I want to distinguish my story from other stories
3. As a developer, I want option to focus on current story using scoping

**Estimated Effort:** 3 story points

**Depends On:** STORY-121 (uses DEVFORGEAI_STORY scoping concept)

**Files to Create/Modify:**
| Action | File Path | Purpose |
|--------|-----------|---------|
| MODIFY | `.claude/skills/devforgeai-development/references/preflight-validation.md` | Add Step 1.8: Story File Isolation Check |

**New Preflight Step (Step 1.8):**
```markdown
## Step 1.8: Story File Isolation Check

**Purpose:** Warn developer when uncommitted story files exist that may conflict with current work.

**Implementation:**
1. Get current story ID from `/dev` argument
2. Query uncommitted story files: `git status --porcelain | grep '\.story\.md$'`
3. Separate into: current_story vs other_stories
4. If other_stories.count > 0, display warning

**Warning Display:**
+---------------------------------------------------------------+
|  WARNING: UNCOMMITTED STORY FILES DETECTED                    |
+---------------------------------------------------------------+
|                                                               |
|  Your story: STORY-114 (will be modified by this /dev run)    |
|                                                               |
|  Other uncommitted stories: 21 files                          |
|    - STORY-100 through STORY-113 (14 files)                   |
|    - STORY-115 through STORY-119 (7 files)                    |
|                                                               |
|  Impact:                                                      |
|    - Git commits will include ONLY your story (scoped)        |
|    - Pre-commit validation will focus on STORY-114            |
|    - Other story files remain uncommitted                     |
|                                                               |
+---------------------------------------------------------------+

**User Options:**
AskUserQuestion:
  question: "How do you want to proceed?"
  options:
    - "Continue with scoped commits (recommended)"
    - "Commit other stories first (I'll do this manually)"
    - "Show me the list of uncommitted files"
```

**Acceptance Criteria Themes:**
- AC#1: Preflight detects uncommitted `.story.md` files via `git status`
- AC#2: Current story distinguished from other stories in warning display
- AC#3: Count and range of other uncommitted stories shown (e.g., "STORY-100 through STORY-113")
- AC#4: User prompted with options: continue scoped, commit first, show list
- AC#5: Integration with STORY-121 scoping (automatically sets DEVFORGEAI_STORY for commits)

### Feature 5: WSL Test Execution Documentation (STORY-124)
**Description:** Add WSL testing section to coding standards with path handling, common issues, and test commands.

**User Stories (high-level):**
1. As a developer, I want documented pytest execution patterns on WSL
2. As a developer, I want common WSL test failures documented with fixes
3. As a developer, I want path conversion guidance (C: vs /mnt/c/)

**Estimated Effort:** 2 story points

**Files to Create/Modify:**
| Action | File Path | Purpose |
|--------|-----------|---------|
| MODIFY | `devforgeai/specs/context/coding-standards.md` | Add WSL Testing section |

**Content to Add (## WSL Test Execution):**
```markdown
## WSL Test Execution

### Path Handling
- Use `/mnt/c/` paths in WSL, not `C:\`
- pytest discovers tests from Unix-style paths
- Coverage reports use Unix paths
- Example: `/mnt/c/Projects/DevForgeAI2/tests/` not `C:\Projects\DevForgeAI2\tests\`

### Environment Setup
```bash
# From WSL terminal
cd /mnt/c/Projects/DevForgeAI2
export PYTHONPATH=".:$PYTHONPATH"
```

### Common Issues and Fixes

| Issue | Cause | Fix |
|-------|-------|-----|
| "Module not found" | PYTHONPATH not set | `export PYTHONPATH=".:$PYTHONPATH"` |
| Permission denied on .sh | Windows file locks | Close file in other programs, or `chmod +x script.sh` |
| Line ending errors (`$'\r': command not found`) | CRLF in shell scripts | `dos2unix script.sh` or `sed -i 's/\r$//' script.sh` |
| Slow file operations | Windows filesystem overhead | Run tests from WSL native filesystem if possible |
| pytest not found | Virtual env not activated | `source venv/bin/activate` or `pip install pytest` |

### Test Commands
```bash
# Run all tests
pytest tests/ -v

# Run specific test file
pytest tests/test_validators.py -v

# Run with coverage
pytest tests/ --cov=src --cov-report=term-missing

# Run single test
pytest tests/test_validators.py::test_dod_validation -v
```

### Shell Script Testing
```bash
# Always run shell scripts with bash, not direct execution
bash path/to/test.sh          # Correct
./path/to/test.sh             # May fail on WSL mounts

# Fix line endings before running
dos2unix path/to/test.sh && bash path/to/test.sh
```
```

**Acceptance Criteria Themes:**
- AC#1: Path handling section documents `/mnt/c/` vs `C:\` conversion
- AC#2: Common issues table with Issue/Cause/Fix columns
- AC#3: Test command examples for pytest, coverage, single tests
- AC#4: Shell script execution guidance (use `bash script.sh` not `./script.sh`)
- AC#5: Environment setup commands documented (PYTHONPATH, venv)

## Requirements Summary

### Functional Requirements

| ID | Requirement | Priority | Story |
|----|-------------|----------|-------|
| FR-1 | Checkpoint file written at each TDD phase completion | CRITICAL | STORY-120 |
| FR-2 | /resume-dev reads checkpoint for auto-detection | HIGH | STORY-120 |
| FR-3 | DEVFORGEAI_STORY env var scopes validation | HIGH | STORY-121 |
| FR-4 | .gitattributes normalizes line endings to LF | MEDIUM | STORY-122 |
| FR-5 | Preflight warns about uncommitted story files | MEDIUM | STORY-123 |
| FR-6 | coding-standards.md includes WSL section | LOW | STORY-124 |

### Non-Functional Requirements

| ID | Requirement | Target | Story |
|----|-------------|--------|-------|
| NFR-1 | Checkpoint write latency | <100ms | STORY-120 |
| NFR-2 | Checkpoint file size | <10KB | STORY-120 |
| NFR-3 | Pre-commit overhead | <500ms additional | STORY-121 |
| NFR-4 | Backward compatibility | 100% when env var unset | STORY-121 |

## Technical Approach

### Checkpoint Architecture
```
devforgeai/sessions/
  STORY-120/
    checkpoint.json    # Current phase, progress, DoD status
  STORY-121/
    checkpoint.json
```

### Pre-Commit Modification
```bash
if [ -n "$DEVFORGEAI_STORY" ]; then
    STORY_FILES=$(git diff --cached --name-only | grep "${DEVFORGEAI_STORY}")
else
    STORY_FILES=$(git diff --cached --name-only | grep '\.story\.md$')
fi
```

## Dependencies

- None external
- STORY-123 depends on STORY-121 (uses scoping concept)

## Risks & Mitigations

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| Checkpoint file bloat | Low | Medium | Auto-cleanup on story completion, 7-day retention |
| Line ending migration creates large diff | Medium | Low | Separate commit, document for team |
| Environment variable collision | Low | Low | Unique prefix DEVFORGEAI_ |

## Sprint Allocation

**Sprint-8 (21 points):**
- STORY-120: Session Checkpoint Protocol (8 pts)
- STORY-121: Story-Scoped Pre-Commit Validation (5 pts)
- STORY-122: Line Ending Normalization (3 pts)
- STORY-123: Uncommitted Story File Warning (3 pts)
- STORY-124: WSL Test Execution Documentation (2 pts)

## Definition of Done

### Epic-Level Completion Criteria
- [ ] All 5 stories reach Released status
- [ ] Checkpoint protocol tested across context window fills
- [ ] Pre-commit scoping tested with multiple staged stories
- [ ] Line ending normalization applied to repository
- [ ] WSL documentation validated on Windows/WSL environment

---

## Stories Summary

| Story | Title | Points | Priority | Status | File |
|-------|-------|--------|----------|--------|------|
| STORY-120 | Session Checkpoint Protocol | 8 | Critical | Backlog | [STORY-120](../Stories/STORY-120-session-checkpoint-protocol.story.md) |
| STORY-121 | Story-Scoped Pre-Commit Validation | 5 | High | Backlog | [STORY-121](../Stories/STORY-121-story-scoped-pre-commit-validation.story.md) |
| STORY-122 | Line Ending Normalization | 3 | Medium | Backlog | [STORY-122](../Stories/STORY-122-line-ending-normalization.story.md) |
| STORY-123 | Uncommitted Story File Warning | 3 | Medium | Backlog | [STORY-123](../Stories/STORY-123-uncommitted-story-file-warning.story.md) |
| STORY-124 | WSL Test Execution Documentation | 2 | Low | Backlog | [STORY-124](../Stories/STORY-124-wsl-test-execution-documentation.story.md) |

**Total Points:** 21 | **Sprint:** Sprint-8 | **Dependencies:** STORY-123 → STORY-121
