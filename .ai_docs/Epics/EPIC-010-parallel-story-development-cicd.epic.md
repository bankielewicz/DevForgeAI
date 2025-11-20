---
id: EPIC-010
title: Parallel Story Development with CI/CD Integration
status: Planning
start_date: 2026-01-20
target_date: 2026-03-20
total_points: 65
completed_points: 0
owner: Framework Maintainer
tech_lead: TBD
created: 2025-11-16
updated: 2025-11-16
complexity_score: 42
architecture_tier: 3
new_subagents: 2
enhanced_subagents: 1
new_skills: 1
modified_skills: 2
new_commands: 2
modified_commands: 2
---

# EPIC-010: Parallel Story Development with CI/CD Integration

## Business Goal

Enable DevForgeAI framework to support concurrent story development across multiple terminals and CI/CD environments, eliminating sequential execution bottlenecks while preserving zero-debt quality gates and maintaining backward compatibility with existing workflows.

**Current State Problem:**
- DevForgeAI supports only sequential story execution (one /dev at a time)
- Multiple developers cannot work concurrently without file system collisions
- Test outputs overwrite each other (TestResults/, coverage/)
- Git operations race (commits, branch creation)
- Build artifacts collide (bin/, obj/, dist/)
- No CI/CD automation (GitHub Actions cannot run /dev, /qa headlessly)
- Time-to-completion bottleneck (8 stories × 8 hours = 64 hours sequential)

**Target State Solution:**
- Support 2-8 concurrent story developments using Git worktrees (complete file system isolation)
- Story-scoped test outputs prevent collisions (TestResults/{story_id}/)
- Strict dependency enforcement with full transitive graph support (A→B→C)
- File overlap detection (hybrid: spec-based pre-flight + git-based post-flight)
- Auto-managed worktrees (create on /dev, cleanup after 7 days + prompt)
- New /worktrees command for visibility and management
- Backward compatible (existing /dev workflow unchanged, parallel is default-ready)
- Optional GitHub Actions integration (Phase 2 - headless mode + CI/CD workflows)

## Success Metrics

1. **Parallel Capacity:** Support 2-5 concurrent story developments without collisions (MVP: 2, Target: 5)
2. **Time-to-Completion:** 8 stories complete in ~16 hours wall-clock (50% reduction from 64 hours sequential)
3. **Zero Quality Degradation:** 100% of quality gates preserved (coverage thresholds, TDD, deferral validation unchanged)
4. **Dependency Accuracy:** 100% dependency violations detected (no stories proceed with unmet dependencies)
5. **File Collision Prevention:** Zero file overwrites or conflicts from parallel execution (test outputs, build artifacts)
6. **Backward Compatibility:** 100% existing /dev behavior preserved (no breaking changes to single-story workflow)
7. **Disk Space Efficiency:** <500MB total for 3-5 worktrees (auto-cleanup prevents exhaustion)
8. **Adoption Rate:** 80%+ of multi-story development uses parallel capability within 3 months of release

## Timeline

**Total Duration:** 8 weeks (2 months, starting 2026-01-20 after EPIC-009 completes)

**Phase 1 - MVP: Local Parallel Development (6 weeks)**
- Week 1-2: Worktree management + test isolation
- Week 3-4: Dependency enforcement + overlap detection
- Week 5-6: Cleanup automation + /worktrees command

**Phase 2 - CI/CD Integration (2 weeks, optional based on MVP success)**
- Week 7: GitHub Actions workflows + headless configuration
- Week 8: Testing, documentation, team onboarding

**Go/No-Go Checkpoint:** After Week 6 (MVP complete)
- Criteria: 2 concurrent stories work without collisions, quality gates preserved, dependency enforcement validated
- Decision: Proceed to Phase 2 (CI/CD) OR iterate on MVP OR ship MVP and defer Phase 2

**Target Completion:** 2026-03-17 (8 weeks from start)

## Priority

**High** - Enables team scaling and faster delivery while maintaining DevForgeAI's zero-debt philosophy.

**Justification:**
- **Blocker for team growth:** Cannot onboard 2+ developers without parallel capability
- **Competitive advantage:** AI-assisted parallel development is differentiator for DevForgeAI
- **Foundation for automation:** CI/CD integration (Phase 2) requires parallel infrastructure (Phase 1)
- **Research validated:** Internet-sleuth confirmed feasibility ($0.08-$0.12 per story, proven patterns)
- **User demand:** Solo dev future-proofing indicates awareness of scaling need

## Features

### Phase 1: MVP - Local Parallel Development (6 features)

#### 1. Git Worktree Auto-Management (8 points)

**Description:** Automatically create Git worktrees for story development on /dev invocation, with hybrid cleanup strategy (auto-delete after 7 days idle + manual prompt on next /dev).

**User Story:**
As a DevForgeAI developer,
I want /dev to automatically create a Git worktree for each story,
So that I can develop multiple stories in parallel without file system collisions or manual worktree management.

**Complexity:** Medium (6/10)
- Git worktree API integration
- Auto-create on /dev Phase 0
- Cleanup detection (7-day idle threshold, configurable)
- Prompt on next /dev if old worktrees exist
- Manual cleanup command integration

**Acceptance Criteria:**
- AC1: Running /dev STORY-037 creates ../devforgeai-story-037/ worktree automatically
- AC2: Worktree idle >7 days flagged for cleanup (checked on next /dev)
- AC3: Prompt offers: Resume, Fresh Start, Delete Old
- AC4: Worktree creation takes <10 seconds
- AC5: Cleanup threshold configurable in .devforgeai/config/parallel.yaml (deployed from src/devforgeai/config/parallel.yaml.example)

**Dependencies:** None (foundational feature)

**Deliverables:**
- **Subagent:** git-worktree-manager (enhanced from git-validator, ~450 lines) in src/claude/agents/
- Worktree manager module (Python or Bash) in src/claude/scripts/ or skill references
- **Config template:** src/devforgeai/config/parallel.yaml.example (defaults: 7-day cleanup, 5 max worktrees)
- **Operational config:** .devforgeai/config/parallel.yaml (created by installer from template)
- Auto-create logic in src/claude/skills/devforgeai-development/ (Phase 0 enhancement)
- Cleanup prompt in /dev command (Phase 0)
- Documentation: Git worktrees for parallel development

**Subagent:** **git-worktree-manager** (ENHANCED from git-validator)
- **Responsibilities:** Create worktrees, detect idle worktrees (>7 days), calculate disk usage, cleanup validation, status reporting
- **Model:** haiku (fast Git operations)
- **Tools:** Bash (git worktree commands), Read, Grep
- **Token Target:** <10K
- **Reusability:** High (any Git worktree workflow)

**Risk:** Medium - Git worktree API must work across platforms (Linux, macOS, WSL)

---

#### 2. Story-Scoped Test Isolation (5 points)

**Description:** Implement story-scoped test output directories (TestResults/{story_id}/, coverage/{story_id}/, logs/{story_id}/) to prevent concurrent test execution from overwriting results.

**User Story:**
As a DevForgeAI developer running /qa on multiple stories,
I want test outputs isolated per story,
So that concurrent QA validations don't overwrite each other's results and I can review results independently.

**Complexity:** Low (4/10)
- Test framework configuration (pytest, jest, dotnet test)
- Output directory parameterization
- QA report path updates
- Coverage aggregation per story

**Acceptance Criteria:**
- AC1: /dev STORY-037 runs tests with --results-directory=tests/results/STORY-037/
- AC2: /qa STORY-038 (concurrent) writes to tests/results/STORY-038/ (no collision)
- AC3: Coverage reports isolated: tests/coverage/STORY-037/coverage.xml, tests/coverage/STORY-038/coverage.xml
- AC4: QA reports reference correct test output paths (tests/results/{story_id}/)
- AC5: Test isolation works for pytest, jest, dotnet test, go test

**Dependencies:** Feature 1 (worktrees provide file system isolation)

**Deliverables:**
- Test configuration updates in src/claude/skills/devforgeai-development/ (Phase 2) and src/claude/skills/devforgeai-qa/ (Phase 1)
- **Config template:** src/devforgeai/config/test-isolation.yaml.example
- **Operational config:** .devforgeai/config/test-isolation.yaml (created by installer)
- Documentation: Story-scoped testing guide

**Risk:** Low - Standard test framework feature, well-documented

---

#### 3. Dependency Graph Enforcement with Transitive Resolution (13 points)

**Description:** Implement strict dependency enforcement using story YAML depends_on field + epic-level dependency definitions, with full transitive dependency graph resolution (A→B→C) and cascade blocking when dependencies fail.

**User Story:**
As a DevForgeAI framework user defining story dependencies,
I want the framework to enforce dependency order with transitive resolution and block dependent stories when dependencies fail,
So that I never develop STORY-038 (Product) before STORY-037 (User) completes and quality is maintained.

**Complexity:** High (8/10)
- YAML schema update (depends_on field in story template)
- Epic-level dependency inheritance (features → stories)
- Transitive dependency graph builder (A→B→C resolution)
- Cascade block logic (failed dependency blocks all downstream)
- Circular dependency detection (prevent A→B→A)
- Developer bypass mechanism (--force flag with warning)

**Acceptance Criteria:**
- AC1: Story YAML supports depends_on: [STORY-037, STORY-039] (array of story IDs)
- AC2: /dev STORY-038 checks dependencies, blocks if STORY-037 status ≠ Dev Complete or QA Approved
- AC3: Epic defines feature dependencies, stories inherit (Feature 2 → Feature 1 becomes STORY-038 → STORY-037)
- AC4: Transitive resolution: STORY-040 → STORY-039 → STORY-037 enforces 037 completes first
- AC5: Circular dependency detection: STORY-037 → STORY-038 → STORY-037 fails with error
- AC6: /dev STORY-038 --force bypasses dependency check (logs warning)
- AC7: Failed dependency (STORY-037 status=QA Failed) blocks STORY-038 with message: "Dependency STORY-037 failed QA, resolve before proceeding"

**Dependencies:** None (can implement independently)

**Deliverables:**
- **Subagent:** dependency-graph-analyzer (NEW, ~400 lines)
- Dependency graph builder (Python module)
- Story template updated (depends_on field in YAML)
- Epic template updated (feature dependency section)
- /dev Phase 0 pre-flight dependency validation
- Circular dependency detector
- Documentation: Story dependency management guide

**Subagent:** **dependency-graph-analyzer** (NEW)
- **Responsibilities:** Parse depends_on YAML, build transitive dependency graph (A→B→C), detect circular dependencies, validate dependency status, cascade blocking logic
- **Model:** haiku (fast graph algorithms)
- **Tools:** Read, Grep, Glob (story files)
- **Token Target:** <15K
- **Reusability:** High (epic-level dependencies, sprint planning, future dependency features)

**Risk:** High - Complex graph algorithms, edge cases (circular, cascade failures)

---

#### 4. File Overlap Detection with Hybrid Analysis (8 points)

**Description:** Implement hybrid file overlap detection (spec-based pre-flight analysis + git-based post-flight validation) to warn developers when concurrent stories modify overlapping files.

**User Story:**
As a DevForgeAI developer,
I want automatic detection when two parallel stories will modify the same files,
So that I can make informed decisions about parallelization safety and avoid merge conflicts.

**Complexity:** Medium (6/10)
- Spec parser (extract file_path from technical_specification YAML)
- Git diff analyzer (compare actual file changes across worktrees)
- Overlap detection algorithm (set intersection)
- Warning UI (display overlapping files with options)

**Acceptance Criteria:**
- AC1: Pre-flight check: Parse STORY-037 and STORY-038 specs, extract file_path fields, detect overlap (e.g., both list src/User.cs)
- AC2: Display warning before /dev starts: "Overlap detected: src/User.cs (STORY-037 and STORY-038). Proceed? (1) Yes (2) No (3) Review"
- AC3: Post-flight check: After /dev Phase 2, run git diff in each worktree, compare changed file lists
- AC4: If actual overlap differs from spec overlap, log discrepancy: "Warning: STORY-038 modified src/Product.cs (not in spec)"
- AC5: Overlap report saved: tests/reports/overlap-STORY-{id}-{timestamp}.md

**Dependencies:** Feature 3 (uses dependency graph data)

**Deliverables:**
- **Subagent:** file-overlap-detector (NEW, ~350 lines) in src/claude/agents/
- Spec parser for file_path extraction (in subagent)
- Git diff analyzer (in subagent)
- Overlap detection module (in subagent)
- Warning prompt integration in src/claude/skills/devforgeai-development/ (Phase 0 Step 0.4)
- **Overlap reports:** tests/reports/overlap-STORY-{id}-{timestamp}.md
- Documentation: File overlap analysis guide

**Subagent:** **file-overlap-detector** (NEW)
- **Responsibilities:** Parse technical_specification YAML (extract file_path), run git diff across worktrees, compute set intersection (overlapping files), generate overlap report with recommendations
- **Model:** haiku (fast parsing and analysis)
- **Tools:** Read (story files), Bash (git diff), Grep (file patterns)
- **Token Target:** <10K
- **Reusability:** Medium (merge conflict prevention, code ownership analysis)

**Risk:** Medium - Spec parsing accuracy (depends on story quality), git diff across worktrees

---

#### 5. /worktrees Management Command (5 points)

**Description:** New slash command to view, manage, and cleanup active Git worktrees with status information (story ID, age, disk usage, current development phase, QA status).

**User Story:**
As a DevForgeAI developer with multiple active worktrees,
I want a central command to see all worktrees and their status,
So that I can identify stale worktrees for cleanup and resume interrupted work.

**Complexity:** Low (4/10)
- Git worktree list parsing
- Worktree status detection (story status, age, disk size)
- Interactive cleanup UI
- Resume capability

**Acceptance Criteria:**
- AC1: /worktrees displays table: Story ID, Path, Age, Size, Story Status, Last Activity
- AC2: Identifies cleanup candidates: "⚠️ 2 worktrees idle >7 days (story-037: 12 days, story-041: 9 days)"
- AC3: Interactive actions: (1) Cleanup all, (2) Cleanup selected, (3) Inspect worktree, (4) Cancel
- AC4: Cleanup verifies story status before deleting: "story-037 status=Released → safe to delete, story-041 status=In Development → keep"
- AC5: Execution time <5 seconds (list + status check)

**Dependencies:** Feature 1 (worktrees must exist to manage)

**Deliverables:**
- .claude/commands/worktrees.md (new command)
- Worktree status analyzer
- Cleanup UI
- Documentation: Worktree management guide

**Risk:** Low - Simple utility command, no complex logic

---

#### 6. Lock File Coordination for Critical Operations (3 points)

**Description:** Implement lock file mechanism for serializing git commit operations to prevent race conditions when multiple worktrees commit simultaneously.

**User Story:**
As a DevForgeAI developer,
I want git commits from parallel stories to be serialized automatically,
So that I don't encounter git index lock conflicts or race conditions.

**Complexity:** Low (3/10)
- Lock file create/check/release
- Stale lock detection (PID check, age threshold)
- Wait-with-progress UI

**Acceptance Criteria:**
- AC1: /dev Phase 5 (git commit) acquires .devforgeai/.locks/git-commit.lock before committing (operational folder, not source)
- AC2: If lock exists, waits with progress: "Waiting for git lock (held by STORY-037 PID 12345)... 15s"
- AC3: Stale lock detection: Lock >5 min old with dead PID auto-removed
- AC4: Lock timeout: After 10 min waiting, prompt: "(1) Continue waiting, (2) Force acquire lock (risky), (3) Abort"
- AC5: Lock released after successful commit

**Note:** Lock files are runtime artifacts in .devforgeai/.locks/ (operational), not in src/ (source) or tests/ (testing)

**Dependencies:** Feature 1 (worktrees create concurrent git operations)

**Deliverables:**
- Lock manager module
- /dev Phase 5 integration
- Stale lock detector
- Documentation: Lock file coordination

**Risk:** Low - Simple file-based locking, proven pattern

---

### Phase 2: CI/CD Integration (2 features - Deferred)

#### 7. GitHub Actions Workflow Templates with Headless Claude Code (13 points)

**Description:** Create GitHub Actions workflow templates that execute /dev and /qa in headless mode using Claude Code Terminal's `claude -p` flag, enabling automated parallel story development on pull requests.

**Complexity:** High (8/10) - **DEFERRED TO PHASE 2**
- Headless Claude Code setup
- GitHub Actions matrix configuration
- ANTHROPIC_API_KEY secret management
- Cost optimization (prompt caching, Haiku model)
- Workflow artifacts (QA reports, test results)

**MVP Deferral Rationale:** Per discovery, CI/CD is "medium priority - nice to have later." Focus Phase 1 on local parallel (higher immediate value).

---

#### 8. Headless Mode Answer Configuration (5 points)

**Description:** Configuration system for providing pre-defined answers to AskUserQuestion prompts when running in headless/CI mode, enabling unattended execution.

**Complexity:** Medium (5/10) - **DEFERRED TO PHASE 2**
- CI answer configuration file
- Answer matching logic
- Fail-on-unanswered-question mode

**MVP Deferral Rationale:** Per discovery, "defer headless to Phase 2." Local parallel doesn't require this complexity.

---

## Technical Assessment

### Complexity Score: 42/60 (Tier 3 - Complex Application)

**Breakdown:**
- Functional: 14/20 (worktrees, test isolation, dependency graphs, overlap detection)
- Technical: 16/20 (Git API integration, file system isolation, YAML schema updates, quality gate preservation)
- Team/Org: 4/10 (solo dev now, future team growth)
- NFRs: 8/10 (performance optimization, disk management, quality preservation)

**Architecture Tier:** Tier 3 - Multi-layered application
- Recommended: Feature-based architecture with clear separation
- Pattern: Modular enhancements to existing /dev, /qa commands

### Key Risks

**Risk 1: Git Worktree Cross-Platform Compatibility**
- **Impact:** CRITICAL (framework unusable on some platforms)
- **Likelihood:** Low (Git worktrees well-supported since Git 2.5, 2015)
- **Mitigation:**
  - Test on Linux, macOS, Windows (WSL and native)
  - Fallback to branch-only mode if worktrees unsupported
  - Document platform requirements (Git 2.5+)

**Risk 2: Quality Gate Bypass in Parallel Mode**
- **Impact:** CRITICAL (violates zero-debt philosophy)
- **Likelihood:** Medium (parallel complexity could introduce loopholes)
- **Mitigation:**
  - All quality gates preserved unchanged (coverage thresholds, TDD, deferral validation)
  - Dependency enforcement prevents out-of-order development
  - Comprehensive testing (validate gates work in parallel mode)
  - Explicit requirement: "Quality cannot be compromised"

**Risk 3: Developer Complexity Overhead**
- **Impact:** HIGH (feature unused if too complex)
- **Likelihood:** Medium (worktrees + dependencies + isolation adds cognitive load)
- **Mitigation:**
  - Default behavior (transparent auto-create)
  - Clear documentation with examples
  - /worktrees command for visibility
  - Backward compatible (/dev works as before for single-story)
  - Tutorial/onboarding guide

**Risk 4: Disk Space Exhaustion from Worktree Accumulation**
- **Impact:** MEDIUM (developer runs out of disk, framework fails)
- **Likelihood:** Medium (3-5 × 100MB = 500MB, plus forgotten old worktrees)
- **Mitigation:**
  - Auto-cleanup after 7 days idle
  - Prompt on next /dev (warns about old worktrees)
  - /worktrees command shows disk usage
  - Configurable cleanup threshold
  - Documentation: Worktree disk management

**Risk 5: Dependency Graph Complexity (Circular, Deep Chains)**
- **Impact:** MEDIUM (blocks development if graph invalid)
- **Likelihood:** Low (careful story planning prevents)
- **Mitigation:**
  - Circular dependency detection (fail fast with error)
  - Limit depth to 5 levels (prevent overly complex chains)
  - Epic-level dependency planning (dependencies defined upfront)
  - Visualization tool (dependency graph display)

**Risk 6: Git History Pollution from Many Story Branches**
- **Impact:** LOW (navigation harder, but functional)
- **Likelihood:** High (2-5 branches per developer, 10 developers = 50 branches)
- **Mitigation:**
  - Auto-delete branches after merge (on QA approval)
  - Branch naming convention (story-{id} consistent)
  - Git alias for filtering (git branch | grep story-)
  - Periodic cleanup tool (/worktrees cleanup-merged)

### Prerequisites

**Before starting this epic:**
- [ ] EPIC-009 complete (src/ migration and installer functional)
- [ ] Git 2.5+ installed (worktrees require this minimum version)
- [ ] Python 3.8+ available (dependency graph algorithms)
- [ ] Sufficient disk space (500MB minimum for 5 worktrees)
- [ ] DevForgeAI context files exist (framework already configured)

**Not required:**
- GitHub Actions account (Phase 2 only)
- Multiple developers (design for solo, scales to team)
- CI/CD infrastructure (Phase 2 only)

## Stakeholders

- **Product Owner:** Framework Maintainer (Bryan)
- **Tech Lead:** TBD (assign before Sprint 1)
- **DevOps Lead:** TBD (Git worktree expertise, CI/CD for Phase 2)
- **QA Lead:** TBD (validate quality gates preserved)
- **Early Adopters:** Solo developer (Bryan) validates MVP, future team for Phase 2

## Subagent Requirements

### New Subagents (2 for Phase 1)

**1. dependency-graph-analyzer** (NEW - Feature 3)
- **Purpose:** Build and validate story dependency graphs with transitive resolution
- **Model:** haiku (fast graph algorithms)
- **Token Target:** <15K
- **Tools:** Read, Grep, Glob
- **Effort:** 6-8 hours to create
- **Reusability:** High (epic dependencies, sprint planning, future dependency features)

**2. file-overlap-detector** (NEW - Feature 4)
- **Purpose:** Detect file conflicts between concurrent stories using hybrid spec + git analysis
- **Model:** haiku (fast parsing and analysis)
- **Token Target:** <10K
- **Tools:** Read, Bash (git diff), Grep
- **Effort:** 4-6 hours to create
- **Reusability:** Medium (merge conflict prevention, code ownership)

### Enhanced Subagents (1 for Phase 1)

**1. git-validator → git-worktree-manager** (ENHANCED - Features 1, 5)
- **Add:** Worktree creation, cleanup detection, age calculation, disk usage, status reporting
- **Model:** haiku (unchanged)
- **Token Target:** <10K (was <5K, grows to support worktrees)
- **Tools:** Bash (git worktree commands), Read, Grep
- **Effort:** 4-6 hours to enhance
- **Reusability:** High (any Git worktree workflow)

### Existing Subagents Reused (No Changes)

- **context-validator** - Validate framework constraints in parallel stories (unchanged)
- **test-automator** - Generate tests in worktree-isolated stories (unchanged)
- **deferral-validator** - Validate deferrals in parallel executions (unchanged)
- **All other subagents** - Work unchanged in worktree environment (isolated contexts)

**Total Subagent Count After EPIC-010:**
- Current: 26 subagents
- New: +2 (dependency-graph-analyzer, file-overlap-detector)
- Enhanced: 1 (git-validator → git-worktree-manager)
- **Result: 28 subagents**

---

## Dependencies

**Upstream Dependencies:**
- **EPIC-009:** src/ Migration and Installer (MUST complete first - parallel development builds on installer pattern)

**Downstream Dependencies:**
- Future team onboarding (depends on parallel capability)
- CI/CD automation roadmap (Phase 2 of this epic)
- v2.0 multi-developer features (depends on parallel foundation)

**External Dependencies:**
- Git 2.5+ (worktrees feature)
- Claude Code Terminal (current version supports basic concurrency)
- GitHub Actions (Phase 2 only)
- Anthropic API (Phase 2 only)

## Related Epics

- **EPIC-009:** DevForgeAI src/ Migration and Installer (prerequisite - must complete first)
- **EPIC-007:** Lean Orchestration Compliance (related - both improve framework efficiency)
- **Future:** Multi-Developer Collaboration Features (depends on this - team workflows)

---

## Command and Skill Architecture

### Commands Modified (2)

#### `/dev` Command → `devforgeai-development` Skill (MODIFIED)

**Current Behavior:** Execute TDD workflow in current directory/branch

**EPIC-010 Enhancements:**

**Command Changes (stays lean, <15K chars):**
- Invokes skill with parallel-mode markers (no logic in command)
- Displays worktree creation status
- Displays dependency validation results
- Displays overlap detection warnings

**Skill Changes (devforgeai-development):**

**New Phase 0 Steps:**
- **Step 0.1:** Git Validation (existing - git-validator, unchanged)
- **Step 0.2:** Worktree Management (NEW - invoke git-worktree-manager)
  - Check if worktree exists: `../devforgeai-story-{id}/`
  - If exists: Prompt (Resume, Fresh Start, Delete Old)
  - If not: Create worktree, checkout story-{id} branch
  - Switch to worktree directory
  - Duration: <10 seconds
- **Step 0.3:** Dependency Validation (NEW - invoke dependency-graph-analyzer)
  - Parse depends_on from story YAML
  - Build transitive dependency graph
  - Validate all dependencies met (status = Dev Complete or QA Approved)
  - Block if unmet OR allow with --force flag
  - Display dependency tree if blocked
- **Step 0.4:** File Overlap Detection (NEW - invoke file-overlap-detector)
  - Parse technical_specification YAML (extract file_path fields)
  - Compare with other active stories (scan all worktrees)
  - Warn if overlap detected
  - Prompt: Proceed, Abort, or Review overlapping files
- **Step 0.5:** Switch to Worktree (NEW)
  - `cd ../devforgeai-story-{id}/`
  - Display: "✓ Working in worktree: ../devforgeai-story-{id}/"
- **Step 0.6:** Tech Stack Detection (existing - tech-stack-detector, unchanged)
- **Step 0.7:** Context Files Validation (existing, unchanged)

**Modified Phase 2 (Green - Tests):**
- Run tests with story-scoped output directories in tests/ tree:
  - `--results-directory=tests/results/{story_id}/`
  - `--cov-report=html:tests/coverage/{story_id}/coverage-html`
  - `--cov-report=xml:tests/coverage/{story_id}/coverage.xml`
  - `--junitxml=tests/results/{story_id}/test-results.xml`

**Modified Phase 5 (Git/Tracking):**
- **Step 5.1:** Acquire Git Commit Lock (NEW)
  - Check .devforgeai/.locks/git-commit.lock
  - Wait if locked (max 10 min, display progress)
  - Acquire lock (write PID, story_id, timestamp)
- **Step 5.2:** Git Commit (modified - commit to story branch in worktree)
  - Commit to `story-{id}` branch (not main)
  - Commit message includes: "Story: STORY-{id}"
- **Step 5.3:** Release Lock (NEW)
  - Remove .devforgeai/.locks/git-commit.lock
- **Step 5.4:** Post-Flight Overlap Check (NEW - invoke file-overlap-detector)
  - Run git diff --name-only in worktree
  - Compare actual files changed vs spec file_path
  - Log discrepancies if found

**New Reference Files (4 files, ~1,550 lines):**
- worktree-management-workflow.md (400 lines) - Step 0.2 worktree logic
- dependency-validation-workflow.md (350 lines) - Step 0.3 dependency checks
- overlap-detection-workflow.md (300 lines) - Step 0.4 pre-flight + 5.4 post-flight
- parallel-development-guide.md (500 lines) - Complete parallel workflow documentation

**Token Impact:**
- Skill grows: ~1,782 lines → ~2,200 lines (increases ~25%, but isolated context)
- Command unchanged: ~527 lines (stays lean, delegates to skill)

---

#### `/qa` Command → `devforgeai-qa` Skill (MODIFIED)

**Current Behavior:** Run quality validation in current directory

**EPIC-010 Enhancements:**

**Command Changes (stays lean):**
- Invokes skill with worktree-aware markers
- Displays auto-merge results (Phase 2)

**Skill Changes (devforgeai-qa):**

**Enhanced Phase 0 (Story Validation):**
- **Step 0.1:** Worktree Detection (NEW)
  - Check if running in worktree: `git worktree list | grep $(pwd)`
  - If worktree: Extract story ID from path
  - Display: "ℹ️ Running QA in worktree: ../devforgeai-story-{id}/"
- **Step 0.2:** Story-Scoped Path Resolution (NEW)
  - Resolve test results: `tests/results/{story_id}/test-results.xml`
  - Resolve coverage: `tests/coverage/{story_id}/coverage.xml`
  - Validate paths exist before analysis

**Modified Phase 1-4 (Validation Phases):**
- Read test results from story-scoped paths in tests/ tree (not shared results/)
- Read coverage from story-scoped paths in tests/ tree (not shared coverage/)
- All validation logic unchanged (same quality gates)

**New Phase 5 (Post-QA Actions) - Only for Deep QA PASSED:**
- **Step 5.1:** Auto-Merge Story Branch (NEW)
  - Checkout main branch: `git checkout main`
  - Merge story branch: `git merge story-{id} --no-ff`
  - If conflicts: Display conflicted files, halt, prompt developer for manual resolution
  - If success: Display "✓ Merged story-{id} → main"
- **Step 5.2:** Delete Story Branch (NEW)
  - `git branch -d story-{id}` (safe delete, verifies merged)
  - Display: "✓ Deleted branch: story-{id}"
- **Step 5.3:** Cleanup Worktree (NEW - invoke git-worktree-manager)
  - Invoke git-worktree-manager with action=cleanup
  - Remove `../devforgeai-story-{id}/`
  - Display: "✓ Cleaned up worktree"
- **Step 5.4:** Update Story Status (modified - now happens after merge)
  - Status = "Released" (merged to main = production-ready in DevForgeAI)
  - Append workflow history: "Merged to main, worktree cleaned"

**New Reference Files (2 files, ~550 lines):**
- parallel-qa-workflow.md (300 lines) - Worktree-aware validation
- auto-merge-on-approval.md (250 lines) - Phase 5 auto-merge logic

**Token Impact:**
- Skill grows: ~1,330 lines → ~1,600 lines (increases ~20%, isolated context)
- Command unchanged: ~309 lines (stays lean)

---

### Commands Created (2)

#### `/worktrees` Command → No Skill (Utility Pattern)

**Purpose:** Manage active Git worktrees (list, cleanup, inspect, resume)

**Pattern:** Utility command (like /audit-budget) - Direct subagent invocation, no skill layer needed

**Workflow:**
```
Phase 0: Validate Git Repository
├─ Check git repository initialized
└─ If not: Display error, exit

Phase 1: Invoke git-worktree-manager Subagent
├─ Task(subagent_type="git-worktree-manager",
│        description="List all worktrees with status",
│        prompt="List all Git worktrees for DevForgeAI stories.
│                Include: story ID, worktree path, age (days),
│                disk usage (MB), story status, last activity.
│                Identify cleanup candidates (idle >7 days).")
└─ Receive structured result (JSON with worktree array)

Phase 2: Display Worktree Table
├─ Format table from subagent result
├─ Columns: Story ID | Path | Age | Size | Status | Last Activity
├─ Highlight cleanup candidates in yellow
└─ Show totals: X worktrees, Y MB disk usage, Z cleanup candidates

Phase 3: Interactive Actions
├─ Prompt user:
│   (1) Cleanup all candidates
│   (2) Cleanup selected
│   (3) Inspect worktree (show files changed)
│   (4) Resume development (cd to worktree, rerun /dev)
│   (5) Cancel
├─ Based on selection:
│   └─ Invoke git-worktree-manager with action (cleanup/inspect/resume)
└─ Display results
```

**Example Output:**
```
$ /worktrees

Active Git Worktrees:
┌──────────┬──────────────────────────────┬─────────┬────────┬──────────────┬─────────────────┐
│ Story ID │ Path                         │ Age     │ Size   │ Status       │ Last Activity   │
├──────────┼──────────────────────────────┼─────────┼────────┼──────────────┼─────────────────┤
│ STORY-037│ ../devforgeai-story-037/     │ 2 days  │ 105 MB │ Dev Complete │ 2025-11-14 10:30│
│ STORY-038│ ../devforgeai-story-038/     │ 5 days  │ 103 MB │ In Development│ 2025-11-11 14:20│
│ STORY-041│ ../devforgeai-story-041/     │ 12 days │ 108 MB │ Released     │ 2025-11-04 09:15│⚠️
│ STORY-044│ ../devforgeai-story-044/     │ 8 days  │ 102 MB │ QA Failed    │ 2025-11-08 16:45│⚠️
└──────────┴──────────────────────────────┴─────────┴────────┴──────────────┴─────────────────┘

Total: 4 worktrees, 418 MB disk usage
⚠️ Cleanup candidates: 2 worktrees (story-041: 12 days idle, story-044: 8 days idle)

Actions:
  (1) Cleanup all candidates (story-041, story-044) - Free 210 MB
  (2) Cleanup selected (choose which to delete)
  (3) Inspect worktree (show files changed, git log)
  (4) Resume development (cd to worktree, rerun /dev)
  (5) Cancel

Choose [1-5]:
```

**Effort:** 3-4 hours (lean command, subagent does heavy lifting)

---

#### `/setup-github-actions` Command → `devforgeai-github` Skill (NEW)

**Purpose:** Set up GitHub Actions CI/CD workflows for DevForgeAI parallel development

**Pattern:** Standard command → skill delegation (like /create-context, /create-epic)

**Workflow:**
```
Phase 0: Argument Validation
├─ Optional: --project-type (nodejs, dotnet, python)
└─ Optional: --workflows (dev, qa, parallel, installer)

Phase 1: Set Context Markers
├─ **Project Type:** {detected or user-selected}
├─ **Workflows:** {selected workflows or all}
├─ **Command:** setup-github-actions
└─ Invoke: Skill(command="devforgeai-github")

Phase 2: Display Results
└─ Output skill summary (workflows created, config files, next steps)
```

**Skill:** `devforgeai-github` (NEW - 10th DevForgeAI skill)

**Skill Workflow (5 phases):**

**Phase 0: Repository Validation**
- Detect GitHub repository (check .git/config for github.com remote)
- Validate GitHub App installed (optional - for @claude mentions)
- Check if .github/workflows/ exists
- Load project type (from tech-stack.md or detect)

**Phase 1: Workflow Generation**
- Create .github/workflows/dev-story.yml (automated /dev execution)
  - Trigger: workflow_dispatch with story_id input
  - Job: Run claude -p "/dev ${{inputs.story_id}}"
  - Artifacts: Upload test results, coverage, story file
- Create .github/workflows/qa-validation.yml (PR quality gate)
  - Trigger: pull_request to main
  - Job: Extract story ID from PR title, run /qa deep
  - Status check: Block merge if QA fails
- Create .github/workflows/parallel-stories.yml (matrix execution)
  - Trigger: workflow_dispatch with story_ids array
  - Strategy: matrix with story_ids
  - Parallel: Run /dev for each story simultaneously
- Create .github/workflows/installer-testing.yml (EPIC-009 support)
  - Trigger: push to main, PR
  - Strategy: matrix (nodejs, dotnet, python) × (ubuntu, windows, macos)
  - Test: Run installer on each configuration

**Phase 2: Configuration Setup**
- Create src/devforgeai/config/github-actions.yaml.example (template):
  - Installer deploys to .devforgeai/config/github-actions.yaml (operational)
  ```yaml
  github_actions:
    enabled: true
    max_parallel_jobs: 5  # Concurrency limit
    default_runner: ubuntu-latest
    cost_optimization:
      enable_prompt_caching: true
      prefer_haiku: true  # vs Sonnet
      max_cost_per_story: 0.15  # USD
    workflows:
      dev_story:
        timeout_minutes: 30
        model: haiku
      qa_validation:
        timeout_minutes: 20
        model: sonnet  # Quality validation uses Sonnet
      parallel_stories:
        max_concurrent: 5
        model: haiku
  ```
- Create src/devforgeai/config/ci-answers.yaml.example (template):
  - Installer deploys to .devforgeai/config/ci-answers.yaml (operational)
  ```yaml
  ci_mode_answers:
    test_failure_action: "fix-implementation"
    deferral_strategy: "never"
    priority_default: "high"
    sprint_default: "backlog"
    epic_association: "auto-detect"
  ```

**Phase 3: Cost Optimization**
- Configure prompt caching (90% API cost savings)
- Set concurrency limits (prevent runaway jobs)
- Create cost estimator script (.github/scripts/estimate-cost.py)
- Document cost monitoring

**Phase 4: Validation**
- Test workflow with sample story (dry run)
- Validate headless execution works
- Verify artifacts upload correctly
- Test PR quality gate blocks merge on QA failure

**Phase 5: Documentation**
- Create .github/README.md (GitHub Actions setup guide)
- Create docs/GITHUB-ACTIONS-GUIDE.md (user documentation)
- Create docs/COST-OPTIMIZATION.md (managing API + runner costs)
- Create docs/TROUBLESHOOTING-CICD.md (common issues)

**Reference Files (6 files, ~3,000 lines):**
- github-actions-setup-workflow.md (500 lines) - Phase 1
- workflow-template-generation.md (600 lines) - Workflow YAML patterns
- cost-optimization-guide.md (450 lines) - Phase 3
- headless-configuration.md (400 lines) - Phase 2
- ci-validation-procedures.md (550 lines) - Phase 4
- github-actions-troubleshooting.md (500 lines) - Error recovery

**Subagents Invoked:**
- **internet-sleuth** (auto-invoked - research latest GitHub Actions best practices)

**Effort:** 12-16 hours (skill creation + 6 reference files)

---

### Commands Created (2)

#### `/worktrees` - List and Manage Active Worktrees (NEW)

**Skill:** None (utility pattern)
**Subagent:** git-worktree-manager (direct invocation)
**Effort:** 3-4 hours
**Lines:** ~300-400 (lean utility)

#### `/setup-github-actions` - Configure CI/CD Workflows (NEW)

**Skill:** devforgeai-github (NEW)
**Subagent:** internet-sleuth (auto-invoked for research)
**Effort:** 3-4 hours command + 12-16 hours skill = 15-20 hours total
**Lines:** Command ~250-350, Skill ~600-800 (entry point, references loaded progressively)

---

## Skills Architecture Summary

### Skills Modified (2)

**1. devforgeai-development**
- Add: Phase 0 Steps 0.2-0.5 (4 new steps: worktree, dependency, overlap, switch)
- Modify: Phase 2 (story-scoped test paths)
- Modify: Phase 5 (lock acquisition + commit to story branch + lock release + post-flight overlap)
- New references: 4 files (~1,550 lines)
- Effort: 8-12 hours

**2. devforgeai-qa**
- Add: Phase 0 Steps 0.1-0.2 (2 new steps: worktree detection, path resolution)
- Modify: Phase 1-4 (use story-scoped paths)
- Add: Phase 5 (4 steps: auto-merge, delete branch, cleanup worktree, update status)
- New references: 2 files (~550 lines)
- Effort: 4-6 hours

### Skills Created (1)

**1. devforgeai-github** (NEW - 11th skill, 10th DevForgeAI skill)
- Purpose: GitHub Actions CI/CD orchestration
- Phases: 5 (validation, generation, configuration, optimization, documentation)
- References: 6 files (~3,000 lines)
- Subagents: internet-sleuth (auto-invoked)
- Effort: 12-16 hours

**Total Skills After EPIC-010:** 10 → **11 skills**
- 10 DevForgeAI skills (9 existing + devforgeai-github)
- 1 infrastructure skill (claude-code-terminal-expert)

## Stories

### Phase 1: MVP - Local Parallel Development

**Sprint 1 (Weeks 1-2): Foundation**
1. STORY-TBD: Git Worktree Auto-Management (8 points)
2. STORY-TBD: Story-Scoped Test Isolation (5 points)
**Total:** 13 points

**Sprint 2 (Weeks 3-4): Dependency & Safety**
3. STORY-TBD: Dependency Graph Enforcement with Transitive Resolution (13 points)
4. STORY-TBD: File Overlap Detection with Hybrid Analysis (8 points)
**Total:** 21 points

**Sprint 3 (Weeks 5-6): Management & Cleanup**
5. STORY-TBD: /worktrees Management Command (5 points)
6. STORY-TBD: Lock File Coordination for Git Operations (3 points)
**Total:** 8 points

**Phase 1 Total:** 6 stories, 42 points, 6 weeks

### Phase 2: CI/CD Integration (Deferred, Go/No-Go after Phase 1)

**Sprint 4 (Weeks 7-9): CI/CD Infrastructure**
7. STORY-TBD: Create devforgeai-github Skill and /setup-github-actions Command (13 points) - **Deferred**
   - Deliverables: devforgeai-github skill (5 phases, 6 reference files), /setup-github-actions command, GitHub Actions workflow templates
8. STORY-TBD: GitHub Actions Workflow Testing and Cost Optimization (10 points) - **Deferred**
   - Deliverables: Test all 4 workflows, validate headless mode, implement cost tracking, documentation

**Total:** 23 points

**Phase 2 Total:** 2 stories, 23 points, 3 weeks (extended from 2 weeks due to skill creation)

**Grand Total:** 8 stories, 65 points, 9 weeks (Phase 1: 42 points over 6 weeks, Phase 2: 23 points over 3 weeks)

## Research Findings (Internet-Sleuth)

**Headless Mode Validated:**
- ✅ Claude Code supports `claude -p` flag for non-interactive execution
- ✅ `--dangerously-skip-permissions` (YOLO mode) for unattended execution
- ✅ JSON output for programmatic parsing
- ✅ Session persistence with `--resume` flag

**GitHub Actions Integration Proven:**
- ✅ Official `anthropics/claude-code-action` available
- ✅ Matrix strategy supports up to 256 parallel jobs
- ✅ Works with self-hosted or GitHub-hosted runners

**Cost Analysis (Per Story):**
- API: $0.051 (Sonnet) or $0.011 (Haiku with 90% caching)
- Runner: $0.04 (GitHub) or $0.01 (Depot small)
- **Total: $0.08-$0.12 per story**
- Free tier feasibility: 2,000 min/month = ~40 stories/month (sufficient for solo dev)

**Git Worktrees:**
- Proven isolation pattern
- Each worktree ~100MB (framework size)
- Shared .git/ directory (no duplication of history)
- Cleanup critical (prevent accumulation)

**Community Validation:**
- 10+ GitHub repos using Claude in CI/CD
- Proven patterns: prompt caching (90% savings), Haiku for cost optimization
- Best practice: fail-on-ambiguity for CI (forces complete specs)

## Implementation Strategy

### MVP First (Phase 1 - 6 weeks)

**Week 1-2:**
- Implement worktree auto-management
- Implement test isolation
- Validate 2 concurrent stories work locally

**Week 3-4:**
- Implement dependency graph with transitive resolution
- Implement file overlap detection
- Validate dependency enforcement works

**Week 5-6:**
- Implement /worktrees management command
- Implement git lock coordination
- Comprehensive testing and documentation

**Go/No-Go Checkpoint (End of Week 6):**
- Criteria: 2 concurrent stories execute without collisions, quality gates 100% preserved, dependency enforcement validated
- If GO: Proceed to Phase 2 (CI/CD integration)
- If NO-GO: Iterate on MVP, extend Phase 1, defer Phase 2

### Phase 2 (Conditional - 2 weeks)

**Only proceed if:**
- MVP successful (Go decision at checkpoint)
- Budget available for GitHub Actions + API costs
- Headless mode requirements clear (AskUserQuestion handling resolved)

**Week 7-8:**
- GitHub Actions workflows
- Headless configuration
- Cost optimization (caching, Haiku)
- CI/CD testing and documentation

---

## Directory Structure Alignment

**EPIC-010 follows DevForgeAI directory conventions:**

### Source Tree (src/)
**Purpose:** All source code (skills, commands, subagents, scripts)

**EPIC-010 Additions:**
- `src/claude/agents/git-worktree-manager.md` (enhanced subagent)
- `src/claude/agents/dependency-graph-analyzer.md` (NEW subagent)
- `src/claude/agents/file-overlap-detector.md` (NEW subagent)
- `src/claude/skills/devforgeai-development/references/worktree-management-workflow.md` (NEW reference)
- `src/claude/skills/devforgeai-development/references/dependency-validation-workflow.md` (NEW reference)
- `src/claude/skills/devforgeai-development/references/overlap-detection-workflow.md` (NEW reference)
- `src/claude/skills/devforgeai-development/references/parallel-development-guide.md` (NEW reference)
- `src/claude/skills/devforgeai-qa/references/parallel-qa-workflow.md` (NEW reference)
- `src/claude/skills/devforgeai-qa/references/auto-merge-on-approval.md` (NEW reference)
- `src/claude/skills/devforgeai-github/SKILL.md` (NEW skill - Phase 2)
- `src/claude/skills/devforgeai-github/references/` (6 new reference files - Phase 2)
- `src/claude/commands/worktrees.md` (NEW command)
- `src/claude/commands/setup-github-actions.md` (NEW command - Phase 2)
- `src/devforgeai/config/parallel.yaml.example` (config template)
- `src/devforgeai/config/test-isolation.yaml.example` (config template)
- `src/devforgeai/config/github-actions.yaml.example` (config template - Phase 2)
- `src/devforgeai/config/ci-answers.yaml.example` (config template - Phase 2)

### Testing Tree (tests/)
**Purpose:** All tests, test results, coverage reports

**EPIC-010 Additions:**
- `tests/results/STORY-{id}/` (story-scoped test results - created at runtime)
- `tests/coverage/STORY-{id}/` (story-scoped coverage reports - created at runtime)
- `tests/logs/STORY-{id}/` (story-scoped test logs - created at runtime)
- `tests/reports/overlap-STORY-{id}-{timestamp}.md` (file overlap reports - created at runtime)
- `tests/unit/test_dependency_graph.py` (unit tests for Feature 3)
- `tests/unit/test_file_overlap.py` (unit tests for Feature 4)
- `tests/unit/test_worktree_manager.py` (unit tests for Feature 1)
- `tests/integration/test_parallel_dev.py` (integration tests for concurrent /dev)
- `tests/integration/test_parallel_qa.py` (integration tests for concurrent /qa)

### Operational Folders (.devforgeai/)
**Purpose:** Runtime artifacts, generated reports, operational config

**EPIC-010 Additions:**
- `.devforgeai/config/parallel.yaml` (deployed from src/ template, user-editable)
- `.devforgeai/config/test-isolation.yaml` (deployed from src/ template, user-editable)
- `.devforgeai/config/github-actions.yaml` (deployed from src/ template - Phase 2, user-editable)
- `.devforgeai/config/ci-answers.yaml` (deployed from src/ template - Phase 2, user-editable)
- `.devforgeai/.locks/git-commit.lock` (runtime lock file, NOT in src/ or tests/)
- `.devforgeai/.locks/build.lock` (runtime lock file if needed)

### Deployed Operational (.claude/)
**Purpose:** Deployed framework files (from src/ via installer)

**EPIC-010 Changes:**
- All source changes deploy via installer: src/claude/ → .claude/
- Worktrees operate in separate directories (../devforgeai-story-{id}/) with own .claude/ copy

### User Content (.ai_docs/)
**Purpose:** Stories, epics, sprints (user-created)

**EPIC-010 No Changes:** Stories continue to live in .ai_docs/Stories/ (unchanged)

---

## Backward Compatibility Guarantee

**Critical Requirement:** Existing /dev workflow MUST work unchanged

**Compatibility Matrix:**

| Scenario | Existing Behavior | With Parallel Feature | Compatible? |
|----------|-------------------|----------------------|-------------|
| /dev STORY-001 (single story) | Works in main repo | Auto-creates worktree, works there | ✅ YES (transparent) |
| /dev --help | Shows help | Shows help (+ new flags) | ✅ YES |
| Story without depends_on | Develops normally | Develops normally (no dependencies) | ✅ YES |
| Quality gates (coverage, TDD) | Enforced strictly | Enforced identically in worktree | ✅ YES |
| Git commits | Commits to current branch | Commits to story branch in worktree | ⚠️ CHANGE (but compatible) |
| Test outputs | tests/ (shared) | tests/results/{story_id}/ (isolated) | ⚠️ CHANGE (but compatible) |
| Coverage reports | tests/ (shared) | tests/coverage/{story_id}/ (isolated) | ⚠️ CHANGE (but compatible) |

**Breaking Changes:** None (changes are additive and transparent)

**Migration Path:** None needed (feature works immediately, backward compatible by default)

## Validation Approach

### Testing Strategy

**Unit Tests (Per Feature):**
- Feature 1: Worktree create, cleanup, resume, config
- Feature 2: Test path isolation, framework integration
- Feature 3: Dependency graph, transitive resolution, circular detection, cascade blocking
- Feature 4: Spec parser, git diff, overlap detection
- Feature 5: /worktrees command (list, cleanup, actions)
- Feature 6: Lock acquisition, stale detection, timeout

**Integration Tests:**
- 2 concurrent /dev executions (STORY-037, STORY-038 simultaneously)
- Dependency enforcement (STORY-038 waits for STORY-037)
- Overlap detection (stories modifying same file)
- Cleanup automation (7-day threshold triggers)
- /worktrees management (list, cleanup, inspect)

**Regression Tests:**
- Single story /dev still works (backward compatibility)
- Quality gates unchanged (coverage, TDD, deferrals)
- Existing commands unaffected (/qa, /release, /orchestrate)

## Status History

- **2025-11-16:** Epic created from /ideate comprehensive discovery (18 questions, internet-sleuth research)
- **2025-11-16:** Status: Planning (no stories created yet)
- **2025-11-16:** Complexity: 42/60 (Tier 3 - Complex Application)
- **2025-11-16:** Research: Headless mode validated, Git worktrees proven, cost-effective ($0.08-$0.12/story)
- **2025-11-16:** Scope: 6 features MVP (Phase 1), 2 features deferred (Phase 2 CI/CD)
- **2025-11-16:** Timeline: 8 weeks (Phase 1: 6 weeks, Phase 2: 2 weeks conditional)
- **2025-11-16:** Dependencies: EPIC-009 must complete first (src/ migration prerequisite)
- **2025-11-16:** Target team: Solo dev (future-proof for 2-10 developers)
- **2025-11-16:** Key requirements: Quality cannot be compromised, backward compatible, free tier cost constraint

---

## Component Summary

### Commands (4 total)

**Modified Commands (2):**
1. **`/dev`** → `devforgeai-development` skill
   - Enhancement: Worktree auto-create, dependency validation, file overlap detection, story-scoped tests, lock-based commits
   - New subagents invoked: git-worktree-manager, dependency-graph-analyzer, file-overlap-detector
   - Backward compatible: ✅ Existing single-story workflow unchanged

2. **`/qa`** → `devforgeai-qa` skill
   - Enhancement: Worktree detection, story-scoped path resolution, auto-merge on approval
   - New subagents invoked: git-worktree-manager
   - Backward compatible: ✅ Existing validation workflow unchanged

**New Commands (2):**
3. **`/worktrees`** → No skill (utility pattern)
   - Purpose: List/manage/cleanup active worktrees
   - Subagent: git-worktree-manager (direct invocation)
   - Pattern: Similar to /audit-budget (utility with direct subagent call)

4. **`/setup-github-actions`** → `devforgeai-github` skill (NEW)
   - Purpose: Configure GitHub Actions CI/CD workflows
   - Subagent: internet-sleuth (auto-invoked for research)
   - Pattern: Standard command → skill delegation

**Total Command Count After EPIC-010:** 14 → **16 commands**

---

### Skills (3 total)

**Modified Skills (2):**

1. **`devforgeai-development`** (MODIFIED)
   - **Current:** 6 phases (Pre-Flight, Red, Green, Refactor, Integration, Deferral Challenge, Git/Tracking)
   - **Add:** Phase 0 Steps 0.2-0.5 (worktree, dependency, overlap, switch to worktree)
   - **Modify:** Phase 2 (story-scoped test output paths)
   - **Modify:** Phase 5 (lock acquisition, commit to story branch, lock release, post-flight overlap)
   - **New references:** 4 files (~1,550 lines)
     - worktree-management-workflow.md
     - dependency-validation-workflow.md
     - overlap-detection-workflow.md
     - parallel-development-guide.md
   - **Size impact:** ~1,782 lines → ~2,200 lines (+25% in isolated context)
   - **Subagents:** +3 invocations (git-worktree-manager, dependency-graph-analyzer, file-overlap-detector)

2. **`devforgeai-qa`** (MODIFIED)
   - **Current:** 5 phases (Pre-Flight, Test Coverage, Anti-Pattern Detection, Spec Compliance, Code Quality Metrics, Generate Report)
   - **Add:** Phase 0 Steps 0.1-0.2 (worktree detection, story-scoped path resolution)
   - **Modify:** Phase 1-4 (read from story-scoped paths: TestResults/{story_id}/, coverage/{story_id}/)
   - **Add:** Phase 5 (auto-merge on Deep QA PASSED: merge to main, delete branch, cleanup worktree, update status)
   - **New references:** 2 files (~550 lines)
     - parallel-qa-workflow.md
     - auto-merge-on-approval.md
   - **Size impact:** ~1,330 lines → ~1,600 lines (+20% in isolated context)
   - **Subagents:** +1 invocation (git-worktree-manager for cleanup)

**Created Skills (1):**

3. **`devforgeai-github`** (NEW - 11th skill, 10th DevForgeAI skill)
   - **Purpose:** GitHub Actions CI/CD orchestration for parallel development automation
   - **Phases:** 5 (Repository Validation, Workflow Generation, Configuration Setup, Cost Optimization, Documentation)
   - **Workflow generation:**
     - .github/workflows/dev-story.yml (automated /dev per story)
     - .github/workflows/qa-validation.yml (PR quality gate)
     - .github/workflows/parallel-stories.yml (matrix parallel execution)
     - .github/workflows/installer-testing.yml (cross-platform installer validation)
   - **Configuration:**
     - src/devforgeai/config/github-actions.yaml.example (source template)
     - src/devforgeai/config/ci-answers.yaml.example (source template)
     - .devforgeai/config/github-actions.yaml (deployed operational config)
     - .devforgeai/config/ci-answers.yaml (deployed operational config)
   - **Reference files:** 6 files (~3,000 lines)
     - github-actions-setup-workflow.md
     - workflow-template-generation.md
     - cost-optimization-guide.md
     - headless-configuration.md
     - ci-validation-procedures.md
     - github-actions-troubleshooting.md
   - **Subagents:** internet-sleuth (auto-invoked for GitHub Actions best practices research)
   - **Invoked by:** /setup-github-actions command
   - **Provides:** Complete GitHub Actions infrastructure for DevForgeAI CI/CD
   - **Reusable:** Yes (any CI/CD needs, expandable to GitLab/CircleCI)
   - **Effort:** 12-16 hours (skill + references)

**Total Skill Count After EPIC-010:** 14 functional (+1 incomplete) → **15 functional skills**
- **DevForgeAI Core Workflow Skills (9):** ideation, architecture, orchestration, story-creation, ui-generator, development, qa, release, rca
- **DevForgeAI Infrastructure Skills (4 → 5):** documentation, feedback, mcp-cli-converter, subagent-creation, **github** (NEW)
- **Claude Code Infrastructure Skills (1):** claude-code-terminal-expert
- **Incomplete Skills (1):** internet-sleuth-integration (has assets/ and references/ but missing SKILL.md)
- **Note:** internet-sleuth functionality available via subagent (.claude/agents/internet-sleuth.md), not skill

---

---

## Implementation Effort Summary

### Total Effort Breakdown

**Feature Implementation:** 65 story points
- Phase 1 MVP: 42 points (6 features)
- Phase 2 CI/CD: 23 points (2 features including skill creation)

**Subagent Work:** 14-20 hours (~12 points)
- Create dependency-graph-analyzer: 6-8 hours
- Create file-overlap-detector: 4-6 hours
- Enhance git-validator → git-worktree-manager: 4-6 hours

**Skill Enhancements:** 24-34 hours (~20 points)
- devforgeai-development: 8-12 hours (4 new reference files)
- devforgeai-qa: 4-6 hours (2 new reference files)
- devforgeai-github (NEW): 12-16 hours (6 new reference files)

**Command Work:** 6-8 hours (~5 points)
- /worktrees command: 3-4 hours
- /setup-github-actions command: 3-4 hours

**Documentation:** 8-12 hours (~8 points)
- Parallel development guide
- GitHub Actions setup guide
- Cost optimization guide
- Troubleshooting guides

**Testing:** 16-24 hours (~15 points)
- Unit tests (subagents, skills, commands)
- Integration tests (2 concurrent stories)
- Regression tests (quality gates preserved)
- Cross-platform tests (Linux, macOS, Windows/WSL)

**Grand Total:** 65 + 12 + 20 + 5 + 8 + 15 = **125 story points**
**Timeline:** 9 weeks (Phase 1: 6 weeks, Phase 2: 3 weeks)
**Developer Time:** ~62-98 hours (10-16 developer days)

---

## Next Steps

1. **Review epic** - Validate 8 features, 3 subagents, 1 new skill, 4 commands align with parallel development vision
2. **Wait for EPIC-009** - Complete src/ migration first (prerequisite dependency)
3. **Create sprint plan** - Plan 4 sprints for complete epic (13 + 21 + 8 + 23 points)
4. **Generate stories** - Use /create-story for each of 8 features (6 MVP + 2 CI/CD)
5. **Create subagents** - Use /create-agent for dependency-graph-analyzer, file-overlap-detector
6. **Enhance git-validator** - Extend to git-worktree-manager capabilities
7. **Begin implementation** - Start with Feature 1 (worktree auto-management)
8. **Checkpoint decision** - After Week 6, decide on Phase 2 (CI/CD) based on MVP success

**Epic ready for story breakdown after EPIC-009 completes! 🚀**

---

## Architecture Impact Summary

**Before EPIC-010:**
- Commands: 23 (11 core workflow + 7 feedback + 4 maintenance + 1 documentation)
- Skills: 14 functional (13 devforgeai-* + 1 claude-code-terminal-expert) + 1 incomplete (internet-sleuth-integration)
- Subagents: 26
- Parallel capability: None (sequential only)
- CI/CD: Manual only

**After EPIC-010:**
- Commands: **25** (+2: /worktrees, /setup-github-actions)
- Skills: **15 functional** (+1: devforgeai-github) + 1 incomplete (unchanged)
- Subagents: **28** (+2 new: dependency-graph-analyzer, file-overlap-detector; +1 enhanced: git-worktree-manager)
- Parallel capability: **2-5 concurrent stories** (Git worktrees + dependency enforcement)
- CI/CD: **Automated** (GitHub Actions workflows with headless Claude Code)

**Key Improvements:**
- ✅ Time-to-completion: 50% reduction (8 stories in 16 hours vs 64 hours)
- ✅ Team scaling: Enabled (2-10 developers can work concurrently)
- ✅ Quality preservation: 100% (all gates unchanged)
- ✅ Dependency enforcement: Strict (transitive graphs, cascade blocking)
- ✅ File collision prevention: Complete (worktrees + scoped outputs + locks)
- ✅ Automation: Full (GitHub Actions for unattended execution)
- ✅ Cost-effective: $0.08-$0.12 per story (free tier sufficient for solo dev)
