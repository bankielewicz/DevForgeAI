---
id: EPIC-010
title: Parallel Story Development with CI/CD Integration
status: Planning
start_date: 2026-01-20
target_date: 2026-03-17
total_points: TBD
owner: Framework Maintainer
tech_lead: TBD
created: 2025-11-16
updated: 2025-11-16
complexity_score: 42
architecture_tier: 3
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
- AC5: Cleanup threshold configurable in .devforgeai/config/parallel.yaml

**Dependencies:** None (foundational feature)

**Deliverables:**
- Worktree manager module (Python or Bash)
- .devforgeai/config/parallel.yaml configuration
- Auto-create logic in /dev Phase 0
- Cleanup prompt in /dev Phase 0
- Documentation: Git worktrees for parallel development

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
- AC1: /dev STORY-037 runs tests with --results-directory=TestResults/STORY-037/
- AC2: /qa STORY-038 (concurrent) writes to TestResults/STORY-038/ (no collision)
- AC3: Coverage reports isolated: coverage/STORY-037/coverage.xml, coverage/STORY-038/coverage.xml
- AC4: QA reports reference correct test output paths
- AC5: Test isolation works for pytest, jest, dotnet test, go test

**Dependencies:** Feature 1 (worktrees provide file system isolation)

**Deliverables:**
- Test configuration updates (/dev Phase 2, /qa Phase 1)
- .devforgeai/config/test-isolation.yaml
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
- Dependency graph builder (Python module)
- Story template updated (depends_on field in YAML)
- Epic template updated (feature dependency section)
- /dev Phase 0 pre-flight dependency validation
- Circular dependency detector
- Documentation: Story dependency management guide

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
- AC5: Overlap report saved: .devforgeai/parallel/overlap-report-{timestamp}.md

**Dependencies:** Feature 3 (uses dependency graph data)

**Deliverables:**
- Spec parser for file_path extraction
- Git diff analyzer
- Overlap detection module
- Warning prompt integration (/dev Phase 0)
- Documentation: File overlap analysis guide

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
- AC1: /dev Phase 5 (git commit) acquires .devforgeai/.locks/git-commit.lock before committing
- AC2: If lock exists, waits with progress: "Waiting for git lock (held by STORY-037 PID 12345)... 15s"
- AC3: Stale lock detection: Lock >5 min old with dead PID auto-removed
- AC4: Lock timeout: After 10 min waiting, prompt: "(1) Continue waiting, (2) Force acquire lock (risky), (3) Abort"
- AC5: Lock released after successful commit

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

**Sprint 4 (Weeks 7-8): Automation**
7. STORY-TBD: GitHub Actions Workflow Templates (13 points) - **Deferred**
8. STORY-TBD: Headless Mode Answer Configuration (5 points) - **Deferred**
**Total:** 18 points

**Phase 2 Total:** 2 stories, 18 points, 2 weeks

**Grand Total:** 8 stories, 60 points, 8 weeks (Phase 1: 42 points, Phase 2: 18 points)

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
| Test outputs | TestResults/ | TestResults/{story_id}/ | ⚠️ CHANGE (but compatible) |

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

## Next Steps

1. **Review epic** - Validate 6+2 features align with parallel development vision
2. **Wait for EPIC-009** - Complete src/ migration first (prerequisite)
3. **Create sprint plan** - Plan 3 sprints for Phase 1 (13 + 21 + 8 points)
4. **Generate stories** - Use /create-story for each of 6 features
5. **Begin implementation** - Start with Feature 1 (worktree auto-management)
6. **Checkpoint decision** - After Week 6, decide on Phase 2 (CI/CD)

**Epic ready for story breakdown after EPIC-009 completes! 🚀**
