# Git Workflow Conventions Reference

Phase 08/9 Git Workflow & Commit conventions for TDD development process.

---

## Phase Progress Indicator

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Phase 08/9: Git Workflow & Commit (78% → 89% complete)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**Display this indicator at the start of Phase 08 execution.**

---

## Phase 08.0: Pre-Commit DoD Validation [MANDATORY - RCA-014 REC-3]

**Execute BEFORE any git operations.** Defense-in-depth even if Phase 06 has bugs or is skipped.

### Detect Incomplete DoD Items

```
Grep(
  pattern="^- \[ \]",
  path="${STORY_FILE}",
  output_mode="content",
  -B=1
)
```

**Filter to Definition of Done section only:**

```
unchecked_dod_items = []

FOR each match:
  preceding_line = previous line (via -B=1)
  item_text = current line

  # Track section boundaries
  IF preceding_line contains "## Definition of Done": in_dod_section = true
  IF preceding_line contains any of ["## Acceptance Criteria", "## Workflow Status",
     "## Implementation Notes", "### AC#", "Checklist"]: in_dod_section = false

  IF in_dod_section AND item_text starts with "- [ ]":
    unchecked_dod_items.append(item_text)
```

### Check for User Approval

```
IF unchecked_dod_items.length > 0:
  Grep(pattern="### Approved Deferrals", path="${STORY_FILE}", output_mode="files_with_matches")

  IF "Approved Deferrals" section NOT found:
    Display: "PHASE 5 BLOCKED: Incomplete DoD Without Approval"
    Display: "Found {unchecked_dod_items.length} unchecked DoD items:"
    FOR each item: Display: "  - {item}"

    Display: "DIAGNOSIS: Should have been caught in Phase 06 (Deferral Challenge)."
    Display: "Possible causes:"
    Display: "  1. Phase 06 was skipped (workflow bug)"
    Display: "  2. User approved deferrals but approval not documented"
    Display: "  3. DoD was manually edited after Phase 06"
    Display: "  4. Phase 06 detection has bug"

    Display: "RESOLUTION OPTIONS:"
    Display: "  1. Investigate: /rca 'Phase 08 blocked - unchecked DoD items without approval'"
    Display: "  2. Get user approval: Add '### Approved Deferrals' to Implementation Notes"
    Display: "  3. Complete the work: Implement missing DoD items, mark [x], re-run /dev"

    HALT workflow - EXIT Phase 08 with status code 1

  ELSE:
    Display: "Pre-Commit Validation: Unchecked DoD items found BUT user approval documented - PASS"

ELSE:
  Display: "Pre-Commit Validation: All DoD items complete (100%) - PASS"
```

**Success Criteria:**
- Validation runs BEFORE any git operations
- Detects ALL unchecked DoD items
- Allows unchecked items IF "Approved Deferrals" section exists
- BLOCKS commit if unchecked items WITHOUT approval
- Does NOT block on AC Checklist unchecked items

---

## Pre-Requisites for Phase 08 (Git Workflow)

**CRITICAL:** Before executing git commit workflow, ensure DoD format is correct.

### Phase 06-5 Bridge Workflow

**Load and execute:**
```
Read(file_path="references/dod-update-workflow.md")
```

**Bridge workflow ensures:**
- [ ] All completed DoD items marked [x] in Definition of Done section
- [ ] All completed DoD items added to Implementation Notes (FLAT LIST - no ### subsections)
- [ ] devforgeai-validate validate-dod passes (exit code 0)
- [ ] Workflow Status section updated

**Common failure:** Placing DoD items under `### Definition of Done Status` subsection (validator's `extract_section()` stops at ### headers, doesn't see items)

**See:** `dod-update-workflow.md` for detailed format requirements

---

## Phase 08.0.5: Lock Coordination for Parallel Commits [STORY-096]

**Purpose:** Serialize git commits across parallel story worktrees to prevent git index lock conflicts.

```
Read(file_path="references/lock-file-coordination.md")
```

**Execute Steps 5.0.1 through 5.0.4:**

1. **Step 5.0.1:** Acquire `devforgeai/.locks/git-commit.lock`
2. **Step 5.0.2:** Wait with progress display if lock held (AC#2)
3. **Step 5.0.3:** Auto-remove stale locks (PID dead + age > 5 min) (AC#3)
4. **Step 5.0.4:** Prompt user if timeout exceeds 10 minutes (AC#4)

**Success Criteria:** Lock acquired (or timeout handled), lock file contains PID/story_id/timestamp/hostname, stale locks auto-removed.

**Failure Modes:**
- **ABORT:** User chose abort at timeout prompt -> Clean exit, changes preserved
- **HALT:** Lock acquisition failed unexpectedly -> Error message with recovery steps

**Proceed to git add/commit ONLY after lock acquired successfully.**

---

## AC Verification Checklist Updates (Phase 08) [RCA-011]

**Execution:** After git commit succeeds, before Phase 09

```
Read(file_path="references/ac-checklist-update-workflow.md")
```

**Identify Phase 08 AC Items:**
```
Grep(pattern="Phase.*: 5", path="${STORY_FILE}", output_mode="content", -B=1)
```

**Common Phase 08 items:** Git commit created, story status updated, backward compatibility verified, deployment readiness confirmed, integration notes documented.

**Batch-update all Phase 08 items after commit succeeds.**

**Display:** Final checklist summary showing all phases (02-08) with item counts and 100% completion.

---

## Git Stash Safety Protocol (RCA-008)

**CRITICAL RULE:** Never stash files without user consent and clear warnings.

**Incident:** RCA-008 - Autonomous git stash hid 21 user-created story files without consent.

### Prohibited Actions

**NEVER:** `git stash push --include-untracked` without warning or consent.

**ALWAYS:**
1. Show user what will be stashed (file list with categories)
2. Display warning about file visibility consequences
3. Get explicit confirmation via AskUserQuestion
4. Execute stash only if user confirms
5. Display recovery instructions immediately after stashing

### Stash Warning Template

When user chooses to stash, display warning box explaining:
- What git stash does (temporarily hides files from filesystem)
- Count of untracked files that will be hidden
- Recovery commands (`git stash pop`, `git stash apply`)

**Then require double confirmation via AskUserQuestion with options:**
1. "Yes, stash them (I understand they'll be hidden)"
2. "No, continue without stashing instead"
3. "No, let me commit them first"

### After Stashing - ALWAYS Display Recovery Instructions

```
After stashing, display:
  "Stashed {total_files} files to stash@{0}"
  "To restore: git stash pop"
```

### Untracked Files Special Handling

If stashing untracked files (--include-untracked):
1. Count untracked files: `git status --short | grep "^??" | wc -l`
2. Show first 10 untracked files
3. Highlight story files if present: `git status --short | grep "^??" | grep "STORY-"`
4. Require double confirmation (strategy selection + warning confirmation)

---

## Smart Stash Strategy (RCA-008)

### Strategy Matrix

| File Status | Tracked | Stash Command | Risk | Recommendation |
|-------------|---------|---------------|------|----------------|
| Modified (M) | Yes | Default `git stash` | LOW | **Stash** |
| Untracked (??) | No | Needs `--include-untracked` | HIGH | **Keep visible** |
| Deleted (D) | Yes | Default `git stash` | LOW | Stash |
| Added (A) | Yes | Default `git stash` | MEDIUM | Stash or keep |

### Three Strategies

**Strategy 1: Stash Modified Only (DEFAULT - RECOMMENDED)**
```bash
git stash push -m "WIP: Modified files only"
# Modified (M) -> Stashed | Untracked (??) -> Remain visible
```
Use when: User has untracked files (especially story files). DEFAULT in Phase 01.1.5.

**Strategy 2: Stash Everything (USE WITH CAUTION)**
```bash
git stash push -m "WIP: All files" --include-untracked
# Requires: Steps 0.1.5 and 0.1.6 user consent workflow
```
Use when: User explicitly requests after seeing full warning, all files are regenerable.

**Strategy 3: File-Based Tracking (SAFEST)**
```bash
# No git commands. Changes tracked in devforgeai/stories/{STORY-ID}/changes/
```
Use when: User wants all files visible, declines git operations, no git repo available.

### Strategy Selection Decision Tree

```
Uncommitted changes?
  NO -> Proceed with clean workflow
  YES -> Untracked files?
    NO (only modified) -> Stash modified files (safe)
    YES -> What type?
      Story files / User-created -> Keep visible OR Commit first
      Cache / Build artifacts -> OK to stash all
      Mixed -> Stash modified only, keep untracked visible (default)
```

### Implementation in Phase 01.1.5

Options in order of safety:
1. **Continue anyway** - File-based tracking (safest)
2. **Stash ONLY modified** - Recommended
3. **Show files first** - Review before deciding
4. **Commit first** - Creates proper git history
5. **Stash ALL** - Use with caution (requires Phase 01.1.6 warning)

---

## Lock File Recovery

### Problem

Git fails with: `fatal: Unable to create '.git/index.lock': File exists`

### Recovery

```bash
# Check for running git processes first
ps aux | grep git

# Only if no git processes running:
rm -f .git/index.lock
```

### WSL2-Specific Notes

**Common Causes:** VS Code Git extension polling, cross-filesystem access (Windows/WSL), previous git crash, filesystem sync issues.

**Prevention:**
1. Close VS Code Git panels before terminal git operations
2. Use native WSL paths (`/mnt/c/`) not Windows paths (`C:\`)
3. Avoid running git from both Windows and WSL on same repo
4. Disable "Git: Autofetch" temporarily

**Alternative (if rm fails):**
```bash
rm -rf .git/index.lock 2>/dev/null || cmd.exe /c "del /f /q .git\\index.lock"
```

---

## Branch Naming Conventions

| Type | Pattern | Example |
|------|---------|---------|
| Feature | `feature/[STORY-ID]-[brief-description]` | `feature/STORY-042-checkout-optimization` |
| Bugfix | `bugfix/[STORY-ID]-[brief-description]` | `bugfix/BUG-028-cart-calculation-error` |
| Hotfix | `hotfix/[description]` | `hotfix/HOTFIX-001-payment-gateway-failure` |
| Release | `release/v[MAJOR].[MINOR].[PATCH]` | `release/v1.2.0` |

**Rules:**
- Always include story/epic ID when available
- Lowercase with hyphens
- Keep description brief (2-4 words)
- Feature branches from main/development; hotfix from production/main

---

## Conventional Commit Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Commit Types

| Type | Usage |
|------|-------|
| **feat** | New feature |
| **fix** | Bug fix |
| **refactor** | Code change (no behavior change) |
| **test** | Adding or updating tests |
| **docs** | Documentation changes |
| **style** | Code formatting (no logic change) |
| **chore** | Build, dependencies, tooling |
| **perf** | Performance improvements |
| **ci** | CI/CD changes |
| **build** | Build system changes |
| **revert** | Revert previous commit |

### DevForgeAI Commit Message Template

**Using heredoc for multi-line messages (use `<<'EOF'` to prevent variable expansion):**

```bash
git commit -m "$(cat <<'EOF'
feat(module): Brief description of feature

- Implemented <functionality>
- Added <components>
- Tests: <count> unit tests, <count> integration tests
- Compliance: tech-stack.md, coding-standards.md
- Coverage: <percentage>%

Closes #STORY-XXX
EOF
)"
```

### Templates by Type

**fix:**
```
fix(module): Brief description of bug

- Fixed <issue>
- Root cause: <explanation>
- Added regression test
- Coverage: <percentage>%

Fixes #BUG-XXX
```

**refactor:**
```
refactor(module): Brief description

- Extracted <method/class>
- No behavior changes
- All tests still passing (100%)

Part of #STORY-XXX refactoring phase
```

**test:**
```
test(module): Brief description

- Added tests for <scenarios>
- Edge cases: <list>
- Coverage increased from X% to Y%

Part of #STORY-XXX TDD cycle
```

**Breaking change (add BREAKING CHANGE in body):**
```
feat(api): Change order creation endpoint contract

BREAKING CHANGE: Order creation now requires customerId in request body

- Updated POST /api/orders to require customerId
- Migration guide added to docs/migration/v2.0.md

Closes #STORY-050
```

---

## Commit Timing in TDD Workflow

### Option 1: Single Commit Per Story (Recommended)

After Phase 08 integration completes. One commit = one story. Clean history, easy revert.

```bash
# Phase 08.0.5: Acquire lock (STORY-096)
python3 src/lock_file_coordinator.py acquire --story-id STORY-001 --timeout 600

# Stage and commit (with lock held)
git add src/ tests/
git commit -m "$(cat <<'EOF'
feat: Implement order discount calculation

- Implemented CalculateDiscount method following TDD
- Tests: 15 unit tests, 3 integration tests
- Coverage: 95% for OrderService
- Compliance: tech-stack.md, coding-standards.md

Closes #STORY-001
EOF
)"

# Release lock (STORY-096) - always release, even on failure
python3 src/lock_file_coordinator.py release --story-id STORY-001

git push origin feature/STORY-001-order-discounts
```

### Option 2: Multiple Commits Per TDD Phase

For complex stories. Shows RED->GREEN->REFACTOR progression.

```bash
# After Phase 02 (RED):   test: Add failing tests for ...  Part of #STORY-001
# After Phase 03 (GREEN): feat: Implement ... (Green phase) Part of #STORY-001
# After Phase 04:         refactor: Improve ... code quality Part of #STORY-001
# After Phase 08:         feat: Complete ... feature         Closes #STORY-001
```

### Option 3: Hybrid Approach

Multiple checkpoint commits, squash before merging to main.

**Recommended: Option 1 (Single Commit Per Story)** - matches DevForgeAI story-driven development.

---

## Staging Strategy

**Always stage explicitly by path. Never use `git add .` or `git add -A` in multi-story working trees.**

### What to Exclude

Never stage: `.env`, secrets, IDE configs, build artifacts, temporary files.

---

## Selective Staging for Parallel Stories

When multiple stories are in progress in the same working tree, use selective staging.

### Pattern-Based Staging

```bash
# Stage only files for a specific story
git add devforgeai/specs/Stories/STORY-XXX-*.story.md
git add devforgeai/workflows/STORY-XXX-phase-state.json
git add tests/STORY-XXX/
git add .claude/skills/implementing-stories/references/target-file.md
git add devforgeai/feedback/ai-analysis/STORY-XXX/
```

### Verification Before Commit

```bash
# List staged files - confirm only current story files
git diff --cached --name-only

# Unstage files that don't belong
git reset HEAD devforgeai/workflows/STORY-OTHER-phase-state.json
git reset HEAD tests/STORY-OTHER/
```

### Anti-Pattern: Broad Staging in Multi-Story Trees

**FORBIDDEN in parallel development:**
```bash
git add .       # Stages ALL changes including other stories
git add -A      # Same problem
git add --all   # Same problem
```

**Safe alternatives:** Stage by explicit path, use story-specific glob patterns, or use `git add -p`.

### When to Use Worktrees Instead

Recommend worktrees when stories touch many shared files, multiple developers work simultaneously, or selective staging becomes tedious.

```bash
git worktree add ../STORY-XXX-worktree -b feature/STORY-XXX
git worktree list
git worktree remove ../STORY-XXX-worktree
```

---

## Push Timing

**Push when:** All tests passing, QA validation passed, ready for review.
**Never push:** Failing tests, commented-out code, secrets, incomplete implementation (unless draft PR).

**First push:** `git push -u origin feature/STORY-XXX-description`
**Force push (feature branches only):** `git push --force-with-lease origin feature/STORY-XXX`
**NEVER force push to shared branches (main, development).**

---

## Git Hooks Integration

### Pre-Commit Hook

Validates: linting, secret detection, quick tests.

### Commit-Msg Hook

Validates: conventional commit format, subject line <= 100 characters.

### Pre-Push Hook

Validates: full test suite, code coverage thresholds.

---

## Branch Management

### Merging Strategies

| Strategy | Use Case | Command |
|----------|----------|---------|
| **Squash and Merge** (recommended) | Feature branches to main | `git merge --squash feature/STORY-XXX` |
| **Merge Commit** | Long-running branches | `git merge feature/STORY-XXX --no-ff` |
| **Rebase and Merge** | Clean linear history | `git rebase main` then `git merge --ff-only` |

### Branch Cleanup After Merge

```bash
git branch -d feature/STORY-XXX        # Delete local
git push origin --delete feature/STORY-XXX  # Delete remote
```

---

## Git Workflow Checklists

### Pre-Commit
- [ ] All tests passing
- [ ] Build succeeds
- [ ] No debug code or secrets
- [ ] Commit message follows conventions
- [ ] Only relevant files staged

### Pre-Push
- [ ] Full test suite passing
- [ ] Coverage meets thresholds (95%/85%/80%)
- [ ] No force push to shared branches
- [ ] Branch up to date with main

### Pre-Merge
- [ ] All CI checks passing
- [ ] Code review approved
- [ ] No merge conflicts
- [ ] Documentation updated
