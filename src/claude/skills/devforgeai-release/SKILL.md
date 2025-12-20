---
name: devforgeai-release
description: Orchestrate production releases with deployment automation, smoke testing, rollback capabilities, and release documentation. Use after QA approval to deploy stories to production. Supports multiple deployment strategies (blue-green, canary, rolling, recreate) and environments (staging, production). Enforces release gates and maintains deployment audit trail.
model: claude-haiku-4-5-20251001
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - AskUserQuestion
  - Bash(git:*)
  - Bash(kubectl:*)
  - Bash(docker:*)
  - Bash(terraform:*)
  - Bash(ansible:*)
  - Bash(az:*)
  - Bash(aws:*)
  - Bash(gcloud:*)
  - Bash(helm:*)
  - Bash(dotnet:*)
  - Bash(npm:*)
  - Bash(pytest:*)
  - Skill
---

# DevForgeAI Release Skill

Automate production releases with staging validation, smoke testing, and rollback capabilities.

---

## ⚠️ EXECUTION MODEL: This Skill Expands Inline

**After invocation, YOU (Claude) execute these instructions phase by phase.**

**When you invoke this skill:**
1. This SKILL.md content is now in your conversation
2. You execute each phase sequentially
3. You display results as you work through phases
4. You complete with success/failure report

**Do NOT:**
- ❌ Wait passively for skill to "return results"
- ❌ Assume skill is executing elsewhere
- ❌ Stop workflow after invocation

**Proceed to "Parameter Extraction" section below and begin execution.**

---

## Parameter Extraction

This skill extracts story ID, environment (staging/production), and deployment strategy from conversation context.

**Skills cannot accept runtime parameters.** All information extracted from conversation (YAML frontmatter, explicit statements, or file references).

**See `references/parameter-extraction.md` for complete extraction algorithm.**

---

## Purpose

Orchestrate safe, automated deployments to staging and production environments with comprehensive validation and rollback capabilities.

### Core Capabilities

1. **Automated Deployment** - Platform-agnostic (K8s, Docker, AWS, Azure, GCP, Vercel, Netlify, VPS)
2. **Progressive Rollout** - Blue-green, canary, rolling, recreate strategies
3. **Smoke Testing** - Health checks, critical path validation, performance verification
4. **Rollback Capability** - Automatic rollback on failure detection
5. **Release Documentation** - Release notes, changelog, audit trail
6. **Multi-Environment** - Staging-first with production promotion

### Philosophy

**"Deploy with Confidence, Fail Gracefully, Safety Over Speed"**

- Automated checks prevent broken deployments
- Quick rollback maintains availability
- QA approval required (never skip gates)
- Complete audit trail for compliance

---

## When to Use This Skill

**Use when:**
- ✅ Story status = "QA Approved" (ready for production)
- ✅ Coordinated sprint releases (multiple stories together)
- ✅ Hotfix deployments (critical bug fix, still requires QA)
- ✅ Rollback operations (production issue detected)

**Prerequisites:** QA approved, tests passing, build successful, config exists in `devforgeai/deployment/`

**Invoked by:**
- `/release` command (user-initiated)
- devforgeai-orchestration skill (automated progression)

---

## Configuration

Platform configs required in `devforgeai/deployment/` (K8s, Docker, AWS, Azure, GCP, Vercel, Netlify, VPS)

Smoke tests config in `devforgeai/smoke-tests/config.json` (URLs, test users, API keys)

**See `references/configuration-guide.md` for schemas and examples.**

---

## Release Workflow (8 Phases)

**⚠️ EXECUTION STARTS HERE - You are now executing the skill's workflow.**

Each phase loads its reference file on-demand for detailed implementation.

### Phase 1: Pre-Release Validation
**Purpose:** Validate all prerequisites before deployment
**Reference:** `pre-release-validation.md`
**Checklist:** `release-checklist.md`
**Validates:** QA approval, tests passing, build success, config exists, dependencies released
**Output:** Validation status (PASS/FAIL with details)

### Phase 2: Staging Deployment
**Purpose:** Deploy to staging environment and run smoke tests
**Reference:** `staging-deployment.md`
**Guides:** `deployment-strategies.md`, `platform-deployment-commands.md`, `smoke-testing-guide.md`
**Steps:** Deploy → Smoke test → Health check → Validate
**Output:** Staging deployment complete, smoke tests passed

### Phase 2.5: Post-Staging Hooks (NEW - STORY-025)
**Purpose:** Trigger retrospective feedback after staging deployment
**Reference:** `post-staging-hooks.md`
**Invokes:** `devforgeai-validate check-hooks --operation=release-staging --status=$STATUS`
**Conditional:** Only invokes `devforgeai-validate invoke-hooks` if check-hooks returns 0 (eligible)
**Graceful Degradation:** Hook failures logged, deployment proceeds regardless
**Output:** Feedback collected (if hooks enabled), deployment continues

### Phase 3: Production Deployment
**Purpose:** Deploy to production with progressive rollout
**Reference:** `production-deployment.md`
**Guides:** `deployment-strategies.md`, `platform-deployment-commands.md`
**Strategies:** Blue-green (zero downtime), canary (progressive), rolling (gradual), recreate (simple)
**Output:** Production deployment complete with chosen strategy

### Phase 3.5: Post-Production Hooks (NEW - STORY-025)
**Purpose:** Trigger retrospective feedback after production deployment
**Reference:** `post-production-hooks.md`
**Invokes:** `devforgeai-validate check-hooks --operation=release-production --status=$STATUS`
**Conditional:** Only invokes `devforgeai-validate invoke-hooks` if check-hooks returns 0 (eligible)
**Default Behavior:** Failures-only mode (skips feedback on production success unless configured)
**Graceful Degradation:** Hook failures logged, deployment proceeds regardless
**Output:** Feedback collected (if hooks enabled and eligible), deployment continues

### Phase 4: Parallel Post-Deployment Validation (UPDATED - STORY-113)

**⚠️ CHECKPOINT: You MUST execute health checks AND smoke tests in PARALLEL (same batch)**

**Step 4.0: Load Parallel Smoke Test Reference (REQUIRED)**
```
Read(file_path=".claude/skills/devforgeai-release/references/parallel-smoke-tests.md")
```

**After loading:** Execute the parallel validation workflow. This phase runs health checks and smoke tests concurrently for 3-5x performance improvement.

**Purpose:** Execute comprehensive smoke tests on production with parallel execution

**Step 4.1: Load Parallel Configuration**
```
Read(file_path="devforgeai/config/parallel-orchestration.yaml")
max_concurrent = config.profiles[active_profile].max_concurrent_tasks
timeout_ms = config.profiles[active_profile].timeout_ms
```

**Step 4.2: Execute Parallel Health Checks + Smoke Tests**

Execute in SINGLE message (concurrent batch):
```
# Health checks (in parallel batch)
Bash(command="curl -s -o /dev/null -w '%{http_code}' $HEALTH_ENDPOINT_1")
Bash(command="curl -s -o /dev/null -w '%{http_code}' $HEALTH_ENDPOINT_2")

# Smoke tests (same parallel batch)
Bash(command="npm test -- --testNamePattern='smoke'")
Bash(command="pytest tests/smoke/ -v")
```

**Step 4.3: Aggregate Results Using PartialResult**
```
partial_result = aggregate_parallel_results(bash_outputs)

IF partial_result.success_rate < 0.5:
    Trigger rollback procedure
    HALT: "Post-deployment validation failed"
```

**Reference Files:**
- `parallel-smoke-tests.md` (STORY-113) - Parallel execution patterns
- `post-deployment-validation.md` - Detailed validation steps
- `smoke-testing-guide.md`, `monitoring-metrics.md` - Test definitions

**Success Threshold:** 50% (more lenient than QA, allows rollback decision)

**Phase 4 Completion Checklist:**
Before proceeding to Phase 5, verify:
- [ ] Loaded parallel-smoke-tests.md (Step 4.0)
- [ ] Loaded parallel configuration (Step 4.1)
- [ ] Executed health checks AND smoke tests in SINGLE message (Step 4.2)
- [ ] Aggregated results into PartialResult model
- [ ] Validated success_rate >= 0.5 (50%)
- [ ] IF failed: Triggered rollback procedure
- [ ] Displayed parallel validation results

**Display to user:**
```
✓ Phase 4 Complete: Parallel Post-Deployment Validation
  Health checks: [X] of [Y] passed
  Smoke tests: [X] of [Y] passed
  Overall success rate: [X]% (threshold: 50%)
  Duration: [X]s (vs ~[5X]s sequential)
```

**IF success_rate < 50%:** Trigger rollback and HALT.

### Phase 5: Release Documentation
**Purpose:** Generate release notes and update story
**Reference:** `release-documentation.md`
**Updates:** Story status = "Released", workflow history, release notes, changelog
**Output:** Documentation complete, audit trail created

### Phase 6: Post-Release Monitoring & Closure
**Purpose:** Set up monitoring and close story
**Reference:** `monitoring-closure.md`
**Guide:** `monitoring-metrics.md`
**Setup:** Error tracking, performance monitoring, alerting rules
**Output:** Monitoring configured, story closed

**See individual phase reference files for complete deployment workflows.**

---

## Rollback Procedures

**Automatic triggers:** Smoke tests fail, health checks fail, error rate spike, performance degradation

**Manual triggers:** User-initiated (AskUserQuestion) or post-release issues

**Execution:** Revert to previous stable deployment, run smoke tests, update story, alert team

**See `references/rollback-procedures.md` for complete procedures.**

---

## Integration Points

**From devforgeai-qa:** Story status "QA Approved" enables release

**To devforgeai-orchestration:** Release completion triggers next story

**Invokes:** deployment-engineer subagent, security-auditor subagent (production only)

**Updates:** Story status ("QA Approved" → "Releasing" → "Released"), workflow history, release notes

---

## Success Criteria

Release complete when:
- [ ] Staging deployment + smoke tests passed
- [ ] Production deployment + smoke tests passed
- [ ] Release notes generated
- [ ] Story status = "Released"
- [ ] Monitoring configured
- [ ] Audit trail complete

---

## Reference Files

Load these on-demand during workflow execution.

### Workflow Files (11 files)
- **parameter-extraction.md** (104 lines) - Story ID, environment, strategy extraction algorithm
- **configuration-guide.md** (52 lines) - Platform config requirements, schemas, examples
- **pre-release-validation.md** (66 lines) - Phase 1: Validation checks and release gates
- **staging-deployment.md** (75 lines) - Phase 2: Staging workflow and smoke testing
- **post-staging-hooks.md** (NEW - STORY-025) - Phase 2.5: Hook integration after staging deployment
- **production-deployment.md** (69 lines) - Phase 3: Production deployment with strategies
- **post-production-hooks.md** (NEW - STORY-025) - Phase 3.5: Hook integration after production deployment
- **parallel-smoke-tests.md** (NEW - STORY-113) - Phase 4: Parallel smoke test execution patterns
- **post-deployment-validation.md** (58 lines) - Phase 4: Smoke tests and health checks
- **release-documentation.md** (65 lines) - Phase 5: Release notes and audit trail
- **monitoring-closure.md** (29 lines) - Phase 6: Monitoring setup and story closure

### Guide Files (6 files - existing)
- **deployment-strategies.md** (322 lines) - Blue-green, canary, rolling, recreate strategies
- **monitoring-metrics.md** (891 lines) - Health check metrics, alerting rules, SLIs/SLOs
- **platform-deployment-commands.md** (731 lines) - Kubernetes, Docker, AWS, Azure, GCP commands
- **release-checklist.md** (572 lines) - Pre-release validation checklist and gate definitions
- **rollback-procedures.md** (178 lines) - Rollback execution procedures and recovery strategies
- **smoke-testing-guide.md** (389 lines) - Post-deployment test procedures and validation

**Total: 17 reference files, ~4,800 lines of comprehensive deployment guidance.**
- 11 workflow files (phases 1-6 + 2 hook phases + 1 parallel pattern)
- 6 guide files (strategies, monitoring, platforms, checklists, rollback, smoke testing)

**Progressive loading ensures only needed references consume tokens during execution.**

**Hook Integration (STORY-025):**
- Phase 2.5 and 3.5 add retrospective feedback collection
- Non-blocking: Hook failures never affect deployment status
- Configurable: `devforgeai/config/hooks.yaml` controls behavior
- See: `post-staging-hooks.md` and `post-production-hooks.md` for implementation details
